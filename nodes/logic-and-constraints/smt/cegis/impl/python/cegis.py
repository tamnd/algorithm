# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cegis/. The authors are listed in prov/P1YF3Y.jsonl.

"""Counterexample-guided inductive synthesis (CEGIS) over finite spaces.

A synthesis problem has a finite list of candidate programs, a finite list of
inputs, a function run(c, x) that runs candidate c on input x, and a
specification spec(x, y) that says whether output y is correct for input x.
The goal is a candidate c with spec(x, run(c, x)) for every input x.

The two oracles of CEGIS are explicit functions here:

* synthesize(examples) returns the first candidate, in the given order, that
  is correct on every example, or None. In a real tool this is an SMT or SAT
  call on the formula "exists c. AND over examples of spec".
* verify(c) returns the first input on which c is wrong, or None. In a real
  tool this is an SMT call on "exists x. not spec(x, run(c, x))".

Both oracles may be replaced by the caller, for example by a solver.
"""

from typing import Callable, Hashable, Iterable, List, NamedTuple, Optional, Sequence


class Result(NamedTuple):
    program: Optional[Hashable]  # a correct candidate, or None if none exists
    examples: List[Hashable]  # the counterexamples, in the order found
    rounds: int  # number of synthesizer calls
    trace: List[tuple]  # (candidate, counterexample or None) per round


def first_consistent(candidates: Sequence, run: Callable, spec: Callable, examples: Iterable) -> Optional[Hashable]:
    """Synthesizer oracle: the first candidate that is correct on all examples."""
    examples = list(examples)
    for c in candidates:
        if all(spec(x, run(c, x)) for x in examples):
            return c
    return None


def first_counterexample(inputs: Sequence, run: Callable, spec: Callable, c: Hashable) -> Optional[Hashable]:
    """Verifier oracle: the first input on which candidate c is wrong."""
    for x in inputs:
        if not spec(x, run(c, x)):
            return x
    return None


def cegis(candidates: Sequence, inputs: Sequence, run: Callable, spec: Callable,
          initial: Iterable = (), synthesize: Optional[Callable] = None,
          verify: Optional[Callable] = None, max_rounds: Optional[int] = None) -> Result:
    """Run the CEGIS loop. Return a correct candidate, or None if none exists.

    With the default oracles and finite lists, the loop stops after at most
    min(len(candidates), len(inputs)) + 1 rounds.
    """
    if synthesize is None:
        def synthesize(ex):
            return first_consistent(candidates, run, spec, ex)
    if verify is None:
        def verify(c):
            return first_counterexample(inputs, run, spec, c)
    examples = list(initial)  # @line L1
    trace = []
    rounds = 0
    while max_rounds is None or rounds < max_rounds:  # @line L2
        rounds += 1
        c = synthesize(examples)  # @line L3
        if c is None:  # @line L4
            trace.append((None, None))
            return Result(None, examples, rounds, trace)
        x = verify(c)  # @line L5
        trace.append((c, x))
        if x is None:  # @line L6
            return Result(c, examples, rounds, trace)
        examples.append(x)  # @line L7
    raise RuntimeError("round limit reached")


def sketch_round_up(h: tuple, x: int) -> int:
    """The sketch (x + h1) & h2 on 4-bit unsigned values."""
    h1, h2 = h
    return ((x + h1) & h2) & 15


def round_up_spec(x: int, y: int) -> bool:
    """y is x rounded up to a multiple of 4, modulo 16."""
    return y == (-(-x // 4) * 4) % 16


def page_example() -> Result:
    holes = [(h1, h2) for h1 in range(16) for h2 in range(16)]
    return cegis(holes, list(range(16)), sketch_round_up, round_up_spec)


if __name__ == "__main__":
    r = page_example()
    for c, x in r.trace:
        print(c, x)
    print("program", r.program, "rounds", r.rounds)
