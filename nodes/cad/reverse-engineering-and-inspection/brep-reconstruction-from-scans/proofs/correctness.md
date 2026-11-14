---
title: From exact samples of a polyhedron with simple vertices, the algorithm stops and returns its planes, adjacency, vertices, edges and face loops
proves: [correctness, termination]
status: full
---

**Setup.** $P$ is a closed polyhedron with faces $1, \dots, F$. Each face $f$ is a polygon without holes in the plane $\Pi_f = \{x : n_f \cdot x = c_f\}$ with $\lvert n_f \rvert = 1$. An edge of $P$ is a segment between two distinct vertices and lies in exactly two faces. The input regions $R_1, \dots, R_F$ and the distances $\delta, \eta$ satisfy:

- **H1.** $R_f$ lies on face $f$ and has three points that are not on one line.
- **H2.** For faces $j \ne k$: some $p \in R_j$ and $q \in R_k$ have $\lvert p - q \rvert \le \delta$ if and only if $j$ and $k$ share an edge.
- **H3.** Every vertex $v$ is simple: exactly three faces contain it, and for each pair of them exactly one edge at $v$ lies in both. Two faces share at most one edge. Each of the three regions of the faces at $v$ has a point within $\eta$ of $v$, and distinct vertices are more than $\eta$ apart.
- **H4.** If three faces pairwise share an edge but no vertex lies on all three, then their planes have no unique common point, or that point is farther than $\eta$ from one of the three regions.
- **H5.** At every edge between faces $j$ and $k$, $\lvert n_j \times n_k \rvert$ is at least the threshold of line L3, and at every vertex with faces $j, k, l$, $\lvert \det(n_j, n_k, n_l) \rvert$ is at least the threshold of line L4.

Arithmetic is exact, and the $3 \times 3$ symmetric eigenproblem of line L1 is solved exactly, as on the real RAM.

**Lemma 1 (line L1).** Under H1, line L1 returns the plane $\Pi_f$, as $(n_f, c_f)$ or $(-n_f, -c_f)$.

*Proof.* Let $c$ be the centroid of $R_f$ and $C = \sum_{p \in R_f} (p - c)(p - c)^\mathsf{T}$. Every $p - c$ lies in the plane $\Pi_f$ moved to the origin, so $(p - c) \cdot n_f = 0$ and $C n_f = 0$. For a unit $u \perp n_f$, $u^\mathsf{T} C u = \sum ((p - c) \cdot u)^2$; if this were $0$, every $p - c$ would be orthogonal to $u$ and to $n_f$, so all points would lie on the line through $c$ with the direction $n_f \times u$, against H1. So $C$ is positive semidefinite, $0$ is a simple eigenvalue with the eigenvectors $\pm n_f$, and all other eigenvalues are positive. The eigenvector of the smallest eigenvalue is $\pm n_f$, and the offset is $\pm n_f \cdot c = \pm c_f$, since $c$ lies in $\Pi_f$. $\square$

**Lemma 2 (line L2).** Line L2 returns exactly the pairs $j < k$ with $p \in R_j$, $q \in R_k$ and $\lvert p - q \rvert \le \delta$. Under H2 this is the set of pairs of faces that share an edge.

*Proof.* The code puts each point $p$ in the cell $(\lfloor p_1 / \delta \rfloor, \lfloor p_2 / \delta \rfloor, \lfloor p_3 / \delta \rfloor)$ and compares each point with all points of the $27$ cells whose indices differ from its own by at most $1$ in each coordinate. It adds a pair only after it tests the distance, so every pair it adds is close. Conversely, if $\lvert p - q \rvert \le \delta$ with $p \in R_j$, $q \in R_k$, $j < k$, then $\lvert p_i - q_i \rvert \le \delta$ for each $i$, so $\lfloor p_i / \delta \rfloor$ and $\lfloor q_i / \delta \rfloor$ differ by at most $1$; when the code visits $p$ it compares it with $q$ and adds $(j, k)$, unless the pair is there already. $\square$

