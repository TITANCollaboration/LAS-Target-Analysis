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
    targetID (string) - the target ID used to designate the specific target photo. Eg. Cu_02. Can take the form Cu_02_02 if two or more photos of Cu_02 were taken
    measurements_dir (pathlike, string) - the parent directory of the ImageJ_output folder containing all of the ImageJ measurements for each target
    @return
    ablation_pos (array) - the ablation spot centroid positions from the ImageJ measurement. 
    rotate_angle (float) - the angle to rotate the ablation positions to best align the positions measured into a horizontal/vertical grid. 
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
    ablation_pos (arraylike) - the positions to rotate
    theta (float) - the amount of rotation in degrees (rotate clockwise)
    @return
    The rotated ablation spot postiitons rotated clockwise by theta.
    """
    rotation_matrix = np.array([[np.cos(theta), -1*np.sin(theta)],[np.sin(theta), np.cos(theta)]])
    return np.dot(ablation_pos, rotation_matrix.T)

def initialize_grid(ablation_pos,rotate_angle, shape):
    """
    Initializes a grid of on-target ablation spot positions from measurements of a rectangular grid taken in imageJ. 
    Scans through a threshold range until the grid can be reconstructed properly. If the deviation 
    of the points in the grid is too large and the grid cannot be reconstructed for the given range of thresholds,
    an error will be thrown. 

    @Params:
    ablation_pos - 2D array of [x,z] ablation spot positions on the target from ImageJ measurement
    rotate_angle - angle taken from ImageJ measurement
    shape (tuple)- The shape of the grid of points taken -(#rows, #cols)
    @return
    """

    #rotate the positions to straighten rows/cols
    ablation_pos = rotate(np.array(ablation_pos), rotate_angle)
    print(ablation_pos)
    #Sorting all coordinates into the 2D grid
    target_grid = []
    for i in range(shape[0]):
        target_grid.append(ablation_pos[shape[1]*i:shape[1]*i+shape[1]])
    return target_grid

def get_grid_spacing(target_grid):
    """
    @Params
    target_grid (arraylike) - the ablation coordinates stored in a 2D array mimicing their real relative positions
    @return
    horz_step (list) - all horizontal spacings between adjacent ablation grid coordinates 
    vert_step (list) - all vertical spacings between adjacent ablation grid coordinates 
    """
    vert_step = []
    horz_step = []

    for r, row in enumerate(target_grid):
        if r == 0:
                continue
        for c, coord in enumerate(row):
            if c == 0:
                continue
            vert_step.append(np.linalg.norm(np.array(target_grid[r-1][c]) - np.array(coord)))
            horz_step.append(np.linalg.norm(np.array(target_grid[r][c-1]) - np.array(coord)))
    return horz_step, vert_step

def main():
    """
    To use this analysis code first specify the directory of the imageJ output folder, then call parse_data with the specific target to be analyzed, then call
    initialize_grid and get_grid_spacings to get the ablation coordinates and spacings.
    """
    dir = os.path.dirname(os.path.abspath(__file__))
    ablation_pos, rotate_angle = parse_data("Cu_17", dir)
    target_grid = initialize_grid(ablation_pos,rotate_angle, (5,5))
    horz_step, vert_step = get_grid_spacing(target_grid)
    print("The average horizontal step is: "+ str(np.mean(horz_step)) + "mm")
    print("The average vertical step is: "+ str(np.mean(vert_step)) + "mm")
    print("The std in horizontal step is: "+ str(np.std(horz_step)) + "mm")
    print("The std in vertical step is: "+ str(np.std(vert_step)) + "mm")
    

#call main()
main()




