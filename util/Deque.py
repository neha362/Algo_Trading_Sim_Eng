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
        self.len = 0
    
    def pop(self):
        if self.head == None:
            raise IndexError()
        ret = self.head
        self.head = self.head.next
        self.len -= 1
        return ret.value

    def push(self, value:T):
        if self.head == None:
            self.head = DequeNode(value)
            self.tail = self.head
        else:
            self.tail.next = DequeNode(value)
            self.tail.next.prev = self.tail
            self.tail = self.tail.next
        self.len += 1
    
    def peek(self):
        if self.head == None:
            raise IndexError()
        return self.head.value
    
    def remove(self, node: DequeNode[T]):
        assert (node != None)
        if node.prev != None:
            node.prev.next = node.next
        if node.next != None:
            node.next.prev = node.prev
        self.len -= 1

    def __len__(self):
        return self.len
    
    def __str__(self):
        return f"deque with head {self.head.value}"