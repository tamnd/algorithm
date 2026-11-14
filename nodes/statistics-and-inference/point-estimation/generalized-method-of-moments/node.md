---
tag: A39F7K
kind: technique
slug: generalized-method-of-moments
name: Generalized method of moments
aliases:
- Hansen's generalized method of moments
area: statistics-and-inference/point-estimation
level: advanced
summary: Hansen's estimator that minimizes a weighted quadratic form in sample moment conditions. With the optimal weight matrix it is efficient among such estimators.
prereqs: [method-of-moments, delta-method, m-estimator]
see_also: [instrumental-variables-estimation, two-stage-least-squares, generalized-estimating-equations, empirical-likelihood, heteroscedasticity-consistent-standard-errors, ordinary-least-squares, maximum-likelihood-estimation, double-machine-learning]
sources:
  - paper: doi:10.2307/1912775
    title: Lars Peter Hansen, Large sample properties of generalized method of moments estimators, Econometrica 50(4), 1982
    locator: pp. 1029 to 1054 (consistency, asymptotic normality, the optimal weight matrix and the test of overidentifying restrictions, for stationary ergodic data)
  - paper: doi:10.2307/1911873
    title: Lars Peter Hansen and Kenneth J. Singleton, Generalized instrumental variables estimation of nonlinear rational expectations models, Econometrica 50(5), 1982
    locator: pp. 1269 to 1286 (the consumption Euler equation estimated from its conditional moment restrictions)
  - book: isbn:9780691010182
    title: Fumio Hayashi, Econometrics, Princeton University Press, 2000
    locator: Chapter 3 (single-equation GMM, efficient weighting, the J statistic) and Chapter 7 (extremum estimators, nonlinear GMM)
  - paper: doi:10.1080/07350015.1996.10524661
    title: Joseph G. Altonji and Lewis M. Segal, Small-sample bias in GMM estimation of covariance structures, Journal of Business and Economic Statistics 14(3), 1996
    locator: pp. 353 to 366 (the estimated optimal weight is correlated with the sample moments, which biases two-step estimates)
---

The generalized method of moments (GMM) estimates a parameter $\theta \in \mathbb{R}^k$ from $q \ge k$ moment conditions $\mathbb{E}[g(X, \theta_0)] = 0$. It chooses the $\theta$ that makes the sample average $\bar g(\theta)$ as close to zero as possible in the quadratic form $\bar g(\theta)^{\mathsf T} W \bar g(\theta)$. With $q = k$ it is the [method of moments](/method-of-moments/); with more conditions than parameters it combines them, and the weight $W = S^{-1}$, the inverse covariance of the moments, gives the smallest asymptotic variance. The surplus conditions also give a test of the model, Hansen's $J$ test. Linear [instrumental variables](/instrumental-variables-estimation/), [two-stage least squares](/two-stage-least-squares/), [ordinary least squares](/ordinary-least-squares/) and [maximum likelihood](/maximum-likelihood-estimation/) are special cases.

## In plain words

A model often tells you several averages that should be zero at the true parameter, more averages than there are unknowns. With real data you cannot make all of them zero at once. So you choose the parameter that makes them as small as possible together.

How much each average counts is a choice. A good rule gives less weight to averages that are noisy and accounts for averages that move together. With that rule the answer is as precise as these averages permit.

The leftover misfit is useful too. If the model is right, the averages should be close to zero at the best parameter, and the size of the misfit has a known reference law. A misfit that is too large says that some of the conditions are false.

## When it applies

