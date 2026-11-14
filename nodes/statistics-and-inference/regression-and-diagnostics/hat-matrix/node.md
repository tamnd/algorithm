---
tag: 7G73ZX
kind: definition
slug: hat-matrix
name: Hat matrix
aliases:
- influence matrix
- projection matrix of least squares
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: The matrix H = X (X^T X)^(-1) X^T that maps the responses to the fitted values. It is a projection; its diagonal holds the leverages.
prereqs: [ordinary-least-squares, qr-decomposition]
see_also: [leverage-statistics, studentized-residual, cooks-distance, pseudoinverse, singular-value-decomposition, sherman-morrison-formula, cross-validation, ridge-regression]
sources:
  - paper: doi:10.1080/00031305.1978.10479237
    title: "David C. Hoaglin and Roy E. Welsch, The hat matrix in regression and ANOVA, The American Statistician 32(1), 1978, pp. 17 to 22"
    locator: The whole paper (the properties of H, the bounds on its diagonal, the average p/n and the rule 2p/n)
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: Chapter 3 (least squares as an orthogonal projection, idempotent matrices and their trace) and Section 10.2 (residuals and hat matrix diagonals)
  - book: isbn:9780471058564
    title: David A. Belsley, Edwin Kuh and Roy E. Welsch, Regression Diagnostics, Wiley, 1980
    locator: Chapter 2 (the hat matrix and the diagnostics built on its diagonal)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.2 (the thin QR factorization, whose Q_1 Q_1^T is the orthogonal projection on the range of X)
---

