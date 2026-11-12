---
tag: ET3B5B
kind: algorithm
slug: hash-aggregation
name: Hash aggregation
aliases:
- hash-based group-by
- hash aggregate operator
area: systems/database-algorithms
level: intro
summary: Group and aggregate rows in a hash table keyed by the group, with one partial state per group; spill new groups to hash partitions when memory is full.
solves: [group-by-aggregation]
model: word-ram
complexity:
  vars: {n: the number of input rows, d: the number of distinct groups, m: the number of group states that fit in memory}
  time: {worst: O(n (1 + d/m)), best: Θ(n)}
  space: {extra: Θ(m)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [group-by-aggregation, hash-table]
see_also: [grace-hash-join, hybrid-hash-join, hash-join, external-merge-sort, combiner, hash-partitioning, universal-hashing]
sources:
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 73 to 169 (1993)
    locator: Section 4 (aggregation and duplicate removal; hash-based aggregation, overflow by partitioning, and early aggregation)
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2009)
    locator: Chapter 15 (one-pass grouping with a main-memory table, and two-pass grouping based on hashing)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 14, Section 14.6 (aggregate operations, with and without grouping)
  - paper: doi:10.1023/A:1009726021843
    title: Jim Gray and others, Data cube, a relational aggregation operator generalizing group-by, cross-tab, and sub-totals, Data Mining and Knowledge Discovery 1(1), 29 to 53 (1997)
    locator: the classes of aggregate functions, which decide what a partial state is
---

Hash aggregation solves the [group-by aggregation problem](/group-by-aggregation/) with a [hash table](/hash-table/) that maps each group key to a partial state of its aggregates, such as $(\text{SUM}, \text{COUNT})$ for AVG. Each input row updates the state of its group at once, so memory holds one state per group and not one row per input row. When the groups do not fit in memory, rows of new groups are written to partitions by a hash of the key, as in the [Grace hash join](/grace-hash-join/), and each partition is aggregated in the same way. If the group states fit in memory, it reads the input once and costs $N$ page I/Os.

## In plain words

You count votes. You have a sheet of paper with one line for each candidate. For each ballot, you find the candidate's line and add one. When the counting ends, the sheet has the answer. You never keep the ballots.

The sheet has a fixed number of lines. When it is full and a ballot names a new candidate, you put that ballot in one of a few boxes. The candidate's name decides the box, so all ballots for one candidate go to the same box. The candidates on the sheet keep their lines, so their ballots never go to a box. When the first count ends, you write down the sheet, clear it, and count each box the same way.

## The problem

