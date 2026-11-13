---
tag: A2Z6XD
kind: algorithm
slug: fir-filter
name: FIR filter
aliases:
- finite impulse response filter
- direct-form FIR
area: graphics-and-signals/signal-processing
level: intro
summary: "Compute y[n] = h[0] x[n] + ... + h[M] x[n-M] from the last M + 1 inputs. It is always stable, and symmetric taps give exactly linear phase."
solves: [digital-filtering]
model: real-ram
complexity:
  vars: {M: the filter order (M + 1 taps), N: the number of input samples}
  time: {worst: Θ(N M), average: Θ(N M), best: Θ(N M), per_sample: Θ(M)}
  space: {extra: Θ(M)}
properties: {causal: true, stable: true, linear_phase: "when the taps are symmetric or antisymmetric", online: true, deterministic: true, recursive: false, in_place: false}
history:
  year: 1940
  people: [Heinz E. Kallmann]
  note: Kallmann described the transversal filter, a tapped delay line whose taps are weighted and added, in 1940. The digital form came with the digital filters of the 1960s.
prereqs: [discrete-convolution, impulse-response, frequency-response]
see_also: [iir-filter, digital-filter-design, parks-mcclellan-algorithm, polyphase-decomposition, overlap-add-method, convolution-via-fft, moving-average, bibo-stability]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 6, Structures for Discrete-Time Systems (the direct form and the transposed form of FIR systems), and Section 5.7, Linear Systems with Generalized Linear Phase (the four types of linear phase FIR systems)
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: the chapter on the implementation of discrete-time systems (structures for FIR systems) and the chapter on the design of digital filters (symmetric and antisymmetric FIR filters)
  - paper: doi:10.1109/JRPROC.1940.229346
    title: Heinz E. Kallmann, Transversal Filters, Proceedings of the IRE 28(7), 1940
    locator: pp. 302 to 310 (the tapped delay line with weighted taps, and its response without phase distortion)
---

A finite impulse response (FIR) filter computes each output sample as a fixed weighted sum of the current input and the last $M$ inputs: $y[n] = \sum_{k=0}^{M} h[k]\, x[n-k]$. The $M + 1$ weights $h[0], \ldots, h[M]$ are the taps, and they are also the [impulse response](/impulse-response/) of the filter, which is zero after $M$ samples. The direct form keeps the last $M + 1$ inputs in a delay line and costs $M + 1$ multiplies per output sample. An FIR filter is causal and always stable. If its taps are symmetric, $h[k] = h[M-k]$, its phase is exactly linear in frequency, so all frequencies are delayed by the same $M/2$ samples. Frequencies on this page are in radians per sample, $\omega \in [-\pi, \pi]$.

## In plain words

Keep the last few input samples in a row. Give each position in the row a fixed weight. When a new sample comes in, push it in at the front and drop the oldest one. Then multiply each sample by its weight and add the products. The sum is the output. If all the weights are equal and add up to one, the output is the average of the last few samples, which smooths the signal.

The filter only looks at a fixed number of past inputs, so one spike in the input can change only that many outputs. It can never feed back on itself. If the weights read the same from both ends, the filter delays every tone by the same amount, so it does not change the shape of a pulse.

## The problem

The input is a stream of samples $x[0], x[1], \ldots$ and the taps $h[0 \ldots M]$. Samples before $n = 0$ are zero. The output is $y[n] = \sum_{k=0}^{M} h[k]\, x[n-k]$ for each $n \ge 0$, produced as soon as $x[n]$ arrives. This is the [discrete convolution](/discrete-convolution/) of $x$ with a finite $h$, in the online form that [digital filtering](/digital-filtering/) needs. In terms of the [z-transform](/z-transform/), the [transfer function](/transfer-function/) is the polynomial $H(z) = \sum_{k=0}^{M} h[k] z^{-k}$, with no poles except at $z = 0$.

## The algorithm

The delay line $B[0 \ldots M]$ is a [circular buffer](/circular-buffer/). The new input overwrites the oldest one, so no sample moves.

