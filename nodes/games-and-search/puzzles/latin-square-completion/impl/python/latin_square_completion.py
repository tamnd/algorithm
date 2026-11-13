# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/latin-square-completion/. The authors are listed in prov/5D4CRB.jsonl.
"""Completion of partial Latin squares.

A partial Latin square of order n is an n by n list of rows whose entries are
symbols 0..n-1 or None, with no symbol twice in a row or a column.

complete_latin searches all completions by backtracking with the
fewest-candidates rule. extend_rectangle completes a k by n Latin rectangle
row by row by bipartite matching, as in Marshall Hall's 1945 proof.
"""


def is_partial_latin(square):
    """True when no symbol repeats in a row or in a column."""
    n = len(square)
    for i in range(n):
        seen_row = set()
        seen_col = set()
        for j in range(n):
            a = square[i][j]
            b = square[j][i]
            if a is not None:
                if a in seen_row:
                    return False
                seen_row.add(a)
            if b is not None:
                if b in seen_col:
                    return False
                seen_col.add(b)
    return True


def is_latin(square):
    """True when the square is full and each row and column is a permutation."""
    n = len(square)
    full = set(range(n))
    return all(set(row) == full for row in square) and all(
        {square[i][j] for i in range(n)} == full for j in range(n))


def complete_latin(partial, limit=None):
    """All completions of a partial Latin square (at most limit of them)."""
    n = len(partial)
    if not is_partial_latin(partial):
        return []
    sq = [list(row) for row in partial]
    full = (1 << n) - 1
    rows = [0] * n
    cols = [0] * n
    empty = []
    for i in range(n):
        for j in range(n):
            v = sq[i][j]
            if v is None:
                empty.append((i, j))
            else:
                rows[i] |= 1 << v
                cols[j] |= 1 << v
    out = []

    def search(k):
        if limit is not None and len(out) >= limit:
            return
        if k == len(empty):
            out.append([list(row) for row in sq])
            return
        best, best_count, best_mask = -1, n + 1, 0
        for idx in range(k, len(empty)):
            i, j = empty[idx]
            mask = full & ~(rows[i] | cols[j])
            count = bin(mask).count("1")
            if count < best_count:
                best, best_count, best_mask = idx, count, mask
                if count <= 1:
                    break
        if best_count == 0:
            return
        empty[k], empty[best] = empty[best], empty[k]
        i, j = empty[k]
        mask = best_mask
        while mask:
            bit = mask & -mask
            mask ^= bit
            sq[i][j] = bit.bit_length() - 1
            rows[i] |= bit
            cols[j] |= bit
            search(k + 1)
            rows[i] ^= bit
            cols[j] ^= bit
            sq[i][j] = None
            if limit is not None and len(out) >= limit:
                break
        empty[k], empty[best] = empty[best], empty[k]

    search(0)
    return out


def perfect_matching(adj, n):
    """A perfect matching of a bipartite graph with n left and n right vertices.

    adj[u] lists the right neighbors of left vertex u. Returns match_left, a
    list with the right partner of each left vertex, or None when no perfect
    matching exists. The method is augmenting paths (Kuhn), with an explicit
    stack instead of recursion.
    """
    match_left = [-1] * n
    match_right = [-1] * n
    for root in range(n):
        parent = {}
        seen = set()
        stack = [root]
        end = -1
        while stack and end < 0:
            u = stack.pop()
            for w in adj[u]:
                if w in seen:
                    continue
                seen.add(w)
                parent[w] = u
                if match_right[w] < 0:
                    end = w
                    break
                stack.append(match_right[w])
        if end < 0:
            return None
        w = end
        while True:
            u = parent[w]
            prev = match_left[u]
            match_left[u] = w
            match_right[w] = u
            if u == root:
                break
            w = prev
    return match_left


def extend_rectangle(rect, n):
    """Extend a k by n Latin rectangle to an n by n Latin square.

    For each new row, column j may take any symbol that column j does not yet
    hold. With k rows filled, this bipartite graph is (n - k)-regular, so it
    has a perfect matching, and the matching is the next row.
    """
    rows = [list(r) for r in rect]
    while len(rows) < n:  # @line L1
        used = [set(r[j] for r in rows) for j in range(n)]
        adj = [[s for s in range(n) if s not in used[j]] for j in range(n)]  # @line L2
        m = perfect_matching(adj, n)  # @line L3
        if m is None:
            raise ValueError("not a Latin rectangle")
        rows.append(m)  # @line L4
    return rows  # @line L5


def evans_counterexample(n):
    """A partial Latin square with n filled cells and no completion (n >= 2).

    Row 0 holds symbols 0..n-2 in columns 0..n-2, and cell (1, n-1) holds n-1.
    Cell (0, n-1) must then hold n-1, which column n-1 already holds.
    """
    sq = [[None] * n for _ in range(n)]
    for j in range(n - 1):
        sq[0][j] = j
    sq[1][n - 1] = n - 1
    return sq
