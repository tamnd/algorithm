---
tag: GRDTV2
kind: algorithm
slug: logarithmic-merging
name: Logarithmic merging
aliases:
- logarithmic index merging
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Keeps indexes of sizes n, 2n, 4n and so on, and merges two of equal size like a binary counter, so each posting is merged O(log(T/n)) times.
solves: [dynamic-index-maintenance]
model: external-memory-model
complexity:
  vars: {T: the number of postings added so far, n: the number of postings that the in-memory index holds}
  time: {build: Θ(T log(T/n)), insert: O(log(T/n)) amortized, indexes_per_query: O(log(T/n))}
  space: {memory: O(n), disk: O(T)}
properties: {deterministic: true, online: true, recursive: false, comparison: true, in_place: false}
prereqs: [dynamic-index-maintenance, binary-counter-increment, inverted-index]
see_also: [geometric-partitioning, log-structured-merge-tree, decomposable-searching-problem, single-pass-in-memory-indexing, blocked-sort-based-indexing, k-way-merge, amortized-cost, posting-list]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 4, Section 4.5 (dynamic indexing, the auxiliary index, the LMERGEADDTOKEN pseudocode, and the bound of O(log(T/n)) merges for each posting)
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 7 (dynamic inverted indices), Section 7.2 (incremental index updates) and Section 7.3 (document deletions)
  - paper: doi:10.1016/0196-6774(80)90015-2
    title: Jon Louis Bentley and James B. Saxe, Decomposable searching problems I. Static-to-dynamic transformation, Journal of Algorithms 1(4), 1980, pages 301 to 358
    locator: the binary transformation, which keeps static structures of sizes that are powers of two
  - paper: doi:10.1145/1099554.1099739
    title: Nicholas Lester, Alistair Moffat and Justin Zobel, Fast on-line index construction by geometric partitioning, Proceedings of CIKM 2005, pages 776 to 783
    locator: Section 3 (merge-based update strategies, the remerge cost that logarithmic schemes avoid)
---

Logarithmic merging keeps an [inverted index](/inverted-index/) up to date while new documents arrive. New postings go into a small index in memory. When it holds $n$ postings it goes to disk, and the disk indexes are kept at sizes $n, 2n, 4n, \ldots$, at most one of each size. When two indexes of the same size exist, they are merged into one of double size, in the same way that adding 1 to a [binary counter](/binary-counter-increment/) turns two 1 bits into a carry. Each posting is then merged at most $\lfloor \log_2(T/n) \rfloor$ times in total, in place of up to $T/n$ times with one auxiliary index. It is the static-to-dynamic method of the [decomposable searching problem](/decomposable-searching-problem/) applied to posting lists. The [log-structured merge tree](/log-structured-merge-tree/) applies the same idea to key-value stores, with a fixed size ratio between levels. [Geometric partitioning](/geometric-partitioning/) uses other ratios and limits the number of indexes. This page covers the scheme with ratio 2, in the form of Manning, Raghavan and Schuetze.

## In plain words

Think of a pile of sorted card boxes. New cards go into a small box on your desk. When the desk box is full, you put it on the shelf. If the shelf already has a box of the same size, you do not keep two: you merge them into one box of double size. If a box of that new size is also there, you merge again, and so on. So the shelf never has two boxes of the same size. A card is merged again only when its box doubles, so it is merged only a few times, even when the collection grows very large. A search must look in each box on the shelf, but there are only a few boxes.

## The problem

Postings arrive one at a time, in any order of terms. After each arrival, a query for a term must return its full posting list over all postings so far. The work to measure is the number of postings that merges write to disk. The simple scheme with one main index and one auxiliary index of $n$ postings in memory merges the auxiliary index into the main index each time it is full. Then the main index is rewritten at each flush, and building an index of $T$ postings costs $\Theta(T^2/n)$ postings written. The goal is to cut this cost, and to keep the number of indexes that a query reads small. The general problem, with deletions, is [dynamic index maintenance](/dynamic-index-maintenance/).

## The algorithm

$Z_0$ is the index in memory, with room for $n$ postings. $I_0, I_1, \ldots$ are the indexes on disk, and $I_i$, when it exists, has exactly $2^i n$ postings. MERGE joins two indexes into one, list by list, as a [k-way merge](/k-way-merge/) with $k = 2$.

