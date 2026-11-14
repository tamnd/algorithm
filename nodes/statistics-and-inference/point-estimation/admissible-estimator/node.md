---
tag: 9GDGE6
kind: definition
slug: admissible-estimator
name: Admissible estimator
aliases:
- inadmissible estimator
area: statistics-and-inference/point-estimation
level: advanced
summary: An estimator that no other estimator dominates, that is, none has risk at most as large for every parameter and strictly smaller for some.
prereqs: [statistical-decision-theory, mean-squared-error]
see_also: [james-stein-estimator, bayes-estimator, minimum-variance-unbiased-estimator, lehmann-scheffe-theorem, empirical-bayes, minimax-theorem, ridge-regression]
sources:
  - book: isbn:9780387402727
    title: Larry Wasserman, All of Statistics, Springer, 2004
    locator: Chapter 12, Section 12.6 (Admissibility) and Section 12.7 (Stein's Paradox)
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 5 (minimaxity and admissibility, including shrinkage estimators)
  - paper: doi:10.1214/aoms/1177729690
    title: Colin R. Blyth, On minimax statistical decision procedures and their admissibility, Annals of Mathematical Statistics 22(1) (1951), pages 22 to 42
    locator: the limiting Bayes method for admissibility
  - paper: "Charles Stein, Inadmissibility of the usual estimator for the mean of a multivariate normal distribution, Proceedings of the Third Berkeley Symposium on Mathematical Statistics and Probability, volume 1 (1956), pages 197 to 206"
    title: Stein 1956
    locator: admissibility of the sample mean in one and two dimensions, inadmissibility in three or more
  - book: isbn:9780387960982
    title: James O. Berger, Statistical Decision Theory and Bayesian Analysis, second edition, Springer, 1985
    locator: the chapters on minimax analysis and on complete and essentially complete classes
---

An admissible estimator is an estimator that cannot be improved everywhere: no other estimator has risk at most as large at every parameter value and strictly smaller at some value. The definition comes from Wald's [statistical decision theory](/statistical-decision-theory/), and it depends on the loss. Admissibility is a weak requirement, since a constant estimator can be admissible, but failing it is serious: an inadmissible estimator can be replaced by one that is never worse. The most famous inadmissible estimator is the sample mean of three or more normal means, which the [James-Stein estimator](/james-stein-estimator/) dominates.

## Definition

The data $X$ have distribution $P_\theta$, $\theta \in \Theta$; estimators $\delta(X)$ of $\psi(\theta)$ are compared by their risk $R(\theta, \delta) = \mathbb{E}_\theta L(\theta, \delta(X))$ for a fixed [loss](/loss-function/) $L$. Under squared error, the risk is the [mean squared error](/mean-squared-error/).

**Domination.** $\delta'$ **dominates** $\delta$ when

$$R(\theta, \delta') \le R(\theta, \delta) \ \text{ for every } \theta \in \Theta, \qquad R(\theta_0, \delta') < R(\theta_0, \delta) \ \text{ for some } \theta_0 \in \Theta.$$

**Admissible and inadmissible.** $\delta$ is **admissible** (for the loss $L$ and the parameter set $\Theta$) when no estimator dominates it, and **inadmissible** when some estimator does.

Admissibility is relative to the loss, to $\Theta$, and to the class of competing estimators (often all estimators, sometimes all randomized ones).

### Properties

**(a) A unique Bayes rule is admissible.** Let $\delta_\pi$ be the unique Bayes rule for a prior $\pi$ (unique up to rules with the same risk), with finite Bayes risk $r(\pi, \delta_\pi) = \int R(\theta, \delta_\pi)\, \pi(d\theta)$. If $\delta'$ dominated $\delta_\pi$, then $r(\pi, \delta') \le r(\pi, \delta_\pi)$, so $\delta'$ would also be Bayes, and by uniqueness it would have the same risk as $\delta_\pi$, which contradicts domination. $\square$

**(b) Bayes rules with a prior of full support.** If $\Theta$ is an open set, every estimator has a risk continuous in $\theta$, $\pi$ gives positive mass to every open set, and $r(\pi, \delta_\pi) < \infty$, then $\delta_\pi$ is admissible. If $\delta'$ dominated it with strict inequality at $\theta_0$, by continuity the inequality would be strict on an open set around $\theta_0$, which has positive prior mass, so $r(\pi, \delta') < r(\pi, \delta_\pi)$. $\square$

**(c) Admissible with constant risk implies minimax.** If $R(\theta, \delta) = c$ for all $\theta$ and $\delta$ were not minimax, some $\delta'$ would have $\sup_\theta R(\theta, \delta') < c$, so $\delta'$ would dominate $\delta$. $\square$

**(d) Blyth's method.** Suppose risks are continuous in $\theta$. If there are priors $\pi_k$, not necessarily of mass 1, with Bayes rules $\delta_k$ such that for every nonempty open set $C \subseteq \Theta$

$$\frac{r(\pi_k, \delta) - r(\pi_k, \delta_k)}{\pi_k(C)} \to 0,$$

then $\delta$ is admissible (Blyth 1951). The idea is that of (b): a rule that dominates $\delta$ would beat it by a fixed amount on some open set, and so its Bayes risk would be below that of the Bayes rule $\delta_k$ for large $k$, which is impossible.

