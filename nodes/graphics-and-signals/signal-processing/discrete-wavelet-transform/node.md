---
tag: CM5P8S
kind: algorithm
slug: discrete-wavelet-transform
name: Discrete wavelet transform
aliases:
- DWT
- multiresolution analysis
area: graphics-and-signals/signal-processing
level: core
summary: Multiresolution decomposition by iterated low-pass and high-pass filtering with decimation.
solves: [time-frequency-analysis]
model: real-ram
complexity:
  vars: {N: the signal length, J: the number of levels, M: "the total number of analysis taps, the length of the low-pass filter plus the length of the high-pass filter"}
  time: {worst: Θ(M N), average: Θ(M N), best: Θ(M N)}
  space: {extra: Θ(N)}
properties: {deterministic: true, recursive: false, in_place: false, exact: true}
history:
  year: 1989
  people: [Stéphane Mallat, Ingrid Daubechies, Albert Cohen, Jean-Christophe Feauveau]
  note: Mallat (1989) computed wavelet coefficients by a cascade of two filters with downsampling. Daubechies (1988) gave finite orthonormal filters, and Cohen, Daubechies and Feauveau (1992) the biorthogonal ones.
prereqs: [haar-wavelet-transform, filter-bank, perfect-reconstruction]
see_also: [fast-wavelet-transform, haar-wavelet, lifting-scheme, continuous-wavelet-transform, jpeg-2000, spiht, subband-coding, signal-denoising]
sources:
  - paper: doi:10.1109/34.192463
    title: Stéphane G. Mallat, A theory for multiresolution signal decomposition, the wavelet representation, IEEE Transactions on Pattern Analysis and Machine Intelligence 11(7), 1989
    locator: pages 674 to 693 (the decomposition by a low-pass and a high-pass filter with downsampling, and the reconstruction)
  - paper: doi:10.1002/cpa.3160450502
    title: Albert Cohen, Ingrid Daubechies and Jean-Christophe Feauveau, Biorthogonal bases of compactly supported wavelets, Communications on Pure and Applied Mathematics 45(5), 1992
    locator: pages 485 to 560 (analysis and synthesis filters that differ, the biorthogonality conditions, and symmetric compactly supported filters)
  - paper: doi:10.1002/cpa.3160410705
    title: Ingrid Daubechies, Orthonormal bases of compactly supported wavelets, Communications on Pure and Applied Mathematics 41(7), 1988
    locator: pages 909 to 996 (finite orthonormal filters with a given number of vanishing moments)
  - book: isbn:9780123743701
    title: Stéphane Mallat, A Wavelet Tour of Signal Processing, The Sparse Way, third edition, Academic Press, 2009
    locator: Chapter 7 (wavelet bases, filter banks, biorthogonal wavelets and boundary handling)
  - book: isbn:9780961408879
    title: Gilbert Strang and Truong Nguyen, Wavelets and Filter Banks, Wellesley-Cambridge Press, 1996
    locator: the chapters on two-channel perfect reconstruction filter banks and biorthogonal filters
---

The discrete wavelet transform (DWT) of a signal of length $N$ splits it, at each of $J$ levels, into a half-length approximation (a low-pass filter followed by keeping every second output) and a half-length detail (a high-pass filter, then the same downsampling), and then repeats the split on the approximation only. The result has exactly $N$ coefficients, and a second pair of *synthesis* filters rebuilds the signal exactly when the four filters satisfy the biorthogonality conditions of a [perfect reconstruction](/perfect-reconstruction/) [filter bank](/filter-bank/). It costs $\Theta(MN)$ time for $M$ analysis taps, for any number of levels. This page treats the general two-channel transform, with analysis and synthesis filters that may differ, and uses the 5/3 filters of [JPEG 2000](/jpeg-2000/) as the running example; the orthonormal periodic case, its operation count and its rounding bound are on the [fast wavelet transform](/fast-wavelet-transform/) page, and the Haar case is on the [Haar wavelet transform](/haar-wavelet-transform/) page.

## In plain words

Take a list of numbers and walk along it in steps of two. At each step, write down a smoothed value of the numbers near you, and a second value that measures how far the numbers there are from a smooth line. You get two lists, each half as long as the input. The first is a blurred, shorter copy of the signal. The second holds the detail that the blur lost, and it is close to zero wherever the signal is smooth.

Now do the same to the blurred copy, and again. Each round works on half as much data, so the whole job costs about twice the first round. A matching set of rebuild rules runs the rounds backwards and gives back the input exactly. Smooth parts give tiny details, so most of the output is close to zero, which is why compression and noise removal use it.

