---
tag: YHB5S5
kind: algorithm
slug: langevin-dynamics
name: Langevin dynamics
aliases:
- Langevin thermostat
area: scientific-computing/molecular-simulation
level: core
summary: Adds friction and a matching random force to Newton's equations so that the dynamics samples the canonical ensemble.
model: real-ram
complexity:
  vars: {N: the number of particles, S: the number of time steps}
  time: {worst: O(S N^2)}
  space: {extra: O(N)}
properties: {deterministic: false, randomized: true, iterative: true, symplectic: false, symmetric: true}
history:
  year: 1908
  people: [Paul Langevin]
  note: Langevin wrote the equation of motion of a Brownian particle as Newton's law with a friction force and a random force; in molecular simulation the same equation became a thermostat and a model of an implicit solvent.
prereqs: [canonical-ensemble, stochastic-differential-equation, verlet-integration]
see_also: [baoab-langevin-integrator, brownian-dynamics, stochastic-velocity-rescaling, andersen-thermostat, nose-hoover-thermostat, metropolis-adjusted-langevin-algorithm, euler-maruyama-method, dissipative-particle-dynamics]
sources:
  - paper: doi:10.1103/PhysRevE.75.056707
    title: Giovanni Bussi and Michele Parrinello, Accurate sampling using Langevin dynamics, Physical Review E 75, 056707, 2007
    locator: the splitting with exact Ornstein-Uhlenbeck half steps around velocity Verlet and the effective energy
  - book: isbn:9783319163741
    title: Ben Leimkuhler and Charles Matthews, Molecular Dynamics, With Deterministic and Stochastic Numerical Methods, Springer, 2015
    locator: Chapter 6, the canonical distribution and stochastic differential equations, and Chapter 7, numerical methods for stochastic molecular dynamics
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: the chapter on mesoscale methods, Langevin and Brownian dynamics
  - book: isbn:9780198525264
    title: Mark E. Tuckerman, Statistical Mechanics, Theory and Molecular Simulation, Oxford University Press, 2010
    locator: the chapter on the Langevin and generalized Langevin equations
---

Langevin dynamics adds two forces to Newton's equations of motion: a friction force $-m\gamma v$ that slows each particle down, and a random force that kicks it. The size of the random force is tied to the friction and the temperature, so that the [canonical ensemble](/canonical-ensemble/) at that temperature is the stationary distribution (a theorem). In [molecular dynamics](/molecular-dynamics/) it is a thermostat, often called the Langevin thermostat. In physics and chemistry it is also a model of a particle in a solvent: the solvent molecules are not simulated, and their effect is the friction and the random kicks. The page gives the equations and the OBABO integrator of Bussi and Parrinello (2007), which solves the friction and noise part exactly.

## In plain words

Picture a ball moving among many small, fast molecules that are too many to simulate. They slow the ball down, like a thick fluid, and they also give it small random knocks.

Langevin dynamics adds exactly these two effects to each atom. The slowing down takes energy away and the knocks put energy in. When the two are matched to the temperature, they balance on average, and the atoms visit their states with the right weights for that temperature.

The program alternates a short step of ordinary motion with a step of slowing and knocking. The slowing and knocking part is solved exactly, so its size does not limit the time step.

## The problem

The input is positions $x_i \in \mathbb{R}^d$, velocities $v_i$ and masses $m_i$ of $N$ particles, a force routine for $f_i = -\nabla_i U$, a time step $h$, a number of steps $S$, the target $k_B T$, the friction coefficient $\gamma \ge 0$ (a rate, with units of inverse time) and a random number source. The Langevin equations are
$$dx_i = v_i\, dt, \qquad m_i\, dv_i = f_i\, dt - m_i \gamma v_i\, dt + \sqrt{2 m_i \gamma k_B T}\, dW_i,$$
with independent Wiener processes $W_i$ in $\mathbb{R}^d$. The amplitude of the noise follows from the fluctuation-dissipation relation, and with it the canonical density $\exp(-(K + U)/k_B T)$ is stationary. The output is the trajectory and samples of $(x, v)$. The noise and the friction act on each particle against a fixed background, so the total momentum is not conserved: for the kinetic temperature $T = 2K / (N_f k_B)$, use $N_f = dN$, less one for each constraint.

