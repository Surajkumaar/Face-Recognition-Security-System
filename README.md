# 🔒 Face Recognition Security System
___
## 📌 Overview

This is a **Flask-based face detection security system** that uses **Mediapipe** for face recognition and **Twilio** for SMS alerts. It detects faces in real-time and sends an alert SMS when an unknown face is detected.

## 🚀 Features

✅ **Live Face Detection** using **Mediapipe**  
✅ **Real-time Video Streaming** with Flask  
✅ **SMS Alerts** via **Twilio** (for unknown faces)  
✅ **Image Upload Support**  
✅ **Web-based Interface**

---

## 📥 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/Face-Recognition-Security-System.git
cd Face-Recognition-Security-System
```

Replace `yourusername` with your actual GitHub username if you’re hosting the repository.

---

### 2️⃣ Create and Activate Virtual Environment

```bash
# Create a virtual environment named "myenv"
python -m venv myenv

# Activate virtual environment (Windows)
myenv\Scripts\activate

# Activate virtual environment (Linux/macOS)
source myenv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install dependencies manually:

```bash
pip install flask opencv-python mediapipe twilio
```

---

## 🎯 Usage

### 🚀 1. Start the Flask Application

Run the following command:

```bash
python app1.py
```

The application will start, and you can access it in your browser at:

```
http://127.0.0.1:5000
```

---

### 📩 2. Configure Twilio (For SMS Alerts)

Set up **Twilio credentials** as environment variables:

For Linux/macOS:

```bash
export TWILIO_ACCOUNT_SID="your_account_sid"
export TWILIO_AUTH_TOKEN="your_auth_token"
export TWILIO_PHONE_NUMBER="your_twilio_number"
```

For Windows (PowerShell):

```bash
$env:TWILIO_ACCOUNT_SID="your_account_sid"
$env:TWILIO_AUTH_TOKEN="your_auth_token"
$env:TWILIO_PHONE_NUMBER="your_twilio_number"
```

Replace `"your_account_sid"`, `"your_auth_token"`, and `"your_twilio_number"` with your actual Twilio details.

---

## 🔧 Project Structure

```bash
Face-Recognition-Security-System/
│── static/                # Contains uploaded images
│── templates/             # HTML templates for web interface
│── app1.py                # Main Flask application
│── requirements.txt       # Python dependencies
│── README.md              # Project documentation
```

---

## 📌 Key Functions in `app1.py`

- **Face Detection**: Uses **Mediapipe** to detect faces in real-time.
- **SMS Alerts**: Sends an **alert SMS** when an unknown face is detected.
- **Web Interface**: Provides a simple **Flask-based web UI** to view the camera feed.
- **Image Upload**: Allows users to upload images.

---

## 🛑 Stopping the App

To **release the camera** and stop the server, visit:

```
http://127.0.0.1:5000/shutdown
```

Or press **Ctrl + C** in the terminal.

---

## 📝 Notes

- Make sure your **webcam** is connected.
- Twilio **requires a verified phone number** for testing.
- Works on **Windows, Linux, and macOS**.

---

## 🤝 Contributing

Feel free to fork this repository, make improvements, and submit a pull request!

---

## 📜 License

This project is licensed under the **MIT License**.

---

This `README.md` is now **fully complete** and follows proper bash syntax formatting! 🚀