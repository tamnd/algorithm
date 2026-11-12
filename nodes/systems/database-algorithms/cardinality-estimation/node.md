---
tag: 44064B
kind: problem
slug: cardinality-estimation
name: Cardinality estimation
aliases:
- result size estimation
- query result size estimation
- intermediate result size estimation
area: systems/database-algorithms
level: advanced
summary: "Estimate the number of tuples that a query or subplan returns, from statistics, samples or sketches, without running it. Errors grow fast with the number of joins."
prereqs: [selectivity]
see_also: [histogram, join-size-estimation-problem, ams-sketch, hyperloglog, count-min-sketch, bernoulli-sampling, reservoir-sampling, agm-bound]
sources:
  - paper: "Yannis E. Ioannidis and Stavros Christodoulakis, On the propagation of errors in the size of join results, Proceedings of ACM SIGMOD 1991, 268 to 277"
    title: On the propagation of errors in the size of join results
    locator: the result that the error in the estimated size of a join result grows exponentially with the number of joins
  - paper: doi:10.14778/2850583.2850594
    title: Viktor Leis, Andrey Gubichev, Atanas Mirchev, Peter Boncz, Alfons Kemper and Thomas Neumann, How good are query optimizers, really?, Proceedings of the VLDB Endowment 9(3) (2015), 204 to 215
    locator: Section 2 (the Join Order Benchmark on the IMDB data set) and Section 3 (the cardinality estimates of several systems against the true sizes, by number of joins)
  - paper: doi:10.1145/582095.582099
    title: P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie and T. G. Price, Access path selection in a relational database management system, Proceedings of ACM SIGMOD 1979, 23 to 34
    locator: Section 4, Table 1, p. 26 (selectivity factors, including 1/MAX(ICARD1, ICARD2) for an equijoin predicate)
  - paper: "Noga Alon, Phillip B. Gibbons, Yossi Matias and Mario Szegedy, Tracking join and self-join sizes in limited storage, Proceedings of ACM PODS 1999, 10 to 20"
    title: Tracking join and self-join sizes in limited storage
    locator: the unbiased sketch estimate of a join size and its variance bound in terms of the self-join sizes
  - paper: "Moses Charikar, Surajit Chaudhuri, Rajeev Motwani and Vivek Narasayya, Towards estimation error guarantees for distinct values, Proceedings of ACM PODS 2000, 268 to 279"
    title: Towards estimation error guarantees for distinct values
    locator: the lower bound on the ratio error of any estimator of the number of distinct values that reads a sample of the rows
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2008)
    locator: Chapter 16 (estimating the sizes of selections, joins and other operations from the counts of distinct values)
---

Cardinality estimation is the problem of estimating the number of tuples in the result of a query, or of each subexpression of a plan, before the query runs. The [query optimizer](/query-optimization/) needs these numbers for every candidate subplan, because the [cost model](/cost-model/) charges each operator by the size of its inputs and the [join ordering](/join-ordering/) search compares plans by these costs. Estimates come from precomputed statistics ([histograms](/histogram/), counts of distinct values), from samples, or from sketches, combined under assumptions of uniformity and independence. The problem is hard in practice: Ioannidis and Christodoulakis (1991) showed that errors grow exponentially with the number of joins, and Leis et al. (2015) measured errors of many orders of magnitude in real systems on the Join Order Benchmark.

## In plain words

Before the database runs a query, it must guess how many rows each step will produce. A step that makes ten rows is cheap to feed into the next step. A step that makes ten million rows is not. The guesses decide which plan the database picks.

The database cannot count the rows, because that would mean running the query. So it guesses from small summaries: how many rows a table has, how many different values a column has, a [histogram](/histogram/) of the values, or a small random sample. For one filter the guesses are often good. But a query with many joins multiplies many guesses, and the errors multiply too. A guess that is off by a factor of two at each of ten joins is off by a factor of about a thousand at the end.

## Definition

**Input.** A query $Q$ (a relational algebra expression, often a select-project-join query with grouping) and a summary $\Sigma(D)$ of the database $D$, much smaller than $D$. The summary can hold table sizes, per-column statistics, histograms, samples and sketches.

**Output.** An estimate $\hat{c}$ of $c = |Q(D)|$.

**Error.** The usual measure is the *q-error* $\max(\hat{c}/c,\; c/\hat{c})$ (with both at least 1), which treats overestimates and underestimates alike and is the factor by which the estimate is off. Costs, and so plan choices, depend on ratios of sizes, which makes a ratio measure more relevant than an absolute error.

## Variants

- **Single-table predicates.** Estimate the [selectivity](/selectivity/) of conjunctions and disjunctions of predicates on one table. Correlated columns are the main difficulty.
- **Join size.** Estimate $|R \bowtie S|$, or the size of a multiway join. With the frequency $f_v$ of value $v$ in $R.a$ and $g_v$ in $S.a$, the exact size of an equijoin is $\sum_v f_v g_v$, an inner product of two frequency vectors.
- **Distinct values.** Estimate the number of groups of a GROUP BY, or the number of distinct values that the join formula needs.
- **Static or streaming.** In the optimizer the statistics are built in advance and queried many times. The streaming [join size estimation problem](/join-size-estimation-problem/) asks for a join size over data that arrive once, in small memory; it is the special case of one equijoin of two streams, and its sketches can serve as optimizer statistics.
- **Upper bounds.** Some optimizers want a guaranteed upper bound in place of a best guess, so that they never pick a plan whose intermediate result is unexpectedly huge.

