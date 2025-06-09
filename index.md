---
layout: default
title: Home
---

# Welcome

This is the new home of my blog, now powered by **GitHub Pages** and **Jekyll**.

## Latest Posts

{% for post in site.posts %}
  <article>
    <h2>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h2>
    <time datetime="{{ post.date | date: "%Y-%m-%d" }}">{{ post.date | date: "%B %d, %Y" }}</time>
    {% if post.description %}
      <p>{{ post.description }}</p>
    {% endif %}
  </article>
{% endfor %}
