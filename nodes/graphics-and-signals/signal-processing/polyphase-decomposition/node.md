---
tag: AYGB1S
kind: technique
slug: polyphase-decomposition
name: Polyphase decomposition
aliases:
- polyphase filter structure
area: graphics-and-signals/signal-processing
level: advanced
summary: "Split a filter into M subfilters made of every M-th tap. With the noble identities a decimator or interpolator then filters at the low rate and saves a factor of M in multiplies."
prereqs: [fir-filter, z-transform]
see_also: [filter-bank, perfect-reconstruction, polyphase-resampling, sample-rate-conversion, subband-coding, aliasing, discrete-wavelet-transform, discrete-fourier-transform]
sources:
  - paper: doi:10.1109/TASSP.1976.1162788
    title: Maurice G. Bellanger, Georges Bonnerot and Michel Coudreuse, Digital Filtering by Polyphase Network, Application to Sample-Rate Alteration and Filter Banks, IEEE Transactions on Acoustics, Speech, and Signal Processing 24(2), 1976
    locator: pp. 109 to 114 (the polyphase network, its use for changing the sample rate and for filter banks)
  - book: isbn:9780136051626
    title: Ronald E. Crochiere and Lawrence R. Rabiner, Multirate Digital Signal Processing, Prentice-Hall, 1983
    locator: Chapter 3, Structures and Network Theory for Multirate Digital Systems (polyphase structures for decimators and interpolators, the commutator model); chapter level locator
  - book: isbn:9780136057185
    title: P. P. Vaidyanathan, Multirate Systems and Filter Banks, Prentice Hall, 1993
    locator: Chapter 4, Multirate Systems Fundamentals (the noble identities, the polyphase representation and efficient decimators and interpolators); chapter level locator
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 4.7, Multirate Signal Processing (4.7.1 the noble identities, 4.7.3 to 4.7.5 polyphase decompositions and polyphase decimation and interpolation)
---

Polyphase decomposition writes a filter $H(z)$ as a sum of $M$ subfilters, each made of every $M$-th tap: $H(z) = \sum_{j=0}^{M-1} z^{-j} E_j(z^M)$ with $e_j[i] = h[iM + j]$. Together with two rules called the noble identities, it lets a decimator compute only the output samples that it keeps, and lets an interpolator skip the zeros that upsampling inserts. Both then do all their filtering at the low rate, which saves a factor of $M$ (or $L$) in multiplies per output sample compared with the direct form, with exactly the same output. Maurice Bellanger, Georges Bonnerot and Michel Coudreuse introduced the polyphase network in 1976. It is the basic structure of [sample rate conversion](/sample-rate-conversion/), of the [polyphase resampler](/polyphase-resampling/) and of [filter banks](/filter-bank/). Frequencies on this page are $\omega$ in radians per sample at the rate where the signal lives, $\omega \in [-\pi, \pi]$.

## In plain words

To reduce the rate of a signal by three, you filter it and then keep one output in three. Computing the two outputs that you throw away is wasted work. Split the filter taps into three groups: the first, fourth, seventh tap, then the second, fifth, eighth, and so on. Split the input in the same way. Each kept output is the sum of three small filters, each applied to one group of inputs, and these small filters only run at the slow rate.

To raise the rate by three, you insert two zeros after each sample and then filter. Most products are with zeros. The same split shows that each output uses only one group of taps on the original samples, so the zeros are never touched.

## When it applies

The technique applies to a linear time invariant filter that is followed by a downsampler $(\downarrow M)$, $y[n] = v[nM]$, or preceded by an upsampler $(\uparrow L)$, which puts $L - 1$ zeros after each sample. It works for any [FIR filter](/fir-filter/) and, with more care, for IIR filters. The savings come from two facts:

- **Noble identity for downsampling.** $(\downarrow M)$ followed by $G(z)$ equals $G(z^M)$ followed by $(\downarrow M)$.
- **Noble identity for upsampling.** $G(z)$ followed by $(\uparrow L)$ equals $(\uparrow L)$ followed by $G(z^L)$.

A filter in $z^M$ has nonzero taps only at multiples of $M$, so it commutes with the rate change. In the polyphase form $H(z) = \sum_j z^{-j} E_j(z^M)$, each branch has this form after its delay, so the rate change moves in front of (or behind) every subfilter $E_j$.