## Examples

**The classic formulas.** Let $R(a, b)$ have 10 000 tuples, with $V(R, a) = 100$ distinct values of $a$, and $S(a, c)$ 5000 tuples with $V(S, a) = 50$. Under uniformity and *containment of value sets* (the values of the side with fewer distinct values all occur in the other), the System R estimate is

$$|R \bowtie_a S| \approx \frac{|R| \cdot |S|}{\max(V(R, a), V(S, a))} = \frac{10\,000 \cdot 5000}{100} = 500\,000.$$

Each of the 50 values of $S.a$ is assumed to match $10\,000/100 = 100$ tuples of $R$, and $5000 \cdot 100 = 500\,000$. If $R.a$ is skewed so that the 50 values in $S$ occur only 10 times each in $R$, the true size is $5000 \cdot 10 = 50\,000$, a q-error of 10.

**Errors multiply.** Take a chain of $k$ joins, and let each join estimate be off by a factor 2 in the same direction (for example, because each join predicate is correlated with the previous ones). The estimate of the whole result is off by $2^k$: a factor 1024 for $k = 10$. Errors that are independent and in random directions partly cancel, but their spread still grows with $k$. Ioannidis and Christodoulakis (1991) gave this exponential growth a precise form.

**Join sampling loses matches.** Take Bernoulli samples of $R$ and $S$ with rate $p$ each. A joining pair survives only if both of its tuples do, so the join of the samples has expected size $p^2 |R \bowtie S|$. With $|R \bowtie S| = 10^6$ and $p = 0.01$, about 100 pairs are expected, and if the join is selective there can be none. Scaling by $1/p^2$ gives an unbiased estimate with a large variance.

## Known algorithms

- **Formulas from simple statistics.** Table sizes, distinct counts and min and max values, combined under uniformity, independence and containment, as in System R. They are fast and need almost no space, and they are the default in most systems.
- **[Histograms](/histogram/)** per column capture skew within one column. Most common value lists capture heavy hitters. Multidimensional histograms capture some correlations. Join sizes come from aligning the histograms of the two join columns bucket by bucket.
- **Sampling.** A [Bernoulli sample](/bernoulli-sampling/) or a sample kept by [reservoir sampling](/reservoir-sampling/) estimates the selectivity of any predicate on one table, correlated or not, with an error that shrinks like $1/\sqrt{\text{sample size}}$ for selectivities that are not too small. For joins, sampling both sides loses most matches (above), so systems sample one side and probe the other through an index, or sample join results directly.
- **Sketches.** The [AMS sketch](/ams-sketch/) gives an unbiased estimate of $\sum_v f_v g_v$ whose variance is at most twice the product of the self-join sizes. The [count-min sketch](/count-min-sketch/) estimates frequencies and gives an inner product estimate that never underestimates. [HyperLogLog](/hyperloglog/) estimates the number of distinct values with a relative error of about $1.04/\sqrt{m}$ for $m$ registers, which feeds the join formula and the size of GROUP BY results.
- **Worst-case bounds.** The [AGM bound](/agm-bound/) gives the largest possible size of a join query from the sizes of its relations, $\prod_i |R_i|^{x_i}$ for any fractional edge cover $x$; refinements use degree statistics. These bounds never underestimate but can be far above the true size.
- **Learned estimators.** Recent systems train models on queries or on the data to predict sizes; they can capture correlations but cost training time and can fail on new kinds of queries.
- **Feedback and adaptivity.** Systems can record the true sizes seen during execution and correct later estimates, or reoptimize a query when an observed size differs too much from the estimate.

## Bounds

- **Error propagation.** Under the independence assumption, a multiplicative error at each join compounds; the error of the result of $k$ joins can be the product of $k$ such factors. On the Join Order Benchmark (113 queries over the IMDB data, with 3 to 16 joins), Leis et al. (2015) found that all systems they tested underestimated most results of many joins, often by several orders of magnitude.
- **Distinct values from samples.** Charikar, Chaudhuri, Motwani and Narasayya (2000) proved that any estimator of the number of distinct values that reads $r$ of $n$ rows has a ratio error of order $\sqrt{n/r}$ on some input, with a constant probability. So small samples cannot estimate distinct counts well in the worst case, and sketches that read all the data are preferable when they can be maintained.
- **Space against accuracy.** For the join size of two streams, sketches need space that grows with the ratio of the self-join sizes to the join size; no small summary estimates all small join sizes well. See the [join size estimation problem](/join-size-estimation-problem/).

## Reductions

- **Selectivity and cardinality.** The cardinality of $\sigma_p(E)$ is the selectivity of $p$ on $E$ times $|E|$, so estimating cardinalities of select-project-join queries reduces to estimating [selectivities](/selectivity/) of predicates over products.
- **Join size and inner products.** The size of an equijoin is the inner product of the frequency vectors of the join column, so any inner product estimator, such as the AMS sketch, estimates it.
- **Distinct counts and grouping.** The number of groups of a GROUP BY is the number of distinct values of the grouping columns, the problem that [HyperLogLog](/hyperloglog/) solves in a stream.

## Applications

Every cost-based optimizer uses cardinality estimates to choose join orders, join algorithms, access paths, memory grants and degrees of parallelism. Physical design tools use them to estimate the benefit of indexes and views. Approximate query processing systems return estimated aggregates from samples or sketches directly, with error bounds.

## References
