---
tag: MB0KJQ
kind: algorithm
slug: block-max-wand
name: Block-max WAND
aliases:
- BMW
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: research
summary: Refines WAND with score upper bounds stored per block of postings, so whole blocks are skipped when their local bounds cannot reach the threshold.
solves: [ranked-retrieval]
model: word-ram
complexity:
  vars: {m: the number of query terms, T: the total length of the m posting lists, k: the number of results, b: the block size}
  time: {worst: "O(T m log m)"}
  space: {extra: O(m + k), index: "O(T / b)"}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 2011
  people: [Shuai Ding, Torsten Suel]
  note: Ding and Suel stored the largest weight of each block of a compressed posting list and used these block maxes to check the WAND pivot again and to skip whole blocks.
prereqs: [wand, skip-pointers]
see_also: [wand, maxscore, document-at-a-time-evaluation, term-at-a-time-evaluation, impact-ordered-index, posting-list, threshold-algorithm]
sources:
  - paper: doi:10.1145/2009916.2010048
    title: Shuai Ding and Torsten Suel, Faster top-k document retrieval using block-max indexes, SIGIR 2011, 993-1002
    locator: the block-max index, the block-max WAND algorithm with its shallow moves and block check, and the experiments against WAND
  - paper: doi:10.1145/3077136.3080780
    title: Antonio Mallia, Giuseppe Ottaviano, Elia Porciani, Nicola Tonellotto and Rossano Venturini, Faster BlockMax WAND with variable-sized blocks, SIGIR 2017
    locator: the partition of each posting list into blocks of variable size, chosen so that the block maxes are tight
  - paper: doi:10.1561/1500000057
    title: Nicola Tonellotto, Craig Macdonald and Iadh Ounis, Efficient query processing for scalable web search, Foundations and Trends in Information Retrieval 12(4-5), 2018, 319-500
    locator: the chapter on dynamic pruning, with block-max indexes, block-max WAND and the safety of these methods
---

Block-max WAND is a dynamic pruning method for [ranked retrieval](/ranked-retrieval/) that adds a second, local bound to [WAND](/wand/). Each [posting list](/posting-list/) is cut into blocks of $b$ consecutive postings, and the index stores the last docid and the largest weight of each block, the block max. WAND finds a pivot with the bounds of the whole lists. Block-max WAND then checks the pivot again with the block maxes of the blocks that can hold it. These are usually much smaller than the list bounds, so the check fails often, and then no document from the pivot to the end of the nearest block boundary can enter the top $k$. The cursors jump past that range without a score. With exact arithmetic the method is safe: it returns exactly the top $k$ of exhaustive scoring.

## In plain words

Plain WAND knows only the best contribution of each word over the whole collection. One great document makes that number large for the word, and then WAND cannot skip much. Block-max WAND also keeps the best contribution in each small group of documents in the word's list. When WAND says that a document might make the top results, the method looks at the groups that hold this document. If even the best contributions of those groups cannot beat the current results, it skips to the end of the nearest group without scoring anything in between. Only documents that pass both tests get a full score.

## The problem

The input is a query of $m$ distinct terms, the posting list of each term in increasing docid order with weights $w \ge 0$, and $k \ge 1$. The score of a document is the sum of the weights of the query terms that it contains, and a document matches if it contains at least one. The output is the $k$ matching documents of highest score, by score descending and then docid ascending. Each list $i$ has the bound $U_i$, its largest weight, and is cut into blocks of $b$ postings. Block $j$ of list $i$ stores $\mathit{last}_{ij}$, its last docid, and $\mathit{bmax}_{ij}$, its largest weight.

## The algorithm

Each cursor has a posting position and a block pointer. A shallow move $\mathit{shallow}(d)$ moves the block pointer to the first block with last docid at least $d$, and reads only the block metadata, not the postings. Past the last block the block max is 0 and the last docid is $\infty$. The heap is the one of DAAT, with $\theta = -\infty$ while it has fewer than $k$ entries.

