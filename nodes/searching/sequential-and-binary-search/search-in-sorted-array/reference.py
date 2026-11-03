# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/search-in-sorted-array/. The oracle of the shared cases (spec 09.5).


def search(a, x):
    """Return the first index i with a[i] == x, or None when x is not in a. It reads each item in turn, so it does not use the order of a."""
    for i, v in enumerate(a):
        if v == x:
            return i
    return None
