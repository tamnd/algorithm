---
tag: HXP9D6
kind: algorithm
slug: least-squares-arx-identification
name: Least-squares identification of ARX models
aliases:
- equation error method
- linear regression identification
area: control/modeling-and-identification
level: core
summary: Estimates ARX parameters by linear least squares on the regression of each output on past outputs and inputs.
solves: [system-identification]
model: real-ram
complexity:
  vars: {N: the number of samples, d: the number of parameters}
  time: {worst: O(N d^2 + d^3)}
  space: {extra: O(d^2)}
properties: {deterministic: true, online: false, recursive: false, exact: true}
history:
  year: 1958
  people: [Rudolf E. Kalman]
  note: "Kalman's self-optimizing controller of 1958 estimated the coefficients of a difference equation model of the plant by least squares, an early use of the method on dynamic systems; the 1971 survey of Åström and Eykhoff made it the reference method of system identification."
prereqs: [arx-model, least-squares-problem, persistent-excitation]
see_also: [rls-algorithm, instrumental-variable-identification, prediction-error-method, normal-equations, qr-decomposition, linear-regression, autoregressive-model, system-identification]
sources:
  - book: isbn:9780136566953
    title: "Lennart Ljung, System Identification: Theory for the User, second edition, Prentice Hall, 1999"
    locator: "Chapter 7 (linear regressions and the least squares method), Chapter 8 (consistency) and Chapter 10 (computing the estimate, including solution by QR factorization)"
  - book: isbn:9780138812362
    title: "Torsten Söderström and Petre Stoica, System Identification, Prentice Hall, 1989"
    locator: "the chapter on linear regression and Chapter 5 (persistent excitation and the nonsingularity of the normal matrix)"
  - paper: doi:10.1016/0005-1098(71)90059-8
    title: "Karl Johan Åström and Pieter Eykhoff, System identification: a survey, Automatica 7(2), 123-162, 1971"
    locator: the least squares method for difference equation models, its bias under correlated residuals, and its history
  - paper: "Rudolf E. Kalman, Design of a self-optimizing control system, Transactions of the ASME 80, 468-478, 1958"
    locator: the estimation of the coefficients of a difference equation model of the plant
---

Least-squares identification of ARX models fits the coefficients of the difference equation $y(k) + a_1 y(k-1) + \cdots + a_{n_a} y(k-n_a) = b_1 u(k-n_k) + \cdots + b_{n_b} u(k-n_k-n_b+1) + e(k)$ to measured input and output data. The [ARX model](/arx-model/) says that each output is a linear function of a few past outputs and inputs plus a white error, so the coefficients that best predict the data one step ahead solve an ordinary [least squares problem](/least-squares-problem/). The algorithm builds the $d \times d$ normal matrix of the regressors, with $d = n_a + n_b$, in one pass over the $N$ samples, and solves one linear system: $O(N d^2 + d^3)$ operations. It returns the exact global minimizer of the sum of squared equation errors whenever the data make that minimizer unique. When the true noise is not white, the minimizer is a biased estimate of the system.

## In plain words

Guess that the next output of the system is a weighted sum of the last few outputs and the last few inputs. For every time step you can then write one equation that says "this output equals that weighted sum, plus a small error". There are many more equations than unknown weights, so they cannot all hold exactly. Least squares picks the weights that make the sum of the squared errors as small as possible. The work is to add up a small table of products of past values, once for each time step, and then to solve one small system of equations.

## The problem

**Input.** Samples $y(0), \ldots, y(N-1)$ and $u(0), \ldots, u(N-1)$, and orders $n_a \ge 0$, $n_b \ge 1$, $n_k \ge 0$.

**Regressor.** For $k \ge k_0 = \max(n_a, n_k + n_b - 1)$ every past value below is inside the data:

$$\varphi(k) = \big(-y(k-1), \ldots, -y(k-n_a),\ u(k-n_k), \ldots, u(k-n_k-n_b+1)\big)^T.$$

**Output.** The $\theta = (a_1, \ldots, a_{n_a}, b_1, \ldots, b_{n_b})$ that minimizes

$$V(\theta) = \sum_{k=k_0}^{N-1} \big(y(k) - \varphi(k)^T \theta\big)^2,$$

or a report that the minimizer is not unique.

## The algorithm

```pseudo id=main
ARX-LS(y, u, na, nb, nk)
L1  k0 ← max(na, nk + nb - 1);  d ← na + nb
L2  R ← the d × d zero matrix;  f ← the zero vector of length d
L3  for k ← k0 to N - 1 do
L4      φ ← (-y(k-1), ..., -y(k-na), u(k-nk), ..., u(k-nk-nb+1))
L5      R ← R + φ φᵀ
L6      f ← f + φ · y(k)
L7  if R is singular then fail: the data are not informative for this model
L8  θ ← the solution of R θ = f
L9  return θ
```

