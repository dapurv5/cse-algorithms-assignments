#!/usr/bin/python

import os
import matplotlib.pyplot as plt

filenames = ['0406', '0507', '0608', '0709', '0810', '0911', '1012', '1113', '1214', '1315', '1416', '1517', '1618']
edges = [65, 129, 260, 531, 1055, 2184, 4412, 9876, 29780, 106362, 372671, 1770678, 7926935]
vertices = [16,32,64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]

path_prefix = "/home/dapurv5/Desktop/Semesters/1st_semester/CSEAlgorithms/Assignments/Assignment1/MST/results"


static_times = []
dynamic_times = []
for file in filenames:
  with open(path_prefix + "/rmat" + file + ".out", 'r') as output:
    line = output.readline().strip('\n')
    static_times.append(float (line.split(" ")[1]))
    sum = 0
    for i in range(100):
      line = output.readline().strip('\n')
      t = float (line.split(" ")[1])
      sum += t
    dynamic_times.append(sum)
    
print static_times
#print dynamic_times
#plt.plot(static_times, edges)
plt.plot(dynamic_times, vertices)
plt.ylabel('time')
plt.xlabel('number of vertices')
plt.show()