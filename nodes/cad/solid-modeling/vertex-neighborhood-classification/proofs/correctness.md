---
title: Vertex neighborhood classification returns the boundary of the regularized result
proves: [correctness]
status: full
---

The proof is for the planar form of the algorithm on the page. Let $A$ and $B$ be simple polygons, each given as a counterclockwise loop, so that the polygon is on the left of each edge. Let $X = A \operatorname{op}^* B$ for op in union, intersection and difference. All coordinates are rational and all signs are exact.

**Lemma 1 (generate).** After line L1, two edges, one of $A$ and one of $B$, are equal as point sets or meet at most in common end points. Every point of $\partial A \cap \partial B$ is a vertex of both split loops or lies on a pair of equal edges.

*Proof.* If two original edges cross at one point, that point is a cut of both. If they overlap along a segment, the ends of the overlap are cuts of both. So after the cuts, a split edge of $A$ meets a split edge of $B$ only at an end of both, or the two edges have the same two ends and lie on one line, which makes them equal. $\square$

**Lemma 2 (classify).** Let $e = (u, w)$ be a split edge of $A$ with relative interior $\operatorname{ri} e$. Exactly one of these holds, and line L3, L4 or L5 returns it: $\operatorname{ri} e \subseteq \operatorname{int} B$ (in), $\operatorname{ri} e \cap B = \emptyset$ (out), $e$ is an edge of $B$ in the same direction (on-same), or in the opposite direction (on-opposite).

*Proof.* If $e$ is not an edge of $B$, then by Lemma 1 the set $\operatorname{ri} e$ misses $\partial B$. It is connected, so it lies in $\operatorname{int} B$ or outside $B$. This is the dichotomy. Line L3 detects the two on cases. For line L4, let $u$ be on $\partial B$. By Lemma 1, $u$ is a vertex of the split loop of $B$, with outgoing direction $d_{\text{out}}$ and the direction $d_{\text{back}}$ toward the previous vertex. Since $B$ is on the left of both of its edges at $u$, a small disk around $u$ meets $\operatorname{int} B$ exactly in the open sector swept counterclockwise from $d_{\text{out}}$ to $d_{\text{back}}$. The direction $d = w - u$ differs from both, since otherwise $e$ would overlap an edge of $B$ and, by Lemma 1, be equal to it. So the points of $e$ near $u$ are in $\operatorname{int} B$ exactly when $d$ is inside the sector, which is the test of line L4 with the pseudo-angle, a strictly increasing function of the angle. For line L5, the tail $u$ is not on $\partial B$, so a small disk around $u$ is inside $B$ or outside $B$, and the previous edge, which ends at $u$, has the same class. The walk starts at a vertex on $\partial B$, so every edge reached by line L5 follows an edge already classified. If no vertex of the loop is on $\partial B$, then by Lemma 1 the loop misses $\partial B$, so the whole loop is in $\operatorname{int} B$ or outside $B$, and one point in polygon test decides it. $\square$

The same lemma holds for the edges of $B$ against $A$.

**Lemma 3 (select).** Call $S$ the list of directed edges built at line L6. A point $x$ in the relative interior of a split edge lies on $\partial X$ if and only if it lies on an edge of $S$. Each such $x$ lies on exactly one edge of $S$, and $X$ is on the left of that edge near $x$.

*Proof.* Take $x \in \operatorname{ri} e$ for a split edge $e$ of $A$, and a small disk $U$ around $x$ that meets no other split edge, except a copy of $e$ in $B$. Then $A \cap U$ is the closed half-disk $H$ on the left of $e$. By Lemma 2, $B \cap U$ is $U$ (in), $\emptyset$ (out), $H$ (on-same) or the closed half-disk $H'$ on the right (on-opposite). The regularized result in $U$ for each case:

| class of $e$ | $A \cup^* B$ | $A \cap^* B$ | $A -^* B$ |
|---|---|---|---|
| in | $U$ | $H$ | $\emptyset$ |
| out | $H$ | $\emptyset$ | $H$ |
| on-same | $H$ | $H$ | $\emptyset$ |
| on-opposite | $U$ | $\emptyset$ | $H$ |

For on-opposite, $H \cap H'$ is the segment, whose regularization is empty, and $H \setminus H'$ is $H$ without the segment, whose regularization is $H$. The point $x$ is on $\partial X$ exactly in the cells with $H$, and then $X$ is on the left of $e$. These cells are the classes that the table SELECT keeps from $A$. Now take $x \in \operatorname{ri} e$ for a split edge $e$ of $B$ that is not an edge of $A$. Then $B \cap U$ is the half-disk $G$ on the left of $e$, and $A \cap U$ is $U$ or $\emptyset$. The result is $U$ or $G$ for the union, $G$ or $\emptyset$ for the intersection, and for the difference it is the closed half-disk on the right of $e$ when $e$ is in $A$, and $\emptyset$ when $e$ is out of $A$. These are the classes kept from $B$, and for the difference the edge is reversed, which puts the result on its left. The on edges of $B$ are equal to edges of $A$ and are never kept from $B$, so each boundary point is on one edge of $S$ only. $\square$

**Lemma 4 (connect).** At every vertex $v$, the edges of $S$ that start at $v$ and those that end at $v$ alternate in angular order around $v$, and there are as many of each. So the rule of line L10 is a bijection from the edges that end at $v$ to the edges that start at $v$, and CONNECT splits $S$ into closed loops that use each edge once.

*Proof.* Let $\chi$ be the indicator of $X$. Walk counterclockwise on a small circle around $v$ that meets only the split edges at $v$. By Lemma 3, $\chi$ changes exactly where the circle crosses an edge of $S$, and $X$ is on the left of that edge. An edge that starts at $v$ has its left side counterclockwise from it, so the walk enters $X$ there. An edge that ends at $v$ has its left side clockwise from it, so the walk leaves $X$ there. Since $\chi$ takes only the values $0$ and $1$, entries and exits alternate around the circle, which gives the claim. Rotating clockwise from the direction of an incoming edge, the next edge met is an outgoing one, so line L10 picks the outgoing edge next to it in clockwise order, which is a bijection. A bijection at each vertex makes the successor map a permutation of $S$, so each traced loop returns to its first edge. $\square$

**Theorem.** BOOLEAN$(A, B, \operatorname{op})$ returns loops whose union is $\partial X$, with $X$ on the left of every edge. For every point $x$ not on the loops, the winding number of the loops around $x$ is $1$ if $x \in X$ and $0$ otherwise.

*Proof.* By Lemma 3, every point of $\partial X$ in the relative interior of a split edge is on an edge of $S$, and every edge of $S$ lies in $\partial X$. The rest of $\partial X$ is a finite set of vertices, which are end points of edges of $S$ because $\partial X$ has no isolated points for a regular closed set. By Lemma 4, the loops use exactly the edges of $S$. For the winding number $w$, both $w$ and $\chi$ are $0$ far away, both are constant off the edges of $S$ and off $\partial X$, and both jump by $+1$ when a path crosses an edge of $S$ from its right to its left at a relative interior point, by Lemma 3. Any two points off the edges can be joined by a path that crosses edges only at such points, since the vertices are finite. So $w = \chi$ off the loops. $\blacksquare$

**Termination.** GENERATE and CLASSIFY loop over finite lists. Each step of CONNECT marks one new edge as used, so it ends after $|S|$ steps.

**From the plane to space.** In three dimensions, Lemma 2 becomes the classification of the sectors around a vertex: the cones between consecutive faces at that vertex, each in, out, or on a face of the other solid with the same or the opposite normal. Lemma 3 becomes the same table for the face pieces, and Lemma 4 becomes the step that joins the cut edges of the two solids into the new faces. The planar proof does not cover the Euler operator steps of the solid version.
