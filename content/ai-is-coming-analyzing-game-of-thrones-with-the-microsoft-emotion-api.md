Title: AI is coming: Analyzing Game of Thrones with the Microsoft Emotion API
Date: 2016-11-08 05:01
Author: Jeorry Balasabas
Category: Machine Learning
Tags: AI, Machine Learning, Python
Slug: ai-is-coming-analyzing-game-of-thrones-with-the-microsoft-emotion-api
Status: Published
Summary: A walkthrough of using Microsoft's Emotion API to parse emotions from facial expressions in a short clip of HBO's Game of Thrones.

 

If you had told me a year ago that Microsoft had a Machine Learning
platform that was capable of performing analysis of images and video I
think I would have muttered something about pigs and flight. Pay
attention, I am now taking my foot out of my mouth. I'll be the first to
admit when I'm wrong. Not only does Microsoft have a Emotion API capable
of determining emotions in faces from image and video but they have an
entire stable of machine learning APIs that they have labled "Cognitive
Services". I was first turned on to Microsoft's machine learning APIs
after reading the Economist's article on tracking the facial expression
of Hillary and Donald
[here](http://www.economist.com/blogs/graphicdetail/2016/10/daily-chart-12).
I was inspired to perform my own analysis of facial expressions using
one of my favorite shows, Game of Thrones, as a sample. My intent is to
provide a little guidance on using the Microsoft Emotion API and
encourage some creativity in performing your own analysis.

This isn't your grandpa's API. I've always associated Microsoft API with
.NET. Much to my surprise, Cognitive Services uses REST and provides
examples in the following languages:

-   Curl
-   C\#
-   Java
-   Javascript
-   ObjC
-   PHP
-   Python
-   Ruby

For this post I've chosen Python and some associated data science
libraries. I want to give a lot of credit to Ben Heubl, a journalist who
was part of the Economist article. Without the help of his
[post](https://benheubl.github.io/data%20analysis/fr/) my analysis
wouldn't have been possible. As much as Microsoft has done to make their
machine platform open to everyone, their documentation is almost
non-existent. Hopefully this post can provide some assistance to those
of you who are looking to get started with the Cognitive Services API.
If you want to skip the explanation you can access my jupyter notebook
[here](https://github.com/jeorryb/Emotion_API/blob/master/emotion_api_video.ipynb).

First we need to import some libraries.

    :::python
    import httplib
    import urllib
    import base64
    import json
    import ijson
    import pandas as pd
    import numpy as np
    import requests
    import matplotlib.pyplot as plt
    %matplotlib inline


In order to use Microsoft's Cognitive Services API you need to sign up
for a free API key
[here](https://www.microsoft.com/cognitive-services/en-us/sign-up).

    :::python
    # you have to sign up for an API key, which has some allowances. Check the API documentation for further details:
    _url = 'https://api.projectoxford.ai/emotion/v1.0/recognizeInVideo'
    _key = 'your key here' #Here you have to paste your primary key
    _maxNumRetries = 10


Next we use Python's Requests library to post and get data from the
Microsoft API. In my sample I used a Game of Thrones Season 7 trailer
that I found on youtube and converted to MP4. You can also point the API
at a url for your video file and I suggest reading the API docs for
details.

    :::python
    paramsPost = urllib.urlencode({'outputStyle' : 'perFrame', 'file':'/Volumes/data/Movies/gots7.mp4'})
    headersPost = dict()
    headersPost['Ocp-Apim-Subscription-Key'] = _key
    headersPost['Content-Type'] = 'application/octet-stream'
    jsonGet={}
    headersGet = dict()
    headersGet['Ocp-Apim-Subscription-Key'] = _key
    paramsGet = urllib.urlencode({}) 
    responsePost = requests.request( 'post', _url + "?" + paramsPost,   
                                   data = open('/Volumes/data/Movies/gots7.mp4','rb').read(),   
                                   headers = headersPost)
    print responsePost.status_code


A status code of '202' is a success and means we can proceed with our
analysis. Next we proceed with processing the result of our post of the
video file.

    :::python
    videoIDLocation = responsePost.headers['Operation-Location']
    print videoIDLocation
    getResponse = requests.request( 'get', videoIDLocation,   
                                     data = None, headers = headersGet, params = paramsGet )
    rawData = json.loads(json.loads(getResponse.text)['processingResult'])
    emotionPerFramePerFace = {}
    currFrameNum = 0
    for currFragment in rawData['fragments']:
        if 'events' in currFragment:
            for currEvent in currFragment['events']:
                emotionPerFramePerFace[currFrameNum] = currEvent
                currFrameNum += 1
    emotionPerFramePerFace = {}
    currFrameNum = 0
    for currFragment in rawData['fragments']:
        if 'events' in currFragment:
            for currEvent in currFragment['events']:
                emotionPerFramePerFace[currFrameNum] = currEvent
                currFrameNum += 1


The following is a snippet of the dictionary that is created from the
response. As you can see, Microsoft breaks the video clip into frames.
For each frame it analyzes the faces in each frame and assigns a score
for the emotions sadness, neutral, contempt, disgust, anger, surprise,
fear, and happiness.

    :::python
    [{u'height': 0.461111, u'width': 0.259375, u'scores': {u'sadness': 0.490348, u'neutral': 0.50085, u'contempt': 0.00298951, u'disgust': 0.00246058,     u'anger': 0.000952272, u'surprise': 0.000819597, u'fear': 0.00130964, u'happiness': 0.000270213}, u'y': -0.0388889, u'x': 0.540625, u'id': 0}]


Naively I thought that I would be able to parse the output and write
this post in a day. The reality is I spent almost a week researching all
the different ways I could parse dictionaries within lists within
dictionaries. After a lot of cursing and and googling I realized I
should have used the method that Ben used in his original article. Below
is basically the same method with a little tweaking.

    :::python
    gotemotions = []
    for frame_no, v in emotionPerFramePerFace.copy().items():
        for i, minidict in enumerate(v):
            for k, v in minidict['scores'].items():
                minidict[k] = v
            minidict['frame'] = frame_no
            gotemotions.append(minidict)


Now we convert to a Pandas dataframe.

    :::python
    dfgot = pd.DataFrame(gotemotions)


Finally, we chart the averages of each emotion for the video clip.

    :::python
    emotions = dfgot[['anger', 'contempt', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']]
    avgemotion = emotions.mean()
    avg_plot = avgemotion.plot(kind='bar', legend=None, title='Avg. Emotions')
    avg_plot.set_xlabel('Emotions')
    avg_plot.set_ylabel('Score')


![Average Emotions]({filename}/images/emotion_api_video.jpg)

If you're a Game of Thrones fan then it should come as no surprise to
see sadness as the emotion with the highest average. I was surprised to
see happiness as a close second. Maybe HBO didn't want viewers to get to
depressed on the final season and wanted to provide some balance. What
really excites me is the potential uses for this API. Imagine Netflix
performing emotion analysis on all their content and then feeding that
into their recommendation engine for a more accurate prediction. (I'm
pretty sure they are already doing this.) The use cases extend beyond
media and could be used to assist people with Autism to better
understand others emotions through facial expressions. I can see public
speakers analyzing their own facial expressions as well as the crowd
they are speaking to be more effective. This kind of analysis would have
been considered fairy dust 5 years ago. With the help of Microsoft I was
able to perform this on my laptop in a couple of hours. Microsoft might
not be top of mind when it comes to AI and Machine Learning, but I'd
watch out if I were Google and Amazon. Satya Nadella has a trick or two
left up his sleeve.
