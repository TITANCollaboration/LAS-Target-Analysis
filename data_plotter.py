import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import os
import pandas as pd
import math
import matplotlib.colors as mcolors
from matplotlib.patches import Ellipse

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
# 2024-04-30_Al_01 data 
dir = '2024-04-30_Al_01'
file = 'data\\'+dir+"\\initial_charge_per_pulse.csv"

charge_pulse_Al_01 = np.loadtxt(file, delimiter = ',', skiprows = 1)
#laser moved to new spot after the first 14 datapoints collected
num_pulses_01  = charge_pulse_Al_01[:14,0] 
num_pulses_02 = charge_pulse_Al_01[14:,0]
charge_01 = charge_pulse_Al_01[:14, 1]
charge_02 = charge_pulse_Al_01[14:,1] 

charge_per_pulse_01 = charge_01/num_pulses_01 
charge_per_pulse_02 = charge_02/num_pulses_02

#print(np.mean(charge_per_pulse_01))
#print(np.mean(charge_per_pulse_02))
#print(np.std(charge_per_pulse_01))
#print(np.std(charge_per_pulse_02))

print("The mean charge/pulse (nC) is: ")
print(np.mean(np.append(charge_per_pulse_01,charge_per_pulse_02)))

print("The normalized standard deviation in charge/pulse (nC) is: ")
print(np.std(np.append(charge_per_pulse_01,charge_per_pulse_02))/np.mean(np.append(charge_per_pulse_01,charge_per_pulse_02)))

file = 'data\\'+dir+"\\Ion_current_laser_focus_pos.csv"

laser_focus = np.loadtxt(file, skiprows = 1, delimiter=',')
focal_lens_pos = laser_focus[:,0]
current_01 = laser_focus[:,1]
plt.figure()
plt.xlabel('Current (pA)')
plt.ylabel('Focal lens position (mm)')
plt.title('Laser Focus Scan')
plt.scatter(focal_lens_pos, current_01)
plt.close()

#2024-04-30_Cu_02 data
dir = '2024-04-30_Cu_02'
file = 'data\\'+dir+"\\MirrorZ_vs_charge.csv"
zScan = np.loadtxt(file, skiprows =1, delimiter = ',')
plt.figure()
plt.ylabel('Charge (nC)')
plt.xlabel('Z position (mirror mm)')
plt.title('Charge Across Vertical')
plt.scatter(zScan[:,0], zScan[:,1])
plt.close()

#2024-05-01_Cu_02 data
dir = '2024-05-01_Cu_02'
file = 'data\\'+dir+"\\Charge_per_Pulse.csv"
charge_pulse_Cu_02 = np.loadtxt(file, skiprows =1, delimiter = ',')

#laser position moved after first three datapoints
num_pulses_03  = charge_pulse_Cu_02[:3,0] 
num_pulses_04 = charge_pulse_Cu_02[3:,0]
charge_03 = charge_pulse_Cu_02[:3, 1]
charge_04 = charge_pulse_Cu_02[3:,1] 

charge_per_pulse_03 = charge_03/num_pulses_03
charge_per_pulse_04 = charge_04/num_pulses_04

print("The mean charge/pulse (nC) is: ")
print(np.mean(np.append(charge_per_pulse_03,charge_per_pulse_04)))

print("The normalized standard deviation in charge/pulse (nC) is: ")
print(np.std(np.append(charge_per_pulse_03,charge_per_pulse_04))/np.mean(np.append(charge_per_pulse_03,charge_per_pulse_04)))

file = 'data\\'+dir+"\\Target_degredation_new_spot.csv"
target_degredation_01 = np.loadtxt(file, skiprows =1, delimiter = ',')
total_pulses_01 = target_degredation_01[:,0]
charge_per_pulse_05 = target_degredation_01[:,1]/500*1000

print("The mean charge/pulse (pC) is: ")
print(np.mean(charge_per_pulse_05))

