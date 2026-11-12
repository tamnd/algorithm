---
title: k-means++ returns k distinct data points and its final cost is at most the cost of the seeds
proves: [correctness]
status: full
---

We prove the structural claims. The bound $\mathbb{E}[\phi] \le 8(\ln k + 2)\phi_{\mathrm{OPT}}$ is proved on the page of the [k-means++ guarantee](/k-means-plus-plus-guarantee/).

**Invariant.** Before line L4 of round $j$ (and after line L2 for $j = 2$), $D_i = \min_{1 \le l < j} \|x_i - c_l\|^2$ for each $i$.

*Proof.* After line L2 this holds with the one center $c_1$. Lines L7 and L8 replace $D_i$ by $\min(D_i, \|x_i - c_j\|^2)$, which is the minimum over $c_1, \ldots, c_j$. $\square$

**Lemma 1 (the law of line L5).** If $S > 0$, line L5 picks index $m$ with probability $D_m / S = D(x_m)^2 / \sum_i D(x_i)^2$, where $D$ is the distance to the nearest chosen center. A point with $D_m = 0$ is never picked.

*Proof.* By the invariant, $D_m$ is the squared distance to the nearest chosen center. The weights $D_m / S$ are non-negative and sum to 1, so line L5 is a draw from a probability distribution, and a weight of 0 has probability 0. In the implementation, a uniform $r \in [0, S)$ selects the first index whose prefix sum exceeds $r$; the index $m$ is selected exactly when $r$ lies in an interval of length $D_m$, so with probability $D_m / S$. $\square$

**Lemma 2 (distinct centers).** If the points $x_1, \ldots, x_n$ are distinct and $k \le n$, the centers $c_1, \ldots, c_k$ are $k$ distinct data points.

*Proof.* Each center is a data point by lines L1 and L6. If $c_l = x_m$ for some $l < j$, then $D_m = 0$ by the invariant, so by Lemma 1 the index $m$ is not picked when $S > 0$. If $S = 0$, each point is at distance 0 from a chosen center, so each point is a center; since the points are distinct and $j - 1 < k \le n$ centers exist, this is impossible. So the case $S = 0$ does not occur, and each new center differs from the earlier ones. $\square$

When the points are not distinct, $S = 0$ can occur; the implementation then takes an index that is not chosen yet, so the $k$ chosen indices are still distinct.

**Lemma 3 (Lloyd only improves).** Let $C$ be the seeds and $C'$ the centers returned by line L9. Then $\phi(C') \le \phi(C)$.

*Proof.* The first assignment step of Lloyd's algorithm gives each point a nearest seed, so the cost of these labels with the seeds is exactly $\phi(C)$. By the [correctness of k-means](/k-means/), each later half step does not increase the cost, and at the end each point is at a nearest center, so the final assignment cost equals $\phi(C')$. $\square$

**Consequence.** Any bound on $\mathbb{E}[\phi(C)]$ also holds for $\mathbb{E}[\phi(C')]$. In particular the $8(\ln k + 2)$ bound holds for the full algorithm.
