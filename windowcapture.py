import win32gui
import win32ui
import win32con
import numpy as np
import time
from threading import Thread, Lock
import ctypes
from ctypes import windll

class WindowCapture:
    # Add Threading Properties
    stopped = True
    lock = None
    screenshot = None

    fps = 0
    frame_count = 0
    start_time = 0 
    
    #properties
    #initialize
    w = 0  
    h = 0
    hwnd = None

    def __init__(self, window_name=None):
        # create a thread lock object
        self.lock = Lock()
        self.window_name = window_name

        try:
            # Windows 10 and later
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
        except AttributeError:
            try:
                # Windows 8.1 and earlier
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception as e:
                print("Failed to set DPI awareness:", e)
        
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        
        #find the window
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        #define the monitor width and height
        #self.w=1920
        #self.h=1080

        #get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        print(window_rect)
        #(left,top,right,bottom)
        self.w = window_rect[2]-window_rect[0]
        self.h = window_rect[3]-window_rect[1]
        #print(self.w)
        #print(self.h)
        
        #remove the window_border
        #border_pixels=13
        #titlebar_pixels=47
        border_pixels = 5
        titlebar_pixels = 10
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels

        self.start_time = time.time()

    def track_window(self):
        try:
            self.hwnd = win32gui.FindWindow(None, self.window_name)
            
            if not self.hwnd:
                return True
            
            return False
        
        except Exception as e:
            return True
            #print ('Window not found: {}'.format(self.window_name))
        
    def get_screenshot(self):

        #bmpfilenamename = "out.bmp" #set this
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        
        # this line make the ss available on certain windows
        result = windll.user32.PrintWindow(self.hwnd, cDC.GetSafeHdc(), 3)

        #save
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')

        #for more speed
        bmpstr = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(bmpstr,dtype=np.uint8)
        img.shape = (self.h,self.w,4)
        '''
        if not result:
            # Free Resources
            win32gui.DeleteObject(dataBitMap.GetHandle())
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, wDC)
            raise RuntimeError(f"Unable to acquire screenshot! Result: {result}")
        '''
        win32gui.DeleteObject(dataBitMap.GetHandle())
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        
        #drop the alpha channel
        img = img[...,:3]
        img = np.ascontiguousarray(img)

        return img

    #get name of windows
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd,ctx):
            if win32gui.IsWindowVisible(hwnd):
                print (hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows( winEnumHandler, None )
    
    # threading methods

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            try:
                # Measure FPS
                self.frame_count += 1
                if self.frame_count % 5 == 0:  # Calculate FPS every 10 frames
                    elapsed_time = time.time() - self.start_time
                    self.fps = self.frame_count / elapsed_time
                    self.frame_count = 0
                    self.start_time = time.time()
                    #print(f'Screenshot Capture fps: {self.fps:.1f}')

                screenshot = self.get_screenshot()
                self.lock.acquire()
                self.screenshot = screenshot
                self.lock.release()
                time.sleep(0.01)
            except Exception as e:
                print(f"Error in run method: {e}")
