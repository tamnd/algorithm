---
tag: 1Z8N2K
kind: definition
slug: impulse-response
name: Impulse response
aliases:
- unit sample response
area: graphics-and-signals/signal-processing
level: core
summary: The output h[n] of a system when the input is the unit impulse. For an LTI system it fixes the system, since the output for any input x is the convolution x * h.
prereqs: [linear-time-invariant-system]
see_also: [discrete-convolution, transfer-function, frequency-response, bibo-stability, fir-filter, iir-filter, point-spread-function]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 2, Sections 2.3 to 2.5 (the impulse response of an LTI system, its causality and stability, FIR and IIR systems, and the impulse response of a difference equation)
  - book: isbn:9780138147570
    title: Alan V. Oppenheim, Alan S. Willsky and S. Hamid Nawab, Signals and Systems, second edition, Prentice Hall, 1997
    locator: Chapter 2, Linear Time-Invariant Systems (the representation of signals by shifted impulses and the convolution sum)
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: Chapter 2, Discrete-Time Signals and Systems
---

The impulse response of a discrete-time system is its output $h[n]$ when the input is the unit impulse $\delta[n]$. For a [linear time-invariant system](/linear-time-invariant-system/) it is the whole description: the output for an input $x$ is the [discrete convolution](/discrete-convolution/) $y = x * h$. Its z-transform is the [transfer function](/transfer-function/) and its DTFT is the [frequency response](/frequency-response/), and the two properties that matter most for a filter, causality and stability, are conditions on $h$.

## Definition

**Notation.** A signal is a sequence $x[n]$, $n \in \mathbb{Z}$. The unit impulse is $\delta[n] = 1$ for $n = 0$ and $\delta[n] = 0$ for $n \ne 0$. Frequencies $\omega$ are in radians per sample.

**Definition.** The impulse response of a system $T$ is

$$h = T\delta, \qquad h[n] = (T\delta)[n],$$

the output at time $n$ when the input is an impulse at time $0$, with the system at rest before the impulse.

**Properties for an LTI system.** Let $T$ be linear and time invariant.

- *Shifted impulses.* The response to $\delta[n - k]$ is $h[n - k]$, by time invariance.
- *Convolution.* Each finite-support input is $x = \sum_k x[k]\, \delta[n-k]$, so linearity gives $(T x)[n] = \sum_k x[k]\, h[n - k]$. Under the continuity hypothesis of the [LTI system](/linear-time-invariant-system/) page, the same holds for inputs of infinite support.
- *Causality.* The system is causal if and only if $h[n] = 0$ for all $n < 0$.
- *Stability.* The system is BIBO stable if and only if $\sum_n |h[n]| < \infty$; see [BIBO stability](/bibo-stability/).
- *Length.* If $h[n] \ne 0$ only for $0 \le n \le M - 1$, with $h[M-1] \ne 0$, the system is a finite impulse response (FIR) system of length $M$ and order $M - 1$. Otherwise it is an infinite impulse response (IIR) system.

**Step response.** The response to the unit step $u[n]$ (equal to $1$ for $n \ge 0$) is $s[n] = \sum_{k \le n} h[k]$, and $h[n] = s[n] - s[n-1]$. For a causal system both carry the same information.

**From a difference equation.** For a causal system $\sum_{k=0}^{p} a_k y[n-k] = \sum_{k=0}^{q} b_k x[n-k]$ with $a_0 \ne 0$ at initial rest, the impulse response comes from running the recursion on $x = \delta$: $h[n] = \frac{1}{a_0}\left(b_n - \sum_{k=1}^{p} a_k h[n-k]\right)$, with $b_n = 0$ for $n > q$ and $h[n] = 0$ for $n < 0$.

## Examples and non-examples

- **Delay.** $y[n] = x[n - n_0]$ has $h = \delta[n - n_0]$. The identity system has $h = \delta$.
- **Moving average.** $y[n] = \frac{1}{3}(x[n] + x[n-1] + x[n-2])$ has $h = [1/3, 1/3, 1/3]$ at $n = 0, 1, 2$: FIR of length 3, causal and stable.
- **First-order recursion.** $y[n] = \frac{1}{2} y[n-1] + x[n]$ has $h[n] = 2^{-n}$ for $n \ge 0$: the samples are $1, 1/2, 1/4, 1/8, \ldots$. It is IIR, causal and stable, and $\sum_n |h[n]| = 2$.
- **Accumulator.** $y[n] = \sum_{k \le n} x[k]$ has $h = u$, the unit step. It is causal and IIR, and not stable, because $\sum_n |h[n]|$ diverges: the bounded input $u$ gives the output $n + 1$.
- **Ideal lowpass filter.** The filter that keeps $|\omega| < \omega_c$ and removes the rest has $h[n] = \sin(\omega_c n)/(\pi n)$, with $h[0] = \omega_c / \pi$. It is IIR in both directions, not causal, and not in $\ell^1$, although it is in $\ell^2$. A practical FIR design truncates and windows it; see [window functions](/window-functions/).
- **Measured responses.** A room or a loudspeaker is measured by its impulse response, recorded with a short click or derived from a swept sine. Convolving dry audio with a room response of several seconds adds the reverberation of the room.
- **Non-example, nonlinear.** The centered 3-point [median filter](/median-filter/) maps $\delta$ to $0$, but it is not the zero system: it maps $u$ to $u$. A nonlinear system is not described by its impulse response.
- **Non-example, time varying.** For $y[n] = n\, x[n]$, the response to $\delta$ is $0$, while the response to $\delta[n - 1]$ is $\delta[n - 1]$. The responses to shifted impulses are not shifts of each other, so the system is not convolution with $T\delta$.

## Related definitions

- [Transfer function](/transfer-function/): the z-transform $H(z) = \sum_n h[n] z^{-n}$ with its region of convergence.
- [Frequency response](/frequency-response/): the DTFT $H(e^{i\omega}) = \sum_n h[n] e^{-i\omega n}$, which exists for $h \in \ell^1$.
- [BIBO stability](/bibo-stability/): the condition $h \in \ell^1$.
- [FIR filter](/fir-filter/) and [IIR filter](/iir-filter/): the two classes by the length of $h$.
- [Point spread function](/point-spread-function/): the impulse response of an imaging system, on two indices.
- [Matched filter](/matched-filter/): the filter whose impulse response is a reversed, conjugated copy of the pulse to detect.
- [Minimum phase](/minimum-phase/): among the impulse responses with one magnitude response, the one with the most energy early.

## References
