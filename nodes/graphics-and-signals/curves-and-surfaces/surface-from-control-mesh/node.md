---
tag: 7GFFRY
kind: problem
slug: surface-from-control-mesh
name: Smooth surface from a control mesh
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Given a polygon mesh of any topology, build a smooth surface that it controls locally and that is the standard spline surface wherever the mesh is a regular grid.
model: real-ram
complexity:
  vars: {n: the number of faces of the control mesh, k: the number of refinement steps}
  time: {worst: "O(4^k n)"}
prereqs: [polygon-mesh, parametric-surface]
see_also: [subdivision-surface, catmull-clark-subdivision, loop-subdivision, doo-sabin-subdivision, butterfly-subdivision, bezier-triangle, bezier-patch, surface-tessellation]
sources:
  - paper: doi:10.1016/0010-4485(78)90110-0
    title: Edwin Catmull and James Clark, Recursively Generated B-spline Surfaces on Arbitrary Topological Meshes, Computer-Aided Design 10(6), 350-355 (1978)
    locator: the face, edge and vertex rules that generalize bicubic B-spline refinement to meshes with any valence
  - paper: doi:10.1016/0010-4485(78)90111-2
    title: Daniel Doo and Malcolm Sabin, Behaviour of Recursive Division Surfaces Near Extraordinary Points, Computer-Aided Design 10(6), 356-360 (1978)
    locator: the biquadratic scheme and the eigenvalue analysis of the subdivision matrix at an extraordinary point
  - paper: doi:10.1016/0167-8396(94)00007-F
    title: Ulrich Reif, A Unified Approach to Subdivision Algorithms Near Extraordinary Vertices, Computer Aided Geometric Design 12(2), 153-174 (1995)
    locator: the characteristic map and the conditions on the subdivision matrix for a tangent plane continuous limit
  - paper: doi:10.1137/S0036142996304346
    title: Jorg Peters and Ulrich Reif, Analysis of Algorithms Generalizing B-Spline Subdivision, SIAM Journal on Numerical Analysis 35(2), 728-748 (1998)
    locator: the analysis of the schemes that generalize biquadratic and bicubic B-spline subdivision
  - paper: doi:10.1145/280814.280945
    title: Jos Stam, Exact Evaluation of Catmull-Clark Subdivision Surfaces at Arbitrary Parameter Values, Proceedings of SIGGRAPH 98, 395-404 (1998)
    locator: evaluation near an extraordinary vertex by the eigen decomposition of the subdivision matrix
  - paper: doi:10.1145/1330511.1330519
    title: Charles Loop and Scott Schaefer, Approximating Catmull-Clark Subdivision Surfaces with Bicubic Patches, ACM Transactions on Graphics 27(1), Article 8 (2008)
    locator: one bicubic patch per quad face with separate tangent patches, for hardware tessellation
  - paper: doi:10.1145/364338.364387
    title: Alex Vlachos, Jorg Peters, Chas Boyd and Jason L. Mitchell, Curved PN Triangles, Proceedings of the 2001 Symposium on Interactive 3D Graphics, 159-166 (2001)
    locator: a cubic triangle per flat triangle from its vertex positions and normals, with a quadratic normal field
---

The problem is to turn a coarse [polygon mesh](/polygon-mesh/) into a smooth surface. Designers and artists shape objects by moving the few vertices of such a mesh, the control mesh, and they want a surface that follows the mesh, changes only near a moved vertex, and has no creases. Where the mesh is a regular grid of quads, the answer is known: the bicubic B-spline surface of the grid. The hard part is the rest: the vertices where more or fewer than four faces meet, which every closed mesh of a sphere must have.

## In plain words

An artist builds a rough model from a few flat faces, like a box for a head. The computer must turn it into a smooth shape that looks like the box with its corners rounded off. Moving one corner of the box should only change the shape near that corner. Where the faces form a neat grid, there is a classical way to do this. But a closed box cannot be a neat grid everywhere: at some corners three faces meet, at others five. The methods for this problem differ mainly in how they treat those corners. Some cut every face into smaller faces again and again, and the limit is smooth. Others put one curved patch on each face and make the patches fit together.

## Definition

**Input.** A polygon mesh $M_0$ that is a 2-manifold, possibly with boundary, with vertex positions in $\mathbb{R}^3$. For a quad scheme the faces are usually quads, and for a triangle scheme triangles. A vertex is regular when it has the valence of the regular grid, 4 for quads and 6 for triangles, and extraordinary otherwise.

