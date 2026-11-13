---
tag: 7902ZW
kind: problem
slug: digital-filter-design
name: Digital filter design
aliases:
- filter design
area: graphics-and-signals/signal-processing
level: core
summary: "Given band edges and allowed ripples for a frequency response, find the FIR taps or IIR coefficients of a filter that meets them, with as few multiplies per output sample as possible."
prereqs: [frequency-response, fir-filter, iir-filter]
see_also: [parks-mcclellan-algorithm, butterworth-filter, bilinear-transform, window-functions, digital-filtering, gibbs-phenomenon, minimum-phase, least-squares-approximation]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 7, Filter Design Techniques (7.1 the specifications, 7.2 and 7.3 IIR design from analog filters and the bilinear transform, 7.5 and 7.6 FIR design by windowing and the Kaiser window, 7.7 optimum FIR approximations and the length estimate)
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: the chapter on the design of digital filters (FIR design by windows, frequency sampling and the minimax method, and IIR design by impulse invariance and the bilinear transform); general locator
  - paper: doi:10.1109/TCT.1972.1083419
    title: Thomas W. Parks and James H. McClellan, Chebyshev Approximation for Nonrecursive Digital Filters with Linear Phase, IEEE Transactions on Circuit Theory 19(2), 1972
    locator: pp. 189 to 194 (FIR design with fixed band edges as weighted Chebyshev approximation)
  - paper: doi:10.1109/PROC.1967.5434
    title: Charles M. Rader and Bernard Gold, Digital Filter Design Techniques in the Frequency Domain, Proceedings of the IEEE 55(2), 1967
    locator: pp. 149 to 171 (recursive digital filters, their design from analog filters and from frequency specifications)
---

Digital filter design is the problem to choose the coefficients of a digital filter so that its [frequency response](/frequency-response/) meets a specification. A typical low-pass specification gives a pass band $[0, \omega_p]$ where the gain must stay within $1 \pm \delta_p$, a stop band $[\omega_s, \pi]$ where it must stay below $\delta_s$, and a transition band between them where it is free. The answer is the taps of an [FIR filter](/fir-filter/) or the coefficients of an [IIR filter](/iir-filter/) of a recursive difference equation. A design is good if it meets the specification with few multiplies per output sample, and often also with linear phase, a short delay or a minimum phase. Frequencies on this page are $\omega$ in radians per sample, $\omega \in [-\pi, \pi]$, and $\Omega$ in radians per second for analog prototypes. Computing the output of a given filter is the separate problem of [digital filtering](/digital-filtering/).

## In plain words

You know which tones a filter should keep and which it should remove, and how much error you can accept in each. Between the two groups there is a gap where you do not care. Filter design finds the numbers inside the filter that do the job.

There is always a trade. A narrower gap or smaller errors need a longer filter, which costs more work for each sample. A filter that feeds its output back into itself can be much shorter, but it delays different tones by different amounts and can become unstable. A filter without feedback is always stable and can delay all tones equally, but it needs more work.

## Definition

**Input.** A specification of the magnitude response $|H(e^{i\omega})|$ on $[0, \pi]$, given as a set of bands. For a low-pass filter it is

$$1 - \delta_p \le |H(e^{i\omega})| \le 1 + \delta_p \ \text{ for } 0 \le \omega \le \omega_p, \qquad |H(e^{i\omega})| \le \delta_s \ \text{ for } \omega_s \le \omega \le \pi,$$

with $0 < \omega_p < \omega_s < \pi$. In decibels the pass band ripple is about $20\log_{10}\big((1 + \delta_p)/(1 - \delta_p)\big)$ and the stop band attenuation is $-20\log_{10}\delta_s$. An edge given in hertz as $f$ at the sample rate $f_s$ is $\omega = 2\pi f/f_s$. The input also says which class of filters is allowed: FIR or IIR, linear phase or not, real coefficients, and sometimes a bound on the order or the delay.

**Output.** For an FIR filter, taps $h[0], \ldots, h[N-1]$ with $H(e^{i\omega}) = \sum_n h[n] e^{-i\omega n}$. For an IIR filter, coefficients $b_0, \ldots, b_q$ and $a_1, \ldots, a_p$ with $H(z) = \sum_k b_k z^{-k} / (1 + \sum_k a_k z^{-k})$, and all poles inside the unit circle so that the causal filter is stable.

**Goal.** Meet the specification with the smallest cost, usually the order or the number of multiplies per output sample. The optimization form fixes the order and minimizes an error, for example the largest weighted error over the bands, or the weighted squared error.

## Variants

- **Band shapes.** High-pass, band-pass, band-stop and multiband filters have more edges. Differentiators and Hilbert transformers have a desired response that is not piecewise constant.
- **FIR with linear phase.** Symmetric or antisymmetric taps give exactly linear phase, a delay of $(N - 1)/2$ samples for all frequencies. This is the most common FIR case.
- **IIR by magnitude only.** The phase is free. The classical answer is an analog prototype mapped to the digital domain.
- **Minimum phase.** A [minimum phase](/minimum-phase/) filter has the smallest delay for a given magnitude. An FIR filter of this kind comes from a linear phase design by spectral factorization.
- **Error norms.** Minimax (equiripple), least squares, or a mix. Least squares gives less noise power in the stop band, and minimax gives the smallest worst case.
- **Fixed point coefficients.** The coefficients must be integers of a given size. This is an integer optimization problem, and rounding a real design is the usual start.
- **Multirate filters.** Anti aliasing and anti imaging filters for [sample rate conversion](/sample-rate-conversion/) have a cutoff near $\pi/M$ and are implemented in [polyphase](/polyphase-decomposition/) form.

## Examples

