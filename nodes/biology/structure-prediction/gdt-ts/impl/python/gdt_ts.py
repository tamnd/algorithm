# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gdt-ts/. The authors are listed in prov/36CBME.jsonl.

"""GDT-TS of a model against a native structure, C-alpha only, in angstrom,
for a fixed residue correspondence (model residue i is matched to native residue i).

  P_c = 100 / L * max over rotations R and translations t of #{i : |R x_i + t - y_i| <= c}
  GDT-TS = (P_1 + P_2 + P_4 + P_8) / 4

Each maximum has no closed form. gdt_counts uses a heuristic search in the
style of LGA: seeds from contiguous fragments, a least-RMSD fit on the seed,
then repeated refits on the residues within the cutoff, for each cutoff.
Each superposition seen updates the counts of all cutoffs, so P_1 <= P_2 <=
P_4 <= P_8 holds. Each count is a lower bound of the true maximum.
Standard library only.
"""

import math

Vec = tuple[float, float, float]
Mat = list[list[float]]

TS_CUTOFFS = (1.0, 2.0, 4.0, 8.0)
HA_CUTOFFS = (0.5, 1.0, 2.0, 4.0)


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


def gdt_counts(model: list[Vec], native: list[Vec], cutoffs: tuple[float, ...] = TS_CUTOFFS,
               min_seed: int = 3, iterations: int = 20) -> list[int]:
    """For each cutoff c, the largest number of residues within c of the native
    found by the search. Never fits fewer than 3 residues."""
    n = len(model)
    if n != len(native):
        raise ValueError("model and native must have the same number of matched residues")
    if n < 3:
        raise ValueError("need at least 3 matched residues")
    best = [0] * len(cutoffs)
    cache: dict[tuple[int, ...], list[float]] = {}

    def fit(sel: tuple[int, ...]) -> list[float]:
        if sel not in cache:
            rot, t = superpose([model[i] for i in sel], [native[i] for i in sel])
            ds = distances(rot, t, model, native)
            cache[sel] = ds
            for k, c in enumerate(cutoffs):
                best[k] = max(best[k], sum(1 for d in ds if d <= c))
        return cache[sel]

    frag = n
    while True:
        for start in range(0, n - frag + 1):
            seed = tuple(range(start, start + frag))
            for c in cutoffs:
                sel = seed
                for _ in range(iterations):
                    ds = fit(sel)
                    nxt = tuple(i for i in range(n) if ds[i] <= c)
                    if len(nxt) < 3 or nxt == sel:
                        break
                    sel = nxt
        if frag <= min_seed:
            break
        frag = max(frag // 2, min_seed)
    return best


def gdt_ts(model: list[Vec], native: list[Vec], length: int | None = None) -> float:
    """GDT-TS in percent, normalized by length (default: len(native))."""
    big_l = len(native) if length is None else length
    counts = gdt_counts(model, native, TS_CUTOFFS)
    return sum(100.0 * k / big_l for k in counts) / len(TS_CUTOFFS)


def gdt_ha(model: list[Vec], native: list[Vec], length: int | None = None) -> float:
    """GDT-HA in percent: the same with the cutoffs 0.5, 1, 2 and 4 angstrom."""
    big_l = len(native) if length is None else length
    counts = gdt_counts(model, native, HA_CUTOFFS)
    return sum(100.0 * k / big_l for k in counts) / len(HA_CUTOFFS)
