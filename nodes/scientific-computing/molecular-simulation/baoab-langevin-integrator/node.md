---
tag: V8MPCG
kind: algorithm
slug: baoab-langevin-integrator
name: BAOAB Langevin integrator
aliases:
- BAOAB splitting
area: scientific-computing/molecular-simulation
level: research
summary: Splits Langevin dynamics into kick, drift and exact Ornstein-Uhlenbeck steps in the order B A O A B, which gives very accurate configurational sampling.
model: real-ram
complexity:
  vars: {N: the number of particles, S: the number of time steps}
  time: {worst: O(S N^2)}
  space: {extra: O(N)}
properties: {deterministic: false, randomized: true, iterative: true, symplectic: false, symmetric: true}
history:
  year: 2013
  people: [Benedict Leimkuhler, Charles Matthews]
  note: Leimkuhler and Matthews compared the orders in which the kick, drift and Ornstein-Uhlenbeck parts of Langevin dynamics can be composed and found that B A O A B has the smallest error in configurational averages.
prereqs: [langevin-dynamics, operator-splitting]
see_also: [brownian-dynamics, verlet-integration, symplectic-integrators, canonical-ensemble, shadow-hamiltonian, metropolis-adjusted-langevin-algorithm, hamiltonian-monte-carlo, stochastic-velocity-rescaling]
sources:
  - paper: doi:10.1093/amrx/abs010
    title: Benedict Leimkuhler and Charles Matthews, Rational construction of stochastic numerical methods for molecular sampling, Applied Mathematics Research eXpress 2013(1), 2013, 34-56
    locator: the splittings of Langevin dynamics into A, B and O parts, the error of their invariant measures, and the high friction limit of BAOAB
  - paper: doi:10.1093/imanum/dru056
    title: Benedict Leimkuhler, Charles Matthews and Gabriel Stoltz, The computation of averages from equilibrium and nonequilibrium Langevin molecular dynamics, IMA Journal of Numerical Analysis 36(1), 2016, 13-79
    locator: the error expansions of averages for splitting methods of Langevin dynamics
  - book: isbn:9783319163741
    title: Ben Leimkuhler and Charles Matthews, Molecular Dynamics, With Deterministic and Stochastic Numerical Methods, Springer, 2015
    locator: Chapter 7, numerical methods for stochastic molecular dynamics
---

BAOAB is an integrator for [Langevin dynamics](/langevin-dynamics/), the equations of motion with friction and random forces that sample the [canonical ensemble](/canonical-ensemble/). It splits the equations into three parts that can each be solved exactly: a kick B by the forces, a drift A of the positions, and an Ornstein-Uhlenbeck step O of the velocities, which holds the friction and the noise. It composes them in the order B A O A B, with the O step in the middle of the drift. Leimkuhler and Matthews (2013) showed that this order gives a much smaller error in averages of the positions than other orders at the same cost. On a harmonic oscillator the positions have the exact canonical law for every stable time step (a theorem).

## In plain words

Langevin dynamics mixes three simple motions: atoms push each other, atoms move on, and the solvent slows them and knocks them at random. A program does the three motions one after another in small time steps, and the order matters.

BAOAB does half a push, half a move, then the slowing and knocking, then the other half of the move and the other half of the push. Doing the random part in the middle of the move turns out to make the positions of the atoms much more accurate. The speeds are less accurate in exchange, but for most questions, such as the shape of a molecule or the free energy of a state, the positions are what matter. It costs the same as other orders: one force computation per step.

## The problem

The input is as for Langevin dynamics: positions $x_i \in \mathbb{R}^d$, velocities $v_i$ and masses $m_i$ of $N$ particles, a force routine for $f_i = -\nabla_i U$, a time step $h$, a number of steps $S$, the target $k_B T$, the friction $\gamma \ge 0$ and a random number source. The equations are
$$dx_i = v_i\, dt, \qquad m_i\, dv_i = f_i\, dt - m_i \gamma v_i\, dt + \sqrt{2 m_i \gamma k_B T}\, dW_i.$$
The parts are B: $dv = (f/m)\,dt$, A: $dx = v\,dt$, and O: $dv = -\gamma v\,dt + \sqrt{2\gamma k_B T / m}\,dW$. The output is the trajectory and samples of $(x, v)$, to be used for averages of functions of $x$. The kinetic temperature uses $N_f = dN$, since the noise does not conserve momentum.

