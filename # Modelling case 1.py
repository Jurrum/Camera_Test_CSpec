import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
Here we calculate the total deformation due to the pressure acting on the outer surface of the cylinder
'''

#Constants
pressure_mmHg = 70  #mmHg
pressure_Pa = pressure_mmHg * 133.322368  # Convert mmHg to Pa
print(f"Pressure: {pressure_Pa} Pa")
young_modulus = 193e9  #Pa
yield_strength = 172.369e6 #Pa
outer_diameter = 35  #mm
inner_diameters = [30, 31, 32, 33, 34, 34.5, 34.6, 34.7, 34.8]  #mm

# Array of sizes for the table
sizes = ["Outside:35mm, Inside:30mm", "Outside:35mm, Inside:31mm", "Outside:35mm, Inside:32mm", 
         "Outside:35mm, Inside:33mm", "Outside:35mm, Inside:34mm", "Outside:35mm, Inside:34.5mm middle mesh",
         "Outside:35mm, Inside:34.6mm fine mesh", "Outside:35mm, Inside:34.7mm fine mesh", 
         "Outside:35mm, Inside:34.8mm fine mesh"]

# Calculate deformation, von Mises stress, and check if yield strength is met
results = []
for D_i in inner_diameters:
    mean_radius = (outer_diameter + D_i) / 2 * 1e-3  # Convert to meters
    wall_thickness = (outer_diameter - D_i) / 2  # Wall thickness in mm for the table
    wall_thickness_m = wall_thickness * 1e-3  # Convert to meters for calculations
    radius_ratio = wall_thickness / (outer_diameter / 2)
    
    # Check if the thin-walled assumption is valid
    thin_walled = radius_ratio < 0.1
    
    # Deformation and von Mises stress calculations
    if thin_walled:
        # Assuming linear elastic behavior and thin-walled condition
        hoop_stress = (pressure_Pa * mean_radius) / wall_thickness_m / 1e6  # in MPa
        longitudinal_stress = hoop_stress / 2  # Approximation for thin-walled cylinders
        von_mises_stress = np.sqrt(hoop_stress**2 - hoop_stress*longitudinal_stress + longitudinal_stress**2)  # in MPa
        deformation = (pressure_Pa * mean_radius) / (wall_thickness_m * young_modulus) * 1e3  # Deformation in mm
    else:
        # Placeholder values for cases where the thin-walled assumption does not hold
        hoop_stress = 0
        von_mises_stress = 0
        deformation = 0 #Wall thickness is too large for thin-walled assumption to hold so deformation is 0
        # Beyond scope of this project / not necesary to calculate for the table since values will be too low
    
    yield_met = "Yes" if von_mises_stress >= yield_strength else "No"
    results.append((wall_thickness, deformation, von_mises_stress, yield_met, thin_walled))

#Dataframe to display results
df = pd.DataFrame(results, columns=['Wall Thickness (mm)', 'Deformation (mm)', 'Von Mises Stress (MPa)', 'Yield Strength Met', 'Thin-Wall'])
df.index = sizes
print(df)

# Plotting Deformation and Von Mises Stress vs. Wall Thickness
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Wall Thickness (mm)')
ax1.set_ylabel('Deformation (mm)', color=color)
ax1.plot(df['Wall Thickness (mm)'], df['Deformation (mm)'], color=color, marker='o', label='Deformation')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  
color = 'tab:blue'
ax2.set_ylabel('Von Mises Stress (MPa)', color=color)
ax2.plot(df['Wall Thickness (mm)'], df['Von Mises Stress (MPa)'], color=color, marker='x', label='Von Mises Stress')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  
plt.title('Corrected Deformation and Von Mises Stress vs. Wall Thickness')
fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
plt.show()
