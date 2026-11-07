---
tag: G69EYG
kind: problem
slug: nonuniform-discrete-fourier-transform
name: Nonuniform discrete Fourier transform
aliases:
- NUDFT
- nonequispaced discrete Fourier transform
- NDFT
- type 1 type 2 and type 3 NUDFT
area: algebra/fast-transforms
level: advanced
summary: DFT evaluated at arbitrary, non-grid frequencies or sample points.
model: real-ram
complexity:
  vars: {n: the number of frequencies, m: the number of points}
  time: {worst: O((m + n) log^2 (m + n))}
prereqs: [discrete-fourier-transform, dft-matrix]
see_also: [nonuniform-fft, fast-multipoint-evaluation, trigonometric-interpolation, bluestein-fft, least-squares-problem, multidimensional-fft, sparse-fourier-transform, polynomial-interpolation]
sources:
  - paper: doi:10.1137/0914081
    title: A. Dutt and V. Rokhlin, Fast Fourier transforms for nonequispaced data, SIAM Journal on Scientific Computing 14(6), 1993
    locator: pp. 1368 to 1393 (the transforms of nonequispaced data and their approximation to precision ε)
  - paper: doi:10.1006/acha.1995.1026
    title: G. Beylkin, On the fast Fourier transform of functions with singularities, Applied and Computational Harmonic Analysis 2(4), 1995
    locator: pp. 363 to 381
  - paper: doi:10.1137/S003614450343200X
    title: Leslie Greengard and June-Yub Lee, Accelerating the nonuniform fast Fourier transform, SIAM Review 46(3), 2004
    locator: pp. 443 to 454 (the type 1 and type 2 transforms in one and more dimensions)
  - paper: doi:10.1016/j.jcp.2004.12.004
    title: June-Yub Lee and Leslie Greengard, The type 3 nonuniform FFT and its applications, Journal of Computational Physics 206(1), 2005
    locator: pp. 1 to 5
  - paper: doi:10.1137/18M120885X
    title: Alexander H. Barnett, Jeremy Magland and Ludvig af Klinteberg, A parallel nonuniform fast Fourier transform library based on an exponential of semicircle kernel, SIAM Journal on Scientific Computing 41(5), 2019
    locator: pp. C479 to C504 (the definitions of the three types and the cost of the FINUFFT library)
  - paper: doi:10.1109/TSP.2002.807005
    title: Jeffrey A. Fessler and Bradley P. Sutton, Nonuniform fast Fourier transforms using min-max interpolation, IEEE Transactions on Signal Processing 51(2), 2003
    locator: pp. 560 to 574
  - paper: doi:10.1145/1555386.1555388
    title: Jens Keiner, Stefan Kunis and Daniel Potts, Using NFFT 3, a software library for various nonequispaced fast Fourier transforms, ACM Transactions on Mathematical Software 36(4), 2009
    locator: Article 19 (the NDFT and NFFT and their adjoints)
  - paper: doi:10.1086/167197
    title: William H. Press and George B. Rybicki, Fast algorithm for spectral analysis of unevenly sampled data, The Astrophysical Journal 338, 1989
    locator: from p. 277 (the Lomb periodogram by extirpolation onto a grid and an FFT)
  - book: isbn:9783030043056
    title: Gerlind Plonka, Daniel Potts, Gabriele Steidl and Manfred Tasche, Numerical Fourier Analysis, Birkhäuser, 2018
    locator: Chapter 7, Fast Fourier Transforms for Nonequispaced Data
  - book: isbn:9780521826464
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, second edition, Cambridge University Press, 2003
    locator: Chapter 10, Fast polynomial evaluation and interpolation (multipoint evaluation in O(M(n) log n) operations)
---

