---
title: The density condition, the diagonal, the fixed points and the momentum laws of IISPH
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact real arithmetic.
The pairs $P$ are the unordered pairs $\{i, j\}$ with $|x_i - x_j| < 2h$, and a sum over $j$ is over the neighbors of $i$.
The kernel is radial, so $\nabla W_{ij} = \phi_{ij}(x_i - x_j)$ for a scalar $\phi_{ij} = \phi_{ji}$, and $\nabla W_{ji} = -\nabla W_{ij}$.
IISPH has no proof that the clamped loop converges; the claims below hold for every run.

## The system is the density condition

**Claim 1.** Move every particle $j$ by $\Delta t^2 a^p_j$, with the neighbors and densities of time $t$. Then the first order change of $\rho_i$ is $(Ap)_i$.

*Proof.*
$\rho_i = \sum_j m_j W(|x_i - x_j|)$, with the term $j = i$ constant.
The first order change for the displacements $u_j$ is $\sum_j m_j\nabla W_{ij}\cdot(u_i - u_j)$.
With $u_j = \Delta t^2 a^p_j$ this is $\Delta t^2\sum_j m_j(a^p_i - a^p_j)\cdot\nabla W_{ij} = (Ap)_i$. $\square$

In the step, lines L10 and L11 give $x_i' = x_i + \Delta t v^{adv}_i + \Delta t^2 a^p_i$.
The same expansion for the displacement $\Delta t v^{adv}_i$ gives $\rho^{adv}_i$ of line L3.
So, to first order, the density after the step is $\rho^{adv}_i + (Ap)_i$, and $Ap = s$ is the condition that it equals $\rho_0$.

## The diagonal

**Claim 2.** The coefficient of $p_i$ in $(Ap)_i$ is $a_{ii}$ of line L4, and $a_{ii} < 0$ when $i$ has a neighbor with $\nabla W_{ij} \ne 0$.

*Proof.*
Set $p = e_i$, the unit vector of particle $i$.
Then $a^p_i = -(1/\rho_i^2)\sum_j m_j\nabla W_{ij} = -G_i/\rho_i^2$ with $G_i = \sum_j m_j\nabla W_{ij}$.
For a neighbor $j$, only the term of $i$ in the sum of $a^p_j$ has $p_i$, so $a^p_j = -m_i(1/\rho_i^2)\nabla W_{ji} = m_i\nabla W_{ij}/\rho_i^2$.
Particles that are not neighbors of $i$ do not enter $(Ap)_i$ through $a^p_j$, because $(Ap)_i$ sums over neighbors only.
So
$$(Ae_i)_i = \Delta t^2\left(a^p_i\cdot G_i - \sum_j m_j a^p_j\cdot\nabla W_{ij}\right) = -\frac{\Delta t^2}{\rho_i^2}\left(|G_i|^2 + m_i\sum_j m_j|\nabla W_{ij}|^2\right),$$
which is line L4.
Both terms are at least 0, and the second is positive when some $\nabla W_{ij} \ne 0$, since $m_i, m_j > 0$. $\square$

## Fixed points

**Claim 3.** Without the clamp, if $a_{ii} \ne 0$ for all $i$, then $p$ is a fixed point of line L8 if and only if $Ap = s$.

*Proof.*
Line L8 maps $p_i$ to $p_i + \omega(s_i - (Ap)_i)/a_{ii}$ with $\omega = 0.5 \ne 0$.
This equals $p_i$ for all $i$ if and only if $s_i - (Ap)_i = 0$ for all $i$. $\square$

With the clamp, a fixed point has, for each $i$, either $p_i > 0$ and $(Ap)_i = s_i$, or $p_i = 0$ and $(s_i - (Ap)_i)/a_{ii} \le 0$, that is $(Ap)_i \le s_i$.
So at a fixed point no particle is predicted to be compressed, and particles with a predicted low density have zero pressure.

## Exit condition

**Claim 4.** If the loop of line L6 stops after fewer than the maximum number of passes, then the mean over $i$ of $\max(\rho^{adv}_i + (Ap)_i - \rho_0, 0)$ is at most $\eta\rho_0$, where $p$ is the pressure at the start of the last pass.

*Proof.*
$\rho^{adv}_i + (Ap)_i - \rho_0 = (Ap)_i - s_i$, and line L9 computes the mean of the positive parts.
After at least 2 passes and below the cap, the loop stops only when this mean is at most $\eta\rho_0$. $\square$

## Momentum

**Claim 5.** With $g = 0$, no walls and any pressures $p$, one step keeps $\sum_i m_i v_i$ and $\sum_i m_i\, x_i \times v_i$.

*Proof.*
Write $c_{ij} = p_i/\rho_i^2 + p_j/\rho_j^2 = c_{ji}$.
Each pair adds $-m_j c_{ij}\nabla W_{ij}$ to $a^p_i$ and $-m_i c_{ij}\nabla W_{ji} = m_i c_{ij}\nabla W_{ij}$ to $a^p_j$.
So the pair adds $-m_i m_j c_{ij}\nabla W_{ij} + m_j m_i c_{ij}\nabla W_{ij} = 0$ to $\sum_i m_i a^p_i$.
Its torque is $m_i m_j c_{ij}\,(x_j - x_i)\times\nabla W_{ij} = 0$, because $\nabla W_{ij}$ is parallel to $x_i - x_j$.
So $\sum_i m_i a^p_i = 0$ and $\sum_i x_i \times m_i a^p_i = 0$.
With $g = 0$, $v' = v + \Delta t\,a^p$ by line L10, so the linear momentum is kept.
With $x' = x + \Delta t\,v'$ by line L11,
$$\sum_i m_i\, x'_i \times v'_i = \sum_i m_i\, x_i \times v'_i = \sum_i m_i\, x_i \times v_i + \Delta t\sum_i x_i \times m_i a^p_i,$$
since $v'_i \times v'_i = 0$, and the last sum is 0. $\square$

The claim does not use the values of $p$, so it holds for any number of passes, with or without the clamp.
The density $\rho_i$ of time $t$ is used in all the sums of a step, so the masses and densities do not change inside the step and the pair terms stay opposite. $\blacksquare$
