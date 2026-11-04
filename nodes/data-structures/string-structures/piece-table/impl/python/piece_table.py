# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/piece-table/. The authors are listed in prov/A8HMV8.jsonl.

"""Piece table: a text kept as a list of pieces into two buffers.

The original buffer is the text at load time and is never changed. The add
buffer only grows: every inserted character is appended to it once. The text
is the concatenation of the pieces in order; a piece (buf, start, length) names
buffer[buf][start : start + length]. This is the list form, in which locating
a position scans the pieces, in O(P) time for P pieces.
"""

ORIGINAL = 0
ADD = 1


class PieceTable:
    """Editable text stored as pieces over an immutable original and an append-only add buffer."""

    def __init__(self, original: str = "") -> None:
        self.original = original
        self.add: list[str] = []
        self.pieces: list[tuple[int, int, int]] = [(ORIGINAL, 0, len(original))] if original else []
        self.n = len(original)

    def __len__(self) -> int:
        return self.n

    def _buffer_slice(self, buf: int, start: int, length: int) -> str:
        if buf == ORIGINAL:
            return self.original[start : start + length]
        return "".join(self.add[start : start + length])

    def _find(self, i: int) -> tuple[int, int]:
        """Return (k, off): position i is offset off in piece k; i == n gives (P, 0)."""
        off = i  # @line L1
        for k, (_, _, length) in enumerate(self.pieces):  # @line L2
            if off < length:  # @line L3
                return k, off
            off -= length  # @line L4
        return len(self.pieces), 0  # @line L5

    def insert(self, i: int, s: str) -> None:
        """Insert s so that it starts at position i (0 <= i <= len)."""
        if not 0 <= i <= self.n:
            raise IndexError("insert position out of range")
        if not s:  # @line L6
            return
        a = len(self.add)  # @line L7
        self.add.extend(s)
        k, off = self._find(i)  # @line L8
        if off == 0 and k > 0:  # @line L9
            b, st, ln = self.pieces[k - 1]
            if b == ADD and st + ln == a:
                self.pieces[k - 1] = (b, st, ln + len(s))
                self.n += len(s)
                return
        if off == 0:  # @line L10
            self.pieces.insert(k, (ADD, a, len(s)))
        else:  # @line L11
            b, st, ln = self.pieces[k]
            self.pieces[k : k + 1] = [(b, st, off), (ADD, a, len(s)), (b, st + off, ln - off)]
        self.n += len(s)

    def delete(self, i: int, d: int) -> None:
        """Delete the d characters at positions i .. i + d - 1."""
        if d < 0 or not 0 <= i <= self.n - d:
            raise IndexError("delete range out of range")
        self.n -= d  # @line L12
        k, off = self._find(i)  # @line L13
        while d > 0:  # @line L14
            b, st, ln = self.pieces[k]  # @line L15
            take = min(d, ln - off)
            if off == 0 and take == ln:  # @line L16
                del self.pieces[k]
            elif off == 0:  # @line L17
                self.pieces[k] = (b, st + take, ln - take)
                k += 1
            elif off + take == ln:  # @line L18
                self.pieces[k] = (b, st, off)
                k += 1
            else:  # @line L19
                self.pieces[k : k + 1] = [(b, st, off), (b, st + off + take, ln - off - take)]
                k += 1
            d -= take  # @line L20
            off = 0

    def char_at(self, i: int) -> str:
        """Return the character at position i."""
        if not 0 <= i < self.n:
            raise IndexError("position out of range")
        k, off = self._find(i)  # @line L21
        b, st, _ = self.pieces[k]  # @line L22
        return self.original[st + off] if b == ORIGINAL else self.add[st + off]

    def substring(self, i: int, j: int) -> str:
        """Return the text at positions i .. j - 1."""
        if not 0 <= i <= j <= self.n:
            raise IndexError("range out of range")
        out: list[str] = []
        k, off = self._find(i)
        need = j - i
        while need > 0:
            b, st, ln = self.pieces[k]
            take = min(need, ln - off)
            out.append(self._buffer_slice(b, st + off, take))
            need -= take
            k, off = k + 1, 0
        return "".join(out)

    def text(self) -> str:
        return "".join(self._buffer_slice(b, st, ln) for b, st, ln in self.pieces)

    def check_invariant(self) -> None:
        total = 0
        for b, st, ln in self.pieces:
            assert b in (ORIGINAL, ADD)
            size = len(self.original) if b == ORIGINAL else len(self.add)
            assert ln > 0 and 0 <= st and st + ln <= size, "piece out of its buffer"
            total += ln
        assert total == self.n
