---
tag: 68FBV9
kind: definition
slug: e-variable
name: E-variable
aliases:
- betting score
area: statistics-and-inference/hypothesis-testing
level: research
summary: A nonnegative statistic with expected value at most one under the null. By Markov's inequality, rejecting when it exceeds 1 / alpha gives a level-alpha test that survives optional continuation.
prereqs: [p-value, statistical-hypothesis-test, type-i-and-type-ii-errors, markov-inequality]
see_also: [test-martingale, ville-inequality, confidence-sequence, bayes-factor, likelihood-ratio-test, neyman-pearson-lemma, fisher-combined-probability-test, kullback-leibler-divergence]
sources:
  - paper: doi:10.1214/20-AOS2020
    title: Vladimir Vovk and Ruodu Wang, E-values, calibration, combination and applications, Annals of Statistics 49(3) (2021), pages 1736 to 1754
    locator: the definition of e-variables and e-values, calibrators between p-values and e-values, and the merging of e-values by products and averages
  - paper: doi:10.1111/rssa.12647
    title: Glenn Shafer, Testing by betting, a strategy for statistical and scientific communication, Journal of the Royal Statistical Society, Series A 184(2) (2021), pages 407 to 431
    locator: the betting score as the factor by which a bet multiplies the money it risks
  - paper: doi:10.1093/jrsssb/qkae011
    title: Peter Grünwald, Rianne de Heide and Wouter Koolen, Safe testing, Journal of the Royal Statistical Society, Series B 86(5) (2024), pages 1091 to 1128
    locator: e-variables for composite nulls, optional continuation and growth-rate optimality
  - paper: doi:10.1214/23-STS894
    title: Aaditya Ramdas, Peter Grünwald, Vladimir Vovk and Glenn Shafer, Game-theoretic statistics and safe anytime-valid inference, Statistical Science 38(4) (2023), pages 576 to 601
    locator: e-variables, e-processes and test martingales, and their relation to p-values
  - paper: doi:10.1073/pnas.1922664117
    title: Larry Wasserman, Aaditya Ramdas and Sivaraman Balakrishnan, Universal inference, Proceedings of the National Academy of Sciences 117(29) (2020), pages 16880 to 16890
    locator: the split likelihood ratio statistic and its validity for any composite null
  - paper: doi:10.7326/M16-2607
    title: Tyler J. VanderWeele and Peng Ding, Sensitivity analysis in observational research, introducing the E-value, Annals of Internal Medicine 167(4) (2017), pages 268 to 274
    locator: the E-value of sensitivity analysis, a different concept with the same name
---

