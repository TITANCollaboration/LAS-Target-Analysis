import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

#os.chdir(os.path.dirname(__file__))
print('cwd:', os.getcwd())
os.chdir('20240814 Scope Data')

data = pd.read_csv('TEK00151.csv', sep=',', skiprows=15)
data['TIME'] = (data['TIME'] - data['TIME'][0]) * 1e9

dData = data.diff() # take 1-step "derivative" of scope trace to find edges

riseedge = dData['CH2'].idxmax() # find rising edge
falledge = dData['CH2'].idxmin() # find falling edge

baseline_low = np.mean(data['CH2'][falledge+25:riseedge-25])
data['CH2'] = data['CH2'] - baseline_low

baseline_pre = np.mean(data['CH2'][:falledge-50])
baseline_post = np.mean(data['CH2'][riseedge+50:])

crit = 0.01

i = falledge -50
while data['CH2'][i] > (1-crit)*baseline_pre:
	i += 1
	continue

fallstart = data['TIME'][i]

while data['CH2'][i] > 0.5*baseline_pre:
	i += 1
	continue
fallhalf = data['TIME'][i]

while data['CH2'][i] > crit*baseline_pre:
	i += 1
	continue

fallend = data['TIME'][i]
falltime = fallend - fallstart

i += 200
while data['CH2'][i] < crit*baseline_post:
	i += 1
	continue

risestart = data['TIME'][i]

while data['CH2'][i] < 0.5*baseline_post:
	i += 1
	continue
risehalf = data['TIME'][i]

while data['CH2'][i] < (1-crit)*baseline_post:
	i += 1
	continue
	
riseend = data['TIME'][i]
risetime = riseend - risestart

plt.plot(data['TIME'], data['CH2'])
plt.vlines([fallstart, fallend, risestart, riseend], 0, 350, ['r','r','b','b'])
plt.hlines([crit*baseline_pre, (1-crit)*baseline_pre, crit*baseline_post, (1-crit)*baseline_post], min(data['TIME']), max(data['TIME']), colors=['r','r','b','b'])
plt.annotate('criteria: 1/99\nFWHM: {0:.0f}ns\nfalltime: {1:.0f}ns\nrisetime: {2:.0f}ns'.format(risehalf - fallhalf, falltime, risetime), (.95,.15), xycoords='axes fraction', fontsize=16, ha='right', va='bottom')
plt.savefig('20240814_00151_PulseAnalysis1-99.png')
plt.show()