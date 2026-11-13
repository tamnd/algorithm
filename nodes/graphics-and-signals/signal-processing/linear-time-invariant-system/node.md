---
tag: KCV6D8
kind: model
slug: linear-time-invariant-system
name: Linear time-invariant system
aliases:
- LTI system
area: graphics-and-signals/signal-processing
level: core
summary: A map from input to output sequences that is linear and commutes with shifts in time. Its impulse response fixes it, and its output is the convolution of the input with that response.
prereqs: [discrete-convolution]
see_also: [impulse-response, transfer-function, frequency-response, bibo-stability, state-space-model, fir-filter, iir-filter, linear-filtering]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 2, Sections 2.2 to 2.5 (linearity, time invariance, causality and stability, the convolution sum, and linear constant-coefficient difference equations) and Section 2.6.1 (complex exponentials as eigenfunctions)
  - book: isbn:9780138147570
    title: Alan V. Oppenheim, Alan S. Willsky and S. Hamid Nawab, Signals and Systems, second edition, Prentice Hall, 1997
    locator: Chapter 1 (system properties) and Chapter 2, Linear Time-Invariant Systems
  - paper: doi:10.1109/TCSI.2003.812614
    title: Irwin W. Sandberg, Causality and the impulse response scandal, IEEE Transactions on Circuits and Systems I 50(6), 2003
    locator: the whole paper (linear time-invariant maps that have no impulse-response representation)
---

A linear time-invariant (LTI) system is a map $T$ from input sequences $x[n]$ to output sequences $y[n]$ that is linear and commutes with a shift of time. It is the cost and behavior model under almost all of signal processing: an LTI system is fixed by its [impulse response](/impulse-response/) $h = T\delta$, and its output is the [discrete convolution](/discrete-convolution/) $y = x * h$. The complex sinusoids $e^{i\omega n}$ pass through it with only a change of amplitude and phase, which gives the [frequency response](/frequency-response/). The model also says what an implementation costs: multiplications per output sample, memory for the state, and the delay from input to output.

## The machine

**Signals.** A signal is a sequence $x : \mathbb{Z} \to \mathbb{C}$. When it comes from sampling, $n$ counts samples at the rate $f_s$, and frequencies $\omega$ are in radians per sample, with $\omega \in [-\pi, \pi]$; $\omega = \pi$ is the frequency $f_s / 2$. The shift by $n_0$ is $(S_{n_0} x)[n] = x[n - n_0]$. The unit impulse is $\delta[n] = 1$ for $n = 0$ and $0$ otherwise.

**System.** A system is a map $T : \mathcal{X} \to \mathcal{Y}$ between spaces of sequences. The input space $\mathcal{X}$ is closed under addition, scalar multiples and shifts, for example the finite-support sequences, $\ell^1$, or the bounded sequences $\ell^\infty$. The system is

- *linear* if $T(a x_1 + b x_2) = a\, T x_1 + b\, T x_2$ for all inputs $x_1, x_2$ and scalars $a, b$;
- *time invariant* if $T(S_{n_0} x) = S_{n_0}(T x)$ for all inputs $x$ and integers $n_0$;
- *causal* if $(Tx)[n]$ depends only on $x[k]$ for $k \le n$;
- *stable* in the BIBO sense if each bounded input gives a bounded output, see [BIBO stability](/bibo-stability/).

An LTI system is linear and time invariant. Linear and time-invariant are two independent conditions: $y[n] = n\, x[n]$ is linear and not time invariant, and $y[n] = x[n]^2$ is time invariant and not linear.

**The impulse response fixes the system.** Let $h = T\delta$. Each finite-support input is a finite sum of shifted impulses, $x = \sum_k x[k]\, S_k \delta$. Linearity and time invariance give

$$T x = \sum_k x[k]\, S_k (T\delta), \qquad (T x)[n] = \sum_k x[k]\, h[n-k] = (x * h)[n].$$

So on finite-support inputs, $T$ is convolution with $h$, and two LTI systems with the same impulse response agree on all of them. For inputs of infinite support, the step from the finite sums to the infinite sum needs a continuity hypothesis: $T$ must commute with the limit of the truncations $x_K = \sum_{|k| \le K} x[k]\, S_k \delta$. If the inputs are in $\ell^p$ with $p < \infty$ and each output sample $(T x)[n]$ depends continuously on $x$ in the $\ell^p$ norm, then $x_K \to x$ in that norm, and $T x = x * h$. For bounded inputs, $x_K$ does not tend to $x$ in the sup norm, and continuity in the sup norm is not enough; the example at the end of this page is continuous in the sup norm and is not a convolution.

