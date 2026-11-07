---
title: Grow-Expansion keeps an exact nonoverlapping expansion, and the final pass rounds it correctly
proves: [correctness]
status: full
---

**Setting.** Binary floating point with precision $p \ge 2$, gradual underflow, and round to nearest. Ties go to even for the final result, and any tie rule is allowed elsewhere. No operation overflows. For a nonzero float $x$, $\epsilon(x)$ is the largest power of two dividing $x$, and $\epsilon(0) = \infty$. An expansion is a list $e_1, \ldots, e_m$ of nonzero floats with $|e_k| < \epsilon(e_{k+1})$. TwoSum$(a, b)$ returns $s = \mathrm{fl}(a + b)$ and $t = a + b - s$ exactly. Fast2Sum$(a, b)$ returns the same pair when $|a| \ge |b|$. Both facts are standard (Knuth Vol. 2 Section 4.2.2, Dekker 1971) and hold with underflow.

**Lemma A (TwoSum error).** Let $(s, t) = \mathrm{TwoSum}(a, b)$. Then $|t| \le \min(|a|, |b|)$, and if $t \ne 0$ then $s \ne 0$ and $|t| < \epsilon(s)$.

*Proof.* $a$ is a float at distance $|b|$ from $a + b$. The nearest float $s$ is no farther, so $|t| \le |b|$, and by symmetry $|t| \le |a|$. If $t \ne 0$, then $a + b$ is not a float, so it lies strictly between two consecutive floats $f_1 < f_2$. Their distance $d = f_2 - f_1$ is a power of two, and both are multiples of $d$. With gradual underflow, every multiple of $2^{e_{\min} - p + 1}$ near 0 is a float, so neither $f_1$ nor $f_2$ is $0$ unless $a + b$ is already a float. Hence $s \in \{f_1, f_2\}$ is nonzero, $\epsilon(s) \ge d$, and $|t| \le d/2 < \epsilon(s)$. $\square$

**Lemma B (grid).** If $a$ and $b$ are multiples of a power of two $g$, then so are $s = \mathrm{fl}(a + b)$ and $t = a + b - s$.

*Proof.* If $a + b$ is a float, then $s = a + b$ and $t = 0$. Otherwise $a + b$ lies strictly between consecutive floats $f_1, f_2$ at distance $d$, which are multiples of $d$. So $d$ does not divide $a + b$, but $g$ does, and therefore $d > g$. As both are powers of two, $g$ divides $d$, so $g$ divides $s \in \{f_1, f_2\}$ and $t$. $\square$

**Lemma C (domination).** In an expansion, $\sum_{l < k} |e_l| < \epsilon(e_k)$ for every $k$. In particular $|e_k| > \sum_{l<k}|e_l|$, every partial sum $e_k + \cdots + e_m$ is nonzero, and a nonzero sum $\sum_{l<k} e_l$ has the sign of its largest term.

*Proof.* $|e_l| < \epsilon(e_{l+1})$ means that all binary digits of $|e_l|$ are below the lowest digit of $e_{l+1}$. So the digit sets of $|e_1|, \ldots, |e_{k-1}|$ are pairwise disjoint and all lie below position $\log_2 \epsilon(e_k)$. A sum of numbers with disjoint digit sets has no carries, so it is below $\epsilon(e_k)$. The other claims follow, because $|e_k| \ge \epsilon(e_k)$. $\square$

**Theorem 1 (Grow-Expansion).** Let $e_1, \ldots, e_m$ be an expansion and $x$ a float. Set $Q_0 = x$ and $(Q_k, h_k) = \mathrm{TwoSum}(Q_{k-1}, e_k)$ for $k = 1, \ldots, m$. Then the list of nonzero $h_k$ in order, followed by $Q_m$ if it is nonzero, is an expansion with value $x + \sum_k e_k$.

*Proof.* *Value.* $Q_k + h_k = Q_{k-1} + e_k$ for each $k$. Summing these equations gives $Q_m + \sum_k h_k = x + \sum_k e_k$.

*Nonoverlap.* Let $g_k = \min(\epsilon(Q_{k-1}), \epsilon(e_k))$, a power of two. By Lemma B, $Q_k$ and $h_k$ are multiples of $g_k$. We show by induction on $k$ that for all $i < k$,
$$
(\ast)\qquad |h_i| < \epsilon(e_k) \quad\text{and}\quad |h_i| < \epsilon(Q_{k-1}).
$$
The first part holds for every $k > i$, by Lemmas A and C: $|h_i| \le |e_i| \le \sum_{l<k}|e_l| < \epsilon(e_k)$. For the second part with $k = i + 1$, Lemma A gives $|h_i| < \epsilon(Q_i)$, or $h_i = 0$. For $k > i + 1$, the induction hypothesis for $k - 1$ gives $|h_i| < g_{k-1}$, and $g_{k-1}$ divides $Q_{k-1}$, so $\epsilon(Q_{k-1}) \ge g_{k-1} > |h_i|$.

