---
tag: B6VAKD
kind: algorithm
slug: mit-rule
name: MIT rule
aliases:
- gradient adaptation rule
area: control/robust-and-adaptive-control
level: core
summary: Adjusts a controller parameter along the negative gradient of the squared model following error, the first model reference adaptation law.
model: real-ram
complexity:
  vars: {N: the number of integration steps, n: the order of the plant and of the model, d: the number of adapted parameters}
  time: {worst: O(N (n^2 + d))}
  space: {extra: O(n + d)}
properties: {deterministic: true, exact: false, recursive: false, online: true}
history:
  year: 1958
  people: [H. Philip Whitaker, Joseph Yamron, Allen Kezer]
  note: "Whitaker, Yamron and Kezer at the MIT Instrumentation Laboratory proposed model reference adaptive control with a gradient adjustment of the gains for aircraft flight control; the law became known as the MIT rule."
prereqs: [adaptive-control, feedback-control-loop, transfer-function, gradient-descent]
see_also: [model-reference-adaptive-control, rohrs-counterexample, routh-hurwitz-criterion, persistent-excitation, lms-algorithm, lyapunov-direct-method, averaging-method, extremum-seeking-control]
sources:
  - book: isbn:9780486462783
    title: "Karl Johan Åström and Björn Wittenmark, Adaptive Control, second edition, Addison-Wesley 1995 (Dover reprint 2008)"
    locator: "Chapter 5, Model-reference adaptive systems: Section 5.2 (the MIT rule, the feedforward gain and first order examples) and Section 5.3 (the choice of the adaptation gain and the instability for large gains)"
  - paper: doi:10.1109/TAC.1966.1098361
    title: "P. C. Parks, Liapunov redesign of model reference adaptive control systems, IEEE Transactions on Automatic Control 11(3), 1966"
    locator: "pages 362 to 367 (the instability of the MIT rule and the Lyapunov redesign of the adaptive law)"
  - paper: "H. P. Whitaker, J. Yamron and A. Kezer, Design of model-reference adaptive control systems for aircraft, Report R-164, Instrumentation Laboratory, MIT, 1958"
    locator: "the whole report (the model reference scheme and the gradient adjustment of the gains)"
  - book: isbn:9780486498171
    title: "Petros A. Ioannou and Jing Sun, Robust Adaptive Control, Prentice Hall 1996 (Dover reprint 2012)"
    locator: "Section 1.3, A brief history (the MIT rule and the instability results of the 1960s)"
---

The MIT rule is the first adaptation law of [model reference adaptive control](/model-reference-adaptive-control/): it changes each adjustable controller parameter $\theta$ at a rate proportional to $-e\,\partial e/\partial\theta$, where $e = y - y_m$ is the error between the plant output and the output of a reference model. It is [gradient descent](/gradient-descent/) in continuous time on the instantaneous cost $e^2/2$, with the gradient computed from approximate sensitivity signals. The rule is simple and often works for small adaptation gains, but it has no stability guarantee: for a large gain or a large command signal the parameters can oscillate with growing amplitude (Parks 1966). The Lyapunov design on the [MRAC](/model-reference-adaptive-control/) page replaced it for this reason.

## In plain words

You have a controller with a knob, and a model that shows how the controlled system should respond. You run the real system and the model side by side and watch the difference between their outputs. The rule turns the knob a little in the direction that makes the squared difference smaller. To know that direction, it needs to know how the output would change if the knob moved; it estimates this with a filter driven by the signals it can measure. The speed of the turning is set by a gain. A small gain gives slow, smooth learning. A large gain, or a large command signal, makes the knob overshoot, and the knob and the output can then swing with larger and larger amplitude. Nothing in the rule itself prevents this.

## The problem

