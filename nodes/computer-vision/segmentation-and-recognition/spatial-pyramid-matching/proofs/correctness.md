---
title: The spatial pyramid kernel counts new matches per level with nonnegative weights and is positive semidefinite
proves: [correctness]
status: full
---

We use the notation of the page. $X$ and $Y$ are finite sets of features $(u, v, m)$. At level $l$, a bin is a pair (cell, word), $H_X^l(b)$ is the number of features of $X$ in bin $b$, and $I^l = \sum_b \min(H_X^l(b), H_Y^l(b))$. Lines L1 to L4 compute exactly these counts and sums, by the definitions, so the claims below are about the values that SPM-KERNEL returns.

**Lemma 1 (the cells nest).** For $l < L$, every bin of level $l + 1$ lies inside exactly one bin of level $l$ with the same word, and every bin of level $l$ is the union of the four bins of level $l + 1$ inside it with the same word.

*Proof.* Let $s = 2^l$ and $c(u) = \min(\lfloor u s / W \rfloor, s - 1)$ the column index at level $l$, and $c'(u) = \min(\lfloor 2 u s / W \rfloor, 2s - 1)$ the one at level $l + 1$. We show $c(u) = \lfloor c'(u)/2 \rfloor$ for $0 \le u \le W$. If $u < W$, then $c(u) = \lfloor y \rfloor$ and $c'(u) = \lfloor 2y \rfloor$ with $y = us/W < s$, and $\lfloor \lfloor 2y \rfloor / 2 \rfloor = \lfloor y \rfloor$. If $u = W$, then $c(u) = s - 1$ and $c'(u) = 2s - 1$, and $\lfloor (2s - 1)/2 \rfloor = s - 1$. The same holds for the rows. So the level-$l$ cell of a feature is a function of its level-$(l+1)$ cell, and each level-$l$ cell $(i, j)$ contains the four cells $(2i + a, 2j + b)$, $a, b \in \{0, 1\}$. The word is the same at all levels. $\square$

**Theorem 1 (the two forms agree).** $I^L + \sum_{l=0}^{L-1} 2^{-(L-l)} (I^l - I^{l+1}) = 2^{-L} I^0 + \sum_{l=1}^{L} 2^{-(L-l+1)} I^l$.

*Proof.* Collect the coefficient of each $I^l$ on the left. $I^0$ appears once, in the term $l = 0$, with $2^{-L}$. For $1 \le l \le L - 1$, $I^l$ appears with $+2^{-(L-l)}$ in term $l$ and with $-2^{-(L-l+1)}$ in term $l - 1$, so its coefficient is $2^{-(L-l)} - 2^{-(L-l+1)} = 2^{-(L-l+1)}$. $I^L$ appears with $+1$ alone and $-2^{-1}$ in term $L - 1$, so its coefficient is $1/2 = 2^{-(L-L+1)}$. If $L = 0$ both sides are $I^0$. $\square$

**Lemma 2 (intersection is a maximum matching).** Call a matching at level $l$ a set of disjoint pairs $(x, y) \in X \times Y$ such that $x$ and $y$ are in the same bin of level $l$. Then the largest such matching has exactly $I^l$ pairs.

*Proof.* The pairs never connect different bins, so a matching is a union of matchings inside the bins. Inside bin $b$ any pairing of $H_X^l(b)$ features with $H_Y^l(b)$ features has at most $\min(H_X^l(b), H_Y^l(b))$ pairs, and pairing them in any order reaches this number. Summing over the bins gives $I^l$. $\square$

**Lemma 3 (monotone).** $I^l \ge I^{l+1}$ for $0 \le l < L$.

*Proof.* By Lemma 1, a matching at level $l + 1$ pairs features that are in the same bin at level $l + 1$, so also in the same bin at level $l$. So it is also a matching at level $l$, and by Lemma 2 $I^{l+1} \le I^l$. In terms of counts: if a bin at level $l$ splits into bins with counts $a_1, \ldots, a_4$ and $b_1, \ldots, b_4$, then $\min(\sum_j a_j, \sum_j b_j) \ge \sum_j \min(a_j, b_j)$, since the right side is at most $\sum_j a_j$ and at most $\sum_j b_j$. $\square$

So $I^L$ is the number of matches at the finest level, and $I^l - I^{l+1} \ge 0$ is the number of matches that a largest matching gains when the cells grow from level $l + 1$ to level $l$. The kernel gives weight 1 to the finest matches and $2^{-(L-l)}$ to those new at level $l$, as the page says.

**Theorem 2 (positive semidefinite).** For any finite list of feature sets $X^{(1)}, \ldots, X^{(N)}$, the matrix $G_{ij} = \kappa^L(X^{(i)}, X^{(j)})$ is symmetric and positive semidefinite. The same holds when each histogram is first divided by the number of features of its image.

*Proof.* Symmetry is clear since $\min$ is symmetric. For $a, b \ge 0$, $\min(a, b) = \int_0^\infty [t < a]\,[t < b]\, dt$, where $[\cdot]$ is 1 if the condition holds and 0 otherwise. So for reals $c_1, \ldots, c_N$ and one bin $b$ of level $l$, with $h_i = H^l_{X^{(i)}}(b)$,
$$\sum_{i,j} c_i c_j \min(h_i, h_j) = \int_0^\infty \Big( \sum_i c_i [t < h_i] \Big)^2 dt \ge 0.$$
So $\min(h_i, h_j)$ is a positive semidefinite kernel for each bin. A sum of positive semidefinite kernels is positive semidefinite, so $I^l$ is one, and so is $\sum_l a_l I^l$ for $a_l \ge 0$. By Theorem 1, $\kappa^L$ has this form with the positive weights $2^{-L}$ and $2^{-(L-l+1)}$. Dividing the histograms of image $i$ by $n_i > 0$ replaces $h_i$ by $h_i/n_i \ge 0$, and the same argument applies. $\square$

**Corollary (the concatenated vector).** Let $\phi(X)$ be the concatenation, over the levels, of the histograms of level $l$ multiplied by $a_0 = 2^{-L}$ and $a_l = 2^{-(L-l+1)}$ for $l \ge 1$. Then $\sum_i \min(\phi(X)_i, \phi(Y)_i) = \kappa^L(X, Y)$.

*Proof.* For $a > 0$, $\min(a h, a h') = a \min(h, h')$. Summing over the entries of level $l$ gives $a_l I^l$, and Theorem 1 gives the claim. $\square$

**What is not claimed.** The weights are a design choice taken from the pyramid match kernel. Nothing here says that the kernel classifies well; that is a benchmark result.
