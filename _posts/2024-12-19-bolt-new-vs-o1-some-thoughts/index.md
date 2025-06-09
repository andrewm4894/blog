---
title: "bolt.new vs o1 - some thoughts"
date: 2024-12-19
categories: 
  - "llm"
  - "machine-learning"
tags: 
  - "llm"
coverImage: "Screenshot-2024-12-19-at-12.16.10 PM.png"
---

this is funny - i tried to make a little app to share daily factoids from chatgpt on a site - just as excuse to learn javascript really.

bolt.new is great and i felt like a wizard at first just freestyling away on the keys but man what a mess i ended up creating - ended up down various dead ends with firebase and deployment to netlify and lots of infra related mess that ended up waaay too complex for me at that stage down the rabbirt hole to know where to start to try untangle anything.

so i jumped over to chatgpt o1 and just have an actual conversation and some back and forth - chatgpt was much more nuanced and less eager to just start cranking out code for me.

we took it step by step and i was actually learning some stuff at each stage rather than blind and wild js flying all over the place.

so ended up with an actual repo in gh thats deployed and a fairly decent starting point for what i want: [https://github.com/andrewm4894/andys-daily-factoids](https://github.com/andrewm4894/andys-daily-factoids)

[https://andys-daily-factoids.com](https://andys-daily-factoids.com)

Anyway funny part is that all my factoids are about how Octopuses have 3 hearts! It really really loves this fact.

Also honey does not spoil is a strong 2nd favorite.

Next step is to add last 100 or so factoids in the prompt and ask it not to repeat itself...
