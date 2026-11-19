---
tag: P5RKY6
kind: algorithm
slug: simple-good-turing
name: Simple Good-Turing
aliases:
- Gale-Sampson smoothing
- SGT
area: natural-language-and-speech/language-modeling
level: advanced
summary: "Good-Turing with smoothed counts of counts: fit log N_r against log r by a line, and use it in place of the raw N_r once the two estimates no longer differ significantly."
model: word-ram
complexity:
  vars: {T: the number of distinct seen types, m: the number of distinct counts}
  time: {worst: "Θ(T + m)"}
  space: {extra: "Θ(T)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1995
  people: [William A. Gale, Geoffrey Sampson]
  note: Gale and Sampson published the method in the Journal of Quantitative Linguistics in 1995, as a Good-Turing estimator that a non-specialist could use without hand smoothing.
prereqs: [good-turing-estimation, ordinary-least-squares]
see_also: [katz-backoff, absolute-discounting, laplace-smoothing, witten-bell-smoothing, kneser-ney-smoothing, zipfs-law, chao1-estimator]
sources:
  - paper: doi:10.1080/09296179508590051
    title: William A. Gale and Geoffrey Sampson, Good-Turing frequency estimation without tears, Journal of Quantitative Linguistics 2(3), 1995, pages 217 to 237
    locator: the averaging transform Z_r, the line fit of log Z_r against log r, the rule that switches from the Turing to the smoothed estimate at 1.96 standard deviations, and the final renormalization
  - paper: doi:10.1093/biomet/40.3-4.237
    title: I. J. Good, The population frequencies of species and the estimation of population parameters, Biometrika 40(3-4), 1953, pages 237 to 264
    locator: the estimate (r+1) N_(r+1) / N_r and the need to smooth the counts of counts
  - book: isbn:9780262133609
    title: Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing, MIT Press, 1999
    locator: Chapter 6, Section 6.2 (Good-Turing estimation and the smoothing of the counts of counts)
---

Simple Good-Turing is a version of [Good-Turing estimation](/good-turing-estimation/) that works on real data without hand tuning. Raw Good-Turing uses the counts of counts $N_r$ (how many types were seen exactly $r$ times) directly, and for larger $r$ these numbers are noisy and often zero. William Gale and Geoffrey Sampson (1995) replaced them by a straight line fitted to $\log N_r$ against $\log r$, and used the line only from the first count where it agrees with the raw estimate. The result is a smooth set of discounts for every count, which [Katz backoff](/katz-backoff/) and other n-gram methods can use, and it does not need the fixed cut-off of raw Good-Turing.

## In plain words

Good-Turing estimates how much to trust a count by looking at how many things were seen once, twice, three times, and so on. For small counts these numbers are large and reliable. For large counts they jump around: there may be four things seen ten times, none seen eleven times and three seen twelve times. Using such numbers directly gives silly answers.

The fix is to draw one smooth curve through all these numbers and read the values from the curve. On the right scale the curve is close to a straight line, so a simple line fit does it. For the smallest counts the raw numbers are better than the line, so the method keeps them until the two answers are close, and from there on it uses the line.

## The problem

The input is a sample of $N$ tokens with the count $c(x) = r \ge 1$ of each seen type $x$. The output is a probability for each seen type and the total probability $P_0$ of the unseen types, with $P_0 + \sum_x p(x) = 1$. As in Good-Turing, $P_0 = N_1 / N$, and a type seen $r$ times gets probability proportional to an adjusted count $r^*$. The task is to compute $r^*$ for every $r$ that occurs, also where $N_{r+1} = 0$.

## The algorithm

Let $r_1 < r_2 < \cdots < r_m$ be the counts that occur. Where the counts become sparse, a count $r_j$ stands for a range of counts with $N = 0$, so the method first spreads each $N_{r_j}$ over the gap around it:

$$Z_{r_j} = \frac{2 N_{r_j}}{r_{j+1} - r_{j-1}}, \qquad r_0 = 0, \quad r_{m+1} = 2 r_m - r_{m-1}.$$

It then fits $\log Z_r = a + b \log r$ by [least squares](/ordinary-least-squares/) and writes $S(r) = e^{a} r^{b}$ for the smoothed counts of counts. For each $r$ there are two estimates: the Turing estimate $x_r = (r+1) N_{r+1} / N_r$ and the smoothed estimate $y_r = (r+1) S(r+1) / S(r)$. The Turing estimate has the approximate variance

$$\sigma_r^2 = (r+1)^2 \, \frac{N_{r+1}}{N_r^2} \Bigl(1 + \frac{N_{r+1}}{N_r}\Bigr).$$

```pseudo id=main
SIMPLE-GOOD-TURING(c)
L1  N ← Σ_x c(x); N_r ← the number of types with c(x) = r; r_1 < ... < r_m the counts that occur
L2  P_0 ← N_1 / N
L3  for j ← 1 to m do Z_{r_j} ← 2 N_{r_j} / (r_{j+1} - r_{j-1})      ▷ r_0 = 0, r_{m+1} = 2 r_m - r_{m-1}
L4  fit log Z_r = a + b log r by least squares over r_1 .. r_m
L5  S(r) ← exp(a + b log r)
L6  smoothed ← false
L7  for j ← 1 to m do  (r ← r_j)
L8      y ← (r + 1) S(r + 1) / S(r)
L9      if not smoothed and (N_{r+1} = 0 or |x_r - y| ≤ 1.96 σ_r) then smoothed ← true
L10     if smoothed then r* ← y else r* ← x_r
L11 N' ← Σ_r N_r r*
L12 for each seen type x do p(x) ← (1 - P_0) r*_{c(x)} / N'
L13 return p, P_0
```

Line L9 is the switch. The Turing estimate is used while it differs from the line by more than 1.96 standard deviations, which is the 95 percent level of a normal test. Once the line is used, it is used for every larger count. Lines L11 and L12 scale the seen probabilities so that they sum to $1 - P_0$. The smoothed estimate has the closed form $y_r = r (1 + 1/r)^{b+1}$, and the method needs a slope $b < -1$: then $y_r < r$ for every $r$.

## Example

Take a sample of $N = 1442$ tokens over $568$ seen types, with these counts of counts:

| $r$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 12 | 15 | 20 | 31 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $N_r$ | 268 | 112 | 70 | 41 | 24 | 14 | 15 | 7 | 6 | 4 | 3 | 2 | 1 | 1 |
| $Z_r$ | 268 | 112 | 70 | 41 | 24 | 14 | 15 | 7 | 6 | 2.667 | 1.2 | 0.5 | 0.125 | 0.091 |

For $r \le 9$ the neighbours are $r - 1$ and $r + 1$, so $Z_r = N_r$. For $r = 10$ the neighbours are 9 and 12, so $Z_{10} = 8/3$. The last count uses $r_{m+1} = 2 \cdot 31 - 20 = 42$, so $Z_{31} = 2/22$. The unseen mass is $P_0 = 268/1442 = 0.1859$. The line fit gives $a = 6.8139$ and $b = -2.5767$.

| $r$ | $x_r$ (Turing) | $y_r$ (line) | $1.96 \sigma_r$ | $r^*$ used | $p$ of one type | $r / N$ |
|---|---|---|---|---|---|---|
| 1 | 0.8358 | 0.3352 | 0.1843 | 0.8358 | 0.000588 | 0.000693 |
| 2 | 1.8750 | 1.0553 | 0.5599 | 1.8750 | 0.001319 | 0.001387 |
| 3 | 2.3429 | 1.9060 | 0.9031 | 1.9060 | 0.001341 | 0.002080 |
| 4 | 2.9268 | 2.8136 | 1.4744 | 2.8136 | 0.001979 | 0.002774 |
| 31 | none | 29.4864 | | 29.4864 | 0.020744 | 0.021498 |

For $r = 1$ and $r = 2$ the difference $|x_r - y_r|$ is larger than $1.96 \sigma_r$, so the Turing estimate stays. At $r = 3$ the difference $0.4369$ is below $0.9031$, so the method switches to the line for $r \ge 3$. The sum $N' = \sum_r N_r r^*$ is $1157.24$, and each type gets $(1 - P_0) r^* / N'$. Note that the line puts $r = 3$ only just above $r = 2$: the switch can make neighbouring counts almost tie.

## Correctness

**A proper distribution.** Every $r^*$ is positive: $x_r$ is used only while $N_{r+1} > 0$, and $y_r$ is a ratio of exponentials. So $N' > 0$, every $p(x) > 0$, and $\sum_x p(x) = (1 - P_0) \sum_r N_r r^* / N' = 1 - P_0$.

**One switch.** The flag of line L9 is never reset, so there is a count $s$ with $r^* = x_r$ for $r < s$ and $r^* = y_r$ for $r \ge s$. Every $r < s$ has $N_{r+1} > 0$, so $x_r$ is defined wherever it is used. The switch always happens, at the latest at $r_m$, because $N_{r_m + 1} = 0$.

**The shape of the smoothed counts.** From $S(r) = e^a r^b$, $y_r = (r+1)((r+1)/r)^{b} = r (1 + 1/r)^{b+1}$. If $b < -1$, write $c = -(b+1) > 0$. Then $y_r < r$, $\log y_r = \log r - c \log(1 + 1/r)$ grows with $r$, and $r - y_r \to c$ as $r \to \infty$. So the smoothed counts are discounted, they keep the order of the raw counts, and for large counts they subtract nearly the same amount. In the example $c = 1.58$, and $31 - y_{31} = 1.51$.

## Complexity

Counting the tokens takes $\Theta(N)$ expected time with a [hash table](/hash-table/). The table of the $N_r$ takes $\Theta(T)$ time. Lines L3 to L11 work on the $m$ distinct counts, in $\Theta(m)$ arithmetic operations, and $m \le \sqrt{2N}$. Line L12 takes $\Theta(T)$. The extra space is $\Theta(T)$ for the output and $\Theta(m)$ for the tables. The method uses floating point for the logarithms and the fit, so the result is not exact; the error is at the level of rounding.

## Properties

- **No cut-off to choose.** Every count gets an adjusted count. The only fixed constant is the 1.96 of the switch.
- **Monotone above the switch.** With $b < -1$ the smoothed counts grow with $r$. Below the switch the raw Turing estimates are used, and they need not be monotone.
- **The unseen mass is still $N_1 / N$.** The smoothing changes only how the remaining mass is split among the seen types.
- **A constant discount in the limit.** For large $r$ the discount $r - r^*$ tends to $-(b+1)$, which is the idea behind [absolute discounting](/absolute-discounting/).
- **A power law fit.** The line in log-log scale is a power law $N_r \propto r^b$, which matches the [Zipf](/zipfs-law/) shape of word counts. For data far from a power law the fit can be poor.

## Variants and improvements

- **Good's own smoothing.** Good (1953) already said that the $N_r$ need smoothing and discussed ways to do it. Simple Good-Turing picks one simple smoother and adds a rule for when to use it.
- **Other confidence levels.** The 1.96 can be changed. A larger value keeps the Turing estimates for more counts.
- **[Katz backoff](/katz-backoff/)** uses discounts only for $r \le k$ and renormalizes them so that the discounted mass equals $N_1$. Simple Good-Turing discounts every count and renormalizes at the end.
- **Per-history use.** In an [n-gram model](/n-gram-language-model/) the method can be applied to all the n-grams of one order, and the discounts then shared by all histories, as Katz does.

## When to use it

Use it when you want Good-Turing estimates for every count of a large sample, such as word or n-gram frequencies, species counts or k-mer counts, and the data have a heavy tail. It needs at least two distinct counts, and it works best with many types seen once or twice. For small samples, or when the fitted slope is not below $-1$, use plain [Laplace smoothing](/laplace-smoothing/) or a held-out method such as [deleted interpolation](/deleted-interpolation/).

## Pitfalls

- **The slope must be below $-1$.** If $b \ge -1$ the smoothed counts are not below the raw counts, and the estimates are not discounts. Check $b$ and fall back to another method.
- **Fit $Z_r$, not $N_r$.** Fitting the raw $N_r$ ignores the zero counts in the gaps and gives a slope that is too flat.
- **The switch is one way.** Do not go back to the Turing estimate after the first agreement, even if a later count disagrees again.
- **Near ties at the switch.** At the switch the adjusted count can drop to the line, so a type seen $r$ times can get almost the same probability as a type seen $r - 1$ times.
- **Renormalize.** The $r^*$ do not sum to $N - N_1$ on their own; without line L12 the result is not a distribution.

## Implementations

## History

Good (1953) gave the Turing estimate and pointed out that the counts of counts must be smoothed, but left the choice of smoother to the user. Church and Gale (1991) compared Good-Turing estimates of English bigram probabilities with held-out counts. Gale and Sampson (1995) wrote the simple method down in full, with the averaging transform, the log-log line and the switching rule, so that a researcher without a background in statistics could use Good-Turing estimation on any frequency table.

## References
