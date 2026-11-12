---
tag: 56ZDC1
kind: definition
slug: orthogonal-transform
name: Orthogonal transform
aliases:
- unitary transform
- orthonormal transform
area: compression-and-coding/transforms-for-compression
level: intro
summary: Linear transform with an orthogonal matrix, which preserves energy and inverts by transposition.
see_also: [karhunen-loeve-transform, discrete-cosine-transform, walsh-hadamard-transform, dft-matrix, householder-reflections, perfect-reconstruction, transform-coding, energy-compaction]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Chapter 2 (orthogonal matrices and the norms they keep) and Section 5.1 (Householder and Givens transformations)
  - book: isbn:9780132119139
    title: N. S. Jayant and Peter Noll, Digital Coding of Waveforms, Prentice-Hall, 1984
    locator: Chapter 12, Transform Coding (unitary transforms, energy preservation and the equal error in the two domains)
  - book: isbn:9780792391814
    title: Allen Gersho and Robert M. Gray, Vector Quantization and Signal Compression, Kluwer, 1992
    locator: Chapter 8, Bit Allocation and Transform Coding
  - paper: doi:10.1109/79.952802
    title: Vivek K. Goyal, Theoretical foundations of transform coding, IEEE Signal Processing Magazine 18(5), 2001
    locator: pp. 9 to 21 (the standard model of transform coding and the role of orthogonality)
---

An orthogonal transform maps a block of $N$ real samples $x$ to the coefficients $y = Ax$, where $A$ is a real $N \times N$ matrix with $A^{\mathsf T} A = I$. In the complex case the matrix is unitary, $A^{*} A = I$, and the map is called a unitary transform. Such a map keeps lengths, angles and energy, and it is undone by the transpose. This is why [transform coding](/transform-coding/) uses it: an error made on the coefficients comes back to the samples with the same energy.

## Definition

Let $N \ge 1$. A real matrix $A \in \mathbb{R}^{N \times N}$ is *orthogonal* if

$$A^{\mathsf T} A = I_N .$$

A complex matrix $A \in \mathbb{C}^{N \times N}$ is *unitary* if $A^{*} A = I_N$, where $A^{*}$ is the conjugate transpose. The *orthogonal transform* (or unitary transform) with matrix $A$ is the linear map $x \mapsto y = Ax$. The entries of $y$ are the *coefficients*. Row $k$ of $A$ is the $k$-th *basis vector* $a_k$, and $y_k = \langle a_k, x \rangle$. For a square matrix, $A^{\mathsf T} A = I$ is the same as $A A^{\mathsf T} = I$, so the rows and the columns are both orthonormal bases of $\mathbb{R}^N$.

These facts follow from the definition. We write them for the real case; for the complex case replace ${}^{\mathsf T}$ by ${}^{*}$.

1. **Inverse by transpose.** $A^{-1} = A^{\mathsf T}$, so $x = A^{\mathsf T} y = \sum_k y_k a_k$. The inverse costs no more than the forward map.
2. **Energy is kept (Parseval).** $\|Ax\|^2 = x^{\mathsf T} A^{\mathsf T} A x = x^{\mathsf T} x = \|x\|^2$. In the same way $\langle Ax, Az \rangle = \langle x, z \rangle$ for all $x, z$.
3. **Squared error is kept.** If the decoder changes the coefficients to $\hat y$ and computes $\hat x = A^{\mathsf T} \hat y$, then $x - \hat x = A^{\mathsf T}(y - \hat y)$, so by fact 2 applied to $A^{\mathsf T}$, $\|x - \hat x\|^2 = \|y - \hat y\|^2$. The mean squared error of a coder is the same in the two domains.
4. **Total variance is kept.** If $x$ is a random vector with covariance matrix $R_x$, then $y$ has covariance $R_y = A R_x A^{\mathsf T}$, and $\operatorname{tr} R_y = \operatorname{tr}(R_x A^{\mathsf T} A) = \operatorname{tr} R_x$. A transform can move variance between coefficients, but it cannot create or destroy it.
5. **Determinant.** $\det(A)^2 = \det(A^{\mathsf T} A) = 1$, so $\det A = \pm 1$ (and $|\det A| = 1$ in the complex case). The map keeps volume, so it maps a cube of quantization cells to a rotated cube of the same size.

Fact 3 is the reason that coders quantize in the transform domain and still measure the error in the signal domain: the bit allocation can work on each coefficient alone, and the sum of the coefficient errors is the signal error. Fact 4 is the reason that [energy compaction](/energy-compaction/) is a question of how the variance is distributed, not of how much there is.

A matrix with orthogonal rows of equal length $c$ ($A^{\mathsf T} A = c^2 I$) is a scaled orthogonal transform. Coders often use such a matrix and fold the factor $c$ into the quantizer step. The facts above then hold with a factor $c^2$ on each energy.

## Examples and non-examples

**Examples.**

