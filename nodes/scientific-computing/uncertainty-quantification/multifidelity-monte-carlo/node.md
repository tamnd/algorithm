---
tag: SQG1XP
kind: algorithm
slug: multifidelity-monte-carlo
name: Multifidelity Monte Carlo
area: scientific-computing/uncertainty-quantification
level: research
summary: Combines a high fidelity model with cheaper surrogates as control variates, choosing sample sizes to minimize the variance at a fixed cost.
solves: [forward-uncertainty-propagation]
model: real-ram
complexity:
  vars: {p: the budget in units of model cost, k: the number of models, N: the number of draws of the random input (the count of the cheapest model)}
  time: {worst: O(p + k N)}
  space: {extra: O(N)}
properties: {deterministic: false, randomized: true, exact: false, iterative: false}
history:
  year: 2016
  people: [Benjamin Peherstorfer, Karen Willcox, Max Gunzburger]
  note: Peherstorfer, Willcox and Gunzburger gave the estimator with nested samples, the optimal sample counts and weights, and the conditions on the models in 2016.
prereqs: [monte-carlo-integration, forward-uncertainty-propagation]
see_also: [multilevel-monte-carlo, monte-carlo-integration, reduced-basis-method, pod-galerkin-reduced-model, gaussian-process, polynomial-chaos-expansion, mlmc-complexity-theorem, variance]
sources:
  - paper: doi:10.1137/15M1046472
    title: Benjamin Peherstorfer, Karen Willcox and Max Gunzburger, Optimal model management for multifidelity Monte Carlo estimation, SIAM Journal on Scientific Computing 38(5), 2016, A3163-A3194
    locator: Section 3 (the estimator, its variance, the optimal sample counts and weights, and the conditions on correlations and costs)
  - paper: doi:10.1137/16M1082469
    title: Benjamin Peherstorfer, Karen Willcox and Max Gunzburger, Survey of multifidelity methods in uncertainty propagation, inference, and optimization, SIAM Review 60(3), 2018, 550-591
    locator: the section on multifidelity uncertainty propagation by control variates
---

Multifidelity Monte Carlo (MFMC) estimates the mean of the output of an expensive high fidelity model, with the help of cheaper models of the same output, such as a coarse mesh, a reduced model or a data fit. The cheap models are control variates: their sample means over many inputs correct the noisy sample mean of the expensive model over a few of the same inputs. The estimate stays unbiased for the mean of the expensive model, whatever the cheap models are. Their quality changes only the variance, and the method picks the number of runs of each model and the weights of the corrections to make the variance as small as possible for a fixed total cost. Unlike [multilevel Monte Carlo](/multilevel-monte-carlo/), it needs no hierarchy of levels and no rates, only the correlation of each cheap model with the expensive one and its cost.

## In plain words

You have one slow, trusted model and some fast models that are only roughly right. You want the average output of the slow model over random inputs.

Run the slow model a few times and average. That average is noisy. Now run a fast model on the same inputs and also on many more inputs. If the fast model goes up when the slow one goes up, the gap between its average on the few inputs and on the many inputs tells you how lucky or unlucky the few inputs were. Use that gap to correct the slow average. A good fast model removes most of the noise, and a bad one removes little, but the correction never shifts the answer on average. The method works out how many runs to give each model for the money you have.

## The problem

The input is a high fidelity model $f_1$ and cheaper models $f_2, \ldots, f_k$, all functions of the same random input $z$, the costs $w_1, \ldots, w_k$ of one run of each, and a budget $p$. The output is an estimate $\widehat{s}$ of $\mathbb{E}[f_1(z)]$ with cost $\sum_i w_i m_i = p$ and the smallest variance. Here $m_i$ is the number of runs of model $i$. Let $\sigma_i^2 = \mathrm{Var}(f_i(z))$ and $\rho_i = \mathrm{Corr}(f_1(z), f_i(z))$, with $\rho_1 = 1$ and $\rho_{k+1} = 0$.

The estimator uses nested draws $z_1, \ldots, z_{m_k}$ with $m_1 \le m_2 \le \cdots \le m_k$, and $\bar{f}_i^{(m)}$ is the mean of $f_i$ over the first $m$ draws:

$$\widehat{s} = \bar{f}_1^{(m_1)} + \sum_{i=2}^{k} \alpha_i \big(\bar{f}_i^{(m_i)} - \bar{f}_i^{(m_{i-1})}\big).$$

The optimal counts and weights exist under two conditions on the models: $|\rho_1| > |\rho_2| > \cdots > |\rho_k|$, and each model is cheap enough for its correlation,

