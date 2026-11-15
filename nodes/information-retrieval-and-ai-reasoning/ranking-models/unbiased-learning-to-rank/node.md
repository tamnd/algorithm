---
tag: TP8SM4
kind: technique
slug: unbiased-learning-to-rank
name: Unbiased learning to rank
aliases:
- counterfactual learning to rank
- propensity-weighted LTR
area: information-retrieval-and-ai-reasoning/ranking-models
level: research
summary: Learns a ranker from biased click logs by weighting each click by the inverse of its estimated examination propensity.
prereqs: [learning-to-rank, position-bias, inverse-probability-weighting]
see_also: [click-model, position-based-click-model, propensity-score, importance-sampling, off-policy-evaluation, ranking-svm, lambdamart, interleaved-evaluation]
sources:
  - paper: doi:10.1145/3018661.3018699
    title: Thorsten Joachims, Adith Swaminathan and Tobias Schnabel, Unbiased learning-to-rank with biased feedback, Proceedings of the 10th ACM International Conference on Web Search and Data Mining (WSDM 2017)
    locator: pp. 781-789; Equation (2) (the sum of the ranks of relevant documents), Section 4 and Equation (4) (the propensity-weighted empirical risk), Section 5.1 and Equation (5) (the examination model), Section 5.3 (estimating propensities by swap interventions), Section 6 (Propensity SVM-Rank), Section 7.1 and Equation (7) (propensities (1/rank) to the power eta), Section 7.2 (clipping)
  - paper: doi:10.1145/775047.775067
    title: Thorsten Joachims, Optimizing search engines using clickthrough data, Proceedings of the 8th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 2002
    locator: pp. 133-142 (pairwise preferences read from clicks, the biased starting point that the propensity method replaces)
---

Unbiased learning to rank trains a ranker from click logs as if it had relevance labels. Clicks are biased: a user can only click a result that they examine, and they examine the top positions much more often, which is [position bias](/position-bias/). If the probability $Q(o_d = 1)$ that the user examined result $d$ is known and positive, dividing each click by it gives an estimate of a relevance-based metric whose expected value is the true metric. This is [inverse probability weighting](/inverse-probability-weighting/) applied to the examination event. The position-bias and [click-model](/click-model/) pages describe how users examine and click; this page uses one of those models, assumes its propensities, and shows how to turn the clicks into an unbiased training objective, with a proof and the two ways it fails. The [learning-to-rank](/learning-to-rank/) page covers training from editorial labels.

## In plain words

People click mostly on the first few results, even when a lower result is better, because they never look at the lower ones. If we train a ranker on raw clicks, it learns to copy the old ranking. The fix is to count a click on a result that people rarely look at as worth more. If only one person in three ever looks at position three, a click there counts three times. On average, this gives the same answer as if every person had looked at every result. For this to work, we must know how often each position is looked at, and every relevant result must have some chance of being seen.

## When it applies

The technique applies when:

- the training data are logs of rankings shown to users and the clicks on them;
- a click on $d$ happens only if the user examined $d$, and then depends on the relevance of $d$ and not on its position: $P(c_d = 1) = Q(o_d = 1)\, r_d$ for binary relevance $r_d$, the examination model of Joachims, Swaminathan and Schnabel (2017), Section 5.1, Equation (5), which is the [position-based click model](/position-based-click-model/) with binary relevance;
- the propensity $Q(o_d = 1)$ is known, or estimated, and positive for every relevant document;
- the metric is a sum over relevant documents of a function of their rank, such as the sum of ranks $\Delta(S) = \sum_d \mathrm{rank}_S(d)\, r_d$ of Equation (2) of that paper, DCG, or precision at $k$.

The method does not apply to clicks that depend on the other results, as in the [cascade model](/cascade-click-model/), without a matching propensity model.

## The template

For a new ranker $S$ and one logged query with clicks $c$, the propensity-weighted estimate of $\Delta(S)$ is

$$\hat\Delta_{\text{IPS}}(S) = \sum_{d : c_d = 1} \frac{\mathrm{rank}_S(d)}{Q(o_d = 1)}.$$

