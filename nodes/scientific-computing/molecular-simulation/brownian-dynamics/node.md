---
tag: 1T83PZ
kind: algorithm
slug: brownian-dynamics
name: Brownian dynamics
aliases:
- Ermak-McCammon algorithm
area: scientific-computing/molecular-simulation
level: core
summary: Integrates the overdamped Langevin equation, moving positions by force times mobility plus noise, for solutes in an implicit solvent.
model: real-ram
complexity:
  vars: {N: the number of particles, S: the number of time steps}
  time: {worst: O(S N^3)}
  space: {extra: O(N^2)}
properties: {deterministic: false, randomized: true, iterative: true, symplectic: false, symmetric: false}
history:
  year: 1978
  people: [Donald L. Ermak, J. Andrew McCammon]
  note: Ermak and McCammon gave the step for the positions of particles in a solvent with a configuration-dependent diffusion tensor, which includes hydrodynamic interactions, and used it for polymers and proteins.
prereqs: [langevin-dynamics, euler-maruyama-method]
see_also: [cholesky-decomposition, baoab-langevin-integrator, stochastic-differential-equation, canonical-ensemble, metropolis-adjusted-langevin-algorithm, kinetic-monte-carlo, dissipative-particle-dynamics, chemical-langevin-equation]
sources:
  - paper: doi:10.1063/1.436761
    title: Donald L. Ermak and J. Andrew McCammon, Brownian dynamics with hydrodynamic interactions, Journal of Chemical Physics 69(4), 1978, 1352-1360
    locator: the step for the positions with a diffusion tensor, the divergence term and the use of the Oseen and Rotne-Prager tensors
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: the chapter on mesoscale methods, Langevin and Brownian dynamics
  - book: isbn:9783319163741
    title: Ben Leimkuhler and Charles Matthews, Molecular Dynamics, With Deterministic and Stochastic Numerical Methods, Springer, 2015
    locator: Chapters 6 and 7, the overdamped limit of Langevin dynamics and its numerical methods
---

Brownian dynamics simulates particles in a solvent on time scales much longer than the time it takes the solvent to stop their motion. On these scales the velocities are not variables any more: each step moves the positions by the force times a mobility plus a random displacement. The equation it integrates is the overdamped limit of [Langevin dynamics](/langevin-dynamics/), and its stationary distribution is the Boltzmann distribution of the positions (a theorem). The step of Ermak and McCammon (1978) uses a diffusion tensor, which can couple the particles through the solvent flow they cause (hydrodynamic interactions). With one diffusion constant per particle it is the [Euler-Maruyama](/euler-maruyama-method/) step of the overdamped Langevin equation.

## In plain words

A protein or a colloid in water is pushed around by water molecules many billions of times each second. When we only care about slow motions, such as two proteins finding each other, we can forget the speed of each particle. A particle in water stops almost at once when no force acts on it.

So each step does two things. It moves each particle a little in the direction of the force on it, more for small particles that move easily in water. Then it adds a random jump, which is the effect of the water knocks. The size of the jumps is tied to the temperature. With these two parts the particles end up in the right places with the right frequencies. A more detailed version also lets a moving particle drag its neighbors through the water.

## The problem

The input is positions $x_i \in \mathbb{R}^d$ of $N$ particles, a force routine for $f_i = -\nabla_i U$, a time step $h$, a number of steps $S$, the temperature $k_B T$, a diffusion tensor $D(x)$ and a random number source. $D$ is a symmetric positive definite matrix of size $dN \times dN$; for particles that do not interact through the solvent it is diagonal, with $D_i = k_B T / \zeta_i$ for a friction coefficient $\zeta_i$, for example the Stokes-Einstein value $D_i = k_B T / (6\pi\eta a_i)$ for a sphere of radius $a_i$ in a fluid of viscosity $\eta$. The equation is
$$dx = \frac{1}{k_B T} D(x) f(x)\, dt + \nabla \cdot D(x)\, dt + \sqrt{2}\, L(x)\, dW, \qquad L L^{\mathsf T} = D.$$
Its stationary density is $\rho(x) \propto e^{-U(x)/k_B T}$. The output is the trajectory of positions and samples of it. Brownian dynamics has no velocities, so it reports no kinetic temperature and needs no count $N_f$ of degrees of freedom: the temperature enters only through $k_B T$ in the drift and the noise.

