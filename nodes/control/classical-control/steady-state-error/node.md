---
tag: W3CB6S
kind: definition
slug: steady-state-error
name: Steady-state error
aliases:
- tracking error at steady state
area: control/classical-control
level: intro
summary: The limit of the error r - y of a stable loop for a step, ramp or parabola reference. The system type and the constants K_p, K_v and K_a give it, for example 1/(1 + K_p) for a step and type 0.
prereqs: [final-value-theorem, feedback-control-loop]
see_also: [feedback-control-loop, final-value-theorem, internal-model-principle, sensitivity-function, step-response-specifications, pid-controller, integral-state-feedback, routh-hurwitz-criterion]
sources:
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Chapter 4, A First Analysis of Feedback (the control of the steady-state error to polynomial inputs, the system type and the error constants)
  - book: isbn:9780136156734
    title: Katsuhiko Ogata, Modern Control Engineering, fifth edition, Prentice Hall, 2010
    locator: Chapter 5, Transient and Steady-State Response Analyses (steady-state errors in unity feedback systems, the static position, velocity and acceleration error constants)
---

The steady-state error of a [feedback control loop](/feedback-control-loop/) is the limit, as time goes to infinity, of the error $e(t) = r(t) - y(t)$ between the reference and the output, for a reference of a given shape. The standard shapes are the step, the ramp and the parabola. In a unity feedback loop the answer depends on only two facts about the loop transfer function $L = P C$: its number of poles at $s = 0$, called the *system type*, and one gain, the *error constant*. A type 0 loop follows a unit step with the error $1/(1 + K_p)$, a type 1 loop follows it with zero error and a ramp with the error $1/K_v$, and so on. The numbers mean something only when the loop is internally stable; the formulas give a finite value for an unstable loop too, and that value is then wrong.

## Definition

Take a negative unity feedback loop with $e = r - y$, $y = L e$, and a rational loop transfer function $L(s) = P(s) C(s)$. Assume the loop is internally stable. With $E(s) = S(s) R(s)$ and $S = 1/(1 + L)$ the [sensitivity function](/sensitivity-function/), the **steady-state error** to the reference $r$ is

$$e_\infty = \lim_{t \to \infty} e(t),$$

when the limit exists. If $e(t)$ is unbounded, the error is said to be infinite.

**System type.** Write $L(s) = \dfrac{K\, b_0(s)}{s^N a_0(s)}$ with $a_0(0) = b_0(0) = 1$ and $K \ne 0$. The integer $N \ge 0$, the number of poles of $L$ at the origin, is the **type** of the loop.

**Error constants.**

$$K_p = \lim_{s \to 0} L(s), \qquad K_v = \lim_{s \to 0} s\,L(s), \qquad K_a = \lim_{s \to 0} s^2 L(s).$$

They are the position, velocity and acceleration error constants. If $r$ and $y$ have the same unit, $K_p$ has no unit, $K_v$ is in 1/s and $K_a$ in 1/s$^2$. For a loop of type $N$, the constant of index $N$ equals $K$, the lower ones are infinite and the higher ones are 0.

**The table.** For the references $r = 1$ (step), $r = t$ (ramp) and $r = t^2/2$ (parabola), $t \ge 0$:

| type $N$ | step | ramp | parabola |
|---|---|---|---|
| 0 | $1/(1 + K_p)$ | $\infty$ | $\infty$ |
| 1 | 0 | $1/K_v$ | $\infty$ |
| 2 | 0 | 0 | $1/K_a$ |

A reference with a different size scales the error: a ramp $r = A t$ gives $A/K_v$ in a type 1 loop.

**Why.** For $r = t^k/k!$, $R(s) = 1/s^{k+1}$ and

$$s E(s) = \frac{S(s)}{s^k} = \frac{s^{N - k}\,a_0(s)}{s^N a_0(s) + K\,b_0(s)}.$$

