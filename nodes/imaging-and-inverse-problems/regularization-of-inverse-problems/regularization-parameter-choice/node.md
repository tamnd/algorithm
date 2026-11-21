---
tag: Y7Q6EW
kind: problem
slug: regularization-parameter-choice
name: Regularization parameter choice
aliases:
- parameter choice rule
- choice of the regularization parameter
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: "Choose the regularization parameter, or the stopping index, from the data and maybe the noise level so that the regularized solution is close to the true one."
model: real-ram
prereqs: [regularization-method, tikhonov-regularization, inverse-problem]
see_also: [morozov-discrepancy-principle, generalized-cross-validation, l-curve-method, unbiased-predictive-risk-estimator, quasi-optimality-criterion, lepskii-balancing-principle, bakushinskii-veto, semi-convergence]
sources:
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: chapters 3 and 4
  - book: isbn:9780898715071
    title: Curtis R. Vogel, Computational Methods for Inverse Problems, SIAM, 2002
    locator: chapter 7 (regularization parameter selection methods)
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: chapter 5 (choosing the regularization parameter)
---

Every regularization method has a parameter: the weight $\alpha$ in Tikhonov regularization, the truncation index of the truncated SVD, the number of iterations of Landweber or CGLS. Regularization parameter choice is the problem of setting it from the information at hand, so that the regularized solution is close to the true one. A small $\alpha$ fits the data well but amplifies the noise; a large $\alpha$ suppresses the noise but also the solution. The best $\alpha$ balances the two, and it depends on the unknown solution and on the noise. A parameter choice rule replaces it by something computable. Rules are classed by what they use: a priori rules use only the noise level $\delta$ and assumed smoothness, a posteriori rules use $\delta$ (or the noise variance $\sigma^2$) and the data, and heuristic rules use the data alone. The [Bakushinskii veto](/bakushinskii-veto/) shows that a heuristic rule cannot be convergent for every ill-posed problem, so this classification is also a classification of the guarantees.

## In plain words

Every method that cleans up a noisy inverse problem has a knob that says how much to smooth. Too little and the answer is full of amplified noise. Too much and real detail is wiped out. The right setting depends on the true answer, which you do not have. A parameter choice rule is a recipe for setting the knob from what you do have: the data, and maybe an estimate of how noisy they are. Rules that know the noise level come with proofs. Rules that do not know it are often good in practice, but a theorem says they can always be fooled.

## Definition

The model is $y^\delta = Ax^\dagger + e$, with $A: X \to Y$ a linear operator between Hilbert spaces or an $m \times n$ matrix, and $x^\dagger$ the minimum norm solution of $Ax = Ax^\dagger$. Two noise models are used:

- deterministic: $\lVert e\rVert \le \delta$ with a known $\delta$, and the worst case over such $e$ is studied;
- statistical: $e \sim N(0, \sigma^2I_m)$ (white noise), so $E\lVert e\rVert^2 = m\sigma^2$, and expected errors are studied.

A regularization method is a family of maps $R_\alpha$, $\alpha > 0$, with $R_\alpha y \to A^\dagger y$ as $\alpha \to 0$ for exact data; see [regularization method](/regularization-method/). For Tikhonov regularization, $R_\alpha y = (A^TA + \alpha I)^{-1}A^Ty$ (the page [Tikhonov regularization](/tikhonov-regularization/) writes $\lambda$ for $\alpha$), and in the SVD it acts by the [filter factors](/spectral-filter-factors/) $f_i = s_i^2/(s_i^2 + \alpha)$.

A parameter choice rule is a map $\alpha = \alpha(\delta, y^\delta)$. It is

- a priori if $\alpha = \alpha(\delta)$ depends on the noise level only, typically with assumed smoothness;
- a posteriori if it depends on $\delta$ (or $\sigma$) and on $y^\delta$;
- heuristic, or noise-level-free, if $\alpha = \alpha(y^\delta)$.

The pair (method, rule) is convergent if

$$\sup\{\lVert R_{\alpha(\delta, y^\delta)}y^\delta - x^\dagger\rVert : \lVert y^\delta - Ax^\dagger\rVert \le \delta\} \to 0 \quad\text{as } \delta \to 0$$

