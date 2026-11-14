---
tag: WKCJWX
kind: algorithm
slug: storey-q-value
name: Storey's q-value method
aliases:
- q-value
- adaptive FDR estimation
area: statistics-and-inference/hypothesis-testing
level: advanced
summary: Estimate the share of true nulls as #{p > lambda} / (m (1 - lambda)) and run BH at q / pi0. The q-value of a test is the smallest estimated FDR at which it is rejected.
model: real-ram
complexity:
  vars: {m: the number of hypotheses}
  time: {worst: Θ(m log m), best: Θ(m log m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2002
  people: [John D. Storey, Robert Tibshirani, Jonathan E. Taylor, David Siegmund]
  note: Storey (2002) estimated the FDR of fixed rejection regions with an estimate of the null proportion. Storey and Tibshirani (2003) made the q-value standard in genomics, and Storey, Taylor and Siegmund (2004) proved finite-sample and asymptotic control.
prereqs: [benjamini-hochberg-procedure, false-discovery-rate]
see_also: [local-false-discovery-rate, benjamini-yekutieli-procedure, empirical-bayes, bootstrap-method, multiple-comparisons-problem, p-value]
sources:
  - paper: doi:10.1111/1467-9868.00346
    title: John D. Storey, A direct approach to false discovery rates, Journal of the Royal Statistical Society, Series B 64(3) (2002), pages 479 to 498
    locator: the estimate of pi_0 from the p-values above lambda, the estimated FDR and pFDR of a fixed rejection region, and the choice of lambda by the bootstrap
  - paper: doi:10.1214/aos/1074290335
    title: John D. Storey, The positive false discovery rate, a Bayesian interpretation and the q-value, The Annals of Statistics 31(6) (2003), pages 2013 to 2035
    locator: the q-value as the minimum pFDR over the nested rejection regions that contain the statistic, and its posterior interpretation under the mixture model
  - paper: doi:10.1073/pnas.1530509100
    title: John D. Storey and Robert Tibshirani, Statistical significance for genomewide studies, Proceedings of the National Academy of Sciences 100(16) (2003), pages 9440 to 9445
    locator: the q-value for genome-wide studies, its estimate from the p-values, and the estimate of pi_0 from a smoother over lambda
  - paper: doi:10.1111/j.1467-9868.2004.00439.x
    title: John D. Storey, Jonathan E. Taylor and David Siegmund, Strong control, conservative point estimation and simultaneous conservative consistency of false discovery rates, a unified approach, Journal of the Royal Statistical Society, Series B 66(1) (2004), pages 187 to 205
    locator: Theorem 1 (the estimated FDR is conservative), Lemma 2 (thresholding the estimate is BH with m replaced by pi0-hat m), Theorem 3 (FDR at most (1 - lambda^(m_0)) alpha for the modified procedure with independent null p-values), and Theorems 4 to 7 (asymptotic control and q-values under weak dependence)
---

Storey's method makes the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/) adaptive. BH controls the [false discovery rate](/false-discovery-rate/) at $(m_0/m)q$, not at $q$, so when many nulls are false it is more conservative than it needs to be. Storey estimates the proportion of true nulls $\pi_0 = m_0/m$ from the p-values above a cutoff $\lambda$, which come mostly from true nulls, as $\hat\pi_0 = \#\{i : p_i > \lambda\}/(m(1 - \lambda))$. Then he runs BH at $q/\hat\pi_0$. The q-value of a hypothesis is the smallest estimated FDR among the rejection rules "reject $p_j \le t$" that reject it; it is to the FDR what an adjusted p-value is to the FWER. With a small change to the estimator, the procedure controls the FDR at $q$ in finite samples when the null p-values are independent (Storey, Taylor and Siegmund 2004), and the plain version controls it asymptotically under weak dependence.

## In plain words

When a study has many real effects, the usual false discovery method acts as if every test could be a false alarm, and so it is too strict. This method first estimates how many tests are really null. It looks at the tests with large p-values, which are mostly nulls, and scales their count up, because a null p-value is equally likely to land anywhere between 0 and 1. If only half the tests look null, the method allows itself about twice the usual leniency. Each test then gets a q-value: the smallest estimated share of false discoveries you must accept to call that test a discovery. Report the tests whose q-value is below the share you can live with.

## The problem

**Input.** P-values $p_1, \dots, p_m$, a tuning constant $\lambda \in [0, 1)$, often $1/2$, and, for a rejection rule, a target level $q$.

**Output.** The estimate $\hat\pi_0$, the q-values $\hat q_1, \dots, \hat q_m$, and the rejected set $\{i : \hat q_i \le q\}$.

**Error rate controlled.** The false discovery rate $E[V/\max(R, 1)]$.

**Dependence and level.**

- **Finite samples, modified estimator.** With $\hat\pi_0^* = (1 + \#\{i : p_i > \lambda\})/(m(1 - \lambda))$ and rejection thresholds limited to $t \le \lambda$, the FDR is at most $(1 - \lambda^{m_0})q \le q$ when the null p-values are valid and independent of each other and of the non-null p-values (Storey, Taylor and Siegmund 2004, Theorem 3). The proof page proves it, and the tests check it exactly on a grid and by Monte Carlo.
- **Asymptotic, plain estimator.** For large $m$ with weakly dependent p-values whose empirical distribution functions converge, the plain rule controls the FDR at $q$ in the limit, and the q-values are simultaneously conservative (Theorems 4 to 7 of the same paper). In finite samples it can exceed $q$; the tests measure 0.112 at $q = 0.1$ in one model.
- **Arbitrary dependence.** No guarantee. Strong positive correlation makes $\hat\pi_0$ very noisy.

## The algorithm

```pseudo id=main
STOREY-Q-VALUES(p₁, …, p_m, λ)          ▷ p-values in [0, 1], 0 ≤ λ < 1
L1  W ← #{i : p_i > λ}
L2  π̂₀ ← min(1, W / (m(1 − λ)))
L3  sort the indices so that p_(1) ≤ … ≤ p_(m)
L4  run ← 1; for r ← m down to 1 do
L5      run ← min(run, π̂₀ · m · p_(r) / r)
L6      q̂_(r) ← run
L7  return q̂                           ▷ reject H_i at level q when q̂_i ≤ q
```

The estimated FDR of the rule "reject $p_j \le t$" is $\widehat{\text{FDR}}(t) = \hat\pi_0mt/\max(\#\{j : p_j \le t\}, 1)$. Over $t \ge p_{(r)}$, between two data points it grows with $t$, so its minimum is at a data point $p_{(j)}$ with $j \ge r$, where it is $\hat\pi_0mp_{(j)}/j$. Lines L4 to L6 take that minimum as a running minimum from the right. With $\lambda = 0$, $\hat\pi_0 = 1$ and the q-values are the BH adjusted p-values. Rejecting $\hat q_i \le q$ is BH at level $q/\hat\pi_0$ (Lemma 2 of Storey, Taylor and Siegmund).

**The version with finite-sample control.** Replace line L2 by $\hat\pi_0^* = (1 + W)/(m(1 - \lambda))$, without the cap, and reject the $k$ smallest p-values for the largest $k$ with $p_{(k)} \le \lambda$ and $\hat\pi_0^*mp_{(k)} \le kq$. This is the rule "reject $p_j \le t$ for the largest $t \le \lambda$ with estimated FDR at most $q$". The added 1 keeps $\hat\pi_0^*$ away from 0, and the limit $t \le \lambda$ keeps the p-values used to estimate $\pi_0$ apart from the ones that are rejected.

## Example

**The 15 p-values of Benjamini and Hochberg (1995)** (0.0001, 0.0004, 0.0019, 0.0095, 0.0201, 0.0278, 0.0298, 0.0344, 0.0459, 0.3240, 0.4262, 0.5719, 0.6528, 0.7590, 1.000), with $\lambda = 0.5$ and $q = 0.05$. Four p-values exceed 0.5, so $\hat\pi_0 = 4/(15 \cdot 0.5) = 0.533$ and $\hat\pi_0^* = 5/7.5 = 0.667$.

| $k$ | $p_{(k)}$ | BH $kq/m$ | Storey $kq/(m\hat\pi_0)$ | STS $kq/(m\hat\pi_0^*)$ | q-value $\hat q_{(k)}$ |
|---|---|---|---|---|---|
| 4 | 0.0095 | 0.0133 | 0.025 | 0.02 | 0.019 |
| 5 | 0.0201 | 0.0167 | 0.03125 | 0.025 | 0.0322 |
| 8 | 0.0344 | 0.0267 | 0.05 | 0.04 | 0.0344 |
| 9 | 0.0459 | 0.03 | 0.05625 | 0.045 | 0.0408 |
| 10 | 0.3240 | 0.0333 | 0.0625 | 0.05 | 0.2592 |

BH rejects 4. The plain Storey rule rejects 9, the last rank below its threshold; these are the nine q-values below 0.05. The STS version rejects 8, because 0.0459 is above 0.045. The q-values of all 15 are 0.0008, 0.0016, 0.0051, 0.019, 0.0322, 0.0341, 0.0341, 0.0344, 0.0408, 0.2592, 0.31, 0.3813, 0.4017, 0.4337 and 0.5333; the last one is $\hat\pi_0$ itself.

**Why the estimate is conservative.** A uniform null p-value exceeds $\lambda$ with probability $1 - \lambda$, so $E[W] \ge m_0(1 - \lambda)$, and the non-null p-values above $\lambda$ only add to $W$. Hence $E[W/(m(1 - \lambda))] \ge m_0/m$: the uncapped estimate is biased upward, which errs on the safe side. The bias is the share of non-null p-values above $\lambda$; it shrinks as $\lambda$ grows, while the variance grows, since fewer p-values are counted.

## Correctness

The finite-sample guarantee for the modified procedure is a theorem of Storey, Taylor and Siegmund (2004), who prove it with a martingale argument. The [proof page](proofs/correctness.md) gives a leave-one-out proof instead. Fix a true null $H_i$. When $p_i \le \lambda$, the count $W$ does not depend on $p_i$, so given the other p-values the procedure is a step-up rule with fixed thresholds at most $kq(1 - \lambda)/(1 + W_{-i})$, where $W_{-i}$ counts the other p-values above $\lambda$. The argument used for BH then bounds the contribution of $H_i$ to the FDR by $q(1 - \lambda)E[1/(1 + W_{-i})]$. Finally $W_{-i}$ is at least a binomial count with $m_0 - 1$ trials and success probability $1 - \lambda$, and $E[1/(1 + B)] = (1 - \lambda^{m_0})/(m_0(1 - \lambda))$ for such a count $B$. Summing over the $m_0$ true nulls gives $(1 - \lambda^{m_0})q$. The proof page also shows that the lines compute the q-values of the definition, and that rejecting $\hat q_i \le q$ is BH at level $q/\hat\pi_0$. The asymptotic control of the plain version is only cited.

The tests check what can be checked:

- the q-values against a brute force from the definition, a minimum over all thresholds, in exact rational arithmetic;
- the STS rule against a brute force that finds the supremum threshold from its definition;
- the rule $\hat q_i \le q$ against BH at $q/\hat\pi_0$;
- the bound $(1 - \lambda^{m_0})q$ exactly for $2 \le m \le 4$, by summing over all values of independent null p-values uniform on $\{1/10, \dots, 1\}$, with $\lambda = 1/2$ and $q = 1/5$;
- by Monte Carlo with $m = 40$, $m_0 = 20$, independent normal statistics with mean 3 for the false nulls, $q = 0.1$ and 2000 runs: the FDR is 0.049 for BH (the theory gives 0.05), 0.100 for STS and 0.112 for the plain q-value rule, and the average power is 0.911, 0.956 and 0.962.

The last line shows the trade-off: the adaptive methods gain power by spending the slack of BH, and the plain version slightly overspends in finite samples.

## Complexity

Counting $W$ takes $\Theta(m)$, the sort at line L3 takes $\Theta(m\log m)$ on a [real RAM](/real-ram/), and the running minimum $\Theta(m)$. So the time is $\Theta(m\log m)$ and the extra space $\Theta(m)$. The rejections at one level need no sort, as for BH. Choosing $\lambda$ by a smoother over a grid of $g$ values adds $O(gm)$, or $O(m\log m + g)$ with the sorted p-values; choosing it by the bootstrap with $B$ resamples adds $O(Bgm)$.

## Properties

- **Finite-sample FDR control** for the modified procedure, under independent valid null p-values, at $(1 - \lambda^{m_0})q$. Proved.
- **Asymptotic FDR control** for the plain procedure under weak dependence. Cited.
- **More powerful than BH** whenever $\hat\pi_0 < 1$, since its thresholds are $1/\hat\pi_0$ times larger. When nearly all nulls are true, $\hat\pi_0$ is near 1 and the methods agree.
- **q-values are monotone in the p-values**, by the running minimum.
- **Bayesian meaning.** Under the two-groups model with independent tests and nested rejection regions, the positive FDR of the region $\{p \le t\}$ is $P(H \text{ null} \mid p \le t)$, so the q-value is a posterior probability of a tail, as the tail-area Fdr in the [local false discovery rate](/local-false-discovery-rate/) page is (Storey 2003).

## Variants and improvements

- **Choosing $\lambda$.** Storey and Tibshirani (2003) fit a cubic spline to $\hat\pi_0(\lambda)$ over a grid of $\lambda$ and take its value near $\lambda = 1$, where the bias is smallest. Storey (2002) chooses $\lambda$ to minimize a [bootstrap](/bootstrap-method/) estimate of the mean squared error of $\hat\pi_0$.
- **Other adaptive procedures.** Benjamini, Krieger and Yekutieli (2006) estimate $m_0$ in a first BH pass and run a second pass with it. Their two-stage procedure also controls the FDR under independence.
- **pFDR q-values.** Storey (2002) also defines q-values for the positive FDR, dividing by the estimated $P(R > 0) = 1 - (1 - t)^m$; the version on this page, without that factor, is the common default.
- **Local fdr.** The estimate of $\pi_0$ is the same idea as Efron's zero assumption for the [local false discovery rate](/local-false-discovery-rate/), which gives a posterior probability for each test instead of a tail.
- **Arbitrary dependence.** No adaptive method on this page covers it. Under unknown dependence use [Benjamini-Yekutieli](/benjamini-yekutieli-procedure/), which gives up the factor $m_0/m$ and more.

## When to use it

Use q-values when many hypotheses are tested, a fair share of them are expected to be false, the tests are independent or weakly dependent, and the p-values are continuous and well calibrated. Genome-wide expression studies are the typical case, which is where the method became standard. When $m$ is small, use the modified STS version, which has the finite-sample guarantee. When the null p-values may not be uniform, for example when they are discrete or when the null distribution is misspecified, check the histogram of the p-values first: $\hat\pi_0$ assumes a flat histogram for the nulls.

## Pitfalls

- **A U-shaped or bumpy histogram near 1.** Conservative tests give null p-values piled near 1 and inflate $\hat\pi_0$; anti-conservative or misspecified tests deflate it and void the control.
- **Discrete p-values.** Many p-values equal to 1, as with sparse count data, push $\hat\pi_0$ up. It stays conservative but the gain over BH can vanish or reverse.
- **Reading the q-value as a probability for one test.** The q-value is an FDR for the set of tests at least as significant, not the probability that this test is null. That is the [local fdr](/local-false-discovery-rate/), which is larger at the boundary.
- **Using $\hat\pi_0$ capped at 1 in the finite-sample proof.** The guarantee is for $\hat\pi_0^*$ with the added 1 and the limit $t \le \lambda$; the plain capped estimator is only asymptotically valid.
- **Strong dependence.** With positively correlated tests, $W$ varies much more than under independence, and $\hat\pi_0$ can be far too small in some data sets.

## Implementations

## History

Benjamini and Hochberg (1995) noted that their procedure is conservative by the factor $m_0/m$, and Benjamini and Hochberg (2000) proposed an adaptive version with an estimate of $m_0$, without a proof of control. Storey (2002) took the other view, estimating the FDR of a fixed rejection region with $\hat\pi_0(\lambda)$, and defined the pFDR and the q-value; Storey (2003) gave the Bayesian interpretation. Storey and Tibshirani (2003) made the q-value the standard summary for genome-wide studies. Storey, Taylor and Siegmund (2004) showed that thresholding the estimate is BH with $m$ replaced by $\hat\pi_0m$, and proved finite-sample control for the modified estimator and asymptotic control for the plain one.

## References
