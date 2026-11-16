---
title: Plane sweep stereo compares the right pixels and returns the winner-takes-all plane of its cost volume
proves: [correctness]
status: full
---

We use the pseudocode of the page. Camera 0 is $K_0 [I \mid 0]$ and camera $k$ maps a point $X$ to $X_k = R_k X + t_k$, with the intrinsic matrix $K_k$. A plane is $\Pi = \{X : n^\top X = d\}$ with $d \ne 0$. For a pixel $p = (u, v)$ we write $\tilde p = (u, v, 1)^\top$, and $a \sim b$ means $a = \lambda b$ for some $\lambda \ne 0$. All $K$ are invertible upper triangular matrices with last row $(0, 0, 1)$.

**Lemma 1 (the ray of a pixel meets the plane at the depth of line L9).** Let $m = K_0^{-1} \tilde p$ and suppose $n^\top m \ne 0$. The ray $\{s m : s > 0\}$ of $p$ meets $\Pi$ at $X = s^* m$ with $s^* = d / (n^\top m)$, and the depth of $X$ in camera 0 is $Z = s^*$.

*Proof.* $n^\top (s m) = d$ holds exactly for $s = d / (n^\top m)$. The last row of $K_0$ is $(0, 0, 1)$, so the last row of $K_0^{-1}$ is also $(0, 0, 1)$ and $m_3 = 1$. The depth of $X = s^* m$ is its third coordinate, $s^* m_3 = s^*$. $\square$

**Lemma 2 (homography).** Let $H = K_k (R_k + t_k n^\top / d) K_0^{-1}$. For every point $X \in \Pi$ with $\tilde p \sim K_0 X$, we have $H \tilde p \sim K_k (R_k X + t_k)$. So if $X$ is in front of camera $k$, $H$ maps the reference pixel of $X$ to the pixel of $X$ in camera $k$.

*Proof.* From $\tilde p \sim K_0 X$ we get $K_0^{-1} \tilde p = \lambda X$ for some $\lambda \ne 0$. Since $n^\top X = d$, we have $t_k n^\top X / d = t_k$. Then

$$H \tilde p = K_k \left(R_k + \frac{t_k n^\top}{d}\right) \lambda X = \lambda K_k \left(R_k X + t_k \frac{n^\top X}{d}\right) = \lambda K_k (R_k X + t_k).$$

The pixel of $X$ in camera $k$ is $K_k X_k$ divided by its third entry, which is the depth of $X_k$ and is positive when $X$ is in front of the camera. $\square$

**Corollary.** In lines L3 to L5 for plane $j$, the sample $I_k(H_k \tilde p)$ is the value of image $k$ at the projection of the point $X_j(p)$ where the ray of $p$ meets plane $j$ (by Lemmas 1 and 2, with $\lambda = 1 / s^*$). So $e_j(p)$ is the mean absolute difference between $I_0(p)$ and the values that the cameras which see $X_j(p)$ inside their images record there. Line L9 returns the depth of $X_{index[p]}(p)$ by Lemma 1.

The code checks the sign of the third entry of $H_k \tilde p$. With $d > 0$ and $n^\top m > 0$, the factor $\lambda = n^\top m / d$ is positive, so this sign is the sign of the depth of $X_j(p)$ in camera $k$, and points behind camera $k$ are skipped.

**Lemma 3 (window sums).** Line L6 sets $S(p) = \sum e(q)$ over the pixels $q$ of the window of $p$ inside the image.

*Proof.* The integral image $T[v][u] = \sum_{v' < v,\, u' < u} e(v', u')$ is built row by row with $T[v+1][u+1] = T[v][u+1] + \sum_{u' \le u} e(v, u')$, which is the definition. For the window rows $[v_0, v_1)$ and columns $[u_0, u_1)$ cut at the border, inclusion and exclusion give $\sum = T[v_1][u_1] - T[v_0][u_1] - T[v_1][u_0] + T[v_0][u_0]$. $\square$

**Lemma 4 (invariant of lines L2 to L8).** After the iteration for plane $j$, for every pixel $p$: $best[p] = \min_{i \le j} S_i(p)$, and $index[p]$ is the least $i \le j$ with $S_i(p) = best[p]$.

*Proof.* By induction on $j$. Before the first iteration $best[p] = \infty$, which is the minimum over the empty set. Suppose the claim holds after plane $j - 1$. If $S_j(p) < best[p]$, line L8 sets $best[p] = S_j(p)$, which is now the strict minimum, and $index[p] = j$ is the only index that reaches it. Otherwise $S_j(p) \ge \min_{i < j} S_i(p)$, so the minimum does not change, and the least index that reaches it is still the old one, since $j$ is larger. $\square$

**Theorem.** PLANE-SWEEP returns, for every pixel $p$, the least index $j^*$ that minimizes the window cost $S_j(p)$ over all planes, and the depth at which the ray of $p$ meets plane $j^*$. The cost $S_j(p)$ is the window sum of the mean absolute differences between the reference and the cameras that see the point where the ray of each window pixel meets plane $j$.

*Proof.* Lemma 4 with $j = D$ gives the index, Lemma 3 and the corollary give the meaning of $S_j$, and Lemma 1 gives the depth. $\blacksquare$

**What is not proved.** The theorem is about the cost, not the scene. The minimum of $S_j(p)$ lies at the true depth only when the surface is Lambertian and textured near $p$, when all cameras used see it, when the surface is close to the swept plane over the whole window, and when a plane passes near the true depth. None of these holds everywhere in real images, so plane sweep is an estimator and has no error bound in general.