## The algorithm

```pseudo id=main
BAOAB(x, v, m, FORCES, h, S, kT, gamma)
L1  f ← FORCES(x); c ← exp(-gamma h)
L2  for step ← 1 to S do
L3      v_i ← v_i + (h / 2) f_i / m_i for each particle i                ▷ B
L4      x_i ← x_i + (h / 2) v_i for each particle i                     ▷ A
L5      v_i ← c v_i + sqrt((1 - c²) kT / m_i) R_i for each particle i    ▷ O, R_i standard normal in R^d
L6      x_i ← x_i + (h / 2) v_i for each particle i                     ▷ A
L7      f ← FORCES(x)
L8      v_i ← v_i + (h / 2) f_i / m_i for each particle i                ▷ B
L9      every k steps, record a copy of (x, v)
L10 return (x, v, the recorded samples)
```

The forces from line L7 serve the kick on line L3 of the next step, so there is one force evaluation per step. Line L5 is the exact solution of the Ornstein-Uhlenbeck part over the full time $h$. With $\gamma = 0$, line L5 does nothing, the two drifts join, and the step is velocity Verlet. The [OBABO splitting](/langevin-dynamics/) uses the same parts with the O step split in two at the ends.

## Example

**One step by hand.** One particle on a spring with $m = k = k_B T = 1$ in reduced units, $x = 1$, $v = 0$, $h = 0.1$, $\gamma = 1$, so $c = e^{-0.1} = 0.904837$ and $\sqrt{1 - c^2} = 0.425757$. With the normal draw $R = 0.5$ on line L5:

| after | L3 | L4 | L5 | L6 | L8 |
|---|---|---|---|---|---|
| $x$ | 1 | 0.9975 | 0.9975 | 1.005882 | 1.005882 |
| $v$ | $-0.05$ | $-0.05$ | 0.167637 | 0.167637 | 0.117343 |

**Exact positions on a harmonic oscillator.** For $U = \frac12 k x^2$, $\omega^2 = k/m$ and $h\omega < 2$, the stationary law of BAOAB has $\langle x^2 \rangle = k_B T / k$ exactly and $\langle v^2 \rangle = (k_B T/m)(1 - h^2\omega^2/4)$, for any $\gamma > 0$ (a theorem, Claim 4 of the proof). A run of 50 oscillators with $m = k = k_B T = \gamma = 1$, 4000 steps from rest, a sample every 5 steps and the first 200 steps dropped (seed 1) gives:

| $h$ | measured $\langle x^2 \rangle$ | exact | measured $\langle v^2 \rangle$ | exact | OBABO exact $\langle x^2 \rangle$ |
|---|---|---|---|---|---|
| 0.5 | 0.9916 | 1 | 0.9335 | 0.9375 | 1.0667 |
| 1 | 0.9918 | 1 | 0.7510 | 0.75 | 1.3333 |
| 1.5 | 1.0039 | 1 | 0.4366 | 0.4375 | 2.2857 |

OBABO has the opposite behavior: exact velocities and wrong positions.

**A quartic well.** For $U = x^4/4$ in one dimension with $k_B T = 1$, the canonical value is $\langle x^2 \rangle = 2\Gamma(3/4)/\Gamma(1/4) = 0.67598$. 50 particles with $m = \gamma = 1$, 8000 steps from rest, a sample every 5 steps and the first 500 steps dropped, averaged over seeds 1 to 5, with the standard error over the seeds:

| $h$ | BAOAB $\langle x^2 \rangle$ | OBABO $\langle x^2 \rangle$ |
|---|---|---|
| 0.1 | $0.6745 \pm 0.0008$ | $0.6759 \pm 0.0016$ |
| 0.2 | $0.6744 \pm 0.0008$ | $0.6791 \pm 0.0014$ |
| 0.3 | $0.6724 \pm 0.0005$ | $0.6850 \pm 0.0016$ |
| 0.4 | $0.6721 \pm 0.0010$ | $0.6944 \pm 0.0012$ |