## The template

Signals are zero before index 0. The filter $h$ has $K$ taps. The decimator computes $y[n] = \sum_k h[k]\, x[nM - k]$, the output of $h$ at the times $nM$. The interpolator computes $y = h * u$, where $u[nL] = x[n]$ and $u$ is zero elsewhere.

```pseudo id=main
POLYPHASE-DECIMATE(h[0 … K − 1], x, M)        ▷ y[n] = Σ_k h[k] x[nM − k]
L1  e_j[i] ← h[iM + j] for j = 0 … M − 1        ▷ the components, about K/M taps each
L2  for j ← 0 to M − 1 do                        ▷ branch j sees the phase x_j[n] = x[nM − j]
L3      for each output index n do acc ← 0
L4          for each tap i of e_j do
L5              acc ← acc + e_j[i] · x[(n − i)M − j]
L6          y[n] ← y[n] + acc

POLYPHASE-INTERPOLATE(h[0 … K − 1], x, L)     ▷ y = h ∗ (x upsampled by L)
L7  e_r[i] ← h[iL + r] for r = 0 … L − 1
L8  for each output index n do
L9      (q, r) ← (⌊n/L⌋, n mod L)
L10     acc ← Σ_i e_r[i] · x[q − i]
L11     y[n] ← acc
```

**Why the decimator is exact.** Write $k = iM + j$ with $0 \le j < M$. Then $y[n] = \sum_j \sum_i h[iM + j]\, x[nM - iM - j] = \sum_j \sum_i e_j[i]\, x_j[n - i]$ with $x_j[n] = x[nM - j]$. Each inner sum is the filter $e_j$ applied to the phase $x_j$, which is a signal at the low rate. This is the identity $H(z) = \sum_j z^{-j} E_j(z^M)$ followed by the downsampling noble identity on each branch.

**Why the interpolator is exact.** $y[n] = \sum_k h[k]\, u[n - k]$, and $u[n - k]$ is nonzero only if $n - k = sL$, where it is $x[s]$. With $n = qL + r$, this needs $k \equiv r \pmod L$, so $k = iL + r$ and $s = q - i$. So $y[qL + r] = \sum_i e_r[i]\, x[q - i]$: output phase $r$ uses only the component $e_r$, and never a zero of $u$.

**Cost.** The direct decimator runs $h$ at the input rate and costs $K$ multiplies per input sample, that is $KM$ per output sample. The polyphase decimator costs $K$ multiplies per output sample, $K/M$ per input sample. The direct interpolator costs $K$ multiplies per output sample. The polyphase interpolator costs $\lceil K/L \rceil$ or $\lfloor K/L \rfloor$ per output sample. In both cases the saving is a factor of $M$ or $L$, and the outputs are equal, not only close. With exact arithmetic, the two forms agree in every sample.

**Example.** Take $h = (1, 2, 3, 4, 5, 6)$ and $M = 2$. Then $e_0 = (1, 3, 5)$ and $e_1 = (2, 4, 6)$. For $x = (1, 0, 2, 1, 3)$, the full convolution is $h * x = (1, 2, 5, 9, 16, 23, 23, 29, 21, 18)$, and keeping the even indices gives $(1, 5, 16, 23, 21)$. The polyphase decimator gives the same values with 6 multiplies per output sample instead of 12. For example, $y[2] = e_0 * x_0$ at 2 plus $e_1 * x_1$ at 2, with $x_0 = (1, 2, 3)$ and $x_1 = (0, 0, 1)$ (the samples $x[2n - 1]$): $(1 \cdot 3 + 3 \cdot 2 + 5 \cdot 1) + (2 \cdot 1) = 14 + 2 = 16$.

For the interpolator, take the same $h$, $L = 3$ and $x = (1, 2, 3)$. The components are $e_0 = (1, 4)$, $e_1 = (2, 5)$ and $e_2 = (3, 6)$, and the output is

$$y = (1, 2, 3,\ 6, 9, 12,\ 11, 16, 21,\ 12, 15, 18,\ 0, 0),$$