The nonuniform discrete Fourier transform (NUDFT) is the [discrete Fourier transform](/discrete-fourier-transform/) with the regular grid of sample points $j/n$, or the regular grid of integer frequencies, or both, replaced by arbitrary real numbers. It arises whenever data are not sampled on a grid: magnetic resonance imaging with non-Cartesian trajectories, radio interferometry, unevenly sampled time series, and spectral methods on adaptive grids. There are three standard types: type 1 sums values at nonuniform points into uniform frequencies, type 2 evaluates a Fourier series with uniform frequencies at nonuniform points, and type 3 has both nonuniform. Direct evaluation costs $O(mn)$ operations for $m$ points and $n$ frequencies. Exact algorithms with $O((m + n) \log^2 (m + n))$ operations exist but are numerically unstable, and in practice the [nonuniform FFT](/nonuniform-fft/) computes it to a chosen precision $\varepsilon$ in $O(n \log n + m \log(1/\varepsilon))$ operations in one dimension.

## In plain words

The ordinary Fourier transform needs samples taken at evenly spaced moments. Real measurements are often uneven: a scanner moves along a spiral, a telescope sees the sky at scattered positions, a sensor drops readings. The nonuniform transform asks the same question as the ordinary one, how much of each frequency is present, but allows the samples to sit anywhere. It can also ask the reverse question: given the amounts of each frequency, what is the signal at a list of arbitrary places. Done naively, every sample meets every frequency, which is slow for large inputs. Fast methods spread the scattered samples onto a nearby even grid and use the ordinary fast transform.

## Definition

**Notation.** As on all pages of fast transforms, $\omega_n = e^{-2\pi i/n}$, the sign of signal processing, FFTW and NumPy (CLRS uses the other sign), and the DFT is $X_k = \sum_{j=0}^{n-1} x_j \omega_n^{jk}$, with inverse factor $1/n$. Write $e(t) = e^{-2\pi i t}$, so $\omega_n^{jk} = e(jk/n)$. There are $m$ points $t_0, \ldots, t_{m-1} \in [0, 1)$ (any real numbers; only their values modulo $1$ matter in types 1 and 2) and $n$ integer frequencies $k = 0, \ldots, n - 1$. Let $A$ be the $m \times n$ matrix with $A_{jk} = e(k t_j)$. No normalization factor is applied in any type.

**Type 1** (nonuniform to uniform). Given $c_0, \ldots, c_{m-1} \in \mathbb{C}$, compute

$$X_k = \sum_{j=0}^{m-1} c_j\, e(k t_j) \qquad (0 \le k < n), \quad\text{that is } X = A^{\mathsf T} c.$$

**Type 2** (uniform to nonuniform). Given $f_0, \ldots, f_{n-1} \in \mathbb{C}$, compute

$$y_j = \sum_{k=0}^{n-1} f_k\, e(k t_j) \qquad (0 \le j < m), \quad\text{that is } y = A f,$$

the values of the trigonometric polynomial $\sum_k f_k e(k t)$ at the points $t_j$.

**Type 3** (nonuniform to nonuniform). Given $c$, points $t_j$ and real frequencies $s_0, \ldots, s_{n-1}$, compute $X_l = \sum_j c_j\, e(s_l t_j)$.

When $m = n$ and $t_j = j/n$, the matrix $A$ is the [DFT matrix](/dft-matrix/), which is symmetric, and types 1 and 2 are both the DFT. In general $A$ is not square and not unitary, and types 1 and 2 are transposes of each other; the adjoint $A^* c$, which is what the reconstruction methods of the Variants need, is type 1 with the opposite sign. Libraries let the user choose the sign and often use the centered frequencies $-n/2 \le k < n/2$; shifting the frequency range by $a$ multiplies $y_j$ by $e(a t_j)$ in type 2 and permutes $X$ in type 1, so the choice does not change the problem.

**Names.** Dutt and Rokhlin (1993) called these "Fourier transforms for nonequispaced data"; the numbering of types 1, 2 and 3 is used by Greengard and Lee (2004), Lee and Greengard (2005) and the FINUFFT library of Barnett, Magland and af Klinteberg (2019), and the names NDFT and NFFT by the NFFT library of Keiner, Kunis and Potts (2009).

## Variants

