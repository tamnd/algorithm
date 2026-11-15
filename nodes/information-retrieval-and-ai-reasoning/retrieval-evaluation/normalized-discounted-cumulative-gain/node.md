---
tag: MDZKM4
kind: definition
slug: normalized-discounted-cumulative-gain
name: Normalized discounted cumulative gain
aliases:
- nDCG
- discounted cumulative gain
- DCG
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: core
summary: Sums graded relevance gains discounted by the log of the rank, and divides by the same sum for the ideal ordering.
prereqs: [precision-at-k, test-collection]
see_also: [mean-average-precision, mean-reciprocal-rank, expected-reciprocal-rank, rank-biased-precision, alpha-ndcg, cwl-framework, learning-to-rank, lambdarank]
sources:
  - paper: doi:10.1145/582415.582418
    title: Kalervo Jarvelin and Jaana Kekalainen, Cumulated gain-based evaluation of IR techniques, ACM Transactions on Information Systems 20(4), 2002, pp. 422-446
    locator: Section 2 (cumulated gain, discounted cumulated gain with log base b and no discount before rank b, and the normalized form divided by the ideal vector)
  - paper: doi:10.1145/1102351.1102363
    title: Chris Burges, Tal Shaked, Erin Renshaw, Ari Lazier, Matt Deeds, Nicole Hamilton and Greg Hullender, Learning to rank using gradient descent, ICML 2005, pp. 89-96
    locator: Section 6.1, equation (16) (NDCG at rank 15 with gain 2 to the power r(j) minus 1 and discount log(1+j))
  - url: https://github.com/usnistgov/trec_eval
    title: trec_eval, the TREC evaluation program by Chris Buckley, maintained by NIST
    locator: files m_ndcg.c and m_ndcg_cut.c (gain is the relevance value in the judgments file, discount log2(rank+1), ideal ranking built from the counts of all judged relevance levels, no division when the ideal DCG is 0)
  - paper: doi:10.1007/978-3-540-78646-7_38
    title: Frank McSherry and Marc Najork, Computing information retrieval performance measures efficiently in the presence of tied scores, ECIR 2008, LNCS 4956, pp. 414-421
    locator: tie-aware NDCG, where each position of a tie group gets the mean gain of the group
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 8, Section 8.4 (NDCG)
---

Discounted cumulative gain (DCG) scores a ranking with graded judgments. Each document adds a gain that grows with its grade, divided by a discount that grows with its rank, so a highly relevant document near the top adds the most. Normalized DCG (nDCG) divides DCG by the DCG of the best possible ranking for the query, so the value lies between 0 and 1 and can be averaged over queries. Two gain functions are in common use, and they can order two systems in opposite ways.

## Definition

**Input.** A ranking $d_{(1)}, \ldots, d_{(n)}$ of $n$ distinct document ids for a query, with ranks starting at 1, graded judgments $g(d) \in \{0, 1, 2, \ldots\}$, where a document that is not judged has $g(d) = 0$, and a cutoff $k \ge 1$. Write $g_i = g(d_{(i)})$.

**Gain.** A nondecreasing function $G$ with $G(0) = 0$. There are two standard choices:

- $G(g) = g$. trec_eval uses the relevance values of the judgments file as the gains (files m_ndcg.c and m_ndcg_cut.c).
- $G(g) = 2^g - 1$. Burges et al. (2005, equation 16) use this form. It gives the top grades much more weight: on a scale 0 to 5, grade 5 is worth 31 and grade 1 is worth 1.

The two agree when the grades are only 0 and 1. A report must say which one it uses.

**Discount.** Rank $i$ is divided by $\log_2(i + 1)$. Rank 1 has weight 1, rank 2 has weight $1/\log_2 3 \approx 0.6309$, rank 3 has weight $1/2$.

$$\mathrm{DCG@}k = \sum_{i=1}^{\min(k, n)} \frac{G(g_i)}{\log_2(i + 1)} .$$

**Normalization.** Sort the grades of all judged documents of the query, retrieved or not, in decreasing order to get the ideal list $a_1 \ge a_2 \ge \cdots$, padded with zeros. The ideal DCG is $\mathrm{IDCG@}k = \sum_{i=1}^{k} G(a_i)/\log_2(i + 1)$, and

$$\mathrm{nDCG@}k = \frac{\mathrm{DCG@}k}{\mathrm{IDCG@}k} .$$

The ideal list must come from the judgments. If it comes from the retrieved documents only, a run that misses a highly relevant document is compared with a weaker ideal and scores too high. trec_eval builds the ideal list from the counts of all judged relevance levels.

