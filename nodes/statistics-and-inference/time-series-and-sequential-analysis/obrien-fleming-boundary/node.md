---
tag: C11SHN
kind: algorithm
slug: obrien-fleming-boundary
name: O'Brien-Fleming boundary
aliases:
- O'Brien-Fleming stopping rule
area: statistics-and-inference/time-series-and-sequential-analysis
level: advanced
summary: The group sequential boundary c_k = C sqrt(K/k), very strict at early looks and near the fixed-sample value at the last. C comes from recursive integration and bisection.
model: real-ram
complexity:
  vars: {K: "the number of analyses", m: "the number of quadrature points per analysis", B: "the number of bisection steps on C"}
  time: {worst: O(B K m^2)}
  space: {extra: O(m)}
properties: {deterministic: true, online: false, recursive: false, exact_up_to_quadrature: true}
history:
  year: 1979
  people: [Peter C. O'Brien, Thomas R. Fleming]
  note: O'Brien and Fleming proposed the boundary in Biometrics in 1979, two years after Pocock's constant boundary. Armitage, McPherson and Rowe had given the recursive integration that computes such boundaries in 1969.
prereqs: [group-sequential-design, numerical-integration]
see_also: [alpha-spending-function, sequential-probability-ratio-test, bisection-method, simpsons-rule, multiple-comparisons-problem, sample-size-determination, statistical-power, confidence-sequence]
sources:
  - paper: doi:10.2307/2530245
    title: Peter C. O'Brien and Thomas R. Fleming, A multiple testing procedure for clinical trials, Biometrics 35(3) (1979), pages 549 to 556
    locator: the definition of the boundary, with critical values proportional to the square root of K/k
  - paper: doi:10.1093/biomet/64.2.191
    title: Stuart J. Pocock, Group sequential methods in the design and analysis of clinical trials, Biometrika 64(2) (1977), pages 191 to 199
    locator: the constant boundary and its table of critical values for equally spaced analyses
  - paper: doi:10.2307/2343787
    title: P. Armitage, C. K. McPherson and B. C. Rowe, Repeated significance tests on accumulating data, Journal of the Royal Statistical Society, Series A 132(2) (1969)
    locator: the recursive numerical integration of the probability of crossing a boundary for sums of normal variables
  - paper: doi:10.2307/2531959
    title: Samuel K. Wang and Anastasios A. Tsiatis, Approximately optimal one-parameter boundaries for group sequential trials, Biometrics 43(1) (1987)
    locator: the family of boundaries proportional to (k/K) to the power Delta minus 1/2, which contains the O'Brien-Fleming and Pocock shapes
  - book: isbn:9780849303166
    title: Christopher Jennison and Bruce W. Turnbull, Group Sequential Methods with Applications to Clinical Trials, Chapman and Hall/CRC, 2000
    locator: Chapter 2 (the Pocock and O'Brien-Fleming tests, their constants and their inflation factors)
  - paper: doi:10.1093/biomet/70.3.659
    title: K. K. Gordon Lan and David L. DeMets, Discrete sequential boundaries for clinical trials, Biometrika 70(3) (1983), pages 659 to 663
    locator: the spending function that approximates the O'Brien-Fleming boundary for analyses at times not fixed in advance
---

The O'Brien-Fleming boundary is the most used stopping rule for a two-sided [group sequential design](/group-sequential-design/). With $K$ analyses at information levels $I_1 < \cdots < I_K$, it rejects $H_0: \theta = 0$ at the first analysis $k$ with $|Z_k| \ge c_k$, where
$$c_k = C\sqrt{I_K/I_k},$$
which is $C\sqrt{K/k}$ for equally spaced analyses. Early critical values are very large, and the last one is only a little above the fixed-sample value: for $K = 5$ and $\alpha = 0.05$ they are 4.56, 3.23, 2.63, 2.28 and 2.04. The constant $C$ is the solution of $P_0(\text{some } |Z_k| \ge c_k) = \alpha$. The algorithm below computes this probability by recursive [numerical integration](/numerical-integration/) over the canonical joint distribution of the $Z_k$, and finds $C$ by [bisection](/bisection-method/). O'Brien and Fleming proposed the boundary in 1979; Pocock's constant boundary, from 1977, is the main alternative and is described under Variants.

## In plain words

A trial will look at its data five times. At each look, a score measures the evidence that the treatment works. If the score crosses a line, the trial stops. The O'Brien-Fleming rule sets the lines so that early looks need overwhelming evidence and the last look needs about the usual amount. So a trial stops early only when the result is striking, and a trial that runs to the end is judged almost as if there had been no early looks. The algorithm finds the height of the lines. It tries a height, computes the chance of a false stop at any look when the treatment does nothing, and adjusts the height up or down until that chance is exactly the planned 5%.

## The problem

**Input.** The number of analyses $K$, the information levels $0 < I_1 < \cdots < I_K$ (or only their ratios), and the two-sided level $\alpha \in (0, 1)$.

**Model.** Under $H_0$, the scores $S_k = Z_k\sqrt{I_k}$ satisfy $S_0 = 0$ and have independent increments $S_k - S_{k-1} \sim N(0, I_k - I_{k-1})$, with $I_0 = 0$. This is the canonical joint distribution of the [group sequential design](/group-sequential-design/) page; it is exact for normal data with known variance and holds approximately for most large-sample statistics.

**Output.** The constant $C$ such that
$$P_0\bigl(|Z_k| \ge C\sqrt{I_K/I_k} \text{ for some } k \le K\bigr) = \alpha,$$
and the critical values $c_k = C\sqrt{I_K/I_k}$. On the score scale the boundary is flat: $|Z_k| \ge c_k$ means $|S_k| \ge C\sqrt{I_K}$.

## The algorithm

```pseudo id=main
OBRIEN-FLEMING(K, α, I_1, ..., I_K)
L1  lo ← z_{1-α/2},  hi ← z_{1-α/(2K)}               ▷ the root lies in [lo, hi]
L2  while hi - lo > tol do
L3      C ← (lo + hi)/2
L4      if CROSS(C, I) > α then lo ← C else hi ← C
L5  return C and c_k = C·sqrt(I_K / I_k) for k = 1..K

CROSS(C, I_1, ..., I_K)                              ▷ P_0(|S_k| ≥ C·sqrt(I_K) for some k)
L6  b ← C·sqrt(I_K)
L7  p ← 2Φ̄(b / sqrt(I_1));  g ← density of N(0, I_1) on [-b, b]
L8  for k ← 2 to K do
L9      σ ← sqrt(I_k - I_{k-1})
L10     p ← p + ∫_{-b}^{b} g(u)[Φ((-b - u)/σ) + Φ̄((b - u)/σ)] du
L11     g(s) ← ∫_{-b}^{b} g(u) φ((s - u)/σ)/σ du  for |s| < b
L12 return p
```

**Lines L6 to L12.** The function $g$ is the sub-density of $S_k$ on the event that no earlier analysis crossed; its total mass is the probability of reaching analysis $k + 1$. Line L7 handles the first analysis: it crosses with probability $2\bar\Phi(b/\sqrt{I_1})$, and the rest of the $N(0, I_1)$ density, restricted to $[-b, b]$, carries on. Line L10 adds the probability of crossing first at analysis $k$: from a position $u$ inside the boundary, the next score is $u$ plus an independent $N(0, \sigma^2)$ step. Line L11 moves the sub-density one step forward by convolution with that step and drops the part outside $[-b, b]$. This is the recursion of Armitage, McPherson and Rowe (1969).

**Lines L1 to L5.** The crossing probability decreases as $C$ grows. At $C = z_{1-\alpha/2}$ the last analysis alone crosses with probability $\alpha$, so the total is at least $\alpha$. At $C = z_{1-\alpha/(2K)}$ every $c_k \ge C$, so each analysis crosses with probability at most $\alpha/K$ and the total is at most $\alpha$. Bisection keeps the root inside $[lo, hi]$ and halves the interval each step.

**Quadrature.** The implementation evaluates the integrals of lines L10 and L11 by [Simpson's rule](/simpsons-rule/) on a grid over $[-b, b]$ with spacing at most $\sigma/16$. Doubling the grid changes the crossing probability by less than $10^{-7}$ in the examples below.

## Example

Take $K = 5$ equally spaced analyses, $I_k = k$, and $\alpha = 0.05$. Then $lo = 1.95996$ and $hi = z_{0.995} = 2.57583$. The first bisection steps are:

| step | $C$ | CROSS$(C)$ | new interval |
|---|---|---|---|
| 1 | 2.2679 | 0.02755 | $[1.9600, 2.2679]$ |
| 2 | 2.1139 | 0.04141 | $[1.9600, 2.1139]$ |
| 3 | 2.0369 | 0.05040 | $[2.0369, 2.1139]$ |
| 4 | 2.0754 | 0.04571 | $[2.0369, 2.0754]$ |
| 5 | 2.0562 | 0.04800 | $[2.0369, 2.0562]$ |
| 6 | 2.0466 | 0.04919 | $[2.0369, 2.0466]$ |

It converges to $C = 2.0401$. The critical values and their parts of $\alpha$ are:

| analysis $k$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $c_k = 2.0401\sqrt{5/k}$ | 4.5617 | 3.2256 | 2.6337 | 2.2809 | 2.0401 |
| nominal two-sided p-value of $c_k$ | 0.000005 | 0.00126 | 0.00845 | 0.02256 | 0.04134 |
| $P_0(\text{first crossing at } k)$ | 0.00001 | 0.00125 | 0.00764 | 0.01668 | 0.02442 |

The last critical value 2.040 corresponds to a nominal p-value of 0.041, so almost all of the 0.05 is still available at the end. With the plain value 1.96 at all five analyses, CROSS gives 0.061 for this shape, and 0.142 for a flat line at 1.96.

The constant for other numbers of analyses, equally spaced, $\alpha = 0.05$ two-sided:

| $K$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| O'Brien-Fleming $C$ | 1.9600 | 1.9774 | 2.0040 | 2.0243 | 2.0401 |
| Pocock constant | 1.9600 | 2.1783 | 2.2895 | 2.3613 | 2.4132 |

For $K = 2$ the boundary is $(2.7965, 1.9774)$: each tail of the first analysis has probability 0.00258 and each tail of the second has first-crossing probability 0.02242.

**Sample size.** With 90% power, the maximum information must be $R = 1.0265$ times the fixed-sample information $(z_{0.975} + z_{0.9})^2/\delta^2 = 10.507/\delta^2$ for $K = 5$. The expected information at stopping is 0.750 of the fixed-sample information when $\theta = \delta$, 0.961 when $\theta = \delta/2$ and 1.019 when $\theta = 0$.

## Correctness

The proof is in full below. In outline:

1. **The recursion is exact.** By induction on $k$, the function $g$ after line L11 at step $k$ is the sub-density of $S_k$ on the event that no analysis $j \le k$ crossed. The induction step is the Chapman-Kolmogorov identity for the independent normal increment. So the value returned by line L12 is $\sum_k P_0(\text{first crossing at } k) = P_0(\text{some } |S_k| \ge b)$, before quadrature.
2. **Monotone in $C$.** If $C < C'$, the event "some $|S_k| \ge C'\sqrt{I_K}$" is contained in the event "some $|S_k| \ge C\sqrt{I_K}$", and the difference contains the event $C\sqrt{I_K} \le |S_K| < C'\sqrt{I_K}$ with no earlier crossing, which has positive probability. So CROSS is strictly decreasing. It is also continuous, because each $|S_k|$ has a continuous distribution.
3. **The bracket.** CROSS$(z_{1-\alpha/2}) \ge P_0(|Z_K| \ge z_{1-\alpha/2}) = \alpha$ and, by the union bound, CROSS$(z_{1-\alpha/(2K)}) \le \sum_k P_0(|Z_k| \ge z_{1-\alpha/(2K)}) = \alpha$, since $c_k \ge C$ for all $k$.
4. **Bisection.** By 2 and 3 there is exactly one root in $[lo, hi]$, and each step of lines L3 and L4 keeps it inside. After $B$ steps the interval has width $(hi - lo)/2^B$.

The only approximation is the quadrature in lines L10 and L11; its error is $O(h^4)$ in the grid spacing $h$ for the smooth parts of the integrands.

## Complexity

One evaluation of CROSS on $m$ grid points per analysis costs $O(m^2)$ for the convolution of line L11 and $O(m)$ for line L10, so $O(Km^2)$ in all. With grid spacing $\sigma/r$ and $b = C\sqrt{I_K}$, $m = O(r\,C\sqrt{I_K/(I_k - I_{k-1})})$, which is $O(r\sqrt K)$ for equally spaced analyses. Bisection to width $\varepsilon$ needs $B = \lceil \log_2((hi - lo)/\varepsilon) \rceil$ evaluations, so the total time is $O(BKm^2)$ and the extra space is $O(m)$ for two grids. For $K = 5$, $r = 16$ and $\varepsilon = 10^{-9}$, this is about 30 evaluations of a few thousand grid operations each.

## Properties

- **Flat on the score scale.** The rule is $|S_k| \ge C\sqrt{I_K}$: the same bound on the sum at every analysis. This is why it spends so little error early, when the variance of $S_k$ is small.
- **Last critical value near $z_{1-\alpha/2}$.** $C$ grows slowly with $K$, from 1.960 to 2.040 for $K = 5$. So the final analysis loses little power against the fixed-sample test.
- **Small inflation.** The maximum information is only 2.7% above the fixed-sample one for $K = 5$ and 90% power.
- **Dependence on the information levels.** $C$ depends on the ratios $I_k/I_K$. If the analyses do not occur at the planned levels, the boundary must be recomputed, or the [alpha spending function](/alpha-spending-function/) approach used instead.
- **A trade-off, not an optimum.** Pocock's shape gives a smaller expected sample size when the effect is as large as planned. The O'Brien-Fleming shape gives a smaller maximum, and a smaller expected sample size when there is no effect.

## Variants and improvements

**Pocock boundary.** Pocock (1977) uses the same critical value $c_k = C_P$ at every analysis. For $K = 5$ and $\alpha = 0.05$, $C_P = 2.4132$. Compared with the O'Brien-Fleming boundary:

| $K = 5$, $\alpha = 0.05$, power 90% | O'Brien-Fleming | Pocock |
|---|---|---|
| critical values | 4.562, 3.226, 2.634, 2.281, 2.040 | 2.413 at every analysis |
| $P_0$ of first crossing at analyses 1 to 5 | 0.00001, 0.00125, 0.00764, 0.01668, 0.02442 | 0.01581, 0.01171, 0.00902, 0.00731, 0.00615 |
| inflation factor $R$ | 1.0265 | 1.2065 |
| expected information, $\theta = \delta$ | 0.750 | 0.685 |
| expected information, $\theta = \delta/2$ | 0.961 | 1.052 |
| expected information, $\theta = 0$ | 1.019 | 1.177 |

The Pocock design stops sooner when the effect is as planned, but its maximum sample size is 21% larger, and a trial that reaches the last analysis needs $|Z_5| \ge 2.413$, a nominal p-value of 0.016. The same bisection computes it, with $c_k = C$ and the general crossing routine.

Other variants:

- **Wang-Tsiatis family.** $c_k = C(I_k/I_K)^{\Delta - 1/2}$ with $0 \le \Delta \le 1/2$. $\Delta = 0$ is O'Brien-Fleming and $\Delta = 1/2$ is Pocock. Wang and Tsiatis (1987) searched this family for boundaries with a small expected sample size.
- **Spending-function version.** Lan and DeMets (1983) give the spending function $2 - 2\Phi(z_{1-\alpha/2}/\sqrt t)$, which produces boundaries close to O'Brien-Fleming for any times of analysis; see [alpha spending function](/alpha-spending-function/).
- **One-sided boundary and futility.** For a one-sided test, line L7 and line L10 count only the upper crossing, and an inner futility boundary can be added; the recursion is the same with a different integration range.
- **Haybittle-Peto rule.** A fixed critical value of 3 at the interim analyses and the fixed-sample value at the end. It resembles O'Brien-Fleming but does not keep the level exactly.

## When to use it

Use the O'Brien-Fleming boundary for the efficacy analysis of a confirmatory trial with a few planned interim analyses, where early stopping should need overwhelming evidence and the final analysis should be almost unchanged. Use the Pocock boundary when early stopping for a large effect is the main goal and the larger maximum is acceptable. Use the [alpha spending function](/alpha-spending-function/) when the times of the analyses are uncertain, and a fully sequential method such as the [SPRT](/sequential-probability-ratio-test/) when the data are analysed after every observation.

## Pitfalls

- **Using 1.96 at the end.** The final critical value is $C$, not $z_{1-\alpha/2}$. A result with $1.96 \le |Z_K| < 2.040$ does not reject for $K = 5$.
- **Analyses at unplanned times.** The constant $C$ depends on the information ratios. Recompute it for the actual times, or use a spending function from the start.
- **Too coarse a quadrature.** With few grid points the recursion error can exceed the target accuracy of $C$, mostly at early analyses where the sub-density is narrow. Choose the spacing relative to $\sqrt{I_k - I_{k-1}}$, as the implementation does.
- **Normal approximation at the first analysis.** The first critical value 4.56 sits far in the tail, where large-sample approximations for binary or survival data are least accurate.
- **Bias after early stopping.** The estimate at an early stop is biased away from 0; report a repeated confidence interval or an adjusted estimate.

## Implementations

## History

Armitage, McPherson and Rowe (1969) showed how much repeated significance tests inflate the type I error and computed the inflation by recursive numerical integration. Pocock (1977) turned this into practical group sequential designs with a constant critical value. O'Brien and Fleming (1979) proposed critical values proportional to $\sqrt{K/k}$, so that early stopping needs very strong evidence; this shape became the standard for efficacy monitoring. Lan and DeMets (1983) gave the spending function that approximates it at analysis times not fixed in advance, and Wang and Tsiatis (1987) placed both boundaries in a one-parameter family.

## References
