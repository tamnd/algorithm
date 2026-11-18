---
tag: B4N0ZP
kind: technique
slug: eager-aggregation
name: Eager aggregation
aliases:
- group-by pushdown
- aggregation pushdown
area: databases/query-planning
level: advanced
summary: "Move a grouping below a join when the conditions of Yan and Larson hold, so the join works on fewer rows."
prereqs: [group-by-aggregation, relational-join, functional-dependency, relational-algebra-equivalences]
see_also: [subquery-unnesting, hash-aggregation, predicate-pushdown, data-cube, exchange-operator, cardinality-estimation, cascades-framework, selinger-join-enumeration]
sources:
  - paper: "Weipeng P. Yan and Per-Åke Larson, Eager aggregation and lazy aggregation, Proceedings of VLDB 1995, 345 to 357"
    title: Eager aggregation and lazy aggregation
    locator: "the transformations eager and lazy group-by, eager and lazy count, double eager and double lazy, and eager and lazy split, with their conditions as functional dependencies in the join result"
  - paper: "Surajit Chaudhuri and Kyuseok Shim, Including group-by in query optimization, Proceedings of VLDB 1994, 354 to 366"
    title: Including group-by in query optimization
    locator: "general locator: the cost-based choice of the place of a grouping in a join plan, in an optimizer of the System R style"
---

Eager aggregation is the technique that computes part of a grouping before a join and finishes it after the join. A query such as `SELECT R.g, SUM(S.v) FROM R JOIN S ON R.k = S.k GROUP BY R.g` joins every row of $S$ with its rows of $R$ and only then adds up. If many rows of $S$ share a join value, it is cheaper to group $S$ by $k$ first, so that the join reads one row for each value of $k$, and then to combine the partial results in a final grouping by $g$. Yan and Larson named this move *eager* aggregation and its reverse *lazy* aggregation, and gave the conditions under which the two forms of the query are equal. Whether the move pays depends on the number of rows per group, so an optimizer makes the choice by cost, as Chaudhuri and Shim proposed.

## In plain words

A shop wants the total amount of each customer's order lines. The direct way is to attach the customer to every order line, and then to add up the lines of each customer. If an order has a hundred lines, the customer is attached a hundred times.

The eager way first adds up the lines of each order. Then it attaches the customer to each order total, and adds up the order totals of each customer. Fewer rows go through the attach step.

This works for totals, counts, smallest and largest values. It needs care in three cases. A count of rows becomes a total of counts. A value from the customer side must be counted once for each order line it stands for. An average is not an average of averages, so the eager way keeps a total and a count and divides at the end.

## When it applies

- The query is SQL, so tables are bags. It is a grouping on top of an inner equijoin, $\gamma_{G;\,\mathrm{aggs}}(R \bowtie_{k} S)$. The code of this page uses $R(g, k, x)$ and $S(k, v)$, with $G$ equal to $\{g\}$ or empty.
- Each aggregate is *decomposable*: it can be computed from the results of the same or another aggregate on the parts of a partition of its input. COUNT, SUM, MIN and MAX are decomposable, and AVG is the quotient of a SUM and a COUNT. COUNT(DISTINCT) and the median are not decomposable in this way.
- The lower grouping groups $S$ by all its join columns and by every column of $S$ in $G$. Then every row of $R$ joins at most one partial row, and a final group never mixes two join values that the query keeps apart.
- The final grouping stays above the join. It can be dropped only when each final group gets at most one row of the join with the partial results. That holds, for example, when $G$ holds a key of $R$. Yan and Larson state conditions of this kind as functional dependencies that must hold in the join result.
- A HAVING clause and an ORDER BY stay above the final grouping.

## The template

Write $c$ for the number of rows of $S$ in a partial group, $v$ for a column of $S$ and $x$ for a column of $R$. A join test with NULL on either side is UNKNOWN, so a row with a NULL join value has no match.

