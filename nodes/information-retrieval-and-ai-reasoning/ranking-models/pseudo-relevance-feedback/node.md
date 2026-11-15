---
tag: E2KHY9
kind: technique
slug: pseudo-relevance-feedback
name: Pseudo-relevance feedback
aliases:
- blind relevance feedback
area: information-retrieval-and-ai-reasoning/ranking-models
level: core
summary: Assumes the top documents of a first retrieval are relevant and expands the query with their terms, with no user input.
prereqs: [relevance-feedback]
see_also: [rocchio-algorithm, relevance-model-rm3, query-likelihood-model, bm25, binary-independence-model, stop-word-removal, kullback-leibler-divergence, mean-average-precision]
sources:
  - paper: "W. Bruce Croft and David J. Harper, Using probabilistic models of document retrieval without relevance information, Journal of Documentation (1979)"
    locator: the use of the top-ranked documents of a first search in place of judged relevant documents in the probabilistic model
  - paper: "Jinxi Xu and W. Bruce Croft, Query expansion using local and global document analysis, Proceedings of the 19th Annual International ACM SIGIR Conference (SIGIR 1996)"
    locator: local feedback from the top-ranked documents and local context analysis
  - paper: doi:10.1145/383952.383972
    title: Victor Lavrenko and W. Bruce Croft, Relevance-based language models, Proceedings of the 24th Annual International ACM SIGIR Conference (SIGIR 2001), 120-127
    locator: Section 3, the estimation of the relevance model from the top-ranked documents with no relevance judgments
  - paper: "Nasreen Abdul-Jaleel, James Allan, W. Bruce Croft, Fernando Diaz, Leah Larkey, Xiaoyan Li, Mark D. Smucker and Courtney Wade, UMass at TREC 2004, novelty and HARD, Proceedings of the Thirteenth Text REtrieval Conference (TREC 2004)"
    locator: Section 3.1.4, RM3 with 50 feedback documents, 200 terms and the original query mixed in
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 9, Section 9.1 (pseudo relevance feedback as the automatic form of relevance feedback)
---

Pseudo-relevance feedback runs [relevance feedback](/relevance-feedback/) with no user. It takes the top $k$ documents of a first search, assumes that they are relevant, finds the terms that are frequent in them and rare elsewhere, adds the best of these terms to the query, and searches again. Any feedback update can be used: [Rocchio](/rocchio-algorithm/) with no negative part, the relevance weights of the [binary independence model](/binary-independence-model/), or the [relevance model](/relevance-model-rm3/) of the language modeling approach. On test collections it raises average effectiveness, mostly recall, but it lowers it on queries whose first top documents are off topic, because the new query then drifts toward them. Croft and Harper proposed using the top documents in place of judgments in 1979, and it became a standard part of TREC systems in the 1990s.

## In plain words

Relevance feedback works well, but users seldom mark results. So we guess. We take the first few results of a search and act as if the user had marked them all as good. The words that these documents share are probably about the topic, so we add the most telling of them to the query and search again. When the first results are good, the new query finds more good documents, including ones that use other words for the same thing. When the first results are bad, the new query finds more documents like the bad ones. This shift away from what the user meant is called drift, and it is the main risk of the method.

## When it applies

Use it when there are no judgments, the first search puts mostly relevant documents at the top, and recall matters, for example in ad hoc search over news or scientific text with short queries. It helps most for short queries that miss synonyms. It is a poor choice when precision at the very top is all that counts, when the first ranking is weak, when queries are already long and specific, and when a second search is too slow for the latency budget, since the expanded query has many terms.

## The template

```pseudo id=main
PRF(q, k, m, λ)
L1  R1 ← SEARCH(q)
L2  F ← the top k documents of R1                       ▷ hole: k, usually 10 to 50
L3  for each term t of F: w(t) ← WEIGHT(t, F)            ▷ hole: Rocchio weight, relevance weight, relevance model
L4  E ← the m terms of largest w(t), without stop words  ▷ hole: m
L5  q' ← λ · q + (1 - λ) · E                             ▷ hole: the share λ of the original query
L6  return SEARCH(q')
```

Line L3 is where the methods differ. Rocchio with $\gamma = 0$ uses the mean weight of $t$ in the documents of $F$. The probabilistic form treats $F$ as the set of relevant documents and computes the relevance weight with $R = k$. The relevance model uses $\sum_{d \in F} p(t \mid d) \, P(d \mid q)$, a mixture of the document models weighted by their query likelihood. Line L5 keeps the original query in the new one; the UMass runs at TREC 2004 used 50 documents, 200 terms and a weight of 0.6 for the original query.

