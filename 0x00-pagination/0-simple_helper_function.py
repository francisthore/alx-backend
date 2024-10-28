#!/usr/bin/env python3
"""
    API Pagination module
"""
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
