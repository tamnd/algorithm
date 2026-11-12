---
tag: 3V5V6X
kind: algorithm
slug: support-vector-machine
name: Support vector machine
aliases:
- SVM
- maximum margin classifier
- soft margin classifier
- support vector classifier
area: machine-learning/supervised-learning
level: core
summary: "A linear or kernel classifier that maximizes the margin 2/||w|| between the classes, with slack weighted by C. Trained by solving a convex dual QP; only the support vectors matter."
solves: [classification]
model: real-ram
complexity:
  vars: {n: the number of training points, t: the cost of one kernel evaluation, s: the number of solver iterations, n_sv: the number of support vectors}
  time: {worst: "O(n^2 t + s n)", best: "Θ(n^2 t)"}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1992
  people: [Bernhard E. Boser, Isabelle M. Guyon, Vladimir N. Vapnik, Corinna Cortes]
  note: Boser, Guyon and Vapnik combined the maximum margin hyperplane with kernels in 1992. Cortes and Vapnik added the soft margin with slack variables in 1995.
prereqs: [linear-separability, kkt-conditions, quadratic-programming, kernel-trick]
see_also: [svm-training, sequential-minimal-optimization, hinge-loss, margin-generalization-bound, support-vector-regression, perceptron, logistic-regression, representer-theorem]
sources:
  - paper: doi:10.1145/130385.130401
    title: Bernhard E. Boser, Isabelle M. Guyon and Vladimir N. Vapnik, A training algorithm for optimal margin classifiers, Proceedings of the Fifth Annual Workshop on Computational Learning Theory (COLT), 1992
    locator: pp. 144 to 152 (the maximum margin classifier, its dual, the support patterns and the use of kernels)
  - paper: doi:10.1007/BF00994018
    title: Corinna Cortes and Vladimir Vapnik, Support-vector networks, Machine Learning 20(3), 1995
    locator: pp. 273 to 297 (the soft margin with slack variables and the constant C, the dual problem, and experiments)
  - book: isbn:9780262194754
    title: Bernhard Schölkopf and Alexander J. Smola, Learning with Kernels, MIT Press, 2002
    locator: Chapter 7 (pattern recognition; the optimal margin hyperplane, the soft margin and the dual)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Chapter 15 (support vector machines; hard and soft SVM, the dual and the support vectors)
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Chapter 5 (support vector machines, the separable and non-separable cases, and margin theory)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Chapter 12 (support vector machines and flexible discriminants; the SVM as hinge loss with a ridge penalty)
---

A support vector machine (SVM) is a classifier $x \mapsto \operatorname{sign}(w \cdot \varphi(x) + b)$ whose hyperplane is chosen to leave the widest possible gap, the *margin* $2/\lVert w \rVert$, between the two classes. The soft margin version lets some points enter the gap or cross it, at a cost $C$ per unit of violation. Training is a convex quadratic program. Its dual uses the data only through a kernel $k(x_i, x_j)$, and its solution depends only on a few training points, the *support vectors*. Boser, Guyon and Vapnik introduced the kernel maximum margin classifier in 1992, and Cortes and Vapnik the soft margin in 1995.

## In plain words

Many lines can split two groups of points. The SVM picks the one that stays as far as possible from both groups: it is the middle of the widest empty street that you can draw between them. The points on the edges of the street hold it in place; they are the support vectors. Moving any other point a little does not change the answer.

Real data often has no empty street. Then the SVM allows some points inside the street or on the wrong side, and it pays a penalty for each. A number $C$ sets the price: a large $C$ gives a narrow street with few violations, and a small $C$ gives a wide street with more violations. With a kernel, the street is straight in a space of new features, and it looks curved in the original space.

## The problem

The input is a training set $(x_1, y_1), \ldots, (x_n, y_n)$ with $y_i \in \{-1, +1\}$, a positive semidefinite kernel $k$ with feature map $\varphi$ ([kernel trick](/kernel-trick/)), and $C > 0$. This is binary [classification](/classification/).

**Hard margin primal.** For [linearly separable](/linear-separability/) data,

