---
tag: YB8QMS
kind: definition
slug: discrete-mean-curvature
name: Discrete mean curvature normal
aliases:
- Meyer discrete curvature operators
- mixed Voronoi area curvature
area: cad/mesh-processing
level: core
summary: The vector at a mesh vertex that Meyer, Desbrun, Schröder and Barr defined as the area gradient over the mixed Voronoi area, an estimate of 2H times the unit normal.
prereqs: [cotangent-laplacian, surface-curvature, polygon-mesh]
see_also: [discrete-gaussian-curvature, curvature-tensor-estimation, implicit-fairing, laplacian-smoothing, laplacian-surface-editing, manifold-harmonics, discrete-gauss-bonnet-theorem]
sources:
  - paper: doi:10.1007/978-3-662-05105-4_2
    title: Mark Meyer, Mathieu Desbrun, Peter Schröder and Alan H. Barr, Discrete differential-geometry operators for triangulated 2-manifolds, in Visualization and Mathematics III (H.-C. Hege and K. Polthier, eds.), Springer, 2003, 35 to 57
    locator: the mean curvature normal operator as the area gradient over the mixed Voronoi area, the mixed area for obtuse triangles, and the principal curvatures from the mean and Gaussian curvatures
  - paper: doi:10.1080/10586458.1993.10504266
    title: Ulrich Pinkall and Konrad Polthier, Computing discrete minimal surfaces and their conjugates, Experimental Mathematics 2(1), 1993, 15 to 36
    locator: the gradient of the area of a triangle mesh with the cotangents of the opposite angles, and discrete minimal surfaces as the critical points of the area
  - paper: doi:10.1007/s10711-006-9109-5
    title: Klaus Hildebrandt, Konrad Polthier and Max Wardetzky, On the convergence of metric and geometric properties of polyhedral surfaces, Geometriae Dedicata 123, 2006, 89 to 112
    locator: the convergence of the mean curvature vectors in a weak sense, under the convergence of the normals (general locator)
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 3, Differential Geometry (the discrete mean curvature from the Laplace-Beltrami operator of the positions)
---

The discrete mean curvature normal is a vector at each vertex of a triangle mesh. Meyer, Desbrun, Schröder and Barr (2003) defined it as

$$\mathbf K_i = \frac{1}{2A_i}\sum_{j \in N(i)} (\cot\alpha_{ij} + \cot\beta_{ij})\,(x_i - x_j),$$

where $N(i)$ is the set of neighbours of vertex $i$, $\alpha_{ij}$ and $\beta_{ij}$ are the two angles opposite the edge $ij$, and $A_i$ is the mixed Voronoi area of the vertex. The sum is twice the gradient of the area of the mesh with respect to $x_i$, so $\mathbf K_i$ is the area gradient per unit area. On a smooth surface, the area gradient per unit area is $2Hn$, where $H = \frac{1}{2}(k_1 + k_2)$ is the [mean curvature](/surface-curvature/) and $n$ the outward unit normal. So $\mathbf K_i$ is an estimate of $2Hn$ at the vertex, and $\frac{1}{2}|\mathbf K_i|$ is an estimate of $|H|$. At a convex vertex the vector points out. In the notation of the [cotangent Laplacian](/cotangent-laplacian/), $\mathbf K_i = (Cx)_i / A_i = -(Lx)_i / A_i$.

## Definition

Let the mesh be a triangle [polygon mesh](/polygon-mesh/) with vertex positions $x_1, \ldots, x_n$ in $\mathbb R^3$ and faces of positive area. For an inner edge $ij$, let $\alpha_{ij}$ and $\beta_{ij}$ be the angles at the third corners of the two faces that hold the edge. A border edge has one face, and the missing cotangent is 0. Write $w_{ij} = \frac{1}{2}(\cot\alpha_{ij} + \cot\beta_{ij})$, the cotangent weight.

**The area gradient.** Let $\mathcal A(x_1, \ldots, x_n)$ be the total area of the mesh. Then