$$\frac{w_{i-1}}{w_i} > \frac{\rho_{i-1}^2 - \rho_i^2}{\rho_i^2 - \rho_{i+1}^2}, \qquad i = 2, \ldots, k.$$

## The algorithm

```pseudo id=main
MFMC(f_1..f_k, w_1..w_k, p, DRAW, n)
L1  σ_i, ρ_i ← sample standard deviations and correlations with f_1, from n pilot draws
L2  if |ρ_i| does not decrease, or w_(i-1)/w_i ≤ (ρ_(i-1)^2 - ρ_i^2)/(ρ_i^2 - ρ_(i+1)^2) for some i, then stop
L3  r_i ← sqrt(w_1 (ρ_i^2 - ρ_(i+1)^2) / (w_i (1 - ρ_2^2)))  for i = 1..k     ▷ r_1 = 1, ρ_(k+1) = 0
L4  m_1 ← p / (w_1 r_1 + ... + w_k r_k);  m_i ← m_1 r_i, rounded down and kept in order
L5  α_i ← ρ_i σ_1 / σ_i  for i = 2..k
L6  draw z_1, ..., z_(m_k) by DRAW
L7  s ← mean of f_1(z_1), ..., f_1(z_(m_1))
L8  for i = 2..k: s ← s + α_i (mean of f_i over z_1..z_(m_i) - mean of f_i over z_1..z_(m_(i-1)))
L9  return s
```

Line L1 is the only step that needs runs of all models on the same inputs; the pilot draws are separate from the draws of line L6. Line L2 tests the two conditions; if they fail, drop or reorder a model and start again. Lines L3 and L4 give the counts: model $i$ gets $r_i$ times as many runs as model 1, and the budget fixes $m_1$. Line L5 is the best weight of a control variate. In lines L7 and L8, the second mean of a correction is over the first $m_{i-1}$ draws of the same list, so the two means of a correction are strongly correlated and their difference is small.

## Example

Let $z$ be uniform on $[0, 1]$, $f_1(z) = e^z$, $f_2(z) = 1 + z + z^2/2$ and $f_3(z) = 1 + z$, the exponential and two of its Taylor polynomials. The costs are $w = (1, 0.01, 0.001)$ and the budget is $p = 100$. The exact statistics, from $\mathbb{E}[f_1] = e - 1$, $\mathrm{Cov}(f_1, f_2) = (2 - e/2)/3$ and $\mathrm{Cov}(f_1, f_3) = (3 - e)/2$, are:

| model $i$ | mean | $\sigma_i$ | $\rho_i$ | $w_i$ |
|---|---|---|---|---|
| 1 | 1.71828 | 0.4919711 | 1 | 1 |
| 2 | 5/3 | 0.4346135 | 0.9990758 | 0.01 |
| 3 | 1.5 | 0.2886751 | 0.9918268 | 0.001 |

Line L2: the cost ratios are $100 > 0.128$ and $10 > 0.01467$, so the conditions hold. Lines L3 to L5 then give:

| model $i$ | $r_i$ | $m_i$ | $\alpha_i$ | cost $w_i m_i$ |
|---|---|---|---|---|
| 1 | 1 | 49.771 | 1 | 49.77 |
| 2 | 27.9495 | 1391.08 | 1.130928 | 13.91 |
| 3 | 729.703 | 36318.1 | 1.690309 | 36.32 |

The variance of $\widehat{s}$ is $1.805 \times 10^{-5}$. Plain Monte Carlo with the same budget runs $f_1$ 100 times and has the variance $\sigma_1^2/100 = 0.00242$, 134 times as large. More than a third of the budget goes to the cheapest model, because it is very cheap and still has $\rho_3^2 = 0.984$.

## Correctness

The claim has two parts. First, $\widehat{s}$ is unbiased for $\mathbb{E}[f_1]$ for every choice of counts and weights, because each correction is a difference of two sample means of the same model. Second, with the true $\sigma_i$ and $\rho_i$ and under the conditions of line L2, the counts and weights of lines L3 to L5 minimize the variance among all choices with cost $p$. The key step is the variance formula

$$\mathrm{Var}(\widehat{s}) = \sigma_1^2 \sum_{i=1}^{k} \frac{\rho_i^2 - \rho_{i+1}^2}{m_i}$$

at the best weights, which uses that the covariance of two nested means is the covariance of one draw over the larger count. The Cauchy-Schwarz inequality with the cost constraint then gives $m_i \propto \sqrt{(\rho_i^2 - \rho_{i+1}^2)/w_i}$, and the second condition is exactly what makes these counts increase with $i$, as nesting requires. The full proof is in the proof file. It does not cover the pilot: with estimated statistics the allocation is close to the optimum, not at it.

