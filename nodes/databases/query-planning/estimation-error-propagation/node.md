---
tag: ZDG38A
kind: theorem
slug: estimation-error-propagation
name: Exponential propagation of estimation errors
aliases:
- Ioannidis-Christodoulakis error propagation
area: databases/query-planning
level: advanced
summary: "If each frequency that a join size estimate uses is off by at most a factor 1 + e, the estimate for a join of n relations is off by at most (1 + e)^n, and this bound is reached."
prereqs: [cardinality-estimation, attribute-value-independence]
see_also: [selectivity, histogram, join-ordering, cost-model, mid-query-reoptimization, pessimistic-cardinality-estimation, learned-cardinality-estimation, agm-bound]
sources:
  - paper: "Yannis E. Ioannidis and Stavros Christodoulakis, On the propagation of errors in the size of join results, Proceedings of ACM SIGMOD 1991, 268 to 277"
    title: On the propagation of errors in the size of join results
    locator: the result that, in their model of equality joins described by the frequencies of the join attribute values, the error of the estimated result size grows exponentially with the number of joins
  - paper: doi:10.1145/169725.169708
    title: Yannis E. Ioannidis and Stavros Christodoulakis, Optimal histograms for limiting worst-case error propagation in the size of join results, ACM Transactions on Database Systems 18(4) (1993), 709 to 748
    locator: histograms chosen to limit the worst-case error that propagates through joins
  - paper: "Guido Moerkotte, Thomas Neumann and Gabriele Steidl, Preventing bad plans by bounding the impact of cardinality estimation errors, Proceedings of the VLDB Endowment 2(1) (2009), 982 to 993"
    title: Preventing bad plans by bounding the impact of cardinality estimation errors
    locator: the q-error, the larger of estimate/truth and truth/estimate, and bounds on the cost of the chosen plan in terms of it
  - paper: doi:10.14778/2850583.2850594
    title: Viktor Leis, Andrey Gubichev, Atanas Mirchev, Peter Boncz, Alfons Kemper and Thomas Neumann, How good are query optimizers, really?, Proceedings of the VLDB Endowment 9(3) (2015), 204 to 215
    locator: Section 3 (measured cardinality estimates of several systems on the Join Order Benchmark, by number of joins)
---

This theorem says that small errors in the statistics of single relations can become large errors in the estimated size of a join result, and that the growth is exponential in the number of relations in the worst case. Ioannidis and Christodoulakis proved results of this kind in 1991, in a model where each relation is described by the frequencies of its join attribute values. This page states and proves a clean form of the result in an explicit model, shows that the bound is reached, and separates it from the measurements of real systems. The estimation problem itself is on the [cardinality estimation](/cardinality-estimation/) page.

## Statement

**Model.** Let $Q = R_1 \bowtie \cdots \bowtie R_n$ be a natural equality join of $n$ relations, with bag semantics. Call an attribute a join attribute if at least two of the relations have it, let $A_i$ be the join attributes of $R_i$, and let $X$ be the set of all assignments of values to the join attributes. For $y$ an assignment to $A_i$, let $f_i(y)$ be the number of tuples of $R_i$ whose values on $A_i$ are $y$. An estimator of the frequency kind has estimates $\hat f_i(y) \ge 0$ of these frequencies and returns

$$\hat S = \sum_{x \in X} \prod_{i=1}^{n} \hat f_i(x|_{A_i}),$$

where $x|_{A_i}$ is the restriction of $x$ to $A_i$. Histograms with a uniform frequency in each bucket, frequencies from a sample, and the classic formulas built on the number of distinct values all give estimators of this kind. The q-error of an estimate $\hat S$ of $S > 0$ is $\max(\hat S/S,\ S/\hat S)$.

**Theorem.** Let $S = |Q|$ and let $c \ge 1$.

1. If every frequency estimate satisfies $f_i(y)/c \le \hat f_i(y) \le c\, f_i(y)$, then $S/c^n \le \hat S \le c^n S$. So the q-error is at most $c^n$, for a join of $n$ relations, that is $n - 1$ joins.
2. The bound is reached: for every instance with $S > 0$, the estimates $\hat f_i = c\, f_i$ satisfy the hypothesis of part 1 and give $\hat S = c^n S$, and $\hat f_i = f_i / c$ gives $\hat S = S / c^n$.

## In plain words

To guess the size of a join, an optimizer multiplies guesses about each table. If each guess is a little too big, the product is too big by the small error times itself, once for each table. Ten tables that are each 10 percent too big give an answer that is about 2.6 times too big. Ten tables that are each twice too big give an answer that is a thousand times too big.

The theorem says that this is the worst that can happen when each table is off by a bounded factor, and that it really can happen. Real data adds a second problem: the guesses for different tables tend to be wrong in the same direction, so the errors do not cancel.

## Proof

**Lemma (the size of a join).** $S = \sum_{x \in X} \prod_{i=1}^{n} f_i(x|_{A_i})$.

