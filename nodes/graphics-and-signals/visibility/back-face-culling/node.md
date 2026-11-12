---
tag: CT7W19
kind: algorithm
slug: back-face-culling
name: Back-face culling
aliases:
- backface culling
- back-face removal
area: graphics-and-signals/visibility
level: intro
summary: Drop each face of a closed mesh whose outer side does not face the viewer. One sign test per face; it never drops a visible face when the viewer is outside.
solves: [visibility-culling]
model: real-ram
complexity:
  vars: {F: the number of faces}
  time: {worst: Θ(F), average: Θ(F), best: Θ(F)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1963
  people: [Lawrence G. Roberts]
  note: Roberts removed the faces of each convex solid that point away from the viewer as the first step of his hidden line method. The step became a standard part of each polygon renderer.
prereqs: [hidden-surface-removal, polygon-mesh, cross-product, dot-product]
see_also: [silhouette-edge, frustum-culling, occlusion-culling, z-buffer, shadow-volume-algorithm, orientation-test, convex-polytope, hidden-line-removal]
sources:
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 19, Section 19.3 (Backface Culling), page 831
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, 1990
    locator: Chapter 15, Section 15.2 (techniques for efficient visible-surface algorithms, back-face culling)
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the discussion of back-facing polygons as a first step of the object space algorithms
---

Back-face culling drops each face of a closed [polygon mesh](/polygon-mesh/) whose outer side does not face the viewer. One sign test per face decides it: the face is kept when the viewer is strictly on the outer side of the plane of the face. When the mesh is closed and the viewer is outside it, a dropped face cannot be seen, so the image does not change. It is a speed step, not a [hidden surface](/hidden-surface-removal/) algorithm: a kept face can still be hidden by another part of the mesh, and a [z-buffer](/z-buffer/) or another visibility method must still resolve it. It is a simple case of [visibility culling](/visibility-culling/).

## In plain words

Think of a closed box. Each side has an outside and an inside. From any point outside the box you can see only the sides whose outside faces you. The sides that face away are behind the box, and the front sides hide them.

So a renderer can throw those sides away before it draws them. For each side it asks one question: is the eye on the outer side of the plane of this side? If not, it skips the side. For a closed object this removes about half of the faces.

The test says nothing about one object in front of another, or about a bumpy object that hides parts of itself. It only removes faces that face away.

## The problem

The input is a list of $F$ triangles $f_0, \ldots, f_{F-1}$ in 3D and the viewer, a point $E$. Each triangle $(v_0, v_1, v_2)$ is listed so that its normal $n = (v_1 - v_0) \times (v_2 - v_0)$ points to the *outer side* of the surface. That is, seen from outside, the vertices are in counterclockwise order. The coordinates are real numbers; the implementation uses integers or exact fractions.

A face is *front facing* when $n \cdot (E - v_0) > 0$, that is, when $E$ is strictly on the outer side of the plane of the face. The output is the list of the front-facing faces, in input order.

The guarantee needs two conditions. The faces form a *closed* surface: they bound a solid $S$, each edge is shared by two faces, and each normal points out of $S$. The viewer $E$ is outside $S$ and not on the surface. Then each point of the surface that $E$ can see lies on a front-facing face. The image is a point sample at each pixel center, as on the page about [hidden surface removal](/hidden-surface-removal/), so the claim is that the nearest hit of each ray from $E$ does not change.

## The algorithm

```pseudo id=main
BACK-FACE-CULL(f[0 .. F − 1], E)
L1  kept ← an empty list
L2  for k ← 0 to F − 1 do let (v0, v1, v2) ← f[k]
L3      n ← (v1 − v0) × (v2 − v0)                         ▷ the outward normal
L4      if n · (E − v0) > 0 then append k to kept          ▷ E is on the outer side
L5  return kept
```

Line L3 computes the normal by a [cross product](/cross-product/). In practice the normal is stored with the mesh and line L3 is a load. Line L4 is one [dot product](/dot-product/) and a sign test. A face with $n \cdot (E - v_0) = 0$ is seen edge on, so it covers no area of the image, and the test drops it. Each face is tested alone, so the faces can come one at a time.

The vector $E - v_0$ is important. It points from the face to the eye. Under a perspective view this vector changes from face to face. A test with one fixed view direction is correct only for an orthographic view.

## Example

Take the cube $[0, 2]^3$ as 12 triangles, two for each side, with outward normals. The center is $(1, 1, 1)$. Let the eye be $E = (5, 1, 4)$. For a side, take the unit outward normal $u$ and a vertex $v_0$ on the side. The implementation uses $n = 4u$, because each triangle has two legs of length 2; the sign is the same.

| side | unit normal $u$ | $u \cdot (E - v_0)$ | front facing |
|---|---|---|---|
| $x = 0$ | $(-1, 0, 0)$ | $-5$ | no |
| $x = 2$ | $(1, 0, 0)$ | $3$ | yes |
| $y = 0$ | $(0, -1, 0)$ | $-1$ | no |
| $y = 2$ | $(0, 1, 0)$ | $-1$ | no |
| $z = 0$ | $(0, 0, -1)$ | $-4$ | no |
| $z = 2$ | $(0, 0, 1)$ | $2$ | yes |

With the sides in the order of the table, the kept triangles are 2, 3, 10 and 11, so 4 of the 12 faces remain. From $E = (5, 1, 1)$, which is between the planes $z = 0$ and $z = 2$, only the side $x = 2$ remains. From $E = (5, 2, 1)$ the side $y = 2$ gives $u \cdot (E - v_0) = 0$; the eye is in its plane, so the side is seen edge on and the test drops it. From $E = (4, 5, 6)$ three sides face the viewer: $x = 2$, $y = 2$ and $z = 2$. The tests check these four cases.

For a closed mesh that is not convex the result is different. Take two tetrahedra, one behind the other. The near one hides parts of the far one, but the faces of the far one that face the eye are still kept. Back-face culling does not remove them; the depth test must do that.

## Correctness

The main claim is that, for a closed surface and an eye outside it, the nearest point that a ray from $E$ meets on the kept faces is the nearest point that the ray meets on all faces. The proof has two steps.

First, take a visible point $X$ in the interior of a face $f$, with $E$ not in the plane of $f$. The open segment from $E$ to $X$ meets no point of the surface, and $E$ is outside $S$, so the points of that segment are all outside $S$. Near $X$, the solid $S$ is on the inner side of the plane of $f$. So a point just before $X$ on the segment is on the outer side, and therefore $E$ is on the outer side too: line L4 keeps $f$.

Second, the first hit $X$ of an arbitrary ray can be at an edge or a vertex. Points of face interiors near $X$ give rays whose first hits are in face interiors and are visible, so they are on kept faces by the first step. These first hits tend to $X$, and the union of the kept faces is a closed set, so $X$ is on a kept face.

For a convex solid the test is exact: each point of a front-facing face is visible. The full proofs are below.

## Complexity

Each face costs one cross product, one dot product and one comparison, so the time is $\Theta(F)$ in each case. The extra space is $\Theta(1)$, plus the output list. With stored normals the cost per face is one dot product.

The saving is in the later stages. For a closed surface $\sum_k A_k u_k = 0$, where $A_k$ is the area and $u_k$ the unit outward normal of face $k$. So under an orthographic view the front-facing faces and the back-facing faces have the same total projected area, and for a mesh with many small faces about half of the faces are back facing. The test removes them before they are clipped, rasterized and depth tested.

## Properties

- **Conservative.** For a closed surface and an eye outside it, no visible face is dropped. See the [proof](#correctness).
- **Not exact in general.** For a solid that is not convex, or for more than one solid, a kept face can be hidden. The method is a speed step, and the renderer still needs a [z-buffer](/z-buffer/) or a priority order such as the [painter's algorithm](/painters-algorithm/).
- **Exact for one convex solid.** For a single convex solid and an eye outside it, the kept faces are exactly the faces that the eye can see. This is why it is enough for the hidden line removal of a single convex object.
- **Local.** Each face is tested alone, in $O(1)$ time, with no data about the other faces. So the test fits in a pipeline and on a GPU.
- **Exact arithmetic.** With integer or fraction coordinates the sign of line L4 is exact. With floating point the sign can be wrong only when the face is nearly edge on.

## Variants and improvements

- **Screen-space test.** GPUs do the test after the projection, by the sign of the area of the projected triangle, which is an [orientation test](/orientation-test/). For a triangle in front of the eye, $\det(v_0 - E, v_1 - E, v_2 - E) = -\,n \cdot (E - v_0)$, and the projection keeps the sign of this determinant. So the screen test and line L4 agree. A triangle that crosses the plane of the eye must be clipped first, or tested with the 3D determinant.
- **Orthographic view.** With a view direction $d$ from the scene to the viewer that is the same for each face, the test becomes $n \cdot d > 0$.
- **Front-face culling.** Drop the faces that face the viewer and keep the others. Renderers use this for some shadow techniques and to draw the inside of a closed object, for example a sky box seen from inside.
- **Two-sided faces.** For an open surface, such as a leaf or a sheet of paper, turn culling off and shade the back side with the reversed normal.
- **Clustered and hierarchical culling.** Group faces whose normals lie in a narrow cone. If the whole cone faces away from each point of the group's bounding volume, drop the group with one test.
- **Silhouette edges.** An edge between a kept face and a dropped face is a [silhouette edge](/silhouette-edge/). The [shadow volume algorithm](/shadow-volume-algorithm/) uses the same test from the light position to find the edges that bound the shadow.

## When to use it

Use back-face culling for closed, consistently oriented meshes when the camera stays outside them, which is the common case for solid objects in games and CAD. It costs almost nothing and removes about half of the faces. Use it together with [frustum culling](/frustum-culling/), which removes objects outside the view, and [occlusion culling](/occlusion-culling/), which removes objects behind others. Turn it off for open surfaces, for two-sided materials, and when the camera can enter a mesh.

## Pitfalls

- **A fixed view direction under perspective.** The test $n \cdot (0, 0, 1) > 0$ is not the same as line L4 in a perspective view. A face at $x = 0$ with normal $(1, 0, 0)$, seen from $E = (3, 1, 2)$, faces the viewer, but its normal has $n_z = 0$, so the fixed direction test drops it. Use $E - v_0$, or test after the projection.
- **Inconsistent winding.** If some triangles are listed clockwise, their normals point in, and the test drops visible faces. Make the orientation consistent before culling.
- **Mirror transforms.** A model matrix with a negative determinant, such as a scale by $-1$, reverses the winding of each projected triangle. Change the culling convention for such objects.
- **Open surfaces.** A single plane, such as a ground quad or a leaf, is visible from both sides. Back-face culling removes it from below. The tests show a triangle that is visible from $E = (1, 1, -9)$ but dropped.
- **Eye inside the solid.** If the camera goes into a closed mesh, each face that the eye sees has its inner side toward the eye, so the test drops all of them and the mesh disappears.
- **Vertex normals.** The normals used for smooth shading are not the face normals. The test must use the face normal, or the screen-space winding.
- **Thinking that the result is the visible set.** For a mesh that is not convex, kept faces can be hidden. Do not skip the depth test.

## Implementations

## History

Lawrence Roberts, in his 1963 thesis on the perception of 3D solids, drew convex objects with hidden lines removed, and the first step of his method was to remove the faces of each convex solid that point away from the viewer. Sutherland, Sproull and Schumacker in 1974 described the removal of back faces as a cheap first step of several of the hidden surface methods that they compared. The test became part of each polygon pipeline, and graphics hardware does it as a fixed stage after the projection, by the sign of the area of the projected triangle.

## References
