---
tag: JKAB4E
kind: algorithm
slug: sparse-pca
name: Sparse PCA
aliases:
- sparse principal component analysis
- cardinality-constrained PCA
- truncated power method for sparse PCA
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Find a direction of large variance that uses at most k of the d variables. The problem is NP-hard; the truncated power method is a fast ascent method for it."
model: real-ram
complexity:
  vars: {d: the number of variables, k: the number of nonzero loadings, T: the number of iterations}
  time: {worst: "O(T d^2)", per_step: "O(d^2)"}
  space: {extra: "O(d)"}
properties: {deterministic: true, exact: false, iterative: true, online: false, recursive: false}
history:
  year: 2006
  people: [Hui Zou, Trevor Hastie, Robert Tibshirani]
  note: "Jolliffe, Trendafilov and Uddin (2003) put an l1 bound on the loadings (SCoTLASS). Zou, Hastie and Tibshirani (2006) wrote sparse PCA as an elastic net regression. d'Aspremont et al. (2007) gave a semidefinite relaxation, and Yuan and Zhang (2013) the truncated power method."
prereqs: [principal-component-analysis, power-iteration, covariance-matrix]
see_also: [lasso-regression, elastic-net, semidefinite-programming, maximum-clique, planted-clique, explained-variance, nonnegative-matrix-factorization, robust-pca]
sources:
  - paper: doi:10.1198/106186006X113430
    title: Hui Zou, Trevor Hastie and Robert Tibshirani, Sparse principal component analysis, Journal of Computational and Graphical Statistics 15(2), 265-286, 2006
    locator: PCA as a ridge regression problem, the SPCA criterion with elastic net penalties, and the alternating algorithm of elastic net fits and a Procrustes (SVD) step
  - paper: doi:10.1137/050645506
    title: "Alexandre d'Aspremont, Laurent El Ghaoui, Michael I. Jordan and Gert R. G. Lanckriet, A direct formulation for sparse PCA using semidefinite programming, SIAM Review 49(3), 434-448, 2007"
    locator: the semidefinite relaxation max Tr(AX) - rho 1^T |X| 1 subject to Tr X = 1, X positive semidefinite
  - paper: "Xiao-Tong Yuan and Tong Zhang, Truncated power method for sparse eigenvalue problems, Journal of Machine Learning Research 14, 899-925, 2013"
    title: Yuan and Zhang 2013
    locator: Algorithm 1 (TPower), the monotone ascent of the objective for positive semidefinite A, and the recovery bound for a sparse leading eigenvector under a perturbation model
  - paper: "Baback Moghaddam, Yair Weiss and Shai Avidan, Spectral bounds for sparse PCA, exact and greedy algorithms, Advances in Neural Information Processing Systems 18, 915-922, 2006"
    title: Moghaddam, Weiss and Avidan 2006
    locator: the cardinality-constrained problem as the largest eigenvalue over principal submatrices, its NP-hardness, the eigenvalue interlacing bounds, the greedy search and the exact branch and bound
  - paper: doi:10.1109/TIT.2013.2290112
    title: Andreas M. Tillmann and Marc E. Pfetsch, The computational complexity of the restricted isometry property, the nullspace property, and related concepts in compressed sensing, IEEE Transactions on Information Theory 60(2), 1248-1259, 2014
    locator: NP-hardness of computing restricted isometry constants, which are sparse extreme eigenvalues of a Gram matrix
  - paper: doi:10.1198/1061860032148
    title: Ian T. Jolliffe, Nickolay T. Trendafilov and Mudassir Uddin, A modified principal component technique based on the LASSO, Journal of Computational and Graphical Statistics 12(3), 531-547, 2003
    locator: SCoTLASS, PCA with an l1 bound on the loading vector
---

