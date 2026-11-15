---
tag: Q6KE5W
kind: technique
slug: two-degree-of-freedom-control
name: Two-degree-of-freedom control
aliases:
- 2DOF control
- setpoint weighting
area: control/classical-control
level: core
summary: A controller that treats the reference and the measured output by separate paths, so tracking and disturbance rejection are tuned apart.
prereqs: [feedback-control-loop, sensitivity-function, complementary-sensitivity-function]
see_also: [pid-controller, feedforward-control, internal-model-control, loop-shaping, anti-windup, reference-governor, model-predictive-control, cascade-control]
sources:
  - book: "Isaac M. Horowitz, Synthesis of Feedback Systems, Academic Press, 1963"
    title: Isaac M. Horowitz, Synthesis of Feedback Systems, Academic Press, 1963
    locator: the whole book (the two-degree-of-freedom structure)
  - book: isbn:9781556179426
    title: Karl Johan Åström and Tore Hägglund, Advanced PID Control, ISA, 2006
    locator: Chapter 3, PID Control (set-point weighting)
---

A two-degree-of-freedom (2DOF) controller computes the input from the reference $r$ and the measured output $y$ by two different transfer functions, $u = C_r r - C_y y$. A one-degree-of-freedom controller has $C_r = C_y$, so it acts only on the error $r - y$. The feedback part $C_y$ alone sets the closed-loop poles, the [sensitivity function](/sensitivity-function/) and the response to disturbances and noise. The part $C_r$ then shapes the response to the reference without changing any of those. Horowitz (1963) is the classic reference for the structure. The simplest form is set-point weighting in a [PID controller](/pid-controller/): a weight $b$ on the reference in the proportional term.

## In plain words

A normal controller looks only at the error, the difference between what you want and what you have. So a jump of the set point and a sudden disturbance look the same to it, and one tuning must serve both. Often a tuning that removes disturbances fast gives a large overshoot after a set-point step. A two-degree-of-freedom controller uses the set point and the measurement in different ways. The part that acts on the measurement is tuned for disturbances and robustness. The part that acts on the set point is then tuned for a smooth and fast set-point response. The second part changes nothing in how the loop reacts to disturbances, so the two jobs are tuned apart.

## When it applies

- The loop must both track set-point changes and reject loads, and one tuning cannot do both well. This is common when the feedback is tuned for load rejection.
- Set-point steps cause large kicks of the input or a large overshoot.
- A model of the plant is available for a reference model and a feedforward term, or only a PID controller is available and set-point weights are the tool.

## The template

1. **Design the feedback** $C_y$ for disturbance rejection, noise and robustness, for example by [loop shaping](/loop-shaping/) or a PID tuning rule.
2. **Choose the reference path.** Common forms:
   - *Set-point weighting in PID:* $u = K\left(b r - y + \frac{1}{T_i}\int (r - y)\,dt + T_d \frac{d}{dt}(c r - y)\right)$, with $0 \le b \le 1$ and usually $c = 0$.
   - *Prefilter:* $u = C_y (F r - y)$.
   - *Reference model and feedforward:* $u = (M/P) r + C_y (M r - y)$, with a desired response $M$.
3. **Keep the integral on the true error.** The integral term must act on $r - y$, so that the steady-state error is zero for every choice of the reference path.
4. **Tune the reference path** with the feedback fixed: lower $b$, or a slower $F$ or $M$, gives less overshoot and a smaller kick of $u$.

**Why it works (theorems).** With a load $d$ at the plant input, $u = C_r r - C_y y$ and $y = P(u + d)$,

$$y = \frac{P C_r}{1 + P C_y} r + \frac{P}{1 + P C_y} d.$$

The denominator and the map from $d$ contain only $C_y$, so the closed-loop poles, the internal stability and the load response do not depend on $C_r$ (when $C_r$ is BIBO stable, or when $C_r$ and $C_y$ share one integrator, as in the PID form). For the PI controller with weight $b$,

$$C_r = K\left(b + \frac{1}{T_i s}\right), \quad C_y = K\left(1 + \frac{1}{T_i s}\right), \quad \frac{C_r}{C_y} = \frac{b T_i s + 1}{T_i s + 1},$$

