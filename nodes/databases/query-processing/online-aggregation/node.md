---
tag: NT88SJ
kind: technique
slug: online-aggregation
name: Online aggregation
aliases:
- progressive aggregation
area: databases/query-processing
level: advanced
summary: "Read the input of an aggregate query in random order and keep a running estimate of each answer with a confidence interval, so that the user can stop as soon as the answer is good enough."
prereqs: [group-by-aggregation, random-sampling, confidence-interval]
see_also: [ripple-join, wander-join, central-limit-theorem, hoeffding-inequality, stratified-sampling, reservoir-sampling, hash-aggregation, iterator-model]
sources:
  - paper: doi:10.1145/253260.253291
    title: "Joseph M. Hellerstein, Peter J. Haas and Helen J. Wang, Online aggregation, SIGMOD 1997, pages 171 to 182"
    locator: the online aggregation interface (running estimates, confidence intervals, stopping a group) for single-table aggregate queries with GROUP BY
  - paper: doi:10.1145/304182.304208
    title: "Peter J. Haas and Joseph M. Hellerstein, Ripple joins for online aggregation, SIGMOD 1999, pages 287 to 298"
    locator: online aggregation over joins with ripple joins and confidence intervals based on a central limit theorem
  - paper: doi:10.1080/01621459.1963.10500830
    title: "Wassily Hoeffding, Probability inequalities for sums of bounded random variables, Journal of the American Statistical Association 58(301), 1963, pages 13 to 30"
    locator: the bound for sums of bounded independent variables and its extension to sampling without replacement from a finite population
---

