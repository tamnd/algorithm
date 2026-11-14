---
tag: 2XMPJR
kind: algorithm
slug: two-stage-least-squares
name: Two-stage least squares
aliases:
- 2SLS
- TSLS
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: First regress the treatment on the instruments, then regress the outcome on the fitted treatment. It is the standard instrumental variables estimator.
model: real-ram
complexity:
  vars: {n: "the number of units", k: "the number of regressors", l: "the number of instruments, l ≥ k"}
  time: {worst: Θ(n l^2 + l^3), best: Θ(n l^2 + l^3)}
  space: {extra: Θ(n k + l^2)}
properties: {deterministic: true, exact_in_rational_arithmetic: true, equals_wald_ratio_with_one_binary_instrument: true, equals_ols_when_instruments_are_regressors: true, consistent_with_valid_strong_instruments: true}
history:
  year: 1953
  people: [Henri Theil, Robert L. Basmann, John Denis Sargan]
  note: Theil (1953) and Basmann (1957) proposed the method independently for one equation of a system of simultaneous equations. Sargan (1958) gave the general instrumental variables theory and the overidentification test.
prereqs: [instrumental-variables-estimation, generalized-method-of-moments]
see_also: [local-average-treatment-effect, ordinary-least-squares, heteroscedasticity-consistent-standard-errors, cluster-robust-standard-errors, errors-in-variables-regression, regression-f-test, instrumental-variable-identification, regression-discontinuity-design]
sources:
  - paper: "Henri Theil, Repeated least squares applied to complete equation systems, mimeographed memorandum, Central Planning Bureau, The Hague, 1953"
    title: Henri Theil, Repeated least squares applied to complete equation systems, Central Planning Bureau, 1953
    locator: the whole memorandum (the two-stage method; cited here from later accounts, not seen)
  - paper: doi:10.2307/1907743
    title: R. L. Basmann, A generalized classical method of linear estimation of coefficients in a structural equation, Econometrica 25(1), 1957
    locator: the article starting on p. 77 (the estimator for one structural equation)
  - paper: doi:10.2307/1907619
    title: J. D. Sargan, The estimation of economic relationships using instrumental variables, Econometrica 26(3), 1958
    locator: the article starting on p. 393 (the general instrumental variables estimator, its large-sample theory and the test of the extra instruments)
  - paper: doi:10.2307/2171753
    title: Douglas Staiger and James H. Stock, Instrumental variables regression with weak instruments, Econometrica 65(3), 1997
    locator: the article starting on p. 557 (weak-instrument asymptotics, bias toward OLS, the first-stage F rule)
  - paper: doi:10.1017/CBO9780511614491.006
    title: James H. Stock and Motohiro Yogo, Testing for weak instruments in linear IV regression, in Identification and Inference for Econometric Models, Cambridge University Press, 2005
    locator: pp. 80 to 108 (critical values of the first-stage F statistic for given bias or size distortion)
  - paper: doi:10.1080/01621459.1995.10476536
    title: John Bound, David A. Jaeger and Regina M. Baker, Problems with instrumental variables estimation when the correlation between the instruments and the endogenous explanatory variable is weak, Journal of the American Statistical Association 90(430), 1995
    locator: pp. 443 to 450 (bias toward OLS with weak instruments, and the quarter of birth estimates reproduced with random instruments)
  - book: isbn:9780691120355
    title: Joshua D. Angrist and Jörn-Steffen Pischke, Mostly Harmless Econometrics, Princeton University Press, 2009
    locator: Chapter 4, Instrumental Variables in Action (2SLS, the Wald estimator, standard errors and weak instruments; general locator, the section numbers were not checked)
---

