---
title: Newton point inversion stops at a first order point, never raises the distance, and converges quadratically near a nondegenerate foot point
proves: [correctness]
status: full
---

Let $r : \Omega \to \mathbb{R}^3$ be a regular patch of class $C^3$ on the box $\Omega = [0, 1]^2$, let $p$ be a point, and let $D(u, v) = |r(u, v) - p|^2$. Write $x = (u, v)$, $w = r - p$, $f = w \cdot r_u$ and $g = w \cdot r_v$, so that $\nabla D = 2 (f, g)$. Let $H(x)$ be half the Hessian of $D$, the matrix of line L6, and let $\mathrm{I}(x)$ be the first fundamental form. The proof uses exact arithmetic. The implementation accepts a step shorter than $10^{-6} (1 + |w|)$ in space without the test of line L8, to stop rounding from blocking the last Newton steps; that device changes nothing below.

Call $x$ a *first order point* if the conditions of the box hold: for each parameter, either its derivative ($f$ for $u$, $g$ for $v$) is zero, or the parameter is on an edge and its derivative points out of the box ($u = 0$ and $f > 0$, or $u = 1$ and $f < 0$, and the same for $v$ with $g$). Every local minimum of $D$ on $\Omega$ is a first order point, by the proof on the [problem page](/point-projection-onto-a-surface/).

**Claim 1 (what is returned).** A point returned at line L5 is a first order point up to the tolerance: each derivative that is not frozen satisfies $|f| \le \varepsilon_2 |w| |r_u|$, that is, the cosine of the angle between $w$ and $r_u$ is at most $\varepsilon_2$, and the same for $g$. A point returned at line L4 is within $\varepsilon_1$ of $p$.

*Proof.* These are the tests of lines L4 and L5. $\square$

