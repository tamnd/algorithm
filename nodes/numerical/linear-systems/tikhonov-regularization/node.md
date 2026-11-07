---
tag: TH9SCR
kind: technique
slug: tikhonov-regularization
name: Tikhonov regularization
aliases:
- ridge regression
- ridge regularization
- damped least squares
- Tikhonov-Phillips regularization
area: numerical/linear-systems
level: advanced
summary: Solve min ||Ax - b||^2 + lambda ||x||^2 to stabilize ill-posed problems.
prereqs: [least-squares-problem, singular-value-decomposition, condition-number]
see_also: [pseudoinverse, normal-equations, qr-decomposition, rank-revealing-factorization, hilbert-matrix, woodbury-identity, regularization, richardson-iteration]
sources:
  - paper: doi:10.1145/321105.321114
    title: David L. Phillips, A technique for the numerical solution of certain integral equations of the first kind, Journal of the ACM 9(1), 1962
    locator: the smoothing constraint added to a discretized first-kind integral equation
  - paper: doi:10.1080/00401706.1970.10488634
    title: Arthur E. Hoerl and Robert W. Kennard, Ridge regression, biased estimation for nonorthogonal problems, Technometrics 12(1), 1970
    locator: the ridge estimator (X^T X + k I)^-1 X^T y and its mean squared error compared with least squares
  - paper: doi:10.1080/00401706.1979.10489751
    title: Gene H. Golub, Michael Heath and Grace Wahba, Generalized cross-validation as a method for choosing a good ridge parameter, Technometrics 21(2), 1979
    locator: the generalized cross-validation function and its minimizer as the choice of the parameter
  - paper: doi:10.1137/1034115
    title: Per Christian Hansen, Analysis of discrete ill-posed problems by means of the L-curve, SIAM Review 34(4), 1992
    locator: the L-curve of residual norm against solution norm and the choice of the parameter at its corner
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 6.1, Constrained Least Squares (least squares with a quadratic constraint and its relation to ridge regression)
---

Tikhonov regularization replaces an ill-conditioned least squares problem by
$$\min_x \; \|A x - b\|_2^2 + \lambda \|L x\|_2^2, \qquad \lambda > 0,$$
whose solution $x_\lambda = (A^T A + \lambda L^T L)^{-1} A^T b$ exists, is unique when $\mathrm{null}(A) \cap \mathrm{null}(L) = \{0\}$, and depends continuously on $b$. With $L = I$ it damps each singular component of the solution by the filter factor $\sigma_i^2/(\sigma_i^2 + \lambda)$, so noise in $b$ is amplified by at most $1/(2\sqrt\lambda)$ instead of $1/\sigma_{\min}$. The price is a bias, and the whole technique turns on choosing $\lambda$ to balance the two.

## In plain words

Some problems are so sensitive that tiny errors in the data produce wild answers: the exact solution of the noisy problem is mostly amplified noise. Tikhonov's remedy is to ask for a compromise. Instead of fitting the data perfectly, find an answer that fits the data well and is also small, or smooth. A weight decides how much to care about each goal. With too little weight the noise comes back, with too much the answer ignores the data. Good rules choose the weight so that the remaining misfit is about the size of the noise.

## When it applies

**Notation.** $A \in \mathbb{R}^{m \times n}$ with singular value decomposition $A = \sum_i \sigma_i u_i v_i^T$, $\sigma_1 \ge \sigma_2 \ge \cdots \ge 0$; the data are $b = b_{\mathrm{exact}} + e$ with noise $e$; $x^+ = A^+ b$ is the minimum-norm least squares solution ([pseudoinverse](/pseudoinverse/)); $L \in \mathbb{R}^{p \times n}$ is the regularization operator (often $I$ or a difference matrix); $u = 2^{-53}$.

Use it when the problem is a *discrete ill-posed problem*: the singular values decay gradually to near zero without a clear gap, so no numerical rank is evident, and the data are noisy. Typical sources are discretized integral equations of the first kind (deblurring, inverse heat conduction, tomography), ill-conditioned regression (ridge regression), and Levenberg-Marquardt steps in nonlinear least squares.

The basic facts, all proved by inserting the SVD (case $L = I$):

