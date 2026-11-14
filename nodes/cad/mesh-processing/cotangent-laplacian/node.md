---
tag: ACV5AY
kind: definition
slug: cotangent-laplacian
name: Cotangent Laplacian
aliases:
- cotan Laplacian
- discrete Laplace-Beltrami operator
area: cad/mesh-processing
level: core
summary: The discrete Laplace-Beltrami operator of a triangle mesh whose edge weights are (cot a + cot b)/2 for the two angles opposite the edge, from linear finite elements.
prereqs: [laplacian-matrix, polygon-mesh, manifold-mesh]
see_also: [discrete-gaussian-curvature, surface-curvature, laplacian-smoothing, implicit-fairing, heat-method, finite-element-method, local-delaunay-criterion, floater-mean-value-coordinates]
sources:
  - paper: doi:10.1080/10586458.1993.10504266
    title: Ulrich Pinkall and Konrad Polthier, Computing discrete minimal surfaces and their conjugates, Experimental Mathematics 2(1), 1993, 15 to 36
    locator: the Dirichlet energy of a piecewise linear map written as a sum over the edges with the cotangents of the opposite angles
  - paper: doi:10.1007/978-3-662-05105-4_2
    title: Mark Meyer, Mathieu Desbrun, Peter Schröder and Alan H. Barr, Discrete differential-geometry operators for triangulated 2-manifolds, in Visualization and Mathematics III (H.-C. Hege and K. Polthier, eds.), Springer, 2003, 35 to 57
    locator: the mean curvature normal operator with the cotangent weights, and the mixed Voronoi area of a vertex
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 3, Differential Geometry (the discrete Laplace-Beltrami operators, uniform and cotangent, and the local averaging regions)
---

The cotangent Laplacian is the matrix that takes the place of the Laplace-Beltrami operator on a triangle mesh. For a function $u$ with one value per vertex, it gives at vertex $i$ the sum of $w_{ij}(u_j - u_i)$ over the neighbours $j$, where the weight of the edge $ij$ is half the sum of the cotangents of the two angles opposite to it. It is the stiffness matrix of linear finite elements on the mesh, so the quadratic form of the matrix is the Dirichlet energy of the piecewise linear function with the values $u$. Unlike the uniform [graph Laplacian](/laplacian-matrix/), it depends on the shape of the triangles, and this is why smoothing, fairing, parameterization and geodesic methods use it.

## Definition

Let $M$ be a [manifold](/manifold-mesh/) triangle mesh with vertex positions $x_i \in \mathbb{R}^3$ and no degenerate triangle. For an edge $ij$ with two faces, let $\alpha_{ij}$ and $\beta_{ij}$ be the angles opposite to the edge in these faces. For a border edge, there is only $\alpha_{ij}$, and we set $\cot \beta_{ij} = 0$. The *cotangent weight* of the edge is

$$w_{ij} = \tfrac{1}{2}\left(\cot \alpha_{ij} + \cot \beta_{ij}\right).$$

The *cotangent Laplacian* is the linear map $L$ on vertex functions with

$$(Lu)_i = \sum_{j \in N(i)} w_{ij}\,(u_j - u_i),$$

where $N(i)$ is the set of neighbours of $i$. As a matrix, $L = -C$, where the *stiffness matrix* $C$ has $C_{ij} = -w_{ij}$ for each edge, $C_{ii} = \sum_j w_{ij}$, and zeros elsewhere. For a function with values in $\mathbb{R}^3$, such as the positions $x$, $L$ acts on each coordinate.

**Where the weights come from.** Let $\varphi_i$ be the hat function of vertex $i$: it is linear on each triangle, 1 at $i$ and 0 at the other vertices. The piecewise linear interpolant of $u$ is $\hat u = \sum_i u_i \varphi_i$. In a triangle $T$ with area $A_T$ and angle $\theta_k$ at its vertex $k$, the gradient of $\varphi_i$ is perpendicular to the edge opposite $i$ and has length $1/h_i$, where $h_i$ is the height from $i$. For the two other vertices $i, j$ of $T$, this gives $\nabla \varphi_i \cdot \nabla \varphi_j = -\cot \theta_k / (2A_T)$, so

$$\int_T \nabla \varphi_i \cdot \nabla \varphi_j \, dA = -\tfrac{1}{2} \cot \theta_k .$$

Summing over the one or two triangles of the edge gives $\int_M \nabla \varphi_i \cdot \nabla \varphi_j \, dA = -w_{ij} = C_{ij}$, and since $\sum_j \varphi_j = 1$, the diagonal is $C_{ii} = -\sum_{j \ne i} C_{ij}$. Hence the *Dirichlet energy* of $\hat u$ is

$$E(u) = \tfrac{1}{2} \int_M |\nabla \hat u|^2 \, dA = \tfrac{1}{2}\, u^{\mathsf T} C u = \tfrac{1}{2} \sum_{ij \in E} w_{ij} (u_i - u_j)^2,$$