$$\min_{w, b} \; \tfrac12 \lVert w \rVert^2 \quad \text{subject to } y_i (w \cdot \varphi(x_i) + b) \ge 1 \text{ for each } i.$$

The constraints say that every point is on its side with functional margin at least 1. The distance from the hyperplane to the plane $w \cdot \varphi(x) + b = \pm 1$ is $1/\lVert w \rVert$, so the width of the street is $2/\lVert w \rVert$, and minimizing $\lVert w \rVert$ maximizes it.

**Soft margin primal (Cortes and Vapnik).** For any data,

$$\min_{w, b, \xi} \; \tfrac12 \lVert w \rVert^2 + C \sum_i \xi_i \quad \text{subject to } y_i (w \cdot \varphi(x_i) + b) \ge 1 - \xi_i, \; \xi_i \ge 0.$$

At the optimum $\xi_i = \max(0, 1 - y_i f(x_i))$, so this is the [hinge loss](/hinge-loss/) plus a ridge penalty: $\min \tfrac12 \lVert w \rVert^2 + C \sum_i \max(0, 1 - y_i f(x_i))$.

**Dual.** With multipliers $\alpha_i \ge 0$ for the margin constraints, [Lagrangian duality](/lagrangian-duality/) gives

$$\max_\alpha \; \sum_i \alpha_i - \tfrac12 \sum_{i,j} \alpha_i \alpha_j y_i y_j k(x_i, x_j) \quad \text{subject to } 0 \le \alpha_i \le C, \; \sum_i \alpha_i y_i = 0.$$

The hard margin dual is the same with $C = \infty$. The constraints of the primal are affine, so [strong duality](/strong-duality/) holds, and $w = \sum_i \alpha_i y_i \varphi(x_i)$. The classifier is

$$f(x) = \sum_i \alpha_i y_i k(x_i, x) + b.$$

**KKT conditions.** At an optimum, for each $i$:

$$\alpha_i = 0 \Rightarrow y_i f(x_i) \ge 1, \qquad 0 < \alpha_i < C \Rightarrow y_i f(x_i) = 1, \qquad \alpha_i = C \Rightarrow y_i f(x_i) \le 1.$$

These come from stationarity ($w = \sum \alpha_i y_i \varphi(x_i)$, $\sum \alpha_i y_i = 0$, and $C - \alpha_i - \mu_i = 0$ for the multiplier $\mu_i$ of $\xi_i \ge 0$) and complementary slackness ($\alpha_i (y_i f(x_i) - 1 + \xi_i) = 0$, $\mu_i \xi_i = 0$). The *support vectors* are the points with $\alpha_i > 0$. The free ones, with $0 < \alpha_i < C$, lie exactly on the margin and fix $b = y_i - \sum_j \alpha_j y_j k(x_j, x_i)$. The bound ones, with $\alpha_i = C$, are inside the street or misclassified.

## The algorithm

```pseudo id=main
SVM-TRAIN(S, k, C)                                       ▷ S = ((x_1, y_1), ..., (x_n, y_n))
L1  K[i][j] ← k(x_i, x_j) for i, j ← 1 to n
L2  Q[i][j] ← y_i y_j K[i][j]
L3  α ← argmin ½ αᵀQα − Σ_i α_i subject to 0 ≤ α ≤ C, Σ_i α_i y_i = 0   ▷ a QP solver; here SMO type with WSS3
L4  SV ← {i : α_i > 0}
L5  b ← the mean of y_i − Σ_j α_j y_j K[j][i] over the free i (0 < α_i < C), or the middle of the feasible interval if none
L6  return (α, b, SV)

SVM-PREDICT(x)
L7  f ← Σ_{i ∈ SV} α_i y_i k(x_i, x) + b
L8  return +1 if f ≥ 0 else −1
```

Line L3 is the dual problem, in the minimization form. Any solver for this [quadratic program](/quadratic-programming/) works; see [SVM training](/svm-training/) for the choices. The implementation here uses an SMO type decomposition: at each step it picks the most violating index $i$, picks $j$ by the second order rule WSS3 of Fan, Chen and Lin (2005), and solves the two-variable subproblem in closed form, as in [sequential minimal optimization](/sequential-minimal-optimization/). It stops when the largest KKT violation is below a tolerance.

