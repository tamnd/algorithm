---
tag: VB856E
kind: problem
slug: inverse-discrete-fourier-transform
name: Inverse discrete Fourier transform
aliases:
- IDFT
- inverse DFT
area: algebra/fast-transforms
level: core
summary: Recover the coefficients a_j from the values A_k, using the conjugate root of unity and a 1/n factor.
model: real-ram
complexity:
  vars: {n: the transform length}
  time: {worst: O(n log n)}
prereqs: [discrete-fourier-transform, roots-of-unity, polynomial-interpolation]
see_also: [inverse-fft, fast-fourier-transform, dft-matrix, parseval-theorem, convolution-theorem, fft-polynomial-multiplication, lagrange-interpolation, vandermonde-matrix]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Section 30.2, The DFT and FFT (the inverse of the Vandermonde matrix at the roots of unity, and interpolation by the FFT with the inverse root)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 8, Section 8.2, The Discrete Fourier Transform and the Fast Fourier Transform (the inverse DFT over a ring in which n is a unit)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1, Section 1.1, Matrix Notation and Algorithms (the inverse of the DFT matrix as its conjugate divided by n)
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 8, The Discrete Fourier Transform (the synthesis equation of the DFT)
  - paper: doi:10.1109/TCOM.1971.1090705
    title: S. B. Weinstein and Paul M. Ebert, Data transmission by frequency-division multiplexing using the discrete Fourier transform, IEEE Transactions on Communication Technology 19(5), 1971
    locator: pp. 628 to 634 (a transmitter that builds the signal by an inverse DFT)
---

The inverse discrete Fourier transform (IDFT) undoes the [DFT](/discrete-fourier-transform/): given $X_0, \ldots, X_{n-1}$, find the $x$ with $X_k = \sum_j x_j \omega^{jk}$ for each $k$. The answer is $x_j = \frac{1}{n} \sum_k X_k \omega^{-jk}$, which is again a DFT, with the inverse root $\omega^{-1}$ and a final division by $n$. In the language of polynomials, it is [interpolation](/polynomial-interpolation/): it finds the coefficients of the polynomial of degree less than $n$ that takes the values $X_k$ at the points $\omega^k$. So every fast algorithm for the DFT is also a fast algorithm for its inverse, and the problem has the same cost $\Theta(n \log n)$ by the [inverse FFT](/inverse-fft/). It exists over a ring exactly when $n$ is a unit there.

## In plain words

The Fourier transform takes a list of numbers and tells how much of each pure wave it contains. The inverse goes back: from the amounts of the waves, it rebuilds the list by adding up the waves.

The surprise is that going back is almost the same work as going forward. The waves used to rebuild are the same waves as before, only turning the other way, and at the end every number is divided by the length of the list. So one program does both jobs with a switch.

This only works if division by the length is allowed. In ordinary numbers it always is. In some kinds of clock arithmetic it is not, and then the transform loses information and cannot be undone.

## Definition

**Notation.** As on all pages of fast transforms: $n \ge 1$ is the transform length, over $\mathbb{C}$ the root is $\omega_n = e^{-2\pi i/n}$ (the sign of signal processing, FFTW and NumPy; CLRS uses $e^{+2\pi i/n}$), and over a commutative ring $R$, $\omega$ is a principal $n$-th [root of unity](/roots-of-unity/): $\omega^n = 1$ and $\sum_{j=0}^{n-1} \omega^{jk} = 0$ for $1 \le k \le n-1$. The forward transform is $X_k = \sum_j x_j \omega^{jk}$, without a factor, and the inverse carries the factor $1/n$.

**Input.** A commutative ring $R$ in which $n \cdot 1$ is a unit, a principal $n$-th root of unity $\omega \in R$, and a vector $X = (X_0, \ldots, X_{n-1}) \in R^n$.

**Output.** The vector $x \in R^n$ with $\mathrm{DFT}_\omega(x) = X$. It is

$$x_j = \frac{1}{n} \sum_{k=0}^{n-1} X_k\, \omega^{-jk}, \qquad 0 \le j \le n-1.$$

The [DFT page](/discrete-fourier-transform/) proves this formula from the definition of a principal root. In matrix form, with the [DFT matrix](/dft-matrix/) $F_n = (\omega^{jk})_{j,k}$, it says $F_n^{-1} = \frac{1}{n} F_n'$, where $F_n' = (\omega^{-jk})_{j,k}$. Over $\mathbb{C}$, $\omega_n^{-1} = \overline{\omega_n}$, so $F_n' = \overline{F_n}$ and $F_n^{-1} = \frac{1}{n} F_n^{H}$.

**When the inverse exists.** Let $\omega$ be a principal $n$-th root of unity in $R$. Then $F_n$ is invertible over $R$ if and only if $n \cdot 1$ is a unit in $R$.

