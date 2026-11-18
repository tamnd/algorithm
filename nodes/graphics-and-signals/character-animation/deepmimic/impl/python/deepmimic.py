# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deepmimic/. The authors are listed in prov/MY80RM.jsonl.
"""A toy of the DeepMimic episode: imitation reward, reference state
initialization (RSI) and early termination (ET).

This is not DeepMimic. There is no neural network and no PPO here. The
character is one rigid rod on a motor at its base (an inverted pendulum in
the x-y plane, y up), and the policy is any function of the state and the
phase. What the toy keeps from Peng et al. (2018) is the structure of one
episode:

  * the reference motion is a periodic clip q_hat(t) = A sin(2 pi t / T);
  * the imitation reward is
        r_I = 0.65 r_p + 0.1 r_v + 0.15 r_e + 0.1 r_c,
        r_p = exp(-2 (q_hat - q)^2),          pose
        r_v = exp(-0.1 (qd_hat - qd)^2),      velocity
        r_e = exp(-40 |e_hat - e|^2),         end effector (the tip)
        r_c = exp(-10 |c_hat - c|^2),         center of mass (the mid point)
    and with a task reward r_G the reward is 0.7 r_I + 0.3 r_G. The weights
    and scales are the paper's; for one joint the quaternion difference of
    the pose term is the angle difference;
  * the policy acts at 30 Hz and the physics steps at 1.2 kHz;
  * RSI starts each episode at a random phase of the clip, in the reference
    state of that phase; the other choice starts at phase 0;
  * ET ends the episode when the tip falls below a height; that step and
    every later step then have reward 0.

The rod: mass m, length l, angle q from straight up, counterclockwise,
moment of inertia m l^2 / 3 about the base. The motor torque is clamped to
tau_max. The ground is at the base height: when |q| reaches pi / 2 the rod
lies on the ground and stays there (q held, qd = 0).
"""

import math

G = 9.81


class Rod:
    def __init__(self, m=10.0, l=1.0, damping=0.5, tau_max=150.0):
        self.m, self.l, self.b, self.tau_max = m, l, damping, tau_max
        self.I = m * l * l / 3.0

    def tip(self, q):
        return (-self.l * math.sin(q), self.l * math.cos(q))

    def com(self, q):
        return (-0.5 * self.l * math.sin(q), 0.5 * self.l * math.cos(q))

    def step(self, q, qd, tau, dt):
        """One symplectic Euler step with the ground stop."""
        tau = max(-self.tau_max, min(self.tau_max, tau))
        qdd = (tau + self.m * G * 0.5 * self.l * math.sin(q) - self.b * qd) / self.I
        qd = qd + dt * qdd
        q = q + dt * qd
        if abs(q) >= math.pi / 2:
            q = math.copysign(math.pi / 2, q)
            qd = 0.0
        return q, qd


class Reference:
    def __init__(self, amplitude=0.4, period=2.0):
        self.A, self.T = amplitude, period

    def q(self, t):
        return self.A * math.sin(2 * math.pi * t / self.T)

    def qd(self, t):
        return self.A * 2 * math.pi / self.T * math.cos(2 * math.pi * t / self.T)


def imitation_reward(rod, ref, t, q, qd):
    qh, qdh = ref.q(t), ref.qd(t)
    rp = math.exp(-2.0 * (qh - q) ** 2)
    rv = math.exp(-0.1 * (qdh - qd) ** 2)
    eh, e = rod.tip(qh), rod.tip(q)
    re = math.exp(-40.0 * ((eh[0] - e[0]) ** 2 + (eh[1] - e[1]) ** 2))
    ch, c = rod.com(qh), rod.com(q)
    rc = math.exp(-10.0 * ((ch[0] - c[0]) ** 2 + (ch[1] - c[1]) ** 2))
    return 0.65 * rp + 0.1 * rv + 0.15 * re + 0.1 * rc


def reward(rod, ref, t, q, qd, r_goal=None):
    r_i = imitation_reward(rod, ref, t, q, qd)
    if r_goal is None:
        return r_i
    return 0.7 * r_i + 0.3 * r_goal


def initial_state(ref, rng=None):
    """RSI if rng is given: a uniform phase and the reference state there."""
    t0 = rng.uniform(0.0, ref.T) if rng is not None else 0.0
    return t0, ref.q(t0), ref.qd(t0)


def episode(rod, ref, policy, steps=60, rng=None, early_termination=True,
            fall_height=0.5, control_hz=30, sim_hz=1200, gamma=0.95):
    """Run one episode of `steps` control steps.

    Return a dict with the rewards per control step (0 after termination),
    the discounted return, the step of termination (None if none), and the
    number of control steps spent in a fallen state."""
    t, q, qd = initial_state(ref, rng)  # @line L1
    sub = sim_hz // control_hz
    dt = 1.0 / sim_hz
    rewards = []
    ended = None
    fallen_steps = 0
    for k in range(steps):
        if ended is not None:
            rewards.append(0.0)
            continue
        tau = policy(t, q, qd)  # @line L2
        for _ in range(sub):
            q, qd = rod.step(q, qd, tau, dt)  # @line L3
            t += dt
        r = reward(rod, ref, t, q, qd)  # @line L4
        fallen = rod.tip(q)[1] < fall_height
        fallen_steps += fallen
        if fallen and early_termination:
            ended = k  # @line L5
            r = 0.0
        rewards.append(r)
    ret = sum(gamma ** k * r for k, r in enumerate(rewards))  # @line L6
    return {"rewards": rewards, "return": ret, "ended": ended, "fallen_steps": fallen_steps}


def pd_policy(rod, ref, kp=400.0, kd=40.0):
    """A hand made tracking policy: PD on the reference plus gravity
    compensation. It stands in for a trained network."""
    def policy(t, q, qd):
        return (kp * (ref.q(t) - q) + kd * (ref.qd(t) - qd)
                - rod.m * G * 0.5 * rod.l * math.sin(q))
    return policy


def zero_policy(t, q, qd):
    return 0.0
