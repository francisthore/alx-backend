#!/usr/bin/env python3
"""
    Implementation of Hyper Media Pagination
"""
from typing import Dict
import csv
import math
from typing import List, Tuple


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
        """
            retrieves dataset page
        """
        assert type(page) is int and type(page_size) is int
        assert page > 0 and page_size > 0

        start_index, end_index = index_range(page=page, page_size=page_size)

        dataset = self.dataset()
        if start_index > len(dataset):
            return []

        return dataset[start_index:end_index]

    def get_hyper(self, page: int, page_size: int) -> Dict:
        """
            Hypepagination implementation
        """
        assert type(page) is int and type(page_size) is int
        assert page > 0 and page_size > 0

        dataset = self.get_page(page=page, page_size=page_size)
        total_pages = math.ceil(len(self.dataset) / page_size)

        result = {
            "page_size": len(dataset),
            "page": page,
            "data": dataset,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages
        }

        return result
