---
tag: V6PA3X
kind: algorithm
slug: nested-loop-join
name: Nested-loop join
aliases:
- tuple nested-loop join
- simple nested-loop join
- page-oriented nested-loop join
area: systems/database-algorithms
level: intro
summary: "Join two relations by testing every pair of tuples: for each tuple or page of the outer relation, scan the whole inner relation. Works for any join condition."
solves: [relational-join]
model: external-memory-model
complexity:
  vars: {M: the number of pages of the outer R, N: the number of pages of the inner S, p: the number of tuples per page of R, q: the number of tuples per page of S}
  time: {worst: Θ(p q M N), average: Θ(p q M N), best: Θ(p q M N)}
  space: {extra: Θ(1)}
  io:
    worst: "M + p M N"
    average: "M + p M N"
    best: "M + p M N"
properties: {deterministic: true, exact: true, external: true, online: false, in_place: true, recursive: false}
history:
  year: 1977
  people: [Mike W. Blasgen, Kapali P. Eswaran]
  note: "Nested loops was one of the join methods of the System R project, which compared it with merging scans in the late 1970s. The idea is older than databases."
prereqs: [relational-join, external-memory-model]
see_also: [block-nested-loop-join, index-nested-loop-join, hash-join, sort-merge-join, set-similarity-join, spatial-join]
sources:
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Section 14.4.1, Nested Loops Join (simple nested loops join, the page-oriented version and the cost example with Reserves and Sailors), and Section 14.4.4, General Join Conditions
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 1993, pages 73 to 169
    locator: the section on nested-loops join algorithms
  - paper: doi:10.1145/582095.582099
    title: Patricia G. Selinger, Morton M. Astrahan, Donald D. Chamberlin, Raymond A. Lorie and Thomas G. Price, Access path selection in a relational database management system, SIGMOD 1979, pages 23 to 34
    locator: the section on the costs of joins (nested loops and merging scans)
---

The nested-loop join computes the [join](/relational-join/) of two relations by testing every pair of tuples. For each tuple (or each page) of the *outer* relation $R$ it scans the whole *inner* relation $S$ and outputs each pair that satisfies the join condition. It needs only three buffer pages and works for any condition, but it reads the inner relation once for each outer tuple or page, so it costs $M + p_R M N$ or $M + MN$ page I/Os. It is the reference that every other join algorithm must agree with.

## In plain words

You have a stack of order slips and a stack of customer cards, and you want every order next to the cards of its customer. The plain way: take the first order slip, then go through every customer card and note each card that matches. Then take the second slip and go through all the cards again, and so on.

This always works, whatever rule decides a match. But if the card stack is far away, you walk to it once for every order slip. A small change helps a lot: take a whole sheet of order slips at once, and compare each card with every slip on the sheet while you hold the card. Then you walk to the cards once per sheet, not once per slip.

## The problem

The input is two relations $R$ and $S$ on disk and a join predicate $\theta$. The output is the multiset $R \bowtie_\theta S$ of the tuples $r \cdot s$ with $\theta(r, s)$ true, as on the page [relational join problem](/relational-join/).

**Cost model.** This page uses the conventions of Ramakrishnan and Gehrke, Section 14.4. $R$ has $M$ pages with $p_R$ tuples per page, $S$ has $N$ pages with $p_S$ tuples per page, and there are $B$ buffer pages. The cost is the number of page I/Os, without the writes of the output. The front matter writes $p$ for $p_R$ and $q$ for $p_S$, and the letters differ from those of the [external memory model](/external-memory-model/), where $N$ is the input size, $M$ the memory and $B$ the block size.

## The algorithm

```pseudo id=main
NESTED-LOOP-JOIN(R, S, θ)             ▷ R is the outer relation, S the inner
L1  out ← an empty list
L2  for each page P of R do
L3      read P                        ▷ M reads in total
L4      for each tuple r of P do
L5          for each page Q of S do
L6              read Q                ▷ N reads for each tuple r
L7              for each tuple s of Q do
L8                  if θ(r, s) then append r · s to out
L9  return out
```

This is the *tuple-at-a-time* or *simple* nested-loop join. Memory holds one page of $R$, one page of $S$ and one output page, so $B = 3$ is enough. The outer loop reads $R$ once. For each tuple $r$, lines L5 to L8 scan all of $S$.

The *page-oriented* version swaps lines L4 and L5:

```pseudo id=page
PAGE-NESTED-LOOP-JOIN(R, S, θ)
P1  out ← an empty list
P2  for each page P of R do
P3      read P
P4      for each page Q of S do
P5          read Q                    ▷ N reads for each page of R
P6          for each tuple r of P and each tuple s of Q do
P7              if θ(r, s) then append r · s to out
P8  return out
```

Now $S$ is scanned once per page of $R$, not once per tuple, and the same pairs are tested. The [block nested-loop join](/block-nested-loop-join/) takes this one step further and scans $S$ once per block of $B - 2$ pages of $R$.

## Example

Let $R = \{(1, a), (2, b), (2, c), (3, d)\}$ and $S = \{(2, x), (3, y), (2, z)\}$ with the condition $r[0] = s[0]$, and two tuples per page. So $M = 2$, $N = 2$, $p_R = 2$: $R$ has pages $[(1,a), (2,b)]$ and $[(2,c), (3,d)]$, and $S$ has pages $[(2,x), (3,y)]$ and $[(2,z)]$.

