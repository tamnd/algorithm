---
title: The network stays acyclic, the counts are right, and the switchings give exactly the displayed trees
proves: [correctness]
status: full
---

**Setting.** The structure stores a finite directed graph $N = (V, E)$ without parallel arcs, by the lists $\mathrm{children}(v)$ and $\mathrm{parents}(v)$, and a label for some vertices. The in-degree of $v$ is $|\mathrm{parents}(v)|$. A *root* is a vertex of in-degree 0, a *reticulation* is a vertex of in-degree 2 or more, and a *sink* is a vertex of out-degree 0. In a valid network, there is one root $\rho$, the sinks are exactly the labeled vertices, and the labels are distinct. $X$ is the set of labels.

**Lemma 1 (acyclic invariant).** After every sequence of operations, $N$ has no directed cycle.

*Proof.* The empty graph has no cycle, and ADD-VERTEX adds a vertex without arcs. Suppose $N$ has no cycle, and ADD-ARC$(u, v)$ adds $u \to v$. A cycle in the new graph must use the new arc, so it is $u \to v$ followed by a path from $v$ to $u$ in $N$. Line L1 tests exactly whether such a path exists, by a depth-first search from $v$ (the path of length 0 covers $u = v$), and it rejects the arc if it does. So line L2 runs only when the new graph has no cycle. $\square$

**Lemma 2 (reticulation number).** $\sum_{v \in V,\ \mathrm{indeg}(v) > 0} (\mathrm{indeg}(v) - 1) = |E| - |V| + r$, where $r$ is the number of roots. For a valid network, $r = 1$ and the value of line L3 is $|E| - |V| + 1$.

*Proof.* Each arc has one head, so $\sum_v \mathrm{indeg}(v) = |E|$. The sum on the left takes this total and subtracts 1 for each of the $|V| - r$ vertices with positive in-degree. $\square$

**Lemma 3 (tree-child test).** Lines L4 and L5 return true if and only if every vertex that is not a sink has a child that is not a reticulation. This holds if and only if every vertex has a directed path to a sink on which every vertex after the first is not a reticulation.

*Proof.* Line L4 looks at every vertex with at least one child and returns false exactly when all its children have in-degree 2 or more. That is the first claim. For the second, suppose the first condition holds and start at any vertex. While the current vertex is not a sink, move to a child that is not a reticulation. By Lemma 1 no vertex repeats, so the walk ends at a sink, and it is a path of the required kind. Conversely, if a vertex $v$ that is not a sink has only reticulations as children, every path from $v$ of length at least 1 has a reticulation as its second vertex, and the path of length 0 does not end at a sink. $\square$

**Definitions for the displayed trees.** A *switching* of a valid network is the subgraph $W$ that keeps all vertices, the one arc into each vertex of in-degree 1, and exactly one chosen arc into each reticulation. A rooted tree on $X$ is identified with its set of clusters, the nonempty sets of labels below its vertices. We say that $N$ *displays* the tree $T$ if $N$ has a subgraph $S$ that contains $\rho$ and every labeled vertex, in which every vertex other than $\rho$ has exactly one parent and is reached from $\rho$, and whose nonempty clusters are the clusters of $T$. This is the usual definition: $T$ comes from $S$ by removing the parts without labels and suppressing the vertices with one child.

**Lemma 4.** Every switching $W$ is a tree rooted at $\rho$ with all vertices of $N$. Its clusters are nested or disjoint, they include $X$ and every singleton $\{x\}$, so they are the clusters of a rooted tree on $X$.

*Proof.* In $W$, every vertex other than $\rho$ has exactly one parent, and $\rho$ has none. Follow parents from any vertex. By Lemma 1 no vertex repeats, so the walk stops, and it can only stop at $\rho$. So $\rho$ reaches every vertex, and the path from $\rho$ to each vertex is unique, because each step back is forced. Two clusters $C(v)$ and $C(w)$ with a common label $x$ have $v$ and $w$ on the unique path from $\rho$ to $x$, so one of $v, w$ is an ancestor of the other, and the clusters are nested. $C(\rho) = X$, because $\rho$ reaches every leaf, and $C(x) = \{x\}$ for each leaf, because a sink has no children. $\square$

**Theorem.** DISPLAYED-TREES (lines L6 to L9) returns exactly the set of trees displayed by $N$, and it returns at most $\prod_r \mathrm{indeg}(r)$ trees, which is $2^h$ for a network whose reticulations have in-degree 2.

*Proof.* Line L6 runs over all choices of one parent for each reticulation, line L7 builds the child lists of the switching $W$ for this choice, and line L8 computes its nonempty clusters in postorder. Postorder is well defined by Lemma 4, and the cluster of $v$ is its own label, if any, together with the clusters of its children, which is the set of labels below $v$.

*Each result is displayed.* $W$ contains $\rho$ and every vertex, and by Lemma 4 it satisfies the conditions on $S$. So the tree of $W$ is displayed.

*Each displayed tree is a result.* Let $S$ witness that $N$ displays $T$. Choose a switching $W$ as follows: for a reticulation in $S$, choose its parent in $S$, and for any other reticulation choose any parent. A vertex of $S$ other than $\rho$ has one parent in $S$, and that arc is in $W$, because $W$ keeps the only arc into a vertex of in-degree 1 and the chosen arc into a reticulation. So $S$ is a subgraph of $W$, and every vertex of $S$ has the same parent in $S$ and in $W$. Let $x$ be a label. The path from $\rho$ to $x$ in $S$ follows parents from $x$, so it is also the unique path from $\rho$ to $x$ in $W$. Now a vertex $v$ has $x$ in its cluster in $W$ exactly when $v$ is on this path, and the same holds in $S$ for $v \in S$. So $v \in S$ has the same cluster in $S$ and in $W$. A vertex $v \notin S$ is on no such path, so its cluster in $W$ is empty. So $S$ and $W$ have the same nonempty clusters, and $T$ is the tree of $W$.

Line L9 returns the set of trees, so trees from different switchings that are equal are counted once. The number of switchings is $\prod_r \mathrm{indeg}(r)$. $\blacksquare$
