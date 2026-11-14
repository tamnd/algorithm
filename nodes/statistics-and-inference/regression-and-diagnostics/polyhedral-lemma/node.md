---
tag: TA2HX1
kind: theorem
slug: polyhedral-lemma
name: Polyhedral lemma
aliases:
- Lee-Sun-Sun-Taylor lemma
- exact post-selection inference for the lasso
area: statistics-and-inference/regression-and-diagnostics
level: research
summary: The lasso selection event is a polyhedron in y, so a linear contrast of y given the event has a truncated normal law. This gives exact post-selection intervals.
prereqs: [post-selection-inference, lasso-regression, kkt-conditions, pivotal-quantity, confidence-interval]
see_also: [stepwise-regression, leaps-and-bounds, scheffe-method, exponential-family-distribution, uniformly-most-powerful-test, conditional-expectation, knockoff-filter, kolmogorov-smirnov-test]
sources:
  - paper: doi:10.1214/15-AOS1371
    title: "Jason D. Lee, Dennis L. Sun, Yuekai Sun and Jonathan E. Taylor, Exact post-selection inference, with application to the lasso, Annals of Statistics 44(3), 2016, pp. 907 to 927"
    locator: Sections 4 and 5 (the lasso selection event as a polyhedron, the polyhedral lemma and the truncated Gaussian pivot)
  - paper: doi:10.1080/01621459.2015.1108848
    title: "Ryan J. Tibshirani, Jonathan Taylor, Richard Lockhart and Robert Tibshirani, Exact post-selection inference for sequential regression procedures, Journal of the American Statistical Association 111(514), 2016, pp. 600 to 620"
    locator: Sections 2 to 4 (the polyhedral form of forward stepwise and least angle regression events, the pivot for general Sigma)
  - paper: doi:10.1073/pnas.1507583112
    title: "Jonathan Taylor and Robert J. Tibshirani, Statistical learning and selective inference, Proceedings of the National Academy of Sciences 112(25), 2015, pp. 7629 to 7634"
    locator: The whole paper (the lemma in the setting of selective inference)
  - paper: doi:10.1080/01621459.2020.1732989
    title: "Danijel Kivaranovic and Hannes Leeb, On the length of post-model-selection confidence intervals conditional on polyhedral constraints, Journal of the American Statistical Association 116(534), 2021, pp. 845 to 857"
    locator: The main theorems (infinite expected length of the intervals from the lemma)
  - paper: doi:10.1214/17-AOS1564
    title: "Xiaoying Tian and Jonathan Taylor, Selective inference with a randomized response, Annals of Statistics 46(2), 2018, pp. 679 to 710"
    locator: The whole paper (randomized selection, which leaves more information for the inference than the lemma does)
  - paper: doi:10.1214/13-AOS1175
    title: "Richard Lockhart, Jonathan Taylor, Ryan J. Tibshirani and Robert Tibshirani, A significance test for the lasso, Annals of Statistics 42(2), 2014, pp. 413 to 468"
    locator: The whole paper (the covariance test, an asymptotic test along the lasso path that came before the exact lemma)
---

The polyhedral lemma, also called the Lee-Sun-Sun-Taylor lemma, gives the exact law of a linear function $\eta^\top y$ of a normal vector $y$ given that $y$ fell in a polyhedron $\{Ay \le d\}$. Given the event and the part of $y$ that is independent of $\eta^\top y$, the law is a normal law truncated to an interval $[V^-, V^+]$ whose ends are computed from the data. The truncated normal CDF at the observed value is then exactly uniform, which gives exact tests and intervals after selection. The lemma is the engine of [post-selection inference](/post-selection-inference/) for the [lasso](/lasso-regression/), forward stepwise regression and least angle regression, whose selection events are polyhedra. Its other name, exact post-selection inference for the lasso, comes from the title of the paper of Lee, Sun, Sun and Taylor.

## Statement

