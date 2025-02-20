import re

def extract_frequencies(file_path):
    frequencies = []
    intensities = []
    in_table = False
    
    with open(file_path, 'r') as file:
        for line in file:
            # Detect the start of a new vibrational frequencies table
            if "Vibrational Frequencies" in line:
                in_table = True
                continue
            
            # Detect the end of the table
            if in_table and "-" * 70 in line:
                in_table = False
            
            if in_table:
                parts = line.split()
                if len(parts) == 9 and parts[7] == 'Y':
                    freq = float(parts[2])
                    intensity = float(parts[6])
                    frequencies.append(freq)
                    intensities.append(intensity)
    
    return frequencies, intensities
import os 
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'input\dfptfreq.txt')
print(filename)
f, i = extract_frequencies(filename)
print(f, i)