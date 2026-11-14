---
tag: YNRN9V
kind: definition
slug: type-i-and-type-ii-errors
name: Type I and type II errors
aliases:
- false rejection and false acceptance
- alpha and beta errors
area: statistics-and-inference/hypothesis-testing
level: intro
summary: A type I error rejects a true null hypothesis and a type II error keeps a false one. The size of a test bounds the first; its power is one minus the second.
prereqs: [statistical-hypothesis-test]
see_also: [statistical-power, p-value, sample-size-determination, neyman-pearson-lemma, family-wise-error-rate, false-discovery-rate, multiple-comparisons-problem, binomial-test]
sources:
  - paper: doi:10.1098/rsta.1933.0009
    title: "J. Neyman and E. S. Pearson, On the problem of the most efficient tests of statistical hypotheses, Philosophical Transactions of the Royal Society A 231, 1933, pp. 289 to 337"
    locator: The introduction (the two sources of error, rejecting a true hypothesis and accepting a false one, and the control of the first while minimizing the second)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 8.3.1 (error probabilities and the power function, the definitions of type I and type II error, size and level)
---

A type I error is the rejection of a null hypothesis $H_0$ that is true; a type II error is the failure to reject $H_0$ when it is false. The two names come from Neyman and Pearson's 1933 theory of [statistical hypothesis tests](/statistical-hypothesis-test/), in which a test is designed to keep the probability of the first below a level $\alpha$ and, subject to that, to make the probability of the second as small as possible. For a fixed amount of data the two error probabilities pull against each other: a test that rejects less often makes fewer type I errors and more type II errors.

## Definition

Let $X$ have a distribution $P_\theta$ with $\theta \in \Theta$, let $H_0: \theta \in \Theta_0$ and $H_1: \theta \in \Theta_1$ with $\Theta_0 \cap \Theta_1 = \emptyset$, and let a test reject $H_0$ exactly when $X$ falls in a rejection region $R$. Its power function is $\pi(\theta) = P_\theta(X \in R)$.

| | $H_0$ true ($\theta \in \Theta_0$) | $H_1$ true ($\theta \in \Theta_1$) |
|---|---|---|
| reject $H_0$ | type I error, probability $\pi(\theta)$ | correct, probability $\pi(\theta)$ (the power) |
| do not reject $H_0$ | correct, probability $1 - \pi(\theta)$ | type II error, probability $\beta(\theta) = 1 - \pi(\theta)$ |

- The **type I error probability** at $\theta \in \Theta_0$ is $\pi(\theta)$.
- The **size** of the test is $\sup_{\theta \in \Theta_0}\pi(\theta)$, the largest type I error probability. The test has **level** $\alpha$ when its size is at most $\alpha$.
- The **type II error probability** at $\theta \in \Theta_1$ is $\beta(\theta) = 1 - \pi(\theta)$. It is a function of the alternative, not one number: it is close to $1 - \alpha$ for alternatives near $\Theta_0$ and goes to 0 for alternatives far from it.

The probabilities are frequentist: they are over repeated data with $\theta$ held fixed. For a randomized test $\phi(X) \in [0, 1]$, the rejection probability is $\pi(\theta) = E_\theta[\phi(X)]$ and the same definitions apply.

## Examples and non-examples

**A coin, and the trade-off.** $X \sim \text{Binomial}(20, p)$, $H_0: p = 1/2$ against $H_1: p > 1/2$, rejecting for $X \ge k$. The exact binomial sums are:

| $k$ | type I error $P_{1/2}(X \ge k)$ | type II error at $p = 0.6$ | type II error at $p = 0.7$ |
|---|---|---|---|
| 13 | 0.1316 | 0.5841 | 0.2277 |
| 14 | 0.0577 | 0.7500 | 0.3920 |
| 15 | 0.0207 | 0.8744 | 0.5836 |
| 16 | 0.0059 | 0.9490 | 0.7625 |
| 17 | 0.0013 | 0.9840 | 0.8929 |

Raising $k$ lowers the type I error and raises the type II error. The smallest $k$ with level 0.05 is 15, whose size is 0.0207, and against $p = 0.6$ it misses 87% of the time. Only more data lowers both at once.

**A medical screening analogy.** With $H_0$ "the patient is healthy", a type I error is a false positive and a type II error a false negative; $1 - \alpha$ is the specificity and the power is the sensitivity.

**Non-example: the p-value.** A p-value of 0.03 is not "a 3% chance of a type I error". The type I error probability is a property of the rule, fixed before the data: for the rule "reject if $p \le 0.05$" it is 0.05 (or less), whatever $p$ is observed. The [p-value](/p-value/) is a statistic computed from the data.

**Non-example: the probability that a rejection is wrong.** $\alpha$ is $P(\text{reject} \mid H_0 \text{ true})$, not $P(H_0 \text{ true} \mid \text{reject})$. Among 1000 tests at $\alpha = 0.05$ of which 900 nulls are true and 100 have power 0.8, the expected counts are 45 false rejections and 80 true ones, so 36% of the rejections are type I errors. The share depends on how many nulls are true, which the test does not control; the [false discovery rate](/false-discovery-rate/) is the error rate built for this question.

**Non-example: "accepting" $H_0$.** Not rejecting is not a proof of $H_0$. With power 0.13 at $p = 0.6$ (the $k = 15$ test above), a coin with $p = 0.6$ gives a non-significant result 87% of the time.

## Related definitions

- **[Power](/statistical-power/)** is $1 - \beta(\theta)$ on the alternative; the power function $\pi(\theta)$ covers both hypotheses.
- **Unbiased test.** A test with $\pi(\theta) \le \alpha$ on $\Theta_0$ and $\pi(\theta) \ge \alpha$ on $\Theta_1$: the probability of rejecting is never smaller under a false null than under a true one.
- **Most powerful test.** Among level-$\alpha$ tests, one with the smallest type II error at a given alternative; the [Neyman-Pearson lemma](/neyman-pearson-lemma/) finds it for simple hypotheses, and a uniformly most powerful test minimizes it at every alternative at once.
- **[Family-wise error rate](/family-wise-error-rate/).** For many tests, the probability of at least one type I error.
- **[False discovery rate](/false-discovery-rate/).** The expected share of type I errors among the rejections.
- **Directional error.** Rejecting a two-sided null and then concluding the wrong sign of the effect; some authors call it a type III error, a name that is also used for other mistakes and has no single meaning.

## References
