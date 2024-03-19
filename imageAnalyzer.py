import os
import cv2
import numpy as np
import pandas as pd
from skimage import exposure, feature, io, color
from skimage.measure import label, regionprops
from sklearn.cluster import KMeans
from PIL import Image, ImageStat


# Specify the path to the base folder containing patient cases
base_folder_path = r'\IARCImageBankVIA'


# Metrics calculation functions
def calculate_brightness(image):
    img = Image.open(image).convert('L')
    stat = ImageStat.Stat(img)
    return stat.mean[0]

def calculate_contrast(image):
    img = cv2.imread(image, 0)
    return img.std()

def calculate_sharpness(image):
    img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    return cv2.Laplacian(img, cv2.CV_64F).var()

def calculate_noise_level(image):
    img = cv2.imread(image)
    dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    noise = img - dst
    return np.mean(noise)

def calculate_dynamic_range(image):
    img = io.imread(image)
    v_min, v_max = np.percentile(img, (2, 98))
    return v_max - v_min

def calculate_color_accuracy(image):
    img = cv2.imread(image)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    reshaped_img = img_rgb.reshape((-1, 3))
    kmeans = KMeans(n_clusters=3, random_state=0).fit(reshaped_img)
    dominant_colors = kmeans.cluster_centers_
    dominant_colors_hex = ['#%02x%02x%02x' % (int(color[0]), int(color[1]), int(color[2])) for color in dominant_colors]
    return dominant_colors_hex

def calculate_texture(image):
    img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    g = feature.graycomatrix(img, [1], [0], 256, symmetric=True, normed=True)
    properties = ['contrast', 'dissimilarity', 'homogeneity', 'ASM', 'energy']
    texture_features = {prop: feature.graycoprops(g, prop)[0, 0] for prop in properties}
    return texture_features

def calculate_geometric_properties(image):
    img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    labels = label(thresh)
    props = regionprops(labels)
    areas = [prop.area for prop in props]
    eccentricities = [prop.eccentricity for prop in props]
    return {"mean_area": np.mean(areas), "mean_eccentricity": np.mean(eccentricities)}

def get_image_dimensions(image):
    with Image.open(image) as img:
        return img.width, img.height
 
def initialize_csv(file_path, columns):
    """Initializes the CSV file with headers."""
    df = pd.DataFrame(columns=columns)
    df.to_csv(file_path, index=False)

def analyze_and_append_results(base_folder_path, csv_file_path):
    columns = ['PatientID', 'Filename', 'Width', 'Height', 'Brightness', 'Contrast', 
               'Sharpness', 'Noise Level', 'Dynamic Range', 'Dominant Color 1 Hex', 
               'Dominant Color 2 Hex', 'Dominant Color 3 Hex', 'Texture Contrast', 
               'Texture Dissimilarity', 'Texture Homogeneity', 'Texture ASM', 'Texture Energy',
               'Mean Area', 'Mean Eccentricity']

    # Initialize the CSV file with the appropriate columns
    initialize_csv(csv_file_path, columns)

    for root, dirs, files in os.walk(base_folder_path):
        # Exclude processing the base folder itself, only process subdirectories (patient cases)
        if root == base_folder_path:
            continue

        patient_id = os.path.basename(root)  # Get the patient ID from the folder name
        
        results = []  # Prepare to collect results for this patient

        for filename in files:
            if filename.lower().endswith((".jpg", ".png")):
                image_path = os.path.join(root, filename)

                # Process image and calculate metrics
                width, height = get_image_dimensions(image_path)
                brightness = calculate_brightness(image_path)
                contrast = calculate_contrast(image_path)
                sharpness = calculate_sharpness(image_path)
                noise_level = calculate_noise_level(image_path)
                dynamic_range = calculate_dynamic_range(image_path)
                color_accuracy = calculate_color_accuracy(image_path)
                texture_features = calculate_texture(image_path)
                geometric_properties = calculate_geometric_properties(image_path)

                # Combine all metric values into a list for the current row
                row_values = [patient_id, filename, width, height, brightness, contrast, sharpness,
                              noise_level, dynamic_range] + color_accuracy + \
                             list(texture_features.values()) + list(geometric_properties.values())
                
                results.append(row_values)
        
        # After collecting all results for this patient, append them to the CSV
        df = pd.DataFrame(results, columns=columns)
        # Use append mode for all cases after the first, without writing the header again
        df.to_csv(csv_file_path, mode='a', header=False, index=False)

# Specify the path to the CSV file to write
csv_file_path = 'image_analysis_results_Colpo.csv'

# Run the analysis and append results to the CSV
analyze_and_append_results(base_folder_path, csv_file_path)

print("Analysis complete. Results appended to the CSV file.")