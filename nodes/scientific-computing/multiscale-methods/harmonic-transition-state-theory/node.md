---
tag: QDKA5Q
kind: theorem
slug: harmonic-transition-state-theory
name: Harmonic transition state theory
aliases:
- Vineyard formula
- HTST
area: scientific-computing/multiscale-methods
level: core
summary: "An approximate escape rate from an energy basin: the product of the normal mode frequencies at the minimum over those at the saddle, times exp(-dE/kT). Exact for harmonic wells, no recrossing."
prereqs: [canonical-ensemble, eigenvalue-problem, partition-function]
see_also: [kinetic-monte-carlo, nudged-elastic-band, dimer-method, temperature-accelerated-dynamics, hyperdynamics, energy-landscape, langevin-dynamics, detailed-balance]
sources:
  - paper: doi:10.1016/0022-3697(57)90059-8
    title: George H. Vineyard, Frequency factors and isotope effects in solid state rate processes, Journal of Physics and Chemistry of Solids 3(1-2), 1957, 121-127
    locator: the many-body harmonic rate formula, with 3N frequencies at the minimum and 3N - 1 at the saddle
  - paper: doi:10.1103/RevModPhys.62.251
    title: Peter Hanggi, Peter Talkner and Michal Borkovec, Reaction-rate theory, fifty years after Kramers, Reviews of Modern Physics 62(2), 1990, 251-341
    locator: the sections on transition state theory, its multidimensional harmonic form, the upper bound property and the Kramers corrections for friction
  - paper: doi:10.1063/1.1749604
    title: Henry Eyring, The activated complex in chemical reactions, Journal of Chemical Physics 3(2), 1935, 107-115
    locator: the transition state (activated complex) rate expression
  - book: doi:10.1137/1.9780898719260
    title: R. Wong, Asymptotic Approximations of Integrals, SIAM Classics in Applied Mathematics 34, 2001 (reprint of the Academic Press edition of 1989)
    locator: Chapter IX, Laplace's method for higher dimensional integrals
  - paper: doi:10.1007/BF00547608
    title: Klaus Muller and Leo D. Brown, Location of saddle points and minimum energy paths by a constrained simplex optimization procedure, Theoretica Chimica Acta 53(1), 1979, 75-93
    locator: the two-dimensional test potential used in the example
---

Harmonic transition state theory (HTST) gives the rate at which a system escapes from a basin of its potential energy over a saddle point, from only three things: the normal mode frequencies at the minimum, the normal mode frequencies at the saddle, and the energy difference $\Delta E$ between them. Vineyard's formula is $k = \bigl(\prod_{i=1}^{n} \nu_i^{A}\bigr) / \bigl(\prod_{i=2}^{n} \nu_i^{S}\bigr)\, e^{-\Delta E / (k_B T)}$. It is an approximation, not an exact law: it is the exact transition state theory rate when the basin and the saddle region are exactly harmonic, and transition state theory is itself exact only when no trajectory recrosses the dividing surface. It supplies the rates of [kinetic Monte Carlo](/kinetic-monte-carlo/), and the saddles come from the [nudged elastic band](/nudged-elastic-band/) or the [dimer method](/dimer-method/).

## Statement

**Setting.** A system has $n$ degrees of freedom (for $N$ atoms in three dimensions, $n = 3N$) with coordinates $x_i$ and masses $m_i$. Use the mass-weighted coordinates $q_i = \sqrt{m_i}\, x_i$, so that the Hamiltonian is $H(q, p) = \frac12 |p|^2 + V(q)$ with the potential energy $V$ (written $U$ on the [molecular dynamics](/molecular-dynamics/) page). The system is in the [canonical ensemble](/canonical-ensemble/) at temperature $T$, with density proportional to $e^{-\beta H}$ and $\beta = 1/(k_B T)$.

