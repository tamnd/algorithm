---
tag: S1SMGT
kind: algorithm
slug: l1-adaptive-control
name: "L1 adaptive control"
aliases:
- L1 adaptive controller
area: control/robust-and-adaptive-control
level: research
summary: A fast adaptation law with a low-pass filter on the control signal that separates adaptation from robustness and bounds the transient.
model: real-ram
complexity:
  vars: {N: the number of integration steps, n: the order of the plant}
  time: {worst: O(N n^2)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: false, recursive: false, online: true}
history:
  year: 2006
  people: [Chengyu Cao, Naira Hovakimyan]
  note: "Cao and Hovakimyan put a low-pass filter on the control signal of a predictor based adaptive controller and proved uniform transient bounds that shrink as the adaptation gain grows."
prereqs: [model-reference-adaptive-control, parameter-projection, small-gain-theorem, bibo-stability]
see_also: [sigma-modification, rohrs-counterexample, lyapunov-direct-method, lyapunov-equation, h-infinity-norm, internal-model-control, certainty-equivalence, adaptive-control]
sources:
  - book: isbn:9780898717044
    title: "Naira Hovakimyan and Chengyu Cao, L1 Adaptive Control Theory: Guaranteed Robustness with Fast Adaptation, SIAM 2010"
    locator: "Chapter 2, State feedback in the presence of matched uncertainties (the architecture, the condition on the L1 norm and the transient bounds)"
  - paper: doi:10.1109/TAC.2007.914282
    title: "C. Cao and N. Hovakimyan, Design and analysis of a novel L1 adaptive control architecture with guaranteed transient performance, IEEE Transactions on Automatic Control 53(2), 2008"
    locator: "pages 586 to 591"
  - paper: doi:10.1109/TAC.2014.2318871
    title: "P. A. Ioannou, A. M. Annaswamy, K. S. Narendra, S. Jafari, L. Rudd, R. Ortega and J. Boskovic, L1-adaptive control: stability, robustness, and interpretations, IEEE Transactions on Automatic Control 59(11), 2014"
    locator: "pages 3075 to 3080 (the critique)"
  - paper: doi:10.1080/00207179.2013.849820
    title: "R. Ortega and E. Panteley, Adaptation is unnecessary in L1-adaptive control, International Journal of Control 87(3), 2014"
    locator: "pages 581 to 588 (the limit of a high adaptation gain)"
---

L1 adaptive control is a predictor based form of [model reference adaptive control](/model-reference-adaptive-control/) in which the control signal passes through a strictly proper low-pass filter $C(s)$, so that the adaptation gain $\Gamma$ can be made very large without high frequency content in the input. Its theory gives bounds on the transient in the norm of the supremum over time (the $L_\infty$ norm): the distance between the adaptive closed loop and a non-adaptive reference system is of order $1/\sqrt\Gamma$, under a small gain condition on the $L_1$ norm of the impulse response of $H(s)(1 - C(s))$. The bandwidth of $C$, not $\Gamma$, then sets the robustness margins. The method has been disputed: Ioannou and co-authors and Ortega and Panteley (2014) argue that with a measured state it is an MRAC with a filtered input, and that in the limit of a large $\Gamma$ it becomes a fixed linear controller.

## In plain words

An adaptive controller learns an unknown part of the plant while it controls it. Fast learning gives good tracking, but it also makes the control signal jump and shake, and that can excite parts of the plant that the model leaves out. L1 adaptive control lets the learning run very fast inside a software copy of the plant, the predictor, and then smooths the control signal with a filter before it reaches the real plant. The filter decides how aggressive the control can be; the learning speed only decides how closely the result matches an ideal controller that knows the unknown part. The price is that the filter must leave out some of the correction, so the loop cannot cancel the uncertainty at high frequencies.

## The problem

