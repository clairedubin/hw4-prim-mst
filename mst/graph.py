import numpy as np
import heapq
from typing import Union

class Graph:

    def __init__(self, adjacency_mat: Union[np.ndarray, str]):
        """
    
        Unlike the BFS assignment, this Graph class takes an adjacency matrix as input. `adjacency_mat` 
        can either be a 2D numpy array of floats or a path to a CSV file containing a 2D numpy array of floats.

        In this project, we will assume `adjacency_mat` corresponds to the adjacency matrix of an undirected graph.
    
        """
        if type(adjacency_mat) == str:
            self.adj_mat = self._load_adjacency_matrix_from_csv(adjacency_mat)
        elif type(adjacency_mat) == np.ndarray:
            self.adj_mat = adjacency_mat
        else: 
            raise TypeError('Input must be a valid path or an adjacency matrix')
        self.mst = None

    def _load_adjacency_matrix_from_csv(self, path: str) -> np.ndarray:
        with open(path) as f:
            return np.loadtxt(f, delimiter=',')

    def construct_mst(self):
        """
    
        TODO: Given `self.adj_mat`, the adjacency matrix of a connected undirected graph, implement Prim's 
        algorithm to construct an adjacency matrix encoding the minimum spanning tree of `self.adj_mat`. 
            
        `self.adj_mat` is a 2D numpy array of floats. Note that because we assume our input graph is
        undirected, `self.adj_mat` is symmetric. Row i and column j represents the edge weight between
        vertex i and vertex j. An edge weight of zero indicates that no edge exists. 
        
        This function does not return anything. Instead, store the adjacency matrix representation
        of the minimum spanning tree of `self.adj_mat` in `self.mst`. We highly encourage the
        use of priority queues in your implementation. Refer to the heapq module, particularly the 
        `heapify`, `heappop`, and `heappush` functions.

        """
        self.mst = None
        g = self.adj_mat
        mst_rv = np.zeros_like(g)


        def _process_edges(edge_array):
        
            """Helper function: Returns a list of (edge_weight, index) for all non-zero edges in edge_array"""
            edges_to_keep = list(np.where(edge_array > 0)[0])
            return [(edge_array[i], i) for i in edges_to_keep]


        #remove loops (edges that connect a node to itself)
        for i in range(g.shape[0]):
            g[i,i] = 0
            
        #select random node as start node
        prev = np.random.randint(g.shape[0])
        h = _process_edges(g[prev])
        #add edges to heap
        heapq.heapify(h)
        visited = [prev]

        all_nodes = set(np.arange(g.shape[0]))

        while set(visited) != all_nodes:
                
            if len(h) == 0:
                
                raise ValueError("Heap became empty before all nodes were added to MST")
                
            weight, node_index = heapq.heappop(h)
                
            if node_index in visited:
                continue
            
            #add to mst
            mst_rv[prev,node_index] = weight
            mst_rv[node_index,prev] = weight
            
            #add child edges to heap
            next_edges = _process_edges(g[node_index])
            for val, idx in next_edges:
                heapq.heappush(h, (val,idx))
                
            #add node to visited
            visited += [node_index]

        self.mst = mst_rv