- **Dimension $d$.** Points $t_j \in [0, 1)^d$ and frequencies in a box $k \in \prod_a [0, n_a)$, with $e(k \cdot t_j)$; the total number of frequencies is $N = \prod_a n_a$. This is the case of imaging.
- **Approximate versions.** Given $\varepsilon > 0$, return $\tilde X$ with $\lVert \tilde X - X \rVert_\infty \le \varepsilon \lVert c \rVert_1$ (or a $2$-norm relative error). This is the problem the nonuniform FFT solves.
- **Equispaced but off-grid points.** If $t_j = a + jh$ for any real $a$ and $h$, type 2 is the evaluation of the polynomial $\sum_k f_k z^k$ on a geometric sequence $z_j = e(a) e(h)^j$, the chirp z-transform, which [Bluestein's FFT](/bluestein-fft/) computes exactly with $O((m + n) \log(m + n))$ operations.
- **Inverse problems.** Given $y$ and the points, find $f$ with $A f \approx y$ in the least-squares sense (a [least-squares problem](/least-squares-problem/)), or given $X$ find $c$. These are solved iteratively with fast type 1 and type 2 transforms inside the iteration, and their difficulty depends on how evenly the points cover $[0, 1)$; there is no direct inverse with a factor $1/n$.
- **Over other rings.** Type 2 with $e(t_j)$ replaced by arbitrary elements $z_j$ of a field is [multipoint evaluation](/fast-multipoint-evaluation/) of a polynomial of degree less than $n$; type 1 is the computation of the power sums $\sum_j c_j z_j^k$ for $k < n$.

## Examples

**Type 1.** Take $m = 2$ points $t = (0, 1/8)$, weights $c = (1, 1)$, and $n = 4$. Then $X_k = 1 + e(k/8) = 1 + \omega_8^k$ with $\omega_8 = (1 - i)/\sqrt2$:

$$X = \left(2,\ 1 + \tfrac{1 - i}{\sqrt2},\ 1 - i,\ 1 - \tfrac{1 + i}{\sqrt2}\right) \approx (2,\ 1.7071 - 0.7071 i,\ 1 - i,\ 0.2929 - 0.7071 i).$$

No DFT of length $4$ gives this, since the point $1/8$ is not on the grid $\{0, 1/4, 1/2, 3/4\}$.

**Type 2.** Take $f = (1, 2, 0, 1)$ and the points $t = (0, 1/8, 1/2)$. The values of $1 + 2e(t) + e(3t)$ are

$$y = \left(4,\ 1 + \tfrac{1 - 3i}{\sqrt2},\ -2\right) \approx (4,\ 1.7071 - 2.1213 i,\ -2).$$

**Type 3.** With $c = (1, 1)$ at $t = (0, 1/2)$ and frequencies $s = (1/2, 3/2)$, $X = (1 + e(1/4), 1 + e(3/4)) = (1 - i, 1 + i)$.

All three examples were checked by script against the definitions.

## Known algorithms

- **Direct evaluation.** Form each entry $e(k t_j)$ and sum: $mn$ complex multiplications and about as many additions, and $mn$ evaluations of the exponential, or only $m$ of them if the powers $e(t_j)^k$ are built by repeated multiplication (which loses accuracy for large $n$), or Horner's rule in type 2. In floating point, each output has error $O(n u)$ relative to $\lVert f \rVert_1$ with recursive summation.
- **[Nonuniform FFT](/nonuniform-fft/).** Spread the values onto an oversampled regular grid of size $\sigma n$ with a smooth kernel of width $w$, run an FFT, and correct by the Fourier transform of the kernel. With $w = O(\log(1/\varepsilon))$ it achieves precision $\varepsilon$ in $O(\sigma n \log (\sigma n) + m w)$ operations in one dimension (Dutt and Rokhlin 1993 with a Gaussian kernel; Greengard and Lee 2004; Barnett, Magland and af Klinteberg 2019 with the "exponential of semicircle" kernel), and $O(N \log N + m w^d)$ in dimension $d$. Fessler and Sutton (2003) choose the interpolation weights by a min-max criterion.
- **Type 3.** Lee and Greengard (2005) reduce type 3 to a type 1 transform followed by a type 2 transform, with a cost that depends on the product of the spreads of the points and the frequencies.
- **Low-rank approximation.** Ruiz-Antolín and Townsend (2018) write $A$ as the DFT matrix multiplied entrywise by a matrix of low numerical rank, and use a few FFTs.
- **Exact algebraic algorithms.** Type 2 is multipoint evaluation of $\sum_k f_k z^k$ at $z_j = e(t_j)$, which takes $O(M(n') \log n')$ operations with $n' = m + n$ and $M$ the cost of polynomial multiplication (von zur Gathen and Gerhard, Chapter 10); with FFT multiplication this is $O(n' \log^2 n')$. Type 1 is the power series of $\sum_j c_j / (1 - z_j y)$ to order $n$: the sum of fractions is formed by a product tree, then expanded by one power series division, in the same time. These counts are exact in the real RAM, but the algorithms are numerically unstable in floating point, so they are not used for large inputs.

## Bounds

- **Upper bounds.** $O(mn)$ by the definition; $O((m + n) \log^2 (m + n))$ exact operations by multipoint evaluation; $O(n \log n + m \log(1/\varepsilon))$ operations to precision $\varepsilon$ in one dimension by the nonuniform FFT.
- **Lower bounds.** Any algorithm reads the input and writes the output, so $\Omega(m + n)$. We know of no better lower bound in a general model; for the special case $t_j = j/n$ the problem is the DFT, for which no lower bound of order $n \log n$ is known for general arithmetic circuits either.
- **Precision.** For the approximate problem the dependence on $\varepsilon$ is through the kernel width $w = O(\log(1/\varepsilon))$; with a Gaussian kernel and oversampling factor $2$, Dutt and Rokhlin bound the error, and the exponential of semicircle kernel achieves about $\log_{10}(1/\varepsilon) + 1$ grid points per dimension (Barnett, Magland and af Klinteberg 2019).

## Reductions

- **To the DFT.** If all $t_j$ lie on the grid $\{0, 1/n', \ldots\}$ for some $n'$, type 1 is a DFT of length $n'$ of the values summed into the grid cells, and type 2 is a DFT of length $n'$ (with $f$ padded with zeros, or folded modulo $n'$ if $n > n'$) read at the grid points.
- **Type 1 and type 2 are transposes.** By the transposition principle for linear algorithms, an algorithm for $y = A f$ with a given number of operations gives one for $X = A^{\mathsf T} c$ with about the same number, and conversely.
- **Type 3 to types 1 and 2.** As in Lee and Greengard (2005), through an intermediate regular grid.
- **From polynomial evaluation.** Over $\mathbb{C}$ with points on the unit circle, type 2 is multipoint evaluation; conversely, multipoint evaluation at points on the unit circle is type 2.
- **To interpolation.** The inverse of square type 2 with distinct points is [polynomial interpolation](/polynomial-interpolation/) at the points $e(t_j)$, or [trigonometric interpolation](/trigonometric-interpolation/).

## Applications

- **Medical imaging.** In magnetic resonance imaging the scanner measures Fourier coefficients along non-Cartesian trajectories such as spirals and radial lines, and reconstruction needs type 1 and type 2 transforms in two and three dimensions (Fessler and Sutton 2003).
- **Radio astronomy.** Interferometers measure Fourier coefficients of the sky at scattered points, and imaging grids them, which is a type 1 transform.
- **Unevenly sampled time series.** Spectral analysis of data at irregular times, for example the Lomb-Scargle periodogram, needs the sums of type 1 with the sample times as points; Press and Rybicki (1989) computed them fast by spreading the data onto a regular grid and running an FFT.
- **Numerical analysis.** Spectral methods with adaptive or moving grids, the evaluation of Fourier series at arbitrary points, and fast summation of kernels use types 1, 2 and 3 (Greengard and Lee 2004; Plonka, Potts, Steidl and Tasche, Chapter 7).

## References
