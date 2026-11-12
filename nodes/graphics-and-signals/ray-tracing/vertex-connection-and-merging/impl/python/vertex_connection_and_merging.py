# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-connection-and-merging/. The authors are listed in prov/PT5JRY.jsonl.

"""Vertex connection and merging (Georgiev, Krivanek, Davidovic and Slusallek 2012).

One iteration traces n light subpaths and n camera subpaths. Each camera vertex is
connected to an emitter (next event estimation), connected to every vertex of its own
light subpath, and merged with the light vertices of all n subpaths within the radius r.
The balance heuristic weights come from three quantities per subpath vertex, dVCM, dVC and
dVM, which are updated at each step as in Georgiev's technical report "Implementing vertex
connection and merging" (2012). Here eta = n pi r^2.

The camera is a point that measures the radiance along one ray, so light tracing to the
camera is not a technique, and the camera subpath starts with dVCM = dVC = dVM = 0.

The scene is the furnace: the inside of the unit sphere, Lambertian with albedo rho and
emitted radiance Le everywhere. With paths of at most K edges the exact radiance along
every camera ray is Le (1 + rho + ... + rho^(K-1)).
"""

import math
import random
from dataclasses import dataclass

Vec = tuple[float, float, float]
INV_2PI = 1.0 / (2.0 * math.pi)
INV_4PI = 1.0 / (4.0 * math.pi)


@dataclass(frozen=True)
class MisState:
    dvcm: float
    dvc: float
    dvm: float


ZERO = MisState(0.0, 0.0, 0.0)


def emission_state(pdf_a, pdf_w_emit, cos_light, vc_factor) -> MisState:
    """The state at a light vertex. The emitter is sampled with the same area pdf for
    emission and for next event estimation."""
    emission_pdf = pdf_a * pdf_w_emit
    dvc = cos_light / emission_pdf
    return MisState(pdf_a / emission_pdf, dvc, dvc * vc_factor)


def hit_update(s: MisState, dist2, cos_hit) -> MisState:
    """Turn the solid angle pdf of the last direction into an area pdf at the new vertex."""
    return MisState(s.dvcm * dist2 / cos_hit, s.dvc / cos_hit, s.dvm / cos_hit)


def scatter_update(s: MisState, cos_out, pdf_fwd_w, pdf_rev_w, eta, vc_factor) -> MisState:
    """After sampling the next direction with the pdf pdf_fwd_w; pdf_rev_w is the pdf of the
    direction back to the previous vertex, given the new direction."""
    k = cos_out / pdf_fwd_w
    return MisState(
        1 / pdf_fwd_w,
        k * (s.dvc * pdf_rev_w + s.dvcm + eta),
        k * (s.dvm * pdf_rev_w + s.dvcm * vc_factor + 1),
    )


def weight_emission(cam: MisState, pdf_a, pdf_w_emit) -> float:
    """The camera subpath hits an emitter."""
    return 1 / (1 + pdf_a * cam.dvcm + pdf_a * pdf_w_emit * cam.dvc)


def weight_nee(cam: MisState, pdf_a, cos_light, dist2, cam_pdf_w, cam_pdf_rev_w, emit_pdf_w, cos_cam, eta) -> float:
    """Next event estimation. cam_pdf_w is the camera vertex's pdf of the direction to the
    light point, cam_pdf_rev_w its pdf of the direction back along the camera subpath."""
    w_light = cam_pdf_w / (pdf_a * dist2 / cos_light)
    w_cam = (emit_pdf_w * cos_cam / dist2) * (eta + cam.dvcm + cam.dvc * cam_pdf_rev_w)
    return 1 / (w_light + 1 + w_cam)


def weight_vc(light: MisState, cam: MisState, p_rev_a, p_fwd_a, light_pdf_rev_w, cam_pdf_rev_w, eta) -> float:
    """Connect a light vertex y to a camera vertex z. p_rev_a is the area pdf of y from z,
    p_fwd_a the area pdf of z from y."""
    w_light = p_rev_a * (eta + light.dvcm + light.dvc * light_pdf_rev_w)
    w_cam = p_fwd_a * (eta + cam.dvcm + cam.dvc * cam_pdf_rev_w)
    return 1 / (w_light + 1 + w_cam)


