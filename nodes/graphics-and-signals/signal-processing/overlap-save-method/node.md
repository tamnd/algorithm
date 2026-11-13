---
tag: 6E7154
kind: algorithm
slug: overlap-save-method
name: Overlap-save method
aliases:
- overlap-discard
area: graphics-and-signals/signal-processing
level: core
summary: "Block convolution of a long signal with a short filter: FFT each overlapping input block, multiply by the filter spectrum, and keep only the outputs that did not wrap."
solves: [discrete-convolution]
model: real-ram
complexity:
  vars: {L: the length of the input, M: the length of the filter, N: "the FFT length, a small multiple of M"}
  time: {worst: O((L + M) log M)}
  space: {extra: O(M)}
properties: {deterministic: true, online: true, in_place: false, exact: false}
history:
  year: 1967
  people: [Thomas G. Stockham Jr., Howard D. Helms]
  note: Stockham sectioned FFT convolution in 1966 and Helms treated FFT filtering of long sequences in 1967; the sources do not settle who first discarded the wrapped outputs.
prereqs: [discrete-convolution, circular-convolution, convolution-via-fft]
see_also: [overlap-add-method, fast-fourier-transform, fir-filter, digital-filtering, real-valued-fft, cross-correlation]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 8.7.3, Implementing Linear Time-Invariant Systems Using the DFT (the overlap-save method)
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: Section 7.3.2, Filtering of Long Data Sequences (the overlap-save method)
  - paper: doi:10.1145/1464182.1464209
    title: Thomas G. Stockham Jr., High-speed convolution and correlation, AFIPS Spring Joint Computer Conference 28, 1966, 229 to 233
    locator: sectioned convolution of a long input by FFT
  - paper: "Howard D. Helms, IEEE Transactions on Audio and Electroacoustics AU-15(2), June 1967"
    title: Howard D. Helms, Fast Fourier transform method of computing difference equations and simulating filters, IEEE Transactions on Audio and Electroacoustics 15(2), 1967, 85 to 90
    locator: FFT filtering of long sequences in sections
---

The overlap-save method computes the [discrete convolution](/discrete-convolution/) $y = x * h$ of a long input $x$ with a filter $h$ of length $M$ from blocks of $N$ input samples that overlap by $M - 1$. Each block is circularly convolved with $h$ by FFTs of length $N$. The first $M - 1$ outputs of a block are wrong, because the circular convolution wraps the end of the block onto its start; the other $N - M + 1$ outputs are exact samples of $y$, and the method keeps only those. With $N$ a small multiple of $M$ it costs $O(\log M)$ operations per output sample, like the [overlap-add method](/overlap-add-method/), and it needs no additions of overlapping tails.

## In plain words

You read a long recording through a window of $N$ samples, and you move the window forward by a bit less than its width each time. Each window shares its first $M - 1$ samples with the end of the window before.

You filter each window with one small FFT. The FFT treats the window as if it repeated forever, so at the start of the window the filter sees samples from the end of the window. Those first $M - 1$ results are garbage, and you throw them away. The rest of the results only used samples that are really in the window and in the right order. They are correct, and you keep them. The windows overlap by exactly the number of thrown-away results, so the kept parts fit together with no gap.

## The problem

The input is a signal $x[0 \ldots L-1]$, a filter $h[0 \ldots M-1]$ and an FFT length $N \ge M$, usually a power of two. The output is $y[n] = \sum_{k=0}^{M-1} h[k]\, x[n-k]$ for $0 \le n \le L + M - 2$, with $x[i] = 0$ outside $0 \le i \le L - 1$. This is the [discrete convolution](/discrete-convolution/) problem with $L \gg M$.

## The algorithm

FFT$_N$ and IFFT$_N$ are the DFT and its inverse of length $N$, computed by the [fast Fourier transform](/fast-fourier-transform/). The signal $x'$ is $x$ delayed by $M - 1$ samples, so that the first block has a history of zeros.

