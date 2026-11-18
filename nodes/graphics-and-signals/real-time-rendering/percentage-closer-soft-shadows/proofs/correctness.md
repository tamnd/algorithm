---
title: The PCSS penumbra estimate is exact for parallel planes, the blocker search region holds every blocker, and PCF then matches the area light within half a tap
proves: [correctness]
status: full
---

We use the setup of the page. The light is a square of side $w$ in the plane $d = 0$ of the light frame, centered on the axis. The shadow map is a perspective view from the center of the light with its image plane at the near plane $d = n > 0$. It stores the linear depth $d$, and a texel is a square of side $h$ on the near plane. A point at lateral position $x$ and depth $d$ projects to the near plane position $x n / d$. The arithmetic is exact real arithmetic, and the bias is 0.

The proofs work in flatland: one lateral axis $x$ and the depth $d$. The projection acts on each lateral axis on its own, so Lemmas 1 to 3 hold per axis in 3D.

## The penumbra width

Take a blocker that covers the half-line $x < 0$ at depth $d_b$, a receiver line at depth $d_r > d_b$, and a light segment $[-w/2, w/2]$ at depth 0.

**Lemma 1.** The fraction of the light that the receiver point at $x_w$ sees is $V(x_w) = \mathrm{clamp}(\tfrac12 + x_w / w_p, 0, 1)$ with $w_p = (d_r - d_b) w / d_b$. So $V$ goes from 0 to 1 over an interval of width $w_p$, the value of line L5.

*Proof.* The segment from the receiver point $(x_w, d_r)$ to the light point $(x_l, 0)$ meets the depth $d_b$ at $x = x_l + (x_w - x_l) d_b / d_r$. It is blocked when this is negative. Multiply by $d_r > 0$: the light point is visible when $x_l (d_r - d_b) + x_w d_b \ge 0$, that is $x_l \ge -x_w d_b / (d_r - d_b)$. The visible part of $[-w/2, w/2]$ has the length $w/2 + x_w d_b / (d_r - d_b)$, clamped to $[0, w]$. Divide by $w$ to get $\tfrac12 + x_w d_b / (w (d_r - d_b)) = \tfrac12 + x_w / w_p$. $\square$

This is the similar triangles argument of Fernando. It needs the light, the blocker edge and the receiver to lie in parallel planes. For a tilted receiver or for several blockers at different depths, $w_p$ is an estimate.

## The blocker search region

**Lemma 2.** Let $R = (x_r, d_r)$ be a receiver point and $L = (x_l, 0)$ a point of the light, $|x_l| \le w/2$. Every point $P$ of the segment $RL$ with depth $z \in [n, d_r)$ projects to the near plane within $r_s = w (d_r - n) / (2 d_r h)$ texels of the projection of $R$. This is the half-width of line L1.

*Proof.* The point at depth $z$ is $P_x = x_r + (x_l - x_r)(d_r - z)/d_r$. Its projection minus the projection of $R$ is

$$\frac{n P_x}{z} - \frac{n x_r}{d_r} = n \left( \frac{x_r (d_r - z)}{z d_r} + \frac{(x_l - x_r)(d_r - z)}{d_r z} \right) = \frac{n\, x_l\, (d_r - z)}{d_r\, z}.$$

Its absolute value is at most $\tfrac{w}{2} \cdot \tfrac{n (d_r - z)}{d_r z}$. The function $(d_r - z)/z$ decreases in $z$, so on $[n, d_r)$ its largest value is at $z = n$, where the bound is $\tfrac{w}{2} (d_r - n) / d_r$ in near plane units. Divide by $h$. $\square$

So a surface nearer to the light than $n$ cannot be seen by the map, and every surface that the map holds and that blocks some light from $R$ lies inside the search square. Line L2 tests the texel centers in that square, so a blocker that covers no texel center there is not found; this is the sampling error of the map, the same as in [shadow mapping](/shadow-mapping/).

## The two limit cases

**Lemma 3.** (a) If no texel in the search region is nearer than the receiver, PCSS returns 1 (line L3). (b) If $w = 0$, PCSS returns the binary test of the texel that holds $(x, y)$.

