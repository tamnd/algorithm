---
tag: KRS7SP
kind: problem
slug: triangle-rasterization
name: Triangle rasterization
aliases:
- triangle scan conversion
area: graphics-and-signals/rasterization
level: core
summary: Given a triangle in screen coordinates, find the pixel centers it covers, with a tie rule for shared edges, and the interpolated vertex values there.
prereqs: [pixel, edge-function]
see_also: [polygon-scan-conversion, pineda-rasterization, top-left-fill-rule, scanline-polygon-fill, tiled-rasterization, conservative-rasterization, graphics-pipeline, line-rasterization]
sources:
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 23, Section 23.1, Rasterization (coverage by edge functions, fixed point vertices, tie rules and triangle setup)
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 8, Section 8.1.2, Triangle Rasterization (coverage of pixel centers, interpolation of vertex colors by barycentric coordinates, pixels on shared edges)
  - paper: doi:10.1145/378456.378457
    title: Juan Pineda, A parallel algorithm for polygon rasterization, Computer Graphics (SIGGRAPH 88 Proceedings) 22(4), 17 to 20, 1988
    locator: the whole paper
  - url: https://learn.microsoft.com/en-us/windows/win32/direct3d11/d3d10-graphics-programming-guide-rasterizer-stage-rules
    title: Microsoft, Rasterization Rules (Direct3D 11), Direct3D 11 Graphics documentation
    locator: Triangle Rasterization Rules (without multisampling) and Multisample Anti-Aliasing Rasterization Rules
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 3, the scan conversion and filling of polygons (spans, edge coherence and the rules for pixels on edges)
---

Triangle rasterization is the problem of finding the [pixels](/pixel/) whose sample points a triangle covers, given the triangle in screen coordinates, and of giving each covered pixel the values of the vertex attributes interpolated at its sample point. A pixel is a point sample, so a pixel is covered when its center is in the triangle, with a tie rule for centers on edges. The rule must make a mesh of triangles cover each center exactly once. It is the core step of the [graphics pipeline](/graphics-pipeline/) and the special case of [polygon scan conversion](/polygon-scan-conversion/) that GPUs implement.

## In plain words

A picture on the screen is a grid of dots. A 3D model is made of many small triangles. After the model is placed and projected, each triangle lands on the grid, and the job is to say which dots it covers. A dot counts when its center is in the triangle.

Two triangles of a model often share an edge. If a dot center is exactly on that edge, a fixed rule must give the dot to one of the two triangles. Otherwise the dot is drawn twice, or a crack of missing dots shows along the edge.

Each corner of the triangle also carries values, such as a color, a depth or a texture position. For each covered dot, the values are mixed by how near the dot is to each corner.

## Definition

**Screen and samples.** The screen has $W \times H$ pixels. Pixel $(i, j)$, for $0 \le i < W$ and $0 \le j < H$, has the sample point $c_{ij} = (i + \tfrac12, j + \tfrac12)$, as in the Direct3D 10 and OpenGL rules, with $x$ to the right and $y$ down.

**Input.** A triangle $T = (v_0, v_1, v_2)$ with vertices in screen coordinates, snapped to a grid of $s$ subpixel steps per pixel, so that $s\,v_k \in \mathbb{Z}^2$. Each vertex can carry attribute values $a_k \in \mathbb{R}^m$, and, for a perspective view, the clip coordinate $w_k > 0$.

**Coverage.** Let $E_0, E_1, E_2$ be the [edge functions](/edge-function/) of $T$, oriented so that they are positive inside, and let $S$ be the signed area. If $S = 0$ the coverage is empty. Otherwise

$$\mathrm{Cov}(T) = \{(i, j) : c_{ij} \text{ is covered by } T \text{ under the top-left rule}\},$$

where $p$ is covered when each $E_k(p) > 0$, or $E_k(p) = 0$ and edge $k$ is a top or left edge ([top-left fill rule](/top-left-fill-rule/)).

**Attributes.** For $(i, j) \in \mathrm{Cov}(T)$, let $\lambda_k = E_k(c_{ij}) / (2S)$ be the screen barycentric coordinates. The screen-affine value is $\sum_k \lambda_k a_k$. The perspective-correct value is

$$a(c_{ij}) = \frac{\sum_k \lambda_k a_k / w_k}{\sum_k \lambda_k / w_k}$$

([perspective-correct interpolation](/perspective-correct-interpolation/)).

**Requirement.** For triangles $T_1, \ldots, T_n$ with pairwise disjoint interiors, each center in the interior of their union is in exactly one $\mathrm{Cov}(T_i)$, and each other center is in at most one. The top-left rule meets this requirement with exact arithmetic; this is the theorem on the [top-left fill rule](/top-left-fill-rule/) page.

**Cost model.** The [word RAM](/word-ram/) with integer subpixel coordinates. For one triangle, $w \times h$ is the size of its pixel bounding box clipped to the screen, and $c = |\mathrm{Cov}(T)|$ is the size of the output. A frame has $n$ triangles.

## Variants

- **Coverage only.** The output is $\mathrm{Cov}(T)$, as for a depth pass or a stencil pass.
- **Coverage with attributes.** The output also has the interpolated values, screen-affine for 2D work and perspective-correct for 3D views.
- **Multisampled coverage.** Each pixel has $k$ sample positions, and the output is a $k$-bit coverage mask per pixel, with the same tie rule at each sample ([multisample antialiasing](/multisample-antialiasing/)).
- **Conservative coverage.** Output each pixel whose square the triangle touches, or each pixel whose square is fully inside ([conservative rasterization](/conservative-rasterization/)). This variant treats a pixel as a square on purpose.
- **Area coverage.** Output the exact area of $T$ in each pixel square, for analytic [antialiasing](/antialiasing/). This is a different problem with a different output.
- **Many triangles.** Rasterize a list of $n$ triangles into one image, with a depth test per pixel ([z-buffer](/z-buffer/)) and with triangles sorted to screen tiles first ([tiled rasterization](/tiled-rasterization/)).
- **Triangles that cross the eye plane.** In a 3D view, a triangle with some $w_k \le 0$ has no finite screen image. It is clipped in homogeneous coordinates first ([graphics pipeline](/graphics-pipeline/)), or rasterized with homogeneous edge functions.

