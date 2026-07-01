import cv2         # OpenCV for image processing
import threading   # Threading for concurrent execution
import pygame       # Play sound for alarm using pygame
import smtplib      # For sending email alerts

# Initialize pygame mixer
pygame.mixer.init()

# Load the Haar cascade fire detection model
fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml')
# Start video capture (0 = default camera)
vid = cv2.VideoCapture(0)
runOnce = False  # Flag to ensure the email is sent only once

# Function to play the alarm soundqq
def play_alarm_sound_function():
    try:
        pygame.mixer.music.load('alarm.wav')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        print("Fire alarm ended")
    except Exception as e:
        print(f"Error playing alarm: {e}")

# Function to send alert email
def send_mail_function():
    sender_email = "anaswork41@gmail.com"
    sender_password = "upmi sjgz gpkx ydow"
    recipient_email = "anaswork41@gmail.com"

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        message = "Subject: Fire Alert!\n\nWarning: Fire has been detected by the system. Please take necessary actions."
        server.sendmail(sender_email, recipient_email, message)
        server.quit()
        print(f"Alert mail sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main loop to read video frames and detect fire
while True:
    Alarm_Status = False
    ret, frame = vid.read()
    if not ret:
        print("Failed to capture frame from camera. Exiting.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (0, 0, 255), 2)
        print("Fire alarm initiated")

        threading.Thread(target=play_alarm_sound_function).start()

        if not runOnce:
            print("Sending alert email...")
            threading.Thread(target=send_mail_function).start()
            runOnce = True
        else:
            print("Alert email already sent.")

    cv2.imshow('Fire Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
vid.release()
cv2.destroyAllWindows()