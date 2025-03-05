from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import os
import mediapipe as mp
from twilio.rest import Client  # Twilio for SMS
import logging

app = Flask(__name__)

# Set up directory for storing uploaded images
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize OpenCV VideoCapture
camera = cv2.VideoCapture(0)

# Initialize Mediapipe Face Detection Model
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TO_PHONE_NUMBER = os.getenv("TO_PHONE_NUMBER")  # Add this if needed

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)


# Test Twilio SMS on startup
def test_twilio_sms():
    """Sends a test SMS on startup to verify Twilio integration."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        message = client.messages.create(
            body="⚠️ ALERT: Unknown face detected!",
            from_=TWILIO_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
        logging.info(f"Twilio Test SMS Sent: {message.sid}")
    except Exception as e:
        logging.error(f"Twilio Test SMS Error: {e}")


# Run Twilio SMS Test on Startup
test_twilio_sms()


# Function to send SMS alert using Twilio
def send_alert(phone_number, message):
    """Sends an SMS alert using Twilio."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number  # Ensure number includes country code (e.g., +91 for India)
        )
        logging.info(f"Twilio Alert SMS Sent: {msg.sid}")
        return {"status": "success", "message_sid": msg.sid}
    except Exception as e:
        logging.error(f"Twilio SMS Error: {e}")
        return {"status": "error", "error": str(e)}


# Function to generate frames with face detection using Mediapipe
def generate_frames():
    """Generates video frames with face detection and bounding box labeling."""
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            h, w, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(rgb_frame)

            if results.detections:
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    x, y, w_box, h_box = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
                    
                    # Draw bounding box
                    cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)

                    # Label "Unknown"
                    label = "Unknown"
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    """Renders the homepage with the latest uploaded image."""
    uploaded_image = None
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if files:
        uploaded_image = url_for('static', filename=f'uploads/{files[0]}')
    return render_template('index.html', uploaded_image=uploaded_image)


@app.route('/video_feed')
def video_feed():
    """Provides video stream with face detection."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/upload', methods=['POST'])
def upload():
    """Handles image uploads."""
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

    return redirect(url_for('index'))


@app.route('/set_phone', methods=['POST'])
def set_phone():
    """Receives phone number and sends an alert SMS."""
    phone_number = request.form.get('phone')
    if phone_number:
        message = "Alert! An unknown face has been detected."
        send_alert(phone_number, message)
    return redirect(url_for('index'))


@app.route('/shutdown', methods=['GET'])
def shutdown():
    """Releases camera resources before shutting down the Flask app."""
    global camera
    if camera.isOpened():
        camera.release()
    return "Camera released. Server shutting down."


if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        if camera.isOpened():
            camera.release()  # Ensure camera is released when the app stops
