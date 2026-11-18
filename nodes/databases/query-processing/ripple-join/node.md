---
tag: NQMZP0
kind: algorithm
slug: ripple-join
name: Ripple join
aliases:
- Haas-Hellerstein ripple join
area: databases/query-processing
level: advanced
summary: "A join for online aggregation. It reads both inputs in random order, joins each new tuple with all tuples read from the other input, and scales the running sum into an unbiased estimate."
solves: [relational-join]
model: real-ram
complexity:
  vars: {n: the number of tuples read from R, m: the number of tuples read from S, j: the number of joining pairs among the tuples read}
  time: {worst: "O(n m)", average: "O(n + m + j)"}
  space: {extra: "O(n + m)"}
properties: {deterministic: false, exact: false, external: false, online: true, in_place: false, recursive: false}
history:
  year: 1999
  people: [Peter J. Haas, Joseph M. Hellerstein]
  note: "Haas and Hellerstein introduced ripple joins at SIGMOD 1999 for the online aggregation of multi-table queries."
prereqs: [online-aggregation, nested-loop-join, symmetric-hash-join]
see_also: [wander-join, confidence-interval, central-limit-theorem, hoeffding-inequality, linearity-of-expectation, random-sampling, block-nested-loop-join, xjoin]
sources:
  - paper: doi:10.1145/304182.304208
    title: "Peter J. Haas and Joseph M. Hellerstein, Ripple joins for online aggregation, SIGMOD 1999, pages 287 to 298"
    locator: the ripple join family (block, index and hash ripple joins), the aspect ratios and their adaptive choice, and the confidence intervals based on a central limit theorem
  - paper: doi:10.1145/253260.253291
    title: "Joseph M. Hellerstein, Peter J. Haas and Helen J. Wang, Online aggregation, SIGMOD 1997, pages 171 to 182"
    locator: the online aggregation interface with running estimates and confidence intervals for single-table queries
  - paper: doi:10.1145/564691.564721
    title: "Gang Luo, Curt J. Ellmann, Peter J. Haas and Jeffrey F. Naughton, A scalable hash ripple join algorithm, SIGMOD 2002, pages 252 to 262"
    locator: the hash ripple join when the tuples read no longer fit in memory
---

A ripple join computes an aggregate such as SUM or COUNT over a join $R \bowtie S$ for [online aggregation](/online-aggregation/): it reports a running estimate with a confidence interval from the first tuples on, and the exact answer when it has read both inputs. It reads both inputs in random order, and at each step it adds a few tuples of each input and joins each new tuple with every tuple already read from the other input, so the pairs it has seen form a growing rectangle. The estimate is the running sum scaled by the fraction of the rectangle seen, and by [linearity of expectation](/linearity-of-expectation/) it is unbiased. The hash form is a [symmetric hash join](/symmetric-hash-join/) over random orders. Unlike a [nested loops join](/nested-loop-join/), which must read all of the inner input for its first outer tuple, a ripple join samples both inputs at once. A [wander join](/wander-join/) samples random paths through indexes instead.

## In plain words

You want the total sales of all orders that match a customer in a promotion list, but both tables are large. Instead of waiting for the exact total, you want a good guess now and a better guess every second.

So you take orders and customers in a random order, a few of each at a time. Each new order is checked against the customers you already took, and each new customer against the orders you already took. You add up the sales of every match you find.

If you have taken a tenth of the orders and a tenth of the customers, you have checked about a hundredth of all pairs. So your total, multiplied by 100, is a fair guess of the full total. The guess gets better as you go, and it is exact when you have taken everything.

## The problem

The input is two relations $R$ and $S$ with $|R| = N$ and $|S| = M$, a join condition $r.a = s.b$ (a NULL key never matches) and a value $v(r, s)$ for each joining pair, for example a column of $r$. The query asks for $\tau = \sum v(r, s)$ over the bag $R \bowtie S$. COUNT is the case $v = 1$, and AVG is SUM divided by COUNT.

The output is a sequence of estimates $\hat\tau_1, \hat\tau_2, \dots$, one per step, each with a confidence interval, such that each estimate is unbiased and the last one equals $\tau$.

**Cost model.** The measure is the work per step in the [real RAM](/real-ram/), with expected $O(1)$ time per hash table operation, and the quality of the estimate after $n$ tuples of $R$ and $m$ tuples of $S$, measured by its variance. The orders of $R$ and $S$ must be independent and uniformly random, for example because the tables are stored in random order or read through a random permutation.

