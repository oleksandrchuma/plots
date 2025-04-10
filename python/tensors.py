import re

def extract_mode_data(file_path):
    mode_data = {}
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if "Mode number:" in line:
            mode_match = re.search(r"Mode number:\s*(\d+)", line)
            if mode_match:
                mode = int(mode_match.group(1))
                matrix = []
                depolarisation_ratio = None
                for j in range(i+1, i+4):
                    row_line = lines[j]
                    numbers = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", row_line)
                    if j == i+1:
                        if len(numbers) >= 4:
                            depolarisation_ratio = float(numbers[3])
                        row = [float(x) for x in numbers[:3]]
                    else:
                        row = [float(x) for x in numbers[:3]]
                    matrix.append(row)
                mode_data[mode] = {"matrix": matrix, "depolarisation_ratio": depolarisation_ratio}
                i += 4
                continue
        i += 1

    return mode_data

def calculate_IRam(matrix):
    a = (matrix[0][0] + matrix[1][1] + matrix[2][2]) / 3.0
    
    diff1 = matrix[0][0] - matrix[1][1]
    diff2 = matrix[0][0] - matrix[2][2]
    diff3 = matrix[1][1] - matrix[2][2]
    b2 = 0.5 * (diff1**2 + diff2**2 + diff3**2)
    b2 += 3 * (matrix[0][1]**2 + matrix[0][2]**2 + matrix[1][2]**2)
    gamma = 0.75*((matrix[0][1]-matrix[1][0])**2 + (matrix[0][2]-matrix[2][0])**2+(matrix[1][2]-matrix[2][1])**2)    
    IRam = 45 * (a**2) + 7 * b2 + 5*gamma
    return IRam, a, b2
print(8.53863120/0.02172849)
file_path = "input\\polar_tensors.txt"  
data = extract_mode_data(file_path)

for mode, info in data.items():
    print(f"Mode: {mode}")
    print("Raman Tensor Matrix:")
    for row in info["matrix"]:
        print(row)
    print("Depolarisation Ratio:", info["depolarisation_ratio"])
    print("-" * 40)

for mode, info in sorted(data.items()):
        matrix = info["matrix"]
        IRam, a, b2 = calculate_IRam(matrix)
        depol_file = info["depolarisation_ratio"]
        denom = 45*(a**2) + 4*b2
        rho_computed = (3*b2)/denom if denom != 0 else None
        print(f"{mode:3d}       {depol_file:>8.5f}                  {IRam:>12.8f}   (a = {a: .8f}, b^2 = {b2: .8f}, rho = {rho_computed: .8f})")

print(8.53863120*11.8651833/0.02172849)