Let $y \in \mathbb R^n$, $A \in \mathbb R^{q \times n}$, $d \in \mathbb R^q$ and $\eta \in \mathbb R^n$. (Lee et al. write $b$ for $d$; here $b$ is kept for regression coefficients.) For $\theta \in \mathbb R$, $\sigma > 0$ and $a < e$ in $[-\infty, \infty]$, let $F^{[a, e]}_{\theta, \sigma^2}$ be the CDF of the normal law $N(\theta, \sigma^2)$ truncated to $[a, e]$:

$$F^{[a, e]}_{\theta, \sigma^2}(x) = \frac{\Phi\bigl(\frac{x - \theta}{\sigma}\bigr) - \Phi\bigl(\frac{a - \theta}{\sigma}\bigr)}{\Phi\bigl(\frac{e - \theta}{\sigma}\bigr) - \Phi\bigl(\frac{a - \theta}{\sigma}\bigr)}, \qquad a \le x \le e.$$

**Conditions.**

1. $y \sim N(\mu, \Sigma)$ with $\Sigma$ known; $\Sigma$ may be singular.
2. $A$ and $d$ are fixed, and $P(Ay \le d) > 0$.
3. $\eta$ is fixed and $\sigma_\eta^2 = \eta^\top\Sigma\eta > 0$.

Write $t = \eta^\top y$, $c = \Sigma\eta/\sigma_\eta^2$, $z = y - ct$ and $\alpha = Ac$, and define

$$V^-(z) = \max_{j: \alpha_j < 0}\frac{d_j - (Az)_j}{\alpha_j}, \qquad V^+(z) = \min_{j: \alpha_j > 0}\frac{d_j - (Az)_j}{\alpha_j}, \qquad V^0(z) = \min_{j: \alpha_j = 0}\bigl(d_j - (Az)_j\bigr),$$

with $\max \emptyset = -\infty$ and $\min \emptyset = +\infty$.

**Theorem (Lee, Sun, Sun and Taylor 2016).** Under conditions 1 to 3:

1. $\{Ay \le d\} = \{V^-(z) \le t \le V^+(z),\ V^0(z) \ge 0\}$.
2. $t$ and $z$ are independent.
3. For almost every $z_0$ with $P(Ay \le d \mid z = z_0) > 0$, the law of $t$ given $Ay \le d$ and $z = z_0$ is $N(\eta^\top\mu, \sigma_\eta^2)$ truncated to $[V^-(z_0), V^+(z_0)]$.
4. The pivot $F^{[V^-(z), V^+(z)]}_{\eta^\top\mu, \sigma_\eta^2}(t)$ has the uniform law on $(0, 1)$ given $Ay \le d$.

## In plain words

Suppose a rule looked at noisy data and chose what to report. Most rules of this kind can be written as a list of straight-line checks on the data, so the data sets that lead to the same choice fill a region with flat sides. Now take one number we want to study, say the effect of the chosen variable. Split the data into this number and the rest, which is unrelated to it. Hold the rest fixed. The flat-sided region then allows the number to move only between a lowest and a highest value. So, given the choice, the number is a bell-curve draw that was forced to land in that range. We know exactly how such a draw behaves, so we can compute an honest p-value and an honest interval that take the choice into account.

## Proof

**Part 1 (the event on a line).** Since $y = z + ct$, $Ay \le d$ holds if and only if $\alpha_j t \le d_j - (Az)_j$ for every row $j$. A row with $\alpha_j > 0$ says $t \le (d_j - (Az)_j)/\alpha_j$; a row with $\alpha_j < 0$ says, after division by a negative number, $t \ge (d_j - (Az)_j)/\alpha_j$; and a row with $\alpha_j = 0$ says $d_j - (Az)_j \ge 0$ and does not involve $t$. The rows of the first kind together say $t \le V^+(z)$, those of the second kind $t \ge V^-(z)$, those of the third kind $V^0(z) \ge 0$. $\square$

