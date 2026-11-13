---
tag: X663WS
kind: definition
slug: z-transform
name: Z-transform
aliases:
- generating function transform
area: graphics-and-signals/signal-processing
level: core
summary: The function X(z) = sum of x[n] z^(-n) of a complex variable z, together with its region of convergence, an annulus in the complex plane. On the unit circle it is the DTFT.
prereqs: [discrete-time-fourier-transform]
see_also: [transfer-function, frequency-response, bibo-stability, generating-functions, partial-fraction-decomposition, linear-recurrences-with-constant-coefficients, bilinear-transform]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 3, The z-Transform (the region of convergence and its properties, the inverse transform by partial fractions, the properties and transform pairs, and the z-transform of LTI systems)
  - book: isbn:9780138147570
    title: Alan V. Oppenheim, Alan S. Willsky and S. Hamid Nawab, Signals and Systems, second edition, Prentice Hall, 1997
    locator: Chapter 10, The z-Transform
  - paper: doi:10.1109/TAI.1952.6371274
    title: John R. Ragazzini and Lotfi A. Zadeh, The analysis of sampled-data systems, Transactions of the AIEE, Part II 71, 1952, 225 to 234
    locator: the transform of sampled-data systems that the paper names the z-transform
---

The z-transform of a sequence $x[n]$ is the function $X(z) = \sum_n x[n] z^{-n}$ of a complex variable $z$, defined on its region of convergence (ROC), the set of $z$ where the series converges absolutely. The formula alone does not fix the sequence: $a^n u[n]$ and $-a^n u[-n-1]$ have the same formula $1/(1 - a z^{-1})$, and only the ROC tells them apart. On the unit circle $z = e^{i\omega}$ it becomes the [discrete-time Fourier transform](/discrete-time-fourier-transform/), when the ROC contains that circle. It turns convolution into multiplication and difference equations into rational functions, which is why the [transfer function](/transfer-function/) of a filter is a z-transform. Ragazzini and Zadeh gave it its name in 1952, in work on sampled-data control.

## Definition

**Notation.** A sequence is $x : \mathbb{Z} \to \mathbb{C}$. The unit step is $u[n] = 1$ for $n \ge 0$ and $0$ for $n < 0$. Frequencies $\omega$ are in radians per sample, and $z = r e^{i\omega}$ with $r = |z|$.

**Definition.** The (two-sided) z-transform of $x$ is

$$X(z) = \sum_{n=-\infty}^{\infty} x[n]\, z^{-n},$$

with the *region of convergence* $\mathrm{ROC}_x = \{ z \in \mathbb{C} : \sum_n |x[n]|\, |z|^{-n} < \infty \}$. The transform is the pair of the function and the region. The series $\sum_n x[n] z^{-n}$ is a Laurent series in $z$, and $X(z) = G(1/z)$, where $G(t) = \sum_n x[n]\, t^n$ is the generating function of $x$ in the sense of [generating functions](/generating-functions/), with the variable inverted.

**The ROC is an annulus.** Absolute convergence depends only on $|z|$. The part $\sum_{n \ge 0} x[n] z^{-n}$ converges for $|z| > r_R$ and the part $\sum_{n < 0} x[n] z^{-n}$ converges for $|z| < r_L$, with $r_R = \limsup_{n \to \infty} |x[n]|^{1/n}$ and $1/r_L = \limsup_{n \to \infty} |x[-n]|^{1/n}$. So the ROC is the annulus $r_R < |z| < r_L$, possibly with some of its boundary circle, and it can be empty. In the ROC, $X$ is analytic.

- If $x$ has finite support, the ROC is the whole plane, except perhaps $z = 0$ (when $x[n] \ne 0$ for some $n > 0$) and $z = \infty$ (when $x[n] \ne 0$ for some $n < 0$).
- If $x$ is right-sided ($x[n] = 0$ for $n < n_0$), the ROC is the outside of a circle, $|z| > r_R$. It contains $z = \infty$ if and only if $x[n] = 0$ for $n < 0$.
- If $x$ is left-sided, the ROC is the inside of a circle, $|z| < r_L$.
- If $X$ is rational, the ROC contains no pole, and it is bounded by poles or extends to $0$ or $\infty$.

**Inverse.** For a circle $|z| = r$ inside the ROC,

$$x[n] = \frac{1}{2\pi i} \oint_{|z| = r} X(z)\, z^{n-1}\, dz.$$

For rational $X$, [partial fraction decomposition](/partial-fraction-decomposition/) in $z^{-1}$ gives the same answer: each term $c/(1 - p z^{-1})$ becomes $c\, p^n u[n]$ if the ROC lies outside $|z| = |p|$, and $-c\, p^n u[-n-1]$ if it lies inside.

**Properties.** Where $X$ has the ROC $R_x$ and $Y$ has $R_y$:

