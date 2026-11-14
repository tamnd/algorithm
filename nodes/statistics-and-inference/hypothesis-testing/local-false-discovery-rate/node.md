---
tag: TK7BPM
kind: definition
slug: local-false-discovery-rate
name: Local false discovery rate
aliases:
- local FDR
- lfdr
area: statistics-and-inference/hypothesis-testing
level: advanced
summary: Efron's posterior probability that a hypothesis is null given its z-value, from a two-group mixture of null and non-null densities estimated from all the tests.
prereqs: [false-discovery-rate, bayes-theorem]
see_also: [empirical-bayes, storey-q-value, benjamini-hochberg-procedure, kernel-density-estimation, gaussian-mixture-model, expectation-maximization, multiple-comparisons-problem]
sources:
  - paper: doi:10.1198/016214501753382129
    title: Bradley Efron, Robert Tibshirani, John D. Storey and Virginia Tusher, Empirical Bayes analysis of a microarray experiment, Journal of the American Statistical Association 96(456) (2001), pages 1151 to 1160
    locator: the two-groups mixture f = p_0 f_0 + p_1 f_1 and the posterior probability p_0 f_0(z) / f(z) that a gene is not differentially expressed
  - paper: doi:10.1198/016214504000000089
    title: Bradley Efron, Large-scale simultaneous hypothesis testing, the choice of a null hypothesis, Journal of the American Statistical Association 99(465) (2004), pages 96 to 104
    locator: the empirical null, a normal density fitted to the center of the z-values, and its effect on the local fdr
  - book: isbn:9780521192491
    title: Bradley Efron, Large-Scale Inference, Empirical Bayes Methods for Estimation, Testing, and Prediction, Cambridge University Press, 2010
    locator: Chapter 2, Section 2.2 (the two-groups model and the Bayesian Fdr), Chapter 5 (local false discovery rates) and Chapter 6 (theoretical, permutation and empirical null distributions)
---