| step | outer tuple $r$ | pages of $S$ read | output so far | reads so far |
|---|---|---|---|---|
| L3 | page 1 of $R$ | | | 1 |
| L4 to L8 | $(1, a)$ | 2 | none | 3 |
| L4 to L8 | $(2, b)$ | 2 | $(2,b,2,x)$, $(2,b,2,z)$ | 5 |
| L3 | page 2 of $R$ | | | 6 |
| L4 to L8 | $(2, c)$ | 2 | $+ (2,c,2,x)$, $(2,c,2,z)$ | 8 |
| L4 to L8 | $(3, d)$ | 2 | $+ (3,d,3,y)$ | 10 |

The output has 5 tuples and the cost is $M + p_R M N = 2 + 2 \cdot 2 \cdot 2 = 10$ reads. The page-oriented version gives the same 5 tuples with $M + MN = 2 + 2 \cdot 2 = 6$ reads.

**The textbook sizes.** Ramakrishnan and Gehrke join Reserves ($M = 1000$ pages, $p_R = 100$) with Sailors ($N = 500$, $p_S = 80$). The simple version costs $1000 + 100 \cdot 1000 \cdot 500 = 50{,}001{,}000$ I/Os. The page-oriented version costs $1000 + 1000 \cdot 500 = 501{,}000$, and with Sailors as the outer, $500 + 500 \cdot 1000 = 500{,}500$. The tests of the implementation check these formulas with exact counts on small inputs.

## Correctness

Each tuple $r$ of $R$ is met exactly once by lines L2 and L4, and for it each tuple $s$ of $S$ is met exactly once by lines L5 and L7. So line L8 tests each pair $(r, s)$ of $R \times S$ exactly once and appends $r \cdot s$ exactly when $\theta(r, s)$ is true. That is the definition of $R \bowtie_\theta S$ as a multiset. The page-oriented version tests the same pairs in a different order. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **Tuple at a time.** Line L3 runs $M$ times. Line L6 runs $N$ times for each of the $p_R M$ tuples of $R$. The total is $M + p_R M N$ reads, the same in every case, because the loops do not depend on the data.
- **Page at a time.** Line P3 runs $M$ times and line P5 runs $N$ times for each page of $R$, so the total is $M + MN$.
- **Which relation is the outer.** Swapping the roles gives $N + NM$ for the page-oriented version. So the relation with fewer pages should be the outer, and the gain is $|M - N|$ reads, which is small. For the simple version the cost is $M + |R| \cdot N$, so the relation with fewer *tuples* should be the outer, and here the gain can be large.
- **Work in memory.** Line L8 tests $|R| \cdot |S| = p_R p_S M N$ pairs in all versions.
- **Memory.** Three buffer pages. More memory does not help the simple version at all. It helps the block version.

## Properties

- **Any condition.** The predicate $\theta$ is a black box, so inequality joins, band joins and user-defined predicates all work.
- **Exact and deterministic.** It returns the exact multiset, in the order of $R$ and then of $S$.
- **Pipelined on the outer.** It can consume the outer relation as a stream from another operator, because it reads $R$ only once. The inner relation must be readable many times.
- **Order.** The output is in the order of the outer relation, so a sort order of $R$ is kept.

## Variants and improvements

- **Page at a time.** Lines P2 to P8 above, cost $M + MN$.
- **Block nested-loop join.** The [block nested-loop join](/block-nested-loop-join/) keeps $B - 2$ pages of $R$ in memory, often with a hash table on them, and costs $M + \lceil M/(B-2) \rceil N$.
- **Index nested-loop join.** If $S$ has an index on the join attribute, the [index nested-loop join](/index-nested-loop-join/) replaces the scan of lines L5 to L7 by one index probe.
- **Zig-zag scan.** Scan $S$ forward for one outer page and backward for the next. The pages of $S$ that are still in the buffer at the turn are not read again.
- **Equality joins.** For an equi-join, [hash join](/hash-join/) and [sort-merge join](/sort-merge-join/) avoid testing all pairs.

## When to use it

Use it when the inner relation is tiny (a few pages), when the condition is not an equality and no index helps, or as the reference oracle in tests. For equi-joins of large relations, it is almost never right: on the textbook sizes it costs $500{,}500$ I/Os, against $5{,}500$ for block nested loops with 102 buffer pages and $4{,}500$ for sort-merge or hash join. Similarity joins with a threshold, such as a [set similarity join](/set-similarity-join/), and overlap tests of a [spatial join](/spatial-join/) start from this method and then add filters or indexes to skip most pairs.

## Pitfalls

- **The larger relation as the outer in the simple version.** Line L2 should loop over the relation with fewer tuples. With Reserves as the outer, the simple version costs $50{,}001{,}000$ I/Os. With Sailors (40,000 tuples) as the outer it costs $500 + 40{,}000 \cdot 1000 = 40{,}000{,}500$.
- **The tuple loop outside the page loop.** Lines L4 and L5 in this order read $S$ once per tuple. If the buffer has room for a page of $R$ anyway, swap them as in lines P4 and P6.
- **A pipelined inner.** Lines L5 to L7 read $S$ many times. If $S$ is the output of another operator, it must first be written to disk, or the other operator must run again for each outer tuple.
- **Set semantics by mistake.** Line L8 appends one tuple for each matching pair. Removing duplicates there gives a wrong answer for SQL, which uses multisets.

## Implementations

## History

Nested loops is the most direct way to compute a join and is older than relational databases. Blasgen and Eswaran compared nested loops with sort-based joins for System R in the late 1970s, and Selinger et al. (1979) costed nested loops and merging scans in the System R optimizer. Ramakrishnan and Gehrke, Section 14.4.1, give the tuple and page versions with the cost formulas used here, and Graefe's survey (1993) covers the variants.

## References