**Claim 2 (descent).** If $x$ is not a first order point, the direction $\delta$ of line L7 satisfies $\nabla D(x) \cdot \delta < 0$, and a step of length $\lambda |\delta|$ along $\delta$ stays in $\Omega$ for all small $\lambda > 0$. So the halving loop of line L8 ends with $D(x') < D(x)$.

*Proof.* Let $F$ be the set of parameters that are not frozen. A frozen parameter has its component of $\delta$ set to $0$. On $F$, the direction is $-A^{-1} \nabla_F$ for a positive definite matrix $A$: the Hessian block when it is positive definite, otherwise the block of $\mathrm{I}$, which is positive definite because $r$ is regular. Then $\nabla_F \cdot \delta = -\nabla_F^\top A^{-1} \nabla_F < 0$ unless $\nabla_F = 0$. A component that points out of the box at a parameter on an edge is set to zero next. If the result still has $\nabla \cdot \delta < 0$, it is kept. Otherwise the code takes the fallback $\delta = (-f / E, -g / G)$ on $F$, with $E, G > 0$, for which $\nabla \cdot \delta = -2 (f^2 / E + g^2 / G) < 0$ unless $f = g = 0$ on $F$, which, with the frozen parameters, makes $x$ a first order point. The fallback never points out of the box: a parameter on an edge whose derivative points into the box is not frozen, and then $-f / E$ points into the box as well. For small $\lambda$ no component is clamped, so $D(x + \lambda \delta) = D(x) + \lambda \nabla D \cdot \delta + O(\lambda^2) < D(x)$, and halving reaches such a $\lambda$. $\square$

**Claim 3 (no increase).** The values of $D$ at the iterates do not increase, and the returned point has $D$ no larger than at the best sample of the start grid.

*Proof.* Line L8 accepts a new point only if $D$ does not increase, and by Claim 2 it finds one unless $x$ is a first order point, in which case line L5 has already returned. $\square$

**Claim 4 (local quadratic convergence).** Let $x^*$ be an interior point with $f = g = 0$ at which $H(x^*)$ is positive definite. By the second order test on the problem page, this holds exactly when $1 - t k_1 > 0$ and $1 - t k_2 > 0$, where $p = r(x^*) + t N$ and $k_1, k_2$ are the principal curvatures, that is, when $x^*$ is a strict local minimum and $p$ is not on the focal surface. Then there are $\rho > 0$ and $C$ such that from every $x_0$ with $|x_0 - x^*| \le \rho$ the iterates take full Newton steps, stay in the ball, and satisfy

$$|x_{k+1} - x^*| \le C |x_k - x^*|^2.$$

*Proof.* Put $\Phi(x) = (f, g)$, so $\Phi' = H$. Since $r \in C^3$, $H$ is Lipschitz near $x^*$ with some constant $\gamma$. Choose $\rho_0$ so that the closed ball $B$ of radius $\rho_0$ about $x^*$ lies inside $\Omega$, and so that on $B$ the matrix $H$ is positive definite with $|H(x)^{-1}| \le 2 \beta$, where $\beta = |H(x^*)^{-1}|$. This is possible by continuity. On $B$ no parameter is on an edge, so nothing is frozen, and line L7 takes the Newton step $\delta = -H(x)^{-1} \Phi(x)$. With $e = x - x^*$ and $\Phi(x^*) = 0$,

$$x + \delta - x^* = H(x)^{-1} \big( H(x) e - (\Phi(x) - \Phi(x^*)) \big).$$

By the fundamental theorem of calculus, $\Phi(x) - \Phi(x^*) = \int_0^1 H(x^* + s e) e \, ds$, so the bracket has norm at most $\int_0^1 \gamma (1 - s) |e|^2 ds = \frac{\gamma}{2} |e|^2$. Hence $|x + \delta - x^*| \le \beta \gamma |e|^2$. Put $C = \beta \gamma$.

It remains to show that line L8 accepts the full step. By Taylor's theorem and the positive definiteness of $H(x^*)$, there are $0 < \mu \le M$ and $\rho_1 \le \rho_0$ with $\mu |e|^2 \le D(x) - D(x^*) \le M |e|^2$ for $|e| \le \rho_1$. Take $\rho = \min(\rho_1, \frac{1}{2C}, \sqrt{\mu / M} / C)$. For $|e| \le \rho$ the full step gives $|e'| \le C |e|^2 \le |e| / 2$, so the new point is in the ball, and

$$D(x + \delta) - D(x^*) \le M C^2 |e|^4 \le \mu |e|^2 \le D(x) - D(x^*),$$

because $C^2 |e|^2 \le \mu / M$. So $D$ does not increase, line L8 keeps $\lambda = 1$, and induction on $k$ gives the claim. $\square$

The constants $\beta$, $\gamma$, $\mu$ and $M$ are not computed by the method. The [Kantorovich theorem](/kantorovich-theorem/) gives a test with constants that can be computed at the start point and that proves a Newton sequence converges, which certified versions use.

**Claim 5 (when the start grid is dense enough).** Let $x^*$ be the global minimizer and assume it satisfies Claim 4 with radius $\rho$. Let $\Lambda$ bound $|\nabla D|$ on $\Omega$ and let $\eta > 0$ be such that every $x \in \Omega$ with $D(x) \le D(x^*) + \eta$ lies within $\rho$ of $x^*$. If the grid spacing $h = 1/n$ satisfies $\Lambda h / \sqrt 2 \le \eta$, the method converges to $x^*$.

*Proof.* Some grid point $y$ lies within half a diagonal of a grid cell, $h / \sqrt 2$, of $x^*$. By the mean value theorem $D(y) \le D(x^*) + \Lambda h / \sqrt 2 \le D(x^*) + \eta$. The best sample $x_0$ has $D(x_0) \le D(y)$, so $|x_0 - x^*| \le \rho$, and Claim 4 applies. $\square$

$\Lambda$ can be bounded from the control net, since $|\nabla D| \le 2 |w| \sqrt{|r_u|^2 + |r_v|^2}$ and the derivative nets bound $r_u$ and $r_v$ by the [convex hull property](/convex-hull-property/). But $\eta$ depends on how close the second best local minimum comes to the global one, and no cheap bound for it is known, so Claim 5 explains when the method works and does not give a grid size in advance. $\blacksquare$
