---
tag: SR875B
kind: algorithm
slug: fisher-combined-probability-test
name: Fisher's method
aliases:
- Fisher's combined probability test
area: statistics-and-inference/hypothesis-testing
level: core
summary: Combines k independent p-values into minus two times the sum of their logs, which has a chi-squared law with 2k degrees of freedom under the global null.
model: real-ram
complexity:
  vars: {k: the number of p-values combined}
  time: {worst: Θ(k), best: Θ(k)}
  space: {extra: Θ(k)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1932
  people: [Ronald A. Fisher]
  note: Fisher added the method to the fourth edition of Statistical Methods for Research Workers in 1932. Karl Pearson proposed the same statistic, and a variant, in 1933.
prereqs: [statistical-hypothesis-test, p-value, poisson-distribution]
see_also: [multiple-comparisons-problem, bonferroni-correction, holm-bonferroni-method, benjamini-hochberg-procedure, closed-testing-principle, e-variable, statistical-power, fisher-exact-test]
sources:
  - paper: doi:10.1080/01621459.1954.10483521
    title: Allan Birnbaum, Combining independent tests of significance, Journal of the American Statistical Association 49(267) (1954), pages 559 to 574
    locator: no method of combining independent tests is optimal in general; optimal properties of the methods of Fisher and Tippett
  - paper: doi:10.1080/01621459.1971.10482347
    title: Ramon C. Littell and J. Leroy Folks, Asymptotic optimality of Fisher's method of combining independent tests, Journal of the American Statistical Association 66(336) (1971), pages 802 to 806
    locator: Fisher's method has the largest exact Bahadur slope among monotone methods of combination
  - paper: doi:10.2307/2529826
    title: Morton B. Brown, A method for combining non-independent, one-sided tests of significance, Biometrics 31(4) (1975), pages 987 to 992
    locator: the scaled chi-squared approximation of the null law of Fisher's statistic for dependent tests
---

Fisher's method combines $k$ p-values from independent tests into one test of the global null hypothesis, the hypothesis that all $k$ nulls are true. Its statistic is $X = -2\sum_{i=1}^k \ln p_i$. When the p-values are independent and each is uniform on $(0, 1)$ under its null, $X$ has the $\chi^2_{2k}$ law exactly, and the combined p-value is the upper tail $P(\chi^2_{2k} \ge X)$. Because the degrees of freedom are even, this tail is a finite sum, $e^{-X/2}\sum_{j<k}(X/2)^j/j!$, so the whole computation is $\Theta(k)$ operations with no special function. The method is not to be confused with [Fisher's exact test](/fisher-exact-test/) for $2 \times 2$ tables.

## In plain words

Several independent studies each test the same kind of claim and each reports a p-value. None of them may be small enough on its own, but together they may still be hard to explain by chance. Fisher's method multiplies the p-values. If every claim is false, the product of k random numbers between 0 and 1 has a known distribution, so we can ask how often a product this small happens by chance. That probability is the combined p-value. Taking logs turns the product into a sum, and minus twice that sum follows a chi-squared law. One very small p-value can make the product small by itself, so the method reacts to strong evidence in a single study.

## The problem

**Model and hypotheses.** There are $k$ tests with p-values $p_1, \dots, p_k$, computed from independent data. Test $i$ has null $H_{0,i}$. The global null is $H_0 = H_{0,1} \cap \dots \cap H_{0,k}$. The alternative is that at least one $H_{0,i}$ is false. Each $p_i$ is uniform on $(0, 1)$ under $H_{0,i}$, as it is for a test with a continuous statistic and a simple null.

**Statistic.** $X = -2\sum_{i=1}^k \ln p_i = -2\ln\prod_i p_i$. Small p-values give a large $X$.

**Null distribution.** Exact. If $U$ is uniform on $(0, 1)$, then $P(-2\ln U \ge x) = P(U \le e^{-x/2}) = e^{-x/2}$, which is the $\chi^2_2$ law. A sum of $k$ independent $\chi^2_2$ variables is $\chi^2_{2k}$. So under $H_0$, $X \sim \chi^2_{2k}$, with mean $2k$ and variance $4k$.

**Rejection rule and size.** Reject at level $\alpha$ when $X \ge \chi^2_{2k, 1-\alpha}$, equivalently when $P \le \alpha$. Under the stated conditions the size is exactly $\alpha$. If some $p_i$ are only valid, $P(p_i \le u) \le u$, as for discrete tests, the size is at most $\alpha$, because $X$ is then stochastically smaller than $\chi^2_{2k}$.

**p-value.** With $h = X/2 = -\sum_i \ln p_i$,
$$P = P(\chi^2_{2k} \ge X) = e^{-h}\sum_{j=0}^{k-1}\frac{h^j}{j!}.$$
This is $P(N \le k - 1)$ for $N$ a [Poisson](/poisson-distribution/) variable with mean $h$. For $k = 1$, $P = p_1$. For $k = 2$, with $q = p_1p_2$, $P = q(1 - \ln q)$.

