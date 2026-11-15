---
tag: V0A2FW
kind: problem
slug: closed-loop-identification
name: Closed-loop identification
aliases:
- identification in closed loop
area: control/modeling-and-identification
level: advanced
summary: Identify a plant from data taken while a feedback controller runs, where the input is correlated with the noise.
model: real-ram
complexity:
  vars: {N: the number of samples, d: the number of parameters}
  time: {worst: O(N d^2 + d^3)}
prereqs: [prediction-error-method, instrumental-variable-identification, persistent-excitation]
see_also: [feedback-control-loop, sensitivity-function, system-identification, output-error-model, arx-model, prbs-input, adaptive-control, self-tuning-regulator]
sources:
  - book: isbn:9780136566953
    title: "Lennart Ljung, System Identification: Theory for the User, second edition, Prentice Hall, 1999"
    locator: "Chapter 13, Section 13.4 (identification in closed loop: identifiability, informative experiments and the direct, indirect and joint input-output approaches)"
  - paper: "Urban Forssell and Lennart Ljung, Closed-loop identification revisited, Automatica 35(7), 1215-1241, 1999"
    locator: "the classification into direct, indirect and joint input-output methods, and their bias and variance"
  - paper: "Ivar Gustavsson, Lennart Ljung and Torsten Söderström, Identification of processes in closed loop: identifiability and accuracy aspects, Automatica 13(1), 59-75, 1977"
    locator: the identifiability of systems under feedback, with and without an external signal
  - book: isbn:9780138812362
    title: "Torsten Söderström and Petre Stoica, System Identification, Prentice Hall, 1989"
    locator: the chapter on identification of systems operating in closed loop
---

Closed-loop identification is the problem of building a model of a plant from data recorded while a feedback controller is running. The controller computes the input $u$ from the measured output $y$, so $u$ is correlated with the disturbances that act on $y$. Many methods that are consistent in open loop then fail: correlation and spectral analysis, output error fits and instrumental variables with past inputs as instruments can all converge to a wrong plant, and with no external excitation the data may not determine the plant at all. The problem is common because many plants cannot be run without their controllers for safety or economic reasons. The known answers are conditions under which a method is consistent. The direct prediction error method is consistent when the model set contains both the true plant and the true noise model and the data are informative. The indirect methods use a known controller or a measured reference signal instead.

## In plain words

You want to learn how a machine responds to its input, but a controller is already holding it steady. Whenever a disturbance pushes the output up, the controller pushes the input down. In the record, the input and the disturbance move together, so it is hard to tell how much of the output came from the input and how much from the disturbance. In the worst case the record would look the same for many different machines. Two things help. You can add a small known test signal to the setpoint, which moves the input for reasons that have nothing to do with the disturbance. And you can use a method that models the disturbance as well, so that its effect is not blamed on the input.

## Definition

Time is discrete, $k = 1, \ldots, N$, with sampling period $h$ and shift operator $q$. The data come from the loop

$$y(k) = G_0(q)\, u(k) + H_0(q)\, e(k), \qquad u(k) = r(k) - K(q)\, y(k),$$

where $e$ is white noise, $r$ is an external signal independent of $e$ (a setpoint change or an added test signal), and the controller $K$ is linear. The loop must be well posed, which holds if $G_0 K$ has a delay, and internally BIBO stable. With the sensitivity function $S_0 = 1/(1 + G_0 K)$,

$$y = S_0 G_0\, r + S_0 H_0\, e, \qquad u = S_0\, r - K S_0 H_0\, e.$$

The second equation shows the difficulty: unless $K = 0$, $u$ depends on $e$.

**The question.** Given $\{y(k), u(k)\}$, and possibly $r$ or $K$, and a model set $\{G(q, \theta), H(q, \theta)\}$, return an estimate $\hat\theta_N$ such that $G(q, \hat\theta_N)$ converges to $G_0$, or, when $G_0$ is not in the model set, to an approximation with a known frequency weighting. The noise model $H$ may or may not be of interest.

**Informative data.** The closed-loop data are informative for the model set if two models that give the same limit prediction errors on them have the same $G$ and $H$ (Ljung 1999, Section 13.4). A [persistently exciting](/persistent-excitation/) $u$ is not enough, because $u$ may be a filter of $y$.

## Variants

- **Known or unknown controller.** The indirect methods need $K$ exactly. The direct method does not use it.
- **Measured or absent reference.** With $r = 0$ the only excitation is the noise, and the data are informative only for some controllers. With a measured $r$, the joint input-output and two-stage methods become available.
- **Linear or nonlinear, fixed or time-varying feedback.** A time-varying or nonlinear controller, or switching between two linear controllers, can make the data informative even with $r = 0$.
- **Consistency of $G$ only.** In some uses only the plant matters; then methods that do not need a correct noise model are preferred.
- **Recursive closed-loop identification.** The [self-tuning regulator](/self-tuning-regulator/) and other [adaptive controllers](/adaptive-control/) identify the plant online while their own feedback acts on it.

## Examples

