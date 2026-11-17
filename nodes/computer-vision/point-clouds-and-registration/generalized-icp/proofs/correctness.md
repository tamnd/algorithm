---
title: The GICP step is well defined, never increases the fixed-weight cost, and contains point-to-point ICP
proves: [correctness]
status: full
---

We use the notation of the page. The source points are $a_1, \ldots, a_n$ with covariances $C^A_i$, and the target points are $b_1, \ldots, b_m$ with covariances $C^B_j$. All covariances are symmetric and positive semidefinite, and every $C^B_j$ is positive definite. In one iteration, line L3 gives a set $\Pi$ of pairs $(i, j)$, and line L4 gives the weights $M_{ij} = (C^B_j + R_0 C^A_i R_0^{\mathsf T})^{-1}$ at the current rotation $R_0$. For a pose $(R, t)$ let $d_{ij}(R, t) = b_j - (R a_i + t)$ and

$$G(R, t) = \sum_{(i, j) \in \Pi} d_{ij}^{\mathsf T} M_{ij}\, d_{ij} .$$

$G$ is the cost of line L5: pairs and weights fixed. The minimizer works on the motion $x \mapsto \operatorname{Exp}(w) x + u$ applied to the current moved points $x_i = R a_i + t$, with $J_i = [\,[x_i]_\times \;\; -I\,]$, the gradient $g = \sum J_i^{\mathsf T} M_{ij} d_{ij}$ and the matrix $H = \sum J_i^{\mathsf T} M_{ij} J_i$. Line L6 solves $H \delta = -g$, and line L7 tries the steps $\lambda \delta$ with $\lambda = 1, 1/2, 1/4, \ldots$ and accepts the first one that lowers $G$.

**Claim.**

1. Each weight $M_{ij}$ exists and is symmetric positive definite.
2. Line L7 accepts a step only if it lowers $G$, so $G$ never increases in line L5, and every accepted pose has $\det R = +1$.
3. If $H$ is nonsingular and $g \ne 0$, then $\delta$ is a descent direction, and a small enough $\lambda$ lowers $G$.
4. With $C^A_i = 0$ and $C^B_j = I$, $G$ is the point-to-point cost $\sum |R a_i + t - b_j|^2$, whose minimum over $SO(3) \times \mathbb{R}^3$ is the Kabsch solution for the pairs.
5. If the target is an exact rigid copy of the source and the pairs are the true ones, the true pose gives $G = 0$, which is the global minimum of $G$.

*Proof of 1.* $R_0 C^A_i R_0^{\mathsf T}$ is symmetric positive semidefinite, since $v^{\mathsf T} R_0 C^A_i R_0^{\mathsf T} v = (R_0^{\mathsf T} v)^{\mathsf T} C^A_i (R_0^{\mathsf T} v) \ge 0$. Adding the positive definite $C^B_j$ gives a symmetric positive definite matrix, which is invertible, and its inverse is symmetric positive definite. $\square$

*Proof of 2.* Line L7 replaces the pose only when the new cost $c_2$ satisfies $c_2 < G$ at the old pose. Each accepted rotation is $\operatorname{Exp}(\lambda w) R$, a product of two rotations. $\square$

*Proof of 3.* For the motion $x \mapsto \operatorname{Exp}(w) x + u$, $\operatorname{Exp}(w) x = x + w \times x + O(|w|^2)$, and $w \times x = -x \times w = -[x]_\times w$. So $d_{ij}$ changes to $d_{ij} + [x_i]_\times w - u + O(|w|^2) = d_{ij} + J_i (w, u) + O(|w|^2)$. Then $G(\lambda \delta) = G + 2 \lambda\, g^{\mathsf T} \delta + O(\lambda^2)$, where the $O$ term depends on $\delta$ and the data. $H$ is a sum of matrices $J_i^{\mathsf T} M_{ij} J_i$, which are positive semidefinite by part 1, so $H$ is positive semidefinite, and if it is nonsingular, it is positive definite. Then $g^{\mathsf T} \delta = -g^{\mathsf T} H^{-1} g < 0$ for $g \ne 0$. So $G(\lambda \delta) < G$ for every small enough $\lambda > 0$. The code tries 30 halvings; with a finite cap, it may stop at a pose that is not stationary, but by part 2 it never makes $G$ worse. $\square$

*Proof of 4.* With $C^A_i = 0$ and $C^B_j = I$, $M_{ij} = I$ for every pair and every $R_0$, so $G(R, t) = \sum |b_j - R a_i - t|^2$. This is the cost of the [optimal superposition](/optimal-superposition/) problem for the pairs, and the [Kabsch algorithm](/kabsch-algorithm/) with the sign fix gives its global minimum. In this case $G$ does not depend on $R_0$, so the outer loop of lines L2 to L8 alternates closest-point matching with a minimization of the ICP cost for the pairs, which is ICP whenever line L5 reaches the minimum. $\square$

*Proof of 5.* If $b_{j} = R^\star a_i + t^\star$ for every pair, then $d_{ij}(R^\star, t^\star) = 0$ and $G(R^\star, t^\star) = 0$. Each term of $G$ is a quadratic form of a positive definite matrix, so $G \ge 0$ everywhere. $\square$

**Theorem.** In each iteration, GENERALIZED-ICP builds positive definite weights, and its inner minimization returns a pose with a proper rotation and a fixed-weight cost no larger than at the start of the iteration; each accepted Gauss-Newton step strictly lowers that cost. With $C^A = 0$ and $C^B = I$ the cost is that of point-to-point ICP, and an exact rigid copy has the true pose as a global minimizer of the fixed-pair cost.

*Proof.* Parts 1 to 5. $\blacksquare$

**What this proof does not give.** The full GICP cost $\sum d^{\mathsf T} (C^B + R C^A R^{\mathsf T})^{-1} d$ has weights that change with $R$. The code holds them fixed within an iteration, so the full cost at the end of an iteration is not proved to be lower than at the start, and a new match can raise it as well. Segal, Haehnel and Thrun (2009) minimize the full cost with conjugate gradients and give no convergence proof. The result is local, and it needs a good start.
