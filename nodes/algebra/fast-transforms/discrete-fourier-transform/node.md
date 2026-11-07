---
tag: 6GT3DW
kind: problem
slug: discrete-fourier-transform
name: Discrete Fourier transform
aliases:
- DFT
- finite Fourier transform
area: algebra/fast-transforms
level: core
summary: Given x_0, ..., x_(n-1) and a principal n-th root of unity ω, compute X_k = sum over j of x_j ω^(jk) for each k; the direct method takes Θ(n^2) ring operations.
model: real-ram
complexity:
  vars: {n: the transform length}
  time: {worst: O(n log n)}
prereqs: [roots-of-unity, polynomial-evaluation, asymptotic-notation]
see_also: [fast-fourier-transform, inverse-discrete-fourier-transform, dft-matrix, fft-summation-lemma, convolution-theorem, number-theoretic-transform, bluestein-fft, discrete-time-fourier-transform]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Section 30.2, The DFT and FFT (the definition with the root e^(2πi/n), the lemmas on roots of unity, and the inverse DFT)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 8, Section 8.2, The Discrete Fourier Transform and the Fast Fourier Transform (roots of unity in a ring, the DFT as evaluation, the inverse)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1, Section 1.1, Matrix Notation and Algorithms (the DFT matrix and its properties)
  - paper: doi:10.1145/321752.321761
    title: Jacques Morgenstern, Note on a lower bound on the linear complexity of the fast Fourier transform, Journal of the ACM 20(2), 1973
    locator: pp. 305 to 306 (the Ω(n log n) bound for linear algorithms with bounded constants)
  - paper: doi:10.1090/S0025-5718-1965-0178586-1
    title: James W. Cooley and John W. Tukey, An algorithm for the machine calculation of complex Fourier series, Mathematics of Computation 19(90), 1965
    locator: pp. 297 to 301
---

The discrete Fourier transform (DFT) maps a sequence $x_0, \ldots, x_{n-1}$ to the sequence $X_k = \sum_{j=0}^{n-1} x_j \omega^{jk}$, where $\omega$ is a principal $n$-th [root of unity](/roots-of-unity/). Over the complex numbers, $\omega = e^{-2\pi i/n}$ and $X_k$ measures how much of the frequency $k$ is in the data. In the language of polynomials, the DFT is the [evaluation](/polynomial-evaluation/) of $x_0 + x_1 t + \cdots + x_{n-1} t^{n-1}$ at the $n$ powers of $\omega$. The direct method takes $\Theta(n^2)$ operations, and the [fast Fourier transform](/fast-fourier-transform/) does it in $O(n \log n)$, which makes the DFT one of the most used computations in science and engineering.

## In plain words

Think of a list of numbers as a sound, sampled at equal steps. Each sound of that length can be built in exactly one way from a fixed set of pure waves: a constant, a wave with one full turn over the list, a wave with two turns, and so on. The discrete Fourier transform finds how much of each pure wave is in the sound, and at what offset.

Each output number is a weighted sum of all the input numbers. The weights are points that walk around a circle at an even speed, faster for higher waves. Done directly, this costs one multiplication for each pair of input and output, so the work grows with the square of the length. The fast Fourier transform gets the same answer with far less work. The transform can also be undone: from the wave amounts you get back the original list.

## Definition

**Notation.** These are the conventions of all pages on fast transforms. The transform length is $n \ge 1$. Over the complex numbers, $\omega_n = e^{-2\pi i/n}$. The minus sign in the forward transform is the convention of signal processing and of FFTW and NumPy. Some texts, among them CLRS, use $e^{+2\pi i/n}$. Each statement on these pages holds for both choices, because both are principal $n$-th roots of unity, and changing the sign only swaps the forward and the inverse transform up to the factor $1/n$.

**Principal root of unity.** Let $R$ be a commutative ring with $1$. An element $\omega \in R$ is a *principal $n$-th root of unity* if $\omega^n = 1$ and

$$\sum_{j=0}^{n-1} \omega^{jk} = 0 \quad \text{for each } k \text{ with } 1 \le k \le n-1.$$

