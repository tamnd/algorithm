---
tag: EWEX4W
kind: algorithm
slug: fast-dct
name: Fast discrete cosine transform
aliases:
- fast cosine transform
- FCT
- DCT-II via FFT
- Makhoul's algorithm
area: algebra/fast-transforms
level: core
summary: Computes the DCT in O(n log n) by reducing it to an FFT of the same length.
model: real-ram
complexity:
  vars: {n: the transform length (a power of two)}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1980
  people: [John Makhoul]
  note: Makhoul gave the reduction of the DCT-II of length n to one FFT of length n in 1980. The DCT itself is due to Ahmed, Natarajan and Rao (1974).
prereqs: [discrete-cosine-transform, fast-fourier-transform]
see_also: [discrete-sine-transform, discrete-fourier-transform, modified-discrete-cosine-transform, jpeg-compression, fast-hartley-transform, poisson-equation, real-valued-fft, discrete-hartley-transform]
sources:
  - paper: doi:10.1109/TASSP.1980.1163351
    title: John Makhoul, A fast cosine transform in one and two dimensions, IEEE Transactions on Acoustics, Speech, and Signal Processing 28(1), 1980
    locator: pp. 27 to 34 (the even-odd reordering and the computation of the DCT from one DFT of the same length)
  - paper: doi:10.1109/T-C.1974.223784
    title: Nasir Ahmed, T. Natarajan and K. R. Rao, Discrete cosine transform, IEEE Transactions on Computers C-23(1), 1974
    locator: pp. 90 to 93 (the definition of the DCT and its computation by a DFT of length 2n)
  - paper: doi:10.1137/S0036144598336745
    title: Gilbert Strang, The discrete cosine transform, SIAM Review 41(1), 1999
    locator: pp. 135 to 147 (the eight types of DCT as eigenvectors of second-difference matrices with different boundary conditions)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 4, Section 4.4, The fast sine and cosine transforms (the DCT and DST by FFTs of real data)
  - paper: doi:10.1109/TCOM.1977.1093941
    title: Wen-Hsiung Chen, C. Harrison Smith and S. C. Fralick, A fast computational algorithm for the discrete cosine transform, IEEE Transactions on Communications 25(9), 1977
    locator: pp. 1004 to 1009 (a direct sparse factorization of the DCT matrix)
  - paper: doi:10.1109/TASSP.1984.1164443
    title: Byeong Gi Lee, A new algorithm to compute the discrete cosine transform, IEEE Transactions on Acoustics, Speech, and Signal Processing 32(6), 1984
    locator: pp. 1243 to 1245 (a recursive radix-2 DCT algorithm)
  - paper: doi:10.1109/ICASSP.1989.266596
    title: Christoph Loeffler, Adriaan Ligtenberg and George S. Moschytz, Practical fast 1-D DCT algorithms with 11 multiplications, ICASSP 1989
    locator: pp. 988 to 991 (the length-8 DCT with 11 multiplications)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 24, Theorem 24.2 (the FFT error bound used for the error analysis on this page)
---

A fast discrete cosine transform computes the [DCT-II](/discrete-cosine-transform/) of length $n$,

$$X_k = \sum_{j=0}^{n-1} x_j \cos\frac{\pi (2j + 1) k}{2n}, \qquad 0 \le k \le n - 1,$$

in $O(n \log n)$ real operations instead of the $\Theta(n^2)$ of the direct sum. The method on this page is Makhoul's (1980): reorder the input so that the even-indexed entries come first and the odd-indexed entries follow in reverse, take one complex [FFT](/fast-fourier-transform/) of length $n$, and rotate each output by $e^{-\pi i k/(2n)}$ and keep its real part. The DCT-II is the transform of JPEG and of much of signal and image coding, because for smooth data it packs the energy into few coefficients; its inverse, a scaled DCT-III, is computed by the same steps in reverse.

## In plain words

