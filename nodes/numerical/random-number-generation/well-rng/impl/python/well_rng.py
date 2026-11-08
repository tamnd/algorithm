# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/well-rng/. The authors are listed in prov/RZPYG3.jsonl.

MASK32 = 0xFFFFFFFF
R = 16  # state words, 512 bits
FACT = 2.32830643653869628906e-10  # 2^-32


def _t0(t: int, v: int) -> int:
    """The WELL matrix M3(-t): v xor (v << t), within 32 bits."""
    return (v ^ (v << t)) & MASK32


def well512a_next(state: list[int], i: int) -> tuple[int, int]:
    """One step of WELL512a (Panneton, L'Ecuyer, Matsumoto 2006).

    state holds 16 words of 32 bits as a circular buffer, i is the index of v_(n,0).
    Returns (output word, new index); state is updated in place.
    """
    z0 = state[(i + 15) & 15]  # @line L1
    z1 = _t0(16, state[i]) ^ _t0(15, state[(i + 13) & 15])  # @line L2
    v = state[(i + 9) & 15]
    z2 = v ^ (v >> 11)  # @line L3
    state[i] = new1 = z1 ^ z2  # @line L4
    state[(i + 15) & 15] = (  # @line L5
        _t0(2, z0) ^ _t0(18, z1) ^ ((z2 << 28) & MASK32) ^ (new1 ^ ((new1 << 5) & 0xDA442D24))
    )
    i = (i + 15) & 15  # @line L6
    return state[i], i  # @line L7


class Well512a:
    def __init__(self, seed_words: list[int]) -> None:
        if len(seed_words) != R or not all(0 <= w <= MASK32 for w in seed_words):
            raise ValueError("WELL512a needs 16 words of 32 bits")
        if not any(seed_words):
            raise ValueError("the all-zero state is a fixed point")
        self.state, self.i = list(seed_words), 0

    def next_u32(self) -> int:
        out, self.i = well512a_next(self.state, self.i)
        return out

    def next_double(self) -> float:
        """The reference output: the word times 2^-32, in [0, 1)."""
        return self.next_u32() * FACT
