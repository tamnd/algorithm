---
tag: GNCEJF
kind: problem
slug: recommendation-problem
name: Recommendation problem
aliases:
- item recommendation
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: intro
summary: Given past interactions of users with items, predict the items each user is most likely to rate highly or engage with.
prereqs: []
see_also: [rating-matrix, collaborative-filtering, content-based-filtering, cold-start-problem, learning-to-rank, matrix-completion, contextual-bandit, precision-at-k]
sources:
  - paper: doi:10.1145/963770.963772
    title: Jonathan L. Herlocker, Joseph A. Konstan, Loren G. Terveen and John T. Riedl, Evaluating collaborative filtering recommender systems, ACM Transactions on Information Systems 22(1), 5-53, 2004
    locator: the user tasks of a recommender, the choice of data sets, the accuracy metrics for predicted ratings and for ranked lists, and the measures beyond accuracy
  - paper: doi:10.1109/MC.2009.263
    title: Yehuda Koren, Robert Bell and Chris Volinsky, Matrix factorization techniques for recommender systems, IEEE Computer 42(8), 30-37, 2009
    locator: sections Recommender system strategies (content filtering and collaborative filtering, explicit and implicit feedback) and Netflix Prize competition (the size of the data, the RMSE of Cinematch and the target of the grand prize)
  - paper: doi:10.1145/1401890.1401944
    title: Yehuda Koren, Factorization meets the neighborhood, a multifaceted collaborative filtering model, Proceedings of the 14th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD 2008), 426-434
    locator: the description of the Netflix test set (the Quiz set) and the validation set (the Probe set), and Table 1 (RMSE of factor models on the Netflix test set)
  - paper: doi:10.1137/110820361
    title: Nicolas Gillis and François Glineur, Low-rank matrix approximation with weights or missing data is NP-hard, SIAM Journal on Matrix Analysis and Applications 32(4), 1149-1165, 2011
    locator: the main result (NP-hardness of low-rank approximation with missing data, already for rank one)
  - book: isbn:9783319296579
    title: Charu C. Aggarwal, Recommender Systems, The Textbook, Springer, 2016
    locator: Chapters 2 to 4 (neighborhood, model-based and content-based methods), Chapter 6 (hybrids) and Chapter 7 (evaluation)
---

The recommendation problem asks, from a record of past interactions between users and items, which items each user will rate highly or choose next. Its input is a partly filled [rating matrix](/rating-matrix/), sometimes with features of the items or users, and its output is a predicted rating for each open pair or a ranked list of items for each user. It is a learning problem: the right answer is the future behavior of the users, which is not in the input, so methods are compared by measured error on held out data, not by an exact objective.

## In plain words

A shop, a film service or a news site knows what each customer bought, watched, read or rated. It wants to show each customer a few things that the customer has not seen yet and will probably like. That is the whole task.

Two forms are common. In the first, the system guesses the score that a person would give to a film. In the second, it only has to put the best few items at the top of a short list for each person.

Nobody can check the answer in advance, because it depends on what people will do later. So systems are judged by hiding some of the known data, making guesses for it, and counting how close the guesses were.

## Definition

Let $U$ be a set of $m$ users and $I$ a set of $n$ items. The input is a set $K \subseteq U \times I$ of observed pairs with values $r_{ui}$, which are either explicit ratings on a scale, such as 1 to 5 stars, or implicit records such as a purchase, a click, a count of plays or a viewing time. It may also hold side information: features of the items, features of the users, the time of each interaction, or the context.

Let $I_u = \{ i : (u, i) \in K \}$. The two standard tasks are:

- **Rating prediction.** Output a function $\hat r : U \times I \to \mathbb{R}$, to be used on pairs not in $K$.
- **Top-$N$ recommendation.** For each user $u$, output an ordered list of $N$ items, usually from $I \setminus I_u$.

A method is judged on data it did not see. The usual protocol splits the known pairs into a training part and a test part, fits on the training part, and measures on the test part:

- For rating prediction, the root mean squared error $\sqrt{\frac{1}{|T|} \sum_{(u, i) \in T} (r_{ui} - \hat r_{ui})^2}$ over the test pairs $T$, or the mean absolute error. Lower is better.
- For lists, [precision at $k$](/precision-at-k/), [recall](/precision-and-recall/), and [normalized discounted cumulative gain](/normalized-discounted-cumulative-gain/), with the test items of each user as the relevant set. Higher is better.
- Beyond accuracy, the coverage of the catalog, the novelty and the diversity of the lists, and, in a running system, measured clicks or sales in a controlled experiment.

Herlocker et al. (2004) survey these measures and argue that the choice of measure must match the task that the users want the system to do. No measure is the definition of the problem; each one is a stand-in for future satisfaction.

## Variants

