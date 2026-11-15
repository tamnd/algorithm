---
tag: M0FN5Q
kind: algorithm
slug: pid-controller
name: PID controller
aliases:
- proportional-integral-derivative controller
- three-term controller
area: control/classical-control
level: intro
summary: Sets the control to a weighted sum of the error, its integral and its filtered derivative, the most used controller in industry.
model: real-ram
complexity:
  vars: {k: the number of samples}
  time: {worst: O(k)}
  space: {extra: O(1)}
properties: {deterministic: true, exact: false, recursive: false, online: true}
history:
  year: 1922
  people: [Nicolas Minorsky]
  note: "Minorsky analyzed the automatic steering of ships in 1922 and showed that a steering law with proportional, integral and derivative terms gives a good course keeping."
prereqs: [feedback-control-loop, transfer-function, sampled-data-system]
see_also: [ziegler-nichols-tuning, relay-autotuning, integrator-windup, anti-windup, two-degree-of-freedom-control, internal-model-control, controller-discretization, lead-lag-compensator]
sources:
  - paper: doi:10.1111/j.1559-3584.1922.tb04958.x
    title: Nicolas Minorsky, Directional stability of automatically steered bodies, Journal of the American Society of Naval Engineers 34(2) (1922) 280-309
    locator: the whole paper (the steering law with proportional, integral and derivative terms)
  - book: isbn:9781556179426
    title: Karl Johan Åström and Tore Hägglund, Advanced PID Control, ISA, 2006
    locator: Chapter 3, PID Control (Sections 3.2 to 3.5, the forms, the derivative filter, set-point weighting and windup) and Section 13.3, Computer implementations
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, second edition, Princeton University Press, 2021
    locator: Chapter 11, PID Control (the sections on integral windup and on implementation)
---

A PID controller computes the control signal from the control error $e = r - y$, the difference between the set point $r$ and the measured output $y$. It adds three terms: one proportional to the error, one proportional to the integral of the error, and one proportional to the derivative of the error. The integral term removes the steady-state error for constant set points and loads. The derivative term adds phase lead and damping. A controller that is used on a real plant also needs a filter on the derivative, separate weights on the set point, limits on the output and a protection against [integrator windup](/integrator-windup/). This page gives the sampled algorithm with all of these parts, as computers run it, and proves its main properties.

## In plain words

Think of a driver who keeps a car at a set speed. The driver presses the pedal more when the car is slow. That is the proportional part. If the car stays a little slow for a long time, for example on a long hill, the driver presses a little more each second until the error is gone. That is the integral part. If the speed starts to fall quickly, the driver reacts before the error becomes large. That is the derivative part. A PID controller does the same with three numbers that set how strong each part is. A computer reads the output at fixed times, updates the three parts and sends a new command each time.

## The problem

**Input.** At each sampling instant $t_k = k h$, with the sampling period $h > 0$ in seconds: the set point $r_k$ and the measured output $y_k$. The parameters are:

- the gain $K > 0$, the integral time $T_i > 0$ and the derivative time $T_d \ge 0$, in seconds;
- the filter constant $N > 0$, usually 5 to 20, so that the derivative filter has the time constant $T_d/N$;
- the set-point weights $b$ and $c$, usually in $[0, 1]$;
- the output limits $u_{\min} \le u_{\max}$ and the tracking time $T_t > 0$ for anti-windup.

**Output.** The control signal $u_k$, held constant over $[t_k, t_{k+1})$ by a zero-order hold.

**The continuous controller.** The algorithm approximates

$$U(s) = K \left( b R(s) - Y(s) \right) + \frac{K}{T_i s} \left( R(s) - Y(s) \right) + \frac{K T_d s}{1 + s T_d/N} \left( c R(s) - Y(s) \right).$$

