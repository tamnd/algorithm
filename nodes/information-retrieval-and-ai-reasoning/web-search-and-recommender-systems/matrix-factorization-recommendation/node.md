---
tag: 99YS69
kind: algorithm
slug: matrix-factorization-recommendation
name: Matrix factorization for recommendation
aliases:
- latent factor model
- Funk SVD
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Fits a user vector and an item vector whose dot product predicts each known rating, by regularized least squares and gradient descent.
solves: [recommendation-problem]
model: word-ram
complexity:
  vars: {m: the number of users, n: the number of items, s: the number of known ratings, r: the number of factors, E: the number of epochs}
  time: {worst: O(E s r)}
  space: {extra: O((m + n) r)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2006
  people: [Simon Funk, Yehuda Koren, Robert Bell, Chris Volinsky]
  note: Simon Funk described the gradient training of a regularized factor model for the Netflix Prize in a blog post of December 2006, and Koren, Bell and Volinsky gave the standard account with biases in IEEE Computer in 2009.
prereqs: [rating-matrix, collaborative-filtering]
see_also: [alternating-least-squares, svd-plus-plus, stochastic-gradient-descent, singular-value-decomposition, ridge-regression, probabilistic-matrix-factorization, matrix-completion, nonnegative-matrix-factorization]
sources:
  - paper: doi:10.1109/MC.2009.263
    title: Yehuda Koren, Robert Bell and Chris Volinsky, Matrix factorization techniques for recommender systems, IEEE Computer 42(8), 30-37, 2009
    locator: sections A basic matrix factorization model (Equations 1 and 2), Learning algorithms (stochastic gradient descent and alternating least squares), Adding biases (Equations 3 to 5) and Netflix Prize competition
  - url: https://sifter.org/~simon/journal/20061211.html
    title: Simon Funk, Netflix Update, Try This at Home, blog post, December 11, 2006
    locator: the training of one feature at a time, the learning rate 0.001, the initial value 0.1, and the regularized update with the constant K
  - paper: doi:10.1145/1401890.1401944
    title: Yehuda Koren, Factorization meets the neighborhood, a multifaceted collaborative filtering model, Proceedings of the 14th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD 2008), 426-434
    locator: Section 2.3 (latent factor models and the remark that Funk popularized gradient descent), Equation 12 (the biased factor model) and Table 1 (RMSE on the Netflix test set)
  - paper: doi:10.1137/110820361
    title: Nicolas Gillis and François Glineur, Low-rank matrix approximation with weights or missing data is NP-hard, SIAM Journal on Matrix Analysis and Applications 32(4), 1149-1165, 2011
    locator: the main result (NP-hardness of low-rank approximation with missing data, already for rank one)
  - book: isbn:9783319296579
    title: Charu C. Aggarwal, Recommender Systems, The Textbook, Springer, 2016
    locator: Chapter 3, Section 3.6 (latent factor models)
---

Matrix factorization for recommendation gives each user $u$ and each item $i$ a vector of $r$ numbers, $p_u$ and $q_i$, and predicts the rating $r_{ui}$ by the dot product $p_u^\top q_i$, usually plus a global mean and a bias for the user and for the item. The vectors are fitted to the known ratings only, by regularized least squares, and the usual training is [stochastic gradient descent](/stochastic-gradient-descent/) that visits one rating at a time. Simon Funk made the method known during the Netflix Prize in 2006, which is why it is also called Funk SVD, although it is not the [singular value decomposition](/singular-value-decomposition/) of any matrix.

## In plain words

Each film gets a short list of hidden scores, for example how much action it has and how serious it is. Each viewer gets a list of the same length that says how much the viewer likes each of these qualities. The guess for a viewer and a film multiplies the two lists entry by entry and adds the results, so a viewer who likes action gets a high guess for an action film.

Nobody chooses the qualities. The method starts from small random lists and goes over the known ratings again and again. For each rating it compares the guess with the true value and moves both lists a little in the direction that makes the error smaller. A penalty keeps the lists short, so that a viewer with few ratings does not get extreme scores.

## The problem

The input is a set $K$ of known ratings $r_{ui}$ of $m$ users for $n$ items, with $s = |K|$, a number of factors $r$, and a penalty $\lambda > 0$. The biased model of Koren, Bell and Volinsky (Equation 4) predicts

$$\hat r_{ui} = \mu + b_u + b_i + p_u^\top q_i,$$

with $\mu$ the mean of the known ratings, scalar biases $b_u$ and $b_i$, and $p_u, q_i \in \mathbb{R}^r$. With $e_{ui} = r_{ui} - \hat r_{ui}$, the fit minimizes