The cosine transform describes a list of real numbers as a sum of cosine waves. It is close to the Fourier transform, but it uses only cosines and real numbers, and it treats the list as if it were mirrored at its ends, so a smooth list stays smooth at the edges. That is why few of its numbers are large for smooth data, which is what compression needs.

The fast method borrows the fast Fourier transform. It first reorders the list: the entries at even places from the front, then the entries at odd places from the back. A Fourier transform of the reordered list contains all the cosine sums, each turned by a known angle. So one transform of the same length, plus one turn per output, gives the cosine transform.

## The problem

**Notation.** As on the [DFT page](/discrete-fourier-transform/): $n$ is the transform length and must be a power of two for this method (it must be even for the reordering, and a power of two for the radix-2 FFT); $\omega_n = e^{-2\pi i/n}$, with the minus sign of signal processing, FFTW and NumPy; the DFT is $V_k = \sum_j v_j \omega_n^{jk}$, and its inverse has the factor $1/n$.

**Input.** A real vector $x = (x_0, \ldots, x_{n-1})$.

**Output.** The DCT-II $X = C x$ defined above, with $C_{kj} = \cos(\pi (2j+1) k / (2n))$. This is the unnormalized form of FFTW (up to a factor $2$) and of the original paper. The orthonormal form multiplies $X_0$ by $\sqrt{1/n}$ and the other $X_k$ by $\sqrt{2/n}$. The inverse is $x_j = \frac{1}{n} X_0 + \frac{2}{n} \sum_{k=1}^{n-1} X_k \cos\frac{\pi (2j+1) k}{2n}$, a scaled DCT-III, because the rows of $C$ are orthogonal with $C C^{\mathsf T} = \mathrm{diag}(n, \frac{n}{2}, \ldots, \frac{n}{2})$.

**Cost model.** Real additions and multiplications in the real RAM, counted separately where the literature does. In floating point, the error is analysed below.

## The algorithm

```pseudo id=main
FAST-DCT(x)             ▷ x[0 .. n − 1] real, n = 2^t; returns the DCT-II of x
L1  n ← |x|
L2  if n = 1 then return x
L3  for j ← 0 to n/2 − 1 do
L4      v[j] ← x[2j]                         ▷ even entries, in order
L5      v[n − 1 − j] ← x[2j + 1]             ▷ odd entries, in reverse order
L6  V ← FFT(v, ω_n)                          ▷ complex FFT of length n
L7  for k ← 0 to n − 1 do
L8      X[k] ← Re(e^(−πik/(2n)) · V[k])
L9  return X

INVERSE-FAST-DCT(X)     ▷ returns x with FAST-DCT(x) = X
L10 W[0] ← X[0]; W[k] ← e^(πik/(2n)) · (X[k] − i · X[n − k]) for k = 1, …, n − 1
L11 w ← INVERSE-FFT(W, ω_n)
L12 for j ← 0 to n/2 − 1 do x[2j] ← Re w[j], x[2j + 1] ← Re w[n − 1 − j]
```

The reordering $v$ is a permutation, so it costs no arithmetic. Line L8 needs only the real part: with $d_k = e^{-\pi i k/(2n)}$, $\mathrm{Re}(d_k V_k) = \cos(\frac{\pi k}{2n}) \mathrm{Re} V_k + \sin(\frac{\pi k}{2n}) \mathrm{Im} V_k$, which is $2$ real multiplications and $1$ addition. Because $v$ is real, $V_{n-k} = \overline{V_k}$, so only half of $V$ is needed, and a [real-valued FFT](/real-valued-fft/) of length $n$ (one complex FFT of length $n/2$ plus $O(n)$ work) is enough.

## Example

Transform $x = (1, 2, 3, 4)$, with $n = 4$. Let $c = \cos\frac{\pi}{8} \approx 0.92388$ and $s = \sin\frac{\pi}{8} \approx 0.38268$.

