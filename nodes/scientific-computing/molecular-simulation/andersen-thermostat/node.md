---
tag: 8Z4JVW
kind: algorithm
slug: andersen-thermostat
name: Andersen thermostat
area: scientific-computing/molecular-simulation
level: core
summary: Samples the canonical ensemble by giving randomly chosen particles new velocities from the Maxwell-Boltzmann distribution at a set collision rate.
model: real-ram
complexity:
  vars: {N: the number of particles, S: the number of time steps}
  time: {worst: O(S N^2)}
  space: {extra: O(N)}
properties: {deterministic: false, randomized: true, iterative: true, symplectic: false, symmetric: false}
history:
  year: 1980
  people: [Hans C. Andersen]
  note: Andersen proposed the stochastic collisions in the same paper as his constant-pressure method, to give molecular dynamics at a constant temperature.
prereqs: [canonical-ensemble, molecular-dynamics]
see_also: [langevin-dynamics, stochastic-velocity-rescaling, nose-hoover-thermostat, berendsen-thermostat, box-muller-transform, green-kubo-relations, dissipative-particle-dynamics, hamiltonian-monte-carlo]
sources:
  - paper: doi:10.1063/1.439486
    title: Hans C. Andersen, Molecular dynamics simulations at constant pressure and/or temperature, Journal of Chemical Physics 72(4), 1980, 2384-2393
    locator: the section on constant temperature (stochastic collisions at a rate nu with a Poisson process of collision times)
  - book: isbn:9780122673511
    title: Daan Frenkel and Berend Smit, Understanding Molecular Simulation, From Algorithms to Applications, second edition, Academic Press, 2002
    locator: the chapter on molecular dynamics in various ensembles (the Andersen thermostat and its effect on the dynamics)
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Chapter 3, molecular dynamics (the constant-temperature methods)
  - book: isbn:9783319163741
    title: Ben Leimkuhler and Charles Matthews, Molecular Dynamics, With Deterministic and Stochastic Numerical Methods, Springer, 2015
    locator: Chapter 6, the canonical distribution and stochastic differential equations
---

The Andersen thermostat runs [molecular dynamics](/molecular-dynamics/) at a fixed temperature $T$ by letting the particles collide with an imaginary heat bath. At random times, at a rate $\nu$ per particle, a particle forgets its velocity and gets a new one drawn from the Maxwell-Boltzmann distribution at $T$. Between collisions the particles follow Newton's equations. Each collision keeps the [canonical ensemble](/canonical-ensemble/), and the Hamiltonian motion keeps it too, so the method samples the canonical distribution, up to the time step error of the integrator. The price is the dynamics: the collisions destroy the velocity memory at the rate $\nu$, so transport properties such as the diffusion coefficient depend on $\nu$ and are not those of the physical system.

## In plain words

Picture the atoms in a box with an invisible gas around them. Now and then, one atom is hit by a gas molecule and leaves with a new random speed and direction. The new speeds are drawn as they would be in a gas at the right temperature. Hot atoms lose energy this way and cold atoms gain it, so the system settles at the temperature of the gas.

The hits are random and independent, and each atom is hit about $\nu$ times per unit of time. Between hits nothing changes in the usual simulation. The method gives the right statistics of the positions and the speeds. It does not give the right motion over long times, because each hit wipes out the motion the atom had.

## The problem

The input is the positions $x_i \in \mathbb{R}^d$, velocities $v_i$ and masses $m_i > 0$ of $N$ particles, a force field that returns the potential energy $U(x)$ and the forces $f_i = -\nabla_i U$, a time step $h > 0$ (the letter $h$ is the time step, as on the molecular dynamics page), a number of steps $S$, the bath temperature $k_B T > 0$, a collision rate $\nu \ge 0$, and a source of random numbers. The output is a trajectory whose stationary distribution is the canonical density
$$\rho(x, v) \propto \exp\bigl(-\beta (K(v) + U(x))\bigr), \qquad \beta = \frac{1}{k_B T}, \qquad K(v) = \sum_i \tfrac12 m_i |v_i|^2,$$
together with the kinetic energy after each step. The kinetic temperature is $2K / N_f$ with $N_f = dN$: the collisions do not keep the total momentum, so no degree of freedom is removed.

## The algorithm

