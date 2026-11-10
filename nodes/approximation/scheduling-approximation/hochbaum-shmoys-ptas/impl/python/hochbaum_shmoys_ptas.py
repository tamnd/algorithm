# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hochbaum-shmoys-ptas/. The authors are listed in prov/KC7QKZ.jsonl.


def _configurations(sizes: list[int], cap: int) -> list[tuple[int, ...]]:
    """All nonzero count vectors c with sum of c[s] * sizes[s] at most cap."""
    out: list[tuple[int, ...]] = []

    def go(s: int, left: int, cur: list[int]) -> None:
        if s == len(sizes):
            if any(cur):
                out.append(tuple(cur))
            return
        c = 0
        while c * sizes[s] <= left:
            cur.append(c)
            go(s + 1, left - c * sizes[s], cur)
            cur.pop()
            c += 1

    go(0, cap, [])
    return out


def dual_test(p: list[int], m: int, k: int, T: int) -> list[int] | None:
    """The dual test with eps = 1/k.

    Returns an assignment (machine of each job) with makespan at most (1 + 1/k) T,
    or None, and None happens only if OPT > T.
    """
    n = len(p)
    if any(x > T for x in p):  # @line L6
        return None
    long_jobs = [j for j in range(n) if p[j] * k > T]
    r = {j: p[j] * k * k // T for j in long_jobs}  # @line L7
    sizes = sorted(set(r.values()))
    cls = {s: c for c, s in enumerate(sizes)}
    configs = _configurations(sizes, k * k)
    memo: dict[tuple[int, ...], tuple[int, tuple[int, ...] | None]] = {}

    def best(cnt: tuple[int, ...]) -> int:
        """Least number of machines for the long jobs with counts cnt, by dynamic programming."""
        if not any(cnt):
            return 0
        if cnt in memo:
            return memo[cnt][0]
        value, pick = n + 1, None
        for c in configs:
            if all(a <= b for a, b in zip(c, cnt)):
                v = 1 + best(tuple(b - a for a, b in zip(c, cnt)))
                if v < value:
                    value, pick = v, c
        memo[cnt] = (value, pick)
        return value

    counts = [0] * len(sizes)
    for j in long_jobs:
        counts[cls[r[j]]] += 1
    cnt = tuple(counts)
    if best(cnt) > m:  # @line L8
        return None  # @line L9
    sigma = [-1] * n
    load = [0] * m
    pools: dict[int, list[int]] = {}
    for j in long_jobs:
        pools.setdefault(cls[r[j]], []).append(j)
    machine = 0
    while any(cnt):  # @line L10
        c = memo[cnt][1]
        for s, a in enumerate(c):
            for _ in range(a):
                j = pools[s].pop()
                sigma[j] = machine
                load[machine] += p[j]
        cnt = tuple(b - a for a, b in zip(c, cnt))
        machine += 1
    for j in range(n):  # @line L11
        if sigma[j] != -1:
            continue
        i = min(range(m), key=lambda q: load[q])  # @line L12
        if load[i] > T:  # @line L13
            return None
        sigma[j] = i  # @line L14
        load[i] += p[j]
    return sigma  # @line L15


def hochbaum_shmoys(p: list[int], m: int, k: int) -> tuple[list[int], int]:
    """(1 + 1/k)-approximation for P||Cmax with positive integer times.

    Returns (sigma, T): sigma[j] is the machine of job j, T <= OPT, and the
    makespan of sigma is at most (1 + 1/k) T.
    """
    if m < 1 or k < 1:
        raise ValueError("m and k must be at least 1")
    if not p:
        return [], 0
    lb = max(max(p), -(-sum(p) // m))
    lo, hi = lb, 2 * lb  # @line L1
    while lo < hi:  # @line L2
        mid = (lo + hi) // 2  # @line L3
        if dual_test(p, m, k, mid) is not None:  # @line L4
            hi = mid
        else:
            lo = mid + 1
    return dual_test(p, m, k, hi), hi  # @line L5