$$\nabla_{x_i}\mathcal A = \sum_{j \in N(i)} w_{ij}\,(x_i - x_j) = \frac{1}{2}\sum_{j \in N(i)} (\cot\alpha_{ij} + \cot\beta_{ij})\,(x_i - x_j).$$

*Proof.* Take one face with corners $x_i, x_j, x_k$ and angles $\theta_i, \theta_j, \theta_k$. Its area is $\frac{1}{2}|e|\,h$, where $e = x_k - x_j$ is the edge opposite $x_i$ and $h$ is the distance from $x_i$ to the line through $e$. A move of $x_i$ along $e$ does not change $h$. A move out of the plane of the face changes $h$ only to second order. A move in the plane, normal to $e$, changes $h$ at unit rate. So the gradient of the face area at $x_i$ is $\frac{1}{2}|e|\,u$, where $u$ is the unit vector in the plane, normal to $e$, that points from the line to $x_i$. Let $\hat e = e / |e|$ and let the foot of the height be $x_j + a\hat e$, with $a$ signed. Then $x_i - x_j = hu + a\hat e$ and $x_i - x_k = hu + (a - |e|)\hat e$. So $\cot\theta_j = a/h$ and $\cot\theta_k = (|e| - a)/h$. These signed forms also hold when the foot is outside the edge: then one of the two angles is obtuse, and its cotangent is negative. Now

$$\cot\theta_k\,(x_i - x_j) + \cot\theta_j\,(x_i - x_k) = (|e| - a)\,u + a\,u + \frac{(|e| - a)\,a + a\,(a - |e|)}{h}\,\hat e = |e|\,u .$$

So the gradient of the face area at $x_i$ is $\frac{1}{2}\big(\cot\theta_k\,(x_i - x_j) + \cot\theta_j\,(x_i - x_k)\big)$. In this face, the coefficient of $x_i - x_j$ is the cotangent of the angle opposite the edge $ij$. Sum over the faces at $i$: each inner edge $ij$ lies in two faces, which give $\cot\alpha_{ij}$ and $\cot\beta_{ij}$. $\square$

**The mean curvature normal.** Divide the area gradient by an area $A_i$ that stands for the vertex:

$$\mathbf K_i = \frac{\nabla_{x_i}\mathcal A}{A_i} .$$

Meyer et al. use the mixed Voronoi area, which the [cotangent Laplacian](/cotangent-laplacian/) page also defines. A face at $i$ with no obtuse angle gives $i$ the part of the face that is nearer to $x_i$ than to the other corners, $\frac{1}{8}\big(|x_i - x_j|^2\cot\theta_k + |x_i - x_k|^2\cot\theta_j\big)$. An obtuse face gives $i$ half its area if the obtuse angle is at $i$, and a quarter of its area if not. The areas $A_i$ of all vertices sum to the area of the mesh.

**Why the factor is 2.** On a smooth closed surface, a motion with velocity field $V$ changes the area at the rate $\int 2H\,\langle V, n\rangle\,dA$, the first variation of area, with $H > 0$ on a sphere and $n$ outward. For the sphere of radius $r$ and $V = n$ the rate is $\frac{2}{r} \cdot 4\pi r^2 = 8\pi r$, the derivative of $4\pi r^2$. So the area gradient is the density $2Hn$ integrated over a region. Meyer et al. read $\nabla_{x_i}\mathcal A$ as the integral of $2Hn$ over the region of vertex $i$, and the division by $A_i$ gives the value at the point. Take care with three factors:

- $\mathbf K_i$ is $2Hn$, so the mean curvature is $\frac{1}{2}|\mathbf K_i|$, not $|\mathbf K_i|$.
- Some texts call $k_1 + k_2$ the mean curvature. With that name, $|\mathbf K_i|$ is the mean curvature.
- If you divide by the area of all faces at $i$, which is three times the barycentric area, the vector is three times too short.

**Signed mean curvature.** With a unit normal $n_i$ at the vertex, $H_i = \frac{1}{2}\mathbf K_i \cdot n_i$ has a sign. It is positive where the surface bends away from $n_i$, as on a sphere with outward normals, and negative in a dent. The length $|\mathbf K_i|$ does not keep the sign.

