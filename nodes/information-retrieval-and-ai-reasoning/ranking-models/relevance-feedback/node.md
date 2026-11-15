---
tag: T0ENHH
kind: technique
slug: relevance-feedback
name: Relevance feedback
aliases:
- user relevance feedback
area: information-retrieval-and-ai-reasoning/ranking-models
level: intro
summary: Uses the documents a user marks relevant or not relevant to build a better query for a second round of retrieval.
prereqs: [vector-space-model, ranked-retrieval]
see_also: [rocchio-algorithm, pseudo-relevance-feedback, relevance-model-rm3, binary-independence-model, bm25, precision-and-recall, interleaving, learning-to-rank]
sources:
  - paper: "J. J. Rocchio, Relevance feedback in information retrieval, in Gerard Salton (editor), The SMART Retrieval System: Experiments in Automatic Document Processing, Prentice-Hall (1971)"
    locator: the query modification from judged relevant and nonrelevant documents in the vector space model
  - paper: doi:10.1002/asi.4630270302
    title: Stephen E. Robertson and Karen Sparck Jones, Relevance weighting of search terms, Journal of the American Society for Information Science 27(3) (1976), 129-146
    locator: the weighting of query terms from the counts of relevant documents that contain them
  - paper: "Gerard Salton and Chris Buckley, Improving retrieval performance by relevance feedback, Journal of the American Society for Information Science 41(4) (1990), 288-297"
    locator: the comparison of twelve feedback methods on six test collections, evaluated on the residual collection
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 9 (relevance feedback and query expansion), Section 9.1 (relevance feedback and pseudo relevance feedback)
---

Relevance feedback is a two-round search. The system returns a first ranking, the user marks some of the results as relevant or not relevant, and the system uses these judgments to build a new query that runs again. The new query gives more weight to terms that the relevant documents share, including terms that the user never typed, and less weight to terms of the nonrelevant ones. The idea goes back to the SMART system of the 1960s, where the [Rocchio algorithm](/rocchio-algorithm/) is the classic form in the [vector space model](/vector-space-model/); the probabilistic models reweight terms by the counts of relevant documents that contain them, and the language models estimate a [relevance model](/relevance-model-rm3/). When the judgments are not given by a user but assumed for the top results, the technique is [pseudo-relevance feedback](/pseudo-relevance-feedback/).

## In plain words

People often do not know the best words for what they want, and documents about the same thing use different words. But people can tell a good result when they see one. Relevance feedback uses this. After the first search, the user says which results are good and which are bad. The system looks at the good ones and finds the words they have in common, and looks at the bad ones to find words to avoid. It adds the common words to the query, makes the words that mark good results count more, and searches again. The second list then holds more documents like the good ones, even documents that do not contain the words that the user first typed.

## When it applies

Use it when a user is willing to judge a few results, or when judgments can be read from behaviour, such as clicks. It helps most when the first query misses relevant documents because of vocabulary, when the task needs high recall, as in a literature search or legal discovery, and when the relevant documents resemble each other. It needs a first ranking with at least some relevant documents near the top; if the user finds nothing relevant, only negative feedback is left, which helps little. It is a weak choice for a query that the first search already answers, and for needs whose relevant documents form several separate groups.

## The template

```pseudo id=main
FEEDBACK-SEARCH(q, c)
L1  R1 ← SEARCH(q), and show its top c documents
L2  (Dr, Dn) ← the shown documents judged relevant and not relevant    ▷ hole: explicit marks, clicks, or an assumption
L3  q' ← UPDATE(q, Dr, Dn)                ▷ hole: Rocchio, term reweighting, a relevance model
L4  R2 ← SEARCH(q')                        ▷ hole: keep the judged documents, or remove them
L5  return R2
```

**Two classic updates on the toy collection.** Take q1 = "sorted array search". In the first ranking, document 1, "binary search finds a key in a sorted array", is first. The user marks document 1 relevant and document 6, "a hash table finds a key in constant expected time", not relevant.

*In the vector space model*, Rocchio with weights 1, 0.75 and 0.15, after [stop word removal](/stop-word-removal/), gives the new query sorted, array and search at 1.75, binary at 0.75, and finds and key at 0.6. The ranking by cosine goes from $1, 2, 8, 7, 4$ to $1, 2, 8, 7, 4, 6, 3, 5$: the order of the top does not change, document 1 rises from 0.7071 to 0.9084, and document 6, which shares no word with q1, now gets a score through "finds" and "key". Without stop word removal the rejected document 6 climbs to third place, through "a", "in", "finds" and "key"; the [Rocchio page](/rocchio-algorithm/) shows the full tables.

