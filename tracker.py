import math

import cv2 as cv

class Tracker:

    '''    
    # boundary boxes: x,y,w,h
    bbox_up = [575,255,180,30] 
    bbox_down = [575,390,180,30]

    counter = 0

    down={}
    up={}
    '''
    
    def __init__(self,y_thres_u=None,y_thres_b=None):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

        self.dist_threshold = 0

        #self.y_thres_u = y_thres_u
        #self.y_thres_b = y_thres_b

    def update(self, objects_rect,thres):
        self.dist_threshold = thres
        if objects_rect == []:
            #print('empty objects')
            return objects_rect
        objects_bbs_ids = []
        # Get center point of new object 
        for rect in objects_rect:
            x1, y1, x2, y2, c, d = rect
            #print(d)
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                if dist > self.dist_threshold:
                    #print(dist, 'CCC')   # For tuning and debug
                    pass

                # Check if the distance is within the threshold
                if dist < self.dist_threshold:
                    #print(dist, 'BBB')
                    self.center_points[id] = (cx, cy)
                    objects_bbs_ids.append([cx, cy, c, d, id])
                    same_object_detected = True
                    break

            # New object is detected, assign a new ID to it
            if not same_object_detected:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([cx, cy, c, d, self.id_count])
                self.id_count += 1
                #print('ABC')
            
            #print(self.id_count)
        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        #print(self.center_points)
        
        return objects_bbs_ids 


'''
    def within_box(self,pt,rect):
        if rect[0] <= pt[0] <= rect[0] + rect[2] and rect[1] <= pt[1] <= rect[1] + rect[3]:
            return True
        else:
            return False

    def count(self, objs):
        # draw rect box 
        # as the point cx,cy locate in between the the box, counter chg
        # [cx, cy, c, d, self.id_count]
        for obj in objs:
            cx, cy, _, _, id = obj
            centre_points = (cx, cy)

            if self.within_box(centre_points, self.bbox_up):
                print('heree')
                if not self.flag:
                    self.flag = True
                    self.counter += 1
                    print('up?')
                    continue
            if self.within_box(centre_points, self.bbox_down):
                print('heree haha')
                if self.flag:
                    continue
                print('down?')
                self.flag = False
                self.counter -= 1

        return self.counter
    '''
