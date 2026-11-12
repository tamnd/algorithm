---
tag: Z231EF
kind: technique
slug: perspective-correct-interpolation
name: Perspective-correct interpolation
aliases:
- hyperbolic interpolation
area: graphics-and-signals/rasterization
level: advanced
summary: Interpolate a/w and 1/w linearly in screen space and divide at each pixel, which gives the value of the attribute at the 3D point that the pixel sees.
prereqs: [triangle-rasterization, graphics-pipeline]
see_also: [texture-mapping, mipmap, z-buffer, gouraud-shading, phong-shading, edge-function, shadow-mapping, pineda-rasterization]
sources:
  - paper: doi:10.1007/978-1-4612-4448-6_5
    title: Paul S. Heckbert and Henry P. Moreton, Interpolation for polygon texture mapping and shading, in State of the Art in Computer Graphics, Visualization and Modeling, Springer, 1991
    locator: pages 101 to 111 (the projective mapping of a polygon, and the linear interpolation of a/w and 1/w in screen space)
  - paper: doi:10.1109/MCG.1992.10028
    title: James F. Blinn, Hyperbolic interpolation, IEEE Computer Graphics and Applications 12(4), 89 to 94, 1992
    locator: the whole column (interpolation of homogeneous parameters and the division per pixel)
  - paper: doi:10.1145/258694.258723
    title: Marc Olano and Trey Greer, Triangle scan conversion using 2D homogeneous coordinates, Graphics Hardware 1997
    locator: the whole paper (interpolation of parameters from homogeneous edge functions, which gives a/w and 1/w directly)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 23, Section 23.1, Rasterization (perspective-correct interpolation of the attributes with barycentric coordinates)
  - paper: doi:10.1145/965139.807398
    title: James F. Blinn and Martin E. Newell, Clipping using homogeneous coordinates, SIGGRAPH 1978, Computer Graphics 12(3), 245 to 251
    locator: the whole paper (the clip coordinates in which the attributes of new vertices are blended)
---

Perspective-correct interpolation is the technique that a rasterizer uses to give each covered pixel the value of a vertex attribute, such as a texture coordinate, at the 3D point of the triangle that the pixel sees. Under a perspective projection, an attribute that is affine on the 3D triangle is not affine in screen coordinates, so plain screen-space interpolation is wrong. But $a/w$ and $1/w$ are affine in screen coordinates, where $w$ is the clip coordinate of the [graphics pipeline](/graphics-pipeline/). So the rasterizer interpolates $a/w$ and $1/w$ linearly, with the screen barycentric coordinates, and divides one by the other at each pixel. Blinn (1992) named the result hyperbolic interpolation, because along a line in screen space the attribute is a ratio of two affine functions.

## In plain words

Look down a straight road with white stripes at equal steps. On the picture, the near stripes are far apart and the far stripes are close together.

A triangle in a 3D scene behaves in the same way. If the computer spreads a picture over the triangle evenly across the screen, the far part of the picture is too large and the near part too small, and straight lines in the picture bend where two triangles meet.

The fix uses one more number per corner, which tells how far away the corner is. Two quantities change evenly across the screen even under perspective: the picture position divided by that distance, and one over that distance. The computer spreads these two evenly, and at each dot it divides one by the other. The result is the right point of the picture.

## When it applies

- The triangle is drawn with a perspective projection, so its vertices have different clip coordinates $w_k > 0$. With an orthographic projection all $w_k = 1$, and plain screen-space interpolation is already correct.
- The attribute $a$ is affine on the 3D triangle, that is, it is $\sum_k \beta_k a_k$ for the barycentric coordinates $\beta_k$ of the 3D point. Texture coordinates, colors and normals given at the vertices are of this kind. A value that is not affine on the triangle, such as a lighting result, is not made correct by this technique.
- The screen positions are $s_k = (x_k/w_k, y_k/w_k)$ after the viewport transform, and pixel $(i, j)$ is the point sample at its center $(i + \tfrac12, j + \tfrac12)$, as in the Direct3D 10 and OpenGL rules. The screen barycentric coordinates $\lambda_k$ of the center come from the [edge functions](/edge-function/): $\lambda_k = E_k / (2S)$.
- The triangle has been clipped so that each $w_k > 0$. The new vertices of a clip get their $w$ and their attributes by linear blends in clip coordinates, not in screen coordinates.

## The template

