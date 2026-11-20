---
tag: 9VVD0G
kind: algorithm
slug: dissipative-particle-dynamics
name: Dissipative particle dynamics
aliases:
- DPD
area: scientific-computing/multiscale-methods
level: advanced
summary: Moves soft mesoscale beads with conservative, dissipative and random pairwise forces that conserve momentum, so the beads show hydrodynamics.
model: real-ram
complexity:
  vars: {N: the number of beads, S: the number of time steps}
  time: {worst: O(S N^2)}
  space: {extra: O(N)}
properties: {deterministic: false, randomized: true, iterative: true, momentum-conserving: true, symplectic: false}
history:
  year: 1992
  people: [P. J. Hoogerbrugge, J. M. V. A. Koelman]
  note: Hoogerbrugge and Koelman introduced soft beads with pairwise friction and noise in 1992. Espanol and Warren wrote the method as stochastic differential equations in 1995 and found the fluctuation-dissipation relation, and Groot and Warren made it a practical tool in 1997.
prereqs: [molecular-dynamics, langevin-dynamics]
see_also: [smoothed-particle-hydrodynamics, lattice-boltzmann-method, force-matching-coarse-graining, mori-zwanzig-formalism, andersen-thermostat, brownian-dynamics, canonical-ensemble, linked-cell-list]
sources:
  - paper: doi:10.1209/0295-5075/19/3/001
    title: P. J. Hoogerbrugge and J. M. V. A. Koelman, Simulating microscopic hydrodynamic phenomena with dissipative particle dynamics, Europhysics Letters 19(3), 1992, 155-160
    locator: the original method, with soft particles that exchange momentum in pairs
  - paper: doi:10.1209/0295-5075/30/4/001
    title: P. Espanol and P. Warren, Statistical mechanics of dissipative particle dynamics, Europhysics Letters 30(4), 1995, 191-196
    locator: the stochastic differential equations of DPD, the Fokker-Planck equation and the fluctuation-dissipation relation for the weight functions and the noise amplitude
  - paper: doi:10.1063/1.474784
    title: "Robert D. Groot and Patrick B. Warren, Dissipative particle dynamics: Bridging the gap between atomistic and mesoscopic simulation, The Journal of Chemical Physics 107(11), 1997, 4423-4435"
    locator: the choice of the conservative force and the parameters for practice, and the modified velocity Verlet scheme with the parameter lambda
  - paper: doi:10.1137/S1064827501392879
    title: Tony Shardlow, Splitting for dissipative particle dynamics, SIAM Journal on Scientific Computing 24(4), 2003, 1267-1282
    locator: the splitting of the dynamics into conservative steps and pairwise friction and noise steps
  - paper: doi:10.1063/1.4979514
    title: "Pep Espanol and Patrick B. Warren, Perspective: Dissipative particle dynamics, The Journal of Chemical Physics 146(15), 2017, 150901"
    locator: a review of the method, its variants and its links to coarse graining
---

Dissipative particle dynamics (DPD) is a particle method for soft matter at scales between atoms and continua. Each bead stands for a cluster of molecules. Pairs of beads within a cutoff feel three forces along the line between them: a soft repulsion, a friction that acts on the relative velocity, and a random force. The friction and the random force are tied by a fluctuation-dissipation relation, so the beads sample the [canonical ensemble](/canonical-ensemble/) at a set temperature (a theorem for the continuous-time dynamics). Every force acts in equal and opposite pairs, so the total momentum is conserved and the beads show hydrodynamic flow at large scales. This is the difference from [Langevin dynamics](/langevin-dynamics/), whose friction acts against a fixed background and destroys momentum. The method sits between [molecular dynamics](/molecular-dynamics/) and continuum solvers such as [smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/) and the [lattice Boltzmann method](/lattice-boltzmann-method/).

## In plain words

Imagine a liquid made of soft balls instead of hard molecules. Each ball is a small blob of many molecules. When two balls come close, they push each other away gently, so they can even overlap a little. They also rub against each other: if they move apart or together, a friction slows down their difference in speed. And they get random kicks, one kick per pair, equal and opposite on the two balls.