Sparse PCA looks for a direction of large variance whose loading vector has few nonzero entries, so each component depends on only a few variables and is easier to read. For a covariance matrix $A$ and a number $k$, the problem is to maximize $x^T A x$ over unit vectors $x$ with at most $k$ nonzero entries. It is NP-hard. The truncated power method of Yuan and Zhang (2013) is a simple and fast ascent method for it: multiply by $A$, keep the $k$ largest entries in absolute value, normalize, and repeat. For a positive semidefinite $A$ the variance never decreases. Other approaches are the elastic net formulation of Zou, Hastie and Tibshirani (2006) and the semidefinite relaxation of d'Aspremont et al. (2007).

## In plain words

Ordinary [PCA](/principal-component-analysis/) gives directions that mix all the variables. With a thousand genes, a component that uses all thousand of them with small weights is hard to explain. Sparse PCA asks for a direction that uses only a few variables but still catches much of the spread.

The truncated power method is the [power iteration](/power-iteration/) with one extra step. The power iteration multiplies a vector by the covariance matrix again and again, and the vector turns toward the direction of largest spread. The truncated version, after each multiplication, keeps only the $k$ biggest entries and sets the rest to zero. So the vector always uses at most $k$ variables, and it moves toward the best spread that such a vector can catch. The answer can depend on the start, because the method can stop at a choice of variables that is good but not the best.

## The problem

**Input.** A symmetric positive semidefinite $d \times d$ matrix $A$, usually the [covariance matrix](/covariance-matrix/) of the data, and a cardinality $k$ with $1 \le k \le d$.

**Output.** A unit vector $x$ with $\|x\|_0 \le k$ that makes $x^T A x$ large. The exact problem is

$$\max_x \; x^T A x \quad \text{subject to} \quad \|x\|_2 = 1,\; \|x\|_0 \le k .$$

Its value is $\max_{|S| = k} \lambda_{\max}(A_{SS})$, the largest top eigenvalue over all $k \times k$ principal submatrices: for a fixed support $S$ the best $x$ is the top eigenvector of $A_{SS}$. For $k = d$ this is ordinary PCA. More components are found one by one with deflation.

## The algorithm

```pseudo id=main
TRUNCATED-POWER(A, k, x₀)
L1  x ← trunc_k(x₀) / ‖trunc_k(x₀)‖               ▷ a k-sparse unit start
L2  repeat
L3      y ← A x
L4      F ← the indices of the k entries of y with largest |y_i|
L5      x' ← y restricted to F, divided by its norm
L6      stop ← ‖x' − x‖ < tol
L7      x ← x'
L8  until stop;  return x, xᵀ A x
```

The truncation in L4 and L5 is the projection on the set of $k$-sparse unit vectors: among them, $x'$ is the one with the largest inner product with $y$. Yuan and Zhang analyze this exact iteration (their Algorithm 1). The start matters. The implementation offers the unit vector on the largest diagonal entry, and a version that tries every coordinate vector $e_i$ and keeps the best result.

**Several components.** After a component $x$ is found, replace $A$ by the projection deflation $(I - x x^T) A (I - x x^T)$, which removes the variance along $x$, and run the method again. Unlike in ordinary PCA, the sparse components found this way are in general not orthogonal.

## Example

Take the eight points of the [PCA](/principal-component-analysis/) page. Their covariance is

$$A = \begin{pmatrix} 29 & 22 & 4 \\ 22 & 44 & 26 \\ 4 & 26 & 53 \end{pmatrix},$$

with the top eigenvalue $81$ for the dense direction $(1, 2, 2)/3$. Ask for $k = 2$. The three supports give

| support | $\lambda_{\max}(A_{SS})$ |
|---|---|
| $\{1, 2\}$ | $(73 + \sqrt{2161})/2 = 59.7433$ |
| $\{1, 3\}$ | $(82 + \sqrt{640})/2 = 53.6491$ |
| $\{2, 3\}$ | $(97 + \sqrt{2785})/2 = 74.8865$ |

So the best 2-sparse direction is $(0, 0.6440, 0.7650)$. It explains $74.8865 / 126 = 59.4\%$ of the total variance $126$, against $81/126 = 64.3\%$ for the dense first component.

