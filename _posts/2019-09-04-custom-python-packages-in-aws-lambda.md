---
title: "Custom Python Packages in AWS Lambda"
date: 2019-09-04
categories: 
  - "aws"
tags: 
  - "aws-lambda"
  - "python"
  - "serverless"
layout: post
---

<figure>

![](/assets/images/2019-09-04-custom-python-packages-in-aws-lambda/so-hot-right-now.png)

<figcaption>

It's True.

</figcaption>

</figure>

I'm pretty sure i'll be looking this up again at some stage so that passed one of my main thresholds for a blog post.

I've recently been porting some data and model development pipelines over to [AWS Lambda](https://aws.amazon.com/lambda/) and was mildly horrified to see how clunky the whole process for adding custom python packages to your Lambda was (see docs [here](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html)).

[This](https://serverless.com/blog/serverless-python-packaging/) was probably the best post i found but it still did not quite cover custom python packages you might need to include beyond just the more typical pypi ones like numpy, pandas, etc. (p.s. [this video](https://www.youtube.com/watch?v=S6dmyzQb6S8) was really useful if you are working in [Cloud9](https://aws.amazon.com/cloud9/)).

So i set out to hack together a process that would automate 90% of the work in packaging up any python packages you might want to make available to your AWS Lambda including local custom python packages you might have built yourself.

The result involves a Docker container to build your packages in (i have to use this as using windows based python package local install does not work in Lambda as the install contains some windows stuff Lambda won't like), and a jupyter notebook (of course there is some jupyter :) ) to take some inputs (what packages you want, what to call the AWS Layer, etc), build local installs of the packages, add them to a zip file, load zip file to S3 and then finally use awscli to make a new layer from said S3 zip file.

## Dockerfile

The first place to start is with the below [Dockerfile](https://github.com/andrewm4894/my-aws-python-packages/blob/master/Dockerfile) that creates a basic conda ready docker container with jupyter installed. Note it also includes [conda-build](https://github.com/conda/conda-build) and copies over the **packages/** folder into the container (required as i wanted to install my "my\_utils" package and have it available to the jupyter notebook).

https://gist.github.com/andrewm4894/7ee15f75af7eab92e61b7ad932b259e5

Build this with:

```
$ docker build -t my-aws-python-packages -f ./Dockerfile ./
```

And then run it with:

```
$ docker run -it --name my-aws-python-packages 
    -p 8888:8888
    --mount type=bind,source="$(pwd)/work",target=/home/jovyan/work
    --mount type=bind,source="$(pwd)/packages",target=/home/jovyan/packages 
    -e AWS_ACCESS_KEY_ID=$(aws --profile default configure get aws_access_key_id)
    -e AWS_SECRET_ACCESS_KEY=$(aws --profile default configure get aws_secret_access_key)
    my-aws-python-packages
```

The above runs the container, port forwards 8888 (for jupyter), mounts both the **/packages** and **/work** folders (as for these files we want changes from outside docker or inside to be reflected and vice versa), and passes in my AWS credentials as environment variables to the container (needed for the asw cli commands we will run inside the container). Its last step is to then launch jupyter lab which you then should be able to get to at http://localhost:8888/lab using the token provided by jupyter.

## Notebook time - make\_layer.ipynb

Once the docker container is running and you are in jupyter the [make\_layer](https://github.com/andrewm4894/my-aws-python-packages/blob/master/work/make_layer.ipynb) notebook automates the local installation of a list of python packages, zipping them to /work/python.zip folder as expected by [AWS Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html) (when unzipped your root folder needs to be /python/...), loading it to an S3 location, and then using awscli to add a new layer or version (if the layer already exists).

The notebook itself is not that big so i've included it below.

\[iframe src="https://nbviewer.jupyter.org/github/andrewm4894/my-aws-python-packages/blob/master/work/make\_layer.ipynb?flush\_cache=true" width="100%" height="1800" scrolling="yes" class="iframe-class" frameborder="0"\]

For this example i've included two custom packages along with [pandas](https://pandas.pydata.org/) into my AWS Layer. The custom packages are just two little basic [hello\_world()](https://github.com/andrewm4894/my-aws-python-packages/blob/master/packages/my_dev/my_dev/dev.py#L3) type packages (one actually creates the [subprocess\_execute()](https://github.com/andrewm4894/my-aws-python-packages/blob/master/packages/my_utils/my_utils/os_utils.py#L6) function used in the make\_layer notebook). I've included pandas then as well to illustrate how to include a pypi package.

## Serverless Deploy!

To round off the example we then also need to create a little AWS Lambda function to validate that the packages installed in our layer can actually be used by Lambda.

To that end, i've adapted the [serverless](https://serverless.com/) example cron lamdba from [here](https://github.com/serverless/examples/tree/master/aws-python-scheduled-cron) into [my own little lambda](https://github.com/andrewm4894/serverless-learn/tree/master/serverless-learn-lambda) using both my custom packages and pandas.

Here is the [handler.py](https://github.com/andrewm4894/serverless-learn/blob/master/serverless-learn-lambda/handler.py) that uses my packages:

https://gist.github.com/andrewm4894/7403c9fb50b489b6f6d58f7640421ce4

And the [serverless.yml](https://github.com/andrewm4894/serverless-learn/blob/master/serverless-learn-lambda/serverless.yml) used to configure and deploy the lambda:

https://gist.github.com/andrewm4894/aa98b3fad0b4b001ab85719b88b7878b

We then deploy this function (from [here](https://github.com/andrewm4894/serverless-learn/tree/master/serverless-learn-lambda)) with:

```
$ serverless deploy
```

And we can then go into the AWS console to the Lamdba function we just created. We can test it in the UI and see the expected output whereby our custom functions work as expected as does Pandas:

<figure>

![](/assets/images/2019-09-04-custom-python-packages-in-aws-lambda/Capture.jpg)

<figcaption>

Success!

</figcaption>

</figure>

That's it for this one, i'm hoping someone might find this useful as i was really surprised by how painful it was to get a simple custom package or even pypi packages for that matter available to your AWS Lambda functions.

If you wanted you could convert the ipynb notebook into a python script and automate the whole thing. Although i'm pretty sure Amazon will continue to make the whole experience a bit more seamless and easier over time.
