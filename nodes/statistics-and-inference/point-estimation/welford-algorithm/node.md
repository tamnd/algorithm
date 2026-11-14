---
tag: 3F3F57
kind: algorithm
slug: welford-algorithm
name: Welford's algorithm
aliases:
- Welford's online algorithm
- running variance algorithm
- online variance algorithm
area: statistics-and-inference/point-estimation
level: core
summary: Computes the mean and variance of a stream in one pass, updating the mean and the sum of squared deviations per item. It avoids the cancellation of the textbook formula.
model: floating-point-model
complexity:
  vars: {n: "the number of data values, at least 2"}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
  flops: {worst: "6 n + 1"}
properties: {deterministic: true, online: true, one_pass: true, recursive: false, exact_in_exact_arithmetic: true}
history:
  year: 1962
  people: [B. P. Welford]
  note: Welford published a one-pass method for corrected sums of squares and products in Technometrics in 1962. Knuth gives the recurrence for the mean and the sum of squares in Section 4.2.2 of The Art of Computer Programming, Volume 2.
prereqs: [sample-variance, catastrophic-cancellation, floating-point-model]
see_also: [chan-parallel-variance, variance, pairwise-summation, kahan-summation, condition-number, exponential-moving-average, covariance-matrix, standard-error]
sources:
  - paper: doi:10.1080/00401706.1962.10490022
    title: B. P. Welford, Note on a method for calculating corrected sums of squares and products, Technometrics 4(3), 1962
    locator: pp. 419 to 420 (updating the mean and the corrected sum of squares one observation at a time)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1997
    locator: Section 4.2.2 (the recurrences for M_k and S_k)
  - paper: doi:10.1080/00031305.1983.10483115
    title: Tony F. Chan, Gene H. Golub and Randall J. LeVeque, Algorithms for computing the sample variance, analysis and recommendations, The American Statistician 37(3), 1983
    locator: pp. 242 to 247 (the updating formulas (1.3), the condition number (2.1) and the error bounds of Table 1)
  - paper: doi:10.1145/359146.359152
    title: Tony F. Chan and John Gregg Lewis, Computing standard deviations, accuracy, Communications of the ACM 22(9), 1979
    locator: pp. 526 to 531 (rounding error analysis of the textbook and the updating algorithms)
  - paper: doi:10.1145/359146.359153
    title: D. H. D. West, Updating mean and variance estimates, an improved method, Communications of the ACM 22(9), 1979
    locator: pp. 532 to 535 (the weighted updating algorithm)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 1.9 (computing the sample variance)
---

Welford's algorithm computes the mean and the sum of squared deviations of a sequence of numbers in one pass and constant memory, by updating both each time a value arrives; the [sample variance](/sample-variance/) is the sum divided by $n - 1$. In exact arithmetic it gives the same numbers as the two-pass formula. In floating point its error bound grows like $n\kappa u$, where $\kappa$ is the condition number of the data, while the textbook formula $\sum_i x_i^2 - n\bar x^2$ has the bound $n\kappa^2 u$ and can lose every digit to [catastrophic cancellation](/catastrophic-cancellation/). The update of two partial results, not one value, is the [Chan-Golub-LeVeque algorithm](/chan-parallel-variance/).

## In plain words

Keep three numbers: how many values you have seen, their average, and a running total of squared distances from the average. When a new value comes, measure how far it is from the old average. Move the average toward it by that distance divided by the new count. Then add to the total the old distance times the distance from the new average. The two distances point the same way, so the total only grows. At the end, the total divided by the count minus one is the sample variance.

The textbook shortcut adds up the squares of the values and subtracts the square of their sum, divided by the count. When the values are large and close together, the two big numbers almost cancel, and what is left is mostly rounding error. Welford's update works with distances from the average, which stay small.

## The problem