The input is a list of rows, the grouping columns $G$, and aggregates $f_1, \ldots, f_p$ on columns $A_1, \ldots, A_p$. Each aggregate is given by three functions: $\text{INIT}(v)$ makes a state from one value, $\text{MERGE}(s, s')$ joins two states, and $\text{FINAL}(s)$ gives the answer. MERGE is associative and commutative, and the state of a multiset $X \uplus Y$ is MERGE of the states of $X$ and $Y$. This holds for the distributive aggregates (COUNT, SUM, MIN, MAX) and for the algebraic ones (AVG with the state $(\text{SUM}, \text{COUNT})$). The output is one row per group, with each $\text{FINAL}$ value.

The cost model counts row operations for the time, with $n$ rows, $d$ distinct groups, a table of at most $m \ge 1$ states and a fan-out $F \ge 2$. For the I/O cost, the input has $N$ pages and the memory has $B$ pages of buffer.

## The algorithm

Each record is a pair (key, state). Level 0 makes one record per input row, with $\text{INIT}$ of its values.

```pseudo id=main
HASH-AGGREGATE(R, m, F)
L1  S ← a stack holding (the records of R, 0)
L2  while S is not empty do
L3      (P, ℓ) ← POP(S)
L4      T ← an empty hash table;  Q[0 .. F − 1] ← empty lists
L5      for each record (k, s) of P do
L6          if k ∈ T then T[k] ← MERGE(T[k], s)        ▷ early aggregation
L7          else if |T| < m then T[k] ← s
L8          else append (k, s) to Q[h_ℓ(k) mod F]      ▷ spill a partial state
L9      for each key k of T do output (k, FINAL(T[k]))
L10     for i ← 0 to F − 1 do
L11         if Q[i] is not empty then PUSH(S, (Q[i], ℓ + 1))
```

The hash function $h_\ell$ changes with the level $\ell$, so a partition that holds many keys is split again at the next level. The keys in $T$ stay there for the whole pass, so their rows never spill. In a database, $Q[i]$ is a file on disk with one output buffer page, and $F$ is at most $B - 1$ minus the pages of the table.

## Example

Group the sales (east, 10), (west, 5), (east, 7), (north, 3), (west, 5), (east, 1) by region with COUNT, SUM, MIN, MAX and AVG, with room for $m = 2$ groups and $F = 2$.

| step | record | action | table after the step |
|---|---|---|---|
| 1 | east, 10 | new key, room | east: (1, 10, 10, 10, (10, 1)) |
| 2 | west, 5 | new key, room | east, west: (1, 5, 5, 5, (5, 1)) |
| 3 | east, 7 | merge | east: (2, 17, 7, 10, (17, 2)) |
| 4 | north, 3 | table full: spill | unchanged |
| 5 | west, 5 | merge | west: (2, 10, 5, 5, (10, 2)) |
| 6 | east, 1 | merge | east: (3, 18, 1, 10, (18, 3)) |

Level 0 outputs east (3, 18, 1, 10, 6) and west (2, 10, 5, 5, 5). One record was written to disk. Level 1 reads that partition and outputs north (1, 3, 3, 3, 3). The answer is the same as the one from sorting on the region.

## Correctness

The key fact is about one pass of lines L5 to L8. Fix a key $k$ that occurs in $P$. The table never loses a key during the pass. If $k$ enters $T$ at its first record, each later record of $k$ finds $k \in T$ and is merged. If $k$ does not enter $T$ at its first record, then $|T| = m$ at that time, and $T$ keeps the same $m$ keys until the end of the pass, so each record of $k$ goes to the same list $Q[h_\ell(k) \bmod F]$. So each key is either output at line L9 with the MERGE of all its records of $P$, or all its records go to one partition. By associativity and commutativity, the merged state is the state of the multiset of all its values. The number of distinct keys in a partition is at most the number in $P$ minus $m$, so the process stops. The full proof is in the proof file.

## Complexity

- **Time.** One pass over $P$ costs $O(|P|)$ expected time with a good hash function, for a constant number of aggregates. A record is spilled once per level, and a key reaches level $\ell$ only if $\ell \cdot m$ other keys were taken before it, so there are at most $\lceil d/m \rceil$ levels. The worst-case time is $O(n (1 + d/m))$, and it is $\Theta(n)$ when $d \le m$. If the hash functions split the keys evenly, the keys of a partition at level $\ell$ are about $d / F^\ell$, and the number of levels is about $1 + \log_F (d/m)$; this is a heuristic estimate, not a worst-case bound.
- **Space.** The table holds at most $m$ states. The partitions hold at most $n$ records on disk at each level.
- **I/O.** If the $d$ states fit in memory, the cost is $N$ reads. Otherwise, with one level of partitioning, the input is read once ($N$), the spilled records are written once and read once. Since a spilled record is a partial state no larger than a row, this is at most $3N$, the same as two-pass sort-based grouping when $N \le B(B-1)$. The rows of the $m$ groups kept in memory are never written, as in the [hybrid hash join](/hybrid-hash-join/).
- **Holistic aggregates.** For MEDIAN the state is the list of all values of the group, so the table memory grows with the rows, not with the groups.

## Properties

- **Early aggregation.** Rows are combined as they arrive, so the memory and the spill volume depend on the number of groups more than on the number of rows.
- **Not order preserving.** The output comes in hash order. A sort-based plan gives the groups in key order, which a later `ORDER BY` can use.
- **Blocking.** No group is final until its whole input is read, so the first output row comes after the scan.
- **Deterministic** for a fixed hash function. The output set does not depend on the hash; only the spill volume does.

## Variants and improvements

- **One-pass hash aggregation.** No partitions: the plan of choice when the optimizer knows that $d$ is small.
- **Hybrid hash aggregation.** This page's version keeps the first $m$ groups in memory and spills only new groups. The plain Grace-style version partitions all rows first and aggregates each partition in a second pass.
- **Pre-aggregation of partitions.** Spill records go through a small table per partition, which merges equal keys before the write.
- **Parallel and distributed.** Each worker aggregates locally, then states are sent by [hash partitioning](/hash-partitioning/) on the key and merged. This is the [combiner](/combiner/) of MapReduce.
- **Switch to sorting.** Some systems sort a partition that still does not fit at a deep level, which bounds the depth.

## When to use it

Use hash aggregation when the number of groups is much smaller than the number of rows, and the output order does not matter. Use sort-based grouping when the input is already sorted on the key, when the output must be sorted, or when the aggregate is holistic.

## Pitfalls

- **One hash function at all levels.** If $h_\ell$ does not change with $\ell$, a partition with too many keys goes to a single child partition again. This version still stops, because $m$ keys leave each level, but the depth can grow to $d/m$.
- **AVG of averages.** A spilled AVG must keep $(\text{SUM}, \text{COUNT})$. Averaging the partial averages gives a wrong answer when the parts have different sizes.
- **Holistic aggregates in a fixed-size table.** MEDIAN or COUNT DISTINCT cannot be kept in a fixed-size state, so the memory estimate that counts groups is wrong for them.
- **Skew.** One very large group is not a problem for a distributive aggregate (its state is small). It is a problem for holistic aggregates and for partition sizes in parallel plans.
- **Floating point.** SUM over floating point values depends on the order of the additions, so two plans can give slightly different answers. Exact numbers (integers or fractions) avoid this.

## Implementations

## History

Graefe's 1993 survey describes hash-based aggregation and duplicate removal with overflow handled by partitioning, and compares it with sort-based aggregation; both plans were in use in relational systems of the 1980s. Gray et al. (1997) named the distributive, algebraic and holistic classes, which tell which aggregates a hash table can keep in a state of fixed size.

## References
