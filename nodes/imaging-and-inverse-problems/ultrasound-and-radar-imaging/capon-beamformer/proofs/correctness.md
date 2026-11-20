---
title: The Capon weights are the unique minimum-power distortionless weights, reduce to delay-and-sum for white noise, and null a strong interferer
proves: [correctness]
status: full
---

We prove the facts behind the main page: lines L1 to L3 (the weights) and lines L4 to L8 (one ultrasound pixel). Vectors are complex column vectors, $u^H$ is the conjugate transpose, and $\langle u, v \rangle = u^H v$ is the dot product of the helper. $R$ is an $L \times L$ Hermitian matrix and $a \ne 0$ is the steering vector.

**Theorem 1 (the optimum).** Let $R$ be Hermitian positive definite. Among all $w$ with $w^H a = 1$, the output power $w^H R w$ has the least value $1/(a^H R^{-1} a)$, and the only minimizer is

$$w^\star = \frac{R^{-1} a}{a^H R^{-1} a}.$$

*Proof.* $R$ has a Hermitian positive definite square root $R^{1/2}$. For a feasible $w$, by the Cauchy-Schwarz inequality,

$$1 = |w^H a|^2 = |(R^{1/2} w)^H (R^{-1/2} a)|^2 \le (w^H R w)\,(a^H R^{-1} a).$$

The second factor is positive because $R^{-1}$ is positive definite and $a \ne 0$, so $w^H R w \ge 1/(a^H R^{-1} a)$. Equality holds if and only if $R^{1/2} w = \beta R^{-1/2} a$ for a scalar $\beta$, that is $w = \beta R^{-1} a$. The constraint gives $\bar\beta\, a^H R^{-1} a = 1$, and since $a^H R^{-1} a$ is real, $\beta = 1/(a^H R^{-1} a)$. So $w^\star$ is the only minimizer, and its power is $1/(a^H R^{-1} a)$. $\square$

Lines L2 and L3 compute $z = R^{-1} a$ and $w = z / (a^H z)$, which is $w^\star$. A Lagrange multiplier argument gives the same formula; the inequality above also shows that it is the global minimum and that it is unique. The tests check $w^H a = 1$ and compare the power with 200 random feasible weights.

**Theorem 2 (white noise gives delay-and-sum).** If $R = \sigma^2 I$, then $w^\star = a/(a^H a)$ and the least power is $\sigma^2/(a^H a)$. For a steering vector with $|a_i| = 1$, such as the all-ones vector after focusing delays, $w^\star = a/L$, the weights of delay-and-sum.

*Proof.* $R^{-1} a = a/\sigma^2$, so $w^\star = a/(a^H a)$ and $1/(a^H R^{-1} a) = \sigma^2/(a^H a)$. $\square$

**Theorem 3 (one interferer).** Let $R = I + s\, a_1 a_1^H$ with $s \ge 0$ and $|a_{1,i}| = 1$, so $a_1^H a_1 = L$. Then, with $c = a_0^H a_1$ for the look direction $a_0$,

$$(w^\star)^H a_1 = \frac{c}{(1 + L s)\, a_0^H R^{-1} a_0}, \qquad a_0^H R^{-1} a_0 = L - \frac{s |c|^2}{1 + L s}.$$

*Proof.* By the Sherman-Morrison formula, $R^{-1} = I - \frac{s\, a_1 a_1^H}{1 + L s}$, so $R^{-1} a_1 = a_1 / (1 + L s)$ and $a_0^H R^{-1} a_0 = L - s|c|^2/(1 + L s)$. Then $(w^\star)^H a_1 = a_0^H R^{-1} a_1 / (a_0^H R^{-1} a_0)$, because $R^{-1}$ is Hermitian and the denominator is real. $\square$

For $|c| < L$, the denominator stays at least $L - |c|^2/L > 0$, so the gain toward the interferer falls like $1/(L s)$ as its power $s$ grows: the Capon beamformer places a null on it. Delay-and-sum has the fixed gain $c/L$. For $L = 8$, $s = 100$ and the directions $u = 0$ and $u = 0.4$ at half-wavelength spacing, the test finds $0.000263$ against $0.2023$, and the output powers are $0.1303$ for Capon against $4.216$ for delay-and-sum.

**Theorem 4 (the ultrasound pixel).** In lines L4 to L8 the steering vector is the all-ones vector $\mathbf 1$ of length $L$, $R$ is the average of $x x^H$ over the subarrays of all snapshots, the loading is $\lambda = \delta\, \operatorname{tr}(R)/L$, and $g$ is the average of the subarrays of the centre snapshot. Then:

1. If $\delta > 0$ and the data are not all zero, $R + \lambda I$ is Hermitian positive definite, so line L2 is well defined.
2. If the centre snapshot is aligned, that is, every channel holds the same value $v$, then the output is $v$ for every $L$ and every $\delta$ for which the weights exist.
3. As $\delta \to \infty$ the output tends to $\frac{1}{L} \sum_i g_i$, a delay-and-sum with a trapezoidal taper over the $M$ channels. For $L = M$ or $L = 1$ this is the plain mean of the $M$ channels.

*Proof.* (1) Each $x x^H$ is Hermitian positive semidefinite, so $R$ is too, and $\operatorname{tr}(R) > 0$ when some sample is nonzero. Adding $\lambda I$ with $\lambda > 0$ makes every eigenvalue at least $\lambda$.

(2) Every subarray of the centre snapshot equals $v \mathbf 1$, so $g = v \mathbf 1$, and the output is $w^H g = v\, w^H \mathbf 1 = v$ by the constraint.

(3) $(R + \lambda I)^{-1} \mathbf 1 = \lambda^{-1} (I + R/\lambda)^{-1} \mathbf 1 \to \lambda^{-1} \mathbf 1$ in direction, so $w \to \mathbf 1/L$ and the output tends to $\frac{1}{L} \sum_i g_i$. Channel $k$ appears in $g_i$ for the subarrays that contain it, so its total weight is the number of such subarrays divided by $L(M - L + 1)$, which is a trapezoid in $k$. For $L = M$ there is one subarray, so the output is $\frac{1}{M} \sum_k x_k$. For $L = 1$ the weight is $w = 1$ and $g$ is the mean of the $M$ channels. $\square$

Part 2 is the distortionless property at the pixel level: an echo that the focusing delays have aligned passes with unit gain, whatever the clutter in $R$. The tests check parts 2 and 3.

**Remark (rank).** Without loading, $R$ is a sum of $K (M - L + 1)$ outer products for $K$ snapshots, so its rank is at most $K (M - L + 1)$. If this is less than $L$, $R$ is singular and line L2 fails. Spatial smoothing over subarrays raises the rank, and it also decorrelates coherent sources in the covariance (Shan, Wax and Kailath 1985); diagonal loading makes the solve well posed in every case.

**Theorem 5 (cost).** With $K$ snapshots, one pixel costs $O(K (M - L + 1) L^2)$ for line L5, $O(L^3)$ for line L2 by Gaussian elimination, and $O(M L)$ for line L7; that is $O(K M L^2 + L^3)$. An $n \times n$ image costs $n^2$ times this, and the extra space is $O(L^2)$.

*Proof.* Each outer product costs $L^2$, the solve is cubic, and the other lines are linear in their inputs. $\square$
