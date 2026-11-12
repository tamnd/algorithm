---
tag: 0FH33C
kind: definition
slug: subdivision-surface
name: Subdivision surface
aliases:
- subdivision scheme surface
- limit surface of a subdivision scheme
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The limit of a polygon mesh under repeated refinement by fixed local rules. Each step splits the faces and sets each new vertex to a fixed weighted average of nearby old ones.
prereqs: [polygon-mesh, b-spline]
see_also: [surface-from-control-mesh, catmull-clark-subdivision, doo-sabin-subdivision, loop-subdivision, butterfly-subdivision, sqrt3-subdivision, chaikin-corner-cutting, euler-formula]
sources:
  - book: isbn:9781558604469
    title: Joe Warren and Henrik Weimer, Subdivision Methods for Geometric Design, A Constructive Approach, Morgan Kaufmann, 2002
    locator: Chapter 2, the subdivision of B-splines and box splines, and the chapters on polyhedral meshes and on the analysis at an extraordinary vertex
  - book: isbn:9783540764052
    title: Jörg Peters and Ulrich Reif, Subdivision Surfaces, Springer, 2008
    locator: Chapter 6, Case Studies of C^k_1-Subdivision Algorithms, pp. 109-124, and the earlier chapters on the subdivision matrix and the characteristic map
  - paper: doi:10.1016/0010-4485(78)90110-0
    title: E. Catmull and J. Clark, Recursively generated B-spline surfaces on arbitrary topological meshes, Computer-Aided Design 10(6), 350-355 (1978)
    locator: the first scheme for meshes of arbitrary topology that gives bicubic B-spline patches on the regular part
  - paper: doi:10.1016/0010-4485(78)90111-2
    title: D. Doo and M. Sabin, Behaviour of recursive division surfaces near extraordinary points, Computer-Aided Design 10(6), 356-360 (1978)
    locator: the dual scheme, and the eigenvalue analysis of the subdivision matrix near an extraordinary point
---

A subdivision surface is the surface that a subdivision scheme makes from a coarse [polygon mesh](/polygon-mesh/). Each step of the scheme splits every face into smaller faces, and it sets each new vertex to a fixed weighted average of a few nearby old vertices. The meshes converge to a limit surface, which is smooth for the usual schemes, and on the regular part of the mesh it is often a known spline surface. The control mesh can have any topology, which is the main advantage over [tensor product surfaces](/tensor-product-surface/).

## Definition

A *mesh* $M = (V, E, F)$ is a set of vertices with positions in $\mathbb{R}^3$, a set of edges, and a set of faces, each face a cycle of vertices. In this page the mesh is a closed 2-manifold: each edge is in exactly two faces, and the faces around each vertex form one cycle. The *valence* of a vertex is its number of edges. The [Euler characteristic](/euler-formula/) is $\chi = |V| - |E| + |F|$, and it is 2 for a sphere and 0 for a torus.

A *subdivision scheme* has two parts.

1. A **topological rule** that maps $M_k$ to a finer mesh $M_{k+1}$ of the same surface topology. The common rules are: split each face at new edge points and a new face point (primal quad split), split each triangle into four at new edge points (primal triangle split), make one new face for each old face, edge and vertex (dual split), or insert a point in each triangle and flip the old edges (the $\sqrt{3}$ split).
2. A **geometric rule** that sets the position of each vertex of $M_{k+1}$ to a linear combination of the positions of a few vertices of $M_k$ near it. The weights are the *stencil*. They depend only on the local connectivity, for example on the valence, and not on the step $k$. The weights of each stencil sum to 1, so the rule commutes with affine maps.

The *subdivision surface* is the limit of the meshes $M_k$ as $k \to \infty$, when this limit exists as a continuous surface. A scheme is *interpolating* if each step keeps the old vertices where they are, so the limit passes through every vertex of every $M_k$. Otherwise it is *approximating*.

A vertex is *regular* if its valence is the one that the scheme repeats everywhere on a regular grid: 4 for quad schemes and 6 for triangle schemes. Other vertices are *extraordinary*. The primal split rules create only regular vertices, so after one or two steps every extraordinary vertex is isolated in a region of regular ones, and the number of extraordinary vertices stays the same. In a dual scheme such as Doo-Sabin every new vertex has valence 4, and the faces that are not quads play the role of the extraordinary vertices.

Near an extraordinary vertex of valence $n$, one step maps the positions of a fixed ring of vertices to the same ring one level finer by a square matrix, the *subdivision matrix*. Its [eigenvalues](/eigenvalue/) decide the smoothness at that point. A common sufficient condition for a tangent plane is $1 = \lambda_0 > \lambda_1 = \lambda_2 > |\lambda_3|$, together with a condition on the characteristic map, which is due to Reif. The exact proofs for each scheme are long, and the pages on the schemes cite them.

