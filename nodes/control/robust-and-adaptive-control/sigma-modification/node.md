---
tag: MTQP3A
kind: technique
slug: sigma-modification
name: Sigma modification
aliases:
- leakage modification
area: control/robust-and-adaptive-control
level: advanced
summary: Adds a leakage term -sigma theta to an adaptive law, which keeps the parameters bounded under disturbances at the cost of a bias.
prereqs: [model-reference-adaptive-control, lyapunov-direct-method]
see_also: [parameter-projection, rohrs-counterexample, persistent-excitation, input-to-state-stability, l1-adaptive-control, lms-algorithm, adaptive-filtering, mit-rule]
sources:
  - book: isbn:9780486498171
    title: "Petros A. Ioannou and Jing Sun, Robust Adaptive Control, Prentice Hall 1996 (Dover reprint 2012)"
    locator: "Section 8.3.1 (the parameter drift example) and Section 8.4.1 (leakage: the fixed sigma modification, law (8.4.9), the switching sigma modification and the epsilon modification)"
  - paper: "Petros A. Ioannou and Petar V. Kokotović, Adaptive Systems with Reduced Models, Lecture Notes in Control and Information Sciences 47, Springer 1983"
    locator: "the chapters on robustness to unmodeled dynamics (the sigma modification of the adaptive law)"
  - paper: "Kumpati S. Narendra and Anuradha M. Annaswamy, A new adaptive law for robust adaptation without persistent excitation, IEEE Transactions on Automatic Control 32(2), 1987"
    locator: "pages 134 to 145 (the epsilon modification, a leakage proportional to the size of the error)"
---

Sigma modification is a change of an adaptive law that adds the leakage term $-\sigma\Gamma\theta$ with a small $\sigma > 0$, so the law becomes $\dot\theta = \Gamma y - \sigma\Gamma\theta$. The leakage pulls the estimate toward zero, which turns the parameter dynamics into an exponentially decaying system driven by bounded signals, so the estimates stay bounded under bounded disturbances and unmodeled dynamics. The price is a bias: even with no disturbance, the tracking error no longer goes to zero in general, and the estimates do not converge to the true values. It is a soft alternative to [parameter projection](/parameter-projection/), which needs a known set, and it was one of the first answers to the drift and instability of the [Rohrs counterexample](/rohrs-counterexample/).

## In plain words

An adaptive controller learns some numbers by adding small corrections all the time. If a small disturbance keeps pushing in the same direction, the corrections add up, and a number can grow without limit even though the error stays small. Sigma modification adds a small leak: each number is always pulled a little back toward zero. Then the corrections cannot add up forever, because the leak grows with the number. The cost is that the numbers settle a little away from their correct values, because the leak never stops, so the controller is never exactly right. A larger leak gives a tighter bound and a larger offset.

## When it applies

- The adaptive law has the form $\dot\theta = \Gamma y$ with $\Gamma$ symmetric positive definite, and the ideal analysis uses a Lyapunov function $V = (\text{error terms}) + \tilde\theta^T\Gamma^{-1}\tilde\theta/2$ with $\dot V \le -c|e|^2$ for some $c > 0$ when there is no disturbance.
- The disturbance or the effect of the unmodeled dynamics enters the error equation as a bounded term.
- No reliable bound on $\theta^*$ is known for projection, or a smooth right-hand side is wanted.

## The template

Replace the law by
$$\dot\theta = \Gamma y - \sigma\Gamma\theta,\qquad \sigma > 0.$$
This is law (8.4.9) of Ioannou and Sun, $\dot\theta = \gamma\epsilon_1 u - \gamma w\theta$, with $w = \sigma$. The analysis uses the inequality
$$-\sigma\tilde\theta^T\theta = -\sigma\tilde\theta^T(\tilde\theta + \theta^*) \le -\frac{\sigma}{2}|\tilde\theta|^2 + \frac{\sigma}{2}|\theta^*|^2,$$
which turns the leakage into a damping term on $\tilde\theta$ plus a constant.

**Theorem (uniform ultimate bound, scalar case).** Let $\dot x = ax + u + d$ with $|d(t)| \le \bar d$, $u = -kx$, and $\dot k = \gamma x^2 - \gamma\sigma k$ with $\gamma > 0$, $\sigma > 0$. For any $a_m > 0$ let $k^* = a + a_m$, $\tilde k = k - k^*$ and $V = x^2/2 + \tilde k^2/(2\gamma)$. Then
$$\dot V \le -\alpha V + \beta,\qquad \alpha = \min(a_m, \sigma\gamma),\quad \beta = \frac{\bar d^2}{2a_m} + \frac{\sigma k^{*2}}{2},$$
so $V(t) \le e^{-\alpha t}V(0) + \beta/\alpha$ and $x$ and $k$ are bounded for every bounded $d$.

*Proof.* $\dot x = -a_mx - \tilde kx + d$, so $\dot V = -a_mx^2 - \tilde kx^2 + xd + \tilde k(x^2 - \sigma k) = -a_mx^2 + xd - \sigma\tilde kk$. Use $xd \le a_mx^2/2 + d^2/(2a_m)$ and the inequality above: $\dot V \le -\frac{a_m}{2}x^2 - \frac{\sigma}{2}\tilde k^2 + \beta \le -\alpha V + \beta$. The comparison lemma gives the bound. $\square$

