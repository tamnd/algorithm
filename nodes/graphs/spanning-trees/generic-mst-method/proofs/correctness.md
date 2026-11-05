---
title: The generic MST method returns a minimum spanning forest for every choice of cuts
proves: [correctness, termination]
status: full
---

**Claim.** Let $G = (V, E)$ be a finite undirected graph with $n$ vertices, $c$ components and a real weight on each edge; ties, parallel edges and self-loops are allowed. For each sequence of choices made at line L3, GENERIC-MST stops after exactly $n - c$ iterations, and the set $A$ that it returns is a minimum spanning forest of $G$.

**Setup.** A *spanning forest* is an acyclic edge set with the components of $G$; each has $n - c$ edges. A cut $(S, V \setminus S)$ respects $A$ when no edge of $A$ has exactly one end in $S$.

**Lemma 1.** If $A$ is a forest, a cut $(S, V \setminus S)$ respects $A$ if and only if $S$ is a union of vertex sets of trees of $(V, A)$. Each edge that crosses such a cut joins two different trees of $(V, A)$.

*Proof.* If $S$ is a union of trees, each edge of $A$ lies in one tree and has both ends in $S$ or both outside. Conversely, if $S$ cuts a tree, the tree has a vertex in $S$ and one outside, and the path between them in the tree has an edge with exactly one end in $S$. For the second part, an edge with one end in $S$ and one outside cannot have both ends in one tree, because each tree is inside $S$ or outside it. $\square$

**Lemma 2 (the cut property, forest form).** If $A$ is a subset of some minimum spanning forest $F^*$, the cut $(S, V \setminus S)$ respects $A$, and $e$ is a light edge of the cut, then $A \cup \{e\}$ is a subset of some minimum spanning forest.

*Proof.* If $e \in F^*$ we are done. Else let $e = (u, v)$, $u \in S$, $v \notin S$. The vertices $u$ and $v$ are in one component of $G$, so $F^*$ has a path $P$ from $u$ to $v$, and $P$ has an edge $f$ that crosses the cut; $f \notin A$ because $A$ respects the cut. The set $F' = F^* - f + e$ is a spanning forest: removing $f$ splits one tree into a part with $u$ and a part with $v$, and $e$ joins them again. Since $e$ is light, $w(e) \le w(f)$ and $w(F') \le w(F^*)$, so $F'$ is minimum, and it contains $A \cup \{e\}$. $\square$

**Invariant.** At the test of line L2, $A$ is a subset of some minimum spanning forest, and in particular $A$ is a forest.

1. *Initialization.* $A = \emptyset$ is a subset of every minimum spanning forest, and one exists because $E$ is finite and contains a spanning forest.
2. *Maintenance.* The cut of line L3 respects $A$, and the edge of line L4 is light for it. Lemma 2 shows that $A \cup \{(u, v)\}$ is a subset of some minimum spanning forest, so the invariant holds after line L5. The edge of line L4 exists, since line L3 chooses a cut that some edge crosses. Such a cut exists whenever the test of line L2 is true: the tree at one end of an edge that joins two trees is a valid $S$.

**Termination.** By Lemma 1, the edge added at line L5 joins two different trees of $(V, A)$, so $A$ stays a forest and its number of trees drops by exactly one in each iteration. The number of trees starts at $n$ and is never less than $c$, because the trees of $A$ lie inside the components of $G$. So there are at most $n - c$ iterations, and the loop stops.

**Conclusion.** When the test of line L2 is false, no edge of $G$ joins two different trees of $(V, A)$. So each component of $G$ lies inside one tree of $A$, and each tree of $A$ lies inside one component of $G$. Thus $A$ is a spanning forest, with $n - c$ edges, and the loop ran exactly $n - c$ times. By the invariant, $A \subseteq F^*$ for a minimum spanning forest $F^*$, which also has $n - c$ edges, so $A = F^*$. $\blacksquare$
