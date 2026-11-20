---
title: The Nose-Hoover equations keep the extended energy and the canonical density, and the splitting is reversible
proves: [correctness]
status: full
---

The Nose-Hoover equations for $N$ particles with $N_f$ velocity components, the friction $\xi$ and the thermostat mass $Q$ are
$$\dot x_i = v_i, \qquad m_i \dot v_i = f_i(x) - \xi m_i v_i, \qquad Q \dot \xi = 2K - N_f k_B T, \qquad \dot \eta = \xi. \qquad (1)$$
Here $K = \sum_i \frac12 m_i |v_i|^2$ and $f = -\nabla U$. In this proof $N_f$ is the number of velocity components that the thermostat scales, which is $N d$ in the implementation.

**Claim 1 (the extended energy).** The exact flow of (1) keeps $H' = K + U + \frac12 Q \xi^2 + N_f k_B T \eta$.

*Proof.* Along (1),
$$\frac{dH'}{dt} = \sum_i v_i \cdot (f_i - \xi m_i v_i) - \sum_i f_i \cdot v_i + \xi (2K - N_f k_B T) + N_f k_B T \xi = -2K\xi + 2K\xi = 0. \qquad \square$$

**Claim 2 (the canonical density is stationary).** The density $\rho(x, v, \xi) \propto \exp\bigl(-\beta (K + U + \frac12 Q \xi^2)\bigr)$ satisfies the Liouville equation $\partial_t \rho + \nabla \cdot (\rho F) = 0$ with $\partial_t \rho = 0$, where $F$ is the vector field of (1) on $(x, v, \xi)$.

*Proof.* We must show $F \cdot \nabla \ln \rho + \nabla \cdot F = 0$. Only the velocity equations depend on their own variable: $\partial \dot v_{ia} / \partial v_{ia} = -\xi$ for each of the $N_f$ components, so $\nabla \cdot F = -N_f \xi$. Next, $\ln \rho = -\beta (K + U + \frac12 Q\xi^2) + \text{const}$, so
$$F \cdot \nabla \ln \rho = -\beta \Bigl( \sum_i \nabla_i U \cdot v_i + \sum_i m_i v_i \cdot \bigl(\tfrac{f_i}{m_i} - \xi v_i\bigr) + Q \xi \cdot \tfrac{2K - N_f k_B T}{Q} \Bigr) = -\beta \bigl( -2K\xi + 2K\xi - N_f k_B T \xi \bigr) = N_f \xi.$$
The sum is 0. $\square$

The marginal of $\rho$ in $(x, v)$ is the canonical density. So time averages along (1) are canonical averages if the flow is ergodic on the set where $H'$ and the other conserved quantities are fixed. This is a hypothesis. It fails for one harmonic oscillator, and for systems with extra conservation laws such as the total momentum without external forces.

**Claim 3 (the splitting).** Write (1) as the sum of three vector fields: $V$, the kick $\dot v_i = f_i / m_i$; $A$, the drift $\dot x_i = v_i$; and $T$, the thermostat part $\dot v_i = -\xi v_i$, $\dot \xi = (2K - N_f k_B T) / Q$, $\dot \eta = \xi$. One step of the algorithm is
$$\Psi_h = T_{h/2} \circ V_{h/2} \circ A_h \circ V_{h/2} \circ T_{h/2},$$
where $V_t$ and $A_t$ are the exact flows and $T_t$ is the symmetric composition $G_{t/2} \circ S_t \circ G_{t/2}$ of two exact flows: $G_s$, the flow of $\dot \xi = (2K - N_f k_B T)/Q$ with $v$ fixed, and $S_t$, the flow of $\dot v_i = -\xi v_i$, $\dot \eta = \xi$ with $\xi$ fixed.

*Proof.* With $v$ fixed, $K$ is fixed, so $G_s$ adds $s (2K - N_f k_B T)/Q$ to $\xi$: these are lines L11 and L14 with $s = h/4$. With $\xi$ fixed, $S_t$ multiplies each velocity by $e^{-\xi t}$ and adds $\xi t$ to $\eta$: these are lines L12 and L13 with $t = h/2$. Line L14 uses the kinetic energy after the scaling, as $G$ must. Lines L4 to L7 are $V_{h/2} A_h V_{h/2}$, with the forces kept from the last evaluation as on the [molecular dynamics](/molecular-dynamics/) page. Line L3 is $T_{h/2}$ before the Verlet part and line L8 is $T_{h/2}$ after it. $\square$

**Claim 4 (time reversal).** Let $R(x, v, \xi, \eta) = (x, -v, -\xi, \eta)$. Then $\Psi_h \circ R \circ \Psi_h = R$.

*Proof.* For each of the exact flows $\phi_t$ above, $R \circ \phi_t \circ R = \phi_{-t}$: under $v \to -v$, $\xi \to -\xi$ each equation of (1) changes sign on the left exactly when the time direction changes, and $\eta$ is a sum of $\xi\,dt$, which also changes sign twice. So $R \circ \Psi_h \circ R$ is the same composition with each $t$ replaced by $-t$, taken in the same order. Because the composition is a palindrome, this is the inverse $\Psi_h^{-1}$. $\square$

A symmetric composition of flows of a split vector field is a method of order 2 (see [operator splitting](/operator-splitting/)), so $H'$ is kept up to $O(h^2)$ over a fixed time. The tests show the error falling by a factor 4 when $h$ is halved.

**Claim 5 (the mean kinetic energy).** Let $K_j$, $j = 1, \ldots, 4n$, be the kinetic energies used by the $4n$ applications of $G_{h/4}$ in $n$ steps, and $\xi_n$ the friction after step $n$. Then
$$\frac{1}{4n} \sum_{j=1}^{4n} \bigl(2K_j - N_f k_B T\bigr) = \frac{Q (\xi_n - \xi_0)}{n h}.$$
So if $\xi$ stays bounded, the mean of $2K_j$ tends to $N_f k_B T$ as $n \to \infty$.

*Proof.* Only $G$ changes $\xi$, and each application adds $\frac{h}{4}(2K_j - N_f k_B T)/Q$. Sum over $j$ and multiply by $4 Q / (4 n h)$. $\square$

Claim 5 needs no ergodicity. So a run with the right mean temperature does not show that the distribution is canonical. The test of the page shows a single oscillator with the right mean of $2K$ and a wrong distribution of $x$.

**Claim 6 (large mass).** As $Q \to \infty$ with $\xi_0 = 0$, $\xi$ stays 0 to within $O(1/Q)$, the scaling factors tend to 1, and the step tends to velocity Verlet. This follows from lines L11 to L14. $\square$
