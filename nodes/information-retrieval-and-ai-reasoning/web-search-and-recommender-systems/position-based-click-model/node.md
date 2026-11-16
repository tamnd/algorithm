---
tag: 56VCGX
kind: model
slug: position-based-click-model
name: Position-based click model
aliases:
- examination hypothesis model
- PBM
- position-based model
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: A click happens when the user examines a rank, with a probability that depends only on the rank, and the document attracts.
prereqs: [click-model, position-bias, expectation-maximization]
see_also: [cascade-click-model, dbn-click-model, maximum-likelihood-estimation, unbiased-learning-to-rank, learning-to-rank, bayesian-network, interleaved-evaluation]
sources:
  - paper: doi:10.1145/1242572.1242643
    title: Matthew Richardson, Ewa Dominowska and Robert Ragno, Predicting clicks, estimating the click-through rate for new ads, Proceedings of the 16th International Conference on World Wide Web (WWW 2007), 521-530
    locator: the assumption that the probability of a click is the probability that the ad is seen, which depends on its position, times the probability that it is clicked once seen
  - paper: doi:10.1145/1341531.1341545
    title: Nick Craswell, Onno Zoeter, Michael Taylor and Bill Ramsey, An experimental comparison of click position-bias models, Proceedings of the 2008 International Conference on Web Search and Data Mining (WSDM 2008), 87-94
    locator: the examination hypothesis as one of the four position-bias models compared, with the cascade model
  - book: isbn:9783031011665
    title: Aleksandr Chuklin, Ilya Markov and Maarten de Rijke, Click Models for Web Search, Morgan and Claypool 2015, reissued by Springer
    locator: Section 3.3 (the position-based model, Equations 3.4 to 3.8, with the convention that the first rank is always examined), Section 4.2 (the EM algorithm for click models), Section 4.3 (the table of update formulas, including the PBM update) and Chapter 7 (an experimental comparison of click models)
---

The position-based click model (PBM) is a [click model](/click-model/) in which a result is clicked when the user examines its rank and is attracted by the document, two independent events: rank $r$ is examined with a probability $\gamma_r$ that depends on the rank only, and document $d$ attracts with a probability $\alpha_d$ that depends on the document only. It is the simplest model that separates [position bias](/position-bias/) from attractiveness, and it is the basis of most estimates of position bias for [unbiased learning to rank](/unbiased-learning-to-rank/). The examination events are hidden, so the parameters are fitted by [EM](/expectation-maximization/). The [cascade model](/cascade-click-model/) instead makes examination depend on the clicks above, which allows only one click per session.

## The machine

A session shows a ranking $d_1, \ldots, d_n$. For each rank $r$, independently of all other ranks:

- the user examines rank $r$, $E_r = 1$, with probability $\gamma_r$;
- the document is attractive, $A_r = 1$, with probability $\alpha_{d_r}$, independently of $E_r$;
- the click is $C_r = E_r A_r$.

This is the examination hypothesis, $C = 1$ exactly when $E = 1$ and $A = 1$. Richardson, Dominowska and Ragno used the same factorization in 2007 to predict the click-through rate of ads, and Craswell, Zoeter, Taylor and Ramsey compared it with the cascade model in 2008. Usually $\gamma_1 = 1$ by convention (footnote to Section 3.3 of Chuklin, Markov and de Rijke).

## What it counts

The probability of a click vector $c_1, \ldots, c_n$ is the product over ranks of

$$P(C_r = 1) = \gamma_r \alpha_{d_r}, \qquad P(C_r = 0) = 1 - \gamma_r \alpha_{d_r}.$$

Any number of clicks is possible, and the click at one rank says nothing about the others. For example, with $\gamma = (1, 0.5)$ and $\alpha_a = 0.6$, $\alpha_b = 0.4$, the ranking a, b has click probabilities $0.6$ and $0.5 \cdot 0.4 = 0.2$, and is clicked at both ranks with probability $0.6 \cdot 0.2 = 0.12$. The ranking b, a has $0.4$ and $0.3$. Document a gets twice as many clicks at the top as at the second rank, with the same attractiveness.

## Relation to other models

