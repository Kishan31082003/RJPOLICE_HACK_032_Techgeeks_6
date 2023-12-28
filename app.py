from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)

# Loading YOLOv3 Model
LABELS = open("yolo-coco/coco.names").read().strip().split("\n")
net = cv2.dnn.readNetFromDarknet("yolo-coco/yolov3.cfg", "yolo-coco/yolov3.weights")
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect_objects', methods=['POST'])
def detect_objects():
    data = request.get_json()
    frame_data = data['frameData']

    # Decode base64 frame data
    frame_bytes = base64.b64decode(frame_data)
    frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

    # YOLO object detection
    (H, W) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > 0.5:
                box = detection[0:4] * np.array([W, H, W, H])
                (x, y, width, height) = box.astype("int")
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

    # Process the detected objects
    detected_objects = []
    if len(idxs) > 0:
        for i in idxs.flatten():
            detected_objects.append(LABELS[classIDs[i]])

    return jsonify(detected_objects)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
