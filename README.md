# FootfallCam
1. Title: Object Detection using YOLO_V8 Model
- dataset link (https://drive.google.com/file/d/1V3nug3Ofc08mPy7OElWfil_twr1k1hp7/view?usp=sharing)
    
***
2. Data Collection/Generation (code link : https://colab.research.google.com/drive/1N5t2dPxPgk_TX3zrzc0LMlEU7-4TA3bg)
- Data is labelled using free tools on Roboflow platform
- Besides, the dataset is set to undergoes some image preprocessing steps, such as Auto-orient, static crop, resize, grayscale, gaussian blur.
- Data augmentation is then performed (1215 -> 3043)
- Example of the label image:
<img src="https://github.com/juxue97/FootfallCam/assets/122148337/00aa6788-0649-4bba-a124-77bd3101a75e" alt="label_image" width="300" height="200">

***
3. Model Training (code link : https://colab.research.google.com/drive/1wi18CjorSLyqkAPOuL-7G7L0tA2cyH4K)
-  Pretrained Ultralytics Yolo-V8 model is selected for this project
-  Some of the model performance metrics and information after training is completed:    
      - training batch image & label information
    
    <img src="https://github.com/juxue97/FootfallCam/assets/122148337/cd64824f-ddee-4649-b34f-2e827187ccbb" alt="training_batch" width="300" height="200"> <img src="https://github.com/juxue97/FootfallCam/assets/122148337/41a8ff2d-59fd-42d6-9c50-541cd3dd1b83" alt="labels" width="300" height="200">
   
      - confusion matrix & f1-confidence curve
    
    <img src="https://github.com/juxue97/FootfallCam/assets/122148337/16f10950-08ab-4c50-920e-0ca7a2ab8236" alt="confusion_matrix" width="300" height="200"> <img src="https://github.com/juxue97/FootfallCam/assets/122148337/1bba81bb-9bfa-4bc0-9b51-36d1f2fded19" alt="f1_curve" width="300" height="200">
   

***
4. Deploy
- Adjust the code in main.py for different visualization types. (Set DEBUG=TRUE and look for plot_obj() in the main loop)
  
  <img src="https://github.com/juxue97/FootfallCam/assets/122148337/ac5ba515-f9da-495d-9e96-1b43ffc919e2" alt="plot_obj" width="300" height="200">   


***
5. Results: 
    - Mode = 3 (default) [rectangle]
      
      <img src="https://github.com/juxue97/FootfallCam/assets/122148337/48abb414-bea2-4dd7-9c5b-4c0050a89c32" alt="Description of your image" width="300" height="200">

    - Mode = 1 & 2 [circle]
      
      <img src="https://github.com/juxue97/FootfallCam/assets/122148337/38307d48-75f7-41a4-9d26-07c2a2882f78" alt="Description of your image" width="300" height="200">

***





