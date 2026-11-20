---
title: The collision estimator is unbiased for the average flux
proves: [correctness]
status: full
---

We assume exact arithmetic and exact independent uniform random numbers, and a transport game in which every history ends with probability 1 and the number of collisions has a finite second moment (for the analog game this is Lemma 1 of the [analog Monte Carlo](/analog-monte-carlo-transport/) proof). Write $P$ for the phase space of position, direction and energy, $\Sigma_t(p) > 0$ for the total cross section at $p \in P$, and $B \subset P$ for a tally bin, whose spatial part has volume $V$.

**The collision density.** For a history, let $p_1, p_2, \ldots$ be the phase space points just before its collisions, with weights $w_1, w_2, \ldots$ ($w_k = 1$ in an analog game). The weighted collision density $F$ is defined by

$$E\Big[\sum_k w_k\, g(p_k)\Big] = \int_P g(p)\, F(p)\, dp$$

for every bounded measurable $g \ge 0$ with support where $\Sigma_t > 0$. For an analog game, Lemma 2 of the analog proof shows that $F$ is the sum of the densities of the $k$-th collisions and solves the integral transport equation $F = F_1 + K F$. Its solution is $F = \Sigma_t \psi$, where $\psi$ is the angular flux of the [linear Boltzmann transport equation](/linear-boltzmann-transport-equation/) with the same source: the collision rate density is the cross section times the flux, by the definition of the cross section. A weighted game is called fair if its weighted collision density is the same $F$; [implicit capture](/implicit-capture/) and [Russian roulette](/russian-roulette/) are fair, which is shown on their pages.

**Lemma (one history).** The total score of one history in the bin, $h = \sum_k w_k \mathbf{1}[p_k \in B] / \Sigma_t(p_k)$, satisfies $E[h] = \int_B \psi\, dp = \int_{B_r} \phi\, dr$, where $B_r$ is the spatial part of the bin and $\phi$ the scalar flux, if $B$ contains all directions and energies at its points (otherwise the angular and energy parts of the bin are integrated over).

*Proof.* Take $g(p) = \mathbf{1}[p \in B]/\Sigma_t(p)$, which is bounded because $\Sigma_t$ has a positive lower bound on $B$. Then $E[h] = \int_B F/\Sigma_t = \int_B \psi$. $\square$

**Theorem (unbiased).** The estimate $\phi_B = S_B/(N V)$ of line L10 satisfies $E[\phi_B] = \frac{1}{V}\int_{B_r} \phi\, dr$ for every $N \ge 1$, and $\mathrm{Var}[\phi_B] = \mathrm{Var}[h]/(N V^2)$.

*Proof.* $S_B$ is the sum of the history totals $h_1, \ldots, h_N$ of line L9. They are independent and have the law of $h$, because each history uses fresh random numbers. So $E[S_B] = N E[h]$ and $\mathrm{Var}[S_B] = N \mathrm{Var}[h]$, and division by $N V$ gives both statements with the lemma. $\blacksquare$

**Finite variance.** $h \le (\max_k w_k)\, k / \min_B \Sigma_t$, where $k$ is the number of collisions. In the analog game the weights are 1 and $k$ has a finite second moment, so $\mathrm{Var}[h] < \infty$. Then $(\phi_B - E\phi_B)/s_B$ tends in law to the standard normal law by the central limit theorem, and line L10 gives a valid asymptotic error bar. The variance of $h$ must be taken over the history totals: two collisions of one history in $B$ are not independent, so the sum of the squares of single scores does not give $\mathrm{Var}[h]$.

**Reaction rates.** With the score $w \Sigma_r / \Sigma_t$ in place of $w/\Sigma_t$, the same argument gives $E[h] = \int_B \Sigma_r \psi$, the rate of reaction $r$ in the bin.

**The void.** If $\Sigma_t = 0$ on a part of the bin, no collision happens there, and the estimate misses $\int \phi$ over that part. The lemma needs $\Sigma_t > 0$ on the bin.

**The slab example.** For a beam on a pure absorber with $\Sigma_t$ constant, the only collision is at the end of the first flight, with density $F(x) = \Sigma_t e^{-\Sigma_t x}$. A bin $[a, b]$ then has $E[h] = \int_a^b e^{-\Sigma_t x}\, dx = (e^{-\Sigma_t a} - e^{-\Sigma_t b})/\Sigma_t$, and the flux average is this value divided by $b - a$, which is the exact value used on the page.
