---
tag: F8XC41
kind: algorithm
slug: boris-pusher
name: Boris pusher
aliases:
- Boris algorithm
- Boris integrator
area: scientific-computing/n-body-and-particle-methods
level: core
summary: Advances a charged particle in electric and magnetic fields by half an electric kick, a rotation about B and another half kick, preserving phase-space volume.
model: real-ram
complexity:
  vars: {N: the number of particles, T: the number of time steps}
  time: {worst: "Θ(N T)"}
  space: {extra: "Θ(1)"}
properties: {deterministic: true, conservative: true, order: "2"}
history:
  year: 1970
  people: [Jay P. Boris]
  note: Boris presented the scheme at the Fourth Conference on Numerical Simulation of Plasmas in 1970; Qin and coworkers showed in 2013 that it conserves phase space volume although it is not symplectic.
prereqs: [verlet-integration]
see_also: [plasma-particle-in-cell, particle-mesh-method, symplectic-integrators, hamiltonian-systems, runge-kutta-methods, yee-fdtd-scheme, vlasov-poisson-system]
sources:
  - paper: "Jay P. Boris, Relativistic plasma simulation: optimization of a hybrid code, Proceedings of the Fourth Conference on Numerical Simulation of Plasmas, Naval Research Laboratory, Washington DC, November 1970, 3-67"
  - paper: doi:10.1063/1.4818428
    title: Hong Qin, Shuangxi Zhang, Jianyuan Xiao, Jian Liu, Yajuan Sun and William M. Tang, Why is Boris algorithm so good?, Physics of Plasmas 20(8), 2013, 084503
    locator: the proof that the Boris step conserves phase space volume and the remark that it is not symplectic
  - book: isbn:9780750310253
    title: Charles K. Birdsall and A. Bruce Langdon, Plasma Physics via Computer Simulation, Taylor and Francis, 2004 (reprint of the IOP edition of 1991)
    locator: Part 1 (the leapfrog mover with a magnetic field)
---

The Boris pusher is the standard time step for charged particles in [plasma particle-in-cell](/plasma-particle-in-cell/) codes. It advances the position and velocity of a particle in given electric and magnetic fields $\mathbf{E}$ and $\mathbf{B}$ in three parts: half an electric kick, a rotation of the velocity about $\mathbf{B}$, and another half electric kick. The rotation keeps the length of the velocity exactly, so in a pure magnetic field the particle never gains or loses energy, however large the step. The method is second order, time reversible, and it conserves phase space volume, which explains its good behaviour over millions of steps.

## In plain words

A charged particle in a magnetic field goes round in circles, and an electric field pushes it along a line. A simple step that follows the push of the magnetic field in a straight line makes the particle drift outward a little on each turn, so it slowly gains energy that it should not have.

The Boris step avoids this. It first gives the particle half of the electric push. Then it turns the velocity by an angle about the magnetic field, without changing its length. Then it gives the second half of the electric push and moves the particle. Because the turn keeps the speed fixed, a particle in a magnetic field alone keeps its energy forever, and the circles stay closed.

## The problem

A particle of charge $q$ and mass $m$ moves by

$$\frac{d\mathbf{x}}{dt} = \mathbf{v}, \qquad \frac{d\mathbf{v}}{dt} = \frac{q}{m} \bigl(\mathbf{E}(\mathbf{x}) + \mathbf{v} \times \mathbf{B}(\mathbf{x})\bigr),$$

with speeds well below the speed of light. The fields are given; in a PIC code they come from the grid. The input is $\mathbf{x}_0$, the velocity $\mathbf{v}_{-1/2}$ half a step before $t = 0$, the step $h$ and the number of steps $T$. The output is $\mathbf{x}_T$ and $\mathbf{v}_{T - 1/2}$. The gyrofrequency is $\Omega = q |\mathbf{B}| / m$, and in a uniform field $\mathbf{B}$ the exact velocity turns about $\mathbf{B}$ by the angle $-\Omega t$.

## The algorithm

The step solves the implicit midpoint equation for the velocity,

$$\frac{\mathbf{v}_{n+1/2} - \mathbf{v}_{n-1/2}}{h} = \frac{q}{m} \Bigl(\mathbf{E}_n + \frac{\mathbf{v}_{n+1/2} + \mathbf{v}_{n-1/2}}{2} \times \mathbf{B}_n\Bigr),$$

