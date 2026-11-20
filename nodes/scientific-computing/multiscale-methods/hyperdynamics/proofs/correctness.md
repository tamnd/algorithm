---
title: Why the boosted clock gives the escape time under transition state theory
proves: [correctness]
status: full
---

The claim of hyperdynamics is a claim about transition state theory (TST) rates, not about every dynamics. We prove it for TST rates, then say what it means for the dynamics of the implementation.

**Setting.** The system is in a basin $A$ with dividing surfaces $\mathcal{S}_1, \ldots, \mathcal{S}_m$ to the neighbouring basins. The canonical density at $\beta = 1/(k_B T)$ is proportional to $e^{-\beta V}$ in position space. The TST rate through $\mathcal{S}_j$ is the one-way equilibrium flux through $\mathcal{S}_j$ divided by the probability of $A$:

$$k_j = \frac{\Phi_j}{Z_A}, \qquad Z_A = \int_A e^{-\beta V(x)}\, dx, \qquad \Phi_j = c \int_{\mathcal{S}_j} e^{-\beta V(x)}\, d\sigma(x),$$

where the constant $c$ comes from the integral over the velocities and does not depend on $V$ (in mass-weighted coordinates $c = (2\pi\beta)^{-1/2}$; see [harmonic transition state theory](/harmonic-transition-state-theory/)). The bias $\Delta V \ge 0$ is zero on every $\mathcal{S}_j$. The biased system has the potential $V_b = V + \Delta V$ and the TST rates $k_j^b = \Phi_j^b / Z_A^b$.

**Lemma 1 (the fluxes do not change).** $\Phi_j^b = \Phi_j$ for every $j$.

*Proof.* On $\mathcal{S}_j$, $V_b = V$, so the two surface integrals are equal, and the velocity factor $c$ is the same. $\square$

**Lemma 2 (the basin integrals).** $Z_A / Z_A^b = \langle e^{\beta \Delta V} \rangle_b$, the average of $e^{\beta \Delta V}$ over the biased canonical density in $A$.

*Proof.* $\langle e^{\beta \Delta V} \rangle_b = \frac{1}{Z_A^b} \int_A e^{\beta \Delta V} e^{-\beta (V + \Delta V)}\, dx = \frac{Z_A}{Z_A^b}$. $\square$

**Theorem (Voter 1997).** Under the hypotheses above:

1. $k_j = k_j^b / \langle e^{\beta \Delta V} \rangle_b$ for every $j$. All rates are divided by the same number, the boost $B = \langle e^{\beta \Delta V} \rangle_b \ge 1$.
2. The probability that the escape goes through $\mathcal{S}_j$, $k_j / \sum_i k_i$, is the same for the biased and the unbiased system.
3. If the biased system escapes after $n$ steps of length $h$ that sample the biased density in $A$, the hyper time $t_{\mathrm{hyper}} = \sum_{s < n} h\, e^{\beta \Delta V(x_s)}$ is $n h B$ up to the error of a time average, and the mean of $n h$ is $1/\sum_i k_i^b$, so the mean of $t_{\mathrm{hyper}}$ is $B / \sum_i k_i^b = 1 / \sum_i k_i$, the mean escape time of the unbiased system.

*Proof.* Part 1 follows from Lemmas 1 and 2: $k_j = \Phi_j / Z_A = \Phi_j^b / Z_A^b \cdot Z_A^b / Z_A = k_j^b / B$. Part 2 follows from part 1, because the common factor cancels in the ratio. Part 3: under the TST hypotheses the escape is a Poisson process, so the escape time of the biased system is exponential with mean $1 / \sum_i k_i^b$, independent of the path inside $A$. The time average of $e^{\beta \Delta V}$ along a long run in $A$ tends to $B$ by the ergodic theorem for the biased dynamics. The mean of $t_{\mathrm{hyper}}$ is then $B$ times the mean biased escape time, and part 1 gives $B / \sum_i k_i^b = 1 / \sum_i k_i$. $B \ge 1$ because $\Delta V \ge 0$. $\blacksquare$

**The conditions in the proof.** Lemma 1 needs the bias to be exactly zero on the dividing surfaces. If it is not, the biased system escapes through a lowered barrier, both $\Phi_j^b > \Phi_j$ and the branching ratios change, and the hyper time is too long by an unknown factor. Part 3 needs the time average to be close to the canonical average, so the biased basin must still have a separation of time scales: the system must equilibrate in the biased basin before it escapes. A bias that fills the basin up to the barrier removes this separation.

**What the theorem means for real dynamics.** The theorem is exact for TST rates. For a dynamics with recrossings, such as the overdamped Langevin dynamics of the implementation, it holds only approximately. For a one-dimensional diffusion $dx = -V_b'(x)\, dt + \sqrt{2 k_B T}\, dW$ with an absorbing point $x_b$ beyond the barrier, the mean of the boosted clock from $y$ solves the backward equation $k_B T\, e^{\beta V_b} (e^{-\beta V_b} \tau')' = -e^{\beta \Delta V}$, whose solution is

$$\tau(y) = \frac{1}{k_B T} \int_y^{x_b} e^{\beta V_b(z)} \int_{-\infty}^{z} e^{-\beta V(u)}\, du\, dz.$$

The unbiased mean first passage time has $e^{\beta V(z)}$ in place of $e^{\beta V_b(z)}$. The two agree up to the contribution of the region where $\Delta V > 0$ to the outer integral, which is small compared with the contribution of the barrier region by a factor of order $e^{-\beta (E_b - V_c)}$ for the flat bias with floor $V_c$ and barrier $E_b$. So the error vanishes as the gap between the bias and the barrier grows in units of $k_B T$. On the page example, it is 2.2 % for $V_c = 0.4$ and 8.5 % for $V_c = 0.6$ at $k_B T = 0.25$.

**What is not proved.** The speedup is not part of the theorem. The boost $B$ depends on the bias, the system and the temperature, and the boost of a run is a measurement. The theorem does not say how to build a bias that is zero on dividing surfaces that are not known in advance; each bias form in use comes with its own argument for this.
