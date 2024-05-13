import RPi.GPIO as GPIO
import cv2
import threading
from time import sleep, time

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pin numbers for buttons and LED
button_pins = {
    'switch_camera': 17,  
    'dim_light_down': 27,
    'dim_light_up': 22,
    'green_filter': 23,
    'take_picture': 24,
    'zoom_in': 25,
    'zoom_out': 5
}
led_pin = 18  # Separate definition for clarity

# Setup LED pin for PWM and buttons for input
GPIO.setup(led_pin, GPIO.OUT)
pwm = GPIO.PWM(led_pin, 1000)  # Set frequency to 1kHz
pwm.start(0)  # Start PWM with 0% duty cycle (off)
for pin in button_pins.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Variables for camera and features
current_camera_index = 0
is_video_recording = False
video_writer = None

def initialize_cameras():
    cameras = []
    for i in range(2):
        cap = cvv.VideoCapture(i)
        if not cap.isOpened():
            print(f"Error: Camera {i} failed to open.")
            continue
        cameras.append(cap)
    return cameras

cameras = initialize_cameras()
if not cameras:
    print("Error: No cameras available.")
    GPIO.cleanup()
    exit(1)

def display_text(text, y=50):
    global frame
    if frame is not None:
        cv2.putText(frame, text, (50, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

def switch_camera():
    global current_camera_index
    if len(cameras) > 1:
        current_camera_index = 1 - current_camera_index
        display_text(f'Switching to camera {current_camera_index + 1}')

def adjust_light(amount):
    global brightness_level
    brightness_level += amount
    brightness_level = max(0, min(100, brightness_level))
    pwm.ChangeDutyCycle(brightness_level)
    display_text(f'Brightness: {brightness_level}%')

def toggle_green_filter():
    global green_filter_mode
    green_filter_mode = (green_filter_mode + 1) % 3
    filter_states = ['No Filter', 'Green Overlay', 'Green-Only']
    display_text(filter_states[green_filter_mode])

def apply_green_filter(frame):
    if green_filter_mode == 1:
        overlay = frame.copy()
        overlay[:, :, 1] = 255
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    elif green_filter_mode == 2:
        frame[:, :, 0] = frame[:, :, 0] * 0.1
        frame[:, :, 2] = frame[:, :, 2] * 0.1
    return frame

def take_picture():
    global frame
    if frame is not None:
        filename = f"Picture_{int(time())}.jpg"
        cv2.imwrite(filename, frame)
        display_text("Picture taken")

def start_stop_video():
    global is_video_recording, video_writer
    if not is_video_recording:
        filename = f"Video_{int(time())}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (int(frame.shape[1]), int(frame.shape[0])))
        is_video_recording = True
        display_text("Video recording started")
    else:
        if video_writer is not None:
            video_writer.release()
            is_video_recording = False
            display_text("Video recording stopped")

def zoom(direction):
    global zoom_level
    zoom_level += direction
    display_text(f'Zoom level: {zoom_level}')

def check_button_press():
    button_state = GPIO.input(button_pins['take_picture'])
    if button_state == GPIO.HIGH:
        start_time = time()
        while GPIO.input(button_pins['take_picture']) == GPIO.HIGH:
            sleep(0.1)
        if time() - start_time < 2:
            take_picture()
        else:
            start_stop_video()

for pin in button_pins.values():
    GPIO.add_event_detect(pin, GPIO.RISING, callback=lambda channel: threading.Thread(target=check_button_press).start(), bouncetime=300)

try:
    while True:
        ret, frame = cameras[current_camera_index].read()
        if ret:
            frame = apply_green_filter(frame)
            cv2.putText(frame, f"Camera {current_camera_index + 1}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow("Camera Feed", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
except KeyboardInterrupt:
    print("Exiting")
finally:
    if video_writer is not None:
        video_writer.release()
    pwm.stop()
    for cam in cameras:
        cam.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
