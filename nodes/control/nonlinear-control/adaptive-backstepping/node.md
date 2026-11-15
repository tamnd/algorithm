---
tag: 5JZM0E
kind: algorithm
slug: adaptive-backstepping
name: Adaptive backstepping
aliases:
- adaptive integrator backstepping
area: control/nonlinear-control
level: advanced
summary: Backstepping with unknown parameters, with tuning functions that give one adaptation law for all steps.
model: real-ram
complexity:
  vars: {n: the number of states, p: the number of unknown parameters, q: the number of arithmetic operations to evaluate all phi_i and beta once}
  time: {worst: "O((3(n + p))^n (q + n p + p^2))"}
  space: {extra: "O((n^2 + n p) 2^n)"}
properties: {deterministic: true, exact: true, recursive: true, online: true}
history:
  year: 1992
  people: [Miroslav Krstić, Ioannis Kanellakopoulos, Petar V. Kokotović, A. Stephen Morse]
  note: "Kanellakopoulos, Kokotović and Morse (1991) gave the first global adaptive design for parametric strict feedback systems, with several estimates of each parameter; Krstić, Kanellakopoulos and Kokotović (1992) removed the extra estimates with tuning functions."
prereqs: [backstepping, lyapunov-direct-method, barbalat-lemma]
see_also: [adaptive-control, model-reference-adaptive-control, certainty-equivalence, persistent-excitation, parameter-projection, control-lyapunov-function, lasalle-invariance-principle, sliding-mode-control]
sources:
  - book: isbn:9780471127321
    title: Miroslav Krstić, Ioannis Kanellakopoulos and Petar Kokotović, Nonlinear and Adaptive Control Design, Wiley, 1995
    locator: Chapter 4 (tuning functions design), Section 4.2 (parametric strict feedback systems)
  - paper: "M. Krstić, I. Kanellakopoulos and P. V. Kokotović, Adaptive nonlinear control without overparametrization, Systems and Control Letters 19(3), 177-185, 1992"
    title: Adaptive nonlinear control without overparametrization
    locator: the tuning functions design, with one estimate of each parameter
  - paper: "I. Kanellakopoulos, P. V. Kokotović and A. S. Morse, Systematic design of adaptive controllers for feedback linearizable systems, IEEE Transactions on Automatic Control 36(11), 1241-1253, 1991"
    title: Systematic design of adaptive controllers for feedback linearizable systems
    locator: the first recursive adaptive design for parametric strict feedback systems, with overparametrization
  - paper: doi:10.1109/37.165507
    title: "Petar V. Kokotović, The joy of feedback: nonlinear and adaptive, IEEE Control Systems Magazine 12(3), 7-17, 1992"
    locator: the 1991 Bode Prize Lecture; adaptive backstepping
---

Adaptive backstepping is a recursive design of a feedback and a parameter update law for a nonlinear system in parametric strict feedback form, $\dot x_i = x_{i+1} + \varphi_i(x_1, \dots, x_i)^T \theta$, where $\theta$ is a constant vector of unknown parameters. It follows the steps of [backstepping](/backstepping/), with an estimate $\hat\theta$ in place of $\theta$. The difficulty is that each virtual control depends on $\hat\theta$, so its time derivative contains $\dot{\hat\theta}$, which is not known until the last step. The tuning functions design collects one term $\tau_i$ per step and uses the final $\tau_n$ in one update law $\dot{\hat\theta} = \Gamma \tau_n$. The result is one estimate per parameter and a Lyapunov function with $\dot V = -\sum c_i z_i^2$. The state goes to zero for every initial state, but the estimate need not reach $\theta$.

## In plain words

Backstepping works back along a chain of states and chooses, step by step, what each state should be. Here some numbers in the model are unknown. The controller uses a guess for them and corrects the guess while it runs. Each step depends on the guess, so each step must know how fast the guess changes. That speed is known only at the end, because every step contributes to it. The tuning functions are the parts that each step adds to that speed, and the method plans for the final speed from the start. One correction law then serves all steps. A score made of the tracking errors and the guess error never goes up. So the state goes to zero. The guess stays bounded, but it can settle at a wrong value, because the controller only needs a guess that works.

## The problem

**Input.** A system in parametric strict feedback form

