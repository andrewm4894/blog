---
title: "Parallel Jupyter Notebooks"
date: 2019-04-27
tags: 
  - "jupyter"
  - "multiprocessing"
  - "papermill"
  - "python"
---

I have become master of the notebooks, they bend at my will and exist to serve my data science needs!

![](/assets/images/2019-04-27-parallel-jupyter-notebooks/tenor-1.gif)

Ok i might be getting a bit carried away, but i recently discovered [papermill](https://papermill.readthedocs.io/en/latest/) and have been finding it very useful in conjunction with Python [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) to speed up a lot of data science experimental type work. So useful in fact, i was motivated to write a post on a Saturday night!

_Note: All the code for this post is_ [_here_](https://github.com/andrewm4894/papermill_dev)_._

### One problem with notebooks

I'm generally (have swayed back and forth) a fan of notebooks but am wary of some of the downsides or costs they can impose. When doing experimental type work, if your not careful, you can end up with lots of duplicated code or what i think of as "notebook instances", where you have ran your notebook many times on different (but similar) datasets and with different (but similar) parameters.

_Aside: Great [talk](https://www.youtube.com/watch?v=7jiPeIFXb6U) and [deck](https://docs.google.com/presentation/d/1n2RlMdmv1p25Xy5thJUhkKGvjtV-dkAIsUXP-AL4ffI/edit#slide=id.g3a428e2eb8_0_331) from_ [_@joelgrus_](https://twitter.com/joelgrus/status/1033035196428378113) _(who is great - and who's meme game is very strong) on some drawbacks of notebooks._

Having the executed notebooks themselves become self documenting artifacts relating to the experiment is really useful - the code you ran and its outputs in one place. But when you start building new features on top of these "notebook instances" as you iterate on the research, things can quickly get messy.

Where I've found papermill to be very useful is in basically template-ing up your notebooks in one single place and paramaterizing them such that the actual living notebook code and the executed "notebook instances" have a much cleaner separation.

I'll try make this clearer with an example.

### [data\_explorer](https://github.com/andrewm4894/papermill_dev/blob/master/notebooks/data_explorer.ipynb) Notebook

Lets suppose you have a notebook that you often use on new datasets (in reality it's more likely to be some more complicated ml pipeline type notebook for quickly experimenting on updated datasets with while maintaining some common structure in how you go about things).

In this example its a [simple notebook](https://nbviewer.jupyter.org/github/andrewm4894/papermill_dev/blob/master/notebooks/data_explorer.ipynb?cache=false) to download a dataset and just do some descriptive stats and plotting.

The main idea here is to paramaterize the whole notebook as much as possible. This is done with a json dictionary called "config". So the idea is that everything the notebook needs is pretty much defined in the first cell.

```
config = {        "data_url" :"https://raw.githubusercontent.com/andrewm4894/papermill_dev/master/data/titanic.csv"     }
```

In this case, the [data\_explorer](https://nbviewer.jupyter.org/github/andrewm4894/papermill_dev/blob/master/notebooks/data_explorer.ipynb?cache=false) notebook just takes in one parameter called "data\_url". It then downloads from this url into a pandas dataframe and does some basic plotting. In reality this "config" dict can contain all the input parameters you need to define and execute you notebook. For example it could be defining the type of models to build against your data, what data to use, model parameters, where to store outputs etc. anything and everything really.

### Enter Papermill

So lets say you now have a number of different datasets that you want to run through your data\_explorer notebook. You could manually update the config and then just rerun the notebook 3 times (making sure to restart the kernel and clear all each time), maybe saving outputs into specific locations. Or worse you could make 3 copies of your notebook and just run them each individually (don't do this, future you will hate it).

Much better is to let papermill kick off the execution of the notebooks so you have a clear separation between the notebooks your code lives in (in this case, the [notebooks](https://github.com/andrewm4894/papermill_dev/tree/master/notebooks) folder of the repo) and the outputs or "notebook instances" of running the same notebooks multiple times against different data or the same data but with slightly different parameters (in this case the [papermill\_outputs](https://github.com/andrewm4894/papermill_dev/tree/master/papermill_outputs) folder according to a convention you can control).

Two things let us do this, a python script ([run\_nb\_batch.py](https://github.com/andrewm4894/papermill_dev/blob/master/run_nb_batch.py)) that uses papermill and multiprocessing to kick of parallel notebook executions as defined in a json file defining the notebooks to be run and their configs to be run with [configs.json](https://github.com/andrewm4894/papermill_dev/blob/master/configs.json).

**[run\_nb\_batch.py:](https://github.com/andrewm4894/papermill_dev/blob/master/run_nb_batch.py)**

https://gist.github.com/andrewm4894/ceeac7a4984ba636ebfadfb120972e48

**[configs.json](https://github.com/andrewm4894/papermill_dev/blob/master/configs.json)**

https://gist.github.com/andrewm4894/5e4d57d1d89bd663e6ede5a1a6aca1f9

The idea is to loop through each config in the [configs.json](https://github.com/andrewm4894/papermill_dev/blob/master/configs.json) file and execute the specified notebook with the specified configuration. Executed notebooks then go to a predefined output file such as [papermill\_outputs/data\_explorer/adult/data\_explorer\_adult.ipynb](https://github.com/andrewm4894/papermill_dev/blob/master/papermill_outputs/data_explorer/adult/data_explorer_adult.ipynb).

In this case i've chosen the naming convention of /papermill\_outputs/<notebook\_name>/<output\_label>/<notebook\_name>\_<output\_label> .ipynb but obviously you can chose whatever you want.

That's pretty much it for this one. Feel free to clone the repo and play around with it or add improvements as you like.

I've been finding that this sort of approach to template-ing up core notebooks you end up using quite a lot (albeit with slightly different params etc.) along with a standardized approach using something like [mlflow](https://mlflow.org/) to further instrument and store artifacts of your notebook runs can make running multiple 'experiments' on your data in parallel much easier and overall help make you a bit more productive.

**Update**: I decided to make a quick video as sometimes easier to just see what we are doing. (Sorry audio quality a bit bad (and poor resolution), first time :))

https://www.youtube.com/watch?v=nwuQ2fpBltY
