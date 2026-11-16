# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/admittance-control/. The authors are listed in prov/373QBF.jsonl.

"""Admittance control: a measured force drives a virtual mass-spring-damper.

At each control period the controller integrates the virtual dynamics

    Ma xc'' + Da (xc' - x0') + Ka (xc - x0) = F_meas

by one semi-implicit Euler step and sends xc to a stiff position loop.
The test robot is a Cartesian robot: a point mass per axis with a PD
position loop, in contact with a spring wall. Vectors are lists, and the
gains are lists of diagonal entries. Only the standard library.
"""


def admittance_step(xc, vc, x0, x0d, f_meas, ma, da, ka, dt):
    """One control period. Return the new commanded position and speed."""
    n = len(xc)
    ac = [(f_meas[i] - da[i] * (vc[i] - x0d[i]) - ka[i] * (xc[i] - x0[i])) / ma[i] for i in range(n)]  # @line L1
    vc = [vc[i] + dt * ac[i] for i in range(n)]  # @line L2
    xc = [xc[i] + dt * vc[i] for i in range(n)]  # @line L3
    return xc, vc  # @line L4


class CartesianRobot:
    """A point mass m per axis with the position loop u = Kp (xc - x) - Kv x'."""

    def __init__(self, mass=5.0, kp=1e5, kv=None):
        self.mass = mass
        self.kp = kp
        self.kv = kv if kv is not None else 2.0 * (kp * mass) ** 0.5

    def accel(self, x, xd, xc, f_ext):
        return [(self.kp * (xc[i] - x[i]) - self.kv * xd[i] + f_ext[i]) / self.mass for i in range(len(x))]


def wall(x_wall, k_env):
    """A frictionless wall x[0] <= x_wall with stiffness k_env."""

    def force(x):
        pen = x[0] - x_wall
        f = [0.0] * len(x)
        if pen > 0.0:
            f[0] = -k_env * pen
        return f

    return force


def free_space(x):
    return [0.0] * len(x)


def rk4_step(f, x, dt):
    """One classical Runge-Kutta step for the autonomous system x' = f(x)."""
    k1 = f(x)
    k2 = f([x[i] + dt / 2 * k1[i] for i in range(len(x))])
    k3 = f([x[i] + dt / 2 * k2[i] for i in range(len(x))])
    k4 = f([x[i] + dt * k3[i] for i in range(len(x))])
    return [x[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(x))]


def simulate(robot, env, goal, x_start, ma, da, ka, dt, periods, substeps=1):
    """Run the controller for a number of periods of length dt.

    goal(t) returns (x0, x0'). The sensor reads the wall force at the start
    of each period, and xc is held over the period. The plant is integrated
    by RK4 with the given number of substeps. Return a list of
    (t, x, xc, f_meas) at the start of each period and after the last one.
    """
    n = len(x_start)
    x, xd = list(x_start), [0.0] * n
    xc, vc = list(x_start), [0.0] * n
    out = []
    h = dt / substeps
    for k in range(periods):
        t = k * dt
        f_meas = env(x)
        out.append((t, x, xc, f_meas))
        x0, x0d = goal(t)
        xc, vc = admittance_step(xc, vc, x0, x0d, f_meas, ma, da, ka, dt)
        hold = list(xc)

        def plant(s):
            p, v = s[:n], s[n:]
            return v + robot.accel(p, v, hold, env(p))

        s = x + xd
        for _ in range(substeps):
            s = rk4_step(plant, s, h)
        x, xd = s[:n], s[n:]
    out.append((periods * dt, x, xc, env(x)))
    return out
