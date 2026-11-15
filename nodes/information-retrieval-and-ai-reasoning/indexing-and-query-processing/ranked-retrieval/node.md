---
tag: FZQ3G1
kind: problem
slug: ranked-retrieval
name: Ranked retrieval
aliases:
- top-k ranked retrieval
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: intro
summary: Given a query and a scoring function, return the k documents of highest score, ideally without scoring every document.
model: word-ram
complexity:
  vars: {m: the number of query terms, T: the total length of the m posting lists, k: the number of results}
  time: {exhaustive: "O(T (m + log k))", lower_bound_without_bounds: "Ω(T)"}
prereqs: [posting-list, bm25]
see_also: [document-at-a-time-evaluation, term-at-a-time-evaluation, wand, block-max-wand, maxscore, impact-ordered-index, tiered-index, top-k-selection]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 6 (scoring, term weighting and the vector space model, with Section 6.3.3 on computing vector scores) and Chapter 7 (computing scores in a complete search system, with Section 7.1 on efficient scoring and ranking)
  - paper: doi:10.1016/0306-4573(95)00020-H
    title: Howard Turtle and James Flood, Query evaluation, strategies and optimizations, Information Processing and Management 31(6), 1995, 831-850
    locator: the term-at-a-time and document-at-a-time strategies for ranked queries and their optimizations
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 5, query processing for ranked retrieval
  - book: isbn:9780136072249
    title: W. Bruce Croft, Donald Metzler and Trevor Strohman, Search Engines, Information Retrieval in Practice, Addison-Wesley, 2010
    locator: the material on query processing with indexes, with document-at-a-time and term-at-a-time evaluation
  - paper: doi:10.1561/1500000057
    title: Nicola Tonellotto, Craig Macdonald and Iadh Ounis, Efficient query processing for scalable web search, Foundations and Trends in Information Retrieval 12(4-5), 2018, 319-500
    locator: the definition of top-k query processing over an inverted index, and the survey of exhaustive and dynamic pruning methods
---

Ranked retrieval is the problem of returning, for a query of a few terms, the $k$ documents of a collection with the highest scores under a ranking function, in order. The ranking function is usually a sum of the weights of the query terms in the document, such as [BM25](/bm25/) or [tf-idf](/tf-idf/) in the [vector space model](/vector-space-model/), and the weights are stored in the [posting lists](/posting-list/) of an [inverted index](/inverted-index/). The simple method scores every document that contains a query term and keeps the best $k$. The interesting methods return the same answer while they score far fewer documents, using upper bounds on the weights; others accept an approximate answer in exchange for speed.

## In plain words

A user types a few words, and the search engine must show the best few documents first. Each document gets points for each query word it contains: more for a rare word, more when the word appears often in a short document. The answer is the documents with the most points, best first. The simple way is to give points to every document that has any of the words and sort. A large collection has millions of such documents, but the user wants only ten. So the clever methods try to prove early that most documents cannot make the top ten, and skip them.

## Definition

The input is a collection of $N$ documents with docids $1, \ldots, N$, a query $q$ of $m$ distinct terms, and an integer $k \ge 1$. Each term $t$ has a posting list of pairs $(x, w)$, one for each document $x$ that contains $t$, in increasing docid order, with a weight $w \ge 0$. The score of a document $x$ is

$$s(q, x) = \sum_{t \in q,\ t \in x} w(t, x),$$

and $x$ matches if it contains at least one query term. The output is the list of the $\min(k, |M|)$ matching documents of highest score, where $M$ is the set of matching documents, ranked by score descending and then by docid ascending. The tie rule makes the answer unique.

A method is **safe** if it returns exactly this list, and **approximate** otherwise. The quality of an approximate method is measured against the safe answer or against relevance judgments, with measures such as [precision at k](/precision-at-k/).

## Variants

- **Disjunctive (OR) queries.** A document matches if it contains any query term. This is the definition above.
- **Conjunctive (AND) queries.** A document matches only if it contains all the query terms. The candidates are then the [intersection](/posting-list-intersection/) of the lists, and ranking happens among them.
- **Safe and approximate.** Safe methods, such as WAND with its threshold used as is, return the exact list. Approximate methods, such as WAND with a threshold factor above 1, accumulator limits, the approximate rule of a [tiered index](/tiered-index/), or [static index pruning](/static-index-pruning/), trade quality for speed.
- **Exact order with partial scores.** Some methods return the right $k$ documents in the right order but with lower bounds in place of the scores, as the safe stop on an [impact-ordered index](/impact-ordered-index/).
- **General scoring.** With a scoring function that is not a sum of term weights, such as a [learned ranking model](/learning-to-rank/), the problem is usually split into stages: a sum-of-weights retrieval of a few hundred candidates, then the costly model on these only.

