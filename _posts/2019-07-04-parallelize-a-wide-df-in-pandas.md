---
title: "Parallelize a wide df in Pandas"
date: 2019-07-04
tags: 
  - "data-science"
  - "multiprocessing"
  - "pandas"
  - "python"
layout: post
---

<figure>

![](/assets/images/2019-07-04-parallelize-a-wide-df-in-pandas/capture.jpg)

<figcaption>

I was going to make a pretty picture.

</figcaption>

</figure>

Sometimes you end up with a very [wide](https://en.wikipedia.org/wiki/Wide_and_narrow_data#Wide) pandas dataframe and you are interested in doing the same types of operations (data processing, building a model etc.) but focused on subsets of the columns.

For example if we had a wide df with different time series kpi's represented as columns then we might want to do something like look at each kpi at a time, apply some pre-processing and build something like an [ARIMA](https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/) time series model perhaps.

This is the situation i found myself in recently and it took me best part of an afternoon to figure out. Usually when i find myself in that situation i try and squeeze out a blog post in case might be useful for someone else or future me.

<figure>

![](/assets/images/2019-07-04-parallelize-a-wide-df-in-pandas/code.png)

<figcaption>

All the code in one glorious screenshot!

</figcaption>

</figure>

**Note**: repository with all code is [here](https://github.com/andrewm4894/parallelize_wide_df). p.s. thanks to [this](https://towardsdatascience.com/make-your-own-super-pandas-using-multiproc-1c04f41944a1) and [this](http://www.racketracer.com/2016/07/06/pandas-in-parallel/) post that i built off of.

For this example i'm afraid i'm going to use the Iris dataset :0 . This example is as minimal and easy as i could throw together, basically the aim of the code is to:

1. Build some function to take in a df, do some processing and spit out a new df.
2. Have that function be parameterized in some way as might be needed (e.g if you wanted to do slightly different work for one subset of columns).
3. Apply that function in parallel across the different subsets of your df that you want to process.

There are two main functions of interest here **parallelize\_dataframe()** and **do\_work()** both of which live in their own file called [my\_functions.py](https://github.com/andrewm4894/parallelize_wide_df/blob/master/my_functions.py) which can be imported into your jupyter notebook.

https://gist.github.com/andrewm4894/932304809840d6cef7ed5c7fc21b72cb

**parallelize\_dataframe()** does the below things:

1. Break out df into a list of df's based on the col\_subsets list passed in as a parameter.
2. Wrap the function that was passed in into a partial along with the kwargs (this is how your parameters make it into the do\_work() function).
3. Use map() from [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) to apply the func (along with the args you want to send it) to each subset of columns from your df in parallel.
4. Reduce all this back into on final df by joining all the resulting df's from the map() output into one wide df again (note the assumption here of joining back on the df indexes - they need to be stable and meaningful).

The **do\_work()** function in this example is just a simple function to add some new columns as examples of types of pandas (or any other) goodness you might want to do. In reality in my case it would be more like a **apply\_model()** type function that would take each subset of columns, do some feature extraction, train a model and then also score the data as needed to.

Having the ability to do this for multiple subsets of columns in your wide df can really free up your time to focus on the more important things like dickying around with model parameters and different pre-processing steps :)

That's pretty much it, a productive afternoon (in the play center with kids i might add) and am quite pleased with myself.

**Update:** One addition i made to this as things got more complicated when i went to implement it was the ability to apply different function params to each subset df. For example if you wanted to pass in different parameters to the function for different columns. In the [do\_parallel\_zip.ipynb](https://github.com/andrewm4894/parallelize_wide_df/blob/master/do_parallel_zip.ipynb) and corresponding [my\_functions\_zip.py](https://github.com/andrewm4894/parallelize_wide_df/blob/master/my_functions_zip.py) (i'm calling them "\_zip" as they use [zip()](https://www.w3schools.com/python/ref_func_zip.asp) to "zip" up both the df\_list and the corresponding kwargs to go with it to be unpacked later by [do\_work\_zip()](https://github.com/andrewm4894/parallelize_wide_df/blob/master/my_functions_zip.py#L34)).

To be concrete, if we wanted to multiply the "sepal\_..." cols by 100 and the "petal\_.." cols by 0.5. We could use the "zip" approach like below (notebook [here](https://github.com/andrewm4894/parallelize_wide_df/blob/master/do_parallel_zip.ipynb)):

![](/assets/images/2019-07-04-parallelize-a-wide-df-in-pandas/capture-2.jpg)

Which is using the "zip" approach in [parallelize\_dataframe\_zip()](https://github.com/andrewm4894/parallelize_wide_df/blob/master/my_functions_zip.py#L6)

![](/assets/images/2019-07-04-parallelize-a-wide-df-in-pandas/capture-3.jpg)

Where the zipped iterable is then unpacked as needed by the [do\_work\_zip()](https://github.com/andrewm4894/parallelize_wide_df/blob/master/my_functions_zip.py#L34) function:

![](/assets/images/2019-07-04-parallelize-a-wide-df-in-pandas/capture-4.jpg)