**Sensitivity and power.** The test rejects when the product of the p-values is small. It has good power when one or a few studies show strong evidence, and when all show moderate evidence. It has less power than Stouffer's method when every study shows the same weak effect, and less power than Tippett's minimum when exactly one study is far from its null and the others are close to theirs. No combination method is most powerful against every alternative (Birnbaum 1954). As the sample sizes of the studies grow, Fisher's method is optimal in Bahadur's sense (Littell and Folks 1971).

## The algorithm

```pseudo id=main
FISHER-METHOD(p₁, …, p_k)          ▷ independent p-values in [0, 1], k ≥ 1
L1  if some pᵢ = 0 then return (∞, 0)
L2  h ← −Σ ln pᵢ                     ▷ compensated sum of logs; never form Π pᵢ
L3  X ← 2h
L4  tⱼ ← exp(−h + j ln h − ln j!) for j = 0, …, k − 1
L5  P ← Σ tⱼ
L6  return (X, min(P, 1))
```

When all $p_i = 1$, $h = 0$, and the implementation returns $(0, 1)$ before line L4, which would need $\ln 0$.

## Example

**Four studies.** Four independent studies of the same treatment report $p = 0.08, 0.12, 0.06, 0.20$. None is significant at 5%.

| step | value |
|---|---|
| $-2\ln p_i$ | 5.0515, 4.2405, 5.6268, 3.2189 |
| L2: $h = -\sum_i \ln p_i$ | 9.0688 |
| L3: $X = 2h$, the sum of the row above | 18.1377 |
| L4: $t_0, t_1, t_2, t_3$ | 0.000115, 0.001045, 0.004737, 0.014320 |
| L5: $P = \sum_j t_j$ | 0.020218 |

So $P = 0.0202$ with 8 degrees of freedom. The 5% critical value is $\chi^2_{8, 0.95} = 15.5073 < 18.1377$, and the global null is rejected at 5%. The combined evidence is stronger than the evidence of each study.

**Three methods, three patterns.** The table compares Fisher's method with Stouffer's method, $Z = \sum_i \Phi^{-1}(1 - p_i)/\sqrt k$, and Tippett's method, $1 - (1 - \min_i p_i)^k$.

| p-values | Fisher | Stouffer | Tippett |
|---|---|---|---|
| 0.08, 0.12, 0.06, 0.20 | 0.0202 | 0.0064 | 0.2193 |
| 0.001, 0.9, 0.9, 0.9 | 0.0708 | 0.6470 | 0.0040 |
| 0.2, ten times | 0.0413 | 0.0039 | 0.8926 |

With moderate evidence everywhere, Stouffer's method gives the smallest p-value and Tippett's the largest. With one strong study and three weak ones, Tippett's gives the smallest, Stouffer's sees nothing, and Fisher's is in between. In each row Fisher's p-value lies between the other two. This balance is one reason why it is a common default.

**Two studies, by hand.** For $p = 0.03$ and $0.04$, $q = 0.0012$ and $P = 0.0012(1 - \ln 0.0012) = 0.0012 \cdot 7.7255 = 0.009271$.

## Correctness

Under $H_0$, each $-2\ln p_i$ has the $\chi^2_2$ law, by the computation in the problem section, and they are independent, so $X \sim \chi^2_{2k}$. The density of $\chi^2_{2k}$ at $x$ is the Gamma density with shape $k$ and scale 2, and integrating by parts $k - 1$ times gives the upper tail $e^{-x/2}\sum_{j<k}(x/2)^j/j!$. Lines L2 to L5 compute exactly this sum. Since the tail function is continuous and strictly decreasing, $P$ is uniform under $H_0$, and rejecting when $P \le \alpha$ has size exactly $\alpha$. This is proved, with no approximation. What depends on the data is the assumption of independent, uniform p-values; when it fails, the size is wrong, as the pitfalls show. The correctness proof gives each step.

## Complexity

On a [real RAM](/real-ram/) with $\ln$ and $\exp$ as unit-cost operations, line L2 takes $k$ logarithms and line L4 $k$ terms, so the time is $\Theta(k)$. The list of terms takes $\Theta(k)$ extra space; a plain running sum would take $\Theta(1)$.

**Numerical stability.** The product $\prod_i p_i$ underflows quickly: 300 p-values of 0.1 give $10^{-300}$, and more give 0. Line L2 sums logarithms instead, with a compensated sum, so $X$ is accurate for any $k$. Each term in line L4 is computed as one exponential of a log, so the code never forms $e^{-h}$ alone, which underflows for $h > 745$, or $h^j/j!$ alone, which can overflow. All terms are positive, so the sum in line L5 has no cancellation, and $P$ has a small relative error even when it is tiny. It underflows to 0 only when the true $P$ is below about $10^{-308}$. Computing $P$ as $1 - P(\chi^2_{2k} \le X)$ would lose all accuracy for small $P$.

## Properties

