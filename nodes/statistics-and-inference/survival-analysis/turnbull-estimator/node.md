---
tag: 0DBRMH
kind: algorithm
slug: turnbull-estimator
name: Turnbull estimator
aliases:
- Turnbull's self-consistency algorithm
- NPMLE for interval-censored data
area: statistics-and-inference/survival-analysis
level: advanced
summary: The nonparametric MLE of the distribution of interval-censored times, found by self-consistency iterations, an EM algorithm, over Turnbull's innermost intervals.
model: real-ram
complexity:
  vars: {n: the number of observations, m: the number of innermost intervals (m ≤ n), k: the number of iterations}
  time: {setup: Θ(n log n + n m), per_iteration: Θ(n m), per_iteration_prefix_sums: Θ(n + m), total: Θ(n log n + k n m)}
  space: {extra: Θ(n m), extra_prefix_sums: Θ(n + m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1976
  people: [Bruce W. Turnbull, Richard Peto]
  note: Peto (1973) defined the NPMLE for interval-censored data and computed it by constrained Newton-Raphson. Turnbull (1976) gave the innermost intervals and the self-consistency algorithm, also for truncated data.
prereqs: [kaplan-meier-estimator, censoring, expectation-maximization]
see_also: [isotonic-regression, pool-adjacent-violators, maximum-likelihood-estimation, empirical-distribution-function, survival-function, missing-data-mechanism, bootstrap-method, log-rank-test]
sources:
  - paper: doi:10.1111/j.2517-6161.1976.tb01597.x
    title: Bruce W. Turnbull, The empirical distribution function with arbitrarily grouped, censored and truncated data, Journal of the Royal Statistical Society Series B 38(3), 1976
    locator: pp. 290 to 295 (the innermost intervals, the self-consistency equations and the iteration, with truncation)
  - paper: doi:10.2307/2346307
    title: Richard Peto, Experimental survival curves for interval-censored data, Applied Statistics 22(1), 1973
    locator: pp. 86 to 91 (the NPMLE for interval-censored data and its support on the intervals between a left end and the next right end)
  - paper: doi:10.1093/biomet/81.3.618
    title: Robert Gentleman and Charles J. Geyer, Maximum likelihood for interval censored data, consistency and computation, Biometrika 81(3), 1994
    locator: pp. 618 to 623 (the Kuhn-Tucker conditions as a check of the computed NPMLE, and its uniqueness)
  - paper: doi:10.1214/aoms/1177728423
    title: Miriam Ayer, H. D. Brunk, G. M. Ewing, W. T. Reid and Edward Silverman, An empirical distribution function for sampling with incomplete information, Annals of Mathematical Statistics 26(4), 1955
    locator: pp. 641 to 647 (the NPMLE for current status data as a monotone regression)
  - book: isbn:9780387953991
    title: John P. Klein and Melvin L. Moeschberger, Survival Analysis, Techniques for Censored and Truncated Data, 2nd edition, Springer, 2003
    locator: Chapter 5 (estimation of the survival function for other sampling schemes, including Turnbull's algorithm for interval-censored data)
---

The Turnbull estimator is the nonparametric maximum likelihood estimate (NPMLE) of a distribution when each event time is known only to lie in an interval $(L_i, R_i]$. Such data arise when a condition is checked at clinic visits, so that an onset is known only to fall between the last negative and the first positive visit. Exact times ($L_i = R_i$) and right-censored times ($R_i = \infty$) are special cases, and on them the estimator is the [Kaplan-Meier estimator](/kaplan-meier-estimator/). The likelihood depends on the distribution only through the probabilities of a few disjoint sets, Turnbull's innermost intervals, and the masses on them are found by the self-consistency iteration $s_j \leftarrow s_j g_j$, which is the [EM algorithm](/expectation-maximization/) for this problem. The estimate of the [survival function](/survival-function/) is determined between the innermost intervals and undetermined inside them.

## In plain words

Each person's event happened somewhere inside a known window. We want the distribution of event times that makes these windows as likely as possible. Only a few places matter: the stretches where windows overlap as much as they can. The method starts with equal weight on each such stretch. Then, for each person, it splits that person between the stretches inside their window, in proportion to the current weights. Adding up these shares gives new weights. Repeating this never makes the fit worse, and it settles on the best weights. A simple test tells how far the current weights can still be from the best.

## The problem

**Input.** Observations $I_i = (L_i, R_i]$, $i = 1, \ldots, n$, with $0 \le L_i \le R_i \le \infty$, meaning that the event time $T_i$ satisfies $L_i < T_i \le R_i$. An exact time $t$ is $L_i = R_i = t$, read as the point $\{t\}$; a right censoring at $c$ is $(c, \infty]$; a left censoring at $c$ is $(0, c]$. The times $T_i$ are independent with distribution function $F$, and the inspection process that produces the intervals is independent of $T_i$ (non-informative interval censoring).

**Output.** A distribution $\hat F$ that maximizes the likelihood

$$\mathcal L(F) = \prod_{i=1}^n P_F(T \in I_i),$$

represented by disjoint sets $Q_1 < \cdots < Q_m$ and masses $s_j \ge 0$ with $\sum_j s_j = 1$, and the survival function $\hat S(t) = \sum_{j:\, Q_j > t} s_j$ at every $t$ outside the $Q_j$.

**Innermost intervals.** Sort the $2n$ endpoints; at equal values put the closed left ends of exact times first, then right ends, then open left ends. Each left end that is followed directly by a right end gives an innermost interval $Q_j$: $(p_j, q_j]$, or the point $\{p_j\}$ when it comes from an exact time. With $\alpha_{ij} = 1\{Q_j \subseteq I_i\}$ and $D_i(s) = \sum_j \alpha_{ij} s_j$, every maximizer of $\mathcal L$ can be moved into the $Q_j$ without loss, so the problem is the concave program

$$\max_{s \in \Delta_m} \ \ell(s) = \sum_{i=1}^n \log D_i(s), \qquad \Delta_m = \Big\{s \ge 0 : \sum_j s_j = 1\Big\}.$$

## The algorithm

```pseudo id=main
TURNBULL(L[1..n], R[1..n], ε)
L1  sort the 2n endpoints, at ties exact left ends, then right ends, then open left ends
L2  Q[1..m] ← the left ends followed directly by a right end, each paired with that right end
L3  α[i][j] ← 1 if Q[j] ⊆ I[i] else 0, for all i and j
L4  s[j] ← 1/m for all j
L5  repeat
L6      D[i] ← Σ_j α[i][j] s[j] for all i                 ▷ P(T ∈ I[i]) under s
L7      g[j] ← (1/n) Σ_i α[i][j] / D[i] for all j         ▷ ∂ℓ/∂s[j] divided by n
L8      if max_j g[j] ≤ 1 + ε then exit the loop
L9      s[j] ← s[j] g[j] for all j                        ▷ expected share of Q[j], divided by n
L10 return Q, s and ℓ = Σ_i log D[i]
```

Line L9 is the E step and the M step at once: $s_j \alpha_{ij}/D_i$ is the conditional probability that $T_i \in Q_j$ given $T_i \in I_i$, the sum over $i$ is the expected number of times in $Q_j$, and dividing by $n$ is the complete-data MLE. The new masses sum to 1 because $\sum_j s_j g_j = \frac1n \sum_i D_i/D_i = 1$; the code renormalizes with `math.fsum` against rounding drift. The stopping rule of line L8 certifies the result: $\ell(\hat s) - \ell(s) \le n(\max_j g_j - 1)$ for the maximizer $\hat s$, so the returned log-likelihood is within $n\varepsilon$ of the maximum. A second function returns the lower and upper value of $\hat S(t)$, which differ only for $t$ inside an innermost interval of positive width.

## Example

Six patients are checked for a condition at irregular visits. Two were negative at week 1 and positive at week 5, one negative at 2 and positive at 7, one had a known onset at week 3, one was negative at 3 and positive at 6, and one negative at 5 and positive at 6: $(1, 5], (1, 5], (2, 7], \{3\}, (3, 6], (5, 6]$.

Sorted endpoints, with $\mathrm L$ and $\mathrm R$ marking left and right ends: $1\mathrm L, 1\mathrm L, 2\mathrm L, 3\mathrm L_{\text{exact}}, 3\mathrm R, 3\mathrm L, 5\mathrm R, 5\mathrm R, 5\mathrm L, 6\mathrm R, 6\mathrm R, 7\mathrm R$. The adjacent pairs $\mathrm L\,\mathrm R$ give $Q_1 = \{3\}$, $Q_2 = (3, 5]$ and $Q_3 = (5, 6]$. Their inclusion pattern is:

| observation | $Q_1 = \{3\}$ | $Q_2 = (3, 5]$ | $Q_3 = (5, 6]$ |
|---|---|---|---|
| $(1, 5]$, twice | 1 | 1 | 0 |
| $(2, 7]$ | 1 | 1 | 1 |
| $\{3\}$ | 1 | 0 | 0 |
| $(3, 6]$ | 0 | 1 | 1 |
| $(5, 6]$ | 0 | 0 | 1 |

From $s = (1/3, 1/3, 1/3)$, the $D_i$ are $2/3, 2/3, 1, 1/3, 2/3, 1/3$, so $g_1 = \frac16(\frac32 + \frac32 + 1 + 3) = \frac76$ and $g_2 = g_3 = \frac{11}{12}$, and the first step gives $s = (7/18, 11/36, 11/36)$. The iteration converges to $\hat s = (1/2, 1/6, 1/3)$: at this point $D = (2/3, 2/3, 1, 1/2, 1/2, 1/3)$ and $g_1 = g_2 = g_3 = 1$, so the Kuhn-Tucker conditions hold and $\ell = 2\log\frac23 + 2\log\frac12 + \log\frac13 = -3.29584$. From the uniform start it took 77, 133 and 189 iterations to reach $\varepsilon = 10^{-6}$, $10^{-9}$ and $10^{-12}$: linear convergence, about 56 iterations per factor 1000.

The estimate is $\hat S(t) = 1$ for $t < 3$, $\hat S(3) = 1/2$, $\hat S(5) = 1/3$ and $\hat S(t) = 0$ for $t \ge 6$. For $3 < t < 5$ it is anywhere in $[1/3, 1/2]$, and for $5 < t < 6$ in $[0, 1/3]$: the data do not say how the mass is spread inside $(3, 5]$ and $(5, 6]$. No mass lies in $(1, 3)$, although three windows meet it, because each of them also contains $\{3\}$, where the exact time needs mass.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows that lines L1 and L2 find exactly the innermost intervals, and that for every point $x$ some innermost interval lies in every observation that contains $x$, so a maximizer of $\mathcal L$ exists with all its mass on the $Q_j$. It proves the Kuhn-Tucker characterization, $\hat s$ is optimal if and only if $g_j(\hat s) \le 1$ for all $j$ with equality where $\hat s_j > 0$, and the certificate $\ell(\hat s) - \ell(s) \le n(\max_j g_j(s) - 1)$ used by line L8. It shows that each step of line L9 increases $\ell$ by at least $n$ times the Kullback-Leibler divergence between the new and the old masses, and that from the uniform start $\ell(\hat s) - \ell(s^{(k)}) \le n \log m/(k + 1)$ after $k$ steps, so the loop ends. Finally, the values $D_i(\hat s)$ are the same for every maximizer.

## Complexity

The sort costs $\Theta(n \log n)$. A left end followed directly by a right end can occur at most $n$ times, so $m \le n$. Line L3 tests all pairs, $\Theta(nm)$, and lines L6 and L7 cost $\Theta(\sum_i \#\{j : Q_j \subseteq I_i\}) = O(nm)$ per iteration. Since the $Q_j$ are disjoint and ordered and each $I_i$ is an interval, the $Q_j$ inside $I_i$ form a contiguous run $a_i..b_i$ found by binary search. Then $D_i$ is a difference of prefix sums of $s$, and $g$ is a prefix sum of a difference array, so an iteration costs $\Theta(n + m)$. The number $k$ of iterations dominates the cost. The bound $n \log m/(k + 1)$ on the likelihood gap is proved, but the linear rate of the example is only observed, and it fails when a Kuhn-Tucker condition holds with equality at a zero mass. For the sets $(0, 2], (1, 3], (2, 4], (3, \infty]$ the maximizer is $(1/2, 0, 1/2)$ on $(1, 2], (2, 3], (3, 4]$ with $g_2 = 1$. There the middle mass decays like $1/k$: 998, 31620 and 999980 iterations to reach $\varepsilon = 10^{-6}$, $10^{-9}$ and $10^{-12}$.

Measured on simulated data with visits at weeks 1 to 4, each attended with probability 0.6, $T$ exponential with rate 0.5, and $\varepsilon = 10^{-8}$: the median number of iterations was 36 (maximum 3747) for $n = 50$, $r = 500$, seed 1978, and 31 (maximum 58) for $n = 200$, $r = 200$, seed 1979. Current status data (one inspection per subject) can be much slower: of 10 simulated current status data sets with $n$ between 5 and 30 (seed 1955), one with $n = 21$ needed 75444 iterations to reach $\varepsilon = 10^{-8}$, and the others at most 599.

## Properties

- **Reduces to Kaplan-Meier.** With only exact and right-censored times, the innermost intervals are the distinct event times plus the interval $(c, \infty]$ when the largest time $c$ is censored, and the NPMLE is the Kaplan-Meier estimator; its self-consistency equation is Efron's (1967).
- **Current status data.** When each subject is inspected once at $c_i$ and only $1\{T_i \le c_i\}$ is seen, the NPMLE of $F$ at the inspection times is the [isotonic regression](/isotonic-regression/) of the indicators, computed in $O(n)$ after sorting by [pool adjacent violators](/pool-adjacent-violators/) (Ayer et al. 1955).
- **Partly unique.** The probabilities $D_i(\hat s)$ of the observed sets are unique. The masses $s_j$ are unique under a rank condition on the matrix $\alpha$ (Gentleman and Geyer 1994), and the spread of each mass inside $Q_j$ is never identified.
- **Slow statistical rate.** Unlike Kaplan-Meier, the estimate is not $\sqrt n$-consistent in general. For current status data $\hat F(t)$ converges at rate $n^{1/3}$ with a non-normal limit (Groeneboom and Wellner 1992), so Greenwood-type standard errors do not apply. The [bootstrap](/bootstrap-method/) of the NPMLE is also unreliable in that case; inference on smooth functionals such as the mean is regular.
- **Not online, deterministic.** All intervals are needed before the innermost intervals are known.

Measured accuracy against the simple fix of replacing each interval by its midpoint and running Kaplan-Meier, for the visit design above, true $S(2) = e^{-1} = 0.3679$: the Turnbull estimate had bias $+0.0009$ and root mean square error $0.083$ at $n = 50$ ($r = 500$, seed 1978), and bias $-0.0001$, RMSE $0.040$ at $n = 200$ ($r = 200$, seed 1979). Midpoint imputation had bias $-0.034$ and $-0.032$, RMSE $0.079$ and $0.047$. Its bias does not shrink with $n$.

## Variants and improvements

- **Truncation.** Turnbull's paper also covers left-truncated data, where subject $i$ is observed only if $T_i$ lies in a set $J_i$. The self-consistency equations then include the expected number of unobserved subjects, the "ghosts", whose times fall outside $J_i$.
- **Iterative convex minorant and hybrid algorithms.** Groeneboom and Wellner (1992) maximize over the distribution function with the iterative convex minorant algorithm, which treats the monotonicity constraint directly. Wellner and Zhan (1997) alternate EM steps and ICM steps, which is much faster when EM is slow.
- **Support reduction and Kuhn-Tucker pruning.** Masses whose $g_j$ stays below 1 can be set to zero and the problem solved on the remaining support, then checked with the Kuhn-Tucker conditions.
- **Smooth and parametric alternatives.** A parametric model (Weibull or log-normal) fitted by [maximum likelihood](/maximum-likelihood-estimation/), or a spline or kernel-smoothed NPMLE, gives a unique curve inside the innermost intervals and $\sqrt n$ rates under its assumptions.
- **Bivariate and regression versions.** The same EM step works for two-dimensional intervals (rectangles), and the semiparametric proportional hazards model for interval-censored data has an NPMLE of the baseline with the same structure.

## When to use it

Use the Turnbull estimator for the survival curve whenever the event is detected at inspections rather than observed when it happens: onset of a disease found at screening visits, failure of equipment found at maintenance, seroconversion between blood tests. Report the estimate as steps over the innermost intervals, not as a continuous curve. For exact and right-censored data, Kaplan-Meier gives the same answer directly. Use the prefix-sum iteration or a hybrid EM-ICM solver for large $n$, and always check the Kuhn-Tucker gap.

## Pitfalls

- **Midpoint or right-endpoint imputation.** Treating each interval as an exact time at its midpoint or right end and running Kaplan-Meier gives a biased curve, as measured above; using the right end systematically delays the events.
- **Stopping on small changes.** EM can move very slowly, so a small change between iterations does not mean a near-optimal fit. Stop on the Kuhn-Tucker gap $\max_j g_j - 1$, which bounds the likelihood gap.
- **Reading the curve inside an innermost interval.** Any value between the two bounds is equally good. Plots that draw a straight line or a step at a chosen point inside $Q_j$ add information that the data do not contain.
- **Open and closed ends.** Whether a visit time belongs to the left or the right set changes the innermost intervals. With visits on a common schedule, use $(L_i, R_i]$ throughout, and represent an exact time as a point, not as $(t - \epsilon, t]$ with an arbitrary $\epsilon$.
- **Informative inspection.** If visits become more frequent after symptoms start, the inspection process depends on $T$, and the likelihood $\prod_i P(T \in I_i)$ is no longer correct.
- **Starting values with zeros.** A mass started at 0 stays at 0 under line L9. Start every $s_j$ positive.

## Implementations

## History

Ayer, Brunk, Ewing, Reid and Silverman (1955) found the NPMLE for current status data as an isotonic regression. Efron (1967) introduced self-consistency for right-censored data, and Peto (1973) defined the NPMLE for general interval-censored data, observed that its support lies in the intervals between a left end and the next right end, and maximized the likelihood numerically. Turnbull (1976) gave the innermost intervals for grouped, censored and truncated data together with the self-consistency algorithm, one year before Dempster, Laird and Rubin (1977) described the EM algorithm in general, of which it is an instance. Groeneboom and Wellner (1992) developed the asymptotic theory and the iterative convex minorant algorithm, and Gentleman and Geyer (1994) used the Kuhn-Tucker conditions to verify that a computed solution is the NPMLE and to study its uniqueness.

## References
