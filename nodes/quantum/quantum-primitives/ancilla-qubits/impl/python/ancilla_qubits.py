# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ancilla-qubits/. The authors are listed in prov/HZ3JH4.jsonl.
"""Ancilla qubits in multi-controlled NOT circuits made of Toffoli gates.

1. v_chain: k controls, k - 2 clean ancillas (they must start at 0), 2k - 3 Toffoli gates.
2. mcx_dirty: k controls, k - 2 dirty ancillas (any start value, also any quantum state),
   4(k - 2) Toffoli gates (Barenco et al. 1995, Lemma 7.2).
3. mcx_one_ancilla: k controls and one dirty ancilla, 8(k - 3) Toffoli gates for k >= 5
   (Barenco et al. 1995, Corollary 7.4).

A gate is ("mcx", (c1, c2), t) for a Toffoli gate, as in qsim.py. Qubit 0 is the least significant bit.
"""


def toffoli(a: int, b: int, t: int) -> tuple:
    return ("mcx", (a, b), t)


def small_mcx(controls, target) -> list:
    """C^k X for k <= 2 with no ancilla: X, CNOT or one Toffoli gate."""
    controls = list(controls)
    if len(controls) == 0:
        return [("x", target)]
    if len(controls) == 1:
        return [("cx", controls[0], target)]
    if len(controls) == 2:
        return [toffoli(controls[0], controls[1], target)]
    raise ValueError("small_mcx takes at most two controls")


def v_chain(controls, target, ancillas) -> list:
    """C^k X with k - 2 clean ancillas. Ancilla i is set to c_1 c_2 ... c_{i+2}, the last one is
    used as a control of the final Toffoli gate, and the chain is then undone, so every ancilla is
    0 again. The result is correct only when the ancillas start at 0."""
    c = list(controls)
    k = len(c)
    if k <= 2:
        return small_mcx(c, target)
    a = list(ancillas)[: k - 2]
    if len(a) < k - 2:
        raise ValueError("the V-chain needs k - 2 ancillas")
    compute = [toffoli(c[0], c[1], a[0])]
    for i in range(1, k - 2):
        compute.append(toffoli(c[i + 1], a[i - 1], a[i]))
    return compute + [toffoli(c[k - 1], a[k - 3], target)] + list(reversed(compute))


def mcx_dirty(controls, target, dirty) -> list:
    """C^k X with k - 2 dirty ancillas, which end with the value they had at the start.

    Ancilla a_i (i = 1 .. k-2) is paired with control c_{i+2}. With D the "down and up" sweep
    T(c_{k-1}, a_{k-3} -> a_{k-2}) ... T(c_3, a_1 -> a_2) T(c_1, c_2 -> a_1) T(c_3, a_1 -> a_2) ...
    T(c_{k-1}, a_{k-3} -> a_{k-2}), the circuit is T(c_k, a_{k-2} -> t) D T(c_k, a_{k-2} -> t) D.
    """
    c = list(controls)
    k = len(c)
    if k <= 2:
        return small_mcx(c, target)
    a = list(dirty)[: k - 2]
    if len(a) < k - 2:
        raise ValueError("the circuit needs k - 2 dirty ancillas")
    # ladder[i] writes onto a[i]: a[0] ^= c1 c2, a[i] ^= c_{i+2} a[i-1]
    ladder = [toffoli(c[0], c[1], a[0])] + [toffoli(c[i + 1], a[i - 1], a[i]) for i in range(1, k - 2)]
    down = list(reversed(ladder))           # from a[k-3] down to a[0]
    sweep = down + ladder[1:]               # down, then back up, without repeating T(c1, c2 -> a1)
    top = toffoli(c[k - 1], a[k - 3], target)
    return [top] + sweep + [top] + sweep


def mcx_one_ancilla(controls, target, ancilla) -> list:
    """C^k X with one dirty ancilla. Split the controls into A (ceil(k/2) of them) and B (the rest):
    C^A X(A -> anc), C^(B+anc) X(-> t), C^A X(A -> anc), C^(B+anc) X(-> t). Each of the four gates
    uses the wires it does not touch as dirty ancillas."""
    c = list(controls)
    k = len(c)
    if k <= 2:
        return small_mcx(c, target)
    m1 = (k + 1) // 2
    group_a, group_b = c[:m1], c[m1:]
    first = mcx_dirty(group_a, ancilla, group_b + [target])
    second = mcx_dirty(group_b + [ancilla], target, group_a)
    return first + second + first + second


def toffoli_count(gates) -> int:
    return sum(1 for g in gates if g[0] == "mcx" and len(g[1]) == 2)


def mcx_permutation(n: int, controls, target) -> list:
    """C^k X on n wires as a permutation of the 2**n basis indices (the reference)."""
    mask = sum(1 << q for q in controls)
    return [x ^ (1 << target) if x & mask == mask else x for x in range(1 << n)]


def permutation_parity(perm) -> int:
    """0 for an even permutation and 1 for an odd one."""
    seen = [False] * len(perm)
    parity = 0
    for i in range(len(perm)):
        j, length = i, 0
        while not seen[j]:
            seen[j] = True
            j = perm[j]
            length += 1
        if length and length % 2 == 0:
            parity ^= 1
    return parity
