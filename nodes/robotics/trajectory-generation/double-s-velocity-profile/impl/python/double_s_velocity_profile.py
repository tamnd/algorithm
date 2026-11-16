# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-s-velocity-profile/. The authors are listed in prov/07FRKR.jsonl.
"""Double-S velocity profile: rest-to-rest motion of one axis with bounded jerk.

double_s(D, V, A, J) returns (Tj, Ta, Tv, vp, T) for the distance D > 0
with |velocity| <= V, |acceleration| <= A and |jerk| <= J. Tj is the time
of one jerk ramp, Ta the time of the whole acceleration phase, Tv the time
of the cruise, vp the peak velocity and T = 2 Ta + Tv the total time. The
deceleration phase is the mirror image of the acceleration phase.

jerk_segments(...) lists the seven (duration, jerk) pieces, and sample()
integrates them exactly, piece by piece.
"""

import math


def double_s(D, V, A, J):
    """Times of the seven-segment rest-to-rest profile."""
    if min(D, V, A, J) <= 0:
        raise ValueError("D, V, A and J must be positive")
    if V * J >= A * A:  # @line L1
        Tj = A / J
        Ta = Tj + V / A
    else:
        Tj = math.sqrt(V / J)  # @line L2
        Ta = 2 * Tj
    if V * Ta <= D:  # @line L3
        Tv = D / V - Ta  # @line L4
        vp = V
    else:
        Tv = 0 * D  # @line L5
        if D * J * J >= 2 * A ** 3:  # @line L6
            Tj = A / J
            vp = (-A * A / J + math.sqrt(A ** 4 / J ** 2 + 4 * A * D)) / 2
            Ta = vp / A + Tj
        else:
            vp = (D * D * J / 4) ** (1 / 3)  # @line L7
            Tj = math.sqrt(vp / J)
            Ta = 2 * Tj
    return Tj, Ta, Tv, vp, 2 * Ta + Tv  # @line L8


def jerk_segments(Tj, Ta, Tv, J):
    """The seven pieces (duration, jerk); some durations can be zero."""
    Tc = Ta - 2 * Tj  # time at constant acceleration
    return [(Tj, J), (Tc, 0), (Tj, -J), (Tv, 0), (Tj, -J), (Tc, 0), (Tj, J)]


def _step(state, dt, j):
    s, v, a = state
    return (s + v * dt + a * dt * dt / 2 + j * dt ** 3 / 6, v + a * dt + j * dt * dt / 2, a + j * dt)


def sample(segments, t):
    """Return (s, v, a, j) at time t by exact integration of the pieces."""
    state = (0 * t, 0 * t, 0 * t)
    t0 = 0 * t
    for dur, j in segments:  # @line L9
        if t <= t0 + dur:
            s, v, a = _step(state, t - t0, j)
            return s, v, a, j
        state = _step(state, dur, j)  # @line L10
        t0 += dur
    s, v, a = state
    return s, v, a, 0


def peak_velocity_distance(vp, A, J):
    """Distance of a symmetric rest-to-rest profile with no cruise and peak velocity vp.

    Used by the tests as an independent check of the closed forms of line L6
    and line L7: the acceleration phase covers vp Ta / 2, so the move covers vp Ta.
    """
    if vp * J >= A * A:
        Ta = vp / A + A / J
    else:
        Ta = 2 * math.sqrt(vp / J)
    return vp * Ta
