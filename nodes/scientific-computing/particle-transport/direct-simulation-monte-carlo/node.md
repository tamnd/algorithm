---
tag: 8HF9Q3
kind: algorithm
slug: direct-simulation-monte-carlo
name: Direct simulation Monte Carlo
aliases:
- DSMC
- "Bird's method"
area: scientific-computing/particle-transport
level: advanced
summary: Simulates a dilute gas by moving particles freely for a time step and then colliding random pairs in each cell with the probabilities of kinetic theory, for the Boltzmann equation.
model: real-ram
complexity:
  vars: {N: the number of simulated particles, S: the number of time steps}
  time: {average: O(S N)}
  space: {extra: O(N)}
properties: {deterministic: false, randomized: true, exact: false, iterative: true, conservative: true}
history:
  year: 1963
  people: [Graeme A. Bird]
  note: Bird simulated the approach to equilibrium of a hard-sphere gas in 1963 and developed DSMC for rarefied flows over the next decades. He gave the no-time-counter scheme in 1989. Wagner proved a convergence result in 1992.
prereqs: [monte-carlo-integration, rejection-sampling]
see_also: [molecular-dynamics, lattice-boltzmann-method, bgk-collision-operator, chapman-enskog-expansion, navier-stokes-equations, kinetic-monte-carlo, analog-monte-carlo-transport, operator-splitting]
sources:
  - book: isbn:9780198561958
    title: G. A. Bird, Molecular Gas Dynamics and the Direct Simulation of Gas Flows, Clarendon Press, Oxford, 1994
    locator: the chapters on the DSMC procedures, with the no-time-counter selection of collision pairs
  - paper: doi:10.1063/1.1710976
    title: G. A. Bird, Approach to translational equilibrium in a rigid sphere gas, Physics of Fluids 6(10), 1963, 1518-1519
    locator: the first simulation of a gas by random collisions of particle pairs
  - paper: doi:10.1007/BF01055714
    title: Wolfgang Wagner, A convergence proof for Bird's direct simulation Monte Carlo method for the Boltzmann equation, Journal of Statistical Physics 66(3-4), 1992, 1011-1044
    locator: the limit of the particle system as the number of particles grows
  - paper: doi:10.1063/1.869674
    title: Francis J. Alexander, Alejandro L. Garcia and Berni J. Alder, Cell size dependence of transport coefficients in stochastic particle algorithms, Physics of Fluids 10(6), 1998, 1540-1542
    locator: the error of the viscosity and the heat conductivity as a function of the cell size
  - paper: doi:10.1063/1.168619
    title: Francis J. Alexander and Alejandro L. Garcia, The direct simulation Monte Carlo method, Computers in Physics 11(6), 1997, 588-593
    locator: a short account of the algorithm, with the selection of pairs and the time step and cell size rules
---

Direct simulation Monte Carlo (DSMC) computes flows of a dilute gas, where the mean free path is not small compared with the size of the flow: the upper atmosphere, a spacecraft at re-entry, a vacuum pump, a micro device. It represents the gas by simulated particles, each standing for $F_N$ real molecules, and splits each time step in two parts: all particles move freely, and then, in each cell of a mesh, randomly chosen pairs of particles in the same cell collide with probabilities from kinetic theory. Collisions conserve momentum and energy exactly. The method is a stochastic solver for the Boltzmann equation of a dilute gas, which has no page here; it is not a model of the [linear Boltzmann transport equation](/linear-boltzmann-transport-equation/) of neutrons, because the collision partners are other gas particles and the problem is nonlinear. It differs from [molecular dynamics](/molecular-dynamics/), which integrates the exact paths of interacting molecules, and from the [lattice Boltzmann method](/lattice-boltzmann-method/), which evolves velocity distributions on a lattice with a model collision operator such as [BGK](/bgk-collision-operator/). The page sits in particle transport because DSMC and neutron Monte Carlo share the idea of free flights and sampled collisions.

## In plain words

