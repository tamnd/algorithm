---
tag: JDXKJ0
kind: algorithm
slug: systematic-sampling
name: Systematic sampling
aliases:
- every k-th item sampling
- interval sampling
- 1-in-k sampling
area: randomized/sampling
level: intro
summary: Choose one random start and then take every k-th item of the population (with a fractional step if needed), so that each item has inclusion probability n/N with one random number.
model: word-ram
complexity:
  vars: {N: the population size, n: the sample size}
  time: {worst: Θ(n)}
  space: {extra: O(1)}
properties: {online: false, deterministic: false, recursive: false}
prereqs: [random-sampling, uniform-distribution, linearity-of-expectation]
see_also: [stratified-sampling, selection-sampling, uniform-random-subset, probability-proportional-to-size-sampling, resampling, latin-hypercube-sampling]
sources:
  - book: isbn:9780471162407
    title: William G. Cochran, Sampling Techniques, third edition, Wiley, 1977
    locator: Chapter 8, systematic sampling (its variance, the comparison with simple random and stratified sampling, populations with a linear trend and with periodic variation)
---

Systematic sampling picks $n$ items from a population of $N$ items listed in some order by drawing one random start and then taking items at equal steps. With $k = N/n$ a whole number, the start $s$ is uniform in $\{0, \ldots, k - 1\}$ and the sample is $s, s + k, s + 2k, \ldots$. When $N/n$ is not a whole number, the step can be the fraction $N/n$ and the positions are rounded down. Each item is in the sample with probability exactly $n/N$, so the sample mean is unbiased. It costs one random number. Unlike a [uniform random subset](/uniform-random-subset/), it can produce only $k$ different samples, so its variance depends on the order of the list: it is better than simple random sampling when the list has a trend, and much worse when the list has a period that matches the step.

## In plain words

To check 1 in 10 boxes coming off a line, pick a random box among the first ten, then take every tenth box after it. Each box has the same chance, 1 in 10, of being checked, and you only had to roll the die once.

The sample spreads evenly over the list. If the list is sorted by size, the sample gets small, middle and large items in fair amounts, which makes the average more accurate. The danger is a list with a rhythm. If every tenth box comes from the same faulty machine, you check either all of its boxes or none of them.

## The problem

The input is a population of $N$ items in a fixed order, $x_0, \ldots, x_{N-1}$, and a sample size $1 \le n \le N$. The output is $n$ distinct items, in order, such that each item has inclusion probability $n/N$. Often the items carry values $y_j$ and the goal is to estimate the mean $\bar Y = \frac{1}{N}\sum_j y_j$. The method does not give each $n$-subset the same probability. It is a sampling design, as described in [random sampling](/random-sampling/), chosen for its low cost and even spread.

## The algorithm

```pseudo id=main
SYSTEMATIC-SAMPLE(x[0..N−1], n)           ▷ 1 ≤ n ≤ N
L1  r ← a uniform random integer in {0, ..., N − 1}
L2  S ← an empty list
L3  for i ← 0 to n − 1
L4      append x[⌊(r + i·N)/n⌋] to S          ▷ the start r/n, the step N/n
L5  return S
```

The points $(r + iN)/n$ are a start in $[0, N/n)$ plus multiples of the step $N/n \ge 1$. Taking the start as $r/n$ with integer $r$ keeps the arithmetic exact. When $n$ divides $N$, line L4 gives $\lfloor r/n \rfloor + ik$ with $k = N/n$, which is the classical rule with start $\lfloor r/n \rfloor$, uniform in $\{0, \ldots, k-1\}$.

## Example

**Classical step.** Let $N = 12$, $n = 3$ and $k = 4$. The four possible samples are the positions $\{0, 4, 8\}$, $\{1, 5, 9\}$, $\{2, 6, 10\}$ and $\{3, 7, 11\}$, each with probability $1/4$.

**Fractional step.** Let $N = 10$ and $n = 4$, so the step is $2.5$. With $r = 7$, line L4 gives $\lfloor 7/4 \rfloor = 1$, $\lfloor 17/4 \rfloor = 4$, $\lfloor 27/4 \rfloor = 6$ and $\lfloor 37/4 \rfloor = 9$.

**Trend and period.** Take the population $y = 1, 2, \ldots, 12$, which has a linear trend, with $n = 3$. The four samples have means 5, 6, 7 and 8, so the sample mean is unbiased for $6.5$, with variance $1.25$. A simple random sample of size 3 has variance $(1 - \frac{3}{12}) \frac{S^2}{3} = 3.25$, where $S^2 = 13$. Now take $y = 10, 0, 0, 0$ repeated three times, a period of length 4, equal to the step. The four samples have means 10, 0, 0 and 0. The estimate is still unbiased for $2.5$, but its variance is $18.75$, against $225/44 \approx 5.11$ for a simple random sample.