def weight_vm(light: MisState, cam: MisState, light_pdf_rev_w, cam_pdf_rev_w, vc_factor) -> float:
    """Merge a light vertex with a camera vertex. Both pdfs are of the camera vertex's BSDF:
    light_pdf_rev_w of the light subpath's incoming direction, given the camera direction,
    and cam_pdf_rev_w the other way."""
    w_light = light.dvcm * vc_factor + light.dvm * light_pdf_rev_w
    w_cam = cam.dvcm * vc_factor + cam.dvm * cam_pdf_rev_w
    return 1 / (w_light + 1 + w_cam)


def balance_weights(p_fwd, p_rev, eta):
    """Brute force balance heuristic weights for the path x_0 (on the light) ... x_k (camera).
    p_fwd[i] is the area pdf of x_i from the light side (i = 0 .. k-1), p_rev[i] the area pdf
    of x_i from the camera side (i = 0 .. k-2). Techniques: ("vc", j) uses the light vertices
    x_0 .. x_(j-1), with j = 0 for an emitter hit and j = 1 for next event estimation;
    ("vm", j) merges at x_j. The camera factor of x_(k-1) is common and left out."""
    k = len(p_fwd)
    p = {}
    for j in range(k):
        prod = 1
        for i in range(j):
            prod *= p_fwd[i]
        for i in range(j, k - 1):
            prod *= p_rev[i]
        p[("vc", j)] = prod
        if j >= 1:
            p[("vm", j)] = eta * p_fwd[j] * prod
    total = sum(p.values())
    return {t: v / total for t, v in p.items()}


def _sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _unit(a: Vec) -> Vec:
    n = math.sqrt(_dot(a, a))
    return (a[0] / n, a[1] / n, a[2] / n)


def _normal(p: Vec) -> Vec:
    return (-p[0], -p[1], -p[2])


def uniform_sphere(rng: random.Random) -> Vec:
    z = 1.0 - 2.0 * rng.random()
    s = math.sqrt(max(0.0, 1.0 - z * z))
    phi = 2.0 * math.pi * rng.random()
    return (s * math.cos(phi), s * math.sin(phi), z)


def _frame(n: Vec) -> tuple[Vec, Vec]:
    a = (1.0, 0.0, 0.0) if abs(n[0]) < 0.9 else (0.0, 1.0, 0.0)
    t = _unit((a[1] * n[2] - a[2] * n[1], a[2] * n[0] - a[0] * n[2], a[0] * n[1] - a[1] * n[0]))
    b = (n[1] * t[2] - n[2] * t[1], n[2] * t[0] - n[0] * t[2], n[0] * t[1] - n[1] * t[0])
    return t, b


def _local(n: Vec, lx: float, ly: float, lz: float) -> Vec:
    t, b = _frame(n)
    return _unit(tuple(lx * t[i] + ly * b[i] + lz * n[i] for i in range(3)))


def cosine_direction(n: Vec, rng: random.Random) -> Vec:
    u1, u2 = rng.random(), rng.random()
    r, phi = math.sqrt(u1), 2.0 * math.pi * u2
    return _local(n, r * math.cos(phi), r * math.sin(phi), math.sqrt(max(0.0, 1.0 - u1)))


def uniform_direction(n: Vec, rng: random.Random) -> Vec:
    z = rng.random()
    s, phi = math.sqrt(max(0.0, 1.0 - z * z)), 2.0 * math.pi * rng.random()
    return _local(n, s * math.cos(phi), s * math.sin(phi), z)


def hit_sphere(p: Vec, v: Vec) -> Vec:
    """The point where the ray from p (inside or on the unit sphere) leaves the sphere."""
    b, c = _dot(p, v), _dot(p, p) - 1.0
    t = -b + math.sqrt(max(0.0, b * b - c))
    return _unit((p[0] + t * v[0], p[1] + t * v[1], p[2] + t * v[2]))


