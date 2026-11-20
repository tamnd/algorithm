---
tag: CN7RTP
kind: definition
slug: microcanonical-ensemble
name: Microcanonical ensemble
aliases:
- NVE ensemble
area: scientific-computing/molecular-simulation
level: core
summary: The uniform distribution over states of fixed particle number, volume and energy. Hamiltonian molecular dynamics, if ergodic, samples it with the total momentum also fixed.
prereqs: [hamiltonian-systems, molecular-dynamics]
see_also: [canonical-ensemble, partition-function, shadow-hamiltonian, periodic-boundary-conditions, green-kubo-relations, nose-hoover-thermostat, symplectic-integrators, radial-distribution-function]
sources:
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 2.1 (sampling from ensembles), Section 2.2 (common statistical ensembles, the microcanonical density and the constant-momentum ensemble of molecular dynamics) and Section 2.5 (fluctuations)
  - book: isbn:9780198525264
    title: Mark E. Tuckerman, Statistical Mechanics, Theory and Molecular Simulation, Oxford University Press, 2010
    locator: Chapter 3, the microcanonical ensemble
  - book: isbn:9780122673511
    title: Daan Frenkel and Berend Smit, Understanding Molecular Simulation, From Algorithms to Applications, second edition, Academic Press, 2002
    locator: Chapter 2 (statistical mechanics, ensembles and the ergodic hypothesis)
  - paper: doi:10.1103/PhysRev.153.250
    title: J. L. Lebowitz, J. K. Percus and L. Verlet, Ensemble dependence of fluctuations with application to machine computations, Physical Review 153(1), 1967, 250-254
    locator: the fluctuation of the kinetic energy at fixed total energy and its relation to the heat capacity
---

The microcanonical ensemble is the probability distribution of an isolated system with a fixed number of particles $N$, a fixed volume $V$ and a fixed energy $E$: every state on the energy surface $H = E$ has the same weight. It is the ensemble of classical mechanics without a heat bath, and plain [molecular dynamics](/molecular-dynamics/), which conserves the energy, samples it if the motion is ergodic. Molecular dynamics in a periodic box also conserves the total momentum, so the ensemble it samples is the microcanonical ensemble at fixed total momentum, often written NVEP. The [canonical ensemble](/canonical-ensemble/) at fixed temperature is the other ensemble used most, and a thermostat is needed to sample it.

## Definition

Let $\Gamma = (q_1, \ldots, q_N, p_1, \ldots, p_N)$ be a point of phase space and $H(\Gamma) = \sum_i |p_i|^2 / (2m_i) + U(q_1, \ldots, q_N)$ the Hamiltonian, with the positions in the volume $V$. The microcanonical ensemble at $(N, V, E)$ is the probability density
$$\rho_{NVE}(\Gamma) = \frac{\delta(H(\Gamma) - E)}{\Omega(N, V, E)}, \qquad \Omega(N, V, E) = \frac{1}{N!\, h_P^{3N}} \int \delta(H(\Gamma) - E)\, d\Gamma ,$$
where $h_P$ is Planck's constant, which only fixes the units of $\Omega$, and $N!$ counts the exchanges of identical particles. The average of an observable $A$ is $\langle A \rangle_{NVE} = \int A\, \rho_{NVE}\, d\Gamma$. The entropy is $S = k_B \ln \Omega$, and the temperature follows from $1/T = \partial S / \partial E$ at fixed $N$ and $V$.

Two remarks make the definition exact:

- **"Uniform" is in the measure $\delta(H - E)\, d\Gamma$.** Per unit of area on the surface $H = E$, the weight is proportional to $1 / |\nabla H|$, so the parts of the surface where $H$ changes slowly get more weight. Some books use the thin shell $E \le H \le E + \Delta E$ instead, which is the same in the limit $\Delta E \to 0$.
- **It is stationary.** By Liouville's theorem the Hamiltonian flow keeps phase-space volume, and it keeps $H$, so any density that is a function of $H$ alone, $\rho_{NVE}$ among them, does not change in time (a theorem).

**The ensemble of molecular dynamics.** If $U$ does not change when all atoms are moved by the same vector, as with [periodic boundary conditions](/periodic-boundary-conditions/), the total momentum $P = \sum_i p_i$ is also conserved. A trajectory then stays on the set $H = E$, $P = P_0$, and the best it can sample is
$$\rho_{NVEP}(\Gamma) \propto \delta(H(\Gamma) - E)\, \delta(P(\Gamma) - P_0) .$$
The usual choice is $P_0 = 0$. With periodic boundaries the box breaks the rotation symmetry, so the angular momentum is not conserved and gives no third constraint. Three degrees of freedom are fixed by the momentum, so the kinetic temperature is
$$T = \frac{2 \langle K \rangle}{N_f\, k_B}, \qquad N_f = 3N - 3 .$$
For an isolated molecule in free space, where the angular momentum is also conserved and set to zero, $N_f = 3N - 6$.

**Ergodicity.** Molecular dynamics gives time averages along one trajectory. These equal the ensemble averages above only if the motion is ergodic on its constant-energy and constant-momentum surface: almost every trajectory spends in each region of that surface a fraction of its time equal to the weight of the region. This is the ergodic hypothesis. It is an assumption for most systems of interest, not a theorem, and it fails for some, as the examples show.

