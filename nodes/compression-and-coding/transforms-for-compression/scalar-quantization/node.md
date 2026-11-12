---
tag: E3908F
kind: technique
slug: scalar-quantization
name: Scalar quantization
aliases:
- uniform quantization
area: compression-and-coding/transforms-for-compression
level: intro
summary: "Map each real value, one at a time, to one of a finite set of levels. Uniform, dead-zone and Lloyd-Max quantizers, and the rule D = Δ^2/12."
prereqs: [lossy-compression]
see_also: [vector-quantization, lloyds-algorithm, k-means, transform-coding, predictive-coding, jpeg-compression, jpeg-2000, bit-plane-coding]
sources:
  - paper: doi:10.1109/TIT.1982.1056489
    title: Stuart P. Lloyd, Least squares quantization in PCM, IEEE Transactions on Information Theory 28(2), 1982
    locator: pages 129 to 137 (the conditions for an optimal quantizer, Method I and Method II; the text of a 1957 Bell Laboratories memorandum)
  - paper: doi:10.1109/TIT.1960.1057548
    title: Joel Max, Quantizing for minimum distortion, IRE Transactions on Information Theory 6(1), 1960
    locator: pages 7 to 12 (the equations for the optimal levels and thresholds, and the table for the Gaussian density)
  - paper: doi:10.1002/j.1538-7305.1948.tb01340.x
    title: William R. Bennett, Spectra of quantized signals, Bell System Technical Journal 27(3), 1948
    locator: pages 446 to 472 (the high-resolution analysis of quantization noise)
  - paper: doi:10.1109/18.720541
    title: Robert M. Gray and David L. Neuhoff, Quantization, IEEE Transactions on Information Theory 44(6), 1998
    locator: pages 2325 to 2383 (the high-resolution formula, the Lloyd-Max conditions, the uniqueness results of Fleischer and Trushkin, and the entropy-coded uniform quantizer)
  - book: isbn:9780792391814
    title: Allen Gersho and Robert M. Gray, Vector Quantization and Signal Compression, Kluwer, 1992
    locator: Chapters 5 and 6 (scalar quantization, the optimality conditions and the Lloyd iteration)
  - book: isbn:9780128094747
    title: Khalid Sayood, Introduction to Data Compression, fifth edition, 2017
    locator: Chapter 9 (scalar quantization, uniform, adaptive and Lloyd-Max quantizers)
---

Scalar quantization maps each real value, one at a time, to one of a finite set of *levels*, and sends only the index of the level. It is the step of a [lossy](/lossy-compression/) coder that throws information away: a uniform quantizer with step $\Delta$ gives a mean squared error near $\Delta^2/12$ at high rate, so each extra bit gains about 6.02 dB. The Lloyd-Max quantizer (Lloyd 1957, Max 1960) places the levels to minimize the error for a known density. Every transform and predictive coder, JPEG and JPEG 2000 among them, quantizes its coefficients with a scalar quantizer.

## In plain words

A ruler with marks every millimetre turns any length into a whole number of millimetres. The true length is lost, but the error is at most half a millimetre. A scalar quantizer does the same with numbers: it cuts the number line into intervals, gives each interval one representative value, and replaces every input by the value of its interval.

The encoder sends only the number of the interval, which takes few bits. The decoder looks up the representative value. Wide intervals need fewer bits but give larger errors.

If most inputs are small, it pays to put the intervals close together near zero and far apart for large values. The best placement for a known distribution satisfies two simple rules: each boundary sits halfway between two neighbouring values, and each value sits at the mean of the inputs that fall in its interval.

## When it applies

Use a scalar quantizer when the values to code are real or have more precision than the receiver needs, and they are nearly independent, so that coding them one at a time loses little. This is the case after a decorrelating step: the coefficients of a [transform](/transform-coding/) or [subband](/subband-coding/) coder, or the residuals of a [predictive coder](/predictive-coding/). For strongly dependent values, [vector quantization](/vector-quantization/) or a transform first does better.