Let $q_A$ be a minimum of $V$ with the Hessian $H_A = \nabla^2 V(q_A)$, positive definite with eigenvalues $\lambda_1^A, \ldots, \lambda_n^A > 0$. Let $q_S$ be a first-order saddle: $\nabla V(q_S) = 0$, and $H_S = \nabla^2 V(q_S)$ has one negative eigenvalue $\lambda_1^S < 0$ with unit eigenvector $e_1$ and $n - 1$ positive eigenvalues $\lambda_2^S, \ldots, \lambda_n^S$. The angular frequencies are $\omega_i = \sqrt{\lambda_i}$ and the frequencies are $\nu_i = \omega_i / (2\pi)$. The barrier is $\Delta E = V(q_S) - V(q_A)$. The dividing surface is the hyperplane $\mathcal{S} = \{q : (q - q_S) \cdot e_1 = 0\}$, and the basin $A$ is the side of $\mathcal{S}$ that holds $q_A$.

**Transition state theory rate.** The TST rate is the one-way flux of the canonical ensemble through $\mathcal{S}$ from $A$ to the other side, divided by the probability of $A$:

$$k_{\mathrm{TST}} = \frac{\int_{\mathcal{S}} \int_{p \cdot e_1 > 0} (p \cdot e_1)\, e^{-\beta H}\, dp\, d\sigma(q)}{\int_A \int e^{-\beta H}\, dp\, dq}.$$

**Theorem (Vineyard 1957).**

(a) *Harmonic case.* Assume (H1) on the basin, $V(q) = V(q_A) + \frac12 (q - q_A)^{\mathsf T} H_A (q - q_A)$, and the basin integral is taken over all of $\mathbb{R}^n$; and (H2) on the surface, $V(q) = V(q_S) + \frac12 (q - q_S)^{\mathsf T} H_S (q - q_S)$ for all $q \in \mathcal{S}$. Then

$$k_{\mathrm{TST}} = \frac{1}{2\pi} \frac{\prod_{i=1}^{n} \omega_i^{A}}{\prod_{i=2}^{n} \omega_i^{S}}\, e^{-\beta \Delta E} = \frac{\prod_{i=1}^{n} \nu_i^{A}}{\prod_{i=2}^{n} \nu_i^{S}}\, e^{-\beta \Delta E} = k_{\mathrm{HTST}}.$$

(b) *Low temperature limit.* Assume instead that $V$ is four times continuously differentiable, that $q_A$ is the unique minimum of $V$ on the closure of $A$, that $q_S$ is the unique minimum of $V$ on $\mathcal{S}$, both nondegenerate as above, and that $\int_A e^{-\beta_0 V} dq$ and $\int_{\mathcal{S}} e^{-\beta_0 V} d\sigma$ are finite for some $\beta_0$. Then $k_{\mathrm{TST}} = k_{\mathrm{HTST}}\,(1 + O(1/\beta))$ as $\beta \to \infty$.

The theorem is about $k_{\mathrm{TST}}$. The true rate of the dynamics equals $k_{\mathrm{TST}}$ only if every trajectory that crosses $\mathcal{S}$ from $A$ goes on to the product state without coming back, and if the system is in equilibrium inside $A$ before it escapes. HTST is thus an approximation with three hypotheses: harmonic wells, no recrossing, and a barrier much larger than $k_B T$ (so that the escape is rare and the basin is in local equilibrium). It is classical: it ignores quantum effects such as zero-point energy and tunneling.

## In plain words

A system in a valley of its energy shakes for a long time before it climbs over the lowest pass into the next valley. The rate of escape has two parts. The first part is a chance: how often the system is at the pass. This falls quickly as the pass gets higher or the temperature gets lower. The second part is a speed: how fast it moves across the pass.

The formula treats the bottom of the valley and the pass as bowls. Then everything comes from how stiff the bowl is in each direction. A narrow, stiff valley holds the system in a small space, so the system is near the pass more often. A wide pass lets more systems through. The formula is good when the pass is high and when systems that cross the pass do not turn back.

## Proof