print("The normalized standard deviation in charge/pulse (pC) is: ")
print(np.std(charge_per_pulse_05)/np.mean(charge_per_pulse_05))

plt.figure()
plt.ylabel('Charge per Pulse (pC)')
plt.xlabel('Total Pulses')
plt.title('Target Degredation')
plt.scatter(total_pulses_01, charge_per_pulse_05)
plt.savefig(file[:-4]+'_plot.png')
plt.close()

file = 'data\\'+dir+"\\Target_degredation.csv"
target_degredation_02 = np.loadtxt(file, skiprows =1, delimiter = ',')
total_pulses_02 = target_degredation_02[:,0]
charge_per_pulse_06 = target_degredation_02[:,1]

print("The mean charge/pulse (pC) is: ")
print(np.mean(charge_per_pulse_06))

print("The normalized standard deviation in charge/pulse (pC) is: ")
print(np.std(charge_per_pulse_06)/np.mean(charge_per_pulse_06))

plt.figure()
plt.ylabel('Charge per Pulse (pC)')
plt.xlabel('Total Pulses')
plt.title('Target Degredation')
plt.scatter(total_pulses_02, charge_per_pulse_06)
plt.savefig(file[:-4]+'_plot.png')
plt.close()

#2024-05-01_CuAl_03 Data
dir = '2024-05-01_CuAl_03'
file = 'data\\'+dir+"\\Energy_scan.csv"
energy_scan = np.loadtxt(file, skiprows =2, delimiter = ',')

plt.figure()
plt.ylabel('Charge per Pulse (pC)', fontsize = 'large')
plt.xlabel('Retarding Electrode Potential (kV)', fontsize = 'large')
plt.title('Ion Energy')
plt.scatter(energy_scan[:,0]/1000,energy_scan[:,1]/100*1000)
plt.ylim(bottom = 0)
plt.savefig(file[:-4]+'_plot.png')
plt.close()

file = 'data\\'+dir+"\\Laser_Power.csv"

laser_power_rep_rate = np.loadtxt(file, skiprows =2, delimiter = ',')

plt.figure()
plt.ylabel('Laser Power ($\mu$J)', fontsize = 'large')
plt.xlabel('Laser Pulse Repetition Rate (Hz)', fontsize = 'large')
plt.title('Laser Power at Various Repetition Rates', )
plt.scatter(laser_power_rep_rate[:,0],laser_power_rep_rate[:,1])
plt.savefig(file[:-4]+'_plot.png')
plt.close()

file = 'data\\'+dir+"\\Mirror_X_vs_charge_mid.csv"

charge_mid_CuAl_03 = np.loadtxt(file, skiprows=1, delimiter = ',')
charge_07 = charge_mid_CuAl_03[:,2]
mirror_x_CuAl_03_mid = charge_mid_CuAl_03[:,0]
charge_per_pulse_07 = charge_07/200
plt.figure()
plt.ylabel('Charge per pulse (nC)')
plt.xlabel('Mirror x (mm)')
plt.title('CuAl_03 mid scan')
plt.scatter(mirror_x_CuAl_03_mid,charge_per_pulse_07)
plt.close()

file = 'data\\'+dir+"\\Mirror_X_vs_charge_high.csv"

charge_high_CuAl_03 = np.loadtxt(file, skiprows=1, delimiter = ',')
charge_08 = charge_high_CuAl_03[:,1]
mirror_x_CuAl_03_high = charge_high_CuAl_03[:,0]
charge_per_pulse_08 = charge_08/200*1000
plt.figure()
plt.ylabel('Charge per pulse (pC)')
plt.xlabel('Mirror x (mm)')
plt.title('CuAl_03 high scan')
plt.scatter(mirror_x_CuAl_03_high,charge_per_pulse_08)
plt.close()

file = 'data\\'+dir+"\\Mirror_X_vs_charge_low.csv"

