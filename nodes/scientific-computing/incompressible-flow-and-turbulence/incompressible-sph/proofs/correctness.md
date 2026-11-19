---
title: The ISPH pressure system is solvable, and the step conserves momentum
proves: [correctness]
status: full
---

We use the notation of the page and of the implementation. There are $N$ particles in a periodic square box, each with volume $V$ and density $\rho_0 = 1$. A pair $(i, j)$ is a pair of particles with $0 < r_{ij} < 2h$, where $x_{ij} = x_i - x_j$ is taken with the minimum image and $r_{ij} = |x_{ij}|$. For a pair, $\nabla_iW_{ij} = W'(r_{ij})\,x_{ij}/r_{ij}$, so $x_{ij} \cdot \nabla_iW_{ij} = r_{ij}W'(r_{ij})$ and $\nabla_jW_{ji} = -\nabla_iW_{ij}$. The operators are

$$(G\phi)_i = \sum_j V(\phi_i + \phi_j)\nabla_iW_{ij}, \qquad (Dv)_i = -\sum_j V\,v_{ij} \cdot \nabla_iW_{ij}, \qquad (L\phi)_i = -\sum_j c_{ij}(\phi_i - \phi_j),$$

with $c_{ij} = -2Vr_{ij}W'(r_{ij})/(r_{ij}^2 + \eta^2)$, $\eta^2 = 0.01h^2$, and the viscous acceleration $a_i = \sum_j \nu\,b_{ij}\,v_{ij}$ with $b_{ij} = -c_{ij}$. We claim, in exact arithmetic:

1. The matrix $A = -L$ is symmetric and positive semidefinite. If the graph of pairs is connected, its null space is the constant vectors, and the system $A\phi = b$ with $b = \overline{Dv^*} - Dv^*$ (where the bar is the mean over particles) has a solution. Conjugate gradients started from $\phi = 0$ stays in the space of vectors with zero mean and reaches the unique zero-mean solution in at most $N - 1$ iterations.
2. Each step changes the total momentum $P = V\sum_i v_i$ by exactly $NV\Delta t\,g$. With $g = 0$ the total momentum is constant.
3. The viscous term never adds kinetic energy: $\sum_i v_i \cdot a_i \le 0$.
4. A uniform flow $v_i = U$ for all $i$ stays uniform: after one step every particle has velocity $U + \Delta t\,g$ and has moved by $\Delta t\,U + \frac12\Delta t^2g$.

**The sign of the weights.** For the cubic spline, $W'(r) = \sigma h^{-3}q(-3 + \frac94q)$ for $q = r/h < 1$, which is negative for $0 < q < \frac43$, and $W'(r) = -\frac34\sigma h^{-3}(2 - q)^2 < 0$ for $1 \le q < 2$. So $W' < 0$ on $(0, 2h)$ and $c_{ij} > 0$ for every pair. The weight $c_{ij}$ depends only on $r_{ij}$, so $c_{ij} = c_{ji}$.

**Claim 1.** The matrix has $A_{ii} = \sum_j c_{ij}$ and $A_{ij} = -c_{ij}$ for a pair, and 0 otherwise. It is symmetric because $c_{ij} = c_{ji}$. For any vector $\phi$, grouping the terms by pairs gives

$$\phi^TA\phi = \sum_{\text{pairs } i < j} c_{ij}(\phi_i - \phi_j)^2 \ge 0.$$

So $A$ is positive semidefinite. If $\phi^TA\phi = 0$, then $\phi_i = \phi_j$ for every pair, because each $c_{ij} > 0$; if the graph of pairs is connected, $\phi$ is constant. So the null space is spanned by $\mathbf 1 = (1, \dots, 1)$. Because $A$ is symmetric, its range is the orthogonal complement of its null space, which is the set of vectors with zero sum. The vector $b$ has zero sum by construction, so $A\phi = b$ has a solution.

Let $Z$ be the space of vectors with zero sum. Every row of $A$ sums to zero, and $A$ is symmetric, so every column sums to zero too, and $\mathbf 1^TA\psi = 0$ for every $\psi$. So $A$ maps every vector into $Z$, and in particular maps $Z$ to itself. On $Z$ the form $\psi^TA\psi$ is zero only for $\psi = 0$, so $A$ restricted to $Z$ is symmetric positive definite. Conjugate gradients from $\phi_0 = 0$ builds its iterates in the Krylov space spanned by $b, Ab, A^2b, \dots$, which lies in $Z$. So it is ordinary conjugate gradients for a symmetric positive definite operator on the space $Z$ of dimension $N - 1$, and it reaches the unique solution in $Z$ in at most $N - 1$ iterations. (In floating point the iteration stops at the residual tolerance instead.)

**Claim 2.** The velocity after a step is $v'_i = v_i + \Delta t(a_i + g) - (G\phi)_i$. Sum over $i$. For the viscous term, each pair adds $\nu b_{ij}v_{ij}$ to $a_i$ and $\nu b_{ji}v_{ji} = -\nu b_{ij}v_{ij}$ to $a_j$, so $\sum_i a_i = 0$. For the gradient, each pair adds $V(\phi_i + \phi_j)\nabla_iW_{ij}$ to $(G\phi)_i$ and $V(\phi_j + \phi_i)\nabla_jW_{ji} = -V(\phi_i + \phi_j)\nabla_iW_{ij}$ to $(G\phi)_j$, so $\sum_i(G\phi)_i = 0$ for every $\phi$, whatever the solver returns. So $\sum_i v'_i = \sum_i v_i + N\Delta t\,g$, and multiplying by $V$ gives the claim. This also holds for the inexact $\phi$ of a stopped solver, and it does not need the positions of the predictor and the projection to be the same.

**Claim 3.** Group the sum by pairs:

$$\sum_i v_i \cdot a_i = \sum_{\text{pairs}} \nu b_{ij}(v_i \cdot v_{ij} - v_j \cdot v_{ij}) = \sum_{\text{pairs}} \nu b_{ij}|v_{ij}|^2 \le 0,$$

because $b_{ij} = -c_{ij} < 0$ and $\nu \ge 0$. So $\frac{d}{dt}\frac12V\sum_i|v_i|^2 = V\sum_iv_i \cdot a_i \le 0$ for the viscous part of the motion.

**Claim 4.** If $v_i = U$ for all $i$, every $v_{ij}$ is zero, so $a_i = 0$ and $v^*_i = U + \Delta t\,g$. Again every $v^*_{ij}$ is zero, so $Dv^* = 0$ and $b = 0$. Conjugate gradients returns $\phi = 0$ at once (the initial residual is zero), so $G\phi = 0$ and $v'_i = U + \Delta t\,g$. The position update gives $x'_i = x_i + \frac12\Delta t(U + U + \Delta t\,g)$. All particles move by the same vector, so their relative positions, and with them all pairs and weights, do not change, and the argument repeats at the next step.

These are exact statements about the update. They do not say that $Dv' = 0$: the projection uses the compact $L$, which is not the product $DG$, so the divergence measured by $D$ is reduced but not removed, and the page reports how large it stays. That the scheme approximates the incompressible Navier-Stokes equations is a consistency property of the SPH operators on regular particle arrangements, and it is checked by measurement on the page, not proved here. $\blacksquare$
