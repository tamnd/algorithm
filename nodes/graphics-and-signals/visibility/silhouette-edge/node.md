---
tag: 9A6GDM
kind: concept
slug: silhouette-edge
name: Silhouette edge
aliases:
- contour edge
area: graphics-and-signals/visibility
level: core
summary: An edge of a closed polygon mesh between a face that turns toward the viewer and a face that turns away. These edges form closed loops, and the outline of the image lies on them.
prereqs: [back-face-culling, polygon-mesh]
see_also: [appel-hidden-line-algorithm, roberts-hidden-line-algorithm, hidden-line-removal, shadow-volume-algorithm, shadow-mapping, back-face-culling, convex-polytope, polygon-mesh]
sources:
  - paper: doi:10.1145/800196.806007
    title: Arthur Appel, The notion of quantitative invisibility and the machine rendering of solids, Proceedings of the 1967 22nd National Conference of the ACM, pages 387 to 393
    locator: the definition of contour lines and their use for quantitative invisibility
  - paper: doi:10.1145/258734.258894
    title: Lee Markosian, Michael A. Kowalski, Samuel J. Trychin, Lubomir D. Bourdev, Daniel Goldstein and John F. Hughes, Real-time nonphotorealistic rendering, SIGGRAPH 1997, pages 415 to 420
    locator: the randomized search for silhouette edges with coherence between frames
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the survey of object-space line algorithms and their use of contour edges
---