The friction takes energy out and the kicks put energy in. If the two are set in the right ratio, the balls settle at the temperature you want. Because every push, rub and kick acts on both balls of a pair with opposite signs, the liquid as a whole never gains or loses momentum. That is why the balls flow like a real liquid, with waves and vortices.

## The problem

The input is a set of $N$ beads of mass $1$ with positions $x_i$ and velocities $v_i$ in a periodic box of side $L$ in two dimensions, a cutoff $r_c$, a repulsion strength $a$, a friction $\gamma$, a noise amplitude $\sigma$ and a time step $h$. For a pair with $r_{ij} = |x_i - x_j| < r_c$ (with the minimum image), let $e_{ij} = (x_i - x_j) / r_{ij}$, $v_{ij} = v_i - v_j$ and $w(r) = 1 - r / r_c$. The force on bead $i$ from bead $j$ is $F_{ij} = (F^C_{ij} + F^D_{ij} + F^R_{ij}) e_{ij}$ with

$$F^C_{ij} = a\, w(r_{ij}), \qquad F^D_{ij} = -\gamma\, w^D(r_{ij})\, (e_{ij} \cdot v_{ij}), \qquad F^R_{ij} = \sigma\, w^R(r_{ij})\, \theta_{ij} / \sqrt{h},$$

where $\theta_{ij} = \theta_{ji}$ is a standard normal number drawn once per pair and step. The conservative force comes from the soft pair potential $\frac{a r_c}{2} w(r)^2$. The goal is a trajectory whose positions and velocities sample the canonical distribution $\propto \exp(-H / k_B T)$, $H = \sum_i |v_i|^2 / 2 + U$, on the surface of fixed total momentum. The fluctuation-dissipation relation of Espanol and Warren (1995) gives this for the continuous-time dynamics:

$$w^D = (w^R)^2, \qquad \sigma^2 = 2 \gamma k_B T .$$

The page uses $w^R = w$ and $w^D = w^2$. With $\sigma$ and $\gamma$ fixed, the temperature is $k_B T = \sigma^2 / (2 \gamma)$. The kinetic temperature of a run is $\sum_i |v_i|^2 / N_f$ with $N_f = 2N - 2$, because the two components of the total momentum are fixed.

## The algorithm

```pseudo id=main
DPD-STEP(x, v, F, h, λ)                           ▷ F holds the forces of the last step
L1  x_i ← x_i + h v_i + (h²/2) F_i  (mod L)        for every bead i
L2  ṽ_i ← v_i + λ h F_i                            ▷ predicted velocity for the friction
L3  F' ← DPD-FORCES(x, ṽ)
L4  v_i ← v_i + (h/2) (F_i + F'_i)                 for every bead i
L5  return F'
DPD-FORCES(x, v)
L6  for each pair i < j with r_ij < r_c, starting from F_i = 0 for all i
L7      w ← 1 - r_ij / r_c
L8      s ← a w - γ w² (e_ij · v_ij) + σ w θ_ij / √h       ▷ θ_ij standard normal, one per pair
L9      F_i ← F_i + s e_ij,  F_j ← F_j - s e_ij
```

Lines L1 to L5 are the modified velocity Verlet scheme of Groot and Warren (1997). The friction depends on the velocities, so the new forces need the new velocities, which in turn need the new forces. Line L2 breaks this loop with a predicted velocity; $\lambda = 1/2$ is the natural choice for [Verlet integration](/verlet-integration/), and Groot and Warren tuned $\lambda$ as a free parameter. The noise term has the factor $1 / \sqrt{h}$ because the impulse of a Wiener process over a step of length $h$ has standard deviation $\sqrt{h}$, and the force is the impulse divided by $h$. Line L9 adds the pair force to bead $i$ and subtracts it from bead $j$; the random number is shared by the two beads.

## Example

**Two beads by hand.** Put two beads on the $x$ axis at distance $0.5$, closing at relative speed $1$, with $a = 25$, $\gamma = 4.5$, $\sigma = 0$ and $r_c = 1$. Then $w = 0.5$ and $e_{01} \cdot v_{01} = -1$, so line L8 gives $s = 25 \cdot 0.5 - 4.5 \cdot 0.25 \cdot (-1) = 12.5 + 1.125 = 13.625$. The repulsion and the friction both push the beads apart, with force $13.625$ on each bead in opposite directions. At distance $1$, $w = 0$ and the force is zero.

