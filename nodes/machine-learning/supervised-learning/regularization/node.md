---
tag: M5KEQK
kind: technique
slug: regularization
name: Regularization
aliases:
- regularisation
- weight penalty
- regularized loss minimization
area: machine-learning/supervised-learning
level: intro
summary: "Minimize the training loss plus a penalty such as lambda times the squared L2 norm or the L1 norm of the weights, or under a norm constraint, to trade fit for stability and reduce overfitting."
prereqs: [overfitting, convex-function, lagrangian-duality]
see_also: [ridge-regression, lasso-regression, elastic-net, early-stopping, weight-decay, structural-risk-minimization, maximum-a-posteriori-estimation, bias-variance-tradeoff]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Chapter 13 (regularized loss minimization; Section 13.2, stable rules do not overfit; Section 13.3, Tikhonov regularization as a stabilizer; Section 13.4, the fitting-stability tradeoff)
  - url: https://www.jmlr.org/papers/v2/bousquet02a.html
    title: Olivier Bousquet and André Elisseeff, Stability and generalization, Journal of Machine Learning Research 2, 2002
    locator: the notions of hypothesis and uniform stability, the generalization bounds for stable algorithms, and the stability of regularization in a reproducing kernel Hilbert space
  - paper: doi:10.1080/00401706.1970.10488634
    title: Arthur E. Hoerl and Robert W. Kennard, Ridge regression, biased estimation for nonorthogonal problems, Technometrics 12(1), 1970
    locator: the ridge estimator and its mean squared error
  - paper: doi:10.1111/j.2517-6161.1996.tb02080.x
    title: Robert Tibshirani, Regression shrinkage and selection via the lasso, Journal of the Royal Statistical Society Series B 58(1), 1996
    locator: the constrained form of the lasso, the orthonormal design case and the Laplace prior reading
  - paper: "A. N. Tikhonov, Solution of incorrectly formulated problems and the regularization method, Soviet Mathematics Doklady 4, 1963"
    locator: the regularization method for ill-posed problems
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 5.2.3 (strong duality under Slater's condition) and Section 5.5.3 (the KKT conditions)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 3.4 (ridge regression and the lasso, their constrained forms and the orthonormal case)
  - paper: "Christopher M. Bishop, Training with noise is equivalent to Tikhonov regularization, Neural Computation 7(1), 1995"
    locator: the second-order expansion of the error under small input noise
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 7.1 (parameter norm penalties) and Section 7.8 (early stopping as a regularizer)
---

Regularization changes the training objective so that the learner prefers simple or small hypotheses: it minimizes the training loss plus a penalty $\lambda R(w)$, or the training loss under a constraint $R(w) \le t$. The two common penalties are the squared $L_2$ norm (Tikhonov regularization, used in [ridge regression](/ridge-regression/)) and the $L_1$ norm (used in the [lasso](/lasso-regression/)). For convex problems the penalized and constrained forms give the same solutions, by [Lagrange duality](/lagrangian-duality/). The penalty has three readings: a bias that lowers variance, a prior in [MAP estimation](/maximum-a-posteriori-estimation/), and a source of stability that bounds the [generalization error](/generalization-error/).

## In plain words

A learner that is free to use any weights it likes will often pick large, extreme weights that fit the training examples very closely, noise included. Regularization adds a cost for large weights to the training error. The learner must now balance two goals: fit the data, and keep the weights small. A single number, chosen by trying values on held-out data, sets the balance. A small cost gives a close fit; a large cost gives a smooth, cautious model. A cost on the sum of squares of the weights shrinks all of them a little. A cost on the sum of their sizes sets many weights to exactly zero, so it also picks features. Stopping a gradient method early has a similar effect, because the weights start at zero and grow step by step.

## When it applies

- **The class is rich for the data.** Many features compared with the number $n$ of examples, a high polynomial degree, a large network. The training error is much lower than the validation error ([overfitting](/overfitting/)).
- **The problem is ill posed.** In least squares, $X^\top X$ is singular or badly conditioned (collinear features, $d > n$), so the solution is not unique or changes a lot with small changes of the data. Tikhonov introduced the method for such inverse problems.
- **There is prior knowledge** that the weights are small, smooth or sparse.
- **A sparse model is wanted**, for interpretation or cost: use an $L_1$ penalty.
- **A stability or generalization guarantee is needed** for a convex learner: the strongly convex $L_2$ penalty gives one (below).

## The template

Notation: a sample $S$ of $n$ examples $(x_i, y_i)$ with $x_i \in \mathbb{R}^d$, a parameter vector $w$, a loss $\ell(w, z)$ on one example, and the empirical risk $L_S(w) = \frac1n \sum_i \ell(w, z_i)$. The data model is i.i.d. examples from an unknown $D$; the penalty weight is $\lambda \ge 0$.

```pseudo id=template
REGULARIZED-FIT(S, V, R, Λ, SOLVE)                  ▷ S training set, V validation set
L1  for each λ in Λ do                               ▷ Λ: a grid, often geometric
L2      w_λ ← SOLVE(min over w of L_S(w) + λ·R(w))   ▷ the penalty R and the solver are the holes
L3  λ* ← the λ in Λ with the least L_V(w_λ)          ▷ or the least cross-validation error
L4  return w_λ*                                       ▷ optionally refit on S ∪ V with λ*
```

The holes are the penalty $R$, the grid $\Lambda$, the solver and the rule that picks $\lambda$. Line L2 is regularized loss minimization (RLM). Common penalties: $R(w) = \|w\|_2^2$ (Tikhonov, $L_2$), $R(w) = \|w\|_1$ ($L_1$), $R(w) = \alpha\|w\|_1 + (1 - \alpha)\|w\|_2^2$ ([elastic net](/elastic-net/)), and $R(w) = \|\Gamma w\|_2^2$ for a fixed matrix $\Gamma$ (general Tikhonov, for example a difference operator for smoothness). The bias term $b$ is usually not penalized.

### Penalized and constrained forms

The constrained form (Ivanov regularization) is: minimize $L_S(w)$ subject to $R(w) \le t$.

**Claim 1 (penalized gives constrained).** If $w^\ast$ minimizes $L_S(w) + \lambda R(w)$ with $\lambda > 0$, then $w^\ast$ minimizes $L_S$ over $\{w : R(w) \le t\}$ for $t = R(w^\ast)$.

*Proof.* Take $w$ with $R(w) \le t = R(w^\ast)$. By the optimality of $w^\ast$, $L_S(w) + \lambda R(w) \ge L_S(w^\ast) + \lambda R(w^\ast)$, so $L_S(w) \ge L_S(w^\ast) + \lambda (R(w^\ast) - R(w)) \ge L_S(w^\ast)$. $\blacksquare$

This direction needs no convexity.

**Claim 2 (constrained gives penalized).** Let $L_S$ and $R$ be [convex](/convex-function/) and finite on $\mathbb{R}^d$, and let $t > \inf_w R(w)$. If $w^\ast$ minimizes $L_S$ over $\{R(w) \le t\}$, then there is $\lambda \ge 0$ such that $w^\ast$ minimizes $L_S(w) + \lambda R(w)$.

*Proof.* The problem is convex, and some $w$ has $R(w) < t$, which is Slater's condition. So strong duality holds and the dual optimum is attained (Boyd and Vandenberghe, Section 5.2.3): there is $\lambda \ge 0$ with $\min_{R(w) \le t} L_S(w) = \inf_w \big(L_S(w) + \lambda (R(w) - t)\big)$ and complementary slackness $\lambda (R(w^\ast) - t) = 0$. Then $L_S(w^\ast) + \lambda (R(w^\ast) - t) = L_S(w^\ast)$ equals the infimum of the Lagrangian, so $w^\ast$ minimizes $L_S(w) + \lambda R(w)$. If the constraint is not active, $\lambda = 0$. $\blacksquare$

So, for convex problems, the path of penalized solutions as $\lambda$ runs over $[0, \infty)$ and the path of constrained solutions as $t$ runs over $(0, \infty)$ trace the same set of minimizers, with a decreasing map between $\lambda$ and $t$. The map depends on the data, so a fixed $\lambda$ is not a fixed $t$ across data sets.

### The Bayesian reading

Let $y_i = w \cdot x_i + \varepsilon_i$ with $\varepsilon_i \sim N(0, \sigma^2)$ i.i.d. With the prior $w \sim N(0, \tau^2 I)$, Bayes' rule gives

$$-\log p(w \mid S) = \frac{1}{2\sigma^2} \sum_{i=1}^{n} (w \cdot x_i - y_i)^2 + \frac{1}{2\tau^2} \|w\|_2^2 + \text{const}.$$

Multiply by $2\sigma^2/n$: the MAP estimate minimizes $L_S(w) + \lambda \|w\|_2^2$ with squared loss and $\lambda = \sigma^2/(n\tau^2)$. With independent Laplace priors $p(w_j) = \frac{1}{2b} e^{-|w_j|/b}$ the same steps give $L_S(w) + \lambda \|w\|_1$ with $\lambda = 2\sigma^2/(nb)$. So $L_2$ is a Gaussian prior and $L_1$ is a Laplace prior. The MAP estimate is the mode of the posterior, not its mean; under the Laplace prior the posterior mean is never exactly sparse, while the mode is.

### Stability: why the penalty controls the gap

**Theorem (Tikhonov regularization is stable).** Let $\ell(\cdot, z)$ be convex and $\rho$-Lipschitz in $w$ for every $z$, and let $A(S)$ minimize $f_S(w) = L_S(w) + \lambda \|w\|_2^2$ with $\lambda > 0$. Let $S^{(i)}$ be $S$ with $z_i$ replaced by any $z'$. Then

$$\|A(S^{(i)}) - A(S)\| \le \frac{2\rho}{\lambda n}, \qquad \mathbb{E}_S\big[L_D(A(S)) - L_S(A(S))\big] \le \frac{2\rho^2}{\lambda n}.$$

*Proof.*

1. *Strong convexity.* Let $u = A(S)$. Since $u$ minimizes the convex $f_S$, some subgradient $g \in \partial L_S(u)$ has $g + 2\lambda u = 0$. For any $v$, convexity gives $L_S(v) \ge L_S(u) + g \cdot (v - u)$, and the identity $\|v\|^2 = \|u\|^2 + 2u \cdot (v - u) + \|v - u\|^2$ gives the penalty exactly. Adding, $f_S(v) \ge f_S(u) + (g + 2\lambda u) \cdot (v - u) + \lambda \|v - u\|^2 = f_S(u) + \lambda \|v - u\|^2$.
2. *Compare the two objectives.* Let $v = A(S^{(i)})$. Since $f_S(w) = f_{S^{(i)}}(w) + \frac1n (\ell(w, z_i) - \ell(w, z'))$,
$$f_S(v) - f_S(u) = \big(f_{S^{(i)}}(v) - f_{S^{(i)}}(u)\big) + \tfrac1n\big(\ell(v, z_i) - \ell(u, z_i)\big) + \tfrac1n\big(\ell(u, z') - \ell(v, z')\big).$$
The first bracket is at most 0, because $v$ minimizes $f_{S^{(i)}}$. The Lipschitz condition bounds each of the other two by $\frac{\rho}{n} \|v - u\|$.
3. *Combine.* Steps 1 and 2 give $\lambda \|v - u\|^2 \le \frac{2\rho}{n} \|v - u\|$, so $\|v - u\| \le \frac{2\rho}{\lambda n}$, and then $\ell(v, z_i) - \ell(u, z_i) \le \rho \|v - u\| \le \frac{2\rho^2}{\lambda n}$.
4. *Stable rules do not overfit.* Draw $z' \sim D$ independent of $S$ and $i$ uniform in $\{1, \ldots, n\}$. The pairs $(S, z')$ and $(S^{(i)}, z_i)$ have the same distribution, so $\mathbb{E}[L_D(A(S))] = \mathbb{E}[\ell(A(S), z')] = \mathbb{E}[\ell(A(S^{(i)}), z_i)]$. Also $\mathbb{E}[L_S(A(S))] = \mathbb{E}[\ell(A(S), z_i)]$. Subtracting, the expected gap is $\mathbb{E}[\ell(A(S^{(i)}), z_i) - \ell(A(S), z_i)] \le \frac{2\rho^2}{\lambda n}$ by step 3. $\blacksquare$

This is the argument of Shalev-Shwartz and Ben-David (Sections 13.2 and 13.3), in the line of Bousquet and Elisseeff (2002), who also prove high-probability bounds from uniform stability. It gives the *fitting-stability tradeoff*: for every fixed $w^\ast$, $\mathbb{E}[L_S(A(S))] \le \mathbb{E}[f_S(A(S))] \le \mathbb{E}[f_S(w^\ast)] = L_D(w^\ast) + \lambda\|w^\ast\|^2$, so

$$\mathbb{E}\big[L_D(A(S))\big] \le L_D(w^\ast) + \lambda \|w^\ast\|^2 + \frac{2\rho^2}{\lambda n}.$$

A large $\lambda$ costs fit; a small $\lambda$ costs stability. If $\|w^\ast\| \le B$, the choice $\lambda = \rho\sqrt{2}/(B\sqrt n)$ gives $L_D(w^\ast) + \rho B \sqrt{8/n}$.

### Early stopping as implicit regularization

Run gradient descent on the least squares risk $L_S(w) = \frac1n\|Xw - y\|^2$ from $w_0 = 0$ with step $\eta$. Let $\Sigma = X^\top X/n$ have eigenpairs $(s_j, u_j)$ and $c = X^\top y/n$. The update $w_{t+1} = w_t - 2\eta(\Sigma w_t - c)$ acts on each coordinate $a_j = u_j \cdot w$ separately, and solving the recursion gives

$$u_j \cdot w_t = \big(1 - (1 - 2\eta s_j)^t\big) \frac{u_j \cdot c}{s_j} \quad (s_j > 0), \qquad u_j \cdot w_t = 0 \quad (s_j = 0),$$

since $u_j \cdot c = 0$ when $Xu_j = 0$. Ridge regression with the same convention gives $u_j \cdot w_\lambda = \frac{s_j}{s_j + \lambda} \cdot \frac{u_j \cdot c}{s_j}$. Both shrink the directions of small $s_j$ the most. If $2\eta s_j \le 1$ for all $j$, each factor $1 - (1 - 2\eta s_j)^t$ rises with $t$, so $\|w_t\|$ never decreases and tends to the norm of the minimum norm least squares solution. Stopping at step $t$ acts like a penalty with $\lambda$ of order $1/(\eta t)$ (Goodfellow, Bengio and Courville, Section 7.8, make this precise for a quadratic loss). See [early stopping](/early-stopping/).

## Classic examples

- **[Ridge regression](/ridge-regression/).** Squared loss with $R = \|w\|_2^2$. The solution is $(X^\top X/n + \lambda I)^{-1} X^\top y/n$, unique for every $\lambda > 0$ even when $X^\top X$ is singular. Hoerl and Kennard (1970) showed that some $\lambda > 0$ gives a smaller mean squared error than least squares.
- **[Lasso](/lasso-regression/).** Squared loss with $R = \|w\|_1$ (Tibshirani 1996). Its solutions are sparse. With an orthonormal design the problem splits by coordinate into $\min_w \frac12 (w - z)^2 + a|w|$, solved by the soft threshold $\mathrm{sign}(z)\max(|z| - a, 0)$; the $L_2$ analogue $\min_w \frac12(w - z)^2 + \frac a2 w^2$ gives $z/(1 + a)$, which is never zero for $z \ne 0$.
- **[Support vector machine](/support-vector-machine/).** Hinge loss with $R = \|w\|_2^2$; the penalty is what maximizes the margin.
- **[Logistic regression](/logistic-regression/)** with an $L_2$ or $L_1$ penalty, which also makes the optimum finite on separable data.
- **[Kernel ridge regression](/kernel-ridge-regression/).** Tikhonov regularization in a reproducing kernel Hilbert space; the [representer theorem](/representer-theorem/) reduces it to $n$ coefficients.
- **[Cost-complexity pruning](/cost-complexity-pruning/)** of decision trees: the penalty is $\alpha$ times the number of leaves.
- **Neural networks:** [weight decay](/weight-decay/), [early stopping](/early-stopping/), [dropout](/dropout/) and [data augmentation](/data-augmentation/).

### A worked example

Take $n = 20$ examples in $\mathbb{R}^3$ with $x$ uniform on $[-1, 1]^3$, $y = w_{\mathrm{true}} \cdot x$ plus Gaussian noise of standard deviation 0.3, clipped to $[-2, 2]$, drawn with `random.Random(1)`. Ridge with $L_S(w) + \lambda\|w\|^2$:

| $\lambda$ | $w_\lambda$ | $\lVert w_\lambda \rVert$ | $L_S(w_\lambda)$ |
|---|---|---|---|
| 0 | (−0.6566, 0.6266, 0.6101) | 1.0936 | 0.0938 |
| 0.01 | (−0.6393, 0.6150, 0.5967) | 1.0691 | 0.0940 |
| 0.1 | (−0.5182, 0.5254, 0.4983) | 0.8905 | 0.1118 |
| 1 | (−0.1833, 0.2081, 0.1888) | 0.3354 | 0.3471 |
| 10 | (−0.0248, 0.0293, 0.0262) | 0.0465 | 0.5783 |

The norm falls and the training error rises with $\lambda$. Projected gradient descent on $\min L_S(w)$ subject to $\|w\| \le 0.8905$ returns $w_{0.1}$ to 8 decimals, and bisection on $\lambda$ for the radius $0.8905\ldots$ returns $\lambda = 0.1$, as Claims 1 and 2 say. Gradient descent from 0 with $\eta = 0.05$ has $\|w_t\| = 0.0485, 0.2219, 0.3985, 0.6507, 0.9769, 1.0797$ at $t = 1, 5, 10, 20, 50, 100$, rising to the least squares norm 1.0936; it passes the ridge norms of the table on the way. For $\lambda = 0.1$, replacing one of the 20 examples by a random one moved $w_\lambda$ by at most 0.260 over all 20 positions, below the bound $2\rho/(\lambda n) \approx 36.9$ that the theorem gives with the Lipschitz constant $\rho$ of the squared loss on the ball that holds both solutions. The bound is valid and loose.

## Variations

- **Elastic net** mixes $L_1$ and $L_2$, which keeps sparsity and groups correlated features.
- **General Tikhonov** $\|\Gamma w\|^2$ penalizes roughness instead of size, as in smoothing splines.
- **Spectral cutoff** (truncated SVD or principal component regression) sets the filter factors to 0 or 1 instead of $s/(s + \lambda)$.
- **Constraint form** (Ivanov) fixes $t$ instead of $\lambda$; some solvers and bounds prefer it.
- **Implicit regularization:** early stopping, the minimum norm bias of gradient descent, dropout, noise injection and data augmentation. Bishop (1995) showed that training with small input noise is close to a Tikhonov penalty; this page does not prove that.
- **Complexity penalties** that are not norms: the number of leaves, the description length ([minimum description length](/minimum-description-length/)), or a capacity bound ([structural risk minimization](/structural-risk-minimization/)).

## Pitfalls

- **Scaling.** The penalty $\|w\|$ is not invariant to the units of the features. Standardize the features first, or the penalty hits some features harder than others.
- **The intercept.** Penalizing $b$ makes the fit depend on the origin of $y$. Center the data, or leave $b$ out of $R$.
- **Choosing $\lambda$ on the test set.** Then the test error is no longer an honest estimate. Use a validation set or [cross-validation](/cross-validation/).
- **Conventions differ.** Some texts penalize the sum of losses, others the mean, some add a factor $\frac12$. The same $\lambda$ means different things; check the scaling before you copy a value.
- **$L_1$ solutions need not be unique** when features are collinear, because the objective is not strictly convex.
- **Weight decay is not always an $L_2$ penalty.** For plain gradient descent they are the same; for Adam they are not, which is the point of [AdamW](/adamw/).

## Exercises

1. Show that the ridge solution $(\Sigma + \lambda I)^{-1} c$ satisfies $\|w_\lambda\| \le \|c\|/\lambda$, and that $\|w_\lambda\|$ is non-increasing in $\lambda$.
2. Prove the soft threshold formula: for $a \ge 0$, the minimizer of $\frac12(w - z)^2 + a|w|$ is $\mathrm{sign}(z)\max(|z| - a, 0)$. Use the subgradient of $|w|$ at 0.
3. Find a non-convex $L_S$ and a $t$ for which a constrained minimizer is not a minimizer of $L_S + \lambda R$ for any $\lambda \ge 0$.
4. In the stability theorem, replace the Lipschitz assumption by "the loss is nonnegative and $\beta$-smooth" and follow Shalev-Shwartz and Ben-David (Section 13.3) to get a bound in terms of the expected training loss.

## References
