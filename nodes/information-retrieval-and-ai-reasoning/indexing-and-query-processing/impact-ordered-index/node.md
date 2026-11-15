---
tag: BBYS9T
kind: data-structure
slug: impact-ordered-index
name: Impact-ordered index
aliases:
- score-at-a-time index
- impact-sorted postings
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: advanced
summary: Sorts each posting list by precomputed impact scores, so query evaluation reads the highest impacts first and can stop early.
model: word-ram
complexity:
  vars: {n: the number of postings in the index, T: the total length of the query lists, k: the number of results, S: the number of segments of the query lists}
  time: {build: O(n log n), query: "O(T (1 + log k))", query_with_safe_stop: "O(S T log k)"}
  space: {total: Θ(n), extra: O(T)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [posting-list, term-at-a-time-evaluation, ranked-retrieval]
see_also: [term-at-a-time-evaluation, document-at-a-time-evaluation, wand, block-max-wand, tiered-index, static-index-pruning, scalar-quantization, inverted-index]
sources:
  - paper: doi:10.1145/1148170.1148235
    title: Vo Ngoc Anh and Alistair Moffat, Pruned query evaluation using pre-computed impacts, SIGIR 2006
    locator: the impact-ordered index with integer impacts in segments, score-at-a-time evaluation, and the stop rules that end the evaluation early
  - paper: doi:10.1145/2808194.2809477
    title: Jimmy Lin and Andrew Trotman, Anytime ranking for impact-ordered indexes, ICTIR 2015
    locator: score-at-a-time evaluation with a fixed budget of postings, so that the query time has a bound
  - paper: doi:10.1145/3018661.3018726
    title: Matt Crane, J. Shane Culpepper, Jimmy Lin, Joel Mackenzie and Andrew Trotman, A comparison of document-at-a-time and score-at-a-time query evaluation, WSDM 2017
    locator: the experiments that compare score-at-a-time evaluation on an impact-ordered index with WAND and block-max WAND on a docid-ordered index
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 7, Section 7.1.5 (impact ordering)
---

An impact-ordered index is an [inverted index](/inverted-index/) in which each [posting list](/posting-list/) is sorted by the contribution of the term to the score, its impact, and not by docid. The impacts are computed at index time, for example from BM25, and are usually small integers. The postings of one term with the same impact form a segment, with the docids of the segment in increasing order, and the segments come in decreasing order of impact. A query is evaluated score at a time: the method reads the segments of all the query terms in one global order of decreasing impact and adds each impact into an accumulator for its document, as in [term-at-a-time evaluation](/term-at-a-time-evaluation/). The most useful postings come first, so the method can stop early. A stop with a proof that the top $k$ and its order cannot change is safe for the impact scores; a stop after a fixed budget of postings is approximate.

## In plain words

In a normal index, each word has a list of documents in number order. Here each word has its documents grouped by how much the word counts in them, with the strongest group first. To answer a query, take the strongest group among all the query words, give its documents their points, then take the next strongest group, and so on. The leaders get most of their points early. You can stop when you can show that the rest of the groups are too weak to change the order of the leaders. Or you can stop when your time is up, and accept that the answer may be a little wrong.

## The abstract type

An impact-ordered index holds, for each term $t$, a sequence of segments $(a_1, D_1), (a_2, D_2), \ldots$ with integer impacts $a_1 > a_2 > \cdots \ge 1$ and disjoint sets of docids $D_j$. The term has impact $a_j$ in each document of $D_j$ and does not occur in other documents. The impact score of a document $x$ for a query $q$ of $m$ distinct terms is the sum of the impacts of the query terms in $x$. The operations are:

- **build** from a docid-ordered index with weights, with a rule that maps each weight to an impact;
- **segments**$(t)$, which gives the segments of $t$ in decreasing order of impact;
- **query**$(q, k)$, which returns the $k$ documents of highest impact score, by score descending and then docid ascending, with one of three stop rules.

## Representation

Each list is a sequence of segments. A segment stores its impact once and then its docids, sorted and usually compressed as gaps. The dictionary entry of a term points to its first segment and stores the number of segments. If the weights are real numbers, a quantizer maps them to integers in $1, \ldots, L$; this page uses the uniform rule $a = 1 + \lfloor (L - 1) w / W \rfloor$, where $W$ is the largest weight in the index. This is a form of [scalar quantization](/scalar-quantization/). The quantized ranking is an approximation of the ranking by the real weights: documents with close weights can get the same impact, and a tie of impacts can change the order.

## Operations

The query reads the segments of all query terms in one global order and keeps a map $A$ from docid to accumulator. For the safe stop, let $r$ be the sum, over the query terms, of the impact of the next unread segment of each term, or 0 for a term with none left. No document can still gain more than $r$.

```pseudo id=main
SAAT(q, k, stop)
L1  G ← the segments of the query terms, sorted by impact descending, then by query position
L2  A ← an empty map from docid to score
L3  for each segment (a, D) in G do
L4      if stop = safe and the top k of A and its order are fixed for the gain r then break
L5      for each docid x in D do                ▷ with stop = budget, break after the budget of postings
L6          A[x] ← A[x] + a, creating A[x] with 0 if needed
L7  return the k best entries of A, by score descending and then docid ascending
```

The test of line L4 needs $|A| \ge k$. Let $a_1 \ge a_2 \ge \cdots$ be the sorted accumulators. The top $k$ and its order are fixed if $a_i > a_{i+1} + r$ for each $i < k$, and $a_k > \max(a_{k+1}, 0) + r$, where $a_{k+1} = 0$ if there are only $k$ entries. The last part also covers the documents with no accumulator yet, which can still reach at most $r$.

The three stop rules are:

- **none** reads every segment. It is exact for the impact scores.
- **safe** stops at line L4. The returned docids and their order are exactly those of **none**, but the scores are lower bounds of the true impact scores, since some postings of the top $k$ may be unread.
- **budget** stops after a fixed number of postings. It is approximate: each returned score is at most the true impact score, and the returned set can differ from the true top $k$.

## Example

Take the toy collection with BM25 weights ($k_1 = 1.2$, $b = 0.75$, the Lucene IDF with the natural log) and $L = 8$ levels. The largest weight is $W = 1.8592$, for the term binary. The query q1 "sorted array search" gives the lists:

| term | segments |
|---|---|
| sorted | impact 4: d2; impact 3: d1, d4, d8 |
| array | impact 4: d1, d2, d8 |
| search | impact 6: d1; impact 5: d7 |

The global order of the segments, and the accumulators after each one:

| segment | d1 | d2 | d4 | d7 | d8 |
|---|---|---|---|---|---|
| search 6 | 6 | | | | |
| search 5 | 6 | | | 5 | |
| sorted 4 | 6 | 4 | | 5 | |
| array 4 | 10 | 8 | | 5 | 4 |
| sorted 3 | 13 | 8 | 3 | 5 | 7 |

The full evaluation gives d1 13, d2 8, d8 7, d7 5, d4 3, the same order as BM25. With a budget of 4 postings and $k = 2$, the method stops after search 6, search 5, sorted 4 and the first posting of array 4, and returns d1 10 and d7 5: d7 is in the second place, while the true second is d2. With $L = 4$ levels, d3, d4 and d5 all get the impact score 5 for q2 "posting list merge", so the top 1 becomes d3 by the docid rule, though d4 has the best BM25 score. This is an effect of the quantization.

On the toy queries the safe stop does not save postings. An example where it does: term a has impact 9 in d1 and impact 1 in d2 and d3, term b has impact 8 in d1 and impact 2 in d4, and $k = 1$. After the two first segments, d1 has 17 and $r = 1 + 2 = 3$, so $17 > 0 + 3$ and the method stops after 2 of 5 postings with d1.

## Correctness

Each document gets exactly one impact from each query term that it contains, since the segments of a term are disjoint. With stop none, line L6 is executed once for each posting, so at the end each accumulator is the impact score of its document, and line L7 selects the top $k$ by the tie rule. For the safe stop, at the time of the break each unread posting of term $t$ has an impact at most the next unread impact of $t$, so each document gains at most $r$ more. The gaps of more than $r$ in line L4 then keep the order of the top $k$ among themselves, and keep each of them before every other document, including the documents without an accumulator. So the docids and their order are those of the full run, while the scores are partial sums. The budget stop has no such guarantee; it only gives partial sums. The full proof is in the proof file.

## Complexity

The model is the [word RAM](/word-ram/). Let $n$ be the number of postings in the index and $T$ the total length of the query lists.

- **Build.** Sorting each list by impact costs $O(n \log n)$ in total, or $O(n + L)$ for each list with a bucket for each impact level.
- **Full query.** $T$ accumulator updates, $O(1)$ expected each with a hash table or $O(1)$ with an array of $N$ accumulators, plus $O(T \log k)$ to select the top $k$.
- **Safe stop.** The check in line L4 is done before each of the $S$ segments. Done by selecting the best $k+1$ accumulators, it costs $O(T \log k)$ each time, so $O(S T \log k)$ in the worst case. Practical systems check less often or keep the leaders in a small structure.
- **Budget stop.** At most the budget of postings, so the query time has a bound that does not depend on the list lengths.
- **Space.** $\Theta(n)$ for the index and $O(T)$ for the accumulators.

## Variants

- **Docid order.** A docid-ordered index supports [document-at-a-time evaluation](/document-at-a-time-evaluation/) with [WAND](/wand/) or [block-max WAND](/block-max-wand/). An impact-ordered index gives up the docid order, so these methods do not apply.
- **Frequency-sorted lists.** Persin, Zobel and Sacks-Davis (1996) sorted each list by term frequency, an earlier form of the same idea, and skipped postings below thresholds set during the query.
- **Phases of Anh and Moffat.** Anh and Moffat (2006) process the segments in impact order and use the bounds to stop creating new accumulators and then to stop the evaluation.
- **Anytime ranking.** Lin and Trotman (2015) stop after a fixed number of postings, so that the query time has a bound, and accept an approximate answer.
- **Tiers.** A [tiered index](/tiered-index/) cuts each list into a few coarse tiers by weight; this is a coarse impact order.

## When to use it

Use an impact-ordered index when the query time must have a fixed bound, as in anytime ranking, or when long queries make the many cursors of DAAT costly. It needs integer impacts fixed at index time, so the scoring function cannot change at query time without a rebuild. Crane and others (WSDM 2017) compared score-at-a-time evaluation with WAND and block-max WAND on the same collections; the results are measurements, and which method is faster depends on the query length, $k$ and the collection.

## Pitfalls

- **Quantization is not free.** Too few levels make ties, and a tie can change the ranking. The exact result of score-at-a-time evaluation is exact for the impacts, not for the real weights.
- **Wrong bound for the gain.** The value $r$ must use the next unread impact of every query term, not only of the current one, and must count a term once even when it has many unread segments, since a document is in at most one segment of each term.
- **Ties at the stop.** The gaps in line L4 must be strictly greater than $r$. A gap equal to $r$ can close, and then the docid rule decides, which the partial scores do not show.
- **Reporting partial scores.** After a safe stop, the scores are lower bounds. Code that uses them as the true scores, for example to merge with another shard, gets them wrong.
- **Budget results called exact.** With a budget stop the result is approximate and must be reported so.

## Implementations

## History

Persin, Zobel and Sacks-Davis (1996) used frequency-sorted indexes for filtered retrieval. Anh and Moffat developed impact-ordered indexes with integer impacts, and in 2006 they gave pruned score-at-a-time evaluation with early stopping. Lin and Trotman (2015) gave anytime ranking with a fixed budget of postings in the JASS system, and Crane and others (2017) compared score-at-a-time and document-at-a-time evaluation by experiments.

## References
