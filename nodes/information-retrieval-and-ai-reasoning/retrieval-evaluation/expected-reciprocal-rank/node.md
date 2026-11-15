---
tag: 6HQRSF
kind: definition
slug: expected-reciprocal-rank
name: Expected reciprocal rank
aliases:
- ERR
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: advanced
summary: The expected value of 1/r for the rank r where a cascade user stops, each document satisfying with a probability set by its grade.
prereqs: [mean-reciprocal-rank, normalized-discounted-cumulative-gain, expected-value]
see_also: [rank-biased-precision, cwl-framework, cascade-click-model, dbn-click-model, alpha-ndcg, mean-average-precision, interleaved-evaluation]
sources:
  - paper: doi:10.1145/1645953.1646033
    title: Olivier Chapelle, Donald Metzler, Ya Zhang and Pierre Grinspan, Expected reciprocal rank for graded relevance, CIKM 2009, pp. 621-630
    locator: the cascade user model, the satisfaction probability (2^g - 1)/2^gmax, the definition of ERR as the expected reciprocal of the stop rank, its linear-time computation and the comparison with click metrics
  - paper: doi:10.1145/1341531.1341545
    title: Nick Craswell, Onno Zoeter, Michael Taylor and Bill Ramsey, An experimental comparison of click position-bias models, WSDM 2008, pp. 87-94
    locator: the cascade model, in which the user reads the results from the top and stops after the first click
  - paper: doi:10.1145/3471158.3472239
    title: Leif Azzopardi, Joel Mackenzie and Alistair Moffat, ERR is not C/W/L, ICTIR 2021
    locator: the relation of ERR to the C/W/L framework of user models
---

Expected reciprocal rank (ERR) scores a ranking with graded judgments by a model of a user who reads the results from the top. At each rank the user is satisfied with a probability that grows with the grade of the document, and stops there; otherwise the user goes on to the next rank. ERR is the expected value of $1/r$, where $r$ is the rank at which the user stops, and a user who never stops counts 0. Chapelle, Metzler, Zhang and Grinspan defined it in 2009 from the cascade click model. The main difference from [nDCG](/normalized-discounted-cumulative-gain/) is that the worth of a document depends on the documents above it: a relevant document below a highly relevant one adds little, because most users have already stopped.

## Definition

**Input.** A ranking $d_{(1)}, \ldots, d_{(n)}$ of distinct documents for a query, with ranks from 1, graded judgments $g(d) \in \{0, 1, \ldots, g_{\max}\}$, where a document that is not judged has grade 0, and an optional cutoff $k$. The maximum grade $g_{\max}$ is the top of the judgment scale of the collection, not the highest grade that occurs for the query. Write $g_i = g(d_{(i)})$.

**Satisfaction probability.** The probability that the document at rank $i$ satisfies the user is

$$R_i = \frac{2^{g_i} - 1}{2^{g_{\max}}} .$$

So $R_i = 0$ for grade 0, and $R_i = 1 - 2^{-g_{\max}} < 1$ for the top grade. Any nondecreasing map from grades to $[0, 1]$ with $R = 0$ at grade 0 gives a member of the same family. This is the form of Chapelle et al.

**The user.** The user examines rank 1. At each examined rank $i$, the user is satisfied and stops with probability $R_i$, and goes on to rank $i + 1$ with probability $1 - R_i$, independent of the other ranks. The user reaches rank $r$ with probability $E_r = \prod_{i < r} (1 - R_i)$ and stops there with probability $E_r R_r$.

**The measure.**

$$\mathrm{ERR@}k = \sum_{r=1}^{\min(k, n)} \frac{1}{r} \, R_r \prod_{i=1}^{r-1} (1 - R_i) .$$

With no cutoff, $k = n$. A user who reaches the end of the list without being satisfied adds 0.

**Computation.** One pass from the top keeps $E$, the probability of reaching the current rank:

$$E \leftarrow 1, \quad \mathrm{ERR} \leftarrow 0; \quad \text{for } r = 1, \ldots, \min(k, n): \ \mathrm{ERR} \leftarrow \mathrm{ERR} + E R_r / r, \ \ E \leftarrow E (1 - R_r) .$$