```pseudo id=main
ANDERSEN-THERMOSTAT(x, v, m, FORCES, h, S, kT, nu)
L1  (U, f) ← FORCES(x);  p ← 1 - exp(-nu h)
L2  for step ← 1 to S do
L3      v_i ← v_i + (h / 2) f_i / m_i for each particle i     ▷ half kick
L4      x_i ← x_i + h v_i for each particle i                ▷ drift
L5      (U, f) ← FORCES(x)
L6      v_i ← v_i + (h / 2) f_i / m_i for each particle i     ▷ half kick
L7      for each particle i do
L8          if UNIFORM(0, 1) < p then                         ▷ a collision in this step
L9              v_i ← sqrt(kT / m_i) · (d independent standard normals)
L10     record K(v)
L11 return (x, v, the recorded kinetic energies)
```

Lines L3 to L6 are one velocity Verlet step. Lines L7 to L9 are the collisions. With the collision probability $p = 1 - e^{-\nu h}$ per step, the number of steps between two collisions of one particle is geometric, and the times are those of a Poisson process of rate $\nu$ observed at the step times. Andersen (1980) used the Poisson times themselves; to put the collisions at the end of the step is the usual discrete form. The implementation copies $x$ and $v$, so the caller's lists do not change.

## Example

**One step by hand.** One particle in one dimension on a spring, with $m = k = k_B T = 1$ in reduced units, $x = 1$, $v = 0$, $h = 0.1$ and $\nu = 1$. Lines L3 to L6 give $v = -0.05$, $x = 0.995$, $f = -0.995$ and $v = -0.09975$, as on the [molecular dynamics](/molecular-dynamics/) page. The collision probability is $p = 1 - e^{-0.1} = 0.095163$. If the uniform number of line L8 is 0.5, nothing happens and $v = -0.09975$. If it is 0.05, line L9 draws a standard normal, say 0.8, and the new velocity is $\sqrt{1/1} \cdot 0.8 = 0.8$. The old velocity has no effect on the new one.

**The kinetic energy of 20 oscillators.** Take 20 independent oscillators on a line with $m = k = k_B T = 1$, all started at $x = 1$, $v = 0$, so that $N_f = 20$. The canonical law of $K$ has mean 10 and variance 10. Run 6000 steps with $h = 0.05$ (seed 11), drop the first 1000 and estimate the error by 10 batch means:

| $\nu$ | mean of $K$ | variance of $K$ |
|---|---|---|
| 0.1 | $9.04 \pm 0.45$ | $6.98 \pm 1.42$ |
| 1 | $10.02 \pm 0.30$ | $9.13 \pm 0.74$ |
| 10 | $10.05 \pm 0.07$ | $9.60 \pm 0.47$ |

These are measurements. With $\nu = 1$ and $\nu = 10$ both moments agree with the canonical values within two standard errors. With $\nu = 0.1$ each oscillator has only about 25 collisions in the run, so the run is too short and the errors are large, although the method is still correct in the limit. The test of the page checks $\nu = 1$.

**The velocity memory of free particles.** With $f = 0$ a velocity changes only at a collision, so the velocity autocorrelation is $\langle v(0) v(t) \rangle = (k_B T/m) e^{-\nu t}$ (proved below). For 400 free particles with $h = 0.1$ and $\nu = 1$, the measured correlation at a lag of 10 steps is within 0.06 of $e^{-1} = 0.3679$. The diffusion coefficient is then $D = k_B T / (m\nu)$: it is set by the thermostat, not by the physics.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **Each collision keeps the canonical density.** Under $\rho$ the velocity of particle $i$ is independent of everything else and has the Maxwell-Boltzmann law, and line L9 replaces it by a fresh draw from that law.
2. **The Hamiltonian flow keeps it.** The exact flow keeps the volume of phase space and $H$, so it keeps any function of $H$. Velocity Verlet keeps the volume, but keeps $H$ only up to $O(h^2)$, so the sampled density is canonical up to the time step error.
3. **Collision times.** The probability of no collision of a particle in $n$ steps is $e^{-\nu n h}$.
4. **Velocity memory.** For free particles, $\mathbb{E}[v_{ia}(0) v_{ia}(nh)] = (k_B T/m_i) e^{-\nu n h}$, and so $D = k_B T/(m_i \nu)$.

