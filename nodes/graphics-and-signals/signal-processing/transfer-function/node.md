---
tag: NFNFGK
kind: definition
slug: transfer-function
name: Transfer function
aliases:
- system function
area: graphics-and-signals/signal-processing
level: core
summary: The z-transform H(z) of the impulse response of an LTI system, with its region of convergence. A difference equation gives a rational H = B/A, fixed by its poles, zeros and gain.
prereqs: [z-transform, impulse-response]
see_also: [frequency-response, bibo-stability, minimum-phase, state-space-model, iir-filter, fir-filter, partial-fraction-decomposition, digital-filter-design]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 3 (the z-transform of LTI systems) and Chapter 5, Transform Analysis of Linear Time-Invariant Systems (systems described by difference equations, the poles and zeros of rational system functions, and their causality and stability)
  - book: isbn:9780138147570
    title: Alan V. Oppenheim, Alan S. Willsky and S. Hamid Nawab, Signals and Systems, second edition, Prentice Hall, 1997
    locator: Chapter 10, The z-Transform (the analysis of LTI systems with the system function, and block diagrams)
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: Chapter 3, The z-Transform and Its Application to the Analysis of LTI Systems
---

The transfer function of a [linear time-invariant system](/linear-time-invariant-system/) is the [z-transform](/z-transform/) $H(z) = \sum_n h[n] z^{-n}$ of its [impulse response](/impulse-response/), together with its region of convergence. In the transform domain the system is a multiplication, $Y(z) = H(z) X(z)$. A system that runs a linear difference equation with constant coefficients has a rational transfer function $H(z) = B(z)/A(z)$, so a few numbers describe a filter with an infinite impulse response: its poles, its zeros and a gain. The poles decide [BIBO stability](/bibo-stability/), the zeros decide [minimum phase](/minimum-phase/), and both shape the [frequency response](/frequency-response/), which is $H$ on the unit circle.

## Definition

**Notation.** Signals are sequences $x[n]$, $n \in \mathbb{Z}$; frequencies $\omega$ are in radians per sample. For a polynomial in $z^{-1}$ we write $B(z) = \sum_{k=0}^{q} b_k z^{-k}$.

**Definition.** The transfer function (system function) of an LTI system with impulse response $h$ is

$$H(z) = \sum_{n=-\infty}^{\infty} h[n]\, z^{-n}, \qquad z \in \mathrm{ROC}_h.$$

For each input $x$ whose ROC meets that of $h$, the output has $Y(z) = H(z)\, X(z)$ on the common region, by the convolution property of the z-transform.

**Rational transfer functions.** A causal system at initial rest that runs

$$\sum_{k=0}^{p} a_k\, y[n-k] = \sum_{k=0}^{q} b_k\, x[n-k], \qquad a_0 \ne 0,$$

has

$$H(z) = \frac{B(z)}{A(z)} = \frac{\sum_{k=0}^{q} b_k z^{-k}}{\sum_{k=0}^{p} a_k z^{-k}} = \frac{b_0}{a_0}\, \frac{\prod_{k=1}^{q} (1 - c_k z^{-1})}{\prod_{k=1}^{p} (1 - d_k z^{-1})},$$

with $b_0 \ne 0$ in the last form. The $c_k$ are the *zeros* and the $d_k$ the *poles*; in the variable $z$, $H$ also has a pole or a zero of order $|p - q|$ at $z = 0$. The difference equation fixes the formula but not the ROC: initial rest, which makes the system causal, picks the outside region $|z| > \max_k |d_k|$. The other annuli bounded by poles give non-causal systems with the same formula.

**Lowest terms.** If $B$ and $A$ have a common factor $(1 - c z^{-1})$, the factor cancels in $H$: the input-output map of the system at rest is that of the reduced fraction. The cancelled root is a mode of the difference equation that the input does not excite, but a nonzero initial state does. Poles and zeros of $H$ always mean those of the reduced fraction, which a [polynomial gcd](/polynomial-gcd/) finds over exact coefficients.

**Impulse response from $H$.** If the poles $d_k$ are distinct and $q < p$, partial fractions give $H(z) = \sum_k \frac{r_k}{1 - d_k z^{-1}}$, and for the causal ROC $h[n] = \sum_k r_k\, d_k^n$ for $n \ge 0$. A pole of multiplicity $m$ gives the terms $n^j d_k^n$ for $j < m$. If $q \ge p$, polynomial division adds an FIR part of length $q - p + 1$. See [partial fraction decomposition](/partial-fraction-decomposition/).

