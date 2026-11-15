---
tag: ZHZBK5
kind: algorithm
slug: xquad
name: xQuAD
aliases:
- explicit query aspect diversification
- eXplicit Query Aspect Diversification
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: research
summary: Greedily picks documents that are relevant to the query and to query aspects not yet covered by the documents already picked.
solves: [search-result-diversification]
model: word-ram
complexity:
  vars: {n: the number of candidate documents, k: the number of results, m: the number of aspects}
  time: {worst: O(n log n + n k m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 2010
  people: [Rodrygo L. T. Santos, Craig Macdonald, Iadh Ounis]
  note: Santos, Macdonald and Ounis introduced xQuAD at WWW 2010, with sub-queries taken from the query reformulations of web search engines, and evaluated it on the diversity task of the TREC 2009 Web track.
prereqs: [search-result-diversification, ia-select]
see_also: [maximal-marginal-relevance, probability-ranking-principle, submodular-function, nemhauser-wolsey-fisher-theorem, alpha-ndcg, bm25, query-likelihood-model, greedy-max-coverage]
sources:
  - paper: doi:10.1145/1772690.1772780
    title: Rodrygo L. T. Santos, Craig Macdonald and Iadh Ounis, Exploiting query reformulations for web search result diversification, Proceedings of the 19th International Conference on World Wide Web (WWW 2010), 881-890
    locator: Section 2 (implicit and explicit diversification, and NP-hardness by reduction from maximum coverage), Section 4.1 (Algorithm 1 and Equations 1 to 5), Section 4.2 (estimation of relevance, coverage, novelty, sub-queries and their importance, with the uniform estimator of Equation 6), Section 5 (the TREC 2009 Web track setup, the baselines and the 5-fold training of lambda), Section 6 (Table 2 and Figure 2)
  - paper: doi:10.1145/1498759.1498766
    title: Rakesh Agrawal, Sreenivas Gollapudi, Alan Halverson and Samuel Ieong, Diversifying search results, Proceedings of the Second ACM International Conference on Web Search and Data Mining (WSDM 2009), 5-14
    locator: Section 3 (Equation 1, the coverage objective that the diversity term of xQuAD shares, and Algorithm 1, IA-Select)
  - paper: doi:10.1145/290941.291025
    title: Jaime Carbonell and Jade Goldstein, The use of MMR, diversity-based reranking for reordering documents and producing summaries, Proceedings of the 21st Annual International ACM SIGIR Conference (SIGIR 1998), 335-336
    locator: the MMR formula, the implicit method that xQuAD is compared with
---

xQuAD (explicit query aspect diversification) is a greedy algorithm for [search result diversification](/search-result-diversification/) that reranks the top of a first ranking by mixing two scores: how relevant a document is to the query, and how well it covers the aspects (sub-queries) of the query that the documents already picked leave uncovered. Rodrygo Santos, Craig Macdonald and Iadh Ounis introduced it in 2010 and took the aspects from the query reformulations that web search engines suggest. Its diversity term is the coverage objective of [IA-Select](/ia-select/); xQuAD adds the plain relevance with a weight $1 - \lambda$, so that $\lambda = 0$ keeps the first ranking and $\lambda = 1$ is IA-Select. Unlike [maximal marginal relevance](/maximal-marginal-relevance/), it never compares two documents with each other.

## In plain words

Suppose someone searches for "jaguar", and the search engine knows that people often rewrite that query as "jaguar car" or "jaguar animal". xQuAD treats each rewrite as one need behind the query. It builds the result list one page at a time. A page earns points for matching the original query, and more points for matching a need that the list does not cover yet. Once a car page is in the list, other car pages earn less from the car need, so a good animal page can move up. A slider sets how much the uncovered needs count against the plain match.

## The problem

The input is a query $q$, a first ranking $R$ of candidates (Santos et al. rerank the top $\tau = 1000$), the relevance $P(d \mid q)$ of each candidate, a set $Q$ of $m$ sub-queries $q_i$ with importances $P(q_i \mid q)$ that sum to 1, the coverage $P(d \mid q_i) \in [0, 1]$ of each candidate for each sub-query, $\lambda \in [0, 1]$ and a length $k$. The output is a list of $\min(k, |R|)$ documents. In the paper, both $P(d \mid q)$ and $P(d \mid q_i)$ come from a retrieval model, such as [BM25](/bm25/) or a [query likelihood](/query-likelihood-model/) model, run once for the query and once for each sub-query.

## The algorithm

With $S$ the list chosen so far, the next document maximizes Equation 5 of the paper:

$$(1 - \lambda)\, P(d \mid q) + \lambda \sum_{q_i \in Q} P(q_i \mid q)\, P(d \mid q_i) \prod_{d_j \in S} \big(1 - P(d_j \mid q_i)\big).$$

The product is the probability that no chosen document satisfies $q_i$, under the assumption that the documents satisfy a sub-query independently. It changes by one factor per pick, so the procedure keeps it per sub-query:

```pseudo id=main
XQUAD(R, rel, P_aspect, cover, λ, k)
L1  for each sub-query i: novel[i] ← 1
L2  S ← empty list
L3  while some document of R is not in S and |S| < k:
L4      for each d not in S, in id order:
L5          score(d) ← (1 − λ) · rel(d) + λ · Σ over i of P_aspect(i) · cover(d, i) · novel[i]
L6      b ← the d with the largest score, ties to the smaller id; append b to S
L7      for each sub-query i that b covers:
L8          novel[i] ← (1 − cover(b, i)) · novel[i]
L9  return S
```

## Example

The query "jaguar" has two aspects, car with importance 0.6 and animal with 0.4, and four candidates:

| doc | $P(d \mid q)$ | $P(d \mid \text{car})$ | $P(d \mid \text{animal})$ |
|---|---|---|---|
| d1 | 0.9 | 0.9 | 0 |
| d2 | 0.8 | 0.8 | 0 |
| d3 | 0.6 | 0 | 0.7 |
| d4 | 0.5 | 0.3 | 0.3 |

With $\lambda = 0$ the list is the first ranking, d1, d2, d3, d4. With $\lambda = 0.5$:

| step | novel(car) | novel(animal) | d1 | d2 | d3 | d4 | pick |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 0.72 | 0.64 | 0.44 | 0.40 | d1 |
| 2 | 0.1 | 1 | | 0.424 | 0.44 | 0.319 | d3 |
| 3 | 0.1 | 0.3 | | 0.424 | | 0.277 | d2 |
| 4 | 0.02 | 0.3 | | | | 0.2698 | d4 |

After d1, the car aspect is 90% covered, so d2 keeps almost only its relevance, $0.4$, plus $0.5 \cdot 0.6 \cdot 0.8 \cdot 0.1 = 0.024$, and d3 moves up because the animal aspect is still open. With $\lambda = 1$ the order is d1, d3, d4, d2: d4 covers a little of both aspects and passes d2, whose only aspect is already served.

## Correctness

The file proofs/correctness.md proves that the loop picks, at each step, the document of Equation 5 with the tie rule. The invariant is that $\mathrm{novel}[i] = \prod_{d_j \in S}(1 - P(d_j \mid q_i))$ before each pass, which line L8 keeps. The proof also shows that the score of $d$ is the marginal gain of the set function

$$F(S) = (1 - \lambda) \sum_{d \in S} P(d \mid q) + \lambda \sum_{q_i} P(q_i \mid q) \Big(1 - \prod_{d \in S} \big(1 - P(d \mid q_i)\big)\Big),$$

the sum of a modular term and the [IA-Select](/ia-select/) objective. With non-negative relevance scores, $F$ is monotone and [submodular](/submodular-function/), so by the [Nemhauser, Wolsey and Fisher theorem](/nemhauser-wolsey-fisher-theorem/) the greedy list has at least $1 - 1/e$ of the best value of $F$. The paper does not state this bound; it is a consequence of the form of Equation 5. The bound is about $F$ under the model, not about measured quality.

## Complexity

Each of the at most $k$ passes computes $n$ scores, each a sum over the sub-queries that the document covers, and updates at most $m$ products. The time is $O(n \log n + nkm)$, including the sort of the ids, and $O(n \log n + k(n + e))$ when only $e$ pairs have nonzero coverage. The extra space is $O(n + m)$. In practice, the main cost is retrieval: one ranking for the query and one for each sub-query. Santos et al. point out that, unlike implicit methods, xQuAD needs no comparisons between the term vectors of documents.

## Properties

- **Explicit.** The aspects are part of the input. The paper takes them from the related and suggested queries of three web search engines.
- **Probabilistic mixture.** The score mixes relevance and novel coverage with one weight $\lambda$.
- **Greedy on a submodular objective.** Each pick has the largest marginal gain of $F$, as shown in the proof.
- **The ends of the range.** $\lambda = 0$ gives the first ranking and $\lambda = 1$ gives IA-Select with the sub-queries as intents.
- **Deterministic.** The tie rule fixes the output.

## Variants and improvements

- **Sub-query importance.** Section 4.2.3 of the paper compares a uniform importance (Equation 6) with estimators from the result sets of the sub-queries, including one inspired by the CRCS method of resource selection.
- **Other aspect sources.** Sub-queries can come from query logs, click graphs, query expansion, clusters of the first ranking, or a taxonomy. Santos et al. also ran xQuAD with the official sub-topics of TREC, as a best case.
- **Implicit counterpart.** [MMR](/maximal-marginal-relevance/) uses the largest similarity to the chosen documents in the place of the per-aspect novelty.
- **Without relevance.** Setting $\lambda = 1$ turns the method into [IA-Select](/ia-select/), and with coverages of $0$ or $1$ into weighted [greedy max coverage](/greedy-max-coverage/).

## When to use it

Use xQuAD when you can produce a few reformulations or sub-topics for an ambiguous query and can score the candidates against each of them, and when you want to keep most of a good first ranking while making room for missed aspects. In the paper, on the 50 queries of the TREC 2009 Web track diversity task, xQuAD with uniform importance improved [alpha-nDCG](/alpha-ndcg/) over the BM25, DPH and language model baselines, by up to 30% (BM25, alpha-nDCG@5), and did better than MMR and simulated versions of IA-Select and of the method of Radlinski and Dumais in most settings. These are measurements on one collection, with $\lambda$ trained by 5-fold cross validation; the learned value was small, with a peak near $\lambda = 0.15$ for BM25 and DPH in Figure 2.

## Pitfalls

- **The meaning of lambda.** In xQuAD, $\lambda$ weights diversity; in MMR, it weights relevance. A value tuned for one does not carry over.
- **Probabilities from scores.** Equation 5 treats $P(d \mid q)$ and $P(d \mid q_i)$ as probabilities. Raw BM25 scores are not in $[0, 1]$ and are not comparable across sub-queries; normalize them first, or the products and the mix lose their meaning.
- **Bad sub-queries.** A sub-query that is only a paraphrase of the query adds no diversity, and a wrong one promotes off-topic documents. The quality of the aspects limits the method.
- **Coverage of 1.** A document with $P(d \mid q_i) = 1$ closes the aspect for good: every later document gets nothing from it.
- **Evaluation leakage.** Running xQuAD with the official sub-topics of a test collection, as the best case in the paper does, uses the judgments' own aspect structure. Report such runs apart from runs with real sub-queries.

## Implementations

## History

Santos, Macdonald and Ounis presented xQuAD at WWW 2010 as part of their work at the University of Glasgow on the diversity task of the TREC 2009 Web track. They framed it as a probabilistic version of the greedy approximation used by most earlier methods, with explicit sub-queries in the place of comparisons between documents, and they built on the coverage idea of Agrawal et al. from 2009. xQuAD became one of the standard explicit diversification baselines, together with IA-Select.

## References