and $(Lu)_i = -\partial E / \partial u_i$. This is the formula of Pinkall and Polthier (1993). The same matrix is the stiffness matrix of the [finite element method](/finite-element-method/) with linear elements for the [Poisson equation](/poisson-equation/), as a [Galerkin method](/galerkin-method/) with the hat functions.

**The weights from the edge lengths.** In a triangle with side lengths $\ell_i, \ell_j, \ell_k$ and area $A_T$, the law of cosines gives $\cot \theta_k = (\ell_i^2 + \ell_j^2 - \ell_k^2) / (4 A_T)$, where $\ell_k$ is the side opposite $\theta_k$. So $L$ depends only on the edge lengths, not on how the mesh sits in space. It is an intrinsic operator, like the Laplace-Beltrami operator of a smooth surface.

**Normalized forms.** $(Lu)_i$ is an integral of the Laplacian over a region around vertex $i$, not a pointwise value. The pointwise estimate divides by an area $A_i$ of vertex $i$:

$$(\Delta u)_i = \frac{1}{A_i}\,(Lu)_i .$$

Two areas are common. The *barycentric area* is one third of the area of the triangles at $i$. The *mixed Voronoi area* of Meyer, Desbrun, Schröder and Barr (2003) adds, for each triangle at $i$ that has no obtuse angle, the part of its Voronoi cell, $\frac{1}{8}(\ell_{ij}^2 \cot \theta_k + \ell_{ik}^2 \cot \theta_j)$, and for an obtuse triangle, half its area if the obtuse angle is at $i$ and a quarter otherwise. With the diagonal *mass matrix* $D = \operatorname{diag}(A_i)$, the operator is $D^{-1}L$, and problems such as [implicit fairing](/implicit-fairing/) and the [heat method](/heat-method/) use the pair $(D, C)$ in the symmetric form $(D + tC)\,u = D\,b$.

**Mean curvature.** On a smooth surface, the Laplace-Beltrami operator of the position is $\Delta x = -2Hn$, where $H$ is the [mean curvature](/surface-curvature/) and $n$ the outward unit normal, so that a sphere of radius $r$ has $H = 1/r$. On a mesh, $\frac{1}{A_i}(Lx)_i$ is the discrete *mean curvature normal* at vertex $i$, and its length divided by 2 is an estimate of $|H|$.

**Properties.** These follow from the formula for $E$.

- $C$ is symmetric and each row sums to 0, so $C\mathbf{1} = 0$.
- $C$ is positive semidefinite, since $u^{\mathsf T} C u = \int |\nabla \hat u|^2 \ge 0$. The kernel is the functions that are constant on each connected component, since $\nabla \hat u = 0$ on every triangle makes $\hat u$ constant across shared edges. So $L$ is negative semidefinite, and its eigenvalues are $\le 0$, as for the smooth operator.
- *Linear precision.* If the mesh lies in a plane and $u$ is a linear function, then $(Lu)_i = 0$ at every inner vertex $i$. Indeed $(Cu)_i = \int \nabla \varphi_i \cdot g \, dA$ for the constant gradient $g$ of $u$, and this is $g \cdot \int \nabla \varphi_i \, dA = 0$, because $\varphi_i$ vanishes on the border of its star. So $L x = 0$ at inner vertices of a flat mesh: a flat mesh has zero mean curvature, whatever the shape of its triangles.
- *Sign of a weight.* Since $\cot \alpha + \cot \beta = \sin(\alpha + \beta) / (\sin \alpha \sin \beta)$, an inner edge has $w_{ij} \ge 0$ if and only if $\alpha_{ij} + \beta_{ij} \le \pi$, which is the [local Delaunay criterion](/local-delaunay-criterion/) for the two triangles of the edge. A mesh with obtuse angles can have negative weights.

**Conventions.** Texts differ in the factor $\frac{1}{2}$, in the sign (some call $C$ the Laplacian), and in the area. The page uses $L = -C$ with the factor $\frac{1}{2}$, so that $L$ is negative semidefinite and $\frac{1}{2}u^{\mathsf T} C u$ is the Dirichlet energy. Check these three choices before you mix formulas from two sources.

## Examples and non-examples

**One right triangle.** Take the vertices $0 = (0, 0)$, $1 = (1, 0)$, $2 = (0, 1)$. The angles are $90°$ at 0 and $45°$ at 1 and 2, so $w_{01} = \frac{1}{2}\cot 45° = \frac{1}{2}$, $w_{02} = \frac{1}{2}$, and $w_{12} = \frac{1}{2}\cot 90° = 0$. For $u = x$, with values $0, 1, 0$, the edge sum is $E = \frac{1}{2} \cdot \frac{1}{2} (0 - 1)^2 = \frac{1}{4}$. The direct integral is $\frac{1}{2} \cdot$ area $\cdot |\nabla u|^2 = \frac{1}{2} \cdot \frac{1}{2} \cdot 1 = \frac{1}{4}$, the same.

