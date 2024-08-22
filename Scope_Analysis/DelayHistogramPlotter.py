import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

os.chdir(os.path.dirname(__file__))
os.chdir('20240821/20240821-output-from-switch')
delay = []

for f in os.listdir():
	if f[-3:] == 'CSV':
		data = pd.read_csv(f, sep=',', skiprows=15)

		dData = data.diff() # take 1-step "derivative" of scope trace to find edges

		edge_ch1 = dData['CH1'].idxmax() # find rising edge of laser TTL
		edge_ch2 = dData['CH2'].idxmin() # find falling edge of arduino TTL
		#if (data['TIME'][edge_ch2] - data['TIME'][edge_ch1])*1e6 < 9 or (data['TIME'][edge_ch2] - data['TIME'][edge_ch1])*1e6 >12:
		#	continue
		delay.append((data['TIME'][edge_ch2] - data['TIME'][edge_ch1])*1e6)
good = len(np.where(np.array(delay)<10.6)[0])
bad = len(np.where(np.array(delay)>=10.6)[0])
bad_ratio = (bad/(bad+good))
print(bad_ratio)
plt.figure('hist')												
plt.hist(delay, 12)
plt.xlim(9,12)
plt.xlabel('Pulse Delay (us)')
plt.annotate('mean: {0:.2f}us\nstd: {1:.2f}us\nrange: {2:.2f}us\nsamples: {3}'.format(np.mean(delay), np.std(delay), np.max(delay)-np.min(delay), len(delay)), (.95,.95), xycoords='axes fraction', fontsize=16, ha='right', va='top')
#plt.savefig('switch_signal_jitter_unfiltered.png')

#sanity check for edge finding
sanity = False
if not sanity:
	plt.figure('check edge')
	plt.plot(data['TIME'], data['CH1'], 'b')
	plt.plot(data['TIME'], data['CH2'], 'r')
	plt.vlines([data['TIME'][edge_ch1], data['TIME'][edge_ch2]], 0, 6, colors=['navy','firebrick'])

plt.show()