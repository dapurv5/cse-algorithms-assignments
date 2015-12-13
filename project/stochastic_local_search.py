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

from timeout import TimeoutError
from timeout import timeout

INITIAL_WEIGHT = 0.05

class SLSVertexCover():
  """Stochastic Local Search algorithm to find vertex cover"""

  def __init__(self, graph, seed):
    self.graph_cpy = graph
    self.total_edges = graph.number_of_edges()
    self.total_vertices = len(graph)    
    self.best_vertex_cover = set() #best vertex cover found so far
    self.seed = seed
    self.reset()
    
  def reset(self):
    """to be called before any new search begins"""
    self.tabu = [] #tabu of size 3
    self.graph = self.graph_cpy.copy()
    self.uncovered_edges = self.graph.copy()
    random.seed(self.seed)

  def get_current_best_solution(self):
    """Returns the current best vertex cover found so far"""
    return self.best_vertex_cover
  
  def reached_a_vertex_cover(self):
    """Is the current solution a complete vertex cover"""
    return self.uncovered_edges.number_of_edges() == 0
    
  def compute_vertex_cover_with_timeout(self, cutoff):
    try:
      with timeout(seconds=cutoff):
        self.compute_vertex_cover()
    except TimeoutError as e:
      pass
    return self.get_current_best_solution()
    
  def importance(self, u):
    """the imp of a vertex is the sum of difficulty of its adjacent edges"""
    imp = 0
    for v, dict in self.graph[u].items():
      imp = imp + dict['weight']
    return imp

  def add_vertex_to_cover(self, u, vc):
    vc.add(u)
    self.uncovered_edges.remove_node(u)
  
  def update_weights(self, delta):
    for (u,v,dict) in self.uncovered_edges.edges(data=True):
      old_weight = dict['weight']
      self.graph.add_weighted_edges_from([(u, v, old_weight+delta)])
  
  def remove_vertex_from_cover(self, u, vc):
    vc.remove(u)
    for v, dict in self.graph[u].items():      
      if v not in vc:
        #there is neither vertex u nor v to cover edge (u,v)
        #edge (u,v) is no longer covered by any vertex
        weight = self.graph[u][v]['weight']
        self.uncovered_edges.add_weighted_edges_from([(u,v, weight)])

  def compute_greedy_initial_vertex_cover(self):
    """greedily constructs the vertex cover by choosing vertices with highest degrees first"""
    vc = set()
    vertices = list(self.graph.nodes(data=False))
    imp = {}
    for vertex in vertices:
      imp[vertex] = self.importance(vertex)
    vertices = sorted(vertices, key = lambda (v): imp[v], reverse=True)
    for vertex in vertices:
      self.add_vertex_to_cover(vertex, vc)
      if self.reached_a_vertex_cover():
        break
    #a bit of randomization in the initial solution
    extra_vertices = random.sample(vertices, len(vertices)/100)
    for vertex in extra_vertices:
      if vertex in vc:
        continue
      self.add_vertex_to_cover(vertex, vc)
    return vc

  def get_random_uncovered_edge(self):
    """Returns a quasi random edge from the uncovered edges graph"""
    #pick a random uncovered edge (u,v), this is done in two steps.
    nbrs = []
    while len(nbrs) == 0:
      vertices = self.uncovered_edges.nodes(data=False)
      u = random.sample(vertices, 1)[0] #(1)get a random src vertex
      nbrs = self.uncovered_edges.neighbors(u)
      #the adjacency of this node, u, is empty (better delete it)
      if len(nbrs) == 0:
        self.uncovered_edges.remove_node(u)
    #(2) get a random dest. vertex from the adjacency of u
    v = random.sample(nbrs, 1)[0]
    return u,v


  def get_vertex_to_add(self, vc):
    u,v = self.get_random_uncovered_edge()
    #determine which vertex to include in cover
    weight_u = self.importance(u)
    weight_v = self.importance(v)
    return v if weight_u < weight_v else u


  def get_vertex_to_remove(self, vc):
    #determine which vertex to remove from cover
    w = -1
    weight_w = sys.maxint
    for vertex in vc:
      if self.importance(vertex) < weight_w:
        w = vertex
        weight_w = self.importance(vertex)
    return w


  def compute_vertex_cover(self):
    #construct an initial vertex cover greedily
    self.reset()
    vc = self.compute_greedy_initial_vertex_cover()
    k = len(vc)
    self.best_vertex_cover = vc.copy()
    while k > 0:
      k = k - 1 #try to find a better vertex cover
      #remove 1 vertex randomly from the vc found previously
      vertices_to_remove = random.sample(vc, 1)
      for vertex in vertices_to_remove:
        self.remove_vertex_from_cover(vertex, vc)
      
      vc = self.compute_vertex_cover_of_size(vc)
      if len(vc) < len(self.best_vertex_cover):
        self.best_vertex_cover = vc.copy()
        write_trace(self.best_vertex_cover)

  

  def compute_vertex_cover_of_size(self, vc):
    iter = 0
    while True:
      iter = iter + 1 
      if self.reached_a_vertex_cover():
        break
      w = self.get_vertex_to_remove(vc)
      u = self.get_vertex_to_add(vc)
      self.add_vertex_to_cover(u, vc)
      self.remove_vertex_from_cover(w, vc)      
      self.update_weights(1)
    return vc


