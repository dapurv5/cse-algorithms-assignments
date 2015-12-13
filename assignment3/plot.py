#!/usr/bin/python

import os
import matplotlib.pyplot as plt

filenames = ['10', '1000', '2000', '3000', '4000', '5000', '6000', '7000', '8000', '9000', '10000']

path_prefix = "/home/dapurv5/Desktop/Semesters/1st_semester/CSEAlgorithms/Assignments/Assignment3/hw3/hw3/output"


sizes = []
times_dc = []
times_dp = []

for file in filenames:
  sizes.append(float(file))
  sum = 0
  count = 0
  with open(path_prefix + "/averma80_output_dc_" + file + ".txt", 'r') as output:
    for line in output:
      line = line.strip('\n')
      time = float(line.strip(" ").split(",")[-1])
      sum += time
      count += 1
    times_dc.append(sum/count)
    
  with open(path_prefix + "/averma80_output_dp_" + file + ".txt", 'r') as output:
    for line in output:
      line = line.strip('\n')
      time = float(line.strip(" ").split(",")[-1])
      sum += time
      count += 1
    times_dp.append(sum/count)

print times_dc
print times_dp
print sizes
plt.plot(sizes, times_dc)
plt.plot(sizes, times_dp)
plt.ylabel('time in ms')
plt.xlabel('size')
plt.show()
