import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

filepath = 'pathToFile/filename.csv'
signalChan = 'CH2' # 'CH1' for channel 1, 'CH2' for channel 2

data = pd.read_csv(filepath, sep=',', skiprows=15) # import scope data
data['TIME'] = (data['TIME'] - data['TIME'][0]) * 1e9 # set first time to 0 and convert to ns

dData = data.diff() # take 1-step "derivative" of scope trace to find edges

riseedge = dData[signalChan].idxmax() # find rising edge
falledge = dData[signalChan].idxmin() # find falling edge

# need all +ve values for height scale to work, so set low level baseline to 0V
baseline_low = np.mean(data[signalChan][falledge+25:riseedge-25])
data[signalChan] = data[signalChan] - baseline_low

# calculates the average signal level before and after pulse
baseline_pre = np.mean(data[signalChan][:falledge-50])
baseline_post = np.mean(data[signalChan][riseedge+50:])

crit = 0.1 # set rise and fall time criterion (0.1 would be 10% to 90% of pulse height)

# This block looks at the fall time. The iterator 'i' is used to step along the values
# find where pulse drops to high criteron
i = falledge -50
while data[signalChan][i] > (1-crit)*baseline_pre:
	i += 1
	continue
fallstart = data['TIME'][i]

# find where pulse drops to half
while data[signalChan][i] > 0.5*baseline_pre:
	i += 1
	continue
fallhalf = data['TIME'][i]

# find where pulse drops to low criteron
while data[signalChan][i] > crit*baseline_pre:
	i += 1
	continue
# calculat falltime
fallend = data['TIME'][i]
falltime = fallend - fallstart

i += 200 # skip to the middle-ish of the pulse

# find where pulse rises to low criteron
while data[signalChan][i] < crit*baseline_post:
	i += 1
	continue
risestart = data['TIME'][i]

# find where pulse rises to half
while data[signalChan][i] < 0.5*baseline_post:
	i += 1
	continue
risehalf = data['TIME'][i]

# find where pulse rises to high criteron
while data[signalChan][i] < (1-crit)*baseline_post:
	i += 1
	continue
# calculates risetime
riseend = data['TIME'][i]
risetime = riseend - risestart

# plot it up!
plt.plot(data['TIME'], data[signalChan])
plt.vlines([fallstart, fallend, risestart, riseend], 0, 350, ['r','r','b','b'])
plt.hlines([crit*baseline_pre, (1-crit)*baseline_pre, crit*baseline_post, (1-crit)*baseline_post], min(data['TIME']), max(data['TIME']), colors=['r','r','b','b'])
plt.annotate('criteria: 1/99\nFWHM: {0:.0f}ns\nfalltime: {1:.0f}ns\nrisetime: {2:.0f}ns'.format(risehalf - fallhalf, falltime, risetime), (.95,.15), xycoords='axes fraction', fontsize=16, ha='right', va='bottom')
plt.savefig('nameOfFileToSavePLot.png')
plt.show()
