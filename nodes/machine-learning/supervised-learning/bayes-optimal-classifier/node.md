---
tag: 644CE2
kind: concept
slug: bayes-optimal-classifier
name: Bayes optimal classifier
aliases:
- Bayes classifier
- Bayes decision rule
- Bayes optimal decision rule
area: machine-learning/supervised-learning
level: core
summary: "The rule that predicts the label with the largest posterior P(y | x). It has the smallest possible 0-1 risk, the Bayes risk; a loss matrix gives the cost-sensitive version."
prereqs: [classification, loss-function, conditional-expectation]
see_also: [cover-hart-theorem, naive-bayes-classifier, quadratic-discriminant-analysis, generative-vs-discriminative-models, bayes-theorem, k-nearest-neighbors, logistic-regression, bayesian-inference]
sources:
  - book: isbn:9780387946184
    title: Luc Devroye, László Györfi and Gábor Lugosi, A Probabilistic Theory of Pattern Recognition, Springer, 1996
    locator: Chapter 2 (the Bayes decision, its optimality, the Bayes error and the excess risk formula)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 2.4 (statistical decision theory, the Bayes classifier and the Bayes rate)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 1.5 (decision theory, minimizing the misclassification rate, the loss matrix and the reject option)
  - book: isbn:9780471056690
    title: Richard O. Duda, Peter E. Hart and David G. Stork, Pattern Classification, second edition, Wiley, 2001
    locator: Chapter 2 (Bayesian decision theory, minimum error rate classification and the conditional risk)
  - book: isbn:9780070428072
    title: Tom M. Mitchell, Machine Learning, McGraw-Hill, 1997
    locator: Section 6.7 (the Bayes optimal classifier as a posterior weighted vote over hypotheses)
  - paper: doi:10.1109/TIT.1970.1054406
    title: C. K. Chow, On optimum recognition error and reject tradeoff, IEEE Transactions on Information Theory 16(1), 1970
    locator: the optimal reject rule
  - paper: doi:10.1198/016214505000000907
    title: Peter L. Bartlett, Michael I. Jordan and Jon D. McAuliffe, Convexity, classification, and risk bounds, Journal of the American Statistical Association 101(473), 2006
    locator: classification calibrated surrogate losses and the bound of the excess 0-1 risk
---

The Bayes optimal classifier is the rule $h^\ast(x) = \arg\max_y \Pr[Y = y \mid X = x]$ that predicts, for each input, the label with the largest posterior probability under the true distribution of the data. Among all [classifiers](/classification/) it has the smallest expected 0-1 loss, and that smallest value is the Bayes risk $R^\ast$. With a loss matrix in place of the 0-1 loss, the optimal rule picks the label with the smallest posterior expected cost. It is a benchmark, not an algorithm: it needs the distribution, which a learner does not have.

## In plain words

Suppose you knew exactly how likely each answer is for every possible input. Then the best you can do on each input is to choose the answer that is most likely. No other rule can make fewer mistakes on average, because on every single input it makes at most the same number of expected mistakes as this one. The mistakes that remain come from inputs that are truly ambiguous, where several answers are possible. Their rate is the smallest error that any method can reach.

When some mistakes cost more than others, for example missing a disease versus a false alarm, the best rule chooses the answer with the smallest expected cost instead of the most likely answer.

## The idea

**Setting.** The pair $(X, Y)$ has a joint distribution $D$ on $\mathcal{X} \times \{1, \ldots, M\}$, where $M$ is the number of classes. The posterior is $\eta_y(x) = \Pr[Y = y \mid X = x]$. A classifier is a measurable map $h : \mathcal{X} \to \{1, \ldots, M\}$, and its risk under the 0-1 loss is $R(h) = \Pr[h(X) \ne Y]$. In learning theory $D$ is unknown and the training data are drawn i.i.d. from it; the Bayes classifier is the rule that a learner would use if it knew $D$.

