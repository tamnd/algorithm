---
tag: KGXG3C
kind: algorithm
slug: nonuniform-fft
name: Nonuniform FFT
aliases:
- NUFFT
- type-1 and type-2 NUFFT
- nonequispaced FFT
- NFFT
- gridding algorithm
area: algebra/fast-transforms
level: advanced
summary: Approximates the NUDFT in near-linear time by gridding, convolving and running an FFT.
solves: [nonuniform-discrete-fourier-transform]
model: real-ram
complexity:
  vars: {n: the number of frequencies, m: the number of points, ε: the target precision (at most 1/2)}
  time: {worst: O(n log n + m log(1/ε) + log(1/ε) log log(1/ε))}
  space: {extra: O(n + log(1/ε))}
  additions: {worst: O(n log n + m log(1/ε) + log(1/ε) log log(1/ε))}
  multiplications: {worst: O(n log n + m log(1/ε) + log(1/ε) log log(1/ε))}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1993
  people: [A. Dutt, V. Rokhlin]
  note: Dutt and Rokhlin (1993) gave the first algorithms for Fourier transforms of nonequispaced data with a proved error to any precision, using Gaussian kernels; Beylkin (1995) used B-splines. Greengard and Lee (2004) accelerated Gaussian gridding, and Barnett, Magland and af Klinteberg (2019) introduced the exponential of semicircle kernel in the FINUFFT library.
prereqs: [nonuniform-discrete-fourier-transform, fast-fourier-transform, convolution-theorem]
see_also: [iterative-fft, multidimensional-fft, bluestein-fft, sparse-fourier-transform, trigonometric-interpolation, fast-multipoint-evaluation, least-squares-problem, parseval-theorem]
sources:
  - paper: doi:10.1137/0914081
    title: A. Dutt and V. Rokhlin, Fast Fourier transforms for nonequispaced data, SIAM Journal on Scientific Computing 14(6), 1993
    locator: pp. 1368 to 1393 (Gaussian spreading onto an oversampled grid and its error analysis)
  - paper: doi:10.1006/acha.1995.1026
    title: G. Beylkin, On the fast Fourier transform of functions with singularities, Applied and Computational Harmonic Analysis 2(4), 1995
    locator: pp. 363 to 381 (the same scheme with B-spline kernels)
  - paper: doi:10.1137/S003614450343200X
    title: Leslie Greengard and June-Yub Lee, Accelerating the nonuniform fast Fourier transform, SIAM Review 46(3), 2004
    locator: pp. 443 to 454 (the Gaussian type 1 and type 2 algorithm, the choice of τ and fast Gaussian gridding)
  - paper: doi:10.1137/18M120885X
    title: Alexander H. Barnett, Jeremy Magland and Ludvig af Klinteberg, A parallel nonuniform fast Fourier transform library based on an exponential of semicircle kernel, SIAM Journal on Scientific Computing 41(5), 2019
    locator: pp. C479 to C504
  - paper: doi:10.1109/TSP.2002.807005
    title: Jeffrey A. Fessler and Bradley P. Sutton, Nonuniform fast Fourier transforms using min-max interpolation, IEEE Transactions on Signal Processing 51(2), 2003
    locator: pp. 560 to 574
  - paper: doi:10.1145/1555386.1555388
    title: Jens Keiner, Stefan Kunis and Daniel Potts, Using NFFT 3, a software library for various nonequispaced fast Fourier transforms, ACM Transactions on Mathematical Software 36(4), 2009
    locator: Article 19
  - paper: doi:10.1016/j.jcp.2004.12.004
    title: June-Yub Lee and Leslie Greengard, The type 3 nonuniform FFT and its applications, Journal of Computational Physics 206(1), 2005
    locator: pp. 1 to 5
  - paper: doi:10.1137/17M1134822
    title: Diego Ruiz-Antolín and Alex Townsend, A nonuniform fast Fourier transform based on low rank approximation, SIAM Journal on Scientific Computing 40(1), 2018
    locator: pp. A529 to A547
  - paper: doi:10.1086/167197
    title: William H. Press and George B. Rybicki, Fast algorithm for spectral analysis of unevenly sampled data, The Astrophysical Journal 338, 1989
    locator: from p. 277 (extirpolation onto a grid and an FFT)
  - book: isbn:9783030043056
    title: Gerlind Plonka, Daniel Potts, Gabriele Steidl and Manfred Tasche, Numerical Fourier Analysis, Birkhäuser, 2018
    locator: Chapter 7, Fast Fourier Transforms for Nonequispaced Data
