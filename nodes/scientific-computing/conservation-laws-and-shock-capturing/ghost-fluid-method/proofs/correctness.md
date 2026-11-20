---
title: The ghost fluid step keeps contacts exactly, and the pressure discretization with jumps is exact for piecewise linear solutions and uniquely solvable
proves: [correctness, termination]
status: full
---

**Setting.** The grid has $M$ cells of width $\Delta x$, with transmissive ends (the end cells are copied into one ghost cell on each side). The single-fluid scheme in L2 is the conservative Rusanov scheme $U_i \leftarrow U_i - \lambda(F_{i+1/2} - F_{i-1/2})$, $\lambda = \Delta t/\Delta x$, with

$$F_{i+1/2} = \tfrac12\big(F(U_i) + F(U_{i+1})\big) - \tfrac12 s_{i+1/2}(U_{i+1} - U_i),$$

where $s_{i+1/2} \ge 0$ is one number for all three components. All arithmetic is exact.

**Lemma 1 (one gas keeps a contact).** Let one gas with ratio $\gamma$ have $u_i = u$ and $p_i = p$ in every cell, and any densities $\rho_i > 0$. After one Rusanov step, $u$ and $p$ are unchanged in every cell.

*Proof.* Write $G_{i+1/2}$ for the mass component of $F_{i+1/2}$. Since $\rho u$ is $u$ times $\rho$ and $\rho u^2 + p = u\cdot\rho u + p$, the momentum component is $uG_{i+1/2} + p$. Since $E = \frac{p}{\gamma - 1} + \tfrac12\rho u^2$ and $(E + p)u = \frac{\gamma pu}{\gamma - 1} + \tfrac12u^2\cdot\rho u$, the energy component is $\frac{\gamma pu}{\gamma - 1} + \tfrac12u^2G_{i+1/2}$, and the differences $U_{i+1} - U_i$ in the dissipation term give the same factors $u$ and $\tfrac12u^2$ times the density difference. So the new state is $\rho_i' = \rho_i - \lambda(G_{i+1/2} - G_{i-1/2})$, $(\rho u)_i' = u\rho_i'$, and $E_i' = \frac{p}{\gamma - 1} + \tfrac12u^2\rho_i'$, because the constant parts of the flux cancel in the difference. Hence $u_i' = u$ and $p_i' = p$. If some $\rho_i' \le 0$ the step is not defined; under the CFL condition $\lambda s \le 1$ the density update is a convex combination, so $\rho_i' > 0$. $\square$

**Lemma 2 (the level set moves exactly).** If $\phi_i = x_i - c$ and every cell velocity is $u$, then after L3, $\phi_i = x_i - c - u\Delta t$.

*Proof.* Every one-sided difference of a linear function, including the one-sided ones at the ends, equals $\Delta x$. So L3 gives $\phi_i - \lambda u\Delta x = \phi_i - u\Delta t$. $\square$

**Theorem 1 (contacts).** Let the two fluids have $u_i = u$ and $p_i = p$ everywhere, with any densities and with $\gamma_0 \ne \gamma_1$, and let $\phi$ be linear. Then after one GFM step, $u_i = u$ and $p_i = p$ in every cell, and the interface has moved by $u\Delta t$.

*Proof.* In L1, every ghost state of fluid $k$ has velocity $u$ and pressure $p$, because it copies them from the real state of its cell, and its density $(p/s)^{1/\gamma_k}$ is positive. So the array that fluid $k$ advances in L2 is one gas with ratio $\gamma_k$, uniform $u$ and $p$. By Lemma 1, all of its new states have velocity $u$ and pressure $p$ for the ratio $\gamma_k$. By Lemma 2, L3 moves the zero of $\phi$ by $u\Delta t$. L4 gives cell $i$ a state of the fluid $k$ that the new $\phi_i$ assigns, and it reads that state with the same $\gamma_k$, so it has velocity $u$ and pressure $p$. $\square$

The conservative one-fluid scheme does not have this property. Its momentum and density updates still give $u' = u$, but in a cell next to the interface the energy flux on one side is computed with $\gamma_0$ and on the other with $\gamma_1$, so the constant parts $\frac{\gamma_k pu}{\gamma_k - 1}$ do not cancel, and $p'$ differs from $p$ by $O(\lambda pu\,|\frac{\gamma_0}{\gamma_0 - 1} - \frac{\gamma_1}{\gamma_1 - 1}|)$ in that cell.

**Setting for the pressure solve.** Nodes $x_i = i\Delta x$, $i = 0, \dots, n$, with $u_0$ and $u_n$ given, the interface at $\alpha$ with $x_k \le \alpha < x_{k+1}$, $0 < k < n - 1$, and $\theta = (\alpha - x_k)/\Delta x \in [0, 1)$. The equation is $(\beta u_x)_x = f$, with $\beta = \beta^\pm > 0$ on the two sides and jumps $u(\alpha^+) - u(\alpha^-) = a$, $\beta^+u_x(\alpha^+) - \beta^-u_x(\alpha^-) = b$.