Two-stage least squares (2SLS) estimates the coefficients of a linear model $y = X\beta + \varepsilon$ in which some regressors are correlated with the error, using instruments $Z$ that are correlated with the regressors but not with the error. The first stage regresses each column of $X$ on the instruments and keeps the fitted values $\hat X$; this keeps only the part of the regressors that the instruments explain, which is uncorrelated with the error. The second stage regresses $y$ on $\hat X$. In one formula, $b = (X^\top P_ZX)^{-1}X^\top P_Zy$ with $P_Z$ the projection on the instruments. It is the standard estimator for [instrumental variables](/instrumental-variables-estimation/): with one binary instrument it is the Wald ratio, with as many instruments as regressors it is the simple instrumental variables formula, and when every regressor is its own instrument it is [ordinary least squares](/ordinary-least-squares/). The residuals for the standard errors must be computed with the original $X$, not with $\hat X$.

## In plain words

We want the effect of a treatment, say years of schooling, on an outcome, say earnings, but the people who got more schooling differ in ways we cannot measure, so a plain regression mixes the effect with those differences. Suppose something else, such as the quarter of the year a person was born, pushes schooling up or down a little for reasons that have nothing to do with earnings.

The first stage asks how much of each person's schooling that push predicts. The second stage relates earnings to that predicted schooling only. Since the predicted part came from the push alone, and the push is unrelated to the hidden differences, the second stage measures the effect of schooling itself. The price is precision: the predicted part varies much less than schooling does, so the estimate is noisier than a plain regression.

## The problem

**Identification.** The structural equation is $y_i = x_i^\top\beta + \varepsilon_i$, where $x_i$ has $k$ entries: a constant, exogenous covariates $w_i$ and endogenous regressors $d_i$ (the treatments). The instrument vector $z_i$ has $l \ge k$ entries: the constant, $w_i$, and the excluded instruments. The assumptions are

- **exogeneity**: $\mathbb{E}[z_i\varepsilon_i] = 0$, which contains both the exclusion restriction (the excluded instruments do not enter the equation for $y$) and the independence of the instruments from the unobserved causes of $y$;
- **relevance**: $\mathbb{E}[z_iz_i^\top]$ is invertible and $\mathbb{E}[z_ix_i^\top]$ has rank $k$, so the instruments move every endogenous regressor.