**Part 2 (independence).** The pair $(z, t)$ is a linear function of the normal vector $y$, so it is jointly normal. Its cross covariance is

$$\operatorname{Cov}(z, t) = \operatorname{Cov}(y - c\,\eta^\top y,\ \eta^\top y) = \Sigma\eta - c\,\eta^\top\Sigma\eta = \Sigma\eta - \Sigma\eta = 0.$$

For a jointly normal vector, zero cross covariance between two blocks means independence of the blocks, also when the covariance is singular, because the joint characteristic function then factors. $\square$

**Part 3 (the truncated law).** Write $\theta = \eta^\top\mu$, $E = \{Ay \le d\}$, $I(z) = [V^-(z), V^+(z)]$ and $\pi(z) = P_\theta(T \in I(z))$ for $T \sim N(\theta, \sigma_\eta^2)$. By Part 1, $\mathbf 1_E = \mathbf 1\{V^0(z) \ge 0\}\,\mathbf 1\{t \in I(z)\}$. The functions $V^-$, $V^+$ and $V^0$ are measurable, being maxima and minima of finitely many affine functions. By Part 2, $t$ is independent of $z$ and has the law $N(\theta, \sigma_\eta^2)$, so for every Borel set $B$, by the substitution rule for [conditional expectations](/conditional-expectation/) of independent variables,

$$P(t \in B,\ E \mid z) = \mathbf 1\{V^0(z) \ge 0\}\,P_\theta\bigl(T \in B \cap I(z)\bigr) \quad \text{almost surely}.$$

With $B = \mathbb R$ this gives $P(E \mid z) = \mathbf 1\{V^0(z) \ge 0\}\,\pi(z)$. Where this is positive, the ratio of the two is $P_\theta(T \in B \mid T \in I(z))$, the truncated normal law. $\square$

**Part 4 (the uniform pivot).** Let $G = F^{I(z)}_{\theta, \sigma_\eta^2}(t)$ and $u \in (0, 1)$. If $X$ has a continuous CDF $F$, then $P(F(X) \le u) = u$. Apply this to the truncated law of Part 3, which has a continuous CDF, for a fixed $z$ with $V^0(z) \ge 0$ and $\pi(z) > 0$:

$$P(G \le u,\ E \mid z) = \pi(z)\,P\bigl(F^{I(z)}_{\theta, \sigma_\eta^2}(T) \le u \bigm| T \in I(z)\bigr) = u\,\pi(z).$$

If $V^0(z) < 0$ or $\pi(z) = 0$, both $P(G \le u, E \mid z)$ and $u\,P(E \mid z)$ are 0. So $P(G \le u, E \mid z) = u\,P(E \mid z)$ almost surely. Taking expectations gives $P(G \le u, E) = u\,P(E)$, and dividing by $P(E) > 0$ gives $P(G \le u \mid E) = u$. $\square$

## Consequences

**Tests.** To test $\eta^\top\mu = \theta_0$ against $\eta^\top\mu > \theta_0$, reject when $1 - F^{[V^-, V^+]}_{\theta_0, \sigma_\eta^2}(t) \le \alpha$. By Part 4 the level is exactly $\alpha$ given the selection event, and so also given the selected model.

**Intervals.** For $a < x < e$, the map $\theta \mapsto F^{[a, e]}_{\theta, \sigma^2}(x)$ is strictly decreasing. *Proof.* The truncated law has density proportional to $e^{\theta s/\sigma^2}e^{-s^2/(2\sigma^2)}$ on $[a, e]$, a one-parameter [exponential family](/exponential-family-distribution/). Differentiating under the integral, $\partial_\theta\log F_\theta(x) = (E_\theta[S \mid S \le x] - E_\theta[S])/\sigma^2$ for $S$ with this law, and the mean of a law with a density, restricted to its part below $x < e$, is smaller than the full mean. As $\theta \to -\infty$ the law piles up at $a$ and $F_\theta(x) \to 1$; as $\theta \to \infty$ it piles up at $e$, or moves to $+\infty$ if $e = \infty$, and $F_\theta(x) \to 0$. $\square$ So there are unique $L < U$ with $F_L(t) = 1 - \alpha/2$ and $F_U(t) = \alpha/2$, and $\{L \le \eta^\top\mu \le U\} = \{\alpha/2 \le F_{\eta^\top\mu}(t) \le 1 - \alpha/2\}$, which has probability $1 - \alpha$ given the event by Part 4. A bisection on $\theta$ finds $L$ and $U$.

