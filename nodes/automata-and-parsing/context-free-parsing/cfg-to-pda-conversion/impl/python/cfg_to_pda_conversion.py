# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cfg-to-pda-conversion/. The authors are listed in prov/X117M6.jsonl.

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

Production = tuple[str, tuple[str, ...]]
EPS = ""  # the input label of a move that reads nothing


@dataclass
class PDA:
    """A pushdown automaton.

    moves[(state, a, X)] lists the pairs (new state, pushed string) for the move that reads a
    (EPS for none) with X on top. The pushed string is a tuple whose first symbol becomes the top.
    The machine accepts by empty stack if final_states is None, and by final state otherwise.
    """

    states: set[str]
    input_alphabet: set[str]
    stack_alphabet: set[str]
    moves: dict[tuple[str, str, str], list[tuple[str, tuple[str, ...]]]] = field(default_factory=dict)
    start_state: str = "q"
    start_symbol: str = "S"
    final_states: set[str] | None = None

    def add(self, state: str, a: str, top: str, new_state: str, push: Sequence[str]) -> None:
        entry = self.moves.setdefault((state, a, top), [])
        if (new_state, tuple(push)) not in entry:
            entry.append((new_state, tuple(push)))

    def number_of_moves(self) -> int:
        return sum(len(v) for v in self.moves.values())


def cfg_to_pda(start: str, productions: Iterable[Production], terminals: Iterable[str]) -> PDA:
    """Build the one-state PDA that accepts L(G) by empty stack.

    Its runs are the leftmost derivations of G: an expand move replaces a nonterminal on top
    of the stack by a right side, and a match move pops a terminal that equals the next input.
    """
    productions = list(productions)
    terminals = set(terminals)
    nonterminals = {a for a, _ in productions} | {start}
    if nonterminals & terminals:
        raise ValueError("a symbol is both a terminal and a nonterminal")
    pda = PDA(  # @line L1
        states={"q"},
        input_alphabet=set(terminals),
        stack_alphabet=nonterminals | terminals,
        start_state="q",
        start_symbol=start,
    )
    for a, rhs in productions:  # @line L2
        pda.add("q", EPS, a, "q", rhs)  # @line L3
    for t in sorted(terminals):  # @line L4
        pda.add("q", t, t, "q", ())  # @line L5
    return pda  # @line L6


def cfg_to_pda_final_state(
    start: str, productions: Iterable[Production], terminals: Iterable[str], bottom: str = "⊥"
) -> PDA:
    """Build a PDA that accepts L(G) by final state, with a bottom marker below S."""
    pda = cfg_to_pda(start, productions, terminals)
    if bottom in pda.stack_alphabet:
        raise ValueError("the bottom marker is a symbol of the grammar")
    pda.states |= {"s", "f"}  # @line L7
    pda.stack_alphabet.add(bottom)
    pda.add("s", EPS, bottom, "q", (start, bottom))  # @line L8
    pda.add("q", EPS, bottom, "f", (bottom,))  # @line L9
    pda.start_state, pda.start_symbol, pda.final_states = "s", bottom, {"f"}  # @line L10
    return pda


def leftmost_run(
    pda: PDA, derivation: Sequence[Production], w: Sequence[str]
) -> list[tuple[str, int, tuple[str, ...]]]:
    """Turn a leftmost derivation of w into the run of the one-state PDA that accepts w.

    Returns the configurations (state, input position, stack with the top first). Raises
    ValueError if the derivation is not a leftmost derivation of w for this machine.
    """
    state, pos, stack = pda.start_state, 0, (pda.start_symbol,)
    run = [(state, pos, stack)]
    steps = iter(derivation)
    while stack:
        top = stack[0]
        if top in pda.input_alphabet:
            if pos >= len(w) or w[pos] != top:
                raise ValueError("the derivation does not derive w")
            state, nxt = pda.moves[(state, top, top)][0]
            pos, stack = pos + 1, nxt + stack[1:]
        else:
            step = next(steps, None)
            if step is None or step[0] != top:
                raise ValueError("not a leftmost derivation")
            if (state, step[1]) not in pda.moves.get((state, EPS, top), []):
                raise ValueError("not a production of the grammar")
            stack = step[1] + stack[1:]
        run.append((state, pos, stack))
    if pos != len(w) or next(steps, None) is not None:
        raise ValueError("the derivation does not derive w")
    return run