- **Exact.** Under independence and uniform p-values, $X \sim \chi^2_{2k}$ with no approximation, for every $k$.
- **Symmetric and monotone.** $P$ does not depend on the order of the p-values, and it decreases when any $p_i$ decreases.
- **Dominated by one small p-value.** A single $p_i \to 0$ sends $X \to \infty$ and $P \to 0$, whatever the other values. A single $p_i = 0$ gives $P = 0$.
- **Not dominated by one large p-value.** $p_i = 1$ adds 0 to $X$ but 2 to the degrees of freedom, so it weakens the evidence without cancelling it.
- **Optimal for large studies.** Among monotone combination methods, it has the largest exact Bahadur slope as the sample sizes grow (Littell and Folks 1971).
- **Valid for discrete p-values.** With p-values that satisfy $P(p_i \le u) \le u$, the test stays valid but is conservative.

## Variants and improvements

- **Stouffer's method.** $Z = \sum_i \Phi^{-1}(1 - p_i)/\sqrt k$, which is $N(0, 1)$ under $H_0$. With weights $w_i$, $Z = \sum_i w_i\Phi^{-1}(1 - p_i)/\sqrt{\sum_i w_i^2}$; weights $\sqrt{n_i}$ give the most power when all studies estimate the same effect. It needs one-sided p-values in a common direction.
- **Tippett's method.** Use $\min_i p_i$, with $P = 1 - (1 - \min_i p_i)^k$. This is the Šidák adjustment of the smallest p-value, and it is close to the [Bonferroni correction](/bonferroni-correction/) $k\min_i p_i$ used as a global test.
- **Pearson's method.** $-2\sum_i \ln(1 - p_i)$ is also $\chi^2_{2k}$ under $H_0$, and it is large when the p-values are near 1. Pearson (1933) proposed this variant along with the product statistic.
- **Lancaster's weighted method.** Replace each $-2\ln p_i$ by the $\chi^2_{d_i}$ quantile of $1 - p_i$, so that larger studies get more degrees of freedom. The sum is $\chi^2_{\sum d_i}$.
- **Brown's method.** For dependent tests, Brown (1975) approximates $X$ by $c\chi^2_f$, with $c$ and $f$ chosen to match the mean $2k$ and the variance $4k + 2\sum_{i<j}\operatorname{Cov}(-2\ln p_i, -2\ln p_j)$: $f = 2E[X]^2/\operatorname{Var}(X)$ and $c = \operatorname{Var}(X)/(2E[X])$. For tests built from correlated normal statistics, Brown gives the covariances as a function of the correlation.
- **Permutation calibration.** When the dependence is unknown but the raw data are available, compute $X$ on permuted data and take the p-value from the [permutation test](/permutation-test/) distribution.
- **Closed testing.** Fisher's method used for every intersection of nulls, inside the [closed testing principle](/closed-testing-principle/), gives tests of the single nulls with strong family-wise error control.
- **e-values.** Products of independent [e-variables](/e-variable/) are e-variables, which gives a combination rule that also works under optional continuation, where Fisher's method does not.

## When to use it

Use Fisher's method to ask whether there is any signal at all in a set of independent tests, for example in a meta-analysis of studies that report only p-values, or to combine tests of one hypothesis on independent subsets of data. It answers "is at least one null false", not "which one", and not "how large is the effect". To find which nulls are false, use a multiple testing procedure such as [Holm's](/holm-bonferroni-method/) or [Benjamini-Hochberg](/benjamini-hochberg-procedure/). When the studies report effects and standard errors, a weighted meta-analysis of the effects is better than any combination of p-values. When the tests are dependent, use Brown's method or permutations instead.

## Pitfalls

- **Dependent p-values.** If all $k$ p-values are the same uniform value $U$, then $X = -2k\ln U$ and the size of the nominal 5% test is $e^{-\chi^2_{2k, 0.95}/(2k)}$: 0.093 for $k = 2$, 0.144 for $k = 4$ and 0.208 for $k = 10$. Positive dependence makes the test anti-conservative.
- **Two-sided p-values.** Combining two-sided p-values from studies with effects in opposite directions gives evidence against the global null that does not support any single direction. Use one-sided p-values when the direction matters.
- **A p-value of 0.** Software that rounds a tiny p-value to 0 makes $X$ infinite and $P = 0$. Keep the p-values to full precision.
- **Selected p-values.** Combining only the published studies, or only the significant subgroups, makes the p-values non-uniform under the null, and the combined p-value is far too small.
- **Rejecting $H_0$ is weak information.** It says that at least one null is false. It does not say that most are false, or that the effect is consistent.

## Implementations

## History

Fisher described the method in the fourth edition of Statistical Methods for Research Workers (1932), in the section on combining the probabilities of independent tests, in which he gave the $\chi^2_{2k}$ law of $-2\ln\prod_i p_i$. Tippett had proposed the minimum p-value in 1931, and Karl Pearson published the same product statistic, with a variant for p-values near 1, in 1933. Stouffer and his coauthors used the normal combination in The American Soldier (1949). Birnbaum (1954) proved that no combination method is best against every alternative, and Littell and Folks (1971) proved that Fisher's method is asymptotically optimal in Bahadur's sense. Brown (1975) gave the scaled chi-squared correction for dependent tests that is still in common use.

## References
