---
tag: JD0Z3X
kind: technique
slug: collaborative-filtering
name: Collaborative filtering
aliases:
- CF
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: intro
summary: Recommends items from the behavior of many users, assuming users who agreed in the past will agree again, with no item content.
prereqs: [recommendation-problem, rating-matrix]
see_also: [user-based-collaborative-filtering, item-based-collaborative-filtering, matrix-factorization-recommendation, content-based-filtering, hybrid-recommender, cold-start-problem, k-nearest-neighbors, implicit-feedback]
sources:
  - paper: doi:10.1145/138859.138867
    title: David Goldberg, David Nichols, Brian M. Oki and Douglas Terry, Using collaborative filtering to weave an information tapestry, Communications of the ACM 35(12), 61-70, 1992
    locator: the Tapestry system, in which users annotate documents and filter on the annotations of other users
  - paper: doi:10.1145/192844.192905
    title: Paul Resnick, Neophytos Iacovou, Mitesh Suchak, Peter Bergstrom and John Riedl, GroupLens, an open architecture for collaborative filtering of netnews, Proceedings of the ACM Conference on Computer Supported Cooperative Work (CSCW 1994), 175-186
    locator: the automatic prediction of a user's rating from the ratings of users who agreed with that user in the past
  - paper: doi:10.1145/371920.372071
    title: Badrul Sarwar, George Karypis, Joseph Konstan and John Riedl, Item-based collaborative filtering recommendation algorithms, Proceedings of the 10th International World Wide Web Conference (WWW 2001), 285-295
    locator: Section 3 (item similarities and the precomputed model of similar items)
  - paper: doi:10.1109/MIC.2003.1167344
    title: Greg Linden, Brent Smith and Jeremy York, Amazon.com recommendations, item-to-item collaborative filtering, IEEE Internet Computing 7(1), 76-80, 2003
    locator: the offline table of similar items built from the items that customers buy together
  - paper: doi:10.1109/MC.2009.263
    title: Yehuda Koren, Robert Bell and Chris Volinsky, Matrix factorization techniques for recommender systems, IEEE Computer 42(8), 30-37, 2009
    locator: section Recommender system strategies (content filtering against collaborative filtering, neighborhood methods and latent factor models, and the cold start problem)
  - book: isbn:9783319296579
    title: Charu C. Aggarwal, Recommender Systems, The Textbook, Springer, 2016
    locator: Chapter 2 (neighborhood-based collaborative filtering) and Chapter 3 (model-based collaborative filtering)
---

Collaborative filtering predicts what a user will like from the recorded behavior of many users: ratings, purchases, clicks or views. It assumes that users who agreed in the past will agree again, so it needs no description of the items, only the [rating matrix](/rating-matrix/). The two main families are neighborhood methods, which compare users or items directly on their common ratings, and latent factor models, which explain all ratings by a small number of hidden factors per user and per item.

## In plain words

If you and a friend liked the same ten films, and your friend also liked an eleventh film that you have not seen, there is a good chance that you will like it too. Collaborative filtering does this with thousands of people at once. It looks for people whose past choices match yours, or for items that the same people tend to like together, and it uses these patterns to fill in the films you have not rated.

It never looks at what an item is about. The same method works for films, songs, books or shop products, because it uses only who liked what.

## When it applies

- **Many users share items.** The method needs overlap: users must have rated some of the same items, and items must have some of the same users.
- **Taste is shared.** It works when preferences fall into patterns that many users follow, such as genres or styles, even if nobody names them.
- **Item content is poor or hard to use.** Films, music or jokes are hard to describe by features that predict taste; the ratings carry that signal.
- **Not for brand new users or items.** A user or item with no interactions has nothing to compare, see the [cold-start problem](/cold-start-problem/). Then [content-based filtering](/content-based-filtering/) or a [hybrid](/hybrid-recommender/) is needed.

## The template

1. **Collect the interactions** into a sparse [rating matrix](/rating-matrix/) $R$ with known pairs $K$. Decide whether the values are explicit ratings or implicit events.
2. **Normalize.** Remove the effects that are not about taste: the global mean $\mu$, the bias of each user, who may rate everything high, and the bias of each item. Many methods work on $r_{ui} - \mu_u$ or on $r_{ui} - (\mu + b_u + b_i)$.
3. **Choose how agreement is modeled.**
   - *Neighborhood (memory-based).* Measure the similarity of two users on their co-rated items, or of two items on their common users, for example by Pearson correlation or adjusted [cosine similarity](/cosine-similarity/), and predict from the $k$ most similar neighbors, as in [$k$-nearest neighbors](/k-nearest-neighbors/).
   - *Latent factors (model-based).* Give each user and item a vector of $r$ numbers and fit them so that $\hat r_{ui} = p_u^\top q_i$, plus biases, matches the known ratings, as in [matrix factorization](/matrix-factorization-recommendation/).
