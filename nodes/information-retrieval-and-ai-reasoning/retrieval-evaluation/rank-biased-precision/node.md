---
tag: 56MWH6
kind: definition
slug: rank-biased-precision
name: Rank-biased precision
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: advanced
summary: The expected rate of relevant documents seen by a user who goes on from each rank with persistence probability p.
prereqs: [precision-at-k, geometric-distribution]
see_also: [expected-reciprocal-rank, cwl-framework, normalized-discounted-cumulative-gain, pooling, bpref, inferred-average-precision, test-collection]
sources:
  - paper: doi:10.1145/1416950.1416952
    title: Alistair Moffat and Justin Zobel, Rank-biased precision for measurement of retrieval effectiveness, ACM Transactions on Information Systems 27(1), Article 2, 2008, pp. 2:1-2:27
    locator: the user model with persistence p, the definition of RBP, and the residual that bounds the effect of documents that are not judged or not ranked
  - paper: doi:10.1145/3331184.3331398
    title: Leif Azzopardi, Paul Thomas and Alistair Moffat, cwl_eval, an evaluation tool for information retrieval, SIGIR 2019, pp. 1321-1324
    locator: RBP as a C/W/L metric with a continuation probability that does not depend on the gain, and the values for RBP with p = 0.6 on the example topic in Table 2
---

Rank-biased precision (RBP) scores a ranking by a model of a user who always looks at the first document and then, after each document, goes on to the next one with a fixed probability $p$, called the persistence. RBP is the expected number of relevant documents the user sees, divided by the expected number of documents the user looks at, which is $1/(1 - p)$. Moffat and Zobel proposed it in 2008. It has two features that most measures lack: it does not need the number of relevant documents of the query, and when some documents are not judged it gives a bound, the residual, on how much the value could still change.

## Definition

**Input.** A ranking $d_{(1)}, d_{(2)}, \ldots$ of distinct documents, judgments that give each document a gain $r(d) \in [0, 1]$, and the persistence $0 < p < 1$. With binary judgments, $r$ is 1 for a relevant document and 0 otherwise. Graded judgments fit by a gain such as $g/g_{\max}$. A document that is not judged has gain 0 in the base value. Write $r_i = r(d_{(i)})$, and let the run have $n$ documents.

**The user.** The user examines rank 1. After examining rank $i$, the user goes on to rank $i + 1$ with probability $p$ and stops with probability $1 - p$. So the user examines rank $i$ with probability $p^{i - 1}$, and the number of documents examined has a [geometric distribution](/geometric-distribution/) with mean $1/(1 - p)$. A user who goes past the end of the run sees nothing more.

**The measure.**

$$\mathrm{RBP}(p) = (1 - p) \sum_{i=1}^{n} r_i \, p^{i - 1} .$$

The weight of rank $i$ is $(1 - p) p^{i - 1}$. The weights of all ranks sum to 1, and the weight of a rank does not depend on the documents at other ranks.

**Residual.** Let the run be judged to depth $d$, with $U$ the set of ranks $i \le d$ whose documents are not judged. The ranks in $U$ and the ranks below $d$ can add at most

$$\mathrm{res} = (1 - p) \sum_{i \in U} p^{i - 1} + p^d .$$

So the true value lies in $[\mathrm{RBP}, \mathrm{RBP} + \mathrm{res}]$, and RBP is reported as a base value and a residual. If the run ends at rank $n \le d$, the term $p^d$ is replaced by 0, since there are no more documents to judge.

**Choice of $p$.** The persistence fixes how deep the user reads: $p = 0.5$ gives an expected depth of 2, $p = 0.8$ gives 5 and $p = 0.95$ gives 20. A report must give $p$, because values with different $p$ cannot be compared.

**No relevant documents.** RBP has no normalization, so a query with no relevant document has RBP 0, and the value is defined.

**Ties.** Tied scores must be broken by a fixed rule before RBP is computed. This area orders by score descending, then by document id ascending. trec_eval orders tied documents by document number in reverse lexical order.

### Properties

**Claim 1.** $\mathrm{RBP}(p) = \mathbb{E}[\text{gain seen}] \,/\, \mathbb{E}[\text{documents examined}]$, where the user stops after rank $D$ with $\Pr[D = i] = (1 - p) p^{i - 1}$.

*Proof.* The user sees rank $j$ exactly when $D \ge j$, which has probability $p^{j - 1}$. So the expected gain seen is $\sum_j r_j p^{j - 1}$, and $\mathbb{E}[D] = \sum_{j \ge 1} p^{j - 1} = 1/(1 - p)$. Their ratio is RBP. $\square$

This is a ratio of expected values. The expected precision at the stop depth, $\mathbb{E}[\sum_{j \le D} r_j / D]$, is a different number, as the examples show.

**Claim 2.** $0 \le \mathrm{RBP}(p) \le 1 - p^n < 1$, and the upper bound is reached when all $n$ documents have gain 1.

*Proof.* Each gain is in $[0, 1]$, so the sum is between 0 and $(1 - p) \sum_{i=1}^{n} p^{i - 1} = 1 - p^n$. $\square$

