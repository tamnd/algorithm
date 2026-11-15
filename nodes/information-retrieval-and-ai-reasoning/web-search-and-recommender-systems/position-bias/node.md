---
tag: YZNN21
kind: concept
slug: position-bias
name: Position bias
aliases:
- presentation bias in clicks
- rank bias
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Users click results near the top more often regardless of relevance, so raw click rates are biased toward higher positions.
prereqs: [ranked-retrieval]
see_also: [click-model, position-based-click-model, cascade-click-model, dbn-click-model, unbiased-learning-to-rank, interleaved-evaluation, team-draft-interleaving, learning-to-rank]
sources:
  - paper: doi:10.1145/1076034.1076063
    title: Thorsten Joachims, Laura Granka, Bing Pan, Helene Hembrooke and Geri Gay, Accurately interpreting clickthrough data as implicit feedback, Proceedings of the 28th Annual International ACM SIGIR Conference (SIGIR 2005), 154-161
    locator: Section 3.1 (an eye-tracking study with Google results in normal, swapped and reversed order), Section 4.1 (the first two results are viewed about equally but the first gets many more clicks), Section 5.2.1 (trust bias, also under the swapped order), Section 5.2.2 (quality bias) and the Click > Skip Above strategy for relative preferences
  - paper: doi:10.1145/1341531.1341545
    title: Nick Craswell, Onno Zoeter, Michael Taylor and Bill Ramsey, An experimental comparison of click position-bias models, Proceedings of the 2008 International Conference on Web Search and Data Mining (WSDM 2008), 87-94
    locator: four models of position bias compared on an experiment that swaps adjacent results, with the cascade model as the best fit at the top ranks
  - paper: doi:10.1145/1242572.1242643
    title: Matthew Richardson, Ewa Dominowska and Robert Ragno, Predicting clicks, estimating the click-through rate for new ads, Proceedings of the 16th International Conference on World Wide Web (WWW 2007), 521-530
    locator: the factorization of the click probability of an ad into the probability that its position is seen and the probability of a click once seen
  - book: isbn:9783031011665
    title: Aleksandr Chuklin, Ilya Markov and Maarten de Rijke, Click Models for Web Search, Morgan and Claypool 2015, reissued by Springer
    locator: Section 1.2 (historical notes on position bias and click models) and Section 3.3 (the examination hypothesis and the position-based model)
---

Position bias is the effect that results shown near the top of a ranked list get more clicks than results lower down, even when they are no more relevant. A click therefore measures two things at once: whether the user saw the result, which depends mostly on its position, and whether the result looked useful once seen. Raw click-through rates are biased toward whatever the current ranking puts on top, so a system that learns from them tends to confirm its own ranking. [Click models](/click-model/) such as the [position-based model](/position-based-click-model/) and the [cascade model](/cascade-click-model/) are the standard way to separate the two parts, and [unbiased learning to rank](/unbiased-learning-to-rank/) corrects the bias when training a ranker.

## In plain words

People read a results page from the top, and many never look past the first few results. So the first result gets clicks just because it is first. People also trust the search engine: if it puts something first, they assume it must be good. If you count clicks to decide which result is best, the result that was already on top wins, whether or not it deserved the place. To learn from clicks, you have to ask how often a result would be clicked if everybody had seen it, not how often it was clicked where it happened to be shown.

## The idea

Most click models use the examination hypothesis: a result is clicked exactly when the user examines it and is attracted by it. In the simplest form, the position-based model, rank $r$ is examined with probability $\gamma_r$ and document $d$ attracts with probability $\alpha_d$, so

$$P(\text{click on } d \text{ at rank } r) = \gamma_r \, \alpha_d.$$

Position bias is the decrease of $\gamma_r$ with $r$. A raw click-through rate estimates $\gamma_r \alpha_d$, averaged over the ranks where $d$ was shown, and not $\alpha_d$. In the cascade model the bias also depends on the documents above: a result is examined only if all results above it were skipped.

Joachims, Granka, Pan, Hembrooke and Gay measured the effect with eye tracking on Google result pages in 2005. The first two results were viewed about equally often, but the first got many more clicks. When the top two results were swapped, users still clicked the first more often even when the second was judged more relevant, which they called trust bias. When the whole list was reversed, users clicked less relevant results than before, so a click also depends on the quality of the other results, which they called quality bias. Their conclusion was that clicks are unreliable as absolute judgments of relevance but reasonably accurate as relative judgments: a clicked result is probably better than a skipped result above it. These findings are measurements from a laboratory study with students.

Three ways to deal with the bias follow from this:

- **Model it.** Fit a [click model](/click-model/) to the logs and use its attractiveness or satisfaction parameters as the relevance signal.
- **Weight it out.** If $\gamma_r$ is known, a click at rank $r$ weighted by $1/\gamma_r$ is an unbiased estimate of attractiveness. This inverse propensity weighting is the basis of [unbiased learning to rank](/unbiased-learning-to-rank/). The propensities $\gamma_r$ come from randomized experiments, such as swapping results, or from a fitted click model.
- **Compare within one list.** Use relative preferences, such as Click > Skip Above, or compare two rankers by [interleaving](/interleaved-evaluation/) their results into one list, so that both face the same position bias.

## Examples

**The same document at two ranks.** With $\gamma = (1, 0.7, 0.5, 0.35, 0.25)$, a document with $\alpha = 0.4$ gets a click-through rate of $0.4$ at rank 1 and $0.4 \cdot 0.25 = 0.1$ at rank 5. Nothing about the document changed.

**A better document that looks worse.** Document A with $\alpha = 0.3$ is always shown at rank 1, and document B with $\alpha = 0.5$ at rank 3. Their click rates are $0.3$ and $0.5 \cdot 0.5 = 0.25$, so the raw rates rank A above B, the reverse of the truth. Dividing each click by the examination probability of its rank gives $0.3 / 1$ and $0.25 / 0.5 = 0.5$, the correct order. If A and B never change places, though, the data alone cannot tell the examination at rank 3 apart from the attractiveness of B: the correction needs $\gamma$ from a randomized experiment or from data where documents move between ranks.

**Fit from simulated logs.** The tests of the position-based model page simulate 200000 sessions with the $\gamma$ above and recover every ratio $\gamma_r / \gamma_1$ within $0.004$ by EM, while the raw click rates of all ten documents fall far below their true attractiveness. That is a measurement on data drawn from the model itself.

## Where it is used

- **Learning to rank from clicks.** Click logs are the largest source of training data for web search and recommendation, and without correction a [learning to rank](/learning-to-rank/) model learns the old ranking back.
- **Online evaluation.** [Interleaving](/interleaved-evaluation/), for example [team-draft interleaving](/team-draft-interleaving/), compares rankers inside one list so that position bias affects both equally.
- **Ad click prediction.** Sponsored search separates the effect of the ad slot from the quality of the ad, as in the model of Richardson, Dominowska and Ragno.
- **Recommendation feeds and carousels.** Items at the top of a feed or the left of a carousel get more interactions for the same reason, and the same corrections apply.
- **Click models.** The [cascade](/cascade-click-model/), [position-based](/position-based-click-model/) and [DBN](/dbn-click-model/) models are different hypotheses about where position bias comes from.

## References
