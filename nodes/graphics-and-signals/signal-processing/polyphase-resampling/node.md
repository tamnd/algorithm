---
tag: 1Y8M5W
kind: algorithm
slug: polyphase-resampling
name: Polyphase resampling
aliases:
- rational sample-rate conversion
area: graphics-and-signals/signal-processing
level: advanced
summary: "Change the sample rate by L/M. It computes upsample by L then filter then keep every M-th sample exactly, but each output uses only one phase of the filter, about K/L multiplies."
solves: [sample-rate-conversion]
model: real-ram
complexity:
  vars: {N: the number of input samples, K: the number of filter taps, L: the upsampling factor, M: the downsampling factor}
  time: {worst: O(N (K + L) / M), average: O(N (K + L) / M), best: O(N (K + L) / M), per_sample: O(K / L)}
  space: {extra: O(K)}
properties: {linear: true, time_invariant: "no, periodically time varying with period L outputs", causal: true, stable: true, linear_phase: "when the taps are symmetric", exact: "equal to the three-stage form", deterministic: true, online: true}
history:
  year: 1976
  people: [Maurice G. Bellanger, Georges Bonnerot, Michel Coudreuse]
  note: Schafer and Rabiner described rational rate change by an upsampler, a filter and a downsampler in 1973. Bellanger, Bonnerot and Coudreuse gave the polyphase network for it in 1976, and Crochiere and Rabiner treated the structures in their book of 1983.
prereqs: [polyphase-decomposition, fir-filter]
see_also: [sample-rate-conversion, sinc-interpolation, image-resampling, aliasing, sampling-theorem, window-functions, parks-mcclellan-algorithm, reconstruction-filter]
sources:
  - book: isbn:9780136051626
    title: Ronald E. Crochiere and Lawrence R. Rabiner, Multirate Digital Signal Processing, Prentice-Hall, 1983
    locator: Chapter 2, Basic Principles of Sampling and Sampling Rate Conversion (conversion by L/M), and Chapter 3, Structures and Network Theory for Multirate Digital Systems (polyphase structures); chapter level locator
  - book: isbn:9780136057185
    title: P. P. Vaidyanathan, Multirate Systems and Filter Banks, Prentice Hall, 1993
    locator: Chapter 4, Multirate Systems Fundamentals (fractional rate change and its polyphase implementation); chapter level locator
  - paper: doi:10.1109/TASSP.1976.1162788
    title: Maurice G. Bellanger, Georges Bonnerot and Michel Coudreuse, Digital Filtering by Polyphase Network, Application to Sample-Rate Alteration and Filter Banks, IEEE Transactions on Acoustics, Speech, and Signal Processing 24(2), 1976
    locator: pp. 109 to 114 (the polyphase network for changing the sample rate)
  - paper: "Ronald W. Schafer and Lawrence R. Rabiner, A Digital Signal Processing Approach to Interpolation, Proceedings of the IEEE 61(6), June 1973, pages 692 to 702"
    locator: interpolation by an integer factor with FIR filters, and rate change by a rational factor as an increase followed by a decrease
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 4.6, Changing the Sampling Rate Using Discrete-Time Processing (rate change by a noninteger factor), and Section 4.7 (polyphase implementation of decimation and interpolation filters)
---

Polyphase resampling changes the sample rate of a signal by a rational factor $L/M$. The textbook method has three stages: insert $L - 1$ zeros after each sample, filter with a low-pass filter $h$ of $K$ taps at the high rate, and keep every $M$-th sample. Most of that work is wasted, because most inputs of the filter are zeros and most of its outputs are thrown away. The polyphase method computes only the kept outputs, and for each one it uses only the taps that meet nonzero inputs. Those taps form one of the $L$ [polyphase components](/polyphase-decomposition/) of $h$, so each output costs about $K/L$ multiplies, and the result equals the three-stage output exactly. It is the standard algorithm for [sample rate conversion](/sample-rate-conversion/) of one-dimensional signals such as audio. Frequencies on this page are $\omega$ in radians per sample, $\omega \in [-\pi, \pi]$, at the high rate $L f_{in}$ unless the text says otherwise.

## In plain words

To turn audio recorded at one rate into audio at another rate, you can imagine a much faster signal that has the original samples and zeros in between. You smooth it with a filter so that the gaps are filled in, then you pick every so many samples from the result.

Doing this literally is slow. Each output only needs the filter weights that line up with real samples, not with the zeros, and you never need the outputs that you skip. So the method steps through the outputs, works out where each one falls between two input samples, picks the small set of weights for that position, and multiplies them with a few nearby input samples.

## The problem

The input is a signal $x[0 \ldots N-1]$ at the rate $f_{in}$, two positive integers $L$ and $M$, and a filter $h[0 \ldots K-1]$. Let $u$ be $x$ upsampled by $L$: $u[sL] = x[s]$ and $u = 0$ elsewhere. The three-stage output is

$$y[n] = \sum_{k=0}^{K-1} h[k]\, u[nM - k], \qquad n = 0, 1, \ldots, \left\lfloor \frac{K + LN - 2}{M} \right\rfloor,$$

