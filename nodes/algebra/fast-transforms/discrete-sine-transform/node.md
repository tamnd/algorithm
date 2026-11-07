---
tag: 0BEMXV
kind: problem
slug: discrete-sine-transform
name: Discrete sine transform
aliases:
- DST
- DST-I
- DST-II
- sine transform
area: algebra/fast-transforms
level: core
summary: Real transform on sine basis functions, the DFT's odd-symmetric counterpart.
model: real-ram
complexity:
  vars: {n: the transform length}
  time: {worst: O(n log n)}
prereqs: [discrete-fourier-transform, discrete-cosine-transform]
see_also: [fast-dct, fast-fourier-transform, real-valued-fft, poisson-equation, karhunen-loeve-transform, spectral-methods, finite-difference-method, discrete-hartley-transform]
sources:
  - paper: doi:10.1109/78.295213
    title: Stephen A. Martucci, Symmetric convolution and the discrete sine and cosine transforms, IEEE Transactions on Signal Processing 42(5), 1994
    locator: pp. 1038 to 1051 (the sixteen DCTs and DSTs as DFTs of symmetric extensions, and the convolution-multiplication property)
  - paper: doi:10.1137/S0036144598336745
    title: Gilbert Strang, The discrete cosine transform, SIAM Review 41(1), 1999
    locator: pp. 135 to 147 (the eight DCTs as eigenvectors of second-difference matrices; the DSTs arise in the same way with Dirichlet ends)
  - paper: doi:10.1109/TCOM.1976.1093409
    title: Anil K. Jain, A fast Karhunen-Loeve transform for a class of random processes, IEEE Transactions on Communications 24(9), 1976
    locator: pp. 1023 to 1029 (the sine transform as the Karhunen-Loève transform of a first-order Markov process with fixed ends)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 4, Section 4.4, The fast sine and cosine transforms (the DST by an FFT of real data, and the Poisson solvers built on it)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 24, Section 24.1 (the FFT error bound, which carries over to the DST through the reductions below)
---

The discrete sine transform (DST) writes a real vector of length $n$ as a combination of sampled sine waves. Its most used form, the DST-I, is

$$X_k = \sum_{j=0}^{n-1} x_j \sin\frac{\pi (j + 1)(k + 1)}{n + 1}, \qquad 0 \le k \le n - 1.$$

It is the [discrete Fourier transform](/discrete-fourier-transform/) of the odd extension of $x$, in the way the [DCT](/discrete-cosine-transform/) is the DFT of an even extension, and it has four main types, DST-I to DST-IV, that differ in where the extension is centred. The DST-I diagonalizes the second-difference matrix with zero (Dirichlet) boundary values, which makes it the standard tool for fast [Poisson solvers](/poisson-equation/) on a rectangle. The direct sum takes $\Theta(n^2)$ operations; every type reduces to an [FFT](/fast-fourier-transform/) with $O(n)$ extra work, so it takes $O(n \log n)$.

## In plain words

A sine transform describes a list of real numbers as a sum of sine waves. Every sine wave starts at zero, so the sine transform suits data that is pinned to zero just outside both ends, like a string held at its two ends. Mirroring the list with a change of sign turns it into a Fourier transform problem, which is why the fast Fourier transform also gives a fast sine transform.

There are several kinds of sine transform. They differ only in where the mirror is placed: exactly on the end point, or half a step past it. Each kind has its own simple inverse, and each kind is computed by the same fast methods as the Fourier transform.

## Definition

**Notation.** As on the [DFT page](/discrete-fourier-transform/): $n$ is the transform length, any positive integer in the definitions (the fast algorithms are simplest when $n + 1$, or $n$, is a power of two); $\omega_N = e^{-2\pi i/N}$, with the minus sign of signal processing; the DFT is $Y_k = \sum_m y_m \omega_N^{mk}$, and its inverse has the factor $1/N$.

**Input.** A real vector $x = (x_0, \ldots, x_{n-1})$. **Output.** $X = S x$ for one of the matrices below, indexed by the row $k$ and the column $j$, with $0 \le j, k \le n - 1$.

