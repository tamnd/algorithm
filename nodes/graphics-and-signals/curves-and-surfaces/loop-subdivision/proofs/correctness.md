---
title: One Loop step gives a closed triangle mesh with V + E vertices and 4F triangles, keeps the Euler characteristic, and is quartic box spline refinement on a regular mesh
proves: [topology, counts, euler-characteristic, stencils, regular-limit, limit-position]
status: full
---

We use the pseudocode of the page. The input is a closed oriented 2-manifold triangle mesh $M$ with $V$ vertices, $E$ edges and $F$ triangles: each directed edge $a \to b$ is in exactly one triangle, its reverse $b \to a$ is in exactly one other triangle, and the triangles around each vertex form one cycle. We write $e_{ab} = e_{ba}$ for the edge point of the edge $ab$, and $n_v$ for the valence of $v$. Because each triangle has 3 edges and each edge is in 2 triangles, $3F = 2E$, and $\sum_v n_v = 2E$.

**Lemma 1 (the new mesh is a closed oriented 2-manifold).** Line L3 makes, for each old triangle $(a, b, c)$, the corner triangles $(a, e_{ab}, e_{ca})$, $(b, e_{bc}, e_{ab})$, $(c, e_{ca}, e_{bc})$ and the middle triangle $(e_{ab}, e_{bc}, e_{ca})$. Each new directed edge is in one new triangle, and its reverse is in one other new triangle.

*Proof.* The new directed edges are of two kinds.

- *Half edges of old edges.* The old directed edge $a \to b$ of $(a, b, c)$ gives $a \to e_{ab}$ in the corner triangle at $a$ and $e_{ab} \to b$ in the corner triangle at $b$. The reverse $b \to a$ is in the other old triangle $(b, a, d)$, which gives $b \to e_{ab}$ and $e_{ab} \to a$. So $a \to e_{ab}$ and $e_{ab} \to a$ pair up, and so do $e_{ab} \to b$ and $b \to e_{ab}$.
- *Inner edges.* In $(a, b, c)$, the corner triangle at $a$ has $e_{ab} \to e_{ca}$, and the middle triangle has $e_{ca} \to e_{ab}$. The same holds at $b$ and at $c$. These edges join two edge points of the same old triangle, so no other old triangle makes them.

Each old directed edge is in one old triangle, so each new directed edge comes from one place only. The triangles around an old vertex $v$ are the corner triangles at $v$ of the $n_v$ old triangles around it, in the same cyclic order. The triangles around an edge point $e_{ab}$ are, in order, the corner triangle at $a$, the middle triangle and the corner triangle at $b$ of $(a, b, c)$, and the same three of $(b, a, d)$. So each vertex has one cycle of triangles, and an edge point has valence 6. $\blacksquare$

**Lemma 2 (counts).** $V' = V + E$, $E' = 2E + 3F$, $F' = 4F$, and $V' - E' + F' = V - E + F$.

*Proof.* Lines L1 and L2 make one point per old edge and one per old vertex. Line L3 makes 4 triangles per old triangle. By Lemma 1, the undirected new edges are the 2 halves of each old edge and the 3 inner edges of each old triangle. Then $(V + E) - (2E + 3F) + 4F = V - E + F$. $\blacksquare$

**Lemma 3 (weights).** The weights of line L1 are $\frac38, \frac38, \frac18, \frac18$, and the weights of line L2 are $1 - n\beta_n$ and $n$ times $\beta_n$. Both sets sum to 1. With $\beta_n = \frac{1}{n}\left(\frac58 - \left(\frac38 + \frac14 \cos\frac{2\pi}{n}\right)^2\right)$, $\beta_3 = \frac{3}{16}$, $\beta_4 = \frac{31}{256}$ and $\beta_6 = \frac{1}{16}$.

*Proof.* The sums are clear. For $n = 3$ the cosine is $-\frac12$, so $\frac38 + \frac14 \cos = \frac14$ and $\beta_3 = \frac13\left(\frac58 - \frac1{16}\right) = \frac{3}{16}$. For $n = 4$ the cosine is 0, so $\beta_4 = \frac14\left(\frac58 - \frac{9}{64}\right) = \frac{31}{256}$. For $n = 6$ the cosine is $\frac12$, so $\frac38 + \frac18 = \frac12$ and $\beta_6 = \frac16 \cdot \frac38 = \frac{1}{16}$. $\blacksquare$

