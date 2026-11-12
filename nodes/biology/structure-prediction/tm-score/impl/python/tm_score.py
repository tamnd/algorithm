# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tm-score/. The authors are listed in prov/NQBJJN.jsonl.

"""TM-score of a model against a native structure, C-alpha only, in angstrom,
for a fixed residue correspondence (model residue i is matched to native residue i).

  TM = max over rotations R and translations t of
       (1 / L) * sum_i 1 / (1 + (d_i / d0)^2),   d_i = |R x_i + t - y_i|,
  d0 = 1.24 (L - 15)^(1/3) - 1.8, at least 0.5 (Zhang and Skolnick 2004).

The maximum has no closed form. tm_score uses a heuristic search in the style
of the TM-score program: seeds from contiguous fragments of length L, L/2,
L/4, ... (at least 4), a least-RMSD fit on the seed, then repeated refits on
the residues closer than a search cutoff. Each fit is a least-RMSD
superposition (Horn's quaternion method), so the result is a lower bound of the
true maximum. Standard library only.
"""

import math

Vec = tuple[float, float, float]
Mat = list[list[float]]


def d0_of_length(length: int) -> float:
    if length <= 15:
        return 0.5
    return max(1.24 * (length - 15) ** (1.0 / 3.0) - 1.8, 0.5)


def _jacobi_top(a: Mat, sweeps: int = 50) -> list[float]:
    """Eigenvector of the largest eigenvalue of a small symmetric matrix (cyclic Jacobi)."""
    n = len(a)
    a = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
        if off <= 1e-30 * (1.0 + sum(a[i][i] ** 2 for i in range(n))):
            break
        for p in range(n):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    top = max(range(n), key=lambda i: a[i][i])
    return [v[r][top] for r in range(n)]


def superpose(xs: list[Vec], ys: list[Vec]) -> tuple[Mat, Vec]:
    """Least-RMSD rotation and translation of xs onto ys (Horn's quaternion method)."""
    n = len(xs)
    cx = [sum(p[k] for p in xs) / n for k in range(3)]
    cy = [sum(p[k] for p in ys) / n for k in range(3)]
    s = [[0.0] * 3 for _ in range(3)]
    for p, q in zip(xs, ys):
        a = (p[0] - cx[0], p[1] - cx[1], p[2] - cx[2])
        b = (q[0] - cy[0], q[1] - cy[1], q[2] - cy[2])
        for r in range(3):
            for c in range(3):
                s[r][c] += a[r] * b[c]
    (sxx, sxy, sxz), (syx, syy, syz), (szx, szy, szz) = s
    nm = [[sxx + syy + szz, syz - szy, szx - sxz, sxy - syx],
          [syz - szy, sxx - syy - szz, sxy + syx, szx + sxz],
          [szx - sxz, sxy + syx, -sxx + syy - szz, syz + szy],
          [sxy - syx, szx + sxz, syz + szy, -sxx - syy + szz]]
    w, x, y, z = _jacobi_top(nm)
    rot = [[w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
           [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
           [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z]]
    t = tuple(cy[r] - sum(rot[r][c] * cx[c] for c in range(3)) for r in range(3))
    return rot, t


def distances(rot: Mat, t: Vec, xs: list[Vec], ys: list[Vec]) -> list[float]:
    out = []
    for p, q in zip(xs, ys):
        m = [sum(rot[r][c] * p[c] for c in range(3)) + t[r] for r in range(3)]
        out.append(math.sqrt((m[0] - q[0]) ** 2 + (m[1] - q[1]) ** 2 + (m[2] - q[2]) ** 2))
    return out


def score_for(rot: Mat, t: Vec, xs: list[Vec], ys: list[Vec], d0: float, length: int) -> float:
    return sum(1.0 / (1.0 + (d / d0) ** 2) for d in distances(rot, t, xs, ys)) / length


def tm_score(model: list[Vec], native: list[Vec], length: int | None = None,
             iterations: int = 20) -> tuple[float, Mat, Vec]:
    """Heuristic TM-score of model against native (pairs i <-> i). length is the
    normalization length L, by default len(native). Returns (score, R, t)."""
    n = len(model)
    if n != len(native):
        raise ValueError("model and native must have the same number of matched residues")
    big_l = len(native) if length is None else length
    if n < 3:
        raise ValueError("need at least 3 matched residues")
    d0 = d0_of_length(big_l)
    d_search = min(max(d0, 4.5), 8.0)
    best = (-1.0, None, None)
    seen: set[tuple[int, ...]] = set()
    frag = n
    while True:
        for start in range(0, n - frag + 1):
            sel = tuple(range(start, start + frag))
            for _ in range(iterations):
                if sel in seen:
                    break
                seen.add(sel)
                rot, t = superpose([model[i] for i in sel], [native[i] for i in sel])
                ds = distances(rot, t, model, native)
                sc = sum(1.0 / (1.0 + (d / d0) ** 2) for d in ds) / big_l
                if sc > best[0]:
                    best = (sc, rot, t)
                cut = d_search
                nxt = tuple(i for i in range(n) if ds[i] < cut)
                while len(nxt) < 3:  # widen the cutoff until three residues are left
                    cut += 0.5
                    nxt = tuple(i for i in range(n) if ds[i] < cut)
                sel = nxt
        if frag <= 4:
            break
        frag = max(frag // 2, 4)
    return best