---

The nonuniform FFT (NUFFT) computes the [nonuniform discrete Fourier transform](/nonuniform-discrete-fourier-transform/) to a chosen precision $\varepsilon$ in nearly linear time. For type 1, it spreads each value $c_j$ at its point $t_j$ onto a regular grid that is finer than needed (oversampled) by convolving with a narrow smooth kernel, takes an ordinary [FFT](/fast-fourier-transform/) of the grid, and divides each Fourier coefficient by the Fourier transform of the kernel to undo the smoothing. Type 2 runs the same three steps transposed and in reverse order. With a Gaussian kernel truncated to $2M$ grid points, $M = O(\log(1/\varepsilon))$, the error is at most $\varepsilon$ times the $1$-norm of the input, which this page proves, and the cost is an FFT of length $O(n)$ plus $O(m \log(1/\varepsilon))$ work for $m$ points, against $mn$ for the direct sum.

## In plain words

Scattered samples cannot be fed to an ordinary fast Fourier transform, which needs a regular grid. The trick is to smear each sample into a small blob, shaped like a bell curve, and add the blobs up on a fine regular grid. The grid now holds a blurred copy of the data, and a regular fast transform handles it. Blurring has a simple effect on the frequencies: each one is weakened by a known factor, so dividing by that factor undoes the blur. Blobs that are narrow on the grid but smooth enough give an answer that is accurate to many digits. Running the steps backwards evaluates a frequency list at scattered places.

## The problem

**Notation.** As on all pages of fast transforms, $\omega_n = e^{-2\pi i/n}$, the sign of signal processing, FFTW and NumPy (CLRS uses the other sign), and the DFT is $X_k = \sum_{j=0}^{n-1} x_j \omega_n^{jk}$ with inverse factor $1/n$. Here $n$ is the number of frequencies and need not be a power of two; the inner FFT has a power-of-two length $N$. Write $e(t) = e^{-2\pi i t}$, so $\omega_n^{jk} = e(jk/n)$.

**Input.** Points $t_0, \ldots, t_{m-1} \in \mathbb{R}$ (used modulo $1$), and a precision $0 < \varepsilon \le 1/2$. For type 1, weights $c_0, \ldots, c_{m-1} \in \mathbb{C}$ and the number $n \ge 1$ of frequencies. For type 2, coefficients $f_0, \ldots, f_{n-1} \in \mathbb{C}$.

**Output.** Type 1: $\tilde X_0, \ldots, \tilde X_{n-1}$ with $|\tilde X_k - X_k| \le \varepsilon \lVert c \rVert_1$, where $X_k = \sum_j c_j\, e(k t_j)$. Type 2: $\tilde y_0, \ldots, \tilde y_{m-1}$ with $|\tilde y_j - y_j| \le \varepsilon \lVert f \rVert_1$, where $y_j = \sum_k f_k\, e(k t_j)$. No normalization factor is applied. The option of the opposite sign $e(-kt_j)$ is obtained by conjugating input and output.

**Cost model.** The [real RAM](/real-ram/), with the real exponential counted as one operation. Real additions (with subtractions) and real multiplications are counted separately; a complex addition is $2$ real additions, a complex product $4$ real multiplications and $2$ real additions, and a complex number times a real one $2$ real multiplications. Floating-point rounding is discussed separately in Complexity.

## The algorithm

Put $x_j = 2\pi (t_j \bmod 1) \in [0, 2\pi)$. Shift the frequencies to the centered range: with $s = \lfloor n/2 \rfloor$ and $\kappa = k - s$, $X_k = \sum_j b_j e^{-i \kappa x_j}$ with $b_j = c_j\, e(s t_j)$, and $|\kappa| \le n/2$. Let $G(x) = e^{-x^2/(4\tau)}$, and let $g_\tau(x) = \sum_{p \in \mathbb{Z}} G(x - 2\pi p)$ be its periodization. Its Fourier coefficients are

$$\hat g(\kappa) = \frac{1}{2\pi} \int_0^{2\pi} g_\tau(x) e^{-i\kappa x}\, dx = \sqrt{\tau/\pi}\; e^{-\tau \kappa^2}.$$

The smoothed function $\sum_j b_j g_\tau(x - x_j)$ has Fourier coefficients $\hat g(\kappa) X_{\kappa + s}$. Sampling it on the grid $\xi_l = 2\pi l/N$ and taking a DFT of length $N$ gives $N \hat g(\kappa) X_{\kappa + s}$ up to aliasing, and $G$ is truncated to the $2M$ grid points nearest each $x_j$. The parameters, following Greengard and Lee (2004) for the choice of $\tau$, are

