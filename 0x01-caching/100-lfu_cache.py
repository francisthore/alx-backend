#!/usr/bin/env python3
""" LFU Caching System Module """

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ Implements LFU (Least Frequently Used) Cache System
    """

    def __init__(self):
        """ Initialize the LFU cache system """
        super().__init__()
        self.usage_frequency = {}
        self.access_order = {}

    def put(self, key, item):
        """
        Add an item to the cache, using LFU and
        LRU policies for eviction if needed.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
        else:
            if len(self.cache_data) >= self.MAX_ITEMS:
                min_frequency = min(self.usage_frequency.values())
                least_frequent_keys = [k for k,
                                       freq in self.usage_frequency.items()
                                       if freq == min_frequency]

                if len(least_frequent_keys) > 1:
                    lru_key = min(least_frequent_keys,
                                  key=lambda k: self.access_order[k])
                    self._evict(lru_key)
                else:
                    self._evict(least_frequent_keys[0])

            self.cache_data[key] = item
            self.usage_frequency[key] = 1
            self.access_order[key] = len(self.access_order)

        self.usage_frequency[key] += 1
        self.access_order[key] = len(self.access_order)

    def get(self, key):
        """
        Retrieve an item from the cache by key.
        """
        if key is None or key not in self.cache_data:
            return None

        self.usage_frequency[key] += 1
        self.access_order[key] = len(self.access_order)
        return self.cache_data[key]

    def _evict(self, key):
        """
        Helper function to evict a key from the cache.
        """
        if key in self.cache_data:
            print(f"DISCARD: {key}")
            del self.cache_data[key]
            del self.usage_frequency[key]
            del self.access_order[key]