**Output.** A surface $S$, given as a map from a domain built from the faces of $M_0$ into $\mathbb{R}^3$, or as a mesh that approximates it within a tolerance, with these properties:

- **Smoothness.** $S$ is tangent plane continuous ($G^1$) everywhere, and $C^2$ away from a finite set of points.
- **Locality.** Each point of $S$ depends only on the vertices within a fixed number of rings around its face.
- **Affine invariance.** Applying an affine map to the control vertices applies it to $S$.
- **Reproduction.** Where the mesh is a regular grid, $S$ is the standard spline surface of the grid: the uniform bicubic B-spline surface for quads, and the quartic box spline surface for triangles.
- **Shape.** $S$ lies in the convex hull of the control vertices, or at least close to the mesh, so that it follows the mesh as a designer expects.

The cost model is the real RAM. Inputs have bounded valence, and the cost counts the vertices of the output mesh, or the points of $S$ evaluated.

**The topological obstruction.** For a closed mesh of quads with $V$ vertices, $E$ edges and $F$ faces, $4F = 2E$ and the sum of valences is $2E$, so

$$\sum_{v} (4 - \operatorname{val}(v)) = 4V - 2E = 4(V - E + F) = 4\chi.$$

For triangles, $3F = 2E$ gives $\sum_v (6 - \operatorname{val}(v)) = 6\chi$ in the same way. A closed mesh of the sphere has $\chi = 2$, so it must have extraordinary vertices, and only the surfaces with $\chi = 0$, the torus and the Klein bottle (the torus if the mesh is oriented), can be covered by a regular grid. So the spline surface of a grid alone cannot solve the problem, and every method needs a rule for extraordinary vertices.

## Variants

- **Subdivision.** Refine the mesh by fixed local rules again and again, and take the limit. This is the [subdivision surface](/subdivision-surface/) of the mesh. That page defines the limit and its properties; this page is the problem that it is one answer to.
- **Patch constructions.** Put one or a few polynomial or rational patches on each face, such as [Bézier patches](/bezier-patch/) or [Bézier triangles](/bezier-triangle/), and choose their control points so that they join smoothly. These give a finite description that CAD systems and GPUs can use directly.
- **Approximating against interpolating.** Most schemes move the control vertices, and the surface passes near them. Interpolating schemes, such as [butterfly subdivision](/butterfly-subdivision/), keep every vertex on the surface, and the surfaces they give are usually less fair.
- **Quads, triangles or mixed meshes.** Schemes exist for each kind, and Catmull-Clark accepts any polygons, which become quads after one step.
- **Features.** Production schemes add rules for boundaries, sharp creases and corners, by tagging edges and using curve rules along them.
- **Exact evaluation.** Given a face and a parameter $(u, v)$, compute the limit point and its derivatives without refining the whole mesh.

## Examples

- **A cube under Catmull-Clark.** The cube has $(V, E, F) = (8, 12, 6)$. One step adds a point per face and per edge and splits each face into 4 quads, giving $(26, 48, 24)$, and a second step gives $(98, 192, 96)$. In each step $V' = V + E + F$, $F' = 4F$ for a quad mesh and $E' = 2E + 4F$, and $\chi = 2$ stays. The 8 corners have valence 3, and $\sum (4 - 3) = 8 = 4\chi$; the new vertices all have valence 4, so the 8 corners stay the only extraordinary vertices. The limit is a rounded box, $C^2$ except at those 8 points, where it is $C^1$.
- **An octahedron under Loop.** $(V, E, F) = (6, 12, 8)$ becomes $(18, 48, 32)$: every edge gets a new vertex and every triangle splits into 4. The 6 old vertices have valence 4, and $\sum (6 - 4) = 12 = 6\chi$. The limit is close to a sphere but is not one.
- **The regular case.** In a part of a quad mesh where all vertices have valence 4, each face with its ring of 16 control vertices is a uniform bicubic B-spline patch, and Catmull-Clark refinement is exactly B-spline knot insertion there. In a regular part of a triangle mesh, each Loop face is a quartic box spline piece, which is a quartic [Bézier triangle](/bezier-triangle/) with 15 control points.
- **A grid on a torus.** A torus can be covered by an $a \times b$ grid of quads with all valences 4. Its Catmull-Clark limit is then a closed bicubic B-spline surface with no extraordinary points at all, which the obstruction above allows only for $\chi = 0$.

## Known algorithms