$$M = \max\left(2, \left\lceil \tfrac{3}{2\pi} \ln(4/\varepsilon) \right\rceil\right), \quad N = \text{the least power of two} \ge \max(2n, 2M), \quad \tau = \frac{\pi M}{N(N - n/2)}.$$

```pseudo id=main
NUFFT-TYPE-1(t, c, n, ε)        ▷ X̃_k ≈ Σ_j c_j e(k t_j) for 0 ≤ k < n
L1  choose M, N, τ as above; h ← 2π/N; s ← ⌊n/2⌋
L2  v ← (0, …, 0) of length N
L3  for j ← 0 to m − 1 do
L4      x ← 2π (t_j mod 1); b ← c_j · e(s t_j); l_0 ← ⌊x / h⌋
L5      for L ← l_0 − M + 1 to l_0 + M do  v_(L mod N) ← v_(L mod N) + b · G(L h − x)     ▷ spread
L6  V ← FFT_N(v)                                         ▷ V_r = Σ_l v_l ω_N^(l r)
L7  for k ← 0 to n − 1 do
L8      κ ← k − s; X̃_k ← √(π/τ) · e^(τ κ²) · V_(κ mod N) / N                        ▷ deconvolve
L9  return X̃
```

**Type 2** is the transpose: place $a_{\kappa \bmod N} = \sqrt{\pi/\tau}\, e^{\tau\kappa^2} f_{\kappa + s} / N$ on the grid, compute $U = \mathrm{FFT}_N(a)$, and return $\tilde y_j = e(s t_j) \sum_{L = l_0 - M + 1}^{l_0 + M} U_{L \bmod N}\, G(Lh - x_j)$. In matrix form, type 1 computes $D F S c$ with $S$ the $N \times m$ spreading matrix, $F$ the symmetric DFT matrix of order $N$ and $D$ the $n \times N$ deconvolution, and type 2 computes $S^{\mathsf T} F D^{\mathsf T} f$.

## Example

Type 1 with $t = (0, 1/8)$, $c = (1, 1)$, $n = 4$ and $\varepsilon = 10^{-2}$. Then $M = \lceil 0.477 \ln 400 \rceil = 3$, $N = 8$, $h = \pi/4$, $\tau = 3\pi/(8 \cdot 6) = \pi/16$, $s = 2$, and $G(Lh - x) = e^{-(Lh - x)^2 \cdot 4/\pi}$. The points are $x = 0$ with $b = 1$ and $l_0 = 0$, and $x = \pi/4$ with $b = e(2/8) = -i$ and $l_0 = 1$. Each spreads onto $6$ grid points with the weights $1, e^{-\pi/4} \approx 0.4559, e^{-\pi} \approx 0.0432, e^{-9\pi/4} \approx 0.0009$ by distance, which gives (to $4$ digits)

$$v = (1 - 0.4559i,\ 0.4559 - i,\ 0.0432 - 0.4559i,\ 0.0009 - 0.0432i,\ -0.0009i,\ 0,\ 0.0432,\ 0.4559 - 0.0432i).$$

The FFT of length $8$ and the deconvolution factor $\sqrt{\pi/\tau}\, e^{\tau\kappa^2}/N = \frac12 e^{\pi\kappa^2/16}$ give:

| k | κ | V_(κ mod 8) | factor | X̃_k | X_k = 1 + ω_8^k | error |
|---|---|---|---|---|---|---|
| 0 | −2 | 1.8271 − 0.0017i | 1.0966 | 2.0037 − 0.0019i | 2 | 4.2e−3 |
| 1 | −1 | 2.8072 − 1.1616i | 0.6085 | 1.7081 − 0.7068i | 1.7071 − 0.7071i | 1.1e−3 |
| 2 | 0 | 1.9992 − 1.9992i | 0.5 | 0.9996 − 0.9996i | 1 − i | 6.0e−4 |
| 3 | 1 | 0.4811 − 1.1628i | 0.6085 | 0.2928 − 0.7075i | 0.2929 − 0.7071i | 4.4e−4 |

