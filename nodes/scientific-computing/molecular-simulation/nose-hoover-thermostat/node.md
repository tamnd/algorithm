---
tag: GC1X6T
kind: algorithm
slug: nose-hoover-thermostat
name: Nose-Hoover thermostat
aliases:
- Nose-Hoover dynamics
area: scientific-computing/molecular-simulation
level: core
summary: Adds a friction variable with its own equation of motion so that the extended dynamics, if ergodic, samples the canonical ensemble.
model: real-ram
complexity:
  vars: {N: the number of particles, S: the number of time steps}
  time: {worst: O(S N^2)}
  space: {extra: O(N)}
properties: {deterministic: true, iterative: true, symplectic: false, symmetric: true}
history:
  year: 1984
  people: [Shuichi Nose, William G. Hoover]
  note: Nose gave an extended Hamiltonian with a variable that scales time, and Hoover rewrote its equations in real time with a friction coefficient and showed that one harmonic oscillator is not ergodic under them.
prereqs: [canonical-ensemble, molecular-dynamics]
see_also: [nose-hoover-chains, ergodicity, operator-splitting, andersen-thermostat, langevin-dynamics, stochastic-velocity-rescaling, microcanonical-ensemble, parrinello-rahman-barostat]
sources:
  - paper: doi:10.1080/00268978400101201
    title: Shuichi Nose, A molecular dynamics method for simulations in the canonical ensemble, Molecular Physics 52(2), 1984, 255-268
    locator: the extended Hamiltonian with the time scaling variable s and the proof that it gives canonical averages
  - paper: doi:10.1063/1.447334
    title: Shuichi Nose, A unified formulation of the constant temperature molecular dynamics methods, Journal of Chemical Physics 81(1), 1984, 511-519
    locator: the equations in real time and the relation to other constant-temperature methods
  - paper: doi:10.1103/PhysRevA.31.1695
    title: William G. Hoover, Canonical dynamics, Equilibrium phase-space distributions, Physical Review A 31(3), 1985, 1695-1697
    locator: the equations with the friction coefficient, the stationary canonical density and the harmonic oscillator
  - paper: doi:10.1080/00268979600100761
    title: Glenn J. Martyna, Mark E. Tuckerman, Douglas J. Tobias and Michael L. Klein, Explicit reversible integrators for extended systems dynamics, Molecular Physics 87(5), 1996, 1117-1157
    locator: the factorization of the Liouville operator into exact flows, which gives the time-reversible step of this page
  - book: isbn:9780198525264
    title: Mark E. Tuckerman, Statistical Mechanics, Theory and Molecular Simulation, Oxford University Press, 2010
    locator: Chapter 4, the canonical ensemble (non-Hamiltonian extended phase-space methods)
  - book: isbn:9783319163741
    title: Ben Leimkuhler and Charles Matthews, Molecular Dynamics, With Deterministic and Stochastic Numerical Methods, Springer, 2015
    locator: Chapter 8, extended variable methods
---

The Nose-Hoover thermostat runs [molecular dynamics](/molecular-dynamics/) at a fixed temperature with deterministic equations. It adds one variable, a friction coefficient $\xi$, that slows the particles down when the kinetic energy is above its target and speeds them up when it is below. The friction has its own equation of motion with a mass $Q$, so the control is smooth and has a memory. The extended system conserves an energy, and the [canonical ensemble](/canonical-ensemble/) is a stationary density of its flow (a theorem). Time averages are canonical averages only if the motion is ergodic, which is a hypothesis: it fails for one harmonic oscillator and for other small or stiff systems, and [Nose-Hoover chains](/nose-hoover-chains/) are the usual repair.

## In plain words

Think of a brake and an accelerator on every atom, both worked by one pedal. The pedal moves by itself. When the atoms move too fast on average, the pedal moves toward the brake, and when they are too slow, it moves toward the accelerator. The pedal has inertia, so it does not jump. It overshoots a little and swings back, and the temperature of the atoms swings around the target.

There is no randomness. The program can run forward and backward, and there is a total energy, which includes the pedal, that stays fixed. This is useful to check the program. The method gives the right statistics if the motion visits all states, and for some simple systems it does not.

## The problem

The input is the positions $x_i \in \mathbb{R}^d$, velocities $v_i$ and masses $m_i$ of $N$ particles, a force field with forces $f_i = -\nabla_i U$, a time step $h$, a number of steps $S$, the target $k_B T$, the thermostat mass $Q > 0$, the number $N_f$ of velocity components that the thermostat scales, and start values of $\xi$ and of the thermostat position $\eta$ (often 0). The output is the trajectory of the equations of Hoover (1985),
$$\dot x_i = v_i, \qquad \dot v_i = \frac{f_i}{m_i} - \xi v_i, \qquad \dot \xi = \frac{2K - N_f k_B T}{Q}, \qquad \dot \eta = \xi,$$
with $K = \sum_i \frac12 m_i |v_i|^2$, and the extended energy
$$H' = K + U + \tfrac12 Q \xi^2 + N_f k_B T\, \eta$$
after each step, which the exact flow conserves. $\eta$ enters only $H'$. In the implementation $N_f = dN$. If the total momentum is fixed at 0, the momentum is a further conserved quantity, and the thermostat should use $N_f = dN - d$ (see Pitfalls).

