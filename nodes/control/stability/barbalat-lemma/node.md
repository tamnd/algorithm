---
tag: 88QYMK
kind: theorem
slug: barbalat-lemma
name: Barbalat's lemma
aliases:
- Barbalat lemma
area: control/stability
level: advanced
summary: If a function of time has a finite limit and its derivative is uniformly continuous, the derivative tends to zero. It replaces LaSalle's principle for time-varying and adaptive systems.
prereqs: [lyapunov-direct-method]
see_also: [lasalle-invariance-principle, lyapunov-direct-method, lyapunov-function, adaptive-control, model-reference-adaptive-control, persistent-excitation, linear-time-varying-system, converse-lyapunov-theorem]
sources:
  - paper: "I. Barbălat, Systèmes d'équations différentielles d'oscillations non linéaires, Revue de Mathématiques Pures et Appliquées 4, 267-270, 1959 (in French)"
    locator: the lemma on functions whose integral converges and which are uniformly continuous
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 8.3, Invariance-like Theorems (Barbalat's lemma and its use for time-varying systems)
---

Barbalat's lemma is a fact from real analysis that control theory uses in place of [LaSalle's invariance principle](/lasalle-invariance-principle/) when the system depends on time. It says when a function of time that settles to a limit also has a derivative that goes to zero. Settling alone is not enough: a function can tend to a limit while it oscillates faster and faster with smaller and smaller amplitude, and then its derivative does not go to zero. The extra condition is that the derivative is uniformly continuous, which holds for example when the second derivative is bounded. In adaptive control the lemma is the standard way to prove that a tracking error goes to zero from a Lyapunov-like function whose derivative is only nonpositive.

## Statement

**Lemma (Barbălat).** Let $\phi : [0, \infty) \to \mathbb{R}$ be uniformly continuous on $[0, \infty)$, and let the limit

$$\lim_{t \to \infty} \int_0^t \phi(\tau)\, d\tau$$

exist and be finite. Then $\phi(t) \to 0$ as $t \to \infty$.

**Corollary (derivative form).** Let $f : [0, \infty) \to \mathbb{R}$ be differentiable, let $\lim_{t \to \infty} f(t)$ exist and be finite, and let $\dot f$ be uniformly continuous on $[0, \infty)$. Then $\dot f(t) \to 0$ as $t \to \infty$.

**Corollary (Lyapunov-like form).** Let $V(t)$ be differentiable along a solution of $\dot x = f(t, x)$, bounded below, with $\dot V(t) \le 0$ for all $t \ge 0$, and let $\dot V$ be uniformly continuous in $t$. Then $\dot V(t) \to 0$ as $t \to \infty$.

A function $\phi$ is uniformly continuous on $[0, \infty)$ if for each $\varepsilon > 0$ there is one $\delta > 0$ such that $|t - s| < \delta$ implies $|\phi(t) - \phi(s)| < \varepsilon$, for all $t, s \ge 0$. A sufficient condition is that $\phi$ is differentiable with a bounded derivative, because then $\phi$ is Lipschitz.

## In plain words

Suppose a quantity changes over time and its total change, added up from the start, approaches a fixed value. One would like to say that the rate of change dies out. This can fail if the rate makes short, sharp spikes that come less and less often or get thinner and thinner: they add up to little, but they never stop. The lemma forbids such spikes by asking that the rate cannot jump quickly, with the same speed limit for all time. Then a rate that stayed away from zero now and then would stay away from zero for a fixed short while each time, and these pieces would add up to too much. So the rate must die out.

## Proof

**Proof of the lemma.** Suppose that $\phi(t)$ does not tend to $0$. Then there are $\varepsilon > 0$ and times $t_k \to \infty$ with $|\phi(t_k)| \ge \varepsilon$. By uniform continuity there is $\delta > 0$ such that $|t - s| < \delta$ implies $|\phi(t) - \phi(s)| < \varepsilon / 2$. So for $t \in [t_k, t_k + \delta]$,

$$|\phi(t)| \ge |\phi(t_k)| - |\phi(t) - \phi(t_k)| > \varepsilon / 2 ,$$

and $\phi(t)$ has the sign of $\phi(t_k)$ on that interval, because it does not pass through $0$. Then

$$\left| \int_0^{t_k + \delta} \phi\, d\tau - \int_0^{t_k} \phi\, d\tau \right| = \int_{t_k}^{t_k + \delta} |\phi(\tau)|\, d\tau \ge \frac{\varepsilon \delta}{2} .$$

But the integral $\int_0^t \phi\, d\tau$ converges as $t \to \infty$, so by the Cauchy criterion the left side tends to $0$ as $k \to \infty$. This is a contradiction. $\square$

**Proof of the derivative form.** Take $\phi = \dot f$. Then $\int_0^t \phi\, d\tau = f(t) - f(0)$, which converges. Apply the lemma. $\square$