## Examples

Take the toy collection of 8 short documents with BM25 weights ($k_1 = 1.2$, $b = 0.75$, the Lucene IDF with the natural log, average length 9.875 tokens). The query q1 "sorted array search" has the lists sorted: d1, d2, d4, d8; array: d1, d2, d8; search: d1, d7. The scores of the 5 matching documents, rounded to 4 places, are:

| docid | sorted | array | search | score |
|---|---|---|---|---|
| d1 | 0.7192 | 0.98 | 1.3291 | 3.0283 |
| d2 | 0.9497 | 0.9396 | | 1.8893 |
| d8 | 0.6896 | 0.9396 | | 1.6292 |
| d7 | | | 1.2743 | 1.2743 |
| d4 | 0.6896 | | | 0.6896 |

The answer for $k = 3$ is d1 3.0283, d2 1.8893, d8 1.6292. Document d1, "binary search finds a key in a sorted array", has all three terms. Document d2 has sorted twice, which gives it the largest weight of sorted.

The tie rule matters for q2 "posting list merge": d4 has 2.6946, and d3 and d5 both have 2.2139, so the top 2 is d4 and d3, the smaller docid. The query q4 "quantum circuit" matches no document, and the answer is empty for every $k$.

## Known algorithms

- **Exhaustive [document-at-a-time evaluation](/document-at-a-time-evaluation/).** Merge the lists by docid, score each matching document once, and keep the best $k$ in a heap. Safe, $O(T (m + \log k))$ time and $O(m + k)$ space.
- **Exhaustive [term-at-a-time evaluation](/term-at-a-time-evaluation/).** Read one list after another into accumulators. Safe, with one accumulator for each matching document.
- **[MaxScore](/maxscore/).** Splits the terms by their upper bounds and takes candidates only from the essential lists. Safe.
- **[WAND](/wand/).** Finds a pivot where the sum of the upper bounds first exceeds the threshold, and skips the documents before it. Safe with the threshold as is.
- **[Block-max WAND](/block-max-wand/).** Adds upper bounds for each block of postings. Safe.
- **Score-at-a-time on an [impact-ordered index](/impact-ordered-index/).** Reads the postings in decreasing impact, with a safe stop or a fixed budget.
- **[Tiered index](/tiered-index/).** Reads the strongest postings first, with a safe or an approximate stop rule.

The speedups of the pruning methods over exhaustive evaluation are measurements on real collections. In the worst case none of them does better than exhaustive evaluation.

## Bounds

- **Exhaustive time.** Exhaustive DAAT reads each of the $T$ postings once and does $O(\log k)$ work for each matching document in the heap, plus the merge of $m$ cursors.
- **Lower bound without bounds.** A safe method that knows nothing about the weights except what it reads must, in the worst case, read every posting of the query lists: an unread posting could carry a weight large enough to move its document into the top $k$. So it needs $\Omega(T)$ time. Upper bounds on the weights, such as the bound of each list in WAND, are what lets a method skip postings, and even with them the worst case does not improve.
- **A special case.** With two terms, unit weights and $k$ at least the number of matching documents, the documents of score 2 are exactly the intersection of the two lists. So in this case ranked retrieval is at least as hard as the intersection of two sorted lists, and the comparison lower bound for that problem applies: about $\log_2 \binom{p + n}{p}$ comparisons for lists of lengths $p \le n$.

## Reductions

- **To [top-k selection](/top-k-selection/).** Compute the score of every matching document, then select the best $k$. This is the exhaustive method, and its second stage is a selection problem.
- **To a [top-k query](/top-k-query/) over sorted lists.** Each query term gives a list of documents sorted by weight, and the score is a monotone sum. This is the setting of the [threshold algorithm](/threshold-algorithm/) of Fagin, Lotem and Naor and of [Fagin's algorithm](/fagin-algorithm/). The impact-ordered and tiered indexes follow this view; WAND and MaxScore work on docid-ordered lists and use no random access.
- **From list intersection.** The special case in Bounds reduces the intersection of two sorted lists to ranked retrieval.

## Applications

- **Web and enterprise search.** The first stage of a search engine retrieves the top few hundred or thousand documents by a sum of term weights, and later stages rerank them.
- **Candidate generation.** The same retrieval feeds question answering and retrieval-augmented generation, which need the top passages for a question.
- **Evaluation.** Test collections and measures such as precision at $k$ judge the ranked lists that these methods return.

## References
