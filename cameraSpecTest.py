import cv2
import numpy as np
import time

def calculate_brightness(frame):
    return np.mean(frame)

def calculate_contrast(frame):
    return np.std(frame)

def calculate_saturation(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    saturation = hsv_frame[:, :, 1]
    return np.mean(saturation)

def calculate_sharpness(frame):
    laplacian_var = cv2.Laplacian(frame, cv2.CV_64F).var()
    return laplacian_var

def calculate_color_balance(frame):
    average_color_per_channel = np.mean(frame, axis=(0, 1))
    return average_color_per_channel

def calculate_noise_level(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    noise_level = np.std(gray)
    return noise_level

def estimate_dynamic_range(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    min_intensity = np.min(gray)
    max_intensity = np.max(gray)
    dynamic_range = max_intensity - min_intensity
    return dynamic_range

def calculate_motion_blur(frame):
    variance = cv2.Laplacian(frame, cv2.CV_64F).var()
    return variance

camera_index = 3
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print(f"Error: Could not open video capture device at index {camera_index}.")
    exit()

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

frame_count = 0
start_time = time.time()
zoom_level = 1.0  # Initial zoom level
pan_x, pan_y = 0, 0  # Initial pan positions

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Adjustments for zoom and pan
        original_height, original_width = frame.shape[:2]
        new_width = int(original_width / zoom_level)
        new_height = int(original_height / zoom_level)
        center_x, center_y = original_width // 2, original_height // 2
        
        x1 = max(center_x - new_width // 2 + pan_x, 0)
        x2 = min(x1 + new_width, original_width)
        y1 = max(center_y - new_height // 2 + pan_y, 0)
        y2 = min(y1 + new_height, original_height)

        # Ensure cropping coordinates are within the frame bounds
        x1 = max(min(center_x - new_width // 2 + pan_x, original_width - new_width), 0)
        x2 = x1 + new_width
        y1 = max(min(center_y - new_height // 2 + pan_y, original_height - new_height), 0)
        y2 = y1 + new_height

        cropped_frame = frame[y1:y2, x1:x2]
        resized_frame = cv2.resize(cropped_frame, (original_width, original_height), interpolation=cv2.INTER_LINEAR)


        # Additional safeguard: Check if cropped_frame is empty before resizing
        if cropped_frame.size == 0:
            print("Cropped frame is empty. Adjusting zoom and pan values...")
            zoom_level = 1.0  # Reset zoom level
            pan_x, pan_y = 0, 0  # Reset pan positions
            continue  # Skip the rest of the loop iteration

        
       
        # Update the calculations to use cropped_frame or resized_frame
        if frame_count % 30 == 0:  # Analyze metrics on the adjusted frame
            brightness = calculate_brightness(cropped_frame)
            contrast = calculate_contrast(cropped_frame)
            saturation = calculate_saturation(cropped_frame)
            sharpness = calculate_sharpness(cropped_frame)
            color_balance = calculate_color_balance(cropped_frame)
            noise_level = calculate_noise_level(cropped_frame)
            dynamic_range = estimate_dynamic_range(cropped_frame)
            motion_blur = calculate_motion_blur(cropped_frame)

            overlay_texts = [
                "Zoom & Pan Info:",
                f"Zoom Level: {zoom_level:.2f}, Pan X: {pan_x}, Pan Y: {pan_y}",
                f"Height: {original_height}. Width: {original_width}",
                f"Brightness: {brightness:.2f}",
                f"Contrast: {contrast:.2f}",
                f"Saturation: {saturation:.2f}",
                f"Sharpness: {sharpness:.2f}",
                f"Color Balance B:{color_balance[0]:.2f} G:{color_balance[1]:.2f} R:{color_balance[2]:.2f}",
                f"Noise Level: {noise_level:.2f}",
                f"Dynamic Range: {dynamic_range}",
                f"Motion Blur: {motion_blur:.2f}"
            ]

        font = cv2.FONT_HERSHEY_SIMPLEX
        initial_position = (10, 25)
        font_scale = 0.5
        font_color = (255, 255, 255)
        line_type = 2
        line_height = 20

        for i, text in enumerate(overlay_texts):
            y_position = initial_position[1] + i * line_height
            cv2.putText(resized_frame, text, (initial_position[0], y_position), font, font_scale, font_color, line_type)

        cv2.imshow('Camera Feed', resized_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('w'):
            pan_y -= 10
        elif key == ord('s'):
            pan_y += 10
        elif key == ord('a'):
            pan_x -= 10
        elif key == ord('d'):
            pan_x += 10
        elif key == ord('r'):
            zoom_level = min(zoom_level + 0.1, 3.0)
        elif key == ord('f'):
            zoom_level = max(zoom_level - 0.1, 1.0)

        frame_count += 1
finally:
    cap.release()
    cv2.destroyAllWindows()