## Examples

Coordinates here are in pixel units.

- **A right triangle.** $T = (0.5, 0.5), (4.5, 0.5), (0.5, 4.5)$ covers the 10 pixels with $i + j \le 3$. The centers on the diagonal $x + y = 5$, those of pixels $(3, 1)$, $(2, 2)$ and $(1, 3)$, are on a right edge and are not covered. The triangle $(4.5, 0.5), (4.5, 4.5), (0.5, 4.5)$ covers them, so the pair covers the 16 pixels of the $4 \times 4$ block once each. The table of the computation is on the [Pineda rasterization](/pineda-rasterization/) page.
- **Interpolated color.** Give the first triangle the colors red $(1, 0, 0)$, green $(0, 1, 0)$ and blue $(0, 0, 1)$ at its three vertices. The center $(1.5, 1.5)$ of pixel $(1, 1)$ has the edge function values $(32, 16, 16)$ in half-pixel units, with $2S = 64$, so $\lambda = (\tfrac12, \tfrac14, \tfrac14)$ and the color is $(0.5, 0.25, 0.25)$.
- **A small triangle with one pixel.** $T = (2.375, 2.375), (2.75, 2.375), (2.375, 2.75)$, on a grid of $s = 8$ steps, has area $0.0703125$ but covers the center $(2.5, 2.5)$, because $2.5 + 2.5 < 5.125$. It covers pixel $(2, 2)$ only.
- **A thin triangle with no pixel.** $T = (0, 0), (4, 0), (4, 0.25)$ has area $0.5$ but covers no center, because each center has $y \ge 0.5$. A moving thin triangle therefore flickers: it covers centers in some frames and none in others.
- **A degenerate triangle.** $T = (1, 1), (2, 2), (3, 3)$ has $S = 0$ and covers no pixel, even though the center $(1.5, 1.5)$ is on it.

## Known algorithms

- [Pineda rasterization](/pineda-rasterization/): evaluate the three edge functions at each center of the bounding box with integer steps. $\Theta(wh)$ time in each case, $\Theta(1)$ extra space, exact.
- Edge walking, as in [scanline polygon fill](/scanline-polygon-fill/) with an [active edge table](/active-edge-table/): find the span of each row from the left and right edges and visit only the span. $O(h + c)$ time per triangle when the span ends are found with exact integer steps. The [Gouraud shading](/gouraud-shading/) page gives this form with interpolation.
- [Tiled rasterization](/tiled-rasterization/): test whole tiles of $t \times t$ pixels against each edge first, and run the pixel loop only in tiles that an edge cuts. The time is $O(wh/t^2 + t(w + h) + c)$, derived on that page.
- [Conservative rasterization](/conservative-rasterization/): the same loop as Pineda's with moved edge constants, for the conservative variant.

## Bounds

Any algorithm that lists $\mathrm{Cov}(T)$ needs $\Omega(c)$ time to write the output and $\Omega(1)$ time to read the triangle, so $\Omega(1 + c)$ per triangle in the word RAM. Edge walking with exact span ends meets this up to the $O(h)$ term for the rows. Pineda's loop is $\Theta(wh)$, which is within a factor of about 2 of $c$ for a well-shaped triangle, since a triangle has at most half the area of its bounding box, but which can be $\Theta(wh)$ when $c = O(w + h)$ or $c = 0$. A brute force test of each center of the screen is $\Theta(WH)$ per triangle.

The exact decisions need integers of $2q + 2$ binary digits for subpixel coordinates of $q$ digits (property 7 of the [edge function](/edge-function/)). Float evaluation needs a robust predicate, such as an exact [orientation test](/orientation-test/), to meet the requirement.

## Reductions

- **From convex polygons.** A convex polygon with $n$ vertices splits into $n - 2$ triangles of a fan. With the top-left rule, the fan covers each center of the polygon's interior once, so scan conversion of a convex polygon reduces to $n - 2$ triangle rasterizations.
- **From simple polygons.** A simple polygon splits into $n - 2$ triangles by [polygon triangulation](/polygon-triangulation/), for example by [ear clipping](/ear-clipping/) in $O(n^2)$ time. Self-intersecting polygons with the [even-odd](/even-odd-fill-rule/) or [nonzero](/nonzero-winding-rule/) rule need [polygon scan conversion](/polygon-scan-conversion/) or the stencil method.
- **To point location.** Triangle rasterization is the [point-in-polygon](/point-in-polygon/) test for a triangle at each center of the screen, with the tie rule for the boundary. The bounding box and the incremental steps make it faster than $WH$ independent tests.

## Applications

- The rasterization stage of the [graphics pipeline](/graphics-pipeline/), with depth by the [z-buffer](/z-buffer/) and color by [Gouraud](/gouraud-shading/) or [Phong shading](/phong-shading/) and [texture mapping](/texture-mapping/).
- [Shadow mapping](/shadow-mapping/), which rasterizes the scene from the light into a depth image.
- Visibility tests such as the [hierarchical z-buffer](/hierarchical-z-buffer/), which rasterize bounding volumes and test depth.
- Voxelization and collision tests with [conservative rasterization](/conservative-rasterization/).

## References
