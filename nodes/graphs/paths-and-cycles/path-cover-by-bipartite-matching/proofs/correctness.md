---
title: The matching on the split graph gives a minimum path cover of a DAG
proves: [correctness, termination]
status: full
---

Let $G = (V, A)$ be a directed acyclic graph with $n$ vertices, parallel arcs allowed. The split graph $H$ has left vertices $u^{\text{out}}$, right vertices $v^{\text{in}}$, and an edge $u^{\text{out}} v^{\text{in}}$ for each arc $u \to v$. Since $G$ has no self-loop, no edge of $H$ joins the two copies of one vertex. A *matching* is a set of edges of $H$ with no common end. An *augmenting path* for a matching $M$ is a path in $H$ whose edges alternate between non-matched and matched, and whose two end vertices are not covered by $M$.

**Lemma 1 (covers and matchings).** For every matching $M$ of $H$, the arcs $S(M) = \{u \to v : u^{\text{out}} v^{\text{in}} \in M\}$ form vertex-disjoint paths that cover $V$, and there are exactly $n - |M|$ of them. Conversely, every cover of $V$ by $p$ vertex-disjoint paths gives a matching of size $n - p$. Hence the least number of paths is $n - \nu(H)$, where $\nu(H)$ is the size of a maximum matching.

*Proof.* In $S(M)$ every vertex has at most one outgoing arc, since $u^{\text{out}}$ is matched at most once, and at most one incoming arc, since $v^{\text{in}}$ is matched at most once. A graph on $V$ with in-degrees and out-degrees at most 1 is a union of vertex-disjoint paths and cycles, and $S(M) \subseteq A$ has no cycle. Each vertex is on exactly one of these paths (possibly a path of one vertex). A path with $k$ vertices has $k - 1$ arcs, so summing over the paths, $|S(M)| = n - p$, and $|S(M)| = |M|$. Conversely, for a cover by $p$ disjoint paths, take the edges $u^{\text{out}} v^{\text{in}}$ for consecutive vertices $u, v$ of a path: each vertex has at most one successor and one predecessor, so this is a matching, of size $n - p$. $\square$

Lines L12 and L13 output exactly the paths of $S(M)$: a path starts at a vertex $s$ with no predecessor, $\mathrm{matchR}[s] = \mathrm{NIL}$, and $\mathrm{matchL}$ follows its arcs. By Lemma 1 every vertex is on one of them. It remains to show that the final $M$ is maximum.

**Lemma 2 (Berge).** If a matching $M$ is not maximum, it has an augmenting path.

*Proof.* Let $M^*$ be a larger matching. In the symmetric difference $M \oplus M^*$ every vertex has degree at most 2, so its components are paths and even cycles whose edges alternate between $M$ and $M^*$. Some component has more edges of $M^*$ than of $M$; it is a path that starts and ends with an $M^*$ edge, and its ends are not covered by $M$. It is an augmenting path for $M$. $\square$

In the bipartite graph $H$ an augmenting path has odd length, so it has one end on each side; call its left end its *start*.

**Lemma 3 (one search).** Let $M$ be the matching before the search from root $r$ (lines L4 to L11), with $r^{\text{out}}$ not covered. The search ends; if an augmenting path starting at $r^{\text{out}}$ exists, it finds one and line L10 replaces $M$ by $M \oplus P$, a matching with one more edge; otherwise $M$ does not change.

*Proof.* *Invariant:* the stack is $x_1 = r, x_2, \ldots, x_k$, the list $\mathrm{via}$ is $y_1, \ldots, y_{k-1}$ (or $y_1, \ldots, y_k$ just after line L8 appends), $x_i^{\text{out}} y_i^{\text{in}}$ is an edge not in $M$, and $y_i^{\text{in}} x_{i+1}^{\text{out}}$ is in $M$. So $r^{\text{out}}, y_1^{\text{in}}, x_2^{\text{out}}, \ldots$ is an alternating path. Line L8 appends $v$ adjacent to the top $x_k$, line L11 pushes $\mathrm{matchR}[v]$, and line L7 pops a frame together with the $\mathrm{via}$ entry that led to it; each keeps the invariant. The right vertices on the path are distinct because each is marked visited when appended, and so the left vertices $x_{i+1} = \mathrm{matchR}[y_i]$ are distinct, and different from $r$, which is not covered.

