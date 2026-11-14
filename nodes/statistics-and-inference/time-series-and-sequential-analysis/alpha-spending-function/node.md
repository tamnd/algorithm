---
tag: 9MKH4V
kind: technique
slug: alpha-spending-function
name: Alpha spending function
aliases:
- Lan-DeMets alpha spending
- error spending function
area: statistics-and-inference/time-series-and-sequential-analysis
level: advanced
summary: Lan and DeMets's rule that spends the type I error as a function of the information fraction, so the timing and number of interim looks need not be fixed in advance.
prereqs: [group-sequential-design]
see_also: [obrien-fleming-boundary, sequential-probability-ratio-test, mixture-sequential-probability-ratio-test, confidence-sequence, family-wise-error-rate, bonferroni-correction, numerical-integration, bisection-method]
sources:
  - paper: doi:10.1093/biomet/70.3.659
    title: K. K. Gordon Lan and David L. DeMets, Discrete sequential boundaries for clinical trials, Biometrika 70(3) (1983), pages 659 to 663
    locator: the definition of the spending function, the computation of the boundaries from it, and the spending functions that approximate the O'Brien-Fleming and Pocock boundaries
  - paper: doi:10.1093/biomet/74.1.149
    title: Kyungmann Kim and David L. DeMets, Design and analysis of group sequential tests based on the type I error spending rate function, Biometrika 74(1) (1987)
    locator: the power family of spending functions alpha t^rho
  - paper: doi:10.1002/sim.4780091207
    title: Irving K. Hwang, Weichung J. Shih and John S. De Cani, Group sequential designs using a family of type I error probability spending functions, Statistics in Medicine 9(12) (1990)
    locator: the one-parameter family alpha (1 - e^(-gamma t)) / (1 - e^(-gamma))
  - paper: doi:10.2307/2343787
    title: P. Armitage, C. K. McPherson and B. C. Rowe, Repeated significance tests on accumulating data, Journal of the Royal Statistical Society, Series A 132(2) (1969)
    locator: the recursive numerical integration of the crossing probabilities
  - book: isbn:9780849303166
    title: Christopher Jennison and Bruce W. Turnbull, Group Sequential Methods with Applications to Clinical Trials, Chapman and Hall/CRC, 2000
    locator: the chapter on the error spending approach
---

