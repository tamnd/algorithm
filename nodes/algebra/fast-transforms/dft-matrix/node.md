---
tag: CQS8J6
kind: concept
slug: dft-matrix
name: DFT matrix
aliases:
- Fourier matrix
- Vandermonde matrix of roots of unity
area: algebra/fast-transforms
level: core
summary: The n-by-n matrix F_n with entries ω^(jk), a Vandermonde matrix of the powers of a principal n-th root of unity; multiplying a vector by it computes the DFT.
prereqs: [discrete-fourier-transform, vandermonde-matrix, matrix-vector-multiplication]
see_also: [fft-summation-lemma, fast-fourier-transform, kronecker-product, bit-reversal-permutation, butterfly-operation, convolution-theorem, parseval-theorem, inverse-discrete-fourier-transform]
sources:
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1, Section 1.1, Matrix Notation and Algorithms (the matrix F_n and its properties), Section 1.3, The Cooley-Tukey Factorization, and Section 1.5, Bit Reversal and Transposition
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Section 30.2 (the DFT as the product with the Vandermonde matrix V_n, and the theorem on the entries of its inverse)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 21, Section 21.1, The discrete Fourier transform, and Chapter 22, Section 22.3, Correlation, convolution, and circulant matrices
  - paper: doi:10.1109/TAU.1972.1162342
    title: James H. McClellan and Thomas W. Parks, Eigenvalue and eigenvector decomposition of the discrete Fourier transform, IEEE Transactions on Audio and Electroacoustics 20(1), 1972
    locator: pp. 66 to 74 (the eigenvalues of the unitary DFT matrix and their multiplicities)
---

The DFT matrix $F_n$ is the $n \times n$ matrix with entry $\omega^{jk}$ in row $j$ and column $k$, for $0 \le j, k \le n-1$, where $\omega$ is a principal $n$-th [root of unity](/roots-of-unity/). The product $F_n x$ is the [discrete Fourier transform](/discrete-fourier-transform/) of $x$. It is the [Vandermonde matrix](/vandermonde-matrix/) of the points $1, \omega, \ldots, \omega^{n-1}$, its inverse is $\frac{1}{n}$ times the same matrix for $\omega^{-1}$, and over $\mathbb{C}$ the scaled matrix $F_n/\sqrt{n}$ is unitary. The [fast Fourier transform](/fast-fourier-transform/) is a factorization of $F_n$ into $\lg n$ sparse factors.

## In plain words

A matrix is a table of numbers that turns one list into another: each output is a weighted sum of all inputs, and row number such-and-such holds the weights for output number such-and-such. The DFT matrix is the table for the Fourier transform. Its rows are the pure waves, sampled at the points of the list: the first row is all ones, the next row turns once around a circle, the row after that turns twice, and so on.

The table has strong structure. Different rows are at right angles to each other, so the table is easy to undo: the reverse table is the same table with the turning direction flipped, divided by the size. The table also breaks into a few very sparse tables, one per halving step. Using those sparse tables one after the other is the fast Fourier transform.

## The idea

**Notation.** We use the conventions of the [DFT page](/discrete-fourier-transform/): $n$ is the transform length, and over $\mathbb{C}$, $\omega = \omega_n = e^{-2\pi i/n}$. Over a commutative ring $R$, $\omega$ is a principal $n$-th root of unity. Rows and columns are numbered from $0$.

**Definition.**

$$F_n = \left(\omega^{jk}\right)_{0 \le j, k \le n-1}, \qquad (F_n x)_k = \sum_{j=0}^{n-1} \omega^{kj} x_j = X_k.$$

Since $\omega^{jk} = \omega^{kj}$, the matrix is symmetric: $F_n^{T} = F_n$. Row $k$ is the sequence $(\omega^k)^j$, so $F_n$ is the Vandermonde matrix $V(1, \omega, \ldots, \omega^{n-1})$.

**The inverse.** Let $G_n = (\omega^{-jk})$. The entry $(j, m)$ of $F_n G_n$ is $\sum_k \omega^{(j-m)k}$, which is $n$ if $j = m$ and $0$ otherwise, by the [summation lemma](/fft-summation-lemma/) applied to a principal root. So $F_n G_n = nI$. If $n$ is a unit of $R$, then

