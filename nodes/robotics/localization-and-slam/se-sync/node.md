---
tag: ZTRAGF
kind: algorithm
slug: se-sync
name: "SE-Sync"
aliases:
- certifiably correct pose graph optimization
area: robotics/localization-and-slam
level: research
summary: Solves pose graph optimization through a semidefinite relaxation and the Riemannian staircase, and certifies a global optimum when the relaxation is tight.
solves: [pose-graph-optimization]
model: real-ram
complexity:
  vars: {n: the number of poses, m: the number of edges, r: the rank of the current step of the staircase}
  time: {local_search_sweep: O(r (n + m)), certificate: O(r (n + m)), jacobi_sweep_dense: O(n^3), rounding: O(r^2 n + r^3)}
  space: {iterate: O(r n), sparse_q: O(n + m)}
properties: {deterministic: true, exact: false, certifies_global_optimum: true, needs_tight_relaxation: true}
history:
  year: 2019
  people: [David M. Rosen, Luca Carlone, Afonso S. Bandeira, John J. Leonard]
  note: Rosen, Carlone, Bandeira and Leonard solved the semidefinite relaxation of pose graph optimization by a low rank Riemannian method and proved that the relaxation is exact when the noise is small enough. A conference version appeared in 2016.
prereqs: [pose-graph-optimization, semidefinite-programming, special-orthogonal-group]
see_also: [rotation-averaging, convex-relaxation, lagrangian-duality, pose-graph, isam2, switchable-constraints, gauss-newton-algorithm, eigenvalue-problem]
sources:
  - paper: doi:10.1177/0278364918784361
    title: "David M. Rosen, Luca Carlone, Afonso S. Bandeira and John J. Leonard, SE-Sync: a certifiably correct algorithm for synchronization over the special Euclidean group, International Journal of Robotics Research 38(2-3), 2019, pages 95 to 125"
    locator: "the semidefinite relaxation of pose graph optimization, the closed form elimination of the translations, the exact recovery guarantee for small noise (Proposition 2), the Riemannian staircase, the optimality certificate and the rounding procedure"
  - paper: doi:10.1007/s10107-002-0352-8
    title: "Samuel Burer and Renato D. C. Monteiro, A nonlinear programming algorithm for solving semidefinite programs via low-rank factorization, Mathematical Programming 95(2), 2003, pages 329 to 357"
    locator: "the low rank factorization Z = Y^T Y of the semidefinite variable"
  - paper: doi:10.1109/TRO.2016.2624754
    title: "Cesar Cadena, Luca Carlone, Henry Carrillo, Yasir Latif, Davide Scaramuzza, Jose Neira, Ian Reid and John J. Leonard, Past, present, and future of simultaneous localization and mapping: toward the robust-perception age, IEEE Transactions on Robotics 32(6), 2016, pages 1309 to 1332"
    locator: "the discussion of global optimality and certifiable back ends"
---

SE-Sync solves [pose graph optimization](/pose-graph-optimization/) and returns a proof that the answer is the global optimum when it can. Pose graph optimization is nonconvex because rotations live on the curved set $SO(d)$, so [Gauss-Newton](/gauss-newton-algorithm/) and similar local methods can stop at a wrong local minimum and cannot tell. SE-Sync first removes the translations in closed form. What is left is a problem over the rotations alone, $\min \mathrm{tr}(\tilde Q R^\top R)$ with $R \in SO(d)^n$. It relaxes this problem to a [semidefinite program](/semidefinite-programming/) and solves the relaxation in the low rank form $Z = Y^\top Y$ of Burer and Monteiro, where $Y$ has only $r$ rows. A local search finds a critical point $Y$. A matrix $S$ built from $Y$ and the data is the certificate: if $S$ is positive semidefinite, $Y^\top Y$ solves the relaxation. If not, the eigenvector of the least eigenvalue of $S$ points downhill in a space with one more row, and the search goes up one step of this "Riemannian staircase". At the end, SE-Sync rounds $Y$ to rotations. The relaxation value is a lower bound, and the cost of the rounded answer is an upper bound. When the relaxation is tight, the two are equal, and the rounded answer is a certified global optimum. Rosen et al. prove that this happens when the noise is below a level that depends on the graph.

