---
tag: 575F6X
kind: definition
slug: false-discovery-rate
name: False discovery rate
area: statistics-and-inference/hypothesis-testing
level: core
summary: The expected proportion of false rejections among all rejections, taken as zero when there are none. It is less strict and more powerful to control than the FWER.
prereqs: [family-wise-error-rate, p-value]
see_also: [benjamini-hochberg-procedure, benjamini-yekutieli-procedure, storey-q-value, local-false-discovery-rate, knockoff-filter, multiple-comparisons-problem, empirical-bayes, e-variable]
sources:
  - paper: doi:10.1111/j.2517-6161.1995.tb02031.x
    title: Yoav Benjamini and Yosef Hochberg, Controlling the false discovery rate, a practical and powerful approach to multiple testing, Journal of the Royal Statistical Society, Series B 57(1) (1995), pages 289 to 300
    locator: the definition of the false discovery rate as the expected value of V / R, set to 0 when R = 0, and its relation to the family-wise error rate
  - paper: doi:10.1214/aos/1074290335
    title: John D. Storey, The positive false discovery rate, a Bayesian interpretation and the q-value, The Annals of Statistics 31(6) (2003), pages 2013 to 2035
    locator: the positive FDR E[V / R | R > 0] and its equality with a posterior probability under the mixture model with independent tests
  - book: isbn:9780521192491
    title: Bradley Efron, Large-Scale Inference, Empirical Bayes Methods for Estimation, Testing, and Prediction, Cambridge University Press, 2010
    locator: Chapter 2 (large-scale hypothesis testing and the Bayesian Fdr) and Chapter 4 (false discovery rate control)
---

The false discovery rate (FDR) is the expected fraction of false rejections among all rejections of a multiple testing procedure, with the fraction set to 0 when nothing is rejected. Benjamini and Hochberg defined it in 1995 for studies with many hypotheses, where a few false rejections among many true ones are acceptable but their proportion should be small. It is never larger than the [family-wise error rate](/family-wise-error-rate/), and it equals it when all the nulls are true, so controlling the FDR also controls the FWER weakly. When many nulls are false the FDR can be much smaller than the FWER, which is why procedures that control it, such as the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/), reject many more hypotheses than [Bonferroni](/bonferroni-correction/) or [Holm](/holm-bonferroni-method/).

## Definition

**Setting.** Hypotheses $H_1, \dots, H_m$, a procedure that rejects a set of them, and for the true distribution $P$ the set $I_0$ of true nulls with $m_0$ elements. $R$ is the number of rejections and $V$ the number of rejected true nulls, as in the table on the [FWER](/family-wise-error-rate/) page.

**False discovery proportion.** The random variable
$$Q = \frac{V}{\max(R, 1)} = \begin{cases} V/R & \text{if } R \ge 1, \\ 0 & \text{if } R = 0. \end{cases}$$

**False discovery rate.** $\text{FDR}(P) = E_P[Q]$. A procedure controls the FDR at level $q$ when $\text{FDR}(P) \le q$ for every $P$ in the model; the level is written $q$, not $\alpha$, to keep it apart from FWER levels. As with the FWER, a page about a procedure states the dependence under which the control holds and whether it is exact in finite samples or asymptotic. For example, Benjamini-Hochberg gives $\text{FDR} = (m_0/m)q$ exactly for independent continuous p-values, so its level is $(m_0/m)q$, not $q$.

**Proposition (FDR and FWER).** For every procedure and every $P$, $\text{FDR}(P) \le \text{FWER}(P)$. If all $m$ nulls are true under $P$, then $\text{FDR}(P) = \text{FWER}(P)$.

*Proof.* We show $Q \le \mathbf 1\{V \ge 1\}$ pointwise. If $V = 0$, then $Q = 0$. If $V \ge 1$, then $R \ge V \ge 1$, so $Q = V/R \le 1$. Taking expectations, $\text{FDR} = E[Q] \le P(V \ge 1) = \text{FWER}$. If all nulls are true, every rejection is false, so $V = R$. Then $Q = 1$ when $R \ge 1$ and $Q = 0$ when $R = 0$, that is, $Q = \mathbf 1\{V \ge 1\}$, and the expectations are equal. $\square$

