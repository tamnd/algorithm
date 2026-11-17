---
title: Each part of the stable fluids step is stable for any time step, and the advection is first order
proves: [correctness]
status: full
---

We use the MAC layout and the line numbers of the page. All statements are in exact arithmetic. A cell outside the grid is SOLID, and the walls are fixed. A face field is a value on each face, and $\|w\|_\infty$ is the largest $|w_f|$. "Stable for any $\Delta t$" means here that the output of a part is bounded by its input in a stated norm, with a bound that does not depend on $\Delta t$, $\nu$ or $\Delta x$.

**Lemma 1 (advection, lines L2 and L3).** For any velocity field, any $\Delta t$ and any field $q$, each value of ADVECT$(q)$ is a convex combination of at most four values of $q$. So a constant field stays the same, and $\min q \le \text{ADVECT}(q) \le \max q$ at every sample point.

*Proof.* Line L2 gives some point $(x_b, y_b)$, whatever the velocity and $\Delta t$. Line L3 clamps the point to the box of the sample points and returns $\sum_k \lambda_k q_k$ over four samples, with weights $(1-s)(1-t)$, $(1-s)t$, $s(1-t)$ and $st$, where $s, t \in [0, 1]$. The weights are nonnegative and sum to 1. A convex combination of equal values is that value, and it lies between the least and the largest of its terms. $\square$

The lemma holds for $u$ and $v$ separately, so $\|u\|_\infty$ and $\|v\|_\infty$ do not increase in the advection of the velocity. It does not say that the sum of $q$ is kept: semi-Lagrangian advection is not conservative.

**Lemma 2 (diffusion, line L4).** Let $L$ be the graph Laplacian of the array, $(L w)_k = \sum_{m \in N(k)} (w_k - w_m)$ over the neighbors $N(k)$ inside the array, and $\alpha = \nu \Delta t / \Delta x^2 \ge 0$. Then $I + \alpha L$ is symmetric positive definite, and the solution $w$ of $(I + \alpha L) w = q$ satisfies

1. $\sum_k w_k = \sum_k q_k$,
2. $\min q \le w_k \le \max q$ for all $k$,
3. $\sum_k w_k^2 \le \sum_k q_k^2$.

*Proof.* $L$ is symmetric, and $x^T L x = \sum_{\{k, m\}} (x_k - x_m)^2 \ge 0$ over the neighbor pairs, so $x^T (I + \alpha L) x \ge x^T x > 0$ for $x \ne 0$. For claim 1, the column sums of $L$ are zero, so $\mathbf 1^T (I + \alpha L) w = \mathbf 1^T w = \mathbf 1^T q$. For claim 2, let $k$ be an index with the largest $w_k$. Then each term $w_k - w_m$ is $\ge 0$, so $q_k = w_k + \alpha \sum_{m} (w_k - w_m) \ge w_k$, and $w_k \le q_k \le \max q$. The lower bound follows in the same way at the smallest $w_k$. For claim 3, the eigenvalues of $L$ are $\mu_i \ge 0$ with an orthonormal eigenbasis, so the eigenvalues of $(I + \alpha L)^{-1}$ are $1 / (1 + \alpha \mu_i) \in (0, 1]$, and $\|w\|_2 = \|(I + \alpha L)^{-1} q\|_2 \le \|q\|_2$. $\square$

This is backward Euler on the heat equation $\partial q / \partial t = \nu \nabla^2 q$ with the 5-point Laplacian. The bounds hold for any $\alpha$, so the step size has no limit. As $\alpha \to \infty$, $w$ tends to the mean of $q$ on each connected array, which is the correct limit of the heat equation and also shows how much a large step can smooth.

**Lemma 3 (projection, lines L5 to L8).** Let $w$ be the face field after line L5, so that $w = 0$ on every face with a SOLID side. Let $p$ solve $A p = b$ with $A$ and $b$ from line L6, and let $w'$ be the field after line L8. Then $w'$ has zero divergence on every FLUID cell, and $\sum_f w_f'^2 \le \sum_f w_f^2$.

*Proof.* Call a face open if no side is SOLID and at least one side is FLUID. For a cell field $q$ with $q = 0$ on AIR cells, let $(G q)_f = (q_{\text{high}} - q_{\text{low}})/\Delta x$ on open faces, between the cells of larger and smaller index, and $(G q)_f = 0$ on the other faces. Let $(D w)_c$ be the net outflow of cell $c$ divided by $\Delta x$. Line L8 is $w' = w - \frac{\Delta t}{\rho} G p$.