@dataclass
class Furnace:
    rho: float
    le: float = 1.0

    def exact(self, k_max: int) -> float:
        return self.le * sum(self.rho**j for j in range(k_max))


@dataclass
class LightVertex:
    x: Vec
    n: Vec
    beta: float
    depth: int
    state: MisState


def trace_light_path(scene: Furnace, k_max: int, eta: float, vc_factor: float, rng: random.Random) -> list[LightVertex]:
    """Emit from a uniform point with a cosine direction, then scatter with uniform
    hemisphere directions. Store the vertices of depth 1 .. k_max - 1."""
    x = uniform_sphere(rng)
    n = _normal(x)
    v = cosine_direction(n, rng)
    cos0 = _dot(n, v)
    pdf_w = cos0 / math.pi
    beta = scene.le * cos0 / (INV_4PI * pdf_w)
    state = emission_state(INV_4PI, pdf_w, cos0, vc_factor)
    out = []
    f = scene.rho / math.pi
    for depth in range(1, k_max):
        y = hit_sphere(x, v)
        ny = _normal(y)
        d = _sub(y, x)
        state = hit_update(state, _dot(d, d), _dot(ny, v) * -1.0)
        out.append(LightVertex(y, ny, beta, depth, state))
        v = uniform_direction(ny, rng)
        cos_out = _dot(ny, v)
        beta *= f * cos_out / INV_2PI
        state = scatter_update(state, cos_out, INV_2PI, INV_2PI, eta, vc_factor)
        x = y
    return out


class HashGrid:
    """Light vertices in cubic cells of side r; a query looks at the 27 cells around a point."""

    def __init__(self, r: float, verts: list[LightVertex]):
        self.r = r
        self.cells: dict[tuple[int, int, int], list[LightVertex]] = {}
        for lv in verts:
            self.cells.setdefault(self._key(lv.x), []).append(lv)

    def _key(self, p: Vec) -> tuple[int, int, int]:
        return (math.floor(p[0] / self.r), math.floor(p[1] / self.r), math.floor(p[2] / self.r))

    def query(self, p: Vec) -> list[LightVertex]:
        i, j, k = self._key(p)
        out = []
        for a in (i - 1, i, i + 1):
            for b in (j - 1, j, j + 1):
                for c in (k - 1, k, k + 1):
                    for lv in self.cells.get((a, b, c), ()):
                        d = _sub(lv.x, p)
                        if _dot(d, d) < self.r * self.r:
                            out.append(lv)
        return out


def _nee(scene, y, ny, beta, state, eta, rng) -> float:
    xl = uniform_sphere(rng)
    nl = _normal(xl)
    d = _sub(xl, y)
    dist2 = _dot(d, d)
    w = _unit(d)
    cos_cam, cos_l = _dot(ny, w), -_dot(nl, w)
    g = cos_cam * cos_l / dist2
    mis = weight_nee(state, INV_4PI, cos_l, dist2, INV_2PI, INV_2PI, cos_l / math.pi, cos_cam, eta)
    return beta * (scene.rho / math.pi) * scene.le * g / INV_4PI * mis


def _connect(scene, y, ny, beta, state, lv, eta) -> float:
    d = _sub(lv.x, y)
    dist2 = _dot(d, d)
    w = _unit(d)
    cos_cam, cos_l = _dot(ny, w), -_dot(lv.n, w)
    g = cos_cam * cos_l / dist2
    mis = weight_vc(lv.state, state, INV_2PI * cos_l / dist2, INV_2PI * cos_cam / dist2, INV_2PI, INV_2PI, eta)
    f = scene.rho / math.pi
    return beta * f * g * f * lv.beta * mis


