---
tag: 43E96Q
kind: algorithm
slug: gouraud-shading
name: Gouraud shading
aliases:
- intensity interpolation shading
area: graphics-and-signals/rasterization
level: intro
summary: Light each vertex with an averaged normal, then interpolate the intensities linearly along the edges and along each scanline of the polygon.
solves: [polygon-shading]
model: real-ram
complexity:
  vars: {h: the number of pixel rows of the triangle, c: the number of covered pixels}
  time: {worst: Θ(h + c), average: Θ(h + c), best: Θ(h + c)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1971
  people: [Henri Gouraud]
  note: Gouraud published continuous shading of curved surfaces, with vertex normals averaged from the adjacent faces and intensities interpolated along scanlines.
prereqs: [polygon-shading, lambertian-reflectance, triangle-rasterization]
see_also: [phong-shading, scanline-polygon-fill, top-left-fill-rule, perspective-correct-interpolation, polygon-mesh, active-edge-table, pineda-rasterization, z-buffer]
sources:
  - paper: doi:10.1109/T-C.1971.223313
    title: Henri Gouraud, Continuous shading of curved surfaces, IEEE Transactions on Computers C-20(6), 623 to 629, 1971
    locator: the whole paper (vertex normals from the adjacent polygons, intensities at the vertices, interpolation along the scan line)
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 16, Section 16.2.4, Gouraud Shading (also called intensity interpolation shading or color interpolation shading; Mach bands and the dependence on orientation)
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 8, Section 8.1.2, Triangle Rasterization (interpolation of vertex colors over a triangle)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 5, Shading Basics (evaluation of shading per vertex and per pixel)
  - paper: doi:10.1145/360825.360839
    title: Bui Tuong Phong, Illumination for computer generated pictures, Communications of the ACM 18(6), 311 to 317, 1975
    locator: the whole paper (the shading by interpolated normals that followed Gouraud's method)
---

Gouraud shading solves [polygon shading](/polygon-shading/) by lighting only the vertices: each vertex gets a normal, the average of the normals of the faces around it, and an intensity from a lighting model such as [Lambertian reflectance](/lambertian-reflectance/). The rasterizer then interpolates the intensities linearly, first along the edges and then along each scanline. On a triangle the result is the affine function of the screen position that has the vertex values at the vertices, so adjacent triangles agree on their shared edge and the [polygon mesh](/polygon-mesh/) looks smooth. The cost is one lighting evaluation per vertex and one addition per pixel, but a highlight inside a triangle is lost, which [Phong shading](/phong-shading/) fixes.

## In plain words

A curved object is drawn as many flat pieces. If each piece has one color, the eye sees the edges between the pieces.

Gouraud's idea is to light only the corners. Each corner gets a direction that points away from the surface, taken as the mean of the directions of the pieces that meet there. From this direction and the light, the corner gets a brightness. Then, inside each piece, the brightness changes evenly from corner to corner: first down the sides, and then across each row of dots, from the left side to the right side.

Two pieces that share a side get the same brightness all along that side, so the steps between pieces go away. The method is cheap, because the light is computed only at the corners.

## The problem

The input is a triangle mesh with vertex positions, a light, and a lighting model. The output is an intensity for each pixel that a triangle covers, with values that vary smoothly over the mesh and are continuous across shared edges. This is [polygon shading](/polygon-shading/), which also gives the other methods.

Here a triangle is already in screen coordinates. Its vertices $v_0, v_1, v_2$ are integers in units of $1/s$ pixel, with $y$ down, and pixel $(i, j)$ is the point sample at its center $(i + \tfrac12, j + \tfrac12)$, as in the Direct3D 10 and OpenGL rules. A pixel is a point, not a little square.

## The algorithm

Before the scan, two steps run once per vertex of the mesh.

1. **Vertex normals.** The normal $n_v$ of vertex $v$ is $\sum_f N_f$ normalized, where $f$ runs over the faces at $v$ and $N_f$ is the cross product of two edges of $f$. The length of $N_f$ is twice the face area, so larger faces weigh more. A vertex on a sharp crease gets one normal per side.
2. **Vertex intensities.** $I_v = k_a + k_d \max(0, n_v \cdot l)$ for a unit light direction $l$, an ambient part $k_a$ and a diffuse part $k_d$. Any lighting model can be used here, also one with a specular term.

Then each triangle is scanned. The rows are half-open, from $y_{\min}$ included to $y_{\max}$ excluded, and each span is half-open, from $x_l$ included to $x_r$ excluded. A horizontal edge is never active.

```pseudo id=main
GOURAUD-TRIANGLE(v0, v1, v2, I0, I1, I2)
L1  for each row j whose center y_c has y_min ≤ y_c < y_max do
L2      for each of the two edges (a, b), ordered so that y_a < y_b, with y_a ≤ y_c < y_b do
L3          t ← (y_c − y_a)/(y_b − y_a);  x ← x_a + t(x_b − x_a);  I ← I_a + t(I_b − I_a)
L4      (x_l, I_l), (x_r, I_r) ← the two ends found by line L3, with x_l ≤ x_r
L5      if x_l = x_r then continue with the next row
L6      ΔI ← (I_r − I_l)/(x_r − x_l)                ▷ the change per unit of x on this row
L7      i ← the first pixel whose center x_c has x_c ≥ x_l
L8      I ← I_l + (x_c − x_l)·ΔI
L9      while x_c < x_r do
L10         write intensity I to pixel (i, j)
L11         I ← I + ΔI·(one pixel width);  i ← i + 1;  x_c ← x_c + one pixel width
```

Line L1 runs over the rows of the triangle. A row with $y_{\min} \le y_c < y_{\max}$ meets exactly two edges in the half-open sense of line L2, one on the left and one on the right. Line L3 finds where the row crosses each edge, and the intensity there by linear interpolation along the edge. Line L5 skips a row that touches only a vertex. Lines L6 to L11 walk the span: the intensity changes by a fixed amount per pixel, so each pixel costs one addition. In a hardware or incremental version, $x$, $I$ and their steps per row are also updated by additions from row to row.

The half-open rows and spans cover the same pixel centers as the [top-left fill rule](/top-left-fill-rule/): the proof shows that both rules sample at a point a tiny step right and a much smaller step below the center. So a mesh is shaded with each pixel once, as with [Pineda rasterization](/pineda-rasterization/).

## Example

**Lighting.** Let the three vertex normals be $n_0 = (0, 0, 1)$, $n_1 = (0.6, 0, 0.8)$ and $n_2 = (0, 0.6, 0.8)$, the light $l = (0.6, 0, 0.8)$, $k_a = 0.1$ and $k_d = 0.9$. The dot products are $0.8$, $1.0$ and $0.64$, so the intensities are $I_0 = 0.82$, $I_1 = 1.0$ and $I_2 = 0.676$.

**Scan.** In pixel units, put the vertices at $v_0 = (0.5, 0.5)$, $v_1 = (4.5, 0.5)$ and $v_2 = (0.5, 4.5)$ on a $5 \times 5$ screen. The rows are $y_c = 0.5, 1.5, 2.5, 3.5$; the center $y_c = 4.5$ is $y_{\max}$ and is excluded. The left edge is $v_0 v_2$ at $x = 0.5$, and the right edge is $v_1 v_2$ at $x = 5 - y_c$. The edge $v_0 v_1$ is horizontal and is never active.

| row $j$ | $y_c$ | $x_l$ | $x_r$ | $I_l$ | $I_r$ | $\Delta I$ per pixel | pixels and intensities |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.5 | 0.5 | 4.5 | 0.820 | 1.000 | 0.045 | 0: 0.820, 1: 0.865, 2: 0.910, 3: 0.955 |
| 1 | 1.5 | 0.5 | 3.5 | 0.784 | 0.919 | 0.045 | 0: 0.784, 1: 0.829, 2: 0.874 |
| 2 | 2.5 | 0.5 | 2.5 | 0.748 | 0.838 | 0.045 | 0: 0.748, 1: 0.793 |
| 3 | 3.5 | 0.5 | 1.5 | 0.712 | 0.757 | 0.045 | 0: 0.712 |

The pixels are the 10 pixels with $i + j \le 3$, the same set as the top-left rule gives. The centers at $x = x_r$, such as $(4.5, 0.5)$ and $(3.5, 1.5)$, are on the right edge and are left to the neighbor triangle. $\Delta I$ is the same on each row, because the interpolated intensity is one affine function of $(x, y)$. At pixel $(1, 1)$ it is $0.829 = \tfrac12 I_0 + \tfrac14 I_1 + \tfrac14 I_2$, the barycentric combination at $(1.5, 1.5)$.

## Correctness

**Claim.** For a triangle with nonzero area, GOURAUD-TRIANGLE writes exactly the pixels whose centers the triangle covers under the top-left rule, and it writes to each such pixel the value $\lambda_0 I_0 + \lambda_1 I_1 + \lambda_2 I_2$, where $\lambda_k$ are the screen barycentric coordinates of the center.

The key facts are two. First, the half-open row and span tests accept a center $p$ exactly when the point $p + (\varepsilon, \varepsilon^2)$, for all small $\varepsilon > 0$, is in the interior of the triangle; the top-left rule has the same description, so the two rules agree. Second, the affine function $f$ with $f(v_k) = I_k$ is linear along each edge and along each row, so lines L3 and L8 compute $f$ at the span ends and at the first center, and each step of line L11 keeps the invariant "$I = f(x_c, y_c)$". The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [real RAM](/real-ram/) for the intensities, with exact rational arithmetic for the coverage decisions: the span ends of line L3 are rationals with integer numerators and denominators, so each test of lines L5, L7 and L9 is exact.

- **Per triangle.** Line L1 visits the $h$ rows of the triangle, each with $O(1)$ work in lines L2 to L8. Lines L9 to L11 run once per covered pixel, with $O(1)$ work. So the time is $\Theta(h + c)$ in each case, and the extra space is $\Theta(1)$.
- **Per mesh.** The vertex normals take $\Theta(V + F)$ time for $V$ vertices and $F$ faces, because each face adds its normal to 3 vertices. The lighting takes one evaluation of the model per vertex, $\Theta(V)$. Phong shading evaluates the model once per covered pixel instead, which is far more when triangles cover many pixels.
- **Arithmetic per pixel.** One addition for the intensity, or three for a color, and one compare.

## Properties

- **Continuous across shared edges.** On an edge, the interpolated value depends only on the two end vertices, so both triangles of the edge give the same values there. The intensity is continuous over the mesh, but its derivative jumps at the edges.
- **Equal to barycentric interpolation on triangles.** For a triangle, scanline interpolation gives the affine function with the vertex values, so it does not depend on the orientation of the triangle on the screen.
- **Exact with rationals.** With integer vertices and rational intensities, each value is exact.
- **Watertight.** The coverage equals the top-left rule, so a mesh covers each pixel center once.

## Variants and improvements

- **Color.** Interpolate red, green and blue separately, with three additions per pixel. This is color interpolation shading.
- **Specular at the vertices.** Add a specular term to the vertex lighting. Highlights then appear only where a vertex is near the highlight, and they move and flicker as the object turns.
- **Perspective-correct Gouraud.** In a 3D view, interpolate $I/w$ and $1/w$ and divide, as in [perspective-correct interpolation](/perspective-correct-interpolation/). Screen-space interpolation is what the original method does, and it is a little wrong under perspective.
- **Phong shading.** Interpolate the normals and light each pixel ([Phong shading](/phong-shading/)). It keeps highlights inside triangles, at the cost of one lighting evaluation per pixel.
- **Flat shading.** One intensity per face, from the face normal. It is cheaper and shows the faces.

## When to use it

Use Gouraud shading when lighting is expensive and triangles are small, a few pixels each, so that the vertices sample the lighting densely: then it looks almost the same as per-pixel lighting at a fraction of the cost. It is also the right choice for values that are linear by nature, such as baked vertex colors. Use [Phong shading](/phong-shading/) or per-pixel lighting when triangles are large compared with the features of the lighting, such as a sharp specular highlight or a spot light, and when the image must not change with the tessellation.

## Pitfalls

- **Highlights lost or flickering.** A specular highlight whose peak falls inside a triangle, away from its vertices, does not appear, because line L3 only interpolates the vertex values; the [Phong shading](/phong-shading/) page has a numeric case. The fix is to interpolate normals, not intensities, and to light per pixel.
- **Mach bands.** The derivative of the intensity jumps at each edge, and the eye sees bright and dark bands along the edges. More triangles make the bands weaker; per-pixel lighting removes the cause.
- **Interpolation of polygons with more than three vertices.** For a quadrilateral, the scanline values of lines L3 and L8 depend on the rotation of the polygon on the screen, and the image changes as the object turns. Split each polygon into triangles first.
- **Wrong normals at creases.** Averaging the normals of faces that meet at a sharp edge rounds the crease. Give such a vertex one normal per smooth group, which means duplicate vertices.
- **A closed span on the right.** Writing `while x_c ≤ x_r` in line L9 instead of `x_c < x_r`, or including the row $y_c = y_{\max}$ in line L1, draws the centers of a shared edge twice and breaks [alpha blending](/alpha-blending/).
- **Not normalized after averaging.** Using the sum of the face normals in the lighting, without the normalization of step 1, scales $n \cdot l$ by the length of the sum, and vertices with many faces look too bright.

## Implementations

## History

Henri Gouraud described the method in 1971, in "Continuous shading of curved surfaces". He approximated a curved surface by polygons, computed a normal at each vertex from the polygons around it, computed the intensity at the vertices, and interpolated the intensity along each scan line. Foley, van Dam, Feiner and Hughes call it intensity interpolation shading or color interpolation shading. Phong (1975) kept the scanline structure but interpolated normals instead of intensities.

## References