**Definition.** An $N$-level scalar quantizer has thresholds $t_1 < t_2 < \cdots < t_{N-1}$ and levels $y_1, \ldots, y_N$. With $t_0 = -\infty$ and $t_N = +\infty$, cell $i$ is $(t_{i-1}, t_i]$ and $Q(x) = y_i$ for $x$ in cell $i$. The encoder outputs the index $i$; with a fixed-length code it costs $\lceil \lg N \rceil$ bits, and with an entropy coder about $H(Q(X))$ bits. The distortion is the mean squared error $D = E[(X - Q(X))^2]$ for a random $X$ with density $f$.

**Uniform quantizers.** All cells except the two outer ones have the same width $\Delta$, the *step*, and the levels are the cell midpoints.

- *Midtread*: a level at 0, $Q(x) = \Delta \cdot \mathrm{round}(x / \Delta)$. It has an odd number of levels and sends silence to exactly 0.
- *Midrise*: a threshold at 0, $Q(x) = \Delta (\lfloor x / \Delta \rfloor + \tfrac{1}{2})$. It has an even number of levels.
- *Dead zone*: the zero cell is wider than the others. JPEG 2000 Part 1 (ISO/IEC 15444-1, Annex E) uses the index $q = \mathrm{sign}(x) \lfloor |x| / \Delta \rfloor$, so the zero cell is $(-\Delta, \Delta)$, and the decoder outputs $\mathrm{sign}(q) (|q| + r) \Delta$ for $q \ne 0$, with $r$ often $1/2$. In H.264 the standard fixes only the decoder's uniform reconstruction, and an encoder makes a dead zone by rounding with an offset below $1/2$. The dead zone codes many small coefficients as 0, which costs few bits after [run-length](/run-length-encoding/) or [bit-plane](/bit-plane-coding/) coding.

**The high-rate rule $D \approx \Delta^2/12$.** Suppose that the density $f$ is nearly constant over each cell and the outer cells have negligible probability. Then, given that $X$ falls in a cell of width $\Delta$, the error $X - Q(X)$ is nearly uniform on $[-\Delta/2, \Delta/2]$, and

$$D \approx \int_{-\Delta/2}^{\Delta/2} \frac{e^2}{\Delta}\, de = \frac{\Delta^2}{12}.$$

The rule is exact for a uniform input on a range that is a whole number of cells. Bennett (1948) gave this analysis. For a uniform input on $[-A, A]$ and $2^b$ levels, $\Delta = 2A / 2^b$, the signal power is $A^2/3$, and

$$\mathrm{SNR} = 10 \log_{10} \frac{A^2/3}{\Delta^2/12} = 20 \log_{10}(2) \cdot b \approx 6.02\, b \ \text{dB}.$$

**The Lloyd-Max conditions.** For a fixed number of levels $N$, an optimal quantizer for the mean squared error satisfies both of these:

1. *Nearest neighbour*: $t_i = (y_i + y_{i+1})/2$. Proof: for fixed levels, each $x$ costs least when it goes to the nearest level, and the set of points nearer to $y_i$ than to the others is the interval between the midpoints.
2. *Centroid*: $y_i = E[X \mid t_{i-1} < X \le t_i]$. Proof: for a fixed cell $C$, $E[(X - y)^2 \mid C] = \mathrm{Var}(X \mid C) + (E[X \mid C] - y)^2$, which is least at $y = E[X \mid C]$.

The conditions are necessary, not sufficient: they can have several solutions. For a log-concave density such as the Gaussian or the Laplacian they have only one, so it is the optimum (Fleischer 1964 and Trushkin 1982, in the survey of Gray and Neuhoff).

**Entropy-coded uniform quantizers.** With an ideal entropy coder on the indices, the rate at high resolution is $H(Q(X)) \approx h(X) - \lg \Delta$, where $h$ is the differential entropy. So $D \approx \frac{1}{12} 2^{2h(X)} 2^{-2H}$. For a Gaussian, $R(D)$ gives $D = \frac{1}{2\pi e} 2^{2h(X)} 2^{-2R}$. The ratio of the two distortions at the same rate is $\pi e / 6$, which is 1.53 dB or $\frac{1}{2} \lg \frac{\pi e}{6} \approx 0.254$ bits per sample. Gish and Pierce (1968, in the survey of Gray and Neuhoff) showed that no other scalar quantizer with an ideal entropy coder does better at high rate, which is why practical coders use uniform or dead-zone quantizers followed by entropy coding.