# Util methods for IO and verification
def read_graph(graphfile_path):
  graph = nx.Graph()
  #Read and construct the graph
  with open(graphfile_path, 'r') as graphfile:
    line = graphfile.readline()
    line = line.strip("\n")
    num_vertices, num_edges, tmp = line.split(" ")    
    u = 1
    for line in graphfile:
      if len(line) == 0:
        continue
      line = line.strip("\n")
      line = line.strip()
      if len(line) == 0:
        continue
      adjacency = line.split(" ")
      for v in adjacency:
        v = int(v)   
        #weight of the edge denotes how difficult it is to be covered
        weight = INITIAL_WEIGHT
        graph.add_weighted_edges_from([(u, v, weight)])
      u = u + 1
  return graph


def verify_cover(graph1, vc):
  graph = graph1.copy()
  print vc
  for (u,v,dict) in graph.edges(data=True):
    if u in vc or v in vc:
      graph.remove_edge(u,v)
  print len(vc)
  print graph.number_of_edges()


def main(args):
  global trace_file_writer
  global sol_file_writer
  global start_time
  
  graph_files = ['as-22july06', 'delaunay_n10', 'email',
                 'football','hep-th','jazz',
                 'karate','netscience','power',
                 'star', 'star2']
  sol_file_path = os.path.join(args.out_dir, "{graph_file}_SLS_{cutoff}_{seed}.sol")
  trace_file_path = os.path.join(args.out_dir, "{graph_file}_SLS_{cutoff}_{seed}.trace")
  graph_prefix = args.graph
  
  for graph_file in graph_files:
    start_time = time.time()
    sol_file_ptr = open(sol_file_path.format(graph_file=graph_file, cutoff=args.cutoff, seed=args.seed), 'wb')
    trace_file_ptr = open(trace_file_path.format(graph_file=graph_file, cutoff=args.cutoff, seed=args.seed), 'wb')
    sol_file_writer = csv.writer(sol_file_ptr, delimiter=',')    
    trace_file_writer = csv.writer(trace_file_ptr, delimiter=',')
    
    graph_path = os.path.join(graph_prefix, graph_file+".graph")    
    graph = read_graph(graph_path)
    solver = SLSVertexCover(graph, args.seed)
    vc = solver.compute_vertex_cover_with_timeout(int(args.cutoff))
    #verify_cover(graph, vc)
    write_solution(vc)

  sol_file_ptr.close()
  trace_file_ptr.close()

def write_trace(soln):
  trace_file_writer.writerow(["{000:.3f}".format(time.time()-start_time), len(soln)])
  
def write_solution(vertex_cover):
  sol_file_writer.writerow([len(vertex_cover)])
  sol_file_writer.writerow(list(vertex_cover))

# python stochastic_local_search.py --graph /home/dapurv5/MyCode/anahata/src/main/resources/graphs 
#                                   --cutoff 600 
#                                   --seed 909
#                                   --out_dir /home/dapurv5/Desktop/Semesters/1st_semester/CSEAlgorithms/Assignments/Project/output/star2/trace_20
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--seed',help='seed',required=False)
  parser.add_argument('--graph',help='path to input graph file',required=True)
  parser.add_argument('--cutoff',help='cutoff time in seconds',required=True)
  parser.add_argument('--out_dir', help='directory in which you write the sol and trace files', required=True)
  args = parser.parse_args()
  if args.seed == None:
    args.seed = int(time.time() % 1000)
  main(args)