A gas is a huge number of molecules that fly in straight lines and now and then hit each other. When the gas is thin, each molecule flies a long way between hits, and the usual equations of fluid flow stop being correct.

DSMC keeps a sample of the molecules on the computer, a few million instead of billions of billions. It cuts time into short steps. In each step, every sample molecule flies in a straight line. Then the space is cut into small boxes, and in each box the method picks random pairs and lets some of them collide, more often when they move fast relative to each other. A collision turns the pair to new directions but keeps their total momentum and energy. Averages over many steps give the density, speed and temperature of the flow.

## The problem

The Boltzmann equation of a dilute monatomic gas evolves the velocity distribution $f(x, v, t)$, the number density of molecules in position and velocity, by free streaming and binary collisions:

$$\frac{\partial f}{\partial t} + v \cdot \nabla_x f = \int \int \big(f(v') f(v_1') - f(v) f(v_1)\big)\, g\, \sigma(g, \Omega)\, d\Omega\, dv_1,$$

where $g = |v - v_1|$ is the relative speed, $\sigma(g, \Omega)$ the differential cross section and $v', v_1'$ the velocities after a collision. For hard spheres of diameter $d$ the total cross section is $\sigma_T = \pi d^2$, the scattering is isotropic in the centre of mass frame, and the mean free path at equilibrium is $\lambda = 1/(\sqrt{2}\, n \sigma_T)$ for the number density $n$. The flow regime is set by the Knudsen number $\mathrm{Kn} = \lambda / \ell$ with $\ell$ a length of the flow: the [Navier-Stokes equations](/navier-stokes-equations/) hold for small Kn, with the [Chapman-Enskog expansion](/chapman-enskog-expansion/) as the link, and DSMC is used for Kn above about 0.01 or 0.1. The input is the geometry, the boundary conditions (walls, inflow, vacuum), the molecular model and the initial state; the output is averages of $f$ over cells and time: density, flow velocity, temperature, stress and heat flux.

## The algorithm

```pseudo id=main
DSMC-STEP(particles, Δt)                         ▷ unit mass, positions x_i, velocities v_i
L1  for each particle i do x_i ← x_i + v_i Δt, then apply the boundary conditions
L2  sort the particles into cells
L3  for each cell c with N_c ≥ 2 particles do
L4      M ← ½ N_c (N_c - 1) F_N (σ_T g)_max,c Δt / V_c + carry_c; carry_c ← M - ⌊M⌋, M ← ⌊M⌋
L5      repeat M times: pick a pair (i, j) of distinct particles of the cell at random
L6          g ← |v_i - v_j|
L7          if σ_T g > (σ_T g)_max,c then (σ_T g)_max,c ← σ_T g
L8          with probability σ_T g / (σ_T g)_max,c do               ▷ else the pair does not collide
L9              n ← a unit vector uniform on the sphere              ▷ hard spheres scatter isotropically
L10             v_cm ← (v_i + v_j)/2, v_i ← v_cm + g n/2, v_j ← v_cm - g n/2
```

Line L4 is Bird's no-time-counter (NTC) scheme. A pair collides in time $\Delta t$ with probability $F_N \sigma_T g \Delta t / V_c$, so the expected number of collisions in the cell is $\frac{1}{2} N_c(N_c - 1) F_N \langle \sigma_T g \rangle \Delta t / V_c$. NTC draws $M$ candidate pairs with the upper bound $(\sigma_T g)_{\max}$ and accepts each with the ratio $\sigma_T g/(\sigma_T g)_{\max}$, which is [rejection sampling](/rejection-sampling/) of the pairs; it costs $O(N_c)$ per cell instead of $O(N_c^2)$ for a test of every pair. Bird writes the candidate count with $N_c \bar N_c$, the product of the number of particles and its time average, in place of $N_c(N_c - 1)$; the form above gives the exact pair rate when $N_c$ is fixed. The fractional part $M - \lfloor M \rfloor$ carries over to the next step, so no collisions are lost on average.

