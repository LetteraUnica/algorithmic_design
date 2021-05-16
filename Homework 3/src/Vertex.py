from typing import TypeVar, Union
from warnings import warn

n = TypeVar("n")
w = TypeVar("w", *[int, float])

from .Edge import Edge, Shortcut


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
    
    def __init__(self, name: n, edges: "list[Edge]" = None):
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
            self.connections = dict([(edge.destination, edge) for edge in edges if edge.source == name])
     
    
    def add_connection(self, edge: Union[Edge, Shortcut]):
        """
        Adds a connection to the Vertex
        
        Parameters
        ----------
        destination: n
            Destination of the connection
        weight: w
            Weight of the connection
        """
        if edge.get_source() != self.name:
            message = f"The edge can't be added because its source {edge.get_source()} "
            message += f"is different than the vertex name {self.name}, exiting\n"
            warn(message, RuntimeWarning)
            return

        self.connections[edge.get_destination()] = edge
    
    
    def remove_connection(self, destination: n):
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
    
    
    def has_connection(self, destination: n) -> bool:
        try:
            _ = self.connections[destination]
        except KeyError:
            return False
        
        return True
        
        
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
            return self.connections[destination].weight
        except KeyError:
            return None

    
    def __getitem__(self, key: n) -> Edge:
        return self.connections[key]


    def __repr__(self):
        """Overload of the print function"""
        return f"{self.name} : {self.connections.keys()}"
        
