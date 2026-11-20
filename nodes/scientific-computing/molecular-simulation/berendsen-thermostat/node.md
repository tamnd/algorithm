---
tag: VZN3KE
kind: algorithm
slug: berendsen-thermostat
name: Berendsen thermostat
aliases:
- weak coupling thermostat
area: scientific-computing/molecular-simulation
level: core
summary: Rescales velocities each step so the temperature relaxes exponentially toward the target; it is stable but does not sample the canonical ensemble.
model: real-ram
complexity:
  vars: {N: the number of particles, S: the number of time steps}
  time: {worst: O(S N^2)}
  space: {extra: O(N)}
properties: {deterministic: true, iterative: true, symplectic: false, symmetric: false}
history:
  year: 1984
  people: [Herman J. C. Berendsen, J. P. M. Postma, Wilfred F. van Gunsteren, A. DiNola, J. R. Haak]
  note: Berendsen and coworkers coupled the system to a bath by a first-order relaxation of the temperature and of the pressure, with a time constant for each.
prereqs: [canonical-ensemble, molecular-dynamics]
see_also: [stochastic-velocity-rescaling, nose-hoover-thermostat, andersen-thermostat, langevin-dynamics, microcanonical-ensemble, parrinello-rahman-barostat]
sources:
  - paper: doi:10.1063/1.448118
    title: H. J. C. Berendsen, J. P. M. Postma, W. F. van Gunsteren, A. DiNola and J. R. Haak, Molecular dynamics with coupling to an external bath, Journal of Chemical Physics 81(8), 1984, 3684-3690
    locator: the coupling to a heat bath (the first-order equation for the temperature and the scaling factor lambda)
  - paper: doi:10.1002/(SICI)1096-987X(199805)19:7<726::AID-JCC4>3.0.CO;2-S
    title: Stephen C. Harvey, Robert K.-Z. Tan and Thomas E. Cheatham III, The flying ice cube, Velocity rescaling in molecular dynamics leads to violation of energy equipartition, Journal of Computational Chemistry 19(7), 1998, 726-740
    locator: the transfer of kinetic energy into the centre of mass motion under velocity rescaling
  - paper: doi:10.1063/1.2408420
    title: Giovanni Bussi, Davide Donadio and Michele Parrinello, Canonical sampling through velocity rescaling, Journal of Chemical Physics 126(1), 2007, 014101
    locator: the comparison with the Berendsen thermostat, which their method contains as the limit without noise
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Chapter 3, molecular dynamics (the constant-temperature methods)
---

The Berendsen thermostat, also called weak coupling, controls the temperature of a [molecular dynamics](/molecular-dynamics/) run by scaling all velocities by a factor $\lambda$ after each step. The factor is chosen so that the kinetic temperature relaxes toward the target as $dT/dt = (T_0 - T)/\tau$, with a coupling time $\tau$ that the user sets. The method is simple, deterministic and very stable, so it brings a system to the target temperature quickly and smoothly. It does not sample the [canonical ensemble](/canonical-ensemble/): the fluctuations of the kinetic energy are too small, and for free particles they vanish. Use it to equilibrate, and use a canonical method such as [stochastic velocity rescaling](/stochastic-velocity-rescaling/) for production runs.

## In plain words

After each step the program measures how hot the system is. If it is too hot, it slows all atoms down by the same small fraction. If it is too cold, it speeds them all up. The size of the correction depends on how far the temperature is from the target and on a time constant: a short time constant corrects hard and a long one corrects gently.

This is like a room thermostat that reacts smoothly instead of switching on and off. It works well to reach a temperature. But in a real system at a fixed temperature, the energy of the atoms goes up and down by a known amount. This method removes most of that natural variation, so averages that depend on it come out wrong.

## The problem

