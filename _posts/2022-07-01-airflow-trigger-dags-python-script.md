---
title: "Airflow \"Trigger Dags\" Python Script"
date: 2022-07-01
categories: 
  - "airflow"
tags: 
  - "airflow"
  - "python"
layout: post
---

You have some dag that runs multiple times a day but you need to do a manual backfill of last 30 days.

It's 2022 and this is still surprisingly painful with Airflow. The "new" [REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) helps and mean's all the building blocks are there but, as I found out today, there can often still be some faffing about left for you to do.

So here is a little Python script to just loop over a range of days and kick of a dag run for each day.

You would run it like this:

```bash
python airflow_trigger_dags.py --dag 'my_beautiful_dag' --start '2022-06-01 00:00:01' --end '2022-07-31 00:00:01'
```

For the `dag` you pass, it will loop over each day and kick off a dag run for the same timestamp you define. So you can just increment the `00:00:01` part to `00:00:02` if you need to rerun the same backfill again for some reason (like you messed up your "fix" the first time around :) ). This assumes your dags are just using typical params like "`ds`" etc and so only need the `execution_date` to run properly. If your dag is more complex and depends of specific start and end times then this approach might not work or may need to be extended a little.

https://gist.github.com/andrewm4894/d83fe3a9aa194ae40a7c4acb6ee5eb02
