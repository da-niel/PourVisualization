# -*- coding: utf-8 -*-
"""
Spyder Editor

Created by Daniel Chow

Input: Video file compatible with OpenCV (e.g. .avi)
Output: CSV of coordinates: Center of Cone X, Center of Cone Y, Water-Coffee X, Water-Coffee Y
"""
#Packages
import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Initialize Variables
center_cone = [0.0,0.0]
vid_name = 'pour1_2'
vid_format = '.avi'
vid_path = vid_name + vid_format
pour_coordinates = []


def get_coordinates(event, x, y, flags, param):
    # Saves coordinates of mouse click to center_cone
    if event == cv2.EVENT_LBUTTONDOWN :
        center_cone[0],center_cone[1] = x,y
        
        
def get_center(frame, video):
    # Saves clicked point to center_cone variable
    # User presses ESC to exit
    cv2.namedWindow('get center')
    cv2.setMouseCallback('get center', get_coordinates)
    while True:
        cv2.putText(frame, 
                    "1. Get center: Click to make selection. Press ESC when finished. Press 'a' to advance to next frame", 
                    (100,80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.75, 
                    (50,170,50),
                    2)
        cv2.imshow('get center', frame)
        k = cv2.waitKey(20) & 0xff
        if k == 27: 
            return frame
        elif k == ord('a'): 
            ok, frame = video.read() #move to next frame
        
        
def create_tracker(tracker_type):
    # Initializes the tracker based on the tracker_type
    # Returns the initialized tracker
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


def calculate_angle(coordinates):
    # Calculates angle of a point (x,y) with respect to origin and x-axis
    # Values range from 0 - 359 degrees
    
    x1 = coordinates[0]
    y1 = coordinates[1]
    x2 = coordinates[2]
    y2 = coordinates[3]
    
    # Create vector of x, y
    v_1 = [x1, y1]
    v_2 = [x2, y2]
    
    # Create unit vector of x, y
    uv_1 = v_1 / np.linalg.norm(v_1)
    uv_2 = v_2 / np.linalg.norm(v_2)
    
    # Calculate angle in radians
    angle = np.arccos(np.clip(np.dot(uv_1, uv_2),-1.0, 1.0))
    
    # Convert to degrees
    angle = angle*180/np.pi
    
    if x2 < x1 and y2 > y1:
        #Quadrant 2
        angle += 90
        return angle
    elif x2 < x1 and y2 < y1:
        #Quadrant 3
        angle += 180
        return angle
    elif x2 > x1 and y2 < y1:
        # Quadrant 4
        angle += 270
        return angle
    else:
        # Quadrant 1
        return angle
    
    return angle


def save_radial_scatterplot(time, theta, radii, path):
    
    plt.figure(figsize=(10,8))
    
    ax = plt.subplot(111, 
                     projection='polar')
    
    colors = time
    
    sc = ax.scatter(theta,
                    radii,
                    c=colors,
                    cmap = 'coolwarm',
                    vmin = min(time),
                    vmax = max(time))
     
    
    plt.colorbar(sc,label = 'Location of water over time (s)')
    ax.set_rmax(500)
    ax.set_xticklabels([])
    ax.set_rgrids([250])
    ax.set_thetagrids([90,180,270,0])
    ax.set_title('Distribution of water on a V60')
    plt.savefig(path + '.png', dpi = 300)
    
  
# Main Program
if __name__ == '__main__':
    
    # Set Up Tracker
    tracker_type = 'CSRT'
    tracker = create_tracker(tracker_type)

    # Read Video Path
    video = cv2.VideoCapture(vid_path)
    
    # Read first frame
    ok, frame = video.read()    
    
    # Get Center of V60
    if ok:
        frame = get_center(frame, video)
    
    # Get ROI
    cv2.putText(frame, 
                "2. Select ROI: Click and drag to make selection. Press space when finished.", 
                (100,150), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.75, 
                (50,170,50),
                2)
    bbox = cv2.selectROI(frame,False)
    ok = tracker.init(frame, bbox)
    
    #Track time elapsed
    time = 0.0
    
    while True:
        # Ends if no more frames
        ok, frame = video.read()
        if not ok:
            break
        
        #Start timer
        timer = cv2.getTickCount()
        
        # Update bounding box
        ok, bbox = tracker.update(frame)
        
        #Calculate FPS
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        
        time += 1 / fps
        
        if ok:
            # Display ROI
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1,p2, (255,0,0),2,1)
            
            # Estimate water-coffee contact point
            m = (bbox[3]-bbox[1])/(bbox[2]-bbox[0])
            x = bbox[0] - 200
            y = m*x + 200
            
            # Save coordinates to pour_coordinates - adjusted
            pour_coordinates.append((time, center_cone[0], center_cone[1], x, y))
            
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


# Convert to DF
output = pd.DataFrame(pour_coordinates, columns = ['time', 'cone_x', 'cone_y', 'water_x', 'water_y'])

# Calculate angle
output['theta'] = output.apply(calculate_angle, axis = 1)

# Calculate distance from center
output['radii'] = np.sqrt((output.water_x - output.cone_x)**2 + (output.water_y - output.cone_y)**2)

# Save and close
print('Saving file...')
output.to_csv(vid_name + '_coordinates.csv', index = False)
print('Making plot...')
save_radial_scatterplot(output.time, output.theta, output.radii, vid_name + '_water_v60')
print('Now exiting...')
cv2.destroyAllWindows()
    