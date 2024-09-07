import numpy as np 
import matplotlib.pyplot as plt 
import os 
import csv
import matplotlib.pyplot as plt

def get_displacement(target_centroid, mirror_centroid, target_coords, mirror_coords, target_to_mirror):
    """
    Takes target and mirror coords and the relation between them and determines the displacement of the spot from the set position in mirror coords
    @params:
    target_centroid : numpy array, the centroid position of the target in target mm
    mirror_centroid : numpy array, the assumed centroid position of the target in mirror mm
    target_coords : numpy array, the coordinates of the point in target mm
    mirror_coords : numpy array, the assumed coordinates of the point in mirror mm 
    target_to_mirror : numpy array, [x scaling factor in mirror mm/target mm, z scaling factor in mirror mm/target mm] 
    """
    #Get vector from the target center to the point in target mm
    target_pos = target_coords-target_centroid

    #Scale vector with conversion factors
    mirror_pos = target_pos*target_to_mirror

    displacement = (mirror_coords-mirror_centroid) - mirror_pos

    return displacement


def visualize_coords(grid):
    max_row_length = max(len(row) if row is not None else 0 for row in grid)

    # Convert None values to strings with the same length as [21.90, 92.245]
    grid_padded = [
        ['{: <1}'.format(str(elem)) if elem is not None else ' ' * 1 for elem in row]
        for row in grid
    ]
    grid_padded = '\n'.join([' '.join(row) for row in grid_padded])
    return grid_padded

def rotate(ablation_spots, theta):
    rotation_matrix = np.array([[np.cos(theta), -1*np.sin(theta)],[np.sin(theta), np.cos(theta)]])
    return np.dot(ablation_spots, rotation_matrix.T)

#----Read output csv from imageJ---- 
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
targetID = 'Cu_12_10 Groups'
file = 'ImageJ_output\\'+targetID+ ' Measurements.csv'

#Store the measurements taken with the following column structure: 
# ID,Area,X,Y,Perim.,BX,BY,Width,Height,Major,Minor,Angle,Length

measurements = np.loadtxt(file, skiprows = 1, delimiter = ',') 

#----Define the mirror coordinates and ablation order----

define_mirror_coords = 2 # 1 for Option1 - Uniform rectangular grid
                         # 2 for Option2 - Manually define
                         # 3 for Option3 - Read from csv
if define_mirror_coords == 1:
    #Option1: Generate mirror coordinates for uniform rectangular grid:
    mirror_center_x = 5.686 
    mirror_center_z = 4.658

    start_x = 5.6339
    stop_x = 5.7381
    step_x = 0.0521 #step size in x (mirror mm)

    start_z = 4.368
    stop_z = 4.513
    step_z = 0.0725 #step size in z (mirror mm)

    mirror_x = np.arange(start_x,stop_x,step_x) 
    mirror_z = np.arange(start_z, stop_z, step_z)

