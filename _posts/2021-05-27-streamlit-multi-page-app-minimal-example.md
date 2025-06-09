---
title: "streamlit multi-page app minimal example"
date: 2021-05-27
categories: 
  - "apps"
  - "eng"
tags: 
  - "app"
  - "python"
  - "streamlit"
  - "web"
---

<figure>

![](/assets/images/2021-05-27-streamlit-multi-page-app-minimal-example/app_a_litt_up.jpg)

<figcaption>

too obvious? maybe. probably.

</figcaption>

</figure>

Recently i had a need to assess [streamlit](https://streamlit.io/) for some internal DS/ML/Data apps i wanted to build in my job. By "i had a need" i mean i heard it was the new cool thing so i wanted to play with it and feel better about myself. Anyway, as part of that i built a horribly useless app to try capture the main things i was after.

In the end i went with [Dash](https://plotly.com/dash/) instead (mainly due to needing tabs and some additional messy 'state' related stuff i could find lots of dash examples for) but i'm pretty sure next time i need to do something similar i will 100% use streamlit as my goto given its just so easy to get going with and should be more than acceptable for 80-90% of my use cases (plus its got a lot of momentum and is getting better and better over time).

So in this post i am sharing a little cleaned up version of the dummy streamlit app i built as a little poc to see if i could get what i needed from it. Also, a few student's in the course where i mentor have been playing with streamlit as part of building an app to share and publish their ml models so i'm hoping this might be useful to refer them too as a potential starting point (although there are many many much cleaner examples in the [streamlit gallery](https://streamlit.io/gallery)). But if you want some of the features below then my little frankenstein here might be an ok starting point for you.

- Some notion of a multipage app where each app can have itself different "screens" or "pages".
- A `src` type folder where you might write custom python modules you want to have available to all your "apps" or "screens" within the app.
- Ability to easily deploy it to [streamlit sharing](https://streamlit.io/sharing), for example this app should be up and available [here](https://share.streamlit.io/andrewm4894/streamlit-learn/main/app.py).
- Show different logos etc on different pages.
- Have dynamic inputs that can vary in types and number of inputs depending on each page.
- Some functions to do stuff with the inputs.

**TL; DR** - Here is the app running on streamlit share: [https://share.streamlit.io/andrewm4894/streamlit-learn/main/app.py](https://share.streamlit.io/andrewm4894/streamlit-learn/main/app.py) and [here is the code](https://github.com/andrewm4894/streamlit-learn) on Github.

## Project structure

Here is how the project is structured and below are some notes on each folder or file.

<figure>

![](/assets/images/2021-05-27-streamlit-multi-page-app-minimal-example/image.png)

<figcaption>

project tree structure

</figcaption>

</figure>

Here are each of the main folders/files and what they do.

- `/.streamlit` - This is where some streamlit specific config files like `config.toml` live, more info in streamlit docs [here](https://docs.streamlit.io/en/stable/streamlit_configuration.html).
- `/apps` - This is where we have an `app_<name>.py` file for each app within our overall streamlit app. For example, `/apps/app_silly_strings.py` contains as much of the logic and code that is specific to the "silly string stuff" app.
- `/assets` - The place where your images and other similar types of files live that you want to use across your apps.
- `/src` - For python code and functions you want to have available on any page of your app you can make a custom module in here. For example the `funny_numbers` module has the functions used by the "crazy numbers" app.
- `app.py` - This is the main streamlit app we launch via `streamlit run app.py` which will import and render the other apps as needed.
- `Pipfile` - Pipenv is used in this example instead of a requirements.txt or any other approaches to define the python environment the app should run in.

That's it, you can look at the code and see it all for yourself, i've also added a README to each folder to make it as clear as possible (some [potential todo's](https://github.com/andrewm4894/streamlit-learn#todo) that could make it a better example).

Lastly, here is a pointless video of me clicking some stuff...

https://videopress.com/v/FSHpaMxM?loop=true&muted=true&persistVolume=false&playsinline=true&preloadContent=metadata
