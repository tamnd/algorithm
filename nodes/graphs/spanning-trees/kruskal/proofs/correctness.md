---
title: Kruskal's algorithm returns a minimum spanning forest
proves: [correctness, termination]
status: full
---

**Claim.** Let $G = (V, E)$ be a finite undirected graph with a real weight $w(e)$ on each edge. Weights may tie, $G$ may have parallel edges and self-loops, and $G$ need not be connected. Then KRUSKAL$(G, w)$ stops, and the set $F$ that it returns is a minimum spanning forest of $G$: a forest with the same connected components as $G$, of least total weight among all such forests.

**Setup.** Let $e_1, e_2, \ldots, e_m$ be the edges in the order of line L3, so $w(e_1) \le w(e_2) \le \cdots \le w(e_m)$. Let $F_k$ be the set $F$ after the edge $e_k$ is processed, with $F_0 = \emptyset$. A *spanning forest* of $G$ is an acyclic set of edges whose components are the components of $G$. A forest on $n$ vertices with $t$ trees has $n - t$ edges ([tree edge count](/tree-edge-count/)), so each spanning forest of $G$ has $n - c$ edges, where $c$ is the number of components of $G$. A minimum spanning forest exists, because $E$ is finite and contains a spanning forest (keep a spanning tree of each component).

**Lemma 1 (the sets).** After each step, the sets of the disjoint-set structure are the vertex sets of the trees of $F$, and $F$ is acyclic.

*Proof.* By induction on the steps. At the start the sets are the $n$ single vertices and $F = \emptyset$. In step $k$, with $e_k = (u, v)$, line L5 compares the sets of $u$ and $v$. If they are equal, nothing changes. If they differ, then by the induction hypothesis $u$ and $v$ are in different trees of $F$. Adding $e_k$ joins these two trees into one tree and closes no cycle, and UNION merges exactly their two sets. $\square$

**Lemma 2 (the cut step).** Let $A \subseteq F^*$ for a minimum spanning forest $F^*$. Let $S \subseteq V$ be a set such that no edge of $A$ has exactly one end in $S$. Let $e$ be an edge with exactly one end in $S$ and with $w(e) \le w(f)$ for each edge $f$ that has exactly one end in $S$. Then $A \cup \{e\}$ is a subset of some minimum spanning forest.

*Proof.* If $e \in F^*$, take $F^*$. Otherwise let $e = (u, v)$ with $u \in S$ and $v \notin S$. The edge $e$ joins $u$ and $v$, so they are in one component of $G$, and so in one tree of $F^*$. Let $P$ be the path from $u$ to $v$ in that tree. The path starts in $S$ and ends outside $S$, so it has an edge $f$ with exactly one end in $S$. The edge $f$ is not in $A$, by the choice of $S$. Let $F' = (F^* \setminus \{f\}) \cup \{e\}$. Removing $f$ splits its tree into two trees, one with $u$ and one with $v$, because $f$ is on the only path between them. Adding $e$ joins these two trees again. So $F'$ is acyclic and has the same components as $F^*$, and $F'$ is a spanning forest. Its weight is $w(F^*) - w(f) + w(e) \le w(F^*)$, so $F'$ is a minimum spanning forest. It contains $A$, because $f \notin A$, and it contains $e$. $\square$

**Invariant.** For each $k$ from $0$ to $m$: there is a minimum spanning forest $F^*_k$ with $F_k \subseteq F^*_k$.

1. *Initialization.* $F_0 = \emptyset$ is a subset of each minimum spanning forest.
2. *Maintenance, edge dropped.* Then $F_k = F_{k-1}$ and $F^*_k = F^*_{k-1}$ works.
3. *Maintenance, edge added.* Let $e_k = (u, v)$, and let $S$ be the vertex set of the tree of $F_{k-1}$ that holds $u$. By Lemma 1, $v \notin S$, so $e_k$ has exactly one end in $S$. No edge of $F_{k-1}$ has exactly one end in $S$, because $S$ is the vertex set of a tree of the forest. Let $f = e_j$ be any edge with exactly one end in $S$. If $j < k$, then at step $j$ the edge was either added, and then $f \in F_{k-1}$, which is false, or dropped, and then its two ends were in one set at step $j$. Sets only merge, so its two ends are in one tree of $F_{k-1}$, and both are in $S$ or both are outside $S$, which is also false. So $j \ge k$ and $w(e_k) \le w(e_j)$ by the order of the sort. Lemma 2, with $A = F_{k-1}$ and $F^* = F^*_{k-1}$, gives a minimum spanning forest $F^*_k \supseteq F_k$.

**Termination.** The loop of line L4 runs once for each of the $m$ edges, and each run does a bounded number of disjoint-set operations, each of which stops. So the algorithm stops after $m$ steps.

**Conclusion.** Let $F = F_m$. Each edge $e_k \notin F$ had both ends in one set at step $k$, so both ends are in one tree of $F$. Each edge of $F$ also has both ends in one tree of $F$. So each path of $G$ stays inside one tree of $F$, and each component of $G$ lies inside one tree of $F$. Since $F \subseteq E$, each tree of $F$ lies inside one component of $G$. So $F$ has the components of $G$, and by Lemma 1 it is acyclic: $F$ is a spanning forest with $n - c$ edges. The invariant gives $F \subseteq F^*_m$, and $F^*_m$ also has $n - c$ edges, so $F = F^*_m$. Therefore $F$ is a minimum spanning forest. When $G$ is connected, $c = 1$ and $F$ is a minimum spanning tree. $\blacksquare$
