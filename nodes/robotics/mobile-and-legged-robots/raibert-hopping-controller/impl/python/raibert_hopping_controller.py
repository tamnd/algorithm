# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/raibert-hopping-controller/. The authors are listed in prov/V4NCCQ.jsonl.
"""Raibert's three-part controller on a planar one-legged hopper.

The model: a rigid body of mass m and pitch inertia I, with the hip at the
center of mass, and a massless telescoping leg with a spring of stiffness k,
a damper b and a rest length that the controller can change. Coordinates:
x forward, z up, gravity -g along z, pitch phi counterclockwise.

The body state is s = [x, z, phi, vx, vz, wphi]. In flight the body is
ballistic and the massless leg is moved at once to the touchdown angle, so
the flight is solved in closed form. In stance the foot is pinned at
(foot_x, 0) and the stance is integrated with RK4 at the fixed step dt.
Lift-off (the spring force falls to zero while the leg lengthens) is found
by bisection on the last step.

The controller (Raibert 1986, chapter 2):
  thrust     - the spring rest length grows from l0 to l0 + delta when the
               leg starts to lengthen, which adds energy each hop;
  placement  - in flight, the foot goes to x_f = vx Ts / 2 + k_x (vx - vx_d)
               ahead of the hip, where Ts is the last stance time;
  attitude   - in stance, the hip torque is -k_p (phi - phi_d) - k_v wphi.
"""

import math

G = 9.81


class Hopper:
    def __init__(self, m=10.0, inertia=0.5, k=4000.0, b=0.0, l0=0.5, g=G):
        self.m = m
        self.inertia = inertia
        self.k = k
        self.b = b
        self.l0 = l0
        self.g = g

    def energy(self, s, foot_x=None, rest=None):
        """Kinetic plus gravity energy, plus the spring energy in stance."""
        e = 0.5 * self.m * (s[3] ** 2 + s[4] ** 2) + 0.5 * self.inertia * s[5] ** 2 + self.m * self.g * s[1]
        if foot_x is not None:
            l = math.hypot(s[0] - foot_x, s[1])
            e += 0.5 * self.k * (rest - l) ** 2
        return e


class Gains:
    def __init__(self, delta=0.0, k_x=0.0, k_p=0.0, k_v=0.0, vx_d=0.0, phi_d=0.0):
        self.delta = delta
        self.k_x = k_x
        self.k_p = k_p
        self.k_v = k_v
        self.vx_d = vx_d
        self.phi_d = phi_d


def foot_placement(vx, vx_d, ts, k_x, l0):
    """Return the leg angle from the vertical; positive puts the foot ahead of the hip."""
    xf = vx * ts / 2.0 + k_x * (vx - vx_d)  # @line L2
    xf = max(-0.9 * l0, min(0.9 * l0, xf))
    return math.asin(xf / l0)  # @line L3


def attitude_torque(phi, wphi, gains):
    """Hip torque on the body during stance."""
    return -gains.k_p * (phi - gains.phi_d) - gains.k_v * wphi  # @line L8


def leg(s, foot_x):
    """Return (l, ldot, ux, uz) of the leg vector from the foot to the hip."""
    rx, rz = s[0] - foot_x, s[1]
    l = math.hypot(rx, rz)
    ux, uz = rx / l, rz / l
    return l, ux * s[3] + uz * s[4], ux, uz


def spring_force(robot, rest, l, ldot):
    return robot.k * (rest - l) - robot.b * ldot


def stance_deriv(robot, s, foot_x, rest, gains):
    l, ldot, ux, uz = leg(s, foot_x)
    fs = spring_force(robot, rest, l, ldot)
    tau = attitude_torque(s[2], s[5], gains)
    # Massless leg: the moment of the leg force about the foot cancels the hip
    # torque on the leg, so the force part normal to the leg is -tau / l.
    fn = -tau / l
    fx = fs * ux - fn * uz
    fz = fs * uz + fn * ux
    return [s[3], s[4], s[5], fx / robot.m, fz / robot.m - robot.g, tau / robot.inertia]


