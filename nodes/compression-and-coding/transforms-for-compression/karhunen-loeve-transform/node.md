---
tag: PSR8K0
kind: algorithm
slug: karhunen-loeve-transform
name: Karhunen-Loève transform
aliases:
- Hotelling transform
- KLT
- principal component transform
area: compression-and-coding/transforms-for-compression
level: advanced
summary: 'Optimal decorrelating transform: the eigenbasis of the signal covariance matrix.'
model: real-ram
complexity:
  vars: {N: the block length, M: the number of training blocks, r: the number of Jacobi rotations}
  time: {worst: "Θ(M N^2 + r N^2)"}
  space: {extra: Θ(N^2)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1933
  people: [Harold Hotelling, Kari Karhunen, Michel Loève]
  note: Hotelling introduced principal components of a vector in 1933; Karhunen and Loève gave the expansion for random processes in the 1940s, and Huang and Schultheiss made the transform the reference of block quantization in 1963.
prereqs: [orthogonal-transform, signal-decorrelation, energy-compaction, jacobi-eigenvalue-algorithm, covariance-matrix]
see_also: [principal-component-analysis, karhunen-loeve-theorem, discrete-cosine-transform, transform-coding, whitening, discrete-sine-transform, symmetric-eigenproblem, explained-variance]
sources:
  - paper: doi:10.1037/h0071325
    title: Harold Hotelling, Analysis of a complex of statistical variables into principal components, Journal of Educational Psychology 24(6), 1933
    locator: pp. 417 to 441, continued in 24(7), pp. 498 to 520 (the principal components as eigenvectors of the correlation matrix)
  - paper: doi:10.1109/TCOM.1963.1088759
    title: J. J. Y. Huang and P. M. Schultheiss, Block quantization of correlated Gaussian random variables, IEEE Transactions on Communications Systems 11(3), 1963
    locator: pp. 289 to 296 (the KLT is the best orthogonal transform for block quantization of Gaussian vectors at high rate)
  - book: isbn:9780132119139
    title: N. S. Jayant and Peter Noll, Digital Coding of Waveforms, Prentice-Hall, 1984
    locator: Chapter 12, Transform Coding (the KLT, its coding gain, and its comparison with the DCT, DFT and WHT)
  - paper: doi:10.1109/79.952802
    title: Vivek K. Goyal, Theoretical foundations of transform coding, IEEE Signal Processing Magazine 18(5), 2001
    locator: pp. 9 to 21 (the conditions under which the KLT is optimal)
  - paper: doi:10.1109/TIT.2004.831787
    title: Michelle Effros, Hanying Feng and Kenneth Zeger, Suboptimality of the Karhunen-Loève transform for transform coding, IEEE Transactions on Information Theory 50(8), 2004
    locator: pp. 1605 to 1619 (non-Gaussian sources for which the KLT is not the best transform)
  - paper: doi:10.1073/pnas.35.11.652
    title: Ky Fan, On a theorem of Weyl concerning eigenvalues of linear transformations I, Proceedings of the National Academy of Sciences 35(11), 1949
    locator: pp. 652 to 655 (the sum of the m largest eigenvalues as a maximum over orthonormal m-frames)
  - paper: doi:10.1515/crll.1846.30.51
    title: C. G. J. Jacobi, Über ein leichtes Verfahren die in der Theorie der Säcularstörungen vorkommenden Gleichungen numerisch aufzulösen, Journal für die reine und angewandte Mathematik 30, 1846
    locator: pp. 51 to 94 (plane rotations that remove the largest off-diagonal entry)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.5, Jacobi Methods (the classical Jacobi algorithm, the choice of the rotation, and the decrease of the off-diagonal norm)
  - paper: doi:10.1137/0106008
    title: Peter Henrici, On the speed of convergence of cyclic and quasicyclic Jacobi methods for computing eigenvalues of Hermitian matrices, Journal of SIAM 6(2), 1958
    locator: pp. 144 to 162 (the quadratic convergence of Jacobi methods)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 7.8 (Hadamard's inequality for positive semidefinite matrices)
---

The Karhunen-Loève transform (KLT) of a random vector $x \in \mathbb{R}^N$ is the [orthogonal transform](/orthogonal-transform/) whose rows are the unit eigenvectors of the [covariance matrix](/covariance-matrix/) $R$ of $x$, sorted by decreasing eigenvalue. The coefficients $y = T(x - \mu)$ are uncorrelated, with variances equal to the eigenvalues. Among all orthogonal transforms, the KLT puts the largest possible share of the variance into the first $m$ coefficients for each $m$, and for a Gaussian source at high rate it gives the largest [transform coding](/transform-coding/) gain. It depends on the source, so a coder must estimate $R$ and solve an eigenproblem; this page does both, with the classical Jacobi method for the eigenvectors.

## In plain words

Take many blocks of a signal, for example many runs of eight neighboring samples. Some directions in the space of blocks carry a lot of variation, such as the overall level of the block, and others carry very little. The KLT finds these directions. The first is the direction of the most variation; the second is the direction of the most remaining variation that is at a right angle to the first; and so on.

Writing each block in these directions gives coefficients that do not move together on average, and the first few carry almost all of the variation. A coder can then spend its bits on the first coefficients and drop the last ones with the smallest possible average error. The price is that the directions depend on the data, so they must be computed and also sent to the decoder.

## The problem

**Input.** Training blocks $x_1, \dots, x_M \in \mathbb{R}^N$, or a model covariance matrix $R$ that is symmetric and positive semidefinite.

**Output.** The mean $\mu$, the eigenvalues $\lambda_1 \ge \dots \ge \lambda_N \ge 0$ of $R$, and an orthogonal matrix $T$ whose row $k$ is a unit eigenvector for $\lambda_k$, so that

$$T R T^{\mathsf T} = \operatorname{diag}(\lambda_1, \dots, \lambda_N).$$

The forward transform of a block is $y = T(x - \mu)$ and the inverse is $x = T^{\mathsf T} y + \mu$.

**KLT and PCA.** The KLT is [principal component analysis](/principal-component-analysis/) in the vocabulary of signal coding, and the two are equal up to centering and scaling conventions. PCA estimates the covariance from data, often with the factor $1/(M-1)$, usually computes it by a singular value decomposition of the data matrix, and keeps the first few components to reduce dimension. A transform coder keeps all $N$ coefficients and quantizes them; it often takes $R$ from a model such as the first-order autoregressive covariance $R_{ij} = \rho^{|i-j|}$, where the mean is zero. This page uses $1/M$; the eigenvectors are the same with either factor.

**KLT and the Karhunen-Loève theorem.** The [Karhunen-Loève theorem](/karhunen-loeve-theorem/) is the statement for random processes in continuous time, with an integral operator in place of $R$. The KLT is the finite case.

## The algorithm

The covariance step is a direct sum. The eigenvectors come from the classical Jacobi method: while the off-diagonal part of $A$ is not small, pick its largest entry $a_{pq}$ and apply the plane rotation $J$ in the coordinates $p, q$ that sets it to zero. The product of the rotations converges to a matrix of eigenvectors.

```pseudo id=main
COVARIANCE(x_1, ..., x_M)                 ▷ M blocks of length N
L1  μ ← (1/M) Σ_m x_m
L2  R ← (1/M) Σ_m (x_m − μ)(x_m − μ)^T
    return μ, R

JACOBI(R)                                 ▷ R symmetric; returns R = V diag(λ) V^T
L3  A ← R;  V ← I
L4  while off(A) > tol · ‖R‖_F do        ▷ off(A)² = Σ_{i≠j} a_ij²
L5      (p, q) ← the pair p < q with the largest |a_pq|
L6      θ ← (a_qq − a_pp) / (2 a_pq)
L7      t ← sign(θ) / (|θ| + √(θ² + 1));  c ← 1/√(t² + 1);  s ← t·c
L8      A ← J^T A J;  V ← V J;  a_pq ← a_qp ← 0
    return diag(A), V

KLT(x_1, ..., x_M)
    (μ, R) ← COVARIANCE(x_1, ..., x_M);  (λ, V) ← JACOBI(R)
L9  sort the pairs (λ_k, column k of V) by decreasing λ_k
L10 T ← the matrix whose row k is the k-th sorted eigenvector, sign fixed
    return T, μ, λ

FORWARD(T, μ, x)
L11 return T (x − μ)

INVERSE(T, μ, y)
L12 return T^T y + μ
```

Here $J$ is the identity except for $J_{pp} = J_{qq} = c$, $J_{pq} = s$ and $J_{qp} = -s$. The value $t = \tan\phi$ is the root of smaller magnitude of $t^2 + 2\theta t - 1 = 0$, which makes the rotation angle at most $\pi/4$. Line L8 changes only rows and columns $p$ and $q$ of $A$, in $\Theta(N)$ operations. An eigenvector is defined only up to sign; line L10 makes the entry of largest magnitude of each row positive, so the output is unique when the eigenvalues are distinct.

## Example

**Five blocks of length 2.** The blocks $(2,1)$, $(0,-1)$, $(3,4)$, $(-1,0)$, $(1,1)$ have the mean $\mu = (1,1)$ and the deviations $(1,0)$, $(-1,-2)$, $(2,3)$, $(-2,-1)$, $(0,0)$. So

$$R = \frac15 \begin{pmatrix} 10 & 10 \\ 10 & 14 \end{pmatrix} = \begin{pmatrix} 2 & 2 \\ 2 & 2.8 \end{pmatrix}.$$

JACOBI needs one rotation with $p = 0$, $q = 1$: $\theta = 0.8/4 = 0.2$, $t = 1/(0.2 + \sqrt{1.04}) = 0.8198$, $c = 0.7733$ and $s = 0.6340$. The new diagonal is $(0.3604, 4.4396)$, which are $2.4 \mp \sqrt{4.16}$. After sorting and the sign rule,

$$T = \begin{pmatrix} 0.6340 & 0.7733 \\ 0.7733 & -0.6340 \end{pmatrix}, \qquad \lambda = (4.4396,\ 0.3604).$$

The coefficients of the five blocks are $(0.634, 0.773)$, $(-2.181, 0.495)$, $(3.588, -0.355)$, $(-2.041, -0.913)$ and $(0, 0)$. Their mean squares are 4.4396 and 0.3604, and the mean of their products is 0. The first coefficient carries $4.4396/4.8 = 92.5\%$ of the variance. Keeping it alone and setting the second to zero gives a mean squared error of exactly $\lambda_2 = 0.3604$ per block, and no other unit direction does better.

**AR(1) with $N = 8$.** For $R_{ij} = 0.9^{|i-j|}$ the Jacobi method stops after 106 rotations at $\text{tol} = 10^{-13}$, with

$$\lambda = (6.2030, 1.0072, 0.3297, 0.1647, 0.1036, 0.0756, 0.0615, 0.0547).$$

The first row of $T$ is $(0.3237, 0.3486, 0.3656, 0.3742, 0.3742, 0.3656, 0.3486, 0.3237)$, a flat bump whose inner product with the constant DCT row is 0.9985. The coding gain is $\frac18 \sum_k \lambda_k / (\prod_k \lambda_k)^{1/8} = 4.2765$, equal to the closed form $(1 - \rho^2)^{-(N-1)/N}$; the DCT reaches 4.2424 on the same source.

## Correctness

The full proofs are in [the correctness proof](proofs/correctness.md). In short:

1. **Decorrelation.** If the rows of $T$ are orthonormal eigenvectors of $R$, then $E[yy^{\mathsf T}] = TRT^{\mathsf T} = \operatorname{diag}(\lambda)$, and $T^{\mathsf T}T = I$ makes INVERSE exact.
2. **Best compaction.** For each orthogonal $A$ and each $m$, the variance in the first $m$ coefficients of $Ax$ is $\sum_{k<m} (ARA^{\mathsf T})_{kk} \le \lambda_1 + \dots + \lambda_m$ (Ky Fan, 1949). The proof writes each row of $A$ in the eigenbasis and bounds a weighted sum of the $\lambda_k$ with weights in $[0,1]$ that add up to $m$.
3. **Best coding gain.** Hadamard's inequality $\prod_k S_{kk} \ge \det S$ for positive semidefinite $S = ARA^{\mathsf T}$ gives $\prod_k \sigma_k^2 \ge \det R = \prod_k \lambda_k$. The arithmetic mean of the $\sigma_k^2$ is $\frac1N \operatorname{tr} R$ for every orthogonal $A$, so the gain $\mathrm{AM}/\mathrm{GM}$ is largest for the KLT.
4. **Jacobi converges.** The rotation of line L8 zeroes $a_{pq}$, keeps the Frobenius norm, and moves $2a_{pq}^2$ from the off-diagonal part to the diagonal. Since $a_{pq}$ is the largest off-diagonal entry, $\operatorname{off}(A)^2$ shrinks by the factor $1 - \frac{2}{N(N-1)}$ or less at each rotation, so the loop stops. When it stops, the sorted diagonal entries are within $\operatorname{off}(A)$ of the sorted eigenvalues of $R$, by Weyl's inequality.

## Complexity

- **Covariance.** $\Theta(M N^2)$ operations and $\Theta(N^2)$ space.
- **One rotation.** The search at line L5 and the test at line L4 take $\Theta(N^2)$; the update at line L8 takes $\Theta(N)$. So $r$ rotations take $\Theta(r N^2)$.
- **Number of rotations.** The factor $1 - 2/(N(N-1))$ per rotation gives $r = O(N^2 \log(1/\text{tol}))$ in the worst case. In practice the classical and cyclic Jacobi methods converge quadratically once the off-diagonal part is small (Henrici, 1958), and the count is a small multiple of $N^2$: 106 rotations for the AR(1) example with $N = 8$.
- **Applying the transform.** FORWARD and INVERSE are matrix-vector products, $\Theta(N^2)$ per block, against $\Theta(N \log N)$ for the [DCT](/discrete-cosine-transform/). A general KLT has no fast algorithm.
- **Other eigensolvers.** The [QR algorithm](/qr-algorithm/) on the tridiagonal form, or a divide-and-conquer solver, takes $O(N^3)$ for all eigenvectors. Jacobi is simpler, very accurate for small eigenvalues, and easy to check, which suits the small $N$ of block coding.

## Properties

- The coefficients are uncorrelated, and their variances are the eigenvalues. For a Gaussian source they are independent; for other sources they need not be (see [signal decorrelation](/signal-decorrelation/)).
- The KLT keeps the energy and the squared error, like every orthogonal transform.
- For a fixed $m$, keeping the first $m$ coefficients gives the smallest mean squared error of any $m$-dimensional linear projection; the error is $\lambda_{m+1} + \dots + \lambda_N$.
- The coding gain $G_{\mathrm{KLT}} = \frac{\frac1N \operatorname{tr} R}{(\det R)^{1/N}}$ is the largest over orthogonal transforms.
- The transform is unique up to the sign of each row when the eigenvalues are distinct. With repeated eigenvalues, any orthonormal basis of the eigenspace works.
- For the AR(1) covariance the KLT tends to the DCT-II as $\rho \to 1$, which is why the fixed DCT is used in its place.

## Variants and improvements

- **PCA by the SVD.** For data, the singular value decomposition of the centered data matrix gives the same basis with better numerical accuracy than forming $R$.
- **Cyclic Jacobi.** Sweep the pairs $(p,q)$ in a fixed order instead of searching for the largest entry; each step is $\Theta(N)$. See [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/).
- **Separable 2D KLT.** For images, compute one KLT for rows and one for columns. This costs much less than a KLT of the $N^2$-dimensional block, at some loss of gain.
- **Adaptive and incremental KLT.** Update $R$ and the eigenvectors as data arrive; see [incremental PCA](/incremental-pca/).
- **Fast KLT for special models.** Jain (1976) showed that the [discrete sine transform](/discrete-sine-transform/) is the KLT of a first-order Markov process with fixed boundary values, which gives a fast transform for that model.
- **Kernel PCA.** The same eigen-decomposition on a kernel matrix gives nonlinear components; see [kernel PCA](/kernel-pca/).

## When to use it

Use the KLT when the source statistics are known or stable, $N$ is small, and the best compaction matters more than speed: as a reference to measure other transforms against, in multispectral and hyperspectral image coding (across the spectral bands), and in coding of data with a known model. Use a fixed transform such as the [DCT](/discrete-cosine-transform/) when the source changes from block to block, when the decoder cannot receive the basis, or when $\Theta(N^2)$ per block is too slow.

## Pitfalls

- **Side information.** The decoder needs $T$ and $\mu$. For small data the cost of sending them can exceed the gain.
- **Estimation error.** With few blocks, the sample covariance is noisy and the small eigenvalues are biased. The KLT of the sample is optimal for the sample, not for the source.
- **Not the best transform in general.** The optimality of the coding gain holds for Gaussian sources under the high-rate model with scalar quantizers. Effros, Feng and Zeger (2004) give non-Gaussian sources for which other transforms do better.
- **Decorrelated is not independent.** For non-Gaussian data, the KLT removes correlation but not dependence; see [independent component analysis](/independent-component-analysis/).
- **Signs and order.** Eigensolvers return eigenvectors with arbitrary signs and in arbitrary order. Fix both before you compare or store them.
- **Repeated eigenvalues.** The basis is not unique, and small changes in the data can rotate it by a large angle inside the eigenspace.
- **Scaling.** The KLT of $R$ and of the correlation matrix differ when the variables have different scales. Choose the one that matches the distortion measure.

## Implementations

## History

Harold Hotelling introduced principal components in 1933, as the eigenvectors of the correlation matrix of a set of test scores. Kosambi (1943), Karhunen (1946) and Loève (1945, 1955) gave the expansion of random processes in the eigenfunctions of their covariance. Huang and Schultheiss (1963) showed that this transform, followed by optimal bit allocation, is the best block quantizer of correlated Gaussian variables at high rate, and the name Karhunen-Loève transform became standard in signal coding. Ahmed, Natarajan and Rao (1974) proposed the DCT as a fast substitute for the KLT of image data. The eigenvector method used here is Jacobi's from 1846; its quadratic convergence was shown by Henrici in 1958. Effros, Feng and Zeger (2004) showed that the KLT is not always the best transform for transform coding.

## References
