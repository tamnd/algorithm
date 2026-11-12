---
tag: N97W1G
kind: algorithm
slug: index-nested-loop-join
name: Index nested-loop join
aliases:
- indexed nested-loop join
- index join
area: systems/database-algorithms
level: intro
summary: "A nested-loop join that, for each tuple of the outer relation, probes an index on the join attribute of the inner relation instead of scanning it."
solves: [relational-join]
model: external-memory-model
complexity:
  vars: {M: the number of pages of the outer R, p: the number of tuples per page of R, C: the I/O cost of one probe (index search plus the fetch of the matches), h: the height of the B+ tree, k: the number of matches of one probe, T: the number of output tuples}
  time: {worst: O(p M C + T), average: O(p M C + T), best: O(p M C + T)}
  space: {extra: Θ(1)}
  io:
    worst: "M + p M C"
    average: "M + p M C"
    best: "M + p M C"
properties: {deterministic: true, exact: true, external: true, online: false, in_place: true, recursive: false}
history:
  year: 1979
  people: [Patricia G. Selinger, Morton M. Astrahan, Donald D. Chamberlin, Raymond A. Lorie, Thomas G. Price]
  note: "The System R optimizer costed nested loops joins that use an index on the inner relation, and chose them when the outer relation is small."
prereqs: [nested-loop-join, b-plus-tree]
see_also: [block-nested-loop-join, clustered-index, covering-index, hash-join, sort-merge-join, map-side-join]
sources:
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Section 14.4.1, Nested Loops Join (index nested loops join, the cost of a probe with a hash or B+ tree index, clustered and unclustered, and the examples with Reserves and Sailors)
  - paper: doi:10.1145/582095.582099
    title: Patricia G. Selinger, Morton M. Astrahan, Donald D. Chamberlin, Raymond A. Lorie and Thomas G. Price, Access path selection in a relational database management system, SIGMOD 1979, pages 23 to 34
    locator: the sections on single-relation access paths and on the costs of nested loops joins with an index on the inner relation
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 1993, pages 73 to 169
    locator: the section on nested-loops join algorithms (index nested loops)
---

Index nested-loop join computes the [join](/relational-join/) of $R$ and $S$ by taking each tuple of the outer relation $R$ and looking up its matches in an index on the join attribute of the inner relation $S$. It is the [nested-loop join](/nested-loop-join/) with the scan of $S$ replaced by a probe of a [B+ tree](/b-plus-tree/) or a hash index. Its cost is $M + p_R M$ times the cost of one probe, so it does not depend on the size of $S$ at all. It is the method of choice when $R$ is small or very selective and $S$ already has an index.

## In plain words

You must find the customer card for each order slip, and the cards are in a filing cabinet with tabs by customer number. You do not read through all the cards for each slip. You take a slip, open the drawer at its number, and pull out the cards behind that tab.

Each slip now costs a few steps: find the tab, then pick up the cards. If the cards with the same number sit together, one grab gets them all. If they are spread over the cabinet, each card needs its own trip. The size of the cabinet hardly matters. What matters is how many slips you have.

## The problem

The input is a relation $R$, a relation $S$ with an index on its attribute $b$, and the equi-join condition $r.a = s.b$. The index can also answer a range condition such as $r.a < s.b$ if it is a B+ tree. The output is the multiset $R \bowtie S$, as on the page [relational join problem](/relational-join/).

**Cost model.** The conventions are those of Ramakrishnan and Gehrke, Section 14.4. $R$ has $M$ pages with $p_R$ tuples per page, $S$ has $N$ pages, and the cost is the number of page I/Os, without the writes of the output. The front matter writes $p$ for $p_R$ and $C$ for the cost of one probe. A probe costs the I/Os to find the matching index entries, plus the I/Os to fetch the matching tuples of $S$. The [external memory model](/external-memory-model/) counts the same transfers with other letters.

## The algorithm

