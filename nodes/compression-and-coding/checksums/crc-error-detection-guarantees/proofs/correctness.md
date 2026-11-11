---
title: Proof of the error-detection guarantees of a CRC
proves: [statement]
status: full
---

Setting. $G(x) \in \mathrm{GF}(2)[x]$ has degree $r \ge 1$ and $G(0) = 1$. A codeword has $N$ bits, and an error is a nonzero polynomial $E(x)$ of degree less than $N$. By Theorem 2 of the proof on the [cyclic redundancy check](/cyclic-redundancy-check/) page, the receiver misses $E$ if and only if $G \mid E$. This holds for every init and xorout, and with reflection after a fixed permutation of the positions, which keeps weights. For bursts with reflection, the statement holds for the bit order in which the register reads the bits.

**Lemma 0.** $\gcd(x, G) = 1$. So $G \mid x^i A$ if and only if $G \mid A$.

*Proof.* $G(0) = 1$, so $x \nmid G$, and $x$ is irreducible. If $G \mid x^i A$, then since $G$ and $x^i$ have no common factor, $G \mid A$. $\square$

**Theorem 1 (single errors).** If $r \ge 1$, every error of weight 1 is detected.

*Proof.* $E = x^i$. By Lemma 0, $G \mid x^i$ would give $G \mid 1$, which is false for $\deg G \ge 1$. $\square$

**Theorem 2 (odd weight).** If $(x + 1) \mid G$, every error of odd weight is detected.

*Proof.* Evaluate at $x = 1$: $E(1)$ is the weight of $E$ modulo 2, which is 1. If $G \mid E$, then $(x + 1) \mid E$, so $E(1) = 0$. Contradiction. $\square$

**Theorem 3 (double errors).** Let $e$ be the period of $G$, the least $e \ge 1$ with $G \mid x^e + 1$. It exists because $x$ is a unit modulo $G$ (Lemma 0) and the unit group of $\mathrm{GF}(2)[x]/(G)$ is finite. An error $x^i + x^{i+j}$ with $j \ge 1$ is missed if and only if $e \mid j$. So if $N \le e$, every error of weight 2 is detected.

*Proof.* $x^i + x^{i+j} = x^i (x^j + 1)$. By Lemma 0 it is missed if and only if $x^j \equiv 1 \pmod G$. The set of $j$ with $x^j \equiv 1$ is the set of multiples of the order $e$ of $x$ in the unit group. For $N \le e$, the distance $j \le N - 1 < e$ is not a multiple of $e$. $\square$

When $G = (x + 1) p(x)$ with $p$ primitive of degree $r - 1$ and $p \ne x + 1$, the period is $\mathrm{lcm}(1, 2^{r-1} - 1) = 2^{r-1} - 1$, because $x \equiv 1 \pmod{x+1}$ and $x$ has order $2^{r-1} - 1$ modulo $p$, and the Chinese remainder theorem applies to the coprime factors. When $G$ is primitive of degree $r$, the period is $2^r - 1$.

**Definition.** A burst of length $b \ge 1$ is an error $E = x^i B(x)$ where $\deg B = b - 1$ and $B(0) = 1$: the first and the last wrong bits are $b - 1$ apart, and the bits between are arbitrary.

**Theorem 4 (short bursts).** Every burst of length $b \le r$ is detected.

*Proof.* By Lemma 0, $x^i B$ is missed if and only if $G \mid B$. But $B \ne 0$ and $\deg B = b - 1 < r = \deg G$, so $G \nmid B$. $\square$

**Theorem 5 (long bursts).** Among the $2^{b-2}$ bursts of length $b \ge 2$ at a fixed position, the number that are missed is 1 if $b = r + 1$, and $2^{b-r-2}$ if $b \ge r + 2$. So the missed fraction is $2^{-(r-1)}$ for $b = r + 1$ and $2^{-r}$ for $b \ge r + 2$.

*Proof.* There are $2^{b-2}$ choices of $B$ with $\deg B = b - 1$ and $B(0) = 1$, one for each choice of the $b - 2$ inner bits. By Lemma 0 the burst is missed if and only if $B = G Q$ for some $Q$. Then $\deg Q = b - 1 - r$, the leading coefficient of $Q$ is 1, and $Q(0) = B(0)/G(0) = 1$.

If $b = r + 1$, then $\deg Q = 0$, so $Q = 1$ and $B = G$: one burst. Since $2^{b-2} = 2^{r-1}$, the fraction is $2^{-(r-1)}$.

If $b \ge r + 2$, then $\deg Q = b - 1 - r \ge 1$, its top and bottom coefficients are 1, and its $b - r - 2$ inner coefficients are free. Each such $Q$ gives a distinct $B = GQ$ with $\deg B = b - 1$ and $B(0) = 1$. So $2^{b-r-2}$ bursts are missed, and the fraction is $2^{b-r-2} / 2^{b-2} = 2^{-r}$. $\square$

**Theorem 6 (all patterns).** For $N \ge r$, exactly $2^{N-r} - 1$ of the $2^N - 1$ nonzero patterns of length $N$ are missed.

*Proof.* The missed patterns are the nonzero multiples $GQ$ with $\deg(GQ) < N$, that is, $\deg Q < N - r$. There are $2^{N-r}$ such $Q$, and $Q = 0$ gives the zero pattern. $\square$

So for errors that are uniform over all nonzero patterns, the missed fraction is $(2^{N-r} - 1)/(2^N - 1) < 2^{-r}$.