1. **No external signal (theorem).** For $y(k) + a\, y(k-1) = b\, u(k-1) + e(k)$ and $u(k) = -c\, y(k)$, the output obeys $y(k) + (a + bc)\, y(k-1) = e(k)$, and the ARX predictor $\hat y(k) = -\hat a\, y(k-1) + \hat b\, u(k-1) = -(\hat a + \hat b c)\, y(k-1)$ depends only on $\hat a + \hat b c$. Every pair on the line $\hat a + \hat b c = a + bc$ fits equally well. For $a = -0.8$, $b = 1$ and $c = 0.5$ the data give only $a + bc = -0.3$, the negative of the closed-loop pole $0.3$, and the least squares normal matrix is singular because $u(k-1) = -0.5\, y(k-1)$.
2. **An added reference (measurement).** In the same loop with $u(k) = r(k) - 0.5\, y(k)$, a white $\pm 1$ signal $r$, unit noise and $N = 20000$, direct least squares on $(y, u)$ gave $(\hat a, \hat b) = (-0.7989, 0.9886)$. The true system is ARX, so the model set contains both $G_0$ and $H_0$, and the direct method is consistent. Identifying the closed loop from $r$ to $y$ gave $y(k) - 0.3046\, y(k-1) = 0.9886\, r(k-1)$, and solving $\hat b = 0.9886$, $\hat a = -0.3046 - 0.5\, \hat b = -0.7989$ gave the same numbers: for an ARX model with a known proportional controller, the indirect estimate equals the direct one, because the two regressor vectors are related by a fixed invertible matrix.
3. **A wrong noise model (measurement).** On the same data, an [output error](/output-error-model/) fit $b q^{-1}/(1 + f q^{-1})$ by the direct method gave $\hat b = 0.4978$ and $\hat f = -0.5532$, far from the true $b = 1$ and $f = -0.8$. In open loop the same fit would be consistent; in closed loop the noise model $H = 1$ is wrong, and the correlation between $u$ and $e$ biases $G$.

## Known algorithms

- **Direct method.** Apply the [prediction error method](/prediction-error-method/) to $(y, u)$ as if the loop were open. Cost $O(N d^2 + d^3)$ per Gauss-Newton step.
- **Indirect method.** Identify the closed-loop map from $r$ to $y$ in open loop, then solve for $G$ with the known $K$: for $u = K(r - y)$ the closed loop is $T = G K/(1 + G K)$, so $G = T / \big(K (1 - T)\big)$.
- **Joint input-output method.** Identify the maps from $r$ to $y$ and from $r$ to $u$, both open-loop problems, and take $G = G_{yr}/G_{ur}$. The controller need not be known.
- **Two-stage and projection methods.** First estimate the part of $u$ caused by $r$, the noise-free input $S_0 r$, and then fit an [output error](/output-error-model/) model from that signal to $y$.
- **[Instrumental variables](/instrumental-variable-identification/) with the reference as instrument.** Instruments built from past values of $r$ are uncorrelated with $e$ and correlated with the regressor. In example 2 with the instruments $r(k-1)$ and $r(k-2)$ the estimate was $(-0.8014, 0.9885)$.

## Bounds

As in open loop, there is no exact complexity; each method costs about what its open-loop version costs in the [real RAM](/real-ram/), $O(N d^2 + d^3)$ for one linear solve or one Gauss-Newton step. What is known are conditions for consistency and expressions for the variance.

- **Consistency of the direct method (theorem).** If the model set contains $G_0$ and $H_0$, the data are informative and the loop has a delay, the direct prediction error estimate is consistent for $G$ and $H$ (Forssell and Ljung 1999; Ljung 1999, Section 13.4). It is also efficient, with the open-loop covariance formula.
- **Bias of the direct method (theorem).** If the noise model is wrong, the limit of $G$ is biased by a term proportional to the correlation between $u$ and $e$ in the loop. The bias is small when the noise is small compared with the part of $u$ caused by $r$, or when the noise model is close to the truth (Forssell and Ljung 1999).
- **Consistency of the indirect and joint methods (theorem).** These methods are consistent for $G$ when the closed-loop maps from $r$ are estimated consistently, which holds with any fixed noise model because $r$ is independent of $e$. The indirect method needs the controller exactly.
- **Variance (theorem).** For high model orders $n$, the variance of the estimated frequency response is about $\frac{n}{N} \Phi_v(\omega) / \Phi_u^r(\omega)$, where $\Phi_v$ is the disturbance spectrum and $\Phi_u^r = \lvert S_0 \rvert^2 \Phi_r$ is the part of the input spectrum caused by $r$ (Forssell and Ljung 1999). In open loop the whole input spectrum takes the place of $\Phi_u^r$; feedback spends part of the input on rejecting noise, and in this high-order expression that part does not reduce the variance.
- **Informativeness without $r$ (theorem).** With $r = 0$ and a fixed linear controller, the data are informative only if the controller is complex enough compared with the model orders; a simple proportional controller is not, as example 1 shows (Gustavsson, Ljung and Söderström 1977).

## Reductions

- **Indirect to open loop.** Since $r$ is independent of $e$, the map from $r$ to $y$ is an open-loop identification problem, and the plant follows from it by algebra with the known $K$.
- **Joint input-output to two open-loop problems.** The maps from $r$ to $y$ and from $r$ to $u$ are two open-loop problems with the same input.
- **Direct to open loop with a full noise model.** With a correct noise model the direct method uses exactly the open-loop prediction error criterion; only the conditions for informative data change.

## Applications

- Re-identifying a plant in the process industry without opening the loop, for retuning or for model predictive control.
- Identification for control: iterating between identification and controller design, so that the model is accurate where the closed loop needs it.
- [Adaptive control](/adaptive-control/) and the self-tuning regulator, where identification always runs in closed loop.
- Plants that are unstable without feedback, such as some flight dynamics and magnetic levitation, where open-loop experiments are impossible.

## References
