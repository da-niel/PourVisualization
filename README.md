# Coffee Pourover Visualization

## Introduction
[Pourover coffee](https://www.seriouseats.com/2014/06/make-better-pourover-coffee-how-pourover-works-temperature-timing.html) is a manual
way to make a cup or two of coffee at a time. I became interested in coffee in college because it was an easy way to keep myself awake for all-nighters. A few years later, my home setup is more chemistry lab than kitchen. Like many experiments, consistency is king when you're looking for correlations and coffee is no different. 

My visualization tool is tackling a typically overlooked point of variability (at least by my standards). The water is poured from a [narrow spouted kettle](https://www.google.com/search?tbm=isch&q=gooseneck+kettle) that provides a steady stream of water dumped in circles over the coffee.

I used image tracking algorithms in openCV that to visualize the water pattern over the coffee.

## The Video


## The Algorithm
There are various out-of-the-box tracking algorithms available in openCV. For my first time, I manually checked which algorithm performed the best. By a mile, it was the DCF-CSR (Discriminative Correlation Filter with Channel and Spatial Reliability) tracker that exceled. 
I adapted the code from [learnopencv](https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/) to start actually using the tracking software. 

## The Data
The data needed from the video was pretty simple: the center of the pourover device and the water-coffee contact points. I have the user select the center and spout locations themselves before running the video. While the video is running, I continue to collect the water-coffee contact coordinates.

## The Analysis
The visualization of the data was not straightforward. It had to show not only the pattern of the pour, but also how the pattern changes over time.