def vcm_iteration(scene: Furnace, n: int, r: float, k_max: int, rng: random.Random, merge: bool = True) -> list[float]:
    """One VCM iteration with n light and n camera subpaths. Return the estimate of each camera
    path. With merge=False the weights and the estimate are those of bidirectional path tracing."""
    eta = n * math.pi * r * r if merge else 0.0  # @line L1
    vc_factor = 1.0 / eta if merge else 0.0
    light_paths = [trace_light_path(scene, k_max, eta, vc_factor, rng) for _ in range(n)]  # @line L2
    grid = HashGrid(r, [lv for path in light_paths for lv in path]) if merge else None  # @line L3
    f = scene.rho / math.pi
    estimates = []
    for j in range(n):  # @line L4
        x, v = (0.0, 0.0, 0.0), uniform_sphere(rng)
        beta, state, total = 1.0, ZERO, 0.0
        for c in range(1, k_max + 1):  # @line L5
            y = hit_sphere(x, v)
            ny = _normal(y)
            d = _sub(y, x)
            cos_in = -_dot(ny, v)
            state = hit_update(state, _dot(d, d), cos_in)
            total += beta * scene.le * weight_emission(state, INV_4PI, cos_in / math.pi)  # @line L6
            if c + 1 <= k_max:
                total += _nee(scene, y, ny, beta, state, eta, rng)  # @line L7
            total += sum(_connect(scene, y, ny, beta, state, lv, eta) for lv in light_paths[j] if lv.depth + 1 + c <= k_max)  # @line L8
            if grid is not None:
                total += sum(beta * f * lv.beta * weight_vm(lv.state, state, INV_2PI, INV_2PI, vc_factor) / eta for lv in grid.query(y) if lv.depth + c <= k_max)  # @line L9
            if c == k_max:
                break
            v = uniform_direction(ny, rng)
            cos_out = _dot(ny, v)
            beta *= f * cos_out / INV_2PI
            state = scatter_update(state, cos_out, INV_2PI, INV_2PI, eta, vc_factor)  # @line L10
            x = y
        estimates.append(total)
    return estimates  # @line L11


def recursive_weights(p_a, cm, cp, d2, pwf, pwr, eta):
    """The weights of all techniques for one path x_0 .. x_k, from the dVCM, dVC and dVM
    recursion, with the same update and weight functions as the renderer. p_a is the area pdf
    of x_0. For the vertex x_i: cm[i] and cp[i] are the cosines toward x_(i-1) and x_(i+1),
    pwf[i] and pwr[i] the solid angle pdfs of the directions toward x_(i+1) and x_(i-1).
    d2[i] is the squared length of the edge x_i x_(i+1), and pwf[0] is the emission pdf.
    Fractions in give fractions out."""
    k = len(cm)
    vc_factor = 1 / eta if eta else 0
    light = [emission_state(p_a, pwf[0], cp[0], vc_factor)]
    for m in range(1, k):
        s = light[-1] if m == 1 else scatter_update(light[-1], cp[m - 1], pwf[m - 1], pwr[m - 1], eta, vc_factor)
        light.append(hit_update(s, d2[m - 1], cm[m]))
    zero = MisState(0, 0, 0)
    cam = [zero] * k
    for s in range(k - 2, -1, -1):
        st = scatter_update(cam[s + 1], cm[s + 1], pwr[s + 1], pwf[s + 1], eta, vc_factor)
        cam[s] = hit_update(st, d2[s], cp[s])
    w = {("vc", 0): weight_emission(cam[0], p_a, pwf[0])}
    if k >= 2:
        w[("vc", 1)] = weight_nee(cam[1], p_a, cp[0], d2[0], pwr[1], pwf[1], pwf[0], cm[1], eta)
    for j in range(2, k):
        p_rev_a = pwr[j] * cp[j - 1] / d2[j - 1]
        p_fwd_a = pwf[j - 1] * cm[j] / d2[j - 1]
        w[("vc", j)] = weight_vc(light[j - 1], cam[j], p_rev_a, p_fwd_a, pwr[j - 1], pwf[j], eta)
    if eta:
        for j in range(1, k):
            w[("vm", j)] = weight_vm(light[j], cam[j], pwr[j], pwf[j], vc_factor)
    return w
