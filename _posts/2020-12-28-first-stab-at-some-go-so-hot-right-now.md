---
title: "First stab at some Go (so hot right now)"
date: 2020-12-28
categories: 
  - "golang"
tags: 
  - "go"
  - "golang"
  - "hansel"
  - "python"
layout: post
---

It may be a combination of starting to go stir crazy over the Christmas break and some self loathing at the amount of FIFA i've been playing that's driven me to finally start learning some Go for a few data science and machine learning related projects i'm working on where it offers unique advantages.

(In reality, the final straw here was a long discussion with an SRE colleague who explained to me how much easier it would be for us to ship the ML code in Go vs Python which should, for our project, ultimately make it easier for people to adopt and use the ML powered features - which is really what i'm most interested in, even if i may not yet have as many fancy ML models and libraries to leverage in Go).

So the first step of my journey is actually pulling the data (using asynchronous goroutines - like i said, so hot right now) i need from a list of api endpoints and basically shoving it into the equivalent of a [Pandas](https://pandas.pydata.org/) dataframe in Go.

I am using the [Gota](https://github.com/go-gota/gota) package, but there is also a few others you can see [here](https://github.com/avelino/awesome-go#data-structures).

So after a bit of searching around and some YouTube videos below is a verbosely commented version of what i have that i think is a decent enough starting point for now (would appreciate any tips if you know Go and have any suggestions).

I think i might actually quite like this Go malarky, or at least continue learning it to make me feel like the hipster i really wish i was.

p.s. I will probably make some more posts as I learn more.

```go
package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
    "regexp"
    "strings"
    "sync"

    "github.com/go-gota/gota/dataframe"
)

// Create a wait group
var wg sync.WaitGroup

// Get api response (expects format=csv) and make a dataframe from it
func getDf(url string, c chan dataframe.DataFrame) {

    // Need to make sure we tell wait group we done
    defer wg.Done()

    // Pull chart name from the url
    re := regexp.MustCompile("chart=(.*?)&")
    match := re.FindStringSubmatch(url)
    chart := match[1]
    resp, _ := http.Get(url)

    // Get body as string for ReadCSV
    bodyBytes, _ := ioutil.ReadAll(resp.Body)
    bodyString := string(bodyBytes)
    df := dataframe.ReadCSV(strings.NewReader(bodyString))

    // Add chart suffix to each col name
    // (ignore first col which should be "time" and used for joins later)
    colnames := df.Names()
    for i, colname := range colnames {
        if i != 0 {
            df = df.Rename(chart+"|"+colname, colname)
        }
    }

    // send df to channel
    c <- df

}

func main() {

    // Define a list of api calls we want data from
    // In this example we have an api call for each chart data we want in our df
    urls := []string{
        "https://london.my-netdata.io/api/v1/data?chart=system.cpu&format=csv&after=-10",
        "https://london.my-netdata.io/api/v1/data?chart=system.net&format=csv&after=-10",
        "https://london.my-netdata.io/api/v1/data?chart=system.load&format=csv&after=-10",
        "https://london.my-netdata.io/api/v1/data?chart=system.io&format=csv&after=-10",
    }

    // Create a channel of dataframes the size of number of api calls we need to make
    dfChannel := make(chan dataframe.DataFrame, len(urls))

    // Create empty df we will outer join into from the df channel later
    df := dataframe.ReadJSON(strings.NewReader(`[{"time":"1900-01-01 00:00:01"}]`))

    // Kick off a go routine for each url
    for _, url := range urls {
        wg.Add(1)
        go getDf(url, dfChannel)
    }

    // Handle synchronization of channel
    wg.Wait()
    close(dfChannel)

    // Pull each df from the channel and outer join onto our original empty df
    for dfTmp := range dfChannel {
        df = df.OuterJoin(dfTmp, "time")
    }

    // Sort based on time
    df = df.Arrange(dataframe.Sort("time"))

    // Print df
    fmt.Println(df, 10, 5)

    // Describe df
    //fmt.Println(df.Describe())

}
```

Which should return something that looks kinda like a Pandas DataFrame!

<figure>

![](/assets/images/2020-12-28-first-stab-at-some-go-so-hot-right-now/go-1-1024x467.jpg)

<figcaption>

Yes Powershell, come at me bro!

</figcaption>

</figure>

Here is a list of some useful links and resources i've used to get this far:

- Great [freeCodeCamp course](https://www.youtube.com/watch?v=YS4e4q9oBaU) (first time i've used anything from freeCodeCamp - was very impressed and have subscribed!).
- Stumbled upon [this Go series](https://pythonprogramming.net/go/introduction-go-language-programming-tutorial/) from sentdex which was great as I love everything he does.
- A [really clear video](https://www.youtube.com/watch?v=LvgVSSpwND8) from [Jake Wright](https://twitter.com/jakewrightuk).
- [Awesome Go list](https://github.com/avelino/awesome-go#data-structures) because of course.
- A more higher level [Go DS/ML related talk](https://www.youtube.com/watch?v=gwg_YXyCYBw) from [Sam Kreter](https://twitter.com/samkreter).
