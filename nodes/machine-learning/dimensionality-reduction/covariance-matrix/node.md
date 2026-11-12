---
tag: N5JYXB
kind: definition
slug: covariance-matrix
name: Covariance matrix
aliases:
- variance-covariance matrix
- dispersion matrix
area: machine-learning/dimensionality-reduction
level: intro
summary: "The d × d matrix of pairwise covariances of a random vector or a data set. It is symmetric and positive semidefinite; the sample version divides by n - 1."
prereqs: [variance, expected-value]
see_also: [principal-component-analysis, whitening, positive-definite-matrix, explained-variance, gaussian-graphical-model, catastrophic-cancellation, pairwise-summation, factor-analysis]
sources:
  - book: isbn:9780471360919
    title: T. W. Anderson, An Introduction to Multivariate Statistical Analysis, third edition, Wiley, 2003
    locator: Chapter 2 (the covariance matrix of a random vector) and Chapter 3 (the maximum likelihood estimates of the mean vector and the covariance matrix, and the unbiased estimate)
  - paper: doi:10.1080/00401706.1962.10490022
    title: B. P. Welford, Note on a method for calculating corrected sums of squares and products, Technometrics 4(3), 419-420, 1962
    locator: the one-pass update of the mean and the corrected sums of squares and products
  - paper: doi:10.1080/00031305.1983.10483115
    title: Tony F. Chan, Gene H. Golub and Randall J. LeVeque, Algorithms for computing the sample variance, analysis and recommendations, The American Statistician 37(3), 242-247, 1983
    locator: the updating formulas, the pairwise algorithm and the error analysis of the textbook one-pass formula
  - book: isbn:9780387954424
    title: I. T. Jolliffe, Principal Component Analysis, second edition, Springer, 2002
    locator: Section 2.3 and Chapter 3 (principal components of covariance and correlation matrices)
---

The covariance matrix of a random vector $X \in \mathbb{R}^d$ is the $d \times d$ matrix $\Sigma$ whose entry $(j, l)$ is the covariance of the coordinates $X_j$ and $X_l$. Its diagonal holds the [variances](/variance/) of the coordinates. It is symmetric and positive semidefinite, and it is the input of [principal component analysis](/principal-component-analysis/), [whitening](/whitening/) and the Gaussian models of [factor analysis](/factor-analysis/). From a data set it is estimated by the sample covariance, which divides by $n - 1$, or by the maximum likelihood estimate, which divides by $n$.

## Definition

**Notation.** The data are $n$ points $x_1, \ldots, x_n \in \mathbb{R}^d$, the rows of the $n \times d$ data matrix $X$. The mean is $\bar x = \frac{1}{n} \sum_i x_i$, and the centered data matrix $X_c$ has the rows $x_i - \bar x$. The data model is a set of points in $\mathbb{R}^d$ with the Euclidean inner product; when we speak of estimation, the points are i.i.d. draws of a random vector $X$.

**Population covariance.** Let $X$ be a random vector in $\mathbb{R}^d$ with $\mathbb{E}\|X\|^2 < \infty$ and mean $\mu = \mathbb{E} X$. Its covariance matrix is

$$\Sigma = \operatorname{Cov}(X) = \mathbb{E}\big[(X - \mu)(X - \mu)^T\big], \qquad \Sigma_{jl} = \mathbb{E}\big[(X_j - \mu_j)(X_l - \mu_l)\big].$$

**Co-moment matrix.** For the data, $M = \sum_{i=1}^n (x_i - \bar x)(x_i - \bar x)^T = X_c^T X_c$. This is also called the scatter matrix, or the matrix of corrected sums of squares and products.

**Sample covariance and MLE.** The two common estimates are

$$S = \frac{1}{n - 1} M \quad (n \ge 2), \qquad \hat\Sigma = \frac{1}{n} M \quad (n \ge 1).$$

$S$ is unbiased: $\mathbb{E} S = \Sigma$. $\hat\Sigma$ is the maximum likelihood estimate of $\Sigma$ when the points are i.i.d. Gaussian, and $\mathbb{E}\hat\Sigma = \frac{n-1}{n}\Sigma$. *Proof of unbiasedness.* For each $c$, $\sum_i (x_i - c)(x_i - c)^T = M + n(\bar x - c)(\bar x - c)^T$, because the cross terms contain $\sum_i (x_i - \bar x) = 0$. With $c = \mu$, $M = \sum_i (x_i - \mu)(x_i - \mu)^T - n(\bar x - \mu)(\bar x - \mu)^T$. The first sum has expectation $n\Sigma$. By independence, $\operatorname{Cov}(\bar x) = \Sigma / n$, so the second term has expectation $\Sigma$. So $\mathbb{E} M = (n - 1)\Sigma$. $\square$

