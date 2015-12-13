#!/usr/bin/python
#
# author: apurvverma@gatech.edu

import argparse
import time


def linear_search(arr, l, m, h):
  curr_sum = 0
  i = m
  best_sum_left = 0
  best_i = m
  while i >= l:
    curr_sum += arr[i]
    if curr_sum > best_sum_left:
      best_sum_left = curr_sum
      best_i = i
    i -= 1
      
  curr_sum = 0
  j = m+1
  best_sum_right = 0
  best_j = m+1
  while j <= h:
    curr_sum += arr[j]
    if curr_sum > best_sum_right:
      best_sum_right = curr_sum
      best_j = j
    j += 1
      
  if best_sum_right == 0 or best_sum_left == 0:
    return 0,-1,-1
  return best_i, best_j, best_sum_left+best_sum_right


def dc_(arr, l, h):
  if l == h:
    return l,h, arr[l]
  
  m = (l+h)/2
  left_i, left_j, left = dc_(arr, l, m)
  right_i, right_j, right = dc_(arr, m+1, h)
  crossover_i, crossover_j, crossover = linear_search(arr, l, m, h)
  maximum = max(left, right, crossover)
  if maximum == left:
    return left_i, left_j, left
  elif maximum == right:
    return right_i, right_j, right
  else:
    return crossover_i, crossover_j, crossover
  
def dc(arr):
  return dc_(arr, 0, len(arr)-1)

def dp(arr):
  B = [0] * (len(arr)+1)
  B[0] = 0
  best_i = 0
  best_j = 0
  best = 0
  
  for j in range(1, len(B)):
    B[j] = max(0, B[j-1] + arr[j-1]) 
  
  for j in range(1, len(B)):
    if B[j] > best:
      best = B[j]
      best_j = j
  
  best_i = best_j
  while B[best_i] > 0:
    best_i-=1
  
  best_i += 1
  return best_i, best_j, best
    

def main(args):
  with open(args.input, 'r') as input:
    line = input.readline()
    line = line.strip('\n')
    line = line.split(",")
    n = int(line[0])
    k = int(line[1])
    for line in input:
      start_time = time.time()
      line = line.strip('\n')
      arr = line.split(',')
      fl = lambda x: float(x)
      arr = map(fl, arr)
            
      if args.algorithm == 'dc':
        best_i, best_j, best = dc(arr)
        best_i += 1
        best_j += 1
      elif args.algorithm == 'dp':
        best_i, best_j, best = dp(arr)
      end_time = time.time()
      elapsed_time = (end_time - start_time)*1000
      print "{best}, {best_i}, {best_j}, {elapsed_time}".format(best=best, best_i=best_i, best_j=best_j, elapsed_time=elapsed_time)

#python max_profit.py --input /home/dapurv5/Desktop/Semesters/1st_semester/CSEAlgorithms/Assignments/Assignment3/hw3/hw3/data/10.txt --algorithm dp
if __name__=="__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--input',help='path to the input file',required=True)
  parser.add_argument('--algorithm',help='the algorithm, dc or dp',required=True)
  args = parser.parse_args()
  main(args)