---
tag: HEPMMW
kind: problem
slug: signal-decorrelation
name: Signal decorrelation
aliases:
- decorrelation
- decorrelating transform
area: compression-and-coding/transforms-for-compression
level: intro
summary: Find a linear map whose outputs are pairwise uncorrelated. It removes linear redundancy; it is not independence.
prereqs: [orthogonal-transform, covariance-matrix]
see_also: [energy-compaction, karhunen-loeve-transform, whitening, independent-component-analysis, linear-prediction, cholesky-decomposition, symmetric-eigenproblem, transform-coding]
sources:
  - book: isbn:9780132119139
    title: N. S. Jayant and Peter Noll, Digital Coding of Waveforms, Prentice-Hall, 1984
    locator: Chapter 12, Transform Coding (the KLT as the decorrelating transform, and the limit of the transform coding gain and of the prediction gain for long blocks)
  - paper: doi:10.1109/79.952802
    title: Vivek K. Goyal, Theoretical foundations of transform coding, IEEE Signal Processing Magazine 18(5), 2001
    locator: pp. 9 to 21, the parts on the optimal transform for Gaussian sources and on orthogonality and independence
  - book: isbn:9780471405405
    title: Aapo Hyvärinen, Juha Karhunen and Erkki Oja, Independent Component Analysis, Wiley, 2001
    locator: Chapter 6, Principal Component Analysis and Whitening, and Chapter 7 (the ICA model, and whitening as its first step)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 4.2 (the Cholesky factorization) and Section 8.5 (Jacobi methods for the symmetric eigenproblem)
---

Signal decorrelation is the problem of finding a linear map $A$ such that the outputs $y = Ax$ of a random vector $x$ are pairwise uncorrelated, that is, the [covariance matrix](/covariance-matrix/) $A R A^{\mathsf T}$ of $y$ is diagonal. With an [orthogonal transform](/orthogonal-transform/) the problem has one answer, the [Karhunen-Loève transform](/karhunen-loeve-transform/); with any invertible map there are many, among them [whitening](/whitening/) and the triangular map of [linear prediction](/linear-prediction/). Decorrelation removes the linear redundancy between samples. It does not make them independent, except when the source is Gaussian.

## In plain words

Neighboring samples of a real signal are similar. If you know one pixel, you can guess the next one well. A coder that codes each sample alone wastes bits, because it codes the same information many times.

A decorrelating transform changes the samples into new numbers that do not move together in a straight-line way. If you plot one new number against another over many blocks, you see no tilted cloud. Then each new number can be coded on its own with little loss.

This removes only the straight-line kind of relation. Two numbers can be unrelated in that sense and still depend on each other in a curved way. For the bell-curve kind of signal, the straight-line kind is the only kind, so there nothing is left.

## Definition

**Model.** The input is a random vector $x \in \mathbb{R}^N$ (a block of $N$ samples) with mean zero and covariance matrix $R = E[x x^{\mathsf T}]$, which is symmetric and positive semidefinite. If the mean $\mu$ is not zero, use $x - \mu$. In practice $R$ is the sample covariance of a set of training blocks, or a model such as the first-order autoregressive (AR(1)) covariance $R_{ij} = \rho^{|i-j|}$.

**Problem (decorrelation).** Given $R$, find an invertible $A \in \mathbb{R}^{N \times N}$ such that

$$R_y = A R A^{\mathsf T} \text{ is diagonal.}$$

**Problem (orthogonal decorrelation).** The same, with the extra condition $A^{\mathsf T} A = I$. This is the version that [transform coding](/transform-coding/) needs, because an orthogonal map keeps the squared error.

**Measures of residual correlation.** A fixed transform such as the DCT only approximately solves the problem. Three measures of how far $R_y$ is from diagonal are used:

- the off-diagonal energy $\operatorname{off}(R_y)^2 = \sum_{k \ne l} (R_y)_{kl}^2$, the quantity that the Jacobi eigenvalue method drives to zero;
- the *decorrelation efficiency* $\eta_c = 1 - \sum_{k \ne l} |(R_y)_{kl}| \,/ \sum_{k \ne l} |R_{kl}|$, which is 1 for a full decorrelation and 0 for the identity;
- the *total correlation* $C(y) = \frac12 \log_2 \frac{\prod_k (R_y)_{kk}}{\det R_y}$ in bits. It is at least 0 by Hadamard's inequality for positive definite matrices, and it is 0 exactly when $R_y$ is diagonal. For a Gaussian $x$ it is the multi-information of the coefficients, $\sum_k h(y_k) - h(y)$, so it measures their dependence exactly.