Summed over the logged queries, it is the empirical risk of Equation (4) of the paper.

```pseudo id=main
UNBIASED-LTR(log, Q, τ, learner)
L1  examples ← empty
L2  for each logged query x with shown ranking y and clicks c:
L3      for each document d with c_d = 1:
L4          q ← Q(examined | rank of d in y)
L5          add (x, d, weight 1 / max(τ, q)) to examples
L6  S ← learner minimizing Σ weight · bound(rank_S(d)) over examples
L7  return S
```

Line L4 reads the propensity of the logged position, for example $(1/\mathrm{rank})^\eta$ as in Section 7.1, Equation (7). Line L5 is the inverse weight; $\tau = 0$ gives the unbiased estimator, and $\tau > 0$ the clipped one of Section 7.2. Line L6 needs a loss that bounds the rank and can be minimized: Propensity SVM-Rank, in Section 6, uses the hinge bound of the [Ranking SVM](/ranking-svm/) and solves $\min_w \frac{1}{2} w \cdot w + \frac{C}{n} \sum_j \frac{1}{q_j} \sum_i \xi_{ji}$, one pair for each clicked document and each other document of its query.

**Unbiasedness.** Fix a query, its relevance $r$, the logged ranking $y$ and a new ranking $S$. Assume the examination model and $Q(o_d = 1) > 0$ for every $d$ with $r_d = 1$. Then $\mathbb E[\hat\Delta_{\text{IPS}}(S)] = \Delta(S)$, where the expectation is over the examination events.

*Proof.* Write $\hat\Delta_{\text{IPS}}(S) = \sum_{d : r_d = 1} c_d\, \mathrm{rank}_S(d) / Q(o_d = 1)$; a document with $r_d = 0$ is never clicked under the model, so it adds nothing, and the division is defined for every document that can appear. By linearity of expectation and $\mathbb E[c_d] = P(c_d = 1) = Q(o_d = 1)\, r_d = Q(o_d = 1)$ for $r_d = 1$,

$$\mathbb E[\hat\Delta_{\text{IPS}}(S)] = \sum_{d : r_d = 1} \frac{Q(o_d = 1)\, \mathrm{rank}_S(d)}{Q(o_d = 1)} = \sum_{d : r_d = 1} \mathrm{rank}_S(d) = \Delta(S). \qquad \square$$

The proof uses nothing about $\mathrm{rank}_S(d)$ except that it does not depend on the clicks of this log entry, so the same holds for any metric of the form $\sum_d \lambda(\mathrm{rank}_S(d))\, r_d$. Summing over queries keeps the expectation, so the empirical risk is unbiased for the mean of $\Delta$ over the logged queries, and the clicks of different queries are independent, so its average converges to that mean by the [law of large numbers](/law-of-large-numbers/).

**Wrong propensities.** If the estimator uses $\hat Q_d$ in place of the true $Q_d$, the same computation gives $\mathbb E[\hat\Delta] = \sum_{d : r_d = 1} \mathrm{rank}_S(d)\, Q_d / \hat Q_d$. Each relevant document is weighted by $Q_d / \hat Q_d$, so documents at positions where the propensity is overestimated count too little, and the learner prefers rankings that move them down. The bias does not shrink with more data.

**Zero propensities.** If $Q_d = 0$ for a relevant $d$, for example a document that was never shown, $c_d = 0$ always, and no weight can recover it: $\mathbb E[\hat\Delta] = \Delta(S) - \sum_{d : r_d = 1, Q_d = 0} \mathrm{rank}_S(d)$. The estimator is unbiased only for the metric over documents that can be examined. This is the condition $Q > 0$ for relevant documents in Section 4 of the paper.

## Classic examples

Take one query with three documents shown in the order A, B, C, with relevance $r = (1, 0, 1)$ and propensities $Q = (1, 1/2, 1/3)$, that is $(1/\mathrm{rank})^\eta$ with $\eta = 1$. A new ranker $S$ orders them C, A, B, so $\Delta(S) = \mathrm{rank}_S(A) + \mathrm{rank}_S(C) = 2 + 1 = 3$. Under the model, A is always clicked and C is clicked with probability $1/3$.

