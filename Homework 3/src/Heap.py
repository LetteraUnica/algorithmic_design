from copy import deepcopy
from collections.abc import Callable
from typing import TypeVar
from warnings import warn
from numpy import inf

T = TypeVar("T")
K = TypeVar("K")

class Binary_heap:
    """
    Implements a binary heap with a generic ordering
    
    Attributes
    ----------
    H: list[T]
        Stores the heap values
    size: int
        Stores the length of H
    _order: Callable[[T, T], bool]
        Function used to order the heap
    needs_dict: bool
        Whether the heap has a dictionary of (T, index) pairs
    key_dict: dict(K, int)
        Dictionary of (key, index) pairs, the dictionary tells the index 
        in the heap of a given value T
    dict_key: Callable[[T], K]
        Gives the key of the key_dict dictionary given a value T
    
    Methods
    -------
    left(i: int) -> int
        Returns the index of the left child of i  
    right(i: int) -> int
        Returns the index of the right child of i
    parent(i: int) -> int
        Returns the index of the parent of i
    get_root() -> int
        Returns the index of the root i.e. 0
    is_root(i: int) -> bool
        Returns True if i is the root, False otherwise
    is_valid_node(i: int) -> boot
        Returns True if index i belongs to the heap, False otherwise
    is_empty() -> bool
        Returns True if the heap is empty i.e. size==0, False otherwise
    extract_min() -> T
        Returns the minimum key stored in the binary heap
    remove_min() -> T 
        Removes the minimum value from the binary heap and returns it
    decrease_key(key: int, new_value: T)
        Decreases the value of H[index] to new_value
    decrease_value(self, value: T, new_value: T)
        Decreases the value to new_value
    insert(self, value: T):
        Inserts a new value into the binary heap
    """
    
    def __init__(self, A: list, to_copy: bool = True,
                 total_order: Callable = None,
                 dict_key: Callable = None):
        """
        Class constructor, creates a heap from a list either in-place or
        by copying it, the ordering of the heap can be changed by passing a
        total_order, furthermore by passing a dict_key function the heap can
        decrease it's elements without needing the respective index
        
        Parameters
        ----------
        A: list[T]
            List containing the values to include in the heap
        to_copy: bool
            If True it copies the list A into another to store the heap,
            If False it uses the list A itself to store the heap
            Default: True
        total_order: Callable[[T, T], bool]
            Function used to order the elements of the heap
            Default: None, which corresponds to a Min-Heap
        dict_key: Callable[[T], K]
            Function used to update a value without needing the index in the heap
        """
        
        # Get the heap size
        self.size = len(A)
        
        # Copy or not the heap
        if to_copy:
            self.H = deepcopy(A)
        else:
            self.H = A
        
        # Define a total_order
        if total_order is None:
            total_order = lambda x, y: x<y
        self._order = total_order
        
        self.needs_dict = False
        if dict_key is not None:
            self.needs_dict = True
            self.dict_key = dict_key
        
        # Build the heap
        self._build_heap()
        
    
    def _swap(self, i: int, j: int):
        """
        Utility function that swappes two elements of H
        
        Parameters
        ----------
        i: int
            Index of the first element to be swapped
        j: int
            Index of the second element to be swapped
        """
        
        if self.needs_dict:
            self.key_dict[self.dict_key(self.H[i])] = j
            self.key_dict[self.dict_key(self.H[j])] = i
            
        tmp = self.H[i]
        self.H[i] = self.H[j]
        self.H[j] = tmp

        
    def _heapify(self, i: int):
        """
        Utility function that restores the heap property if it has been broken
        only on index i, the function restores the heap property iteratively
        instead of recursively
        
        Parameters
        ----------
        i: int
            Index on which to restore the heap property
        """
        
        keep_fixing = True
        m = i
        # Repeats until the parent is a leaf or is less than either childs
        while keep_fixing:
            i = m
            # Find a child that is less than the parent
            for j in (self.left(i), self.right(i)):
                if self.is_valid_node(j) and self._order(self.H[j], self.H[m]):
                    m = j
            
            # Swap child and parent
            self._swap(i, m)
            if i == m:
                keep_fixing=False
    
    
    def _build_dict(self):
        """Utility function that builds the key_dict dictionary"""
        self.key_dict = dict((self.dict_key(self.H[i]), i) for i in range(self.size))
    
    
    def _build_heap(self):
        """
        Utility function used to build an heap
        """
        
        if self.needs_dict:
            self._build_dict()
            
        for i in range(self.parent(self.size), -1, -1):
            self._heapify(i)
   
    def left(self, i: int) -> int:
        """
        Returns the index of the left child of i
        """
        return 2*i + 1

    def right(self, i: int) -> int:
        """
        Returns the index of the right child of i
        """
        return 2*(i+1)

    def parent(self, i: int) -> int:
        """
        Returns the index of the parent of i
        """
        return (i-1)//2

    def get_root(self) -> int:
        """
        Returns the index of the root of the heap, i.e 0
        """
        return 0

    def is_root(self, i: int) -> bool:
        """
        Returns True if index i is the root of the heap, False otherwise
        """
        return i == self.get_root()

    def is_valid_node(self, i: int) -> bool:
        """
        Returns True if index i is contained in the heap, False otherwise
        """
        return i < self.size

    def is_empty(self) -> bool:
        """
        Returns True if the heap is empty i.e. size==0, False otherwise
        """
        return self.size == 0
    
    def extract_min(self) -> T:
        """
        Returns the minimum value stored in the heap
        """
        return self.H[self.get_root()]
    
    
    def remove_min(self) -> T:
        """
        Removes the minimum value stored in the heap and returns it
        
        Returns
        -------
        The minimum value of the heap
        """
        
        if self.is_empty():
            message = f"The heap is empty"
            warn(message, category=RuntimeWarning)
            return
        
        minimum = self.extract_min()
        # Replace minimum with leftmost value
        self.H[0] = self.H[self.size-1]
        # Decrease the heap size
        self.size -=1
        
        # Restore heap property on index 0
        self._heapify(0)
        
        return minimum
                
        
    def decrease_key(self, key: int, new_value: T):
        """
        Decreases the index "key" to "new_value"
        
        Parameters
        ----------
        key: int
            Index to decrease
        new_value: T
            New value to assign to H[key]
        
        Raises
        ------
        RuntimeWarning
            If new_value is smaller than H[key]
        """
        
        # Exit if new_value > H[key]
        if self.H[key] != inf and self._order(self.H[key], new_value):
            message = f"{new_value} is smaller than the previous one, "
            message += "the function does nothing in this case"
            warn(message, category=RuntimeWarning)
            return
        
        # Otherwise update H[key] and fix the heap property by iteratively
        # swapping parent and child
        self.H[key] = new_value
        i = key
        p = self.parent(i)
        while not self.is_root(i) and self._order(self.H[i], self.H[p]):
            self._swap(p, i)
            i = p
            p = self.parent(i)
    
    
    def decrease_value(self, value: T, new_value: T):
        """
        Decreases the value to new_value
        
        Parameters
        ----------
        value: T
            Value to decrease
        new_value: T
            New value to assign to H[key]
        
        Raises
        ------
        RuntimeWarning
            If new_value has a different dictionary key than the previous
            one, i.e. dict_key(value) != dict_key(new_value)
        RuntimeWarning
            If new_value is smaller than value
        """
        
        if self.dict_key(value) != self.dict_key(new_value):
            message = "The new value has a different dictionary key than the previous one"
            message += f" {self.dict_key(value)} != {self.dict_key(new_value)}"
            message += " exiting\n"
            warn(message, RuntimeWarning)
            return

        key = self.key_dict[self.dict_key(value)]
        self.decrease_key(key, new_value)


    def insert(self, value: T, to_copy=True):
        """
        Inserts a new value in the heap
        
        Parameters
        ----------
        value: T
            New value to insert in the heap
        to_copy: bool, Optional
            If True copies the value before inserting it in the heap, Default: True
        """
        
        if to_copy:
            value = deepcopy(value)
        self.size += 1

        try:
            self.H[self.size-1] = inf
        except IndexError:
            self.H.append(inf)

        if self.needs_dict:
            self.key_dict[self.dict_key(value)] = self.size-1
        self.decrease_key(self.size-1, value)
        
        
    def _test_heap_property(self):
        """
        Function useful to test whether the heap satisfies the heap property

        Raises
        ------
        RuntimeWarning 
            If the heap property isn't satisfied
        """
        for i in range(0, self.size):
            for j in (self.left(i), self.right(i)):
                if self.is_valid_node(j) and self._order(self.H[j], self.H[i]):
                    message = f"The heap property isn't satisfied: {j} is smaller than its parent"
                    warn(message, RuntimeWarning)
                    return
                
    
    def __repr__(self):
        """
        Utility function to print the array containing the heap
        """
        return self.H[0:self.size].__repr__()