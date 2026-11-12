---
tag: BD9CER
kind: concept
slug: cost-model
name: Query cost model
aliases:
- query cost estimation
- plan cost function
- optimizer cost model
area: systems/database-algorithms
level: core
summary: "A formula that gives each physical query plan a number, mostly page I/O plus a weighted CPU term, so that the optimizer can compare plans without running them."
prereqs: [query-plan]
see_also: [selectivity, cardinality-estimation, block-nested-loop-join, sort-merge-join, grace-hash-join, index-nested-loop-join, join-ordering, index-selection]
sources:
  - paper: doi:10.1145/582095.582099
    title: P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie and T. G. Price, Access path selection in a relational database management system, Proceedings of ACM SIGMOD 1979, 23 to 34
    locator: Section 4, p. 25 (COST = PAGE FETCHES + W * (RSI CALLS)) and Table 2, p. 27 (the cost formulas for single relation access paths); Section 5 (the costs of nested loop and merge joins)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 14 (the I/O costs of the selection, projection and join algorithms) and Chapter 15 (cost estimation in a relational optimizer)
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2008)
    locator: Chapter 15 (the disk I/O costs of the physical operators) and Chapter 16 (cost-based plan selection)
  - url: https://www.postgresql.org/docs/current/using-explain.html
    title: PostgreSQL documentation, Using EXPLAIN
    locator: the first examples on the table tenk1 (358 pages and 10000 rows give the cost 358 * seq_page_cost + 10000 * cpu_tuple_cost = 458; a WHERE clause adds 10000 * cpu_operator_cost)
  - paper: "Sophie Cluet and Guido Moerkotte, On the complexity of generating optimal left-deep processing trees with cross products, Proceedings of ICDT 1995, LNCS 893, 54 to 67"
    title: On the complexity of generating optimal left-deep processing trees with cross products
    locator: the cost function C_out, the sum of the sizes of the intermediate results
  - paper: doi:10.14778/2850583.2850594
    title: Viktor Leis, Andrey Gubichev, Atanas Mirchev, Peter Boncz, Alfons Kemper and Thomas Neumann, How good are query optimizers, really?, Proceedings of the VLDB Endowment 9(3) (2015), 204 to 215
    locator: the section on cost models (a simple main-memory cost function against the PostgreSQL cost model, with true and estimated cardinalities)
---

A cost model is the function that the [query optimizer](/query-optimization/) uses to rank the physical [query plans](/query-plan/) of a query. It gives each operator a cost from the estimated sizes of its inputs and outputs and from the resources it uses, and it adds these costs up the plan tree. The classic models count page reads and writes, because disk I/O was the slow part; System R used $\text{COST} = \text{PAGE FETCHES} + W \cdot \text{RSI CALLS}$, where the second term counts tuples passed to the upper layer and $W$ sets the weight of CPU against I/O. A cost model is only as good as its inputs: the sizes come from [selectivity](/selectivity/) and [cardinality estimates](/cardinality-estimation/), and errors there matter more than errors in the formulas.

## In plain words

One query can run in many ways. You can read a table from start to end or jump into it through an index. You can join two tables with a loop, by sorting them, or with a hash table. The optimizer must pick one way before it runs anything. So it needs a quick way to say which plan is cheaper.

A cost model is that quick way. It is a set of simple formulas. Each formula takes the sizes of the inputs and gives a number, usually the number of disk pages that the step reads and writes, plus a smaller charge for the work of the processor. The cost of a plan is the sum over its steps. The number is not a time in seconds. It only has to put the plans in the right order.

## The idea

**What is counted.** A cost model picks the resources that dominate the run time and counts them:

- **I/O.** The number of pages read and written. Sequential reads are cheaper than random reads, so many systems charge them differently. PostgreSQL, for example, charges `seq_page_cost` = 1 for a page read in sequence and `random_page_cost` = 4 by default for a page read at random.
- **CPU.** A charge per tuple processed and per predicate or operator evaluated. System R charged $W$ per tuple returned by the storage layer (an RSI call).
- **Memory.** Not a cost in itself, but a parameter: the number $B$ of buffer pages that an operator can use changes its I/O cost, as in the formulas below.
- **Network.** In a distributed system, messages and bytes sent.

The cost of a plan is the sum of the costs of its operators. An operator's cost depends on the sizes of its inputs, so the model needs the estimated number of tuples and pages for every edge of the plan; those come from cardinality estimation.

**System R.** Selinger et al. (1979) gave formulas for each access path. For a relation with $NCARD$ tuples on $TCARD$ pages, and $RSICARD$ the expected number of tuples returned to the upper layer:

| access path | cost |
|---|---|
| unique index, equality predicate | $1 + 1 + W$ |
| clustered index $I$ with matching predicates | $F(\text{preds}) \cdot (NINDX(I) + TCARD) + W \cdot RSICARD$ |
| non-clustered index $I$ with matching predicates | $F(\text{preds}) \cdot (NINDX(I) + NCARD) + W \cdot RSICARD$ |
| segment scan | $TCARD / P + W \cdot RSICARD$ |

Here $F(\text{preds})$ is the selectivity of the predicates that the index matches, $NINDX(I)$ is the number of pages of the index, and $P$ is the fraction of the segment's pages that hold tuples of the relation. A [clustered index](/clustered-index/) reads each data page once; a non-clustered one can read a page once per tuple. For joins, the cost of a nested loop join of an outer path with $N$ tuples and an inner path is $C_{\text{outer}} + N \cdot C_{\text{inner}}$; a merge join has the same form, where the inner cost is that of scanning a sorted inner.

