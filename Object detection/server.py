# from flask import Flask, request
# import numpy as np
# import cv2
# from flask import Flask, render_template, Response
# import numpy as np
# import time
# # import cv2
# import os
# import imutils
# import subprocess
# from gtts import gTTS
# from pydub import AudioSegment
# import imageio as iio

# LABELS = open("yolo-coco/coco.names").read().strip().split("\n")
# print("[INFO] loading YOLO from disk...")
# net = cv2.dnn.readNetFromDarknet("yolo-coco/yolov3.cfg", "yolo-coco/yolov3.weights")
# ln = net.getLayerNames()
# ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
# frame_count = 0
# start = time.time()
# first = True
# frames = []
# app = Flask(__name__)
# # received_image = None
# def gen_frames(received_image):
    

#     while True:

#         # print("hello")
#         if received_image is not None:
#             frame=received_image

        
#             # key = cv2.waitKey(1)
#             # if frame_count % 60 == 0:
#             #     end = time.time()
#                 # grab the frame dimensions and convert it to a blob
#             (H, W) = frame.shape[:2]
#                 # construct a blob from the input image and then perform a forward
#                 # pass of the YOLO object detector, giving us our bounding boxes and
#                 # associated probabilities
#             blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
#                                              swapRB=True, crop=False)
#             net.setInput(blob)
#             layerOutputs = net.forward(ln)

#                 # initialize our lists of detected bounding boxes, confidences, and
#                 # class IDs, respectively
#             boxes = []
#             confidences = []
#             classIDs = []
#             centers = []

#                 # loop over each of the layer outputs
#             for output in layerOutputs:
#                 # loop over each of the detections
#                 for detection in output:
#                     # extract the class ID and confidence (i.e., probability) of
#                     # the current object detection
#                     scores = detection[5:]
#                     classID = np.argmax(scores)
#                     confidence = scores[classID]
#                     # filter out weak predictions by ensuring the detected
#                     # probability is greater than the minimum probability
#                     if confidence > 0.5:
#                         # scale the bounding box coordinates back relative to the
#                         # size of the image, keeping in mind that YOLO actually
#                         # returns the center (x, y)-coordinates of the bounding
#                         # box followed by the boxes' width and height
#                         box = detection[0:4] * np.array([W, H, W, H])
#                         (centerX, centerY, width, height) = box.astype("int")

#                         # use the center (x, y)-coordinates to derive the top and
#                         # and left corner of the bounding box
#                         x = int(centerX - (width / 2))
#                         y = int(centerY - (height / 2))

#                         # update our list of bounding box coordinates, confidences,
#                         # and class IDs
#                         boxes.append([x, y, int(width), int(height)])
#                         confidences.append(float(confidence))
#                         classIDs.append(classID)
#                         centers.append((centerX, centerY))

#                 # apply non-maxima suppression to suppress weak, overlapping bounding
#                 # boxes
#             idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
#             texts = []
#             # ensure at least one detection exists
#             if len(idxs) > 0:
#                 # loop over the indexes we are keeping
#                 for i in idxs.flatten():
#                     # find positions
#                     centerX, centerY = centers[i][0], centers[i][1]
#                     if centerX <= W / 3:
#                         W_pos = "left "
#                     elif centerX <= (W / 3 * 2):
#                         W_pos = "center "
#                     else:
#                         W_pos = "right "
#                     if centerY <= H / 3:
#                         H_pos = "top "
#                     elif centerY <= (H / 3 * 2):
#                         H_pos = "mid "
#                     else:
#                         H_pos = "bottom "
#                     texts.append(H_pos + W_pos + LABELS[classIDs[i]])
#             print(texts)
#             if texts:
#                 description = ', '.join(texts)
#                 tts = gTTS(description, lang='en', tld="com")
#                 tts.save('tts.mp3')
#                 tts = AudioSegment.from_mp3("tts.mp3")
#                 subprocess.call(["ffplay", "-nodisp", "-autoexit", "tts.mp3"])
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
# @app.route('/upload', methods=['POST'])
# def upload():
#     try:
#         # Receive the image data
#         image_data = request.data
        
