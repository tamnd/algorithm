---
tag: BWFWVW
kind: problem
slug: discrete-convolution
name: Discrete convolution
aliases:
- linear convolution
- sequence convolution
area: graphics-and-signals/signal-processing
level: intro
summary: Given a signal x[n] and a filter h[n], compute the sequence y[n] = sum over k of h[k] x[n-k], the output of the LTI system with impulse response h.
prereqs: [convolution]
see_also: [linear-time-invariant-system, circular-convolution, overlap-add-method, overlap-save-method, convolution-via-fft, fir-filter, digital-filtering, linear-filtering]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 2, Sections 2.3 and 2.4 (the convolution sum of an LTI system and its properties) and Section 8.7 (linear convolution computed with the DFT)
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: Chapter 2 (the convolution sum) and Section 7.3, Linear Filtering Methods Based on the DFT
  - book: isbn:9780138147570
    title: Alan V. Oppenheim, Alan S. Willsky and S. Hamid Nawab, Signals and Systems, second edition, Prentice Hall, 1997
    locator: Chapter 2, Linear Time-Invariant Systems (the convolution sum)
---

Discrete convolution is the problem to compute $y[n] = \sum_k h[k]\, x[n-k]$ from a signal $x$ and a filter $h$, both sequences indexed by the integers. It is the signal-processing form of the algebraic [convolution](/convolution/) of two coefficient vectors: here the sequences can be two-sided and infinite, the filter is usually much shorter than the signal, and the output often has to come out one sample at a time. Every [linear time-invariant system](/linear-time-invariant-system/) computes it, with $h$ its [impulse response](/impulse-response/). For finite sequences of lengths $N$ and $M$, the defining sum costs $NM$ multiplications, and the FFT methods cost much less.

## In plain words

A filter is a short list of weights. To filter a signal, you slide the reversed list of weights along the signal. At each position, you multiply each weight by the sample under it and add the products. The sum is one output sample. Then you move one step and do it again.

Each input sample thus spreads a scaled copy of the weights into the output, and the output is the sum of all these copies. A sum of weights that is 1 and all positive gives a smoothing filter. Weights of opposite sign give a filter that responds to change.

## Definition

**Signals.** A signal is a sequence $x : \mathbb{Z} \to \mathbb{C}$, written $x[n]$. When it comes from a sampled signal, $n$ counts samples at the rate $f_s$. A finite signal of length $N$ starting at $n = 0$ is a sequence with $x[n] = 0$ outside $0 \le n \le N-1$.

**Input.** A signal $x$ and a filter $h$. In the finite case, $x$ has length $N$ and $h$ has length $M$, so the filter has order $M - 1$.

**Output.** The sequence

$$y[n] = (x * h)[n] = \sum_{k=-\infty}^{\infty} x[k]\, h[n-k] = \sum_{k=-\infty}^{\infty} h[k]\, x[n-k], \qquad n \in \mathbb{Z},$$

for each $n$ where the sum converges. The two forms are equal by the change of index $k \mapsto n - k$. In the finite case only the indices $0 \le k \le N-1$ with $0 \le n - k \le M - 1$ contribute, so $y[n] = 0$ outside $0 \le n \le N + M - 2$, and the output has length $N + M - 1$.

**Support.** If $x$ is zero outside $[a, b]$ and $h$ is zero outside $[c, d]$, then $y$ is zero outside $[a + c, b + d]$. A filter with $h[k] = 0$ for $k < 0$ is *causal*: $y[n]$ then depends only on $x[n], x[n-1], \ldots$.

**Convergence.** For infinite sequences the sum need not converge. It converges absolutely for every $n$ in these cases:

- $h \in \ell^1$ and $x$ bounded: $|y[n]| \le \sup_k |x[k]| \cdot \sum_k |h[k]|$. This is the case of a [BIBO stable](/bibo-stability/) filter.
- $x, h \in \ell^1$: then $y \in \ell^1$ and $\sum_n y[n] = \left(\sum_n x[n]\right)\left(\sum_n h[n]\right)$.
- $x, h \in \ell^2$: then $|y[n]| \le \|x\|_2 \|h\|_2$ by the Cauchy-Schwarz inequality, so $y$ is bounded.
- $x$ and $h$ both zero for $n < n_0$ (both right-sided): each sum is finite.

**Algebra.** Where the sums converge absolutely, convolution is commutative, associative and distributive over addition, and the unit impulse $\delta[n]$ ($1$ at $n = 0$, else $0$) is its identity. A shift of $x$ by $n_0$ shifts $y$ by $n_0$. Associativity can fail without absolute convergence: see the examples.

## Variants

