---
title: DPD conserves momentum, and its fluctuation-dissipation relation makes the Gibbs distribution stationary
proves: [correctness]
status: full
---

Setup. $N$ beads of mass $1$ with positions $x_i$ and velocities $v_i$ in a periodic box, the cutoff $r_c$, $r_{ij} = |x_i - x_j|$ with the minimum image, $e_{ij} = (x_i - x_j) / r_{ij}$, $v_{ij} = v_i - v_j$, the weight $w(r) = 1 - r / r_c$ for $r < r_c$ and $w = 0$ otherwise. The pair force on bead $i$ from bead $j$ is $F_{ij} = s_{ij} e_{ij}$ with the scalar
$$s_{ij} = a\, w(r_{ij}) - \gamma\, w^D(r_{ij}) (e_{ij} \cdot v_{ij}) + \sigma\, w^R(r_{ij})\, \theta_{ij} / \sqrt{h},$$
where the code uses $w^R = w$ and $w^D = w^2$, and $\theta_{ij} = \theta_{ji}$ is one standard normal number per pair and step.

**Lemma 1 (Newton's third law).** $F_{ji} = -F_{ij}$ for every pair, so $\sum_i F_i = 0$ for the forces $F_i = \sum_{j \ne i} F_{ij}$ of lines L6 to L9.

*Proof.* $r_{ji} = r_{ij}$, $e_{ji} = -e_{ij}$ and $v_{ji} = -v_{ij}$, so $e_{ji} \cdot v_{ji} = e_{ij} \cdot v_{ij}$, and $\theta_{ji} = \theta_{ij}$ because the code draws one number per unordered pair. So $s_{ji} = s_{ij}$ and $F_{ji} = s_{ij} e_{ji} = -F_{ij}$. Line L9 adds $F_{ij}$ to bead $i$ and $-F_{ij}$ to bead $j$, and the sum over all beads cancels pair by pair. $\square$

**Lemma 2 (momentum).** In exact arithmetic, a step of lines L1 to L5 keeps the total momentum $P = \sum_i v_i$.

*Proof.* Line L4 changes $P$ by $(h / 2) (\sum_i F_i + \sum_i F^{\text{new}}_i)$. Both sums are zero by Lemma 1, for any positions and any predicted velocities. $\square$

**Lemma 3 (the conservative part).** With $U = \sum_{i < j} (a r_c / 2)\, w(r_{ij})^2$, the conservative part of $F_i$ is $-\nabla_{x_i} U$.

*Proof.* $\frac{d}{dr} \frac{a r_c}{2} (1 - r / r_c)^2 = -a (1 - r / r_c) = -a\, w(r)$ for $r < r_c$, and $\nabla_{x_i} r_{ij} = e_{ij}$. So $-\nabla_{x_i}$ of the pair term is $a\, w(r_{ij}) e_{ij}$. The pair term and its derivative are $0$ at $r = r_c$, so $U$ is continuously differentiable across the cutoff. $\square$

**Theorem (fluctuation-dissipation, Espanol and Warren 1995).** Consider the stochastic differential equations of DPD as $h \to 0$:
$$dx_i = v_i\, dt, \qquad dv_i = \Big( -\nabla_{x_i} U - \gamma \sum_{j \ne i} w^D(r_{ij}) (e_{ij} \cdot v_{ij}) e_{ij} \Big) dt + \sigma \sum_{j \ne i} w^R(r_{ij})\, e_{ij}\, dW_{ij},$$
with independent Wiener processes $W_{ij} = W_{ji}$ per pair. The noise coefficient depends on positions only and the positions carry no noise, so the Ito and Stratonovich forms agree. Let $\rho = Z^{-1} \exp(-\beta H)$ with $H = \sum_i |v_i|^2 / 2 + U$. Then $\rho$ is a stationary solution of the Fokker-Planck equation if $w^D = (w^R)^2$ and $\sigma^2 = 2 \gamma k_B T$. Conversely, if $\rho$ is stationary for every $\beta$-independent choice of the potential and $w^R \ne 0$ on $(0, r_c)$, then $\gamma\, w^D = (\beta \sigma^2 / 2) (w^R)^2$.

*Proof.* The Fokker-Planck operator splits into the Liouville part of $H$ and one part per pair. The Liouville part is $-\{\rho, H\}$, which is zero for any function of $H$. For a pair $(i, j)$, write $D_{ij} = e_{ij} \cdot (\nabla_{v_i} - \nabla_{v_j})$. The drift of the pair is $-\gamma w^D (e_{ij} \cdot v_{ij})$ times the vector $(e_{ij}, -e_{ij})$ in the variables $(v_i, v_j)$, and the noise vector is $\sigma w^R (e_{ij}, -e_{ij})$. Since $w^D$ and $w^R$ do not depend on the velocities, the pair part of the operator applied to $\rho$ is
$$L_{ij} \rho = D_{ij} \Big[ \gamma\, w^D (e_{ij} \cdot v_{ij})\, \rho + \tfrac{1}{2} \sigma^2 (w^R)^2\, D_{ij} \rho \Big].$$
For the Gibbs density, $\nabla_{v_i} \rho = -\beta v_i \rho$, so $D_{ij} \rho = -\beta (e_{ij} \cdot v_{ij}) \rho$, and the bracket is $(e_{ij} \cdot v_{ij})\, \rho\, [\gamma w^D - \beta \sigma^2 (w^R)^2 / 2]$. With $w^D = (w^R)^2$ and $\sigma^2 = 2 \gamma k_B T$, the factor in square brackets is zero for every $r$, so $L_{ij} \rho = 0$ for every pair, and $\rho$ is stationary. Conversely, the bracket is zero for all states only if $\gamma w^D(r) = (\beta \sigma^2 / 2) (w^R(r))^2$ for every $r$; if the bracket is not zero, $L_{ij} \rho$ is a function of the state that is not identically zero (take one pair in range, all others out of range), and $\rho$ is not stationary. $\square$

Remarks. The theorem gives stationarity of the Gibbs distribution on each surface of fixed total momentum; it does not prove that the dynamics are ergodic or that the distribution is reached from every start. With the total momentum fixed, the kinetic temperature is $k_B T = \sum_i |v_i|^2 / N_f$ with $N_f = 2N - 2$ in two dimensions. The scheme of lines L1 to L5 has a step size error, so the sampled temperature differs from $k_B T$ by an amount that grows with $h$; this error is measured on the page, not bounded here. The code meets both conditions of the theorem: $w^R = w$, $w^D = w^2$, and the tests choose $\sigma^2 = 2 \gamma k_B T$. $\blacksquare$
