---
title: "Papers i'm reading #2"
date: 2020-02-20
tags: 
  - "academic-papers"
  - "anomaly-detection"
  - "machine-learning"
  - "research"
layout: post
---

Continuation from [this post](https://andrewm4894.com/2019/12/30/papers-im-reading-1/).

## An unsupervised spatiotemporal graphical modeling approach to anomaly detection in distributed CPS (Cyber Physical Systems).

[Link](http://web.me.iastate.edu/soumiks/pdf/Conference/LGJS16_conf.pdf)

My Summary: Really interesting paper - PGM’s, HMM’s and all that good stuff. Quite complicated though and no clear route to implementation. Also I would wonder how well it scales beyond 10’s of time series. More good for learning about some different approaches as opposed to anything that could be implemented easily. 

Notes:

- “Spatiotemporal” feature extraction, “Symbolic dynamics”, “Causal interactions”... some fancy sounding stuff, seems to try get at causal relationships which might be a bit too strong a claim be defo interesting stuff that i had not come across before.
- CPS = power plants, power grids, transport systems etc. 
- Symbolic dynamic filtering - look this up.
- General setting in this paper is a probabilistic graphical model type set up.
- State, Alphabet, Symbol generation matrix, Importance Score - similar sort of set up to HMM type models.
- Partitioning → States → Spatiotemporal Pattern Network (STPN).
- Energy based models another way to frame and think about these models.
- I wonder how well this model scales to many time series? My gut says probably ok for a handful of time series as opposed to 100’s.
- Some nice pictures of how it all hangs together. 
- All focused on short subsequences as the core inputs it learns on. Can be overlapping windows. 
- Lots of maths and symbols in this paper! Very complicated and hard to follow - would need to read 10 times.
- Does not look like any code or implementations out there so not sure if easily implementable. 
- Nice results on synthetic data with multiple modalities. 
- Interesting results on real world smart home (HVAC and underfloor heating) data too. Just a handful of time series and nice an clear case study with obvious causal chains. 
- Interesting to see global and local anomalies picked up.
- Still seems like some parameters to tune/pick - also need to threshold the importance score.   

* * *

## Recent Advances in Anomaly Detection Methods applied to Aviation.

[Link](https://www.preprints.org/manuscript/201909.0326/v1)

My Summary: Interesting paper focusing specifically on aviation but in a broad sense and in an up to date manner covering many newer techniques too. Still seems in reality a lot of domain specific and traditional methods is what is actually used in reality as opposed to in the research.

Notes:

- Good food for thought on differences and similarities between novelty detection and anomaly detection. 
- They use the usual typical taxonomy of point, contextual, and collective.
- Lots of references to explainability as well, which makes sense in an aviation setting.  
- “Temporal Logic Based Models” - sounds interesting need to look into  this more.
- “Model Driven” (rules from experts) vs “Data Driven” (Machine learned).
- Really nice taxonomy below.
- 3 types of clustering based assumptions:
    - Anomaly as outside any cluster.
    - Anomaly as far away from centroids.
    - Density based whereby cluster can be a sparse cluster that are all anomalies. 
- Nice discussion and motivation for Isolation Forest based approach. “Anomalies should be easier to isolate and so should have a shorter path length on average. 
- Need to look up reference on online isolation forest: “[An Anomaly Detection Approach Based on Isolation Forest Algorithm for Streaming Data using Sliding Window](https://www.sciencedirect.com/science/article/pii/S1474667016314999)”
- Statistical methods - estimation of probability densities. Can be quicker at inference time than clustering. 
- GMM’s as example approach here. But you still need to pick the number of gaussians. Bayesian GMM’s as option.
- ICA application to AD is worth looking at. 
- [NASA MKAD](https://ti.arc.nasa.gov/opensource/projects/mkad/) seems to get a lot of mention and looks like maybe SOTA in this setting.  
- PCA based motivation - if less important comps have bigger values then thats a sign of an anomaly. 
- Autoencoders motivation - anomalies cannot be compressed well. 
- Extreme Learning Machines (ELM) - some references to this - need to look it up.
- Overlapping sliding windows as feature transformers. 
- [MSCRED](https://arxiv.org/pdf/1811.08055.pdf) encdec+conv+lstm approach. Worth looking into. 
- A section and discussion around cases when interpretability matters and “temporal logic based learning” that can learn signal temporal logic (STL) predicates that human domain experts can then understand. No idea what this stuff is, need to look into it. Maybe start [here](https://ieeexplore.ieee.org/document/7500142/). 
- Good discussion on a range of different applications to the aviation sector. 
- Still what's actually in production a lot of the times in domain expert systems with manual thresholds.
- OC-SVM seems to come up quite a bit in the paper. 
- Whole section on anomaly detection as a input into predictive maintenance.  
- Once you have flagged anomalies maybe you can build models to look for precursor events before the anomaly. Part of discussion on temporal logic based learning. 

* * *

## Anomaly Detection in Flight Recorder Data: A Dynamic Data-driven Approach (NASA).

[Link](https://pdfs.semanticscholar.org/5cf8/81d1db19834f123fcfc79ad32097aeafe17f.pdf)

My Summary: A nice look at the different systems and approaches used in aviation. Interesting type of feature engineering proposed Symbolic Dynamic Filtering (SDF). 

Notes:

- Idea: What about using SDF feature extraction and then applying point based AD algos.
- SDF > PCA for feature based extraction and dimensionality reduction in some of the examples they looked at. 
- Seems like a lot more focus on unusual patterns as opposed to just point detection in flight setting. 
- Lots of good references on more traditional approaches and systems used in aviation.
- SDF - notions of fast scale vs slow scale time features in an interesting idea. 
- They used simple enough correlation based preprocessing to throw away and reduce redundant features.
- Looks like they compared normalised zscores to sdf based scores. 
- Big question is if SDF features can efficiently be calculated in an online setting. 

* * *

## Histogram-based Outlier Score (HBOS): A fast Unsupervised Anomaly Detection Algorithm

[Link](https://pdfs.semanticscholar.org/5cf8/81d1db19834f123fcfc79ad32097aeafe17f.pdf)

My Summary: Very quick and crisp paper, big focus on computational efficiency and linear time of HBOS. Main downside is HBOS seems mainly univariate. 

Notes:

- Linear scoring time.
- But does perform poorly on local outlier problems as opposed to global ones.
- Fast.
- 3 main categories of unsupervised AD:
    - Nearest Neighbour
    - Clustering 
    - Statistical
        - Parametric
            - GMM
        - Non-Parametric
            - Hist
            - KDE
- Main idea - just use histograms as density estimators!
- Dynamic bin’s recommended.
- One problem is that it's still just a point anomaly detector - scores a point at a time.
    - Maybe could get around this with post scoring smoothing or something but still a limitation.
- When and how to update the reference histogram?
- Maybe with careful feature processing or grouping it could be done in multivariate setting.
- Would be interesting to see how hbos compares to traditional zscore based approach.  

* * *

## Visualizing Big Data Outliers through Distributed Aggregation (HDOutliers)

[Link](https://www.cs.uic.edu/~wilkinson/Publications/outliers.pdf)

My Summary: Seems to have some nice properties but not clear if is suitable at all for an online setting.

Notes:

- Nice plots and discussion around boxen plots and letter-value-boxplot or dixons plot. 
    - IQR and traditional box plots flag way too much as outliers when data size is large, due to the ways percentiles are calculated, is an inherent property.
- Good discussion on underlying assumptions, their typical violations etc.
- Typical zscore based approaches assume normality but use estimated mean and stdev from data which are very sensitive to the presence of outliers - so there is a circularity here to be careful of. Some robust extensions to this are possible.
- Gaps based approach to univariate anomaly detection sound interesting. Not really applicable to multivariate data.
- All seems to revolve around a normalized X vector. 
- Unclear on the efficiency of the inference step if any.
- Mentions LOF as one of the most popular algos and does some comparisons to it.
- Interesting use of parallel coords chart to explore anomalies once detected.
- Non parametrics smoothers often used for time series setting, smoother as model and residuals as anomaly score. 
- HDOutliers does give a probability based threshold which is a nice property.    

* * *

## Anomaly Detection for Discrete Sequences: A Survey

[Link](http://i2pc.es/coss/Docencia/SignalProcessingReviews/Chandola2012.pdf)

My Summary: Interesting enough survey of a totally different way of potentially framing time series AD. Paper is from 2012 so a little old, but a good overview of higher level approaches in a more traditional sense.

Notes:

- We can sometimes map our anomaly detection problem into a sequence detection problem with a predefined alphabet. 
- There is a design choice around full sequence vs subsequence approach. 
- Computational complexity can be a concern if focusing on subsequences within long sequences (potential parallels to genomics in this regard).
- Wide range of domains and applications - this paper tries to give a more universal overview and approach that is agnostic of domain and application specifics.
- Three broad problem formulations
    - Entire sequence anomaly detection
    - Subsequence anomaly detection
    - Frequency lookup/reference based anomaly detection given a specific query sequence.
- Formulation 1 and 2 can be considered special cases of each other in certain circumstances. 
- For online time series AD we are either in 1 or 2 formulation.
- If anomaly length is known in advance then this can impact design a lot (e.g. known mutation lengths in DNA for example).
- Looks to me like this approach is fundamentally univariate based which could be one big drawback. 
- There are similarities to something like a language model and if probability for the ‘sentence’ is very small then it might be an anomaly. 
- Rolling window based approaches can better find localised anomalies. 
- Markovian and ‘model’ based approaches.
- Sparse markovian approaches allow for more flexible and inexact anomaly pattern matching. 
- HMM approaches can be very sensitive to underlying assumptions and params.
- Seems like these sequence based approaches could be useful to explore as a totally different way to attack the problem. So could not be strong enough on their own but could be useful in a more ensemble based approach. 
- Anomalous ‘discord’ detection within a sequence.
- Mentions Hot Sax paper - must look into this. 
- Some talk of bitmap based representations - need to look into this. 
- Third approach is to ask “What is the expected frequency of this sequence pattern?”.

* * *

## Anomaly Detection in Streams with Extreme Value Theory (SPOT)

[Link](https://hal.archives-ouvertes.fr/hal-01640325/document)

My Summary: Very interesting paper, hbos seems to have lots of advantages as being fast and making little assumptions. Very much focused on point anomaly setting.

Notes:

- Makes no assumptions about underlying distributions.
- Risk is only input parameter. 
- Can be used to automatically set dynamic thresholds.
- Idea: would it be possible to convert contextual or collective into a point detection setting by using clever feature transformations (e.g Catch22 etc).
- EVT is like a CLT type result but for extreme values.
- DSPOT for non-stationary case (D for Drift).
- They are working in a univariate and unimodal setting <- potential limitation. 
- Builds on Peak Over Thresholds (POT) approach to EVT estimation.
- DSPOT reacts quickly to change in stream properties. 
- Me: DSPOT is really comparable to zscore based approach for spike detection type setting. 
- They use typical taxonomy of distance based, nearest neighbour, or clustering. 
- Lots of interesting discussion and motivation around EVT and the nice properties it has. 
- Some detailed discussion on estimation approaches to EVT. 
- MLE as best way to estimate EVD properties. 
- Idea: potential to slice windows for feeding into DSPOT in non standard ways. 
- There is a burn in or ‘calibration’ phase that you kind of can think of an initial training step. N>=1000 is their recommendation. Just not too small. 
- Initial threshold t = 0.98, determines initialisation. 
- Python3 implementation here: [https://gforge.inria.fr/scm/browser.php?group\_id=9388](https://gforge.inria.fr/scm/browser.php?group_id=9388)
- SPOT is robust.
- Nice example application with some feature engineering around network attack setting. 
- Idea: using DSPOT and smoothing/preprocessing to tune various properties of the detector. 
- q param as a false positive regulator. Interesting ROC curve showing TPR vs FPR for different q values. 
- Another reference to [https://www.comp-engine.org/](https://www.comp-engine.org/) was made.   
- Curious why not preprocess to look at abs(diffs) in some of the examples they discuss. They also show evidence that this is slightly faster as opposed to bi-DSPOT.
- Well worth playing around with this algo to compare to traditional zscore based approach. 
- Maybe implementing it at different granularities could be useful/interesting. 

* * *