$$\dot x_i = x_{i+1} + \varphi_i(\bar x_i)^T \theta \quad (i = 1, \dots, n - 1), \qquad \dot x_n = \beta(x)\, u + \varphi_n(x)^T \theta,$$

with $\bar x_i = (x_1, \dots, x_i)$, a scalar input $u$, an unknown constant $\theta \in \mathbb{R}^p$, smooth known $\varphi_i : \mathbb{R}^i \to \mathbb{R}^p$ with $\varphi_i(0) = 0$, and a smooth known $\beta$ with $\beta(x) \neq 0$ everywhere. The closed loop is then locally Lipschitz, so solutions exist and are unique (see the [Lipschitz condition](/lipschitz-condition/) and the [Picard-Lindelöf theorem](/picard-lindelof-theorem/)). Also gains $c_1, \dots, c_n > 0$ and an adaptation gain $\Gamma$, a symmetric positive definite $p \times p$ matrix.

**Output.** A feedback $u(x, \hat\theta)$ and an update law $\dot{\hat\theta} = \Gamma \tau_n(x, \hat\theta)$, with error coordinates $z = (z_1, \dots, z_n)$, such that

$$V = \frac12 |z|^2 + \frac12 (\theta - \hat\theta)^T \Gamma^{-1} (\theta - \hat\theta)$$

satisfies $\dot V = -\sum_{i=1}^n c_i z_i^2$ along the closed loop. Then all signals are bounded and $x(t) \to 0$ for every $x(0)$ and $\hat\theta(0)$. This is a statement about regulation, not about the equilibrium $(x, \hat\theta) = (0, \theta)$, which is in general not asymptotically stable.

## The algorithm

```pseudo id=main
ADAPTIVE-BACKSTEPPING(φ, β, c, Γ, x, θ̂)
L1  α_0 ← 0; z_0 ← 0; τ_0 ← 0
L2  for i ← 1 to n
L3      z_i ← x_i - α_{i-1}(x̄_{i-1}, θ̂)
L4      w_i ← φ_i(x̄_i) - Σ_{k<i} ∂α_{i-1}/∂x_k · φ_k(x̄_k)
L5      τ_i ← τ_{i-1} + w_i z_i
L6      α_i ← -z_{i-1} - c_i z_i - w_iᵀθ̂ + Σ_{k<i} ∂α_{i-1}/∂x_k · x_{k+1} + ∂α_{i-1}/∂θ̂ · Γ τ_i + Σ_{k=2}^{i-1} z_k · ∂α_{k-1}/∂θ̂ · Γ w_i
L7  return u = α_n / β(x), θ̂' = Γ τ_n, z = (z_1, ..., z_n)
```

Line L3 is the error between $x_i$ and the value that the previous step wanted for it. Line L4 is the regressor of $z_i$: the unknown part of $\dot z_i$ is $w_i^T \theta$, because $\theta$ enters $\dot z_i$ through $\dot x_i$ and through the time derivative of $\alpha_{i-1}$. Line L5 is the tuning function. It is the update law that would be right if the design stopped at step $i$. Line L6 has four parts:

- The terms $-z_{i-1} - c_i z_i$ are those of backstepping.
- $-w_i^T \hat\theta$ is the certainty equivalence term: it cancels $w_i^T \theta$ with the estimate in place of $\theta$.
- The sum over $x_{k+1}$ is the known part of the time derivative of $\alpha_{i-1}$.
- The two terms with $\partial \alpha / \partial \hat\theta$ handle the derivative of $\alpha_{i-1}$ with respect to the estimate. The first uses $\tau_i$ as a stand-in for the final $\tau_n$. The second makes the error of this stand-in skew-symmetric, so that it cancels in $\dot V$. This second sum is empty when $n \le 2$.

Line L7 divides by $\beta$ and gives the update law.

The partial derivatives in lines L4 and L6 are of functions, not of numbers. The implementation evaluates every function at a point and gets the partial derivatives exactly by forward-mode automatic differentiation. Step $i$ evaluates step $i - 1$ once more for each of the $i - 1 + p$ variables $x_1, \dots, x_{i-1}, \hat\theta_1, \dots, \hat\theta_p$, with that variable replaced by $x_k + \varepsilon$ or $\hat\theta_l + \varepsilon$, $\varepsilon^2 = 0$, and reads each partial derivative from the coefficient of $\varepsilon$. Each step adds one level of nested dual numbers with its own tag.