The method samples the canonical ensemble, not the microcanonical one: the collisions change the energy on purpose. Ergodicity is not proved on this page, but the collisions reach every velocity, which removes the main way that deterministic thermostats fail, such as the case of one oscillator on the [Nose-Hoover](/nose-hoover-thermostat/) page. The dynamics are not physical: momentum is not conserved, and time correlation functions decay faster than they should.

## Complexity

Each step does one force evaluation, $O(N)$ work in the Verlet part and $N$ uniform draws. A collision draws $d$ normals; the expected number of collisions per step is $pN \approx \nu h N$. With the all-pairs force loop of the molecular dynamics page, $S$ steps cost $O(S N^2)$ time, and the thermostat adds $O(S N)$. The extra space is $O(N)$ for the copies of $x$, $v$ and $f$.

## Properties

- **Ensemble.** Canonical (NVT), with $N_f = dN$, for any $\nu > 0$, up to the error of the integrator.
- **Randomized.** The trajectory depends on the random numbers. The implementation takes a `random.Random` object, so a fixed seed gives a fixed run.
- **Not time-reversible and not symplectic.** A collision is a random map, not a map of phase space. It is a Markov step that keeps $\rho$.
- **No conserved energy to monitor.** There is no extended energy, so a bad integrator is hidden by the thermostat. Check the integrator without collisions.
- **Momentum.** Not conserved. The centre of mass does a random walk.

## Variants and improvements

- **Massive collisions.** All velocities are redrawn at the same time, every fixed number of steps. This also keeps $\rho$, and is simple, but it gives a stronger jump in the dynamics.
- **Partial refresh.** Replace $v$ by $c\,v + \sqrt{1 - c^2}\sqrt{k_B T/m}\,R$ for all particles in each step. With $c = e^{-\gamma h}$ this is the exact Ornstein-Uhlenbeck step of [Langevin dynamics](/langevin-dynamics/), the O part of the [BAOAB integrator](/baoab-langevin-integrator/).
- **Pairwise collisions.** The Lowe-Andersen thermostat redraws the relative velocity of a pair of close particles along their line of centres. It conserves momentum, so hydrodynamics survive, and it is close in spirit to [dissipative particle dynamics](/dissipative-particle-dynamics/).
- **Kinetic energy rescaling.** [Stochastic velocity rescaling](/stochastic-velocity-rescaling/) changes only the total kinetic energy, with the right random law, and so disturbs the dynamics less.
- **Hamiltonian Monte Carlo.** [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/) redraws all momenta, runs a Verlet trajectory and adds a Metropolis test, which removes the time step error.

## When to use it

Use the Andersen thermostat to sample static canonical averages with a simple and robust method: structure, energies, the [radial distribution function](/radial-distribution-function/). It is a good choice for small systems, where deterministic thermostats can fail to be ergodic. Do not use it to compute diffusion coefficients, viscosities or other [Green-Kubo](/green-kubo-relations/) integrals, unless $\nu$ is so small that the effect is negligible, and then the thermostat is slow. For dynamics, use a weak thermostat that disturbs less, or run NVE after equilibration.

## Pitfalls

- **Too large or too small a rate.** A large $\nu$ makes the dynamics a random walk with a small diffusion coefficient, so the configurations decorrelate slowly. A small $\nu$ gives a slow approach to the temperature. A rate near the inverse of a typical collision time of the physical system is a common choice, and it is a choice, not a rule from theory.
- **Using the dynamics.** Time correlation functions and transport coefficients depend on $\nu$.
- **Fixing $N_f$ wrongly.** The thermostat does not keep the total momentum, so $N_f = dN$. A code that removes the centre of mass motion and also uses this thermostat must decide which $N_f$ it reports.
- **Momentum drift.** The total momentum does a random walk. With a periodic box this is harmless for static averages, but it shows up in a plot of the centre of mass.
- **Correlated random numbers.** The new velocities must be independent of the old ones. Reusing a seed between runs that are averaged together gives correlated runs.

## Implementations

## History

Andersen (1980) introduced the stochastic collisions together with his method for molecular dynamics at constant pressure, in which the volume is an extra dynamical variable with its own mass. The collision method was one of the first ways to run molecular dynamics in the canonical ensemble. Nose (1984) and Hoover (1985) then gave a deterministic method, the [Nose-Hoover thermostat](/nose-hoover-thermostat/), and the constant-pressure idea was extended to a cell that changes shape by [Parrinello and Rahman](/parrinello-rahman-barostat/) (1980, 1981).

## References
