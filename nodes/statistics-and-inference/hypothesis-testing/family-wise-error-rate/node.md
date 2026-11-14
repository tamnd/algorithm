---
tag: ND6ZTJ
kind: definition
slug: family-wise-error-rate
name: Family-wise error rate
aliases:
- FWER
- familywise error rate
area: statistics-and-inference/hypothesis-testing
level: core
summary: The probability of at least one false rejection among a family of tests. Strong control bounds it under every configuration of true and false nulls.
prereqs: [type-i-and-type-ii-errors, multiple-comparisons-problem]
see_also: [false-discovery-rate, bonferroni-correction, holm-bonferroni-method, hochberg-procedure, closed-testing-principle, westfall-young-procedure, union-bound, tukey-hsd]
sources:
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Chapter 9, Section 9.1 (introduction and the FWER, with weak and strong control)
  - paper: doi:10.1214/ss/1056397487
    title: Sandrine Dudoit, Juliet Popper Shaffer and Jennifer C. Boldrick, Multiple hypothesis testing in microarray experiments, Statistical Science 18(1) (2003), pages 71 to 103
    locator: the section on type I error rates (per-comparison, per-family, family-wise, false discovery rate; weak and strong control)
  - paper: doi:10.1093/biomet/63.3.655
    title: Ruth Marcus, Eric Peritz and K. R. Gabriel, On closed testing procedures with special reference to ordered analysis of variance, Biometrika 63(3) (1976), pages 655 to 660
    locator: the requirement that the probability of rejecting any true hypothesis be at most alpha whatever the true hypotheses are
---

