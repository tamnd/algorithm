---
tag: KDGAXT
kind: technique
slug: feedforward-control
name: Feedforward control
aliases:
- feedforward compensation
- disturbance feedforward
area: control/classical-control
level: intro
summary: Adds a control term computed from the reference or from a measured disturbance, so the loop acts before an error appears.
prereqs: [feedback-control-loop, sensitivity-function]
see_also: [two-degree-of-freedom-control, cascade-control, pid-controller, internal-model-control, smith-predictor, disturbance-observer, lead-lag-compensator, model-predictive-control]
sources:
  - book: isbn:9781556179426
    title: Karl Johan Åström and Tore Hägglund, Advanced PID Control, ISA, 2006
    locator: the whole book (feedforward from measured disturbances and from the set point)
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, second edition, Princeton University Press, 2021
    locator: the whole book (feedforward and two-degree-of-freedom structures)
---

Feedforward control adds to the feedback signal a term that is computed from a signal the controller knows in advance: a measured disturbance $d$, or the reference $r$. If $d$ acts on the output through $P_d$ and the actuator acts through $P$, the term $u_{ff} = F d$ with $F = -P_d/P$ cancels the effect of $d$ before any error appears. Feedback cannot do this, because it acts only on an error that has already happened. In practice $F$ is not exact or not realizable, so feedforward is always used together with feedback, which removes what is left. Feedforward does not change the poles of the closed loop, so it cannot destroy internal stability when $F$ is BIBO stable.

## In plain words

A feedback controller waits until the output is wrong and then corrects it. If you can measure a disturbance when it happens, you can correct for it at once, before the output moves. For example, if more cold water flows into a tank, you can open the heater more at the same moment instead of waiting for the temperature to drop. The correction is computed from a model: how strongly the disturbance pushes the output, and how strongly the actuator pushes back. A perfect correction needs a perfect model and an actuator that is at least as fast as the disturbance. Neither is ever true, so feedback stays in the loop to clean up what the correction misses. Feedforward costs a sensor and a model, but it does not make the loop oscillate.

## When it applies

- A disturbance $d$ can be measured before or when it acts, and its effect $P_d$ on the output is known with a fair model.
- The actuator path $P$ is not slower than the disturbance path $P_d$, or a static correction is enough.
- Feedback alone is too slow, for example because the plant has a long delay or because the loop gain is limited by robustness.
- For the reference: the set point changes in known ways, and a model of the plant gives the input that makes the output follow it.

## The template

1. **Model the two paths.** Find $P(s)$ from $u$ to $y$ and $P_d(s)$ from $d$ to $y$, for example by step tests.
2. **Compute the ideal compensator** $F = -P_d/P$.
3. **Make it realizable.**
   - If $F$ is improper, add a filter: a lead-lag $-P_d/(P (T_f s + 1)^k)$.
   - If $P$ has a longer delay than $P_d$, the ideal $F$ needs a prediction. Drop the difference of the delays.
   - If $P$ has a zero in the right half-plane, $F$ would have an unbounded response. Invert only the minimum phase part.
   - The simplest choice is the static gain $F = -P_d(0)/P(0)$.
4. **Add it to the feedback.** $u = C (r - y) + F d$. Keep integral action in $C$ for the model error and the disturbances that are not measured.
5. **Check the residual.** Simulate a step of $d$ with the model error you expect.

**Why it works (theorems).** With $S = 1/(1 + P C)$, the loop gives

$$y = (P_d + P F) S \, d.$$

If $F = -P_d/P$, the effect of $d$ is zero for every $C$. Otherwise feedback reduces the residual $P_d + P F$ by the factor $S$. The characteristic equation $1 + P C = 0$ does not contain $F$, so a BIBO stable $F$ leaves the closed-loop poles and the internal stability unchanged. With a relative model error, $P_d + P F = P_d \epsilon$ when $F = -P_d (1 - \epsilon)/P$, so a 10 percent error in the gain of $F$ leaves 10 percent of the disturbance, before feedback.

## Classic examples

**Two lags.** Let $P = 1/(s + 1)^2$, $P_d = 1/(s + 1)$, a unit step of $d$, and the PI controller $K = 1$, $T_i = 1$, so $P C = 1/(s(s + 1))$. The ideal $F = -(s + 1)$ is improper. Use the static $F = -1$ or the lead-lag $F = -(s + 1)/(0.1 s + 1)$.

Feedback only, by hand: $y = 1/(s^2 + s + 1) \cdot d$, so for a unit step