**Cutoff.** $k$ is part of the name: nDCG@5, nDCG@10. With no cutoff, $k$ is the length of the run, which is the trec_eval measure ndcg. The trec_eval measure ndcg_cut uses the cutoffs 5, 10, 15, 20, 30, 100, 200, 500 and 1000 by default.

**Ties.** Tied scores change DCG when the tied documents have different grades. This area orders by score descending, then by document id ascending. trec_eval orders tied documents by document number in reverse lexical order.

**No relevant documents.** If no judged document has $g \ge 1$, then $\mathrm{IDCG@}k = 0$ and nDCG is undefined. Return None and leave the query out of the mean. trec_eval skips the division in that case, reports 0 and counts the query in its mean.

The mean over queries is the arithmetic mean of nDCG@k over the queries where it is defined. Unnormalized DCG should not be averaged over queries, because a query with many highly relevant documents has a larger DCG for any system.

### The form of Jarvelin and Kekalainen

Jarvelin and Kekalainen (2002, Section 2) define DCG with a parameter $b$: ranks $i < b$ have no discount, and rank $i \ge b$ is divided by $\log_b i$. With $b = 2$, ranks 1 and 2 both have weight 1, and rank 3 has weight $1/\log_2 3$. This is a different form from the one above, though trec_eval cites their paper for its measure. The two forms give different values on the same ranking, as the examples show.

### Properties

**Claim 1.** $0 \le \mathrm{nDCG@}k \le 1$ whenever $\mathrm{IDCG@}k > 0$.

*Proof.* Write $w_i = 1/\log_2(i + 1)$, which is positive and strictly decreasing in $i$. The value is at least 0 because every term is at least 0. For the upper bound, let $h_1, \ldots, h_k$ be the grades at the first $k$ ranks of the run, with $h_i = 0$ for $i > n$.

Step 1. Let $h^*_1 \ge \cdots \ge h^*_k$ be the same grades sorted in decreasing order. Then $\sum_i G(h_i) w_i \le \sum_i G(h^*_i) w_i$. Take any $i < j$ with $G(h_i) < G(h_j)$. Swapping the two grades changes the sum by $(w_i - w_j)(G(h_j) - G(h_i)) > 0$. Each such swap makes the number of out-of-order pairs smaller, so after a finite number of swaps the list is sorted, and the sum has not gone down.

Step 2. $h^*_i \le a_i$ for every $i$. The grades $h_1, \ldots, h_k$ belong to distinct documents, so their nonzero values are some of the grades of the judged documents. The $i$-th largest value of a part of a list is at most the $i$-th largest value of the whole list.

Since $G$ is nondecreasing, $\sum_i G(h^*_i) w_i \le \sum_i G(a_i) w_i = \mathrm{IDCG@}k$. With Step 1, $\mathrm{DCG@}k \le \mathrm{IDCG@}k$. $\square$

This is the exchange argument behind the rearrangement inequality. It uses only that the discount decreases and that $G$ does not decrease, so it holds for both gains.

**Claim 2.** In the form above, the base of the logarithm does not change nDCG.

*Proof.* For a base $c > 1$, $1/\log_c(i + 1) = \ln c / \ln(i + 1)$. So every term of DCG and of IDCG is multiplied by the same constant $\ln c$, and the constant cancels in the ratio. $\square$

So equation 16 of Burges et al., which writes $\log(1 + j)$ with no base, gives the same NDCG as base 2. In the Jarvelin and Kekalainen form the base does matter, because $b$ also decides which ranks have no discount. An example follows.

## Examples and non-examples

### The fixed run on the toy collection

Query q1 "sorted array search" has the judgments d1 grade 2, d2 grade 1 and d8 grade 1. The fixed run ranks 1, 6, 8, 2, 4 with the tie rule of this area, so the grades are 2, 0, 1, 1, 0. The ideal list is 2, 1, 1.

| Rank $i$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Document | d1 | d6 | d8 | d2 | d4 |
| Grade | 2 | 0 | 1 | 1 | 0 |
| $1/\log_2(i+1)$ | 1 | 0.6309 | 0.5 | 0.4307 | 0.3869 |
| Term with $G(g) = g$ | 2 | 0 | 0.5 | 0.4307 | 0 |
| Term with $G(g) = 2^g - 1$ | 3 | 0 | 0.5 | 0.4307 | 0 |

