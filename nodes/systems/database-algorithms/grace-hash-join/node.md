---
tag: MQ5FAS
kind: algorithm
slug: grace-hash-join
name: Grace hash join
aliases:
- partitioned hash join
- GRACE join
area: systems/database-algorithms
level: core
summary: "Split both relations into B - 1 partitions on disk with one hash function, then join each pair of partitions with an in-memory hash table and a second hash function. 3(M + N) I/Os."
solves: [relational-join]
model: external-memory-model
complexity:
  vars: {M: the number of pages of the smaller relation R, N: the number of pages of S, B: the number of buffer pages, f: the fudge factor of the hash table, p: the number of tuples per page of R, q: the number of tuples per page of S, T: the number of output tuples}
  time: {worst: Θ(p q M N), average: O(p M + q N + T), best: O(p M + q N + T)}
  space: {extra: Θ(M + N)}
  io:
    worst: "O((M + N) log_B M + M N)"
    average: "3(M + N)"
    best: "3(M + N)"
properties: {deterministic: true, exact: true, external: true, online: false, in_place: false, recursive: true}
history:
  year: 1983
  people: [Masaru Kitsuregawa, Hidehiko Tanaka, Tohru Moto-Oka]
  note: "The join method of the GRACE database machine at the University of Tokyo. It split both relations into buckets by a hash function, so that each pair of buckets could be joined in memory."
prereqs: [hash-join, external-memory-model]
see_also: [hybrid-hash-join, sort-merge-join, hash-partitioning, data-skew, reduce-side-join, hash-aggregation]
sources:
  - paper: doi:10.1007/BF03037022
    title: Masaru Kitsuregawa, Hidehiko Tanaka and Tohru Moto-Oka, Application of hash to data base machine and its architecture, New Generation Computing 1(1), 1983, pages 63 to 74
    locator: the hash-based join of the GRACE database machine (the partitioning of both relations into buckets and the join of each bucket pair)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Section 14.4.3, Hash Join (the partitioning and probing phases, the cost 3(M + N), the memory requirement B > sqrt(f M), and recursive partitioning of a partition that does not fit)
  - paper: doi:10.1145/6314.6315
    title: Leonard D. Shapiro, Join processing in database systems with large main memories, ACM Transactions on Database Systems 11(3), 1986, pages 239 to 264
    locator: the analysis of the GRACE hash join and its memory requirement, and the comparison with sort-merge and hybrid hash join
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 1993, pages 73 to 169
    locator: the section on hash join algorithms (overflow avoidance, recursive partitioning and skew)
---

The Grace hash join computes the equi-join of two relations that are too large for memory. It first reads both relations and splits each one into $B - 1$ *partitions* on disk with the same hash function $h_1$, so that tuples with equal keys land in partitions with the same number. Then, for each pair of partitions, it builds an in-memory [hash table](/hash-table/) on the partition of $R$ with a second hash function $h_2$ and probes it with the partition of $S$. Each page is read, written and read again, so the cost is $3(M + N)$ page I/Os when each partition of $R$ fits in memory, which needs $B > \sqrt{f M}$. It was the join method of the GRACE database machine of Kitsuregawa, Tanaka and Moto-Oka (1983).

## In plain words

You must match a huge pile of order slips with a huge pile of customer cards, and neither fits on your desk. First you sort them roughly into boxes: put each card in the box for the last digit of its customer number, and do the same with the slips, in a second row of boxes. A slip and its card always end up in boxes with the same digit.

Now take box 0 of cards to your desk. It is small enough. File its cards by customer number, then go through box 0 of slips and match each slip with the filed cards. Then do box 1, and so on. Each card and each slip is handled three times: read, put in a box, read again.

## The problem

The input is two relations $R$ and $S$ on disk and the condition $r.a = s.b$. The output is the multiset $R \bowtie S$, as on the page [relational join problem](/relational-join/). The method needs equality, because it relies on equal keys having equal hash values.

**Cost model.** The conventions are those of Ramakrishnan and Gehrke, Section 14.4. $R$ is the smaller relation, with $M$ pages and $p_R$ tuples per page; $S$ has $N$ pages and $p_S$ tuples per page; memory holds $B \ge 3$ pages. A hash table on $x$ pages of tuples needs $f \cdot x$ pages, for a fudge factor $f$ a little above 1. The cost is the number of page reads and writes, without the writes of the output. The front matter writes $p$ for $p_R$ and $q$ for $p_S$. The [external memory model](/external-memory-model/) counts the same transfers with other letters.

## The algorithm