## The template

```pseudo id=main
QUANTIZE(x, t)                               ▷ t: sorted thresholds t1 < … < tN−1 (hole: the cell layout)
L1  return the number of thresholds below x, plus 1   ▷ binary search
RECONSTRUCT(i, y)                            ▷ y: the levels (hole: the reconstruction rule)
L2  return y[i]

LLOYD-MAX(y, f)                              ▷ Lloyd's Method I; f: the density, y: start levels
L3  repeat
L4      t[i] ← (y[i] + y[i+1]) / 2 for i = 1 to N − 1
L5      y[i] ← E[X | t[i−1] < X ≤ t[i]] for i = 1 to N   ▷ keep y[i] if the cell has mass 0
L6      D ← E[(X − Q(X))²]
L7  until the levels stop changing
L8  return t, y
```

QUANTIZE costs $O(\log N)$ comparisons, and $O(1)$ for a uniform quantizer, which divides by $\Delta$. LLOYD-MAX alternates the two conditions. Line L4 makes the cells optimal for the levels, and line L5 makes the levels optimal for the cells, so neither line can raise $D$: the sequence of distortions of line L6 never increases and, being bounded below by 0, converges. Each iteration costs $O(N)$ evaluations of the cell mass and first moment of $f$. For the Gaussian density these are $\Phi(b) - \Phi(a)$ and $\phi(a) - \phi(b)$, with $\phi$ and $\Phi$ the standard normal density and distribution function.

Max (1960) solved the same two conditions in another way: guess $y_1$, compute $t_1, y_2, t_2, \ldots$ in turn from the two equations, and adjust $y_1$ until the last centroid condition holds. Lloyd called this Method II.

**The holes.** The cell layout of line L1 (uniform, dead zone, or designed), the reconstruction rule of line L2 (midpoint, centroid, or a decoder offset $r$), and the code for the indices (fixed length, Huffman, arithmetic).

### Worked examples

**Uniform quantizers with $\Delta = 0.5$.** Midtread: $0.24 \to 0$, $0.26 \to 0.5$, $-0.75 \to -1.0$ (a tie, rounded away from 0). Midrise: $0.24 \to 0.25$, $-0.01 \to -0.25$.

**Dead zone with $\Delta = 2$.** The inputs $-4.5, -1.9, 0, 1.9, 2.0, 5.9$ get the indices $-2, 0, 0, 0, 1, 2$. With $r = 1/2$ the decoder outputs $-5, 0, 0, 0, 3, 5$.

**Monte Carlo of $\Delta^2/12$.** For 60 000 samples of a unit Gaussian, the measured MSE of the midtread and midrise quantizers with $\Delta = 0.1$ and $\Delta = 0.25$ is within 3% of $\Delta^2/12$. At $\Delta = 2$ the exact MSE of the midtread quantizer is 0.3304 against $\Delta^2/12 = 0.3333$, but at $\Delta = 4$ it is 0.8641 against 1.3333: the rule fails when cells are as wide as the density.

**Lloyd-Max on the unit Gaussian.** With two levels the conditions give $t_1 = 0$, $y = \pm \sqrt{2/\pi} = \pm 0.7979$ and $D = 1 - 2/\pi = 0.3634$. Lloyd's iteration from the start levels $-1.5, -0.5, 0.5, 1.5$ (four levels) and from $-3.5, \ldots, 3.5$ (eight levels) gives:

| levels $N$ | positive thresholds | positive levels | $D$ | SNR | best uniform $D$ (its step) | $R(D)$ bound at $\lg N$ bits |
|---|---|---|---|---|---|---|
| 2 | (0) | 0.7979 | 0.3634 | 4.40 dB | 0.3634 (1.596) | 0.2500 (6.02 dB) |
| 4 | 0, 0.9816 | 0.4528, 1.5104 | 0.1175 | 9.30 dB | 0.1188 (0.996) | 0.0625 (12.04 dB) |
| 8 | 0, 0.5005, 1.0500, 1.7479 | 0.2451, 0.7560, 1.3439, 2.1519 | 0.03455 | 14.62 dB | 0.03744 (0.586) | 0.015625 (18.06 dB) |

