---
tag: 87CAT3
kind: algorithm
slug: svd-plus-plus
name: SVD++
aliases:
- Koren SVD++
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Adds to the biased latent factor model an implicit-feedback term, a scaled sum of factors of the items the user rated or viewed, so that the fact of rating counts as a signal.
solves: [recommendation-problem]
model: word-ram
complexity:
  vars: {m: the number of users, n: the number of items, s: the number of known ratings, r: the number of factors, d: the largest number of implicit items of one user, E: the number of epochs}
  time: {worst: O(E s d r)}
  space: {extra: O((m + n) r)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2008
  people: [Yehuda Koren]
  note: Koren (KDD 2008) introduced SVD++ together with Asymmetric-SVD and an integrated model that adds a neighborhood term, all trained by gradient descent on the Netflix Prize data.
prereqs: [rating-matrix, collaborative-filtering, matrix-factorization-recommendation]
see_also: [implicit-feedback, alternating-least-squares, item-based-collaborative-filtering, stochastic-gradient-descent, factorization-machine, implicit-feedback-als, cold-start-problem, probabilistic-matrix-factorization]
sources:
  - paper: doi:10.1145/1401890.1401944
    title: Yehuda Koren, Factorization meets the neighborhood, a multifaceted collaborative filtering model, Proceedings of the 14th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD 2008), 426-434
    locator: Section 2.5 (implicit feedback as the binary matrix of rated and not rated), Section 4 (Asymmetric-SVD, Equation 13, and SVD++, Equation 15, with Table 1), Section 5 (the integrated model, Equation 16, its gradient steps and the values of the meta parameters)
  - paper: doi:10.1109/MC.2009.263
    title: Yehuda Koren, Robert Bell and Chris Volinsky, Matrix factorization techniques for recommender systems, IEEE Computer 42(8), 30-37, 2009
    locator: section Additional input sources (the normalized sum of item vectors over the items with implicit preference)
  - book: isbn:9783319296579
    title: Charu C. Aggarwal, Recommender Systems, The Textbook, Springer, 2016
    locator: Chapter 3, Section 3.6 (latent factor models)
---

SVD++ is a latent factor model for rating prediction in which the vector of a user is the free vector $p_u$ of [matrix factorization](/matrix-factorization-recommendation/) plus a normalized sum of item vectors $y_j$ over the set $N(u)$ of items with implicit feedback from $u$, such as the items the user rated, rented or viewed. Koren introduced it in 2008 for the Netflix Prize, where $N(u)$ was the set of rated items: which films a user chose to rate says something about the user, apart from the values of the ratings. The model is trained by [stochastic gradient descent](/stochastic-gradient-descent/) on the regularized squared error of the known ratings.

## In plain words

Plain matrix factorization learns a taste profile for each user from the ratings alone. SVD++ also uses the list of items that the user touched, even when it does not know what the user thought of them. Each item gets a second profile that says what having touched this item tells about a person. The user's full profile is the learned taste profile plus the average of these second profiles over the items the user touched.

So a user with few ratings but a long history of views still gets a useful profile, and a user's profile changes as soon as a new view enters the history, even before the model learns anything new.

## The problem

The input is a set $K$ of known ratings of $m$ users for $n$ items, $s = |K|$, and for each user $u$ a set $N(u)$ of items with implicit feedback. In Koren's experiments $N(u)$ is the set of items that $u$ rated, since the Netflix data had no other implicit data (Section 2.5). The model of Equation 15 predicts

$$\hat r_{ui} = \mu + b_u + b_i + q_i^\top \Bigl( p_u + |N(u)|^{-1/2} \sum_{j \in N(u)} y_j \Bigr),$$

with $\mu$ the mean rating, biases $b_u, b_i$, and vectors $p_u, q_i, y_j \in \mathbb{R}^r$. Write $z_u$ for the vector in the parentheses; the sum is 0 when $N(u)$ is empty. With $e_{ui} = r_{ui} - \hat r_{ui}$, training minimizes

$$J = \sum_{(u, i) \in K} \Bigl[ e_{ui}^2 + \lambda_b \bigl( b_u^2 + b_i^2 \bigr) + \lambda_f \Bigl( \lVert p_u \rVert^2 + \lVert q_i \rVert^2 + \sum_{j \in N(u)} \lVert y_j \rVert^2 \Bigr) \Bigr],$$

with the penalties inside the sum over the ratings, as in the paper. Like plain matrix factorization, $J$ is not convex, and training finds a model with a low value, not a certified minimum.

## The algorithm