which is every $M$-th sample of the full convolution $h * u$. Its rate is $f_{in} L/M$. If $\gcd(L, M) = g > 1$, use $L/g$ and $M/g$ instead.

The filter does two jobs at the high rate: it removes the $L - 1$ images that upsampling creates, and it removes the frequencies that would alias in the downsampling. An ideal choice is a low-pass filter with cutoff $\pi/\max(L, M)$ and pass band gain $L$. The gain makes up for the zeros. In practice $h$ is a windowed [sinc](/sinc-interpolation/) or a [Parks-McClellan](/parks-mcclellan-algorithm/) design.

## The algorithm

Write $nM = qL + r$ with $0 \le r < L$. A term $h[k]\, u[nM - k]$ is nonzero only if $nM - k = sL$, so $k \equiv r \pmod L$. Put $k = iL + r$ and $s = q - i$. Then

$$y[n] = \sum_{i} h[iL + r]\, x[q - i] = \sum_i e_r[i]\, x[q - i],$$

where $e_r[i] = h[iL + r]$ is the component of phase $r$. When $n$ grows by 1, $nM$ grows by $M$, so $(q, r)$ is updated by one addition and a carry.

```pseudo id=main
RESAMPLE-POLY(x[0 … N − 1], h[0 … K − 1], L, M)   ▷ y[n] = Σ_k h[k] u[nM − k]
L1  e_r[i] ← h[iL + r] for r = 0 … L − 1
L2  (q, r) ← (0, 0)                                   ▷ invariant: nM = qL + r and 0 ≤ r < L
L3  for n ← 0 to ⌊(K + LN − 2)/M⌋ do acc ← 0
L4      for each tap i of e_r with 0 ≤ q − i < N do
L5          acc ← acc + e_r[i] · x[q − i]
L6      y[n] ← acc
L7      r ← r + M; q ← q + ⌊r/L⌋
L8      r ← r mod L
```

The phase $r$ runs through a fixed cycle of length $L$, and $q$ is the index of the newest input sample that the output needs. In a streaming version, $x[q - i]$ comes from a delay line of $\lceil K/L \rceil$ samples, and a new input enters it each time $q$ grows.

## Example

**A small exact case.** Take $h = (1, 2, 3, 4, 5, 6)$, $L = 3$, $M = 2$ and $x = (1, 2, 3)$. The phases are $e_0 = (1, 4)$, $e_1 = (2, 5)$ and $e_2 = (3, 6)$. There are $\lfloor (6 + 9 - 2)/2 \rfloor + 1 = 7$ outputs.

| $n$ | $nM$ | $(q, r)$ | phase | $y[n]$ |
|---|---|---|---|---|
| 0 | 0 | (0, 0) | $e_0$ | $1 \cdot 1 = 1$ |
| 1 | 2 | (0, 2) | $e_2$ | $3 \cdot 1 = 3$ |
| 2 | 4 | (1, 1) | $e_1$ | $2 \cdot 2 + 5 \cdot 1 = 9$ |
| 3 | 6 | (2, 0) | $e_0$ | $1 \cdot 3 + 4 \cdot 2 = 11$ |
| 4 | 8 | (2, 2) | $e_2$ | $3 \cdot 3 + 6 \cdot 2 = 21$ |
| 5 | 10 | (3, 1) | $e_1$ | $5 \cdot 3 = 15$ |
| 6 | 12 | (4, 0) | $e_0$ | $0$ |

The three-stage form computes $u = (1, 0, 0, 2, 0, 0, 3, 0, 0)$, the 14 values of $h * u = (1, 2, 3, 6, 9, 12, 11, 16, 21, 12, 15, 18, 0, 0)$, and keeps the even indices: $(1, 3, 9, 11, 21, 15, 0)$, the same values.

**CD audio to 48 kHz.** From 44.1 kHz to 48 kHz the ratio is $48000/44100 = 160/147$, since $\gcd(48000, 44100) = 300$. So $L = 160$ and $M = 147$, and the three-stage form would run its filter at $44100 \cdot 160 = 7.056$ MHz. With a windowed sinc of cutoff $\pi/160$ and 10 zero crossings on each side, $K = 3201$. The direct form computes all $147$ high-rate outputs for each kept one, about $3201 \cdot 147 \approx 470{,}000$ multiplies per output sample. The polyphase form uses one phase of 20 or 21 taps, about $3201/160 \approx 20$ multiplies per output sample, that is about $0.96$ million multiplies per second. The saving is the factor $LM = 23{,}520$. The $160$ phases take the memory of the $3201$ taps.

## Correctness

The algorithm keeps the invariant $nM = qL + r$ with $0 \le r < L$: it holds at $n = 0$ by line L2, and lines L7 and L8 add $M$ to $qL + r$ and then move whole multiples of $L$ from $r$ into $q$. Given the invariant, the sum of lines L4 and L5 is exactly the sum over the taps $k = iL + r$ that meet nonzero samples $u[(q - i)L] = x[q - i]$, and all other terms of the three-stage sum are products with zero. So $y[n]$ equals the three-stage value for every $n$ in exact arithmetic. In floating point both forms add the same nonzero products, possibly in a different order. The full proof is in the proof file.