```pseudo id=main
INDEX-NESTED-LOOP-JOIN(R, S, a, I)          ▷ I is an index on S.b
L1  out ← an empty list
L2  for each page P of R do
L3      read P                              ▷ M reads in total
L4      for each tuple r of P do
L5          E ← SEARCH(I, r.a)              ▷ the record ids of S with b = r.a
L6          for each record id (page q, slot i) in E do
L7              if the index is unclustered or q is not the page read last then
L8                  read page q of S
L9              append r · S[q][i] to out
L10 return out
```

Line L5 searches the index. For a [B+ tree](/b-plus-tree/) of height $h$ that stores pairs of a key and a record id, it reads $h$ inner pages and then every leaf that holds the key. For a hash index it reads the bucket page and its overflow pages. Lines L6 to L9 fetch the matching tuples. If the index is *clustered*, $S$ is stored in the order of the key, the matches lie on consecutive pages, and each page is read once. If it is *unclustered*, the matches can be on different pages, and each match costs one read. An index that stores the tuples of $S$ in its leaves needs no fetch at all.

## Example

Let $S$ have the keys $[5, 2, 8, 2, 6, 1, 9, 4]$ in the tuples $s_0, \ldots, s_7$, two tuples per page, with an unclustered B+ tree on the key. The leaves hold two entries each: $[1, 2]$, $[2, 4]$, $[5, 6]$, $[8, 9]$, and the tree has height $h = 2$. Let $R$ hold $(2, a), (7, b), (4, c), (9, d)$ on $M = 2$ pages.

| step | $r$ | line L5: index reads | matches | line L8: page reads | output | reads so far |
|---|---|---|---|---|---|---|
| L3 | page 1 of $R$ | | | | | 1 |
| L4 to L9 | $(2, a)$ | $2 + 2$ (key 2 is on two leaves) | $s_1$, $s_3$ | 2 | 2 | 7 |
| L4 to L9 | $(7, b)$ | $2 + 1$ | none | 0 | 0 | 10 |
| L3 | page 2 of $R$ | | | | | 11 |
| L4 to L9 | $(4, c)$ | $2 + 1$ | $s_7$ | 1 | 1 | 15 |
| L4 to L9 | $(9, d)$ | $2 + 1$ | $s_6$ | 1 | 1 | 19 |

The output has 4 tuples and the cost is 19 reads, which is $M$ plus the sum of the probe costs: $2 + (4 + 2) + 3 + (3 + 1) + (3 + 1)$.

**The textbook sizes.** Ramakrishnan and Gehrke join Reserves ($M = 1000$, $p_R = 100$) with Sailors ($N = 500$, $p_S = 80$). With a hash index on the key of Sailors, a probe costs about 1.2 I/Os to reach the index entry and 1 I/O to fetch the one matching sailor. The cost is $1000 + 100{,}000 \cdot 2.2 = 221{,}000$ I/Os. With Sailors as the outer and a hash index on the sailor id of Reserves, each sailor has $100{,}000/40{,}000 = 2.5$ reservations on average. A clustered index fetches them from one page, for $500 + 40{,}000 \cdot (1.2 + 1) = 88{,}500$ I/Os. An unclustered index fetches one page per reservation, for $500 + 40{,}000 \cdot (1.2 + 2.5) = 148{,}500$ I/Os. The 1.2 is an average from the textbook, not an exact count.

## Correctness

For each tuple $r$ of $R$, line L5 returns the record ids of exactly the tuples of $S$ with $b = r.a$, each once, because the index has one entry per tuple of $S$. Lines L6 to L9 append $r \cdot s$ once for each of them. Each $r$ is met once by lines L2 and L4. So the output holds one copy of $r \cdot s$ for each matching pair. Line L7 only decides whether a page must be read; it does not change the output. The full proof, with the B+ tree search, is in [the proof page](proofs/correctness.md).

## Complexity

