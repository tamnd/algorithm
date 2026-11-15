---
tag: 7QVRVJ
kind: algorithm
slug: ziegler-nichols-tuning
name: Ziegler-Nichols tuning
aliases:
- Ziegler-Nichols method
- ultimate gain method
area: control/classical-control
level: intro
summary: Sets PID gains by rules from the ultimate gain and period found at the edge of oscillation, or from a step response.
model: real-ram
complexity:
  vars: {g: the number of frequency grid points, n: the degree of the plant, k: the number of samples of the step response}
  time: {worst: "O(g n + k)"}
  space: {extra: O(g)}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1942
  people: [John G. Ziegler, Nathaniel B. Nichols]
  note: "Ziegler and Nichols of the Taylor Instrument Companies published two sets of tuning rules for industrial controllers in 1942, one from the ultimate sensitivity and period and one from the process reaction curve."
prereqs: [frequency-response, gain-margin, process-reaction-curve]
see_also: [pid-controller, relay-autotuning, internal-model-control, nyquist-stability-criterion, describing-function, limit-cycle, phase-margin, time-delay-system]
sources:
  - paper: doi:10.1115/1.4019264
    title: J. G. Ziegler and N. B. Nichols, Optimum settings for automatic controllers, Transactions of the ASME 64(8) (1942) 759-768
    locator: the summary table of the settings on p. 765 and the quarter amplitude decay on p. 764
  - paper: doi:10.1016/j.jprocont.2004.01.002
    title: Karl Johan Åström and Tore Hägglund, Revisiting the Ziegler-Nichols step response method for PID control, Journal of Process Control 14(6) (2004) 635-650
    locator: the whole paper (the analysis of the step response method and the AMIGO rules)
  - book: isbn:9781556179426
    title: Karl Johan Åström and Tore Hägglund, Advanced PID Control, ISA, 2006
    locator: Section 6.2, Ziegler-Nichols and related methods, and Chapter 7, the AMIGO rules
---

Ziegler-Nichols tuning sets the three parameters of a [PID controller](/pid-controller/) from two numbers that one simple experiment gives. In the *ultimate cycle method* a P controller is put on the plant and its gain is raised until the loop oscillates with a constant amplitude. The gain at that point is the ultimate gain $K_u$ and the period of the oscillation is the ultimate period $T_u$. In the *step response method* the plant gets a step input in open loop, and a tangent at the steepest point of the response gives a slope and an apparent delay. A table then gives $K$, $T_i$ and $T_d$. The rules are rules of thumb that aim at a decay ratio of one quarter. This page computes the ultimate point from a model, fits the tangent to a sampled response and applies both tables.

## In plain words

Turn up the gain of a simple controller until the loop starts to swing with a steady size. Note that gain and the time of one swing. These two numbers tell how much gain the plant takes and how fast it is. The rules then say: use a bit more than half that gain, and set the integral and derivative times to fixed parts of the swing time. The other method kicks the plant once and draws a straight line along the steepest part of the response. Where that line starts tells the delay, and how steep it is tells the gain. Both methods are fast and need no model. The loop they give is often too lively, so people treat the result as a first try and then adjust it.

## The problem

**Input for the ultimate cycle method.** A plant $P(s) = \frac{n(s)}{d(s)} e^{-\theta s}$ with real polynomials, $\deg n < \deg d$, a delay $\theta \ge 0$ and a positive gain at low frequency. On a real plant the input is the experiment itself.

**Input for the step response method.** Samples $y_0, \dots, y_{k-1}$ of the response to an input step of size $\Delta u$ at $t = 0$, from rest, with a uniform time step $\Delta t$.

**Output.** The parameters of the ideal PID form $C(s) = K (1 + 1/(T_i s) + T_d s)$, or of its P or PI part.

**The ultimate point.** It is the smallest $\omega_u > 0$ with $\arg P(j\omega_u) = -180$ degrees, and

