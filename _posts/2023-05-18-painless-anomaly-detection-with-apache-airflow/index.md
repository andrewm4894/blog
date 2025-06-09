---
title: "Painless Anomaly Detection with Apache Airflow"
date: 2023-05-18
categories: 
  - "airflow"
  - "anomaly-detection"
  - "machine-learning"
tags: 
  - "airflow"
  - "anomaly-detection"
  - "machine-learning"
  - "python"
coverImage: "data-obs-so-hot.jpg"
---

Data observability _is_ so hot right now...but do you know what's also hot? Using some tried and tested ingredients like [Apache Airflow](https://airflow.apache.org/) and [PyOD](https://pyod.readthedocs.io/en/latest/) to perform painless anomaly detection on your key business metrics.

You don't need to run off and buy an (expensive!) subscription for the latest hot data observability Sass offering (there is lots and some of them are great in my experience, [Metaplane](https://www.metaplane.dev/) does a lot really well here in my opinion but i am of course not familiar with all of tools - [obligatory crazy landscape picture](https://mattturck.com/mad2023/)).

If instead, you want to keep things simple to begin with, you probably already have most of the main ingredients you need for a pretty decent anomaly detection stack on whatever metrics you want - using our old friend Airflow and [this](https://pypi.org/project/airflow-provider-anomaly-detection/) new anomaly detection provider package I built because I just love anomaly detection that much.

(I really do - metrics are everywhere so we need decent anomaly detection to avoid overload, anomaly detection is a great mix of art and science as can be quite subjective, and decent anomaly detection should some-day kill all dashboards!!!)

## Anomaly detection Airflow provider

So here is the **TL;DR;** (if curious for more detail check out the project [README](https://github.com/andrewm4894/airflow-provider-anomaly-detection) on GitHub).

An Airflow Provider for Anomaly Detection:

1. You define "metrics batches" in some sql (for example, [here](https://github.com/andrewm4894/airflow-provider-anomaly-detection/blob/main/airflow_anomaly_detection/example_dags/anomaly-detection-dag/sql/metrics/metrics_hourly.sql) is the "metrics\_hourly" batch in the example dag).

3. Some yaml configuration fun (you can just use the defaults) for params of config you might want to change (for example, [here](https://github.com/andrewm4894/airflow-provider-anomaly-detection/blob/main/airflow_anomaly_detection/example_dags/anomaly-detection-dag/config/metrics_hourly.yaml) is the config for the "metrics\_hourly" batch).

5. You get some alerts via email (which you can just use for Slack etc too) when metrics look anomalous.

## How it works

Really all this provider and example dag are doing is creating a set of 4 dags within airflow, one set for each "metric batch" you define (different "metric batches" can be for different frequency or subject areas - you can use them however you want as each metric batch is basically just templated jinja sql files and a corresponding yaml config file):

1. **Ingestion**: Ingest each metric batch by running the sql and just appending the results (the metrics) to some table you can pointed it at.

3. **Training**: Train an anomaly detection model, one per metric within each metric batch, and save the trained model to a Google Cloud Storage (GCS) bucket.

5. **Scoring**: Use the model trained in step 2 to score recent data and save scored metrics to another table you have pointed it at.

7. **Alerting**: A dag that looks over recent scored metrics and just alerts based on traditional enough rolling thresholds on those scored metrics.

## Pros vs. Cons

Here are some pro's and con's to help you decide if using and getting involved in this project makes sense to you.

**Pros**:

- You bring your SQL to define your metrics and let this provider do the rest.

- Nice and simple alerts.

- A lot of us are already using Airflow for ETL type stuff so we are quite comfortable with it.

- This just packages up the problem into a few Airflow dags and so makes it all a bit easier to reason about and understand (as well as customize if you like).

- A lot of us also have business metrics in cloud data stores like Google BigQuery, AWS Redshift, and Snowflake etc so we don't actually need to involve a new database layer in any of this - just let Airflow do the orchestration and work for ingestion, training and scoring.

**Cons**:

- Better suited for metric batches of stuff that does not need to be near real time - eg. hourly or daily business metrics are very well suited (it's what I built this for).

- Still a fairly immature project so more a case of try it yourself and see how it goes (I'd love some help :) ).

- Some limits to the size and complexity of models that make sense - from my experience decent enough anomaly detection is totally possible with reasonable traditional ML models and sensible feature engineering.

- Don't really have the ability to build a workflow into the anomaly alerts just yet - you get an email when something looks strange and that's that - we don't have any incident management type workflows as part of this since that would be another fairly complex moving part we are avoiding for now.

## Get involved!

This project is very very easy to get involved in and I hope could end up being quite useful for the wider Airflow community - it's crazy that we don't really have easy ways to just get some decent anomaly detection on all our business metrics within the same context of the ETL's and dags we create all the time in Airflow.

The basic core idea is, le'ts just use Airflow for a bit more than ETL's - one way to frame the anomaly detection use case is just some ETL's and a few small python tasks so Airflow is a perfect tool for this.

Feel free to make issues and PR's in the Github repo: [https://github.com/andrewm4894/airflow-provider-anomaly-detection](https://github.com/andrewm4894/airflow-provider-anomaly-detection)

## Useful links

- Project [README](https://github.com/andrewm4894/airflow-provider-anomaly-detection/tree/main#readme)

- [Example alert](https://github.com/andrewm4894/airflow-provider-anomaly-detection#example-alert) - An example of what an alert looks like.

- [Anomaly gallery](https://github.com/andrewm4894/airflow-provider-anomaly-detection/tree/main/anomaly-gallery) - Some real world example i have been adding while dogfooding.

- [Example dag](https://github.com/andrewm4894/airflow-provider-anomaly-detection/tree/main/airflow_anomaly_detection/example_dags/anomaly-detection-dag) - The example dag that ships with the provider. Best place to start and look around if just want to see what's going on and already familiar with Airflow etc.

- [Getting started](https://github.com/andrewm4894/airflow-provider-anomaly-detection#getting-started) - How to play around and try it out yourself.