## The algorithm

```pseudo id=main
RIPPLE-JOIN(R, S, v, β_R, β_S)          ▷ v(r, s) is the value of a joining pair
L1  put R and S in independent random orders; R_t, S_t ← empty; Σ ← 0
L2  while some tuple of R or S is not read do
L3      for β_R new tuples r of R, as far as they last: Σ ← Σ + the sum of v(r, s) over s in S_t that join with r; add r to R_t
L4      for β_S new tuples s of S, as far as they last: Σ ← Σ + the sum of v(r, s) over r in R_t that join with s; add s to S_t
L5      τ̂ ← N M / (|R_t| |S_t|) · Σ
L6      h ← z · the square root of the estimated variance of τ̂
L7      report τ̂ ± h
```

The pair $(\beta_R, \beta_S)$ is the *aspect ratio*. The *square* ripple join has $\beta_R = \beta_S = 1$. With $\beta_S = M$, the first step reads all of $S$, and the ripple join becomes a nested loops join over a random order of $R$. Lines L3 and L4 can scan the tuples read from the other input (the block or nested-loops form) or look up the key in a hash table on them (the hash form). Both forms add the same pairs, so they give the same estimates.

The variance in line L6 is the first-order part of the formula in the section on correctness, with the variances of the row and column means estimated from the sample. The number $z$ comes from the normal distribution, for example $z = 1.96$ for a 95% interval.

## Example

Let $R = r_1(1, 3), r_2(2, 5), r_3(1, 2), r_4(3, 4)$, written as (key, price), and $S = s_1(1), s_2(2), s_3(1)$. The query is the SUM of the price over $R \bowtie S$. The true answer is $\tau = 3 \cdot 2 + 5 + 2 \cdot 2 = 15$. Take the square ripple join, and let the random order be the order given.

| step | new tuples | new joining pairs | $\Sigma$ | rectangle | estimate $\frac{12}{n m} \Sigma$ |
|---|---|---|---|---|---|
| 1 | $r_1$, $s_1$ | $(r_1, s_1)$: 3 | 3 | $1 \times 1$ | 36 |
| 2 | $r_2$, $s_2$ | $(r_2, s_2)$: 5 | 8 | $2 \times 2$ | 24 |
| 3 | $r_3$, $s_3$ | $(r_3, s_1)$: 2, $(r_1, s_3)$: 3, $(r_3, s_3)$: 2 | 15 | $3 \times 3$ | 20 |
| 4 | $r_4$ ($S$ is exhausted) | none | 15 | $4 \times 3$ | 15 |

The estimate at step 3 is 20, although the sum already holds all 15. The ripple join cannot know that the unread tuple $r_4$ joins with nothing. Over all $4! \cdot 3! = 144$ orders, the mean of the estimate at each step is exactly 15.

**A larger run.** Let $R$ have 200 tuples with keys from 5 values and prices from 1 to 19, and $S$ have 200 tuples with keys from the same 5 values, all drawn with seed 5. The true SUM is 79718. Over 200 square ripple joins with different random orders:

| tuples read from each input | mean estimate | standard deviation of the estimate | median half width at 95% | runs whose interval holds 79718 |
|---|---|---|---|---|
| 10 | 79962 | 22178 | 50722 | 193 of 200 |
| 25 | 79050 | 9254 | 22948 | 197 of 200 |
| 50 | 79466 | 5866 | 12656 | 195 of 200 |
| 100 | 80115 | 3150 | 6607 | 193 of 200 |

The exact standard deviation from the variance formula is 21904, 10393, 6039 and 3244 at these four steps. At 100 tuples of each input the ripple join has seen a quarter of the pairs, and the standard deviation of its estimate is about 4% of the answer. These numbers are measurements of this simulation.

## Correctness

At each step the running sum is the sum of $v$ over all joining pairs in the rectangle $R_t \times S_t$, because each pair is added once, when the later of its two tuples is read. A prefix of a random order is a uniform random subset, so a pair is in the rectangle with probability $\frac{n}{N} \cdot \frac{m}{M}$, and the scaled sum has expectation $\tau$. The exact variance is

$$\operatorname{Var}(\hat\tau) = N^2 M^2 \left( \frac{(1 - n/N) S_a^2}{n} + \frac{(1 - m/M) S_b^2}{m} + \frac{(1 - n/N)(1 - m/M) S_g^2}{n m} \right),$$