*The momentum integrals.* The Hamiltonian splits as $\frac12|p|^2 + V(q)$, so each integral in $k_{\mathrm{TST}}$ is a product of a momentum integral and a position integral. Over all of $\mathbb{R}^n$, $\int e^{-\beta |p|^2 / 2} dp = (2\pi/\beta)^{n/2}$. In the numerator, choose an orthonormal basis of momentum space whose first vector is $e_1$. Then

$$\int_{p_1 > 0} p_1 e^{-\beta p_1^2 / 2}\, dp_1 \cdot \Bigl(\frac{2\pi}{\beta}\Bigr)^{(n-1)/2} = \frac{1}{\beta} \Bigl(\frac{2\pi}{\beta}\Bigr)^{(n-1)/2}.$$

The ratio of the two momentum factors is $\beta^{-1} (2\pi / \beta)^{-1/2} = (2\pi\beta)^{-1/2}$. So, without any assumption on $V$,

$$k_{\mathrm{TST}} = \frac{1}{\sqrt{2\pi\beta}}\, \frac{\int_{\mathcal{S}} e^{-\beta V}\, d\sigma}{\int_A e^{-\beta V}\, dq}. \tag{1}$$

The mass weighting matters here: in the coordinates $q$, the velocity is $p$, so the speed normal to $\mathcal{S}$ is $p \cdot e_1$, and the kinetic energy has the same form in every direction.

*Part (a).* Under (H1), with $u = q - q_A$,

$$\int_{\mathbb{R}^n} e^{-\beta V}\, dq = e^{-\beta V(q_A)} \int_{\mathbb{R}^n} e^{-\beta u^{\mathsf T} H_A u / 2}\, du = e^{-\beta V(q_A)} \Bigl(\frac{2\pi}{\beta}\Bigr)^{n/2} \prod_{i=1}^n (\lambda_i^A)^{-1/2},$$

by the change of variables to the orthonormal eigenvectors of $H_A$, which turns the integral into a product of $n$ one-dimensional Gaussian integrals $\int e^{-\beta \lambda s^2/2} ds = (2\pi / (\beta\lambda))^{1/2}$. On $\mathcal{S}$, the eigenvectors $e_2, \ldots, e_n$ of the symmetric matrix $H_S$ are orthogonal to $e_1$, so they are an orthonormal basis of the hyperplane. Write $q = q_S + \sum_{i \ge 2} s_i e_i$. Then $(q - q_S)^{\mathsf T} H_S (q - q_S) = \sum_{i \ge 2} \lambda_i^S s_i^2$ and $d\sigma = ds_2 \cdots ds_n$, so under (H2)

$$\int_{\mathcal{S}} e^{-\beta V}\, d\sigma = e^{-\beta V(q_S)} \Bigl(\frac{2\pi}{\beta}\Bigr)^{(n-1)/2} \prod_{i=2}^n (\lambda_i^S)^{-1/2}.$$

Put both into (1). The powers of $2\pi/\beta$ leave $(2\pi/\beta)^{-1/2}$, and $(2\pi\beta)^{-1/2} (2\pi/\beta)^{-1/2} = 1/(2\pi)$. So

$$k_{\mathrm{TST}} = \frac{1}{2\pi} \frac{\prod_{i=1}^n (\lambda_i^A)^{1/2}}{\prod_{i=2}^n (\lambda_i^S)^{1/2}}\, e^{-\beta (V(q_S) - V(q_A))},$$

which is the first form with $\omega_i = \lambda_i^{1/2}$. The second form follows from $\nu_i = \omega_i / (2\pi)$: there are $n$ factors $1/(2\pi)$ above and $n - 1$ below, which leaves one factor $1/(2\pi)$. $\square$

