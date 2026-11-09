# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pascal-triangle-dp/. The authors are listed in prov/RACQ8D.jsonl.


def pascal_binomial(n: int, k: int, modulus: int | None = None) -> int:
    """Return C(n, k), or C(n, k) mod modulus, by one row of Pascal's triangle.

    The row is updated in place from right to left. Only additions are used,
    so any modulus >= 1 works, prime or not. C(n, k) is 0 for k < 0 or k > n.
    """
    if n < 0:
        raise ValueError("n must be nonnegative")
    if modulus is not None and modulus < 1:
        raise ValueError("modulus must be at least 1")
    if k < 0 or k > n:  # @line L1
        return 0
    k = min(k, n - k)  # @line L2
    row = [0] * (k + 1)  # @line L3
    row[0] = 1 if modulus is None else 1 % modulus  # @line L4
    for i in range(1, n + 1):  # @line L5
        for j in range(min(i, k), 0, -1):  # @line L6
            s = row[j] + row[j - 1]  # @line L7
            row[j] = s if modulus is None else s % modulus
    return row[k]  # @line L8


def pascal_triangle(n: int, modulus: int | None = None) -> list[list[int]]:
    """Return rows 0 to n of Pascal's triangle, row i having i + 1 entries."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    if modulus is not None and modulus < 1:
        raise ValueError("modulus must be at least 1")
    one = 1 if modulus is None else 1 % modulus
    rows: list[list[int]] = [[one]]
    for i in range(1, n + 1):
        prev = rows[-1]
        cur = [one] * (i + 1)
        for j in range(1, i):
            s = prev[j - 1] + prev[j]
            cur[j] = s if modulus is None else s % modulus
        rows.append(cur)
    return rows


def count_additions(n: int, k: int) -> int:
    """Return how many times line L7 runs for the input (n, k)."""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    return sum(min(i, k) for i in range(1, n + 1))
