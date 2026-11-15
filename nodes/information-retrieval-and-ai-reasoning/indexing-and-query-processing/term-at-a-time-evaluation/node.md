---
tag: AQAN27
kind: algorithm
slug: term-at-a-time-evaluation
name: Term-at-a-time evaluation
aliases:
- TAAT
- accumulator-based evaluation
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Reads the posting lists one term after another and adds each term's contribution into a score accumulator per document.
solves: [ranked-retrieval]
model: word-ram
complexity:
  vars: {m: the number of query terms, T: the total length of the m posting lists, k: the number of results}
  time: {expected: "O(T (1 + log k))"}
  space: {extra: O(T)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1995
  people: [Howard Turtle, James Flood]
  note: Turtle and Flood compared term-at-a-time with document-at-a-time evaluation and gave the max_score rule that stops creating accumulators once no new document can reach the top k.
prereqs: [ranked-retrieval, posting-list, hash-table]
see_also: [document-at-a-time-evaluation, maxscore, impact-ordered-index, wand, top-k-selection, vector-space-model, bm25]
sources:
  - paper: doi:10.1016/0306-4573(95)00020-H
    title: Howard Turtle and James Flood, Query evaluation, strategies and optimizations, Information Processing and Management 31(6), 1995, 831-850
    locator: the term-at-a-time strategy with accumulators, its comparison with document-at-a-time evaluation, and the max_score optimization for term-at-a-time evaluation
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 6, Section 6.3.3 (computing vector scores, the accumulators and term-at-a-time scoring) and Chapter 7, Section 7.1 (efficient scoring and ranking)
  - paper: doi:10.1145/237496.237497
    title: Alistair Moffat and Justin Zobel, Self-indexing inverted files for fast text retrieval, ACM Transactions on Information Systems 14(4), 1996, 349-379
    locator: the limit on the number of accumulators with the quit and continue strategies, and the skips that make the continue strategy fast
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 5, query processing for ranked retrieval (term-at-a-time methods and accumulator pruning)
---

Term-at-a-time evaluation, or TAAT, answers a [ranked retrieval](/ranked-retrieval/) query by reading the [posting lists](/posting-list/) of the query terms one after the other. It keeps an accumulator for each document seen so far, a partial score, and adds the weight of each posting into the accumulator of its document. After the last list every accumulator holds a full score, and the best $k$ are selected. It differs from [document-at-a-time evaluation](/document-at-a-time-evaluation/) in the order of the work: DAAT finishes one document before it starts the next and needs only $O(m + k)$ memory, while TAAT finishes one term before it starts the next and needs one accumulator for each matching document. TAAT reads each list in one sequential pass, which suits lists on disk, and it is the natural order for an [impact-ordered index](/impact-ordered-index/).

## In plain words

Make an empty score sheet with a line for each document. Take the first word of the query and walk down its list of documents. For each document on the list, add the word's points to that document's line, and make a new line if the document has none yet. Then do the same with the next word, and so on. After the last word, every line holds the full score of its document, and you pick the best few lines. The sheet can get long: it has a line for every document that contains any query word. A smarter version reads the most valuable words first and, once the leaders are far enough ahead, stops adding new lines and only updates the old ones.

## The problem

The input is a query of $m$ distinct terms, the posting list of each term, and $k \ge 1$. A posting $(d, w)$ gives the weight $w \ge 0$ of the term in document $d$, and each list is in strictly increasing order of $d$. The score $s(q, d)$ is the sum of the weights of the query terms that $d$ contains, and a document matches if it contains at least one of them. The output is the $k$ matching documents of highest score, ranked by score descending and then docid ascending. The upper bound $U_i$ of term $i$ is the largest weight in its list.

## The algorithm

The plain method has five lines. The accumulator map $A$ is a [hash table](/hash-table/), or an array of $N$ numbers when $N$ is small.

```pseudo id=main
TAAT(q, k)                               ▷ q has m terms, each with a posting list
L1  A ← an empty map from docid to score
L2  for i ← 1 to m do
L3      for each posting (d, w) of list i do
L4          if d ∈ A then A[d] ← A[d] + w else A[d] ← w
L5  return the k best entries of A, by score descending and then docid ascending
```

The max_score variant of Turtle and Flood reads the terms in decreasing order of $U_i$. Before term $i$, the remaining bound $R = U_i + \cdots + U_m$ is the most that a document with no accumulator can still score. When the $k$-th largest accumulator is greater than $R$, the method stops creating accumulators and only adds weights to the ones it has.

```pseudo id=maxscore
TAAT-MAXSCORE(q, k)
M1  order the terms so that U_1 ≥ U_2 ≥ … ≥ U_m
M2  A ← an empty map, or_mode ← true
M3  for i ← 1 to m do
M4      R ← U_i + … + U_m; if or_mode and |A| ≥ k and the k-th largest value in A > R then or_mode ← false
M5      if or_mode then for each posting (d, w) of list i do add w to A[d], creating it if needed
M6      else for each d in A in docid order, find d in list i by a forward search, and if found add its weight to A[d]
M7  return the k best entries of A, by score descending and then docid ascending
```

Line M6 uses forward searches in list i, for example with [skip pointers](/skip-pointers/), so it reads only the postings of documents that already have an accumulator.

## Example

Take the toy collection with BM25 weights ($k_1 = 1.2$, $b = 0.75$, the Lucene IDF with the natural log) and the query q1 "sorted array search". The accumulators after each list, rounded to 4 places:

| after list | d1 | d2 | d4 | d7 | d8 |
|---|---|---|---|---|---|
| sorted | 0.7192 | 0.9497 | 0.6896 | | 0.6896 |
| array | 1.6992 | 1.8893 | 0.6896 | | 1.6292 |
| search | 3.0283 | 1.8893 | 0.6896 | 1.2743 | 1.6292 |

Plain TAAT read 9 postings and made 5 accumulators. The top 2 are d1 3.0283 and d2 1.8893, and the top 5 is the same as with DAAT.

The max_score variant with $k = 1$ orders the terms by their bounds: search ($U = 1.3291$), array ($0.98$), sorted ($0.9497$). After search, $A$ = {d1 1.3291, d7 1.2743}. Before array, $R = 0.98 + 0.9497 = 1.9297$, and the best accumulator 1.3291 is not greater, so it reads array in full: $A$ = {d1 2.3091, d2 0.9396, d7 1.2743, d8 0.9396}. Before sorted, $R = 0.9497$ and $2.3091 > 0.9497$, so it switches to AND mode. It looks up d1, d2, d7 and d8 in the list of sorted and finds d1, d2 and d8; it never creates an accumulator for d4. It read 8 postings and made 4 accumulators, and it returns d1 3.0283.

## Correctness

For plain TAAT, after list $i$ each accumulator $A[d]$ is the sum of the weights of terms $1, \ldots, i$ in $d$, and a document has an accumulator if and only if one of these lists contains it. After the last list, $A$ maps each matching document to its exact score, and line L5 selects the top $k$ by the tie rule. For the max_score variant, let the switch happen before term $i$. A document with no accumulator then contains none of the terms $1, \ldots, i-1$, so its final score is at most $R$. The accumulators only grow, so at least $k$ documents end with a score greater than $R$, and the document cannot enter the top $k$. Every document with an accumulator gets all its remaining weights in line M6, so its score is exact. The top $k$ of $A$ is then the top $k$ of all documents. The full proof is in the proof file.

## Complexity

Let $T$ be the total length of the $m$ query lists. The model is the [word RAM](/word-ram/), with the index and the accumulators in memory.

- **Postings read.** Plain TAAT reads exactly $T$ postings, one pass over each list.
- **Accumulators.** One for each matching document, at most $T$. On a large collection this can be a large part of $N$; this is the cost that DAAT avoids.
- **Time.** With a hash table, each update costs $O(1)$ expected, and the selection of the top $k$ from at most $T$ accumulators with a heap costs $O(T \log k)$. The total is $O(T (1 + \log k))$ expected. With an array of $N$ accumulators the updates are $O(1)$ in the worst case, but the array costs $O(N)$ to clear and to scan.
- **The variant.** It makes at most as many accumulators and reads at most as many postings as plain TAAT. In AND mode it does at most $|A|$ forward searches in each later list.
- **On disk.** Each list is read once from start to end, so only one list needs to be in memory at a time.

## Properties

- **Exact.** Both versions return the exact top $k$. The variant uses only the bounds $U_i$, which are true maximums of the lists.
- **Not an online method.** No score is final until the last list has been read, so a threshold test on a whole document, as in WAND, does not apply.
- **Order free.** The plain method gives the same accumulators in any term order, up to the order of the floating-point additions.
- **Memory grows with the matches**, not with $k$.

## Variants and improvements

- **Accumulator limits.** Moffat and Zobel (1996) fix a largest number of accumulators. The quit strategy stops when the limit is reached; the continue strategy then only updates existing accumulators, as line M6 does. Both are approximate, because they stop by a count and not by a score bound, so a document of the true top $k$ can be left out.
- **Impact order.** On an [impact-ordered index](/impact-ordered-index/) the postings with the largest weights come first, and score-at-a-time evaluation can stop with a proven top $k$ or after a fixed budget.
- **Frequency-sorted lists.** Persin, Zobel and Sacks-Davis (1996) sort each list by term frequency and skip postings below thresholds that are set as the query runs.
- **[MaxScore](/maxscore/).** The same bound idea, applied document at a time, is the MaxScore page.

## When to use it

Use TAAT when the lists are on disk and must be read in one pass each, when the index is impact ordered, or when the accumulators fit in memory and the code must stay simple. For a docid-ordered index in memory with small $k$, DAAT with dynamic pruning usually does less work. Crane and others (WSDM 2017) compare the two families by measurement on large collections.

## Pitfalls

- **Missing accumulator.** Line L4 must create the accumulator on the first posting of a document. Reading $A[d]$ before it exists is an error in many languages.
- **Bound from the wrong terms.** In line M4, $R$ must be the sum of the bounds of the terms not yet read, including term $i$. Using only the next term, or leaving out term $i$, can switch too early and lose a document.
- **Greater than, not at least.** The switch needs the $k$-th accumulator strictly greater than $R$. With "at least", a new document could tie the $k$-th one and should win by a smaller docid, but it never gets an accumulator.
- **Selecting by score only.** Line L5 must break ties by docid. A hash table has no docid order, so a selection by score alone returns an arbitrary member of a tie.

## Implementations

## History

Turtle and Flood (1995) described term-at-a-time and document-at-a-time evaluation and the max_score optimizations for both. Moffat and Zobel (1996) made accumulator limits practical with the quit and continue strategies and with skips inside compressed lists, and Persin, Zobel and Sacks-Davis (1996) used frequency-sorted lists with dynamic thresholds. Anh and Moffat later moved to impact-ordered indexes, where term-at-a-time and score-at-a-time evaluation are the natural order.

## References
