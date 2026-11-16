---
tag: 32NTDV
kind: algorithm
slug: isam2
name: "iSAM2"
aliases:
- incremental smoothing and mapping with the Bayes tree
area: robotics/localization-and-slam
level: research
summary: Incremental SLAM on a Bayes tree. Each update re-eliminates only the top of the tree above the new factors and the relinearized variables, with fluid relinearization by a threshold.
solves: [full-slam]
model: real-ram
complexity:
  vars: {p: the number of poses, m: the number of landmarks, w: the number of variables in the removed top, s: the number of variables in the largest clique, v: the number of cliques that the back substitution visits}
  time: {eliminate_top: O(w s^2), back_substitution: O(v s^2), worst_update: O((p + m)^3)}
  space: {tree: O((p + m) s)}
properties: {deterministic: true, exact: false, incremental: true, cost_depends_on_ordering: true}
history:
  year: 2012
  people: [Michael Kaess, Hordur Johannsson, Richard Roberts, Viorela Ila, John J. Leonard, Frank Dellaert]
  note: Kaess and colleagues replaced the matrix of iSAM by the Bayes tree, so that an update edits only the affected cliques, and added fluid relinearization and partial back substitution.
prereqs: [bayes-tree, isam, elimination-ordering]
see_also: [square-root-sam, factor-graph, junction-tree, variable-elimination, gauss-newton-algorithm, powell-dogleg, pose-graph-optimization, smoothing]
sources:
  - paper: doi:10.1177/0278364911430419
    title: "Michael Kaess, Hordur Johannsson, Richard Roberts, Viorela Ila, John J. Leonard and Frank Dellaert, iSAM2: incremental smoothing and mapping using the Bayes tree, International Journal of Robotics Research 31(2), 2012, pages 216 to 235"
    locator: "the creation of the Bayes tree from the eliminated factor graph, the incremental update of the top of the tree with the orphans, fluid relinearization with the threshold beta, partial state updates with the threshold alpha, and the constrained ordering"
  - paper: "Michael Kaess, Viorela Ila, Richard Roberts and Frank Dellaert, The Bayes tree: an algorithmic foundation for probabilistic robot mapping, Algorithmic Foundations of Robotics IX (WAFR 2010), Springer Tracts in Advanced Robotics 68, 2011, pages 157 to 173"
    locator: "the Bayes tree and its incremental update, the conference version of the data structure"
  - paper: doi:10.1561/2300000043
    title: "Frank Dellaert and Michael Kaess, Factor graphs for robot perception, Foundations and Trends in Robotics 6(1-2), 2017"
    locator: "the chapter on incremental smoothing with the Bayes tree"
---

iSAM2 keeps the solution of a SLAM problem current as new measurements arrive, without a full refactorization and without the periodic batch steps of [iSAM](/isam/). It stores the square root information matrix as a [Bayes tree](/bayes-tree/): a tree of cliques, each with Gaussian conditionals of its frontal variables given its separator. A new factor changes only the cliques that contain its variables and their ancestors up to the root. iSAM2 removes this top of the tree, turns it back into factors, adds the new factors, eliminates them again in a fresh local order, and puts the untouched subtrees back. Fluid relinearization moves the linearization point of a variable only when its step exceeds a threshold $\beta$, and partial back substitution stops at cliques whose inputs changed by less than $\alpha$. Both thresholds make it an approximation of batch [Gauss-Newton](/gauss-newton-algorithm/); with no relinearization and $\alpha = 0$, the linear solution is exact. The cost of an update depends on the [variable ordering](/elimination-ordering/) and the fill-in.

## In plain words

The robot keeps its map as a family tree of small groups of unknowns. Each group knows how its members depend on the group above it. When a new measurement arrives, only the groups that hold the measured unknowns, and the chain of groups above them, can change. iSAM2 takes off that part of the tree, redoes it with the new measurement, and hangs the rest back where it fits. It also redoes the straight-line view of a measurement only when an unknown has moved a lot since the last time. When it computes the answer, it walks down from the top and stops where nothing above has changed.

## The problem

The input is a stream of updates. Each update brings new nonlinear factors $f$ with Gaussian noise and initial values for new variables. After each update, the output is an estimate of all variables that minimizes, approximately, the [nonlinear least squares](/nonlinear-least-squares/) cost $\sum_f \|h_f(X) - z_f\|^2_{\Sigma_f}$ of all factors so far.

