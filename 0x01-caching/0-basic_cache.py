#!/usr/bin/env python3
"""
    Basic Cache Module
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
        Class that implements basic caching
    """
    def __init__(self):
        """
            Initializes the cache dictionary
        """
        super().__init__()

    def put(self, key, item):
        """
            Adds an item to the cache dictionary
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """
            Retrieves an item from the cache dictionary
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
