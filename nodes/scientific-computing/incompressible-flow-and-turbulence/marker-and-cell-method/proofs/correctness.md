---
title: The MAC pressure step in a closed box gives an exactly divergence-free velocity, and the MAC gradient has no checkerboard null space
proves: [correctness, termination]
status: full
---

**Setting.** The box has $n_x \times n_y = M$ cells of size $\Delta x \times \Delta y$. A face field $\mathbf{u} = (u, v)$ has $u_{i,j}$ on the vertical faces, $i = 0, \dots, n_x$, and $v_{i,j}$ on the horizontal faces, $j = 0, \dots, n_y$. Let $W$ be the face fields with zero values on the wall faces ($u_{0,j} = u_{n_x,j} = 0$ and $v_{i,0} = v_{i,n_y} = 0$); every iterate of the method is in $W$, because lines L3 and L5 change only interior faces. For a cell field $p$,

$$(D\mathbf{u})_{i,j} = \frac{u_{i+1,j} - u_{i,j}}{\Delta x} + \frac{v_{i,j+1} - v_{i,j}}{\Delta y}, \qquad (Gp)^x_{i,j} = \frac{p_{i,j} - p_{i-1,j}}{\Delta x} \ (0 < i < n_x), \qquad (Gp)^y_{i,j} = \frac{p_{i,j} - p_{i,j-1}}{\Delta y} \ (0 < j < n_y),$$

and $G$ is zero on the wall faces, so $Gp \in W$. The inner products are the plain sums $\langle \mathbf{u}, \mathbf{w}\rangle$ over faces and $(p, q)$ over cells.

**Lemma 1 (summation by parts).** For $\mathbf{u} \in W$ and every cell field $p$, $\langle \mathbf{u}, Gp\rangle = -(D\mathbf{u}, p)$.

*Proof.* Fix a row $j$. With $u_{0,j} = u_{n_x,j} = 0$,

$$\sum_{i=0}^{n_x - 1} p_{i,j}(u_{i+1,j} - u_{i,j}) = \sum_{i=1}^{n_x} p_{i-1,j}u_{i,j} - \sum_{i=0}^{n_x-1} p_{i,j}u_{i,j} = -\sum_{i=1}^{n_x - 1} u_{i,j}(p_{i,j} - p_{i-1,j}),$$

because the terms with $i = 0$ and $i = n_x$ vanish. Dividing by $\Delta x$ and summing over $j$ gives the $x$ part, and the columns give the $y$ part. $\square$

**Lemma 2 ($-DG$ is the Neumann 5-point matrix).** $A := -DG$ is the matrix of minus the 5-point Laplacian in which a missing neighbor across a wall drops out of the stencil, which is `poisson2d(..., bc="neumann")`. It is symmetric positive semidefinite, and $Ap = 0$ exactly when $Gp = 0$, exactly when $p$ is constant.

*Proof.* At an interior cell, $(DGp)_{i,j} = (p_{i+1,j} - 2p_{i,j} + p_{i-1,j})/\Delta x^2 + (\dots)/\Delta y^2$. At a cell next to the wall $i = 0$, the face $(0, j)$ carries $(Gp)^x = 0$, so the $x$ part is $(p_{1,j} - p_{0,j})/\Delta x^2$: the west neighbor drops out, which is the discrete condition $\partial p/\partial n = 0$. By Lemma 1 with $\mathbf{u} = Gq \in W$, $(Ap, q) = \langle Gp, Gq\rangle$, so $A$ is symmetric and $(Ap, p) = \|Gp\|^2 \ge 0$. If $Gp = 0$ then $p_{i,j} = p_{i-1,j}$ and $p_{i,j} = p_{i,j-1}$ across every interior face, and the cells are connected through interior faces, so $p$ is constant. $\square$

The test file checks Lemma 2 column by column in exact rational arithmetic.

**Corollary (no checkerboard mode).** The only pressures with zero MAC gradient are the constants. The checkerboard $p_{i,j} = (-1)^{i+j}$ has $|Gp| = 2/\Delta x$ or $2/\Delta y$ on every interior face, so the projection sees it and removes it. With the collocated central gradient $(p_{i+1,j} - p_{i-1,j})/(2\Delta x)$ the checkerboard has zero gradient at every interior point, and a pressure solve with that gradient cannot control it.

**Theorem (the pressure step).** Let $\mathbf{u}^* \in W$ and $b = -D\mathbf{u}^*/\Delta t$. Then $\sum b = 0$, $Ap = b$ has a solution, unique up to a constant, and $\mathbf{u} = \mathbf{u}^* - \Delta t\, Gp$ satisfies

1. $\mathbf{u} \in W$ and $D\mathbf{u} = 0$;
2. $\mathbf{u}$ is the orthogonal projection of $\mathbf{u}^*$ onto $V = \{\mathbf{w} \in W : D\mathbf{w} = 0\}$, and $\|\mathbf{u}\| \le \|\mathbf{u}^*\|$.

*Proof.* Lemma 1 with $p \equiv 1$ gives $\sum D\mathbf{u}^* = -\langle \mathbf{u}^*, G1\rangle = 0$: what enters the box leaves it, because no flow crosses the walls. $A$ is symmetric, so its range is the orthogonal complement of its null space, the constants (Lemma 2), and $b$ is in the range. Then $D\mathbf{u} = D\mathbf{u}^* + \Delta t\, Ap = 0$, and $\mathbf{u} \in W$ because $Gp \in W$. For any $\mathbf{w} \in V$, Lemma 1 gives $\langle \mathbf{w}, Gp\rangle = -(D\mathbf{w}, p) = 0$, so $\mathbf{u}^* - \mathbf{u} = \Delta t\, Gp$ is orthogonal to $V$ while $\mathbf{u} \in V$. This characterizes the orthogonal projection, and Pythagoras gives the norm bound. $\square$

This is the discrete form of the [Helmholtz-Hodge decomposition](/helmholtz-hodge-decomposition/) with the boundary condition $\mathbf{u}\cdot\mathbf{n} = 0$.

**Lemma 3 (marker interpolation).** Away from the walls (at least half a cell), the interpolated velocity is the bilinear interpolant of the four nearest unknowns of each component, so it reproduces every velocity field whose components are linear in $x$ and $y$ exactly. Each marker step is a midpoint (second order Runge-Kutta) step of $\dot{\mathbf{x}} = \mathbf{u}_h(\mathbf{x})$.

*Proof.* The weights $(1-a)(1-c)$, $a(1-c)$, $(1-a)c$ and $ac$ sum to 1 and reproduce $x$ and $y$ on a rectangle. $\square$

**Termination.** The loop runs $N$ times. Lines L2, L3, L5 and L7 cost $O(M)$ each, and line L6 costs $O(1)$ per marker. Line L4 is a CG solve of a symmetric positive semidefinite system with a right side in the range; in exact arithmetic its iterates stay in the range, where $A$ is positive definite, so it ends in at most $M - 1$ iterations, and in floating point the implementation stops at its tolerance or at $10M$ iterations.

**What is not proved here.** The order of accuracy (second order in space for smooth flow, first order in time) is measured in the tests on the free-slip Taylor-Green vortex. The no-slip ghost value $2u_{\text{wall}} - u_{\text{inner}}$ is a linear extrapolation, and the viscous term next to a no-slip wall is only first order accurate locally.
