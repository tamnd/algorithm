---
title: The sorted edges of a minimum spanning tree give the single linkage hierarchy
proves: [correctness]
status: full
---

Let $G$ be the complete graph on the points $1, \ldots, n$, with weight $D(u, v)$ on the edge $uv$. For two disjoint clusters, $\mathcal{L}(A, B) = \min_{a \in A, b \in B} D(a, b)$.

**Lemma 1 (Prim).** Lines L1 to L6 produce the $n - 1$ edges of a minimum spanning tree $T$ of $G$.

*Proof.* We show that after each round, the chosen edges are a subset of some minimum spanning tree, and that $\text{best}[v] = \min_{u \in S} D(u, v)$ for each $v \notin S$, where $S$ is the set of tree points, with the origin of $\text{best}[v]$ as the point $u$ that gives the minimum. Both hold after line L1 with $S = \{1\}$ and no edges. In a round, line L4 picks $k \notin S$ with the smallest $\text{best}[k]$, so the edge of line L5 is a lightest edge across the cut $(S, V - S)$. By the [cut property](/cut-property/), a minimum spanning tree that holds the edges so far also holds this edge, possibly after an exchange of one edge across the cut. Line L6 keeps the second statement for $S \cup \{k\}$. After $n - 1$ rounds, $S$ holds all points and the $n - 1$ edges form a spanning tree that is a subset of a minimum spanning tree, so it is one. $\square$

**Lemma 2 (minimax).** For each two points $x$ and $y$, let $\text{mx}_T(x, y)$ be the largest weight on the path from $x$ to $y$ in $T$. Then $\text{mx}_T(x, y) \le \max_i D(p_{i-1}, p_i)$ for each path $x = p_0, \ldots, p_m = y$ of $G$. In particular $\text{mx}_T(x, y) \le D(x, y)$.

*Proof.* Let $e$ be a heaviest edge on the tree path from $x$ to $y$. Removing $e$ from $T$ splits the points into two sides, with $x$ on one side and $y$ on the other. Each path from $x$ to $y$ in $G$ has an edge $f$ that crosses between the two sides. Then $T - e + f$ is a spanning tree, so $D(f) \ge D(e)$, or else $T$ was not minimum. So the path has an edge of weight at least $D(e) = \text{mx}_T(x, y)$. $\square$

**Theorem.** Lines L7 to L10 return a sequence of merges that the greedy single linkage rule can make: merge $t$ joins two current clusters $A$ and $B$ with $\mathcal{L}(A, B)$ minimal over all pairs of current clusters, at the height $\mathcal{L}(A, B)$. If all dissimilarities are distinct, it is the only greedy sequence.

*Proof.* Let the sorted tree edges be $e_1, \ldots, e_{n-1}$ with weights $w_1 \le \cdots \le w_{n-1}$. Before edge $e_t$ is replayed, the clusters are the components of the forest $F = \{e_1, \ldots, e_{t-1}\}$. The edge $e_t$ joins two different components, because the edges of $T$ form no cycle, so line L9 merges two clusters $A$ and $B$.

*The height is $\mathcal{L}(A, B)$ and it is the smallest.* Take any two points $x$ and $y$ in different components of $F$. The tree path from $x$ to $y$ leaves the component of $x$, so it has an edge $e_s$ with $s \ge t$. Then $\text{mx}_T(x, y) \ge w_s \ge w_t$, and Lemma 2 gives $D(x, y) \ge w_t$. So each pair of current clusters has $\mathcal{L} \ge w_t$. The edge $e_t = uv$ has $u \in A$, $v \in B$ and $D(u, v) = w_t$, so $\mathcal{L}(A, B) \le w_t$. Together, $\mathcal{L}(A, B) = w_t$, and no pair of clusters has a smaller value. The merge is a greedy step at height $w_t$.

*Uniqueness.* If the dissimilarities are distinct, the greedy rule has one choice at each step, so its sequence is unique, and the sequence above is it. $\square$

**Corollary 1 (cophenetic distance).** In the tree of the theorem, the height at which two points $x \ne y$ first share a cluster is

$$u^*(x, y) = \text{mx}_T(x, y) = \min_{\text{paths } x = p_0, \ldots, p_m = y} \max_i D(p_{i-1}, p_i).$$

This value does not depend on the choice of $T$ or of the order of equal weights.

*Proof.* The points $x$ and $y$ are in one component of $F = \{e_1, \ldots, e_t\}$ exactly when all edges of their tree path are among $e_1, \ldots, e_t$. The first such $t$ is the position of the heaviest edge on the path, of weight $\text{mx}_T(x, y)$. So they meet at that height. Lemma 2 shows that $\text{mx}_T(x, y)$ is at most the max over each path, and the tree path itself reaches that value. The right side does not mention $T$. $\square$

**Corollary 2 (subdominant ultrametric).** $u^*$ is the largest ultrametric $u$ with $u(x, y) \le D(x, y)$ for all $x, y$.

*Proof.* $u^*$ is an ultrametric: a path from $x$ to $y$ and a path from $y$ to $z$ join into a path from $x$ to $z$, so $u^*(x, z) \le \max(u^*(x, y), u^*(y, z))$. It is at most $D$, because the one-edge path gives $u^*(x, y) \le D(x, y)$. Let $u$ be any ultrametric with $u \le D$, and let $x = p_0, \ldots, p_m = y$ be a path with $\max_i D(p_{i-1}, p_i) = u^*(x, y)$. Apply the ultrametric inequality $m - 1$ times: $u(x, y) \le \max_i u(p_{i-1}, p_i) \le \max_i D(p_{i-1}, p_i) = u^*(x, y)$. $\square$

**Corollary 3 (cuts).** For a threshold $h$, the clusters of the merges of height at most $h$ are the components of the graph of all pairs with $D(x, y) \le h$.

*Proof.* By Corollary 1, $x$ and $y$ share a cluster at height $h$ exactly when some path joins them with all weights at most $h$, which is the definition of a component of that graph. $\square$

**Running time.** Lines L4 and L6 scan $O(n)$ points in each of the $n - 1$ rounds, which is $\Theta(n^2)$. Line L7 sorts $n - 1$ edges in $O(n \log n)$ time. The $n - 1$ unions and $2(n - 1)$ finds of lines L8 and L9 take $O(n\,\alpha(n))$ time with union by size and path compression. The arrays best, origin, the edge list and the disjoint sets use $O(n)$ memory.