- The data $X_1, \ldots, X_n$ are iid, or stationary and ergodic (Hansen's setting), and $g(x, \theta) \in \mathbb{R}^q$ is known, with $\mathbb{E}[g(X, \theta_0)] = 0$ at the true $\theta_0$.
- Identification: $\mathbb{E}[g(X, \theta)] = 0$ holds only at $\theta = \theta_0$, and the $q \times k$ Jacobian $G = \mathbb{E}[\partial g(X, \theta_0)/\partial\theta]$ has rank $k$. Then $q \ge k$ is necessary.
- The moment covariance $S = \operatorname{Var}[g(X, \theta_0)]$ is finite and nonsingular. For dependent data, $S$ is the long-run covariance $\sum_{h} \operatorname{Cov}(g_t, g_{t+h})$.
- The model need not give a full likelihood. Only the conditions are assumed, which is why the method is common in economics.

## The template

```pseudo id=main
GMM(x_1, ..., x_n, θ_0)
L1  choose MOMENT-FUNCTION g(x, θ) ∈ R^q, q ≥ k           ▷ hole: E g(X, θ_0) = 0 at the truth
L2  ḡ(θ) ← (1/n) Σ_i g(x_i, θ)
L3  W ← FIRST-WEIGHT                                      ▷ hole: identity, or (Z'Z/n)^-1 for IV
L4  θ_1 ← MINIMIZE ḡ(θ)' W ḡ(θ) from θ_0                  ▷ hole: closed form or Gauss-Newton
L5  S ← (1/n) Σ_i (g(x_i, θ_1) - ḡ(θ_1)) (g(x_i, θ_1) - ḡ(θ_1))'   ▷ hole: long-run S for time series
L6  θ̂ ← MINIMIZE ḡ(θ)' S^-1 ḡ(θ) from θ_1
L7  G ← ∂ḡ/∂θ at θ̂
L8  V ← (G' S^-1 G)^-1 / n                               ▷ estimated covariance of θ̂
L9  J ← n ḡ(θ̂)' S^-1 ḡ(θ̂)                               ▷ compare with chi-squared, q - k df
L10 return θ̂, V, J
```

The holes are the moment conditions (line L1), the first weight (line L3), the minimizer (lines L4 and L6) and the estimate of $S$ (line L5). The estimate in line L5 is centered and has divisor $n$; the uncentered version $\frac1n\sum_i g_i g_i^{\mathsf T}$ has the same limit when the conditions hold. For moments that are linear in $\theta$, each minimization has a closed form. Otherwise Gauss-Newton steps $\delta = -(G^{\mathsf T} W G)^{-1} G^{\mathsf T} W \bar g$ with step halving work well, and for linear moments they reach the minimum in one step.

**Why it is consistent.** By a uniform law of large numbers, $\bar g(\theta) \to \mathbb{E}[g(X, \theta)]$ in probability, uniformly on a compact $\Theta$, under a dominance condition. So the objective converges to $\mathbb{E}[g]^{\mathsf T} W \,\mathbb{E}[g]$, which is zero only at $\theta_0$ by identification. The minimizer of a uniformly convergent objective converges to the unique minimizer of the limit, so $\hat\theta \to \theta_0$ in probability. This is proved (Hansen 1982; Hayashi, Chapter 7) for any fixed positive definite $W$ and for an estimated $W$ that converges to one.

**The asymptotic law.** The first-order condition is $G_n(\hat\theta)^{\mathsf T} W \bar g(\hat\theta) = 0$ with $G_n = \partial\bar g/\partial\theta$. Expand $\bar g(\hat\theta) = \bar g(\theta_0) + G_n(\tilde\theta)(\hat\theta - \theta_0)$ and solve:

$$\sqrt n(\hat\theta - \theta_0) = -(G_n^{\mathsf T} W G_n)^{-1} G_n^{\mathsf T} W \sqrt n\, \bar g(\theta_0) + o_p(1).$$

The central limit theorem gives $\sqrt n\,\bar g(\theta_0) \to N(0, S)$ in distribution, and [Slutsky's theorem](/slutsky-theorem/) gives

$$\sqrt n(\hat\theta - \theta_0) \to N\big(0,\; (G^{\mathsf T}WG)^{-1} G^{\mathsf T} W S W G (G^{\mathsf T}WG)^{-1}\big) \quad \text{in distribution}.$$

This sandwich has the same form as for an [M-estimator](/m-estimator/).

**Why $W = S^{-1}$ is optimal.** Write $A = (G^{\mathsf T}WG)^{-1}G^{\mathsf T}W$ and $B = (G^{\mathsf T}S^{-1}G)^{-1}G^{\mathsf T}S^{-1}$. Both satisfy $AG = BG = I_k$, so $ASB^{\mathsf T} = AG(G^{\mathsf T}S^{-1}G)^{-1} = (G^{\mathsf T}S^{-1}G)^{-1} = BSB^{\mathsf T}$. Hence

$$ASA^{\mathsf T} - BSB^{\mathsf T} = (A - B)\,S\,(A - B)^{\mathsf T},$$

which is positive semidefinite. The left side is the sandwich minus $(G^{\mathsf T}S^{-1}G)^{-1}$, so no weight does better than $S^{-1}$, which gives the variance $(G^{\mathsf T}S^{-1}G)^{-1}$ of line L8. This is proved. Line L5 needs a first, consistent estimate because $S$ depends on $\theta_0$; replacing $S$ by a consistent estimate does not change the limit.

**The $J$ test.** If all $q$ conditions hold and $q > k$, then $J = n\,\bar g(\hat\theta)^{\mathsf T} \hat S^{-1} \bar g(\hat\theta) \to \chi^2_{q-k}$ in distribution (Hansen 1982). The $k$ degrees of freedom are used to fit $\theta$. A large $J$ says that some condition is false, but not which one. With $q = k$, $J = 0$ always and there is nothing to test.

## Classic examples

**The method of moments.** With $q = k$ and a solution of $\bar g(\theta) = 0$, the objective is zero there for every $W$, so GMM is the [method of moments](/method-of-moments/) and the weight does not matter. For $g(x, \theta) = (x - \mu,\; x^2 - \sigma^2 - \mu^2)$ it gives $\bar x$ and the variance with divisor $n$. The covariance $(G^{\mathsf T}S^{-1}G)^{-1} = G^{-1}SG^{-\mathsf T}$ is the [delta method](/delta-method/) result.

**Linear instrumental variables.** For $y = x^{\mathsf T}\beta + u$ with instruments $z \in \mathbb{R}^q$ and $\mathbb{E}[z u] = 0$, take $g = z(y - x^{\mathsf T}\beta)$. The conditions are linear in $\beta$, and

$$\hat\beta(W) = (X^{\mathsf T}Z W Z^{\mathsf T}X)^{-1} X^{\mathsf T}Z W Z^{\mathsf T}y.$$

With $W = (Z^{\mathsf T}Z/n)^{-1}$ this is [two-stage least squares](/two-stage-least-squares/); with $z = x$ it is [ordinary least squares](/ordinary-least-squares/). Under heteroscedastic errors, the second step with $\hat S = \frac1n\sum_i \hat u_i^2 z_i z_i^{\mathsf T}$ (centered as in line L5) is more efficient than 2SLS, and the estimate $V$ of line L8 is robust in the same way as [heteroscedasticity-consistent standard errors](/heteroscedasticity-consistent-standard-errors/). A small exact case, with $x = (1, x_1)$ and $z = (1, z_1, z_2)$:

| $y$ | 3 | 6 | 4 | 9 | 2 | 8 | 5 | 11 | 7 |
|---|---|---|---|---|---|---|---|---|---|
| $x_1$ | 1 | 2 | 1 | 4 | 0 | 3 | 2 | 5 | 3 |
| $z_1$ | 0 | 1 | 1 | 2 | 0 | 2 | 0 | 3 | 1 |
| $z_2$ | 1 | 1 | 0 | 1 | 0 | 0 | 2 | 2 | 1 |

OLS gives $(1.8333, 1.8333)$. The first step with $W = (Z^{\mathsf T}Z/n)^{-1}$ gives $(863/486, 301/162) \approx (1.7757, 1.8580)$, the same as the two literal stages of 2SLS, in exact arithmetic. The second step gives $(1.9434, 1.7874)$ with standard errors $0.228$ and $0.050$, and $J = 5.546$ on 1 degree of freedom, $p = 0.019$. With $n = 9$ the chi-squared reference is a rough guide only.

**Poisson with two conditions.** For Poisson$(\lambda)$ counts, $\mathbb{E}X = \lambda$ and $\mathbb{E}X^2 = \lambda + \lambda^2$, so $g = (x - \lambda,\; x^2 - \lambda - \lambda^2)$ with $q = 2$, $k = 1$. The population quantities are $G = -(1, 1 + 2\lambda)^{\mathsf T}$ and $S$ with entries $\lambda$, $2\lambda^2 + \lambda$ and $4\lambda^3 + 6\lambda^2 + \lambda$. The first column of $S$ is $S e_1 = \lambda(1, 1 + 2\lambda)^{\mathsf T} = -\lambda G$, so $S^{-1}G = -e_1/\lambda$ and $(G^{\mathsf T}S^{-1}G)^{-1} = \lambda$. Efficient GMM reaches the Cramér-Rao bound $\lambda/n$ of $\bar X$, and the second condition adds no precision but makes the $J$ test a test of equidispersion. For negative binomial counts with mean 3 and variance 6 (a Poisson law with a Gamma(3, 1) mean), the measured rejection rate of $J$ at level 0.05 was 0.594 for $n = 50$ (500 data sets) and 1.0 for $n = 200$ (500 data sets).

**Euler equations.** Hansen and Singleton (1982) estimated the discount factor $\beta$ and risk aversion $\gamma$ of a consumer from $\mathbb{E}[\beta (c_{t+1}/c_t)^{-\gamma} r_{t+1} - 1 \mid \mathcal I_t] = 0$. Any variable $z_t$ known at time $t$ gives an unconditional condition $\mathbb{E}[(\beta (c_{t+1}/c_t)^{-\gamma} r_{t+1} - 1) z_t] = 0$, so lagged variables serve as instruments and there is no need to model the law of consumption.

**Estimating equations.** With $q = k$, the conditions $\frac1n\sum_i \psi(x_i, \theta) = 0$ of an [M-estimator](/m-estimator/), of [generalized estimating equations](/generalized-estimating-equations/) and the score equations of [maximum likelihood](/maximum-likelihood-estimation/) are exactly identified GMM, and the GMM sandwich is their robust covariance.

## Variations

- **Iterated GMM.** Repeat lines L5 and L6 until $\hat\theta$ stops changing. The limit law is the same as for two steps.
- **Continuously updated GMM.** Minimize $\bar g(\theta)^{\mathsf T} \hat S(\theta)^{-1} \bar g(\theta)$ with $S$ recomputed at each $\theta$ (Hansen, Heaton and Yaron, 1996). It does not depend on a first step and is invariant to nonsingular linear transformations of $g$.
- **Long-run covariance.** For time series, $S$ in line L5 is a kernel estimate of the long-run covariance, such as the Newey-West estimate, which is positive semidefinite by construction.
- **Generalized empirical likelihood.** [Empirical likelihood](/empirical-likelihood/) and its relatives reweight the data so that the conditions hold exactly. They have the same first-order limit as efficient GMM and a smaller higher-order bias.
- **Simulated moments.** When $\mathbb{E}[g(X, \theta)]$ has no formula, estimate it by simulation at each $\theta$, with the same random draws for every $\theta$.
- **Orthogonal moments.** Moment functions whose derivative with respect to a nuisance part is zero let a machine learning estimate of that part enter without first-order effect, as in [double machine learning](/double-machine-learning/).

## Pitfalls

- **Small-sample bias of the two-step estimate.** The estimated weight $\hat S^{-1}$ is correlated with $\bar g$, and this biases the second step (Altonji and Segal, 1996). In the Poisson example with the data $(0, 0, 1, 1, 2, 3, 3, 5, 7, 8)$, where $\bar x = 3$ and the variance with divisor $n$ is $7.2$, the first step with $W = I$ gave $3.548$ and the second step gave $1.802$, with $J = 2.98$. The sample mean, which is the efficient estimate under the model, is 3. With few observations, report the first step too.
- **The $J$ test over-rejects at moderate $n$.** Measured for the Poisson example with true Poisson data, nominal level 0.05: for $\lambda = 3$ the rejection rate was 0.106 at $n = 50$ and 0.074 at $n = 200$ (1000 data sets each), and 0.070 at $n = 1000$ (300 data sets). For $\lambda = 1$ the rates were 0.088, 0.074 and 0.043. The chi-squared limit is proved; its accuracy at a given $n$ is only measured.
- **Weak identification.** When $G$ is close to rank deficient, as with instruments that hardly move $x$, the normal limit is a poor guide, $\hat\theta$ is biased toward OLS and Wald intervals undercover.
- **Too many conditions.** Many weak conditions make $\hat S$ hard to estimate and increase the bias. More conditions can only help in the limit; in finite samples they can hurt.
- **Scaling with a fixed weight.** With $W = I$, the estimate changes when one condition is multiplied by a constant. The efficient objective $\bar g^{\mathsf T}\hat S^{-1}\bar g$ is invariant to $g \mapsto Ag$ for a fixed $\theta$ and nonsingular $A$, but two-step estimates still change through the first step.
- **A small $J$ does not confirm the model.** $J$ tests only the surplus conditions. If the $k$ conditions used for identification are false, $\hat\theta$ is inconsistent and $J$ can still be small.
- **Singular $\hat S$.** Redundant conditions, such as the same instrument twice, make $\hat S$ singular. Remove them before line L5.

## Exercises

1. Show that when $q = k$ and $\bar g(\theta) = 0$ has a solution, GMM gives that solution for every positive definite $W$, and that $J = 0$.
   *Answer.* The objective is a positive definite quadratic form in $\bar g$, so it is at least 0 and equals 0 exactly where $\bar g = 0$. The minimum is therefore the root, whatever $W$ is, and $J = n \cdot 0 = 0$.
2. For $g = z(y - x^{\mathsf T}\beta)$ and $W = (Z^{\mathsf T}Z)^{-1}$, show that the GMM estimate is $(X^{\mathsf T}P_ZX)^{-1}X^{\mathsf T}P_Zy$ with $P_Z = Z(Z^{\mathsf T}Z)^{-1}Z^{\mathsf T}$.
   *Answer.* $\bar g = Z^{\mathsf T}(y - X\beta)/n$. Setting the gradient of $(y - X\beta)^{\mathsf T}Z(Z^{\mathsf T}Z)^{-1}Z^{\mathsf T}(y - X\beta)$ to zero gives $X^{\mathsf T}P_Z(y - X\beta) = 0$. The scale $1/n^2$ does not change the minimizer.
3. Prove that the two-step objective $\bar g(\theta)^{\mathsf T}\hat S^{-1}\bar g(\theta)$ is unchanged when $g$ is replaced by $Ag$ with $A$ nonsingular and $\hat S$ is computed from the new moments at the same point.
   *Answer.* The new $\hat S$ is $A\hat SA^{\mathsf T}$ and the new $\bar g$ is $A\bar g$, so the form is $\bar g^{\mathsf T}A^{\mathsf T}A^{-\mathsf T}\hat S^{-1}A^{-1}A\bar g = \bar g^{\mathsf T}\hat S^{-1}\bar g$.
4. In the Poisson example with $W = I$, find the asymptotic variance of $\sqrt n(\hat\lambda - \lambda)$ and show it exceeds $\lambda$ for every $\lambda > 0$.
   *Answer.* With $c = 1 + 2\lambda$, the entries of $S$ are $\lambda$, $\lambda c$ and $\lambda c^2 + 2\lambda^2$. So $G^{\mathsf T}G = 1 + c^2$ and $G^{\mathsf T}SG = \lambda + 2\lambda c^2 + c^2(\lambda c^2 + 2\lambda^2) = \lambda(1 + c^2)^2 + 2\lambda^2c^2$. The variance is $G^{\mathsf T}SG/(G^{\mathsf T}G)^2 = \lambda + 2\lambda^2c^2/(1 + c^2)^2 > \lambda$.
5. Show that efficient GMM with the $k$ score functions $u(x, \theta)$ as conditions has the asymptotic covariance $I(\theta)^{-1}$.
   *Answer.* $q = k$, $S = \operatorname{Var}u = I(\theta)$ and $G = \mathbb{E}[\partial u/\partial\theta] = -I(\theta)$ by the information identity, so $(G^{\mathsf T}S^{-1}G)^{-1} = (I I^{-1} I)^{-1} = I(\theta)^{-1}$.

## References
