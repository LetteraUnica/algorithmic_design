from typing import TypeVar, Union
from warnings import warn

n = TypeVar("n")
w = TypeVar("w", *[int, float])

class Edge:
    """
    Simple class that implements a weighed edge of a graph

    Attributes
    ----------
    source: n
        Source of the edge
    destination: n
        Destination of the edge
    weight: w
        weight of the edge

    Methods
    -------
    get_source() -> n:
        Returns the source of the edge
    get_destination() -> n:
        Returns the destination of the edge
    def T() -> "Edge":
        Transposes the edge, i.e. swaps the source and destination 
    def decompose() -> "list[n]":
        Returns the list: [source, destination]
    """

    def __init__(self, source: n, destination: n, weight: w):
        """Class constructor

        Args:
            source (n): Source of the edge
            destination (n): Destination of the edge
            weight (w): Weight of the connection
        """
        self.source = source
        self.destination = destination
        self.weight = weight
    
    def get_source(self) -> n:
        """Returns the source of the edge

        Returns:
            n: The edge source
        """
        return self.source
    
    def get_destination(self) -> n:
        """Returns the destination of the edge

        Returns:
            n: The edge destination
        """
        return self.destination
    
    def T(self) -> "Edge":
        """Transposes the edge, i.e. swaps the source and destination

        Returns:
            Edge: The transposed edge
        """
        return Edge(self.destination, self.source, self.weight)
    
    def decompose(self) -> "list[n]":
        """Returns the list: [source, destination]

        Returns:
            list[n]: List with source and destination of the edge
        """
        return [self.source, self.destination]

    def __repr__(self) -> str:
        """Overload of the print function"""
        return (self.source, self.destination, self.weight).__repr__()

    
class Shortcut:
    """
    Simple class that implements a shortcut of a graph

    Attributes
    ----------
    e1: Edge
        First edge of the shortcut
    e2: Edge
        Second edge of the shortcut
    weight: w
        weight of the shortcut

    Methods
    -------
    get_source() -> n:
        Returns the source of the shortcut
    get_destination() -> n:
        Returns the destination of the shortcut
    def T() -> "Edge":
        Transposes the shortcut, i.e. inverts its direction
    def decompose() -> "list[n]":
        Returns a list with the Vertexes it passes by
    """
    
    def __init__(self, edge1: Edge, edge2: Edge):
        """Class constructor, creates a shortcut given two edges/shortcuts

        Args:
            edge1 (Edge): First edge
            edge2 (Edge): Second edge
        """
        self.e1 = edge1
        self.e2 = edge2
        self.weight = edge1.weight + edge2.weight
    
    def get_source(self) -> n:
        """Returns the source of the shortcut

        Returns:
            n: The source of the shortcut
        """
        return self.e1.get_source()
    
    def get_destination(self) -> n:
        """Returns the destination of the shortcut

        Returns:
            n: The destination of the shortcut
        """
        return self.e2.get_destination()    
        
    def T(self) -> "Shortcut":
        """Transposes the shortcut, i.e. inverts its direction

        Returns:
            Shortcut: Inverted shortcut
        """
        return Shortcut(self.e2.T(), self.e1.T())
    
    def decompose(self) -> "list[n]":
        """Returns a list with the Vertexes it passes by

        Returns:
            list[n]: list with the vertexes the shortcut passes by
        """
        path = self.e1.decompose()
            
        path.extend(self.e2.decompose()[1:])
            
        return path

    def __repr__(self) -> str:
        """Overload of the print function"""
        return (self.decompose(), self.weight).__repr__()