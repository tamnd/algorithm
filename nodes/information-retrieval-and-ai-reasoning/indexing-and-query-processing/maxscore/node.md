---
tag: ZNWK20
kind: algorithm
slug: maxscore
name: MaxScore
aliases:
- Turtle-Flood MaxScore
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: advanced
summary: Splits query terms into essential and nonessential by their score upper bounds, and skips documents that only nonessential terms could lift into the top k.
solves: [ranked-retrieval]
model: word-ram
complexity:
  vars: {m: the number of query terms, T: the total length of the m posting lists, k: the number of results}
  time: {worst: "O(T (m log T + log k))"}
  space: {extra: O(m + k)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1995
  people: [Howard Turtle, James Flood]
  note: Turtle and Flood gave the max_score optimization, which uses the largest possible contribution of each term to stop work on documents that cannot reach the top k.
prereqs: [document-at-a-time-evaluation, term-at-a-time-evaluation]
see_also: [wand, block-max-wand, document-at-a-time-evaluation, term-at-a-time-evaluation, threshold-algorithm, no-random-access-algorithm, skip-pointers]
sources:
  - paper: doi:10.1016/0306-4573(95)00020-H
    title: Howard Turtle and James Flood, Query evaluation, strategies and optimizations, Information Processing and Management 31(6), 1995, 831-850
    locator: the max_score optimization for term-at-a-time and document-at-a-time evaluation
  - paper: doi:10.1145/1076034.1076074
    title: Trevor Strohman, Howard Turtle and W. Bruce Croft, Optimization strategies for complex queries, SIGIR 2005
    locator: the document-at-a-time form of max_score and its use for complex queries
  - paper: doi:10.1561/1500000057
    title: Nicola Tonellotto, Craig Macdonald and Iadh Ounis, Efficient query processing for scalable web search, Foundations and Trends in Information Retrieval 12(4-5), 2018, 319-500
    locator: the chapter on dynamic pruning, with the essential and nonessential lists of MaxScore and the safety of the method
---

MaxScore is a dynamic pruning method for [ranked retrieval](/ranked-retrieval/) on a docid-ordered index. It sorts the query terms by their upper bounds $U_i$, the largest weight in each [posting list](/posting-list/), from small to large. When the heap of the best $k$ is full with threshold $\theta$, the longest prefix of terms whose bounds sum to at most $\theta$ is nonessential: a document that contains only these terms cannot enter the top $k$. So the candidates come only from the essential lists, read as in [document-at-a-time evaluation](/document-at-a-time-evaluation/). The nonessential lists are only probed, with forward searches, for the candidates, and the probes stop as soon as the partial score plus the bounds of the terms not yet probed is at most $\theta$. As $\theta$ grows, more terms become nonessential. With exact arithmetic MaxScore is safe: it returns exactly the top $k$ of exhaustive scoring. [WAND](/wand/) uses the same bounds but chooses a pivot again at each step.

## In plain words

Each query word has a best possible contribution. Put the words in order from the weakest to the strongest. Once you have a list of top results, add up the weak words from the bottom. If even all of them together cannot beat the worst current result, then a document that has only weak words can never make the list. So look for candidates only in the lists of the strong words. For each candidate, add the strong words first, and then check the weak words one by one. Stop checking as soon as the candidate cannot win even with the best values of the words that remain.

## The problem

The input is a query of $m$ distinct terms, the posting list of each term in increasing docid order with weights $w \ge 0$, and $k \ge 1$. The score of a document is the sum of the weights of the query terms that it contains, and a document matches if it contains at least one. The output is the $k$ matching documents of highest score, by score descending and then docid ascending. Each list supports next and $\mathit{next\_geq}(d)$, a forward search to the first posting with docid at least $d$, for example with [skip pointers](/skip-pointers/).

## The algorithm

The heap is the one of DAAT: it holds the best $k$ pairs so far and replaces its least entry only on a strictly greater score. While it has fewer than $k$ entries, there is no threshold and every term is essential.

```pseudo id=main
MAXSCORE(q, k)
L1  sort the cursors so that U_1 ≤ U_2 ≤ … ≤ U_m
L2  P_0 ← 0; for i ← 1 to m do P_i ← P_(i-1) + U_i           ▷ prefix sums of the bounds
L3  H ← an empty heap of size k; θ is the least score in H when |H| = k; e ← 0
L4  loop                                 ▷ terms 1..e are nonessential
L5      while |H| = k and e < m and P_(e+1) ≤ θ do e ← e + 1
L6      d ← the least docid of the cursors e+1, …, m
L7      if d = ∞ then return the entries of H, by score descending and then docid ascending
L8      s ← the sum of the weights of the essential cursors at d; move each of them by next
L9      for i ← e down to 1 do
L10         if s + P_i ≤ θ then go to L4 without a score    ▷ d cannot enter the top k
L11         c_i.next_geq(d); if c_i.docid = d then s ← s + its weight
L12     offer (s, d) to H
```

The test in line L10 uses $P_i = U_1 + \cdots + U_i$, the bounds of the nonessential terms that are not yet probed. Line L10 can only be true when $e \ge 1$, so the heap is full and $\theta$ exists. The split $e$ never goes down, since $\theta$ only grows.

## Example

Take the toy collection with BM25 weights ($k_1 = 1.2$, $b = 0.75$, the Lucene IDF with the natural log), q1 "sorted array search" and $k = 2$. Sorted by bound: sorted ($U = 0.9497$), array ($0.98$), search ($1.3291$), with prefix sums $0.9497$, $1.9297$ and $3.2588$. The lists are sorted: d1, d2, d4, d8; array: d1, d2, d8; search: d1, d7.

| candidate | $\theta$ before | nonessential | action |
|---|---|---|---|
| d1 | none | none | full score 3.0283, into the heap |
| d2 | none | none | full score 1.8893, into the heap; now $\theta = 1.8893$ |
| d7 | 1.8893 | sorted | essential part 1.2743; $1.2743 + 0.9497 > \theta$, so probe sorted: no d7; full score 1.2743, rejected |
| d8 | 1.8893 | sorted | essential part 0.9396 (array); $0.9396 + 0.9497 = 1.8893 \le \theta$, so stop |
| none | 1.8893 | sorted | the essential lists are at the end; return |

After d2, $P_1 = 0.9497 \le 1.8893$ makes sorted nonessential, and $P_2 = 1.9297 > 1.8893$ keeps array and search essential. The document d4, which contains only sorted, is never a candidate. MaxScore fully scored 3 of the 5 matching documents and returns d1 3.0283 and d2 1.8893, as DAAT does. For d8, the bound test meets $\theta$ with equality, and the tie rule makes this right: a score of 1.8893 at d8 would lose to d2, which has the smaller docid.

## Correctness

The proof uses three conditions. (1) Each bound $U_i$ is at least every weight of list $i$, and the prefix sums and scores are computed exactly. (2) The heap replaces its least entry only on a strictly greater score, and the candidates come in increasing docid order, so a tie keeps the smaller docid. (3) Each document left out has a score of at most $\theta$. The essential cursors move as in DAAT, so each candidate is the next document of the essential lists, and every essential list that contains it has its cursor on it. The nonessential cursors have never moved past a document after the last candidate, so each probe finds the candidate if and only if the list contains it. A document that is never a candidate is in no essential list at the time the essential cursors pass it, so its score is at most $P_e \le \theta$. A candidate stopped by line L10 has a score at most $s + P_i \le \theta$. In both cases the full heap holds $k$ documents with smaller docids and scores at least $\theta$. The full proof is in the proof file.

## Complexity

The model is the [word RAM](/word-ram/) with the index in memory. Let $T$ be the total length of the $m$ query lists.

- **Worst case.** Each pass through the loop moves at least one essential cursor by one posting, so there are at most $T$ passes. Each pass finds the least essential docid in $O(m)$, does at most $m$ forward searches of $O(\log T)$ each with binary search, and one heap operation of $O(\log k)$. This gives $O(T (m \log T + \log k))$, which is no better than DAAT in the worst case.
- **Documents scored.** At most the number of matching documents; on the toy query 3 of 5.
- **Space.** $O(m + k)$ besides the index.
- **Measured speed.** The speedups of MaxScore over DAAT are measurements, not bounds. The survey of Tonellotto and others (2018) reviews such measurements against WAND and block-max WAND; which method is fastest depends on the query length, $k$ and the collection.

## Properties

- **Safe** under the three conditions, with exact arithmetic or bounds that are rounded up.
- **No re-sorting.** The terms are sorted once by bound, in line L1. WAND sorts the cursors by docid at each step.
- **No random access.** All cursors move forward only; the probes are forward searches, not lookups out of order, unlike the [threshold algorithm](/threshold-algorithm/), which uses random access.
- **Online.** Each scored document is final, and $\theta$ only grows.
- **Needs nonnegative weights**, so that the prefix sums bound the scores.

## Variants and improvements

- **Term-at-a-time form.** The original max_score of Turtle and Flood also has a term-at-a-time form, which stops creating accumulators when the bound of the remaining terms falls below the $k$-th accumulator. It is described on the [term-at-a-time evaluation](/term-at-a-time-evaluation/) page.
- **Block maxes.** The bounds of the nonessential terms in line L10 can be replaced by the block max of the block that holds $d$, as in [block-max WAND](/block-max-wand/), which stops more probes early.
- **Conjunctive queries.** When every term must occur, all lists can be probed in order of length, and the bound test still applies.
- **Initial threshold.** A safe lower bound on the final $\theta$ makes terms nonessential from the start.

## When to use it

Use MaxScore for disjunctive queries with small $k$ on a docid-ordered index, in particular for longer queries, where the sort of WAND at each step costs more and many low-bound terms become nonessential early. With few terms of similar bound, the split helps little, and WAND or block-max WAND may skip more.

## Pitfalls

- **Ascending order of bounds.** The nonessential terms must be the ones with the smallest bounds. A prefix in another order gives a weaker split, and a split that is not a prefix of some order with $P_e \le \theta$ is unsafe.
- **Equal to the threshold.** Line L5 may move a term with $P_{e+1} \le \theta$, and line L10 may stop with $s + P_i \le \theta$, because a tie is lost by the later docid. This is right only because the candidates come in increasing docid order and the heap replaces only on a strictly greater score.
- **Probing past the candidate.** Line L11 must move to the first docid at least $d$. Moving to the next posting after $d$, or reusing a cursor that has already moved past $d$, loses weights.
- **Float sums.** If the prefix sums are rounded down below a computed score, a document can be dropped. Round the bounds up, or use exact weights.

## Implementations

## History

Turtle and Flood (1995) gave the max_score optimization for both term-at-a-time and document-at-a-time evaluation. Strohman, Turtle and Croft (2005) used the document-at-a-time form for complex queries. The split into essential and nonessential lists, with the prefix sums of the sorted bounds, is the form of MaxScore that later studies of dynamic pruning use, for example the survey of Tonellotto, Macdonald and Ounis (2018).

## References
