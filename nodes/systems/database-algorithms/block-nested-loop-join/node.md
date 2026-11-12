---
tag: 7N79ZS
kind: algorithm
slug: block-nested-loop-join
name: Block nested-loop join
aliases:
- BNLJ
- blocked nested-loop join
area: systems/database-algorithms
level: intro
summary: "A nested-loop join that reads the outer relation in blocks of B - 2 pages and scans the inner relation once per block, often with a hash table on the block."
solves: [relational-join]
model: external-memory-model
complexity:
  vars: {M: the number of pages of the outer R, N: the number of pages of the inner S, B: the number of buffer pages, p: the number of tuples per page of R, q: the number of tuples per page of S, T: the number of output tuples}
  time: {worst: Θ(p q M N), average: "O(p M + q N ⌈M/(B - 2)⌉ + T)", best: "O(p M + q N ⌈M/(B - 2)⌉)"}
  space: {extra: Θ(B)}
  io:
    worst: "M + ⌈M/(B - 2)⌉ N"
    average: "M + ⌈M/(B - 2)⌉ N"
    best: "M + ⌈M/(B - 2)⌉ N"
properties: {deterministic: true, exact: true, external: true, online: false, in_place: true, recursive: false}
history:
  year: 1980
  people: [Won Kim]
  note: "Kim proposed a nested-block method for the product and the join at SIGMOD 1980. The textbook form with B - 2 pages per block is in Ramakrishnan and Gehrke."
prereqs: [nested-loop-join]
see_also: [index-nested-loop-join, hash-join, grace-hash-join, sort-merge-join, hash-table, set-similarity-join]
sources:
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Section 14.4.1, Nested Loops Join (block nested loops join, the hash table on the outer block, the cost example with Reserves and Sailors, and blocked access to the inner)
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 1993, pages 73 to 169
    locator: the section on nested-loops join algorithms
---

Block nested-loop join computes the [join](/relational-join/) of $R$ and $S$ by reading the outer relation $R$ in blocks of $B - 2$ pages and scanning the inner relation $S$ once for each block. It is the [nested-loop join](/nested-loop-join/) with the memory put to use: the number of scans of $S$ drops from $M$ to $\lceil M/(B-2) \rceil$, so the cost is $M + \lceil M/(B-2) \rceil N$ page I/Os. For an equi-join, a hash table on the block finds the matches of each tuple of $S$ in expected constant time. It works for any join condition.

## In plain words

You must match order slips with customer cards, and your desk holds many slips at once. Fill the desk with order slips, sorted into piles by customer number. Then walk once through the whole card stack. For each card, look only at the pile with its number and note each match. When the cards are done, clear the desk, fill it with the next slips, and walk through the cards again.

The cards are read once for each desk load of slips, not once for each slip. A bigger desk means fewer walks. If all the slips fit on the desk, you walk through the cards only once.

## The problem

The input is two relations $R$ and $S$ on disk and a join condition. This page shows the equi-join $r.a = s.b$, where a hash table helps. The output is the multiset $R \bowtie S$, as on the page [relational join problem](/relational-join/).

**Cost model.** The conventions are those of Ramakrishnan and Gehrke, Section 14.4. $R$ has $M$ pages with $p_R$ tuples per page, $S$ has $N$ pages with $p_S$ tuples per page, and memory holds $B \ge 3$ pages. The cost is the number of page I/Os, without the writes of the output. The front matter writes $p$ for $p_R$ and $q$ for $p_S$. The [external memory model](/external-memory-model/) counts the same transfers with other letters.

## The algorithm

```pseudo id=main
BLOCK-NESTED-LOOP-JOIN(R, S, a, b, B)      ▷ the join r.a = s.b, B ≥ 3
L1  out ← an empty list
L2  for each block of B − 2 consecutive pages of R do
L3      read the pages of the block       ▷ M reads in total
L4      build a hash table H on the attribute a of the tuples of the block
L5      for each page Q of S do
L6          read Q                        ▷ N reads for each block
L7          for each tuple s of Q do
L8              for each tuple r in H with r.a = s.b do append r · s to out
L9  return out
```

Memory holds the $B - 2$ pages of the block, one input page for $S$ and one output page. Line L4 builds a [hash table](/hash-table/) in memory; it needs some space beyond the $B - 2$ pages, so in practice the block is a little smaller. For a general condition $\theta$, skip line L4 and let line L8 test each tuple of the block against $s$. The I/O count does not change, only the work in memory.

## Example

Let $R$ have keys $[1, 4, 2, 2, 5, 3, 1, 4, 6, 2]$ and $S$ have keys $[2, 4, 4, 7, 1, 2]$, two tuples per page, so $M = 5$ and $N = 3$. With $B = 4$, a block has $B - 2 = 2$ pages.

| block | keys in $H$ | matches of the keys of $S$ $(2, 4, 4, 7, 1, 2)$ | output | reads so far |
|---|---|---|---|---|
| pages 1 and 2 | 1, 4, 2, 2 | 2, 1, 1, 0, 1, 2 | 7 | $2 + 3 = 5$ |
| pages 3 and 4 | 5, 3, 1, 4 | 0, 1, 1, 0, 1, 0 | 3 | $5 + 2 + 3 = 10$ |
| page 5 | 6, 2 | 1, 0, 0, 0, 0, 1 | 2 | $10 + 1 + 3 = 14$ |

