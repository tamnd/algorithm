---
tag: 32XY8A
kind: algorithm
slug: guaranteed-error-estimator
name: Guaranteed-error estimator
aliases:
- GEE distinct value estimator
area: databases/query-planning
level: advanced
summary: "Estimate the number of distinct values in a column from r random rows of n. Its bias is at most a factor 1 + sqrt(n/r), the order of the lower bound for every estimator that reads r rows."
solves: [distinct-elements-problem]
model: real-ram
complexity:
  vars: {n: the number of rows in the column, r: the number of rows in the sample}
  time: {expected: "O(r)"}
  space: {extra: "O(r)"}
properties: {deterministic: false, randomized: true, exact: false, recursive: false}
history:
  year: 2000
  people: [Moses Charikar, Surajit Chaudhuri, Rajeev Motwani, Vivek Narasayya]
  note: Given at PODS 2000 with a lower bound on the ratio error of every estimator that reads a sample of the rows.
prereqs: [cardinality-estimation, distinct-elements-problem]
see_also: [hyperloglog, kmv-sketch, selectivity, histogram, chao1-estimator, reservoir-sampling, estimation-error-propagation, linearity-of-expectation]
sources:
  - paper: "Moses Charikar, Surajit Chaudhuri, Rajeev Motwani and Vivek Narasayya, Towards estimation error guarantees for distinct values, Proceedings of ACM PODS 2000, 268 to 279"
    title: Towards estimation error guarantees for distinct values
    locator: the lower bound on the ratio error of every estimator that examines r of n rows, the estimator GEE and its expected ratio error of order sqrt(n/r), and the adaptive estimator AE
  - paper: "Phillip B. Gibbons, Distinct-values estimation over data streams, in Data Stream Management, Springer (2016)"
    title: Distinct-values estimation over data streams
    locator: Section 2.1 (sampling-based estimation) and Section 5, Theorem 7 (the lower bound of Charikar et al. restated, with sqrt((n - r)/(2r) ln(1/gamma)) and probability gamma)
  - paper: "Peter J. Haas, Jeffrey F. Naughton, S. Seshadri and Lynne Stokes, Sampling-based estimation of the number of distinct values of an attribute, Proceedings of VLDB 1995"
    title: Sampling-based estimation of the number of distinct values of an attribute
    locator: the earlier sampling estimators of the number of distinct values (Shlosser, the jackknife estimators and a hybrid of them)
---

The guaranteed-error estimator (GEE) estimates the number $D$ of distinct values in a column of $n$ rows from a uniform random sample of $r$ rows. If $f_j$ values occur exactly $j$ times in the sample, it returns $\sqrt{n/r}\, f_1 + \sum_{j \ge 2} f_j$. Charikar, Chaudhuri, Motwani and Narasayya gave it in 2000 together with a lower bound: every estimator that reads only $r$ of the $n$ rows has, on some column, a ratio error of order $\sqrt{n/r}$ with constant probability. GEE never overestimates by more than the factor $\sqrt{n/r}$, and its expected value is at least $D/(1 + \sqrt{n/r})$, so it reaches that order. This page is about one statistic that [cardinality estimation](/cardinality-estimation/) needs, the number of distinct values, which the [selectivity](/selectivity/) formulas of the optimizer divide by. It is also about one setting, a sample. Sketches such as [HyperLogLog](/hyperloglog/) and the [KMV sketch](/kmv-sketch/) solve the [distinct elements problem](/distinct-elements-problem/) with small relative error, but they read every row.

## In plain words

To count the different values in a large column, read a random part and count there. The values that show up two or more times in the part are probably common in the whole column, so each one counts once. A value that shows up only once is a sign of rare values: for each rare value the sample caught, there are probably many that it missed. GEE counts each value seen once as several values, and the number of copies grows with the ratio of the column size to the sample size.

No method can do much better from a sample. A column where one value fills almost every row looks the same in a small sample as a column that also holds many rare values. Any guess is then far off for one of the two columns. GEE stays within a constant factor of this limit.

## The problem

The input is a column of $n$ rows and a sample size $r$ with $1 \le r \le n$. The column has $D$ distinct values, and the goal is an estimate $\hat D$ of $D$. The algorithm may read only the values of $r$ rows. The measure is the ratio error $\max(\hat D/D,\ D/\hat D)$, which is 1 for an exact answer and treats an estimate that is 10 times too high like one that is 10 times too low. It is the q-error of the optimizer literature for this one number.

## The algorithm

```pseudo id=main
GEE(column of n rows, sample size r)
L1  S ← r rows of the column, drawn uniformly at random without replacement
L2  count the number of times each value occurs in S
L3  for each j ≥ 1, f_j ← the number of values that occur exactly j times in S
L4  return sqrt(n/r) · f_1 + (the sum of f_j over j ≥ 2)
```

The vector $(f_1, f_2, \ldots)$ is the frequency profile of the sample. With $d = \sum_j f_j$, the number of distinct values in the sample, the result is $d + (\sqrt{n/r} - 1) f_1$: the sample count, plus $\sqrt{n/r} - 1$ extra values for each value seen once. The code takes the profile from any sampler, so it also works on a sample that the system already keeps, for example a reservoir sample of a table.

## Example

A column of $n = 16$ rows holds the value a in 8 rows, b in 4 rows, and c, d, e and f in one row each, so $D = 6$. Take $r = 4$, so $\sqrt{n/r} = 2$. The sample a, a, b, e has $f_1 = 2$ (b and e) and $f_2 = 1$ (a). GEE returns $2 \cdot 2 + 1 = 5$, a ratio error of $6/5 = 1.2$.

