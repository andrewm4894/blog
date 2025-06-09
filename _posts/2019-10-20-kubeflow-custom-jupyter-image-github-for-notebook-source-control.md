---
title: "KubeFlow Custom Jupyter Image (+ github for notebook source control)"
date: 2019-10-20
categories: 
  - "kubeflow"
  - "machine-learning"
tags: 
  - "jupyter"
  - "kubeflow"
  - "machine-learning"
  - "python"
---

I've been playing around a bit with [KubeFlow](https://www.kubeflow.org/) a bit lately and found that a lot of the tutorials and [examples](https://github.com/kubeflow/examples/blob/master/pipelines/simple-notebook-pipeline/Simple%20Notebook%20Pipeline.ipynb) of Jupyter notebooks on KubeFlow do a lot of the `pip install` and other sort of setup and config stuff in the notebook itself which feels icky.

![](/assets/images/2019-10-20-kubeflow-custom-jupyter-image-github-for-notebook-source-control/3duv0s.jpg)

But, in reality, if you were working in Jupyter notebooks on KubeFlow for real you'd want to build a lot of this into the image used to build the notebook server. Luckily, as with most of KubeFlow, its pretty flexible to customize and extend as you want, in this case by adding [custom jupyter images](https://www.kubeflow.org/docs/notebooks/custom-notebook/).

Two main example use cases you'd want to do this are for ensuring some custom python package (e.g. [my\_utils](https://github.com/andrewm4894/my_utils)) you have built is readily available in all your notebooks, and other external libraries that you use all the time are also available - e.g. [kubeflow pipelines](https://pypi.org/project/kfp/).

To that end, [here](https://github.com/andrewm4894/my-kf-jupyter/blob/master/Dockerfile) is a Dockerfile that illustrates this (and [here](https://cloud.docker.com/repository/docker/andrewm4894/my-kf-jupyter) is corresponding image on docker hub).

https://gist.github.com/andrewm4894/ff38b48382d4f4a70734ef47ad974015

Once you have such a custom image building fine it's pretty easy to just point KubeFlow at it when creating a Jupyter notebook server.

<figure>

![](/assets/images/2019-10-20-kubeflow-custom-jupyter-image-github-for-notebook-source-control/Capture.png)

<figcaption>

Just specify your custom image

</figcaption>

</figure>

Now when you create a new workbook on that jupyter server you have all your custom goodness ready to go.

## Github for notebooks

As i was looking around it seems like there is currently plans to implement some git functionality into the notebooks on KubeFlow in a bit more of a native way (see [this issue](https://github.com/kubeflow/kubeflow/issues/2889)).

For now i decided to just create a ssh key ([help docs](https://help.github.com/en/articles/connecting-to-github-with-ssh)) for the persistent workspace volume connected to the notebook server (see step 10 [here](https://www.kubeflow.org/docs/notebooks/setup/)).

Then once you want to `git push` from your notebook server you can just hack together a little notebook [like this](https://github.com/andrewm4894/my-kf-notebooks/blob/master/git.ipynb) that you can use as a poor man's git ui :)