**Decorrelation is not independence.** The outputs are *uncorrelated* when $E[y_k y_l] = 0$ for $k \ne l$. They are *independent* when their joint distribution is the product of the marginals. [Independent random variables](/independent-random-variables/) with finite variance are uncorrelated, but the converse is false in general. It is true when $x$ is jointly Gaussian, because $y = Ax$ is then jointly Gaussian and a Gaussian vector with a diagonal covariance has a product density.

**Decorrelation is not compaction.** Decorrelation is about the entries of $R_y$ off the diagonal. [Energy compaction](/energy-compaction/) is about how the fixed total $\operatorname{tr} R_y$ is spread along the diagonal. Whitening decorrelates and has no compaction at all; the DCT compacts nearly as well as the KLT but leaves some correlation.

## Variants

- **Orthogonal, from the true covariance.** The answer is the KLT: the rows of $A$ are orthonormal eigenvectors of $R$, by the [spectral theorem](/spectral-theorem/). When the eigenvalues are distinct it is unique up to the order and the signs of the rows.
- **Orthogonal, from data.** $R$ is the sample covariance of $M$ blocks. Then the coefficients are uncorrelated over the training data, and only approximately on new data.
- **Whitening.** Ask also that $R_y = I$. Then $A = D^{-1/2} V^{\mathsf T}$ (PCA whitening) or $A = R^{-1/2}$ (ZCA whitening), and any $QA$ with $Q$ orthogonal also works. Only defined when $R$ is positive definite.
- **Triangular (causal) decorrelation.** Ask that $A$ be unit lower triangular. With the factorization $R = L D L^{\mathsf T}$ (a scaled [Cholesky decomposition](/cholesky-decomposition/)), $A = L^{-1}$ gives $R_y = D$. Row $k$ of $A$ is the optimal linear predictor of $x_k$ from $x_0, \dots, x_{k-1}$, and $y_k$ is the prediction error. This is the basis of [predictive coding](/predictive-coding/).
- **Decorrelation of a stationary sequence.** For an infinite sequence the triangular variant becomes a prediction-error filter, which turns the sequence into a white innovation sequence. The [Levinson-Durbin recursion](/levinson-durbin-recursion/) computes its coefficients from the [autocorrelation](/autocorrelation/).
- **Fixed approximate decorrelation.** A fixed fast transform that nearly decorrelates a class of sources: the [discrete cosine transform](/discrete-cosine-transform/) for smooth images, the color transform from RGB to YCbCr that JFIF files use with [JPEG compression](/jpeg-compression/), and mid and side channels in stereo audio coding.
- **The stronger problem, independence.** Find $A$ so that the outputs are independent, not only uncorrelated. For non-Gaussian sources this is [independent component analysis](/independent-component-analysis/), which usually starts by whitening and then searches for the rotation that maximizes non-Gaussianity.

## Examples

**A pair of samples.** Let $R = \begin{pmatrix} 1 & 0.9 \\ 0.9 & 1 \end{pmatrix}$. The orthogonal map $A = \frac{1}{\sqrt 2}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$ gives $A R A^{\mathsf T} = \operatorname{diag}(1.9, 0.1)$: the scaled sum and difference are uncorrelated. The triangular map $y = (x_1, x_2 - 0.9 x_1)$ gives $\operatorname{diag}(1, 0.19)$, also uncorrelated, with a different split of the variance. Both have determinant of absolute value 1 and the same product of variances, $0.19 = \det R$.

**AR(1) with prediction.** For $R_{ij} = \rho^{|i-j|}$, the unit lower bidiagonal matrix with $-\rho$ below the diagonal maps $x$ to $(x_0, x_1 - \rho x_0, \dots, x_{N-1} - \rho x_{N-2})$, and the covariance of the output is $\operatorname{diag}(1, 1-\rho^2, \dots, 1-\rho^2)$. For $\rho = 0.9$ the variances are $1$ and seven times $0.19$.

**AR(1) with the DCT.** For $N = 8$ and $\rho = 0.9$ the orthonormal DCT-II leaves these correlations. All covariances between an even-index and an odd-index coefficient are exactly zero, because the AR(1) covariance is symmetric under reversal of the block and the even DCT basis vectors are symmetric and the odd ones antisymmetric. The largest remaining entry is $(R_y)_{02} = -0.3117$, between the DC coefficient (variance 6.1855) and coefficient 2 (variance 0.3461), a correlation coefficient of $-0.213$. The other numbers are:

| transform | off-diagonal energy | $\eta_c$ | total correlation $C(y)$ |
|---|---|---|---|
| identity | 31.651 | 0 | 8.386 bits |
| DCT-II | 0.2075 | 0.9782 | 0.0462 bits |
| KLT | 0 | 1 | 0 |