A silhouette edge, or contour edge, of a closed polygon mesh is an edge where one of its two faces turns toward the viewer and the other turns away. The two words are used in slightly different ways: some authors keep "silhouette" for the outline of the image of the object, and use "contour" for all edges with this front and back property. This page uses the second meaning for both words. The outline of the image always lies on contour edges, but a contour edge can also be inside the image or hidden. Contour edges depend on the viewpoint, so they change when the camera moves. The test for one face is [back-face culling](/back-face-culling/); a silhouette edge is the border between the faces that culling keeps and the faces it removes. Line drawing algorithms such as [Appel's](/appel-hidden-line-algorithm/) and shadow methods such as [shadow volumes](/shadow-volume-algorithm/) use these edges. The word "contour" has other meanings in other areas, such as the curves of [active contours](/active-contours/) in image processing and the iso-surfaces of [dual contouring](/dual-contouring/); those are a different idea.

## In plain words

Hold a box in front of a lamp and look at its shadow on the wall. The edge of the shadow comes from edges of the box where one side of the edge faces the lamp and the other side faces away. These are the silhouette edges, seen from the lamp. Seen from your eye, the same rule picks out the edges that a person would draw to show the outline of the box. If you turn the box, other edges take their place. For a shape with dents, some of these edges are behind other parts of the shape, and some of them are in the middle of the picture, not at its outer border.

## The idea

**Setting.** A *closed mesh* is a set of flat polygons (faces) where each edge is shared by exactly two faces. Each face $f$ has an outward normal $n_f$ and a point $p_f$ on it. For a viewer at the eye point $e$ (a perspective view), the face is *front-facing* if $n_f \cdot (e - p_f) > 0$ and *back-facing* if $n_f \cdot (e - p_f) < 0$. For a parallel view along a direction, replace $e - p_f$ by the fixed vector $v$ that points toward the viewer. The view is in *general position* if no face gives $0$, that is, if no face is seen edge-on.

**Definition.** An edge with the faces $f_1$ and $f_2$ is a *silhouette edge* (or contour edge) if one of $f_1, f_2$ is front-facing and the other is back-facing.

**Test.** One pass over the edges finds them all: compute the sign for each face once, and keep the edges whose two faces have different signs. This takes $O(F + E)$ time for $F$ faces and $E$ edges. It needs only the face signs, not the depth order, so it is a local test.

**Property 1 (closed loops).** In general position, each vertex of a closed manifold mesh lies on an even number of silhouette edges, so the silhouette edges form closed loops.

*Proof.* Around a vertex $w$, the faces and edges that meet at $w$ form one cycle, face, edge, face, edge, and so on. Each edge in the cycle is a silhouette edge exactly when the faces on its two sides have different signs. When you go once around the cycle and come back to the first face, the sign has changed an even number of times. So $w$ has an even number of silhouette edges. A finite graph where every vertex has even degree is a union of closed loops that do not share edges. $\square$

**Property 2 (concave silhouette edges are hidden).** Take a silhouette edge where the inside angle of the solid is more than $\pi$, a concave edge. Then the view ray to any point of the edge passes through the solid just before it reaches the edge, so the edge is hidden.

*Proof.* Put the point $o$ of the edge at the origin, let $w$ be the direction from the eye to $o$, and let $f_1$ be the front face and $f_2$ the back face, so $n_1 \cdot w < 0 < n_2 \cdot w$. At a concave edge the outside of the solid near $o$ is the wedge where $n_1 \cdot x > 0$ and $n_2 \cdot x > 0$, and the inside is the rest. The point $x = -s w$ for a small $s > 0$ lies on the ray just before $o$, and $n_2 \cdot x = -s\, n_2 \cdot w < 0$. So $x$ is inside the solid. $\square$

At a convex edge the same computation puts $x$ outside, so a convex silhouette edge is not hidden by its own two faces, but other parts of the scene can still hide it.

**Property 3 (the outline).** If a point of the image is on the outer border of the image of the solid, the view ray through it touches the solid without going inside. In general position such a ray meets the mesh at a point of a silhouette edge, or at a vertex on one. So the outline of the image is the image of part of the silhouette loops. For a convex solid, every face that the eye can see is front-facing, the silhouette is one loop, and its image is the boundary of the image of the solid, a convex polygon.

**Smooth surfaces.** On a smooth surface the same idea gives the *contour generator*, the curve of points $p$ where the view ray is tangent to the surface: $n(p) \cdot (e - p) = 0$. The silhouette edges of a fine mesh follow this curve, but they can zigzag along the mesh edges near it.

**Other edges that drawings use.** A line drawing often also shows *boundary edges* of an open mesh (edges with only one face) and *crease edges*, where two faces meet at a sharp angle. These are fixed and do not depend on the viewer. Silhouette edges are the only kind that move when the viewer moves.

## Examples

**A cube seen from a corner.** Take the cube $[0, 1]^3$ and the eye at $e = (3, 2, 5)$. The eye is outside the planes $x = 1$, $y = 1$ and $z = 1$, so those three faces are front-facing and the other three are back-facing. An edge between two front faces or two back faces is not a silhouette edge, and this leaves 6 of the 12 edges: the loop $(0,0,1)$, $(0,1,1)$, $(0,1,0)$, $(1,1,0)$, $(1,0,0)$, $(1,0,1)$ and back to $(0,0,1)$. Its image is the hexagon that outlines the picture of the cube. The three edges at the corner $(1, 1, 1)$ are inside the picture, between front faces.

**A cube seen from above.** With the eye at $(1/2, 1/2, 5)$ only the top face $z = 1$ is front-facing, and the silhouette is the loop of its 4 edges. Its image is a square, and the picture shows only the top face.

**An L-shaped prism.** Take the prism with the cross-section $(0,0)$, $(2,0)$, $(2,1)$, $(1,1)$, $(1,2)$, $(0,2)$ in the $xz$-plane and $0 \le y \le 1$, with 8 faces and 18 edges, in a parallel view with the vector $v = (1, 1/2, -1)$ toward the viewer, so the viewer is on the side of large $x$, a little toward large $y$, and below. The front-facing faces are the bottom $z = 0$, the two faces $x = 2$ and $x = 1$ with the normal $(1, 0, 0)$, and the face $y = 1$. There are 10 silhouette edges, and they form one loop. One of them is the concave edge from $(1, 0, 1)$ to $(1, 1, 1)$, between the front face $x = 1$ and the back face $z = 1$. By Property 2 it is hidden: the view ray to it passes through the lower block $[0, 2] \times [0, 1] \times [0, 1]$ first.

## Where it is used

- **Hidden-line removal.** In [Appel's algorithm](/appel-hidden-line-algorithm/) the number of faces in front of a point of an edge changes only where the edge passes behind a silhouette edge. So only silhouette edges, not all edges, are tested as possible blockers. [Roberts' algorithm](/roberts-hidden-line-algorithm/) uses the same front and back test on each convex solid. See [hidden-line removal](/hidden-line-removal/).
- **Shadows.** The [shadow volume algorithm](/shadow-volume-algorithm/) finds the silhouette edges as seen from the light and extends them away from the light to bound the shadow. [Shadow mapping](/shadow-mapping/) works on depth images and does not need them.
- **Line drawings and stylized rendering.** Drawings of 3D models in the style of a sketch or a cartoon draw the visible silhouette edges with strokes. Markosian and others (1997) find them fast for a moving camera: they test a random sample of edges and then follow each loop from edge to edge, and they keep edges found in the previous frame as starting points.
- **Mesh simplification.** A simplified mesh with the same silhouette looks the same from a given view, so view-dependent methods keep more detail near the silhouette (see [mesh simplification](/mesh-simplification/)).

## References
