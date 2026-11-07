---
tag: H8RGV6
kind: algorithm
slug: fast-wavelet-transform
name: Fast wavelet transform
aliases:
- Mallat's algorithm
- pyramid algorithm
- FWT
- periodic orthogonal wavelet transform
area: algebra/fast-transforms
level: core
summary: Computes the DWT in O(n) by repeatedly filtering and downsampling with a pair of filters.
model: real-ram
complexity:
  vars: {n: the input length, L: the filter length, J: the number of levels}
  time: {worst: Θ(L n), average: Θ(L n), best: Θ(L n)}
  space: {extra: Θ(n)}
  multiplications: {worst: 2 L n}
  additions: {worst: 2 (L - 1) n}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1989
  people: [Stéphane Mallat]
  note: Mallat (1989) showed that the coefficients of an orthonormal wavelet basis built from a multiresolution analysis are computed by a cascade of two filters and downsampling; Daubechies (1988) gave the compactly supported filters.
prereqs: [discrete-wavelet-transform, haar-wavelet-transform, convolution]
see_also: [filter-bank, lifting-scheme, jpeg-2000, subband-coding, laplacian-pyramid, haar-wavelet, orthogonal-transform, fast-fourier-transform]
sources:
  - paper: doi:10.1109/34.192463
    title: Stéphane G. Mallat, A theory for multiresolution signal decomposition, the wavelet representation, IEEE Transactions on Pattern Analysis and Machine Intelligence 11(7), 1989
    locator: pp. 674 to 693 (multiresolution analysis, the conjugate filters, and the pyramid algorithm for the decomposition and the reconstruction)
  - paper: doi:10.1002/cpa.3160410705
    title: Ingrid Daubechies, Orthonormal bases of compactly supported wavelets, Communications on Pure and Applied Mathematics 41(7), 1988
    locator: pp. 909 to 996 (the filters of length 2N with N vanishing moments, including the four-tap filter)
  - book: isbn:9780898712742
    title: Ingrid Daubechies, Ten Lectures on Wavelets, SIAM, 1992
    locator: Chapter 5 (multiresolution analysis and the filter conditions) and Chapter 6 (compactly supported orthonormal wavelets)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 27, Fast wavelet transforms (Section 27.1, Wavelet filters; 27.2, Implementation; 27.3, Moment conditions), and Chapter 24, The Haar transform
  - paper: doi:10.1007/BF02476026
    title: Ingrid Daubechies and Wim Sweldens, Factoring wavelet transforms into lifting steps, Journal of Fourier Analysis and Applications 4(3), 1998
    locator: pp. 247 to 269 (the lifting factorization of a two-channel filter bank, and its operation count)
  - paper: doi:10.1109/TCOM.1983.1095851
    title: Peter J. Burt and Edward H. Adelson, The Laplacian pyramid as a compact image code, IEEE Transactions on Communications 31(4), 1983
    locator: pp. 532 to 540 (the image pyramid built by repeated filtering and downsampling, the precursor of the name pyramid algorithm)
---

The fast wavelet transform computes the coefficients of a vector in an orthonormal wavelet basis by a cascade of filters. One level splits a vector of length $m$ into $m/2$ smooth (approximation) coefficients, given by a low-pass filter $h$ followed by keeping every second output, and $m/2$ detail coefficients, given in the same way by the high-pass filter $g_l = (-1)^l h_{L-1-l}$. The next level repeats this on the smooth half only. Because each level works on half as much data as the one before, $J$ levels on $n$ inputs cost less than twice the first level, $\Theta(L n)$ for a filter of length $L$, which is $O(n)$ for a fixed wavelet and faster than the [FFT](/fast-fourier-transform/). The inverse runs the same filters transposed, from the coarsest level up, and recovers the input exactly in exact arithmetic. This is Mallat's (1989) algorithm, and it is how the [discrete wavelet transform](/discrete-wavelet-transform/) is computed in practice, for example in [JPEG 2000](/jpeg-2000/).

## In plain words

