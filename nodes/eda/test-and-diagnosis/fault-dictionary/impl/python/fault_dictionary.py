# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fault-dictionary/. The authors are listed in prov/4SH7E3.jsonl.
"""Fault dictionaries for single stuck-at faults.

A dictionary is built once from a circuit and a test set t_0, ..., t_(T-1).
For each modeled fault f it stores the response of the faulty circuit, coded
as an error word per test: bit k of R[f][j] is 1 when output k of the faulty
circuit differs from the good circuit on test j.

- The full-response dictionary maps the tuple R[f] to the faults with that
  response. It needs T * O bits per fault for O outputs.
- The pass-fail dictionary maps the set P[f] of failing tests (a T-bit mask)
  to the faults with that set. It needs T bits per fault.

Diagnosis looks up the response observed on the tester. Building costs one
fault simulation per (fault, test) pair; a lookup is one hash probe.
"""

from __future__ import annotations

from typing import Iterable, Optional, Sequence

from td3net import Circuit, Fault


def error_word(good: Sequence[int], seen: Sequence[int]) -> int:
    """Bit k is 1 when output k differs from the good value."""
    w = 0
    for k, (g, s) in enumerate(zip(good, seen)):
        if g != s:
            w |= 1 << k
    return w


class FaultDictionary:
    """Full-response and pass-fail dictionaries over one test set."""

    def __init__(self, circuit: Circuit, tests: Sequence[Sequence[int]]) -> None:
        """Precondition: every test is a 0/1 vector over the primary inputs. Cost O(T (L + P))."""
        self.circuit = circuit
        self.tests = [tuple(t) for t in tests]
        self.n_outputs = len(circuit.po)
        self.good = [circuit.outputs(t) for t in self.tests]  # @line L1
        self.response: dict[Fault, tuple[int, ...]] = {}
        self.full: dict[tuple[int, ...], list[Fault]] = {}
        self.pass_fail: dict[int, list[Fault]] = {}

    def add_fault(self, fault: Fault) -> None:
        """Simulate one fault on every test and file it in both dictionaries. O(T (L + P))."""
        if fault in self.response:
            return
        r = tuple(  # @line L2
            error_word(g, self.circuit.outputs(t, fault))  # @line L3
            for t, g in zip(self.tests, self.good)
        )
        p = 0  # @line L4
        for j, w in enumerate(r):
            if w:
                p |= 1 << j
        self.response[fault] = r
        self.full.setdefault(r, []).append(fault)  # @line L5
        self.pass_fail.setdefault(p, []).append(fault)  # @line L6

    def build(self, faults: Optional[Iterable[Fault]] = None) -> "FaultDictionary":
        """Add every fault of the list, by default all 2L single stuck-at faults."""
        for f in self.circuit.faults() if faults is None else faults:
            self.add_fault(f)
        return self

    def observe(self, responses: Sequence[Sequence[int]]) -> tuple[int, ...]:
        """Turn the output vectors seen on the tester (one per test) into error words."""
        if len(responses) != len(self.tests):
            raise ValueError("one response per test")
        return tuple(error_word(g, s) for g, s in zip(self.good, responses))  # @line L7

    def lookup_full(self, observed: tuple[int, ...]) -> list[Fault]:
        """Faults whose full response equals the observed error words. One hash probe."""
        return list(self.full.get(tuple(observed), []))  # @line L8

    def lookup_pass_fail(self, observed: tuple[int, ...]) -> list[Fault]:
        """Faults that fail on exactly the tests that failed on the tester."""
        p = 0
        for j, w in enumerate(observed):
            if w:
                p |= 1 << j
        return list(self.pass_fail.get(p, []))  # @line L9

    def nearest(self, observed: tuple[int, ...]) -> tuple[int, list[Fault]]:
        """Faults whose response is closest in Hamming distance to the observed one. O(|F| T)."""
        best, out = None, []
        for f, r in self.response.items():
            d = sum(bin(a ^ b).count("1") for a, b in zip(r, observed))
            if best is None or d < best:
                best, out = d, [f]
            elif d == best:
                out.append(f)
        return (0 if best is None else best), out

    def size_bits_full(self) -> int:
        return len(self.response) * len(self.tests) * self.n_outputs

    def size_bits_pass_fail(self) -> int:
        return len(self.response) * len(self.tests)

    def classes_full(self) -> int:
        return len(self.full)

    def classes_pass_fail(self) -> int:
        return len(self.pass_fail)

    def check_invariant(self) -> bool:
        """Every fault sits in exactly one class of each dictionary, under the key of its response."""
        n = len(self.response)
        if sum(map(len, self.full.values())) != n or sum(map(len, self.pass_fail.values())) != n:
            return False
        for key, fs in self.full.items():
            if not fs or any(self.response[f] != key for f in fs):
                return False
        for key, fs in self.pass_fail.items():
            for f in fs:
                if sum(1 << j for j, w in enumerate(self.response[f]) if w) != key:
                    return False
        return True
