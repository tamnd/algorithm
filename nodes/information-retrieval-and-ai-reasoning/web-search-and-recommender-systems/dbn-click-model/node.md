---
tag: H0ZAVM
kind: model
slug: dbn-click-model
name: Dynamic Bayesian network click model
aliases:
- Chapelle-Zhang click model
- DBN click model
- DBN
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Extends the cascade model so that a clicked document may or may not satisfy the user, who continues with a fixed perseverance.
prereqs: [cascade-click-model, dynamic-bayesian-network, expectation-maximization]
see_also: [click-model, position-based-click-model, position-bias, expected-reciprocal-rank, hidden-markov-model, unbiased-learning-to-rank, learning-to-rank, maximum-likelihood-estimation]
sources:
  - paper: doi:10.1145/1526709.1526711
    title: Olivier Chapelle and Ya Zhang, A dynamic Bayesian network click model for web search ranking, Proceedings of the 18th International Conference on World Wide Web (WWW 2009), 1-10
    locator: the model with attractiveness, satisfaction and the perseverance gamma, its reduction to the cascade model when gamma and the satisfactions are 1, the EM fit, and Section 5 (the simplified model with gamma = 1)
  - book: isbn:9783031011665
    title: Aleksandr Chuklin, Ilya Markov and Maarten de Rijke, Click Models for Web Search, Morgan and Claypool 2015, reissued by Springer
    locator: Section 3.8 (the DBN model, Equations 3.34 to 3.40), Section 3.8.1 (the simplified DBN and its reduction to the cascade model), Section 4.1.3 (the counting estimates of the simplified DBN, Equation 4.10), Section 4.2.4 (EM estimation for DBN) and Chapter 7 (an experimental comparison of click models)
  - paper: doi:10.1145/1341531.1341545
    title: Nick Craswell, Onno Zoeter, Michael Taylor and Bill Ramsey, An experimental comparison of click position-bias models, Proceedings of the 2008 International Conference on Web Search and Data Mining (WSDM 2008), 87-94
    locator: the cascade model that the DBN model extends
---

The dynamic Bayesian network (DBN) click model is a [click model](/click-model/) in which the user scans the results from the top, clicks attractive ones, and after each click is either satisfied and stops, or not satisfied and goes on with a fixed probability $\gamma$, the perseverance. Olivier Chapelle and Ya Zhang introduced it in 2009 to estimate the relevance of documents from search logs. It extends the [cascade model](/cascade-click-model/), which stops at the first click, and it separates two things that a single click rate mixes: how attractive a result looks in the list, and how satisfying the document is once opened. The model is a [dynamic Bayesian network](/dynamic-bayesian-network/) over the ranks, its hidden states make the fit an [EM](/expectation-maximization/) problem, and the [position-based model](/position-based-click-model/) is the alternative without a top-down scan.

## The machine

A session shows a ranking $d_1, \ldots, d_n$. Each document has an attractiveness $a_d$ and a satisfaction $s_d$, and $\gamma$ is shared by all sessions. At rank $i$ there are hidden events $E_i$ (examined), $A_i$ (attracted), $S_i$ (satisfied) and the observed click $C_i$:

- $E_1 = 1$, and $C_i = 1$ exactly when $E_i = 1$ and $A_i = 1$, with $P(A_i = 1) = a_{d_i}$.
- After a click, $P(S_i = 1 \mid C_i = 1) = s_{d_i}$; without a click, $S_i = 0$.
- A satisfied user stops: $P(E_{i+1} = 1 \mid S_i = 1) = 0$.
- Otherwise the user goes on with probability $\gamma$: $P(E_{i+1} = 1 \mid E_i = 1, S_i = 0) = \gamma$, and a user who stopped never resumes.

These are Equations 3.34 to 3.40 in Section 3.8 of Chuklin, Markov and de Rijke. The same $\gamma$ applies after a skip and after an unsatisfying click.

## What it counts

The model gives a probability to every click vector $c_1, \ldots, c_n$, including vectors with several clicks. A forward pass computes it in $O(n)$ time. Keep two numbers: $e$, the probability of the clicks so far and that rank $i$ is examined, and $f$, the probability of the clicks so far and that the user has stopped. Start with $e = 1$, $f = 0$. At rank $i$, with $a = a_{d_i}$ and $s = s_{d_i}$:

- if $c_i = 1$: $e \leftarrow e\, a (1 - s) \gamma$ and $f \leftarrow e\, a \big(s + (1 - s)(1 - \gamma)\big)$, with the old $e$ on the right, because only an examined user clicks;
- if $c_i = 0$: $e \leftarrow e (1 - a) \gamma$ and $f \leftarrow f + e (1 - a)(1 - \gamma)$.

The answer is $e + f$ after the last rank. The probability of a click at rank $i$ alone is $a_{d_i}$ times the probability that rank $i$ is examined, and that probability falls by the factor $\gamma\,(1 - a_d s_d)$ at each rank.

For example, take the ranking x, y, z with $a = (0.5, 0.4, 0.3)$, $s = (0.6, 0.5, 0.5)$ and $\gamma = 0.9$:

| clicks | probability | clicks | probability |
|---|---|---|---|
| 0 0 0 | 0.2471 | 1 0 0 | 0.39884 |
| 0 0 1 | 0.0729 | 1 0 1 | 0.02916 |
| 0 1 0 | 0.1557 | 1 1 0 | 0.06228 |
| 0 1 1 | 0.0243 | 1 1 1 | 0.00972 |

The click rates of the three ranks are $0.5$, $0.252$ and $0.13608$. Each of the 8 values matches an enumeration over all $2^9$ settings of the hidden attraction, satisfaction and perseverance coins in the tests.

## Relation to other models

- **Cascade model.** With $\gamma = 1$ and $s_d = 1$ for every document, a user clicks the first attractive result and stops: this is the [cascade model](/cascade-click-model/). The tests check this reduction on every click vector.
- **Simplified DBN.** With $\gamma = 1$ alone, the user never leaves without a reason. Chapelle and Zhang (Section 5) and Section 3.8.1 of Chuklin, Markov and de Rijke call this the simplified DBN (SDBN).
- **Click chain model and dependent click model.** These also extend the cascade model with a chance to go on after a click. The click chain model ties the satisfaction to the attractiveness, while DBN gives each document its own satisfaction parameter.
- **Position-based model.** The [PBM](/position-based-click-model/) has no scan: the examination of each rank is a fixed probability. DBN explains why ranks below a satisfying result get fewer clicks, which the PBM cannot.
- **Hidden Markov models.** The examination state moves down the ranks as a Markov chain driven by the clicks, so the forward pass above is the forward algorithm of a [hidden Markov model](/hidden-markov-model/) with two states.
- **Expected reciprocal rank.** [Expected reciprocal rank](/expected-reciprocal-rank/) is a metric built on a cascade user who stops at each result with a probability that depends on its relevance, the same idea of satisfaction.

## Known results in the model

**Relevance from clicks.** The probability that an examined document both attracts and satisfies the user is $a_d s_d$. Chapelle and Zhang use this product as the relevance of the document estimated from the logs, which removes the [position bias](/position-bias/) of raw click rates.

**EM fit.** The examination and satisfaction events are hidden after the last click, so the full model is fitted by EM, which needs the posterior of these events in each session (Section 4.2.4 of Chuklin, Markov and de Rijke). Above the last click nothing is hidden: every rank was examined, and every earlier click was unsatisfying. The fit can stop at a local maximum.

**Counting estimates for the simplified model.** Section 4.1.3 of Chuklin, Markov and de Rijke assumes, for $\gamma = 1$, that the user examines every result down to the last click and then stops. Then all events above the last click are observed and

$$\hat a_d = \frac{\text{clicks on } d}{\text{sessions with } d \text{ at or above the last click}}, \qquad \hat s_d = \frac{\text{sessions where } d \text{ is the last click}}{\text{clicks on } d}.$$

These are maximum likelihood estimates under that assumption. Under the model itself with $\gamma = 1$, a user who is not satisfied by the last click still examines the results below it without clicking, so the assumption is an approximation that drops this hidden examination.

**Fit on real logs.** In the comparison of Chapter 7 of Chuklin, Markov and de Rijke on a public log of a commercial search engine, DBN and SDBN are among the best models by perplexity, and DBN is close to UBM, the best model by log likelihood. Chapelle and Zhang report that DBN predicts click-through rates and relevance better than the earlier models on their data. Both are measurements on particular logs.

**A simulation.** The tests also draw 40000 sessions with a fixed seed from a 4-result ranking and check the frequency of each of the 16 click vectors against the forward pass, within the Hoeffding half width $\sqrt{\ln(2/\delta)/(2n)}$ for $\delta = 10^{-6}$.

## References
