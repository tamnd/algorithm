---
tag: 8YF7JV
kind: algorithm
slug: lifting-scheme
name: Lifting scheme
aliases:
- lifting wavelet construction
- second-generation wavelets
area: graphics-and-signals/signal-processing
level: advanced
summary: Wavelet transform level as split, predict and update steps; in place, exactly invertible, also integer to integer.
model: real-ram
complexity:
  vars: {N: the signal length, T: "the total number of taps over all lifting steps of one level"}
  time: {worst: Θ(T N), average: Θ(T N), best: Θ(T N)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: true, exact: true}
history:
  year: 1996
  people: [Wim Sweldens, Ingrid Daubechies]
  note: Sweldens (1996, 1998) built wavelets from predict and update steps. Daubechies and Sweldens (1998) showed that every finite two-channel filter bank factors into such steps.
prereqs: [discrete-wavelet-transform, polyphase-decomposition]
see_also: [fast-wavelet-transform, haar-wavelet-transform, haar-wavelet, filter-bank, perfect-reconstruction, jpeg-2000, subband-coding, scalar-quantization]
sources:
  - paper: doi:10.1006/acha.1996.0015
    title: Wim Sweldens, The lifting scheme, a custom-design construction of biorthogonal wavelets, Applied and Computational Harmonic Analysis 3(2), 1996
    locator: pages 186 to 200 (the lifting step that changes a biorthogonal filter pair, and its use to add vanishing moments)
  - paper: doi:10.1137/S0036141095289051
    title: Wim Sweldens, The lifting scheme, a construction of second generation wavelets, SIAM Journal on Mathematical Analysis 29(2), 1998
    locator: pages 511 to 546 (the split, predict and update form, wavelets on intervals and irregular samples, and the in-place transform)
  - paper: doi:10.1007/BF02476026
    title: Ingrid Daubechies and Wim Sweldens, Factoring wavelet transforms into lifting steps, Journal of Fourier Analysis and Applications 4(3), 1998
    locator: pages 247 to 269 (the factorization of a polyphase matrix into lifting steps by the Euclidean algorithm, and the operation counts)
  - paper: doi:10.1006/acha.1997.0238
    title: A. Robert Calderbank, Ingrid Daubechies, Wim Sweldens and Boon-Lock Yeo, Wavelet transforms that map integers to integers, Applied and Computational Harmonic Analysis 5(3), 1998
    locator: pages 332 to 369 (rounding inside each lifting step gives an invertible integer transform)
  - book: isbn:9780123743701
    title: Stéphane Mallat, A Wavelet Tour of Signal Processing, The Sparse Way, third edition, Academic Press, 2009
    locator: Chapter 7 (the section on lifting)
---

The lifting scheme computes one level of a two-channel [discrete wavelet transform](/discrete-wavelet-transform/) by splitting the signal into its even and odd samples and then running a short list of *lifting steps*: a predict step adds a filtered copy of the even half to the odd half, and an update step adds a filtered copy of the odd half to the even half. Each step reads one half and writes the other, so it works in place and is undone by the same step with the opposite sign. This makes the inverse exact even when each step rounds its result to an integer, which gives the reversible 5/3 transform of [JPEG 2000](/jpeg-2000/). Daubechies and Sweldens (1998) showed that every finite filter bank with perfect reconstruction factors into lifting steps, and the lifted form needs fewer operations than the convolution form.

## In plain words

Split a list of numbers into the ones at even places and the ones at odd places. Guess each odd number from its even neighbors, and keep only the error of the guess. Where the signal is smooth, the guess is good, and the errors are small. Then nudge each even number with the nearby errors, so that the even numbers keep the average of the signal. The even list is now a short, smooth copy of the signal, and the odd list holds the detail.

To undo it, run the same steps backwards with the opposite sign. Each step changes only one list and reads only the other, which has not changed yet, so you always know what was added and can take it away. This works even if each step rounds to whole numbers, so whole numbers go in, whole numbers come out, and nothing is lost.

## The problem

