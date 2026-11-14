---
tag: Z3VQ97
kind: concept
slug: statistical-decision-theory
name: Statistical decision theory
aliases:
- Wald's decision theory
- risk function
area: statistics-and-inference/point-estimation
level: core
summary: Wald's framework in which an estimator or test is a decision rule judged by its risk, the expected loss. It defines admissible, minimax and Bayes rules.
prereqs: [estimator, loss-function, expected-value]
see_also: [admissible-estimator, bayes-estimator, james-stein-estimator, minimax-theorem, zero-sum-game, empirical-risk-minimization, type-i-and-type-ii-errors, mean-squared-error]
sources:
  - book: "Abraham Wald, Statistical Decision Functions, Wiley, 1950"
    title: Wald 1950
    locator: the general theory of decision functions, risk, minimax and Bayes solutions, complete classes
  - book: isbn:9780387960982
    title: James O. Berger, Statistical Decision Theory and Bayesian Analysis, second edition, Springer, 1985
    locator: the chapters on basic concepts, Bayesian analysis, minimax analysis and complete and essentially complete classes
  - book: isbn:9780387402727
    title: Larry Wasserman, All of Statistics, Springer, 2004
    locator: Chapter 12 (Statistical Decision Theory), Sections 12.1 to 12.6
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 7.3.4 (loss function optimality)
  - paper: doi:10.1214/aoms/1177729838
    title: J. L. Hodges Jr. and E. L. Lehmann, Some problems in minimax point estimation, Annals of Mathematical Statistics 21 (1950), pages 182 to 197
    locator: the minimax estimator of a binomial proportion under squared error
---

Statistical decision theory treats every statistical procedure, such as an estimator, a test or a confidence set, as a rule that maps the data to an action. A [loss function](/loss-function/) scores each action against the true parameter, and the rule is judged by its risk, the expected loss at each parameter value. Abraham Wald built the framework in the 1940s and set it out in his book of 1950. It gives exact meanings to "better", "best on average" and "best in the worst case", through the ideas of [admissible](/admissible-estimator/), Bayes and minimax rules.

## In plain words

A statistician must act on data without knowing the truth: give a number, accept or reject a claim, choose a treatment. Each action has a cost that depends on the truth. A rule says in advance what to do for each possible data set. Because the data are random, the cost of a rule is random too, so we look at its average cost for each possible truth. One rule is better than another if its average cost is never higher and sometimes lower. Usually no rule is best for every possible truth, so we choose a rule that is best on average over a weighting of the truths, or one whose worst case is as small as possible.

## The idea

**The parts.**

- A parameter space $\Theta$, and data $X$ with distribution $P_\theta$, $\theta \in \Theta$.
- An action space $\mathcal A$: the values of $\psi(\theta)$ for estimation, $\{\text{accept}, \text{reject}\}$ for a test, a set of intervals for interval estimation.
- A loss $L(\theta, a) \ge 0$: the cost of action $a$ when $\theta$ is true. Squared error $(\psi(\theta) - a)^2$ and absolute error $\lvert \psi(\theta) - a \rvert$ are common for estimation; 0-1 loss for tests.
- A decision rule $\delta : \mathcal X \to \mathcal A$. A randomized rule picks the action at random, with a distribution that depends on $x$.

**Risk.** The risk of $\delta$ at $\theta$ is

$$R(\theta, \delta) = \mathbb{E}_\theta\, L(\theta, \delta(X)).$$

Under squared error, the risk of an estimator is its [mean squared error](/mean-squared-error/). For a test with 0-1 loss, the risk is the probability of a [type I error](/type-i-and-type-ii-errors/) when $\theta$ is in the null set and of a type II error when it is in the alternative. The risk of a rule is a curve over $\Theta$, not a single number.

**Domination and admissibility.** $\delta'$ *dominates* $\delta$ when $R(\theta, \delta') \le R(\theta, \delta)$ for every $\theta$, with strict inequality for at least one $\theta$. A rule that no other rule dominates is [admissible](/admissible-estimator/). An inadmissible rule should not be used, because some other rule is never worse.

**Why no rule is best everywhere.** The constant estimator $\delta(X) = \theta_0$ has risk zero at $\theta = \theta_0$ under squared error. A rule that is best at every $\theta$ would need risk zero at every $\theta$, which is impossible except in trivial problems. There are three standard ways out.

1. **Restrict the class of rules.** Ask for the best rule among unbiased rules ([minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/)), or among rules that respect a symmetry of the problem (equivariant rules).
2. **Average over $\theta$: Bayes rules.** For a prior $\pi$ on $\Theta$, the Bayes risk is $r(\pi, \delta) = \int R(\theta, \delta)\, \pi(d\theta)$, and a rule that minimizes it is a Bayes rule for $\pi$.
3. **Guard against the worst case: minimax rules.** A rule $\delta^*$ is minimax when $\sup_\theta R(\theta, \delta^*) = \inf_\delta \sup_\theta R(\theta, \delta)$.