- Gain $g$: $\mathrm{DCG@}5 = 2.9307$ and $\mathrm{IDCG@}5 = 2 + 0.6309 + 0.5 = 3.1309$, so $\mathrm{nDCG@}5 = 0.9360$.
- Gain $2^g - 1$: $\mathrm{DCG@}5 = 3.9307$ and $\mathrm{IDCG@}5 = 3 + 0.6309 + 0.5 = 4.1309$, so $\mathrm{nDCG@}5 = 0.9515$.
- At $k = 3$, $\mathrm{IDCG@}3$ is the same as at $k = 5$, because the ideal list has three nonzero entries. With gain $g$, $\mathrm{nDCG@}3 = 2.5/3.1309 = 0.7985$. With gain $2^g - 1$, it is $3.5/4.1309 = 0.8473$.

A run that ranks 1, 2, 8, 7, 4 puts the grades in the order 2, 1, 1, 0, 0 and has nDCG 1 at every cutoff, with both gains.

### The ideal list from the wrong place

If the ideal list at $k = 3$ is built from the first three retrieved documents only, its grades are 2, 1, 0 and its DCG is $2 + 0.6309 = 2.6309$. The run then scores $2.5/2.6309 = 0.9502$ instead of 0.7985, because d2, which the run ranks 4th, is no longer in the ideal.

### Ties change nDCG

trec_eval reads the same scores as the order 6, 1, 8, 4, 2. Then $\mathrm{nDCG@}5$ is 0.6863 with gain $g$ and 0.6729 with gain $2^g - 1$, and $\mathrm{nDCG@}3$ is 0.5627 and 0.5792. The tie-aware value of McSherry and Najork (2008) is the mean over the four orders of the tied documents. Because DCG is a sum of gain times weight, the mean is the same as giving each position of a tie group the mean gain of the group. With gain $g$, the gains become 1, 1, 1, 0.5, 0.5, and $\mathrm{nDCG@}5 = 0.8112$. With gain $2^g - 1$ they become 1.5, 1.5, 1, 0.5, 0.5, and $\mathrm{nDCG@}5 = 0.8122$.

### The gain can reverse a comparison

Take two rankings of length 3 for q1: X ranks d2, d1, d3 (grades 1, 2, 0), and Y ranks d1, d3, d4 (grades 2, 0, 0).

| Ranking | nDCG@3, gain $g$ | nDCG@3, gain $2^g - 1$ |
|---|---|---|
| X | $(1 + 2 \cdot 0.6309)/3.1309 = 0.7224$ | $(1 + 3 \cdot 0.6309)/4.1309 = 0.7003$ |
| Y | $2/3.1309 = 0.6388$ | $3/4.1309 = 0.7262$ |

With gain $g$, X is better. With gain $2^g - 1$, Y is better: its grade 2 document at rank 1 adds 3, while X gets only $1 + 3 \cdot 0.6309 = 2.8928$ from a grade 1 document at rank 1 and a grade 2 document at rank 2.

### The Jarvelin and Kekalainen form

With $b = 2$, the fixed run has DCG $2 + 0 + 1/\log_2 3 + 1/\log_2 4 = 3.1309$ and the ideal 2, 1, 1 has DCG $2 + 1 + 1/\log_2 3 = 3.6309$, so the normalized value is $0.8623$, not 0.9360. With $b = 10$, ranks 1 to 9 have no discount, the run and the ideal both sum to 4, and the value is 1. The base changes the value in this form.

### Query q4

q4 "quantum circuit" has no relevant document. The ideal list is empty, $\mathrm{IDCG@}k = 0$, and nDCG is None.

### Non-examples

- Mean unnormalized DCG over queries. It mixes queries with different ideal values.
- [Alpha-nDCG](/alpha-ndcg/). It changes the gain so that a document that repeats a subtopic already covered higher in the ranking is worth less. It measures diversity, not graded relevance alone.
- [Average precision](/mean-average-precision/), which uses binary relevance and normalizes by $R$, not by an ideal ranking.

## Related definitions

- [Expected reciprocal rank](/expected-reciprocal-rank/) and [rank-biased precision](/rank-biased-precision/) also weight ranks, but from a model of when the user stops. The [CWL framework](/cwl-framework/) describes all of them with one user model.
- [LambdaRank](/lambdarank/) and other methods of [learning to rank](/learning-to-rank/) train directly towards nDCG, usually with the gain $2^g - 1$.
- [Precision at k](/precision-at-k/) is the special case of DCG@k with binary gains and the flat weight $1/k$ in place of the log discount.

Claims 1 and 2 are proved and hold for every ranking. Which gain and which cutoff agree best with users is a question of measurement, and the gain-flip example shows that the choice can decide which system wins. A claim that one system has a higher mean nDCG than another needs a paired test over the queries, such as the [Wilcoxon signed-rank test](/wilcoxon-signed-rank-test/), a [permutation test](/permutation-test/) or a [bootstrap interval](/bootstrap-percentile-interval/).

## References
