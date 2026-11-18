---
tag: ZDF77H
kind: algorithm
slug: sort-based-aggregation
name: Sort-based aggregation
aliases:
- sort aggregate
- stream aggregate
area: databases/query-processing
level: core
summary: Sort the rows on the grouping key with an external merge sort, and combine rows of equal key into one partial state while the runs are formed and merged.
solves: [group-by-aggregation]
model: external-memory-model
complexity:
  vars: {N: the number of input pages, B: the number of buffer pages, p: the number of records per page, n: the number of input rows, d: the number of groups, P: the number of passes}
  time: {worst: O(n log n), best: O(n log n)}
  space: {extra: Θ(B p)}
  io:
    worst: "2 N P - N"
    average: "2 N P - N"
    best: "N"
properties: {deterministic: true, exact: true, external: true, online: false, in_place: false, recursive: false}
history:
  year: 1983
  people: [Dina Bitton, David J. DeWitt]
  note: "Bitton and DeWitt studied duplicate elimination in large files and removed duplicates while the runs of an external merge sort were formed and merged, so that the runs shrink early."
prereqs: [external-merge-sort, group-by-aggregation]
see_also: [hash-aggregation, sort-merge-join, sorted-run, k-way-merge, replacement-selection, combiner, iterator-model, data-cube]
sources:
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 73 to 169 (1993)
    locator: Section 4 (aggregation and duplicate removal; sort-based aggregation with early aggregation in the runs)
  - paper: doi:10.1145/319983.319987
    title: Dina Bitton and David J. DeWitt, Duplicate record elimination in large data files, ACM Transactions on Database Systems 8(2), 255 to 265 (1983)
    locator: duplicate removal during the runs of an external merge sort
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2009)
    locator: Chapter 15 (two-pass grouping and duplicate elimination based on sorting)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 14, Section 14.6 (aggregate operations, with and without grouping)
---

Sort-based aggregation solves the [group-by aggregation problem](/group-by-aggregation/) with an [external merge sort](/external-merge-sort/) on the grouping key. When two records with the same key meet, in the sort of one run or in a merge of runs, they are replaced by one record that holds a partial state of the aggregates, such as $(\text{SUM}, \text{COUNT})$ for AVG. This early aggregation keeps each [sorted run](/sorted-run/) no longer than the number of groups, so the sort costs less when there are few groups. Unlike [hash aggregation](/hash-aggregation/), it gives the groups in key order, and it is the plan of choice when the input already comes sorted on the key.

## In plain words

You count votes on paper ballots. You take a pile that fits on your desk, sort it by candidate, and write one slip per candidate with that candidate's count. You put the slips on a shelf and take the next pile. Then you take a few stacks of slips at a time, which are all sorted by name, and go through them together. When two slips have the same name, you add them into one slip. You do this until one stack is left. Each slip in it gives one candidate and the final count, in name order. If there are only a few candidates, the stacks of slips stay small, and the work after the first piles is fast.

## The problem