**Correlation matrix.** With $D = \operatorname{diag}(\Sigma_{11}, \ldots, \Sigma_{dd})$ and all $\Sigma_{jj} > 0$, the correlation matrix is $R = D^{-1/2} \Sigma D^{-1/2}$. It is the covariance matrix of the standardized coordinates, and its diagonal is all ones.

### Properties

- **Symmetric.** $\Sigma_{jl} = \Sigma_{lj}$ by the definition.
- **Positive semidefinite.** For each $v \in \mathbb{R}^d$, $v^T \Sigma v = \mathbb{E}[(v^T(X - \mu))^2] = \operatorname{Var}(v^T X) \ge 0$, and $v^T M v = \|X_c v\|^2 \ge 0$. So all eigenvalues are real and nonnegative (see [positive definite matrix](/positive-definite-matrix/)). The eigenvalues are the variances along the principal axes, which is the basis of PCA.
- **Rank.** $\operatorname{rank} S \le \min(d, n - 1)$. The rank of $M = X_c^T X_c$ equals the rank of $X_c$. $X_c$ has $d$ columns, and its $n$ rows sum to the zero vector, so the row space has dimension at most $n - 1$. In particular $S$ is singular when $n \le d$, and then $S^{-1}$ does not exist.
- **Positive definite case.** $S$ is positive definite if and only if $X_c$ has rank $d$, that is, no nonzero $v$ has $v^T(x_i - \bar x) = 0$ for all $i$. This needs $n \ge d + 1$ points not all on one affine hyperplane.
- **Affine maps.** $\operatorname{Cov}(AX + b) = A\Sigma A^T$ for each $m \times d$ matrix $A$ and $b \in \mathbb{R}^m$. The same rule holds for $S$ and $\hat\Sigma$ of the mapped points. [Whitening](/whitening/) uses it with $A = \Sigma^{-1/2}$.
- **Trace.** $\operatorname{tr}\Sigma = \mathbb{E}\|X - \mu\|^2$ is the total variance. It is the sum of the eigenvalues, and it is the denominator of the [explained variance](/explained-variance/) ratio.

### Computing it

The *two-pass* method computes $\bar x$ first, then sums $(x_i - \bar x)(x_i - \bar x)^T$. It costs $O(n d^2)$ operations and $O(d^2)$ memory, and it is numerically stable. The *textbook one-pass* formula $M = \sum_i x_i x_i^T - n \bar x \bar x^T$ is exact in exact arithmetic but subtracts two large, nearly equal numbers when $\|\bar x\|$ is large compared with the spread. In floating point it then suffers [catastrophic cancellation](/catastrophic-cancellation/), and it can even give a matrix that is not positive semidefinite.

**Welford update (1962).** Keep $n$, $\bar x$ and $M$. To add a point $x$:

$$n \leftarrow n + 1, \quad \delta = x - \bar x_{\text{old}}, \quad \bar x_{\text{new}} = \bar x_{\text{old}} + \delta / n, \quad M \leftarrow M + \delta\,(x - \bar x_{\text{new}})^T.$$

**Merge (Chan, Golub and LeVeque).** For two disjoint sets $A$ and $B$ with summaries $(n_A, \bar x_A, M_A)$ and $(n_B, \bar x_B, M_B)$, let $n = n_A + n_B$ and $\delta = \bar x_B - \bar x_A$. Then the summary of $A \cup B$ is

$$\bar x = \bar x_A + \delta\,\frac{n_B}{n}, \qquad M = M_A + M_B + \delta\delta^T \frac{n_A n_B}{n}.$$

*Proof.* Use the identity $\sum_{x \in A}(x - c)(x - c)^T = M_A + n_A(\bar x_A - c)(\bar x_A - c)^T$ from the proof above, for $A$ and for $B$, with $c = \bar x$. Since $\bar x_A - \bar x = -\delta n_B / n$ and $\bar x_B - \bar x = \delta n_A / n$, the two extra terms sum to $\delta\delta^T (n_A n_B^2 + n_B n_A^2)/n^2 = \delta\delta^T n_A n_B / n$. $\square$

