---
title: The shadow test is exact at texel centers, and a bias of half the slope removes self-shadowing
proves: [correctness]
status: full
---

We use the pseudocode and the definitions of the page. The light transform $M$ maps a world point $p$ to $(x, y, z) = (h_x, h_y, h_z)/h_w$ with $h_w > 0$ at every point of the scene. The light is the point where $h_w = 0$ for a perspective light, or the point at infinity in the direction of decreasing depth for an orthographic light. For a triangle $t$ let $t'$ be its image, and let $z_t(x, y)$ be the depth of $t'$ at $(x, y)$. A point $p$ is *in shadow* at texel $(i, j)$ when some triangle $t$ has $(x, y) \in t'$ under the fill rule and $z_t(x, y) < z$.

**Lemma 1 (the map).** After line L4, $S[i, j] = \min z_t(i + \tfrac12, j + \tfrac12)$ over the triangles $t$ whose image covers the center of texel $(i, j)$, and $S[i, j] = +\infty$ if there is none.

*Proof.* Lines L1 to L4 are the z-buffer of the triangles $t'$ without the color buffer. The z-buffer proof shows that each cell holds the least plane depth at its center over the covering triangles, since $\min$ does not depend on the order of the updates. $\square$

**Lemma 2 (the segment to the light).** Let $p$ be a point of the scene with image $(x, y, z)$. A point $p'$ of the scene lies on the open segment from $p$ to the light if and only if its image is $(x, y, z')$ with $z' < z$.

*Proof.* $M$ is a projective map, so it takes lines to lines and keeps the order of points on a line where $h_w$ does not change sign. The line from $p$ to the light maps to the line of the points with the same $(x, y)$, since all rays from the light map to lines parallel to the depth axis: for a perspective light the light is the center of projection, and for an orthographic light the rays are parallel to the depth axis already. The light maps to depth $-\infty$ in the order of the depth axis, because the depth increases away from the light along each ray. So the points between $p$ and the light are those with the same $(x, y)$ and a smaller depth. $\square$

**Theorem 1 (exact at texel centers).** Let $p$ map to $(x, y, z)$ with $(x, y) = (i + \tfrac12, j + \tfrac12)$ inside the map. Then SHADOWED$(S, M, p, 0)$ is true if and only if $p$ is in shadow.

*Proof.* Line L6 gives the texel $(i, j)$, since $\lfloor i + \tfrac12 \rfloor = i$. Line L7 returns $z > S[i, j]$. By Lemma 1 this holds if and only if some triangle $t$ covers the center with $z_t(i + \tfrac12, j + \tfrac12) < z$. By Lemma 2 the point of $t$ there lies between $p$ and the light. A triangle through $p$ has $z_t = z$ at the center and does not make the strict test true, so a surface does not shadow itself at a texel center. $\blacksquare$

**Theorem 2 (the bias for a planar receiver).** Let $p$ lie on a triangle $t$ whose image covers the whole texel $(i, j)$ that holds $(x, y)$, and let no other triangle cover the center of that texel with a smaller depth. Let $z_t(x, y) = a x + b y + c$. If the bias is $\beta \ge \tfrac12 (|a| + |b|)$, then SHADOWED$(S, M, p, \beta)$ is false.

*Proof.* By Lemma 1, $S[i, j] = z_t(i + \tfrac12, j + \tfrac12)$. The point $(x, y)$ is in the texel, so $|x - (i + \tfrac12)| \le \tfrac12$ and $|y - (j + \tfrac12)| \le \tfrac12$. Then
$$z - S[i, j] = a (x - i - \tfrac12) + b (y - j - \tfrac12) \le \tfrac12 (|a| + |b|) \le \beta,$$
so $z - \beta \le S[i, j]$, and line L7 returns false. $\square$

The bound is tight: for $a > 0$, $b = 0$ and $x$ just below $i + 1$, the difference $z - S[i, j]$ is just below $a/2$. In the example of the page, $a = \tfrac12$ and $b = 0$, so a bias of $\tfrac14$ suffices.

**Theorem 3 (PCF).** PCF$(S, M, p, b, r)$ returns the fraction of the $(2r + 1)^2$ texels around $(\lfloor x \rfloor, \lfloor y \rfloor)$ at which line L7 with the same $z$ and $b$ returns true.

*Proof.* Line L9 counts the pairs $(u, v)$ for which the test of line L7 holds at texel $(i + u, j + v)$, with the border rule of line L7 for texels outside the map, and line L10 divides by the number of pairs. $\square$

So PCF is a value in $[0, 1]$ that is 0 where all neighbors are lit and 1 where all are shadowed, and filtering the binary results, not the depths, is what gives this meaning.