From now on, by Lemmas 1 and 2, the planes are the planes of the faces and $A$ is the set of pairs of faces that share an edge.

**Lemma 3 (line L3).** For $\{j, k\} \in A$, line L3 returns a point and a direction of the line $\Pi_j \cap \Pi_k$, and every edge between $j$ and $k$ lies on this line.

*Proof.* Let $d = n_j \times n_k$; by H5, $d \ne 0$ and the code does not return none. By the cyclic rule of the triple product, $n_j \cdot (n_k \times d) = d \cdot (n_j \times n_k) = \lvert d \rvert^2$ and $n_k \cdot (d \times n_j) = d \cdot (n_j \times n_k) = \lvert d \rvert^2$, while $n_j \cdot (d \times n_j) = 0$ and $n_k \cdot (n_k \times d) = 0$. So $x_0 = (c_j (n_k \times d) + c_k (d \times n_j)) / \lvert d \rvert^2$ has $n_j \cdot x_0 = c_j$ and $n_k \cdot x_0 = c_k$. The direction $d$ is orthogonal to both normals, and two planes with independent normals meet in exactly one line, so the line is $x_0 + \mathbb{R} d$. An edge between $j$ and $k$ lies in both faces, so in both planes and on the line. $\square$

**Lemma 4 (lines L4 and L5).** After line L5 the vertices are exactly the vertices of $P$, each once, and the face set of each is the set of the three faces that contain it.

*Proof.* Take a vertex $v$ with faces $j, k, l$. By H3, each pair of them shares an edge, so $\{j, k, l\}$ is a triangle of $A$. By H5 the normals are independent and the system of line L4 has one solution, which is $v$, since $v$ lies on the three planes. By H3 each of the three regions has a point within $\eta$ of $v$. So line L4 keeps $v$.

Take a triangle $\{j, k, l\}$ of $A$ that is not the face set of a vertex. If some vertex $w$ lay on all three faces, then by H3 its faces would be exactly $j, k, l$, which is excluded. So H4 applies: either the planes have no unique common point, and line L4 gets none (when the determinant is $0$ or below the threshold), or the point is farther than $\eta$ from one region, and line L4 drops it. So line L4 keeps no point from such a triangle.

So the kept points are the vertices of $P$, each kept once, from the triangle of its own faces. In line L5, each new point is compared with the points kept before it; these are other vertices of $P$, which by H3 are more than $\eta$ away, so no merge happens, and each vertex keeps the face set $\{j, k, l\}$. $\square$

**Lemma 5 (line L6).** Line L6 returns exactly the edges of $P$, each once, with the pair of faces that contain it.

*Proof.* Take $\{j, k\} \in A$, and let $e$ be the edge between $j$ and $k$, which exists by Lemma 2 and is unique by H3. Its two endpoints lie in both faces, so by Lemma 4 they are vertices whose face sets contain $j$ and $k$. Conversely, let $v$ be a vertex whose face set contains $j$ and $k$. By H3 some edge at $v$ lies in both $j$ and $k$; by uniqueness it is $e$, so $v$ is an endpoint of $e$. So the list of line L6 has exactly the two endpoints of $e$, which are distinct, the line of Lemma 3 exists, and the pairing gives the one edge $(u, w, (j, k))$ with the endpoints of $e$. Every edge of $P$ lies in two faces that then share it, so every edge of $P$ arises from its pair in $A$, and only once. $\square$

**Lemma 6 (line L7).** For each face $f$, line L7 returns the vertices of $f$ in the order of its boundary.

*Proof.* By Lemma 5, the edges whose face pair contains $f$ are exactly the edges of the polygon $f$. A polygon without holes has a boundary that is one simple cycle of $s \ge 3$ edges, so in the graph of these edges every vertex has exactly two distinct neighbors, and the code does not return the empty loop. The walk starts at a vertex and each step moves to the neighbor of the current vertex other than the one it came from, so it follows the cycle in one direction, visits each of the $s$ vertices once, and returns to the start after $s$ steps. The list then has $s$ vertices, which is the number of vertices of the graph, and the code returns it. $\square$

