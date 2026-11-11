---
title: The additive checksum computes the sum mod 2^k and misses exactly the errors whose changes sum to a multiple of 2^k
proves: [correctness]
status: full
---

Let the message be the words $x_1, \ldots, x_m$, each in $[0, 2^k)$, after the zero padding of line L3. Write $S = (x_1 + \cdots + x_m) \bmod 2^k$.

**Lemma 1 (the loop).** Line L5 returns $S$.

*Proof.* We show the invariant: at the test of line L2 for index $i$, $s = (x_1 + \cdots + x_{i-1}) \bmod 2^k$. Before the first test, $i = 1$ and line L1 sets $s = 0$, the empty sum. If the invariant holds for $i$, line L4 sets $s$ to $((x_1 + \cdots + x_{i-1}) \bmod 2^k + x_i) \bmod 2^k = (x_1 + \cdots + x_i) \bmod 2^k$, because reduction mod $2^k$ commutes with addition. So it holds for $i + 1$. The loop ends with $i = m + 1$, and line L5 returns $S$. $\square$

**Lemma 2 (the check word).** Let $c = (-S) \bmod 2^k$. The checksum of $x_1, \ldots, x_m, c$ is 0.

*Proof.* By Lemma 1 it is $(S + c) \bmod 2^k = (S - S) \bmod 2^k = 0$. $\square$

**Theorem (exact detection rule).** Let the received words be $y_1, \ldots, y_m$ with $y_i = x_i + \delta_i$, so that $-2^k < \delta_i < 2^k$. The checksum of $y$ equals the checksum of $x$ if and only if $\sum_i \delta_i \equiv 0 \pmod{2^k}$.

*Proof.* By Lemma 1, the two checksums are $\sum x_i \bmod 2^k$ and $(\sum x_i + \sum \delta_i) \bmod 2^k$. Two integers have the same residue mod $2^k$ if and only if their difference $\sum \delta_i$ is a multiple of $2^k$. The same holds when the receiver checks $y$ followed by a received check word, by Lemma 2. $\square$

**Corollary 1 (single errors).** If exactly one word changes, the error is detected.

*Proof.* Then $\sum \delta_i = \delta_j$ for one $j$, with $0 < |\delta_j| < 2^k$. No nonzero integer of absolute value below $2^k$ is a multiple of $2^k$. $\square$

**Corollary 2 (permutations).** If $y$ is any permutation of $x$, the error is missed.

*Proof.* A permutation does not change the multiset of the words, so $\sum y_i = \sum x_i$ and $\sum \delta_i = 0$. $\square$

**Corollary 3 (byte swaps in 16-bit words).** Let $k = 16$, and swap two bytes $a \ne b$ of the message. If both bytes are high bytes of their words, or both are low bytes, the error is missed. If one is a high byte and the other a low byte, the error is detected.

*Proof.* A high byte $a$ contributes $256a$ to the sum, and a low byte contributes $a$. In the first case the swap moves $256a$ and $256b$ (or $a$ and $b$) between two words, so $\sum \delta_i = 0$. In the second case, with $a$ high and $b$ low before the swap, the change is $256b + a - 256a - b = 255(b - a)$. Since $0 < |b - a| \le 255$, the value $255(b - a)$ is nonzero, of absolute value below $2^{16}$, and so not a multiple of $2^{16}$. $\square$

**Corollary 4 (two top-bit flips).** With $k = 8$, flipping the top bit of two bytes is always missed.

*Proof.* Each flip changes its byte by $+128$ or $-128$. The total change is $0$ or $\pm 256$, a multiple of $2^8$ in each case. $\square$

**Cost.** Line L4 runs once per word, and each run is one addition and one reduction, which is free on a $k$-bit register. So the time is $\Theta(m)$ and the extra space is one register. $\blacksquare$