## The algorithm

```pseudo id=main
BROWNIAN-DYNAMICS(x, FORCES, h, S, kT, DIFFUSION)
L1  f ← FORCES(x)
L2  for step ← 1 to S do
L3      D ← DIFFUSION(x)                     ▷ dN by dN; skip L3 and L4 for one constant per particle
L4      L ← CHOLESKY(D)                      ▷ L L^T = D
L5      R ← dN independent standard normal numbers
L6      x ← x + (h / kT) D f + sqrt(2 h) L R
L7      f ← FORCES(x)
L8      every k steps, record a copy of x
L9  return (x, the recorded samples)
```

With one diffusion constant $D_i$ per particle, line L6 reads $x_i \leftarrow x_i + (h D_i / k_B T) f_i + \sqrt{2 D_i h}\, R_i$. Line L6 leaves out the term $h \nabla \cdot D$. It is zero for a constant $D$ and for the Rotne-Prager-Yamakawa tensor, which the implementation provides; for other tensors it must be added. The [Cholesky decomposition](/cholesky-decomposition/) on line L4 gives noise with covariance $2hD$.

## Example

**One step by hand.** One particle in one dimension in the well $U = \frac12 k x^2$ with $k = D = k_B T = 1$ in reduced units, $x = 1$, $h = 0.1$ and the normal draw $R = 0.3$. The force is $-1$, so line L6 gives $x = 1 - 0.1 + \sqrt{0.2} \cdot 0.3 = 1.034164$.

**The time step error in a harmonic well.** For $U = \frac12 k x^2$ and a constant $D$, let $c = hDk/k_B T$. The stationary variance of the step is $(k_B T/k)/(1 - c/2)$ for $0 < c < 2$ (a theorem, Claim 5 of the proof), and the step is unstable for $c \ge 2$. A run of 400 particles with $k = D = k_B T = 1$, 1000 steps from 0, a sample every 2 steps and the first 100 steps dropped (seed 1):

| $h$ | 0.1 | 0.5 | 1 | 1.5 |
|---|---|---|---|---|
| measured $\langle x^2 \rangle$ | 1.0474 | 1.3354 | 2.0042 | 4.0145 |
| exact for the step | 1.0526 | 1.3333 | 2 | 4 |

The right value is 1. The error is of order $h$, as for any Euler-Maruyama step.

**Free diffusion.** With no forces, the step is exact for any $h$: after a time $t$, the mean squared displacement in $d$ dimensions is $2dDt$. 400 free particles in two dimensions with $D = 0.7$, $h = 0.1$ and 50 steps (seed 3) give 14.11 against 14.

**Hydrodynamic coupling.** For two spheres of radius $a$ at distance $r$ along the first axis, the Rotne-Prager-Yamakawa tensor gives the following coupling blocks, as fractions of the Stokes-Einstein value $D_0$:

| $r / a$ | 1 | 2 | 4 | 10 |
|---|---|---|---|---|
| along the line of centers | 0.8125 | 0.625 | 0.3594 | 0.149 |
| across it | 0.7188 | 0.4375 | 0.1953 | 0.0755 |
| Oseen, along, $3a/(2r)$ | 1.5 | 0.75 | 0.375 | 0.15 |

At contact, $r = 2a$, both forms of the tensor give $\frac{7}{16}$ and $\frac{3}{16}$ for the parts across and along, so it is continuous. Far apart it approaches the Oseen tensor, which decays like $1/r$. The Oseen tensor can fail to be positive definite when spheres are close, which is why the corrected tensor is used.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **The Boltzmann density is stationary**, with zero probability flux, for the Fokker-Planck equation of the overdamped equation.
2. **The step** is the Euler-Maruyama step of that equation when $\nabla \cdot D = 0$.
3. **The Rotne-Prager-Yamakawa tensor has zero divergence** in both of its regions, so no divergence term is needed with it.
4. **Free particles and a constant force** give the exact mean and covariance of the displacement for every $h$.
5. **In a harmonic well** the stationary variance of the step is $(k_B T/k)/(1 - c/2)$.