charge_low_CuAl_03 = np.loadtxt(file, skiprows=1, delimiter = ',')
charge_09 = charge_low_CuAl_03[:,1]
mirror_x_CuAl_03_low = charge_low_CuAl_03[:,0]
charge_per_pulse_09 = charge_09/200*1000
plt.figure()
plt.ylabel('Charge per pulse (pC)')
plt.xlabel('Mirror x (mm)')
plt.title('CuAl_03 low scan')
plt.scatter(mirror_x_CuAl_03_low,charge_per_pulse_09)
plt.close()

file = 'data\\'+dir+"\\Rep_rate_nplc_low.csv"

rep_rate_nplc_low = np.loadtxt(file, skiprows=2, delimiter = ',')

plt.figure()
plt.ylabel('Charge per pulse (pC)', fontsize = 'large')
plt.xlabel('Laser Pulse Repetition Rate (Hz)', fontsize = 'large')
plt.title('Charge per Pulse at Various Laser Pulse Rates')
plt.scatter(rep_rate_nplc_low[:, 0],(rep_rate_nplc_low[:,1]+rep_rate_nplc_low[:,2])/2*10)
plt.savefig(file[:-4]+'_plot.png')
plt.close()

file = 'data\\'+dir+"\\Rep_rate_nplc_med.csv"

rep_rate_nplc_med = np.loadtxt(file, skiprows=2, delimiter = ',')

plt.figure()
plt.ylabel('Charge per pulse (pC)')
plt.xlabel('Laser Pulse Repetition Rate (Hz)')
plt.title('Laser Pulse Repetition Rate nplc med')
plt.scatter(rep_rate_nplc_med[:, 0],rep_rate_nplc_med[:,1])
plt.savefig(file[:-4]+'_plot.png')
plt.close()

plt.figure()
plt.ylabel('Charge per pulse (pC)', fontsize = 'large')
plt.xlabel('Laser Pulse Repetition Rate (Hz)', fontsize = 'large')
plt.title('Charge per Laser Pulse at Various Repetition Rates')
plt.scatter(rep_rate_nplc_med[:, 0],rep_rate_nplc_med[:,1]*10,label = 'nplc = med')
plt.scatter(rep_rate_nplc_low[:, 0],(rep_rate_nplc_low[:,1]+rep_rate_nplc_low[:,2])/2*10, label = "nplc = low")
plt.legend()
plt.savefig('data\\'+dir+'\\Rep_rate_charge_plot.png')
plt.close()

file = 'data\\'+dir+"\\small_grid_charge.csv"

small_grid_charge = np.loadtxt(file, skiprows=1, delimiter = ',')
mirror_x_CuAl_03_small_grid = small_grid_charge[0,1:]
mirror_z_CuAl_03_small_grid = small_grid_charge[1:,0]
mirror_x_coords_CuAl_03_small_grid = []
mirror_z_coords_CuAl_03_small_grid = []
charge_CuAl_03_small_grid = []
for i, row in enumerate(small_grid_charge[1:,1:]):
    for j, charge in enumerate(row):
        mirror_x_coords_CuAl_03_small_grid.append(mirror_x_CuAl_03_small_grid[i])
        mirror_z_coords_CuAl_03_small_grid.append(mirror_z_CuAl_03_small_grid[j])
        charge_CuAl_03_small_grid.append(charge)



plt.figure()
plt.ylabel('Mirror Z pos (mm)')
plt.xlabel('Mirror X pos (mm)')
plt.title('CuAl_03 Small grid')
CuAl_03_small_grid_plot = plt.scatter(mirror_x_coords_CuAl_03_small_grid,mirror_z_coords_CuAl_03_small_grid, c= charge_CuAl_03_small_grid, s = 200)
colorbar = plt.colorbar(CuAl_03_small_grid_plot)
colorbar.set_label('Charge (nC)') 
plt.close()


#2024-05-02_CuAl_04 data

dir = '2024-05-02_CuAl_04'
file = 'data\\'+dir+"\\MirrorX_scan_bot.csv"

