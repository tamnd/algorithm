---
tag: W1XYZE
kind: algorithm
slug: backstepping
name: Backstepping
aliases:
- integrator backstepping
area: control/nonlinear-control
level: core
summary: Builds a Lyapunov function and a feedback step by step for a system in strict feedback form, treating each state as a virtual control.
model: real-ram
complexity:
  vars: {n: the number of states, q: the number of arithmetic operations to evaluate all f_i and g_i once}
  time: {worst: "O(3^n q)"}
  space: {extra: "O(n 2^n)"}
properties: {deterministic: true, exact: true, recursive: true, online: true}
history:
  year: 1991
  people: [Ioannis Kanellakopoulos, Petar V. Kokotović, A. Stephen Morse, Miroslav Krstić]
  note: "Kanellakopoulos, Kokotović and Morse (1991) made the recursive design systematic for systems in strict feedback form; Kokotović's Bode lecture (1992) and the book of Krstić, Kanellakopoulos and Kokotović (1995) made it a standard tool."
prereqs: [control-lyapunov-function, lyapunov-direct-method, control-affine-system]
see_also: [adaptive-backstepping, sontag-universal-formula, feedback-linearization, input-output-linearization, sliding-mode-control, passivity-based-control, zero-dynamics, high-gain-observer]
sources:
  - book: isbn:9780471127321
    title: Miroslav Krstić, Ioannis Kanellakopoulos and Petar Kokotović, Nonlinear and Adaptive Control Design, Wiley, 1995
    locator: Section 2.2 (Backstepping) with 2.2.1 Integrator backstepping; Section 2.3.1 Strict-feedback systems; Section 2.4.3 Avoiding cancellations; Section 2.5.1 Nonlinear damping
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 14.3, Backstepping
  - book: isbn:9780387984896
    title: Eduardo D. Sontag, Mathematical Control Theory, second edition, Springer, 1998
    locator: Section 5.9, Lemma 5.9.5 (adding an integrator to a stabilizable system, with W = V + |z - k(x)|^2 / 2)
  - paper: doi:10.1109/37.165507
    title: "Petar V. Kokotović, The joy of feedback: nonlinear and adaptive, IEEE Control Systems Magazine 12(3), 7-17, 1992"
    locator: the 1991 Bode Prize Lecture; the backstepping procedure and its adaptive form
  - paper: "I. Kanellakopoulos, P. V. Kokotović and A. S. Morse, Systematic design of adaptive controllers for feedback linearizable systems, IEEE Transactions on Automatic Control 36(11), 1241-1253, 1991"
    title: Systematic design of adaptive controllers for feedback linearizable systems
    locator: the recursive design for systems in parametric strict feedback form
---

Backstepping is a recursive design of a feedback and a [Lyapunov function](/lyapunov-function/) for a nonlinear system in strict feedback form, $\dot x_i = f_i(x_1, \dots, x_i) + g_i(x_1, \dots, x_i)\, x_{i+1}$, where each state drives the next one and the input enters last. Step $i$ treats $x_{i+1}$ as a virtual input, chooses a desired value $\alpha_i$ for it, and adds the square of the error $x_{i+1} - \alpha_i$ to the Lyapunov function. After $n$ steps the real input appears, and the result is a feedback $u = \alpha_n(x)$ with a [control Lyapunov function](/control-lyapunov-function/) $V = \frac12 \sum z_i^2$ whose derivative is $-\sum c_i z_i^2$. Unlike [feedback linearization](/feedback-linearization/), it does not need to cancel every nonlinearity, and it gives the Lyapunov function as part of the result.

## In plain words

Think of a chain of tanks, where the first tank is filled from the second, the second from the third, and you control only the last pump. You cannot set the first level directly. So you first decide what the second level should be to drive the first one to its target, as if you could choose it. Then you decide what the third level should be to drive the second one to that wish, and so on, back along the chain to the pump. At each step you also keep a score of how far each level is from its wish. The method chooses every wish so that the total score always goes down. When the score reaches zero, every level is at its target. The work is in the bookkeeping: each wish depends on how the earlier wishes change.

## The problem

**Input.** A system in strict feedback form

$$\dot x_i = f_i(\bar x_i) + g_i(\bar x_i)\, x_{i+1} \quad (i = 1, \dots, n - 1), \qquad \dot x_n = f_n(\bar x_n) + g_n(\bar x_n)\, u,$$

