# By Yang Lin
# Example loads youtube video, run it against yolo5 model from pytorch
# Show bounding box, name, and confidence
# Stop playing when atleast 4 people are detected in frame with confidence greater than threshold = 50%

import cv2
import pafy
import numpy as np
import torch
import torch.backends.cudnn as cudnn

url = 'https://www.youtube.com/watch?v=8YjFbMbfXaQ'
video = pafy.new(url)
best = video.getbest(preftype="mp4")
capture = cv2.VideoCapture(best.url)

model = torch.hub.load("ultralytics/yolov5", "yolov5s", force_reload=True)
cudnn.benchmark = True

while True:
    isTrue, frame = capture.read()
    if not isTrue:
        break

    results = model(frame, size=1080)
    bounding_boxes = results.pandas().xyxy[0]
    bounding_boxes_json = bounding_boxes.to_json(orient="records")

    num_of_people = 0
    threshold = .5

    for index, bounding_box in bounding_boxes.iterrows():

        if bounding_box['name'] == 'person' and bounding_box['confidence'] >= threshold:
            num_of_people += 1

        # bounding box
        cv2.rectangle(frame, (int(bounding_box['xmin']), int(bounding_box['ymin'])), 
            (int(bounding_box['xmax']), int(bounding_box['ymax'])), (0, 255, 0), 1)
        
        text = ' ' + bounding_box['name'] + ' ' + str(int(bounding_box['confidence'] * 100)) + '% '

        # put background behind label
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(frame, (int(bounding_box['xmin']), int(bounding_box['ymin']) - 20), 
            (int(bounding_box['xmin']) + text_width, int(bounding_box['ymin'])), (0, 255, 0), cv2.FILLED)

        # label and confidence above bounding box
        cv2.putText(frame, text, (int(bounding_box['xmin']), 
            int(bounding_box['ymin']) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    if num_of_people > 3:
        cv2.putText(frame, 'Detected 4 people!', (0,0), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 0), 1)
        cv2.imshow('Video', frame)
        if cv2.waitKey(0) & 0xFF == ord('n'):
            break
    else:
        cv2.imshow('Video', frame)

    if cv2.waitKey(33) & 0xFF == ord('d'):
        break
    
capture.release()
cv2.destroyAllWindows()
