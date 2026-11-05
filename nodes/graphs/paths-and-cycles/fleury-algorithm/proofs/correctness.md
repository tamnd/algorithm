---
title: Fleury's algorithm finds an Eulerian trail when one exists
proves: [correctness, termination]
status: full
---

Let $G$ be an undirected multigraph with $m \ge 1$ edges, where a self-loop adds 2 to the degree of its vertex. For a multigraph $H$, a *bridge* of $H$ is an edge $e = uv$ with $u \ne v$ such that $u$ and $v$ are in different components of $H - e$; a self-loop is never a bridge.

**NIL is correct.** By Euler's theorem, $G$ has an Eulerian trail if and only if its edges lie in one component and it has at most two odd vertices. By the handshaking lemma the number of odd vertices is even, so it is 0 or 2. Line L1 returns NIL exactly when this condition fails. From now on the condition holds.

**Setup.** Let $s$ be the start chosen at line L2. If $G$ has two odd vertices, $s$ is one of them and $t$ is the other; otherwise $t = s$. Each pass of the loop removes one edge, so the loop runs at most $m$ times and the algorithm stops. We show that at the test of line L4:

- (a) if $H$ has an edge, every edge of $H$ lies in the component of $H$ that contains $u$;
- (b) the odd vertices of $H$ are $\{u, t\}$ if $u \ne t$, and there are none if $u = t$.

**Initially.** $H = G$ and $u = s$. Line L1 gives (a), and (b) holds by the choice of $s$ and $t$.

**Lemma 1 (one bridge at most).** Assume (a) and (b), and $\deg_H(u) \ge 2$. Then at most one edge at $u$ is a bridge of $H$. In particular, line L6 finds an edge.

*Proof.* Let $e = uv$ be a bridge of $H$ at $u$, and let $C$ be the component of $H - e$ that contains $v$; it does not contain $u$. The degrees in $H - e$ of the vertices of $C$ are their degrees in $H$, except for $v$, whose degree is one less. Suppose $t \notin C$. Then by (b) every vertex of $C$ has even degree in $H$, because the only odd vertices of $H$ are $u$ and $t$, which are outside $C$. So in $H - e$ the vertex $v$ is the only odd vertex of $C$. But $C$ is a graph on its own, and the number of its odd vertices is even by the handshaking lemma. This is a contradiction, so $t \in C$.

Now let $e_1 = uv_1$ and $e_2 = uv_2$ be two different bridges at $u$, with far components $C_1$ and $C_2$ as above. If some vertex $x$ were in both, there would be a walk from $v_1$ to $x$ in $C_1$ and from $x$ to $v_2$ in $C_2$, both avoiding $u$, because $u \notin C_1 \cup C_2$. Then $v_1$ and $v_2$ are joined by a walk that avoids $u$, so $e_1$ and $e_2$ lie on a cycle through $u$, and $e_1$ is not a bridge. So $C_1$ and $C_2$ are disjoint, but both contain $t$, a contradiction.

If $\deg_H(u) \ge 2$ then either $u$ has at least two edges of $H$, or one self-loop. In the first case at most one of them is a bridge, and in the second the loop is not a bridge. Either way line L6 finds an edge. $\square$

**Lemma 2 (the invariants are kept).** If (a) and (b) hold at line L4 and $\deg_H(u) > 0$, they hold again after lines L5 to L8.

*Proof.* Let $e = uv$ be the edge removed, $H' = H - e$, and $v$ the new current vertex.

For (b): removing $e$ lowers the degrees of $u$ and $v$ by 1 each, or the degree of $u$ by 2 if $e$ is a loop, so the parities of $u$ and $v$ flip if $u \ne v$, and nothing changes if $u = v$. If $u = v$, (b) is the same statement for $H'$. If $u \ne v$: when $u \ne t$, the odd set $\{u, t\}$ becomes $\{t\} \triangle \{v\}$, which is $\{v, t\}$ if $v \ne t$ and empty if $v = t$; when $u = t$, the empty odd set becomes $\{u, v\} = \{t, v\}$. In each case it is the set stated in (b) for the new current vertex $v$.

For (a): if $e$ was chosen at line L6, it is not a bridge, so $H'$ has the same components as $H$ on the vertices that keep edges, and all edges of $H'$ are in the component of $u$, which contains $v$. If $e$ was chosen at line L5, $e$ was the only edge at $u$, so $u$ has no edge in $H'$. Every edge $f$ of $H'$ was joined to $u$ in $H$ by a walk, by (a), and the walk enters $u$ only through $e$, so the part of it after the last use of $e$ is a walk in $H'$ from $v$ to $f$. So all edges of $H'$ are in the component of $v$. $\square$

**Lemma 3 (all edges are used).** When the loop stops, $H$ has no edges.

*Proof.* The loop stops when $\deg_H(u) = 0$. Then the component of $u$ in $H$ is $\{u\}$ with no edge, and by (a) $H$ has no edge at all. $\square$

**Theorem.** If $G$ has an Eulerian trail, FLEURY returns one, with the edges in $T$ and the vertices in $W$; otherwise it returns NIL.

*Proof.* The NIL case is shown above. Otherwise, each pass appends to $T$ an edge of $H$ at the current vertex $u$, removes it from $H$, and moves to its other end, so $(W, T)$ is a walk in $G$ that uses no edge twice. By Lemmas 1 and 2 each pass is well defined, and by Lemma 3 the walk uses all $m$ edges when it stops. So it is an Eulerian trail. $\blacksquare$