The input is a file $R$ of $N$ pages with $p$ records per page, the grouping columns $G$, and aggregates $f_1, \ldots, f_q$ on columns $A_1, \ldots, A_q$. Each aggregate is given by three functions: $\text{INIT}(v)$ makes a state from one value, $\text{MERGE}(s, s')$ joins two states, and $\text{FINAL}(s)$ gives the answer. MERGE is associative and commutative, and the state of a multiset $X \uplus Y$ is MERGE of the states of $X$ and $Y$. This holds for the distributive aggregates (COUNT, SUM, MIN, MAX) and for the algebraic ones (AVG with the state $(\text{SUM}, \text{COUNT})$), two of the classes of aggregates that come with the [data cube](/data-cube/). The output is one row per group, $\gamma_{G;\, f_1(A_1), \ldots, f_q(A_q)}(R)$, sorted on $G$.

The memory holds $B \ge 3$ pages. In the external memory model, the memory holds M/B blocks; this is the number of buffer pages B of this page. The cost is the number of page reads and page writes. The final output is not counted, because a parent operator can use it as it comes.

## The algorithm

Each record is a pair (key, state). A run is a file of records sorted on the key.

```pseudo id=main
SORT-AGGREGATE(R, B)                       ▷ R has N pages
L1  runs ← an empty list
L2  for each group of B consecutive pages of R do
L3      X ← the records of the group as (key, INIT) pairs, sorted on the key
L4      if N ≤ B then return FINAL of each record of COMBINE(X)    ▷ one pass, nothing is written
L5      if early then X ← COMBINE(X)       ▷ early aggregation in pass 0
L6      write X as a new run; append it to runs
L7  while |runs| > B - 1 do
L8      new ← an empty list
L9      for each group of B - 1 consecutive runs do
L10         X ← the merge of the runs of the group on the key
L11         if early then X ← COMBINE(X); write X as a new run, append it to new, and free the group
L12     runs ← new
L13 return FINAL of each record of COMBINE(the merge of runs)       ▷ the output is not written

COMBINE(X)                                 ▷ X is sorted on the key
L14 for each record (k, s) of X in order do
L15     if c exists and the key of c is k then
L16         c ← (k, MERGE(state of c, s))
L17     else output c if it exists; c ← (k, s)
L18 output c if it exists
```

A merge (lines L10 and L13) reads one page of each run at a time, so it uses $B - 1$ input buffers and one output buffer, and it picks the smallest key with a [k-way merge](/k-way-merge/). COMBINE needs only the current record, so it does not use more memory. Without early aggregation, lines L5 and L11 write the records as they are, and the passes are those of a plain external merge sort.

## Example

Take $B = 3$ and $p = 2$, and compute COUNT(\*) and SUM(v) per key over 16 rows in $N = 8$ pages: (d, 4), (b, 2), (a, 5), (c, 1), (b, 7), (a, 3), (d, 6), (c, null), (a, 2), (e, 8), (b, 1), (a, 4), (e, 3), (c, 5), (d, 2), (b, 6). A state is (count, sum), and the sum of no non-null value is null.

| step | input | records written | pages |
|---|---|---|---|
| pass 0, run 1 | rows 1 to 6 | a (2, 8), b (2, 9), c (1, 1), d (1, 4) | 2 |
| pass 0, run 2 | rows 7 to 12 | a (2, 6), b (1, 1), c (1, null), d (1, 6), e (1, 8) | 3 |
| pass 0, run 3 | rows 13 to 16 | b (1, 6), c (1, 5), d (1, 2), e (1, 3) | 2 |
| pass 1, merge runs 1 and 2 | 5 pages | a (4, 14), b (3, 10), c (2, 1), d (2, 10), e (1, 8) | 3 |
| pass 1, run 3 alone | 2 pages | the same 4 records | 2 |
| pass 2, final merge | 5 pages | not written | - |

The output is a (4, 14), b (4, 16), c (3, 6), d (3, 12), e (2, 11). Pass 0 reads 8 pages and writes 7, pass 1 reads 7 and writes 5, and the final merge reads 5: 20 reads and 12 writes, 32 I/Os. Without early aggregation, the runs of pass 0 have 3, 3 and 2 pages, pass 1 makes runs of 6 and 2 pages, and the cost is 24 reads and 16 writes, 40 I/Os, which is $2 N P - N$ with $P = 3$.

## Correctness

COMBINE gets a sequence sorted on the key, so all records of one key are adjacent. It keeps one current record $c$ and merges into it each next record with the same key, so it outputs one record per key, in key order, whose state is the MERGE of the states of all records of that key. Let $\sigma(R_k)$ be the MERGE of the INIT states of all rows with key $k$. The invariant is that, after each pass, every run is sorted on the key, and for each key $k$ the MERGE of the states of all its records in all runs is $\sigma(R_k)$. Pass 0 makes this true, since each row gives one record and COMBINE keeps the MERGE. A merge keeps the order and the records, and COMBINE keeps the MERGE again, by associativity and commutativity. The loop of line L7 ends, because $\lceil r/(B-1) \rceil < r$ for $r > B - 1 \ge 2$ runs. The last COMBINE then sees all records of key $k$ adjacent and outputs $\text{FINAL}(\sigma(R_k))$ once. The full proof is in the proof file.

## Complexity

- **Passes.** Pass 0 makes $\lceil N/B \rceil$ runs, and each merge pass divides the number of runs by $B - 1$, so there are $P = 1 + \lceil \log_{B-1} \lceil N/B \rceil \rceil$ passes in total, the last one being the final merge.
- **I/O without early aggregation.** Each pass reads $N$ pages, and each pass but the last writes $N$ pages, so the cost is $2 N P - N$. If $N \le B$, it is $N$. If $B < N \le B(B-1)$, it is $3N$, the same as two-pass hash aggregation.
- **I/O with early aggregation.** A run never holds more than one record per group, so it has at most $\lceil d/p \rceil$ pages. The cost is never more than without it, and when $d$ is small, the runs after pass 0 are short and the merge passes cost almost nothing. The exact cost depends on how many distinct keys each group of pages holds.
- **Time.** Sorting pass 0 costs $O(n \log (B p))$ comparisons, and each merge pass costs $O(\log B)$ per record, for $O(n \log n)$ in total.
- **Space.** The memory holds $B$ pages, $B p$ records, at all times.

## Properties

- **Order preserving.** The groups come out sorted on $G$, so a later `ORDER BY` on $G$, or a [sort-merge join](/sort-merge-join/) on $G$, needs no new sort.
- **Blocking.** No group is output before the input is read to the end, unless the input is already sorted on $G$.
- **Stable memory use.** The memory does not depend on the number of groups, so a bad estimate of $d$ does not cause an overflow, as it can for a hash table.
- **Deterministic.** The output does not depend on how ties in the merge are broken, for exact arithmetic.

## Variants and improvements

- **Stream aggregation.** If the input already comes sorted on $G$, for example from an index or a sort-merge join, only COMBINE runs, in one pass and with one record of memory. The first group is output as soon as its last row is read.
- **Duplicate elimination.** With no aggregate, the state is empty and COMBINE drops the duplicates. This is $\delta(R)$, and is how Bitton and DeWitt studied the method.
- **Longer runs.** [Replacement selection](/replacement-selection/) makes runs of about $2B$ pages on random input, so fewer merge passes are needed. With early aggregation, the heap can merge equal keys at once.
- **Merge order.** A system can merge fewer than $B - 1$ runs in the first merge pass so that all later passes merge full groups, as in external sorting.
- **Parallel.** Each worker sorts and combines its part, and the sorted partial results are merged by key ranges. This is the [combiner](/combiner/) step of MapReduce in sorted form.

## When to use it

Use sort-based aggregation when the input is already sorted on the key, when the output must be sorted on the key, or when the number of groups is not known and may be large. Use hash aggregation when the groups are few and the order does not matter, since it reads the input once and does not sort.

## Pitfalls

- **AVG of averages.** A partial AVG must keep $(\text{SUM}, \text{COUNT})$. Averaging partial averages gives a wrong answer when the parts have different sizes.
- **Holistic aggregates.** MEDIAN or COUNT DISTINCT have no state of fixed size. For COUNT DISTINCT, sort on $G$ and the column, and count the changes of the column inside each group.
- **Nulls.** SQL puts all rows with a null key into one group, so the sort order must place nulls together, either first or last. COUNT(\*) counts every row, while the other aggregates skip null values, and SUM of only nulls is null.
- **Empty input.** With no grouping columns, an empty input still gives one row, with COUNT equal to 0 and the other aggregates null. With grouping columns, it gives no row.
- **Floating point.** SUM over floating point values depends on the order of the additions, so two plans can give slightly different answers.

## Implementations

## History

Bitton and DeWitt (1983) studied duplicate elimination in large files, and showed that duplicates can be removed during the runs of an external merge sort and not only after it. Graefe's 1993 survey describes sort-based aggregation with early aggregation in the runs and compares it with hash-based aggregation. Both plans were in use in relational systems of the 1980s, and many systems still offer both, often under the names stream aggregate and hash aggregate.

## References
