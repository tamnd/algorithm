---
tag: 2CCGX1
kind: algorithm
slug: hash-join
name: Hash join
aliases:
- in-memory hash join
- classic hash join
area: systems/database-algorithms
level: intro
summary: "Build a hash table on the join key of the smaller relation, then scan the larger relation and probe the table with each tuple. One pass, M + N page reads, if the table fits in memory."
solves: [relational-join]
model: external-memory-model
complexity:
  vars: {M: the number of pages of the smaller relation R, N: the number of pages of the larger relation S, B: the number of buffer pages, p: the number of tuples per page of R, q: the number of tuples per page of S, T: the number of output tuples}
  time: {worst: Θ(p q M N), average: O(p M + q N + T), best: O(p M + q N + T)}
  space: {extra: Θ(M)}
  io:
    worst: "M + N"
    average: "M + N"
    best: "M + N"
properties: {deterministic: true, exact: true, external: true, online: false, in_place: false, recursive: false}
history:
  year: 1984
  people: [David J. DeWitt, Randy H. Katz, Frank Olken, Leonard D. Shapiro, Michael R. Stonebraker, David Wood]
  note: "Hash joins became a standard method in the early 1980s, when memories grew large enough to hold a hash table on one input. DeWitt et al. compared them with sort-merge joins in 1984."
prereqs: [relational-join, hash-table]
see_also: [grace-hash-join, hybrid-hash-join, block-nested-loop-join, sort-merge-join, hash-aggregation, map-side-join]
sources:
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Section 14.4.3, Hash Join (the build and probe phases, the fudge factor f for the hash table, and the memory requirement), and Section 14.4.1 (block nested loops with a hash table on the outer block)
  - paper: doi:10.1145/602259.602261
    title: David J. DeWitt, Randy H. Katz, Frank Olken, Leonard D. Shapiro, Michael R. Stonebraker and David Wood, Implementation techniques for main memory database systems, SIGMOD 1984, pages 1 to 8
    locator: the section on join algorithms (the hash join methods and their comparison with sort-merge)
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 1993, pages 73 to 169
    locator: the section on hash join algorithms (build input and probe input)
---

Hash join computes the equi-join of two relations by building a [hash table](/hash-table/) on the join key of the smaller relation $R$, the *build input*, and then scanning the larger relation $S$, the *probe input*, and looking up each of its tuples in the table. Each relation is read once, so the cost is $M + N$ page I/Os, the least possible. It needs the table on $R$ to fit in memory, about $f \cdot M \le B - 2$ pages for a small overhead factor $f$. When it does not fit, the [Grace hash join](/grace-hash-join/) and the [hybrid hash join](/hybrid-hash-join/) first split both inputs into parts that do.

## In plain words

You have a short list of customers and a long stack of order slips. You copy the customers onto index cards and file them in a box with one slot for each last digit of the customer number. Now you take the order slips one by one. For each slip you look at the last digit of its customer number, open that one slot, and look only at the few cards in it. For each card with the same number, you write a combined line.

You go through each list once. The only condition is that the box with all the customer cards fits on your desk.

## The problem

The input is two relations $R$ and $S$ on disk and the condition $r.a = s.b$. The output is the multiset $R \bowtie S$, as on the page [relational join problem](/relational-join/). Hashing works only for equality: it puts equal keys in the same bucket but says nothing about order.

**Cost model.** The conventions are those of Ramakrishnan and Gehrke, Section 14.4. $R$ has $M$ pages with $p_R$ tuples per page, $S$ has $N$ pages with $p_S$ tuples per page, $M \le N$, and memory holds $B$ pages. A hash table on $M$ pages of tuples takes $f \cdot M$ pages, where the *fudge factor* $f$, a little more than 1, covers the pointers and the free space of the table. The cost is the number of page I/Os, without the writes of the output. The front matter writes $p$ for $p_R$ and $q$ for $p_S$. The [external memory model](/external-memory-model/) counts the same transfers with other letters.

## The algorithm

```pseudo id=main
HASH-JOIN(R, S, a, b, B, f)                ▷ the join r.a = s.b
L1  if R has more pages than S then swap the roles of R and S      ▷ build on the smaller input
L2  if f · M > B − 2 then fail             ▷ use a Grace or hybrid hash join instead
L3  H ← an empty hash table
L4  read each page of R and insert each tuple r into H with the key r.a      ▷ build phase
L5  out ← an empty list
L6  for each page Q of S do                ▷ probe phase
L7      read Q
L8      for each tuple s of Q and each tuple r in the bucket of s.b with r.a = s.b do append r · s to out
L9  return out
```

Memory holds the table on $R$, one input page for $S$ and one output page, which is why line L2 compares with $B - 2$. Line L4 is the *build phase*: the table here uses [separate chaining](/separate-chaining/) and keeps all tuples with the same key, so duplicates on the build side are kept. Lines L6 to L8 are the *probe phase*. A probe hashes $s.b$, goes to one bucket and compares $s.b$ with the key of each tuple in it, because different keys can share a bucket.

## Example

Let $R$ have the keys $[3, 1, 4, 1, 5, 9, 2, 6]$ (tuples $r_0$ to $r_7$) and $S$ have the keys $[1, 4, 1, 8]$ ($s_0$ to $s_3$), two tuples per page, so $R$ has 4 pages and $S$ has 2. With $B = 4$ and $f = 1$, line L1 swaps the roles: the build input is $S$, because $2 \le B - 2 = 2$.

