# Coffee Pourover Visualization

## Introduction
[Pourover coffee](https://www.seriouseats.com/2014/06/make-better-pourover-coffee-how-pourover-works-temperature-timing.html) is a manual way to make a cup or two of coffee at a time. I became interested in coffee in college because it was an easy way to keep myself awake for all-nighters. A few years later, my home setup is more chemistry lab than kitchen. Like many experiments, consistency is king when you're looking for correlations, and coffee is no different. 

My visualization tool attempts to bring visibility to a generally overlooked point of variability: the pour. Pourover coffee uses a [narrow spouted kettle](https://www.google.com/search?tbm=isch&q=gooseneck+kettle) that provides a steady stream of water to be poured in circles over the coffee. Given that all extraction of the coffee comes from the contact of water to coffee, the pour pattern is an underlooked source of variability. With this project, I hope to shed some light into this topic.

## Video (sample)
![](https://media.giphy.com/media/Riyf0ealXqOoNG3i5j/giphy.gif)

## Algorithm
There are various out-of-the-box tracking algorithms available in openCV. The CSTR (Discriminative Correlation Filter with Channel and Spatial Reliability) tracker the spout the best. I adapted the code from [learnopencv](https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/) to start actually using the tracking software. 

## Data
The data needed from the video was straightforward: the center of the pourover device and the water-coffee contact points. I have the user select the center and spout locations themselves before running the video. While the video is running, water-coffee contact coordinates are collected for each frame.

Additional calculations were performed on the coordinates to translate them into a polar plot friendly format. Namely, the distance and angle between the two points (with respect to the x-axis) were calculated and labeled respectively as 'theta' and 'radii' below.

time | cone_x |cone_y	| water_x	| water_y	| theta	| radii
:---: | :---: | :---: | :---: | :---: | :---: | :---:
0.0718 | 719 |	635	| 848.16	| 496.17	| 281.12 | 189.61
0.1405 | 719 | 635	| 837.88	| 489.78	| 281.14	| 187.67
0.2110 | 719	| 635	| 822.25	| 491.43	| 280.58	| 176.84
0.2800 | 719	| 635	| 818.58	| 495.86	| 280.24	| 171.10

## Visualization
Below is the visualization that mimics the video's aerial view.
![](/Images/pour1_1_water_v60.png)
![](/Images/pour1_2_water_v60.png)

## Future Work
* Create golden batch
* Scale with different FOV
