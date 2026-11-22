# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shadow-stack/. The authors are listed in prov/5QQA10.jsonl.

"""Shadow stack on an abstract call and return trace.

The model has no real memory and no real addresses. A return address is any
hashable label, such as the string "r1". The normal stack of the program is a
Python list that a modeled memory error may overwrite. The shadow stack is a
separate object that only the operations below change, which models a shadow
stack in memory that ordinary stores of the program cannot write.
"""

from collections.abc import Hashable, Sequence


class ShadowStackFault(Exception):
    """Raised when a check fails. kind is "full", "empty", "mismatch" or "restore"."""

    def __init__(self, kind: str) -> None:
        super().__init__(kind)
        self.kind = kind


class ShadowStack:
    """A bounded stack of return addresses with a check on each return.

    Each operation takes O(1) time in the word RAM model. The space is
    capacity entries. Precondition: push is called at every call and
    check_return at every return of the protected program, in order.
    """

    def __init__(self, capacity: int = 1024) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self._s: list[Hashable] = [None] * capacity  # @line L1
        self._t = 0  # @line L1
        self._cap = capacity

    def push(self, a: Hashable) -> None:
        """Save the return address a of a call."""
        if self._t == self._cap:  # @line L2
            raise ShadowStackFault("full")
        self._s[self._t] = a  # @line L3
        self._t += 1  # @line L4

    def check_return(self, r: Hashable) -> Hashable:
        """Compare r, read from the normal stack, with the saved copy; return r if they agree."""
        if self._t == 0:  # @line L5
            raise ShadowStackFault("empty")
        self._t -= 1  # @line L6
        if self._s[self._t] != r:  # @line L7
            raise ShadowStackFault("mismatch")
        return r  # @line L8

    def restore(self, d: int) -> None:
        """Drop the entries above depth d, for a non-local exit to a frame saved at depth d."""
        if d < 0 or d > self._t:  # @line L9
            raise ShadowStackFault("restore")
        self._t = d  # @line L10

    def depth(self) -> int:
        """The number of saved return addresses."""
        return self._t

    def entries(self) -> list[Hashable]:
        """The saved return addresses, oldest first."""
        return self._s[: self._t]

    def check_invariant(self) -> None:
        """The top index stays inside the array."""
        assert 0 <= self._t <= self._cap


Event = tuple


def run_trace(
    trace: Sequence[Event], capacity: int = 1024
) -> tuple[list[Hashable], int | None, str | None]:
    """Run an abstract program trace with a shadow stack and stop at the first fault.

    Events:
      ("call", a)      push a on the normal stack and on the shadow stack
      ("ret",)         pop r from the normal stack, check it, and return to r
      ("write", k, v)  a modeled memory error sets the normal stack entry k
                       places below the top to v; the shadow stack is not touched
      ("setjmp", j)    save the current depth under the name j
      ("longjmp", j)   cut both stacks back to the depth saved under j

    Returns (targets, fault_index, fault_kind): the return targets taken before
    the run stopped, the index of the event that faulted (or None), and the kind
    of the fault (or None). Cost: O(1) per event, O(capacity) space.
    Precondition: the trace never returns from an empty normal stack, writes
    only existing entries, and jumps only to a saved name whose depth is not
    above the current depth.
    """
    normal: list[Hashable] = []
    shadow = ShadowStack(capacity)
    saved: dict[Hashable, int] = {}
    targets: list[Hashable] = []
    for i, ev in enumerate(trace):
        op = ev[0]
        try:
            if op == "call":
                normal.append(ev[1])
                shadow.push(ev[1])
            elif op == "ret":
                if not normal:
                    raise ValueError("return from an empty normal stack")
                r = normal.pop()
                targets.append(shadow.check_return(r))
            elif op == "write":
                k, v = ev[1], ev[2]
                if not 0 <= k < len(normal):
                    raise ValueError("write outside the normal stack")
                normal[len(normal) - 1 - k] = v
            elif op == "setjmp":
                saved[ev[1]] = len(normal)
            elif op == "longjmp":
                d = saved[ev[1]]
                if d > len(normal):
                    raise ValueError("jump to a frame that has returned")
                del normal[d:]
                shadow.restore(d)
            else:
                raise ValueError(f"unknown event {op!r}")
        except ShadowStackFault as f:
            return targets, i, f.kind
    return targets, None, None
