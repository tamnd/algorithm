---
tag: S32WCK
kind: algorithm
slug: verlet-integration
name: Verlet integration
aliases:
- leapfrog integration
- velocity Verlet
- Stormer method
- Störmer-Verlet method
area: numerical/differential-equations
level: core
summary: "Second-order symplectic, time-reversible integrator for Newtonian dynamics q'' = a(q): half kick, drift, half kick, with one force evaluation per step and no energy drift."
solves: [ode-initial-value-problem, hamiltonian-systems]
model: real-ram
complexity:
  vars: {N: "the number of steps, ⌈(T - t_0)/h⌉", k: "the dimension of q", C: "the cost of one evaluation of the force a"}
  time: {worst: "Θ(N (C + k))"}
  space: {extra: "Θ(k)"}
  evaluations: {worst: "N + 1"}
properties: {deterministic: true, implicit: false, one_step: true, order: "2", a_stable: false, symplectic: true, symmetric: true}
history:
  year: 1967
  people: [Carl Størmer, Loup Verlet, Isaac Newton]
  note: Størmer used the two-step form around 1907 for the motion of charged particles in the Earth's magnetic field, and Verlet (1967) made it the standard method of molecular dynamics. Hairer, Lubich and Wanner trace the scheme back to Newton's Principia (1687).