**Temperature.** A fluid of $N = 48$ beads in a box of side $4$ (density $3$) with $a = 25$, $\gamma = 4.5$ and $\sigma = 3$ has the target $k_B T = 9 / 9 = 1$; with $\gamma = 9$ it has $k_B T = 1/2$. These parameters are choices of the page. The mean kinetic temperature over 4 runs of 30 time units with $\lambda = 1/2$ is $1.0042$ at $h = 0.01$, $1.0077$ at $h = 0.02$, $1.0337$ at $h = 0.04$ and $1.0698$ at $h = 0.06$, with $N_f = 2N - 2 = 94$. The noise of one run is about $\pm 0.025$. So the temperature is right to within the noise at small steps, and the step size error grows quickly above $h = 0.02$. These are measurements.

**Energy without the thermostat.** With $\gamma = \sigma = 0$ the scheme is velocity Verlet for the soft potential. Over 3 time units, the largest error in the energy per bead is $0.0594$, $0.0125$ and $0.00247$ for $h = 0.02$, $0.01$ and $0.005$, against an energy of about $10.13$ per bead. Each halving of $h$ divides the error by about $5$, which is second order or a bit better (measurement).

## Correctness

The proof in the proofs file has two parts. First, the pair force of line L8 is the same scalar for $(i, j)$ and $(j, i)$, because $e_{ij} \cdot v_{ij}$ and $\theta_{ij}$ are symmetric, and $e_{ji} = -e_{ij}$. So the forces are equal and opposite, the total force is zero, and line L4 keeps the total momentum exactly in exact arithmetic (a theorem; the tests find drift at the level of rounding, below $10^{-11}$ over 200 steps). The conservative part is the negative gradient of $U = \sum_{i < j} \frac{a r_c}{2} w(r_{ij})^2$.

Second, for the stochastic differential equations of DPD, the limit $h \to 0$ of the scheme, the Gibbs density $\rho \propto \exp(-H / k_B T)$ is stationary if $w^D = (w^R)^2$ and $\sigma^2 = 2 \gamma k_B T$. The proof applies the Fokker-Planck operator to $\rho$: the Hamiltonian part gives zero, and the part of each pair is proportional to $\gamma w^D - \sigma^2 (w^R)^2 / (2 k_B T)$, which the relation makes zero. Stationarity does not prove ergodicity, and the scheme at finite $h$ samples a slightly different distribution; that error is measured above, not bounded.

## Complexity

In the [real RAM](/real-ram/) model, lines L6 to L9 visit all $N (N - 1) / 2$ pairs, so a step costs $O(N^2)$ and $S$ steps cost $O(S N^2)$. With a [linked cell list](/linked-cell-list/) of cell side $r_c$, a step costs $O(N)$ at fixed density, because each bead has a bounded number of neighbors. The memory is $O(N)$ for positions, velocities and two force arrays. Each step needs one random number per interacting pair. The soft repulsion allows time steps much larger than in atomistic molecular dynamics, which is the main source of the speed of the method.

## Properties

- **Momentum conservation.** The total momentum is exact in exact arithmetic (theorem). Angular momentum is also conserved for an isolated system, because all pair forces are central; in a periodic box it is not defined.
- **Galilean invariance.** The forces depend only on relative positions and relative velocities, so a uniform flow does not change the dynamics (theorem). A Langevin thermostat does not have this property.
- **Canonical sampling.** The Gibbs distribution is stationary for the continuous-time dynamics under the fluctuation-dissipation relation (theorem); at finite $h$ the temperature has a step size error (measurement above).
- **Hydrodynamics.** Momentum conservation and local interactions give flow governed at large scales by the Navier-Stokes equations, with a viscosity that depends on $\gamma$, $r_c$ and the density (a known result of kinetic theory, not proved here).
- **Soft potential.** The repulsion $a w$ is bounded, so beads can overlap and the fluid has no hard core. This gives large time steps but a fluid that is much more compressible than a real liquid.
- **Not symplectic.** With friction and noise the scheme is stochastic and dissipative; without them it is velocity Verlet.

## Variants and improvements