*Proof.* (a) is line L3. (b) With $w = 0$, $r_s = 0$. The square of half-width 0 holds a texel center only when $(x, y)$ is a texel center, and then it is the center of the texel that holds $(x, y)$; otherwise the region rule falls back to that texel. So the search tests exactly that texel. If it is not nearer than $d_r$, the result is 1 by (a), and the binary test also says lit. If it is nearer, the blocker depth is its depth, $w_p = 0$ and $r_f = 0$ (line L6), and the PCF of line L7 tests the same single texel, which is in shadow, so the result is 0. $\square$

## The flatland match

Use the map of the half-plane blocker: texel $i$ holds $d_b$ when its center lies left of the axis, and $d_r$ otherwise. Measure the lookup position $u$ in texels from the axis, so the texel centers are the half-integers $c = k + \tfrac12$ and the blocker texels are those with $c < 0$. The receiver point at $x_w$ has $u = x_w n / (d_r h)$.

**Theorem 4.** Suppose $r_f \ge 1$ and that the squares of half-width $r_s$ and $r_f$ around $u$ lie inside the map. Then the PCSS result $P(u)$ satisfies $|P(u) - V(x_w)| \le 1/(2 r_f)$.

*Proof.* The texels with depth less than $d_r$ are exactly the blocker texels, and they all hold $d_b$. So when line L2 finds any, the average of line L4 is $d_b$, line L5 gives the $w_p$ of Lemma 1, and line L6 gives $r_f = w_p n / (2 d_r h)$, which is the half-width $w_p / 2$ of the penumbra measured in texels at the receiver. With $u = x_w n / (d_r h)$, Lemma 1 becomes $V = \mathrm{clamp}((u + r_f) / (2 r_f), 0, 1)$: the length of the part of the window $I = [u - r_f, u + r_f]$ to the right of 0, divided by the length $2 r_f$ of $I$.

Line L7 returns $N_+ / N$, where $N$ is the number of half-integers in $I$ and $N_+$ the number of them that are positive. If $I$ lies on one side of 0, both $P$ and $V$ are 0 or both are 1, because $V$ is clamped exactly when $|u| \ge r_f$ and the half-integer nearest to 0 is $\tfrac12$ away from it. Otherwise let $L_+ = u + r_f > 0$ and $L_- = r_f - u > 0$ be the lengths of the two parts of $I$. The half-integers in $(0, b]$ for $b > 0$ number $\lfloor b + \tfrac12 \rfloor$, which is within $\tfrac12$ of $b$, because 0 lies halfway between two half-integers. So $N_+ = L_+ + e_+$ and $N_- = N - N_+ = L_- + e_-$ with $|e_+|, |e_-| \le \tfrac12$. Then

$$\frac{N_+}{N} - \frac{L_+}{2 r_f} = \frac{N_+ (L_+ + L_-) - L_+ (N_+ + N_-)}{2 r_f N} = \frac{e_+ L_- - e_- L_+}{2 r_f N},$$

and $|e_+ L_- - e_- L_+| \le \tfrac12 (L_- + L_+) = r_f$. So the error is at most $1/(2N)$. Also $N = 2 r_f + e_+ + e_- \ge 2 r_f - 1$, so the error is at most $1/(2 (2 r_f - 1))$, which is at most $1/(2 r_f)$ when $r_f \ge 1$.

There is one more case: the search finds no blocker. Then no half-integer $c < 0$ lies in $[u - r_s, u + r_s]$, so $u - r_s > -\tfrac12$, and PCSS returns 1. Since $d_b \ge n$, we have $r_s \ge r_f$: the inequality $(d_r - n) d_b \ge (d_r - d_b) n$ reduces to $d_r d_b \ge d_r n$. So $u + r_f > r_s + r_f - \tfrac12 \ge 2 r_f - \tfrac12$, and $V \ge (2 r_f - \tfrac12)/(2 r_f) = 1 - 1/(4 r_f)$. The error is at most $1/(4 r_f)$. $\square$

The test checks this bound at random points with $3 \le r_f \le 18$ and a window inside the map. The example of the page has $r_f = 2.5$, and its largest error is $0.05$, at $x_w = \pm 0.25$.