**Input.** A signal $x[0], \ldots, x[N-1]$ with $N$ even, and a two-channel perfect reconstruction [filter bank](/filter-bank/) given as a list of lifting steps. Let $h = N/2$, let $s[i] = x[2i]$ (the even half) and $d[i] = x[2i+1]$ (the odd half). Indices of $s$ and $d$ are taken modulo $h$, which is the periodic extension of the signal.

**Lifting steps.** A step is a kind, P (predict) or U (update), and a finite set of taps $c_k$ at integer offsets $k$. They act as

$$\text{P: } d[i] \leftarrow d[i] + \sum_k c_k\, s[i + k], \qquad \text{U: } s[i] \leftarrow s[i] + \sum_k c_k\, d[i + k].$$

After the last step, the halves are scaled by constants $K_s$ and $K_d$, which are $1$ unless the target filters are orthonormal.

**Output.** The approximation $s$ and the detail $d$ of one level, equal to the outputs of the analysis filters $\tilde h$ and $\tilde g$ of the filter bank, each followed by keeping every second output. The multilevel transform runs the level again on $s$.

**Polyphase form.** In the [polyphase](/polyphase-decomposition/) notation, with $z$ the delay variable of the [z-transform](/z-transform/), a P step multiplies the vector of the two halves by $\begin{pmatrix} 1 & 0 \\ p(z) & 1 \end{pmatrix}$ and a U step by $\begin{pmatrix} 1 & u(z) \\ 0 & 1 \end{pmatrix}$, where $p$ and $u$ are Laurent polynomials made from the taps. Lifting writes the polyphase matrix of the analysis filters as a product of these triangular matrices and a diagonal scaling.

**Cost model.** The [real RAM](/real-ram/). For rational taps, as in the Haar and 5/3 cases, the arithmetic is exact. The integer version rounds each step, and then all values stay integers.

## The algorithm

```pseudo id=main
LIFT-FORWARD(x, steps, K_s, K_d)       ▷ |x| = N even, h = N/2
L1  s ← the even places of x, d ← the odd places of x      ▷ views, no copy
L2  for each step (kind, c) in order do                    ▷ σ = +1
L3      (src, dst) ← (s, d) if kind = P, else (d, s)
L4      for i ← 0 to h − 1 do
L5          t ← Σ_k c_k · src[(i + k) mod h]                ▷ the integer version rounds t
L6          dst[i] ← dst[i] + σ · t
L7  scale s by K_s and d by K_d; return (s, d)

LIFT-INVERSE(s, d, steps, K_s, K_d)
L8  scale s by 1/K_s and d by 1/K_d
L9  for each step (kind, c) in reverse order do
L10     run L3 to L6 with σ = −1
L11 interleave s and d into x; return x
```

Line L6 writes only `dst`, and line L5 reads only `src`, which no write of the same step changes. So the step can update `dst` in place in any order of $i$, and the inverse on line L10 sees the same `src` and subtracts the same values.

**The step lists used below.**

- Haar: P with $c_0 = -1$, then U with $c_0 = \tfrac12$. This gives $d = x[2i+1] - x[2i]$ and $s = \tfrac12(x[2i] + x[2i+1])$.
- LeGall 5/3: P with $c_0 = c_1 = -\tfrac12$, then U with $c_{-1} = c_0 = \tfrac14$. So $d[i] = x[2i+1] - \tfrac12(x[2i] + x[2i+2])$ and $s[i] = x[2i] + \tfrac14(d[i-1] + d[i])$.
- Daubechies 4: U with $c_0 = \sqrt 3$; P with $c_0 = -\tfrac{\sqrt 3}{4}$ and $c_{-1} = -\tfrac{\sqrt 3 - 2}{4}$; U with $c_1 = -1$; then $K_s = \tfrac{\sqrt 3 - 1}{\sqrt 2}$ and $K_d = \tfrac{\sqrt 3 + 1}{\sqrt 2}$. The result is the orthonormal four-tap transform. Its high-pass output is the usual one, negated and moved by one place.

## Example

Take $x = (4, 6, 10, 12, 8, 6, 5, 5)$ and the 5/3 steps. Then $s = (4, 10, 8, 5)$ and $d = (6, 12, 6, 5)$ before the steps.

