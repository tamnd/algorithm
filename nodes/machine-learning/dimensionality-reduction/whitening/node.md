---
tag: H04HKR
kind: technique
slug: whitening
name: Whitening
aliases:
- data whitening
- sphering
- ZCA whitening
- PCA whitening
- Mahalanobis whitening
area: machine-learning/dimensionality-reduction
level: core
summary: "Transform centered data by a matrix W with W C W^T = I, so that the covariance becomes the identity. PCA, ZCA and Cholesky whitening differ only by a rotation."
prereqs: [covariance-matrix, principal-component-analysis]
see_also: [independent-component-analysis, fastica, signal-decorrelation, karhunen-loeve-transform, batch-normalization, linear-discriminant-analysis, cholesky-decomposition, positive-definite-matrix]
sources:
  - paper: doi:10.1080/00031305.2016.1277159
    title: Agnan Kessy, Alex Lewin and Korbinian Strimmer, Optimal whitening and decorrelation, The American Statistician 72(4), 309-314, 2018
    locator: the family W = Q Sigma^(-1/2) of all whitening matrices, the five common choices (ZCA, ZCA-cor, PCA, PCA-cor, Cholesky), and the optimality of ZCA and ZCA-cor (closest to the original data) and of PCA-cor (most compression)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 12.1.3 (PCA for data pre-processing, standardization and whitening to zero mean and unit covariance)
  - paper: doi:10.1016/S0893-6080(00)00026-5
    title: Aapo Hyvarinen and Erkki Oja, Independent component analysis, algorithms and applications, Neural Networks 13(4-5), 411-430, 2000
    locator: Section 5.2 (whitening by the eigenvalue decomposition of the covariance, and the reduction of the ICA problem to an orthogonal mixing matrix)
  - paper: doi:10.1016/S0042-6989(97)00121-1
    title: Anthony J. Bell and Terrence J. Sejnowski, The independent components of natural scenes are edge filters, Vision Research 37(23), 3327-3338, 1997
    locator: the zero-phase (ZCA) whitening filter W = C^(-1/2) applied to image patches
---

Whitening transforms data with a mean $\mu$ and an invertible [covariance matrix](/covariance-matrix/) $C$ by $z = W(x - \mu)$, with a $d \times d$ matrix $W$ chosen so that $z$ has the identity as covariance: $W C W^T = I$. The features of $z$ are uncorrelated and have variance 1. The solutions are exactly the matrices $W = Q C^{-1/2}$ with $Q$ orthogonal, so whitening is unique only up to a rotation. PCA whitening, ZCA (Mahalanobis) whitening and Cholesky whitening are three choices of $Q$ (Kessy, Lewin and Strimmer 2018).

## In plain words

Real features are often correlated, and they have different spreads. Whitening changes the coordinates of the data so that the cloud of points becomes round: every direction has the same spread, equal to 1, and no two features are correlated.

There are many ways to do this, because after the cloud is round you can turn it in any direction and it stays round. The common methods pick one turn. PCA whitening uses the axes of principal component analysis. ZCA whitening turns the cloud back so that it stays as close as possible to the original data, which keeps image pixels looking like image pixels. Cholesky whitening uses a triangular matrix, which is cheap.

Whitening is a preprocessing step. Learn the mean and the matrix on the training data, and apply the same ones to new data.

## When it applies

- The features are real numbers and the covariance matrix is positive definite. This needs at least $d + 1$ points in general position: the sample covariance has rank at most $n - 1$, so for $n \le d$ it is singular and no exact whitening exists.
- Second moments are what matter. Whitening removes all linear correlation, but it does not make the features independent unless the data are Gaussian.
- The next step works better or is simpler on white data: [independent component analysis](/independent-component-analysis/), where whitening reduces the unknown mixing matrix to an orthogonal one; distances that should not depend on the scale and correlation of the features; or gradient methods, whose convergence improves when the Hessian of a quadratic loss is the identity.
- Do not whiten before [PCA](/principal-component-analysis/) itself: after whitening every direction has variance 1, and PCA has nothing to find.

## The template

The data are the rows $x_1, \ldots, x_n$ of $X$, with the covariance taken with the divisor $n$ (the divisor $n - 1$ only changes $W$ by the factor $\sqrt{(n-1)/n}$). The hole is CHOOSE-Q, which returns an orthogonal $d \times d$ matrix. The regularization $\varepsilon \ge 0$ is a second hole; $\varepsilon = 0$ gives exact whitening.

