---
tag: V7E58W
kind: algorithm
slug: model-reference-adaptive-control
name: Model reference adaptive control
aliases:
- MRAC
- Lyapunov-based MRAC
area: control/robust-and-adaptive-control
level: core
summary: Adjusts the controller so that the plant output follows a reference model, with an adaptation law chosen to make a Lyapunov function decrease.
model: real-ram
complexity:
  vars: {N: the number of integration steps, n: the order of the plant}
  time: {worst: O(n^6 + N n^2)}
  space: {extra: O(n^4)}
properties: {deterministic: true, exact: false, recursive: false, online: true}
history:
  year: 1966
  people: [P. C. Parks]
  note: "Parks replaced the gradient rule of the MIT scheme by an adaptation law derived from a Lyapunov function, which gave bounded signals and a model following error that goes to zero."
prereqs: [adaptive-control, mit-rule, state-feedback, lyapunov-direct-method, lyapunov-equation]
see_also: [slotine-li-adaptive-control, barbalat-lemma, persistent-excitation, rohrs-counterexample, sigma-modification, parameter-projection, l1-adaptive-control, self-tuning-regulator]
sources:
  - book: isbn:9780486462783
    title: "Karl Johan Åström and Björn Wittenmark, Adaptive Control, second edition, Addison-Wesley 1995 (Dover reprint 2008)"
    locator: "Chapter 5, Model-reference adaptive systems: the sections on Lyapunov theory and on the design of model reference adaptive systems with Lyapunov theory"
  - book: isbn:9780486498171
    title: "Petros A. Ioannou and Jing Sun, Robust Adaptive Control, Prentice Hall 1996 (Dover reprint 2012)"
    locator: "Chapter 6, Model reference adaptive control: Section 6.2 (simple direct MRAC schemes, with the scalar and the full state examples)"
  - paper: doi:10.1109/TAC.1966.1098361
    title: "P. C. Parks, Liapunov redesign of model reference adaptive control systems, IEEE Transactions on Automatic Control 11(3), 1966"
    locator: "pages 362 to 367"
---

Model reference adaptive control (MRAC) is a direct adaptive controller: it adjusts the gains of a controller online so that the plant follows a reference model with a Hurwitz state matrix, with the adaptation law chosen so that a [Lyapunov function](/lyapunov-function/) of the tracking error and the gain error never increases. This page treats the state feedback form for a linear plant with unknown constant matrices. The result is a theorem: all signals stay bounded and the error goes to zero for every bounded reference, and the gains converge to their ideal values when the reference is [persistently exciting](/persistent-excitation/). The [Slotine-Li adaptive controller](/slotine-li-adaptive-control/) of robotics uses the same Lyapunov construction for the nonlinear dynamics of a robot arm, with the regressor of the arm in place of the state.

## In plain words

You choose a model that shows how the controlled system should behave. The real system and the model get the same command, and the controller compares their states. A controller with adjustable gains acts on the real system. When the real system lags or overshoots the model, the gains move in the direction that removes the difference. The rule for this movement is not a guess: it is chosen so that a measure of the total error, made from the tracking error and the gain error, can only fall. So the gains and the states cannot run away, and the tracking error dies out. The gains themselves reach the correct values only if the command is rich enough, for example a sum of sine waves.

## The problem

The plant is $\dot x = A x + b u$ with the state $x \in \mathbb{R}^n$ measured, a single input $u$, and $A$, $b$ unknown. The reference model is $\dot x_m = A_m x_m + b_m r$, where $A_m$ is a Hurwitz matrix and $r(t)$ is a bounded, piecewise continuous reference. The controller is $u = k^T x + l\,r$ with adjustable $k \in \mathbb{R}^n$ and $l \in \mathbb{R}$. The structural assumptions are these.

- **Matching.** There are constant $k^*$ and $l^*$ with $A + b\,k^{*T} = A_m$ and $b\,l^* = b_m$. Then the controller with $k = k^*$ and $l = l^*$ makes the closed loop equal to the model.
- **Known sign.** The sign of $l^*$ is known. This is the sign of the high frequency gain of the plant.

The aim is to choose $\dot k$ and $\dot l$ from measured signals so that the tracking error $e = x - x_m$ goes to zero and all signals stay bounded.

## The algorithm

With $\tilde k = k - k^*$ and $\tilde l = l - l^*$, the matching conditions give the error equation

$$\dot e = A_m e + \frac{b_m}{l^*}\big(\tilde k^T x + \tilde l\, r\big).$$

Choose a symmetric positive definite $Q$ and solve the [Lyapunov equation](/lyapunov-equation/) $A_m^T P + P A_m = -Q$ for $P$. With $\gamma > 0$, the adaptive laws are