## Examples and non-examples

**Examples.** The five schemes on the scheme pages:

| Scheme | Faces | Split | Kind | $V'$ | $E'$ | $F'$ | Regular part | Extraordinary vertex |
|---|---|---|---|---|---|---|---|---|
| [Catmull-Clark](/catmull-clark-subdivision/) | any, quads after one step | primal | approximating | $V + E + F$ | $2E + \sum_f \deg f$ | $\sum_f \deg f$ | bicubic B-spline, $C^2$ | $C^1$ |
| [Doo-Sabin](/doo-sabin-subdivision/) | any | dual | approximating | $2E$ | $4E$ | $V + E + F$ | biquadratic B-spline, $C^1$ | $C^1$ |
| [Loop](/loop-subdivision/) | triangles | primal | approximating | $V + E$ | $2E + 3F$ | $4F$ | quartic box spline, $C^2$ | $C^1$ |
| [Butterfly](/butterfly-subdivision/) | triangles | primal | interpolating | $V + E$ | $2E + 3F$ | $4F$ | $C^1$ | not $C^1$ at some valences in the original form |
| [$\sqrt{3}$](/sqrt3-subdivision/) | triangles | insert and flip | approximating | $V + F$ | $E + 3F$ | $3F$ | $C^2$ | $C^1$ |

Here $V, E, F$ are the counts of $M_k$ and $V', E', F'$ the counts of $M_{k+1}$. For a closed mesh $\sum_f \deg f = 2E$, so each row keeps $\chi$: for example $(V + E + F) - 4E + 2E = V - E + F$ for Catmull-Clark.

**A cube.** Take the cube $[-1, 1]^3$ as a quad mesh with $V = 8$, $E = 12$, $F = 6$, so $\chi = 2$. One Catmull-Clark step gives $V' = 26$, $E' = 48$ and $F' = 24$, and $\chi$ is still 2. The corner $(1, 1, 1)$ has valence 3, so it is extraordinary, and it moves to $(5/9, 5/9, 5/9)$. The limit is a smooth closed surface like a rounded cube, with 8 extraordinary points that stay at valence 3 at every level.

**The curve case.** For a closed polygon, [Chaikin's corner cutting](/chaikin-corner-cutting/) is a subdivision scheme whose limit is the quadratic uniform [B-spline](/b-spline/) curve, the [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/) gives every degree, and the [four-point scheme](/four-point-scheme/) is interpolating. A curve has no extraordinary vertices, so the whole analysis is the regular one. The surface schemes on a regular grid reduce to products or box spline forms of these rules.

**Non-examples.**

- *Midpoint refinement alone.* Splitting each face at the midpoints of its edges, with no averaging, refines the mesh, but every new vertex lies on an old face. The limit is the input polyhedron itself, which is not smooth. It meets the definition of a scheme, but its limit is only $C^0$, so it does not make a smooth subdivision surface.
- *A global smoothing step.* A refinement that solves one linear system over the whole mesh for the new positions, for example to minimize a bending energy, is not a stationary subdivision scheme: the weights depend on the whole mesh and on the level.
- *Rules with weights that change with the level.* Non-stationary schemes exist, for example those that reproduce circles, but they are outside the definition above.
- *Meshes with boundary.* The definition needs extra rules for boundary edges and corners. The usual choice applies a curve scheme, such as the cubic B-spline rule or the four-point rule, along the boundary.

## Related definitions

- **Control mesh.** The mesh $M_0$. The problem of making a smooth surface from it is [surface from a control mesh](/surface-from-control-mesh/).
- **Limit point and limit position.** The point of the limit surface that corresponds to a vertex. It is the left eigenvector of the subdivision matrix for the eigenvalue 1, applied to the positions of the ring, and each scheme has a closed formula for it.
- **Primal and dual schemes.** In a primal scheme the old vertices correspond to new vertices. In a dual scheme the old faces correspond to new faces, as in Doo-Sabin and Chaikin.
- **Knot insertion.** On a regular grid, the approximating quad schemes are [knot refinement](/knot-refinement/) of uniform tensor product B-splines, with every knot interval halved.
- **Exact evaluation.** At a regular point the limit is a B-spline or box spline patch, and it can be evaluated directly. Near an extraordinary vertex the eigen decomposition of the subdivision matrix gives a direct formula, which Stam gave for Catmull-Clark in 1998.
- **Tessellation.** To draw a limit surface, stop after a few steps, or evaluate it at chosen parameters. See [surface tessellation](/surface-tessellation/).
- **Simplification.** The opposite direction, from a fine mesh to a coarse one, is [mesh simplification](/mesh-simplification/).

## References