## The algorithm

```pseudo id=main
LANGEVIN-OBABO(x, v, m, FORCES, h, S, kT, gamma)
L1  f ← FORCES(x); c ← exp(-gamma h / 2)
L2  for step ← 1 to S do
L3      v_i ← c v_i + sqrt((1 - c²) kT / m_i) R_i for each particle i   ▷ O: exact half step, R_i standard normal in R^d
L4      v_i ← v_i + (h / 2) f_i / m_i for each particle i               ▷ B: half kick
L5      x_i ← x_i + h v_i for each particle i                          ▷ A: drift
L6      f ← FORCES(x)
L7      v_i ← v_i + (h / 2) f_i / m_i for each particle i               ▷ B: half kick
L8      v_i ← c v_i + sqrt((1 - c²) kT / m_i) R_i for each particle i   ▷ O: exact half step, fresh R_i
L9      every k steps, record a copy of (x, v)
L10 return (x, v, the recorded samples)
```

The friction and the noise alone form an Ornstein-Uhlenbeck process in $v$, and lines L3 and L8 are its exact solution over a time $h/2$. Lines L4 to L7 are a velocity Verlet step. The letters name the parts: O for Ornstein-Uhlenbeck, B for the kick and A for the drift, so the step is O B A B O. With $\gamma = 0$ it is velocity Verlet. The order B A O A B is the [BAOAB integrator](/baoab-langevin-integrator/), which samples positions more accurately.

## Example

**One step by hand.** One particle on a spring with $m = k = k_B T = 1$ in reduced units, $x = 1$, $v = 0$, $h = 0.1$ and $\gamma = 1$. Then $c = e^{-0.05} = 0.951229$ and $\sqrt{1 - c^2} = 0.308484$. With the normal draws $R = 0.5$ on line L3 and $R = -0.3$ on line L8:

| after | L3 | L4 | L5 | L7 | L8 |
|---|---|---|---|---|---|
| $x$ | 1 | 1 | 1.010424 | 1.010424 | 1.010424 |
| $v$ | 0.154242 | 0.104242 | 0.104242 | 0.053721 | $-0.041444$ |

**The time step error on a harmonic oscillator.** For $U = \frac12 k x^2$ with $\omega^2 = k/m$ and $h\omega < 2$, the stationary law of OBABO is normal with $\langle v^2 \rangle = k_B T / m$ exactly and $\langle x^2 \rangle = (k_B T / k) / (1 - h^2\omega^2 / 4)$, for any $\gamma > 0$ (a theorem, Claim 4 of the proof). A run of 50 oscillators with $m = k = k_B T = \gamma = 1$, 4000 steps from rest, a sample every 5 steps and the first 200 steps dropped (seed 1) gives:

| $h$ | measured $\langle x^2 \rangle$ | exact $\langle x^2 \rangle$ | measured $\langle v^2 \rangle$ |
|---|---|---|---|
| 0.5 | 1.0719 | 1.0667 | 0.9914 |
| 1 | 1.3193 | 1.3333 | 0.9994 |
| 1.5 | 2.2885 | 2.2857 | 0.9971 |

The canonical values are 1 and 1. The velocities are right for any step, and the positions carry an $O(h^2)$ error, which BAOAB removes for this example.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **The canonical density is stationary** for the Fokker-Planck equation of the Langevin equations: the Hamiltonian part and the friction and noise part each keep it.
2. **The O step is exact.** Lines L3 and L8 draw the Ornstein-Uhlenbeck solution over a time $h/2$, which keeps the Maxwell law of $v$ exactly.
3. **The step** is O around velocity Verlet, so it keeps the canonical law up to the $O(h^2)$ error of the Verlet part.
4. **On a harmonic oscillator** the stationary law of the step is the normal law above, and it is unique.
5. **Limits.** With $\gamma = 0$ the step is velocity Verlet. With no forces the velocities are an exact sample path of the Ornstein-Uhlenbeck process.