The gap to the rate distortion bound grows with the rate for fixed-length indices: at 3 bits the Lloyd-Max quantizer is 3.4 dB from the bound. Entropy coding of the indices and coding in blocks close most of it.

## Classic examples

- [JPEG](/jpeg-compression/): a uniform midtread quantizer per DCT coefficient, with a step from an $8 \times 8$ table; the decoder multiplies the index by the step.
- [JPEG 2000](/jpeg-2000/): a dead-zone quantizer per subband, whose indices are then coded by [bit planes](/bit-plane-coding/), so that a cut in the bit stream is a coarser dead-zone quantizer.
- [Predictive coding](/predictive-coding/) (DPCM): the prediction error is quantized, often with a Lloyd-Max quantizer for a Laplacian density.
- [Subband coding](/subband-coding/) and [transform coding](/transform-coding/): one quantizer per band, with the steps set by bit allocation.
- Pulse code modulation of sound: a uniform quantizer with 16 bits for CD audio, and the companded $\mu$-law and A-law quantizers of telephony, which are uniform quantizers of a compressed signal.

## Variations

- **Companding.** Apply a compressor function $G$, quantize $G(x)$ uniformly, and expand. At high rate the best $G'$ is proportional to $f^{1/3}$ (Panter and Dite, in the survey of Gray and Neuhoff).
- **Sample-based design.** Run Lloyd's iteration on a training set instead of a density. In one dimension this is [k-means](/k-means/) on the real line. The same iteration with a density in the plane is [Lloyd's algorithm](/lloyds-algorithm/) for centroidal Voronoi tessellations, and in $k$ dimensions it is the LBG algorithm of [vector quantization](/vector-quantization/).
- **Entropy-constrained design.** Minimize $D + \lambda H(Q(X))$ instead of $D$ at a fixed $N$. The Lloyd iteration then uses a biased nearest-neighbour rule.
- **Adaptive quantizers.** The step follows a local estimate of the signal power, as in ADPCM.
- **Embedded quantizers.** Coding the indices of a dead-zone quantizer from the most significant bit down gives a family of quantizers with steps $\Delta, 2\Delta, 4\Delta, \ldots$; see [bit-plane coding](/bit-plane-coding/).

## Pitfalls

- **The rounding rule.** Python's `round` and many FPUs round halves to even, which makes the cells of a midtread quantizer uneven at exact ties. Use $\lfloor |x|/\Delta + 1/2 \rfloor$ with the sign of $x$, as the tests do.
- **The high-rate rule at low rate.** $\Delta^2/12$ needs cells much narrower than the density. At $\Delta = 4\sigma$ it is off by more than 50% (the Monte Carlo example above).
- **Overload.** A fixed-length quantizer has finitely many levels. Inputs beyond the outer levels give large errors that $\Delta^2/12$ does not count. A range of about $\pm 4\sigma$ is a common choice for a Gaussian.
- **Local optima.** Lloyd's iteration stops at any solution of the two conditions. For a density with several peaks, run it from several starts.
- **Empty cells.** With a training set, a cell can get no samples, and line L5 then has no mean. Keep the old level, or split the most populated cell.
- **Midtread against midrise.** A midrise quantizer has no zero level, so it turns silence into a small tone of $\pm \Delta/2$, and it cannot code the many zero coefficients of a transform coder cheaply.

## Exercises

1. Show that for a uniform density on $[0, 1]$ the Lloyd-Max quantizer with $N$ levels is the uniform quantizer with $\Delta = 1/N$, and that its distortion is exactly $1/(12 N^2)$.
2. For the Laplacian density $\frac{1}{2} e^{-|x|}$ and two levels, find the Lloyd-Max levels and the distortion.
3. Prove that the distortion of a dead-zone quantizer with index $\mathrm{sign}(x)\lfloor |x|/\Delta \rfloor$ and reconstruction offset $r = 1/2$ is at most $\Delta^2$ in each sample, and at most $\Delta^2/4$ outside the zero cell.

## References