- **Splitting schemes.** Shardlow (2003) splits each step into the conservative forces and the friction and noise of each pair, and solves the pair parts one after another. This removes most of the step size error in the temperature at a small extra cost.
- **Other thermostats with momentum conservation.** The Lowe-Andersen scheme replaces friction and noise by pairwise velocity exchanges with a heat bath, in the spirit of the [Andersen thermostat](/andersen-thermostat/) but on relative velocities.
- **Other weights.** The relation only needs $w^D = (w^R)^2$, so other choices of $w^R$, for example a power of $1 - r / r_c$, keep the canonical distribution and change the transport coefficients such as the viscosity.
- **Energy-conserving and many-body DPD.** Variants add an internal energy per bead, so that heat flows, or let the repulsion depend on the local density, so that the fluid can have a liquid-vapor interface.
- **Coarse-grained forces from atomistic data.** The conservative force can come from [force matching](/force-matching-coarse-graining/) or [iterative Boltzmann inversion](/iterative-boltzmann-inversion/), and the friction and noise from the [Mori-Zwanzig formalism](/mori-zwanzig-formalism/) in its Markov approximation.

## When to use it

Use DPD for complex fluids where flow matters at scales of tens of nanometers to microns: polymer solutions and melts, block copolymers, membranes, vesicles and colloids. Use [Brownian dynamics](/brownian-dynamics/) or [Langevin dynamics](/langevin-dynamics/) when hydrodynamic interactions do not matter, because they are simpler and give the right equilibrium. Use the [lattice Boltzmann method](/lattice-boltzmann-method/) or [smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/) when the fluid is a plain continuum and thermal noise is small. Use [molecular dynamics](/molecular-dynamics/) when chemical detail matters.

## Pitfalls

- **The wrong dissipative weight.** Writing line L8 with $\gamma w (e_{ij} \cdot v_{ij})$, the same weight as the noise, breaks the relation $w^D = (w^R)^2$. With $\gamma = 4.5$ and $\sigma = 3$, the target $k_B T = 1$ becomes a kinetic temperature of about $0.36$ in the example fluid at $h = 0.02$ (measurement, 4 runs). Use $\gamma w^2 (e_{ij} \cdot v_{ij})$, as in line L8.
- **The wrong noise amplitude.** Choosing $\sigma^2 = \gamma k_B T$ halves the temperature, because the stationary temperature is $\sigma^2 / (2 \gamma)$ (theorem). Use $\sigma = \sqrt{2 \gamma k_B T}$.
- **No factor $1 / \sqrt{h}$.** Writing line L8 as $\sigma w \theta_{ij}$ makes the noise impulse of a step $h \sigma w \theta$ instead of $\sqrt{h} \sigma w \theta$, so the temperature falls with $h$ and goes to zero as $h \to 0$. Keep $\theta_{ij} / \sqrt{h}$.
- **Two random numbers per pair.** Drawing one $\theta$ for bead $i$ and another for bead $j$ in line L9 makes the random forces unequal, and the total momentum drifts like a random walk. Draw one $\theta_{ij}$ per pair and step, and use it for both beads.
- **The wrong count of degrees of freedom.** With zero total momentum, the kinetic temperature is $\sum_i |v_i|^2 / (2N - 2)$ in two dimensions. Dividing by $2N$ reports a temperature that is low by the factor $(N - 1) / N$.
- **Too large a step.** The temperature error grows from below $1\%$ at $h = 0.02$ to $7\%$ at $h = 0.06$ in the example. Check the kinetic temperature against $\sigma^2 / (2 \gamma)$ for each new set of parameters.

## Implementations

## History

Hoogerbrugge and Koelman introduced dissipative particle dynamics in 1992 to simulate hydrodynamics of complex fluids with soft particles that exchange momentum in pairs. Espanol and Warren wrote the method in 1995 as stochastic differential equations, derived its Fokker-Planck equation and found the fluctuation-dissipation relation between the weights and the amplitudes that makes the Gibbs distribution stationary. Groot and Warren made DPD a practical tool in 1997, with a choice of the conservative force and parameters for real fluids and the modified velocity Verlet scheme. Shardlow gave splitting integrators in 2003. Espanol and Warren reviewed the method in 2017.

## References