```pseudo id=main
LMERGE-ADD(x)                          ▷ x: one new posting
L1  Z0 ← MERGE(Z0, {x})                 ▷ in memory
L2  if |Z0| = n then
L3      Z ← Z0, i ← 0
L4      while I_i exists do
L5          Z ← MERGE(I_i, Z), delete I_i  ▷ now |Z| = 2^(i+1) n
L6          i ← i + 1
L7      I_i ← Z, Z0 ← empty             ▷ written to disk

QUERY(t)
L8  read the list of t from Z0 and from each I_i that exists
L9  return the union of these lists, in increasing document id order
```

Line L1 adds the posting to the in-memory index. When $Z_0$ is full (line L2), lines L3 to L6 carry it up the levels. At level $i$, if $I_i$ exists, line L5 merges it with the carry, which doubles the size, and deletes it. Line L7 stores the carry at the first free level. This is the binary counter: the existing levels are the 1 bits of the number of flushes so far, and a flush clears the trailing 1 bits and sets the next 0 bit. Lines L8 and L9 answer a query from all indexes. The indexes hold disjoint sets of postings, so the union is the full list.

## Example

Take $n = 4$ and add 32 postings, so that $Z_0$ is flushed 8 times. The table shows the levels after each flush and the number of postings that the merges of line L5 write in that flush.

| flush $t$ | $t$ in binary | levels after the flush | merges at line L5 | postings written by merges |
|---|---|---|---|---|
| 1 | 1 | $I_0$ | none | 0 |
| 2 | 10 | $I_1$ | $I_0$ | 8 |
| 3 | 11 | $I_0, I_1$ | none | 0 |
| 4 | 100 | $I_2$ | $I_0$, $I_1$ | 8 + 16 = 24 |
| 5 | 101 | $I_0, I_2$ | none | 0 |
| 6 | 110 | $I_1, I_2$ | $I_0$ | 8 |
| 7 | 111 | $I_0, I_1, I_2$ | none | 0 |
| 8 | 1000 | $I_3$ | $I_0$, $I_1$, $I_2$ | 8 + 16 + 32 = 56 |

The merges write 96 postings in total. That is $T \log_2(T/n) = 32 \cdot 3$: each of the 32 postings is merged exactly 3 times, once at each doubling from 4 to 32. With one auxiliary index, flush $t \ge 2$ rewrites the main index of $4t$ postings, which costs $4 \cdot (2 + 3 + \cdots + 8) = 140$ postings. The gap grows with $T$: at 1,024 flushes of the same $n$, logarithmic merging writes $4 \cdot 1024 \cdot 10 = 40{,}960$ postings, while the auxiliary scheme writes $4 \cdot (1024 \cdot 1025/2 - 1) = 2{,}099{,}196$. Right after flush 7, a query reads three disk indexes; right after flush 8 it reads one.

## Correctness

The proof keeps three statements true after each call. $Z_0$ holds $T \bmod n$ postings. The level $I_i$ exists exactly when bit $i$ of $\lfloor T/n \rfloor$ is 1, and then it holds $2^i n$ postings. And $Z_0$ and the levels hold disjoint sets whose union is all postings added so far. A call that does not fill $Z_0$ keeps all three. A call that fills $Z_0$ carries through the trailing 1 bits of the flush count: the loop keeps $|Z| = 2^i n$ and moves the postings of each merged level into $Z$, then line L7 sets the first 0 bit. So no posting is lost or copied, and a query that takes the union of all levels is correct. The full proof, with the count of merges, is in the proof file below.

## Complexity

- **Merges for one posting.** Each merge that a posting takes part in doubles the size of the index that holds it, from $n$ up to at most $T$. So a posting is merged at most $\lfloor \log_2(T/n) \rfloor$ times. Manning, Raghavan and Schuetze state this as $O(\log(T/n))$ merges for each posting.
- **Total merge work.** Summed over the postings, the merges write at most $T \lfloor \log_2(T/n) \rfloor$ postings, so the build costs $\Theta(T \log(T/n))$, against $\Theta(T^2/n)$ for one auxiliary index. When $T = 2^m n$ the count is exactly $mT$. The amortized cost of one insertion is $O(\log(T/n))$ postings written.
- **Worst case for one insertion.** One flush can merge every level, which writes up to $2T$ postings. The bound is amortized, not a worst case per insertion.
- **Queries.** A query reads $Z_0$ and up to $\lfloor \log_2(T/n) \rfloor + 1$ disk indexes, in place of 2 with one auxiliary index. This is the price of the cheaper merges.
- **Space.** $O(n)$ words of memory, and $O(T)$ words of disk. During a carry, the old levels and the new one exist at the same time, so the disk can briefly hold up to twice the index.