*In the binary independence model*, with $N$ documents, $n_t$ of them holding term $t$, $R$ judged relevant documents and $r_t$ of them holding $t$, the weight of a query term is

$$w_t = \log \frac{(r_t + 0.5)/(R - r_t + 0.5)}{(n_t - r_t + 0.5)/(N - n_t - R + r_t + 0.5)}.$$

With no judgments ($R = r_t = 0$) this is an idf, $\log((N - n_t + 0.5)/(n_t + 0.5))$. With $N = 8$ and $n_t$ equal to 4, 3 and 2 for "sorted", "array" and "search":

| term | $n_t$ | weight, no feedback | weight, $R = 1$ and $r_t = 1$ |
|---|---|---|---|
| sorted | 4 | 0 | 1.3499 |
| array | 3 | 0.4520 | 1.8871 |
| search | 2 | 0.9555 | 2.5649 |

A document scores the sum of the weights of the query terms it holds. Before feedback, document 7 (search only) at 0.9555 is above documents 2 and 8 (sorted and array) at 0.4520, and document 4 (sorted only) gets 0. After document 1 is judged relevant, documents 2 and 8 get 3.2370 and pass document 7 at 2.5649, and "sorted" gets a positive weight, because the relevant document holds all three terms. The order becomes $1, 2, 8, 7, 4$, with 2 and 8 tied.

## Classic examples

- **[Rocchio algorithm](/rocchio-algorithm/).** Move the query vector toward the centroid of the relevant documents and away from the centroid of the nonrelevant ones. It expands the query with new terms.
- **[Binary independence model](/binary-independence-model/).** Replace the idf of each query term by the relevance weight of Robertson and Sparck Jones, computed from $R$ and $r_t$ as above. Plain use reweights the query terms and adds none; choosing new terms by their weight in the relevant documents adds expansion. In [BM25](/bm25/) the same weight replaces the idf factor.
- **[Relevance model](/relevance-model-rm3/).** Estimate a distribution of words from the relevant documents, mix it with the query model, and rank by it in the language modeling approach.
- **[Pseudo-relevance feedback](/pseudo-relevance-feedback/).** Assume the top documents of the first round are relevant and run any of the updates above with no user.

## Variations

- **Explicit, implicit and pseudo.** The judgments can come from the user's marks, from behaviour such as clicks and reading time, or from the assumption that the top results are relevant. Implicit judgments are noisy: a click shows that a snippet looked good, not that the document was. Clicks are also used to train rankers, with [learning to rank](/learning-to-rank/) and [interleaving](/interleaving/).
- **Positive feedback only.** Many systems ignore the nonrelevant documents, because they are varied and their centroid says little.
- **Interactive query expansion.** The system proposes terms from the relevant documents and the user picks some, in place of adding them all.
- **Several rounds.** Repeat the loop. Each round needs new judgments, and the gains of later rounds are usually smaller.
- **Term selection.** Add only the best $m$ new terms, by weight in the relevant documents, to keep the second query short.

## Pitfalls

- **Measuring on the judged documents.** The documents that the user marked relevant rise in the second ranking almost by construction. Evaluate on the residual collection, the documents the user has not judged, as Salton and Buckley did, or report both.
- **Common words.** Every word of a relevant document gets weight, including function words, which can lift rejected documents, as in the Rocchio example. Remove stop words or use idf weights first.
- **Query drift.** If the judged relevant documents cover only one side of the need, the new query follows that side and can lose the rest. Keep the original query terms in the new query with a large weight.
- **Cost of the second round.** The new query can hold many terms, each with a posting list, so the second search is slower. Cut the query to its top terms.
- **Users may not judge.** The method needs judgments. If users rarely give them, as in most web search, use implicit or pseudo feedback, and measure whether it helps.

## Exercises

1. In the probabilistic example, compute the weight of "binary", which only document 1 holds, after the same feedback. *Answer:* $n_t = 1$, so $w_t = \log((1.5/0.5)/(0.5/7.5)) = \log 45 = 3.8067$, larger than the weight of any original query term. A system that adds new terms by this weight would add "binary" first.
2. Show that with $R = 0$ the weight of a term is 0 exactly when the term occurs in half of the documents, and negative when it occurs in more, and explain why "sorted" gets weight 0 before feedback. *Answer:* the ratio $(N - n_t + 0.5)/(n_t + 0.5)$ is 1 exactly when $n_t = N/2$, and "sorted" occurs in 4 of the 8 documents.
3. Explain why the Rocchio update with $\gamma = 0$ and a pseudo set of the top $k$ documents can never lower the weight of an original query term. *Hint:* all document weights are nonnegative, so line L2 of Rocchio only adds.

## References
