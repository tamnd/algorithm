---
tag: EEK1JS
kind: concept
slug: statistical-hypothesis-test
name: Statistical hypothesis test
aliases:
- significance test
- null hypothesis significance test
area: statistics-and-inference/hypothesis-testing
level: intro
summary: A rule that decides from data whether to reject a null hypothesis in favour of an alternative, with a bound alpha on the chance of rejecting a true null.
prereqs: [random-variable, sampling-distribution]
see_also: [p-value, type-i-and-type-ii-errors, statistical-power, z-test, neyman-pearson-lemma, likelihood-ratio-test, multiple-comparisons-problem, bayes-factor]
sources:
  - paper: doi:10.1098/rsta.1933.0009
    title: "J. Neyman and E. S. Pearson, On the problem of the most efficient tests of statistical hypotheses, Philosophical Transactions of the Royal Society A 231, 1933, pp. 289 to 337"
    locator: The whole paper (the null and the alternative hypothesis, the two kinds of error, the critical region of fixed size and the most powerful region)
  - url: https://psychclassics.yorku.ca/Fisher/Methods/
    title: Ronald A. Fisher, Statistical Methods for Research Workers, Oliver and Boyd, 1925, online text of the first edition
    locator: Chapter III, section 12 (the test of significance, P and the 5% convention) and Chapter V (tests of significance of means)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Chapter 8 (hypothesis testing; Section 8.3.1 on error probabilities and the power function, Section 8.3.4 on p-values)
  - paper: doi:10.1080/00031305.2016.1154108
    title: "Ronald L. Wasserstein and Nicole A. Lazar, The ASA statement on p-values: context, process, and purpose, The American Statistician 70(2), 2016, pp. 129 to 133"
    locator: The six principles on the use and interpretation of p-values and statistical significance
---

A statistical hypothesis test is a rule that looks at data and either rejects a null hypothesis $H_0$ about the distribution that produced them, or does not. The rule is fixed before the data are seen and is built so that, when $H_0$ is true, it rejects with probability at most a chosen level $\alpha$. Its other side is its [power](/statistical-power/), the probability of rejecting when an alternative $H_1$ is true. Two traditions shaped it: Fisher's significance test, which measures the evidence against $H_0$ by a [p-value](/p-value/), and the Neyman-Pearson test, which is a decision rule with controlled [type I and type II error](/type-i-and-type-ii-errors/) rates.

## In plain words

A test is a way to check a claim against data while admitting that data are noisy. You start from a default claim, such as "the coin is fair" or "the new drug works no better than the old one". You choose a summary of the data that tends to be large when the claim is false. Then you ask: if the claim were true, how surprising would a summary this large be? If it would be very surprising, you reject the claim. You fix in advance how often you are willing to reject a true claim, often 1 time in 20. A test never proves the default claim: failing to reject it can simply mean the data were too few to see the difference.

## The idea

**The ingredients.** A statistical model $\{P_\theta : \theta \in \Theta\}$ for the data $X$, a null hypothesis $H_0: \theta \in \Theta_0$ and an alternative $H_1: \theta \in \Theta_1$, with $\Theta_0$ and $\Theta_1$ disjoint. A hypothesis is simple if it names one distribution and composite otherwise. A test statistic $T(X)$ is chosen so that large values point to $H_1$, and the test rejects $H_0$ when $X$ falls in a rejection region $R$, for example $R = \{T \ge c\}$.