**Lemma 3 (the interface flux).** Let $w$ be a function that is linear on $[x_k, \alpha]$ and on $[\alpha, x_{k+1}]$, with values $u_k$ and $u_{k+1}$ at the nodes, and with the two jumps $a$ and $b$ at $\alpha$. Then its flux on the left side is

$$\beta^-w_x(\alpha^-) = \hat\beta\Big(\frac{u_{k+1} - u_k - a}{\Delta x} - \frac{b(1 - \theta)}{\beta^+}\Big),\qquad \beta^+w_x(\alpha^+) = \hat\beta\Big(\frac{u_{k+1} - u_k - a}{\Delta x} + \frac{b\theta}{\beta^-}\Big),$$

with $\hat\beta = \beta^+\beta^-/(\beta^+\theta + \beta^-(1 - \theta))$.

*Proof.* Let $v = w(\alpha^-)$, so $w(\alpha^+) = v + a$. The slopes are $(v - u_k)/(\theta\Delta x)$ and $(u_{k+1} - v - a)/((1 - \theta)\Delta x)$, and the flux jump condition is $\beta^+\frac{u_{k+1} - v - a}{(1 - \theta)\Delta x} - \beta^-\frac{v - u_k}{\theta\Delta x} = b$. This is one linear equation for $v$ with the positive coefficient $\frac{\beta^+}{1 - \theta} + \frac{\beta^-}{\theta}$ (for $\theta = 0$ take $v = u_k$). Solving it gives $v - u_k = \frac{\theta}{\beta^+\theta + \beta^-(1 - \theta)}\big(\beta^+(u_{k+1} - u_k - a) - b\Delta x(1 - \theta)\big)$, and multiplying by $\beta^-/(\theta\Delta x)$ gives the first formula. The second is the first plus $b$, and $b - \hat\beta b(1 - \theta)/\beta^+ = b\beta^+\theta/(\beta^+\theta + \beta^-(1 - \theta)) = \hat\beta b\theta/\beta^-$. $\square$

The rows $k$ and $k + 1$ of the discretization are the flux balances $\big(\beta^-w_x(\alpha^-) - \beta^-\frac{u_k - u_{k-1}}{\Delta x}\big)/\Delta x = f_k$ and $\big(\beta^+\frac{u_{k+2} - u_{k+1}}{\Delta x} - \beta^+w_x(\alpha^+)\big)/\Delta x = f_{k+1}$. Moving the known terms of Lemma 3 to the right side gives exactly the $\hat\beta$ face coefficient and the two right-hand side corrections on the main page.

**Theorem 2 (exactness for linear pieces).** If the exact solution $u$ is linear on $[0, \alpha)$ and on $(\alpha, 1]$ (so $f = 0$), the discrete solution equals $u$ at every node.

*Proof.* Insert the exact nodal values. In every row away from the interface, the three-point stencil of a linear function with constant $\beta$ is zero. In rows $k$ and $k + 1$ the function $w$ of Lemma 3 is the exact $u$, so $\beta^\pm w_x(\alpha^\pm)$ are the exact one-sided fluxes, which equal $\beta^-u_x$ on the left and $\beta^+u_x$ on the right. Each flux balance is then the difference of two equal fluxes, which is $0 = f$. So the exact values satisfy the system, and by Theorem 3 the system has only one solution. $\square$

**Theorem 3 (unique solution).** The matrix of the discrete system is symmetric and negative definite, so the solve has a unique solution and the Thomas algorithm runs without a zero pivot.

*Proof.* Every row has the form $(c_{i+1/2}(u_{i+1} - u_i) - c_{i-1/2}(u_i - u_{i-1}))/\Delta x^2$ with face coefficients $c > 0$ ($\beta^-$, $\beta^+$ or $\hat\beta$, which is positive). The off-diagonal entry between nodes $i$ and $i + 1$ is $c_{i+1/2}/\Delta x^2$ in both rows, so the matrix is symmetric. For a vector $v$ with $v_0 = v_n = 0$, summation by parts gives $v^TAv = -\sum_{i} c_{i+1/2}(v_{i+1} - v_i)^2/\Delta x^2 < 0$ unless $v = 0$. A symmetric negative definite tridiagonal matrix has nonzero leading minors, so Gaussian elimination without pivoting, which is the Thomas algorithm, does not break down. $\square$

**Termination.** One GFM step is a fixed number of passes over the $M$ cells (two sweeps for the nearest cells, two flux sweeps, one level set sweep, one selection). The time loop takes steps of at least $\min(\text{CFL}\,\Delta x/s_{\max}, T - t)$ with $s_{\max}$ finite, so it ends after finitely many steps. The Thomas algorithm makes two passes over $n - 1$ unknowns.

$\blacksquare$