in closed form, with the fields at $\mathbf{x}_n$.

```pseudo id=main
BORIS-RUN(x, v, E, B, q/m, h, T)
L1  for n ← 1 to T do
L2      e ← E(x);  b ← B(x)
L3      v⁻ ← v + (q h / 2m) e                    ▷ first half electric kick
L4      t ← (q h / 2m) b;  s ← 2 t / (1 + |t|²)
L5      v′ ← v⁻ + v⁻ × t
L6      v⁺ ← v⁻ + v′ × s                         ▷ rotation about b, |v⁺| = |v⁻|
L7      v ← v⁺ + (q h / 2m) e                    ▷ second half electric kick
L8      x ← x + h v
L9  return x, v
```

Lines L3 and L7 are the two halves of the electric impulse. Lines L4 to L6 turn $\mathbf{v}^-$ about $\mathbf{b}$ by the angle $-2 \arctan(\Omega h / 2)$, where $|\mathbf{t}| = |\Omega| h / 2$. The length of $\mathbf{t}$ is the tangent of half the angle, and the length of $\mathbf{s}$ is the sine of the full angle; this pair makes the result have the same length as $\mathbf{v}^-$. Line L8 is the drift of the leapfrog. To start from a velocity $\mathbf{v}(0)$, set $\mathbf{v}_{-1/2}$ by one explicit half step backward; this keeps the method second order.

## Example

Take $q/m = 1$, $h = 1$, $\mathbf{B} = (0, 0, 1)$ and $\mathbf{v}_{-1/2} = (1, 0, 0)$.

With $\mathbf{E} = 0$: line L4 gives $\mathbf{t} = (0, 0, 0.5)$ and $\mathbf{s} = (0, 0, 0.8)$. Line L5 gives $\mathbf{v}' = (1, -0.5, 0)$, and line L6 gives $\mathbf{v}^+ = (1, 0, 0) + (-0.4, -0.8, 0) = (0.6, -0.8, 0)$. The speed is still 1, and the velocity has turned clockwise by $\arctan(0.8 / 0.6) = 2 \arctan(0.5) \approx 0.9273$, a little less than the exact angle $\Omega h = 1$.

With $\mathbf{E} = (0.5, 0, 0)$: line L3 gives $\mathbf{v}^- = (1.25, 0, 0)$, lines L5 and L6 give $\mathbf{v}' = (1.25, -0.625, 0)$ and $\mathbf{v}^+ = (0.75, -1, 0)$, and line L7 gives $\mathbf{v}_{1/2} = (1, -1, 0)$. As a check of the midpoint equation, the mean velocity is $(1, -0.5, 0)$, its cross product with $\mathbf{B}$ is $(-0.5, -1, 0)$, and $\mathbf{E}$ plus this is $(0, -1, 0)$, which is the change of the velocity.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). It shows these facts (all theorems).

- Lines L3 to L7 return the unique solution $\mathbf{v}_{n+1/2}$ of the implicit midpoint equation above.
- Lines L4 to L6 are a rotation: $|\mathbf{v}^+| = |\mathbf{v}^-|$, and the angle is $2 \arctan(|\Omega| h / 2)$. So with $\mathbf{E} = 0$ the speed is conserved exactly, for any $h$ and any field $\mathbf{B}(\mathbf{x})$.
- For uniform fields with $\mathbf{E} \perp \mathbf{B}$, the drift velocity $\mathbf{E} \times \mathbf{B} / |\mathbf{B}|^2$ is a fixed point of lines L3 to L7.
- The step is time reversible when $\mathbf{B}$ is reversed with the velocity, as the exact motion is.
- One step, as a map of $(\mathbf{x}, \mathbf{v})$ in $\mathbb{R}^6$, has Jacobian determinant 1 (Qin and coworkers 2013).

The method is second order: it is a symmetric composition of a drift and a velocity map that is itself a symmetric (midpoint) rule. The tests measure an error ratio near 4 when $h$ is halved.

## Complexity

In the [real-RAM](/real-ram/) model, one step of one particle costs one evaluation of the fields and a fixed number of arithmetic operations (two cross products, a few additions and one division), so $T$ steps for $N$ particles cost $\Theta(N T)$ time plus the cost of the field evaluations. The extra space is $\Theta(1)$ per particle beyond its position and velocity. The step needs no square root and no trigonometric function.