The output has $7 + 3 + 2 = 12$ tuples, and the cost is $M + \lceil M/(B-2) \rceil N = 5 + 3 \cdot 3 = 14$ reads. The page-oriented [nested-loop join](/nested-loop-join/) would read $5 + 5 \cdot 3 = 20$ pages.

**The textbook sizes.** For Reserves ($M = 1000$) and Sailors ($N = 500$) with $B = 102$, a block has 100 pages. With Reserves as the outer, the cost is $1000 + 10 \cdot 500 = 6000$ I/Os. With Sailors as the outer, it is $500 + 5 \cdot 1000 = 5500$. The tests of the implementation reproduce both counts on relations of these sizes.

## Correctness

The blocks partition the pages of $R$, so each tuple $r$ of $R$ is in exactly one block. While that block is in memory, lines L5 to L7 meet each tuple $s$ of $S$ exactly once, and line L8 appends $r \cdot s$ exactly when $r$ is in the bucket of $s.b$ with $r.a = s.b$. So the output holds one copy of $r \cdot s$ for each matching pair, which is the join as a multiset. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **I/O.** Line L3 reads each page of $R$ once: $M$ reads. There are $\lceil M/(B-2) \rceil$ blocks, and line L6 reads all $N$ pages of $S$ for each block. The total is $M + \lceil M/(B-2) \rceil N$, the same for every input of these sizes.
- **The outer relation.** Swapping the roles gives $N + \lceil N/(B-2) \rceil M$. The relation with fewer pages should usually be the outer, as in the textbook sizes, where it saves 500 I/Os.
- **One scan.** If $M \le B - 2$, there is one block and the cost is $M + N$, the minimum. This is then the in-memory [hash join](/hash-join/).
- **Work in memory.** With the hash table and a good hash function, line L8 costs expected $O(1)$ plus the number of matches. So the expected work is $O(|R| + |S| \lceil M/(B-2) \rceil + T)$, with $T$ the output size. With a general condition, each of the $|R| \cdot |S|$ pairs is tested.

## Properties

- **Any condition.** With a general predicate, it is the best method that does not need an index or an order. Only line L4 and line L8 depend on the condition.
- **Exact and deterministic.** The I/O count does not depend on the data.
- **No writes.** Unlike the [Grace hash join](/grace-hash-join/) and the [sort-merge join](/sort-merge-join/), it writes no temporary page.
- **Graceful in memory.** The cost falls smoothly as $B$ grows, from $M + MN$ at $B = 3$ to $M + N$ when $R$ fits.

## Variants and improvements

- **Blocked access to the inner.** Read $S$ in blocks too, for example with half the buffer for $R$ and half for $S$. The number of I/Os goes up a little, but the number of seeks goes down a lot, which can be faster on a disk (Ramakrishnan and Gehrke, Section 14.4.1).
- **Zig-zag scan.** Scan $S$ forward for one block and backward for the next, so the pages of $S$ still in the buffer are not read again.
- **Hash join.** When $R$ fits in memory, block nested-loop join with a hash table is the in-memory [hash join](/hash-join/). When it does not fit, the [Grace hash join](/grace-hash-join/) partitions both inputs and costs about $3(M + N)$, which is far less than $\lceil M/(B-2) \rceil N$ for large inputs.
- **Fallback inside hash joins.** Grace and hybrid hash join use block nested loops for a partition whose tuples all have the same key, because no hash function can split it.

## When to use it

Use it for a general condition with no useful index, or for an equi-join where the smaller relation fills only a few blocks. If $\lceil M/(B-2) \rceil$ is 1 or 2, it costs $M + N$ or $M + 2N$, which beats the $3(M + N)$ of a Grace hash join or a sort-merge join, and it writes nothing. If $M$ is many times $B$, a hash join or a sort-merge join is much cheaper: on the textbook sizes with $B = 102$, block nested loops costs 5500 I/Os against 4500 for both.

## Pitfalls

- **A block of $B$ pages.** Line L2 must use $B - 2$ pages: one frame is needed for the current page of $S$ and one for the output. A block of $B$ pages has no room to read $S$.
- **The larger relation as the outer.** Line L2 should loop over the smaller relation. With Reserves as the outer the textbook example costs 6000 I/Os; with Sailors it costs 5500.
- **Memory for the hash table.** Line L4 needs space for the table on top of the block. If the block uses all $B - 2$ frames, the table does not fit. Use a little fewer pages per block.
- **Duplicate keys in the block.** Line L8 must append every tuple of the bucket with an equal key, not only the first. A table that keeps one tuple per key loses matches.

## Implementations

## History

Reading the outer relation in large blocks to cut the scans of the inner relation goes back to the first relational systems. Kim (1980, "A new way to compute the product and join of relations", SIGMOD) proposed a nested-block method that keeps as much of the outer relation in memory as fits. Ramakrishnan and Gehrke, Section 14.4.1, give the form with $B - 2$ pages per block, the hash table on the block and the cost formula used here. Graefe's survey (1993) places it among the nested-loops variants.

## References
