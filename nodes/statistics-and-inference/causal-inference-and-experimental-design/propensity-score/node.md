---
tag: JNBFXX
kind: definition
slug: propensity-score
name: Propensity score
aliases:
- treatment propensity
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: The probability of receiving treatment given the covariates. Rosenbaum and Rubin showed it is a balancing score, so adjusting for it removes confounding by those covariates.
prereqs: [ignorability]
see_also: [inverse-probability-weighting, propensity-score-matching, augmented-inverse-probability-weighting, logistic-regression, rosenbaum-sensitivity-analysis, average-treatment-effect, stratified-sampling, double-machine-learning]
sources:
  - paper: doi:10.1093/biomet/70.1.41
    title: Paul R. Rosenbaum and Donald B. Rubin, The central role of the propensity score in observational studies for causal effects, Biometrika 70(1), 1983
    locator: pp. 41 to 55 (balancing scores, the propensity score as the coarsest balancing score, strong ignorability given a balancing score)
  - paper: doi:10.1080/01621459.1984.10478078
    title: Paul R. Rosenbaum and Donald B. Rubin, Reducing bias in observational studies using subclassification on the propensity score, Journal of the American Statistical Association 79(387), 1984
    locator: pp. 516 to 524 (subclassification on an estimated score and checks of covariate balance)
  - paper: doi:10.1093/biomet/87.3.706
    title: Guido W. Imbens, The role of the propensity score in estimating dose-response functions, Biometrika 87(3), 2000
    locator: pp. 706 to 710 (the generalized propensity score for treatments with several levels)
  - book: isbn:9780521885881
    title: Guido W. Imbens and Donald B. Rubin, Causal Inference for Statistics, Social, and Biomedical Sciences, Cambridge University Press, 2015
    locator: Chapter 12 (unconfounded assignment and the propensity score) and Chapter 13 (estimating the propensity score)
  - book: isbn:9780387989679
    title: Paul R. Rosenbaum, Observational Studies, second edition, Springer, 2002
    locator: Chapter 3, pp. 71 to 104 (overt bias, adjustment by the propensity score)
---

The propensity score of a unit is its probability of being treated, given its covariates: $e(x) = \Pr[T = 1 \mid X = x]$. Rosenbaum and Rubin (1983) proved two facts that make it central to observational studies. First, units with the same propensity score have the same distribution of covariates whether treated or not, so the score *balances* $X$. Second, if treatment is [ignorable](/ignorability/) given $X$, it is also ignorable given the single number $e(X)$. So a problem of adjusting for many covariates becomes a problem of adjusting for one, and [inverse probability weighting](/inverse-probability-weighting/), [propensity score matching](/propensity-score-matching/) and subclassification all rest on it. In a randomized experiment the score is known; in an observational study it must be estimated, usually by [logistic regression](/logistic-regression/).

## Definition

Let $X$ be covariates measured before a binary treatment $T$. The **propensity score** is
$$e(x) = \Pr[T = 1 \mid X = x].$$
A function $b(X)$ is a **balancing score** if $X \perp T \mid b(X)$: given $b(X)$, the law of $X$ is the same for treated and controls. The covariates $X$ themselves are the finest balancing score.

The proofs below use only the tower rule $\mathbb{E}\big[\mathbb{E}[V \mid X] \mid g(X)\big] = \mathbb{E}[V \mid g(X)]$ for a function $g$, so they hold for any $X$. A reader may take $X$ discrete, where each step is a finite sum. For a binary $T$, the statement $T \perp W \mid V$ is the same as $\Pr[T = 1 \mid W, V] = \Pr[T = 1 \mid V]$.

**Theorem 1 (the propensity score is a balancing score).** $T \perp X \mid e(X)$.

*Proof.* Since $e(X)$ is a function of $X$, $\Pr[T = 1 \mid X, e(X)] = \Pr[T = 1 \mid X] = e(X)$. Also $\Pr[T = 1 \mid e(X)] = \mathbb{E}\big[\mathbb{E}[T \mid X] \mid e(X)\big] = \mathbb{E}[e(X) \mid e(X)] = e(X)$. The two are equal, so $T \perp X \mid e(X)$. $\square$

**Theorem 2 (which scores balance).** A function $b(X)$ is a balancing score if and only if $e(X) = f(b(X))$ for some function $f$. So $e$ is the coarsest balancing score, and every balancing score is at least as fine.

*Proof.* If $e(X) = f(b(X))$, then $\Pr[T = 1 \mid b(X)] = \mathbb{E}[e(X) \mid b(X)] = f(b(X)) = e(X) = \Pr[T = 1 \mid X, b(X)]$, so $T \perp X \mid b(X)$. For the converse, suppose $b$ is balancing, and let $x_1$ and $x_2$ be values of positive probability with $b(x_1) = b(x_2) = \beta$. Balancing gives $\Pr[T = 1 \mid X = x, b(X) = \beta] = \Pr[T = 1 \mid b(X) = \beta]$ for $x = x_1$ and $x = x_2$, and the left side is $e(x)$. So $e(x_1) = e(x_2)$: $e$ is constant on each level set of $b$, which is to say $e = f \circ b$. (For a general $X$ the same argument holds almost surely.) $\square$

**Theorem 3 (ignorability given the score).** If $(Y(0), Y(1)) \perp T \mid X$ and $0 < e(X) < 1$, then $(Y(0), Y(1)) \perp T \mid e(X)$ and $0 < e(X) < 1$.

