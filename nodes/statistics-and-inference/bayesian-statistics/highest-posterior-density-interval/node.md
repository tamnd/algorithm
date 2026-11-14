---
tag: 9T76SY
kind: definition
slug: highest-posterior-density-interval
name: Highest posterior density region
aliases:
- HPD interval
- highest density interval
area: statistics-and-inference/bayesian-statistics
level: core
summary: The smallest region with a given posterior probability, made of the points where the posterior density exceeds a level.
prereqs: [credible-interval, probability-density-function, bayesian-inference]
see_also: [maximum-a-posteriori-estimation, bayes-estimator, likelihood-function, likelihood-ratio-test, confidence-interval, prediction-interval, jeffreys-prior]
sources:
  - book: isbn:9780471574286
    title: "George E. P. Box and George C. Tiao, Bayesian Inference in Statistical Analysis, Addison-Wesley, 1973; Wiley Classics Library reprint, 1992"
    locator: Chapter 2 (highest posterior density intervals and regions, and their lack of invariance)
  - book: isbn:9781439840955
    title: "Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, 3rd edition, CRC Press, 2013"
    locator: Chapter 2 (central posterior intervals and highest posterior density regions, with a bimodal example)
  - book: isbn:9780387715988
    title: "Christian P. Robert, The Bayesian Choice, 2nd edition, Springer, 2007"
    locator: Chapter 5, Section 5.5.1 (credible intervals and HPD regions)
---

The $1 - \alpha$ highest posterior density (HPD) region is the set of parameter values where the posterior density is at least some level $k$, with $k$ chosen so that the set has posterior probability $1 - \alpha$. Among all sets with that posterior probability it has the smallest length, area or volume. For a unimodal posterior on the line it is an interval whose two ends have the same density; for a posterior with two modes it can be two separate intervals. Unlike the equal-tailed [credible interval](/credible-interval/), it changes when the parameter is transformed, because a density changes with the Jacobian of the transformation.

## Definition

Let the posterior of $\theta \in \Theta \subseteq \mathbb{R}^d$ given data $x$ have a [density](/probability-density-function/) $p(\theta \mid x)$ with respect to Lebesgue measure $\lambda$, as in [Bayesian inference](/bayesian-inference/). For $k \ge 0$ let $R_k = \{\theta : p(\theta \mid x) \ge k\}$, and let

$$k_\alpha = \sup\{k : P(\theta \in R_k \mid x) \ge 1 - \alpha\}.$$

The **$1 - \alpha$ HPD region** is $R = R_{k_\alpha}$. If no level set $\{\theta : p(\theta \mid x) = k\}$ has positive Lebesgue measure (the density has no flat parts), then $P(\theta \in R \mid x) = 1 - \alpha$ exactly. When $R$ is an interval it is called the HPD interval.

**It is the smallest credible set.** Let $A$ be any set with $P(\theta \in A \mid x) \ge 1 - \alpha = P(\theta \in R \mid x)$. Then $P(A \setminus R \mid x) \ge P(R \setminus A \mid x)$. On $R \setminus A$ the density is at least $k = k_\alpha$, and on $A \setminus R$ it is less than $k$. So

$$k\, \lambda(R \setminus A) \le P(R \setminus A \mid x) \le P(A \setminus R \mid x) \le k\, \lambda(A \setminus R),$$

and $\lambda(R) \le \lambda(A)$ (for $k > 0$). The last inequality is strict if $\lambda(A \setminus R) > 0$, so when the density has no flat parts the HPD region is the only shortest credible set, up to sets of measure zero.

**The equal-density rule.** For a continuous unimodal posterior on the line, the HPD interval $[a, b]$ solves $P(a \le \theta \le b \mid x) = 1 - \alpha$ and $p(a \mid x) = p(b \mid x)$, unless an end of $\Theta$ is reached first. If the density decreases on all of $\Theta = [0, 1]$, the interval starts at 0. If the posterior is symmetric and unimodal, the HPD and equal-tailed intervals agree.

**It is not invariant.** Let $\phi = g(\theta)$ with $g$ smooth and strictly monotone. The density of $\phi$ is $p(g^{-1}(\phi) \mid x)\, |(g^{-1})'(\phi)|$. The Jacobian factor changes which points have high density, so the HPD region for $\phi$ is in general not $g(R)$. The equal-tailed interval is invariant under every strictly monotone $g$; the HPD region is invariant only under affine maps, which have constant Jacobian.

**It contains the mode.** Every HPD region contains each point where the posterior density is largest, the [maximum a posteriori estimate](/maximum-a-posteriori-estimation/). With a flat prior the posterior density is proportional to the [likelihood](/likelihood-function/), and the HPD region is a likelihood region $\{\theta : L(\theta) \ge c\}$, the same shape of set that a [likelihood ratio test](/likelihood-ratio-test/) inverts.

