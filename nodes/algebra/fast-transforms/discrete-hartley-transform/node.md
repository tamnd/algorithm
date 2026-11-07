---
tag: 0Z5JPG
kind: problem
slug: discrete-hartley-transform
name: Discrete Hartley transform
aliases:
- DHT
- Hartley transform
area: algebra/fast-transforms
level: advanced
summary: Real self-inverse transform using the cas(x)=cos x + sin x kernel.
model: real-ram
complexity:
  vars: {n: the transform length}
  time: {worst: O(n log n)}
prereqs: [discrete-fourier-transform, convolution]
see_also: [fast-hartley-transform, real-valued-fft, fast-fourier-transform, discrete-sine-transform, fast-dct, convolution-theorem, split-radix-fft, dft-matrix]
sources:
  - paper: doi:10.1109/JRPROC.1942.234333
    title: Ralph V. L. Hartley, A more symmetrical Fourier analysis applied to transmission problems, Proceedings of the IRE 30(3), 1942
    locator: pp. 144 to 150 (the continuous transform with the kernel cos plus sin, and its self-inverse property)
  - paper: doi:10.1364/JOSA.73.001832
    title: Ronald N. Bracewell, Discrete Hartley transform, Journal of the Optical Society of America 73(12), 1983
    locator: p. 1832 onward (the discrete transform, its inverse, its relation to the DFT, and the convolution theorem)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 25, The Hartley transform (Section 25.1, Definition and symmetries; 25.3 to 25.5, FFTs by FHTs and back; 25.7, Convolution via FHT)
  - paper: doi:10.1109/TASSP.1985.1164687
    title: Henrik V. Sorensen, Douglas L. Jones, C. Sidney Burrus and Michael T. Heideman, On computing the discrete Hartley transform, IEEE Transactions on Acoustics, Speech, and Signal Processing 33(5), 1985
    locator: pp. 1231 to 1238 (operation counts of Hartley algorithms compared with real-valued FFTs)
  - paper: doi:10.1109/TASSP.1987.1165218
    title: Pierre Duhamel and Martin Vetterli, Improved Fourier and Hartley transform algorithms, application to cyclic convolution of real data, IEEE Transactions on Acoustics, Speech, and Signal Processing 35(6), 1987
    locator: pp. 818 to 824 (conversions between the real DFT and the DHT at O(n) cost, and real cyclic convolution)
---

The discrete Hartley transform (DHT) of a real vector $x$ of length $n$ is the real vector

$$H_k = \sum_{j=0}^{n-1} x_j \, \mathrm{cas}\frac{2\pi jk}{n}, \qquad \mathrm{cas}\,\theta = \cos\theta + \sin\theta, \qquad 0 \le k \le n - 1.$$

It carries the same information as the [discrete Fourier transform](/discrete-fourier-transform/) of $x$, but it maps real data to real data, and it is its own inverse up to the factor $1/n$: applying it twice gives $n x$. The two transforms convert into each other with $O(n)$ additions, $H_k = \mathrm{Re}\,X_k - \mathrm{Im}\,X_k$ with the sign convention of this section, so the DHT can be computed in $O(n \log n)$ by the [fast Hartley transform](/fast-hartley-transform/) or by a [real-valued FFT](/real-valued-fft/). Hartley introduced the continuous transform in 1942, and Bracewell the discrete one in 1983.

## In plain words

The Fourier transform describes a list of numbers by waves, but it uses complex numbers even when the list is real. The Hartley transform uses one real wave shape instead, a cosine and a sine added together. A real list then gives a real result, and the same formula that takes the list to the result also takes the result back to the list, after dividing by the length.

Nothing is lost by this: the Fourier result can be read off from the Hartley result by adding and subtracting pairs of numbers, and the other way round. So any fast method for one gives a fast method for the other. For a time the Hartley transform was thought to be faster for real data, but careful counts showed that good real Fourier methods are just as fast.

## Definition

