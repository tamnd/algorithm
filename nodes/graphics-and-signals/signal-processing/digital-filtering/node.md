---
tag: 6CQQM0
kind: problem
slug: digital-filtering
name: Digital filtering
area: graphics-and-signals/signal-processing
level: intro
summary: Given a sampled signal and a linear filter, as FIR taps or a difference equation, compute the filtered signal, often as a stream with a bounded delay and cost per sample.
prereqs: [linear-time-invariant-system, discrete-convolution, transfer-function]
see_also: [fir-filter, iir-filter, overlap-add-method, overlap-save-method, digital-filter-design, frequency-response, adaptive-filtering, linear-filtering]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 6, Structures for Discrete-Time Systems (direct, cascade and parallel forms of FIR and IIR systems) and Section 8.7.3, Implementing Linear Time-Invariant Systems Using the DFT
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: Section 7.3, Linear Filtering Methods Based on the DFT
  - paper: "William G. Gardner, Journal of the Audio Engineering Society 43(3), March 1995"
    title: William G. Gardner, Efficient convolution without input-output delay, Journal of the Audio Engineering Society 43(3), 1995, 127 to 136
    locator: the hybrid of a direct-form head and FFT blocks that gives a convolution with no input-output delay
---

Digital filtering is the problem to compute the output of a linear time-invariant filter for a sampled signal: the convolution of the signal with a finite impulse response, or the solution of a recursive difference equation. It is the one-dimensional signal problem behind equalizers, noise removal, channel filters and the anti-aliasing step before a change of the sampling rate. In practice the signal is a stream, so the problem also fixes the cost per output sample and the delay from input to output, and the methods trade one against the other. For images, the two-dimensional technique is [linear filtering](/linear-filtering/); this page is about sequences in time.

## In plain words

A sensor or a microphone gives a stream of numbers, many thousands per second. You want to change the stream: remove a hum, keep only the low tones, smooth the noise. A filter does this with a fixed rule. Each output number is a weighted sum of the latest input numbers, and in some filters also of the latest output numbers.

The task is to run that rule on the whole stream. You must keep up with the rate of the stream, and the output must not come too late. A long rule is slow if you compute each sum alone, so fast methods work on blocks of numbers at a time, at the price of a small wait.

## Definition

**Signals.** The input is a signal $x[n]$ sampled at the rate $f_s$, either a finite block $x[0 \ldots N-1]$ or a stream that starts at $n = 0$. Frequencies $\omega$ are in radians per sample, $\omega \in [-\pi, \pi]$, with $\omega = \pi$ at $f_s / 2$.

**The filter.** One of two forms:

- *FIR.* Coefficients $h[0], \ldots, h[M-1]$, order $M - 1$. The output is $y[n] = \sum_{k=0}^{M-1} h[k]\, x[n-k]$.
- *Rational (IIR).* Coefficients $b_0, \ldots, b_q$ and $a_0, \ldots, a_p$ with $a_0 \ne 0$. The output is the solution of $\sum_{k=0}^{p} a_k\, y[n-k] = \sum_{k=0}^{q} b_k\, x[n-k]$ with initial rest ($x[n] = y[n] = 0$ for $n < 0$), or with a given initial state. Its transfer function is $H(z) = B(z)/A(z)$.

In both cases $x[n] = 0$ for $n < 0$, and the filter is causal. Its stability and phase are properties of the input data: an FIR filter is always [BIBO stable](/bibo-stability/), an IIR filter is stable when the poles of $H$ in lowest terms are inside the unit circle, and a filter has linear phase when its impulse response is symmetric.

**Output.** For a block, $y[0 \ldots N + M - 2]$ for an FIR filter, or $y[0 \ldots N-1]$, or as many samples as asked. For a stream with a delay $D \ge 0$, the sample $y[n]$ must be output before $x[n + D + 1]$ is read. The cost measure is the number of arithmetic operations per output sample, and the memory for the state.

## Variants

- **FIR or IIR.** FIR filters can have exact linear phase and are always stable; IIR filters reach a sharp [frequency response](/frequency-response/) with far fewer coefficients, but have a nonlinear phase and need care with stability and rounding. See [FIR filter](/fir-filter/) and [IIR filter](/iir-filter/).
- **Streaming or offline.** A stream asks for a bounded delay. An offline signal can be filtered with any delay, or with a non-causal filter.
- **Zero-phase filtering.** Offline, run a causal filter forward, reverse the result, run the filter again and reverse again. The total frequency response is $|H(e^{i\omega})|^2$, real and nonnegative, so there is no phase shift, but the filter is not causal.
- **Multirate filtering.** Filter and keep every $L$-th output (decimation), or insert zeros and filter (interpolation). [Polyphase decomposition](/polyphase-decomposition/) computes only the samples that are kept; see [sample-rate conversion](/sample-rate-conversion/) and [polyphase resampling](/polyphase-resampling/).
- **Adaptive filtering.** The coefficients change with time to follow a target, as in [adaptive filtering](/adaptive-filtering/) and the [LMS algorithm](/lms-algorithm/). The system is then linear but not time invariant.
- **Fixed point.** Coefficients and state are integers of a fixed width, which adds rounding noise, limit cycles and overflow to the problem.
- **Two dimensions.** Images are filtered by the same sums over two indices, see [linear filtering](/linear-filtering/) and the [separable filter](/separable-filter/).