**Theorem (regular mesh).** Let $M$ be the regular triangle mesh on an $n \times m$ torus grid with $n, m \ge 3$: the vertex $(i, j)$ is $p_{i,j}$, indices are taken modulo $n$ and $m$, and each cell $(i, j)$ is cut into the triangles $((i,j), (i{+}1,j), (i{+}1,j{+}1))$ and $((i,j), (i{+}1,j{+}1), (i,j{+}1))$. Every vertex has valence 6. Give the vertex point of $(i, j)$ the fine index $(2i, 2j)$, and the edge point of the edge from $(i, j)$ to $(i, j) + d$ the fine index $(2i, 2j) + d$, for $d \in \{(1,0), (0,1), (1,1)\}$. Then the new point at the fine index $\alpha$ is
$$q_\alpha = \sum_\beta a_{\alpha - 2\beta + (2,2)}\, p_\beta, \qquad \sum_\alpha a_\alpha x^{\alpha_1} y^{\alpha_2} = \tfrac{1}{16}(1 + x)^2 (1 + y)^2 (1 + xy)^2.$$
This is the subdivision mask of the quartic box spline with the directions $(1,0)$, $(0,1)$ and $(1,1)$, each twice. So one step gives the control points of the same box spline surface on the grid of half the spacing.

*Proof.* Write $a_{r,s}$ for the coefficient of $x^r y^s$ times 16. A term of the product is $\binom{2}{u} x^u \binom{2}{w} y^w \binom{2}{c} (xy)^c$, so $a_{r,s} = \sum_c \binom{2}{r - c}\binom{2}{s - c}\binom{2}{c}$ over $0 \le c \le 2$. The values we need are:

| $(r, s)$ | terms | $16\, a_{r,s}$ |
|---|---|---|
| $(2, 2)$ | $1 + 8 + 1$ | 10 |
| $(0,0), (4,4), (2,0), (0,2), (4,2), (2,4)$ | one term each | 1 |
| $(1, 2), (3, 2), (2, 1), (2, 3), (1, 1), (3, 3)$ | $2 + 4$ | 6 |
| $(1, 0), (3, 4), (0, 1), (4, 3), (1, 3), (3, 1)$ | one term each | 2 |
| $(3, 0), (1, 4), (0, 3), (4, 1)$ | none | 0 |

*Vertex points.* For $\alpha = (2i, 2j)$, only even entries of the mask are used. The center $\beta = (i, j)$ gets $\frac{10}{16}$, and the six $\beta$ at $(i \pm 1, j)$, $(i, j \pm 1)$, $(i + 1, j + 1)$ and $(i - 1, j - 1)$ get $\frac{1}{16}$. These six are the neighbors of $(i, j)$ in $M$. Line L2 with $n = 6$ and $\beta_6 = \frac1{16}$ gives $1 - \frac{6}{16} = \frac{10}{16}$ and $\frac{1}{16}$, the same weights.

*Edge points.* For $\alpha = (2i + 1, 2j)$, the edge from $(i, j)$ to $(i + 1, j)$, the first entry is odd, so $\beta_1 \in \{i, i + 1\}$, and the second is even, so $\beta_2 \in \{j - 1, j, j + 1\}$. The ends $(i, j)$ and $(i + 1, j)$ get $a_{3,2} = a_{1,2} = \frac{6}{16} = \frac38$. The point $(i + 1, j + 1)$ gets $a_{1,0} = \frac18$, and $(i, j - 1)$ gets $a_{3,4} = \frac18$. The points $(i, j + 1)$ and $(i + 1, j - 1)$ get $a_{3,0} = a_{1,4} = 0$. The two triangles on this edge are $((i,j), (i{+}1,j), (i{+}1,j{+}1))$ of the cell $(i, j)$ and $((i,j{-}1), (i{+}1,j), (i,j))$ of the cell $(i, j - 1)$, so the opposite vertices are $(i + 1, j + 1)$ and $(i, j - 1)$, and line L1 gives the same weights. The case $\alpha = (2i, 2j + 1)$ is the same with the two coordinates swapped, since the mask and the mesh are symmetric under that swap. For $\alpha = (2i + 1, 2j + 1)$, the diagonal from $(i, j)$ to $(i + 1, j + 1)$, both entries are odd, so $\beta \in \{i, i+1\} \times \{j, j+1\}$. The ends get $a_{3,3} = a_{1,1} = \frac38$, and $(i + 1, j)$ and $(i, j + 1)$ get $a_{1,3} = a_{3,1} = \frac18$. These are the opposite vertices of the two triangles of the cell $(i, j)$, so line L1 again gives the same weights.