An e-variable is a nonnegative statistic $E$ whose expected value is at most 1 under every distribution of the null hypothesis. A large observed value, an e-value, is evidence against the null: by [Markov's inequality](/markov-inequality/), $E \ge 1/\alpha$ happens with probability at most $\alpha$ under the null, so rejecting at that threshold is a level-$\alpha$ test. An e-value is the factor by which a bettor who bets against the null multiplies the money at stake, which is why Shafer calls it a betting score. Unlike [p-values](/p-value/), e-values from successive studies can be multiplied, and the product is again an e-value, so a researcher can decide to collect more data after seeing the current evidence without losing the error guarantee.

## Definition

Let $\mathcal P_0$ be a set of distributions, the null hypothesis, for data $X$ on a sample space $\mathcal X$.

**Definition.** An e-variable for $\mathcal P_0$ is a statistic $E = e(X)$ with values in $[0, \infty]$ such that
$$E_P[E] \le 1 \quad \text{for every } P \in \mathcal P_0.$$
The observed value $e(x)$ is an e-value.

**The test.** For $0 < \alpha \le 1$, reject $\mathcal P_0$ when $E \ge 1/\alpha$. For every $P \in \mathcal P_0$, Markov's inequality gives
$$P(E \ge 1/\alpha) \le \alpha\,E_P[E] \le \alpha.$$
So the test has level $\alpha$. The bound holds for every $\alpha$ at once and needs no assumption on the distribution of $E$ beyond its mean.

**Optional continuation.** Let $E_1$ be an e-variable for the first data set, and let $E_2$ be computed from a second data set that is collected only if the first result looks promising. If, given the first data, $E_2$ has conditional expectation at most 1 under every null distribution, then
$$E_P[E_1 E_2] = E_P\left[E_1\,E_P[E_2 \mid X_1]\right] \le E_P[E_1] \le 1,$$
so $E_1 E_2$ is an e-variable, whatever rule decided to continue. When $E_2$ is not computed, set it to 1. Repeated over many steps, the running products form a nonnegative supermartingale, a [test martingale](/test-martingale/) under a simple null, and [Ville's inequality](/ville-inequality/) then gives the anytime bound $P(\sup_t E_1 \cdots E_t \ge 1/\alpha) \le \alpha$. A process whose value at every stopping time is an e-variable is an e-process. Every test martingale is an e-process, but not every e-process is a test martingale, so the two words are not synonyms.

**Words.** Vovk and Wang (2021) use "e-variable" for the random variable and "e-value" for its observed value. Grünwald, de Heide and Koolen first called them S-values. Shafer (2021) uses "betting score" for the observed value.

## Examples and non-examples

**A likelihood ratio (simple null).** Let $\mathcal P_0 = \{P_0\}$ with density $p_0$, and let $q$ be any density, fixed before the data are seen. Then $E = q(X)/p_0(X)$, with $E = \infty$ where $p_0 = 0 < q$, is an e-variable, because
$$E_{P_0}[E] = \int_{\{p_0 > 0\}} \frac{q}{p_0}\,p_0\,d\nu = \int_{\{p_0 > 0\}} q\,d\nu \le 1.$$
This is the ratio of the [Neyman-Pearson lemma](/neyman-pearson-lemma/). A [Bayes factor](/bayes-factor/) of a simple null against a composite alternative with a prior is of this kind, with $q$ the marginal density of the alternative.

**The Markov bound on a discrete example.** Let $K$ be binomial with 10 trials, test $p = 1/2$, and take $q$ binomial with $p = 0.8$. Then
$$E = \frac{0.8^K\,0.2^{10 - K}}{0.5^{10}} = 1.6^K\,0.4^{10 - K},$$
and in exact arithmetic $E_0[E] = \sum_{k=0}^{10} \binom{10}{k} 2^{-10}\,1.6^k\,0.4^{10-k} = (0.8 + 0.2)^{10} = 1$. The values of $E$ for $K = 8, 9, 10$ are $6.87$, $27.49$ and $109.95$. So $E \ge 20$ exactly when $K \ge 9$, which has null probability $11/1024 \approx 0.0107 \le 0.05$, and $E \ge 100$ exactly when $K = 10$, with probability $1/1024 \approx 0.00098 \le 0.01$. The bound holds with room to spare, because Markov's inequality is loose for most distributions. It is attained only by an e-variable that takes the values 0 and $1/\alpha$, with null probabilities $1 - \alpha$ and $\alpha$.

**Products and averages.** The product of independent e-variables is an e-variable, and so is the product of sequential ones, as above. Any weighted average $\sum_j w_j E_j$ with $w_j \ge 0$ and $\sum_j w_j = 1$ is an e-variable under any dependence, because expectation is linear. For p-values, no such simple rule exists: [Fisher's method](/fisher-combined-probability-test/) needs independence, and averages of p-values must be multiplied by a constant to stay valid.

**Calibrators from p-values.** Let $P$ be a p-value, so $P_0(P \le u) \le u$ for all $u$. For $0 < \kappa < 1$, the function $f(p) = \kappa p^{\kappa - 1}$ is decreasing with $\int_0^1 f = 1$, so $f(P)$ is an e-variable. At $p = 0.01$ and $\kappa = 1/2$ it gives $e = 5$. No member of this family gives more than $-1/(e\,p\ln p)$ at $p$, with $e$ here Euler's number, which is $7.99$ at $p = 0.01$ and $2.46$ at $p = 0.05$. Conversely, $\min(1, 1/E)$ is a p-value, by Markov's inequality. So an e-value of 20 corresponds to a p-value of at most $0.05$, but a p-value of $0.05$ corresponds to an e-value of at most about $2.5$.

**The split likelihood ratio (composite null).** Split the data into $D_0$ and $D_1$. Fit any estimate $\hat\theta_1$ on $D_1$, and let $\hat\theta_0$ maximize the likelihood over the null set $\Theta_0$ on $D_0$. Then
$$E = \frac{L(\hat\theta_1; D_0)}{L(\hat\theta_0; D_0)}$$
is an e-variable for $\Theta_0$. For any $\theta \in \Theta_0$, $L(\hat\theta_0; D_0) \ge L(\theta; D_0)$, so $E \le L(\hat\theta_1; D_0)/L(\theta; D_0)$, and given $D_1$ the right side is a likelihood ratio with a fixed numerator, whose expectation under $\theta$ is at most 1. This is the universal inference of Wasserman, Ramdas and Balakrishnan (2020). It needs no regularity conditions, unlike [Wilks' theorem](/wilks-theorem/).

**Non-example: the reciprocal of a p-value.** If $P$ is uniform on $(0, 1)$, then $E_0[1/P] = \int_0^1 u^{-1}\,du = \infty$. So $1/P$ is not an e-variable, even though $P_0(1/P \ge 1/\alpha) = \alpha$.

**Non-example: the maximized likelihood ratio.** Let $X \sim N(\mu, 1)$ and test $\mu = 0$. The ratio $\sup_\mu L(\mu; X)/L(0; X) = e^{X^2/2}$ has null expectation $\int \varphi(x)\,e^{x^2/2}\,dx = \infty$. The alternative was fitted to the same data, which breaks the computation of the first example. The [likelihood ratio test](/likelihood-ratio-test/) calibrates this statistic by its chi-squared limit, not by Markov's inequality.

**Non-example: the E-value of sensitivity analysis.** VanderWeele and Ding (2017) define an "E-value" for observational studies: the smallest strength of association, on the risk ratio scale, that an unmeasured confounder must have with both treatment and outcome to explain away an observed risk ratio $RR > 1$. It equals $RR + \sqrt{RR(RR - 1)}$. It is a measure of robustness to confounding, not a statistic with expectation at most 1, and it has nothing to do with this page except the name.

## Related definitions

- **p-value.** A [p-value](/p-value/) $P$ satisfies $P_0(P \le u) \le u$ for each $u$, a condition on the whole distribution. An e-variable satisfies one condition on the mean. A p-value test is valid for one fixed $\alpha$ and one fixed sample size. An e-value keeps its meaning when data are added.
- **Test martingale and e-process.** A [test martingale](/test-martingale/) is a nonnegative martingale with initial value 1 under the null. Its value at any stopping time is an e-variable. An e-process is a process whose value at any stopping time is an e-variable. For composite nulls, e-processes exist in cases where no nontrivial test martingale does.
- **Ville's inequality.** [Ville's inequality](/ville-inequality/) is the time-uniform form of the Markov bound for nonnegative supermartingales. It gives anytime-valid tests and [confidence sequences](/confidence-sequence/).
- **Growth-rate optimality.** Among e-variables for $\mathcal P_0$, a growth-rate optimal one maximizes $E_Q[\log E]$ under an alternative $Q$, the Kelly criterion of betting. For a simple null $P_0$ and a simple alternative $Q$, the optimum is the likelihood ratio $q/p_0$, and the optimal growth rate is the [Kullback-Leibler divergence](/kullback-leibler-divergence/) $D(Q \Vert P_0)$.
- **Likelihood ratios and Bayes factors.** Every likelihood ratio of a simple null with a fixed alternative, and every [Bayes factor](/bayes-factor/) of a simple null, is an e-variable. For composite nulls, a Bayes factor is not an e-variable in general, because its null expectation can exceed 1 at some null distributions.
- **Multiple testing.** The e-BH procedure applies the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/) to the p-values $1/E_j$ and controls the false discovery rate under arbitrary dependence of the e-values.

## References