Start the truncated power method at $e_3$, the largest diagonal entry. Then $A e_3 = (4, 26, 53)$, the truncation keeps $\{2, 3\}$, and the values $x^T A x$ are $53, 71.8155, 74.6037, 74.8618, 74.8844, \ldots$, which reach $74.8865$, the optimum.

Start instead at $e_1$. Then $A e_1 = (29, 22, 4)$, the truncation keeps $\{1, 2\}$, and the values are $29, 55.6657, 59.5242, 59.7324, \ldots$, which reach $59.7433$. At $x = (0.5819, 0.8132, 0)$ the product $A x = (34.76, 48.58, 23.47)$ again has its two largest entries in places 1 and 2, so this is a fixed point, but not the optimum. The method is an ascent method, not a global one.

With deflation, the second component is $(0.8924, 0.4512, 0)$ with variance $34.5132$ in the deflated matrix. Its inner product with the first component is $0.29$, so the two sparse components are not orthogonal.

## Correctness

The proofs file proves three facts.

- **Ascent.** If $A$ is positive semidefinite, the value $x^T A x$ never decreases from one iteration to the next. The reason is that $f(x) = x^T A x$ is convex, so $f(x') \ge f(x) + 2 (Ax)^T (x' - x)$, and L4 and L5 choose $x'$ to maximize $(Ax)^T x'$ over the $k$-sparse unit vectors, which include $x$. The values are bounded by $\lambda_{\max}(A)$, so they converge.
- **Fixed points.** If $x$ does not change, then on its support $F$ it is an eigenvector of $A_{FF}$ with the eigenvalue $x^T A x$. For $k = d$ the method is the power iteration and finds the top eigenvalue.
- **Hardness.** The decision version of the problem is NP-hard, by a reduction from [maximum clique](/maximum-clique/): for a graph with adjacency matrix $W$ and maximum degree $\Delta$, the matrix $W + \max(\Delta, 1) I$ is positive semidefinite, and its best $k$-sparse value is $k - 1 + \max(\Delta, 1)$ exactly when the graph has a clique of $k$ vertices. Moghaddam, Weiss and Avidan (2006) state the NP-hardness, and Tillmann and Pfetsch (2014) prove it for the closely related restricted isometry constants.

So no polynomial-time method solves every instance unless P = NP. Yuan and Zhang give a guarantee for a statistical model instead: if $A$ is a small perturbation of a matrix whose top eigenvector is $\bar k$-sparse, with $k \ge \bar k$, and the start is close enough to that vector, then the iterates approach it at a geometric rate up to an error set by the perturbation restricted to sparse vectors.

## Complexity

In the real RAM, one iteration costs $O(d^2)$ for the product $Ax$ with a dense $A$, and $O(d)$ for the truncation with a linear-time selection (the implementation sorts, $O(d \log d)$). So $T$ iterations cost $O(T d^2)$ and $O(d)$ extra memory. When $A = X_c^T X_c / n$ is not formed, $Ax$ costs $O(n k + n d)$ through $X_c x$, which uses only $k$ columns, and $X_c^T (X_c x)$. Forming $A$ costs $O(n d^2)$ once. The exact method by brute force tries $\binom{d}{k}$ supports, each with an eigenvalue problem of size $k$, so $O(\binom{d}{k} k^3)$; this is practical only for small $d$ or with branch and bound.

## Properties

- **Sparse by construction.** Every iterate has at most $k$ nonzero entries, so the cardinality is exact; there is no penalty to tune.
- **Monotone.** For positive semidefinite $A$ the objective never decreases.
- **Local.** The result depends on the start, and it can be a fixed point that is not optimal.
- **Cheap.** Each iteration costs one matrix-vector product and a selection, like the power iteration.
- **Non-orthogonal components.** Several components found with deflation are not orthogonal in general, and their variances do not add up to explained variance in the usual way.

## Variants and improvements

