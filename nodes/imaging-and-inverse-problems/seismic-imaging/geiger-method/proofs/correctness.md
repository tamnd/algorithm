---
title: Each step of Geiger's method solves the linearized least-squares problem, its fixed points are the stationary points of the arrival-time misfit, it converges quadratically near an exact location, and stations on a flat surface cannot tell a source from its mirror image
proves: [correctness]
status: full
---

**Setting.** There are $n \ge 4$ stations $s_i \in \mathbb{R}^3$ with observed arrival times $T_i$, and a constant velocity $v > 0$. The model is $m = (h, t_0)$, a hypocenter $h \in \mathbb{R}^3$ and an origin time $t_0$. With $D_i(h) = |h - s_i|$, the predicted times are $\tau_i(m) = t_0 + D_i(h)/v$, the residuals are $r_i(m) = T_i - \tau_i(m)$, and the misfit is $\Phi(m) = \sum_i r_i(m)^2$. We assume $D_i(h) > 0$ for all $i$ at the points we consider, so every $\tau_i$ is smooth there. $G(m)$ is the $n \times 4$ Jacobian of $\tau$. Line L5 solves $(G^T G + \lambda I)\,\delta = G^T r$ with the damping $\lambda \ge 0$, and line L6 sets $m \leftarrow m + \delta$.

**Claim 1 (the Jacobian).** Row $i$ of $G(m)$ is $\big((h - s_i)^T/(v D_i),\ 1\big)$: the unit vector from the station to the source divided by $v$, and a $1$ for the origin time.

*Proof.* $\nabla_h |h - s_i| = (h - s_i)/|h - s_i|$ for $h \ne s_i$, and $\partial \tau_i/\partial t_0 = 1$. $\square$

**Claim 2 (one step).** If $G = G(m)$ has rank 4, line L5 with $\lambda = 0$ returns the unique $\delta$ that minimizes $\|r(m) - G\delta\|^2$, the misfit of the linearized times $\tau(m) + G\delta$. With $\lambda > 0$ it returns the unique minimizer of $\|r - G\delta\|^2 + \lambda\|\delta\|^2$, for every $G$.

*Proof.* $\|r - G\delta\|^2$ is a convex quadratic in $\delta$ with gradient $2(G^T G\delta - G^T r)$. With rank 4, $G^T G$ is positive definite, so the zero of the gradient is unique and is the minimizer. With $\lambda > 0$ the Hessian is $2(G^T G + \lambda I)$, positive definite for any $G$. $\square$

**Claim 3 (fixed points).** $\nabla\Phi(m) = -2\,G(m)^T r(m)$. So line L5 returns $\delta = 0$ if and only if $\nabla\Phi(m) = 0$, for every $\lambda \ge 0$ for which the system is solvable. A limit of the iteration at which $G$ has rank 4 (or $\lambda > 0$) is a stationary point of $\Phi$.

*Proof.* $\nabla\Phi = \sum_i 2 r_i \nabla r_i = -2\sum_i r_i \nabla\tau_i = -2G^T r$. The matrix $G^T G + \lambda I$ is invertible in the cases named, so $\delta = 0$ exactly when $G^T r = 0$. If $m_k \to m^\ast$, then $\delta_k = m_{k+1} - m_k \to 0$, and by continuity of $G$, $r$ and the inverse near $m^\ast$, $\delta(m^\ast) = 0$. $\square$

A stationary point can be a local minimum, a saddle point, or the global minimum; the claim does not say which. The code does not check that $\Phi$ decreases; the safeguards max_step and keep_below_surface are heuristics, and the tests measure that they help.

**Claim 4 (local quadratic convergence for exact data).** Let $\lambda = 0$. Suppose the data are exact for some $m^\ast$, that is $r(m^\ast) = 0$, with all $D_i(h^\ast) > 0$ and $G(m^\ast)$ of rank 4. Then there are $\varepsilon > 0$ and $K$ such that for $\|m - m^\ast\| < \varepsilon$ the step gives $\|m + \delta - m^\ast\| \le K\,\|m - m^\ast\|^2$. So the iteration started close enough converges to $m^\ast$, and the error is squared at each step, up to the factor $K$.

*Proof.* Choose $\varepsilon$ so that on the ball $B$ of radius $\varepsilon$ around $m^\ast$ all $D_i > 0$, $G$ has rank 4 and $\|(G^T G)^{-1} G^T\| \le C_1$; this is possible because these hold at $m^\ast$ and depend continuously on $m$. The second derivatives of the $\tau_i$ are bounded on $B$, so Taylor's theorem gives $\tau(m^\ast) = \tau(m) + G(m)\,e + \rho$ with $e = m^\ast - m$ and $\|\rho\| \le C_2\|e\|^2$. Since $T = \tau(m^\ast)$, $r(m) = G(m)\,e + \rho$, and line L5 gives $\delta = e + (G^T G)^{-1} G^T \rho$. The new error is $e - \delta = -(G^T G)^{-1}G^T\rho$, of norm at most $C_1 C_2 \|e\|^2$. With $K = C_1 C_2$ and $\varepsilon \le 1/(2K)$ the error halves at least at each step, so the iterates stay in $B$ and converge. $\square$

With noisy data, $r(m^\ast) \ne 0$ at the minimizer, and Gauss-Newton converges only linearly in general, at a rate that depends on the size of the residuals; it can fail when they are large. Then Claim 3 still applies.

**Claim 5 (the best origin time).** For a fixed hypocenter $h$, the $t_0$ that minimizes $\Phi$ is the mean of $T_i - D_i(h)/v$, which the function best_origin_time returns.

*Proof.* $\Phi = \sum_i (c_i - t_0)^2$ with $c_i = T_i - D_i(h)/v$, a quadratic in $t_0$ with derivative $-2\sum_i (c_i - t_0)$, which is zero at the mean. $\square$

**Claim 6 (the mirror ambiguity).** If every station has depth $0$, then $\tau(x, y, -z, t_0) = \tau(x, y, z, t_0)$, so $\Phi$ takes the same value at a source and at its mirror image above the surface. For a source at depth $z = 0$, the depth column of $G$ is zero, so $G^T G$ is singular.

*Proof.* With $s_i = (a_i, b_i, 0)$, $D_i^2 = (x - a_i)^2 + (y - b_i)^2 + z^2$ does not change when $z$ changes sign. By Claim 1 the depth entry of row $i$ is $(z - 0)/(v D_i) = 0$ at $z = 0$. $\square$

So with stations on a flat surface the data cannot decide between $z$ and $-z$, the iteration may converge to the mirror image, and replacing $z < 0$ by $-z$, as keep_below_surface does, does not change $\Phi$. In practice stations at different elevations, or a velocity that changes with depth, remove the exact symmetry, but the problem stays poorly conditioned near it.

**Claim 7 (cost).** One step costs $O(n)$: $O(n)$ for the times, the residuals and the Jacobian, $O(16 n)$ for $G^T G$ and $G^T r$, and $O(1)$ for the $4 \times 4$ solve. $k$ steps cost $O(k n)$, with $O(n)$ extra space.

*Proof.* Each of the $n$ rows needs one distance. $G^T G$ has 16 entries, each a sum of $n$ products. A dense solve of fixed size 4 costs a fixed number of operations. $\square$
