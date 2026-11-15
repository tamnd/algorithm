---
tag: J6839A
kind: data-structure
slug: tiered-index
name: Tiered index
aliases:
- champion lists
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Splits each posting list into tiers by score, and reads lower tiers only when the higher tiers give fewer than k results.
model: word-ram
complexity:
  vars: {n: the number of postings in the index, r: the number of weight thresholds, m: the number of query terms, T: the total length of the query lists, k: the number of results}
  time: {build: O(n log r), query: "O(T m + r T log k) expected"}
  space: {total: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [posting-list, ranked-retrieval]
see_also: [impact-ordered-index, static-index-pruning, threshold-algorithm, fagin-algorithm, term-at-a-time-evaluation, document-at-a-time-evaluation, inverted-index, index-partitioning]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 7, Section 7.1.3 (champion lists) and Section 7.2.1 (tiered indexes, as a generalization of champion lists, with the rule that falls back to the next tier when fewer than k documents are found)
  - paper: doi:10.1109/LAWEB.2003.1250291
    title: Knut Magne Risvik, Yngve Aasheim and Mathias Lidal, Multi-tier architecture for web search engines, LA-WEB 2003
    locator: the split of a web index into tiers of documents, with a query sent to the lower tiers only when the higher tiers do not give a good enough answer
  - paper: doi:10.1561/1500000057
    title: Nicola Tonellotto, Craig Macdonald and Iadh Ounis, Efficient query processing for scalable web search, Foundations and Trends in Information Retrieval 12(4-5), 2018, 319-500
    locator: the parts on tiering and on early termination of query processing
---

A tiered index is an [inverted index](/inverted-index/) in which each [posting list](/posting-list/) is cut into a few tiers by the weight of the term in the document. With thresholds $\tau_1 > \tau_2 > \cdots > \tau_r > 0$, tier 1 holds the postings with weight at least $\tau_1$, tier $j$ the postings with weight from $\tau_j$ up to but not including $\tau_{j-1}$, and tier $r+1$ the rest. A query reads tier 1 of all its terms, then tier 2, and so on, and computes the full score of each new document. The approximate rule of Manning, Raghavan and Schuetze stops as soon as at least $k$ documents are found. A safe rule stops after tier $j$ only when the $k$-th best full score is at least $m \tau_j$, where $m$ is the number of query terms; every unseen document has a score strictly below this bound. The approximate rule is fast and can miss documents; the safe rule returns exactly the top $k$ of exhaustive scoring.

## In plain words

Put the best postings of each word on a short list, the next best on a second list, and the rest on a third. To answer a query, read the short lists first and compute the real score of every document that you find there. If that gives enough good results, stop. Otherwise read the second lists, and so on. The quick version stops as soon as it has enough results, and it can miss a document that is good in many words but best in none. The careful version also checks that the results it has beat anything that could still be hiding in the lists not yet read.

## The abstract type

A tiered index over a docid-ordered index with weights $w \ge 0$ holds, for each term $t$ and each tier $j \in \{1, \ldots, r+1\}$, the sorted list of docids $x$ whose weight of $t$ falls in tier $j$. Each posting is in exactly one tier. The index also keeps random access to the weight of $t$ in $x$, for example a hash table or the docid-ordered lists. The score of a document for a query of $m$ distinct terms is the sum of the weights of the query terms in it. The operations are:

- **build**$(\tau_1, \ldots, \tau_r)$ from the docid-ordered index;
- **tier**$(t, j)$, the docids of tier $j$ of term $t$;
- **query**$(q, k)$, which returns $k$ documents with their full scores, by score descending and then docid ascending, with the safe or the approximate stop rule.

## Representation

Each tier of each term is a short docid-ordered posting list, so the usual compression applies. The thresholds are global in this page, the same for all terms; MRS also allows a threshold for each term. The full score of a new document needs the weights of all query terms in it, which come from a second, docid-ordered copy of the lists or from a forward index. The total size is $\Theta(n)$ for the tiers plus the size of this second copy.

## Operations

```pseudo id=main
TIERED-SEARCH(q, k, stop)
L1  F ← an empty map from docid to full score
L2  for j ← 1 to r + 1 do
L3      for each query term t and each docid x in tier(t, j) do
L4          if x ∉ F then
L5              F[x] ← the full score of x, by random access to the weight of each query term
L6      if stop = approx and |F| ≥ k then break
L7      if stop = safe and j ≤ r and |F| ≥ k and the k-th best score in F ≥ m τ_j then break
L8  return the k best entries of F, by score descending and then docid ascending
```

After tier $j \le r$, every weight not yet read is less than $\tau_j$, so a document that is not in $F$ has a score less than $m \tau_j$. This is the reason line L7 can use "at least". After tier $r + 1$ every posting has been read.

## Example

Take the toy collection with BM25 weights ($k_1 = 1.2$, $b = 0.75$, the Lucene IDF with the natural log) and the thresholds $\tau_1 = 1.5$, $\tau_2 = 1.0$. Tier 1 holds the strongest postings of the collection, for example list in d4 (1.755) and rank in d7 (1.7825). For q1 "sorted array search", tier 1 has no posting, tier 2 has search in d1 and d7, and tier 3 has sorted in d1, d2, d4, d8 and array in d1, d2, d8.

- **$k = 1$.** After tier 2, $F$ = {d1 3.0283, d7 1.2743}. The best score $3.0283 \ge 3 \times 1.0$, so the safe rule stops after reading 2 postings and scoring 2 documents, with d1, which is the true top 1.
- **$k = 2$, approximate rule.** After tier 2 there are 2 documents, so it stops and returns d1 3.0283 and d7 1.2743. The true second is d2 1.8893, which has no posting in tier 2: d2 is good in sorted and array but best in neither.
- **$k = 2$, safe rule.** After tier 2 the second best score is $1.2743 < 3$, so it reads tier 3 and returns d1 3.0283 and d2 1.8893.

## Correctness

Line L5 gives each document of $F$ its true score, so both rules return true scores in the order of the tie rule. For the safe rule, suppose that line L7 stops after tier $j \le r$. A matching document $y$ that is not in $F$ has no posting in tiers $1, \ldots, j$ for any query term. So each of its query weights is less than $\tau_j$, and at least one is present, so $s(y) < m \tau_j$, which is at most the $k$-th best score in $F$. Each of these $k$ documents ranks before $y$, so the top $k$ of $F$ is the top $k$ of all documents. If no stop happens, $F$ holds all matching documents. The approximate rule has only the weaker property that its $k$ documents carry their true scores; the toy example above shows that it can miss a document of the true top $k$. The full proof is in the proof file.

## Complexity

The model is the [word RAM](/word-ram/) with the index in memory. Let $n$ be the number of postings in the index, $r$ the number of thresholds, and $T$ the total length of the query lists.

- **Build.** Each posting finds its tier by a binary search over the $r$ thresholds, $O(n \log r)$ in total.
- **Query.** At most $T$ tier postings are read, and each new document costs $m$ expected $O(1)$ lookups, so $O(T m)$ expected. The test of line L7 selects the $k$ best of at most $T$ scores after each of at most $r + 1$ tiers, $O(r T \log k)$. In the good case only the first tiers are read, and the cost depends on their length, not on $T$.
- **Space.** $\Theta(n)$ for the tiers, plus the copy for random access.

## Variants

- **Champion lists.** MRS (Section 7.1.3) keep, for each term, a champion list of a fixed number of documents with the highest weights for that term, and score only the union of the champion lists of the query terms. This is a different structure from a tiered index: it has one cut for each term, by rank in the list and not by a weight threshold, and no lower tiers to fall back on. MRS describe tiered indexes as a generalization of champion lists.
- **Thresholds for each term.** A cut by rank or by a weight threshold for each term in place of global thresholds. The safe rule then uses the sum of the thresholds of the query terms in place of $m \tau_j$.
- **Document tiers.** Risvik, Aasheim and Lidal (2003) split a web index by documents, with the most useful documents in the first tier, and send a query to a lower tier only when the first tier does not give a good enough answer.
- **Link to the threshold algorithm.** The safe rule is a coarse form of the stop rule of the [threshold algorithm](/threshold-algorithm/): sorted access by tiers, random access for the full score, and a stop when the $k$-th score reaches a bound on all unseen documents. [Fagin's algorithm](/fagin-algorithm/) is the older method of this family.
- **Static pruning.** Dropping the last tier is [static index pruning](/static-index-pruning/); it saves space but is lossy.

## When to use it

Use a tiered index when most queries are answered well by the strongest postings, and a fast approximate answer is acceptable, for example in a first stage of a large web engine. With the safe rule, use it when the strong postings of the query terms are rare and the $k$-th score after the first tiers is often high; else the safe rule falls back to the lower tiers and does more work than a single pass.

## Pitfalls

- **Calling the approximate rule exact.** The rule "stop when $k$ documents are found" can miss a document that is good in many terms but has no strong posting. Report it as approximate.
- **Bound from the wrong tier.** The safe bound after tier $j$ uses $\tau_j$, the lower edge of tier $j$, not $\tau_{j+1}$ or $\tau_{j-1}$.
- **Partial scores.** Line L5 must compute the full score by random access. Adding only the weights seen in the read tiers gives lower bounds, and then the safe rule is wrong.
- **Count of terms.** The bound $m \tau_j$ needs $m$ to count every query term that has a posting list. Counting fewer is unsafe.
- **Float thresholds.** A weight that is rounded across a threshold goes into the wrong tier, and the bound can then fail. Build the tiers and the bound from the same numbers.

## Implementations

## History

Manning, Raghavan and Schuetze (2008) describe champion lists and tiered indexes as heuristics for fast inexact top $k$ retrieval. Risvik, Aasheim and Lidal (2003) described a multi-tier architecture for web search engines, with tiers of documents. Fagin, Lotem and Naor's threshold algorithm gives the stop rule that the safe version of this page follows.

## References
