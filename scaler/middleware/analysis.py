import re
import numpy as np

test = open('test').read()
pressures = re.findall(r'pressureNum: (.*?)\n', test)
pressureIntervals = list()
for i in range(1,len(pressures)):
	pressureIntervals.append(float(pressures[i])-float(pressures[i-1]))
pressureIntervalArr = np.array(pressureIntervals)
pressureAvg = pressureIntervalArr.mean()
pressureStd = pressureIntervalArr.std()
print(len(pressures))
print(pressureAvg)
print(pressureStd)

conds = re.findall(r'condNum: (.*?)\n', test)
condIntervals = list()
for i in range(1,len(conds)):
	condIntervals.append(float(conds[i])-float(conds[i-1]))
condIntervalArr = np.array(condIntervals)
condAvg = condIntervalArr.mean()
condStd = condIntervalArr.std()
print(len(conds))
print(condAvg)
print(condStd)

curconds = re.findall(r'curCondNum: (.*?)\n', test)
curcondIntervals = list()
for i in range(1,len(curconds)):
	curcondIntervals.append(float(curconds[i])-float(curconds[i-1]))
curcondIntervalArr = np.array(curcondIntervals)
curcondAvg = curcondIntervalArr.mean()
curcondStd = curcondIntervalArr.std()
print(len(curconds))
print(curcondAvg)
print(curcondStd)