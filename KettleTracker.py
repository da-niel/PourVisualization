# -*- coding: utf-8 -*-
"""
Spyder Editor

Kettle Tracker created by Daniel Chow using code adapted from https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/

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
vid_name = 'pour1'
vid_format = '.avi'
vid_path = vid_name + vid_format

pour_coordinates = []

def get_coordinates(event, x, y, flags, param):
    # Saves coordinates of mouse click to center_cone
    if event == cv2.EVENT_LBUTTONDOWN :
        center_cone[0],center_cone[1] = x,y
        
        
def get_center(frame):
    # Saves clicked point to center_cone variable
    # User presses ESC to exit
    cv2.namedWindow('get center')
    cv2.setMouseCallback('get center', get_coordinates)
    while True:
        cv2.imshow('get center', frame)
        k = cv2.waitKey(20) & 0xff
        if k == 27: break
        elif k == ord('a'): print(center_cone[0], center_cone[1])
        
        
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


def save_radial_scatterplot(theta, radii, path):
    # force square figure and square axes looks better for polar, IMO
    plt.figure(figsize=(8,8))
    
    ax = plt.subplot(111, 
                     projection='polar')
    
    colors = range(len(theta))
    
    ax.scatter(theta,
               radii,
               c=colors,
               cmap = 'Greens')
    
    ax.set_xticklabels([])
    ax.set_rmax(400)
    ax.set_rgrids([])
    ax.set_thetagrids([90,180,270,0])
    ax.set_title('Distribution of water on a V60')
    plt.savefig(path + '.png')
    
    

def periodic_time_plot(time, radii):
    plt.figure(figsize=(16,8))
    fig, ax = plt.subplot()
    
    ax.plot(time, 
            radii, 
            marker = '.', 
            c='Blue')

    ax.set_ylabel('Distance (pixels)')
    ax.set_xlabel('Time (frames)')
    ax.set_title('Evolution of a Manual Pour')
    
    plt.show()
    
  
# Main Program
if __name__ == '__main__':
    
    # Set Up Tracker - Tracker Types: 'BOOSTING','MIL','KCF','TLD','MEDIANFLOW','GOTURN','MOSSE','CSRT'
    tracker_type = 'CSRT'
    tracker = create_tracker(tracker_type)

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
            
            # Save coordinates to pour_coordinates - adjusted
            pour_coordinates.append((center_cone[0], center_cone[1], x, y))
            
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
output = pd.DataFrame(pour_coordinates, columns = ['cone_x','cone_y','water_x', 'water_y'])

# Calculate angle
output['theta'] = output.apply(calculate_angle, axis = 1)

# Calculate distance from center
output['radii'] = np.sqrt((output.water_x - output.cone_x)**2 + (output.water_y - output.cone_y)**2)

# Time variable
output['time'] = range(1,len(output)+1)

# Save and close
print('Saving file...')
output.to_csv(vid_name + '_coordinates.csv', index = False)
print('Making plot...')
save_radial_scatterplot(output.theta, output.radii, 'water_v60')
print('Now exiting...')
cv2.destroyAllWindows()
    