The plant is $\dot x = A_m x + b(\omega u + \theta^T x + \sigma)$ with the state measured, a known Hurwitz matrix $A_m$, a known $b$, and unknown parameters in known sets: here the scalar case with $\omega = 1$ and $\sigma = 0$ is treated, so

$$\dot x = a_m x + b(u + \theta x), \qquad a_m < 0,\ |\theta| \le \theta_b .$$

The aim is that $x$ tracks the response of $x_m = \frac{b\,k_g}{s - a_m} r$ with $k_g = -a_m/b$, with a transient that is bounded uniformly in time and a control signal without high frequency components, for every $\theta$ in the set.

## The algorithm

Let $p = -1/(2a_m)$ solve $2 a_m p = -1$, choose $\Gamma > 0$, a projection set given by $\theta_b$ and $\epsilon > 0$, and the filter $C(s) = \omega_c/(s + \omega_c)$. With $\tilde x = \hat x - x$, the controller is

- the state predictor $\dot{\hat x} = a_m \hat x + b(u + \hat\theta x)$,
- the adaptive law $\dot{\hat\theta} = \Gamma\,\mathrm{Proj}(\hat\theta, -\tilde x\, p\, b\, x)$, with the smooth projection operator of [parameter projection](/parameter-projection/),
- the control law $u = C(s)\,[k_g r - \hat\theta x]$.

```pseudo id=main
L1-ADAPTIVE(Γ, θ_b, ε, ω_c, k_g, dt, N)
L1  θ̂ ← θ̂₀; x̂ ← x(0); u ← 0
L2  for i ← 0 to N - 1 do
L3      r ← r(t); measure x                    ▷ t = i dt
L4      x̃ ← x̂ - x                              ▷ prediction error
L5      x̂' ← a_m x̂ + b (u + θ̂ x)               ▷ state predictor
L6      θ̂' ← Γ Proj(θ̂, -x̃ p b x)              ▷ adaptation with projection
L7      u' ← ω_c (k_g r - θ̂ x - u)             ▷ low-pass filter C(s)
L8      advance x, x̂, θ̂ and u by one RK4 step of length dt
L9  return θ̂
```

The projection uses $f(\theta) = (\theta^2 - \theta_b^2)/(\epsilon\theta_b^2)$. It returns $y$ unchanged when $f \le 0$ or $y$ points inward, and otherwise $y(1 - f)$, so $|\hat\theta| \le \theta_b\sqrt{1 + \epsilon}$ for all time. The difference from MRAC is in line L7: the law $u = k_g r - \hat\theta x$ of MRAC passes through $C(s)$.

## Example

Take $a_m = -1$, $b = 1$, the unknown $\theta = 1.5$ (so the open loop pole is at $+0.5$), $\theta_b = 2$, $\epsilon = 0.1$, $\omega_c = 10$ rad/s, $k_g = 1$, $p = 1/2$ and the step $r = 1$. Everything starts at zero, and $\hat\theta(0) = 0$.

**The condition.** $G(s) = H(s)(1 - C(s)) = \frac{s}{(s + 1)(s + \omega_c)}$ has the impulse response $g(t) = (\omega_c e^{-\omega_c t} - e^{-t})/(\omega_c - 1)$. It changes sign once, at $t_0 = \ln\omega_c/(\omega_c - 1)$, and integrates to $G(0) = 0$, so $\|G\|_{L_1} = 2(e^{-t_0} - e^{-\omega_c t_0})/(\omega_c - 1)$. With $L = \theta_b = 2$:

| $\omega_c$ | $\|G\|_{L_1}$ | $\|G\|_{L_1} L$ |
|---|---|---|
| 1 | 0.7358 | 1.472 |
| 2 | 0.5000 | 1.000 |
| 5 | 0.2675 | 0.535 |
| 10 | 0.1549 | 0.310 |
| 20 | 0.0854 | 0.171 |
| 50 | 0.0369 | 0.074 |

