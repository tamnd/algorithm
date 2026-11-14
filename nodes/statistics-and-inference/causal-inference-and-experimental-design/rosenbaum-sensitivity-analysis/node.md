---
tag: 4KS2ZT
kind: technique
slug: rosenbaum-sensitivity-analysis
name: Rosenbaum sensitivity analysis
aliases:
- Rosenbaum bounds
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: Asks how strong an unmeasured confounder, measured by a bound Gamma on the odds of treatment in matched pairs, would have to be to explain away a finding.
prereqs: [propensity-score-matching, wilcoxon-signed-rank-test]
see_also: [ignorability, sign-test, mcnemar-test, binomial-test, permutation-test, p-value, inverse-probability-weighting, instrumental-variables-estimation]
sources:
  - paper: doi:10.1093/biomet/74.1.13
    title: Paul R. Rosenbaum, Sensitivity analysis for certain permutation inferences in matched observational studies, Biometrika 74(1), 1987
    locator: pp. 13 to 26 (the model with the bound Gamma and the bounds on the p-values of sign-score statistics)
  - book: isbn:9780387989679
    title: Paul R. Rosenbaum, Observational Studies, second edition, Springer, 2002
    locator: Chapter 4, Sensitivity to Hidden Bias, pp. 105 to 170 (the model, matched pairs, the signed-rank and McNemar bounds, and the smoking example)
  - paper: doi:10.1198/jasa.2009.tm08470
    title: Paul R. Rosenbaum and Jeffrey H. Silber, Amplification of sensitivity analysis in matched observational studies, Journal of the American Statistical Association 104(488), 2009
    locator: pp. 1398 to 1405 (Gamma written as a pair of effects on treatment and on outcome)
  - paper: doi:10.1093/jnci/22.1.173
    title: Jerome Cornfield, William Haenszel, E. Cuyler Hammond, Abraham M. Lilienfeld, Michael B. Shimkin and Ernst L. Wynder, Smoking and lung cancer, recent evidence and a discussion of some questions, Journal of the National Cancer Institute 22(1), 1959
    locator: the article starting on p. 173 (the first sensitivity argument for an unmeasured cause)
  - paper: doi:10.1093/jnci/32.5.1161
    title: E. Cuyler Hammond, Smoking in relation to mortality and morbidity, Journal of the National Cancer Institute 32(5), 1964
    locator: the article starting on p. 1161 (the matched smokers and nonsmokers of the example)
  - paper: doi:10.1111/j.2517-6161.1983.tb01242.x
    title: Paul R. Rosenbaum and Donald B. Rubin, Assessing sensitivity to an unobserved binary covariate in an observational study with binary outcome, Journal of the Royal Statistical Society Series B 45(2), 1983
    locator: pp. 212 to 218 (a sensitivity model with an explicit unobserved covariate)
  - book: isbn:9780521885881
    title: Guido W. Imbens and Donald B. Rubin, Causal Inference for Statistics, Social, and Biomedical Sciences, Cambridge University Press, 2015
    locator: Chapter 22 (sensitivity analysis and bounds), Section 22.5 on the Rosenbaum approach
---

Rosenbaum sensitivity analysis asks how much hidden bias would be needed to change the conclusion of a matched observational study. Matching on measured covariates, as in [propensity score matching](/propensity-score-matching/), removes only measured differences, and the test of no effect assumes [ignorability](/ignorability/): within a matched pair, each unit was equally likely to be the treated one. The analysis replaces this assumption by a weaker one. Two units in the same pair may differ in their odds of treatment by a factor of at most $\Gamma \ge 1$, because of a covariate nobody measured. For each $\Gamma$ it computes the smallest and the largest p-value that any such bias could produce. The value of $\Gamma$ at which the largest p-value crosses the level $\alpha$ is the *sensitivity value*: a measure of how strong the hidden bias would have to be to explain the finding away.

## In plain words