Then $\beta$ is the unique solution of $\mathbb{E}[z_i(y_i - x_i^\top\beta)] = 0$ in the column space selected by the rank condition, and with $l > k$ the $l$ moment conditions overidentify it. Relevance is testable with the first-stage regression. Exogeneity is not testable when $l = k$; with $l > k$ only the consistency of the extra conditions with the others can be tested (Sargan's test), assuming at least $k$ of them are valid. The linear equation with a constant $\beta$ is itself an assumption: if the effect varies across units, 2SLS with one binary instrument estimates the [local average treatment effect](/local-average-treatment-effect/) of the compliers, not an average over everyone.

**Estimation.** The input is $y$ ($n$-vector), $X$ ($n \times k$) and $Z$ ($n \times l$). The output is $b$, the residuals $u = y - Xb$, the homoskedastic variance $\hat\sigma^2(\hat X^\top\hat X)^{-1}$ with $\hat\sigma^2 = u^\top u/(n - k)$, and the [heteroscedasticity-consistent](/heteroscedasticity-consistent-standard-errors/) (HC0) sandwich. 2SLS is consistent under the two assumptions and asymptotically normal under finite fourth moments. It is biased in finite samples, toward OLS, and the bias and the size distortion of its $t$ tests are large when the instruments are weak. The first-stage $F$ statistic of the excluded instruments is the usual diagnostic: Staiger and Stock (1997) suggested $F > 10$ as a rule of thumb for one endogenous regressor, and Stock and Yogo (2005) give critical values.

## The algorithm

```pseudo id=main
TSLS(y, X, Z)                                 ▷ X is n × k, Z is n × l, l ≥ k
L1  Π ← solve (ZᵀZ) Π = ZᵀX                    ▷ first stage: one regression per column of X
L2  X̂ ← Z Π                                    ▷ fitted regressors; exogenous columns are reproduced exactly
L3  b ← solve (X̂ᵀX) b = X̂ᵀy                    ▷ second stage; X̂ᵀX = X̂ᵀX̂
L4  u ← y - X b                                ▷ residuals with the ORIGINAL X
L5  σ² ← uᵀu / (n - k)
L6  V ← σ² (X̂ᵀX̂)⁻¹;  V_HC0 ← (X̂ᵀX̂)⁻¹ (Σ_i u_i² x̂_i x̂_iᵀ) (X̂ᵀX̂)⁻¹
L7  return (b, V, V_HC0)
```

The columns of $X$ that are also columns of $Z$ (the constant and the exogenous covariates) are fitted exactly in line L1, so only the endogenous columns change in $\hat X$. Line L3 can be read as the regression of $y$ on $\hat X$, which is where the name comes from; but the residual variance of that regression uses $y - \hat Xb$, which is wrong, and that is why line L4 goes back to $X$. In floating point, solve the least squares problems by QR rather than by forming $Z^\top Z$, which squares the condition number.

## Example

Eight units. The instrument $z$ is a random encouragement, $d$ is whether the unit took the treatment, and $y$ is the outcome.

| $z$ | $d$ | $y$ |
| --- | --- | --- |
| 0 | 0, 0, 0, 1 | 1, 2, 3, 6 |
| 1 | 1, 1, 1, 0 | 5, 6, 4, 2 |

**First stage.** $\bar d = 1/4$ when $z = 0$ and $3/4$ when $z = 1$, so $\hat d = 1/4 + z/2$: the encouragement raises the treatment rate by $1/2$.

**Second stage.** $\bar y = 3$ when $z = 0$ and $17/4$ when $z = 1$. The regression of $y$ on $(1, \hat d)$ gives $b = (19/8, 5/2)$. The slope is the Wald ratio $(17/4 - 3)/(3/4 - 1/4) = (5/4)/(1/2) = 5/2$, as it must be with one binary instrument. OLS of $y$ on $(1, d)$ gives slope $21/4 - 2 = 13/4$: the units that took the treatment against the encouragement differ from the rest.

**Standard errors.** The residuals $u = y - 19/8 - \frac52 d$ are $(-11, -3, 5, 9, 1, 9, -7, -3)/8$, so $u^\top u = 47/8$ and $\hat\sigma^2 = 47/48$. The centred sum of squares of $\hat d$ is $8 \cdot (1/4)^2 = 1/2$, so the variance of the slope is $\frac{47}{48} \cdot 2 = 47/24$ and its standard error is 1.40; the HC0 standard error is $\sqrt{47/32} = 1.21$. The residuals of the literal second regression, $y - 19/8 - \frac52\hat d$, are $-2, -1, 0, 3$ and $3/4, 7/4, -1/4, -9/4$, with sum of squares $91/4$; a program run on $\hat d$ would report a standard error of $\sqrt{91/12} = 2.75$, twice too large here, and in other data too small.

**Simulation.** $y = 1 + d + u$, $d = 0.5(z_1 + z_2 + z_3) + v$ with three standard normal instruments and $\operatorname{corr}(u, v) = 0.6$, so OLS tends to $1 + 0.6/1.75 = 1.343$. Over 300 samples of $n = 200$, measured:

| design | 2SLS mean | 2SLS SD | OLS mean | 95% HC0 coverage | Sargan rejects at 5% | median first-stage $F$ |
| --- | --- | --- | --- | --- | --- | --- |
| strong instruments | 1.006 | 0.085 | 1.344 | 0.94 | 0.06 | 50.4 |
| weak, $\pi = 0.05$ each | 1.388 | 0.623 | 1.604 | 0.82 | 0.03 | 1.2 |
| first instrument invalid | 1.327 | 0.091 | 1.483 | 0.05 | 1.00 | 50.2 |

With weak instruments 2SLS moves toward OLS and its intervals undercover. With one instrument that has a direct effect of 0.5 on $y$, the estimate is badly biased, and Sargan's test catches it every time, because the other two instruments are valid and disagree with it.

## Correctness

The full proofs are in [the correctness proof](proofs/correctness.md). The key facts:

- **Projection form.** $\hat X = P_ZX$, and since $P_Z$ is symmetric and idempotent, $\hat X^\top X = \hat X^\top\hat X = X^\top P_ZX$. So line L3 computes $b = (X^\top P_ZX)^{-1}X^\top P_Zy$, which is also the regression of $y$ on $\hat X$.
- **Just-identified.** With $l = k$, $b = (Z^\top X)^{-1}Z^\top y$, the simple instrumental variables formula.
- **One binary instrument.** With $X = [1, d]$ and $Z = [1, z]$, the equations $Z^\top(y - Xb) = 0$ say the residuals sum to 0 in each instrument group, so $\bar y_1 = a + b_d\bar d_1$ and $\bar y_0 = a + b_d\bar d_0$, and $b_d$ is the Wald ratio. The tests check this exactly on 200 random data sets.
- **No endogeneity.** With $Z = X$, $\hat X = X$ and 2SLS is OLS, with White's sandwich.
- **Consistency.** $b - \beta = (X^\top P_ZX)^{-1}X^\top P_Z\varepsilon$, and with $Z^\top\varepsilon/n \to 0$ and the rank condition, the law of large numbers and continuous mapping give $b \to \beta$. OLS tends to $\beta + Q_{xx}^{-1}\mathbb{E}[x_i\varepsilon_i]$ instead.

Proved: the algebra above and consistency. Cited: asymptotic normality, the validity of the variance estimates, and the $\chi^2_{l - k}$ law of Sargan's statistic (Sargan 1958). The simulation numbers are measured.

## Complexity

Forming $Z^\top Z$ costs $\Theta(nl^2)$ and $Z^\top X$ costs $\Theta(nlk)$; solving for $\Pi$ costs $\Theta(l^3 + l^2k)$; $\hat X$ costs $\Theta(nlk)$; the second stage costs $\Theta(nk^2 + k^3)$. Since $k \le l$, the total is $\Theta(nl^2 + l^3)$, the cost of one least squares fit on the instruments. The space is $\Theta(nk)$ for $\hat X$ and $\Theta(l^2)$ for the cross products; a streaming version that keeps only $Z^\top Z$, $Z^\top X$, $Z^\top y$, $X^\top X$, $X^\top y$ and $y^\top y$ needs $\Theta(l^2)$ space and one pass, and gets $u^\top u = y^\top y - 2b^\top X^\top y + b^\top X^\top Xb$ without the residuals (but not the HC0 sandwich).

## Properties

- **GMM with a fixed weight.** 2SLS minimizes $(y - Xb)^\top Z(Z^\top Z)^{-1}Z^\top(y - Xb)$, the [generalized method of moments](/generalized-method-of-moments/) criterion with weight $(Z^\top Z)^{-1}$. That weight is optimal under homoskedastic errors; with heteroskedastic errors, two-step GMM is more efficient when $l > k$.
- **Biased toward OLS.** A common approximation puts the bias of 2SLS at about the OLS bias times $1/(F + 1)$, where $F$ is the population first-stage $F$ statistic of the excluded instruments; adding weak instruments lowers $F$ and makes it worse (Bound, Jaeger and Baker 1995; Staiger and Stock 1997). In the weak design of the simulation, $F \approx 0.5$ predicts a bias of $0.604/1.5 \approx 0.40$, and the measured bias was 0.39.
- **No finite moments when just-identified.** With one instrument per endogenous regressor, the 2SLS estimate has no finite mean; its distribution has heavy tails. The median is still a useful summary.
- **Invariant to the choice of instruments within a span.** Only the column span of $Z$ matters, since $b$ depends on $Z$ only through $P_Z$.
- **Exact in rational arithmetic.** All steps are rational operations, so with fraction inputs the code gives the exact $b$, which the tests use.

## Variants and improvements

- **Limited information maximum likelihood (LIML).** Anderson and Rubin (1949) derived the maximum likelihood estimator of one equation with normal errors. It is approximately median-unbiased and behaves much better than 2SLS with many or weak instruments. Fuller's modification gives it finite moments.
- **k-class estimators.** OLS ($\kappa = 0$), 2SLS ($\kappa = 1$) and LIML ($\kappa = \hat\kappa_{\text{LIML}}$) are members of one family $b(\kappa) = (X^\top(I - \kappa M_Z)X)^{-1}X^\top(I - \kappa M_Z)y$ with $M_Z = I - P_Z$.
- **Two-step efficient GMM.** Use the 2SLS residuals to estimate $S = \frac1n\sum_i u_i^2z_iz_i^\top$, then minimize with weight $S^{-1}$. The Hansen $J$ statistic replaces Sargan's test under heteroskedasticity.
- **Cluster-robust variance.** With grouped data, replace the HC0 meat by sums over clusters, as in [cluster-robust standard errors](/cluster-robust-standard-errors/).
- **Weak-instrument-robust inference.** The Anderson-Rubin test, described on the [instrumental variables page](/instrumental-variables-estimation/), has the right size whatever the strength of the instruments.
- **Control function.** Add the first-stage residual $\hat v$ as a regressor in the outcome equation. In the linear model the coefficient on $d$ equals the 2SLS estimate, and the $t$ test on $\hat v$ is a test of endogeneity (the Durbin-Wu-Hausman test).

## When to use it

Use 2SLS when a regressor of interest is correlated with the error, through omitted variables, measurement error or simultaneity, and you have instruments that you can defend as excluded from the outcome equation and as unrelated to the hidden causes. Examples are random encouragements, lotteries, rules that set eligibility, and the physical or institutional quirks used in natural experiments. Report the first-stage $F$; if it is small, prefer LIML or the Anderson-Rubin test. If the regressors are exogenous, use OLS: 2SLS then only adds variance. For [errors in variables](/errors-in-variables-regression/) with a second independent measurement, the second measurement is a natural instrument.

## Pitfalls

- **Doing the two stages by hand.** The point estimate is right, the standard errors are not, because the residuals of the second regression use $\hat X$. Use a routine that computes $u = y - Xb$.
- **Leaving the exogenous covariates out of the first stage.** Every exogenous regressor of the outcome equation must also be in $Z$. If a covariate is in the second stage but not in the first, the first-stage fits are not orthogonal to it, and the estimate is inconsistent in general.
- **Nonlinear first stages.** Plugging fitted values from a probit or logit first stage into a linear second stage ("forbidden regression") is not 2SLS and is not consistent unless the nonlinear model is exactly right. Use the fitted probabilities as an instrument instead.
- **Weak instruments.** A first-stage $F$ of 2 can give an estimate close to OLS with a small standard error and a confident but wrong interval, as in the simulation, where the coverage was 0.82.
- **Many instruments.** Adding instruments raises the first-stage $R^2$ by chance and pulls 2SLS toward OLS. Angrist and Krueger (1991) used up to 180 interactions of quarter of birth; Bound, Jaeger and Baker (1995) showed that random instruments reproduced their estimates.
- **Reading Sargan's test as a proof of validity.** The test has power only if some instruments are valid and the invalid ones pull in a different direction. If all instruments share the same bias, it does not reject.
- **Constant effects.** With heterogeneous effects, different instruments identify different local effects, so Sargan's test can reject even if every instrument satisfies the exclusion restriction.

## Implementations

## History

Theil (1953), in a memorandum of the Netherlands Central Planning Bureau, and Basmann (1957) proposed two-stage least squares independently, as a way to estimate one equation of a system of simultaneous equations without the full maximum likelihood of the Cowles Commission. Anderson and Rubin (1949) had already given the limited information maximum likelihood estimator and the test that bears their names. Sargan (1958) set out the general instrumental variables estimator, of which 2SLS is the efficient case under homoskedasticity, and the test of overidentifying restrictions. In the 1990s the method became the main tool of the "natural experiments" of labour economics, and the problems with weak instruments found by Bound, Jaeger and Baker (1995) and Staiger and Stock (1997) led to the first-stage diagnostics and the robust tests used today.

## References
