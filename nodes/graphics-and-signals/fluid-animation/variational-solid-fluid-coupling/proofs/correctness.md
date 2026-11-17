---
title: The pressure minimizes the kinetic energy, the matrix is semidefinite, and still water stays still
proves: [correctness]
status: full
---

We use the line numbers of the page and the notation of the code. A face $f$ has the fluid weight $w_f$, the body weight $b_f$ and the wall weight $s_f$, with $w_f + b_f + s_f = 1$. $(G p)_f = (p_r - p_l) / \Delta x$ for the cells $l$ and $r$ on the two sides of $f$, with $p = 0$ in AIR cells. $G^\mathsf{T} q$ is minus the discrete divergence of a face field $q$. $R_f$ is the row with $R_f V = $ the normal component at $f$ of the rigid velocity $V = (v_x, v_y, \omega)$: $R_f = (1, 0, -(y_f - c_y))$ on a $u$ face and $(0, 1, x_f - c_x)$ on a $v$ face. $W$ and $B$ are the diagonal matrices of the $w_f$ and the $b_f$. Let $M_g = R^\mathsf{T} B R$; the mass matrix of the body is $M = \rho_s \Delta x^2 M_g$ per unit depth.

**Lemma 1 (the energy).** For a pressure vector $p$ on the unknown cells, let $u(p) = u^* - (\Delta t / \rho) G p$ and $V(p) = V^* - (\Delta t / \rho_s) M_g^{-1} R^\mathsf{T} B G p$ (lines L6 and L7). Then

$$E(p) = \tfrac12 \rho \Delta x^2\, u(p)^\mathsf{T} W u(p) + \tfrac12 V(p)^\mathsf{T} M V(p)$$

is a convex quadratic function of $p$, and its gradient is zero exactly when $A p = r$, with $A$ and $r$ of lines L3 and L4.

*Proof.* Write $K = M_g^{-1} R^\mathsf{T} B G$. The derivative of the first term is $-\Delta t \Delta x^2 G^\mathsf{T} W u(p)$. The second term is $\tfrac12 \rho_s \Delta x^2 V(p)^\mathsf{T} M_g V(p)$, and its derivative is $-\Delta t \Delta x^2 K^\mathsf{T} M_g V(p) = -\Delta t \Delta x^2 G^\mathsf{T} B R V(p)$, because $M_g$ is symmetric. So the gradient is $-\Delta t \Delta x^2 G^\mathsf{T} (W u(p) + B R V(p))$. Expand $u(p)$ and $V(p)$:

$$G^\mathsf{T} (W u(p) + B R V(p)) = G^\mathsf{T} (W u^* + B R V^*) - \left(\frac{\Delta t}{\rho} G^\mathsf{T} W G + \frac{\Delta t}{\rho_s} G^\mathsf{T} B R M_g^{-1} R^\mathsf{T} B G\right) p = r - A p.$$

$E$ is a sum of squares of affine functions of $p$ with weights $w_f \ge 0$ and $M \succeq 0$, so it is convex. $\square$

The gradient also shows what a minimum means: $G^\mathsf{T}(W u + B R V) = 0$, the mixed velocity of fluid and body has zero divergence in every unknown cell. This is the discrete form of $\nabla \cdot \mathbf u = 0$ in the fluid and $\mathbf u \cdot \hat n = \mathbf v \cdot \hat n$ on the body. The paper (section 2) derives the same equations; its equation 6 is the case without a body, and section 3.1 adds the body.

**Theorem 1 (the matrix).** $A$ is symmetric positive semidefinite. If every connected group of unknown cells (joined by faces with $w_f > 0$) has a face with $w_f > 0$ to an AIR cell, $A$ is positive definite.

*Proof.* $A = (\Delta t / \rho) G^\mathsf{T} W G + (\Delta t / \rho_s) (R^\mathsf{T} B G)^\mathsf{T} M_g^{-1} (R^\mathsf{T} B G)$, and both terms have the form $X^\mathsf{T} D X$ with $D$ symmetric positive semidefinite ($M_g^{-1}$ is positive definite when $M_g$ is invertible, which the code checks). So $A$ is symmetric and $x^\mathsf{T} A x \ge (\Delta t / \rho) \sum_f w_f (G x)_f^2 \ge 0$. If $x^\mathsf{T} A x = 0$, then $(G x)_f = 0$ on every face with $w_f > 0$, so $x$ is constant on each group, and it is 0 on a group that has a face with $w_f > 0$ to an AIR cell, where the other value is 0. $\square$

Without AIR, constant vectors are in the null space: $G$ of a constant is zero on every face between two unknowns. The paper calls the system "symmetric positive semi-definite" for this reason. The right side is then compatible: summed over all cells of the grid, $G^\mathsf{T} q$ telescopes to the flux through the grid border, which is zero, and a cell inside the body has zero divergence of the rigid field (a constant $u$ along each row and a constant $v$ along each column). The code removes the mean of $r$ and of $p$ in this case. The test file checks on an 8 by 8 grid that $A$ is symmetric, that $A \mathbf 1 = 0$ and $x^\mathsf{T} A x \ge 0$ for 20 random $x$ without AIR, and that Cholesky has positive pivots with a row of AIR.

**Theorem 2 (the minimum).** Under the condition of Theorem 1 for definiteness, line L5 gives the unique minimizer $p$ of $E$. After lines L6 and L7, the mixed divergence is zero in every unknown cell, and $E(p) \le E(0)$: the projection does not add kinetic energy.

