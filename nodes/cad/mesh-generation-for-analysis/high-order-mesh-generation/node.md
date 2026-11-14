---
tag: WWP9SX
kind: technique
slug: high-order-mesh-generation
name: High-order curved mesh generation
aliases:
- curved mesh generation
area: cad/mesh-generation-for-analysis
level: research
summary: Bends a straight-sided mesh to fit curved boundaries with high-order elements and fixes invalid elements by elasticity or optimisation, as Persson and Peraire did.
prereqs: [finite-element-method, lagrange-interpolation, bernstein-polynomials]
see_also: [mesh-untangling, optimization-based-mesh-smoothing, scaled-jacobian, volumetric-spline-parameterization, boundary-layer-mesh-generation, de-casteljau-algorithm, convex-hull-property, isogeometric-analysis]
sources:
  - paper: "Per-Olof Persson and Jaime Peraire, Curved mesh generation and mesh refinement using Lagrangian solid mechanics, 47th AIAA Aerospace Sciences Meeting, 2009"
    locator: the curving of a straight mesh by a nonlinear elastic problem with the boundary displacement as data (general locator)
  - paper: "S. J. Sherwin and J. Peiró, Mesh generation in curvilinear domains using high-order elements, International Journal for Numerical Methods in Engineering 53, 2002"
    locator: the placement of the high-order nodes on curved boundaries and the invalid elements that it can make (general locator)
  - paper: "Saikat Dey, Curvilinear mesh generation in 3D, Proceedings of the 8th International Meshing Roundtable, 1999, 407 to 417"
    locator: curved tetrahedral meshes for high-order analysis and the check of their validity (general locator)
  - paper: "Amaury Johnen, Jean-François Remacle and Christophe Geuzaine, Geometrical validity of curvilinear finite elements, Journal of Computational Physics 233, 2013, 359 to 372"
    locator: the Bernstein form of the Jacobian determinant, the bound by its coefficients and the adaptive subdivision that sharpens it (general locator)
  - paper: "Thomas Toulorge, Christophe Geuzaine, Jean-François Remacle and Jonathan Lambrechts, Robust untangling of curvilinear meshes, Journal of Computational Physics 254, 2013"
    locator: the optimization with a barrier on the Jacobian that untangles the invalid elements in patches (general locator)
  - paper: "Xevi Roca, Abel Gargallo-Peiró and Josep Sarrate, Defining quality measures for high-order planar triangles and curved mesh generation, Proceedings of the 20th International Meshing Roundtable, 2012, 365 to 383"
    locator: quality measures for curved triangles (general locator)
  - paper: "Nico Pietroni, Marcel Campen, Alla Sheffer, Gianmarco Cherchi, David Bommes, Xifeng Gao, Riccardo Scateni, Franck Ledoux, Jean-François Remacle and Marco Livesu, Hex-mesh generation and processing, a survey, arXiv 2202.12670, 2022"
    locator: the paragraph on determinant bounds in the Bernstein basis in the section on element quality, and the paragraphs on high-order hex meshes
---

High-order mesh generation makes meshes whose elements have curved sides. Each element is the image of a reference triangle, tetrahedron or cube under a polynomial map of degree $p \ge 2$, given by nodes at its corners and also on its edges, faces and inside. High-order finite element and spectral methods need such meshes: with straight sides, a curved boundary is only approximated to second order, and the error of the geometry spoils the high accuracy of the method. The usual approach starts from a good straight-sided mesh, moves the boundary nodes onto the true curved boundary, and then repairs the elements that this makes invalid. Persson and Peraire (2009) did the repair by solving an elastic problem for the inner nodes, and later methods use optimization.

## In plain words

Take a triangle mesh of a disk. The outer edges are straight, so the mesh misses thin slivers of the disk. A quadratic element has an extra node in the middle of each edge. Push the middle nodes of the outer edges onto the circle, and the outer edges now bend to follow it.

The trouble is that a bend can be too strong for a small element. If an element is thin and its curved edge bulges inward, the edge can cross the opposite side, and the element folds over. Then the map from the reference element is no longer one to one, and the analysis fails. So the method must check every element and, where needed, also bend the neighbours, as if the mesh were a rubber sheet pushed at its boundary.

## When it applies

- The domain has curved boundaries, given by CAD curves and surfaces, and the analysis uses elements of degree $p \ge 2$, for example discontinuous Galerkin or spectral element methods for flow and waves.
- A straight-sided mesh of good quality exists, from any method: [Delaunay refinement](/tetrahedral-delaunay-refinement/), [advancing front](/advancing-front-mesh-generation/) or a hex mesher. The method does not change the connectivity, only the node positions.
- Elements near the boundary are not much smaller than the radius of curvature of the boundary, or there is room inside to spread the bend. Thin [boundary layer](/boundary-layer-mesh-generation/) elements on strongly curved walls are the hardest case.

