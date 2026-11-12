---
title: One Doo-Sabin step gives a closed mesh with one face per old face, edge and vertex, keeps the Euler characteristic, and is biquadratic B-spline refinement on a regular grid
proves: [topology, counts, euler-characteristic, stencils, regular-limit]
status: full
---

We use the pseudocode of the page. The input is a closed oriented 2-manifold mesh $M$ with $V$ vertices, $E$ edges and $F$ faces: each directed edge $a \to b$ is in exactly one face, its reverse is in exactly one other face, and the faces around each vertex form one cycle. We write $p(f, v)$ for the new point that line L1 makes at the corner $v$ of the face $f$. Then $\sum_f \deg f = 2E$ and $\sum_v n_v = 2E$, where $n_v$ is the valence of $v$.

**Lemma 1 (the new mesh is a closed oriented 2-manifold).** The directed edges of the new faces are:

- *F-face of $f$:* $p(f, a) \to p(f, b)$ for each directed edge $a \to b$ of $f$;
- *E-face of the edge $ab$, with $a \to b$ in $f$ and $b \to a$ in $g$:* $p(f, b) \to p(f, a)$, $p(f, a) \to p(g, a)$, $p(g, a) \to p(g, b)$ and $p(g, b) \to p(f, b)$;
- *V-face of $v$:* for each edge $vu$, the edge $p(g, v) \to p(f, v)$, where $g$ has $u \to v$ and $f$ has $v \to u$.

Each directed edge is in one new face, and its reverse is in one other new face.

*Proof.* The list is line L2, line L3, and the walk of line L4, which goes from the face $g$ that has the edge $u \to v$ into $v$ to the face $f$ that has $v \to u$. We pair the edges.

- $p(f, a) \to p(f, b)$ of the F-face of $f$ is reversed by the first edge of the E-face of $ab$.
- $p(f, a) \to p(g, a)$ of the E-face of $ab$ is reversed by the V-face of $a$, because $g$ has $b \to a$ into $a$ and $f$ has $a \to b$ out of $a$.
- $p(g, b) \to p(f, b)$ of the E-face of $ab$ is reversed by the V-face of $b$, because $f$ has $a \to b$ into $b$ and $g$ has $b \to a$ out of $b$.

Each old directed edge is in one old face, so each of these new edges comes from one place only. This pairs all edges of the three kinds. Each new point $p(f, v)$ is in exactly four new faces: the F-face of $f$, the V-face of $v$, and the E-faces of the two edges of $f$ at $v$. They form one cycle around it, in the order F-face, E-face, V-face, E-face. $\blacksquare$

**Lemma 2 (counts).** $V' = 2E$, $E' = 4E$, $F' = F + E + V$, and $V' - E' + F' = V - E + F$.

*Proof.* Line L1 makes one point per corner, and there are $\sum_f \deg f = 2E$ corners. There is one new face per old face, edge and vertex. By Lemma 1, each undirected new edge is an edge of an F-face or of a V-face, and the E-faces only share them. There are $\sum_f \deg f = 2E$ edges of F-faces and $\sum_v n_v = 2E$ edges of V-faces, and no edge is of both kinds, so $E' = 4E$. Then $2E - 4E + F + E + V = V - E + F$. $\blacksquare$

**Lemma 3 (weights).** For a face with $k$ sides, the weights $\alpha_0 = \frac{1}{4} + \frac{5}{4k}$ and $\alpha_i = \frac{3 + 2 \cos(2 \pi i / k)}{4k}$ for $0 < i < k$ sum to 1. For $k = 4$ they are $\frac{9}{16}, \frac{3}{16}, \frac{1}{16}, \frac{3}{16}$, which is the average of the corner, the centroid and the two edge midpoints at the corner.

*Proof.* $\alpha_0 = \frac14 + \frac{3 + 2\cos 0}{4k}$, so $\sum_i \alpha_i = \frac{1}{4} + \frac{3k}{4k} + \frac{2}{4k} \sum_{i=0}^{k-1} \cos(2 \pi i / k) = 1$, because the sum of the $k$-th roots of unity is 0 for $k \ge 2$. For $k = 4$ the cosines are $1, 0, -1, 0$. The average $\frac{1}{4}(v + c + \frac{v + a}{2} + \frac{v + b}{2})$, with the centroid $c$ and the neighbors $a, b$ of $v$ in the quad, gives $v$ the weight $\frac14 + \frac1{16} + \frac14 = \frac{9}{16}$, $a$ and $b$ the weight $\frac{1}{16} + \frac{1}{8} = \frac{3}{16}$, and the opposite corner $\frac{1}{16}$. $\blacksquare$

**Theorem (regular grid).** Let $M$ be the $n \times m$ quad grid on a torus with $n, m \ge 3$, with the cell $(i, j)$ on the corners $(i, j), (i{+}1, j), (i{+}1, j{+}1), (i, j{+}1)$. Map the new point at the corner $(i{+}a, j{+}b)$ of the cell $(i, j)$, with $a, b \in \{0, 1\}$, to the fine index $(2i{+}a, 2j{+}b)$. Then the new mesh is the $2n \times 2m$ grid, and its points are the control points of the same biquadratic uniform B-spline surface on the halved knots.

*Proof.* For the corner $(i, j)$ of the cell $(i, j)$, Lemma 3 gives $\frac{9}{16} P_{i,j} + \frac{3}{16}(P_{i+1,j} + P_{i,j+1}) + \frac{1}{16} P_{i+1,j+1}$, which is the tensor product of the weights $(\frac{3}{4}, \frac{1}{4})$ in each direction. The other three corners are the same up to symmetry. [Chaikin's corner cutting](/chaikin-corner-cutting/) maps a closed polygon to the points $\frac34 p_i + \frac14 p_{i+1}$ and $\frac14 p_i + \frac34 p_{i+1}$ at the indices $2i$ and $2i + 1$, and its proof shows that this is knot refinement of the quadratic uniform B-spline curve. So the new points are the biquadratic refinement. For the faces: the F-face of the cell $(i, j)$ is the fine cell $(2i, 2j)$; the E-face of the edge between the cells $(i, j)$ and $(i{+}1, j)$ is the fine cell $(2i{+}1, 2j)$, and the one between $(i, j)$ and $(i, j{+}1)$ is $(2i, 2j{+}1)$; the V-face of the vertex $(i{+}1, j{+}1)$ is the fine cell $(2i{+}1, 2j{+}1)$. These are all $4nm$ fine cells, each once. $\blacksquare$

The limit at an extraordinary face, a face with $k \ne 4$ sides that every later step keeps as an F-face, is $C^1$. This needs the eigen analysis of the subdivision matrix, which Doo and Sabin began in 1978, and Peters and Reif proved the $C^1$ property in 1998 (check). It is not proved here.

**Corollary (regular part).** On a regular grid the limit of the meshes is the biquadratic B-spline surface of the first grid, which is $C^1$.

*Proof.* By the theorem, each step gives new control points of the same surface on finer knots. The control net of a uniform B-spline surface converges to the surface as the knot spacing goes to 0. $\blacksquare$
