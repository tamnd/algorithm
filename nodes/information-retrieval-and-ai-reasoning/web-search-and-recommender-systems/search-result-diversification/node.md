---
tag: EC4SG4
kind: problem
slug: search-result-diversification
name: Search result diversification
aliases:
- diversity-aware ranking
- result diversification
- diversified ranking
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Rank results so that the top covers the different intents of an ambiguous query while each result stays relevant.
prereqs: [ranked-retrieval, probability-ranking-principle]
see_also: [maximal-marginal-relevance, ia-select, xquad, alpha-ndcg, normalized-discounted-cumulative-gain, max-coverage, submodular-function, max-coverage-inapproximability]
sources:
  - paper: doi:10.1145/1498759.1498766
    title: Rakesh Agrawal, Sreenivas Gollapudi, Alan Halverson and Samuel Ieong, Diversifying search results, Proceedings of the Second ACM International Conference on Web Search and Data Mining (WSDM 2009), 5-14
    locator: Section 3 (Equation 1, the objective P(S | q)), Section 3.3 (Lemma 1, NP-hardness from Max Coverage), Section 3.4 (Lemma 2, submodularity), Section 3.5 (Algorithm 1, IA-Select), Section 3.6 (Theorem 1 and Corollary 1, optimality with one category per document; Theorem 2, the (1 - 1/e) bound), Section 4 (NDCG-IA, MAP-IA and MRR-IA)
  - paper: doi:10.1145/1772690.1772780
    title: Rodrygo L. T. Santos, Craig Macdonald and Iadh Ounis, Exploiting query reformulations for web search result diversification, Proceedings of the 19th International Conference on World Wide Web (WWW 2010), 881-890
    locator: Section 2 (diversification as a bicriterion problem, its NP-hardness as an instance of maximum coverage, and implicit against explicit methods), Section 5 (the TREC 2009 Web track diversity task with 50 queries, alpha-nDCG and IA-P) and Section 6 (Table 2)
  - paper: "Charles L. A. Clarke, Maheedhar Kolla, Gordon V. Cormack, Olga Vechtomova, Azin Ashkan, Stefan Büttcher and Ian MacKinnon, Novelty and diversity in information retrieval evaluation, Proceedings of the 31st Annual International ACM SIGIR Conference (SIGIR 2008)"
    locator: Section 1 (the ambiguous query jaguar), Section 2 (related work, including Goffman 1964 on relevance that depends on the documents seen before), Section 4 (information needs and documents as sets of nuggets, a document being relevant when it contains at least one nugget of the need) and the definition of alpha-nDCG
  - paper: doi:10.1145/290941.291025
    title: Jaime Carbonell and Jade Goldstein, The use of MMR, diversity-based reranking for reordering documents and producing summaries, Proceedings of the 21st Annual International ACM SIGIR Conference (SIGIR 1998), 335-336
    locator: the MMR criterion, which trades the relevance of a document against its largest similarity to the documents already selected
---

Search result diversification is the problem of choosing and ordering the top results for a query so that they cover the different intents of the query, for example the car, the cat and the guitar for "jaguar", while each result stays relevant. It exists because the [probability ranking principle](/probability-ranking-principle/) scores each document on its own, while a user who is already satisfied by one result gains little from a second result about the same thing. This page states the problem, its hardness and its known methods. The methods have their own pages: [maximal marginal relevance](/maximal-marginal-relevance/) compares documents with each other, [IA-Select](/ia-select/) maximizes intent coverage, and [xQuAD](/xquad/) mixes coverage with relevance; the measures, such as [alpha-nDCG](/alpha-ndcg/), are also separate pages.

## In plain words

Some queries mean several things. "Jaguar" can be a car, an animal or a guitar. If a search engine scores each page on its own, the top ten may all be about the car, because most people mean the car. Then everybody who meant the animal leaves with nothing. A better top ten puts the best car pages first but also gives the animal and the guitar a page each, early enough to be seen. The hard part is the trade: every place given to a rare meaning is a place taken from the common one. Diversification asks for the list that serves the most users in total, where a user is served when at least one page in the list fits what that user meant.

