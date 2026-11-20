---
title: SHAKE returns positions of the constrained Verlet form that satisfy every bond, keeps the centre of mass, and converges near a solution
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. There are $N$ atoms with inverse masses $w_i = 1/m_i \ge 0$ and $C$ constraints $c = (i, j, d_c)$, each asking $\sigma_c(x) = |x_i - x_j|^2 - d_c^2 = 0$. Write $r_c = x^{\text{old}}_i - x^{\text{old}}_j$ for the bond vector at the old positions $x^n$. The constrained position Verlet method of Ryckaert, Ciccotti and Berendsen (1977) asks for $x^{n+1}$ and multipliers $\lambda$ with
$$x^{n+1} = 2x^n - x^{n-1} + h^2 W f(x^n) - h^2 W \nabla\sigma(x^n)^{\mathsf T} \lambda, \qquad \sigma(x^{n+1}) = 0,$$
where $W$ is the diagonal matrix of inverse masses. The gradient of $\sigma_c$ at $x^n$ is $2 r_c$ at atom $i$, $-2 r_c$ at atom $j$ and 0 elsewhere.

**Claim 1 (the form of the result).** At every point of the loop, $x = x^{\text{unc}} + \sum_c g_c \, W b_c$ for some numbers $g_c$, where $x^{\text{unc}}$ is the result of line L1 and $b_c$ has $r_c$ at atom $i$, $-r_c$ at atom $j$ and 0 elsewhere.

*Proof.* Line L6 adds $w_i g r_c$ to $x_i$ and subtracts $w_j g r_c$ from $x_j$, which adds $g W b_c$ to $x$. By induction over the updates, the sum of the $g$ values for each constraint is $g_c$. $\square$

Since $b_c = \frac12 \nabla \sigma_c(x^n)$, the result has the form of the constrained Verlet step with $\lambda_c = -g_c / (2h^2)$.

**Claim 2 (line L5 is a Newton step).** For one constraint $c$ with the others fixed, line L5 is one Newton step at $g = 0$ for the equation $\psi(g) = d_c^2 - |s + (w_i + w_j) g r_c|^2 = 0$, where $s = x_i - x_j$.

*Proof.* Line L6 changes $s$ to $s + (w_i + w_j) g r_c$. Then $\psi(0) = d_c^2 - |s|^2$ and $\psi'(0) = -2 (w_i + w_j) s \cdot r_c$, so the Newton step is $g = (d_c^2 - |s|^2) / \bigl(2 (w_i + w_j) s \cdot r_c\bigr)$, the formula of line L5. $\square$

The code refuses the step when $w_i + w_j = 0$ or $s \cdot r_c \le 0$, where the Newton step has no meaning. This happens when a bond has rotated by more than a right angle in one step, which a usable time step never does.

**Claim 3 (the stopping test).** If the loop returns, every constraint holds to the relative tolerance: $|d_c^2 - |x_i - x_j|^2| \le 2 \tau d_c^2$, so $\bigl| |x_i - x_j| - d_c \bigr| \le \tau d_c (1 + O(\tau))$.

*Proof.* The loop returns at line L7 only after a sweep in which line L4 found every constraint within the tolerance. In such a sweep line L6 never runs, so $x$ does not change during the sweep, and every test of line L4 applied to the final $x$. For the second form, $|a^2 - d^2| = |a - d| (a + d) \ge |a - d| d$. $\square$

With Claim 1, the returned positions solve the constrained Verlet equations up to the tolerance. Otherwise the code raises an error after `max_sweeps` sweeps, so it never returns positions that break a constraint.

**Claim 4 (the centre of mass).** If no atom is fixed, $\sum_i m_i x_i$ is the same before and after the loop.

*Proof.* Line L6 changes it by $m_i w_i g r_c - m_j w_j g r_c = g r_c - g r_c = 0$. $\square$

With position Verlet, the velocity estimate $(x^{n+1} - x^{n-1})/2h$ then keeps the total momentum when $f$ is a sum of pair forces.

**Claim 5 (local convergence).** Let $x^\star$ be a solution of the form of Claim 1, and let $J_{cd} = 2 b_c(x^\star)^{\mathsf T} W b_d$, where $b_c(x^\star)$ is built like $b_c$ from the bond vectors $x^\star_i - x^\star_j$. If the Gauss-Seidel iteration matrix of $J$ has spectral radius $\rho < 1$, then for $x^{\text{unc}}$ close enough to $x^\star$ the sweeps converge to $x^\star$, and the error falls asymptotically by the factor $\rho$ in each sweep.

*Proof.* In the variables $g$, the equations are $\Phi_c(g) = d_c^2 - |s_c(g)|^2 = 0$, and their Jacobian at the solution is $-J$. One sweep of lines L3 to L6 is a nonlinear Gauss-Seidel sweep in which each unknown gets one Newton step (Claim 2). The derivative of this sweep map at the solution is the Gauss-Seidel iteration matrix of $J$, the same as for the linear system with matrix $J$. A fixed-point map whose derivative at the fixed point has spectral radius $\rho < 1$ converges locally, with the rate $\rho$. $\square$

For a small step, $x^\star_i - x^\star_j$ is close to $r_c$, so $J$ is close to $J^0_{cd} = 2 b_c^{\mathsf T} W b_d$. $J^0$ is symmetric and positive definite when the vectors $W^{1/2} b_c$ are linearly independent, and then its Gauss-Seidel iteration matrix has spectral radius below 1, by the classical theorem on the Gauss-Seidel method. The spectral radius depends continuously on the matrix, so $\rho < 1$ for small steps. This fails, and SHAKE slows down or stops converging, when the bonds form a nearly flat ring or another nearly dependent set. The water triangle of the example needs about 4.5 sweeps for each factor of 10 in the tolerance, which shows the linear rate.

**What is not claimed.** The velocities of position Verlet are not on the tangent space of the constraints, and the method is not written in velocity form. The [RATTLE algorithm](/rattle-algorithm/) adds the velocity constraint, and it gives the same positions as SHAKE from the same two starting positions.
