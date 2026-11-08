# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mersenne-twister/. The authors are listed in prov/0AJ2E4.jsonl.

"""MT19937, the 32-bit Mersenne Twister of Matsumoto and Nishimura (1998), with
the 2002 initialization. Every word is masked to 32 bits."""

W, N, M, R = 32, 624, 397, 31
A = 0x9908B0DF
U, D = 11, 0xFFFFFFFF
S, B = 7, 0x9D2C5680
T, C = 15, 0xEFC60000
L = 18
F = 1812433253
MASK = 0xFFFFFFFF
UPPER = 0x80000000  # the upper w - r = 1 bit
LOWER = 0x7FFFFFFF  # the lower r = 31 bits


class MT19937:
    def __init__(self, seed: int = 5489) -> None:
        self.mt = [0] * N
        self.index = N
        self.init_genrand(seed)

    def init_genrand(self, seed: int) -> None:
        mt = self.mt
        mt[0] = seed & MASK
        for i in range(1, N):
            mt[i] = (F * (mt[i - 1] ^ (mt[i - 1] >> 30)) + i) & MASK
        self.index = N

    def init_by_array(self, key: list[int]) -> None:
        self.init_genrand(19650218)
        mt, k_len = self.mt, len(key)
        i, j = 1, 0
        for _ in range(max(N, k_len)):
            mt[i] = ((mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1664525)) + key[j] + j) & MASK
            i, j = i + 1, j + 1
            if i >= N:
                mt[0], i = mt[N - 1], 1
            if j >= k_len:
                j = 0
        for _ in range(N - 1):
            mt[i] = ((mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1566083941)) - i) & MASK
            i += 1
            if i >= N:
                mt[0], i = mt[N - 1], 1
        mt[0] = UPPER  # a nonzero state is assured
        self.index = N

    def twist(self) -> None:
        mt = self.mt
        for k in range(N):  # @line L1
            y = (mt[k] & UPPER) | (mt[(k + 1) % N] & LOWER)  # @line L2
            v = mt[(k + M) % N] ^ (y >> 1)  # @line L3
            if y & 1:  # @line L4
                v ^= A  # @line L5
            mt[k] = v  # @line L6
        self.index = 0  # @line L7

    def next_u32(self) -> int:
        if self.index >= N:  # @line L8
            self.twist()  # @line L9
        y = self.mt[self.index]  # @line L10
        self.index += 1
        y ^= (y >> U) & D  # @line L11
        y ^= (y << S) & B  # @line L12
        y ^= (y << T) & C  # @line L13
        y ^= y >> L  # @line L14
        return y & MASK  # @line L15

    def random(self) -> float:
        """genrand_res53: a multiple of 2^-53 in [0, 1), from two outputs."""
        a = self.next_u32() >> 5
        b = self.next_u32() >> 6
        return (a * 67108864 + b) / 9007199254740992.0


def temper(y: int) -> int:
    y ^= y >> U
    y ^= (y << S) & B
    y ^= (y << T) & C
    y ^= y >> L
    return y & MASK


def untemper(z: int) -> int:
    """The inverse of temper, so 624 outputs give the whole state."""
    z ^= z >> L  # L = 18 >= 16: one step inverts it
    z ^= (z << T) & C  # T = 15 and C has no bits below 17: one step
    y = z
    for _ in range(5):  # y = z ^ ((y << 7) & B), fixed point after 32 / 7 steps
        y = z ^ ((y << S) & B)
    z = y & MASK
    y = z
    for _ in range(3):  # y = z ^ (y >> 11)
        y = z ^ (y >> U)
    return y & MASK
