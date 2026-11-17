# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/impulse-based-simulation/. The authors are listed in prov/P8GDCY.jsonl.

"""Impulse-based simulation of discs on a ground line in 2D, after Mirtich and Canny (1995).

Every contact, also resting contact, is a collision: an impulse at one
instant. Between collisions all bodies move on ballistic paths, which this
version follows exactly. A collision is detected when the gap between two
bodies falls to the collision envelope eps_c while they approach.

The collision impulse uses Poisson's hypothesis and Coulomb friction, and it
is integrated along the collision with the normal impulse p_n as the
parameter (Mirtich and Canny, Section 4). In 2D the direction of the
friction impulse is constant within each phase, so the integration is exact:
it moves along straight lines in impulse space from one event to the next.

Conventions: y is up, gravity is (0, -g). The contact normal n points from
B to A, the tangent is t = (n_y, -n_x), and the contact velocity u = (u_t,
u_n) is the velocity of A at the contact point minus that of B. The impulse
p = (p_t, p_n), in the frame (t, n), acts on A, and -p acts on B. The matrix
K maps an impulse to the change of u; it is stored as (K_tt, K_tn, K_nn).
"""

import math


class Disc:
    """A uniform disc: center x, velocity v, angle theta, angular velocity w, mass m, radius."""

    def __init__(self, x, v, w, m, radius, theta=0):
        self.x = tuple(x)
        self.v = tuple(v)
        self.w = w
        self.theta = theta
        self.m = m
        self.radius = radius
        self.I = m * radius * radius / 2
        self.inv_m = 1 / m
        self.inv_I = 1 / self.I


class Ground:
    """The static half plane y <= 0."""

    inv_m = 0
    inv_I = 0
    v = (0, 0)
    w = 0


GROUND = Ground()


def cross2(a, b):
    return a[0] * b[1] - a[1] * b[0]


def point_velocity(body, r):
    """v + w x r in 2D."""
    return (body.v[0] - body.w * r[1], body.v[1] + body.w * r[0])


def contact_frame(n):
    return (n[1], -n[0]), n


def contact_matrix(a, b, r_a, r_b, n):
    """K_de = sum over the bodies of inv_m (d . e) + inv_I (r x d)(r x e), for d, e in {t, n}."""
    t, n = contact_frame(n)
    ktt = a.inv_m + b.inv_m + a.inv_I * cross2(r_a, t) ** 2 + b.inv_I * cross2(r_b, t) ** 2
    ktn = a.inv_I * cross2(r_a, t) * cross2(r_a, n) + b.inv_I * cross2(r_b, t) * cross2(r_b, n)
    knn = a.inv_m + b.inv_m + a.inv_I * cross2(r_a, n) ** 2 + b.inv_I * cross2(r_b, n) ** 2
    return ktt, ktn, knn


def contact_velocity(a, b, r_a, r_b, n):
    t, n = contact_frame(n)
    va, vb = point_velocity(a, r_a), point_velocity(b, r_b)
    du = (va[0] - vb[0], va[1] - vb[1])
    return du[0] * t[0] + du[1] * t[1], du[0] * n[0] + du[1] * n[1]


def apply_impulse(a, b, r_a, r_b, n, p):
    """Apply p_t t + p_n n to A at r_a and the opposite impulse to B at r_b."""
    t, n = contact_frame(n)
    imp = (p[0] * t[0] + p[1] * n[0], p[0] * t[1] + p[1] * n[1])
    for body, r, s in ((a, r_a, 1), (b, r_b, -1)):
        if body.inv_m == 0:
            continue
        body.v = (body.v[0] + s * imp[0] * body.inv_m, body.v[1] + s * imp[1] * body.inv_m)
        body.w = body.w + s * body.inv_I * cross2(r, imp)


def microcollision_impulse(K, u):
    """The impulse p with K p = -2 u, which reverses the contact velocity."""
    ktt, ktn, knn = K
    det = ktt * knn - ktn * ktn
    return (-2 * (knn * u[0] - ktn * u[1]) / det, -2 * (ktt * u[1] - ktn * u[0]) / det)