4. **Fit on the known pairs only.** A blank is unknown, not zero.
5. **Predict and rank.** Score the open items of each user, add back the normalization of step 2, and keep the best $N$ by [top-$k$ selection](/top-k-selection/).
6. **Evaluate on held out data**, with the measures of the [recommendation problem](/recommendation-problem/), and tune the neighborhood size, the number of factors and the penalties there.

## Classic examples

- **Tapestry (1992).** Goldberg, Nichols, Oki and Terry coined the term for a mail system in which users annotated messages, and others filtered on these annotations. The collaboration was manual: a user wrote filters that referred to the annotations of other, named users.
- **GroupLens (1994).** Resnick et al. made the process automatic for Usenet news: [user-based collaborative filtering](/user-based-collaborative-filtering/) with Pearson weights over co-rated articles.
- **Item-to-item filtering.** Sarwar et al. (2001) compared items instead of users, and Linden, Smith and York (2003) described the item-to-item method of Amazon.com, see [item-based collaborative filtering](/item-based-collaborative-filtering/). [Slope One](/slope-one/) is a simple item-pair method that updates online.
- **The Netflix Prize (2006 to 2009).** Latent factor models, such as [matrix factorization](/matrix-factorization-recommendation/), [alternating least squares](/alternating-least-squares/) and [SVD++](/svd-plus-plus/), together with neighborhood models, gave the most accurate predictions on the competition data.

On the toy matrix of this group, user $u_1$ rated $i_1$ high and $i_4$ low, as $u_2$ did, and opposite to $u_3$ and $u_4$. A user-based method predicts the open rating $r_{u_1 i_3}$ from the high rating 4 of the agreeing user $u_2$ and from the low ratings 2 and 1 of the disagreeing users, read in reverse; the [user-based page](/user-based-collaborative-filtering/) works it out to about 3.934.

## Variations

- **User-based or item-based.** Item-based methods precompute a table of similar items, which is often smaller and more stable than a table of similar users when there are many more users than items.
- **Explicit or implicit.** With [implicit feedback](/implicit-feedback/) the matrix holds events, and the methods change: [ALS for implicit feedback](/implicit-feedback-als/), [Bayesian personalized ranking](/bayesian-personalized-ranking/) and [SLIM](/sparse-linear-method/).
- **Probabilistic and neural models.** [Probabilistic matrix factorization](/probabilistic-matrix-factorization/) gives the factor model a Gaussian likelihood; [neural collaborative filtering](/neural-collaborative-filtering/) replaces the dot product by a learned function.
- **Sequential.** [Session-based recommendation](/session-based-recommendation/), with models such as [GRU4Rec](/gru4rec/) and [SASRec](/sasrec/), uses the order of the interactions.
- **With side information.** [Factorization machines](/factorization-machine/) and [hybrid recommenders](/hybrid-recommender/) add item or user features.

## Pitfalls

- **Sparsity.** Two users often share very few items, and a similarity computed on one or two co-rated items is noise. Shrink such similarities, or use a factor model.
- **Popularity.** Popular items have many ratings and enter most neighborhoods, so the lists can fill with what everybody already knows. Measure coverage and novelty, not only accuracy.
- **Missing not at random.** Users rate what they chose to consume, so the known ratings are biased toward liked items. A model fit to them can predict too high for the items users avoided.
- **Cold start.** New users and items get no personal prediction until they have interactions.
- **Feedback loops.** The system's own recommendations shape the data it learns from next. See [position bias](/position-bias/) and [off-policy evaluation](/off-policy-evaluation/).
- **Scale.** Comparing all pairs of users costs $O(m^2)$ similarities. Precompute item neighbors, sample, or use approximate methods such as [locality-sensitive hashing](/locality-sensitive-hashing/).

## Exercises

1. On the toy matrix of the [rating matrix](/rating-matrix/) page, list the co-rated items of each pair of users. Which pair shares the fewest, and why does that make its similarity less reliable? *Hint: $u_1$ and $u_4$ share only $i_2$ and $i_4$.*
2. Show that if one user adds 1 to all of their ratings, a prediction for that user of the form $\mu_u + \sum_v w_v (r_{vi} - \mu_v) / \sum_v |w_v|$ also rises by 1, and the predictions for other users do not change when the weights are Pearson correlations. *Hint: Pearson correlation does not change when one of its two vectors is shifted.*
3. A shop has 10 million customers and 100,000 products. Compare the number of user pairs and item pairs, and explain which neighborhood method is cheaper to precompute.
4. Explain why a model that fits the dense matrix with zeros in the blanks recommends badly, even if it fits that matrix well. *Hint: what does it predict for an item a user has never seen?*

## References
