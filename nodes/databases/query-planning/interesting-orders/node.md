---
tag: 58Q25G
kind: concept
slug: interesting-orders
name: Interesting orders
aliases:
- interesting sort orders
area: databases/query-planning
level: core
summary: "Sort orders of intermediate results that a later join, grouping or ORDER BY can use, which a plan enumerator keeps alongside cost."
prereqs: [query-plan, sort-merge-join, principle-of-optimality]
see_also: [selinger-join-enumeration, access-path-selection, volcano-optimizer-generator, cascades-framework, external-merge-sort, sort-based-aggregation, functional-dependency, clustered-index]
sources:
  - paper: doi:10.1145/582095.582099
    title: "P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie and T. G. Price, Access path selection in a relational database management system, Proceedings of ACM SIGMOD 1979, 23 to 34"
    locator: "Sections 4 and 5, Costs for single relation access paths and Access path selection for joins (interesting orders from the GROUP BY and ORDER BY clauses and from the join columns, and the cheapest plan kept for each)"
  - paper: "Goetz Graefe and William J. McKenna, The Volcano optimizer generator: extensibility and efficient search, Proceedings of ICDE 1993, 209 to 218"
    title: "The Volcano optimizer generator: extensibility and efficient search"
    locator: "physical properties, of which sort order is one, and enforcers such as sort that produce them"
---

An interesting order is a sort order of an intermediate result that some later operator of the query can use. A merge join on a column needs both inputs sorted on it, a grouping can run on sorted input without a hash table, and an ORDER BY needs the final result in its order. Selinger and her colleagues introduced the idea in the System R optimizer (1979). A plan that is more expensive but gives an interesting order can lead to a cheaper whole plan, because it saves a sort later. So the plan enumerator keeps, for each set of relations, the cheapest plan for each interesting order and the cheapest plan overall, not only the cheapest one. The [System R join enumeration](/selinger-join-enumeration/) is the algorithm that does this for join orders; this page is about the idea itself: which orders are interesting, how plans with orders are compared, and how the idea grew into the physical properties of later optimizers.

## In plain words

A query joins two tables and then wants the answer sorted by date. One plan joins fast, but its result is in no order, so it must sort at the end. Another plan joins a little more slowly, but its result comes out sorted by date already.

If the optimizer keeps only the fastest join, it forgets the second plan, and it pays for the sort later. So it keeps both: the fastest plan, and the fastest plan that gives each useful order. An order is useful, or interesting, if a later step needs it: a join on that column, a grouping on it, or the final sort. Other orders are not kept, because no later step can use them.

## The idea

**Orders.** An order is a list of columns, each with a direction, such as $(a \uparrow, b \uparrow)$. A result sorted on $(a, b)$ is also sorted on $(a)$, so an order *satisfies* every prefix of itself. A result with no known order satisfies only the empty order.

**Where orders come from.** A scan through a [B+ tree](/b-plus-tree/) index returns tuples in key order, and a [clustered index](/clustered-index/) does so at the cost of a full scan. A sort operator produces any order, at the cost of a sort, such as an [external merge sort](/external-merge-sort/). A [sort-merge join](/sort-merge-join/) returns its result in the order of its join columns. A nested loop join keeps the order of its outer input. A hash join and a hash grouping give no order.

**Which orders are interesting.** For one block of a query:

- the join columns of each join that is still to be done, because a merge join can use them;
- the GROUP BY columns, in any order of the columns, because a [sort-based grouping](/sort-based-aggregation/) needs only that equal keys are next to each other;
- the ORDER BY list, with its directions, for the final result.

**Comparing plans.** Two plans for the same set of relations are compared by cost and by order. A plan $P$ *dominates* a plan $Q$ if $P$ costs at most as much as $Q$ and the order of $P$ satisfies every interesting order that the order of $Q$ satisfies. The enumerator keeps only plans that no other plan dominates. With $k$ interesting orders this is at most $k + 1$ plans per set: one for each order and one with no order. Without the order in the comparison, the [principle of optimality](/principle-of-optimality/) fails: the best plan for a set is not always built from the cheapest plans of its parts, because a part with a useful order can be worth its extra cost. With the order in the comparison, it holds again, for each pair of a set and an order.

**Fewer distinct orders.** Several rules make two orders the same, so the enumerator keeps fewer plans.

- After a join on $R.a = S.b$, a result sorted on $R.a$ is also sorted on $S.b$, so the two columns are one class.
- After a selection $a = 5$, the column $a$ is constant and can be removed from any order.
- If the [functional dependency](/functional-dependency/) $a \to b$ holds, a result sorted on $(a)$ is also sorted on $(a, b)$, because tuples with equal $a$ have equal $b$.

**Physical properties.** The [Volcano optimizer generator](/volcano-optimizer-generator/) and the [Cascades framework](/cascades-framework/) treat the sort order as one *physical property* among others, such as the partitioning of a result in a parallel plan. A goal asks for a group of equivalent expressions with a required property, and an *enforcer*, such as a sort, produces the property when no plan has it for free.

## Examples

**A join followed by ORDER BY.** A query joins $R$ and $S$ on $a$ and asks for ORDER BY $a$. The costs, in page reads, are these.

| plan for $R \bowtie S$ | cost of the join | order of the result | sort at the end | total |
|---|---|---|---|---|
| hash join of two full scans | 300 | none | 200 | 500 |
| merge join of two index scans on $a$ | 350 | $(a)$ | 0 | 350 |

A comparison on cost alone keeps the hash join, because 300 is less than 350, and then the best whole plan costs 500. With $(a)$ as an interesting order, the enumerator keeps both plans for $\{R, S\}$: the hash join as the cheapest plan with no order, and the merge join as the cheapest plan with order $(a)$. At the end it compares $300 + 200$ with $350 + 0$ and chooses the merge join.

**Three relations on one column.** A query joins $R$, $S$ and $T$ on $R.a = S.a$ and $S.a = T.a$. The three columns are one class, so the only interesting order is $(a)$. A merge join of $R$ and $S$ gives $(a)$, and a second merge join with $T$ needs no sort of the intermediate result. A plan that joins $R$ and $S$ by hash must sort the result before a merge join with $T$.

**A grouping.** For GROUP BY $b, a$, a result sorted on $(a, b)$ or on $(b, a)$ can be grouped in one pass. A result sorted on $(a)$ alone cannot, because tuples with the same $(a, b)$ need not be next to each other, unless $a \to b$ holds.

## Where it is used

- **System R style enumeration.** The [System R join enumeration](/selinger-join-enumeration/) keeps one plan for each set of relations and each interesting order. The choice of the [access path](/access-path-selection/) for a single relation does the same: an index scan that costs more than a full scan is kept if it gives an interesting order.
- **Top-down optimizers.** Volcano and Cascades ask for a group with a required order, and they memoize the best plan for each pair of a group and an order.
- **Sort avoidance.** An optimizer that tracks orders can drop a sort for ORDER BY, DISTINCT or GROUP BY when the input already has a suitable order.
- **Cost of the search.** Each interesting order can multiply the number of plans that the enumerator keeps, so the work grows with the number of distinct orders. The rules above that merge orders reduce this growth.

## References