## The algorithm

```pseudo id=main
NOSE-HOOVER(x, v, m, FORCES, h, S, kT, Q, N_f, xi, eta)
L1  (U, f) ← FORCES(x)
L2  for step ← 1 to S do
L3      (xi, eta) ← THERMOSTAT-HALF(v, xi, eta)
L4      v_i ← v_i + (h / 2) f_i / m_i for each particle i     ▷ half kick
L5      x_i ← x_i + h v_i for each particle i                ▷ drift
L6      (U, f) ← FORCES(x)
L7      v_i ← v_i + (h / 2) f_i / m_i for each particle i     ▷ half kick
L8      (xi, eta) ← THERMOSTAT-HALF(v, xi, eta)
L9      record H' = K + U + Q xi^2 / 2 + N_f kT eta
L10 return (x, v, xi, eta, the recorded H')

THERMOSTAT-HALF(v, xi, eta)                          ▷ exact flows for a time h / 2
L11 xi ← xi + (h / 4)(2K - N_f kT) / Q
L12 v_i ← exp(-xi h / 2) v_i for each particle i
L13 eta ← eta + (h / 2) xi
L14 xi ← xi + (h / 4)(2K - N_f kT) / Q                ▷ K after the scaling
```

This is the splitting of Martyna, Tuckerman, Tobias and Klein (1996). The thermostat part is split into two exact flows: with $v$ fixed, $\xi$ moves at a constant rate (L11, L14), and with $\xi$ fixed, the velocities decay as $e^{-\xi t}$ and $\eta$ grows as $\xi t$ (L12, L13). The palindrome of exact flows makes the step time-reversible and of order 2.

## Example

**One step by hand.** One particle on a spring with $m = k = k_B T = Q = 1$ in reduced units, $N_f = 1$, $x = 1$, $v = 0$, $\xi = \eta = 0$ and $h = 0.1$, so $H' = 0.5$.

| line | update | value |
|---|---|---|
| L11 | $\xi \leftarrow 0 + 0.025 (0 - 1)$ | $\xi = -0.025$ |
| L12, L13 | $v = 0$ stays 0; $\eta \leftarrow 0.05 \cdot (-0.025)$ | $\eta = -0.00125$ |
| L14 | $\xi \leftarrow -0.025 - 0.025$ | $\xi = -0.05$ |
| L4 to L7 | velocity Verlet | $x = 0.995$, $v = -0.09975$ |
| L11 | $2K = 0.0099500$, $\xi \leftarrow -0.05 + 0.025(0.00995 - 1)$ | $\xi = -0.0747512$ |
| L12 | $v \leftarrow e^{0.0037376} \cdot (-0.09975)$ | $v = -0.1001235$ |
| L13 | $\eta \leftarrow -0.00125 + 0.05 \cdot (-0.0747512)$ | $\eta = -0.0049876$ |
| L14 | $\xi \leftarrow -0.0747512 + 0.025(0.0100247 - 1)$ | $\xi = -0.0995006$ |

The particle is colder than the target, so $\xi$ becomes negative and the scaling speeds it up: $|v|$ is larger than the 0.09975 of plain Verlet. The extended energy after the step is $H' = 0.4999875$.

**The extended energy is conserved to second order.** Two oscillators with $k = 1$, masses 1 and 2, started at $x = (1, 0.3)$, $v = (0, 0.7)$, with $Q = 0.5$, $k_B T = 1$ and $N_f = 2$, run to $t = 20$. The spread $\max H' - \min H'$ is

| $h$ | 0.1 | 0.05 | 0.025 |
|---|---|---|---|
| spread of $H'$ | 0.03168 | 0.008336 | 0.002110 |

so it falls by a factor of about 4 when $h$ is halved. Running 300 steps forward, flipping $v$ and $\xi$, and running 300 steps back recovers the start to $10^{-9}$.

**One oscillator is not ergodic.** One oscillator with $m = k = k_B T = Q = 1$, $N_f = 1$, from $x = 1$, $v = 0$, with $h = 0.05$ and a sample every 10 steps to $t = 10^4$, gives $\langle x^2 \rangle = 0.793$ and $\langle x^4 \rangle / \langle x^2 \rangle^2 = 1.538$. The canonical values are 1 and 3. The mean of $2K$ is 0.99915, close to $N_f k_B T = 1$, as it must be for any bounded run. These are measurements: the trajectory stays near a torus and does not fill the phase space. The right mean temperature does not show that the distribution is right.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **The extended energy** $H'$ is conserved by the exact flow.
2. **The canonical density is stationary.** The density $\exp(-\beta(K + U + \frac12 Q\xi^2))$ on $(x, v, \xi)$ solves the stationary Liouville equation, since the flow has divergence $-N_f \xi$. Its marginal in $(x, v)$ is canonical.
3. **The step is a palindrome of exact flows**, so it is time-reversible and has order 2.
4. **Time reversal.** With $R(x, v, \xi, \eta) = (x, -v, -\xi, \eta)$, $\Psi_h \circ R \circ \Psi_h = R$.
5. **The mean kinetic energy.** The mean of $2K - N_f k_B T$ over the $4n$ updates of $\xi$ in $n$ steps is exactly $Q(\xi_n - \xi_0)/(nh)$, which tends to 0 if $\xi$ stays bounded. This needs no ergodicity.

