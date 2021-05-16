from typing import TypeVar, Union
from warnings import warn

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
    
    def get_source(self) -> n:
        return self.source
    
    def get_destination(self) -> n:
        return self.destination
    
    def T(self) -> "Edge":
        return Edge(self.destination, self.source, self.weight)
    
    def decompose(self) -> "list[n]":
        return [self.source, self.destination]

    def __repr__(self) -> str:
        return (self.source, self.destination, self.weight).__repr__()

    
class Shortcut:
    def __init__(self, edge1: Edge, edge2: Edge):
        self.e1 = edge1
        self.e2 = edge2
        self.weight = edge1.weight + edge2.weight
    
    def get_source(self) -> n:
        return self.e1.get_source()
    
    def get_destination(self) -> n:
        return self.e2.get_destination()    
        
    def T(self) -> "Shortcut":
        return Shortcut(self.e2.T(), self.e1.T())
    
    def decompose(self) -> "list[n]":
        path = self.e1.decompose()
            
        path.extend(self.e2.decompose()[1:])
            
        return path