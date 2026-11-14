---
tag: 876K96
kind: technique
slug: mesh-untangling
name: Mesh untangling
aliases:
- inverted element repair
area: cad/mesh-generation-for-analysis
level: advanced
summary: Moves vertices to make every element Jacobian positive by maximising the smallest signed volume, as Knupp and Freitag and Plassmann proposed, before smoothing.
prereqs: [mesh-quality-measures, linear-programming-problem, orientation-test]
see_also: [optimization-based-mesh-smoothing, simplex-method, laplacian-smoothing, convex-function, finite-element-method, mesh-generation]
sources:
  - paper: doi:10.1002/1097-0207(20000910/20)49:1/2<109::AID-NME925>3.0.CO;2-U
    title: Lori A. Freitag and Paul Plassmann, Local optimization-based simplicial mesh untangling and improvement, International Journal for Numerical Methods in Engineering 49(1-2), 2000, 109 to 125
    locator: the untangling of one vertex as a linear program that maximises the smallest signed area or volume, solved by the simplex method, followed by smoothing (general locator)
  - paper: doi:10.1007/s003660170006
    title: Patrick M. Knupp, Hexahedral and tetrahedral mesh untangling, Engineering with Computers 17(3), 2001, 261 to 268
    locator: the untangling objective, the sum of |alpha - beta| - (alpha - beta) over the corner Jacobian determinants, for tetrahedra and hexahedra (general locator)
  - book: isbn:978-1-84821-029-5
    title: Pascal Jean Frey and Paul-Louis George, Mesh Generation, Application to Finite Elements, 2nd edition, ISTE and Wiley, 2008
    locator: chapter 18 (mesh optimisation)
---

Mesh untangling repairs a mesh in which some elements are inverted, that is, turned inside out, with a negative signed area, volume or Jacobian determinant. Such elements appear when a mesh is moved to follow a deforming body, when a smoother such as [Laplacian smoothing](/laplacian-smoothing/) moves a vertex outside the region where its elements are valid, or when a hexahedral mesh is projected onto a curved boundary. A finite element code cannot use an inverted element, and quality measures that assume positive volume give wrong answers on it. Untangling moves the free vertices, keeping the boundary and the connectivity fixed, so that every signed volume becomes positive. Freitag and Plassmann solve one vertex at a time as a linear program; Knupp minimises a convex penalty on the negative Jacobians. Both are followed by smoothing, because an untangled mesh is valid but often poor.

## In plain words

Some tiles of a mesh are folded over, like a sheet of paper creased back on itself. Each tile has a signed size: positive when it lies the right way up, negative when it is folded. The task is to slide the inner corner points, without changing which corners make each tile, until every tile has a positive size.

Take one corner point and the ring of tiles around it. The size of each tile changes in a straight line as the point moves. So the question "where should the point go to make the smallest size as large as possible" is a linear program, which has an exact answer. If the best smallest size is positive, the ring is fixed. If it is not, no place for this point can fix the ring, and other points or the connections must change.

## When it applies

- The mesh has a fixed connectivity and some elements with negative signed area, volume or Jacobian determinant at a corner.
- Some vertices may move; usually the boundary vertices are fixed, or may move only along the boundary.
- For triangles and tetrahedra, the signed volume is affine in the position of any one vertex. This is what makes the local problem linear and the penalty convex. For quadrilaterals and hexahedra, the Jacobian determinant at each corner is the signed volume of the corner tetrahedron, so the same holds corner by corner.
- It does not apply when the region around a vertex has no valid position at all. Then the problem needs moves of several vertices together, edge flips or a remesh.

## The template

For a free vertex $x$ with star elements $e_1, \dots, e_m$, let $\alpha_i(x)$ be the signed area of $e_i$ (twice the area, or the Jacobian determinant, gives the same results). Each $\alpha_i$ is affine in $x$.

```pseudo id=main
UNTANGLE(mesh, free vertices)
L1  repeat
L2      for each free vertex x with an inverted element in its star do
L3          solve the linear program: maximise t subject to α_i(x) ≥ t for i = 1, ..., m
L4          if the optimum t* > 0 then move x to the optimal position
L5          else note that the star of x has no valid position
L6  until no element is inverted, or no move helps
L7  smooth the mesh with a method that keeps the elements valid
```

**Why the linear program decides it.** The kernel of the star is the set of positions with all $\alpha_i(x) > 0$. If the kernel contains a point $y$, then $(y, \min_i \alpha_i(y))$ is feasible with $t > 0$, so $t^* > 0$. Conversely, if $t^* > 0$, the optimal position has every $\alpha_i \ge t^* > 0$, so it is in the kernel. The program is bounded: for the signed areas of a star in the plane, $\sum_i \alpha_i(x)$ is the area of the link polygon for every $x$, by the shoelace formula, so $t \le (\text{link area})/m$. The program has 3 variables in 2D and 4 in 3D, and $m$ constraints, so the [simplex method](/simplex-method/) or any small LP solver finds the exact optimum quickly. Freitag and Plassmann used the simplex method. The optimum is not only valid but as far from inversion as possible, which is a good start for smoothing.

**Knupp's penalty.** Knupp minimises, over all free vertices together or one at a time,