$$\dot k = -\gamma\,\mathrm{sgn}(l^*)\, x\, b_m^T P e, \qquad \dot l = -\gamma\,\mathrm{sgn}(l^*)\, r\, b_m^T P e.$$

The plant, the model and the gains form one system of differential equations. The implementation integrates it with the classical fourth order Runge-Kutta method and a fixed step $dt$.

```pseudo id=main
MRAC(A_m, b_m, Q, γ, sgn, k₀, l₀, dt, N)          ▷ A_m Hurwitz, Q ≻ 0, γ > 0
L1  solve A_mᵀ P + P A_m = -Q for P
L2  k ← k₀; l ← l₀; set the states x and x_m
L3  for i ← 0 to N - 1 do
L4      r ← r(t)                                  ▷ the reference at t = i dt
L5      e ← x - x_m                               ▷ tracking error
L6      u ← kᵀ x + l r
L7      x' ← A x + b u; x_m' ← A_m x_m + b_m r
L8      k' ← -γ sgn x (b_mᵀ P e); l' ← -γ sgn r (b_mᵀ P e)
L9      advance x, x_m, k and l by one RK4 step of length dt
L10 return k, l
```

Line L1 runs once. Lines L4 to L8 are the right-hand side of the differential equation, and RK4 evaluates them four times per step in line L9. The plant matrices $A$ and $b$ in line L7 stand for the real plant; the controller uses only the measured $x$.

## Example

**Scalar plant.** The plant $\dot y = y + 2u$ has a pole at $+1$. The model is $\dot y_m = -2 y_m + 2 r$, so $k^* = -(1 + 2)/2 = -1.5$ and $l^* = 1$. With $Q = 4$ the Lyapunov equation gives $P = 1$, and the laws are $\dot k = -2\gamma\, y e$ and $\dot l = -2\gamma\, r e$. All states and gains start at zero, and $dt = 0.01$ s.

| Reference | $\gamma$ | $k(10)$ | $l(10)$ | $k(60)$ | $l(60)$ |
|---|---|---|---|---|---|
| $\sin t$ | 1 | -1.4731 | 0.9438 | -1.4997 | 0.9996 |
| $\sin t$ | 5 | -1.5248 | 1.0466 | -1.5000 | 1.0000 |
| 1 | 1 | -1.0756 | 0.5879 | -1.0818 | 0.5818 |
| 1 | 5 | -1.2382 | 0.7363 | -1.2372 | 0.7372 |

With the constant reference the error goes to zero in all runs, but the gains stop at a wrong point. The point is on the line $k + l = -0.5$, which is the set of gains with the correct static gain $2l/(-(1 + 2k)) = 1$. A constant reference fixes only this one number. The sine excites one frequency, which fixes two numbers, and the gains converge to $(k^*, l^*)$.

**Second order plant.** The plant $\dot x_1 = x_2$, $\dot x_2 = x_1 - x_2 + u$ is unstable. The model has $A_m = [0, 1; -4, -2]$ and $b_m = (0, 4)$, so $k^* = (-5, -1)$ and $l^* = 4$. With $Q = I$ the exact solution is $P = [3/2, 1/8; 1/8, 5/16]$. The reference is $r = \sin t + \sin 3t$, $x(0) = (1, 0)$, and the gains start at zero. For $\gamma = 1$, $V(0) = 12$ and $V(60) = 3.4 \times 10^{-9}$, and $V$ decreases at every sample. The gains are $k(10) = (-4.522, -0.747)$, $l(10) = 3.697$, $k(30) = (-4.987, -1.000)$, $l(30) = 3.993$, and $(k, l) = (-5.000, -1.000, 4.000)$ at $t = 60$. Three gains need two frequencies; one sine would not be enough.

## Correctness

Take $V = e^T P e + (\tilde k^T \tilde k + \tilde l^2)/(\gamma |l^*|)$. Along solutions,

$$\dot V = -e^T Q e + \frac{2}{l^*} e^T P b_m(\tilde k^T x + \tilde l r) + \frac{2}{\gamma |l^*|}(\tilde k^T \dot k + \tilde l \dot l) = -e^T Q e \le 0,$$

