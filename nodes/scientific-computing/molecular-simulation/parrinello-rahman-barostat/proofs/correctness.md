---
title: The Parrinello-Rahman splitting is a symmetric composition of exact Hamiltonian flows, and it samples NPH
proves: [correctness]
status: full
---

The cell is the $d \times d$ matrix $H$ whose columns are the cell vectors, with volume $V = \det H > 0$. Particle $i$ has scaled coordinates $s_i$, position $r_i = H s_i$ and momentum $\pi_i$ conjugate to $s_i$; $P_H$ is conjugate to $H$, $W > 0$ is the cell mass and $P$ the external pressure. With $v_i = H^{-\mathsf T} \pi_i / m_i$, the Hamiltonian is
$$E = \underbrace{\sum_i \tfrac12 m_i |v_i|^2}_{K} + U(Hs) + \frac{\operatorname{tr}(P_H^{\mathsf T} P_H)}{2W} + P \det H.$$
Since $\pi_i = m_i H^{\mathsf T} H \dot s_i$ along the flow, $v_i = H \dot s_i$ is the velocity of particle $i$ relative to the moving cell, and $K = \sum_i \frac12 m_i \dot s_i^{\mathsf T} H^{\mathsf T} H \dot s_i$ is the kinetic energy of Parrinello and Rahman (1981). The potential is a sum of pair terms $\phi(|r_{ij}|)$ over minimum images, with $r_{ij} = H s_{ij}$ and $f_{ij} = -\phi'(|r_{ij}|)\, r_{ij}/|r_{ij}|$.

**Claim 1 (the three flows are exact).** Write $E = E_V + E_T + E_C$ with $E_V = U + P\det H$, $E_T = K$ and $E_C = \operatorname{tr}(P_H^{\mathsf T} P_H)/(2W)$. The exact flows for a time $t$ are:

- $E_V$: $\pi_i \mathrel{+}= t\,H^{\mathsf T} f_i$ and $P_H \mathrel{+}= t\bigl(\sum_{i<j} f_{ij} s_{ij}^{\mathsf T} - P V H^{-\mathsf T}\bigr)$ (lines L3 and L8).
- $E_T$: $s_i \mathrel{+}= t\,H^{-1} v_i$ and $P_H \mathrel{+}= t \sum_i m_i v_i (H^{-1} v_i)^{\mathsf T}$ (lines L4 and L6).
- $E_C$: $H \mathrel{+}= t P_H / W$ (line L5).

*Proof.* $E_V$ depends only on $s$ and $H$, so under its flow $s$ and $H$ are fixed and the momenta move at constant rates $-\partial E_V/\partial s_i$ and $-\partial E_V/\partial H$. Now $-\partial U/\partial s_i = H^{\mathsf T} f_i$ by the chain rule. Inside one minimum image region $s_{ij}$ differs from $s_i - s_j$ by a fixed integer vector, so $\partial |H s_{ij}| / \partial H_{ab} = (r_{ij})_a (s_{ij})_b / |r_{ij}|$ and $-\partial U/\partial H = \sum_{i<j} f_{ij} s_{ij}^{\mathsf T}$. Jacobi's formula gives $\partial \det H/\partial H = V H^{-\mathsf T}$.

$E_T$ depends only on $\pi$ and $H$, so these are fixed, $v_i$ is fixed, $\dot s_i = \partial K / \partial \pi_i = H^{-1}H^{-\mathsf T}\pi_i/m_i = H^{-1} v_i$, and $\dot P_H = -\partial K/\partial H$. With $y_i = H^{-\mathsf T}\pi_i = m_i v_i$, $dy_i = -H^{-\mathsf T}\,dH^{\mathsf T}\,y_i$, so
$$dK = \sum_i \frac{y_i^{\mathsf T} dy_i}{m_i} = -\sum_i m_i (H^{-1} v_i)^{\mathsf T} dH^{\mathsf T} v_i = -\sum_i m_i\, v_i^{\mathsf T}\, dH\, (H^{-1} v_i),$$
and $-\partial K/\partial H = \sum_i m_i v_i (H^{-1} v_i)^{\mathsf T}$.

$E_C$ depends only on $P_H$, so $P_H$ is fixed and $\dot H = P_H/W$. $\square$

Each flow is the exact flow of a Hamiltonian, so it is symplectic. The step is the palindrome $\Psi_h = \phi^V_{h/2} \circ \phi^T_{h/2} \circ \phi^C_h \circ \phi^T_{h/2} \circ \phi^V_{h/2}$, so it is symplectic and has order 2 (see [operator splitting](/operator-splitting/)), and $E$ is kept up to $O(h^2)$ over a fixed time. Line L7 computes the forces at the new $s$ and $H$, and they are used again in line L3 of the next step, where $s$ and $H$ have not changed.

**Claim 2 (time reversal).** With $R(s, \pi, H, P_H) = (s, -\pi, H, -P_H)$, $\Psi_h \circ R \circ \Psi_h = R$.

*Proof.* $E$ is even in $(\pi, P_H)$, so for each part $R \circ \phi_t \circ R = \phi_{-t}$, and a palindrome of such maps is reversed by $R$. $\square$

