---
tag: H1GGYR
kind: algorithm
slug: overlap-add-method
name: Overlap-add method
aliases:
- overlap-add
area: graphics-and-signals/signal-processing
level: core
summary: Block convolution of a long signal with a short filter using FFTs and summed overlapping tails.
solves: [discrete-convolution]
model: real-ram
complexity:
  vars: {L: the length of the input, M: the length of the filter, N: "the FFT length, a small multiple of M"}
  time: {worst: O((L + M) log M)}
  space: {extra: O(M)}
properties: {deterministic: true, online: true, in_place: false, exact: false}
history:
  year: 1966
  people: [Thomas G. Stockham Jr.]
  note: Stockham described sectioned convolution with the FFT in 1966, one year after the Cooley-Tukey paper.
prereqs: [discrete-convolution, circular-convolution, convolution-via-fft]
see_also: [overlap-save-method, fast-fourier-transform, fir-filter, digital-filtering, short-time-fourier-transform, real-valued-fft]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 8.7.3, Implementing Linear Time-Invariant Systems Using the DFT (the overlap-add method)
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: Section 7.3.2, Filtering of Long Data Sequences (the overlap-add method)
  - paper: doi:10.1145/1464182.1464209
    title: Thomas G. Stockham Jr., High-speed convolution and correlation, AFIPS Spring Joint Computer Conference 28, 1966, 229 to 233
    locator: the sectioning of a long input into blocks, each convolved by FFT
---

The overlap-add method computes the [discrete convolution](/discrete-convolution/) $y = x * h$ of a long input $x$ with a filter $h$ of length $M$, one block at a time. It cuts $x$ into blocks of $B = N - M + 1$ samples, convolves each block with $h$ by FFTs of length $N$, and adds the overlapping tails of the block outputs. With $N$ a small multiple of $M$, the cost is $O(\log M)$ operations per output sample, against $M$ for the direct sum. It is the block form of [convolution via FFT](/convolution-via-fft/), and the delay from input to output is one block instead of the whole input.

## In plain words

A long recording and a short filter are given. One big FFT of the whole recording would work, but it needs all the samples first and a lot of memory. So you cut the recording into short pieces that do not overlap. You filter each piece alone with a small FFT.

A filtered piece is longer than the piece: the filter adds a tail of $M - 1$ samples at its end. That tail falls on top of the start of the next filtered piece. You add the overlapping parts together. The sum is exactly the filtered recording, because filtering a sum of pieces gives the sum of the filtered pieces.

## The problem

The input is a signal $x[0 \ldots L-1]$, a filter $h[0 \ldots M-1]$ and an FFT length $N \ge M$, usually a power of two. The output is the full linear convolution $y[n] = \sum_{k=0}^{M-1} h[k]\, x[n-k]$ for $0 \le n \le L + M - 2$, with $x[i] = 0$ outside $0 \le i \le L - 1$. This is the [discrete convolution](/discrete-convolution/) problem with $L \gg M$.

## The algorithm

FFT$_N$ and IFFT$_N$ are the DFT and the inverse DFT of length $N$, computed by the [fast Fourier transform](/fast-fourier-transform/). The product of two spectra is taken entry by entry.

```pseudo id=main
OVERLAP-ADD(x, h, N)                       ▷ x has length L, h has length M ≤ N
L1  B ← N − M + 1                          ▷ new input samples per block
L2  Hf ← FFT_N(h padded with zeros to length N)
L3  y ← L + M − 1 zeros
L4  for s ← 0, B, 2B, ... while s < L do
L5      u ← x[s .. s + B − 1] padded with zeros to length N    ▷ the last block can be short
L6      v ← IFFT_N(FFT_N(u) · Hf)          ▷ v = u ⊛_N h, which equals u ∗ h
L7      for j ← 0 to N − 1 do
L8          if s + j < L + M − 1 then y[s + j] ← y[s + j] + v[j]
L9  return y
```

Line L2 transforms the filter once. Each pass of the loop of line L4 takes the next $B$ input samples. A block has at most $B$ nonzero samples, so its linear convolution with $h$ has at most $B + M - 1 = N$ samples, and the [circular convolution](/circular-convolution/) of length $N$ in line L6 has nothing to wrap: $v$ is the exact linear convolution of the block. Lines L7 and L8 add $v$ into $y$ at offset $s$. The first $B$ samples of $v$ fall on new positions, and the last $M - 1$ fall on the first $M - 1$ samples of the next block: this is the overlap that is added. The test of line L8 drops samples past the end of $y$, which are zero in exact arithmetic.

## Example

Let $x = [1, 2, 3, 4, 5, 6, 7]$ ($L = 7$), $h = [1, 1, 1]$ ($M = 3$) and $N = 4$. Then $B = 2$, and the output has $L + M - 1 = 9$ samples.

| $s$ | block $u$ (padded to 4) | $v = u * h$ | added at | $y$ after the block |
|---|---|---|---|---|
| 0 | [1, 2, 0, 0] | [1, 3, 3, 2] | 0 to 3 | [1, 3, 3, 2, 0, 0, 0, 0, 0] |
| 2 | [3, 4, 0, 0] | [3, 7, 7, 4] | 2 to 5 | [1, 3, 6, 9, 7, 4, 0, 0, 0] |
| 4 | [5, 6, 0, 0] | [5, 11, 11, 6] | 4 to 7 | [1, 3, 6, 9, 12, 15, 11, 6, 0] |
| 6 | [7, 0, 0, 0] | [7, 7, 7, 0] | 6 to 8 | [1, 3, 6, 9, 12, 15, 18, 13, 7] |

