---
title: The planarization heuristic outputs a planarization of G, with a maximal planar subgraph and locally optimal insertions
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple graph with $n$ vertices and $m$ edges. A rotation system $\rho$ on a graph $H$ defines darts $(a, b)$ for every edge $ab$, and the face permutation $\varphi(a, b) = (b, c)$, where $c$ is the neighbour just before $a$ in $\rho(b)$. Its cycles are the faces. For a connected graph with at least one edge, $V - E + F \le 2$, with equality if and only if $\rho$ is the rotation system of a planar embedding; we call such a $\rho$ *planar*. For a disconnected graph, $\rho$ is planar when it is planar on every component. We assume that the test at line L3 is correct and that line L4 returns a planar rotation system of $P$.

**Claim 1 (the subgraph is maximal planar).** At the end of phase 1, $P$ is planar and $P + e$ is not planar for every $e \in R$.

*Proof.* Edges are added to $P$ only when the result is planar, so $P$ stays planar. Let $e \in R$, rejected when the subgraph was $P_t \subseteq P$. Then $P_t + e$ is not planar, and $P_t + e \subseteq P + e$. A subgraph of a planar graph is planar, so $P + e$ is not planar. $\square$

**Claim 2 (removed edges stay within a component).** For every $uv \in R$, the vertices $u$ and $v$ lie in the same component of $P$.

*Proof.* If not, $P + uv$ would join two components of a planar graph by a bridge: draw the two components in disjoint discs, with $u$ and $v$ on their outer faces, and join them by a curve outside both. This is planar, contradicting Claim 1. $\square$

The vertices of $H$ are those of $P$ plus dummy vertices, and the dummy vertices are added to the component that contains the inserted edge. So the components of $H$ have the same original vertices as the components of $P$ throughout.

**Lemma 3 (subdivision).** Let $\rho$ be a rotation system with an edge $xy$. Replace $y$ by $d$ in $\rho(x)$, $x$ by $d$ in $\rho(y)$, and set $\rho(d) = (x, y)$. Then the faces are the same, except that the dart $(x, y)$ is replaced by the two darts $(x, d), (d, y)$ in its face, and $(y, x)$ by $(y, d), (d, x)$ in its face.

