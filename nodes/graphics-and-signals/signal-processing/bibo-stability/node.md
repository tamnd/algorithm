---
tag: WPRRG6
kind: definition
slug: bibo-stability
name: BIBO stability
aliases:
- bounded-input bounded-output stability
area: graphics-and-signals/signal-processing
level: core
summary: A system is BIBO stable if every bounded input gives a bounded output. An LTI system is BIBO stable if and only if its impulse response is absolutely summable.
prereqs: [impulse-response, transfer-function]
see_also: [frequency-response, minimum-phase, iir-filter, z-transform, levinson-durbin-algorithm, polynomial-gcd, state-space-model]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 2.4 (stability of LTI systems and the absolutely summable impulse response) and Chapters 3 and 5 (the region of convergence, and the poles of causal stable rational systems)
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: Chapter 2 (stability of LTI systems) and Chapter 3 (causality and stability in the z-domain)
  - url: https://www.dsprelated.com/freebooks/filters/Stability_Revisited.html
    title: Julius O. Smith III, Introduction to Digital Filters with Audio Applications, Stability Revisited
    locator: the step-down (Schur-Cohn) test with reflection coefficients
---

A system is BIBO stable (bounded-input bounded-output stable) if every bounded input gives a bounded output. For a [linear time-invariant system](/linear-time-invariant-system/), this holds if and only if the [impulse response](/impulse-response/) is absolutely summable, $\sum_n |h[n]| < \infty$, and then $\sum_n |h[n]|$ is the largest gain from the peak of the input to the peak of the output. For a causal filter with a rational [transfer function](/transfer-function/) in lowest terms, the test is on the poles: all must lie strictly inside the unit circle. A step-down recursion on the denominator decides this in $O(p^2)$ exact rational operations, without finding the poles.

## Definition

**Notation.** Signals are sequences $x[n]$, $n \in \mathbb{Z}$. A signal is *bounded* if $\|x\|_\infty = \sup_n |x[n]| < \infty$.

**Definition.** A system $T$ is BIBO stable if for every input $x$ with $\|x\|_\infty < \infty$, the output $y = T x$ is defined and $\|y\|_\infty < \infty$.

**Theorem (LTI systems).** The LTI system $y = x * h$ is BIBO stable if and only if $h \in \ell^1$. Then $\|y\|_\infty \le \|h\|_1 \|x\|_\infty$, and the constant $\|h\|_1$ is the best possible.

*Proof.* If $h \in \ell^1$, then $|y[n]| \le \sum_k |h[k]|\, |x[n-k]| \le \|h\|_1 \|x\|_\infty$ for every $n$. If $\|h\|_1 = \infty$, take $x[n] = \overline{h[-n]} / |h[-n]|$ where $h[-n] \ne 0$, and $x[n] = 0$ elsewhere. Then $\|x\|_\infty \le 1$, and $y[0] = \sum_k h[k]\, x[-k] = \sum_k |h[k]|$ diverges, so the output is not bounded. For $h \in \ell^1$ the same input, cut to the finitely many terms that hold most of $\|h\|_1$, gives $|y[0]|$ as close to $\|h\|_1$ as one wants, so the constant is the best. $\square$

**Theorem (rational causal systems).** Let $H(z) = B(z)/A(z)$ be in lowest terms, with the causal region of convergence. The system is BIBO stable if and only if every pole $d$ of $H$ satisfies $|d| < 1$.

*Proof.* By partial fractions, $h[n]$ is, for $n$ larger than the length of the FIR part, a sum $\sum_d \sum_{j < m_d} c_{d,j}\, n^j d^n$ with nonzero top coefficients $c_{d, m_d - 1}$, where $m_d$ is the multiplicity of the pole $d$. If all $|d| < 1$, each $\sum_n n^j |d|^n$ is finite, so $h \in \ell^1$. If some $|d| \ge 1$, let $\rho \ge 1$ be the largest modulus of a pole and $J$ the largest $j$ with $c_{d,j} \ne 0$ among the poles of modulus $\rho$. Then $h[n] / (n^J \rho^n) = \sum_{|d| = \rho} c_{d,J}\, e^{i\theta_d n} + o(1)$, with distinct angles $\theta_d$. A nonzero trigonometric sum with distinct frequencies does not tend to $0$, because its mean square over $n = 1, \ldots, N$ tends to $\sum |c_{d,J}|^2 > 0$. So $|h[n]| \ge \varepsilon\, n^J \rho^n \ge \varepsilon$ for infinitely many $n$, and $h \notin \ell^1$. $\square$

**Region of convergence.** For any LTI system with a z-transform, BIBO stability is the same as: the ROC of $H$ contains the unit circle. A stable system can be non-causal, with poles on both sides of the circle.

