import os
import numpy as np

itnums = np.array([])
itnums = np.append(itnums, np.arange(2017338, 2017001-1, -1))
itnums = np.append(itnums, np.arange(2016366, 2016001-1, -1))
itnums = np.append(itnums, np.arange(2015365, 2015001-1, -1))
itnums = np.append(itnums, np.arange(2014365, 2014001-1, -1))
itnums = np.append(itnums, np.arange(2013365, 2013001-1, -1))
itnums = np.append(itnums, np.arange(2012366, 2012320-1, -1))




for itnum in itnums:
    os.system('python insertWind.py ' + str(int(itnum)) + ' ' + str(int(itnum)) + ' 1')