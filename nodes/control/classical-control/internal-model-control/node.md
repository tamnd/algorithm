---
tag: AJSRRM
kind: technique
slug: internal-model-control
name: Internal model control
aliases:
- IMC
area: control/classical-control
level: core
summary: A controller structure that runs a model of the plant in parallel and inverts its invertible part with a filter, which gives PID tuning rules.
prereqs: [feedback-control-loop, time-delay-system, complementary-sensitivity-function]
see_also: [internal-model-principle, smith-predictor, pid-controller, youla-parametrization, model-uncertainty, two-degree-of-freedom-control, small-gain-theorem, model-predictive-control]
sources:
  - paper: doi:10.1021/i200017a016
    title: Carlos E. Garcia and Manfred Morari, Internal model control. 1. A unifying review and some new results, Industrial and Engineering Chemistry Process Design and Development 21(2) (1982) 308-323
    locator: the whole paper (the structure, the stability result and the design by inversion with a filter)
  - paper: doi:10.1021/i200032a041
    title: "Daniel E. Rivera, Manfred Morari and Sigurd Skogestad, Internal model control: PID controller design, Industrial and Engineering Chemistry Process Design and Development 25(1) (1986) 252-265"
    locator: the whole paper (PID settings from IMC)
  - book: isbn:978-0-13-782153-2
    title: Manfred Morari and Evanthia Zafiriou, Robust Process Control, Prentice Hall, 1989
    locator: the whole book (IMC design and robustness for single and multivariable plants)
  - paper: doi:10.1016/S0959-1524(02)00062-8
    title: Sigurd Skogestad, Simple analytic rules for model reduction and PID controller tuning, Journal of Process Control 13(4) (2003) 291-309
    locator: the whole paper (the SIMC rules)
---

Internal model control (IMC) is a controller structure in which the controller contains a model $\tilde P$ of the plant. The model gets the same input as the plant, and the controller $Q$ acts on the difference between the measured output and the model output. Do not confuse it with the [internal model principle](/internal-model-principle/): that principle says a regulator must contain a model of the signals it rejects (for example an integrator for steps), while IMC puts a model of the plant into the controller. With an exact model, the loop has the simple closed-loop map $T = \tilde P Q$, so the design is an inversion of the plant with a low-pass filter. One tuning parameter, the filter time constant $\lambda$, trades speed for robustness, and for simple models the result is a PI or PID controller.

## In plain words

The controller keeps a copy of the plant in its memory and feeds it the same commands as the real plant. If the copy is perfect and nothing disturbs the plant, the real output and the copy agree, and the controller only has to send the right command, which it gets by running the plant backward. A disturbance makes the real output differ from the copy, and the controller sees exactly the effect of the disturbance and acts on it. Running a plant backward is not always possible: a delay cannot be undone, and some plants first move the wrong way. The method keeps those parts and inverts the rest. A filter slows the result, and its single time constant is the tuning knob. For many common plants the result is a normal PI or PID controller with simple formulas.

## When it applies

- The plant is BIBO stable, or it can be made so by an inner loop, and a model $\tilde P$ with a gain, time constants and a delay is known.
- One parameter for tuning is wanted, with a direct meaning: $\lambda$ is about the closed-loop time constant.
- PI or PID settings are wanted from a first or second order model with delay. The IMC rules and the SIMC rules of Skogestad (2003) come from this structure.
- The plant has a long delay. With a delay in the model, IMC is the [Smith predictor](/smith-predictor/).

## The template

1. **Model.** Choose a BIBO stable model $\tilde P(s)$.
2. **Factor.** Write $\tilde P = \tilde P_+ \tilde P_-$. The factor $\tilde P_+$ holds the delay and the zeros in the right half-plane as an all-pass part with $\tilde P_+(0) = 1$, for example $e^{-\theta s}$ or $(1 - s)/(1 + s)$. The factor $\tilde P_-$ is minimum phase.
3. **Invert and filter.** Set
   $$Q(s) = \tilde P_-(s)^{-1} f(s), \qquad f(s) = \frac{1}{(\lambda s + 1)^n},$$
   with the smallest $n$ that makes $Q$ proper.
4. **Implement.** Either run the IMC structure, $u = Q (r - (y - \tilde P u))$, or use the equivalent classical controller
   $$C(s) = \frac{Q(s)}{1 - \tilde P(s) Q(s)}.$$
5. **Tune $\lambda$.** Start near the delay $\theta$ or near the dominant time constant, and increase $\lambda$ until the robustness test below holds for the expected model error.

