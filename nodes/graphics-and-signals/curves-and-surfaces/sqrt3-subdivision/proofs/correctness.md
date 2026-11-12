---
title: One sqrt(3) step gives a closed triangle mesh with V + F vertices and 3F triangles, keeps the Euler characteristic, and two steps on a regular planar mesh give the triadic split
proves: [topology, counts, euler-characteristic, stencils, limit-position, two-step-triadic-split]
status: full
---

We use the pseudocode of the page. The input is a closed oriented 2-manifold triangle mesh $M$ with $V$ vertices, $E$ edges and $F$ triangles: each directed edge $a \to b$ is in exactly one triangle, its reverse $b \to a$ is in exactly one other triangle, and the triangles around each vertex form one cycle. Then $3F = 2E$. We write $c_f$ for the centroid of the triangle $f$ from line L1, and $n_v$ for the valence of $v$. For a directed edge $a \to b$ in the triangle $f$, with $b \to a$ in $g$, let $T(a \to b) = (c_f, a, c_g)$. Line L3 adds, for the edge $ab$, the two triangles $T(a \to b)$ and $T(b \to a) = (c_g, b, c_f)$. So the new triangles are the $T(a \to b)$, one for each of the $2E = 3F$ directed edges.

**Lemma 1 (the new mesh is a closed oriented 2-manifold).** Each new directed edge is in one new triangle, and its reverse is in one other new triangle. An old vertex $v$ has the $n_v$ centroids of its triangles as its new neighbors, and each centroid has valence 6.

*Proof.* The triangle $T(a \to b) = (c_f, a, c_g)$ has the directed edges $c_f \to a$, $a \to c_g$ and $c_g \to c_f$. We pair them.

- $c_g \to c_f$ of $T(a \to b)$ is reversed by $c_f \to c_g$ of $T(b \to a) = (c_g, b, c_f)$.
- $c_f \to a$ of $T(a \to b)$, where $a \to b$ is in $f$: let $x \to a$ be the edge of $f$ that ends at $a$, and $h$ the triangle with $a \to x$. Then $T(a \to x) = (c_h, a, c_f)$ has $a \to c_f$.
- $a \to c_g$ of $T(a \to b)$, where $b \to a$ is in $g$: let $a \to y$ be the edge of $g$ that starts at $a$, and $k$ the triangle with $y \to a$. Then $T(a \to y) = (c_g, a, c_k)$ has $c_g \to a$.

Each new triangle comes from one old directed edge, and each old directed edge is in one old triangle, so each of these new directed edges comes from one place only. The triangles $T(a \to u)$ over the $n_a$ edges $a \to u$ out of $a$ are the new triangles at $a$, and by the second and third cases they form one cycle, in the order of the old triangles around $a$. So the neighbors of $a$ are the $n_a$ centroids. The centroid $c_f$ of $f = (a, b, x)$ is in the six triangles $T(a \to b), T(b \to x), T(x \to a)$ and $T(b \to a), T(x \to b), T(a \to x)$, and its neighbors are $a, b, x$ and the three centroids of the triangles across the edges of $f$. $\blacksquare$

**Lemma 2 (counts).** $V' = V + F$, $E' = E + 3F$, $F' = 3F$, and $V' - E' + F' = V - E + F$. Two steps give $V + 4F$ vertices, $E + 12F$ edges and $9F$ triangles.

*Proof.* Lines L1 and L2 make one point per old triangle and one per old vertex. There are $2E = 3F$ new triangles. By Lemma 1, the undirected new edges are the $E$ edges $c_f c_g$, one per old edge, and the 3 edges from each centroid to its corners. Then $(V + F) - (E + 3F) + 3F = V - E + F$. A second step adds $F' = 3F$ vertices and $3F' = 9F$ edges, and makes $3F' = 9F$ triangles. $\blacksquare$

**Lemma 3 (weights).** The weights of line L1 are $\frac13, \frac13, \frac13$, and the weights of line L2 are $1 - \alpha_n$ and $n$ times $\frac{\alpha_n}{n}$. Both sets sum to 1. With $\alpha_n = \frac{4 - 2\cos(2\pi/n)}{9}$, $\alpha_3 = \frac59$, $\alpha_4 = \frac49$ and $\alpha_6 = \frac13$.

*Proof.* The sums are clear. The cosines are $-\frac12$, $0$ and $\frac12$, which give $\frac{5}{9}$, $\frac{4}{9}$ and $\frac{3}{9}$. $\blacksquare$

**Lemma 4 (limit position).** Let $v$ have valence $n$, the neighbors $u_1, \dots, u_n$ and the mean $\bar u = \frac1n \sum_j u_j$, and let $\lambda = \frac{1}{1 + 3 \alpha_n}$. Then $L(v) = \lambda v + (1 - \lambda) \bar u$ has the same value before and after one step, with the new point $v'$ and its new neighbors.

*Proof.* By Lemma 1, the new neighbors of $v'$ are the centroids of the $n$ triangles $(v, u_j, u_{j+1})$ around $v$, with indices modulo $n$. Their mean is $\frac1n \sum_j \frac{v + u_j + u_{j+1}}{3} = \frac13 v + \frac23 \bar u$. With $v' = (1 - \alpha_n) v + \alpha_n \bar u$, the new value is
$$\lambda (1 - \alpha_n) v + \lambda \alpha_n \bar u + (1 - \lambda)\left(\tfrac13 v + \tfrac23 \bar u\right).$$
The coefficient of $v$ is $\lambda - \lambda \alpha_n + \frac{1 - \lambda}{3} = \lambda$, because $1 - \lambda = 3 \alpha_n \lambda$. The coefficients sum to 1, so the coefficient of $\bar u$ is $1 - \lambda$. $\blacksquare$