| step | rule | result |
|---|---|---|
| P | $d[i] \leftarrow d[i] - \tfrac12(s[i] + s[i+1])$ | $d = (-1, 3, -\tfrac12, \tfrac12)$ |
| U | $s[i] \leftarrow s[i] + \tfrac14(d[i-1] + d[i])$ | $s = (\tfrac{31}{8}, \tfrac{21}{2}, \tfrac{69}{8}, 5)$ |

For example, $d[3] = 5 - \tfrac12(5 + 4) = \tfrac12$ uses the wrap $s[4] = s[0]$, and $s[0] = 4 + \tfrac14(d[3] + d[0]) = 4 - \tfrac18$. These are the outputs of the 5/3 filters in convolution form.

**The integer version.** Round half up inside each step, which is the reversible 5/3 transform of JPEG 2000:

$$d[i] \leftarrow d[i] - \Big\lfloor \tfrac{s[i] + s[i+1]}{2} \Big\rfloor, \qquad s[i] \leftarrow s[i] + \Big\lfloor \tfrac{d[i-1] + d[i] + 2}{4} \Big\rfloor.$$

The same input gives $d = (-1, 3, 0, 1)$ and $s = (4, 11, 9, 5)$, all integers. The inverse first computes $s[i] - \lfloor (d[i-1] + d[i] + 2)/4 \rfloor$, which gives back $(4, 10, 8, 5)$ from the stored $d$, and then adds $\lfloor (s[i] + s[i+1])/2 \rfloor$ to $d$, which gives back $(6, 12, 6, 5)$. The integer outputs differ from the exact ones by at most $\tfrac12$ in $d$ and $\tfrac34$ in $s$.

## Correctness

There are two claims. First, LIFT-INVERSE undoes LIFT-FORWARD for any step list, linear or not. A P step maps $(s, d)$ to $(s, d + F(s))$ for some function $F$, and $s$ is not changed. The inverse step computes $F(s)$ again from the same $s$ and subtracts it. A U step is the same with the halves swapped. The scaling is undone by the reciprocals, and the inverse runs the steps in reverse order, so each one meets the state that its forward step left. Rounding $F$ to integers does not change this argument, which is why the integer transform is exact.

Second, the steps compute the target filters. For the 5/3 list, put the P step into the U step:

$$s[i] = -\tfrac18 x[2i-2] + \tfrac14 x[2i-1] + \tfrac34 x[2i] + \tfrac14 x[2i+1] - \tfrac18 x[2i+2],$$

which is the 5/3 low-pass filter $\tilde h$, and $d[i]$ is the high-pass $\tilde g$ directly. In general, a product of triangular polyphase matrices is the polyphase matrix of the composed filters. The full proof is below. Daubechies and Sweldens (1998) prove the converse: every polyphase matrix with Laurent polynomial entries and determinant $1$ factors into lifting steps, by the Euclidean algorithm for Laurent polynomials, with a diagonal scaling when the determinant is another constant.

## Complexity

A step with $T_k$ taps does $T_k$ multiplications and $T_k$ additions for each of the $h = N/2$ indices, so one level costs $\tfrac N2 T$ multiplications for $T = \sum_k T_k$, plus $N$ for the scaling when it is not $1$. Over all levels of the multilevel transform, the block lengths sum to less than $2N$, so the time is $\Theta(TN)$, which is $\Theta(N)$ for a fixed step list. The algorithm writes into the input array and needs $\Theta(1)$ extra space, since each step reads a half that it does not write.

The gain over the convolution form, for each pair of outputs:

| filter pair | convolution | lifting |
|---|---|---|
| 5/3 | 8 multiplications, 6 additions | 4 multiplications, 4 additions |
| Daubechies 4 | 8 multiplications, 6 additions | 5 multiplications, 4 additions |

For the 5/3 pair, the two equal taps of each step can share one multiplication, which leaves 2. Daubechies and Sweldens (1998) show that for long filters, lifting needs about half the operations of the convolution form.

## Properties

