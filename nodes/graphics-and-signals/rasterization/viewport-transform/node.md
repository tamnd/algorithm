---
tag: NYQG1K
kind: concept
slug: viewport-transform
name: Viewport transform
aliases:
- window-to-viewport transform
area: graphics-and-signals/rasterization
level: intro
summary: The affine map, a scale and a shift on each axis, that takes normalized device coordinates in [-1, 1] to window coordinates, where pixel (i, j) has its center at (i + 1/2, j + 1/2).
prereqs: [pixel]
see_also: [graphics-pipeline, triangle-rasterization, line-rasterization, primary-ray-generation, line-clipping, frame-buffer, z-buffer]
sources:
  - url: https://registry.khronos.org/OpenGL/specs/gl/glspec14.pdf
    title: Mark Segal and Kurt Akeley, The OpenGL Graphics System, A Specification, version 1.4, 2002
    locator: Section 2.10.1, Controlling the Viewport (x_w = (p_x/2) x_d + o_x with o_x = x + w/2 and p_x = w, and the depth range)
  - url: https://microsoft.github.io/DirectX-Specs/d3d/archive/D3D11_3_FunctionalSpec.htm
    title: Microsoft, Direct3D 11.3 Functional Specification
    locator: Section 3.3.1, Pixel Coordinate System, and Section 3.4.1, Coordinate Snapping (fixed point with 8 bits of subpixel precision)
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 5, Geometrical Transformations (the window-to-viewport transformation as a composition of a translation, a scale and a translation)
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 7, Viewing (the viewport transformation from the canonical view volume to the screen)
---

The viewport transform is the affine map that takes a point from normalized device coordinates, where the visible region is the square or cube $[-1, 1]$ on each axis, to window coordinates measured in pixels. On each axis it is a scale and a shift: for a viewport of $w$ by $h$ pixels at $(x_0, y_0)$, the point $x_d = -1$ goes to the left edge $x_0$ and $x_d = 1$ to the right edge $x_0 + w$. In window coordinates [pixel](/pixel/) $(i, j)$ has its center at $(i + \tfrac12, j + \tfrac12)$, so the edges of the square $[-1, 1]^2$ land on pixel edges, not on pixel centers. In two dimensions the same map, from a rectangle of world coordinates to a rectangle of the screen, is the window-to-viewport transform.

## In plain words

A program describes the visible part of a scene in a standard square that goes from minus one to plus one across and up. The screen, or the part of it that shows the picture, is a rectangle measured in pixels. The viewport transform stretches the standard square to the size of that rectangle and moves it to its place.

Each pixel sits in a small cell, and its sample is taken in the middle of the cell. So the left edge of the square goes to the left edge of the first pixel, and the middle of the first pixel is half a pixel further in. Getting this half pixel right keeps shapes from moving by half a pixel when they are drawn.

## The idea

**The window-to-viewport map.** Let a window $[x_{\min}, x_{\max}] \times [y_{\min}, y_{\max}]$ in some coordinates go to a viewport $[u_{\min}, u_{\max}] \times [v_{\min}, v_{\max}]$ on the screen. The map is

$$u = u_{\min} + (x - x_{\min})\,\frac{u_{\max} - u_{\min}}{x_{\max} - x_{\min}}, \qquad v = v_{\min} + (y - y_{\min})\,\frac{v_{\max} - v_{\min}}{y_{\max} - y_{\min}}.$$

It is the composition of a translation of the window corner to the origin, a scale on each axis, and a translation to the viewport corner. It keeps straight lines straight and ratios of lengths along each axis, so a segment clipped to the window stays clipped to the viewport. If the two scale factors differ, circles become ellipses; to keep the shapes, use the same factor on both axes and leave a border.

**From normalized device coordinates.** In a 3D [graphics pipeline](/graphics-pipeline/), clipping and the division by $w$ give normalized device coordinates $(x_d, y_d, z_d)$ with $x_d, y_d \in [-1, 1]$. OpenGL specifies, for the viewport $(x_0, y_0, w, h)$ and the depth range $[n, f]$,

$$x_w = \frac{w}{2}\,x_d + x_0 + \frac{w}{2}, \qquad y_w = \frac{h}{2}\,y_d + y_0 + \frac{h}{2}, \qquad z_w = \frac{f - n}{2}\,z_d + \frac{n + f}{2},$$

with $(x_0, y_0)$ the lower left corner and $y_w$ growing upward. Direct3D has the origin at the top left, $y$ growing downward and $z_d \in [0, 1]$, so it flips the $y$ axis:

