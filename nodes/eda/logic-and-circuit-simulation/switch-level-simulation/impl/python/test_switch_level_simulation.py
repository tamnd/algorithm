# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/switch-level-simulation/. The authors are listed in prov/Z1Y4FS.jsonl.
"""Tests for switch-level simulation: hand-worked transistor networks, the path
definition of the steady state by brute force, and soundness of X results."""

import itertools
import random

import pytest

from switch_level_simulation import (
    NONE, OMEGA, X, Network, Oscillation, channel_connected_components, simulate,
    steady_state, switch_state,
)


def lub(u, v):
    return u if u == v else X


def leq(u, v):
    return u == v or v == X


# ---------------------------------------------------------------- networks

def inverter(net, a, out, strength=10):
    net.add_transistor("p", a, "vdd", out, strength)
    net.add_transistor("n", a, out, "gnd", strength)


def nand2():
    net = Network()
    net.add_input("a")
    net.add_input("b")
    net.add_node("out")
    net.add_node("m")
    net.add_transistor("p", "a", "vdd", "out")
    net.add_transistor("p", "b", "vdd", "out")
    net.add_transistor("n", "a", "out", "m")
    net.add_transistor("n", "b", "m", "gnd")
    return net


def nor2():
    net = Network()
    net.add_input("a")
    net.add_input("b")
    net.add_node("out")
    net.add_node("m")
    net.add_transistor("p", "a", "vdd", "m")
    net.add_transistor("p", "b", "m", "out")
    net.add_transistor("n", "a", "out", "gnd")
    net.add_transistor("n", "b", "out", "gnd")
    return net


def run(net, inputs, init=None):
    return simulate(net, inputs, init or {})[0]


# ---------------------------------------------------------------- hand-worked networks

def test_switch_states():
    assert [switch_state("n", v) for v in (0, 1, X)] == [0, 1, X]
    assert [switch_state("p", v) for v in (0, 1, X)] == [1, 0, X]


def test_cmos_inverter():
    net = Network()
    net.add_input("a")
    net.add_node("y")
    inverter(net, "a", "y")
    assert run(net, {"a": 0})["y"] == 1
    assert run(net, {"a": 1})["y"] == 0
    assert run(net, {"a": X})["y"] == X