```pseudo id=main
BLOCK-MAX-WAND(q, k)
L1  for i ← 1 to m do c_i ← a cursor on list i, with U_i and the block metadata of list i
L2  H ← an empty heap of size k; θ is -∞ while |H| < k, else the least score in H
L3  loop
L4      sort the cursors by docid, so that c_1.docid ≤ … ≤ c_m.docid
L5      p ← the least index with c_p.docid < ∞ and U_1 + … + U_p > θ
L6      if there is no such p then return the entries of H, by score descending and then docid ascending
L7      d ← c_p.docid                    ▷ the pivot
L8      while p < m and c_(p+1).docid = d do p ← p + 1
L9      for i ← 1 to p do c_i.shallow(d); B ← the sum of the block maxes of c_1, …, c_p
L10     if B > θ then
L11         if c_1.docid = d then s ← the sum of the weights of the cursors at d; move each of them by next
L12             offer (s, d) to H
L13         else j ← the largest index ≤ p with c_j.docid < d; c_j.next_geq(d)
L14     else                             ▷ no document in [d, n) can enter the top k
L15         n ← 1 + the least last docid of the blocks of c_1, …, c_p; if p < m then n ← min(n, c_(p+1).docid)
L16         for i ← 1 to p do c_i.next_geq(n)
```

Line L8 extends the prefix over all the cursors at the pivot. This makes the check in line L9 use every list that can hold $d$, and it makes $n > d$ in line L15, so the loop always moves on. Line L16 moves all the cursors of the prefix. Many implementations move only one of them, for example the one with the largest bound, and both choices are safe.

## Example

Take the toy collection with BM25 weights ($k_1 = 1.2$, $b = 0.75$ in the BM25 formula, the Lucene IDF with the natural log), q1 "sorted array search", $k = 2$, and blocks of 2 postings. The lists and blocks are:

| term | postings | blocks (last docid, block max) | $U$ |
|---|---|---|---|
| sorted | d1 0.7192, d2 0.9497, d4 0.6896, d8 0.6896 | (d2, 0.9497), (d8, 0.6896) | 0.9497 |
| array | d1 0.98, d2 0.9396, d8 0.9396 | (d2, 0.98), (d8, 0.9396) | 0.98 |
| search | d1 1.3291, d7 1.2743 | (d7, 1.3291) | 1.3291 |

| step | cursors by docid | $\theta$ | pivot, prefix | $B$ | action |
|---|---|---|---|---|---|
| 1 | sorted 1, array 1, search 1 | $-\infty$ | d1, all three | 3.2588 | score d1 = 3.0283 |
| 2 | sorted 2, array 2, search 7 | $-\infty$ | d2, sorted and array | 1.9297 | score d2 = 1.8893 |
| 3 | sorted 4, search 7, array 8 | 1.8893 | d7, sorted and search | 2.0187 | move sorted to d7 or later: d8 |
| 4 | search 7, sorted 8, array 8 | 1.8893 | d8, all three | 1.6292 | skip: all move to d9 or later |
| 5 | all at $\infty$ | 1.8893 | none | | stop |

In step 3 the block of sorted that can hold d7 is its second block, with block max 0.6896, and $0.6896 + 1.3291 = 2.0187 > 1.8893$, so the pivot passes. In step 4 search has no block with last docid at least d8, so its block max is 0, and $0 + 0.6896 + 0.9396 = 1.6292$ is not greater than $\theta$. All three cursors jump to d9, which ends all lists. Block-max WAND scored 2 documents; WAND scores 3 on the same query, since it scores d8. Both return d1 3.0283 and d2 1.8893.

A case where the block maxes matter more: list a is d1 9, d2 1, d3 1, d4 1, d5 1 and list b is d1 1, d3 2, d4 2, d5 2, with $k = 1$ and $b = 2$. After d1, $\theta = 10$, and the list bounds $9 + 2 = 11$ pass every pivot. WAND scores d1, d3, d4 and d5. Block-max WAND sees block sums of 3 at d3, d4 and d5 and skips them all; it scores only d1.

## Correctness