$$x_w = (x_d + 1)\,\frac{w}{2} + x_0, \qquad y_w = (1 - y_d)\,\frac{h}{2} + y_0, \qquad z_w = z_{\min} + z_d\,(z_{\max} - z_{\min}).$$

Vulkan uses the form of OpenGL with the origin at the top left, so $y_d = -1$ is the top row there, and $z_d \in [0, 1]$.

**The pixel center rule.** Window coordinates measure in pixel widths from the corner of the buffer. Pixel $(i, j)$ is the point sample at the center $(i + \tfrac12, j + \tfrac12)$ of the cell $[i, i + 1) \times [j, j + 1)$, as in OpenGL, Direct3D 10 and later, and Vulkan. The inverse map gives the normalized device coordinate of the center of column $i$ in a viewport at $x_0 = 0$:

$$x_d = \frac{2i + 1}{w} - 1.$$

So the centers of the first and the last column are at $\pm(1 - 1/w)$, and $x_d = \pm 1$ are pixel edges. Marschner and Shirley use the other common convention, with the centers at integer points: their viewport map sends $[-1, 1]$ to $[-\tfrac12, n_x - \tfrac12]$. The two conventions differ by a shift of half a pixel, and a program must use one of them throughout.

**Snapping.** After the transform, hardware converts $x_w$ and $y_w$ to fixed point with a few bits for the part below one pixel, 8 bits in Direct3D 11, so that the edge tests of the rasterizer are exact integer tests. The transform is the last step in floating point before the integer world of [triangle rasterization](/triangle-rasterization/) and [line rasterization](/line-rasterization/).

## Examples

- **The center of the screen.** In an OpenGL viewport $(0, 0, 800, 600)$, the point $(x_d, y_d) = (0, 0)$ goes to $(400, 300)$. This is the corner that the pixels $(399, 299)$, $(400, 299)$, $(399, 300)$ and $(400, 300)$ share, not the center of a pixel: a screen with an even number of columns has no center pixel.
- **A corner pixel.** The center $(0.5, 0.5)$ of pixel $(0, 0)$ comes from $x_d = 1/800 - 1 = -0.99875$ and $y_d = 1/600 - 1 \approx -0.99833$. In Direct3D the same viewport sends $(x_d, y_d) = (-1, 1)$ to $(0, 0)$, the top left corner of the buffer.
- **A full point.** With the depth range $[0, 1]$ of OpenGL, the point $(0.25, -0.5, 0.2)$ goes to $x_w = 400 \cdot 1.25 = 500$, $y_w = 300 \cdot 0.5 = 150$ and $z_w = 0.5 \cdot 0.2 + 0.5 = 0.6$.
- **A map window.** Showing the world rectangle $[100, 300] \times [50, 150]$ in a viewport of 400 by 200 pixels scales both axes by 2, so the world point $(250, 75)$ goes to $(300, 50)$ above the lower left corner of the viewport. The same window in a viewport of 400 by 400 pixels scales $y$ by 4 and stretches each shape to twice its height.
- **A snapped vertex.** With 8 subpixel bits, $x_w = 500.3$ becomes $\operatorname{round}(500.3 \cdot 256)/256 = 128077/256 \approx 500.30078$.
- **Split screen.** Two players each get a viewport of 400 by 600 pixels at $x_0 = 0$ and at $x_0 = 400$, and the same scene in normalized device coordinates appears in each half.

## Where it is used

- **The graphics pipeline.** Each GPU applies the transform to each vertex after clipping and the perspective division, and before rasterization; the [graphics pipeline](/graphics-pipeline/) page shows it in place. The depth $z_w$ goes to the [z-buffer](/z-buffer/).
- **Ray generation.** A ray tracer runs the map in the other direction: [primary ray generation](/primary-ray-generation/) takes the center $(i + \tfrac12, j + \tfrac12)$ of each pixel to normalized coordinates and then to a direction from the camera.
- **Picking.** A program that finds the object under the mouse turns the window coordinates of the mouse back into normalized device coordinates with the inverse map, and then into a ray.
- **2D drawing and maps.** Plotting libraries, map viewers and CAD programs map a rectangle of data or world coordinates to a rectangle of the window, then [clip lines](/line-clipping/) to it.
- **Window systems.** A window system gives each window its own viewport in the [frame buffer](/frame-buffer/) of the screen.

## References
