import pandas as pd
import matplotlib.pyplot as plt

# Data as per the table provided by the user
data = {
    "Wall Thickness (mm)": [2.5, 2.0, 1.5, 1.0, 0.5, 0.25, 0.2, 0.15, 0.1],
    "Von Mises Stress Python (MPa)": [0.00, 0.00, 0.180503, 0.274796, 0.557674, 1.123431, 1.406310, 1.877774, 2.820701],
    "Von Mises Stress SW (MPa)": [0.00, 0.08486, 0.1043, 0.1292, 0.1877, 0.2503, 0.2684, 0.2884, 0.3135]
}

# Creating a DataFrame
df = pd.DataFrame(data)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df["Wall Thickness (mm)"], df["Von Mises Stress Python (MPa)"], marker='o', label='Python Script')
plt.plot(df["Wall Thickness (mm)"], df["Von Mises Stress SW (MPa)"], marker='s', label='SW')

# Titles and labels
plt.title('Comparison of Von Mises Stress Over Wall Thickness')
plt.xlabel('Wall Thickness (mm)')
plt.ylabel('Von Mises Stress (MPa)')
plt.legend()
plt.grid(True)
plt.gca().invert_xaxis()  # Inverting the x-axis as the wall thickness decreases from left to right
plt.show()
