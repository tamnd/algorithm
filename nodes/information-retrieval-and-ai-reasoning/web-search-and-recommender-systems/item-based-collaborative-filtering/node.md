---
tag: Z4THKH
kind: algorithm
slug: item-based-collaborative-filtering
name: Item-based collaborative filtering
aliases:
- item-item collaborative filtering
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Precomputes similarities between items from co-ratings and predicts a user's rating from the user's ratings of the most similar items.
solves: [recommendation-problem]
model: word-ram
complexity:
  vars: {m: the number of users, n: the number of items, s: the number of known ratings, k: the model size (neighbors kept per item)}
  time: {worst: O(n s + n^2 log n)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2001
  people: [Badrul Sarwar, George Karypis, Joseph Konstan, John Riedl]
  note: Sarwar, Karypis, Konstan and Riedl (WWW 2001) compared cosine, correlation and adjusted cosine similarity between items, with a precomputed model of the k most similar items. Linden, Smith and York (2003) described the item-to-item method used at Amazon.com.
prereqs: [rating-matrix, collaborative-filtering, user-based-collaborative-filtering]
see_also: [slope-one, cosine-similarity, matrix-factorization-recommendation, sparse-linear-method, cold-start-problem, top-k-selection, jaccard-similarity]
sources:
  - paper: doi:10.1145/371920.372071
    title: Badrul Sarwar, George Karypis, Joseph Konstan and John Riedl, Item-based collaborative filtering recommendation algorithms, Proceedings of the 10th International World Wide Web Conference (WWW 2001), 285-295
    locator: Section 3.1 (cosine, correlation and adjusted cosine similarity, 3.1.1 to 3.1.3), Section 3.2.1 (the weighted sum prediction), Section 3.3 (the precomputed model of the k most similar items and its size), Section 4 (the experiments with mean absolute error)
  - paper: doi:10.1109/MIC.2003.1167344
    title: Greg Linden, Brent Smith and Jeremy York, Amazon.com recommendations, item-to-item collaborative filtering, IEEE Internet Computing 7(1), 76-80, 2003
    locator: the offline table of similar items built from the items that customers buy together, cosine similarity on customer vectors, the worst case cost of the build and the online cost
  - book: isbn:9783319296579
    title: Charu C. Aggarwal, Recommender Systems, The Textbook, Springer, 2016
    locator: Chapter 2 (neighborhood-based collaborative filtering, item-based neighborhood models and the comparison with user-based models)
---

Item-based collaborative filtering predicts the rating of a user $u$ for an item $i$ from the ratings that $u$ gave to the items most similar to $i$. The similarity of two items is computed from the users who rated both, for example by the adjusted cosine of Sarwar et al. (2001), and the $k$ most similar items of each item are stored in advance as the model. Where [user-based collaborative filtering](/user-based-collaborative-filtering/) compares rows of the [rating matrix](/rating-matrix/) at prediction time, this method compares columns once, offline. [Slope One](/slope-one/) uses the same item pairs but stores an average rating difference in place of a similarity.

## In plain words

To guess how much you will like a film, look at the films you already rated, and keep those that resemble it most. Two films resemble each other when the same people liked both and the same people disliked both. Your guess is the average of your own ratings of the close films, with the closer ones counting more.

The resemblance between films changes slowly, because each film has many ratings. So the system computes, once a day or once a week, a short list of close films for each film. A guess then needs only a few lookups in your own ratings, which is fast enough to do while a page loads.

## The problem

The input is a set $K$ of known ratings $r_{ui}$ over $m$ users and $n$ items, and pairs $(u, i) \notin K$ to predict. Let $U_i$ be the set of users who rated $i$, $I_u$ the set of items that $u$ rated, and $\mu_u$ the mean rating of $u$. The adjusted cosine similarity of items $i \ne j$ is

$$s(i, j) = \frac{\sum_{u \in U_i \cap U_j} (r_{ui} - \mu_u)(r_{uj} - \mu_u)}{\sqrt{\sum_{u \in U_i \cap U_j} (r_{ui} - \mu_u)^2} \, \sqrt{\sum_{u \in U_i \cap U_j} (r_{uj} - \mu_u)^2}},$$

with $s(i, j) = 0$ when a sum under a root is 0. It is the [cosine similarity](/cosine-similarity/) of the two columns on their common users after each rating has its user's mean subtracted. The model $M_i$ is the list of the $k$ items $j \ne i$ with the largest positive $s(i, j)$. With $J = M_i \cap I_u$, the prediction is

$$\hat r_{ui} = \frac{\sum_{j \in J} s(i, j)\, r_{uj}}{\sum_{j \in J} s(i, j)},$$

and $\hat r_{ui} = \mu_u$ when $J$ is empty. This page keeps only positive similarities in $M_i$; the reason is in Pitfalls. The choice of the items to show from these predictions is the [recommendation problem](/recommendation-problem/).

## The algorithm

```pseudo id=main
BUILD(K, k)
L1  μ_u ← the mean of the ratings of u, for each user u
L2  c_ui ← r_ui - μ_u for each (u, i) in K       ▷ centered ratings
L3  for each pair of items i < j do
L4      U ← U_i ∩ U_j                            ▷ users who rated both
L5      s(i, j) ← s(j, i) ← Σ_U c_ui c_uj / sqrt(Σ_U c_ui² · Σ_U c_uj²), or 0 if a sum is 0
L6  for each item i do
L7      M_i ← the k items j ≠ i with the largest s(i, j) > 0 (ties: smaller id)

PREDICT(u, i)
L8  if u has no rating then return the mean of all ratings
L9  J ← the items of M_i that u rated
L10 if J is empty then return μ_u
L11 return Σ_{j ∈ J} s(i, j) r_uj / Σ_{j ∈ J} s(i, j)
```

With $k$ unset, line L7 keeps all items with a positive similarity. BUILD runs offline; PREDICT reads only $M_i$ and the ratings of $u$.

## Example

The toy rating matrix of this group, with the user means:

| | $i_1$ | $i_2$ | $i_3$ | $i_4$ | mean |
|---|---|---|---|---|---|
| $u_1$ | 5 | 4 | - | 1 | 10/3 |
| $u_2$ | 4 | 5 | 4 | 2 | 15/4 |
| $u_3$ | 1 | 2 | 2 | 5 | 5/2 |
| $u_4$ | - | 1 | 1 | 4 | 2 |

Predict $r_{u_1 i_3}$. Item $i_3$ is rated by $u_2$, $u_3$ and $u_4$, with centered values $1/4$, $-1/2$ and $-1$.

| $j$ | common users | $\sum c_{ui_3} c_{uj}$ | $\sum c_{ui_3}^2$ | $\sum c_{uj}^2$ | $s(i_3, j)$ |
|---|---|---|---|---|---|
| $i_1$ | $u_2, u_3$ | 13/16 | 5/16 | 37/16 | 0.956 |
| $i_2$ | $u_2, u_3, u_4$ | 25/16 | 21/16 | 45/16 | 0.813 |
| $i_4$ | $u_2, u_3, u_4$ | $-59/16$ | 21/16 | 213/16 | $-0.882$ |

So $M_{i_3} = (i_1, i_2)$, and $u_1$ rated both. The prediction is $(0.956 \cdot 5 + 0.813 \cdot 4) / (0.956 + 0.813) = 4.540$. Item $i_4$, which the users rate in the opposite way to $i_3$, does not enter. For $(u_4, i_1)$, $M_{i_1} = (i_3, i_2)$ with similarities 0.956 and 0.641, and $u_4$ gave 1 to both, so the prediction is 1.

The plain cosine of the raw columns on the common users gives 0.976, 0.996 and 0.716 for $i_1$, $i_2$ and $i_4$: all positive, so it cannot see that $i_4$ is the opposite of $i_3$.

## Correctness

Correctness here means that the algorithm computes the formulas of the problem section. The proof in `proofs/correctness.md` shows that lines L3 to L5 compute $s(i, j)$ for each pair, that $s$ is symmetric with values in $[-1, 1]$ by the Cauchy-Schwarz inequality, that each $M_i$ has at most $k$ items, all with positive similarity, and that PREDICT returns the weighted mean. Because the weights $s(i, j)$ in line L11 are positive, the prediction is a convex combination of ratings of $u$, so it lies between the smallest and the largest rating of $u$ on $J$, and inside the rating scale.

## Complexity

The model is the word RAM, with hash tables for the ratings of each user and each item. Let $n_u = |I_u|$.

- **Build, pair by pair.** For a pair $(i, j)$, line L5 scans $U_i$ and looks up each user in $U_j$, so it costs $O(|U_i|)$. Summed over all pairs this is $O(n \sum_i |U_i|) = O(n s)$, and $s \le m n$ gives $O(m n^2)$ in the worst case. Line L7 sorts $n - 1$ values for each item, $O(n^2 \log n)$ in total, or $O(n^2 \log k)$ with a heap of size $k$.
- **Build, user by user.** Linden, Smith and York loop over the items, the users of each item and the other items of each user. In this order only pairs with a common user are touched, and the work is $O(\sum_u n_u^2)$. Their paper states the worst case as $O(N^2 M)$ for $N$ items and $M$ customers, and notes that in practice it is much lower, because most customers rate or buy few items.
- **Space.** The full similarity table has up to $\binom{n}{2}$ entries, $O(n^2)$. The model keeps $O(n k)$ entries.
- **Prediction.** Line L9 looks up each of the at most $k$ items of $M_i$ in the ratings of $u$, so PREDICT costs $O(k)$ expected time, independent of $m$ and $n$. To rank all items for $u$, loop over the items $j$ that $u$ rated and add $s(i, j)$ and $s(i, j) r_{uj}$ to two accumulators for each $i$ with $j \in M_i$; with the lists $M_i$ stored in reverse this costs $O(n_u k)$, plus [top-k selection](/top-k-selection/) at the end.

## Properties

- **Model-based in its cost, memory-based in its form.** The model is a table of similarities, built offline. A prediction is still a weighted mean of real ratings, so it can be explained as "because you rated these items".
- **Stable similarities.** When an item has many ratings, a few new ratings change its similarities little, so the table can be rebuilt on a schedule and not at each new rating.
- **Uses the target user's own scale.** The prediction is a mean of the user's own ratings, so no mean-centering of the result is needed.
- **No prediction for a new item.** An item with no rating has no similarities, see the [cold-start problem](/cold-start-problem/).

## Variants and improvements

- **Other similarities.** Sarwar et al. compared the plain cosine of the columns (3.1.1), the Pearson correlation of the two items on their common users (3.1.2) and the adjusted cosine (3.1.3); in their experiments on MovieLens data, the adjusted cosine gave the lowest mean absolute error. For 0 and 1 data, such as purchases, the cosine of the binary columns or the [Jaccard similarity](/jaccard-similarity/) are common.
- **Regression in place of the raw rating.** Section 3.2.2 of Sarwar et al. fits a linear model from the ratings of the neighbor item to those of the target item and uses its output in place of $r_{uj}$.
- **Mean-centered prediction.** Predict $\mu_u + \sum_j s(i, j)(r_{uj} - \mu_u) / \sum_j |s(i, j)|$; with this form, negative similarities can be kept.
- **Learned weights.** [SLIM](/sparse-linear-method/) learns the item-item weights by sparse regression in place of a fixed similarity formula.
- **Top-N lists for implicit data.** For clicks or purchases there are no ratings to average. The score of an item is the sum of its similarities to the items in the user's history, and the list is the $N$ items with the largest score, see [implicit feedback](/implicit-feedback/).

## When to use it

Use it when there are many more users than items, when items get many ratings each, and when the system must answer in a few milliseconds with an explanation: this is the setting of Linden, Smith and York. It is a strong baseline for top-N lists from purchases or clicks. When the data are very sparse and ratings must be predicted accurately, factor models such as [matrix factorization](/matrix-factorization-recommendation/) are the usual next step.

## Pitfalls

- **Negative similarities with a plain weighted sum.** Section 3.2.1 of Sarwar et al. divides $\sum_j s(i, j) r_{uj}$ by $\sum_j |s(i, j)|$. With a negative similarity in the sum, the result is no longer a mean of ratings: in the example, keeping $i_4$ gives $(0.956 \cdot 5 + 0.813 \cdot 4 - 0.882 \cdot 1) / 2.651 = 2.697$, and with larger negative weights the value can fall below the scale. Keep only positive similarities, as on this page, or use the mean-centered form.
- **Plain cosine on ratings.** On a scale of 1 to 5 all entries are positive, so the plain cosine is positive for every pair; the example shows 0.716 for two items with opposite ratings. Center the ratings first.
- **Similarities on few common users.** A pair with one or two common users can get a similarity near 1 by chance. Require a minimum number of common users, or shrink the similarity toward 0 by a factor that grows with the overlap.
- **Centering by the item mean.** The adjusted cosine subtracts the user mean. Subtracting the item mean gives the Pearson correlation of the two items, a different measure.
- **A model that is too small.** With a small $k$, many pairs $(u, i)$ have no item of $M_i$ in $I_u$, and the method falls back to $\mu_u$. Sarwar et al. measured the accuracy as a function of the model size.
- **Stale tables.** New items stay without neighbors until the next build.

## Implementations

## History

Sarwar, Karypis, Konstan and Riedl (2001) studied item-based algorithms as a way to scale collaborative filtering beyond the user-based methods of GroupLens: they compared three item similarities and two prediction rules, and introduced the precomputed model of the $k$ most similar items. Linden, Smith and York (2003) described the item-to-item method that Amazon.com used for its recommendations, with an offline table of similar items and an online step whose cost does not depend on the numbers of customers and items.

## References