The plant has a known structure and unknown constant parameters. A controller with adjustable parameters $\theta \in \mathbb{R}^d$ acts on the plant. A reference model, a BIBO stable [transfer function](/transfer-function/) $G_m(s)$, gives the wanted response $y_m = G_m u_c$ to the command signal $u_c(t)$. The aim is to find $\theta$ so that $e(t) = y(t) - y_m(t)$ goes to zero. For each fixed $\theta$ the closed loop gives an output $y(t, \theta)$, and the cost is $J(\theta) = e^2/2$.

Two standard cases are used on this page.

- **Feedforward gain.** The plant is $k\,G(s)$ with $G$ known and BIBO stable and the gain $k > 0$ unknown. The model is $k_0 G(s)$. The controller is $u = \theta u_c$, and the ideal value is $\theta^* = k_0/k$.
- **First order plant.** The plant is $\dot y = -a y + b u$ with $b > 0$, the model is $\dot y_m = -a_m y_m + b_m u_c$ with $a_m > 0$, and the controller is $u = \theta_1 u_c - \theta_2 y$. The closed loop is $\dot y = -(a + b\theta_2) y + b\theta_1 u_c$, so the ideal values are $\theta_1^* = b_m/b$ and $\theta_2^* = (a_m - a)/b$.

## The algorithm

For a slowly changing $\theta$, the gradient of $J$ is $e\,\partial e/\partial\theta = e\,\partial y/\partial\theta$. The MIT rule sets

$$\dot\theta = -\gamma\, \psi\, e,$$

where $\gamma > 0$ is the adaptation gain and $\psi$ is a signal that approximates the sensitivity derivative $\partial e/\partial\theta$. Known positive constants in $\psi$ are absorbed into $\gamma$; this needs the sign of the plant gain.

- Feedforward gain: $y = k G(p)\,\theta u_c$ for a constant $\theta$, where $p = d/dt$. So $\partial e/\partial\theta = k G u_c = (k/k_0)\, y_m$, and with $k/k_0 > 0$ absorbed, $\dot\theta = -\gamma\, y_m e$. Here the sensitivity is exact and needs no filter.
- First order plant: the exact sensitivities are $\partial e/\partial\theta_1 = \frac{b}{p + a + b\theta_2} u_c$ and $\partial e/\partial\theta_2 = -\frac{b}{p + a + b\theta_2} y$. They contain the unknown plant. Near the ideal parameters $p + a + b\theta_2 = p + a_m$, so the rule uses the model pole: $\dot\theta_1 = -\gamma \big(\frac{a_m}{p + a_m} u_c\big) e$ and $\dot\theta_2 = \gamma \big(\frac{a_m}{p + a_m} y\big) e$, with $b/a_m > 0$ absorbed into $\gamma$.

The plant, the model, the sensitivity filters and $\theta$ form one system of differential equations. The implementation integrates it with the classical fourth order Runge-Kutta method and a fixed step $dt$.

```pseudo id=main
MIT-RULE(γ, θ₀, dt, N)                           ▷ γ > 0, N steps of length dt
L1  θ ← θ₀; set the plant, model and filter states
L2  for i ← 0 to N - 1 do
L3      r ← u_c(t)                                ▷ the command signal at t = i dt
L4      e ← y - y_m                               ▷ model following error
L5      ψ ← sensitivity filter outputs            ▷ ψ ≈ ∂e/∂θ
L6      u ← controller output with the current θ
L7      θ' ← -γ ψ e                               ▷ negative gradient of e²/2
L8      advance plant, model, filters and θ by one RK4 step of length dt
L9  return θ
```

Lines L3 to L7 are the right-hand side of the differential equation; RK4 evaluates them four times per step in line L8.

## Example

**Feedforward gain.** Take $G(s) = 1/(s^2 + s + 1)$, the plant gain $k = 1$, the model gain $k_0 = 2$ and a constant command $u_c = u_0 = 1$. Start with $\theta(0) = 1$, the plant at rest at $y = \theta(0) u_0 = 1$ and the model at rest at $y_m = 2$. The ideal value is $\theta^* = 2$. With RK4 and $dt = 0.02$ s:

| $\gamma$ | $\theta(10)$ | $\theta(20)$ | $\theta(30)$ | $\theta(60)$ |
|---|---|---|---|---|
| 0.25 | 2.0486 | 1.9996 | 1.9986 | 2.0000 |
| 1 | -3.35 | -37.25 | -209.3 | about $2 \times 10^4$ |

The section Correctness shows why. With $y_m$ at rest, $\theta$ obeys exactly the linear equation $\dddot\theta + \ddot\theta + \dot\theta + 2\gamma u_0^2 \theta = 4\gamma u_0^2$. For $\gamma = 0.25$ the characteristic polynomial is $s^3 + s^2 + s + 0.5$, with roots $-0.6478$ and $-0.1761 \pm 0.8607j$, so $\theta \to 2$. For $\gamma = 1$ it is $s^3 + s^2 + s + 2$, with roots $-1.3532$ and $0.1766 \pm 1.2028j$, so $\theta$ oscillates with growing amplitude at about $1.2$ rad/s. By the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/) the limit is $\gamma u_0^2 < 1/2$. The gain $\gamma = 0.25$ with the larger command $u_0 = 2$ gives $\gamma u_0^2 = 1$, and the loop is again unstable: the amplitude of the command matters as much as the gain.

**First order plant.** Take $a = 1$, $b = 0.5$ and $a_m = b_m = 2$, so $\theta_1^* = 4$ and $\theta_2^* = 2$. The command is a square wave of amplitude 1 and period 20 s, and $\theta(0) = (0, 0)$. With $dt = 0.01$ s, at $t = 100$ s:

| $\gamma$ | $\theta_1(100)$ | $\theta_2(100)$ |
|---|---|---|
| 1 | 3.248 | 1.248 |
| 2 | 3.680 | 1.680 |
| 5 | 3.974 | 1.974 |

The error $e$ is below 0.03 at the end of each run, but the parameters are still far from their ideal values for $\gamma = 1$. In every run $\theta_1 - \theta_2 \approx 2$ after the first seconds. While the command is constant, the output only fixes the static gain $b\theta_1/(a + b\theta_2) = b_m/a_m = 1$, which is the line $\theta_1 - \theta_2 = 2$. Only the short transients after each switch of the square wave carry information along the line. This is a weak form of [persistent excitation](/persistent-excitation/).

## Correctness

The MIT rule is a heuristic, and the proof in [proofs/correctness.md](proofs/correctness.md) shows what it does and does not give. It proves three facts. First, with $\theta$ frozen, $-\gamma\,\psi\,e$ is exactly $-\gamma$ times the gradient of $e^2/2$ when $\psi$ is the exact sensitivity, so the rule is gradient descent on the instantaneous squared error. Second, the ideal parameter is an equilibrium of the adaptive loop: there $e \to 0$ and $\dot\theta \to 0$. Third, for the feedforward gain with $G(s) = 1/(s^2 + a_1 s + a_2)$ and a constant command, the parameter obeys a linear third order equation, and the adaptive loop converges if and only if $\gamma k k_0 u_0^2 < a_1 a_2^2$ (a theorem, proved there with Routh-Hurwitz). The last fact shows that no gain $\gamma > 0$ is safe for all command amplitudes. There is no general convergence theorem for the MIT rule; the design with a stability proof is the Lyapunov rule of [MRAC](/model-reference-adaptive-control/) (Parks 1966).

## Complexity

The cost is that of a fixed step simulation, in the real-RAM model. Each RK4 step evaluates the right-hand side four times. One evaluation costs $O(n^2)$ for the plant and the model in state space with dense matrices of order $n$, and $O(d)$ for $d$ parameters with first order sensitivity filters. So $N$ steps cost $O(N(n^2 + d))$ operations, and the memory is $O(n + d)$ besides the output samples. In a real controller the rule runs once per sampling period, so the cost per sample is $O(n^2 + d)$.

## Properties

