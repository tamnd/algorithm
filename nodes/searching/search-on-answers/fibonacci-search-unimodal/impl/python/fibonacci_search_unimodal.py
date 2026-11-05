# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fibonacci-search-unimodal/. The authors are listed in prov/FM952M.jsonl.

from typing import Callable


def fibonacci_search_max(f: Callable[[int], float], n: int) -> int:
    """Return the mode of a strictly unimodal f on the indices 1..n.

    It evaluates f exactly N times, where N is the smallest number with
    F(N + 2) - 1 >= n, which is the least number that any method can guarantee.
    Indices above n stand for padding values that are smaller than every f(i).
    """
    if n < 1:
        raise ValueError("empty range")
    fib = [0, 1]  # @line L1
    while fib[-1] < n + 1:
        fib.append(fib[-1] + fib[-2])
    big_n = len(fib) - 3  # F(N + 2) is the first Fibonacci number >= n + 1
    lo, hi = 0, fib[big_n + 2]  # @line L2
    p = fib[big_n]  # @line L3
    fp = f(p)
    k = big_n - 1  # @line L4
    while k > 0:  # @line L5
        if p - lo > hi - p:  # @line L6
            q = p - fib[k]
        else:
            q = p + fib[k]
        fq = f(q) if q <= n else None  # @line L7
        if fq is not None and fq > fp:  # @line L8
            if q > p:
                lo = p
            else:
                hi = p
            p, fp = q, fq
        else:  # @line L9
            if q > p:
                hi = q
            else:
                lo = q
        k -= 1  # @line L10
    return p  # @line L11
