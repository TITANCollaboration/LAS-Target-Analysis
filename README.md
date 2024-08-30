# LAS-Target-Analysis #

This repository contains code to analyze the post-ablation target data. 
## Repitition_Test.py ##
This script can be used to investigate the mirror positioning and step sizing variation for ablated targets that have been repeatedly ablated in the same pattern. 

## Target_Image_Anlaysis.py ##
This script takes the ablation measurements from ImageJ and the and determines the step sizes and conversion factor between mirror and target coordinates.

## data_plotter.py ## 
This script is used to generate plots for various targets and studies.

# Scope Plots

## DelayHistogramPlot
This script finds the edges of the laser TTL and Arduino pulse TTL and calculates the time between the two edges. It makes a histogram of the delay times and calculates some basic stats. The delay calculation is written in a for loop that looks through a directory to get all the scope files. You should put all relevant scope data files into a repository and then use the `os.chdir('path')` command to point the script to the directory with the data. The script then saves the plot to that folder, to see the file name enter it into the `plot.savefig('filename')` command located near the end of the script.

## PlotScopeData
This script simply plots the scope data. Use the full file path to the file in the variable called `filepath`.

## PulseShapeAnalysis
This script calculates the FWHM of a pulse and the rise and fall times. The rise time and fall time condition can be defined in the `crit` variable. This number gives the percent of full height to consider as the start and end of the rise or fall. For example: setting `crit = 0.10` will give you the time it takes for the pulse to go from 10% to 90% of it's full height. The script then plots the pulse, vertical lines where the `crit` cutoffs are and horizontal lines at the voltage corresponding to the `crit` values for both rise and fall times. The plot is then saved to the same folder as the data file.
