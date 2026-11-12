---
title: Day's cluster table computes the strict consensus tree
proves: [correctness]
status: full
---

**Setting.** $T_1, \ldots, T_k$ are rooted trees on the same leaf set $X$, $|X| = n \ge 2$. No internal node has exactly one child. The cluster of a node $v$, written $C(v)$, is the set of leaves below $v$. $\mathcal{C}(T)$ is the set of clusters of the internal nodes of $T$. The strict consensus is the tree $S$ with $\mathcal{C}(S) = \bigcap_j \mathcal{C}(T_j)$. We prove three claims: such a tree exists and is unique, the procedure STRICT-CONSENSUS returns it, and it does so in $O(kn)$ time.

**Fact 1 (clusters form a laminar family).** For two nodes $u, v$ of one tree, $C(u)$ and $C(v)$ are disjoint or one contains the other. If no node has one child, distinct internal nodes have distinct clusters.

*Proof.* If $u$ is an ancestor of $v$, then $C(v) \subseteq C(u)$. If neither is an ancestor of the other, no leaf is below both, so the clusters are disjoint. If $u$ is a proper ancestor of an internal node $v$, then $u$ has a child $u'$ that is not on the path to $v$, and the leaves below $u'$ are in $C(u) \setminus C(v)$. $\square$

**Lemma 1 (existence and uniqueness).** Let $\mathcal{F}$ be a laminar family of subsets of $X$ that contains $X$, where each member has at least two elements. There is exactly one rooted tree $S$ without nodes of one child such that $\mathcal{C}(S) = \mathcal{F}$. If $\mathcal{F} \subseteq \mathcal{C}(T)$ for a tree $T$, then $S$ is the tree that we get from $T$ when we contract every edge $(p, v)$ with $v$ internal and $C(v) \notin \mathcal{F}$.

*Proof.* Take one node for each member of $\mathcal{F}$ and one leaf for each element of $X$. Make the parent of a member $F \ne X$, or of a leaf $x$, the smallest member of $\mathcal{F}$ that strictly contains it. This member exists, because $X$ contains everything, and it is unique, because two members that both contain a given set intersect, so by laminarity one of them is inside the other. Every member $F$ has two or more elements, and its children cover $F$. A child that is a member is a proper subset, so $F$ has at least two children. So the result is a tree $S$ with $\mathcal{C}(S) = \mathcal{F}$. The tree is unique, because the parent of each node is forced: in any such tree, the parent of the node of $F$ has the smallest cluster that strictly contains $F$. Now contract the edges of $T$ as the lemma says. A contraction does not change the cluster of any node that remains, and it removes exactly one cluster. So the result has the cluster set $\mathcal{F}$. A node of the result has at least as many children as it had in $T$, so it has at least two. By uniqueness, the result is $S$. $\square$

The family $\bigcap_j \mathcal{C}(T_j)$ is a subfamily of $\mathcal{C}(T_1)$, so it is laminar, it contains $X$, and Lemma 1 applies. This is the reason why strict consensus is always defined.

**Lemma 2 (clusters of $T_1$ are intervals).** Lines L1 and L2 number the leaves of $T_1$ in the order in which a depth-first traversal meets them. For each node $v$ of $T_1$, $C(v)$ is the set of ranks $\{lo(v), \ldots, hi(v)\}$, where $lo(v)$ is the rank of the leftmost leaf below $v$ and $hi(v)$ is the rank of the rightmost leaf below $v$.

*Proof.* The traversal visits all leaves below $v$ in one run, without a leaf from outside between them. So their ranks are consecutive. Line L2 computes $lo(v)$ from the first child and $hi(v)$ from the last child, which is the same by induction on the postorder. $\square$

**Lemma 3 (one entry per row).** Line L3 stores the interval of each internal node $v$ of $T_1$ in row $hi(v)$ if $v$ is the root or the leftmost child of its parent, and in row $lo(v)$ otherwise. No two internal nodes use the same row.

