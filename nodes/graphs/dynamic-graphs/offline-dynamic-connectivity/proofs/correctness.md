---
title: The walk over the segment tree answers every query on the graph of its time
proves: [correctness]
status: full
---

Let $G_t$ be the multigraph of the edges present after the operations $o_0, \ldots, o_t$. For a node $x$ of the segment tree, let $R(x) \subseteq [0, T)$ be its range, let $L(x)$ be its list of edge copies, and let $\mathrm{anc}(x)$ be the set of nodes on the path from the root to $x$, including $x$.

**Lemma 1 (lifetimes).** A copy of an edge with lifetime $[a, d)$ is present in $G_t$ if and only if $a \le t < d$.

*Proof.* Line L1 pairs each removal of $\{u, v\}$ with the latest open start time of a copy of $\{u, v\}$, and a copy that is never removed gets the end $T$. The copy is inserted by $o_a$, so it is in $G_t$ for $t \ge a$, and it is deleted by $o_d$, so it is not in $G_t$ for $t \ge d$. Since all copies of one edge are equal, the choice of which copy a removal deletes does not change the multigraph $G_t$. $\square$

**Lemma 2 (canonical nodes).** For a lifetime $I = [a, d)$ and a leaf $\ell$ of time $t$, exactly one canonical node of $I$ is in $\mathrm{anc}(\ell)$ if $t \in I$, and none is if $t \notin I$.

*Proof.* Line L2 puts the copy at a set $C$ of nodes whose ranges are pairwise disjoint and have the union $I$; this is the property of the standard segment tree decomposition. The ranges of the nodes in $\mathrm{anc}(\ell)$ are exactly the ranges of the tree that contain $t$. If $t \in I$, some node of $C$ has a range that contains $t$, and only one does, since the ranges of $C$ are disjoint. If $t \notin I$, no range of $C$ contains $t$. $\square$

So the multiset $E(\ell) = \bigcup_{y \in \mathrm{anc}(\ell)} L(y)$ is the edge multiset of $G_t$, by Lemmas 1 and 2.

**Lemma 3 (the walk).** When VISIT$(x)$ starts, the union-find $D$ is in the state reached from $n$ singletons by the unions of the edges in $\bigcup_{y \in \mathrm{anc}(x) \setminus \{x\}} L(y)$. When VISIT$(x)$ ends, $D$ is in the same state as when it started.

*Proof.* By induction on the height of $x$. Let $S$ be the state when VISIT$(x)$ starts, and let $h$ be the log height saved in line L3. Line L4 applies the unions of $L(x)$, so $D$ is now the state of the unions of the edges of $\mathrm{anc}(x)$. If $x$ is internal, VISIT of the left child starts in this state, as the claim for the child needs, and by the induction hypothesis it ends in the same state; the same holds for the right child. Line L7 then undoes every union recorded after height $h$. Each union records the two fields it wrote, and the undo restores them in the reverse order, so by the correctness of the [rollback technique](/rollback-technique/) the state returns to $S$. At the root, the start state is $n$ singletons, which matches the empty set of ancestors. $\square$

**Theorem.** For each time $t$ whose operation is a query, the answer at the leaf of $t$ is the answer for $G_t$.

*Proof.* By Lemma 3, after line L4 at the leaf $\ell$ of $t$, the union-find holds the unions of the edges in $E(\ell)$, which is the edge multiset of $G_t$. The sets of a union-find after the unions of an edge set are the connected components of the graph of those edges: two vertices are in one set if and only if a chain of the unioned edges joins them, and union by size changes only the shape of the trees, not the sets. So $\mathrm{find}(u) = \mathrm{find}(v)$ if and only if $u$ and $v$ are connected in $G_t$. The component counter starts at $n$, decreases by one exactly at each union that merges two sets, and is restored by each undo, so it equals the number of components of $G_t$. Line L5 reads these values. The leaves are visited in the order of time, left before right, so the answers come out in the order of the queries. $\blacksquare$
