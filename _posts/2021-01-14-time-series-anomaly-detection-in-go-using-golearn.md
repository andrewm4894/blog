---
title: "Time series anomaly detection in Go using GoLearn"
date: 2021-01-14
categories: 
  - "anomaly-detection"
  - "golang"
  - "machine-learning"
  - "time-series"
tags: 
  - "anomaly-detection"
  - "go"
  - "machine-learning"
  - "time-series"
layout: post
---

<figure>

![](/assets/images/2021-01-14-time-series-anomaly-detection-in-go-using-golearn/go-1024x614.jpg)

<figcaption>

Output of the Go script.

</figcaption>

</figure>

I've posted recently about learning just enough Go to be dangerous over the christmas break, well here is a update on my adventures so far.

The below script (which is probably horrible in places if you know Go properly - tips welcome) uses goroutines to pull data from some REST API endpoints and then use GoLearn to train a model and start producing anomaly scores for new observations.

```go
package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "sync"
    "time"

    "github.com/sjwhitworth/golearn/base"
    "github.com/sjwhitworth/golearn/trees"
    "gonum.org/v1/gonum/mat"
)

// Create a wait group
var wg sync.WaitGroup

// Struct used to unmarshal json from netdata api
type netdataResponse struct {
    Labels []string    `json:"labels"`
    Data   [][]float64 `json:"data"`
}

// Get instances from the netdata api
func getInstances(host, chart, after, before string, lags, diffs, smoothing int, c chan map[string]base.FixedDataGrid) {

    // Need to make sure we tell wait group we done
    defer wg.Done()

    // Create response
    var data netdataResponse

    // Get response from netdata rest api
    resp, _ := http.Get("https://" + host + "/api/v1/data?chart=" + chart + "&format=json&after=" + after + "&before=" + before)
    bodyBytes, _ := ioutil.ReadAll(resp.Body)

    // Unmarshal into netdataResponse
    _ = json.Unmarshal([]byte(bodyBytes), &data)

    // Flatten data into one slice, ignoring the first column which is always "time", and adding nLags
    nDims := len(data.Labels) - 1
    nCols := nDims + (lags * nDims)
    nRows := len(data.Data) - lags

    // Make flat slice to put data into
    dataFlat := make([]float64, nCols*nRows)

    // Loop over and add lags to flat data
    i := 0
    for t := range data.Data {
        //fmt.Println(data.Data[t])
        if t >= (lags + diffs) {
            for dim := range data.Data[t] {
                // Ignore time which is the first dim in the response
                if dim > 0 {
                    // Add each lag
                    for l := 0; l <= lags; l++ {
                        if diffs > 0 {
                            dataFlat[i] = data.Data[t-l][dim] - data.Data[t-l-diffs][dim]
                        } else {
                            dataFlat[i] = data.Data[t-l][dim]
                        }
                        i++
                    }
                }
            }
        }
    }

    // Create instances
    instances := base.InstancesFromMat64(nRows, nCols, mat.NewDense(nRows, nCols, dataFlat))
    //fmt.Println(instances)

    // Must set a class attribute in golearn
    // Ok to just use any feature as per comment here:
    // https://github.com/sjwhitworth/golearn/issues/260#issuecomment-756086922
    attrArray := instances.AllAttributes()
    instances.AddClassAttribute(attrArray[0])

    // Create map for data so we can later identify what comes back from the channel
    instancesMap := make(map[string]base.FixedDataGrid, 1)
    instancesMap[host+"|"+chart] = instances

    // Send to channel
    c <- instancesMap

}

func fitModel(instances base.FixedDataGrid, nTrees, maxDepth, subSpace int) trees.IsolationForest {
    forest := trees.NewIsolationForest(nTrees, maxDepth, subSpace)
    forest.Fit(instances)
    return forest
}

func main() {

    // How many steps to run for
    var nSteps = 30

    // How often to retrain models
    var trainEvery = 15

    // define config for each chart we want and anomaly score for
    var host = "london.my-netdata.io"
    var trainAfter = "-100"
    var trainBefore = "0"
    var lags = 1
    var diffs = 0
    var smoothing = 2
    config := map[string]map[string]interface{}{
        "1": {"host": host, "chart": "system.net", "trainAfter": trainAfter, "trainBefore": trainBefore, "lags": lags, "diffs": diffs, "smoothing": smoothing},
        "2": {"host": host, "chart": "system.ram", "trainAfter": trainAfter, "trainBefore": trainBefore, "lags": lags, "diffs": diffs, "smoothing": smoothing},
    }

    // Create map to store trained models in
    trainedModels := make(map[string]trees.IsolationForest, len(config))

    // Run for nSteps
    for i := 0; i <= nSteps; i++ {

        // Train models
        if i%trainEvery == 0 {

            // Get training data
            trainDataChannel := make(chan map[string]base.FixedDataGrid, len(config))

            // Get training data
            for _, conf := range config {
                wg.Add(1)
                go getInstances(
                    conf["host"].(string),
                    conf["chart"].(string),
                    conf["trainAfter"].(string),
                    conf["trainBefore"].(string),
                    conf["lags"].(int),
                    conf["diffs"].(int),
                    conf["smoothing"].(int),
                    trainDataChannel,
                )
            }
            wg.Wait()
            close(trainDataChannel)

            // Train each model and save it to trainedModels
            for trainInstancesMap := range trainDataChannel {
                for trainInstancesKey, trainInstancesData := range trainInstancesMap {
                    fmt.Printf("\nTraining %v model at: %v (step %v)\n", trainInstancesKey, time.Now().Unix(), i)
                    trainedModels[trainInstancesKey] = fitModel(trainInstancesData, 10, 10, 100)
                }
            }

        }

        // Get prediction data
        predDataChannel := make(chan map[string]base.FixedDataGrid, len(config))
        for _, conf := range config {
            wg.Add(1)
            go getInstances(
                conf["host"].(string),
                conf["chart"].(string),
                //string(-1*conf["lags"].(int)+conf["diffs"].(int)),
                "-20",
                "0",
                conf["lags"].(int),
                conf["diffs"].(int),
                conf["smoothing"].(int),
                predDataChannel,
            )
        }
        wg.Wait()
        close(predDataChannel)

        // Make predictions
        preds := make(map[string]float64)
        for predInstancesMap := range predDataChannel {
            for predInstancesKey, predInstancesData := range predInstancesMap {
                //fmt.Println(predInstancesKey)
                //fmt.Println(predInstancesData)
                model := trainedModels[predInstancesKey]
                recentPreds := model.Predict(predInstancesData)
                //fmt.Println(recentPreds)
                preds[predInstancesKey] = recentPreds[len(recentPreds)-1-diffs]
            }
        }

        // Print scores at each step
        fmt.Printf("\nAnomaly scores (step %v) as at: %v\n", i, time.Now().Unix())
        fmt.Println(preds)

        time.Sleep(500 * time.Millisecond)

    }

}
```