Line L5 uses the KKT conditions: a free support vector satisfies $y_i f(x_i) = 1$, so $b = y_i - \sum_j \alpha_j y_j K_{ji}$. Averaging over all free points reduces rounding error. If no point is free, every $b$ between the largest lower bound and the smallest upper bound from the KKT conditions is optimal, and the middle is taken.

Line L7 sums only over the support vectors, which is what makes the SVM sparse at prediction time.

## Example

Take the linearly separable points $(2, 0)$, $(0, 2)$, $(3, 3)$ with $y = +1$ and $(-1, 0)$, $(0, -1)$, $(-2, -2)$ with $y = -1$, and the linear kernel.

**Hard margin** ($C = 10^6$, so no $\alpha_i$ reaches $C$). The solver returns $w = (2/3, 2/3)$ and $b = -1/3$, so $f(x) = \tfrac23 (x_1 + x_2) - \tfrac13$. The points $(2, 0)$ and $(0, 2)$ have $f = 1$, and $(-1, 0)$ and $(0, -1)$ have $f = -1$: they lie on the edges of the street. The other two points are farther away. The margin is $2/\lVert w \rVert = 2/(2\sqrt2/3) = 3/\sqrt2 \approx 2.121$, which is the distance between the parallel lines $x_1 + x_2 = 2$ and $x_1 + x_2 = -1$. The multipliers are $\alpha \approx (\tfrac13, \tfrac19, 0, 0, \tfrac49, 0)$: they satisfy $\sum_i \alpha_i y_i = \tfrac13 + \tfrac19 - \tfrac49 = 0$ and $\sum_i \alpha_i y_i x_i = w$. The dual value is $\sum \alpha_i - \tfrac12 \lVert w \rVert^2 = \tfrac89 - \tfrac49 = \tfrac49 = \tfrac12 \lVert w \rVert^2$, the primal value. Only three of the four margin points have $\alpha_i > 0$; the optimal $\alpha$ is not unique here, though $w$ and $b$ are.

**Soft margin** ($C = 0.1$). Now all four margin points reach $\alpha_i = C = 0.1$, and the solution is $w = (0.3, 0.3)$, $b = -0.25$. The street is wider, $2/\lVert w \rVert \approx 4.71$, and four points are inside it, with slacks $0.65, 0.65, 0.45, 0.45$. The primal value is $\tfrac12 \cdot 0.18 + 0.1 \cdot 2.2 = 0.31$, equal to the dual value $0.4 - 0.09 = 0.31$.

**XOR.** On $(0, 0), (1, 1)$ labelled $-1$ and $(0, 1), (1, 0)$ labelled $+1$, a linear SVM must misclassify a point. With the Gaussian kernel $\exp(-\lVert x - z \rVert^2 / (2 \cdot 0.7^2))$ and $C = 10$, it classifies all four correctly, and all four are support vectors.

## Correctness

The primal is a convex QP. When it is feasible, which the soft margin version always is, a minimizer exists, because the objective is coercive in $w$ and $\xi$. The constraints are affine, so Slater's condition is not needed: strong duality holds and the KKT conditions are necessary and sufficient. A dual optimum $\alpha$ gives the primal optimum $w = \sum_i \alpha_i y_i \varphi(x_i)$, and the $b$ of line L5 satisfies the KKT conditions with it. The solver of line L3 stops when the largest violation is below its tolerance, so the result is optimal within that tolerance. The proofs folder derives the dual and the KKT conditions, proves that $w$ is unique, and shows that the hard margin solution is the maximum margin hyperplane.

The tests check, on 60 problems with a linear and a Gaussian kernel and $C \in \{0.1, 1, 10\}$, that $0 \le \alpha_i \le C$, that the KKT conditions hold within $10^{-5}$, and that the duality gap between the primal and the dual value is below $10^{-4}$ relative.

## Complexity

