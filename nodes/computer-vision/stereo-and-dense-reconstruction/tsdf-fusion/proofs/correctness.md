---
title: TSDF fusion computes the weighted mean of the truncated distances, and its zero crossing is the weighted least squares surface along a line of sight
proves: [correctness]
status: full
---

We use the pseudocode of the page and exact real arithmetic. A voxel $x$ keeps a value $D(x)$ and a weight $W(x)$, both 0 at the start. Frame $i$ gives the voxel a reading $f_i(x)$ with weight $w_i > 0$ if lines L2 to L5 do not skip it, and no reading otherwise. Let $A(x)$ be the set of frames that give $x$ a reading.

**Lemma 1 (running weighted mean).** After any sequence of frames, $W(x) = \sum_{i \in A(x)} w_i$, and if $W(x) > 0$ then $D(x) = \sum_{i \in A(x)} w_i f_i(x) / W(x)$. In particular the result does not depend on the order of the frames.

*Proof.* By induction on the number of frames. At the start both sums are empty and $W = 0$. A frame that gives no reading changes nothing. Suppose a frame with reading $f$ and weight $w$ arrives, and before it $W = \sum w_i$ and $W D = \sum w_i f_i$ over the earlier frames in $A(x)$. This also holds when $W = 0$, since then both sides are 0. Line L7 sets $D' = (W D + w f) / (W + w) = (\sum w_i f_i + w f) / (W + w)$ and $W' = W + w$, which is the claim for the longer sequence. The two sums do not depend on the order of their terms. $\square$

**Lemma 2 (the three states of a voxel).** Let $\eta_i(x)$ be the value of line L4 for frame $i$. If $\eta_i(x) \ge \mu$, the reading is $1$. If $-\mu \le \eta_i(x) < \mu$, the reading is $\eta_i(x) / \mu \in [-1, 1)$. If $\eta_i(x) < -\mu$, there is no reading. So $D(x) \in [-1, 1]$, a voxel far in front of every observed surface has $D = 1$, and a voxel that is more than $\mu$ behind the surface in every frame keeps $W = 0$, which marks it as unseen.

*Proof.* Lines L5 and L6. A weighted mean of numbers in $[-1, 1]$ lies in $[-1, 1]$. $\square$

**Theorem (zero crossing on a line of sight).** Let voxels $a$ and $b$ be neighbors on a line with centers at positions $z_a < z_b$ along the line. Suppose that in every frame both voxels project to pixels with readings, and that the signed distance in frame $i$ is $\eta_i(z) = z_i - z$ at both centers, for a surface position $z_i$ along the line with $|z_i - z_a| \le \mu$ and $|z_i - z_b| \le \mu$. Let $\bar z = \sum w_i z_i / \sum w_i$ and assume $z_a < \bar z \le z_b$. Then the point that linear interpolation of $D$ places between $a$ and $b$ is $\bar z$, and $\bar z$ is the unique minimizer of $E(z) = \sum_i w_i (z - z_i)^2$.

*Proof.* By the assumptions and Lemma 2, every frame gives both voxels the reading $(z_i - z)/\mu$, without truncation. By Lemma 1, for $z \in \{z_a, z_b\}$,

$$D(z) = \frac{\sum_i w_i (z_i - z) / \mu}{\sum_i w_i} = \frac{\bar z - z}{\mu}.$$

So $D(z_a) > 0 \ge D(z_b)$, and the sign changes between the two voxels. The interpolated point is $z_a + s (z_b - z_a)$ with

$$s = \frac{D(z_a)}{D(z_a) - D(z_b)} = \frac{\bar z - z_a}{z_b - z_a},$$

which is $\bar z$. Finally $E'(z) = 2 \sum w_i (z - z_i)$ is zero only at $z = \bar z$, and $E'' = 2 \sum w_i > 0$. $\blacksquare$

The assumption that $\eta_i(z) = z_i - z$ at both centers holds in the setting of the test file: every frame is taken by a camera on the line, which looks along it, and $z$ is the depth. With cameras in other positions, each frame measures the distance along its own line of sight. Curless and Levoy show in their appendix that the zero set is still the weighted least squares surface when the lines of sight are nearly parallel and the weights vary slowly, and they give the full argument in Curless's thesis. We do not prove that general case here.

**What is not proved.** The theorem holds only inside the truncation band. Where a reading is truncated to 1 or skipped, $D$ is no longer linear in $z$, and the crossing moves. The value $\eta = $ depth $- Z_c$ is the distance along the line of sight, not the Euclidean distance to the surface; for a plane whose normal makes an angle $\theta$ with the line of sight, the true distance is $\eta \cos \theta$. The zero set is right in both cases, but the band is wider than $\mu$ on slanted surfaces, and readings from different directions are scaled differently.
