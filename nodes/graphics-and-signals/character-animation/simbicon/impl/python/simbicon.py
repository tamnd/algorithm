# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simbicon/. The authors are listed in prov/FMSJGE.jsonl.
"""SIMBICON control of a planar biped: a toy.

The controller is the one of Yin, Loken and van de Panne (2007): a finite
state machine of target poses, PD control of every joint, the torso and the
swing hip controlled in the world frame, the stance hip torque
tau_A = -tau_torso - tau_B, and the balance feedback
theta_d = theta_d0 + c_d d + c_v v on the swing hip.

The simulated character is a toy, not the model of the paper. It has five
links (torso, two thighs, two shins), point feet, no ankles, a penalty
spring and damper for the ground and a tangential spring with a Coulomb
limit for friction. The world is the xy plane with y up and gravity
(0, -9.81) m/s^2; the character walks toward +x.

Coordinates q = (x, y, phi_0, ..., phi_4): (x, y) is the hip, phi_0 is the
world angle of the torso measured from straight up, and phi_1 ... phi_4
are the world angles of the left thigh, left shin, right thigh and right
shin measured from straight down. All angles are counterclockwise, so a
positive thigh angle puts the leg forward and a bent knee has a negative
relative angle phi_shin - phi_thigh, as in the paper.

The step is symplectic Euler: M(q) qdd = Q, then qd += dt qdd, q += dt qd.
All gains and the gait table are tuning; the number of steps without a fall
is a measurement of this toy only.
"""

import math

G = 9.81

# Links: (mass kg, length m). The shin includes the foot.
M_TORSO, L_TORSO = 70.0, 0.48
M_THIGH, L_THIGH = 5.0, 0.45
M_SHIN, L_SHIN = 4.0, 0.50

KP_JOINT, KD_JOINT = 300.0, 30.0       # Nm/rad and Nms/rad (paper, Section 7)
KP_GROUND, KD_GROUND = 1.0e5, 1.0e3    # N/m and Ns/m (toy values)
KT_GROUND, DT_GROUND = 5.0e4, 5.0e2    # tangential spring and damper (toy)
MU = 0.8                               # Coulomb friction (toy)
TORQUE_LIMIT = 400.0                   # Nm

# Index of each link angle in q.
TORSO, THIGH_L, SHIN_L, THIGH_R, SHIN_R = 2, 3, 4, 5, 6
LEGS = {"L": (THIGH_L, SHIN_L), "R": (THIGH_R, SHIN_R)}

# A gait is four states. Each has a duration (None means "until the swing
# foot touches"), c_d, c_v, and the targets: torso (world), swing hip
# (world), swing knee and stance knee (relative). States 0 and 1 swing the
# left leg, states 2 and 3 the right leg.
WALK_TABLE_1 = (
    # dt, cd, cv, torso, swing hip, swing knee, stance knee
    (0.30, 0.0, 0.20, 0.0, 0.40, -1.10, -0.05),
    (None, 2.20, 0.0, 0.0, -0.70, -0.05, -0.10),
)


def make_gait(table=WALK_TABLE_1):
    a, b = table
    return [a, b, a, b]


def swing_side(state):
    return "L" if state in (0, 1) else "R"


def stance_side(state):
    return "R" if state in (0, 1) else "L"


def _dirs(q):
    """Unit direction d_k and its derivative d'_k for every link angle."""
    d, dp = {}, {}
    s, c = math.sin(q[TORSO]), math.cos(q[TORSO])
    d[TORSO], dp[TORSO] = (-s, c), (-c, -s)
    for k in (THIGH_L, SHIN_L, THIGH_R, SHIN_R):
        s, c = math.sin(q[k]), math.cos(q[k])
        d[k], dp[k] = (s, -c), (c, s)
    return d, dp


# Each point is the hip plus a sum of a * d_k over its terms (k, a).
BODIES = (
    (M_TORSO, M_TORSO * L_TORSO ** 2 / 12.0, TORSO, ((TORSO, L_TORSO / 2),)),
    (M_THIGH, M_THIGH * L_THIGH ** 2 / 12.0, THIGH_L, ((THIGH_L, L_THIGH / 2),)),
    (M_SHIN, M_SHIN * L_SHIN ** 2 / 12.0, SHIN_L, ((THIGH_L, L_THIGH), (SHIN_L, L_SHIN / 2))),
    (M_THIGH, M_THIGH * L_THIGH ** 2 / 12.0, THIGH_R, ((THIGH_R, L_THIGH / 2),)),
    (M_SHIN, M_SHIN * L_SHIN ** 2 / 12.0, SHIN_R, ((THIGH_R, L_THIGH), (SHIN_R, L_SHIN / 2))),
)
FEET = {"L": ((THIGH_L, L_THIGH), (SHIN_L, L_SHIN)), "R": ((THIGH_R, L_THIGH), (SHIN_R, L_SHIN))}
TOTAL_MASS = sum(b[0] for b in BODIES)