Line L1 skips the first samples, whose regressors would reach before the start of the record. Lines L3 to L6 add up the normal equations one sample at a time, so the data are read once and the regressors are never stored. $R$ is symmetric, so only its upper triangle needs to be formed. Line L7 is the case where the minimizer is not unique: then some nonzero direction $m$ has $\varphi(k)^T m = 0$ for every sample, and $\theta + t\, m$ fits equally well for every $t$. Line L8 solves the normal equations $R \theta = f$, the condition for a zero gradient of $V$.

## Example

Take $n_a = n_b = n_k = 1$, so the model is $y(k) + a\, y(k-1) = b\, u(k-1) + e(k)$ and $\varphi(k) = (-y(k-1), u(k-1))$. The data are

$$u = (1, 1, -1, 1, -1, -1), \qquad y = (0, 1, 1.4, -0.2, 0.9, -0.6).$$

Line L1 gives $k_0 = 1$, so there are five equations, $k = 1, \ldots, 5$.

| $k$ | $\varphi(k)$ | $y(k)$ | $\varphi(k)^T \hat\theta$ | residual |
|---|---|---|---|---|
| 1 | $(0, 1)$ | $1$ | $0.9655$ | $0.0345$ |
| 2 | $(-1, 1)$ | $1.4$ | $1.4507$ | $-0.0507$ |
| 3 | $(-1.4, -1)$ | $-0.2$ | $-0.2864$ | $0.0864$ |
| 4 | $(0.2, 1)$ | $0.9$ | $0.8685$ | $0.0315$ |
| 5 | $(-0.9, -1)$ | $-0.6$ | $-0.5289$ | $-0.0711$ |

The loop of L3 to L6 gives

$$R = \begin{pmatrix} 3.81 & 1.5 \\ 1.5 & 5 \end{pmatrix}, \qquad f = \begin{pmatrix} -0.4 \\ 4.1 \end{pmatrix}.$$

For example $R_{11} = 0 + 1 + 1.96 + 0.04 + 0.81 = 3.81$ and $f_2 = 1 + 1.4 + 0.2 + 0.9 + 0.6 = 4.1$. The determinant is $3.81 \cdot 5 - 1.5^2 = 16.8$, so L7 passes, and L8 gives

$$\hat a = \frac{5 \cdot (-0.4) - 1.5 \cdot 4.1}{16.8} = -\frac{163}{336} \approx -0.4851, \qquad \hat b = \frac{3.81 \cdot 4.1 - 1.5 \cdot (-0.4)}{16.8} = \frac{5407}{5600} \approx 0.9655.$$

The residual column of the table sums in squares to $V(\hat\theta) = 2899/168000 \approx 0.017256$, and it is orthogonal to both columns of $\varphi$, as the normal equations require.

## Correctness

**Claim.** If $R = \sum_{k \ge k_0} \varphi(k) \varphi(k)^T$ is nonsingular, ARX-LS returns the unique minimizer of $V$. If $R$ is singular, $V$ has infinitely many minimizers and ARX-LS reports this at L7.

**Key invariant.** After the pass of the loop for time $k$, $R = \sum_{j=k_0}^{k} \varphi(j) \varphi(j)^T$ and $f = \sum_{j=k_0}^{k} \varphi(j)\, y(j)$.

With the invariant at $k = N - 1$, $V(\theta) = \theta^T R \theta - 2 f^T \theta + \sum y(k)^2$. This is a convex quadratic whose gradient vanishes exactly on the solutions of $R \theta = f$, and $R$ is positive semidefinite, so it is positive definite when it is nonsingular. The full proof is below.

## Complexity

Line L4 costs $O(d)$ to gather the regressor. Line L5 costs $d^2$ multiplications, or $d(d+1)/2$ using symmetry, and line L6 costs $d$. Over the $N - k_0$ samples this is $O(N d^2)$. Line L8 solves a $d \times d$ system by Gaussian elimination in $O(d^3)$, and the same elimination detects the singular case of L7. The total is $O(N d^2 + d^3)$ in the [real RAM](/real-ram/), with $O(d^2)$ extra space for $R$ and $f$. Reading the data costs $\Omega(N)$, and for $N \gg d$ the pass over the samples dominates.

## Properties

