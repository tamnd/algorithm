---
tag: ZY48RG
kind: algorithm
slug: square-root-sam
name: Square root smoothing and mapping
aliases:
- square root SAM
area: robotics/localization-and-slam
level: advanced
summary: The full SLAM method of Dellaert and Kaess. It factors the sparse measurement Jacobian by QR or Cholesky in a fill-reducing variable order and solves by back substitution.
solves: [full-slam]
model: real-ram
complexity:
  vars: {p: the number of poses, m: the number of landmarks, k: the number of scalar measurement rows, n: the number of scalar unknowns, c: the number of nonzero entries of R, I: the number of Gauss-Newton iterations}
  time: {linearize: O(k), factor_worst: O(k n^2), solve: O(c), total_worst: O(I k n^2)}
  space: {jacobian: O(k), factor: O(c)}
properties: {deterministic: true, exact: false, batch: true, cost_depends_on_ordering: true}
history:
  year: 2006
  people: [Frank Dellaert, Michael Kaess]
  note: Dellaert and Kaess solved full SLAM by a sparse QR or Cholesky factorization of the measurement Jacobian, and showed that a good column order keeps the factor sparse.
prereqs: [full-slam, qr-decomposition, elimination-ordering, least-squares-problem]
see_also: [graphslam, isam, isam2, givens-rotations, cholesky-decomposition, minimum-degree-ordering, nested-dissection, factor-graph]
sources:
  - paper: doi:10.1177/0278364906072768
    title: "Frank Dellaert and Michael Kaess, Square Root SAM: simultaneous localization and mapping via square root information smoothing, International Journal of Robotics Research 25(12), 2006, pages 1181 to 1203"
    locator: "the linearized least squares problem, its QR and Cholesky factorizations, and the effect of the variable ordering on the fill-in"
  - paper: doi:10.1561/2300000043
    title: "Frank Dellaert and Michael Kaess, Factor graphs for robot perception, Foundations and Trends in Robotics 6(1-2), 2017"
    locator: "the factor graph view of SLAM, elimination, and the link between the variable order and the sparsity of the square root information matrix"
  - book: isbn:9780898716139
    title: "Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006"
    locator: "the chapters on sparse orthogonal methods and on fill-reducing orderings"
---

Square root smoothing and mapping (square root SAM) solves the [full SLAM problem](/full-slam/) as a sparse [least squares problem](/least-squares-problem/). At each [Gauss-Newton](/gauss-newton-algorithm/) step, it builds the whitened Jacobian $A$ of all measurements, factors it as $A = Q R$ by a [QR decomposition](/qr-decomposition/), or factors $A^\top A = R^\top R$ by a [Cholesky decomposition](/cholesky-decomposition/), and solves $R\,\delta = d$ by back substitution. The factor $R$ is the square root of the information matrix, hence the name. Dellaert and Kaess (2006) showed that the work and the fill-in of $R$ depend on the order of the columns, and that a fill-reducing [elimination ordering](/elimination-ordering/) keeps $R$ sparse. Unlike [GraphSLAM](/graphslam/), which always removes the landmarks first, square root SAM lets the ordering choose, and it never forms the inverse.

## In plain words

All the measurements form one large system of equations with more equations than unknowns. Each equation touches only a pose and a landmark, or two poses. The method rewrites the system into a staircase shape, where the last unknown can be found alone, then the one before it, and so on back to the first. The rewrite keeps all the information. The order in which the unknowns are placed decides how many new entries the staircase gets. A good order keeps the staircase almost as empty as the original system, and so the work stays small. A bad order can fill it almost completely.

## The problem

The variables are $\theta = (x_0, \dots, x_T, m_1, \dots, m_M)$, with planar poses and point landmarks. Each factor $f$ has a measurement $z_f$, a model $h_f$ and a Gaussian noise with covariance $\Sigma_f$. The cost is

$$J(\theta) = \sum_f \|h_f(\theta) - z_f\|^2_{\Sigma_f}, \qquad \|e\|^2_\Sigma = e^\top \Sigma^{-1} e.$$

Linearize at the estimate $\theta$, with the Jacobian $H_f$ of $h_f$, and whiten each factor by $\Sigma_f^{-1/2}$. The step $\delta$ minimizes

