import re
import math

def stokes_factor(nu_cm, I_raman, T=300.0):
    # k_B * 300 K ~ 208 cm^-1 (roughly)
    # h nu / (k_B T) ~ nu / (208 cm^-1)
    k_B_T_cm = 208.0 * (T / 300.0)  # scale if T != 300

    x = nu_cm / k_B_T_cm  # dimensionless ratio h nu / (k_B T)
    if x < 1e-6:
        # avoid numerical blow-up if nu_cm is extremely small
        # in practice, you won't usually have that small, but just in case
        n_bar = 1.0 / x  # approximate expansion
    else:
        n_bar = 1.0 / (math.exp(x) - 1.0)  # Bose-Einstein factor
    laser_factor = math.pow((15600.0-nu_cm)/15600.0, 4)
    return ((n_bar + 1.0) / nu_cm) * I_raman * laser_factor


def extract_frequencies(file_path):
    frequencies = []
    intensities = []
    activities = []
    irreps = []
    in_table = False
    
    with open(file_path, 'r') as file:
        for line in file:
            # Detect the start of a new vibrational frequencies table
            if "Vibrational Frequencies" in line:
                in_table = True
                continue
            
            # Detect the end of the table
            if in_table and "." * 70 in line:
                in_table = False
            
            if in_table:
                parts = line.split()
                if len(parts) == 9 and parts[7] == 'Y':
                    freq = float(parts[2])
                    activity = float(parts[6])
                    intensity = stokes_factor(freq, activity)
                    frequencies.append(freq)
                    intensities.append(intensity)
                    activities.append(activity)
                    irreps.append(parts[3])
    return frequencies, intensities, activities, irreps
import os 
filename = 'input\dfpt_freq.txt'
frequencies, intensities, activities, irreps = extract_frequencies(filename)

print("Extracted Frequencies:", frequencies)
print("Extracted Intensities:", intensities)