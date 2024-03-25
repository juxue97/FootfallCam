# FootfallCam
1. Title: Object Detection using YOLO_V8 Model
- dataset link (https://drive.google.com/file/d/1V3nug3Ofc08mPy7OElWfil_twr1k1hp7/view?usp=sharing)

1. Data Collection/Generation (code link : https://colab.research.google.com/drive/1N5t2dPxPgk_TX3zrzc0LMlEU7-4TA3bg)
- Data was labelled using free tools on Roboflow platform
- Besides, the dataset was set to undergoes some image preprocessing steps, such as Auto-orient, static crop, resize, grayscale, gaussian blur.
- Data augmentation was then performed (1215 -> 3043)
Example of the preprocessed image: 0: person, 1: tag
<img src="https://github.com/juxue97/FootfallCam/assets/122148337/ea13772a-2401-4ff8-9ee8-df4b6de3b216" alt="Description of your image" width="300" height="200">





3. Model Training (code link : https://colab.research.google.com/drive/1wi18CjorSLyqkAPOuL-7G7L0tA2cyH4K)

Adjust the mode for different visualization types.
Results: 
- Mode = 3 (default) [rectangle]
<img src="https://github.com/juxue97/FootfallCam/assets/122148337/48abb414-bea2-4dd7-9c5b-4c0050a89c32" alt="Description of your image" width="300" height="200">

- Mode = 1 & 2 [circle]
<img src="https://github.com/juxue97/FootfallCam/assets/122148337/38307d48-75f7-41a4-9d26-07c2a2882f78" alt="Description of your image" width="300" height="200">





