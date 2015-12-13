#!/usr/bin/env/python
#
# author: apurvverma@gatech.edu

import networkx as nx
import argparse
import time
import sys

from anahata.collections.unionfind import UnionFind

  
def kruskals_mst(graph):
  """
  Args:
    graph - networkx graph object
  Returns:
    The weight of the minimum spanning tree
  """
  uf = UnionFind()
  for node in graph.nodes():
    uf.add(node)
        
  mst_weight = 0
  #sort the edges by weight
  edges_sorted = sorted(graph.edges(data=True), key = lambda (u,v,w): w)
  spanning_tree = nx.MultiGraph()
  #pick edges in ascending order of their weights  
  for edge in edges_sorted:
    #the picked edge will be a part of the spanning tree if it connects two separate 
    #connected components.
    src_vertex = edge[0]
    dst_vertex = edge[1]
    weight_edge = edge[2]['weight']
    if uf.find(src_vertex) != uf.find(dst_vertex):
      mst_weight += weight_edge
      spanning_tree.add_weighted_edges_from([(src_vertex, dst_vertex, weight_edge)])
      uf.union(src_vertex, dst_vertex)
      #TODO: can early exit here if the number of nodes picked up is n-1
  return mst_weight, spanning_tree

def get_max_edge_weight(graph, start, target):
  """
  Since there may be parallel edges, this method returns the
  weight of the maximum weighted edge between start and target node.
  """
  max_weight = 0
  for edge_attr in graph[start][target].values():
    max_weight = max(max_weight, edge_attr['weight'])
  return max_weight


def remove_edge(graph, start, target, weight):
  key_to_remove = None
  for key, edge_attr in graph[start][target].items():
    if edge_attr['weight'] == weight:
      key_to_remove = key
  graph.remove_edge(start, target, key=key_to_remove)
  
  
def recompute_mst(spanning_tree, new_edge, old_mst_weight):
  """
  Inserts the new edge src_vertex, dst_vertex in the spanning tree.
  Removes the heaviest edge in the cycle thus formed
  """
  src_vertex = new_edge[0]
  dst_vertex = new_edge[1]
  new_edge_weight = new_edge[2]
  
  #Add the new edge to the spanning tree, this will form a cycle
  spanning_tree.add_weighted_edges_from([new_edge])
  
  heaviest_edge_weight = 0 #the weight of the heaviest edge on the cycle
  heaviest_edge_src = -1
  heaviest_edge_dst = -1
  #TODO: assert that there are only two paths from src_vertex to dst_vertex
  # since at max one cycle may be introduced.
  for path in nx.all_simple_paths(spanning_tree, source=src_vertex, target=dst_vertex):
    for i in range(len(path)-1):            
      curr_weight = get_max_edge_weight(spanning_tree, path[i], path[i+1])
      if curr_weight > heaviest_edge_weight:
        heaviest_edge_weight = curr_weight
        heaviest_edge_src = path[i]
        heaviest_edge_dst = path[i+1]
  new_mst_weight = old_mst_weight + new_edge_weight - heaviest_edge_weight
  
  #remove the heaviest edge from the cycle
  remove_edge(spanning_tree, heaviest_edge_src, heaviest_edge_dst, heaviest_edge_weight)
  return new_mst_weight, spanning_tree

def main(args):
  graph = nx.MultiGraph()
  with open(args.graph, 'r') as graphfile:
    line = graphfile.readline()
    line = line.strip("\n")
    num_vertices, num_edges = line.split(" ")
    for line in graphfile:
      line = line.strip("\n")
      src_vertex, dst_vertex, weight = line.split(" ")
      weight = int(weight)
      graph.add_weighted_edges_from([(src_vertex, dst_vertex, weight)])
    start_time = time.time()
    mst_weight, spanning_tree = kruskals_mst(graph)
    end_time = time.time()
    print mst_weight, (end_time - start_time)*1000
    
  with open(args.changes, 'r') as changesfile:
    line = changesfile.readline()
    line = line.strip('\n')
    num_changes = int(line)
    for line in changesfile:
      line = line.strip('\n')
      src_vertex, dst_vertex, weight = line.split(" ")
      weight = int(weight)      
      start_time = time.time()
      new_edge = (src_vertex, dst_vertex, weight)
      new_mst_weight, spanning_tree = recompute_mst(spanning_tree, new_edge, mst_weight)
      end_time = time.time()
      mst_weight = new_mst_weight
      print mst_weight, (end_time - start_time)*1000
  
#python mst.py --graph rmat0406.gr (Assignment1 cse algos class) --changes rmat0406.extra
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--graph',help='path to input graph file',required=True)
  parser.add_argument('--changes', help='path to the update graph file', required=True)
  args = parser.parse_args()
  main(args)
  