```pseudo id=main
WHITEN(X, CHOOSE-Q, ε)                       ▷ returns μ and W; the whitened point is W(x − μ)
L1  μ ← (1/n) Σ_i x_i
L2  C ← (1/n) Σ_i (x_i − μ)(x_i − μ)^T
L3  (λ_1 ≥ ... ≥ λ_d, v_1, ..., v_d) ← eigenpairs of C   ▷ for example by the Jacobi method
L4  W_PCA ← diag((λ_j + ε)^(−1/2)) V^T        ▷ V = [v_1, ..., v_d]
L5  Q ← CHOOSE-Q(V)                           ▷ I for PCA whitening, V for ZCA whitening
L6  W ← Q W_PCA
L7  return μ, W
```

**Why it works.** With $\varepsilon = 0$, $W_{PCA} C W_{PCA}^T = \Lambda^{-1/2} V^T (V \Lambda V^T) V \Lambda^{-1/2} = I$, and then $W C W^T = Q I Q^T = I$. Conversely, let $W$ be any matrix with $W C W^T = I$. Put $Q = W C^{1/2}$, where $C^{1/2} = V \Lambda^{1/2} V^T$. Then $Q Q^T = W C W^T = I$, so $Q$ is orthogonal and $W = Q C^{-1/2}$. So the template, with all orthogonal choices of $Q$ composed with $V$, gives every whitening matrix.

**ZCA is the closest.** Write $y = x - \mu$. For $z = W y$ with $W = Q C^{-1/2}$,

$$\frac1n \sum_i \|z_i - y_i\|^2 = \operatorname{tr}(W C W^T) + \operatorname{tr} C - 2 \operatorname{tr}(W C) = d + \operatorname{tr} C - 2 \operatorname{tr}(Q C^{1/2}).$$

With $C^{1/2} = \sum_j \sqrt{\lambda_j} v_j v_j^T$, $\operatorname{tr}(Q C^{1/2}) = \sum_j \sqrt{\lambda_j}\, v_j^T Q v_j \le \sum_j \sqrt{\lambda_j}$, since $|v_j^T Q v_j| \le 1$. Equality holds for $Q = I$, that is $W = C^{-1/2}$, and only for it when $C$ is positive definite. So ZCA whitening changes the data the least, which is the result of Kessy et al. (2018) for the covariance version.

**Cost.** L1 and L2 take $O(n d^2)$ time, L3 takes $O(d^3)$, and transforming $m$ points takes $O(m d^2)$. The space is $O(d^2)$ beyond the data.

## Classic examples

