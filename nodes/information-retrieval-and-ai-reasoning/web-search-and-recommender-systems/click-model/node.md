---
tag: B3RJ18
kind: concept
slug: click-model
name: Click model
aliases:
- user click model
- click model for web search
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: A probabilistic model of how users examine and click a ranked list, used to infer relevance from clicks and to simulate users.
prereqs: [position-bias, bayesian-network]
see_also: [cascade-click-model, position-based-click-model, dbn-click-model, expectation-maximization, maximum-likelihood-estimation, unbiased-learning-to-rank, expected-reciprocal-rank, interleaved-evaluation]
sources:
  - book: isbn:9783031011665
    title: Aleksandr Chuklin, Ilya Markov and Maarten de Rijke, Click Models for Web Search, Morgan and Claypool 2015, reissued by Springer
    locator: Section 1.2 (historical notes), Chapter 2 (terminology and Bayesian networks), Chapter 3 (basic click models, Sections 3.1 to 3.9), Chapter 4 (MLE and EM estimation), Chapter 5 (evaluation, with log likelihood in Section 5.1 and perplexity in Section 5.2, Equation 5.4), Chapter 7 (an experimental comparison) and Chapter 9 (applications)
  - paper: doi:10.1145/1341531.1341545
    title: Nick Craswell, Onno Zoeter, Michael Taylor and Bill Ramsey, An experimental comparison of click position-bias models, Proceedings of the 2008 International Conference on Web Search and Data Mining (WSDM 2008), 87-94
    locator: the cascade model and the comparison of four position-bias models on an experiment that swaps adjacent results
  - paper: doi:10.1145/1390334.1390392
    title: Georges E. Dupret and Benjamin Piwowarski, A user browsing model to predict search engine click data from past observations, Proceedings of the 31st Annual International ACM SIGIR Conference (SIGIR 2008), 331-338
    locator: the user browsing model, in which examination depends on the rank and the distance to the previous click, and perplexity as a measure of click prediction
  - paper: doi:10.1145/1526709.1526711
    title: Olivier Chapelle and Ya Zhang, A dynamic Bayesian network click model for web search ranking, Proceedings of the 18th International Conference on World Wide Web (WWW 2009), 1-10
    locator: the DBN model with attractiveness, satisfaction and perseverance
---

A click model is a probabilistic model of how a user examines and clicks the results of one query on a ranked list, written as a set of hidden events (examination, attraction, satisfaction) and observed clicks. Its parameters are fitted to search logs, and it is used to estimate the relevance of documents from clicks with [position bias](/position-bias/) removed, to predict clicks, and to simulate users. Chuklin, Markov and de Rijke trace the term to the 2008 paper of Nick Craswell, Onno Zoeter, Michael Taylor and Bill Ramsey that introduced the [cascade model](/cascade-click-model/), in their survey of the field. This page covers the common ideas; the [cascade](/cascade-click-model/), [position-based](/position-based-click-model/) and [DBN](/dbn-click-model/) models have their own pages.

## In plain words

A search log says which results people clicked, but not why. A result may get no click because it was bad, or because nobody scrolled down to it. A click model is a small story about a user that explains the clicks: the user looks at some results, likes some of them, clicks, and maybe stops. Each part of the story has a probability. If you choose the probabilities so that the story produces clicks like those in the log, you learn how far people read and how good each result is. You can then use the story to guess how people would click on a new ranking.

## The idea

A query session shows a ranking $d_1, \ldots, d_n$ and records clicks $c_1, \ldots, c_n$. A click model is a [Bayesian network](/bayesian-network/) over these clicks and some hidden events per rank:

- **Examination** $E_r$: the user looks at the snippet at rank $r$.
- **Attraction** $A_r$: the snippet looks relevant, with a probability $\alpha_d$ for the document. Almost all models use the examination hypothesis, $C_r = 1$ exactly when $E_r = 1$ and $A_r = 1$.
- **Satisfaction** $S_r$: after a click, the document meets the need and the user stops.

The models differ in what examination depends on:

| model | examination of rank $r$ |
|---|---|
| click-through rate models | every rank, or a constant per rank, with no hidden events |
| [position-based model](/position-based-click-model/) | a probability $\gamma_r$ for the rank alone |
| [cascade model](/cascade-click-model/) | all results above were examined and skipped |
| user browsing model | the rank and the rank of the previous click |
| dependent and click chain models | a cascade that can go on after a click |
| [DBN model](/dbn-click-model/) | a cascade that goes on with probability $\gamma$ unless the user is satisfied |

**Estimation.** When the model makes every hidden event observable from the clicks, as the cascade model does by treating every result above the click as examined, the [maximum likelihood](/maximum-likelihood-estimation/) estimates are ratios of counts. Otherwise the parameters are fitted by [EM](/expectation-maximization/), which needs the posterior of the hidden events in each session (Chapter 4 of Chuklin, Markov and de Rijke).

**Evaluation.** A click model is judged by how well it predicts held-out clicks: by log likelihood, and by perplexity, $2$ to the power of the average negative $\log_2$ probability of the observed click at each rank (Equation 5.4 of Chuklin, Markov and de Rijke, after Dupret and Piwowarski). A perfect prediction has perplexity 1, a coin with probability $0.5$ has perplexity 2, and lower is better. All such comparisons are measurements on a particular log; a better fit on one engine's users is not a law about users in general.

## Examples

**Same click rates, different users.** Take the ranking a, b, c with attractiveness $0.5$, $0.4$ and $0.2$. The cascade model gives click rates $0.5$, $0.5 \cdot 0.4 = 0.2$ and $0.5 \cdot 0.6 \cdot 0.2 = 0.06$. A position-based model with $\gamma = (1, 0.5, 0.3)$ gives the same three rates. Yet the two models describe different users:

- The cascade user never clicks twice, while the position-based user clicks both a and b with probability $0.5 \cdot 0.2 = 0.1$.
- If b and a are swapped, the cascade model predicts $0.4$ for b and $0.6 \cdot 0.5 = 0.3$ for a, because a is now examined only when b is skipped. The position-based model predicts $0.4$ and $0.5 \cdot 0.5 = 0.25$.

So the logs of a single ranking cannot tell the models apart, and experiments that change the order, such as the swaps of Craswell et al., are what separate them.

**Relevance from clicks.** In the [DBN model](/dbn-click-model/), the product of attractiveness and satisfaction, $a_d s_d$, is the probability that an examined document both gets a click and satisfies the user. Chapelle and Zhang use it as a relevance estimate from logs.

**Comparison on a real log.** In Chapter 7 of Chuklin, Markov and de Rijke, on a public log of a commercial search engine, the models with hidden examination (PBM, UBM, DCM variants, the click chain model, DBN and its simplified form) all beat the click-through rate models and the cascade model in log likelihood and perplexity, and UBM tends to have the highest log likelihood. These are measurements on that log.

## Where it is used

- **Relevance estimation.** Click model parameters serve as labels or features for [learning to rank](/learning-to-rank/), with position bias taken out.
- **Unbiased learning to rank.** The examination probabilities of a fitted model are the propensities in [unbiased learning to rank](/unbiased-learning-to-rank/).
- **Evaluation metrics.** Metrics such as [expected reciprocal rank](/expected-reciprocal-rank/) assume a model of the user, in that case a cascade with satisfaction.
- **Simulation.** A fitted model generates realistic clicks to test online learning and [interleaving](/interleaved-evaluation/) methods without live users (Chapter 9 of Chuklin, Markov and de Rijke).
- **Understanding users.** The fitted examination and perseverance parameters show how far people read on different queries, devices and page layouts.

## References