def point(q, terms, d=None):
    if d is None:
        d, _ = _dirs(q)
    x, y = q[0], q[1]
    for k, a in terms:
        x += a * d[k][0]
        y += a * d[k][1]
    return x, y


def point_vel(q, qd, terms, dp=None):
    if dp is None:
        _, dp = _dirs(q)
    vx, vy = qd[0], qd[1]
    for k, a in terms:
        vx += a * dp[k][0] * qd[k]
        vy += a * dp[k][1] * qd[k]
    return vx, vy


def foot(q, side):
    return point(q, FEET[side])


def center_of_mass(q):
    d, _ = _dirs(q)
    sx = sy = 0.0
    for m, _, _, terms in BODIES:
        x, y = point(q, terms, d)
        sx += m * x
        sy += m * y
    return sx / TOTAL_MASS, sy / TOTAL_MASS


def dynamics(q, qd, gen_force):
    """Return qdd from M(q) qdd = gravity and velocity terms + gen_force."""
    n = 7
    d, dp = _dirs(q)
    M = [[0.0] * n for _ in range(n)]
    Q = list(gen_force)
    for m, inertia, own, terms in BODIES:
        M[0][0] += m
        M[1][1] += m
        M[own][own] += inertia
        # bias acceleration of the COM: -sum a d_k phi_k'^2
        bx = by = 0.0
        for k, a in terms:
            w2 = qd[k] * qd[k]
            bx -= a * d[k][0] * w2
            by -= a * d[k][1] * w2
        fx, fy = -m * bx, -m * (G + by)
        Q[0] += fx
        Q[1] += fy
        for k, a in terms:
            jx, jy = a * dp[k][0], a * dp[k][1]
            M[0][k] += m * jx
            M[1][k] += m * jy
            M[k][0] += m * jx
            M[k][1] += m * jy
            Q[k] += jx * fx + jy * fy
            for k2, a2 in terms:
                M[k][k2] += m * (jx * a2 * dp[k2][0] + jy * a2 * dp[k2][1])
    return solve(M, Q)


def solve(A, b):
    """Gaussian elimination with partial pivoting on copies of A and b."""
    n = len(b)
    A = [row[:] for row in A]
    b = list(b)
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        b[c], b[p] = b[p], b[c]
        piv = A[c][c]
        for r in range(c + 1, n):
            f = A[r][c] / piv
            if f != 0.0:
                Ar, Ac = A[r], A[c]
                for k in range(c, n):
                    Ar[k] -= f * Ac[k]
                b[r] -= f * b[c]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        s = b[r] - sum(A[r][k] * x[k] for k in range(r + 1, n))
        x[r] = s / A[r][r]
    return x


def joint_torques_to_generalized(tau):
    """tau = (hip_L, knee_L, hip_R, knee_R). A joint torque acts +tau on the
    child link angle and -tau on the parent link angle."""
    Q = [0.0] * 7
    pairs = ((TORSO, THIGH_L), (THIGH_L, SHIN_L), (TORSO, THIGH_R), (THIGH_R, SHIN_R))
    for t, (parent, child) in zip(tau, pairs):
        Q[child] += t
        Q[parent] -= t
    return Q


def pd(kp, kd, target, angle, rate):
    return kp * (target - angle) - kd * rate


def clampt(t):
    return max(-TORQUE_LIMIT, min(TORQUE_LIMIT, t))


def balance_target(theta0, cd, cv, d, v):
    """The SIMBICON feedback law theta_d = theta_d0 + c_d d + c_v v."""
    return theta0 + cd * d + cv * v


