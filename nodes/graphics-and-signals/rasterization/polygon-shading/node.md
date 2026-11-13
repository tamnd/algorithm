---
tag: C9GW73
kind: problem
slug: polygon-shading
name: Polygon shading
aliases:
- smooth shading
- intensity interpolation
area: graphics-and-signals/rasterization
level: intro
summary: Given a polygon mesh that stands for a curved surface, a light and a viewer, give each covered pixel an intensity that varies smoothly over the mesh and hides the facets.
prereqs: [graphics-pipeline, polygon-mesh]
see_also: [gouraud-shading, phong-shading, triangle-rasterization, lambertian-reflectance, brdf, perspective-correct-interpolation, texture-mapping, ear-clipping]
sources:
  - paper: doi:10.1109/T-C.1971.223313
    title: Henri Gouraud, Continuous shading of curved surfaces, IEEE Transactions on Computers C-20(6), 623 to 629, 1971
    locator: the whole paper (the problem of shading a polygon approximation of a curved surface without visible facets)
  - paper: doi:10.1145/360825.360839
    title: Bui Tuong Phong, Illumination for computer generated pictures, Communications of the ACM 18(6), 311 to 317, 1975
    locator: the whole paper (normal interpolation, and why interpolated vertex intensities miss highlights)
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 16, Section 16.2, Shading Models for Polygons (constant shading, Gouraud shading, Phong shading, and the problems with interpolated shading)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 5, Shading Basics (per-vertex and per-pixel evaluation of shading, interpolation of normals)
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 8, Section 8.1.2, Triangle Rasterization (interpolation of vertex values by barycentric coordinates)
---

Polygon shading is the problem of giving each pixel that a [polygon mesh](/polygon-mesh/) covers an intensity, or a color, so that the mesh looks like the smooth surface it stands for. The input has the mesh in screen coordinates, data at the vertices (normals, colors or other values), a light, a viewer and a lighting model. The output is one value per covered pixel, with values that agree on the edges shared by two polygons, so that the eye does not see the facets. It is the step after [triangle rasterization](/triangle-rasterization/) in the [graphics pipeline](/graphics-pipeline/). The classic solutions are flat shading, [Gouraud shading](/gouraud-shading/) and [Phong shading](/phong-shading/), which differ in what they interpolate and in how often they evaluate the lighting.

## In plain words

A round object, such as a ball, is drawn as many small flat pieces. If each piece gets one color, the picture shows the pieces, and the ball looks cut from gems.

The problem is to color the dots inside each piece so that the colors change smoothly from piece to piece, and the ball looks round again. The only help is what each corner knows: which way the true surface faces there, or a color.

There are two main answers. One computes the light at the corners and blends the brightness across the piece. The other blends the facing direction and computes the light at each dot. The first is cheaper. The second shows a shiny spot even when it falls in the middle of a piece.

## Definition

**Input.** A polygon mesh with vertex positions $x_v$ and, at each vertex, a unit normal $n_v$ or a value $a_v \in \mathbb{R}^m$ (a color, for example). Each face is in screen coordinates and covers the pixel set $\mathrm{Cov}(f)$ of [triangle rasterization](/triangle-rasterization/), under the [top-left fill rule](/top-left-fill-rule/). A lighting model SHADE maps a unit normal, a light and a viewer to an intensity, such as the [Lambertian](/lambertian-reflectance/) model or a [BRDF](/brdf/).

**Output.** A value $I(i, j)$ for each pixel $(i, j)$ in the coverage of some face. Pixel $(i, j)$ is the point sample at its center $(i + \tfrac12, j + \tfrac12)$, as in the Direct3D 10 and OpenGL rules; a pixel is a point, not a little square.

**Requirements.** For a face $f$ and a covered center $p$, let $I_f(p)$ be the value from face $f$.

1. **Agreement at the vertices.** As $p$ goes to a vertex $v$ of $f$, $I_f(p)$ goes to the value of $v$: $\mathrm{SHADE}(n_v)$, or $a_v$.
2. **Continuity across edges.** If faces $f$ and $g$ share an edge, then $I_f$ and $I_g$, extended to the edge, are equal on it. So the values form one continuous function over the mesh.
3. **Independence of the screen orientation.** Turning the mesh in the image plane turns the image and does not change the values at the surface points.

The ideal value at a covered center is $\mathrm{SHADE}(N(p))$, where $N(p)$ is the normal of the true surface at the point seen through $p$. The mesh does not know the true surface, so each method approximates $N$, or approximates $\mathrm{SHADE} \circ N$ directly, from the vertex data.

**Cost model.** The [real RAM](/real-ram/) for the values, with exact integer coverage. For a mesh, $V$ is the number of vertices, $F$ the number of faces, and $C$ the number of covered pixels over all faces. One evaluation of SHADE costs $O(1)$ but is the expensive step.

## Variants

- **Flat shading.** One value per face, from the face normal. It violates requirement 2 and shows the facets, but it is the right answer for objects that are faceted, such as a cube.
- **Interpolation of vertex values.** The vertex values are given, such as baked colors or a scalar field from a simulation, and no lighting is evaluated. The barycentric interpolant on triangles meets all three requirements.
- **Interpolation of normals.** The vertex normals are given, and the lighting is evaluated per pixel from an interpolated normal.
- **Perspective-correct values.** In a 3D view, interpolate in the plane of the face, not in screen space, with [perspective-correct interpolation](/perspective-correct-interpolation/). Screen-space interpolation of the original methods depends a little on the view.
- **Polygons with more than three vertices.** Scanline interpolation of a quadrilateral violates requirement 3; see the examples.
- **Textured values.** The value comes from an image through interpolated texture coordinates ([texture mapping](/texture-mapping/)).

