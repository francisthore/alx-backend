#!/usr/bin/env python3
"""
    MRU Cache Module
"""
from base_caching import BaseCaching
from collections import OrderedDict


class MRUCache(BaseCaching):
    """
        Class that implements MRU Caching policy
    """
    def __init__(self):
        """
            Initializes the cache dictionary
        """
        super().__init__()
        self.cache_data = OrderedDict()
        self.access_frequency = {}

    def put(self, key, item):
        """
            Adds an item to the cache dictionary
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data.pop(key)
            self.access_frequency[key] += 1

        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_access = min(self.access_frequency.value())
                data_keys = [k for k,
                             accessed in self.access_frequency.items()
                             if accessed == min_access]
                

        self.cache_data[key] = item

    def get(self, key):
        """
            Retrieves an item from the cache dictionary
        """
        if key is None or key not in self.cache_data:
            return None
        item = self.cache_data.pop(key)
        self.cache_data[key] = item
        return item