- **Explicit or implicit data.** With [implicit feedback](/implicit-feedback/), the data shows only what users did, not what they disliked, and a missing pair is ambiguous.
- **Rating prediction or ranking.** A method that is good at one need not be good at the other. Ranking losses such as [Bayesian personalized ranking](/bayesian-personalized-ranking/) target the list directly.
- **With or without content.** [Collaborative filtering](/collaborative-filtering/) uses only the interactions, [content-based filtering](/content-based-filtering/) uses item features, and [hybrids](/hybrid-recommender/) use both.
- **New users and items.** The [cold-start problem](/cold-start-problem/) is the case of users or items with few or no interactions.
- **Sessions and sequences.** [Session-based recommendation](/session-based-recommendation/) predicts the next item from the current session, often with no long-term profile.
- **Interactive.** When the system's choices decide what data it sees next, the problem becomes a [contextual bandit](/contextual-bandit/).

## Examples

The toy rating matrix used in this group has four users, four items and 14 known ratings out of 16:

| | $i_1$ | $i_2$ | $i_3$ | $i_4$ |
|---|---|---|---|---|
| $u_1$ | 5 | 4 | - | 1 |
| $u_2$ | 4 | 5 | 4 | 2 |
| $u_3$ | 1 | 2 | 2 | 5 |
| $u_4$ | - | 1 | 1 | 4 |

Rating prediction asks for $\hat r_{u_1 i_3}$ and $\hat r_{u_4 i_1}$. Top-1 recommendation for $u_1$ has only one open item, $i_3$, so the interesting question is the predicted value. Different methods give different answers on the same data, all of them correct outputs of their methods: [user-based filtering](/user-based-collaborative-filtering/) with Pearson weights gives about 3.934, [item-based filtering](/item-based-collaborative-filtering/) with positive adjusted cosine weights about 4.540, and [Slope One](/slope-one/) $53/18 \approx 2.944$. The problem itself does not say which is right; only the true later rating of $u_1$ would.

At large scale, the Netflix Prize data held more than 100 million ratings of about 500,000 customers for more than 17,000 films (Koren, Bell and Volinsky, 2009), and its test set held over 1.4 million recent ratings whose values were not published (Koren, 2008).

## Known algorithms

- **Baselines.** The global mean, the mean of the user or of the item, and the bias model $\mu + b_u + b_i$.
- **Neighborhood methods.** [User-based](/user-based-collaborative-filtering/) and [item-based collaborative filtering](/item-based-collaborative-filtering/), and [Slope One](/slope-one/).
- **Latent factor models.** [Matrix factorization](/matrix-factorization-recommendation/) trained by SGD or by [alternating least squares](/alternating-least-squares/), [SVD++](/svd-plus-plus/), [probabilistic matrix factorization](/probabilistic-matrix-factorization/), and [factorization machines](/factorization-machine/).
- **Implicit data and ranking.** [ALS for implicit feedback](/implicit-feedback-als/), [Bayesian personalized ranking](/bayesian-personalized-ranking/), and [SLIM](/sparse-linear-method/).
- **Neural and sequential models.** [Neural collaborative filtering](/neural-collaborative-filtering/), [GRU4Rec](/gru4rec/) and [SASRec](/sasrec/).
- **Content and hybrids.** [Content-based filtering](/content-based-filtering/) and [hybrid recommenders](/hybrid-recommender/).

## Bounds

Since the target is future behavior, the problem has no complexity in the sense of an exact computational problem, and no method is optimal for all data. What can be stated:

- **Measured values.** On the Netflix test set, the Netflix system Cinematch had an RMSE of 0.9514, and the grand prize asked for 0.8563, a 10 percent improvement (Koren, Bell and Volinsky, 2009). Koren (2008, Table 1) reports values from 0.9046 down to 0.8911 for factor models. These are measurements on one data set and one split.
- **Formulations with exact results.** Once the problem is cast as fitting a low-rank matrix to the known entries, exact statements become possible: fitting the best rank-one matrix to a partly known matrix is NP-hard (Gillis and Glineur, 2011, see [alternating least squares](/alternating-least-squares/)), and the theory of [matrix completion](/matrix-completion/) gives conditions under which a low-rank matrix can be recovered from few entries.
- **The cost of methods.** Each algorithm page gives the time and space of its method.

## Reductions

- **From rating prediction to top-$N$.** Score every open item of a user and keep the $N$ best by [top-$k$ selection](/top-k-selection/). With a factor model, this is [maximum inner product search](/maximum-inner-product-search/).
- **To matrix completion.** Treat the ratings as entries of a matrix assumed to have low rank, see [matrix completion](/matrix-completion/).
- **To supervised learning.** Each known pair becomes a training example with user and item features and the rating as label, as in [linear regression](/linear-regression/) or, for clicks, [logistic regression](/logistic-regression/).
- **To ranking.** Top-$N$ recommendation is a case of [learning to rank](/learning-to-rank/), with the user in the role of the query.
- **To bandits.** When recommendations change the data, the exploration and exploitation trade-off of [multi-armed bandits](/multi-armed-bandit/) appears, and logged data needs [off-policy evaluation](/off-policy-evaluation/).

## Applications

Recommendation is used in online shops, where item-to-item methods suggest products related to those in a customer's history, in film, video and music services, and in news feeds. In search engines, the same signals of clicks are subject to [position bias](/position-bias/), which also affects implicit data for recommendation.

## References