**Step-down test.** Let $A(z) = 1 + a_1 z^{-1} + \cdots + a_p z^{-p}$ with real coefficients. Set $A_p = A$ and, for $m = p, p - 1, \ldots, 1$,

$$k_m = \text{the coefficient of } z^{-m} \text{ in } A_m, \qquad A_{m-1}(z) = \frac{A_m(z) - k_m z^{-m} A_m(1/z)}{1 - k_m^2}.$$

All zeros of $z^p A(z)$ lie strictly inside the unit circle if and only if $|k_m| < 1$ for every $m$; stop with "unstable" at the first $|k_m| \ge 1$. This is the Schur-Cohn test in its step-down form, the [Levinson-Durbin](/levinson-durbin-algorithm/) recursion run backwards, and the $k_m$ are the reflection coefficients of a lattice filter. It costs $O(p^2)$ operations and is exact on rational coefficients. Applied to the denominator of $H$ after the common factors with $B$ have been cancelled by a [polynomial gcd](/polynomial-gcd/), it decides BIBO stability of a causal rational filter.

**Other kinds of stability.** For a [state-space model](/state-space-model/) $s[n+1] = A_s s[n] + B_s x[n]$, *internal* (asymptotic) stability asks that all eigenvalues of $A_s$ lie inside the unit circle. It implies BIBO stability. The converse fails when a mode is cancelled: the system is then BIBO stable while a nonzero initial state grows.

## Examples and non-examples

- **First-order recursion.** $h[n] = 2^{-n} u[n]$ has $\|h\|_1 = 2$, so $|y[n]| \le 2 \sup |x|$, with equality for the constant input $1$ in the limit.
- **Step-down.** $A(z) = 1 - \frac{1}{6} z^{-1} - \frac{1}{6} z^{-2} = (1 - \frac{1}{2} z^{-1})(1 + \frac{1}{3} z^{-1})$ has the poles $\frac{1}{2}$ and $-\frac{1}{3}$. The test gives $k_2 = -\frac{1}{6}$, then $A_1(z) = 1 - \frac{1}{5} z^{-1}$ and $k_1 = -\frac{1}{5}$. Both are below $1$ in modulus, so the causal $1/A$ is stable.
- **FIR filters.** Every FIR filter is stable: $\|h\|_1$ is a finite sum.
- **Accumulator, a pole at $1$.** $y[n] = y[n-1] + x[n]$ has $h = u$ and $\|h\|_1 = \infty$. The bounded input $u$ gives $y[n] = n + 1$.
- **A pole at $-1$.** $y[n] = -y[n-1] + x[n]$ has $h[n] = (-1)^n u[n]$. The bounded input $(-1)^n u[n]$ gives $y[n] = (n + 1)(-1)^n$.
- **An oscillator.** $H(z) = 1/(1 + z^{-2})$ has the poles $\pm i$ on the circle, and $h = 1, 0, -1, 0, 1, \ldots$ is bounded. The system is still not BIBO stable: an input with the same pattern, of frequency $\pi/2$, makes the output grow linearly. A bounded impulse response is not enough.
- **Cancellation.** $H(z) = \frac{1 - 2z^{-1}}{1 - 2z^{-1}}$ is the identity, $h = \delta$, and is stable. The step-down test on the uncancelled denominator gives $k_1 = -2$ and the wrong answer.
- **Stable but not causal.** $H(z) = \frac{1}{(1 - \frac{1}{2} z^{-1})(1 - 2z^{-1})}$ with the ROC $\frac{1}{2} < |z| < 2$ is stable, with a pole outside the circle; its impulse response is two-sided. With the causal ROC $|z| > 2$ it is unstable.
- **Ideal lowpass.** $h[n] = \sin(\omega_c n)/(\pi n)$ has $\sum_n |h[n]| = \infty$, like the harmonic series, so the ideal filter is not BIBO stable, although $h \in \ell^2$.
- **Non-example, nonlinear.** $y[n] = x[n]^2$ is stable, with $\|y\|_\infty = \|x\|_\infty^2$, but it is not linear, so the $\ell^1$ criterion does not apply to it.

## Related definitions

- [Impulse response](/impulse-response/): the sequence whose $\ell^1$ norm decides stability.
- [Transfer function](/transfer-function/) and [z-transform](/z-transform/): the poles and the region of convergence.
- [Frequency response](/frequency-response/): exists as a continuous function for every stable system.
- [Minimum phase](/minimum-phase/): stable, with a stable causal inverse.
- [IIR filter](/iir-filter/): the filters for which stability is a question; quantized coefficients can move poles out of the circle.
- [Levinson-Durbin algorithm](/levinson-durbin-algorithm/): the forward recursion of the step-down test.

## References
