---
tag: 2S7QFD
kind: algorithm
slug: canonical-correlation-analysis
name: Canonical correlation analysis
aliases:
- CCA
- canonical correlations
- canonical variates
area: machine-learning/dimensionality-reduction
level: core
summary: "Find paired directions a and b for two sets of variables that maximize corr(a^T x, b^T y). The answer is the SVD of C_XX^(-1/2) C_XY C_YY^(-1/2)."
model: real-ram
complexity:
  vars: {n: the number of paired examples, p: the number of features in the first view, q: the number of features in the second view}
  time: {worst: "O(n (p + q)^2 + (p + q)^3)", best: "Θ(n (p + q)^2 + p^3 + q^3)"}
  space: {extra: "Θ((p + q)^2)"}
properties: {deterministic: true, online: false, exact: true, recursive: false, supervised: false, linear: true}
history:
  year: 1936
  people: [Harold Hotelling]
  note: Hotelling defined canonical correlations and canonical variates in 1936, in the same period as his work on principal components.
prereqs: [covariance-matrix, singular-value-decomposition, whitening]
see_also: [principal-component-analysis, linear-discriminant-analysis, kernel-pca, factor-analysis, tikhonov-regularization, gram-schmidt-process, independent-component-analysis, golub-kahan-svd-algorithm]
sources:
  - paper: doi:10.1093/biomet/28.3-4.321
    title: Harold Hotelling, Relations between two sets of variates, Biometrika 28(3/4), 1936
    locator: pp. 321 to 377 (the definition of canonical correlations and variates, and the determinantal equation for them)
  - book: isbn:9780471360919
    title: T. W. Anderson, An Introduction to Multivariate Statistical Analysis, third edition, Wiley, 2003
    locator: Chapter 12 (canonical correlations and canonical variables)
  - paper: doi:10.1162/0899766042321814
    title: David R. Hardoon, Sandor Szedmak and John Shawe-Taylor, Canonical correlation analysis, an overview with application to learning methods, Neural Computation 16(12), 2004
    locator: Sections 2 to 4 (CCA as a generalized eigenproblem, regularized CCA, kernel CCA)
  - paper: "Åke Björck and Gene H. Golub, Numerical methods for computing angles between linear subspaces, Mathematics of Computation 27(123), 1973"
    locator: pp. 579 to 594 (principal angles from the SVD of Q_X^T Q_Y, and canonical correlations as their cosines)
---

Canonical correlation analysis (CCA) takes two sets of variables measured on the same $n$ examples, a vector $x \in \mathbb{R}^p$ and a vector $y \in \mathbb{R}^q$, and finds weight vectors $a$ and $b$ that make the scores $a^{\top} x$ and $b^{\top} y$ as correlated as possible. Then it finds a second pair, uncorrelated with the first, and so on, up to $\min(p, q)$ pairs. Hotelling (1936) defined it. The solution is the [singular value decomposition](/singular-value-decomposition/) of the whitened cross-covariance $C_{XX}^{-1/2} C_{XY} C_{YY}^{-1/2}$: its singular values are the canonical correlations. With a ridge term on the two covariance blocks it becomes regularized CCA, which works when $n$ is small compared with $p + q$.

## In plain words

You measure two kinds of things on the same people: some blood values and some answers to a questionnaire. You want to know how the two groups of numbers are related. Each group has many columns, so you cannot just compare one column with one column. CCA makes one weighted sum of the blood values and one weighted sum of the answers, and chooses the weights so that the two sums go up and down together as closely as possible. That pair is the strongest shared signal. Then it looks for a second pair that carries new shared information, and so on.

The method does not care about the units of the columns or about columns that repeat each other. It finds what the two groups have in common, not what is large in each group.

## The problem

