# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-svd/. The authors are listed in prov/0XCKNF.jsonl.
"""K-SVD dictionary learning (Aharon, Elad and Bruckstein, 2006).

Signals are a list of N vectors of length n. A dictionary is a list of K
atoms, each a vector of length n with norm 1. Codes are a list of N vectors
of length K with at most s nonzero entries each. The objective is

    F(D, X) = sum_i ||y_i - D x_i||^2  (the squared Frobenius norm of Y - D X).

Each iteration codes every signal with the current dictionary and then
updates the atoms one at a time. The update of atom k uses only the signals
whose code uses atom k, and replaces the atom and its coefficients on those
signals by the best rank 1 approximation of the restricted error matrix.
"""

from itertools import combinations

from imgla import svd


def _lstsq(cols, y, rcond=1e-12):
    """Minimum norm least squares coefficients of y on the given columns (by the SVD)."""
    n, p = len(y), len(cols)
    if p == 0:
        return []
    m = [[cols[j][i] for j in range(p)] for i in range(n)]
    u, sv, v = svd(m)
    if not sv or sv[0] == 0.0:
        return [0.0] * p
    coef = [0.0] * p
    for t, st in enumerate(sv):
        if st <= rcond * sv[0]:
            continue
        h = sum(u[i][t] * y[i] for i in range(n)) / st
        for j in range(p):
            coef[j] += v[j][t] * h
    return coef


def _combine(atoms, x):
    """D x for a dictionary given as a list of atoms."""
    n = len(atoms[0])
    out = [0.0] * n
    for k, xk in enumerate(x):
        if xk != 0.0:
            for i, v in enumerate(atoms[k]):
                out[i] += xk * v
    return out


def objective(signals, atoms, codes):
    """sum_i ||y_i - D x_i||^2."""
    total = 0.0
    for y, x in zip(signals, codes):
        total += sum((a - b) ** 2 for a, b in zip(y, _combine(atoms, x)))
    return total


def omp(atoms, y, s, tol=1e-12):
    """Orthogonal matching pursuit with at most s atoms. Ties go to the lower index."""
    kk = len(atoms)
    x = [0.0] * kk
    chosen = []
    r = list(y)
    ynorm = sum(v * v for v in y) ** 0.5
    for _ in range(min(s, kk)):
        best, best_c = -1, -1.0
        for k in range(kk):
            if k in chosen:
                continue
            c = abs(sum(a * b for a, b in zip(atoms[k], r)))
            if c > best_c:
                best, best_c = k, c
        if best_c <= tol * ynorm:
            break
        chosen.append(best)
        coef = _lstsq([atoms[k] for k in chosen], y)
        approx = _combine([atoms[k] for k in chosen], coef)
        r = [a - b for a, b in zip(y, approx)]
    if chosen:
        coef = _lstsq([atoms[k] for k in chosen], y)
        for k, c in zip(chosen, coef):
            x[k] = c
    return x


def exact_code(atoms, y, s):
    """The best code with at most s nonzero entries, by trying every support of size min(s, K)."""
    kk = len(atoms)
    best_x, best_r = [0.0] * kk, sum(v * v for v in y)
    for supp in combinations(range(kk), min(s, kk)):
        coef = _lstsq([atoms[k] for k in supp], y)
        approx = _combine([atoms[k] for k in supp], coef)
        r = sum((a - b) ** 2 for a, b in zip(y, approx))
        if r < best_r:
            best_r = r
            best_x = [0.0] * kk
            for k, c in zip(supp, coef):
                best_x[k] = c
    return best_x


def update_atom(signals, atoms, codes, k, replace_unused=True):
    """Update atom k and row k of the codes in place by a rank 1 SVD. Returns True if it changed."""
    omega = [i for i, x in enumerate(codes) if x[k] != 0.0]  # @line L4
    if not omega:  # @line L5
        if not replace_unused:
            return False
        # Replace an unused atom by the signal with the largest residual, normalized.
        # Row k of the codes is zero, so the objective does not change.
        worst, worst_r = -1, 0.0
        for i, (y, x) in enumerate(zip(signals, codes)):
            r = sum((a - b) ** 2 for a, b in zip(y, _combine(atoms, x)))
            if r > worst_r:
                worst, worst_r = i, r
        if worst < 0:
            return False
        res = [a - b for a, b in zip(signals[worst], _combine(atoms, codes[worst]))]
        nrm = sum(v * v for v in res) ** 0.5
        atoms[k] = [v / nrm for v in res]
        return True
    n = len(atoms[0])
    e_cols = []
    for i in omega:  # @line L6
        x = list(codes[i])
        x[k] = 0.0
        approx = _combine(atoms, x)
        e_cols.append([a - b for a, b in zip(signals[i], approx)])
    e = [[e_cols[c][r] for c in range(len(omega))] for r in range(n)]
    u, sv, v = svd(e)  # @line L7
    atoms[k] = [u[r][0] for r in range(n)]  # @line L8
    for c, i in enumerate(omega):
        codes[i][k] = sv[0] * v[c][0]
    return True


def ksvd(signals, atoms, s, iters=10, coder=omp, replace_unused=True):
    """Run K-SVD from the initial dictionary atoms (copied, not changed).

    Returns (atoms, codes, history), where history[j] is the pair
    (objective after the coding step, objective after the atom updates) of
    iteration j.
    """
    atoms = [list(a) for a in atoms]
    codes = []
    history = []
    for _ in range(iters):  # @line L1
        codes = [coder(atoms, y, s) for y in signals]  # @line L2
        after_coding = objective(signals, atoms, codes)
        for k in range(len(atoms)):  # @line L3
            update_atom(signals, atoms, codes, k, replace_unused)
        history.append((after_coding, objective(signals, atoms, codes)))
    return atoms, codes, history  # @line L9
