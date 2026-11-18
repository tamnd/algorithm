---
title: Tiled light culling never drops a light that reaches a pixel
proves: [correctness]
status: full
---

**Setting.** The camera is at the origin and looks along $-z$. The screen has $W \times H$ pixels, the aspect ratio is $a = W / H$ and $\tan\theta$ is the tangent of half the vertical field of view. A screen point $(s_x, s_y)$ in pixels has the slopes $u(s_x) = (2 s_x / W - 1)\, a \tan\theta$ and $v(s_y) = (2 s_y / H - 1) \tan\theta$, and the pixel $(i, j)$ with view depth $d > 0$ has the position $P = d\,(u(i + 1/2), v(j + 1/2), -1)$. A light has a center $c$ and a radius $r > 0$, and it reaches $P$ if $\lVert P - c \rVert < r$. SHADE returns exactly 0 when $\lVert P - c \rVert \ge r$. A tile covers the pixel rectangle $[x_0, x_1] \times [y_0, y_1]$, and $d_{\min}$ and $d_{\max}$ are the smallest and largest depths of its pixels with geometry. Lines L11 to L13 keep a light unless $m \cdot c < -r$ for one of the four unit plane normals $m$, or $-c_z + r < d_{\min}$, or $-c_z - r > d_{\max}$. The claims are in exact arithmetic. The code adds a slack of $10^{-9} r$ to the radius, which only keeps more lights.

**Lemma 1 (pixels lie in their tile frustum).** Let $u_0 = u(x_0)$, $u_1 = u(x_1)$, $v_0 = v(y_0)$, $v_1 = v(y_1)$, and let the four planes have the normals $(1, 0, u_0)$, $(-1, 0, -u_1)$, $(0, 1, v_0)$ and $(0, -1, -v_1)$, each divided by its length. Then $m \cdot P \ge 0$ for each of these normals and for every pixel $(i, j)$ of the tile at any depth $d > 0$.

*Proof.* $u$ is an increasing linear function of $s_x$, and $x_0 \le i + 1/2 \le x_1$, so $u_0 \le u_P \le u_1$ with $u_P = u(i + 1/2)$. For the first normal, $(1, 0, u_0) \cdot P = d u_P - d u_0 = d (u_P - u_0) \ge 0$. For the second, $(-1, 0, -u_1) \cdot P = d (u_1 - u_P) \ge 0$. The two planes in $y$ are the same with $v$. Dividing by a positive length keeps the signs. $\square$

**Theorem 1 (no miss).** If a light reaches the position $P$ of a pixel of a tile, then the light is in the list of that tile.

*Proof.* Let $\delta = \lVert P - c \rVert < r$. For each unit normal $m$ of the tile, Lemma 1 and the Cauchy-Schwarz inequality give

$$m \cdot c = m \cdot P + m \cdot (c - P) \ge 0 - \lVert m \rVert \lVert c - P \rVert = -\delta > -r,$$

so no plane rejects the light. For the depth test, the depth of the pixel is $d = -P_z$ with $d_{\min} \le d \le d_{\max}$, and $|(-c_z) - d| = |P_z - c_z| \le \delta < r$. So $-c_z + r > d \ge d_{\min}$ and $-c_z - r < d \le d_{\max}$, and the depth test does not reject it either. Line L13 then keeps the light. $\square$

**Theorem 2 (the image is the brute-force image).** Suppose that each tile list holds every light that reaches a pixel of the tile, and that its lights are visited in increasing index order. Then the tiled image equals the image of shading every pixel with every light in index order, value for value, also in floating point.

*Proof.* For a pixel, let $J$ be the list of its tile. By the assumption, every light not in $J$ does not reach the pixel, so SHADE returns exactly 0 for it. The brute-force sum visits the lights in index order and adds $+0$ for each light not in $J$; in IEEE 754 arithmetic $x + 0 = x$ for every $x$ that is not $-0$, and the partial sums start at $+0$ and stay $\ge 0$. So the brute-force sum performs the same nonzero additions in the same order as the tiled sum, and the two results are equal. $\square$

Theorem 1 gives the assumption of Theorem 2 in exact arithmetic. In floating point, a rounded plane test could drop a light whose sphere touches the frustum within the rounding error. The slack on the radius is there for that case, and the tests check the assumption directly against the exact distance test at every pixel.

**Theorem 3 (cost).** With $t$ tiles, $l$ lights and $p$ pixels, building the lists costs $O(p + t l)$ and shading costs $O(\sum_q |J(q)|) \le O(p l)$.

*Proof.* The depth ranges read each pixel once. Each tile tests each light once at $O(1)$ cost. Each pixel loops over its list once. $\square$

**What is not claimed.** The test is conservative, not exact. It keeps lights that reach no pixel of the tile: lights near the corner of two planes, where the sphere is outside the frustum but not outside one plane, and lights that sit in a depth gap between the near and the far pixels of a tile. The number of such false positives depends on the scene and is measured, not proved. The radius of a light is a property of the light model: a light whose real falloff never reaches 0 is cut at a radius, and the error of that cut is tuning.