- **Full, same and valid.** For finite signals, the *full* output has all $N + M - 1$ samples. The *same* output keeps $N$ samples aligned with $x$, here $y[\lfloor (M-1)/2 \rfloor \ldots \lfloor (M-1)/2 \rfloor + N - 1]$. The *valid* output keeps only the $N - M + 1$ samples where the filter lies entirely over $x$, $y[M-1 \ldots N-1]$, and is empty if $M > N$. Libraries name these modes the same way, but they center the same output differently when $M$ is even.
- **Streaming.** The input arrives one sample at a time and each $y[n]$ must be output before $x[n+1]$ arrives, or after a fixed delay. This is the setting of [digital filtering](/digital-filtering/).
- **Circular convolution.** For two blocks of length $L$, indices are taken modulo $L$. [Circular convolution](/circular-convolution/) is what the DFT computes, and it equals the linear one only with enough zero padding.
- **Infinite impulse response.** If $h$ is infinite but has a rational [transfer function](/transfer-function/), the convolution is computed by a recursive difference equation, see the [IIR filter](/iir-filter/), not by the sum.
- **Correlation.** The [cross-correlation](/cross-correlation/) $\sum_k x[k]\, h[k+n]$ is the convolution of $x$ with the reversed conjugate of $h$.
- **Two and more dimensions.** For images, the same sum runs over two indices; see [linear filtering](/linear-filtering/) for that technique.
- **Exact.** Over the integers or modulo a prime, as in polynomial and integer multiplication; see [convolution](/convolution/).

## Examples

- $x = [1, 2, 3, 4, 5]$ and the difference filter $h = [1, 0, -1]$. The full output is $[1, 2, 2, 2, 2, -4, -5]$. The same output is $[2, 2, 2, 2, -4]$ and the valid output is $[2, 2, 2]$: in the middle, each sample is $x[n] - x[n-2] = 2$. The sums agree with the identity of sums: $15 \cdot 0 = 0$.
- The moving average $h = [1/3, 1/3, 1/3]$ applied to $x = [3, 6, 9, 3]$ gives $[1, 3, 6, 6, 4, 1]$.
- $x * \delta[n - n_0] = x[n - n_0]$: convolution with a shifted impulse is a delay.
- The unit step $u[n]$ ($1$ for $n \ge 0$) convolved with itself gives $(n + 1)\, u[n]$. Both are right-sided, so each sum is finite, though neither is in $\ell^1$.
- **Non-example of associativity.** Let $a[n] = 1$ for all $n$, $b = \delta[n] - \delta[n-1]$ and $c = u[n]$. Then $a * b = 0$, so $(a * b) * c = 0$. But $b * c = \delta$, so $a * (b * c) = a \ne 0$. The product $a * c$ does not converge, which is why the rule breaks.

## Known algorithms

For finite signals of lengths $N \ge M$:

| method | cost | output delay | notes |
|---|---|---|---|
| defining sum (direct form) | $NM$ multiplications, $M$ per output sample | none | exact on integers; best for small $M$ |
| [convolution via FFT](/convolution-via-fft/) | $O((N + M) \log(N + M))$ | the whole input | one transform of length at least $N + M - 1$ |
| [overlap-add method](/overlap-add-method/) | $O(N \log M)$, $O(\log M)$ per output sample | one block, about $M$ samples | blocks of the input, tails added |
| [overlap-save method](/overlap-save-method/) | $O(N \log M)$, $O(\log M)$ per output sample | one block, about $M$ samples | overlapping blocks, wrapped outputs discarded |
| [Karatsuba multiplication](/karatsuba-multiplication/) | $O(N\, M^{0.585})$ in blocks of $M$ | depends on the blocking | exact, no roots of unity |
| [number-theoretic transform](/number-theoretic-transform/) | $O((N + M) \log(N + M))$ | the whole input | exact modulo a prime |

The [FIR filter](/fir-filter/) page describes the direct form as a filter structure, and [convolution](/convolution/) lists more algorithms for the algebraic problem.

## Bounds

The output has $N + M - 1$ samples, each of which depends on the input, so $\Omega(N + M)$ operations are necessary. The best known upper bound in the [real RAM](/real-ram/) with exact complex arithmetic is $O((N + M) \log(N + M))$ by the FFT, and $O(N \log M)$ by sectioned FFT methods when $M \le N$. The lower bounds known in restricted models, such as the exact number of multiplications in a bilinear algorithm, are on the [convolution](/convolution/) page. For a stream, the direct form has no delay and costs $M$ multiplications per sample; a block FFT method of block length $B$ has a delay of about $B$ samples. Hybrid methods combine a short direct-form part with FFT blocks of growing size, and give zero delay at a cost far below $M$ per sample, see [digital filtering](/digital-filtering/).

## Reductions

- **To and from polynomial multiplication.** The full convolution of $x$ and $h$ is the coefficient vector of the product of $\sum_n x[n] t^n$ and $\sum_n h[n] t^n$, so the two problems are the same; see [polynomial multiplication](/polynomial-multiplication/).
- **To circular convolution.** Pad both inputs with zeros to a length $L \ge N + M - 1$. The circular convolution of length $L$ then equals the linear one, at no extra cost but the padding; see [circular convolution](/circular-convolution/).
- **Long to short.** A convolution of a length-$N$ signal with a length-$M$ filter splits into $\lceil N/B \rceil$ convolutions of a block of length $B$ with the filter, plus $O(N)$ additions; this is the overlap-add method.
- **Correlation to convolution.** Reverse and conjugate one input, in $O(M)$ time.

## Applications

- FIR filtering of audio, radio and sensor data: smoothing, differentiation, band selection.
- Reverberation by convolution with a measured room impulse response, which can be several seconds long.
- The response of any LTI system to an input, when its impulse response is known.
- Blur and sharpening of images, through the 2D form, see [linear filtering](/linear-filtering/) and the [point spread function](/point-spread-function/).
- Detection of a known pulse in noise with a [matched filter](/matched-filter/).
- Multiplication of polynomials and large integers.

## References