**Claim 3.** For every assignment of gains in $[0, 1]$ to the unjudged documents and to documents below depth $d$, the value lies between RBP and RBP plus the residual.

*Proof.* Each of these documents adds $(1 - p) r_i p^{i - 1}$ with $r_i \in [0, 1]$, so it adds at least 0 and at most $(1 - p) p^{i - 1}$. The ranks below $d$ add at most $(1 - p) \sum_{i > d} p^{i - 1} = p^d$. $\square$

## Examples and non-examples

### The fixed run on the toy collection

Query q1 "sorted array search" has the judgments d1 grade 2, d2 grade 1 and d8 grade 1. With the gain $g/2$ and the tie rule of this area, the fixed run 1, 6, 8, 2, 4 has gains 1, 0, 0.5, 0.5, 0.

| Rank $i$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Document | d1 | d6 | d8 | d2 | d4 |
| Gain $r_i$ | 1 | 0 | 0.5 | 0.5 | 0 |
| Weight at $p = 0.8$ | 0.2 | 0.16 | 0.128 | 0.1024 | 0.08192 |
| Term | 0.2 | 0 | 0.064 | 0.0512 | 0 |

So $\mathrm{RBP}(0.8) = 0.3152$. For other values of $p$: $\mathrm{RBP}(0.5) = 0.59375$ and $\mathrm{RBP}(0.95) = 0.0940$. A shallow user gives most of the weight to d1 at rank 1; a deep user spreads it over many ranks, and the run has only five documents.

With binary gains, so that d1, d2 and d8 have gain 1, $\mathrm{RBP}(0.8) = 0.2 (1 + 0.64 + 0.512) = 0.4304$.

### Ties change RBP

trec_eval reads the same scores as the order 6, 1, 8, 4, 2, with gains 0, 1, 0.5, 0, 0.5. Then $\mathrm{RBP}(0.8) = 0.2 (0.8 + 0.32 + 0.2048) = 0.26496$.

### The residual

Say the run goes on below rank 5 with documents that are not judged. With all five top documents judged, the residual at $p = 0.8$ is $0.8^5 = 0.32768$, so the true value is in $[0.3152, 0.6429]$. If d6 at rank 2 and d4 at rank 5 are also not judged, the residual is $0.2 (0.8 + 0.4096) + 0.32768 = 0.5696$, and the value is in $[0.3152, 0.8848]$. At $p = 0.95$ the residual for depth 5 is $0.95^5 = 0.7738$, much larger than the base 0.0940, so a deep user needs judgments much deeper than 5.

### Rate, not expected precision

For the fixed run at $p = 0.8$, the expected precision at the stop depth is $\sum_i (1 - p) p^{i - 1} \cdot (\text{gain in the top } i)/i = 0.5034$, while RBP is 0.3152. The first is the mean of a ratio, RBP is a ratio of means.

### The best value depends on the query

Query q3 "rank documents" has one relevant document, d7, with grade 2 and gain 1. The best ranking puts d7 first and has $\mathrm{RBP}(0.8) = 0.2$. A query with many relevant documents can score close to 1. RBP is an absolute measure of what the user gets, not a fraction of the best possible value, so values of different queries mean different things.

### Query q4

q4 "quantum circuit" has no relevant document, and $\mathrm{RBP} = 0$ for every run.

### Non-examples

- RBP with judgments only to depth $d$ and no residual. The base value treats every document that is not judged as not relevant, which favours runs that retrieve the judged documents, such as the runs that formed the [pool](/pooling/).
- $\mathrm{RBP}$ divided by its value for the ideal ranking. This normalized form needs the gains of all relevant documents, so it loses the property that RBP does not depend on them.

## Related definitions

- [Precision at k](/precision-at-k/) gives the first $k$ ranks the weight $1/k$ each and the others 0. RBP replaces the step by a geometric decay.
- [Expected reciprocal rank](/expected-reciprocal-rank/) has a stop probability that depends on the document. In RBP the user goes on with the same $p$ at every rank.
- In the [C/W/L framework](/cwl-framework/), RBP is the metric whose continuation probability is $C(i) = p$ at every rank, which does not depend on the gain. Its expected depth is $1/(1 - p)$, and its expected rate of gain is RBP. For the example topic of the cwl_eval paper, with gains 0, 0, 0.2, 0.4, 1, 0.2, 0, 0, 1, 0, 0, 0.4, 0, 0, 0, RBP at $p = 0.6$ is 0.1287 and the expected depth is 2.5.
- [nDCG](/normalized-discounted-cumulative-gain/) also has weights that fall with the rank, but it is normalized by the ideal ranking.
- [bpref](/bpref/) and [inferred average precision](/inferred-average-precision/) handle documents that are not judged by changing the measure. RBP keeps the measure and reports the residual instead.

Claims 1 to 3 are proved and hold for every ranking. The value of $p$ that matches real users is a question of measurement, not of proof. A claim that one system has a higher mean RBP than another needs a paired test over the queries, such as the [Wilcoxon signed-rank test](/wilcoxon-signed-rank-test/) or a [permutation test](/permutation-test/), and a large residual can make the comparison meaningless.

## References