**Why it works (theorems).** With an exact model $\tilde P = P$, the signal $y - \tilde P u$ equals the output disturbance $d$, so the loop has

$$T = \tilde P Q = \tilde P_+ f, \qquad S = 1 - \tilde P Q.$$

For a BIBO stable plant and an exact model, the loop is internally stable if and only if $Q$ is BIBO stable. This is why $Q$ must not invert $\tilde P_+$: the inverse of a zero in the right half-plane gives a pole of $Q$ there, and the inverse of a delay is not causal. Since $f(0) = 1$ and $\tilde P_+(0) = 1$, $T(0) = 1$ and $S(0) = 0$, so the steady-state error to a step is zero. For a model error $P = \tilde P (1 + \Delta)$ with $\Delta$ BIBO stable, the loop is $Q$ in feedback with $(P - \tilde P) = \tilde P \Delta$. By the [small gain theorem](/small-gain-theorem/) it stays internally stable if

$$|\tilde T(j\omega) \Delta(j\omega)| < 1 \quad \text{for all } \omega, \qquad \tilde T = \tilde P Q.$$

A larger $\lambda$ makes $\tilde T$ smaller at high frequencies, where $\Delta$ is large, so it buys robustness. For a BIBO stable plant, $Q \mapsto C$ is the [Youla parametrization](/youla-parametrization/) of all controllers that make the loop internally stable.

## Classic examples

**A first order plant gives a PI controller.** Let $P = K/(\tau s + 1)$. Then $\tilde P_+ = 1$, $Q = (\tau s + 1)/(K(\lambda s + 1))$, $T = 1/(\lambda s + 1)$ and

$$C = \frac{Q}{1 - P Q} = \frac{\tau s + 1}{K \lambda s},$$

a PI controller with $K_c = \tau/(K\lambda)$ and $T_i = \tau$.

**A delay gives the Smith predictor or a PI approximation.** Let $P = K e^{-\theta s}/(\tau s + 1)$. Then $\tilde P_+ = e^{-\theta s}$, $Q$ is the same as above, and $T = e^{-\theta s}/(\lambda s + 1)$. The exact $C$ is the Smith predictor around the PI controller $K_c = \tau/(K\lambda)$, $T_i = \tau$. If $e^{-\theta s} \approx 1 - \theta s$ in the denominator of $C$, then $1 - P Q \approx (\lambda + \theta) s/(\lambda s + 1)$ and

$$C \approx \frac{\tau s + 1}{K (\lambda + \theta) s}, \qquad K_c = \frac{\tau}{K(\lambda + \theta)}, \quad T_i = \tau.$$

This is the PI rule of Rivera et al. (1986) and the first part of the SIMC rule; SIMC adds $T_i = \min(\tau, 4(\lambda + \theta))$ (Skogestad 2003). Measurements for $P = e^{-s}/(s + 1)$, a sampled loop with $h = 0.01$ s, a unit set-point step and a unit load step at the plant input:

| $\lambda$ | exact IMC: settling time (2 percent) | PI approximation: overshoot, settling time | integral of the load error, both | peak of the load error: IMC, PI | first plant delay that fails: IMC, PI |
|---|---|---|---|---|---|
| 0.5 s | 2.93 s | 0.179, 7.48 s | 1.5 | 0.667, 0.709 | 2.15 s, 1.85 s |
| 1 s | 4.88 s | 0.043, 6.14 s | 2.0 | 0.694, 0.726 | 2.55 s, 2.35 s |
| 2 s | 8.79 s | 0, 7.81 s | 3.0 | 0.732, 0.753 | 3.30 s, 3.10 s |

The exact IMC loop has no overshoot. Its settling time is near the formula $\theta + \lambda \ln 50$ (2.956 s, 4.912 s and 8.824 s), and the sampled loop is a little faster. The integral of the load error is $\lambda + \theta$ in both loops, as theory says: for the PI loop it is $T_i/K_c = K(\lambda + \theta)$, and for the IMC loop it is $T_i/K_c + K\theta = K(\lambda + \theta)$, as on the Smith predictor page. In the last column the model delay stays 1 s, the plant delay grows in steps of 0.05 s, and the entry is the first value at which the loop does not converge. A larger $\lambda$ accepts a larger delay error, as the robustness test says.