$$y(t) = \frac{2}{\sqrt 3} e^{-t/2} \sin\frac{\sqrt 3 t}{2},$$

with the peak $e^{-\pi/(3\sqrt 3)} = 0.5463$ at $t = 2\pi/(3\sqrt 3) = 1.209$ and the integral of the error equal to 1.

Feedforward only, by hand: with $F = -1$, $P_d + P F = s/(s + 1)^2$ and $y = t e^{-t}$, with the peak $1/e = 0.368$ at $t = 1$. With the lead-lag, $P_d + P F = 0.1 s/((s + 1)(0.1 s + 1))$ and $y = (e^{-t} - e^{-10t})/9$, with the peak 0.0774 at $t = \ln 10/9 = 0.256$ and the integral 0.1.

Measured with a simulation step of 0.001 s, with feedback:

| structure | peak of $y$ | time of the peak | IAE over 30 s |
|---|---|---|---|
| feedback only | 0.5463 | 1.209 s | 1.390 |
| static feedforward and feedback | 0.315 | 0.74 s | 0.921 |
| lead-lag feedforward and feedback | 0.0761 | 0.241 s | 0.130 |

The lead-lag reduces the peak by a factor of about 7 and the IAE by a factor of more than 10. Feedback lowers the peak of the lead-lag case only a little (from 0.0774 to 0.0761), because the residual is fast compared with the loop.

**Reference feedforward.** For a reference $r$ filtered by a model $M$ (a desired response), the term $u_{ff} = (M/P) r$ makes $y = M r$ with an exact model, and the feedback acts only on $M r - y$. This is a [two-degree-of-freedom](/two-degree-of-freedom-control/) structure. It needs $M/P$ to be proper and BIBO stable, so $M$ must keep the delay and the zeros in the right half-plane of $P$.

## Variations

- **Static feedforward.** A gain only, often with a ratio to a measured flow. It removes the steady effect of $d$ and some of the transient.
- **Dynamic feedforward.** A lead-lag, or a full inverse with a filter, for the transient.
- **Feedforward to an inner loop.** In a [cascade](/cascade-control/), feed the disturbance to the inner set point, where the inner loop handles the actuator.
- **Gain scheduling of $F$.** If $P$ and $P_d$ change with the operating point, schedule $F$ too.
- **Estimated disturbances.** If $d$ is not measured, a [disturbance observer](/disturbance-observer/) can estimate it, and the estimate is fed forward. This adds feedback again, and the loop poles change.
- **Prediction.** [Model predictive control](/model-predictive-control/) uses a model and known future references or disturbances to plan the input.

## Pitfalls

- **Model error.** Feedforward reduces a disturbance only as much as the model allows. Keep feedback with integral action.
- **Delay mismatch.** If the actuator acts later than the disturbance, no causal $F$ cancels it. A static gain with the right sign still helps.
- **Inverse of a zero in the right half-plane.** It makes $F$ have a growing response. Use the minimum phase part only.
- **Large lead.** A large ratio of lead to lag in $F$ gives large peaks of $u$ and can saturate the actuator. A saturated actuator gives no cancellation; see [anti-windup](/anti-windup/).
- **Noise on the measured disturbance.** A dynamic $F$ with a high gain at high frequencies passes the noise to the actuator.
- **Sign and units.** A wrong sign doubles the disturbance. Test with a small gain first.

## Exercises

1. Compute the ideal $F$ for $P = 1/(s + 1)^2$ and $P_d = 1/(s + 1)$. (Answer: $F = -(s + 1)$, which is improper.)
2. Without feedback and with $F = -1$, find the response to a unit step of $d$. (Answer: $y = t e^{-t}$, peak $1/e$ at $t = 1$.)
3. With the lead-lag $F = -(s + 1)/(0.1 s + 1)$ and no feedback, find the integral of $y$. (Answer: $y = (e^{-t} - e^{-10t})/9$, and the integral is $(1 - 0.1)/9 = 0.1$.)
4. Show that $F$ does not change the closed-loop poles. (Answer: $y = (P_d + P F) S d + T r$, and $F$ does not appear in $1 + P C$.)
5. Let $P = e^{-2s}/(s + 1)$ and $P_d = e^{-s}/(s + 1)$. What is the ideal $F$, and what can you use instead? (Answer: $F = -e^{s}$ needs a prediction of 1 s; use the static $F = -1$, which acts 1 s late.)

## References