The method looks at a signal at several scales. At the first step it walks along the signal in steps of two and computes, at each step, a local average and a local difference of a few neighbouring values. The averages form a half-length blurred copy of the signal, and the differences record what the blur lost. The next step does the same to the blurred copy, and so on.

Each step handles half as much data as the one before, so all the steps together take about twice as long as the first, which is linear in the length. Running the steps backwards puts the averages and differences together again and gives back the signal exactly. For smooth stretches of the signal most differences are tiny, which is what makes wavelets useful for compression and noise removal.

## The problem

**Notation.** $n$ is the input length; for $J$ levels it must be divisible by $2^J$, and it is a power of two when the transform runs down to a single coefficient. The filter $h = (h_0, \ldots, h_{L-1})$ has even length $L$ and is *orthonormal*: $\sum_l h_l h_{l+2s} = 1$ for $s = 0$ and $0$ for $s \ne 0$. The high-pass filter is $g_l = (-1)^l h_{L-1-l}$. Indices into a block of length $m$ are taken modulo $m$ (periodic boundary). Unlike the Fourier pages of this section no roots of unity are involved, but the filters are often described by their frequency responses $H(\omega) = \sum_l h_l e^{-i l \omega}$, with the same sign convention as $\omega_n = e^{-2\pi i/n}$ on the [DFT page](/discrete-fourier-transform/).

**Input.** A real vector $x$ of length $n$, an orthonormal filter $h$, and a number of levels $J$.

**Output.** The vector $y = (a^{(J)}, d^{(J)}, d^{(J-1)}, \ldots, d^{(1)})$, where $a^{(0)} = x$ and, for a block $a = a^{(\ell-1)}$ of length $m = n/2^{\ell-1}$,

$$a^{(\ell)}_i = \sum_{l=0}^{L-1} h_l \, a_{(2i + l) \bmod m}, \qquad d^{(\ell)}_i = \sum_{l=0}^{L-1} g_l \, a_{(2i + l) \bmod m}, \qquad 0 \le i < m/2.$$

These are the coefficients of $x$ in the periodized orthonormal wavelet basis, so the map $x \mapsto y$ is an orthogonal matrix.

**Cost model.** Real multiplications and additions, counted separately, in the real RAM. In floating point the error is analysed below.

## The algorithm

```pseudo id=main
FWT(x, h, J)            ▷ |x| = n divisible by 2^J; h orthonormal of even length L
L1  n ← |x|; L ← |h|
L2  g[l] ← (−1)^l · h[L − 1 − l] for l = 0, …, L − 1
L3  a ← x; m ← n
L4  for level ← 1 to J do
L5      for i ← 0 to m/2 − 1 do
L6          s[i] ← Σ_l h[l] · a[(2i + l) mod m]       ▷ low-pass and downsample
L7          d[i] ← Σ_l g[l] · a[(2i + l) mod m]       ▷ high-pass and downsample
L8      y[m/2 .. m − 1] ← d; a ← s; m ← m/2
L9  y[0 .. m − 1] ← a
L10 return y

INVERSE-FWT(y, h, J)    ▷ returns x with FWT(x, h, J) = y
L11 m ← n / 2^J; a ← y[0 .. m − 1]
L12 for level ← 1 to J do
L13     b ← zero vector of length 2m
L14     for i ← 0 to m − 1, l ← 0 to L − 1 do b[(2i + l) mod 2m] ← b[(2i + l) mod 2m] + h[l] · a[i] + g[l] · y[m + i]
L15     a ← b; m ← 2m
L16 return a
```

Line L8 stores the details of the current level at the end of the current block, so the details of the finest level end up at the end of $y$ and the final smooth block at the front. Line L14 is the transpose of lines L6 and L7: each coefficient adds back its filter, shifted by $2i$, into the finer level. With $J = 0$ both procedures return their input.

## Example

**Haar, $J = 3$.** With $h = (\frac{1}{\sqrt 2}, \frac{1}{\sqrt 2})$ and $g = (\frac{1}{\sqrt 2}, -\frac{1}{\sqrt 2})$, transform $x = (4, 6, 10, 12, 8, 6, 5, 5)$.