*Proof.* $\varphi(x, d) = (d, c)$ with $c$ just before $x$ in $(x, y)$, so $c = y$. And $\varphi(d, y) = (y, c')$ with $c'$ just before $d$ in $\rho(y)$, which is the neighbour that was just before $x$, so $\varphi(d, y)$ is the old $\varphi(x, y)$. A dart $(z, x)$ with $\varphi(z, x) = (x, y)$ before now has $\varphi(z, x) = (x, d)$. The other values of $\varphi$ do not change. The same holds for $(y, x)$. $\square$

So a subdivision adds one vertex and one edge and keeps the number of faces. $V - E + F$ is unchanged, and $\rho$ stays planar.

**Lemma 4 (inserting an edge into one face).** Let $f$ be a face with corners $(a, x), (x, c)$ and $(a', y), (y, c')$, where $x \ne y$ and $x, y$ are not adjacent. Insert $y$ between $c$ and $a$ in $\rho(x)$, and $x$ between $c'$ and $a'$ in $\rho(y)$. Then $f$ is split into two faces, and every other face is unchanged.

*Proof.* Write the cycle of $f$ as $A, B$, where $A$ is the run of darts from $(x, c)$ to $(a', y)$ and $B$ the run from $(y, c')$ to $(a, x)$. After the insertion, $y$ is just before $a$ in $\rho(x)$, so $\varphi(a, x) = (x, y)$, and $\varphi(x, y) = (y, c')$ because $c'$ is just before $x$ in $\rho(y)$. So $B$ followed by $(x, y)$ is a cycle. In the same way $\varphi(a', y) = (y, x)$ and $\varphi(y, x) = (x, c)$, so $A$ followed by $(y, x)$ is a cycle. For any other dart $(z, w)$, the neighbour just before $z$ in $\rho(w)$ is unchanged, because the only new entries are $y$, placed just before $a$ in $\rho(x)$, and $x$, placed just before $a'$ in $\rho(y)$. $\square$

The insertion adds one edge and one face, keeps the vertices, and keeps $x$ and $y$ in one component. So $V - E + F$ is unchanged, and $\rho$ stays planar.

**Claim 5 (termination of the search).** At line L7, the search reaches a face at $v$.

*Proof.* By Claim 2 and the remark after it, $u$ and $v$ lie in one component $K$ of $H$. The dual of the connected plane graph $K$ is connected: two faces of $K$ that share a vertex $z$ are joined by a dual path that crosses the edges at $z$ one after another, and any two faces are linked by a chain of faces sharing vertices along a path of $K$. The faces at $v$ are faces of $K$, so the search reaches one. $\square$

The search is a breadth-first search on a finite graph, and the loops at lines L2, L5, L8 and L9 are finite, so the algorithm terminates.

**Claim 6 (the search avoids the ends).** No crossed edge $e_i$ is incident to $u$ or $v$, the faces $f_0, \ldots, f_k$ are distinct, and each $e_i$ has $f_{i-1}$ on one side and $f_i$ on the other, with $f_{i-1} \ne f_i$.

*Proof.* Both faces on the two sides of an edge $uz$ contain $u$, so both have distance 0, and a shortest dual path never crosses $uz$. Both faces on the sides of an edge $vz$ contain $v$, so the search stops at the first of them that it reaches and never crosses $vz$. A shortest path in the dual repeats no face, so the $f_i$ are distinct, and a dual edge that leads from a face to itself is never used, because the face is already visited. $\square$

**Claim 7 (each insertion keeps the embedding planar and creates true crossings).** After lines L8 and L9, $\rho$ is planar, and at each $d_i$ the two paths through $d_i$ alternate.

*Proof.* By Lemma 3, line L8 keeps $\rho$ planar and keeps the faces $f_0, \ldots, f_k$, with the dart $(x_i, y_i)$ of $f_{i-1}$ replaced by $(x_i, d_i), (d_i, y_i)$ and the dart $(y_i, x_i)$ of $f_i$ replaced by $(y_i, d_i), (d_i, x_i)$. So $f_{i-1}$ has the corner $(x_i, d_i), (d_i, y_i)$ at $d_i$, and $f_i$ has the corner $(y_i, d_i), (d_i, x_i)$. The edges of line L9 are added one by one: the edge $d_{i-1} d_i$ (with $d_0 = u$ and $d_{k+1} = v$) goes into $f_{i-1}$, at the corner of $d_{i-1}$ in $f_{i-1}$ and the corner of $d_i$ in $f_{i-1}$. The faces $f_0, \ldots, f_k$ are distinct by Claim 6, so when the $i$-th edge is added, the face $f_{i-1}$ and its corners have not been touched by the earlier edges, which only split $f_0, \ldots, f_{i-2}$ and changed corners in those faces. The two ends are distinct and not adjacent. By Lemma 4, each addition keeps $\rho$ planar.

At $d_i$, the edge from the earlier face goes between $y_i$ and $x_i$ (the corner after $y_i$), and the edge to the later face between $x_i$ and $y_i$ (the corner after $x_i$). So $\rho(d_i) = (x_i, d_{i+1}, y_i, d_{i-1})$: the neighbours of the two paths alternate. $\square$

**Claim 8 (every removed edge is crossed).** Every $uv \in R$ is inserted with $k \ge 1$.

*Proof.* Suppose $u$ and $v$ shared a face of $H$ when $uv$ is inserted. Draw $H$ without crossings and add $uv$ inside that face. In this drawing, the edges of $P$ are curves through dummy vertices, the earlier inserted edges are other curves through them, and $uv$ crosses nothing. Erase the earlier inserted edges, and treat the dummy vertices on edges of $P$ as interior points of those curves. What remains is a crossing-free drawing of $P + uv$, which contradicts Claim 1. $\square$

**Claim 9 (each insertion is optimal for the current embedding).** No curve from $u$ to $v$, drawn in the current embedding of $H$ through no vertex and crossing edges transversally, crosses fewer than $k$ edges.

*Proof.* Such a curve starts in a face at $u$, ends in a face at $v$, and passes from one face to the next only when it crosses an edge separating them. So the faces it visits form a walk in the dual from a face at $u$ to a face at $v$, with one dual edge per crossing. The search returns a shortest such walk, of length $k$. $\square$

**Conclusion.** By Claims 7 and 5, after all insertions $\rho$ is a planar rotation system of $H$. Every edge of $G$ in $P$ is a path in $H$ whose inner vertices are dummy vertices of later insertions, and every edge in $R$ is the path $u, d_1, \ldots, d_k, v$; each edge of $H$ lies on exactly one of these paths, since a split replaces one edge of a path by two edges of the same path, and line L9 adds the edges of the new path. Every dummy vertex has degree 4 and lies on exactly two paths, which alternate there by Claim 7. So $(H, \rho)$ is a planarization of $G$ with $|D|$ crossings, built on the maximal planar subgraph $P$ of Claim 1, with at least one crossing per removed edge by Claim 8 and a fewest-crossings route for each insertion in the current embedding by Claim 9. $\blacksquare$
