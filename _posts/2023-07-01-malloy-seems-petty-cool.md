---
title: "Malloy seems petty cool..."
date: 2023-07-01
categories: 
  - "data-eng"
tags: 
  - "data"
  - "data-eng"
  - "etl"
  - "malloy"
  - "sql"
coverImage: "malloy.png"
layout: post
---

I discovered [Malloy](https://github.com/malloydata/malloy) recently in [this great talk](https://youtu.be/zmmJgwc3oPI), it seems like a really interesting idea (a higher level abstraction or DSL on top of sql) with some great people behind it ([looker founder](https://www.linkedin.com/in/lloydtabb/) who seems to really know his stuff).

So I decided to try get going with it in as minimal a way as possible using everyone's favourite dataset.

[https://github.com/andrewm4894/learn-malloy](https://github.com/andrewm4894/learn-malloy)

To get going all you need to do is:

- install [malloy vscode extension](https://marketplace.visualstudio.com/items?itemName=malloydata.malloy-vscode)

- that's pretty much it, each .malloy or .malloynb file will make it obvious how to run queries or run usual notebook style flow.

## Moving parts

- a [source object](https://github.com/andrewm4894/learn-malloy/blob/main/titanic/titanic.source.malloy) defining some sort of data connection (in this case just a local csv) and, optionally, some additional measures and dimensions.

- some [queries](https://github.com/andrewm4894/learn-malloy/blob/main/titanic/titanic.queries.malloy) against a source. This is where i think it essentially becomes a sort of [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) (and more) on top of SQL.

- optionally some [style objects](https://github.com/andrewm4894/learn-malloy/blob/main/titanic/titanic.styles.json) that can help map queries to output visualisations. This is what's behind the magic of some of the default visualizations in the cool demos [here](https://github.com/malloydata/try-malloy).

- even the ability to bring it all together into a familiar [notebook](https://github.com/andrewm4894/learn-malloy/blob/main/titanic/titanic.notebook.malloynb) experience.

## Initial thoughts

- Seems like a really interesting project and idea (no doubt a lot has been learned from look.ml and those learnings will be baked into this project).

- Seems to have a lot of the abstractions right imo - feels natural in some sense while also still quite flexible.

- I was able to just guess about 70% of what I wanted or expected when writing some example queries.

- Can't wait until I can use this natively in something like BigQuery UI and easily share results of analysis with co-workers.

- Seem to be a cool use case for duckdb in my csv example - need to learn more how that's all working.

- I could see this becoming a nice standard way to package up and share analysis type projects with bosses and colleagues in a way that they can easily then play with, customize and build on if they have follow on questions - so i no longer become the bottleneck - great!

- Could also see this be quite a useful tool to translate and define business questions with stakeholders without having to show them any sql!

- One of my hot takes over last few years was that SQL is the new excel, but maybe Malloy could also be the new excel.