$$F_n^{-1} = \frac{1}{n} G_n = \frac{1}{n}\left(\omega^{-jk}\right).$$

Over $\mathbb{C}$, $\omega^{-1} = \overline{\omega}$, so $G_n = \overline{F_n} = F_n^{*}$ (the conjugate transpose, since $F_n$ is symmetric). Then $\left(F_n/\sqrt{n}\right)^{*} \left(F_n/\sqrt{n}\right) = I$: the matrix $F_n/\sqrt{n}$ is unitary. Its 2-norm condition number is $1$. Each of its columns has length $1$, and the transform keeps lengths up to the factor $\sqrt{n}$, which is [Parseval's theorem](/parseval-theorem/).

**The square and the fourth power.** The entry $(j, m)$ of $F_n^2$ is $\sum_k \omega^{(j+m)k}$, which is $n$ if $j + m \equiv 0 \pmod n$ and $0$ otherwise. So $F_n^2 = n P$, where $P$ is the permutation matrix that sends index $j$ to $(-j) \bmod n$: it fixes $0$ and reverses $1, \ldots, n-1$. Since $P^2 = I$, $F_n^4 = n^2 I$. Over $\mathbb{C}$ this means that each eigenvalue $\lambda$ of $F_n/\sqrt{n}$ satisfies $\lambda^4 = 1$, so $\lambda \in \{1, -1, i, -i\}$. McClellan and Parks (1972) found the multiplicities.

**The determinant.** Over $\mathbb{C}$, $F_n F_n^{*} = nI$ gives $|\det F_n|^2 = n^n$, so $|\det F_n| = n^{n/2}$. Morgenstern's lower bound for the FFT uses this value (see [the DFT problem](/discrete-fourier-transform/)). As a Vandermonde matrix, $\det F_n = \prod_{0 \le j < k \le n-1} (\omega^k - \omega^j)$. This is a unit of $R$ exactly when the matrix can be inverted, which the formula for $F_n^{-1}$ shows whenever $n$ is a unit.

**The Cooley-Tukey factorization.** Let $n = 2m$. Let $\Pi_n$ be the permutation matrix that puts the even-indexed entries of a vector first and the odd-indexed entries after them, let $\Omega_m = \mathrm{diag}(1, \omega_n, \ldots, \omega_n^{m-1})$, and let

$$B_n = \begin{pmatrix} I_m & \Omega_m \\ I_m & -\Omega_m \end{pmatrix}.$$

Then

$$F_n = B_n \, (I_2 \otimes F_m) \, \Pi_n,$$

where $I_2 \otimes F_m = \mathrm{diag}(F_m, F_m)$ is a [Kronecker product](/kronecker-product/). *Proof.* For $0 \le k \le m - 1$, split the sum $X_k = \sum_j \omega_n^{jk} x_j$ into even $j = 2r$ and odd $j = 2r + 1$. By the [cancellation lemma](/fft-cancellation-lemma/), $\omega_n^{2rk} = \omega_m^{rk}$, so $X_k = E_k + \omega_n^k O_k$, where $E = F_m (x_0, x_2, \ldots)$ and $O = F_m (x_1, x_3, \ldots)$. Since $\omega_m^{r(k+m)} = \omega_m^{rk}$ and $\omega_n^{k + m} = -\omega_n^k$, $X_{k+m} = E_k - \omega_n^k O_k$. These are the rows of $B_n (I_2 \otimes F_m) \Pi_n x$. $\square$ Applied again to each $F_m$, this gives, for $n = 2^t$,

$$F_n = A_t A_{t-1} \cdots A_1 \, P_n, \qquad A_q = I_{n/2^q} \otimes B_{2^q},$$

where $P_n$ is the [bit-reversal permutation](/bit-reversal-permutation/) and each $A_q$ has two nonzero entries in each row: one stage of [butterflies](/butterfly-operation/). Multiplying by the $t = \lg n$ sparse factors one after the other costs $O(n \log n)$. This is the [iterative FFT](/iterative-fft/), and other orders of the same factors give the other FFT frameworks in Van Loan's book.

**Circulant matrices.** A circulant matrix $C$ has entry $c_{(j - k) \bmod n}$ in row $j$ and column $k$, so $Cx$ is the cyclic [convolution](/convolution/) of $c$ and $x$. The [convolution theorem](/convolution-theorem/) in matrix form is

$$C = F_n^{-1} \, \mathrm{diag}(F_n c) \, F_n.$$

So the DFT matrix diagonalizes every circulant matrix at once, and the eigenvalues of $C$ are the entries of $F_n c$.

## Examples

**Small sizes over $\mathbb{C}$.** $F_1 = (1)$ and $F_2 = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$. With $\omega_4 = -i$,

$$F_4 = \begin{pmatrix} 1 & 1 & 1 & 1 \\ 1 & -i & -1 & i \\ 1 & -1 & 1 & -1 \\ 1 & i & -1 & -i \end{pmatrix}.$$

Row $2$ alternates in sign: it measures the fastest wave. Rows $1$ and $3$ are complex conjugates. $|\det F_4| = 16 = 4^{4/2}$, and $|\det F_8| = 4096 = 8^{4}$.

**Over $\mathbb{Z}/17\mathbb{Z}$.** With $\omega = 4$,

$$F_4 = \begin{pmatrix} 1 & 1 & 1 & 1 \\ 1 & 4 & 16 & 13 \\ 1 & 16 & 1 & 16 \\ 1 & 13 & 16 & 4 \end{pmatrix}, \qquad F_4^2 = \begin{pmatrix} 4 & 0 & 0 & 0 \\ 0 & 0 & 0 & 4 \\ 0 & 0 & 4 & 0 \\ 0 & 4 & 0 & 0 \end{pmatrix} = 4P,$$

and $F_4^4 = 16 I$. The inverse is $4^{-1} = 13$ times the matrix with $\omega^{-1} = 13$ in place of $4$.

**The factorization for $n = 4$.** Here $\Pi_4$ reorders $(x_0, x_1, x_2, x_3)$ to $(x_0, x_2, x_1, x_3)$, which is also the bit-reversal order for $n = 4$, $\Omega_2 = \mathrm{diag}(1, \omega)$, and $F_4 = B_4 \, \mathrm{diag}(F_2, F_2) \, \Pi_4$. Over $\mathbb{Z}/17\mathbb{Z}$ with $\omega = 4$, the product of the three matrices is the matrix $F_4$ above.

**A non-example.** For $\omega = 1$ and $n \ge 2$, the matrix of all ones has rank $1$ and no inverse. The definition needs a principal root: an element of order $n$ in a field, or the stronger condition of the [DFT page](/discrete-fourier-transform/) in a ring with zero divisors.

## Where it is used

- **Every FFT is a factorization of $F_n$.** The radix-2 [FFT](/fast-fourier-transform/), the [mixed-radix FFT](/mixed-radix-fft/), the [split-radix FFT](/split-radix-fft/) and the [Good-Thomas algorithm](/chinese-remainder-theorem-fft/) are different ways to write $F_n$ as a product of sparse matrices and permutations.
- **The inverse transform.** $F_n^{-1} = \frac{1}{n}\overline{F_n}$ over $\mathbb{C}$ is the basis of the [inverse DFT](/inverse-discrete-fourier-transform/) and the [inverse FFT](/inverse-fft/).
- **Fast circulant and Toeplitz products.** The diagonalization of circulant matrices gives $O(n \log n)$ products with circulant matrices, and with Toeplitz matrices after embedding them in a circulant matrix of twice the size; see [convolution via FFT](/convolution-via-fft/).
- **Polynomial arithmetic.** As a Vandermonde matrix, $F_n$ turns coefficients into values at the powers of $\omega$, the step of the [evaluation-interpolation paradigm](/evaluation-interpolation-paradigm/) in [FFT polynomial multiplication](/fft-polynomial-multiplication/).
- **Numerical stability.** Because $F_n/\sqrt{n}$ is unitary, the DFT does not amplify errors in the 2-norm. This is one reason why the FFT is accurate in [floating point](/floating-point-arithmetic/).
- **The Walsh-Hadamard matrix.** The Hadamard matrix $H_{2^m} = F_2 \otimes \cdots \otimes F_2$ is the analogue of $F_n$ for the group $(\mathbb{Z}/2\mathbb{Z})^m$, and the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/) is its factorization.

## References
