---
tag: EGNDGE
kind: technique
slug: hybrid-recommender
name: Hybrid recommender
aliases:
- hybrid recommendation
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Combines collaborative and content-based signals, by weighting, switching, cascading or feature combination, to offset each one's weaknesses.
prereqs: [collaborative-filtering, content-based-filtering]
see_also: [collaborative-filtering, content-based-filtering, cold-start-problem, factorization-machine, ensemble-learning, stacking, svd-plus-plus, learning-to-rank]
sources:
  - paper: doi:10.1023/A:1021240730564
    title: Robin Burke, Hybrid recommender systems, survey and experiments, User Modeling and User-Adapted Interaction 12(4), 331-370, 2002
    locator: the classes of recommendation techniques and the seven hybridization methods (weighted, switching, mixed, feature combination, cascade, feature augmentation, meta-level)
  - book: isbn:9783319296579
    title: Charu C. Aggarwal, Recommender Systems, The Textbook, Springer, 2016
    locator: Chapter 6 (ensemble-based and hybrid recommender systems)
  - paper: doi:10.1109/MC.2009.263
    title: Yehuda Koren, Robert Bell and Chris Volinsky, Matrix factorization techniques for recommender systems, IEEE Computer 42(8), 30-37, 2009
    locator: sections Recommender system strategies (the weak and strong points of content filtering and collaborative filtering) and Additional input sources (user attributes and implicit feedback added to the factor model)
---

A hybrid recommender combines two or more recommendation methods, most often [collaborative filtering](/collaborative-filtering/) and [content-based filtering](/content-based-filtering/), so that the strong points of one cover the weak points of the other. Collaborative methods capture taste that no feature describes but know nothing about new items; content methods handle new items but tend to recommend more of the same. Burke (2002) sorts the ways to combine them into seven methods, from a weighted sum of scores to models that use the output of one method as the input of another.

## In plain words

One adviser knows what people like you enjoyed. Another adviser knows what each product is. Each one makes mistakes the other would not make. A hybrid asks both and combines their answers, or lets one adviser go first and the other refine the result, or simply asks the second adviser when the first has no opinion.

The combination can be simple, like an average of two scores, or it can be one model that learns from ratings and descriptions at the same time.

## When it applies

- **Both kinds of data exist.** There are interactions and also item or user features.
- **Cold start matters.** New items or new users arrive often, see the [cold-start problem](/cold-start-problem/), and a purely collaborative method would ignore them.
- **One method alone has a known gap.** For example, the content method gives lists with no variety, or the collaborative method gives noisy results for items with few ratings.
- **Several good models exist.** Even among collaborative models alone, a blend of different methods can make smaller errors than each one, which is the idea of [ensemble learning](/ensemble-learning/).

## The template

1. **Choose the components.** For example, a collaborative predictor $\hat r^{\mathrm{cf}}_{ui}$ and a content predictor $\hat r^{\mathrm{cb}}_{ui}$, each trained as on its own page.
2. **Choose the way to combine them**, one of the seven methods of Burke (2002):
   - *Weighted.* $\hat r_{ui} = \alpha \hat r^{\mathrm{cf}}_{ui} + (1 - \alpha) \hat r^{\mathrm{cb}}_{ui}$, or a learned combination of several scores.
   - *Switching.* Use one component when a condition holds, for example the collaborative one when the item has at least $c$ ratings, and the other otherwise.
   - *Mixed.* Show the lists of both components side by side, or merge them.
   - *Feature combination.* Give one learner both kinds of data, for example a model that takes the ratings of other users as extra features next to the content features.
   - *Cascade.* Let one component produce a coarse ranking and the second break ties or reorder only the candidates of the first.
   - *Feature augmentation.* Let one component compute a feature, such as a predicted rating or a category, that becomes input of the other.
   - *Meta-level.* Let one component learn a model, such as a content profile of each user, and give that model, not the raw data, to the other, for example to compare users by their profiles.
3. **Fit the combination on held out data.** Learn $\alpha$, the switching condition or the second stage on data that the components did not train on, so that the combination does not favor the component that overfits most.
4. **Evaluate** with the measures of the [recommendation problem](/recommendation-problem/), and separately on new users and new items.

