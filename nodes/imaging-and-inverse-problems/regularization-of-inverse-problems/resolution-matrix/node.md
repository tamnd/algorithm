---
tag: WFYBWJ
kind: definition
slug: resolution-matrix
name: Model resolution matrix
aliases:
- resolution kernel
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: "For a linear estimate x_est = G y of y = A x + e, the matrix R = G A, so that x_est = R x_true when e = 0. Its rows show how each estimated value averages the true model."
model: real-ram
prereqs: [forward-operator, pseudoinverse, singular-value-decomposition]
see_also: [backus-gilbert-method, spectral-filter-factors, truncated-svd, tikhonov-regularization, point-spread-function, linear-gaussian-inverse-problem, generalized-cross-validation, regularization-method]
sources:
  - paper: doi:10.1111/j.1365-246X.1968.tb00216.x
    title: George Backus and Freeman Gilbert, The resolving power of gross earth data, Geophysical Journal of the Royal Astronomical Society 16(2), 1968, 169 to 205
    locator: the averaging (resolving) kernels of linear estimates, their spread, and the trade-off between resolution and error
  - book: isbn:9780128135556
    title: William Menke, Geophysical Data Analysis, Discrete Inverse Theory, fourth edition, Academic Press, 2018
    locator: the chapters Solution of the Linear Gaussian Inverse Problem, Viewpoint 2, Generalized Inverses (the model and data resolution matrices), and Nonuniqueness and Localized Averages
---

The model resolution matrix of a linear estimate $x_{\mathrm{est}} = G y$ for the [inverse problem](/inverse-problem/) $y = A x + e$ is the $n \times n$ matrix $R = G A$. For noise-free data, $x_{\mathrm{est}} = R\, x_{\mathrm{true}}$, so $R$ tells exactly how the estimate sees the truth: row $i$ shows which weighted average of the true model the $i$-th estimated value is, and column $j$ shows the estimate of a spike at position $j$. If $R = I$, every value is resolved perfectly; a regularized estimate has $R \ne I$, and the difference is its bias. The noise part of the estimate is measured separately, by $G e$ and its covariance.

## Definition

Let $A \in \mathbb{R}^{m \times n}$ be the [forward operator](/forward-operator/) and $G \in \mathbb{R}^{n \times m}$ a linear inverse, for example a [pseudoinverse](/pseudoinverse/) or a regularized inverse. With $y = A x_{\mathrm{true}} + e$,
$$x_{\mathrm{est}} = G y = R\, x_{\mathrm{true}} + G e, \qquad R = G A.$$

- **The model resolution matrix** is $R = G A$.
- **The resolution kernel** (or averaging kernel) of the estimate $x_{\mathrm{est},i}$ is row $i$ of $R$: $x_{\mathrm{est},i} = \sum_j R_{ij}\, x_{\mathrm{true},j}$ when $e = 0$. In the continuous setting, $x_{\mathrm{est}}(s) = \int R(s, t)\, x_{\mathrm{true}}(t)\, dt$, and $R(s, t)$ is a kernel.
- **The point spread function** of the estimate at position $j$ is column $j$ of $R$, the estimate of the unit spike $e_j$.
- **The data resolution matrix** is $N = A G \in \mathbb{R}^{m \times m}$, with predicted data $A x_{\mathrm{est}} = N y$. Since $\operatorname{tr}(A G) = \operatorname{tr}(G A)$, the two matrices have the same trace.

From the definition follow three facts:

- The bias of the estimate is $\mathbb{E}[x_{\mathrm{est}}] - x_{\mathrm{true}} = (R - I)\, x_{\mathrm{true}}$ for zero-mean noise.
- The noise part has covariance $G\, \Gamma_{\mathrm{n}}\, G^T$ when $e$ has covariance $\Gamma_{\mathrm{n}}$.
- $R$ annihilates the null space of $A$: if $A z = 0$, then $R z = 0$. No linear method can resolve what the data do not see.

**Measures of resolution.** One number per estimate or per method:

- The Dirichlet spread $\|R - I\|_F^2$, which is $0$ for perfect resolution.
- The Backus-Gilbert spread of row $i$, $\sum_j (i - j)^2 R_{ij}^2$ (with a weight that grows with the distance from $i$), which is small when the row is a narrow peak at $i$.
- The trace $\operatorname{tr} R$, read as the effective number of parameters that the data determine. In [generalized cross-validation](/generalized-cross-validation/), $m - \operatorname{tr} N$ is the number of degrees of freedom of the residual.