**Notation.** As on the [DFT page](/discrete-fourier-transform/): $n$ is the transform length, any positive integer in the definition (the radix-2 fast Hartley transform needs a power of two); $\omega_n = e^{-2\pi i/n}$, with the minus sign of signal processing; the DFT is $X_k = \sum_j x_j \omega_n^{jk}$, and its inverse has the factor $1/n$. Indices are taken modulo $n$, so $H_{n-k}$ means $H_0$ when $k = 0$.

**Input.** A real vector $x = (x_0, \ldots, x_{n-1})$. **Output.** $H = \mathcal H_n x$, where $\mathcal H_n$ is the real symmetric $n \times n$ matrix with entries $\mathrm{cas}(2\pi jk/n)$.

**Inverse.** $\mathcal H_n^2 = n I$, so $x_j = \frac{1}{n} \sum_k H_k \, \mathrm{cas}\frac{2\pi jk}{n}$. The proof is short: $\mathrm{cas}\,a \, \mathrm{cas}\,b = \cos(a - b) + \sin(a + b)$, and summing over $k$ the sine terms cancel and the cosine terms give $n$ or $0$ as in the [summation lemma](/fft-summation-lemma/). The scaled matrix $n^{-1/2} \mathcal H_n$ is symmetric and orthogonal.

**Relation to the DFT.** Since $\omega_n^{jk} = \cos\frac{2\pi jk}{n} - i \sin\frac{2\pi jk}{n}$, with $E_k = \sum_j x_j \cos\frac{2\pi jk}{n}$ and $O_k = \sum_j x_j \sin\frac{2\pi jk}{n}$ we have $X_k = E_k - i O_k$ and $H_k = E_k + O_k$. Because $E$ is even and $O$ is odd in $k$,

$$E_k = \frac{H_k + H_{n-k}}{2}, \qquad O_k = \frac{H_k - H_{n-k}}{2}, \qquad H_k = \mathrm{Re}\,X_k - \mathrm{Im}\,X_k.$$

With the opposite sign convention $\omega_n = e^{+2\pi i/n}$ the last formula becomes $H_k = \mathrm{Re}\,X_k + \mathrm{Im}\,X_k$.

## Variants

- **Normalizations.** Unnormalized (as above, inverse with $1/n$), or unitary with $n^{-1/2}$ on both sides.
- **Complex input.** The DHT is defined by the same formula for complex $x$, acting on the real and imaginary parts separately.
- **Multidimensional DHT.** The separable form with $\mathrm{cas}(2\pi j_1 k_1/n_1) \, \mathrm{cas}(2\pi j_2 k_2/n_2)$ is not the same as the kernel $\mathrm{cas}(2\pi(j_1 k_1/n_1 + j_2 k_2/n_2))$; the two differ by an $O(n)$ correction.
- **The continuous transform.** Hartley's original transform of a function, $\int f(t) \, \mathrm{cas}(2\pi \nu t) \, dt$.

## Examples

**Length 4.** For $x = (1, 2, 3, 4)$, the kernel values $\mathrm{cas}(\pi jk/2)$ are $1, 1, -1, -1$ for $k = 1$ and $1, -1, 1, -1$ for $k = 2$, so

$$H = (10, \ 1 + 2 - 3 - 4, \ 1 - 2 + 3 - 4, \ 1 - 2 - 3 + 4) = (10, -4, -2, 0).$$

The DFT is $X = (10, -2 + 2i, -2, -2 - 2i)$, and indeed $\mathrm{Re}\,X_1 - \mathrm{Im}\,X_1 = -2 - 2 = -4$ and $\mathrm{Re}\,X_3 - \mathrm{Im}\,X_3 = -2 + 2 = 0$. Going back, $E_1 = \frac{H_1 + H_3}{2} = -2$ and $O_1 = \frac{H_1 - H_3}{2} = -2$, so $X_1 = E_1 - i O_1 = -2 + 2i$. Applying the DHT to $H$ gives $(4, 8, 12, 16) = 4x$.

**Length 8.** For $x = (1, 2, \ldots, 8)$, $H \approx (36, -13.6569, -8, -5.6569, -4, -2.3431, 0, 5.6569)$.

