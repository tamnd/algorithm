---
title: The perspective-correct march of screen-space reflections and what its hits mean
proves: [correctness]
status: full
---

**Setting.** The camera is at the origin and looks along $-z$. A point $p$ has the view depth $d = -p_z$, and for $d > 0$ it projects to $s_x = (p_x k / (a \tan\theta) + 1)\, W/2$ and $s_y = (p_y k / \tan\theta + 1)\, H/2$ with $k = 1/d$, as in the code. The depth buffer $D$ gives one depth per pixel, or none for the background. The ray starts at the visible point $o$ of a pixel and has the direction $r$ and the length $\ell$. A pixel with the depth $D$ counts as a hit for a ray piece with the depths $[r_{\min}, r_{\max}]$ if $r_{\max} \ge D$ and $r_{\min} \le D + \tau$. That is, every pixel is taken as a slab of thickness $\tau$ behind its visible surface.

**Lemma 1 (the near plane).** After line L1, every point of the segment from $o$ to $e = o + \ell r$ has a depth of at least $\min(d_o, n)$, where $n$ is the near distance. So the projection is defined on the whole segment, and $k > 0$ on it.

*Proof.* The depth is affine along the segment, so it is at least the smaller of its two end values. If $e$ would be nearer than $n$, line L1 shortens the segment so that $e$ has the depth $n$ exactly. $\square$

Without this clip, a ray that points toward the camera can pass through $d = 0$. There $k$ changes sign, and the projected segment is not the image of the 3D segment.

**Lemma 2 (homogeneous interpolation).** Let $p(t) = (1 - t)\, o + t\, e$ for $t \in [0, 1]$, with the depths $d(t) > 0$, and put $k_0 = 1/d_o$, $k_1 = 1/d_e$, $Q_0 = k_0 o$ and $Q_1 = k_1 e$. Put $\lambda = t\, d_e / d(t)$. Then $\lambda$ runs over $[0, 1]$ increasingly with $t$, and

$$\frac{1}{d(t)} = (1 - \lambda) k_0 + \lambda k_1, \qquad \frac{p(t)}{d(t)} = (1 - \lambda) Q_0 + \lambda Q_1.$$

The screen coordinates $s_x$ and $s_y$ of $p(t)$ are also affine in $\lambda$.

*Proof.* Because $d(t) = (1 - t) d_o + t d_e$, we have $1 - \lambda = (1 - t) d_o / d(t)$. Then $(1 - \lambda) Q_0 + \lambda Q_1 = ((1 - t) o + t e) / d(t) = p(t)/d(t)$, and $(1 - \lambda) k_0 + \lambda k_1 = ((1 - t) + t)/d(t) = 1/d(t)$. The derivative of $\lambda$ in $t$ is $d_o d_e / d(t)^2 > 0$. Last, $s_x$ is an affine function of the $x$ coordinate of $p/d$, and $s_y$ of its $y$ coordinate, so both are affine in $\lambda$. $\square$

This is the identity behind [perspective-correct interpolation](/perspective-correct-interpolation/), used in the other direction. The tests check it at random points to $10^{-9}$.

**Theorem 1 (the march is exact).** Let the projected segment not be a point, and let $u$ be its major screen axis (line L3). At every step, the values $k$ and $Q$ of the code are $1/d$ and $p/d$ of the point $p$ of the 3D segment that projects to the current screen position $(p_x, p_y)$, apart from rounding. The reported point $Q/k$ lies on the 3D ray.

*Proof.* By Lemma 2, $s_u$ is affine in $\lambda$ and not constant, so $\lambda$ is affine in $s_u$. The other screen coordinate, $k$ and $Q$ are then affine in $s_u$ as well. An affine function grows by the same amount for every unit step of its argument. Line L4 adds these amounts ($dy$, $dQ$ and $dk$ of the code) for each unit step of $s_u$, starting from the exact values at $o$, so by induction the values at step $m$ are the affine functions at $s_u = x_0 + m$. Then $Q/k = (p/d)\, d = p$. $\square$

A march that interpolates the depth $d$ itself in screen space, or a march that takes equal steps along the 3D ray, does not have this property. The first gets wrong depths. The second puts many steps in one pixel near the camera and skips pixels far away.

**Lemma 3 (the depth ranges cover the march).** The depth $1/k$ is monotone in $s_u$. Step $m$ tests the depth range of the ray over the part of the segment with $s_u$ between $x_0 + m - 1/2$ and $x_0 + m + 1/2$. For the first step, the lower end is $x_0$. These parts follow one another without gaps or overlaps.

*Proof.* $k$ is affine in $s_u$ and positive, so $1/k$ is monotone. A monotone function takes its extreme values on an interval at the ends. The code keeps the depth at the end of the previous part as the start of the next one (`prev_d`). The end of a part is $1/(k + dk/2)$, which is exact by Theorem 1, because $k + dk/2$ is the affine value half a step on. $\square$

**Theorem 2 (what the result means).** Let $(i_m, j_m)$ be the pixel that holds the screen position of step $m$. `trace` returns a hit at step $m$ exactly when these conditions are true:

- Steps $1$ to $m$ are on the screen.
- Steps $1$ to $m$ are not past the end of the projected segment.
- Step $m$ is the first step at which the depth range of Lemma 3 overlaps the slab $[D, D + \tau]$ of the pixel $(i_m, j_m)$.

The returned point is the point of the 3D ray at the center of the part. `trace` returns no hit when the march leaves the screen (line L5), reaches the end of the segment (line L7) or runs out of steps, and none of the earlier steps was a hit.

*Proof.* This follows from the order of the tests in the loop, Lemma 3 and Theorem 1. $\square$

The march visits one pixel per unit of the major axis, the pixel of the center of the part. With a slope of up to 1 on the minor axis, the part can also touch the next pixel on that axis, and that pixel is not tested. So the hit pixel can differ by one pixel from a fine 3D march that tests every pixel the ray crosses. A conservative march that visits every pixel the line crosses would test both. That costs up to twice the steps. The tests compare the code with a fine 3D march on 40 reflections off the floor of a small room. Hit or miss agrees every time, and the hit pixels agree to within one pixel.

**What is not a theorem.** Theorem 2 describes the intersection of the ray with the depth buffer read as slabs of the thickness $\tau$. This is not the intersection with the scene.

- The real objects can be thinner or thicker than $\tau$. A ray behind an object then gives a false hit or passes through it.
- Surfaces that are hidden or off the screen are not in $D$ at all.
- A ray that starts exactly on a flat surface overlaps the slab of the next pixel of the same surface. The caller must move the origin off the surface or skip the first pixels.

The tests show each case in a scene they can solve exactly. With $\tau = \infty$, a ray at depth 9 behind a plate at depth 6 hits the plate. With $\tau = 0.5$ it misses. How good the reflections look in real scenes is a measurement.

**Theorem 3 (cost).** A call of `trace` takes at most $\min(c, \max(W, H) + 1)$ steps of $O(1)$ work, where $c$ is the step limit. So an image of $p$ pixels with one ray each costs $O(p n)$, where $n$ is the number of steps per ray.

*Proof.* Each step moves the screen position by one unit along the major axis, and the march stops at the first position that is off the screen. The origin is a visible pixel, so this takes at most one more step than the length of the screen along that axis. $\square$
