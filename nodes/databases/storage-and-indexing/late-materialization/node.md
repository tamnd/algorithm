---
tag: DADXAP
kind: technique
slug: late-materialization
name: Late materialization
aliases:
- late tuple reconstruction
area: databases/storage-and-indexing
level: advanced
summary: "In a column store, run the filters on single columns and pass lists of row positions through the plan. Fetch the other columns of a row only for the positions that survive."
prereqs: [decomposition-storage-model]
see_also: [decomposition-storage-model, dictionary-encoding, frame-of-reference-encoding, vectorized-query-execution, predicate-pushdown, bitmap-index, zone-map, pax-page-layout]
sources:
  - paper: "Daniel J. Abadi, Daniel S. Myers, David J. DeWitt and Samuel R. Madden, Materialization strategies in a column-oriented DBMS, Proceedings of the 23rd International Conference on Data Engineering (ICDE), 2007, 466 to 475"
    title: Materialization strategies in a column-oriented DBMS
    locator: the early and late materialization strategies, their cost model, and the experiments on selections, aggregations and joins
  - paper: "Daniel Abadi, Samuel Madden and Miguel Ferreira, Integrating compression and execution in column-oriented database systems, Proceedings of the 2006 ACM SIGMOD International Conference on Management of Data, 2006, 671 to 682"
    title: Integrating compression and execution in column-oriented database systems
    locator: operators that work directly on compressed columns and pass positions
  - paper: "Daniel Abadi, Peter Boncz, Stavros Harizopoulos, Stratos Idreos and Samuel Madden, The design and implementation of modern column-oriented database systems, Foundations and Trends in Databases 5(3), 2013, 197 to 280"
    title: The design and implementation of modern column-oriented database systems
    locator: the section on late materialization and the section on joins in column stores
---

Late materialization is a way to run queries on a column store, a table stored as in the [decomposition storage model](/decomposition-storage-model/). A record is spread over many columns, and putting its values together into a tuple is called *materialization* or *tuple reconstruction*. Early materialization builds the tuples first, from every column the query uses, and then runs the plan on tuples, as a row store would. Late materialization runs the filters on one column at a time and passes lists of *positions* (row numbers) from operator to operator. It reads an output column only at the positions that passed all the filters. It is a choice of plan, not of storage: the same columns serve both. It works well with compressed columns, because a filter can often run on the codes of [dictionary encoding](/dictionary-encoding/) or [frame of reference encoding](/frame-of-reference-encoding/) without decoding the values of the records that fail.

## In plain words

Think of a table kept as separate lists, one list of regions, one of prices, one of quantities, all in the same order of rows.

You want the quantities of the rows with region EU and price under 50. The early way is to copy out every row with its region, price and quantity, and then throw away the rows you do not want. Most of the copying was for nothing.

The late way is to read only the region list first and write down the row numbers that say EU. Then look up the prices only at those row numbers, and cross out the ones that are too high. At the end, look up the quantities only at the row numbers that are left.

## When it applies

- The data is stored by column, and a query reads several columns of the same records.
- The filters are selective: a large part of the records fails at least one predicate, so most values of the other columns are never needed.
- The columns are compressed, and the predicates can be evaluated on the compressed values, for instance an equality on dictionary codes or a range on frame-of-reference offsets.
- The positions that survive come out in increasing order, so that the output columns are read in one forward pass. This is true for scans and filters, and for the outer side of many joins.

## The template

A *position list* $P$ is a sorted list of row numbers; it can also be a bitmap of $N$ bits or a list of ranges. A predicate $c \mathbin{\theta} v$ compares column $c$ with a constant; a comparison with NULL is never true.

```pseudo id=main
LATE(R, preds, out)
L1  P ← the positions 0 to N - 1
L2  for each predicate (c, θ, v) in preds, the most selective first do
L3      P ← the positions i in P with R.c[i] θ v            ▷ read column c only at P
L4  for each column c in out do
L5      V_c ← the values R.c[i] for i in P, in order
L6  return the tuples (V_c[x] for each c in out), for x ← 0 to |P| - 1

EARLY(R, preds, out)
L7  for i ← 0 to N - 1 do
L8      t ← the values of record i in every column that preds or out uses
L9      if t satisfies every predicate then output the columns out of t
```

Line L3 keeps the sorted order of $P$, so every column is read forward, at increasing positions, and line L6 joins the output columns by position, with no search. The *parallel* form of late materialization scans each predicate column fully into a bitmap and combines the bitmaps with AND; it reads more values but scans the columns independently, which suits SIMD and several cores.

