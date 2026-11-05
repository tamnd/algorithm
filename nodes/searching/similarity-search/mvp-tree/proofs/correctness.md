---
title: The MVP-tree range search reports exactly the objects within the radius, and the tree has logarithmic height
proves: [correctness]
status: full
---

We use the names of the pseudocode on the page. $(U, d)$ is a metric space, $P$ a finite set of $n$ objects, $m \ge 2$, $k \ge 1$ and $p \ge 0$. For a node $N$, $\mathrm{obj}(N)$ is the set of objects stored in its subtree, as vantage points or as entries.

**Lemma 1 (partition).** BUILD$(S)$ stores every object of $S$ exactly once in its subtree.

*Proof.* By induction on $|S|$. A leaf stores $v_1$, $v_2$ and the others as entries (with $v_2$ absent when $|S| = 1$ and nothing when $S$ is empty). At an internal node, $|S| \ge k + 3 \ge 4$; $v_1$ and $v_2$ are stored at the node, and the subrings partition the remaining objects, each of size less than $|S|$. $\square$

**Lemma 2 (intervals and paths).** (a) At an internal node, every $x \in \mathrm{obj}(\text{child } (i, j))$ has $d(x, v_1) \in I_i$ and $d(x, v_2) \in J_{i,j}$. (b) For every entry $x$ of a leaf at depth $\delta$ (the root at depth 0), with internal ancestors $N_0, \ldots, N_{\delta - 1}$ from the root, $\mathrm{PATH}(x)$ is the first $\min(p, 2\delta)$ elements of the list $d(x, N_0.v_1), d(x, N_0.v_2), \ldots, d(x, N_{\delta-1}.v_2)$. (c) When RANGE is called on that leaf, $Q$ is the first $\min(p, 2\delta)$ elements of the list $d(q, N_0.v_1), d(q, N_0.v_2), \ldots, d(q, N_{\delta-1}.v_2)$.

*Proof.* (a) Line L4 takes $I_i$ as the least and greatest value of $d(\cdot, v_1)$ over ring $i$, and $v_2$ is removed from a ring after that, so the remaining objects of ring $i$ still lie in $I_i$; line L6 does the same for $J_{i,j}$, and the objects of child $(i, j)$ are exactly subring $(i, j)$. (b) $x$ passes through each internal ancestor once, where line L3 appends $d(x, v_1)$ and line L6 appends $d(x, v_2)$, each only while the list is shorter than $p$; nothing else appends to it, and the leaf stores the list unchanged. (c) RANGE starts with $Q$ empty, and line L15 appends $t_1 = d(q, v_1)$ and $t_2 = d(q, v_2)$ at each internal node on the way down, and cuts after $p$; the descent to the leaf passes through the same ancestors. $\square$

**Theorem 1 (range).** RANGE$(\text{root}, q, r, ())$ reports exactly the objects $x \in P$ with $d(q, x) \le r$, each once.

*Proof.* By Lemma 1 every object is a vantage point or an entry of one node, so it is reported at most once. A reported object passed an exact test $d(q, \cdot) \le r$ in line L9, L13 or L14, so it is an answer. Let $x$ be an answer, and suppose it is not reported. Then one of three things happened.

- RANGE skipped a child $(i, j)$ of an internal ancestor $N$ of the node of $x$. If the reason was $I_i$, then $I_i = [a, b]$ with $t_1 + r < a$ or $t_1 - r > b$. By Lemma 2(a), $d(x, v_1) \in [a, b]$. In the first case $d(q, x) \ge d(x, v_1) - d(q, v_1) \ge a - t_1 > r$; in the second, $d(q, x) \ge d(q, v_1) - d(x, v_1) \ge t_1 - b > r$. The case of $J_{i,j}$ and $v_2$ is the same. (An empty ring has an empty interval and no object.)
- Line L11 skipped the entry $x$: then $|d(q, u) - d(x, u)| > r$ for $u = v_1$ or $u = v_2$ of the leaf.
- Line L12 skipped it: then by Lemma 2(b) and 2(c), $Q[i]$ and $\mathrm{PATH}(x)[i]$ are the distances from $q$ and from $x$ to the same vantage point $u$, and $|d(q, u) - d(x, u)| > r$.

In the last two cases the triangle inequality gives $d(q, x) \ge |d(q, u) - d(x, u)| > r$. Each case contradicts $d(q, x) \le r$. $\square$

**Lemma 3 (height and build cost).** Every node at depth $\delta$ holds at most $\lceil n / m^{2\delta} \rceil$ objects. Internal nodes exist only at depths $\delta < \log_{m^2} n$, so the tree has at most $\lceil \log_{m^2} n \rceil + 1$ levels, and BUILD makes at most $2n$ evaluations per level.

*Proof.* A split by rank of $s$ objects into $m$ parts gives parts of size at most $\lceil s/m \rceil$. A child of a node with $s$ objects gets at most $\lceil \lceil s/m \rceil / m \rceil = \lceil s/m^2 \rceil$ objects, and the nested ceilings give $\lceil n/m^{2\delta} \rceil$ at depth $\delta$. An internal node has at least 4 objects, so $n/m^{2\delta} > 3 \ge 1$ and $\delta < \log_{m^2} n$. Each object at a node costs at most two evaluations there (lines L3 and L6, or the two of line L2), and the nodes at one depth hold disjoint sets. $\blacksquare$