## In plain words

Many poses must agree with many measurements of how they relate. A normal solver walks downhill from a guess and stops at the first low point, which may not be the lowest. SE-Sync loosens the problem so that it has no false low points, solves the loose version, and then checks a simple condition that proves the loose answer is the best one. If the check fails, the check itself shows a way down, and the search continues with one more degree of freedom. At the end, the loose answer is turned back into real rotations. If the loose problem and the real problem give the same value, the answer is proved to be the best possible. When the measurements are very noisy, the two values can differ. Then the gap still tells how far from the best the answer can be.

## The problem

The input is a connected graph on $n$ poses. Each edge $(i, j)$ has a measured relative rotation $\tilde R_{ij}$, a measured relative translation $\tilde t_{ij}$, and weights $\kappa_{ij}, \tau_{ij} > 0$. The problem is

$$\min_{R_i \in SO(d),\ t_i \in \mathbb{R}^d} \sum_{(i,j)} \kappa_{ij} \|R_j - R_i \tilde R_{ij}\|_F^2 + \tau_{ij} \|t_j - t_i - R_i \tilde t_{ij}\|_2^2.$$

For fixed rotations the cost is a linear least squares problem in the translations, so the translations can be eliminated. The result is $\min \mathrm{tr}(\tilde Q R^\top R)$ over $R = [R_1 \cdots R_n] \in SO(d)^n$, for a symmetric positive semidefinite matrix $\tilde Q$ of size $dn$. With rotation edges only, $\tilde Q$ is the connection Laplacian $Q$, with blocks $Q_{ii} = \sum_{j \sim i} \kappa_{ij} I$ and $Q_{ij} = -\kappa_{ij} \tilde R_{ij}$. Its scalar analogue is the [Laplacian matrix](/laplacian-matrix/) of the graph.

The code is the planar rotation case: $d = 2$ and the matrix $Q$ of the rotation edges. It is the core of SE-Sync without the translation step. The same steps apply to $\tilde Q$ and to $d = 3$.

## The algorithm

The relaxation replaces $R_i \in SO(d)$ by $Y_i \in \mathbb{R}^{r \times d}$ with $Y_i^\top Y_i = I$. The set of such $Y_i$ is the Stiefel manifold $\mathrm{St}(d, r)$. For $r \ge d$, $\min \mathrm{tr}(Q Y^\top Y)$ is a lower bound on the original problem. Burer and Monteiro showed that for $r$ large enough it equals the semidefinite program $\min \mathrm{tr}(QZ)$ with $Z \succeq 0$ and $Z_{ii} = I$.

```pseudo id=main
SE-SYNC(Q, initial rotations R⁰)
L1  r ← d;  Y ← [R⁰_1 ... R⁰_n]
L2  loop
L3      Y ← a first order critical point of tr(Q YᵀY) on St(d, r)^n, by local search from Y
L4      Λ ← the block diagonal matrix with Λ_ii = Sym((Q YᵀY)_ii);  S ← Q - Λ
L5      (λ, v) ← the least eigenvalue of S and a unit eigenvector
L6      if λ ≥ -ε then leave the loop
L7      r ← r + 1;  Y ← a descent step from [Y; 0] along the new row vᵀ, with a line search
L8  R̂ ← ROUND(Y): the top d rows of UᵀY from the SVD of Y, sign fix, nearest rotation per block
L9  return R̂, the lower bound tr(Q YᵀY) and the upper bound tr(Q R̂ᵀR̂)
```

**Local search (line L3).** Rosen et al. use a Riemannian trust region method. The code uses block coordinate descent. With all blocks except $Y_i$ fixed, the cost is $2\,\mathrm{tr}(Y_i^\top G_i)$ plus a constant, with $G_i = \sum_{j \ne i} Y_j Q_{ji}$. Its minimizer over $\mathrm{St}(d, r)$ is the polar factor of $-G_i$. Each step can only decrease the cost. The search stops when a full sweep changes the cost by less than a relative $10^{-12}$.

