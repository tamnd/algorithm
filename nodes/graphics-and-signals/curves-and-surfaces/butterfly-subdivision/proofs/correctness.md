---
title: One butterfly step keeps the old vertices, gives a closed triangle mesh with V + E vertices and 4F triangles, keeps the Euler characteristic, and reproduces cubic polynomials on a regular mesh
proves: [topology, counts, euler-characteristic, interpolation, stencils, cubic-reproduction]
status: full
---

We use the pseudocode of the page. The input is a closed oriented 2-manifold triangle mesh $M$ with $V$ vertices, $E$ edges and $F$ triangles: each directed edge $a \to b$ is in exactly one triangle, its reverse $b \to a$ is in exactly one other triangle, and the triangles around each vertex form one cycle. We write $\operatorname{opp}(x, y)$ for the third vertex of the triangle that has the directed edge $x \to y$, and $e_{ab} = e_{ba}$ for the edge point of the edge $ab$.

**Lemma 1 (topology and counts).** Line L3 gives a closed oriented 2-manifold triangle mesh with $V' = V + E$, $E' = 2E + 3F$ and $F' = 4F$, so $V' - E' + F' = V - E + F$.

*Proof.* Line L3 is the same split of each triangle into four as in [Loop subdivision](/loop-subdivision/), and the proof there uses only the connectivity, not the positions. Its Lemmas 1 and 2 give the claim. $\blacksquare$

**Lemma 2 (interpolation).** Every vertex of $M$ is a vertex of the new mesh at the same position, and so it is a vertex of every later mesh at the same position. If the meshes converge to a limit surface, the surface passes through every vertex of $M$, and through every edge point of every step.

*Proof.* Line L2 copies each old point. By induction on the number of steps, each point that any step makes is kept by all later steps. The limit of a sequence that is constant from some step on is that constant. $\blacksquare$

**Lemma 3 (the stencil is well defined, and its weights sum to 1).** For the edge $ab$ with the triangles $(a, b, c)$ and $(b, a, d)$, the wing vertices $\operatorname{opp}(c, b)$, $\operatorname{opp}(a, c)$, $\operatorname{opp}(d, a)$ and $\operatorname{opp}(b, d)$ exist, and the weights $\frac12, \frac12, 2w, 2w, -w, -w, -w, -w$ sum to 1 for each $w$.

*Proof.* The directed edges $b \to c$ and $c \to a$ are in $(a, b, c)$, so their reverses $c \to b$ and $a \to c$ are each in one other triangle, and $\operatorname{opp}$ is defined for them. The same holds for $a \to d$ and $d \to b$ in $(b, a, d)$. The sum is $1 + 4w - 4w = 1$. $\blacksquare$

The wings can repeat on a small mesh, and the implementation then adds their weights. Lemma 3 still holds.

**Theorem (cubic reproduction).** Let $M$ be the regular triangle mesh of the integer grid $\mathbb{Z}^2$, with each unit square $(i, j)$ cut into the triangles $((i,j), (i{+}1,j), (i{+}1,j{+}1))$ and $((i,j), (i{+}1,j{+}1), (i,j{+}1))$. Put the value $p(i, j)$ at the vertex $(i, j)$, for a polynomial $p$ of total degree at most 3. Then with $w = \frac1{16}$, line L1 gives each edge point the value of $p$ at the midpoint of the edge. For $w \ne \frac{1}{16}$ this fails for $p = x^2$, and for $w = \frac{1}{16}$ it fails for $p = x^2 y^2$.

*Proof.* The linear map $L(x, y) = (-y, x - y)$ maps $\mathbb{Z}^2$ to itself, maps the edge directions $(1, 0) \to (0, 1) \to (-1, -1)$, and maps the triangles of $M$ to triangles of $M$ with the same orientation. Translations by integer vectors also keep $M$. So every edge of $M$ is the image of the edge from $(0, 0)$ to $(1, 0)$ under such a map $A$, and the map takes the stencil of that edge to the stencil of the image edge. A polynomial of degree at most 3 composed with $A$ is again of degree at most 3. So it is enough to check the edge $a = (0, 0)$, $b = (1, 0)$.