*Proof.* Suppose that the distinct internal nodes $v$ and $w$ use the same row $i$. By Fact 1 the clusters of $v$ and $w$ are different and laminar. Both contain the rank $i$, so they are nested. Say $C(w) \subsetneq C(v)$, so $w$ is a proper descendant of $v$ and is not the root.

Case 1: both use the right end, so $hi(w) = hi(v) = i$. Let $p$ be the parent of $w$. Then $p$ is $v$ or a descendant of $v$, so $hi(p) \le hi(v) = hi(w) \le hi(p)$, and $w$ holds the rightmost leaf of $p$. So $w$ is the last child of $p$. As $p$ has two or more children, $w$ is not the leftmost child. So $w$ uses the left end, which is a contradiction.

Case 2: both use the left end, so $lo(w) = lo(v) = i$. The same argument with left and right exchanged shows that $w$ is the first child of its parent. So $w$ uses the right end, which is a contradiction.

Case 3: the two nodes use different ends. If $w$ uses its left end and $v$ its right end, then $lo(w) = i = hi(v) \ge hi(w)$, so $C(w)$ has one element. If $w$ uses its right end and $v$ its left end, then $hi(w) = i = lo(v) \le lo(w)$, and again $C(w)$ has one element. An internal node has at least two leaves below it, which is a contradiction. $\square$

**Lemma 4 (the membership test).** Let $C$ be the cluster of an internal node of $T_j$, and let $a$, $b$ and $s$ be the smallest rank, the largest rank and the size of $C$. Then $C \in \mathcal{C}(T_1)$ if and only if $b - a + 1 = s$ and row $a$ or row $b$ of the table holds the pair $(a, b)$.

*Proof.* The ranks are distinct, so $C$ is the interval $\{a, \ldots, b\}$ if and only if $b - a + 1 = s$. If $C \in \mathcal{C}(T_1)$, then by Lemma 2, $C$ is that interval and is the cluster of an internal node $v$ of $T_1$ with $lo(v) = a$ and $hi(v) = b$. Line L3 stored $(a, b)$ in row $a$ or row $b$. Conversely, a pair $(a, b)$ in the table is the interval of an internal node of $T_1$, and that interval is the cluster $C$. $\square$

**Theorem.** STRICT-CONSENSUS returns the strict consensus tree.

*Proof.* By Lemma 3, each internal node $v$ of $T_1$ has its own row $r(v)$, and line L4 sets its counter to 1. Fix a tree $T_j$ with $j \ge 2$. Its internal nodes have distinct clusters by Fact 1. By Lemma 4, line L7 increments the counter of row $r(v)$ exactly when some internal node of $T_j$ has the cluster $C(v)$, and this happens at most once for each $T_j$. Line L7 never increments a row that holds no entry, because the test needs the pair $(a, b)$ in that row. So after the loop, the counter of $r(v)$ is the number of trees that contain $C(v)$, and it equals $k$ exactly when $C(v) \in \bigcap_j \mathcal{C}(T_j)$. Line L8 keeps these nodes and the root. Line L9 contracts the other internal edges of $T_1$, and by Lemma 1 the result is the strict consensus tree. $\square$

**Running time.** Each tree has $n$ leaves and fewer than $n$ internal nodes, because each internal node has at least two children. Lines L1 to L4 visit each node of $T_1$ a constant number of times, and the work at a node is proportional to its number of children. So they take $O(n)$ time. For each other tree, line L6 computes the minimum, the maximum and the size of every cluster from the values of the children, in time $O(n)$ for the whole tree, and line L7 takes $O(1)$ time per node. So the loop takes $O(kn)$ time. Line L9 is one more traversal of $T_1$. The total is $O(kn)$ time. The table, the counters and the arrays for the current tree take $O(n)$ space. The input itself takes $O(kn)$ space. $\blacksquare$
