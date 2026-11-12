---
title: The dendrogram operations return the cophenetic matrix and the cuts
proves: [correctness]
status: full
---

The tree has leaves $1, \ldots, n$ and internal nodes $n + 1, \ldots, 2n - 1$, where node $n + t$ is made by merge $t$ from two nodes with smaller numbers. Each node except the root $2n - 1$ has one parent. We write $L(v)$ for the leaf set of node $v$ and $\text{lca}(i, j)$ for the lowest common ancestor of two leaves.

**Fact 1.** For distinct leaves $i$ and $j$, there is exactly one internal node $v$ such that $i$ and $j$ are below different children of $v$, and $v = \text{lca}(i, j)$.

*Proof.* The ancestors of a leaf form one path to the root. The common ancestors of $i$ and $j$ are the nodes on both paths, and the lowest of them is $\text{lca}(i, j)$. It is not a leaf because $i \ne j$. If $i$ and $j$ were below the same child $c$ of it, then $c$ would be a lower common ancestor. So they are below different children. At a node $u$ above the lca, both leaves are below the same child, the one on the path to the lca. At a node that is not a common ancestor, at most one of the two leaves is below it. $\square$

**Lemma 1 (COPHENETIC).** After line L7, $C[i, j] = h(\text{lca}(i, j))$ for all distinct leaves $i, j$.

*Proof.* We show this invariant for the loop of line L2: before node $v$ is handled, $\text{below}[u] = L(u)$ for each node $u < v$. It is true at the start by line L1. Line L6 sets $\text{below}[v] = \text{below}[a] \cup \text{below}[b] = L(a) \cup L(b) = L(v)$, because $a, b < v$. So in the step for $v$, lines L4 and L5 write $h(v)$ to $C[i, j]$ for exactly the pairs with $i \in L(a)$ and $j \in L(b)$, that is, the pairs below different children of $v$. By Fact 1, each pair of distinct leaves is written in exactly one step, the step of its lca, and it gets the height of its lca. $\square$

**Lemma 2 (CUT-K).** For $1 \le k \le n$, the set $R$ at line L12 is the set of roots of the forest that the first $n - k$ merges make. So CUT-K returns the clustering after $n - k$ merges.

*Proof.* Let $F_m$ be the forest of the first $m$ merges. Its roots are the leaves and the nodes $n + 1, \ldots, n + m$ that have no parent among the nodes $n + 1, \ldots, n + m$. We show that while $|R| = q$, the set $R$ is the root set of $F_{n - q}$. At line L8, $R = \{2n - 1\}$, which is the root set of $F_{n-1}$. Assume that $R$ is the root set of $F_m$ with $m = n - q \ge 1$. The node $n + m$ is a root of $F_m$, because no merge of $F_m$ comes after it. Each node of $R$ has a number of at most $n + m$. So line L10 picks $v = n + m$. The forest $F_{m-1}$ is $F_m$ without the node $v$, so its roots are the roots of $F_m$ other than $v$, and the two children of $v$. That is the new $R$ of line L11, with $|R| = q + 1$. The loop stops at $|R| = k$, with the root set of $F_{n - k}$. Each tree of a forest is a cluster, so the leaf sets of the roots are the clusters. $\square$

**Lemma 3 (CUT-HEIGHT).** Let the tree be monotone and $t \ge 0$. CUT-HEIGHT returns the classes of the relation $C(i, j) \le t$ on the leaves, where $C(i, i) = 0$.

*Proof.* The walk visits each node on a path from the root until it meets a leaf or a node of height at most $t$, and adds that node to $R$. Each leaf has a unique path from the root, and the walk stops at the first node on this path that is a leaf or has height at most $t$. So each leaf is below exactly one node of $R$, and $R$ is a partition of the leaves.

Let $i$ and $j$ be below the same node $r \in R$. If $r$ is a leaf, then $i = j$. If not, $h(r) \le t$, and $\text{lca}(i, j)$ is $r$ or a node below $r$. Heights do not increase from a parent to a child, so $C(i, j) = h(\text{lca}(i, j)) \le h(r) \le t$.

Let $C(i, j) \le t$ with $i \ne j$, and let $w = \text{lca}(i, j)$, so $h(w) \le t$. The walk from the root toward $i$ passes through $w$, and it stops at $w$ or earlier. If it stops at a node $r$ above $w$ or at $w$, both $i$ and $j$ are below $r$. It cannot stop below $w$, because $w$ itself meets the stop rule. So $i$ and $j$ are in the same class. $\square$

**Corollary.** For a monotone tree whose merges come in non-decreasing order of height, CUT-HEIGHT$(t)$ is the clustering after all merges of height at most $t$. Lemma 2 and Lemma 3 then agree: if the merge heights are $h_1 \le \cdots \le h_{n-1}$ and $h_{n-k} < h_{n-k+1}$, then CUT-K$(k)$ = CUT-HEIGHT$(h_{n-k})$.

*Proof.* The merges of height at most $t$ are a prefix of the list, say the first $m$. By Lemma 3, two leaves are in the same class when their lca has height at most $t$, that is, when their lca is one of the first $m$ merges. That holds when they are in the same tree of $F_m$. $\square$

**Lemma 4 (ultrametric).** For a monotone tree, $C(x, z) \le \max(C(x, y), C(y, z))$ for all leaves $x, y, z$.

*Proof.* If two of the three leaves are equal, the claim is direct. Otherwise let $u = \text{lca}(x, y)$ and $w = \text{lca}(y, z)$. Both are ancestors of $y$, so they are on one path, and one is an ancestor of the other. Say that $u$ is $w$ or an ancestor of $w$. Then $x$ and $z$ are both below $u$, so $\text{lca}(x, z)$ is $u$ or below $u$, and monotonicity gives $C(x, z) \le h(u) = C(x, y) \le \max(C(x, y), C(y, z))$. The other case is symmetric. $\square$

**Lemma 5 (cost by nodes).** For weights $w_{ij} \ge 0$, $\sum_{v} |L(v)| \cdot \sum_{i \in L(\text{left}(v)),\ j \in L(\text{right}(v))} w_{ij} = \sum_{i < j} w_{ij}\, |L(\text{lca}(i, j))|$, where $v$ runs over the internal nodes. This is the form of [Dasgupta's cost](/dasgupta-cost/) that the code computes.

*Proof.* By Fact 1, each pair $\{i, j\}$ appears in the inner sum of exactly one node, its lca, with the factor $|L(\text{lca}(i, j))|$. $\square$

**Running time.** Line L5 runs one time for each pair of leaves, so $n(n-1)/2$ times. Line L6 builds a list of size $|L(v)|$ for each $v$. The sizes add up to at most $n(n-1)/2 + n$ over all nodes, because the leaf $i$ is counted once for each of its ancestors and a chain gives the worst case. So COPHENETIC takes $\Theta(n^2)$ time. CUT-K runs $k - 1$ steps, each one a maximum over at most $k$ nodes, and then lists the leaves in $O(n)$ time. CUT-HEIGHT visits each node at most one time.
