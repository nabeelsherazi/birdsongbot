# Birdsong

_A sweet tweetbot built at [HackBeanpot 2017](https://hackbeanpot.com) by [Nabeel Sherazi](https://github.com/nabeelsherazi) (Northeastern University), Kyle Coelho (Northeastern University), [Cole Wuilleumier](https://github.com/Cole-Wuilleumier/) (Bunker Hill Community College), Noah Sirin (Berklee College), and Khang Bui (UMass Amherst)_

> Birdsong is a Twitter bot that intelligently distinguishes haikus leveraging the latest advancements in machine learning technology and plays an accompanying musical arrangement to fit the sentiment of the text. ~ Our buzz-tastic flavor text

**🏅 Won 3rd place in Best Use of Indico API and the Genuine #InventTogether Award 🏅**

[Check out our project listing here!](https://projects.hackbeanpot.com/2017-projects.html)

[Meet the real birdsongbot on Twitter!](https://twitter.com/birdsongbot) (May or may not be running at the moment)

## About (for real)

We dreamed up Birdsong as a collaborative art experience, with a vision to connect people through poetry. Twitter is a medium that allows people from all around the world to talk to each other, but it falls short of real human connection. We wanted to bridge this gap by creating a bot that would give friends on the internet a real voice -- through poetry. When installed, people could gather around Birdsong and hear poetry sent to them from around the world. Together, we're art.

## Features

* Cross-platform (Windows, Mac, Linux) thanks to PyTTSx3
* Easy to setup
* Customizable via config.ini
* Spam filter and abuse filter built in
* Cool as heck!!

## How to use

Create a [Twitter](https://twitter.com) account, and open the Twitter Developer console. Obtain a consumer key, consumer secret, access token, and access token secret. Add these keys, and the username of the Twitter account you created, into the config.ini file.

Create an [Indico](https://indico.io) account. Get an API key. Add this to config.ini as well.

In the root directory, install all required modules by running `pip install -r requirements.txt`

You should now be all set! Start the bot with `python start.py`. Happy Haikuing!!

## Acknowledgements

We'd like to thank the HackBeanpot team for putting on such a great event, Genuine and Indico for letting us play in their place (and the nice prizes!).

Thanks is also given to [AbigailB on StackOverflow](https://stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word) for her neat syllable counting function, and [Luis von Ahn at Carnegie Mellon University](https://www.cs.cmu.edu/~biglou/resources/) for his list of bad words.
