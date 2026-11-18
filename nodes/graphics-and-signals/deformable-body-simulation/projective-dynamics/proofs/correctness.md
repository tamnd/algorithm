---
title: Local and global steps of projective dynamics never increase the backward Euler objective, and their limit points are backward Euler steps
proves: [correctness]
status: full
---

We use the notation of the page, for 2D triangles. The free vertices have positions $\mathbf x$, the lumped mass matrix is $M$ (positive diagonal), and pinned vertices are fixed. Triangle $t$ has the weight $w_t > 0$ and a deformation gradient $F_t(\mathbf x) = \sum_{v \in t} \mathbf x_v \mathbf g_{t,v}^T$ that is linear in $\mathbf x$, with constant vectors $\mathbf g_{t,v}$ from the rest shape that satisfy $\sum_{v \in t} \mathbf g_{t,v} = 0$. Let $\mathcal R = SO(2)$ and define the surrogate

$$h(\mathbf x, R) = \frac{1}{2\Delta t^2}(\mathbf x - \mathbf y)^T M (\mathbf x - \mathbf y) + \sum_t \frac{w_t}{2} |F_t(\mathbf x) - R_t|_F^2, \qquad R = (R_t)_t \in \mathcal R^{T},$$

and the objective $g(\mathbf x) = \min_{R} h(\mathbf x, R)$, which is $\frac{1}{2\Delta t^2}|\mathbf x - \mathbf y|_M^2 + \sum_t \frac{w_t}{2}\operatorname{dist}(F_t(\mathbf x), \mathcal R)^2$. Line L5 sets $R_t$ to the rotation factor of $F_t$, and line L6 solves $L\mathbf x = \mathbf b(R)$.

## The two steps solve their subproblems exactly

**Lemma 1 (local step).** For fixed $\mathbf x$, $h(\mathbf x, \cdot)$ is minimized by taking each $R_t$ to be the rotation that maximizes $\operatorname{tr}(R_t^T F_t)$. In 2D this is $R(\theta)$ with $\theta = \operatorname{atan2}(f_{10} - f_{01}, f_{00} + f_{11})$, unique when $(f_{00} + f_{11}, f_{10} - f_{01}) \ne 0$.

*Proof.* The terms are independent, and $|F - R|_F^2 = |F|_F^2 + |R|_F^2 - 2\operatorname{tr}(R^T F) = |F|_F^2 + 2 - 2\operatorname{tr}(R^T F)$ for a rotation. With $R = R(\theta)$, $\operatorname{tr}(R^T F) = \cos\theta(f_{00} + f_{11}) + \sin\theta(f_{10} - f_{01})$, a sinusoid in $\theta$ whose maximum is at the stated angle. $\square$

**Lemma 2 (global step).** For fixed $R$, $h(\cdot, R)$ is a strictly convex quadratic in each coordinate $d \in \{x, y\}$ separately, with the Hessian

$$L = \frac{M}{\Delta t^2} + \sum_t w_t \sum_{u, v \in t} (\mathbf g_{t,u} \cdot \mathbf g_{t,v})\, \mathbf e_u \mathbf e_v^T$$

restricted to the free vertices. $L$ is the same for both coordinates, symmetric positive definite and independent of $\mathbf x$, $R$ and $\mathbf y$. The unique minimizer solves $L\mathbf x_d = \mathbf b_d$ with $\mathbf b_d = \frac{M}{\Delta t^2}\mathbf y_d + \sum_t w_t \sum_{v \in t}(R_t)_{d,:}\mathbf g_{t,v}\,\mathbf e_v - (\text{terms of pinned vertices})$.

*Proof.* Row $d$ of $F_t$ is $\sum_v x_{v,d}\mathbf g_{t,v}^T$, so $|F_t - R_t|_F^2 = \sum_d |\sum_v x_{v,d}\mathbf g_{t,v} - (R_t)_{d,:}^T|^2$, and the coordinates do not mix. Expanding the square, the quadratic part in $\mathbf x_d$ is $\frac12\mathbf x_d^T L\mathbf x_d$ with $L$ as stated, and the linear part gives $\mathbf b_d$; the pinned vertices enter only through known constants. $L$ depends only on $M$, $\Delta t$, the $w_t$ and the rest shape. The first part is positive definite and the second is a sum of Gram matrices, which are positive semidefinite, so $L$ is positive definite and the minimizer is unique. $\square$