```pseudo id=main
OVERLAP-SAVE(x, h, N)                      ▷ x has length L, h has length M ≤ N
L1  B ← N − M + 1                          ▷ new output samples per block
L2  Hf ← FFT_N(h padded with zeros to length N)
L3  x′[t] ← x[t − (M − 1)] for M − 1 ≤ t < L + M − 1, else 0
L4  y ← L + M − 1 zeros
L5  for s ← 0, B, 2B, ... while s < L + M − 1 do
L6      u ← x′[s .. s + N − 1]               ▷ overlaps the block before by M − 1 samples
L7      v ← IFFT_N(FFT_N(u) · Hf)          ▷ v = u ⊛_N h
L8      for j ← M − 1 to N − 1 do          ▷ discard v[0 .. M − 2], which wrapped
L9          if s + j − (M − 1) < L + M − 1 then y[s + j − (M − 1)] ← v[j]
L10 return y
```

Line L3 does not need a copy: a real program reads $x$ through a buffer of $N$ samples and keeps its last $M - 1$ samples for the next block. In line L7, the output $v[j] = \sum_{k=0}^{M-1} h[k]\, u[(j - k) \bmod N]$ uses $u[j], u[j-1], \ldots, u[j - M + 1]$. For $j \ge M - 1$ these indices are all in $[0, N - 1]$, so there is no wrap and $v[j]$ is a true output sample; for $j < M - 1$ some index wraps to the end of the block. The loop of line L8 keeps the $B$ good samples, and line L9 writes them to their places in $y$, which the next block continues with no gap and no overlap.

## Example

Let $x = [1, 2, 3, 4, 5, 6, 7]$ ($L = 7$), $h = [1, 1, 1]$ ($M = 3$) and $N = 4$. Then $B = 2$, $x' = [0, 0, 1, 2, 3, 4, 5, 6, 7, 0, 0, \ldots]$, and the output has 9 samples. The cyclic output is $v[j] = u[j] + u[(j-1) \bmod 4] + u[(j-2) \bmod 4]$.

| $s$ | block $u$ | $v = u \circledast_4 h$ | discarded | kept, at $y$ indices |
|---|---|---|---|---|
| 0 | [0, 0, 1, 2] | [3, 2, 1, 3] | 3, 2 | 1, 3 at 0, 1 |
| 2 | [1, 2, 3, 4] | [8, 7, 6, 9] | 8, 7 | 6, 9 at 2, 3 |
| 4 | [3, 4, 5, 6] | [14, 13, 12, 15] | 14, 13 | 12, 15 at 4, 5 |
| 6 | [5, 6, 7, 0] | [12, 11, 18, 13] | 12, 11 | 18, 13 at 6, 7 |
| 8 | [7, 0, 0, 0] | [7, 7, 7, 0] | 7, 7 | 7 at 8 (index 9 is past the end) |

So $y = [1, 3, 6, 9, 12, 15, 18, 13, 7]$, the direct convolution. In the row $s = 2$, the discarded $v[0] = 8$ is $u[0] + u[3] + u[2] = 1 + 4 + 3$: it mixes the start of the block with its end. The true sample $y[1] = 3$ came from the block before.

## Correctness

For $j \ge M - 1$, the sum of line L7 only reads $u[j - k]$ with $0 \le j - k \le N - 1$, so $v[j] = \sum_k h[k]\, x'[s + j - k] = y[s + j - (M - 1)]$, by the delay of line L3. The kept indices $s + j - (M - 1)$ for $M - 1 \le j \le N - 1$ form the interval $[s, s + B - 1]$, and the starts $0, B, 2B, \ldots$ make these intervals cover the output once. The full proof is below.

## Complexity

The loop of line L5 runs $\lceil (L + M - 1) / B \rceil$ times. Each pass does one FFT and one inverse FFT of length $N$ and $N$ products. With a radix-2 FFT, this is $N \log_2 N + N$ complex multiplications for $B = N - M + 1$ output samples, the same count as overlap-add:

$$\frac{N \log_2 N + N}{N - M + 1} \text{ per output sample},$$

