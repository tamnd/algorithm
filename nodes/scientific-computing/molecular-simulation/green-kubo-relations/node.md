---
tag: HQFQQ3
kind: theorem
slug: green-kubo-relations
name: Green-Kubo relations
aliases:
- Green-Kubo formula
area: scientific-computing/molecular-simulation
level: advanced
summary: Express transport coefficients such as diffusion and viscosity as time integrals of equilibrium autocorrelation functions that MD can estimate.
prereqs: [molecular-dynamics, autocorrelation]
see_also: [langevin-dynamics, mori-zwanzig-formalism, wiener-khinchin-theorem, mcmc-autocorrelation, effective-sample-size, canonical-ensemble, ergodicity, brownian-dynamics]
sources:
  - paper: doi:10.1063/1.1740082
    title: Melville S. Green, Markoff random processes and the statistical mechanics of time-dependent phenomena. II. Irreversible processes in fluids, Journal of Chemical Physics 22(3), 1954, 398-413
    locator: transport coefficients of fluids as time integrals of equilibrium correlation functions
  - paper: doi:10.1143/JPSJ.12.570
    title: Ryogo Kubo, Statistical-mechanical theory of irreversible processes. I. General theory and simple applications to magnetic and conduction problems, Journal of the Physical Society of Japan 12(6), 1957, 570-586
    locator: the linear response derivation of the response functions and the conductivity
  - paper: doi:10.1146/annurev.pc.16.100165.000435
    title: Robert Zwanzig, Time-correlation functions and transport coefficients in statistical mechanics, Annual Review of Physical Chemistry 16, 1965, 67-102
    locator: a review of the correlation function formulas for transport coefficients
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Chapter 2, the section on transport coefficients and time correlation functions
---

The Green-Kubo relations express a transport coefficient, such as the diffusion coefficient, the shear viscosity or the thermal conductivity, as the time integral of an equilibrium autocorrelation function. For self-diffusion the relation is $D = \frac13 \int_0^\infty \langle v(0) \cdot v(t) \rangle \, dt$, the integral of the velocity [autocorrelation](/autocorrelation/) of one particle. So an equilibrium [molecular dynamics](/molecular-dynamics/) run, with no flow and no gradient, can measure how the system responds to a flow or a gradient. The result has two layers. The first is an exact identity: for any stationary velocity process, the mean square displacement grows like $2t$ times the integral of the autocorrelation, so the Green-Kubo integral equals the Einstein value $\lim \langle |r(t) - r(0)|^2 \rangle / 6t$ whenever the integral converges. The second is physics: the claim that these limits are the coefficients in Fick's law or the Navier-Stokes equations rests on linear response and on the hypothesis that small fluctuations decay by the same law as macroscopic disturbances. A value from a simulation is a measurement, with a truncated integral and a statistical error that grows with the truncation time.

## Statement

**Setting.** Let $v(t)$ be a stationary random process in $\mathbb{R}^3$ with $\langle |v(t)|^2 \rangle < \infty$, for example the velocity of one particle in an equilibrium molecular dynamics run, with the average over the equilibrium ensemble. Let $r(t) = r(0) + \int_0^t v(s) \, ds$, and let $C(s) = \langle v(u) \cdot v(u + s) \rangle$, which does not depend on $u$.

**Theorem (the Einstein and Green-Kubo forms agree).** For every $t > 0$,
$$\langle |r(t) - r(0)|^2 \rangle = 2 \int_0^t (t - s) \, C(s) \, ds.$$
If the improper integral $\int_0^\infty C(s) \, ds$ converges, then
$$\lim_{t \to \infty} \frac{\langle |r(t) - r(0)|^2 \rangle}{6t} = \frac13 \int_0^\infty C(s) \, ds.$$