- **Preprocessing for ICA.** [FastICA](/fastica/) and other [ICA](/independent-component-analysis/) methods whiten first. If $x = A s$ with independent unit-variance sources, then the whitened data are $z = (W A) s$ with $W A$ orthogonal, so the search is over rotations only (Hyvarinen and Oja 2000, Section 5.2).
- **Mahalanobis distance.** $\|C^{-1/2}(x - x')\|$ is the Euclidean distance after ZCA whitening, and any other whitening gives the same value, since $Q$ preserves lengths. Gaussian models such as [quadratic discriminant analysis](/quadratic-discriminant-analysis/) use this distance.
- **The Karhunen-Loeve transform.** The [KLT](/karhunen-loeve-transform/) of transform coding is the rotation $V^T$, which [decorrelates](/signal-decorrelation/) the signal. PCA whitening adds the scaling $\Lambda^{-1/2}$ on top of it.
- **Linear discriminant analysis.** [LDA](/linear-discriminant-analysis/) can be computed by whitening with the within-class covariance and then running PCA on the class means.
- **Image patches.** Bell and Sejnowski (1997) used the ZCA filter $C^{-1/2}$ on patches of natural images. The rows of $C^{-1/2}$ look like local center-surround filters, and the whitened patches still look like images, which PCA whitened patches do not.
- **Sampling, the inverse.** To draw from $\mathcal{N}(\mu, C)$, draw white $z$ and return $\mu + L z$ with $C = L L^T$ from the [Cholesky decomposition](/cholesky-decomposition/). This is coloring, the inverse of Cholesky whitening.

## Variations

- **PCA whitening**, $Q = I$: $z_j = v_j^T (x - \mu) / \sqrt{\lambda_j}$, the principal component scores scaled to variance 1. Keep only the first $k$ rows of $W$ to whiten and reduce the dimension in one step. The signs of the $v_j$ are arbitrary, so two programs can return different $z$.
- **ZCA or Mahalanobis whitening**, $Q = V$: $W = C^{-1/2} = V \Lambda^{-1/2} V^T$, symmetric and unique. It does not depend on the signs or on the order of the eigenvectors.
- **Cholesky whitening**: $W = L^{-1}$ with $C = L L^T$, a lower triangular matrix. It needs no eigenvalues, and the factorization takes about $d^3/3$ arithmetic operations, which is $O(d^3)$. The first whitened feature depends only on the first original feature, the second only on the first two, and so on, so the result depends on the order of the features. Kessy et al. write the same family with the Cholesky factor of $C^{-1}$, which gives an upper triangular $W$.
- **Correlation-based versions.** Standardize first with the diagonal $D$ of the variances, and whiten the correlation matrix $P$: $W = Q P^{-1/2} D^{-1/2}$. Kessy et al. show that ZCA-cor gives whitened features closest to the standardized ones, and that PCA-cor puts the most of the original features into the first whitened components.
- **Regularized whitening**, $\varepsilon > 0$: the covariance of $z$ becomes $\operatorname{diag}(\lambda_j / (\lambda_j + \varepsilon))$ in the PCA basis. Directions with $\lambda_j \ll \varepsilon$ are damped instead of scaled up.
- **Standardization**, $W = D^{-1/2}$, makes the variances 1 but leaves the correlations. [Batch normalization](/batch-normalization/) standardizes each feature over a mini-batch in this way and does not whiten.

## Pitfalls

- **Noise is amplified.** The direction $v_d$ is scaled by $1/\sqrt{\lambda_d}$. When $\lambda_d$ is small, which often means noise, whitening makes that noise as large as the signal. Use $\varepsilon > 0$, or drop the directions with small $\lambda_j$.
- **Singular covariance.** With $n \le d$, or with a feature that is a linear combination of others, $C$ is singular and $C^{-1/2}$ does not exist. The code must check the smallest eigenvalue; a [Cholesky](/cholesky-decomposition/) step fails in this case, which is a useful test.
- **Fit once.** Compute $\mu$ and $W$ on the training data and apply them unchanged to validation, test and new data. Fitting again on each set gives each set a different coordinate system, and it leaks information from the test data.
- **Uncorrelated is not independent.** For non-Gaussian data, whitened features can still depend on each other. ICA exists because of this gap.
- **Whitening is not a rotation.** It changes the lengths and angles of the data. Do not compare distances or angles before and after whitening, and do not run PCA on whitened data.
- **The divisor.** Using $n - 1$ for the fit and $n$ for the check, or the reverse, gives a covariance of $\frac{n-1}{n} I$ or $\frac{n}{n-1} I$, not $I$.

## Exercises

1. For the eight points of the [PCA](/principal-component-analysis/) page, with mean $(4, 5, 6)$ and covariance eigenvalues $81, 36, 9$ with eigenvectors $(1, 2, 2)/3$, $(2, 1, -2)/3$, $(2, -2, 1)/3$, show that PCA whitening sends every point to a corner of the cube $\{-1, 1\}^3$. *Answer:* the scores of every point are $\pm 9, \pm 6, \pm 3$, and the scaling divides them by $9, 6, 3$.
2. For the same data, show that $C^{-1/2} = \frac{1}{162}\begin{pmatrix} 38 & -14 & 4 \\ -14 & 35 & -10 \\ 4 & -10 & 26 \end{pmatrix}$, and that ZCA whitening sends $(13, 11, 9)$ to $(5/3, 1/3, 1/3)$. *Answer:* $C^{-1/2} = \frac19 v_1 v_1^T + \frac16 v_2 v_2^T + \frac13 v_3 v_3^T$, and the point has the scores $(9, 6, 3)$, so $z = v_1 + v_2 + v_3 = (5, 1, 1)/3$. Both points have the same length $\sqrt 3$, as the rotation $Q = V$ predicts.
3. Show that if $W_1$ and $W_2$ both whiten the same data, then $W_1 W_2^{-1}$ is orthogonal.

## References