$$K_u = \frac{1}{|P(j\omega_u)|}, \qquad T_u = \frac{2\pi}{\omega_u}.$$

At $K = K_u$ the closed loop with a P controller has the poles $\pm j\omega_u$, so it oscillates with the period $T_u$. So $K_u$ is the [gain margin](/gain-margin/) of the plant under unit proportional feedback. A plant whose phase stays above $-180$ degrees, such as $1/(s + 1)^2$, has no finite ultimate gain, and the method does not apply.

**The tables.** For the ultimate cycle method:

| controller | $K$ | $T_i$ | $T_d$ |
|---|---|---|---|
| P | $0.5 K_u$ | | |
| PI | $0.45 K_u$ | $T_u/1.2$ | |
| PID | $0.6 K_u$ | $T_u/2$ | $T_u/8$ |

For the step response method, with the largest slope $R$ per unit input, the apparent delay $L$ and $a = R L$:

| controller | $K$ | $T_i$ | $T_d$ |
|---|---|---|---|
| P | $1/a$ | | |
| PI | $0.9/a$ | $L/0.3$ | |
| PID | $1.2/a$ | $2 L$ | $L/2$ |

Ziegler and Nichols gave the PI integral time as a reset rate of $0.3/L$ repeats per minute, which is $T_i = 3.33 L$. Many books round it to $3 L$. The two tables agree on the PID times if $T_u = 4 L$.

## The algorithm

```pseudo id=main
ZN-ULTIMATE(n, d, theta, rule)
L1  phi_i ← continuous phase of P(j w_i) on a log grid w_0 < w_1 < ... < w_g
L2  i ← the first index with phi_i ≤ -pi;  if there is none then fail
L3  w_u ← bisection of phi(w) = -pi on [w_(i-1), w_i]
L4  K_u ← 1/|P(j w_u)|;  T_u ← 2 pi / w_u
L5  return (K, T_i, T_d) from the ultimate cycle table
ZN-STEP(t, y, du, rule)
L6  j ← the sample with the largest slope R = (y_(j+1) - y_(j-1)) / (2 dt du)
L7  L ← t_j - (y_j - y_0) / (R du);  a ← R L
L8  return (K, T_i, T_d) from the step response table
```

Line L1 starts the phase at $-90$ degrees per net pole at the origin. It unwraps the phase of the rational part from one grid point to the next and adds $-\omega\theta$ for the delay. The grid has 4000 points from $10^{-6}$ to $10^3$ rad/s. Line L3 halves the bracket until it is $10^{-15}$ of its upper end. Line L6 uses central differences, so the first and the last sample cannot be the steepest point. If the steepest point is at the end of the record, the record is too short and the code stops with an error.

## Example

**A third order lag.** Take $P(s) = 1/(s + 1)^3$. Its phase is $-3 \arctan \omega$, which is $-180$ degrees at $\omega_u = \tan 60° = \sqrt 3$. Its gain there is $(1 + 3)^{-3/2} = 1/8$. So $K_u = 8$ and $T_u = 2\pi/\sqrt 3 = 3.62760$ s. Indeed $(s + 1)^3 + 8 = (s + 3)(s^2 + 3)$, with the roots $\pm j\sqrt 3$. The code gives $K_u = 8$ and $\omega_u = \sqrt 3$ to 15 digits.

The unit step response is $y(t) = 1 - e^{-t}(1 + t + t^2/2)$, with the slope $y'(t) = t^2 e^{-t}/2$. The slope is largest at $t = 2$. So $R = 2 e^{-2} = 0.270671$, $L = (9 - e^2)/2 = 0.805472$ s and $a = 9 e^{-2} - 1 = 0.218018$. From a response sampled with $\Delta t = 0.01$ s the code gives $L = 0.805462$ s. Here $4 L = 3.22$ s, a little shorter than $T_u$.