*Termination.* Each iteration either reads a new list entry through $\mathrm{ptr}$ or pops a frame. A left vertex is pushed only as $\mathrm{matchR}[v]$ for a newly visited $v$, so at most $n$ pushes happen, and the lists are finite.

*Success.* At line L9, $v = y_k$ is not covered, so the alternating path from $r^{\text{out}}$ to $y_k^{\text{in}}$ is augmenting. Line L10 matches $x_i$ with $y_i$ for all $i$, which removes the matched edges $y_i x_{i+1}$ (each $x_{i+1}$ is rematched to $y_{i+1}$ and each $y_i$ to $x_i$) and adds the others: this is $M \oplus P$, a matching of size $|M| + 1$.

*Failure.* Suppose the stack empties. Let $Y$ be the visited right vertices. Every $y \in Y$ is covered (otherwise line L9 succeeds), its partner $\mathrm{matchR}[y]$ was pushed and later popped with its whole list read, and so every right neighbour of it is in $Y$; also every right neighbour of $r$ is in $Y$. By induction along any alternating path from $r^{\text{out}}$, every right vertex on it is in $Y$ and so is covered. Hence no augmenting path starts at $r^{\text{out}}$. $\square$

**Lemma 4 (Kuhn).** Let $P$ be an augmenting path for $M$ with start $x$, and $M' = M \oplus P$. If no augmenting path for $M$ starts at a left vertex $u$, then no augmenting path for $M'$ starts at $u$.

*Proof.* Suppose $Q$ is an augmenting path for $M'$ with start $u$. Then $u$ is not covered by $M'$, so not by $M$, and $u \ne x$ and $u$ is not on $P$ (every vertex of $P$ is covered by $M'$). If $Q$ has no vertex on $P$, then $M$ and $M'$ agree on the edges of $Q$, and $Q$ is augmenting for $M$, a contradiction. Otherwise let $z$ be the first vertex of $Q$, from $u$, that lies on $P$, and let $y$ be the vertex before it. The edge $yz$ is not on $P$, since $y$ is not, so it is in $M'$ exactly when it is in $M$. If $z$ is a left vertex, $Q$ enters it by a matched edge of $M'$; but the $M'$ partner of a vertex of $P$ lies on $P$, and $y$ does not, a contradiction. So $z$ is a right vertex $y_i$ of $P = x, y_1, x_1, y_2, \ldots, x_{k-1}, y_k$, where $x_{j-1} y_j \notin M$ and $y_j x_j \in M$. The part of $Q$ from $u$ to $z$ alternates with respect to $M$ and enters $z$ by a non-matched edge, and $y_i, x_i, y_{i+1}, \ldots, y_k$ alternates with respect to $M$, starting with the matched edge $y_i x_i$ and ending at $y_k$, which $M$ does not cover. The two parts share only $z$, so together they are an augmenting path for $M$ starting at $u$, a contradiction. $\square$

**Theorem.** PATH-COVER terminates and returns a cover of $V$ by $n - \nu(H)$ vertex-disjoint paths, which is the minimum.

*Proof.* Each of the $n$ searches terminates by Lemma 3, and lines L12 to L14 follow at most $n$ pointers. The algorithm keeps a matching, by Lemma 3. A covered left vertex stays covered, because line L10 only rematches covered vertices and covers new ones. *Claim:* after the search from $r$, no augmenting path starts at any uncovered left vertex among $0, \ldots, r$. If $r$ is covered after its search, the claim for $r$ is empty; otherwise its search failed and Lemma 3 shows there is none from $r$. For earlier uncovered roots, the claim held before, and the matching changed only by augmenting paths, so it still holds by Lemma 4. At the end, no augmenting path starts at any uncovered left vertex, and every augmenting path has a left start, so there is none at all. By Lemma 2 the matching is maximum, and by Lemma 1 the output is a minimum path cover. $\blacksquare$