**One specification, four designs.** Take $\omega_p = 0.4\pi$, $\omega_s = 0.6\pi$ and $\delta_p = \delta_s = 0.01$, which is a pass band loss of at most $0.0873$ dB at the edge and a stop band attenuation of 40 dB.

- **Butterworth and the bilinear transform.** With $T = 1$, prewarp the edges: $\Omega_p = 2\tan(0.2\pi) \approx 1.4531$ and $\Omega_s = 2\tan(0.3\pi) \approx 2.7528$ rad/s. The [Butterworth](/butterworth-filter/) order formula gives $N \ge 10.26$, so order 11. After the [bilinear transform](/bilinear-transform/), the filter costs about 12 multiplies per output sample in second order sections, because its zeros are all at $z = -1$.
- **Chebyshev type I.** The same prewarped edges give $N \ge \operatorname{arccosh}(\sqrt{r})/\operatorname{arccosh}(\Omega_s/\Omega_p) \approx 5.78$, with $r = (10^{A_s/10} - 1)/(10^{A_p/10} - 1)$, so order 6. An elliptic filter needs a still lower order.
- **Parks-McClellan.** The [Parks-McClellan algorithm](/parks-mcclellan-algorithm/) gives a largest error of about 0.0114 with 19 taps, and the same with 21 taps because the two outer taps are then zero; both fail. It gives 0.00553 with 23 taps, which meets the specification. The filter has exact linear phase and costs 23 multiplies per output sample, or 12 when the symmetric taps are paired.
- **The length estimate.** Kaiser's empirical formula $N \approx \big(-20\log_{10}\sqrt{\delta_p\delta_s} - 13\big)/\big(14.6\,(\omega_s - \omega_p)/(2\pi)\big) + 1$ gives $N \approx 19.5$. It is close, but the exact answer here is 23 because this specification gives a half-band filter, whose length grows in steps of 4.

The IIR filters are shorter, but their phase is not linear, and their group delay peaks near the pass band edge.

## Known algorithms

| method | filter | criterion | notes |
|---|---|---|---|
| windowing of the ideal impulse response, see [window functions](/window-functions/) | FIR, linear phase | none exact; ripple set by the window | the Kaiser window has formulas for $\beta$ and $N$ |
| frequency sampling | FIR | exact at $N$ frequencies | free samples in the transition band improve the stop band |
| least squares, via the [normal equations](/normal-equations/) | FIR | weighted squared error | a linear system; plain truncation of the ideal response is the case with equal weights and no transition band |
| [Parks-McClellan algorithm](/parks-mcclellan-algorithm/) | FIR, linear phase | weighted minimax | optimal; equiripple |
| [linear programming](/linear-programming-problem/) | FIR | minimax with extra constraints | slower; flexible |
| [Butterworth](/butterworth-filter/), Chebyshev and elliptic prototypes with the [bilinear transform](/bilinear-transform/) | IIR | magnitude | closed form; prewarp the edges |
| impulse invariance | IIR | samples of the analog impulse response | aliasing; not for high-pass filters |
| iterative and convex methods on the poles and zeros | IIR | magnitude and phase | local optima; stability must be enforced |

The window method and truncation show the [Gibbs phenomenon](/gibbs-phenomenon/): the overshoot near an edge does not go to zero as $N$ grows, so only the window, not the length, sets the ripple.

## Bounds

- **Ideal filters cannot be reached.** A nonzero FIR amplitude is a trigonometric polynomial, so it cannot vanish on a whole interval. The same holds for a nonzero rational $H$. So every real filter has $\delta_s > 0$ and a transition band of positive width.
- **FIR length.** For fixed ripples, the minimal length grows as $1/(\omega_s - \omega_p)$. Kaiser's formula describes this growth well for most specifications, but it is empirical, not a bound. The exact minimal length of a linear phase filter comes from running the Parks-McClellan algorithm for increasing $N$, because it gives the optimum for each $N$.
- **IIR order.** For the classical families the order formulas are exact. For a given order and ripples, the elliptic filter has the narrowest transition band of the classical families.
- **Linear phase and IIR.** With real coefficients, exactly linear phase needs an impulse response that is symmetric or antisymmetric about some time. A causal response of infinite length cannot be, so a causal IIR filter cannot have exactly linear phase. Zero phase IIR filtering is only possible offline, by a forward and a backward pass.

## Reductions

- **Minimax FIR to Chebyshev approximation.** With linear phase, the amplitude is a polynomial of degree $L$ in $\cos\omega$, so the design is a weighted [minimax approximation](/minimax-approximation/) problem, solved by the [Remez algorithm](/remez-algorithm/).
- **Least squares FIR to a linear system.** The weighted squared error is a quadratic form in the taps, which is a [least squares approximation](/least-squares-approximation/) problem.
- **Digital IIR to analog design.** The bilinear transform maps an analog filter that meets the prewarped specification to a digital filter that meets the original one, because it maps the $\Omega$ axis one to one onto the unit circle.
- **Other band shapes to low-pass.** Substitutions of the frequency variable turn a low-pass prototype into a high-pass, band-pass or band-stop filter, in the analog or the digital domain.
- **Minimum phase FIR to linear phase.** Design a linear phase filter for the squared magnitude and factor it, keeping the zeros inside the unit circle.

## Applications

- Anti aliasing and anti imaging filters for [sample rate conversion](/sample-rate-conversion/) and for converters between analog and digital signals.
- Audio equalizers and crossovers, hearing aids, and channel filters in radio receivers.
- Smoothing and differentiation of measured data; the [Savitzky-Golay filter](/savitzky-golay-filter/) is a least squares design with a polynomial constraint.
- The analysis and synthesis filters of [filter banks](/filter-bank/) and of the [discrete wavelet transform](/discrete-wavelet-transform/).

## References
