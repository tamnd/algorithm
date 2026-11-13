---
tag: 5FKK98
kind: concept
slug: graphics-pipeline
name: Graphics pipeline
aliases:
- rendering pipeline
area: graphics-and-signals/rasterization
level: intro
summary: The fixed order of stages that turns triangles into pixels, from the vertex transforms through clipping, the divide by w and rasterization to shading and the frame buffer.
prereqs: [pixel]
see_also: [triangle-rasterization, polygon-window-clipping, viewport-transform, z-buffer, perspective-correct-interpolation, sort-middle-rendering, tiled-rasterization, frame-buffer]
sources:
  - paper: doi:10.1145/965139.807398
    title: James F. Blinn and Martin E. Newell, Clipping using homogeneous coordinates, SIGGRAPH 1978, Computer Graphics 12(3), 245 to 251
    locator: the whole paper (clipping against the view volume in homogeneous coordinates, before the division, and the points behind the eye)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 2, The Graphics Rendering Pipeline (application, geometry processing, rasterization and pixel processing), and Chapter 3, The Graphics Processing Unit
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 7, Viewing (the projection matrices), and Chapter 8, The Graphics Pipeline (rasterization, clipping, and the operations before and after rasterization)
  - paper: doi:10.1145/258694.258723
    title: Marc Olano and Trey Greer, Triangle scan conversion using 2D homogeneous coordinates, Graphics Hardware 1997
    locator: the whole paper (rasterization of triangles without clipping and without the divide)
  - paper: doi:10.1109/38.291528
    title: Steven Molnar, Michael Cox, David Ellsworth and Henry Fuchs, A sorting classification of parallel rendering, IEEE Computer Graphics and Applications 14(4), 23 to 32, 1994
    locator: the whole paper (the pipeline as geometry processing followed by rasterization, and where a parallel renderer sorts)
---

The graphics pipeline is the fixed order of stages that a rasterizing renderer runs to turn a list of triangles into an image. Each vertex is transformed to clip coordinates, each triangle is clipped against the view volume, the vertices are divided by $w$ and mapped to the screen, and [triangle rasterization](/triangle-rasterization/) finds the covered [pixels](/pixel/). Each covered pixel is then shaded, tested against the depth in the [z-buffer](/z-buffer/), and written to the [frame buffer](/frame-buffer/). The order is the point: clipping must come before the divide by $w$, because the divide sends points behind the eye to the wrong side of the screen.

## In plain words

A 3D scene is a list of small triangles in space. The screen is a flat grid of dots. The pipeline is the assembly line between them.

First, each corner is moved so that it is seen from the camera, and the view is squeezed so that what the camera sees fits in a box. Next, the parts of each triangle outside the box are cut off. Only then does the line make the far things small, which is the step that gives depth to the picture. Then the corners are put on the grid, and the line finds the dots that each triangle covers. Each such dot gets a color, and the nearest triangle at each dot wins.

The cutting must come before the step that makes things small. A corner behind the camera would otherwise land on the wrong side of the picture.

## The idea

The stages, in order, for one triangle with vertices $P_0, P_1, P_2$ in the coordinates of its model:

1. **Vertex processing.** Each vertex is multiplied by the model, view and projection matrices to get clip coordinates $(x, y, z, w)$. For a perspective view of a [pinhole camera](/pinhole-camera-model/), $w = -z_e$, where $z_e$ is the eye-space $z$ coordinate, negative in front of the eye because the camera looks down the $-z$ axis, so $w > 0$ in front of the eye and $w < 0$ behind it. A vertex program can also compute colors, normals and texture coordinates.
2. **Clipping.** The view volume is $-w \le x \le w$, $-w \le y \le w$ and $-w \le z \le w$ in the OpenGL convention ($0 \le z \le w$ in Direct3D). Each bound is a linear inequality in $(x, y, z, w)$, so a triangle is clipped plane by plane, as in [polygon window clipping](/polygon-window-clipping/) by [Sutherland and Hodgman](/sutherland-hodgman/), and the new vertices are linear blends of the old ones in clip coordinates. A clipped triangle is a convex polygon with up to 9 vertices, which is split into a fan of triangles.
3. **The divide.** Each vertex is divided by its $w$, to get normalized device coordinates $(x/w, y/w, z/w)$ in $[-1, 1]^3$. After clipping, $w > 0$ at each vertex, so the divide is defined and keeps the side.
4. **Viewport.** The [viewport transform](/viewport-transform/) maps $[-1, 1]^2$ to the screen of $W \times H$ pixels, $x_s = (x/w + 1)\,W/2$ and $y_s = (1 - y/w)\,H/2$ with $y$ down, and the vertices are snapped to a grid of subpixel steps. [Back-face culling](/back-face-culling/) drops a triangle by the sign of its screen area here.
5. **Rasterization.** The rasterizer finds the pixel centers $(i + \tfrac12, j + \tfrac12)$ that the triangle covers, as in the Direct3D 10 and OpenGL rules, with the [top-left fill rule](/top-left-fill-rule/) for centers on edges. A pixel is a point sample here, not a little square. It also interpolates the vertex values at each center, with [perspective-correct interpolation](/perspective-correct-interpolation/), which interpolates $a/w$ and $1/w$ and divides.
6. **Fragment processing.** Each covered pixel, a fragment, gets a color: [Gouraud](/gouraud-shading/) or [Phong shading](/phong-shading/), [texture mapping](/texture-mapping/), or any fragment program.
7. **Per-fragment tests and output.** The depth test against the [z-buffer](/z-buffer/), the [stencil test](/stencil-buffer/), and [alpha blending](/alpha-blending/) decide what reaches the frame buffer.

