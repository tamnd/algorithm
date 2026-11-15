---
tag: F0GVXM
kind: model
slug: cascade-click-model
name: Cascade click model
aliases:
- Craswell cascade model
- cascade model
- CM
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: The user scans results from the top and clicks the first attractive one, then stops; each result is examined only if all above were skipped.
prereqs: [click-model, maximum-likelihood-estimation]
see_also: [position-based-click-model, dbn-click-model, position-bias, expected-reciprocal-rank, hoeffding-inequality, multi-armed-bandit, unbiased-learning-to-rank, bayesian-network]
sources:
  - paper: doi:10.1145/1341531.1341545
    title: Nick Craswell, Onno Zoeter, Michael Taylor and Bill Ramsey, An experimental comparison of click position-bias models, Proceedings of the 2008 International Conference on Web Search and Data Mining (WSDM 2008), 87-94
    locator: the four position-bias hypotheses (baseline, mixture, examination and cascade), the experiment that swaps adjacent results, and the finding that the cascade model fits best at the top ranks
  - book: isbn:9783031011665
    title: Aleksandr Chuklin, Ilya Markov and Maarten de Rijke, Click Models for Web Search, Morgan and Claypool 2015, reissued by Springer
    locator: Section 3.4 (the cascade model, Equations 3.9 to 3.14, and the remark that it can only describe sessions with one click), Section 3.8.1 (the cascade model as a special case of the simplified DBN), Chapter 4 (maximum likelihood estimation when the examinations are observed) and Chapter 7 (an experimental comparison of click models)
  - paper: doi:10.1145/1526709.1526711
    title: Olivier Chapelle and Ya Zhang, A dynamic Bayesian network click model for web search ranking, Proceedings of the 18th International Conference on World Wide Web (WWW 2009), 1-10
    locator: the DBN model, which extends the cascade model with satisfaction and perseverance and reduces to it when both are 1
---

The cascade click model is a [click model](/click-model/) in which the user reads a result list from the top, clicks the first result that looks attractive, and stops. Nick Craswell, Onno Zoeter, Michael Taylor and Bill Ramsey introduced it in 2008, in the paper that compared several explanations of [position bias](/position-bias/). It has one parameter per document, the probability $\alpha_d$ that the document attracts a click when it is examined, and its examinations are fully determined by the click, so the parameters have closed-form [maximum likelihood](/maximum-likelihood-estimation/) estimates. The [position-based model](/position-based-click-model/) instead lets examination depend on the rank alone, and the [DBN model](/dbn-click-model/) lets the user continue after a click.

## The machine

A session shows a ranking $d_1, \ldots, d_n$ for one query. The model has hidden examination events $E_i$ and attraction events $A_i$, and the observed click events $C_i$:

- $E_1 = 1$: the user always examines the first result.
- $A_i \sim \mathrm{Bernoulli}(\alpha_{d_i})$, independently, and $C_i = 1$ exactly when $E_i = 1$ and $A_i = 1$.
- $E_{i+1} = 1$ exactly when $E_i = 1$ and $C_i = 0$: after a skip the user goes on, and after a click the user stops.

So the user examines the results one by one and stops at the first click. Every session has at most one click, and every result above the click was examined and skipped.

## What it counts

The model gives the probability of each possible session. The click falls at rank $i$ with probability

$$P(C_i = 1) = \alpha_{d_i} \prod_{j < i} (1 - \alpha_{d_j}),$$

and there is no click with probability $\prod_{j \le n} (1 - \alpha_{d_j})$; these $n + 1$ numbers sum to 1. For example, with $\alpha = 0.5, 0.4, 0.2$ for the ranking a, b, c, the click is on a with probability $0.5$, on b with $0.5 \cdot 0.4 = 0.2$, on c with $0.5 \cdot 0.6 \cdot 0.2 = 0.06$, and there is no click with probability $0.5 \cdot 0.6 \cdot 0.8 = 0.24$. A document has a click-through rate that falls with its rank even when its $\alpha$ is fixed, because every result above it can take the click first.

## Relation to other models

- **Examination hypothesis.** Like most click models, it clicks exactly when a result is examined and attractive. In the [position-based model](/position-based-click-model/) the examination of rank $i$ has a fixed probability that ignores the other results; in the cascade model it is the probability that all results above were skipped.
- **Craswell et al. 2008.** The paper compared four hypotheses on data from an experiment that swapped two adjacent results: a baseline with no position bias, a mixture model, the examination model and the cascade model. The cascade model predicted the clicks best, most clearly at the top ranks. This result is a measurement on their logs.
- **Extensions.** The dependent click model, the click chain model and the [DBN model](/dbn-click-model/) all keep the scan from the top and add a chance to continue after a click. The DBN model with perseverance $\gamma = 1$ and satisfaction $1$ for every document is the cascade model (Section 3.8.1 of Chuklin, Markov and de Rijke).
- **Metrics.** [Expected reciprocal rank](/expected-reciprocal-rank/) is a metric built on a cascade user who stops at a satisfying result.
- **Online learning.** Cascading versions of the [multi-armed bandit](/multi-armed-bandit/) learn a ranking from clicks under this model.

## Known results in the model

**The examinations are observed.** In a session with a click at rank $c$, the results at ranks $1, \ldots, c$ were examined and the results below were not. In a session without a click all $n$ were examined. So the likelihood factors over documents:

$$L(\alpha) = \prod_d \alpha_d^{k_d} (1 - \alpha_d)^{m_d - k_d},$$

where $m_d$ is the number of sessions in which $d$ was examined and $k_d$ the number in which it was clicked. The maximum likelihood estimate is $\hat\alpha_d = k_d / m_d$: the clicks on $d$ divided by the impressions of $d$ at or above the click, or anywhere in a session without a click. No iterative method such as [EM](/expectation-maximization/) is needed.

**The estimate concentrates.** Whether $d$ is examined in a session depends only on the attraction coins of the results above it, not on those of $d$. So, given $m_d$, the $k_d$ clicks are a sum of $m_d$ independent Bernoulli($\alpha_d$) coins, and [Hoeffding's inequality](/hoeffding-inequality/) gives $|\hat\alpha_d - \alpha_d| \le \sqrt{\ln(2/\delta) / (2 m_d)}$ with probability at least $1 - \delta$. The tests simulate 50000 sessions of 5 results drawn from 10 documents with a fixed seed, and check every estimate against this bound with $\delta = 10^{-6}$. This shows that the estimator recovers the parameters when the data come from the model; how well the model fits real users is a separate question, answered only by measurements on logs.

**One click per session.** The model gives probability 0 to a session with two clicks. Real logs have many such sessions, so in practice the model is fitted on the part of each session up to its first click, or a model that allows more clicks is used. Section 3.4 of Chuklin, Markov and de Rijke notes that the cascade model can only describe sessions with one click and cannot explain non-linear examination patterns. In their experimental comparison on a public log of a commercial search engine (Chapter 7), more complex models fit better than the cascade model; this is a measurement as well.

**A worked estimate.** Four sessions show a, b, c. Two click a, one clicks b and one has no click. Then a was examined 4 times and clicked twice, b examined twice and clicked once, and c examined once and never clicked, so $\hat\alpha = (0.5, 0.5, 0)$. The raw click-through rates, $0.5$, $0.25$ and $0$, understate b because two of its four impressions were never examined.

## References