So the code factors $L = CC^T$ once (line L1) and every global step costs two triangular solves per coordinate.

## Descent and convergence

**Theorem 3 (monotone descent).** Let $\mathbf x_{k+1}$ come from $\mathbf x_k$ by one local and one global step. Then

$$g(\mathbf x_k) - g(\mathbf x_{k+1}) \ge \tfrac12 (\mathbf x_k - \mathbf x_{k+1})^T L (\mathbf x_k - \mathbf x_{k+1}) \ge 0,$$

with $L$ applied to each coordinate.

*Proof.* Let $R^k$ be the result of the local step at $\mathbf x_k$. Then $g(\mathbf x_k) = h(\mathbf x_k, R^k)$ by Lemma 1. The function $q = h(\cdot, R^k)$ is quadratic with Hessian $L$ and minimizer $\mathbf x_{k+1}$ (Lemma 2), so $q(\mathbf x_k) - q(\mathbf x_{k+1}) = \frac12(\mathbf x_k - \mathbf x_{k+1})^T L(\mathbf x_k - \mathbf x_{k+1})$. Finally $g(\mathbf x_{k+1}) = \min_R h(\mathbf x_{k+1}, R) \le h(\mathbf x_{k+1}, R^k) = q(\mathbf x_{k+1})$. $\square$

**Lemma 4 (gradient).** At a point where every $F_t(\mathbf x)$ has a unique best rotation $R_t^*$, $g$ is differentiable and $\nabla g(\mathbf x) = \nabla_{\mathbf x} h(\mathbf x, R^*)$, that is, for a free vertex $v$, $\nabla_v g = \frac{m_v}{\Delta t^2}(\mathbf x_v - \mathbf y_v) + \sum_{t \ni v} w_t (F_t - R_t^*)\mathbf g_{t,v}$.

*Proof.* $\operatorname{dist}(F, \mathcal R)^2 = |F|_F^2 + 2 - 2\max_\theta \operatorname{tr}(R(\theta)^T F)$, and $\max_\theta \operatorname{tr}(R(\theta)^T F) = |(f_{00} + f_{11}, f_{10} - f_{01})|$ is the norm of a linear function of $F$, which is differentiable where it is not zero, with derivative $R^*$ (the unit vector of that linear function, mapped back). So $\nabla_F \frac12\operatorname{dist}(F, \mathcal R)^2 = F - R^*$, and the chain rule with $\partial F_t / \partial \mathbf x_v = (\cdot)\,\mathbf g_{t,v}^T$ gives the formula. $\square$

**Theorem 5 (limit points are backward Euler steps).** The sequence $\mathbf x_k$ is bounded, $g(\mathbf x_k)$ converges, $|\mathbf x_{k+1} - \mathbf x_k| \to 0$, and every limit point $\bar{\mathbf x}$ at which all best rotations are unique satisfies $\nabla g(\bar{\mathbf x}) = 0$, the backward Euler equation $M(\bar{\mathbf x} - \mathbf y)/\Delta t^2 = -\nabla\Psi(\bar{\mathbf x})$ for $\Psi = \sum_t \frac{w_t}{2}\operatorname{dist}(F_t, \mathcal R)^2$.

*Proof.* By Theorem 3, $g(\mathbf x_k) \le g(\mathbf x_0)$, and $g(\mathbf x) \ge \frac{1}{2\Delta t^2}|\mathbf x - \mathbf y|_M^2$, so the iterates stay in a bounded set. $g$ is bounded below by 0 and nonincreasing along the sequence, so it converges, and summing Theorem 3 gives $\sum_k |\mathbf x_k - \mathbf x_{k+1}|_L^2 \le 2g(\mathbf x_0) < \infty$, so the steps go to zero. Let $\mathbf x_{k_j} \to \bar{\mathbf x}$. Write the iteration as $\mathbf x_{k+1} = T(\mathbf x_k) = L^{-1}\mathbf b(R^*(\mathbf x_k))$. Where the best rotations are unique, $R^*$ is continuous (Lemma 1: it is the unit vector of a nonzero linear function of $F$), so $T$ is continuous at $\bar{\mathbf x}$, and $T(\bar{\mathbf x}) = \lim T(\mathbf x_{k_j}) = \lim \mathbf x_{k_j + 1} = \bar{\mathbf x}$ because the steps go to zero. A fixed point of $T$ minimizes $h(\cdot, R^*(\bar{\mathbf x}))$, so $\nabla_{\mathbf x} h(\bar{\mathbf x}, R^*(\bar{\mathbf x})) = 0$, which is $\nabla g(\bar{\mathbf x}) = 0$ by Lemma 4. $\square$