## Correctness

**Theorem.** For $1 \le n \le N$, SYSTEMATIC-SAMPLE returns $n$ distinct items in input order, each position is included with probability exactly $n/N$, and the sample mean is an unbiased estimate of the population mean.

The steps are $N/n \ge 1$, so the floors are distinct. Position $j$ is sampled when some $r + iN$ falls in the window $\{jn, \ldots, jn + n - 1\}$. The numbers $r + iN$ are the integers in $[0, nN)$ with residue $r$ modulo $N$. A window of $n \le N$ consecutive integers has $n$ different residues, so exactly $n$ of the $N$ values of $r$ hit it. Unbiasedness then follows from linearity of expectation. The full proof is below.

## Complexity

- **Time.** One random number and $n$ index computations: $\Theta(n)$ with random access to the items. On a sequential file, one scan of $\Theta(N)$.
- **Space.** $O(1)$ besides the output.
- **Variance.** The design has only $N$ equally likely outcomes, and when $n$ divides $N$ only $k$ different samples. So the variance of $\bar y$ is the variance of $k$ numbers, the means of the $k$ possible samples. Cochran writes it as
$$\operatorname{Var}[\bar y_{\text{sy}}] = \frac{N-1}{N} S^2 - \frac{k(n-1)}{N} S^2_{\text{wsy}},$$
where $S^2$ is the population variance and $S^2_{\text{wsy}}$ is the variance among items of the same systematic sample. So systematic sampling beats simple random sampling exactly when the items inside one sample differ more than items at random do.

## Properties

- **One random number.** The whole sample is fixed by the start.
- **Even spread.** Every stretch of $\lceil N/n \rceil$ consecutive items holds at least one sampled item. This is the reason for its gain on sorted lists and lists with trends.
- **Equal inclusion probabilities, unequal joint probabilities.** Two items closer than the step, or not a multiple of the step apart in the classical form, are never sampled together. So the design is not simple random sampling.
- **No variance estimate from one sample.** Because there is only one random start, the sample itself gives no unbiased estimate of the variance of $\bar y$. A common remedy is to take several systematic samples with independent starts.

## Variants and improvements

- **Several random starts.** Take $m$ systematic samples with step $mk$ and independent starts. The spread between their means gives an unbiased variance estimate.
- **Systematic sampling with unequal sizes.** Apply the same rule to the cumulative sizes of the items: lay the items end to end on a line by size, and take the points start plus multiples of a step. Each item is then included with probability proportional to its size, if no size exceeds the step. See [probability proportional to size sampling](/probability-proportional-to-size-sampling/).
- **Systematic resampling.** Particle filters use the same rule to resample particles by weight with one random number. See [resampling](/resampling/).
- **Stratified sampling with one item per stratum.** If each block of $k$ items gets its own independent start, the design is [stratified sampling](/stratified-sampling/) with one item per stratum. It loses the single random number but has no trouble with periods.
- **Latin hypercube sampling.** In several dimensions, one point per stratum in each coordinate is [Latin hypercube sampling](/latin-hypercube-sampling/).

## When to use it

Use systematic sampling when the population is a list or a stream in a known order and a cheap, evenly spread sample is wanted: quality control on a production line, every $k$-th record in a register, every $k$-th tree along a transect, or every $k$-th packet in a network monitor. It works best when the order is random with respect to the values or follows a smooth trend. Do not use it when the order may have a cycle near the step, such as weekdays, rows of houses or seats in a plane. Then use [stratified sampling](/stratified-sampling/) or a uniform random subset by [selection sampling](/selection-sampling/).

## Pitfalls

- **Periodic order.** If the values repeat with a period that divides the step, all items in a sample look alike, and the variance can be far larger than for simple random sampling, as in the example.
- **A fixed start.** Starting always at item 0 makes the sample deterministic. Only a random start makes the inclusion probabilities $n/N$.
- **Rounding the step.** Using the whole step $\lfloor N/n \rfloor$ when $n$ does not divide $N$ makes the sample size depend on the start, or leaves the tail of the list with no chance. Use the fractional step of line L4, or a circular list.
- **Using the simple random sampling variance formula.** The formula $(1 - n/N) s^2/n$ with the sample variance $s^2$ is biased for systematic samples. It is often too large for lists with a trend and too small for periodic lists.

## Implementations

## History

Systematic selection, every $k$-th unit from a list, was in use long before its theory. William and Lillian Madow gave a theory of its variance in the 1940s, and Cochran's Sampling Techniques treats it in a chapter of its own, with the comparisons to simple random and stratified sampling for populations in random order, with linear trends, and with periodic variation.

## References
