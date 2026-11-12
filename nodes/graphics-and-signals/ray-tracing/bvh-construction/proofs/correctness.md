---
title: The binned SAH build ends with a valid BVH and takes the cheapest binned split at each node
proves: [correctness]
status: full
---

Let $P$ be a nonempty set of $n$ primitives, each with a box $b(p)$ and a centroid $c(p)$. For a set $S$ let $B(S)$ be the union of the boxes of $S$, $A$ the surface area, and $C(S)$ the box of the centroids. For an axis $a$ with $C_a^- < C_a^+$, the bin of $p$ is $k_a(p) = \min(K - 1, \lfloor K (c_a(p) - C_a^-)/(C_a^+ - C_a^-) \rfloor)$, an integer in $[0, K - 1]$ since $C_a^- \le c_a(p) \le C_a^+$. The candidate $(a, j)$ with $1 \le j \le K - 1$ is the partition $L = \{p : k_a(p) < j\}$, $R = S \setminus L$; it is *valid* if both parts are nonempty.

**Lemma 1 (a valid candidate exists).** If $|S| \ge 2$ and $C(S)$ is not a point, line L8 finds a valid candidate.

*Proof.* Take an axis $a$ with $C_a^- < C_a^+$. A primitive with $c_a = C_a^-$ has bin 0, and one with $c_a = C_a^+$ has bin $\min(K - 1, K) = K - 1 \ge 1$. So $(a, 1)$ has both parts nonempty. $\square$

**Lemma 2 (the sweep is exact).** For each axis and each $j$, line L7 computes $A(B(L)) |L| + A(B(R)) |R|$ for the candidate $(a, j)$, and line L8 keeps the least value over all valid candidates.

*Proof.* Line L5 puts each primitive of $S$ into exactly one bin, $k_a(p)$, and stores the union of the boxes and the count per bin. $L$ is the union of the bins $0, \ldots, j - 1$ and $R$ of the bins $j, \ldots, K - 1$. Union of boxes is associative and commutative, so the box of a union of bins is the union of their boxes. Line L6 builds, for $j = K - 1$ down to 1, the union and the count of the bins $j, \ldots, K - 1$ by adding one bin at a time, and line L7 does the same from the left. So both sums are exact for each $j$. Line L8 keeps a candidate only if it is valid and strictly cheaper than the best so far, so at the end it holds a least one, the first in the order of axes and then of $j$. $\square$

**Lemma 3 (termination and the partition of refs).** Each task pops a contiguous range of refs that is a nonempty set $S$, and the two child tasks get ranges that split it into two nonempty parts. The build ends after at most $2n - 1$ tasks.

*Proof.* The root task is the whole range. A split at line L10 writes $L$ and then $R$ into the range of $S$ and makes two tasks for those subranges. By Lemmas 1 and 2 the chosen candidate is valid, so both are nonempty and smaller than $S$. The tasks form a binary tree whose leaves are disjoint nonempty ranges, so it has at most $n$ leaves and $2n - 1$ nodes. $\square$

**Theorem.** The build returns a binary tree in which (i) each primitive is in exactly one leaf, (ii) the box of each node is $B(S)$ for the set $S$ of primitives below it, so it contains each of them, and (iii) each inner node is split by a candidate of least binned SAH cost $c_t + c_i (A(B(L))|L| + A(B(R))|R|)/A(B(S))$ among all valid candidates of that node.

*Proof.* (i) follows from Lemma 3: the ranges of the leaves partition the refs, and refs is a permutation of $P$, since line L10 only reorders a range. (ii) Line L3 computes the box of the node as the union of the boxes of the refs in its range, which are the primitives below it. (iii) The positive factor $1/A(B(S))$ and the constant $c_t$ do not change the order of the candidates, so the least sum of Lemma 2 gives the least cost. A node becomes a leaf only at line L4, when it cannot be split, or at line L9, when the leaf cost $c_i |S|$ is not more than the cost of that split and $|S|$ is at most the leaf size. $\blacksquare$

**Remark.** The theorem is about each split. The tree is greedy: each split is the best for that node under the assumption that its children become leaves, and the total SAH cost of the tree need not be the least among all trees. Only the containment in (ii) and the cover in (i) matter for the correctness of [BVH traversal](/bvh-traversal/).