**A machine to run it.** An implementation reads one input sample and writes one output sample per step. A finite impulse response filter of length $M$ keeps the last $M - 1$ inputs as its state. A system with a rational [transfer function](/transfer-function/) of orders $p$ and $q$ keeps $p + q$ past values, or a state vector of dimension $\max(p, q)$ in a [state-space model](/state-space-model/).

## What it counts

- **Multiplications per output sample.** The direct form of a length-$M$ FIR filter costs $M$ multiplications per sample. A block FFT method costs $O(\log M)$ per sample, see the [overlap-add method](/overlap-add-method/) and the [overlap-save method](/overlap-save-method/). A recursive filter of orders $p$ and $q$ costs $p + q + 1$ per sample, whatever the length of its impulse response.
- **State.** The number of stored values, $M - 1$ for an FIR filter in direct form, $\max(p, q)$ for a recursive filter in a canonical form.
- **Delay.** The number of samples between the arrival of $x[n]$ and the output of $y[n]$. The direct form has none; a block method of block length $B$ has about $B$.
- **Arithmetic.** In the [real RAM](/real-ram/), each operation on a real or complex number costs one unit and is exact. In fixed or floating point, the coefficients and the state are rounded, which can move poles and change stability.

## Relation to other models

- **Linear time-varying systems.** Linearity alone gives $y[n] = \sum_k g[n, k]\, x[k]$ with $g[n, k] = (T S_k \delta)[n]$ on finite-support inputs. Time invariance is the condition $g[n, k] = h[n - k]$: a Toeplitz kernel.
- **Nonlinear systems.** The [median filter](/median-filter/) is time invariant and not linear, so no impulse response describes it.
- **Shift-invariant systems on $\mathbb{Z}^2$.** For images, the shift runs over two indices, and the output is a 2D convolution with the point spread function; see [linear filtering](/linear-filtering/) and the [point spread function](/point-spread-function/).
- **Continuous time.** The same definitions with $t \in \mathbb{R}$ give continuous-time LTI systems, with the convolution integral and the Laplace transform. A sampled LTI system is a discrete-time LTI system only if the sampling avoids [aliasing](/aliasing/).
- **Finite-dimensional systems.** A causal LTI system has a finite-dimensional [state-space model](/state-space-model/) if and only if its transfer function is rational. The [Kalman filter](/kalman-filter/) works on state-space models that are linear and possibly time varying.

## Known results in the model

- **Convolution.** On finite-support inputs, $y = x * h$ with $h = T\delta$. The convolution of finite sequences is commutative and associative, so a cascade of LTI systems does not depend on the order, and its impulse response is $h_1 * h_2$. A parallel connection has the impulse response $h_1 + h_2$.
- **Causality.** A system $y = x * h$ is causal if and only if $h[n] = 0$ for all $n < 0$.
- **Stability.** A system $y = x * h$ is BIBO stable if and only if $\sum_n |h[n]| < \infty$, see [BIBO stability](/bibo-stability/).
- **Eigenfunctions.** If $h \in \ell^1$, then $T e^{i\omega n} = H(e^{i\omega})\, e^{i\omega n}$ with $H(e^{i\omega}) = \sum_k h[k] e^{-i\omega k}$, the [frequency response](/frequency-response/). In the frequency domain, convolution becomes multiplication: $Y(e^{i\omega}) = H(e^{i\omega}) X(e^{i\omega})$, by the [convolution theorem](/convolution-theorem/).
- **Transfer function.** With the [z-transform](/z-transform/), $Y(z) = H(z) X(z)$ in the common region of convergence. A system described by a linear constant-coefficient difference equation, with initial rest, has a rational $H(z)$; see [transfer function](/transfer-function/).
- **Inverse systems.** The inverse of $H$ has the transfer function $1/H(z)$. It is causal and stable exactly when $H$ is [minimum phase](/minimum-phase/).
- **No representation without continuity.** On the space of convergent sequences, the system $(T x)[n] = \lim_{k \to \infty} x[k]$ for every $n$ is linear and time invariant. Its impulse response is $T\delta = 0$, yet $T u = 1$ for the unit step $u$. So the impulse response does not fix an LTI system on all inputs unless a continuity hypothesis holds. Sandberg gives such examples for continuous-time systems and calls the gap in the textbook argument a scandal.

## References