def control(state, q, qd, gait, kp=KP_JOINT, kd=KD_JOINT):
    """Return the joint torques (hip_L, knee_L, hip_R, knee_R) for one step."""
    _, cd, cv, tor, swh, swk, stk = gait[state]
    sw_th, sw_sh = LEGS[swing_side(state)]
    st_th, st_sh = LEGS[stance_side(state)]
    fx, _ = foot(q, stance_side(state))
    d = q[0] - fx  # @line L2
    v = qd[0]
    theta_swh = balance_target(swh, cd, cv, d, v)  # @line L3
    tau_torso = pd(kp, kd, tor, q[TORSO], qd[TORSO])  # @line L4
    tau_b = pd(kp, kd, theta_swh, q[sw_th], qd[sw_th])  # @line L5
    tau_a = -tau_torso - tau_b  # @line L6
    tau_swk = pd(kp, kd, swk, q[sw_sh] - q[sw_th], qd[sw_sh] - qd[sw_th])  # @line L7
    tau_stk = pd(kp, kd, stk, q[st_sh] - q[st_th], qd[st_sh] - qd[st_th])
    tau = {}
    tau[(swing_side(state), "hip")] = clampt(tau_b)
    tau[(swing_side(state), "knee")] = clampt(tau_swk)
    tau[(stance_side(state), "hip")] = clampt(tau_a)
    tau[(stance_side(state), "knee")] = clampt(tau_stk)
    return (tau[("L", "hip")], tau[("L", "knee")], tau[("R", "hip")], tau[("R", "knee")])  # @line L8


class Ground:
    """Penalty contact for one point foot, with a tangential anchor spring."""

    def __init__(self):
        self.anchor = {"L": None, "R": None}

    def force(self, side, p, v):
        x, y = p
        vx, vy = v
        if y >= 0.0:
            self.anchor[side] = None
            return 0.0, 0.0
        fn = max(0.0, -KP_GROUND * y - KD_GROUND * vy)
        if self.anchor[side] is None:
            self.anchor[side] = x
        ft = -KT_GROUND * (x - self.anchor[side]) - DT_GROUND * vx
        lim = MU * fn
        if abs(ft) > lim:
            ft = math.copysign(lim, ft)
            # slide: move the anchor so that the spring holds the limit
            self.anchor[side] = x + (ft + DT_GROUND * vx) / KT_GROUND
        return ft, fn


def foot_force_generalized(q, side, f):
    _, dp = _dirs(q)
    Q = [0.0] * 7
    Q[0] += f[0]
    Q[1] += f[1]
    for k, a in FEET[side]:
        Q[k] += a * (dp[k][0] * f[0] + dp[k][1] * f[1])
    return Q


def initial_state(speed=0.8):
    """Right foot under the hip, left leg behind and off the ground."""
    q = [0.0, L_THIGH + L_SHIN - 0.003, 0.0, -0.30, -0.45, 0.0, 0.0]
    qd = [speed, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    return q, qd


def fallen(q):
    return q[1] < 0.6 or abs(q[TORSO]) > 0.8


def simulate(gait=None, steps=5000, dt=0.001, speed=0.8):
    """Run the toy and return a dict with the measured quantities.

    Each line is one simulation step; the controller runs at every step.
    """
    if gait is None:
        gait = make_gait()
    q, qd = initial_state(speed)
    ground = Ground()
    state, clock = 0, 0.0
    strikes, fell_at, transitions = [], None, []
    for i in range(steps):
        sw = swing_side(state)
        fy_sw = foot(q, sw)[1]
        dur = gait[state][0]
        if (dur is not None and clock >= dur) or (dur is None and fy_sw < 0.0):  # @line L1
            if dur is None:
                strikes.append((i * dt, foot(q, sw)[0]))
            transitions.append((i * dt, state))
            state, clock = (state + 1) % 4, 0.0
        tau = control(state, q, qd, gait)
        Q = joint_torques_to_generalized(tau)
        _, dp = _dirs(q)
        for side in ("L", "R"):
            p = foot(q, side)
            v = point_vel(q, qd, FEET[side], dp)
            f = ground.force(side, p, v)
            if f != (0.0, 0.0):
                Qf = foot_force_generalized(q, side, f)
                Q = [a + b for a, b in zip(Q, Qf)]
        qdd = dynamics(q, qd, Q)
        qd = [a + dt * b for a, b in zip(qd, qdd)]
        q = [a + dt * b for a, b in zip(q, qd)]
        clock += dt
        if fallen(q):
            fell_at = i * dt
            break
    return {
        "strikes": strikes,
        "fell_at": fell_at,
        "transitions": transitions,
        "distance": q[0],
        "time": (i + 1) * dt,
        "q": q,
        "qd": qd,
    }
