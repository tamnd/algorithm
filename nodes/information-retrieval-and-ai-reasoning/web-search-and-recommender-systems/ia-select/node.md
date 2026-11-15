---
tag: PXB2Y2
kind: algorithm
slug: ia-select
name: IA-Select
aliases:
- intent-aware select
- intent-aware diversification
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: research
summary: Greedily picks documents that maximize the probability that each query intent is satisfied by at least one result; a (1 - 1/e) approximation.
solves: [search-result-diversification]
model: word-ram
complexity:
  vars: {n: the number of candidate documents, k: the number of results, m: the number of intents}
  time: {worst: O(n log n + n k m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 2009
  people: [Rakesh Agrawal, Sreenivas Gollapudi, Alan Halverson, Samuel Ieong]
  note: Agrawal, Gollapudi, Halverson and Ieong defined the intent-aware objective at WSDM 2009, proved it NP-hard and submodular, and gave the greedy IA-Select with its (1 - 1/e) bound and the intent-aware evaluation measures.
prereqs: [search-result-diversification, submodular-function, nemhauser-wolsey-fisher-theorem]
see_also: [xquad, maximal-marginal-relevance, greedy-max-coverage, max-coverage, max-coverage-inapproximability, probability-ranking-principle, alpha-ndcg, normalized-discounted-cumulative-gain]
sources:
  - paper: doi:10.1145/1498759.1498766
    title: Rakesh Agrawal, Sreenivas Gollapudi, Alan Halverson and Samuel Ieong, Diversifying search results, Proceedings of the Second ACM International Conference on Web Search and Data Mining (WSDM 2009), 5-14
    locator: Section 3 (Equation 1, the objective P(S | q)), Section 3.3 (Lemma 1, NP-hardness from Max Coverage, and the instance of Table 1), Section 3.4 (Lemma 2, submodularity), Section 3.5 (Algorithm 1, IA-Select), Section 3.6 (Theorem 1 and Corollary 1, optimality with one category per document; Theorem 2 and Corollary 2, the (1 - 1/e) bound), Section 3.7 (a worked example), Section 4 (NDCG-IA, MAP-IA and MRR-IA)
  - paper: "George L. Nemhauser, Laurence A. Wolsey and Marshall L. Fisher, An analysis of approximations for maximizing submodular set functions, I, Mathematical Programming 14, 265-294, 1978"
    locator: the bound 1 - (1 - 1/k)^k for the greedy algorithm on a monotone submodular function with f of the empty set equal to 0, under the constraint of at most k elements
  - paper: doi:10.1145/1772690.1772780
    title: Rodrygo L. T. Santos, Craig Macdonald and Iadh Ounis, Exploiting query reformulations for web search result diversification, Proceedings of the 19th International Conference on World Wide Web (WWW 2010), 881-890
    locator: Section 2 (the approach of Agrawal et al. as explicit diversification with a taxonomy), Section 5 (a simulated best case of IA-Select with the official TREC 2009 Web track sub-topics as classes) and Section 6 (Table 2, IA-Select as a baseline)
---

IA-Select is a greedy algorithm for [search result diversification](/search-result-diversification/) that builds a result list one document at a time, each time adding the document that most increases the probability that the user finds at least one satisfying result. Rakesh Agrawal, Sreenivas Gollapudi, Alan Halverson and Samuel Ieong introduced it in 2009 with a distribution over the intents (categories) of the query. The objective is [submodular](/submodular-function/), so the [Nemhauser, Wolsey and Fisher theorem](/nemhauser-wolsey-fisher-theorem/) makes the greedy list at least $1 - 1/e$ of the optimum. Unlike [maximal marginal relevance](/maximal-marginal-relevance/), which only compares documents with each other, IA-Select models the intents explicitly; [xQuAD](/xquad/) uses the same coverage term but mixes it with plain relevance.

## In plain words

A short query such as "jaguar" can mean a car, an animal or a football team. A list of ten car pages is perfect for some users and useless for the rest. IA-Select knows roughly how many users mean each thing, and how well each page serves each meaning. It picks the page that helps the most users first. After that, the users who are already served count for less, so the next page is the one that helps most of the users who are still waiting. Repeating this gives a list where popular meanings come first, but rare meanings still get a page before a popular meaning gets its fifth. The list is never far from the best possible list, and the method can prove how far.

## The problem

The input is a query $q$, a set $D$ of $n$ candidate documents, a set $C$ of $m$ categories with probabilities $P(c \mid q)$ that sum to 1, a value $V(d \mid q, c) \in [0, 1]$ for each document and category, and a length $k$. The value is the probability that $d$ satisfies a user whose intent is $c$; it is $0$ when $d$ does not belong to $c$. The users are assumed to have one intent each, and given the intent, the documents satisfy them independently. The probability that a set $S$ satisfies the user is

$$P(S \mid q) = \sum_{c \in C} P(c \mid q) \Big(1 - \prod_{d \in S} \big(1 - V(d \mid q, c)\big)\Big),$$

and the task is to find $S$ with $|S| = k$ that maximizes it. Agrawal et al. prove that this is [NP-hard](/np-hard/) by a reduction from [maximum coverage](/max-coverage/): with uniform $P(c \mid q)$ and values $0$ or $1$, $P(S \mid q)$ is the fraction of the categories that $S$ covers.

## The algorithm

IA-Select keeps $U(c)$, the probability that the intent is $c$ and no chosen document satisfies it. The gain of a document is the expected number of these still unsatisfied users that it satisfies:

```pseudo id=main
IA-SELECT(D, P, V, k)
L1  for each category c: U(c) ← P(c | q)
L2  S ← empty list
L3  while some document is not in S and |S| < k:
L4      for each d not in S, in id order:
L5          g(d) ← Σ over c of U(c) · V(d | q, c)
L6      b ← the d with the largest g(d), ties to the smaller id; append b to S
L7      for each category c of b:
L8          U(c) ← (1 − V(b | q, c)) · U(c)
L9  return S
```

The paper calls $U(c)$ "the conditional probability" that the intent is $c$ given that the documents so far failed, but line L8 does not renormalize it, and the analysis needs the unnormalized form: $U(c)$ is a joint probability, and the gain of line L5 is then the exact increase of $P(S \mid q)$.

## Example

Table 1 of the paper has two equally likely intents and three documents:

| doc | $V(\cdot \mid c_1)$ | $V(\cdot \mid c_2)$ |
|---|---|---|
| d1 | 0.8 | 0.8 |
| d2 | 1 | 0 |
| d3 | 0 | 1 |

| step | $U(c_1)$ | $U(c_2)$ | g(d1) | g(d2) | g(d3) | pick | $P(S \mid q)$ |
|---|---|---|---|---|---|---|---|
| 1 | 0.5 | 0.5 | 0.8 | 0.5 | 0.5 | d1 | 0.8 |
| 2 | 0.1 | 0.1 | | 0.1 | 0.1 | d2 | 0.9 |
| 3 | 0 | 0.1 | | | 0.1 | d3 | 1.0 |

For $k = 1$ the greedy choice d1 is optimal. For $k = 2$ the greedy list d1, d2 has value $0.9$, while d2 and d3 together reach $1.0$. So no single ordering is optimal for every $k$, and the greedy result can be below the optimum. The loss here, $0.9$ against $1.0$, is well inside the bound $1 - 1/e \approx 0.632$. Section 3.7 of the paper works a larger example with intents of probability $0.7$ and $0.3$ over ten documents.

## Correctness

The file proofs/correctness.md proves the guarantees. Line L8 keeps the invariant $U(c) = P(c \mid q) \prod_{d \in S} (1 - V(d \mid q, c))$, so the gain of line L5 equals $P(S \cup \{d\} \mid q) - P(S \mid q)$. The marginal gain is a sum of products of numbers in $[0, 1]$, and adding documents only adds factors, so the objective is monotone and submodular, with value $0$ on the empty set. The theorem of Nemhauser, Wolsey and Fisher then gives

$$P(S_{\text{greedy}} \mid q) \ge \Big(1 - \big(1 - \tfrac{1}{k}\big)^k\Big) \max_{|S| = k} P(S \mid q) \ge \Big(1 - \frac{1}{e}\Big) \max_{|S| = k} P(S \mid q).$$

The paper's Theorem 2 states this for "a submodular set function"; the bound also needs monotonicity and $f(\emptyset) = 0$, which this objective has. When each document belongs to only one category, IA-Select is optimal for every $k$ (Theorem 1 of the paper). The reduction from maximum coverage and the [max coverage inapproximability](/max-coverage-inapproximability/) result mean that no polynomial-time algorithm can guarantee a better constant unless P = NP.

## Complexity

Each of the at most $k$ passes computes $n$ gains, each a sum over the categories of a document, and updates at most $m$ values of $U$. With at most $m$ categories per document the time is $O(n \log n + nkm)$, including the sort of the ids, and with sparse values it is $O(n \log n + ke)$, where $e$ is the number of nonzero values. The extra space is $O(n + m)$. Lazy evaluation with a [priority queue](/priority-queue/) of stale gains, which is valid for any submodular objective, usually cuts the number of gain computations a lot.

## Properties

- **Explicit.** It needs a set of intents, their probabilities and per-intent values, for example from a query classifier and per-intent relevance scores.
- **Monotone submodular objective.** Every pick has a non-negative gain, and the gain of a document never grows as the list grows.
- **Approximation.** At least $1 - 1/e$ of the optimum for every $k$, and optimal when each document has one category.
- **Not a ranking by relevance.** Once an intent is well served, its documents drop in gain, so a highly relevant document can fall below a weaker document of another intent. This breaks the assumptions of the [probability ranking principle](/probability-ranking-principle/) on purpose.
- **Deterministic.** The tie rule fixes the output.

## Variants and improvements

- **Intent-aware measures.** The same paper defines NDCG-IA, MAP-IA and MRR-IA: a measure is computed for each intent with the judgments of that intent and averaged with the weights $P(c \mid q)$. See [nDCG](/normalized-discounted-cumulative-gain/) and [mean reciprocal rank](/mean-reciprocal-rank/) for the base measures, and [alpha-nDCG](/alpha-ndcg/) for a related measure of novelty and coverage.
- **xQuAD.** [xQuAD](/xquad/) adds the relevance $P(d \mid q)$ to the same coverage term, with a weight $\lambda$, and takes its aspects from query reformulations.
- **Max coverage.** With values $0$ and $1$, IA-Select is [greedy max coverage](/greedy-max-coverage/) with weights on the elements.
- **Ranked lists.** The objective ignores the order inside $S$. For a ranking, one runs the loop with $k$ equal to the length of the list and uses the order of the picks, which is what the test collections evaluate.

## When to use it

Use IA-Select when you have a taxonomy of intents and a classifier that gives each query a distribution over them, and when you want to maximize the chance that every likely intent finds a good result near the top. If the intents come from query reformulations, or if you want to keep more of the first ranking, [xQuAD](/xquad/) is the closer fit; if you have no intents at all, [MMR](/maximal-marginal-relevance/) needs only a similarity function. The gains reported for IA-Select in the paper and in later comparisons are measurements on particular data sets and intent models.

## Pitfalls

- **The values must be probabilities.** The guarantee and the meaning of $U$ need $V(d \mid q, c) \in [0, 1]$. Raw retrieval scores such as BM25 must be calibrated or normalized first. The implementation rejects values outside the range.
- **A bad intent distribution.** If $P(c \mid q)$ is wrong, the algorithm faithfully optimizes the wrong objective. A rare but missing intent gets no document at all.
- **Value 1 stops an intent.** A document with $V = 1$ for an intent sets $U(c)$ to 0, and no further document of that intent can gain anything. Clipping values below 1 keeps some redundancy.
- **Do not renormalize U.** Dividing $U$ by its sum after each step looks natural, since the paper calls it a conditional probability, but it changes the gains and loses the link to the objective.
- **The bound is on the objective.** The $1 - 1/e$ guarantee is about $P(S \mid q)$ under the model, not about measured user satisfaction.

## Implementations

## History

Agrawal, Gollapudi, Halverson and Ieong presented the problem and IA-Select at WSDM 2009 under the title "Diversifying search results". They framed diversification as maximizing the probability that the average user finds at least one useful result, proved the problem NP-hard, showed that the objective is submodular, and applied the 1978 greedy bound of Nemhauser, Wolsey and Fisher. They also defined intent-aware versions of the standard measures. The paper became a reference point for explicit diversification, and xQuAD in 2010 built on the same coverage term.

## References