*Part (b).* Laplace's method (Wong, Chapter IX) says: if $f$ is four times continuously differentiable on a domain $D$ of dimension $d$, has a unique minimum on the closure of $D$ at an interior point $y_0$ with a positive definite Hessian $F$, and $\int_D e^{-\beta_0 f}$ is finite, then $\int_D e^{-\beta f} = e^{-\beta f(y_0)} (2\pi/\beta)^{d/2} (\det F)^{-1/2} (1 + O(1/\beta))$. The term of order $\beta^{-1/2}$ vanishes because the cubic term of the Taylor series is odd. Apply it to the basin integral with $d = n$, $f = V$, $y_0 = q_A$, $F = H_A$, and to the surface integral with $d = n - 1$, $f = V$ restricted to $\mathcal{S}$, $y_0 = q_S$, and $F$ the restriction of $H_S$ to $\mathcal{S}$, whose eigenvalues are $\lambda_2^S, \ldots, \lambda_n^S$ as in part (a). The leading terms are the integrals of part (a), so the ratio in (1) is the harmonic ratio times $(1 + O(1/\beta)) / (1 + O(1/\beta)) = 1 + O(1/\beta)$. $\blacksquare$

## Consequences

**A one-dimensional example by hand.** For one particle of mass 1 in $V(x) = (x^2 - 1)^2$, the minimum $x = -1$ has $V'' = 8$, so $\omega^A = 2\sqrt2$, and the saddle $x = 0$ has $\Delta E = 1$. With $n = 1$ the product over the saddle is empty, and

$$k_{\mathrm{HTST}} = \frac{2\sqrt2}{2\pi} e^{-\beta} = 0.450158\, e^{-\beta}.$$

**The Muller-Brown surface.** On the Muller-Brown potential (Muller and Brown 1979), with unit masses, the eigenvalues of the Hessian are:

| point | $(x, y)$ | $V$ | $\lambda_1$ | $\lambda_2$ |
|---|---|---|---|---|
| minimum A | $(-0.55822, 1.44173)$ | $-146.6995$ | 410.5311 | 4068.1990 |
| minimum B | $(0.62350, 0.02804)$ | $-108.1667$ | 543.8362 | 3005.3959 |
| minimum C | $(-0.05001, 0.46669)$ | $-80.7678$ | 221.0375 | 1479.1970 |
| saddle S1 | $(-0.82200, 0.62431)$ | $-40.6648$ | $-750.8627$ | 490.2407 |
| saddle S2 | $(0.21249, 0.29299)$ | $-72.2489$ | $-735.2473$ | 510.8866 |

The prefactor $\nu = \sqrt{\lambda_1^A \lambda_2^A} / (2\pi \sqrt{\lambda_2^S})$ and the rate at $k_B T = 10$, in the units of the potential, are:

| escape | $\Delta E$ | prefactor | $k_{\mathrm{HTST}}$ at $k_B T = 10$ |
|---|---|---|---|
| A over S1 | 106.0347 | 9.2894 | $2.3065 \times 10^{-4}$ |
| C over S1 | 40.1030 | 4.1102 | $7.4509 \times 10^{-2}$ |
| C over S2 | 8.5189 | 4.0263 | $1.7176$ |
| B over S2 | 35.9178 | 9.0021 | $2.4800 \times 10^{-1}$ |

The prefactors differ by a factor of about 2, and the exponentials by many orders of magnitude. This is why the barrier matters most, and why a constant prefactor, often $10^{12}$ to $10^{13}\ \mathrm{s}^{-1}$ in solids, is a common simplification.

**Detailed balance.** In the harmonic approximation the probability of basin $A$ is proportional to $e^{-\beta V(q_A)} \prod_i (\lambda_i^A)^{-1/2}$. Then $\pi_A k_{A \to B}$ through the saddle $S$ is proportional to $e^{-\beta V(q_S)} / \prod_{i \ge 2} (\lambda_i^S)^{1/2}$, which does not depend on the basin. So HTST rates through the same saddle in both directions satisfy [detailed balance](/detailed-balance/) with the harmonic populations, and a [kinetic Monte Carlo](/kinetic-monte-carlo/) run with these rates has the harmonic Boltzmann distribution as its stationary law. For the Muller-Brown values above, $k_{C \to S1} / k_{A \to S1} = 323.04$, which equals the ratio of the harmonic populations of A and C.