| type | entry $S_{kj}$ | inverse |
|---|---|---|
| DST-I | $\sin\frac{\pi(j+1)(k+1)}{n+1}$ | $S_{\mathrm I}^2 = \frac{n+1}{2} I$ |
| DST-II | $\sin\frac{\pi(2j+1)(k+1)}{2n}$ | $S_{\mathrm{II}} S_{\mathrm{II}}^{\mathsf T} = \mathrm{diag}(\frac{n}{2}, \ldots, \frac{n}{2}, n)$ |
| DST-III | $\sin\frac{\pi(j+1)(2k+1)}{2n}$, so $S_{\mathrm{III}} = S_{\mathrm{II}}^{\mathsf T}$ | $x = S_{\mathrm{II}}^{\mathsf T} D^{-1} X$ inverts the DST-II |
| DST-IV | $\sin\frac{\pi(2j+1)(2k+1)}{4n}$ | $S_{\mathrm{IV}}^2 = \frac{n}{2} I$ |

These are the unnormalized forms; FFTW's RODFT00, RODFT10, RODFT01 and RODFT11 are twice these (FFTW also halves the weight of the last input of the DST-III, which makes it exactly the inverse of the DST-II up to the factor $2n$). The orthonormal forms multiply $S_{\mathrm I}$ by $\sqrt{2/(n+1)}$ and $S_{\mathrm{IV}}$ by $\sqrt{2/n}$, which makes them symmetric orthogonal matrices, each its own inverse.

**Odd extension.** For the DST-I, put $N = 2(n + 1)$ and $y = (0, x_0, \ldots, x_{n-1}, 0, -x_{n-1}, \ldots, -x_0)$, so that $y_{N - m} = -y_m$. Then the DFT of $y$ is purely imaginary, and $Y_{k+1} = -2i X_k$ for $0 \le k \le n - 1$. The other types come from the odd extensions about a half-sample point (Martucci 1994).

## Variants

- **The eight DSTs.** Martucci lists eight DSTs, matching the eight DCTs. Types I to IV come from symmetric extensions of even length and are the common ones; types V to VIII come from extensions of odd length.
- **Normalizations.** Unnormalized (as above), FFTW's (a factor $2$), and orthonormal.
- **Two and more dimensions.** The DST of an array is a DST along each axis in turn.
- **Integer approximations.** Video codecs use integer matrices close to a scaled DST; HEVC uses one close to a DST-VII for small intra-predicted luma blocks.

## Examples

**DST-I, $n = 3$.** With $\sin\frac{\pi}{4} = \sin\frac{3\pi}{4} = \frac{\sqrt 2}{2}$ and $\sin\frac{\pi}{2} = 1$, the DST-I of $x = (1, 2, 3)$ is

$$X = \left(\tfrac{\sqrt 2}{2} \cdot 1 + 2 + \tfrac{\sqrt 2}{2} \cdot 3,\ 1 - 3,\ \tfrac{\sqrt 2}{2} \cdot 1 - 2 + \tfrac{\sqrt 2}{2} \cdot 3\right) = (2 + 2\sqrt 2,\ -2,\ 2\sqrt 2 - 2) \approx (4.8284, -2, 0.8284).$$

Applying the DST-I again gives $(2, 4, 6) = \frac{n+1}{2} x$, as the table says. For $n = 1$ the DST-I is the identity.

**DST-II, $n = 4$.** For $x = (1, 2, 3, 4)$, $X \approx (6.5328, -2.8284, 2.7060, -2)$. The last entry is $\sum_j (-1)^j x_j = 1 - 2 + 3 - 4 = -2$, since $\sin\frac{\pi(2j+1)}{2} = (-1)^j$.

