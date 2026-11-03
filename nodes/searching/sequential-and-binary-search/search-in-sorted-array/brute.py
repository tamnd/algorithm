# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/search-in-sorted-array/. The brute force oracle (spec 09.5). Rule S07 checks that it agrees with reference.py.


def search(a, x):
    """Return the last index i with a[i] == x, or None when x is not in a. It reads from the end, so where x is in a more than once, it gives another index than reference.py, and checker.py must accept both."""
    for i in range(len(a) - 1, -1, -1):
        if a[i] == x:
            return i
    return None