These are measurements. The error of OBABO grows like $h^2$, to 0.018 at $h = 0.4$. The error of BAOAB stays below 0.004 over this range. For this well, both are unstable near $h = 0.6$, since the force grows like $x^3$.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **The parts are exact.** Lines L3 and L8 are the flow of B, lines L4 and L6 the flow of A, and line L5 an exact draw from the flow of O.
2. **What each part keeps.** O keeps the canonical density exactly. A and B keep the volume of phase space but not the density.
3. **The regrouped chain.** Cut the step at line L5: the state there follows $A_{h/2} B_h A_{h/2} O_h$, which is position Verlet followed by O.
4. **The harmonic oscillator.** The chain has a unique stationary law, it converges to it from any start, and the positions have the exact canonical variance.
5. **Limits.** With $\gamma = 0$ the step is velocity Verlet.

For general smooth potentials, the error of BAOAB in averages of the positions is $O(h^2)$, and in the limit of high friction the leading term vanishes and the error is of order $h^4$, as shown by Leimkuhler and Matthews (2013). That result is a theorem of the paper, under its assumptions; it is not proved on this page. So the method samples the canonical ensemble up to the time step error, and the error is smaller than for other splittings of the same cost.

## Complexity

Each step does one force evaluation, $dN$ normal draws and $O(N)$ other work. With the all-pairs forces of the molecular dynamics page, $S$ steps take $O(S N^2)$ time. The extra space is $O(N)$ for the copies of $x$ and $v$, plus the samples.

## Properties

- **Ensemble.** Canonical (NVT) for the positions, up to a small time step error, for any $\gamma > 0$.
- **Accurate positions, less accurate velocities.** On a harmonic oscillator the position law is exact and the velocity law at the end of a step is too narrow by the factor $1 - h^2\omega^2/4$.
- **Robust at high friction.** As $\gamma h \to \infty$ the method becomes a stable and accurate integrator of [Brownian dynamics](/brownian-dynamics/), where other splittings degrade.
- **Dynamics.** For small $\gamma$ the motion is close to Newtonian, as for any Langevin integrator, and diffusion is slowed as $\gamma$ grows.
- **Cost.** The same as velocity Verlet plus $dN$ normal draws.

## Variants and improvements

- **Other orders.** The five-letter words in A, B and O give a family of methods. ABOBA, OBABO and BAOAB are the symmetric ones studied by Leimkuhler and Matthews. OBABO, the splitting of Bussi and Parrinello, has exact velocities on the harmonic oscillator, and BAOAB has exact positions.
- **The high friction limit.** For $\gamma \to \infty$ with the time rescaled, BAOAB becomes the update $x' = x + \frac{h}{\gamma m} f(x) + \sqrt{\frac{h k_B T}{2\gamma m}}(R_n + R_{n+1})$, which averages two successive normal draws. It is a more accurate alternative to the Euler-Maruyama step of Brownian dynamics.
- **Constraints.** With bond constraints, the A step is followed by a projection, as in [RATTLE](/rattle-algorithm/) and its geodesic variants.
- **Exact sampling.** A Metropolis test on top of a Langevin step removes the bias, as in the [Metropolis-adjusted Langevin algorithm](/metropolis-adjusted-langevin-algorithm/) and generalized [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/).

## When to use it

Use BAOAB when the goal is configurational averages from Langevin dynamics: free energies, structures, distributions of collective variables. It allows larger time steps for the same accuracy, so it saves force evaluations. It is a good choice at high friction too. When velocity statistics or dynamical properties at large steps matter, use a different splitting or a smaller step.

## Pitfalls

- **The kinetic temperature from the end-of-step velocities.** At large $h$ it is too low, as the example shows, even though the positions are right. Do not use it to judge the thermostat. On the harmonic oscillator the velocity just before line L5 has the right variance, so it is a better choice there.
- **Unstable steps.** The method needs $h\omega < 2$ for the fastest motion $\omega$, as velocity Verlet does. Stiff bonds limit the step.
- **The force at line L7.** It serves line L3 of the next step. If something else moves the positions between steps, such as a barostat, compute the force again.
- **Comparing integrators by the temperature.** Compare them by configurational averages, such as the potential energy or a radial distribution function.

## Implementations

## History

Splittings of Langevin dynamics with an exact Ornstein-Uhlenbeck part were used by Bussi and Parrinello (2007), in the order OBABO. Leimkuhler and Matthews (2013) studied the error of the invariant measure for all symmetric orders of the A, B and O parts and found the order B A O A B best for configurational averages, with a fourth order error in the high friction limit. Leimkuhler, Matthews and Stoltz (2016) gave error expansions for equilibrium and nonequilibrium averages. Integrators based on BAOAB are available in several molecular dynamics codes.

## References