#         # Decode the image
        
#         received_image = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)
#         video_feed(received_image)
#         # Process the image as needed (e.g., save to disk, perform analysis, etc.)
#         # Example: save the received frames to a file
#         # cv2.imwrite('received_frame.jpg', image)

#         return "Received and processed image successfully"
#     except Exception as e:
#         return str(e), 500


# @app.route('/video_feed')
# def video_feed(received_image):
#     return Response(gen_frames(received_image), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__=='__main__':
#     app.run(debug=True,host='127.0.0.1')


from flask import Flask, request,jsonify
from flask import send_file

import numpy as np
import cv2
# import subprocess
# from gtts import gTTS
# from pydub import AudioSegment
# from flask import Flask, request
# import numpy as np
# import cv2
from flask import Flask, render_template, Response
from flask_cors import CORS
# import numpy as np
# import time
# # import cv2
# import os
# import imutils
# import subprocess
from gtts import gTTS
# from pydub import AudioSegment
# import imageio as iio
LABELS = open("yolo-coco/coco.names").read().strip().split("\n")
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet("yolo-coco/yolov3.cfg", "yolo-coco/yolov3.weights")
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

app = Flask(__name__)
CORS(app)
text_data=[]
@app.route('/get_text', methods=['GET'])
def get_text_data():
    global text_data
    return jsonify(text_data)
def process_image(image_data):
    global text_data
    try:
        # Decode the image
        received_image = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Process the received image
        frame = received_image
        (H, W) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)

        boxes = []
        confidences = []
        classIDs = []
        centers = []

                # loop over each of the layer outputs
        for output in layerOutputs:
                # loop over each of the detections
            for detection in output:
                    # extract the class ID and confidence (i.e., probability) of
                    # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                    # filter out weak predictions by ensuring the detected
                    # probability is greater than the minimum probability
                if confidence > 0.5:
                        # scale the bounding box coordinates back relative to the
                        # size of the image, keeping in mind that YOLO actually
                        # returns the center (x, y)-coordinates of the bounding
                        # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                        # use the center (x, y)-coordinates to derive the top and
                        # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
                    centers.append((centerX, centerY))

                # apply non-maxima suppression to suppress weak, overlapping bounding
                # boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
        texts = []
            # ensure at least one detection exists
        if len(idxs) > 0:
                # loop over the indexes we are keeping
            for i in idxs.flatten():
                    # find positions
                centerX, centerY = centers[i][0], centers[i][1]
                if centerX <= W / 3:
                    W_pos = "left "
                elif centerX <= (W / 3 * 2):
                    W_pos = "center "
                else:
                    W_pos = "right "
                if centerY <= H / 3:
                    H_pos = "top "
                elif centerY <= (H / 3 * 2):
                    H_pos = "mid "
                else:
                    H_pos = "bottom "
                texts.append(H_pos + W_pos + LABELS[classIDs[i]])
        print(texts)
        text_data=texts
        if texts:
            description = ', '.join(texts)
            tts = gTTS(description, lang='en', tld="com")
           
            # tts.save('static/tts.mp3')
            # tts = AudioSegment.from_mp3("static/tts.mp3")
            # subprocess.call(["ffplay", "-nodisp", "-autoexit", "static/tts.mp3"])
            
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        return 'success'
    except Exception as e:
        return str(e), 500
# print('hi',text1)

@app.route('/process_image', methods=['POST'])
def process_image_route():
    
    try:
        # Receive the image data
        image_data = request.data
        text1 = process_image(image_data)
        
        return text1

        
    except Exception as e:
        return str(e), 500



if __name__ == '__main__':
    app.run(debug=True)