**A square with a center vertex.** The unit square with corners $(0,0), (1,0), (1,1), (0,1)$ and center $c = (\frac{1}{2}, \frac{1}{2})$, cut into four right triangles with the right angle at $c$. Each spoke from $c$ to a corner has two opposite angles of $45°$, so its weight is $\frac{1}{2}(1 + 1) = 1$. Each side of the square is a border edge with the opposite angle $90°$, so its weight is 0. For a linear $u$, $(Lu)_c$ is the sum of the four corner values minus $4u_c$, which is 0, as linear precision says. For $u = x^2 + y^2$, with $u_c = \frac{1}{2}$ and the corner values $0, 1, 2, 1$, we get $(Lu)_c = 2$. The true Laplacian is $\Delta u = 4$. The mixed Voronoi area of $c$ is $4 \cdot \frac{1}{8}(\frac{1}{2} + \frac{1}{2}) = \frac{1}{2}$, which gives $2 / \frac{1}{2} = 4$, the exact value. The barycentric area is $4 \cdot \frac{1}{4} \cdot \frac{1}{3} = \frac{1}{3}$, which gives $6$. So the choice of area matters, even on a regular mesh.

**The octahedron.** Take the vertices $(\pm 1, 0, 0)$, $(0, \pm 1, 0)$, $(0, 0, \pm 1)$, which lie on the unit sphere. Each face is equilateral, so every weight is $\frac{1}{2}(2 \cot 60°) = 1/\sqrt{3}$. At the top vertex $t = (0, 0, 1)$, the four neighbours give $\sum_j (x_j - t) = (0, 0, -4)$, so $(Lx)_t = (0, 0, -4/\sqrt{3})$. The barycentric area of $t$ is $4 \cdot \frac{1}{3} \cdot \frac{\sqrt 3}{2} = 2/\sqrt{3}$. The mean curvature normal is $(0, 0, -2)$, that is, $-2Hn$ with $H = 1$ and $n = (0, 0, 1)$: the curvature of the unit sphere, even on this coarse mesh.

**A negative weight.** Take two triangles in the plane on the edge from $(0, 0)$ to $(2, 0)$, with the apexes $(1, \frac{1}{4})$ and $(1, -\frac{1}{4})$. At each apex, the vectors to the ends of the edge are $(\mp 1, -\frac{1}{4})$, with dot product $-\frac{15}{16}$ and cross product $\frac{1}{2}$, so the cotangent is $-\frac{15}{8}$. The angle is about $151.9°$, and the two angles sum to more than $\pi$. The weight is $w = -\frac{15}{8}$. The quadrilateral is convex, and the edge flip to the other diagonal gives a Delaunay pair with nonnegative weights. With negative weights, $(Lu)_i = 0$ no longer makes $u_i$ an average of its neighbours, so the discrete maximum principle can fail.

**Non-example: the uniform Laplacian.** The [graph Laplacian](/laplacian-matrix/) of the mesh, with $w_{ij} = 1$ for each edge, depends only on the connectivity. It is what [Laplacian smoothing](/laplacian-smoothing/) uses in its simplest form. It has no linear precision: at the origin with the neighbours $(1, 0)$, $(1, 1)$, $(0, 1)$, $(-1, 0)$, $(0, -1)$ in this order, a fan of five triangles in the plane, the uniform Laplacian of $u = x$ is $1 + 1 + 0 - 1 + 0 = 1 \ne 0$, so smoothing with it moves vertices inside a flat region. The cotangent Laplacian of $u = x$ is 0 there.

**Non-example: mean value weights.** The weights of [Floater's mean value coordinates](/floater-mean-value-coordinates/) are always positive and reproduce linear functions in the plane, but they are not symmetric, $w_{ij} \ne w_{ji}$, so they do not come from an energy and do not give a symmetric matrix.

## Related definitions

- [Laplacian matrix](/laplacian-matrix/): the combinatorial Laplacian of a graph, with weights 1 or with given edge weights. The cotangent Laplacian is the weighted Laplacian of the edge graph with the cotangent weights, which can be negative.
- [Discrete Gaussian curvature](/discrete-gaussian-curvature/): the angle defect, the discrete form of $K$. The cotangent Laplacian of the position gives the discrete form of $H$, so the two together estimate the principal curvatures.
- [Surface curvature](/surface-curvature/): the smooth $K$ and $H$ that the discrete operators estimate.
- [Positive definite matrix](/positive-definite-matrix/): $C$ is positive semidefinite, and $D + tC$ is positive definite for $t > 0$, so it can be solved with the [conjugate gradient method](/conjugate-gradient-method/) or a [Cholesky decomposition](/cholesky-decomposition/).
- [Local Delaunay criterion](/local-delaunay-criterion/): the condition $\alpha + \beta \le \pi$ under which an inner weight is nonnegative.
- [Heat equation](/heat-equation/): $\partial u / \partial t = \Delta u$ on a mesh becomes $D\,\dot u = L u$, the system of [implicit fairing](/implicit-fairing/) and of the [heat method](/heat-method/).

## References