At $\rho = 0.95$ the DCT has $\eta_c = 0.9894$ and $C(y) = 0.0270$ bits.

**Uncorrelated but dependent.** Let $X$ be uniform on $[-1, 1]$ and $Y = X^2 - \frac13$. Then $E[Y] = 0$ and $E[XY] = E[X^3] - \frac13 E[X] = 0$, so $X$ and $Y$ are uncorrelated. But $Y$ is a function of $X$. For example $E[X^2 Y] = E[X^4] - \frac13 E[X^2] = \frac15 - \frac19 = \frac{4}{45}$, while $E[X^2]\,E[Y] = 0$, so they are not independent. No linear map can find this relation; a coder that knows it can send $Y$ for free once it has sent $X$.

## Known algorithms

- **Symmetric eigendecomposition** solves orthogonal decorrelation exactly. The [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/) applies plane rotations that each zero one off-diagonal entry and lower $\operatorname{off}^2$; the [QR algorithm](/qr-algorithm/) after a tridiagonal reduction is faster for large $N$. Both take $O(N^3)$ operations. See [symmetric eigenproblem](/symmetric-eigenproblem/) and the [Karhunen-Loève transform](/karhunen-loeve-transform/).
- **Cholesky or $LDL^{\mathsf T}$ factorization** solves triangular decorrelation in about $N^3/3$ multiplications.
- **Levinson-Durbin recursion** solves triangular decorrelation for a Toeplitz $R$ (a stationary source) in $O(N^2)$ operations.
- **Gram-Schmidt on the samples.** The [Gram-Schmidt process](/gram-schmidt-process/) with the inner product $\langle u, v \rangle = E[uv]$ produces the same triangular decorrelation.
- **Fixed transforms.** The DCT and its fast algorithms cost $O(N \log N)$ operations per block, and approximately decorrelate smooth sources. A fixed transform needs no side information about $R$.

## Bounds

- **Orthogonal decorrelation and coding gain.** For an orthogonal $A$, $\det R_y = \det R$, so the total correlation is $C(Ax) = \frac{N}{2} \log_2 \frac{G_{\mathrm{KLT}}}{G_A}$, where $G_A$ is the coding gain of $A$ (the ratio of the arithmetic and geometric means of the coefficient variances). So the gain lost by an orthogonal transform is exactly its residual total correlation, and the KLT, with $C = 0$, has the largest gain. For the DCT at $\rho = 0.9$, $N = 8$, this gives $6.311 - 6.276 = 0.035$ dB.
- **Product of variances.** For any $A$ with $|\det A| = 1$ that decorrelates, the product of the output variances is $\det R$, the smallest value that $\prod_k (R_y)_{kk}$ can take for such $A$ (Hadamard's inequality). The KLT and the triangular map reach it with different variances.
- **Long blocks.** For a stationary Gaussian source, as $N \to \infty$ the KLT coding gain and the gain of optimal linear prediction both tend to the inverse of the spectral flatness measure of the source (Jayant and Noll, Chapter 12). For AR(1) both limits are $1/(1-\rho^2)$: the KLT gain is $(1-\rho^2)^{-(N-1)/N}$ and the prediction gain is $1/(1-\rho^2)$.

## Reductions

- Orthogonal decorrelation of $R$ is the same problem as the symmetric eigenproblem for $R$: $A R A^{\mathsf T} = \Lambda$ with $A$ orthogonal says exactly that the rows of $A$ are eigenvectors.
- Whitening reduces to orthogonal decorrelation plus a diagonal scaling, or to a Cholesky factorization plus a scaling.
- Triangular decorrelation of a stationary source reduces to solving the Toeplitz normal equations of linear prediction.
- For Gaussian sources, independence reduces to decorrelation. For other sources it does not, and ICA is a separate problem.

## Applications

- [Transform coding](/transform-coding/): decorrelate with an orthogonal transform, then quantize and code each coefficient on its own.
- [Predictive coding](/predictive-coding/): decorrelate with a causal predictor, then quantize and code the prediction error.
- Color image coding: JPEG files in the JFIF format store YCbCr, not RGB, and JPEG 2000 has a reversible and an irreversible color transform, before the spatial transform.
- Stereo audio: mid and side coding of the sum and difference of the two channels.
- Preprocessing in statistics and machine learning: [principal component analysis](/principal-component-analysis/) and [whitening](/whitening/) before ICA or other models. There the aim is a simpler description of the data, not fewer bits, and the page on whitening covers the scale conventions.

## References
