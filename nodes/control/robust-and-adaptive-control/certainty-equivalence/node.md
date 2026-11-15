---
tag: QHF40X
kind: concept
slug: certainty-equivalence
name: Certainty equivalence principle
aliases:
- certainty equivalence
area: control/robust-and-adaptive-control
level: core
summary: Design the controller as if the current parameter estimates were the true values, a principle behind most adaptive schemes.
prereqs: [adaptive-control, kalman-filter]
see_also: [separation-principle, lqg-control, self-tuning-regulator, adaptive-pole-placement, parameter-projection, model-based-reinforcement-learning, rls-algorithm, persistent-excitation]
sources:
  - book: isbn:9780486462783
    title: "Karl Johan Åström and Björn Wittenmark, Adaptive Control, second edition, Addison-Wesley 1995 (Dover reprint 2008)"
    locator: "Chapter 3, Deterministic self-tuning regulators (the indirect self-tuner as a certainty equivalence design) and Chapter 7, Stochastic adaptive control (dual control, cautious control and the certainty equivalence controller)"
  - book: isbn:9780486498171
    title: "Petros A. Ioannou and Jing Sun, Robust Adaptive Control, Prentice Hall 1996 (Dover reprint 2012)"
    locator: "Section 7.6.1 (the certainty equivalence control law u = -2y/b-hat and the loss of stabilizability when b-hat crosses zero) and Section 7.6.2 (projection that keeps the estimate in a stabilizable set)"
  - paper: "Herbert A. Simon, Dynamic programming under uncertainty with a quadratic criterion function, Econometrica 24(1), 1956"
    locator: "pages 74 to 81 (the optimal decision with a quadratic cost uses only the expected values of the uncertain quantities)"
  - paper: "Yaakov Bar-Shalom and Edison Tse, Dual effect, certainty equivalence, and separation in stochastic control, IEEE Transactions on Automatic Control 19(5), 1974"
    locator: "pages 494 to 500 (certainty equivalence holds exactly when the control has no dual effect)"
---

The certainty equivalence principle is the rule to design the controller as if the current estimates of the unknown quantities were the true values. It splits an adaptive controller into two independent parts: an estimator, for example the [recursive least squares algorithm](/rls-algorithm/), and a design rule for a known plant, for example pole placement. In linear quadratic Gaussian control with known parameters and an unknown state, the principle is a theorem: the optimal controller is the optimal state feedback applied to the state estimate of the [Kalman filter](/kalman-filter/). For unknown parameters it is in general not optimal, because the control also decides how much the controller will learn; then it is a design heuristic that most adaptive schemes use.

## In plain words

When you do not know a number that you need, the simplest plan is to use your best guess and act as if the guess were right. In adaptive control, the controller keeps a best guess of the machine and redesigns itself for this guess at every step. This is easy, because the design methods for a known machine can be used without change. It ignores two things. First, the guess can be wrong, and a careful controller would act more gently while it is unsure. Second, a controller that pushes the machine a little more could learn faster. The rule also fails when the guess describes a machine that cannot be controlled at all.

## The idea

Let the plant depend on parameters $\theta$, and let $\vartheta = F(\theta)$ be a controller design for the known $\theta$, for example the solution of a pole placement equation. An estimator gives $\hat\theta_t$ from the data up to time $t$. The certainty equivalence controller applies $\vartheta_t = F(\hat\theta_t)$. The [self-tuning regulator](/self-tuning-regulator/) and [adaptive pole placement](/adaptive-pole-placement/) are built this way.

**When it is exact.** For the linear plant $x_{t+1} = Ax_t + Bu_t + w_t$, $y_t = Cx_t + v_t$ with known matrices, Gaussian noises and a quadratic cost, the optimal input is $u_t = -K\hat x_{t|t}$, where $K$ is the optimal gain for the noise free problem with the state known and $\hat x_{t|t}$ is the Kalman filter estimate. This is the [separation principle](/separation-principle/) of [LQG control](/lqg-control/), a theorem. The reason is that the input does not change the covariance of the estimation error: the control has no dual effect (Bar-Shalom and Tse 1974).

**When it is not exact.** With an unknown parameter, the input changes what the controller will learn. Take the scalar plant $x_{t+1} = x_t + bu_t + w_t$ with $w_t$ of variance $\sigma^2$, and suppose that the current knowledge of $b$ is a mean $\hat b$ and a variance $p$. The one step cost $E[x_{t+1}^2] = (x_t + \hat bu_t)^2 + pu_t^2 + \sigma^2$ is minimal at the cautious input $u_t = -\hat b x_t/(\hat b^2 + p)$, with the cost $x_t^2\,p/(\hat b^2 + p) + \sigma^2$. The certainty equivalence input $u_t = -x_t/\hat b$ gives the cost $x_t^2\,p/\hat b^2 + \sigma^2$. For $\hat b = 1$ and $p = 1$ the extra cost is $x_t^2$ for certainty equivalence and $x_t^2/2$ for cautious control (an exact computation). Cautious control can stop learning, because a small input gives little information about $b$ (the turn-off effect). The truly optimal controller, the dual controller of Feldbaum, balances caution and probing, but it solves a [Bellman equation](/bellman-equation/) on the space of distributions and is not practical except for very small problems.

**What adaptive control does in practice.** The certainty equivalence design is kept, and three safeguards are added: [persistent excitation](/persistent-excitation/) of the command so that the estimate converges, [parameter projection](/parameter-projection/) or a similar rule so that the estimate stays in a set where $F$ exists and is well conditioned, and a slow enough adaptation so that the estimate does not react to noise.

## Examples

- **Loss of stabilizability.** For the plant $\dot y = y + bu$ with $b$ unknown, the certainty equivalence design for the closed loop pole $-1$ is $u = -2y/\hat b$. When $\hat b$ passes through zero, the input is not defined, and near zero it is very large. Ioannou and Sun (Section 7.6) show this failure, and fix it by projecting $\hat b$ into a set $|\hat b| \ge b_0 > 0$ whose sign is known.
- **Adaptive pole placement.** The estimate $\hat A = q^2$, $\hat B = q$ has the common factor $q$, so the pole placement equation has no solution, and the certainty equivalence input is not defined; see the [adaptive pole placement](/adaptive-pole-placement/) page, where the start $\hat B = q + 0.1$ avoids the problem.
- **Self-tuning to the right law with a wrong model.** For the plant $y_{t+1} = 0.9y_t + 0.5u_t + e_{t+1} + 0.5e_t$, the self-tuning regulator estimates a model that ignores the noise term $0.5e_t$. The estimates are biased, but the certainty equivalence law converges to the minimum variance law $u_t = -2.8y_t$ (a theorem on the [self-tuning regulator](/self-tuning-regulator/) page, the self-tuning property). Here certainty equivalence works better than the model suggests.

## Where it is used

Most indirect adaptive controllers use the principle: self-tuning regulators, adaptive pole placement, adaptive LQ control and adaptive [model predictive control](/model-predictive-control/). In LQG control it is exact. In economics, Simon (1956) and Theil (1957) introduced the term for decisions with a quadratic cost. In [model-based reinforcement learning](/model-based-reinforcement-learning/), acting optimally for the estimated model is also called certainty equivalence; there the same tension between using and improving the model appears as the trade-off between exploitation and exploration.

## References