for every $x^\dagger$. It is order optimal on a smoothness class, such as the source condition $x^\dagger = (A^\ast A)^\nu w$ with $\lVert w\rVert \le \varrho$ (see [source condition](/source-condition/)), if its worst-case error is within a constant factor of the best possible error $O(\varrho^{1/(2\nu + 1)}\delta^{2\nu/(2\nu + 1)})$ over all methods. In the statistical model, the goal is usually a small expected error or predictive risk $\frac1mE\lVert A(x_\alpha - x^\dagger)\rVert^2$.

## Variants

- **Continuous or discrete parameter.** Tikhonov has a continuous $\alpha$; truncated SVD and iterations have an index $k$. For iterations, a rule is a stopping rule, and [semi-convergence](/semi-convergence/) makes stopping essential.
- **Which error.** The error $\lVert x_\alpha - x^\dagger\rVert$, the predictive error $\lVert A(x_\alpha - x^\dagger)\rVert$, or an error in a weaker or stronger norm. Different targets give different best $\alpha$.
- **Several parameters.** Multi-parameter regularization, such as $\alpha_1\lVert L_1x\rVert^2 + \alpha_2\lVert L_2x\rVert^2$, needs a vector of parameters. Most rules extend, at a higher cost.
- **Nonlinear problems.** For nonlinear $F(x) = y$ the same rules are used as stopping rules for iterative methods such as iteratively regularized Gauss-Newton.
- **Bayesian view.** In a [Bayesian inverse problem](/bayesian-inverse-problem/), the parameter is a prior precision. It can be fixed, estimated by maximizing the marginal likelihood, or given its own hyperprior and sampled.

## Examples

All rules on one problem: $A = \mathrm{diag}(1/i^2)$ for $i = 1, \dots, 32$, the true solution $x^\dagger_i = 1/i^2$, white noise of standard deviation $\sigma = 10^{-3}$ drawn from `random.Random(0)`, so $\delta = \lVert e\rVert = 0.006508$, and Tikhonov regularization. The best $\alpha$ on a fine grid gives the error $0.05817$.

| rule | type | uses | chosen $\alpha$ | $\lVert x_\alpha - x^\dagger\rVert$ |
|---|---|---|---|---|
| [discrepancy principle](/morozov-discrepancy-principle/), $\tau = 1.1$ | a posteriori | $\delta$ | $2.14 \times 10^{-3}$ | 0.06248 |
| [balancing principle](/lepskii-balancing-principle/), grid $10^{-6}\cdot 2^j$ | a posteriori | $\delta$ | $6.55 \times 10^{-2}$ | 0.19141 |
| [UPRE](/unbiased-predictive-risk-estimator/) | a posteriori, statistical | $\sigma^2$ | $5.04 \times 10^{-4}$ | 0.06641 |
| [GCV](/generalized-cross-validation/) | heuristic | nothing | $7.09 \times 10^{-4}$ | 0.06056 |
| [quasi-optimality](/quasi-optimality-criterion/), $q = 1/2$ | heuristic | nothing | $1.95 \times 10^{-3}$ | 0.06146 |
| [L-curve](/l-curve-method/) | heuristic | nothing | $1.10 \times 10^{-4}$ | 0.15965 |

On this problem the heuristic rules GCV and quasi-optimality do as well as the rules that know the noise, and the balancing principle, with its worst-case noise bound, over-smooths. With the noise from seed 2 instead of seed 0, GCV picks the lowest $\alpha$ of its interval and has an error 25 times the best. One example does not rank rules; it shows the kind of spread to expect.

A second example is in the page [L-curve method](/l-curve-method/): a discretized second-derivative problem with 10 percent noise, where the L-curve corner gives an error within 8 percent of the best.

## Known algorithms