Its triangles are $(a, b, c)$ with $c = (1, 1)$, and $(b, a, d)$ with $d = (0, -1)$, which is the second triangle of the square $(0, -1)$. The wings are $\operatorname{opp}(c, b) = (2, 1)$, from the second triangle of the square $(1, 0)$; $\operatorname{opp}(a, c) = (0, 1)$, from the second triangle of the square $(0, 0)$; $\operatorname{opp}(d, a) = (-1, -1)$, from the first triangle of the square $(-1, -1)$; and $\operatorname{opp}(b, d) = (1, -1)$, from the first triangle of the square $(0, -1)$.

Move the origin to the midpoint $(\frac12, 0)$. The stencil points are then $\pm(\frac12, 0)$ with the weight $\frac12$, $\pm(\frac12, 1)$ with the weight $2w$, and $\pm(\frac32, 1)$ and $\pm(\frac12, -1)$ with the weight $-w$. A polynomial of degree at most 3 is a sum of monomials $x^r y^s$ in the new coordinates, and the edge point is the value at the origin when the weighted sum $S(x^r y^s)$ of each monomial is its value at the origin: 1 for $r = s = 0$ and 0 otherwise.

- *Degree 0.* $S(1) = 1$ by Lemma 3.
- *Degrees 1 and 3.* The points come in pairs $\pm q$ with equal weights, and an odd monomial has opposite values at $q$ and $-q$. So $S = 0$.
- *$x^2$.* $S = \frac12 \cdot 2 \cdot \frac14 + 2w \cdot 2 \cdot \frac14 - w \cdot 2 \cdot \left(\frac94 + \frac14\right) = \frac14 + w - 5w = \frac14 - 4w$, which is 0 exactly when $w = \frac1{16}$.
- *$xy$.* $S = 2w \cdot 2 \cdot \frac12 - w \cdot 2 \cdot \left(\frac32 - \frac12\right) = 2w - 2w = 0$.
- *$y^2$.* $S = 2w \cdot 2 \cdot 1 - w \cdot 2 \cdot (1 + 1) = 0$.

So for $w = \frac{1}{16}$ every monomial of degree at most 3 gives its value at the origin, and by linearity so does every cubic. The value at the new origin is the value of the original $p$ at the midpoint, because the change of coordinates is a translation. For $x^2 y^2$ in the new coordinates, which is 0 at the origin, $S = 2w \cdot 2 \cdot \frac14 - w \cdot 2 \cdot \left(\frac94 + \frac14\right) = w - 5w = -4w$. In the original coordinates, with $x = X + \frac12$, the polynomial $x^2$ is $X^2 + X + \frac14$, so its error is $\frac14 - 4w$, and $x^2 y^2$ is $X^2 Y^2 + X Y^2 + \frac14 Y^2$, so its error with $w = \frac1{16}$ is $-\frac14 + 0 + 0 \ne 0$. $\blacksquare$

The limit on a regular mesh is $C^1$ for $w = \frac{1}{16}$, and the limit at an extraordinary vertex of the original scheme is not $C^1$ for some valences (check). These need the analysis of the subdivision matrix, and they are not proved here.

**Corollary (closed regular meshes).** On the regular mesh of an $n \times m$ torus grid, with the vertex values $p(i, j)$ for $0 \le i < n$ and $0 \le j < m$ and a cubic $p$, the edge point of each edge whose eight stencil points have $1 \le i \le n - 2$ and $1 \le j \le m - 2$ is the value of $p$ at the midpoint of the edge.

*Proof.* Such a stencil does not wrap around the torus, so it is the stencil of the same edge in the grid $\mathbb{Z}^2$, with the same values. The theorem gives the claim. $\blacksquare$