**Walk-through on the toy collection.** Take q1 = "sorted array search", a first search by the [query likelihood model](/query-likelihood-model/) with Dirichlet smoothing at $\mu = 10$, $k = 2$ and the relevance model in line L3. The top two documents are document 1, "binary search finds a key in a sorted array", and document 2, "merge sort merges two sorted runs into one sorted array", with feedback weights 0.7817 and 0.2183. After [stop words](/stop-word-removal/) are removed, the six best terms are "sorted", "array", "search", "binary", "finds" and "key", and with $\lambda = 0.5$ the new query weights are 0.2779 for "sorted", 0.2593 for "array", 0.2407 for "search" and 0.0740 for each of the other three. The [relevance model page](/relevance-model-rm3/) gives every step. Both rows of the table are scores $\sum_t p(t \mid \theta_q) \log p(t \mid d)$ with the same document models; for the first search the query model gives each of the three words $1/3$, so its scores are the log likelihoods divided by 3.

| document | 1 | 2 | 8 | 7 | 4 | 6 | 3 | 5 |
|---|---|---|---|---|---|---|---|---|
| first search, divided by 3 | -2.5985 | -3.0236 | -3.1829 | -3.3957 | -3.6129 | -3.9289 | -3.9289 | -3.9289 |
| second search | -2.6281 | -3.3303 | -3.4630 | -3.6760 | -3.7976 | -3.8242 | -4.0610 | -4.0610 |

The top five keep their order $1, 2, 8, 7, 4$, which already held all three relevant documents of q1 (1, 2 and 8). The change is below them: document 6, "a hash table finds a key in constant expected time", tied with documents 3 and 5 at the bottom before feedback, and now it is above them, because it shares "finds" and "key" with document 1. Document 6 is not relevant to q1. This is drift on a small scale: the new terms describe document 1, not the need of the query.

## Classic examples

- **[Rocchio algorithm](/rocchio-algorithm/).** In vector space systems, the top $k$ documents are the relevant set and $\gamma = 0$. TREC systems of the 1990s used this form.
- **[Binary independence model](/binary-independence-model/) and [BM25](/bm25/).** The top documents give $R$ and $r_t$ for the relevance weight, and new terms are chosen by their weight. Croft and Harper used the top documents in this way.
- **[Relevance model](/relevance-model-rm3/).** Lavrenko and Croft estimate the relevance model from the top documents of a query likelihood search; RM3 mixes it with the query model. It is a common baseline of pseudo-relevance feedback.
- **[Query likelihood model](/query-likelihood-model/) with a feedback query model.** Any query model estimated from the top documents can replace the maximum likelihood query model in the ranking by negative [KL divergence](/kullback-leibler-divergence/).

## Variations

- **Local context analysis.** Xu and Croft choose expansion terms by how often they occur near the query terms in the top passages, not in the whole top documents.
- **Weighting the feedback documents.** Give each document of $F$ a weight by its first-round score, as the relevance model does, instead of treating the top $k$ alike.
- **Selective feedback.** Predict from the first ranking whether feedback will help this query, and skip it when the top documents look inconsistent.
- **External collections.** Run the first search on a larger or cleaner collection, take the expansion terms from there, and search the target collection with them.
- **Feedback for dense retrievers.** Combine the embeddings of the top documents with the query embedding, the analogue of Rocchio in a dense vector space.

## Pitfalls

- **Query drift.** If the top $k$ are off topic, or about one side of the need, the expansion pulls the second ranking further that way, as document 6 shows. Keep a large share $\lambda$ for the original query and a small $m$.
- **Average gains hide losses.** Gains are reported as a mean over queries, such as [mean average precision](/mean-average-precision/). Some queries get worse. Report how many queries improve and how many get worse, not only the mean.
- **Common words.** Without stop word removal or an idf-like term score, the top terms of $F$ are function words, which add noise and cost. Line L4 removes them.
- **Tuning three parameters.** The results depend on $k$, $m$ and $\lambda$, and the best values differ across collections. Values tuned on the test queries overstate the gain.
- **Latency.** The second search reads one posting list for each of up to hundreds of terms. In an interactive system this can cost more than the gain is worth.

## Exercises

1. In the walk-through, why do documents 3 and 5 still tie after feedback? *Answer:* neither holds any of the six expansion terms, and they have the same length, so they get the same smoothed score.
2. Explain why pseudo-relevance feedback with $k = 1$ and Rocchio with $\gamma = 0$ moves the query toward one document, and what happens to the ranking if that document is not relevant. *Hint:* the centroid of one document is that document.
3. Show that if $\lambda = 1$ in line L5, the second search returns the first ranking. *Answer:* then $q' = q$.

## References