From $(\ast)$, $|h_i| < g_k \le \epsilon(h_k)$ whenever $i < k$ and $h_k \ne 0$. The same argument with $k = m + 1$, using $g_{m+1} := \epsilon(Q_m)$, gives $|h_i| < \epsilon(Q_m)$ for $i < m$. Lemma A gives $|h_m| < \epsilon(Q_m)$. So every pair of consecutive components of the output, after the zeros are removed, satisfies the expansion condition. $\square$

**Theorem 2 (rounding).** Let $e_1, \ldots, e_m$ be a nonempty expansion with value $S$. Lines L8 to L11 return $\mathrm{RN}(S)$, the nearest float with ties to even.

*Proof.* Write $\sigma_j = e_j + \cdots + e_m$. Every $e_l$ with $l \ge j$ is a multiple of $\epsilon(e_j)$, because $\epsilon(e_l)$ increases with $l$.

*Exact phase.* Suppose that before $e_j$ is processed, $s = \sigma_{j+1}$. This is true at the start. $\sigma_{j+1}$ is a nonzero multiple of $\epsilon(e_{j+1})$ (Lemma C), so $|s| \ge \epsilon(e_{j+1}) > |e_j|$, and Fast2Sum is exact. If its error is $0$, then $s = \sigma_j$ and the invariant continues. If the loop runs to the end, then $s = \sigma_1 = S$ is a float, L10 does nothing, and the result is $S$.

*First inexact step.* Otherwise the loop breaks at some $j$ with $s = \mathrm{RN}(\sigma_j)$ and $t = \sigma_j - s \ne 0$. Let $R = \sum_{l < j} e_l$, so $S = s + t + R$. By Lemma B with $g = \epsilon(e_j)$, $t$ is a nonzero multiple of $\epsilon(e_j)$. By Lemma C, $|R| < \epsilon(e_j) \le |t|$, and if $j > 1$ then $R \ne 0$ has the sign of $e_{j-1}$. Let $D$ be the distance from $s$ to the next float in the direction of $t$. It is a power of two, and $|t| \le D/2$ because $s$ is nearest to $s + t$. $D/2 \ge |t| \ge \epsilon(e_j)$ is a power of two, so it is a multiple of $\epsilon(e_j)$. Line L10 computes $2t$ exactly. Also, $\mathrm{fl}(s + 2t) - s$ is computed exactly, since it is $0$ or the float $\pm D$, the difference of two adjacent floats.

- *Case $|t| < D/2$.* Then $|t| \le D/2 - \epsilon(e_j)$, so $t + R$ has the sign of $t$ and $|t + R| < D/2$. $S$ lies strictly between $s$ and the midpoint in that direction, so $\mathrm{RN}(S) = s$. In L10, $s + 2t$ lies strictly between $s$ and its neighbour, so $\mathrm{fl}(s + 2t) - s \in \{0, \pm D\}$ differs from $2t$, and $s$ is kept.
- *Case $|t| = D/2$, $j = 1$.* Then $S = s + t$ is a midpoint, and $s = \mathrm{RN}(\sigma_1)$ was chosen by ties to even. L10 does not fire.
- *Case $|t| = D/2$, $j > 1$, $R$ with the sign of $t$.* Then $D/2 < |t + R| < D/2 + \epsilon(e_j) \le D$. $S$ is past the midpoint, so $\mathrm{RN}(S) = s + 2t$, the neighbour. In L10, $s + 2t$ is a float, so $\mathrm{fl}(s + 2t) - s = 2t$, and the step is taken.
- *Case $|t| = D/2$, $j > 1$, $R$ with the opposite sign.* Then $0 < |t + R| < D/2$, so $\mathrm{RN}(S) = s$. The sign test in L10 fails, and $s$ is kept.

In every case the result is $\mathrm{RN}(S)$. $\square$

**Corollary.** SHEWCHUK-SUM returns $\mathrm{RN}(x_1 + \cdots + x_n)$. *Proof.* The empty list is an expansion with value 0. By Theorem 1 and induction on $i$, after step $i$ the list $e$ is an expansion with value $x_1 + \cdots + x_i$. If it is empty, the sum is $0$ and the result is $0$. Otherwise Theorem 2 applies. $\blacksquare$