$$\|A\delta - b\|^2, \qquad A = \begin{bmatrix} \vdots \\ \Sigma_f^{-1/2} H_f \\ \vdots \end{bmatrix}, \quad b = \begin{bmatrix} \vdots \\ -\Sigma_f^{-1/2}(h_f(\theta) - z_f) \\ \vdots \end{bmatrix}.$$

The code has a prior on $x_0$, odometry factors that measure the pose $x_{t}$ in the frame of $x_{t-1}$, and range and bearing factors. The noise is diagonal, so whitening divides each row by its standard deviation. Poses are updated by adding $\delta$ to $(x, y, \theta)$ and wrapping the angle.

## The algorithm

```pseudo id=main
SQRT-SAM(factors, θ)
L1  π ← a fill-reducing order of the variables (block minimum degree)
L2  repeat
L3      A, b ← the whitened Jacobian and right side at θ, with the columns in the order π
L4      R, d ← GIVENS-QR(A, b)
L5      δ ← the solution of R δ = d by back substitution
L6      θ ← θ ⊕ δ
L7  until max |δ| < tol
L8  return θ, R
GIVENS-QR(A, b)
L9  R ← no rows
L10 for each row a of [A | b] do
L11     while a has a nonzero entry in A; let c be its first column do
L12         if R has no row with the pivot c then store a as that row; next row
L13         rotate the row of R with the pivot c and a by a Givens rotation that sets a_c to 0
L14 return R and its right side column d
```

Line L13 uses a [Givens rotation](/givens-rotations/). A row that becomes zero leaves its right side behind, which is a part of the final residual. Lines L9 to L14 are the row by row form that [iSAM](/isam/) also uses to add new rows. A batch code would use a multifrontal QR or a sparse Cholesky of $A^\top A$; the result is the same $R$ up to the signs of its rows. The code computes the Cholesky form too, as a check.

**The ordering.** Line L1 orders the variables, not the scalar columns, because the columns of one variable are always dense together. Block minimum degree takes the graph whose vertices are the variables and whose edges join two variables that share a factor. It removes a variable with the fewest scalar neighbors, joins all its neighbors into a clique, and repeats. This is [minimum degree ordering](/minimum-degree-ordering/) on the variable graph. Dellaert and Kaess used COLAMD, an approximate minimum degree order for the columns of $A$. [Nested dissection](/nested-dissection/) is the other common choice. Finding an order with the least fill is [NP-hard](/np-hard/) (Yannakakis 1981), so all of these are heuristics.

## Example

The robot drives 12 steps of 1 m with a turn of $30°$ after each, a closed polygon of radius $1.93$ m, among 6 landmarks, and measures each landmark within 3 m. The noise is $0.02$ m and $0.01$ rad on the odometry, and $0.05$ m and $0.02$ rad on range and bearing. With the seed 4 there are 1 prior, 12 odometry factors and 40 range and bearing factors. $A$ has 119 rows, 51 columns ($13 \times 3 + 6 \times 2$) and 503 nonzero entries. A full upper triangle of size 51 has 1326 entries.

| column order | nonzero entries of $R$ | Givens rotations |
|---|---|---|
| block minimum degree | 573 | 1636 |
| natural: $x_0, \dots, x_{12}$, then $l_0, \dots, l_5$ | 653 | 2729 |
| landmarks first, then the poses | 1038 | 2701 |

The landmarks-first order is the order of [GraphSLAM](/graphslam/): after the landmarks, the pose block of $R$ is almost full. The minimum degree order starts with the poses $x_9, x_{10}, x_0, x_1, x_{12}, x_{11}$, which see few landmarks, and ends with four landmarks. All three orders give the same solution to $10^{-8}$.

Gauss-Newton from dead reckoning took 7 iterations. The largest step was $0.228$, then $7.5 \times 10^{-3}$, $1.2 \times 10^{-4}$, $2.9 \times 10^{-6}$ and $2.6 \times 10^{-8}$. The cost $J$ went from 549.57 to 66.20. The error of the last position went from 0.239 m (dead reckoning) to 0.054 m, and every landmark is within 0.062 m of the truth.

## Correctness