- **No stability guarantee.** Theorem in the example class above: the loop is asymptotically stable for $\gamma k k_0 u_0^2 < a_1 a_2^2$ and unstable above. In general the rule can make the closed loop unstable for large $\gamma$ or a large command (Parks 1966; Åström and Wittenmark, Section 5.3).
- **Scale dependence.** The update is proportional to $\psi e$, which is quadratic in the signal level. A normalized version $\dot\theta = -\gamma\,\psi e/(\alpha + \psi^T\psi)$ with $\alpha > 0$ removes this dependence (Åström and Wittenmark, Chapter 5).
- **Sign of the gain.** The rule needs the sign of the plant gain, because it absorbs $k/k_0$ or $b/a_m$ into $\gamma$. With the wrong sign it pushes $\theta$ away from $\theta^*$.
- **Parameter convergence.** $e \to 0$ does not imply $\theta \to \theta^*$. The parameters converge only if the command excites the loop enough; the first order example shows the drift along a line.
- **Approximate sensitivities.** The sensitivity filters use the model in place of the unknown plant. Far from $\theta^*$ they can have the wrong phase, and then the update is not a descent direction.

## Variants and improvements

- **Normalized MIT rule.** Divide by $\alpha + \psi^T\psi$, as above. This bounds the update for large signals but still gives no proof of stability.
- **Lyapunov redesign.** Parks (1966) chose the adaptation law so that a [Lyapunov function](/lyapunov-function/) of the error and the parameter error decreases. For the first order plant this gives $\dot\theta_1 = -\gamma u_c e$ and $\dot\theta_2 = \gamma y e$, the same form without the sensitivity filters, with bounded signals and $e \to 0$ for every bounded command. See [MRAC](/model-reference-adaptive-control/).
- **Sign-sign and sign-error versions.** Use the signs of $\psi$ and $e$, or of $e$ only. They are cheap to build, and they are also gradient-like heuristics with no general guarantee.
- **Discrete time.** The update $\theta_{k+1} = \theta_k - \gamma h\,\psi_k e_k$ with sampling period $h$ is the same rule as the [LMS algorithm](/lms-algorithm/) when $e$ is linear in $\theta$.
- **Extremum seeking.** When the gradient cannot be computed from a model, [extremum seeking control](/extremum-seeking-control/) estimates it with a dither signal.

## When to use it

Use the MIT rule to explain the idea of gradient adaptation, or in a loop where the adaptation is slow compared with the closed loop dynamics and the command amplitude is bounded and known. Then the gain can be chosen by the averaging analysis of Åström and Wittenmark (Section 5.3), as a rule of thumb. For a design that must keep all signals bounded for all bounded commands, use the Lyapunov based [MRAC](/model-reference-adaptive-control/) or a [self-tuning regulator](/self-tuning-regulator/).

## Pitfalls

- **Large gain or large command.** The stability limit depends on $\gamma u_0^2$, not on $\gamma$ alone. A gain that is tuned for small commands can be unstable for large ones.
- **Wrong sign of the gain.** The rule then moves $\theta$ the wrong way.
- **Exact sensitivities assumed.** The derivation treats $\theta$ as a constant. When $\theta$ changes fast, $\psi$ is not the gradient, and the rule is no longer a descent method.
- **Unmodeled dynamics.** Even the Lyapunov version can drift and lose stability under unmodeled dynamics and disturbances; see [Rohrs counterexample](/rohrs-counterexample/).
- **Error definition.** This page uses $e = y - y_m$. With $e = y_m - y$ every sign in the update changes.

## Implementations

## History

Whitaker, Yamron and Kezer (1958) at the MIT Instrumentation Laboratory proposed the model reference adaptive system for the flight control of aircraft, with the gains adjusted along the gradient of the squared error. The rule had no stability proof. Parks (1966) showed that it can be unstable and redesigned the law with Lyapunov theory, which gave model reference adaptive systems with bounded signals and an error that goes to zero for every bounded command. Ioannou and Sun (Section 1.3) give a short history of this period.

## References