```pseudo id=main
FIT(K, N, r, λ_b, λ_f, γ, E, decay)
L1  μ ← the mean of the ratings in K; b_u, b_i ← 0; p_u, q_i, y_j ← small random vectors
L2  repeat E times
L3      for each (u, i) in K, in a new random order, do
L4          z ← p_u + |N(u)|^(-1/2) Σ_{j ∈ N(u)} y_j
L5          e ← r_ui - (μ + b_u + b_i + q_i·z)
L6          b_u ← b_u + γ (e - λ_b b_u); b_i ← b_i + γ (e - λ_b b_i)
L7          (q_i, p_u) ← (q_i + γ (e z - λ_f q_i), p_u + γ (e q_i - λ_f p_u))
L8          y_j ← y_j + γ (e |N(u)|^(-1/2) q_i - λ_f y_j) for each j in N(u)   ▷ the old q_i
L9      γ ← decay · γ
L10 return μ, b, p, q, y

PREDICT(u, i)
L11 return μ + b_u + b_i + q_i·(p_u + |N(u)|^(-1/2) Σ_{j ∈ N(u)} y_j)
```

Lines L6 to L8 are the gradient steps that Koren gives for the factor part of the integrated model of Section 5, with one step size in place of his $\gamma_1$ for the biases and $\gamma_2$ for the vectors. For that model he reports $\gamma_1 = \gamma_2 = 0.007$, $\lambda_6 = 0.005$ for the biases, $\lambda_7 = 0.015$ for the vectors, and a decrease of the step sizes by a factor of 0.9 after each iteration. The defaults of the code on this page follow these values.

## Example

Use the toy rating matrix of this group, with $N(u)$ the items each user rated:

| | $i_1$ | $i_2$ | $i_3$ | $i_4$ |
|---|---|---|---|---|
| $u_1$ | 5 | 4 | - | 1 |
| $u_2$ | 4 | 5 | 4 | 2 |
| $u_3$ | 1 | 2 | 2 | 5 |
| $u_4$ | - | 1 | 1 | 4 |

Take one factor and the hand-set parameters $\mu = 3$, $b_u = (0.2, 0.5, -0.5, -1)$, $b_i = 0$, $p = (0.5, 0.5, -0.5, -0.5)$, $q = (1, 1, 1, -1)$ and $y = (0.4, 0.4, 0.4, -0.4)$. These values are not trained; they only show how the user vector works.

| prediction | $N(u)$ | $\sum_{j \in N(u)} y_j$ | $z_u$ | $\hat r_{ui}$ |
|---|---|---|---|---|
| $u_1$, $i_3$ | $i_1, i_2, i_4$ | 0.4 | $0.5 + 0.4/\sqrt{3} \approx 0.7309$ | $3 + 0.2 + 0.7309 \approx 3.931$ |
| $u_4$, $i_1$ | $i_2, i_3, i_4$ | 0.4 | $-0.5 + 0.4/\sqrt{3} \approx -0.2691$ | $3 - 1 - 0.2691 \approx 1.731$ |
| $u_4$, $i_1$, after a view of $i_1$ | $i_1, i_2, i_3, i_4$ | 0.8 | $-0.5 + 0.8/2 = -0.1$ | $3 - 1 - 0.1 = 1.9$ |

In the last row, $u_4$ has viewed $i_1$ without rating it. Nothing was retrained, but $i_1$ entered $N(u_4)$, its vector $y_{i_1} = 0.4$ entered the sum, and the prediction for $u_4$ rose. Plain matrix factorization with the same $p$, $q$ and biases would give $3 - 1 - 0.5 = 1.5$ in both rows for $u_4$, with or without the view.

## Correctness

The proof in `proofs/correctness.md` shows the following. The term $\ell_{ui}$ of one rating in $J$ depends only on $b_u$, $b_i$, $p_u$, $q_i$ and the $y_j$ with $j \in N(u)$. Its gradient is $-2 e_{ui} z_u + 2 \lambda_f q_i$ in $q_i$, $-2 e_{ui} q_i + 2 \lambda_f p_u$ in $p_u$, and $-2 e_{ui} |N(u)|^{-1/2} q_i + 2 \lambda_f y_j$ in each $y_j$, with the bias parts as in matrix factorization. So lines L4 to L8 make the step $\theta \leftarrow \theta - (\gamma / 2) \nabla \ell_{ui}(\theta)$, with all parts at the old values, and the method is stochastic gradient descent on $J$. When every $N(u)$ is empty, the prediction, the objective and the steps are those of biased matrix factorization with $\lambda_b$ for the biases and $\lambda_f$ for the vectors. As for matrix factorization, no convergence result is claimed.

## Complexity

The model is the word RAM with real numbers of fixed size. Let $d = \max_u |N(u)|$.

