#!/usr/bin/env python3
"""
    Implements simple pagination using index
"""
import csv
import math
from typing import List
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
        Uses page_size for indexing and pagination
    """
    if page == 1:
        start_index = 0
        end_index = page_size
    else:
        start_index: int = (page - 1) * page_size
        end_index = (start_index + page_size)
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        assert type(page) is int, "page must be an int"
        assert page > 0, "page must be a positive number greater than zero"
        assert page_size > 0, "page_size must be a positive number"
        assert type(page_size) is int, "page_size must be an int"

        start_index, end_index = index_range(page=page, page_size=page_size)

        self.dataset()

        results = self.dataset()[start_index:end_index]
        return results