```pseudo id=main
GRACE-HASH-JOIN(R, S, a, b, B, f)          ▷ the join r.a = s.b, B ≥ 3
L1  out ← an empty list, and push (R, S, 0) on a stack      ▷ a pair of inputs and a level
L2  while the stack is not empty do
L3      pop (R′, S′, ℓ)
L4      if ℓ > 0 and f · |R′| ≤ B − 2 then                    ▷ |R′| in pages: the partition fits
L5          build a table on R′ with h2, probe it with each tuple of S′, append the matches; continue
L6      read R′ and write each tuple r to partition R_i, with i = h1(r.a, ℓ) mod (B − 1)
L7      read S′ and write each tuple s to partition S_i, with i = h1(s.b, ℓ) mod (B − 1)
L8      for i ← 0 to B − 2 do
L9          if R_i or S_i is empty then skip i                  ▷ no tuple of this pair can match
L10         else if R_i does not fit and all its tuples have one key, or ℓ + 1 is the depth limit, then join R_i and S_i by block nested loops
L11         else push (R_i, S_i, ℓ + 1)
L12 return out
```

Lines L6 and L7 are the *partitioning phase*. Memory holds one input page and $B - 1$ output frames, one per partition. When a frame is full, it is written to its partition on disk. Line L5 is the *probing phase*, which is an in-memory [hash join](/hash-join/) with a second function $h_2$. The table must not use $h_1$: every tuple of $R_i$ has the same value of $h_1$ modulo $B - 1$, so a table that hashes with $h_1$ puts them into few buckets.

If a partition of $R$ is still too large, line L11 partitions the pair again at the next level with a new function $h_1(\cdot, \ell + 1)$. This is *recursive partitioning*. It cannot help when all tuples of $R_i$ have the same key, because every hash function sends them to the same partition, so line L10 then joins the pair with a [block nested-loop join](/block-nested-loop-join/). The implementation uses an explicit stack instead of recursion.

## Example

Let $R$ have the keys $[4, 7, 2, 9, 4, 6, 1, 5, 3, 8, 0, 2]$ (tuples $r_0$ to $r_{11}$) and $S$ have the keys $[2, 4, 3, 7, 0, 5]$ ($s_0$ to $s_5$), two tuples per page, so $M = 6$ and $N = 3$. With $B = 4$ there are $B - 1 = 3$ partitions, and for the example $h_1(k, 0) = k$, so the partition is $k \bmod 3$.

| partition | keys of $R_i$ | pages | keys of $S_i$ | pages | matches |
|---|---|---|---|---|---|
| 0 | 9, 6, 3, 0 | 2 | 3, 0 | 1 | $r_8 s_2$, $r_{10} s_4$ |
| 1 | 4, 7, 4, 1 | 2 | 4, 7 | 1 | $r_0 s_1$, $r_4 s_1$, $r_1 s_3$ |
| 2 | 2, 5, 8, 2 | 2 | 2, 5 | 1 | $r_2 s_0$, $r_{11} s_0$, $r_7 s_5$ |

Lines L6 and L7 read 9 pages and write 9 pages. Each partition of $R$ has 2 pages, which fits in $B - 2 = 2$, so line L5 reads each pair once: 9 more reads. The output has 8 tuples, and the cost is $27 = 3(M + N)$.

**The textbook sizes.** For Sailors ($M = 500$) and Reserves ($N = 1000$) with $B = 102$, each partition of Sailors has about $500/101 \approx 5$ pages, which fits. The cost is $3 \cdot 1500 = 4500$ I/Os, against 5500 for [block nested-loop join](/block-nested-loop-join/) with the same memory.

**Recursion and skew, from the tests.** With $B = 4$, two tuples per page and the keys $0$ to $17$ in both relations, each partition of $R$ has 3 pages, more than $B - 2$. Each is split again by the next digit in base 3, and the cost is $5(M + N) = 90$. With all 12 keys of $R$ and all 8 keys of $S$ equal, there is one full partition of 6 pages that no hash function can split; the cost is $10 + 10$ for the partitioning and $6 + 3 \cdot 4 = 18$ for the block nested-loop join, or 38 in total.

## Correctness

