
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

# head tail 
class LRUCache:
    def __init__(self, capacity):
        if type(capacity) is not int or capacity <= 0:
            raise ValueError("Invalid capacity")

        self.capacity = capacity
        self.cache = {}

        # Dummy head and tail
        self.head = Node(None, None)
        self.tail = Node(None, None)

        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        prev = node.prev
        nxt = node.next

        prev.next = nxt
        nxt.prev = prev

        node.prev = None
        node.next = None

    def _add_to_end(self, node):
        last = self.tail.prev

        last.next = node
        node.prev = last
        node.next = self.tail
        self.tail.prev = node

    def _move_to_end(self, node):
        self._remove(node)
        self._add_to_end(node)

    def read(self, key):
        if key is None:
            raise ValueError("Key cannot be None")

        if key not in self.cache:
            return None

        node = self.cache[key]
        self._move_to_end(node)
        return node.value

    def write(self, key, value):
        if key is None:
            raise ValueError("Key cannot be None")

        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_end(node)
            return

        node = Node(key, value)
        self.cache[key] = node
        self._add_to_end(node)

        if len(self.cache) > self.capacity:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]

    def delete(self, key):
        if key is None:
            raise ValueError("Key cannot be None")

        node = self.cache.pop(key, None)

        if node is None:
            return None

        self._remove(node)
        return node.value

    def clear(self):
        n = len(self.cache)
        self.cache.clear()
        self.head.next = self.tail
        self.tail.prev = self.head
        return n

    def count(self):
        return len(self.cache)

    def to_h(self):
        return {
            key: node.value
            for key, node in self.cache.items()
        }