*Proof.* The overlap part is the same statement. For independence, write $Y^* = (Y(0), Y(1))$. Since $e(X)$ is a function of $X$, the tower rule gives
$$\Pr[T = 1 \mid Y^*, e(X)] = \mathbb{E}\big[\Pr[T = 1 \mid Y^*, X] \mid Y^*, e(X)\big].$$
By ignorability given $X$, $\Pr[T = 1 \mid Y^*, X] = \Pr[T = 1 \mid X] = e(X)$, so the right side is $\mathbb{E}[e(X) \mid Y^*, e(X)] = e(X)$. By the proof of Theorem 1, $\Pr[T = 1 \mid e(X)] = e(X)$ too. So $\Pr[T = 1 \mid Y^*, e(X)]$ does not depend on $Y^*$, and $Y^* \perp T \mid e(X)$. $\square$

Rosenbaum and Rubin (1983) prove the same for every balancing score $b(X)$, with $\Pr[T = 1 \mid b(X)] = e(X)$ in the last step, which holds by Theorem 2. The proof works one potential outcome at a time, so weak unconfoundedness given $X$ gives weak unconfoundedness given $e(X)$.

**Consequence.** Under the conditions of Theorem 3, the identification result of the [ignorability](/ignorability/) page applies with $e(X)$ in place of $X$:
$$\mathbb{E}[Y(t)] = \mathbb{E}\big[\mathbb{E}[Y \mid T = t, e(X)]\big], \qquad t \in \{0, 1\},$$
and $\mathbb{E}[Y(1) - Y(0) \mid e(X) = s] = \mathbb{E}[Y \mid T = 1, e(X) = s] - \mathbb{E}[Y \mid T = 0, e(X) = s]$. So treated and control units with the same score can be compared directly, as if they came from a randomized experiment with probability $s$.

**What is proved and what is not.** Theorems 1 to 3 are exact properties of the true score in the population. They say nothing about covariates outside $X$: the score balances only what it was built from. With an *estimated* score, balance in a sample is not guaranteed and is checked by comparing covariate means and distributions within strata or matched sets. Such checks measure balance; they do not prove it, and they cannot test ignorability.

## Examples and non-examples

**Example: a score that balances.** Let $X$ take four values $a, b, c, d$, each with probability $1/4$, with $e(a) = 1/5$, $e(b) = e(c) = 1/2$ and $e(d) = 4/5$. Then $\Pr[T = 1] = \frac14(\frac15 + \frac12 + \frac12 + \frac45) = \frac12$. Among units with $e(X) = 1/2$, the treated are $b$ or $c$ with probability $\frac{1/8}{1/8 + 1/8} = \frac12$ each, and the controls also $\frac12$ each. Given the score, $X$ has the same law in both groups, as Theorem 1 says, though $b$ and $c$ may differ in every other way.

**Non-example: a coarser score.** Let $b(X) = 1$ if $X \in \{c, d\}$ and $0$ otherwise. Among units with $b(X) = 1$, a treated unit has $X = d$ with probability $\frac{\frac14 \cdot \frac45}{\frac14 \cdot \frac12 + \frac14 \cdot \frac45} = \frac{8}{13}$, but a control has $X = d$ with probability $\frac{\frac14 \cdot \frac15}{\frac14 \cdot \frac12 + \frac14 \cdot \frac15} = \frac{2}{7}$. The groups differ, so $b$ is not balancing. Theorem 2 predicts this: $e(c) \ne e(d)$, so $e$ is not a function of $b$.

**Example: a randomized experiment.** In a Bernoulli trial with probability $p$, $e(x) = p$ for every $x$, a constant, and Theorem 1 says that $X \perp T$ with no conditioning. In a stratified experiment, $e$ is the known probability of each stratum.

**Example: treatment by severity.** In the example of the [ignorability](/ignorability/) page, $e(\text{mild}) = 1/4$ and $e(\text{severe}) = 3/4$. The score takes two values and is a one-to-one function of severity, so stratifying on it is the same as stratifying on severity, and gives the effect $0.25$.

**Non-example: balance on an unmeasured covariate.** If a variable $U$ affects both treatment and outcome but is not in $X$, then $e(X)$ need not balance $U$, and Theorem 3 does not apply, because its premise fails. A score estimated with high accuracy from $X$ does not remove confounding by $U$. [Rosenbaum sensitivity analysis](/rosenbaum-sensitivity-analysis/) models exactly such a $U$.

**Non-example: a post-treatment covariate.** If $X$ contains a variable changed by the treatment, $e(X)$ is still defined, but ignorability given $X$ fails, as the [ignorability](/ignorability/) page shows, so Theorem 3 gives nothing.

## Related definitions

- [Ignorability](/ignorability/): the assumption that Theorem 3 transfers from $X$ to $e(X)$.
- [Inverse probability weighting](/inverse-probability-weighting/): weights each unit by $1/e(X)$ or $1/(1 - e(X))$. Its page proves unbiasedness with the true score, and shows that the score estimated within strata gives the stratified estimate.
- [Propensity score matching](/propensity-score-matching/): pairs treated units with controls of nearly equal score, to estimate the effect on the treated.
- [Augmented inverse probability weighting](/augmented-inverse-probability-weighting/): combines a model of $e$ with a model of the outcome, and is consistent if either is right.
- **Generalized propensity score.** For a treatment with several levels, Imbens (2000) uses $r(t, x) = \Pr[T = t \mid X = x]$, and weak unconfoundedness given $X$ gives weak unconfoundedness of $Y(t)$ given $r(t, X)$, for each $t$.
- [Stratified sampling](/stratified-sampling/): subclassification on the score, with strata of units of similar $e(X)$, is the observational analogue of a stratified design.

## References
