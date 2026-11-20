---
title: Fixed points of iterative Boltzmann inversion, the dilute limit and the quasi-Newton form
proves: [correctness]
status: full
---

The grid is $r_0, \dots, r_{M-1}$. A simulator is a map from a tabulated potential $V$ to a function $g_V > 0$ on the grid, $\beta = 1 / (k_B T)$, the target is $g^*$, and $\alpha > 0$. We assume exact arithmetic and an exact (noise free) simulator. Let $U$ be the set of grid points where $g^* > 0$, and assume that $g_V > 0$ on $U$ for the potentials that occur, so that line L5 updates exactly the points of $U$.

**Lemma 1 (what is returned).** If the procedure returns at line L4, then $\max_r |g_V(r) - g^*(r)| < \mathrm{tol}$ for the returned $V$.

*Proof.* Line L4 returns $V$ only after line L3 has computed $g = g_V$ for this $V$ and the test has held. Nothing changes $V$ between line L3 and the return. $\square$

**Lemma 2 (fixed points).** A potential $V$ is left unchanged by lines L5 and L6 if and only if $g_V(r) = g^*(r)$ at every point $r$ of $U$.

*Proof.* Line L6 changes $V(r)$ by $\alpha k_B T \ln(g_V(r) / g^*(r))$ at each $r \in U$. Since $\alpha k_B T > 0$, the change is zero if and only if $\ln(g_V(r) / g^*(r)) = 0$, that is $g_V(r) = g^*(r)$. Points outside $U$ are never changed. $\square$

**Corollary (uniqueness).** Let the simulator be exact for a fluid of particles with pairwise additive interactions, in the canonical ensemble at the density and temperature of the target, and let $g^* = g_{V^*}$ for a pair potential $V^*$. By Henderson's theorem (1974), two pair potentials with the same pair correlation function at the same density and temperature differ by a constant. So a fixed point of Lemma 2 with $U$ the whole grid equals $V^* + c$, and $c = 0$ if both potentials vanish at the cutoff. The corollary uses Henderson's theorem as stated in the source; it is not proved here.

**Lemma 3 (the dilute limit).** If $g_V = e^{-\beta V}$ for every $V$, then line L1 gives a fixed point at once: $g_{V_0} = g^*$ on $U$, and the loop returns after one simulation for any $\mathrm{tol} > 0$.

*Proof.* Line L1 sets $V_0(r) = -k_B T \ln g^*(r)$ on $U$, so $g_{V_0}(r) = e^{-\beta V_0(r)} = e^{\ln g^*(r)} = g^*(r)$, and the test of line L4 holds with error $0$. $\square$

**Lemma 4 (the quasi-Newton form).** Write $g_V = e^{-\beta V} y_V$, with the cavity function $y_V = g_V e^{\beta V} > 0$. Consider the equation $\Phi(V) = \ln g_V - \ln g^* = 0$ on $U$. Its Jacobian is $J = -\beta I + D$, where $D(r, r') = \partial \ln y_V(r) / \partial V(r')$. The update of line L6 is exactly the step $V \leftarrow V - \alpha J_0^{-1} \Phi(V)$ with $J_0 = -\beta I$, the Jacobian of the dilute limit, where $D = 0$.

*Proof.* $\ln g_V(r) = -\beta V(r) + \ln y_V(r)$, so $\partial \ln g_V(r) / \partial V(r') = -\beta \delta_{r r'} + D(r, r')$. With $J_0 = -\beta I$, $-\alpha J_0^{-1} \Phi(V) = \alpha k_B T (\ln g_V - \ln g^*) = \alpha k_B T \ln(g_V / g^*)$, which is the change of line L6. $\square$

So IBI is a quasi-Newton iteration with a fixed approximate Jacobian. Near a solution $V^*$ the error map has the linear part $I - \alpha J_0^{-1} J(V^*) = (1 - \alpha) I + \alpha k_B T\, D(V^*)$, and the iteration converges locally if the spectral radius of this matrix is less than $1$. For $\alpha = 1$ it is the spectral radius of $k_B T\, D(V^*)$, which tends to $0$ with the density for a smooth exact simulator, because $y_V \to 1$ for every $V$ as $\rho \to 0$. This gives local convergence at low enough density. There is no general bound on the spectral radius at liquid densities, so global convergence is not claimed.

**Theorem.** With an exact simulator, a returned potential reproduces the target to the tolerance (Lemma 1). A limit of the iteration reproduces it exactly on $U$ (Lemma 2), and it is the true pair potential up to a constant under the hypotheses of Henderson's theorem (corollary). In the dilute limit the first inversion is exact (Lemma 3). The update is the quasi-Newton step of Lemma 4.

*Proof.* Lemmas 1 to 4 and the corollary. $\blacksquare$