**The loops.** The table shows the four tunings and the closed loops that they give. The derivative has the filter constant $N = 20$, all terms act on the error, and the loop is simulated with the classical Runge-Kutta method of order 4 and the step 0.01 s up to $t = 80$ s. The decay ratio is the second peak above the final value divided by the first. The load response is the response of $y$ to a unit step at the plant input.

| tuning | $K$ | $T_i$ (s) | $T_d$ (s) | set-point overshoot | set-point decay ratio | load peak | load decay ratio |
|---|---|---|---|---|---|---|---|
| ultimate PI | 3.6 | 3.0230 | | 0.561 | 0.578 | 0.299 | 0.409 |
| ultimate PID | 4.8 | 1.8138 | 0.4534 | 0.523 | 0.138 | 0.188 | 0.097 |
| step PI | 4.1281 | 2.6849 | | 0.684 | 0.755 | 0.276 | 0.525 |
| step PID | 5.5041 | 1.6109 | 0.4027 | 0.645 | 0.254 | 0.174 | 0.188 |

These are measurements of this simulation. All four loops are asymptotically stable, and the overshoot of the set-point response is above 50 percent in every case. The PI tunings decay slowly. The ultimate P controller, $K = 4$, gives the final value $4/5 = 0.8$, so the steady-state error is 0.2, and its decay ratio is 0.39. The [PID controller](/pid-controller/) page shows that the ultimate PID tuning has a phase margin of about 30 degrees and the peak sensitivity $M_s = 2.13$.

**Delays.** For $P(s) = e^{-\theta s}/(s + 1)$, the ultimate frequency solves $\arctan \omega_u + \omega_u \theta = \pi$, and $K_u = \sqrt{1 + \omega_u^2}$. With $\theta = 1$ s the code gives $\omega_u = 2.02876$ rad/s, $T_u = 3.09706$ s and $K_u = 2.26183$. With $\theta = 0.1$ s it gives $\omega_u = 16.3199$ rad/s and $K_u = 16.3506$. The ultimate gain grows as the delay gets shorter, and for $\theta \to 0$ a first order lag has no finite ultimate gain.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md).

- **The ultimate point (theorem).** At $K = K_u$ the closed loop with a P controller has the poles $\pm j\omega_u$. Conversely, a closed-loop pole on the imaginary axis can only occur at a frequency where the phase is $-180$ degrees, with $K = 1/|P|$ there.
- **Below the ultimate gain (theorem).** If the plant has no poles in the open right half plane, at most one integrator, and a gain $|P(j\omega)|$ that falls strictly with $\omega$, then every gain $0 < K < K_u$ gives an asymptotically stable closed loop. The proof uses the [Nyquist stability criterion](/nyquist-stability-criterion/).
- **Above the ultimate gain (measurement).** For random products of 3 to 5 real lags, the tests find a closed-loop pole in the right half plane at $K = 1.1 K_u$.
- **The search (theorem).** If the grid is fine enough that the phase moves less than 180 degrees between neighbours and crosses $-180$ degrees only once inside each grid interval, lines L1 to L3 converge to $\omega_u$.
- **The tangent fit (theorem).** At the inflection point the time $t - (y - y_0)/y'$ has a zero derivative. So the fit has an error of order $\Delta t^2$.
- **The tables (rule of thumb).** Ziegler and Nichols chose the factors from many tests, to get a decay ratio near one quarter on typical process plants. They do not follow from a theorem. The example shows that the decay ratio can be far from one quarter.

## Complexity

The search evaluates the plant at $g$ grid points. Each evaluation is two Horner evaluations of degree at most $n$, so the search costs $O(g n)$ time. The bisection adds about 50 steps of $O(n)$ each. The tangent fit visits each of the $k$ samples once, so it costs $O(k)$. The phase list takes $O(g)$ space. The cost that counts on a real plant is the time of the experiment: the ultimate cycle method needs several periods $T_u$ at each trial gain, and the step response method needs one response that reaches the steepest point.

## Properties