#Option 2: Input mirror coordinates manually
elif define_mirror_coords == 2:
    if targetID[:5] == 'Cu_11':
        mirror_x = np.array([5.6339, 5.7381, 5.7381, 5.6339, 5.686]) #stores the x coordinate (in mirror mm) of each point ablated in order of ablation
        mirror_z = np.array([4.5855, 4.5855, 4.7305, 4.7305, 4.658]) #stores the z coordinate (in mirror mm) of each point ablated in order of ablation
        step_x = 0.0521 #step size in x (mirror mm)
        step_z = 0.0725 #step size in z (mirror mm)
        mirror_center_x = 5.686 
        mirror_center_z = 4.658
        step_thresh_x = 0.5
        step_thresh_z = 0.5
        

    elif targetID == 'Cu_10_01':
        mirror_x = np.array([5.5818, 5.6339, 5.686, 5.7381, 5.7902, 5.7902,5.7902, 5.7381, 5.686, 5.6339, 5.5818, 5.5818, 5.686])
        mirror_z = np.array([4.5855, 4.5855, 4.5855, 4.5855, 4.5855, 4.658, 4.7305, 4.7305, 4.7305, 4.7305, 4.7305, 4.658, 4.658])
        step_x = 0.0521 #step size in x (mirror mm)
        step_z = 0.0725 #step size in z (mirror mm)
        mirror_center_x = 5.686 
        mirror_center_z = 4.658
        step_thresh_x = 0.5
        step_thresh_z = 0.5
    elif targetID == 'Al_05':
        #(5.56,4.78), (5.46, 4.88), (5.46, 4.48), (5.86,4.48), (5.86, 4.58), (5.86, 4.68) () missing from picture

        mirror_x = np.array([5.61,5.61,5.61,5.61,5.61,5.635,5.635,5.635,5.635,5.635,5.66,5.66,5.66,5.66,5.66,5.66,5.685,5.685,5.685,5.685,5.685,5.71,5.71,5.71,5.71,5.71,5.71,5.66,5.61,5.56,5.56,5.56,5.56,5.61,5.66,5.71,5.76,5.76,5.76,5.76,5.76,5.76,5.66,5.56,5.46,5.46,5.46,5.46,5.56,5.66,5.76,5.86,5.86])
        mirror_z = np.array([4.63,4.655,4.68,4.705,4.73,4.73,4.705,4.68,4.655,4.63,4.63,4.655,4.68,4.705,4.73,4.73,4.705,4.68,4.655,4.63,4.63,4.655,4.68,4.705,4.73,4.78,4.78,4.78,4.73,4.68,4.63,4.58,4.58,4.58,4.58,4.58,4.63,4.68,4.73,4.78,4.88,4.88,4.88,4.78,4.68,4.58,4.48,4.48,4.48,4.48,4.78,4.88])
        step_x = 0.025 #smallest step size
        step_z = 0.05
        mirror_center_x = 5.66
        mirror_center_z = 4.68
        step_thresh_x = 0.14
        step_thresh_z = 0.14
    elif targetID =='Al_05 Rotate':
        #(5.61,4.78), (5.56,4.78), (5.76, 4.68), (5.46,4.88), (5.46,4.78), (5.46,4.48), (5.86, 4.48), (5.86, 4.58), (5.86,4.68) skipped due to poor visibility
        mirror_x = np.array([5.61,5.61 ,5.61,5.61, 5.61,5.635,5.635,5.635,5.635,5.635,5.66, 5.66, 5.66, 5.66, 5.66,5.685,5.685,5.685,5.685,5.685,5.71,5.71, 5.71,5.71, 5.71,5.71, 5.66,5.56,5.56,5.56,5.56, 5.61, 5.66, 5.71, 5.76, 5.76,5.76,5.76,5.76,5.66,5.56,5.46,5.46,5.56,5.66,5.76,5.86,5.86])
        mirror_z = np.array([4.63,4.655,4.68,4.705,4.73,4.73, 4.705,4.68 ,4.655,4.63, 4.63, 4.655,4.68, 4.705,4.73,4.73, 4.705,4.68, 4.655,4.63, 4.63,4.655,4.68,4.705,4.73,4.78, 4.78,4.73,4.68,4.63,4.58, 4.58, 4.58, 4.58, 4.58, 4.63,4.73,4.78,4.88,4.88,4.88,4.68,4.58,4.48,4.48,4.48,4.78,4.88])
        step_x = 0.025 #smallest step size in mirror mm
        step_z = 0.025
        mirror_center_x = 5.66
        mirror_center_z = 4.68
        step_thresh_x = step_x/0.0531-0.05 #convert to target mm and assume uncertainty in step size of 0.05
        step_thresh_z = step_z/0.072-0.05 
        print(step_thresh_x)
    order = np.array(range(len(mirror_x)))
    center_offset = np.array([0,0])


#Option 3: Read mirror coordinates from previously saved csv
elif define_mirror_coords == 3:
    file = ''
    np.loadtxt(file)

rotate_angle = measurements[2,11]/180*np.pi
rotate_angle = 1.5/180*np.pi
rotated_centroids = rotate(np.array(measurements[:,2:4]), rotate_angle)
target_centroid = np.array([rotated_centroids[1, 0],rotated_centroids[1, 1]])




minor_ticks_x = np.arange(3.2, 12.2, step_x/0.053)
minor_ticks_y = np.arange(6.4, 13.4, step_z/0.072)

print(step_x/0.053)

plt.figure()
plt.scatter(measurements[3:,2],measurements[3:,3])
plt.gca().set_xticks(minor_ticks_x, minor = True)
plt.gca().set_yticks(minor_ticks_y, minor = True)
plt.grid(True, which='minor', linestyle='--', linewidth=0.5)
plt.gca().invert_yaxis()