## The problem

**Signals.** A discrete signal $x[0], \ldots, x[N-1]$ of real (or rational) numbers. For $J$ levels, $2^J$ must divide $N$. Indices of a block of length $m$ are taken modulo $m$, which is the periodic extension; the variants below replace it.

**Filters.** Four finite filters, each a map from integer tap positions to numbers: the analysis low-pass $\tilde h$ and high-pass $\tilde g$, and the synthesis low-pass $h$ and high-pass $g$. Taps may have negative positions, so a symmetric filter can be centered at $0$. Frequencies are in radians per sample, $\omega \in [-\pi, \pi]$, and the frequency response of $\tilde h$ is $\tilde H(\omega) = \sum_l \tilde h[l] e^{-i\omega l}$.

**Biorthogonality.** The four filters must satisfy, for every integer $k$,

$$\sum_l \tilde h[l]\, h[l - 2k] = \sum_l \tilde g[l]\, g[l - 2k] = \delta_{k,0}, \qquad \sum_l \tilde h[l]\, g[l - 2k] = \sum_l \tilde g[l]\, h[l - 2k] = 0.$$

In the orthonormal case $h = \tilde h$ and $g = \tilde g$, and these are the conditions of the fast wavelet transform page.

**Output.** With $a^{(0)} = x$ and $a = a^{(j-1)}$ of length $m = N/2^{j-1}$, level $j$ computes

$$a^{(j)}[i] = \sum_l \tilde h[l]\, a[(2i + l) \bmod m], \qquad d^{(j)}[i] = \sum_l \tilde g[l]\, a[(2i + l) \bmod m], \qquad 0 \le i < m/2.$$

The output is $a^{(J)}$ and $d^{(1)}, \ldots, d^{(J)}$, with $N/2^J + \sum_j N/2^j = N$ numbers in total.

**Cost model.** The [real RAM](/real-ram/): each addition and multiplication of reals costs one step. With rational filters and a rational signal, as for the 5/3 pair, every operation is exact.

## The algorithm

```pseudo id=main
DWT(x, h̃, g̃, J)                      ▷ N = |x| is divisible by 2^J
L1  a ← x
L2  for j ← 1 to J do
L3      (a, d) ← ANALYSIS(a, h̃, g̃)
L4      d⁽ʲ⁾ ← d
L5  return (a, d⁽¹⁾, …, d⁽ᴶ⁾)

ANALYSIS(a, h̃, g̃)                    ▷ m = |a| is even
L6  for i ← 0 to m/2 − 1 do
L7      s[i] ← Σ_l h̃[l] · a[(2i + l) mod m]
L8      d[i] ← Σ_l g̃[l] · a[(2i + l) mod m]
L9  return (s, d)

IDWT(a, d⁽¹⁾, …, d⁽ᴶ⁾, h, g)
L10 for j ← J downto 1 do
L11     a ← SYNTHESIS(a, d⁽ʲ⁾, h, g)
L12 return a

SYNTHESIS(s, d, h, g)                 ▷ the output has length m = 2|s|
L13 b ← the zero vector of length m
L14 for i ← 0 to m/2 − 1 do
L15     for each tap l: add h[l] · s[i] and g[l] · d[i] to b[(2i + l) mod m]
L16 return b
```

ANALYSIS is a correlation with each filter, evaluated only at even shifts. SYNTHESIS is the reverse: it puts each coefficient back at position $2i$, spreads it by the synthesis filter, and adds the two channels. A tap that one filter does not have counts as $0$ on line L15. IDWT undoes the levels in reverse order, coarsest first.

**The 5/3 filters.** The pair used in the example is

$$\tilde h = \big(-\tfrac18, \tfrac14, \tfrac34, \tfrac14, -\tfrac18\big) \text{ at } l = -2, \ldots, 2, \qquad \tilde g = \big(-\tfrac12, 1, -\tfrac12\big) \text{ at } l = 0, 1, 2,$$

$$h = \big(\tfrac12, 1, \tfrac12\big) \text{ at } l = -1, 0, 1, \qquad g = \big(-\tfrac18, -\tfrac14, \tfrac34, -\tfrac14, -\tfrac18\big) \text{ at } l = -1, \ldots, 3.$$

All four are symmetric about their centers, which no orthonormal filter longer than two taps can be. $\tilde H(0) = 1$ and $\tilde H(\pi) = 0$, so $\tilde h$ is low-pass; $\tilde g$ is a second difference centered on the odd sample, so $\tilde G(0) = 0$.