prereqs: [ode-initial-value-problem, local-truncation-error, order-of-accuracy]
see_also: [symplectic-integrators, symplectic-euler-method, hamiltonian-systems, gauss-legendre-runge-kutta, molecular-dynamics, global-error, wave-equation]
sources:
  - book: isbn:9783540306634
    title: Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric Numerical Integration, second edition, Springer, 2006
    locator: Section I.1.4 (the Störmer-Verlet scheme), Section I.3 (Störmer-Verlet as a composition), Section VI.3 (symplecticity), Section IX.8 (long-time energy conservation)
  - paper: "Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric numerical integration illustrated by the Störmer-Verlet method, Acta Numerica 12 (2003) 399-450"
    locator: Sections 1 to 4 (derivations, history from Newton to Verlet, symplecticity, backward error analysis); doi:10.1017/S0962492902000144
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.14 (numerical methods for second order differential equations, Störmer's method)
  - paper: "Loup Verlet, Computer experiments on classical fluids. I. Thermodynamical properties of Lennard-Jones molecules, Physical Review 159 (1967) 98-103"
    locator: the position form used for molecular dynamics; doi:10.1103/PhysRev.159.98
---

Verlet integration solves Newton's equations $q'' = a(q)$ (with $a = -\nabla V$ for a potential $V$) by alternating half kicks of the velocity with a full drift of the position. Written for the first-order system $y = (q, v)$, $y' = (v, a(q))$ in $\mathbb{R}^d$ with $d = 2k$, it is a one-step method of order 2 that costs one force evaluation per step, the same as the [Euler method](/euler-method/). It is symplectic and time-reversible, so on [Hamiltonian systems](/hamiltonian-systems/) its energy error stays bounded over very long times instead of drifting. This makes it the standard method of molecular dynamics and celestial mechanics, and an example of a [symplectic integrator](/symplectic-integrators/).

## In plain words

To move a ball under a force, first give it half the push the force gives over the step, then move it at its new speed for the whole step, then give it the other half push using the force at the new place. Each push uses the force once, and the force at the end of one step is the force at the start of the next, so each step costs one force computation.

The method is balanced: running it backward with a negative step undoes the forward run exactly. Because of that balance, and because it keeps the geometry of the motion, the computed energy of an orbit wobbles slightly but does not creep up or down, even over millions of steps. A method that ignores this structure, even a more accurate one, usually lets the energy creep.

## The problem

Given a force field $a : \mathbb{R}^k \to \mathbb{R}^k$, start values $q_0$, $v_0$ at $t_0$, an end time $T \ge t_0$ and a step size $h > 0$, compute $(q_N, v_N) \approx (q(T), v(T))$. We assume $a \in C^2$ and Lipschitz with constant $L_a$; for the structure results, $a = -\nabla V$. The cost is the number of evaluations of $a$. Errors are measured in the Euclidean norm on $(q, v)$.

## The algorithm

```pseudo id=main
VELOCITY-VERLET(a, t0, q0, v0, T, h)
L1  N ← ⌈(T − t0)/h − δ⌉                     ▷ δ: relative slack 10^-9 against rounding
L2  t ← t0, q ← q0, v ← v0
L3  A ← a(q)
L4  for n ← 0 to N − 1 do
L5      τ ← (T if n = N − 1 else t0 + (n + 1)h) − t
L6      v ← v + (τ/2) A                       ▷ half kick
L7      q ← q + τ v                           ▷ drift
L8      A ← a(q)                              ▷ the only force evaluation of the step
L9      v ← v + (τ/2) A                       ▷ half kick
L10     t ← t + τ
L11 return (t, q, v)
```

Eliminating $v$ gives Störmer's two-step form $q_{n+1} = 2q_n - q_{n-1} + h^2 a(q_n)$, which produces the same positions when started with $q_1 = q_0 + h v_0 + \frac{h^2}{2} a(q_0)$. The "leapfrog" form keeps $v$ at half steps $t_{n+1/2}$. All three are the same method. As in the [Euler method](/euler-method/), $T = t_0$ gives zero steps, and $h > T - t_0$ gives one step of length $T - t_0$.

## Example

Take $q'' = -q$, $q(0) = 1$, $v(0) = 0$, exact $q = \cos t$, with $h = \frac12$ in exact rational arithmetic:

| $n$ | $t_n$ | $q_n$ | $v_n$ | $\cos t_n$ | $-\sin t_n$ |
|---|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 1 | 0 |
| 1 | 0.5 | 7/8 | -15/32 | 0.87758 | -0.47943 |
| 2 | 1.0 | 17/32 | -105/128 | 0.54030 | -0.84147 |

With $h = \frac13$ the quantity $v^2 + (1 - h^2/4) q^2$ equals $35/36$ at every step, exactly (proved below). The max error at $t = 10$ for $h = 0.1, 0.05, 0.025, 0.0125$ is $2.81 \times 10^{-3}$, $7.04 \times 10^{-4}$, $1.76 \times 10^{-4}$, $4.40 \times 10^{-5}$, observed order 2.00.

*Kepler orbit.* With $q'' = -q/|q|^3$, eccentricity $0.5$, period $2\pi$ and $h = 2\pi/200$, the energy error of Verlet over 100 orbits never exceeds $1.34 \times 10^{-3}$, and its maximum is already reached in the first 10 orbits (observed). Halving $h$ divides it by 4.03. Angular momentum is conserved to $2 \times 10^{-14}$, because the force is central. Heun's method, also of order 2 with the same $h$ but two evaluations per step, has energy errors $9.5 \times 10^{-4}$, $1.2 \times 10^{-2}$ and $7.9 \times 10^{-2}$ after 1, 10 and 100 orbits, a steady drift.

## Correctness

**Theorem (proved).** Let $a \in C^2$ be Lipschitz. Then:
1. Velocity Verlet has local error $O(h^3)$ and global error $O(h^2)$ on bounded intervals.
2. It is symmetric: $\Phi_{-h} \circ \Phi_h = \mathrm{id}$.
3. If $a = -\nabla V$, then each step is a symplectic map.
4. For $q'' = -\omega^2 q$ and $z = h\omega$, it conserves $v^2 + \omega^2(1 - z^2/4) q^2$ exactly, is stable for $0 < z < 2$ and unstable for $z \ge 2$.

The proof writes the step as kick, drift, kick. Each of these is the exact flow of a simple Hamiltonian, so each is symplectic, and the inverse of each is the same map with $-\tau$. Order 2 follows from a two-term Taylor expansion and the usual Lipschitz argument for one-step methods; see [global error](/global-error/). The long-time statement $|H(y_n) - H(y_0)| = O(h^2)$ for exponentially long times is an asymptotic result of backward error analysis, which we cite from Hairer, Lubich and Wanner (Section IX.8) without proof.

## Complexity

Each step evaluates $a$ once (line L8) and does $\Theta(k)$ vector work, so $N$ steps cost $N + 1$ force evaluations and $\Theta(N(C + k))$ time. Only $q$, $v$ and $A$ are stored, $\Theta(k)$ extra space. In molecular dynamics the force evaluation dominates, often $\Theta(k)$ with neighbour lists or $\Theta(k \log k)$ with tree or mesh methods.

## Properties

- **Order** 2; explicit; one force evaluation per step.
- **Symplectic** for $a = -\nabla V$, and **symmetric** (time-reversible).
- **Conservation.** First integrals that are bilinear in $q$ and $v$, of the form $q^T B v$, in particular angular momentum for central forces, are conserved exactly (Hairer, Lubich and Wanner, Section IV.2). Energy is not conserved exactly, but its error stays $O(h^2)$ over exponentially long times (asymptotic, cited).
- **Stability.** Linear stability needs $h\omega < 2$ for the fastest frequency $\omega$. The method is not A-stable and not meant for stiff problems.
- **Variable steps** destroy symplecticity and the long-time behaviour unless done with special care.

## Variants and improvements

- **Position Verlet** (drift, kick, drift) is the adjoint ordering with the same properties.
- **[Symplectic Euler](/symplectic-euler-method/)** is half of a Verlet step; Verlet is the composition of symplectic Euler and its adjoint with steps $h/2$.
- **Composition methods** (Yoshida, Suzuki) combine Verlet steps of sizes $\gamma_i h$ to reach orders 4, 6 and 8 while keeping symmetry and symplecticity.
- **Multiple time stepping** (r-RESPA, impulse method) kicks with slow forces at a long step and integrates fast forces with Verlet at short steps.
- **RATTLE and SHAKE** add holonomic constraints, such as fixed bond lengths.
- **Implicit symplectic methods** such as the [Gauss-Legendre Runge-Kutta methods](/gauss-legendre-runge-kutta/) handle non-separable Hamiltonians.

## When to use it

Use Verlet for long simulations of conservative mechanical systems with separable energy $\frac12|v|^2 + V(q)$: molecular dynamics, planetary and N-body problems, particle methods for plasmas, and the semi-discrete [wave equation](/wave-equation/), where leapfrog in time is the same scheme. Use a fixed step. For short, accurate trajectories, or for problems with dissipation, an adaptive Runge-Kutta method is usually better. For stiff forces, the step limit $h\omega < 2$ forces tiny steps.

## Pitfalls

- **Step limit.** For $q'' = -q$, $h = 1.99$ stays bounded over 1000 steps, while $h = 2.01$ grows to $3 \times 10^{86}$ (observed).
- **Adaptive steps.** Changing $h$ from step to step with an error controller destroys the long-time energy behaviour. Use a fixed step, or a reversible step-size rule.
- **Starting the two-step form.** Using $q_1 = q_0 + h v_0$ in Störmer's form reduces the global order to 1.
- **Velocity at the wrong time.** In the leapfrog form the stored velocity lives at half steps. Computing the energy with it gives an error of order $h$, not $h^2$.
- **Shortened last step.** Ending exactly at $T$ with a shorter last step is fine for accuracy, but it breaks the exact conservation of the modified energy for that step.

## Implementations

## History

Hairer, Lubich and Wanner (2003) trace the scheme back to Newton's Principia (1687), where it appears in the proof of Kepler's second law. Störmer used the two-step form from about 1907 to compute trajectories of charged particles in the Earth's magnetic field, for the theory of the aurora. Verlet (1967) used it for molecular dynamics of Lennard-Jones fluids, and the velocity form was introduced by Swope, Andersen, Berens and Wilson (1982). Its symplecticity and the backward error analysis that explains its energy behaviour came in the 1980s and 1990s.

## References
