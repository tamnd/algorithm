# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maccormack-method/. The authors are listed in prov/6EZVM9.jsonl.

"""MacCormack's predictor-corrector scheme for U_t + F(U)_x = 0 on a uniform grid.

Each grid value is a state: a number for a scalar law, or a tuple for a system.
The arithmetic is generic, so Fraction data give exact results. The boundary is
periodic or transmissive (one ghost cell that copies the end value).
"""


def _as_tuple(v):
    return tuple(v) if isinstance(v, (tuple, list)) else (v,)


def _extend(u: list, bc: str) -> list:
    if bc == "periodic":
        return [u[-1]] + u + [u[0]]
    if bc == "transmissive":
        return [u[0]] + u + [u[-1]]
    raise ValueError("bc must be 'periodic' or 'transmissive'")


def _predict(ext: list, flux, lam):
    f = [flux(v) for v in ext]
    # predictor: forward difference, for the ghost cell on the left and the M cells
    pred = [tuple(a - lam * (b - c) for a, b, c in zip(ext[i], f[i + 1], f[i])) for i in range(len(ext) - 1)]
    return f, pred


def maccormack_step(u: list, flux, lam, bc: str = "periodic") -> list:
    """One step with lam = dt / dx. States and fluxes are tuples of equal length."""
    ext = _extend(u, bc)
    f, pred = _predict(ext, flux, lam)  # @line L2
    fp = [flux(v) for v in pred]
    # corrector: backward difference on the predicted values, then the average
    return [
        tuple((a + b) / 2 - lam * (c - d) / 2 for a, b, c, d in zip(ext[i], pred[i], fp[i], fp[i - 1]))  # @line L3
        for i in range(1, len(ext) - 1)
    ]


def numerical_flux(u: list, flux, lam, bc: str = "periodic") -> list:
    """The M + 1 face fluxes H = (F(U_right) + F(U*_left)) / 2. H[j] is on the left face of cell j and H[M] on the right end."""
    ext = _extend(u, bc)
    f, pred = _predict(ext, flux, lam)
    return [tuple((b + c) / 2 for b, c in zip(f[i + 1], flux(pred[i]))) for i in range(len(ext) - 1)]


def maccormack(u0: list, flux, dx, dt, steps: int, bc: str = "periodic", visc=0) -> list:
    """Run the given number of steps. Scalar data and a scalar flux are accepted and returned as scalars.

    visc > 0 adds visc * (U_(j+1) - 2 U_j + U_(j-1)) of the old values after each step, a constant
    artificial viscosity in conservation form. It damps the oscillations at shocks and makes the scheme
    first order. visc = 0 is the plain scheme.
    """
    scalar = not isinstance(u0[0], (tuple, list))
    u = [_as_tuple(v) for v in u0]
    vflux = (lambda v: (flux(v[0]),)) if scalar else (lambda v: _as_tuple(flux(v)))
    lam = dt / dx
    for _ in range(steps):  # @line L1
        new = maccormack_step(u, vflux, lam, bc)
        if visc:
            e = _extend(u, bc)
            new = [tuple(a + visc * (b - 2 * c + d) for a, b, c, d in zip(new[j], e[j + 2], e[j + 1], e[j])) for j in range(len(u))]
        u = new
    return [v[0] for v in u] if scalar else u  # @line L4
