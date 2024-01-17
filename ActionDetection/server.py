# predict_code_flask.py
from flask import Flask, render_template, Response
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from collections import deque
from moviepy.editor import VideoFileClip
from flask import Flask, render_template, Response
import numpy as np
import time
import cv2
import os
import imutils
import subprocess
from gtts import gTTS
from pydub import AudioSegment
from twilio.rest import Client

# Twilio account SID, Auth Token, and Twilio phone number
account_sid = 'AC659a709460c9b655a97ecfdceabc02bd'
auth_token = '053234457ea222b57258778cfb3d601c'
twilio_phone_number = '+15034069206'

# Create a Twilio client
client = Client(account_sid, auth_token)

def send_sms(to, message):
    try:
        # Send the SMS
        message = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=to
        )
        print(f"SMS sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")



LABELS = open("yolo-coco/coco.names").read().strip().split("\n")

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet("yolo-coco/yolov3.cfg", "yolo-coco/yolov3.weights")

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
app = Flask(__name__)
# initialize
cap = cv2.VideoCapture(0)
frame_count = 0
start = time.time()
first = True
frames = []
sms_out=1
# Load the pre-trained model.
LRCN_model = load_model('LRCN_model___Date_Time_2024_01_17__14_15_40___Loss_1.1685377359390259___Accuracy_0.3499999940395355.h5')
CLASSES_LIST = ["Fight", "Vandalism", "burglary"]

# Specify the sequence length for prediction.
SEQUENCE_LENGTH = 20

# Function for prediction
IMAGE_HEIGHT, IMAGE_WIDTH = 64, 64
frames_queue = deque(maxlen=SEQUENCE_LENGTH)

# Define video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can try other codecs as well
output_video_file = 'output.avi'
out = None

def predict_on_video(frame):
    # Resize the Frame to fixed Dimensions.
    resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))

    # Normalize the resized frame by dividing it with 255 so that each pixel value then lies between 0 and 1.
    normalized_frame = resized_frame / 255

    # Appending the pre-processed frame into the frames list.
    frames_queue.append(normalized_frame)

    # Check if the number of frames in the queue are equal to the fixed sequence length.
    if len(frames_queue) == SEQUENCE_LENGTH:
        # Pass the normalized frames to the model and get the predicted probabilities.
        predicted_labels_probabilities = LRCN_model.predict(np.expand_dims(frames_queue, axis=0))[0]

        # Get the index of class with highest probability.
        predicted_label = np.argmax(predicted_labels_probabilities)

        # Get the class name using the retrieved index.
        predicted_class_name = CLASSES_LIST[predicted_label]
        return predicted_class_name

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    global sms_out
    global out  # Use the global video writer variable
    global frame_count
    global start
    global output_video_file
    video_capture = cv2.VideoCapture(0)
    while True:
        success, frame = video_capture.read()
        if not success:
            break

        # Get the predicted action
        predicted_action = predict_on_video(frame)
        print(predicted_action)

        if predicted_action in CLASSES_LIST and sms_out==1:
            recipient_number = '+916266114341'  # Replace with the recipient's phone number
            sms_message = f"Subject: Urgent: Info on Durga Nagar, Vidisha Address: Durga Nagar, Vidisha CCTV: [CCTV No.454] Electricity Line: 260543Crucial info available through CCTV and power line might aid ongoing investigations. Your swift attention to this matter is pivotal for community safety.information is related to {predicted_action}"
            send_sms(recipient_number, sms_message)
            sms_out=0


        # Write predicted class name on top of the frame.
        cv2.putText(frame, predicted_action, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Convert the frame to JPEG format for streaming.

        if out is None:
            out = cv2.VideoWriter(output_video_file, fourcc, 20.0, (640, 480))
        
        # Save the frame to the video file
        out.write(frame)

        
        key = cv2.waitKey(1)
        if frame_count % 60 == 0:
            end = time.time()
            # grab the frame dimensions and convert it to a blob
            (H, W) = frame.shape[:2]
            # construct a blob from the input image and then perform a forward
            # pass of the YOLO object detector, giving us our bounding boxes and
            # associated probabilities
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                            swapRB=True, crop=False)
            net.setInput(blob)
            layerOutputs = net.forward(ln)

            # initialize our lists of detected bounding boxes, confidences, and
            # class IDs, respectively
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

            if texts:
                description = ', '.join(texts)
                tts = gTTS(description, lang='en', tld="com")
                tts.save('tts.mp3')
                tts = AudioSegment.from_mp3("tts.mp3")
                subprocess.call(["ffplay", "-nodisp", "-autoexit", "tts.mp3"])

            # ret, buffer = cv2.imencode('.jpg', frame)
            # frame = buffer.tobytes()
            # yield (b'--frame\r\n'
            #         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
        
        if time.time() - start > 60:  # Change this value based on your needs
            out.release()
            frame_count = 0
            start = time.time()
            output_video_file = f'output_{int(start)}.avi'
            out = None
    video_capture.release()
    if out is not None:
        out.release()

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
