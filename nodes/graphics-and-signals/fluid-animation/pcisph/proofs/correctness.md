---
title: The exit condition, the momentum laws and the first order meaning of delta in PCISPH
proves: [correctness]
status: full
---

We use the notation of the page.
All particles have the mass $m > 0$.
The arithmetic is exact real arithmetic.
PCISPH has no general proof of convergence; the claims below are what holds for every run.

## The exit condition

**Claim 1.** If the loop of line L4 ends with fewer than the maximum number of passes, then $\rho^*_i \le (1 + \eta)\rho_0$ for every particle, where $\rho^*$ is the density of line L7 in the last pass.

*Proof.*
The loop ends only when its condition fails.
After at least 3 passes and below the cap, the condition fails only if $\max_i e_i \le \eta\rho_0$, with $e_i = \rho^*_i - \rho_0$ from line L8 of the last pass. $\square$

## Momentum

**Claim 2.** With $g = 0$, no other forces and no walls, one step keeps $\sum_i m v_i$ and $\sum_i m\, x_i \times v_i$.

*Proof.*
By line L10, $a^p_i = \sum_{(i,j) \in P} -c\,(p_i + p_j)\nabla W_{ij} + \sum_{(j,i) \in P} c\,(p_j + p_i)\nabla W_{ji}$ with $c = m/\rho_0^2$: each stored pair adds $-c(p_i + p_j)\nabla W_{ij}$ to $a^p_i$ and the negative of it to $a^p_j$.
So $\sum_i m\, a^p_i = 0$, and line L11 keeps $\sum_i m v_i$.
Each pair term is a scalar times $\nabla W_{ij}$, which is parallel to $x_i - x_j$ (the gradient of a radial kernel).
The torque of the pair is $-c(p_i + p_j)\,m\,(x_i - x_j)\times\nabla W_{ij} = 0$, so $\sum_i x_i \times m a^p_i = 0$.
With $v' = v + \Delta t\,a^p$ and $x' = x + \Delta t\,v'$,
$$\sum_i m\, x'_i \times v'_i = \sum_i m\, x_i \times v'_i = \sum_i m\, x_i \times v_i + \Delta t\sum_i x_i \times m a^p_i,$$
since $v'_i \times v'_i = 0$, and the last sum is 0. $\square$

The values of $p$ do not matter in Claim 2, so it holds for any number of passes and with the clamp of line L9.

## The first order meaning of delta

Let $i$ be the prototype particle with neighbors $j$, and let $G = \sum_j \nabla W_{ij}$.
Give $i$ and its neighbors the pressure $\tilde p$, and keep the gradients of time $t$.
Following the derivation of Section 2.3 of the paper, the pressure moves $i$ by $\Delta x_i = -\Delta t^2 m\,(2\tilde p/\rho_0^2)\,G$, and the pair force of $i$ on $j$ moves $j$ by $\Delta x_j = \Delta t^2 m\,(2\tilde p/\rho_0^2)\nabla W_{ij}$.

**Claim 3.** To first order in the displacements, the density of $i$ changes by $-\tilde p\,\beta\,(|G|^2 + \sum_j|\nabla W_{ij}|^2)$. So $\tilde p = \delta e$ changes it by $-e + O(e^2)$.

*Proof.*
$\rho_i = m W(0) + \sum_j m W(|x_i - x_j|)$.
The first order change is $\sum_j m\,\nabla W_{ij}\cdot(\Delta x_i - \Delta x_j)$.
Substituting,
$$\sum_j m\nabla W_{ij}\cdot\Delta x_i = -\frac{2\Delta t^2 m^2\tilde p}{\rho_0^2}\,G\cdot G, \qquad \sum_j m\nabla W_{ij}\cdot\Delta x_j = \frac{2\Delta t^2 m^2\tilde p}{\rho_0^2}\sum_j|\nabla W_{ij}|^2.$$
The change is the first sum minus the second, which is $-\tilde p\,\beta\,(|G|^2 + \sum_j|\nabla W_{ij}|^2)$ with $\beta = 2\Delta t^2 m^2/\rho_0^2$.
With $\tilde p = \delta e$ and the definition of $\delta$, this is $-e$.
The kernel is twice differentiable away from $r = 0$ and $r = 2h$, so the rest of the Taylor expansion is $O(|\Delta x|^2) = O(e^2)$ for a lattice with no neighbor at exactly $2h$. $\square$

The test checks Claim 3 by a direct sum on a lattice: for $e = 10^{-3}$ and $e = 10^{-2}$ the density drop is within 5% of $e$.
Claim 3 is the reason for the factor in line L9; it is a statement about one particle in a full neighborhood, not a proof that the loop converges for the whole fluid. $\blacksquare$