- **Exact.** In exact arithmetic the result is the exact minimizer of $V$; with rational data it is rational.
- **Global.** $V$ is a convex quadratic, so there are no local minima to get stuck in.
- **Consistent for ARX data (theorem).** If the data come from an ARX system of the same orders with white noise, an open-loop input that is [persistently exciting](/persistent-excitation/) of order $n_a + n_b$, and coprime $A$ and $B$, then $\hat\theta \to \theta_0$ with probability 1 as $N \to \infty$ (Ljung 1999, Chapter 8).
- **Biased for colored noise (theorem and measurement).** If the equation error is not white, $\varphi(k)$ contains past outputs that are correlated with it, and the limit is not $\theta_0$. For the system $A = 1 - 1.5 q^{-1} + 0.7 q^{-2}$, $B = q^{-1} + 0.5 q^{-2}$ with ARMAX noise $C = 1 - q^{-1} + 0.2 q^{-2}$, a white $\pm 1$ input and $N = 50000$, the estimate was $(-1.2286, 0.4547, 0.9965, 0.7650)$ against the true $(-1.5, 0.7, 1, 0.5)$.
- **Asymptotic covariance (theorem).** For ARX data, $\sqrt{N}(\hat\theta - \theta_0)$ tends to a normal law with covariance $\sigma^2 \big(\mathbb{E}\, \varphi \varphi^T\big)^{-1}$, which is estimated by $\hat\sigma^2 N R^{-1}$ with $\hat\sigma^2 = V(\hat\theta)/(N - k_0 - d)$.
- **Not online.** The batch form needs all data before L8; the [RLS algorithm](/rls-algorithm/) gives the same answer after every sample.

## Variants and improvements

- **QR on the data matrix.** Stack the regressors as rows of an $(N - k_0) \times d$ matrix $\Phi$ and solve $\min \lVert Y - \Phi \theta \rVert$ by a [QR decomposition](/qr-decomposition/). This costs $O(N d^2)$ as well, but avoids squaring the condition number in L5.
- **Recursive least squares.** Update $\hat\theta$ at each sample in $O(d^2)$ by the Sherman-Morrison formula; with a forgetting factor it tracks slowly changing systems.
- **Weighted and prefiltered least squares.** Weight the equations, or filter $y$ and $u$ by the same filter $L(q)$ before L3, to shape the frequency range where the model fits best.
- **Regularized least squares.** Add $\lambda I$ or a kernel matrix to $R$ in L8, as in [kernel-based identification](/kernel-based-identification/), to fit long FIR or high-order ARX models with less variance.
- **[Instrumental variables](/instrumental-variable-identification/).** Replace one $\varphi$ in L5 and L6 by an instrument vector uncorrelated with the noise, which removes the bias under colored noise.
- **Order scan.** With the columns of the data matrix ordered as $-y(k-1), u(k-1), -y(k-2), u(k-2), \ldots$, the leading columns are the regressors of the lower orders, and one QR decomposition gives the losses of all of them.

## When to use it

Use it as the first fit on new data, as a starting value for the [prediction error method](/prediction-error-method/) or for instrumental variables, inside recursive and adaptive schemes, and whenever the signal-to-noise ratio is high. High-order ARX models fitted this way also approximate a general linear system well. Do not trust its pole estimates when the disturbance is strongly colored and the model order is low; use instrumental variables or a prediction error method with a noise model.

## Pitfalls

- **Zero padding before the record.** Starting the loop at $k = 0$ in L1 with the missing past set to 0 adds equations that the data do not support, and biases the fit when the system was not at rest. L1 must start at $k_0 = \max(n_a, n_k + n_b - 1)$.
- **The sign of the output terms.** Writing $+y(k-i)$ in L4 makes the regression estimate $-a_i$ instead of $a_i$. L4 must use $-y(k-i)$, because $A(q) = 1 + a_1 q^{-1} + \cdots$ has the coefficients on the left side.
- **Ignoring a singular $R$.** A constant input makes $u(k-1)$ and $u(k-2)$ equal, so with $n_b = 2$ the matrix of L5 is singular; a solver without the check of L7 returns an arbitrary point or overflows. Keep L7, and choose an input that is persistently exciting of order at least $n_b$.
- **Ill-conditioning of the normal equations.** In floating point, forming $R$ in L5 squares the condition number of the data. For fast sampling or high orders, replace L5 to L8 by a QR decomposition of the stacked regressors.
- **Unremoved means.** A constant offset in $u$ or $y$ that is not in the model is fitted by distorting $\theta$. Subtract the sample means before L3, or add a constant 1 to the regressor in L4.

## Implementations

## History

Least squares itself goes back to Legendre and Gauss at the start of the nineteenth century. Kalman's 1958 design of a self-optimizing controller estimated the coefficients of a difference equation model of the plant by least squares and recomputed the controller from them. Åström and Eykhoff's survey of 1971 presented least squares for difference equation models as the basic method of system identification and discussed its bias when the residuals are correlated, the problem that led to instrumental variables and to maximum likelihood fits of ARMAX models.

## References
