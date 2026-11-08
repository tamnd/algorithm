---
title: For each key, Threefry is a bijection of the counter space, so counter mode never repeats a block before the counter wraps
proves: [correctness]
status: full
---

Let $w$ be the word size and do all additions and subtractions modulo $2^w$. Write $\mathrm{rotl}_d$ for rotation of a $w$-bit word left by $d$ positions, $0 < d < w$. Threefry$n$x$w$ with key $K = (k_0, \ldots, k_{n-1})$ uses the extended key $k_n = C \oplus k_0 \oplus \cdots \oplus k_{n-1}$ for a fixed constant $C$ (line L1). Starting from the counter $X = (x_0, \ldots, x_{n-1})$ it computes:

- the initial injection $x_i \leftarrow x_i + k_i$ (line L2);
- for $r = 0, \ldots, R - 1$, the round $r$: for each pair $(a, b)$ of the round (one pair for $n = 2$, two disjoint pairs for $n = 4$), the MIX step $x_a \leftarrow x_a + x_b$, then $x_b \leftarrow \mathrm{rotl}_{d}(x_b) \oplus x_a$ with the rotation $d$ of the round (line L4);
- after every round $r$ with $r \equiv 3 \pmod 4$, the injection with $s = (r + 1)/4$: $x_i \leftarrow x_i + k_{(s + i) \bmod (n+1)}$ for all $i$, and then $x_{n-1} \leftarrow x_{n-1} + s$ (lines L5 and L6).

The output is the final $X$ (line L7). We write $\Theta_K$ for the resulting map on $\mathbb{Z}_{2^w}^n$.

**Lemma 1 (MIX is invertible).** For every rotation $d$, the map $(a, b) \mapsto (a + b,\ \mathrm{rotl}_d(b) \oplus (a + b))$ is a bijection of $\mathbb{Z}_{2^w}^2$, with inverse $(y_a, y_b) \mapsto (y_a - b,\ b)$ where $b = \mathrm{rotl}_{w - d}(y_b \oplus y_a)$.

*Proof.* Let $y_a = a + b$ and $y_b = \mathrm{rotl}_d(b) \oplus y_a$. XOR is its own inverse, so $y_b \oplus y_a = \mathrm{rotl}_d(b)$, and rotation left by $w - d$ undoes rotation left by $d$, so $b = \mathrm{rotl}_{w-d}(y_b \oplus y_a)$. Then $a = y_a - b$. Each output therefore has exactly one preimage, given by the formula, and the map is a bijection of a finite set. $\square$

**Lemma 2 (injection is invertible).** For fixed $s$ and key, the injection $x_i \mapsto x_i + k_{(s+i) \bmod (n+1)}$ (plus $s$ on the last word) is a bijection, inverted by subtracting the same values.

*Proof.* Addition of a constant modulo $2^w$ is a bijection of $\mathbb{Z}_{2^w}$ with inverse the subtraction of that constant; the injection acts on each word separately. $\square$

**Theorem 1.** For every key $K$, every number of rounds $R$ and every choice of rotations, $\Theta_K$ is a permutation of $\mathbb{Z}_{2^w}^n$. Consequently, in counter mode, the blocks $\Theta_K(i)$ for the counters $i = 0, 1, \ldots, 2^{n w} - 1$ are pairwise distinct; the stream of blocks has period exactly $2^{nw}$ in the counter ($2^{128}$ blocks for Threefry2x64 and Threefry4x32, $2^{256}$ for Threefry4x64), and each block can be computed from its index alone.

*Proof.* Within a round with two pairs, the pairs $(0, 1), (2, 3)$ or $(0, 3), (2, 1)$ are disjoint, so the round applies a bijection to each pair independently and is a bijection of $\mathbb{Z}_{2^w}^4$ (Lemma 1). The extended key and the injection constants depend only on $K$, $r$ and $s$, never on the counter, so every injection is a fixed bijection (Lemma 2). $\Theta_K$ is a composition of these bijections, hence a bijection, and its inverse applies the inverses in reverse order. Distinct counters therefore give distinct blocks, and the counter, incremented modulo $2^{nw}$, returns to its start after exactly $2^{nw}$ steps. $\square$

The tests check the inverse on Random123's 36 known-answer vectors and on random inputs for all four sizes, and check the bijection exhaustively for toy versions with 16-bit counters.

The theorem says nothing about how random the outputs look: a plain counter is also a bijection. That 20 rounds of Threefry produce outputs that pass statistical tests, and that 13 rounds are enough for the TestU01 batteries in the authors' experiments, are empirical claims; the avalanche measurements in the tests support them but prove nothing. Threefry also inherits no proven security from the Threefish cipher, since it drops the tweak and, in the 32-bit and 2-word variants, changes the rotations. $\blacksquare$
