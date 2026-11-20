---
tag: 9JVEXY
kind: algorithm
slug: farrow-interpolator
name: Farrow interpolator
aliases:
- Farrow structure
- Farrow filter
area: communications/synchronization
level: core
summary: "A polynomial interpolation filter. Fixed FIR filters give the coefficients of a polynomial in the fractional delay mu, and Horner's rule evaluates it, so a new delay costs no new filter design."
solves: [sample-rate-conversion]
model: real-ram
complexity:
  vars: {D: the degree of the polynomial, K: the number of taps per filter, N: the number of output samples}
  time: {per_output: O(D K), total: O(N D K)}
  space: {extra: O(D)}
properties: {deterministic: true, online: true, linear: true, passes_through_samples: true, exact_for_polynomials_of_degree: "3 (cubic Lagrange) or 1 (parabolic)"}
history:
  year: 1988
  people: [C. W. Farrow]
  note: "Farrow presented the structure at ISCAS 1988 as a continuously variable digital delay element. Gardner, Erup and Harris made it the standard interpolator for digital timing recovery in 1993."
prereqs: [lagrange-interpolation, fir-filter, horner-rule]
see_also: [symbol-timing-recovery, gardner-timing-error-detector, oerder-meyr-timing-estimation, mueller-muller-timing-recovery, early-late-gate-synchronizer, sample-rate-conversion, cubic-spline-interpolation, raised-cosine-filter]
sources:
  - paper: doi:10.1109/ISCAS.1988.15483
    title: "C. W. Farrow, A continuously variable digital delay element, Proceedings of the IEEE International Symposium on Circuits and Systems, 1988, pages 2641 to 2645"
    locator: "the structure of fixed FIR filters whose outputs are combined as a polynomial in the delay"
  - paper: doi:10.1109/26.221081
    title: "Floyd M. Gardner, Interpolation in digital modems, Part I, Fundamentals, IEEE Transactions on Communications 41(3), 1993, pages 501 to 507"
    locator: "the basepoint index, the fractional interval mu and the control of the interpolator by a numerically controlled oscillator"
  - paper: doi:10.1109/26.231921
    title: "Lars Erup, Floyd M. Gardner and Robert A. Harris, Interpolation in digital modems, Part II, Implementation and performance, IEEE Transactions on Communications 41(6), 1993, pages 998 to 1008"
    locator: "the cubic Lagrange and the piecewise parabolic Farrow interpolators and their performance"
  - book: isbn:9780471502753
    title: "Heinrich Meyr, Marc Moeneclaey and Stefan A. Fechtel, Digital Communication Receivers, Wiley, 1998"
    locator: "Chapter 9 (interpolation and decimation)"
---