**Definition.** A Bayes classifier is any $h^\ast$ with $h^\ast(x) \in \arg\max_y \eta_y(x)$ for each $x$. The Bayes risk is
$$ R^\ast = R(h^\ast) = \mathbb{E}\big[1 - \max_y \eta_y(X)\big]. $$
By [Bayes' theorem](/bayes-theorem/), $\eta_y(x) = \pi_y p(x \mid y) / \sum_{c} \pi_c p(x \mid c)$, where $\pi_y$ is the prior of class $y$ and $p(x \mid y)$ the class conditional density. The denominator is the same for each $y$, so $h^\ast(x) \in \arg\max_y \pi_y p(x \mid y)$.

**Theorem (optimality).** For every classifier $h$, $R(h) \ge R^\ast$.

*Proof.* Fix $x$. Given $X = x$, the label $Y$ has the law $\eta(x)$, and $h(x)$ is a fixed label. So the conditional risk is $\Pr[h(X) \ne Y \mid X = x] = 1 - \eta_{h(x)}(x)$. Since $\eta_{h(x)}(x) \le \max_y \eta_y(x)$, this is at least $1 - \max_y \eta_y(x)$, which is the conditional risk of $h^\ast$. Take the expectation over $X$ ([law of total expectation](/conditional-expectation/)): $R(h) = \mathbb{E}[1 - \eta_{h(X)}(X)] \ge \mathbb{E}[1 - \max_y \eta_y(X)] = R^\ast$. $\square$

The proof shows more: $h^\ast$ is optimal at each point, not only on average, and a rule $h$ is optimal if and only if $\eta_{h(x)}(x) = \max_y \eta_y(x)$ for almost every $x$. When two labels tie for the largest posterior, either choice is optimal, so the Bayes classifier is not unique, but the Bayes risk is.

**The excess risk for two classes.** Let the labels be $\{0, 1\}$ and $\eta(x) = \Pr[Y = 1 \mid X = x]$, so $h^\ast(x) = 1$ when $\eta(x) > 1/2$. For any $h$,
$$ R(h) - R^\ast = \mathbb{E}\big[\,|2\eta(X) - 1| \cdot \mathbf{1}\{h(X) \ne h^\ast(X)\}\big]. $$
*Proof.* Where $h(x) = h^\ast(x)$ the two conditional risks are equal. Where they differ, one rule predicts 1 with conditional risk $1 - \eta(x)$ and the other predicts 0 with conditional risk $\eta(x)$, and the difference of the larger and the smaller is $|2\eta(x) - 1|$. Take the expectation. $\square$ So a mistake against $h^\ast$ costs little where $\eta(x)$ is near $1/2$. A plug-in rule $\hat h(x) = \mathbf{1}\{\hat\eta(x) > 1/2\}$ therefore has $R(\hat h) - R^\ast \le 2\,\mathbb{E}|\hat\eta(X) - \eta(X)|$, since $\hat h$ and $h^\ast$ can differ at $x$ only if $|\eta(x) - 1/2| \le |\hat\eta(x) - \eta(x)|$.

**The cost-sensitive version.** Let $L(y, \hat y) \ge 0$ be the cost of predicting $\hat y$ when the truth is $y$, given as an $M \times M$ loss matrix. The conditional risk of predicting $\hat y$ at $x$ is $\sum_y L(y, \hat y)\eta_y(x)$, and the same pointwise argument proves that
$$ h_L^\ast(x) \in \arg\min_{\hat y} \sum_{y=1}^M L(y, \hat y)\, \eta_y(x) $$
minimizes $\mathbb{E}[L(Y, h(X))]$ over all classifiers. The 0-1 loss, $L(y, \hat y) = \mathbf{1}\{y \ne \hat y\}$, gives back $\arg\max_y \eta_y(x)$. For two classes with zero cost on the diagonal, a false positive cost $c_{01} = L(0, 1)$ and a false negative cost $c_{10} = L(1, 0)$, the rule is: predict 1 if and only if $c_{10}\eta(x) > c_{01}(1 - \eta(x))$, that is, if $\eta(x) > c_{01}/(c_{01} + c_{10})$. So costs move the threshold on the posterior and keep its form.

**The reject option.** If a rejection costs $c \in (0, 1/2)$ and an error costs 1, the optimal rule predicts $\arg\max_y \eta_y(x)$ when $\max_y \eta_y(x) \ge 1 - c$ and rejects otherwise (Chow 1970). This is the cost-sensitive rule with one more action.

**Two meanings of the name.** This page uses the name for the decision theoretic rule $\arg\max_y \Pr[Y = y \mid X = x]$ under the true distribution. Mitchell (1997, Section 6.7) uses "Bayes optimal classifier" for a different object: given a hypothesis space $H$, a prior on $H$ and training data $S$, it predicts
$$ \arg\max_{y} \sum_{h \in H} \Pr[y \mid x, h]\, \Pr[h \mid S], $$
a vote of all hypotheses weighted by their posterior. That rule is optimal on average over the prior, for the given $H$ and prior; it is [Bayesian](/bayesian-inference/) model averaging. The two agree when the prior puts all its mass on the true distribution. Mitchell's example: three hypotheses with posteriors 0.4, 0.3 and 0.3, where the first predicts $+$ and the other two predict $-$. The single most probable hypothesis predicts $+$, but the weighted vote is 0.4 for $+$ and 0.6 for $-$, so the posterior averaging rule predicts $-$.

## Examples

**A discrete distribution.** Let $\mathcal{X} = \{a, b, c\}$ with labels $\{0, 1\}$ and this joint distribution:

| $x$ | $\Pr[x, Y = 0]$ | $\Pr[x, Y = 1]$ | $\eta(x)$ | $h^\ast(x)$ | conditional error times $\Pr[x]$ |
| --- | --- | --- | --- | --- | --- |
| $a$ | 3/10 | 1/10 | 1/4 | 0 | 1/10 |
| $b$ | 3/20 | 3/20 | 1/2 | 0 or 1 | 3/20 |
| $c$ | 1/20 | 1/4 | 5/6 | 1 | 1/20 |

So $R^\ast = 1/10 + 3/20 + 1/20 = 3/10$. No rule on this distribution has error below $3/10$, and the point $b$ alone contributes half of it.

**The same distribution with costs.** Let a false negative cost 4 and a false positive cost 1, so $L(1, 0) = 4$ and $L(0, 1) = 1$. The threshold on $\eta$ is $1/(1 + 4) = 1/5$. The expected costs of the two actions are $(2/5, 3/10)$ at $a$, $(3/5, 3/20)$ at $b$ and $(1, 1/20)$ at $c$, for predicting 0 and 1. The rule predicts 1 everywhere, with expected cost $3/10 + 3/20 + 1/20 = 1/2$. The 0-1 Bayes rule with $b \mapsto 1$ has expected cost $2/5 + 3/20 + 1/20 = 3/5$ under the same loss. The cost-sensitive rule has the larger error rate, $1/2$ against $3/10$, and the smaller cost.

**Two Gaussians.** Let $Y$ be 0 or 1 with probability $1/2$ each, $X \mid Y = 0 \sim N(0, 1)$ and $X \mid Y = 1 \sim N(2, 1)$. The log ratio of the densities is $2x - 2$, so $h^\ast(x) = \mathbf{1}\{x > 1\}$ and $R^\ast = \Phi(-1) \approx 0.15866$, where $\Phi$ is the standard normal distribution function. With the costs above, the rule predicts 1 when $2x - 2 > -\ln 4$, that is, when $x > 1 - \ln 2 \approx 0.3069$. Its error rate is about 0.2123 and its expected cost about 0.2802, against an expected cost of about 0.3966 for the threshold 1. With unequal variances the log ratio is quadratic in $x$, and the Bayes rule becomes [quadratic discriminant analysis](/quadratic-discriminant-analysis/) with the true parameters.

**A non-example.** The rule that predicts the label of the most probable hypothesis in a finite $H$ (the MAP hypothesis) is not the Bayes optimal classifier in either sense: Mitchell's example above shows that it can disagree with the posterior vote, and it can be worse than $h^\ast$ when no hypothesis in $H$ equals $h^\ast$.

## Where it is used

- **The target of plug-in methods.** [Naive Bayes](/naive-bayes-classifier/), [quadratic discriminant analysis](/quadratic-discriminant-analysis/) and linear discriminant analysis estimate $\pi_y$ and $p(x \mid y)$, and [logistic regression](/logistic-regression/) estimates $\eta$ directly; each then applies the Bayes rule to its estimate. See [generative versus discriminative models](/generative-vs-discriminative-models/).
- **Consistency.** A learning rule is consistent if its risk tends to $R^\ast$ as $n \to \infty$. The [k-nearest neighbors](/k-nearest-neighbors/) rule with $k \to \infty$ and $k/n \to 0$ is consistent for every distribution. The [Cover-Hart theorem](/cover-hart-theorem/) compares the 1-NN error with $R^\ast$.
- **Surrogate losses.** Training minimizes a convex loss such as the logistic or the hinge loss, not the 0-1 loss. Bartlett, Jordan and McAuliffe (2006) characterize the classification calibrated losses, whose minimizers have the sign of $2\eta(x) - 1$, and bound the excess 0-1 risk by the excess surrogate risk.
- **Simulation studies.** When the data come from a known model, $R^\ast$ is computable, as in the examples above, and shows how far a method is from the best possible.
- **Decisions with costs.** Medical screening, fraud detection and spam filtering use the cost-sensitive rule, with the threshold $c_{01}/(c_{01} + c_{10})$ on a calibrated estimate of $\eta$.

## References