## Complexity

The cost model is real multiplies and additions.

- **Per output sample.** One phase has $\lceil K/L \rceil$ or $\lfloor K/L \rfloor$ taps, so each output costs at most $\lceil K/L \rceil$ multiplies, plus $O(1)$ work for the phase update.
- **Total.** There are about $NL/M$ outputs, so the time is $O\big(NL/M \cdot (K/L + 1)\big) = O\big(N(K + L)/M\big)$.
- **Direct form.** The three-stage form costs $K$ multiplies per high-rate sample, which is $KM$ per output sample. Skipping only the zeros gives $K/L$ per high-rate sample, and skipping only the discarded outputs gives $K$ per output sample; the polyphase form does both.
- **Space.** The phases take $K$ numbers, and a streaming delay line takes $\lceil K/L \rceil$ samples.

For a fixed quality, $K$ grows in proportion to $\max(L, M)$, because the cutoff is $\pi/\max(L, M)$. So for $L \ge M$ the cost per output is about the number of zero crossings of the filter, independent of $L$.

## Properties

- **Exact.** The output equals the upsample, filter and downsample form sample by sample.
- **Linear and periodically time varying.** A delay of the input by $M$ samples delays the output by $L$ samples. A delay by one input sample does not give a delayed output in general.
- **Causal and stable.** It is built from an FIR filter. The latency is the group delay of $h$, $(K - 1)/2$ samples at the high rate for a symmetric filter.
- **Linear phase.** With a symmetric $h$, all frequencies are delayed by the same time, $(K - 1)/(2 L f_{in})$ seconds.
- **Interpolates when $M = 1$, decimates when $L = 1$.** These are the two halves of the [polyphase decomposition](/polyphase-decomposition/) template.
- **Reduced fraction.** For $\gcd(L, M) = g$, the ratio $L/M$ and $(L/g)/(M/g)$ give the same output rate. A filter designed for the reduced ratio has $g$ times fewer taps and phases, with the same work per output sample.

## Variants and improvements

- **Multistage conversion.** Factor $L/M$ into several smaller ratios, for example $160/147 = (4/3)(5/7)(8/7)$. Each stage has a wide transition band and a short filter, so the total cost can be lower.
- **Arbitrary and varying ratios.** For a ratio that is not a fraction of small integers, or that drifts, interpolate between the phases of a filter with many phases, or compute the taps for each output from a formula. This is the bandlimited [sinc interpolation](/sinc-interpolation/) of audio resamplers.
- **Polynomial taps.** Approximate each tap as a polynomial in the fractional position. The filter structure that does this is often credited to Farrow.
- **Integer arithmetic.** With integer taps and inputs, the output is exact, which is useful for testing and for fixed point hardware.
- **Images.** For two-dimensional images the same idea gives separable filters with a small number of phases, but the filters and the quality criteria are different. See [image resampling](/image-resampling/) for that case.

## When to use it

Use polyphase resampling for a fixed rational rate change of a sampled signal: audio between 44.1, 48 and 96 kHz, telephone speech between 8 and 16 kHz, and channels in software radio. It is also the core of interpolation by an integer factor and of decimation. For a ratio that is not fixed in advance, use a resampler with interpolated phases. For images and textures, use the methods of [image resampling](/image-resampling/) and [reconstruction filters](/reconstruction-filter/).

## Pitfalls

- **Missing gain.** Upsampling by $L$ divides the level by $L$. A filter with gain 1 gives an output that is $L$ times too quiet.
- **Wrong cutoff.** The cutoff must be $\pi/\max(L, M)$ at the high rate. With $\pi/L$ when $M > L$, the downsampling aliases.
- **Unreduced fractions.** A ratio of $6/4$ with a filter for $L = 6$ needs twice the taps and twice the memory of $3/2$ for the same output rate. Divide $L$ and $M$ by their greatest common divisor first.
- **Start and length.** The first outputs depend on the zeros before the signal, and the filter delay shifts the output by $(K - 1)/2$ high-rate samples. Remove the delay if the output must line up with the input.
- **Phase step.** The phase advances by $M$, not by 1. Writing $r \leftarrow r + 1$ gives an interpolator by $L$, not a converter by $L/M$.
- **Accumulated drift.** A floating point position $n M/L$ drifts for long signals. Keep $q$ and $r$ as integers, as in lines L7 and L8.

## Implementations

## History

Ronald Schafer and Lawrence Rabiner described interpolation with FIR filters and rate change by a rational factor, as an integer increase followed by an integer decrease, in 1973. In 1976 Maurice Bellanger, Georges Bonnerot and Michel Coudreuse introduced the polyphase network, which does this work at the low rate. Ronald Crochiere and Lawrence Rabiner collected the theory and the structures in their book Multirate Digital Signal Processing in 1983, and P. P. Vaidyanathan's book of 1993 gave the general theory of multirate systems and filter banks. Rate conversion between the CD rate of 44.1 kHz and the studio rate of 48 kHz made the method common in digital audio.

## References
