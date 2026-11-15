---
tag: F32JTH
kind: concept
slug: cold-start-problem
name: Cold-start problem
aliases:
- new user and new item problem
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Collaborative methods give poor or no personal recommendations for new users and new items, which have few or no interactions to learn from.
prereqs: [collaborative-filtering, content-based-filtering]
see_also: [content-based-filtering, hybrid-recommender, multi-armed-bandit, contextual-bandit, thompson-sampling, ucb1, session-based-recommendation, svd-plus-plus]
sources:
  - paper: doi:10.1145/564376.564421
    title: Andrew I. Schein, Alexandrin Popescul, Lyle H. Ungar and David M. Pennock, Methods and metrics for cold-start recommendations, Proceedings of the 25th Annual International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2002), 253-260
    locator: the recommendation of items that have no ratings, by a probabilistic model that combines content and collaborative data, and the measures proposed for that setting
  - paper: doi:10.1145/1401890.1401944
    title: Yehuda Koren, Factorization meets the neighborhood, a multifaceted collaborative filtering model, Proceedings of the 14th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD 2008), 426-434
    locator: Section 4 (Asymmetric-SVD, which represents a user by the items the user rated and so serves new users without retraining, and SVD++, which keeps a learned vector per user)
  - paper: doi:10.1109/MC.2009.263
    title: Yehuda Koren, Robert Bell and Chris Volinsky, Matrix factorization techniques for recommender systems, IEEE Computer 42(8), 30-37, 2009
    locator: section Recommender system strategies (the cold start problem of collaborative filtering, which content filtering does not have)
  - book: isbn:9783319296579
    title: Charu C. Aggarwal, Recommender Systems, The Textbook, Springer, 2016
    locator: Chapters 4 and 6 (content-based and hybrid methods as remedies for cold start)
---

The cold-start problem is the failure of [collaborative filtering](/collaborative-filtering/) on users and items that have few or no interactions. A collaborative method predicts from agreement in past behavior, and a new user or a new item has no past behavior to agree on, so the method gives no personal prediction, or a poor one, until data arrives. The remedies bring in other information, such as item content, user attributes or questions to the user, or they collect data on purpose by exploration.

## In plain words

A friend who has never seen you choose a film cannot say which film you will like. A shop that sells a new product cannot say who will buy it from sales that have not happened yet. A recommender that learns only from who liked what is in the same position on the first day of every user and every item.

The usual fixes are to look at what the item is, to ask the new user a few questions, to start with popular items, or to try a few items on purpose and learn from the reaction.

## The idea

The [rating matrix](/rating-matrix/) of a collaborative method has a row for each user and a column for each item. A new user is an empty row, and a new item is an empty column. Three cases are usual:

- **New user.** The row of $u$ is empty or has very few entries. A user-based method finds no co-rated items, so every similarity with $u$ is undefined. A factor model has a vector $p_u$ that no rating has moved from its start value, so its prediction is close to the baseline $\mu + b_i$ and the same for all new users.
- **New item.** The column of $i$ is empty. No user can be similar on it, no item can be similar to it, and its factor $q_i$ has not been trained, so it is almost never ranked high. If it is never shown, it never gets ratings, and the gap persists.
- **New system.** All rows and columns are sparse at the start of a service, and every method is weak.

The cold start is a matter of degree, not only of empty rows. A user with one rating still has no Pearson correlation with anyone, since the variance on one co-rated item is 0, and a similarity computed on two or three items is mostly noise.

The remedies sort into four groups:

- **Content.** [Content-based filtering](/content-based-filtering/) scores a new item from its features as soon as these exist, and a [hybrid recommender](/hybrid-recommender/) uses the content score until the collaborative one has enough data. Schein et al. (2002) study this case of items with no ratings, with a model that joins content and collaborative data.
- **Models that need no training per user.** Koren (2008) describes Asymmetric-SVD, which represents a user only through the items the user rated, so a new user with a few ratings gets a personal prediction without retraining; [SVD++](/svd-plus-plus/) also has a learned vector $p_u$, which a new user does not have until the model is trained again. [Session-based recommendation](/session-based-recommendation/) works from the current session alone.
- **Asking.** On sign up, the system asks the user to rate or choose a few items. The items should be ones that many users know and that split users well.
- **Exploring.** The system shows new items to some users on purpose and learns from the response. This is the [exploration and exploitation trade-off](/exploration-exploitation-tradeoff/) of a [multi-armed bandit](/multi-armed-bandit/), and with user and item features of a [contextual bandit](/contextual-bandit/), with policies such as [UCB1](/ucb1/) and [Thompson sampling](/thompson-sampling/).

## Examples

Add a new user $u_5$ with no ratings and a new item $i_5$ with no ratings to the toy matrix of this group:

| | $i_1$ | $i_2$ | $i_3$ | $i_4$ | $i_5$ |
|---|---|---|---|---|---|
| $u_1$ | 5 | 4 | - | 1 | - |
| $u_2$ | 4 | 5 | 4 | 2 | - |
| $u_3$ | 1 | 2 | 2 | 5 | - |
| $u_4$ | - | 1 | 1 | 4 | - |
| $u_5$ | - | - | - | - | - |

- **For $u_5$**, [user-based filtering](/user-based-collaborative-filtering/) has no co-rated items with anyone and gives no prediction. A non-personal fallback ranks items by their mean rating: $i_1$ has $10/3$, $i_2$ and $i_4$ have 3, and $i_3$ has $7/3$, so every new user gets $i_1$ first. If $u_5$ then rates $i_2$ with 5, the only co-rated item with each other user is $i_2$, and the Pearson correlation on one item is still undefined.
- **For $i_5$**, [item-based filtering](/item-based-collaborative-filtering/) and [Slope One](/slope-one/) have no pair of ratings that includes $i_5$, so they give nothing. With the features of the [content-based filtering](/content-based-filtering/) page, $i_5 = (0, 0, 1)$ is a comedy, and the content profile of $u_1$ gives it a negative cosine, so $u_1$ is not offered it; the [hybrid recommender](/hybrid-recommender/) page works out a switching hybrid on this case.

Large services have this problem without end: a news site has new articles every hour, a shop adds new products every day, and every service gets new users.

## Where it is used

- **Design of recommenders.** The choice between collaborative, content and hybrid methods often depends on how many users and items are new at any time.
- **Evaluation.** Accuracy measured over all test pairs is dominated by users and items with many ratings. A split that holds out whole users or whole items measures the cold-start case on its own.
- **Interactive systems.** News, ads and music services treat new items as arms to explore, with bandit policies and [off-policy evaluation](/off-policy-evaluation/) of the logged data.
- **Sign-up flows.** The first questions to a new user are a short, chosen sample of the items.

## References