The Farrow interpolator computes the value of a sampled signal between its samples, at a fractional delay $\mu$ that can change at every output. It writes the interpolated value as a polynomial in $\mu$, $y(m + \mu) = \sum_{i=0}^{D} c_i[m]\,\mu^i$, where each coefficient $c_i[m]$ is the output of a fixed [FIR filter](/fir-filter/) on the input around the basepoint $m$. [Horner's rule](/horner-rule/) then evaluates the polynomial. A change of delay needs no new filter taps, only a new value of $\mu$. In all-digital receivers the sampling clock is free-running, and the timing loop or estimator gives the strobe times as $m_k + \mu_k$. The Farrow interpolator produces the strobes for the [Gardner detector](/gardner-timing-error-detector/), the [Mueller and Müller loop](/mueller-muller-timing-recovery/) and the [Oerder and Meyr estimator](/oerder-meyr-timing-estimation/). The two standard coefficient sets are cubic [Lagrange interpolation](/lagrange-interpolation/) through four samples and the piecewise parabolic interpolator of Erup, Gardner and Harris.

## In plain words

A receiver often takes samples at moments that do not match the moments it needs. To get a value between two samples, it fits a smooth curve through a few nearby samples and reads the curve at the wanted point. The Farrow method does the fit with a few fixed filters. Each filter gives one number that describes the curve. To read the curve at a point, it only needs the position of that point between the samples. So the receiver can move the reading point at every step for very little work, and it never has to design a new filter.

## The problem

The input is a sequence $x[n] = f(n)$, sampled on a grid of spacing $T_s = 1$. A second input is a sequence of output times $t_k$, each split as $t_k = m_k + \mu_k$ with the basepoint $m_k = \lfloor t_k\rfloor$ and the fractional interval $\mu_k \in [0, 1)$. The output is $y_k \approx f(t_k)$ for each $k$. The interpolator is a linear combination of the samples near $m_k$ whose weights depend on $\mu_k$. Its quality is the error $|y_k - f(t_k)|$ for band-limited $f$, which depends on the frequency response of the equivalent continuous filter. For a timing loop, the times come from a numerically controlled oscillator with a step of $W = T_i/T_s$ input samples.

## The algorithm

```pseudo id=main
FARROW(x, m, mu, b[0..D][0..3])
L1  w <- (x[m-1], x[m], x[m+1], x[m+2])
L2  c[i] <- sum_j b[i][j] * w[j] for i <- 0 to D     ▷ D+1 fixed FIR filters
L3  y <- c[D]
L4  for i <- D - 1 downto 0 do
L5      y <- y * mu + c[i]                          ▷ Horner's rule
L6  return y

RESAMPLE(x, times, b)
    for each t in times do
L7      m <- floor(t)
L8      mu <- t - m
L9      append FARROW(x, m, mu, b) to the output
```

Line L1 takes four samples around the basepoint. For cubic Lagrange interpolation ($D = 3$) the coefficient rows are
$$b = \begin{pmatrix} 0 & 1 & 0 & 0 \\ -\frac13 & -\frac12 & 1 & -\frac16 \\ \frac12 & -1 & \frac12 & 0 \\ -\frac16 & \frac12 & -\frac12 & \frac16 \end{pmatrix}.$$
For the piecewise parabolic interpolator ($D = 2$) with parameter $\alpha$ they are $(0, 1, 0, 0)$, $(-\alpha, \alpha - 1, \alpha + 1, -\alpha)$ and $(\alpha, -\alpha, -\alpha, \alpha)$. With $\alpha = \frac12$ all taps are multiples of $\frac12$, so the filters need only shifts and additions. Line L2 is the filter bank. When several outputs share the same basepoint, as in upsampling, line L2 runs once for them. Lines L3 to L5 evaluate the polynomial.

## Example

Take $x[m-1..m+2] = 1, 3, 2, 0$ and $\mu = 0.4$. With the cubic rows, line L2 gives $c = (3, 0.16667, -1.5, 0.33333)$. Lines L3 to L5 compute:

| step | value |
|---|---|
| L3: $y = c_3$ | $0.33333$ |
| L5: $y\mu + c_2$ | $-1.36667$ |
| L5: $y\mu + c_1$ | $-0.38$ |
| L5: $y\mu + c_0$ | $2.848$ |

The same value comes from the Lagrange weights at $\mu = 0.4$, which are $-0.064, 0.672, 0.448, -0.056$. The parabolic interpolator with $\alpha = \frac12$ gives $c = (3, 1, -2)$ and $y = 3 + 0.4 - 0.32 = 3.08$.

For a sinusoid of unit amplitude at frequency $\nu$, the largest error over all phases and over a grid of 2001 values of $\mu$ was (computed), with the theoretical bound $\frac{3}{128}(2\pi\nu)^4$ of the cubic:

| $\nu$ (cycles per sample) | cubic | parabolic, $\alpha = \frac12$ | cubic bound |
|---|---|---|---|
| $0.05$ | $2.26 \times 10^{-4}$ | $0.0119$ | $2.28 \times 10^{-4}$ |
| $0.1$ | $3.54 \times 10^{-3}$ | $0.0419$ | $3.65 \times 10^{-3}$ |
| $0.25$ | $0.116$ | $0.0607$ | $0.143$ |

At four samples per symbol, a raised cosine signal with $\beta = \frac12$ has no energy above $\nu = (1 + \beta)/8 = 0.1875$ cycles per sample, so the cubic error is small for the signals of a timing loop.

## Correctness

**Claim.** With the cubic rows, the output is the unique polynomial of degree at most 3 through the four samples, read at $\mu$. If $f$ has four continuous derivatives, the error is at most $\frac{3}{128}\max|f''''|$ for $\mu \in [0, 1)$. The parabolic interpolator is exact for polynomials of degree at most 1 and passes through the samples, but not for degree 2: on $x[n] = n^2$ at $\mu = \frac12$ it returns $0$ instead of $\frac14$ when $\alpha = \frac12$.

**Key steps.** By Horner's rule, $y = \sum_j x[m - 1 + j]\,\ell_j(\mu)$ with $\ell_j(\mu) = \sum_i b_{ij}\mu^i$. Each column of the cubic rows is the coefficient vector of the Lagrange basis polynomial for the node $j - 1$, so the output is the interpolating polynomial. The Lagrange remainder is $\frac{f''''(\xi)}{24}(\mu + 1)\mu(\mu - 1)(\mu - 2)$, and the product has its largest magnitude on $[0, 1]$ at $\mu = \frac12$, where it is $\frac{9}{16}$. The full proof is in the proofs file. The error bound is a theorem. The sinusoid errors are measurements.

## Complexity

In the [real RAM](/real-ram/), line L2 costs $(D + 1)K$ multiply-adds with $K = 4$ taps, and lines L3 to L5 cost $D$ multiply-adds. So one output costs $O(DK)$ operations, which is 16 plus 3 for the cubic and 12 plus 2 for the parabolic, fewer when the zero and unit taps are skipped. $N$ outputs cost $O(NDK)$, and the extra space is $O(D)$ for the coefficients. A filter whose taps are designed for each new $\mu$ would need $K$ evaluations of a $\mu$-dependent kernel per output instead. The hardware cost is fixed filters and $D$ multipliers by $\mu$.

## Properties

- **Linear and time-varying.** For fixed $\mu$ it is an FIR filter. Its continuous impulse response $h(t)$, with $y(t) = \sum_n x[n]h(t - n)$, is piecewise polynomial on $[-2, 2]$. At $t = -1.5, -0.5, 0.5, 1.5$ its values are $-\frac1{16}, \frac9{16}, \frac9{16}, -\frac1{16}$ for the cubic and $-\frac18, \frac58, \frac58, -\frac18$ for the parabolic with $\alpha = \frac12$.
- **Passes through the samples.** At $\mu = 0$ the output is $x[m]$ for both coefficient sets.
- **Exact on polynomials.** The cubic form is exact on polynomials of degree at most 3. The parabolic form is exact on degree at most 1.
- **Response to a constant.** Both sets give the constant back for every $\mu$, so the interpolator does not modulate a flat signal.
- **Delay in one parameter.** The filters do not depend on $\mu$. Only the Horner step does.

## Variants and improvements

- **Higher degree and more taps.** Lagrange interpolation with more points, or polynomial fits to a longer ideal interpolator, give better frequency response at the cost of more filters.
- **Optimized coefficients.** Instead of Lagrange coefficients, the rows can be designed to minimize the error over a frequency band. Any piecewise polynomial impulse response has a Farrow form.
- **Parabolic with other $\alpha$.** Erup, Gardner and Harris studied how $\alpha$ changes the performance in a modem. The value $\frac12$ is the cheap choice.
- **Polyphase interpolators.** A bank of fixed filters, one per quantized value of $\mu$, is the alternative. It needs memory for every phase but no multiplication by $\mu$.
- **Splines.** [Cubic spline interpolation](/cubic-spline-interpolation/) is smoother but depends on all samples, so it is not a short filter in its exact form.

## When to use it

Use the Farrow interpolator when the receiver samples with a free-running clock and the timing must be corrected digitally, when the delay changes at every output, or when the output rate is not a simple ratio of the input rate, as in [sample rate conversion](/sample-rate-conversion/) by an arbitrary factor. At two to four samples per symbol the cubic or the parabolic form is enough for most modems. When the signal is close to the Nyquist frequency, use more taps or an optimized design.

## Pitfalls

- **Wrong basepoint.** The window is $x[m - 1]$ to $x[m + 2]$ with $\mu \in [0, 1)$. Using $\mu \in [-\frac12, \frac12)$ with the same rows reads the curve in the wrong interval.
- **Edges.** An output time needs one sample before and two after its basepoint. The implementation only returns times with a full window.
- **Underestimating the error at high frequency.** At a quarter of the sample rate the cubic error is about $12\%$ of the amplitude. The table shows that the cubic is not always better than the parabolic there.
- **Mixing the timing estimate and $\mu$.** A timing estimate $\hat\tau$ in symbols must be converted to input samples, and its integer part goes into the basepoint. A carry from $\mu$ to $m$ that is lost causes a slip of one sample.

## Implementations

## History

C. W. Farrow presented the structure at the IEEE International Symposium on Circuits and Systems in 1988 as a continuously variable digital delay element. In 1993 Floyd M. Gardner described how digital modems use an interpolator controlled by a basepoint index and a fractional interval, and Lars Erup, Gardner and Robert A. Harris analysed the cubic Lagrange and the piecewise parabolic Farrow interpolators in the second part of that work. Since then the Farrow structure has been the usual interpolator in all-digital timing recovery and in sample rate converters with an arbitrary ratio.

## References
