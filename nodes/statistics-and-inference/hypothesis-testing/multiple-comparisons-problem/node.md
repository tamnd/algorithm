---
tag: W0S7V6
kind: problem
slug: multiple-comparisons-problem
name: Multiple comparisons problem
aliases:
- multiple testing problem
- multiplicity problem
area: statistics-and-inference/hypothesis-testing
level: intro
summary: Testing many hypotheses at once inflates the chance of false rejections. The problem is to control an error rate over the whole family while keeping power.
prereqs: [statistical-hypothesis-test, p-value, type-i-and-type-ii-errors]
see_also: [family-wise-error-rate, false-discovery-rate, bonferroni-correction, holm-bonferroni-method, benjamini-hochberg-procedure, closed-testing-principle, tukey-hsd, post-selection-inference]
sources:
  - paper: doi:10.1214/ss/1056397487
    title: Sandrine Dudoit, Juliet Popper Shaffer and Jennifer C. Boldrick, Multiple hypothesis testing in microarray experiments, Statistical Science 18(1) (2003), pages 71 to 103
    locator: the survey of type I error rates, of single-step, step-down and step-up procedures, and of resampling methods
  - paper: doi:10.1111/j.2517-6161.1995.tb02031.x
    title: Yoav Benjamini and Yosef Hochberg, Controlling the false discovery rate, a practical and powerful approach to multiple testing, Journal of the Royal Statistical Society, Series B 57(1) (1995), pages 289 to 300
    locator: the definition of the FDR, the comparison with FWER methods, and the example with 15 p-values used in the table below
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Chapter 9 (multiple testing and simultaneous inference)
---

The multiple comparisons problem arises when one data analysis tests many hypotheses $H_1, \dots, H_m$ and reports the ones it rejects. Each test alone has a small chance $\alpha$ of a false rejection, but over many tests false rejections become likely: with 15 independent true nulls tested at $\alpha = 0.05$, the chance of at least one is $1 - 0.95^{15} = 0.537$. The problem is to choose which hypotheses to reject so that an error rate for the whole family stays below a set level, and to reject as many false nulls as possible under that limit. The two main error rates are the [family-wise error rate](/family-wise-error-rate/) (FWER), the probability of any false rejection, and the [false discovery rate](/false-discovery-rate/) (FDR), the expected share of false rejections among all rejections. Solutions differ in which rate they control, under which dependence between the tests, and how much power they keep.

## In plain words

If you flip a fair coin five times, getting five heads is rare. If a thousand people each flip five times, some of them will surely get five heads, and none of them has a special coin. Testing many hypotheses is the same. A result that would be surprising alone is expected somewhere in a large batch. So you must judge each result against the size of the batch. You can ask for no false alarms at all in the batch, which is strict and finds fewer real effects. Or you can ask that false alarms make up only a small part of what you report, which is looser and finds more. Either way, the rule must be fixed before you look at the results.

## Definition

**Input.** Hypotheses $H_1, \dots, H_m$ about the law of the data, and for each a p-value $p_i$, or the data themselves when a method uses the joint law of the tests. Sorted p-values are written $p_{(1)} \le \dots \le p_{(m)}$. A level: $\alpha$ for the FWER, $q$ for the FDR.

**Output.** A set $\mathcal R$ of rejected hypotheses, often with an adjusted p-value for each hypothesis, the smallest level at which it would be rejected.

**Counts.** Let $I_0$ be the unknown set of true nulls, $m_0 = |I_0|$, $R = |\mathcal R|$ the number of rejections and $V = |\mathcal R \cap I_0|$ the number of false rejections.

**Criterion.** Control an error rate for every possible $I_0$ (strong control):

- FWER: $P(V \ge 1) \le \alpha$.
- FDR: $E[V/\max(R, 1)] \le q$.

Among the procedures that control the chosen rate under the assumed dependence, prefer the one that rejects more false nulls. The FDR is never larger than the FWER, so FDR control is the weaker requirement and allows more power.

**Assumptions on dependence.** Each null p-value is valid, $P(p_i \le u) \le u$. Beyond that, a method may assume arbitrary dependence, independence, positive dependence (PRDS), or invariance of the joint law of the data under a permutation group.

