---
title: Each outer loop of incremental 4D-Var is a Gauss-Newton step, exact in one loop for a linear model
proves: [correctness, termination]
status: full
---

**Setting.** The full model steps $M_k$ are differentiable, the trajectory from $x_0$ is $x_k = M_{0 \to k}(x_0)$, and $T$ is the set of times with observations $y_k$, linear operators $H_k$ and symmetric positive definite $R_k$. $B$ is symmetric positive definite. The full cost is

$$J(x_0) = \tfrac12 (x_0 - x^b)^\top B^{-1}(x_0 - x^b) + \sum_{k \in T} \tfrac12 d_k^\top R_k^{-1} d_k, \qquad d_k = y_k - H_k M_{0 \to k}(x_0).$$

In one outer loop, lines L3 and L4 give the trajectory $x_k$ and the departures $d_k$ at the current $x_0$. Let $L_k$ be the linear inner model from time $0$ to time $k$ along this trajectory: the product of the linear steps of `tangent` from step 1 to step $k$. If the inner model is the exact tangent linear model, $L_k = M'_{0 \to k}(x_0)$, the Jacobian of $M_{0 \to k}$ at $x_0$.

**Lemma 1 (the sweeps).** The forward sweep returns $L_k\,\delta x_0$ for every $k$, and the backward sweep with forcings $f_k$ returns $\sum_k L_k^\top f_k$, provided each `adjoint` step is the transpose of the matching `tangent` step.

*Proof.* The forward claim is the definition of $L_k$. For the backward claim, the same induction as on the [4D-Var proof page](/four-dimensional-variational-assimilation/) shows that after the forcing at time $k$, $\lambda = \sum_{j \ge k} (\text{steps } k + 1 \text{ to } j)^\top f_j$; at $k = 0$ this is $\sum_j L_j^\top f_j$. $\square$

**Lemma 2 (the inner problem).** Line L6 applies the matrix $A = B^{-1} + \sum_{k \in T} L_k^\top H_k^\top R_k^{-1} H_k L_k$, which is symmetric positive definite. Line L5 gives $b = -B^{-1}(x_0 - x^b) + \sum_{k \in T} L_k^\top H_k^\top R_k^{-1} d_k$. The solution $\delta x_0 = A^{-1} b$ of line L7 is the unique minimizer of the inner quadratic cost

$$\tilde J(\delta x_0) = \tfrac12 (x_0 + \delta x_0 - x^b)^\top B^{-1}(x_0 + \delta x_0 - x^b) + \sum_{k \in T} \tfrac12 (d_k - H_k L_k \delta x_0)^\top R_k^{-1}(d_k - H_k L_k \delta x_0).$$

*Proof.* The formulas for $A$ and $b$ follow from Lemma 1. $A$ is symmetric, and $v^\top A v \ge v^\top B^{-1} v > 0$ for $v \ne 0$. The gradient of $\tilde J$ is $A\,\delta x_0 - b$ and its Hessian is $A$, so $\tilde J$ is strictly convex with the single stationary point $A^{-1} b$. $\square$

**Theorem 3 (Gauss-Newton).** With the exact tangent linear model, $b = -\nabla J(x_0)$ and line L8 is one Gauss-Newton step for $J$, seen as the least squares problem with the residuals $B^{-1/2}(x_0 - x^b)$ and $R_k^{-1/2} d_k$.

*Proof.* By the chain rule the Jacobian of $d_k$ with respect to $x_0$ is $-H_k M'_{0 \to k}(x_0) = -H_k L_k$. The gradient of $J$ is then $B^{-1}(x_0 - x^b) - \sum_k L_k^\top H_k^\top R_k^{-1} d_k = -b$, and the Gauss-Newton matrix, the product of the transposed Jacobian of the weighted residuals with itself, is $A$. The Gauss-Newton step solves $A\,\delta x_0 = -\nabla J$, which is line L7. $\square$

So the outer iteration has the convergence properties of the [Gauss-Newton algorithm](/gauss-newton-algorithm/) (Lawless, Gratton and Nichols 2005): a step is a descent direction for $J$, since $\nabla J^\top \delta x_0 = -b^\top A^{-1} b < 0$ for $b \ne 0$; the convergence near a minimum with small residuals is fast, and with large residuals it is in general only linear.

**Corollary 4 (linear model).** If every $M_k$ is linear, the first outer loop, with an exact inner solve, returns the 4D-Var minimizer, and the second outer loop gives $\delta x_0 = 0$.

*Proof.* For a linear model $L_k = M_{0 \to k}$ at every point, so $\tilde J(\delta x_0) = J(x_0 + \delta x_0)$ and Lemma 2 says that line L8 moves to the minimizer of $J$. At the minimizer $b = -\nabla J = 0$, so the next increment is zero. $\square$

The theorem on the 4D-Var page then gives that, for a linear model and Gaussian errors, this point is the posterior mean of $x_0$, and its trajectory is the Kalman smoother mean (with $Q = 0$). The tests check the first outer loop against a separate Kalman filter and smoother to $10^{-8}$.

**Proposition 5 (an inexact inner model).** If the inner model is not the tangent linear model, a fixed point of the outer loop satisfies $B^{-1}(x_0 - x^b) = \sum_k L_k^\top H_k^\top R_k^{-1} d_k$, which is in general not $\nabla J(x_0) = 0$.

*Proof.* A fixed point has $\delta x_0 = 0$, so $b = 0$ because $A$ is invertible. The equation $b = 0$ has $L_k$ in place of $M'_{0 \to k}(x_0)$. The two equations agree when all $d_k = 0$, or when $\sum_k (L_k - M'_{0 \to k})^\top H_k^\top R_k^{-1} d_k = 0$ for another reason, and they differ in general. $\square$

This is the point of Lawless, Gratton and Nichols (2005): a simplified or lower resolution inner model changes the solution, not only the speed. The test with the tangent linear model scaled by 0.9 shows it.

**Termination.** The conjugate gradient method of line L7 stops after at most $2n$ steps, and the outer loop runs at most `max_outer` times, so the algorithm always returns.

**Summary.** Each outer loop minimizes exactly a quadratic cost built from the full model departures and the inner linear model. With the exact tangent linear model this is a Gauss-Newton step for the 4D-Var cost, and for a linear model the first step lands on the 4D-Var minimizer. With an inexact inner model the fixed point is in general not a stationary point of the full cost. $\blacksquare$
