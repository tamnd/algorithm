---
tag: 64PX56
kind: algorithm
slug: phong-shading
name: Phong shading
aliases:
- normal interpolation shading
area: graphics-and-signals/rasterization
level: advanced
summary: Interpolate the vertex normals across each triangle, normalize the result at each pixel and evaluate the lighting model there, so highlights inside a triangle appear.
solves: [polygon-shading]
model: real-ram
complexity:
  vars: {h: the number of pixel rows of the triangle, c: the number of covered pixels}
  time: {worst: Θ(h + c), average: Θ(h + c), best: Θ(h + c)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1975
  people: [Bui Tuong Phong]
  note: Phong interpolated the surface normal along the edges and scanlines of each polygon and evaluated a lighting model with a specular term at each pixel.
prereqs: [gouraud-shading, polygon-shading]
see_also: [lambertian-reflectance, brdf, microfacet-brdf, perspective-correct-interpolation, top-left-fill-rule, fast-inverse-square-root, texture-mapping, z-buffer]
sources:
  - paper: doi:10.1145/360825.360839
    title: Bui Tuong Phong, Illumination for computer generated pictures, Communications of the ACM 18(6), 311 to 317, 1975
    locator: the whole paper (interpolation of the normal along the scan line, and the reflection model with a specular term)
  - paper: doi:10.1145/965141.563893
    title: James F. Blinn, Models of light reflection for computer synthesized pictures, SIGGRAPH 1977, Computer Graphics 11(2), 192 to 198
    locator: the whole paper (the half vector form of the specular term)
  - paper: doi:10.1145/15886.15897
    title: Gary Bishop and David M. Weimer, Fast Phong shading, SIGGRAPH 1986, Computer Graphics 20(4), 103 to 106
    locator: the whole paper (a Taylor expansion of the shading that costs a few additions per pixel)
  - paper: doi:10.1109/T-C.1971.223313
    title: Henri Gouraud, Continuous shading of curved surfaces, IEEE Transactions on Computers C-20(6), 623 to 629, 1971
    locator: the whole paper (the vertex normals and the scanline interpolation that Phong shading keeps)
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 16, Section 16.2.5, Phong Shading (normal-vector interpolation shading)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 5, Shading Basics (evaluation of shading per vertex and per pixel, and the normalization of interpolated normals)
---

Phong shading solves [polygon shading](/polygon-shading/) by interpolating the surface normal instead of the intensity. It keeps the vertex normals and the scanline structure of [Gouraud shading](/gouraud-shading/), but at each pixel it normalizes the interpolated normal and evaluates the lighting model there. A specular highlight whose peak falls inside a triangle, away from its vertices, then appears, where Gouraud shading loses it. The cost is one lighting evaluation and one square root per covered pixel. Bui Tuong Phong published the method in 1975, in the same paper as the Phong reflection model, but the two are separate things: this page is the interpolation scheme, and the lighting model at each pixel can be any model.

## In plain words

A curved object is drawn as many flat pieces. Each corner of a piece knows which way the true surface faces there.

Gouraud shading computes the light only at the corners and then blends the brightness. A shiny spot that falls in the middle of a piece is lost, because no corner sees it.

Phong shading blends the facing direction instead. At each dot inside the piece, it mixes the corner directions in the same even way, makes the result a direction of unit length again, and then computes the light for that dot. So each dot gets its own light, and a shiny spot in the middle of a piece shows up.

The cost is more work for each dot instead of only for each corner.

## The problem

The input is a triangle mesh with a unit normal at each vertex, a light, a viewer, and a lighting model SHADE that maps a unit normal to an intensity. The output is an intensity for each pixel that a triangle covers, smooth over the mesh and continuous across shared edges. This is [polygon shading](/polygon-shading/); the vertex normals come from the mesh as in [Gouraud shading](/gouraud-shading/).

A triangle is already in screen coordinates. Its vertices $v_0, v_1, v_2$ are integers in units of $1/s$ pixel, with $y$ down, and pixel $(i, j)$ is the point sample at its center $(i + \tfrac12, j + \tfrac12)$, as in the Direct3D 10 and OpenGL rules. A pixel is a point, not a little square. The light direction $l$ and the view direction $v$ are unit vectors, the same at each pixel (a distant light and a distant viewer).

## The algorithm

The lighting model in line L11 is a parameter. The usual one is the Phong reflection model,

$$\mathrm{SHADE}(n) = k_a + k_d \max(0, n \cdot l) + k_s \max(0, r \cdot v)^{\alpha}, \qquad r = 2(n \cdot l)\,n - l ,$$

with an ambient part $k_a$, a diffuse part $k_d$ (the [Lambertian](/lambertian-reflectance/) term), a specular part $k_s$ and a shininess $\alpha$, and with the specular term set to zero when $n \cdot l \le 0$. Blinn (1977) replaced $r \cdot v$ with $n \cdot h$, where $h$ is the unit vector half way between $l$ and $v$. Both are lighting models, not shading methods; a physically based [BRDF](/brdf/) such as a [microfacet BRDF](/microfacet-brdf/) fits line L11 in the same way.

The rows are half-open, from $y_{\min}$ included to $y_{\max}$ excluded, and each span is half-open, from $x_l$ included to $x_r$ excluded. A horizontal edge is never active.

```pseudo id=main
PHONG-TRIANGLE(v0, v1, v2, n0, n1, n2)
L1  for each row j whose center y_c has y_min ≤ y_c < y_max do
L2      for each of the two edges (a, b), ordered so that y_a < y_b, with y_a ≤ y_c < y_b do
L3          t ← (y_c − y_a)/(y_b − y_a);  x ← x_a + t(x_b − x_a);  m ← n_a + t(n_b − n_a)
L4      (x_l, m_l), (x_r, m_r) ← the two ends found by line L3, with x_l ≤ x_r
L5      if x_l = x_r then continue with the next row
L6      Δm ← (m_r − m_l)/(x_r − x_l)                ▷ a vector: the change per unit of x
L7      i ← the first pixel whose center x_c has x_c ≥ x_l
L8      m ← m_l + (x_c − x_l)·Δm
L9      while x_c < x_r do
L10         n ← m / |m|                               ▷ back to unit length
L11         write SHADE(n) to pixel (i, j)
L12         m ← m + Δm·(one pixel width);  i ← i + 1;  x_c ← x_c + one pixel width
```

Lines L1 to L9 are the scan of Gouraud shading, with a vector $m$ in place of the intensity: line L3 interpolates the normal along each edge, and lines L6, L8 and L12 interpolate it along the span with three additions per pixel. The interpolated vector is shorter than 1 between normals that point in different directions, so line L10 normalizes it; without this step the [dot products](/dot-product/) in line L11 are wrong. Line L11 is the only place where the light and the viewer enter.

The coverage is the same as in Gouraud shading, so it equals the [top-left fill rule](/top-left-fill-rule/), and a mesh is shaded with each pixel once.

## Example

Let the triangle be $v_0 = (0, 0)$, $v_1 = (8, 0)$ and $v_2 = (0, 8)$ in pixel units, on an $8 \times 8$ screen, with the vertex normals $n_0 = (-0.48, -0.36, 0.8)$, $n_1 = (0.6, 0, 0.8)$ and $n_2 = (0, 0.6, 0.8)$. The light and the viewer are both along $l = v = (0, 0, 1)$, so $r \cdot v = 2(n \cdot l)^2 - 1$. The model has $k_a = 0.1$, $k_d = 0.5$, $k_s = 0.4$ and $\alpha = 20$.

**At the vertices.** Each normal has $n \cdot l = 0.8$, so $r \cdot v = 0.28$ and the specular term is $0.4 \cdot 0.28^{20} \approx 3.5 \cdot 10^{-12}$. Each vertex has the intensity $0.1 + 0.5 \cdot 0.8 = 0.500$. Gouraud shading interpolates three equal values and writes $0.500$ to all 28 covered pixels.

**At pixel (2, 2).** The center $(2.5, 2.5)$ has the barycentric coordinates $(0.375, 0.3125, 0.3125)$, so $m = (0.0075, 0.0525, 0.8)$, with length $0.80176$. Line L10 gives $n = (0.00935, 0.06548, 0.99781)$. Then $n \cdot l = 0.99781$, $r \cdot v = 0.99125$, $(r \cdot v)^{20} = 0.83880$, and line L11 writes $0.1 + 0.5 \cdot 0.99781 + 0.4 \cdot 0.83880 = 0.934$.

**All covered pixels.** The covered pixels are those with $i + j \le 6$; the centers with $i + j = 7$ are on the right edge $v_1 v_2$ and are left to the neighbor triangle. Phong shading writes:

| row $j$ | $i = 0$ | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.531 | 0.561 | 0.602 | 0.701 | 0.634 | 0.570 | 0.541 |
| 1 | 0.556 | 0.602 | 0.850 | 0.850 | 0.602 | 0.556 | |
| 2 | 0.579 | 0.738 | 0.934 | 0.651 | 0.567 | | |
| 3 | 0.602 | 0.701 | 0.634 | 0.570 | | | |
| 4 | 0.586 | 0.586 | 0.565 | | | | |
| 5 | 0.562 | 0.554 | | | | | |
| 6 | 0.537 | | | | | | |

The highlight peaks at $0.934$ near the point where the interpolated normal is closest to $(0, 0, 1)$, and it is fully inside the triangle. Gouraud shading shows a flat $0.500$ here: it cannot make a value larger than the largest vertex value.

## Correctness

**Claim.** If the three vertex normals lie in one open half space, then for a triangle with nonzero area PHONG-TRIANGLE writes exactly the pixels whose centers the triangle covers under the top-left rule, and it writes to each such pixel $\mathrm{SHADE}(g/\lVert g \rVert)$, where $g = \lambda_0 n_0 + \lambda_1 n_1 + \lambda_2 n_2$ for the screen barycentric coordinates $\lambda_k$ of the center.

The coverage tests are those of Gouraud shading, so the coverage part of its proof applies. Each component of $g$ is an affine function of the screen position, so the invariant "$m = g(x_c, y_c)$" holds at line L10 by the same induction. The half space condition makes $g \cdot u > 0$ for a fixed vector $u$ at each point of the closed triangle, so $g \ne 0$ and line L10 is defined. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [real RAM](/real-ram/), with exact rational arithmetic for the coverage decisions, as in Gouraud shading.

- **Per triangle.** Line L1 visits the $h$ rows of the triangle, each with $O(1)$ work in lines L2 to L8. Lines L9 to L12 run once per covered pixel. So the time is $\Theta(h + c)$ in each case, and the extra space is $\Theta(1)$.
- **Per pixel.** Three additions for $m$, one square root and three divisions (or one [inverse square root](/fast-inverse-square-root/) and three multiplications) for line L10, and one evaluation of SHADE: two dot products, and a power for the specular term. Gouraud shading needs one addition per pixel instead.
- **Per mesh.** The lighting runs $\Theta(C)$ times for $C$ covered pixels in total, instead of $\Theta(V)$ times for $V$ vertices in Gouraud shading. With a [z-buffer](/z-buffer/), pixels that are later hidden are also shaded; deferred shading, which first resolves visibility and then shades, makes it $\Theta(wh)$ for a $w \times h$ screen.

## Properties

- **Highlights inside triangles.** The value at a pixel depends on the interpolated normal, not on the vertex values, so it can be larger or smaller than all three vertex values.
- **Continuous across shared edges.** On an edge, $g$ depends only on the two end vertices, so both triangles of the edge give the same normal and the same value there. The derivative of the normal still jumps at the edges, but the Mach bands of Gouraud shading are much weaker.
- **Independent of the orientation on the screen.** For a triangle, the scanline interpolation gives the barycentric combination, so the result does not change when the triangle turns on the screen.
- **Equal to Gouraud shading for linear lighting.** If SHADE is linear in $n$ and the normalization is left out, the two methods give the same values. The difference comes from the normalization and from the nonlinear terms, such as $\max$ and the power.
- **Watertight.** The coverage equals the top-left rule, so a mesh covers each pixel center once.

## Variants and improvements

- **Blinn half vector.** Use $\max(0, n \cdot h)^{\alpha}$ in line L11, as Blinn (1977) proposed. With a distant light and viewer, $h$ is the same at each pixel, so each pixel needs one dot product less work for the reflected vector.
- **Fast Phong shading.** Bishop and Weimer (1986) expanded the diffuse and specular terms in a second order Taylor series in the screen position, so that each pixel costs a few additions and a table lookup instead of a square root and a power.
- **Local light and viewer.** Interpolate the surface position too, and compute $l$ and $v$ per pixel. This is the usual per-pixel lighting of a fragment shader.
- **Perspective-correct normals.** In a 3D view, interpolate $m/w$ and $1/w$ and divide, as in [perspective-correct interpolation](/perspective-correct-interpolation/). The original method interpolates in screen space.
- **Normals from a texture.** Read a perturbed normal from an image with [texture mapping](/texture-mapping/) and use it in line L10, which adds detail that the mesh does not have.

## When to use it

Use Phong shading, or per-pixel lighting in general, when the triangles are large compared with the features of the lighting: a sharp specular highlight, a spot light, or a light close to the surface. The image then does not depend on the tessellation. Use [Gouraud shading](/gouraud-shading/) when the lighting is expensive, the surface is dull, and the triangles cover only a few pixels each, because then the vertices sample the lighting densely and the per-pixel work buys little.

## Pitfalls

- **Not normalized.** Using $m$ in line L11 without line L10 gives $\lVert m \rVert < 1$ between normals that point in different directions. The center between $(0.6, 0, 0.8)$ and $(-0.6, 0, 0.8)$ gets $m = (0, 0, 0.8)$ and a diffuse term $0.8$ instead of $1$, so the middle of a triangle is too dark and the highlight is too weak. Write `n ← m / |m|` in line L10, before any dot product.
- **Normals in opposite directions.** If two vertex normals are almost opposite, $m$ can be close to zero inside the triangle, and line L10 divides by a tiny length or by zero. The proof needs the three normals in one open half space; split such a triangle or fix the normals of the mesh.
- **A closed span on the right.** Writing `while x_c ≤ x_r` in line L9 instead of `x_c < x_r`, or including the row $y_c = y_{\max}$ in line L1, shades the centers of a shared edge twice and breaks [alpha blending](/alpha-blending/).
- **Normals transformed like positions.** Under a nonuniform scaling, a normal multiplied by the model matrix is no longer perpendicular to the surface. Transform the normals by the inverse transpose of the upper $3 \times 3$ part of the model matrix before line L3, and keep $n$, $l$ and $v$ in one coordinate system.
- **Sharp highlights alias.** With a large $\alpha$ the highlight can be narrower than a pixel, and the point samples of line L11 hit or miss it from frame to frame. Phong shading samples the lighting at the pixel centers and does not filter it; use [antialiasing](/antialiasing/) or lower $\alpha$ for small, shiny objects.

## Implementations

## History

Bui Tuong Phong published the method in 1975, in "Illumination for computer generated pictures". He kept the scanline interpolation of [Gouraud shading](/gouraud-shading/) (1971) but interpolated the normal, and he evaluated at each pixel a reflection model with a specular term, the term that Gouraud's interpolation of vertex intensities could not show inside a polygon. The same paper gave the Phong reflection model. Blinn (1977) gave the half vector form of the specular term, which is now called the Blinn-Phong model. Bishop and Weimer (1986) made the per-pixel work cheap enough for hardware with a Taylor expansion. Foley, van Dam, Feiner and Hughes call the method normal-vector interpolation shading.

## References