With $b = c = 1$ and $N \to \infty$ this is the *ideal* (or standard) form $C(s) = K (1 + 1/(T_i s) + T_d s)$ applied to $E(s)$. Two other forms are common. The *parallel* form is $C(s) = k_p + k_i/s + k_d s$, with $k_p = K$, $k_i = K/T_i$ and $k_d = K T_d$. The *series* (or interacting) form is $C(s) = K' (1 + 1/(T_i' s))(1 + T_d' s)$. Every series form has an ideal form. An ideal form has a series form with real parameters if and only if $T_i \ge 4 T_d$, because only then are the zeros of $C$ real. Old pneumatic controllers and many industrial products use the series form, so the same numbers mean different controllers in different products.

## The algorithm

The integral is approximated by the forward difference and the filtered derivative by the backward difference, as Åström and Hägglund recommend. The output limits act on $v$, and the difference $u - v$ is fed back into the integral with the gain $h/T_t$. This is the back-calculation form of [anti-windup](/anti-windup/).

```pseudo id=main
PID-STEP(r, y)    ▷ state: I, D, e_old; I = D = 0 at start
L1  once: b_i ← K h / T_i;  a_r ← h / T_t;  a_d ← T_d / (T_d + N h);  b_d ← K T_d N / (T_d + N h)
L2  e ← r - y;  e_d ← c r - y;  if this is the first call then e_old ← e_d
L3  P ← K (b r - y)
L4  D ← a_d D + b_d (e_d - e_old)
L5  v ← P + I + D
L6  u ← min(max(v, u_min), u_max)
L7  I ← I + b_i e + a_r (u - v)
L8  e_old ← e_d
L9  return u
```

Line L1 runs once, when the parameters are set. With no integral action, set $b_i = 0$; with no tracking, set $a_r = 0$. Line L2 starts the derivative at rest, so the first sample causes no jump in $D$. Line L4 is the backward difference of $(T_d/N) D' + D = K T_d\, (e^d)'$; its pole $a_d$ is in $[0, 1)$ for every $h > 0$. Line L7 runs after line L9 sends $u$ in a real controller, because the integral update is not needed for the current output. This keeps the time from the reading of $y$ to the output of $u$ short.

## Example

**Plant and tuning.** Take the plant $P(s) = 1/(s + 1)^3$, with time in seconds. Its ultimate gain is $K_u = 8$ and its ultimate period is $T_u = 2\pi/\sqrt 3 = 3.62760$ s. The classic [Ziegler-Nichols](/ziegler-nichols-tuning/) PID rule gives $K = 0.6 K_u = 4.8$, $T_i = T_u/2 = 1.81380$ s and $T_d = T_u/8 = 0.45345$ s. Take $N = 10$ and $h = 0.05$ s. Line L1 gives

| coefficient | formula | value |
|---|---|---|
| $b_i$ | $K h/T_i$ | 0.132319 |
| $a_d$ | $T_d/(T_d + N h)$ | 0.475589 |
| $b_d$ | $K T_d N/(T_d + N h)$ | 22.8283 |

At the first sample $y_0 = 0$ and $r = 1$, so $P = 4.8$, $D = 0$, $I = 0$ and $u_0 = 4.8$. Then $I$ becomes $0.132319$.

**Set-point weights.** The plant is simulated with the classical Runge-Kutta method of order 4 and the step $dt = 0.01$ s, which divides $h$. For a unit step in $r$ at $t = 0$, with no limits and $c = 0$:

| $b$ | overshoot | peak time (s) | 2 percent settling time (s) | largest $u$ |
|---|---|---|---|---|
| 1 | 0.5503 | 2.61 | 9.72 | 5.27 |
| 0.5 | 0.1826 | 3.00 | 7.90 | 3.17 |
| 0 | 0.0377 | 3.96 | 8.16 | 2.13 |

These numbers are measurements of this simulation. In all three runs $y$ is within $2 \cdot 10^{-10}$ of 1 at $t = 60$ s, as Claim 3 of the proof says. A load step of $-0.5$ at the plant input at $t = 30$ s gives the same change of $y$ for each $b$, to $10^{-12}$, as Claim 2 says. The weight $b$ trades the speed of the set-point response for its overshoot, without any change to the loop.

**Robustness of this tuning.** With the ideal derivative the loop $L = P C$ has the gain crossover at 1.37545 rad/s, a [phase margin](/phase-margin/) of 30.62 degrees and the peak sensitivity $M_s = \max_\omega |S(j\omega)| = 2.13$. With $N = 10$ the crossover moves to 1.40479 rad/s, the phase margin to 29.43 degrees and $M_s$ to 2.24. Both are on the aggressive side of the usual design range of $M_s$ from 1.2 to 2, which is a rule of thumb.

**Limits.** With $|u| \le 2$ and no tracking ($a_r = 0$), the overshoot is 0.569. With tracking and $T_t = \sqrt{T_i T_d} = 0.907$ s, the overshoot is 0.162. The [anti-windup](/anti-windup/) page explains the difference.

**Sampling period.** Compare the sampled controller with the continuous controller on the same plant, over $0 \le t \le 20$ s. The largest difference of $y$ at the sampling instants is 0.0487 for $h = 0.08$, 0.0237 for $h = 0.04$ and 0.0117 for $h = 0.02$. The error halves when $h$ halves, as expected for a first order difference scheme. With $h = 0.2$ the overshoot grows to 0.654 and with $h = 0.5$ to 0.914, because the hold adds a delay of about $h/2$ to the loop.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md).

- **Difference approximations (proved).** Line L7 is the forward Euler step of $I' = (K/T_i) e$, and line L4 is the backward Euler step of the derivative filter. The filter pole $a_d = T_d/(T_d + N h)$ is in $[0, 1)$ for every $h > 0$, so the discrete filter is asymptotically stable (Schur) for every sampling period. The forward difference would need $h < 2 T_d/N$.
- **Set-point weights (proved).** Without limits, $b$ and $c$ change only the response to $r$. The loop transfer function and the responses to load disturbances and noise do not depend on them. With $c = 0$ a step in $r$ causes no derivative kick.
- **Zero steady-state error (proved).** If the closed loop converges for a constant $r$ and the output is not held at a limit, then $y$ converges to $r$. The claim needs integral action. It does not say that the loop converges; that depends on the plant and the tuning.
- **Back-calculation (proved).** While the output is held at a limit with a constant error $e$, and $0 < h/T_t < 2$, the integral converges geometrically and $v$ tends to $u_{\max} + (T_t/T_i) K e$. Without tracking the integral grows without bound.
- **Forms (proved).** The series form converts to the ideal form, and an ideal form has a real series form if and only if $T_i \ge 4 T_d$.
- **Convergence as $h \to 0$ (measured).** The tests show the first order convergence of the sampled loop to the continuous loop on the example plant. The proof proves only that each update is a first order Euler step.