Line L10 keeps the centre of mass velocity and the relative speed, so the momentum $v_i + v_j$ and the energy $\frac{1}{2}(|v_i|^2 + |v_j|^2) = |v_{cm}|^2 + g^2/4$ do not change. For other molecular models, such as the variable hard sphere model, $\sigma_T$ depends on $g$ and line L9 samples the deflection angle from the model.

## Example

**A gas at rest.** In one cell of unit volume with $N = 400$ particles, $F_N = 1$, $\sigma_T = 0.002$ and a Maxwellian of temperature $T = 1$ (units $m = k = 1$), the mean relative speed is $\langle g \rangle = 4\sqrt{kT/(\pi m)}$. The sample drawn with `random.Random(2)` has the kinetic temperature $0.9477$, so $\langle g \rangle = 2.1969$, and the expected number of collisions in 150 steps of $\Delta t = 0.1$ is $\frac{1}{2} \cdot 400 \cdot 399 \cdot 0.002 \cdot 2.1969 \cdot 15 = 5259$. The run with `random.Random(2)` gave 5241 collisions from 17501 candidates, so about 30 percent of the candidates were accepted. The difference, $-18$, is well inside one standard deviation of a Poisson count, $\sqrt{5259} = 73$.

**Relaxation to the Maxwellian.** Start 1500 particles with speed 1 in random directions, so $\langle c^4 \rangle / \langle c^2 \rangle^2 = 1$. The Maxwellian value is $15/9 = 5/3$. With $F_N \sigma_T / V = 1/1500$ and $\Delta t = 1$ (`random.Random(3)`):

| steps | collisions per particle | $\langle c^4 \rangle / \langle c^2 \rangle^2$ |
|---|---|---|
| 0 | 0 | 1.000 |
| 1 | 1.14 | 1.215 |
| 2 | 2.46 | 1.414 |
| 3 | 3.75 | 1.511 |
| 5 | 6.10 | 1.643 |
| 10 | 12.67 | 1.675 |
| 25 | 31.93 | 1.740 |

The ratio reaches the Maxwellian value after about 5 collisions per particle, and then fluctuates around it: the sample estimate of $\langle c^4 \rangle$ from 1500 particles has a standard deviation of about 0.08 in the ratio. The energy and the momentum of the gas are the same at every step to rounding.

## Correctness

Two claims are theorems. First, every collision conserves momentum and energy exactly (line L10), so the totals of the gas change only at the boundaries. Second, in a cell with $N_c$ particles and fixed velocities, NTC gives each unordered pair $\{i, j\}$ an expected number of collisions $F_N \sigma_T g_{ij} \Delta t / V_c$ per step, the same as the pair collision rate of the stochastic Kac model of the gas, if $(\sigma_T g)_{\max}$ is a true upper bound. Hard spheres scatter isotropically in the centre of mass frame, so line L9 samples the exact post-collision law. The proofs are below.

The link to the Boltzmann equation is a theorem from the literature, not proved here. Wagner (1992) proved that, as the number of particles goes to infinity with fixed cells and time step, the empirical measure of Bird's particle system converges to the solution of an equation of Boltzmann type in which particles collide with partners anywhere in the same cell, a mollified Boltzmann equation. The Boltzmann equation itself is the further limit of small cells and small time steps. The errors of a finite cell and step are known from analysis and measurement: Alexander, Garcia and Alder (1998) showed that the viscosity and the heat conductivity of hard-sphere DSMC have an error that grows like $(\Delta x/\lambda)^2$. The usual practice of cells smaller than about a third of a mean free path, time steps smaller than the mean collision time and about 20 particles per cell is a rule of thumb, not a theorem.

## Complexity

