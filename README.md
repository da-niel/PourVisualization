# Coffee Pourover Visualization

## Introduction
[Pourover coffee](https://www.seriouseats.com/2014/06/make-better-pourover-coffee-how-pourover-works-temperature-timing.html) is a manual
way to make a cup or two of coffee at a time. I became interested in coffee in college because it was an easy way to keep myself awake for all-nighters. A few years later, my home setup is more chemistry lab than kitchen. Like many experiments, consistency is king when you're looking for correlations and coffee is no different. 

My visualization tool attempts to bring visibility to a typically overlooked point of variability (at least by my standards). The water is poured from a [narrow spouted kettle](https://www.google.com/search?tbm=isch&q=gooseneck+kettle) that provides a steady stream of water dumped in circles over the coffee. I used image tracking algorithms in openCV that to visualize the water pattern over the coffee.

## Video (sample)
![](https://media.giphy.com/media/Riyf0ealXqOoNG3i5j/giphy.gif)

## Algorithm
There are various out-of-the-box tracking algorithms available in openCV. The DCF-CSR (Discriminative Correlation Filter with Channel and Spatial Reliability) tracker the spout the best. I adapted the code from [learnopencv](https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/) to start actually using the tracking software. 

## Data
The data needed from the video was straightforward: the center of the pourover device and the water-coffee contact points. I have the user select the center and spout locations themselves before running the video. While the video is running, water-coffee contact coordinates are collected for each frame.

Additional calculations were performed on the coordinates to translate them into a polar plot friendly format. Namely, the distance and angle between the two points (with respect to the x-axis) were calculated and labeled respectively as 'theta' and 'radii' below.

time | cone_x |cone_y	| water_x	| water_y	| theta	| radii
:---: | :---: | :---: | :---: | :---: | :---: | :---:
1 | 719 |	635	| 848.16	| 496.17	| 281.12 | 189.61
2 | 719 | 635	| 837.88	| 489.78	| 281.14	| 187.67
3 | 719	| 635	| 822.25	| 491.43	| 280.58	| 176.84
4 | 719	| 635	| 818.58	| 495.86	| 280.24	| 171.10

## Visualization
Below is the visualization that mimics the video's aerial view.
![](/water_v60.png)
![](/pour1_2_water_v60.png)

## Future Work
As I continue to process more videos, I can create a "golden batch" of the perfect pour, in which all subsequent pours would be based off of.
