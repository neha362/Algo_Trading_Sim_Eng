from typing import TypeVar
T = TypeVar('T')

class DequeNode[T]:
    def __init__(self, value:T):
        self.value = value
        self.prev = None
        self.next = None
    
class Deque[T]:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def pop(self):
        if self.head == None:
            raise IndexError()
        ret = self.head
        self.head = self.head.next
        return ret.value

    def push(self, value:T):
        if self.head == None:
            self.head = DequeNode(value)
            self.tail = self.head
        else:
            self.tail.next = DequeNode(value)
            self.tail = self.tail.next
    
    def peek(self):
        if self.head == None:
            raise IndexError()
        return self.head.value