def test_nand2_with_internal_node():
    net = nand2()
    expect = {(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 0}
    for (a, b), y in expect.items():
        assert run(net, {"a": a, "b": b}, {"m": 0})["out"] == y
    # internal node m, worked by hand
    assert run(net, {"a": 0, "b": 1}, {"m": 1})["m"] == 0      # pulled down by n_b
    assert run(net, {"a": 1, "b": 0}, {"m": 0})["m"] == 1      # joined to out through n_a
    assert run(net, {"a": 0, "b": 0}, {"m": 1})["m"] == 1      # isolated: keeps its charge
    assert run(net, {"a": 0, "b": 0}, {"m": 0})["m"] == 0


def test_nand2_x_input():
    net = nand2()
    # a = 0 holds out at 1 through p_a, whatever b is.
    assert run(net, {"a": 0, "b": X}, {"m": 0})["out"] == 1
    assert run(net, {"a": X, "b": 0}, {"m": 0})["out"] == 1
    # a = 1, b = X: out can be 0 or 1.
    assert run(net, {"a": 1, "b": X}, {"m": 0})["out"] == X


def test_nor2():
    net = nor2()
    expect = {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 0}
    for (a, b), y in expect.items():
        assert run(net, {"a": a, "b": b}, {"m": 0})["out"] == y
    assert run(net, {"a": 1, "b": X}, {"m": 0})["out"] == 0


def test_ratioed_nmos_inverter():
    net = Network()
    net.add_input("a")
    net.add_node("y")
    net.add_transistor("n", "vdd", "vdd", "y", 4)   # load, always on, weak
    net.add_transistor("n", "a", "y", "gnd", 8)     # pull-down, strong
    assert run(net, {"a": 0})["y"] == 1
    assert run(net, {"a": 1})["y"] == 0
    assert run(net, {"a": X})["y"] == X


def test_dynamic_latch_keeps_charge():
    net = Network()
    net.add_input("d")
    net.add_input("phi")
    net.add_node("s")
    net.add_node("q")
    net.add_transistor("n", "phi", "d", "s")
    inverter(net, "s", "q")
    v = run(net, {"d": 1, "phi": 1})
    assert (v["s"], v["q"]) == (1, 0)
    v = run(net, {"d": 0, "phi": 0}, {"s": v["s"], "q": v["q"]})
    assert (v["s"], v["q"]) == (1, 0)                   # stored, d is cut off
    v = run(net, {"d": 0, "phi": 1}, {"s": v["s"], "q": v["q"]})
    assert (v["s"], v["q"]) == (0, 1)


def charge_pair(size_a, size_b):
    net = Network()
    net.add_input("e")
    net.add_node("a", size_a)
    net.add_node("b", size_b)
    net.add_transistor("n", "e", "a", "b")
    return net


def test_charge_sharing_by_size():
    v = run(charge_pair(2, 1), {"e": 1}, {"a": 1, "b": 0})
    assert (v["a"], v["b"]) == (1, 1)                   # the larger node wins
    v = run(charge_pair(1, 2), {"e": 1}, {"a": 1, "b": 0})
    assert (v["a"], v["b"]) == (0, 0)
    v = run(charge_pair(1, 1), {"e": 1}, {"a": 1, "b": 0})
    assert (v["a"], v["b"]) == (X, X)                   # equal sizes: unknown
    v = run(charge_pair(1, 1), {"e": 0}, {"a": 1, "b": 0})
    assert (v["a"], v["b"]) == (1, 0)                   # switch open: both keep
    v = run(charge_pair(2, 1), {"e": X}, {"a": 1, "b": 0})
    assert (v["a"], v["b"]) == (1, X)


def bus(sa, sb):
    net = Network()
    net.add_input("a")
    net.add_input("b")
    net.add_node("bus")
    net.add_transistor("n", "a", "vdd", "bus", sa)
    net.add_transistor("n", "b", "bus", "gnd", sb)
    return net


def test_bus_fight():
    assert run(bus(10, 10), {"a": 1, "b": 1})["bus"] == X
    assert run(bus(10, 6), {"a": 1, "b": 1})["bus"] == 1
    assert run(bus(6, 10), {"a": 1, "b": 1})["bus"] == 0
    assert run(bus(10, 10), {"a": 1, "b": 0})["bus"] == 1
    assert run(bus(10, 10), {"a": 0, "b": 0}, {"bus": 0})["bus"] == 0
    assert run(bus(10, 6), {"a": 1, "b": X})["bus"] == 1     # the stronger side is on
    assert run(bus(10, 6), {"a": X, "b": 1})["bus"] == X


def test_strongest_signal_blocks_weaker_path():
    # vdd -5- m, gnd -10- m, m -5- n: the vdd signal is blocked at m.
    net = Network()
    net.add_node("m")
    net.add_node("n")
    net.add_transistor("n", "vdd", "vdd", "m", 5)
    net.add_transistor("n", "vdd", "gnd", "m", 10)
    net.add_transistor("n", "vdd", "m", "n", 5)
    v = run(net, {}, {"m": 1, "n": 1})
    assert (v["m"], v["n"]) == (0, 0)


def test_documented_x_pessimism():
    # Two transistors in parallel from vdd, one n-type and one p-type, both gated by s.
    # For s = 0 or s = 1 one of them conducts, so out = 1. With s = X both are in
    # state X, no path is definite, and the stored 0 may survive: the result is X.
    net = Network()
    net.add_input("s")
    net.add_node("out")
    net.add_transistor("n", "s", "vdd", "out")
    net.add_transistor("p", "s", "vdd", "out")
    assert run(net, {"s": 0}, {"out": 0})["out"] == 1
    assert run(net, {"s": 1}, {"out": 0})["out"] == 1
    assert run(net, {"s": X}, {"out": 0})["out"] == X
    assert run(net, {"s": X}, {"out": 1})["out"] == 1


def test_ring_oscillator_never_settles():
    net = Network()
    for k in range(3):
        net.add_node(f"n{k}")
    for k in range(3):
        inverter(net, f"n{k}", f"n{(k + 1) % 3}")
    with pytest.raises(Oscillation):
        simulate(net, {}, {"n0": 0, "n1": 1, "n2": 0}, max_rounds=50)
    v, _ = simulate(net, {}, {})                         # all X is a fixed point
    assert [v[f"n{k}"] for k in range(3)] == [X, X, X]


def test_cross_coupled_inverters_hold():
    net = Network()
    net.add_node("q")
    net.add_node("qb")
    inverter(net, "q", "qb")
    inverter(net, "qb", "q")
    v = run(net, {}, {"q": 1, "qb": 0})
    assert (v["q"], v["qb"]) == (1, 0)
    v = run(net, {}, {"q": 0, "qb": 1})
    assert (v["q"], v["qb"]) == (0, 1)


def test_channel_connected_components():
    net = nand2()
    comps = channel_connected_components(net)
    assert sorted(sorted(c[0]) for c in comps) == [["m", "out"]]
    chain = Network()
    chain.add_input("a")
    names = ["a"] + [f"y{k}" for k in range(4)]
    for k in range(4):
        chain.add_node(names[k + 1])
        inverter(chain, names[k], names[k + 1])
    assert len(channel_connected_components(chain)) == 4
    tg = Network()
    tg.add_input("s")
    tg.add_input("sb")
    for n in ("u", "w"):
        tg.add_node(n)
    tg.add_transistor("n", "s", "u", "w")
    tg.add_transistor("p", "sb", "u", "w")
    assert sorted(sorted(c[0]) for c in channel_connected_components(tg)) == [["u", "w"]]


def test_check_rejects_sizes_above_strengths():
    net = Network()
    net.add_node("y", 5)
    net.add_transistor("n", "vdd", "vdd", "y", 3)
    with pytest.raises(ValueError):
        simulate(net, {}, {})


# ---------------------------------------------------------------- brute force

def random_network(rng, k):
    net = Network()
    for name in ("i0", "i1"):
        net.add_input(name)
    for j in range(k):
        net.add_node(f"s{j}", rng.choice((1, 2)))
    storage = [f"s{j}" for j in range(k)]
    for _ in range(rng.randint(k, k + 4)):
        a = rng.choice(storage)
        b = rng.choice([n for n in storage + net.inputs if n != a])
        g = rng.choice(storage + ["i0", "i1"])
        net.add_transistor(rng.choice("np"), g, a, b, rng.choice((3, 4, 5)))
    return net


def brute_steady(net, nodes, trans, val):
    """The path definition, by enumeration of simple paths. Transistor gates must be binary."""
    adj = {n: [] for n in nodes}
    starts = [(m, net.size[m], val[m]) for m in nodes]
    for i in trans:
        kind, g, a, b, gamma = net.trans[i]
        assert val[g] != X
        if switch_state(kind, val[g]) == 0:
            continue
        for u, w in ((a, b), (b, a)):
            if w in adj:
                if net.is_input(u):
                    starts.append((w, gamma, val[u]))
                else:
                    adj[w].append((u, gamma))
    paths = []  # (list of (node, prefix strength), source value)

    def extend(path, value):
        paths.append((list(path), value))
        node, p = path[-1]
        on_path = {m for m, _ in path}
        for w, gamma in adj[node]:
            if w not in on_path:
                path.append((w, min(p, gamma)))
                extend(path, value)
                path.pop()

    for m, s, v in starts:
        extend([(m, s)], v)
    strength = {n: max(p for path, _ in paths for m, p in path if m == n) for n in nodes}
    value = {}
    for path, v in paths:
        if all(p == strength[m] for m, p in path):
            n = path[-1][0]
            value[n] = v if n not in value else lub(value[n], v)
    return value, strength


def relevant(net, nodes, trans):
    names = set(nodes)
    for i in trans:
        kind, g, a, b, s = net.trans[i]
        names |= {g, a, b}
    return sorted(names - {"vdd", "gnd"})


def random_val(rng, net, p_x):
    val = {n: (X if rng.random() < p_x else rng.randint(0, 1)) for n in list(net.size) + ["i0", "i1"]}
    val["vdd"], val["gnd"] = 1, 0
    return val


def test_binary_steady_state_matches_path_definition():
    rng = random.Random(41)
    checked = 0
    for _ in range(300):
        net = random_network(rng, rng.randint(1, 5))
        val = random_val(rng, net, 0.0)
        for nodes, trans in channel_connected_components(net):
            got, strength = steady_state(net, nodes, trans, val)
            want, want_strength = brute_steady(net, nodes, trans, val)
            assert strength == want_strength
            assert got == want
            checked += len(nodes)
    assert checked > 500


def test_x_charges_with_binary_gates_match_path_definition():
    rng = random.Random(42)
    for _ in range(200):
        net = random_network(rng, rng.randint(1, 5))
        val = random_val(rng, net, 0.3)
        for n in ("i0", "i1"):
            val[n] = rng.randint(0, 1)
        for nodes, trans in channel_connected_components(net):
            if any(val[net.trans[i][1]] == X for i in trans):
                continue
            assert steady_state(net, nodes, trans, val)[0] == brute_steady(net, nodes, trans, val)[0]


def completions(val, names):
    free = [n for n in names if val[n] == X]
    for bits in itertools.product((0, 1), repeat=len(free)):
        c = dict(val)
        c.update(zip(free, bits))
        yield c


def test_ternary_steady_state_is_sound():
    rng = random.Random(43)
    exact = total = 0
    for _ in range(150):
        net = random_network(rng, rng.randint(1, 4))
        val = random_val(rng, net, 0.35)
        for nodes, trans in channel_connected_components(net):
            got, _ = steady_state(net, nodes, trans, val)
            best = {}
            for c in completions(val, relevant(net, nodes, trans)):
                want, _ = brute_steady(net, nodes, trans, c)
                for n in nodes:
                    best[n] = want[n] if n not in best else lub(best[n], want[n])
            for n in nodes:
                assert leq(best[n], got[n])
                total += 1
                exact += best[n] == got[n]
    assert total > 200 and exact > total // 2


def test_steady_state_is_monotone():
    rng = random.Random(44)
    for _ in range(300):
        net = random_network(rng, rng.randint(1, 5))
        val = random_val(rng, net, 0.2)
        up = {n: (X if rng.random() < 0.3 and n not in ("vdd", "gnd") else v) for n, v in val.items()}
        for nodes, trans in channel_connected_components(net):
            lo, _ = steady_state(net, nodes, trans, val)
            hi, _ = steady_state(net, nodes, trans, up)
            assert all(leq(lo[n], hi[n]) for n in nodes)


def test_simulate_is_sound_against_binary_runs():
    rng = random.Random(45)
    settled = compared = 0
    for _ in range(120):
        net = random_network(rng, rng.randint(2, 5))
        inputs = {"i0": rng.choice((0, 1, X)), "i1": rng.choice((0, 1, X))}
        init = {n: rng.choice((0, 1, X)) for n in net.size}
        try:
            top, _ = simulate(net, inputs, init, max_rounds=60)
        except Oscillation:
            continue
        settled += 1
        start = dict(init)
        start.update(inputs)
        names = [n for n in start if start[n] == X][:6]
        for c in completions(start, names):
            for n in start:
                if c[n] == X:
                    c[n] = 0
            try:
                low, _ = simulate(net, {k: c[k] for k in inputs}, {k: c[k] for k in init}, max_rounds=60)
            except Oscillation:
                continue
            compared += 1
            assert all(leq(low[n], top[n]) for n in net.size)
    assert settled > 60 and compared > 200


def test_constants():
    assert NONE < 0 < X < OMEGA
