---
tag: HC9Z9C
kind: definition
slug: bayes-estimator
name: Bayes estimator
aliases:
- posterior mean estimator
area: statistics-and-inference/bayesian-statistics
level: core
summary: 'The estimator that minimizes posterior expected loss: the posterior mean for squared loss, the median for absolute loss. It minimizes the Bayes risk.'
prereqs: [statistical-decision-theory, bayesian-inference, loss-function, median]
see_also: [maximum-a-posteriori-estimation, admissible-estimator, credible-interval, james-stein-estimator, empirical-bayes, estimator-bias, mean-squared-error, quantile]
sources:
  - book: isbn:9780387715988
    title: "Christian P. Robert, The Bayesian Choice, 2nd edition, Springer, 2007"
    locator: Chapter 2 (decision-theoretic foundations, Bayes risk and Bayes estimators) and Chapter 4 (Bayesian point estimation under squared, absolute and 0-1 losses)
  - paper: doi:10.1214/aoms/1177698625
    title: "P. J. Bickel and D. Blackwell, A note on Bayes estimates, Annals of Mathematical Statistics 38(6), 1967"
    locator: pages 1907 to 1911 (an unbiased Bayes estimate under squared error has Bayes risk 0, and the extension to more general losses)
  - book: isbn:9781439840955
    title: "Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, 3rd edition, CRC Press, 2013"
    locator: Chapter 2 (posterior summaries for the binomial and normal models) and Chapter 9 (decision analysis)
---

A Bayes estimator for a prior $\pi$ and a [loss function](/loss-function/) $L$ is an estimator that minimizes the Bayes risk, the risk averaged over the prior. It can be found one data set at a time: for each observed $x$, take the value $a$ that minimizes the posterior expected loss $\int L(\theta, a)\, \pi(d\theta \mid x)$. Under squared error this is the posterior mean, under absolute error a posterior [median](/median/), and the posterior mode is the limit under 0-1 losses with a shrinking window. The prior and the loss together decide the estimator; the data enter only through the posterior.

## Definition

Use the notation of [statistical decision theory](/statistical-decision-theory/). Data $X$ have density $f(x \mid \theta)$, $\theta \in \Theta$ has a prior $\pi$, the posterior is $\pi(d\theta \mid x)$ and the marginal law of $X$ is $m$. A rule $\delta$ has risk $R(\theta, \delta) = E[L(\theta, \delta(X)) \mid \theta]$ and Bayes risk $r(\pi, \delta) = \int R(\theta, \delta)\, \pi(d\theta)$.

- The **posterior expected loss** of an action $a$ is $\rho(a \mid x) = \int L(\theta, a)\, \pi(d\theta \mid x)$.
- A **Bayes estimator** (Bayes rule) for $\pi$ is a rule $\delta_\pi$ with $r(\pi, \delta_\pi) = \inf_\delta r(\pi, \delta) < \infty$.
- By Fubini's theorem $r(\pi, \delta) = \int \rho(\delta(x) \mid x)\, m(dx)$. So a rule with $\delta(x)$ a minimizer of $\rho(\cdot \mid x)$ for $m$-almost every $x$ is a Bayes estimator. Its values on a set of $x$ with $m$-probability 0 do not matter.
- A **generalized Bayes estimator** minimizes $\rho(a \mid x)$ when $\pi$ is an [improper prior](/improper-prior/) with a proper posterior. It need not be a Bayes rule, because its Bayes risk against an infinite measure is usually infinite.

**Squared error: the posterior mean.** Let $L(\theta, a) = (\theta - a)^2$ and let the posterior have a finite second moment. Then

$$\rho(a \mid x) = \mathrm{Var}(\theta \mid x) + \big(E[\theta \mid x] - a\big)^2,$$

which is smallest at $a = E[\theta \mid x]$, with value $\mathrm{Var}(\theta \mid x)$. So $\delta_\pi(x) = E[\theta \mid x]$, and its Bayes risk is $r(\pi, \delta_\pi) = E[\mathrm{Var}(\theta \mid X)]$, the expected posterior variance. For a vector $\theta$ and the loss $\lVert \theta - a \rVert^2$ the Bayes estimator is the vector of posterior means. For the weighted loss $w(\theta)(\theta - a)^2$ it is $E[w(\theta)\theta \mid x]/E[w(\theta) \mid x]$.

**Absolute error: a posterior median.** Let $L(\theta, a) = |\theta - a|$ and let the posterior have a finite first moment. Then $\rho(a \mid x) = E[|\theta - a| \mid x]$ is convex in $a$, with right derivative $P(\theta \le a \mid x) - P(\theta > a \mid x)$ and left derivative $P(\theta < a \mid x) - P(\theta \ge a \mid x)$. A convex function is smallest at $a$ exactly when its left derivative is at most 0 and its right derivative at least 0, that is when $P(\theta < a \mid x) \le 1/2 \le P(\theta \le a \mid x)$. This is the definition of a posterior median, so every posterior median minimizes $\rho$. With the asymmetric loss $c_1(\theta - a)^+ + c_2(a - \theta)^+$ the same argument gives the posterior [quantile](/quantile/) of order $c_1/(c_1 + c_2)$.

**0-1 loss: the mode as a limit.** Let $L_\varepsilon(\theta, a) = 1\{|\theta - a| > \varepsilon\}$. The Bayes action maximizes the posterior probability of $[a - \varepsilon, a + \varepsilon]$. If the posterior density is continuous with a unique maximum, these actions tend to the posterior mode as $\varepsilon \to 0$. The mode is the [maximum a posteriori estimate](/maximum-a-posteriori-estimation/); it is a limit of Bayes estimators, and it is not a Bayes estimator for a fixed loss in general.

