---
title: "Ireland Covid19 Data"
date: 2020-03-23
tags: 
  - "coronavirus"
  - "data"
  - "python"
layout: post
---

![](/assets/images/2020-03-23-ireland-covid19-data/200130165125-corona-virus-cdc-image-super-tease.jpg)

I was looking around a bit and could not really find any datasets behind the daily updates from the Irish government that get posted [here](https://www.gov.ie/en/news/7e0924-latest-updates-on-covid-19-coronavirus/). In particular i was thinking the break out tables of numbers by different dimensions might be of use for anyone looking to analyse the data.

So [here](https://github.com/andrewm4894/ireland_covid19_data) is a python script to grab all press release links from the updates page, pull the html tables in pandas dataframes, do some ugly/gnarly data wrangling and save results into csv files [here](https://github.com/andrewm4894/ireland_covid19_data/tree/master/data).

As an example i've stuck some of the headline figures and stats in a Tableau dashboard [here](https://public.tableau.com/profile/andrew.maguire#!/vizhome/IrealndCovid19Data/Daily).

**Update1**: [This](https://datastudio.google.com/u/0/reporting/8bc04c57-017b-4f4d-975b-d004bcc7728d/page/9cEJB?s=rlQVDcBF3sY) looks like a nice dashboard using similar data for Ireland.

**Update2**: [IrishDataViz](https://twitter.com/IrishDataViz) is a great twitter account with some analysis of the irish numbers.