So the method samples the canonical ensemble if the extended flow is ergodic on the set where $H'$ and the other conserved quantities are fixed. This is a hypothesis, and it fails on the examples above. The dynamics are not physical in a strict sense, since the friction acts on all particles at once. The rule of thumb is that for a large system and a slow thermostat the effect on time correlations is small; this is not a theorem.

## Complexity

Each step does one force evaluation and $O(N)$ other work, including two computations of $K$. With the all-pairs forces of the molecular dynamics page, $S$ steps cost $O(S N^2)$ time, and the thermostat adds $O(S N)$. The extra space is $O(N)$ and two numbers.

## Properties

- **Ensemble.** Canonical (NVT) for the $(x, v)$ marginal, if the extended dynamics is ergodic, up to the time step error. The extended energy $H'$ is conserved.
- **Deterministic and time-reversible.** The step is a palindrome of exact flows.
- **Not symplectic in the usual sense.** The flow does not keep the volume $dx\,dv\,d\xi$; it keeps the measure $e^{N_f \eta}\,dx\,dv\,d\xi\,d\eta$, which is the reason a canonical density can be stationary.
- **A quantity to monitor.** A drift of $H'$ shows an integration error, as $H$ does in NVE.
- **Momentum.** The friction scales all velocities, so a total momentum of 0 stays 0, and a nonzero one decays or grows with $\xi$.

## Variants and improvements

- **Nose-Hoover chains.** [Nose-Hoover chains](/nose-hoover-chains/) thermostat $\xi$ with a second thermostat, and so on. This repairs the lack of ergodicity in many cases.
- **Nose's form.** Nose (1984) used a variable $s$ that scales time and a Hamiltonian in the extended variables. Hoover's equations are the same dynamics in real time. With Nose's virtual time the sampling needs $N_f + 1$ in place of $N_f$ in the logarithm term.
- **Massive thermostats.** One thermostat for each degree of freedom, or for each group of atoms, makes the method much more robust, at the price of a stronger effect on the dynamics.
- **Barostats.** The same idea with a variable for the volume or for the box gives constant pressure methods. The [Parrinello-Rahman barostat](/parrinello-rahman-barostat/) is the version without a thermostat; with a Nose-Hoover thermostat on top it samples a form of NPT.
- **Stochastic thermostats.** [Langevin dynamics](/langevin-dynamics/) and [stochastic velocity rescaling](/stochastic-velocity-rescaling/) add noise, which makes ergodicity much easier to prove.

## When to use it

Use the Nose-Hoover thermostat for canonical sampling of large systems with many degrees of freedom, such as liquids and solvated proteins, where the motion is chaotic enough. It disturbs the dynamics only a little when $Q$ is not too small, so it is common in runs that also measure dynamical properties. For small or stiff systems, harmonic solids or systems with few degrees of freedom, use [Nose-Hoover chains](/nose-hoover-chains/) or a stochastic thermostat.

## Pitfalls

- **Non-ergodic systems.** One oscillator, a harmonic crystal at low temperature, or a molecule in vacuum can give wrong distributions with the right mean temperature.
- **The choice of $Q$.** A small $Q$ gives fast temperature swings and strong coupling, and a large $Q$ gives slow swings that need long runs. Martyna, Klein and Tuckerman (1992) relate $Q = N_f k_B T \tau^2$ to a thermostat period $\tau$, which is a choice, often a little longer than the period of a typical vibration.
- **Extra conservation laws.** Without external forces the total momentum is conserved, and the sampled distribution is not canonical in the full space. Use $N_f = dN - d$ with the centre of mass fixed at rest.
- **Start far from the target.** Large swings of the temperature at the start can take long to die out, because the thermostat has no damping. Equilibrate first, for example with a [Berendsen thermostat](/berendsen-thermostat/).
- **Monitoring the wrong energy.** $H = K + U$ is not conserved. Monitor $H'$.

## Implementations

## History

Nose (1984) introduced an extended Hamiltonian with a variable that scales time, and proved that its microcanonical ensemble gives canonical averages for the physical variables. In a second paper he gave the equations in real time and related them to other constant-temperature methods. Hoover (1985) simplified the real-time equations to the friction form of this page, derived the stationary canonical density from the Liouville equation, and showed that one harmonic oscillator does not fill its phase space. Martyna, Klein and Tuckerman (1992) added the chains, and Martyna, Tuckerman, Tobias and Klein (1996) gave the reversible splitting into exact flows that is used here.

## References