```pseudo id=main
FIR-FILTER(h[0 .. M], x)                   ▷ y[n] = Σ h[k] x[n − k]
L1  B[0 .. M] ← 0, p ← 0                   ▷ the delay line and the write position
L2  for each new input v = x[n] do
L3      B[p] ← v                           ▷ overwrite x[n − M − 1]
L4      acc ← h[0] · B[p]
L5      for k ← 1 to M do
L6          j ← (p − k) mod (M + 1)         ▷ B[j] holds x[n − k]
L7          acc ← acc + h[k] · B[j]
L8      output y[n] ← acc
L9      p ← (p + 1) mod (M + 1)
```

The output of line L8 does not depend on any earlier output, so the filter has no feedback. This is the difference with an [IIR filter](/iir-filter/).

**Frequency response.** The input $x[n] = e^{i\omega n}$ gives $y[n] = H(e^{i\omega})\, e^{i\omega n}$ with the [frequency response](/frequency-response/) $H(e^{i\omega}) = \sum_{k=0}^{M} h[k]\, e^{-i\omega k}$. The filter multiplies each tone by this complex number.

**Linear phase.** If $h[k] = h[M-k]$, pair the term $k$ with the term $M - k$:

$$H(e^{i\omega}) = e^{-i\omega M/2} A(\omega), \qquad A(\omega) = \sum_{k=0}^{M} h[k] \cos\!\big(\omega (M/2 - k)\big),$$

and $A$ is real. So the phase is $-\omega M/2$, with a jump of $\pi$ where $A$ changes sign, and the group delay is $M/2$ samples at each frequency. If $h[k] = -h[M-k]$, the same pairing gives $H = i\, e^{-i\omega M/2} A(\omega)$ with a sine sum for $A$. This gives four types:

| type | symmetry | order $M$ | forced zeros of $H$ | typical use |
|---|---|---|---|---|
| 1 | $h[k] = h[M-k]$ | even | none | any band |
| 2 | $h[k] = h[M-k]$ | odd | $\omega = \pi$ | low-pass, band-pass |
| 3 | $h[k] = -h[M-k]$ | even | $\omega = 0$ and $\omega = \pi$ | differentiator over a band, Hilbert transformer |
| 4 | $h[k] = -h[M-k]$ | odd | $\omega = 0$ | differentiator, Hilbert transformer |

The forced zeros come from $A(\pi)$ or $A(0)$: for type 2 each cosine $\cos(\pi(M/2 - k))$ has a half-integer multiple of $\pi$ in it, so it is zero.

## Example

Take the moving average $h = [\tfrac14, \tfrac14, \tfrac14, \tfrac14]$, so $M = 3$, and the input $x = [0, 0, 4, 8, 8, 8, 0]$.

| $n$ | delay line, newest first | $y[n]$ |
|---|---|---|
| 0 | 0, 0, 0, 0 | 0 |
| 1 | 0, 0, 0, 0 | 0 |
| 2 | 4, 0, 0, 0 | 1 |
| 3 | 8, 4, 0, 0 | 3 |
| 4 | 8, 8, 4, 0 | 5 |
| 5 | 8, 8, 8, 4 | 7 |
| 6 | 0, 8, 8, 8 | 6 |

The output rises over four samples where the input rises in two: the filter smooths the step. The taps are symmetric with odd order, so the filter is of type 2. Its amplitude is $A(\omega) = \tfrac12\big(\cos(3\omega/2) + \cos(\omega/2)\big)$, so $A(0) = 1$, and $A(\pi/2) = A(\pi) = 0$. The group delay is $3/2$ samples. A tone at $\omega = \pi/2$, such as $x = [1, 0, -1, 0, 1, 0, -1, \ldots]$, gives zero output once the delay line is full.

## Correctness

The proof uses one [loop invariant](/loop-invariant/). At the start of the step for $x[n]$, the position is $p = n \bmod (M + 1)$, and for $k = 1, \ldots, M$ the cell $B[(p - k) \bmod (M + 1)]$ holds $x[n-k]$, with $x[i] = 0$ for $i < 0$. Line L3 then puts $x[n]$ in the one cell that held $x[n - M - 1]$, which the sum does not need. So lines L4 to L7 add $h[k]\, x[n-k]$ for each $k$, and line L8 outputs $y[n]$. Line L9 moves $p$ on by one, which shifts every age by one and restores the invariant. The full proof, with the linear phase identity and the stability bound, is in the proof file.

## Complexity