def collide(K, u, mu, e, trace=None):
    """Integrate a frictional collision with Poisson's hypothesis; return p = (p_t, p_n).

    The parameter is p_n. In each phase dp/dp_n = d = (d_t, 1) is constant:
    sliding uses d_t = -mu sgn(u_t), sticking uses d_t = -K_tn / K_tt, and
    sliding again from rest uses d_t = -mu sgn(K_tn). A phase ends at the next
    event: u_t reaches 0, u_n reaches 0 (maximum compression, which fixes the
    end of the collision at p_n = (1 + e) p_mc), or p_n reaches that end.
    If trace is a list, one tuple (mode, event, p_t, p_n, u_t, u_n) is added per phase.
    """
    ktt, ktn, knn = K
    ut, un = u
    if un >= 0:
        return 0 * ut, 0 * un
    pt, pn = 0 * ut, 0 * un  # @line L10
    target = None  # @line L10
    for _ in range(16):  # @line L11
        if ut != 0:  # @line L12
            mode, dt = "slide", (-mu if ut > 0 else mu)  # @line L12
        elif abs(ktn) <= mu * ktt:  # @line L12
            mode, dt = "stick", -ktn / ktt  # @line L12
        else:  # @line L12
            mode, dt = "slide again", (-mu if ktn > 0 else mu)  # @line L12
        dut = ktt * dt + ktn
        dun = ktn * dt + knn
        steps = []  # @line L13
        if mode == "slide" and ut * dut < 0:  # @line L13
            steps.append((-ut / dut, "stop"))  # @line L13
        if target is None:  # @line L13
            if dun > 0:  # @line L13
                steps.append((-un / dun, "max"))  # @line L13
        else:  # @line L13
            steps.append((target - pn, "end"))  # @line L13
        if not steps:
            raise RuntimeError("no event ahead; K must be positive definite")
        h, event = min(steps, key=lambda s: s[0])  # @line L13
        h = max(h, 0 * h)
        pt, pn = pt + dt * h, pn + h  # @line L14
        ut, un = ut + dut * h, un + dun * h  # @line L14
        if event == "stop":
            ut = 0 * ut
        if trace is not None:
            trace.append((mode, event, pt, pn, ut, un))
        if event == "max":  # @line L15
            un = 0 * un  # @line L15
            target = (1 + e) * pn  # @line L15
        elif event == "end":  # @line L16
            return pt, pn  # @line L17
    raise RuntimeError("too many phases")


def in_cone(p, mu):
    return p[1] >= 0 and abs(p[0]) <= mu * p[1]


def contact_geometry(a, b):
    """Normal n (from B to A) and arms for the point p of A that is nearest to B."""
    if b is GROUND:
        n = (0, 1)
        r_a = (0, -a.radius)
        p = (a.x[0], a.x[1] - a.radius)
        return n, r_a, p
    d = (a.x[0] - b.x[0], a.x[1] - b.x[1])
    length = math.hypot(d[0], d[1])
    n = (d[0] / length, d[1] / length)
    r_a = (-a.radius * n[0], -a.radius * n[1])
    p = (a.x[0] + r_a[0], a.x[1] + r_a[1])
    return n, r_a, p


def resolve(a, b, mu, e, v_e):
    """Resolve one detected contact. Return "micro", "collision" or "none"."""
    n, r_a, p = contact_geometry(a, b)  # @line L6
    r_b = (p[0] - b.x[0], p[1] - b.x[1]) if b is not GROUND else (0, 0)  # @line L6
    K = contact_matrix(a, b, r_a, r_b, n)  # @line L6
    u = contact_velocity(a, b, r_a, r_b, n)  # @line L6
    if u[1] >= 0:
        return "none"
    e_used = e
    if -u[1] < v_e:  # @line L7
        q = microcollision_impulse(K, u)  # @line L7
        if in_cone(q, mu):  # @line L7
            apply_impulse(a, b, r_a, r_b, n, q)  # @line L9
            return "micro"
        # A slow contact that slides: resolve it with e = 1. This choice of the
        # page keeps the normal speed, so the bounces do not pile up in finite time.
        e_used = 1  # @line L8
    q = collide(K, u, mu, e_used)  # @line L8
    apply_impulse(a, b, r_a, r_b, n, q)  # @line L9
    return "collision"


