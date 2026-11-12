---
tag: DZDDDE
kind: algorithm
slug: elastic-net
name: Elastic net
aliases:
- elastic net regression
- elastic-net regularization
area: machine-learning/supervised-learning
level: advanced
summary: Least squares with both an L1 and an L2 penalty. It is sparse like the lasso, keeps correlated features together, and is solved by coordinate descent.
solves: [linear-regression]
model: real-ram
complexity:
  vars: {n: the number of examples, d: the number of features, k: the number of sweeps}
  time: {worst: O(k n d), best: Θ(n d)}
  space: {extra: Θ(n d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2005
  people: [Hui Zou, Trevor Hastie]
  note: Zou and Hastie proposed the elastic net in 2005, with the naive and the rescaled forms and the grouping effect. glmnet (2010) solves it by coordinate descent.
prereqs: [lasso-regression, ridge-regression]
see_also: [coordinate-descent, proximal-operator, regularization, cross-validation, logistic-regression, generalized-linear-model]
sources:
  - paper: doi:10.1111/j.1467-9868.2005.00503.x
    title: Hui Zou and Trevor Hastie, Regularization and variable selection via the elastic net, Journal of the Royal Statistical Society Series B 67(2), 301 to 320, 2005
    locator: Section 2.1 (the naive elastic net), Lemma 1 (the augmented lasso form), Section 2.3 and Theorem 1 (the grouping effect), Section 3.1 and Theorem 2 (the rescaled elastic net)
  - paper: doi:10.18637/jss.v033.i01
    title: Jerome Friedman, Trevor Hastie and Robert Tibshirani, Regularization paths for generalized linear models via coordinate descent, Journal of Statistical Software 33(1), 1 to 22, 2010
    locator: Section 2 and Section 2.1 (the penalty λ(α|β|_1 + (1 - α)|β|^2/2) and its coordinate update)
  - book: isbn:9781498712163
    title: Trevor Hastie, Robert Tibshirani and Martin Wainwright, Statistical Learning with Sparsity, the Lasso and Generalizations, CRC Press, 2015
    locator: Section 4.2 (the elastic net, its coordinate update and the case of identical features)
---

The elastic net fits a [linear regression](/linear-regression/) with a penalty that mixes the L1 penalty of the [lasso](/lasso-regression/) and the squared L2 penalty of [ridge regression](/ridge-regression/). The L1 part sets some weights exactly to zero. The L2 part makes the problem strictly convex, so the solution is unique, and it gives the grouping effect: features that are strongly correlated get similar weights, and enter or leave the model together. The lasso, in the same situation, tends to keep one of them. Zou and Hastie (2005) proposed it. It is solved by cyclic [coordinate descent](/coordinate-descent/), with the same soft thresholding as the lasso and one extra term in the denominator.

## In plain words

The lasso makes many weights zero, which gives a small model. But when two inputs carry almost the same information, the lasso often keeps one and drops the other, and which one it keeps can depend on small details of the data. Ridge regression keeps both and gives them similar weights, but it never sets a weight to zero.

The elastic net uses both costs at the same time. One cost is the sum of the sizes of the weights, as in the lasso. The other is the sum of their squares, as in ridge. The result keeps only some inputs, and inputs that move together are kept or dropped together. The solver changes one weight at a time, in the same way as for the lasso.

## The problem

The data are $X \in \mathbb{R}^{n \times d}$ with columns $x_j$ and $y \in \mathbb{R}^n$. With the scaling of the lasso page, for $\lambda_1, \lambda_2 \ge 0$, the **naive elastic net** is

$$(\hat w, \hat b) = \arg\min_{w,\, b}\; F(w, b) = \frac{1}{2n}\|y - Xw - b\mathbf{1}\|_2^2 + \lambda_1\|w\|_1 + \frac{\lambda_2}{2}\|w\|_2^2 .$$

glmnet writes the penalty as $\lambda\left(\alpha\|w\|_1 + \frac{1-\alpha}{2}\|w\|_2^2\right)$ with $0 \le \alpha \le 1$, which is $\lambda_1 = \alpha\lambda$ and $\lambda_2 = (1 - \alpha)\lambda$. Here $\lambda_2 = 0$ is the lasso and $\lambda_1 = 0$ is ridge. The intercept is not penalized. As for the lasso and ridge, center $X$ and $y$, solve without intercept, and set $\hat b = \bar y - \bar x^\top\hat w$. From here on the data are centered.

**The augmented lasso form** (Zou and Hastie, Lemma 1). Let

$$X^* = \begin{pmatrix} X \\ \sqrt{n\lambda_2}\, I_d \end{pmatrix}, \qquad y^* = \begin{pmatrix} y \\ 0 \end{pmatrix}.$$

Then $\frac{1}{2n}\|y^* - X^*w\|^2 = \frac{1}{2n}\|y - Xw\|^2 + \frac{\lambda_2}{2}\|w\|^2$, so the naive elastic net is a lasso on $n + d$ rows (with the loss still divided by $n$). The matrix $X^*$ has rank $d$ when $\lambda_2 > 0$, so the problem is strictly convex and the solution is unique, also for $d > n$, and the model can select all $d$ features, while the lasso selects at most $n$.

**Optimality.** With $r = y - Xw$, $w$ is the minimizer exactly when, for each $j$,

$$\frac1n x_j^\top r - \lambda_2 w_j = \lambda_1\operatorname{sign}(w_j) \text{ if } w_j \ne 0, \qquad \left|\frac1n x_j^\top r\right| \le \lambda_1 \text{ if } w_j = 0 .$$

**The corrected (rescaled) elastic net.** The naive estimate shrinks twice: once by the L1 part and once more by the L2 part. Zou and Hastie found that this extra shrinkage adds bias without much drop in variance, and proposed the rescaled estimate

$$\hat w^{\text{enet}} = (1 + \lambda_2)\,\hat w^{\text{naive}},$$

for standardized columns with $\frac1n x_j^\top x_j = 1$. By their Theorem 2, in this scaling $\hat w^{\text{enet}}$ minimizes $\frac12 w^\top\frac{\hat\Sigma + \lambda_2 I}{1 + \lambda_2}w - \frac1n y^\top Xw + \lambda_1\|w\|_1$, with $\hat\Sigma = X^\top X/n$. So the elastic net is a lasso with the correlation matrix shrunk toward the identity. glmnet returns the naive form.

## The algorithm

As a function of $w_j$ alone, $F$ is $\frac{a_j + \lambda_2}{2}w_j^2 - \rho_j w_j + \lambda_1|w_j|$ plus a constant, with $a_j = \|x_j\|^2/n$ and $\rho_j = \frac1n x_j^\top(r + x_j w_j)$. Its minimizer is a soft thresholding:

$$w_j = \frac{S(\rho_j, \lambda_1)}{a_j + \lambda_2}, \qquad S(z, t) = \operatorname{sign}(z)\max(|z| - t, 0).$$

```pseudo id=main
ELASTIC-NET-CD(X, y, λ₁, λ₂, tol, corrected)
L1  x̄ ← the column means of X;  ȳ ← the mean of y;  center X and y
L2  a_j ← ‖x_j‖² / n for each j;  w ← 0;  r ← y
L3  repeat
L4      for j ← 1 to d with a_j + λ₂ > 0 do
L5          ρ ← x_jᵀ r / n + a_j w_j
L6          w_new ← S(ρ, λ₁) / (a_j + λ₂)
L7          r ← r − x_j (w_new − w_j);  w_j ← w_new
L8  until no weight moved by more than tol in the last sweep
L9  if corrected then w ← (1 + λ₂) w
L10 b ← ȳ − x̄ᵀ w
L11 return (w, b)
```

The only change from the lasso is the term $\lambda_2$ in the denominator of line L6. Line L5 uses the residual $r$ that line L7 keeps up to date, so a sweep costs $O(nd)$. Line L9 is the rescaling of Zou and Hastie. It must come after the loop, because the fit itself is the naive one. glmnet adds a path of $\lambda$ values with warm starts and active set sweeps, as for the lasso.

## Example

Use the two correlated features of the lasso page with a different response, $n = 6$:

| $x_1$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $x_2$ | 2 | 1 | 4 | 3 | 6 | 5 |
| $y$ | 2 | 2 | 5 | 4 | 8 | 7 |

After centering, $a_1 = a_2 = 35/12$, $x_1^\top x_2/n = 29/12$ (correlation 0.83), $x_1^\top y/n = 7/2$ and $x_2^\top y/n = 23/6$. Take $\lambda_1 = 2$ and $\lambda_2 = 1$, so the denominator of line L6 is $35/12 + 1 = 47/12 = 3.9167$.

| sweep | $j$ | $\rho$ | $S(\rho, 2)$ | new $w$ |
|---|---|---|---|---|
| 1 | 1 | 3.5000 | 1.5000 | $(0.3830, 0)$ |
| 1 | 2 | 2.9078 | 0.9078 | $(0.3830, 0.2318)$ |
| 2 | 1 | 2.9399 | 0.9399 | $(0.2400, 0.2318)$ |
| 2 | 2 | 3.2534 | 1.2534 | $(0.2400, 0.3200)$ |
| 3 | 1 | 2.7266 | 0.7266 | $(0.1855, 0.3200)$ |
| 3 | 2 | 3.3850 | 1.3850 | $(0.1855, 0.3536)$ |

The sweeps converge to the unique solution $\hat w = (26/171, 64/171) = (0.1520, 0.3743)$, with $\hat b = 14/3 - 3.5 \cdot 90/171 = 161/57 = 2.8246$. Both features stay in the model. The lasso with the same $\lambda_1 = 2$ gives $\hat w = (0, 22/35)$: it drops $x_1$, although $x_1$ and $x_2$ are almost equally related to $y$. The rescaled form multiplies the naive weights by $1 + \lambda_2 = 2$, which gives $(52/171, 128/171) = (0.3041, 0.7485)$.

## Correctness

Each step of line L6 minimizes $F$ exactly in one coordinate, and $F$ is $(a_j + \lambda_2)$-strongly convex in that coordinate, so each step lowers $F$ by at least $\frac{a_j + \lambda_2}{2}(\Delta w_j)^2$. The sum of the squared movements over all sweeps is finite, so the movements go to 0 and line L8 stops. At a limit point no coordinate can move, which is the optimality condition above, and that is the global minimum because $F$ is convex. For $\lambda_2 > 0$, $F$ is strongly convex, so the minimizer is unique and the whole sequence converges to it. The proof below gives the details.

## Complexity

The same as for the lasso. One sweep costs $\Theta(nd)$, so $k$ sweeps cost $O(knd)$, plus $\Theta(nd)$ for centering. When $\lambda_2 > 0$, the objective is $\lambda_2$-strongly convex, and cyclic coordinate descent converges at a linear rate. A larger $\lambda_2$ makes the problem better conditioned and needs fewer sweeps. The extra memory is $\Theta(nd)$ for the centered copy of $X$. The augmented form would need $\Theta((n + d)d)$, so the algorithm puts $\lambda_2$ into the denominator instead.

## Properties

### The grouping effect

If $x_i = x_j$, then $\hat w_i = \hat w_j$ for each $\lambda_2 > 0$. Proof: swapping $w_i$ and $w_j$ does not change $F$, so it maps the unique minimizer to itself. The lasso has no such property: any split of the weight is optimal.

More generally (Zou and Hastie, Theorem 1), let the columns be standardized with $\frac1n x_j^\top x_j = 1$, let $\rho_{ij} = \frac1n x_i^\top x_j$ be the sample correlation, and assume $\hat w_i \hat w_j > 0$. Then, in the scaling of this page,

$$|\hat w_i - \hat w_j| \le \frac{\sqrt{2(1 - \rho_{ij})}}{\lambda_2}\cdot\frac{\|y\|_2}{\sqrt n} .$$

*Proof.* The optimality conditions for $i$ and $j$ have the same sign on the right, so subtracting them gives $\lambda_2(\hat w_i - \hat w_j) = \frac1n(x_i - x_j)^\top r$. By Cauchy-Schwarz the right side is at most $\frac1n\|x_i - x_j\|\,\|r\|$. Here $\|x_i - x_j\|^2 = 2n(1 - \rho_{ij})$, and $\|r\| \le \|y\|$ because $F(\hat w) \le F(0)$. $\blacksquare$

So when $\rho_{ij}$ is close to 1, the two weights are close. The paper states the bound in its scaling, with the factor $\|y\|_1$, which is larger than $\|y\|_2$.

### Other properties

- **Unique solution** for $\lambda_2 > 0$, for each $X$.
- **Up to $d$ nonzero weights.** The lasso keeps at most $\min(n, d)$ features (for a unique solution). The elastic net can keep all $d$, which matters when $d \gg n$, as in gene expression data.
- **Bayesian view.** The penalty is the negative log of a prior that is a product of a Laplace and a Gaussian density for each weight.
- **Not scale equivariant.** Standardize the features first. The rescaling of line L9 assumes it.

## Variants and improvements

- **LARS-EN.** Zou and Hastie computed the path by LARS on the augmented data, for a fixed $\lambda_2$.
- **glmnet.** Pathwise coordinate descent over $\lambda$ for a fixed $\alpha$, for linear, [logistic](/logistic-regression/), Poisson and Cox models. For a [GLM](/generalized-linear-model/), the same update runs inside each IRLS step with weights.
- **Proximal gradient.** The proximal operator of the elastic net penalty is $w \mapsto S(w, \eta\lambda_1)/(1 + \eta\lambda_2)$, so ISTA and FISTA apply directly.
- **Choosing $\alpha$ and $\lambda$.** Cross-validate over a grid of $\alpha$ values and, for each, over the path of $\lambda$.
- **Adaptive elastic net and group lasso.** Weighted L1 terms, or penalties on predefined groups of features.

## When to use it

Use the elastic net when you want a sparse model and the features come in groups of strongly correlated ones, or when $d \gg n$ and you expect more than $n$ features to matter. It is a safe default between the lasso and ridge: with $\alpha$ close to 1 it behaves like the lasso, and it still has a unique, stable solution. Choose $\lambda$, and $\alpha$ if needed, by [cross-validation](/cross-validation/).

## Pitfalls

- **Naive or rescaled.** The two forms differ by the factor $1 + \lambda_2$. Libraries such as glmnet and scikit-learn return the naive form. Know which one you report.
- **Scalings of the penalty.** The same names $\lambda$ and $\alpha$ mean different things in different libraries (for example $\frac{1}{2n}$ or $\frac12$ in front of the loss, and $\frac{\lambda_2}{2}$ or $\lambda_2$ in front of the L2 term).
- **Rescaling without standardization.** The factor $1 + \lambda_2$ matches Theorem 2 of Zou and Hastie only when $\frac1n x_j^\top x_j = 1$.
- **Rescaling inside the loop.** Line L9 is applied once, after convergence. Applying it to each update changes the problem.
- **Penalizing the intercept.** Center the data as in lines L1 and L10.

## Implementations

## History

Zou and Hastie (2005) proposed the elastic net to fix three limits of the lasso: it selects at most $n$ features, it picks one feature at random from a group of correlated ones, and it predicts worse than ridge when the features are strongly correlated. They gave the naive form, its augmented lasso representation, the grouping theorem, the rescaled form and the LARS-EN algorithm. Friedman, Hastie and Tibshirani (2010) made pathwise coordinate descent in glmnet the standard way to fit it, also for generalized linear models.

## References
