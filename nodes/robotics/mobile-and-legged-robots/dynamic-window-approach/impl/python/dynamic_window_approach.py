# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-window-approach/. The authors are listed in prov/0PW0PJ.jsonl.

"""The dynamic window approach (Fox, Burgard and Thrun 1997) for a round robot.

The robot is a unicycle: x' = v cos(theta), y' = v sin(theta), theta' = w. Velocities are
held for one control interval dt, so each command moves the robot on a circular arc (or
a straight segment). Obstacles are discs; the robot radius is added to their radius.

At each interval the method searches the velocities that the accelerations can reach
within dt (the dynamic window), keeps the admissible ones (the robot can still stop on
the same arc before it reaches an obstacle), and picks the one that maximizes a weighted
sum of heading to the goal, clearance and speed.

Admissible here means: the stopping distance s(v, w) of the discrete braking sequence on
the arc of (v, w) is at most the free arc length dist(v, w). The braking pair on the
current arc is always a candidate, so an admissible pair always exists when the start
velocity is admissible (Theorem 1 of the proof).
"""

import math

INF = float("inf")
TWO_PI = 2.0 * math.pi


class Robot:
    """Limits of the robot. Speeds in m/s and rad/s, accelerations in m/s^2 and rad/s^2."""

    def __init__(self, radius=0.3, v_max=0.95, w_max=1.0, a_v=0.5, a_w=math.radians(60.0), dt=0.25):
        self.radius, self.v_max, self.w_max = radius, v_max, w_max
        self.a_v, self.a_w, self.dt = a_v, a_w, dt


def move(pose, v, w, t):
    """Exact unicycle motion for time t with constant (v, w)."""
    x, y, th = pose
    if abs(w) < 1e-12:
        return (x + v * t * math.cos(th), y + v * t * math.sin(th), th)
    r = v / w
    th2 = th + w * t
    return (x + r * (math.sin(th2) - math.sin(th)), y - r * (math.cos(th2) - math.cos(th)), th2)


def arc_distance(pose, v, w, obstacles, inflate):
    """Arc length from pose along the path of (v, w) until the robot touches an obstacle.

    obstacles is a list of (ox, oy, r); the robot touches it when its center is within
    r + inflate. Returns INF if the path never touches one (or if v = 0: the round robot
    turns in place). The start pose must be free.
    """
    if v <= 0.0:
        return INF
    x, y, th = pose
    best = INF
    if abs(w) < 1e-9:
        c, s = math.cos(th), math.sin(th)
        for ox, oy, r in obstacles:
            rho = r + inflate
            dx, dy = ox - x, oy - y
            along = dx * c + dy * s
            perp2 = (dx * dx + dy * dy) - along * along
            if perp2 >= rho * rho or along < 0.0:
                continue
            t = along - math.sqrt(rho * rho - perp2)
            best = min(best, max(t, 0.0))
        return best
    rad = v / abs(w)
    sgn = 1.0 if w > 0 else -1.0
    cx, cy = x - sgn * rad * math.sin(th), y + sgn * rad * math.cos(th)
    phi0 = math.atan2(y - cy, x - cx)
    for ox, oy, r in obstacles:
        rho = r + inflate
        dx, dy = ox - cx, oy - cy
        d = math.hypot(dx, dy)
        if d > rad + rho or d < rad - rho or d == 0.0:
            continue
        cosa = (rad * rad + d * d - rho * rho) / (2.0 * rad * d)
        a = math.acos(max(-1.0, min(1.0, cosa)))
        base = math.atan2(dy, dx)
        for phi in (base - a, base + a):
            delta = ((phi - phi0) * sgn) % TWO_PI
            best = min(best, rad * delta)
    return best


def stopping_distance(v, w, robot):
    """Arc length covered by holding (v, w) for one interval and then braking on the same arc.

    Braking keeps the ratio w / v (the same arc), so both speeds drop by the same fraction
    per interval; the fraction is set by the tighter of the two deceleration limits.
    """
    if v <= 0.0:
        return 0.0
    n = braking_intervals(v, w, robot)
    # Speeds v, v (n-1)/n, ..., v/n, each for dt: dt v (n + 1) / 2.
    return robot.dt * v * (n + 1) / 2.0


def braking_intervals(v, w, robot):
    """The number n of intervals after the first one that braking on the arc needs."""
    steps = max(v / (robot.a_v * robot.dt), abs(w) / (robot.a_w * robot.dt))
    return max(1, math.ceil(steps - 1e-12))


def brake_pair(v, w, robot):
    """The next velocity of the braking sequence on the current arc."""
    if v <= 0.0:
        step = robot.a_w * robot.dt
        return 0.0, (0.0 if abs(w) <= step else w - math.copysign(step, w))
    n = braking_intervals(v, w, robot)
    f = (n - 1) / n
    return v * f, w * f


def heading_score(pose, goal):
    """pi minus the absolute angle between the heading and the direction to the goal."""
    ang = math.atan2(goal[1] - pose[1], goal[0] - pose[0]) - pose[2]
    ang = (ang + math.pi) % TWO_PI - math.pi
    return math.pi - abs(ang)


def dwa_step(pose, vel, goal, obstacles, robot, alpha=2.0, beta=0.2, gamma=0.2, nv=11, nw=21, dist_cap=3.0):
    """Choose the velocity for the next interval. Returns (v, w)."""
    v0, w0 = vel
    dt = robot.dt
    vlo, vhi = max(0.0, v0 - robot.a_v * dt), min(robot.v_max, v0 + robot.a_v * dt)  # @line L1
    wlo, whi = max(-robot.w_max, w0 - robot.a_w * dt), min(robot.w_max, w0 + robot.a_w * dt)  # @line L1
    cands = [brake_pair(v0, w0, robot)]  # @line L2
    for i in range(nv):
        for j in range(nw):
            v = vlo + (vhi - vlo) * i / (nv - 1)
            w = wlo + (whi - wlo) * j / (nw - 1)
            cands.append((v, w))
    rows = []
    for v, w in cands:  # @line L2
        dist = arc_distance(pose, v, w, obstacles, robot.radius)  # @line L3
        s = stopping_distance(v, w, robot)
        if s > dist + 1e-9:  # @line L4
            continue
        t_stop = s / v if v > 0 else 0.0
        ahead = move(pose, v, w, t_stop if v > 0 else dt)
        rows.append((v, w, heading_score(ahead, goal), min(dist, dist_cap), v))  # @line L5
    if not rows:
        raise RuntimeError("no admissible velocity; the start velocity was not admissible")
    mh = max(r[2] for r in rows) or 1.0  # @line L6
    md = max(r[3] for r in rows) or 1.0
    ms = max(r[4] for r in rows) or 1.0
    best = max(rows, key=lambda r: alpha * r[2] / mh + beta * r[3] / md + gamma * r[4] / ms)  # @line L7
    return best[0], best[1]


def run(start, goal, obstacles, robot, max_steps=400, tol=0.2, record=None, **kw):
    """Simulate until the robot is within tol of the goal. Returns (pose, steps, reached)."""
    pose, vel = start, (0.0, 0.0)
    for k in range(max_steps):
        if math.hypot(goal[0] - pose[0], goal[1] - pose[1]) < tol:
            return pose, k, True
        v, w = dwa_step(pose, vel, goal, obstacles, robot, **kw)
        if record is not None:
            record(pose, vel, (v, w))
        pose = move(pose, v, w, robot.dt)  # @line L8
        vel = (v, w)
    return pose, max_steps, False