**An unbiased Bayes estimator has Bayes risk 0.** Under squared error, let $\delta$ be a Bayes estimator for a proper prior $\pi$ with $E[\theta^2] < \infty$ and $r(\pi, \delta) < \infty$. If $\delta$ is unbiased, $E[\delta(X) \mid \theta] = \theta$ for every $\theta$, then $r(\pi, \delta) = 0$. Proof: compute $E[\theta\, \delta(X)]$ in two ways under the joint law of $(\theta, X)$. Given $X$, $\delta(X) = E[\theta \mid X]$, so $E[\theta\, \delta(X)] = E[\delta(X)^2]$. Given $\theta$, $E[\delta(X) \mid \theta] = \theta$, so $E[\theta\, \delta(X)] = E[\theta^2]$. Then $r(\pi, \delta) = E[\delta^2] - 2E[\theta\delta] + E[\theta^2] = 0$. The result is older than the paper of Bickel and Blackwell (1967), who extend it to other losses. A Bayes risk of 0 means the data determine $\theta$ with prior probability 1, so in every non-trivial problem a Bayes estimator under squared error is biased (see [estimator bias](/estimator-bias/)).

## Examples and non-examples

**Three losses, one posterior.** With $n = 10$ trials, $x = 3$ successes and the uniform prior, the posterior of $p$ is Beta$(4, 8)$. Its mean is $1/3$, its median 0.3238 and its mode $3/10$. The posterior expected squared loss at the mean is the posterior variance $4 \cdot 8/(12^2 \cdot 13) = 2/117 = 0.017094$; the expected absolute loss at the median is 0.10571. A direct search over $a = 0.0005, 0.0010, \ldots, 0.9995$, with the posterior written as a sum over 20000 equal cells, finds the minimum of the expected squared loss at 0.3335 (the grid point next to $1/3$) and of the expected absolute loss at 0.3240 (next to 0.3238). The 0-1 loss with window $\varepsilon = 0.1$, 0.05 and 0.01 gives 0.3065, 0.3015 and 0.3000, which approach the mode.

**Bayes risk against the MLE.** In the same model, $X \sim$ Binomial$(10, p)$ with the uniform prior, the posterior mean is $(X + 1)/12$. Its risk is $\big(10p(1 - p) + (1 - 2p)^2\big)/144$, and the average over the uniform prior is exactly $1/72 = 0.01389$. This equals $E[\mathrm{Var}(p \mid X)]$, which is $\sum_{x=0}^{10} \frac{1}{11} \cdot \frac{(x + 1)(11 - x)}{12^2 \cdot 13} = 1/72$, because $X$ is uniform on $\{0, \ldots, 10\}$ under this prior. The MLE $X/10$ has Bayes risk $\int_0^1 p(1 - p)/10\, dp = 1/60 = 0.01667$, larger, as it must be. Both values are exact rational numbers.

**A normal mean.** Let $X_1, \ldots, X_n \mid \theta$ be iid $N(\theta, \sigma^2)$ with $\sigma$ known and $\theta \sim N(\mu_0, \tau_0^2)$. The posterior is normal, so its mean, median and mode agree: $\delta_\pi = w\bar X + (1 - w)\mu_0$ with $w = (n/\sigma^2)/(n/\sigma^2 + 1/\tau_0^2)$. It is biased, $E[\delta_\pi \mid \theta] = w\theta + (1 - w)\mu_0$, as the theorem above requires. For the data 9.8, 10.4, 10.1, 9.6, 10.6 with $\sigma = 0.5$ and prior $N(9, 0.4^2)$, $w = 20/26.25 = 0.7619$ and $\delta_\pi = 9.8381$.

**An unbiased rule that is Bayes.** For $X \sim$ Binomial$(n, p)$ and a prior that puts mass 1/2 on each of $p = 0$ and $p = 1$, the data are all 0 or all 1, and $X/n$ gives the right answer with probability 1. It is unbiased and Bayes, with Bayes risk 0, as the theorem allows.

**Non-example: the sample mean of normal data.** $\bar X$ is unbiased for $\theta$ with risk $\sigma^2/n > 0$ at every $\theta$, so by the theorem it is not a Bayes estimator under squared error for any proper prior. It is the generalized Bayes estimator for the flat improper prior, and a limit of the Bayes estimators above as $\tau_0 \to \infty$. In one dimension it is still [admissible](/admissible-estimator/) and minimax.

**Non-example: the mode after a change of scale.** The posterior median is invariant under strictly monotone maps: the median of $\log(p/(1 - p))$ is the log-odds of the median of $p$. The mode is not. On the log-odds scale the Beta$(4, 8)$ posterior has density proportional to $p^4(1 - p)^8$, whose maximum is at $p = 1/3$, not at the mode $3/10$ on the $p$ scale. The posterior mean is not invariant either: $E[g(\theta) \mid x] \ne g(E[\theta \mid x])$ for a nonlinear $g$.

## Related definitions

- **[Statistical decision theory](/statistical-decision-theory/).** The framework of loss, risk and Bayes risk; a Bayes rule with constant risk is minimax.
- **[Admissible estimator](/admissible-estimator/).** A unique Bayes estimator with finite Bayes risk is admissible; Bayes and generalized Bayes rules are the main source of admissible rules.
- **[Maximum a posteriori estimate](/maximum-a-posteriori-estimation/).** The posterior mode, a limit of Bayes estimators under 0-1 loss.
- **[Empirical Bayes](/empirical-bayes/).** The prior is estimated from the data, and the Bayes estimator for the fitted prior is used; the [James-Stein estimator](/james-stein-estimator/) is the classic case.
- **[Credible interval](/credible-interval/).** The interval summary of the same posterior that gives the point summary here.
- **[Mean squared error](/mean-squared-error/).** The risk under squared error; the Bayes risk is its average over the prior.

## References
