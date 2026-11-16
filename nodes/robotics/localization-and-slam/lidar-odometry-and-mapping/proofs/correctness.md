---
title: The smoothness value does not depend on the scale or the rotation of the scan, a noise-free flat point has zero residual at the true motion, and the steps of the LOAM toy solve the problems that they claim to solve
proves: [correctness]
status: full
---

**Setting.** The toy of `impl/python/lidar_odometry_and_mapping.py` takes planar scans, each a list of points $X_1, \dots, X_n$ in the frame of the sensor, in the order of the beams. A pose is $T = (t_x, t_y, \theta)$, and it maps a point $p$ to $T(p) = R(\theta) p + t$. Lines L1 to L10 of the pseudocode process one scan. These claims are about the toy, not about the full LOAM system.

**Assumptions.** (A1) Exact arithmetic. (A2) No point of a scan is at the sensor, so $\|X_i\| > 0$.

**Claim 1 (the smoothness value).** Let $c_i = \|\sum_{j \in S} (X_i - X_j)\| / (|S| \, \|X_i\|)$, where $S$ holds the $k$ beams on each side of beam $i$, so $|S| = 2k$. Then:

(a) for every $\lambda > 0$ and every rotation $R$, the scan $\lambda R X_1, \dots, \lambda R X_n$ has the same values $c_i$;

(b) if $X_{i+d} = X_i + d\,v$ for $d = -k, \dots, k$ and some vector $v$ (equally spaced points on a line, centered on $X_i$), then $c_i = 0$;

(c) $c_i = \|X_i - \bar X\| / \|X_i\|$, where $\bar X$ is the mean of the $2k$ neighbors.

*Proof.* (c) $\sum_{j \in S}(X_i - X_j) = 2k X_i - \sum_{j \in S} X_j = 2k (X_i - \bar X)$, and dividing by $2k \|X_i\|$ gives the formula. (a) Both $X_i - \bar X$ and $X_i$ are multiplied by $\lambda R$, and $\|\lambda R x\| = \lambda \|x\|$, so the ratio does not change. (b) The neighbors are $X_i + d v$ for $d = \pm 1, \dots, \pm k$, and their mean is $X_i + v \sum d / (2k) = X_i$, so $c_i = 0$ by (c). $\square$

So $c_i$ measures how far $X_i$ lies from the mean of its neighbors, as a fraction of its range. It is near zero on a wall that is sampled evenly and large at a corner. Because of (a), the same thresholds work at every range. The value is not invariant under translation of the scan, but a translation of the sensor is not a valid change of a scan anyway, because the points are measured from the sensor.

**Claim 2 (the residuals and their Jacobians).** For a point $p$ and a pose $T$, let $q = T(p)$. The sharp residual is $r = q - m$ for a target point $m$. The flat residual is $r = n^\top (q - a)$ for a point $a$ on a line with unit normal $n$, and $|r|$ is the distance from $q$ to the line. The Jacobians in the code are the derivatives of these residuals with respect to $(t_x, t_y, \theta)$.

*Proof.* The distance from $q$ to the line $\{a + s d\}$ with unit direction $d$ and unit normal $n \perp d$ is the length of the component of $q - a$ along $n$, which is $|n^\top (q - a)|$. The derivative of $q$ is the identity in $(t_x, t_y)$, and in $\theta$ it is $R'(\theta) p = (-\sin\theta\, p_x - \cos\theta\, p_y,\ \cos\theta\, p_x - \sin\theta\, p_y)$, the vector `(dqx, dqy)` of the code. The chain rule gives the rows $[1, 0, \mathrm{dqx}]$ and $[0, 1, \mathrm{dqy}]$ for the sharp residual and $[n_x, n_y, n_x \mathrm{dqx} + n_y \mathrm{dqy}]$ for the flat residual. $\square$

**Claim 3 (the true motion is a zero of the flat cost on noise-free scans).** Let two scans be taken without noise from the poses $A$ and $B = A \oplus M$, so a point $p$ of the new scan is the world point $B(p)$ and a point $a$ of the old scan is $A(a)$. If a flat point $p$ of the new scan is matched to two old points $a, b$, and $B(p)$, $A(a)$ and $A(b)$ lie on one wall, then the flat residual of $p$ at the motion $M$ is zero. If this holds for every match found at $M$, then $M$ is a global minimizer of the weighted flat cost, and the Gauss-Newton loop of lines L4 to L8 stops at $M$ when it reaches it.

*Proof.* The residual is computed in the frame of the old scan. There $M(p) = A^{-1}(B(p))$, and $a$ and $b$ are $A^{-1}(A(a))$ and $A^{-1}(A(b))$. The map $A^{-1}$ is rigid, so it sends the wall to a line that holds all three points. The line through $a$ and $b$ is that line, so $M(p)$ is on it and the residual is zero. The cost is a sum of nonnegative terms $w r^2$, so a cost of zero is a global minimum. At $M$ the gradient $\sum w J^\top r$ is zero, so the step solves $H \delta = 0$ and is $\delta = 0$ when $H$ is positive definite, and the loop stops. $\square$