which equals 1 at $s = 0$. So the weight acts as a prefilter that moves the controller zero from $-1/T_i$ to $-1/(b T_i)$, and the steady-state error to a step is zero for every $b$. For the reference model form with an exact model, $y = M r$ and the feedback sees no error.

## Classic examples

**A PI controller on three lags.** Let $P = 1/(s + 1)^3$ and the PI controller $K = 1.65646$, $T_i = 4.47205$ from the [loop shaping](/loop-shaping/) page (a phase margin of 60 degrees). Measured with a simulation step of 0.01 s, for a unit set-point step and, separately, a unit load step at the plant input:

| weight $b$ | overshoot | settling time (2 percent) | time to 90 percent | IAE of the set-point step |
|---|---|---|---|---|
| 0 | 0 | 24.64 s | 14.97 s | 7.176 |
| 0.5 | 0 | 21.89 s | 11.88 s | 4.941 |
| 1 | 0.043 | 16.11 s | 2.89 s | 2.781 |

The load response is the same for all three values of $b$: the peak of $y$ is 0.43861, and the integral of the error is 2.6996, which matches the theorem $T_i/K = 2.6998$ to the accuracy of the simulation. On this plant $b = 1$ gives the fastest set-point response with a small overshoot. A low $b$ removes the kick of $u$ at the step: $u(0^+) = b K$, which is 1.656 for $b = 1$ and 0 for $b = 0$. The example shows that the weight changes only the set-point response; whether a low $b$ helps depends on the feedback tuning.

**Reference model with feedforward.** For $P = 1/(s + 1)^3$ and $M = 1/(0.5 s + 1)^3$, the feedforward is $u_{ff} = (M/P) r = (s + 1)^3/(0.5 s + 1)^3 \, r$, and the output follows $M$ exactly when the model is exact. A unit step gives $u_{ff}(0^+) = 8$, so the desired response must respect the actuator limits.

## Variations

- **Set-point weights $b$ and $c$** in the PID controller: $c = 0$ (derivative on the measurement) is the usual choice and avoids a derivative kick.
- **Prefilter** $F$ on the reference, of any order, with $F(0) = 1$.
- **Feedforward with a reference model**, as in the template; it needs $M/P$ proper and BIBO stable, so $M$ must keep the delay and the zeros of $P$ in the right half-plane. See [feedforward control](/feedforward-control/).
- **IMC with two filters.** In [internal model control](/internal-model-control/) use one filter for the reference and another for the disturbance.
- **Reference shaping.** Ramp or filter the set point, or use a [reference governor](/reference-governor/) to respect constraints.
- **Quantitative feedback theory.** Horowitz's design method uses the two degrees of freedom to meet bounds on the response for a set of plants.

## Pitfalls

- **Integral on the weighted error.** If the integral acts on $b r - y$, the steady-state error is not zero for $b \neq 1$. The integral must act on $r - y$.
- **Expecting better disturbance rejection.** The reference path cannot improve the response to loads or noise; only $C_y$ can.
- **Bumps at mode changes.** A change of $b$ during operation changes $u$ at once. Change the weights with the integral adjusted, as for bumpless transfer.
- **Saturation.** A fast $M$ or a large $b$ makes $u$ large right after a step. Then the actuator saturates; see [anti-windup](/anti-windup/).
- **Model error in the feedforward form.** With a model error, the feedback sees $M r - y \neq 0$ and corrects it; the response is then between $M$ and the one-degree-of-freedom response.

## Exercises

1. Give the prefilter $F$ that is equivalent to the weight $b$ in a PI controller. (Answer: $F = (b T_i s + 1)/(T_i s + 1)$.)
2. Show that the load response does not depend on $b$. (Answer: $y/d = P/(1 + P C_y)$ and $C_y$ does not contain $b$.)
3. Show that the steady-state error to a step is zero for every $b$. (Answer: $C_r/C_y \to 1$ as $s \to 0$, so $y/r \to 1$ when the loop has integral action.)
4. In the example, what is the jump of $u$ at a unit set-point step for $b = 0.5$? (Answer: $b K = 0.828$.)
5. What is $u_{ff}(0^+)$ for $M = 1/(0.5 s + 1)^3$ and $P = 1/(s + 1)^3$? (Answer: the ratio of the leading coefficients, $1/0.5^3 = 8$.)

## References