| rule | page | needs | guarantee |
|---|---|---|---|
| a priori $\alpha \sim (\delta/\varrho)^{2/(2\nu + 1)}$ | [Tikhonov convergence rates](/tikhonov-convergence-rates/) | $\delta$, $\nu$, $\varrho$ | order optimal for $\nu$ up to the qualification |
| discrepancy principle | [Morozov discrepancy principle](/morozov-discrepancy-principle/) | $\delta$ | convergent; order optimal for Tikhonov up to $\nu = 1/2$ |
| balancing principle | [Lepskii balancing principle](/lepskii-balancing-principle/) | $\delta$ | oracle inequality on the grid; order optimal for all $\nu$ up to the qualification |
| UPRE | [unbiased predictive risk estimator](/unbiased-predictive-risk-estimator/) | $\sigma^2$ | unbiased estimate of the predictive risk at each $\alpha$ |
| SURE | [Stein's unbiased risk estimate](/stein-unbiased-risk-estimate/) | $\sigma^2$, Gaussian noise | unbiased risk estimate for nonlinear estimators |
| GCV | [generalized cross-validation](/generalized-cross-validation/) | nothing | expected GCV close to the predictive risk when the trace of the influence matrix is small compared with $m$ |
| L-curve | [L-curve method](/l-curve-method/) | nothing | heuristic; known non-convergence examples |
| quasi-optimality | [quasi-optimality criterion](/quasi-optimality-criterion/) | nothing | convergent under conditions on the noise |

For iterative methods the discrepancy principle becomes the stopping rule "stop at the first $k$ with $\lVert Ax_k - y^\delta\rVert \le \tau\delta$". In the Bayesian setting, empirical Bayes and hierarchical models estimate the parameter together with the solution.

## Bounds

- **No convergence without the noise level.** By the [Bakushinskii veto](/bakushinskii-veto/), if a rule does not use $\delta$ and the method converges for all data, then $A^\dagger$ is bounded. So for ill-posed problems every heuristic rule fails for some noise. Heuristic rules converge only under conditions that exclude such noise.
- **Best possible rates.** Under $x^\dagger = (A^\ast A)^\nu w$, $\lVert w\rVert \le \varrho$, no method and rule can do better in the worst case than order $\varrho^{1/(2\nu + 1)}\delta^{2\nu/(2\nu + 1)}$ (theorem, see Engl, Hanke and Neubauer). The a priori rule above reaches it if $\nu$ is known.
- **Saturation.** Tikhonov regularization cannot do better than $O(\delta^{2/3})$, whatever the rule, because its qualification is $1$; see [qualification](/qualification-of-regularization/). With the discrepancy principle it reaches only $O(\delta^{1/2})$.
- **Adaptation costs little.** The balancing principle reaches the best rate for every $\nu$ without knowing $\nu$, at the price of a constant factor.
- **Statistical setting.** With white noise, the predictive risk can be estimated without bias (UPRE), and GCV and $C_L$ are asymptotically optimal for the predictive risk under conditions as $m \to \infty$.

## Reductions

- **To one-dimensional optimization or root finding.** With the SVD known, each rule is a scalar problem in $\log\alpha$: a root of the discrepancy function, or a minimum of the GCV, UPRE or curvature function. Each value costs $\Theta(n)$. Root finders such as the [secant method](/secant-method/) or the [Newton-bisection hybrid](/newton-bisection-hybrid/), and the [golden-section search](/golden-section-search/), then finish the job.
- **To a stopping rule.** For iterative methods, the parameter is the iteration count, and the rule is evaluated once per iteration.
- **From a regularized problem to a denoising problem.** In the SVD basis, Tikhonov regularization is a family of diagonal shrinkage estimators of the coefficients $b_i$, so parameter choice for linear inverse problems reduces to choosing a shrinkage level in a Gaussian sequence model, the setting of [SURE](/stein-unbiased-risk-estimate/) and of [ridge regression](/ridge-regression/).

## Applications

- Image deblurring and tomography, where Tikhonov or total variation regularization is tuned by GCV, the discrepancy principle or SURE.
- Geophysical inversion, where the L-curve and the discrepancy principle with a measured noise level are common.
- Smoothing splines and ridge regression in statistics, where GCV and $C_L$ choose the smoothing parameter.
- Early stopping of iterative reconstruction in medical imaging, and of Krylov methods in [hybrid Krylov regularization](/hybrid-krylov-regularization/), where the rule is applied inside the iteration.
- Learned reconstruction, where parameters of a regularizer are trained by bilevel optimization, and SURE allows training without clean data.

## References
