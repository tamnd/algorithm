---
tag: B9ZN3M
kind: algorithm
slug: symplectic-euler-method
name: Symplectic Euler method
aliases:
- semi-implicit Euler method
- symplectic Euler
- Euler-Cromer method
- semi-explicit Euler method
area: numerical/differential-equations
level: advanced
summary: "First-order Euler variant for Hamiltonian systems that updates momentum and position in turn, each with the newest value of the other. It is symplectic, so energy errors stay bounded."
solves: [hamiltonian-systems, ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps, ⌈(T - t_0)/h⌉", k: "the dimension of q and p", C: "the cost of one evaluation of grad T and grad V"}
  time: {worst: "Θ(N (C + k))"}
  space: {extra: "Θ(k)"}
  evaluations: {worst: "2 N"}
properties: {deterministic: true, implicit: false, one_step: true, order: "1", a_stable: false, symplectic: true, symmetric: false}
history:
  year: 1956
  people: [René de Vogelaere, Ronald D. Ruth, Feng Kang]
  note: De Vogelaere (1956) gave symplectic Euler and its adjoint in a report on canonical integration; Ruth (1983) and Feng Kang (1985) rediscovered symplectic methods and started their systematic study.
prereqs: [euler-method, hamiltonian-systems]
see_also: [verlet-integration, symplectic-integrators, gauss-legendre-runge-kutta, operator-splitting, global-error, stability-region]
sources:
  - book: isbn:9783540306634
    title: Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric Numerical Integration, second edition, Springer, 2006
    locator: Section I.1 (the symplectic Euler method on the Lotka-Volterra and pendulum problems), Section II.2 (symplectic Euler as a partitioned Runge-Kutta method), Section VI.3 (Theorem VI.3.3, symplecticity), Section IX.3 (modified Hamiltonian)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.16 (symplectic integration methods)
  - paper: "René de Vogelaere, Methods of integration which preserve the contact transformation property of the Hamiltonian equations, Report 4, Department of Mathematics, University of Notre Dame, 1956"
    locator: the first symplectic methods
  - paper: "Ronald D. Ruth, A canonical integration technique, IEEE Transactions on Nuclear Science 30 (1983) 2669-2671"
    locator: symplectic methods for accelerator physics; doi:10.1109/TNS.1983.4332919
---

The symplectic Euler method integrates a [Hamiltonian system](/hamiltonian-systems/) $p' = -H_q(p, q)$, $q' = H_p(p, q)$ by updating the momentum and then the position, each update using the newest value of the other variable. In the page notation $y = (q, p)$ and $y' = f(y)$. For a separable energy $H = T(p) + V(q)$ the step is explicit and costs the same as the [Euler method](/euler-method/): one evaluation of $\nabla V$ and one of $\nabla T$. Like Euler it has order 1, but its step map is symplectic, so on long runs the energy error stays bounded instead of drifting. Two half steps of it and its adjoint give the [Verlet method](/verlet-integration/).

## In plain words

The ordinary Euler method moves the position with the old velocity and changes the velocity with the old force, both at once. For a swinging pendulum that slowly pumps energy in, and the swing grows until the pendulum goes over the top.

The symplectic version makes one small change: first update the speed using the force, then move using the new speed. This ordering makes each step preserve area in the space of positions and speeds, which is the geometric rule real mechanical motion obeys. The computed energy still has an error of the size of the step, but it wobbles around the right value forever instead of growing. The method is no more expensive than plain Euler.

## The problem

Given $\nabla T$ and $\nabla V$ for $H(p, q) = T(p) + V(q)$ with $p, q \in \mathbb{R}^k$, start values $q_0$, $p_0$ at $t_0$, an end time $T \ge t_0$ and a step size $h > 0$, compute $(q_N, p_N) \approx (q(T), p(T))$. We assume $\nabla T$ and $\nabla V$ are Lipschitz with constant $L$. The cost is the number of evaluations of $\nabla T$ and $\nabla V$. Errors are measured in the Euclidean norm.

## The algorithm

```pseudo id=main
SYMPLECTIC-EULER(∇T, ∇V, t0, q0, p0, T, h)
L1  N ← ⌈(T − t0)/h − δ⌉                       ▷ δ: relative slack 10^-9 against rounding
L2  t ← t0, q ← q0, p ← p0
L3  for n ← 0 to N − 1 do                       ▷ step τ = h, or T − t for the last step
L4      p ← p − τ ∇V(q)                          ▷ kick with the old position
L5      q ← q + τ ∇T(p)                          ▷ drift with the new momentum
L6      t ← t + τ
L7  return (t, q, p)
```

The adjoint (variant B) swaps lines L4 and L5: drift with the old momentum, then kick with the new position. For a general $H(p, q)$, variant A reads $p_{n+1} = p_n - hH_q(p_{n+1}, q_n)$, $q_{n+1} = q_n + hH_p(p_{n+1}, q_n)$, which is implicit in $p_{n+1}$ only; the implementation solves it by fixed-point iteration. As a partitioned Runge-Kutta method it treats $p$ by implicit Euler and $q$ by explicit Euler.

## Example

Take $H = (p^2 + q^2)/2$, so $q'' = -q$, with $q(0) = 1$, $p(0) = 0$ and $h = \frac12$ in exact arithmetic:

| $n$ | $t_n$ | $q_n$ | $p_n$ | $\cos t_n$ | $-\sin t_n$ |
|---|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 1 | 0 |
| 1 | 0.5 | 3/4 | -1/2 | 0.87758 | -0.47943 |
| 2 | 1.0 | 5/16 | -7/8 | 0.54030 | -0.84147 |

With $h = \frac13$, the quantity $q^2 + p^2 - hqp$ equals 1 at every step, exactly. The max error at $t = 10$ for $h = 0.1, 0.05, 0.025, 0.0125$ is $2.97 \times 10^{-2}$, $1.42 \times 10^{-2}$, $6.95 \times 10^{-3}$, $3.44 \times 10^{-3}$, observed order 1.

*Pendulum.* For $H = p^2/2 - \cos q$, $q(0) = 0$, $p(0) = 1.5$, $h = 0.1$ and $t \in [0, 100]$, the energy error of symplectic Euler never exceeds $0.051$, and $0.025$ with $h = 0.05$ (observed). Explicit Euler with the same step gains $5.07$ in energy by $t = 100$; the pendulum, which should swing, ends up rotating over the top.

## Correctness

**Theorem (proved).** Let $\nabla T$ and $\nabla V$ be $C^1$ and Lipschitz. Then:
1. symplectic Euler converges with global error $O(h)$ on bounded intervals;
2. each step is a symplectic map;
3. variant B with step $-h$ inverts variant A with step $h$;
4. variant A with step $h/2$ followed by variant B with step $h/2$ is one step of Störmer-Verlet;
5. on the harmonic oscillator it conserves $q^2 + p^2 - hqp$ exactly, and it is stable for $0 < h < 2$ and unstable for $h > 2$.

The step is the composition of a kick, which changes only $p$, and a drift, which changes only $q$. Each is the exact flow of the Hamiltonian $V(q)$ or $T(p)$ for time $h$. Their Jacobians are shears with symmetric off-diagonal blocks, which are symplectic, and so is their product. Convergence is the usual Lipschitz argument for one-step methods. Symplecticity of the implicit variant for non-separable $H$, and the long-time energy bound $|H(y_n) - H(y_0)| = O(h)$ over exponentially long times, are cited from Hairer, Lubich and Wanner (Theorem VI.3.3 and Section IX.8), not proved here.

## Complexity

Each step evaluates $\nabla V$ once and $\nabla T$ once and does $\Theta(k)$ vector work: $2N$ evaluations and $\Theta(N(C + k))$ time, $\Theta(k)$ extra space. Usually $T(p) = \frac12 p^T M^{-1} p$, so $\nabla T$ is a cheap linear map and the force $\nabla V$ dominates. For non-separable $H$ each step also solves a nonlinear system of size $k$.

## Properties

- **Order** 1, explicit for separable $H$.
- **Symplectic**, not symmetric: the method is not its own adjoint, so it is not time-reversible.
- **Conservation.** Quadratic invariants of the form $q^T B p$, such as angular momentum, are conserved exactly. Energy is conserved up to $O(h)$ over very long times (cited, asymptotic).
- **Linear stability** for $q'' = -\omega^2 q$ requires $h\omega < 2$.
- **Variable steps** destroy the long-time behaviour.

## Variants and improvements

- **Adjoint (variant B):** drift first, kick second.
- **[Störmer-Verlet](/verlet-integration/):** the composition of the two variants with half steps, order 2 and symmetric, at the same cost per step.
- **Composition methods** of higher order (Yoshida, Suzuki) and splitting methods (see [operator splitting](/operator-splitting/)).
- **Implicit symplectic methods** such as the [Gauss-Legendre Runge-Kutta methods](/gauss-legendre-runge-kutta/) for non-separable $H$ and higher order.
- **Euler-Cromer** is the name used in physics teaching for the same scheme on $q'' = a(q)$.

## When to use it

Use symplectic Euler as a simple, cheap long-time integrator for separable Hamiltonian systems when order 1 is enough, for teaching, and as the building block of splitting methods. In almost every practical case, Störmer-Verlet costs the same per step and gives order 2, so it is the better default. Do not use either for problems with damping, forcing, or stiffness, where their structural advantages disappear.

## Pitfalls

- **Wrong order of updates.** Updating $q$ and $p$ from the same old values is explicit Euler, which drifts in energy.
- **Mixing variants.** Using A in one step and B in the next by accident (for example, by swapping lines when refactoring) changes the method; consistently alternating them with half steps gives Verlet.
- **Reading the energy at the wrong time.** The positions and momenta are each first-order accurate, but the conserved quantity is the modified energy, so the observed energy oscillates with amplitude $O(h)$.
- **Step limit.** For $q'' = -q$, $h = 1.99$ stays bounded over 1000 steps, while $h = 2.01$ grows beyond $10^{80}$ (observed).

## Implementations

## History

De Vogelaere (1956) described symplectic Euler and its adjoint in a little-known report on integration methods that preserve the canonical structure. Ruth (1983), working on particle accelerators, and Feng Kang (1985) rediscovered symplectic methods and started their systematic study. Sanz-Serna (1988), Lasagni and Suris characterized the symplectic Runge-Kutta methods (Hairer, Lubich and Wanner 2006, Section VI.3).

## References
