---
title: The track-length estimator is unbiased for the average flux
proves: [correctness]
status: full
---

We assume exact arithmetic and exact independent uniform random numbers, and the analog game of [analog Monte Carlo transport](/analog-monte-carlo-transport/), in which every history ends with probability 1 and the number of flights has a finite second moment. The argument for a fair weighted game is the same with weights. Write a phase space point as $p = (r, \Omega)$ (energy can be added as one more coordinate), $\Sigma_t(r) \ge 0$ for the total cross section, and $\tau(r, \Omega, t) = \int_0^t \Sigma_t(r + t'\Omega)\, dt'$ for the optical depth along a ray.

**The flight starts.** Let $\chi(p)$ be the density of the starting points of flights: the source points, plus the points just after a scattering. By the same summation over generations as for the collision density, $E[\text{number of flights starting in } A] = \int_A \chi$, and in the analog game $\chi = q + \int K_s F$, where $q$ is the source density and the second term is the density of scattered particles leaving collisions. The integral form of the [linear Boltzmann transport equation](/linear-boltzmann-transport-equation/) states that the angular flux is the uncollided transport of $\chi$:

$$\psi(r, \Omega) = \int_0^\infty \chi(r - t\Omega, \Omega)\, e^{-\tau(r - t\Omega, \Omega, t)}\, dt. \qquad (1)$$

This is the definition of the emission density $\chi$ in the integral equation, and (1) is the integral form of the streaming and absorption part, $\Omega \cdot \nabla \psi + \Sigma_t \psi = \chi$, solved along each characteristic.

**Lemma 1 (one flight).** For a flight that starts at $p_0 = (r_0, \Omega)$, the expected track length in a set $B$ of positions is $\int_0^\infty \mathbf{1}[r_0 + t\Omega \in B]\, e^{-\tau(r_0, \Omega, t)}\, dt$.

*Proof.* The flight covers the ray up to its path length $S$, which satisfies $P(S > t) = e^{-\tau(r_0, \Omega, t)}$ by [free-flight sampling](/free-flight-sampling/) (if the ray leaves the system, the flight stops at the face, and for later $t$ the indicator of $B$ is 0 because $B$ is inside the system). The track length in $B$ is $\int_0^S \mathbf{1}[r_0 + t\Omega \in B]\, dt = \int_0^\infty \mathbf{1}[t < S]\, \mathbf{1}[r_0 + t\Omega \in B]\, dt$. Taking expectations and exchanging the expectation and the integral (the integrand is non-negative) gives the claim. $\square$

**Lemma 2 (one history).** The total track length $h$ of one history in $B$ satisfies $E[h] = \int_B \int \psi(r, \Omega)\, d\Omega\, dr = \int_B \phi(r)\, dr$.

*Proof.* Sum Lemma 1 over the flights of the history. Given its starting point, each flight has the law of Lemma 1, so by the tower rule and the definition of $\chi$,

$$E[h] = \int \chi(r_0, \Omega) \int_0^\infty \mathbf{1}[r_0 + t\Omega \in B]\, e^{-\tau(r_0, \Omega, t)}\, dt\, dr_0\, d\Omega.$$

Change variables to the end point $r = r_0 + t\Omega$ for fixed $\Omega$ and $t$; the map $r_0 \mapsto r$ is a translation with Jacobian 1. Then

$$E[h] = \int \int_B \int_0^\infty \chi(r - t\Omega, \Omega)\, e^{-\tau(r - t\Omega, \Omega, t)}\, dt\, dr\, d\Omega = \int_B \int \psi(r, \Omega)\, d\Omega\, dr$$

by (1). The exchanges of integrals are valid because everything is non-negative. $\square$

**Theorem (unbiased).** The estimate $\phi_B = S_B/(N V)$ of line L10 satisfies $E[\phi_B] = \frac{1}{V}\int_B \phi\, dr$ for every $N \ge 1$, also where $\Sigma_t = 0$, and $\mathrm{Var}[\phi_B] = \mathrm{Var}[h]/(N V^2)$.

*Proof.* $S_B$ is the sum of $N$ independent copies of $h$, one per history, so $E[S_B] = N E[h]$ and $\mathrm{Var}[S_B] = N \mathrm{Var}[h]$. Lemma 2 gives the mean. Nothing in Lemmas 1 and 2 needs $\Sigma_t > 0$ in $B$. $\blacksquare$

**Finite variance.** If $B$ is bounded with diameter $D$, each flight contributes at most $D$, so $h \le D \cdot n_f$ with $n_f$ the number of flights, and $\mathrm{Var}[h] \le D^2 E[n_f^2] < \infty$. The central limit theorem then gives the asymptotic error bar of line L10.

**The slab.** In a slab, positions are $x \in [0, L]$, the bins are intervals and $\Omega$ reduces to $\mu$. A flight from $x_0$ with path length $S$ ends at $x_0 + \mu S$, and the path length in a bin $[a, b]$ is the length of $[\min(x_0, x_0 + \mu S), \max(x_0, x_0 + \mu S)] \cap [a, b]$ divided by $|\mu|$, which is what line L5 adds. For a beam on a pure absorber with $\mu = 1$, the history is one flight, and Lemma 1 gives $E[h] = \int_a^b e^{-\Sigma_t x}\, dx$ for the bin $[a, b]$, the same exact value as for the collision estimator.