| estimator | value if only A is clicked | value if A and C are clicked | mean | variance |
|---|---|---|---|---|
| clicks without weights | 2 | 3 | 2.3333 | 0.2222 |
| IPS with the true $Q$ | 2 | 5 | 3.0000 | 2.0000 |
| IPS with $\eta = 0.5$ in place of 1 | 2 | 3.7321 | 2.5774 | 0.6667 |
| IPS clipped at $\tau = 0.5$ | 2 | 4 | 2.6667 | 0.8889 |

The unweighted clicks underestimate the cost of putting C first, because C is rarely examined at rank 3 of the log. IPS with the true propensities is exactly unbiased and has the largest variance. The wrong $\eta$ and the clipping trade bias for variance. If C had never been shown ($Q_C = 0$), every estimator would give 2, and the bias of $-1$ would remain for any amount of data.

Further examples of the technique:

- **Propensity SVM-Rank.** Joachims, Swaminathan and Schnabel (2017), Section 6: the [Ranking SVM](/ranking-svm/) with each clicked document's slack terms weighted by $1/q$.
- **Propensity-weighted LambdaMART.** Weight the lambdas of each clicked document by its inverse propensity in [LambdaMART](/lambdamart/), which gives an unbiased estimate of a DCG-like objective under the same model.
- **Counterfactual evaluation.** The same estimator, with no training, compares rankers offline from logs, as in [off-policy evaluation](/off-policy-evaluation/) of a [contextual bandit](/contextual-bandit/), where the propensity is that of the logged action.

## Variations

- **Propensity estimation by intervention.** Section 5.3 of the paper swaps the result at rank 1 with the result at rank $k$ for a random fraction of queries; the ratio of click rates at the two positions estimates $Q_k / Q_1$, since relevance is the same on average.
- **Propensities from the logs.** Later methods fit the propensities and the relevance together with a click model, from logs where the same document appeared at different positions, without new interventions.
- **Clipping and normalization.** $\max\{\tau, Q\}$ caps the weights at $1/\tau$, and self-normalized estimators divide by the sum of the weights. Both reduce variance and add bias.
- **Trust bias and noise.** If users also click irrelevant documents with a probability that depends on the position, a single inverse weight is no longer enough; affine corrections with two parameters per position handle that model.
- **Online alternatives.** [Interleaved evaluation](/interleaved-evaluation/) and online learning to rank collect new clicks under randomized rankings instead of correcting old logs.

## Pitfalls

- **Unchecked examination model.** The proof needs clicks that depend only on examination and relevance. Under a cascade-like user, the probability of examining rank 3 depends on what is at ranks 1 and 2, and a fixed $Q(\text{rank})$ is wrong.
- **Variance.** Weights up to $1/Q_{\min}$ make a few clicks at low positions dominate the objective. Clip, or gather more data, and report the effective sample size.
- **Propensities from the same model.** Estimating $\eta$ from logs of the ranker being corrected, without intervention or a click model, confounds position with relevance.
- **Documents that were never shown.** Their propensity is 0, and nothing in the clicks tells their relevance. Truncated result lists, pagination and filters create such documents.
- **Non-clicks as negatives.** IPS weights the clicks. Treating every unclicked document as irrelevant with full weight brings the position bias back.

## Exercises

1. In the example, show that IPS with $\hat Q_C = 1/2$ in place of $1/3$ has the mean $2 + \frac{1}{3} \cdot 2 = 2.6667$, the same as clipping at $\tau = 0.5$, and explain why.
2. Prove that the IPS estimator of DCG, with the gain $\lambda(\mathrm{rank}) = 1/\log_2(1 + \mathrm{rank})$, is unbiased under the same assumptions.
3. Under the examination model with click noise, $P(c_d = 1) = Q_d (\epsilon_+ r_d + \epsilon_- (1 - r_d))$, compute $\mathbb E[\hat\Delta_{\text{IPS}}]$ and show that it is an affine function of $\Delta$ with a positive slope when $\epsilon_+ > \epsilon_-$, so it still ranks rankers in the right order if the extra term does not depend on $S$.

## References
