---
title: SplitMix64 has period 2^64 and outputs every 64-bit word once per period
proves: [correctness]
status: full
---

Let $N = 2^{64}$ and let all arithmetic be modulo $N$ on words in $\{0, 1, \ldots, N - 1\}$. Let $\gamma$ be odd, and let $g$ be the mixer of lines L3 to L5,

$$g = \sigma_{31} \circ \mu_{M_2} \circ \sigma_{27} \circ \mu_{M_1} \circ \sigma_{30},$$

where $\sigma_s(z) = z \oplus (z \gg s)$ and $\mu_M(z) = M z \bmod N$, with $M_1$ and $M_2$ odd.

**Lemma 1.** For $1 \le s < 64$, $\sigma_s$ is a bijection of 64-bit words. Its inverse maps $y$ to the fixed point of $t \mapsto y \oplus (t \gg s)$, which is reached after at most $\lceil 64 / s \rceil$ iterations from $t = y$.

*Proof.* Let $y = \sigma_s(z)$. Bits $63$ down to $64 - s$ of $y$ equal those of $z$, because $z \gg s$ has zeros there. For a lower bit $j$, $y_j = z_j \oplus z_{j + s}$, so $z_j = y_j \oplus z_{j+s}$, which determines $z_j$ from a bit of $z$ that is $s$ places higher. By induction from the top, $y$ determines $z$, so $\sigma_s$ is injective, and an injective map of a finite set to itself is a bijection. The iteration $t \leftarrow y \oplus (t \gg s)$ makes the top $k s$ bits of $t$ correct after $k$ rounds, by the same induction, so $\lceil 64/s \rceil$ rounds suffice. $\square$

**Lemma 2.** For odd $M$, $\mu_M$ is a bijection of $\mathbb{Z}_N$.

*Proof.* $\gcd(M, N) = 1$ because $N$ is a power of 2 and $M$ is odd. By Bézout's identity there are integers $u, v$ with $u M + v N = 1$, so $u M \equiv 1 \pmod N$, and $\mu_u$ is the inverse of $\mu_M$. $\square$

**Lemma 3.** The sequence $x_i = x_0 + i \gamma \bmod N$ of line L1 satisfies $x_i = x_j$ if and only if $i \equiv j \pmod N$. So its period is exactly $N$, and $\{x_1, \ldots, x_N\} = \mathbb{Z}_N$.

*Proof.* By induction on $i$, line L1 gives $x_i = x_0 + i \gamma \bmod N$. Then $x_i = x_j$ if and only if $N \mid (i - j) \gamma$. Since $\gamma$ is odd, $\gcd(\gamma, N) = 1$, and $N \mid (i - j)\gamma$ if and only if $N \mid i - j$. Hence $x_1, \ldots, x_N$ are $N$ distinct elements of a set of size $N$, which is all of it, and $x_{i + N} = x_i$ while no smaller positive shift works. $\square$

**Theorem.** For every seed $x_0$ and every odd $\gamma$, the outputs $z_i = g(x_i)$ of SPLITMIX64-NEXT satisfy $z_{i + N} = z_i$ for all $i$, and $\{z_1, \ldots, z_N\}$ is the set of all $N$ words, each taken once. In particular, the state sequence has period exactly $N$, and no output value repeats within $N$ consecutive calls.

*Proof.* By Lemmas 1 and 2, $g$ is a composition of five bijections, hence a bijection. By Lemma 3, $x_1, \ldots, x_N$ run through all words once, so their images $z_1, \ldots, z_N$ run through all words once. Since $x_{i+N} = x_i$, also $z_{i+N} = z_i$. The state sequence has period exactly $N$ by Lemma 3. $\blacksquare$
