import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from scipy.stats import pearsonr, spearmanr

# Load the dataset
data_path = r'\image_analysis_results_VIA.csv'  
data = pd.read_csv(data_path)

# Basic Descriptive Statistics
print("Descriptive Statistics:")
print(data.describe())

# Distribution Analysis for Selected Metrics
metrics = ['Brightness', 'Contrast', 'Sharpness', 'Texture Contrast']
sns.set(style="whitegrid")

fig, axes = plt.subplots(len(metrics), 1, figsize=(8, 15))
for i, metric in enumerate(metrics):
    sns.histplot(data[metric], bins=30, ax=axes[i], kde=True)
    axes[i].set_title(f'Distribution of {metric}')
    axes[i].set_xlabel(metric)
    axes[i].set_ylabel('Frequency')
plt.tight_layout()
plt.show()

# Outlier Detection
def detect_outliers(data, feature):
    Q1 = data[feature].quantile(0.25)
    Q3 = data[feature].quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((data[feature] < (Q1 - 1.5 * IQR)) | (data[feature] > (Q3 + 1.5 * IQR)))
    return outliers

outliers_dict = {metric: detect_outliers(data, metric) for metric in metrics}
outliers_counts = {metric: outliers.sum() for metric, outliers in outliers_dict.items()}
print("Outliers counts:")
print(outliers_counts)

# Correlation Analysis
correlation_matrix = data[metrics].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', square=True, fmt=".2f")
plt.title('Correlation Matrix of Selected Metrics')
plt.show()

# Color Analysis
# Convert hex color codes to RGB
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

# Applying the conversion
colors = data['Dominant Color 1 Hex'].apply(hex_to_rgb)

# Clustering dominant colors
kmeans = KMeans(n_clusters=5)  # Adjust the number of clusters as needed
colors_rgb = np.array(list(colors))
kmeans.fit(colors_rgb)
cluster_centers = kmeans.cluster_centers_

# Plotting the most common colors
plt.figure(figsize=(10, 2))
for i, color in enumerate(cluster_centers):
    plt.fill_between([i, i+1], 0, 1, color=color/255)
plt.xlim(0, len(cluster_centers))
plt.axis('off')
plt.title('Most Common Dominant Colors')
plt.show()

# Statistical Tests
print("\nConducting Statistical Tests...")
# Example: Pearson and Spearman correlations between 'Brightness' and 'Texture Contrast'
pearson_corr, _ = pearsonr(data['Brightness'], data['Texture Contrast'])
spearman_corr, _ = spearmanr(data['Brightness'], data['Texture Contrast'])
print(f"Pearson correlation between Brightness and Texture Contrast: {pearson_corr:.3f}")
print(f"Spearman correlation between Brightness and Texture Contrast: {spearman_corr:.3f}")