In the second row, the tail $[3, 2]$ of the first block adds to the head $[3, 7]$ of the second, and gives $6$ and $9$. The final $y$ is the direct convolution, $y[n] = x[n] + x[n-1] + x[n-2]$. In the last row the sample $v[3] = 0$ would land at index $9$, so line L8 drops it.

## Correctness

Write $x = \sum_s S_s u_s$, where $u_s$ is the block that starts at $s$ and $S_s$ shifts by $s$. Convolution is linear and commutes with shifts, so $x * h = \sum_s S_s (u_s * h)$. Each block has at most $B$ nonzero samples, so $u_s * h$ has at most $N$ samples and the circular convolution of length $N$ equals it. Lines L7 and L8 add exactly $S_s(u_s * h)$ into $y$. The full proof is below.

## Complexity

The loop of line L4 runs $\lceil L / B \rceil$ times. Each pass does one FFT and one inverse FFT of length $N$, $N$ complex products and $N$ additions. A radix-2 FFT of length $N$ costs $\frac{N}{2} \log_2 N$ complex multiplications, so one block costs $N \log_2 N + N$ of them, and gives $B = N - M + 1$ new output samples. The cost per output sample is

$$\frac{N \log_2 N + N}{N - M + 1}.$$

With $N = 2M$ this is at most $2(\log_2 M + 2)$, so it is $O(\log M)$, and the total is $O((L + M) \log M)$ in the [real RAM](/real-ram/), counting the transform of $h$. The direct sum costs $M$ multiplications per sample. The function has its minimum at $N$ a few times $M$: in this count, for $M = 64$ it is $15.75$ at $N = 128$, $11.94$ at $N = 256$, $11.40$ at $N = 512$ and $11.72$ at $N = 1024$. A complex multiplication is three or four real ones, and a [real-valued FFT](/real-valued-fft/) halves the cost for real data. The extra space is $O(N) = O(M)$ for $H_f$ and one block, apart from the output. The delay from an input sample to its output is at most one block of $B$ samples plus the computing time of a block.

## Properties

- **Exact in exact arithmetic.** In floating point, the FFT adds a rounding error of the order of $\varepsilon \log_2 N$ times the size of the data, where $\varepsilon$ is the unit round-off. With integer data, rounding the result gives the exact integers while the error stays below $1/2$.
- **Block online.** The output for a block is final after that block and the tail of the one before. A stream is processed one block at a time with $M - 1$ samples of state.
- **Linear and time invariant.** It computes the same LTI system as the direct form, so causality and stability are those of $h$.
- **Any block convolution.** Line L6 can use any method that gives the exact linear convolution of a block, for example the direct sum or an exact cyclic convolution; the overlap logic does not change.

## Variants and improvements

- **Overlap-save.** The [overlap-save method](/overlap-save-method/) overlaps the input blocks instead of the output blocks, and discards the $M - 1$ wrapped samples of each block. It has the same cost and saves the additions of the tails.
- **Real-valued FFTs.** For real $x$ and $h$, use a [real-valued FFT](/real-valued-fft/), or put two blocks into the real and imaginary parts of one complex FFT.
- **Partitioned filters.** For a long filter and a small delay, cut $h$ into partitions of length $B$ too, keep the spectra of the last input blocks, and sum their products with the partition spectra. The delay is then one partition, not one filter length.
- **Non-uniform partitions.** Short partitions at the start of $h$ and longer ones later give a delay of zero with a direct-form head; Gardner described such a scheme in 1995. See [digital filtering](/digital-filtering/).
- **Weighted overlap-add.** The synthesis step of the [short-time Fourier transform](/short-time-fourier-transform/) adds windowed overlapping frames in the same way; it is a different use of the same addition.
- **Two dimensions.** Images are filtered by 2D tiles with the same rule, see [linear filtering](/linear-filtering/).

## When to use it

Use overlap-add to apply an FIR filter of more than a few dozen taps to a long or endless signal, when a delay of one block is acceptable. The crossover with the direct form depends on the machine and on the FFT library, so measure it. For a short filter, use the direct form of the [FIR filter](/fir-filter/). For a signal that fits in memory and is filtered once, a single [convolution via FFT](/convolution-via-fft/) is simpler. Prefer overlap-add when the input already comes in frames that do not overlap, and the [overlap-save method](/overlap-save-method/) when you read a stream into a sliding buffer.

## Pitfalls

- **A block that is too long.** With $B = N$ in line L1, the convolution of a block has $N + M - 1$ samples, and the circular convolution of line L6 wraps the last $M - 1$ onto the first. Line L1 must give $B = N - M + 1$, or less.
- **A lost tail.** If $y$ in line L3 has only $L$ samples, or the loop stops before the last block, the last $M - 1$ output samples are missing. The full output has $L + M - 1$ samples; cut it after the loop if you need the "same" mode.
- **The filter transform in the loop.** Computing FFT$_N(h)$ inside the loop of line L4 doubles the cost per block. Line L2 does it once.
- **Complex output for real data.** The inverse FFT of line L6 returns complex numbers with small imaginary parts from rounding. Keep the real parts for real data, and round to integers only when the data are integers.
- **Too small an FFT.** With $N$ close to $M$, the block gives few new samples: $N = M$ gives $B = 1$ and costs more than the direct sum. Take $N$ at least $2M$.

## Implementations

## History

Thomas Stockham described sectioned convolution with the FFT in 1966, one year after the Cooley-Tukey paper made FFTs practical. He cut a long input into sections, convolved each section with the filter by an FFT of a padded length, and added the overlapping results. Helms described FFT methods for difference equations and filters in 1967. The textbooks of Oppenheim and Schafer and of Proakis and Manolakis present overlap-add and overlap-save as the two standard block methods.

## References