*Proof.* If $n$ is a unit, the formula above is an inverse. Conversely, the entry $(j, m)$ of $F_n F_n'$ is $\sum_k \omega^{(j - m)k}$, which is $n$ when $j = m$ and $0$ otherwise, since $\omega$ is principal. So $F_n F_n' = nI$. Also $\omega^{-jk} = \omega^{((n - j) \bmod n) k}$, so $F_n'$ is $F_n$ with its rows permuted, and $\det F_n' = \pm \det F_n$. Taking determinants, $\pm (\det F_n)^2 = n^n$. If $F_n$ is invertible, $\det F_n$ is a unit, so $n^n$ is a unit, and then so is $n$. $\square$

**Cost model.** Additions (with subtractions) and multiplications in $R$ are counted separately, each at unit cost, as in the [real RAM](/real-ram/) for $R = \mathbb{C}$. Over $\mathbb{Z}/p\mathbb{Z}$ with $p$ below the word size, each ring operation is $O(1)$ steps of the [word RAM](/word-ram/). The final scaling costs $n$ multiplications by the constant $n^{-1}$, or none if the caller accepts $n x$ in place of $x$.

## Variants

There are four standard ways to turn a forward DFT routine into an inverse one. All of them are exact identities.

- **Inverse root.** Run the forward transform with $\omega^{-1}$ in place of $\omega$, then multiply by $n^{-1}$. Over a ring this is the usual choice: $\omega^{-1} = \omega^{n-1}$ and $n^{-1}$ are computed once, the latter by a [modular inverse](/modular-inverse/).
- **Index reversal.** $x_j = \frac{1}{n} Y_{(n - j) \bmod n}$ with $Y = \mathrm{DFT}_\omega(X)$. The same routine and the same table of [twiddle factors](/twiddle-factor/) serve both directions. This holds in each ring.
- **Conjugation.** Over $\mathbb{C}$, $x = \frac{1}{n}\, \overline{\mathrm{DFT}_\omega(\overline{X})}$. This costs $2n$ sign changes and no more.
- **Swap.** Over $\mathbb{C}$, let $s(a + bi) = b + ai$. Then $x = \frac{1}{n}\, s(\mathrm{DFT}_\omega(s(X)))$, applied entrywise. The swap moves no data in a split format with separate arrays for the real and the imaginary parts: one passes the two arrays in the other order.
- **Normalization.** The unitary convention puts $1/\sqrt{n}$ on both directions, and some libraries put $1/n$ on the forward transform instead. Only the product of the two factors is fixed: it must be $1/n$.
- **Unnormalized inverse.** In convolution, the scaling can be folded into another step. For example, [FFT polynomial multiplication](/fft-polynomial-multiplication/) can multiply one of the two inputs by $n^{-1}$ before the forward transform.

## Examples

**Over $\mathbb{C}$.** For $n = 4$, $\omega_4 = -i$, and $X = (10, -2 + 2i, -2, -2 - 2i)$, the transform of $(1, 2, 3, 4)$ on the [DFT page](/discrete-fourier-transform/). The formula with $\omega_4^{-1} = i$ gives

$$x_1 = \tfrac14 \bigl(10 + (-2 + 2i) i + (-2)(-1) + (-2 - 2i)(-i)\bigr) = \tfrac14 (10 - 2 - 2i + 2 - 2 + 2i) = 2,$$

and in the same way $x = (1, 2, 3, 4)$. The conjugation, reversal and swap methods give the same vector, checked by script.

**Over $\mathbb{Z}/17\mathbb{Z}$.** Let $\omega = 4$, a principal $4$-th root, and $X = (10, 7, 15, 6)$. By index reversal: $Y = \mathrm{DFT}_4(X) = (4, 16, 12, 8)$, reversed to $(Y_0, Y_3, Y_2, Y_1) = (4, 8, 12, 16)$, and multiplied by $4^{-1} = 13$ this is $(52, 104, 156, 208) \equiv (1, 2, 3, 4)$.

**Edge cases.** For $n = 1$ the inverse is the identity. For $n = 2$, $\omega = -1$ and $x = \bigl(\frac{X_0 + X_1}{2}, \frac{X_0 - X_1}{2}\bigr)$. The spike $X = (n, 0, \ldots, 0)$ comes from the constant $x = (1, \ldots, 1)$, and the constant $X = (1, \ldots, 1)$ comes from the impulse $x = (1, 0, \ldots, 0)$.