**Principal curvatures.** Let $K^G_i$ be the [angle defect](/discrete-gaussian-curvature/) at $i$ divided by the same $A_i$. Meyer et al. estimate the principal curvatures as

$$k_{1,2} = H_i \pm \sqrt{\max(H_i^2 - K^G_i,\ 0)} .$$

The two estimates come from different formulas, so $H_i^2 - K^G_i$ can be slightly negative, and the clamp at 0 is necessary. The principal directions need more than these two numbers: see [curvature tensor estimation](/curvature-tensor-estimation/).

**Properties.**

- *Translation.* A translation of the whole mesh does not change its area. So $\sum_i \nabla_{x_i}\mathcal A = 0$, that is $\sum_i A_i\mathbf K_i = 0$, on every mesh.
- *Scale.* The area is homogeneous of degree 2 in the positions. By Euler's identity for homogeneous functions, $\sum_i x_i \cdot \nabla_{x_i}\mathcal A = 2\mathcal A$. A scaling of the mesh by $s$ scales each $\mathbf K_i$ by $1/s$, as for the curvature of a sphere.
- *Flat stars.* At an inner vertex whose faces lie in one plane, $\mathbf K_i = 0$, for every shape of the triangles. A move of $x_i$ in the plane does not change the area of its star, because the outer polygon stays the same. A move out of the plane changes the area only to second order.
- *Rotation.* A rotation of the mesh rotates each $\mathbf K_i$ with it.
- *Zeros.* A mesh with $\mathbf K_i = 0$ at every inner vertex is a critical point of the area for a fixed border. Pinkall and Polthier (1993) call it a discrete minimal surface.
- *Convergence.* For meshes that converge to a smooth surface together with their normals, Hildebrandt, Polthier and Wardetzky (2006) prove that the mean curvature vectors converge in a weak, integrated sense. The value at a single vertex can still be wrong, and its convergence needs more conditions on the triangles.

## Examples and non-examples

**All vertices alike on a sphere.** Take a mesh with all vertices on the sphere of radius $r$ about the origin, such that the symmetries of the mesh map any vertex to any other, and each vertex has a symmetry that turns about its radius by a nonzero angle less than a half turn. The octahedron and the icosahedron are examples. By symmetry, each $\nabla_{x_i}\mathcal A$ is along the radius, with the same length $g$, and each $A_i = \mathcal A / n$. Euler's identity gives $n\,r\,g = 2\mathcal A$, so $|\mathbf K_i| = g / A_i = 2/r$ and $H = 1/r$, exactly. For the icosahedron on the unit sphere, the edge length is $4/\sqrt{10 + 2\sqrt 5} \approx 1.0515$, every weight is $\cot 60° = 1/\sqrt 3$, and $A_i \approx 0.7979$. The formula gives $|\mathbf K_i| = 2$. This exact value comes from the symmetry. It does not mean that a coarse mesh is a good model of the sphere.

**A cylinder, exactly.** Cut the cylinder of radius $r$ into $m$ columns and rows of height $h$, and cut each rectangle by the diagonal in the same direction. Each face is a right triangle with legs $c = 2r\sin(\pi/m)$ and $h$, and area $\frac{1}{2}ch$. Each inner vertex is the right-angle corner of 2 of its 6 faces, so its mixed area is $2 \cdot \frac{1}{2} \cdot \frac{ch}{2} + 4 \cdot \frac{1}{4} \cdot \frac{ch}{2} = ch$. The half turn about the radial line through $x_i$ maps the mesh to itself, so the area gradient at $x_i$ is along the radius. In a tube that repeats along its axis, all vertices are alike, and the area per vertex, $ch$, is linear in $r$. A scaling of all radii by $1 + \epsilon$ thus adds $\epsilon\,ch$ to the area per vertex, and the radial gradient is $g = ch / r$. So $|\mathbf K_i| = 1/r$ and $H = \frac{1}{2r}$, the mean curvature of the cylinder, for every $m$ and $h$.