def rk4_step(robot, s, foot_x, rest, gains, h):
    def f(y):
        return stance_deriv(robot, y, foot_x, rest, gains)

    k1 = f(s)
    k2 = f([a + h / 2 * b for a, b in zip(s, k1)])
    k3 = f([a + h / 2 * b for a, b in zip(s, k2)])
    k4 = f([a + h * b for a, b in zip(s, k3)])
    return [a + h / 6 * (p + 2 * q + 2 * r + w) for a, p, q, r, w in zip(s, k1, k2, k3, k4)]


def flight(robot, s, theta):
    """Ballistic flight until the foot, held at leg angle theta, touches z = 0.

    Return (state at touchdown, flight time, apex height of the hip).
    """
    zc = robot.l0 * math.cos(theta)
    z, vz, g = s[1], s[4], robot.g
    apex = z + max(vz, 0.0) ** 2 / (2 * g)
    if apex < zc:
        raise ValueError("the hopper does not rise high enough to swing the leg")
    t = (vz + math.sqrt(vz * vz + 2 * g * (z - zc))) / g
    out = [s[0] + s[3] * t, zc, s[2] + s[5] * t, s[3], vz - g * t, s[5]]
    return out, t, apex


def stance(robot, s, foot_x, gains, dt=1e-3, max_steps=5000):
    """Integrate one stance from touchdown to lift-off with RK4.

    Return (state at lift-off, stance time, number of RK4 steps).
    """
    t, steps = 0.0, 0
    thrusting = False
    rest = robot.l0  # @line L7
    for _ in range(max_steps):
        l, ldot, _, _ = leg(s, foot_x)
        if not thrusting and ldot > 0.0:  # @line L5
            thrusting = True
            rest = robot.l0 + gains.delta  # @line L6
        new = rk4_step(robot, s, foot_x, rest, gains, dt)
        steps += 1
        l, ldot, _, _ = leg(new, foot_x)
        if thrusting and spring_force(robot, rest, l, ldot) <= 0.0:
            lo, hi = 0.0, dt
            for _ in range(40):
                mid = (lo + hi) / 2
                y = rk4_step(robot, s, foot_x, rest, gains, mid)
                ly, ldy, _, _ = leg(y, foot_x)
                if spring_force(robot, rest, ly, ldy) <= 0.0:
                    hi = mid
                else:
                    lo = mid
            steps += 40
            return rk4_step(robot, s, foot_x, rest, gains, hi), t + hi, steps
        s = new
        t += dt
    raise ValueError("no lift-off within max_steps")


def hop(robot, gains, s, ts, dt=1e-3):
    """One flight and one stance, starting in flight.

    Return (state at the next lift-off, the new stance time Ts, a record dict).
    """
    theta = foot_placement(s[3], gains.vx_d, ts, gains.k_x, robot.l0)  # @line L1
    td, t_fl, apex = flight(robot, s, theta)
    foot_x = td[0] + robot.l0 * math.sin(theta)
    lo, ts_new, steps = stance(robot, td, foot_x, gains, dt)  # @line L4
    record = {"apex": apex, "vx": s[3], "phi_td": td[2], "theta": theta, "ts": ts_new, "steps": steps}
    return lo, ts_new, record  # @line L9


def run(robot, gains, s, n_hops, ts=None, dt=1e-3):
    """Run n_hops hops from the flight state s; return the list of hop records."""
    if ts is None:
        ts = math.pi * math.sqrt(robot.m / robot.k)
    out = []
    for _ in range(n_hops):
        s, ts, rec = hop(robot, gains, s, ts, dt)
        out.append(rec)
    return out, s


def vertical_stance_time(robot, v):
    """Closed form stance time of a vertical bounce at touchdown speed v, no damping, no thrust."""
    w = math.sqrt(robot.k / robot.m)
    alpha = math.atan2(v / w, robot.m * robot.g / robot.k)
    return (2 * math.pi - 2 * alpha) / w