*Faces.* By line L3, the four new triangles of $((i,j), (i{+}1,j), (i{+}1,j{+}1))$ have the fine indices $((2i,2j), (2i{+}1,2j), (2i{+}1,2j{+}1))$, $((2i{+}2,2j), (2i{+}2,2j{+}1), (2i{+}1,2j))$, $((2i{+}2,2j{+}2), (2i{+}1,2j{+}1), (2i{+}2,2j{+}1))$ and $((2i{+}1,2j), (2i{+}2,2j{+}1), (2i{+}1,2j{+}1))$. Up to a cyclic shift, these are the first triangle of the fine cell $(2i, 2j)$, both triangles of the fine cell $(2i{+}1, 2j)$, and the first triangle of the fine cell $(2i{+}1, 2j{+}1)$ of the regular mesh on the $2n \times 2m$ grid. In the same way, the other old triangle of the cell gives the second triangles of the fine cells $(2i, 2j)$ and $(2i{+}1, 2j{+}1)$ and both triangles of $(2i, 2j{+}1)$. So the new mesh is the regular mesh on the fine grid.

The box spline $B$ with these six directions satisfies the refinement equation $B(t) = \sum_\alpha a_\alpha B(2t - \alpha)$ with the mask above, because each direction $d$ adds the factor $\frac{1}{2}(1 + z^d)$ and the factor 4 comes from the scale in two dimensions. So $\sum_\beta p_\beta B(t - \beta) = \sum_\alpha q_\alpha B(2t - \alpha + (2,2))$, which is the claim. $\blacksquare$

**Corollary (regular part).** On a regular mesh the limit of the meshes is the quartic three direction box spline surface of the first mesh, which is $C^2$.

*Proof.* By the theorem, each step gives new control points of the same surface on a finer grid. The box spline with the directions $(1,0), (0,1), (1,1)$, each twice, has continuity $C^{r-2}$, where $r = 4$ is the least number of directions that must be removed to leave a set that does not span the plane. So it is $C^2$. The control net of a box spline surface converges to the surface as the grid spacing goes to 0. $\blacksquare$

**Lemma 4 (limit position).** Let $v$ have valence $n$ and the neighbors $u_1, \dots, u_n$, and let $\omega = \frac{3}{8 \beta_n}$. Then $L(v) = \frac{\omega v + \sum_j u_j}{\omega + n}$ has the same value before and after one step, with the new point $v'$ and its new neighbors $e_{v u_j}$.

*Proof.* The new neighbors of $v'$ are the $n$ edge points $e_{v u_j} = \frac38 (v + u_j) + \frac18 (u_{j-1} + u_{j+1})$, with indices modulo $n$. Their sum is $\frac{3n}{8} v + \frac38 \sum_j u_j + \frac{2}{8} \sum_j u_j = \frac{3n}{8} v + \frac58 \sum_j u_j$. Then
$$\omega v' + \sum_j e_{v u_j} = \left(\omega (1 - n \beta_n) + \frac{3n}{8}\right) v + \left(\omega \beta_n + \frac58\right) \sum_j u_j = \omega v + \sum_j u_j,$$
because $\omega \beta_n = \frac38$. $\blacksquare$

The limit at an extraordinary vertex, a vertex of valence $n \ne 6$, is $C^1$ with Loop's $\beta_n$. This needs the eigen analysis of the subdivision matrix, which Loop began in 1987 and later authors made complete (check). It is not proved here. We use only that the meshes converge, so that the ring of $v$ shrinks to the limit point of $v$.

**Corollary (limit point).** If the meshes converge, the limit point of $v$ is $L(v)$. For $n = 6$ this is $\frac12 v + \frac{1}{12} \sum_j u_j$.

*Proof.* The valence of an old vertex does not change, so by Lemma 4 the value $L$ of the vertex point of $v$ and its ring is the same after every step. The weights of $L$ are positive and sum to 1, and the points of the ring converge to the limit point of $v$, so $L(v)$ is that point. For $n = 6$, $\omega = 3/(8 \cdot \frac1{16}) = 6$, which gives the weights $\frac{6}{12}$ and $\frac{1}{12}$. $\blacksquare$