The data are $n$ paired examples $(x_i, y_i)$ with $x_i \in \mathbb{R}^p$ and $y_i \in \mathbb{R}^q$, stacked as the $n \times p$ matrix $X$ and the $n \times q$ matrix $Y$. No labels are used: the second view plays the role that labels play in [linear discriminant analysis](/linear-discriminant-analysis/). After centring each column, the covariance blocks are
$$ C_{XX} = \tfrac1n X^{\top} X, \qquad C_{YY} = \tfrac1n Y^{\top} Y, \qquad C_{XY} = \tfrac1n X^{\top} Y = C_{YX}^{\top} . $$
For weights $a \ne 0$ and $b \ne 0$ the sample correlation of the scores is
$$ \rho(a, b) = \frac{a^{\top} C_{XY} b}{\sqrt{a^{\top} C_{XX} a}\, \sqrt{b^{\top} C_{YY} b}} . $$
The first canonical pair maximizes $\rho(a, b)$. The $t$-th pair maximizes it among the $a$ with $a^{\top} C_{XX} a_s = 0$ for $s < t$, which makes the new score uncorrelated with the earlier ones. The maxima $\rho_1 \ge \rho_2 \ge \cdots \ge \rho_m \ge 0$, with $m = \min(p, q)$, are the canonical correlations, and $a_t^{\top} x$, $b_t^{\top} y$ are the canonical variates. The same definitions with the population covariances $\Sigma_{XX}$, $\Sigma_{YY}$, $\Sigma_{XY}$ give the population CCA.

## The algorithm

```pseudo id=main
CCA(X, Y, κ_X, κ_Y)
L1  centre each column of X and of Y
L2  C_XX ← XᵀX / n,  C_YY ← YᵀY / n,  C_XY ← XᵀY / n
L3  C_XX ← C_XX + κ_X I,  C_YY ← C_YY + κ_Y I                ▷ κ = 0 gives plain CCA
L4  R_X ← C_XX^(−1/2),  R_Y ← C_YY^(−1/2)                    ▷ symmetric inverse square roots
L5  T ← R_X C_XY R_Y                                         ▷ a p × q matrix
L6  T = Σ_t σ_t u_t v_tᵀ with σ_1 ≥ σ_2 ≥ … ≥ σ_m ≥ 0         ▷ thin SVD
L7  a_t ← R_X u_t,  b_t ← R_Y v_t   for t = 1..m
L8  return ρ_t = σ_t and the pairs (a_t, b_t)
```

Line L4 needs the two blocks to be positive definite. Without the ridge terms this requires $n - 1 \ge p$ and $n - 1 \ge q$ and no exactly dependent columns. The implementation computes the inverse square roots and the SVD with a Jacobi eigensolver: $R = V \Lambda^{-1/2} V^{\top}$ from $C = V \Lambda V^{\top}$, and the SVD from the eigenvectors $u_t$ of $T T^{\top}$ with $v_t = T^{\top} u_t / \sigma_t$. A [Cholesky factor](/cholesky-decomposition/) $C_{XX} = L L^{\top}$ can replace the symmetric root: $L^{-1}$ differs from $C_{XX}^{-1/2}$ by an orthogonal factor on the left, which does not change the singular values. The scaling of line L7 gives $a_t^{\top} C_{XX} a_t = b_t^{\top} C_{YY} b_t = 1$, so each canonical variate has unit variance.

## Example