#plt.figure()
#plt.plot(measurements[3:,2],measurements[3:,3])
#plt.gca().invert_yaxis()

plt.figure()
plt.plot(rotated_centroids[3:,0],rotated_centroids[3:,1])
plt.gca().set_xticks(minor_ticks_x, minor = True)
plt.gca().set_yticks(minor_ticks_y, minor = True)
plt.grid(True, which='minor', linestyle='--', linewidth=0.5)
plt.gca().invert_yaxis()

plt.show()
ablated_x = rotated_centroids[3:,0]
ablated_z = rotated_centroids[3:,1]

#Sorting all coordinates into a 2D grid

#sort by z 
sorted_z= np.argsort(ablated_z)
ablated_x = ablated_x[sorted_z]
ablated_z = ablated_z[sorted_z]
mirror_x = mirror_x[sorted_z]
mirror_z = mirror_z[sorted_z]
order = order[sorted_z]
cols = []
col = []
rows = []
row = []

#iterating over sorted z indices except last one  
for i in range(len(ablated_z)-1):
    #add the index to the row 
    row.append(i)
    #if the vertical distance to the next point is greater than the threshold, add the row to the list of rows and start a new row for the next index
    if np.abs(ablated_z[i]-ablated_z[i+1])>step_thresh_z: #assuming vertical step size>step_thresh target mm
        rows.append(row)
        row = []

#add the final index to the last row and add the last row to the list of rows
row.append(range(len(ablated_z))[-1])
rows.append(row)

#sort by x
sorted_x = np.argsort(ablated_x)

#finds the smallest difference in x coordinates that is a real step (ie. greater than the threshold)
min_step_x = min((num for num in (ablated_x[sorted_x][i + 1] - ablated_x[sorted_x][i] for i in range(len(ablated_x[sorted_x]) - 1)) if num > step_thresh_x)) 

#iterate over sorted x indices except last one
for i in range(len(ablated_x)-1):
    #add the index to the column
    col.append(i)
    #if the horizontal distance to the next point is greater than the threshold, add the column to the list of columns and start a new column for the next index
    if np.abs(ablated_x[sorted_x][i]-ablated_x[sorted_x][i+1])>step_thresh_x: #assuming horizontal step size >step_thresh target mm
        cols.append(col)
        col = []
    
#accounting for the final index as with the rows:
col.append(range(len(ablated_x))[-1])
cols.append(col)

#initialize target and mirror grids
target_grid = [[None] * (len(cols)) for _ in range(len(rows))]
mirror_grid = [[None] * (len(cols)) for _ in range(len(rows))]

target_grid = []
mirror_grid = []

row_counter = 0

#Fill grid and add spacings row by row:
for row in rows:
    target_grid.append([None])
    mirror_grid.append([None])

    #sort columns within each row
    sorted_cols = np.argsort(ablated_x[row])
    ablated_x[row] = ablated_x[row][sorted_cols]
    ablated_z[row] = ablated_z[row][sorted_cols]
    mirror_x[row] = mirror_x[row][sorted_cols]
    mirror_z[row] = mirror_z[row][sorted_cols]
    order[row] = order[row][sorted_cols]

    #Take the first x value in the row (leftmost) and get horizontal spacing from the leftmost x value in any row 
    spacings = np.array([ablated_x[row][0]-np.min(ablated_x)])

    #Copy the row and get all of the follow horizontal spacings of the points
    row_copy = np.append(ablated_x[row][1:],0)
    spacings = np.append(spacings,np.abs(row_copy-ablated_x[row])[:-1])

    #Divide the spacings into the minimum spacing and round to the nearest integer
    #THIS ASSUMES ALL STEPS ARE INTEGER MULTIPLES OF THE SMALLEST STEP
    spacings = np.int32(np.round(spacings/min_step_x))

    spacing_counter = 0 #counts the total number of empty spaces in the row (in units of the min step x)
    for i in range(len(row)):
        #Loop over each coordinate in the row and add to the grids
        if len(row)==len(cols):
            #target_grid[row_counter][i] = [ablated_x[row][i], ablated_z[row][i]]
            #mirror_grid[row_counter][i] = [mirror_x[row][i], mirror_z[row][i]]

            target_grid[row_counter].append([ablated_x[row][i], ablated_z[row][i]])
            mirror_grid[row_counter].append([mirror_x[row][i], mirror_z[row][i]])

        
        #if there is empty space to the left of the current coordinate add the coordinate in the correct grid index:
        else:
            if int(spacings[i])>1:
                target_grid[row_counter].extend([None]*(spacings[i]-1))
                target_grid[row_counter].append(([ablated_x[row][i], ablated_z[row][i]]))

                mirror_grid[row_counter].extend([None]*(spacings[i]-1))
                mirror_grid[row_counter].append(([mirror_x[row][i], mirror_z[row][i]]))
            else:
                target_grid[row_counter].extend([None]*spacings[i])
                target_grid[row_counter].append(([ablated_x[row][i], ablated_z[row][i]]))

                mirror_grid[row_counter].extend([None]*spacings[i])
                mirror_grid[row_counter].append(([mirror_x[row][i], mirror_z[row][i]]))
            if int(spacings[i])>0:
                spacing_counter+=spacings[i]-1
    row_counter+=1

