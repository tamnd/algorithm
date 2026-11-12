---
title: Day's algorithm returns the Robinson-Foulds distance
proves: [correctness]
status: full
---

Let $T_1$ and $T_2$ be rooted trees on the same set $X$ of $n$ taxa, in which every inner vertex has at least two children, with the children of each vertex in a fixed order. For a vertex $v$, let $L(v)$ be the set of taxa below $v$ (the leaf $v$ itself if $v$ is a leaf), and let $\mathcal{C}(T)$ be the set of the clusters $L(v)$ of the inner vertices $v$ of $T$. DAY-RF is claimed to return $|\mathcal{C}(T_1) \triangle \mathcal{C}(T_2)|$.

## Part 1: the clusters of $T_1$ are intervals

**Claim.** After line L4 for an inner vertex $v$ of $T_1$, $\{ \operatorname{num}[x] : x \in L(v) \} = \{lo[v], lo[v] + 1, \ldots, hi[v]\}$, and $lo[v] < hi[v]$.

*Proof.* A postorder walk of the subtree of $v$ visits the subtrees of the children $u_1, \ldots, u_k$ of $v$ one after another, in order, and then $v$; it never leaves the subtree of $v$ in between. Line L1 gives the leaves consecutive numbers in the order of the walk, so the leaves below $v$ get a block of consecutive numbers, made of the blocks of $u_1, \ldots, u_k$ in this order. The block starts with the block of $u_1$ and ends with the block of $u_k$. By induction in postorder (leaves have $lo = hi = \operatorname{num}$ by line L2), line L4 sets $lo[v]$ to the start of the block of $u_1$ and $hi[v]$ to the end of the block of $u_k$. Since $k \ge 2$, the block has at least two numbers. $\square$

So we write $I(v) = [lo[v], hi[v]]$ for the interval of $v$. Two facts follow.

- (F1) For inner vertices $v \ne w$, either one is a proper descendant of the other or $L(v) \cap L(w) = \emptyset$. If $w$ is a proper descendant of $v$, then $L(w) \subsetneq L(v)$, because $v$ has a child that is not an ancestor of $w$, and that child has a leaf below it.
- (F2) If $w$ is a child of $p$ and not its last child, then $hi[w] < hi[p]$. If $w$ is a child of $p$ and not its first child, then $lo[w] > lo[p]$. Both follow from the order of the blocks in the proof above, since every block is nonempty.

## Part 2: no two intervals are stored in the same row

The row of $v$ is $\operatorname{row}(v) = lo[v]$ if $v$ is the root or the last child of its parent (line L5), and $\operatorname{row}(v) = hi[v]$ otherwise (line L6).

**Claim.** For distinct inner vertices $v$ and $w$ of $T_1$, $\operatorname{row}(v) \ne \operatorname{row}(w)$.

*Proof.* Each row lies in the interval of its vertex. If $L(v) \cap L(w) = \emptyset$, the intervals are disjoint, so the rows differ. Otherwise, by (F1), one of them, say $w$, is a proper descendant of the other, and $I(w) \subsetneq I(v)$. Suppose $\operatorname{row}(v) = \operatorname{row}(w) = i$. Let $p$ be the parent of $w$; it is $v$ or a descendant of $v$, so $I(p) \subseteq I(v)$.

*Case $\operatorname{row}(v) = lo[v]$.* Then $i = lo[v]$ and $i \in I(w) \subseteq I(v)$, so $lo[w] = lo[v]$. If $\operatorname{row}(w) = hi[w]$, then $hi[w] = i = lo[w]$, which contradicts $lo[w] < hi[w]$. So $\operatorname{row}(w) = lo[w]$, which means that $w$ is the last child of $p$ ($w$ is not the root). Since $p$ has at least two children, $w$ is not its first child, and by (F2) $lo[w] > lo[p] \ge lo[v]$. This contradicts $lo[w] = lo[v]$.

*Case $\operatorname{row}(v) = hi[v]$.* Then $i = hi[v]$, and $i \in I(w) \subseteq I(v)$ gives $hi[w] = hi[v]$. If $\operatorname{row}(w) = lo[w]$, then $lo[w] = hi[w]$, a contradiction. So $\operatorname{row}(w) = hi[w]$, which means that $w$ is not the last child of $p$, and by (F2) $hi[w] < hi[p] \le hi[v]$. This contradicts $hi[w] = hi[v]$. $\square$

