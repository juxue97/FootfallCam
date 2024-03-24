import ultralytics
print(ultralytics.__version__)

from threading import Thread, Lock
from tracker import Tracker

import cv2
import pandas as pd
from ultralytics import YOLO

class Model:
    # Add Threading Properties
    stopped = True
    lock = None
    coor_person = []
    coor_tag = []
    rect=[]

    # model properties
    model=None
    count=0
    tracker=None

    class_list = ['person','tag']

    #processing properties
    frame=None

    #calculate properties
    confidence_threshold = 0.25
    cx=0
    cy=0
    w_r = 450
    w_l = 950

    y_line_u = 275
    y_line_b = 400

    counter = 0

    def __init__(self,frame):
        # create a thread lock object
        self.lock = Lock()

        self.model=YOLO('best_2.pt')
        self.frame=frame
        self.tracker = Tracker()

    def read_frame(self, frame):
        if frame is not None:
            roi = frame[:, self.w_r:self.w_l]
            gray_image = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            preprocessed_img = cv2.merge([gray_image] * 3)
            #cv2.imshow("preproc",preprocessed_img)
            #cv2.waitKey(1)
            results = self.model.predict(preprocessed_img,verbose=False)
            a=results[0].boxes.data
            a = a.detach().cpu().numpy()  # added this line
            px = pd.DataFrame(a).astype("float")
            #print(px)

            # Extract bounding box information
            bbox_list_person = []
            bbox_list_tag =[]
            rectangles = []
            for index, row in px.iterrows():
                x1=int(row[0])
                y1=int(row[1])
                x2=int(row[2])
                y2=int(row[3])
                c=float(row[4])
                d=int(row[5])
                id=self.class_list[int(d)]

                if c >= self.confidence_threshold:
                    format_c = f'{c:.2f}'
                    x1, y1, x2, y2 = self.w_r+int(x1), int(y1), self.w_r+int(x2), int(y2)

                    rectangles.append([x1, y1, x2, y2, format_c, id])
                    if id == 'person':
                        #print(d)
                        bbox_list_person.append([x1, y1, x2, y2, format_c, id])
                        
                    elif id == 'tag':
                        bbox_list_tag.append([x1, y1, x2, y2, format_c, id])


            objs_person = self.tracker.update(bbox_list_person,620)
            #objs_person=[] # for debugging
            objs_tag = self.tracker.update(bbox_list_tag,150)
            #objs_tag=[]    # for debugging
            #print('did i came here')
            
            return objs_person,objs_tag,rectangles
    '''
    def extract(self, px):
        # Extract bounding box information
        bbox_list = []
        rectangle_points =[]
        for index, row in px.iterrows():
            if row[4] >= self.confidence_threshold:
                x1, y1, x2, y2, c, id = row
                format_c = f'{c:.2f}'
                d=self.class_list[int(id)]
                x1, y1, x2, y2 = self.w_r+int(x1), int(y1), self.w_r+int(x2), int(y2)
                #cv2.rectangle(self.frame , (x1, y1), (x2, y2), (0, 255, 0), 2)
                #cv2.putText(self.frame , f'{d}: {format_c}', (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

                rectangle_points.append([x1, y1, x2, y2, format_c, d])
                bbox_list.append([x1, y1, x2, y2, format_c, d])

        objs = self.tracker.update(bbox_list)

        return objs,rectangle_points
    '''
    # threading methods
            
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def update(self,frame):
        with self.lock:
            self.frame = frame

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            try:
                if not self.frame is None:

                    p,t,rect = self.read_frame(self.frame)
                    self.lock.acquire()
                    self.coor_person,self.coor_tag,self.rect = p,t,rect
                    self.lock.release()
                        
                            
          
            except Exception as e:
                print(f"Error in run method: {e}")     


    