In a matched study, each smoker is paired with a nonsmoker who is alike in age, job and so on. If the pairs were truly alike, a coin toss decided which one of each pair smoked, and the usual test applies. But some unmeasured trait might make one person of the pair more likely to smoke.

So we ask: suppose that trait could make one person up to $\Gamma$ times more likely (in odds) to smoke than the other. In the worst case, how large could the p-value be? We try $\Gamma = 1, 2, 3, \ldots$ until the worst case is no longer significant. If a hidden trait would need to multiply the odds of smoking by 5 to explain the result, the result is hard to explain away. If 1.1 is enough, it is fragile.

## When it applies

- The data are matched pairs (or matched sets) from an observational study, with one treated and one control unit per pair, matched on the measured covariates.
- The test statistic is a sum over pairs of a nonnegative score times the indicator that the treated unit did better: the [signed-rank statistic](/wilcoxon-signed-rank-test/), the [sign test](/sign-test/), [McNemar's test](/mcnemar-test/) for binary outcomes, and others of the same form.
- The null hypothesis is Fisher's sharp null of no effect for any unit. Then the two responses of each pair are fixed numbers, and only the question of which unit was treated is random, as in a [permutation test](/permutation-test/).
- The question is how much unmeasured confounding the conclusion can bear. The analysis does not estimate the hidden bias; the data have no information about it.

## The template

**The model.** Let $\pi_j$ be the probability that unit $j$ is treated, and suppose $\log\frac{\pi_j}{1 - \pi_j} = \kappa(x_j) + \gamma u_j$, with an unmeasured $u_j \in [0, 1]$ and $\Gamma = e^\gamma \ge 1$. Two units $j, k$ with the same measured $x$ then have odds of treatment whose ratio is between $1/\Gamma$ and $\Gamma$. In a pair with exactly one treated unit, the chance that it is unit $j$ is
$$\frac{\pi_j(1 - \pi_k)}{\pi_j(1 - \pi_k) + \pi_k(1 - \pi_j)} = \frac{O_j}{O_j + O_k}, \qquad O = \frac{\pi}{1 - \pi},$$
and with $O_j/O_k \in [1/\Gamma, \Gamma]$ this lies in $\left[\frac{1}{1 + \Gamma}, \frac{\Gamma}{1 + \Gamma}\right]$. The pairs are independent. $\Gamma = 1$ is a [randomized experiment](/randomized-experiment/) within pairs.

**The bound.** Under the sharp null, the treated-minus-control difference $D_s$ of pair $s$ is $\pm$ a fixed number, so $|D_s|$ is fixed and only its sign is random. Take a statistic $T = \sum_s q_s\,[D_s > 0]$ with fixed scores $q_s \ge 0$ that depend only on the $|D_s|$. Let $T^+$ and $T^-$ be the same sum with independent signs, positive with probability $p^+ = \Gamma/(1 + \Gamma)$ and $p^- = 1/(1 + \Gamma)$. Then for every assignment law allowed by the model and every $t$,
$$\Pr[T^- \ge t] \le \Pr[T \ge t] \le \Pr[T^+ \ge t].$$
*Proof.* In pair $s$ the sign is positive with some probability $p_s \in [p^-, p^+]$, independently over pairs. Take independent uniforms $U_s$ and set the sign of pair $s$ positive when $U_s \le p_s$. Then $[U_s \le p^-] \le [U_s \le p_s] \le [U_s \le p^+]$ for each $s$, and $T$ is nondecreasing in each indicator because $q_s \ge 0$. So $T^- \le T \le T^+$ on every outcome of the uniforms, which gives the two inequalities. Both bounds are attained: by the law in which, in every pair, the unit with the larger response has the higher odds (for $T^+$) or the lower odds (for $T^-$) by the factor $\Gamma$. $\square$

The tests check both claims, by enumerating every vertex of $[p^-, p^+]^n$ and every assignment for small designs in exact arithmetic.

```pseudo id=main
ROSENBAUM-BOUNDS(D[1..S], Γ)                 ▷ pair differences, treated minus control
L1  drop the pairs with D_s = 0; let n be the number left
L2  q ← SCORES(|D_1|, ..., |D_n|)             ▷ hole: ranks, all ones, or another nonnegative score
L3  t ← Σ_{s : D_s > 0} q_s                    ▷ the observed statistic
L4  p⁺ ← Γ / (1 + Γ);  p⁻ ← 1 / (1 + Γ)
L5  law⁺ ← law of Σ_s B_s q_s, B_s ~ Bernoulli(p⁺) independent    ▷ a subset-sum dynamic program
L6  law⁻ ← the same with p⁻
L7  return (Pr_{law⁻}[≥ t], Pr_{law⁺}[≥ t])    ▷ bounds on the one-sided p-value
SENSITIVITY-VALUE(D, α)
L8  find by bisection the Γ ≥ 1 at which the upper bound of L7 equals α
```

The holes are SCORES, the level $\alpha$, and the grid of $\Gamma$ values to report. Line L5 is the dynamic program of the [signed-rank test](/wilcoxon-signed-rank-test/) with weights $p^+$ and $1 - p^+$ in place of $1/2$: for each score, $\mathrm{law}[v] \leftarrow (1 - p)\,\mathrm{law}[v] + p\,\mathrm{law}[v - q_s]$, scanning $v$ downward. With ranks doubled to keep midranks integral, it takes $\Theta(n \cdot \sum_s q_s) = \Theta(n^3)$ operations. For large $n$ the normal approximation uses the mean $p^+\sum_s q_s$ and the variance $p^+(1 - p^+)\sum_s q_s^2$. The upper bound is nondecreasing in $\Gamma$, by the same coupling, so the bisection in line L8 is valid. For a two-sided test, double the one-sided bound in the direction of the observed effect.

## Classic examples

- **Smoking and lung cancer, binary outcome.** Hammond (1964) matched 36,975 heavy smokers to nonsmokers. In 122 pairs exactly one man died of lung cancer, and in 110 of them it was the smoker. With all scores 1, $T$ is McNemar's count of 110 out of 122 discordant pairs, and the bounds are binomial tails: $\Pr[\mathrm{Bin}(122, p^+) \ge 110]$. At $\Gamma = 1$ this is below $10^{-20}$; at $\Gamma = 5$ the exact upper bound is 0.0232, and at $\Gamma = 6$ it is 0.0969. The exact sensitivity value at $\alpha = 0.05$ is about 5.47. An unmeasured trait would have to raise the odds of smoking more than five-fold, and nearly decide who dies, to explain the result. (Published analyses quote 0.03 at $\Gamma = 5$ and 0.10 at $\Gamma = 6$, which match the normal approximation with a continuity correction.)
- **Signed ranks, continuous outcome.** Take the ten pair differences of the [signed-rank test](/wilcoxon-signed-rank-test/) example: $1.8, -0.6, 3.1, 2.4, -1.3, 0.9, 2.2, 0.0, 1.5, -0.4$. The zero is dropped, $n = 9$ and $W^+ = 38$. At $\Gamma = 1$ both bounds are $19/512 = 0.0371$, the exact one-sided Wilcoxon p-value. At $\Gamma = 1.5$ the p-value can be anywhere in $[0.0101, 0.1034]$, and at $\Gamma = 2$ in $[0.0034, 0.1821]$. The sensitivity value at $\alpha = 0.05$ is about 1.11: a small hidden bias could explain this finding.
- **The sign test.** With all scores 1 on continuous differences, the bound is a binomial tail, as for the [sign test](/sign-test/) and the [binomial test](/binomial-test/). On the ten differences above, 6 of 9 nonzero signs are positive, and the bound at $\Gamma = 1$ is already $130/512 \approx 0.254$, because the sign test ignores that the three negative differences are small. Different scores give different sensitivity values for the same data, so choose the score before the analysis.
- **Cornfield's argument.** Cornfield and coauthors (1959) argued that a hidden cause that explains a risk ratio of 9 for smoking and lung cancer must be at least 9 times more common in smokers. This was the first sensitivity analysis, and Rosenbaum's model makes it a statement about p-values in a matched design.

## Variations

- **Amplification.** Rosenbaum and Silber (2009) write $\Gamma$ as a pair $(\Lambda, \Delta)$: an unmeasured $u$ that raises the odds of treatment by $\Lambda$ and the odds of a positive pair difference by $\Delta$ has the same worst case as $\Gamma = (\Lambda\Delta + 1)/(\Lambda + \Delta)$. For example, $\Gamma = 5$ corresponds to $\Lambda = \Delta \approx 9.9$. This answers the objection that the worst case assumes $u$ predicts the outcome perfectly.
- **Matched sets and strata.** With one treated unit and several controls per set, or several treated units, the bounds are no longer two simple Bernoulli laws. Rosenbaum's book gives bounds and a normal approximation that uses the extreme allocation in each set.
- **Point estimates and intervals.** Inverting the test for each shift $\tau_0$ in $D_s - \tau_0$ gives, for each $\Gamma$, an interval of Hodges-Lehmann estimates and a [confidence interval](/confidence-interval/) that widens as $\Gamma$ grows.
- **Explicit covariate models.** Rosenbaum and Rubin (1983) model a binary unobserved covariate with given effects on treatment and outcome, and report the estimate for each choice. Bounds for weighting estimators, such as the marginal sensitivity model for [inverse probability weighting](/inverse-probability-weighting/), use the same idea of a bounded odds ratio.

## Pitfalls

- **Reading $\Gamma$ as a probability.** $\Gamma$ is a bound on an odds ratio within pairs, not the chance that a confounder exists. A sensitivity value of 5.47 says what the bias would need to be, not how likely it is.
- **Reading the upper bound as the p-value.** The true p-value is somewhere between the two bounds. The upper bound is attained only if the hidden trait both shifts the odds of treatment by the full factor $\Gamma$ in every pair and lines up perfectly with which unit had the larger response.
- **A large study is not a robust study.** Sample size moves the p-value at $\Gamma = 1$, but the sensitivity value is limited by the size and the consistency of the effect. Two studies with the same tiny p-value can have very different sensitivity values.
- **Only the sharp null.** The bounds are for the hypothesis of no effect for every unit. They say nothing directly about the size of the effect without the inversion described above.
- **The normal approximation.** For the ten pairs of the example, at $\Gamma = 2$ the exact upper bound is 0.182 and the normal approximation without a continuity correction gives 0.157; at $\Gamma = 3$ the numbers are 0.331 and 0.280. The approximation can err in either direction; compute the exact law when $n$ is small. These are measured values.
- **Bias from measured covariates.** The model assumes that matching removed all measured differences. Pairs with poor matches on $x$ add bias that the analysis attributes to $u$.
- **Choosing the score after seeing the data.** Trying the sign test, the signed-rank test and others, and reporting the one with the largest sensitivity value, overstates robustness.

## Exercises

1. Show that if $O_j/O_k \in [1/\Gamma, \Gamma]$, then $O_j/(O_j + O_k) \in [1/(1 + \Gamma), \Gamma/(1 + \Gamma)]$, and that both ends are reached.
2. For 10 discordant pairs with 9 events in the treated unit, compute the upper bound of the one-sided p-value at $\Gamma = 1$ and $\Gamma = 2$ by hand.
   <details><summary>Answer</summary>At $\Gamma = 1$: $11/1024 \approx 0.0107$. At $\Gamma = 2$, with $p^+ = 2/3$: $(10 \cdot 2^9 + 2^{10})/3^{10} = 6144/59049 \approx 0.104$.</details>
3. Explain why the bound $\Pr[T \ge t] \le \Pr[T^+ \ge t]$ needs every score $q_s$ to be nonnegative, and give a statistic with a negative score for which it fails.
4. Use the code to find the sensitivity value at $\alpha = 0.10$ for the ten differences of the example. (It is about 1.48.)

## References