## Properties

- **Exact speed in a magnetic field.** The rotation of lines L4 to L6 keeps $|\mathbf{v}|$, so the kinetic energy is constant when $\mathbf{E} = 0$.
- **Phase error in the gyration.** The angle per step is $2 \arctan(\Omega h / 2)$ instead of $\Omega h$. The relative error is about $(\Omega h)^2 / 12$ for small $\Omega h$. For $\Omega h \gg 1$ the particle still moves on a circle of the right radius for its speed, but turns at most by $\pi$ per step.
- **Correct E×B drift.** The drift velocity is exact for uniform fields, for any $h$.
- **Volume preserving but not symplectic.** Qin and coworkers (2013) showed that the step conserves phase space volume, and that it is not symplectic in general. Volume preservation is one reason why errors do not build up over very long runs (a heuristic: no theorem bounds the energy error of the Boris step for all fields).
- **Time reversible.** With $\mathbf{B}$ reversed, running the step backward returns the start.
- **Explicit.** No equation is solved by iteration; the implicit midpoint equation has the closed form solution of lines L3 to L7.

## Variants and improvements

- **Relativistic Boris push.** Advance $\mathbf{u} = \gamma \mathbf{v}$ instead of $\mathbf{v}$, and use $\mathbf{t} = q h \mathbf{B} / (2 m \gamma)$, with $\gamma$ computed from $\mathbf{u}^-$. At very large $\gamma$ this variant gives a wrong drift in strong crossed fields, and later pushers change the rotation step to fix it.
- **Exact-angle rotation.** Replace $\mathbf{t}$ by $\tan(\Omega h / 2) \, \mathbf{b} / |\mathbf{b}|$, which makes the gyration angle exact in a uniform field, at the cost of a tangent.
- **Guiding-centre and gyrokinetic codes.** When $\Omega h$ must be large, codes follow the guiding centre instead of the full orbit.
- **Higher order.** Symmetric compositions of the Boris step (as for [symplectic integrators](/symplectic-integrators/)) give methods of order 4 and higher.

## When to use it

Use the Boris pusher for charged particles in any code where magnetic fields matter and the step is a fixed fraction of the gyroperiod, which is the usual case in PIC simulation and in test particle studies. Keep $\Omega h$ below about 0.5 if the gyration phase must be accurate, since the phase error per step grows as $(\Omega h)^3$. For a pure electric field the step reduces to the leapfrog, so it can be used everywhere without a switch. Use a guiding-centre method instead when the gyration is much faster than every other time scale.

## Pitfalls

- **The wrong sign of the rotation.** The force is $q \mathbf{v} \times \mathbf{B}$, so with $q > 0$ and $\mathbf{B}$ along $z$ the velocity turns clockwise. Swapping the order of the cross product in line L5 or L6 reverses it.
- **Fields at the wrong time.** $\mathbf{E}$ and $\mathbf{B}$ must be taken at $\mathbf{x}_n$, between the two half-step velocities. In electromagnetic codes $\mathbf{B}$ is often stored at half steps and must be averaged to whole steps.
- **Mixing up the half steps.** The velocity in the output is $\mathbf{v}_{T - 1/2}$, not $\mathbf{v}(T)$. Kinetic energy computed from it is off by $O(h)$, so average $\mathbf{v}_{T - 1/2}$ and $\mathbf{v}_{T + 1/2}$ for diagnostics.
- **Using $s = t$.** With $\mathbf{s} = \mathbf{t}$ the rotation changes the speed by a factor $1 + O(|\mathbf{t}|^2)$ per step, and the energy grows.
- **A large $\Omega h$.** The step is stable for any $\Omega h$, but the gyration angle saturates at $\pi$ per step, so the motion is wrong in phase even though the radius is right.

## Implementations

## History

Boris presented the method in 1970 at the Fourth Conference on Numerical Simulation of Plasmas, held at the Naval Research Laboratory in Washington, in a paper on a relativistic hybrid code. Birdsall and Langdon describe it as the standard velocity rotation in their plasma programs. Its long-term accuracy was long known in practice, and Qin, Zhang, Xiao, Liu, Sun and Tang (2013) gave an explanation: the step conserves phase space volume, although it is not symplectic.

## References
