---
tag: RNYWEA
kind: concept
slug: selectivity
name: Selectivity
aliases:
- predicate selectivity
- selectivity factor
- reduction factor
- filter factor
area: systems/database-algorithms
level: intro
summary: "The fraction of tuples that satisfy a predicate. Optimizers estimate it from statistics, and assume independence and uniformity when they lack better data."
prereqs: [relational-algebra]
see_also: [cardinality-estimation, histogram, cost-model, query-optimization, selinger-join-enumeration, count-min-sketch, hyperloglog, bernoulli-sampling]
sources:
  - paper: doi:10.1145/582095.582099
    title: P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie and T. G. Price, Access path selection in a relational database management system, Proceedings of ACM SIGMOD 1979, 23 to 34
    locator: Section 4, Table 1, Selectivity factors, p. 26 (the defaults 1/10, 1/3 and 1/4, and the rules for AND, OR and NOT)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 15 (estimating the size of a result with reduction factors)
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2008)
    locator: Chapter 16 (estimating the sizes of selections and joins from the number of distinct values)
  - paper: doi:10.14778/2850583.2850594
    title: Viktor Leis, Andrey Gubichev, Atanas Mirchev, Peter Boncz, Alfons Kemper and Thomas Neumann, How good are query optimizers, really?, Proceedings of the VLDB Endowment 9(3) (2015), 204 to 215
    locator: the sections on cardinality estimation for base table predicates and for joins (correlated predicates in the IMDB data)
---

The selectivity of a predicate $p$ on a relation $R$ is the fraction of the tuples of $R$ that satisfy $p$. It is a number between 0 and 1, and a small selectivity means a strong filter. The [query optimizer](/query-optimization/) multiplies selectivities and relation sizes to estimate the sizes of intermediate results ([cardinality estimation](/cardinality-estimation/)), and these sizes drive the [cost model](/cost-model/). When it has no exact data, it assumes that values are spread evenly and that predicates on different columns are independent; both assumptions often fail.

## In plain words

Suppose a table has a thousand rows and a filter keeps fifty of them. The filter keeps one row in twenty. That fraction is its selectivity. To choose a good plan, the database must know how many rows each step will produce, before it runs anything. So it guesses each fraction from small summaries of the data: the number of rows, the number of different values in a column, the smallest and largest value, and sometimes a [histogram](/histogram/).

When a query has two filters, the usual guess multiplies the two fractions. That is right only if the two columns have nothing to do with each other. Real columns are often linked: a car model tells you the maker. Then the guess can be wrong by a large factor.

## The idea

### Definitions

Let $R$ be a relation with $|R| > 0$ tuples and let $p$ be a predicate on the tuples of $R$. The selectivity of $p$ is

$$\mathrm{sel}(p) = \frac{|\sigma_p(R)|}{|R|} \in [0, 1].$$

For a join predicate $p$ between $R$ and $S$, the selectivity is the fraction of pairs that match:

$$\mathrm{sel}(p) = \frac{|R \bowtie_p S|}{|R| \cdot |S|}.$$

The estimated size of a result is then a product: $|\sigma_p(R)| \approx \mathrm{sel}(p) \, |R|$, and $|R \bowtie_p S| \approx \mathrm{sel}(p) \, |R| \, |S|$. Some textbooks call $\mathrm{sel}(p)$ the *reduction factor* (Ramakrishnan and Gehrke) and System R called it the *selectivity factor* $F$.

### The statistics

An optimizer keeps, for each relation $R$ and column $A$: the number of tuples $|R|$, the number of distinct values $V(R, A)$, the minimum and maximum, and often a [histogram](/histogram/) and a list of the most common values. These are refreshed from time to time, not after each update, so they can be stale.

### The two assumptions

- **Uniformity.** Each of the $V(R, A)$ values occurs equally often, and the values of a range are spread evenly between the minimum and the maximum. Then $\mathrm{sel}(A = c) = 1/V(R, A)$, and for a numeric column with $lo < hi$, $\mathrm{sel}(A > c) = (hi - c)/(hi - lo)$ for $lo \le c \le hi$.
- **Independence.** The predicates on different columns are independent events for a tuple chosen uniformly from $R$. Then

$$\mathrm{sel}(p \wedge q) = \mathrm{sel}(p) \, \mathrm{sel}(q), \qquad \mathrm{sel}(p \vee q) = \mathrm{sel}(p) + \mathrm{sel}(q) - \mathrm{sel}(p) \, \mathrm{sel}(q).$$

The rule $\mathrm{sel}(\neg p) = 1 - \mathrm{sel}(p)$ needs no assumption in two-valued logic. The rule for $\vee$ is exact by inclusion and exclusion once the rule for $\wedge$ is exact.

For an equijoin $R.A = S.B$, the classic estimate adds a third assumption, *containment of value sets*: each value of the column with fewer distinct values also occurs in the other column. With uniformity this gives

$$\mathrm{sel}(R.A = S.B) = \frac{1}{\max(V(R, A), V(S, B))}.$$

*Derivation.* Say $V(R, A) \le V(S, B)$. By containment each value of $R.A$ occurs in $S.B$, and by uniformity it occurs $|S|/V(S, B)$ times there. So each tuple of $R$ matches $|S|/V(S, B)$ tuples, and $|R \bowtie S| = |R| \, |S| / V(S, B)$.

### The System R defaults

Selinger et al. (1979, Table 1) give these selectivity factors $F$, where ICARD is the number of distinct keys of an index on the column:

| predicate | with statistics | without |
|---|---|---|
| column = value | $1/\text{ICARD}$ | $1/10$ |
| column1 = column2 | $1/\max(\text{ICARD}_1, \text{ICARD}_2)$, or $1/\text{ICARD}_i$ with one index | $1/10$ |
| column > value | $(\text{high key} - \text{value})/(\text{high key} - \text{low key})$ | $1/3$ |
| column BETWEEN v1 AND v2 | $(v_2 - v_1)/(\text{high key} - \text{low key})$ | $1/4$ |
| column IN (list) | the list length times $F(\text{column} = \text{value})$, at most $1/2$ | |
| p AND q | $F(p) \, F(q)$ | |
| p OR q | $F(p) + F(q) - F(p) \, F(q)$ | |
| NOT p | $1 - F(p)$ | |

The paper says that the defaults have "no significance" beyond their order: an unknown range predicate should be less selective than an unknown equality, and keep less than half of the tuples. It also says that the AND rule assumes that column values are independent.

### What holds without assumptions

For any two predicates, the probability bounds of Fréchet give

$$\max(0, \ \mathrm{sel}(p) + \mathrm{sel}(q) - 1) \ \le \ \mathrm{sel}(p \wedge q) \ \le \ \min(\mathrm{sel}(p), \mathrm{sel}(q)).$$

*Proof.* $\sigma_{p \wedge q}(R)$ is a subset of $\sigma_p(R)$ and of $\sigma_q(R)$, which gives the upper bound. By inclusion and exclusion, $|\sigma_{p \wedge q}| = |\sigma_p| + |\sigma_q| - |\sigma_{p \vee q}| \ge |\sigma_p| + |\sigma_q| - |R|$; divide by $|R|$. $\square$

Both bounds are reached: the upper one when $p$ implies $q$, the lower one when $p$ and $q$ are disjoint and $\mathrm{sel}(p) + \mathrm{sel}(q) \le 1$. The independence estimate $\mathrm{sel}(p)\,\mathrm{sel}(q)$ always lies between them, so it can be wrong by any factor up to the ratio of the bounds.

## Examples

**Correlated predicates.** A table `Cars(make, model)` has 16 rows: 2 rows each of (Honda, Civic), (Honda, Accord), (Toyota, Corolla), (Toyota, Camry), (Ford, Focus), (Ford, Fiesta), (BMW, X3) and (BMW, M3).

| predicate | true selectivity | rows | independence estimate | estimated rows |
|---|---|---|---|---|
| make = Honda | 1/4 | 4 | | |
| model = Civic | 1/8 | 2 | | |
| make = Honda AND model = Civic | 1/8 | 2 | $1/4 \cdot 1/8 = 1/32$ | 0.5 |
| make = Toyota AND model = Civic | 0 | 0 | $1/32$ | 0.5 |
| make = Honda OR model = Civic | 1/4 | 4 | $1/4 + 1/8 - 1/32 = 11/32$ | 5.5 |

The model Civic implies the make Honda, so the first conjunction is as selective as `model = Civic` alone: the true value is the Fréchet upper bound $\min(1/4, 1/8)$, and the estimate is 4 times too small. The second conjunction is empty, which is the lower bound, and the estimate is too large. With $k$ such predicates in a chain of joins, the factors multiply.

**Skew breaks uniformity.** A column has the 20 values 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 7, 8, 9, 9, 10, 60, 75, 90, 100, so $lo = 1$ and $hi = 100$. For $A > 50$, linear interpolation gives $(100 - 50)/(100 - 1) = 50/99 \approx 0.505$, or about 10 rows. The true answer is 4 rows, a selectivity of $1/5$. An [equi-depth histogram](/histogram/) with 4 buckets of 5 values has the buckets $[1, 3]$, $[3, 5]$, $[6, 9]$ and $[10, 100]$. Only the last bucket meets the range, and interpolation inside it gives $5 \cdot 50/90 \approx 2.8$ rows. The error can be at most the 5 rows of that bucket.

**A join estimate.** $R$ has 1000 tuples with $V(R, A) = 10$, and $S$ has 500 tuples with $V(S, A) = 50$. The estimate is $1000 \cdot 500 / 50 = 10000$ tuples. If $R$ has the values 0 to 9, 100 times each, and $S$ has the values 0 to 49, 10 times each, the true size is $10 \cdot 100 \cdot 10 = 10000$, because containment and uniformity hold. If instead $S$ has the values 50 to 99, the true size is 0, and the estimate is wrong by an unbounded factor.

## Where it is used

- [Cardinality estimation](/cardinality-estimation/) builds the size of each intermediate result from the sizes of the base relations and the selectivities of the predicates applied so far. Its errors grow with the number of joins.
- The [cost model](/cost-model/) turns these sizes into page I/Os and CPU work, and the choice between an index scan and a full scan depends mostly on the selectivity of the predicate on the indexed column.
- [Join ordering](/join-ordering/) and [System R join enumeration](/selinger-join-enumeration/) put the most selective joins and filters early.
- [Predicate pushdown](/predicate-pushdown/) applies a filter as early as possible; the order of several filters at one place should put the cheap and selective ones first.
- Better statistics replace the assumptions: [histograms](/histogram/) replace uniformity inside one column; most common value lists and frequency sketches such as the [count-min sketch](/count-min-sketch/) estimate the selectivity of an equality; the number of distinct values $V(R, A)$ comes from a distinct-count sketch such as [HyperLogLog](/hyperloglog/); samples, for example a [Bernoulli sample](/bernoulli-sampling/), estimate the selectivity of a conjunction directly and so capture correlation, but they miss rare values. Statistics on groups of columns capture correlation between those columns.
- Leis et al. (2015) found on real data (the IMDB data of the Join Order Benchmark) that the estimates of the systems they tested were often wrong by orders of magnitude for queries with many joins, and that correlated predicates and joins are a main cause.

## References
