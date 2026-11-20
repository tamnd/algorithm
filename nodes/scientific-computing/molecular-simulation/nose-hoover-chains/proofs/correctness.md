---
title: "Nose-Hoover chains keep the extended energy and the canonical density, and the splitting is reversible"
proves: [correctness]
status: full
---

The equations of Martyna, Klein and Tuckerman (1992) for a chain of $M \ge 1$ thermostats with masses $Q_1, \ldots, Q_M$ are
$$\dot x_i = v_i, \qquad \dot v_i = \frac{f_i}{m_i} - \xi_1 v_i, \qquad \dot \eta_j = \xi_j,$$
$$\dot \xi_j = G_j - \xi_j \xi_{j+1} \ (j < M), \qquad \dot \xi_M = G_M, \qquad (1)$$
with the thermostat forces
$$G_1 = \frac{2K - N_f k_B T}{Q_1}, \qquad G_j = \frac{Q_{j-1}\xi_{j-1}^2 - k_B T}{Q_j} \ (j \ge 2).$$
$N_f$ is the number of velocity components that link 1 scales.

**Claim 1 (the extended energy).** The exact flow of (1) keeps
$$H' = K + U + \sum_{j=1}^{M} \tfrac12 Q_j \xi_j^2 + N_f k_B T \eta_1 + k_B T \sum_{j=2}^{M} \eta_j.$$

*Proof.* The particle terms give $\frac{d}{dt}(K + U) = -2K\xi_1$, as for one thermostat. For the chain,
$$\sum_j Q_j \xi_j \dot \xi_j = \xi_1 (2K - N_f k_B T) + \sum_{j=2}^{M} \xi_j (Q_{j-1}\xi_{j-1}^2 - k_B T) - \sum_{j=1}^{M-1} Q_j \xi_j^2 \xi_{j+1}.$$
The term $\xi_j Q_{j-1} \xi_{j-1}^2$ for $j \ge 2$ cancels the term $Q_{j-1}\xi_{j-1}^2 \xi_j$ of the last sum. What is left is $2K\xi_1 - N_f k_B T \xi_1 - k_B T \sum_{j \ge 2} \xi_j$. The $\eta$ terms give $N_f k_B T \xi_1 + k_B T \sum_{j \ge 2} \xi_j$. The total is 0. $\square$

**Claim 2 (the canonical density is stationary).** The density $\rho \propto \exp\bigl(-\beta(K + U + \sum_j \frac12 Q_j \xi_j^2)\bigr)$ on $(x, v, \xi_1, \ldots, \xi_M)$ is stationary for (1).

*Proof.* We show $F \cdot \nabla \ln \rho + \nabla \cdot F = 0$ for the vector field $F$ of (1). The divergence comes from $\partial \dot v_{ia} / \partial v_{ia} = -\xi_1$ ($N_f$ times) and $\partial \dot \xi_j / \partial \xi_j = -\xi_{j+1}$ for $j < M$; $G_j$ does not depend on $\xi_j$. So $\nabla \cdot F = -N_f \xi_1 - \sum_{j=2}^{M} \xi_j$. Next,
$$F \cdot \nabla \ln \rho = -\beta \Bigl( -2K\xi_1 + \sum_j Q_j \xi_j \dot \xi_j \Bigr) = -\beta \Bigl( -N_f k_B T \xi_1 - k_B T \sum_{j \ge 2} \xi_j \Bigr) = N_f \xi_1 + \sum_{j \ge 2} \xi_j,$$
by the computation in Claim 1. The sum is 0. $\square$

As for one thermostat, the marginal of $\rho$ in $(x, v)$ is canonical, and time averages are canonical averages only if the flow is ergodic. The chain does not prove ergodicity. It adds variables that make the dynamics chaotic in cases where one thermostat is not, such as one harmonic oscillator (a measurement on the page).

**Claim 3 (the splitting).** One step is $C_{h/2} \circ V_{h/2} \circ A_h \circ V_{h/2} \circ C_{h/2}$, where $V$ and $A$ are the exact kick and drift and $C_{h/2}$ is a palindrome of exact flows of parts of the chain field:
$$C_{h/2} = P_M \circ \cdots \circ P_1 \circ S \circ P_1 \circ \cdots \circ P_M,$$
read from right to left. Here $S$ is the exact flow for a time $h/2$ of $\dot v_i = -\xi_1 v_i$, $\dot \eta_j = \xi_j$ with all $\xi$ fixed. For $j < M$, $P_j = E_j \circ B_j \circ E_j$, with $E_j$ the exact flow for a time $h/8$ of $\dot \xi_j = -\xi_j \xi_{j+1}$ and $B_j$ the exact flow for a time $h/4$ of $\dot \xi_j = G_j$, all other variables fixed; and $P_M = B_M$.

*Proof.* $E_j$ multiplies $\xi_j$ by $e^{-\xi_{j+1} h/8}$: lines L12, L13 and L15. $G_j$ depends on $K$ or $\xi_{j-1}$ and not on $\xi_j$, so $B_j$ adds $\frac{h}{4} G_j$ to $\xi_j$: line L14, and line L11 for $j = M$. Line L16 applies $P_M, \ldots, P_1$ in this order, line L17 scales the velocities by $e^{-\xi_1 h/2}$ and line L18 adds $\frac{h}{2}\xi_j$ to each $\eta_j$, which is $S$, and line L19 applies $P_1, \ldots, P_M$. The kinetic energy is updated after the scaling, so the second $B_1$ uses the new $K$. Lines L4 to L7 are the Verlet part. $\square$

**Claim 4 (time reversal).** With $R(x, v, \xi, \eta) = (x, -v, -\xi, \eta)$, each exact flow $\phi_t$ above satisfies $R \circ \phi_t \circ R = \phi_{-t}$, and the step $\Psi_h$ is a palindrome of such flows, so $\Psi_h \circ R \circ \Psi_h = R$.

*Proof.* Under $R$, $G_1$ and $G_j$ are unchanged (they depend on $K$ and on $\xi_{j-1}^2$), so $B_j$ changes the sign of its increment; $E_j$ multiplies by $e^{-\xi_{j+1} t}$, and with $\xi_{j+1} \to -\xi_{j+1}$ this is $E_j$ for $-t$; the same holds for $S$, $V$ and $A$. A palindrome of maps with this property is reversed by $R$, as in the proof for one thermostat. $\square$

A symmetric composition of the flows of a split field has order 2, so $H'$ is kept up to $O(h^2)$ over a fixed time.

**Claim 5 (length 1).** For $M = 1$ the step is the Nose-Hoover step with $Q = Q_1$.

*Proof.* With $M = 1$ there are no $E$ maps, and $C_{h/2} = B_1 \circ S \circ B_1$: a quarter kick of $\xi_1$ by $(2K - N_f k_B T)/Q_1$, the scaling of $v$ by $e^{-\xi_1 h/2}$ with $\eta_1 \mathrel{+}= \frac{h}{2}\xi_1$, and a quarter kick with the new $K$. These are lines L11 to L14 of the Nose-Hoover page, and $H'$ reduces to $K + U + \frac12 Q_1 \xi_1^2 + N_f k_B T \eta_1$. $\square$