## Example

Transform the ramp $x = (1, 2, 3, 4, 5, 6, 7, 8)$, so $N = 8$, with the 5/3 filters and $J = 3$.

| level $j$ | input $a^{(j-1)}$ | approximation $a^{(j)}$ | detail $d^{(j)}$ |
|---|---|---|---|
| 1 | $(1, 2, 3, 4, 5, 6, 7, 8)$ | $(2, 3, 5, 8)$ | $(0, 0, 0, 4)$ |
| 2 | $(2, 3, 5, 8)$ | $(3, 6)$ | $(-\tfrac12, \tfrac92)$ |
| 3 | $(3, 6)$ | $(\tfrac92)$ | $(3)$ |

At level 1, $d[i] = x[2i+1] - \tfrac12(x[2i] + x[2i+2])$ is zero wherever the three samples lie on a line. Only $d[3] = 8 - \tfrac12(7 + 1) = 4$ is not, because the periodic wrap puts $x[0] = 1$ after $x[7] = 8$. The interior approximations $a^{(1)}[1] = 3$ and $a^{(1)}[2] = 5$ equal the even samples $x[2]$ and $x[4]$, since $\tilde h$ reproduces a line. The wrap also changes $a^{(1)}[0]$ and $a^{(1)}[3]$. The last coefficient $\tfrac92$ is the mean of $x$. SYNTHESIS on $(\tfrac92)$ and $(3)$ gives $(3, 6)$ back, and two more levels give $x$.

For comparison, the Haar filters in the averaging scale, $\tilde h = (\tfrac12, \tfrac12)$ and $\tilde g = (\tfrac12, -\tfrac12)$ at $l = 0, 1$, give the details $(-\tfrac12, -\tfrac12, -\tfrac12, -\tfrac12)$, $(-1, -1)$ and $(-2)$, and the same final mean $\tfrac92$. The Haar high-pass has one vanishing moment, so a line gives constant, nonzero details at every level. The 5/3 high-pass has two, so the interior details vanish.

## Correctness

One level of ANALYSIS is a matrix $\tilde A_m$ with $m$ rows: row $i$ holds $\tilde h$ shifted by $2i$, and row $m/2 + i$ holds $\tilde g$ shifted by $2i$, both wrapped modulo $m$. SYNTHESIS is a matrix $S_m$ whose columns are $h$ and $g$ shifted by $2i$ in the same way. The entry of $\tilde A_m S_m$ for an $\tilde h$ row $i$ and an $h$ column $i'$ is the sum of $\sum_l \tilde h[l] h[l - 2k]$ over all $k \equiv i - i' \pmod{m/2}$, and by biorthogonality this sum is $1$ if $i = i'$ and $0$ otherwise. The other three blocks work the same way, so $\tilde A_m S_m = I$. Both matrices are square, so $S_m \tilde A_m = I$ as well: SYNTHESIS inverts ANALYSIS for every even $m$, even $m = 2$. IDWT applies these inverses in the reverse order of DWT. The full proof is below.

## Complexity

A level on a block of length $m$ computes $m/2$ outputs of each analysis filter, so it does $\tfrac m2 M$ multiplications and fewer additions, where $M = |\tilde h| + |\tilde g|$. The block lengths are $N, N/2, \ldots, N/2^{J-1}$, which sum to less than $2N$, so the transform does fewer than $MN$ multiplications for every $J$. For the 5/3 pair, $M = 8$. The inverse costs the same with the synthesis lengths. The time is $\Theta(MN)$, which is $\Theta(N)$ for a fixed filter pair, and the extra space is $\Theta(N)$. The [lifting scheme](/lifting-scheme/) computes the same coefficients with fewer operations: for long filters, about half as many.

## Properties

