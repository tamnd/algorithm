---
tag: F02PAM
kind: algorithm
slug: wand
name: WAND
aliases:
- weak AND
- Broder WAND
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: advanced
summary: Sorts posting cursors by docid and finds a pivot where the summed term upper bounds first exceed the heap threshold, skipping all earlier documents.
solves: [ranked-retrieval]
model: word-ram
complexity:
  vars: {m: the number of query terms, T: the total length of the m posting lists, k: the number of results}
  time: {worst: "O(T m log m)"}
  space: {extra: O(m + k)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 2003
  people: [Andrei Z. Broder, David Carmel, Michael Herscovici, Aya Soffer, Jason Zien]
  note: Broder and others at IBM defined the weak AND operator and the two-level evaluation in which a cheap pivot test on term upper bounds decides which documents get a full score.
prereqs: [document-at-a-time-evaluation, skip-pointers]
see_also: [block-max-wand, maxscore, term-at-a-time-evaluation, threshold-algorithm, fagin-algorithm, no-random-access-algorithm, top-k-query, exponential-search]
sources:
  - paper: doi:10.1145/956863.956944
    title: Andrei Z. Broder, David Carmel, Michael Herscovici, Aya Soffer and Jason Zien, Efficient query evaluation using a two-level retrieval process, CIKM 2003, 426-434
    locator: the WAND operator, the upper bound of each term, the pivot selection over cursors sorted by docid, the threshold from the heap, and the threshold factor F that trades accuracy for speed
  - paper: doi:10.1145/2009916.2010048
    title: Shuai Ding and Torsten Suel, Faster top-k document retrieval using block-max indexes, SIGIR 2011, 993-1002
    locator: the description of WAND as the baseline of block-max WAND
  - paper: doi:10.1561/1500000057
    title: Nicola Tonellotto, Craig Macdonald and Iadh Ounis, Efficient query processing for scalable web search, Foundations and Trends in Information Retrieval 12(4-5), 2018, 319-500
    locator: the chapter on dynamic pruning, with MaxScore, WAND and block-max WAND and their safety
---

WAND is a dynamic pruning method for [ranked retrieval](/ranked-retrieval/) on a docid-ordered index. It works like [document-at-a-time evaluation](/document-at-a-time-evaluation/), but it does not score every matching document. Each query term $i$ has an upper bound $U_i$, the largest weight in its [posting list](/posting-list/). WAND keeps the cursors sorted by their current docid and adds up their bounds in that order. The first cursor at which the sum is greater than the threshold $\theta$, the least score in a full heap of size $k$, is the pivot. No document before the pivot docid can enter the top $k$, so WAND moves cursors forward to the pivot with a forward search and scores a document only when all the cursors before the pivot are on it. With the threshold used as is, WAND is safe: it returns exactly the top $k$ of exhaustive scoring. With a threshold factor $F > 1$ it is faster but unsafe. Compared with [MaxScore](/maxscore/), which splits the terms into two fixed groups, WAND chooses the pivot again at each step. [Block-max WAND](/block-max-wand/) adds a bound for each block of postings.

## In plain words

Each query word has a best possible contribution: the most points it gives to any document. Line up the words by the next document that each one points to. Go down the line and add up the best contributions. As long as the sum is too small to beat the worst of the current top results, no document up to that point can make it. The document where the sum first gets large enough is the pivot. Every document before it can be skipped, so the words behind jump ahead to the pivot. When all the words before the pivot point to it, score it for real. The jumps skip whole runs of documents that a plain scan would score one by one.

## The problem

The input is a query of $m$ distinct terms, the posting list of each term in increasing docid order with weights $w \ge 0$, and $k \ge 1$. The score of a document is the sum of the weights of the query terms that it contains, and a document matches if it contains at least one. The output is the $k$ matching documents of highest score, by score descending and then docid ascending. Each list supports $\mathit{next}$, which moves one posting, and $\mathit{next\_geq}(d)$, which moves to the first posting with docid at least $d$, for example with [skip pointers](/skip-pointers/) or [exponential search](/exponential-search/).

## The algorithm

The heap is the one of DAAT: it holds the best $k$ pairs seen so far, and it replaces its least entry only on a strictly greater score. While it has fewer than $k$ entries, the threshold is $\theta = -\infty$. $F = 1$ gives the safe method.

```pseudo id=main
WAND(q, k, F)                            ▷ F = 1 for the safe method
L1  for i ← 1 to m do c_i ← a cursor on list i, with U_i ← the largest weight in list i
L2  H ← an empty heap of size k; θ is -∞ while |H| < k, else the least score in H
L3  loop
L4      sort the cursors by docid, so that c_1.docid ≤ … ≤ c_m.docid
L5      p ← the least index with c_p.docid < ∞ and U_1 + … + U_p > F θ
L6      if there is no such p then return the entries of H, by score descending and then docid ascending
L7      d ← c_p.docid                    ▷ the pivot
L8      if c_1.docid = d then
L9          s ← the sum of the weights of the cursors at d, in query order; move each of them by next
L10         offer (s, d) to H
L11     else
L12         j ← the largest index < p with c_j.docid < d; c_j.next_geq(d)
```

In line L5, $U_1, \ldots, U_p$ are the bounds of the cursors in their sorted order. Line L12 moves one cursor; Broder and others pick it by a heuristic, and any cursor before the pivot with a docid less than $d$ keeps the method safe. Line L10 is line L8 of DAAT.

## Example

Take the toy collection with BM25 weights ($k_1 = 1.2$, $b = 0.75$, the Lucene IDF with the natural log), q1 "sorted array search" and $k = 2$. The bounds are $U = 0.9497$ for sorted, $0.98$ for array and $1.3291$ for search. The lists are sorted: d1, d2, d4, d8; array: d1, d2, d8; search: d1, d7.

| step | cursors by docid | $\theta$ | pivot | action |
|---|---|---|---|---|
| 1 | sorted 1, array 1, search 1 | $-\infty$ | d1 | score d1 = 3.0283 |
| 2 | sorted 2, array 2, search 7 | $-\infty$ | d2 | score d2 = 1.8893; the heap is full |
| 3 | sorted 4, search 7, array 8 | 1.8893 | search at d7 | move sorted to d7 or later: it lands on d8 |
| 4 | search 7, sorted 8, array 8 | 1.8893 | sorted at d8 | move search to d8 or later: it ends |
| 5 | sorted 8, array 8, search $\infty$ | 1.8893 | array at d8 | score d8 = 1.6292, not greater than 1.8893 |
| 6 | all at $\infty$ | 1.8893 | none | stop |

In step 3 the bound of sorted alone, 0.9497, is not greater than 1.8893, so d4, which contains only sorted, is skipped without a score. In step 4 the bound of search alone, 1.3291, is too small, so d7 is skipped. WAND scored 3 of the 5 matching documents and returns d1 3.0283, d2 1.8893, as DAAT does. With $k = 1$ it scores only d1: after it, $\theta = 3.0283$, a pivot needs all three bounds (sum 3.2588), and two moves of line L12 push array and then search past the end, so no other document gets a score.

Ties: for q2 "posting list merge" with $k = 2$, WAND scores d2, d3 and d4, and then $\theta = 2.2139$, the score of d3. The cursors of posting and merge are at d5 with bounds $0.9396 + 1.2743 = 2.2139$, which is not greater than $\theta$, so d5 is never scored. This is right: d5 ties d3, and the tie rule puts the smaller docid d3 first.

Threshold factor: let list a be d1 1, d2 1 and list b be d2 1, with $k = 1$. The true answer is d2 with score 2. After d1, $\theta = 1$. With $F = 1$ the bound sum 2 at d2 is greater than 1, and WAND finds d2. With $F = 2$ the test is $2 > 2$, which fails, and WAND returns d1, a wrong answer.

## Correctness

The proof needs three conditions. (1) Each bound $U_i$ is at least every weight of list $i$, and the sums in line L5 are at least the scores they bound, in the same arithmetic. (2) The heap replaces its least entry only on a strictly greater score, and documents are scored in increasing docid order, so a tie keeps the smaller docid. (3) Each skipped document has a score of at most $\theta$. For (3): when a cursor moves past a document $y < d$ in line L12, only the cursors before the pivot can still contain $y$, and their bounds sum to at most $\theta$, so $s(y) \le \theta$. At that time the heap holds $k$ documents with scores at least $\theta$ and docids less than $y$, so each of them ranks before $y$, and $y$ is not in the top $k$. The pivots never decrease, so a skipped document is never scored with a missing term, and a scored document gets its exact score. With $F > 1$ the argument gives only $s(y) \le F\theta$, which is not enough. The full proof is in the proof file.

## Complexity

The model is the [word RAM](/word-ram/) with the index in memory. Let $T$ be the total length of the $m$ query lists.

- **Worst case.** Each step moves at least one cursor by at least one posting, so there are at most $T$ steps. Each step sorts $m$ cursors, $O(m \log m)$, or $O(m)$ if one cursor moved and is put back in place. With the heap the time is $O(T m \log m)$, not better than DAAT. When $\theta$ stays low, for example when $k$ is close to the number of matching documents, WAND does all the work of DAAT plus the pivot tests.
- **Documents scored.** At most the number of matching documents, and on the toy query above 3 of 5.
- **Postings read.** At most $T$. A forward search can skip postings that are never decoded, which saves work on compressed lists in blocks.
- **Space.** $O(m + k)$, as DAAT.
- **Measured speed.** The speedups of WAND over exhaustive DAAT are measurements, not bounds. Broder and others measured large reductions in the number of full evaluations on their collection, and later studies such as Ding and Suel (2011) measured the query times of WAND against block-max WAND.

## Properties

- **Safe for $F = 1$** under the three conditions above, with exact or same-order arithmetic.
- **Unsafe for $F > 1$.** The returned documents have their true scores, but a document of the true top $k$ can be skipped.
- **No random access.** WAND only moves cursors forward on each list with next and next_geq. It never looks up a document in a list out of order. This is the difference from the [threshold algorithm](/threshold-algorithm/) of databases, which mixes sorted access with random access, and it puts WAND closer to the [no random access algorithm](/no-random-access-algorithm/). [Fagin's algorithm](/fagin-algorithm/) is the older database method of the same family.
- **Online.** Each scored document is final, and $\theta$ only grows.
- **Needs nonnegative weights.** The prefix sums of line L5 bound the score only if no term can lower it.

## Variants and improvements

- **[Block-max WAND](/block-max-wand/).** Checks the pivot again with the bound of the current block in each list, and skips whole blocks.
- **Threshold factor.** Broder and others multiply $\theta$ by $F \ge 1$ for faster, approximate results. A factor $F < 1$, or a $\theta$ that starts low, makes WAND score more documents, and it stays safe.
- **Initial threshold.** A safe lower bound on the final $\theta$, for example from a previous query, lets pruning start before the heap is full.
- **Choice of the cursor in line L12.** The cursor with the largest bound or the shortest list are common choices. Each choice before the pivot with a smaller docid is safe.
- **[MaxScore](/maxscore/).** Uses the same bounds but a fixed split of the terms, which avoids the sort at each step.

## When to use it

Use WAND for disjunctive queries with small $k$ on a docid-ordered index, when the bounds $U_i$ differ a lot from term to term, so the pivot often lands deep in the list order. For very long queries, the sort in each step costs more, and MaxScore or block-max WAND may be faster. For an index sorted by impact, use score-at-a-time evaluation on an [impact-ordered index](/impact-ordered-index/).

## Pitfalls

- **Float bounds.** If $U_i$ is computed with a different formula or rounding than the weights, or if the prefix sums in line L5 are added in another order than the scores, the computed bound can be a little less than a computed score. Then a document is skipped wrongly. Round the bounds up, or use the same arithmetic.
- **Equal scores.** Line L10 must replace only on a strictly greater score. With "at least", d5 would push d3 out of the heap in the q2 example, against the tie rule.
- **Moving the wrong cursor.** Line L12 must move a cursor with docid less than $d$. Moving a cursor that is already at $d$ to $d$ does nothing, and the loop never ends.
- **Moving past the pivot.** A cursor before the pivot must move to the first docid at least $d$, not greater than $d$, or the pivot document loses a term.
- **Calling WAND with $F > 1$ exact.** It is not; its results must be reported as approximate.

## Implementations

## History

Broder, Carmel, Herscovici, Soffer and Zien presented WAND at CIKM 2003, as the first level of a two-level retrieval process at IBM: the weak AND operator generalizes AND and OR with a threshold, and a cheap test on upper bounds decides which documents get a full evaluation. The idea of score bounds for each term goes back to the max_score optimization of Turtle and Flood (1995). Ding and Suel (2011) added bounds for each block and called the result block-max WAND.

## References
