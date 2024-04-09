import numpy as np

# Example parameters - replace with your actual measurements and material properties
torque_applied = 10  # Nm, example torque applied to the screw thread
lever_arm_length = 0.05  # m, distance from the hinge axis to the point of force application
frequency_of_operation = 2  # operations per second, estimate based on typical use
material_fatigue_strength_coefficient = 900e6  # Pa, for the specified material
material_fatigue_strength_exponent = -0.12  # for the specified material
safety_factor = 1.5  # Chosen based on engineering judgment

# Calculate resultant forces at the hinge points
# Assuming direct linear relationship between torque applied and force at the hinge
force_at_hinge = torque_applied / lever_arm_length

# Estimate stress range at the hinge - this requires more detailed mechanical analysis or FEA
# Placeholder for stress calculation - replace with actual stress analysis results
stress_range = force_at_hinge / (np.pi * (lever_arm_length ** 2))  # Simplified assumption

# Adjust for stress concentration factor (SCF) - requires empirical data or detailed FEA
scf = 2.0  # Example SCF for a similar hinge connection geometry
adjusted_stress_range = stress_range * scf

# Calculate fatigue life using the S-N curve method
cycles_to_failure = (material_fatigue_strength_coefficient / adjusted_stress_range) ** (1 / material_fatigue_strength_exponent)

# Apply safety factor
safe_cycles_to_failure = cycles_to_failure / safety_factor

print(f"Estimated safe cycles to failure: {safe_cycles_to_failure:.0f}")


""" second iteration of the script """
# import numpy as np
# import matplotlib.pyplot as plt

# # Material properties for 316 Stainless Steel, simplified for educational purposes
# density = 8000  # kg/m^3
# youngs_modulus = 193e9  # Pa
# poissons_ratio = 0.27
# yield_strength = 172.369e6  # Pa
# fatigue_strength_coefficient = 1000e6  # Pa, simplified assumption
# fatigue_strength_exponent = -0.12  # Typical for stainless steel

# # Simplified cyclic loading details
# max_stress = 250e6  # Pa, peak stress
# min_stress = 50e6  # Pa, minimum stress
# stress_ratio = min_stress / max_stress

# # Analytical estimation of fatigue life using a simplified Basquin equation
# def fatigue_life(stress_amplitude, fatigue_strength_coefficient, fatigue_strength_exponent):
#     N_f = (fatigue_strength_coefficient / stress_amplitude) ** (1 / fatigue_strength_exponent)
#     return N_f

# stress_amplitude = (max_stress - min_stress) / 2
# N_f = fatigue_life(stress_amplitude, fatigue_strength_coefficient, fatigue_strength_exponent)
# print(f"Estimated fatigue life: {N_f:.2e} cycles")


""" More advanced first iteration script """

# import numpy as np
# import matplotlib.pyplot as plt
# import scipy.stats as stats

# # Material properties for 316 Stainless Steel
# density = 8000  # kg/m^3
# youngs_modulus = 193e9  # Pa
# poissons_ratio = 0.27
# yield_strength = 172.369e6  # Pa
# ultimate_strength = 540e6  # Pa
# # Assumed S-N curve parameters for 316 Stainless Steel (replace with actual data)
# fatigue_strength_coefficient = 1000e6  # Pa
# fatigue_strength_exponent = -0.12  # Typical for stainless steel

# # Stress concentration factor (Kt) for the connection, assumed value for illustration
# stress_concentration_factor = 2.0

# # Load application details reflecting real operational conditions
# max_stress = 250e6  # Pa, peak stress
# min_stress = 50e6  # Pa, minimum stress
# R = min_stress / max_stress  # Stress ratio

# # Incorporating Goodman or Gerber correction for mean stress effect
# def goodman_correction(sigma_max, sigma_min, ultimate_strength):
#     sigma_m = (sigma_max + sigma_min) / 2
#     sigma_a = (sigma_max - sigma_min) / 2
#     corrected_sigma_a = sigma_a / (1 - (sigma_m / ultimate_strength))
#     return corrected_sigma_a

# # Adjusted S-N calculation with Goodman correction and SCF
# def calculate_adjusted_SN_life(sigma_max, sigma_min, Kt, ultimate_strength, fatigue_strength_coefficient, fatigue_strength_exponent):
#     sigma_a_corrected = goodman_correction(sigma_max * Kt, sigma_min * Kt, ultimate_strength)
#     N_f = (fatigue_strength_coefficient / sigma_a_corrected) ** (1 / fatigue_strength_exponent)
#     return N_f

# # Probabilistic approach to account for variability
# def probabilistic_SN_life(N_f):
#     # Assuming a log-normal distribution for life variability
#     mu, sigma = np.log(N_f), 0.1  # sigma is assumed variability, replace with actual data
#     dist = stats.lognorm(s=sigma, scale=np.exp(mu))
#     return dist

# N_f = calculate_adjusted_SN_life(max_stress, min_stress, stress_concentration_factor, ultimate_strength, fatigue_strength_coefficient, fatigue_strength_exponent)
# life_distribution = probabilistic_SN_life(N_f)

# print(f"Mean estimated cycles to failure: {life_distribution.mean():.2e}")
# print(f"Standard deviation of cycles to failure: {life_distribution.std():.2e}")

# # Plotting the probability density function of the fatigue life
# x = np.linspace(life_distribution.ppf(0.01), life_distribution.ppf(0.99), 100)
# plt.figure(figsize=(8, 4))
# plt.plot(x, life_distribution.pdf(x), 'r-', lw=2)
# plt.title('Probability Density Function of Fatigue Life')
# plt.xlabel('Cycles to Failure')
# plt.ylabel('Density')
# plt.grid(True)
# plt.show()

# # Note: This script assumes specific values for illustration purposes. Replace these with your actual data.