**The null distribution.** The [sampling distribution](/sampling-distribution/) of $T$ when $H_0$ is true is what makes a test possible. For the [z-test](/z-test/) of a normal mean with known $\sigma$ it is $N(0, 1)$ exactly; for [Student's t-test](/student-t-test/) it is the t distribution; for many tests it is known only in the limit $n \to \infty$, through the [central limit theorem](/central-limit-theorem/) or Wilks's theorem for the [likelihood ratio test](/likelihood-ratio-test/), or it is computed by permutation or simulation.

**Size, level and power.** The power function $\pi(\theta) = P_\theta(X \in R)$ gives the rejection probability at each parameter value. The size of the test is $\sup_{\theta \in \Theta_0}\pi(\theta)$, and a test has level $\alpha$ if its size is at most $\alpha$. On $\Theta_1$, $\pi(\theta)$ is the power, and $1 - \pi(\theta)$ is the type II error probability. A good test has size at most $\alpha$ and power as high as possible; the [Neyman-Pearson lemma](/neyman-pearson-lemma/) says that, for a simple null against a simple alternative, rejecting for large values of the likelihood ratio is most powerful at its size.

**The p-value.** For a statistic $T$ with observed value $t$, the p-value is $\sup_{\theta \in \Theta_0} P_\theta(T \ge t)$, the null probability of a result at least as extreme. Rejecting when $p \le \alpha$ is the same as rejecting when $t$ is in the level-$\alpha$ region, for every $\alpha$ at once.

**Fisher and Neyman-Pearson.** Fisher (1925) used only $H_0$ and a statistic. The p-value was a graded measure of evidence against $H_0$, to be weighed with other knowledge; 5% was a convenient mark, not a rule fixed in advance, and there was no explicit alternative and no type II error. Neyman and Pearson (1933) treated a test as a decision between $H_0$ and $H_1$. The level $\alpha$ is fixed before the data, the outcome is "reject" or "do not reject", the two errors are controlled as long-run frequencies, and the alternative decides which statistic to use, through power. The common practice of computing a p-value and comparing it with 0.05 mixes the two: it uses the Neyman-Pearson decision rule but reads the p-value as Fisher's evidence. Both views are frequentist: the probabilities are over repeated samples with the hypothesis held fixed, and neither gives the probability that $H_0$ is true. That probability needs a prior and Bayesian methods, such as the [Bayes factor](/bayes-factor/).

**Asymmetry.** $H_0$ and $H_1$ are not treated alike. Rejecting $H_0$ at level $\alpha$ is a statement with a controlled error rate. Not rejecting it is not evidence for $H_0$ unless the power against the relevant alternatives is high; "not significant" is not "no effect".

## Examples

**A coin.** Toss a coin 20 times and let $X$ be the number of heads, $X \sim \text{Binomial}(20, p)$. Test $H_0: p = 1/2$ against $H_1: p > 1/2$ with the region $\{X \ge 15\}$. Its size, an exact binomial sum, is $P_{1/2}(X \ge 15) = 5425/262144 = 0.0207$. Its power at $p = 0.7$ is $1 - 0.5836 = 0.4164$: a coin that lands heads 70% of the time is caught less than half the time with 20 tosses. The region $\{X \ge 14\}$ has size 0.0577, above 5%, so with this discrete statistic no region has size exactly 0.05.

**The lady tasting tea.** In Fisher's design (The Design of Experiments, 1935), a lady claims she can tell whether milk or tea was poured first. She gets 8 cups, 4 of each kind in random order, and must pick the 4 with milk first. Under $H_0$ (no ability) each of the $\binom{8}{4} = 70$ choices is equally likely, so the probability of naming all 4 correctly is $1/70 = 0.0143$. The test that rejects only for a perfect answer has size 0.0143; the randomization alone gives the null distribution.

**A filling machine.** Nine packs from a machine set to 500 g, with known $\sigma = 4$ g, have mean 502.78 g. The [z-test](/z-test/) of $H_0: \mu = 500$ gives $z = 25/12 = 2.0833$ and a two-sided p-value of 0.0372, so it rejects at 5% but not at 1%. Its power against a true mean of 503 g is only 0.614 with nine packs.

**Many tests.** If 1000 hypotheses are tested at $\alpha = 0.05$ and 900 nulls are true, about 45 true nulls are rejected. If the other 100 tests have power 0.8, about 80 false nulls are rejected, so about $45/125 = 0.36$ of the rejections are errors (expected counts). The error rate per test is controlled; the share of errors among the discoveries is not. This is the [multiple comparisons problem](/multiple-comparisons-problem/).

## Where it is used

- **Science and medicine.** Clinical trials test a treatment effect at a level fixed in the protocol, with a sample size chosen for power.
- **Quality control.** Control charts and acceptance sampling are repeated tests of "the process is in control".
- **Online experiments.** A/B tests compare conversion rates of two versions of a product.
- **Model checking.** Goodness-of-fit tests, such as chi-squared tests and normality tests, check the assumptions of a model.
- **Genomics and imaging.** Thousands to millions of simultaneous tests, where the error rate is controlled for the whole family or as a false discovery rate.

The American Statistical Association's 2016 statement (Wasserstein and Lazar) lists what a test does not give: a p-value does not measure the probability that the hypothesis is true or the size of an effect, and scientific conclusions should not rest only on whether a p-value passes a threshold.

## References