## The template

Each element is the image of a reference element $\hat K$ under the map $x(\xi) = \sum_i x_i N_i(\xi)$, with the Lagrange shape functions $N_i$ of degree $p$ and the nodes $x_i$. The element is valid when the Jacobian determinant $\det J(\xi) = \det \partial x / \partial \xi$ is positive on all of $\hat K$.

```pseudo id=main
CURVE-MESH(T, ∂Ω, p)
L1  for each element K of the straight mesh T do place the nodes of degree p on its straight edges, faces and inside
L2  for each boundary edge or face do move its nodes onto ∂Ω, by projection or by the CAD parameters
L3  for each element K do compute the Bernstein coefficients b_K of det J
L4  bad ← the elements with min b_K ≤ 0, after subdivision where the test is not sure
L5  if bad is empty then return the mesh
L6  move the free nodes in a patch around bad: solve an elastic problem with the moves of L2 as boundary data, or minimize a distortion energy with a barrier on det J
L7  go to L3, or give up after a fixed number of rounds
```

The holes are the placement rule of L2, the energy or elastic law of L6, and the size of the patch.

**Why Bernstein coefficients (L3).** For a simplex in $n$ dimensions and degree $p$, each entry of $J$ has degree $p - 1$, so $\det J$ is a polynomial of degree $d = n (p - 1)$. Any polynomial of degree $d$ on a simplex with barycentric coordinates $\lambda_1, \dots, \lambda_{n+1}$ can be written in the [Bernstein basis](/bernstein-polynomials/)

$$\det J = \sum_{|\alpha| = d} b_\alpha B_\alpha, \qquad B_\alpha = \frac{d!}{\alpha_1! \cdots \alpha_{n+1}!} \lambda_1^{\alpha_1} \cdots \lambda_{n+1}^{\alpha_{n+1}}.$$

For a quadratic triangle, $d = 2$, and the six coefficients come from the six values of $\det J$ at the corners $v_i$ and the edge midpoints $m_{ij}$: $b_{ii} = \det J(v_i)$ and $b_{ij} = 2 \det J(m_{ij}) - (\det J(v_i) + \det J(v_j)) / 2$. The second formula follows from the value at the midpoint, where $\lambda_i = \lambda_j = 1/2$, so $\det J(m_{ij}) = (b_{ii} + 2 b_{ij} + b_{jj}) / 4$.

**Claim.** (1) If every coefficient $b_\alpha$ is positive, then $\det J > 0$ on the whole element. (2) The coefficient at each corner equals the value of $\det J$ there, so a coefficient $b_{d e_i} \le 0$ at a corner proves that the element is not valid. (3) The converse of (1) is false: an element can be valid while some coefficient is negative.

**Proof.** On the element, every $\lambda_k \ge 0$, so every $B_\alpha \ge 0$. By the multinomial theorem, $\sum_\alpha B_\alpha = (\lambda_1 + \dots + \lambda_{n+1})^d = 1$. So $\det J$ is a weighted mean of the coefficients, and

$$\det J(\xi) = \sum_\alpha b_\alpha B_\alpha(\xi) \ge \min_\alpha b_\alpha \sum_\alpha B_\alpha(\xi) = \min_\alpha b_\alpha > 0,$$

which is (1). At the corner $v_i$, $\lambda_i = 1$ and the other $\lambda_k = 0$, so all $B_\alpha$ vanish except $B_{d e_i} = 1$, which gives (2). For (3), take the quadratic triangle with corner nodes $(0, 0)$, $(1, 0)$, $(0, 1)$ and edge nodes $(0, \tfrac14)$ on the edge from the first to the second corner, $(\tfrac12, \tfrac12)$ on the edge from the second to the third, and $(-\tfrac12, \tfrac12)$ on the edge from the third to the first. A direct computation from the shape functions gives

$$\det J(\xi, \eta) = 1 - 3\xi - 2\eta + 4(\xi + \eta)^2.$$

With $u = \xi + \eta$ this is $4u^2 - 3u + 1 + \eta = 4(u - \tfrac38)^2 + \tfrac{7}{16} + \eta \ge \tfrac{7}{16}$, since $\eta \ge 0$. So the element is valid, with the least value $\tfrac{7}{16}$ at $(\tfrac38, 0)$. But the corner values are $1$, $2$, $3$, and the midpoint values $\tfrac12$, $\tfrac52$, $1$ give the edge coefficients $2 \cdot \tfrac12 - \tfrac32 = -\tfrac12$, $\tfrac52$ and $0$. One coefficient is negative. $\blacksquare$