The input is the positions $x_i \in \mathbb{R}^d$, velocities $v_i$ and masses $m_i$ of $N$ particles, a force field with forces $f_i = -\nabla_i U$, a time step $h$, a number of steps $S$, the target temperature $k_B T_0$, the coupling time $\tau \ge h$ and the number of degrees of freedom $N_f$ used for the kinetic temperature. The target kinetic energy is $K_0 = \frac12 N_f k_B T_0$, and the kinetic temperature of a state is $k_B T = 2K/N_f$. The output is the trajectory and the kinetic energy after each step. The goal is a temperature that follows
$$\frac{dT}{dt} = \frac{T_0 - T}{\tau}.$$
No ensemble is the goal. This is the reason the method has no sampling guarantee.

## The algorithm

```pseudo id=main
BERENDSEN-THERMOSTAT(x, v, m, FORCES, h, S, kT0, tau, N_f)
L1  (U, f) ← FORCES(x);  K0 ← N_f kT0 / 2
L2  for step ← 1 to S do
L3      v_i ← v_i + (h / 2) f_i / m_i for each particle i     ▷ half kick
L4      x_i ← x_i + h v_i for each particle i                ▷ drift
L5      (U, f) ← FORCES(x)
L6      v_i ← v_i + (h / 2) f_i / m_i for each particle i     ▷ half kick
L7      K ← sum_i m_i |v_i|^2 / 2
L8      lambda ← sqrt(1 + (h / tau)(K0 / K - 1))
L9      v_i ← lambda v_i for each particle i
L10     record lambda^2 K
L11 return (x, v, the recorded kinetic energies)
```

The scaling of line L9 changes the kinetic energy to $\lambda^2 K = K + \frac{h}{\tau}(K_0 - K)$, one explicit Euler step of the relaxation equation. With $\tau = h$ it sets $K = K_0$ exactly in each step, the plain velocity rescaling. As $\tau \to \infty$ the step becomes velocity Verlet. The implementation skips the scaling when $K = 0$ and raises an error for $\tau < h$, where $\lambda^2$ can be negative.

## Example

**Free particles by hand.** Four free particles on a line with $m = 1$ and $v = 2$, so $K = 8$. Let $k_B T_0 = 1$ and $N_f = 4$, so $K_0 = 2$, and $h = 0.1$, $\tau = 1$. In step 1, the Verlet part changes nothing, line L8 gives $\lambda^2 = 1 + 0.1 \cdot (2/8 - 1) = 0.925$, and $K$ becomes $8 \cdot 0.925 = 7.4$. Each step multiplies $K - K_0$ by $1 - h/\tau = 0.9$:

| step | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $K$ | 7.4 | 6.86 | 6.374 | 5.9366 | 5.54294 |

After $n$ steps, $K - 2 = 6 \cdot 0.9^n$, and $K$ tends to 2 with no fluctuation at all. In the canonical ensemble, $K$ for $N_f = 4$ has mean 2 and variance 2.

**Twenty oscillators.** Take 20 independent oscillators on a line with $m = k = k_B T_0 = 1$, started at $x_i = 1 + 0.05i$ for $i = 0, \ldots, 19$ with $v = 0$, so $N_f = 20$. The canonical law of $K$ has mean 10 and variance 10. Run 3000 steps with $h = 0.05$ and drop the first 1000:

| $\tau$ | mean of $K$ | variance of $K$ |
|---|---|---|
| 0.1 | 10.0025 | 0.00477 |
| 0.5 | 10.0000 | $6.1 \times 10^{-13}$ |
| 2 | 9.99976 | $1.0 \times 10^{-4}$ |

These are measurements. The mean is right, and the variance is wrong by a factor of more than 2000 for all three coupling times. On this harmonic system the scaling drives the oscillators into a state where $K$ hardly changes; in a system with interactions the effect is weaker but of the same kind.

## Correctness

The method is not a sampler, so there is no claim of correctness for an ensemble. The proof in [proofs/correctness.md](proofs/correctness.md) shows what the method does:

1. **The factor is real** for $K > 0$ and $\tau \ge h$.
2. **One scaling** gives $K' = K + \frac{h}{\tau}(K_0 - K)$, the explicit Euler step of $dK/dt = (K_0 - K)/\tau$.
3. **Free particles** relax as $K_n - K_0 = (K_{\text{init}} - K_0)(1 - h/\tau)^n$, exactly.
4. **Not canonical.** For free particles the law of $K_n$ tends to a point mass at $K_0$, while the canonical law of $K$ is a gamma law with variance $\frac12 N_f (k_B T_0)^2$.
5. **Weak coupling limit.** As $\tau \to \infty$ the step tends to velocity Verlet.