charge_bot_CuAl_04 = np.loadtxt(file, skiprows=2, delimiter = ',')
charge_10 = charge_bot_CuAl_04[:,1]
mirror_x_CuAl_04_bot = charge_bot_CuAl_04[:,0]
charge_per_pulse_10 = charge_10/200
plt.figure()
plt.ylabel('Charge per pulse (nC)')
plt.xlabel('Mirror x (mm)')
plt.title('CuAl_04 bot scan')
plt.scatter(mirror_x_CuAl_04_bot,charge_per_pulse_10)
plt.close()

file = 'data\\'+dir+"\\MirrorX_scan_mid.csv"

charge_mid_CuAl_04 = np.loadtxt(file, skiprows=2, delimiter = ',')
charge_11 = charge_mid_CuAl_04[:,1]
mirror_x_CuAl_04_mid = charge_mid_CuAl_04[:,0]
charge_per_pulse_11 = charge_11/200
plt.figure()
plt.ylabel('Charge per pulse (nC)')
plt.xlabel('Mirror x (mm)')
plt.title('CuAl_04 mid scan')
plt.scatter(mirror_x_CuAl_04_mid,charge_per_pulse_11)
plt.close()

file = 'data\\'+dir+"\\MirrorX_scan_top.csv"

charge_top_CuAl_04 = np.loadtxt(file, skiprows=2, delimiter = ',')
charge_12 = charge_top_CuAl_04[:,1]
mirror_x_CuAl_04_top = charge_top_CuAl_04[:,0]
charge_per_pulse_12 = charge_12/200
plt.figure()
plt.ylabel('Charge per pulse (nC)')
plt.xlabel('Mirror x (mm)')
plt.title('CuAl_04 top scan')
plt.scatter(mirror_x_CuAl_04_top,charge_per_pulse_12)
plt.close()


file = 'data\\'+dir+"\\MirrorZ_scan.csv"

charge_z_CuAl_04 = np.loadtxt(file, skiprows=3, delimiter = ',')
charge_13 = charge_z_CuAl_04[:,1]
mirror_x_CuAl_04_z = charge_z_CuAl_04[:,0]
charge_per_pulse_13 = charge_13/200
plt.figure()
plt.ylabel('Charge per pulse (nC)')
plt.xlabel('Mirror z (mm)')
plt.title('CuAl_04 z scan')
plt.scatter(mirror_x_CuAl_04_z,charge_per_pulse_13)
plt.close()

#2024-05-02_Al_05 data

#2024-05-03_CuAl_06 data
dir = '2024-05-03_CuAl_06'
file = 'data\\'+dir+"\\Center_grid_charge.csv"
grid_data_CuAl_06 = np.loadtxt(file, delimiter = ',')

x_values = grid_data_CuAl_06[0,1:]
z_values = grid_data_CuAl_06[1:,0]
charge_CuAl_06 = grid_data_CuAl_06[1:,1:]/200*1000

X, Z = np.meshgrid(x_values, z_values)

# Plot the grid values
plt.figure()
plt.contourf(X, Z, charge_CuAl_06, cmap=cm.viridis, levels = 8)
plt.colorbar(label='Charge per pulse (pC)', fontsize = 'large')

plt.xlabel('Mirror X position (mm)', fontsize = 'large')
plt.ylabel('Mirror Z position (mm)', fontsize = 'large')
plt.title('Aluminum Strip Target')
plt.gca().invert_yaxis()
plt.gca().set_aspect(1)
plt.savefig(file[:-4]+'_plot.png')
plt.close()

plt.figure()
plt.imshow(charge_CuAl_06, extent=[x_values[0], x_values[-1], z_values[0], z_values[-1]])
plt.colorbar(label='Charge per pulse (pC)')
plt.gca().set_aspect(2)
plt.close()





#2024-05-02_CuAl_13 data
dir = '2024-05-22_CuAl_13'
file = 'data\\'+dir+"\\Charge_grid.csv"
grid_data_CuAl_13 = np.loadtxt(file, delimiter = ',')