## Classic examples

On the toy matrix of this group, take the item features of the [content-based filtering](/content-based-filtering/) page: $i_1 = (1, 1, 0)$, $i_2 = (1, 0, 0)$, $i_3 = (1, 0, 0)$, $i_4 = (0, 1, 1)$, and a new item $i_5 = (0, 0, 1)$ that nobody has rated. As a content predictor, use a neighbor method on the features: predict $\mu_u$ plus the average of $r_{uj} - \mu_u$ over the items $j$ that $u$ rated, with the cosine of the feature vectors of $i$ and $j$ as weights. User $u_1$ has the mean $10/3$ and rated $i_1$, $i_2$ and $i_4$.

| open pair | collaborative ([user-based](/user-based-collaborative-filtering/)) | content | weighted, $\alpha = 1/2$ | switching |
|---|---|---|---|---|
| $(u_1, i_3)$ | about 3.934 | $3 + \sqrt 2 \approx 4.414$ | about 4.174 | about 3.934 |
| $(u_1, i_5)$ | none, no ratings of $i_5$ | 1 | none | 1 |

For $i_3$ the weights are $1/\sqrt 2$ for $i_1$, 1 for $i_2$ and 0 for $i_4$, which gives $10/3 + (\frac{5}{3\sqrt 2} + \frac{2}{3}) / (\frac{1}{\sqrt 2} + 1) = 3 + \sqrt 2$. For $i_5$ only $i_4$ has a nonzero weight, so the prediction is the rating 1 that $u_1$ gave to the comedy $i_4$. A plain weighted hybrid has no answer for $i_5$, because one of its parts has none; the switching hybrid, with the rule "use the collaborative score when the item has ratings", answers both pairs.

Other examples:

- **Blends of collaborative models.** The leading teams of the Netflix Prize combined many neighborhood and factor models with learned weights, a weighted hybrid in which all components are collaborative.
- **Side information in the factor model.** Koren, Bell and Volinsky (2009) add user attributes and implicit feedback to the factor vector of a user, a feature combination inside one model; [SVD++](/svd-plus-plus/) is the implicit feedback part of this.
- **Factorization machines.** A [factorization machine](/factorization-machine/) takes one feature vector that holds the user, the item and any content or context features, and learns factors for all of them at once.

## Variations

- **Learned blending.** Replace the fixed $\alpha$ by a model, such as [linear regression](/linear-regression/) or [gradient boosting](/gradient-boosting/), that takes the component scores and also counts such as the number of ratings of the user and item. This is [stacking](/stacking/).
- **Confidence-based weighting.** Let $\alpha$ grow with the number of ratings of the item, so that the collaborative score takes over as data arrives.
- **Two-stage systems.** A fast candidate stage, often content or embedding based, and an accurate ranking stage, often trained by [learning to rank](/learning-to-rank/), form a cascade.

## Pitfalls

- **Scales that differ.** A rating prediction and a cosine score are not on the same scale. Normalize them before a weighted sum.
- **Leakage in the blend.** If the weights are fit on the same data the components trained on, the blend trusts the component that memorized the training data.
- **Cost.** Every component must be trained, stored and served, and a cascade adds latency.
- **Hiding a gap.** A hybrid that is good on average can still be poor for new users; measure the cold-start cases on their own.
- **Explanations.** A blended score is harder to explain than the output of one method.

## Exercises

1. On the example, find $\alpha$ such that the weighted hybrid gives 4 for $(u_1, i_3)$. *Hint: solve $3.934 \alpha + 4.414 (1 - \alpha) = 4$.*
2. For each of the seven methods of Burke (2002), say whether it can recommend a new item that has features but no ratings, when one component is collaborative and the other content-based.
3. Design a switching rule on the number of ratings of the item, and explain how to choose its threshold on held out data.
4. Explain why the weighted sum of two predictors with errors that are not correlated can have a smaller mean squared error than both. *Hint: expand the square of $\alpha e_1 + (1 - \alpha) e_2$.*

## References
