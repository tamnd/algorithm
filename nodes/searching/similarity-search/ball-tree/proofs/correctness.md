---
title: The ball tree is balanced and its searches are exact
proves: [correctness]
status: full
---

Let $(M, \delta)$ be a metric space, $S \subseteq M$ with $|S| = n \ge 1$, and $b \ge 1$ the leaf size.

**Lemma 1 (covering).** Every node $t$ built by BUILD satisfies (R): $\delta(t.c, x) \le t.\rho$ for every point $x$ of its subtree.

*Proof.* Line L2 sets $t.\rho = \max_{x \in S} \delta(t.c, x)$, where $S$ is the set of points of the subtree of $t$. $\square$

**Lemma 2 (height).** A node at depth $j$ (the root has depth 0) holds at most $\lceil n / 2^j \rceil$ points, and the tree has at most $\lceil \lg(n/b) \rceil + 1$ levels when $n > b$.

*Proof.* Line L4 gives the children $\lfloor s/2 \rfloor$ and $\lceil s/2 \rceil$ points, and $\lceil \lceil n/2^j \rceil / 2 \rceil = \lceil n / 2^{j+1} \rceil$. A node with at most $b$ points is a leaf. At depth $j = \lceil \lg(n/b) \rceil$, $n/2^j \le b$, and $b$ is an integer, so $\lceil n/2^j \rceil \le b$ and every node at that depth is a leaf. $\square$

**Lemma 3 (lower bound).** For every $q \in M$ and every point $x$ in the subtree of $t$, $\delta(q, x) \ge \delta(q, t.c) - t.\rho$.

*Proof.* By the triangle inequality, $\delta(q, t.c) \le \delta(q, x) + \delta(x, t.c)$, and $\delta(x, t.c) \le t.\rho$ by Lemma 1. $\square$

**Theorem 1.** KNN$(root, q, k)$ returns $\min(k, n)$ pairs whose distances are the $\min(k, n)$ smallest values of $\delta(q, x)$ over $x \in S$, each with a point at that distance.

*Proof.* Let $\tau$ be the $k$-th distance in $H$, or $\infty$ when $H$ has fewer than $k$ pairs; $\tau$ never increases. Every pair in $H$ is a stored point with its true distance, since only line L7 offers pairs. Call a point *skipped* if it lies in a subtree pruned at line L6. At the moment a node $t$ is pruned, Lemma 3 gives $\delta(q, x) \ge \delta(q, t.c) - t.\rho \ge \tau$ for each point $x$ of $t$, so $H$ already holds $k$ pairs of distance at most $\delta(q, x)$. Since $H$ keeps the $k$ least offered pairs, it holds $k$ pairs of distance at most $\delta(q, x)$ at the end as well.

Let $D_1 \le \dots \le D_k$ be the final distances in $H$ and $\delta_1 \le \dots \le \delta_n$ the true sorted distances. Each $D_i$ is the distance of a distinct point, so $D_i \ge \delta_i$. Suppose $D_i > \delta_i$ for some $i$, and take the $i$ points $x_1, \dots, x_i$ with distances $\delta_1, \dots, \delta_i$. At most $i - 1$ of them are in $H$ with a distance below $D_i$, so some $x_j$ with $\delta(q, x_j) \le \delta_i < D_i$ is not in $H$. If $x_j$ was offered and later dropped or never kept, then at that moment $H$ held $k$ pairs of distance at most $\delta(q, x_j)$, and the final pairs are no larger, so $D_k \le \delta(q, x_j) < D_i \le D_k$, which is impossible. If $x_j$ was skipped, the paragraph above gives $D_k \le \delta(q, x_j) < D_i \le D_k$, again impossible. So $D_i = \delta_i$ for all $i$. If $n < k$, no node is pruned since $\tau = \infty$, and every point is offered. $\square$

**Theorem 2.** RANGE$(root, q, r)$ reports exactly the points $x \in S$ with $\delta(q, x) \le r$, each once.

*Proof.* Line L10 reports only points that pass the test. A point $x$ is not offered only if an ancestor node $t$ was pruned at line L9, and then Lemma 3 gives $\delta(q, x) \ge \delta(q, t.c) - t.\rho > r$. Each point is in exactly one leaf, which is visited at most once. $\blacksquare$