x_values = grid_data_CuAl_13[0,1:]
z_values = grid_data_CuAl_13[1:,0]
charge_CuAl_13 = grid_data_CuAl_13[1:,1:]/200

X, Z = np.meshgrid(x_values, z_values)

# Plot the grid values
plt.figure()
plt.contourf(X, Z, charge_CuAl_13, cmap=cm.viridis, levels = 50)
plt.colorbar(label='Charge per pulse (nC)', fontsize = 'large')

plt.xlabel('Mirror X position (mm)', fontsize = 'large')
plt.ylabel('Mirror Z position (mm)', fontsize = 'large')
plt.title('Toonie Target')
plt.close()

plt.figure()
plt.imshow(charge_CuAl_13, extent=[x_values[0], x_values[-1], z_values[0], z_values[-1]])
plt.colorbar(label='Charge per pulse (nC)')
plt.savefig(file[:-4]+'_plot.png')
plt.close()


file = 'data\\'+dir+"\\Charge_grid_circle.csv"
grid_data_CuAl_13 = np.loadtxt(file, delimiter = ',')/200*1000

x_values = np.arange(5.745, 5.971, 0.045)
z_values = np.arange(4.48, 4.841, 0.04)

X, Z = np.meshgrid(x_values, z_values)

# Plot the grid values
plt.figure()
plt.contourf(X, Z, grid_data_CuAl_13, cmap=cm.viridis, levels = 20)
plt.colorbar(label='Charge per pulse (pC)', fontsize = 'large')
plt.xlabel('Mirror X position (mm)', fontsize = 'large')
plt.ylabel('Mirror Z position (mm)', fontsize = 'large')
plt.title('Al Cu Toonie Target Center')
plt.gca().invert_yaxis()
plt.savefig(file[:-4]+'_plot.png')
plt.close()

plt.figure()
plt.imshow(grid_data_CuAl_13, extent=[x_values[0], x_values[-1], z_values[0], z_values[-1]])
plt.colorbar(label='Charge per pulse (nC)')
plt.close()


#2024-05-23_CuAl_14 data
dir = '2024-05-23_CuAl_14'
file = 'data\\'+dir+"\\Charge_grid.csv"
grid_data_CuAl_14 = np.loadtxt(file, delimiter = ',')

x_values = grid_data_CuAl_14[0,1:]
z_values = grid_data_CuAl_14[1:,0]
charge_CuAl_14 = grid_data_CuAl_14[1:,1:]/200*1000

X, Z = np.meshgrid(x_values, z_values)

plt.figure()
plt.contourf(X, Z, charge_CuAl_14, cmap=cm.viridis)
plt.colorbar(label='Charge per pulse (pC)')
plt.xlabel('Mirror X position (mm)', fontsize = 'large')
plt.ylabel('Mirror Z position (mm)', fontsize  = 'large')
plt.title('Toonie Target')
plt.gca().invert_yaxis()
plt.savefig(file[:-4]+'_contour_plot.png')
plt.close()


#imshow
thresh = 0.08
cmap = plt.cm.viridis
norm = mcolors.Normalize(vmin=thresh, vmax=charge_CuAl_14.max())

# Create a masked array where values below the threshold are masked
masked_data = np.ma.masked_less(charge_CuAl_14, thresh)
fig, ax = plt.subplots()

# Display the image with the masked data
cmap.set_bad(color='black')  # Set color for masked values
cax = ax.imshow(masked_data,extent=[x_values[0], x_values[-1], z_values[-1], z_values[0]], cmap=cmap, norm=norm)

# Add a colorbar
fig.colorbar(cax)
ax.set_aspect(0.736)
ellipse = Ellipse(xy=(5.86,4.658), width=0.53, height=0.72, angle=0, edgecolor='red', facecolor='none', linewidth=2)

# Add the ellipse to the axes
ax.add_patch(ellipse)
plt.savefig(file[:-4]+'_imshow_plot.png')

plt.close()



plt.show()