where $S_a^2$ is the variance of the row means $a(r) = \frac{1}{M} \sum_s v(r, s)$, $S_b^2$ the variance of the column means, and $S_g^2$ the variance of the rest. When both inputs are read, every factor $1 - n/N$ and $1 - m/M$ is 0 and the estimate is exact. The proofs are in [the proof page](proofs/correctness.md).

The interval of line L6 uses an estimate of the first two terms and a [central limit theorem](/central-limit-theorem/), so its coverage is close to the nominal level only for large samples. A conservative interval from [Hoeffding's inequality](/hoeffding-inequality/) needs a bound on the values and is wider. See [confidence interval](/confidence-interval/) for the general idea.

## Complexity

- **Work.** The hash form does expected $O(1)$ work per tuple read and per joining pair found, so the work up to the rectangle $n \times m$ is expected $O(n + m + j)$. The block form does $n m$ comparisons for the same rectangle. The variance can be kept up to date in $O(1)$ per pair with running sums of squares.
- **Variance.** For a fixed aspect ratio the variance falls like $1/n$ in the number of tuples read from each input, plus a term in $1/(n m)$ that matters only for small samples. A ratio that reads more from the input whose row means vary more gives a smaller variance for the same work.
- **Space.** All tuples read stay in memory, $O(n + m)$, because a later tuple of the other input may join with any of them.

## Properties

- **Online.** An estimate is available after each step, and the user may stop the query at any time.
- **Unbiased at every step** for SUM and COUNT, when the orders are uniformly random. AVG is a ratio of two estimates and is only consistent.
- **Exact at the end.** After both inputs are read, the estimate is the answer and the interval has width 0.
- **Randomized.** The estimates depend on the random orders. With a fixed seed they are repeatable.
- **Any join condition.** The block form works for any predicate, not only for equality, but it needs $n m$ comparisons.

## Variants and improvements

- **Adaptive aspect ratio.** Haas and Hellerstein choose the aspect ratio during the run, from the estimated variances of the two inputs, to make the interval shrink fastest for the work done.
- **Index ripple join.** If $S$ has an index on the key, each new tuple of $R$ looks up all its matches in $S$ at once. This is the case $\beta_S = M$ done through the index, and the estimate is then a mean over a random sample of $R$ only.
- **Hash ripple join out of memory.** Luo, Ellmann, Haas and Naughton (2002) extend the hash ripple join to the case where the tuples read no longer fit in memory, by partitioning them to disk in the manner of a [Grace hash join](/grace-hash-join/).
- **More than two inputs.** The same idea works for $k$ inputs: each step extends a hyper-rectangle, and the estimate scales the sum by the product of the sampling fractions.
- **Wander join.** A [wander join](/wander-join/) does not read the inputs in order: it walks a random path through indexes from one tuple to a matching tuple, and weights each path by the inverse of its probability.

## When to use it

Use a ripple join when a user wants a fast approximate answer to an aggregate over a join of large tables and is ready to stop early, and the tables can be read in random order. It works best when the join has many results, so that a small rectangle already contains many joining pairs. For a join with very few results, most of the early rectangle contains nothing and the interval stays wide for a long time.

## Pitfalls

- **Input that is not in random order.** If the tables are sorted or clustered, a prefix is not a random sample and the estimate is biased. The orders must also be independent of each other.
- **Selective joins.** When few pairs join, the variance is large compared with $\tau^2$, and the interval from the central limit theorem can be too narrow for small samples.
- **Reusing the interval at every step.** A 95% interval at each step does not give 95% confidence that all intervals hold at once. A user who stops when the interval looks good needs an interval that holds over all steps.
- **Memory.** The memory grows with the tuples read, as in a symmetric hash join.
- **AVG.** The AVG estimate is biased for small samples, and its interval needs the delta method for the ratio.

## Implementations

## History

Hellerstein, Haas and Wang (1997) proposed online aggregation for single-table queries in a relational system, with running estimates and confidence intervals. Haas and Hellerstein (1999) introduced ripple joins to extend online aggregation to joins, as a family that includes block, index and hash ripple joins, and they gave confidence intervals based on a central limit theorem and a rule for choosing the aspect ratio during the run. Luo, Ellmann, Haas and Naughton (2002) made the hash ripple join scale beyond memory. Later work, such as wander join, sampled join paths through indexes instead of rectangles.

## References