```pseudo id=main
EAGER(R, S, G, aggregates)                      ▷ the query γ_{G; aggregates}(R ⋈_k S), G a set of columns of R
L1  P ← γ_{k; c ← COUNT(*), and a partial aggregate for each aggregate of a column of S}(S)
L2  J ← R ⋈ P                                    ▷ each row of R joins at most one row of P
L3  add to each row of J the columns x·c and c, or NULL and NULL if x is NULL
L4  F ← γ_{G; the final aggregates}(J)
L5  replace each NULL count of F by 0, and compute each AVG as its sum divided by its count
```

The partial and final aggregates are these.

| aggregate of the query | partial, in $P$ | final, in $F$ |
|---|---|---|
| COUNT(\*) | $c$ | SUM($c$) |
| COUNT($v$), SUM($v$) | the same aggregate | SUM |
| MIN($v$), MAX($v$) | the same aggregate | MIN, MAX |
| AVG($v$) | SUM($v$) and COUNT($v$) | SUM of each, then the quotient |
| SUM($x$) | none | SUM($x \cdot c$) |
| COUNT($x$) | none | SUM of $c$ over the rows with $x$ not NULL |
| MIN($x$), MAX($x$) | none | MIN($x$), MAX($x$) |
| AVG($x$) | none | SUM($x \cdot c$) divided by the final of COUNT($x$) |

**Why it works.** Let $S_a$ be the bag of rows of $S$ with $k = a$. A row $r$ of $R$ joins exactly the rows of $S_{r.k}$, and none if $r.k$ is NULL. So the joined rows of a final group are the union, over the rows $r$ of $R$ in the group and with their counts, of the parts $\{r\} \times S_{r.k}$. Line L1 makes one row of $P$ for each $a$ with $S_a$ not empty, and the row for a NULL key never joins. So line L2 gives one row of $J$ for each row $r$ whose part is not empty, and the row carries the partial aggregates of its part. A final group of the query exists exactly when one of its parts is not empty, and so it exists in $F$ too. The final aggregates then combine the parts. A count of the union is the sum of the counts. A SUM, MIN or MAX of $v$ over the union is the SUM, MIN or MAX of the partial values, and NULL handling agrees: a partial value is NULL when its part has no non-null $v$, the final aggregate skips it, and the result is NULL only when no part has a non-null $v$. In the part of $r$ the value $x$ of $r$ appears $c$ times, which line L3 accounts for, and repeats do not change MIN and MAX. Line L5 handles the one case where the final aggregate differs from the count: with $G$ empty and no joined row, SQL returns one row with COUNT equal to 0, while SUM over no rows is NULL.

**Cost.** Line L1 is one grouping of $S$, $O(|S|)$ expected time with a hash table. Line L2 joins $R$ with at most $|S|$ partial rows and returns at most $|R|$ rows, while the original join can return $|R| \cdot |S|$ rows. The move pays when the rows of $S$ repeat their join values, and it costs one extra grouping when they do not. The code of this page uses the dbrel helper, whose operators work by their definitions, so it shows that the results are equal, and it counts the join rows, but its time is not that of a real engine.

**Example.** Take $R = \{(a, 1, 10), (a, 2, 20), (b, 2, \mathrm{NULL}), (b, \mathrm{NULL}, 5)\}$ as $(g, k, x)$ and $S = \{(1, 3), (1, \mathrm{NULL}), (2, 4), (2, 4), (2, 6), (\mathrm{NULL}, 7)\}$ as $(k, v)$. The query asks for COUNT(\*), SUM($v$), SUM($x$), COUNT($x$) and AVG($v$) for each $g$. The join $R \bowtie S$ has 8 rows. Line L1 gives $P$ with the columns $(k, c, \mathrm{SUM}(v), \mathrm{COUNT}(v))$.

| $k$ | $c$ | SUM($v$) | COUNT($v$) |
|---|---|---|---|
| 1 | 2 | 3 | 1 |
| 2 | 3 | 14 | 3 |
| NULL | 1 | 7 | 1 |