Take a population with $p = q = 2$ and unit variances:
$$ \Sigma_{XX} = \begin{pmatrix} 1 & 0.6 \\ 0.6 & 1 \end{pmatrix}, \qquad \Sigma_{YY} = I, \qquad \Sigma_{XY} = \begin{pmatrix} 0.5 & 0.2 \\ 0 & 0 \end{pmatrix} . $$
The joint $4 \times 4$ covariance has eigenvalues about 1.806, 1, 1 and 0.194, so it is valid. The second variable $x_2$ is uncorrelated with both $y_1$ and $y_2$. Since $\Sigma_{XY}$ has rank 1, there is one nonzero canonical correlation, and
$$ \rho_1^2 = \max_a \frac{a^{\top} \Sigma_{XY} \Sigma_{XY}^{\top} a}{a^{\top} \Sigma_{XX} a} = 0.29 \cdot (\Sigma_{XX}^{-1})_{11} = \frac{0.29}{0.64}, \qquad \rho_1 = \frac{\sqrt{29}}{8} \approx 0.6731 . $$
The weights are $a_1 = (1.25, -0.75)$, proportional to $\Sigma_{XX}^{-1} e_1 \propto (1, -0.6)$, and $b_1 = (0.5, 0.2)/\sqrt{0.29} \approx (0.9285, 0.3714)$, with $a_1^{\top} \Sigma_{XX} a_1 = 1$. The second correlation is $\rho_2 = 0$.

The variable $x_2$ has no correlation with $y$, but it gets the weight $-0.75$. It removes the part of $x_1$ that is noise shared with $x_2$, and this raises the correlation from $\sqrt{0.29} \approx 0.5385$ (with $x_1$ alone) to $0.6731$. The direction of largest covariance, the top left singular vector of $\Sigma_{XY}$ as in partial least squares, is $(1, 0)$, and it gets only 0.5385. So CCA is not the SVD of the raw cross-covariance: the whitening in line L4 matters.

In the step-by-step form, $\Sigma_{XX}^{-1/2} = \begin{pmatrix} 1.1859 & -0.3953 \\ -0.3953 & 1.1859 \end{pmatrix}$, $T = \begin{pmatrix} 0.5929 & 0.2372 \\ -0.1976 & -0.0791 \end{pmatrix}$, and the singular values of $T$ are $0.6731$ and 0.

## Correctness

Put $u = C_{XX}^{1/2} a$ and $v = C_{YY}^{1/2} b$. Then $\rho(a, b) = u^{\top} T v / (\lVert u \rVert \lVert v \rVert)$, and the constraint $a^{\top} C_{XX} a_s = 0$ becomes $u^{\top} u_s = 0$. Expand $u$ and $v$ in the singular vectors of $T$: $u^{\top} T v = \sum_k \sigma_k \alpha_k \beta_k$, and with $\alpha_s = 0$ for $s < t$ the Cauchy-Schwarz inequality bounds this by $\sigma_t$, which the pair $(u_t, v_t)$ attains. So the canonical correlations are the singular values, in order. The same expansion shows that the canonical variates are uncorrelated across pairs, both within and across the two views, and that $\rho_t \le 1$. The full proof, with the link to principal angles, is below.

## Complexity

The model is the [real RAM](/real-ram/).

- **Covariances.** $\Theta(n (p + q)^2)$ operations for line L2.
- **Whitening.** $\Theta(p^3 + q^3)$ for the two symmetric eigendecompositions of line L4, or about $(p^3 + q^3)/3$ with Cholesky factors.
- **SVD.** $\Theta(p q \min(p, q))$ for the $p \times q$ matrix $T$.
- **Total.** $O(n (p + q)^2 + (p + q)^3)$ time and $\Theta((p + q)^2)$ extra memory. Scoring a new pair costs $\Theta(r(p + q))$ for $r$ kept pairs.

For large $n$ the covariance step dominates; for wide data ($p$ or $q$ in the thousands) the cubic terms dominate, and iterative methods that never form $C_{XX}$ are used.

## Properties

