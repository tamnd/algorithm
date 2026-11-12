---
tag: QBJGD1
kind: algorithm
slug: ordinary-least-squares
name: Ordinary least squares
aliases:
- OLS
- OLS estimator
area: machine-learning/supervised-learning
level: intro
summary: Fit linear regression weights that minimize the sum of squared residuals. Solve by QR in O(n d^2); the estimator is BLUE by Gauss-Markov.
solves: [linear-regression]
model: real-ram
complexity:
  vars: {n: the number of examples, d: "the number of features, with d <= n"}
  time: {worst: Θ(n d^2), best: Θ(n d^2)}
  space: {extra: Θ(n d)}
  flops: {worst: "2n d^2 - 2d^3/3 + O(n d)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1805
  people: [Adrien-Marie Legendre, Carl Friedrich Gauss, Andrey Markov]
  note: Legendre published the method of least squares in 1805 and Gauss in 1809. Gauss proved the optimality among linear unbiased estimators in 1821 to 1823.
prereqs: [linear-regression, least-squares-problem, qr-decomposition]
see_also: [normal-equations, householder-reflections, singular-value-decomposition, ridge-regression, condition-number, cholesky-decomposition, pseudoinverse, quantile-regression]
sources:
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 3.2 (linear regression models and least squares), Section 3.2.2 (the Gauss-Markov theorem) and Section 3.2.3 (QR and successive orthogonalization)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.3 (the full-rank least squares problem, the normal equations, the QR method, the flop counts and the sensitivity with the square of the condition number)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 11 (least squares problems by normal equations, QR and SVD), Lecture 18 (conditioning of least squares) and Lecture 19 (stability of the least squares algorithms)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 20 (the least squares problem, the backward stability of Householder QR and the error of the normal equations)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 3.1.1 (maximum likelihood and least squares) and Section 3.1.2 (the geometry of least squares)
---

Ordinary least squares (OLS) is the estimator of [linear regression](/linear-regression/) that minimizes the sum of the squared residuals $\|y - Xw\|_2^2$. When the $n \times d$ data matrix $X$ has rank $d$, the minimizer is unique and solves the [normal equations](/normal-equations/) $X^\top X w = X^\top y$. The standard way to compute it is a [QR decomposition](/qr-decomposition/) of $X$ by [Householder reflections](/householder-reflections/), in $2nd^2 - 2d^3/3$ flops, because forming $X^\top X$ squares the [condition number](/condition-number/). By the Gauss-Markov theorem, OLS has the least variance among linear unbiased estimators when the errors have mean zero, equal variance and no correlation.

## In plain words

You have a table of examples. Each row has some input numbers and one output number. You want weights, one for each input column, so that the weighted sum of the inputs in a row comes close to the output of that row. For each row, the miss is the output minus the prediction. Least squares picks the weights that make the sum of the squared misses as small as it can be.

At the best weights, the list of misses has no part left that the input columns can explain. You can find these weights by solving a small square system. A safer way first turns the input columns into a set of perpendicular directions, and then reads the weights from a triangle of numbers. The safer way keeps more correct digits when two columns are almost the same.

## The problem

The data are $n$ examples $(x_i, y_i)$ with $x_i \in \mathbb{R}^d$ and $y_i \in \mathbb{R}$. The matrix $X \in \mathbb{R}^{n \times d}$ has the rows $x_i^\top$, and an intercept is a column of ones. Find

$$\hat w = \arg\min_{w \in \mathbb{R}^d} \|y - Xw\|_2^2 = \arg\min_w \sum_{i=1}^{n} (y_i - x_i^\top w)^2 .$$

This is the [least squares problem](/least-squares-problem/) of numerical linear algebra, with the statistical meaning of [linear regression](/linear-regression/): the empirical risk under the [mean squared error](/mean-squared-error/). We assume $n \ge d$ and $\operatorname{rank} X = d$ (full column rank). Then the objective is strictly convex, and $\hat w$ is unique.

**The normal equations.** The gradient of $\|y - Xw\|^2$ is $-2X^\top(y - Xw)$. It is zero exactly when

$$X^\top X\, \hat w = X^\top y .$$

So the residual $r = y - X\hat w$ is orthogonal to each column of $X$, and $X\hat w$ is the orthogonal projection of $y$ onto the column space of $X$. With full column rank, $X^\top X$ is [positive definite](/positive-definite-matrix/), and $\hat w = (X^\top X)^{-1}X^\top y$.

## The algorithm

Householder QR writes $X = QR$ with $Q$ orthogonal ($n \times n$) and $R$ upper triangular in its first $d$ rows. An orthogonal $Q$ keeps the 2-norm, so

$$\|y - Xw\|^2 = \|Q^\top y - Rw\|^2 = \|c_1 - R_1 w\|^2 + \|c_2\|^2,$$

where $R_1$ is the top $d \times d$ block of $R$, $c_1$ is the first $d$ entries of $c = Q^\top y$, and $c_2$ is the rest. The second term does not depend on $w$, so $\hat w$ solves the triangular system $R_1 w = c_1$, and the residual sum of squares is $\|c_2\|^2$. The algorithm never forms $Q$: it applies each reflection to $y$ as it goes.

```pseudo id=main
OLS-QR(X, y)                               ▷ X is n × d, n ≥ d, rank X = d
L1  A ← a copy of X;  b ← a copy of y
L2  for k ← 1 to d do
L3      α ← −sign(A[k][k]) · ‖A[k..n][k]‖₂                 ▷ sign(0) = 1
L4      v ← A[k..n][k];  v₁ ← v₁ − α                       ▷ the Householder vector
L5      for j ← k to d do  A[k..n][j] ← A[k..n][j] − (2 vᵀA[k..n][j] / vᵀv) · v
L6      b[k..n] ← b[k..n] − (2 vᵀb[k..n] / vᵀv) · v
L7  solve the upper triangular system A[1..d][1..d] w = b[1..d] by back substitution
L8  return w
```

Lines L3 and L4 build the reflection $H_k = I - 2vv^\top / v^\top v$ that maps the column $A[k..n][k]$ to $\alpha e_1$. The sign of $\alpha$ is opposite to the sign of $A[k][k]$, so that $v_1 = A[k][k] - \alpha$ adds two numbers of the same sign and does not cancel. Line L5 applies $H_k$ to the columns $k$ to $d$, which makes the entries below the diagonal of column $k$ zero. Line L6 applies the same $H_k$ to $b$. After the loop, $A$ holds $R$ and $b$ holds $Q^\top y$. Line L7 is [back substitution](/back-substitution/). A column with $\|A[k..n][k]\| = 0$ at line L3 means that $X$ does not have full rank. The implementation stops there, with a small relative tolerance.

## Example

Fit a line $y \approx w_0 + w_1 x$ to the six points $(1, 1), (2, 3), (3, 2), (4, 5), (5, 4), (6, 9)$. So $X$ has the rows $(1, x_i)$.

**Normal equations.** $X^\top X = \begin{pmatrix} 6 & 21 \\ 21 & 91 \end{pmatrix}$ and $X^\top y = (24, 107)^\top$. The solution is $\hat w = (-3/5, 46/35)$, so the fitted line is $\hat y = -0.6 + 1.3143\,x$.

**Householder QR**, to four decimals:

| step | $\alpha$ | the column after the reflection | $b$ after the reflection |
|---|---|---|---|
| $k = 1$ | $-\sqrt{6} = -2.4495$ | column 1 becomes $(-2.4495, 0, 0, 0, 0, 0)$; column 2 becomes $(-8.5732, -0.7753, 0.2247, 1.2247, 2.2247, 3.2247)$ | $(-9.7980, -0.1303, -1.1303, 1.8697, 0.8697, 5.8697)$ |
| $k = 2$ | $\sqrt{17.5} = 4.1833$ | column 2 becomes $(-8.5732, 4.1833, 0, 0, 0, 0)$ | $(-9.7980, 5.4981, -1.3854, 0.4795, -1.6556, 2.2093)$ |

So $R_1 = \begin{pmatrix} -2.4495 & -8.5732 \\ 0 & 4.1833 \end{pmatrix}$ and $c_1 = (-9.7980, 5.4981)$. Back substitution gives $w_1 = 5.4981 / 4.1833 = 1.3143$ and $w_0 = (-9.7980 + 8.5732 \cdot 1.3143)/(-2.4495) = -0.6000$, the same as the normal equations. The sum of the squares of the last four entries of $b$ is $9.7714 = 342/35$, which is the residual sum of squares $\|y - X\hat w\|^2$.

Here $X^\top X$ has the eigenvalues $95.905$ and $1.095$, so $\kappa_2(X) = 9.36$ and $\kappa_2(X^\top X) = 87.6 = \kappa_2(X)^2$.

## Correctness

The algorithm is correct by three facts. Each $H_k$ is symmetric and orthogonal, so $H_d \cdots H_1 = Q^\top$ is orthogonal and $\|y - Xw\| = \|Q^\top y - Q^\top X w\|$ for each $w$. After step $k$, the first $k$ columns of $A$ are zero below the diagonal, and later steps do not change them. With full column rank, each diagonal entry $\alpha$ of $R_1$ is nonzero, so the triangular system has one solution, and it makes the first block of the residual zero. The full proof, with the invariant of the loop, is in the correctness proof below.

## Complexity

Count floating point operations (flops) on a [real RAM](/real-ram/), for $n \ge d$.

- **Householder QR.** Step $k$ updates a block of $(n - k + 1) \times (d - k + 1)$ entries with about 4 flops per entry. The sum over $k$ is $2nd^2 - 2d^3/3 + O(nd)$ flops (Golub and Van Loan, Section 5.3). Lines L6 and L7 add $O(nd)$ and $O(d^2)$. The time is $\Theta(nd^2)$ in each case.
- **Normal equations with Cholesky.** Forming the symmetric $X^\top X$ costs $nd^2$ flops, and [Cholesky](/cholesky-decomposition/) costs $d^3/3$. When $n \gg d$ this is about half the work of QR.
- **SVD.** The [singular value decomposition](/singular-value-decomposition/) of $X$ costs $O(nd^2)$ flops too, with a larger constant.
- **Memory.** QR overwrites a copy of $X$, so $\Theta(nd)$ extra memory, or none if $X$ may be overwritten. The normal equations need only $\Theta(d^2)$ and one pass over the data, so they suit data that does not fit in memory.

**Accuracy: why QR and not the normal equations.** Let $\kappa = \kappa_2(X) = \sigma_{\max}/\sigma_{\min}$, the ratio of the extreme singular values. The singular values of $X^\top X$ are $\sigma_i^2$, so $\kappa_2(X^\top X) = \kappa^2$. Householder QR is backward stable. When the residual is small, its computed solution has relative error of order $u\,\kappa$, where $u$ is the unit roundoff. The normal equations have error of order $u\,\kappa^2$ in general, because rounding already happens when $X^\top X$ is formed. Information can be lost at that point and cannot come back. The Läuchli matrix shows it: with $\varepsilon = 10^{-8}$,

$$X = \begin{pmatrix} 1 & 1 \\ \varepsilon & 0 \\ 0 & \varepsilon \end{pmatrix}, \qquad X^\top X = \begin{pmatrix} 1 + \varepsilon^2 & 1 \\ 1 & 1 + \varepsilon^2 \end{pmatrix}.$$

In double precision $1 + \varepsilon^2$ rounds to $1$, so the computed $X^\top X$ is singular and Cholesky fails. With $y = (2, \varepsilon, \varepsilon)$ the exact answer is $w = (1, 1)$, and Householder QR finds it to about 8 digits. When the residual is large, the least squares problem itself has a $\kappa^2$ term in its sensitivity, and the two methods are closer (Golub and Van Loan, Section 5.3).

## Properties

### Geometry and the hat matrix

$X\hat w = Hy$ with the hat matrix $H = X(X^\top X)^{-1}X^\top$, the orthogonal projection onto the column space. $H$ is symmetric, $H^2 = H$, and $\operatorname{tr} H = d$. The fitted values and the residuals are orthogonal: $(X\hat w)^\top r = 0$. With an intercept column, the residuals sum to zero, and the fitted line passes through the point of means $(\bar x, \bar y)$.

### The Gauss-Markov theorem

**Statement.** Assume the linear model $y = X\beta + \varepsilon$, where:

1. $X$ is a fixed (non-random) $n \times d$ matrix of rank $d$,
2. $\mathbb{E}[\varepsilon] = 0$,
3. $\operatorname{Cov}(\varepsilon) = \sigma^2 I$ for some $\sigma^2 > 0$: the errors have equal variance (homoscedastic) and are uncorrelated.

Let $\tilde\beta = Cy$ be any linear estimator that is unbiased for every $\beta$, that is $\mathbb{E}[Cy] = \beta$ for all $\beta \in \mathbb{R}^d$. Then $\operatorname{Cov}(\tilde\beta) - \operatorname{Cov}(\hat\beta)$ is positive semidefinite, where $\hat\beta = (X^\top X)^{-1}X^\top y$ is OLS. So for each $a \in \mathbb{R}^d$, $\operatorname{Var}(a^\top \tilde\beta) \ge \operatorname{Var}(a^\top \hat\beta)$: OLS is the best linear unbiased estimator (BLUE).

**Proof.** Unbiasedness for every $\beta$ means $CX\beta = \beta$ for all $\beta$, so $CX = I$. Write $C = (X^\top X)^{-1}X^\top + D$. Then $I = CX = I + DX$, so $DX = 0$. Since $\operatorname{Cov}(Cy) = C\operatorname{Cov}(\varepsilon)C^\top = \sigma^2 CC^\top$,

$$CC^\top = (X^\top X)^{-1}X^\top X (X^\top X)^{-1} + DX(X^\top X)^{-1} + (X^\top X)^{-1}X^\top D^\top + DD^\top = (X^\top X)^{-1} + DD^\top,$$

because $DX = 0$ and $X^\top D^\top = (DX)^\top = 0$. The matrix $(X^\top X)^{-1}$ times $\sigma^2$ is $\operatorname{Cov}(\hat\beta)$. So $\operatorname{Cov}(\tilde\beta) - \operatorname{Cov}(\hat\beta) = \sigma^2 DD^\top$, and $a^\top DD^\top a = \|D^\top a\|^2 \ge 0$. $\blacksquare$

The theorem needs no normal distribution. It compares OLS only with linear and unbiased estimators: a biased estimator such as [ridge regression](/ridge-regression/) can have a smaller mean squared error, and a nonlinear estimator can do better when the errors are not Gaussian. If the errors are correlated or have unequal variances, $\operatorname{Cov}(\varepsilon) = \sigma^2\Sigma$, then generalized least squares with weights $\Sigma^{-1}$ is the BLUE, by the same proof after the change of variables $\Sigma^{-1/2}y$.

### The Gaussian maximum likelihood view

If in addition $\varepsilon \sim \mathcal{N}(0, \sigma^2 I)$, the log-likelihood of $(\beta, \sigma^2)$ is

$$\log p(y \mid X, \beta, \sigma^2) = -\frac{n}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\|y - X\beta\|^2 .$$

For each $\sigma^2$, the maximum over $\beta$ is at the minimum of $\|y - X\beta\|^2$, so the [maximum likelihood estimate](/maximum-likelihood-estimation/) of $\beta$ is OLS. The maximum over $\sigma^2$ is $\hat\sigma^2 = \|y - X\hat\beta\|^2 / n$, which is biased. The unbiased estimate is $s^2 = \|y - X\hat\beta\|^2/(n - d)$, because $\mathbb{E}\|(I - H)\varepsilon\|^2 = \sigma^2 \operatorname{tr}(I - H) = \sigma^2(n - d)$. Under normality, $\hat\beta \sim \mathcal{N}(\beta, \sigma^2(X^\top X)^{-1})$, which gives the usual $t$ and $F$ tests.

### Other properties

- **Not exact in floating point**, but backward stable with Householder QR. With rational data, Gaussian elimination on the normal equations in exact arithmetic gives the exact $\hat w$.
- **Equivariant.** Replacing $X$ by $XA$ for an invertible $A$ replaces $\hat w$ by $A^{-1}\hat w$ and does not change the fit. So scaling a feature does not change the predictions.
- **Sensitive to outliers.** One point far from the others in $y$ moves the fit without limit. [Quantile regression](/quantile-regression/) with $\tau = 1/2$ does not have this problem.

## Variants and improvements

- **Modified Gram-Schmidt.** QR by [Gram-Schmidt](/gram-schmidt-process/) orthogonalization of the columns. The classical form loses orthogonality; the modified form gives a solution as accurate as Householder when $Q$ is not formed explicitly but the right side is processed as an extra column. ESL Section 3.2.3 shows the regression meaning: each coefficient is the regression of $y$ on the part of its column that the other columns do not explain.
- **[Givens rotations](/givens-rotations/).** Zero one entry at a time. They suit sparse $X$ and adding rows one at a time.
- **SVD.** $\hat w = V\Sigma^{-1}U^\top y$. This is the most robust method, and it handles rank deficiency: the [pseudoinverse](/pseudoinverse/) solution $X^+y$ is the least squares solution with the smallest norm.
- **QR with column pivoting.** Finds a numerical rank and a basic solution for a rank deficient $X$.
- **Iterative methods.** Conjugate gradient on the normal equations (CGLS) or LSQR for large sparse $X$, and [stochastic gradient descent](/stochastic-gradient-descent/) for data that streams.
- **Weighted and generalized least squares.** Minimize $(y - Xw)^\top W (y - Xw)$, which is OLS on $W^{1/2}X$ and $W^{1/2}y$. This is also the inner step of [iteratively reweighted least squares](/generalized-linear-model/) for GLMs.
- **Recursive least squares.** Update $\hat w$ with the [Sherman-Morrison formula](/sherman-morrison-formula/) when one example arrives, in $O(d^2)$ per example.

## When to use it

Use OLS when the number of examples is larger than the number of features, the columns are not close to dependent, and you want an unbiased estimate of the coefficients with a closed form. Use QR by default, the normal equations when $n$ is huge, $X$ is well conditioned and memory is tight, and the SVD when $X$ may be rank deficient. When $d$ is close to $n$ or larger, or the columns are nearly collinear, use [ridge regression](/ridge-regression/) or the [lasso](/lasso-regression/), which trade a small bias for a large drop in variance.

## Pitfalls

- **Forming $X^\top X$ by default.** It squares the condition number. The Läuchli example above loses all information in double precision. Use line L3 to L6 (QR) instead.
- **Inverting $X^\top X$.** Computing $(X^\top X)^{-1}$ and multiplying is slower and less accurate than a solve. Never form the inverse to get $\hat w$.
- **The wrong sign in line L3.** With $\alpha = +\operatorname{sign}(A[k][k])\|\cdot\|$, $v_1 = A[k][k] - \alpha$ cancels when the column is close to a multiple of $e_1$, and $v$ loses its accuracy.
- **Rank deficiency.** Two equal columns, or a dummy variable for each category plus an intercept, make $X^\top X$ singular. QR finds a zero pivot at line L3; detect it with a relative tolerance, not with $= 0$.
- **Reading BLUE as best.** Gauss-Markov compares only linear unbiased estimators, and only under its three hypotheses. It says nothing about heteroscedastic or correlated errors, or about biased estimators.

## Implementations

## History

Legendre published the method of least squares in 1805, for the orbits of comets. Gauss published it in 1809, linked it to the normal distribution of errors, and later (1821 to 1823) proved that it has the least variance among linear unbiased estimators. Markov restated the result in the early twentieth century, which gave the name Gauss-Markov theorem. Householder (1958) introduced the reflections, and Golub (1965) used Householder QR for least squares, which made the stable method standard.

## References