## Properties

- **Online.** Each posting is visible to queries right after LMERGE-ADD returns.
- **Deterministic.** The levels present depend only on $\lfloor T/n \rfloor$.
- **Sequential disk access.** Each merge reads two sorted indexes from start to end and writes one.
- **Ratio 2.** The size of each level is twice the size of the level below. With ratio $r$, both the merge cost and the number of levels change, which is what geometric partitioning studies.

## Variants and improvements

- **Geometric partitioning.** Lester, Moffat and Zobel allow up to $r - 1$ indexes per level for a ratio $r$, and merge many of them in one multiway merge. A fixed bound on the number of indexes is also possible. See [geometric partitioning](/geometric-partitioning/).
- **One multiway merge per carry.** In LMERGE-ADD, a carry through levels $0, \ldots, c-1$ writes $(2^{c+1} - 2) n$ postings in a chain of pairwise merges. A single merge of $Z_0$ and all these levels writes only $2^c n$. The example would then write 64 postings, not 96.
- **Deletions.** A deleted document goes into an invalidation bit vector that queries filter against. The postings are removed when the merges rewrite their index, or by garbage collection. Buettcher, Clarke and Cormack discuss both methods.
- **Logarithmic method in general.** Bentley and Saxe show the same transformation for any decomposable searching problem: a static structure that can be built in time $P(n)$ becomes a dynamic one with amortized insertion cost $O((P(n)/n) \log n)$ and queries over $O(\log n)$ structures.
- **Log-structured merge trees.** Key-value stores keep levels with a fixed size ratio, often 10, and merge a level into the next one when it is full. See [log-structured merge tree](/log-structured-merge-tree/).

## When to use it

Use logarithmic merging when documents arrive all the time and must be searchable soon, and when the cost of rebuilding or remerging the whole index at each flush is too high. It suits collections that grow by orders of magnitude. If queries are much more frequent than updates, the many indexes slow each query, so a scheme with fewer indexes, or a periodic full merge in the background, can be better. For a static collection, build the index once with [single-pass in-memory indexing](/single-pass-in-memory-indexing/) or [blocked sort-based indexing](/blocked-sort-based-indexing/).

## Pitfalls

- **Wrong bound.** The bound is $O(\log(T/n))$ merges for each posting, not $O(\log T)$. With $T = n$ there is no merge at all. The difference matters when $n$ is large, as it is in practice.
- **Merge without deleting the old level.** If line L5 forgets to delete $I_i$, a query reads the postings of $I_i$ twice, once in $I_i$ and once in the new level. The level must be deleted after the merge, as in line L5.
- **Merge at the wrong level.** Merging $Z_0$ always into the largest level in place of the carry of lines L4 to L6 gives back the auxiliary scheme with its $\Theta(T^2/n)$ cost.
- **Collection statistics.** A score such as [BM25](/bm25/) needs the document frequency of a term over the whole collection. Each level only knows its own part, so the engine must add the counts over all levels, or keep the statistics in a separate global table.
- **Burst of work.** One flush can rewrite the whole index. A system that must answer queries during updates needs to run the merge in the background, and to keep the old levels readable until the new one is complete.

## Implementations

## History

Bentley and Saxe described the binary transformation for decomposable searching problems in 1980, with structures of sizes that are powers of two. For text indexes, Lester, Moffat and Zobel in 2005 compared merge-based update strategies such as rebuild, in-place update and remerge, and proposed geometric partitioning, which keeps partitions of geometrically growing sizes with any ratio. Manning, Raghavan and Schuetze describe logarithmic merging as the standard answer to dynamic indexing in their 2008 textbook, with the bound of $O(\log(T/n))$ merges for each posting.

## References
