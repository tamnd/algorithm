---
title: pcg32 has period 2^64 and each 32-bit output appears 2^32 times per period
proves: [correctness]
status: full
---

Let $N = 2^{64}$, $a = 6364136223846793005$ and let $c$ be odd. Line L2 computes $f(x) = (a x + c) \bmod N$, and lines L3 to L5 output $g(x) = \mathrm{rotr}_{32}(h(x), x \gg 59)$ with $h(x) = \lfloor (x \oplus (x \gg 18)) / 2^{27} \rfloor \bmod 2^{32}$, where $x$ is the old state. Write $x_j$ for bit $j$ of $x$.

**Lemma 1 (full period).** For every start state, the sequence $x_{i+1} = f(x_i)$ has period exactly $N$, and it visits every element of $\mathbb{Z}_N$ once per period.

*Proof.* This is the case $m = 2^{64}$ of the Hull-Dobell theorem; here is a direct proof. Let $S_k = 1 + a + \cdots + a^{k-1}$. By induction on $k$, $f^k(x) = a^k x + c S_k \bmod N$, and $a^k - 1 = (a - 1) S_k$. Hence

$$f^k(x) - x = (a^k - 1) x + c S_k = S_k \big( (a - 1) x + c \big).$$

The factor $(a - 1) x + c$ is odd, because $a - 1$ is even and $c$ is odd. So $f^k(x) \equiv x \pmod N$ if and only if $2^{64} \mid S_k$.

We show that the power of 2 in $S_k$ equals the power of 2 in $k$. Since $a \bmod 8 = 5$, $a \equiv 1 \pmod 4$, so $a^m \equiv 1 \pmod 4$ and $1 + a^m \equiv 2 \pmod 4$ for all $m$. From $S_{2m} = S_m (1 + a^m)$, the power of 2 in $S_{2m}$ is one more than in $S_m$. For odd $k$, $S_k$ is a sum of $k$ odd numbers, so it is odd. By induction on the power of 2 in $k$, the claim follows.

So $f^k(x) = x$ if and only if $2^{64} \mid k$: every state has period exactly $N$. A cycle of length $N$ in a set of $N$ states contains all of them. $\square$

**Lemma 2.** Fix $\tau \in \{0, \ldots, 31\}$ and let $X_\tau$ be the set of states whose top five bits $x_{63} \ldots x_{59}$ encode $\tau$. The map $x \mapsto h(x)$ from $X_\tau$ to $\{0, 1\}^{32}$ takes every value exactly $2^{27}$ times.

*Proof.* Bit $k$ of $h(x)$, for $0 \le k \le 31$, is bit $k + 27$ of $x \oplus (x \gg 18)$, which is $x_{k+27} \oplus x_{k+45}$ if $k + 45 \le 63$, that is $k \le 18$, and $x_{k+27}$ if $k \ge 19$. So $h(x)$ depends only on the bits $x_{27}, \ldots, x_{63}$, and not on the 27 low bits. Fix the top five bits. Given a target $y \in \{0, 1\}^{32}$, solve for $x_{58}, x_{57}, \ldots, x_{27}$ in this order: for $k \ge 19$, $x_{k+27} = y_k$; for $k \le 18$, $x_{k+27} = y_k \oplus x_{k+45}$, and $x_{k+45}$ is either one of the fixed top bits ($k + 45 \ge 59$) or a bit $x_{k+45}$ with $k + 45 > k + 27$ that is already solved. So there is exactly one choice of $x_{27}, \ldots, x_{58}$ for each $y$, and the 27 low bits are free. Each $y$ has exactly $2^{27}$ preimages in $X_\tau$. $\square$

**Theorem.** Over any $N$ consecutive calls of PCG32-NEXT, every 32-bit value is output exactly $2^{32}$ times.

*Proof.* By Lemma 1, $N$ consecutive calls see each state $x \in \mathbb{Z}_N$ once as the old state. For $x \in X_\tau$, the output is $\mathrm{rotr}_{32}(h(x), \tau)$. Rotation by the fixed amount $\tau$ is a bijection of 32-bit words, so by Lemma 2 each 32-bit value $v$ is the output of exactly $2^{27}$ states of $X_\tau$, those with $h(x) = \mathrm{rotl}_{32}(v, \tau)$. Summing over the 32 values of $\tau$ gives $32 \cdot 2^{27} = 2^{32}$ states with output $v$. $\blacksquare$