$$J = \sum_{(u, i) \in K} \Bigl[ e_{ui}^2 + \lambda \bigl( b_u^2 + b_i^2 + \lVert p_u \rVert^2 + \lVert q_i \rVert^2 \bigr) \Bigr].$$

The sum runs over the known entries only. A missing entry is not a zero rating, and filling it in would change the problem. The penalty sits inside the sum, as in Equation 5 of the 2009 paper, so a user with $n_u$ ratings pays $\lambda n_u \lVert p_u \rVert^2$, which is the reading that gives the SGD rule below. The unbiased model drops $\mu$, $b_u$ and $b_i$ and predicts $p_u^\top q_i$ (Equations 1 and 2).

$J$ is not convex in all parameters together. Without the penalty, finding the best rank $r$ fit to a partly known matrix is NP-hard already for $r = 1$ (Gillis and Glineur, 2011). The algorithm below is therefore a local search: it gives a model with a low value of $J$, not a certified minimum.

## The algorithm

```pseudo id=main
FIT(K, r, λ, γ, E)                       ▷ γ: step size, E: number of epochs
L1  μ ← the mean of the ratings in K
L2  b_u ← 0, b_i ← 0 for all u, i; p_u, q_i ← small random vectors in R^r
L3  repeat E times
L4      for each (u, i) in K, in a new random order, do
L5          e ← r_ui - (μ + b_u + b_i + p_u·q_i)
L6          b_u ← b_u + γ (e - λ b_u); b_i ← b_i + γ (e - λ b_i)
L7          (p_u, q_i) ← (p_u + γ (e q_i - λ p_u), q_i + γ (e p_u - λ q_i))
L8  return μ, b, p, q

PREDICT(u, i)
L9  return μ + b_u + b_i + p_u·q_i
```

Line L7 updates both vectors at once from the old values. This is the rule of Koren, Bell and Volinsky. The code of Funk's post updates the user value first and then uses the new user value for the item, which is a slightly different step that also works. The unbiased model skips line L6 and the bias terms.

## Example

Use the toy rating matrix of this group, with $\mu = 41/14 \approx 2.9286$ over its 14 ratings:

| | $i_1$ | $i_2$ | $i_3$ | $i_4$ |
|---|---|---|---|---|
| $u_1$ | 5 | 4 | - | 1 |
| $u_2$ | 4 | 5 | 4 | 2 |
| $u_3$ | 1 | 2 | 2 | 5 |
| $u_4$ | - | 1 | 1 | 4 |

Take one factor ($r = 1$), $b_{u_1} = b_{i_1} = 0$, $p_{u_1} = q_{i_1} = 0.5$, and $\gamma = \lambda = 0.1$. One step on the rating $r_{u_1 i_1} = 5$:

| quantity | before | after |
|---|---|---|
| prediction | $\mu + 0.25 \approx 3.1786$ | $\approx 3.6363$ |
| error $e$ | $\approx 1.8214$ | $\approx 1.3637$ |
| $b_{u_1}$, $b_{i_1}$ | 0 | $0.1 \cdot 1.8214 \approx 0.1821$ |
| $p_{u_1}$, $q_{i_1}$ | 0.5 | $0.5 + 0.1 (1.8214 \cdot 0.5 - 0.05) \approx 0.5861$ |
| term $e^2 + \lambda (b_u^2 + b_i^2 + p^2 + q^2)$ | $\approx 3.3676$ | $\approx 1.9349$ |

Both biases and both factors rise, because the prediction was too low. The step changes only the four parameters of $u_1$ and $i_1$; the other 12 parameters of the model wait for their own ratings.

The factors are not unique. With $r = 1$, replacing every $p_u$ by $-p_u$ and every $q_i$ by $-q_i$ keeps all predictions and the penalty, so two different models have the same $J$. With $r \ge 2$, any rotation of the factor space does the same. Only the predictions, not the single factors, carry meaning.

## Correctness

The proof in `proofs/correctness.md` shows the following. The term $\ell_{ui}$ of one rating in $J$ has the gradient $-2 e_{ui} + 2 \lambda b_u$ in $b_u$, $-2 e_{ui} q_i + 2 \lambda p_u$ in $p_u$, and the symmetric forms in $b_i$ and $q_i$, and no other parameter enters it. So lines L5 to L7 make the step $\theta \leftarrow \theta - (\gamma / 2) \nabla \ell_{ui}(\theta)$, and for a rating drawn uniformly from $K$ the expected step is $-(\gamma / 2s) \nabla J$: the method is stochastic gradient descent on $J$. The proof also shows that the penalty inside the sum equals $\lambda \sum_u n_u (b_u^2 + \lVert p_u \rVert^2) + \lambda \sum_i n_i (b_i^2 + \lVert q_i \rVert^2)$, that $J$ is invariant under orthogonal changes of the factor space, and that all factors equal to zero give a stationary point in the factors, which is why line L2 starts from random vectors. It gives no convergence result for the fixed step size $\gamma$.

