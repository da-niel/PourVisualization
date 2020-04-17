# -*- coding: utf-8 -*-
"""
Spyder Editor

Kettle Tracker created by Daniel Chow using code adapted from https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/

Input: OpenCV compatible video file (e.g. .avi)
Output: CSV of coordinates: Center of Cone X, Center of Cone Y, Water-Coffee X, Water-Coffee Y
"""
#Packages
import cv2
import pandas as pd

#Initialize Variables
center_cone = [0,0]
vid_name = 'pour1'
vid_format = '.avi'
vid_path = vid_name + vid_format

pour_coordinates = []

# Function to save user selected point
def get_coordinates(event, x, y, flags, param) :
    if event == cv2.EVENT_LBUTTONDOWN :
        center_cone[0],center_cone[1] = x,y
        
        
# Saves point to center_cone variable
def get_center(frame):
    cv2.namedWindow('get center')
    cv2.setMouseCallback('get center', get_coordinates)
    while True:
        cv2.imshow('get center', frame)
        k = cv2.waitKey(20) & 0xff
        if k == 27: break
        elif k == ord('a'): print(center_cone[0], center_cone[1])
        
def initialize_tracker(tracker_type):
    if tracker_type =='BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    elif tracker_type =='MIL':
        tracker = cv2.TrackerMIL_create()
    elif tracker_type =='KCF':
        tracker = cv2.TrackerKCF()
    elif tracker_type =='TLD':
        tracker = cv2.TrackerBoosting_create()
    elif tracker_type =='MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    elif tracker_type =='GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    elif tracker_type =='MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    elif tracker_type =='CSRT':
        tracker = cv2.TrackerCSRT_create()
    
    return tracker


# Main Program
if __name__ == '__main__':
    
    # Set Up Tracker - Tracker Types: 'BOOSTING','MIL','KCF','TLD','MEDIANFLOW','GOTURN','MOSSE','CSRT'
    tracker_type = 'CSRT'
    tracker = initialize_tracker(tracker_type)

    # Read Video Path
    video = cv2.VideoCapture(vid_path)
    # Read first frame
    ok, frame = video.read()    
    
    # Center of V60 UserSelection
    if ok:
        get_center(frame)
    
    
    # User selects custom box to track kettle
    # Enter space to accept selection
    bbox = cv2.selectROI(frame,False)
    ok = tracker.init(frame, bbox)
    
    while True:
        # Ends if no more frames
        ok, frame = video.read()
        if not ok:
            break
        
        # Update bounding box
        ok, bbox = tracker.update(frame)

        if ok:
            # Display ROI
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1,p2, (255,0,0),2,1)
            
            # Estimate water-coffee contact point
            m = (bbox[3]-bbox[1])/(bbox[2]-bbox[0])
            x = bbox[0] - 200
            y = m*x + 200
            
            # Save coordinates to pour_coordinates
            pour_coordinates.append((center_cone[0],center_cone[1],x,y))
            
            # Display water-coffee contact point
            cv2.rectangle(frame,(int(x-5),int(y-5)),(int(x+5),int(y+5)),(255,0,0),-1)
            
            # Display Center of Cone
            cv2.rectangle(frame,(int(center_cone[0]-5),int(center_cone[1]-5)),(int(center_cone[0]+5),int(center_cone[1]+5)),(255,0,0),-1,1)
        else:
            # Tracking Failure
            cv2.putText(frame, "Object out of view",(100,80),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
        
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + "tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
        cv2.imshow("Tracking",frame)
        
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break

# Save data to csv
output = pd.DataFrame(pour_coordinates, columns = ['Cone X','Cone Y','Water X','Water Y'])
output.to_csv(vid_name + '_coordinates.csv', index=False)

cv2.destroyAllWindows()
    