**Spectral methods.** For a filter method with [spectral filter factors](/spectral-filter-factors/) $f_i$, $G = \sum_i f_i\, v_i u_i^T/\sigma_i$ and
$$R = \sum_i f_i\, v_i v_i^T = V \operatorname{diag}(f_i)\, V^T.$$
So $R$ is symmetric, its eigenvalues are the filter factors, and $\operatorname{tr} R = \sum_i f_i$.

## Examples and non-examples

**Least squares with full column rank.** $G = (A^T A)^{-1} A^T$ gives $R = I$: perfect resolution and no bias. For an ill-conditioned $A$ this is a bad estimate, because $G e$ is huge. Resolution alone does not measure quality.

**Truncated SVD.** $R = V_k V_k^T$, the orthogonal projection onto the first $k$ right singular vectors. Its trace is $k$ and its Dirichlet spread is $n - k$. For the rectangle-rule matrix of the integration operator with $n = 24$ and $k = 6$, row 12 (at $t = 0.479$) of $R$ is
$0.031, 0.019, -0.003, -0.027, -0.043, -0.043, -0.021, 0.024, 0.086, 0.150, 0.202, \mathbf{0.226}, 0.214, 0.167, 0.098, 0.025, -0.033, -0.061, -0.056, -0.027, 0.011, 0.040, 0.047, 0.031$.
The peak is at the right place, but it is wide, and it has negative side lobes (down to $-0.061$) and a far tail. The row sums to $1.059$. These are the ringing and the loss of detail of the sharp cutoff (see [truncated SVD](/truncated-svd/)).

**Tikhonov regularization.** $R = (A^T A + \alpha I)^{-1} A^T A$, with $f_i = \sigma_i^2/(\sigma_i^2 + \alpha)$. For the same matrix with $\alpha = 10^{-3}$, row 12 is $0.001, 0.004, 0.013, 0.046, 0.160, \mathbf{0.550}, 0.160, 0.046, 0.013, 0.004, 0.001$ at positions 7 to 17, and zero to three decimals elsewhere. It is a narrow positive peak, with $\operatorname{tr} R = 13.33$ and Dirichlet spread $6.08$. This value of $\alpha$ keeps more components than TSVD with $k = 6$, so it resolves more and amplifies more noise.

**A diagonal check.** For $A = \operatorname{diag}(1, 0.1, 0.01)$ and Tikhonov with $\alpha = 0.01$, $R = \operatorname{diag}(0.990, 0.5, 0.0099)$. The first value is resolved, the second is halved, and the third is almost lost. The trace is exactly $1.5$, since $1/1.01 + 0.01/1.01 = 1$.

**The linear Gaussian model.** For the [linear Gaussian inverse problem](/linear-gaussian-inverse-problem/) with prior covariance $\Gamma_{\mathrm{pr}}$, the posterior mean has $R = I - \Gamma_{\mathrm{post}}\Gamma_{\mathrm{pr}}^{-1}$. The resolution and the posterior covariance are two views of the same matrix.

**Backus-Gilbert.** The [Backus-Gilbert method](/backus-gilbert-method/) picks each row of $G$ to make the resolution kernel of that estimate as narrow as possible under a bound on its variance. There the resolution matrix is the design goal, not a diagnostic.

**Non-example: a nonlinear estimate.** If the estimate is not a fixed linear map of $y$, as for TSVD or Tikhonov with a parameter chosen from the data, for [CGLS](/cgls/) stopped by a rule, or for total variation, there is no single $R$. A local resolution matrix can be defined from the derivative of the estimate with respect to the data, but it changes with $y$.

**Non-example: the data resolution matrix.** $N = A G$ acts on the data, not on the model. $N = I$ means the estimate fits the data exactly, which for noisy data is a sign of overfitting, not of good resolution.

## Related definitions

- [Spectral filter factors](/spectral-filter-factors/): the eigenvalues of $R$ for a filter method.
- [Point spread function](/point-spread-function/): the response of an imaging system to a point; the columns of $R$ are the point spread functions of the whole chain, measurement plus reconstruction.
- [Regularization method](/regularization-method/): $R \to I$ on the range of $A^T$ as the parameter goes to zero, which is the pointwise convergence $R_\alpha y \to A^\dagger y$ for noise-free data.
- [Linear Gaussian inverse problem](/linear-gaussian-inverse-problem/): the posterior covariance, which measures the error that the resolution matrix leaves out.

## References
