---
tag: 6YC3GK
kind: model
slug: cwl-framework
name: C/W/L framework
aliases:
- conditional continuation probability framework
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: research
summary: Describes each metric by a user model of continuation probabilities at each rank, from which the weights and the expected utility follow.
prereqs: [rank-biased-precision, expected-reciprocal-rank, mean-average-precision]
see_also: [precision-at-k, normalized-discounted-cumulative-gain, mean-reciprocal-rank, cascade-click-model, position-based-click-model, click-model, geometric-distribution]
sources:
  - paper: doi:10.1145/3052768
    title: Alistair Moffat, Peter Bailey, Falk Scholer and Paul Thomas, Incorporating user expectations and behavior into the measurement of search effectiveness, ACM Transactions on Information Systems 35(3), Article 24, 2017, pp. 24:1-24:38
    locator: the C/W/L framework, the weights derived from the continuation probability, the expected rate of gain, and the adaptive metric INST with the target T
  - paper: doi:10.1145/3331184.3331398
    title: Leif Azzopardi, Paul Thomas and Alistair Moffat, cwl_eval, an evaluation tool for information retrieval, SIGIR 2019, pp. 1321-1324
    locator: the definitions of C, W and L, the measures EU, ETU, EC, ETC and ED, Table 1 (the values of AP, RR, P@5, NDCG-k@10 and INST with T = 2 on the example topic T1) and Table 2 (RBP with p = 0.6)
  - url: https://github.com/ireval/cwl
    title: cwl_eval, the reference implementation of the C/W/L framework
    locator: the residual option -r (the difference between the best and the worst case for the items that are not judged), the default maximum gain 1.0 and the default depth 1000
  - paper: "Alistair Moffat, Peter Bailey, Falk Scholer and Paul Thomas, INST: an adaptive metric for information retrieval evaluation, ADCS 2015, pp. 5:1-5:4"
    locator: the metric INST, whose continuation probability depends on the gain still wanted
  - paper: doi:10.1145/3471158.3472239
    title: Leif Azzopardi, Joel Mackenzie and Alistair Moffat, ERR is not C/W/L, ICTIR 2021
    locator: the relation of expected reciprocal rank to the framework
---

The C/W/L framework describes a metric of a ranked list by a model of a user who reads the list from the top, one item at a time. The model is given by one function: the conditional continuation probability $C(i)$, the probability that a user who has looked at the item at rank $i$ goes on to rank $i + 1$. From $C$ follow the weight $W(i)$, the share of the user's attention that goes to rank $i$, and the last-item probability $L(i)$, the probability that rank $i$ is the last one the user looks at. The metric is the expected gain per item looked at. [Precision at k](/precision-at-k/), [rank-biased precision](/rank-biased-precision/), scaled DCG, [average precision](/mean-average-precision/), [reciprocal rank](/mean-reciprocal-rank/) and the adaptive metric INST are all cases, each with its own $C$. Moffat, Bailey, Scholer and Thomas set out the framework in 2017, and the tool cwl_eval of Azzopardi, Thomas and Moffat computes it.

## The machine

The input is a ranking of items for one query, with a gain $g_i \in [0, 1]$ for the item at rank $i$, for example a grade divided by the top grade, and optionally a cost $c_i \ge 0$ for looking at it. Items that are not judged have gain 0.

A step is one look at one item. The user looks at rank 1. After looking at rank $i$, the user goes on to rank $i + 1$ with probability $C(i) \in [0, 1]$ and stops with probability $1 - C(i)$. The function $C$ may read the rank $i$, the gains $g_1, \ldots, g_i$ seen so far, and fixed parameters such as the persistence $p$ or the target $T$. Some metrics also read gains below rank $i$, as AP does below. This is the memory of the model: what the user knows when deciding whether to go on.

Let $V(i) = \prod_{j < i} C(j)$ be the probability that the user looks at rank $i$, so $V(1) = 1$. From $C$ the framework derives

$$W(i) = \frac{V(i)}{\sum_{k \ge 1} V(k)}, \qquad L(i) = V(i) \, (1 - C(i)).$$

$W(i)$ is the expected share of the looks that fall on rank $i$, and $L(i)$ is the probability that rank $i$ is the last item looked at. A tool must stop at some depth; cwl_eval looks at no more than 1000 items by default and treats the items past the end of the ranking as having gain 0.

