# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/long-division/. The authors are listed in prov/BHDBGW.jsonl.


def _normalize(a: list[int]) -> list[int]:
    while a and a[-1] == 0:
        a.pop()
    return a


def short_divide(u: list[int], v: int, base: int = 256) -> tuple[list[int], int]:
    """Divide the digit array u (least significant first) by one digit 0 < v < base.

    Returns (quotient digits, remainder). Each step divides a two-digit number
    r * base + u[j] by v, where r < v, so each quotient digit is below base.
    """
    if not 0 < v < base:
        raise ValueError("the divisor must be one nonzero digit")
    q = [0] * len(u)
    r = 0
    for j in range(len(u) - 1, -1, -1):
        t = r * base + u[j]
        q[j], r = divmod(t, v)
    return _normalize(q), r


def long_divide(u: list[int], v: list[int], base: int = 256, trace: list | None = None) -> tuple[list[int], list[int]]:
    """Knuth's Algorithm D: quotient and remainder of digit arrays in radix base.

    u and v are least significant digit first; v must be nonzero. The result
    arrays are normalized (no leading zero digits; zero is []). Cost:
    Theta(n (m + 1)) digit operations for n = len(v) and m = len(u) - n.
    """
    u = _normalize(list(u))
    v = _normalize(list(v))
    if not v:
        raise ZeroDivisionError("division by zero")
    n = len(v)
    if len(u) < n:
        return [], u
    if n == 1:
        q, r = short_divide(u, v[0], base)
        return q, ([r] if r else [])
    m = len(u) - n
    d = base // (v[-1] + 1)  # @line L1: normalize, so that v[n-1] >= base // 2
    u = _mul_digit(u, d, base) + [0]
    u = u[: m + n + 1] + [0] * (m + n + 1 - len(u))
    v = _mul_digit(v, d, base)[:n]
    q = [0] * (m + 1)
    for j in range(m, -1, -1):  # @line L2
        top = u[j + n] * base + u[j + n - 1]
        qhat, rhat = divmod(top, v[n - 1])  # @line L3: estimate from the leading digits
        while rhat < base and (qhat >= base or qhat * v[n - 2] > rhat * base + u[j + n - 2]):  # @line L4
            qhat -= 1
            rhat += v[n - 1]
        borrow = 0  # @line L5: u[j .. j + n] <- u[j .. j + n] - qhat * v
        carry = 0
        for i in range(n + 1):
            p = qhat * (v[i] if i < n else 0) + carry
            carry = p // base
            t = u[j + i] - (p % base) - borrow
            borrow = 1 if t < 0 else 0
            u[j + i] = t + base * borrow
        added_back = False
        if borrow:  # @line L6: qhat was one too large, add v back once
            qhat -= 1
            added_back = True
            c = 0
            for i in range(n + 1):
                t = u[j + i] + (v[i] if i < n else 0) + c
                u[j + i] = t % base
                c = t // base
        q[j] = qhat  # @line L7
        if trace is not None:
            trace.append((j, divmod(top, v[n - 1])[0], qhat, added_back))
    r, rest = short_divide(u[:n], d, base)  # @line L8: undo the normalization
    assert rest == 0
    return _normalize(q), r  # @line L9


def _mul_digit(a: list[int], d: int, base: int) -> list[int]:
    out = []
    c = 0
    for x in a:
        t = x * d + c
        out.append(t % base)
        c = t // base
    out.append(c)
    return out


def divmod_signed(a: int, b: int, base: int = 256) -> tuple[int, int]:
    """Floor division of Python ints through long_divide on their magnitudes.

    Returns (q, r) with a = q b + r and 0 <= r < |b| when b > 0, or -|b| < r <= 0 when b < 0,
    matching Python's divmod.
    """
    def to_digits(x: int) -> list[int]:
        out = []
        while x:
            x, t = divmod(x, base)
            out.append(t)
        return out

    def val(d: list[int]) -> int:
        x = 0
        for t in reversed(d):
            x = x * base + t
        return x

    qd, rd = long_divide(to_digits(abs(a)), to_digits(abs(b)), base)
    q, r = val(qd), val(rd)
    if (a < 0) != (b < 0):
        q = -q
        if r:
            q -= 1
            r = abs(b) - r
    if b < 0:
        r = -r
    return q, r
