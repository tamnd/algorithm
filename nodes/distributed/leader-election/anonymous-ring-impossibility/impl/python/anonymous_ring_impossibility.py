# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anonymous-ring-impossibility/. The authors are listed in prov/DFYQ3T.jsonl.

"""Symmetry of anonymous rings, checked by running programs.

A program is one deterministic state machine for all processes. In a round,
each process computes its two outgoing messages (to the left and to the right)
from its state, and then its new state from its state and the two messages it
received. On an oriented ring, the message a process gets on its left port is
the one its left neighbour sent to the right.

The functions here run a program in lock-step rounds and also in the
asynchronous phase schedule of the proof, and record the states so the tests
can check that all processes stay in the same state.
"""

import random
from typing import Callable, Hashable

State = Hashable
Msg = Hashable
Program = tuple[
    Callable[[int], State],                      # init(n) -> state
    Callable[[State], tuple[Msg, Msg]],          # send(state) -> (to left, to right)
    Callable[[State, Msg, Msg], State],          # step(state, from left, from right) -> state
    Callable[[State], bool],                     # is_leader(state)
]


def run_sync(prog: Program, n: int, rounds: int) -> list[list[State]]:
    """Lock-step rounds on an oriented ring of n identical processes."""
    init, send, step, _ = prog
    states = [init(n) for _ in range(n)]
    history = [list(states)]
    for _ in range(rounds):
        out = [send(s) for s in states]
        new = []
        for i in range(n):
            from_left = out[(i - 1) % n][1]   # left neighbour sent it to the right
            from_right = out[(i + 1) % n][0]  # right neighbour sent it to the left
            new.append(step(states[i], from_left, from_right))
        states = new
        history.append(list(states))
    return history


def run_phases(prog: Program, n: int, phases: int) -> list[list[State]]:
    """The asynchronous schedule of the proof.

    In each phase the processes take turns, p_0 first. A process takes the
    messages that were in its input channels at the start of the phase (left
    channel first), and sends at once; messages sent in a phase are delivered
    in the next phase. This is a fair asynchronous run; it is not lock-step,
    because p_1 moves after p_0 has already moved.
    """
    init, send, step, _ = prog
    states = [init(n) for _ in range(n)]
    left_in = [[send(states[(i - 1) % n])[1]] for i in range(n)]
    right_in = [[send(states[(i + 1) % n])[0]] for i in range(n)]
    history = [list(states)]
    for _ in range(phases):
        snap_left = [list(q) for q in left_in]
        snap_right = [list(q) for q in right_in]
        for i in range(n):
            left_in[i].clear()
            right_in[i].clear()
        for i in range(n):  # p_0, then p_1, and so on
            for a, b in zip(snap_left[i], snap_right[i]):
                states[i] = step(states[i], a, b)
                to_left, to_right = send(states[i])
                right_in[(i - 1) % n].append(to_left)
                left_in[(i + 1) % n].append(to_right)
        history.append(list(states))
    return history


def random_program(seed: int, k: int = 7) -> Program:
    """A seeded random deterministic program with k states that knows n."""

    def table(*key: object) -> int:
        return random.Random(repr((seed,) + key)).randrange(k)

    def init(n: int) -> State:
        return table("init", n)

    def send(s: State) -> tuple[Msg, Msg]:
        return table("left", s), table("right", s)

    def step(s: State, a: Msg, b: Msg) -> State:
        return table("step", s, a, b)

    def is_leader(s: State) -> bool:
        return s == 0

    return init, send, step, is_leader


def lcr_without_ids() -> Program:
    """Chang-Roberts with every identifier equal to 1, and n known.

    Each process sends its value to the right; when a process has seen n
    values it decides. All processes decide leader in the same round.
    """

    def init(n: int) -> State:
        return (1, 0, n, False)  # (value, count, n, leader)

    def send(s: State) -> tuple[Msg, Msg]:
        return None, s[0]

    def step(s: State, a: Msg, b: Msg) -> State:
        value, count, n, leader = s
        count += 1
        if a is not None and a == value and count >= n:
            leader = True
        return value, count, n, leader

    def is_leader(s: State) -> bool:
        return s[3]

    return init, send, step, is_leader


def leaders(prog: Program, states: list[State]) -> int:
    return sum(1 for s in states if prog[3](s))