**Convolution.** The cyclic convolution of $x = (1, 2, 3, 4)$ and $y = (1, 1, 0, 0)$ is $z = (5, 3, 5, 7)$. With $H^y = (2, 2, 0, 0)$, the Hartley convolution theorem below gives $H^z_1 = \frac{1}{2}(-4 \cdot 2 + 0 \cdot 2) = -4$ and $H^z = (20, -4, 0, 4)$, which is the DHT of $z$.

**Edge cases.** For $n = 1$, $H_0 = x_0$; for $n = 2$, $H = (x_0 + x_1, x_0 - x_1)$, the same as the DFT. The DHT of an impulse at $0$ is the all-ones vector, and the DHT of a constant $c$ is $(nc, 0, \ldots, 0)$.

All examples were checked by a script against the direct sums.

## Known algorithms

- **Direct sum.** $\Theta(n^2)$ real operations with a table of $\mathrm{cas}$ values.
- **[Fast Hartley transform](/fast-hartley-transform/).** Bracewell's radix-2 algorithm (1984), $O(n \log n)$ real operations, in place, with the same structure as the radix-2 FFT; split-radix and higher-radix versions exist.
- **Through a real FFT.** Compute $X$ by a [real-valued FFT](/real-valued-fft/) and set $H_k = \mathrm{Re}\,X_k - \mathrm{Im}\,X_k$, at $n$ extra additions. Sorensen, Jones, Burrus and Heideman (1985) showed that this route and the best FHTs have essentially the same operation counts.
- **Through a complex FFT.** Treat $x$ as complex and take one FFT of length $n$; simpler but about twice the work.

## Bounds

**Upper bound.** $O(n \log n)$ real operations, by the algorithms above.

**Lower bound.** $|\det \mathcal H_n| = n^{n/2}$, because $\mathcal H_n^2 = n I$ and $\mathcal H_n$ is real. So Morgenstern's determinant argument gives at least $\frac{1}{2} n \lg n$ additions for linear algorithms whose constants have modulus at most $1$, the same bound and model as for the [DFT](/discrete-fourier-transform/). Without that restriction on the constants, no lower bound beyond $\Omega(n)$ is known, as for the DFT.

**Equivalence.** The DHT and the real DFT convert into each other with $O(n)$ additions, so their complexities differ by $O(n)$.

## Reductions

- **DHT to DFT.** $H_k = \mathrm{Re}\,X_k - \mathrm{Im}\,X_k$.
- **DFT to DHT.** $X_k = \frac{H_k + H_{n-k}}{2} - i \, \frac{H_k - H_{n-k}}{2}$.
- **Convolution theorem.** If $z$ is the cyclic [convolution](/convolution/) of real $x$ and $y$, then

$$H^z_k = \tfrac{1}{2}\left(H^x_k (H^y_k + H^y_{n-k}) + H^x_{n-k} (H^y_k - H^y_{n-k})\right).$$

This follows from the [convolution theorem](/convolution-theorem/) for the DFT and the two conversions. If $y$ is even ($y_j = y_{n-j}$), it simplifies to $H^z_k = H^x_k H^y_k$.

- **Shift.** A cyclic shift mixes $H_k$ and $H_{n-k}$: the DHT of $(x_{j-s})_j$ is $\cos(2\pi sk/n) H_k + \sin(2\pi sk/n) H_{n-k}$, from $\mathrm{cas}(a + b) = \cos b \, \mathrm{cas}\, a + \sin b \, \mathrm{cas}(-a)$.

## Applications

- **Real convolution and correlation** with real arithmetic only, through the convolution theorem above.
- **Real-input spectra.** The power spectrum is $|X_k|^2 = \frac{1}{2}(H_k^2 + H_{n-k}^2)$.
- **Optics and image processing**, where Bracewell promoted it for real data.
- **A single routine for forward and inverse.** Because the DHT is its own inverse up to $1/n$, one program serves both directions.

## References