```pseudo id=main
PERSPECTIVE-CORRECT(triangle with clip w_k > 0 and attributes a_k, k = 0, 1, 2)
L1  for k ← 0 to 2 do                                ▷ once per triangle
L2      q_k ← 1/w_k;  b_k ← a_k/w_k
L3  for each covered pixel center p do
L4      (λ_0, λ_1, λ_2) ← the screen barycentric coordinates of p
L5      q ← λ_0 q_0 + λ_1 q_1 + λ_2 q_2              ▷ equals 1/w at p
L6      b ← λ_0 b_0 + λ_1 b_1 + λ_2 b_2              ▷ equals a/w at p
L7      a ← b/q
```

Lines L5 and L6 are affine in the screen position, so a scanline or [Pineda](/pineda-rasterization/) rasterizer can update $q$ and $b$ with one addition each per pixel. Line L7 is one division per pixel, or one reciprocal of $q$ and then one multiplication per attribute. The value $1/q$ is also the clip $w$ at the pixel, which is the eye depth for a standard projection.

**Why it works.** The projection is linear in homogeneous coordinates. Let $c_k = (x_k, y_k, z_k, w_k)$ be the clip coordinates of the vertices, and let the pixel see the 3D point with barycentric coordinates $\beta_k$, so its clip coordinates are $c = \sum_k \beta_k c_k$ and $w = \sum_k \beta_k w_k$. Its screen position is

$$s = \frac{(x, y)}{w} = \sum_k \frac{\beta_k w_k}{\sum_j \beta_j w_j}\, s_k .$$

The weights sum to 1, so they are the screen barycentric coordinates: $\lambda_k = \beta_k w_k / w$. Solve for $\beta_k$: $\beta_k = w\,\lambda_k / w_k$, and $\sum_k \beta_k = 1$ gives $w \sum_j \lambda_j / w_j = 1$. So

$$\frac{1}{w} = \sum_j \frac{\lambda_j}{w_j}, \qquad \beta_k = \frac{\lambda_k / w_k}{\sum_j \lambda_j / w_j}, \qquad a = \sum_k \beta_k a_k = \frac{\sum_k \lambda_k\, a_k / w_k}{\sum_k \lambda_k / w_k} .$$

The first equation is line L5, the numerator of the last is line L6, and the last is line L7. Both $1/w$ and $a/w$ are affine in the screen position, because the $\lambda_k$ are.

## Classic examples

- **[Texture mapping](/texture-mapping/).** The texture coordinates $(u, v)$ are interpolated with lines L5 to L7. This is the case that made the technique standard.
- **The [z-buffer](/z-buffer/).** The stored depth $z/w$ is itself affine in screen space, so it is interpolated with line L6 alone, with $a = z$ and no division. This is why the depth buffer is not linear in the eye distance.
- **[Mipmap](/mipmap/) level selection.** The derivatives of $u$ and $v$ with respect to $x$ and $y$ come from the quotient rule on $b/q$: $\partial a/\partial x = (\partial b/\partial x - a\, \partial q/\partial x)/q$.
- **Colors and normals.** [Gouraud shading](/gouraud-shading/) and [Phong shading](/phong-shading/) in a 3D view interpolate the colors or the normals in the same way.
- **[Shadow mapping](/shadow-mapping/) and projective textures.** The light space coordinates $(s, t, r, q)$ form a homogeneous attribute; the rasterizer interpolates them affinely in the plane of the triangle, and the shader divides by the interpolated $q$.

**A worked example.** Use the projection with $w = -z_e$, a field of view of $90°$ and an $8 \times 8$ screen. The eye points $(-1, -1, -1)$, $(4, -4, -4)$ and $(-4, 4, -4)$ have $w = 1, 4, 4$ and the screen points $(0, 8)$, $(8, 8)$ and $(0, 0)$. Give them the texture coordinates $(0, 0)$, $(1, 0)$ and $(0, 1)$. The exact value is found by casting the ray from the eye through the pixel center and intersecting it with the 3D triangle in rational arithmetic; it agrees with line L7 at each point:

