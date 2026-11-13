# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/open-quantum-system-simulation/. The authors are listed in prov/12TXF0.jsonl.
"""Exact reference solutions of small Lindblad equations.

d rho / dt = -i [H, rho] + sum_k (L_k rho L_k^dagger - 1/2 {L_k^dagger L_k, rho}).

A d x d density matrix is stored row by row as a vector of length d^2, so that
vec(A rho B) = (A kron B^T) vec(rho). The generator is then a d^2 x d^2 matrix
and rho(t) = exp(t L) rho(0), computed by a Taylor series with scaling and squaring.
"""

from qsim import add, dagger, expm_taylor, identity, kron, matmul, matvec, scale, zeros


def transpose(a):
    return [list(row) for row in zip(*a)]


def conj(a):
    return [[x.conjugate() for x in row] for row in a]


def lindbladian(h, jumps):
    """The d^2 x d^2 matrix of the Lindblad generator for the Hamiltonian h and the jump operators."""
    d = len(h)
    eye = identity(d)
    gen = scale(-1j, add(kron(h, eye), scale(-1, kron(eye, transpose(h)))))
    for l in jumps:
        ldl = matmul(dagger(l), l)
        gen = add(gen, kron(l, conj(l)))
        gen = add(gen, scale(-0.5, add(kron(ldl, eye), kron(eye, transpose(ldl)))))
    return gen


def vec(rho):
    return [x for row in rho for x in row]


def unvec(v, d):
    return [v[i * d:(i + 1) * d] for i in range(d)]


def evolve(h, jumps, rho, t):
    """rho(t) = exp(t L) rho(0)."""
    d = len(rho)
    prop = expm_taylor(scale(t, lindbladian(h, jumps)))
    return unvec(matvec(prop, vec(rho)), d)


def apply_generator(h, jumps, rho):
    """L(rho), computed straight from the formula, for a check of the matrix form."""
    comm = add(matmul(h, rho), scale(-1, matmul(rho, h)))
    out = scale(-1j, comm)
    for l in jumps:
        ld = dagger(l)
        ldl = matmul(ld, l)
        out = add(out, matmul(matmul(l, rho), ld))
        out = add(out, scale(-0.5, add(matmul(ldl, rho), matmul(rho, ldl))))
    return out


def purity(rho):
    return sum((rho[i][k] * rho[k][i]) for i in range(len(rho)) for k in range(len(rho))).real


def choi(h, jumps, t):
    """The Choi matrix sum_ij |i><j| (x) E_t(|i><j|) of the channel E_t = exp(t L)."""
    d = len(h)
    prop = expm_taylor(scale(t, lindbladian(h, jumps)))
    c = zeros(d * d)
    for i in range(d):
        for j in range(d):
            e = zeros(d)
            e[i][j] = 1 + 0j
            out = unvec(matvec(prop, vec(e)), d)
            for a in range(d):
                for b in range(d):
                    c[i * d + a][j * d + b] = out[a][b]
    return c


def partial_trace_first(rho, d1, d2):
    """Trace out the first (left, more significant) factor of a (d1 d2) x (d1 d2) matrix."""
    out = zeros(d2)
    for a in range(d1):
        for i in range(d2):
            for j in range(d2):
                out[i][j] += rho[a * d2 + i][a * d2 + j]
    return out