The same holds for the map: on noise-free data from exact poses, the map points of one wall are collinear and the fitted line is the wall, by Claim 5. A sharp point is different. The beam nearest to a corner hits the wall up to one beam spacing away from the corner, so a sharp residual at the true motion is not zero in general. The tests check the claim with flat points only.

**Claim 4 (one Gauss-Newton step).** Let the matches and the weights $w_m = \rho(d_m)$ be fixed, where $\rho(d) = (1 - (d/\tau)^2)^2$ for $|d| < \tau$ and 0 otherwise. If $H = \sum_m w_m J_m^\top J_m$ is positive definite, the step $\delta$ of line L7 is the unique minimizer of the linearized cost $\sum_m w_m \|r_m + J_m \delta\|^2$.

*Proof.* The linearized cost is a quadratic in $\delta$ with Hessian $2H$ and gradient $2(H \delta + g)$ with $g = \sum_m w_m J_m^\top r_m$. A strictly convex quadratic has one minimizer, the zero of the gradient, $\delta = -H^{-1} g$. The code accumulates $H$ and $-g$ and solves $H \delta = -g$ by Gaussian elimination with partial pivoting, which is exact in exact arithmetic for a nonsingular matrix. $\square$

This is one step of iteratively reweighted least squares with the bisquare weight. Matches with $d_m \ge \tau$ get the weight zero and do not count. The code stops with an error when fewer than three matches are left or the matrix is singular, because then the features do not fix the three degrees of freedom.

**Claim 5 (the line fit).** For points $p_1, \dots, p_m$ with mean $\mu$ and covariance $C = \frac1m \sum (p_k - \mu)(p_k - \mu)^\top$, `fit_line` returns $\mu$, a unit eigenvector $d$ of $C$ for the larger eigenvalue, and the two eigenvalues. The line $\{\mu + s d\}$ minimizes the sum of squared distances of the points to a line, and the smaller eigenvalue is zero if and only if the points are collinear.

*Proof.* With $C = \begin{pmatrix} s_{xx} & s_{xy} \\ s_{xy} & s_{yy} \end{pmatrix}$, the eigenvalues are $\frac{s_{xx} + s_{yy}}2 \pm \sqrt{(\frac{s_{xx} - s_{yy}}2)^2 + s_{xy}^2}$, which is what the code computes. The vector $(\cos\phi, \sin\phi)$ with $\phi = \frac12 \mathrm{atan2}(2 s_{xy}, s_{xx} - s_{yy})$ maximizes $d^\top C d = \frac{s_{xx} + s_{yy}}2 + \frac{s_{xx} - s_{yy}}2 \cos 2\phi + s_{xy} \sin 2\phi$, since the last two terms are the inner product of $(\cos 2\phi, \sin 2\phi)$ with $(\frac{s_{xx} - s_{yy}}2, s_{xy})$. So it is an eigenvector for the larger eigenvalue. The sum of squared distances to a line through $\mu$ with unit normal $n$ is $m\, n^\top C n$, which is smallest for $n \perp d$, and the best line passes through the mean because shifting a line along its normal adds $m$ times the square of the shift to the sum. The smaller eigenvalue is $\frac1m$ times this least sum, which is zero if and only if all points lie on the line. $\square$

**Claim 6 (the grid search).** `Grid.near(q, r)` returns the indices of exactly the points within distance $r$ of $q$, in order of distance.

*Proof.* A point is stored in the cell $(\lfloor x / h \rfloor, \lfloor y / h \rfloor)$ for the cell size $h$. If $|p_x - q_x| \le r$, then $|\lfloor p_x / h \rfloor - \lfloor q_x / h \rfloor| \le \lceil r / h \rceil$, and the same holds for $y$. So every point within distance $r$ lies in one of the cells that the search visits. The search tests the distance of each point in these cells and keeps exactly those within $r$, then sorts them. $\square$

**Claim 7 (the two rates).** After each scan, `odom_path` ends with the composition of all odometry motions, and `path` ends with the latest mapped pose composed with the odometry motions after it. The mapping step never changes the odometry motions.

*Proof.* `odom_pose` is changed only by composition with `motion` at each scan. `pose` is composed with the same motion and, at every `map_every`-th scan, replaced by the result of the scan to map step, which starts from it. The odometry step reads only the previous scan and the last motion, not `pose` or the map. $\square$

**What this does not show.** It does not show that the Gauss-Newton loop converges from a far start, or to the true motion when the matches found from the start are wrong; the motion guess must be close, which is why the last motion is used as the guess. It does not show that a sharp point matches the same corner in two scans, and the beam spacing bias of Claim 3 remains. It does not bound the drift: the mapping step removes error only where the map is older and more accurate than the odometry chain, and nothing closes a loop. The tests measure the drift on simulated scans; they do not prove a bound. It does not cover what the toy leaves out: 3D scans, the removal of motion distortion within a sweep, Levenberg-Marquardt, and the local cube of the map in LOAM.
