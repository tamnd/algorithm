---
tag: SMRZT0
kind: algorithm
slug: linear-discriminant-analysis
name: Linear discriminant analysis
aliases:
- FLD
- Fisher's linear discriminant
- Fisher discriminant analysis
- multiple discriminant analysis
area: machine-learning/dimensionality-reduction
level: core
summary: "Project labelled data onto the directions that maximize between-class over within-class scatter, found from S_B w = λ S_W w. It gives at most k - 1 directions for k classes."
solves: [classification]
model: real-ram
complexity:
  vars: {n: the number of training examples, d: the number of features, k: the number of classes, r: "the number of directions kept, at most k - 1"}
  time: {worst: "O(n d^2 + d^3)", best: "Θ(n d^2 + d^3)"}
  space: {extra: "Θ(d^2)"}
properties: {deterministic: true, online: false, exact: true, recursive: false, supervised: true, linear: true}
history:
  year: 1936
  people: [Ronald A. Fisher, C. Radhakrishna Rao]
  note: Fisher introduced the discriminant for two classes in 1936 and applied it to the iris data. Rao extended it to several classes in 1948.
prereqs: [covariance-matrix, generalized-eigenvalue-problem, rayleigh-quotient]
see_also: [quadratic-discriminant-analysis, bayes-optimal-classifier, principal-component-analysis, canonical-correlation-analysis, cholesky-decomposition, classification, logistic-regression, latent-dirichlet-allocation]
sources:
  - paper: doi:10.1111/j.1469-1809.1936.tb02137.x
    title: Ronald A. Fisher, The use of multiple measurements in taxonomic problems, Annals of Eugenics 7(2), 1936
    locator: pp. 179 to 188 (the criterion, the two-class solution, the iris example)
  - paper: "C. Radhakrishna Rao, The utilization of multiple measurements in problems of biological classification, Journal of the Royal Statistical Society, Series B 10(2), 1948"
    locator: pp. 159 to 203 (discrimination among several groups)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 4.3 (linear discriminant analysis, eq. 4.10) and Section 4.3.3 (reduced-rank LDA and Fisher's problem)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Sections 4.1.4 to 4.1.6 (Fisher's linear discriminant, its relation to least squares, Fisher's discriminant for several classes)
  - book: isbn:9780471056690
    title: Richard O. Duda, Peter E. Hart and David G. Stork, Pattern Classification, second edition, Wiley, 2001
    locator: Section 3.8 (Fisher linear discriminant and multiple discriminant analysis)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.7 (the symmetric-definite generalized eigenproblem and its reduction by a Cholesky factor)
---

Linear discriminant analysis (LDA) is a supervised linear method for labelled data in $\mathbb{R}^d$. The name has two meanings that give the same answer in the main case. **Fisher's discriminant** is a projection: it finds the directions $w$ that maximize the ratio of the between-class scatter to the within-class scatter, which are the top solutions of the [generalized eigenvalue problem](/generalized-eigenvalue-problem/) $S_B w = \lambda S_W w$, and there are at most $k - 1$ useful directions for $k$ classes. **The Gaussian LDA classifier** is the [Bayes rule](/bayes-optimal-classifier/) for Gaussian classes with one shared [covariance matrix](/covariance-matrix/); its class boundaries are hyperplanes, and [quadratic discriminant analysis](/quadratic-discriminant-analysis/) is the version with one covariance per class. For two classes, Fisher's direction is $S_W^{-1}(\mu_1 - \mu_0)$, and the Gaussian classifier thresholds the projection on it.

## In plain words

You have points from a few labelled groups and you want to look at them along a few directions only. Principal component analysis picks the direction where the whole cloud is widest, and it ignores the labels. That direction can mix the groups together. LDA uses the labels. It looks for a direction where the group centers are far apart and each group is narrow at the same time. It scores a direction by the spread of the centers divided by the spread inside the groups, and it keeps the best directions.

With two groups, one direction is enough, because two centers lie on one line. With three groups, two directions are enough, because three centers lie in one plane. In general, the number of useful directions is one less than the number of groups.

## The problem

The data are $n$ labelled examples $(x_i, y_i)$ with $x_i \in \mathbb{R}^d$ and $y_i$ in one of $k$ classes. Class $c$ has $n_c$ points and mean $\mu_c$, and $\mu$ is the overall mean. The two scatter matrices are
$$ S_W = \sum_{c} \sum_{i : y_i = c} (x_i - \mu_c)(x_i - \mu_c)^{\top}, \qquad S_B = \sum_c n_c (\mu_c - \mu)(\mu_c - \mu)^{\top} . $$
Their sum is the total scatter $S_T = \sum_i (x_i - \mu)(x_i - \mu)^{\top}$. Fisher's criterion for a direction $w \ne 0$ is
$$ J(w) = \frac{w^{\top} S_B w}{w^{\top} S_W w} . $$
The output is $r \le k - 1$ directions $w_1, \ldots, w_r$, where $w_t$ maximizes $J$ among the directions with $w^{\top} S_W w_s = 0$ for $s < t$ (the projections on different directions are uncorrelated within the classes). The reduced data are $z_i = W^{\top} x_i$ with $W = [w_1, \ldots, w_r]$. The page assumes that $S_W$ is [positive definite](/positive-definite-matrix/), which needs $n - k \ge d$.

## The algorithm

The algorithm reduces the generalized problem to an ordinary symmetric one with a [Cholesky factor](/cholesky-decomposition/) of $S_W$, and solves that with a [symmetric eigensolver](/symmetric-eigenproblem/).

```pseudo id=main
FISHER-LDA(X, y, r)
L1  for each class c do n_c ← |{i : y_i = c}|, μ_c ← mean of its points;  μ ← mean of all points
L2  S_W ← Σ_c Σ_{i: y_i = c} (x_i − μ_c)(x_i − μ_c)ᵀ
L3  S_B ← Σ_c n_c (μ_c − μ)(μ_c − μ)ᵀ
L4  L ← the Cholesky factor of S_W, with L Lᵀ = S_W      ▷ fails if S_W is singular
L5  M ← L⁻¹ S_B L⁻ᵀ                                       ▷ by triangular solves
L6  (λ_t, v_t) for t = 1..d ← eigenpairs of M, with λ_1 ≥ … ≥ λ_d and orthonormal v_t
L7  w_t ← L⁻ᵀ v_t for t = 1..r
L8  return λ_1..λ_r and W = [w_1 … w_r]
```

The returned directions satisfy $W^{\top} S_W W = I$, so the projected classes have unit pooled scatter along each direction, and $J(w_t) = \lambda_t$. To classify a point with the Gaussian LDA rule, use the pooled maximum likelihood covariance $\Sigma = S_W / n$, the priors $\pi_c = n_c / n$, and the linear discriminant functions (ESL eq. 4.10)
$$ \delta_c(x) = x^{\top} \Sigma^{-1} \mu_c - \tfrac12 \mu_c^{\top} \Sigma^{-1} \mu_c + \log \pi_c , $$
and predict the class with the largest $\delta_c(x)$. With $r = k - 1$ directions this is the same as predicting $\arg\max_c \big(-\frac n2 \lVert W^{\top}(x - \mu_c) \rVert^2 + \log \pi_c\big)$ in the projected space, so the reduction loses nothing that the Gaussian classifier uses.

## Example

Two classes in $\mathbb{R}^2$ with four points each:

| class | points | mean | scatter |
| --- | --- | --- | --- |
| A | (1, 2), (2, 3), (3, 3), (2, 4) | (2, 3) | $\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ |
| B | (4, 4), (5, 6), (6, 5), (5, 5) | (5, 5) | $\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ |

So $S_W = \begin{pmatrix} 4 & 2 \\ 2 & 4 \end{pmatrix}$, $\delta = \mu_B - \mu_A = (3, 2)$, and $S_B = \frac{4 \cdot 4}{8} \delta \delta^{\top} = 2\,\delta\delta^{\top}$. The Fisher direction is
$$ S_W^{-1} \delta = \tfrac1{12} \begin{pmatrix} 4 & -2 \\ -2 & 4 \end{pmatrix} \begin{pmatrix} 3 \\ 2 \end{pmatrix} = \begin{pmatrix} 2/3 \\ 1/6 \end{pmatrix} \propto (4, 1) , $$
with $J = 2\, \delta^{\top} S_W^{-1} \delta = 2 (2 + \tfrac13) = \tfrac{14}{3} \approx 4.667$. Other directions score less:

| direction | $J$ |
| --- | --- |
| Fisher, $(4, 1)$ | 14/3 ≈ 4.667 |
| the first axis, $(1, 0)$ | 9/2 = 4.5 |
| the mean difference, $(3, 2)$ | 169/38 ≈ 4.447 |
| the first principal component of all eight points, about $(0.817, 0.576)$ | ≈ 4.416 |
| the diagonal, $(1, 1)$ | 25/6 ≈ 4.167 |
| the second axis, $(0, 1)$ | 2 |

The projections $4 x_1 + x_2$ are 6, 11, 15, 12 for class A and 20, 26, 29, 25 for class B, so the classes separate with a gap from 15 to 20. The Gaussian LDA rule with equal priors has $\Sigma^{-1} \delta = 8\, S_W^{-1} \delta = \frac43 (4, 1)$, and its boundary is the line $4 x_1 + x_2 = 18$, which passes through the midpoint $(3.5, 4)$ of the two means. The normalized direction from line L7 is $(0.4364, 0.1091)$, which has $w^{\top} S_W w = 1$.

If a third class C with points (8, 1), (9, 2), (10, 1), (9, 0) is added, $S_B$ has rank 2 and the two generalized eigenvalues are about 25.93 and 2.57. In $\mathbb{R}^d$ with $d > 2$, three classes still give only two nonzero eigenvalues.

## Correctness

Put $u = L^{\top} w$. Then $w^{\top} S_W w = u^{\top} u$ and $w^{\top} S_B w = u^{\top} M u$, so $J(w)$ is the [Rayleigh quotient](/rayleigh-quotient/) of the symmetric matrix $M$ at $u$, and the $S_W$-orthogonality constraints become ordinary orthogonality. By the [Courant-Fischer theorem](/courant-fischer-theorem/), the constrained maxima are the eigenvalues of $M$ in decreasing order, attained at its eigenvectors, and $M v = \lambda v$ is the same as $S_B w = \lambda S_W w$. The rank bound follows from $\sum_c n_c (\mu_c - \mu) = 0$: the $k$ vectors $\mu_c - \mu$ span at most $k - 1$ dimensions, so $S_B$ has rank at most $k - 1$, and every later direction has $J = 0$ and gives all class means the same projection. For two classes $S_B$ is a multiple of $\delta\delta^{\top}$, which forces $w \propto S_W^{-1}\delta$. The full proofs, including the equivalence with the Gaussian classifier in the projected space, are below.

## Complexity

The model is the [real RAM](/real-ram/), and the costs count arithmetic operations.

- **Scatter matrices.** $\Theta(n d^2)$: one $d \times d$ outer product per point for $S_W$, and $k$ of them for $S_B$.
- **Eigenproblem.** The Cholesky factor costs about $d^3/3$ operations, the matrix $M$ costs $\Theta(d^3)$ by triangular solves, and a symmetric QR eigensolver costs $\Theta(d^3)$. Since $M$ has rank at most $k - 1$, it is cheaper to write $S_B = B B^{\top}$ with the $k$ columns $\sqrt{n_c}(\mu_c - \mu)$ and to take the [SVD](/singular-value-decomposition/) of the $d \times k$ matrix $L^{-1} B$, in $O(d k^2)$ operations.
- **Total.** $O(n d^2 + d^3)$ time and $\Theta(d^2)$ extra memory. Projecting one point costs $\Theta(r d)$ and one Gaussian LDA prediction costs $\Theta(k d)$.

The method is exact: it has no iterations apart from the eigensolver, no learning rate and no local optima.

## Properties

- **At most $k - 1$ directions.** Asking for more directions than $k - 1$ returns directions with $J = 0$, which are arbitrary inside the null space of $S_B$.
- **Invariance.** For an invertible matrix $A$, the map $x \mapsto A x$ turns $S_W$ into $A S_W A^{\top}$ and $S_B$ into $A S_B A^{\top}$, so $J(A^{-\top} w)$ on the new data equals $J(w)$ on the old data. The projections $w^{\top} x$, and hence the classifier, do not change. PCA does not have this property.
- **Total scatter gives the same directions.** With $J_T(w) = w^{\top} S_B w / w^{\top} S_T w$ one gets $J_T = J / (1 + J)$, an increasing function of $J$, so the maximizers are the same. This form is used when $S_W$ is not stored.
- **No distribution needed for the projection.** Fisher's criterion uses only means and scatter matrices. The Gaussian model is needed only to call the classifier Bayes optimal.
- **Linear boundaries.** The Gaussian LDA classifier divides $\mathbb{R}^d$ into convex cells bounded by hyperplanes.

## Variants and improvements

- **Regularized LDA.** Replace $S_W$ by $S_W + \gamma I$ with $\gamma > 0$. This makes line L4 work when $n - k < d$, and it is the $\gamma$ part of Friedman's regularized discriminant analysis on the [QDA page](/quadratic-discriminant-analysis/).
- **Reduced-rank LDA.** Classify with only $r < k - 1$ directions, the nearest projected mean with the prior term. ESL Section 4.3.3 shows that this is the Gaussian classifier with the class means restricted to an $r$-dimensional subspace.
- **PCA then LDA.** For images and other data with $d > n$, first project onto the leading [principal components](/principal-component-analysis/) so that $S_W$ becomes invertible, then run LDA.
- **Kernel Fisher discriminant.** Replace the inner products by a kernel, as in [kernel PCA](/kernel-pca/), to get nonlinear projections. This needs regularization, because the within-class scatter in the feature space is singular.
- **Large $d$ with low rank.** Use the SVD form of the complexity section, or solve the generalized problem directly with the [QZ algorithm](/qz-algorithm/) when $S_W$ is badly conditioned.

## When to use it

Use Fisher LDA to reduce labelled data to $k - 1$ or fewer dimensions before plotting or before a simple classifier such as [k nearest neighbors](/k-nearest-neighbors/). Use the Gaussian LDA classifier when the classes have similar spreads and $n$ is small compared with $d^2$; it estimates one covariance instead of $k$, so it has much less variance than QDA. Do not use it when the classes differ in spread but not in mean, when classes have several clusters, or when the boundary is strongly curved.

## Pitfalls

- **Singular $S_W$.** With $n - k < d$, or with a feature that is constant within each class, line L4 fails. Use regularization or PCA first, not a pseudo-inverse with no thought: the null space of $S_W$ contains directions with $J = \infty$ that separate the training data perfectly and generalize badly.
- **Equal means.** If all class means are equal, $S_B = 0$ and every direction has $J = 0$, even when the classes have very different covariances. LDA sees only differences in the means.
- **Too many components.** Libraries return at most $k - 1$ components for this reason. A plot of the third Fisher direction for three classes shows noise.
- **PCA is not LDA.** The direction of largest total variance can be the worst one for separation; in the example above it scores 4.416 against 4.667, and with long thin classes the difference can be arbitrarily large.
- **Two different LDAs.** The abbreviation LDA also names [latent Dirichlet allocation](/latent-dirichlet-allocation/), a topic model with no relation to this method.
- **Normalization.** Directions are defined only up to scale. Fix a scale such as $W^{\top} S_W W = I$ before you compare distances in the projected space.

## Implementations

## History

Ronald Fisher introduced the criterion in 1936 for two classes, and applied it to the iris measurements of three species. He asked for the linear function of the measurements that best separates two species relative to the variation within species. C. R. Rao extended the method to several groups in 1948. The Gaussian derivation with a shared covariance, and its quadratic version with separate covariances, became standard in multivariate statistics. The textbooks of Duda, Hart and Stork and of Hastie, Tibshirani and Friedman present the projection and the classifier as two views of one method.

## References
