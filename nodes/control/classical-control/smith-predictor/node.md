---
tag: R7T7GR
kind: algorithm
slug: smith-predictor
name: Smith predictor
aliases:
- Smith dead-time compensator
area: control/classical-control
level: core
summary: Takes the dead time out of the loop by feeding back a delay-free model output, so the controller can be tuned as if there were no delay.
model: real-ram
complexity:
  vars: {k: the number of samples, n: the order of the model, d: the delay of the model in samples}
  time: {worst: "O(k n^2)"}
  space: {extra: "O(n + d)"}
properties: {deterministic: true, exact: true, recursive: false, online: true}
history:
  year: 1957
  people: [Otto J. M. Smith]
  note: "O. J. M. Smith proposed in 1957 to control a plant with dead time through a model of the plant, so that the controller acts on a prediction of the output without the delay."
prereqs: [time-delay-system, feedback-control-loop, complementary-sensitivity-function]
see_also: [pid-controller, internal-model-control, ziegler-nichols-tuning, pade-approximation, small-gain-theorem, model-predictive-control, dynamic-matrix-control, disturbance-observer]
sources:
  - paper: "O. J. M. Smith, Closer control of loops with dead time, Chemical Engineering Progress 53(5), 217-219, 1957"
    locator: the whole paper (the predictor structure)
  - book: isbn:9781556179426
    title: Karl Johan Åström and Tore Hägglund, Advanced PID Control, ISA, 2006
    locator: Sections 8.2 and 8.3 (the Smith predictor and its properties)
  - paper: doi:10.1021/i200017a016
    title: Carlos E. Garcia and Manfred Morari, Internal model control. 1. A unifying review and some new results, Industrial and Engineering Chemistry Process Design and Development 21(2) (1982) 308-323
    locator: the whole paper (the internal model control structure, which contains the Smith predictor)
---

The Smith predictor is a controller structure for a plant with a dead time, $P(s) = P_0(s) e^{-\theta s}$. It runs a model of the plant next to it. The model gives two outputs: the output without the delay, $\hat y_0$, and the same output delayed by $\theta$, $\hat y_d$. The primary controller, often a [PID controller](/pid-controller/), gets the signal $y + \hat y_0 - \hat y_d$. If the model is exact, $y = \hat y_d$, so the controller sees the output that the plant would have without the delay. The controller can then be tuned for $P_0$ alone, and the closed loop answers a set-point change as the delay-free loop does, only $\theta$ later.

## In plain words

Some plants answer late. A valve opens, and the flow far down the pipe changes only seconds later. A normal controller sees no effect, pushes harder, and overshoots. The Smith predictor keeps a copy of the plant in the computer. The copy has two outputs: what the plant will do without the wait, and what it will do with the wait. The controller looks at the first output, so it sees the effect of its action at once and does not overshoot. The real measurement still counts. The difference between the real output and the copy with the wait shows the effects that the copy does not know, such as a load or a model error, and this difference is added in. The result is good only if the copy is close to the plant, the delay most of all.

## The problem

**Input.** A plant $P = P_0 e^{-\theta s}$ with one input and one output, a model $P_m = P_{0m} e^{-\theta_m s}$ of it, and a primary controller $C$ designed for $P_{0m}$. For the sampled form, the sampling period $h$, a model $\hat x_{k+1} = A_m \hat x_k + B_m u_k$, $\hat y_k = C_m \hat x_k$ of order $n$ from a [zero-order hold discretization](/zero-order-hold-discretization/), and the model delay $d = \theta_m/h$ in whole samples.

**Output.** At each sample, the control signal $u_k$ from the set point $r_k$ and the measurement $y_k$.

**The aim.** With an exact model the loop from $r$ to $y$ is $T_0(s) e^{-\theta s}$, where $T_0 = C P_0/(1 + C P_0)$ is the [complementary sensitivity](/complementary-sensitivity-function/) of the delay-free loop. So the delay is outside the loop: it does not enter the characteristic equation, and it does not limit the gain of $C$. A load $v$ at the input of $P_0$ gives $y = P_0 (1 - T_0 e^{-\theta s}) v$. The load still acts for the time $\theta$ before the controller can answer it, and no controller can avoid that.

## The algorithm