| level | smooth $a^{(\ell)}$ | detail $d^{(\ell)}$ |
|---|---|---|
| 1 | $(10, 22, 14, 10)/\sqrt 2$ | $(-2, -2, 2, 0)/\sqrt 2$ |
| 2 | $(32, 24)/2 = (16, 12)$ | $(-12, 4)/2 = (-6, 2)$ |
| 3 | $28/\sqrt 2 = 14\sqrt 2$ | $4/\sqrt 2 = 2\sqrt 2$ |

So $y = (14\sqrt 2, 2\sqrt 2, -6, 2, -\sqrt 2, -\sqrt 2, \sqrt 2, 0)$. The energy is kept: $\sum x_j^2 = 446 = 392 + 8 + 36 + 4 + 2 + 2 + 2 + 0$. The inverse of lines L11 to L16 rebuilds $(16, 12)$, then $(10, 22, 14, 10)/\sqrt 2$, then $x$.

**Daubechies-4, one level.** With $h = \frac{1}{4\sqrt 2}(1 + \sqrt 3, 3 + \sqrt 3, 3 - \sqrt 3, 1 - \sqrt 3) \approx (0.4830, 0.8365, 0.2241, -0.1294)$, the filter $g$ has two vanishing moments: $\sum_l g_l = \sum_l l \, g_l = 0$. So on the linear input $x = (0, 1, \ldots, 7)$ the details $d_0, d_1, d_2$ are $0$, and only $d_3 = -2\sqrt 2 \approx -2.8284$, whose filter wraps around from $x_7 = 7$ to $x_0 = 0$, is not. Both examples were checked by script.

## Correctness

The one-level map $a \mapsto (s, d)$ is a matrix $W_m$ whose rows are the filters $h$ and $g$, shifted by even amounts and wrapped modulo $m$. The orthonormality of $h$ and the choice of $g$ give $\sum_l h_l g_{l + 2s} = 0$ and $\sum_l g_l g_{l+2s} = \sum_l h_l h_{l+2s}$ for every $s$, and wrapping modulo an even $m$ only adds terms with even shifts, so the rows of $W_m$ are orthonormal. Hence $W_m$ is orthogonal, $W_m^{-1} = W_m^{\mathsf T}$, and line L14 computes exactly $W_m^{\mathsf T}$ applied to $(a, d)$. The whole transform is a product of the orthogonal maps $W_m \oplus I$ for $m = n, n/2, \ldots$, so it is orthogonal, and the inverse undoes the levels in reverse order. The full proof is below.

## Complexity

**Operations.** A level on a block of length $m$ computes $m/2$ outputs of each filter, which is $L m$ multiplications and $(L - 1) m$ additions. Summed over the levels $m = n, n/2, \ldots, n/2^{J-1}$, that is $L n (2 - 2^{1-J}) < 2 L n$ multiplications and less than $2(L - 1) n$ additions. The inverse has the same counts, with $2L$ additions per coefficient pair because it accumulates. For the Haar filter the factor $\frac{1}{\sqrt 2}$ can be applied once per pair, giving $n$ multiplications per level; the [Haar transform](/haar-wavelet-transform/) page counts this case.

**Time and space.** $\Theta(L n)$ for any number of levels, which is $\Theta(n)$ for a fixed filter. The extra space is $\Theta(n)$ for the buffers $s$, $d$ and $y$; the transform can be done in place with an interleaved output order.

**Lower bound.** Every output depends on the input, and the transform is invertible, so $\Omega(n)$ operations are needed; the algorithm is optimal up to the factor $L$.

**Rounding errors (proved).** Let the stored filter satisfy $|\hat h_l - h_l| \le \mu |h_l|$, and let $u$ be the unit roundoff, $\gamma_L = L u/(1 - L u)$. Each computed coefficient of a level is a dot product of length $L$, and the computed transform satisfies

