---
title: "Weights &amp; Biases - log Keras model summary &amp; architecture"
date: 2024-03-04
categories: 
  - "machine-learning"
  - "observability"
tags: 
  - "machine-learning"
  - "observability"
  - "python"
  - "wandb"
coverImage: "Screenshot-2024-03-04-at-4.10.47 PM.png"
---

Maybe i missed something but i could not find any easy and simple out of the box ways to just save Keras `[model.summary()](https://github.com/keras-team/keras/blob/v3.0.5/keras/models/model.py#L217)` and `[plot_model()](https://keras.io/api/utils/model_plotting_utils/#plotmodel-function)` outputs to [wandb](https://wandb.ai/site).

So below is one little recipie to do this, feel free to use and adapt however suits your needs.

https://gist.github.com/andrewm4894/7c22a7944b791959bbf662b87cb0139d