- **One step.** Line L4 sums $|N(u)|$ vectors of length $r$, and line L8 updates the same vectors, so a step costs $O(|N(u)| r + r)$, at most $O(d r)$.
- **One epoch.** $O(r \sum_{(u, i) \in K} (|N(u)| + 1))$, at most $O(s d r)$. All $E$ epochs cost $O(E s d r)$. With $N(u)$ the rated items, the sum is $\sum_u |I_u| (|I_u| + 1)$, so heavy users dominate the cost.
- **Prediction.** $O(|N(u)| r)$ for the first item of a user, and $O(r)$ for each further item once $z_u$ is stored.
- **Space.** $m + n$ biases and $(m + 2n) r$ numbers for $p$, $q$ and $y$, so $O((m + n) r)$.

A common change to the order of the work processes all ratings of one user together, computes $z_u$ once and adds up the updates of the $y_j$, so that an epoch costs $O(s r + r \sum_u |N(u)|)$. This is a different sequence of steps from lines L3 to L8, not the same computation.

## Properties

- **More signal per user.** The vector $z_u$ uses every item in $N(u)$, including items without a rating, so a user with many views and few ratings gets more than $p_u$ alone.
- **Reduces to the biased model.** With all $N(u)$ empty, SVD++ is biased matrix factorization.
- **Shared item vectors.** Each $y_j$ is learned from all users with $j \in N(u)$, so a new implicit item of a known user changes $z_u$ at once. A new user, however, still has no $p_u$, and the paper notes that SVD++ needs retraining to handle new users, unlike its Asymmetric-SVD.
- **Not unique.** A joint rotation of all $p_u$, $q_i$ and $y_j$ by the same orthogonal matrix keeps every prediction and $J$.
- **Randomized and approximate.** The result depends on the random start and the order of the ratings.

## Variants and improvements

- **Asymmetric-SVD.** Equation 13 of the paper drops $p_u$ and builds the user from two normalized sums, one over the rated items weighted by the rating minus its baseline, and one over $N(u)$. It has fewer parameters, handles a new user as soon as the user gives feedback, and explains a prediction by the user's own past actions. It builds on the NSVD model of Paterek, which also represents a user through the items the user rated.
- **The integrated model.** Equation 16 adds to SVD++ the global neighborhood model of Section 3 of the paper, with learned item to item weights over the $k$ most similar items.
- **Time effects.** Koren's later timeSVD++ lets the biases and the user vector change over time.
- **Other implicit sets.** $N(u)$ can hold purchases, clicks or views. The model then joins explicit ratings with [implicit feedback](/implicit-feedback/).
- **Factorization machines.** A [factorization machine](/factorization-machine/) with the user, the item and the normalized set $N(u)$ as features contains the SVD++ prediction, plus further pairwise terms between the items of $N(u)$.
- **Training by ALS.** With all other parameters fixed, the $p$ block and the $q$ block have ridge regression updates as in [alternating least squares](/alternating-least-squares/). The $y_j$ of one user enter the same sum, so their problem does not split item by item. The paper trains all parameters by gradient steps.

## When to use it

Use SVD++ for explicit ratings when the system also knows which items each user touched, and when accuracy of the rating prediction matters more than the cost of training. Koren (2008, Table 1) reports test RMSE on the Netflix data of 0.8952, 0.8924 and 0.8911 for SVD++ with 50, 100 and 200 factors, against 0.9046, 0.9025 and 0.9009 for the biased factor model and 0.9037, 0.9013 and 0.9000 for Asymmetric-SVD. These are measurements on one data set. When there are no ratings at all, only implicit data, use a model made for implicit data such as [ALS for implicit feedback](/implicit-feedback-als/). When new users must be served at once, Asymmetric-SVD or a neighborhood method avoids retraining.

## Pitfalls

- **Cost of heavy users.** A user with thousands of items in $N(u)$ makes each of the user's steps cost thousands of vector updates. Group the steps by user, or cap $N(u)$.
- **The wrong $q_i$ in line L8.** The steps for $p_u$ and the $y_j$ use the value of $q_i$ from before line L7. Using the new value is a different step, close to the old one for small $\gamma$.
- **Leaking the target.** When $N(u)$ is the set of rated items and the model is evaluated on held out ratings, build $N(u)$ only from information that the system would have at prediction time. If the held out item is in $N(u)$ only because it was rated, the evaluation tells the model which items the user chose, and the measured error can be too low.
- **Penalty on $y$.** The penalty $\lambda_f \sum_{j \in N(u)} \lVert y_j \rVert^2$ appears in the term of every rating of $u$, so popular implicit items are penalized many times. Tune $\lambda_f$ for this form.
- **Empty $N(u)$.** Skip the normalization when $N(u)$ is empty, rather than divide by zero.

## Implementations

## History

Koren presented SVD++ at KDD 2008 in a paper that also introduced a global neighborhood model and Asymmetric-SVD, and that combined the neighborhood model and SVD++ in one integrated model. The work came out of the Netflix Prize, where his team used the binary information of which films each user rated. Koren, Bell and Volinsky (2009) describe the same normalized sum of item vectors as a way to add implicit inputs to matrix factorization.

## References
