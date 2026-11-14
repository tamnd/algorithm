# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sum-of-coherent-systems/. The authors are listed in prov/5NQR8Z.jsonl.
"""Sum of coherent systems (SOCS) for a one-dimensional periodic mask.

Units: frequencies are in units of NA / wavelength, lengths in wavelength / NA. The mask
has period P and is given by samples m[0..N-1] at x = n P / N; its spectrum is the
discrete Fourier transform M(k) = (1/N) sum_n m[n] exp(-2 pi i k n / N), at the
frequency k / P. The source is a list of points (s, J) with weights J >= 0. The pupil
is a function of the frequency, zero outside [-1, 1].

The transmission cross coefficient on the band of integers k is
    T[k1][k2] = sum over source points of J * H(k1/P + s) * conj(H(k2/P + s)),
a Hermitian positive semidefinite matrix. Its eigendecomposition
T = sum_j lam_j v_j v_j^* gives I(x) = sum_j lam_j |sum_k v_j[k] M(k) e^{2 pi i k x / P}|^2.
"""

import cmath
import math


def ideal_pupil(defocus=0.0, coma=0.0):
    """Pupil 1 on |f| <= 1 times a phase exp(2 pi i (defocus f^2 + coma f^3))."""
    def H(f):
        if abs(f) > 1 + 1e-12:
            return 0j
        return cmath.exp(2j * math.pi * (defocus * f * f + coma * f ** 3))
    return H


def source_points(sigma, count):
    """count equally weighted points spread evenly over [-sigma, sigma], total weight 1."""
    if count == 1:
        return [(0.0, 1.0)]
    return [(-sigma + 2 * sigma * i / (count - 1), 1.0 / count) for i in range(count)]


def band(P, sigma):
    """The integers k with |k / P| <= 1 + sigma, where T can be nonzero."""
    kmax = int(math.floor((1 + sigma) * P + 1e-9))
    return list(range(-kmax, kmax + 1))


def tcc(ks, P, source, H):
    n = len(ks)
    T = [[0j] * n for _ in range(n)]
    for s, w in source:
        h = [H(k / P + s) for k in ks]
        for a in range(n):
            if h[a] == 0:
                continue
            for b in range(n):
                T[a][b] += w * h[a] * h[b].conjugate()  # @line L1
    return T


def off_norm(A):
    n = len(A)
    return math.sqrt(sum(abs(A[i][j]) ** 2 for i in range(n) for j in range(n) if i != j))


def jacobi_hermitian(T, tol=1e-14, max_sweeps=60):
    """Eigenvalues and eigenvectors of a Hermitian matrix by cyclic complex Jacobi rotations.

    Returns (lams, V) with T = V diag(lams) V^*, V unitary, columns the eigenvectors.
    Each rotation U = W R first turns a[p][q] real with the phase W = diag(1, e^{-i phi})
    and then zeroes it with a real plane rotation R.
    """
    n = len(T)
    A = [row[:] for row in T]
    V = [[1 + 0j if i == j else 0j for j in range(n)] for i in range(n)]
    scale = math.sqrt(sum(abs(A[i][j]) ** 2 for i in range(n) for j in range(n))) or 1.0
    for _ in range(max_sweeps):
        if off_norm(A) <= tol * scale:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                g = A[p][q]
                if abs(g) <= 1e-300:
                    continue
                r = abs(g)
                e = g / r  # e^{i phi}
                theta = (A[q][q].real - A[p][p].real) / (2 * r)
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                # U = [[c, s], [-s e^{-i phi}, c e^{-i phi}]] acting on columns p and q.
                upp, upq = c, s
                uqp, uqq = -s * e.conjugate(), c * e.conjugate()
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = akp * upp + akq * uqp
                    A[k][q] = akp * upq + akq * uqq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = upp * apk + uqp.conjugate() * aqk
                    A[q][k] = upq * apk + uqq.conjugate() * aqk
                A[p][q] = A[q][p] = 0j
                for k in range(n):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p] = vkp * upp + vkq * uqp
                    V[k][q] = vkp * upq + vkq * uqq  # @line L2
    lams = [A[i][i].real for i in range(n)]
    return lams, V


def socs_kernels(T, K):
    """The K largest eigenvalues of T, with their eigenvectors (the kernel spectra)."""
    lams, V = jacobi_hermitian(T)
    order = sorted(range(len(lams)), key=lambda j: -lams[j])  # @line L3
    n = len(T)
    return [(lams[j], [V[i][j] for i in range(n)]) for j in order[:K]]  # @line L4


def mask_spectrum(mask, ks):
    N = len(mask)
    return [sum(mask[n] * cmath.exp(-2j * math.pi * k * n / N) for n in range(N)) / N for k in ks]  # @line L5


def coherent_field(phi, M, ks, x, P):
    return sum(p * m * cmath.exp(2j * math.pi * k * x / P) for p, m, k in zip(phi, M, ks))


def socs_image(kernels, M, ks, xs, P):
    """I_K(x) = sum_j lam_j |E_j(x)|^2 at the points xs."""
    out = []
    for x in xs:
        total = 0.0
        for lam, phi in kernels:  # @line L6
            E = coherent_field(phi, M, ks, x, P)  # @line L7
            total += lam * abs(E) ** 2
        out.append(total)  # @line L8
    return out


def sum_of_coherent_systems(mask, P, source, H, K, xs):
    """Build the TCC, keep K kernels, and return (image at xs, all eigenvalues sorted)."""
    ks = band(P, max(abs(s) for s, _ in source))
    T = tcc(ks, P, source, H)
    kernels = socs_kernels(T, len(ks))
    M = mask_spectrum(mask, ks)
    return socs_image(kernels[:K], M, ks, xs, P), [lam for lam, _ in kernels]


def hopkins_image(T, M, ks, xs, P):
    """The direct Hopkins double sum over pairs of frequencies."""
    n = len(ks)
    out = []
    for x in xs:
        e = [M[a] * cmath.exp(2j * math.pi * ks[a] * x / P) for a in range(n)]
        total = sum(T[a][b] * e[a] * e[b].conjugate() for a in range(n) for b in range(n))
        out.append(total.real)
    return out


def abbe_image(source, H, M, ks, xs, P):
    """The image summed over source points, one coherent image per point."""
    out = []
    for x in xs:
        total = 0.0
        for s, w in source:
            E = sum(H(k / P + s) * m * cmath.exp(2j * math.pi * k * x / P) for k, m in zip(ks, M))
            total += w * abs(E) ** 2
        out.append(total)
    return out