A step costs $O(N)$ for the move, $O(N)$ for the sort into cells with a counting sort, and $O(1)$ per candidate pair. The number of candidates per cell is about $\frac{1}{2} N_c^2 F_N (\sigma_T g)_{\max} \Delta t / V_c$, which is $O(N_c)$ when $\Delta t$ is a fixed fraction of the collision time, because $F_N N_c / V_c$ is the real number density. So a step costs $O(N)$ and a run of $S$ steps costs $O(S N)$, with $O(N)$ space. In practice the cost is dominated by the number of particles needed for low noise: the statistical error of a cell average falls like $1/\sqrt{N_c \cdot (\text{number of samples})}$, and low-speed flows, where the signal is small compared with the thermal noise, need very many samples.

## Properties

- **Conservative.** Momentum and energy are conserved in each collision exactly; mass is conserved because particles are never created or destroyed inside the gas.
- **Physical noise.** At equilibrium the fluctuations of DSMC are those of an ideal gas with the simulated number of particles, so they are larger than in the real gas when $F_N > 1$. With $F_N = 1$ the method can be used to study the fluctuations of the gas itself.
- **No closure.** Unlike the Navier-Stokes equations, DSMC needs no constitutive law; viscosity and heat conduction come out of the collisions.
- **Splitting error.** Moving and colliding in separate parts of the step is a form of [operator splitting](/operator-splitting/) with an error that vanishes as $\Delta t \to 0$.
- **Not exact.** For a finite cell size, time step and number of particles, DSMC has errors of all three kinds; only the conservation laws are exact.

## Variants and improvements

- **Other molecular models.** Variable hard sphere and variable soft sphere models fit the temperature dependence of real viscosities; Borgnakke-Larsen exchange handles rotational and vibrational energy of molecules.
- **Other pair selection schemes.** The time counter of Bird's early work, Nanbu's scheme derived directly from the Boltzmann equation, and the majorant frequency scheme select pairs with the same mean rate and different noise.
- **Subcells and nearest neighbours.** Pick collision partners from a subcell or the nearest particle in the cell, which lowers the error of a finite cell without more cells.
- **Chemistry and radiation.** Reactions, ionization and radiation are added as collision outcomes with their own probabilities.
- **Hybrid methods.** Couple DSMC in rarefied regions to a Navier-Stokes solver where the Knudsen number is small.

## When to use it

Use DSMC for rarefied flows, with Knudsen numbers from about 0.01 to the free molecular limit, where the continuum equations fail: hypersonic flow at high altitude, plumes of thrusters in vacuum, flows in micro and nano devices, the gas in a vacuum system. For small Knudsen numbers it is much more expensive than a Navier-Stokes solver, because the cells must resolve the mean free path. For dense gases and liquids use [molecular dynamics](/molecular-dynamics/), because the Boltzmann equation itself assumes binary collisions of uncorrelated particles.

## Pitfalls

- **Cells too large.** Collisions between particles up to a cell apart give too much transport of momentum and energy. The error grows like the square of the cell size over the mean free path.
- **Too few particles per cell.** With $N_c$ near 1 there are hardly any pairs; with the form $N_c^2$ instead of $N_c(N_c - 1)$, a cell with one particle would even get collision candidates. Keep $N_c$ at about 10 or more.
- **A wrong upper bound.** If $(\sigma_T g)_{\max}$ is below the true maximum, pairs with large $g$ collide too rarely, and line L7 only fixes this after the fact. Start with a safe bound and let line L7 raise it.
- **Repeated collisions.** With few particles per cell the same pair can collide twice in one step, which carries no information. Some codes forbid it.
- **Noise in slow flows.** For a flow speed much smaller than the thermal speed, the signal to noise ratio is very low, and DSMC needs a huge number of samples; low-noise variants exist for this case.

## Implementations

## History

Graeme Bird simulated the relaxation of a hard-sphere gas to equilibrium by random pair collisions in 1963 and developed the method for rarefied flows in the following years, with his first book on molecular gas dynamics in 1976. Nanbu derived a related scheme directly from the Boltzmann equation in 1980. Bird introduced the no-time-counter scheme in 1989, and his 1994 book became the standard reference. Wagner gave a convergence proof in 1992, and Alexander, Garcia and Alder analysed the cell size error in 1998. DSMC is now the standard tool for rarefied gas dynamics.

## References
