---
title: The 1D FE2 method solves the macro problem for the homogenized law and uses its exact tangent
proves: [correctness]
status: full
---

We prove the facts behind the 1D implementation, in exact arithmetic. A micro cell $j$ of the RVE has the energy density $\psi_j(e) = \tfrac12 c_j e^2 + \tfrac14 d e^4$ with $c_j > 0$ and $d \ge 0$, so its stress is $s_j = \psi_j'(e) = c_j e + d e^3$ and its tangent is $k_j = \psi_j''(e) = c_j + 3 d e^2 \ge c_j > 0$. The RVE has $n$ cells of length $\eta = 1/n$, and $\langle \cdot \rangle$ is the mean over the cells.

**Lemma 1 (the RVE problem).** For a macro strain $E$, let $e_j = E + (w_{j+1} - w_j)/\eta$ with $w_0 = w_n = 0$, and let

$$\Phi_E(w) = \sum_{j} \eta\, \psi_j(e_j).$$

Then $\Phi_E$ has exactly one minimizer $w^*$. It is the only solution of the equilibrium equations $r_m = s_{m-1} - s_m = 0$ for $m = 1, \ldots, n - 1$, which line L4 solves, and at $w^*$ all cells carry the same stress $s$. Moreover $\langle e \rangle = E$, the macro stress is $\Sigma(E) = \langle s \rangle = s$, and the Hill-Mandel condition $\langle s\, e \rangle = \Sigma E$ holds.

*Proof.* The map from $w$ to the differences $w_{j+1} - w_j$ is linear and one to one under $w_0 = w_n = 0$. Each $\psi_j$ is strictly convex with $\psi_j'' \ge c_j > 0$, so $\Phi_E$ is strictly convex and grows at least quadratically in $w$, and it has one minimizer. Its partial derivative is $\partial \Phi_E / \partial w_m = \psi_{m-1}'(e_{m-1}) - \psi_m'(e_m) = r_m$, so the minimizer is the only zero of $r$, and there the stresses of neighbor cells agree. The sum of the differences is $w_n - w_0 = 0$, so $\langle e \rangle = E$. With $s_j = s$ for all $j$, $\langle s e \rangle = s \langle e \rangle = s E = \Sigma E$. $\square$

Line L4 is Newton's method for $r = 0$. Its Jacobian $J$ is the tridiagonal matrix with $(k_{m-1} + k_m)/\eta$ on the diagonal and $-k/\eta$ beside it, which is symmetric positive definite, so each step is defined, and near $w^*$ the iteration converges quadratically. The loop stops when the residual is below the tolerance, and the claims below hold for the returned state up to that tolerance.

**Lemma 2 (the consistent tangent).** Line L5 returns

$$C = \langle k \rangle - \frac{1}{n \eta} \beta^T J^{-1} \beta = \frac{d \Sigma}{d E} = \Big\langle \frac{1}{k} \Big\rangle^{-1}, \qquad \beta_m = k_{m-1} - k_m.$$

*Proof.* At equilibrium $r(w^*(E), E) = 0$. The derivative of $r_m$ with respect to $E$ at fixed $w$ is $k_{m-1} - k_m = \beta_m$, so the implicit function theorem gives $d w^* / d E = -J^{-1} \beta$. Write $z = d w^* / d E$, with $z_0 = z_n = 0$. Then

$$\frac{d \Sigma}{d E} = \frac1n \sum_j k_j \Big( 1 + \frac{z_{j+1} - z_j}{\eta} \Big) = \langle k \rangle + \frac{1}{n \eta} \sum_{m=1}^{n-1} z_m (k_{m-1} - k_m) = \langle k \rangle - \frac{1}{n\eta} \beta^T J^{-1} \beta,$$

by summation by parts. For the second form, differentiate $s_j(e_j) = \Sigma$ for all $j$: $k_j\, d e_j = d \Sigma$, so $d e_j = d \Sigma / k_j$. The mean of $d e_j$ is $d E$ by Lemma 1, so $d E = d \Sigma\, \langle 1/k \rangle$. $\square$

The first form is static condensation of the fluctuation unknowns, which is what an FE2 code computes in any dimension. The second form, the harmonic mean of the micro tangents, holds only in 1D, and the tests check that both agree.

**Lemma 3 (the macro law is convex).** Let $W(E) = \min_w \Phi_E(w)$. Then $W'(E) = \Sigma(E)$ and $W''(E) = C(E) > 0$.

*Proof.* At the minimizer, $\partial \Phi_E / \partial w = 0$, so $W'(E) = \partial \Phi_E / \partial E = \sum_j \eta\, s_j = \Sigma$. Lemma 2 gives $W'' = C = \langle 1/k \rangle^{-1} > 0$. $\square$

**Theorem (the macro problem).** Lines L1 to L8 compute the P1 solution of the bar with the macro law $\Sigma(E)$, one Gauss point per element and $U_0 = 0$, $U_M = g$:

$$\Sigma_{i-1} - \Sigma_i = b H, \qquad i = 1, \ldots, M - 1, \qquad \Sigma_e = \Sigma\Big( \frac{U_{e+1} - U_e}{H} \Big).$$

This system has exactly one solution. If $b = 0$ and each macro element holds a whole number of periods of the resolved bar, then $U$ equals the resolved solution at the macro nodes.

*Proof.* The equations are the stationarity conditions of the macro energy $\sum_e H\, W((U_{e+1} - U_e)/H) - \sum_i b H U_i$ over $U_1, \ldots, U_{M-1}$, which is strictly convex by Lemma 3, so they have one solution. Line L6 forms their residual and the Jacobian, the tridiagonal matrix with entries $C_e / H$, using the exact tangent of Lemma 2, and line L7 is a Newton step. For $b = 0$, the equations say that $\Sigma_e$ is the same in all elements; since $\Sigma$ is strictly increasing, all macro strains are equal, and $U_M = g$ gives $E_e = g$ and $U_i = g\, i H$. In the resolved bar with $b = 0$ the stress is one constant $s$ in all cells, so each cell strain is the unique solution $e_j(s)$ of $s_j(e) = s$, and the strains of every period are the same. A macro element holding $p$ whole periods therefore has the mean strain $\bar e(s)$, and $u(1) = g$ gives $\bar e(s) = g$. By Lemma 1, the RVE with $E = g$ has cell strains $e_j(\Sigma(g))$ with mean $g$; since $\bar e$ is strictly increasing, $\Sigma(g) = s$, and the resolved displacement at the node $iH$ is $iH\, \bar e(s) = g\, iH = U_i$. $\square$

With a body force, the stress changes inside each period of the resolved bar, while the RVE sees one constant macro strain, so FE2 and the resolved bar differ by a term that shrinks with the period; the tests measure a factor of about 2 per halving.
