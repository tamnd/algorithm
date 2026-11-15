---
tag: SEEFZS
kind: algorithm
slug: user-based-collaborative-filtering
name: User-based collaborative filtering
aliases:
- user-user collaborative filtering
- GroupLens algorithm
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Predicts a rating as the user's mean plus a similarity-weighted average of how far other users rated the item above or below their own means.
solves: [recommendation-problem]
model: word-ram
complexity:
  vars: {m: the number of users, n: the number of items, k: the number of neighbors}
  time: {worst: O(m n)}
  space: {extra: O(m)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1994
  people: [Paul Resnick, Neophytos Iacovou, Mitesh Suchak, Peter Bergstrom, John Riedl]
  note: The GroupLens system for Usenet news (CSCW 1994) predicted a rating from the ratings of other readers, weighted by their Pearson correlation with the reader.
prereqs: [rating-matrix, collaborative-filtering]
see_also: [item-based-collaborative-filtering, slope-one, k-nearest-neighbors, cosine-similarity, matrix-factorization-recommendation, cold-start-problem, top-k-selection]
sources:
  - paper: doi:10.1145/192844.192905
    title: Paul Resnick, Neophytos Iacovou, Mitesh Suchak, Peter Bergstrom and John Riedl, GroupLens, an open architecture for collaborative filtering of netnews, Proceedings of the ACM Conference on Computer Supported Cooperative Work (CSCW 1994), 175-186
    locator: the prediction formula, the user's mean plus the correlation-weighted deviations of the other users, with Pearson correlation over the co-rated articles
  - paper: doi:10.1145/312624.312682
    title: Jonathan L. Herlocker, Joseph A. Konstan, Al Borchers and John Riedl, An algorithmic framework for performing collaborative filtering, Proceedings of SIGIR 1999, 230-237
    locator: the three steps (weight all users, select a neighborhood, combine the deviations), the choice of neighborhood size, and the devaluation of correlations based on few co-rated items
  - book: isbn:9783319296579
    title: Charu C. Aggarwal, Recommender Systems, The Textbook, Springer, 2016
    locator: Chapter 2 (neighborhood-based collaborative filtering, user-based models, similarity functions and the mean-centered prediction)
  - paper: doi:10.1145/963770.963772
    title: Jonathan L. Herlocker, Joseph A. Konstan, Loren G. Terveen and John T. Riedl, Evaluating collaborative filtering recommender systems, ACM Transactions on Information Systems 22(1), 5-53, 2004
    locator: the accuracy measures for predicted ratings (mean absolute error, root mean squared error) and for ranked lists
  - paper: doi:10.1145/138859.138867
    title: David Goldberg, David Nichols, Brian M. Oki and Douglas Terry, Using collaborative filtering to weave an information tapestry, Communications of the ACM 35(12), 61-70, 1992
    locator: the Tapestry system, in which users annotate documents and filter on the annotations of other users
  - paper: doi:10.1109/MC.2009.263
    title: Yehuda Koren, Robert Bell and Chris Volinsky, Matrix factorization techniques for recommender systems, IEEE Computer 42(8), 30-37, 2009
    locator: the opening comparison of matrix factorization with nearest-neighbor methods in the light of the Netflix Prize
---

User-based collaborative filtering predicts the rating of a user $u$ for an item $i$ from the ratings that other users gave to $i$. Each other user $v$ gets a weight, the Pearson correlation of $u$ and $v$ on the items that both rated, and the prediction is the mean of $u$ plus the weighted mean of how far each $v$ rated $i$ above or below the mean of $v$. It is the method of the GroupLens system of Resnick et al. (1994), and it is the user-to-user form of the general [collaborative filtering](/collaborative-filtering/) idea. The [item-based](/item-based-collaborative-filtering/) form compares columns of the [rating matrix](/rating-matrix/) in place of rows, and [Slope One](/slope-one/) and [matrix factorization](/matrix-factorization-recommendation/) replace the weights by fitted offsets or factors.

## In plain words

To guess how much you will like a film, look at the people who already saw it. For each of them, check how much your past opinions agree with theirs, on the films that both of you rated. A person who agrees with you counts with a plus sign, a person who always disagrees counts with a minus sign, and a stranger counts for nothing.

People use the scale in different ways: one person gives 4 to a film they find average, another gives 2. So the method looks at how far each person rated the film above or below their own usual rating, takes a weighted average of these shifts, and adds the result to your own usual rating.

## The problem

The input is a set $K$ of known ratings $r_{vi}$ over $m$ users and $n$ items, and a pair $(u, i)$ with $(u, i) \notin K$. Let $I_v$ be the set of items that $v$ rated, $U_i$ the set of users who rated $i$, and $\mu_v = \frac{1}{|I_v|} \sum_{t \in I_v} r_{vt}$ the mean of $v$. The output is a predicted rating $\hat r_{ui}$. The task of choosing the items to show is the [recommendation problem](/recommendation-problem/); a predictor of single ratings is one way to solve it, by ranking the items that $u$ did not rate by $\hat r_{ui}$.

For two users with $I_{uv} = I_u \cap I_v$, the Pearson weight is

$$w(u, v) = \frac{\sum_{t \in I_{uv}} (r_{ut} - \mu_u)(r_{vt} - \mu_v)}{\sqrt{\sum_{t \in I_{uv}} (r_{ut} - \mu_u)^2 \, \sum_{t \in I_{uv}} (r_{vt} - \mu_v)^2}},$$

with $w(u, v) = 0$ when $I_{uv}$ is empty or one of the two sums under the root is 0. For a set $N \subseteq U_i \setminus \{u\}$ of neighbors, the prediction is

$$\hat r_{ui} = \mu_u + \frac{\sum_{v \in N} w(u, v)\,(r_{vi} - \mu_v)}{\sum_{v \in N} |w(u, v)|},$$

and $\hat r_{ui} = \mu_u$ when the denominator is 0. The means here are over all ratings of each user. Some texts take $\mu_u$ and $\mu_v$ over $I_{uv}$ only in the weight; that is a different number, see Pitfalls.

## The algorithm

```pseudo id=main
PREDICT(u, i)
L1  if u has no rating then return the mean of all ratings
L2  C ← U_i \ {u}                         ▷ the users who rated i
L3  for each v in C do w_v ← WEIGHT(u, v)
L4  if a neighborhood size k is given then
L5      keep in C the k users with the largest w_v (ties: smaller id first)
L6  D ← Σ_{v ∈ C} |w_v|
L7  if D = 0 then return μ_u
L8  return μ_u + Σ_{v ∈ C} w_v (r_vi - μ_v) / D

WEIGHT(u, v)
L9  I ← I_u ∩ I_v                        ▷ the co-rated items
L10 x_t ← r_ut - μ_u and y_t ← r_vt - μ_v for each t in I
L11 if Σ x_t² = 0 or Σ y_t² = 0 then return 0
L12 return Σ x_t y_t / sqrt(Σ x_t² · Σ y_t²)
```

The means $\mu_v$ are computed once from the rating lists. With $k$ unset, line L5 does nothing and all users who rated $i$ take part, as in GroupLens. Line L5 keeps the most similar users, so users with a negative weight drop out first.

## Example

The toy rating matrix of this group has four users and four items; a dash is a missing rating.

| | $i_1$ | $i_2$ | $i_3$ | $i_4$ | mean |
|---|---|---|---|---|---|
| $u_1$ | 5 | 4 | - | 1 | 10/3 |
| $u_2$ | 4 | 5 | 4 | 2 | 15/4 |
| $u_3$ | 1 | 2 | 2 | 5 | 5/2 |
| $u_4$ | - | 1 | 1 | 4 | 2 |

Predict $r_{u_1 i_3}$. The users who rated $i_3$ are $u_2$, $u_3$ and $u_4$.

| $v$ | co-rated items | $\sum x_t y_t$ | $\sum x_t^2$ | $\sum y_t^2$ | $w(u_1, v)$ | $r_{v i_3} - \mu_v$ |
|---|---|---|---|---|---|---|
| $u_2$ | $i_1, i_2, i_4$ | 16/3 | 26/3 | 75/16 | 0.837 | 0.25 |
| $u_3$ | $i_1, i_2, i_4$ | $-26/3$ | 26/3 | 35/4 | $-0.995$ | $-0.5$ |
| $u_4$ | $i_2, i_4$ | $-16/3$ | 53/9 | 5 | $-0.983$ | $-1$ |

The numerator is $0.837 \cdot 0.25 + (-0.995)(-0.5) + (-0.983)(-1) = 1.690$ and the denominator is $0.837 + 0.995 + 0.983 = 2.815$, so $\hat r_{u_1 i_3} = 10/3 + 0.600 = 3.934$. The two users with tastes opposite to $u_1$ rated $i_3$ below their means, and their negative weights turn this into evidence for a high rating. With $k = 1$ only $u_2$ is left, and the prediction is $10/3 + 0.25 = 3.583$.

The same formula for $r_{u_4 i_1}$ uses $w(u_4, u_1) = -0.983$, $w(u_4, u_2) = -0.943$ and $w(u_4, u_3) = 0.943$, with deviations $5/3$, $1/4$ and $-3/2$. The result is $2 - 3.288 / 2.868 = 0.854$, which is below the scale 1 to 5.

## Correctness

The method is a definition, not an optimization, so correctness means that PREDICT returns the formula of the problem section, and that the formula has the stated properties. The proof in `proofs/correctness.md` shows that $-1 \le w(u, v) \le 1$ and $w(u, v) = w(v, u)$, by the Cauchy-Schwarz inequality on the centered vectors; that $w$ does not change when all ratings of one user are multiplied by a positive number or shifted by a constant; and that $|\hat r_{ui} - \mu_u| \le \max_{v \in C} |r_{vi} - \mu_v|$, because the prediction is $\mu_u$ plus a weighted mean of the values $\pm (r_{vi} - \mu_v)$ with the weights $|w_v| / D$. The last bound is all that holds: the prediction can leave the rating scale, as in the second example.

## Complexity

The model is the word RAM with the ratings of each user in a hash table, so a lookup $r_{vt}$ costs $O(1)$ expected time. Let $n_u = |I_u|$ and $s = |K|$.

- **One weight.** WEIGHT$(u, v)$ scans the items of $u$ and looks each one up in the table of $v$: $O(n_u)$ time, or $O(\min(n_u, n_v))$ when it scans the shorter list.
- **One prediction.** Line L3 computes $|U_i| \le m$ weights, so PREDICT costs $O(\sum_{v \in U_i} \min(n_u, n_v)) \subseteq O(m n)$. Line L5 is [top-k selection](/top-k-selection/), $O(|U_i| \log k)$ with a heap. The extra space is $O(m)$ for the weights.
- **All weights in advance.** A table of all $\binom{m}{2}$ weights costs $O(m^2)$ space and $O(m s)$ time, since each pair $(u, v)$ costs at most $O(n_u)$ and $\sum_v \sum_u n_u = m s$. For millions of users this table does not fit, which is the main reason for the item-based form.
- **Updates.** A new rating changes one user's mean and that user's weights, and nothing has to be retrained: the next prediction uses it at once.

## Properties

- **Memory-based.** The ratings are the model. There is no training step, and a new rating is used at the next prediction.
- **Invariant to each user's use of the scale.** Mean-centering removes a user's offset, and the Pearson weight removes a positive scale factor, from the weight. The prediction is shifted to the target user's mean.
- **Explainable.** Each prediction comes with the list of neighbors and their ratings, which a system can show to the user.
- **Sensitive to sparse overlap.** A weight from two co-rated items can be as large as one from two hundred. On one co-rated item $t$ the weight is the sign of $(r_{ut} - \mu_u)(r_{vt} - \mu_v)$, so it is $-1$, $0$ or $1$.

## Variants and improvements

- **Other weights.** [Cosine similarity](/cosine-similarity/) of the raw rating rows, the Spearman rank correlation, or a mean squared difference. Plain cosine on ratings 1 to 5 is always positive, so it cannot express disagreement.
- **Significance weighting.** Herlocker et al. (1999) multiplied a correlation computed on few co-rated items by a factor that grows with the size of the overlap, so that weights from small overlaps count less.
- **Neighborhood selection.** Keep the $k$ most similar users, or the users with $w$ above a threshold. Herlocker et al. studied the effect of the neighborhood size on the accuracy.
- **Case amplification.** Raise each weight to a power above 1, keeping its sign, so that close neighbors dominate.
- **Z-scores.** Divide each deviation $r_{vi} - \mu_v$ by the standard deviation of $v$ and multiply the result by the standard deviation of $u$.
- **Item-based form.** Swap the roles of users and items, see [item-based collaborative filtering](/item-based-collaborative-filtering/).

## When to use it

Use it when the number of users is small or moderate, when ratings change often, and when the system must explain each prediction by real neighbors. For a large catalog with many more users than items, the [item-based](/item-based-collaborative-filtering/) form gives tables that are smaller and change less. When accuracy matters most, factor models such as [matrix factorization](/matrix-factorization-recommendation/) are the usual choice: Koren, Bell and Volinsky (2009) report from the Netflix Prize that they were more accurate than the classic neighborhood methods. The method cannot predict for a user with no ratings, see the [cold-start problem](/cold-start-problem/).

## Pitfalls

- **Means over the co-rated items.** If the weight centers each user on the mean of the co-rated items only, the weight changes, and it no longer matches the mean used in line L8. Both choices appear in the literature; state which one you use. In the toy matrix, $u_2$ has the mean 11/3 on the items $i_1, i_2, i_4$, and the weight of $u_1$ and $u_2$ becomes $16/\sqrt{364} \approx 0.839$ in place of 0.837.
- **Division by the plain sum of weights.** Dividing by $\sum w_v$ in place of $\sum |w_v|$ breaks when positive and negative weights cancel, and the prediction can jump far out of range.
- **Out of range predictions.** The second example gives 0.854 on the scale 1 to 5. Clip the prediction to the scale when ratings are shown to users; for ranking only, clipping is not needed.
- **Neighbors who did not rate the item.** The neighborhood for $(u, i)$ is chosen among the users who rated $i$. Choosing the $k$ most similar users first and then dropping those who did not rate $i$ often leaves too few or no neighbors.
- **Zero weight users in the denominator.** A user with $w = 0$ adds nothing to either sum, so it is harmless; a missing guard for $D = 0$ divides by zero.
- **Leakage in evaluation.** The hidden test ratings must not take part in the means and the weights.

## Implementations

## History

Goldberg, Nichols, Oki and Terry (1992) built Tapestry, a mail filter in which users annotated messages for each other. Resnick, Iacovou, Suchak, Bergstrom and Riedl (1994) automated the idea in GroupLens for Usenet news, with the Pearson-weighted prediction of this page. Herlocker, Konstan, Borchers and Riedl (1999) studied the choices of the method in a common framework: the weight, significance weighting, the neighborhood size and the normalization of the ratings. Herlocker, Konstan, Terveen and Riedl (2004) reviewed the ways to measure the accuracy of such predictors.

## References