**A zero in the right half-plane gives a PID controller.** Let $P = (1 - s)/(s + 1)^2$. Then $\tilde P_+ = (1 - s)/(1 + s)$, $\tilde P_- = 1/(s + 1)$, $Q = (s + 1)/(\lambda s + 1)$ and $T = (1 - s)/((s + 1)(\lambda s + 1))$. The equivalent controller is

$$C = \frac{(s + 1)^2}{s (\lambda s + \lambda + 2)},$$

a PID controller in series form with gain $1/(\lambda + 2)$, $T_i = T_d = 1$ and a derivative filter with time constant $\lambda/(\lambda + 2)$. The inverse response of $T$ remains: no BIBO stable $Q$ removes it.

## Variations

- **IMC-PID rules.** Rivera et al. (1986) give PI and PID settings from IMC for first and second order models, with and without delay.
- **SIMC.** Skogestad (2003) reduces a model to first or second order with delay by the half rule and uses $\tau_c = \lambda$ with $T_i = \min(\tau, 4(\tau_c + \theta))$. The choice $\tau_c = \theta$ is a rule of thumb for a good balance of speed and robustness.
- **Smith predictor.** For a model with delay, the exact IMC controller is the [Smith predictor](/smith-predictor/).
- **Two degrees of freedom.** Use one filter for the set point and another for the disturbance, which is a [two-degree-of-freedom](/two-degree-of-freedom-control/) design.
- **Plants that are not BIBO stable.** The IMC structure needs a BIBO stable model. For an integrating plant or a pole in the right half-plane, design $Q$ with extra interpolation conditions and implement the classical $C$ only.
- **Constraints.** If the model gets the limited actuator signal and the model is exact, the feedback signal is $d$ and does not depend on the limit, so $Q$ acts in open loop and nothing winds up. With a model error this is only an approximation. [Model predictive control](/model-predictive-control/) puts the limits into an optimization and uses the same idea of a model running in parallel.
- **Multivariable plants.** The same factorization and filter apply to a [transfer function matrix](/transfer-function-matrix/), with more care in the choice of $\tilde P_+$ (Morari and Zafiriou 1989).

## Pitfalls

- **Slow load response.** The PI rule with $T_i = \tau$ cancels the plant pole. With $P = K/(\tau s + 1)$ and $C = (\tau s + 1)/(K\lambda s)$, the map from a load at the plant input to the output is $K \lambda s/((\tau s + 1)(\lambda s + 1))$, which still has the pole $-1/\tau$. For $\tau \gg \lambda$ a load decays slowly. This is why SIMC limits $T_i$ to $4(\tau_c + \theta)$.
- **Inverting the wrong part.** Putting a zero in the right half-plane into $\tilde P_-$ gives a $Q$ with a pole there, and the loop is not internally stable even with an exact model.
- **Too small $\lambda$.** The robustness test fails when $\lambda$ is small compared with the model error, mostly the error in the delay. The table shows that the PI approximation also loses some delay margin.
- **Running the structure on an integrating plant.** The model output then drifts with any offset in the actuator signal. Use the classical form $C$.
- **Noise.** A $Q$ with a high order of inversion has a high gain at high frequencies when $\lambda$ is small. Choose $n$ and $\lambda$ with the noise in mind.

## Exercises

1. Give the IMC PI settings for $P = 2/(5s + 1)$ with $\lambda = 1$ s. (Answer: $K_c = 5/(2 \cdot 1) = 2.5$, $T_i = 5$ s.)
2. Give the PI approximation for $P = 2 e^{-s}/(5s + 1)$ with $\lambda = 1$ s, and check the SIMC limit on $T_i$. (Answer: $K_c = 5/(2 \cdot 2) = 1.25$, $T_i = \min(5, 8) = 5$ s.)
3. Derive $C$ for $P = (1 - s)/(s + 1)^2$ and $Q = (s + 1)/(\lambda s + 1)$. (Answer: $1 - PQ = (\lambda s^2 + (\lambda + 2) s)/((s + 1)(\lambda s + 1))$, so $C = (s + 1)^2/(s(\lambda s + \lambda + 2))$.)
4. Why is $Q = (s + 1)^2/((1 - s)(\lambda s + 1))$ not allowed for the plant of Exercise 3? (Answer: $Q$ has the pole $s = 1$, so it is not BIBO stable and the loop is not internally stable.)
5. With an exact model and $T = e^{-\theta s}/(\lambda s + 1)$, when does the step response enter the 2 percent band? (Answer: $1 - e^{-(t - \theta)/\lambda} = 0.98$, so $t = \theta + \lambda \ln 50$.)

## References