**Connections.** For systems $H_1$ and $H_2$:

- *cascade*: $H(z) = H_1(z)\, H_2(z)$;
- *parallel*: $H(z) = H_1(z) + H_2(z)$;
- *feedback*: with $y = H_1 (x - H_2 y)$, $H(z) = \dfrac{H_1(z)}{1 + H_1(z) H_2(z)}$.

**State space.** A system $s[n+1] = A_s s[n] + B_s x[n]$, $y[n] = C_s s[n] + D_s x[n]$ has $H(z) = C_s (zI - A_s)^{-1} B_s + D_s$, rational with the poles among the eigenvalues of $A_s$; see [state-space model](/state-space-model/). A causal transfer function is rational if and only if it has a finite-dimensional state-space realization.

**Cost.** A rational $H$ of orders $p$ and $q$ runs in $p + q + 1$ multiplications per output sample by its difference equation, whatever the length of $h$. An FIR filter is the case $A(z) = 1$: all its poles are at $z = 0$.

## Examples and non-examples

- **Moving average.** $y[n] = \frac{1}{3}(x[n] + x[n-1] + x[n-2])$ has $H(z) = \frac{1}{3}(1 + z^{-1} + z^{-2}) = \frac{z^2 + z + 1}{3 z^2}$. Its zeros are $e^{\pm 2\pi i / 3}$ on the unit circle, so the frequency $\omega = 2\pi/3$ is removed, and it has a double pole at $z = 0$. ROC $z \ne 0$.
- **First-order recursion.** $y[n] = \frac{1}{2} y[n-1] + x[n]$ has $H(z) = \frac{1}{1 - \frac{1}{2} z^{-1}}$, a pole at $\frac{1}{2}$ and a zero at $0$. The causal ROC is $|z| > \frac{1}{2}$, and $h[n] = 2^{-n} u[n]$.
- **Resonator.** $y[n] = 2r\cos\theta\, y[n-1] - r^2 y[n-2] + x[n]$ with $0 < r < 1$ has the poles $r e^{\pm i\theta}$. Its frequency response peaks near $\omega = \pm\theta$, more sharply as $r \to 1$.
- **Accumulator.** $H(z) = \frac{1}{1 - z^{-1}}$ has a pole at $z = 1$ on the unit circle; it is causal and not stable.
- **Two poles, two systems.** $H(z) = \frac{1}{(1 - \frac{1}{2} z^{-1})(1 - 2 z^{-1})}$ with $|z| > 2$ is the causal system of the equation $y[n] - \frac{5}{2} y[n-1] + y[n-2] = x[n]$, and it is not stable. With $\frac{1}{2} < |z| < 2$ it is a stable non-causal system: the [z-transform](/z-transform/) page gives the three impulse responses.
- **Hidden mode.** $y[n] - 2 y[n-1] = x[n] - 2 x[n-1]$ has $H(z) = \frac{1 - 2 z^{-1}}{1 - 2 z^{-1}} = 1$ and $h = \delta$, so the system at rest is the identity and is stable. But with the initial value $y[-1] = c$ and zero input, the output is $c\, 2^{n+1}$: the cancelled root $2$ is still a mode of the recursion.
- **A transfer function that is not rational.** $h[n] = 1/n!$ for $n \ge 0$ has $H(z) = e^{1/z}$, ROC $z \ne 0$: causal and stable, but no finite difference equation computes it exactly.
- **Non-example.** The [median filter](/median-filter/) and the squarer $y[n] = x[n]^2$ are not linear, and $y[n] = n\, x[n]$ is not time invariant; none of them has a transfer function.
- **Non-example.** The ideal lowpass filter has a frequency response but no transfer function in this sense: its impulse response $\sin(\omega_c n)/(\pi n)$ has an empty ROC.

## Related definitions

- [Z-transform](/z-transform/): the transform and its region of convergence.
- [Impulse response](/impulse-response/): the inverse z-transform of $H$.
- [Frequency response](/frequency-response/): $H(e^{i\omega})$, the transfer function on the unit circle.
- [BIBO stability](/bibo-stability/): for a causal rational $H$ in lowest terms, all poles strictly inside the unit circle.
- [Minimum phase](/minimum-phase/): a causal stable $H$ with all zeros strictly inside the unit circle too.
- [FIR filter](/fir-filter/) and [IIR filter](/iir-filter/): $A = 1$, and a nontrivial $A$.
- [Digital filter design](/digital-filter-design/): the choice of poles and zeros for a given frequency response.
- [State-space model](/state-space-model/): the matrix form of a rational transfer function.

## References