**Why it works.** By induction over the loop at lines L2 and L3, after the $m'$-th predicate $P$ is the sorted list of the records that satisfy the first $m'$ predicates. After the loop it is the sorted list $Q$ of the records that satisfy all of them, and lines L4 to L6 output, in that order, the output columns of exactly those records. EARLY outputs the same list. So the two plans give the same bag of tuples, and in the same order. The proof file has the details.

**Cost.** Count the column values that the plan reads. With $m$ predicates, $r$ output columns, and $|P_{m'}|$ the size of $P$ after the $m'$-th predicate, LATE reads $N + |P_1| + \ldots + |P_{m-1}| + r \lvert Q \rvert$ values. EARLY reads $N u$, where $u$ is the number of distinct columns that the query uses, and the parallel form reads $N m + r \lvert Q \rvert$. With one predicate and $r$ other output columns, LATE reads $N + r \lvert Q \rvert$ against $N(1 + r)$.

**Example.** Take $N = 8$ and the query "qty where region = EU and price < 50".

| position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| region | EU | US | EU | EU | ASIA | US | EU | ASIA |
| price | 10 | 70 | 80 | 30 | 20 | 40 | 45 | 90 |
| qty | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |

LATE reads all 8 regions and gets $P = (0, 2, 3, 6)$. It reads 4 prices and keeps $P = (0, 3, 6)$. It reads 3 quantities and returns 1, 4 and 7. That is $8 + 4 + 3 = 15$ values. EARLY reads all three columns of all 8 records, 24 values, for the same three rows. If the price predicate goes first, it keeps 5 positions, $(0, 3, 4, 5, 6)$, and LATE reads 16 values. The parallel form reads $8 + 8 + 3 = 19$.

## Classic examples

- **Selections in C-Store.** Abadi, Myers, DeWitt and Madden (2007) compare early and late materialization in C-Store, each in a pipelined and a parallel form, and give a cost model. Late materialization wins for selective predicates and for aggregations over compressed columns; early materialization can win when most records qualify and many columns are output.
- **Operating on compressed data.** Abadi, Madden and Ferreira (2006) run selections and aggregations directly on compressed columns. A filter on a [run-length encoded](/run-length-encoding/) column returns position ranges, and a sum over an encoded column can multiply a value by its run length.
- **Vectorized engines.** MonetDB and engines in the style of [vectorized execution](/vectorized-query-execution/) pass vectors of positions, or selection vectors, between operators, which is late materialization in blocks of rows.
- **Index scans.** A [bitmap index](/bitmap-index/) scan in a row store builds a bitmap of qualifying rows from several indexes and fetches the rows only at the end, the same idea on row storage.

## Variations

- **Position lists, bitmaps or ranges.** A sorted list is compact when few records qualify, a bitmap when many do, and a list of ranges when the qualifying records are clustered, as after a filter on a sorted column.
- **Multi-column blocks.** Abadi et al. (2007) pass blocks that hold a position list and the values of some columns at those positions, so that an operator does not need to read a column twice.
- **Late materialization in joins.** A join can take only the join columns and positions, produce pairs of positions, and fetch the other columns after the join. The positions of the inner side then come out of order.
- **Zone maps first.** A [zone map](/zone-map/) can drop whole blocks of positions before the first column is read, and [predicate pushdown](/predicate-pushdown/) moves the filters as close to the scan as possible so that they act on positions.

## Pitfalls

- **Positions out of order.** After a join or a sort, the positions of one side are not sorted, and fetching a column at them is random access. Sort the positions first and keep the permutation, or use early materialization for that side.
- **Reading a column twice.** If an output column is also a predicate column and most records qualify, LATE reads it once to filter and again to output. Keep the values from the filter, as multi-column blocks do.
- **Unselective filters.** When nearly every record qualifies, position lists cost as much as the data and save nothing. A cost model should choose the strategy per query.
- **Order of the predicates.** The cost depends on which predicate runs first. Without statistics on selectivity and correlation, the plan can read far more than it needs.
- **Positions that change.** Positions are valid only while the columns do not change. Updates and deletes in a column store need a stable snapshot, or a delete bitmap, so that a plan sees one version of every column.

## Exercises

1. For one predicate and $r$ output columns, find the fraction of qualifying records above which EARLY reads fewer values than LATE when the output columns include the predicate column.
2. Give three predicates on independent columns with selectivities $1/2$, $1/4$ and $1/8$. Compute the expected values read by LATE for every order, and show that the most selective first is the best order here.
3. Change LATE so that it keeps every value it reads, and reads a value of a column again only if it did not keep it. Prove that it never reads more values than EARLY.
4. A join produces pairs of positions of two tables, sorted by the positions of the first. Describe how to fetch an output column of the second table with sequential reads, and give its cost.

## References
