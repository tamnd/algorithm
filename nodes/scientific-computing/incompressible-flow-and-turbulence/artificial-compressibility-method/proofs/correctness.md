---
title: The fixed points of artificial compressibility are the discrete steady incompressible solutions, and the linear Stokes iteration converges under a sharp step condition
proves: [correctness, termination]
status: full
---

**Setting.** The grid is the periodic MAC grid of the main page with $M$ cells. $D$ is the divergence at the cell centers, $G$ the gradient at the faces, and $A = -DG$, the periodic 5-point matrix, which is symmetric positive semidefinite with the constants as its null space (summation by parts gives $G^T = -D$; see the proof on the [Chorin projection method](/chorin-projection-method/) page). $R(\mathbf{u}, p) = -N_h(\mathbf{u}) + \nu L_h\mathbf{u} - Gp + \mathbf{f}$ is the momentum residual of line L2, with $N_h$ the central advection term and $L_h$ the 5-point Laplacian on each component. One iteration with step $\tau > 0$ and sound speed $c > 0$ is

$$\mathbf{u}^{m+1} = \mathbf{u}^m + \tau R(\mathbf{u}^m, p^m), \qquad p^{m+1} = p^m - \tau c^2 D\mathbf{u}^{m+1}.$$

**Theorem 1 (fixed points).** $(\mathbf{u}, p)$ is a fixed point of the iteration if and only if $R(\mathbf{u}, p) = 0$ and $D\mathbf{u} = 0$, that is, if and only if it solves the discrete steady incompressible equations. The set of fixed points does not depend on $c$ or on $\tau$.

*Proof.* If $R(\mathbf{u}, p) = 0$ and $D\mathbf{u} = 0$, then $\mathbf{u}^{m+1} = \mathbf{u}$ and $p^{m+1} = p$. Conversely, a fixed point has $\tau R = 0$, so $R = 0$, and then $\mathbf{u}^{m+1} = \mathbf{u}$ and $\tau c^2 D\mathbf{u} = 0$, so $D\mathbf{u} = 0$, because $\tau c^2 > 0$. Neither condition contains $c$ or $\tau$. $\square$

So if the iteration converges, the limit is a steady solution of the incompressible discrete equations, whatever $c$ was used. The stopping test of line L5 checks the two conditions of Theorem 1 directly: when it stops, $\max|R| \le$ tol and $\max|D\mathbf{u}| \le$ tol. Theorem 1 does not say that the iteration converges; for the nonlinear problem that is not guaranteed.

**Theorem 2 (linear Stokes iteration).** Drop the advection term ($N_h = 0$). Let $\mu_{\max} = 4/\Delta x^2 + 4/\Delta y^2$, which bounds every eigenvalue of $A$ and of $-L_h$. If

$$\tau^2 c^2\mu + 2\tau\nu\mu < 4 \quad \text{for every eigenvalue } \mu \text{ of } A, \text{ in particular if } \tau^2 c^2\mu_{\max} + 2\tau\nu\mu_{\max} < 4,$$

then the iteration converges, from any start, to a solution of $\nu L_h\mathbf{u} - Gp + \mathbf{f} = 0$, $D\mathbf{u} = 0$, provided $\mathbf{f}$ has zero mean on each face set and the start has the same mean velocity as the solution sought. If the condition fails for an eigenvalue $\mu$ that $A$ has, the iteration diverges for some start.

*Proof.* The iteration is affine, so the errors $(\mathbf{e}, q)$ with respect to a solution obey the same update with $\mathbf{f} = 0$. On the uniform periodic grid, $L_h$, $D$ and $G$ are shift invariant difference operators, so they commute in the sense $L_h G = G\Delta_h$ and $DL_h = \Delta_h D$, with $\Delta_h = -A$ on cell fields. Split the error orthogonally (discrete Helmholtz-Hodge) as $\mathbf{e} = \mathbf{e}_0 + Gs$ with $D\mathbf{e}_0 = 0$.

The divergence-free part. $D L_h\mathbf{e}_0 = \Delta_h D\mathbf{e}_0 = 0$, so $L_h$ maps divergence-free fields to divergence-free fields, and the update gives $\mathbf{e}_0 \leftarrow (I + \tau\nu L_h)\mathbf{e}_0$, independent of $q$, and the pressure update does not see $\mathbf{e}_0$. The eigenvalues of $-L_h$ on this space lie in $[0, \mu_{\max}]$, so the factor $1 - \tau\nu\mu$ has modulus below 1 when $0 < \tau\nu\mu < 2$, which the condition implies. The eigenvalue $0$ belongs to the constant fields, the mean velocity, which never changes; this is why the start must have the right mean.

The gradient part. Expand $s$ and $q$ in eigenvectors $\phi$ of $A$ with $A\phi = \mu\phi$, $\mu > 0$ (the constant eigenvector has $G\phi = 0$ and does not affect the velocity). Write $\mathbf{e} = \alpha G\phi$ (plus divergence-free terms) and $q = \beta\phi$. Then $L_hG\phi = G\Delta_h\phi = -\mu G\phi$ and $DG\phi = -\mu\phi$, so

$$\alpha' = (1 - s)\alpha - \tau\beta, \qquad \beta' = \beta - \tau c^2 D(\alpha' G\phi)/\phi = \beta + \tau c^2\mu\alpha', \qquad s = \tau\nu\mu.$$

The matrix of this map is $\begin{pmatrix} 1 - s & -\tau \\ \tau c^2\mu(1 - s) & 1 - r\end{pmatrix}$ with $r = \tau^2c^2\mu$. Its determinant is $(1 - s)(1 - r) + r(1 - s) = 1 - s$ and its trace is $2 - s - r$. A real $2 \times 2$ matrix has both eigenvalues inside the unit disk exactly when $|\det| < 1$ and $|\mathrm{tr}| < 1 + \det$ (the Schur-Cohn or Jury conditions). Here they read $0 < s < 2$ and $|2 - s - r| < 2 - s$, that is $r > 0$ and $r + 2s < 4$. Since $r > 0$ always, and $r + 2s < 4$ implies $s < 2$, the condition of the theorem is exactly the condition that every mode with $\mu > 0$ decays. If $r + 2s \ge 4$ for some eigenvalue that $A$ has, that mode has an eigenvalue of modulus at least 1 and does not decay; with $r + 2s > 4$ it grows. Both functions of $\mu$ are increasing, so the condition at $\mu_{\max}$ covers all $\mu$. $\square$

For even $n_x$ and $n_y$ the checkerboard $(-1)^{i+j}$ is an eigenvector of $A$ with $\mu = \mu_{\max}$, so the bound is sharp. The tests check it: a small checkerboard pressure decays with $0.98$ times the limiting step and grows with $1.02$ times it. The implementation solves $\tau^2c^2\mu_{\max} + 2\tau\nu\mu_{\max} = 4$ for $\tau$ and multiplies by a safety factor $0.8$, which is a choice. With the advection term the step must also satisfy the rule of thumb $\tau \le 2\nu/|\mathbf{u}|_{\max}^2$ for central differences with forward Euler; that part is not proved here.

**Termination.** Each iteration costs $O(M)$ operations, with no linear solve. The loop ends when the two residuals of Theorem 1 are below the tolerance, or after a fixed maximum number of iterations, so it always ends. Under the condition of Theorem 2 for the Stokes problem, the error decays geometrically, so the tolerance is reached after $O(\log(1/\text{tol}))$ iterations times a factor that depends on the spectral radius; for the nonlinear problem the iteration count is a measurement.
