---
title: Clipping and filtering is an alternating projection, so the output is band-limited and the clipped-off energy never grows
proves: [correctness]
status: full
---

Work in $\mathbb{C}^{LN}$ with the Euclidean norm $\|v\|^2 = \sum_m |v[m]|^2$, in exact arithmetic. Let

- $S = \{ v : |v[m]| \le A \text{ for all } m \}$, the signals that the amplifier passes without clipping, and
- $B = \{ v : (F_{LN} v)[k] = 0 \text{ for } N/2 \le k < LN - N/2 \}$, the band-limited signals, which are the oversampled OFDM symbols $\sqrt L F_{LN}^H Z$ of line L1.

$S$ is closed and convex, since it is a product of closed discs. $B$ is a linear subspace. Write $x_0$ for the symbol of line L1, and $x_{i}$ for the value of $x$ after iteration $i$ (lines L4 to L7). Let $d_i = \operatorname{dist}(x_i, S)$ and $c_i$ be the clipped signal of line L4 in iteration $i + 1$.

**Lemma 1 (line L4 is the projection onto $S$).** For every $v$, the clipped signal $c$ with $c[m] = v[m]$ if $|v[m]| \le A$ and $c[m] = A\, v[m] / |v[m]|$ otherwise is the unique point of $S$ nearest to $v$, and $\|v - c\|^2 = \sum_{|v[m]| > A} (|v[m]| - A)^2$.

*Proof.* The norm is a sum over $m$ and $S$ is a product of discs, so the nearest point can be found one coordinate at a time. For one coordinate, the nearest point of the disc $|z| \le A$ to $v[m]$ is $v[m]$ itself if it is inside. Otherwise, for $|z| \le A$, the triangle inequality gives $|v[m] - z| \ge |v[m]| - |z| \ge |v[m]| - A$, with equality only for $z = A v[m]/|v[m]|$. $\square$

**Lemma 2 (lines L5 to L7 are the orthogonal projection onto $B$).** For every $c$, the signal $P_B c$ obtained by an FFT, zeroing the out-of-band bins and an inverse FFT, is the unique point of $B$ nearest to $c$, and $c - P_B c$ is orthogonal to $B$.

*Proof.* $F_{LN}/\sqrt{LN}$ is unitary, so it preserves distances. In the frequency domain, $B$ is the set of vectors that are zero on the out-of-band bins, a coordinate subspace. The nearest point of a coordinate subspace keeps the free coordinates and sets the others to zero, and the difference has its support on the zeroed bins, so it is orthogonal to the subspace. Line L7 uses the exact inverse of the FFT of line L5, so the result is this nearest point in time. $\square$

So one iteration is $x_{i+1} = P_B P_S x_i$, and $c_i = P_S x_i$.

**Theorem 1 (band limit).** For every $i \ge 0$, $x_i \in B$. The final $x$ has no energy outside the $N$ subcarriers of the symbol, and line L8 returns its $N$ in-band values, from which line L1 gives back the same $x$.

*Proof.* $x_0 \in B$ by construction, and $x_{i+1} = P_B c_i \in B$ by Lemma 2. Line L1 applied to the in-band values of a vector of $B$ rebuilds that vector, because its out-of-band bins are zero. $\square$

**Theorem 2 (the clipped-off energy never grows).** With $e_i = \|c_i - x_{i+1}\| = \operatorname{dist}(c_i, B)$, the energy that the filter removes,

$$d_0 \ge e_0 \ge d_1 \ge e_1 \ge d_2 \ge \cdots.$$

*Proof.* $e_i = \operatorname{dist}(c_i, B) \le \|c_i - x_i\| = d_i$, because $x_i \in B$ (Theorem 1) and $\|c_i - x_i\| = \operatorname{dist}(x_i, S)$ by Lemma 1. And $d_{i+1} = \operatorname{dist}(x_{i+1}, S) \le \|x_{i+1} - c_i\| = e_i$, because $c_i \in S$. $\square$

By Lemma 1, $d_i^2$ is the energy $\sum (|x_i[m]| - A)^2$ above the threshold, the quantity that the implementation returns for each iteration.

**Theorem 3 (convergence).** $d_i \to 0$, and the sequence $x_i$ converges to a point of $S \cap B$.

*Proof.* The set $S \cap B$ is not empty, since it contains $0$. Fix any $z \in S \cap B$. For a projection $P$ onto a closed convex set that contains $z$, the projection inequality $\mathrm{Re}\langle v - Pv, z - Pv \rangle \le 0$ gives

$$\|Pv - z\|^2 \le \|v - z\|^2 - \|v - Pv\|^2.$$

Apply it to $P_S$ at $x_i$ and to $P_B$ at $c_i$:

$$\|x_{i+1} - z\|^2 \le \|x_i - z\|^2 - d_i^2 - e_i^2.$$

Summing over $i$ gives $\sum_i (d_i^2 + e_i^2) \le \|x_0 - z\|^2$, so $d_i \to 0$ and $e_i \to 0$. The sequence $\|x_i - z\|$ does not increase, so $(x_i)$ is bounded and has a convergent subsequence $x_{i_t} \to x^\ast$. Since $x_{i_t} \in B$ and $\operatorname{dist}(x_{i_t}, S) \to 0$ and both sets are closed, $x^\ast \in S \cap B$. Take $z = x^\ast$: $\|x_i - x^\ast\|$ does not increase and has a subsequence that tends to $0$, so the whole sequence tends to $x^\ast$. $\square$

**What the theorems do not say.** The limit lies in $S \cap B$, so its peak amplitude is at most $A$. But its mean power can be smaller than that of $x_0$, so its PAPR relative to its own mean power can still be above $A^2$ divided by the original mean power. And its in-band values differ from the data $X$: the method trades in-band distortion for a lower peak. The theorems hold in exact arithmetic; in floating point each step adds a rounding error of the order of the machine precision times $\|x_i\|$.