**Claim 3 (the cell equation).** Along the exact flow of $E$,
$$W \ddot H = V\,(\Pi - P I)\,H^{-\mathsf T}, \qquad \Pi = \frac{1}{V}\Bigl( \sum_i m_i v_i v_i^{\mathsf T} + \sum_{i<j} f_{ij} r_{ij}^{\mathsf T} \Bigr).$$

*Proof.* $W\ddot H = \dot P_H$, the sum of the rates in Claim 1. Since $(H^{-1} v_i)^{\mathsf T} = v_i^{\mathsf T} H^{-\mathsf T}$, $v_i (H^{-1}v_i)^{\mathsf T} = v_i v_i^{\mathsf T} H^{-\mathsf T}$, and $s_{ij}^{\mathsf T} = r_{ij}^{\mathsf T} H^{-\mathsf T}$. $\square$

$\Pi$ is the internal pressure tensor (kinetic part plus virial), computed in line L9. So the cell accelerates while $\Pi \ne P I$. If $P_H$ stays bounded, the time average of $\dot P_H$ tends to 0, so the time average of $V(\Pi - P I)H^{-\mathsf T}$ is 0: the internal pressure balances the external one on average. The tests show this for two values of $P$.

**Claim 4 (conserved momenta).** The exact flow and the step $\Psi_h$ keep $\sum_i \pi_i$ and the antisymmetric part of $P_H H^{\mathsf T}$.

*Proof.* $\pi$ changes only in $\phi^V$, by $t H^{\mathsf T}\sum_i f_i = 0$, because the pair forces cancel. For the second, each of $E_V$, $E_T$ and $E_C$ is invariant under $H \mapsto QH$, $P_H \mapsto QP_H$ for a rotation $Q$, with $s$ and $\pi$ fixed: $|(QH)^{-\mathsf T}\pi_i| = |H^{-\mathsf T}\pi_i|$, $U$ depends on distances, $\det QH = \det H$ and $|QP_H| = |P_H|$. The generator of this group action is $\operatorname{tr}\bigl((AH)^{\mathsf T}P_H\bigr)$ for antisymmetric $A$, which is the $A$ component of the antisymmetric part of $P_H H^{\mathsf T}$. By Noether's theorem the exact flow of each part keeps it, so the composition does too. $\square$

So a cell started with a nonzero antisymmetric part of $P_H H^{\mathsf T}$ turns steadily. The test runs start with a zero cell velocity.

**Claim 5 (large cell mass).** With $\dot H(0) = 0$, $P_H(0) = 0$. As $W \to \infty$ with $h$ fixed, $\phi^C_h$ changes $H$ by $O(h^2/W)$ per step, and the step tends to velocity Verlet in a fixed cell.

*Proof.* $P_H$ grows by at most a bounded amount per step, so $H$ moves by $O(n h^2/W)$ in $n$ steps. With $H$ fixed, $\phi^V_{t}$ is $v_i \mathrel{+}= t f_i/m_i$ (since $v_i = H^{-\mathsf T}\pi_i/m_i$) and $\phi^T_t$ is $r_i \mathrel{+}= t v_i$, which give $V_{h/2}A_hV_{h/2}$. $\square$

**Claim 6 (minimum image).** Let $w_1, \ldots, w_d$ be the distances between opposite faces of the cell. If $2r_c < \min_k w_k$, then for each pair there is at most one image closer than $r_c$, and it is the one with scaled separation $a = s_{ij} - \operatorname{round}(s_{ij})$.

*Proof.* Row $k$ of $H^{-1}$ is normal to the face spanned by the other cell vectors, with length $1/w_k$. So for $r = Ha$, $|a_k| \le |r|/w_k$. An image with $|r| < r_c$ has $|a_k| < r_c/w_k < 1/2$ for all $k$, and rounding finds this $a$. Two such images would differ by an integer vector with all components less than 1 in size, which is 0. The implementation raises an error when the condition fails. $\square$

**Claim 7 (the ensemble).** The flow keeps $E$ and $N$ at the fixed pressure $P$, and $E$ is the enthalpy $K + U + PV$ plus the cell kinetic energy. So, if it is ergodic, it samples an isoenthalpic-isobaric (NPH) distribution, not the isothermal-isobaric one. Now let a thermostat at $k_B T$ act on all of $(s, \pi, H, P_H)$ so that the stationary density is $e^{-\beta E}\,ds\,d\pi\,dH\,dP_H$. Then the density of $(r, p, H)$ with $p_i = m_i v_i$ is
$$e^{-\beta (K + U + PV)}\,dr\,dp\,dH,$$
with the Lebesgue measure on the $d^2$ entries of $H$.

*Proof.* $r_i = H s_i$ and $\pi_i = H^{\mathsf T} p_i$ at fixed $H$, so $ds_i\,d\pi_i = (\det H)^{-1} dr_i\,(\det H)\,dp_i = dr_i\,dp_i$. The integral over $P_H$ is a Gaussian constant. $\square$

Integrated over the cell shapes at a fixed volume near a given shape, the measure $dH$ gives the weight $V^{d-1}\,dV$, since $H = V^{1/d} H_0$ with $\det H_0 = 1$ and $dH$ scales as $V^{d - 1} dV$ times a measure on $H_0$. So with a thermostat the method samples an NPT distribution in which the volume has the weight $V^{d-1}\,dV$, not $dV$. The configurational integral already carries the factor $V^N$, so the extra factor changes the volume averages by a relative amount of order $(d-1)/N$.
