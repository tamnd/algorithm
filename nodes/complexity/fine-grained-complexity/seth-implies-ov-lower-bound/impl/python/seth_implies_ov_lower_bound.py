# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/seth-implies-ov-lower-bound/. The authors are listed in prov/CX4N6X.jsonl.

"""Williams' split-and-list reduction from CNF-SAT to Orthogonal Vectors.

A formula is a list of clauses. A clause is a list of nonzero integers in
the DIMACS style: the literal v means x_v and -v means "not x_v", for
variables 1..N. A vector is a tuple of 0-1 integers with one coordinate
per clause.
"""

from itertools import product

Clause = list[int]
Vector = tuple[int, ...]


def _vector(clauses: list[Clause], half: dict[int, int]) -> Vector:
    """Coordinate j is 1 when the partial assignment makes no literal of clause j true."""
    out = []
    for clause in clauses:
        hit = any(abs(lit) in half and (lit > 0) == (half[abs(lit)] == 1) for lit in clause)
        out.append(0 if hit else 1)
    return tuple(out)


def halves(nvars: int) -> tuple[list[int], list[int]]:
    """The two halves of the variables. An odd N gets the dummy variable N + 1."""
    n = nvars + 1 if nvars % 2 else nvars  # @line L1
    h = n // 2  # @line L2
    return list(range(1, h + 1)), list(range(h + 1, n + 1))


def sat_to_ov(clauses: list[Clause], nvars: int) -> tuple[list[Vector], list[Vector]]:
    """Return the lists A and B, with 2^(N/2) vectors each and dimension m.

    The i-th vector of A belongs to the i-th assignment of the first half, in
    the order of itertools.product over the values 0 and 1; the same holds for B.
    """
    for clause in clauses:
        for lit in clause:
            if lit == 0 or abs(lit) > nvars:
                raise ValueError(f"literal {lit} is not over the variables 1..{nvars}")
    first, second = halves(nvars)
    a_list: list[Vector] = []
    b_list: list[Vector] = []
    for bits in product((0, 1), repeat=len(first)):  # @line L3
        a_list.append(_vector(clauses, dict(zip(first, bits))))  # @line L4
    for bits in product((0, 1), repeat=len(second)):  # @line L5
        b_list.append(_vector(clauses, dict(zip(second, bits))))  # @line L6
    return a_list, b_list  # @line L7


def pair_to_assignment(nvars: int, i: int, j: int) -> list[int]:
    """Map the pair (A[i], B[j]) to an assignment of x_1..x_N, as a list of 0-1 values."""
    first, second = halves(nvars)
    alpha = list(product((0, 1), repeat=len(first)))[i]
    beta = list(product((0, 1), repeat=len(second)))[j]
    full = list(alpha) + list(beta)
    return full[:nvars]


def assignment_to_pair(nvars: int, assignment: list[int]) -> tuple[int, int]:
    """Map an assignment of x_1..x_N to the indices (i, j) of its two halves.

    The dummy variable of an odd N gets the value 0.
    """
    first, second = halves(nvars)
    values = list(assignment) + [0] * (len(first) + len(second) - nvars)
    alpha = values[: len(first)]
    beta = values[len(first):]
    i = int("".join(map(str, alpha)) or "0", 2)
    j = int("".join(map(str, beta)) or "0", 2)
    return i, j