- **Filter factors.** $x_\lambda = \sum_i \frac{\sigma_i^2}{\sigma_i^2 + \lambda}\,\frac{u_i^T b}{\sigma_i}\, v_i$. Components with $\sigma_i \gg \sqrt\lambda$ pass, those with $\sigma_i \ll \sqrt\lambda$ are suppressed.
- **Noise amplification.** $\|(A^T A + \lambda I)^{-1} A^T\|_2 = \max_i \frac{\sigma_i}{\sigma_i^2 + \lambda} \le \frac{1}{2\sqrt\lambda}$, since $\sigma^2 + \lambda \ge 2\sigma\sqrt\lambda$. So the error caused by $e$ is at most $\|e\|_2/(2\sqrt\lambda)$.
- **Bias.** For exact data, $x^+_{\mathrm{exact}} - x_\lambda = \sum_i \frac{\lambda}{\sigma_i^2 + \lambda}\,\frac{u_i^T b_{\mathrm{exact}}}{\sigma_i}\, v_i$, which tends to $0$ as $\lambda \to 0$; $\|x_\lambda\|_2$ decreases and $\|A x_\lambda - b\|_2$ increases with $\lambda$.
- **Conditioning.** $\kappa_2(A^T A + \lambda I) = (\sigma_1^2 + \lambda)/(\sigma_n^2 + \lambda) \le (\sigma_1^2 + \lambda)/\lambda$, and the stacked matrix $\begin{pmatrix} A \\ \sqrt\lambda I \end{pmatrix}$ has condition number at most $\sqrt{(\sigma_1^2 + \lambda)/\lambda}$.

## The template

```pseudo id=main
TIKHONOV(A, b, data about the noise)
L1  choose the operator L                                   ▷ hole: the regularization operator (I, a difference matrix, a weight)
L2  choose a first λ                                        ▷ hole: the starting parameter
L3  repeat
L4      solve min ‖[A; √λ L] x − [b; 0]‖_2 for x_λ          ▷ hole: the solver (QR of the stacked matrix, bidiagonalization, LSQR)
L5      evaluate the parameter rule at λ                    ▷ hole: discrepancy, GCV, L-curve corner
L6      if the rule is satisfied then return x_λ
L7      update λ                                            ▷ hole: the search (bisection, Newton, a grid)
```

The holes are the operator $L$ (L1), the solver (L4), and the parameter choice rule with its search (L2, L5, L7). With an SVD or a bidiagonalization of $A$ computed once, every new $\lambda$ costs only $O(n)$ or $O(n^2)$ flops; with a stacked QR, each $\lambda$ costs a new factorization, $2 n^2 (m + n) - \tfrac23 n^3$ flops for $L = I$ in the stacked $(m + n) \times n$ form, though Eldén's bidiagonal trick reduces this to $O(n)$ per $\lambda$ after one bidiagonalization.

## Classic examples

**The Hilbert matrix with noise.** Let $A$ be the [Hilbert matrix](/hilbert-matrix/) of order $12$ ($\kappa_2 \approx 1.7 \times 10^{16}$), $x_{\mathrm{true}} = (1, \ldots, 1)^T$ with $\|x_{\mathrm{true}}\|_2 = 3.464$, $b = A x_{\mathrm{true}} + e$ with $e$ uniform in $[-10^{-6}, 10^{-6}]$ (seed 7, $\|e\|_2 = 2.14 \times 10^{-6}$). Solving $A x = b$ exactly gives an error of $8.4 \times 10^{9}$. The Tikhonov solutions, computed exactly in rational arithmetic, give:

| $\lambda$ | $\|x_\lambda - x_{\mathrm{true}}\|_2$ | $\|A x_\lambda - b\|_2$ |
|---|---|---|
| $10^{-14}$ | 1.05 | $1.18 \times 10^{-6}$ |
| $10^{-12}$ | 0.123 | $1.22 \times 10^{-6}$ |
| $10^{-10}$ | 0.029 | $1.24 \times 10^{-6}$ |
| $10^{-8}$ | 0.014 | $2.32 \times 10^{-6}$ |
| $10^{-6}$ | 0.051 | $5.25 \times 10^{-5}$ |
| $10^{-4}$ | 0.182 | $1.60 \times 10^{-3}$ |
| $10^{-2}$ | 0.590 | $5.30 \times 10^{-2}$ |

The error first falls (less noise) and then rises (more bias). The discrepancy principle picks the $\lambda$ where the residual reaches $\|e\|_2 = 2.14 \times 10^{-6}$, just below $10^{-8}$, which is close to the best value in the table.