**Selection events that are polyhedra.** The lemma needs $A$, $d$ and $\eta$ fixed, so in use one conditions on the event $\{\hat M = M\}$ for the model $M$ that was selected, and lets $\eta = \eta_M$, for example the row of $(X_M^\top X_M)^{-1}X_M^\top$ for one coefficient. Then the lemma applies whenever $\{\hat M = M\}$, or a finer event inside it, is a polyhedron.

- *Largest $|y_j|$.* Selecting $j$ with sign $s$ is the event $\{s y_j \ge y_k,\ s y_j \ge -y_k \text{ for } k \ne j,\ s y_j \ge 0\}$.
- *The lasso.* Let $\hat b$ minimize $\frac12\|y - Xb\|^2 + \lambda\|b\|_1$ with fixed $\lambda > 0$; here $b$ is the coefficient vector. Let $E$ be the active set, $s$ its signs, $X_E$ of full column rank, $X_E^+ = (X_E^\top X_E)^{-1}X_E^\top$ and $P_E = X_EX_E^+$. Up to a set of probability 0, $\{\hat E = E, \hat s = s\}$ is the polyhedron of the two conditions
$$-\operatorname{diag}(s)X_E^+y < -\lambda\operatorname{diag}(s)(X_E^\top X_E)^{-1}s, \qquad \Bigl|\tfrac1\lambda X_{-E}^\top(I - P_E)y + X_{-E}^\top(X_E^+)^\top s\Bigr| < \mathbf 1.$$
*Proof.* By the [KKT conditions](/kkt-conditions/), $\hat b$ solves the problem if and only if $X^\top(y - X\hat b) = \lambda g$ with $g_j = \operatorname{sign}(\hat b_j)$ where $\hat b_j \ne 0$ and $|g_j| \le 1$ elsewhere. If $\hat E = E$ and $\hat s = s$, the rows in $E$ give $\hat b_E = X_E^+y - \lambda(X_E^\top X_E)^{-1}s$, so the first condition is $\operatorname{diag}(s)\hat b_E > 0$; the rows outside $E$ give $g_{-E}$ equal to the vector inside the absolute value, using $y - X_E\hat b_E = (I - P_E)y + \lambda(X_E^+)^\top s$; and $|g_{-E}| = 1$ in some coordinate has probability 0. Conversely, if $y$ satisfies both conditions, the vector with these $\hat b_E$ and $\hat b_{-E} = 0$ satisfies the KKT conditions, so it is a solution. All solutions have the same fit $X\hat b$, because the loss is strictly convex in $Xb$ and the objective is convex, so they have the same $g$, and $|g_j| < 1$ forces $\hat b_j = 0$ off $E$; since $X_E$ has full rank, the solution is unique. $\square$
- *Forward stepwise and least angle regression.* Each step compares the candidates by inner products with the current residual, and the event "this variable entered with this sign at this step" is again a set of linear inequalities in $y$ (Tibshirani et al. 2016).

Conditioning only on $\hat E = E$, without the signs, gives a union of $2^{|E|}$ polyhedra; on a line through $y$ this is a union of intervals, and the same proof gives a normal law truncated to that union, with shorter intervals.

