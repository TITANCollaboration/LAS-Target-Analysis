import numpy as np
import os 

def mirror_to_target(mirror_coords):
    """
    Converts from mirror coords to target coords
    """
    return np.array([mirror_coords[0]/0.0521,mirror_coords[1]/0.0725])
    
def target_to_mirror(target_coords):
    """
    Converts from target coords to mirror coords
    """
    return np.array([target_coords[0]*0.0521,target_coords[1]*0.0725])
                    
def parse_data(targetID,measurements_dir):
    """
    Parses ImageJ output and returns important parameters to pass to other functions. 

    @Params

    @return
    """
    os.chdir(measurements_dir)
    file = 'ImageJ_output\\'+targetID+ ' Measurements.csv'
    measurements = np.loadtxt(file, skiprows = 1, delimiter = ',')
    """
    Measurements are taken with the following column structure: 
    ID,Area,X,Y,Perim.,BX,BY,Width,Height,Major,Minor,Angle,Length

    The first three rows of measurements contain:
    - The unscaled full target ellipse
    - The scaled full target ellipse
    - A line measurement taken across a row to provide the angle of rotation
    """
     

    rotate_angle = measurements[2,11]/180*np.pi
    ablation_pos = measurements[3:,2:4]
    return ablation_pos, rotate_angle

def rotate(ablation_pos, theta):
    """
    Rotates a set of ablation positions by some angle theta

    @Params

    @return
    """
    rotation_matrix = np.array([[np.cos(theta), -1*np.sin(theta)],[np.sin(theta), np.cos(theta)]])
    return np.dot(ablation_pos, rotation_matrix.T)

def initialize_grid(ablation_pos,rotate_angle, step_thresh):
    """
    Initializes a grid of on-target ablation spot positions from measurements of a rectangular grid taken in imageJ. 
    Scans through a threshold range until the grid can be reconstructed properly. If the deviation 
    of the points in the grid is too large and the grid cannot be reconstructed for the given range of thresholds,
    an error will be thrown. 

    @Params:
    ablation_pos - 2D array of [x,z] ablation spot positions on the target from ImageJ measurement
    rotate_angle - angle taken from ImageJ measurement
    step thresh - array of scalars [step thresh x, step thresh z] the thresholds for the step sizes such that one step
    in a given direction is greater than the thresh 

    @return
    """

    #rotate the positions to straighten rows/cols
    ablation_pos = rotate(np.array(ablation_pos), rotate_angle)
    ablated_x = ablation_pos[3:,0]
    ablated_z = ablation_pos[3:,1]

    #Sorting all coordinates into a 2D grid

    #sort by z 
    sorted_z= np.argsort(ablated_z)
    ablated_x = ablated_x[sorted_z]
    ablated_z = ablated_z[sorted_z]
    cols = []
    col = []
    rows = []
    row = []
    row_length = 0 
    col_length = 0
    #iterating over sorted z indices except last one  
    for i in range(len(ablated_z)-1):
        #add the index to the row 
        row.append(i)
        #if the vertical distance to the next point is greater than the threshold, add the row to the list of rows and start a new row for the next index
        if np.abs(ablated_z[i]-ablated_z[i+1])>step_thresh[1]: #assuming vertical step size>step_thresh target mm
            if len(rows) == 0:
                row_length = len(row)
            if len(row)!=row_length and i<len(ablated_z)-2:
                raise ValueError("Attempting to build grid with non uniform row lenghts.")
            rows.append(row)
            row_length = len(row)
            row = []
    #add the final index to the last row and add the last row to the list of rows
    row.append(range(len(ablated_z))[-1])
    if len(row) != row_length:
        raise ValueError("Attempting to build grid with non uniform row lenghts.")
    rows.append(row)
    
    #sort by x
    sorted_x = np.argsort(ablated_x)

    #iterate over sorted x indices except last one
    for i in range(len(ablated_x)-1):
        #add the index to the column
        col.append(i)
        #if the horizontal distance to the next point is greater than the threshold, add the column to the list of columns and start a new column for the next index
        if np.abs(ablated_x[sorted_x][i]-ablated_x[sorted_x][i+1])>step_thresh[0]: #assuming horizontal step size >step_thresh target mm
            if len(cols) == 0:
                col_length = len(col)
            if len(col)!=col_length and i<len(ablated_x)-2:
                raise ValueError("Attempting to build grid with non-uniform column lengths")
            cols.append(col)
            col = []
        
    #accounting for the final index as with the rows:
    col.append(range(len(ablated_x))[-1])
    if len(col)!=col_length:
        raise ValueError("Attempting to build grid with non-uniform column lengths")
    cols.append(col)

    #initialize target and mirror grids
    target_grid = []
    row_counter = 0

    #Fill grid and add spacings row by row:
    for row in rows:
        target_grid.append([None]) #initialize an empty row

        #sort columns within each row
        sorted_cols = np.argsort(ablated_x[row])
        ablated_x[row] = ablated_x[row][sorted_cols]
        ablated_z[row] = ablated_z[row][sorted_cols]
        for i in range(len(row)):
            #Loop over each coordinate in the row and add to the grids
            target_grid[row_counter].append([ablated_x[row][i], ablated_z[row][i]])
        row_counter+=1
    return target_grid

def get_grid_spacing(target_grid):
    """

    @Params

    @return
    """
    vert_step = []
    horz_step = []

    for r, row in enumerate(target_grid):
        for c, coord in enumerate(row):
            vert_step.append(np.linalg.norm(np.array(target_grid[r+1][c]) - np.array(coord)))
            horz_step.append(np.linalg.norm(np.array(target_grid[r][c+1]) - np.array(coord)))