The denominator is the characteristic polynomial of the loop up to a constant factor, so it is Hurwitz. If $k \le N$, $s E(s)$ has all its poles in the open left half plane, and the [final value theorem](/final-value-theorem/) gives $e_\infty = \lim_{s \to 0} s E(s)$: this is 0 for $k < N$, and $1/(1 + K)$ for $k = N = 0$, and $1/K$ for $k = N \ge 1$. If $k > N$, $E(s)$ has a pole of order $k - N + 1 \ge 2$ at the origin, so by partial fractions $e(t)$ contains a term $c\,t^{k - N}$ with $c \ne 0$ and grows without bound. The final value theorem does not apply in that case.

## Examples and non-examples

**Example: type 0.** $L(s) = 10/((s + 1)(s + 2))$. Then $K_p = 10/2 = 5$ and the step error is $1/(1 + 5) = 1/6$. The closed loop $s^2 + 3 s + 12$ is Hurwitz, so the value is correct. A ramp reference gives an error that grows like $t/6$.

**Example: type 1.** $L(s) = 10/(s(s + 2))$. Then $K_v = 10/2 = 5$ 1/s, the step error is 0 and the ramp error is $1/5 = 0.2$. The closed loop $s^2 + 2 s + 10$ is Hurwitz. This loop is the [standard second-order system](/second-order-system/) with $\omega_n = \sqrt{10}$ and $\zeta = 1/\sqrt{10}$, and indeed $K_v = \omega_n/(2\zeta) = 5$.

**Example: a disturbance is a different input.** Let $P(s) = 1/(s(s + 1))$ and $C(s) = k > 0$, a type 1 loop with zero step error to the reference. A unit step load disturbance $d$ at the plant input gives $E = -P S\,D$, and

$$e_\infty = -\lim_{s \to 0} \frac{P(s)}{1 + k P(s)} = -\lim_{s \to 0} \frac{1}{s(s + 1) + k} = -\frac{1}{k}.$$

The integrator of the plant does not remove this error, because it is behind the point where the disturbance enters. An integrator in $C$ does. The system type counts the poles of $L$, so it only speaks about the reference; the [internal model principle](/internal-model-principle/) gives the rule for a disturbance at any point.

**Non-example: an unstable loop.** $L(s) = 10/(s(s + 1)(s + 2))$ gives $K_v = 5$ and the formula ramp error $0.2$. But the closed loop $s^3 + 3 s^2 + 2 s + 10$ is not Hurwitz (for a cubic $s^3 + a_2 s^2 + a_1 s + a_0$ with positive coefficients, the test is $a_2 a_1 > a_0$, and $3 \cdot 2 = 6 < 10$; see the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/)). The error grows without bound. The value 0.2 is meaningless.

**Non-example: a non-unity feedback loop.** If the sensor has the transfer function $H(s)$ with $H(0) \ne 1$, the signal the controller sees, $r - H y$, is not the error $r - y$. The table applies only after the loop is redrawn as a unity feedback loop with the equivalent loop transfer function $P C/(1 + P C (H - 1))$.

## Related definitions

- **Sensitivity at zero frequency.** For a step, $e_\infty = S(0)$. A type $N$ loop has $S(s) = O(s^N)$ near the origin, which is the frequency-domain form of the table.
- **Bode plot reading.** For a type 1 loop the low-frequency asymptote of $|L(j\omega)|$ is $K_v/\omega$, which crosses 1 at $\omega = K_v$.
- **Discrete time.** For a loop $L(z)$ with the sampling period $h$, the type is the number of poles at $z = 1$, and $K_p = \lim_{z \to 1} L(z)$, $K_v = \lim_{z \to 1} (z - 1) L(z)/h$. The discrete final value theorem replaces the continuous one.
- **Integral action.** An integrator in the controller raises the type by one; this is the reason for the I term of the [PID controller](/pid-controller/) and for [integral state feedback](/integral-state-feedback/).
- **Internal model principle.** Zero steady-state error to a step, a ramp or a sinusoid for all small plant changes needs a copy of the signal model in the controller; see [internal model principle](/internal-model-principle/).

## References
