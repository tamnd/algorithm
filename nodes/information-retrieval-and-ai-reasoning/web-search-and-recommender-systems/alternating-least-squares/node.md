---
tag: S7Y3XE
kind: algorithm
slug: alternating-least-squares
name: Alternating least squares for matrix factorization
aliases:
- ALS
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Fixes the item factors and solves a ridge regression for each user, then the reverse, so the regularized error never increases from one half step to the next.
solves: [recommendation-problem]
model: word-ram
complexity:
  vars: {m: the number of users, n: the number of items, s: the number of known ratings, r: the number of factors, T: the number of sweeps}
  time: {worst: O(T (s r^2 + (m + n) r^3))}
  space: {extra: O((m + n) r + r^2)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2008
  people: [Yunhong Zhou, Dennis Wilkinson, Robert Schreiber, Rong Pan]
  note: Zhou, Wilkinson, Schreiber and Pan (AAIM 2008) gave ALS with weighted lambda regularization as a parallel method for the Netflix Prize, and Koren, Bell and Volinsky (2009) described ALS as one of the two standard ways to fit the factor model.
prereqs: [rating-matrix, collaborative-filtering, matrix-factorization-recommendation]
see_also: [ridge-regression, coordinate-descent, cholesky-decomposition, normal-equations, implicit-feedback-als, svd-plus-plus, conjugate-gradient-method, matrix-completion]
sources:
  - paper: doi:10.1007/978-3-540-68880-8_32
    title: Yunhong Zhou, Dennis Wilkinson, Robert Schreiber and Rong Pan, Large-scale parallel collaborative filtering for the Netflix Prize, Algorithmic Aspects in Information and Management (AAIM 2008), Lecture Notes in Computer Science 5034, 337-348
    locator: Equation 5 (the objective with weighted lambda regularization), the solution of the user and the movie least squares problems, the initialization of the movie matrix, the stopping rule on the probe RMSE, and the results with up to 1000 hidden features
  - paper: doi:10.1109/MC.2009.263
    title: Yehuda Koren, Robert Bell and Chris Volinsky, Matrix factorization techniques for recommender systems, IEEE Computer 42(8), 30-37, 2009
    locator: section Learning algorithms (alternating least squares, and when it is preferable to stochastic gradient descent)
  - paper: doi:10.1137/110820361
    title: Nicolas Gillis and François Glineur, Low-rank matrix approximation with weights or missing data is NP-hard, SIAM Journal on Matrix Analysis and Applications 32(4), 1149-1165, 2011
    locator: the main result (NP-hardness of low-rank approximation with missing data, already for rank one)
  - book: isbn:9783319296579
    title: Charu C. Aggarwal, Recommender Systems, The Textbook, Springer, 2016
    locator: Chapter 3, Section 3.6 (latent factor models)
---

Alternating least squares (ALS) fits the factor model $\hat r_{ui} = p_u^\top q_i$ of [matrix factorization](/matrix-factorization-recommendation/) by turns. With the item vectors $q_i$ fixed, the regularized squared error splits into one [ridge regression](/ridge-regression/) for each user, which has a closed form; then the user vectors are fixed and each item gets its ridge regression. Each half step solves its subproblem exactly, so the objective never increases, and the solves of one half step are independent of each other, which makes the method easy to run in parallel.

## In plain words

Fitting user scores and item scores at the same time is hard, because each one depends on the other. If the item scores were known, the best scores for one user would be a small, standard fitting problem with an exact answer, and each user could be solved alone. ALS pretends that the item scores are known, solves for all users, then pretends that the new user scores are known and solves for all items, and goes back and forth.

Each turn can only make the fit better or keep it the same. The method can still stop at a fit that is not the best one, so the starting point matters.

## The problem

The input is a set $K$ of known ratings of $m$ users for $n$ items, $s = |K|$, a number of factors $r$, and $\lambda > 0$. Let $I_u$ be the items that user $u$ rated and $U_i$ the users who rated item $i$. ALS minimizes

$$J(P, Q) = \sum_{(u, i) \in K} \bigl(r_{ui} - p_u^\top q_i\bigr)^2 + \lambda \Bigl( \sum_u c_u \lVert p_u \rVert^2 + \sum_i c_i \lVert q_i \rVert^2 \Bigr)$$

over the user vectors $p_u \in \mathbb{R}^r$ and the item vectors $q_i \in \mathbb{R}^r$. With $c_u = c_i = 1$ this is the plain ridge penalty. With $c_u = |I_u|$ and $c_i = |U_i|$ it is the weighted lambda regularization of Zhou et al. (ALS-WR, their Equation 5), which is the same as putting the penalty inside the sum over the ratings, as on the [matrix factorization](/matrix-factorization-recommendation/) page.

With $Q$ fixed, $J$ is a sum over the users of the separate problems $\min_{p_u} \sum_{i \in I_u} (r_{ui} - p_u^\top q_i)^2 + \lambda c_u \lVert p_u \rVert^2$. Each one is a ridge regression with the vectors $q_i$ as rows of the design matrix, and its unique solution satisfies the [normal equations](/normal-equations/)

$$\Bigl( \sum_{i \in I_u} q_i q_i^\top + \lambda c_u I \Bigr) p_u = \sum_{i \in I_u} r_{ui}\, q_i.$$

The same holds for each item with $P$ fixed. The problem of the whole $J$ is not convex, and without the penalty the best rank $r$ fit to a partly known matrix is NP-hard already for $r = 1$ (Gillis and Glineur, 2011). ALS does not try to find the global minimum; its limit points are points where neither block can be improved alone.

## The algorithm

```pseudo id=main
ALS(K, r, λ, T)
L1  q_i ← small random vectors in R^r for all items; p_u ← 0 for all users
L2  repeat T times (or until J changes by less than a tolerance)
L3      P ← SOLVE(the users, Q)            ▷ one ridge regression per user
L4      Q ← SOLVE(the items, P)            ▷ one ridge regression per item
L5  return P, Q

SOLVE(rows, Y)                             ▷ the vectors y_j of the other side are fixed
L6  for each row x (a user or an item) do
L7      if x has no rating then f_x ← 0 and go to the next row
L8      A ← Σ_j y_j y_jᵀ + λ c_x I; b ← Σ_j r_xj y_j      ▷ sums over the ratings of x
L9      f_x ← the solution of A f = b, by Cholesky decomposition
L10 return the vectors f_x
```

The matrix $A$ of line L8 is symmetric positive definite because $\lambda c_x > 0$, so the [Cholesky decomposition](/cholesky-decomposition/) of line L9 exists. The rows of one call of SOLVE do not depend on each other and can run on different processors.

## Example

Use the toy rating matrix of this group, with one factor ($r = 1$), $\lambda = 1$, the plain penalty, and the start $q_i = 1$ for all items:

| | $i_1$ | $i_2$ | $i_3$ | $i_4$ |
|---|---|---|---|---|
| $u_1$ | 5 | 4 | - | 1 |
| $u_2$ | 4 | 5 | 4 | 2 |
| $u_3$ | 1 | 2 | 2 | 5 |
| $u_4$ | - | 1 | 1 | 4 |

With every $q_i = 1$, line L8 gives $A = |I_u| + 1$ and $b = \sum_{i \in I_u} r_{ui}$ for each user:

| user | $A$ | $b$ | $p_u$ |
|---|---|---|---|
| $u_1$ | 4 | 10 | 5/2 |
| $u_2$ | 5 | 15 | 3 |
| $u_3$ | 5 | 10 | 2 |
| $u_4$ | 4 | 6 | 3/2 |

Then each item gets $q_i = \sum_{u \in U_i} r_{ui} p_u / (\sum_{u \in U_i} p_u^2 + 1)$. For $i_1$, rated by $u_1$, $u_2$ and $u_3$, this is $(5 \cdot 5/2 + 4 \cdot 3 + 1 \cdot 2) / (25/4 + 9 + 4 + 1) = 26.5 / 20.25 = 106/81$. The four values are $q = (106/81, 61/45, 14/13, 49/45)$.

The objective goes from $J = 155 + 4 = 159$ at the start, where $P = 0$, to $60$ after the user step and to about $54.9526$ after the item step. With one factor and a start of all ones, the model can only say how much each user likes items in general. The toy matrix has two groups of users with opposite tastes, and $r = 1$ from this start does not separate them.

With the ALS-WR penalty, $c_u = |I_u|$, the user step gives $p_u = b / (2 |I_u|)$, so $p = (5/3, 15/8, 5/4, 1)$: every user gets half the mean of their ratings, whatever their number. Against the plain step, $p_u = b / (|I_u| + 1)$, the ratio is $(|I_u| + 1) / (2 |I_u|)$, which is $2/3$ for three ratings and $5/8$ for four, so the users with more ratings are shrunk more in relative terms.

If the start is $q_i = 0$ for all items, every $b$ is 0, so every $p_u = 0$, and then every $q_i = 0$. The run stays at $P = Q = 0$ with $J = 155$, a stationary point that is not a minimum.

## Correctness

The proof in `proofs/correctness.md` shows four facts. First, with $Q$ fixed, $J$ is the sum of the user problems plus a constant, and the matrix of each normal equation is positive definite, so line L3 returns the unique minimizer of $J$ over $P$; the same holds for line L4. Second, therefore $J(P_{k+1}, Q_k) \le J(P_k, Q_k)$ and $J(P_{k+1}, Q_{k+1}) \le J(P_{k+1}, Q_k)$, and the values of $J$ converge, since they decrease and are at least 0. Third, the iterates stay in a bounded set, and every limit point of the sequence of sweeps is a stationary point of $J$. Fourth, a stationary point need not be a minimum, as the zero start of the example shows. The factors themselves need not converge.

## Complexity

The model is the word RAM with real numbers of fixed size.

- **Forming the systems.** Line L8 adds an $r \times r$ outer product for each rating of $x$. Over all users this costs $O(s r^2)$, and the same over all items.
- **Solving.** One Cholesky solve costs $O(r^3)$, so a half step costs $O(m r^3)$ or $O(n r^3)$.
- **One sweep.** $O(s r^2 + (m + n) r^3)$. All $T$ sweeps cost $O(T (s r^2 + (m + n) r^3))$. Computing $J$ for a stopping rule adds $O(s r)$ per sweep.
- **Space.** The factors take $O((m + n) r)$, and one system takes $O(r^2)$ at a time, or one per processor in a parallel run.

Since $r$ is usually small next to $s / (m + n)$, the $s r^2$ term is often the larger one.

## Properties

- **Monotone.** $J$ never increases, from one half step to the next. This holds without a step size, unlike [stochastic gradient descent](/stochastic-gradient-descent/).
- **Parallel.** All users of one half step are independent, and so are all items.
- **Block coordinate descent.** ALS is [coordinate descent](/coordinate-descent/) with two blocks, $P$ and $Q$, each minimized exactly.
- **Local.** The result depends on the start, and the global minimum is not certified.
- **Deterministic after the start.** Given $Q$ at line L1, the run is fixed.

## Variants and improvements

- **ALS-WR.** The weights $c_u = |I_u|$ and $c_i = |U_i|$ of Zhou et al. Their paper starts the movie matrix with the average rating of each movie in the first row and small random numbers in the other rows, and stops when the RMSE on the probe set changes by less than 1 basis point (0.0001) between rounds.
- **Implicit feedback.** [ALS for implicit feedback](/implicit-feedback-als/) treats every pair as known, with a confidence weight, and uses an algebraic trick to keep the cost close to linear in the nonzero entries.
- **Biases.** Add to each item vector a coordinate that the item step keeps at 1, and the matching user coordinate acts as a user bias; the reverse gives item biases.
- **Inexact solves.** A few steps of the [conjugate gradient method](/conjugate-gradient-method/) in place of the Cholesky solve lower the cost per row when $r$ is large. Started from the old vector, conjugate gradient does not increase $J$, but the half step no longer minimizes it.
- **Gradient training.** [Matrix factorization](/matrix-factorization-recommendation/) by SGD fits the same model with cheaper steps and no linear solves.

## When to use it

Use ALS when the ratings are on many machines and each machine can hold the factors of the other side, when the data is implicit, so that all pairs count, or when a step size is hard to tune. Koren, Bell and Volinsky (2009) say that SGD is easier and faster in general, and that ALS is the better choice when the system can use parallelization and when the data is implicit. Zhou et al. report Netflix RMSE values from 0.9114 with 50 hidden features to 0.8985 with 1000 features for ALS-WR, and that they did not see overfitting as the number of features grew in their tests. These are measurements on one data set, not guarantees.

## Pitfalls

- **No penalty.** With $\lambda = 0$, a user with fewer than $r$ ratings has a singular matrix in line L8. Keep $\lambda > 0$, or the Cholesky decomposition can break down.
- **Zero start.** $Q = 0$ is a fixed point of ALS, as in the example. Start from small random values or from item means.
- **Explicit inverses.** Compute $A^{-1} b$ by a Cholesky or [QR](/qr-decomposition/) solve, not by forming $A^{-1}$.
- **Stopping on the factors.** The values of $J$ converge, but nothing proved here makes the factors converge, and they can keep moving while $J$ hardly changes. Stop on the change in $J$ or on the error of held out ratings.
- **Missing entries as zeros.** For explicit ratings, the sums of line L8 run over the known ratings of $x$ only. Summing over all items treats blanks as ratings of zero.
- **Comparing penalties.** The plain and the weighted penalty need different values of $\lambda$.

## Implementations

## History

Zhou, Wilkinson, Schreiber and Pan presented ALS with weighted lambda regularization at AAIM 2008 as a method for the Netflix Prize that runs in parallel. The same year, Hu, Koren and Volinsky adapted ALS to implicit feedback, where every user and item pair enters the loss. In their 2009 survey in IEEE Computer, Koren, Bell and Volinsky listed ALS and stochastic gradient descent as the two learning methods for the factor model.

## References