The hat matrix of a linear regression is the $n \times n$ matrix $H$ that turns the observed responses $y$ into the fitted values: $\hat y = Hy$. It "puts the hat on $y$". For a design matrix $X$ of full column rank it is $H = X(X^\top X)^{-1}X^\top$, the orthogonal projection onto the column space of $X$. It depends only on $X$, not on $y$. Its diagonal entries are the [leverages](/leverage-statistics/), and most single-point regression diagnostics ([studentized residuals](/studentized-residual/), [Cook's distance](/cooks-distance/), leave-one-out residuals) are simple functions of $H$ and the residuals. The fit itself is on the [ordinary least squares](/ordinary-least-squares/) page.

## Definition

Let $X$ be a real $n \times p$ matrix of rank $p$ (so $p \le n$). Its $p$ columns include the intercept column of ones when the model has one; some texts write $k$ for $p$. The **hat matrix** is

$$H = X(X^\top X)^{-1}X^\top, \qquad h_{ij} = x_i^\top (X^\top X)^{-1} x_j,$$

where $x_i^\top$ is row $i$ of $X$. If $\hat b = (X^\top X)^{-1}X^\top y$ is the least squares coefficient vector, then $\hat y = X\hat b = Hy$ and the residual vector is $e = y - \hat y = (I - H)y$. The matrix $I - H$ is sometimes called the residual maker.

**Computation.** With a thin [QR decomposition](/qr-decomposition/) $X = Q_1R$, where $Q_1$ is $n \times p$ with orthonormal columns and $R$ is nonsingular, $H = Q_1R R^{-1}R^{-\top}R^\top Q_1^\top = Q_1Q_1^\top$. With a thin [singular value decomposition](/singular-value-decomposition/) $X = U\Sigma V^\top$, $H = UU^\top$. So $h_{ii}$ is the squared length of row $i$ of $Q_1$, which costs $O(np^2)$ for the factorization and $O(np)$ for all diagonal entries, without forming $X^\top X$ or the $n \times n$ matrix $H$. If $X$ has rank $r < p$, the projection onto its column space is still unique and equals $XX^+$, with $X^+$ the [pseudoinverse](/pseudoinverse/), but the formula with $(X^\top X)^{-1}$ does not apply.

**Properties.** Each follows from the definition in one or two lines.

1. *Symmetric:* $H^\top = H$, since $(X^\top X)^{-1}$ is symmetric.
2. *Idempotent:* $H^2 = X(X^\top X)^{-1}X^\top X(X^\top X)^{-1}X^\top = H$. So $H$ is the orthogonal projection onto $\operatorname{col}(X)$, and $I - H$ is the orthogonal projection onto its orthogonal complement, the residual space. In particular $HX = X$, $(I - H)X = 0$ and $X^\top e = 0$.
3. *Trace and rank $p$:* $\operatorname{tr} H = \operatorname{tr}((X^\top X)^{-1}X^\top X) = \operatorname{tr} I_p = p$. A symmetric idempotent matrix has [eigenvalues](/eigenvalue/) $\lambda$ with $\lambda^2 = \lambda$, so each is 0 or 1; $H$ has $p$ eigenvalues 1 and $n - p$ eigenvalues 0, and $\operatorname{tr}(I - H) = n - p$, the residual degrees of freedom.
4. *Only the column space matters:* if $A$ is a nonsingular $p \times p$ matrix, $XA$ has the same hat matrix. Rescaling, centering or reordering the predictors does not change $H$.
5. *Sensitivities:* $h_{ij} = \partial \hat y_i/\partial y_j$. Row $i$ gives the weights with which the fitted value $\hat y_i$ averages the responses.
6. *Covariances:* if $\operatorname{Var}(y) = \sigma^2 I$, then $\operatorname{Var}(\hat y) = \sigma^2 H$ and $\operatorname{Var}(e) = \sigma^2(I - H)$, so $\operatorname{Var}(e_i) = \sigma^2(1 - h_{ii})$: residuals are correlated and have unequal variances even when the errors do not.
7. *Diagonal bounds:* $h_{ii} = \sum_j h_{ij}^2 \ge h_{ii}^2$ by properties 1 and 2, so $0 \le h_{ii} \le 1$. If the model has an intercept, $H\mathbf 1 = \mathbf 1$ (rows sum to 1) and $H - \frac1n\mathbf 1\mathbf 1^\top$ is again a projection, so $h_{ii} \ge 1/n$. The average of the $h_{ii}$ is $p/n$.
8. *Leave-one-out:* the prediction error of $y_i$ from the fit without observation $i$ is $y_i - \hat y_{(i)} = e_i/(1 - h_{ii})$ when $h_{ii} < 1$. This follows from the [Sherman-Morrison formula](/sherman-morrison-formula/) applied to $X^\top X - x_ix_i^\top$.

## Examples and non-examples

**Intercept only.** $X = \mathbf 1$ gives $H = \frac1n\mathbf 1\mathbf 1^\top$: every fitted value is $\bar y$, and every $h_{ii} = 1/n$.

**Simple linear regression.** For $X = (\mathbf 1, x)$, with $\bar x$ the mean and $S_{xx} = \sum (x_k - \bar x)^2$,

$$h_{ij} = \frac1n + \frac{(x_i - \bar x)(x_j - \bar x)}{S_{xx}}.$$

**A numerical case.** Take $x = (1, 2, 3, 4, 5, 10)$, so $n = 6$, $p = 2$, $\bar x = 25/6$ and $S_{xx} = 305/6$. Exact arithmetic gives the diagonal

$$h_{ii} = \tfrac{111}{305},\ \tfrac{79}{305},\ \tfrac{59}{305},\ \tfrac{51}{305},\ \tfrac{11}{61},\ \tfrac{51}{61} \approx 0.364,\ 0.259,\ 0.193,\ 0.167,\ 0.180,\ 0.836,$$

whose sum is $2 = p$. The last row is $\frac{1}{61}(-12, -5, 2, 9, 16, 51)$; it sums to 1, and the sum of its squares is $51/61 = h_{66}$, as property 7 says. So the fitted value at $x = 10$ puts weight 0.836 on its own response, and the five other points share the rest, with negative weights on the far ones. With the responses $y = (2, 3, 5, 4, 6, 4)$ the residual at $x = 10$ is $e_6 = -63/61 \approx -1.033$, but the line fitted without that point predicts 10.3 there, a prediction error of $-6.3 = e_6/(1 - h_{66})$. A small residual at a high-leverage point says little about the fit there.

**One-way layout.** For group indicator columns, $H$ is block diagonal, and each block is $\frac{1}{n_g}\mathbf 1\mathbf 1^\top$: the fitted value is the group mean, and $h_{ii} = 1/n_g$.

**Non-example: the ridge smoother.** [Ridge regression](/ridge-regression/) gives $\hat y = S_\lambda y$ with $S_\lambda = X(X^\top X + \lambda I)^{-1}X^\top$, $\lambda > 0$. It is symmetric but not idempotent: its eigenvalues are $d_j^2/(d_j^2 + \lambda) < 1$, with $d_j$ the singular values of $X$. Its trace, the effective degrees of freedom, is less than $p$. Diagnostics that use $H^2 = H$ do not carry over unchanged.

**Non-example: weighted least squares.** With weights $W$, the fitted values are $X(X^\top WX)^{-1}X^\top Wy$. This matrix is idempotent but not symmetric, an oblique projection. The symmetric version is $W^{1/2}X(X^\top WX)^{-1}X^\top W^{1/2}$, the hat matrix of the scaled problem; [weighted least squares](/weighted-least-squares/) uses that one.

**Non-example: $X$ without full column rank.** If two columns are equal, $X^\top X$ is singular and the formula fails. The projection $XX^+$ still exists and has trace equal to the rank.

## Related definitions

- **[Leverage](/leverage-statistics/)** is the diagonal entry $h_{ii}$, the self-influence of observation $i$.
- **[Studentized residuals](/studentized-residual/)** divide $e_i$ by an estimate of $\sigma\sqrt{1 - h_{ii}}$, using property 6.
- **[Cook's distance](/cooks-distance/)** measures the shift of all fitted values when observation $i$ is deleted, through $h_{ii}$ and $e_i$.
- **Smoother matrix.** For a linear smoother $\hat y = Sy$ (kernel, spline, ridge), $S$ plays the role of $H$, and $\operatorname{tr} S$ is called the effective number of parameters. The leave-one-out shortcut of property 8 holds for ridge regression and gives the closed form of leave-one-out [cross-validation](/cross-validation/).
- **Projection matrices in general.** Any symmetric idempotent matrix is the orthogonal projection onto its column space. The [least squares problem](/least-squares-problem/) page derives least squares as this projection.

## References