*Proof.* By Lemma 1 and Theorem 1, $E$ is a strictly convex quadratic, its only stationary point solves $A p = r$, and that point is its minimum. $E(0)$ is the energy of $u^*$ and $V^*$. $\square$

The test file checks $E(p) < E(0)$ and $E(p) < E(p + \delta)$ for 10 random $\delta$, with random $u^*$ and a body that moves and spins.

**Lemma 2 (cells inside the body).** Let a cell $c$ have $b_f = 1$ on its four faces. Then the column of $c$ in $R^\mathsf{T} B G$ is zero, so the pressure in $c$ does not act on the body or on the fluid.

*Proof.* The left and right $u$ faces of $c$ contribute $+R_f / \Delta x$ and $-R_f / \Delta x$ to the column. Their rows $R_f = (1, 0, -(y - c_y))$ are equal, because both faces are at the height of the center of $c$. The same holds for the two $v$ faces, which have the same $x$. $w_f = 0$ on all four faces, so $c$ does not appear in $G^\mathsf{T} W G$ either. $\square$

This is the telescoping that the paper notes after its equation 10. The code does not make such cells unknowns, and uses $p = 0$ in them.

**Theorem 3 (still water stays still).** Let the AIR cells be all cells above some row, let the walls be any level set, and let $u^* = 0$ and $v^* = -g \Delta t$ on every face with $w_f > 0$ next to a FLUID cell. Then the solution is $p = \rho g (y_a - y)$, where $y_a$ is the height of the centers of the first AIR row, and every fluid face velocity is 0 after line L6. If a body of density $\rho_s = \rho$ is also present, with $V^* = (0, -g \Delta t, 0)$, and every cell with a face $b_f > 0$ either is an unknown or has $b_f = 1$ on its four faces, then also $V = 0$.

*Proof.* For this $p$, $(G p)_f = 0$ on a $u$ face and $-\rho g$ on a $v$ face, also on a face to the first AIR row. So line L6 gives $0$ on a $u$ face and $-g \Delta t + (\Delta t / \rho) \rho g = 0$ on a $v$ face. By Lemma 2 we may give the cells inside the body the same formula without a change. Then $R^\mathsf{T} B G p = -\rho g \sum_{v\text{ faces}} b_f (0, 1, x_f - c_x)^\mathsf{T}$, which is $-\rho g$ times the second column of $M_g$, because $R_f$ has a zero second entry on $u$ faces. So $M_g^{-1} R^\mathsf{T} B G p = (0, -\rho g, 0)$, and line L7 gives $V = (0, -g \Delta t + \Delta t \rho g / \rho_s, 0) = 0$. The mixed velocity is zero, so its divergence is zero, and by Lemma 1 this $p$ is the minimizer. $\square$

The container may be round or tilted; only the face weights change, and they do not enter the argument. The paper states this result for the hydrostatic case after its equation 7, and says that a neutrally buoyant body needs the mass matrix from the same volumes. In the test file, still water in a round bowl on a 24 by 24 grid stays still to $10^{-10}$, and a disk of density $\rho$ stays at rest to $10^{-12}$.

**Theorem 4 (binary weights).** Let there be no body and no wall level set, so that $w_f = 0$ on faces that touch a SOLID cell and $w_f = 1$ elsewhere. If every group of FLUID cells touches an AIR cell, the result is that of `macgrid.project`.

*Proof.* Multiply row $i$ of $A p = r$ by $\rho \Delta x^2 / \Delta t$. It becomes $\sum_{j} (p_i - p_j) = -(\rho \Delta x^2 / \Delta t) \operatorname{div}_i$ over the neighbors $j$ that are not SOLID, with $p_j = 0$ for AIR, and the divergence uses 0 on faces that touch a SOLID cell. This is the 5-point system of `macgrid.pressure_solve` after `macgrid.set_solid_boundaries`. Both solutions are unique, and both updates subtract $(\Delta t / (\rho \Delta x))$ times the pressure difference on the same faces. $\square$

The test file checks this on a 12 by 12 grid with random SOLID cells to $10^{-10}$. (Without AIR, the helper removes the mean on each closed group and this code on all unknowns at once, so the two can differ by a constant in $p$ when there are several groups.)

**Lemma 3 (flow along a straight wall).** Let $u^*$ be a constant field $\mathbf U$, let the wall level set be linear in each cell that a wall crosses, and let $\mathbf U$ be parallel to each wall. Then $r = 0$ in every unknown cell, so $p = 0$ and the flow does not change.

*Proof.* The fluid part $P$ of a cell is a polygon. Its border is the fluid part of each face, of length $w_f \Delta x$ (exact, because the level set is linear along the face), and the pieces of wall. The flux of a constant field out of a closed polygon is zero, and $\mathbf U \cdot \hat n = 0$ on a wall piece. So $\sum_f \pm w_f \Delta x\, U_f = 0$, which is $\Delta x^2$ times the weighted divergence. $\square$

In the test file, a channel of width 0.24 at 10 and 20 degrees across a 24 by 16 grid keeps a uniform flow of speed 1 to $10^{-12}$, with the flux 0.24. The voxelized solve of the same channel gives the fluxes 0.2239 and 0.2186: the stair steps block part of the flow.