| screen point | $\lambda$ | $1/w$ | $w$ | affine $(u, v)$ | correct $(u, v)$ = exact |
| --- | --- | --- | --- | --- | --- |
| $(3.5, 4.5)$ | $(\tfrac18, \tfrac{7}{16}, \tfrac{7}{16})$ | $\tfrac{11}{32}$ | $2.909$ | $(0.4375, 0.4375)$ | $(\tfrac{7}{22}, \tfrac{7}{22}) = (0.3182, 0.3182)$ |
| $(4, 8)$, the screen midpoint of an edge | $(\tfrac12, \tfrac12, 0)$ | $\tfrac58$ | $1.6$ | $(0.5, 0)$ | $(0.2, 0)$ |
| $(0.5, 7.5)$ | $(\tfrac78, \tfrac{1}{16}, \tfrac{1}{16})$ | $\tfrac{29}{32}$ | $1.103$ | $(0.0625, 0.0625)$ | $(\tfrac{1}{58}, \tfrac{1}{58}) = (0.0172, 0.0172)$ |
| $(2.5, 2.5)$, on the far edge | $(0, \tfrac{5}{16}, \tfrac{11}{16})$ | $\tfrac14$ | $4$ | $(0.3125, 0.6875)$ | $(0.3125, 0.6875)$ |

The screen midpoint of the edge from $w = 1$ to $w = 4$ sees the point one fifth of the way along the 3D edge, not the midpoint. On the far edge both vertices have $w = 4$, and there the affine value is already correct.

## Variations

- **Division per span.** Software renderers of the 1990s computed the exact value every 8 or 16 pixels of a span and interpolated affinely between, to save divisions. The error is small when the depth changes little over the short piece.
- **Homogeneous rasterization.** Olano and Greer (1997) set up the edge functions in 2D homogeneous coordinates; the interpolated parameters then come out as $a/w$ and $1/w$, without the divide of the vertices.
- **Barycentric form.** GPUs compute $\beta_k$ once per pixel from $\lambda_k / w_k$ and then use them for all attributes, which costs one reciprocal per pixel instead of one division per attribute.
- **No perspective.** Shading languages let an attribute ask for plain screen-space interpolation (the `noperspective` qualifier in GLSL), for values that are defined on the screen.
- **Quadrilaterals and polygons.** For a planar polygon, $a/w$ and $1/w$ are still affine in screen space, so the same interpolation works on the whole polygon; Heckbert and Moreton (1991) give the projective map.

## Pitfalls

- **Affine texture mapping.** Writing $a \leftarrow \sum_k \lambda_k a_k$ instead of lines L5 to L7 stretches the near part of each triangle and bends straight lines of the texture along the shared edges. The first PlayStation drew textures in this way, and its games split large polygons into smaller ones to hide it.
- **The wrong depth.** Using the normalized depth $z/w$ or the screen depth in place of $w$ in line L2 gives the wrong weights; line L2 needs the clip $w$, which is the eye distance $-z_e$.
- **Interpolating $w$ instead of $1/w$.** Writing $q \leftarrow \sum_k \lambda_k w_k$ in line L5 and then $1/q$ as the reciprocal depth, or dividing an interpolated $a$ by an interpolated $w$, is not the formula. The quantities that are affine on the screen are $1/w$ and $a/w$, so line L2 divides at the vertices, lines L5 and L6 sum, and only line L7 divides the two sums.
- **Clipped vertices blended in screen space.** A vertex made by the near-plane clip must get its attribute by a blend in clip coordinates, with the same parameter as its position. A blend of the screen positions uses a different parameter and puts a seam along the clip edge.
- **Precision of $1/w$.** For a triangle that reaches far away, $q$ is small at the far end and the relative error of the float sums of lines L5 and L6 grows. Compute $\lambda_k$ from exact integer [edge functions](/edge-function/) and keep $q$ and $b$ in full float precision.

## Exercises

1. Show that for an orthographic projection, with $w_k = 1$, lines L5 to L7 reduce to plain screen-space interpolation.
2. On a segment from a vertex with $w = 1$ to one with $w = 4$, find the screen parameter $\mu$ that sees the 3D midpoint. (Answer: $\mu = \tfrac45$.)
3. Prove that $z/w$, for $z$ the clip depth, is affine in screen space, and so a depth buffer needs no division per pixel.
4. Derive the formula for $\partial u/\partial x$ in terms of the screen derivatives of $b$ and $q$, and use it to find the mipmap level at pixel $(3.5, 4.5)$ of the worked example for a $256 \times 256$ texture.
5. A span of 16 pixels has $w$ from 2 to 3 at its ends. Bound the largest error of affine interpolation of $u$ from 0 to 1 over the span, and compare it with the error over 8 pixels.

## References
