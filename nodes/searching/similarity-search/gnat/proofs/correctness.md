---
title: Correctness of GNAT range and nearest neighbor search
proves: [correctness]
status: full
---

Let $(M, \delta)$ be a metric space and $S$ a finite set stored in a GNAT. For a node $t$, write $S(t)$ for the points stored in its subtree, that is, its bucket or its split points together with $S(\text{child}_j)$ for each $j$.

**Lemma 1 (structure).** For an internal node with split points $p_1, \dots, p_k$ and groups $D_1, \dots, D_k$: $S(t) = \bigcup_j (D_j \cup \{p_j\})$, the union is disjoint, $S(\text{child}_j) = D_j$, and $\delta(p_i, x) \in \text{range}(i, j)$ for every $x \in D_j \cup \{p_j\}$.

*Proof.* Line L3 puts every non-split point into exactly one group, so the sets $D_j \cup \{p_j\}$ partition $S(t)$. Line L5 builds child$_j$ from $D_j$. Line L4 defines range$(i, j)$ as the least interval that contains $\delta(p_i, x)$ for all $x \in D_j \cup \{p_j\}$. $\square$

**Lemma 2 (safe pruning).** Let $d_i = \delta(q, p_i)$. If $x \in D_j \cup \{p_j\}$ and $\delta(q, x) \le r$, then $[d_i - r, d_i + r] \cap \text{range}(i, j) \ne \emptyset$.

*Proof.* By the triangle inequality, $\delta(p_i, x) \le \delta(p_i, q) + \delta(q, x) \le d_i + r$ and $d_i = \delta(p_i, q) \le \delta(p_i, x) + \delta(x, q)$, so $\delta(p_i, x) \ge d_i - r$. So $\delta(p_i, x)$ lies in $[d_i - r, d_i + r]$, and by Lemma 1 it lies in range$(i, j)$. $\square$

**Theorem 1.** RANGE$(t, q, r)$ reports each $x \in S(t)$ with $\delta(q, x) \le r$ exactly once, and nothing else.

*Proof.* By induction on the height of $t$. For a leaf, line L6 tests every point of the bucket. For an internal node, every reported point passed a test $\delta \le r$ at line L6 or L8, so nothing else is reported. Let $x \in S(t)$ with $\delta(q, x) \le r$, and let $j$ be the unique index with $x \in D_j \cup \{p_j\}$ (Lemma 1). By Lemma 2, no measured split point $p_i$ removes $j$ at line L9. So $j$ stays in $P$. If $x = p_j$, then $p_j$ is measured at line L8, since $j \in P$ when the loop reaches it, and it is reported. If $x \in D_j$, line L10 calls RANGE on child$_j$, which reports $x$ by the induction hypothesis. Exactly once: the sets $D_j \cup \{p_j\}$ are disjoint, each split point is measured once, and each child is visited once. $\square$

**Lemma 3 (lower bound of line L12).** For every measured $i$ and every $x \in D_j \cup \{p_j\}$, $\delta(q, x) \ge \max(d_i - \max \text{range}(i, j),\ \min \text{range}(i, j) - d_i)$.

*Proof.* $\delta(q, x) \ge d_i - \delta(p_i, x) \ge d_i - \max \text{range}(i, j)$, and $\delta(q, x) \ge \delta(p_i, x) - d_i \ge \min \text{range}(i, j) - d_i$, by the triangle inequality and Lemma 1. $\square$

**Theorem 2.** NEAREST returns $(\delta^*, x^*)$ with $\delta^* = \min_{x \in S} \delta(q, x)$ and $x^* \in S$ at that distance.

*Proof.* The pair $(\delta^*, x^*)$ only changes to a measured point with a smaller distance, so at all times $\delta^*$ is the distance of a stored point $x^*$, and $\delta^*$ never increases. Let $y$ be a nearest point, at distance $\delta_y$. We show that $y$ is measured or that, at the moment its group is skipped, $\delta^* \le \delta_y$ already; in both cases the final $\delta^* \le \delta_y$, hence $= \delta_y$.

Follow the path of nodes from the root toward $y$. At a node, let $j$ be the index with $y \in D_j \cup \{p_j\}$. At line L11, $j$ is removed only if the interval $[d_i - \delta^*, d_i + \delta^*]$ misses range$(i, j)$ for the current $\delta^*$. If $\delta^* \ge \delta_y$ at that moment, Lemma 2 with $r = \delta^*$ and $x = y$ shows that the interval meets the range, so $j$ is not removed. So if $j$ is removed, then $\delta^* < \delta_y$, which is impossible since $\delta_y$ is the minimum distance and $\delta^*$ is a distance to a stored point. Hence $j$ is not removed at line L11, and $p_j$ is measured. If $y = p_j$, we are done. Otherwise, at line L12, group $j$ is skipped only if a lower bound of Lemma 3 for $y$ exceeds the current $\delta^*$, so $\delta_y > \delta^*$, again impossible. So the search descends into child$_j$, and by induction reaches the leaf or node where $y$ is measured. $\blacksquare$