**When $n$ is not a unit.** In $\mathbb{Z}/16\mathbb{Z}$, $\omega = -1 = 15$ is a principal square root of unity, since $1 + 15 \equiv 0$. But $2$ is not a unit. The DFT $(x_0, x_1) \mapsto (x_0 + x_1, x_0 - x_1)$ sends both $(0, 8)$ and $(8, 0)$ to $(8, 8)$, so it cannot be inverted. Over $\mathbb{Z}$, the same map is one to one, but its image holds only the pairs of equal parity, so $(1, 0)$ has no preimage in $\mathbb{Z}^2$: one has to pass to $\mathbb{Q}$.

## Known algorithms

- **Direct sum.** Evaluate the formula by [Horner's rule](/horner-rule/) at each point $\omega^{-j}$: $n(n-1)$ additions and $n(n-1)$ multiplications, plus $n - 2$ multiplications for the powers $\omega^{-j}$ and $n$ for the scaling, so $\Theta(n^2)$.
- **[Inverse FFT](/inverse-fft/).** Any of the reductions in Variants applied to the [fast Fourier transform](/fast-fourier-transform/). For $n$ a power of two: $n \lg n$ additions and $\frac{n}{2}\lg n + n$ multiplications in $R$, the last $n$ for the scaling. The other FFTs, [mixed radix](/mixed-radix-fft/), [split radix](/split-radix-fft/), [Rader](/rader-fft/) and [Bluestein](/bluestein-fft/), invert in the same way.
- **General interpolation.** [Lagrange interpolation](/lagrange-interpolation/) at arbitrary points takes $\Theta(n^2)$ operations, and [fast interpolation](/fast-interpolation/) takes $O(M(n) \log n)$, where $M(n)$ is the cost of [polynomial multiplication](/polynomial-multiplication/). At the roots of unity the [Vandermonde matrix](/vandermonde-matrix/) has the explicit inverse $\frac{1}{n} F_n'$, which is why the special case is faster by a factor of $\log n$.

## Bounds

**Upper bound.** $O(n \log n)$ operations over $\mathbb{C}$ for each $n$, and over a ring $R$ whenever the forward transform has that cost. The reductions in Variants show that the costs of the forward and the inverse problem differ by at most $n$ multiplications and a permutation.

**Lower bounds.** $\Omega(n)$, since each output depends on each input. Morgenstern's $\Omega(n \log n)$ bound for linear algorithms whose constants have absolute value at most $1$ applies to the unnormalized inverse $n F_n^{-1} = F_n'$, whose determinant has absolute value $n^{n/2}$, as for $F_n$. For the normalized inverse his determinant argument gives nothing, because $|\det F_n^{-1}| = n^{-n/2} < 1$. No lower bound better than $\Omega(n)$ is known for general arithmetic circuits.

**Floating point.** Over $\mathbb{C}$ the problem is perfectly conditioned: $F_n / \sqrt n$ is unitary ([Parseval's theorem](/parseval-theorem/)), so the [condition number](/condition-number/) of $F_n^{-1}$ in the 2-norm is $1$. The inverse FFT has the same proved relative error bound as the forward FFT, $O(u \log n)$ in the 2-norm (Higham, Theorem 24.2), because it is the same computation with conjugate weights. When $n$ is a power of two, the final division by $n$ is exact in binary floating point unless it underflows.

## Reductions

- **Inverse to forward.** $\mathrm{IDFT}_\omega(X) = n^{-1}\, \mathrm{DFT}_{\omega^{-1}}(X)$, and $\mathrm{DFT}_{\omega^{-1}}(X)$ is $\mathrm{DFT}_\omega(X)$ with the indices $1, \ldots, n-1$ reversed.
- **Forward to inverse.** In the other direction, $\mathrm{DFT}_\omega(x) = n \cdot \mathrm{IDFT}_{\omega^{-1}}(x)$.
- **Interpolation.** The IDFT is interpolation at the $n$ points $\omega^k$, a special case of [polynomial interpolation](/polynomial-interpolation/) at distinct points. Over a ring one needs the stronger condition that $\omega$ is principal and $n$ is a unit, not only that the points are distinct.

## Applications

- **Multiplication.** The last step of [FFT polynomial multiplication](/fft-polynomial-multiplication/), of [convolution via FFT](/convolution-via-fft/) and of [Schönhage-Strassen multiplication](/schonhage-strassen-multiplication/) is an inverse transform of the pointwise product, by the [convolution theorem](/convolution-theorem/).
- **Synthesis.** Building a signal from its spectrum, for filtering in the frequency domain, for [trigonometric interpolation](/trigonometric-interpolation/), and for the overlap methods of the [short-time Fourier transform](/short-time-fourier-transform/).
- **Data transmission.** Weinstein and Ebert (1971) proposed to build a frequency-division multiplexed signal by an inverse DFT at the transmitter and to separate it by a DFT at the receiver.
- **Correlation.** The [autocorrelation](/autocorrelation/) and the [cross-correlation](/cross-correlation/) are inverse transforms of products of spectra.

## References
