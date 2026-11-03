# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/search-in-sorted-array/. The checker of the shared cases (spec 09.3).


def check(args, output, expected=None):
    """Return None if output is an index of x in a, or None when x is not in a. Else return a short reason."""
    a, x = args["a"], args["x"]
    if output is None:
        if x in a:
            return f"x is at index {a.index(x)}, but the output is none"
        return None
    if isinstance(output, bool) or not isinstance(output, int):
        return f"the output {output!r} is not an index"
    if not 0 <= output < len(a):
        return f"the index {output} is out of range for a list of {len(a)} items"
    if a[output] != x:
        return f"a[{output}] is {a[output]!r}, not x"
    return None