## Complexity

One call does a fixed number of operations: at most 10 multiplications, 10 additions and 2 comparisons, and line L1 adds 6 operations once. The state is three numbers, $I$, $D$ and $e_{\text{old}}$. So $k$ samples cost $O(k)$ time and $O(1)$ extra space. This fixed cost per sample is one reason that PID control runs on the smallest processors. A closed-loop simulation costs the number of integration steps times the cost of one step of the plant model.

## Properties

- **Online.** Each output uses only the present and past samples.
- **Not exact.** The algorithm is exact for its own difference equations, but it approximates the continuous controller with an error of order $h$.
- **Linear inside the limits.** Without saturation, the controller is a linear time-invariant discrete system of order 2 (one integrator state and one filter state).
- **Proper.** The filter makes the derivative part proper. Its gain at high frequency is $K N$ in place of infinity.
- **Fixed structure.** Only two zeros and a pole at the origin can be placed. Plants with large delays, many oscillatory modes or strong coupling need other structures.

## Variants and improvements

- **PI and PD.** With $T_d = 0$ the controller is PI, the most common case in process control. Without integral action it is PD, used where the plant has an integrator, as in positioning.
- **Velocity form.** Compute the change $\Delta u_k = u_k - u_{k-1}$ and add it to the previous output. The integral is then implicit, and windup protection only needs a limit on the integrated output. This form is common in programmable controllers.
- **Second order filter.** Filter the measurement with $1/(1 + s T_f)^2$ before the controller, in place of the filter on the derivative only. This gives a roll-off of the whole controller at high frequency.
- **Gain scheduling.** Change $K$, $T_i$ and $T_d$ with an operating variable. See [gain scheduling](/gain-scheduling/).
- **Tuning.** The parameters come from rules such as [Ziegler-Nichols tuning](/ziegler-nichols-tuning/), from an experiment with [relay autotuning](/relay-autotuning/), from [internal model control](/internal-model-control/), or from [loop shaping](/loop-shaping/).
- **Other discretizations.** The Tustin approximation of the whole controller is also used; see [controller discretization](/controller-discretization/).
- **Structures.** PID controllers are the building blocks of [cascade control](/cascade-control/), [feedforward control](/feedforward-control/) and the [Smith predictor](/smith-predictor/).

## When to use it

Use a PID controller for a single loop where the plant has dominant dynamics of first or second order, perhaps with a short delay, and where the aim is to hold the output at a set point against loads. Most flow, pressure, level, temperature and speed loops are of this kind. Use PI when the measurement is noisy or the plant is close to first order. Add the derivative when the plant has two lags of similar size or when the loop must be fast. Use another design when the delay is long compared with the time constants, when several loops interact strongly (see [relative gain array](/relative-gain-array/)), or when constraints must be handled in a planned way, as in [model predictive control](/model-predictive-control/).

## Pitfalls

- **Unfiltered derivative.** The ideal derivative amplifies measurement noise without limit. Always filter it, and choose $N$ so that the noise in $u$ is acceptable.
- **Derivative kick.** With $c = 1$ a step in the set point gives an impulse in $u$. Use $c = 0$ unless the set point is smooth.
- **Windup.** If the actuator saturates and nothing stops the integral, the integral grows during the saturation, and the overshoot afterwards can be large. Use tracking or conditional integration.
- **Forms differ.** The same three numbers give different controllers in the ideal, series and parallel forms. Convert the parameters before moving a tuning to another product.
- **Sign of the action.** If the plant gain is negative, the controller must use the reverse action. A wrong sign gives positive feedback.
- **Bumpless transfer.** When the operator moves from manual to automatic, set the integral so that $v$ equals the present manual output. Otherwise the output jumps.
- **Sampling.** The hold adds a delay of about $h/2$, which reduces the phase margin by about $\omega_c h/2$ radians at the crossover frequency $\omega_c$. Take many samples per closed-loop rise time, and check the margins of the sampled loop. The example shows how the overshoot grows with $h$.

## Implementations

## History

Nicolas Minorsky studied the automatic steering of ships and published in 1922 an analysis that recommended a steering law with proportional, integral and derivative terms. Pneumatic process controllers with proportional and reset (integral) action came into use in the 1930s, and the derivative action was added under the name pre-act. Ziegler and Nichols used these terms in 1942, when they gave the first tuning rules. Electronic analog controllers and then computer controllers replaced most of the pneumatic ones. The computer made it easy to add the filter, the set-point weights, anti-windup and automatic tuning. Åström and Hägglund describe this development and the modern form of the algorithm.

## References
