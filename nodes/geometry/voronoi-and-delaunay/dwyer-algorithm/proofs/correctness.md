---
title: Dwyer's algorithm returns the Delaunay triangulation
proves: [correctness, termination]
status: full
---

**Claim.** Let $S$ be the distinct points of $P$ after line L1, with $n = |S| \ge 2$, and assume that no four points of $S$ lie on one circle. Then DWYER terminates for every number of strips $k$ with $1 \le k \le n/2$. If $S$ lies on one line it returns the empty list; otherwise it returns the unique Delaunay triangulation of $S$.

**Notation.** $\prec$ is the lexicographic order on $(x, y)$. For a finite set $A$, $\mathrm{Del}(A)$ is the set of pairs $pq$ of points of $A$ for which some circle through $p$ and $q$ has all other points of $A$ strictly outside. A *proper structure* for $A$ with respect to an order $<$ is a quad-edge structure that is a plane straight-line graph on $A$ with counterclockwise Onext rings, whose edge set is $\mathrm{Del}(A)$, whose bounded faces are the triangles of the Delaunay triangulation of $A$ when $A$ is not on one line, and with two handles: le, a boundary edge of $\operatorname{conv} A$ out of the $<$-smallest point with the outer face on its right, and re, a boundary edge out of the $<$-largest point with the outer face on its left.

We use two results of the [Guibas-Stolfi correctness proof](/guibas-stolfi-algorithm/), proved there for the order $\prec$ and under the same hypothesis on circles.

- (GS1) For a list $s$ of $m \ge 2$ points sorted by $\prec$, BUILD$(s)$ returns a proper structure for the set of $s$ with respect to $\prec$ (its Lemma 1).
- (GS2) If $A \prec B$ pointwise, $|A|, |B| \ge 2$, and proper structures for $A$ and for $B$ with respect to $\prec$ are given, MERGE returns a proper structure for $A \cup B$ with respect to $\prec$ (its Lemma 8). That proof uses only the properties of a proper structure, not the way it was made.

**Lemma 1 (rotation).** Let $\rho(x, y) = (-y, x)$, the rotation by a quarter turn. Then $\mathrm{orient}(\rho a, \rho b, \rho c) = \mathrm{orient}(a, b, c)$ and $\mathrm{incircle}(\rho a, \rho b, \rho c, \rho d) = \mathrm{incircle}(a, b, c, d)$ for all points. Sorting by the key $(-y, x)$ is sorting by $\rho(p)$ in the order $\prec$. $\mathrm{Del}(\rho A) = \rho\,\mathrm{Del}(A)$.

*Proof.* $\rho$ is linear with determinant $1$, so it keeps the cross product $(b - a) \times (c - a)$. The in-circle determinant has rows $(d_x, d_y, d_x^2 + d_y^2)$ for the differences $d = a - d, b - d, c - d$. $\rho$ maps $(d_x, d_y)$ to $(-d_y, d_x)$, which keeps $d_x^2 + d_y^2$ and multiplies the first two columns by a matrix of determinant $1$, so the determinant is the same. The key $(-y, x)$ is exactly $\rho(x, y)$. A rotation maps circles to circles and keeps inside and outside, which gives the last statement. $\square$

**Lemma 2 (one strip).** Let $B$ be a block of line L3 with $m \ge 2$ points. Lines L4 to L6 make a proper structure for $B$ with respect to $\prec$.

*Proof.* BUILD only reads its input through the order of the list, the two predicates and the quad-edge operations. By Lemma 1, running it on the list of line L4 performs exactly the same operations as running it on the list $\rho(B)$ sorted by $\prec$, and $\rho(B)$ satisfies the hypothesis on circles. By (GS1) the result for $\rho(B)$ is a proper structure for $\rho(B)$ with respect to $\prec$; since $\rho$ keeps plane graphs, counterclockwise order, faces and $\mathrm{Del}$, the same structure on $B$ is a proper structure for $B$ with respect to the order $p < q \iff \rho p \prec \rho q$. Only its handles are wrong for $\prec$.

Line L6 fixes the handles. Its le is a boundary edge with the outer face on its right, so $\mathrm{Sym}$ of it has the outer face on its left, and the walk by Lnext goes once around the boundary of the outer face and back to its start. If $B$ is not on one line, this boundary is the boundary of $\operatorname{conv} B$ traversed clockwise, and it passes through every point of $B$ on that boundary once, because every such point is a vertex of the Delaunay triangulation and the boundary edges are Delaunay edges. If $B$ is on one line, the structure is the path through $B$ in order, and the walk goes along it and back. In both cases the $\prec$-smallest point $v$ of $B$ is the head of exactly one edge $f$ of the walk; $f$ has the outer face on its left, so $\mathrm{Sym}(f)$ is a boundary edge out of $v$ with the outer face on its right. The code returns it as le. In the same way the edge of the walk out of the $\prec$-largest point is a valid re. $\square$

**Lemma 3 (the blocks).** Line L2 gives $1 \le k \le n/2$ (or $k = 1$ when $n < 4$), and the blocks of line L3, with bounds $\lfloor jn/k \rfloor$, are consecutive runs of the $\prec$-sorted list with at least two points each.

*Proof.* Block $j$ has $\lfloor (j+1)n/k \rfloor - \lfloor jn/k \rfloor \ge \lfloor n/k \rfloor \ge 2$ points, as $n/k \ge 2$; for $k = 1$ the block is all of $S$ with $n \ge 2$ points. $\square$

**Lemma 4 (the merge rounds).** At the start of each pass of line L7, the list of handles describes proper structures with respect to $\prec$ for consecutive runs $B_1 \prec B_2 \prec \cdots \prec B_t$ of the sorted list that cover $S$, each with at least two points.

*Proof.* At the first pass this is Lemma 2 and Lemma 3. In a pass, line L8 merges $B_{2j-1}$ and $B_{2j}$; they are consecutive runs, so every point of the first is $\prec$ every point of the second, and both have at least two points, so (GS2) gives a proper structure for their union. A last run without a partner is kept. The new runs are again consecutive, in order, and cover $S$. $\square$

**Proof of the claim.** Each pass of line L7 replaces $t \ge 2$ runs by $\lceil t/2 \rceil < t$ runs, so the loop ends after $\lceil \log_2 k \rceil$ passes with one run, which is $S$. By Lemma 4 the structure is then a proper structure for $S$. If $S$ is on one line, it is a path with no bounded face, and line L9 returns the empty list. Otherwise its bounded faces are the triangles of the unique Delaunay triangulation of $S$, and line L9 lists the faces with three edges and positive area, which are exactly these triangles. Each strip build terminates by the Guibas-Stolfi proof, and each merge terminates by the same proof. $\blacksquare$

*What is not covered.* With four or more cocircular points the Delaunay triangulation is not unique and (GS1) and (GS2) are not proved. The code uses strict tests, and the tests on grids find a Delaunay triangulation each time; this is observed, not proved.
