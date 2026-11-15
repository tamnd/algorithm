---
tag: TWQ776
kind: technique
slug: static-index-pruning
name: Static index pruning
aliases:
- Carmel static pruning
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: advanced
summary: Removes low-impact postings from an inverted index at build time, so the index is smaller and faster with a small, measured loss in ranking quality.
prereqs: [posting-list, ranked-retrieval]
see_also: [tiered-index, impact-ordered-index, wand, inverted-index, precision-at-k, mean-average-precision, test-collection, pruning]
sources:
  - paper: doi:10.1145/383952.383958
    title: David Carmel, Doron Cohen, Ronald Fagin, Eitan Farchi, Michael Herscovici, Yoelle S. Maarek and Aya Soffer, Static index pruning for information retrieval systems, SIGIR 2001
    locator: the top-k pruning rule with the factor epsilon for each term, the uniform pruning rule with one global threshold, the guarantee on the top answers of short queries, and the experiments with the Juru search engine on TREC data
  - paper: doi:10.1145/1183614.1183644
    title: Stefan Buettcher and Charles L. A. Clarke, A document-centric approach to static index pruning in text retrieval systems, CIKM 2006
    locator: the pruning rule that keeps, for each document, the terms that contribute most to it, and its comparison with term-centric pruning
  - paper: doi:10.1561/1500000057
    title: Nicola Tonellotto, Craig Macdonald and Iadh Ounis, Efficient query processing for scalable web search, Foundations and Trends in Information Retrieval 12(4-5), 2018, 319-500
    locator: the part on static pruning of the index, as opposed to the dynamic pruning of WAND and MaxScore
---

Static index pruning removes postings from an [inverted index](/inverted-index/) once, at build time, when they are not likely to matter for the top results of any query. The pruned index is smaller, so it fits in faster memory and its [posting lists](/posting-list/) are shorter to read. This is unlike the dynamic pruning of [WAND](/wand/) or MaxScore, which skips work at query time and can be safe. Static pruning is lossy: a removed posting is gone for every query, so scores change and some rankings change. Its quality is measured, not proved in general. The usual test runs the queries of a [test collection](/test-collection/) on the full and the pruned index, and compares measures such as [precision at k](/precision-at-k/) or [mean average precision](/mean-average-precision/), together with the size of the index. Carmel and others (2001) gave the classic term-centric rule: for each term, keep the postings whose score is at least a fraction $\varepsilon$ of the $k$-th best score in the list of that term.

## In plain words

Most entries of a search index are weak: a word that appears once in a long document adds very little to its score. If you throw such entries away before any query comes, the index gets smaller and searches get faster. The price is that some answers change. A document that was good because it had many weak matches can drop down or vanish. Nothing can promise that the answers stay the same for all queries, so you check by experiment: run many test queries on both indexes and see how much the quality drops for the space you save.

## When it applies

It applies when the full index is too large for the memory or the time budget, and a small drop in ranking quality is acceptable. It needs a ranking function whose score is a sum of the weights of the query terms, such as [BM25](/bm25/) or [tf-idf](/tf-idf/), so that the contribution of each posting can be judged on its own. It suits short queries best: a query with few terms depends mostly on the strong postings of those terms. It does not apply when the results must be exactly those of the full index; then use a safe method such as WAND, MaxScore, or the safe rule of a [tiered index](/tiered-index/).

## The template

1. **Score each posting.** Compute the weight $w(t, x)$ of each posting with the ranking function of the system.
2. **Choose a rule.** The term-centric rule of Carmel and others, top-$k$ pruning: for each term $t$, let $z_t$ be the $k$-th largest weight in the list of $t$, or the smallest one if the list is shorter, and keep the postings with $w(t, x) \ge \varepsilon z_t$, for a factor $0 < \varepsilon \le 1$. Uniform pruning: keep the postings with $w(t, x) \ge \tau$ for one global $\tau$. A document-centric rule: for each document, keep its strongest terms.
3. **Remove the postings.** Write the pruned lists. Keep the original weights; do not compute the weights again from the pruned index, or the scores of all documents change.
4. **Measure.** Run a set of test queries on both indexes. Report the fraction of postings removed, the size and query time, and the quality: the overlap of the top $k$ and measures such as precision at $k$, MAP or [nDCG](/normalized-discounted-cumulative-gain/), each compared with the full index.
5. **Tune.** Choose $k$ and $\varepsilon$, or $\tau$, by the measured trade-off between size and quality.