## Examples

- **A lost highlight.** The [Phong shading](/phong-shading/) page gives a triangle whose three vertices all have the intensity $0.500$ but whose interpolated normal points at the light near pixel $(2, 2)$. Interpolating the intensities gives $0.500$ at each of its 28 pixels; interpolating the normals gives a highlight of $0.934$ there.
- **A shaded triangle.** The [Gouraud shading](/gouraud-shading/) page lights three vertices with intensities $0.82$, $1.0$ and $0.676$, and interpolates them over 10 pixels, with a step of $0.045$ per pixel on each row.
- **A quadrilateral that depends on the rotation.** Give the unit square the values $1$ at $(0, 0)$, $0$ at $(1, 0)$, $1$ at $(1, 1)$ and $0$ at $(0, 1)$. Scanline interpolation at the center row meets the left edge at $\tfrac12$ and the right edge at $\tfrac12$, so the center gets $\tfrac12$. Turn the square by $45°$ so that the diagonal from $(0, 0)$ to $(1, 1)$ is horizontal: the center row now passes through these two vertices, and the center gets $1$. Turn it by $-45°$ instead, and the center row passes through the other two vertices, so the center gets $0$. Split into two triangles, the center gets $1$ or $0$ depending on the diagonal, but no longer on the rotation.
- **Flat shading of a cube.** Each face has one normal and one value, and the six faces should look flat. Smooth shading with averaged vertex normals would round the corners; a vertex on a crease needs one normal per face.

## Known algorithms

- **Flat shading.** One SHADE per face, then a constant fill: $\Theta(F + C)$ time.
- [Gouraud shading](/gouraud-shading/) (1971): average the face normals at each vertex, evaluate SHADE at the vertices, and interpolate the intensities along the edges and spans. $\Theta(V + F)$ for the normals, $V$ evaluations of SHADE, and $\Theta(h + c)$ time per triangle with $h$ rows and $c$ pixels.
- [Phong shading](/phong-shading/) (1975): interpolate the normals, normalize them, and evaluate SHADE at each pixel. $\Theta(h + c)$ time per triangle, with $C$ evaluations of SHADE in total.
- **Fast Phong shading** (Bishop and Weimer, 1986): a second order Taylor expansion of the per-pixel shading, so that each pixel costs a few additions. It is on the [Phong shading](/phong-shading/) page.
- **Barycentric interpolation** with the [edge functions](/edge-function/) of [Pineda rasterization](/pineda-rasterization/): the same values as the scanline methods on triangles, computed per pixel without the spans.

## Bounds

Each method reads each face and writes one value per covered pixel, so the time is $\Omega(F + C)$ for a mesh. Gouraud shading meets this bound up to the $O(h)$ term per triangle for its rows, as in [triangle rasterization](/triangle-rasterization/), with $V$ lighting evaluations, and Phong shading in the same way with $C$ of them.

The error of Gouraud shading on an edge follows from the error of linear interpolation. If $f(t)$ is the ideal intensity along an edge of length $L$ and $|f''| \le M$ on it, then the linear interpolant $\ell$ of the two end values has

$$|f(t) - \ell(t)| \le \frac{M}{2}\,t\,(L - t) \le \frac{M L^2}{8} .$$

The proof is the standard one: for a fixed $t$, the function $f - \ell - K\,s(L - s)$, with $K$ chosen so that it is zero at $s = t$, has three zeros, so its second derivative, $f'' + 2K$, has a zero, and $|K| \le M/2$. For a highlight with shininess $\alpha$, the specular term near its peak is $\cos^{\alpha}\theta \approx e^{-\alpha\theta^2/2}$, whose second derivative in $\theta$ is $-\alpha$ at $\theta = 0$. If the angle $\theta$ changes by $\kappa$ per unit length along the edge, then $M \approx \alpha\kappa^2$ and the bound is about $\alpha\kappa^2 L^2/8$. So with fixed triangles the error grows with $\alpha$, and only shorter edges make it small.

## Reductions

- **Polygons to triangles.** A convex polygon with $n$ vertices splits into a fan of $n - 2$ triangles, and a simple polygon into $n - 2$ triangles by [ear clipping](/ear-clipping/). On triangles, scanline interpolation equals barycentric interpolation, which meets requirement 3.
- **To attribute interpolation.** Each method reduces to the interpolation part of [triangle rasterization](/triangle-rasterization/): Gouraud shading interpolates one value (or three for a color), and Phong shading interpolates a vector and then applies a function per pixel.
- **To visibility.** Shading a whole scene needs the visible face at each pixel, which comes from the [z-buffer](/z-buffer/) or another hidden surface method; the shading itself treats one face at a time.

## Applications

- Real-time rendering in the [graphics pipeline](/graphics-pipeline/), where per-pixel lighting in a fragment shader is Phong shading with a physically based lighting model.
- Smooth display of curved surfaces in modelers and CAD, from tessellated meshes.
- Scientific visualization, where a scalar field at the vertices is shown with a color map interpolated over the mesh.
- Terrain rendering from height fields, where the vertex normals come from the heights.

## References
