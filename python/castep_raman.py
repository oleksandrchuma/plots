import re
import math
import scipy
import scipy.constants
import numpy as np
import matplotlib.pyplot as plt

def stokes_factor(nu_cm, I_raman, T=300.0):
    hc = scipy.constants.Planck*scipy.constants.speed_of_light*100.0 #J·cm
    kb = scipy.constants.Boltzmann  
    x = nu_cm*hc / (kb*T)  
    n_bar = 1.0 / (math.exp(x) - 1.0)  # Bose-Einstein factor
    laser_factor = math.pow((15600.0-nu_cm)/15600.0, 4)
    return ((n_bar + 1.0) / nu_cm) * I_raman * laser_factor

def extract_frequencies(file_path):
    frequencies = []
    intensities = []
    ir_freq = []
    ir_intes = []
    activities = []
    irreps = []
    in_table = False
    
    with open(file_path, 'r') as file:
        for line in file:
            # table start
            if "Vibrational Frequencies" in line:
                in_table = True
                continue
            
            # table end
            if in_table and "." * 70 in line:
                in_table = False
            
            if in_table:
                parts = line.split()
                if len(parts) == 9:
                    if parts[7] == 'Y':
                        freq = float(parts[2])
                        activity = float(parts[6])
                        intensity = stokes_factor(freq, activity)
                        frequencies.append(freq)
                        intensities.append(intensity)
                        activities.append(activity)
                        irreps.append(parts[3])
                    if parts[5] == 'Y':
                        ir_freq.append(float(parts[2]))
                        ir_intes.append(float(parts[4]))
    return frequencies, intensities, activities, irreps, ir_freq, ir_intes

def gaussian(x, x0, I0, sigma):
    return I0 * np.exp(-((x - x0) ** 2) / (sigma ** 2))

def lorentzian(x, x0, I0, gamma):
    return I0 / (1 + ((x - x0) / (gamma*0.5)) ** 2)

def generate_raman_spectrum(peaks, intensities, sigma=5, scalea=100, scalee=100, scalef=100, x_range=(0, 900), num_points=900, radioVal = 'Lorentzian'):
    #max_intensity = max(intensities)
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = np.zeros_like(x)
    for x0, I0, irr in zip(peaks, intensities, irreps):
        scale = 100 
        if irr == 'a':
            scale = scalef
        elif irr == 'b':
            scale = scalea
        elif irr == 'c':
            scale = scalee
        if radioVal == 'Gaussian':
            y += gaussian(x, x0, (I0)*(scale/100.0), sigma)
        else:
            y += lorentzian(x, x0, (I0)*(scale/100.0), sigma)
    
    return x, y

def save(sigma):
    #save x,y to csv
    x, y = generate_raman_spectrum(frequencies, intensities, sigma=sigma)
    np.savetxt('raman.csv', np.column_stack((x, y)), delimiter=',', fmt='%.4f')

import os 
filename = 'dfpt_freq.txt'
frequencies, intensities, activities, irreps, ir_freq, ir_intens = extract_frequencies(filename)
#print("Extracted Activities:", activities)
#print("Extracted Frequencies:", frequencies)
#print("Extracted Intensities:", intensities)
#print("Extracted IR frequencies:", ir_freq)
#print("Extracted IR intensities:", ir_intens)
#print("Irreps: ", irreps)

sigma = 10
x, y= generate_raman_spectrum(frequencies, intensities, sigma, 100, 100,100)
fig,ax = plt.subplots(figsize=(1000 / 100, 520 / 100), dpi=100)
plt.xlim(0, 900)
line, = plt.plot(x, y, label="Simulated Raman Spectrum", color='b')
plt.xlabel("Raman Shift (cm⁻¹)")
plt.ylabel("Intensity (a.u.)")
plt.title("Simulated Raman Spectrum")
major_ticks = np.arange(0, 900, step=100)
minor_ticks = np.arange(0, 900, step=10)
plt.xticks(major_ticks)
plt.gca().set_xticks(minor_ticks, minor=True)
plt.legend()
plt.show()