**The certificate (lines L4 to L6).** The Riemannian gradient at $Y$ is $2YS$, so at a critical point $YS = 0$. If also $S \succeq 0$, then for any feasible $Z$, $\mathrm{tr}(QZ) = \mathrm{tr}(SZ) + \mathrm{tr}(\Lambda) \ge \mathrm{tr}(\Lambda) = \mathrm{tr}(Q Y^\top Y)$. So $Y^\top Y$ solves the semidefinite program, and $\Lambda$ is the dual solution. The code finds the least eigenvalue with the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/) on the dense $S$. Rosen et al. use a sparse Lanczos method. The tolerance $\varepsilon$ is $10^{-6}$ times the largest entry of $Q$.

**The staircase step (line L7).** If $v^\top S v = \lambda < 0$, then the step $[Y; 0] + \alpha [0; v^\top]$, mapped back to $\mathrm{St}(d, r + 1)$ by the polar factor of each block, changes the cost by $\alpha^2 \lambda + O(\alpha^4)$. The code starts at $\alpha = 1$ and halves $\alpha$ until the cost decreases.

**Rounding (line L8).** If $Y$ has rank $d$, the top $d$ rows of $U^\top Y$ give $R$ with $R^\top R = Y^\top Y$ and $R_i \in O(d)$. If most blocks have a negative determinant, the code changes the sign of one row. Then each block goes to the nearest rotation, and the result is multiplied by $\hat R_1^\top$ so that $\hat R_1 = I$.

## Example

**A wrong critical point.** Take a cycle of 9 rotations whose 9 measurements are all the identity, with weights 1. The global optimum has all rotations equal and cost 0. Start at the "twisted" state $R_i = \mathrm{Rot}(2\pi i / 9)$. Each edge then has the error $\|\mathrm{Rot}(40°) - I\|_F^2 = 4 - 4\cos 40° = 0.9358$, so the cost is $8.4224$. Every rotation sits halfway between its two neighbors, so the gradient is zero, and block coordinate descent does not move. A local solver stops here. The certificate does not. The eigenvalues of $S$ at this point are $-0.4679$ (twice), $0$ (four times), $1.1848$, $2.5321$ and $3.4115$ (four times each). The staircase runs as follows.

| rank $r$ | cost after the local search | least eigenvalue of $S$ | sweeps |
|---|---|---|---|
| 2 | 8.4224 | -0.4679 | 1 |
| 3 | 4.2112 | -0.4679 | 35 |
| 4 | $7.4 \times 10^{-13}$ | $-8 \times 10^{-14}$ | 41 |

At rank 4 the certificate holds, and rounding gives all rotations equal with cost about 0.

**A random problem.** Ten rotations at random angles, a path through them plus 10 random extra edges, and Gaussian angle noise with $\sigma = 0.1$ rad on each measurement (seed 4). The start composes the measurements along a breadth-first [spanning tree](/spanning-tree/). It has cost 1.0634 and a largest angle error of 0.264 rad. The truth has cost 0.6213. After 14 sweeps the certificate holds at rank 2 with $\lambda_{\min} = -2.1 \times 10^{-15}$. The lower bound and the upper bound are both 0.248577, so the answer is a certified global optimum. Its largest angle error against the truth is 0.130 rad.

**More noise.** On five random problems for each noise level, with 10 rotations and 10 extra edges, the relaxation was tight at rank 2 for all problems at $\sigma = 0.3$ and $0.6$ rad. At $\sigma = 1.0$ rad it was tight for three of the five. The other two stopped at rank 4 with gaps of 0.875 and 3.42 between the upper and the lower bound. At $\sigma = 1.5$ and $2.0$ rad, some problems again had gaps. One problem at $\sigma = 2.0$ went up to rank 3 and was still tight. These are measurements on small problems, and they agree with the guarantee: below a noise level the relaxation is exact, and above it a gap can appear.

## Correctness

