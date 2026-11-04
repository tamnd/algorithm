# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hire-assistant/. The authors are listed in prov/9RHJGA.jsonl.

import random
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def hire_assistant(candidates: list[T]) -> list[int]:
    """Return the 0-based positions of the hires, in order.

    A candidate is hired when it is strictly better than every earlier
    candidate. The last position in the result is the position of the best
    candidate (the first one, if several are equal and best).
    """
    hires: list[int] = []
    best = -1  # @line L1
    for i in range(len(candidates)):  # @line L2
        c = candidates[i]  # @line L3
        if best < 0 or candidates[best] < c:  # @line L4
            best = i  # @line L5
            hires.append(i)  # @line L6
    return hires


def randomized_hire_assistant(
    candidates: list[T], rng: random.Random | None = None
) -> list[T]:
    """Shuffle the candidates, run hire_assistant, and return the hired candidates in order."""
    rng = rng if rng is not None else random.Random()
    order = list(candidates)
    rng.shuffle(order)
    return [order[i] for i in hire_assistant(order)]
