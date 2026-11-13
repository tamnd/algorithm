# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-combination-of-unitaries/. The authors are listed in prov/XGJBQG.jsonl.
"""A linear combination of unitaries with oblivious amplitude amplification.

The joint state of the ancilla index register and the system is a list of
system vectors, parts[j] = (<j| (x) I) |state>, one for each ancilla basis state j.
"""

import math

from qsim import householder, matvec, norm


def prep_matrix(betas):
    """B with B|0> = s^(-1/2) sum_j sqrt(beta_j) |j>, padded to a power of two. B is Hermitian, so B^dagger = B."""
    m = 1 << max(1, math.ceil(math.log2(len(betas))))
    s = sum(betas)
    v = [complex(math.sqrt(b / s)) for b in betas] + [0j] * (m - len(betas))
    return householder(v)


def apply_ancilla_matrix(b, parts):
    """(B (x) I) on the list form: new parts[i] = sum_j B[i][j] parts[j]."""
    d = len(parts[0])
    out = []
    for i in range(len(b)):
        v = [0j] * d
        for j, bij in enumerate(b[i]):
            if bij != 0:
                pj = parts[j]
                for x in range(d):
                    v[x] += bij * pj[x]
        out.append(v)
    return out


def apply_select(unitaries, parts, inverse=False):
    """SELECT = sum_j |j><j| (x) U_j, the identity on unused indices."""
    out = []
    for j, p in enumerate(parts):
        if j < len(unitaries):
            u = unitaries[j]
            if inverse:
                u = [[u[k][i].conjugate() for k in range(len(u))] for i in range(len(u))]
            out.append(matvec(u, p))
        else:
            out.append(list(p))
    return out


def apply_w(b, unitaries, parts, inverse=False):
    """W = (B^dagger (x) I) SELECT (B (x) I), and W^dagger with inverse=True (B is Hermitian)."""
    return apply_ancilla_matrix(b, apply_select(unitaries, apply_ancilla_matrix(b, parts), inverse))


def reflect_zero(parts):
    """R = 2 |0><0| (x) I - I: keep the ancilla-0 part and negate the rest."""
    return [list(parts[0])] + [[-x for x in p] for p in parts[1:]]


def lcu_oaa(betas, unitaries, psi, rounds):
    """Run W and then `rounds` steps of S = -W R W^dagger R on |0>|psi>. Returns the final parts."""
    s = sum(betas)  # @line L1
    b = prep_matrix(betas)  # @line L2
    m = len(b)
    parts = [list(psi)] + [[0j] * len(psi) for _ in range(m - 1)]
    parts = apply_w(b, unitaries, parts)  # @line L3
    for _ in range(rounds):  # @line L4
        parts = reflect_zero(parts)  # @line L5
        parts = apply_w(b, unitaries, parts, inverse=True)
        parts = reflect_zero(parts)
        parts = apply_w(b, unitaries, parts)
        parts = [[-x for x in p] for p in parts]
    p0 = norm(parts[0]) ** 2  # @line L6
    return parts, p0


def rounds_for(s):
    """The least l with s <= 1/sin(pi/(2(2l + 1))), and the padded s for which l rounds are exact."""
    rounds = 0
    while 1 / math.sin(math.pi / (2 * (2 * rounds + 1))) < s - 1e-12:
        rounds += 1
    return rounds, 1 / math.sin(math.pi / (2 * (2 * rounds + 1)))


def pad_to(betas, unitaries, target_s):
    """Add the pair +c I and -c I with 2c = target_s - s. The sum is unchanged and its 1-norm becomes target_s."""
    s = sum(betas)
    if target_s < s - 1e-12:
        raise ValueError("cannot pad down")
    c = (target_s - s) / 2
    if c <= 1e-15:
        return list(betas), list(unitaries)
    d = len(unitaries[0])
    eye = [[1 + 0j if i == j else 0j for j in range(d)] for i in range(d)]
    minus = [[-x for x in row] for row in eye]
    return list(betas) + [c, c], list(unitaries) + [eye, minus]


def implement_exactly(betas, unitaries, psi):
    """Apply V = sum_j beta_j U_j (assumed unitary) to psi with probability 1: pad, then amplify."""
    rounds, s_target = rounds_for(sum(betas))
    bp, up = pad_to(betas, unitaries, s_target)
    parts, p0 = lcu_oaa(bp, up, psi, rounds)
    return parts[0], p0, rounds