**Textbook join formulas.** Let $R$ have $M$ pages with $p_R$ tuples per page, let $S$ have $N$ pages, and let $B$ be the number of buffer pages. The I/O costs, without the cost of writing the result, are:

| algorithm | I/O cost |
|---|---|
| tuple-at-a-time [nested loop join](/nested-loop-join/) | $M + p_R \cdot M \cdot N$ |
| page-at-a-time nested loop join | $M + M \cdot N$ |
| [block nested loop join](/block-nested-loop-join/) | $M + \lceil M/(B - 2) \rceil \cdot N$ |
| [index nested loop join](/index-nested-loop-join/) | $M + p_R \cdot M \cdot c_{\text{probe}}$ |
| [sort-merge join](/sort-merge-join/), inputs not sorted, two-pass sort | $5(M + N)$, or $3(M + N)$ if the last merge pass feeds the join |
| [Grace hash join](/grace-hash-join/), $B > \sqrt{\min(M, N)}$ about | $3(M + N)$ |

Here $c_{\text{probe}}$ is the cost of one index lookup plus the fetch of the matching tuples. Each formula assumes something about memory and data: the sort-merge and hash formulas assume about $\sqrt{M}$ buffer pages and no heavy skew, and the [hybrid hash join](/hybrid-hash-join/) is cheaper than $3(M + N)$ when part of the build input fits in memory.

**A logical cost function.** For join ordering, a simpler function is often used: $C_{\text{out}}(T)$, the sum of the cardinalities of all intermediate results of the plan $T$. It ignores the join algorithm, but it captures the main effect (large intermediate results are expensive), and the hardness results for [join ordering](/join-ordering/) use it.

**Properties the optimizer needs.** The [Selinger enumeration](/selinger-join-enumeration/) builds the best plan for a set of relations from the best plans for its subsets. That is valid only if the cost of a plan is a monotone function of the costs of its subplans (and of properties such as sort order, which the DP tracks separately). Sums of operator costs have this property. Polynomial algorithms for special cases need more: the IKKBZ algorithm needs a cost function with the adjacent sequence interchange (ASI) property.

## Examples

**Choosing a join algorithm.** Let $R$ have $M = 1000$ pages with $p_R = 100$ tuples per page, let $S$ have $N = 500$ pages, and let $B = 102$ buffer pages. The formulas give:

| plan | I/O cost |
|---|---|
| tuple-at-a-time nested loop, $R$ outer | $1000 + 100 \cdot 1000 \cdot 500 = 50\,001\,000$ |
| page-at-a-time nested loop, $R$ outer | $1000 + 1000 \cdot 500 = 501\,000$ |
| block nested loop, $R$ outer | $1000 + \lceil 1000/100 \rceil \cdot 500 = 6000$ |
| block nested loop, $S$ outer | $500 + \lceil 500/100 \rceil \cdot 1000 = 5500$ |
| index nested loop, $R$ outer, $c_{\text{probe}} = 2.2$ | $1000 + 100\,000 \cdot 2.2 = 221\,000$ |
| sort-merge join, two-pass sorts | $5 \cdot 1500 = 7500$ |
| sort-merge join, last merge feeds the join | $3 \cdot 1500 = 4500$ |
| Grace hash join | $3 \cdot 1500 = 4500$ |

The range is four orders of magnitude, so even rough estimates rule out the bad plans. The order of the inputs matters for the block nested loop join: the smaller relation should be the outer one. If the query selects 1% of $R$ first, the outer of the index nested loop join has 1000 tuples, its cost falls to about $1000 + 1000 \cdot 2.2 = 3200$, and it becomes the best plan. So the choice depends on the selectivity estimate, not only on the formulas.

**PostgreSQL.** The PostgreSQL documentation shows a sequential scan of the table `tenk1`, which has 10000 rows on 358 pages. Its estimated cost is $358 \cdot 1.0 + 10000 \cdot 0.01 = 458$: one unit per sequential page read plus `cpu_tuple_cost` = 0.01 per row. With a `WHERE` condition the cost becomes 483, because each of the 10000 rows also pays `cpu_operator_cost` = 0.0025 to test the condition. The estimated number of output rows does not change the cost of the scan, which still reads every page.

**C_out.** Take relations with $|R_1| = 10$, $|R_2| = 1000$, $|R_3| = 100$, the predicates $R_1.a = R_2.a$ and $R_2.b = R_3.b$, and estimated result sizes $|R_1 \bowtie R_2| = 50$, $|R_2 \bowtie R_3| = 5000$, $|R_1 \bowtie R_2 \bowtie R_3| = 250$. The plan $(R_1 \bowtie R_2) \bowtie R_3$ has $C_{\text{out}} = 50 + 250 = 300$, and the plan $(R_2 \bowtie R_3) \bowtie R_1$ has $C_{\text{out}} = 5000 + 250 = 5250$. The final result counts in both, so only the intermediate result makes a difference.

## Where it is used

- **Plan choice.** Every cost-based optimizer, from System R to current systems, ranks plans with a cost model; see [query optimization](/query-optimization/) and the [Selinger join enumeration](/selinger-join-enumeration/).
- **Physical design.** [Index selection](/index-selection/) and [view selection](/view-selection/) tools call the optimizer's cost model on a workload with hypothetical indexes or views to estimate the benefit of each one.
- **Parallel and distributed queries.** The models add the cost of messages and of moving data between nodes, and some estimate the response time instead of the total work.
- **Main-memory systems.** When the data fits in memory, I/O no longer dominates; the models count tuples processed, cache misses, or simply $C_{\text{out}}$. Leis et al. (2015) found on the Join Order Benchmark that a simple cost function close to $C_{\text{out}}$ did about as well as a tuned one, because the errors in the cardinality estimates were much larger than the differences between cost functions.

## References