- **Training.** Computing $K$ costs $\Theta(n^2 t)$ and $\Theta(n^2)$ memory. An SMO type solver costs $O(n)$ per iteration with $K$ in memory, so the total is $O(n^2 t + s n)$ for $s$ iterations. The number of iterations depends on the data and grows with $C$; in practice training takes between about $n^2$ and $n^3$ operations. A general interior point QP solver costs $O(n^3)$ per iteration.
- **Prediction.** $O(n_{sv} t)$ per point, where $n_{sv}$ is the number of support vectors. For a linear kernel, keep $w$ and pay $O(d)$.
- **Linear SVMs.** Without a kernel, dual coordinate descent and Pegasos train in time close to linear in the number of nonzero features; see [SVM training](/svm-training/).

## Properties

- **Convex.** There are no local minima. The weight vector $w$ is unique because $\tfrac12 \lVert w \rVert^2$ is strictly convex; $b$ is unique when some $\alpha_i$ is free.
- **Sparse.** Only the support vectors enter the classifier. Every margin error, a point with $y_i f(x_i) < 1$, has $\alpha_i = C$, so the number of support vectors is at least the number of margin errors.
- **Leave-one-out bound.** Removing a point that is not a support vector does not change the solution, so the leave-one-out error is at most $n_{sv}/n$.
- **Margin based generalization.** The bounds of the [margin generalization bound](/margin-generalization-bound/) depend on $R/\gamma$, not on the dimension of the feature space, which explains why the SVM works with infinite dimensional kernels.
- **No probabilities.** The output $f(x)$ is a score, not a probability. Platt scaling fits a sigmoid to it after training.
- **Hinge loss with a ridge penalty.** The soft margin SVM is regularized empirical risk minimization with the hinge loss and $\lambda = 1/C$ (up to scaling).

## Variants and improvements

- **ν-SVM.** It replaces $C$ by $\nu \in (0, 1]$, an upper bound on the fraction of margin errors and a lower bound on the fraction of support vectors.
- **Squared hinge (L2-SVM).** It uses $C \sum_i \xi_i^2$, which makes the dual box constraints disappear and the objective smooth.
- **Multiclass.** One-versus-rest and one-versus-one combine binary SVMs; Crammer and Singer give a single joint problem.
- **[Support vector regression](/support-vector-regression/).** It uses the ε-insensitive loss for real targets.
- **One-class SVM.** It separates the data from the origin to estimate the support of a distribution.
- **Structured SVMs.** They extend the margin to outputs such as sequences and trees.

## When to use it

Use an SVM for classification with up to a few hundred thousand points, when a good kernel is known, or with a linear kernel for high-dimensional sparse data such as text. It is strong when the number of features is large compared with the number of points. For very large data or when probabilities are needed, consider [logistic regression](/logistic-regression/) or a linear SVM trained by stochastic methods.

## Pitfalls

- **Unscaled features.** The margin is measured in the Euclidean norm, so a feature with a large range dominates. Standardize first.
- **Choosing $C$ and the kernel width.** Both need cross-validation, usually on a logarithmic grid. A small Gaussian width with a large $C$ memorizes the training set.
- **Unbalanced classes.** One $C$ for both classes favors the larger one. Use class weights $C_+$ and $C_-$.
- **Reading $\alpha$.** The optimal $\alpha$ need not be unique, as in the example. Interpret $w$, $f$ and the margin, not single multipliers.
- **The bias with no free support vector.** If every $\alpha_i$ is 0 or $C$, $b$ lies in an interval. Take the middle, not the value from one point.
- **Non-PSD kernels.** A function such as $\tanh(a\, x \cdot z + c)$ is not positive semidefinite for all parameters, and then the dual is not convex.

## Implementations

## History

Vapnik and Chervonenkis studied the optimal separating hyperplane in the 1960s and 1970s. Boser, Guyon and Vapnik (1992) combined it with kernels, following the potential functions of Aizerman, Braverman and Rozonoer (1964), and trained it through its dual. Cortes and Vapnik (1995) added slack variables for data that is not separable and named the method support-vector networks. Fast solvers followed: decomposition by Osuna, Freund and Girosi (1997), SMO by Platt (1998), SVMlight by Joachims, and LIBSVM by Chang and Lin.

## References
