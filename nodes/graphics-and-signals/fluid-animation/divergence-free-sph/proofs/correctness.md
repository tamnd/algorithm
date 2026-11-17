---
title: The factor alpha, the link to Jacobi, the exit conditions and the momentum laws of DFSPH
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact real arithmetic.
A sum over $j$ is over the neighbors of $i$, the pairs and the gradients are those of line L1 (density solver) or line L8 (divergence solver), and they do not change inside a solver.
The kernel is radial, so $\nabla W_{ij}$ is parallel to $x_i - x_j$ and $\nabla W_{ji} = -\nabla W_{ij}$.
Write $G_i = \sum_j m_j\nabla W_{ij}$ and $S_i = \sum_j m_j|\nabla W_{ij}|^2$.
DFSPH has no general proof that its solvers converge; the claims below hold for every run.

## The effect of one stiffness

**Lemma 1.** Apply the update of line L6 with $\kappa_i = c$ and $\kappa_j = 0$ for $j \ne i$. Then $D\rho_i/Dt$ changes by $-\Delta t\,(c/\rho_i)\,(|G_i|^2 + m_i S_i)$.

*Proof.*
The update changes $v_i$ by $-\Delta t\,(c/\rho_i)\,G_i$.
For a neighbor $j$, only the term of $i$ in its sum has $\kappa_i$, so $v_j$ changes by $-\Delta t\,m_i(c/\rho_i)\nabla W_{ji} = \Delta t\,m_i(c/\rho_i)\nabla W_{ij}$.
Other particles do not change.
$D\rho_i/Dt = \sum_j m_j(v_i - v_j)\cdot\nabla W_{ij}$ is linear in the velocities, so it changes by
$$\sum_j m_j\left(-\Delta t\frac{c}{\rho_i}G_i - \Delta t\,m_i\frac{c}{\rho_i}\nabla W_{ij}\right)\cdot\nabla W_{ij} = -\Delta t\frac{c}{\rho_i}\left(|G_i|^2 + m_i S_i\right). \;\square$$

**Claim 2.** Let all masses be equal and let the denominator of $\alpha_i$ be positive. With $\kappa_i = e_i\alpha_i/\Delta t^2$ on $i$ alone, where $e_i = \rho_i + \Delta t\,D\rho_i/Dt - \rho_0$, the new predicted density $\rho_i + \Delta t\,D\rho_i/Dt$ is $\rho_0$. With $\kappa_i = (D\rho_i/Dt)\,\alpha_i/\Delta t$ on $i$ alone, the new $D\rho_i/Dt$ is 0.

*Proof.*
With equal masses $m$, $\sum_j|m_j\nabla W_{ij}|^2 = m S_i = m_i S_i$, so $\alpha_i = \rho_i/(|G_i|^2 + m_i S_i)$.
By Lemma 1 with $c = e_i\alpha_i/\Delta t^2$, the predicted density changes by $\Delta t \cdot(-\Delta t\,(c/\rho_i)(|G_i|^2 + m_i S_i)) = -\Delta t^2 c/\alpha_i = -e_i$.
By Lemma 1 with $c = (D\rho_i/Dt)\alpha_i/\Delta t$, the rate changes by $-\Delta t\,c/\alpha_i = -D\rho_i/Dt$. $\square$

## The link to Jacobi

Let $K_i$ be the sum of the stiffness values $\kappa_i$ of the density passes so far, and $p_i = \rho_i K_i$.
The update of line L6 is linear in $\kappa$, so after the passes $v^*_i = v^{adv}_i + \Delta t\,a^p_i$ with
$$a^p_i = -\sum_j m_j\left(\frac{K_i}{\rho_i} + \frac{K_j}{\rho_j}\right)\nabla W_{ij} = -\sum_j m_j\left(\frac{p_i}{\rho_i^2} + \frac{p_j}{\rho_j^2}\right)\nabla W_{ij},$$
the pressure acceleration of the IISPH page, and $v^{adv}_i = v_i + \Delta t\,g$.
So the predicted density of line L4 is $\rho_i + \Delta t\,D\rho_i/Dt(v^{adv}) + \Delta t^2\sum_j m_j(a^p_i - a^p_j)\cdot\nabla W_{ij} = \rho^{adv}_i + (Ap)_i$ in the notation of IISPH, and $\rho^*_i - \rho_0 = (Ap)_i - s_i$.

**Claim 3.** With equal masses and without the max of line L4, one density pass changes $p_i$ by $(s_i - (Ap)_i)/a_{ii}$, where $a_{ii} = -(\Delta t^2/\rho_i^2)(|G_i|^2 + m_i S_i)$ is the IISPH diagonal. This is one Jacobi pass with weight $\omega = 1$.

*Proof.*
The pass adds $\kappa_i = (\rho^*_i - \rho_0)\alpha_i/\Delta t^2$ to $K_i$, so it adds $\rho_i\kappa_i$ to $p_i$.
With equal masses, $\rho_i\alpha_i/\Delta t^2 = \rho_i^2/(\Delta t^2(|G_i|^2 + m_i S_i)) = -1/a_{ii}$.
So $p_i$ changes by $-(\rho^*_i - \rho_0)/a_{ii} = (s_i - (Ap)_i)/a_{ii}$. $\square$

## Exit conditions

**Claim 4.** If the density solver stops before the cap, the mean of $\max(\rho^*_i - \rho_0, 0)$ in its last pass is at most $\eta\rho_0$. If the divergence solver stops before the cap, $\Delta t$ times the mean of $\max(D\rho_i/Dt, 0)$ in its last pass is at most $\eta_v\rho_0$.

*Proof.*
After the minimum number of passes and below the cap, the loops of lines L3 and L9 stop only when err is at most the tolerance times $\rho_0$, and err is the mean of line L4 or $\Delta t$ times the mean of line L10. $\square$

## Momentum

**Claim 5.** With $g = 0$, no walls and any stiffness values, one step keeps $\sum_i m_i v_i$ and $\sum_i m_i\,x_i \times v_i$.

*Proof.*
Write $c_{ij} = \kappa_i/\rho_i + \kappa_j/\rho_j = c_{ji}$.
In line L6 or L12, each pair changes $m_i v_i$ by $-\Delta t\,m_i m_j c_{ij}\nabla W_{ij}$ and $m_j v_j$ by $-\Delta t\,m_j m_i c_{ij}\nabla W_{ji} = +\Delta t\,m_i m_j c_{ij}\nabla W_{ij}$.
The sum is 0, so every update keeps $\sum_i m_i v_i$.
The change of the angular momentum at fixed positions is $-\Delta t\,m_i m_j c_{ij}(x_i - x_j)\times\nabla W_{ij} = 0$, because the two vectors are parallel.
So the updates of the density solver keep $\sum_i m_i x_i \times v^*_i$ at the old positions, and the updates of the divergence solver keep it at the new positions.
Line L7 gives $x'_i = x_i + \Delta t\,v^*_i$, so $\sum_i m_i x'_i \times v^*_i = \sum_i m_i x_i \times v^*_i$, since $v^*_i \times v^*_i = 0$.
With $g = 0$, line L2 does not change $v$.
So each part of the step keeps both sums. $\blacksquare$