The theorem says nothing about the rate. It is linear at best, and it is slow when the triangles are stiff compared with $M/\Delta t^2$; the page measures this.

## Invariances

**Lemma 6.** $\Psi$ is zero exactly on the configurations that are rotated and moved copies of the rest shape on each triangle; in particular $\Psi(Q\mathbf X + \mathbf t) = 0$ for a rotation $Q$ and a translation $\mathbf t$ of the whole rest mesh $\mathbf X$.

*Proof.* $\operatorname{dist}(F_t, \mathcal R) = 0$ if and only if $F_t$ is a rotation. For $\mathbf x = Q\mathbf X + \mathbf t$, $F_t = Q\sum_v \mathbf X_v\mathbf g_{t,v}^T + \mathbf t\sum_v\mathbf g_{t,v}^T = Q \cdot I + 0 = Q$, since the rest shape has $F_t = I$. $\square$

**Theorem 7 (linear momentum).** With no pinned vertices and no gravity, every global step satisfies $\sum_v m_v \mathbf x_v = \sum_v m_v \mathbf y_v$, so the step keeps $\sum_v m_v \mathbf v_v$ for any number of iterations.

*Proof.* Let $\mathbf 1$ be the vector of ones. Since $\sum_{u \in t}\mathbf g_{t,u} = 0$, the second part of $L$ has $\mathbf 1^T(\cdot) = 0$, so $\mathbf 1^T L = \mathbf 1^T M/\Delta t^2$. Also $\mathbf 1^T \mathbf b_d = \mathbf 1^T M\mathbf y_d/\Delta t^2 + \sum_t w_t (R_t)_{d,:}\sum_{v \in t}\mathbf g_{t,v} = \mathbf 1^T M\mathbf y_d/\Delta t^2$. Multiplying $L\mathbf x_d = \mathbf b_d$ by $\mathbf 1^T$ gives $\mathbf 1^T M\mathbf x_d = \mathbf 1^T M\mathbf y_d$. With $\mathbf y = \mathbf x^n + \Delta t\mathbf v^n$ and line L7, $\sum m_v\mathbf v^{n+1}_v = \sum m_v(\mathbf x_v - \mathbf x^n_v)/\Delta t = \sum m_v \mathbf v^n_v$. $\square$

**Lemma 8 (free fall).** If the body is at its rest shape up to a rigid motion, has no pins and all vertices have the same velocity $\mathbf u$, one step under gravity moves every vertex to $\mathbf y_v = \mathbf x_v + \Delta t\mathbf u + \Delta t^2\mathbf g$.

*Proof.* $\mathbf y$ is a translated copy of $\mathbf x$, so $\Psi(\mathbf y) = 0$ and $g(\mathbf y) = 0$, the smallest possible value. The iteration starts at $\mathbf y$ (line L3), and by Theorem 3 with $g \ge 0$ every step satisfies $|\mathbf x_k - \mathbf x_{k+1}|_L^2 \le 0$, so it stays at $\mathbf y$. $\square$

## Cost

**Lemma 9.** With $n$ free vertices and $T$ triangles, the setup costs $O(T + n^3)$ for the dense factorization of the code, each local step $\Theta(T)$, and each global step $\Theta(T + n^2)$ for the dense triangular solves.

*Proof.* Assembling $L$ costs $O(1)$ per triangle; the dense Cholesky factorization costs $\Theta(n^3)$. A local step does one $2 \times 2$ polar decomposition per triangle. A global step assembles $\mathbf b$ in $\Theta(T)$ plus the pinned terms and does two forward and two backward substitutions with a dense $n \times n$ factor. $\square$

With a sparse factorization, as in the paper, the cost of a global step is linear in the number of nonzeros of the factor, which depends on the mesh and on the ordering.