- The identity, and each permutation matrix. These keep energy but move no variance between samples.
- A rotation of the plane, $A = \begin{pmatrix} \cos\theta & \sin\theta \\ -\sin\theta & \cos\theta \end{pmatrix}$. With $\theta = \pi/4$ it maps the pair $(x_1, x_2)$ to the scaled sum and difference $((x_1 + x_2)/\sqrt 2, (x_2 - x_1)/\sqrt 2)$, which is the 2-point [Karhunen-Loève transform](/karhunen-loeve-transform/) of a pair with equal variances.
- A Householder reflection $I - 2vv^{\mathsf T}/(v^{\mathsf T} v)$ and a Givens rotation; see [Householder reflections](/householder-reflections/) and [Givens rotations](/givens-rotations/).
- The orthonormal [Walsh-Hadamard transform](/walsh-hadamard-transform/) $H_N / \sqrt N$, the unitary DFT $F_N / \sqrt N$ (see [DFT matrix](/dft-matrix/)), the orthonormal [discrete cosine transform](/discrete-cosine-transform/), and the orthonormal [Haar wavelet transform](/haar-wavelet-transform/).
- The [Karhunen-Loève transform](/karhunen-loeve-transform/), whose rows are orthonormal eigenvectors of a covariance matrix.

**A worked example.** Take the orthonormal 4-point Walsh-Hadamard matrix in Sylvester order,

$$A = \frac12 \begin{pmatrix} 1 & 1 & 1 & 1 \\ 1 & -1 & 1 & -1 \\ 1 & 1 & -1 & -1 \\ 1 & -1 & -1 & 1 \end{pmatrix}, \qquad x = (4, 2, -1, 3).$$

Then $y = Ax = (4, -1, 2, 3)$, and $\|x\|^2 = \|y\|^2 = 30$. Quantize each coefficient to the nearest multiple of 2, with ties rounded up: $\hat y = (4, 0, 2, 4)$. The error in the coefficients is $(0, -1, 0, -1)$, with energy 2. The decoder computes $\hat x = A^{\mathsf T} \hat y = (5, 1, -1, 3)$. The error in the samples is $(-1, 1, 0, 0)$, also with energy 2, as fact 3 says.

**Non-examples.**

- The unnormalized Hadamard matrix $\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$. Its rows are orthogonal, but $A^{\mathsf T} A = 2I$. It doubles the energy, and its inverse is $A^{\mathsf T}/2$, not $A^{\mathsf T}$. The DFT matrix $F_N$ without the factor $1/\sqrt N$ fails in the same way, with $F_N^{*} F_N = N I$.
- The prediction matrix $P = \begin{pmatrix} 1 & 0 \\ -1 & 1 \end{pmatrix}$, which maps $(x_1, x_2)$ to $(x_1, x_2 - x_1)$. It is invertible with $\det P = 1$, but it is not orthogonal: $P^{\mathsf T} P = \begin{pmatrix} 2 & -1 \\ -1 & 1 \end{pmatrix}$. An error $(0.5, 0.5)$ on the outputs comes back through $P^{-1} = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ as $(0.5, 1.0)$, so the error energy grows from 0.5 to 1.25. This is why open-loop [predictive coding](/predictive-coding/) lets errors add up, and why practical predictive coders put the quantizer inside the loop.
- The biorthogonal LeGall 5/3 wavelet transform of JPEG 2000. It is invertible and has the [perfect reconstruction](/perfect-reconstruction/) property, but its analysis and synthesis filters are different, so it is not orthogonal, and an error on a coefficient is scaled by the norm of a synthesis filter that is not 1.
- A tall matrix $B \in \mathbb{R}^{M \times N}$ with $M > N$ and $B^{\mathsf T} B = I_N$. It keeps energy, but it is not square and $B B^{\mathsf T} \ne I_M$, so it is not a transform of $\mathbb{R}^M$. Such a map is an isometry onto a subspace of dimension $N$. The synthesis matrix of a single MDCT frame, with a window that meets the Princen-Bradley condition, is of this kind; only the lapped transform of the whole signal is orthogonal, as the page on the [modified discrete cosine transform](/modified-discrete-cosine-transform/) shows.

## Related definitions

- **Orthogonal versus orthonormal.** In linear algebra an orthogonal matrix has orthonormal rows. Some signal processing texts call a transform orthogonal when its basis vectors are only pairwise orthogonal. This page uses the strict meaning, $A^{\mathsf T} A = I$, and calls the other case a scaled orthogonal transform.
- **Parseval's identity.** Fact 2 is the finite form of [Parseval's theorem](/parseval-theorem/) for the DFT; the page [Parseval's theorem](/parsevals-theorem/) in signal processing gives the version for sequences and the DTFT.
- **Biorthogonal transform.** A pair of matrices $A$ (analysis) and $S$ (synthesis) with $SA = I$. Each invertible transform is biorthogonal with $S = A^{-1}$. It is orthogonal when $S = A^{\mathsf T}$. Biorthogonal filter banks give [perfect reconstruction](/perfect-reconstruction/) but not fact 3.
- **Orthogonal matrices in numerical linear algebra.** [Householder reflections](/householder-reflections/), [Givens rotations](/givens-rotations/) and the [QR decomposition](/qr-decomposition/) use orthogonal matrices because they do not grow rounding errors. A coder uses them for a different reason, fact 3: a quantization error does not grow when it goes back to the signal.
- **Energy compaction and decorrelation.** These are the two aims that make one orthogonal transform better than another for coding; see [energy compaction](/energy-compaction/) and [signal decorrelation](/signal-decorrelation/).

## References