**Computing a Bayes rule.** By Fubini's theorem, $r(\pi, \delta) = \int \Big(\int L(\theta, \delta(x))\, \pi(d\theta \mid x)\Big)\, m(dx)$, where $\pi(\cdot \mid x)$ is the posterior and $m$ the marginal law of $X$. So a rule that, for each $x$, picks the action with the smallest posterior expected loss is a Bayes rule. Under squared error this is the posterior mean, under absolute error a posterior median, and under 0-1 loss on a finite $\Theta$ the posterior mode. See [Bayes estimator](/bayes-estimator/).

**A Bayes rule with constant risk is minimax.** Let $\delta_\pi$ be a Bayes rule for $\pi$ with $R(\theta, \delta_\pi) = c$ for every $\theta$. For any rule $\delta$,

$$\sup_\theta R(\theta, \delta) \ \ge\ r(\pi, \delta) \ \ge\ r(\pi, \delta_\pi) = c = \sup_\theta R(\theta, \delta_\pi).$$

The first step holds because an average is at most the maximum, and the second because $\delta_\pi$ is Bayes. So $\delta_\pi$ is minimax, and $\pi$ is a least favorable prior: no prior has a larger Bayes risk.

**The statistical game.** Decision theory is a [zero-sum game](/zero-sum-game/) between nature, which picks $\theta$, and the statistician, who picks $\delta$, with payoff $R(\theta, \delta)$. Randomized rules and priors are the mixed strategies. Under conditions such as a finite $\Theta$, the [minimax theorem](/minimax-theorem/) gives $\inf_\delta \sup_\pi r(\pi, \delta) = \sup_\pi \inf_\delta r(\pi, \delta)$: the minimax risk equals the largest Bayes risk.

**Complete classes.** Wald's complete class theorems say that, under conditions, every admissible rule is a Bayes rule or a limit of Bayes rules. With a convex loss, the [Rao-Blackwell theorem](/rao-blackwell-theorem/) shows that rules that depend on the data only through a sufficient statistic are enough, and that randomized rules are not needed.

## Examples

**A binomial proportion with four trials.** Let $X \sim$ Binomial$(4, p)$ and use squared error. Compare $\bar X = X/4$ with $\delta^*(X) = (X + 1)/6$.

| $p$ | $0$ | $0.1$ | $0.3$ | $0.5$ |
|---|---|---|---|---|
| $R(p, \bar X) = p(1-p)/4$ | $0$ | $0.0225$ | $0.0525$ | $0.0625$ |
| $R(p, \delta^*)$ | $0.0278$ | $0.0278$ | $0.0278$ | $0.0278$ |

The risk of $\delta^*$ is $\big(4p(1-p) + (1 - 2p)^2\big)/36 = 1/36$ for every $p$. The estimator $\delta^*$ is the posterior mean under the uniform prior, so it is a Bayes rule with constant risk, and so it is minimax. Its maximum risk $1/36 \approx 0.0278$ is well below the $1/16 = 0.0625$ of $\bar X$. But $\bar X$ has smaller risk when $p(1-p) < 1/9$, that is for $p < 0.1273$ or $p > 0.8727$. Neither rule dominates the other. Under the uniform prior, the Bayes risk of $\bar X$ is $\int_0^1 p(1-p)/4\, dp = 1/24$, larger than $1/36$. For general $n$ the minimax rule is $(X + \sqrt n/2)/(n + \sqrt n)$, the Bayes rule for the Beta$(\sqrt n/2, \sqrt n/2)$ prior, with constant risk $1/(4(\sqrt n + 1)^2)$ (Hodges and Lehmann 1950); at $n = 4$ that prior is uniform.

**Shrinking a normal mean.** Let $X \sim N(\theta, 1)$ and $\delta_c(X) = cX$ under squared error. Then $R(\theta, \delta_c) = c^2 + (1 - c)^2\theta^2$. For $c = 1$ the risk is $1$ for every $\theta$. For $c < 1$ it is smaller near $\theta = 0$ but grows without bound, so $X$ is minimax. In one dimension $X$ is also admissible; in three or more dimensions the [James-Stein estimator](/james-stein-estimator/) dominates it.

**Testing.** For a test of $H_0: \theta \in \Theta_0$ with 0-1 loss, the risk at $\theta \in \Theta_0$ is the probability of rejection, and at $\theta \notin \Theta_0$ the probability of acceptance. Neyman-Pearson theory fixes the first below $\alpha$ and minimizes the second, which is the "restrict the class" route; a Bayes test instead weights the two errors by a prior and rejects when the posterior odds exceed the ratio of the losses.

## Where it is used

- **Estimation theory.** Mean squared error comparisons, [admissible estimators](/admissible-estimator/), minimax estimators and shrinkage, including the [James-Stein estimator](/james-stein-estimator/) and empirical Bayes methods.
- **Bayesian statistics.** A [Bayes estimator](/bayes-estimator/) is the action that minimizes posterior expected loss; the loss chosen decides whether it is a mean, a median or a mode.
- **Machine learning.** [Empirical risk minimization](/empirical-risk-minimization/) replaces the expected loss by its average over training data. There the risk is taken over the data distribution for a fixed predictor, which is a different reading of the same word.
- **Sequential analysis.** Wald's [sequential probability ratio test](/sequential-probability-ratio-test/) came from the same program, with the cost of sampling added to the loss.
- **Games and robustness.** The minimax criterion links statistics to [game theory](/minimax-theorem/) and to robust procedures that control the worst case over a set of models.

## References