The input is a sequence of real numbers $x_1, \ldots, x_n$ with $n \ge 2$, which may arrive one at a time with no way to read them again. The output is the mean $\bar x = \frac1n\sum_i x_i$, the sum of squared deviations $\mathrm{SS} = \sum_i (x_i - \bar x)^2$ and the sample variance $S^2 = \mathrm{SS}/(n-1)$. The divisor-$n$ variance is $\mathrm{SS}/n$. The memory may not grow with $n$, and after any prefix the values for that prefix should be available.

## The algorithm

```pseudo id=main
WELFORD(x_1, ..., x_n)                     ▷ n ≥ 2
L1  M ← 0, S ← 0
L2  for k ← 1 to n do
L3      d ← x_k - M                         ▷ distance from the old mean
L4      M ← M + d / k                       ▷ M is now the mean of x_1 .. x_k
L5      S ← S + d · (x_k - M)               ▷ old distance times new distance
L6  V ← S / (n - 1)                         ▷ sample variance; S / n for divisor n
L7  return M, V, S
```

The invariant is that after iteration $k$, $M$ is the mean of the first $k$ values and $S$ is their sum of squared deviations. Line L5 multiplies the distance from the old mean by the distance from the new one. Both have the sign of $d$, and their product equals $\frac{k-1}{k}d^2$, which is the amount by which the sum of squared deviations grows when $x_k$ joins. Line L5 can also be written $S \leftarrow S + \frac{k-1}{k} d^2$; Chan, Golub and LeVeque write the update in that form as (1.3), and say that the methods of Welford, West and Hanson are virtually identical for unweighted data.

For a stream, lines L3 to L5 are the update and line L6 is a query that can be asked after any $k \ge 2$.

## Example

The data are $x = (3, 7, 7, 9, 14)$, in exact arithmetic.

| $k$ | $x_k$ | $d = x_k - M_{k-1}$ | $M_k$ | $x_k - M_k$ | $S_k$ |
|---|---|---|---|---|---|
| 1 | 3 | 3 | 3 | 0 | 0 |
| 2 | 7 | 4 | 5 | 2 | 8 |
| 3 | 7 | 2 | 17/3 | 4/3 | 32/3 |
| 4 | 9 | 10/3 | 13/2 | 5/2 | 19 |
| 5 | 14 | 15/2 | 8 | 6 | 64 |

So $\bar x = 8$, $\mathrm{SS} = 64$ and $V = 64/4 = 16$, the values on [sample variance](/sample-variance/). Each $S_k$ is the sum of squared deviations of the first $k$ values; for $k = 3$, the values $3, 7, 7$ have mean $17/3$ and $(8/3)^2 + 2(4/3)^2 = 96/9 = 32/3$.

**The same data, shifted.** Add $10^9$ to each value. The spread is unchanged, so $S^2$ is still 16. In IEEE double precision, the textbook formula $(\sum_i x_i^2 - n\bar x^2)/(n-1)$ returns $-256$, a negative variance, because $\sum_i x_i^2 \approx 5 \times 10^{18}$ is stored with a spacing of 1024 between neighbouring doubles. The two-pass formula returns 16.0 and Welford's algorithm returns 16.000000044703484, a relative error of $2.8 \times 10^{-9}$.

## Correctness

By induction on $k$, after iteration $k$, $M$ is the mean $\bar x_k$ of the first $k$ values and $S$ is their sum of squared deviations $\mathrm{SS}_k$. The mean update is $\bar x_k = ((k-1)\bar x_{k-1} + x_k)/k$. For the sum, write the old deviations around the new mean with the shift identity $\sum_{i<k}(x_i - \bar x_k)^2 = \mathrm{SS}_{k-1} + (k-1)(\bar x_{k-1} - \bar x_k)^2$, add the new term, and simplify with $\bar x_k - \bar x_{k-1} = d/k$: the increase is $\frac{k-1}{k}d^2 = d\,(x_k - \bar x_k)$. The full proof is below. It is a statement about exact arithmetic; the floating-point behaviour is in the next sections.