This takes $O(\min(k, n))$ time and $O(1)$ extra space. The direct form with the product inside the sum takes quadratic time.

**No relevant documents.** ERR has no normalization, so a query with no relevant document has ERR 0, and the value is defined. Compare nDCG, which is undefined in that case.

**Ties.** As for every measure that reads ranks, tied scores must be broken by a fixed rule before ERR is computed. This area orders by score descending, then by document id ascending. trec_eval orders tied documents by document number in reverse lexical order.

### Properties

**Claim 1.** $0 \le \mathrm{ERR@}k \le 1 - \prod_{i \le \min(k, n)} (1 - R_i) < 1$.

*Proof.* The stop events at ranks $1, \ldots, \min(k, n)$ are disjoint, and their probabilities $E_r R_r$ sum to $1 - \prod_{i \le \min(k,n)} (1 - R_i)$, the probability that the user stops at some rank. Each term of ERR is that probability times $1/r \le 1$. Each $R_i < 1$, so the bound is less than 1. $\square$

So ERR never reaches 1, not even for a perfect ranking. The best value for a query depends on its judgments, which is why ERR is often reported next to a normalized measure.

**Claim 2.** The ranking that sorts the judged documents by grade, highest first, has the largest ERR@k among all rankings of documents of the collection.

*Proof.* First, raising one $R_i$ does not lower ERR. Write $\mathrm{ERR} = A + E_i (R_i / i + (1 - R_i) T)$, where $A$ is the sum of the terms above rank $i$ and $T = \sum_{r > i} (R_r / r) \prod_{i < j < r} (1 - R_j)$. Neither $A$, $E_i$ nor $T$ depends on $R_i$, and $T \le 1/(i + 1) < 1/i$ by the argument of Claim 1, so ERR grows with $R_i$. So the $\min(k, n)$ ranks are best filled with the documents of the highest grades. Next, take adjacent ranks $i$ and $i + 1$ with satisfaction probabilities $a$ and $b$, and let $E$ be the probability of reaching rank $i$. The two ranks add $E(a/i + (1 - a) b/(i + 1))$ in one order and $E(b/i + (1 - b) a/(i + 1))$ in the other. The difference is $E(a - b)(1/i - 1/(i + 1))$, which is at least 0 when $a \ge b$. The probability $(1 - a)(1 - b)$ of going past both ranks does not depend on the order, so the ranks below do not change. A ranking that is not sorted has an adjacent pair with $a < b$, and swapping it does not lower ERR. A finite number of such swaps sorts the list. $\square$

**Claim 3.** If $R_i = 1$ for every relevant document, then ERR is the reciprocal rank of the first relevant document.

*Proof.* Then $E_r = 0$ for every rank below the first relevant document $r_1$, $E_{r_1} = 1$ and $R_{r_1} = 1$, so the sum has one nonzero term, $1/r_1$. $\square$

The standard form never has $R = 1$, so ERR on binary judgments is not [reciprocal rank](/mean-reciprocal-rank/). With $g_{\max} = 1$, a relevant document stops only half of the users who reach it.

## Examples and non-examples

### The fixed run on the toy collection

Query q1 "sorted array search" has the judgments d1 grade 2, d2 grade 1 and d8 grade 1, on a scale with $g_{\max} = 2$. The fixed run ranks 1, 6, 8, 2, 4 with the tie rule of this area, so the grades are 2, 0, 1, 1, 0 and the satisfaction probabilities are $3/4, 0, 1/4, 1/4, 0$.

| Rank $r$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Document | d1 | d6 | d8 | d2 | d4 |
| $R_r$ | 0.75 | 0 | 0.25 | 0.25 | 0 |
| $E_r$, reach rank $r$ | 1 | 0.25 | 0.25 | 0.1875 | 0.140625 |
| $E_r R_r$, stop at $r$ | 0.75 | 0 | 0.0625 | 0.046875 | 0 |
| $E_r R_r / r$ | 0.75 | 0 | 0.020833 | 0.011719 | 0 |

