---
title: "Papers i'm reading #1"
date: 2019-12-30
categories: 
  - "anomaly-detection"
  - "machine-learning"
tags: 
  - "anomaly-detection"
  - "machine-learning"
---

I've recently set myself the goal of reading one academic paper a week relating to the ML/AI things i'm working on i'm my current role.

![](images/papers.jpg)

To try help keep me honest and diligent in this regard, I've decided to get into the habit of jotting down some quick notes on each paper and every now and then as i get through a batch of them, stick them into blog post (because i like to try squeeze everything and anything into a blog post if i can get away with it, even better if is minimal extra effort on my part :) ).

* * *

## Anomaly Detection in Streaming Non-stationary Temporal Data

[Link](https://robjhyndman.com/papers/oddstream.pdf)

My Summary: Really interesting paper and application, considers a lot of different design aspects in it. Nice example of a different approach leveraging feature extraction and statistical techniques to get the job done.

Notes:

- Leverages EVT approaches, forecasts boundary for typical behavior in relation to the extremes.
- Leverages a feature vector and dimensional reduction approach too which is interesting and somewhat independent of the AD algo. 
- It is multivariate but the data they use are all sensor data so measuring the same thing, so not quite the same as multivariate measures measuring different things - so still questions on how one would normalize accordingly for this approach.
- Some lovely pictures. 
- It is online but does have a sort of offline or training phase where it fits to the ‘representative example’ of the data - and this may need to change/evolve over time. 
- So it is streaming and unsupervised but with some small caveats. 
- Interesting discussion on differences between density based and distance based approaches to anomaly detection.
    - “In contrast, defining an anomaly in terms of the density of the observations means that an anomaly is an observation (or cluster of observations) that has a very low chance of occurrence”.
- Offline phase - estimate the properties of the typical dataset which will be used in the online phase of anomaly detection.
- HDOutliers is another approach worth looking into.  
- Interesting choice of 14 features which they then do pca on. Worth looking into these specific features.
- Offline phase is implemented as just a burn in window on the streaming data so this is not too bad.  
- Feature extraction and dimension reduction a big part of the preprocessing, interesting approach that could be applied to other algos.
- Just using first 2 components of the PCA - found that interesting.
- There is quite a few steps in the algos - quite involved. 
- Sliding window with concept drift detection used to determine when need to refit the data - interesting approach as opposed to just refitting at regular intervals. Pros and cons to each potentially. 
- The output at each timestep is a list of time series flagged as anomalous within that sliding window. So there is not really an anomaly score as such. 
- They suggest that having the ‘informed’ concept drift based approach is more efficient overall as avoids wasteful refits.
- Unclear to me how this would apply to multivariate ts data with many different types of measurements. Does not really discuss this in the paper - maybe worth a question on the repo if playing around with it. 
- There still are some probably important params like window size and things like that.

* * *

## A comparative evaluation of unsupervised anomaly detection algorithms for multivariate data

[Link](https://com-mendeley-prod-publicsharing-pdfstore.s3.eu-west-1.amazonaws.com/7ffd-PUBMED/10.1371/journal.pone.0152173/pone_0152173_pdf.pdf?X-Amz-Security-Token=FwoGZXIvYXdzENL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDHT3HOe1yi2ZAERVnSLqAoBm9b5SiEgs9eXbgFxQmoLc%2FigzOomg%2BeVjVx5eAblU%2F4zse4R3%2BrORVASAOsyCYWmmPZiXlsFeWWs8kKin4lmQ93tZ%2Fm6RTJmqVbd1Q75i0cSuQRjPaYup%2FTIpqhCy%2FP8%2FpQgOQlO%2FJlw6cyoi%2BtuEDKMDV4PKiOJGqxwiLQrFiiIe3eCVU3dgH%2B7LW4u%2BM5LyVMQW0Q97JEJDGfBgVCQIe9oeAwAW2IUpHijgN2KnOI6dobZlynQyIHZrRSZxx85DDNhOKLuDryMJVwo1Kv%2FTJHERr2%2BvwbrnWg9eXoOptc71qtVA2fPJWCCIlBHUlppYUGlKSep7B68V%2BeSy09qihdRoKO48B2Ie30OnV0RI%2FQiucaANoR5X897b20kVU92qLXMEXNhbc0kKHccq1vgz0JSm4t82RKqIAF8NNQXj7fJBhj0qBYq2pdANuBpxSGJcaSwIefFbg9mDhyxIsh9HT2HFdKs1214fKKfTye8FMqEBwbE1jW0mFmcyGUPEQrSfULYQdkqdR6zK7jZl9rHsaxvc9CaQhrLZJwRR%2B2tjkfB%2B3jPavgBMcccM6lGBqLwvfhpxo8RvlXI1R7nZM9eyWdgebEvxUKQ53QDcNGv%2F8%2B3cEGdqE3GctqJD2TNo8shjmaRA4HHW8Q2FFDz3LQ8mxvaPjWA88%2B3AVuvldrW9vXQKzbyfNRpPfmSyPec7BP5VvqQ%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20191212T170838Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIARSLZVEVE3YHMPX5D%2F20191212%2Feu-west-1%2Fs3%2Faws4_request&X-Amz-Signature=7339d6f6e3802665c4f4037ecc3c5197dce611b9ec2611efd3ae290759ca905b)

My Summary: Very good reference paper for more traditional methods as opposed to deep learning based approaches. Good discussion on complexity and online setting too. Primarily concerned with traditional tabular data as opposed to time series but still some good ideas to pursue.

Notes:

- 2016 paper so maybe pre-deep learning hype which is nice. 
- Time series data and setting not really any part of this paper so bear that in mind. 
- Authors use similar taxonomy in terms of types of AD setting as I have seen in other papers. 
- Mainly if we ‘flatten’ our time series data into feature vectors (tabular data) then we would be in a similar setting as this paper. 
- Scores are much more useful then binary labels as outputs. 
- AD Settings (similar to elsewhere):
    - Point AD.
    - Collective AD.
    - Contextual AD.
- Normalization suggested as important but no mention of difficulty in normalizing streaming data. 
- Another reference to the NASA shuttle data - must look into this. 
- 4 Groups of unsupervised AD algos:
    - Nearest neighbor.
    - Clustering based.
    - Statistical.
    - Subspace techniques.
- KNN based approaches, 10 < k <50 as rule of thumb.
- KNN can miss local outliers as relies on neighbours.
- LOF nice in that can give a score between 0 and 1 ← this is a nice property to have.
- They go through various extensions of LOF.
- LoOP - Local Outlier Probability - makes some small changes such that you get back a probability. But still that probability can be very specific to the particular model. Its not like its really a probability you can compare to other models. More useful for within model observation comparisons.
- Some extensions of LOF that first use clustering to reduce complexity. 
- Clustering based approaches can be very sensitive to the choice of K. 
- HBOS - histogram statistical based approach. Simple and fast, surprisingly performant.
- One class SVM - a range of ways to implement, not really lends itself well to online setting. 
- PCA - get components and then use them in some way to get AS. PCA can reduce to clustering equivalence under certain conditions. 
- PCA can be fast if D not too large.
- Metrics@TopN is a good way to evaluate AD systems. E.g so long as some anomalies appear in the top of the pile that can be progress (similar evaluation methods to information retrieval). 
- Rank comparison approaches can be useful too (we should make sure any data we capture lends itself to this approach also).
- Local vs Global anomalies are a big consideration in this paper. Is not quite clear what this would mean in our setting. It’s probably true that we are more interested in global anomalies than local ones. But also hard to know which setting you are in, especially in higher dimensions. 
- #k has a big impact on computation time for clustering algos, as does the size of dataset.
- HBOS is fast!
- All algos in this paper are available via a rapidminer extension if we wanted to play with them.
- Recommendation to start with global based algos as they can also work somewhat on local anomalies. 
- Clustering approaches also sensitive to random start so good to restart a few times. 
- Nearest neighbour approaches can be more robust to choice of parameters.
- But clustering approaches can be faster then knn approaches.

* * *

## Deep Learning for Anomaly Detection: A Survey

[Link](https://arxiv.org/abs/1901.03407)

My Summary: A looot of references and got some good ideas out of it. Not much else to it. 

Notes:

- I like the general taxonomy they use for types of AD problems/framings.
    - Point, contextual, vs collective.
- Good point about maybe an over focus on autoencoders, not clear what is driving that.
- Interesting discussion around one class neural networks. 
- Labels in practice not as big of an area for practical reasons (hard to collect) and in cases where anomalous patterns may change. 
- Hybrid approaches could be interesting if provide efficiency at runtime. Use DL model for feature representation and then some other model for the scoring.
    - One problem is this is not end to end but could still be something to keep in mind.
    - One class NN as better option here.
- Little discussion in the paper around considerations in productionising any of it or dealing with specific considerations involving streaming data.  
- Could convert time series problem into a sequence problem and use things like language models or event based approaches.
- Adaptivity of your model as a design param you need to think about and decide on.
- The part about interconnectedness of IoT nodes resonates with some use cases for us.
- Deep attention based models as useful in helping to explain and locate the anomaly in addition to just detecting it. 
- GAN’s as an approach worth looking into. 
- No clear theory or guidance on what choices to make in network architecture and hyper params.
- Transfer learning based approaches as an open and active area of research. 
- Hilbert transform and other DSP based approaches mentioned.

* * *

## Time2Vec: Learning a Vector Representation of Time

[Link](https://arxiv.org/abs/1907.05321)

My Summary: Nice little paper and idea of learning the frequency functions and representations seems really interesting. 

Notes:

- Key idea is that time2vec gives you a “general purpose model agnostic representation of time that can be potentially used in any architecture”.
- Basically it’s trying to extend the notion of feature embeddings to the time series domain.
- Time2vec as a featurizer essentially.
- Talk of asynchronous time/sequence based models is interesting. Perhaps could be a class of models we could explore that could run on irregularly sampled data.
- A large focus here on capturing various periodicity and time varying effects. It could be that 1 second monitoring data is not a great candidate for this by its nature.
- Could use time2vec type approach to get a more universal feature representation?
- Unclear if this is all univariate or multivariate.
- Worth looking around to see if any time2vec implementations to play with.

* * *

## catch22: CAnonical Time-series CHaracteristics

[Link](https://link.springer.com/content/pdf/10.1007/s10618-019-00647-x.pdf)

My Rating: 8/10

My Summary: Well done paper, limited application potentially to an online setting but great food for thought on the range of ts feature transformations literature already out there.

Notes:

- Idea to compress time series into useful ‘feature vectors’ that can be used for downstream ML tasks, mainly classification and clustering in this paper.
- Starting point is [hctsa](https://github.com/benfulcher/hctsa) matlab package feature space of ~5k features. Catch22 is a project to empirically discover the most useful (and computationally reasonable) of these.
- Builds on a lot of literature and hand crafted feature engineering in the time series space. 
- Catch22 is implemented in C with python, R, mathlab wrappers. This could be useful for netdata core C based stuff. 
- Many features here may require the full ts to be available prior to calculation so not suitable for online streaming setting. Although could implement windowed versions potentially. 
- E.g. how do you z-score normalise a stream of data?
- They just used a decision tree as the classification model they used. I wonder how sensitive results are to this. I guess makes sense as they wanted to try test the usefulness of the features themselves. Curious why no linear models. 
- Clustered the ‘performance vectors’ to try to reduce redundancy and overlap of features. That was nice. 
- Check out the [tsfeatures](https://cran.r-project.org/web/packages/tsfeatures/vignettes/tsfeatures.html) package from Hyndman mentioned in this paper. 
- It is interesting to look at some of the ts features themselves - don’t reinvent the wheel when all this already exists!
- Look into [compengine](https://www.comp-engine.org/).

* * *

## Time Series Anomaly Detection; Detection of anomalous drops with limited features and sparse examples in noisy highly periodic data

[Link](https://arxiv.org/abs/1708.03665), 

My rating: 6/10

My summary: Good example of simple regression based approach, not very generalisable, data and results not really powerful. 

Notes:

- Typical ‘Expected Value’ regression based approach. 
- Focus on sustained anomalies as opposed to single timesteps.  
- No semantic or domain based understanding -just independent time series all treated separately. 
- Data in this paper is “periodic but noisey” 5 min level byte counts.
- Shout out to Numenta approach to anomaly likelihood, must revisit this.
- Use of simulated data. 
- Data Normalization to 0-1 scale. Unclear how this is implemented without data leakage or in an online manner.
- Simple threshold based approach to detection given, Yhat - Y = AS.  
- Use of dummy data for model/approach comparison.
- Pretty small dataset for DL approaches.
- In the absence of labeled data, leveraging multiple approaches and comparing anomalies raised by each approach and their profiles could be a useful way to iterate towards golden datasets.
- DL models they used looked quite big and deep for nature and size of the data - not really motivated why chose more complex architecture.
- LSTM or RNN did not do better than vanilla DNN.
- Not the most convincing set up and approach. Very limited in terms of data and depth of the research.

* * *

## Time-series anomaly detection service at Microsoft

[Link](https://www.mendeley.com/catalogue/timeseries-anomaly-detection-service-microsoft/)

My rating: 8/10

My summary: Good walkthrough of end to end service, interesting computer vision application, some good leads to follow up. 

Notes:

- Interesting to see they use influxdb (and Kafka, and some flink).
- Deployed as service on kubernetes.
- Stuck with needing to treat each individual time series separately in the model.
- They build model to label each point in window as anomalous or not - seems potentially limiting if just interested in if each window of data is anomalous or not. 
- SR sounds interesting, have not seen that before, worth looking into, although their SR example looks very similar to what you’d get by looking at pct change or something so feels maybe over-engineered. 
- Converting the problem into a computer vision friendly setting is interesting and not uncommon. In the multivariate setting we could encode the data visually, e.g. fft and wavelet frequency distributions etc. Heatmaps or even some custom encoding into a visual space based on specific characteristics of the data.  
- Some of the windowed feature engineering stuff seemed interesting, as well as then layering ratios of those windowed features on top of each other. 
- Is a way for users to label data which seems to help build golden datasets used for later validation and experimentation.
- Need to look into SPOT and DSPOT as EVT based approaches i’ve only previously superficially looked at.
- Need to look into DONUT.
- Some other good references to follow up on.
- Seems like this is indeed a technical paper relating to [this Azure api](https://azure.microsoft.com/en-us/services/cognitive-services/anomaly-detector/).