So the sampled distribution is the Boltzmann distribution of the positions up to an $O(h)$ error, the weak order of the Euler-Maruyama method.

## Complexity

With one diffusion constant per particle, each step does one force evaluation and $dN$ normal draws, so $S$ steps take $O(S N^2)$ time with all-pairs forces and $O(N)$ extra space. With a full diffusion tensor, building it takes $O(N^2)$ time and space per step, and its Cholesky factor $O(N^3)$ time, so $S$ steps take $O(S N^3)$ time and $O(N^2)$ extra space. Fixman's Chebyshev method and Ewald-like methods for the tensor reduce this for large $N$.

## Properties

- **Ensemble.** The Boltzmann (canonical) distribution of the positions, up to $O(h)$, for any positive definite $D$ when the divergence term is right.
- **No velocities.** The method has no kinetic energy and no inertia. The dynamics are physical only on time scales much longer than the velocity relaxation time $m/\zeta$.
- **Diffusion is correct** in the free case for any step, which is the main use: diffusion constants and rates of encounter.
- **Hydrodynamics are optional.** A diagonal $D$ gives the free-draining model, and a full tensor couples the particles through the solvent.
- **Not time-reversible.** The process satisfies detailed balance with respect to the Boltzmann density, but the step does not.

## Variants and improvements

- **The limit of BAOAB.** The high friction limit of [BAOAB](/baoab-langevin-integrator/) gives the update $x' = x + (hD/k_B T) f + \sqrt{Dh/2}\,(R_n + R_{n+1})$, which uses two successive draws and is more accurate for configurational averages.
- **A Metropolis test.** Accepting or rejecting each step with the Metropolis rule removes the time step bias; with $D$ constant this is the [Metropolis-adjusted Langevin algorithm](/metropolis-adjusted-langevin-algorithm/).
- **Faster noise.** Fixman (1986) approximated $L R$ with Chebyshev polynomials of $D$, which avoids the Cholesky factor.
- **Event-based methods.** For rare transitions between states, [kinetic Monte Carlo](/kinetic-monte-carlo/) jumps from state to state with known rates.
- **Concentrations.** For chemical species in well-mixed systems, the [chemical Langevin equation](/chemical-langevin-equation/) uses the same kind of equation for concentrations.

## When to use it

Use Brownian dynamics for solutes in an implicit solvent when the time scale of interest is much longer than the velocity relaxation time: colloids, polymers in solution, protein association, coarse-grained models. It allows much larger time steps than molecular dynamics with explicit water. Do not use it when inertia matters, for example for vibrations, for fast molecular motion or for gases.

## Pitfalls

- **A missing divergence term.** For a diffusion tensor that depends on the positions and has nonzero divergence, leaving out $h \nabla \cdot D$ gives the wrong distribution.
- **The Oseen tensor.** It is not positive definite when particles are close, and the Cholesky factor fails. Use the Rotne-Prager-Yamakawa form.
- **Too large a step.** In a stiff well the step is unstable for $hDk/k_B T \ge 2$, and the error is of order $h$ below that. Steep repulsive walls need a small step or a rejection rule.
- **Units.** $D$ has units of length squared per time, and the drift is $D f / k_B T$, not $D f$.
- **Interpreting the time.** With a wrong $D$, all times scale; check a known diffusion constant.

## Implementations

## History

Einstein (1905) and Smoluchowski (1906) explained Brownian motion as diffusion and related the diffusion constant to friction and temperature. Ermak and McCammon (1978) gave the simulation step with a configuration-dependent diffusion tensor, including the divergence term, and used the Oseen and Rotne-Prager tensors for hydrodynamic interactions. The Rotne-Prager tensor (1969) and Yamakawa's form (1970) give a positive definite tensor for spheres. Later work by Fixman and others reduced the cost of the correlated noise for many particles.

## References
