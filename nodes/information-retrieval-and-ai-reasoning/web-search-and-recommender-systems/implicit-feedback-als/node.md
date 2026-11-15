---
tag: 84ZRE0
kind: algorithm
slug: implicit-feedback-als
name: Weighted matrix factorization for implicit feedback
aliases:
- implicit ALS
- Hu-Koren-Volinsky model
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Factorizes binary preferences with confidence weights from counts, using a sum over all cells that ALS evaluates in time linear in the data.
solves: [recommendation-problem]
model: word-ram
complexity:
  vars: {m: the number of users, n: the number of items, s: the number of nonzero counts, r: the number of factors, T: the number of sweeps}
  time: {worst: O(T (s r^2 + (m + n) r^3))}
  space: {extra: O((m + n) r + r^2)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2008
  people: [Yifan Hu, Yehuda Koren, Chris Volinsky]
  note: Hu, Koren and Volinsky (ICDM 2008) gave the model with 0/1 preferences and confidence weights, and the ALS solve that uses Y^T Y so that the zero cells cost nothing extra.
prereqs: [implicit-feedback, alternating-least-squares]
see_also: [bayesian-personalized-ranking, matrix-factorization-recommendation, ridge-regression, cholesky-decomposition, conjugate-gradient-method, sparse-linear-method, coordinate-descent]
sources:
  - paper: doi:10.1109/ICDM.2008.22
    title: Yifan Hu, Yehuda Koren and Chris Volinsky, Collaborative filtering for implicit feedback datasets, Eighth IEEE International Conference on Data Mining (ICDM 2008), 263-272
    locator: Section 4 (Equation 3 for the cost, Equation 4 for the user step with the Y^T Y identity and its cost, Equation 5 for the item step, Equation 6 for the log scaling of the confidence), Section 5 (explaining recommendations), Section 6 (expected percentile ranking on the TV data)
  - paper: doi:10.1109/MC.2009.263
    title: Yehuda Koren, Robert Bell and Chris Volinsky, Matrix factorization techniques for recommender systems, IEEE Computer 42(8), 30-37, 2009
    locator: sections Learning algorithms and Inputs with varying confidence levels
  - paper: arxiv:1205.2618
    title: Steffen Rendle, Christoph Freudenthaler, Zeno Gantner and Lars Schmidt-Thieme, BPR, Bayesian personalized ranking from implicit feedback, Proceedings of the 25th Conference on Uncertainty in Artificial Intelligence (UAI 2009)
    locator: Section 5.1 (relation to weighted regularized matrix factorization)
---

Weighted matrix factorization for implicit feedback, often called implicit ALS, fits user vectors $x_u$ and item vectors $y_i$ so that $x_u^\top y_i$ is close to 1 where a user has used an item and close to 0 elsewhere, with a confidence weight on each cell that grows with the count. It differs from [alternating least squares](/alternating-least-squares/) for explicit ratings in what the loss sums over: explicit ALS sums only over the known ratings, while here every one of the $m n$ cells is a data point, because an empty cell also says something. A direct solve would cost time proportional to $m n$ in each step; the algebraic identity $Y^\top C^u Y = Y^\top Y + Y^\top (C^u - I) Y$ of Hu, Koren and Volinsky (2008) brings the cost of one sweep down to $O(s r^2 + (m + n) r^3)$, linear in the number $s$ of nonzero counts.

## In plain words

A play count or a click count is not a rating. A user who played a song 30 times probably likes it, and a user who never played a song may dislike it, or may never have heard of it. So the method treats every cell as a guess: "used" means a target of 1 and "not used" a target of 0, and a large count makes the method trust the 1 more.

There are many more empty cells than full ones. The trick is that every empty cell has the same weight, so their total effect is one small matrix per step that is shared by all users. Each user then only pays for the items that user actually used.

## The problem

The input is a set of counts $r_{ui} > 0$ for $s$ pairs of $m$ users and $n$ items; every other pair has $r_{ui} = 0$. Hu, Koren and Volinsky define the preference $p_{ui} = 1$ if $r_{ui} > 0$ and $p_{ui} = 0$ otherwise, and the confidence $c_{ui} = 1 + \alpha r_{ui}$, with $\alpha = 40$ in their experiments. Given $r$ and $\lambda > 0$, the method minimizes their Equation 3,

$$J(X, Y) = \sum_{u=1}^{m} \sum_{i=1}^{n} c_{ui} \bigl(p_{ui} - x_u^\top y_i\bigr)^2 + \lambda \Bigl( \sum_u \lVert x_u \rVert^2 + \sum_i \lVert y_i \rVert^2 \Bigr),$$

over $x_u, y_i \in \mathbb{R}^r$. Write $Y$ for the $n \times r$ matrix with rows $y_i^\top$, $C^u$ for the diagonal $n \times n$ matrix of the $c_{ui}$ of user $u$, and $p(u)$ for the vector of the $p_{ui}$. With $Y$ fixed, the best $x_u$ is the weighted [ridge regression](/ridge-regression/) solution (their Equation 4)

$$x_u = \bigl(Y^\top C^u Y + \lambda I\bigr)^{-1} Y^\top C^u p(u),$$

and the item step is the same with the roles exchanged (their Equation 5). The output is a ranked list per user: the unused items with the largest $x_u^\top y_i$.

## The algorithm

```pseudo id=main
IMPLICIT-ALS(counts, r, λ, α, T)
L1  for the s observed pairs: p_ui ← 1, c_ui ← 1 + α r_ui      ▷ all other cells have p = 0, c = 1
L2  Y ← small random n × r matrix; X ← 0
L3  repeat T times
L4      X ← HALF(users, Y)
L5      Y ← HALF(items, X)
L6  return X, Y

HALF(rows, Y)                         ▷ the vectors y_j of the other side are fixed
L7  G ← YᵀY                           ▷ once per half step, O(n r^2)
L8  for each row u do
L9      A ← G + λI + Σ_{j: r_uj > 0} (c_uj - 1) y_j y_jᵀ
L10     b ← Σ_{j: r_uj > 0} c_uj y_j
L11     x_u ← the solution of A x = b, by Cholesky decomposition
L12 return the vectors x_u
```

Line L9 is $Y^\top C^u Y + \lambda I$ written as $Y^\top Y + Y^\top (C^u - I) Y + \lambda I$: the diagonal matrix $C^u - I$ is zero on every item the user did not use. Line L10 is $Y^\top C^u p(u)$, since $p_{uj} = 0$ on those items too. A row with no counts gets $A = G + \lambda I$ and $b = 0$, so $x_u = 0$.

## Example

Three users, three items, counts

| | $i_1$ | $i_2$ | $i_3$ |
|---|---|---|---|
| $u_1$ | 2 | 1 | 0 |
| $u_2$ | 0 | 1 | 3 |
| $u_3$ | 1 | 0 | 0 |

with $\alpha = 1$, $\lambda = 1$, one factor ($r = 1$) and the start $y_i = 1$ for all items. The confidences of the nonzero cells are $c = 1 + r_{ui}$: 3 and 2 for $u_1$, 2 and 4 for $u_2$, and 2 for $u_3$. Line L7 gives $G = 1 + 1 + 1 = 3$.

| user | $A$ (line L9) | $b$ (line L10) | $x_u$ |
|---|---|---|---|
| $u_1$ | $3 + 1 + 2 + 1 = 7$ | $3 + 2 = 5$ | $5/7$ |
| $u_2$ | $3 + 1 + 1 + 3 = 8$ | $2 + 4 = 6$ | $3/4$ |
| $u_3$ | $3 + 1 + 1 = 5$ | $2$ | $2/5$ |

The direct form gives the same numbers. For $u_1$, $Y^\top C^u Y + \lambda = 3 + 2 + 1 + 1 = 7$, a sum over all three items with weight 1 on the empty cell $i_3$.

The objective at the start, with $X = 0$, is the sum of the confidences of the nonzero cells plus $\lambda \lVert Y \rVert^2$: $13 + 3 = 16$. A ridge step lowers $g_u$ by $b^2 / A$, so after the user step $J = 16 - 25/7 - 9/2 - 4/5 = 499/70 \approx 7.1286$. The item step then gives $y \approx (0.8622, 0.8860, 0.7653)$ and $J \approx 6.8048$. The test file checks these values.

## Correctness

The proof in `proofs/correctness.md` shows that the system of lines L9 and L10 is exactly $Y^\top C^u Y + \lambda I$ and $Y^\top C^u p(u)$, because $c_{ui} - 1 = 0$ and $p_{ui} = 0$ on the empty cells. With $Y$ fixed, $J$ splits into one strictly convex quadratic per user, so line L4 returns the unique minimizer over $X$, and line L5 the unique minimizer over $Y$. Hence $J$ does not increase after each half step, the values of $J$ converge, the iterates stay in a bounded set, and every limit point is a stationary point. The factors themselves need not converge, and a stationary point need not be the global minimum; the start $Y = 0$ is a fixed point.

## Complexity

The model is the word RAM with real numbers of fixed size.

- **Shared part.** Line L7 costs $O(n r^2)$ per user half step and $O(m r^2)$ per item half step.
- **Per row.** Lines L9 and L10 cost $O(n_u r^2)$ for a user with $n_u$ nonzero counts, and line L11 costs $O(r^3)$. Hu, Koren and Volinsky give the total as $O(r^2 s + r^3 m)$ for the user step.
- **One sweep.** $O(s r^2 + (m + n) r^3)$, and $T$ sweeps cost $O(T (s r^2 + (m + n) r^3))$. The paper used about 10 sweeps.
- **Without the identity.** Forming $Y^\top C^u Y$ directly costs $O(n r^2)$ per user, so $O(m n r^2)$ per half step, which is the cost of a dense problem.
- **Space.** $O((m + n) r)$ for the factors and $O(r^2)$ for $G$ and one system.

Computing $J$ exactly costs $O(m n r)$; it can be done in $O(s r + (m + n) r^2)$ with the same trick, but it is not needed to run the method.

## Properties

- **Monotone.** $J$ does not increase after each half step, with no step size.
- **Dense loss, sparse cost.** Every cell enters the loss, yet one sweep costs time linear in $s$.
- **Parallel.** The users of one half step are independent once $G$ is known, and so are the items.
- **Local.** The problem is not convex in $(X, Y)$, and the result depends on the start.
- **Explainable.** Section 5 of the paper writes the score as $\sum_{j} s^u_{ij} c_{uj}$ over the items $j$ the user used, with weights from $(Y^\top C^u Y + \lambda I)^{-1}$, so a recommendation can be traced to past items.

## Variants and improvements

- **Log confidence.** The paper also proposes $c_{ui} = 1 + \alpha \log(1 + r_{ui} / \epsilon)$ (Equation 6), with $\epsilon = 10^{-8}$ in its experiments.
- **Inexact solves.** A few steps of the [conjugate gradient method](/conjugate-gradient-method/), started from the old $x_u$, in place of line L11 lower the cost per row when $r$ is large. Each such step still does not increase $J$, but the half step no longer minimizes it exactly.
- **Pairwise loss.** [Bayesian personalized ranking](/bayesian-personalized-ranking/) fits the same scores with a loss on pairs of a used and an unused item, trained by sampling. Rendle et al. (2009, Section 5.1) contrast the two: the weighted least squares loss fits a score to each cell, while BPR optimizes the order.
- **Item models.** The [sparse linear method](/sparse-linear-method/) learns item-to-item weights from the same 0/1 matrix.

## When to use it

Use it when the data is counts or events with no negative signal, such as plays, views or purchases, when the catalog is large, and when the factors must be refit in parallel. Hu, Koren and Volinsky measured it on the TV viewing data of about 300,000 set-top boxes and 17,000 programs with the expected percentile ranking of the watched programs, where 50% is random and lower is better. They report 16.46% for ranking by popularity, 10.74% for an item-item neighborhood model, and 8.35% for the factor model with 200 factors, with the factor model improving as the number of factors grew. As with all recommender results, this is a measurement on one data set, not a proved property of the method.

## Pitfalls

- **Treating zeros as missing.** If the sums run only over the nonzero cells, every target is 1 and $x_u^\top y_i = 1$ fits everything. The empty cells must stay in the loss; the identity of line L9 is how they stay in cheaply.
- **Forming $Y^\top C^u Y$ directly.** It is correct but costs $O(n r^2)$ per user, so the method becomes as slow as a dense problem.
- **The scale of $\alpha$.** The confidence weights and $\lambda$ interact, so a new $\alpha$ usually needs a new $\lambda$.
- **Stopping on the factors.** The values of $J$ converge, but the factors can keep moving; stop on the change in $J$ or on a held-out ranking measure.
- **Reading $p_{ui} = 0$ as dislike.** The model only gives low confidence to the zero. A held-out evaluation should still count an unused item as unknown, not as a true negative.

## Implementations

## History

Hu, Koren and Volinsky presented the model at ICDM 2008, working with TV viewing data, where only watching time was recorded. The same conference had the one-class collaborative filtering paper of Pan, Zhou, Cao, Liu, Lukose, Scholz and Yang (ICDM 2008, 502-511), which also put weights on the missing cells. Rendle et al. (2009) compared both of these with their pairwise BPR loss, and Koren, Bell and Volinsky (2009) described confidence levels for implicit inputs in their survey of matrix factorization.

## References