All errors are below $\varepsilon \lVert c \rVert_1 = 0.02$; the proved bound below gives $4 e^{-2\pi M/3} \lVert c \rVert_1 \approx 0.015$. The values were checked by script.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) splits the computed $\tilde X_k$ into the exact value and two errors. Without truncation, the DFT of the samples of $\sum_j b_j g_\tau(\cdot - x_j)$ equals $N \sum_{q} \hat g(\kappa + qN) \sum_j b_j e^{-i(\kappa + qN)x_j}$, by the Fourier series of $g_\tau$ and the orthogonality of the grid exponentials. The term $q = 0$, divided by $N \hat g(\kappa)$, is $X_k$. The terms $q \ne 0$ (aliasing) are bounded by $\lVert c \rVert_1 \cdot 2r/(1 - r)$ with $r = e^{-\tau N (N - n)}$, since $|\kappa| \le n/2$. The truncation of $G$ to $2M$ points drops terms of size at most $G(Mh)$ and smaller, and dividing by $N \hat g(\kappa)$ multiplies them by at most $e^{\tau n^2/4}/(N\sqrt{\tau/\pi})$. With the chosen $\tau$, both errors decay like $e^{-2\pi M/3}$ when $N \ge 2n$, and their sum is at most $4 e^{-2\pi M/3} \le \varepsilon$ by the choice of $M$. Type 2 is the transpose of the same linear map, so its error matrix is the transpose, and the bound on every entry gives $|\tilde y_j - y_j| \le \varepsilon \lVert f \rVert_1$.

## Complexity

**Operations (type 1).** Let $M$ and $N$ be as above, so $M = O(\log(1/\varepsilon))$ and $N \le 4\max(n, M)$.

- Lines L3 to L5: $m$ complex exponentials for the phases $e(s t_j)$ and $2Mm$ real exponentials for the kernel; $2Mm$ products of a complex number by a real one ($4Mm$ real multiplications) and $2Mm$ complex additions ($4Mm$ real additions), plus $O(1)$ real operations per kernel argument.
- Line L6: the radix-2 FFT of length $N$, $\frac N2 \lg N$ complex multiplications and $N \lg N$ complex additions, that is $2N \lg N$ real multiplications and $3N \lg N$ real additions.
- Lines L7 and L8: $n$ real exponentials and $O(n)$ real multiplications.

In total $O(N \log N + mM)$ additions and multiplications, which is $O(n \log n + m \log(1/\varepsilon) + \log(1/\varepsilon) \log\log(1/\varepsilon))$, and $O(m \log(1/\varepsilon) + n)$ exponentials. Type 2 has the same counts. The direct sum needs $mn$ complex multiplications.

**Space.** The grid of length $N = O(n + \log(1/\varepsilon))$ and the output; the input is only read.

**Error.** *Proved* (in exact arithmetic, for every input): $|\tilde X_k - X_k| \le 4 e^{-2\pi M/3} \lVert c \rVert_1 \le \varepsilon \lVert c \rVert_1$, and the same for type 2 with $\lVert f \rVert_1$. *Not proved here:* the effect of floating-point rounding, which adds the error of the FFT (Higham proves a bound of order $u \lg N$ for the radix-2 FFT) amplified by the deconvolution factor, at most $e^{\pi M/(4R(R - 1/2))}/\sqrt M$ with $R = N/n \ge 2$, about $10$ for $\varepsilon = 10^{-12}$. *Observed:* for $m = 97$ Gaussian random weights at uniform random points, the largest error relative to $\lVert c \rVert_1$ was between $10^{-4}\varepsilon$ and $4 \times 10^{-2}\varepsilon$ for $\varepsilon$ from $10^{-2}$ to $10^{-12}$ and $n \le 256$, so the bound is pessimistic by a factor of $25$ or more. At $\varepsilon = 10^{-14}$ rounding dominates, and the error reached $2.8\varepsilon$, about $125u$. The tests use the tolerance $(\varepsilon + 256(\lg N + 2) u) \lVert c \rVert_1$.

## Properties

- **Approximate, with a guarantee.** The error is controlled by one parameter, and halving $\varepsilon$ costs a constant number of extra grid points per point.
- **Linear.** Both types are linear maps, and type 2 is exactly the transpose of type 1 as computed, not only of the exact transform.
- **Any $n$.** The number of frequencies is arbitrary; only the inner FFT length is a power of two.
- **Oversampling.** The grid has at least $2n$ points; less oversampling needs wider kernels for the same precision.
- **Deterministic.** The operations depend on the positions of the points, not on the weights.

## Variants and improvements