So FDR control at $q$ implies weak FWER control at $q$: under the global null the two rates are the same number. It does not imply strong FWER control. When some nulls are false, $Q$ is strictly less than $\mathbf 1\{V \ge 1\}$ whenever $1 \le V < R$, and the gap can be large.

## Examples and non-examples

**Two hypotheses.** Let $H_1$ be false with $p_1 = 0$, always rejected, and $H_2$ true with $p_2$ uniform, rejected when $p_2 \le \alpha$. Then $V = \mathbf 1\{p_2 \le \alpha\}$ and $R = 1 + V$, so $Q = 1/2$ when $p_2 \le \alpha$ and $Q = 0$ otherwise. The FWER is $\alpha$ and the FDR is $\alpha/2$.

**Many discoveries.** If a procedure always rejects the $m - m_0$ false nulls and, with probability $\alpha$, one true null as well, then the FWER is $\alpha$ and the FDR is $\alpha/(m - m_0 + 1)$. With 99 real effects found, one false one adds only 1% to the proportion. This is the regime in which FDR control is useful: the proportion matters, not the existence of one error.

**Benjamini-Hochberg.** For independent continuous p-values, the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/) at level $q$ has $\text{FDR} = (m_0/m)q$ exactly, for every configuration of the false nulls. Under the global null this is $q$, and by the proposition the procedure then has FWER $q$ too; it is the Simes test of the global null.

**Not a bound on one experiment.** FDR control is a statement about the mean of $Q$ over repetitions. In one experiment the proportion of false discoveries can be far above $q$. With $m = m_0$ and $q = 0.05$, Benjamini-Hochberg rejects nothing 95% of the time, but when it rejects anything every rejection is false, so $Q = 1$ on that event. Bounds of the form $P(Q > \gamma) \le \alpha$ control the tail of $Q$ instead, which is a different error rate.

**Not the posterior probability of the null for one hypothesis.** The FDR is an average over all rejected hypotheses. The hypotheses rejected near the boundary have a much higher chance of being null than the average; the [local false discovery rate](/local-false-discovery-rate/) measures that chance for each one.

## Related definitions

- **Positive FDR.** $\text{pFDR} = E[V/R \mid R > 0]$, from Storey (2002, 2003). It equals $\text{FDR}/P(R > 0)$. Under the global null it is 1 for any procedure that rejects with positive probability, so it cannot be controlled at $q < 1$ in that case, but it has a Bayesian meaning: when the $m$ tests are independent, identical and use the same rejection region $\Gamma$, and each null is true with prior probability $\pi_0$, $\text{pFDR}(\Gamma) = P(H \text{ null} \mid p \in \Gamma)$.
- **Marginal FDR.** $E[V]/E[R]$, a ratio of means. It is close to the FDR and the pFDR when $m$ is large and $R$ is concentrated, but it is a different quantity.
- **Bayesian Fdr.** In the two-groups model, Efron's tail-area $\text{Fdr}(z) = \pi_0F_0(z)/F(z)$ is the posterior probability that a case with statistic at most $z$ is null. See [local false discovery rate](/local-false-discovery-rate/).
- **q-value.** The smallest estimated FDR (or pFDR) at which a hypothesis is rejected, the FDR analogue of an adjusted p-value. See [Storey's q-value method](/storey-q-value/).
- **False discovery exceedance.** $P(Q > \gamma)$ for a tolerance $\gamma$; controlling it bounds the proportion in one experiment with high probability.
- **Family-wise error rate.** $P(V \ge 1)$. See [family-wise error rate](/family-wise-error-rate/).
- **Power analogues.** The average power $E[S]/(m - m_0)$, with $S = R - V$, and the false non-discovery rate $E[T/\max(m - R, 1)]$, the expected proportion of false nulls among the accepted hypotheses.

## References
