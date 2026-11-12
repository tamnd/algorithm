# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/benes-network-routing/. The authors are listed in prov/ZPDNJR.jsonl.

"""Route a permutation through a Benes network with the looping algorithm.

The Benes network on N = 2^n lines is built as follows. For N = 2 it is one
2 x 2 switch. For N >= 4 it has a first column of N/2 switches, an upper and a
lower Benes network on N/2 lines, and a last column of N/2 switches. Input
switch k takes lines 2k and 2k+1; its top output goes to line k of the upper
subnetwork and its bottom output to line k of the lower subnetwork. Output
switch k takes line k of the upper subnetwork on top and line k of the lower
subnetwork at the bottom, and drives lines 2k and 2k+1.

A switch setting is 0 (straight: top to top) or 1 (cross: top to bottom).
The routing of perm (input x goes to output perm[x]) is a nested tuple:
("switch", bit) for N = 2, else ("benes", in_bits, upper, lower, out_bits).
"""


def route(perm: list[int]):
    n = len(perm)
    if n < 2 or n & (n - 1):
        raise ValueError("the number of lines must be a power of 2, at least 2")
    if n == 2:  # @line L1
        return ("switch", perm[0])
    inv = [0] * n
    for x, y in enumerate(perm):
        inv[y] = x
    up = [None] * n  # @line L2
    for x in range(n):  # @line L3
        if up[x] is not None:
            continue
        y = x  # @line L4
        while up[y] is None:  # @line L5
            up[y], up[y ^ 1] = True, False  # @line L6
            y = inv[perm[y ^ 1] ^ 1]  # @line L7
    in_bits = [0 if up[2 * k] else 1 for k in range(n // 2)]  # @line L8
    out_bits = [0 if up[inv[2 * k]] else 1 for k in range(n // 2)]  # @line L9
    perm_up = [0] * (n // 2)
    perm_low = [0] * (n // 2)
    for x in range(n):  # @line L10
        if up[x]:
            perm_up[x >> 1] = perm[x] >> 1
        else:
            perm_low[x >> 1] = perm[x] >> 1
    upper = route(perm_up)  # @line L11
    lower = route(perm_low)
    return ("benes", in_bits, upper, lower, out_bits)  # @line L12


def apply(net, values: list) -> list:
    """Push values through the set network: values[x] enters input line x."""
    if net[0] == "switch":
        return values[:] if net[1] == 0 else [values[1], values[0]]
    _, in_bits, upper, lower, out_bits = net
    half = len(values) // 2
    top, bottom = [None] * half, [None] * half
    for k in range(half):
        a, b = values[2 * k], values[2 * k + 1]
        top[k], bottom[k] = (a, b) if in_bits[k] == 0 else (b, a)
    top, bottom = apply(upper, top), apply(lower, bottom)
    out = [None] * len(values)
    for k in range(half):
        a, b = top[k], bottom[k]
        out[2 * k], out[2 * k + 1] = (a, b) if out_bits[k] == 0 else (b, a)
    return out


def realizes(net, perm: list[int]) -> bool:
    """True if the value that enters input x leaves at output perm[x], for all x."""
    out = apply(net, list(range(len(perm))))
    return all(out[perm[x]] == x for x in range(len(perm)))


def switch_count(net) -> int:
    if net[0] == "switch":
        return 1
    _, in_bits, upper, lower, out_bits = net
    return len(in_bits) + switch_count(upper) + switch_count(lower) + len(out_bits)


def first_switches_straight(net) -> bool:
    """Waksman's observation: the looping algorithm never crosses input switch 0
    of a subnetwork with N >= 4, so that switch can be a plain wire."""
    if net[0] == "switch":
        return True
    _, in_bits, upper, lower, _ = net
    return in_bits[0] == 0 and first_switches_straight(upper) and first_switches_straight(lower)


def stage_count(n: int) -> int:
    """Columns of switches: 2 log2 N - 1."""
    return 2 * (n.bit_length() - 1) - 1