So L4 has three outcomes: all coefficients positive (valid), a corner value or another sampled value of $\det J$ not positive (invalid), or neither (not known). In the third case, split the element into smaller pieces and compute the coefficients of each piece. Johnen, Remacle and Geuzaine show that the coefficients approach the values of $\det J$ as the pieces get smaller, so a valid element is certified after enough splits (general locator). For the triangle above, one split into four triangles by the edge midpoints gives 24 coefficients, all positive, the least being $\tfrac14$.

**What is proved and what is measured.** The claim above is proved, and it makes the check of L3 and L4 exact. The repair of L6 has no guarantee. An elastic solve can itself produce inverted elements when the boundary moves are large compared with the elements, and an optimization can stop at a local minimum with elements still invalid. How often the repair succeeds, and the quality it reaches, are measured on test cases in the papers.

## Classic examples

- **A curved edge pushed inward.** Take the quadratic triangle with corners $(0, 0)$, $(1, 0)$, $(0, 1)$, straight edge nodes $(\tfrac12, 0)$ and $(0, \tfrac12)$, and the node of the third edge moved from $(\tfrac12, \tfrac12)$ to $(\tfrac12 + t, \tfrac12 + t)$. Then $\det J = 1 + 4t(\xi + \eta)$. It is positive on the element exactly when $1 + 4t > 0$, that is $t > -\tfrac14$. For a boundary edge that bends into the element, as on a concave wall, a bend of a quarter of the size of the element is the limit. Smaller elements near such a wall, or moving the inner nodes, are the cure.
- **Sherwin and Peiró (2002).** They place the nodes of curved boundary elements by the parameters of the CAD surface, and discuss the invalid elements that this makes near strong curvature.
- **Persson and Peraire (2009).** The straight mesh is treated as an elastic body. The boundary nodes are moved to the curve, and a nonlinear elastic problem moves the inner nodes. Large bends are spread over many layers of elements. This is a relative of [optimization-based mesh smoothing](/optimization-based-mesh-smoothing/).
- **Toulorge and others (2013).** Only patches around invalid elements are changed. The node positions minimize a distortion energy with a barrier on $\det J$, raised in steps, which is a curved form of [mesh untangling](/mesh-untangling/).
- **Spline volumes.** The same test applies to the volumetric maps of isogeometric analysis. The [volumetric spline parameterization](/volumetric-spline-parameterization/) page gives a 1D form of the converse in (3), with the coefficients $(1, -0.8, 1)$ and the least value $0.1$.

## Variations

- **Hexes and prisms.** For tensor product elements, $\det J$ is written in the tensor product Bernstein basis, and the same proof works. The survey of Pietroni and others describes this for trilinear and higher-order hexes.
- **Quality, not only validity.** The ratio of the least to the largest value of $\det J$, or the [scaled Jacobian](/scaled-jacobian/) at sample points, measures how much an element is distorted. Roca, Gargallo-Peiró and Sarrate define such measures for curved triangles.
- **Linear elasticity.** A cheaper form of L6 solves one linear elastic problem. It works for small bends and can fail for large ones.
- **Splitting.** The check of L4 can use the [de Casteljau algorithm](/de-casteljau-algorithm/) to split the Bernstein form, instead of computing new values of $\det J$.

## Pitfalls

- **Checking only at nodes or sample points.** $\det J$ can be positive at all nodes and quadrature points and negative between them. Use the Bernstein bound, which covers the whole element.
- **Reading a negative coefficient as an invalid element.** By part (3) of the claim, it only means that the test is not sure. Split before rejecting the element.
- **Moving only the boundary nodes.** If the boundary moves by more than about a quarter of the size of the elements next to it, as in the first example, those elements fold. The inner nodes must move too.
- **Geometry error at the corners of CAD faces.** Nodes on a curve where two CAD faces meet must lie on both faces. Projection to one face alone can move them off the edge.

## Exercises

1. Prove that $\det J = 1 + 4t(\xi + \eta)$ for the first classic example. *Hint:* only the shape function of the moved node changes the map, and it is $4 \xi \eta$.
2. On one edge, $\det J$ has the Bernstein coefficients $(1, b, 1)$. Show that it is positive on the whole edge if and only if $b > -1$. *Answer:* the polynomial is $1 - 2(1 - b) s (1 - s)$, For $b \le 1$ its least value on $[0, 1]$ is $(1 + b)/2$ at $s = \tfrac12$, and for $b > 1$ it is at least $1$.
3. For a cubic tetrahedron, find the degree of $\det J$ and the number of Bernstein coefficients. *Answer:* the degree is $3 \cdot 2 = 6$, and there are $\binom{6 + 3}{3} = 84$ coefficients.

## References