## Variants

- **Simultaneous confidence intervals.** Cover all parameters at once with probability at least $1 - \alpha$; intervals that do so give tests with strong FWER control. [Tukey's HSD](/tukey-hsd/) does this for all pairwise differences of means, and the [Scheffé method](/scheffe-method/) for all contrasts.
- **Generalized error rates.** The $k$-FWER $P(V \ge k)$, the tail of the false discovery proportion $P(V/\max(R, 1) > \gamma)$, and the per-family rate $E[V]$.
- **Posterior and empirical Bayes versions.** The positive FDR, Storey's q-values and Efron's [local false discovery rate](/local-false-discovery-rate/) treat the hypotheses as draws from a two-group mixture.
- **Structured families.** Ordered or hierarchical hypotheses (gatekeeping, graphical procedures), families of variables in a regression ([knockoffs](/knockoff-filter/)), and tests chosen after looking at the data ([post-selection inference](/post-selection-inference/)).
- **Online testing.** Hypotheses arrive one at a time and each decision is final, with the error rate controlled over the whole stream.

## Examples

**Fifteen p-values.** Benjamini and Hochberg (1995) used 15 p-values from a clinical trial: 0.0001, 0.0004, 0.0019, 0.0095, 0.0201, 0.0278, 0.0298, 0.0344, 0.0459, 0.3240, 0.4262, 0.5719, 0.6528, 0.7590, 1.000. At level 0.05 ($\alpha$ or $q$), the methods of this area reject:

| method | error rate | dependence allowed | rejections |
|---|---|---|---|
| no correction | per test | any | 9 |
| [Bonferroni](/bonferroni-correction/) | FWER | any | 3 |
| [Holm](/holm-bonferroni-method/) | FWER | any | 3 |
| [Hochberg](/hochberg-procedure/) | FWER | independent or PRDS | 3 |
| [Benjamini-Yekutieli](/benjamini-yekutieli-procedure/) | FDR | any | 3 |
| [Benjamini-Hochberg](/benjamini-hochberg-procedure/) | FDR | independent or PRDS | 4 |
| [Storey-Taylor-Siegmund](/storey-q-value/), $\lambda = 0.5$ | FDR | independent | 8 |
| [Storey q-values](/storey-q-value/) at 0.05, $\lambda = 0.5$ | FDR, asymptotic | weak dependence, large $m$ | 9 |

Bonferroni compares each p-value with $0.05/15 = 0.00333$, so 0.0019 passes and 0.0095 fails. Benjamini-Hochberg compares $p_{(k)}$ with $0.05k/15$; the largest $k$ that passes is 4, since $0.0095 \le 0.0133$ and no later p-value passes its threshold. Storey's methods estimate the share of true nulls from the 4 p-values above $0.5$: the q-values use $4/(15 \cdot 0.5) = 8/15$, and STS adds one to the count, which gives $10/15$. They divide the BH thresholds by that share. The plain q-value rule has no finite-sample guarantee. The counts were computed with the implementations on the linked pages.

**Pairwise comparisons.** With 5 groups there are 10 pairs of means. Ten $t$-tests at 0.05 each can have a FWER well above 0.05 when all means are equal. Tukey's HSD uses the joint law of all pairwise differences and controls the FWER at exactly 0.05 for balanced groups with normal errors, with more power than Bonferroni at $0.005$ per pair.

**Correlated tests with few units.** With 8 units in two groups of 4, the smallest possible permutation p-value is $2/70$. Holm at 0.05 can then never reject among 4 tests, since $4 \cdot 2/70 > 0.05$, while the [Westfall-Young procedure](/westfall-young-procedure/), which uses the joint permutation law, can.

## Known algorithms

| method | type | rate and assumption | cost |
|---|---|---|---|
| [Bonferroni correction](/bonferroni-correction/) | single-step | FWER, any dependence | $\Theta(m)$ |
| [Holm-Bonferroni method](/holm-bonferroni-method/) | step-down | FWER, any dependence | $\Theta(m\log m)$ |
| [Hochberg procedure](/hochberg-procedure/) | step-up | FWER, independence or PRDS | $\Theta(m\log m)$ |
| [Closed testing principle](/closed-testing-principle/) | general | FWER from any local level-$\alpha$ tests | $2^m - 1$ tests, less with shortcuts |
| [Westfall-Young procedure](/westfall-young-procedure/) | step-down, resampling | FWER, permutation invariance of the true nulls | $\Theta(Bmn + m\log m)$ for $B$ permutations |
| [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/) | step-up | FDR $= (m_0/m)q$, independence; $\le (m_0/m)q$ under PRDS | $\Theta(m)$ with buckets |
| [Benjamini-Yekutieli procedure](/benjamini-yekutieli-procedure/) | step-up | FDR, any dependence, level $q/\sum_{k \le m}1/k$ | $\Theta(m)$ |
| [Storey q-value](/storey-q-value/) | adaptive step-up | FDR, independence (modified version); asymptotic (plain) | $\Theta(m\log m)$ |
| [Knockoff filter](/knockoff-filter/) | selection with fake features | FDR in a regression, Gaussian linear model with $n \ge 2p$ | $\Theta(np^2 + p^3)$ to build |
| [Tukey's HSD](/tukey-hsd/), [Scheffé](/scheffe-method/) | simultaneous intervals | FWER for pairs or contrasts of means | closed form |

## Bounds

- **The union bound is sharp under arbitrary dependence.** For a test of the global null that rejects when $\min_ip_i \le c$, the worst case over all joint laws with uniform marginals gives $P(\min_ip_i \le c) = \min(1, mc)$, attained when the rejection events are disjoint. So $c = \alpha/m$, the Bonferroni threshold, is the largest constant threshold valid for every dependence.
- **The BY factor is sharp.** Under arbitrary dependence a step-up procedure with the BH thresholds can have FDR as large as $q\sum_{k \le m}1/k \approx q\ln m$, so the division by this sum in Benjamini-Yekutieli cannot be removed in general; the BY page gives the law that attains it.
- **BH is exact.** For independent continuous p-values the FDR of BH equals $(m_0/m)q$, whatever the false nulls are; so its level is $q$ only when $m_0 = m$, and adaptive methods such as Storey's recover the factor $m/m_0$.
- **FDR is at most FWER**, with equality when all nulls are true. So any FDR method gives weak FWER control, and any strong FWER method controls the FDR.
- **Discreteness.** With permutation or exact discrete tests, a p-value cannot go below the smallest attainable value, which limits what any method can reject.
- **Computation.** Every method above reads all $m$ p-values, so $\Omega(m)$ time is needed. Step-wise methods that depend on the order use a sort, $\Theta(m\log m)$, though BH needs only the count of rejections and runs in $\Theta(m)$. Closed testing without a shortcut takes $2^m - 1$ local tests.

## Reductions

- **Closed testing.** Any family of level-$\alpha$ tests of the intersections $\bigcap_{i \in I}H_i$ gives strong FWER control. Holm is closed testing with Bonferroni local tests, Hommel's method is closed testing with Simes local tests, and Westfall-Young is closed testing with permutation tests of the maximum.
- **Global null to FDR.** Under the global null, BH at level $q$ is the Simes test of $\bigcap_iH_i$ at level $q$.
- **Tests to intervals.** Simultaneous confidence intervals at level $1 - \alpha$ give tests with strong FWER control, by checking which null values the intervals exclude.
- **Adjusted p-values.** Every procedure with nested rejection sets as the level grows can report one adjusted p-value per hypothesis, so a reader can apply their own level.

## Applications

Genome-wide studies test thousands to millions of genes or variants at once, and FDR methods, q-values and the local FDR were developed largely for them. Clinical trials with several end points or several doses use FWER control, often with gatekeeping or graphical versions of Holm's method, because regulators require strict control. Neuroimaging tests every voxel of a brain scan and uses permutation methods of the Westfall-Young type. Online experiments in industry run many A/B tests at once and over time. Pairwise comparisons after an analysis of variance use Tukey's HSD. In regression, variable selection with FDR control uses knockoffs.

## References