- **Invariance.** For invertible $G$ and $H$, the data $(X G^{\top} + 1 c^{\top}, Y H^{\top} + 1 e^{\top})$ have the same canonical correlations. The units and the correlations inside each view do not matter. This is the main difference from [PCA](/principal-component-analysis/) and from partial least squares.
- **Symmetry.** Swapping $X$ and $Y$ gives the same correlations and swaps the weights.
- **Special cases.** With $q = 1$, $\rho_1$ is the multiple correlation coefficient of the [least squares](/ordinary-least-squares/) regression of $y$ on $x$. With $Y$ the indicator matrix of $k$ classes (one column dropped), CCA gives Fisher's [discriminant directions](/linear-discriminant-analysis/), with $\rho_t^2 = \lambda_t / (1 + \lambda_t)$ for the Fisher eigenvalues $\lambda_t$.
- **Principal angles.** The canonical correlations are the cosines of the principal angles between the column spaces of the centred $X$ and $Y$ (Björck and Golub 1973). This gives a stable way to compute them: take QR factorizations $X = Q_X R_X$, $Y = Q_Y R_Y$ with [Gram-Schmidt](/gram-schmidt-process/) or Householder, then the SVD of $Q_X^{\top} Q_Y$.
- **Gaussian view.** For jointly Gaussian $(x, y)$, the mutual information between the two views is $-\frac12 \sum_t \log(1 - \rho_t^2)$, so CCA finds all the shared information of a Gaussian pair.

## Variants and improvements

- **Regularized CCA.** Lines L3 with $\kappa_X, \kappa_Y > 0$. This is a [Tikhonov regularization](/tikhonov-regularization/) of the two blocks. As $\kappa \to \infty$, $C_{XX} + \kappa I$ is dominated by $\kappa I$ and the weights tend to the singular vectors of $C_{XY}$, which is partial least squares. Choose $\kappa$ by [cross-validation](/cross-validation/) on the correlation of held-out scores.
- **Kernel CCA.** Replace the two views by kernel feature maps. Without regularization, kernel CCA always finds correlation 1 on the training data, so the ridge term is required (Hardoon and others 2004).
- **Sparse CCA.** Add $\ell_1$ penalties on $a$ and $b$ so that each pair uses few variables, for genomics data with $p$ and $q$ much larger than $n$.
- **More than two views.** Generalized CCA maximizes a function of all pairwise correlations among several views.
- **Probabilistic CCA.** A latent variable model in which a shared Gaussian factor generates both views, like [factor analysis](/factor-analysis/) with two blocks; its maximum likelihood solution is spanned by the canonical directions.

## When to use it

Use CCA when you have two views of the same examples (two sensors, images and captions, genes and proteins, two languages) and want the directions they share. Use it to build features for one view that predict the other, or to align two embeddings. With $n$ not much larger than $p + q$, always regularize and test the correlations on held-out data.

## Pitfalls

- **Small samples give correlation 1.** The centred columns lie in a space of dimension $n - 1$. If $p + q > n - 1$, the two column spaces meet, and at least $p + q - n + 1$ canonical correlations equal 1 for any data, even pure noise. With $n = 5$ and $p = q = 3$, the first two are exactly 1.
- **Large $\rho$ does not mean large variance.** A canonical variate can be a tiny, high-correlation direction that carries almost no variance of either view. Check the variance that each variate explains.
- **Weights are not loadings.** The weights $a_t$ can have large signs that cancel, as $x_2$ in the example shows. To interpret a variate, use the correlations between it and the original variables (the structure coefficients).
- **Squaring the condition number.** Forming $C_{XX}$ and taking $C_{XX}^{-1/2}$ squares the condition number of $X$. For ill-conditioned data use the QR form.
- **Significance.** The sample $\rho_1$ is biased upward. Use a permutation test or Bartlett's test before you report a canonical correlation as real.

## Implementations

## History

Harold Hotelling introduced canonical correlations and canonical variates in 1936, as the general answer to the question of how two sets of variables are related; he called the pairs the canonical variates and the maxima the canonical correlations. The method became a standard part of multivariate analysis, in texts such as Anderson's. Björck and Golub (1973) gave the numerical method through principal angles between subspaces. Regularized and kernel forms entered machine learning around 2000, and Hardoon, Szedmak and Shawe-Taylor (2004) surveyed them.

## References
