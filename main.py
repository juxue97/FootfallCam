import cv2 as cv
import numpy as np
import time

from windowcapture import WindowCapture #capture screenshots
from model_person import Model

#print("start - s")
print("quit - q") 
time.sleep(2) 

# Initialize some constants
window_name = 'Media Player'
xs = 575
xe = 790
y_line_u = 275
y_line_b = 400

start_point_u = (xs, y_line_u)
end_point_u = (xe, y_line_u)

start_point_b = (xs, y_line_b)
end_point_b = (xe, y_line_b)

#WindowCapture.list_window_names() 
wincap = WindowCapture(window_name)  
object = Model(frame=wincap.screenshot)

# Start the thread
wincap.start()
object.start()

#object detection plot
def plot_obj(mode=3):
        if mode == 1: # circle - person 
            for person in object.coor_person:
                cx1,cy1,_,_,id1 = person
                cv.circle(object.frame, (cx1,cy1), 7, (0,0,255), -1)
                cv.putText(object.frame , f'pos_person{id1}: {cx1,cy1}', (cx1, cy1 - 10), cv.FONT_HERSHEY_COMPLEX, 0.8, (255, 0, 255), 2)
    
        elif mode == 2: # circle - tag 
            for tag in object.coor_tag:
                cx2,cy2,_,_,id2 = tag
                cv.circle(object.frame, (cx2,cy2), 7, (255,0,0), -1)
                cv.putText(object.frame , f'pos_tag{id2}: {cx2,cy2}', (cx2, cy2 - 10), cv.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 0), 2)

        else: # rectangle - mixed
            for obj in object.rect:
                x1, y1, x2, y2, c, cate=obj
                cv.rectangle(object.frame , (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv.putText(object.frame , f'{cate}: {c}', (x1, y1 - 10), cv.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 1)

#main display
def display(frame):
    #cropped_img = ss[:,450:950]
    #cropped_img = ss[:,220:580]
    overall_fps = f'Main fps: {main_fps:.2f}'
    ss_fps_text = f'Screenshot Capture fps: {wincap.fps:.2f}'

    cv.putText(frame , overall_fps, (10, 70), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv.putText(frame , ss_fps_text, (10, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Set decision boundary
    #_line_up 
    #cv.line(object.frame, start_point_u, end_point_u, (0,0,255), 8)
    #cv.rectangle(frame,(575,255),(755,285),(0,0,255),3)

    #_line_bot
    #cv.line(object.frame, start_point_b, end_point_b, (255,0,), 8)
    #cv.rectangle(frame,(575,390),(755,420),(255,0,0),3)
    
    #cv.imshow("croped",cropped_img)
    cv.imshow("CV",frame)

# Visualization flag
DEBUG = True 

# fps timer
loop_time = time.time()

while (True): 
    ### Main operations happen here 
    # if None, go next loop 
    if wincap.screenshot is None: 
        #print('no detected image') 
        continue 
  
    # Get the Screenshot of that window  
    ss=wincap.screenshot
    #ss = cv.resize(ss, (640, 640))
    
    # Update the frame for object detection
    object.update(ss)
    # To visualize the object_location:
    # -> mode=1 -> circle - person
    # -> mode=2 -> circle - tag
    # -> mode=3 (by default) -> rectangle - mixed 
    plot_obj()
    plot_obj(mode=1) # circle - person
    plot_obj(mode=2) # circle - tag
        
    

    try:
        main_fps = 1 / (time.time() - loop_time)
        
    except Exception as e: # ZeroDivisionError
        #print(f"Error in run method: {e}")
        pass

    # display image to debug/visualize
    if DEBUG:
        display(ss)
        
    key = cv.waitKey(1)

    loop_time=time.time()

    if key==ord('q'):

        wincap.stop()
        object.stop()
    

        if DEBUG:
            cv.destroyAllWindows()

        break

print("done")

