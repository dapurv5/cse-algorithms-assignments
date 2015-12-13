#!/usr/bin/env/python
#
# author: apurvverma@gatech.edu

import networkx as nx
import argparse
import random
import sys
import time
import os
import csv

import matplotlib.pyplot as plt
from pylab import *

def plot(X, Y, xlabel, ylabel, label):
  line, = plt.plot(X, Y, label=label, linewidth=2)
  plt.legend()
  plt.ylabel(ylabel)
  plt.xlabel(xlabel)  


def get_size_of_soln_at(t, f):
  with open(f, 'rb') as file:
    prev = file.readline()
    for curr in file:
      curr_time = float(curr.split(",")[0])
      if curr_time > t:
        break
      prev = curr
    return float(prev.split(",")[1])
  
#constructs the RTD graph using the multiple trace files
def main(folder):
  
  #opt_sol = 2203.0
  #t_min = 1.0
  #t_max = 70.0
  #t_step = 1.0
  
  opt_sol = 4542#2203.0
  t_min = 200.0#1.0
  t_max = 600.0#70.0
  t_step = 10.0#1.0
  
  #for q in [5.5, 6,7,10]:
  for q in [40,30, 20,15]:
    t_axis = []
    p_solve_axis = []
    t = t_min
    while t <= t_max:
      n = 0
      files = os.listdir(folder)
      for f in files:
        vc_found = get_size_of_soln_at(t, folder+"/"+f)
        sol_quality = (vc_found-opt_sol)/opt_sol * 100
        if sol_quality <= q:
          #print "file = ", f, "has reached q = ", q, "in time = ", t, sol_quality
          n = n + 1
      t_axis.append(t)
      p_solve_axis.append(float(n)/float(len(files)))
      t = t + t_step
    plot(t_axis, p_solve_axis, "time", "prob(solve)", str(q)+"%")    
  plt.show()

if __name__ == "__main__":
  #folder = "/home/dapurv5/Desktop/Semesters/1st_semester/CSEAlgorithms/Assignments/Project/output/power/trace_70"
  folder = "/home/dapurv5/Desktop/Semesters/1st_semester/CSEAlgorithms/Assignments/Project/output/star2/trace_20"
  main(folder)
  #print get_size_of_soln_at(4.48, folder+"/"+"power_SLS_100.trace")