So $\mathrm{ERR} = 601/768 = 0.78255$. With probability $9/64 = 0.140625$ the user is never satisfied. At cutoff 3, $\mathrm{ERR@}3 = 0.770833$.

The ideal ranking puts the grades in the order 2, 1, 1. Its ERR is $0.75 + 0.03125 + 0.015625 = 0.796875$. So the run is close to the best possible value for q1, and the ratio of the two is $0.98203$.

### Ties change ERR

trec_eval reads the same scores as the order 6, 1, 8, 4, 2, with grades 0, 2, 1, 0, 1. Then $\mathrm{ERR} = 0.75/2 + 0.25 \cdot 0.25/3 + 0.25 \cdot 0.25 \cdot 0.75/5 = 0.40521$. The tie between d1 and d6 at rank 1 halves the value, because d1, which satisfies most users, moves to rank 2.

### The documents above matter

The ranking 6, 4, 8 has only d8 relevant, at rank 3, and $\mathrm{ERR} = 0.25/3 = 0.08333$. In the fixed run, d8 is also at rank 3 but adds only $0.020833$, because d1 at rank 1 has already satisfied three quarters of the users. In nDCG, a grade 1 document at rank 3 adds the same amount in both rankings.

### Binary judgments

If q1 is judged on a binary scale, so that d1, d2 and d8 have grade 1 and $g_{\max} = 1$, then every relevant document has $R = 1/2$. The fixed run gets $0.5 + 0.5 \cdot 0.5/3 + 0.5 \cdot 0.5 \cdot 0.5/4 = 0.61458$, not the reciprocal rank 1.

### Query q4

q4 "quantum circuit" has no relevant document. Every $R_i$ is 0, and ERR is 0.

### Non-examples

- ERR with $g_{\max}$ taken per query. If a query has grades up to 1 on a scale up to 2, setting $g_{\max} = 1$ for that query lets each relevant document stop half of the users instead of a quarter, and values of different queries can no longer be compared.
- The expected reciprocal rank of the first relevant document under a random tie order. That is a tie-aware form of reciprocal rank, not ERR.
- [Rank-biased precision](/rank-biased-precision/). Its user goes on with a fixed probability $p$ that does not depend on the documents.

## Related definitions

- The user model is the [cascade click model](/cascade-click-model/) of Craswell et al., in which the user reads from the top and stops at the first click, with the click replaced by satisfaction. The [DBN click model](/dbn-click-model/) also has a probability of satisfaction after a click, but learns it from logs instead of setting it from the grade.
- [Rank-biased precision](/rank-biased-precision/) and [nDCG](/normalized-discounted-cumulative-gain/) give each rank a weight that does not depend on the other documents. ERR gives rank $r$ the weight $E_r / r$, which falls faster below a highly relevant document.
- In the [C/W/L framework](/cwl-framework/), set the continuation probability at rank $i$ to $C(i) = (1 - R_i) \cdot i/(i + 1)$. Then $\prod_{j < i} C(j) = E_i / i$, and the expected total gain $\sum_i R_i \prod_{j < i} C(j)$ is ERR. The C/W/L framework reports the expected rate of gain per document, which is this total divided by the expected depth, so that value is not ERR. Azzopardi, Mackenzie and Moffat (2021) study the relation in a paper titled "ERR is not C/W/L".
- Averaging ERR over the subtopics of a query, each weighted by its probability, gives an intent-aware form for diversity. [Alpha-nDCG](/alpha-ndcg/) is another measure of diversity, built on nDCG.
- In [average precision](/mean-average-precision/), the term of a relevant document is the precision at its rank, which grows with the relevant documents above it. In ERR, the worth of a document falls with the relevant documents above it.

Claims 1 to 3 are proved and hold for every ranking. That ERR agrees with user behaviour better than other measures is a measured result, not a theorem: Chapelle et al. report that it correlates better with click metrics than the other editorial metrics they test. A claim that one system has a higher mean ERR than another needs a paired test over the queries, such as the [Wilcoxon signed-rank test](/wilcoxon-signed-rank-test/) or a [permutation test](/permutation-test/).

## References
