---
title: The point-to-plane step solves the linearized problem and keeps a rotation
proves: [correctness]
status: full
---

We use the notation of the page. The source is $P = (p_1, \ldots, p_n)$, the target is $Q = \{q_1, \ldots, q_m\}$, and $\nu_j$ is the unit normal at $q_j$. In one iteration the moved points are $x_i = R p_i + t$, line L3 picks the closest target point $q_{c(i)}$ of $x_i$ and writes $y_i = q_{c(i)}$ and $n_i = \nu_{c(i)}$. The residual is $r_i = n_i \cdot (x_i - y_i)$ and the cost of line L4 is $\sum_i r_i^2$. For $w, u \in \mathbb{R}^3$ let $\operatorname{Exp}(w)$ be the rotation by the angle $|w|$ about the axis $w/|w|$ (the identity for $w = 0$), given by the Rodrigues formula. Let

$$a_i = \begin{pmatrix} x_i \times n_i \\ n_i \end{pmatrix} \in \mathbb{R}^6, \qquad A = \sum_i a_i a_i^{\mathsf T}, \qquad b = -\sum_i r_i a_i .$$

**Claim.** In each iteration, with the match $c$ fixed:

1. For the motion $x \mapsto \operatorname{Exp}(w) x + u$, the new residual is $r_i(w, u) = r_i + a_i^{\mathsf T} (w, u) + \rho_i$ with $|\rho_i| \le \tfrac12 |w|^2 |x_i|$.
2. If $A$ is nonsingular, line L5 returns the unique minimizer of the linearized cost $\ell(w, u) = \sum_i (r_i + a_i^{\mathsf T}(w, u))^2$. If $A$ is singular, the linearized cost has no unique minimizer, and the code raises an error.
3. Line L6 keeps $R \in SO(3)$, and the new moved points are exactly $\operatorname{Exp}(w) x_i + u$.
4. The returned step is zero if and only if $\sum_i r_i a_i = 0$, which is the condition that the fixed-match cost $\sum_i r_i(w, u)^2$ is stationary at $(w, u) = (0, 0)$. If every $r_i = 0$, the step is zero.

**Lemma 1 (first order expansion).** For every $x, n, y \in \mathbb{R}^3$ with $|n| = 1$ and every $w, u$,

$$n \cdot (\operatorname{Exp}(w) x + u - y) = n \cdot (x - y) + (x \times n) \cdot w + n \cdot u + \rho, \qquad |\rho| \le \tfrac12 |w|^2 |x| .$$

*Proof.* Let $\theta = |w|$. The Rodrigues formula gives $\operatorname{Exp}(w) x = x + \frac{\sin\theta}{\theta} (w \times x) + \frac{1 - \cos\theta}{\theta^2}\, w \times (w \times x)$ for $\theta > 0$. So $\operatorname{Exp}(w) x - x - w \times x = \big(\frac{\sin\theta}{\theta} - 1\big) (w \times x) + \frac{1 - \cos\theta}{\theta^2}\, w \times (w \times x)$. Let $x_\perp$ be the part of $x$ orthogonal to $w$. The two terms are orthogonal, with lengths $(1 - \frac{\sin\theta}{\theta})\, \theta |x_\perp|$ and $(1 - \cos\theta) |x_\perp|$. The square of the length of the sum is $|x_\perp|^2 \big((\theta - \sin\theta)^2 + (1 - \cos\theta)^2\big) = |x_\perp|^2 \big(\theta^2 + 2 - 2\cos\theta - 2\theta\sin\theta\big)$. The function $g(\theta) = \theta^4/4 - \theta^2 - 2 + 2\cos\theta + 2\theta\sin\theta$ has $g(0) = 0$ and $g'(\theta) = \theta^3 - 2\theta + 2\theta\cos\theta = \theta(\theta^2 - 2 + 2\cos\theta) \ge 0$, because $\cos\theta \ge 1 - \theta^2/2$. So the length is at most $\tfrac12 \theta^2 |x_\perp| \le \tfrac12 |w|^2 |x|$. Finally $n \cdot (w \times x) = w \cdot (x \times n)$ by the cyclic rule of the triple product, and $|n| = 1$ bounds the dot product of $n$ with the remainder. For $w = 0$ the remainder is 0. $\square$

*Proof of 1.* Apply Lemma 1 with $x = x_i$, $y = y_i$, $n = n_i$. $\square$

*Proof of 2.* $\ell$ is the squared length of $M z + r$, where $M$ is the $n \times 6$ matrix with rows $a_i^{\mathsf T}$, $z = (w, u)$ and $r = (r_1, \ldots, r_n)$. A vector $z$ minimizes $\ell$ if and only if it solves the [normal equations](/normal-equations/) $M^{\mathsf T} M z = -M^{\mathsf T} r$, that is $A z = b$. If $A = M^{\mathsf T} M$ is nonsingular, the solution is unique, and line L5 computes it by Gaussian elimination. If $A$ is singular, there is $z_0 \ne 0$ with $M z_0 = 0$, and $\ell(z + s z_0) = \ell(z)$ for every $s$, so no minimizer is unique. $\square$

*Proof of 3.* $\operatorname{Exp}(w)$ is a rotation, and the product of two rotations is a rotation, so $R' = \operatorname{Exp}(w) R \in SO(3)$. With $t' = \operatorname{Exp}(w) t + u$, $R' p_i + t' = \operatorname{Exp}(w)(R p_i + t) + u = \operatorname{Exp}(w) x_i + u$. $\square$

*Proof of 4.* If $A$ is nonsingular, $z = A^{-1} b$ is zero exactly when $b = 0$. The gradient of $\sum_i r_i(w, u)^2$ at $(0, 0)$ is $2 \sum_i r_i a_i$ by part 1, since the remainders $\rho_i$ are of second order in $w$. If every $r_i = 0$, then $b = 0$ and the step is zero. $\square$

**Theorem.** Each iteration of POINT-TO-PLANE-ICP takes the Gauss-Newton step of the fixed-match point-to-plane cost, parametrized by $(w, u)$ around the current pose, and applies it as an exact rigid motion. The returned $R$ is a rotation. If the loop stops by line L7 with tol $= 0$, the current pose is a stationary point of the point-to-plane cost for its closest-point match. If the source is an exact rigid copy of points of the target, so that each moved point coincides with its target point at the true pose, then the true pose gives zero residuals and a zero step, so it is a fixed point of the iteration.

*Proof.* The Jacobian of the residual vector at $(0, 0)$ has rows $a_i^{\mathsf T}$ by part 1, so the Gauss-Newton step is the minimizer of $\ell$, which line L5 computes by part 2. Part 3 gives the rotation and the exact motion. Part 4 gives the stationary point and the fixed point. At the true pose of an exact copy, each moved point is a target point, so its closest target point is itself, at distance 0, and $r_i = 0$. $\blacksquare$

**What this proof does not give.** It does not show that the cost falls in every iteration: a full Gauss-Newton step can overshoot, and the match can change. It gives no rate. Pottmann, Huang, Yang and Hu (2006) show that the method is a Gauss-Newton method for the squared distance function, with quadratic convergence for a zero-residual problem from a good start; the page cites that result and does not prove it.