The 1820 possible samples of 4 rows give these estimates:

| estimate | 1 | 2 | 3 | 5 | 8 |
|---|---|---|---|---|---|
| samples | 71 | 168 | 496 | 844 | 241 |

The estimate 1 comes from the 70 samples that hold only a and the one sample that holds only b. The mean is $8043/1820 \approx 4.42$, which is above the bound $D/(1 + 2) = 2$ of the correctness section. The largest estimate, 8, is below $2D = 12$. The mean ratio error over all samples is about 1.79, and the worst is 6, on the samples that see only one value.

## Correctness

The proof file proves two facts. First, for every sample, $d \le \hat D \le \sqrt{n/r}\, d \le \sqrt{n/r}\, D$, because $f_1 \le d \le D$. Second, $E[\hat D] \ge D/(1 + \sqrt{n/r})$. The key step is a property of sampling without replacement: for a value with $m$ rows, the probability that the sample misses it is at most $n/r$ times the probability that the sample holds it exactly once. So the expected number of missed values is at most $(n/r)\,E[f_1]$, and the extra weight that GEE puts on $f_1$ covers it within the factor $1 + \sqrt{n/r}$.

The proof file also proves the lower bound. For $\gamma \ge e^{-r}$, let $K = \frac{n - r}{2r}\ln\frac{1}{\gamma}$. A column of one value and a column with $\lfloor K \rfloor$ extra singletons give the same sample with probability at least $\gamma$, so an estimator that sees only that sample is off by at least $\sqrt{K}$ on one of them. With $n/r = 100$ and $\gamma = 1/2$, this is a ratio error of at least 5.86. The proof here gives probability $\gamma/(1+\gamma)$ for randomized estimators; Charikar et al. state probability $\gamma$.

A guarantee on the expected estimate is not a guarantee on each run. On a column of one common value and $n/r$ singletons, the sample misses all singletons with probability near $1/e$, and then GEE returns 1 for a true value of $n/r + 1$.

## Complexity

The work is in the sample. Lines L2 and L3 use a hash table on the values of the sample, so they take $O(r)$ expected time and $O(r)$ space, and line L4 adds up at most $r$ numbers. Drawing the sample takes $O(r)$ time when rows can be read by position. On disk it can cost up to $r$ page reads, and a block sample (all rows of some pages) is cheaper but is not a uniform row sample. GEE never reads the other $n - r$ rows; that is the point of the method.

## Properties

- **Never far too high.** The estimate is at most $\sqrt{n/r}$ times the true count on every sample. This is a theorem.
- **Bounded bias downward.** Its expected value is at least $D/(1 + \sqrt{n/r})$. This is a theorem.
- **Optimal order.** Every estimator that reads $r$ of $n$ rows has ratio error of order $\sqrt{n/r}$ on some column with constant probability, so no estimator gains more than a constant factor on the worst column. This is the lower bound of Charikar et al.
- **Exact on the whole column.** With $r = n$, it returns the true count.
- **Uses only the profile.** It needs $f_1$ and the sample count $d$, nothing else.

## Variants and improvements

- **AE.** The same paper gives the adaptive estimator AE, which fits the number of rare values to the low part of the profile ($f_1$, $f_2$, and so on). It is often more accurate on real data, without the worst-case guarantee of GEE.
- **Classic sampling estimators.** Haas, Naughton, Seshadri and Stokes (1995) compared the Shlosser estimator, jackknife estimators and a hybrid that picks one by a test of skew. These estimators can be better on many columns and much worse on some.
- **Species estimators.** Statistics has the same problem as the number of species in a population. The [Chao1 estimator](/chao1-estimator/) uses $f_1$ and $f_2$ in a similar way.
- **Sketches over all the data.** If the system can read every row once, for example while it builds a [histogram](/histogram/), a [HyperLogLog](/hyperloglog/) or [KMV](/kmv-sketch/) sketch gives a small relative error in small space, and the lower bound of this page does not apply.

## When to use it

Use it when the number of distinct values of a column is needed and only a sample can be read: statistics collection on a large table, or a quick estimate during optimization. Use it when a safe worst-case error matters more than the best average accuracy. If a full scan is possible, a sketch is far more accurate. If the column is known to have few values, the sample count $d$ is often already exact.

## Pitfalls

- **Expecting a small error from a small sample.** With a 1 percent sample, every estimator can be off by a factor of about 6 on some columns. The lower bound is about the problem, not about GEE.
- **Reading the guarantee as a bound per run.** The theorem bounds the expected estimate. One estimate can be much worse, as the example with $n/r$ singletons shows.
- **A sample that is not uniform.** Block samples, or the first rows of a table, break the analysis. Rows that are sorted or clustered on the column make $f_1$ too small.
- **Sampling with or without replacement.** The proof here uses a sample without replacement. With replacement, the same row can be drawn twice and looks like a repeated value, which lowers $f_1$; use the row identifier to remove repeats first.
- **Integer arithmetic.** $\sqrt{n/r}$ is not an integer in general; compute the estimate in floating point and round only at the end.

## Implementations

## History

The database literature had several sampling estimators for distinct values by 1995, among them those of Haas, Naughton, Seshadri and Stokes, and no method was good on all columns. In 2000 Moses Charikar, Surajit Chaudhuri, Rajeev Motwani and Vivek Narasayya proved that this is not a lack of skill: any estimator that reads a small sample has a large ratio error on some column. They designed GEE so that its error matches the order of this lower bound, and gave AE as a practical companion. Later surveys of distinct-value estimation, such as the one by Gibbons, restate the lower bound as the reason that streaming sketches, which see all rows, are needed for accurate counts.

## References
