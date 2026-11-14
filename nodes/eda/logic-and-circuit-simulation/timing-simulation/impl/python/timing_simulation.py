# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/timing-simulation/. The authors are listed in prov/F3Y8TC.jsonl.
"""Timing simulation of MOS circuits in the style of MOTIS.

Every circuit node has a capacitance to ground. Transistors follow the
square-law (Shichman-Hodges, level 1) model with no body effect and no
channel-length modulation. The node equations C_i dv_i/dt = I_i(v) are
discretized by backward Euler. Instead of solving the whole nonlinear
system by Newton's method, each time step visits the nodes in a fixed order,
Gauss-Seidel style, and does one Newton step on each node's own equation,
with the newest voltages of the other nodes. Nodes whose neighbours did not
move by more than eps are skipped (event skipping).

Units: volts, nanoseconds, femtofarads and microamperes, which agree:
1 fF * 1 V / 1 ns = 1 uA.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional, Sequence, Tuple


class Circuit:
    """Nodes with grounded capacitors, fixed nodes with voltage waveforms, and MOSFETs."""

    def __init__(self, vdd: float = 1.8, vt: float = 0.5) -> None:
        self.vdd = vdd
        self.vt = vt
        self.fixed: Dict[str, Callable[[float], float]] = {"vdd": lambda t: vdd, "gnd": lambda t: 0.0}
        self.order: List[str] = []
        self.cap: Dict[str, float] = {}
        self.trans: List[Tuple[str, str, str, str, float]] = []  # (kind, gate, a, b, k)

    def add_input(self, name: str, wave: Callable[[float], float]) -> None:
        self.fixed[name] = wave

    def add_node(self, name: str, cap: float) -> None:
        self.order.append(name)
        self.cap[name] = cap

    def add_transistor(self, kind: str, gate: str, a: str, b: str, k: float) -> None:
        if kind not in ("n", "p"):
            raise ValueError("a transistor is of type n or p")
        self.trans.append((kind, gate, a, b, k))

    def at_node(self) -> Dict[str, List[int]]:
        """Transistors whose channel touches each node."""
        out: Dict[str, List[int]] = {n: [] for n in self.order}
        for i, (kind, g, a, b, k) in enumerate(self.trans):
            for n in {a, b}:
                if n in out:
                    out[n].append(i)
        return out

    def fanout(self) -> Dict[str, List[str]]:
        """For each node or input, the nodes whose current depends on its voltage."""
        out: Dict[str, set] = {n: set() for n in list(self.order) + list(self.fixed)}
        for kind, g, a, b, k in self.trans:
            for n in (a, b):
                if n in self.cap:
                    out[g].add(n)
                    out[a].add(n)
                    out[b].add(n)
        return {n: sorted(s, key=self.order.index) for n, s in out.items()}


def ramp(t0: float, t1: float, v0: float, v1: float) -> Callable[[float], float]:
    """A piecewise-linear waveform: v0 until t0, a straight line to v1 at t1, then v1."""
    def wave(t: float) -> float:
        if t <= t0:
            return v0
        if t >= t1:
            return v1
        return v0 + (v1 - v0) * (t - t0) / (t1 - t0)
    return wave


def mos(kind: str, k: float, vt: float, vg: float, va: float, vb: float) -> Tuple[float, float, float, float]:
    """Channel current from terminal a to terminal b, and its derivatives in va, vb and vg."""
    if kind == "n":
        if va >= vb:
            sign, vd, vs = 1.0, va, vb
        else:
            sign, vd, vs = -1.0, vb, va
        vov, vds = vg - vs - vt, vd - vs
    else:
        if va >= vb:
            sign, vs, vd = 1.0, va, vb
        else:
            sign, vs, vd = -1.0, vb, va
        vov, vds = vs - vg - vt, vs - vd
    if vov <= 0.0:
        return 0.0, 0.0, 0.0, 0.0
    if vds < vov:
        cur = k * (vov * vds - 0.5 * vds * vds)
        gm, gds = k * vds, k * (vov - vds)
    else:
        cur = 0.5 * k * vov * vov
        gm, gds = k * vov, 0.0
    # Derivatives of cur in the gate, the higher and the lower channel terminal.
    if kind == "n":
        d_g, d_hi, d_lo = gm, gds, -gm - gds
    else:
        d_g, d_hi, d_lo = -gm, gm + gds, -gds
    if sign > 0:
        return cur, d_hi, d_lo, d_g
    return -cur, -d_lo, -d_hi, -d_g


def node_current(c: Circuit, at: Sequence[int], node: str, v: Dict[str, float]) -> Tuple[float, float]:
    """Current into the node through the channels at it, and its derivative in the node voltage."""
    total = deriv = 0.0
    for i in at:
        kind, g, a, b, k = c.trans[i]
        i_ab, d_a, d_b, d_g = mos(kind, k, c.vt, v[g], v[a], v[b])
        sign = -1.0 if node == a else 1.0  # current a -> b leaves a and enters b
        total += sign * i_ab
        deriv += sign * ((d_a if node == a else 0.0) + (d_b if node == b else 0.0) + (d_g if node == g else 0.0))
    return total, deriv


def motis(c: Circuit, init: Dict[str, float], t_end: float, h: float, eps: float = 0.0,
          exact: bool = False) -> Tuple[List[float], Dict[str, List[float]], int]:
    """Timing simulation. Returns (time points, waveform of every node, node updates).

    With exact=True each node equation is solved to convergence instead of one Newton step.
    """
    at = c.at_node()
    fan = c.fanout()
    v = {n: f(0.0) for n, f in c.fixed.items()}  # @line L1
    v.update({n: init[n] for n in c.order})
    active = set(c.order)
    times, waves, evals = [0.0], {n: [v[n]] for n in c.order}, 0
    steps = int(round(t_end / h))
    for s in range(1, steps + 1):  # @line L2
        t = s * h
        for n, f in c.fixed.items():  # @line L3
            new = f(t)
            if abs(new - v[n]) > eps or eps <= 0.0:
                active.update(fan[n])
            v[n] = new
        woken = set()
        for n in c.order:  # @line L4
            if n not in active and eps > 0.0:  # @line L5
                continue
            evals += 1
            old = v[n]
            cur, d = node_current(c, at[n], n, v)  # @line L6
            v[n] = old + h * cur / (c.cap[n] - h * d)  # @line L7
            if exact:
                v[n] = _solve_node(c, at[n], n, v, old, h)
            if abs(v[n] - old) > eps:  # @line L8
                woken.add(n)
                woken.update(fan[n])
                active.update(fan[n])
        active = woken  # @line L9
        times.append(t)  # @line L10
        for n in c.order:
            waves[n].append(v[n])
    return times, waves, evals  # @line L11


def _solve_node(c: Circuit, at: Sequence[int], n: str, v: Dict[str, float], old: float, h: float) -> float:
    """Solve C (x - old) / h = I(x) for the voltage x of node n, others fixed.

    The left side minus the right side increases in x when the gates at the node are
    other nodes, so the root is unique. Newton steps, kept inside a bracket.
    """
    def g(x: float) -> Tuple[float, float]:
        v[n] = x
        cur, d = node_current(c, at, n, v)
        return c.cap[n] * (x - old) / h - cur, c.cap[n] / h - d

    lo, hi = -10.0 * c.vdd - 10.0, 10.0 * c.vdd + 10.0
    x = v[n]
    for _ in range(200):
        gx, dx = g(x)
        if gx > 0:
            hi = min(hi, x)
        else:
            lo = max(lo, x)
        step = gx / dx
        nxt = x - step
        if not lo < nxt < hi:
            nxt = 0.5 * (lo + hi)
        if abs(nxt - x) < 1e-13:
            x = nxt
            break
        x = nxt
    v[n] = x
    return x


def crossing(times: Sequence[float], wave: Sequence[float], level: float) -> Optional[float]:
    """First time at which the waveform crosses the level, by linear interpolation."""
    for i in range(1, len(wave)):
        a, b = wave[i - 1] - level, wave[i] - level
        if a == 0.0:
            return times[i - 1]
        if a * b < 0.0:
            return times[i - 1] + (times[i] - times[i - 1]) * a / (a - b)
    return None