## Examples

- **Moving average, block.** The FIR filter $h = [\frac{1}{3}, \frac{1}{3}, \frac{1}{3}]$ on $x = [3, 6, 9, 3]$ gives $y = [1, 3, 6, 6, 4, 1]$. It is causal, stable and linear phase, with group delay $1$ sample, and it removes $\omega = 2\pi/3$.
- **First-order recursion, stream.** $y[n] = \frac{1}{2} y[n-1] + x[n]$ is a causal, stable IIR lowpass filter with one pole at $\frac{1}{2}$; it is not linear phase. The impulse gives $1, \frac{1}{2}, \frac{1}{4}, \frac{1}{8}, \ldots$. The step $x = u$ gives $1, \frac{3}{2}, \frac{7}{4}, \frac{15}{8}, \ldots$, which tends to $2 = H(1)$, the gain at $\omega = 0$. It costs one multiplication and one addition per sample, though its impulse response is infinite.
- **Zero phase.** Filtering forward and backward with $h = [\frac{1}{2}, \frac{1}{2}]$ is the same as filtering once with $[\frac{1}{4}, \frac{1}{2}, \frac{1}{4}]$ centered at $n = 0$, whose frequency response $\cos^2(\omega/2)$ is real.
- **An unstable input.** The filter $y[n] = 2y[n-1] + x[n]$ is causal and not stable. On the step input its output $2^{n+1} - 1$ overflows any fixed format; the problem is well posed, but the result is useless.

## Known algorithms

| method | cost per output sample | delay | when |
|---|---|---|---|
| direct form of an [FIR filter](/fir-filter/) | $M$ multiplications | 0 | short filters |
| [overlap-add method](/overlap-add-method/) | $O(\log M)$, with FFTs of length about $2M$ | about $M$ samples | long filters, frames |
| [overlap-save method](/overlap-save-method/) | $O(\log M)$ | about $M$ samples | long filters, streams |
| uniformly partitioned FFT convolution, partitions of $B$ | $O(\log B + M/B)$ | about $B$ samples | long filters, short delay |
| hybrid of a direct head and growing FFT blocks (Gardner 1995) | far below $M$ | 0 | very long filters, no delay |
| [convolution via FFT](/convolution-via-fft/) of the whole block | $O(\log(N + M))$ | the whole signal | offline |
| difference equation, direct or cascade form of an [IIR filter](/iir-filter/) | $p + q + 1$ multiplications | 0 | rational filters |
| [polyphase decomposition](/polyphase-decomposition/) for decimation by $L$ | $M / L$ per input sample | 0 | multirate |

For the partitioned method, each block of $B$ samples costs one FFT and one inverse FFT of length $2B$, which is $O(B \log B)$, and one product of length $2B$ for each of the $\lceil M / B \rceil$ partitions of $h$, which is $O(M)$; per sample this is $O(\log B + M/B)$. The [Savitzky-Golay filter](/savitzky-golay-filter/) and the [matched filter](/matched-filter/) are FIR filters with special coefficients. The [median filter](/median-filter/) is not linear and is not an instance of this problem.

## Bounds

Offline, every input sample can change the output, so $\Omega(N + M)$ operations are necessary; the best known upper bound for an FIR filter is $O(N \log M)$ with sectioned FFTs, and the [convolution](/convolution/) page gives the lower bounds known in restricted models. For a stream, the direct form costs $\Theta(M)$ per sample with no delay, and block FFT methods with a delay of $B$ samples cost $O(\log B + M/B)$ per sample, which is $O(\log M)$ for $B = \Theta(M)$. A rational filter of orders $p$ and $q$ costs $\Theta(p + q)$ per sample in its difference equation, whatever the length of its impulse response; no FIR method matches this for an IIR response, which has infinite length.

## Reductions

- **FIR filtering is discrete convolution.** A block FIR filter is exactly the [discrete convolution](/discrete-convolution/) of the signal with $h$, so every convolution algorithm applies.
- **IIR filtering is a triangular Toeplitz solve.** For $N$ samples at initial rest, the difference equation reads $T_A\, y = T_B\, x$, with $T_A$ and $T_B$ lower triangular banded Toeplitz matrices of the coefficients. Forward substitution in $O(pN)$ is the recursion; see [Toeplitz system solving](/toeplitz-system-solving/).
- **IIR to FIR.** A stable IIR filter is approximated to any accuracy by truncating its impulse response at the point where $\sum_{n > M} |h[n]|$ is small enough, and then filtering by FFT. This pays off only when $p + q$ is not small.
- **Zero-phase to causal.** Two causal passes and two reversals, at twice the cost.
- **Two dimensions to one.** A separable 2D filter is a 1D filter along the rows, then along the columns.

## Applications

- Audio: equalizers, crossovers, reverberation by convolution with a measured impulse response, and loudness and hum filters.
- Communications: pulse shaping, channel selection, and the [matched filter](/matched-filter/) at the receiver.
- Anti-aliasing and anti-imaging filters in [sample-rate conversion](/sample-rate-conversion/), so that the [aliasing](/aliasing/) stays below a target level.
- Measurement and biomedical signals: removal of baseline drift and of power-line interference, and smoothing of sensor data.
- [Signal denoising](/signal-denoising/) with fixed or adaptive filters, and the [Wiener filter](/wiener-filter/).

## References