**A sphere with unequal vertices.** The icospheres cut each triangle of the icosahedron into four and project the new vertices to the unit sphere. At the twelve vertices of valence 5, the measured values of $\frac{1}{2}|\mathbf K_i|$ are:

| level | vertices | mixed Voronoi area | barycentric area |
|---|---|---|---|
| 1 | 42 | 1.0000 | 1.1024 |
| 2 | 162 | 1.0000 | 1.1345 |
| 3 | 642 | 1.0000 | 1.1430 |
| 4 | 2562 | 1.0000 | 1.1452 |

With the mixed area, the vertices of valence 6 also give values within 0.0002 of 1. With the barycentric area, the estimate at the valence 5 vertices does not tend to 1, because the faces around them have unequal sizes. At the pole of a latitude and longitude sphere with $m$ thin faces at the pole, the barycentric area gives 0.873, 0.779, 0.757 and 0.752 for $m = 8, 16, 32, 64$ with $m$ rings, and the mixed area gives 1.0000. For a thin face at the pole, the barycentric share is about $\frac{4}{3}$ times the Voronoi share, so the barycentric value tends to $\frac{3}{4}$.

**A saddle with zero mean curvature.** Put the vertex at the origin with the four neighbours $(1, 0, 1)$, $(0, 1, -1)$, $(-1, 0, 1)$, $(0, -1, -1)$ in this order. Each face is isosceles, with sides $\sqrt 2$ and an angle of $120°$ at the origin, so its two other angles are $30°$. Each spoke is opposite two angles of $30°$, so every weight is $\frac{1}{2}(\sqrt 3 + \sqrt 3) = \sqrt 3$. The area gradient is $\sqrt 3\sum_j (0 - x_j)$, and the neighbours sum to $0$, so $\mathbf K = 0$. The [discrete Gaussian curvature](/discrete-gaussian-curvature/) of the same vertex is $-2\pi/3$. Zero mean curvature with negative Gaussian curvature is the local shape of a minimal surface.

**Non-example: a border vertex.** Cut the unit square into two triangles by the diagonal from $(0, 0)$ to $(1, 1)$. At the corner $(1, 0)$, the area gradient is $(\frac{1}{2}, -\frac{1}{2}, 0)$ and the mixed area is $\frac{1}{4}$, so the formula gives $(2, -2, 0)$, although the square is flat. At a border vertex the area gradient also holds the pull of the border, because a move outward makes the area larger. So the formula gives a mean curvature only at inner vertices. At border vertices, leave it out or use a border term.

**Non-example: the uniform Laplacian.** The vector $\frac{1}{d_i}\sum_j (x_j - x_i)$ of [Laplacian smoothing](/laplacian-smoothing/) is not a curvature. Take the vertex $(0, 0, 0)$ with the neighbours $(2, 0, 0)$, $(0, 1, 0)$, $(-1, 0, 0)$, $(0, -1, 0)$ in one plane. The uniform vector is $(\frac{1}{4}, 0, 0)$, along the plane, while $\mathbf K = 0$ because the star is flat.

## Related definitions

- [Surface curvature](/surface-curvature/): the smooth mean curvature $H$ and the principal curvatures $k_1, k_2$ that $\mathbf K_i$ estimates.
- [Cotangent Laplacian](/cotangent-laplacian/): the operator $L$, with $\mathbf K_i = -(Lx)_i / A_i$, and the mixed area in detail.
- [Discrete Gaussian curvature](/discrete-gaussian-curvature/): the angle defect, the companion estimate. The two together give $k_1$ and $k_2$.
- [Curvature tensor estimation](/curvature-tensor-estimation/): estimates of the principal directions, which $\mathbf K_i$ does not give.
- [Implicit fairing](/implicit-fairing/): moves each vertex along $-\mathbf K_i$, a discrete mean curvature flow.
- [Laplacian surface editing](/laplacian-surface-editing/): stores the vectors $(Lx)_i$, which are $-A_i\mathbf K_i$ with the cotangent weights, as the detail of a shape.

## References
