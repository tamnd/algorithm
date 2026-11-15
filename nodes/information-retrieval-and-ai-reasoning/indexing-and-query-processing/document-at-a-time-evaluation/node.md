---
tag: CR25E3
kind: algorithm
slug: document-at-a-time-evaluation
name: Document-at-a-time evaluation
aliases:
- DAAT
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Reads all query posting lists in parallel in docid order and scores each document fully before moving on, keeping a heap of the best k.
solves: [ranked-retrieval]
model: word-ram
complexity:
  vars: {m: the number of query terms, T: the total length of the m posting lists, k: the number of results}
  time: {worst: "O(T (m + log k))", with_cursor_heap: "O(T (log m + log k))"}
  space: {extra: O(m + k)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1995
  people: [Howard Turtle, James Flood]
  note: Turtle and Flood described and compared the document-at-a-time and term-at-a-time strategies for ranked queries, and an optimization of each that skips work by score bounds.
prereqs: [ranked-retrieval, posting-list, priority-queue]
see_also: [term-at-a-time-evaluation, wand, maxscore, block-max-wand, k-way-merge, merge-based-list-intersection, top-k-selection, threshold-algorithm]
sources:
  - paper: doi:10.1016/0306-4573(95)00020-H
    title: Howard Turtle and James Flood, Query evaluation, strategies and optimizations, Information Processing and Management 31(6), 1995, 831-850
    locator: the term-at-a-time and document-at-a-time evaluation strategies and their cost, and the max_score optimization for each
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 6, Section 6.3.3 (computing vector scores with accumulators) and Chapter 7, Section 7.1 (efficient scoring and ranking, with the heap for the top k)
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 5, query processing for ranked retrieval (document-at-a-time and term-at-a-time methods)
  - paper: doi:10.1561/1500000057
    title: Nicola Tonellotto, Craig Macdonald and Iadh Ounis, Efficient query processing for scalable web search, Foundations and Trends in Information Retrieval 12(4-5), 2018, 319-500
    locator: the chapter on query processing, with document-at-a-time and term-at-a-time traversal and the dynamic pruning methods built on them
---

Document-at-a-time evaluation, or DAAT, answers a [ranked retrieval](/ranked-retrieval/) query from an inverted index. It opens one cursor on the [posting list](/posting-list/) of each query term and moves all cursors forward together in increasing document id order. At each step it takes the smallest document id under any cursor, adds the weights of all terms whose cursor is at that id, and so finishes the score of that document before it looks at the next one. A min-heap of size $k$ keeps the best $k$ documents seen so far. DAAT reads every posting of every query list and scores every matching document, so it is the baseline that the dynamic pruning methods [WAND](/wand/), [MaxScore](/maxscore/) and [block-max WAND](/block-max-wand/) improve on. The other basic strategy is [term-at-a-time evaluation](/term-at-a-time-evaluation/), which reads one whole list after the other and keeps a partial score for each document.

## In plain words

Each word of the query has a list of the documents that contain it, sorted by document number. Put a finger on the first entry of each list. The smallest number under your fingers is the next document to look at. Add up what each word that has this document gives to its score, move those fingers one step, and the document is done: its score is final. Keep a short table of the best few documents seen so far. A new document goes into the table only if it is better than the worst one there. When all fingers fall off their lists, the table holds the answer. The work grows with the total length of the lists, and only a few numbers are kept in memory at any time.

## The problem

The input is a query of $m$ distinct terms, the posting list of each term, and a number $k \ge 1$. A posting is a pair $(d, w)$ of a document id $d$ and a weight $w \ge 0$, the contribution of the term to the score of $d$, for example a [BM25](/bm25/) term weight. Each list is in strictly increasing order of $d$. The score $s(q, d)$ is the sum of the weights of the query terms that $d$ contains. A document matches if it contains at least one query term. The output is the $k$ matching documents of highest score, or all of them if fewer than $k$ match, ranked by score descending and then by document id ascending. This is the tie rule of this area. A term with no posting list has an empty list.

## The algorithm

Each cursor $c_i$ points into list $i$. It reports $c_i.\mathit{docid}$, which is $\infty$ when the cursor is past the end, and $c_i.\mathit{weight}$, and it moves with $c_i.\mathit{next}$.

```pseudo id=main
DAAT(q, k)                               ▷ q has m terms, each with a sorted list
L1  for i ← 1 to m do c_i ← a cursor at the start of list i
L2  H ← an empty min-heap of (score, docid) pairs
L3  d ← min over i of c_i.docid
L4  while d < ∞ do
L5      s ← 0
L6      for i ← 1 to m do
L7          if c_i.docid = d then s ← s + c_i.weight, c_i.next()
L8      if |H| < k then insert (s, d) into H
        else if s > the least score in H then replace the least entry of H by (s, d)
L9      d ← min over i of c_i.docid
L10 return the entries of H, by score descending and then docid ascending
```

The heap orders its entries by score and, among equal scores, puts the larger docid lower, so its least entry is the one that the tie rule ranks last. Line L8 replaces it only on a strictly greater score. Line L7 adds the weights in query order, the same order as an exhaustive scan, so with floating-point weights the scores agree to the last bit.

## Example

Take the toy collection of this area with BM25 weights ($k_1 = 1.2$, $b = 0.75$, the Lucene IDF $\ln(1 + (N - \mathrm{df} + 0.5)/(\mathrm{df} + 0.5))$, $N = 8$, $\mathrm{avgdl} = 9.875$), the query q1 "sorted array search" and $k = 2$. The lists are, with weights rounded to 4 places:

- sorted: d1 0.7192, d2 0.9497, d4 0.6896, d8 0.6896
- array: d1 0.98, d2 0.9396, d8 0.9396
- search: d1 1.3291, d7 1.2743

| step | $d$ | terms at $d$ | $s$ | line L8 | $H$ after |
|---|---|---|---|---|---|
| 1 | 1 | sorted, array, search | 3.0283 | insert | d1 3.0283 |
| 2 | 2 | sorted, array | 1.8893 | insert | d1 3.0283, d2 1.8893 |
| 3 | 4 | sorted | 0.6896 | not greater than 1.8893 | unchanged |
| 4 | 7 | search | 1.2743 | not greater than 1.8893 | unchanged |
| 5 | 8 | sorted, array | 1.6292 | not greater than 1.8893 | unchanged |

After step 5 every cursor is at $\infty$. The answer is d1 3.0283, d2 1.8893. DAAT read all 9 postings and scored all 5 matching documents. For $k = 5$ it returns d1, d2, d8, d7, d4 with the scores 3.0283, 1.8893, 1.6292, 1.2743, 0.6896, the same as scoring every document. For q2 "posting list merge", d3 and d5 both score 2.2139; d3 comes first in docid order and enters the heap first, and d5 cannot push it out, so the ranking is d4, d3, d5, as the tie rule asks.

## Correctness

Before each test of line L4, two facts hold. First, each cursor $c_i$ is at the first posting of list $i$ with docid at least $d$, and $d$ is the least docid under any cursor; so each matching document less than $d$ has been scored, and no document between two consecutive values of $d$ matches. Second, each scored document got its exact score, because when $d$ is processed every list that contains $d$ has its cursor on $d$. The heap rule keeps the top $k$ of the documents scored so far by the tie rule: documents arrive in increasing docid order, so a new document with a score equal to the least score in $H$ has a larger docid than every entry and ranks below them all, and line L8 is right to keep it out. When the loop ends every matching document has been scored, so $H$ is the top $k$. The full proof is in the proof file.

## Complexity

Let $T$ be the total length of the $m$ query lists, and let the cost model be the [word RAM](/word-ram/) with an in-memory index.

- **Postings read.** Exactly $T$. Each posting is read once in line L7, and each iteration of line L4 reads at least one.
- **Documents scored.** Exactly the number of matching documents, which is at most $T$. DAAT has no way to skip a document.
- **Time.** Lines L3, L6 and L9 scan the $m$ cursors, so each iteration costs $O(m)$, and the heap costs $O(\log k)$. With at most $T$ iterations the time is $O(T (m + \log k))$. With the cursors in a second heap keyed by docid, the minimum costs $O(\log m)$ for each posting, and the time is $O(T (\log m + \log k))$.
- **Space.** $O(m + k)$ besides the index: one cursor for each term and the heap. This is the main advantage over term-at-a-time evaluation, which keeps one accumulator for each matching document.
- **On disk.** The lists are read in order, but $m$ of them at once, so each list needs its own read buffer.

## Properties

- **Exact.** It returns the same top $k$, scores and order as scoring every document, for any nonnegative or even negative weights, since it never uses a bound.
- **Small memory.** Only the cursors and the heap, independent of the number of matching documents.
- **Each score is final when computed.** This allows the threshold tests of WAND and MaxScore, which compare a bound on a whole document with the least score in the heap.
- **Sequential access only.** Each list is read from left to right, which suits compressed lists that decode in order.

## Variants and improvements

- **Boolean AND.** Score $d$ only if all $m$ cursors are at $d$, and move the others to $d$ with a forward search. This is a [k-way](/k-way-merge/) form of [list intersection](/posting-list-intersection/).
- **[MaxScore](/maxscore/).** Splits the terms by their upper bounds and never starts a document from the lists of terms that cannot lift it into the top $k$ alone.
- **[WAND](/wand/).** Keeps the cursors sorted by docid and jumps to the first document whose summed term upper bounds exceed the threshold.
- **[Block-max WAND](/block-max-wand/).** Adds an upper bound for each block of postings, so it skips whole blocks.
- **Cursor heap.** A heap of cursors replaces the linear scan for long queries.
- **Score-at-a-time.** An [impact-ordered index](/impact-ordered-index/) gives up docid order, and with it the DAAT structure.

## When to use it

Use DAAT when the index is in docid order and memory for accumulators is short, or as the base of a dynamic pruning method. Plain DAAT is the right choice for short lists or when $k$ is close to the number of matching documents, since then no pruning method can skip much. For long lists and small $k$, use WAND, block-max WAND or MaxScore on the same index.

## Pitfalls

- **Replacing on equal scores.** If line L8 used "at least" in place of "greater than", d5 would push out d3 in q2 with $k = 2$, and the result would break the tie rule.
- **Forgetting to advance.** Each cursor that is at $d$ must move in line L7. A cursor left behind makes line L9 return $d$ again and the loop never ends.
- **Different summation order.** With floats, adding the weights in cursor order and not in query order can change the last bit of a score, and then a tie may break the other way than in the exhaustive scan.
- **Missing terms.** A term with no list must give a cursor at $\infty$, not an error.

## Implementations

## History

Turtle and Flood (1995) named and compared the two classic evaluation strategies, term-at-a-time and document-at-a-time, and gave a max_score optimization for each. Moffat and Zobel (1996) studied the term-at-a-time side with limited accumulators and skips. Broder and others (2003) built WAND on the document-at-a-time strategy, and most later dynamic pruning methods, such as block-max WAND (Ding and Suel 2011), also process one document at a time.

## References