iSAM2 keeps the linearization point $\theta$, the current step $\Delta$, the estimate $\theta \oplus \Delta$, and the Bayes tree of the linear system at $\theta$. A clique has frontal variables $F$ and separator variables $S$, the conditionals $R_v \delta_v + \sum_s S_{vs} \delta_s = d_v$ of its frontal variables, and the cached factor on $S$ that its elimination passed to its parent. The code works on planar pose graphs with a prior and between factors. $\oplus$ adds the step to $(x, y, \theta)$ and wraps the angle.

## The algorithm

```pseudo id=main
UPDATE(new factors F', new values Θ')
L1  J ← {j : |Δ_j| ≥ β}                                   ▷ fluid relinearization
L2  θ_J ← θ_J ⊕ Δ_J;  Δ_J ← 0
L3  for each clique C with a variable of J in F_C ∪ S_C, or a variable of F' in F_C do
L4      mark C and all its ancestors                         ▷ the top
L5  orphans ← the unmarked children of the marked cliques
L6  G ← the factors whose variables all lie in the top, linearized at θ (again only if new or touching J)
L7  add the cached factors of the orphans to G
L8  π ← a minimum degree order of the top variables, with the variables of F' last
L9  eliminate G in the order π into conditionals
L10 build cliques from the conditionals and replace the top by them
L11 for each orphan o do attach o under the clique of the first variable of S_o in π
L12 BACK-SUBSTITUTE from the roots:
L13     skip a clique (and its subtree) if it is not new and no variable of S changed by more than α
L14     solve its frontal variables from the last eliminated to the first: δ_v ← R_v⁻¹ (d_v - Σ_s S_vs δ_s)
L15     record the variables that changed by more than α
```

**Building cliques (line L10).** Go through the conditionals in the reverse of the elimination order. A conditional with no parents starts a root clique. Otherwise, let $p$ be the clique of the first eliminated parent. If the parents are exactly all the variables $F_p \cup S_p$ of $p$, add the variable to $p$ as a frontal variable. If not, start a new child clique of $p$ with the parents as its separator. This is the rule of Kaess et al.

**Elimination (line L9).** The code keeps each linear factor in information form, $\tfrac12 \delta^\top \Lambda \delta - \eta^\top \delta$. To eliminate $v$, it adds the factors on $v$, takes the Cholesky factor $R$ of $\Lambda_{vv}$, and forms $S_s = R^{-\top}\Lambda_{vs}$ and $d = R^{-\top}\eta_v$. The new factor on the other variables is $\Lambda_{ab} - S_a^\top S_b$ and $\eta_a - S_a^\top d$. Kaess et al. use QR on the Jacobian rows instead; the conditionals are the same up to the signs of the rows of $R$.

**Why only the top.** A new factor on variables $V$ becomes a part of the clique of the first eliminated variable of $V$, and its effect flows only up to the root. A relinearized variable changes every factor that contains it, and those factors live in cliques that hold the variable as frontal or separator. Everything below the top is unchanged and is summed up by the cached factors of the orphans.

**Ordering (line L8).** The code uses minimum degree on the top only, with the new variables last; Kaess et al. use constrained COLAMD. Putting the newest variables last keeps them near the root, so the next update, which will likely touch them again, removes a small top.

## Example

The robot drives two laps of a 12-sided polygon with sides of 1 m, so there are 25 poses. Each step adds a between factor for the odometry (noise 0.05 m, 0.05 m and 0.02 rad). In the second lap, each pose $t$ also gets a loop closure to the pose $t - 12$ at the same place, with the same noise. The seed is 4. Dead reckoning drifts to a largest position error of 0.577 m.

With $\beta = 0.1$ and $\alpha = 0$:

| step | relinearized variables | cliques eliminated | cliques in the tree |
|---|---|---|---|
| 1 to 11 | 0 | 1 or 2 | 1 to 11 |
| 12 (first loop closure) | 0 | 11 | 11 |
| 13 | 6 | 12 | 12 |
| 14 to 24 | 1 or 2 | 9 to 16 | 12 to 22 |

Over the 25 updates, 183 cliques were eliminated out of 277 cliques present after the updates, and 18 variables were relinearized. The final estimate is within 0.0026 of the batch Gauss-Newton optimum, and its cost is 36.858 against 36.844 for the batch optimum. The largest position error against the truth is 0.153 m. The final tree has 22 cliques of at most 4 variables, with the root clique $\{x_{12}, x_{23}, x_{24}\}$.

Without relinearization ($\beta = \infty$), the estimate stays at the linearization of dead reckoning and is 0.017 from the batch optimum, with the cost 37.366. With $\alpha = 10^{-3}$, the back substitution solved 229 cliques instead of 267, and the result was the same to the digits above.

