#!/usr/bin/env python3
"""
    FIFO Cache Module
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
        Class that implements FIFO Caching policy
    """
    def __init__(self):
        """
            Initializes the cache dictionary
        """
        super().__init__()
        self.track_list = []

    def put(self, key, item):
        """
            Adds an item to the cache dictionary
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                old_key = self.track_list.pop(0)
                print('DISCARD:', old_key)
                del self.cache_data[old_key]

            self.cache_data[key] = item
            self.track_list.append(key)

    def get(self, key):
        """
            Retrieves an item from the cache dictionary
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