The [correctness proof](proofs/correctness.md) shows that the row by row Givens rotations build an upper triangular $R$ with $Q^\top [A \mid b] = \begin{bmatrix} R & d \\ 0 & e \end{bmatrix}$ for an orthogonal $Q$. Then $\|A\delta - b\|^2 = \|R\delta - d\|^2 + \|e\|^2$, so back substitution gives the unique least squares step when $A$ has full column rank. It also shows that a permutation of the columns permutes the step and changes nothing else, so the order affects only the cost. A fixed point of the loop has a zero gradient. The tests check $R$ against a Cholesky factor of $A^\top A$, check the step against the normal equations, check three orders against each other, and check that the gradient at the noisy solution is below $10^{-6}$.

## Complexity

Let $k$ be the number of scalar rows, $n$ the number of scalar unknowns ($3p + 2m$ in the plane) and $c$ the number of nonzero entries of $R$.

- Linearize: $O(k)$, because each row has a bounded number of entries.
- Factor: the cost depends on the variable ordering and the fill-in. A dense QR would cost $O(k n^2)$, which is the worst case. With a good [ordering](/elimination-ordering/) on typical SLAM graphs, the cost is far smaller; in the example, minimum degree used 1636 rotations instead of 2701 for the landmarks-first order.
- Solve: $O(c)$ for the back substitution.
- Memory: $O(k)$ for $A$ and $O(c)$ for $R$.

No useful bound on $c$ holds for all graphs. For planar graphs, nested dissection gives $c = O(n \log n)$ for the Cholesky factor (Lipton, Rose and Tarjan); a SLAM graph with long loops and landmarks seen from far is not planar in general. The number of iterations is measured, not bounded.

## Properties

- **No inverse.** It never forms $\Sigma$ or $\Omega^{-1}$. Marginal covariances, if needed, come from $R$ by a separate recursion.
- **Numerically stable.** QR works on $A$, not on $A^\top A$, so the condition number is not squared. The Cholesky form is faster and works well when the problem is well conditioned.
- **Batch.** Each iteration factors from the start. [iSAM](/isam/) adds rows to $R$ instead, and [iSAM2](/isam2/) keeps $R$ as a [Bayes tree](/bayes-tree/).
- **The same graph as a factor graph.** $A$ is the matrix of the [factor graph](/factor-graph/), and the factorization is [variable elimination](/variable-elimination/) in the chosen order.

## Variants and improvements

- **Cholesky instead of QR.** Factor $A^\top A$ with a sparse Cholesky. It does less work than QR, because it does not touch the rows of $A$ twice, but it squares the condition number. Dellaert and Kaess compare both forms.
- **Levenberg-Marquardt or dogleg.** Replace the plain Gauss-Newton step by [Levenberg-Marquardt](/levenberg-marquardt/) or [Powell's dogleg](/powell-dogleg/) when the start is poor.
- **Incremental.** [iSAM](/isam/) updates $R$ with Givens rotations as new rows arrive, and [iSAM2](/isam2/) updates only a part of a Bayes tree.
- **Constrained orders.** For an online system, put the newest variables last, so that new rows touch only the end of $R$.

## When to use it

Use square root SAM for batch full SLAM when the problem fits in memory, the data association is fixed, and a good initial guess exists. For a robot that must keep its estimate current as it drives, use [iSAM2](/isam2/). For a certificate of global optimality on pose graphs, use [SE-Sync](/se-sync/).

## Pitfalls

- **A missing prior.** Without a prior or an anchor, $A$ does not have full column rank, and the factorization meets a zero pivot. The code raises an error.
- **A bad ordering.** A natural or landmarks-first order can fill $R$. In larger problems the difference becomes orders of magnitude.
- **Unwrapped angle residuals.** Wrap every angle error to $[-\pi, \pi)$ before whitening.
- **Rank loss by geometry.** A landmark seen once by a bearing only sensor, or seen along one line, makes $A$ rank deficient in that direction.

## Implementations

## History

Dellaert (2005) and Dellaert and Kaess (2006) introduced square root SAM. They noted that smoothing over the whole path keeps the information matrix sparse, while filtering makes it dense. They used sparse QR and Cholesky with the COLAMD ordering. The work led to [iSAM](/isam/) (2008), the [Bayes tree](/bayes-tree/) and [iSAM2](/isam2/) (2012), and the GTSAM library.

## References