In $\mathbb{C}$, and in each field, this holds exactly when $\omega$ has order $n$ (see the [summation lemma](/fft-summation-lemma/)). In a ring with zero divisors it is stronger than order $n$. Von zur Gathen and Gerhard call this stronger notion *primitive*.

**Input.** A commutative ring $R$, a length $n \ge 1$, a principal $n$-th root of unity $\omega \in R$, and a vector $x = (x_0, \ldots, x_{n-1}) \in R^n$.

**Output.** The vector $X = (X_0, \ldots, X_{n-1}) \in R^n$ with

$$X_k = \sum_{j=0}^{n-1} x_j \, \omega^{jk}, \qquad 0 \le k \le n-1.$$

We write $X = \mathrm{DFT}_\omega(x)$, or $X = F_n x$ with the [DFT matrix](/dft-matrix/) $F_n = (\omega^{jk})_{j,k}$.

**The inverse.** If $n$ is a unit in $R$, then $\omega^{-1} = \omega^{n-1}$ is also a principal $n$-th root of unity, and

$$x_j = \frac{1}{n} \sum_{k=0}^{n-1} X_k \, \omega^{-jk}, \qquad 0 \le j \le n-1.$$

*Proof.* Put the definition of $X_k$ into the right side and change the order of the sums: $\frac{1}{n}\sum_{m} x_m \sum_{k} \omega^{(m-j)k}$. If $m = j$, the inner sum is $n$. If $m \ne j$, let $r = (m - j) \bmod n$, so $1 \le r \le n-1$ and $\omega^{(m-j)k} = \omega^{rk}$ since $\omega^n = 1$. The inner sum is then $0$ by the definition of a principal root. So the right side is $\frac{1}{n} \cdot n x_j = x_j$. $\square$

The problem of computing $x$ from $X$ is the [inverse discrete Fourier transform](/inverse-discrete-fourier-transform/).

**Polynomial form.** With $A(t) = \sum_j x_j t^j$, the output is $X_k = A(\omega^k)$. So the DFT turns the coefficient form of a polynomial of degree less than $n$ into its [point-value form](/point-value-representation/) at the points $1, \omega, \ldots, \omega^{n-1}$, and the inverse DFT is [interpolation](/polynomial-interpolation/) at those points.

**Cost model.** Costs are counted in arithmetic operations of $R$: additions (and subtractions) and multiplications, each of unit cost, as in the [real RAM](/real-ram/) for $R = \mathbb{C}$. Over $\mathbb{Z}/p\mathbb{Z}$ with $p$ less than the word size, each ring operation is $O(1)$ operations of the [word RAM](/word-ram/), so the counts carry over.

## Variants