- **Exact inverse by construction.** The inverse is the forward steps in reverse with the opposite sign. No matrix inverse or synthesis filter is needed.
- **In place.** Each step overwrites one half. The even and odd halves can stay interleaved in the input array.
- **Integer to integer.** With rounding in each step and no scaling, integers map to integers and back exactly (Calderbank, Daubechies, Sweldens and Yeo 1998). The integer transform is not linear.
- **Rounding error.** For the integer 5/3 transform, each rounded P value is within $\tfrac12$ of the exact one, so $|d - d_{\text{exact}}| \le \tfrac12$. The U step reads two $d$ values, each off by at most $\tfrac12$, so its exact sum is off by at most $\tfrac14(\tfrac12 + \tfrac12) = \tfrac14$, and its own rounding adds at most $\tfrac12$. So $|s - s_{\text{exact}}| \le \tfrac34$.
- **Mean kept.** For the 5/3 steps with the periodic extension, $\sum_i s[i] = \sum_i x[2i] + \tfrac12 \sum_i d[i] = \tfrac12 \sum_k x[k]$, because $\sum_i d[i] = \sum_i x[2i+1] - \sum_i x[2i]$. The update step is what keeps the mean.
- **Vanishing moments by steps.** The predict step sets the number of vanishing moments of the high-pass: the 5/3 predict is exact on lines, so lines give zero detail. The update step sets the moments that the low-pass keeps.

## Variants and improvements

- **Second-generation wavelets.** Sweldens (1998) uses the same split, predict and update steps on intervals, on irregular samples and on surfaces, where there is no translation or dilation. The predict step uses the local geometry, for example a polynomial fit through the nearby samples.
- **Longer predictors.** A predict step with the taps $-\tfrac1{16}, \tfrac9{16}, \tfrac9{16}, -\tfrac1{16}$ is exact on cubics, so the high-pass gets four vanishing moments.
- **The 9/7 pair.** The lossy JPEG 2000 filters factor into two predict steps, two update steps and a scaling.
- **Adaptive and nonlinear lifting.** The predictor can depend on the data, for example a median of neighbors or a choice of direction in an image. The inverse stays exact because it sees the same `src` values.
- **Symmetric extension.** For symmetric filters, replace the wrap by a mirror at the ends. Each step then reads a mirrored neighbor, and the inverse uses the same rule.

## When to use it

Use lifting whenever you compute a wavelet transform with known filters and care about speed, memory or exactness: in hardware and embedded encoders, in lossless image coding, and in JPEG 2000. Use the integer version when the decoder must give back the exact input. Use the second-generation form to build wavelets on data that is not a regular grid. The convolution form of the [discrete wavelet transform](/discrete-wavelet-transform/) is simpler to read and to check against a filter design, and it is a good reference implementation for tests.

## Pitfalls

- **Order of the inverse.** The inverse must run the steps in reverse order. Running them in forward order with the opposite sign gives a different map.
- **Rounding must match.** The decoder must use exactly the same rounding rule and offsets as the encoder. Round half up and round half to even give different, both reversible, transforms.
- **Scaling and integers.** The scaling constants of orthonormal filters are irrational. The integer version leaves them out, so it is not orthonormal and the coefficients of the halves have different weights.
- **Boundary rule.** The periodic wrap and the mirror give different coefficients near the ends. Both directions must use the same rule.
- **The factorization is not unique.** Different step lists give the same filters, with different rounding errors and different numerical stability.
- **Offsets of the taps.** A tap at the wrong offset still gives an exact inverse, but of a different transform. Test the lifted form against the convolution form.

## Implementations

## History

Sweldens (1996) introduced the lifting step as a way to change one biorthogonal filter pair into another with more vanishing moments, and Sweldens (1998) built second-generation wavelets from split, predict and update steps, with an in-place transform. Similar ladder structures had appeared in filter bank design. Daubechies and Sweldens (1998) proved that every finite two-channel filter bank with perfect reconstruction factors into lifting steps. Calderbank, Daubechies, Sweldens and Yeo (1998) showed that rounding inside the steps gives invertible integer wavelet transforms. JPEG 2000 adopted the lifted 5/3 transform for lossless coding.

## References
