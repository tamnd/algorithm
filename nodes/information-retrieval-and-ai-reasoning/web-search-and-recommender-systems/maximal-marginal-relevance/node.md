---
tag: 2ZKYCZ
kind: algorithm
slug: maximal-marginal-relevance
name: Maximal marginal relevance
aliases:
- MMR
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Greedily adds the document that maximizes lambda times relevance minus (1 - lambda) times maximum similarity to those already chosen.
solves: [search-result-diversification]
model: word-ram
complexity:
  vars: {n: the number of candidates, k: the number of results}
  time: {worst: O(n log n + n k)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1998
  people: [Jaime Carbonell, Jade Goldstein]
  note: Carbonell and Goldstein introduced MMR at SIGIR 1998 for reranking retrieved documents and for building summaries; it became the standard implicit diversification method.
prereqs: [ranked-retrieval, cosine-similarity, greedy-algorithm]
see_also: [search-result-diversification, ia-select, xquad, probability-ranking-principle, vector-space-model, alpha-ndcg, jaccard-similarity, submodular-function]
sources:
  - paper: doi:10.1145/290941.291025
    title: Jaime Carbonell and Jade Goldstein, The use of MMR, diversity-based reranking for reordering documents and producing summaries, Proceedings of the 21st Annual International ACM SIGIR Conference (SIGIR 1998), 335-336
    locator: the definition of MMR as the argmax over the unselected documents of lambda Sim1(Di, Q) minus (1 - lambda) times the largest Sim2(Di, Dj) over the selected documents, and its use for reranking and for summaries
  - paper: doi:10.1145/3130348.3130369
    title: Jaime Carbonell and Jade Goldstein, The use of MMR, diversity-based reranking for reordering documents and producing summaries, ACM SIGIR Forum 51(2), 2017
    locator: the reprint of the 1998 paper
  - paper: doi:10.1145/1772690.1772780
    title: Rodrygo L. T. Santos, Craig Macdonald and Iadh Ounis, Exploiting query reformulations for web search result diversification, Proceedings of the 19th International Conference on World Wide Web (WWW 2010), 881-890
    locator: Section 2 (MMR as the canonical implicit diversification method, which assumes that similar documents cover similar aspects) and Section 6 (MMR with a trained lambda as a baseline on the TREC 2009 Web track)
---

Maximal marginal relevance (MMR) is a greedy method that reorders a list of retrieved documents so that each new document is both relevant to the query and different from the documents already chosen. Jaime Carbonell and Jade Goldstein introduced it in 1998, for search results and for summaries built from sentences. One parameter $\lambda$ sets the balance: $\lambda = 1$ gives the plain ranking by relevance, and smaller values push near duplicates down. The problem itself, and the methods that model the intents of a query explicitly, such as [IA-Select](/ia-select/) and [xQuAD](/xquad/), are on the [search result diversification](/search-result-diversification/) page; MMR is the implicit method, which only looks at how similar the documents are to each other.

## In plain words

Suppose a search returns ten pages that all say the same thing. The first is useful, but the next nine add little. MMR builds the result list one item at a time. It always takes the item with the best balance of two things: how well it matches the query, and how different it is from everything already in the list. An item that is almost a copy of one already chosen gets a large penalty, even if it matches the query well. A slider decides how much the difference counts, from not at all to a lot.

## The problem

The input is a set $R$ of $n$ candidate documents, usually the top of a first ranking, a relevance score $\mathrm{Sim}_1(d, q)$ for each, a similarity $\mathrm{Sim}_2(d, d')$ between documents, $\lambda \in [0, 1]$ and a length $k$. The output is a list of $\min(k, n)$ documents. Carbonell and Goldstein allow any two similarity functions; the usual choice is [cosine similarity](/cosine-similarity/) of term vectors for both. The method is a heuristic: it does not claim to optimize a stated measure of the whole list, so its gains on diversity metrics are measured on test collections.

## The algorithm

With $S$ the list chosen so far, the next document is

$$d^\ast = \arg\max_{d \in R \setminus S} \Big[ \lambda\, \mathrm{Sim}_1(d, q) - (1 - \lambda) \max_{d' \in S} \mathrm{Sim}_2(d, d') \Big].$$

The maximum over the empty set is taken as 0, so for $\lambda > 0$ the first pick is the most relevant document. Ties go to the smaller document id. The largest similarity of each candidate to $S$ only changes by one new term per step, so the procedure keeps it in an array:

```pseudo id=main
MMR(R, rel, sim, λ, k)
L1  rest ← R sorted by id
L2  S ← empty list
L3  for each d in rest: closest[d] ← 0
L4  while rest is not empty and |S| < k:
L5      for each d in rest:
L6          score(d) ← λ · rel(d) − (1 − λ) · closest[d]
L7      b ← the d with the largest score, ties to the smaller id; move b from rest to S
L8      for each d in rest:
L9          closest[d] ← sim(d, b) if |S| = 1, else max(closest[d], sim(d, b))
L10 return S
```

## Example

Take query q2, "posting list merge", on the eight documents of the shared toy collection. Both similarities are cosines of raw term-count vectors, with no stop words removed. Four documents share a term with the query:

| doc | text | rel |
|---|---|---|
| d2 | merge sort merges two sorted runs into one sorted array | 0.1667 |
| d3 | an inverted index maps each term to a posting list | 0.3651 |
| d4 | a posting list is a sorted list of document ids | 0.4629 |
| d5 | skip pointers speed up the merge of two posting lists | 0.3651 |

The similarities to d4 are 0.1543 for d2, 0.4226 for d3 and 0.1690 for d5: d3 and d4 share "a", "posting" and "list". With $\lambda = 1$ the order is the ranking by relevance, d4, d3, d5, with the tie of d3 and d5 broken by the id. With $\lambda = 0.7$:

| step | d2 | d3 | d4 | d5 | pick |
|---|---|---|---|---|---|
| 1 | 0.1167 | 0.2556 | 0.3240 | 0.2556 | d4 |
| 2 | 0.0704 | 0.1288 | | 0.2049 | d5 |
| 3 | 0.0619 | 0.1288 | | | d3 |

At step 2, d3 loses $0.3 \cdot 0.4226 = 0.1268$ for its overlap with d4, while d5 loses only $0.3 \cdot 0.1690 = 0.0507$, so d5, the document that the judgments of the collection rate highest for q2, moves up to second place. With $\lambda = 0.5$ the order becomes d4, d5, d2: d3 is now penalized below d2, which is not relevant at all. Too small a $\lambda$ trades relevance for difference, which is why $\lambda$ is tuned on judged queries.

## Correctness

The file proofs/correctness.md proves that the loop picks, at every step, the document of the MMR formula with the tie rule. The invariant is that before each pass, $\mathrm{closest}[d]$ is the largest similarity of $d$ to the chosen documents, or 0 before the first pick. Line L9 keeps it, because the maximum over $S \cup \{b\}$ is the larger of the maximum over $S$ and $\mathrm{sim}(d, b)$. Then line L6 computes the MMR score exactly. The proof also shows the two ends of the range: $\lambda = 1$ gives the ranking by relevance, and $\lambda = 0$ ignores relevance entirely: every first score is 0, so the first pick is the smallest id, and each later pick is the document least similar to the chosen ones.

## Complexity

Each of the at most $k$ passes scores at most $n$ documents and computes at most $n$ similarities, so MMR makes at most $nk$ calls of $\mathrm{Sim}_2$ and $O(nk)$ other work, after an $O(n \log n)$ sort of the ids. It keeps one value per candidate, $O(n)$ extra space. If a similarity costs $O(t)$ time, as a cosine of sparse vectors with $t$ terms does, the total is $O(nkt)$. The direct form of the formula, which recomputes the maximum over $S$ at every step, needs $O(nk^2)$ similarities.

## Properties

- **Greedy and myopic.** Each pick is final, and MMR does not look ahead. It gives no approximation guarantee for an objective of the whole list.
- **Implicit.** It knows nothing about the intents of the query. It assumes that documents that are different from each other cover different needs, which Santos, Macdonald and Ounis call implicit diversification.
- **Scale-sensitive.** Relevance and similarity are subtracted, so they must be on comparable scales for $\lambda$ to mean anything.
- **Reduces to relevance ranking.** With $\lambda = 1$ the output is the first ranking, so MMR can only help when $\lambda < 1$.
- **Deterministic.** The tie rule fixes the output.

## Variants and improvements

- **Other similarities.** Any measure works, such as [Jaccard similarity](/jaccard-similarity/) of shingles, distances between embeddings, or the overlap of topic distributions.
- **Summaries.** Carbonell and Goldstein also used MMR to choose sentences for a summary, with sentences in the place of documents. It is still a common baseline for extractive summarization.
- **Recommendation and retrieval for language models.** Recommender systems and retrieval-augmented generation use MMR to pick a varied set of items or passages from the top of a nearest-neighbour search.
- **Explicit methods.** When the intents of a query are known, [IA-Select](/ia-select/) and [xQuAD](/xquad/) reward the coverage of each intent. They have the same greedy shape, with a novelty term per intent in place of the largest similarity.
- **Sum in place of maximum.** Some variants penalize the sum or the average similarity to $S$, which punishes a document that resembles many chosen documents a little.

## When to use it

Use MMR when the top of a ranking contains near duplicates and you have no model of the intents of the query: it needs only a similarity function and one parameter. Tune $\lambda$ on judged queries with a diversity measure such as [alpha-nDCG](/alpha-ndcg/), and expect the best value to be close to 1 when the first ranking is good. If query intents are available, the explicit methods usually do better in the published comparisons, which are measurements on specific test collections.

## Pitfalls

- **The meaning of lambda.** In MMR, $\lambda$ weights relevance; in xQuAD, $\lambda$ weights diversity. Do not carry a tuned value from one to the other.
- **Scores on different scales.** A relevance score such as [BM25](/bm25/) is not bounded by 1, while a cosine is. Normalize the relevance scores, for example by dividing by the largest, before mixing them with similarities.
- **Shared stop words.** Raw cosines are dominated by words such as "a" and "the", as in the example. Use [tf-idf](/tf-idf/) weights or remove stop words before computing similarities.
- **Quadratic similarity cost.** For long lists, $nk$ similarities of long vectors are the main cost. Rerank only the top few hundred documents.
- **Different is not useful.** A document can be different from the chosen ones because it is off topic. Keep $\lambda$ large enough that relevance still counts.

## Implementations

## History

Carbonell and Goldstein presented MMR in a two-page paper at SIGIR 1998. They built it at Carnegie Mellon for reranking search results and for single and multi-document summaries, and they described it as a balance of relevance and novelty. The method became the standard implicit approach to diversification, and later methods such as IA-Select in 2009 and xQuAD in 2010 kept its greedy form while modelling the intents of the query. The paper was reprinted in SIGIR Forum in 2017.

## References