$$\lVert \hat y - y \rVert_2 \le J \sqrt L \, (\gamma_L + \mu) \, \lVert x \rVert_2 + O(u^2),$$

and $\lVert y \rVert_2 = \lVert x \rVert_2$, so this is a relative bound. It grows only linearly in the number of levels, $J \le \lg n$. The inverse satisfies the same bound. As usual, observed errors on random data are much smaller than this worst-case bound.

## Properties

- **Orthogonal.** $\lVert y \rVert_2 = \lVert x \rVert_2$, and the inverse is the transpose (perfect reconstruction).
- **Linear time.** Faster than the FFT, because the levels shrink geometrically.
- **Local.** A coefficient at level $\ell$ depends on about $L 2^\ell$ neighbouring inputs, so an edge or spike affects few coefficients per level.
- **Vanishing moments.** If $g$ has $p$ vanishing moments ($\sum_l l^r g_l = 0$ for $r < p$), the details of polynomial data of degree below $p$ are zero away from the wrap-around. The Haar filter has $p = 1$; Daubechies' filters of length $2p$ have $p$, the most possible for that length.
- **Non-recursive.** The levels form a simple loop, with no recursion.

## Variants and improvements

- **Lifting.** Daubechies and Sweldens (1998) factor the two filters into a sequence of [lifting steps](/lifting-scheme/), which roughly halves the operation count, works in place, and gives integer-to-integer wavelet transforms by rounding inside each step. JPEG 2000 uses the lifting form of the 5/3 and 9/7 filters.
- **Biorthogonal filters.** Analysis and synthesis filters may differ; then the transform is invertible but not orthogonal, and symmetric filters become possible. The 9/7 filter of JPEG 2000 is biorthogonal.
- **Boundary handling.** Instead of the periodic wrap, symmetric extension (as in the [DCT](/fast-dct/)) or special boundary wavelets avoid the artificial jump at the ends.
- **Stationary (undecimated) transform.** Skipping the downsampling gives a shift-invariant but redundant transform, $O(n \log n)$ in total.
- **Wavelet packets.** Splitting the detail halves as well gives a full tree of $O(n \log n)$ coefficients from which a best basis is chosen.
- **Two dimensions.** Apply one level along the rows and then along the columns, giving four subbands, and recurse on the smooth one.

## When to use it

Use the fast wavelet transform for image compression ([JPEG 2000](/jpeg-2000/)), for denoising by shrinking small detail coefficients, for multiresolution analysis of signals with local features such as edges and transients, and for fast operator compression in numerical analysis. For stationary signals whose content is best described by frequency, the [FFT](/fast-fourier-transform/) and the DCT are the better tools.

## Pitfalls

- **Length.** Each level needs an even block length; $J$ levels need $2^J \mid n$.
- **Filter conventions.** Some texts index $h$ in reverse, use $g_l = (-1)^{l+1} h_{L-1-l}$, or normalize with $\sum h_l = 1$ instead of $\sqrt 2$. All work, but the analysis and synthesis must use the same convention or reconstruction fails.
- **Boundary artifacts.** The periodic wrap treats the two ends as neighbours, so a signal with different end values gets large details near the ends, as $d_3$ in the example.
- **Output layout.** Libraries order the coefficient blocks differently (coarsest first, finest first, or interleaved); check before comparing.
- **Shift variance.** A shift of the input by one sample can change the coefficients a lot; use the undecimated transform where this matters.

## Implementations

## History

Filtering followed by downsampling was used before wavelets in subband coding and in the Laplacian pyramid of Burt and Adelson (1983), which gave the method its name of pyramid algorithm. Daubechies (1988) constructed orthonormal bases of compactly supported wavelets, with the finite filters such as the four-tap filter of the example. Mallat (1989) showed that a multiresolution analysis leads to a pair of conjugate filters, and that the wavelet coefficients of a signal are computed by the cascade on this page, with the transposed cascade for the reconstruction. Daubechies and Sweldens (1998) showed that every such two-channel filter bank factors into lifting steps.

## References