So no write in lines L5 and L6 overwrites another, and after line L6 the table satisfies:

**Table invariant.** $X[i] = (a, b)$ if and only if $[a, b] = I(v)$ for an inner vertex $v$ of $T_1$ with $\operatorname{row}(v) = i$. Every entry that is not *none* is the interval of a cluster of $T_1$, and the interval of each cluster of $T_1$ is in row $a$ or row $b$ of the table, where $a, b$ are its ends. Line L4 runs once per inner vertex, and distinct inner vertices have distinct clusters by (F1), so $c_1 = |\mathcal{C}(T_1)|$.

## Part 3: the test of line L10

The trees have the same taxa, so every leaf of $T_2$ has a number. By induction in postorder over $T_2$, after line L9 for an inner vertex $v$ of $T_2$, $lo[v]$ and $hi[v]$ are the smallest and the largest number of a taxon in $L(v)$, and $size[v] = |L(v)|$: the sets $L(u)$ of the children $u$ of $v$ partition $L(v)$.

**Claim.** The test of line L10 is true if and only if $L(v) \in \mathcal{C}(T_1)$.

*Proof.* Let $a = lo[v]$ and $b = hi[v]$. The numbers of the taxa are distinct and all lie in $[a, b]$, so $|L(v)| \le b - a + 1$, with equality if and only if the numbers of $L(v)$ are exactly $[a, b]$.

If $L(v) \in \mathcal{C}(T_1)$, say $L(v) = L(u)$ for an inner vertex $u$ of $T_1$, then by Part 1 the numbers of $L(v)$ are the interval $I(u)$, so it is $[a, b]$ and the first condition holds. By the table invariant, $(a, b)$ is in row $a$ or row $b$, so the second condition holds.

Conversely, if both conditions hold, the numbers of $L(v)$ are exactly $[a, b]$, and some row holds $(a, b)$, so by the table invariant $[a, b] = I(u)$ for an inner vertex $u$ of $T_1$. Then $L(u)$ and $L(v)$ have the same numbers, and the numbering is one to one, so $L(v) = L(u) \in \mathcal{C}(T_1)$. $\square$

Distinct inner vertices of $T_2$ have distinct clusters by (F1) applied to $T_2$, so $c_2 = |\mathcal{C}(T_2)|$ and $s = |\mathcal{C}(T_1) \cap \mathcal{C}(T_2)|$.

## Conclusion

$|\mathcal{C}(T_1) \triangle \mathcal{C}(T_2)| = |\mathcal{C}(T_1) \setminus \mathcal{C}(T_2)| + |\mathcal{C}(T_2) \setminus \mathcal{C}(T_1)| = (c_1 - s) + (c_2 - s)$, which line L11 returns.

## Unrooted trees

Let $U_1$ and $U_2$ be unrooted phylogenetic trees on $X$ with $n \ge 3$, and $r \in X$. Root $U_i$ at the neighbour $u_i$ of the leaf $r$ and delete $r$; call the result $T_i$, a rooted tree on $X \setminus \{r\}$. Every inner vertex of $T_i$ has at least two children: $u_i$ had degree at least 3 and lost only the edge to $r$, and every other inner vertex keeps all neighbours but its parent. Each edge of $U_i$ other than the edge at $r$ joins a vertex $v$ to its parent in $T_i$, and its split has the side $L(v)$ without $r$. So the map from the splits of $U_i$ to the sides without $r$ is a bijection from the nontrivial splits of $U_i$ onto the clusters of the inner vertices of $T_i$ other than the root, from the trivial splits $\{x\} \mid X \setminus \{x\}$ with $x \ne r$ onto the leaves of $T_i$, and from the trivial split of $r$ onto the root cluster $X \setminus \{r\}$. The trivial splits and the root are common to both trees, so $|\Sigma(U_1) \triangle \Sigma(U_2)| = |\mathcal{C}(T_1) \triangle \mathcal{C}(T_2)|$, which DAY-RF computes.