$$f = \sum_{\text{corners } k} \bigl(|\alpha_k - \beta| - (\alpha_k - \beta)\bigr) = \sum_k 2\max(\beta - \alpha_k, 0),$$

where $\alpha_k$ is the Jacobian determinant at corner $k$ and $\beta > 0$ is a small target. A corner with $\alpha_k \ge \beta$ costs nothing; a corner below $\beta$ costs twice its shortfall. So $f = 0$ exactly when every corner has $\alpha_k \ge \beta$, and then the mesh is untangled. As a function of one vertex position, each $\alpha_k$ is affine and $\max(\beta - \alpha_k, 0)$ is convex, so $f$ is a [convex function](/convex-function/) of that vertex, and a local minimum over one vertex is global. Over all vertices together, $\alpha_k$ is a polynomial of degree 2 or 3 in the coordinates and $f$ is not convex.

## Classic examples

**An arrow-shaped star.** The link polygon $(-2, 0)$, $(0, -2)$, $(6, -1)$, $(1, 0)$, $(6, 1)$, $(0, 2)$ has a notch at $(1, 0)$. Laplacian smoothing puts the free vertex at the mean of the link, $(11/6, 0)$, beyond the notch, and the six signed areas are $23/6$, $61/12$, $-5/12$, $-5/12$, $61/12$ and $23/6$. Two triangles are folded. The linear program, solved exactly by checking the vertices of the feasible region, gives $t^* = 1$ at $x = (-1, 0)$, where the signed areas are $1$, $13/2$, $1$, $1$, $13/2$, $1$. They sum to 17, the area of the link polygon, as the shoelace identity says. Knupp's penalty with $\beta = 1/10$ and $\alpha$ equal to twice the area is $56/15$ at the Laplacian position and $0$ at the LP optimum.

**A star with no valid position.** The U-shaped link $(0,0)$, $(3,0)$, $(3,3)$, $(2,3)$, $(2,1)$, $(1,1)$, $(1,3)$, $(0,3)$ has an edge from $(2, 3)$ down to $(2, 1)$, whose left side is $x > 2$, and an edge from $(1, 1)$ up to $(1, 3)$, whose left side is $x < 1$. No point is on both sides, so the kernel is empty. The linear program confirms it: $t^* = -1/2$, at $(3/2, -1/3)$, where three triangles still have signed area $-1/2$. Moving this vertex alone cannot untangle the star; a neighbour must move, or the connectivity must change.

**Mesh motion.** When a boundary moves, as in a fluid and structure computation, the interior vertices follow by some rule, and elements near a fast moving part fold. Untangling the folded region, then smoothing, keeps the mesh usable without a new mesh.

**Hexahedral meshes.** A hexahedral mesh projected onto a curved surface often has corners with negative Jacobian near the surface. Knupp's penalty works on the eight corner Jacobians of each hexahedron, with the interior vertices free.

## Variations

- **Global versus local.** The LP is local, one vertex at a time, in Gauss-Seidel sweeps. Knupp's penalty can be minimised over all vertices together with a gradient method, which moves several vertices at once and can fix stars that no single move fixes.
- **Shifted barriers.** Escobar, Montenegro and coauthors replaced the volume by a regularised value $\frac12(\alpha + \sqrt{\alpha^2 + 4\delta^2})$ inside a smooth quality measure, so that one smooth objective untangles and smooths at the same time.
- **Boundary vertices.** Allowing boundary vertices to slide along the boundary curve or surface enlarges the kernel and fixes many cases near curved boundaries.
- **Connectivity changes.** When the kernel is empty, an edge flip in 2D or a face or edge flip in 3D, as in [topological tetrahedral mesh improvement](/topological-tetrahedral-mesh-improvement/), changes the star.
- **After untangling.** [Optimization-based mesh smoothing](/optimization-based-mesh-smoothing/) then raises the worst quality and keeps every element valid, because it accepts only moves that stay in the kernel.

## Pitfalls

- **Smoothing a tangled mesh.** Many quality measures are positive for a folded element, for example those built from edge lengths only. A smoother that uses them can make a tangled mesh look good. Untangle with a signed measure first.
- **Float signs.** A nearly flat element can get the wrong sign. Use exact orientation and volume tests to decide whether an element is inverted.
- **Empty kernel.** If $t^* \le 0$, no position of that vertex works. Repeating the local step does not help; move neighbours, flip, or remesh.
- **Stopping at $t^* > 0$ only just.** An LP optimum with a tiny $t^*$ is valid but almost flat. Smooth after untangling.
- **Corner Jacobians of hexahedra.** For a hexahedron, positive Jacobians at the eight corners do not imply a positive Jacobian everywhere inside, because the Jacobian is not linear. Check more points, or use a sufficient condition, when this matters.
- **Choosing $\beta$.** With $\beta = 0$, Knupp's penalty is zero for a mesh that has flat elements. A small positive $\beta$, a fraction of the mean element size, pushes elements away from zero.

## Exercises

- Show that for the signed areas of a star in the plane, $\sum_i \alpha_i(x)$ does not depend on $x$, and conclude that $t^* \le (\text{link area})/m$. Deduce that a link polygon with negative or zero signed area has no valid position.
- Show that for a tetrahedron the signed volume is affine in each vertex, and write the linear program of one free vertex in 3D. How many variables does it have?

## References