Without the leakage ($\sigma = 0$) the same computation gives only $\dot V \le -a_mx^2/2 + \bar d^2/(2a_m)$, which says nothing about $\tilde k$; this is why the gain can drift.

## Classic examples

**Drift with a vanishing disturbance.** Ioannou and Sun (Section 8.3.1) take $a = 1$, $\gamma = 1$, $x(0) = 1$, $k(0) = 5$ and $d(t) = 5(1 + t)^{-1/5} - (1 + t)^{-2/5} - 0.4(1 + t)^{-7/5}$. Without leakage the exact solution is $x = (1 + t)^{-2/5}$, $k = 5(1 + t)^{1/5}$, so $k \to \infty$ while $x \to 0$. With $\sigma = 0.1$, a simulation with RK4 and the step 0.01 gives $k(10) = 5.03$, $k(100) = 3.93$, $k(1000) = 3.13$ and $x(1000) = 0.559$, against $k(1000) = 19.91$ and $x(1000) = 0.063$ without leakage (measurements). The gain stays bounded, and the error is larger.

**The bias with no disturbance.** Take $d = 0$, $a = 1$, $\gamma = 1$, $x(0) = 1$, $k(0) = 0$. Without leakage, $x^2 = 1 + 2k - k^2$ along solutions (from $\frac{d}{dt}x^2 = 2(1 - k)\dot k$), so $x \to 0$ and $k \to 1 + \sqrt 2 = 2.414$ (exact). With leakage, the equilibrium with $x \ne 0$ is $k = a$, $x^2 = \sigma a$, and the linearization there has the characteristic polynomial $\lambda^2 + \gamma\sigma\lambda + 2\gamma\sigma a$, whose roots have negative real parts. For $\sigma = 0.1$ the simulation gives $x(200) = 0.3162 = \sqrt{0.1}$ and $k(200) = 1.0001$; for $\sigma = 0.5$, $x(200) = 0.7071$ (measurements that match the equilibrium). The leakage pulls $k$ down to the value where the open loop pole $a - k$ is zero, and a nonzero $x$ is needed to hold it there.

**Leaky LMS.** In adaptive filtering, the update $w_{k+1} = (1 - \mu\sigma)w_k + \mu e_kx_k$ is the discrete form of the same idea; see the [LMS algorithm](/lms-algorithm/). It keeps the weights bounded when the input is not persistently exciting.

## Variations

- **Switching sigma modification.** Use $\sigma(\theta) = 0$ for $|\theta| \le M_0$ and a positive $\sigma$ that grows to $\sigma_0$ for $M_0 \le |\theta| \le 2M_0$ and stays there for larger $|\theta|$ (Ioannou and Tsakalis 1986). With $|\theta^*| \le M_0$, the ideal properties ($e \to 0$ with no disturbance) are kept, and the bound under disturbances remains.
- **Epsilon modification.** Use $-\sigma|e|\Gamma\theta$ (Narendra and Annaswamy 1987): the leakage is small when the error is small, which reduces the bias.
- **Leakage toward a nominal value.** Use $-\sigma\Gamma(\theta - \theta_0)$ with a prior estimate $\theta_0$; the bias then scales with $|\theta^* - \theta_0|$ in place of $|\theta^*|$.
- **Dead zone.** Stop the adaptation when the error is below a threshold related to the disturbance bound; this is another way to avoid drift.

## Pitfalls

- **The bias.** With a fixed $\sigma$, the error does not go to zero even in the ideal case, as the second example shows. Choose $\sigma$ small, or use the switching or epsilon versions.
- **The leakage fights persistent excitation.** When the command is rich, the leakage still pulls the estimates away from $\theta^*$, by an amount of order $\sigma|\theta^*|$ divided by the level of excitation (a rule of thumb).
- **Slow oscillations for small sigma.** In the second example the linearization has the damping $\gamma\sigma$, so for $\sigma = 0.01$ the approach to the equilibrium is a slow, lightly damped oscillation; a simulation of 200 s does not reach it.
- **Not a cure for every instability.** The theorem bounds the signals for bounded disturbances. With unmodeled dynamics, the bound needs in addition that the unmodeled part is small enough for the leakage to dominate; the conditions in Ioannou and Sun (Chapter 8) are explicit but conservative.

## Exercises

1. Repeat the proof of the theorem for the vector law $\dot\theta = \Gamma y - \sigma\Gamma\theta$ in the [MRAC](/model-reference-adaptive-control/) setting, and find $\alpha$ and $\beta$.
2. In the second example, show that $x^2 = 1 + 2k - k^2$ when $\sigma = 0$, and find the limit of $k$.
3. Find the equilibria of $\dot x = (a - k)x$, $\dot k = \gamma x^2 - \gamma\sigma k$ for $a > 0$, and show that the origin is not asymptotically stable.
4. For the epsilon modification $\dot k = \gamma x^2 - \gamma\sigma|x|k$, repeat the computation of the equilibrium and compare the bias with the fixed sigma case.
5. Show that for the leaky LMS update with a constant input $x_k = 1$ and $e_k = d - w_k$, the limit weight is $d/(1 + \sigma)$, a bias of $\sigma d/(1 + \sigma)$.

## References