with $\bar x_i = (x_1, \dots, x_i)$, a scalar input $u$, smooth $f_i, g_i : \mathbb{R}^i \to \mathbb{R}$, $f_i(0) = 0$ and $g_i(\bar x_i) \neq 0$ for every $\bar x_i$. Smoothness makes the closed loop locally Lipschitz, so solutions exist and are unique (see the [Lipschitz condition](/lipschitz-condition/) and the [Picard-Lindelöf theorem](/picard-lindelof-theorem/)). Also gains $c_1, \dots, c_n > 0$.

**Output.** A smooth feedback $u = \alpha_n(x)$ with $\alpha_n(0) = 0$, and new coordinates $z = \Phi(x)$, such that $V = \frac12 |z|^2$ is positive definite and proper and

$$\dot V = -\sum_{i=1}^n c_i z_i^2$$

along the closed loop. Then the origin is globally asymptotically stable. This is a [control-affine system](/control-affine-system/) with a special triangular structure; the structure is what makes the construction possible.

## The algorithm

```pseudo id=main
BACKSTEPPING(f, g, c, x)
L1  α_0 ← 0; z_0 ← 0; g_0 ← 0
L2  for i ← 1 to n
L3      z_i ← x_i - α_{i-1}(x̄_{i-1})
L4      D_i ← Σ_{j<i} ∂α_{i-1}/∂x_j · (f_j(x̄_j) + g_j(x̄_j) x_{j+1})
L5      α_i ← (-c_i z_i - g_{i-1} z_{i-1} - f_i(x̄_i) + D_i) / g_i(x̄_i)
L6  return u = α_n, z = (z_1, ..., z_n)
```

Line L3 is the error between the state $x_i$ and the value $\alpha_{i-1}$ that the previous step wanted for it. Line L4 is the time derivative of $\alpha_{i-1}$ along the system, which can be computed from the state alone, because $\alpha_{i-1}$ depends only on $x_1, \dots, x_{i-1}$ and their derivatives do not involve $u$. Line L5 chooses the virtual input $\alpha_i$ for $x_{i+1}$ so that the error $z_i$ obeys $\dot z_i = -c_i z_i - g_{i-1} z_{i-1} + g_i z_{i+1}$. The term $-g_{i-1} z_{i-1}$ cancels the cross term that step $i - 1$ left in $\dot V$.

Each $\alpha_i$ is a function, and line L4 needs its partial derivatives. A symbolic implementation differentiates formulas. The implementation here evaluates the functions at a point and gets line L4 exactly by forward-mode automatic differentiation: it evaluates $\alpha_{i-1}$ at $x + \varepsilon v$ with $\varepsilon^2 = 0$, where $v_j = f_j + g_j x_{j+1}$, and reads $D_i$ from the coefficient of $\varepsilon$. Each step adds one level of nested dual numbers with its own tag.

## Example

Take $\dot x_1 = x_1^2 + x_2$, $\dot x_2 = u$, with $c_1 = c_2 = 1$. Here $f_1 = x_1^2$, $g_1 = 1$, $f_2 = 0$, $g_2 = 1$. The term $x_1^2$ makes the open loop escape to infinity in finite time from $x_1(0) > 0$ with $x_2 = 0$.

| line | step 1 | step 2 |
|---|---|---|
| L3 | $z_1 = x_1$ | $z_2 = x_2 + x_1 + x_1^2$ |
| L4 | $D_1 = 0$ | $D_2 = -(1 + 2 x_1)(x_1^2 + x_2)$ |
| L5 | $\alpha_1 = -x_1 - x_1^2$ | $\alpha_2 = -z_2 - z_1 - (1 + 2 x_1)(x_1^2 + x_2)$ |

Expanded, the feedback is $u = -2 (x_1 + x_2 + x_1^2 + x_1^3 + x_1 x_2)$. In the new coordinates the closed loop is linear:

$$\dot z = \begin{bmatrix} -1 & 1 \\ -1 & -1 \end{bmatrix} z,$$

so $z(t) = e^{-t} \begin{bmatrix} \cos t & \sin t \\ -\sin t & \cos t \end{bmatrix} z(0)$ and $V(t) = V(0)\, e^{-2t}$ exactly. Start at $x(0) = (1, 0)$, so $z(0) = (1, 2)$, $V(0) = 2.5$ and $u(0) = -6$. A 4th order Runge-Kutta simulation with step $0.01$, with the feedback evaluated inside the right side, gives:

| $t$ | $x_1 = z_1$ | $x_2$ | $z_2$ | $u$ | $V$ |
|---|---|---|---|---|---|
| 0 | 1 | 0 | 2 | -6 | 2.5 |
| 0.5 | 1.11385 | -1.58075 | 0.77378 | -0.78996 | 0.91970 |
| 1 | 0.81789 | -1.39885 | 0.08797 | 1.01803 | 0.33834 |
| 2 | 0.18980 | -0.46152 | -0.23570 | 0.63292 | 0.04579 |
| 3 | -0.03524 | -0.07161 | -0.10560 | 0.20625 | 0.00620 |
| 4 | -0.03969 | 0.02804 | -0.01008 | 0.02252 | 0.00084 |
| 6 | 0.00099 | 0.00446 | 0.00545 | -0.01091 | 0.00002 |

Over the 800 steps to $t = 8$, $V$ differs from $2.5\, e^{-2t}$ by at most $1.7 \cdot 10^{-9}$, which is the error of the integrator, and it decreases at every step. The first state rises at first, from 1 to about 1.11, because the input needs time to pull $x_2$ negative.

## Correctness

The full proof is in proofs/correctness.md. Its main steps:

- **Each $\alpha_i$ is smooth and zero at zero.** By induction: line L5 divides smooth functions by $g_i \neq 0$, and at $x = 0$ every term vanishes because $f_j(0) = 0$.
- **The error dynamics.** The chain rule gives $\frac{d}{dt} \alpha_{i-1} = D_i$, because the derivatives of $x_1, \dots, x_{i-1}$ do not involve $u$. With $x_{i+1} = z_{i+1} + \alpha_i$ and line L5, $\dot z_i = -c_i z_i - g_{i-1} z_{i-1} + g_i z_{i+1}$.
- **The cross terms cancel.** In $\dot V = \sum z_i \dot z_i$, the sums $\sum g_i z_i z_{i+1}$ and $-\sum g_{i-1} z_{i-1} z_i$ are the same sum, so $\dot V = -\sum c_i z_i^2$.
- **Global result.** $x \mapsto z$ is triangular with unit diagonal, so it has a smooth inverse. $V$ is positive definite and proper in $x$, and $\dot V \le -2 \min_i c_i\, V$. [Lyapunov's direct method](/lyapunov-direct-method/) gives global asymptotic stability, and $z$ decays at least like $e^{-\min_i c_i\, t}$.
- **The implementation.** Forward-mode differentiation with dual numbers follows the sum, product, quotient and chain rules, so line L4 is exact with exact data.

The tests check the closed form of the example in exact rationals, the identity $\dot V = -\sum c_i z_i^2$ exactly in Fraction for 36 random polynomial systems with $n = 1, 2, 3$ (with $\dot V$ computed by one more dual direction along the closed loop), the linear gain $u = -(1 + c_1 c_2) x_1 - (c_1 + c_2) x_2$ for the double integrator, that the triple integrator closed loop has the same characteristic polynomial as the error system, the simulation against $V(0) e^{-2t}$ and the rotation formula within $10^{-8}$, and a system with $\sin$ and $\cos$ terms.

## Complexity

Count real operations at unit cost, as in the real RAM. Let $q$ be the number of operations needed to evaluate all $f_i$ and $g_i$ once at a point.

- **The recursion.** Step $i$ evaluates step $i - 1$ once, on numbers with one more level of dual parts. A number with $d$ levels has $2^d$ parts, and one product of such numbers costs $3^d$ products of plain numbers (the rule $(a + b\varepsilon)(c + d\varepsilon) = ac + (ad + bc)\varepsilon$ applied at each level). Step $i$ runs at $n - i$ levels and evaluates at most all the $f_j$ and $g_j$, so the total is $\sum_i O(3^{n-i} q) = O(3^n q)$ operations per evaluation of the feedback.
- **Space.** Each level keeps a state of $n$ numbers with up to $2^d$ parts, so $O(n 2^n)$ in total.
- **Simulation.** A closed-loop RK4 simulation with $N$ steps evaluates the feedback $4 N$ times.

The exponential factor comes from the nested derivatives. A symbolic implementation computes $\alpha_n$ once as a formula, but the formula grows fast with $n$, because each step differentiates the previous virtual control and multiplies by the terms $f_j + g_j x_{j+1}$. This growth is known as the explosion of terms. For small $n$ (the usual case is 2 to 4) either way is cheap.

## Properties

- **Constructive.** The output includes a Lyapunov function, not only a feedback, so the result can be combined with other Lyapunov-based tools: [Sontag's formula](/sontag-universal-formula/) applied to the same $V$, [input-to-state stability](/input-to-state-stability/) arguments or adaptation.
- **Global.** Under the stated hypotheses, the result holds for every initial state, not only near an equilibrium.
- **Exponential in z.** $|z(t)| \le e^{-\min_i c_i\, t} |z(0)|$. In $x$ this gives local exponential stability, because $z = \Phi(x)$ is a diffeomorphism with $\Phi(0) = 0$.
- **Not unique.** Line L5 is one choice. Any $\alpha_i$ that makes $\dot V_i$ negative works, and good choices keep useful nonlinear terms (see the pitfalls).

## Variants and improvements

- **Avoiding cancellations.** Line L5 cancels $f_i$ even when $f_i$ helps. For $\dot x_1 = -x_1^3 + x_2$, the choice $\alpha_1 = -c_1 x_1$ keeps the damping term $-x_1^3$ and uses less input than $\alpha_1 = -c_1 x_1 + x_1^3$ (Krstić, Kanellakopoulos and Kokotović 1995, Section 2.4.3).
- **Nonlinear damping.** If $\dot x_i$ has an unknown bounded term $\varphi_i(\bar x_i)^T \delta(t)$, adding $-\kappa_i |\varphi_i|^2 z_i$ to $\alpha_i$ keeps the state bounded (Section 2.5.1 of the same book; Khalil 2002, Section 14.2.2).
- **Unknown constant parameters.** [Adaptive backstepping](/adaptive-backstepping/) adds an update law for the parameters and tuning functions so that one update law serves all steps.
- **Avoiding the derivatives.** Dynamic surface control and command-filtered backstepping pass each $\alpha_i$ through a first order filter and use the filter state and its derivative instead of $D_i$. This removes the explosion of terms at the cost of an error that the analysis must bound.
- **Several inputs and block structure.** The same steps work when each $x_i$ is a vector and $g_i$ is an invertible matrix (block backstepping).
- **Output feedback.** When only $x_1$ is measured, an observer replaces the unmeasured states. The [high-gain observer](/high-gain-observer/) and observer backstepping are the usual routes.

## When to use it

Use it when the system is in strict feedback form, or can be brought to it by a change of coordinates, and when you want a global result with a Lyapunov function, for example to add adaptation or to prove robustness. It suits mechanical and electromechanical systems where a force drives a velocity that drives a position. Prefer [input-output linearization](/input-output-linearization/) when the system is not triangular but has a well defined relative degree and stable [zero dynamics](/zero-dynamics/). Prefer [sliding mode control](/sliding-mode-control/) when the model has large matched uncertainty. When the input is limited, the global result does not survive saturation, and a design that takes the limit into account, such as [model predictive control](/model-predictive-control/), is often better.

## Pitfalls

- **Division by a small g_i at line L5.** The design needs $g_i \neq 0$ everywhere. If $g_i$ is small somewhere, $\alpha_i$ is large there, and so are all later virtual controls and the input. If $g_i$ vanishes somewhere, the result is only local, on a region that avoids the zero set.
- **Finite differences at line L4.** Each $D_i$ differentiates $\alpha_{i-1}$, which already contains derivatives of $\alpha_{i-2}$. Difference quotients nest, and the rounding error grows by about the inverse of the step size at each level. Differentiate exactly, symbolically or with automatic differentiation as here.
- **Cancelling a useful term at line L5.** The term $-f_i$ in line L5 removes stabilizing nonlinearities too, and the input then grows like the cancelled term. In the example, $u$ contains $-2 x_1^3$ because line L5 cancels the destabilizing $x_1^2$; for a helpful term such as $-x_1^3$ the cancellation is a waste.
- **Large inputs.** The feedback is polynomial of high degree when the $f_i$ are. In the example, $u(0) = -6$ for a unit initial state, and $u$ grows like $x_1^3$. With input limits the global guarantee is lost.
- **Sampled implementation.** The proof assumes that line L6 is evaluated continuously. With a computer, the input is held between samples, and $\dot V = -\sum c_i z_i^2$ holds only approximately.

## Implementations

## History

The step that adds one integrator to a system with a known stabilizing feedback and Lyapunov function, with the new function $V + \frac12 (x_{n+1} - \alpha(x))^2$, appears in the nonlinear stabilization literature of the late 1980s; Sontag's book states it as a lemma (Section 5.9). Kanellakopoulos, Kokotović and Morse (1991) turned the repeated use of this step into a systematic procedure for systems in strict feedback form with unknown parameters. Kokotović's 1991 Bode Prize Lecture, published in 1992 as "The joy of feedback", explained the procedure and its name, and the 1995 book of Krstić, Kanellakopoulos and Kokotović gave the full theory, including tuning functions and the methods that avoid useless cancellations.

## References