An alpha spending function $f$ describes how a [group sequential design](/group-sequential-design/) uses its type I error over the course of a study. It maps the information fraction $t \in [0, 1]$, the share of the planned maximum information observed so far, to the error spent up to that point, with $f(0) = 0$ and $f(1) = \alpha$. When an analysis happens at fraction $t_k$, its critical value $c_k$ is chosen so that the probability under $H_0$ of crossing first at this analysis is exactly $f(t_k) - f(t_{k-1})$. Lan and DeMets introduced the method in 1983. Its value is flexibility: the number and the times of the analyses need not be fixed in advance, and the overall type I error is still $f(1) = \alpha$, as long as the times do not depend on the observed effect. The choice of $f$ sets the shape: some functions give boundaries close to the [O'Brien-Fleming boundary](/obrien-fleming-boundary/), others give boundaries close to Pocock's.

## In plain words

Think of the allowed false positive rate as a budget, for example 5%. Each look at the data spends some of it. A spending function is a plan, written before the study, that says how much of the budget may be used by each point of the study, measured by the share of the data collected. Early looks spend little, so they need very strong evidence to stop. When a look actually happens, you check how far the study is, see how much budget the plan allows by then, and spend the difference since the last look. You can look more often or less often than you expected. As long as the plan stays the same, the total spent cannot exceed the budget.

## When it applies

- A study with interim analyses whose number or timing is not known in advance, for example because a data monitoring committee meets on calendar dates while patients enter the trial at an uneven rate.
- The test statistics have the canonical joint distribution of a [group sequential design](/group-sequential-design/): the score $S_k = Z_k\sqrt{t_k}$, on the information fraction scale, is a Brownian motion with drift $\theta\sqrt{I_{\max}}$ observed at the times $t_1 < t_2 < \cdots$.
- The maximum information $I_{\max}$ can be planned, so the information fraction $t_k = I_k/I_{\max}$ is known at each analysis.
- The times $t_k$ are chosen without looking at the estimated effect. They may depend on calendar time, on recruitment, or on the previous decisions to continue.

## The template

Fix the spending function $f$ and the two-sided level $\alpha = f(1)$. Under $H_0$, $S_k = Z_k\sqrt{t_k}$ has independent increments $S_k - S_{k-1} \sim N(0, t_k - t_{k-1})$. Let $\sigma_k = \sqrt{t_k - t_{k-1}}$ and $b_k = c_k\sqrt{t_k}$. At analysis $k$ the procedure needs only $t_1, \ldots, t_k$.

```pseudo id=main
SPENDING-BOUNDARIES(f, t_1 < t_2 < ... < t_K)       ▷ 0 < t_1, t_K ≤ 1, f increasing
L1  c_1 ← z_{1 - f(t_1)/2};  g ← density of N(0, t_1), restricted to |s| < c_1·sqrt(t_1)
L2  for k ← 2 to K do
L3      π_k ← f(t_k) - f(t_{k-1})                        ▷ the error to spend now
L4      c_k ← the root c of ∫ g(u)[Φ̄((c·sqrt(t_k) - u)/σ_k) + Φ((-c·sqrt(t_k) - u)/σ_k)] du = π_k, by bisection
L5      g ← ∫ g(u) φ((s - u)/σ_k)/σ_k du,  restricted to |s| < c_k·sqrt(t_k)
L6  return c_1, ..., c_K
```

The function $g$ in line L1 and line L5 is the sub-density of $S_k$ on the event that the boundary was not crossed at analyses $1, \ldots, k$. Its total mass is the probability of reaching analysis $k + 1$. The integral in line L4 is the probability of crossing first at analysis $k$ with critical value $c$; it is the recursion of Armitage, McPherson and Rowe (1969) from the [group sequential design](/group-sequential-design/) page. The implementation evaluates the integrals by Simpson's rule on a grid ([numerical integration](/numerical-integration/)) and solves line L4 by [bisection](/bisection-method/).

**Why the total is $\alpha$.** Let $A_k$ be the event that the test crosses first at analysis $k$. Line L1 gives $P_0(A_1) = P_0(|Z_1| \ge c_1) = f(t_1)$. Line L4 gives $P_0(A_k) = f(t_k) - f(t_{k-1})$ for $k \ge 2$. The events are disjoint, so
$$P_0\Bigl(\bigcup_{k \le K} A_k\Bigr) = f(t_1) + \sum_{k=2}^K \bigl(f(t_k) - f(t_{k-1})\bigr) = f(t_K) \le f(1) = \alpha,$$
with equality when the last analysis is at $t_K = 1$. Nothing in this sum depends on $K$ or on the values $t_k$; that is the whole point of the method.

**Why line L4 has exactly one root.** Let $q_k$ be the total mass of $g$ before line L4, the probability of reaching analysis $k$. The crossing probability in line L4 is continuous and strictly decreasing in $c \ge 0$, from $q_k$ at $c = 0$ to 0 as $c \to \infty$. Since $q_k = 1 - f(t_{k-1}) > f(t_k) - f(t_{k-1}) = \pi_k > 0$ when $f(t_k) \le \alpha < 1$, there is exactly one root. If $f(t_k) = f(t_{k-1})$, no error is left to spend and $c_k = \infty$: the analysis cannot stop the study.

**Times that depend on the past.** The times may be chosen after the earlier analyses, as long as the choice uses only information that is independent of the effect estimates, or only the decisions to continue. The argument above conditions on the times, so it still holds. If the timing reacts to the observed effect, this argument does not apply and the level is no longer guaranteed.

**Cost.** With $m$ grid points per analysis and $B$ bisection steps, each analysis costs $O(m^2)$ for line L5 and $O(Bm)$ for line L4, so the whole set costs $O(K(m^2 + Bm))$ time and $O(m)$ space.

**Example: five equally spaced analyses, $\alpha = 0.05$ two-sided.** Lan and DeMets's O'Brien-Fleming type function is $f(t) = 2 - 2\Phi(z_{1-\alpha/2}/\sqrt t)$, which equals $\alpha$ at $t = 1$. Its cumulative spending at $t = 0.2, 0.4, 0.6, 0.8, 1$ is $0.000012$, $0.001942$, $0.011396$, $0.02843$ and $0.05$. The boundaries from the template are:

| spending function $f(t)$ | $c_1$ | $c_2$ | $c_3$ | $c_4$ | $c_5$ |
|---|---|---|---|---|---|
| O'Brien-Fleming type $2 - 2\Phi(z_{1-\alpha/2}/\sqrt t)$ | 4.3826 | 3.0997 | 2.5534 | 2.2538 | 2.0635 |
| same shape spent on each tail with $\alpha/2$ | 4.8769 | 3.3570 | 2.6803 | 2.2898 | 2.0310 |
| Pocock type $\alpha\log(1 + (e - 1)t)$ | 2.4380 | 2.4268 | 2.4102 | 2.3966 | 2.3860 |
| power $\alpha t$ ($\rho = 1$) | 2.5758 | 2.4920 | 2.4108 | 2.3391 | 2.2755 |
| power $\alpha t^3$ ($\rho = 3$) | 3.5401 | 2.9743 | 2.6045 | 2.3064 | 2.0455 |
| Hwang-Shih-DeCani, $\gamma = -4$ | 3.2527 | 2.9860 | 2.6917 | 2.3737 | 2.0253 |
| Hwang-Shih-DeCani, $\gamma = 1$ | 2.4487 | 2.4190 | 2.3984 | 2.3912 | 2.3948 |

For comparison, the exact O'Brien-Fleming boundary is 4.5617, 3.2256, 2.6337, 2.2809, 2.0401, and the exact Pocock boundary is 2.4132 at every analysis. The spending versions are close but not equal.

There are two conventions for the O'Brien-Fleming type function in a two-sided test, and they give different numbers. In the first row, the function is applied to the total two-sided $\alpha$, as in Lan and DeMets (1983). In the second row, which many software packages use, each tail spends $\alpha/2$ with the one-sided function $2 - 2\Phi(z_{1-\alpha/4}/\sqrt t)$, so the total is $f(t) = 4 - 4\Phi(z_{1-\alpha/4}/\sqrt t)$. The second convention spends less early and more late. A report must state which one it used.

**Example: the analyses happen at other times.** The study planned five analyses but the committee met only at $t = 0.3$, $0.7$ and $1$. With the O'Brien-Fleming type function on the total $\alpha$, the template gives 3.5784, 2.3454 and 2.0238, and the total error is still exactly 0.05.

## Classic examples

- **Approximating the O'Brien-Fleming design.** The function $2 - 2\Phi(z_{1-\alpha/2}/\sqrt t)$ gives boundaries close to the [O'Brien-Fleming boundary](/obrien-fleming-boundary/) for equally spaced analyses, and stays valid when the spacing changes. It is the most common choice in clinical trials.
- **Approximating the Pocock design.** $\alpha\log(1 + (e - 1)t)$ gives nearly constant boundaries close to Pocock's, as the table shows.
- **Flexible monitoring in a [group sequential design](/group-sequential-design/).** A data monitoring committee that meets every six months while recruitment speeds up computes each boundary at the meeting, from the information fraction at that time.
- **Linear spending and Bonferroni.** With $f(t) = \alpha t$ and $K$ equally spaced analyses, each analysis spends $\alpha/K$. A [Bonferroni correction](/bonferroni-correction/) would also test each analysis at $\alpha/K$, but the spending boundaries are lower (2.58 down to 2.28 against $z_{1 - 0.005} = 2.58$ at every look), because they use the correlation of the statistics. The [family-wise error rate](/family-wise-error-rate/) is exactly $\alpha$ for the spending boundaries and below $\alpha$ for Bonferroni.
- **Continuous monitoring as a limit.** With very many analyses the boundary tends to a curved boundary for Brownian motion. For truly continuous monitoring without a planned maximum, the [mixture SPRT](/mixture-sequential-probability-ratio-test/) and [confidence sequences](/confidence-sequence/) are the matching tools.