**(e) Complete classes.** Under conditions on $\Theta$ and $L$, Wald's complete class theorems say that every admissible rule is a Bayes rule or a limit of Bayes rules. Under a strictly convex loss, the [Rao-Blackwell theorem](/rao-blackwell-theorem/) shows that an estimator with finite risk that is not a function of a sufficient statistic is inadmissible.

## Examples and non-examples

**The normal mean in one dimension is admissible.** Let $X \sim N(\theta, 1)$, $\theta \in \mathbb R$, with squared error. Apply Blyth's method with the unnormalized priors $\pi_\tau(d\theta) = e^{-\theta^2/(2\tau^2)}\, d\theta$. The Bayes rule is $\frac{\tau^2}{1 + \tau^2} X$, with risk $\frac{\tau^4 + \theta^2}{(1 + \tau^2)^2}$; integrating against $\pi_\tau$, whose total mass is $\sqrt{2\pi}\,\tau$, gives the Bayes risk $\sqrt{2\pi}\,\tau \cdot \frac{\tau^2}{1 + \tau^2}$. The risk of $X$ is $1$, so its Bayes risk is $\sqrt{2\pi}\,\tau$. The difference is $\sqrt{2\pi}\,\tau/(1 + \tau^2) \to 0$ as $\tau \to \infty$, while $\pi_\tau(C)$ increases to the Lebesgue measure of $C$, which is positive. So $X$ is admissible. It has constant risk, so by (c) it is also minimax.

**The binomial proportion is admissible.** Let $X \sim$ Binomial$(n, p)$, $0 < p < 1$, with squared error. Use the weighted loss $(d - p)^2/(p(1-p))$ and the uniform prior. For $1 \le x \le n - 1$ the posterior expected loss is proportional to $\int_0^1 (d - p)^2 p^{x-1}(1-p)^{n-x-1}\, dp$, minimized only at the Beta$(x, n-x)$ mean $x/n$; for $x = 0$ it is finite only at $d = 0$, and for $x = n$ only at $d = 1$. So $X/n$ is the unique Bayes rule for the weighted loss and is admissible for it by (a). On $(0, 1)$ the two risks differ by the positive factor $p(1-p)$, so domination under one loss is domination under the other, and $X/n$ is admissible under squared error.

**Constant estimators.** In the normal model, $\delta(X) = \theta_0$ is admissible under squared error. A rule that dominates it must have risk $0$ at $\theta_0$, so it equals $\theta_0$ with $P_{\theta_0}$-probability 1. All $P_\theta$ have the same null sets, so it equals $\theta_0$ almost surely under every $\theta$ and has the same risk. Admissible does not mean good.

**Non-example: the unbiased normal variance.** For iid $N(\mu, \sigma^2)$ data and squared error, $S^2$ (divisor $n - 1$) has risk $2\sigma^4/(n-1)$, and $\sum_i (X_i - \bar X)^2/(n + 1)$ has risk $2\sigma^4/(n+1)$, smaller for every $(\mu, \sigma^2)$. So $S^2$, the [minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/), is inadmissible. Stein (1964) showed that the estimator with divisor $n + 1$ is also inadmissible.

**Non-example: values outside the range.** If $\psi(\theta)$ always lies in an interval $[a, b]$, clipping an estimator to $[a, b]$ moves every outside value closer to every possible target. If the estimator falls outside $[a, b]$ with positive probability, the clipped version dominates it under squared error. For one Poisson observation, the unbiased estimator $(-1)^X$ of $e^{-2\lambda} \in (0, 1)$ is dominated by $\mathbf{1}\{X \text{ even}\}$.

**Non-example: the normal mean in three or more dimensions.** Let $X \sim N_p(\theta, I_p)$ with the total squared error $\lVert \delta - \theta \rVert^2$. The estimator $X$ has risk $p$ for every $\theta$. It is admissible for $p = 1$ (shown above) and for $p = 2$ (Stein 1956). For $p \ge 3$, the [James-Stein estimator](/james-stein-estimator/) $\big(1 - (p-2)/\lVert X \rVert^2\big) X$ has risk $p - (p-2)^2\, \mathbb{E}_\theta[1/\lVert X \rVert^2] < p$ for every $\theta$, with risk $2$ at $\theta = 0$. So $X$ is inadmissible, although it is minimax and is the maximum likelihood estimator. This is Stein's paradox.

### Pitfalls

- **Admissible is a weak property.** A constant estimator is admissible. Admissibility rules estimators out; it does not single one out.
- **The loss matters.** The same estimator can be admissible under one loss and inadmissible under another. For the normal means problem, inadmissibility of $X$ is for the sum of the squared errors over the coordinates; each coordinate of $X$ alone is admissible for its own mean.
- **A dominating estimator can itself be inadmissible.** The James-Stein estimator is dominated by its positive-part version, which is still inadmissible.
- **Good properties do not imply admissibility.** Being unbiased, minimax, maximum likelihood or of minimum variance among unbiased estimators does not make an estimator admissible, as $S^2$ and the normal mean in three dimensions show.

## Related definitions

- [Statistical decision theory](/statistical-decision-theory/): risk, Bayes and minimax rules.
- Minimax estimator: an estimator with the smallest maximum risk. An admissible estimator with constant risk is minimax; a minimax estimator need not be admissible.
- [Bayes estimator](/bayes-estimator/): unique Bayes rules are admissible, and admissible rules are often limits of Bayes rules.
- [James-Stein estimator](/james-stein-estimator/) and [empirical Bayes](/empirical-bayes/): shrinkage that dominates the sample mean in three or more dimensions.

## References
