---
title: For each key, Philox is a bijection of the counter space, so counter mode never repeats a block before the counter wraps
proves: [correctness]
status: full
---

Let $w$ be the word size and $\mathbb{Z}_{2^w} = \{0, \ldots, 2^w - 1\}$ with arithmetic modulo $2^w$. For a word $x$ and a multiplier $M$, write $M x = \mathrm{hi}(M, x)\, 2^w + \mathrm{lo}(M, x)$ for the full product of $2w$ bits, so $\mathrm{lo}(M, x) = M x \bmod 2^w$. Philox4x$w$ with multipliers $M_0, M_1$ applies to a counter $X = (x_0, x_1, x_2, x_3)$ and a round key $(k_0, k_1)$ the round

$$\rho_{k}(x_0, x_1, x_2, x_3) = \bigl(\mathrm{hi}(M_1, x_2) \oplus x_1 \oplus k_0,\ \mathrm{lo}(M_1, x_2),\ \mathrm{hi}(M_0, x_0) \oplus x_3 \oplus k_1,\ \mathrm{lo}(M_0, x_0)\bigr)$$

(lines L2 to L4). The round keys are $K^{(r)} = (k_0 + r W_0, k_1 + r W_1) \bmod 2^w$ for $r = 0, \ldots, R - 1$ (line L5), and the output is $\Phi_K(X) = \rho_{K^{(R-1)}} \circ \cdots \circ \rho_{K^{(0)}}(X)$. Philox2x$w$ is the same with two words: $\rho_k(x_0, x_1) = (\mathrm{hi}(M, x_0) \oplus x_1 \oplus k,\ \mathrm{lo}(M, x_0))$.

**Lemma 1.** If $M$ is odd, then $x \mapsto \mathrm{lo}(M, x)$ is a bijection of $\mathbb{Z}_{2^w}$, with inverse $y \mapsto M^{-1} y \bmod 2^w$.

*Proof.* An odd $M$ is coprime to $2^w$, so it has an inverse modulo $2^w$, and $M^{-1} (M x) \equiv x$. $\square$

**Theorem 1 (each round is invertible).** If $M_0$ and $M_1$ are odd, then for every round key $k$, $\rho_k$ is a bijection of $\mathbb{Z}_{2^w}^4$, and its inverse is

$$\rho_k^{-1}(y_0, y_1, y_2, y_3) = \bigl(x_0,\ y_0 \oplus \mathrm{hi}(M_1, x_2) \oplus k_0,\ x_2,\ y_2 \oplus \mathrm{hi}(M_0, x_0) \oplus k_1\bigr), \quad x_0 = M_0^{-1} y_3,\ x_2 = M_1^{-1} y_1.$$

The same holds for the two-word round with an odd $M$.

*Proof.* Let $(y_0, y_1, y_2, y_3) = \rho_k(x_0, x_1, x_2, x_3)$. Then $y_3 = \mathrm{lo}(M_0, x_0)$, so $x_0 = M_0^{-1} y_3$ by Lemma 1; likewise $x_2 = M_1^{-1} y_1$. Knowing $x_0$ and $x_2$, we know $\mathrm{hi}(M_0, x_0)$ and $\mathrm{hi}(M_1, x_2)$, and since XOR is its own inverse, $x_1 = y_0 \oplus \mathrm{hi}(M_1, x_2) \oplus k_0$ and $x_3 = y_2 \oplus \mathrm{hi}(M_0, x_0) \oplus k_1$. So every output has exactly one preimage, given by the formula, and $\rho_k$ is a bijection of the finite set. For two words, $x_0 = M^{-1} y_1$ and $x_1 = y_0 \oplus \mathrm{hi}(M, x_0) \oplus k$. $\square$

**Corollary 1 (counter mode).** For a fixed key $K$, $\Phi_K$ is a permutation of $\mathbb{Z}_{2^w}^4$ (or $\mathbb{Z}_{2^w}^2$). Hence the blocks $\Phi_K(i)$ for the counters $i = 0, 1, \ldots, 2^{4w} - 1$, read as $4w$-bit integers, are pairwise distinct: the stream of blocks has period exactly $2^{4w}$ in the counter, $2^{128}$ blocks for Philox4x32, and no block repeats within a period. Each block can be computed directly from its index, in $R$ rounds, without computing the blocks before it.

*Proof.* A composition of bijections is a bijection, and the round keys depend only on $K$ and $r$, not on the counter. Distinct counters therefore give distinct outputs. The counter returns to its start after exactly $2^{4w}$ increments modulo $2^{4w}$. $\square$

All multipliers of Random123 are odd (their last hexadecimal digit is 3 or 7), so the corollary applies to Philox2x32, Philox4x32, Philox2x64 and Philox4x64 for every number of rounds. The tests check the inverse formula on the published known-answer vectors and on random inputs, and check the bijection exhaustively on toy versions with 16-bit counters.

What the proof does not give is randomness: bijectivity says that the outputs never repeat within a period, which is also true of a counter alone. That the outputs of Philox4x32-10 look independent and uniform is an empirical claim, supported by the authors' runs of the TestU01 batteries and by the avalanche measurements in the tests, not a theorem. $\blacksquare$