## Examples and non-examples

**A skewed beta posterior.** With $n = 10$ trials, $x = 3$ successes and the uniform prior, the posterior is Beta$(4, 8)$. The 95% HPD interval is $[0.0934, 0.5880]$, of length 0.4946, and the density at both ends is 0.5410. The equal-tailed interval is $[0.1093, 0.6097]$, of length 0.5005: it moves to the right, toward the long tail. A search over all intervals of posterior mass 0.95 with ends on a grid of 200000 equal cells of $[0, 1]$ gives the same shortest length to within $10^{-5}$; the ends it finds differ by up to $5 \times 10^{-4}$, because the length is flat near its minimum. Under the [Jeffreys prior](/jeffreys-prior/) the posterior is Beta$(3.5, 7.5)$, with 95% HPD interval $[0.0745, 0.5795]$ (length 0.5049) against the equal-tailed $[0.0927, 0.6058]$ (length 0.5131).

**An end of the parameter space.** With $n = 4$, $x = 0$ and the uniform prior, the posterior is Beta$(1, 5)$, with density $5(1 - p)^4$, which decreases on $[0, 1]$. The HPD interval is $[0, c]$ with $1 - (1 - c)^5 = 0.95$, so $c = 1 - 0.05^{1/5} = 0.4507$. The two ends do not have equal density. The equal-tailed interval is $[0.0051, 0.5218]$, of length 0.5168, and it excludes $p = 0$, the most probable value.

**A transformation changes the region.** Put the Beta$(4, 8)$ posterior on the log-odds scale $\eta = \log(p/(1 - p))$. The density of $\eta$ is proportional to $p^4 (1 - p)^8$, with $p = 1/(1 + e^{-\eta})$, because $dp/d\eta = p(1 - p)$. Its 95% HPD interval is $\eta \in [-2.0511, 0.4871]$, which maps back to $p \in [0.1139, 0.6194]$. That is a 95% credible interval for $p$, but it is not the HPD interval $[0.0934, 0.5880]$ for $p$. The equal-tailed interval maps to the log-odds scale exactly, to $[-2.0983, 0.4462]$.

**Two intervals.** Let $X \mid \theta \sim N(|\theta|, 1)$, observe $x = 3$, and use the flat prior on $\theta \in \mathbb{R}$. The posterior density is $\varphi(|\theta| - 3)/(2\Phi(3))$, where $\varphi$ and $\Phi$ are the standard normal density and distribution function; it has modes at $\pm 3$. The 95% HPD region is $\{\theta : 1.0509 \le |\theta| \le 4.9491\}$, two intervals of total length 7.7964, where $c = 1.949109$ solves $(2\Phi(c) - 1)/\Phi(3) = 0.95$. The equal-tailed interval is $[-4.6455, 4.6455]$, of length 9.2910. It contains $\theta = 0$, where the posterior density is $e^{-4.5} = 0.0111$ times its peak.

**Non-example: the interval between the 2.5% and 97.5% posterior quantiles.** That is the equal-tailed credible interval. It is the HPD interval only when the posterior is symmetric and unimodal.

**Non-example: equal density, wrong mass.** For Beta$(4, 8)$, the interval $[0.2, 0.4148]$ has density 2.2146 at both ends, but its posterior mass is 0.5764. It is the 57.64% HPD interval, not the 95% one. The equal-density rule fixes the shape of the interval; the mass condition fixes its level. Both are needed.

**Non-example: a confidence region.** The HPD region is a statement about $\theta$ given $x$, like every credible set. Its frequentist coverage at a fixed $\theta$ is a separate property; see [credible interval](/credible-interval/) for when the two agree.

## Related definitions

- **[Credible interval](/credible-interval/).** Any set of posterior probability $1 - \alpha$; the equal-tailed one is invariant under monotone maps, the HPD one is the shortest.
- **[Maximum a posteriori estimate](/maximum-a-posteriori-estimation/).** The mode of the posterior; the HPD regions shrink to it as $\alpha$ grows to 1 when the mode is unique.
- **Highest density region of a predictive law.** The same construction applied to the [posterior predictive distribution](/posterior-predictive-distribution/) gives the shortest prediction set for a new observation.
- **Likelihood region.** With a flat prior, the HPD region is a set $\{\theta : L(\theta) \ge c\}$; the frequentist [likelihood ratio test](/likelihood-ratio-test/) inverts sets of this form with a different choice of $c$.
- **[Confidence interval](/confidence-interval/).** A rule with coverage at least $1 - \alpha$ at every $\theta$ over repeated samples; a different statement.

## References