The [correctness proof](proofs/correctness.md) shows that the cost equals $\mathrm{tr}(Q R^\top R)$, that the Riemannian gradient is $2YS$, that $YS = 0$ and $S \succeq 0$ make $Y^\top Y$ optimal for the semidefinite program, and that the staircase step decreases the cost when $S$ has a negative eigenvalue. It also shows that the lower bound is at most the optimum and the upper bound at least the optimum, and that a rank $d$ certified $Y$ with the right determinants rounds to a global minimizer. It does not show that the relaxation is tight; that is the theorem of Rosen et al. for small noise. The tests check the trace form, exact recovery without noise, the certificate and a zero gap at low noise, the first order condition, a brute force search over three rotations, and the twisted cycle.

## Complexity

Let $n$ be the number of poses, $m$ the number of edges and $r$ the current rank.

- One sweep of block coordinate descent costs $O(r (n + m))$: each block reads its neighbors and takes the polar factor of an $r \times d$ matrix.
- Forming $S$ and the gradient costs $O(r (n + m))$ with a sparse $Q$.
- The least eigenvalue costs $O(n^3)$ per Jacobi sweep with the dense $S$ of the code. A sparse Lanczos method needs only products with $S$, at $O(n + m)$ each.
- Rounding costs $O(r^2 n + r^3)$.
- The number of local search iterations and of staircase steps depends on the data. In practice the staircase stops at $r = d$ or one step above when the noise is moderate.

## Properties

- **Certifiable.** A tight run returns a proof of global optimality that anyone can check with one eigenvalue computation.
- **Bounds.** Every run returns a lower and an upper bound on the optimum.
- **Exact below a noise level.** Rosen et al. prove that the relaxation is exact when the noise is small enough.
- **Independent of the start.** The certificate does not depend on the initial guess. The start changes only the run time.
- **No translations in the search.** The translations are recovered in closed form after the rotations.

## Variants and improvements

- **Other local solvers.** A Riemannian trust region method converges faster than block coordinate descent.
- **Verification only.** Carlone and colleagues earlier used [Lagrangian duality](/lagrangian-duality/) to verify a candidate from a local solver. SE-Sync makes the same kind of check part of the solver.
- **Other synchronization problems.** The same relaxation and certificate work for [rotation averaging](/rotation-averaging/) in structure from motion.
- **Distributed and incremental versions.** Later work splits the problem across robots or keeps the certificate up to date as the graph grows.
- **Robust costs.** Wrong loop closures break the noise assumption. Robust versions combine certifiable relaxations with outlier models such as [switchable constraints](/switchable-constraints/).

## When to use it

Use SE-Sync when a wrong local minimum is costly and the measurements have moderate noise, for example to check a map before a long mission, or to start a local solver from a good point. For online use with frequent updates, [iSAM2](/isam2/) is faster, and SE-Sync can check its result from time to time. With outliers in the loop closures, first remove them or use a robust method.

## Pitfalls

- **Outliers.** A wrong loop closure is not small noise. The relaxation can then be loose, and a certified optimum of the wrong cost is still wrong.
- **The tolerance on $\lambda$.** The least eigenvalue of $S$ is zero at a solution, because the rows of $Y$ are in its null space. A test against an exact zero fails because of rounding. Scale the tolerance by the size of $Q$.
- **Rank above $d$.** If the staircase stops at a rank above $d$, the rounded answer is not certified. Report the gap, not a claim of optimality.
- **The gauge.** The cost does not change when all rotations are multiplied by one rotation. Fix one pose, as the code does with $\hat R_1 = I$, before comparing results.
- **A disconnected graph.** The cost then has more than one gauge freedom, and the spanning tree start fails.

## Implementations

## History

Synchronization problems over rotations were studied in computer vision and in signal processing before SLAM. Carlone, Rosen, Calafiore, Leonard and Dellaert used Lagrangian duality in 2015 to verify the optimality of a pose graph solution from a local solver. Rosen, Carlone, Bandeira and Leonard presented SE-Sync in 2016 and published the journal version in 2019. It joins the semidefinite relaxation, the low rank method of Burer and Monteiro (2003), and the Riemannian staircase of Boumal. Later certifiable methods extend the idea to landmarks, to robust costs and to distributed solvers.

## References