- **I/O.** Line L3 reads $M$ pages. Line L5 runs once for each of the $p_R M$ tuples of $R$. With $C$ the average I/O cost of lines L5 to L8 for one tuple, the total is $M + p_R M \cdot C$.
- **The cost of one probe.** For a B+ tree of height $h$ whose key fits on $\ell$ leaves, the search costs $h + \ell$ reads in this implementation, where $h$ counts the inner levels and $\ell \ge 1$ even when the key is absent. A key larger than every key stops at the root after one read. Ramakrishnan and Gehrke use 2 to 4 I/Os for a B+ tree and about 1.2 for a hash index. The fetch costs the number of distinct pages of the matches for a clustered index, and $k$ reads for $k$ matches with an unclustered index.
- **Independent of $N$.** The cost does not grow with $S$, only with the height of the index. For a small outer relation and a large inner one, this is far below $M + N$.
- **Work in memory.** $O(p_R M C + T)$, with $T$ the output size.
- **Memory.** One page for $R$, one for the index path, one for $S$ and one for the output. The upper levels of the index are often kept in the buffer pool, which lowers the real cost of a probe to about one read.

## Properties

- **Exact and deterministic.** The output and the I/O count depend only on the data and the index.
- **Needs an index.** It cannot run without an index on the join attribute of the inner relation, or it must build one first.
- **Pipelined.** It reads $R$ once, in order, so it can take $R$ as a stream from another operator and keeps the order of $R$.
- **Range conditions.** With a B+ tree, line L5 can return all keys in a range, so it also does band joins and inequality joins.

## Variants and improvements

- **Clustered against unclustered.** A [clustered index](/clustered-index/) keeps $S$ in key order, so the matches of one probe cost one or a few page reads. An unclustered index costs one read per match.
- **Covering index.** If the index holds every attribute of $S$ that the query needs, a [covering index](/covering-index/) answers line L5 alone and lines L7 and L8 disappear.
- **Sorted outer.** Sort $R$ on $a$ first. Then equal keys probe the index one after the other and find its pages in the buffer, and the probes walk the leaves from left to right. The cost moves toward that of a [sort-merge join](/sort-merge-join/).
- **Hash index.** A hash index has a probe of about one read but cannot answer a range condition.
- **A B-tree instead of a B+ tree.** A [B-tree](/b-tree/) keeps keys and record ids in its inner nodes too, so some probes stop above the leaves. Its leaves are not linked, so a key with many matches costs more inner-node reads. The join is the same; only the probe cost $C$ changes.
- **On a cluster.** The [map-side join](/map-side-join/) of MapReduce uses the same idea when one input is small: each mapper looks up its tuples in a copy of the small input held in memory.

## When to use it

Use it when $S$ already has an index on the join attribute and $R$ is small, for example after a selective filter. Then $p_R M C$ is far below the $3(M + N)$ of a [hash join](/hash-join/) or a [sort-merge join](/sort-merge-join/). For a large $R$ it loses: on the textbook sizes, index nested loops costs $221{,}000$ I/Os with Reserves as the outer, against 4500 for a hash join. A rule of thumb follows from the formula: index nested loops wins when the number of outer tuples times the probe cost is less than the cost of reading both relations a few times.

## Pitfalls

- **An unclustered index with many matches.** If each key has $k$ matches spread over $S$, line L8 costs $k$ reads per probe. With many matches this is worse than a scan of $S$. The cost model must use $k$ for an unclustered index, not 1.
- **One leaf per probe.** Line L5 must read every leaf that holds the key. With many duplicates, a key spans several leaves, and a search that stops at the first leaf loses matches.
- **The wrong outer relation.** Line L2 should loop over the relation with fewer tuples, and the index must be on the other one. With the roles swapped the textbook cost goes from $88{,}500$ to $221{,}000$.
- **Repeated probes for equal keys.** If $R$ has the same key many times, line L5 searches the index each time. Sorting $R$ first, or caching the last result, removes the repeats.

## Implementations

## History

Index nested loops goes back to the first relational systems. The System R optimizer of Selinger et al. (1979) costed nested loops joins with an index on the inner relation and used them for small outer relations. Ramakrishnan and Gehrke, Section 14.4.1, give the cost formula with a hash or B+ tree index, clustered or not, used here, and Graefe's survey (1993) covers the variants.

## References
