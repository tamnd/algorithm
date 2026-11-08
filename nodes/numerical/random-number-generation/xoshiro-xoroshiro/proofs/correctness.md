---
title: xoshiro256** has period 2^256 - 1, an exact jump of 2^128 steps and 4-dimensional equidistribution
proves: [correctness]
status: full
---

Write a state of xoshiro256 as a vector $s \in V = \mathrm{GF}(2)^{256}$, the four words side by side. Lines L2 to L6 of XOSHIRO256SS-NEXT compute $s \mapsto T s$ for a $256 \times 256$ matrix $T$ over $\mathrm{GF}(2)$: each line is a XOR of words, a shift or a rotation, and all of these are linear over $\mathrm{GF}(2)$. Let $P$ be the characteristic polynomial of $T$. Line L1 computes the output $g(s_1)$ from the old state, with $g(x) = \mathrm{rotl}(5x \bmod 2^{64}, 7) \cdot 9 \bmod 2^{64}$.

The facts marked *(computed)* are finite computations in exact integer arithmetic, carried out by the tests of the implementation.

**Lemma 1.** $T$ is invertible, and its characteristic polynomial is the degree-256 polynomial $P$ given in the reference code (the words `0x9d116f2bb0f0f001`, `0x0280002bcefd1a5e`, `0x04b4edcf26259f85`, `0x0003c03c3f3ecb19`, lowest first, plus $z^{256}$).

*Proof.* Let $b_i$ be the lowest bit of $s_0$ after $i$ steps from the state $(1, 2, 3, 4)$, for $i = 1, \ldots, 512$. *(Computed)* The Berlekamp-Massey algorithm gives linear complexity 256 for these bits and the connection polynomial whose reverse is $P$. As in Lemma 4 of the [xorshift](/xorshift/) proof, the sequence $b_i$ satisfies the recurrence of the characteristic polynomial of $T$, which has degree 256; so its minimal polynomial, $P$, divides that characteristic polynomial, and both are monic of degree 256, so they are equal. The constant coefficient of $P$ is 1, so $\det T = 1$ and $T$ is invertible. $\square$

**Lemma 2.** $P$ is primitive.

*Proof.* $2^{256} - 1 = F_0 F_1 \cdots F_7$ with $F_k = 2^{2^k} + 1$, by repeated use of $2^{2m} - 1 = (2^m - 1)(2^m + 1)$. *(Computed)* The product of the eleven numbers 3, 5, 17, 257, 65537, 641, 6700417, 274177, 67280421310721, 59649589127497217 and 5704689200685129054721 is $2^{256} - 1$, and each is prime by a Miller-Rabin test with the first 13 prime bases, which is exact below $3.3 \cdot 10^{24}$. *(Computed)* $z^{2^{256} - 1} \equiv 1 \pmod P$ and $z^{(2^{256} - 1)/q} \not\equiv 1 \pmod P$ for each of these primes $q$. By the primitivity criterion proved at the end of the [xorshift](/xorshift/) proof, $P$ is primitive. $\square$

**Theorem 1 (period).** Every non-zero state has period exactly $2^{256} - 1$, and the state 0 is fixed.

*Proof.* By Lemmas 1 and 2 and Lemma 3 of the xorshift proof, $T$ has order $2^{256} - 1$. By Lemma 2 of that proof, every non-zero state has period $2^{256} - 1$. $T 0 = 0$ because $T$ is linear. $\square$

**Theorem 2 (jump).** Let $J(z) = \sum_{i < 256} j_i z^i$ be the polynomial stored in JUMP, bit $i$ of the 256-bit constant being $j_i$. Then $J(z) = z^{2^{128}} \bmod P(z)$, and the jump function, which returns $\sum_i j_i T^i s$, returns $T^{2^{128}} s$.

*Proof.* *(Computed)* 128 successive squarings of $z$ modulo $P$ give $J$. So $z^{2^{128}} = Q(z) P(z) + J(z)$ for some polynomial $Q$. Substituting $T$ and using $P(T) = 0$ (the Cayley-Hamilton theorem) gives $T^{2^{128}} = J(T)$. The jump function keeps an accumulator $a$, and for $i = 0, \ldots, 255$ adds the current state $T^i s$ to $a$ if $j_i = 1$, then steps; so it returns $\sum_i j_i T^i s = J(T) s$. The same argument with 192 squarings proves LONG_JUMP. $\square$

**Theorem 3 (equidistribution).** Over one period, starting from any non-zero state, the 4-tuples $(r_i, r_{i+1}, r_{i+2}, r_{i+3})$ of consecutive outputs of xoshiro256** take every value in $(\{0, 1\}^{64})^4$ exactly once, except $(0, 0, 0, 0)$, which never occurs.

*Proof.* Let $\pi(s) = (s_1, (Ts)_1, (T^2 s)_1, (T^3 s)_1)$, the second word of four consecutive states, a linear map from $V$ to $\mathrm{GF}(2)^{256}$. *(Computed)* The images of the 256 unit vectors are linearly independent, so $\pi$ has rank 256 and is a bijection. The map $g$ is a bijection of 64-bit words: multiplication by an odd number modulo $2^{64}$ is invertible, and a rotation permutes the bits. So $s \mapsto (g, g, g, g) \circ \pi(s)$ is a bijection of $V$, and it sends 0 to $(0, 0, 0, 0)$ because $g(0) = 0$. By Theorem 1, one period visits each non-zero state once, and the 4-tuple of outputs starting at state $s$ is $(g, g, g, g)(\pi(s))$. So each 4-tuple other than $(0, 0, 0, 0)$ appears once. $\square$

The same proof, with the polynomial `0x095b8f76579aa001`, `0x0008828e513b43d5` of degree 128, the prime factors of $2^{128} - 1 = F_0 \cdots F_6$, and the map to two consecutive values of $s_0$, gives period $2^{128} - 1$, the exactness of the xoroshiro128 jumps by $2^{64}$ and $2^{96}$ steps, and 2-dimensional equidistribution of xoroshiro128**. $\blacksquare$