- **SPCA by elastic net** (Zou, Hastie and Tibshirani 2006). Write PCA as a regression of the data on themselves, then add [lasso](/lasso-regression/) and ridge penalties on the loadings, as in the [elastic net](/elastic-net/). Alternate between elastic net fits for the loadings and an SVD (Procrustes) step for the other factor. The sparsity comes from an $\ell_1$ penalty instead of an exact count.
- **SCoTLASS** (Jolliffe, Trendafilov and Uddin 2003) maximizes the variance under the constraint $\|x\|_1 \le t$, a nonconvex problem.
- **Semidefinite relaxation (DSPCA)** of d'Aspremont et al. (2007): lift $x x^T$ to a matrix $X$ and solve the [semidefinite program](/semidefinite-programming/) $\max \operatorname{Tr}(AX) - \rho\, \mathbf{1}^T |X| \mathbf{1}$ subject to $\operatorname{Tr} X = 1$, $X \succeq 0$. Its value is an upper bound that can certify that a sparse solution is optimal, at a much higher cost.
- **Greedy and exact search** (Moghaddam, Weiss and Avidan 2006). Add or remove one variable at a time and use eigenvalue interlacing to bound the best value, which gives a branch and bound for the exact optimum.
- **Generalized power method** (Journée, Nesterov, Richtárik and Sepulchre 2010) solves penalized versions with a similar iteration on the data matrix.
- **Thresholding** the ordinary PCA loadings is the simplest heuristic, but it can choose a poor support when variables are correlated.

## When to use it

Use sparse PCA when the components must be explained in terms of few variables, as with genes, words or sensors, or when the data follow a model with a sparse leading direction, where it is also more accurate than PCA in high dimension. Use the truncated power method when you know the cardinality $k$ and want a fast method; run it from several starts, for example from the coordinate vectors of the largest diagonal entries or from the truncated PCA direction, and keep the best. Use the elastic net or penalized forms when a penalty is more natural than a count, and the semidefinite relaxation when a certificate of optimality is needed for small $d$.

## Pitfalls

- **One start only.** As the example shows, a bad start gives a local fixed point. Use several starts.
- **An indefinite matrix.** The ascent proof needs $A \succeq 0$. For an indefinite matrix, add a multiple of $I$ first; this does not change the optimal $x$.
- **Variables on different scales.** The variable with the largest variance dominates the support. Standardize the variables first when the units differ, as for PCA on correlations.
- **Reading explained variance.** Sparse components are not orthogonal and their scores are correlated, so adding up their variances overstates the total variance explained. Use an adjusted measure, such as the variance of the projection on the span of the components.
- **Choosing $k$.** There is no rule like the [scree plot](/scree-plot/) for $k$. Plot the explained variance against $k$, or use cross-validation.
- **The hidden statistical limit.** Detecting a sparse spike in high dimension near the information limit is believed to be hard on average for all efficient methods, through the [planted clique](/planted-clique/) conjecture (Berthet and Rigollet). Good starts are not always available.

## Implementations

## History

Rotations of principal components to simple structure, in the spirit of [factor analysis](/factor-analysis/), were long the practical way to read components. Cadima and Jolliffe (1995) showed that simply thresholding the loadings can mislead. Jolliffe, Trendafilov and Uddin (2003) introduced SCoTLASS, PCA with an $\ell_1$ bound, after the lasso. Zou, Hastie and Tibshirani (2006) gave the elastic net formulation SPCA, which became widely used. d'Aspremont, El Ghaoui, Jordan and Lanckriet (2004 conference, 2007 journal) gave the semidefinite relaxation. Moghaddam, Weiss and Avidan (2006) studied the exact cardinality problem with spectral bounds and noted its NP-hardness. Journée et al. (2010) and Yuan and Zhang (2013) gave power-type methods; the truncated power method is among the simplest, and it comes with a recovery guarantee. Berthet and Rigollet (2013) linked the detection of sparse components to the planted clique problem.

## References
