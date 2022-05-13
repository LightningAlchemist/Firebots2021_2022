import numpy as np
import pandas as pd
import matplotlib as plt

arduinoFile = pd.read_csv("C:/Users/josep/OneDrive/Documents/UniversityofWashington/SeniorProject/BrianValidation/LEDValidation/LedVal5.csv")
brianFile = pd.read_csv("C:/Users/josep/OneDrive/Documents/UniversityofWashington/SeniorProject/BrianValidation/RobotValidation/robotVal2.csv")

print(type(arduinoFile))
print(arduinoFile.head())
print()

fig = plt.figure()
ax = plt.axes()

