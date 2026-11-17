---
title: The D2Q9 equilibrium has the prescribed moments, so BGK collision and streaming conserve mass and momentum exactly, and D1Q3 with tau = 1 is FTCS with mu = 1/6
proves: [correctness, termination, convergence]
status: full
---

**Setting.** D2Q9 velocities $c_0 = (0, 0)$, $c_{1..4} = (\pm1, 0), (0, \pm1)$, $c_{5..8} = (\pm1, \pm1)$, weights $w_0 = \frac49$, $w_{1..4} = \frac19$, $w_{5..8} = \frac1{36}$, and for each $i$ the opposite index $\bar\imath$ with $c_{\bar\imath} = -c_i$. Indices $a, b, c, d$ denote the two coordinate directions. Arithmetic is exact (the implementation runs in `Fraction` when $\tau$ is a `Fraction`).

**Lemma 1 (lattice isotropy).**

$$\sum_i w_i = 1, \quad \sum_i w_ic_{ia} = 0, \quad \sum_i w_ic_{ia}c_{ib} = \tfrac13\delta_{ab}, \quad \sum_i w_ic_{ia}c_{ib}c_{ic} = 0,$$
$$\sum_i w_ic_{ia}c_{ib}c_{ic}c_{id} = \tfrac19\bigl(\delta_{ab}\delta_{cd} + \delta_{ac}\delta_{bd} + \delta_{ad}\delta_{bc}\bigr).$$

*Proof.* $\frac49 + 4 \cdot \frac19 + 4 \cdot \frac1{36} = 1$. The odd moments vanish because the velocity set with its weights is symmetric under $c \mapsto -c$. Second moment: $\sum w_ic_{ix}^2 = 2 \cdot \frac19 + 4 \cdot \frac1{36} = \frac13$, $\sum w_ic_{ix}c_{iy} = 0$ by the symmetry $c_y \mapsto -c_y$. Fourth moment: $\sum w_ic_{ix}^4 = 2 \cdot \frac19 + 4 \cdot \frac1{36} = \frac13 = \frac19 \cdot 3$; $\sum w_ic_{ix}^2c_{iy}^2 = 4 \cdot \frac1{36} = \frac19$; moments with an odd power of a component vanish by reflection symmetry. These match the right-hand side in every case. $\square$

**Lemma 2 (moments of the equilibrium).** For $f_i^{\mathrm{eq}} = w_i\rho(1 + 3c_i\cdot u + \frac92(c_i\cdot u)^2 - \frac32|u|^2)$,

$$\sum_i f_i^{\mathrm{eq}} = \rho, \qquad \sum_i c_if_i^{\mathrm{eq}} = \rho u, \qquad \sum_i c_{ia}c_{ib}f_i^{\mathrm{eq}} = \tfrac13\rho\delta_{ab} + \rho u_au_b.$$

*Proof.* By Lemma 1, $\sum_i w_i(c_i\cdot u)^2 = \frac13|u|^2$, so $\sum f^{\mathrm{eq}} = \rho(1 + 0 + \frac32|u|^2 - \frac32|u|^2) = \rho$. The first moment keeps only the odd term, $3\sum_i w_ic_i(c_i\cdot u) = u$. For the second moment, $\sum_i w_ic_{ia}c_{ib}(c_i\cdot u)^2 = \frac19(\delta_{ab}|u|^2 + 2u_au_b)$, so it equals $\rho[\frac13\delta_{ab} + \frac12(\delta_{ab}|u|^2 + 2u_au_b) - \frac12|u|^2\delta_{ab}] = \rho(\frac13\delta_{ab} + u_au_b)$. $\square$

This is the Euler momentum flux with pressure $p = \rho/3$, which is the reason the method recovers the fluid equations; the viscous part needs the Chapman-Enskog expansion and is cited below.

**Lemma 3 (collision).** Let $j = \sum_ic_if_i$ at a node, $\rho = \sum_if_i$, $u = (j + \frac12g)/\rho$ (line L3), $\omega = 1/\tau$, and let $f_i^\ast$ be given by line L4. Then $\sum_if_i^\ast = \rho$ and $\sum_ic_if_i^\ast = j + g$. In particular, with $g = 0$ collision conserves mass and momentum at every node.

*Proof.* Write the source as $s_i = (1 - \frac\omega2)w_i[3(c_i - u)\cdot g + 9(c_i\cdot u)(c_i\cdot g)]$. By Lemma 1, $\sum_is_i = (1 - \frac\omega2)[0 - 3u\cdot g + 9 \cdot \frac13u\cdot g] = 0$, and $\sum_ic_is_i = (1 - \frac\omega2)[3 \cdot \frac13g - 0 + 0] = (1 - \frac\omega2)g$. With Lemma 2, $\sum_if_i^\ast = \rho - \omega(\rho - \rho) = \rho$ and