These numbers are measurements on a graph with a loop closure at every step of the second lap. There, each loop closure reaches far back, and an update re-eliminates most of the tree. iSAM2 gains much more on large graphs where most updates are local.

## Correctness

The [correctness proof](proofs/correctness.md) shows by induction over the updates that the conditionals of the tree always sum to the full linear system of all factors at the current linearization point. The key step is that a factor whose clique stays below the top contains no relinearized variable, so its old linear form is still valid, and the cached factor of each orphan sums up its whole subtree. It also shows that the tree stays valid (each variable is frontal once, and each separator lies in the parent clique), and that with $\alpha = 0$ the back substitution gives the exact solution of the linear system. The tests check the tree against a dense solve to $10^{-9}$ after the updates without relinearization, check the tree invariants and the full information matrix after every update with relinearization, and check that repeated updates with a tiny $\beta$ reach the batch optimum to $10^{-8}$.

Fluid relinearization and partial back substitution are approximations controlled by thresholds. The estimate with $0 < \beta$ is not a stationary point of the nonlinear cost in general.

## Complexity

Let $w$ be the number of variables in the removed top, $s$ the number of variables of the largest clique, and $v$ the number of cliques that the back substitution visits, with blocks of a fixed size.

- Removing the top and finding the orphans: proportional to the size of the top.
- Elimination of the top: $O(w s^2)$ block operations.
- Back substitution: $O(v s^2)$.
- Memory: $O((p + m) s)$ for the conditionals.

The size of the top and of the cliques depends on the variable ordering and the fill-in; see [elimination ordering](/elimination-ordering/). An update that touches the oldest pose of a long loop can remove the whole tree, which costs as much as a batch step, $O((p + m)^3)$ in the worst case. Kaess et al. report on data sets that most updates touch a small top. That is a measurement, not a bound. The code also scans all factors at line L6 to find those in the top; an index from variables to factors removes this scan.

## Properties

- **Incremental and exact for linear problems.** With no relinearization, every update gives the same linear solution as a batch solve.
- **No periodic batch steps.** Unlike [iSAM](/isam/), it reorders only the top, so the fill-in does not build up over time in the same way.
- **Approximate for nonlinear problems.** The thresholds $\beta$ and $\alpha$ trade accuracy for time.
- **Local edits.** A new measurement between two recent poses touches only cliques near the root.

## Variants and improvements

- **Trust region steps.** A step such as [Powell's dogleg](/powell-dogleg/) can replace the Gauss-Newton step, so that a poor initial value does not make the update diverge.
- **Per-variable thresholds.** Use a different $\beta$ for rotations and translations, or for landmarks and poses.
- **Marginal covariances.** The Bayes tree gives the marginal covariance of a variable by a recursion from the root, which is useful for data association.
- **Fixed-lag smoothing.** Marginalize the oldest variables out of the tree to bound the memory.

## When to use it

Use iSAM2 for online SLAM and visual-inertial odometry, where the estimate must be current after every new measurement and the problem grows over time. For a one-time batch problem, [square root SAM](/square-root-sam/) or a sparse solver is simpler. When the problem is a pose graph and a certificate of global optimality matters, use [SE-Sync](/se-sync/) offline.

## Pitfalls

- **A threshold $\beta$ that is too large.** Variables keep a stale linearization, and the estimate stays biased. The example shows this with $\beta = \infty$.
- **Mixed units.** One threshold on meters and radians treats them alike. Set the thresholds per variable type.
- **Wrong orphan placement.** An orphan must go under the clique of the first eliminated variable of its separator. Any other place breaks the running intersection property, and the back substitution then uses values that are not solved yet.
- **New variables first.** If the order puts a new pose early, the next update removes most of the tree.
- **Missing priors.** Like every Gaussian elimination, the tree needs a positive definite block for each variable, so the graph needs a prior or an anchor.

## Implementations

## History

Dellaert and Kaess (2006) solved full SLAM by sparse QR in [square root SAM](/square-root-sam/). Kaess, Ranganathan and Dellaert (2008) made it incremental with Givens rotations in [iSAM](/isam/), with periodic batch steps for the ordering and the relinearization. Kaess, Ila, Roberts and Dellaert presented the [Bayes tree](/bayes-tree/) at WAFR 2010, and Kaess et al. (2012) built iSAM2 on it. iSAM2 is the incremental solver of the GTSAM library.

## References