**The integrator.** A [symplectic](/symplectic-integrators/) integrator such as velocity Verlet with step $h$ does not keep $H$ exactly. It keeps a nearby [shadow Hamiltonian](/shadow-hamiltonian/) $\tilde H = H + O(h^2)$ for very long times, so $H$ fluctuates by $O(h^2)$ and does not drift. A simulation is checked by monitoring $H$: a drift means a too large step or a force that is not the gradient of a smooth $U$, for example a force that jumps at a cutoff.

## Examples and non-examples

**One harmonic oscillator.** Take $H = p^2/(2m) + k x^2 / 2$ at energy $E$, with amplitude $A = \sqrt{2E/k}$. The energy surface is an ellipse. Integrating $\delta(H - E)$ over $p$ gives the density of $x$:
$$P(x) = \frac{1}{\pi \sqrt{A^2 - x^2}}, \qquad -A < x < A,$$
the arcsine law: the oscillator is most often near its turning points. The probability of $|x| < A/2$ is $\tfrac{2}{\pi} \arcsin \tfrac{1}{2} = \tfrac{1}{3}$. The trajectory $x = A \sin(\omega t)$ gives the same: $|\sin \theta| < 1/2$ on two arcs of length $\pi/3$ each, which is $1/3$ of the period. A system with one degree of freedom is ergodic on its energy curve, so the time average and the ensemble average agree.

**Two oscillators, an ensemble but not ergodic dynamics.** Take two independent oscillators with total energy $E = E_1 + E_2$. One oscillator has a constant density of states, so in the ensemble the share $E_1$ is uniform on $[0, E]$, with mean $E/2$ and variance $E^2/12$. But each oscillator keeps its own energy along the motion, so a trajectory started with $E_1 = 0.9E$ keeps $E_1 = 0.9E$ forever, and its time average is $0.9E$, not $E/2$. The same happens with the normal modes of a harmonic crystal. The microcanonical ensemble is well defined here; molecular dynamics does not sample it.

**The ideal gas and the Maxwell distribution.** For $N$ free atoms with no momentum constraint, the momenta are uniform on the sphere $\sum |p_i|^2 = 2mE$ in $3N$ dimensions. One component $p$ of one momentum then has density proportional to
$$\left(1 - \frac{p^2}{2mE}\right)^{(3N-3)/2} .$$
For $N = 1$ the exponent is 0, so each component is uniform on $[-\sqrt{2mE}, \sqrt{2mE}]$, which is Archimedes' result for the sphere. With $E = \tfrac{3}{2} N k_B T$ and $N \to \infty$, the density tends to $\exp(-p^2 / (2 m k_B T))$, the Maxwell-Boltzmann distribution of the canonical ensemble.

**Counting degrees of freedom.** A run with $N = 108$ atoms and zero total momentum has mean kinetic energy $\langle K \rangle = 160.5\,\epsilon$. With $N_f = 3N - 3 = 321$, the reduced temperature is $T^* = 2 \cdot 160.5 / 321 = 1.000$. With $3N = 324$ it would be $0.991$, an error of about 1 percent that shrinks as $1/N$.

**Fluctuations depend on the ensemble.** In the canonical ensemble the energy fluctuates; in the microcanonical ensemble it does not, but the kinetic energy $K$ does. Lebowitz, Percus and Verlet showed that at fixed energy, to leading order in $N$,
$$\langle \delta K^2 \rangle_{NVE} = \frac{3}{2} N k_B^2 T^2 \left(1 - \frac{3 N k_B}{2 C_V}\right),$$
with $C_V$ the heat capacity, so a molecular dynamics run gives $C_V$ from the fluctuation of $K$ (a theorem). For an ideal gas, $C_V = \tfrac{3}{2} N k_B$ and the fluctuation is 0, as it must be, since then $K = E$. Averages of local quantities, such as the pressure or the [radial distribution function](/radial-distribution-function/), agree between the two ensembles up to $O(1/N)$.

**Non-example: a thermostatted run.** Molecular dynamics with a [Nosé-Hoover thermostat](/nose-hoover-thermostat/) or an [Andersen thermostat](/andersen-thermostat/) changes the energy of the atoms on purpose and samples the canonical ensemble, not this one.

**Non-example: a trajectory that does not conserve energy.** With a plain truncated potential, the force is not the gradient of a continuous energy, and each crossing of the cutoff changes $H$. The energy then drifts, and the run samples no fixed-energy ensemble.

## Related definitions

- **[Canonical ensemble](/canonical-ensemble/).** Fixed $N$, $V$ and $T$, with density proportional to $\exp(-H / k_B T)$. For large $N$ it is concentrated near one energy, and it is the microcanonical ensemble averaged over $E$ with the weight $\Omega(E) e^{-E/k_B T}$.
- **[Partition function](/partition-function/).** The canonical normalization $Z$ is the Laplace transform of $\Omega(E)$ in the energy.
- **Ergodic hypothesis.** The assumption that time averages equal the ensemble averages. For Markov chains, the [ergodic theorem](/ergodic-theorem/) is the analogous result, with conditions that can be checked.
- **[Shadow Hamiltonian](/shadow-hamiltonian/).** The quantity that a symplectic integrator keeps, so a long run samples the microcanonical ensemble of $\tilde H$, close to that of $H$.
- **[Green-Kubo relations](/green-kubo-relations/).** Transport coefficients from time correlations, usually computed in microcanonical runs, since a thermostat changes the dynamics.

## References