The condition $\|G\|_{L_1} L < 1$ holds for $\omega_c = 5$ and above, and fails for $\omega_c \le 2$.

**The reference system.** With $\hat\theta = \theta$ the loop is linear, with the characteristic polynomial $(s - 0.5)(s + 10) + 15 = s^2 + 9.5s + 10$ and the poles $-1.21$ and $-8.29$. Its step response is $x(1) = 0.650$, $x(2) = 0.895$ and $x(10) = 1.0000$.

**The adaptive loop.** RK4 with $dt = 0.002$ s over 10 s. The bound on $\tilde x$ is $\sqrt{\tilde\theta(0)^2/(\Gamma p)}$ (see Correctness). These are measurements, except the bound.

| $\Gamma$ | $\max \lvert\tilde x\rvert$ | bound | $\max\lvert x - x_{\mathrm{ref}}\rvert$ | $\max\lvert u - u_{\mathrm{ref}}\rvert$ | $\hat\theta(10)$ |
|---|---|---|---|---|---|
| 10 | 0.4955 | 0.6708 | 0.5316 | 1.162 | 1.4939 |
| 100 | 0.1759 | 0.2121 | 0.1817 | 0.595 | 1.4955 |
| 1000 | 0.0598 | 0.0671 | 0.0558 | 0.303 | 1.4962 |

The distance to the reference system falls by about $\sqrt{10} = 3.2$ per factor 10 of $\Gamma$ in $x$, and by about 2 in $u$. In every run $x(10)$ is within 0.005 of 1, and $\hat\theta$ reaches 2.0976, just inside the projection limit $2\sqrt{1.1} = 2.0976$, during the first transient.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) gives the prediction error bound in full. With $V = p\tilde x^2 + \tilde\theta^2/\Gamma$ and $\tilde\theta = \hat\theta - \theta$, the error equation is $\dot{\tilde x} = a_m\tilde x + b\tilde\theta x$, and the projection gives $\dot V \le -\tilde x^2$ whenever $|\theta| \le \theta_b$. So $p\tilde x^2 \le V(0) = \tilde\theta(0)^2/\Gamma$ when $\tilde x(0) = 0$, which gives $\|\tilde x\|_{L_\infty} \le \sqrt{\tilde\theta(0)^2/(\Gamma p)}$, a theorem; the general form uses the largest possible $\tilde\theta$, $4\theta_b^2(1 + \epsilon)$ in place of $\tilde\theta(0)^2$. The second step is the main theorem of Cao and Hovakimyan, stated here and not reproved: if $\|G\|_{L_1} L < 1$, the reference system is bounded in the $L_\infty$ norm, and $\|x - x_{\mathrm{ref}}\|_{L_\infty} \le \gamma_1/\sqrt\Gamma$ and $\|u - u_{\mathrm{ref}}\|_{L_\infty} \le \gamma_2/\sqrt\Gamma$ with constants that do not depend on $\Gamma$. The proof combines the prediction error bound with the [small gain theorem](/small-gain-theorem/) for the filtered loop.

## Complexity

For an $n$-dimensional state, each evaluation of the right-hand side costs $O(n^2)$ for the plant, the predictor and the matrix $P$, and $O(n)$ for the adaptive law and the filter, in the real-RAM model. $N$ RK4 steps cost $O(N n^2)$, and the memory is $O(n^2)$ for $A_m$ and $P$. The large $\Gamma$ makes the adaptive law stiff, so $dt$ must shrink as $\Gamma$ grows: with RK4 the product of $dt$ and the adaptation rate $\Gamma p b^2 x^2$ must stay below about 2.8 (a rule of thumb from the stability region of RK4). In an implementation on a computer, the sampling period $h$ of the adaptive law limits the useful $\Gamma$.

## Properties

