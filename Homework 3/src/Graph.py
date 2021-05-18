from typing import TypeVar, Union
from warnings import warn

n = TypeVar("n")
w = TypeVar("w", *[int, float])

from .Edge import Edge, Shortcut
from .Vertex import Vertex
        

class Graph:
    """
    Implements a weighed graph structure, can be either directed or undirected
    
    Attributes
    ----------
    _graph: dict[n, Vertex]
        Stores the graph connection in a ordered list-like fashion: given a
        node name it returns an instance of the class Vertex
    _directed: bool
        True if the graph is directed, False otherwise
    
    Methods
    -------
    add_vertex(vertex_name: n)
        Adds a new vertex to the graph
        
    remove_vertex(vertex_name: n)
        Removes a vertex from the graph
    
    contains_vertex(vertex_name: n) -> bool
        Returns True if the graph contains the given vertex, False otherwise
    
    get_vertex(vertex_name: n) -> Union[Vertex, None]:
        Returns the vertex with the given name
        
    add_edge(source: n, destination: n, weight: w = 1.)
        Adds an edge to the graph, if the vertexes containing source and
        destination are not present it adds them as well
            
    remove_edge(source: n, destination: n)
        Removes the edge (source, destination) from the graph

    contains_edge(source: n, destination: n) -> bool
        Returns True if the graph contains the edge (source, destination),
        False otherwise
        
    Adj(vertex_name: n) -> list[n]
        Returns the adjacent vertexes of the given vertex
    
    V() -> list[Vertex]
        Returns a list of all the vertexes present in the graph
    
    E() -> list[Edge]
        Returns a list of all the edges present in the graph

    T() -> Graph:
        Returns a transposed version of the graph, i.e. a new graph with
        its connections flipped

    add_shortcut(v: Vertex):
        Adds the shortcut from a particular Vertex v to the graph,
        takes time O(|V| + n_parents(v) + n_childs(v)) 

    add_shortcuts():
        Adds all the shortcuts to the graph, takes time O(|V|^2 + |E|)

    get_parents(vertex_name: n) -> list[Vertex]:
        Returns the parent of a given Vertex, takes time O(|V|) on average

    get_childs(vertex_name: n) -> list[Vertex]:
        Returns the childs of the given vertex
    """
    
    def __init__(self, directed: bool = True):
        """
        Class constructor, creates an empty graph
        
        Parameters
        ----------
        directed: bool
            If True it creates a directed graph, if False an undirected graph
            Default: True
        """
        
        self._graph = dict()
        self._directed = directed
    
    
    def add_shortcuts(self):
        """Adds all the shortcuts to the graph, takes time O(|V|^2 + |E|)"""

        # Get vertex importances
        try:
            importances = [(v.importance, v) for v in self.V()]
        except AttributeError:
            warn("The graph has vertexes without an importance attribute, exiting", RuntimeWarning)
            return
        
        # Sort by increasing importance
        importances.sort(key = lambda x: x[0])
        
        # Add the shortcuts
        [self.add_shortcut(v) for _, v in importances]


    def add_shortcut(self, v: Vertex):
        """Adds the shortcut from a particular Vertex v to the graph,
        takes time O(|V| + n_parents(v) + n_childs(v)) 

        Args:
            v (Vertex): Vertex to add the shortcuts
        """

        # Get parents and childs of the node to remove
        parents = self.get_parents(v.name)
        childs = self.get_childs(v.name)
        
        for p in parents:
            if p.importance < v.importance:
                continue
            for c in childs:
                if c.importance < v.importance or p.name==c.name:
                    continue
                
                # Add the shortcut if v is less important than either p and c
                # and the shortcut has less weight than the existing connection
                w = p.get_weight(v.name) + v.get_weight(c.name)
                if p.get_weight(c.name) is None or p.get_weight(c.name) > w:
                    e1 = p[v.name]
                    e2 = v[c.name]
                    shortcut = Shortcut(e1, e2)
                    self.add_edge_aux(shortcut)
        
    
    def get_parents(self, vertex_name: n) -> "list[Vertex]":
        """Returns the parent of a given Vertex, takes time O(|V|) on average
        because v.get_connections() is a dictionary

        Args:
            vertex_name (n): vertex to get the parents

        Returns:
            list[Vertex]: List of vertexes which are the parents of vertex_name
        """
        return [v for v in self.V() if vertex_name in v.get_connections()]
    
    
    def get_childs(self, vertex_name: n) -> "list[Vertex]":
        """Returns the childs of the given vertex

        Returns:
            list[Vertex]: List with the child vertexes of vertex_name
        """
        if not self.contains_vertex(vertex_name):
            return
        return [self.get_vertex(v) for v in self.Adj(vertex_name)]
    
    
    def add_vertex(self, vertex_name: n):
        """
        Adds a new vertex to the graph
        
        Parameters
        ----------
        vertex_name: n
            Name of the vertex to be added
        """
        new_vertex = Vertex(vertex_name)
        self._graph[new_vertex.name] = new_vertex
       
    
    def remove_vertex(self, vertex_name: n):
        """
        Removes a vertex from the graph
        
        Parameters
        ----------
        vertex_name: n
            Name of the vertex to be removed
        """
        # Remove incoming connections
        for v in self.V():
            v.remove_connection(vertex_name)
        
        # Remove the vertex
        try:
            self._graph.pop(vertex_name)
        except KeyError:
            pass
    
    
    def contains_vertex(self, vertex_name: n) -> bool:
        """Returns True if the graph contains the given vertex, False otherwise

        Args:
            vertex_name (n): Vertex to test if its contained in the graph

        Returns:
            bool: True if the graph contains the given vertex, False otherwise
        """
        return vertex_name in self._graph.keys()
    
    
    def get_vertex(self, vertex_name: n) -> Union[Vertex, None]:
        """
        Returns the vertex with the given name
        
        Parameters
        ----------
        vertex_name: n
            Name of the vertex to be found
            
        Returns
        -------
        Union(Vertex, None):
            A vertex if vertex_name is present in the graph, otherwise None
        """
        try:
            return self._graph[vertex_name]
        except KeyError:
            return None
        
        
    def add_edge_aux(self, edge: Union[Edge, Shortcut]):
        """Utility function to add a member of the class Edge to the graph,
        tipically you would use add_edge and not this function.

        Args:
            edge (Union[Edge, Shortcut]): Edge to add to the graph
        """
        self._graph[edge.get_source()].add_connection(edge)
        
        
    def add_edge(self, source: n, destination: n, weight: w = 1.):
        """
        Adds an edge to the graph, if the vertexes containing source and
        destination are not present it adds them as well
        
        Parameters
        ----------
        source: n
            Source of the edge to be added
        
        destination: n
            Destination of the edge
        
        weight: w, Optional
            Weight of the connection, Default=1.
        """
        
        if not self.contains_vertex(destination):
            self.add_vertex(destination)
        if not self.contains_vertex(source):
            self.add_vertex(source)
        
        self.add_edge_aux(Edge(source, destination, weight))
            
        if not self._directed:
            self.add_edge_aux(Edge(destination, source, weight))
            
        
    def remove_edge(self, source: n, destination: n):
        """
        Removes the edge (source, destination) from the graph
        """
        try:
            self._graph[source].remove_connection(destination)
        except KeyError:
            pass
        
        if not self._directed:
            try:
                self._graph[destination].remove_connection(source)
            except KeyError:
                pass
    
    
    def contains_edge(self, source: n, destination: n) -> bool:
        """ 
        Returns True if the graph contains the edge (source, destination),
        False otherwise
        """
        if not self.contains_vertex(source):
            return False
        if not self.contains_vertex(destination):
            return False
        
        return self._graph[source].has_connection(destination)
      
        
    def Adj(self, vertex_name: n) -> list:
        """Returns the adjacent vertexes of the given vertex

        Raises:
        RuntimeWarning
            If vertex_name is not present in the graph 
        """
        try:
            return self._graph[vertex_name].get_connections().keys()
        except KeyError:
            warn(f"vertex {vertex_name} does not exist, exiting", RuntimeWarning)
    
    
    def V(self) -> "list[Vertex]":
        """Returns a list of all the vertexes present in the graph"""
        return list(self._graph.values())
    
    
    def E(self) -> "list[Edge]":
        """Returns a list of all the edges present in the graph"""
        res = []
        for v in self.V():
            res.extend([i for i in v.get_connections().values()])
        return res
    
    
    def T(self) -> "Graph":
        """
        Returns a transposed version of the graph, i.e. a new graph with
        its connections flipped
        """
        new_G = Graph()

        # Add the vertexes
        [new_G.add_vertex(v.name) for v in self.V()]

        # Add the edges reversed
        [new_G.add_edge_aux(edge.T()) for edge in self.E()]

        # Copy additional vertexes attributes, for example importances
        for new_v in new_G.V():
            old_v = self.get_vertex(new_v.name)
            [setattr(new_v, a, getattr(old_v, a)) for a in dir(old_v) if not hasattr(new_v, a)]
        
        return new_G
            
    
    def __repr__(self) -> str:
        """Overload of the print function"""
        s = ""
        for v in self.V():
            s += f"{v.__repr__()}\n"
            
        return s