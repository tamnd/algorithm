---
title: The FRT tree dominates the metric and has expected stretch at most 16 H_n
proves: [correctness, termination]
status: full
---

Let $d$ be a metric on the points $0, \ldots, n - 1$, $n \ge 1$. Lines L1 to L9 are those of the pseudocode on the page. Since every quantity in the algorithm scales with $d_{\min}$, assume $d_{\min} = 1$ (for $n = 1$ there are no pairs and nothing to scale). Then $\delta$ is the smallest integer $\ge 1$ with $2^\delta \ge d_{\max}$ when $n \ge 2$, and $\delta = 0$ when $n = 1$; the radius at level $i$ is $\beta_i = \beta 2^{i-1}$ with $\beta \in [1, 2)$; and an edge from level $i + 1$ to level $i$ weighs $2^{i+1}$. For a point $x$ and level $i$ write $c_i(x)$ for the first $w$ in $\pi$ with $d(w, x) \le \beta_i$, and $N_i(x)$ for the value of $node(x)$ after the pass of line L4 for level $i$, with $N_\delta(x)$ the root.

**Lemma 1 (termination and well-definedness).** The algorithm stops after $\delta$ passes of the loop of line L4, each of $n$ iterations. Line L6 always finds $c_i(x)$, and for $0 \le i < \delta$ the clusters $C(a) = \{x : N_i(x) = a\}$ over the nodes $a$ at level $i$ partition the points, each refining a cluster of level $i + 1$.

*Proof.* The loops are bounded. Since $d(x, x) = 0 \le \beta_i$, the scan of $\pi$ in line L6 meets $x$ at the latest. By line L8, $N_i(x)$ is a child of $N_{i+1}(x)$, so the parent of the cluster of $x$ at level $i$ is the cluster of $x$ at level $i + 1$. By line L7, two points $x, y$ get the same node at level $i$ exactly when $N_{i+1}(x) = N_{i+1}(y)$ and $c_i(x) = c_i(y)$, so the clusters at level $i$ are the classes of an equivalence relation that refines the one at level $i + 1$. $\square$

**Lemma 2 (radius).** If $x$ and $y$ are in one cluster at level $i < \delta$, then $d(x, y) \le 2\beta_i < 2^{i+1}$.

*Proof.* They share the center $w = c_i(x) = c_i(y)$, so $d(x, y) \le d(x, w) + d(w, y) \le 2\beta_i = \beta 2^i < 2^{i+1}$, since $\beta < 2$. $\square$

**Lemma 3 (leaves).** The nodes at level 0 are leaves holding one point each, so $leaf$ is injective.

*Proof.* Level 0 is the last pass, so its nodes get no children. If $x \ne y$ shared a node at level 0, they would share a center $w$ with $d(w, x), d(w, y) \le \beta_0 = \beta / 2 < 1$. Distances between distinct points are at least $d_{\min} = 1$, so $w = x$ and $w = y$, a contradiction. $\square$

**Lemma 4 (tree distance).** Let $x \ne y$, and let $\ell$ be the smallest level at which they are in one cluster, so $1 \le \ell \le \delta$ (they share the root at level $\delta$, and not a node at level 0 by Lemma 3). Then $d_T(x, y) = 2^{\ell+2} - 4$.

*Proof.* By Lemma 1 the tree path from $leaf(x)$ goes up through $N_0(x), N_1(x), \ldots$, and the same for $y$. The nodes $N_j(x)$ and $N_j(y)$ differ for $j < \ell$ and agree for $j \ge \ell$, so the path meets at $N_\ell(x)$ and uses, on each side, the edges from level $j$ to level $j + 1$ for $0 \le j < \ell$, of weights $2^{j+1}$. So $d_T(x, y) = 2 \sum_{j=0}^{\ell-1} 2^{j+1} = 2(2^{\ell+1} - 2) = 2^{\ell+2} - 4$. $\square$

**Theorem 1 (dominance).** For all points $x, y$, $d_T(x, y) \ge d(x, y)$.

*Proof.* For $x = y$ both sides are 0. Otherwise let $\ell$ be as in Lemma 4. If $\ell < \delta$, Lemma 2 gives $d(x, y) < 2^{\ell+1}$. If $\ell = \delta$, then $d(x, y) \le d_{\max} \le 2^\delta = 2^\ell$. In both cases $d(x, y) \le 2^{\ell+1} \le 2^{\ell+2} - 4$, because $\ell \ge 1$ gives $2^{\ell+1} \ge 4$. By Lemma 4 this is $d_T(x, y)$. $\square$

