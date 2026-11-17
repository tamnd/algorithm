---
title: WINNOWER keeps every n-clique and ends with the unique largest subgraph of extendable edges
proves: [correctness]
status: full
---

Let $s_1, \ldots, s_n$ ($n \ge 2$) be sequences and $\Gamma = (V, E)$ the graph of line L1: the vertices are the windows $(i, q)$, and an edge joins windows of different sequences with Hamming distance at most $2d$. For a subgraph $H = (V, F)$ with $F \subseteq E$, call an edge $(u, v) \in F$ *extendable in $H$* if for every sequence $p$ other than the sequences of $u$ and $v$ there is a vertex $w$ of $p$ with $(u, w) \in F$ and $(v, w) \in F$. Call $H$ *closed* if every edge of $H$ is extendable in $H$.

**Lemma 1 (monotone).** If $F \subseteq F'$ and $(u, v) \in F$ is extendable in $(V, F)$, then it is extendable in $(V, F')$.

*Proof.* The common neighbours that witness it in $F$ are still neighbours in $F'$. $\square$

**Lemma 2 (a largest closed subgraph).** There is a unique closed subgraph $H^* = (V, F^*)$ that contains every closed subgraph.

*Proof.* The empty edge set is closed. If $(V, F_1)$ and $(V, F_2)$ are closed, then each edge of $F_1$ is extendable in $(V, F_1)$ and so, by Lemma 1, in $(V, F_1 \cup F_2)$; the same holds for $F_2$. So the union of closed subgraphs is closed, and $F^*$ is the union of all closed edge sets, which are finitely many. $\square$

**Lemma 3 (the planted cliques are closed).** If $K$ is an $n$-clique of $\Gamma$ (one vertex per sequence), its edge set is closed, so $K \subseteq H^*$.

*Proof.* For an edge $(u, v)$ of $K$ and a sequence $p$ other than those of $u$ and $v$, the vertex of $K$ in $p$ is joined to both $u$ and $v$ by edges of $K$. $\square$

**Theorem.** Whatever the order of the removals, lines L2 to L6 end with the edge set $F^*$.

*Proof.* Invariant: the current edge set $F$ contains $F^*$. It holds at the start, since $F = E$. Suppose it holds and line L5 removes $(u, v)$. Line L4 found that $(u, v)$ is not extendable in $(V, F)$. If $(u, v)$ were in $F^*$, it would be extendable in $H^*$ and, by Lemma 1, in $(V, F)$, since $F^* \subseteq F$. So $(u, v) \notin F^*$, and the invariant holds after the removal.

The loop ends: each pass but the last removes at least one edge, and $E$ is finite. It ends after a pass that removes no edge, that is, after a pass in which every edge of the current $F$ was found extendable. An edge that was checked early in the pass could only lose witnesses through a later removal in the same pass, but that pass made no removal, so at the end every edge of $F$ is extendable in $(V, F)$, and $(V, F)$ is closed. By Lemma 2, $F \subseteq F^*$, and with the invariant, $F = F^*$. $\square$

**Corollary 1 (no clique is lost).** By Lemma 3 and the theorem, every edge of every $n$-clique of $\Gamma$ survives, so the $n$-cliques of the pruned graph are exactly the $n$-cliques of $\Gamma$. Removing edges creates no new cliques.

**Corollary 2 (idempotent).** A second run of lines L2 to L6 on the result makes one pass and removes nothing, since $H^*$ is closed.

**Lemma 4 (the clique listing).** Line L7 lists every $n$-clique of the pruned graph exactly once.

*Proof.* The backtracking picks a vertex of $s_1$ and, at depth $p$, a vertex of $s_{p+1}$ that is joined to all vertices already picked; these candidates are the intersection of their neighbour sets in $s_{p+1}$. Every $n$-clique $(v_1, \ldots, v_n)$ is found along the path $v_1, v_2, \ldots$, since each $v_{p+1}$ is a candidate after $v_1, \ldots, v_p$. Different paths give different tuples, and a tuple at depth $n$ has every pair joined. $\square$

**Planted motifs.** If $M$ is a string with $d_H(M, s_i[q_i .. q_i + L - 1]) \le d$ for every $i$, then by the triangle inequality every pair of these windows is within $2d$, so $(q_1, \ldots, q_n)$ is an $n$-clique of $\Gamma$, and by Corollary 1 it is in the output. The converse is false: an $n$-clique need not have a string within $d$ of all its windows.

**Cost.** Line L1 computes $\binom{n}{2} W^2$ distances of $O(L)$ each. A pass checks each of at most $E$ edges against $n - 2$ sequences with a set intersection of $O(W)$, so $O(E n W)$, and there are at most $E + 1$ passes. The listing is $O(W^n)$ in the worst case.

The tests compare the output cliques with brute force over all choices of windows, check that every left edge is extendable and that a second run removes nothing, and check that removing edges one at a time in a random order gives the same edge set.
