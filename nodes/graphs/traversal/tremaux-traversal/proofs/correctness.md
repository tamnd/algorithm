---
title: Trémaux's rule walks each edge of the component twice and returns to the start
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be an undirected multigraph, $s \in V$, and $C$ the vertex set of the component of $s$. The walker is at $v$. Call the vertices with $\mathrm{visited} = $ true *visited*. For each visited $u \ne s$, the edge $\mathrm{entry}[u]$ joins $u$ to the vertex $p(u)$ at which the walker stood when he first entered $u$. Let $P$ be the sequence $s = u_0, u_1, \ldots, u_k = v$ in which $u_{i-1} = p(u_i)$; we show that it exists.

**Invariant.** At the start of each iteration of the loop of line L2:

1. the entry edges of the visited vertices other than $s$ form a tree $T$ on the visited vertices, and $v$ is visited, so $P$ is the path in $T$ from $s$ to $v$;
2. an edge has mark 1 if and only if it is $\mathrm{entry}[u_i]$ for some $i \ge 1$;
3. each visited vertex that is not on $P$ has no edge with mark 0;
4. the walk so far goes from $s$ to $v$, an edge with mark 0 has not been walked, and an edge with mark $j$ has been walked $j$ times.

*Initialization.* Only $s$ is visited, $T$ has no edges, $P = (s)$, all marks are 0 and the walk is empty. All four parts hold.

*A consequence.* The edges with mark 1 at $v$ are $\mathrm{entry}[v]$, if $v \ne s$, and nothing else. By part 2, an edge with mark 1 is $\mathrm{entry}[u_i] = \{u_{i-1}, u_i\}$. It is not a loop, because $u_i$ was unvisited and $p(u_i)$ visited when it was set. If it contains $v = u_k$, then $u_i = v$ or $u_{i-1} = v$, and a vertex is on a path only once, so $i = k$.

*Maintenance.* Consider the three cases of one iteration.

- *Line L5.* The edge $e = \{v, w\}$ has mark 0 and $w$ is visited. The walker goes to $w$ and back, $e$ gets mark 2 and has been walked twice. Nothing else changes, so all parts still hold.
- *Line L6.* The edge $e = \{v, w\}$ has mark 0 and $w$ is not visited. Now $w$ is visited with $\mathrm{entry}[w] = e$ and $p(w) = v$, so $T$ grows by a leaf, and $P$ becomes $u_0, \ldots, u_k, w$. The edge $e$ has mark 1, it has been walked once, and it is the entry edge of the new last vertex of $P$. Part 3 is unchanged because $w$ is on $P$.
- *Line L8.* No edge at $v$ has mark 0, and $v \ne s$. The walker goes along $\mathrm{entry}[v]$ to $u_{k-1}$, which gives that edge its second walk and mark 2. Now $P$ is $u_0, \ldots, u_{k-1}$, which agrees with part 2. The vertex $v$ leaves $P$ and has no edge with mark 0, so part 3 holds.

**Termination.** Each iteration that does not stop raises the sum of all marks by 1 or 2, and the sum is at most $2|E|$, because a mark never exceeds 2: lines L4 to L6 act only on an edge with mark 0, and line L8 acts only on $\mathrm{entry}[v]$, which has mark 1 by part 2. So the loop stops after at most $2|E|$ iterations.

**Lemma 1 (local rule).** At each step, the walker can choose by the local marks alone: an edge at $v$ with mark 0 for line L3, and, for line L8, the only edge at $v$ with mark 1.

*Proof.* This is the consequence above. $\square$

**Lemma 2.** When the walker stops, he is at $s$, every vertex of $C$ is visited, every edge with an end in $C$ has mark 2, and no other edge has a mark.

*Proof.* Line L9 runs only if $\mathrm{entry}[v] = \mathrm{NIL}$, so $v = s$, $P = (s)$, and no edge at $s$ has mark 0. By part 2, no edge has mark 1. By part 3, and the test at $s$, no visited vertex has an edge with mark 0. Suppose that a vertex of $C$ is not visited. A path from $s$ to it has an edge $\{x, y\}$ with $x$ visited and $y$ not. This edge has mark 2, so it has been walked, by part 4, and the walker has stood at $y$. Each arrival at a vertex happens at line L4, L5 or L8, and an arrival at an unvisited vertex makes it visited at line L6. So $y$ is visited, a contradiction. So all of $C$ is visited, and each edge with an end in $C$ has mark 2. The walk stays in $C$, so other edges are never walked and have mark 0. $\square$

**Lemma 3 (Trémaux tree).** At the end, $T$ is a spanning tree of $C$, and each edge $\{x, y\}$ of the component that is not in $T$ joins an ancestor and a descendant in $T$.

*Proof.* $T$ is a tree on the visited vertices, which are $C$, by part 1 and Lemma 2. A non-tree edge $\{x, y\}$ gets its first mark at line L4 when the walker stands at one end, say $x$, and line L5 applies, so $y$ is visited at that moment. If $y$ were not on the path $P$ from $s$ to $x$ at that moment, then by part 3 it would have no edge with mark 0, but $\{x, y\}$ has mark 0 then. So $y$ is on the tree path from $s$ to $x$, which makes it an ancestor of $x$. A loop $x = y$ joins $x$ to itself. $\square$

**Theorem.** TREMAUX$(G, s)$ stops after a closed walk from $s$ that visits every vertex of the component of $s$, walks each edge of the component exactly twice, never walks another edge, and needs at each step only the marks at the current vertex. Its entry edges form a spanning tree of the component in which every other edge joins an ancestor and a descendant.

*Proof.* Termination and Lemma 2 give the walk and its end at $s$. By part 4 and Lemma 2, each edge of the component has been walked exactly twice and every other edge never. Lemma 1 gives the local rule and Lemma 3 the tree. $\blacksquare$
