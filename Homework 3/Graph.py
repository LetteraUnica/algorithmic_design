from typing import TypeVar, Union

n = TypeVar("n")
w = TypeVar("w", *[int, float])

class Edge:
    """
    Simple class that implements weighed edge of a graph

    Attributes
    ----------
    source: n
        Source of the edge
    destination: n
        Destination of the edge
    weight: w
        weight of the edge
    """
    def __init__(self, source: n, destination: n, weight: w):
        self.source = source
        self.destination = destination
        self.weight = weight

        
class Vertex:
    """
    Class that implements a graph vertex, the class uses a dictionary to store
    the outward connection from this Vertex to others
    
    Attributes
    ----------
    name: n
        Name of the vertex
    connections: dict[n, w]
        Dictionary holding destination:weight pairs
    
    Methods
    -------
    add(destination: n, weight: w)
        Adds a connection to the Vertex, 
        i.e. it adds a destination:weight pair to the connection dictionary
        
    remove(destination: n):
        Removes a connection from the vertex
        
    get_connections():
        Returns the connections dictionary   
    """
    
    def __init__(self, name: n, edges: list = None):
        """
        Class constructor, given a name and a list of edges builds a new vertex
        
        Parameters
        ----------
        name: n
            Name of the vertex
            
        edges: list[Edge], Optional
            List of members of the Edge class, used to build the outward
            connections of the edge
            Default: None i.e. builds a vertex with no connections
        """
        
        self.name = name
        if edges is None:
            self.connections = dict()
        else:
            self.connections = dict([(edge.destination, edge.weight) for edge in edges if edge.source == name])
     
    
    def add(self, destination: n, weight: w):
        """
        Adds a connection to the Vertex
        
        Parameters
        ----------
        destination: n
            Destination of the connection
        weight: w
            Weight of the connection
        """
        self.connections[destination] = weight
        
        
    def remove(self, destination: n):
        """
        Removes a connection from the vertex
        
        Parameters
        ----------
        destination: n
            Destination of the connection to remove
        """
        try:
            self.connections.pop(destination)
        except KeyError:
            pass
        
        
    def get_connections(self):
        """Returns the connections dictionary"""
        return self.connections
    
    def get_weight(self, destination: n) -> Union[float, int, None]:
        """
        Returns the weight of the connection from this vertex to destination
        if the connection is not present returns None
        
        Parameters
        ----------
        destination: n
            Destination of the connection to get the weight
            
        Returns
        -------
        connection_weight: Union[float, int, None]
            Weight of the connection from this vertex to destination,
            if the connection is not present returns None
        """
        try:
            return self.connections[destination]
        except KeyError:
            return None

        
    def __repr__(self):
        """Overload of the print function"""
        return f"{self.name} : {self.get_connections()}"
        

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
    
    E() -> list[(n, n)]
        Returns a list of all the edges present in the graph
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
        for vertex in self._graph.values():
            vertex.remove(vertex_name)
        
        # Remove the vertex
        try:
            self._graph.pop(vertex_name)
        except KeyError:
            pass
    
    
    def contains_vertex(self, vertex_name: n):
        """Returns True if the graph contains the given vertex, False otherwise"""
        return vertex_name in self._graph.keys()
    
        
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
        
        self._graph[source].add(destination, weight)
            
        if not self._directed:
            self._graph[destination].add(source, weight)
            
            
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
        
    def remove_edge(self, source: n, destination: n):
        """
        Removes the edge (source, destination) from the graph
        """
        self._graph[source].remove(destination)
        if not self._directed:
            self._graph[destination].remove(source)
    
    
    def contains_edge(self, source: n, destination: n) -> bool:
        """ 
        Returns True if the graph contains the edge (source, destination),
        False otherwise
        """
        if not contains_vertex(source):
            return False
        if not contains_vertex(destination):
            return False
        return destination in self._graph[source].get_connections()
      
        
    def Adj(self, vertex_name: n) -> list:
        """Returns the adjacent vertexes of the given vertex"""
        return self._graph[vertex_name].get_connections()
    
    
    def V(self) -> list:
        """Returns a list of all the vertexes present in the graph"""
        return list(self._graph.values())
    
    
    def E(self) -> list:
        """Returns a list of all the edges present in the graph"""
        res = []
        for v in self.V():
            res.extend([(v.name, i) for i in v.get_connections().keys()])
        return res
    
    
    def __repr__(self):
        """Overload of the print function"""
        s = ""
        for v in self.V():
            s += f"{v.__repr__()}\n"
            
        return s