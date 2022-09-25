import datetime
from random import random
import os
import io
from io import BytesIO
import random
import time
import cv2
import numpy as np
from flask import Flask, Response, make_response, send_file, jsonify
from flask_cors import CORS, cross_origin
import requests
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import logging

# Initialize the Flask app
app = Flask(__name__)
CORS(app, support_credentials=True)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' 
for local webcam use cv2.VideoCapture(0)
'''

class_path = "models/coco.names"
weightsPath = "models/yolov4.weights"
configPath = "models/yolov4.cfg"
object_detected = False
data = None
SavePath = ""


def send_telegram(text: str, name, conf):
    token = ""  # your token
    url = "https://api.telegram.org/bot"
    channel_id = ""  # channel_id
    url += token
    method = url + "/sendMessage"

    try:
        r = requests.post(method, data={
            "chat_id": channel_id,
            "text": text + " " + name + " " + str(conf)
        })

    except:
        print("post_text error")


net = cv2.dnn_DetectionModel(configPath, weightsPath)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
input_size = 416
net.setInputSize(input_size, input_size)
net.setInputScale(1.0 / 255)
net.setInputSwapRB(True)
with open(class_path, 'r') as f:
    names = [line.strip() for line in f.readlines()]
COLORS = np.random.uniform(0, 255, size=(len(names), 3))


def stream_inf():
    """ Method to run inference on a stream. """
    global object_detected
    global data
    source = cv2.VideoCapture(0)

    b = random.randint(0, 255)
    g = random.randint(0, 255)
    r = random.randint(0, 255)

    while source.isOpened():
        ret, frame = source.read()
        if ret:
            timer = time.time()
            classes, confidences, boxes = net.detect(frame, confThreshold=0.1, nmsThreshold=0.4)
            print('[Info] Time Taken: {} | FPS: {}'.format(time.time() - timer, 1 / (time.time() - timer)),
                  end='\r')

            if not len(classes) == 0:
                for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
                    label = '%s: %.2f' % (names[classId], confidence)
                    left, top, width, height = box
                    b = random.randint(0, 255)
                    g = random.randint(0, 255)
                    r = random.randint(0, 255)
                    cv2.rectangle(frame, box, color=(b, g, r), thickness=2)
                    cv2.rectangle(frame, (left, top), (left + len(label) * 20, top - 30), (b, g, r), cv2.FILLED)
                    cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_COMPLEX, 1, (255 - b, 255 - g, 255 - r),
                                1, cv2.LINE_AA)
                    cv2.putText(frame, f"FPS: {str(round(1 / (time.time() - timer)))} ", (40, 35),
                                cv2.FONT_HERSHEY_DUPLEX, 0.8, (186, 74, 82), 1, lineType=cv2.LINE_AA)
                    send_telegram("object detected!", names[classId], confidence)
                    object_detected = True
                    a = str(datetime.datetime.now())
                    a = a.replace(':', '-')
                    # cv2.imwrite('%s/%s.jpg' % (SavePath, str(a)), frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            data = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def image_inf(image):
    """ Method to run inference on a image. """

    b = random.randint(0, 255)
    g = random.randint(0, 255)
    r = random.randint(0, 255)

    classes, confidences, boxes = net.detect(image, confThreshold=0.1, nmsThreshold=0.4)
    if not len(classes) == 0:
        for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
            label_img = '%s: %.2f' % (names[classId], confidence)
            left, top, width, height = box
            b = random.randint(0, 255)
            g = random.randint(0, 255)
            r = random.randint(0, 255)
            cv2.rectangle(image, box, color=(b, g, r), thickness=2)
            cv2.rectangle(image, (left, top), (left + len(label_img) * 20, top - 30), (b, g, r), cv2.FILLED)
            cv2.putText(image, label_img, (left, top), cv2.FONT_HERSHEY_COMPLEX, 1, (255 - b, 255 - g, 255 - r),
                        1, cv2.LINE_AA)

    ret, buffer = cv2.imencode('.jpg', image)
    frame = buffer.tobytes()
    return frame


@app.route('/video_feed')
def video_feed():
    return Response(stream_inf(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/image')
def get_image():
    global data
    return Response(data, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/detect')
def detect():
    global object_detected
    if object_detected:
        object_detected = False
        return {'detect': 1}
    else:
        return {'detect': 0}


@app.route('/upload', methods=['POST'])
def fileUpload():
    files = request.files
    file = files.get('file')
    f = file.stream.read()
    bin_data = io.BytesIO(f)
    file_bytes = np.asarray(bytearray(bin_data.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    prediction = image_inf(img)
    global data
    return Response(prediction, mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