*Zero divergence.* For a FLUID cell $c$, each face is open or has a SOLID side. On an open face toward the neighbor $n$, the outward flux of $G p$ is $(p_n - p_c)/\Delta x$, with $p_n = 0$ for an AIR cell. So $\Delta x^2 (D G p)_c = \sum_{n \text{ not SOLID}} (p_n - p_c) = -(A p)_c$, which is how line L6 counts the diagonal and the off-diagonal entries. Line L6 sets $b_c = -\frac{\rho \Delta x^2}{\Delta t} (D w)_c$. Then $(D w')_c = (D w)_c + \frac{\Delta t}{\rho \Delta x^2} (A p)_c = (D w)_c + \frac{\Delta t}{\rho \Delta x^2} b_c = 0$.

The system is solvable. $A$ is symmetric positive semidefinite, and its null space is spanned by the indicators of the connected FLUID regions with no AIR neighbor (the proof is on the [MAC grid](/mac-grid/) page). On such a closed region, the sum of $\Delta x (D w)_c$ is the net flow through its solid faces, which is zero after line L5, so $b$ is orthogonal to the null space. Line L7 removes the mean of $b$ on each closed region, which changes nothing in exact arithmetic, and the mean of $p$, which picks one of the solutions.

*Energy.* Let $z$ be a face field with $z = 0$ on every face with a SOLID side, and $q = \frac{\Delta t}{\rho} p$. Write $\sum_f (G q)_f z_f = \frac{1}{\Delta x} \sum_{f \text{ open}} (q_{\text{high}} - q_{\text{low}}) z_f$ and give each term to its cell. The terms of an AIR cell are zero, and the faces of a FLUID cell that are not open carry $z = 0$, so $\sum_f (G q)_f z_f = -\sum_{c \text{ FLUID}} q_c (D z)_c$. With $z = w'$, the right side is zero, so $w'$ and $G q$ are orthogonal, and $\sum_f w_f^2 = \sum_f (w'_f + (G q)_f)^2 = \sum_f w_f'^2 + \sum_f (G q)_f^2$. $\square$

**Lemma 4 (dissipation of a scalar, line L9).** For $a_s \ge 0$ and $\Delta t \ge 0$, $s \leftarrow s / (1 + \Delta t\, a_s)$ is backward Euler for $ds/dt = -a_s s$, and the factor is in $(0, 1]$.

*Proof.* Backward Euler gives $s^{n+1} = s^n - \Delta t\, a_s s^{n+1}$, so $s^{n+1} = s^n / (1 + \Delta t\, a_s)$, and $1 + \Delta t\, a_s \ge 1$. $\square$

**Theorem 1 (stability of one step).** With no force, for any $\Delta t > 0$, $\nu \ge 0$, $\kappa \ge 0$ and $a_s \ge 0$:

1. Each value of a scalar field after the step lies in $[\gamma \min s^n, \gamma \max s^n]$, where $s^n$ is the field before the step and $\gamma = 1 / (1 + \Delta t\, a_s)$.
2. The velocity after the step has zero divergence on the FLUID cells, and $\sum_f w_f^2 \le F \cdot \max(\|u^n\|_\infty, \|v^n\|_\infty)^2$, where $F$ is the number of faces.

*Proof.* Claim 1 follows from Lemma 1, Lemma 2 (claim 2) and Lemma 4, applied in this order. For claim 2, Lemma 1 bounds each component after advection by its old maximum, Lemma 2 does not increase the maximum, so after line L4 $\sum_f w_f^2 \le F \max(\|u^n\|_\infty, \|v^n\|_\infty)^2$. Line L5 only sets values to zero, and Lemma 3 does not increase $\sum_f w_f^2$ and gives zero divergence. $\square$

The bound in claim 2 does not depend on $\Delta t$ or $\nu$. That is the sense of "stable for any time step" in Stam's paper: advection takes values only from inside the old field, and the other parts are implicit or are projections. We do not claim that the velocity stays bounded uniformly over many steps with a constant independent of $F$. Lemma 1 bounds the advection in the maximum norm and Lemma 3 bounds the projection in the energy norm, and the two norms differ by up to the factor $\sqrt F$. The test file measures the energy over ten steps at a CFL number of 5 and finds that it decreases at every step.

**Theorem 2 (first order advection).** On an infinite or periodic 1D grid of spacing $\Delta x$, let the velocity be a constant $u > 0$, let $c = u \Delta t / \Delta x = m + \phi$ with an integer $m \ge 0$ and $\phi \in [0, 1)$, and let $q$ be a smooth function with $|q''| \le K$. After $N$ steps of lines L2 and L3, with $T = N \Delta t$, the error at every sample point is at most

$$\frac{T\,u\,\Delta x\,\phi (1 - \phi)}{2 c} K.$$

At a fixed CFL number $c$ with $\phi > 0$, the error is $O(\Delta x)$: the method is first order.

*Proof.* With a constant velocity, both stages of the RK2 backtrace use $u$, so line L2 is exact: the foot of sample $x_a$ is $x_a - c \Delta x$, at the distance $\phi \Delta x$ from $x_{a - m}$ and $(1 - \phi) \Delta x$ from $x_{a - m - 1}$. Line L3 is linear interpolation between these two samples. For a smooth $q$, the error of linear interpolation at a point between two nodes at distances $\theta \Delta x$ and $(1 - \theta) \Delta x$ is at most $\frac12 \theta (1 - \theta) \Delta x^2 K$; here $\theta = \phi$. Let $e^n$ be the error at step $n$ against the exact solution $q(x - u t_n)$, which has the same bound $K$ on its second derivative. One step gives $e^{n+1}_a = I(e^n)_a + \tau_a$, where $I$ is the interpolation and $|\tau_a| \le \frac12 \phi(1 - \phi) \Delta x^2 K$. $I$ is a convex combination, so $\|I(e^n)\|_\infty \le \|e^n\|_\infty$, and $\|e^N\|_\infty \le N \cdot \frac12 \phi (1 - \phi) \Delta x^2 K$. With $N = T / \Delta t = T u / (c \Delta x)$ this is the bound. $\square$

The leading term of the local error is $\frac12 \phi(1-\phi)\Delta x^2 q''$, a diffusion term. So on a bump the bound is close to the actual error: the method smooths with an effective viscosity $u\,\Delta x\,\phi(1 - \phi)/(2c)$. For $\phi = 0$ the step moves the field by whole cells and is exact. The test file moves a Gaussian bump with $\sigma = 0.1$ ($K = 1/\sigma^2 = 100$) by $0.3125$ at $c = 2.5$. For $n_x = 32$ the bound is $0.3125 \cdot (1/32) \cdot 0.25 \cdot 100 / 5 \approx 0.0488$, and the measured error is $0.0444$. The order between $n_x = 16$ and $n_x = 32$ is 1.00.

The theorem is for the interior of the domain. At an inflow border, line L3 clamps the foot to the last sample, which is a first order boundary condition.
