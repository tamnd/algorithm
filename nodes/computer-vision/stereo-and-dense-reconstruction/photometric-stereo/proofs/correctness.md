---
title: Photometric stereo recovers the albedo and normal exactly when the lit lights span space, and the least squares estimate otherwise
proves: [correctness]
status: full
---

We use the pseudocode of the page and exact real arithmetic. At one pixel the surface has albedo $\rho > 0$ and unit normal $n$, and we write $g = \rho n$. Image $k$ has a known light vector $s_k \in \mathbb{R}^3$. The image formation model is the Lambertian model with attached shadows,

$$I_k = \max(0, s_k^\top g).$$

**Lemma 1 (the shadow test).** With threshold 0, line L2 keeps reading $k$ if and only if $s_k^\top g > 0$, and then $I_k = s_k^\top g$.

*Proof.* If $s_k^\top g > 0$ then $I_k = s_k^\top g > 0$. Otherwise $I_k = 0$, which is not greater than the threshold. $\square$

**Lemma 2 (normal equations).** Let $A$ be the set of kept readings and $M = \sum_{k \in A} s_k s_k^\top$. Then $M$ is invertible if and only if the vectors $s_k$, $k \in A$, span $\mathbb{R}^3$.

*Proof.* For any $x$, $x^\top M x = \sum_{k \in A} (s_k^\top x)^2 \ge 0$, so $M$ is positive semidefinite, and $M x = 0$ implies $x^\top M x = 0$, which holds if and only if $x$ is orthogonal to every $s_k$ with $k \in A$. Such an $x \ne 0$ exists if and only if the $s_k$ do not span $\mathbb{R}^3$. $\square$

**Theorem 1 (exact recovery).** If the lights with $s_k^\top g > 0$ span $\mathbb{R}^3$, the algorithm returns $\rho$ and $n$ exactly at the pixel.

*Proof.* By Lemma 1, $A = \{k : s_k^\top g > 0\}$, and $I_k = s_k^\top g$ for $k \in A$. Spanning needs at least three vectors, so line L3 does not skip the pixel. Line L4 computes $b = \sum_{k \in A} I_k s_k = \sum_{k \in A} s_k s_k^\top g = M g$. By Lemma 2, $M$ is invertible, so line L5 returns $g$. Then $|g| = \rho |n| = \rho > 0$, and line L6 returns $\rho$ and $g / \rho = n$. $\blacksquare$

**Theorem 2 (least squares).** If $M$ is invertible, line L5 returns the unique minimizer of $E(g) = \sum_{k \in A} (I_k - s_k^\top g)^2$, for any readings.

*Proof.* $E$ is a convex quadratic with gradient $2 (M g - b)$ and Hessian $2 M$, which is positive definite by Lemma 2. Its only stationary point is $M^{-1} b$, and it is the minimum. $\square$

If the readings are $s_k^\top g$ plus independent noise with mean 0 and equal variance, this is the ordinary least squares estimate, which the Gauss-Markov theorem shows to be the best linear unbiased estimate of $g$. The albedo $|g|$ and the normal $g / |g|$ are nonlinear functions of $g$, so the theorem does not make them unbiased.

**Theorem 3 (the condition is needed).** Suppose the lit lights do not span $\mathbb{R}^3$ and $s_k^\top g \ne 0$ for every $k$. Then other vectors $g' \ne g$ give exactly the same images.

*Proof.* Take $x \ne 0$ orthogonal to every $s_k$ with $k \in A$, and let $g' = g + t x$. For $k \in A$, $s_k^\top g' = s_k^\top g > 0$. For $k \notin A$, $s_k^\top g < 0$, and for $|t|$ small enough $s_k^\top g' < 0$ too, so the reading stays 0. So $g$ and $g'$ give the same value in every image. $\square$

**Lemma 3 (unknown lights).** Let $G$ be any invertible $3 \times 3$ matrix. The pair $\bar g = G^{-\top} g$, $\bar s_k = G s_k$ gives the same images, attached shadows included.

*Proof.* $\bar g^\top \bar s_k = g^\top G^{-1} G s_k = g^\top s_k$, so both $\max(0, \cdot)$ values agree. $\square$

So if the lights are not known, images alone determine $g$ only up to an invertible matrix. If $g$ comes from a smooth height field, $g \propto (-p, -q, 1)$ with $p = z_x$ and $q = z_y$. For the generalized bas-relief matrix

$$G = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ \mu & \nu & \lambda \end{pmatrix}, \quad \lambda \ne 0,$$

we get $G^{-\top} (-p, -q, 1)^\top = (-p - \mu / \lambda, -q - \nu / \lambda, 1 / \lambda)^\top$, which is proportional to $(-(\lambda p + \mu), -(\lambda q + \nu), 1)$. This is the normal of the height field $\bar z = \lambda z + \mu x + \nu y$. So the transformed normals again come from a surface, and the images cannot tell the two surfaces apart. Belhumeur, Kriegman and Yuille show that these are the only such matrices that keep every surface integrable, and that cast shadows are also preserved; we do not prove those parts here.