| sequence | transform | ROC |
|---|---|---|
| $a x[n] + b y[n]$ | $a X(z) + b Y(z)$ | contains $R_x \cap R_y$ |
| $x[n - n_0]$ | $z^{-n_0} X(z)$ | $R_x$, except perhaps $0$ or $\infty$ |
| $(x * y)[n]$ | $X(z)\, Y(z)$ | contains $R_x \cap R_y$ |
| $a^n x[n]$ | $X(z / a)$ | $\lvert a \rvert R_x$ |
| $n\, x[n]$ | $-z\, X'(z)$ | $R_x$ |
| $x[-n]$ | $X(1/z)$ | $1 / R_x$ |
| $\overline{x[n]}$ | $\overline{X(\bar z)}$ | $R_x$ |

For a causal $x$, the initial value is $x[0] = \lim_{z \to \infty} X(z)$.

**On the unit circle.** If the ROC contains $|z| = 1$, then $X(e^{i\omega}) = \sum_n x[n] e^{-i\omega n}$ is the DTFT, and $x \in \ell^1$. Conversely, $x \in \ell^1$ puts the unit circle in the ROC. A sequence in $\ell^2$ but not in $\ell^1$, such as the ideal lowpass response, has a DTFT in the mean-square sense but its ROC can be empty.

**Causality and stability.** For an LTI system with impulse response $h$ and transfer function $H(z)$: the system is causal if and only if the ROC of $H$ is the outside of a circle and contains $z = \infty$; it is [BIBO stable](/bibo-stability/) if and only if the ROC contains the unit circle. For a rational $H$ in lowest terms, both hold if and only if every pole lies strictly inside the unit circle, $|p| < 1$, and the ROC is $|z| > \max |p|$.

## Examples and non-examples

- $\delta[n] \leftrightarrow 1$, ROC all $z$. $\delta[n - n_0] \leftrightarrow z^{-n_0}$.
- The finite sequence $x = [1, 2, 3]$ at $n = 0, 1, 2$ has $X(z) = 1 + 2z^{-1} + 3z^{-2}$, ROC $z \ne 0$.
- $a^n u[n] \leftrightarrow \dfrac{1}{1 - a z^{-1}}$, ROC $|z| > |a|$: the geometric series in $a z^{-1}$.
- $-a^n u[-n-1] \leftrightarrow \dfrac{1}{1 - a z^{-1}}$, ROC $|z| < |a|$. Same formula, another sequence: the ROC is part of the transform.
- $n\, a^n u[n] \leftrightarrow \dfrac{a z^{-1}}{(1 - a z^{-1})^2}$, ROC $|z| > |a|$, from the rule for $n\, x[n]$.
- $\cos(\omega_0 n)\, u[n] \leftrightarrow \dfrac{1 - \cos(\omega_0) z^{-1}}{1 - 2\cos(\omega_0) z^{-1} + z^{-2}}$, ROC $|z| > 1$: two poles on the unit circle at $e^{\pm i\omega_0}$.
- **Three sequences for one formula.** $X(z) = \dfrac{1}{(1 - \frac{1}{2} z^{-1})(1 - 2 z^{-1})} = \dfrac{-1/3}{1 - \frac{1}{2} z^{-1}} + \dfrac{4/3}{1 - 2 z^{-1}}$ has three possible ROCs. For $|z| > 2$, $x[n] = \left(-\frac{1}{3} 2^{-n} + \frac{4}{3} 2^{n}\right) u[n]$: causal, not stable, and $x[0] = 1$, $x[1] = 5/2$. For $\frac{1}{2} < |z| < 2$, $x[n] = -\frac{1}{3} 2^{-n} u[n] - \frac{4}{3} 2^{n} u[-n-1]$: two-sided and stable. For $|z| < \frac{1}{2}$, $x[n] = \left(\frac{1}{3} 2^{-n} - \frac{4}{3} 2^{n}\right) u[-n-1]$: anticausal, not stable.
- **Non-example, empty ROC.** $x[n] = 1$ for all $n$: the right part needs $|z| > 1$ and the left part needs $|z| < 1$, so no $z$ works, and $x$ has no z-transform, although its DTFT exists as a distribution, $2\pi\delta(\omega)$ on $[-\pi, \pi]$.
- **Non-example, fast growth.** $x[n] = 2^{n^2} u[n]$ grows faster than any $r^n$, so its series diverges for every $z$.

## Related definitions

- [Discrete-time Fourier transform](/discrete-time-fourier-transform/): the z-transform on the unit circle.
- [Transfer function](/transfer-function/): the z-transform of an impulse response, a rational function for a difference equation.
- [Frequency response](/frequency-response/): the transfer function on the unit circle.
- [BIBO stability](/bibo-stability/): the condition that the ROC of $H$ contains the unit circle.
- [Generating functions](/generating-functions/): the same series in the variable $t = z^{-1}$, used for counting and for recurrences; see also [linear recurrences with constant coefficients](/linear-recurrences-with-constant-coefficients/).
- [Bilinear transform](/bilinear-transform/): the map between the Laplace variable $s$ and $z$ used to design digital filters from analog ones.
- [Filter bank](/filter-bank/) and [polyphase decomposition](/polyphase-decomposition/): multirate systems written with z-transforms of the subsequences.

## References