which is $O(\log M)$ for $N = 2M$, and $O((L + M) \log M)$ in total in the [real RAM](/real-ram/). The cost function and its minimum at $N$ a few times $M$ are on the [overlap-add method](/overlap-add-method/) page. Overlap-save does no additions of tails. It runs $\lceil (L + M - 1)/B \rceil$ blocks against $\lceil L/B \rceil$ for overlap-add, because its blocks also produce the last $M - 1$ samples; with $N \ge 2M - 1$ this is at most one block more. The extra space is $O(N) = O(M)$ for $H_f$, one block and the $M - 1$ samples of history. The delay is one block of $B$ samples plus the computing time of a block.

## Properties

- **Exact in exact arithmetic.** With an exact cyclic convolution in line L7, the result is exact. In floating point, each output sample comes from exactly one block, so its error is the error of one FFT pair.
- **Each output written once.** Line L9 writes every output sample exactly once, with no read-modify-write of $y$, so blocks can run in parallel and the output can go straight to a device.
- **Stream form.** The state between blocks is the last $M - 1$ input samples, the same state as the direct form of an [FIR filter](/fir-filter/).
- **Linear and time invariant.** It computes the same LTI system as the direct form.

## Variants and improvements

- **Overlap-add.** The [overlap-add method](/overlap-add-method/) uses blocks of $x$ that do not overlap and pads them, so nothing wraps, then adds the overlapping output tails.
- **Uniformly partitioned convolution.** For a long filter at a small delay, split $h$ into partitions of length $B$, keep the spectra of the last input blocks in a frequency-domain delay line, and sum their products with the partition spectra before one inverse FFT. Each block then costs one forward and one inverse FFT plus one product per partition.
- **Non-uniform partitions.** Short partitions at the start of $h$ and longer ones later, with a direct-form head, give a delay of zero. Gardner described such a hybrid in 1995; see [digital filtering](/digital-filtering/).
- **Correlation.** Use the reversed conjugate of the template as $h$ to get a sliding [cross-correlation](/cross-correlation/), for example a [matched filter](/matched-filter/) on a long stream.
- **Real-valued FFTs.** For real data, a [real-valued FFT](/real-valued-fft/) halves the work.
- **Frequency-domain adaptive filters.** Block LMS filters update $H_f$ between blocks and use overlap-save for the filtering; see [adaptive filtering](/adaptive-filtering/).

## When to use it

Use overlap-save for streaming FIR filtering of more than a few dozen taps when a delay of one block is acceptable: the input buffer slides, each output is written once, and no output accumulator is needed. It has the same cost as overlap-add, so the choice is about the data flow. Use overlap-add when the input comes in separate frames, or when the frames are processed in the frequency domain anyway. For a short filter use the direct form, and for a whole signal in memory use one [convolution via FFT](/convolution-via-fft/).

## Pitfalls

- **Keeping the wrong samples.** Keeping $v[0 \ldots B-1]$ instead of $v[M - 1 \ldots N - 1]$ in line L8 gives the $M - 1$ wrapped samples at the start of each block. The loop must start at $j = M - 1$.
- **No zero history.** Without the $M - 1$ leading zeros of line L3, the first block discards the first $M - 1$ samples of $y$, and the whole output is shifted by $M - 1$. Start with $M - 1$ zeros, or drop the first $M - 1$ samples of $y$ on purpose if you want the "valid" mode.
- **Wrong step.** A step of $N$ or of $N - M$ between blocks in line L5 leaves a gap or writes a sample twice. The step must be $B = N - M + 1$, the number of kept samples.
- **A filter longer than the FFT.** With $M > N$, every output wraps. Line L1 needs $N \ge M$, and $N \ge 2M$ for a good cost.

## Implementations

## History

Thomas Stockham showed in 1966 how to convolve a long input in sections with FFTs of a fixed length, and Howard Helms treated FFT methods for filtering and difference equations in 1967. The two textbook forms are the overlap-add method, which adds the output tails, and the overlap-save method, which discards the wrapped outputs; the second is also called overlap-discard and select-save. The sources checked here do not settle who first described the save form.

## References