The Welford update is the merge with $B = \{x\}$: then $n_B = 1$, $M_B = 0$ and $x - \bar x_{\text{new}} = \delta (n - 1)/n$, so $\delta(x - \bar x_{\text{new}})^T = \delta\delta^T (n-1)/n$. The merge lets a program compute $M$ in parallel over blocks, or by a pairwise tree, as in [pairwise summation](/pairwise-summation/). Chan, Golub and LeVeque (1983) analyse the rounding errors of these methods and of the one-pass formula.

## Examples and non-examples

**A small data set.** Take the $n = 4$ points $(2, 0), (4, 2), (6, 2), (8, 4)$ in $\mathbb{R}^2$. The mean is $(5, 2)$ and the centered points are $(-3, -2), (-1, 0), (1, 0), (3, 2)$. The co-moment matrix and the two estimates are

$$M = \begin{pmatrix} 20 & 12 \\ 12 & 8 \end{pmatrix}, \qquad S = \frac{M}{3} = \begin{pmatrix} 20/3 & 4 \\ 4 & 8/3 \end{pmatrix}, \qquad \hat\Sigma = \frac{M}{4} = \begin{pmatrix} 5 & 3 \\ 3 & 2 \end{pmatrix}.$$

$\hat\Sigma$ has trace 7 and determinant 1, so its eigenvalues are $(7 \pm 3\sqrt 5)/2$, about $6.854$ and $0.146$. Both are positive, as they must be for points that are not on one line. The correlation of the two coordinates is $3/\sqrt{10} \approx 0.949$.

**The merge on the same data.** Split the points into $A = \{(2,0), (4,2)\}$ and $B = \{(6,2), (8,4)\}$. Then $\bar x_A = (3, 1)$, $\bar x_B = (7, 3)$ and $M_A = M_B = \begin{pmatrix} 2 & 2 \\ 2 & 2 \end{pmatrix}$. With $\delta = (4, 2)$ and $n_A n_B / n = 1$, the merge gives $M = M_A + M_B + \delta\delta^T = \begin{pmatrix} 20 & 12 \\ 12 & 8 \end{pmatrix}$, the same matrix as above.

**Cancellation.** For the four numbers $10^9 + 4$, $10^9 + 7$, $10^9 + 13$, $10^9 + 16$ in IEEE double precision, the sample variance is $90 / 3 = 30$. The two-pass method and the Welford update give 30. The textbook one-pass formula gives 0, because $\sum x_i^2$ and $n\bar x^2$ are about $4 \cdot 10^{18}$ and their difference, 90, is below the rounding unit at that size.

**Non-examples.**

- $\begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$ is symmetric, but it is not a covariance matrix: $v = (1, -1)$ gives $v^T A v = -2 < 0$, a negative variance.
- A $3 \times 3$ matrix of rank 3 cannot be the sample covariance of 3 points, since the rank is at most $n - 1 = 2$.
- The matrix $\frac{1}{n} X^T X$ of uncentered data is the second moment matrix, not the covariance. It equals $\hat\Sigma + \bar x \bar x^T$. PCA on it finds the direction of the mean first, which is a common bug.
- A matrix of pairwise covariances where each entry is estimated from a different subset of the data (pairwise deletion of missing values) can fail to be positive semidefinite.

## Related definitions

- [Variance](/variance/) is the case $d = 1$, and the diagonal of $\Sigma$.
- [Principal component analysis](/principal-component-analysis/) diagonalizes $\Sigma$ or $S$; the eigenvalues are the variances of the components. The [Karhunen-Loève transform](/karhunen-loeve-transform/) of signal processing is the same eigenbasis for a random signal.
- [Explained variance](/explained-variance/) divides an eigenvalue by the trace.
- [Whitening](/whitening/) maps the data by a matrix $W$ with $W\Sigma W^T = I$.
- The precision matrix $\Sigma^{-1}$ gives the conditional independence structure of a [Gaussian graphical model](/gaussian-graphical-model/), and the Mahalanobis distance $\sqrt{(x - \mu)^T \Sigma^{-1}(x - \mu)}$.
- [Factor analysis](/factor-analysis/) and [probabilistic PCA](/probabilistic-pca/) model $\Sigma$ as a low-rank matrix plus a diagonal matrix.
- [Positive definite matrix](/positive-definite-matrix/): $\Sigma$ is positive definite exactly when no nonzero linear combination of the coordinates is constant.

## References
