import speech_recognition as sr
import cv2
import sys
import subprocess
import os
import pyttsx3  # Text-to-Speech
import tkinter as tk
from tkinter import messagebox

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Change to different index based on your system
engine.setProperty("rate", 160)  # Adjust speed (default ~200)
engine.setProperty("volume", 1.0)  # Set volume

# Define the correct path to the objects.py script
OBJECTS_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "objects.py")

def speak(text):
    """Convert text to speech and speak it."""
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        root.update()
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        status_label.config(text=f"You said: {command}")
        root.update()
        speak(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        status_label.config(text="Sorry, I didn't catch that.")
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        status_label.config(text="Could not connect to speech recognition service.")
        speak("Could not connect to speech recognition service.")
        return ""

def open_camera():
    cap = cv2.VideoCapture(0)
    status_label.config(text="Camera opened. Say 'close camera' to close or 'stop' to exit.")
    speak("Camera opened. Say 'close camera' to close or 'stop' to exit the program.")
    root.update()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Camera", frame)
        
        command = listen_command()
        if "close camera" in command:
            break
        if "stop" in command:
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    status_label.config(text="Camera closed.")
    root.update()

def start_object_detection():
    if os.path.exists(OBJECTS_SCRIPT_PATH):
        status_label.config(text="Starting YOLO object detection...")
        speak("Starting YOLO object detection.")
        root.update()
        subprocess.run(["python", OBJECTS_SCRIPT_PATH])
    else:
        messagebox.showerror("Error", "objects.py not found!")
        speak("Error: objects.py not found.")

# GUI Setup
root = tk.Tk()
root.title("Voice-Controlled Assistant")
root.geometry("400x300")

status_label = tk.Label(root, text="Welcome! I am Zeel's Bot.", font=("Arial", 12), wraplength=350)
status_label.pack(pady=10)

btn_listen = tk.Button(root, text="Listen Command", command=listen_command, font=("Arial", 12))
btn_listen.pack(pady=5)

btn_camera = tk.Button(root, text="Open Camera", command=open_camera, font=("Arial", 12))
btn_camera.pack(pady=5)

btn_yolo = tk.Button(root, text="Start Object Detection", command=start_object_detection, font=("Arial", 12))
btn_yolo.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12), fg="red")
btn_exit.pack(pady=10)

speak("Welcome! I am Zeel's Bot designed specially for you cutie. How may I help you?")

root.mainloop()