**The Arrhenius form.** The prefactor does not depend on $T$, so $\ln k$ is linear in $1/T$ with slope $-\Delta E / k_B$. [Temperature accelerated dynamics](/temperature-accelerated-dynamics/) uses this to extrapolate event times from a high to a low temperature.

**Isotope effects.** Under a change of mass, the mass-weighted Hessian changes, while $\Delta E$ does not. The rate thus changes only through the prefactor. This was the purpose of Vineyard's paper.

## Tightness

**The harmonic approximation.** For the one-dimensional well above, the TST rate of formula (1), with the integral over $(-\infty, 0)$ by quadrature, compares with HTST as follows:

| $\beta$ | $k_{\mathrm{TST}}$ | $k_{\mathrm{HTST}}$ | ratio |
|---|---|---|---|
| 2 | $5.4117 \times 10^{-2}$ | $6.0922 \times 10^{-2}$ | 0.88830 |
| 5 | $2.8826 \times 10^{-3}$ | $3.0331 \times 10^{-3}$ | 0.95037 |
| 10 | $2.0008 \times 10^{-5}$ | $2.0437 \times 10^{-5}$ | 0.97898 |
| 20 | $9.1870 \times 10^{-10}$ | $9.2785 \times 10^{-10}$ | 0.99015 |
| 40 | $1.9033 \times 10^{-18}$ | $1.9124 \times 10^{-18}$ | 0.99520 |

The relative error is $O(1/\beta)$ and not smaller, as part (b) predicts. The next term of Laplace's method for $V = 4u^2 - 4u^3 + u^4$ with $u = x + 1$ gives the relative error $3/(16\beta) \approx 0.19/\beta$, and the table approaches this value at large $\beta$. The well is softer than its harmonic bowl, so the basin holds more states and the true TST rate is lower. For a barrier of a few $k_B T$, HTST errs by 10 % or more.

**Recrossing.** Classical TST counts every crossing of $\mathcal{S}$ from $A$ as an escape. A trajectory that crosses and comes back is counted, although it does not react. So for classical dynamics, $k_{\mathrm{TST}}$ is an upper bound of the rate defined by the reactive flux, and a dividing surface that minimizes $k_{\mathrm{TST}}$ gives the best bound (Hanggi, Talkner and Borkovec 1990). The ratio of the true rate to $k_{\mathrm{TST}}$ is the transmission coefficient $\kappa \le 1$. For [Langevin dynamics](/langevin-dynamics/) with friction $\gamma$ in the moderate to strong friction regime, Kramers' result is $\kappa = (\sqrt{\gamma^2/4 + |\omega_1^S|^2} - \gamma/2) / |\omega_1^S|$ in the harmonic setting, which goes to 0 like $|\omega_1^S| / \gamma$ for strong friction. For very weak friction, the rate is limited by the slow exchange of energy, and it also falls below $k_{\mathrm{TST}}$.

**Other limits.** When the barrier is comparable to $k_B T$, the escapes are not rare, the system does not reach local equilibrium in $A$, and the notion of a rate loses its meaning. At low temperature, quantum effects (zero-point energy and tunneling) make the classical formula wrong for light atoms such as hydrogen. Soft modes with small $\lambda_i$, as in molecules with free rotations, make the harmonic approximation poor even at a high barrier.

## History

Eyring gave the transition state (activated complex) theory of reaction rates in 1935. Vineyard derived the many-body harmonic form in 1957 for diffusion in solids, with the products of the $3N$ normal mode frequencies at the minimum and the $3N - 1$ at the saddle, and used it to explain isotope effects. Hanggi, Talkner and Borkovec reviewed in 1990 the theory of rates beyond TST, starting from Kramers' work of 1940 on friction.

## References