def ground_event_time(disc, eps_c, g):
    """First time at which the gap to the ground is at most eps_c and closing."""
    h = disc.x[1] - disc.radius - eps_c
    vy = disc.v[1]
    if h <= 0 and vy < 0:
        return 0.0
    if g == 0:
        return h / -vy if (vy < 0 and h > 0) else math.inf
    return (vy + math.sqrt(vy * vy + 2 * g * max(h, 0))) / g


def pair_event_time(a, b, eps_c):
    """First time at which the gap between two discs is at most eps_c and closing.

    Gravity acts on both, so the relative motion is a straight line."""
    d = (a.x[0] - b.x[0], a.x[1] - b.x[1])
    w = (a.v[0] - b.v[0], a.v[1] - b.v[1])
    s = a.radius + b.radius + eps_c
    qa = w[0] * w[0] + w[1] * w[1]
    qb = 2 * (d[0] * w[0] + d[1] * w[1])
    qc = d[0] * d[0] + d[1] * d[1] - s * s
    if qb >= 0 or qa == 0:
        return math.inf
    if qc <= 0:
        return 0.0
    disc = qb * qb - 4 * qa * qc
    if disc < 0:
        return math.inf
    return 2 * qc / (-qb + math.sqrt(disc))


def drift(discs, tau, g):
    """Move every disc on its ballistic path for the time tau."""
    for d in discs:
        d.x = (d.x[0] + d.v[0] * tau, d.x[1] + d.v[1] * tau - g * tau * tau / 2)
        d.v = (d.v[0], d.v[1] - g * tau)
        d.theta = d.theta + d.w * tau


def simulate(discs, t_end, mu, e, eps_c, g=9.81, ground=True, max_events=200000):
    """Run the simulation from t = 0 to t_end. Return the list of events (t, i, j, kind, u_n).

    j is -1 for the ground. The discs are changed in place."""
    v_e = math.sqrt(2 * g * eps_c)
    t = 0.0  # @line L1
    log = []
    while True:  # @line L2
        best = (math.inf, None, None)  # @line L3
        for i, a in enumerate(discs):  # @line L3
            if ground:  # @line L3
                tau = ground_event_time(a, eps_c, g)  # @line L3
                if tau < best[0]:  # @line L3
                    best = (tau, i, -1)  # @line L3
            for j in range(i + 1, len(discs)):  # @line L3
                tau = pair_event_time(a, discs[j], eps_c)  # @line L3
                if tau < best[0]:  # @line L3
                    best = (tau, i, j)  # @line L3
        tau, i, j = best
        if t + tau > t_end:  # @line L4
            drift(discs, t_end - t, g)  # @line L4
            return log  # @line L4
        drift(discs, tau, g)  # @line L5
        t += tau  # @line L5
        a, b = discs[i], (GROUND if j < 0 else discs[j])
        n, r_a, p = contact_geometry(a, b)
        r_b = (p[0] - b.x[0], p[1] - b.x[1]) if b is not GROUND else (0, 0)
        un = contact_velocity(a, b, r_a, r_b, n)[1]
        kind = resolve(a, b, mu, e, v_e)
        log.append((t, i, j, kind, un))
        if len(log) > max_events:
            raise RuntimeError("too many events")


def kinetic_energy(discs):
    return sum(d.m * (d.v[0] ** 2 + d.v[1] ** 2) / 2 + d.I * d.w * d.w / 2 for d in discs)


def linear_momentum(discs):
    return (sum(d.m * d.v[0] for d in discs), sum(d.m * d.v[1] for d in discs))


def angular_momentum(discs, origin=(0, 0)):
    total = 0
    for d in discs:
        r = (d.x[0] - origin[0], d.x[1] - origin[1])
        total += d.m * cross2(r, d.v) + d.I * d.w
    return total