- **Critically sampled.** $N$ inputs give $N$ coefficients. There is no redundancy, unlike the [continuous wavelet transform](/continuous-wavelet-transform/) or the [Laplacian pyramid](/laplacian-pyramid/), which stores about $\tfrac43 N$ numbers for an image.
- **Invertible but not orthogonal.** For the 5/3 pair, $\tilde A_m^{-1} = S_m \ne \tilde A_m^{\mathsf T}$. The ramp has energy $\sum x[k]^2 = 204$, and its coefficients have $\tfrac{81}{4} + 9 + \tfrac14 + \tfrac{81}{4} + 16 = \tfrac{263}{4}$. Only orthonormal filters keep the energy.
- **Mean kept.** The even taps of $\tilde h$ sum to $-\tfrac18 + \tfrac34 - \tfrac18 = \tfrac12$, and the odd taps to $\tfrac14 + \tfrac14 = \tfrac12$. So $\sum_i a^{(j)}[i] = \tfrac12 \sum_i a^{(j-1)}[i]$, and when $N = 2^J$ the last coefficient is the mean of $x$.
- **Vanishing moments.** $\sum_l \tilde g[l] = 0$ and $\sum_l l\, \tilde g[l] = 0$, but $\sum_l l^2 \tilde g[l] = -1$. So the details of any line are zero away from the wrap, and those of a parabola are not.
- **Local.** A coefficient at level $j$ depends on a window of input samples whose length grows like $2^j$. An edge changes only a few coefficients per level, and the [energy compaction](/energy-compaction/) of the transform comes from this.
- **Shift variant.** The downsampling makes the coefficients depend on the alignment of the signal with the even positions (see the pitfalls).

## Variants and improvements

- **Orthonormal filters.** With $h = \tilde h$ and $g = \tilde g$ (the Daubechies filters), the transform is orthogonal and the inverse is the transpose. The [fast wavelet transform](/fast-wavelet-transform/) page treats this case.
- **Symmetric extension.** For symmetric filters such as 5/3 and 9/7, extend the signal by mirror symmetry, $x[-k] = x[k]$ and $x[N - 1 + k] = x[N - 1 - k]$, instead of wrapping. The extended signal has no jump at the ends. For the ramp, the boundary detail becomes $8 - \tfrac12(7 + 7) = 1$, which measures only the kink of the mirror, instead of $4$.
- **Integer transform.** Rounding inside the lifting steps of the 5/3 pair gives an integer-to-integer transform that inverts exactly. JPEG 2000 uses it for lossless coding and the 9/7 pair for lossy coding.
- **Two dimensions.** Apply one level to each row, then to each column. This gives four subbands, and the next level splits the low-low band. [SPIHT](/spiht/) and JPEG 2000 code these subbands.
- **Undecimated transform.** Skip the downsampling and spread the filters instead. The result is shift invariant but has $(J+1)N$ coefficients.
- **Wavelet packets.** Split the detail bands too, and choose the best tree for the signal.

## When to use it

Use the DWT when the signal is smooth in most places and has a few local events: edges in images, transients in audio, and spikes in sensor data. It is the transform of JPEG 2000 and the base of wavelet [signal denoising](/signal-denoising/), where small detail coefficients are set to zero. Choose biorthogonal symmetric filters (5/3, 9/7) for images, because symmetric extension avoids boundary artifacts and the linear phase avoids shifted edges. Choose orthonormal filters when energy must be kept, for example when the noise must stay white in the coefficient domain. For a signal that is a sum of steady tones, the Fourier transform describes it better.

## Pitfalls

- **Shift variance.** With the Haar averaging filters, $(1, 1, 1, 1, 0, 0, 0, 0)$ has the level 1 details $(0, 0, 0, 0)$, but its shift by one sample, $(0, 1, 1, 1, 1, 0, 0, 0)$, has $(-\tfrac12, 0, \tfrac12, 0)$. Do not compare coefficients of signals that are not aligned.
- **Mismatched filters.** The synthesis filters must match the analysis filters in scale and in the position of their taps. Moving $g$ by one sample, or using the $\sqrt 2$ scale on one side and the averaging scale on the other, breaks perfect reconstruction.
- **The wrong boundary rule.** Periodic extension makes large details at the ends of a signal whose ends differ, like $d[3] = 4$ in the example. The decoder must use the same rule as the encoder.
- **Length.** Each level needs an even length, so $J$ levels need $2^J \mid N$. Pad or use a boundary rule that handles odd lengths.
- **Energy.** With biorthogonal filters, the squared error in the coefficients is not the squared error in the signal. Thresholds and quantizer steps tuned for an orthonormal transform need a weight per level.

## Implementations

## History

Filtering with downsampling came first in [subband coding](/subband-coding/) and in the image pyramid of Burt and Adelson. Daubechies (1988) built orthonormal bases of compactly supported wavelets, whose coefficients are given by finite filters. Mallat (1989) showed that the wavelet coefficients of a signal are computed by the cascade of a low-pass and a high-pass filter with downsampling, and the signal rebuilt by the reverse cascade. Cohen, Daubechies and Feauveau (1992) let the synthesis filters differ from the analysis filters, which allows short symmetric filters such as the 5/3 pair.

## References
