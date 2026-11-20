---
title: 3D-Var gives the Kalman analysis for a linear operator, and its outer loop stops only at stationary points
proves: [correctness, termination]
status: full
---

**Setting.** $B$ ($n \times n$) and $R$ ($p \times p$) are symmetric positive definite, $x^b \in \mathbb R^n$, $y^o \in \mathbb R^p$, and $h : \mathbb R^n \to \mathbb R^p$ is differentiable with the Jacobian $H(x)$. The cost is

$$J(x) = \tfrac12 (x - x^b)^\top B^{-1}(x - x^b) + \tfrac12 (y^o - h(x))^\top R^{-1}(y^o - h(x)).$$

In one outer loop at the point $x$, line L3 gives $d = y^o - h(x)$, line L4 gives $H = H(x)$, line L5 defines $A = B^{-1} + H^\top R^{-1} H$, and line L6 gives $g = B^{-1}(x - x^b) - H^\top R^{-1} d$.

**Lemma 1 (gradient).** $\nabla J(x) = g$, the vector of line L6.

*Proof.* The first term of $J$ has the gradient $B^{-1}(x - x^b)$ because $B^{-1}$ is symmetric. For the second term, the chain rule gives $-H(x)^\top R^{-1}(y^o - h(x))$. $\square$

**Lemma 2 (the inner problem).** $A$ is symmetric positive definite, and $\delta x = -A^{-1} g$ (line L7) is the unique minimizer of the quadratic

$$J_x(\delta x) = \tfrac12 (x + \delta x - x^b)^\top B^{-1}(x + \delta x - x^b) + \tfrac12 (d - H\delta x)^\top R^{-1}(d - H\delta x),$$

which is $J$ with $h$ replaced by its linearization $h(x) + H\delta x$.

*Proof.* $v^\top A v = v^\top B^{-1} v + (Hv)^\top R^{-1}(Hv) \ge v^\top B^{-1} v > 0$ for $v \ne 0$. The gradient of $J_x$ with respect to $\delta x$ is $B^{-1}(x + \delta x - x^b) - H^\top R^{-1}(d - H\delta x) = g + A\delta x$, and its Hessian is $A$. So $J_x$ is strictly convex and its only stationary point is $\delta x = -A^{-1}g$. $\square$

The conjugate gradient method of line L7 solves $A\,\delta x = -g$. In exact arithmetic it finds the solution in at most $n$ steps for a symmetric positive definite $A$ (Hestenes and Stiefel 1952). In floating point the code stops when the residual is small or after $2n$ steps.

**Termination.** Line L7 does at most $2n$ conjugate gradient steps, and the loop of line L2 runs at most `max_outer` times. Line L9 can stop it earlier. So the algorithm always returns at line L10.

**Theorem 3 (linear operator).** Let $h(x) = Hx$ with a fixed matrix $H$. Then $J$ has the unique minimizer

$$x^a = x^b + K(y^o - Hx^b), \qquad K = B H^\top (H B H^\top + R)^{-1} = (B^{-1} + H^\top R^{-1} H)^{-1} H^\top R^{-1},$$

and the first outer loop, started at $x = x^b$ (line L1) with an exact inner solve, returns $x^a$. The second outer loop gives $\delta x = 0$, so line L9 stops.

*Proof.* For a linear $h$ the linearization is exact, so $J_x(\delta x) = J(x + \delta x)$ and $J$ is strictly convex by Lemma 2. At $x = x^b$, $g = -H^\top R^{-1} d$ with $d = y^o - Hx^b$, so line L8 gives $x^b + A^{-1} H^\top R^{-1} d$, the minimizer of $J$ by Lemma 2. The identity $(B^{-1} + H^\top R^{-1} H) B H^\top = H^\top R^{-1}(H B H^\top + R)$ shows that the two forms of $K$ are equal. At the minimizer $g = \nabla J = 0$, so the next inner solve gives $\delta x = 0$. $\square$

So for a linear $H$, 3D-Var, global [optimal interpolation](/optimal-interpolation/) and the analysis step of the Kalman filter give the same $x^a$. The covariance $A^{-1} = (B^{-1} + H^\top R^{-1} H)^{-1}$ is the analysis error covariance $(I - KH)B$ (see the proof on the optimal interpolation page). If the errors are Gaussian, $J$ is the negative logarithm of the posterior density of $x$ up to a constant, so $x^a$ is the [maximum a posteriori estimate](/maximum-a-posteriori-estimation/), which for a linear $H$ is also the posterior mean.

**Theorem 4 (nonlinear operator).** For any differentiable $h$:

1. If $g \ne 0$, the increment of line L7 is a descent direction: $g^\top \delta x < 0$.
2. The increment is zero exactly when $\nabla J(x) = 0$. So if line L9 stops with $\delta x = 0$, the returned $x$ is a stationary point of $J$.

*Proof.* (1) $g^\top \delta x = -g^\top A^{-1} g < 0$ because $A^{-1}$ is positive definite. (2) $A$ is invertible, so $\delta x = -A^{-1} g = 0$ exactly when $g = 0$, and $g = \nabla J(x)$ by Lemma 1. $\square$

A stationary point of a nonconvex $J$ need not be the global minimum, and the full Gauss-Newton step can increase $J$ far from a minimum. A line search on $J$ along $\delta x$ makes each step decrease $J$; the plain method of the pseudocode uses the full step, which is the usual choice in operational incremental 3D-Var with few outer loops. Near a stationary point with zero residual $y^o - h(x)$ the convergence is quadratic, and with a nonzero residual it is in general only linear, as the measured example on the page shows.

**Summary.** The algorithm always stops. Each outer loop exactly minimizes the cost with $h$ linearized at the current point. For a linear $h$ the first outer loop returns the unique minimizer of $J$, which equals the Kalman and optimal interpolation analysis $x^b + K(y^o - Hx^b)$. For a nonlinear $h$ every increment is a descent direction, and the loop stops with a zero increment only at a stationary point of $J$. $\blacksquare$