## Complexity

The model is the word RAM with real numbers of fixed size.

- **One step.** Lines L5 to L7 cost $O(r)$.
- **One epoch.** Line L4 visits all $s$ ratings, and the random order costs $O(s)$, so an epoch costs $O(s r)$. All $E$ epochs cost $O(E s r)$.
- **Prediction.** $O(r)$ for one pair, and $O(n r)$ to score all items for one user.
- **Space.** The model has $m + n$ biases and $(m + n) r$ factors, $O((m + n) r)$ beside the input.

The number of epochs that gives a good model is not fixed by the method. It depends on the data, $\gamma$ and $\lambda$, and is found on held out ratings.

## Properties

- **Approximate and randomized.** The result depends on the random start and the random order. Runs with different seeds give different factors and, in general, slightly different predictions.
- **Only known ratings.** The cost per epoch grows with $s$, not with $m n$, so it works on sparse matrices of any shape.
- **Low rank.** The matrix of the dot products $p_u^\top q_i$ has rank at most $r$. This is the assumption of the method: a few hidden factors explain most of the ratings.
- **Not clipped.** $\hat r_{ui}$ can leave the rating scale.
- **Non-unique factors.** Orthogonal changes of the factor space keep $J$, as in the example.

## Variants and improvements

- **[Alternating least squares](/alternating-least-squares/).** Fixes one side of the factors and solves a ridge regression for each vector of the other side, which parallelizes well and suits [implicit feedback](/implicit-feedback-als/).
- **[SVD++](/svd-plus-plus/).** Adds to $p_u$ a sum of item vectors over the items the user rated, so that the fact of rating counts as a signal.
- **[Probabilistic matrix factorization](/probabilistic-matrix-factorization/).** Reads the squared error with the penalty counted once per parameter, not inside the sum as in $J$, as the negative log posterior of a Gaussian model, with $\lambda$ as a ratio of variances.
- **Nonnegative factors.** [Nonnegative matrix factorization](/nonnegative-matrix-factorization/) keeps all entries at or above zero, which can make the factors easier to read.
- **One factor at a time.** Funk's post trains one feature for many epochs, adds it to the finished features, and then trains the next one on what the finished features do not explain.
- **[Factorization machines](/factorization-machine/)** generalize the dot product to any set of features of the user, the item and the context.
- **Ranking losses.** For clicks and views, a pairwise loss such as [Bayesian personalized ranking](/bayesian-personalized-ranking/) replaces the squared error.

## When to use it

Use it for explicit ratings on a large sparse matrix, when the goal is to predict ratings or to rank items for each user, and when the model can be retrained from time to time. Koren (2008, Table 1) reports test RMSE on the Netflix data of 0.9046, 0.9025 and 0.9009 for the biased model with 50, 100 and 200 factors, against 0.9514 for the Netflix system Cinematch. These values are measurements on one data set. The method cannot give factors to a user or an item with no rating, see the [cold-start problem](/cold-start-problem/). When there is no rating at all, only clicks or views, use a method made for implicit data.

## Pitfalls

- **Zero start.** If all $p_u$ and $q_i$ are zero, every step leaves them at zero, and the model stays a bias model. Start from small random values.
- **Missing entries as zeros.** A truncated SVD of the matrix with zeros in the blanks fits the blanks too and predicts low ratings for all unseen items. Sum over $K$ only.
- **Step size.** A large $\gamma$ makes the error grow from epoch to epoch. A small one needs many epochs. Watch $J$ or the error on held out ratings.
- **The penalty convention.** The per rating penalty and a penalty counted once per parameter give different models for the same $\lambda$. Tune $\lambda$ again when you change the convention.
- **Tuning on the test set.** Choose $r$, $\lambda$, $\gamma$ and $E$ by [cross-validation](/cross-validation/) or on a held out part of the training ratings, or the reported error is too low. See [overfitting](/overfitting/).
- **Reading single factors.** A factor of one run need not match a factor of another run, because of the rotation freedom.

## Implementations

## History

Factor models for ratings came before the Netflix Prize; earlier systems often filled in the missing entries and then took an SVD, which Koren, Bell and Volinsky describe as expensive and as a source of distortion. In December 2006, two months after the prize began, Simon Funk published on his blog a short program that fitted one feature at a time by gradient steps on the known ratings only, with a penalty. Koren (2008) states that Funk popularized gradient descent for this model. Koren, Bell and Volinsky, members of the team that won the Netflix Prize in 2009, summarized the method with biases, implicit feedback, temporal effects and confidence weights in IEEE Computer in 2009.

## References