- **Kernels.** Dutt and Rokhlin (1993) used Gaussians, Beylkin (1995) B-splines, Fessler and Sutton (2003) interpolators chosen by a min-max criterion, the NFFT library (Keiner, Kunis and Potts 2009) Kaiser-Bessel and other windows, and FINUFFT (Barnett, Magland and af Klinteberg 2019) the "exponential of semicircle" $e^{\beta(\sqrt{1 - z^2} - 1)}$, which reaches the same precision with fewer grid points per point.
- **Fast Gaussian gridding.** Greengard and Lee (2004) factor $G(Lh - x)$ into three exponentials, one depending on the point, one on $L - l_0$ only, and one computed by a running product, so each point needs $O(1)$ exponentials instead of $2M$.
- **More dimensions.** In dimension $d$ the kernel is a product of one-dimensional kernels, the grid is $d$-dimensional with $N^d$ points and a [multidimensional FFT](/multidimensional-fft/), and the spreading costs $O(m M^d)$.
- **Type 3.** Lee and Greengard (2005) handle nonuniform frequencies as well by spreading onto a grid, a type 2 transform, and a deconvolution.
- **Inverse transforms.** Recovering $f$ from nonuniform samples is a [least-squares problem](/least-squares-problem/), solved by conjugate gradients with one type 1 and one type 2 NUFFT per step.
- **Other methods.** Low-rank approximation of the NUDFT matrix (Ruiz-Antolín and Townsend 2018) and exact algebraic methods by [fast multipoint evaluation](/fast-multipoint-evaluation/) are listed on the page of the problem.

## When to use it

Use it whenever Fourier sums involve points or frequencies off a regular grid and $mn$ is large: image reconstruction from non-Cartesian measurements, spectral analysis of irregularly sampled data, and spectral methods with nonuniform grids. For points that are equispaced but off the integer grid, [Bluestein's algorithm](/bluestein-fft/) is exact and simpler. For small $m$ or $n$ the direct sum, or [Goertzel's algorithm](/goertzel-algorithm/) for a few frequencies, is faster.

## Pitfalls

- **Centered frequencies.** The deconvolution factor $e^{\tau\kappa^2}$ grows with $|\kappa|$; using frequencies $0$ to $n - 1$ without the shift $s$ makes it $e^{\tau(n-1)^2}$ instead of $e^{\tau n^2/4}$ and destroys the precision. The phase $e(s t_j)$ restores the uncentered convention.
- **Points outside $[0, 1)$.** Reduce them modulo $1$ first, or $l_0$ is off the grid; the spreading indices must wrap modulo $N$.
- **Too small a grid.** If $2M > N$ the $2M$ spread points wrap onto each other; the choice of $N$ above prevents this.
- **Precision beyond rounding.** Asking for $\varepsilon$ near $10^{-16}$ only adds work: rounding errors of order $100u$ remain.
- **Normalization.** Libraries differ in the sign, in centered or uncentered frequencies, and in the range of the points ($[0, 1)$ or $[-\pi, \pi)$); check against a direct sum.

## Implementations

The Python implementation in [impl/python/nonuniform_fft.py](impl/python/nonuniform_fft.py) follows the main block for type 1 and its transpose for type 2, with a radix-2 FFT using twiddles from the exact angles, and both signs through conjugation. The tests compare both types with the direct $O(mn)$ sums for $\varepsilon$ from $10^{-2}$ to $10^{-14}$, $n \in \{1, 2, 3, 8, 37, 128\}$ (not only powers of two) and up to $60$ points anywhere in $[-2, 2)$; check the transpose identity $\sum_k \tilde X_k f_k = \sum_j c_j \tilde y_j$; check that grid points $t_j = j/n$ give the DFT and that type 2 with the opposite sign and the factor $1/n$ inverts it; and check zeros, an impulse, a constant, no points, periodicity in the points, and a case with $n = 512$ and $m = 400$.

## History

Dutt and Rokhlin (1993) gave algorithms for the Fourier transforms of nonequispaced data with a cost of order $n \log n + m \log(1/\varepsilon)$ and a proved error, spreading with Gaussians onto an oversampled grid. Beylkin (1995) gave the same kind of scheme with B-splines. Earlier, Press and Rybicki (1989) had computed the Lomb periodogram of unevenly sampled data by extirpolation onto a regular grid followed by an FFT. Greengard and Lee (2004) reduced the number of exponentials in Gaussian gridding, and Lee and Greengard (2005) treated the type 3 transform. Fessler and Sutton (2003) designed min-max interpolators for imaging, Keiner, Kunis and Potts (2009) described the NFFT 3 library, and Barnett, Magland and af Klinteberg (2019) the FINUFFT library and its exponential of semicircle kernel.

## References