## Definition

**Intent-aware form** (Agrawal, Gollapudi, Halverson and Ieong, Section 3). The input is:

- a query $q$ and a set $R$ of $n$ candidate documents, usually the top of a first [ranked retrieval](/ranked-retrieval/) run;
- a number $k$ of results;
- a set $C$ of $m$ intents (categories, aspects, sub-topics) with a distribution $P(c \mid q)$;
- for each document $d$ and intent $c$, a value $V(d \mid q, c) \in [0, 1]$, the probability that $d$ satisfies a user with intent $c$.

The task is to find $S \subseteq R$ with $|S| = k$ that maximizes

$$P(S \mid q) = \sum_{c \in C} P(c \mid q) \Big( 1 - \prod_{d \in S} \big(1 - V(d \mid q, c)\big) \Big),$$

the probability that a random user finds at least one satisfying result in $S$. The documents are assumed to satisfy a user independently once the intent is fixed. The objective is a set function, so the order inside $S$ is not part of it; methods return the documents in the order in which they choose them, and the measures reward lists that cover the intents early.

**Bicriterion form** (Santos, Macdonald and Ounis, Section 2). Without a model of the user, the problem is stated as two goals at once: every result should be relevant to the query, and the results should differ from each other in the aspects they cover. A weight sets the balance between the two, as in MMR and xQuAD.

**Nugget form** (Clarke et al., Section 4). An information need and a document are each a set of nuggets, small units of information. A document is relevant when it contains at least one nugget of the need, and a nugget that already appeared higher in the list adds less. This follows Goffman (1964), cited by Clarke et al., who observed that the relevance of a document depends on the documents shown before it.

## Variants

- **Explicit diversification.** The intents are given or estimated: categories of a taxonomy in Agrawal et al., query reformulations used as sub-queries in Santos et al.
- **Implicit diversification.** There are no intents. The method penalizes a candidate for its similarity to the documents already chosen, on the assumption that similar documents cover similar aspects. MMR is the standard example.
- **Novelty against diversity.** Clarke et al. (Section 1) separate novelty, the need to avoid redundancy, where a document repeats nuggets already seen, from diversity, the need to resolve ambiguity, where the query has several meanings. Near-duplicate pages are the extreme case of redundancy.
- **Fixed set against ranking.** The objective above is for a set of size $k$. A ranking version asks for one order that is good for every prefix, which the greedy methods give by construction.
- **Other lists.** The same problem appears for recommendation lists, news feeds and summaries, with items or sentences in the place of documents.

## Examples

**The probability ranking principle can be wrong.** Take two intents, car with $P = 0.6$ and animal with $P = 0.4$, and three documents:

| document | $V(\cdot \mid \text{car})$ | $V(\cdot \mid \text{animal})$ | $P(\text{relevant})$ |
|---|---|---|---|
| $d_1$ | 0.9 | 0 | 0.54 |
| $d_2$ | 0.8 | 0 | 0.48 |
| $d_3$ | 0 | 0.9 | 0.36 |

The probability ranking principle puts $d_1$ and $d_2$ on top. A user is satisfied by that pair with probability $0.6 \cdot (1 - 0.1 \cdot 0.2) = 0.588$: animal users get nothing, and $d_2$ only helps the few car users whom $d_1$ did not satisfy. The pair $d_1, d_3$ gives $0.6 \cdot 0.9 + 0.4 \cdot 0.9 = 0.90$, which is the optimum for $k = 2$. The ranking that is best document by document is not the best list.

**Coverage with yes or no values.** If every $V$ is 0 or 1 and the intents are equally likely, $P(S \mid q)$ is the number of intents with at least one document in $S$, divided by $m$. The problem is then exactly [maximum coverage](/max-coverage/), with intents as elements and documents as sets.

## Known algorithms