**A hand example.** Take $y \sim N(\mu, I_3)$, the largest-$|y_j|$ rule and the observed $y = (2.5, -1.0, 0.8)$. The rule picks $j = 1$ with sign $+$, so $\eta = e_1$, $t = 2.5$, $c = e_1$ and $z = (0, -1.0, 0.8)$. Every row of $A$ has coefficient $-1$ on $y_1$, so $\alpha_j = -1$ for all rows, $V^+ = \infty$, and $V^- = \max(|y_2|, |y_3|, 0) = 1$: given the event and $z$, $y_1$ is a normal variable truncated to $[1, \infty)$. The selective p-value for $\mu_1 = 0$ against $\mu_1 > 0$ is $Q(2.5)/Q(1) = 0.006210/0.158655 = 0.0391$, where $Q = 1 - \Phi$, against the naive one-sided $0.0062$. The 95% interval is $[-0.341, 4.455]$, against the naive $[0.540, 4.460]$. Moving $y_1$ and keeping $y_2$ and $y_3$:

| $y_1$ | selective 95% interval | selective p | naive one-sided p |
|---|---|---|---|
| 1.05 | $[-72.74, 1.531]$ | 0.926 | 0.147 |
| 1.2 | $[-17.29, 2.657]$ | 0.725 | 0.115 |
| 1.5 | $[-5.994, 3.309]$ | 0.421 | 0.0668 |
| 2.0 | $[-1.933, 3.933]$ | 0.143 | 0.0228 |
| 2.5 | $[-0.341, 4.455]$ | 0.0391 | 0.0062 |
| 3.0 | $[0.630, 4.959]$ | 0.0085 | 0.0013 |
| 4.0 | $[1.963, 5.960]$ | 0.0002 | 0.00003 |

Far from the edge $V^- = 1$ the selective and naive answers agree; near it the data barely passed the selection, and the interval becomes long on the left.

**A measured check.** With 5 coordinates, 4000 draws (seed 20261114) and the same rule, the Kolmogorov-Smirnov distance of the 4000 pivots from the uniform law was 0.0114 for $\mu = 0$ and 0.0161 for $\mu = (1, 0.5, 0, 0, -2)$. The naive pivot $\Phi(t - \eta^\top\mu)$ gave 0.7249 and 0.3593. These distances are measurements of one simulation; the uniformity itself is what Part 4 proves.

## Tightness

**Normality.** Part 2 uses that uncorrelated parts of a normal vector are independent. For other error laws, $z$ and $t$ are uncorrelated but not independent, the law of $t$ given $z$ is not normal, and the pivot is only approximately uniform. Asymptotic versions need extra conditions, and they are less well understood near the edges of the selection region.

**Known covariance.** The pivot uses $\sigma_\eta^2$. With $\sigma^2$ estimated from the same data, the plug-in pivot is not exactly uniform, and the estimate is not independent of the selection when it uses the residuals of the selected model.

**Fixed $A$, $d$ and $\eta$.** If the analyst chooses $\eta$ after looking at more than the selection event, for example at $t$ itself, Part 4 fails.

**Length of the intervals.** In the table, as $y_1$ moves down to $V^- = 1$, the lower end of the interval goes to $-\infty$. Kivaranovic and Leeb (2021) proved that, in common settings, the expected length of these intervals is infinite. The lemma is exact, but it can be very uninformative.

**Power.** Conditioning on $z$ and on the signs uses less of the data than is available. Conditioning on the selected model alone (the union of polyhedra above), or randomizing the selection step (Tian and Taylor 2018), gives shorter intervals with the same exact guarantee.

## History

Lockhart, Taylor, Tibshirani and Tibshirani (2014) gave the covariance test, an asymptotic test for variables entering along the lasso path. Lee, Sun, Sun and Taylor posted the exact result in 2013 and published it in the Annals of Statistics in 2016, with the lasso as the main application. Tibshirani, Taylor, Lockhart and Tibshirani (2016) used the same lemma for forward stepwise regression and least angle regression, and Taylor and Tibshirani (2015) placed it in a general framework of selective inference. Later work by Tian and Taylor (2018) and others added randomization for power, and Kivaranovic and Leeb (2021) studied the length of the intervals.

## References