- **Per output sample:** $M + 1$ multiplies and $M$ additions. This is the cost model of the area: a direct FIR filter costs $\Theta(M)$ per sample.
- **For $N$ samples:** $\Theta(NM)$ time.
- **Space:** the $M + 1$ cells of the delay line and the $M + 1$ taps, $\Theta(M)$.
- **Latency:** none. The output $y[n]$ is ready as soon as $x[n]$ is in.

For long filters, block convolution with the FFT, by the [overlap-add method](/overlap-add-method/) or the [overlap-save method](/overlap-save-method/), costs $\Theta(\log M)$ multiplies per sample, at the price of a delay of about one block. For short filters the direct form is faster.

## Properties

- **Causal.** The output $y[n]$ uses only $x[n], \ldots, x[n-M]$.
- **Always stable.** If $|x[n]| \le X$ for all $n$, then $|y[n]| \le X \sum_k |h[k]|$. A finite sum is finite, so the filter is [BIBO stable](/bibo-stability/) for every choice of taps. The bound is reached by the input $x[n-k] = X \operatorname{sign}(h[k])$.
- **Linear phase when the taps are symmetric or antisymmetric**, as in the table above. An IIR filter cannot have exactly linear phase and be causal and stable at the same time; an FIR filter can.
- **Finite memory.** An input sample affects at most $M + 1$ outputs. Errors and start-up effects are gone after $M$ samples.
- **No limit cycles.** With rounded arithmetic, an FIR filter with zero input reaches zero output after $M$ samples. A recursive filter can keep a small oscillation forever.

## Variants and improvements

- **Symmetric folding.** For a linear phase filter, add $x[n-k] + x[n-M+k]$ first and multiply once. This uses $\lceil (M+1)/2 \rceil$ multiplies per sample.
- **Transposed form.** Multiply the input by all taps and add the products into a chain of partial sums. It has the same cost and suits hardware with a short critical path.
- **Block convolution.** Use the FFT on blocks of the input, by the overlap-add or the overlap-save method, for filters with hundreds of taps or more.
- **Polyphase form.** For a filter followed by a decimator, or a filter after an expander, split the taps into phases and compute only the samples that are kept. See [polyphase decomposition](/polyphase-decomposition/) and [polyphase resampling](/polyphase-resampling/).
- **Design.** The taps come from a specification. Windowing the ideal impulse response, see [window functions](/window-functions/), is simple. The [Parks-McClellan algorithm](/parks-mcclellan-algorithm/) gives the shortest equiripple filter. The [Savitzky-Golay filter](/savitzky-golay-filter/) gets its taps from a local least squares fit. See [digital filter design](/digital-filter-design/) for the full list.

## When to use it

Use an FIR filter when the phase matters: audio crossovers, data transmission and image processing need the same delay at all frequencies. Use it when you need a guaranteed stable filter, or when you run it in fixed point arithmetic, because it has no feedback that can grow or ring. Use it in multirate systems, where the polyphase form makes it cheap. If you need a sharp cutoff at low cost and the phase does not matter, an [IIR filter](/iir-filter/) reaches the same magnitude specification with a much lower order.

## Pitfalls

- **Off-by-one in the delay line.** A buffer of $M$ cells for a filter of order $M$ loses one input. The filter has $M + 1$ taps and needs $M + 1$ cells.
- **Shifting the buffer.** Moving all samples one place per input costs $M$ copies per sample. Use a circular index, or a buffer of twice the length that is written at two places, so that the window is always contiguous.
- **Group delay.** A linear phase filter of order $M$ delays the signal by $M/2$ samples. Compensate for it when you compare the output with the input. For even $M$ the delay is a whole number of samples; for odd $M$ it is half a sample.
- **The wrong type.** A type 2 filter always has $H(e^{i\pi}) = 0$, so it cannot be a high-pass filter. A type 3 or type 4 filter has $H(1) = 0$, so it cannot pass a constant.
- **Overflow in fixed point.** The output can be up to $\sum_k |h[k]|$ times the input. Use an accumulator with enough guard range, or scale the taps.

## Implementations

## History

Heinz Kallmann described the transversal filter in 1940. It was a delay cable with taps, and the tapped signals were weighted and added. He showed that such a filter can approximate a given amplitude response without phase distortion. Digital filters followed in the 1960s, when the delay cable became a memory and the weights became multiplies. The design methods for FIR filters by windows, by frequency sampling and by the Remez exchange came in the late 1960s and early 1970s.

## References
