---
tag: Z3BC5K
kind: concept
slug: implicit-feedback
name: Implicit feedback
aliases:
- one-class collaborative filtering
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Signals such as clicks, plays and purchases that indicate preference indirectly, with no negative examples and varying confidence.
prereqs: [recommendation-problem, rating-matrix]
see_also: [implicit-feedback-als, bayesian-personalized-ranking, sparse-linear-method, neural-collaborative-filtering, session-based-recommendation, click-model, position-bias, collaborative-filtering]
sources:
  - paper: doi:10.1109/ICDM.2008.22
    title: Yifan Hu, Yehuda Koren and Chris Volinsky, Collaborative filtering for implicit feedback datasets, Eighth IEEE International Conference on Data Mining (ICDM 2008), 263-272
    locator: Section 1 (the four characteristics of implicit feedback), Section 4 (preference p_ui, confidence c_ui = 1 + alpha r_ui with alpha = 40, and the log form of Equation 6), Section 6 (expected percentile ranking)
  - paper: doi:10.1109/ICDM.2008.16
    title: Rong Pan, Yunhong Zhou, Bin Cao, Nathan N. Liu, Rajan Lukose, Martin Scholz and Qiang Yang, One-class collaborative filtering, Eighth IEEE International Conference on Data Mining (ICDM 2008), 502-511
    locator: Abstract and Section 1 (the one-class problem, where only positive examples are observed, and weighting or sampling of the missing entries)
  - paper: arxiv:1205.2618
    title: Steffen Rendle, Christoph Freudenthaler, Zeno Gantner and Lars Schmidt-Thieme, BPR, Bayesian personalized ranking from implicit feedback, Proceedings of the 25th Conference on Uncertainty in Artificial Intelligence (UAI 2009), 452-461
    locator: Section 3 (implicit feedback as positive observations only, and the pairwise training set D_S)
---

Implicit feedback is what a recommender learns from when users do not say what they like: it watches what they do. Clicks, plays, purchases, views, time spent and repeat visits are all implicit feedback. The data are plentiful, since every user produces them just by using the system, but they are hard to read. Hu, Koren and Volinsky (2008, Section 1) list four properties that set implicit feedback apart from explicit ratings: there is no negative feedback, the signal is noisy, its numeric value shows confidence rather than preference, and it needs its own evaluation measures. Most recommenders in practice are built on implicit feedback, and several methods on this site were designed for it. The task of learning from such data, where only positive examples are seen, is called one-class collaborative filtering (Pan et al. 2008); that alias names the learning problem rather than the signal.

## In plain words

A rating says "I liked this, 4 out of 5". A click only says "I did something with this". If a user watched a show ten times, they probably like it. If a user never watched a show, you do not know why: maybe they dislike it, maybe they never heard of it. So you have many weak yes signals and no clear no signals. Methods for implicit feedback must treat the unseen items as weak, uncertain negatives, and must use the number of actions as a measure of how sure you are, not of how much the user likes the item.

## The idea

**Data.** For users $u$ and items $i$, the raw data are counts or amounts $r_{ui} \ge 0$: how many times $u$ bought $i$, or what fraction of a show $u$ watched. Most $r_{ui}$ are 0. Unlike a [rating matrix](/rating-matrix/) with explicit ratings, the zeros are not missing values. They are observations, of an uncertain kind.

**The four properties (Hu et al. 2008, Section 1).**

1. *No negative feedback.* The data show what users chose, not what they rejected. A recommender for explicit ratings can ignore the missing entries, but with implicit data the observed entries are almost all positive, so ignoring the rest leaves nothing to contrast them with. The missing entries are where most of the negative signal is.
2. *Noise.* A purchase may be a gift; a television may be on a channel while the viewer sleeps.
3. *The value shows confidence, not preference.* Watching a series every week does not mean the user likes it more than a film they watched once. But a repeated action is more likely to reflect a real preference than a single one.
4. *Evaluation needs its own measures.* There is no true rating to compare with, so squared error does not apply. Evaluation must deal with item availability, items that compete for the same time, and repeated actions.

**Preference and confidence (Hu et al. 2008, Section 4).** Split each raw value into a binary preference $p_{ui} = 1$ if $r_{ui} > 0$ and $0$ otherwise, and a confidence $c_{ui} = 1 + \alpha r_{ui}$. Every pair, observed or not, gets at least confidence 1, and repeated actions get more. The authors found $\alpha = 40$ to work well on their data, and also give the form $c_{ui} = 1 + \alpha \log(1 + r_{ui} / \epsilon)$. Fitting factors to $p_{ui}$ with weights $c_{ui}$ over all pairs is [ALS for implicit feedback](/implicit-feedback-als/).

**Three ways to treat the unobserved pairs.**

- *All pairs, weighted.* Treat every unobserved pair as a negative with low weight, as above. This needs algebra that avoids touching every pair, since there are $|U| \cdot |I|$ of them.
- *Sampling.* Draw some unobserved pairs as negatives at each step, as in [neural collaborative filtering](/neural-collaborative-filtering/) and in the weighting and sampling schemes of Pan et al. (2008).
- *Pairs of items.* Assume only that a user prefers an item they acted on to one they did not, and learn a ranking from such pairs, as in [Bayesian personalized ranking](/bayesian-personalized-ranking/) (Rendle et al. 2009, Section 3).

**Evaluation.** Offline evaluation hides some observed actions and checks where the model ranks them: hit rate or recall at $k$, [mean reciprocal rank](/mean-reciprocal-rank/), [NDCG](/normalized-discounted-cumulative-gain/), AUC, or the expected percentile ranking of Hu et al. (2008, Section 6). All of these are measurements on a data set. Whether one way of handling implicit feedback is better than another is measured, never proved, and the answer depends on the data and the protocol.

## Examples

- **Television.** Hu et al. built their method for a TV recommender with about 300,000 set-top boxes and about 17,000 programs over four weeks, where $r_{ui}$ was how much of program $i$ box $u$ watched (Section 6).
- **Shopping.** Purchase counts and add-to-cart events. A single purchase is weak evidence; repeat purchases are stronger.
- **Music and video streaming.** Play counts and the fraction of a track or video that was played. Skipping after a few seconds is a weak negative, one of the few negatives that implicit data give.
- **Web search.** Clicks on search results are implicit feedback on the ranking. They depend strongly on the position of the result, which is the subject of [position bias](/position-bias/) and of [click models](/click-model/).
- **Sessions.** The ordered clicks of one anonymous visit are the input to [session-based recommendation](/session-based-recommendation/).

A small example of the preference and confidence split, with $\alpha = 40$: a user watched show A three times and show B once, and never watched show C. Then $p = (1, 1, 0)$ and $c = (121, 41, 1)$. The model is pushed hard to score A high, less hard for B, and only weakly to score C low.

## Where it is used

- [ALS for implicit feedback](/implicit-feedback-als/) fits the weighted preference model over all user-item pairs.
- [Bayesian personalized ranking](/bayesian-personalized-ranking/) learns from pairs of an observed and an unobserved item.
- [SLIM](/sparse-linear-method/) learns a sparse item-item weight matrix from a binary purchase or click matrix.
- [Neural collaborative filtering](/neural-collaborative-filtering/) trains on observed pairs and sampled negatives with a log loss.
- [GRU4Rec](/gru4rec/) and [SASRec](/sasrec/) learn from sequences of clicks or other actions.
- [Item-based collaborative filtering](/item-based-collaborative-filtering/) is often run on co-purchase or co-view counts.

## References