- **Inverse transform.** Compute $x$ from $X$. By the formula above, $x_j = \frac{1}{n} Y_{(n-j) \bmod n}$ where $Y = \mathrm{DFT}_\omega(X)$, so each forward algorithm also inverts. See [inverse DFT](/inverse-discrete-fourier-transform/) and [inverse FFT](/inverse-fft/).
- **Normalization.** The *unitary* DFT multiplies by $1/\sqrt{n}$ in both directions, so that $F_n/\sqrt{n}$ is a unitary matrix over $\mathbb{C}$ ([Parseval's theorem](/parseval-theorem/)).
- **Number-theoretic transform.** $R = \mathbb{Z}/p\mathbb{Z}$ with a prime $p \equiv 1 \pmod n$, for example $p = 998244353 = 119 \cdot 2^{23} + 1$ with the [primitive root](/primitive-root/) $3$. The arithmetic is exact. See [number-theoretic transform](/number-theoretic-transform/).
- **Real input.** If each $x_j$ is real and $\omega = \omega_n$, then $X_{n-k} = \overline{X_k}$, so half the output is redundant. See [real-valued FFT](/real-valued-fft/).
- **Real transforms.** The [discrete cosine transform](/discrete-cosine-transform/), the [discrete sine transform](/discrete-sine-transform/) and the [discrete Hartley transform](/discrete-hartley-transform/) are real cousins of the DFT. The [Walsh-Hadamard transform](/walsh-hadamard-transform/) is the DFT over the group $(\mathbb{Z}/2\mathbb{Z})^m$.
- **Several dimensions.** The DFT of an $n_1 \times n_2$ array applies the DFT along each axis. See [multidimensional FFT](/multidimensional-fft/).
- **A few outputs.** One coefficient $X_k$ costs $O(n)$ with the [Goertzel algorithm](/goertzel-algorithm/). When only $s$ coefficients are large, the [sparse Fourier transform](/sparse-fourier-transform/) is faster than $n$.
- **Other points.** Evaluation at frequencies that are not multiples of $1/n$ is the [nonuniform DFT](/nonuniform-discrete-fourier-transform/). The [chirp z-transform](/bluestein-fft/) evaluates at points $a z^k$ on a spiral.

## Examples

**A complex transform.** For $n = 4$, $\omega_4 = e^{-2\pi i/4} = -i$, and $x = (1, 2, 3, 4)$:

$$X_0 = 10, \quad X_1 = 1 - 2i - 3 + 4i = -2 + 2i, \quad X_2 = 1 - 2 + 3 - 4 = -2, \quad X_3 = 1 + 2i - 3 - 4i = -2 - 2i.$$

The input is real, and $X_3 = \overline{X_1}$, as the real-input symmetry says.

**A box.** For $n = 8$ and $x = (1, 1, 1, 1, 0, 0, 0, 0)$, the output is $X_0 = 4$, $X_2 = X_4 = X_6 = 0$, $X_1 = 1 - (1 + \sqrt{2})i$, $X_3 = 1 - (\sqrt{2} - 1)i$, and $X_5, X_7$ are the conjugates of $X_3, X_1$. The even outputs vanish because $X_{2m} = \sum_{j=0}^{3} \omega_4^{jm}$, a full sum of fourth roots of unity.

**An exact transform.** In $\mathbb{Z}/17\mathbb{Z}$, the powers of $4$ are $1, 4, 16, 13, 1$, so $\omega = 4$ has order $4$, and it is a principal $4$-th root of unity because $\mathbb{Z}/17\mathbb{Z}$ is a field. For $x = (1, 2, 3, 4)$, $\mathrm{DFT}_4(x) = (10, 7, 15, 6)$. The inverse uses $4^{-1} = 13$ and $\omega^{-1} = 13$: $\mathrm{DFT}_{13}(10, 7, 15, 6) = (4, 8, 12, 16)$, and $13 \cdot (4, 8, 12, 16) \equiv (1, 2, 3, 4)$.

**Special inputs.** The impulse $x = (0, 1, 0, 0)$ gives $X_k = \omega^k$, here $(1, 4, 16, 13)$ over $\mathbb{Z}/17\mathbb{Z}$. The constant $x = (1, 1, 1, 1)$ gives $(4, 0, 0, 0)$. For $n = 1$ the DFT is the identity. For $n = 2$, $\omega = -1$ and $X = (x_0 + x_1, x_0 - x_1)$.

**A non-example.** In $\mathbb{Z}/15\mathbb{Z}$, $4^2 = 16 \equiv 1$, so $4$ has order $2$. But $1 + 4 = 5 \ne 0$, so $4$ is not a principal square root of unity, because $4 - 1 = 3$ is a zero divisor. The map $(x_0, x_1) \mapsto (x_0 + x_1, x_0 + 4x_1)$ sends $(5, 10)$ to $(15, 45) \equiv (0, 0)$, so it cannot be inverted.

## Known algorithms

- **Direct evaluation.** Compute each $X_k$ by [Horner's rule](/horner-rule/) at $\omega^k$: $n(n-1)$ additions and $n(n-1)$ multiplications, plus $n - 2$ multiplications for the powers $\omega^k$, so $\Theta(n^2)$.
- **[Fast Fourier transform](/fast-fourier-transform/)** (radix 2, Cooley and Tukey). For $n$ a power of two: $\frac{n}{2}\lg n$ multiplications and $n \lg n$ additions in $R$. The [iterative FFT](/iterative-fft/) runs in place after a [bit-reversal permutation](/bit-reversal-permutation/).
- **[Mixed-radix FFT](/mixed-radix-fft/).** For $n = n_1 n_2$: $O(n \sum_i p_i)$ operations, where the $p_i$ are the prime factors of $n$ with multiplicity.
- **[Split-radix FFT](/split-radix-fft/).** For $n$ a power of two, with the lowest classical count of real operations for complex data, $4n \lg n - 6n + 8$ for $n \ge 2$.
- **[Good-Thomas prime-factor FFT](/chinese-remainder-theorem-fft/).** For $n = n_1 n_2$ with $\gcd(n_1, n_2) = 1$, with no twiddle factors.
- **[Rader's algorithm](/rader-fft/).** For prime $n$, through a cyclic convolution of length $n - 1$.
- **[Bluestein's algorithm](/bluestein-fft/).** For each $n$, through a linear convolution of length $2n - 1$, in $O(n \log n)$ over $\mathbb{C}$.
- **[Winograd Fourier transform](/winograd-fourier-transform/).** Small lengths with few multiplications, nested by the prime-factor map.

## Bounds

**Upper bound.** Over $\mathbb{C}$, each length $n$ has an algorithm with $O(n \log n)$ arithmetic operations: the radix-2 FFT for powers of two, and Bluestein's reduction for the other lengths. Over a ring $R$, the radix-2 FFT gives $O(n \log n)$ when $n$ is a power of two and a principal $n$-th root exists. Bluestein's reduction needs more roots of unity, which a given finite ring may lack.

**Lower bounds.** Each output depends on each input, and there are $n$ outputs, so $\Omega(n)$ operations are needed. Morgenstern (1973) proved $\Omega(n \log n)$ for *linear* algorithms over $\mathbb{C}$ (straight-line programs of additions and multiplications by constants) whose constants have absolute value at most $1$. The proof follows determinants: a step $u = a v + b w$ with $|a|, |b| \le 1$ at most doubles the largest absolute value of a determinant made from the linear forms computed so far, and $|\det F_n| = n^{n/2}$ because $F_n \overline{F_n}^{T} = nI$. So at least $\frac{n}{2}\lg n$ such steps are needed. The FFT is such an algorithm, so it is optimal in that model up to a constant factor. For general arithmetic circuits, with unbounded constants, no lower bound better than $\Omega(n)$ is known. This is a well-known open problem.

**Exact counts.** For $n = 2^m$ and complex input, the smallest known number of real additions and multiplications is $\frac{34}{9} n \lg n + O(n)$, from the modified split radix of Johnson and Frigo (2007). No matching lower bound is known.

## Reductions

- **Convolution to DFT.** By the [convolution theorem](/convolution-theorem/), a cyclic [convolution](/convolution/) of length $n$ costs three DFTs of length $n$ and $n$ pointwise products. See [convolution via FFT](/convolution-via-fft/).
- **DFT to convolution.** Bluestein writes a DFT of any length $n$ as a linear convolution of length about $2n$. Rader writes a DFT of prime length $p$ as a cyclic convolution of length $p - 1$.
- **Inverse to forward.** The inverse DFT is a forward DFT, a reversal of the indices $1, \ldots, n-1$, and a division by $n$, as in Variants.
- **Multipoint evaluation.** The DFT is [multipoint evaluation](/multipoint-evaluation/) at the points $\omega^k$. For general points, the best known methods take $O(M(n) \log n)$, where $M(n)$ is the cost of [polynomial multiplication](/polynomial-multiplication/).

## Applications

- **Fast multiplication.** [FFT polynomial multiplication](/fft-polynomial-multiplication/) and [Schönhage-Strassen multiplication](/schonhage-strassen-multiplication/) of integers.
- **Signal processing.** Spectral analysis, the [short-time Fourier transform](/short-time-fourier-transform/), fast filtering with long [FIR filters](/fir-filter/), and [cross-correlation](/cross-correlation/).
- **Images and compression.** Image filtering, [phase correlation](/phase-correlation/), and the DCT of [JPEG compression](/jpeg-compression/).
- **Numerical methods.** Spectral methods for differential equations, fast solvers for the [Poisson equation](/poisson-equation/), and [trigonometric interpolation](/trigonometric-interpolation/).
- **Quantum computing.** The [quantum Fourier transform](/quantum-fourier-transform/) is the unitary DFT on the amplitudes of a state.

## References
