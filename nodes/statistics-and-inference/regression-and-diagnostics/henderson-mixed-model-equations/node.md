---
tag: 3AX196
kind: algorithm
slug: henderson-mixed-model-equations
name: Henderson's mixed model equations
aliases:
- best linear unbiased prediction of random effects
area: statistics-and-inference/regression-and-diagnostics
level: advanced
summary: A linear system whose solution gives at once the GLS estimates of the fixed effects and the best linear unbiased predictions of the random effects.
model: real-ram
complexity:
  vars: {n: the number of observations, p: the number of fixed-effect columns, q: the number of random effects}
  time: {worst: "Θ(n^3 + n (p + q)^2 + (p + q)^3)", best: "Θ(n (p + q)^2 + (p + q)^3)"}
  space: {extra: "Θ(n^2 + n (p + q) + (p + q)^2)"}
  flops: {worst: "n^3/3 + 2 (p + q + 1) n^2 + n (p + q)^2 + (p + q)^3/3 + q^3"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1959
  people: [Charles R. Henderson, Oscar Kempthorne, Shayle R. Searle, C. M. von Krosigk]
  note: Henderson and coauthors derived the equations by maximizing the joint density of the records and the random effects, so that sire evaluation could avoid inverting the covariance matrix of all records.
prereqs: [linear-mixed-model, generalized-least-squares, cholesky-decomposition, schur-complement, woodbury-identity]
see_also: [restricted-maximum-likelihood, ridge-regression, kriging, empirical-bayes, james-stein-estimator, gauss-markov-theorem, positive-definite-matrix, expectation-maximization]
sources:
  - paper: doi:10.2307/2529430
    title: "C. R. Henderson, Best linear unbiased estimation and prediction under a selection model, Biometrics 31(2), 1975, pp. 423 to 447"
    locator: The mixed model equations, the proof that they give the BLUE of estimable functions of b and the BLUP of u, and the inverse of the coefficient matrix as the error covariance
  - paper: doi:10.2307/2527669
    title: "C. R. Henderson, Oscar Kempthorne, S. R. Searle and C. M. von Krosigk, The estimation of environmental and genetic trends from records subject to culling, Biometrics 15(2), 1959, pp. 192 to 218"
    locator: The derivation of the equations from the joint density of y and u
  - paper: "C. R. Henderson, Estimation of genetic parameters (abstract), Annals of Mathematical Statistics 21(2), 1950, pp. 309 to 310"
    locator: The first statement of the equations
  - paper: doi:10.2307/2529339
    title: "C. R. Henderson, A simple method for computing the inverse of a numerator relationship matrix used in prediction of breeding values, Biometrics 32(1), 1976, pp. 69 to 83"
    locator: The rules that write down the inverse of the relationship matrix directly from a pedigree
  - paper: doi:10.1214/aos/1176343414
    title: "David Harville, Extension of the Gauss-Markov theorem to include the estimation of random effects, Annals of Statistics 4(2), 1976, pp. 384 to 395"
    locator: The whole paper (BLUP of linear combinations of fixed and random effects as a Gauss-Markov theorem)
  - paper: doi:10.1080/01621459.1962.10480665
    title: "Arthur S. Goldberger, Best linear unbiased prediction in the generalized linear regression model, Journal of the American Statistical Association 57(298), 1962, pp. 369 to 375"
    locator: The whole paper (the BLUP of a future observation with correlated errors)
  - paper: doi:10.1214/ss/1177011926
    title: "G. K. Robinson, That BLUP is a good thing: the estimation of random effects, Statistical Science 6(1), 1991, pp. 15 to 32"
    locator: Sections 2 to 5 (derivations of the equations and of BLUP, and the links to Bayes, kriging and credibility)
  - paper: doi:10.18637/jss.v067.i01
    title: "Douglas Bates, Martin Mächler, Ben Bolker and Steve Walker, Fitting linear mixed-effects models using lme4, Journal of Statistical Software 67(1), 2015, pp. 1 to 48"
    locator: Section 3 (the penalized least squares form of the equations solved by a sparse Cholesky factor)
  - book: isbn:9780471621621
    title: Shayle R. Searle, George Casella and Charles E. McCulloch, Variance Components, Wiley, 1992
    locator: Chapter 7 (prediction of random variables, BLUP and the mixed model equations)
---

Henderson's mixed model equations are a linear system of order $p + q$ whose solution gives, for known covariance matrices $G$ and $R$, both the generalized least squares estimate $\hat b$ of the fixed effects and the best linear unbiased predictor $\tilde u$ of the random effects in the [linear mixed model](/linear-mixed-model/) $y = Xb + Zu + e$. On this page $b$ is the vector of fixed-effect coefficients. The direct route to $\hat b$ is [generalized least squares](/generalized-least-squares/) with $V = ZGZ^\top + R$, an $n \times n$ matrix, and $\tilde u = GZ^\top V^{-1}(y - X\hat b)$. The equations avoid $V^{-1}$: they need only $R^{-1}$, which is often diagonal, and $G^{-1}$, which is often diagonal or sparse. That made national genetic evaluations of millions of animals possible, and the same system is inside every modern mixed model program. The predictions of the random effects are what the alias "best linear unbiased prediction of random effects" names.

## In plain words

Suppose you want to rank bulls by the milk yield of their daughters. Each bull has a few daughters in different herds, and herds differ. A plain average per bull is noisy for bulls with few daughters and mixes in herd effects. The equations solve for the herd effects and the bull effects together. They treat the bull effects as random draws around zero, so a bull with few daughters is pulled toward the average, and a bull with many daughters keeps most of his own average. The amount of pull comes from how much bulls truly differ compared with the noise in single records. One system of equations, about as large as the number of herds plus bulls, gives all of these answers at once.

## The problem

**Input.** $y \in \mathbb R^n$; $X$ ($n \times p$) of rank $p$; $Z$ ($n \times q$); a symmetric positive definite $G$ ($q \times q$), the covariance of $u$; a symmetric positive definite $R$ ($n \times n$), the covariance of $e$.

**Output.** $\hat b$ and $\tilde u$ that solve

$$\begin{pmatrix} X^\top R^{-1}X & X^\top R^{-1}Z \\ Z^\top R^{-1}X & Z^\top R^{-1}Z + G^{-1} \end{pmatrix}\begin{pmatrix} \hat b \\ \tilde u \end{pmatrix} = \begin{pmatrix} X^\top R^{-1}y \\ Z^\top R^{-1}y \end{pmatrix},$$

and on request the blocks of the inverse of the coefficient matrix $C$: the top left block is $\operatorname{Cov}(\hat b)$ and the bottom right block is $\operatorname{Cov}(\tilde u - u)$, the prediction error covariance (PEV).

**What the solution is.** $\hat b = (X^\top V^{-1}X)^{-1}X^\top V^{-1}y$, the GLS estimate, which is the best linear unbiased estimator of $b$ and its maximum likelihood estimate for known $G$ and $R$. For every linear combination $k^\top b + m^\top u$ with $k$ in the row space of $X$, $k^\top\hat b + m^\top\tilde u$ is the best linear unbiased predictor (BLUP): it has the smallest mean squared error among linear functions $\ell^\top y$ with $E[\ell^\top y - k^\top b - m^\top u] = 0$ for all $b$.

## The algorithm

```pseudo id=main
MIXED-MODEL-EQUATIONS(X[1..n, 1..p], Z[1..n, 1..q], G[1..q, 1..q], R[1..n, 1..n], y[1..n])
L1  W ← [X  Z]                                    ▷ n × (p + q)
L2  F ← R⁻¹W;  f ← R⁻¹y                           ▷ divide rows if R is diagonal, else LDLᵀ of R and solves
L3  C ← Wᵀ F                                       ▷ (p + q) × (p + q), symmetric
L4  C[p+1..p+q, p+1..p+q] ← C[p+1..p+q, p+1..p+q] + G⁻¹
L5  r ← Wᵀ f
L6  (L, D) ← LDLᵀ factor of C                      ▷ every pivot is positive
L7  s ← solve L D Lᵀ s = r
L8  return b̂ = s[1..p], ũ = s[p+1..p+q]
L9  on request: C⁻¹ from p + q solves; Cov(b̂) = top left p × p block, PEV = bottom right q × q block
```

Line L2 is the only step that touches $R$. With independent errors, $R = \sigma_e^2I$ or a diagonal matrix of weights, it costs $O(n(p + q))$. Line L4 needs $G^{-1}$, which is $\sigma_u^{-2}I$ for independent random effects, block diagonal for random slopes, and, for relationship matrices in animal breeding, sparse and written down from the pedigree by Henderson's (1976) rules without forming $G$. In large problems $C$ is sparse, and line L6 is a sparse Cholesky factorization with a fill-reducing order, or lines L6 and L7 are replaced by an iterative solver.

## Example

Three groups with $y = (10, 12, 14;\ 15, 17;\ 18, 20, 22, 24)$, an intercept ($p = 1$), one random effect for each group ($q = 3$), $\sigma_u^2 = 15$ and $\sigma_e^2 = 3$, so $G = 15I_3$ and $R = 3I_9$. Lines L1 to L5 give

$$C = \begin{pmatrix} 3 & 1 & 2/3 & 4/3 \\ 1 & 16/15 & 0 & 0 \\ 2/3 & 0 & 11/15 & 0 \\ 4/3 & 0 & 0 & 7/5 \end{pmatrix}, \qquad r = \begin{pmatrix} 152/3 \\ 12 \\ 32/3 \\ 28 \end{pmatrix}.$$

The first row is $X^\top R^{-1}X = 9/3$ and the group sizes divided by 3. The diagonal of the lower block is $n_i/3 + 1/15$. Solving in exact arithmetic:

| quantity | exact | decimal |
|---|---|---|
| $\hat b_0$ | $33852/2069$ | 16.3615 |
| $\tilde u_1$ | $-8460/2069$ | $-4.0889$ |
| $\tilde u_2$ | $-680/2069$ | $-0.3287$ |
| $\tilde u_3$ | $9140/2069$ | 4.4176 |
| $\operatorname{Var}(\hat b_0)$ | $11088/2069$ | 5.3591 |
| PEV of $u_1, u_2, u_3$ | $11685/2069,\ 11985/2069,\ 11535/2069$ | 5.6477, 5.7927, 5.5752 |

The group means are 12, 16 and 21, and the plain mean of the 9 values is 16.889. $\hat b_0$ is the GLS weighted mean of the group means with weights $n_i/(\sigma_e^2 + n_i\sigma_u^2)$, which are nearly equal here because $\sigma_u^2$ is large, so it is close to the unweighted mean 16.33 of the group means. Each $\tilde u_i$ is the deviation $\bar y_{i\cdot} - \hat b_0$ times the shrinkage factor $n_i\sigma_u^2/(n_i\sigma_u^2 + \sigma_e^2)$, which is $15/16$, $10/11$ and $20/21$ for the groups of sizes 3, 2 and 4: the smallest group is shrunk most and has the largest PEV. With the balanced data $y = (10, 12, 14;\ 15, 16, 17;\ 18, 20, 22)$ and the same $G$ and $R$, the solution is $\hat b_0 = 16$ and $\tilde u = (-15/4, 0, 15/4)$, the deviations $-4, 0, 4$ times $15/16$, with $\operatorname{Var}(\hat b_0) = 16/3$ and PEV $45/8$ for each group.

## Correctness

The proof in this folder shows four facts in exact arithmetic. First, $C$ is positive definite when $X$ has full column rank and $G$ and $R$ are positive definite, so every pivot of line L6 is positive and the solution is unique. Second, the push-through identity $(Z^\top R^{-1}Z + G^{-1})^{-1}Z^\top R^{-1} = GZ^\top V^{-1}$ and the matching form of $V^{-1}$ turn the second block row into $\tilde u = GZ^\top V^{-1}(y - X\hat b)$ and the first into the GLS normal equations $X^\top V^{-1}X\hat b = X^\top V^{-1}y$. Third, a direct comparison of mean squared errors shows that $k^\top\hat b + m^\top\tilde u$ is the BLUP. Fourth, the Schur complement formula gives the two diagonal blocks of $C^{-1}$ as $(X^\top V^{-1}X)^{-1}$ and $G - GZ^\top PZG$, which are $\operatorname{Cov}(\hat b)$ and the PEV.

## Complexity

For dense $R$, the $LDL^\top$ factor costs $n^3/3$ flops and the $p + q + 1$ solves $2(p + q + 1)n^2$; the product of line L3 costs about $n(p + q)^2$ and the factor of $C$ $(p + q)^3/3$. Inverting a dense $G$ adds $O(q^3)$. Extra space is $\Theta(n^2)$ for the factor of $R$, $\Theta(n(p + q))$ for $F$ and $\Theta((p + q)^2)$ for $C$. With diagonal $R$ and $G$, the time is $\Theta(n(p + q)^2 + (p + q)^3)$ and the $n \times n$ matrices are never formed; the GLS route instead costs $\Theta(n^3)$ for $V$, which is dense within each group. Line L9 adds $\Theta((p + q)^3)$.

## Properties

- **Exact.** In exact arithmetic the result equals GLS and BLUP exactly; the implementation checks this with rational numbers on random problems.
- **The ridge view.** The equations are the normal equations of the penalized least squares problem $\min_{b, u}(y - Xb - Zu)^\top R^{-1}(y - Xb - Zu) + u^\top G^{-1}u$. This is how Henderson et al. (1959) found them, as the maximum of the joint density of $y$ and $u$ over $b$ and $u$. With $G = \sigma_u^2I$ and $R = \sigma_e^2I$ it is [ridge regression](/ridge-regression/) on the $Z$ columns with penalty $\sigma_e^2/\sigma_u^2$ and no penalty on $X$.
- **Shrinkage.** $\tilde u$ is pulled toward 0 compared with a fit that treats $u$ as fixed; the pull grows with $\sigma_e^2/\sigma_u^2$ and shrinks with the amount of data on each effect. As $\sigma_u^2 \to \infty$ the equations become the normal equations of the fixed effects fit.
- **Bayes.** For known $G$ and $R$ and a flat prior on $b$, $\tilde u$ is the posterior mean of $u$ and $C^{-1}$ is the posterior covariance of $(b, u)$.
- **Boundary.** A variance component equal to 0 makes $G$ singular, and line L4 cannot form $G^{-1}$; the implementation raises an error. The limit $\sigma_u^2 \to 0$ sets $\tilde u = 0$ and $\hat b$ to the GLS fit without that effect, so the effect can be dropped. A form of the equations that multiplies the second block by $G$ instead of using $G^{-1}$ handles a singular $G$ directly.

## Variants and improvements

- **Estimated variance components (EBLUP).** In practice $G = G(\hat\theta)$ and $R = R(\hat\theta)$ with $\hat\theta$ from [restricted maximum likelihood](/restricted-maximum-likelihood/). The result is the empirical BLUP. EM and average information REML algorithms reuse $C$ and the blocks of $C^{-1}$ at every iteration.
- **Animal models.** With $G = \sigma_a^2\mathcal A$, $\mathcal A^{-1}$ has at most a few nonzeros for each animal and is written down from the pedigree (Henderson 1976), so $C$ stays sparse even with millions of animals; the system is solved by Gauss-Seidel or preconditioned conjugate gradients.
- **Penalized least squares with a Cholesky factor of the relative covariance.** lme4 (Bates et al. 2015) writes $u = \Lambda_\theta v$ with $v \sim N(0, \sigma^2I)$ and solves a sparse Cholesky system in $\Lambda_\theta^\top Z^\top Z\Lambda_\theta + I$, which stays well defined when a variance component is 0.
- **Absorption.** When $q$ is large and the lower block is diagonal, as for one random factor, eliminate $u$ first: the Schur complement $X^\top V^{-1}X$ is computed cheaply, then $\tilde u$ follows group by group.

## When to use it

Use the equations whenever $b$ and $u$ are wanted for given covariance parameters and $R^{-1}$ and $G^{-1}$ are cheap: clustered and longitudinal data with independent errors, genetic evaluation, small area estimation and penalized spline fits. If $V$ is small and dense, or $R$ is a dense matrix with no structure, GLS with $V$ directly is as fast. If only $b$ is wanted and $n$ is small, GLS is simpler.

## Pitfalls

- **Unknown covariance treated as known.** The blocks of $C^{-1}$ assume the true $G$ and $R$; with estimated values they understate the uncertainty, most with few groups.
- **Collinear $X$.** If $X$ is not of full column rank, $C$ is singular. Only estimable functions $k^\top b$ have a BLUE; drop or constrain columns first.
- **Dense $G^{-1}$.** Inverting a dense $G$ that has no structure loses the main advantage; then GLS or a factor of $V$ may be cheaper.
- **Selection.** BLUP stays unbiased under selection on $y$ only when the data used for the selection are in the model (Henderson 1975); otherwise the ranking of animals or schools is biased.
- **Rounding.** Large differences in scale between $G^{-1}$ and $Z^\top R^{-1}Z$ make $C$ badly conditioned; scale the columns or use the $\Lambda_\theta$ form.

## Implementations

## History

Henderson stated the equations in a 1950 abstract, for the evaluation of dairy sires. Henderson, Kempthorne, Searle and von Krosigk (1959) derived them by maximizing the joint density of the records and the random effects, without a proof that the result was best. Goldberger (1962) gave the best linear unbiased predictor in a regression with correlated errors. Henderson (1963, 1975) proved that the solutions are the BLUE and the BLUP, and the 1975 paper treated data subject to selection. Henderson (1976) found the direct rules for the inverse of the relationship matrix, which made evaluations with whole pedigrees possible. Harville (1976) put BLUP in the form of a Gauss-Markov theorem, and Robinson (1991) reviewed the many derivations and uses of BLUP.

## References