- **Cascade model.** In the [cascade model](/cascade-click-model/) the examination of rank $r$ is the event that all results above were skipped, so it depends on the documents above. In the PBM it does not. The cascade model allows at most one click, the PBM any number.
- **User browsing model.** The UBM of Dupret and Piwowarski (2008) makes the examination depend on the rank and on the distance to the previous click; the PBM is the case where it depends on the rank only.
- **DBN.** The [DBN model](/dbn-click-model/) keeps a top-down scan, like the cascade model, and adds satisfaction after a click.
- **Click-through rate models.** Without $\gamma$, all ranks are examined and $\alpha_d$ is the click-through rate of the document. Those raw rates mix the attraction of a document with the ranks where it was shown, which is the bias the PBM removes.
- **Unbiased learning to rank.** If the clicks follow the PBM and $\gamma_r > 0$ is known, weighting each click at rank $r$ by $1 / \gamma_r$ gives an unbiased estimate of attractiveness. This inverse propensity weighting is the core of [unbiased learning to rank](/unbiased-learning-to-rank/), and the PBM is its usual model of examination.

## Known results in the model

**Only the products are identified.** The likelihood depends on the parameters through the products $\gamma_r \alpha_d$ alone, so $(t \gamma, \alpha / t)$ fits the data exactly as well as $(\gamma, \alpha)$ for every $t > 0$ that keeps all values in $[0, 1]$. One fixes the scale with $\gamma_1 = 1$, or compares the ratios $\gamma_r / \gamma_1$ and the products $\alpha_d \gamma_1$. The ranks are also only separable from the documents if the same document appears at several ranks: if every document always stays at one rank, the data determine only one click rate per pair, and position bias cannot be told apart from attractiveness. Randomized or swapped rankings, as in the experiment of Craswell et al., give the variation that is needed.

**EM updates.** Let $N_{d,r}$ be the number of impressions of $d$ at rank $r$ and $K_{d,r}$ the clicks among them. A click shows $E = A = 1$. For a non-click, Bayes' rule gives

$$P(E = 1 \mid C = 0) = \frac{\gamma_r (1 - \alpha_d)}{1 - \gamma_r \alpha_d}, \qquad P(A = 1 \mid C = 0) = \frac{\alpha_d (1 - \gamma_r)}{1 - \gamma_r \alpha_d}.$$

The M-step sets $\gamma_r$ to the expected examinations at rank $r$ divided by $\sum_d N_{d,r}$, and $\alpha_d$ to the expected attractions of $d$ divided by $\sum_r N_{d,r}$:

$$\gamma_r \leftarrow \frac{\sum_d \big(K_{d,r} + (N_{d,r} - K_{d,r}) P(E = 1 \mid C = 0)\big)}{\sum_d N_{d,r}}, \qquad \alpha_d \leftarrow \frac{\sum_r \big(K_{d,r} + (N_{d,r} - K_{d,r}) P(A = 1 \mid C = 0)\big)}{\sum_r N_{d,r}}.$$

This is the update in the table of Section 4.3 of Chuklin, Markov and de Rijke. Each iteration costs time linear in the number of distinct pairs $(d, r)$, not in the number of sessions. As for any EM, the log likelihood never decreases, but EM may stop at a local maximum or a saddle point, and the result depends on the starting values.

**A simulation.** The tests draw 200000 sessions with a fixed seed, each showing 5 of 10 documents in random order, with $\gamma = (1, 0.7, 0.5, 0.35, 0.25)$ and $\alpha_d$ from $0.10$ to $0.73$. After 1000 EM iterations from $\alpha = \gamma = 0.5$, every ratio $\hat\gamma_r / \hat\gamma_1$ and every product $\hat\alpha_d \hat\gamma_1$ is within $0.004$ of the truth, the fitted scale is $\hat\gamma_1 \approx 0.855$ rather than 1, and the log likelihood rises at every step. The test asserts a tolerance of $0.03$. This is a measurement on simulated data from the model itself; it shows that the fit works, not that real users follow the PBM. In the comparison on a real log in Chapter 7 of Chuklin, Markov and de Rijke, the PBM beats the click-through rate models and the cascade model in log likelihood and perplexity, and comes close to UBM, the best model there, with parameters that are easier to interpret; these are measurements on one log.

**Raw rates are biased.** In the same simulation, the click-through rate of every document is well below its $\alpha_d$, because the average examination over the five ranks is $0.56$. A document shown mostly at the top would look better than an equal document shown lower.

## References