| method | intents | idea | page |
|---|---|---|---|
| exhaustive search | explicit | try all $\binom{n}{k}$ sets, $O\big(\binom{n}{k} k m\big)$ time | |
| maximal marginal relevance (1998) | implicit | add the document with the best relevance minus its largest similarity to the chosen ones | [MMR](/maximal-marginal-relevance/) |
| IA-Select (2009) | explicit | greedy on $P(S \mid q)$, $O(n k m)$ time after sorting | [IA-Select](/ia-select/) |
| xQuAD (2010) | explicit | greedy on a mix of relevance and the coverage of sub-queries | [xQuAD](/xquad/) |

All three named methods are greedy: they build the list one document at a time. Clarke et al. also cite earlier work of Zhai and colleagues on subtopic retrieval with risk minimization, and of Chen and Karger, who treat each chosen document as not relevant and retrieve the next one under that negative feedback.

## Bounds

- **NP-hard.** Finding the best set of size $k$ is [NP-hard](/np-hard/), by the reduction from maximum coverage below (Lemma 1 of Agrawal et al.; Santos et al., Section 2).
- **Greedy is within $1 - 1/e$.** $P(S \mid q)$ is [submodular](/submodular-function/) (Lemma 2 of Agrawal et al.), monotone, and 0 on the empty set. By the [Nemhauser, Wolsey and Fisher theorem](/nemhauser-wolsey-fisher-theorem/), the greedy set reaches at least $1 - (1 - 1/k)^k > 1 - 1/e \approx 0.632$ of the optimum. Agrawal et al. state their Theorem 2 for a submodular function only; the [IA-Select](/ia-select/) page proves the monotonicity that the bound also needs.
- **No better constant.** The reduction from maximum coverage keeps the objective exact, so a polynomial algorithm with a ratio of $1 - 1/e + \varepsilon$ would give the same ratio for maximum coverage, which is NP-hard by [Feige's result](/max-coverage-inapproximability/). This consequence is not stated in the papers above; it follows from the two results.
- **Easy cases.** With one intent, $P(S \mid q) = 1 - \prod_{d \in S}(1 - V(d))$, and the best set is the $k$ documents with the largest $V$, the ranking of the probability ranking principle. When each document serves only one intent, greedy is optimal for every $k$ (Theorem 1 and Corollary 1 of Agrawal et al.).

## Reductions

- **From maximum coverage.** Given elements $u_1, \ldots, u_m$, sets $T_1, \ldots, T_n$ and a number $k$, make one intent per element with $P(c \mid q) = 1/m$, one document per set, and $V(d_j \mid u_i) = 1$ when $u_i \in T_j$ and 0 otherwise. Then $P(S \mid q)$ is the fraction of elements covered by the chosen sets, so an optimal or approximate list is an optimal or approximate cover.
- **To monotone submodular maximization.** Any method for maximizing a monotone submodular function under a size limit $k$ applies, including the plain greedy of [greedy max coverage](/greedy-max-coverage/) and its faster lazy versions.
- **To ranking.** With $m = 1$ the problem is ordinary ranking by $V$, so diversification contains the [probability ranking principle](/probability-ranking-principle/) as a special case.

## Applications

- **Ambiguous and broad web queries.** Short queries such as names and acronyms have several common meanings, and a diversified top ten reduces the chance that a user finds nothing. The methods run as a rerank of the top results of a normal ranker.
- **Evaluation with intents.** [Alpha-nDCG](/alpha-ndcg/) discounts nuggets already seen (Clarke et al.). Agrawal et al. define intent-aware versions of [nDCG](/normalized-discounted-cumulative-gain/), MAP and [MRR](/mean-reciprocal-rank/) that average the measure over intents with the weights $P(c \mid q)$. Santos et al. also report IA-P, an intent-aware form of [precision at k](/precision-at-k/).
- **The TREC 2009 Web track.** Its diversity task has 50 queries, each with official sub-topics, and became the standard benchmark. On it, Santos et al. report that xQuAD raises alpha-nDCG@5 over a BM25 baseline by up to 30%. Such gains are measurements on one collection with one set of sub-topics, and they depend on how well the intents and the values $V$ are estimated.
- **Recommendation and summarization.** A [recommendation](/recommendation-problem/) list or a summary that repeats one item or one sentence many times has the same fault, and MMR was proposed for both document reranking and summaries.

## References