because the laws make the last two terms cancel. So $e$, $k$ and $l$ are bounded, and $e$ is square integrable. Since $x_m$ is bounded, $x = e + x_m$ and $\dot e$ are bounded, and [Barbalat's lemma](/barbalat-lemma/) gives $e(t) \to 0$. If in addition the regressor $(x_m, r)$ is persistently exciting, the gain errors go to zero exponentially. The full proof is in [proofs/correctness.md](proofs/correctness.md); the tests check that $V$ never increases and that $V(0) - V(T)$ equals the integral of $e^T Q e$.

## Complexity

In the real-RAM model, the Lyapunov equation in line L1 is a linear system of $n^2$ unknowns. The implementation solves it in Kronecker form by Gaussian elimination, which costs $O(n^6)$ operations and $O(n^4)$ memory once; a Bartels-Stewart solver would cost $O(n^3)$. Each evaluation of the right-hand side costs $O(n^2)$ for the plant and the model and $O(n)$ for the laws, so $N$ RK4 steps cost $O(N n^2)$. In a real controller the plant is the physical system, and the work per sample is $O(n^2)$ for the model and $O(n)$ for the laws.

## Properties

- **Bounded signals and zero error.** Theorem: under matching and the known sign, every solution is bounded and $e(t) \to 0$ for every bounded piecewise continuous $r$ and every $\gamma > 0$.
- **No parameter convergence without excitation.** Theorem: the gains converge to $(k^*, l^*)$ exponentially if the regressor is persistently exciting; otherwise they can stop at any point that gives zero error, as the constant reference shows.
- **Direct.** The law adapts the controller gains, not a plant model. Compare the indirect [self-tuning regulator](/self-tuning-regulator/).
- **No robustness margin.** The proof needs the exact matching structure. With a bounded disturbance the gains can drift without bound, and with unmodeled dynamics the loop can lose stability ([Rohrs counterexample](/rohrs-counterexample/)).
- **Transient.** $V$ bounds the tracking error by $e^T P e \le V(0)$, but $V(0)$ grows with the initial gain error divided by $\gamma$, so the bound says little about the size of the transient for small $\gamma$, and a large $\gamma$ gives oscillatory control signals.

## Variants and improvements

- **Robust modifications.** [Sigma modification](/sigma-modification/), [parameter projection](/parameter-projection/), the $e$-modification and a dead zone keep the gains bounded under disturbances and unmodeled dynamics, at the cost of a residual error.
- **Output feedback MRAC.** When only the output is measured, the controller uses filters of the input and output. For a model of relative degree one with a strictly positive real transfer function, the same Lyapunov argument works through the [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/). Higher relative degree needs an augmented error or [adaptive backstepping](/adaptive-backstepping/).
- **[L1 adaptive control](/l1-adaptive-control/).** Adds a low-pass filter on the control signal and uses a high adaptation gain, to separate the speed of adaptation from robustness.
- **Nonlinear plants.** When the uncertainty is linear in the unknown parameters, the same design applies with a regressor in place of $x$; the [Slotine-Li adaptive controller](/slotine-li-adaptive-control/) is the robot arm case.
- **The MIT rule.** The older gradient law of the [MIT rule](/mit-rule/) has the same form for the first order plant but needs sensitivity filters, and it has no stability proof.

## When to use it

Use MRAC when the plant structure is known, the parameters are constant or slowly varying, the full state is measured and the matching condition holds, for example a flight control loop with unknown aerodynamic coefficients. Add a robust modification in every real application, because measurement noise and unmodeled dynamics break the proof. When the plant changes in a known way with an operating point, [gain scheduling](/gain-scheduling/) is often simpler.

## Pitfalls

- **Wrong sign of $l^*$.** The laws then push the gains away from $k^*$, and the loop can go unstable.
- **No matching.** If $A + b k^T = A_m$ has no solution, the error does not go to zero and the gains can drift.
- **Parameter drift.** A small constant disturbance and a reference that is not persistently exciting can make $k$ grow slowly without bound, until the loop goes unstable.
- **High adaptation gain.** The proof holds for every $\gamma > 0$, but a large $\gamma$ gives a stiff system and high frequency control signals that excite unmodeled dynamics.
- **Error sign.** This page uses $e = x - x_m$. With the opposite sign every law changes sign.

## Implementations

## History

Whitaker, Yamron and Kezer (1958) proposed the model reference scheme with the [MIT rule](/mit-rule/), which has no stability guarantee. Parks (1966) redesigned the law from a Lyapunov function and gave the first model reference adaptive systems with a stability proof (bounded signals and an error that goes to zero) for plants whose state is measured. Around 1980 several groups, among them Morse, Narendra, Lin and Valavani, proved global stability for output feedback MRAC of linear plants of any relative degree. Rohrs and co-authors showed in 1985 that these schemes can lose stability under small unmodeled dynamics, which started the work on robust adaptive control (Ioannou and Sun, Section 1.3 and Chapter 8).

## References