The rule of Carmel and others comes with a guarantee for their scoring model: for queries with few terms, the top answers of the pruned index stay close to those of the full index, by a closeness that depends on $\varepsilon$. The guarantee is about the similarity of the top answers under their model, not about equal results, and it is stated in the paper.

## Classic examples

**Top-$k$ pruning on the toy collection.** Take the toy collection with BM25 weights ($k_1 = 1.2$, $b = 0.75$, the Lucene IDF with the natural log), which has 74 postings. With $k = 1$ and $\varepsilon = 0.8$, each term keeps the postings with weight at least 0.8 times its largest weight. Six postings are removed: a in d3 and d7, sorted in d1, d4 and d8, and list in d3. For example, sorted has the largest weight 0.9497, so it keeps only weights of at least 0.7598, which leaves d2.

| query | full index | pruned index |
|---|---|---|
| q1 "sorted array search" | d1 3.0283, d2 1.8893, d8 1.6292, d7 1.2743, d4 0.6896 | d1 2.3091, d2 1.8893, d7 1.2743, d8 0.9396 |
| q2 "posting list merge" | d4 2.6946, d3 2.2139, d5 2.2139, d2 1.2743 | d4 2.6946, d5 2.2139, d2 1.2743, d3 0.9396 |

The top document of each query stays the same, as the rule aims for $k = 1$. Below it the ranking changes: for q1, d8 drops below d7 and d4 is gone; for q2, d3, which tied with d5 and won by docid, drops to fourth. With $k = 2$ and $\varepsilon = 1.0$, four postings are removed (a in d3 and d7, sorted in d4 and d8); the top 2 of q1 stays the same, but the third place changes. With $k = 2$ and $\varepsilon = 0.9$ only the two postings of a are removed.

**Carmel and others (2001).** They tested top-$k$ pruning and uniform pruning with the Juru search engine on TREC data. Their measurements showed that a large part of the index could be removed with a small change in the top results and in precision for short queries. These results are measurements on their collections and queries.

**Document-centric pruning.** Buettcher and Clarke (2006) keep, for each document, the terms that contribute most to it, and they measured that for some sizes this keeps quality better than term-centric pruning. A document then always keeps its most typical terms, even when they are common in the collection.

## Variations

- **Uniform pruning.** One global threshold for all terms. It is simple, but it can empty the lists of terms whose weights are all small.
- **Term-centric with a share.** Keep a fixed share of each list in place of a factor of the $k$-th score.
- **Pruning with tiers.** Keep the removed postings in a second, slower index, as the last tier of a [tiered index](/tiered-index/), and read it only when the first tier does not give good enough results. This keeps the space saving on the fast index and lets a safe stop rule fall back.
- **Pruning by document.** Remove whole documents that are not likely to be retrieved, for example by a static quality score.
- **Combination with dynamic pruning.** A pruned index can still be queried with WAND or MaxScore; these methods are then safe for the pruned index, not for the full one.

## Pitfalls

- **Calling it safe.** Static pruning changes scores and rankings. A guarantee for short queries under one scoring model is not a guarantee for all queries.
- **Recomputing statistics.** If the document frequencies or lengths are computed again from the pruned index, every weight changes, and the effect is not the one that was measured.
- **Measuring only the top 1.** A rule tuned for the top $k$ can change the ranks below $k$ a lot, as the toy example shows. Measure at the depth that the users see.
- **Lost terms.** A rare term with only weak postings can lose its whole list under uniform pruning, and then queries with that term find nothing for it.
- **Ties.** A removed posting can break a tie, as with d3 and d5 in q2. Tests that compare rankings must use the same tie rule on both indexes.

## Exercises

1. On the toy collection, compute the postings that top-$k$ pruning removes with $k = 1$ and $\varepsilon = 0.9$, and the new top 3 of q1.
2. Give an index and a query of two terms for which top-$k$ pruning with $k = 1$ and $\varepsilon = 1$ changes the top 1 of the query.
3. Show that uniform pruning with threshold $\tau$ keeps the top $k$ of a one-term query unchanged whenever the $k$-th weight of its list is at least $\tau$.
4. A pruned index is queried with WAND. Explain why the results are exactly the top $k$ of the pruned index but can differ from the top $k$ of the full index.

## References