## Variations

- **Families of spending functions.** Kim and DeMets (1987) use the power family $\alpha t^\rho$: $\rho = 1$ is close to Pocock, $\rho = 3$ is close to O'Brien-Fleming. Hwang, Shih and DeCani (1990) use $\alpha(1 - e^{-\gamma t})/(1 - e^{-\gamma})$: $\gamma = 1$ is close to Pocock, $\gamma = -4$ is close to O'Brien-Fleming, and $\gamma = 0$ means linear spending.
- **Beta spending.** A second function spends the type II error and gives a futility boundary. The two boundaries are found together, analysis by analysis.
- **One-sided designs.** For a one-sided test of level $\alpha$, line L1 uses $z_{1 - f(t_1)}$ and line L4 counts only the upper crossing.
- **Changing the maximum information.** If the final analysis falls above the planned $I_{\max}$, spend the rest of $\alpha$ at the final analysis, setting its fraction to 1. If the study ends early at $t_K < 1$, it can spend the rest of $\alpha$ there instead of only $f(t_K)$, as long as that decision does not depend on the observed effect.
- **Repeated confidence intervals.** The boundaries $c_k$ give the intervals $\hat\theta_k \pm c_k/\sqrt{I_k}$, which cover $\theta$ at all analyses together with probability $1 - \alpha$.

## Pitfalls

- **Choosing $f$ after seeing data.** The function must be fixed in the protocol. Switching to a less strict function after an interim result inflates the error.
- **Timing that reacts to the effect.** Calling an extra analysis because the last one looked promising breaks the assumption that the times are independent of the effect estimates.
- **Mixing conventions.** The two-sided O'Brien-Fleming type function has two conventions, as the example shows. Software defaults differ, so record the convention and the resulting boundaries.
- **Information fraction in survival trials.** Information is the number of events, not the number of patients. Use the observed number of events divided by the planned number, or the fraction will be wrong.
- **Overrunning.** Data that arrive after the decision to stop, for example patients already treated, change the final statistic. The plan should say how they enter the final analysis.

## Exercises

1. Show that $f(t) = 2 - 2\Phi(z_{1-\alpha/2}/\sqrt t)$ is increasing on $(0, 1]$, tends to 0 as $t \to 0$ and equals $\alpha$ at $t = 1$. For $\alpha = 0.05$, compute $f(0.2)$ and explain why the first boundary in the example is above 4.
2. Prove that the crossing probability in line L4 is strictly decreasing in $c$ when $g$ has positive mass.
3. With $f(t) = \alpha t$ and two analyses at $t = 1/2$ and $1$, write the equation for $c_2$ as a bivariate normal probability with correlation $\sqrt{1/2}$.

## References
