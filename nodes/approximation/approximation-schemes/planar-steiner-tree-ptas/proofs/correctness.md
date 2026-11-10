---
title: The approximate tree, the portal graph and the brick states, with a sketch of the structure theorem and the dynamic program
proves: [correctness, time.worst]
status: sketch
---

**Setting.** $G$ is a connected plane graph with positive edge weights, and $Q$ is a set of $k \ge 2$ terminals. $\mathrm{OPT}$ is the least weight of a tree in $G$ that contains $Q$. The *mortar graph* $MG$ is a connected subgraph of $G$ whose faces, other than the outer face, are the *bricks*; a brick $B$ is the subgraph inside and on one face cycle $\partial B$ of $MG$. Each brick has a set of *portals* on $\partial B$, at least one of them. The *portal graph* $B^+$ has the vertices and edges of $MG$, a separate copy of each brick, and an edge of weight 0 from each portal of each copy to the same vertex of $MG$. A terminal on $MG$ is its vertex in $MG$, and a terminal strictly inside a brick is its vertex in the copy of that brick.

Lemmas 1 to 5 have full proofs, and the code checks each of them. The structure theorem and the dynamic program are a sketch after Borradaile, Klein and Mathieu (2009).

**Lemma 1 (the approximate tree, line L1).** The tree of line L1 has weight at most $2(1 - 1/k)\,\mathrm{OPT}$.

*Proof.* Walk around an optimal tree, using each edge twice. The walk has weight $2\,\mathrm{OPT}$ and visits the terminals in some cyclic order $q_1, \ldots, q_k$. The sum of the $k$ distances $d(q_i, q_{i+1})$ is at most $2\,\mathrm{OPT}$, so without the longest one the path $q_1, \ldots, q_k$ in the distance graph weighs at most $2(1 - 1/k)\,\mathrm{OPT}$. The minimum spanning tree of the distance graph on $Q$, which Prim's rule builds, weighs no more than this path. Replacing each of its edges by a shortest path gives a connected subgraph with the same or smaller weight, and a spanning tree of that subgraph is no heavier. $\square$

**Lemma 2 (mapping back, line L6).** A tree in $B^+$ that contains the terminals maps to a connected subgraph of $G$ that contains them, of no larger weight.

*Proof.* Map each vertex of $B^+$ to the vertex of $G$ it copies. An edge of weight 0 maps to a single vertex, and each other edge maps to an edge of the same weight. The image of a connected subgraph is connected, and two edges may map to the same edge, which only lowers the weight. $\square$

So the code always returns a feasible tree, and $\mathrm{OPT} \le \mathrm{ALG} \le \mathrm{OPT}(B^+)$.

**Lemma 3 (the cost of portals).** $\mathrm{OPT}(B^+) \le \mathrm{OPT} + 2 \sum_B w(\partial B)$. If every vertex of every $\partial B$ is a portal, then $\mathrm{OPT}(B^+) = \mathrm{OPT}$.

*Proof.* Let $T^*$ be an optimal tree. Put each edge of $T^*$ that lies in $MG$ into $MG$, and each other edge, which lies in exactly one brick $B$, into the copy of $B$. For each brick whose copy got an edge, add the copy of $\partial B$ and the cycle $\partial B$ in $MG$; the weight added is at most $2 \sum_B w(\partial B)$. Now take an edge $uv$ of $T^*$ at a vertex $v$ of some $\partial B$, with $uv$ in the copy of $B$ and a different edge $vx$ of $T^*$ in $MG$ or another copy. In $B^+$, the copy of $v$ reaches a portal $p$ along the copy of $\partial B$, $p$ reaches $MG$ by its edge of weight 0, and $MG$ reaches $v$ along $\partial B$. So every two edges of $T^*$ that meet at a vertex are joined in the new subgraph, and it is connected and contains all terminals. If every boundary vertex is a portal, the copy of $v$ is joined to $MG$ at $v$ directly, the cycles are not needed, and $\mathrm{OPT}(B^+) \le \mathrm{OPT}$; Lemma 2 gives equality. $\square$

**Lemma 4 (more portals help).** If every portal of one choice is also a portal of a second choice, the second $B^+$ has the same vertices and more edges of weight 0, so its optimum is at most that of the first.

**Lemma 5 (brick states are non-crossing).** Number the portals of a brick $p_1, \ldots, p_\theta$ in order around $\partial B$. For any subgraph $F$ of the brick, the partition of the portals by the components of $F$ is non-crossing: there are no $a < b < c < d$ with $p_a, p_c$ in one component and $p_b, p_d$ in another. So a brick has at most the Catalan number $C_\theta = \frac{1}{\theta + 1}\binom{2\theta}{\theta}$ connection states.

*Proof.* A path in $F$ from $p_a$ to $p_c$ is a curve inside the closed disc bounded by $\partial B$ that splits it into two parts, one containing $p_b$ and the other $p_d$ on the boundary. By the Jordan curve theorem, a path from $p_b$ to $p_d$ inside the disc meets the first one. The graph is plane, so curves of edges meet only at vertices, and the two paths share a vertex, so the two components are one. The non-crossing partitions of $\theta$ points in a circle are counted by $C_\theta$. $\square$

**The structure theorem (sketch).** Borradaile, Klein and Mathieu first cut $G$ open along the tree of Lemma 1, so that all terminals lie on the outer face, whose boundary has weight at most $4\,\mathrm{OPT}$. They then build $MG$ from that boundary and from shortest paths between boundary points, so that $w(MG) \le f(\varepsilon)\,\mathrm{OPT}$ and each brick boundary splits into four paths with a short-path property. Their structure theorem says that some tree of weight at most $(1 + c\varepsilon)\,\mathrm{OPT}$ meets the boundary of each brick in at most $\alpha(\varepsilon)$ vertices. With $\theta$ portals spaced evenly by length on each $\partial B$, each such vertex is moved to a portal at a cost of at most $2\,w(\partial B)/\theta$, and $\sum_B w(\partial B) \le 2\,w(MG)$. So $\theta = \Theta(\alpha(\varepsilon) f(\varepsilon)/\varepsilon)$ makes the total cost of moving at most $\varepsilon\,\mathrm{OPT}$, and $\mathrm{OPT}(B^+) \le (1 + O(\varepsilon))\,\mathrm{OPT}$. Lemma 3 is the version of this step without the structure theorem, where a crossing can cost the whole boundary.

**The dynamic program (sketch).** Contract each brick copy of $B^+$ to one vertex. The result is planar. Its vertices are split into classes by breadth-first levels, and deleting the edges of $MG$ in the lightest of $\eta$ classes costs at most $w(MG)/\eta$; with $\eta = \Theta(f(\varepsilon)/\varepsilon)$ this is at most $\varepsilon\,\mathrm{OPT}$, and the pieces that are left have treewidth $O(\eta)$. A dynamic program over a tree decomposition of each piece keeps, at each brick vertex, a non-crossing partition of its portals (Lemma 5), so $2^{O(\theta)}$ states per brick, and the cost of each brick state is a Steiner tree problem with all terminals on one face of the brick. Each brick takes part in a bounded number of pieces, and the paper gives a total time of $O(n \log n)$ for each fixed $\varepsilon$.

**Running time of the code.** Lines L1 to L4 take $O(k\,n \log n)$ for the shortest paths and $O(n)$ for $B^+$. Line L5 is the Dreyfus-Wagner algorithm in place of the dynamic program, in $O(3^k n + 2^k n \log n)$ time on $B^+$, which has $O(n)$ vertices. Line L6 is linear.