grid_center_x = int(len(target_grid)/2) + center_offset[0]
grid_center_z = int(len(target_grid[0])/2) + center_offset[1]

#print("Target grid:")
#print(visualize_coords(target_grid))
#-------Analyze the data---------

#spacings- consider an ordered traversal:
vert_step = []
horz_step = []
for r, row in enumerate(target_grid):
    for c, coord in enumerate(row):
        if coord == None: 
            continue
        found_bottom_neighbour = False
        found_right_neighbour = False
        if r==len(target_grid)-1:
            found_bottom_neighbour = True
        if c==len(row)-1:
            found_right_neighbour = True
        
        n_steps = 1 
        while not found_bottom_neighbour:
            if n_steps+r>len(target_grid)-1:
                break
            elif c>len(target_grid[r+n_steps])-1:
                n_steps+=1
                raise ValueError("WARNING: THE TARGET GRID ARRAY IS POORLY SHAPED")
            elif target_grid[r+n_steps][c] is not None:
                vert_step.append(np.linalg.norm(np.array(target_grid[r+n_steps][c]) - np.array(coord))/n_steps)
                found_bottom_neighbour = True
            else:
                n_steps+=1
        
        n_steps = 1
        while not found_right_neighbour:
            if n_steps+c>len(row)-1: 
                break
            elif target_grid[r][c+n_steps] is not None:
                horz_step.append(np.linalg.norm(np.array(target_grid[r][c+n_steps]) - np.array(coord))/n_steps)
                found_right_neighbour = True
            n_steps+=1




print("The average horizontal step is: "+ str(np.mean(horz_step)) + "mm")
print("The average vertical step is: "+ str(np.mean(vert_step)) + "mm")

target_to_mirror_x = step_x/np.mean(horz_step)
target_to_mirror_z = step_z/np.mean(vert_step)
print("The conversion factor in x is: "+ str(target_to_mirror_x) + " mirror mm/target mm")
print("The conversion factor in x is: "+ str(target_to_mirror_z) + " mirror mm/target mm")

target_displacement = np.array([target_grid[grid_center_x][grid_center_z][0],target_grid[grid_center_x][grid_center_z][1]]) - target_centroid #assumes target grid centered on target center
mirror_displacement = [target_displacement[0]*target_to_mirror_x,target_displacement[1]*target_to_mirror_z]
print("The center of the target is off by: " +str(target_displacement) + " target mm")
print("The center of the target is off by: " +str(mirror_displacement)+ " mirror mm")

writefile = 'Multi-Target Analysis.csv'
write_data = [targetID, str(np.mean(horz_step)),str(np.std(horz_step)), str(np.mean(vert_step)), str(np.std(vert_step)), str(target_to_mirror_x), str(target_to_mirror_z), str(mirror_center_x), str(mirror_center_z), str(mirror_displacement[0]), str(mirror_displacement[1])]
with open(writefile, 'a') as csvfile:
    csvwriter = csv.writer(csvfile,lineterminator='\n')
    csvwriter.writerow(write_data)



#print("Mirror grid:")
#print(visualize(mirror_grid))
#print("Target grid:")
#print(visualize_coords(target_grid))