**Physical relation (Green 1954, Kubo 1957).** Suppose that the system is in thermal equilibrium at temperature $T$, that a small disturbance relaxes by a linear macroscopic law, and that the equilibrium fluctuations relax by the same law (Onsager's regression hypothesis, or linear response). Then the coefficient of that law is the integral of the autocorrelation of the matching flux. In particular, the self-diffusion coefficient of Fick's law is $D = \frac13 \int_0^\infty \langle v(0) \cdot v(t) \rangle dt$, and the shear viscosity of a fluid of volume $V$ is
$$\eta = \frac{V}{k_B T} \int_0^\infty \langle P_{xy}(0) P_{xy}(t) \rangle \, dt,$$
where $P_{xy}$ is an off-diagonal element of the pressure tensor. The thermal conductivity is $\lambda = \frac{V}{k_B T^2} \int_0^\infty \langle J_x(0) J_x(t) \rangle dt$ with the heat flux density $J$. This part is not a theorem in general: it holds under the stated hypotheses, which are well supported for simple fluids.

## In plain words

A drop of ink spreads in water because each ink molecule wanders. How fast it spreads depends on how long a molecule keeps moving in the same direction before collisions turn it around.

The relation says: measure how long a molecule remembers its own velocity, and add up that memory over time. The total is the diffusion coefficient. If the memory is long, the molecule travels far before it turns, and the ink spreads fast. If the memory fades quickly, it spreads slowly.

The same idea works for the stickiness of a liquid and for the flow of heat, with other quantities in place of the velocity. The great benefit is that a simulation of a liquid at rest is enough. Nobody needs to stir it or heat one side.

## Proof

**The identity.** Since $r(t) - r(0) = \int_0^t v(s) \, ds$,
$$\langle |r(t) - r(0)|^2 \rangle = \int_0^t \int_0^t \langle v(s) \cdot v(s') \rangle \, ds' \, ds = \int_0^t \int_0^t C(s' - s) \, ds' \, ds.$$
Moving the average inside the integrals is allowed by Fubini's theorem, because $|\langle v(s) \cdot v(s') \rangle| \le C(0)$ by the Cauchy-Schwarz inequality, so the integrand is bounded on the square. Stationarity gives $C(-s) = \langle v(u) \cdot v(u - s) \rangle = \langle v(u - s) \cdot v(u) \rangle = C(s)$. The set of pairs $(s, s')$ in the square with $|s' - s| = \sigma$ has length $2(t - \sigma)$ along each value $\sigma \in [0, t]$, after the change of variables $\sigma = |s' - s|$. So the double integral is $2 \int_0^t (t - \sigma) C(\sigma) \, d\sigma$.

**The limit.** Let $F(\sigma) = \int_0^\sigma C$. Integration by parts gives $\int_0^t (t - \sigma) C(\sigma) \, d\sigma = \int_0^t F(\sigma) \, d\sigma$. Then
$$\frac{\langle |r(t) - r(0)|^2 \rangle}{6t} = \frac13 \cdot \frac1t \int_0^t F(\sigma) \, d\sigma.$$
If $F(\sigma) \to F_\infty$, then for every $\varepsilon > 0$ there is a $\sigma_0$ with $|F(\sigma) - F_\infty| < \varepsilon$ for $\sigma > \sigma_0$. The mean $\frac1t \int_0^t F$ differs from $F_\infty$ by at most $\frac{\sigma_0}{t} \sup_{[0, \sigma_0]} |F - F_\infty| + \varepsilon$, which is below $2\varepsilon$ for large $t$. So the limit is $\frac13 F_\infty$. $\square$

**The physical relation for diffusion.** If the probability density of the displacement of a tagged particle obeys the diffusion equation $\partial_t G = D \nabla^2 G$ at long times, with $G$ starting as a point mass, then $\frac{d}{dt} \int |r|^2 G \, dr = 6D$, so the mean square displacement grows like $6Dt$. With the theorem, this $D$ is $\frac13 \int_0^\infty C$. The step that cannot be proved in general is the hypothesis itself: that the tagged particle in a many-body Hamiltonian system diffuses according to Fick's law at long times. The relations for viscosity and thermal conductivity follow in the same way from the hydrodynamic equations for the decay of transverse momentum and of energy, under the same kind of hypothesis, and from Kubo's linear response theory for mechanical perturbations.

The identity and the limit are proved here in full. The link to the macroscopic laws is derived from the stated hypotheses, not from the equations of motion alone.

## Consequences

- **A case to check by hand.** For a particle with Langevin dynamics, friction $\gamma$ and mass $m$, the velocity is an Ornstein-Uhlenbeck process and $C(t) = \frac{3 k_B T}{m} e^{-\gamma t}$. The integral gives $D = \frac{k_B T}{m \gamma}$, the Einstein relation. The identity gives the whole mean square displacement: $\langle |r(t) - r(0)|^2 \rangle = \frac{6 k_B T}{m \gamma} \bigl(t - \frac{1 - e^{-\gamma t}}{\gamma}\bigr)$, which is ballistic, $\frac{3 k_B T}{m} t^2$, for small $t$, and diffusive for large $t$.
- **Estimates from a run.** In one dimension with $\gamma = 1$ and $k_B T / m = 1$, so that $D = 1$, four runs of length 5000 with the step 0.05 (seed 11) give, for the integral of the measured autocorrelation up to a cutoff $\tau$ (a measurement):

| cutoff $\tau$ | exact truncated value | mean of 4 runs | spread between runs |
|---|---|---|---|
| 1 | 0.6321 | 0.6417 | 0.026 |
| 2 | 0.8647 | 0.8772 | 0.041 |
| 5 | 0.9933 | 0.9933 | 0.091 |
| 10 | 1.0000 | 1.0236 | 0.123 |
| 20 | 1.0000 | 1.0387 | 0.160 |

A short cutoff misses part of the integral, and a long one adds the noise of the tail. Here a cutoff near five correlation times is the best compromise. The mean square displacement at the lag 20 gives $0.97 \pm 0.10$ from the same runs, against the exact $0.95$ at that lag: the Einstein form has the same statistical error.
- **Equilibrium is enough.** One run gives the diffusion of every species, and averages over all particles reduce the noise of $D$ by the square root of their number. Viscosity and thermal conductivity are collective quantities with one flux per system, so their noise is much larger.
- **Spectra.** By the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/), the integral of $C$ is half the power spectrum of the velocity at zero frequency. So one may estimate it with spectral methods, as for the integrated autocorrelation time of [MCMC output](/mcmc-autocorrelation/).

## Tightness

- **The integral must converge.** In a two-dimensional fluid, the velocity autocorrelation decays like $1/t$, a long-time tail found by Alder and Wainwright, so the integral diverges and a two-dimensional diffusion coefficient does not exist. In three dimensions the tail is $t^{-3/2}$ and the integral converges, but slowly, which biases a truncated integral.
- **Linear response only.** The relations give the coefficient at zero driving force and zero frequency. Strong shear, which thins many liquids, is outside their scope.
- **Stationarity and ergodicity.** The identity needs a stationary process. A run that is not yet in equilibrium, or that does not explore the phase space in the time of the run, gives a time average that is not the ensemble average. See [ergodicity](/ergodicity/).
- **Thermostats.** A thermostat that acts on each particle, such as Langevin dynamics, changes the velocity autocorrelation, and the value of $D$ is then the one of the thermostatted system. Use energy-conserving dynamics, or a weak or global thermostat, for transport coefficients.
- **Finite boxes.** With periodic boundary conditions, the hydrodynamic interaction with the images lowers $D$ by an amount that falls like $1/L$ for a box of side $L$, a heuristic result of hydrodynamics. Extrapolate in $L$ or correct for it.
- **The diffusion step.** The theorem gives only the limit of the mean square displacement. Saying that this is Fick's coefficient needs the diffusion equation at long times, which can fail in glasses and in crowded or confined systems with anomalous diffusion, where the mean square displacement does not grow linearly.

## History

Einstein (1905) related the diffusion coefficient of a Brownian particle to its friction. Green (1954) gave the transport coefficients of fluids as time integrals of equilibrium correlation functions, starting from a Markov description of the fluctuations. Kubo (1957) derived the response of a system to a mechanical perturbation from linear response theory, and gave the electrical conductivity as an integral of the current autocorrelation. Zwanzig (1965) reviewed the correlation function formulas. Alder and Wainwright found the long-time tail of the velocity autocorrelation in simulations of hard spheres, an early sign that the decay of correlations needs care.

## References