**Why clipping comes before the divide.** The map $(x, y, z, w) \mapsto (x/w, y/w)$ sends a line in clip space to a line on the screen, but it is not continuous where $w = 0$: an edge from a vertex with $w > 0$ to one with $w < 0$ passes through $w = 0$, where its image goes to infinity, and comes back from the other side. The screen image of such an edge is two rays to infinity, not the segment between the two divided points. A divide first draws that segment, which is the wrong part of the line. In clip coordinates nothing special happens at $w = 0$: the clip bounds are linear, and the cut is a linear blend. Blinn and Newell (1978) gave this argument and clipped in homogeneous coordinates for this reason.

**Variants of the order.** Hardware clips only against the near plane (and the far plane) and lets the rasterizer skip what falls outside the screen, with a guard band around it. Olano and Greer (1997) rasterize with edge functions in 2D homogeneous coordinates, which needs neither the clip against the side planes nor the divide of the vertices. A parallel renderer splits the pipeline between geometry and rasterization, and sorts the triangles to screen regions there ([sort-middle rendering](/sort-middle-rendering/), [tiled rasterization](/tiled-rasterization/)).

## Examples

Take a projection with the near plane at depth 1 and the far plane at depth 9, a field of view of $90°$ and a $12 \times 12$ screen. Then $x_c = x_e$, $y_c = y_e$, $z_c = -\tfrac54 z_e - \tfrac94$ and $w = -z_e$. The triangle has eye coordinates $A = (-2, -1, -3)$, $B = (2, -1, -3)$ and $C = (0, 2, 1)$; $C$ is behind the eye.

| vertex | eye $(x, y, z)$ | clip $(x, y, z, w)$ | $z + w$ | inside the near plane |
| --- | --- | --- | --- | --- |
| $A$ | $(-2, -1, -3)$ | $(-2, -1, 1.5, 3)$ | $4.5$ | yes |
| $B$ | $(2, -1, -3)$ | $(2, -1, 1.5, 3)$ | $4.5$ | yes |
| $C$ | $(0, 2, 1)$ | $(0, 2, -3.5, -1)$ | $-4.5$ | no |

**Clip first.** The near plane is $z + w \ge 0$. On the edge $BC$ the value $z + w$ goes from $4.5$ to $-4.5$, so the cut is at $t = \tfrac12$, at the clip point $(1, 0.5, -1, 1)$. On $CA$ the cut is $(-1, 0.5, -1, 1)$. The triangle becomes the quadrilateral $A, B, (1, 0.5, -1, 1), (-1, 0.5, -1, 1)$, and each of its vertices now has $w > 0$. The divide gives $(-\tfrac23, -\tfrac13)$, $(\tfrac23, -\tfrac13)$, $(1, \tfrac12)$ and $(-1, \tfrac12)$, and the viewport gives the screen points $(2, 8)$, $(10, 8)$, $(12, 3)$ and $(0, 3)$. The fan of two triangles covers 20 and 30 pixels, 50 in total, in rows 3 to 7: 12 pixels in row 3, 10 in each of rows 4 to 6, and 8 in row 7. The image is a trapezoid that is wide at the top, where the triangle comes close to the eye.

**Divide first.** Dividing $C$ by $w = -1$ gives $(0, -2)$, below the screen, and the screen point $(6, 18)$. The triangle $(2, 8), (10, 8), (6, 18)$ covers 26 pixels in rows 8 to 11, where the true image has none, and the 50 pixels of rows 3 to 7 stay empty. On the edge $AC$, $w$ goes from 3 to $-1$ and is zero at $t = \tfrac34$, at the clip point $(-0.5, 1.25, -2.25, 0)$: the true image of the edge runs from $A$ up and off the top of the screen, and the segment from $A$ down to the divided $C$ is the other part of the line.

**Depth.** After the divide, $z/w = \tfrac12$ at $A$ and $B$, and $-1$ at the two cut points on the near plane. These values go to the depth test.

## Where it is used

- GPUs and the graphics interfaces OpenGL, Direct3D, Vulkan and Metal, where the vertex and fragment stages are programs and the clipping, the divide, the viewport and the rasterizer are fixed hardware.
- Software rasterizers for previews, for tests of hardware and for [shadow mapping](/shadow-mapping/) on the CPU, which follow the same order.
- Parallel and tiled GPU designs, which add a sort step between the stages; mobile GPUs sort to screen tiles.
- The model for other stages that come later in a renderer: visibility with the [hierarchical z-buffer](/hierarchical-z-buffer/), culling with [frustum culling](/frustum-culling/) before vertex processing, and antialiasing with [multisample antialiasing](/multisample-antialiasing/) in the rasterizer.

## References
