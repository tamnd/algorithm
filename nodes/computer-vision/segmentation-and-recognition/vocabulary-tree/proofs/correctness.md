---
title: The vocabulary tree has depth at most L and branch factor at most k, quantizes to exactly one leaf, and its inverted file score is the L1 distance
proves: [correctness]
status: full
---

We use the notation of the page. Distances are Euclidean, and "nearest child" uses the tie rule of line L8 (the smaller index wins).

**Theorem 1 (shape).** BUILD stops. In the tree it returns, every leaf has depth at most $L$ and every inner node has at most $k$ children, so there are at most $k^L$ leaves. QUANTIZE stops at a leaf after at most $L$ steps of line L8.

*Proof.* A call at depth $L$ returns a leaf in line L2, and each recursive call in line L4 has depth one more than its caller, so no call has depth more than $L$. Each call makes at most $k$ recursive calls, since line L3 makes $k$ groups and line L4 keeps only the nonempty ones; each k-means run stops after a bounded number of iterations. So the recursion tree is finite, and BUILD stops. A tree of depth at most $L$ with at most $k$ children per node has at most $k^L$ leaves, by induction on $L$. Every inner node has at least one child, so line L8 always finds a child, the depth grows by one at each step, and the loop stops at a leaf after at most $L$ steps. $\square$

**Theorem 2 (nested cells).** For every $x \in \mathbb{R}^D$, QUANTIZE returns one leaf $\ell(x)$. For a node $i$, let $S_i$ be the set of $x$ whose path passes through $i$. Then $S_{\text{root}} = \mathbb{R}^D$, and for each inner node $i$ the sets $S_j$ of its children $j$ are disjoint and their union is $S_i$. So the leaf cells $S_\ell$ split $\mathbb{R}^D$.

*Proof.* QUANTIZE is deterministic, so each $x$ has one path and one leaf. Every path starts at the root. If the path of $x$ passes through an inner node $i$, line L8 picks exactly one child of $i$ (the tie rule makes the choice unique), so $x$ is in exactly one $S_j$. Conversely, $S_j \subseteq S_i$ for every child $j$ of $i$, since a path reaches $j$ only from $i$. $\square$

**Remark (the cell is not the Voronoi cell).** With the tree of the example of the page, $x = 4.6$ is in $S_8$, but its nearest leaf center is $4$. So $S_\ell$ is not in general the set of points nearest to the center of $\ell$ among all leaf centers, and the error of greedy descent has no bound in terms of the distance to the nearest leaf center. Greedy descent is a heuristic for nearest center search.

**Theorem 3 (counts nest).** For an image with descriptors $x_1, \ldots, x_m$, let $m_i = \#\{t : x_t \in S_i\}$. Then $m_{\text{root}} = m$, and $m_i = \sum_j m_j$ over the children $j$ of each inner node $i$. If every database image has a descriptor in $S_i$, then $w_i = 0$.

*Proof.* The first two claims follow from Theorem 2, since the $S_j$ split $S_i$. If all $N$ images use node $i$, then $N_i = N$ and $w_i = \ln 1 = 0$. $\square$

**Theorem 4 (the scoring formula).** Let $q, d \in \mathbb{R}^n$ with $q_i, d_i \ge 0$ and $\sum_i q_i = \sum_i d_i = 1$. Then
$$\lVert q - d \rVert_1 = 2 + \sum_{i \in C} \big( |q_i - d_i| - q_i - d_i \big) = 2 - 2 \sum_i \min(q_i, d_i),$$
where $C = \{i : q_i > 0 \text{ and } d_i > 0\}$.

*Proof.* Split the indices into $C$, the set $Q$ where only $q_i > 0$, the set $P$ where only $d_i > 0$, and the rest, where both are 0. Then
$$\lVert q - d \rVert_1 = \sum_{C} |q_i - d_i| + \sum_{Q} q_i + \sum_{P} d_i.$$
Since $\sum_Q q_i = 1 - \sum_C q_i$ and $\sum_P d_i = 1 - \sum_C d_i$, this is $2 + \sum_C (|q_i - d_i| - q_i - d_i)$. For $a, b \ge 0$, $|a - b| - a - b = -2 \min(a, b)$, and $\min(q_i, d_i) = 0$ outside $C$, which gives the last form. $\square$

**Corollary (the inverted files compute the score).** Let the inverted file of node $i$ list each database image $d$ with $d_i > 0$, with the value $d_i$. The query loop sets $\mathrm{acc}(d) = 0$ for all $d$, and for each node $i$ with $q_i > 0$ and each $(d, d_i)$ in the file of $i$ adds $|q_i - d_i| - q_i - d_i$. For each $d$, the pairs it visits are exactly the indices $i \in C$, each once, so $\mathrm{acc}(d) = \sum_{i \in C} (|q_i - d_i| - q_i - d_i)$, and $2 + \mathrm{acc}(d) = \lVert q - d \rVert_1$ by Theorem 4. If $q = 0$ or $d = 0$ (all its nodes have weight 0), the code returns $\lVert q \rVert_1 + \lVert d \rVert_1 + \mathrm{acc}(d)$, with $\mathrm{acc}(d) = 0$, which is again $\lVert q - d \rVert_1$. $\square$

**What is not claimed.** Nothing here says that the leaf of a descriptor is its nearest leaf center, that the k-means splits are good, or that a small L1 distance means that two images show the same object. Those are heuristics, and the ranking quality is a benchmark result.
