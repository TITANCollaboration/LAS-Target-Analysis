import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
numfiles = 10
os.chdir(current_dir)
targetIDs = []
files = []
for i in range(numfiles): 
    targetID = 'Cu_11_' + '0'*(2-len(str(i+1))) + str(i+1)
    targetIDs.append(targetID)
    file = 'ImageJ_output\\'+targetID+ ' Measurements.csv'
    files.append(file)

total_ablation_spots_x = []
total_ablation_spots_z = []
first = True
for i in range(len(files)):
    measurements = np.loadtxt(files[i], skiprows = 1, delimiter = ',') 
    target_centroid = np.array([measurements[1, 2],measurements[1, 3]])
    ablation_spots = measurements[2:,:]

    ablated_x = ablation_spots[:,2]
    ablated_z = ablation_spots[:,3]
    for j in range(len(ablated_x)):
        
        if first:
            for _ in range(len(ablated_x)):
                total_ablation_spots_x.append([])
                total_ablation_spots_z.append([])
            first = False
        total_ablation_spots_x[j].append(ablated_x[j]-target_centroid[0])
        total_ablation_spots_z[j].append(ablated_z[j]-target_centroid[1])



target_to_mirror_x = 0.053
target_to_mirror_z = 0.072
std_x = []
std_z = []
for i in range(len(total_ablation_spots_x)):
    std_x.append(np.std(total_ablation_spots_x[i]))
    std_z.append(np.std(total_ablation_spots_z[i]))
    print("-----STD for point: " + str(i+1)+"------")
    print("Target X: " + str(np.std(total_ablation_spots_x[i])))
    print('Target Z: ' + str(np.std(total_ablation_spots_z[i])))
    print("Mirror X: " + str(np.std(total_ablation_spots_x[i])*target_to_mirror_x))
    print("Mirror Z: " + str(np.std(total_ablation_spots_z[i])*target_to_mirror_z))

print(np.mean(std_x))
print(np.mean(std_z))
print(np.mean(std_x)*target_to_mirror_x)
print(np.mean(std_z)*target_to_mirror_z)



