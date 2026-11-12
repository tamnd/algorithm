---
tag: R0WW8P
kind: concept
slug: z-fighting
name: Z-fighting
aliases:
- depth fighting
area: graphics-and-signals/visibility
level: intro
summary: A pattern of pixels that flips between two surfaces when the depth buffer cannot tell their depths apart, from limited depth precision or coplanar surfaces.
prereqs: [z-buffer, ieee-754]
see_also: [shadow-mapping, ulp, floating-point-model, depth-peeling, perspective-correct-interpolation, viewport-transform]
sources:
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 4.7 (perspective projection, the distribution of depth values, and reversed depth with a floating-point buffer)
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 15, the section on the z-buffer algorithm (the depth resolution after the perspective transform)
  - url: https://registry.khronos.org/OpenGL/extensions/ARB/ARB_clip_control.txt
    title: The Khronos Group, ARB_clip_control, OpenGL extension specification
    locator: the overview (the mode ZERO_TO_ONE, which puts the near plane at a normalized depth of 0 as in Direct3D, to improve the precision of floating-point depth buffers)
---

Z-fighting is the pattern of pixels that switch between two surfaces when the [z-buffer](/z-buffer/) cannot tell their depths apart. It happens when the surfaces are coplanar, or when they are closer together than the depth resolution at their distance. After a perspective projection the resolution is far from uniform: with a $b$-bit fixed-point buffer it is about $z^2 (f - n)/(f n 2^b)$ at view distance $z$, for near and far planes $n$ and $f$. A larger near distance, or reversed depth in a floating-point buffer, makes it much finer.

## In plain words

A depth buffer stores the distance of the nearest surface at each dot of the picture, but only with a fixed number of digits. Near the camera these digits are fine. Far away they are coarse, because of the way the camera maps distance to stored numbers.

When two surfaces are almost at the same distance, for example a poster on a wall, the stored numbers of both can be equal, or the order can change from one dot to the next by small rounding errors. Then some dots show the poster and some dots show the wall, in a noisy pattern. When the camera moves, the pattern changes in each frame, and the picture flickers.

## The idea

**The depth after projection.** A perspective projection with near plane $n$ and far plane $f$ (both positive, $n < f$) maps the view distance $z \in [n, f]$ to the stored depth. In the Direct3D form with the range $[0, 1]$,

$$d(z) = \frac{f}{f - n} \left(1 - \frac{n}{z}\right), \qquad d(n) = 0, \quad d(f) = 1.$$

This $d$ is affine in the screen coordinates on each triangle, which is why the z-buffer can interpolate it (see [perspective-correct interpolation](/perspective-correct-interpolation/)). But it is not affine in $z$: its slope is

$$d'(z) = \frac{f n}{(f - n) z^2},$$

which is large near the camera and small far away. Half of the range $[0, 1]$ is used for $z \le 2n f/(f + n)$, which is less than $2n$.

**Resolution.** A $b$-bit fixed-point buffer stores $d$ in steps of $2^{-b}$. Two surfaces at distance $z$ get distinct stored values only if their distances differ by about

$$\Delta z \approx \frac{2^{-b}}{d'(z)} = \frac{z^2 (f - n)}{f n \, 2^b}.$$

The resolution grows as $z^2$, and it is set mostly by $n$: for $f \gg n$ it is about $z^2/(n 2^b)$, almost independent of $f$. So moving the near plane out from $0.1$ to $1$ makes it 10 times finer at each distance, but moving the far plane in from 1000 to 100 changes it very little.

**Reversed depth.** Store $d_r = 1 - d$ in a 32-bit [IEEE 754](/ieee-754/) float, so that the near plane is at 1 and the far plane at 0, and use the depth test $>$ in place of $<$. The spacing of floats near a value $v$ is about $v \cdot 2^{-23}$ (one [ulp](/ulp/)), so the floats are dense near 0, which is now the far part of the scene. For $f \gg n$, $d_r \approx n/z$, and the resolution becomes about $z$ times a value between $2^{-24}$ and $2^{-23}$: a nearly constant *relative* precision. A float buffer in the normal direction gains almost nothing, because there the values near $d = 1$ get the coarse spacing of floats near 1. In OpenGL the default clip range of $[-1, 1]$ maps $d_r$ around $\tfrac12$ and loses the gain; the extension ARB_clip_control gives the range $[0, 1]$.

**Coplanar surfaces.** Two triangles in the same plane, with different vertices, have the same exact depth at each pixel center. In floating point the two depths are computed by different operations from different vertices, so they differ in the last digits, with a sign that changes from pixel to pixel. No depth precision removes this. The fixes are to remove one of the surfaces, to draw the second surface with a depth offset (a *polygon offset* or *depth bias*), or to draw it with an equal-or-nearer test after the first one.

## Examples

**Resolution at 24 bits.** For $n = 0.1$, $f = 1000$ and a 24-bit fixed-point buffer, the smallest depth difference that changes the stored value is about:

| distance $z$ | 24 bits, $n = 0.1$ | 24 bits, $n = 1$ | 32-bit float, reversed, $n = 0.1$ |
|---|---|---|---|
| 1 | $6.0 \times 10^{-7}$ | $6.0 \times 10^{-8}$ | $7.5 \times 10^{-8}$ |
| 10 | $6.0 \times 10^{-5}$ | $6.0 \times 10^{-6}$ | $9.3 \times 10^{-7}$ |
| 100 | $6.0 \times 10^{-3}$ | $6.0 \times 10^{-4}$ | $5.8 \times 10^{-6}$ |
| 1000 | $0.60$ | $0.060$ | not used (the far plane) |

The first two columns are the formula for $\Delta z$. The last column is the gap between a 32-bit float $d_r(z)$ and the next float, divided by $|d_r'(z)|$. In a scene in meters, a 24-bit buffer with the near plane at 10 cm cannot separate two surfaces 6 mm apart at 100 m.

**Equal stored values.** With $n = 0.1$, $f = 1000$, 24 bits and rounding to nearest, the distances $100$ and $100.002$ both store the integer $16{,}762{,}115$. The two surfaces are equal to the depth test, and the result at each pixel depends on the draw order and the test. With $n = 1$, the same distances store $16{,}626{,}070$ and $16{,}626{,}073$, and the test separates them.

**A decal.** A poster drawn on a wall, in the plane of the wall, fights with the wall at each distance. A small depth bias toward the camera, or drawing the poster after the wall with the test $\le$, fixes it.

## Where it is used

The depth precision analysis sets the near and far planes of a camera: put the near plane as far out as the scene allows, because it controls the resolution. Large outdoor scenes and space scenes use reversed depth with a 32-bit float buffer, or split the depth range into several passes. Decals, outlines and the second pass of a multipass renderer use a depth bias or an equal test. The same precision problem appears in [shadow mapping](/shadow-mapping/), where a surface compared with its own stored depth shadows itself (shadow acne), and the same fix, a depth bias, has the same cost: too much bias moves the surfaces apart. In [depth peeling](/depth-peeling/), coplanar fragments need a tie break, or a layer is lost.

## References
