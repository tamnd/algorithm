---
title: One Catmull-Clark step gives a closed quad mesh with the stated counts and the same Euler characteristic, and on a regular grid it is bicubic B-spline refinement
proves: [topology, counts, euler-characteristic, stencils, regular-limit]
status: full
---

We use the pseudocode of the page. The input is a closed oriented 2-manifold mesh $M = (V, E, F)$: each directed edge $a \to b$ is in exactly one face, its reverse $b \to a$ is in exactly one other face, and the faces around each vertex form one cycle. We write $\deg f$ for the number of vertices of a face and $n_v$ for the valence of a vertex. We also write $V, E, F$ for the counts. Each face has $\deg f$ directed edges, and each edge gives two directed edges, so $\sum_f \deg f = 2E$.

**Lemma 1 (the new mesh is a closed oriented 2-manifold of quads).** Line L5 makes, for each face $f = (v_0, \dots, v_{k-1})$ and each $i$, the quad $Q_{f,i} = (v_i', r_{v_i v_{i+1}}, q_f, r_{v_{i-1} v_i})$, with indices mod $k$.

*Proof.* The directed edges of $Q_{f,i}$ are of two kinds.

- *Between an edge point and a face point.* $Q_{f,i}$ has $r_{v_i v_{i+1}} \to q_f$ and $q_f \to r_{v_{i-1} v_i}$. So for each edge $v_i v_{i+1}$ of $f$, the directed edge $r_{v_i v_{i+1}} \to q_f$ is in $Q_{f,i}$ and its reverse $q_f \to r_{v_i v_{i+1}}$ is in $Q_{f,i+1}$, and in no other quad.
- *Between a vertex point and an edge point.* $Q_{f,i}$ has $v_i' \to r_{v_i v_{i+1}}$ and $r_{v_{i-1} v_i} \to v_i'$. Fix an edge $ab$, with $a \to b$ in face $f$ and $b \to a$ in face $g$. Then $a' \to r_{ab}$ is in the quad of $f$ at the corner $a$, because $a \to b$ leaves $a$ in $f$. Its reverse $r_{ab} \to a'$ is in the quad of $g$ at the corner $a$, because $b \to a$ enters $a$ in $g$. No other quad has either, because each directed edge of $M$ is in one face only.

So each directed edge of the new mesh is in exactly one quad, and its reverse is in exactly one other quad. Around each new vertex the quads form one cycle: around $v'$ they are the quads at the corner $v$ of the faces around $v$, in the cyclic order of those faces; around $r_{ab}$ they are the four quads at the corners $a$ and $b$ of $f$ and $g$; around $q_f$ they are the $\deg f$ quads of $f$ in order. $\blacksquare$

**Lemma 2 (counts).** The new mesh has $V' = V + E + F$, $E' = 2E + \sum_f \deg f = 4E$ and $F' = \sum_f \deg f = 2E$, so $V' - E' + F' = V - E + F$.

*Proof.* Lines L1 to L4 make one point for each face, edge and vertex. Line L5 makes one quad per corner of a face. By the proof of Lemma 1, the undirected new edges are the pairs (vertex, incident edge), which are $2E$, and the pairs (edge, adjacent face), which are $\sum_f \deg f = 2E$. Then $V' - E' + F' = V + E + F - 4E + 2E = V - E + F$. $\blacksquare$

**Lemma 3 (vertex stencil on quads).** If all faces around $v$ are quads, with edge neighbors $e_1, \dots, e_n$ and diagonal vertices $d_1, \dots, d_n$, then

$$v' = \left(1 - \frac{7}{4n}\right) v + \frac{3}{2n^2} \sum_j e_j + \frac{1}{4n^2} \sum_j d_j.$$

*Proof.* The face point of the quad $(v, e_j, d_j, e_{j+1})$ is $(v + e_j + d_j + e_{j+1}) / 4$. Each $e_j$ is in two of the $n$ quads, so the average of the face points is $Q = v/4 + \frac{1}{2n} \sum e_j + \frac{1}{4n} \sum d_j$. The average of the midpoints is $R = v/2 + \frac{1}{2n} \sum e_j$. Then

$$Q + 2R + (n - 3) v = \left(n - \tfrac{7}{4}\right) v + \frac{3}{2n} \sum e_j + \frac{1}{4n} \sum d_j,$$

and line L4 divides by $n$. $\blacksquare$

For $n = 4$ the weights are $9/16$, $3/32$ and $1/64$, and for $n = 3$ they are $5/12$, $1/6$ and $1/36$.

**Lemma 4 (edge stencil on quads).** If $ab$ is in the quads $(a, b, c, d)$ and $(b, a, e, f)$, then $r_{ab} = \frac{3}{8}(a + b) + \frac{1}{16}(c + d + e + f)$.

*Proof.* Line L2 gives $\frac{1}{4}\left(a + b + \frac{a + b + c + d}{4} + \frac{b + a + e + f}{4}\right)$, which is the claim. $\blacksquare$

**Theorem (regular grid).** Let $M$ be the $n \times m$ quad grid on a torus with $n, m \ge 3$, with control points $P_{i,j}$. Map the vertex point of $(i, j)$ to the fine index $(2i, 2j)$, the edge points of $(i, j)(i{+}1, j)$ and $(i, j)(i, j{+}1)$ to $(2i{+}1, 2j)$ and $(2i, 2j{+}1)$, and the face point of the cell at $(i, j)$ to $(2i{+}1, 2j{+}1)$. Then the new mesh is the $2n \times 2m$ grid, and its points are the control points of the same periodic bicubic uniform B-spline surface on the halved knots.

*Proof.* For a closed cubic uniform B-spline curve, halving every knot interval gives the new points $\frac{1}{8}(p_{i-1} + 6 p_i + p_{i+1})$ at the even indices and $\frac{1}{2}(p_i + p_{i+1})$ at the odd ones. This is the case $d = 3$ of the [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/), and its proof shows that the curve does not change. For a tensor product surface, the refinement in each direction is applied to the rows and then to the columns, so the new point at $(2i, 2j)$ has the weights $\frac{1}{64}(1, 6, 1) \otimes (1, 6, 1)$, the point at $(2i{+}1, 2j)$ has $\frac{1}{16}(1, 1) \otimes (1, 6, 1)$, and the point at $(2i{+}1, 2j{+}1)$ has $\frac{1}{4}(1, 1) \otimes (1, 1)$. These are $9/16$, $3/32$, $1/64$ for the vertex, $3/8$ and $1/16$ for the edge, and $1/4$ for the face. They are the weights of Lemma 3 with $n = 4$, of Lemma 4, and of line L1. The new quads of line L5 join the fine indices $(2i, 2j), (2i{+}1, 2j), (2i{+}1, 2j{+}1), (2i, 2j{+}1)$ and their shifts, which are the cells of the fine grid. $\blacksquare$

The claim that the limit is $C^1$ at an extraordinary vertex is not proved here. It needs the eigen analysis of the subdivision matrix and a test of the characteristic map. Doo and Sabin started this analysis in 1978, and Peters and Reif gave a full proof for Catmull-Clark (check).

**Corollary (regular part).** On a regular grid the limit of the meshes is the bicubic B-spline surface of the first grid, which is $C^2$. The same holds over the inner cell of each $3 \times 3$ block of regular quads in any mesh.

*Proof.* By the theorem, each step gives new control points of the same surface on finer knots. The control polygon of a uniform B-spline converges to the surface as the knot spacing goes to 0, so the meshes converge to it. The weights of lines L1 to L4 use only the faces that touch a vertex, edge or face. The four inner vertices of a $3 \times 3$ block are surrounded by the four quads of the block, so they have valence 4. The new points of the $5 \times 5$ fine block over the inner cell are vertex points of these four vertices and edge and face points inside the block, so they depend only on the 16 vertices of the block, with the same weights as on a regular grid. Each of the four fine cells of the inner cell is again the inner cell of a $3 \times 3$ block of quads in that fine block, so the argument repeats at every level. The limit over the inner cell is therefore the same as on a regular grid, which is the bicubic patch of the 16 control points. $\blacksquare$
