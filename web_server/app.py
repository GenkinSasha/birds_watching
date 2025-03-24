from flask import Flask, render_template, Response
import cv2
import os

app = Flask(__name__)

# Set your IP camera URL (Replace with your actual IP camera URL)
IP_CAMERA_URL = "rtsp://10.0.0.6:10554/udp/av0_0"

# Check if the IP camera is available
def is_camera_available():
    cap = cv2.VideoCapture(IP_CAMERA_URL)
    if cap.isOpened():
        cap.release()
        return True
    return False

# Generate video frames
def generate_frames():
    cap = cv2.VideoCapture(IP_CAMERA_URL)
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cap.release()

@app.route('/')
def index():
    if is_camera_available():
        return render_template('index.html', camera_available=True)
    else:
        return render_template('index.html', camera_available=False)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/about')
def about():
    return '<h1>About Page</h1><p>This is a simple Flask web app.</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