## What it counts

The framework reports five numbers:

- the expected depth $\mathrm{ED} = \sum_i V(i) = 1/W(1)$, the expected number of items looked at;
- the expected utility $\mathrm{EU} = \sum_i W(i) \, g_i$, the expected gain per item looked at, which is the value of the metric;
- the expected total utility $\mathrm{ETU} = \sum_i V(i) \, g_i = \mathrm{EU} \cdot \mathrm{ED}$, the expected gain over the whole visit;
- the expected cost $\mathrm{EC} = \sum_i W(i) \, c_i$ per item, and the expected total cost $\mathrm{ETC} = \mathrm{EC} \cdot \mathrm{ED}$.

**Claim 1.** $\sum_i W(i) = 1$, $W(i + 1) = C(i) \, W(i)$ and $\mathrm{ED} = 1/W(1)$.

*Proof.* The weights are the $V(i)$ divided by their sum, so they sum to 1. $V(i + 1) = C(i) V(i)$ by the definition of $V$, and dividing by the sum keeps the ratio. $W(1) = V(1)/\mathrm{ED} = 1/\mathrm{ED}$. $\square$

So $C$ and $W$ fix each other: $C(i) = W(i + 1)/W(i)$ wherever $W(i) > 0$. A metric that is a weighted sum of gains with weights that do not grow with the rank and sum to 1 has a C/W/L form.

**Claim 2.** If the user stops for sure by the cut depth, so that $\sum_i L(i) = 1$, then $\mathrm{ETU} = \sum_i L(i) \sum_{j \le i} g_j$, the expected gain collected up to the last item.

*Proof.* The user looks at rank $j$ exactly when the last item is at rank $i \ge j$, so $\sum_{i \ge j} L(i) = V(j)$. Swap the two sums: $\sum_i L(i) \sum_{j \le i} g_j = \sum_j g_j \sum_{i \ge j} L(i) = \sum_j g_j V(j)$. $\square$

At the cut depth the tool sets $C = 0$, which makes $\sum_i L(i) = 1$. EU is ETU divided by ED, so it is a ratio of expected values: the expected gain over the expected number of looks, as in Claim 1 of the [RBP page](/rank-biased-precision/).

## Relation to other models

- **Metrics.** Each metric of the list above is a choice of $C$. With the gains of q1 below, the table of known results gives the values.

| Metric | $C(i)$ |
|---|---|
| Precision at $k$ | 1 for $i < k$, 0 for $i = k$ |
| RBP with persistence $p$ | $p$ |
| Scaled DCG at $k$ | $\log_2(i + 1)/\log_2(i + 2)$ for $i < k$, 0 for $i = k$ |
| Reciprocal rank | 1 if $g_i = 0$, 0 if $g_i > 0$ |
| Average precision, binary gains | $\sum_{j > i} g_j / j \;/\; \sum_{j \ge i} g_j / j$ |
| INST with target $T$ | $((i + T + T_i - 1)/(i + T + T_i))^2$, with $T_i = T - \sum_{j \le i} g_j$ |

Scaled DCG at $k$ is DCG@k divided by the sum of the first $k$ discounts $\sum_{i \le k} 1/\log_2(i + 1)$, which cwl_eval lists as NDCG-k. It is not [nDCG](/normalized-discounted-cumulative-gain/), which divides by the DCG of the ideal ranking.

- **Click models.** $V(i)$ is the probability of examination in a [click model](/click-model/). In the [cascade click model](/cascade-click-model/), the user goes on unless the current item satisfies, which is $C(i) = 1 - g_i$ when the gain is read as the probability of satisfaction. In the [position-based click model](/position-based-click-model/), examination depends only on the rank, which is a $C$ that reads only $i$.
- **Expected reciprocal rank.** With $C(i) = (1 - R_i) \, i/(i + 1)$, where $R_i$ is the satisfaction probability of ERR, $V(i) = E_i / i$, and ETU is [expected reciprocal rank](/expected-reciprocal-rank/). The value of this C/W/L metric is EU, which is ERR divided by ED, not ERR. Azzopardi, Mackenzie and Moffat (2021) study this relation under the title "ERR is not C/W/L".
- **Fixed and adaptive users.** When $C$ reads only the rank, as for precision at $k$, RBP and scaled DCG, the weights are fixed and EU is linear in the gains. When $C$ reads gains, as for RR, AP and INST, the weights move with the ranking, and EU is not linear. The cwl_eval paper notes that the $C$ of RBP is not sensitive to the gain or to the cost.