**Ridge regression.** For a design matrix $X$ with nearly collinear columns, $\hat\beta_\lambda = (X^T X + \lambda I)^{-1} X^T y$ has a smaller mean squared error than least squares for some $\lambda > 0$ (Hoerl and Kennard, 1970). When $X$ has far fewer rows $m$ than columns $p$, the [Woodbury identity](/woodbury-identity/) gives $\hat\beta_\lambda = X^T (X X^T + \lambda I_m)^{-1} y$, an $m \times m$ solve.

**Levenberg-Marquardt.** A Gauss-Newton step damped by $\lambda$ is a Tikhonov problem with $A$ the Jacobian and $b$ the residual, and $\lambda$ acts as a trust region radius.

**Smoothing with a derivative.** $L$ the first or second difference matrix penalizes roughness instead of size; this is Phillips' 1962 method for first-kind integral equations and the basis of smoothing splines.

## Variations

- **Parameter choice.** The discrepancy principle (Morozov) needs $\|e\|$; generalized cross-validation minimizes $\|A x_\lambda - b\|^2/\big(\mathrm{trace}(I - H_\lambda)\big)^2$, with $H_\lambda = A(A^T A + \lambda I)^{-1}A^T$ the influence matrix, without it (Golub, Heath and Wahba, 1979); the L-curve picks the corner of $\log\|x_\lambda\|$ against $\log\|A x_\lambda - b\|$ (Hansen, 1992).
- **Truncated SVD.** Keep the terms with $\sigma_i > \tau$ and drop the rest: filter factors $0$ or $1$ instead of $\sigma_i^2/(\sigma_i^2 + \lambda)$. A [rank-revealing factorization](/rank-revealing-factorization/) gives a cheaper version.
- **Iterative regularization.** Landweber iteration (Richardson on the normal equations, see [Richardson iteration](/richardson-iteration/)), CGLS and LSQR regularize by stopping early; the number of steps plays the role of $1/\lambda$.
- **General form and standard form.** With $L \ne I$, a transformation through the $A$-weighted pseudoinverse of $L$ (Eldén) or the generalized SVD of $(A, L)$ reduces the problem to $L = I$.
- **Other penalties.** $\|x\|_1$ (lasso, sparsity) or total variation $\|D x\|_1$ (edges in images) replace the quadratic term; they no longer give a linear solution formula.

## Pitfalls

- **Solving through the normal equations.** Forming $A^T A + \lambda I$ is cheap and its condition is bounded by $(\sigma_1^2 + \lambda)/\lambda$, but for small $\lambda$ this is still the square of the stacked problem's condition; QR of $\begin{pmatrix} A \\ \sqrt\lambda L \end{pmatrix}$ or a bidiagonalization is the stable choice ([normal equations](/normal-equations/)).
- **Choosing $\lambda$ by eye.** Error curves like the table above are not available in practice, since $x_{\mathrm{true}}$ is unknown; a rule (discrepancy, GCV, L-curve) is needed, and each can fail on some problems (GCV for correlated noise, the L-curve for very smooth solutions).
- **Scaling.** $\lambda$ has the units of $\sigma^2$; columns of $A$ in different units must be scaled first, or the penalty treats them unequally.
- **Regularizing a well-posed problem.** If the noise is far below $\sigma_{\min}\|x\|$, regularization only adds bias.
- **Expecting exact recovery.** No choice of $\lambda$ recovers components along singular vectors with $\sigma_i\,|v_i^T x_{\mathrm{true}}|$ below the noise level; the information is lost.

## Exercises

1. Derive the filter factor formula for $x_\lambda$ from the SVD, and prove $\max_\sigma \sigma/(\sigma^2 + \lambda) = 1/(2\sqrt\lambda)$.
2. Show that $x_\lambda$ solves the stacked least squares problem with $\begin{pmatrix} A \\ \sqrt\lambda I \end{pmatrix}$ and compute that matrix's condition number.
3. Prove that $\|x_\lambda\|_2$ is decreasing and $\|A x_\lambda - b\|_2$ increasing in $\lambda$, and that the discrepancy equation has a unique root when $\|e\| < \|b\|$ and $b$ has no component outside $\mathrm{range}(A)$.
4. Show that $x_\lambda \to A^+ b$ as $\lambda \to 0$, and that Tikhonov regularization with parameter $\lambda$ is the same as minimizing $\|A x - b\|_2$ subject to $\|x\|_2 \le \delta$ for a suitable $\delta$.
5. Reproduce the Hilbert matrix table, then add the truncated SVD solutions for each cut-off and compare the best errors.
6. Prove the Woodbury form $X^T (X X^T + \lambda I)^{-1} y$ of the ridge estimator.

## References