**Eigenvectors.** Let $T$ be the $n \times n$ matrix with $2$ on the diagonal and $-1$ next to it, the second difference with $x_{-1} = x_n = 0$. The rows of $S_{\mathrm I}$ are eigenvectors of $T$: the row $k$ has the eigenvalue $2 - 2\cos\frac{\pi(k+1)}{n+1} = 4\sin^2\frac{\pi(k+1)}{2(n+1)}$. So $T = \frac{2}{n+1} S_{\mathrm I} \Lambda S_{\mathrm I}$, and solving $T u = f$ costs two DST-I and $n$ divisions.

All three examples were checked by a script against the direct sums.

## Known algorithms

- **Direct sum.** $\Theta(n^2)$ operations with a table of sines.
- **FFT of the odd extension.** Build $y$ of length $2(n+1)$ and take one complex [FFT](/fast-fourier-transform/); $X_k = \frac{i}{2} Y_{k+1}$. This is $O(n \log n)$ but wastes a factor of about $4$, because $y$ is real and odd.
- **Real FFT of length $n + 1$.** Van Loan (Section 4.4) gives the classical method: a pre-processing step on $x$ of $O(n)$ operations, one [real-valued FFT](/real-valued-fft/) of length $n + 1$, and a post-processing recursion. This removes the redundancy of the odd extension.
- **Through the DCT.** $S_{\mathrm{II}} x$ is the [DCT-II](/fast-dct/) of $((-1)^j x_j)$ read backwards: $(S_{\mathrm{II}} x)_k = (C ((-1)^j x_j))_{n-1-k}$, by $\cos(\frac{\pi(2j+1)}{2} - \theta) = (-1)^j \sin\theta$. So any fast DCT-II, such as Makhoul's, gives a fast DST-II, and in the same way a fast DCT-III gives a fast DST-III. The DST-IV is reduced to the DCT-IV, which is computed by a complex FFT of length $n/2$.
- **Direct factorizations.** Sparse factorizations of the sine matrices, analogous to those for the DCT, reach about the same operation counts as the best DCT algorithms.

## Bounds

**Upper bound.** $O(n \log n)$ real operations for every type, by the reductions above; the FFT error bound (Higham, Chapter 24) carries over, so the relative 2-norm error is $O(u \log n)$ for an accurate FFT.

**Lower bound.** Each DST matrix is invertible. For $S_{\mathrm I}$, $S_{\mathrm I}^2 = \frac{n+1}{2} I$ gives $|\det S_{\mathrm I}| = \left(\frac{n+1}{2}\right)^{n/2}$, so Morgenstern's determinant argument gives $\Omega(n \log n)$ additions for linear algorithms whose constants have modulus at most $1$, the same model in which the [FFT](/fast-fourier-transform/) bound holds. Every algorithm must read all $n$ inputs, which gives the trivial $\Omega(n)$ in general.

## Reductions

- **DST to DFT.** The DST-I is $\frac{i}{2}$ times a DFT of length $2(n+1)$ of the odd extension; the other types are DFTs of half-sample odd extensions.
- **DST to DCT.** The sign change $x_j \mapsto (-1)^j x_j$ and the index reversal $k \mapsto n - 1 - k$ turn the DST-II into the DCT-II, and the DST-III into the DCT-III, with no arithmetic.
- **Symmetric convolution.** Martucci showed that the DSTs and DCTs diagonalize symmetric convolutions, as the DFT diagonalizes cyclic [convolution](/convolution/), which gives filtering of symmetric signals without boundary artifacts.
- **Inverse.** Each type inverts with a DST of the same or the transposed type and a diagonal scaling, as in the table.

## Applications

- **Poisson and heat equations with Dirichlet boundaries.** The DST-I diagonalizes the [finite-difference](/finite-difference-method/) Laplacian on a rectangle with zero boundary values, giving an $O(n^2 \log n)$ solver on an $n \times n$ grid.
- **Spectral methods.** Sine series expansions in [spectral methods](/spectral-methods/) for problems with zero boundary values.
- **Signal and image coding.** The DST-I is the [Karhunen-Loève transform](/karhunen-loeve-transform/) of a first-order Markov process whose end values are known (Jain 1976). Small DST-type transforms code the residuals of intra prediction in video.
- **Interpolation and filtering** of data that is odd about its ends.

## References