**Theorem (two steps on a regular planar mesh).** Let $M$ be the regular triangle mesh of the grid $\mathbb{Z}^2$ in the plane, with each unit square $(i, j)$ cut into the triangles $((i,j), (i{+}1,j), (i{+}1,j{+}1))$ and $((i,j), (i{+}1,j{+}1), (i,j{+}1))$, and with the vertex $(i, j)$ at the point $(i, j)$. The rules are local, so they apply to this infinite mesh. After two steps, the points are the points of $\frac13 \mathbb{Z}^2$, each once, and the mesh is the regular mesh of $\frac13 \mathbb{Z}^2$ with the same pattern. So the two steps together split each triangle into 9, as a triadic split does.

*Proof.* The maps $A(x, y) = (-y, x - y)$ and $-I$ and the integer translations map $\mathbb{Z}^2$ to itself and the triangles of $M$ to triangles of $M$ with the same orientation, so they commute with both steps. They permute the six vectors $\pm(1, 0), \pm(0, 1), \pm(1, 1)$, and they act transitively on the directed edges of $M$.

*The points stay.* Each vertex of $M$ has valence 6, and its neighbors are $v \pm (1,0), v \pm (0,1), v \pm (1,1)$, with the mean $v$. So line L2 keeps $v$. The centroids are $(i + \frac23, j + \frac13)$ and $(i + \frac13, j + \frac23)$. In the first step's mesh, the centroid $(\frac23, \frac13)$ has the neighbors $(0, 0), (1, 0), (1, 1)$ and the centroids $(\frac13, -\frac13), (\frac43, \frac23), (\frac13, \frac23)$ across the edges of its triangle, and their mean is $\frac16 (4, 2) = (\frac23, \frac13)$. By the symmetries every centroid has the same form, so the second step keeps all points of the first step.

*The new points.* For the directed edge $a = (0, 0) \to b = (1, 0)$, the triangle on the left is $f = ((0,0), (1,0), (1,1))$ and the one on the right is $g = ((0,-1), (1,0), (0,0))$, so $c_f = (\frac23, \frac13)$, $c_g = (\frac13, -\frac13)$, and $T(a \to b) = ((\frac23, \frac13), (0, 0), (\frac13, -\frac13))$. Its centroid is $t = (\frac13, 0)$, and the centroid of $T(b \to a)$ is $(\frac23, 0)$. So the second step puts two points on each old edge, at a third and two thirds of its length. Each unit square has 3 edges, so with the vertex and the 2 centroids it has $1 + 2 + 6 = 9$ points, which are the 9 points of $\frac13 \mathbb{Z}^2$ in the square.

*The new edges.* By Lemma 1 applied to the first step's mesh, every edge of the second step's mesh has an end at a new centroid of the second step, and each such centroid has six neighbors: the three corners of its triangle and the three centroids across the edges. For $t$ these are the corners $(\frac23, \frac13), (0, 0), (\frac13, -\frac13)$; the centroid $(\frac23, 0)$ of $T(b \to a)$; the centroid $(\frac13, \frac13)$ of $T(a \to x) = ((\frac13, \frac23), (0, 0), (\frac23, \frac13))$ with $x = (1, 1)$; and the centroid $(0, -\frac13)$ of $T(a \to y) = ((\frac13, -\frac13), (0, 0), (-\frac13, -\frac23))$ with $y = (0, -1)$. The differences from $t$ are $(\frac13, \frac13), (-\frac13, 0), (0, -\frac13), (\frac13, 0), (0, \frac13)$ and $(-\frac13, -\frac13)$, the six short vectors of $\frac13 \mathbb{Z}^2$. The second step's centroids correspond to the triangles of the first step, and so to the directed edges of $M$, so by the symmetries every one of them has the six short vectors as its edges.

So every edge of the new mesh is a short vector of $\frac13 \mathbb{Z}^2$ in one of the three directions. By Lemma 1 every vertex has valence 6 in the new mesh, because the valence of each old vertex is kept and the centroids have valence 6. A point of $\frac13 \mathbb{Z}^2$ with 6 distinct neighbors among its 6 short neighbors is joined to all of them. So the edges are those of the regular mesh of $\frac13 \mathbb{Z}^2$. Each triangle of the new mesh is a cycle of three such edges, which is one of the small triangles. There are $9 \cdot 2 = 18$ new triangles per unit square by Lemma 2, all different, and the regular mesh has 18 small triangles per unit square, so the new triangles are all of them. $\blacksquare$

On a closed regular mesh, such as a torus, the same holds for every part whose stencils do not wrap around, which is what the tests check. The limit at a regular vertex is $C^2$, and at an extraordinary vertex, a vertex of valence $n \ne 6$, Kobbelt chose $\alpha_n$ so that the limit is $C^1$ (check). This needs the eigen analysis of the subdivision matrix, and it is not proved here.

**Corollary (limit point).** If the meshes converge, the limit point of $v$ is $L(v) = \frac{v + 3 \alpha_n \bar u}{1 + 3 \alpha_n}$. For $n = 6$ it is $\frac12 v + \frac12 \bar u$, and for $n = 3$ it is $\frac38 v + \frac58 \bar u$.

*Proof.* The valence of an old vertex does not change, so by Lemma 4 the value $L$ is the same after every step. Its weights are positive and sum to 1, and the ring of $v$ converges to the limit point of $v$, so $L(v)$ is that point. For $n = 6$, $3 \alpha_6 = 1$, and for $n = 3$, $3 \alpha_3 = \frac53$ and $\lambda = \frac{3}{8}$. $\blacksquare$
