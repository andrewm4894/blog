---
title: "Terraform is Magic + r/MachineLearning Links"
date: 2020-04-29
categories: 
  - "machine-learning"
tags: 
  - "machine-learning"
  - "python"
  - "r-machinelearning"
  - "terraform"
  - "youtube"
---

![](/assets/images/2020-04-29-terraform-is-magic-r-machinelearning-links/tfismagic.jpg)

[Terraform](https://www.terraform.io/) is magic, i may be a little late to the game on this one and i'm sure it has it's fair share of haters (i've seen [some have a love hate relationship with it](https://medium.com/@hbarcelos/how-i-learnt-to-love-and-hate-terraform-in-the-past-few-weeks-db085d012882), maybe i'm still in my honeymoon period).

But from my point of view as a Data Scientist/ML Engineer playing around with various services in a multi-cloud environment (mainly GCP and AWS) its one of the things that keeps me sane in a sea of changing features and web ui's that the cloud providers love to throw at us.

When it comes to cloud projects i'm working with, if its not under source control and managed by terraform then i don't want to know about it.

So as I've been on my voyage of discovery with terraform i decided to put it to use in a little side project I've been wanting to do for a while.

(**Note**: All code is available in my [reddit-links Github repo](https://github.com/andrewm4894/reddit-links).)

## The Set Up

The idea is to have a cloud function that runs each day, looks at top posts on [r/MachineLearning](https://www.reddit.com/r/machinelearning), pulls out all links, and some metadata, and then saves those links somewhere useful.

My original goal (and something i might get to at some stage) was to pull all YouTube links shared on r/MachineLearning that have a decent score into an automatic playlist on YouTube or maybe automatically add them to my own watch later playlist. I have the data now so this might be an easy enough next project.

So given the goal above here are the various moving parts I've picked to use:

- **Terraform**: To manage all the GCP stuff used.
- **GCP Cloud Function**: This will be the code that pulls from r/MachineLearning, wrangles the text and html data from reddit, pulls out the links and then either inserts or updates Airtable accordingly.
- **GCP PubSub Topic**: This will be the trigger for the cloud function.
- **GCP Cloud Scheduler**: This will run a sort of cron job in GCP each day to push a message to the pubsub topic which will in turn trigger the cloud function.
- **Airtable**: This is where the data will be stored and published from. I had considered a GCP bucket but Airtable is much easier to share and a bit more user friendly for anyone who might want to use the links pulled from reddit.

## Terraform

Once you work with and set up a Terraform project once then its pretty straight forward. I have used [Serverless](https://www.serverless.com/) for some cloud functions before but i like the way terraform gives you everything GCP or AWS or Azure etc have to offer at your fingertips once you invest that little bit of learning up front.

Here is a list of the .tf files i'm using and what they all do. There are of course many ways to set things up in Terraform but this seemed like a straightforward enough way and works for me for smaller projects like this.

- [**backend.tf**](https://github.com/andrewm4894/reddit-links/blob/master/terraform/backend.tf) - this is optional and used to have a remote [backend](https://www.terraform.io/docs/backends/types/gcs.html) for the state of your project as opposed to somewhere on your laptop.
- **[conf.tf](https://github.com/andrewm4894/reddit-links/blob/master/terraform/conf_example.tf)** - this is a file i'm using to define any sensitive variables in terraform that i don't want to go into source control (make sure you add to .gitignore) but need to make available to terraform to do it's stuff. I have included an [conf\_example.tf](https://github.com/andrewm4894/reddit-links/blob/master/terraform/conf_example.tf) file in the repo to show how this looks.
- **[variables.tf](https://github.com/andrewm4894/reddit-links/blob/master/terraform/variables.tf)** - used to define other variables used by terraform.
- **[provider.tf](https://github.com/andrewm4894/reddit-links/blob/master/terraform/provider.tf)** - conventional file to define the cloud [providers](https://www.terraform.io/docs/providers/index.html) you want to be able to use.
- **[gcp-cloud-functions.tf](https://github.com/andrewm4894/reddit-links/blob/master/terraform/gcp-cloud-functions.tf)** - this is where we will define all the things we need related to our [Cloud Functions](https://cloud.google.com/functions).
- **[gcp-cloud-scheduler.tf](https://github.com/andrewm4894/reddit-links/blob/master/terraform/gcp-cloud-scheduler.tf)** - used to define the [Cloud Scheduler](https://cloud.google.com/scheduler) cron jobs we need.
- [**gcp-pubsub-topics.tf**](https://github.com/andrewm4894/reddit-links/blob/master/terraform/gcp-pubsub-topics.tf) - used to define the [PubSub](https://cloud.google.com/pubsub) topics that will trigger the cloud function.

## GCP Function - redditlinks

The function used to pull from reddit is below. It might be a little verbose and could probably be refactored a little but hey - it works. Mainly using the [PRAW](https://praw.readthedocs.io/en/latest/) library to pull from reddit, some usual data wrangling libraries, and then the [airtable-python-wrapper](https://github.com/gtalarico/airtable-python-wrapper) library to insert/update records in Airtable.

https://gist.github.com/andrewm4894/dbea54c122d8f3dd4e2695887e337567

## End Results - Airtable

The end results of all this being a cloud function that runs once a day to update or insert records into [this Airtable](https://airtable.com/shrCe8ZWuLJpHNiG8). Then from that i have made some views for links from specific domains.

(**Note**: If you wanted to do this but for a different subreddit then you should need to make minimal changes once you have your terraform variables all set up - primarily changing or adding another cloud scheduler job to [here](https://github.com/andrewm4894/reddit-links/blob/master/terraform/gcp-cloud-scheduler.tf) with the relevant params, as well as making sure all keys etc you need are available in the right places).

## r/MachineLearning - YouTube Links

<iframe class="airtable-embed" src="https://airtable.com/embed/shrfM8xpQlzEchVWB?backgroundColor=orange&amp;viewControls=on" frameborder="0" onmousewheel="" width="800" height="500" style="background: transparent; border: 1px solid #ccc;"></iframe>

## r/MachineLearning - Arxiv Links

<iframe class="airtable-embed" src="https://airtable.com/embed/shrNMyw1d6BKS3R89?backgroundColor=orange&amp;viewControls=on" frameborder="0" onmousewheel="" width="100%" height="533" style="background: transparent; border: 1px solid #ccc;"></iframe>