| step | tuple | action | output so far | reads so far |
|---|---|---|---|---|
| L4 | page 1 of $S$ | insert $s_0$ (key 1), $s_1$ (key 4) | 0 | 1 |
| L4 | page 2 of $S$ | insert $s_2$ (key 1), $s_3$ (key 8) | 0 | 2 |
| L7 to L8 | $r_0$ (3), $r_1$ (1) | $r_1$ finds $s_0, s_2$ | 2 | 3 |
| L7 to L8 | $r_2$ (4), $r_3$ (1) | $r_2$ finds $s_1$, $r_3$ finds $s_0, s_2$ | 5 | 4 |
| L7 to L8 | $r_4$ (5), $r_5$ (9) | none | 5 | 5 |
| L7 to L8 | $r_6$ (2), $r_7$ (6) | none | 5 | 6 |

The output has 5 tuples, and the cost is $2 + 4 = 6$ reads, which is $M + N$. The implementation writes each output tuple as $r \cdot s$ even when $S$ is the build input.

**The textbook sizes.** For Reserves (1000 pages) and Sailors (500 pages), a table on Sailors needs about $f \cdot 500$ pages. With $B \ge 502$ and $f = 1$, hash join costs $500 + 1000 = 1500$ I/Os. With $B = 102$ it cannot run, and the choice is between [block nested-loop join](/block-nested-loop-join/) at 5500 I/Os and a [Grace hash join](/grace-hash-join/) at $3 \cdot 1500 = 4500$.

## Correctness

After line L4, the bucket of a key $v$ holds every tuple of $R$ with $r.a = v$, each once, and possibly tuples with other keys. Line L8 meets each tuple $s$ of $S$ once, and for it appends $r \cdot s$ exactly for the tuples $r$ of the bucket with $r.a = s.b$, which are exactly the matches of $s$. So the output holds one copy of $r \cdot s$ for each matching pair. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **I/O.** Line L4 reads each page of $R$ once and line L7 reads each page of $S$ once: $M + N$ reads, with no writes. This does not depend on the data.
- **Memory.** $f \cdot M + 2$ pages. So hash join needs memory about the size of the *smaller* input, while [sort-merge join](/sort-merge-join/) needs about $\sqrt{M + N}$ pages to reach $3(M + N)$.
- **Work in memory.** With a table of $\Theta(p_R M)$ buckets and a hash function from a [universal family](/universal-hashing/), a probe looks at an expected $O(1)$ tuples with other keys. So the expected work is $O(p_R M + p_S N + T)$, where $T$ is the output size. The worst case is $\Theta(p_R p_S M N)$ comparisons, when all keys collide in one bucket.

## Properties

- **One pass.** It reads each input once and writes nothing, so its I/O cost is the lower bound $M + N$.
- **Pipelined probe.** The probe input is read once in order, so it can be a stream from another operator, and the output comes in the order of $S$. The build input must be complete before the first output.
- **Equality only.** Hashing cannot answer $r.a < s.b$ or a band condition.
- **Skew.** A key with many tuples makes a long chain, but the result stays correct and the I/O cost stays $M + N$.

## Variants and improvements

- **Grace hash join.** When $f \cdot M > B - 2$, the [Grace hash join](/grace-hash-join/) partitions both inputs into $B - 1$ parts on disk with one hash function, then runs this algorithm on each pair of parts with a second hash function. It costs $3(M + N)$.
- **Hybrid hash join.** The [hybrid hash join](/hybrid-hash-join/) keeps one part of $R$ in memory during the partitioning and joins it at once, so its cost moves smoothly from $M + N$ to $3(M + N)$ as memory shrinks.
- **The name "simple hash join".** In DeWitt et al. (1984), the *simple hash join* is a method that builds a table on as much of $R$ as fits, writes the rest of $R$ and the matching part of $S$ back to disk, and repeats. It is not the one-pass algorithm of this page, although some texts use the name for it.
- **Block nested loops.** A [block nested-loop join](/block-nested-loop-join/) with a hash table on each block is this algorithm repeated once per block of $R$.
- **Aggregation.** [Hash aggregation](/hash-aggregation/) uses the same build step to group tuples by key, with one entry per group instead of one per tuple.
- **On a cluster.** The broadcast or [map-side join](/map-side-join/) sends a copy of the small relation to every machine and runs a hash join there.

## When to use it

Use it when the smaller input fits in memory, which is common after a selective filter or for a small dimension table. It then beats every other method, with $M + N$ I/Os. When the smaller input is a little too large, use the [hybrid hash join](/hybrid-hash-join/), and when it is much larger than memory, use the [Grace hash join](/grace-hash-join/) or a [sort-merge join](/sort-merge-join/). For a non-equality condition, use a nested-loop join.

## Pitfalls

- **Building on the larger relation.** Line L1 must put the smaller relation into the table. Building on the larger one needs more memory and fails line L2 sooner, for no gain: the I/O cost is $M + N$ either way.
- **Ignoring the table overhead.** Line L2 must use $f \cdot M$, not $M$. A table with pointers and a load factor below one is larger than the data, and a table that does not fit makes the system page.
- **Keeping one tuple per key.** Line L4 must keep every tuple with the same key. A map from a key to one tuple loses matches when $R$ has duplicate keys.
- **Comparing only hash values.** Line L8 must compare the keys themselves, not their hash values: two different keys can have the same hash value.

## Implementations

## History

Hash-based joins came into use in the early 1980s, when main memories grew large enough to hold a hash table on one relation. DeWitt, Katz, Olken, Shapiro, Stonebraker and Wood (1984) studied hash joins for large memories, including the simple, Grace and hybrid hash joins, and showed that they beat sort-merge joins in many cases. Graefe's survey (1993) names the build and probe inputs and describes the variants. Ramakrishnan and Gehrke, Section 14.4.3, give the in-memory join as the probing phase of the partitioned hash join.

## References