Line L2 gives 3 rows: $(a, 1, 10)$ with the row of $k = 1$, and $(a, 2, 20)$ and $(b, 2, \mathrm{NULL})$ with the row of $k = 2$. The row of $R$ with a NULL key and the row of $P$ with a NULL key find no partner. Lines L3 to L5 give, for $a$: COUNT(\*) $= 2 + 3 = 5$, SUM($v$) $= 3 + 14 = 17$, SUM($x$) $= 10 \cdot 2 + 20 \cdot 3 = 80$, COUNT($x$) $= 5$ and AVG($v$) $= 17/4$. For $b$: COUNT(\*) $= 3$, SUM($v$) $= 14$, SUM($x$) is NULL, COUNT($x$) is 0 and AVG($v$) $= 14/3$. These are the values of the original query, and the tests check them and random tables with NULL values for every aggregate, with and without the grouping by $g$.

## Classic examples

- **Star schemas.** A query joins a large fact table with a dimension table and groups by a column of the dimension. Grouping the fact rows by the foreign key first is eager group-by on the fact table.
- **Local and global aggregation.** A parallel plan groups each partition before the [exchange](/exchange-operator/) and finishes the grouping after it. The partial and final aggregates are those of the table above, and the exchange plays the part of the join.
- **Roll-up in a data cube.** The [data cube](/data-cube/) computes a coarse grouping from a finer one with the same pairs of partial and final aggregates.
- **After unnesting.** [Subquery unnesting](/subquery-unnesting/) turns a correlated aggregate into a grouping of the inner table followed by a join, which is eager aggregation already. Lazy aggregation can move that grouping above the join when that is cheaper.

## Variations

- **Eager count.** Group the side with no aggregate column, here $R$ by $(g, k)$ with a count $d$, join with $S$, and weight each value of $v$ by $d$ in the final grouping. Yan and Larson call this eager count.
- **Double eager.** Group both sides by their join columns and combine the two counts in the final grouping.
- **Lazy aggregation.** The reverse move pulls a grouping up above a join, which pays when the join removes many rows first.
- **Dropping the final grouping.** If each final group gets one row of $J$, the final grouping is a projection. The code has this case as eager_without_final.
- **Partial pre-aggregation.** An engine can run line L1 with a small hash table that sends a group on when the table is full. The final grouping still gives the right answer, so the lower grouping does not need to be complete.
- **Outer joins.** For $R$ left outer join $S$, a row of $R$ with no match has NULL partial values. Its COUNT(\*) must be 1 and its count of $S$ columns 0, so the final aggregates need a case for the padded rows.

## Pitfalls

- **COUNT(\*) as a count of the join rows.** After line L2 a row of $J$ stands for $c$ joined rows. In the example, counting the rows of $J$ gives 2 for $a$, not 5.
- **Sums of the other side without weights.** SUM($x$) over $J$ without the factor $c$ gives 30 for $a$, not 80.
- **The average of averages.** The partial averages of $a$ are 3 and $14/3$, and their average is $23/6$, not $17/4$. Keep a sum and a count.
- **NULL in place of 0.** With no grouping columns and no joined rows, the final SUM of counts is NULL, but SQL returns 0 for COUNT. Line L5 fixes this.
- **Dropping the final grouping when $G$ is not a key.** In the example, $a$ joins two partial rows, so the result without the final grouping has two rows for $a$.
- **Too coarse a lower grouping.** If $S$ is grouped by fewer columns than its join columns, one partial row mixes rows that join different rows of $R$.
- **No reduction.** If the join values of $S$ are almost all distinct, line L1 costs a pass and saves nothing. The decision needs an estimate of the number of groups from [cardinality estimation](/cardinality-estimation/).

## Exercises

1. Give the partial and final aggregates for the population variance of $S.v$.
2. Apply eager count to the example: group $R$ by $(g, k)$ with a count, join with $S$, and compute SUM($v$) for each $g$.
3. Show that COUNT(DISTINCT $S.v$) cannot be computed from $P$ as defined, and give a lower grouping of $S$ from which it can be computed.
4. The join is $R$ left outer join $S$. Change lines L2 to L5 so that COUNT(\*) and SUM($v$) are right for the rows of $R$ with no match.

## References