## Known results in the model

### Values on the toy collection

Query q1 "sorted array search" has the judgments d1 grade 2, d2 grade 1 and d8 grade 1. The fixed run 1, 6, 8, 2, 4 has gains $g/2$ = 1, 0, 0.5, 0.5, 0. For RR and AP the gains are binary, 1, 0, 1, 1, 0. Values are computed to depth 1000.

| Metric | EU | ED | $W(1), W(2), \ldots$ |
|---|---|---|---|
| P@3 | 0.5 | 3 | 1/3, 1/3, 1/3 |
| RBP, $p = 0.8$ | 0.3152 | 5 | 0.2, 0.16, 0.128, 0.1024, ... |
| Scaled DCG@5 | 0.49698 | 2.94846 | 0.3392, 0.2140, 0.1696, 0.1461, 0.1312 |
| RR | 1 | 1 | 1 |
| AP | 0.80556 | 1.89474 | 0.5278, 0.1944, 0.1944, 0.0833 |
| INST, $T = 1$ | 0.69387 | 1.56210 | |
| INST, $T = 2$ | 0.40016 | 3.24991 | |
| INST, $T = 3$ | 0.28539 | 5.06917 | |

The AP row is the average precision $29/36$ of the run, since all three relevant documents are retrieved. The last-item probabilities show the stopping behaviour: for P@3 they are 0, 0, 1, so every user stops at rank 3, and for RBP they are $(1 - p) p^{i - 1}$ = 0.2, 0.16, 0.128, 0.1024, ... . A larger target $T$ makes the INST user read deeper and gives a lower rate, because the run has its best item first.

### The example topic of cwl_eval

The cwl_eval paper uses a topic T1 with the gains 0, 0, 0.2, 0.4, 1, 0.2, 0, 0, 1, 0, 0, 0.4, 0, 0, 0 and no costs. The $C$ functions of the table above, computed to depth 1000, give the values of its Table 1 and Table 2. RR stops at rank 3, the first item of positive gain, and credits its graded gain 0.2, so ETU is 0.2 and EU is 0.2/3.

| Metric | EU | ETU | ED |
|---|---|---|---|
| AP | 0.2722 | 1.6000 | 5.8776 |
| RR | 0.0667 | 0.2000 | 3.0000 |
| P@5 | 0.3200 | 1.6000 | 5.0000 |
| NDCG-k@10 | 0.2270 | 1.0314 | 4.5436 |
| INST, $T = 2$ | 0.1545 | 0.6069 | 3.9292 |
| RBP, $p = 0.6$ | 0.1287 | 0.3218 | 2.5000 |

### Residuals

When some items are not judged, cwl_eval with the option -r reports a residual: the difference between the best case and the worst case for the items that are not judged. For RBP this is the residual of the [RBP page](/rank-biased-precision/). For a metric whose $C$ reads gains, the weights change between the two cases, so the residual is not a sum of weights.

### Pitfalls

- **The cut depth changes adaptive metrics.** For INST, $C(i)$ tends to 1 as $i$ grows, so $V(i)$ falls only like $1/i^2$ and ED depends on where the tool stops. On T1 with $T = 2$, depth 1000 gives EU 0.1545 and ED 3.9292, and depth 3000 gives 0.1543 and 3.9339. A report must give the depth.
- **AP knows the future.** The $C$ of AP at rank $i$ reads the gains below rank $i$, which the user has not seen. The form also divides by the number of relevant items in the ranking, not by the number of relevant items of the query. For the fixed run of q1 both are 3; for a run that misses a relevant document, the C/W/L value is larger than the AP of trec_eval.
- **EU is not ETU.** EU is a rate per item and ETU is a total. Two metrics with the same ETU can have different EU: on T1, AP and P@5 both have ETU 1.6, with EU 0.2722 and 0.32.
- **Gains must be in $[0, 1]$.** INST and the residual assume a maximum gain, 1 by default in cwl_eval. Grades on a larger scale must be divided by the top grade first.

## References
