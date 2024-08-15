import matplotlib.pyplot as plt
import pandas as pd
import os

filepath = 'pathToFile/filename.csv'

data = pd.read_csv(filename, sep=',', skiprows=15)

plt.plot(data['TIME'], data['CH1'])
plt.plot(data['TIME'], data['CH2'])
plt.show()