## Complexity

Each iteration does one subtraction in line L3, a division and an addition in line L4, and a subtraction, a multiplication and an addition in line L5. With the division of line L6, the count is exactly $6n + 1$ floating-point operations, for every input. The time is $\Theta(n)$ and the extra space is $\Theta(1)$: $M$, $S$, $d$ and $k$.

For comparison, the textbook formula $(\sum_i x_i^2 - (\sum_i x_i)^2/n)/(n-1)$ costs about $3n$ operations in one pass, and the two-pass formula about $4n$ operations in two passes, with the data stored or read twice.

**Rounding error.** Let $u$ be the unit roundoff ($2^{-53}$ in double precision). Chan, Golub and LeVeque measure the difficulty of the data by the condition number

$$\kappa = \sqrt{1 + \frac{n\bar x^2}{\mathrm{SS}}} \;\ge\; 1,$$

which is about $\lvert\bar x\rvert/s$, the mean divided by the standard deviation, when that ratio is large. Their Table 1 lists bounds on the relative error of the computed $\mathrm{SS}$, with small constants and higher-order terms dropped:

| algorithm | error bound |
|---|---|
| textbook, one pass | $n\kappa^2 u$ |
| two-pass | $nu + n^2\kappa^2u^2$ |
| updating (Welford, West) | $n\kappa u$ |
| pairwise ([Chan-Golub-LeVeque](/chan-parallel-variance/)) | $\kappa u \log n$, conjectured |

The bounds for the textbook and the updating algorithms are proved by Chan and Lewis (1979). So when $\kappa$ is near $u^{-1/2} \approx 10^8$, the textbook bound exceeds 1 and the result can have no correct digit, while the bound for Welford's algorithm is $n u^{1/2}$.

**Measured errors.** The table gives the relative error of $S^2$ in double precision against the exact value of the stored data, computed with Python's `fractions.Fraction`. The data are $c + Z_i$ with $Z_i$ standard normal from `random.Random(1)`, $n = 10^4$, one run per row, the rows drawn in this order from one generator. The textbook column is $(\sum_i x_i^2 - (\sum_i x_i)^2/n)/(n-1)$, the two-pass column uses plain left-to-right sums, and the pairwise column is the recursive merge of the [Chan-Golub-LeVeque algorithm](/chan-parallel-variance/).

| $c$ | $\kappa$ | textbook | two-pass | Welford | pairwise |
|---|---|---|---|---|---|
| $10^2$ | 101 | $8.5 \times 10^{-11}$ | $2.8 \times 10^{-15}$ | $7.9 \times 10^{-16}$ | $2.3 \times 10^{-16}$ |
| $10^4$ | $9.96 \times 10^3$ | $1.5 \times 10^{-7}$ | $3.3 \times 10^{-15}$ | $2.4 \times 10^{-13}$ | $3.8 \times 10^{-14}$ |
| $10^6$ | $1.0 \times 10^6$ | $6.4 \times 10^{-3}$ | $4.8 \times 10^{-15}$ | $2.1 \times 10^{-11}$ | $7.2 \times 10^{-13}$ |
| $10^8$ | $9.9 \times 10^7$ | 7.45 | $8.3 \times 10^{-15}$ | $2.9 \times 10^{-9}$ | $1.7 \times 10^{-10}$ |

These are single measured runs, not bounds. They follow the pattern of the bounds: the textbook error grows much faster with $\kappa$ than the Welford error, which grows roughly in proportion to $\kappa$ and stays far below $n\kappa u$; the two-pass error stays below $10^{-14}$. At $c = 10^8$ the textbook error is 7.45 times the true value.

## Properties

