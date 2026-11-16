---
tag: CYW7G6
kind: algorithm
slug: isam
name: Incremental smoothing and mapping
aliases:
- iSAM
area: robotics/localization-and-slam
level: research
summary: Incremental SLAM back end of Kaess, Ranganathan and Dellaert. It updates the square root information matrix by Givens rotations as measurements arrive, with periodic reordering and relinearization.
solves: [full-slam]
model: real-ram
complexity:
  vars: {p: the number of poses, m: the number of landmarks, k: the period of the batch step, g: the number of Givens rotations in one update, z: the number of nonzero entries of R}
  time: {incremental_update: O(g (p + m) + z), batch_step: O((p + m)^3), amortized: O(g (p + m) + z + (p + m)^3 / k)}
  space: {factor: O(z)}
properties: {deterministic: true, exact: false, incremental: true, cost_depends_on_ordering: true}
history:
  year: 2008
  people: [Michael Kaess, Ananth Ranganathan, Frank Dellaert]
  note: Kaess, Ranganathan and Dellaert made square root SAM incremental. New measurement rows enter the triangular factor by Givens rotations, and a periodic batch step reorders the variables and relinearizes.
prereqs: [square-root-sam, givens-rotations, qr-decomposition]
see_also: [isam2, bayes-tree, elimination-ordering, minimum-degree-ordering, graphslam, back-substitution, factor-graph, pose-graph-optimization]
sources:
  - paper: doi:10.1109/TRO.2008.2006706
    title: "Michael Kaess, Ananth Ranganathan and Frank Dellaert, iSAM: incremental smoothing and mapping, IEEE Transactions on Robotics 24(6), 2008, pages 1365 to 1378"
    locator: "the update of the square root information matrix by Givens rotations, the periodic variable reordering and relinearization, and the recovery of marginal covariances for data association"
  - paper: doi:10.1177/0278364906072768
    title: "Frank Dellaert and Michael Kaess, Square root SAM: simultaneous localization and mapping via square root information smoothing, International Journal of Robotics Research 25(12), 2006, pages 1181 to 1203"
    locator: "the batch factorization of the measurement Jacobian that iSAM updates"
  - book: isbn:9780898716139
    title: "Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006"
    locator: "sparse QR factorization, fill-in and fill-reducing orderings"
---

iSAM solves the [full SLAM problem](/full-slam/) online. It keeps the upper triangular factor $R$ of the whitened measurement Jacobian, as in [square root SAM](/square-root-sam/), and changes it as measurements arrive instead of computing it again. A new measurement adds rows to the Jacobian. Each new row enters $R$ by [Givens rotations](/givens-rotations/), one rotation for each nonzero entry that must be cleared. A new variable adds columns at the end of the column order. After each update, one [back substitution](/back-substitution/) gives the new estimate. Two things go stale over time: the column order, which was chosen for the old graph, and the linearization point. So every $k$ updates iSAM does a batch step. It relinearizes all factors at the current estimate, finds a new fill-reducing [elimination order](/elimination-ordering/), and factors again. The cost of each update depends on the order and the fill-in. [iSAM2](/isam2/) later replaced the matrix by a [Bayes tree](/bayes-tree/) and the periodic batch step by local edits.

## In plain words

The robot keeps its map as a triangle of numbers that makes the answer quick to read out. When a new measurement arrives, it does not rebuild the triangle. It slides the new line of numbers into the triangle, one small turn at a time, until the line is used up or finds an empty slot. Then it reads out the new answer from the bottom up. Over time the triangle gets crowded, because the order of the unknowns was chosen for an older and smaller map. So, every so often, the robot picks a better order, redoes the straight-line view of all measurements at the current answer, and builds the triangle again.

## The problem

The input is a stream of updates. Each update brings new variables with initial values and new factors, each with a measurement function $h_f$, a measurement $z_f$ and a diagonal noise $\sigma_f$. After each update, the output is an estimate that minimizes, approximately, the [nonlinear least squares](/nonlinear-least-squares/) cost $\sum_f \|(h_f(X) - z_f) / \sigma_f\|^2$ over all factors so far.

