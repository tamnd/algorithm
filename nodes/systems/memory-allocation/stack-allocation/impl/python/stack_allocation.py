# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stack-allocation/. The authors are listed in prov/2NC7TG.jsonl.

"""Stack allocation over the range [base, limit).

Blocks are allocated by a bump of top and freed in last-in-first-out order.
The allocator keeps an explicit stack of the block starts, so free(p) checks
that p is the most recent live block and raises an error otherwise. mark()
saves top and the block count; release(m) frees every block made after the
mark at once.
enter() and leave() build call frames from marks; alloca(n) allocates in the
current frame, and leave() frees the frame with everything in it.
"""


class StackOrderError(Exception):
    """A free that does not follow last-in-first-out order."""


class StackAllocator:
    def __init__(self, base: int, limit: int) -> None:
        if not 0 <= base <= limit:
            raise ValueError("need 0 <= base <= limit")
        self.base, self.limit, self.top = base, limit, base
        self.blocks: list[int] = []  # starts of the live blocks, oldest first
        self.frames: list[tuple[int, int]] = []  # marks of the open frames

    def alloc(self, n: int) -> int | None:
        if n < 0:
            raise ValueError("n must be at least 0")
        if self.top + n > self.limit:  # @line L1
            return None
        p = self.top  # @line L2
        self.blocks.append(p)
        self.top = p + n
        return p

    def free(self, p: int) -> None:
        if not self.blocks or self.blocks[-1] != p:  # @line L3
            raise StackOrderError(f"{p} is not the last live block")
        self.blocks.pop()  # @line L4
        self.top = p

    def mark(self) -> tuple[int, int]:
        """Save top and the number of live blocks."""
        return self.top, len(self.blocks)  # @line L5

    def release(self, m: tuple[int, int]) -> None:
        """Free every block made after the mark m."""
        top, k = m
        if k > len(self.blocks) or top != (self.blocks[k] if k < len(self.blocks) else self.top):
            raise StackOrderError("the mark is no longer valid")
        del self.blocks[k:]  # @line L6
        self.top = top

    # Call frames, as a compiler lays them out.
    def enter(self, frame_size: int) -> int | None:
        """Open a frame with frame_size bytes of fixed locals; return its address."""
        self.frames.append(self.mark())
        p = self.alloc(frame_size)
        if p is None:
            self.frames.pop()
        return p

    def alloca(self, n: int) -> int | None:
        """Allocate n bytes that live until the current frame is left."""
        if not self.frames:
            raise StackOrderError("alloca outside a frame")
        return self.alloc(n)

    def leave(self) -> None:
        self.release(self.frames.pop())