- **[Catmull-Clark subdivision](/catmull-clark-subdivision/)** (1978) generalizes bicubic B-spline refinement to any mesh. Its limit is $C^2$ away from the extraordinary vertices and $C^1$ at them.
- **[Doo-Sabin subdivision](/doo-sabin-subdivision/)** (1978) generalizes biquadratic B-spline refinement by cutting corners. Its limit is $C^1$. Doo and Sabin also began the analysis of the limit at an extraordinary point through the eigenvalues of the local subdivision matrix.
- **[Loop subdivision](/loop-subdivision/)**, from Charles Loop's 1987 thesis, generalizes the quartic box spline to triangle meshes. Its limit is $C^2$ at regular points and $C^1$ at extraordinary vertices.
- **Butterfly and $\sqrt 3$ subdivision.** [Butterfly](/butterfly-subdivision/) interpolates the vertices of a triangle mesh. [$\sqrt 3$ subdivision](/sqrt3-subdivision/) refines more slowly, by a factor 3 in the number of faces per step, which gives finer control over the mesh size.
- **Exact evaluation** (Stam 1998). Near an extraordinary vertex the limit is a sum over the eigenvectors of the subdivision matrix, so a point at any parameter costs a constant number of operations for a fixed valence after a precomputation, with no refinement.
- **Approximate Catmull-Clark** (Loop and Schaefer 2008) puts one bicubic patch on each quad, equal to the Catmull-Clark limit on regular faces, and a separate pair of tangent patches to give a continuous normal field. It is made for GPU tessellation.
- **PN triangles** (Vlachos, Peters, Boyd and Mitchell 2001) put a cubic Bézier triangle with 10 control points on each flat triangle, from its vertex positions and normals only, and a quadratic normal field. Each patch needs no neighbors, so it suits hardware, but the patches meet with continuous position only, and the normal field hides the creases in shading.

## Bounds

- **Output size.** For a quad scheme, each step multiplies the number of faces by 4, so $k$ steps on a mesh of $n$ faces give $\Theta(4^k n)$ faces, and with bounded valence each new vertex costs a constant. So $k$ steps cost $\Theta(4^k n)$ in the worst case, which equals the output size and is therefore optimal. Triangle schemes with 1 to 4 splits have the same bound, and $\sqrt 3$ subdivision gives $\Theta(3^k n)$.
- **Approximation.** In regular regions the refined mesh after $k$ steps is within $O(4^{-k})$ of the limit, as for a B-spline control polygon, so $k = O(\log(1/\epsilon))$ steps reach a tolerance $\epsilon$, and the output has $O(n/\epsilon)$ faces. This is an asymptotic bound with a constant that depends on the mesh.
- **Smoothness at extraordinary points.** For a stationary linear scheme, the behavior of the limit at an extraordinary point is decided by the eigenvalues and eigenvectors of the local subdivision matrix and by the characteristic map that they define (Reif 1995). Peters and Reif (1998) apply this analysis to the schemes that generalize biquadratic and bicubic B-spline subdivision. The standard schemes are $C^1$ but not $C^2$ at extraordinary points, and getting $C^2$ there needs more complex rules or patches of higher degree.

## Reductions

- **To spline evaluation.** In regular regions the problem reduces to the evaluation of tensor-product B-splines or box splines, with the [de Boor](/de-boor-algorithm/) or de Casteljau algorithm on each patch.
- **To an eigenproblem.** Exact evaluation and the smoothness analysis at an extraordinary vertex reduce to the eigen decomposition of a fixed matrix per valence, computed once.
- **To tessellation.** A patch construction gives patches that a [tessellator](/surface-tessellation/) turns into a mesh. A subdivision scheme gives a mesh directly, and a few steps of refinement are a uniform tessellation of the limit.
- **From curves.** Restricted to a boundary or a sharp crease, the quad schemes reduce to the curve rules of uniform cubic B-splines, so the [curve version](/curve-from-control-polygon/) of the problem is a special case.

## Applications

- **Film and animation.** Characters are modeled as coarse quad meshes and drawn as Catmull-Clark limit surfaces, refined until each face is smaller than a pixel.
- **Games and real-time graphics.** GPU tessellation draws approximate Catmull-Clark patches or PN triangles, so a game can send a coarse mesh and get a smooth silhouette.
- **Modeling tools.** Most polygon modelers offer a subdivision preview, so the artist moves the control mesh and sees the smooth result.
- **CAD and engineering.** Free-form parts can start as a control mesh and then be converted to [NURBS](/nurbs/) patches, which needs a patch construction with exact or approximate joins at the extraordinary points.

## References