iSAM keeps the linearization point $\theta$, a column order, and the sparse upper triangular $R$ with the right side $d$. These satisfy $R^\top R = A^\top A$ and $R^\top d = A^\top b$, where $A\delta = b$ is the whitened linear system of all factors at $\theta$. The estimate is $\theta \oplus \delta$ with $R\delta = d$. The code works with planar poses $(x, y, \theta)$, point landmarks, a prior, odometry, and range and bearing measurements.

## The algorithm

```pseudo id=main
UPDATE(new values Θ', new factors F')
L1  append the variables of Θ' to the end of the column order;  θ ← θ ∪ Θ'
L2  for each whitened row [a | β] of the factors F' at θ do
L3      ROTATE-IN(a, β):
L4      while a has a nonzero entry do
L5          c ← the first column where a is not zero
L6          if R has no row with the pivot c then R_c ← [a | β];  stop
L7          apply the Givens rotation that sets a_c to 0 to the pair (R_c, [a | β])
L8  if the number of updates is a multiple of k then
L9      θ ← θ ⊕ δ;  find a fill-reducing order of all variables
L10     R ← empty;  ROTATE-IN every whitened row of every factor at θ, in the new order
L11 δ ← the solution of R δ = d by back substitution
L12 return θ ⊕ δ
```

**The rotation (line L7).** With $h = \sqrt{(R_c)_c^2 + a_c^2}$, $\cos\phi = (R_c)_c / h$ and $\sin\phi = a_c / h$, the pair becomes $(\cos\phi\, R_c + \sin\phi\, a,\ -\sin\phi\, R_c + \cos\phi\, a)$. The first row keeps its place in $R$ with the pivot $h$. The second row has a zero at $c$, and its next nonzero entry is further right. The rotation is orthogonal, so $R^\top R + a^\top a$ does not change. A row that becomes zero except for $\beta$ leaves only its $\beta$ in the residual and is dropped.

**New variables (line L1).** The new columns go last. Old rows are zero there, so $R$ stays upper triangular. A new pose is linearized at its initial value, which is usually the estimate of the previous pose composed with the odometry.

**Fill-in.** A Givens rotation writes the nonzero entries of the new row into $R_c$. An odometry row from the newest pose touches only the last columns and costs a few rotations. A measurement of a landmark seen long ago starts at the old column of the landmark, rotates through every row between it and the end, and fills them. That is the fill-in that the batch step removes.

**The batch step (lines L9 and L10).** Kaess et al. use COLAMD for the order. The code uses minimum degree on the graph of the variables, with the degree counted in scalar columns. The batch step is also the only place where iSAM relinearizes.

## Example

The robot drives two laps of a 12-sided polygon with sides of 1 m, so there are 25 poses. Six landmarks lie around the path, and the robot measures range and bearing to every landmark within 3 m. The noise is 0.05 m, 0.05 m and 0.02 rad for odometry, and 0.05 m and 0.02 rad for range and bearing. The seed is 4. In total there are 136 factors, 297 rows and 87 columns. A full upper triangle of size 87 has 3828 entries. Dead reckoning drifts to a position error of 0.714 m.

| batch period $k$ | rotations in total | rotations per update in steps 20 to 23 | nonzeros of the final $R$ | final cost | distance to the optimum |
|---|---|---|---|---|---|
| none | 9213 | 750 to 832 | 3534 | 230.124 | 0.019 |
| 10 | 8659 | 166 to 229 | 1295 | 214.746 | 0.0035 |
| 5 | 14190 | 166 to 229 | 1193 | 214.141 | 0.00074 |

The optimum of the cost is 214.132. Without batch steps, the rotations per update grow from 71 at the first odometry step to about 800 in the second lap, and $R$ ends at 92% of a full triangle. Each landmark that comes back into view starts at an early column and fills the rows after it. With $k = 5$, the batch steps at updates 5, 10, 15, 20 and 25 cost 517, 1415, 2368, 3200 and 3869 rotations, and the updates between them cost 78 to 242. On this small problem, the batch steps with $k = 5$ cost more rotations in total than they save. The gains are a sparser $R$, a cheaper back substitution, and an estimate close to the optimum because of the relinearization. With $k = 10$, the total is lower than without batch steps. The largest position error against the truth is 0.081 m without batch steps and 0.073 m with $k = 5$.

