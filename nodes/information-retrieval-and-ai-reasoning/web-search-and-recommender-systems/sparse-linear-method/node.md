---
tag: XKTFZV
kind: algorithm
slug: sparse-linear-method
name: Sparse linear method for recommendation
aliases:
- SLIM
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: research
summary: Learns a sparse item-item weight matrix with zero diagonal by elastic-net regression of the interaction matrix on itself.
solves: [recommendation-problem]
model: word-ram
complexity:
  vars: {m: the number of users, n: the number of items, s: the number of nonzero entries of A, T: the number of coordinate descent sweeps per column}
  time: {worst: O(T n s)}
  space: {extra: O(n^2 + m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2011
  people: [Xia Ning, George Karypis]
  note: Ning and Karypis (ICDM 2011) proposed SLIM as a model that keeps the sparse item-item form of item kNN but learns the weights by an elastic net with nonnegativity and a zero diagonal.
prereqs: [item-based-collaborative-filtering, elastic-net, coordinate-descent]
see_also: [implicit-feedback, implicit-feedback-als, bayesian-personalized-ranking, lasso-regression, ridge-regression, kkt-conditions, proximal-operator, top-k-selection]
sources:
  - paper: doi:10.1109/ICDM.2011.134
    title: Xia Ning and George Karypis, SLIM, sparse linear methods for top-N recommender systems, 11th IEEE International Conference on Data Mining (ICDM 2011), 497-506
    locator: the SLIM model and its optimization problem with W >= 0 and diag(W) = 0, the split into independent column problems, fsSLIM (feature selection with item kNN), and the leave-one-out evaluation with HR and ARHR on eight data sets
  - paper: doi:10.18637/jss.v033.i01
    title: Jerome Friedman, Trevor Hastie and Robert Tibshirani, Regularization paths for generalized linear models via coordinate descent, Journal of Statistical Software 33(1), 2010
    locator: Section 2 (coordinate descent for the elastic net, the soft-thresholding update)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, 2nd edition, Springer, 2009
    locator: Section 3.4 (shrinkage methods, ridge regression and the lasso)
---

The sparse linear method (SLIM) of Ning and Karypis (2011) recommends items with a learned item-to-item weight matrix $W$. The score of item $i$ for user $u$ is $\tilde a_{ui} = a_u^\top w_i$, a weighted sum of the user's own past items, as in [item-based collaborative filtering](/item-based-collaborative-filtering/). The difference is that the weights are not a fixed similarity such as the cosine: they are the solution of an [elastic net](/elastic-net/) regression of the user-item matrix $A$ on itself, with $W \ge 0$ and a zero diagonal so that an item cannot predict itself. The $\ell_1$ penalty makes $W$ sparse, so scoring stays as cheap as in item kNN.

## In plain words

Item kNN says: users who bought this also bought that, and it measures "also" with a fixed formula. SLIM instead asks, for each item, which other items best predict who has it, and it learns the answer from data. It forbids an item from predicting itself, since that would be a trivial perfect fit, and it forbids negative weights.

A penalty pushes most weights to exactly zero, so each item keeps only a few strong neighbors. Each item can be learned on its own, which makes the training easy to split across machines.

## The problem

The input is the $m \times n$ matrix $A$ of users and items, with 0/1 entries for purchases or clicks, or ratings; $a_j$ is column $j$. Given $\beta > 0$ and $\lambda \ge 0$, SLIM solves

$$\min_{W} \; \tfrac12 \lVert A - A W \rVert_F^2 + \tfrac{\beta}{2} \lVert W \rVert_F^2 + \lambda \lVert W \rVert_1 \quad \text{subject to } W \ge 0, \; \operatorname{diag}(W) = 0.$$

The objective and the constraints split by columns, so this is $n$ independent problems,

$$\min_{w_j} \; \tfrac12 \lVert a_j - A w_j \rVert^2 + \tfrac{\beta}{2} \lVert w_j \rVert^2 + \lambda \lVert w_j \rVert_1 \quad \text{subject to } w_j \ge 0, \; w_{jj} = 0,$$

each a nonnegative elastic net. Without the constraint $w_{jj} = 0$ the problem would have the useless answer close to $W = I$. The output is $W$, and the recommendation for $u$ is the items with the largest entries of $a_u^\top W$ among the items $u$ has not used.

## The algorithm

The page solves each column by cyclic [coordinate descent](/coordinate-descent/), the standard solver for the elastic net (Friedman, Hastie and Tibshirani, 2010). The step for one coordinate is a soft threshold clipped at zero.

```pseudo id=main
SLIM(A, β, λ, tol)
L1  for each item j do                         ▷ the columns are independent
L2      w ← 0; e ← a_j                         ▷ e = a_j - A w, the residual
L3      repeat until no coordinate moves by more than tol in a sweep
L4          for each item k ≠ j with a_k ≠ 0 do
L5              ρ ← a_kᵀ e + ‖a_k‖² w_k
L6              t ← max(0, ρ - λ) / (‖a_k‖² + β)
L7              e ← e - a_k (t - w_k); w_k ← t
L8      column j of W ← w                      ▷ w_j stayed 0
L9  return W

RECOMMEND(u, N)
L10 return the N items i with a_ui = 0 and the largest (a_uᵀ W)_i
```

Line L5 is the correlation of $a_k$ with the residual that would remain if $w_k$ were 0. Line L6 shrinks it by $\lambda$, sets it to 0 if it is below $\lambda$, and divides by the curvature. Line L7 keeps the residual current at a cost of one column.

## Example

Five users and four items, with $\beta = \lambda = 0.5$:

| | $i_1$ | $i_2$ | $i_3$ | $i_4$ |
|---|---|---|---|---|
| $u_1$ | 1 | 1 | 0 | 0 |
| $u_2$ | 1 | 1 | 1 | 0 |
| $u_3$ | 0 | 1 | 1 | 0 |
| $u_4$ | 0 | 0 | 1 | 1 |
| $u_5$ | 1 | 0 | 0 | 1 |

For column $i_1$, $a_1 = (1, 1, 0, 0, 1)$. The correlations with the other columns are $a_2^\top a_1 = 2$, $a_3^\top a_1 = 1$ and $a_4^\top a_1 = 1$, and the squared norms are 3, 3 and 2. Columns $a_2$ and $a_4$ have no user in common, so they do not interact. The solution has $w_{21} = (2 - 0.5) / (3 + 0.5) = 3/7$, $w_{41} = (1 - 0.5) / (2 + 0.5) = 1/5$ and $w_{31} = 0$. The KKT condition for $i_3$ holds: the residual is $e = (4/7, 4/7, -3/7, -1/5, 4/5)$, so $a_3^\top e = -2/35$, which is below $\lambda$, and $w_{31} = 0$ is optimal.

The full matrix, with $W_{kj}$ the weight of item $k$ in the prediction of item $j$, is

| | $i_1$ | $i_2$ | $i_3$ | $i_4$ |
|---|---|---|---|---|
| $i_1$ | 0 | 1/3 | 0 | 1/9 |
| $i_2$ | 3/7 | 0 | 3/7 | 0 |
| $i_3$ | 0 | 1/3 | 0 | 1/9 |
| $i_4$ | 1/5 | 0 | 1/5 | 0 |

The diagonal is zero, every entry is nonnegative, and 4 of the 12 entries off the diagonal are 0. User $u_1$ has $a_1 = (1, 1, 0, 0)$, so the scores are rows $i_1$ plus $i_2$: $(3/7, 1/3, 3/7, 1/9)$. Among the unused items, $i_3$ scores $3/7$ and $i_4$ scores $1/9$, so SLIM recommends $i_3$ first. The test file checks these numbers.

## Correctness

The proof in `proofs/correctness.md` has four steps. The problem splits into one problem per column. Each column problem is strongly convex on the set $\{w \ge 0, w_j = 0\}$ because $\beta > 0$, so it has a unique minimizer, which the [KKT conditions](/kkt-conditions/) characterize: with $g_k = -a_k^\top(a_j - A w) + \beta w_k$, every $k \ne j$ has $g_k + \lambda = 0$ if $w_k > 0$ and $g_k + \lambda \ge 0$ if $w_k = 0$. Line L6 is the exact minimizer of the objective in one coordinate over $w_k \ge 0$, and it lowers the objective by at least $\frac{\beta}{2}$ times the square of the move. Since the nonsmooth part is a sum of functions of one coordinate each, every limit point of the coordinate descent satisfies the KKT conditions, and the iterates converge to the unique minimizer. The tests check the KKT conditions at the computed solution to $10^{-9}$, and compare with a brute force that tries every support in exact rational arithmetic.

## Complexity

- **One coordinate step.** Lines L5 and L7 cost $O(\text{nnz}(a_k))$ with sparse columns.
- **One sweep of one column.** $O(s)$, since the columns hold $s$ nonzero entries in total. With dense columns it is $O(m n)$.
- **All columns.** $O(T n s)$ for $T$ sweeps per column, and the $n$ columns can run in parallel. Precomputing the Gram matrix $A^\top A$ once, in $O(\sum_u |I_u|^2)$ time, makes each coordinate step cost $O(n)$ instead.
- **Space.** $O(m)$ for the residual of one column, and $O(n^2)$ for $W$ in the worst case; a sparse $W$ needs space proportional to its nonzero entries.
- **Scoring.** $a_u^\top W$ costs time proportional to the nonzero weights in the rows of the items of $u$.

## Properties

- **Sparse model.** The $\ell_1$ penalty sets many weights to exactly 0, so $W$ is as cheap to apply as an item kNN table.
- **Convex.** Unlike [matrix factorization](/matrix-factorization-recommendation/), each column problem is convex, so the result does not depend on the start.
- **Parallel.** The $n$ column problems are independent.
- **Interpretable.** Each recommendation is a sum of nonnegative contributions of the user's past items.

## Variants and improvements

- **fsSLIM.** Feature selection: restrict the support of $w_j$ to the columns of the item kNN neighbors of $j$. Each column problem then has a few variables in place of $n - 1$, which cuts the training time.
- **Other solvers.** [Proximal gradient](/proximal-gradient-method/) steps, with the [proximal operator](/proximal-operator/) of $\lambda \lVert w \rVert_1$ plus the constraint, give the same solution. A solver with active sets or warm starts along a path of $\lambda$ values speeds up the tuning.
- **Ridge only.** With $\lambda = 0$ and without the sign constraint, the problem has a closed form through $(A^\top A + \beta I)^{-1}$, and the zero diagonal can be enforced with a Lagrange multiplier per column. The model is then dense.

## When to use it

Use SLIM for top-N recommendation from purchase or click data when the catalog is of moderate size, when fast scoring matters, and when a convex model with no random start is preferred. Ning and Karypis evaluated it on eight data sets with leave-one-out cross-validation, measuring the hit rate HR $= \#\text{hits} / \#\text{users}$ and the average reciprocal hit rank, and compared it with item kNN and with matrix factorization methods, including the time to learn and to apply each model. Their reported results favor SLIM on their data sets. These are measurements; the method has no guarantee about ranking quality.

## Pitfalls

- **Forgetting the zero diagonal.** Without $w_{jj} = 0$ the minimizer is close to $W = I$ for small penalties, and every user gets their own past items back.
- **The scale of $\lambda$.** With $\lambda$ larger than every $a_k^\top a_j$, all weights are 0 and SLIM recommends nothing useful. The test file checks this case.
- **Dense $A^\top A$.** For a large catalog, the Gram matrix has up to $n^2$ entries. Use the sparse residual form of lines L5 and L7, or fsSLIM.
- **Stopping too early.** A loose tolerance leaves small positive weights that the exact solution would set to 0, so the model is less sparse than expected. Check the KKT conditions, not only the change in the objective.
- **Ratings as targets.** On rating data, $A$ holds the ratings, and the regression then fits rating values; the top-N list should still leave out the items the user has rated.

## Implementations

## History

Ning and Karypis presented SLIM at ICDM 2011 as a way to get the speed of the item-based top-N methods of Deshpande and Karypis together with the quality of learned models. The elastic net is due to Zou and Hastie (2005), and coordinate descent for it was popularized by Friedman, Hastie and Tibshirani (2010).

## References
