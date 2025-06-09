---
title: "Java Weka API: Adding List To Instances Object"
date: 2019-04-30
categories: 
  - "java"
tags: 
  - "weka"
  - "weka-api"
---

This is just a quick one to save anyone else new to the [Weka api in Java](https://waikato.github.io/weka-wiki/use_weka_in_your_java_code/) spending as much time as i did figuring this one out.

Lets suppose you have a weka instances object and a new list of values you want to add into it as a new attribute (weka slang for a new column in your data).

Below gist shows a small reproducible example of this.

https://gist.github.com/andrewm4894/9e78efeb96921e5272ae2d1d2d603fef

And you should see some output like this:

```
====== BEFORE ====== sepallength,sepalwidth,petallength,petalwidth,class 5.1,3.5,1.4,0.2,Iris-setosa 4.9,3,1.4,0.2,Iris-setosa 4.7,3.2,1.3,0.2,Iris-setosa 4.6,3.1,1.5,0.2,Iris-setosa 5,3.6,1.4,0.2,Iris-setosa====== AFTER ====== sepallength,sepalwidth,petallength,petalwidth,class,randomDouble 5.1,3.5,1.4,0.2,Iris-setosa,0.173003 4.9,3,1.4,0.2,Iris-setosa,0.304703 4.7,3.2,1.3,0.2,Iris-setosa,0.925626 4.6,3.1,1.5,0.2,Iris-setosa,0.733839 5,3.6,1.4,0.2,Iris-setosa,0.710073
```

Above we can see the new attribute "randomDouble" has been added to the instances object.

I'm learning the weka java api at the moment so will try post little tidbits like this that could be useful for others of even myself 6 months from now :)