These are measurements on one small run. On long runs with many loops, the fill without reordering grows much more, and Kaess et al. report that periodic reordering keeps the update time low.

## Correctness

The [correctness proof](proofs/correctness.md) shows by induction over the rows that $R$ stays upper triangular with nonzero pivots and that $R^\top R = A^\top A$ and $R^\top d = A^\top b$ hold for the whitened system of all factors at $\theta$. The key facts are that a Givens rotation is orthogonal, that each rotation moves the leading column of the new row to the right, and that appended columns are zero in all old rows. So the back substitution gives the exact least squares solution of the linear system at $\theta$, which is one [Gauss-Newton](/gauss-newton-algorithm/) step from $\theta$. The tests check these equations against dense products after the updates, with and without batch steps, and check a noise-free stream against the truth.

The estimate between batch steps is not a stationary point of the nonlinear cost, because the linearization point is old. It is an approximation, and the period $k$ controls it.

## Complexity

Let $p$ be the number of poses, $m$ the number of landmarks, $g$ the number of rotations of one update, $z$ the number of nonzero entries of $R$, and $k$ the batch period.

- One rotation touches the union of two rows, at most $O(p + m)$ entries, so the rotations of one update cost $O(g (p + m))$.
- The back substitution costs $O(z)$.
- A batch step is a sparse QR factorization of all rows. Its cost depends on the order and the fill-in, and is $O((p + m)^3)$ in the worst case of a dense factor.
- Memory is $O(z)$.

The numbers $g$ and $z$ depend on the column order and the fill-in; see [elimination ordering](/elimination-ordering/). For exploration with odometry only, $g$ is bounded and $z$ grows linearly. A loop closure to an old variable makes $g$ grow with the number of columns after it.

## Properties

- **Exact for a fixed linearization.** Between batch steps, $\delta$ is the exact solution of the linear system at $\theta$.
- **Incremental.** An update touches only the rows of $R$ from the first column of the new rows to the end.
- **Periodic batch steps.** The update time has spikes at the batch steps.
- **Square root form.** It never forms $A^\top A$, so it avoids squaring the condition number.

## Variants and improvements

- **Marginal covariances.** Kaess et al. recover the needed entries of the covariance from $R$ by a recursion, and use them for data association.
- **Cholesky updates.** A new row $a$ adds $a^\top a$ to $A^\top A$. A rank one update of the [Cholesky factor](/cholesky-decomposition/) gives the same $R$ up to the signs of its rows.
- **Fixed lag.** Marginalize old variables to bound the size of $R$.
- **The Bayes tree.** [iSAM2](/isam2/) stores $R$ as a [Bayes tree](/bayes-tree/), reorders only the affected cliques, and relinearizes only the variables that moved. It has no periodic batch step.

## When to use it

Use iSAM for online SLAM with an estimate after every measurement when the loops are rare or the batch period can be tuned. When loops are frequent or the spikes of the batch steps matter, [iSAM2](/isam2/) is the better choice. For a one-time problem, use [square root SAM](/square-root-sam/) or a batch Gauss-Newton solver.

## Pitfalls

- **New variables in the middle.** If a new variable is not put at the end of the order, the old rows of $R$ are no longer triangular in the new order. Append new columns.
- **Old linearization.** Between batch steps, a large correction from a loop closure is computed on an old linearization. A small period $k$ helps, at the cost of more batch steps.
- **Poor initial values.** A new pose must be initialized from the current estimate and the odometry, not from dead reckoning. Otherwise its linearization point is far from the solution.
- **Rank deficiency.** A variable that no factor constrains enough has no pivot row. The graph needs a prior and enough measurements for each landmark.
- **Dropped rows.** A row that becomes zero still carries its right side. Keep it in the residual if the cost is needed, but it does not change $\delta$.

## Implementations

## History

Dellaert and Kaess (2006) solved full SLAM in batch with sparse QR or Cholesky in [square root SAM](/square-root-sam/). Kaess, Ranganathan and Dellaert (2008) made it incremental with Givens rotations and periodic reordering and relinearization, and called it iSAM. Kaess and colleagues later replaced the matrix by the [Bayes tree](/bayes-tree/), first at WAFR 2010 and then in [iSAM2](/isam2/) (2012).

## References