- **One pass and online.** Each value is used once, in order, and the mean and variance of every prefix are available.
- **Constant memory.** Three numbers and a counter, whatever $n$ is.
- **Exact in exact arithmetic.** With rational inputs and exact arithmetic it returns exactly $\bar x$, $\mathrm{SS}$ and $S^2$.
- **Nonnegative.** In exact arithmetic every increment of $S$ is $\frac{k-1}{k}d^2 \ge 0$. The textbook formula is a difference and can be negative in floating point, as the example shows.
- **Order dependent in floating point.** Feeding the same values in another order changes the last digits of the result.

## Variants and improvements

- **Weights.** For weights $w_k > 0$, keep $W = \sum w_k$ and use $W \leftarrow W + w_k$, $M \leftarrow M + (w_k/W)\,d$ and $S \leftarrow S + w_k\, d\,(x_k - M)$. This is West's (1979) weighted updating. With frequency weights, $S/(W - 1)$ is the sample variance of the expanded data.
- **Covariance.** For pairs $(x_k, y_k)$, update both means and $C \leftarrow C + (x_k - M_x^{\text{old}})(y_k - M_y^{\text{new}})$. Then $C/(n-1)$ is the sample covariance; the vector form updates a [covariance matrix](/covariance-matrix/) by an outer product.
- **Merging.** Two accumulators $(n_a, M_a, S_a)$ and $(n_b, M_b, S_b)$ combine in $O(1)$ operations. That is the [Chan-Golub-LeVeque algorithm](/chan-parallel-variance/); Welford's update is its case $n_b = 1$.
- **Higher moments.** The same approach updates the third and fourth central sums, for the skewness and the kurtosis of a stream.
- **Forgetting.** Replacing $1/k$ in line L4 by a fixed weight $\alpha$ gives the [exponential moving average](/exponential-moving-average/) of the mean, which follows a drifting stream.
- **Shift first.** Subtracting a rough estimate of the mean, for example $x_1$, from every value reduces $\kappa$; Chan, Golub and LeVeque show that a shift within $\sqrt{\mathrm{SS}/n}$ of the mean gives $\kappa < \sqrt 2$ for the shifted data, after which even the textbook formula is accurate.

## When to use it

Use Welford's algorithm when the data come as a stream, are too large to store, or must be summarized after every value, as in monitoring and in online learning. If the data fit in memory, the two-pass formula is simpler and more accurate. If the data are small integers, the textbook formula in exact integer arithmetic has no rounding error until the final division. To summarize parts in parallel, use one Welford accumulator per part and merge them with the [Chan-Golub-LeVeque algorithm](/chan-parallel-variance/).

## Pitfalls

- **The new mean in both factors.** The update $S \leftarrow S + (x_k - M)^2$ with the new $M$ adds too little: on the example it gives $1729/36 \approx 48.03$ instead of 64. With the old mean in both factors, $S \leftarrow S + d^2$ adds $d^2/k$ too much in each step. The two factors must use the old and the new mean.
- **Integer division.** In a language where $d/k$ with integer operands truncates, line L4 is wrong for integer data. Convert to floating point first.
- **The divisor.** Return $S/(n - 1)$ for the sample variance and $S/n$ for the divisor-$n$ variance, and say which one. For $n = 1$, $S/(n-1)$ is undefined.
- **Not immune to bad conditioning.** The error still grows with $\kappa$. For data with a huge mean and a tiny spread, shift the data first.
- **Removing values.** Running the update backwards removes a value from the accumulator, for a sliding window, but it subtracts and can lose the accuracy that the forward update keeps.

## Implementations

## History

Welford (1962) gave a method for computing corrected sums of squares and products in one pass, by updating them one observation at a time. Knuth gives the recurrence for $M_k$ and $S_k$ in Section 4.2.2 of The Art of Computer Programming. Chan and Lewis (1979) analysed the rounding error of the textbook and updating algorithms, West (1979) gave the weighted version, and Chan, Golub and LeVeque (1983) compared the known algorithms, bounded their errors in terms of $\kappa$ and recommended which to use.

## References