Two tuples with equal keys have equal values of $h_1(\cdot, \ell)$, so a matching pair $(r, s)$ lands in partitions $R_i$ and $S_i$ with the same $i$. Each tuple goes to exactly one partition, so $R' \bowtie S'$ is the disjoint union of the joins $R_i \bowtie S_i$. A pair with an empty side contributes nothing. Line L5, line L10 and the joins of the pairs pushed by line L11 each compute $R_i \bowtie S_i$, by induction on the number of pairs still to process. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **One level.** Lines L6 and L7 read $M + N$ pages and write them again into partitions. If every partition page is full, they write $M + N$ pages. Line L5 then reads every partition once, so the total is $3(M + N)$. In general, each nonempty partition can end with one page that is not full, so the cost is $M + N + 2W$, where $W \le M + N + 2(B - 1)$ is the number of pages written. The implementation also skips a pair with an empty side.
- **Memory.** If $h_1$ spreads the keys evenly, each partition of $R$ has about $M/(B - 1)$ pages, and its table fits when $f M/(B - 1) \le B - 2$. This holds roughly when $B > \sqrt{f M}$. Only the smaller relation matters, because the table is built on $R$. Sort-merge join needs about $\sqrt{M + N}$ instead.
- **Recursive partitioning.** If a partition does not fit, each further level reads and writes its pages once more, adding $2(M_i + N_i)$. With $L$ levels for all partitions, the cost is $(2L + 1)(M + N)$. A level divides the size of a partition by about $B - 1$, so $L \approx \lceil \log_{B-1} (f M / (B - 2)) \rceil + 1$, and the cost is $O((M + N) \log_B M)$ in the worst case without heavy duplicates.
- **Skew.** With many tuples of one key, a partition cannot shrink, and line L10 uses block nested loops, at $|R_i| + \lceil |R_i|/(B - 2) \rceil |S_i|$ I/Os on that pair. In the worst case, all tuples share one key, and the cost is quadratic in the pages, like any method, because the output has $|R| \cdot |S|$ tuples.
- **Work in memory.** With good hash functions, the expected work is $O(p_R M + p_S N + T)$ per level.

## Properties

- **Equality only.** Like every hash join, it needs an equality condition.
- **Memory on the smaller input.** The memory needed depends on $M$ only, not on $N$.
- **Blocking.** No output appears until both inputs have been partitioned, so the first tuple comes late.
- **Sensitive to skew.** Heavy keys make some partitions large. Recursive partitioning handles a skew of many keys, and block nested loops handles a single heavy key.
- **Exact and deterministic.** For a fixed hash function, the output and the I/O count are fixed.

## Variants and improvements

- **Hybrid hash join.** The [hybrid hash join](/hybrid-hash-join/) keeps partition 0 of $R$ in memory as a hash table during the partitioning, so the tuples of $S_0$ are joined at once and never written. It costs less than $3(M + N)$ when $B$ is large compared with $\sqrt{M}$.
- **Role reversal.** If a partition $S_i$ is smaller than $R_i$, build on $S_i$ instead. This saves memory and often avoids recursion.
- **Bit-vector filtering.** During the partitioning of $R$, set bits in a bit vector for the hash values of the keys. During the partitioning of $S$, drop each tuple whose bit is not set. This is the idea of the [Bloom join](/bloom-join/) and of [Bloom filters](/bloom-filter/).
- **Many partitions, then grouping.** Partition into more buckets than needed and then group small buckets so that each group fills memory. The GRACE machine used this to handle uneven bucket sizes.
- **On a cluster.** [Hash partitioning](/hash-partitioning/) both relations over the machines of a cluster is the same idea, with machines instead of partitions on disk. The [reduce-side join](/reduce-side-join/) does it with MapReduce, and the [data skew](/data-skew/) problem is the same.

## When to use it

Use it for an equi-join of two large relations when neither is sorted and the output does not need an order. With $B > \sqrt{f M}$, it costs $3(M + N)$, the same as a [sort-merge join](/sort-merge-join/) with combined passes, but needs memory only for the smaller relation. If the smaller relation fits in memory, the in-memory [hash join](/hash-join/) costs only $M + N$. If memory is between these sizes, the [hybrid hash join](/hybrid-hash-join/) is better. For keys with heavy skew, or when sorted output is needed, prefer the sort-merge join.

## Pitfalls

- **The same hash function for partitioning and probing.** Line L5 must use a function $h_2$ that is not $h_1$. With $h_1$, all tuples of a partition fall into the same few buckets of the table, and each probe scans a long chain.
- **The same function at every level.** Line L11 must use a new function $h_1(\cdot, \ell + 1)$. With the old one, the whole partition lands in one partition again, and the recursion never ends.
- **Recursion on a single key.** Line L10 must stop when a partition has one key. No hash function splits it, and recursive partitioning would loop until the depth limit.
- **Too many partitions.** Line L6 can use at most $B - 1$ partitions, one output frame each, with one frame left for the input page. More partitions than frames means frames are written before they are full, which wastes I/O.

## Implementations

## History

Kitsuregawa, Tanaka and Moto-Oka (1983) proposed the method for the GRACE database machine at the University of Tokyo: both relations are split into buckets by a hash function, and each pair of buckets is joined in memory. DeWitt et al. (1984) and Shapiro (1986) analyzed it next to the simple and hybrid hash joins for systems with large memories. Graefe's survey (1993) describes overflow handling, recursive partitioning and the treatment of skew. Ramakrishnan and Gehrke, Section 14.4.3, give the form with $B - 1$ partitions and the cost $3(M + N)$ used here.

## References