Online aggregation is the technique of answering an aggregate query, such as an AVG or SUM with GROUP BY, with an estimate that improves while the query runs, instead of one exact answer at the end. The system reads the input in random order, so that the tuples read so far are a random sample, and after each batch it reports for each group an estimate and a [confidence interval](/confidence-interval/) from a [central limit theorem](/central-limit-theorem/) or from [Hoeffding's inequality](/hoeffding-inequality/). The user can stop the query, or one group, as soon as the interval is narrow enough, and if nobody stops it, the last estimate is the exact answer. A plain [group-by aggregation](/group-by-aggregation/) gives nothing until the end. A [ripple join](/ripple-join/) extends the technique to joins.

## In plain words

You want the average salary in each department of a large company. The exact answer needs every record, which takes an hour. But after a few thousand random records you already know the averages quite well.

So the system takes the records in a random order and shows you the running average of each department, with a range that says how sure it is, for example "52,300, give or take 800". Every second the numbers change a little and the ranges get smaller. Small departments have wider ranges, because fewer of their records have come in.

When the ranges are small enough for your purpose, you stop. If you never stop, the system reads everything, and the last numbers are the exact ones.

## When it applies

- The query computes SUM, COUNT or AVG, which are sums or ratios of sums. Each estimate is a scaled sample sum. MIN, MAX and COUNT DISTINCT do not have simple unbiased estimates from a sample and need other methods.
- The input can be read in random order: the table is stored in random order, it is read through a random permutation of its pages or tuples, or an index gives random access. A prefix of a random order is a uniform random sample without replacement.
- An approximate answer early is worth more than an exact answer late, as in data exploration. Results that must be exact, such as a bill, need the full run.
- Each step of the query plan can output partial results, so the plan must not have a blocking operator, such as a sort, before the aggregate.

## The template

```pseudo id=main
ONLINE-AGGREGATE(T, g, x, z)          ▷ SELECT g, SUM(x), COUNT(*), AVG(x) FROM T GROUP BY g, with |T| = N
L1  read T in a random order
L2  for i ← 1 to N do
L3      t ← the i-th tuple; in the group h = g(t): c_h ← c_h + 1, s_h ← s_h + x(t), q_h ← q_h + x(t)²
L4      every so often, for each group h: report SUM ≈ (N/i) s_h, COUNT ≈ (N/i) c_h, AVG ≈ s_h / c_h, each with a half width
L5  at i = N every estimate is the exact answer
```

For AVG, the large-sample half width is $z \sqrt{(1 - i/N)\, v_h / c_h}$, where $v_h = (q_h - s_h^2 / c_h) / (c_h - 1)$ is the sample variance of the group and $z = 1.96$ for 95%. If every value lies in $[a, b]$, Hoeffding's inequality gives the conservative half width $(b - a) \sqrt{\ln(2/\delta) / (2 c_h)}$ for confidence $1 - \delta$. Hoeffding (1963) showed that the bound also holds for sampling without replacement.

**Why it works.** After $i$ tuples, the tuples read are a uniform random subset of size $i$ of $T$, so each tuple is in it with probability $i/N$. The SUM estimate is $\frac{N}{i} \sum_{t \text{ read}} x(t) [g(t) = h]$, and by [linearity of expectation](/linearity-of-expectation/) its mean is the true sum of the group. The COUNT estimate is the case $x = 1$. For AVG, given that $c_h = c \ge 1$ tuples of group $h$ have been read, every set of $c$ tuples of the group is equally likely, so the tuples read from the group are a random sample of it, and their mean is an unbiased estimate of the group mean. The sample mean of a random sample of size $c$ without replacement from $N_h$ values has variance $(1 - c/N_h) S_h^2 / c$, which the formula estimates with $c/N_h \approx i/N$ and $v_h$ for $S_h^2$. At $i = N$ the sample is the whole table.

**Cost.** Each tuple costs $O(1)$ updates of three numbers in its group, the same as a [hash aggregation](/hash-aggregation/). Each report costs $O(G)$ for $G$ groups. The width of each interval shrinks like $1/\sqrt{c_h}$, so halving the width of a group needs four times as many of its tuples.

**Example.** Let $T$ hold 10 tuples (group, $x$): $(a, 4), (b, 10), (a, 6), (a, 2), (b, 14), (a, 8), (b, 12), (a, 5), (a, 7), (b, 8)$. The exact answers are AVG$(a) = 16/3 \approx 5.33$, AVG$(b) = 11$ and SUM$(b) = 44$. Let the random order be $b{:}12, a{:}7, b{:}8, a{:}5, a{:}8, a{:}2, a{:}4, b{:}14, b{:}10, a{:}6$, with a report every 2 tuples.

| tuples read $i$ | AVG$(a)$ estimate | AVG$(b)$ estimate | SUM$(b)$ estimate $\frac{10}{i} s_b$ |
|---|---|---|---|
| 2 | 7 | 12 | 60 |
| 4 | 6 | 10 | 50 |
| 6 | 5.5 | 10 | 33.3 |
| 8 | 5.2 | 11.33 | 42.5 |
| 10 | 5.33 | 11 | 44 |

At $i = 8$ the large-sample half width of AVG$(a)$ is 0.94 and that of AVG$(b)$ is 1.55. With $[a, b] = [0, 20]$ and $\delta = 0.05$, Hoeffding's half widths are 12.15 and 15.68: they are safe for any data in the range, but much wider. On 300 random orders of a table of 200 tuples in 3 groups with values from 0 to 99, the Hoeffding intervals held the true group averages in every case after 20, 50 and 100 tuples, and the large-sample intervals held in 87%, 93% and 93% of the cases. These are measurements of a simulation.

## Classic examples

- **Single-table GROUP BY.** Hellerstein, Haas and Wang (1997) gave the interface: a running estimate and interval per group, with a control to stop a group whose estimate is good enough, so that the remaining work goes to the other groups.
- **Joins.** A [ripple join](/ripple-join/) reads both inputs of a join in random order and scales the sum over the pairs seen, which keeps the SUM estimate unbiased.
- **Joins through indexes.** A [wander join](/wander-join/) samples random join paths through indexes and weights each path by the inverse of its probability, in the manner of a [Horvitz and Thompson estimator](/horvitz-thompson-estimator/).
- **Approximate query answering from samples.** A system can keep a [stratified sample](/stratified-sampling/) or a [reservoir sample](/reservoir-sampling/) of each table and answer from it first, the same estimators applied to a stored sample.

## Variations

- **Fair access to groups.** In a random order, a small group gets few tuples and its interval stays wide. If an index on the grouping column exists, the system can read the groups in turn through the index (index striding), so that each group gets tuples at a rate that the user controls.
- **Conservative and large-sample intervals.** Hoeffding intervals hold for every sample size but need bounds on the values and are wide. Intervals from the central limit theorem are narrower and need large samples.
- **Intervals over time.** A user who watches the interval and stops when it looks good is testing at many times. An interval that holds at all times at once needs a wider bound, for example a union bound over the reporting times.
- **Block sampling.** Reading random pages instead of random tuples is much cheaper on disk, but tuples on one page are often alike, which makes the variance larger than the formula for tuples says.

## Pitfalls

- **Input in storage order.** If the table is sorted or clustered, for example by date, a prefix is not a random sample, and the estimates are biased until the end.
- **AVG of a group with one tuple.** The sample variance needs two tuples. With one, the large-sample interval has no meaning, and the implementation reports width 0, which must not be read as certainty.
- **Small groups and outliers.** A group with few tuples, or with a few very large values, has an estimate that can be far off with a narrow interval from the central limit theorem. Hoeffding's interval needs the bounds of the column, which are often only known loosely.
- **Blocking operators.** A sort, a hash join that builds first, or an ORDER BY before the aggregate stops the running estimates until it finishes.
- **The final answer.** The estimates are exact only at $i = N$. A group that has had all its tuples read before the end is exact too, but the system cannot know that without the group sizes.

## Exercises

1. Show that the COUNT estimate $\frac{N}{i} c_h$ is unbiased, and compute its variance for a group of size $N_h$ from the formula for sampling without replacement.
2. Show that the AVG estimate $s_h / c_h$ is unbiased given $c_h \ge 1$, but that the ratio $\frac{\text{SUM estimate}}{\text{COUNT estimate}}$ of two unbiased estimates is not unbiased in general for a ratio of two unknown sums.
3. Values lie in $[0, 100]$. How many tuples of a group does Hoeffding's interval need for a half width of 1 at 95%? How many does the large-sample interval need when the standard deviation of the group is 10?
4. A table is stored sorted by its aggregated column. Describe the running AVG estimate in storage order, and explain why its interval does not hold.

## References
