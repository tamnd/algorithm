---
tag: 2SQEWG
kind: algorithm
slug: respa-multiple-time-step
name: Reversible reference system propagator algorithm
aliases:
- r-RESPA
- multiple time step integrator
area: scientific-computing/molecular-simulation
level: advanced
summary: Splits forces into fast and slow parts and integrates the fast part with smaller steps inside a symplectic Trotter splitting.
model: real-ram
complexity:
  vars: {N: the number of coordinates, n: the number of inner steps per outer step, F: the cost of one fast force, S: the cost of one slow force}
  time: {worst: O(n F + S + n N)}
  space: {extra: O(N)}
properties: {deterministic: true, symplectic: true, time_reversible: true, order: "2"}
history:
  year: 1992
  people: [Mark Tuckerman, Bruce J. Berne, Glenn J. Martyna]
  note: Tuckerman, Berne and Martyna derived the method in 1992 from a Trotter factorisation of the Liouville propagator; Grubmüller, Heller, Windemuth and Schulten had given the same impulse scheme in 1991.
prereqs: [verlet-integration, operator-splitting]
see_also: [symplectic-integrators, shadow-hamiltonian, hamiltonian-systems, molecular-dynamics, smooth-particle-mesh-ewald, ewald-summation, stiff-ode-problem, langevin-dynamics]
sources:
  - paper: doi:10.1063/1.463137
    title: Mark Tuckerman, Bruce J. Berne and Glenn J. Martyna, Reversible multiple time scale molecular dynamics, Journal of Chemical Physics 97(3), 1992, 1990-2001
    locator: the Trotter factorisation of the classical propagator into fast and slow parts
  - paper: doi:10.1080/08927029108022142
    title: Helmut Grubmüller, Helmut Heller, Andreas Windemuth and Klaus Schulten, Generalized Verlet algorithm for efficient molecular dynamics simulations with long-range interactions, Molecular Simulation 6(1-3), 1991, 121-142
    locator: the impulse form of the multiple time step method
  - paper: doi:10.1137/S1064827501399833
    title: Qun Ma, Jesús A. Izaguirre and Robert D. Skeel, Verlet-I/r-RESPA/impulse is limited by nonlinear instabilities, SIAM Journal on Scientific Computing 24(6), 2003, 1951-1973
    locator: the resonance limit on the outer step
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 5.4, Non-bonded interactions and multiple timesteps
---

The reversible reference system propagator algorithm, r-RESPA, is a multiple time step integrator for molecular dynamics. It splits the force into a fast part, such as bond vibrations, which is cheap and changes quickly, and a slow part, such as long-range electrostatics, which is costly and changes slowly. One outer step of size $h$ gives a half kick with the slow force, then $n$ [velocity Verlet](/verlet-integration/) steps of size $h/n$ with the fast force alone, then a second half kick with the slow force. The slow force is computed once per outer step instead of $n$ times. Each part is the exact flow of a Hamiltonian, so the step is symplectic, time reversible and of order 2. Its limit is resonance: when $h$ is close to half a period of a fast motion, or as Ma, Izaguirre and Skeel found, even a third of one, the slow kicks pump energy into the fast motion. The [shadow Hamiltonian](/shadow-hamiltonian/) theory explains the good energy behaviour of a symplectic method with a step small against all time scales; RESPA uses an outer step that is not small against the fast ones, which is why the resonance is possible.

## In plain words

In a molecule, some forces change very fast and some change slowly. A normal integrator must use a step small enough for the fastest force, and it pays for all forces at every small step. That is a waste, because the slow forces are often the costly ones.

RESPA gives the slow force a big step and the fast force many small steps inside it. It starts with half a push from the slow force, then lets the atoms move under the fast force alone for many small steps, then gives the second half push from the slow force. The pattern is the same backward and forward in time, which keeps the energy from drifting. The big step must not match the rhythm of the fast motion, or the pushes build it up like a swing.

