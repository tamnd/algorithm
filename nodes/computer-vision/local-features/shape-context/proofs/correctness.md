---
title: Correctness of shape context matching
proves: [correctness]
status: full
---

Let $P = \{p_1, \dots, p_n\}$ with $n \ge 2$ distinct points, $\alpha_P = \frac{1}{n^2}\sum_{i, j} \lVert p_j - p_i \rVert > 0$, and $h_i$ the normalized log-polar histogram of $p_i$ as defined on the page. The cost of two histograms $a$ and $b$ with nonnegative entries that sum to 1 (or are all 0) is $C(a, b) = \frac{1}{2}\sum_k (a_k - b_k)^2 / (a_k + b_k)$ with $0/0 = 0$.

**Lemma 1 (translation and scale).** Let $P' = \{s p_i + t\}$ with $s > 0$. Then $h'_i = h_i$ for each $i$.

*Proof.* $p'_j - p'_i = s (p_j - p_i)$, so each distance is multiplied by $s$, and so is the mean $\alpha$. So $r'_{ij} = s \lVert p_j - p_i \rVert / (s \alpha_P) = r_{ij}$. The direction of $s (p_j - p_i)$ is the direction of $p_j - p_i$ since $s > 0$, so $\theta'_{ij} = \theta_{ij}$. Each vector falls into the same bin or is left out in both cases, so the counts and their total are the same, and so are the normalized histograms. $\square$

In floating point the lemma holds exactly when $s$ is a power of 2 and the translation keeps the coordinates exact, as in the tests; otherwise a vector very close to a bin edge can change bins.

**Lemma 2 (the cost).** $0 \le C(a, b) \le 1$, and $C(a, b) = 0$ exactly when $a = b$.

*Proof.* Each term with $a_k + b_k > 0$ is a square divided by a positive number, so it is $\ge 0$, and it is 0 exactly when $a_k = b_k$. Terms with $a_k + b_k = 0$ have $a_k = b_k = 0$. So $C \ge 0$, with equality exactly when $a = b$. For $a_k, b_k \ge 0$ we have $(a_k - b_k)^2 \le (a_k + b_k)^2$, so each term is at most $a_k + b_k$, and $C \le \frac{1}{2}\sum_k (a_k + b_k) \le \frac{1}{2}(1 + 1) = 1$. $\square$

**Lemma 3 (the Hungarian method is optimal).** For an $N \times N$ matrix $C$, the procedure of line L8 returns a permutation $\pi$ with the least $\sum_i C_{i \pi(i)}$.

*Proof.* The procedure keeps potentials $u_i$ and $v_j$ with $u_i + v_j \le C_{ij}$ for all $i, j$ (dual feasibility) and a partial matching that uses only tight pairs, those with $u_i + v_j = C_{ij}$. It adds the rows one at a time. For a new row it grows a tree of alternating paths over tight pairs; when no tight pair leaves the tree, it changes the potentials by the smallest slack $\delta$ of a pair from a row in the tree to a column outside it. Adding $\delta$ to $u$ on the rows of the tree and subtracting it from $v$ on the columns of the tree keeps every pair of the tree and of the matching tight, keeps dual feasibility by the choice of $\delta$, and makes at least one new pair tight. So after at most $N$ such changes the tree reaches a free column, and the matching grows by one along the path. After $N$ rows, $\pi$ is a perfect matching of tight pairs, so $\sum_i C_{i\pi(i)} = \sum_i u_i + \sum_j v_j$. For any permutation $\sigma$, dual feasibility gives $\sum_i C_{i\sigma(i)} \ge \sum_i (u_i + v_{\sigma(i)}) = \sum_i u_i + \sum_j v_j$. So $\pi$ is optimal. This is the argument of Kuhn (1955), in the form with shortest augmenting paths. $\square$

**Lemma 4 (dummies).** Let $C$ be $n \times m$ and $\varepsilon \ge 0$. Pad it to $(n + m) \times (n + m)$ with the cost $\varepsilon$ between a real row and a dummy column or a dummy row and a real column, and 0 between two dummies. Then the least cost of the padded assignment equals the least cost, over all partial matchings $M$ of rows to columns, of $\sum_{(i, j) \in M} C_{ij} + \varepsilon (n + m - 2|M|)$.

*Proof.* Take an assignment of the padded matrix, and let $M$ be its pairs of a real row and a real column. The other $n - |M|$ real rows go to dummy columns, and the other $m - |M|$ real columns get dummy rows, each at the cost $\varepsilon$. The remaining dummy rows go to dummy columns at the cost 0. So the cost of the assignment is the cost of $M$ in the formula. Conversely, given a partial matching $M$, assign the unmatched real rows to distinct dummy columns, the unmatched real columns to distinct dummy rows, and the remaining $|M|$ dummy rows to the remaining $|M|$ dummy columns. There are $n$ dummy rows and $m$ dummy columns, so this is possible, and the cost is the cost of $M$ in the formula. So the two minima are equal, and an optimal padded assignment gives an optimal partial matching. $\square$

**Theorem.** SHAPE-CONTEXT-MATCH returns a matching of least total chi-square cost between the shape contexts of $P$ and $Q$, with each point matched to a dummy costing $\varepsilon_d$ when dummies are used. The result does not change under a translation or a scaling by $s > 0$ of either shape, and if $Q$ is a translated and scaled copy of $P$ with its points permuted by $\sigma$, the matching $\sigma$ has cost 0 and is optimal.

*Proof.* Lines L1 to L5 compute the histograms of the definition, and line L6 the costs. By Lemma 3 line L8 returns an optimal assignment of the matrix, and by Lemma 4 it is an optimal partial matching when dummies are used. By Lemma 1 the histograms, and so the costs and the matching, do not change under translation and scaling. If $Q$ is such a copy, Lemma 1 gives $h^Q_{\sigma(i)} = h^P_i$, so by Lemma 2 the matching $\sigma$ has cost 0, which is the least possible cost since all costs are $\ge 0$. $\square$