The local false discovery rate is the probability that a hypothesis is null given the exact value of its test statistic. It comes from the two-groups model of Efron and his coauthors (2001): each of many cases is null with probability $\pi_0$ and non-null otherwise, and its z-value has density $f_0$ in the first case and $f_1$ in the second. Then, by [Bayes' theorem](/bayes-theorem/), the local fdr at $z$ is $\text{fdr}(z) = \pi_0f_0(z)/f(z)$, where $f = \pi_0f_0 + (1 - \pi_0)f_1$ is the density of all the z-values. Unlike the [false discovery rate](/false-discovery-rate/), which is an average over all rejected cases, the local fdr is a statement about one case. The tail-area Fdr is the average of the local fdr over a tail. With thousands of cases, $f$ can be estimated from the data, which makes the local fdr an [empirical Bayes](/empirical-bayes/) quantity.

## Definition

**Two-groups model.** There are $N$ cases, for example genes, each with a z-value $z_i$. Each case is null with prior probability $\pi_0$ and non-null with probability $\pi_1 = 1 - \pi_0$. A null z-value has density $f_0$, often the theoretical null $N(0, 1)$, and a non-null z-value has density $f_1$. So every z-value has the mixture density and distribution function
$$f(z) = \pi_0f_0(z) + \pi_1f_1(z), \qquad F(z) = \pi_0F_0(z) + \pi_1F_1(z).$$

**Local false discovery rate.** For $z$ with $f(z) > 0$,
$$\text{fdr}(z) = \frac{\pi_0f_0(z)}{f(z)} = P(\text{case is null} \mid z_i = z).$$
The second equality is Bayes' theorem for a density: the joint density of "null" and $z$ is $\pi_0f_0(z)$, and the marginal density of $z$ is $f(z)$. So $\text{fdr}(z) \in [0, 1]$, and $1 - \text{fdr}(z) = \pi_1f_1(z)/f(z)$ is the posterior probability of a real effect.

**Tail-area Fdr.** For a left tail, $\text{Fdr}(z) = \pi_0F_0(z)/F(z) = P(\text{null} \mid z_i \le z)$, and for a right tail the same with survival functions, $\pi_0(1 - F_0(z))/(1 - F(z))$.

**Proposition (the Fdr averages the fdr).** For every $z$ with $F(z) > 0$, $\text{Fdr}(z) = E[\text{fdr}(Z) \mid Z \le z]$, where $Z$ has density $f$. The same holds for right tails.

*Proof.* $E[\text{fdr}(Z)\mathbf 1\{Z \le z\}] = \int_{-\infty}^z \frac{\pi_0f_0(t)}{f(t)}f(t)\,dt = \pi_0F_0(z)$. Dividing by $P(Z \le z) = F(z)$ gives the claim. $\square$

If $f_1/f_0$ increases in $z$, so that large z-values favour the non-null group, then $\text{fdr}$ decreases in $z$, and for a right tail $\text{Fdr}(z) = E[\text{fdr}(Z) \mid Z \ge z] \le \text{fdr}(z)$: the cases on the boundary of a rejection region are more likely to be null than the average rejected case.

**Reporting rule.** Efron suggests reporting the cases with $\text{fdr}(z_i) \le 0.2$ as interesting. Since $\text{fdr}(z) \le 0.2$ means $0.8\pi_0f_0(z) \le 0.2\pi_1f_1(z)$, the rule asks for a Bayes factor $f_1(z)/f_0(z) \ge 4\pi_0/\pi_1$. With $\pi_0 = 0.9$ this is $f_1/f_0 \ge 36$.

## Examples and non-examples

**A normal example by hand.** Let $\pi_0 = 0.9$, $f_0 = N(0, 1)$ and $f_1 = N(2.5, 1)$. Then $f_1(z)/f_0(z) = e^{2.5z - 3.125}$ and $\text{fdr}(z) = 1/(1 + (\pi_1/\pi_0)e^{2.5z - 3.125})$, with $\pi_1/\pi_0 = 1/9$. The right-tail Fdr uses the normal survival function $\bar\Phi$: $\text{Fdr}(z) = 0.9\bar\Phi(z)/(0.9\bar\Phi(z) + 0.1\bar\Phi(z - 2.5))$.

| $z$ | $f_1(z)/f_0(z)$ | $\text{fdr}(z)$ | right-tail $\text{Fdr}(z)$ |
|---|---|---|---|
| 1 | 0.535 | 0.9439 | 0.6048 |
| 2 | 6.521 | 0.5799 | 0.2285 |
| 2.5 | 22.76 | 0.2834 | 0.1005 |
| 3 | 79.44 | 0.1018 | 0.0379 |
| 4 | 967.8 | 0.0092 | 0.0042 |

The rule $\text{fdr} \le 0.2$ holds for $z \ge (\ln 36 + 3.125)/2.5 = 2.683$, and the region $z \ge 2.683$ has $\text{Fdr} = 0.0713$. A tail-area rule at $\text{Fdr} \le 0.1$ starts at about $z = 2.503$, where the local fdr is 0.28: the last case let in by the tail rule is null with probability 0.28, although the rejected cases are null with probability 0.1 on average. In this model the non-null cases above 2.683 are 42.7% of all non-null cases.

**Estimated from data.** In practice $f$ is estimated from all $N$ z-values, by a smooth fit to their histogram (Efron uses a Poisson regression on the bin counts, Lindsey's method) or by [kernel density estimation](/kernel-density-estimation/). $f_0$ is taken as $N(0, 1)$ or, when the center of the histogram is wider or shifted, as the empirical null of Efron (2004), a normal density fitted to the central z-values. $\pi_0$ is estimated from the center, under the assumption that almost all cases near 0 are null. The estimated $\widehat{\text{fdr}}(z) = \hat\pi_0\hat f_0(z)/\hat f(z)$ is the empirical Bayes estimate, and its accuracy depends on $N$ being in the hundreds or thousands.

**Link to Benjamini-Hochberg.** With $\pi_0 = 1$ and the theoretical null, the natural estimate of the right-tail Fdr at $z$ is $N\bar\Phi(z)/\#\{i : z_i \ge z\}$. Rejecting where it is at most $q$ is the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/) at level $q$ on the one-sided p-values. Estimating $\pi_0$ as well gives [Storey's method](/storey-q-value/).

**Non-example: a p-value.** The p-value $\bar\Phi(z)$ uses only $f_0$ and does not change with $\pi_0$ or $f_1$. At $z = 3$ in the example it is 0.00135, while the local fdr is 0.10. A small p-value does not mean a small probability that the null is true.

**Non-example: the FDR of a procedure.** The FDR is the expected false discovery proportion of a rejection rule, an average over repetitions of the experiment and over the rejected cases. The local fdr is a posterior probability for one case, under a model with a prior. They agree only in the sense of the proposition: the Bayesian Fdr of a tail is the average local fdr in it.

**Identifiability.** From $f$ alone, $\pi_0$ and $f_1$ are not identified: part of $f_0$ can always be moved into $f_1$. The usual fix is the zero assumption that $f_1$ is close to 0 near $z = 0$. Then $\hat\pi_0$ is an upper bound for $\pi_0$, and the estimated fdr is conservative.

## Related definitions

- **False discovery rate.** The frequentist rate $E[V/\max(R, 1)]$ of a procedure. See [false discovery rate](/false-discovery-rate/).
- **Tail-area Fdr and the positive FDR.** Under the two-groups model with independent cases, the positive FDR of the region $\{z_i \ge z\}$ equals the right-tail Fdr at $z$ (Storey 2003). The [q-value](/storey-q-value/) of a case is the smallest such Fdr over the regions that contain it.
- **Posterior probability in a mixture.** The local fdr is the responsibility of the null component in a two-component mixture, as in a [Gaussian mixture model](/gaussian-mixture-model/) fitted by [EM](/expectation-maximization/), with the difference that the null component is fixed or fitted only to the center.
- **Empirical Bayes.** Estimating the prior quantities $\pi_0$ and $f$ from many parallel cases is the setting of [empirical Bayes](/empirical-bayes/) inference.
- **Bayes factor.** $f_1(z)/f_0(z)$ is the Bayes factor of the non-null group against the null group at $z$, and $\text{fdr}(z) = 1/(1 + (\pi_1/\pi_0)f_1(z)/f_0(z))$.

## References