## Example

Take $\dot x_1 = x_2 + \theta x_1^2$, $\dot x_2 = u$, with true $\theta = 1$, unknown to the controller, so $n = 2$, $p = 1$, $\varphi_1 = x_1^2$, $\varphi_2 = 0$, $\beta = 1$. Use $c_1 = c_2 = 1$ and $\Gamma = 1$. With $\theta$ known, this is the example of [backstepping](/backstepping/).

| line | step 1 | step 2 |
|---|---|---|
| L3 | $z_1 = x_1$ | $z_2 = x_2 + c_1 x_1 + \hat\theta x_1^2$ |
| L4 | $w_1 = x_1^2$ | $w_2 = (c_1 + 2 \hat\theta x_1)\, x_1^2$ |
| L5 | $\tau_1 = x_1^3$ | $\tau_2 = x_1^3 + w_2 z_2$ |
| L6 | $\alpha_1 = -c_1 x_1 - \hat\theta x_1^2$ | $\alpha_2 = -z_1 - c_2 z_2 - w_2 \hat\theta - (c_1 + 2 \hat\theta x_1)\, x_2 - x_1^2\, \Gamma \tau_2$ |

So $u = \alpha_2$ and $\dot{\hat\theta} = \Gamma \tau_2$. Start at $x(0) = (1, 0)$ and $\hat\theta(0) = 0$. Then $z(0) = (1, 1)$, $\tau_2 = 2$, $u(0) = -1 - 1 - 0 - 0 - 2 = -4$, $\dot{\hat\theta}(0) = 2$ and $V(0) = \frac12 (1 + 1 + 1) = 1.5$. A 4th order Runge-Kutta simulation of the state $(x_1, x_2, \hat\theta)$ with step $0.01$, with the controller evaluated inside the right side, gives:

| $t$ | $x_1 = z_1$ | $x_2$ | $\hat\theta$ | $z_2$ | $u$ | $V$ |
|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 1 | -4 | 1.5 |
| 0.5 | 0.92282 | -2.22663 | 1.64547 | 0.09745 | 1.35718 | 0.63886 |
| 1 | 0.32603 | -0.98258 | 1.64337 | -0.48186 | 1.83703 | 0.37621 |
| 2 | -0.09364 | -0.11940 | 1.63368 | -0.19871 | 0.36530 | 0.22490 |
| 3 | -0.08494 | 0.06198 | 1.63190 | -0.01118 | 0.04281 | 0.20332 |
| 4 | -0.02153 | 0.04477 | 1.63173 | 0.02400 | -0.04481 | 0.20006 |
| 6 | 0.00415 | -0.00287 | 1.63173 | 0.00130 | -0.00257 | 0.19955 |
| 10 | -0.00007 | 0.00011 | 1.63173 | 0.00004 | -0.00008 | 0.19954 |

$V$ decreases at every one of the 1000 steps (measurement). The state goes to zero, but the estimate settles at about $1.63173$, not at $\theta = 1$. The limit of $V$ is $\frac12 (1 - 1.63173)^2 = 0.19954$, all of it from the parameter error. Once $x$ is near zero, $\tau_2 \approx 0$ and the estimate stops moving, because a state at rest carries no information about $\theta$.

## Correctness

The full proof is in proofs/correctness.md. Its main steps:

- **Smoothness.** By induction, each $\alpha_i$ is a smooth function of $(\bar x_i, \hat\theta)$ with $\alpha_i(0, \hat\theta) = 0$, because $\varphi_i(0) = 0$.
- **The error dynamics.** The time derivative of $\alpha_{i-1}$ contains $\frac{\partial \alpha_{i-1}}{\partial \hat\theta} \Gamma \tau_n$. Line L6 used $\tau_i$, and the difference is $\tau_n - \tau_i = \sum_{j > i} w_j z_j$. This gives $\dot z_i = -c_i z_i + z_{i+1} - z_{i-1} + w_i^T \tilde\theta - \sum_{j > i} \sigma_{ij} z_j + \sum_{1 < k < i} \sigma_{ki} z_k$ with $\sigma_{ij} = \frac{\partial \alpha_{i-1}}{\partial \hat\theta} \Gamma w_j$ and $\tilde\theta = \theta - \hat\theta$.
- **Cancellation.** In $\sum z_i \dot z_i$, the terms $z_i z_{i+1}$ cancel as in backstepping, and the $\sigma$ terms cancel because the last sum of line L6 is the mirror image of the error of using $\tau_i$. What remains is $-\sum c_i z_i^2 + \tilde\theta^T \tau_n$. The update law gives $\frac{d}{dt} \frac12 \tilde\theta^T \Gamma^{-1} \tilde\theta = -\tilde\theta^T \tau_n$. So $\dot V = -\sum c_i z_i^2$.
- **Regulation.** $V$ is nonincreasing, so $z$ and $\hat\theta$ are bounded, and so is $x$ (it is a continuous function of $z$ and $\hat\theta$). Then $\dot z$ is bounded and $\int_0^\infty \sum c_i z_i^2\, dt \le V(0)$, so [Barbalat's lemma](/barbalat-lemma/) gives $z \to 0$, and then $x \to 0$.
- **The implementation.** Dual numbers follow the sum, product and quotient rules, so lines L4 and L6 are exact with exact data.

The tests check the values at $x = (1, 0)$, $\hat\theta = 0$ ($u = -4$, $\dot{\hat\theta} = 2$, $z = (1, 1)$), the closed form of the example at 20 random rational points with random gains, the case $n = 1$ with $p = 2$ and a non-diagonal $\Gamma$, and the identity $\dot V = -\sum c_i z_i^2$ exactly in Fraction for 24 random polynomial systems with $n = 1, 2, 3$ and $p = 1, 2$, a non-diagonal $\Gamma$ and $\beta = 1 + x_1^2$. There, $\dot V$ is computed with one more dual direction along the closed-loop vector field, so the check does not use the error equations of the proof. A simulation test checks that $V$ is nonincreasing, that $x(10)$ is within $10^{-3}$ of zero, the limit of $\hat\theta$, and one row of the table.

## Complexity

Count real operations at unit cost, as in the real RAM. Let $q$ be the number of operations to evaluate all $\varphi_i$ and $\beta$ once.

- **The recursion tree.** A call of step $i \ge 2$ calls step $i - 1$ once with plain inputs and $i - 1 + p$ times with one new dual direction. So step $i$ is called at most $\prod_{j > i} (j + p) \le (n + p)^{n - i}$ times.
- **The cost of a call.** A call of step $i$ works on numbers with at most $n - i$ levels of dual parts, and one product at $d$ levels costs $3^d$ plain products. Without its recursive calls, it does $O(q + n p + p^2)$ operations on such numbers.
- **Total.** $\sum_i (3(n + p))^{n - i}\, O(q + n p + p^2) = O((3(n + p))^n (q + n p + p^2))$ per evaluation of the controller.
- **Space.** The recursion is $n$ calls deep, and the call of step $i$ keeps $O(i^2 + i p)$ numbers with $2^{n - i}$ parts, so $O((n^2 + n p) 2^n)$ in total.

The bound is exponential in $n$, like the size of the symbolic formulas, which grow with each differentiation (the explosion of terms). The usual cases have $n$ from 2 to 4, and then the cost is small. For the example, the 1000-step simulation runs in well under a second in Python.

## Properties

- **One estimate per parameter.** The update law has $p$ states. The earlier overparametrized design used one estimate of $\theta$ per step, $n p$ states in total.
- **Global.** The result holds for every initial state and estimate.
- **Regulation without identification.** $x \to 0$ always. $\hat\theta \to \theta$ only if the regressor is rich enough along the solution ([persistent excitation](/persistent-excitation/)), which a regulated state is not.
- **Certainty equivalence with corrections.** The controller is not the known-parameter controller with $\theta$ replaced by $\hat\theta$. The terms with $\partial \alpha / \partial \hat\theta$ are extra, and without them the proof fails (compare [certainty equivalence](/certainty-equivalence/)).
- **Lyapunov based.** The design gives the Lyapunov function, so it can be extended with damping terms and robust modifications.

## Variants and improvements

- **Overparametrized design.** Kanellakopoulos, Kokotović and Morse (1991) used a new estimate of $\theta$ in each step, with its own update law. It is simpler to derive, but it has $n p$ estimates.
- **Modular design.** Instead of a Lyapunov update law, one can combine a controller that makes the system input-to-state stable with respect to the parameter error and its derivative, and any identifier with bounded outputs. The book of Krstić, Kanellakopoulos and Kokotović (1995) treats this as the modular approach.
- **Robust modifications.** With disturbances, the update law of line L7 is changed with [parameter projection](/parameter-projection/) or a leakage term so that $\hat\theta$ stays bounded.
- **Output feedback.** When only $x_1$ is measured, adaptive observer backstepping uses filters of the input and output in place of the unmeasured states.
- **Command-filtered and dynamic surface versions.** They replace the analytic derivatives of the virtual controls by filter outputs, to avoid the growth of the formulas.
- **Linear plants.** For linear systems with unknown coefficients, [model reference adaptive control](/model-reference-adaptive-control/) is the classical alternative.

## When to use it

Use it when the model has the parametric strict feedback structure with constant unknown parameters that enter linearly, when you need a global result, and when you can compute the partial derivatives of the virtual controls. Typical cases are mechanical and electromechanical systems with unknown friction or load coefficients that enter in the same equation as a nonlinearity. If the parameters vary in time or the model has unknown disturbances, add the robust modifications or use a robust method such as [sliding mode control](/sliding-mode-control/). If you need the true parameter values, add excitation to the reference signal or identify the parameters separately; the controller alone does not give them.

## Pitfalls

- **Expecting the estimate to converge at line L7.** In the example, $\hat\theta$ settles at about $1.632$ while $\theta = 1$ (measurement). With $\Gamma = 0.1$ and $\Gamma = 10$, the limits are about $1.302$ and $1.444$ (measurement, step $0.005$). The limit depends on the gain and the initial state. Do not use $\hat\theta$ as a parameter estimate without persistent excitation.
- **A large adaptation gain at line L6.** $\Gamma$ appears in line L6 multiplied by the partial derivatives of the virtual controls. In the example, the peak of $|u|$ is about $6.9$ with $\Gamma = 1$ and $57.7$ with $\Gamma = 10$ (measurement, step $0.005$). A small gain is not free either: with $\Gamma = 0.1$ the peak of $|u|$ is $12.6$ and $x_1$ rises to $1.97$, because the estimate learns slowly (measurement).
- **Dropping the last sum at line L6.** For $n \ge 3$, without the terms $z_k \frac{\partial \alpha_{k-1}}{\partial \hat\theta} \Gamma w_i$, the $\sigma$ terms in $\dot V$ do not cancel in general, and the proof no longer applies. The sum is empty for $n \le 2$, so a design checked only on second order examples does not show the error.
- **Parameter drift at line L7.** The update law integrates $\tau_n$. With a bounded disturbance or unmodeled dynamics, $V$ need not decrease, and $\hat\theta$ can grow without bound while $x$ stays small. This is a known property of integral update laws in adaptive control (rule of thumb from that field). Projection or leakage prevents it.
- **Finite differences at lines L4 and L6.** Each virtual control contains the partial derivatives of the previous one. Nested difference quotients lose about the inverse of the step size in accuracy at each level. Differentiate exactly, as here.
- **Sampled implementation.** The proof assumes that line L7 is evaluated continuously. With a sampled controller, $\dot V = -\sum c_i z_i^2$ holds only approximately.

## Implementations

## History

The first adaptive controllers for nonlinear systems used certainty equivalence and needed growth conditions on the nonlinearities. Kanellakopoulos, Kokotović and Morse (1991) gave a recursive design that is global for every system in parametric strict feedback form, at the price of several estimates of each parameter. Krstić, Kanellakopoulos and Kokotović (1992) introduced the tuning functions, which give one estimate per parameter; the paper is titled "Adaptive nonlinear control without overparametrization". Kokotović's 1991 Bode Prize Lecture, published in 1992, presented the adaptive design as a main use of backstepping, and the 1995 book of Krstić, Kanellakopoulos and Kokotović gave the full theory, including the modular and output feedback designs.

## References
