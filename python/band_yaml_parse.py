import lzma
import os
import sys
import numpy as np
import yaml
from yaml import CLoader as Loader
with open(".\\input\\band_with_eigen.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.CLoader)

frequencies = []
distances = []
qpoints = []
labels = []
for v in data["phonon"]:
    if "label" in v:
        labels.append(v["label"])
    else:
        labels.append(None)
    frequencies.append([f["frequency"] for f in v["band"]])
    qpoints.append(v["q-position"])
    distances.append(v["distance"])

if "labels" in data:
    labels = data["labels"]
elif all(x is None for x in labels):
    labels = []
dist = np.array(distances)
freqs = np.array(frequencies)
qp = np.array(qpoints)
combined = np.column_stack((dist, freqs))
np.savetxt('phonon_dispersion.csv', combined, delimiter=',', comments='', fmt='%.6f')
print("Distances: ", len(distances))
print("Freq len: ",len(frequencies))
print("Frequencies: ", len(frequencies[0]))
print("QPoints: ", qpoints)
print("Labels: ", labels)
print("Segment: ", data["segment_nqpoint"])
#return (
#    np.array(distances),
##    np.array(frequencies),
#    np.array(qpoints),
#    data["segment_nqpoint"],
#    labels,
#)