The proof uses the three conditions of WAND. (1) Each list bound and each block max is at least every weight that it bounds, and the sums are computed exactly. (2) The heap replaces its least entry only on a strictly greater score, and the documents are scored in increasing docid order, so a tie keeps the smaller docid. (3) Each skipped document has a score of at most $\theta$. Steps that pass line L10 are WAND steps, and a document skipped there is covered by the WAND argument. For a block skip in line L16, take a document $x$ with $d \le x < n$. Lists after the prefix have their cursors at $n$ or later, and no cursor has passed $x$, so $x$ can only be in lists of the prefix. In each of them, $x$ is at most the last docid of the current block and at least $d$, so it lies in the current block, and its weight is at most that block max. So $s(x) \le B \le \theta$. After a skip all the cursors are at $n$ or later, so the pivots never go back, and every scored document gets its exact score. The full proof is in the proof file.

## Complexity

The model is the [word RAM](/word-ram/) with the index in memory. Let $T$ be the total length of the $m$ query lists and $b$ the block size.

- **Worst case.** Each step moves at least one cursor past at least one posting, so there are at most $T$ steps, each with a sort of $m$ cursors and at most $m$ shallow moves. This is $O(T m \log m)$, not better than WAND or DAAT.
- **Documents scored.** At most as many as WAND on the same input, in practice, but this is not a theorem for each query: the two methods visit different pivots and can raise $\theta$ in a different order.
- **Index space.** Two numbers for each block, $O(T / b)$ for the query lists. Small blocks give tight bounds and more metadata.
- **Measured speed.** The speedups of block-max WAND over WAND are measurements on large collections, not bounds. Ding and Suel (2011) reported them in their experiments, and they depend on the block size, the query length and $k$.

## Properties

- **Safe** under the three conditions, with exact arithmetic or bounds that are rounded up.
- **Two-level bounds.** The list bound picks the pivot; the block maxes confirm or reject it.
- **No random access.** As WAND, it moves cursors only forward, with next, next_geq and shallow moves.
- **Online.** Each scored document is final, and $\theta$ only grows.
- **Block maxes depend on the scoring function.** They are computed at index time, so a change of the weights or of BM25 parameters needs new block maxes.

## Variants and improvements

- **Variable-sized blocks.** Mallia and others (2017) cut each list into blocks of different sizes, chosen so that the block maxes are close to the weights inside the blocks.
- **Moving one cursor.** On a failed block check, move only one cursor of the prefix to $n$. This page moves all of them; both are safe.
- **Block maxes with MaxScore.** The same block maxes can tighten the bounds of the nonessential lists in [MaxScore](/maxscore/).
- **Approximate versions.** Multiplying $\theta$ by a factor $F > 1$ in lines L5 and L10 makes the method faster and unsafe, as in WAND.

## When to use it

Use block-max WAND for disjunctive queries with small $k$ on a large docid-ordered index in memory, where the weights in a list vary a lot, so the list bound is loose and the block maxes are tight. It needs block metadata in the index, which most block-compressed indexes can store next to their skip data. For very small collections, or when $k$ is close to the number of matching documents, plain DAAT is simpler and does about the same work.

## Pitfalls

- **Stale block pointer.** The block check must use the block that can hold the pivot, after a shallow move to $d$. Using the block of the cursor's current posting gives a wrong bound for cursors before $d$.
- **No extension in line L8.** If a cursor at $d$ after the pivot is left out of the prefix, its weight is missing from $B$, and $n$ can equal $d$, so the loop does not move.
- **Jumping too far.** In line L15, $n$ must be at most the docid of the next cursor after the prefix. A jump past it would skip documents in lists that the block check did not bound.
- **Float bounds.** Block maxes computed with other rounding than the weights can be a little too small. Round them up, or use exact weights.
- **Strict test.** Line L10 must test $B > \theta$, and line L12 must replace only on a strictly greater score, as in WAND.

## Implementations

## History

Ding and Suel presented block-max indexes and block-max WAND at SIGIR 2011. They built on [WAND](/wand/) of Broder and others (2003), which uses one bound for each list, and on compressed indexes in blocks, which already store the last docid of each block for skips. Mallia, Ottaviano, Porciani, Tonellotto and Venturini (2017) made the blocks variable in size to tighten the bounds.

## References