```pseudo id=main
SMITH-STEP(r, y)
L1  y_f ← yhat0 + (y - yhat_d)      // yhat0 = C_m xhat; yhat_d = oldest value in the delay line
L2  e ← r - y_f
L3  u ← primary controller step with the error e
L4  xhat ← A_m xhat + B_m u
L5  push yhat0 into the delay line and drop its oldest value
L6  return u
```

The delay line holds the last $d$ values of $\hat y_0$, so its oldest value is $\hat y_0$ from $d$ samples ago, which is the model output with the delay. The state of the controller is $\hat x$, the delay line and the state of the primary controller. In the code the primary controller is a sampled PI controller, $u = K e + I$, then $I \leftarrow I + (K h/T_i) e$. Any controller with a step method can take its place.

The order of the operations in L1 matters for exact arithmetic. With an exact model, $y$ and $\hat y_d$ are the same number, so $y - \hat y_d$ is exactly 0 and $y_f = \hat y_0$.

## Example

**The plant.** Take $P_0 = 1/(s + 1)$, a delay $\theta = 2$ s, $h = 0.1$ s, so $d = 20$ samples. The delay is twice the time constant. Choose the PI controller $K = 2$, $T_i = 1$ s. Then $T_i$ cancels the plant pole, $C P_0 = 2/s$ and $T_0 = 2/(s + 2)$, a first order loop with the time constant 0.5 s.

**Set-point step.** All numbers are measurements on the sampled loop; the 2 percent band defines the settling time.

| controller | overshoot | settling time |
|---|---|---|
| PI $K = 2$, $T_i = 1$ s, no delay in the plant | 0.0021 | 1.7 s |
| Smith predictor with the same PI | 0.0021 | 3.7 s |
| the same PI with the delay, no predictor | output grows, peak 326 by 20 s | - |
| Ziegler-Nichols PI, $K = 0.684$, $T_i = 4.575$ s | 0 | 32.0 s |
| PI $K = 0.5$, $T_i = 2$ s | 0 | 12.7 s |
| PI $K = 0.4$, $T_i = 1.5$ s | 0.012 | 6.2 s |

The Smith loop gives the delay-free response shifted by exactly 2 s; the difference between the two records is 0 in floating point. Without the predictor the same PI makes the loop diverge. The [Ziegler-Nichols](/ziegler-nichols-tuning/) PI comes from the ultimate point $K_u = 1.5198$, $T_u = 5.4901$ s of this plant, and is slow. A PI tuned by hand for the delay does better, but it still settles more slowly than the Smith loop.

**Load step.** A unit load at the input of $P_0$ gives the peak 0.8775 and the integral of $y$ equal to 2.500 with the Smith loop. The Ziegler-Nichols PI gives the peak 0.883 and the integral 6.69. The peaks are close, because for the first 2 s no controller can act on the load. The Smith loop removes the load faster afterwards.

**Model errors.** The plant stays as above and the model changes. The settling times are for the set-point step.

| model error | overshoot | settling time |
|---|---|---|
| model delay 2.2 s | 0.031 | 8.8 s |
| model delay 1.8 s | 0.158 | 6.7 s |
| model delay 3.0 s | output grows, peak 833 by 150 s | - |
| model gain 1.2 | 0 | 6.9 s |
| model gain 0.8 | 0.224 | 7.8 s |
| model time constant 1.5 s | 0.188 | 11.3 s |

A delay error of 10 percent doubles or triples the settling time. In this example the loop converges for every model delay from 0.8 s to 2.7 s, and it diverges for model delays of 0.6 s or less and from 2.9 s to 4.0 s, the largest value tried (measurement). The small gain bound of the Correctness section guarantees convergence of the continuous loop for delay errors below 0.7387 s.

**A plant with a pole in the right half-plane.** For $P_0 = 1/(s - 1)$, $\theta = 0.5$ s, $h = 0.05$ s and the PI $K = 3$, $T_i = 1$ s, the set-point step has the overshoot 0.507 and settles in 4.65 s. A load of 0.01 makes $y$ grow by the factor $e$ every second. The predictor does not work for such a plant.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md).