## Complexity

In the [real RAM](/real-ram/) model with a model run of cost $w_i$, lines L6 to L8 cost $\sum_i w_i m_i = p$ in model work, plus $O(m_i)$ additions for each model, which is $O(k N)$ with $N = m_k$. The pilot of line L1 costs $n \sum_i w_i$, outside the budget. Lines L2 to L5 cost $O(k)$. The list of draws takes $O(N)$ space; a version that draws each input once and adds it to all running sums needs $O(k)$.

The variance at the optimum is $\frac{\sigma_1^2}{p} \big(\sum_i \sqrt{w_i (\rho_i^2 - \rho_{i+1}^2)}\big)^2$, so the error falls like $p^{-1/2}$, as for plain Monte Carlo, with a smaller constant. The ratio of the two variances is $\big(\sum_i \sqrt{(w_i/w_1)(\rho_i^2 - \rho_{i+1}^2)}\big)^2$, which is 0.00746 in the example.

## Properties

- **Unbiased.** The mean of the estimate is the mean of the high fidelity model, for any cheap models. A bad cheap model costs efficiency, not accuracy.
- **Non-intrusive.** All models are black boxes on the same input. There is no need for levels, meshes or rates.
- **Optimal for its class.** Among estimators of this nested form with a fixed cost, the allocation is the best, given the true statistics.
- **Not always better than plain Monte Carlo.** The conditions of line L2 do not ensure a gain; the variance ratio must also be below 1.

## Variants and improvements

- **Multilevel Monte Carlo as a special case.** With levels of one discretization as the models and all weights $\alpha_i = 1$, the estimator is close to [multilevel Monte Carlo](/multilevel-monte-carlo/), which uses independent draws on each level instead of nested ones.
- **Approximate control variates.** Later work generalizes the sharing of draws between the models (for example, each cheap model compared with model 1 directly) and optimizes over these sample structures.
- **Model selection.** Run the allocation for every ordered subset of the cheap models and keep the subset with the smallest variance. With a few models this is cheap, because it uses only the pilot statistics.
- **Multifidelity for other statistics.** The same idea applies to variances, quantiles or [Sobol indices](/sobol-indices/), with the estimator of that statistic in place of the mean.

## When to use it

Use MFMC when one model is expensive and you have cheap models whose outputs are strongly correlated with it, but that do not form a sequence of levels with known rates: reduced models such as the [reduced basis method](/reduced-basis-method/) or a [POD-Galerkin reduced model](/pod-galerkin-reduced-model/), a [Gaussian process](/gaussian-process/) fit, or a simpler physics model. Use [multilevel Monte Carlo](/multilevel-monte-carlo/) when the models are discretization levels and the bias of the finest level must also go to zero. Use the cheap model alone only when its error against the expensive one is known to be small; MFMC does not need this, because the expensive model removes the bias. Use plain [Monte Carlo integration](/monte-carlo-integration/) when no cheap model has a correlation close to 1.

## Pitfalls

- **Independent draws in a correction.** If line L8 takes the second mean over new draws instead of the first $m_{i-1}$ of the same list, the two means are independent, the correction adds variance instead of removing it, and the estimate is worse than plain Monte Carlo. Nest the draws as in line L6.
- **Using the pilot runs in the estimate.** If the draws of line L1 are reused in lines L7 and L8, the weights depend on the samples and the estimate is slightly biased. Keep the pilot separate, or accept the bias knowingly.
- **Ordering by cost instead of correlation.** Line L2 needs the models in order of decreasing $|\rho_i|$. A cheap model with a higher correlation than a more expensive one must come first, or the counts of line L4 are not in order.
- **A weak cheap model.** With $\rho_2^2 = 0.01$ and $w_2 = w_1/100$, the conditions hold, but the variance ratio is 1.01, so the method loses to plain Monte Carlo. Check the ratio after line L4 and drop such a model.
- **Few pilot runs.** Line L1 with a few runs gives noisy correlations near 1, where the counts of line L3 are very sensitive to $\rho_i^2 - \rho_{i+1}^2$. Use enough pilot runs that these differences are clearly resolved.

## Implementations

## History

Control variates are an old variance reduction method of Monte Carlo simulation, in which a correlated variable with a known mean corrects a sample mean. Multifidelity methods replace the known mean by a cheap estimate from many runs of a cheap model. Peherstorfer, Willcox and Gunzburger gave the estimator with nested draws, the optimal counts and weights for any number of models, and the two conditions on correlations and costs in 2016, and surveyed multifidelity methods for uncertainty propagation, inference and optimization in 2018.

## References
