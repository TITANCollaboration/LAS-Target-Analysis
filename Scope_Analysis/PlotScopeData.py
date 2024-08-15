import matplotlib.pyplot as plt
import pandas as pd
import os

#os.chdir(os.path.dirname(__file__))
print(os.getcwd())
os.chdir('20240814 Scope Data')

data = pd.read_csv('TEK00151.csv', sep=',', skiprows=15)

plt.plot(data['TIME'], data['CH1'])
plt.plot(data['TIME'], data['CH2'])
plt.show()