*Proof.* A result tuple of $Q$ is a choice of one tuple $t_i$ from each $R_i$ such that any two chosen tuples agree on the attributes they share. Only join attributes are shared, so the chosen tuples agree exactly when there is one assignment $x \in X$ with $t_i|_{A_i} = x|_{A_i}$ for every $i$, and this $x$ is unique, because every join attribute is in some $A_i$. For a fixed $x$, the tuples $t_i$ can be chosen independently among the $f_i(x|_{A_i})$ tuples of $R_i$ with these values, which gives $\prod_i f_i(x|_{A_i})$ result tuples. Summing over $x$ counts each result tuple once. $\square$

**Part 1.** For each $x$, every factor satisfies $f_i(x|_{A_i})/c \le \hat f_i(x|_{A_i}) \le c\, f_i(x|_{A_i})$, and all the numbers are at least 0, so the products satisfy

$$c^{-n} \prod_i f_i(x|_{A_i}) \le \prod_i \hat f_i(x|_{A_i}) \le c^{n} \prod_i f_i(x|_{A_i}).$$

Sum over $x$ and use the lemma: $c^{-n} S \le \hat S \le c^n S$. When $S > 0$, this gives $\hat S/S \le c^n$ and $S/\hat S \le c^n$. $\square$

**Part 2.** With $\hat f_i = c\, f_i$, every product has the factor $c^n$, so $\hat S = c^n S$ by the lemma, and the q-error is $c^n$. The case $\hat f_i = f_i/c$ is the same with $c^{-n}$. $\blacksquare$

## Consequences

- **Numbers.** With $c = 1.1$ and $n = 10$, the bound is $1.1^{10} \approx 2.59$. With $c = 1.5$ it is about 57.7, and with $c = 2$ it is $1024$. A plan whose intermediate result is a thousand times larger than estimated can be the wrong plan, for example a nested loop join where a hash join was needed.
- **Errors in the same direction (a consequence of the proof).** If each relation is off by a factor $c_i$ in the same direction for all its frequencies, for example because a sample of the table was scaled wrongly, then $\hat S/S = \prod_i c_i$ exactly. In logarithms, $\log(\hat S/S) = \sum_i \log c_i$. If the $\log c_i$ are independent random variables with mean $\mu$ and variance $\sigma^2$, then $\log(\hat S/S)$ has mean $n\mu$ and variance $n\sigma^2$. So a systematic bias $\mu \ne 0$ makes the error grow exponentially in $n$, and errors with no bias still give a typical q-error of about $e^{\sigma\sqrt n}$, which also grows without limit.
- **Uniformity alone (an example in the model).** Even exact table sizes and exact distinct counts give exponential errors when the data is skewed. Let $R_1, \ldots, R_n$ each have 100 tuples on one join attribute $a$, with value $u$ in 99 tuples and value $w$ in 1 tuple. Then $S = 99^n + 1$. A uniform estimate uses $\hat f_i = 100/2 = 50$ for both values and gives $\hat S = 2 \cdot 50^n$. The ratio $S/\hat S$ is about 1.96 for $n = 2$, 15.2 for $n = 5$ and 463 for $n = 10$, close to $2^{n-1}$.
- **Measurements (not part of the theorem).** Leis et al. (2015) measured the estimates of several systems on the Join Order Benchmark over the IMDB data. The estimates were mostly too small, and the errors grew quickly with the number of joins, which matches the second consequence with $\mu < 0$. Correlated columns, handled by the [attribute value independence assumption](/attribute-value-independence/), are a main reason for the common direction.
- **What an optimizer can do.** Keep the error of each estimate small where it matters, as histograms built for joins try to do; use bounds instead of estimates, as [pessimistic cardinality estimation](/pessimistic-cardinality-estimation/) does; or check the sizes at run time and re-plan, as [mid-query re-optimization](/mid-query-reoptimization/) does. Moerkotte, Neumann and Steidl (2009) define the q-error and bound the extra cost of the chosen plan in terms of the q-errors of its estimates.

## Tightness

Part 2 of the theorem shows that the factor $c^n$ cannot be improved for any instance: the estimates that are off by exactly $c$ in the same direction for every frequency reach it. The exponent $n$ is the number of relations, so a chain of $j$ joins has exponent $j + 1$. If the errors of the relations have different directions, they can cancel, and the bound is then far from the truth; the theorem gives only the worst case. If the hypothesis is weakened to an error of a factor $c$ in the total size of each relation, with no control of single frequencies, the q-error is not bounded at all: two relations of $N$ tuples each join in 0 tuples if their join values are disjoint and in $N^2$ tuples if all tuples have the same join value, while the sizes are the same.

## History

Ioannidis and Christodoulakis (1991) studied the size of the results of equality joins in a model that describes each relation by the frequency distribution of its join attribute values, and showed that the error of the estimate can grow exponentially with the number of joins. In 1993 they studied which histograms limit this worst-case growth. Moerkotte, Neumann and Steidl (2009) introduced the q-error as the measure of these errors that fits multiplication. Leis et al. (2015) built the Join Order Benchmark and measured the growth in real systems.

## References