**Theorem 2 (expected stretch).** If $\pi$ is a uniformly random order and $\beta$ is uniform on $[1, 2)$, independent of $\pi$, then $\mathbf{E}[d_T(x, y)] \le 16 H_n \, d(x, y)$ for all points $x, y$, where $H_n = \sum_{s=1}^{n} 1/s$.

*Proof.* Fix $x \ne y$ and write $D = d(x, y)$. Say the pair is *split at level $i$*, for $0 \le i < \delta$, if $x$ and $y$ share a cluster at level $i + 1$ but not at level $i$. By Lemma 1 and Lemma 3 the pair is split at exactly one level $i$, which is $\ell - 1$ in Lemma 4, and then $d_T(x, y) = 2^{i+3} - 4 \le 2^{i+3}$. So
$$\mathbf{E}[d_T(x, y)] \le \sum_{i=0}^{\delta - 1} 2^{i+3} \Pr[\text{split at level } i].$$

For each point $w$ let $m(w) = \min(d(w, x), d(w, y))$ and $M(w) = \max(d(w, x), d(w, y))$; by the triangle inequality $M(w) - m(w) \le D$. Number the points $w_1, \ldots, w_n$ so that $m(w_1) \le m(w_2) \le \cdots \le m(w_n)$, breaking ties by label; this order does not depend on $\pi$ or $\beta$.

Suppose the pair is split at level $i$. Since $x$ and $y$ share a cluster at level $i + 1$, they share $N_{i+1}$, so by Lemma 1 they must have different centers, $c_i(x) \ne c_i(y)$. Let $w$ be the first point in $\pi$ with $m(w) \le \beta_i$; it exists because $m(x) = 0$. Every point before $w$ in $\pi$ is farther than $\beta_i$ from both $x$ and $y$, so $c_i(x) = w$ if $d(w, x) \le \beta_i$, and $c_i(y) = w$ if $d(w, y) \le \beta_i$. If both held, the centers would be equal. So exactly one holds, which means $m(w) \le \beta_i < M(w)$. Call $w$ the *cutter*.

If the cutter is $w_s$, then (a) $\beta_i \in [m(w_s), M(w_s))$, and (b) $w_s$ comes before $w_1, \ldots, w_{s-1}$ in $\pi$, because each $w_t$ with $t < s$ has $m(w_t) \le m(w_s) \le \beta_i$ and so would be the cutter if it came earlier. Event (a) depends only on $\beta$ and event (b) only on $\pi$, and in a uniform random order each of $w_1, \ldots, w_s$ is equally likely to come first, so
$$\Pr[\text{split at level } i] \le \sum_{s=1}^{n} \frac{1}{s} \Pr[\beta_i \in [m(w_s), M(w_s))].$$

Now fix $s$, write $I = [m(w_s), M(w_s))$, an interval of length at most $D$, and let $|J|$ denote the length of an interval $J$. The radius $\beta_i = \beta 2^{i-1}$ is uniform on $J_i = [2^{i-1}, 2^i)$, with density $1 / 2^{i-1}$, so $\Pr[\beta_i \in I] = |I \cap J_i| / 2^{i-1}$. Hence
$$\sum_{i=0}^{\delta-1} 2^{i+3} \Pr[\beta_i \in I] = \sum_{i=0}^{\delta - 1} 2^{i+3} \frac{|I \cap J_i|}{2^{i-1}} = 16 \sum_{i=0}^{\delta-1} |I \cap J_i| \le 16 |I| \le 16 D,$$
because the intervals $J_0, J_1, \ldots$ are pairwise disjoint. Exchanging the two finite sums,
$$\mathbf{E}[d_T(x, y)] \le \sum_{s=1}^{n} \frac{1}{s} \sum_{i=0}^{\delta-1} 2^{i+3} \Pr[\beta_i \in [m(w_s), M(w_s))] \le \sum_{s=1}^{n} \frac{16 D}{s} = 16 H_n D. \qquad \square$$

**Theorem 3 (correctness).** The algorithm terminates and returns a rooted tree with positive edge weights whose leaves are the points, one per leaf, such that $d_T$ dominates $d$ on every run and $\mathbf{E}[d_T(x, y)] \le 16 H_n \, d(x, y) = O(\log n) \, d(x, y)$ for every pair.

*Proof.* Termination and the tree structure are Lemma 1, the leaves are Lemma 3, dominance is Theorem 1, and the stretch bound is Theorem 2, with $H_n \le 1 + \ln n$. Undoing the scaling by $d_{\min}$ multiplies $d$, the radii and all edge weights by $d_{\min}$, which changes none of the comparisons. $\blacksquare$
