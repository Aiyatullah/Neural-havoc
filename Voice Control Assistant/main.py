import speech_recognition as sr
import cv2
import sys
import subprocess
import os
import pyttsx3  # Text-to-Speech


# Initialize text-to-speech engine
engine = pyttsx3.init()

# Change the voice
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Change to different index based on your system

engine.setProperty("rate", 160)  # Adjust speed (default ~200)
engine.setProperty("volume", 1.0)  # Set volume

# Define the correct path to the objects.py script
OBJECTS_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "objects.py")
GESTURE_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "gesture_control.py")



def speak(text):
    """Convert text to speech and speak it."""
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        speak(f"You said: {command}")  # Echo command in speech
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Could not connect to speech recognition service.")
        speak("Could not connect to speech recognition service.")
        return ""
    



def open_camera():
    cap = cv2.VideoCapture(0)
    print("Camera opened. Say 'close camera' to close or 'stop' to exit the program.")
    speak("Camera opened. Say 'close camera' to close or 'stop' to exit the program.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Camera", frame)

        command = listen_command()
        if "close camera" in command:
            print("Closing camera...")
            speak("Closing camera.")
            break

        if "stop" in command:
            print("Stopping program...")
            speak("Stopping program.")
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()







def start_geture_recognition():
    if os.path.exists(GESTURE_SCRIPT_PATH):
        print("Starting gesture recognition...")
        speak("Starting gesture recognition.")
        subprocess.run(["python", GESTURE_SCRIPT_PATH])
    else:
        print(f"Error: gesture_control.py not found at {GESTURE_SCRIPT_PATH}")
        speak(f"Error: gesture_control.py not found.")  






def start_object_detection():
    if os.path.exists(OBJECTS_SCRIPT_PATH):
        print("Starting YOLO object detection...")
        speak("Starting YOLO object detection.")
        subprocess.run(["python", OBJECTS_SCRIPT_PATH])
    else:
        print(f"Error: objects.py not found at {OBJECTS_SCRIPT_PATH}")
        speak(f"Error: objects.py not found.")

# Speak the welcome message at the start
speak("Welcome! I am Zeel's Bot designed specially for you cutie. How may I help you?")



# Main Loop
while True:
    command = listen_command()
    
    if "open camera" in command:
        open_camera()
    
    elif "start" in command:
        start_object_detection()

    elif "gesture" in command:
        start_geture_recognition()
    
    elif "stop" in command:
        print("Stopping program...")
        speak("Stopping program.")

    elif "who is hansa" in command:
        print("hansa is a good gurl")
        speak("hansa the bhosadpapu by thura")
        
    
    