- **Exact model (theorem).** With $P_m = P$, the set-point response is $T_0 e^{-\theta s}$ and the load response is $P_0 (1 - T_0 e^{-\theta s})$. For the sampled loop, $y_k$ equals the output of the delay-free loop at sample $k - d$, exactly.
- **Internal stability (theorem).** If $P_0$ is BIBO stable and the model is exact, the Smith loop is internally stable if and only if the delay-free loop of $C$ and $P_0$ is. The proof uses the [internal model control](/internal-model-control/) form of the loop.
- **Poles in the right half-plane (theorem).** If $P_0$ has a pole $p$ with $\operatorname{Re} p \ge 0$ and $e^{-\theta p} \ne 1$, the load response keeps that pole for every $C$, so the loop is not internally stable.
- **Robust stability (theorem).** With $P = P_m (1 + \Delta)$ and both BIBO stable, the loop is internally stable if $|T_{0m}(j\omega)|\, |\Delta(j\omega)| < 1$ for all $\omega$. For a delay error $\delta$ the factor is $|e^{-j\omega\delta} - 1|$, which reaches 2. The condition is sufficient, not necessary.
- **Integral action (theorem).** With a PI controller the steady-state error to a set-point step is zero, and the integral of $y$ after a unit load step is $T_i/K + P_0(0)\,\theta$.

## Complexity

One controller step costs $O(n^2)$ time for the model update and $O(1)$ for the delay line and a PI controller. A run of $k$ samples costs $O(k n^2)$. The controller keeps $O(n + d)$ numbers, the model state and the delay line. A long delay at a short sampling period needs a long delay line, but the cost per sample does not grow with it.

## Properties

- **The delay leaves the loop.** With an exact model the characteristic equation is that of the delay-free loop, so the controller can have a high gain even when the delay is long.
- **Model based.** The structure needs a model of $P_0$ and of the delay. The quality of control depends on the model, the delay most of all.
- **Load response.** The predictor does not shorten the time that a load acts before the controller answers. It helps after that time.
- **Plants with all poles in the left half-plane only.** The basic predictor does not suit a plant with an integrator, where a constant load leaves a constant error, or a plant with a pole in the right half-plane, where the loop is not internally stable. Both are theorems in the proof.
- **Linear time-invariant.** The structure adds no nonlinearity. Actuator limits need the same care as in any loop with integral action.

## Variants and improvements

- **Internal model control.** The Smith predictor with the controller $C$ is the internal model control structure with $Q = C/(1 + C P_0)$. Designing $Q$ directly gives the same structure with a different tuning.
- **Filtered predictors.** A filter on the correction $y - \hat y_d$ reduces the effect of noise and model errors and can make the scheme work for a plant with an integrator. Several variants of this kind exist for integrating plants and for plants with a pole in the right half-plane.
- **Model predictive control.** [Model predictive control](/model-predictive-control/) and [dynamic matrix control](/dynamic-matrix-control/) also predict the output over the delay with a model, and they add constraints and several inputs.
- **Disturbance observer.** A [disturbance observer](/disturbance-observer/) uses a similar comparison of plant and model to estimate the load.

## When to use it

Use the Smith predictor when the delay is long compared with the main time constant of the plant, the plant has all its poles in the left half-plane, and the delay is known well, for example from the length and speed of a conveyor or a pipe. When the delay is short compared with the time constant, a PID controller does about as well and needs no model. When the delay changes with the operating point, the model delay must follow it, or the loop must be tuned for the worst case.

## Pitfalls

- **Delay errors.** A wrong model delay hurts more than a wrong gain. In the example, a model delay 10 percent too short gives 16 percent overshoot. Keep the bandwidth of the delay-free loop moderate when the delay is uncertain.
- **Tuning for the delay-free model only.** A controller tuned very fast for $P_0$ has $|T_0|$ near 1 at high frequency, and the robust stability condition then fails for small delay errors.
- **Integrating and other plants with poles outside the open left half-plane.** The basic structure cannot remove a constant load on a plant with an integrator, and it cannot be internally stable for a plant with a pole in the right half-plane. Use a modified predictor.
- **Load response expectations.** The set-point response looks like the delay-free one, but a load still acts for the full delay before any correction arrives.
- **Sampling and the delay.** The sampled model holds the delay in whole samples. A delay that is not a whole number of samples needs a fractional delay in the model, or the error counts as a delay error.

## Implementations

## History

Otto J. M. Smith published the predictor in 1957 in Chemical Engineering Progress, in a short paper on the control of loops with dead time. A delay is hard to build with analog hardware, but in a digital controller it is only a queue of samples, so the predictor became easy to implement. In 1982 Garcia and Morari showed that the Smith predictor is a special case of internal model control, which gave a frame for its robustness analysis. Åström and Hägglund treat it in Sections 8.2 and 8.3 of their 2006 book on PID control.

## References