**Theorem 1 (termination).** On every input the algorithm stops.

*Proof.* Lines L1 to L6 are loops over finite sets: the regions, the points of $27$ cells for each point, the pairs in $A$, the triples of faces, the kept vertices and the vertices on a line. In the code, the eigenproblem of line L1 uses at most a fixed number of Jacobi sweeps. In line L7, the walk starts only when every vertex of the edge graph of $f$ has exactly two neighbors. A finite graph in which every vertex has degree $2$ is a disjoint union of cycles, and the component of the start is one cycle of some length $s \ge 2$, since an edge joins two distinct vertices. For $s \ge 3$ the walk follows the cycle as in Lemma 6 and is back at the start after $s$ steps. For $s = 2$, the start $a$ has the neighbor $b$ twice and $b$ has $a$ twice; the walk goes to $b$, where both neighbors are $a$, and stops. So every walk stops after at most as many steps as the graph has vertices. $\square$

**Theorem 2 (correctness).** Under H1 to H5 the algorithm returns the planes of the faces of $P$, the pairs of faces of $P$ that share an edge, the vertices of $P$ with their faces, the edges of $P$ with their faces, and the boundary cycle of each face. In particular $V - E + F$ of the result equals that of $P$, which is $2 - 2g$ for a polyhedron of genus $g$ whose faces are disks; so the check $V - E + F = 2$ passes exactly when $P$ has no handles.

*Proof.* Lemmas 1 to 6 give the parts in turn, and Theorem 1 shows that the algorithm returns them. The counts of the result are the counts of $P$. For a closed polyhedral surface whose faces are disks, $V - E + F = 2 - 2g$ by the Euler-Poincaré formula. $\square$

**Corollary 1 (the box of the example).** For the box $[0, a] \times [0, b] \times [0, c]$ with $a, b, c > 0$, sampled at the centers of cells of side $s$ that divide the sides, with $s \le \min(a, b, c) / 2$, $s / \sqrt 2 \le \delta < \min(a, b, c)$ and $s / \sqrt 2 \le \eta < \min(a, b, c)$, the algorithm returns the $8$ corners, the $12$ edges and the $6$ faces of the box, with $V - E + F = 2$.

*Proof.* Each face has at least $2 \times 2$ cell centers, which are not on one line, so H1 holds. For two faces that share an edge, the two sample points nearest to the edge are at distance $s / 2$ from it, orthogonally in the two faces, so they are $s / \sqrt 2 \le \delta$ apart. Two opposite faces are at distance at least $\min(a, b, c) > \delta$. So H2 holds. Each corner is simple, each pair of its faces shares one edge, and two faces share at most one edge. The nearest point of each face to a corner is the center of the corner cell, at $s / \sqrt 2 \le \eta$, and two corners are at least $\min(a, b, c) > \eta$ apart; so H3 holds. Three pairwise adjacent faces take one face from each pair of opposite faces, so they always have a common corner, and H4 holds with nothing to check. The normals are the unit vectors of the axes, so $\lvert n_j \times n_k \rvert = 1$ and $\lvert \det \rvert = 1$, and H5 holds. Theorem 2 gives the claim, with $g = 0$. $\square$

**What is not proved.** Nothing is proved for noisy data. With noise, the planes of line L1 are only near the true planes, the vertices and edges move with them, and the choice of $\delta$ and $\eta$ decides whether faces are joined and corners merged correctly; the page reports measurements for this, not a bound. Vertices with four or more faces, faces with holes, and curved faces are outside the hypotheses. In floating point, the corners of the example agree with the true corners within $10^{-12}$ in the tests. $\blacksquare$