For $\gamma > 0$ and a smooth potential that grows at infinity, the continuous Langevin process is ergodic, since the noise reaches all variables through the coupling of $x$ and $v$ (a theorem). So unlike the Nose-Hoover thermostat, Langevin dynamics needs no hypothesis of ergodicity.

## Complexity

Each step does one force evaluation, $2dN$ normal draws and $O(N)$ other work. With the all-pairs forces of the molecular dynamics page, $S$ steps take $O(S N^2)$ time; with neighbor lists the forces take $O(N)$ per step. The extra space is $O(N)$ for the copies of $x$ and $v$, plus the samples that are recorded.

## Properties

- **Ensemble.** Canonical (NVT), up to the time step error, for any $\gamma > 0$. Ergodicity holds without an extra hypothesis.
- **Local.** Each particle has its own friction and noise, so the thermostat works on small, stiff and harmonic systems and on systems with hot spots.
- **Dynamics are changed.** The friction slows diffusion: a free particle has the diffusion constant $D = k_B T / (m\gamma)$ (a theorem), and in a liquid a small $\gamma$ changes $D$ little while a large one makes it much smaller. Momentum is not conserved, so hydrodynamic correlations are damped.
- **Exact velocity distribution** on a harmonic oscillator for any step, as in the example.
- **Time-symmetric splitting**, but not reversible as a deterministic map, since fresh noise is drawn.

## Variants and improvements

- **BAOAB.** The [BAOAB integrator](/baoab-langevin-integrator/) uses the same parts in the order B A O A B and has a much smaller error in configurational averages, in particular for large friction.
- **Overdamped limit.** For large $\gamma$ the velocities relax at once, and the motion of positions alone is [Brownian dynamics](/brownian-dynamics/).
- **Older integrators.** Schneider and Stoll (1978), van Gunsteren and Berendsen (1982) and Brunger, Brooks and Karplus (1984) gave earlier schemes. A direct [Euler-Maruyama](/euler-maruyama-method/) step is simple but has a larger error and no exact O part.
- **Momentum-conserving noise.** [Dissipative particle dynamics](/dissipative-particle-dynamics/) puts friction and noise on pairs of particles, so momentum is conserved and hydrodynamics survive.
- **Global thermostats.** [Stochastic velocity rescaling](/stochastic-velocity-rescaling/) acts on the total kinetic energy only and changes the dynamics less.
- **Sampling.** In statistics, the [Metropolis-adjusted Langevin algorithm](/metropolis-adjusted-langevin-algorithm/) uses the overdamped Langevin equation as a proposal and removes the time step error with an accept-reject step.

## When to use it

Use Langevin dynamics when the goal is to sample the canonical ensemble robustly, for example for free energies, structure and equilibrium averages, or to model a solute in an implicit solvent. A common heuristic is a small $\gamma$, about $1\ \mathrm{ps}^{-1}$ in atomistic simulation, when dynamics matter, and a larger one when only sampling matters. Avoid it when transport properties such as viscosity or diffusion constants are measured in an explicit solvent, where a global thermostat changes them less.

## Pitfalls

- **Too large a friction.** The dynamics then crawl, and sampling of slow motions gets slower, not faster.
- **The same random numbers in every run.** Restarts with the same seed repeat the noise, and parallel copies with one seed are correlated.
- **A wrong $N_f$.** Momentum is not conserved, so do not subtract $d$ for the centre of mass when the kinetic temperature is computed.
- **Units of $\gamma$.** Some codes give a friction per mass, others a collision frequency, others a damping time $1/\gamma$. Check which.
- **Judging the step by the velocities.** The kinetic temperature is right even when the step is too large; check configurational quantities such as $\langle x^2 \rangle$ or the potential energy.

## Implementations

## History

Langevin (1908) wrote the equation of a Brownian particle as Newton's law with friction and a random force. Its use as a numerical method in molecular simulation came much later: Schneider and Stoll (1978) used it for phase transitions, and van Gunsteren and Berendsen (1982) and Brunger, Brooks and Karplus (1984) gave integrators for molecules. Bussi and Parrinello (2007) gave the splitting with exact Ornstein-Uhlenbeck half steps used here. Leimkuhler and Matthews (2013) studied the order of the parts and found the more accurate BAOAB.

## References
