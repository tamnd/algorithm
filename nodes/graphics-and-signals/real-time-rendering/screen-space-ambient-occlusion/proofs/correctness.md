---
title: What screen-space ambient occlusion estimates, and its exact cases
proves: [correctness]
status: full
---

**Setting.** The camera is orthographic and looks along $-z$, as in the code. The pixel $(i, j)$ has its center at $(i + 1/2, j + 1/2)$ and the depth $D_{ij} > 0$, and its point is $P = (x, y, -d)$. The reconstructed depth $\hat D(x, y)$ is the bilinear or the nearest lookup of the buffer. For an offset $k$, the sample $S = P + k$ is occluded when $\hat D(S_x, S_y) < d - k_z - \beta$ with the bias $\beta \ge 0$: the stored surface is nearer to the camera than the sample. Without the range check, each occluded sample adds 1, and the result is $A = 1 - (\text{occluded samples}) / s$ for $s$ samples. The claims assume that every sample projects inside the buffer, away from the clamped border.

**Lemma 1 (bilinear lookup on a plane).** If $D_{ij} = d_0 + g_x (i + 1/2) + g_y (j + 1/2)$ for all pixels, then the bilinear lookup gives $\hat D(x, y) = d_0 + g_x x + g_y y$ inside the buffer.

*Proof.* Bilinear interpolation is a convex combination of the four corner values with the weights $(1 - f_u)(1 - f_v)$, $f_u (1 - f_v)$, $(1 - f_u) f_v$ and $f_u f_v$. These weights sum to 1 and reproduce the coordinates: the weighted mean of the corner positions is $(x, y)$. An affine function of the corners therefore interpolates to the same affine function at $(x, y)$. $\square$

**Theorem 1 (sphere kernel on a plane).** Let the buffer hold a plane as in Lemma 1, read with the bilinear lookup, with $\beta = 0$. Let the kernel be made of pairs $k, -k$ with $m \cdot k \ne 0$ for $m = (g_x, g_y, 1)$. Then $A = 1/2$ at every pixel.

*Proof.* By Lemma 1, $\hat D(S_x, S_y) = d + g_x k_x + g_y k_y$, so the sample is occluded if and only if $d + g_x k_x + g_y k_y < d - k_z$, that is, $m \cdot k < 0$. Of $k$ and $-k$, exactly one has $m \cdot k < 0$. So half of the samples are occluded. $\square$

So the sphere kernel shows every plane, open or not, as half occluded. This is the gray of flat surfaces that the first form of SSAO has, and it is the reason for the normal-oriented form.

**Lemma 2 (normal of a plane).** For a plane as in Lemma 1, the central differences of the code give the unit normal $n = m / \lVert m \rVert$, which faces the camera.

*Proof.* The differences of an affine function over two pixels, divided by 2, are exactly $g_x$ and $g_y$. The surface is the zero set of $F(x, y, z) = z + d_0 + g_x x + g_y y$, whose gradient is $m$. $\square$

**Theorem 2 (hemisphere kernel on a plane).** For a plane as in Lemma 1 with any lookup that is exact on the plane, and for any kernel in the open upper half ball (tangent offsets with $k_z > 0$) rotated into the frame of $n$, $A = 1$ at every pixel for every $\beta \ge 0$.

*Proof.* The rotation keeps the length and sends the third axis to $n$, so the offset $o$ has $n \cdot o = k_z > 0$, hence $m \cdot o > 0$. As in the proof of Theorem 1, the sample is occluded only if $m \cdot o < -\beta \le 0$, which does not happen. $\square$

**Theorem 3 (what the estimate converges to).** Let the $s$ offsets be independent and uniform in the half ball of radius $R$ around $n$, with $\beta = 0$ and no range check. Let $V$ be the set of offsets $o$ of this half ball with $\hat D(P_x + o_x, P_y + o_y) < d - o_z$, the part of the half ball that lies behind the surface seen in the buffer. Then $1 - A$ is an unbiased estimate of $\lvert V \rvert / (\tfrac{2}{3} \pi R^3)$, the volume fraction of $V$, with variance at most $1 / (4 s)$.

*Proof.* Each sample is occluded with probability $\lvert V \rvert / (\tfrac{2}{3}\pi R^3)$, the measure of $V$ under the uniform distribution. $1 - A$ is the mean of $s$ independent Bernoulli variables with this mean, and a Bernoulli variable has variance at most $1/4$. $\square$

This volume fraction is not the cosine-weighted ambient occlusion integral over directions. The two agree at the ends (0 for an open plane and 1 for a closed one), and in between they are different functions of the geometry. A claim that SSAO matches ray traced ambient occlusion would be a measurement on scenes, not a consequence of this theorem.

**Theorem 4 (the wall).** Let $P$ lie on a frontal floor ($n = (0, 0, 1)$) at a distance $\delta \in [0, R]$ from the foot of an infinite wall that is nearer to the camera by $H \ge R$, with the edge on a pixel boundary and the nearest lookup. Then the volume fraction of Theorem 3 is

$$\frac{(R - \delta)^2 (2R + \delta)}{4 R^3},$$

which is $1/2$ at the foot of the wall.

*Proof.* With the nearest lookup the buffer holds the step exactly. An offset with $o_x > \delta$ projects onto the wall, whose depth is $d - H < d - o_z$ because $o_z < R \le H$, so it is behind the wall; an offset with $o_x < \delta$ projects onto the floor at depth $d > d - o_z$ and is free. $V$ is the part of the half ball with $o_x > \delta$. The ball is symmetric in $z$, so this fraction equals the fraction of the whole ball with $o_x > \delta$, a cap of height $R - \delta$ with the volume $\pi (R - \delta)^2 (3R - (R - \delta)) / 3$. Dividing by $\tfrac43 \pi R^3$ gives the formula. $\square$

The tests compare 6000 samples with this formula at pixels 1.5 to 5.5 units from the wall and find errors below 0.025. A pixel next to the edge is not tested: its central difference crosses the edge and tilts the normal.

**Theorem 5 (cost).** For $p$ pixels, $s$ samples and a blur of radius $r$, the cost is $O(p s)$ lookups and $O(p r^2)$ for the box blur.

*Proof.* Each pixel does $s$ samples of $O(1)$ work, and the blur sums $(2r + 1)^2$ values per pixel. $\square$