## The problem

There are positions $x$ and velocities $v$ with inverse masses $W$, and the force is split as $F = F_{\text{fast}} + F_{\text{slow}}$, where both parts come from potentials, $F_{\text{fast}} = -\nabla U_{\text{fast}}$ and $F_{\text{slow}} = -\nabla U_{\text{slow}}$. Given an outer step $h$ and a number $n$ of inner steps, find a map $\Psi_h$ that approximates the flow of $H = \frac12 v^{\mathsf T} W^{-1} v + U_{\text{fast}} + U_{\text{slow}}$ with one evaluation of $F_{\text{slow}}$ per step. The operator form is the Trotter splitting
$$\Psi_h = e^{\frac{h}{2} L_{\text{slow}}} \bigl[ e^{\frac{\delta}{2} L_{\text{fast}}} e^{\delta L_x} e^{\frac{\delta}{2} L_{\text{fast}}} \bigr]^n e^{\frac{h}{2} L_{\text{slow}}}, \qquad \delta = h / n,$$
where $L_{\text{slow}}$ and $L_{\text{fast}}$ are the kicks with each force and $L_x$ is the free drift.

## The algorithm

```pseudo id=main
RESPA-STEP(x, v, W, F_fast, F_slow, h, n)
L1  v ← v + (h/2) W F_slow(x)                  ▷ slow half kick
L2  for k ← 1 to n do                          ▷ δ = h / n
L3      v ← v + (δ/2) W F_fast(x)
L4      x ← x + δ v
L5      v ← v + (δ/2) W F_fast(x)
L6  v ← v + (h/2) W F_slow(x)                  ▷ slow half kick
L7  return (x, v)
```

The fast force at the end of one inner step is the one at the start of the next, so one call per inner step is enough. The slow force at the end of an outer step is the one at the start of the next. More levels are possible: the fast loop can itself be a RESPA step with a faster force inside.

## Example

Take one particle of mass 1 with a fast spring $F_{\text{fast}} = -\Omega^2 x$, $\Omega = 10$, so the fast period is $0.628$, and a slow pendulum force $F_{\text{slow}} = -\sin x$. Start at $x = 1$, $v = 0$, with the energy $H = 50.4597$, and run to the time 20. The largest energy error over the run:

| method | slow force calls | fast force calls | largest energy error |
|---|---|---|---|
| Verlet, $h = 0.1$ | 200 | 200 | 12.72 |
| RESPA, $h = 0.1$, $n = 10$ | 200 | 2000 | 0.293 |
| RESPA, $h = 0.05$, $n = 10$ | 400 | 4000 | 0.0707 |
| Verlet, $h = 0.01$ | 2000 | 2000 | 0.127 |

RESPA with ten inner steps cuts the error of Verlet with the large step by a factor of 43 at the same number of slow force calls. Halving the outer step divides the error by 4.1, the second order. Verlet with the small step is more accurate, but it calls the slow force ten times as often.

**Resonance.** Replace the slow force by $-\kappa x$ with $\kappa = 1$, and use $n = 200$ inner steps. The one-step map is linear with determinant 1, so it is stable only when the absolute value of its trace is below 2. The trace from the code agrees to $3 \times 10^{-5}$ with the formula $2 \cos(\Omega h) - \kappa h \sin(\Omega h) / \Omega$:

| outer step $h$ | trace |
|---|---|
| 0.1 | 1.0722 |
| 0.2 | -0.8505 |
| 0.25 | -1.6173 |
| 0.3 | -1.9842 |
| $(\pi - 0.015)/10 = 0.31266$ | -2.00024 |

The last step is just below half the fast period, and the map is unstable there: after 3000 steps the amplitude has grown by a factor of about $3 \times 10^{19}$. The same total force with a third of that step is stable.

## Correctness

The proof below shows these claims:

1. **The step** is the composition of the slow half kick, $n$ velocity Verlet steps with the fast force, and the slow half kick, the Trotter splitting above.
2. **Special cases.** With $n = 1$ it is velocity Verlet with the full force. With no slow force it is $n$ Verlet steps of size $h/n$.
3. **Symplectic.** Each part is the exact flow of a Hamiltonian, and a composition of symplectic maps is symplectic.
4. **Time reversible.** The composition is a palindrome, so reversing the velocities and taking one step returns to the start.
5. **Order 2,** because a symmetric method has even order.
6. **Resonance in a linear model.** With the inner loop replaced by its exact limit, the trace of the step is $2 \cos(\Omega h) - \kappa h \sin(\Omega h) / \Omega$, and there are unstable steps just below $\pi / \Omega$ for every $\kappa > 0$. This is a theorem for the model; the limit of about a third of the fast period found by Ma, Izaguirre and Skeel (2003) for nonlinear systems is a measurement.

The tests check both special cases, reversibility to $10^{-10}$, the preserved area to $10^{-6}$, the second order of the energy error, and the resonance.

## Complexity

One outer step costs $n$ fast force calls, one slow force call and $\Theta(nN)$ for the updates, where $N$ is the number of coordinates. With Verlet at the small step $h/n$, the same time costs $n$ calls of each force. RESPA saves almost a factor of $n$ when the slow force dominates the cost. Memory is $\Theta(N)$, plus one stored slow force.

## Properties

- **Symplectic and reversible,** so the energy stays in a band for steps away from resonance.
- **Order two** in the outer step for a fixed $n$.
- **One slow force per outer step,** with the stored force reused at the start of the next step.
- **Resonance limited.** The outer step must stay below about a third of the shortest period of the fast motion for nonlinear systems, which caps the possible gain.
- **Nested.** Three or more levels of forces fit the same pattern.

## Variants and improvements

- **Impulse method.** The same scheme is the impulse method or Verlet-I of Grubmüller, Heller, Windemuth and Schulten (1991).
- **Mollified impulse.** Evaluating the slow force at averaged positions softens the kicks and widens the stable range of steps.
- **Isokinetic and stochastic versions.** Thermostats that hold the kinetic energy of each degree of freedom, or Langevin damping on the fast modes, damp the resonance and can allow larger outer steps.
- **Splitting by distance.** In molecular dynamics, the slow force is often the long-range part of the electrostatics from [SPME](/smooth-particle-mesh-ewald/), and the fast force contains the bonds and short-range pairs.
- **With constraints.** The position and velocity projections of [RATTLE](/rattle-algorithm/) fit after each inner drift and kick.

## When to use it

Use RESPA when a costly force changes slowly and a cheap force changes fast, for example the reciprocal part of the Ewald sum against bonded and short-range forces. Keep the outer step well below half the shortest period of the fast motion, and in practice below a third of it. When the costly force is not much smoother than the cheap one, or when the bonds to hydrogen are already removed by constraints, the gain is small, and plain Verlet is simpler.

## Pitfalls

- **Resonance.** An outer step near half a period of any fast motion, or near a multiple of it, makes the energy grow. Scan the outer step on a small test before a long run.
- **A slow force that is not smooth.** A sharp cutoff between the fast and slow parts puts fast changes into the slow force. Split with a smooth switching function.
- **Kicks in the wrong place.** The slow half kicks must come at both ends of the outer step, not one full kick at one end, or the method loses its symmetry and its second order.
- **Reusing the wrong force.** The slow force at the end of an outer step must be computed at the final positions of the inner loop.

## Implementations

## History

Grubmüller, Heller, Windemuth and Schulten (1991) gave the impulse form of multiple time stepping for long-range interactions. Tuckerman, Berne and Martyna (1992) derived the reversible version from a Trotter factorisation of the classical Liouville propagator. Ma, Izaguirre and Skeel (2003) analysed the instabilities and found that nonlinear resonance limits the outer step to about a third of the fastest period.

## References