- **Uniform transient bounds.** Theorem (Cao and Hovakimyan): under the $L_1$ norm condition the state and the input stay within $O(1/\sqrt\Gamma)$ of a linear reference system, uniformly in time, not only as $t \to \infty$.
- **Robustness set by the filter.** The time delay margin of the loop is bounded below by a quantity that depends on $C(s)$ and not on $\Gamma$, as $\Gamma \to \infty$ (theorem in Hovakimyan and Cao, Chapter 2).
- **Trade-off in the filter.** A wider filter bandwidth makes $\|G\|_{L_1}$ smaller and the reference system closer to the ideal model, but it lowers the robustness margins. The table shows how $\|G\|_{L_1}$ falls with $\omega_c$.
- **No parameter convergence claim.** As in MRAC, $\hat\theta$ need not converge to $\theta$; the example gives $1.494$ to $1.496$ after 10 s.
- **Disputed interpretation.** Ioannou and co-authors (2014) argue that with a measured state the scheme is an MRAC with an input filter, and that its claimed advantages can be obtained by standard robust adaptive designs. Ortega and Panteley (2014) show that as $\Gamma \to \infty$ the controller tends to a linear time-invariant controller, so the adaptation is not needed for the limit. Hovakimyan and co-authors disputed these readings. This page states the theorems and the critique; it does not decide between them.

## Variants and improvements

- **Unknown input gain and disturbances.** The general architecture estimates $\omega$, $\theta$ and $\sigma$ with three projection laws and uses a filter $D(s)$ with a feedback gain $k$ in $u = -k D(s)(\hat\eta - k_g r)$.
- **Piecewise constant adaptation.** The adaptive law is replaced by a law that updates $\hat\sigma$ once per sampling period $h$ from the prediction error, which makes the speed of adaptation a matter of $h$ (Hovakimyan and Cao treat this law in the later chapters of the book).
- **Output feedback.** For a plant with only the output measured, the predictor is an output predictor, and the same filter structure applies.
- **Nonlinear and time-varying uncertainty.** The theory extends to matched nonlinear uncertainty that is Lipschitz in $x$ and to unmatched uncertainty.

## When to use it

Use L1 adaptive control when the state is measured, the uncertainty is matched and bounded in a known set, and a guaranteed transient bound in the $L_\infty$ norm matters more than parameter learning, for example in flight control research. The computer that runs it must have a fast sampling rate to support a large $\Gamma$. If the analysis of a fixed robust controller with the same filter gives the same margins, as the critique says it often does, prefer the fixed controller.

## Pitfalls

- **The condition fails.** For a narrow filter, $\|G\|_{L_1} L \ge 1$, and the bounds do not hold. The example shows the border at $\omega_c = 2$.
- **Stiff integration.** A large $\Gamma$ needs a small step $dt$ or sampling period $h$; otherwise the discrete adaptive law is not a good approximation of the continuous law, and the bounds of the continuous theory do not apply.
- **Projection set too small.** The proof needs the true $\theta$ inside the set $|\theta| \le \theta_b$. A wrong set gives a biased estimate and no bound.
- **Filter too wide.** A filter with a large bandwidth gives a small $\|G\|_{L_1}$ but passes the high frequency content of $\hat\theta x$ to the plant, which the filter was meant to remove.
- **Reading $1/\sqrt\Gamma$ as zero.** The bounds compare with the reference system, not with the ideal model $x_m$; the reference system itself differs from $x_m$ by an amount set by $C(s)$.

## Implementations

## History

Cao and Hovakimyan introduced the architecture in 2006 and published the analysis with the uniform transient bounds in 2008. The book of Hovakimyan and Cao (2010) collects the state feedback, output feedback and nonlinear versions. In 2014 Ioannou, Annaswamy, Narendra, Jafari, Rudd, Ortega and Boskovic published a critique of the stability and robustness claims, and Ortega and Panteley showed that the controller tends to a fixed linear controller for large $\Gamma$. The debate is about the interpretation of the results and their advantage over earlier robust adaptive designs.

## References
