
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        if type(capacity) is not int or capacity <= 0:
            raise ValueError("Capacity must be a positive integer")

        self.capacity = capacity
        self.dic = OrderedDict()

    def _validate_key(self, key):
        if key is None:
            raise ValueError("Key cannot be None")

    def read(self, key):
        self._validate_key(key)

        if key not in self.dic:
            return None

        self.dic.move_to_end(key)
        return self.dic[key]

    def write(self, key, value):
        self._validate_key(key)

        if key in self.dic:
            self.dic.move_to_end(key)

        self.dic[key] = value

        if len(self.dic) > self.capacity:
            self.dic.popitem(last=False)

    def delete(self, key):
        self._validate_key(key)
        return self.dic.pop(key, None)

    def clear(self):
        current_length = len(self.dic)
        self.dic.clear()
        return current_length

    def count(self):
        return len(self.dic)

    def to_h(self):
        return dict(self.dic)