| step | values |
|---|---|
| L3 to L5, v | 1 3 4 2 |
| L6, V = F_4 v | 10, −3 − i, 0, −3 + i |
| L8, k = 0 | Re(10) = 10 |
| L8, k = 1 | Re((c − is)(−3 − i)) = −3c − s ≈ −3.1543 |
| L8, k = 2 | Re(e^(−πi/4) · 0) = 0 |
| L8, k = 3 | Re((s − ic)(−3 + i)) = −3s + c ≈ −0.2242 |

So $X \approx (10, -3.1543, 0, -0.2242)$, which equals the direct sums; for instance $X_2 = \cos\frac{\pi}{4} + 2\cos\frac{3\pi}{4} + 3\cos\frac{5\pi}{4} + 4\cos\frac{7\pi}{4} = \frac{\sqrt 2}{2}(1 - 2 - 3 + 4) = 0$. For $x = (1, 2, \ldots, 8)$ the method gives $X_0 = 36$, $X_1 \approx -12.8846$, $X_3 \approx -1.3469$, $X_5 \approx -0.4018$, $X_7 \approx -0.1014$, and $X_k = 0$ for even $k \ge 2$, because $x_j - \frac{9}{2}$ is odd about the centre.

## Correctness

Split the sum for $X_k$ by the parity of $j$. The even entries $x_{2r} = v_r$ give the angles $\pi(4r + 1)k/(2n)$. The odd entries $x_{2r+1} = v_{n-1-r}$ give $\pi(4r + 3)k/(2n)$, and with $r' = n - 1 - r$ this is $\pi(4n - (4r' + 1))k/(2n)$, whose cosine equals $\cos(\pi(4r' + 1)k/(2n))$ because $\cos(2\pi k - \theta) = \cos\theta$. So $X_k = \sum_{r=0}^{n-1} v_r \cos\frac{\pi(4r+1)k}{2n} = \mathrm{Re}\left(e^{-\pi i k/(2n)} \sum_r v_r e^{-2\pi i rk/n}\right) = \mathrm{Re}(d_k V_k)$, since $v$ is real. For the inverse, $V_{n-k} = \overline{V_k}$ gives $\mathrm{Re}(d_{n-k} V_{n-k}) = -\mathrm{Im}(d_k V_k)$, so $d_k V_k = X_k - i X_{n-k}$ for $1 \le k \le n - 1$, which is line L10 solved for $V_k$. The full proof is below.

## Complexity

**Real operations.** With a complex radix-2 FFT of length $n$ on the real vector $v$, line L6 costs about $5 n \lg n$ real operations, and lines L7 and L8 cost $2n$ multiplications and $n$ additions. With a real-valued FFT, line L6 costs about half as much, so the total is about $\frac{5}{2} n \lg n + O(n)$ real operations. Algorithms that factor the DCT matrix directly, such as those of Chen, Smith and Fralick (1977) and Lee (1984), and split-radix style DCTs, lower the constant further. For the length $8$ used by JPEG, Loeffler, Ligtenberg and Moschytz (1989) compute the DCT with $11$ multiplications.

**Time and space.** $\Theta(n \log n)$ in each case, with $\Theta(n)$ extra space for $v$, $V$ and the tables. The inverse has the same cost.

**Lower bound.** The DCT is an invertible linear map with $|\det C| = \sqrt{n \cdot (n/2)^{n-1}}$, so Morgenstern's determinant argument gives $\Omega(n \log n)$ for linear algorithms with constants of modulus at most $1$, as for the [FFT](/fast-fourier-transform/).

**Rounding errors (proved to first order).** Let $\delta$ be the relative 2-norm error bound of the FFT from Higham, Theorem 24.2, and let the rotations $d_k$ be computed with relative error at most $\mu$ and multiplied with error at most $\gamma = \sqrt 2 \gamma_2$. Since $\lVert V \rVert_2 = \sqrt n \lVert x \rVert_2$ and $\lVert C x \rVert_2 \ge \sqrt{n/2} \lVert x \rVert_2$, the computed $\hat X$ satisfies

$$\frac{\lVert \hat X - X \rVert_2}{\lVert X \rVert_2} \le \sqrt 2 \, (\delta + \mu + \gamma) + O(u^2),$$

which is $O(u \log n)$ for accurate twiddle factors. The derivation is in the proof below. As for the FFT, observed errors on random data are much smaller than this worst-case bound.

## Properties

- **Real in, real out.** The input and output are real; only the intermediate $V$ is complex.
- **Same length.** The FFT has the length $n$ of the input, not $2n$ or $4n$ as in the older reductions.
- **Not in place** in the form above, because of the reordering into $v$; it can be done in place with a permutation by cycles.
- **Energy compaction.** For smooth data the coefficients $X_k$ fall off quickly with $k$, because the DCT-II corresponds to the even extension of $x$, which has no jump at the ends.

## Variants and improvements

- **Older reductions.** Ahmed, Natarajan and Rao computed the DCT from a DFT of length $2n$ of $x$ padded with zeros. The even extension $(x_0, \ldots, x_{n-1}, x_{n-1}, \ldots, x_0)$ of length $2n$ also works, at twice the cost of Makhoul's method.
- **Direct factorizations.** Chen, Smith and Fralick (1977), Lee (1984), and many later algorithms factor $C$ into sparse matrices, with fewer operations than the FFT route.
- **Scaled DCTs.** When the output is quantized anyway, as in JPEG, the scaling factors can be moved into the quantization table, which saves multiplications.
- **Other types.** The DCT-III is the inverse of the DCT-II up to scaling (lines L10 to L12). The DCT-I and DCT-IV, and the [discrete sine transforms](/discrete-sine-transform/), reduce to FFTs in similar ways. The DCT-IV is the core of the [MDCT](/modified-discrete-cosine-transform/) used in audio coding.
- **Two dimensions.** The 2D DCT of an $n \times n$ block is $n$ DCTs of the rows followed by $n$ DCTs of the columns, $O(n^2 \log n)$ in total; Makhoul also gives a direct 2D form.
- **Via the Hartley transform.** The [fast Hartley transform](/fast-hartley-transform/) gives another real-arithmetic route to the DCT.

## When to use it

Use a fast DCT for transform coding of images, video and audio ([JPEG](/jpeg-compression/), MPEG, MP3 through the MDCT), for fast solvers of the [Poisson equation](/poisson-equation/) with Neumann boundary conditions, and for spectral methods with Chebyshev polynomials, whose coefficients are a DCT of the values at Chebyshev points. Use Makhoul's method when an FFT library is at hand; use a dedicated small-length DCT, such as the length-$8$ algorithms, inside codecs.

## Pitfalls

- **Normalization.** Libraries differ by a factor $2$ (FFTW's REDFT10 is $2X_k$) and by the orthonormal scaling. Check the round trip.
- **The sign convention.** With $\omega_n = e^{+2\pi i/n}$ the rotation must be $e^{+\pi i k/(2n)}$; the two choices give the same real output only if they are paired correctly.
- **Odd lengths.** The reordering of lines L3 to L5 needs $n$ even; for odd $n$ use the even extension of length $2n$ or a mixed-radix method.
- **Forgetting the real part.** $d_k V_k$ is complex in general; its imaginary part is $-X_{n-k}$, not zero.
- **DCT-II versus DCT-III.** The inverse of the DCT-II is the DCT-III with the weights $\frac{1}{n}$ and $\frac{2}{n}$, not the DCT-II again.

## Implementations

## History

Ahmed, Natarajan and Rao introduced the DCT in 1974, noting that it is close to the optimal Karhunen-Loève transform for highly correlated data and computing it with an FFT of length $2n$. Chen, Smith and Fralick (1977) gave a direct fast algorithm. Makhoul (1980) showed that one FFT of length $n$ suffices, by the even-odd reordering used on this page. Lee (1984) gave a recursive algorithm, and Loeffler, Ligtenberg and Moschytz (1989) the length-$8$ algorithm with $11$ multiplications. Strang (1999) surveyed the eight types of DCT and their origin as eigenvectors of second-difference matrices.

## References