The scaling also changes the volume of phase space at each step, so there is no Liouville argument for any invariant density. The dynamics are not physical either: the scaling acts on all particles at once, so the temperature of one part of the system depends on the rest at once.

## Complexity

Each step does one force evaluation and $O(N)$ other work. With the all-pairs forces of the molecular dynamics page, $S$ steps cost $O(S N^2)$ time and the thermostat adds $O(S N)$. The extra space is $O(N)$.

## Properties

- **Ensemble.** None that is known in closed form. It is not canonical, and it is not microcanonical, since the energy changes. The mean of $K$ tends to $K_0$.
- **Deterministic.** The same input gives the same run.
- **Not time-reversible and not symplectic.** The factor depends on $K$, and the step does not keep phase-space volume.
- **Momentum.** A uniform scaling keeps $\sum_i m_i v_i = 0$ if it is 0 at the start. If it is not 0, the scaling acts on the centre of mass motion too.

## Variants and improvements

- **Stochastic velocity rescaling.** Bussi, Donadio and Parrinello (2007) add a noise term with the right size to the same relaxation equation, so that $K$ has the canonical law. [Stochastic velocity rescaling](/stochastic-velocity-rescaling/) keeps the smooth control and samples the canonical ensemble. With the noise set to zero it is the Berendsen method.
- **Plain rescaling.** $\tau = h$ sets $K = K_0$ in every step. This is the strongest form and has the smallest fluctuations.
- **Berendsen barostat.** The same paper scales the coordinates and the box by a factor that relaxes the pressure to a target. It has the same problem: the volume fluctuations are wrong. The [Parrinello-Rahman barostat](/parrinello-rahman-barostat/) gives a box with its own dynamics instead.
- **Group coupling.** Scale each group of atoms, for example the solute and the solvent, with its own factor, to reduce the transfer of energy between groups.

## When to use it

Use the Berendsen thermostat to equilibrate: to bring a system from a bad start, for example after energy minimization or after heating, to the target temperature without large swings. Then switch to a method that samples the canonical ensemble, such as [stochastic velocity rescaling](/stochastic-velocity-rescaling/), the [Nose-Hoover thermostat](/nose-hoover-thermostat/) or [Langevin dynamics](/langevin-dynamics/). The use of the Berendsen thermostat for production runs is a habit from the time before these methods were common. It is not a method with a guarantee.

## Pitfalls

- **Wrong fluctuations.** Any average that depends on the fluctuations is wrong: the heat capacity from energy fluctuations, the width of distributions, free energies from fluctuation formulas.
- **The flying ice cube.** Harvey, Tan and Cheatham (1998) showed that repeated velocity rescaling can move kinetic energy from the internal motions into the motion of the centre of mass and into slow modes. A molecule then moves as a cold, rigid body. Remove the centre of mass motion and couple groups separately, or use a canonical method.
- **A wrong $N_f$.** The target $K_0$ uses $N_f$. If constraints or a fixed centre of mass are not counted, the temperature is wrong by the ratio of the two counts.
- **Short coupling times.** With $\tau$ close to $h$, the method is nearly plain rescaling, and the dynamics are disturbed strongly. Values of $\tau$ around 0.1 to 1 ps are common in biomolecular codes; these are choices.

## Implementations

## History

Berendsen, Postma, van Gunsteren, DiNola and Haak (1984) proposed to couple a molecular dynamics system to an external bath by a first-order relaxation of the temperature with a time constant $\tau$, and of the pressure with a time constant $\tau_P$. The method became the default way to control temperature in biomolecular codes for many years. Its failure to give canonical fluctuations was known, and Harvey, Tan and Cheatham (1998) described the flying ice cube artefact. Bussi, Donadio and Parrinello (2007) added the missing noise and obtained a canonical method with the same structure.

## References