- **Two numbers.** Each method reduces the plant to two numbers, $K_u$ and $T_u$, or $a$ and $L$. Plants with the same two numbers get the same controller.
- **Scale.** The controller gain scales as $1/K_u$ or $1/a$, and the times scale with $T_u$ or $L$. So a change of the units of time or of the plant gain gives the same loop in the new units.
- **Fixed ratio.** Both PID rules give $T_i = 4 T_d$, so the PID has a double real zero and it has a [series form](/pid-controller/) with equal times.
- **Aggressive.** The target decay ratio of one quarter gives a damping ratio near 0.2 for a dominant pair of poles. This is a fast but lightly damped loop, with poor robustness for many plants.

## Variants and improvements

- **Relay feedback.** [Relay autotuning](/relay-autotuning/) finds the ultimate point with a relay in place of a P controller at the edge of oscillation. The loop then oscillates with a controlled amplitude, which is safer on a real plant.
- **Smaller factors.** Many later tables keep the form of the ultimate cycle rule and use a smaller gain factor than 0.6, to get less overshoot at the cost of a slower load response.
- **AMIGO rules.** Åström and Hägglund fitted rules to a large test batch of plants under a constraint on the peak sensitivity $M_s$. These rules use a first order model with a delay in place of the two numbers $a$ and $L$, and they give much better robustness.
- **Model based rules.** [Internal model control](/internal-model-control/) gives PI and PID settings from a first order model with a delay, with one tuning knob, the closed-loop time constant. Skogestad's SIMC rules are of this kind.
- **Set-point weighting.** A set-point weight $b < 1$ in the proportional term cuts the overshoot to set-point steps without a change of the load response. See [two-degree-of-freedom control](/two-degree-of-freedom-control/).

## When to use it

Use the ultimate cycle method when the plant can be run safely at the edge of oscillation for a few periods, and when a quick first tuning is good enough. Use the step response method when the plant can be run in open loop, its response is slow and has an S shape, and the noise is small enough that a tangent can be drawn. Use either set of factors as a start, and then reduce the gain or add a set-point weight if the overshoot is too large. Do not use the method on plants with a negative low-frequency gain without the reverse action, or on plants with lightly damped modes, where the two numbers do not describe the plant.

## Pitfalls

- **Large overshoot.** The quarter decay target gives overshoots of 50 percent and more to set-point steps, as the example shows. Treat the result as a first try.
- **Running at the limit.** The ultimate cycle experiment brings the loop to the edge of a growing oscillation. A change of the plant during the test can make the oscillation grow. Use a relay in place of the high gain where this is a risk.
- **Integral times in the PI rule.** The step response PI rule is $T_i = L/0.3 = 3.33 L$ in the paper and $3 L$ in many books. State which one you use.
- **Forms.** The rules are for the ideal (standard) form. A controller in the series or parallel form needs a conversion; see [PID controller](/pid-controller/).
- **Long delays.** The two numbers $a$ and $L$ do not tell a plant with a long delay from a plant with a long lag, and Åström and Hägglund (2004) show that the step response rules work poorly when the delay is long compared with the time constant. A [Smith predictor](/smith-predictor/) or a model based rule works better there.
- **Noise and the tangent.** The steepest slope of a noisy record is an estimate of a derivative, which amplifies noise. Filter the record or fit a model first.

## Implementations

## History

John G. Ziegler and Nathaniel B. Nichols worked at the Taylor Instrument Companies in Rochester, New York. In 1942 they published "Optimum settings for automatic controllers" in the Transactions of the ASME. They measured the ultimate sensitivity and the ultimate period of a loop, and the reaction rate and the lag of a plant from its response curve, and gave the settings in a short table. They chose the settings so that an oscillation decays to a quarter of its amplitude in each period. The rules spread through the process industry and are still the best known tuning rules. Åström and Hägglund revisited the step response method in 2004 and showed that its robustness is often poor; they proposed the AMIGO rules in its place.

## References