**Proof of the Lyapunov-like form.** $V$ is nonincreasing and bounded below, so it has a finite limit. Apply the derivative form to $V$. $\square$

## Consequences

**A recipe for time-varying systems.** For $\dot x = f(t, x)$, find $V(t, x)$ bounded below with $\dot V \le -W(x) \le 0$ along solutions, with $W$ continuous. Show that the solution is bounded, often from $V$ itself. Then show that $\frac{d}{dt} W(x(t))$ is bounded, so that $W(x(t))$ is uniformly continuous. Since $\int_0^t W(x(\tau))\, d\tau \le V(0, x(0)) - \inf V$, the integral converges, and the lemma gives $W(x(t)) \to 0$ (Khalil 2002, Section 8.3).

**Example: an adaptive error equation.** Let $e$ be a tracking error and $\tilde\theta$ a parameter error, with a bounded regressor $w(t)$:

$$\dot e = -e + \tilde\theta\, w(t), \qquad \dot{\tilde\theta} = -e\, w(t) .$$

This is the error system of a simple model reference adaptive law. With $V = e^2 + \tilde\theta^2$,

$$\dot V = 2 e (-e + \tilde\theta w) + 2 \tilde\theta (-e w) = -2 e^2 \le 0 .$$

So $V$ is nonincreasing, and $e$ and $\tilde\theta$ stay bounded. Then $\dot e$ is bounded, so $\ddot V = -4 e \dot e$ is bounded, and $\dot V$ is uniformly continuous. By the Lyapunov-like form, $\dot V \to 0$, so $e(t) \to 0$. The system is time-varying through $w(t)$, so the invariance principle does not apply here.

The lemma says nothing about $\tilde\theta$. A simulation with $e(0) = \tilde\theta(0) = 1$ (classical Runge-Kutta, step $0.001$) shows the difference:

| $w(t)$ | $e(20)$ | $\tilde\theta(20)$ | $\tilde\theta(60)$ |
|---|---|---|---|
| $\sin t$ | $9.8 \cdot 10^{-5}$ | $5.7 \cdot 10^{-4}$ | below $10^{-6}$ |
| $e^{-t}$ | below $10^{-6}$ | $0.3251$ | $0.3251$ |

With $w = \sin t$ the parameter error also goes to zero. With $w = e^{-t}$ the regressor dies out, and the parameter error stays at about $0.3251$ while the tracking error goes to zero. Convergence of the parameters needs [persistent excitation](/persistent-excitation/) of $w$. This is the usual situation in [adaptive control](/adaptive-control/): Barbalat's lemma proves that the error converges, and a separate argument is needed for the parameters.

**Rule of thumb, not a theorem.** In practice one checks uniform continuity by showing that the derivative of the function is bounded. This is only a sufficient condition. It is the step that is most often skipped in faulty proofs, and the counterexamples below show that it is needed.

## Tightness

**Uniform continuity cannot be dropped.** Let $f(t) = \sin(t^2) / t$ for $t \ge 1$. Then $f(t) \to 0$, but

$$\dot f(t) = 2 \cos(t^2) - \frac{\sin(t^2)}{t^2} ,$$

which takes values near $2$ and near $-2$ for arbitrarily large $t$, so $\dot f$ has no limit. Here $\dot f$ is continuous but not uniformly continuous: $\ddot f(t) = -4 t \sin(t^2) + O(1/t)$ is unbounded, and the oscillations of $\dot f$ get faster and faster.

**Continuity is not enough in the integral form either.** Let $\phi$ be made of triangular pulses: at each integer $k \ge 1$, a triangle of height $1$ and base width $1 / k^2$, and $\phi = 0$ elsewhere. Then $\phi$ is continuous, $\int_0^\infty \phi\, d\tau = \sum_k \frac{1}{2 k^2}$ is finite, and $\phi(k) = 1$ for every $k$. The pulses get steeper, so $\phi$ is not uniformly continuous.

**A finite limit of $f$ is needed.** $f(t) = \sin t$ has a uniformly continuous derivative $\cos t$, which does not tend to $0$. The function $f$ is bounded but has no limit.

**The converse is false.** $\dot f \to 0$ does not imply that $f$ converges: $f(t) = \ln(1 + t)$ has $\dot f(t) = 1 / (1 + t) \to 0$ and $f(t) \to \infty$, and $f(t) = \sin(\ln(1 + t))$ has $\dot f \to 0$ and oscillates forever between $-1$ and $1$.

## History

Barbălat published the lemma in 1959, in a short French paper on systems of nonlinear oscillation equations in the Revue de Mathématiques Pures et Appliquées. Adaptive control later adopted it, because Lyapunov designs of adaptive laws give functions whose derivative is only negative semidefinite, and the systems are time-varying through the reference signals. Textbooks on nonlinear and adaptive control then made it a standard tool, often in the Lyapunov-like form above. Khalil (2002, Section 8.3) states it with the other invariance-like theorems for time-varying systems.

## References