which equals $h * (1, 0, 0, 2, 0, 0, 3, 0, 0)$. For instance $y[7] = y[2 \cdot 3 + 1] = e_1[0]\, x[2] + e_1[1]\, x[1] = 2 \cdot 3 + 5 \cdot 2 = 16$.

## Classic examples

- **Decimators and interpolators.** An integer rate change by $M$ or $L$ in [sample rate conversion](/sample-rate-conversion/) uses the template directly. The anti aliasing or anti imaging filter has a cutoff near $\pi/M$ or $\pi/L$, so it is long, and the factor of $M$ matters.
- **Rational resampling.** A rate change by $L/M$ upsamples, filters and downsamples. The [polyphase resampler](/polyphase-resampling/) combines both halves of the template: it computes only the kept outputs and uses only the nonzero inputs, so it needs about $K/L$ multiplies per output sample.
- **Filter banks.** An $M$ channel [filter bank](/filter-bank/) writes each analysis filter in polyphase form. The polyphase matrix of all channels then decides aliasing and [perfect reconstruction](/perfect-reconstruction/), and a DFT bank is the polyphase network followed by one [DFT](/discrete-fourier-transform/) per block of $M$ inputs.
- **Wavelets and subband coding.** The two channel bank of the [discrete wavelet transform](/discrete-wavelet-transform/) and of [subband coding](/subband-coding/) is computed in polyphase form, and the lifting scheme factors its polyphase matrix.
- **Half-band filters.** In a half-band filter every second tap is zero except the center, so for $M = 2$ one component is a single tap. A decimator by 2 then costs about $K/4$ multiplies per input sample, and less if the symmetric taps are paired.

## Variations

- **Type 1 and type 2 components.** The components $e_j[i] = h[iM + j]$ use the delays $z^{-j}$. The other convention uses $z^{j - M + 1}$ and the components $h[iM + M - 1 - j]$, which suits the interpolator.
- **Commutator model.** The decimator is a switch that sends input samples to the $M$ branches in the order $0, M - 1, M - 2, \ldots, 1$, and adds the branch outputs once per cycle. This is the hardware form of lines L2 to L6.
- **IIR filters.** A polyphase IIR decimator needs a denominator in $z^M$. Multiply the numerator and the denominator by a suitable polynomial to get one, or use allpass branches.
- **Multistage designs.** For a large $M$, decimate in several stages, each with its own polyphase filter. The early stages can use short filters because their transition bands are wide.
- **Fractional delays.** The $L$ components of a long low-pass filter are $L$ filters that delay the signal by $0, 1/L, \ldots, (L - 1)/L$ samples. This is the bank of fractional delay filters of an arbitrary ratio resampler.

## Pitfalls

- **Phase index and sign.** The branch $j$ of the decimator sees $x[nM - j]$, not $x[nM + j]$. Mixing the two conventions shifts the output by a sample and can break the equality with the direct form.
- **Start and length.** Decide whether the output starts at $n = 0$ and how many outputs there are. The direct form gives $\lfloor (K + N - 2)/M \rfloor + 1$ outputs for $N$ inputs.
- **Decimating without a filter.** The polyphase form is only cheap; it does not remove aliasing by itself. The filter $h$ must still be a good low-pass filter with a cutoff near $\pi/M$.
- **Component lengths.** When $K$ is not a multiple of $M$, the components have different lengths. Pad with zeros or handle each length.
- **Gain of the interpolator.** Upsampling by $L$ divides the average level by $L$. The filter needs a pass band gain of $L$ to keep the level.

## Exercises

1. Prove both noble identities in the time domain, from $y[n] = v[nM]$ and from the definition of upsampling.
2. Show that the polyphase decimator with $M = 1$ is the direct form, and that with $K \le M$ each branch is a single multiply.
3. For $h = (1, 2, 3, 4, 5, 6)$ and $M = 3$, write the three components and compute the decimated output for $x = (1, 0, 2, 1, 3)$. Check it against the full convolution.
4. A decimator by 4 uses a filter of 64 taps at an input rate of 48 kHz. Count the multiplies per second in the direct and in the polyphase form.
5. Show that the $L$ components of $h$ have frequency responses $E_r(e^{i\omega})$ that, for an ideal low-pass filter with cutoff $\pi/L$ and gain $L$, are all-pass filters with the delays $-r/L$ samples, up to a common delay.

## References