$$\sum_ic_if_i^\ast = j - \omega(j - \rho u) + (1 - \tfrac\omega2)g = j - \omega\bigl(j - j - \tfrac12g\bigr) + g - \tfrac\omega2g = j + g. \qquad \square$$

**Lemma 4 (streaming).** Line L5 with periodic wrap-around is a permutation of the population values that keeps each value in its velocity class $i$; with walls, line L6 sends the populations that would cross a wall back to their node in class $\bar\imath$, and every other population moves as before. Hence the total mass $\sum_{x,i}f_i(x)$ is unchanged by streaming in both cases, and the total momentum $\sum_{x,i}c_if_i(x)$ is unchanged in the periodic case.

*Proof.* Periodically, $x \mapsto x + c_i$ is a bijection of the nodes for each $i$, so each class is permuted and both sums are invariant. With walls, the moves inside the domain are injective for each $i$ and the targets left empty in class $\bar\imath$ near a wall are exactly the nodes that receive the reflected populations, so every value lands in exactly one slot. Reflection preserves the value and so the mass; it reverses $c_i$, which is the momentum transfer to the wall. $\square$

**Theorem 5 (exact conservation).** In exact arithmetic, after any number of steps: (a) the total mass equals the initial mass, with or without walls; (b) without walls the total momentum equals the initial momentum plus $S\,M\,g$, where $M$ is the number of nodes and $S$ the number of steps.

*Proof.* Lemmas 3 and 4, summed over nodes and iterated over the $S$ steps of line L2. $\square$

**Termination and cost.** Line L1 visits $M$ nodes; each of the $S$ steps visits each node once in lines L3 and L4 with $\Theta(Q)$ work and moves $Q$ values per node in lines L5 and L6; line L7 is one more pass. The loops have fixed bounds, so the run ends after $\Theta(SQM)$ operations.

**Theorem 6 (D1Q3 with $\tau = 1$).** With velocities $0, \pm1$, weights $\frac23, \frac16, \frac16$, equilibrium $w_i\rho$ and $\tau = 1$, the densities satisfy $\rho_j^{n+1} = \rho_j^n + \frac16(\rho_{j-1}^n - 2\rho_j^n + \rho_{j+1}^n)$. Under diffusive scaling with $D = \frac16\Delta x^2/\Delta t$ fixed, this scheme converges to the solution of $u_t = Du_{xx}$ with error $O(\Delta x^4)$ for smooth periodic data.

*Proof.* With $\omega = 1$, $f_i^\ast = w_i\rho_j$. Streaming moves $f_1^\ast$ from $j - 1$ to $j$ and $f_2^\ast$ from $j + 1$ to $j$, so $\rho_j^{n+1} = \frac23\rho_j + \frac16\rho_{j-1} + \frac16\rho_{j+1}$, which is the stated FTCS form with $\mu = \frac16$. The FTCS local truncation error is $\frac{\Delta t}2u_{tt} - \frac{D\Delta x^2}{12}u_{xxxx} + O(\Delta t^2 + \Delta x^4) = \bigl(\frac{D^2\Delta t}2 - \frac{D\Delta x^2}{12}\bigr)u_{xxxx} + O(\Delta x^4)$, using $u_{tt} = D^2u_{xxxx}$; with $D\Delta t = \frac16\Delta x^2$ the bracket is $0$, so the scheme is consistent of order 4 in $\Delta x$. Its amplification factor $1 - \frac23\sin^2(\theta/2)$ lies in $[\frac13, 1]$, so it is stable in $\ell^2$, and the [Lax equivalence theorem](/lax-equivalence-theorem/) with the rate addendum gives convergence with error $O(\Delta x^4)$. $\square$

**What is cited and what is observed.** The Chapman-Enskog analysis showing that D2Q9 BGK reproduces the incompressible Navier-Stokes equations with $\nu = (\tau - \frac12)/3$ and errors $O(\Delta x^2) + O(\mathrm{Ma}^2)$ under diffusive scaling, and that D1Q3 with general $\tau$ reproduces diffusion with $D = (\tau - \frac12)/3$, is cited from Krüger et al. (Chapter 4) and Qian, d'Humières and Lallemand. The analysis of the bounce-back slip in Poiseuille flow is cited from He, Zou, Luo and Dembo. The convergence orders, the slip values and the stability limits in the examples are observations of the implementation.