The family-wise error rate (FWER) of a multiple testing procedure is the probability that it rejects at least one true null hypothesis. It is the direct extension of the [type I error](/type-i-and-type-ii-errors/) of one test to a family of $m$ tests, and it is the error rate controlled by the [Bonferroni correction](/bonferroni-correction/), [Holm's method](/holm-bonferroni-method/) and every [closed testing](/closed-testing-principle/) procedure. A procedure controls it weakly when the bound holds only if all the nulls are true, and strongly when it holds whatever the set of true nulls is. Only strong control justifies claims about single hypotheses. Without correction, the FWER grows quickly with $m$: for $m$ independent tests at level $\alpha$ with all nulls true, it is $1 - (1 - \alpha)^m$.

## Definition

**Setting.** A family of null hypotheses $H_1, \dots, H_m$ about the distribution $P$ of the data. For each $P$, $I_0(P) = \{i : H_i \text{ is true under } P\}$ is the set of true nulls, with $m_0 = |I_0(P)|$ elements. A multiple testing procedure maps the data to a set $\mathcal R$ of rejected indices. The counts are

| | not rejected | rejected | total |
|---|---|---|---|
| true nulls | $U$ | $V$ | $m_0$ |
| false nulls | $T$ | $S$ | $m - m_0$ |
| total | $m - R$ | $R$ | $m$ |

so $V = |\mathcal R \cap I_0(P)|$ is the number of false rejections and $R = |\mathcal R|$ the number of rejections.

**Family-wise error rate.** $\text{FWER}(P) = P(V \ge 1)$, the probability of rejecting at least one true null. If $m_0 = 0$, then $V = 0$ and $\text{FWER}(P) = 0$.

**Weak control at level $\alpha$.** $\text{FWER}(P) \le \alpha$ for every $P$ under which all $m$ nulls are true, the global null. Under the global null, $V = R$, so weak control is the statement that the procedure, used as one test of the global null, has level $\alpha$.

**Strong control at level $\alpha$.** $\text{FWER}(P) \le \alpha$ for every $P$, whatever $I_0(P)$ is. Strong control implies weak control. It means that, with probability at least $1 - \alpha$, every rejected hypothesis is false, so each rejection can be reported as a finding.

The control is exact (in finite samples) when the bound holds for every sample size under the stated model, and asymptotic when $\limsup_{n \to \infty}\text{FWER}(P) \le \alpha$. A page about a procedure states which, and under which dependence between the tests.

## Examples and non-examples

**No correction, independent tests.** Test each $H_i$ at level $\alpha$ with independent tests, each of size exactly $\alpha$. Then $V$ is the number of successes among $m_0$ independent trials with probability $\alpha$, so $\text{FWER} = 1 - (1 - \alpha)^{m_0}$. Under the global null this is $1 - (1 - \alpha)^m$. At $\alpha = 0.05$ it is 0.05 for $m = 1$, 0.2262 for $m = 5$, 0.4013 for $m = 10$, 0.6415 for $m = 20$ and 0.9941 for $m = 100$. The expected number of false rejections is $m_0\alpha$, which is 5 for 100 true nulls.

**No correction, identical tests.** If all $m$ tests are the same test, $V \ge 1$ exactly when that test rejects, and the FWER is $\alpha$. In general, for tests of size $\alpha$ under the global null, $\alpha \le \text{FWER} \le \min(1, m\alpha)$. The upper bound is the [union bound](/union-bound/); it is attained when the rejection events are disjoint.

**Bonferroni.** Testing each hypothesis at $\alpha/m$ gives $\text{FWER} \le m_0\alpha/m \le \alpha$ for every $P$, by the union bound. This is strong control under arbitrary dependence; the [Bonferroni correction](/bonferroni-correction/) page proves it.

**Weak but not strong control.** First test the global null with the Bonferroni rule $\min_i p_i \le \alpha/m$. If it is rejected, reject every $H_i$ with $p_i \le \alpha$, with no further correction. Under the global null the second step only happens when the first one rejects, so the FWER is at most $\alpha$: the control is weak. But let $H_1$ be false with $p_1$ close to 0, and $H_2, \dots, H_m$ true with independent uniform p-values. The first step then rejects with probability close to 1, and the second step tests $m - 1$ true nulls at $\alpha$ each, so the FWER is close to $1 - (1 - \alpha)^{m-1}$, which is 0.37 for $m = 10$. Fisher's protected least significant difference method for pairwise comparisons of means has this two-stage form.

**Not a FWER statement.** "Each of the 20 tests has a 5% false positive rate" is a statement about each test, the per-comparison error rate. It implies nothing better than $\text{FWER} \le 1$ for the family.

**Simultaneous confidence intervals.** For intervals $C_1, \dots, C_m$ for parameters $\theta_1, \dots, \theta_m$, the analogue of strong FWER control is simultaneous coverage, $P(\theta_i \in C_i \text{ for all } i) \ge 1 - \alpha$. Testing $\theta_i = \theta_{i,0}$ by checking whether $\theta_{i,0} \in C_i$ then controls the FWER strongly, as in [Tukey's HSD](/tukey-hsd/) for pairwise differences.

## Related definitions

- **Per-comparison error rate.** $E[V]/m$, the expected fraction of the tests that are false rejections. Testing each hypothesis at $\alpha$ controls it at $\alpha$.
- **Per-family error rate.** $E[V]$, the expected number of false rejections. Since $\mathbf 1\{V \ge 1\} \le V$, $\text{FWER} \le E[V]$, so controlling $E[V]$ at $\alpha$ controls the FWER. Bonferroni controls both.
- **$k$-FWER.** $P(V \ge k)$, the probability of $k$ or more false rejections. It allows a few errors in large families; the case $k = 1$ is the FWER.
- **False discovery rate.** $E[V/\max(R, 1)]$, the expected proportion of false rejections among the rejections. It is never larger than the FWER, and equal to it under the global null. See [false discovery rate](/false-discovery-rate/).
- **False discovery proportion.** $V/\max(R, 1)$ itself, a random variable; procedures that bound $P(V/\max(R, 1) > \gamma)$ control its tail.
- **Type I error.** For $m = 1$, the FWER is the probability of a [type I error](/type-i-and-type-ii-errors/), and weak and strong control are the same.

## References
