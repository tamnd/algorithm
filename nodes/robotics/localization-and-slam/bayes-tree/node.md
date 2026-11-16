---
tag: XZ2CJC
kind: data-structure
slug: bayes-tree
name: Bayes tree
aliases:
- Bayes tree of a factor graph
area: robotics/localization-and-slam
level: research
summary: A directed tree of cliques from the elimination of a factor graph that encodes the square root information matrix and supports local updates.
model: real-ram
complexity:
  vars: {n: the number of variables, K: the number of factors, w: the number of variables in the largest clique, t: the number of variables in the removed top, o: the number of orphans}
  time: {build: O(K + n w^2), solve: O(n w), update: O(t w^2 + o)}
  space: {total: O(n w)}
history:
  year: 2010
  people: [Michael Kaess, Viorela Ila, Richard Roberts, Frank Dellaert]
  note: Kaess, Ila, Roberts and Dellaert presented the Bayes tree at WAFR 2010 as a directed clique tree for the incremental solution of sparse least squares problems in robot mapping.
prereqs: [factor-graph, variable-elimination, junction-tree]
see_also: [isam2, isam, square-root-sam, elimination-ordering, elimination-tree, multifrontal-method, chordal-graph, bayesian-network]
sources:
  - paper: "Michael Kaess, Viorela Ila, Richard Roberts and Frank Dellaert, The Bayes tree: an algorithmic foundation for probabilistic robot mapping, Algorithmic Foundations of Robotics IX (WAFR 2010), Springer Tracts in Advanced Robotics 68, 2011, pages 157 to 173"
    locator: "the definition of the Bayes tree from a chordal Bayes net, the clique creation rule, and the update with new factors that removes the top of the tree and reinserts the orphans"
  - paper: doi:10.1177/0278364911430419
    title: "Michael Kaess, Hordur Johannsson, Richard Roberts, Viorela Ila, John J. Leonard and Frank Dellaert, iSAM2: incremental smoothing and mapping using the Bayes tree, International Journal of Robotics Research 31(2), 2012, pages 216 to 235"
    locator: "the Bayes tree section: the algorithm that builds the tree from the eliminated factor graph, and the linear update of the tree with new factors"
  - paper: doi:10.1561/2300000043
    title: "Frank Dellaert and Michael Kaess, Factor graphs for robot perception, Foundations and Trends in Robotics 6(1-2), 2017"
    locator: "the chapters on variable elimination, the Bayes net and the Bayes tree, and incremental smoothing"
---

A Bayes tree stores the result of [variable elimination](/variable-elimination/) on a linear Gaussian [factor graph](/factor-graph/). Elimination in an order turns the factors into one Gaussian conditional per variable, $R_v x_v + \sum_s S_{vs} x_s = d_v$, given its parents $s$. These conditionals are the block rows of the square root information matrix $R$, so they form a [Bayesian network](/bayesian-network/) that is chordal. The Bayes tree groups the conditionals into cliques. Each clique holds frontal variables $F$ and separator variables $S$, and the conditionals of $F$ given $S$, and the separator lies in the parent clique. The root holds a joint density. Back substitution walks down the tree. A new factor changes only the clique where its first variable lives and the path above it to the root, so an update re-eliminates that top and keeps the rest. The tree is a directed form of the [junction tree](/junction-tree/), and it is the data structure of [iSAM2](/isam2/).

## In plain words

Solving a big system of measurements one unknown at a time leaves a chain of small rules. Each rule says how to compute one unknown from a few unknowns that come later. The Bayes tree puts these rules in small groups and hangs the groups in a tree, so that a group only needs the answers of the group above it. To get the answer, start at the top and go down. When a new measurement arrives, only the groups that hold its unknowns, and the groups above them, can change. The tree removes that part, redoes it with the new measurement, and hangs the old lower branches back where they fit.

## The abstract type

A Bayes tree over vector variables holds:

- a set of cliques, each with an ordered list of frontal variables $F$, a set of separator variables $S$, a parent clique (none for a root) and child cliques;
- for each frontal variable $v$, a Gaussian conditional $(R_v, \{S_{vs}\}, d_v)$ whose parents lie in the later frontal variables of its clique and in $S$;
- a map from each variable to the clique where it is frontal.

The tree must satisfy three rules: every variable is frontal in exactly one clique, the parents of each conditional lie in its clique, and the separator of each clique lies in the variables $F \cup S$ of its parent (the running intersection property). The tree encodes the quadratic $\sum_v \tfrac12\|R_v x_v + \sum_s S_{vs} x_s - d_v\|^2$, which equals the sum of the input factors up to a constant.

The operations are BUILD (from factors and an elimination order), SOLVE (the minimizer of the encoded quadratic), and UPDATE (add new factors).

## Representation

A clique is a record with the list of frontal variables in elimination order, the separator list, a parent pointer, a list of children, and a map from each frontal variable to its conditional. The conditional of $v$ holds the upper triangular $R_v$, a block $S_{vs}$ for each parent, and the vector $d_v$. The tree keeps a list of roots and a hash map from each variable to its clique. The code stores factors as $\tfrac12\|\sum_k A_k x_k - b\|^2$ with dense blocks, and works inside one elimination step in information form.

## Operations

```pseudo id=main
ELIMINATE(factors, order)
L1  for each variable v in order do
L2      G ← the remaining factors whose first variable in order is v
L3      (conditional of v given P_v, factor on P_v) ← eliminate v from the sum of G
L4      put the factor on P_v with the factors of its first variable
GROUP-INTO-CLIQUES(conditionals)
L5  for each conditional of v given P_v, in the reverse of the order do
L6      if P_v is empty then make a new root clique with F = [v]
L7      else p ← the clique of the first variable of P_v in the order
L8          if P_v = F_p ∪ S_p then put v at the front of F_p
L9          else make a new child clique of p with F = [v] and S = P_v
SOLVE(tree)
L10 for each clique, parents before children do
L11     for each v in F, from the last to the first do x_v ← R_v⁻¹ (d_v - Σ_s S_vs x_s)
UPDATE(tree, new factors F')
L12 top ← the cliques where a variable of F' is frontal, and all their ancestors
L13 orphans ← the children of top cliques that are not in the top
L14 G ← the conditionals of the top, read as factors, and the factors F'
L15 ELIMINATE G in a new order (the variables of F' last) and GROUP-INTO-CLIQUES
L16 for each orphan o do attach o under the new clique of the first variable of S_o in the new order
```

BUILD is ELIMINATE followed by GROUP-INTO-CLIQUES. Line L3 is one step of block Gaussian elimination: with $R^\top R = \Lambda_{vv}$ from the [Cholesky decomposition](/cholesky-decomposition/), $S_s = R^{-\top}\Lambda_{vs}$ and $d = R^{-\top}\eta_v$, and the factor on $P_v$ is $\Lambda_{ab} - S_a^\top S_b$, $\eta_a - S_a^\top d$. QR on the stacked Jacobian rows gives the same conditionals up to the signs of the rows of $R$.

Line L8 is the merge rule of Kaess et al. It puts a variable into the clique of its first parent only if its parents are all the variables of that clique. This makes each clique a clique of the chordal graph of the Bayes net.

Line L14 is valid because a conditional is itself a quadratic factor on $v$ and its parents. The first conditional of a clique involves all of $F \cup S$, so the separator of every orphan lies in one factor of $G$, and after elimination it lies in one new clique. That is why line L16 can always place the orphan. [iSAM2](/isam2/) adds relinearization to this update: it rebuilds the top from the original nonlinear factors instead of from the conditionals, and then needs the cached factors of the orphans.

## Example

Three poses $x_1, x_2, x_3$ and two landmarks $\ell_1, \ell_2$ lie on a line. All factors have unit noise:

| factor | equation |
|---|---|
| prior | $x_1 = 0$ |
| odometry | $x_2 - x_1 = 1$, $x_3 - x_2 = 1$ |
| landmark $\ell_1$ | $\ell_1 - x_1 = 2.1$, $\ell_1 - x_2 = 0.9$ |
| landmark $\ell_2$ | $\ell_2 - x_3 = 1$ |

Eliminate in the order $\ell_1, \ell_2, x_1, x_2, x_3$. The conditionals, rounded to four digits, are:

| variable | $R_v$ | $S_{vs}$ | $d_v$ |
|---|---|---|---|
| $\ell_1$ | 1.4142 | $x_1$: -0.7071, $x_2$: -0.7071 | 2.1213 |
| $\ell_2$ | 1 | $x_3$: -1 | 1 |
| $x_1$ | 1.5811 | $x_2$: -0.9487 | -1.0119 |
| $x_2$ | 1.2649 | $x_3$: -0.7906 | -0.2846 |
| $x_3$ | 0.6124 | | 1.2656 |

Grouping from $x_3$ back: $x_3$ starts the root. The parents of $x_2$ are $\{x_3\}$, all of the root, so $x_2$ merges into it. The parents of $x_1$ are $\{x_2\}$, not all of $\{x_2, x_3\}$, so $x_1$ starts a child clique with the separator $\{x_2\}$. The parents of $\ell_2$ are $\{x_3\}$, again not all of the root, so $\ell_2$ starts a second child. The parents of $\ell_1$ are $\{x_1, x_2\}$, all of the clique of $x_1$, so $\ell_1$ merges there. The tree is the root $\{x_2, x_3\}$ with the children $\{\ell_1, x_1 \mid x_2\}$ and $\{\ell_2 \mid x_3\}$.

SOLVE gives $x_3 = 1.2656 / 0.6124 = 2.0667$ at the root, then $x_2 = 1.0667$, then $x_1 = 0$ and $\ell_1 = 2.0333$ in the first child, and $\ell_2 = 3.0667$ in the second. Odometry says that $x_2 - x_1 = 1$, and the landmark says $1.2$. The three unit residuals of this loop share the gap of $0.2$ equally.

Now add a pose $x_4$ with the odometry $x_4 - x_3 = 1$. The variable $x_3$ is frontal in the root, so the top is the root only, and both children are orphans. The two root conditionals and the new factor are eliminated in the order $x_2, x_3, x_4$. The conditional of $x_2$ comes out the same as before. The new ones are $1.1726\,x_3 - 0.8528\,x_4 = -0.1919$ and $0.5222\,x_4 = 1.6015$. The new root is $\{x_3, x_4\}$ with the child $\{x_2 \mid x_3\}$. The orphan $\{\ell_1, x_1 \mid x_2\}$ goes under the clique of $x_2$, and the orphan $\{\ell_2 \mid x_3\}$ under the root. One clique was removed, two were made, and two were kept without any computation. SOLVE gives $x_4 = 3.0667$ and leaves the other values unchanged, because the new measurement agrees with the old estimate.

## Correctness

The [correctness proof](proofs/correctness.md) shows that ELIMINATE preserves the sum of the factors, that GROUP-INTO-CLIQUES gives a tree with the three rules above, and that SOLVE makes every conditional zero, which is the unique minimizer. For UPDATE it shows that the tree encodes the old system plus the new factors, and that each orphan's separator lies in the new clique where line L16 puts it. The tests compare SOLVE with a dense solve of the normal equations, and the sum of the conditionals with the dense $\Lambda$ and $\eta$, on random graphs with variables of size 1 and 2, under any order and after a sequence of updates.

## Complexity

Let $n$ be the number of variables, $K$ the number of factors, $w$ the number of variables of the largest clique, $t$ the number of variables in the removed top, and $o$ the number of orphans, with blocks of a fixed size.

- BUILD: $O(K + n w^2)$, because each elimination forms a new factor on at most $w$ variables.
- SOLVE: $O(n w)$ block products.
- UPDATE: $O(t w^2 + o)$, plus the time to find the top, which is the length of the paths to the root.
- Space: $O(n w)$ blocks for the conditionals.

The value of $w$ depends on the [elimination order](/elimination-ordering/) and the fill-in. Its smallest value over all orders is the [treewidth](/treewidth/) plus one, and finding that order is NP-hard. Heuristics such as [minimum degree](/minimum-degree-ordering/) and [nested dissection](/nested-dissection/) are used in practice.

## Variants

- **Marginals.** The root clique holds a joint density. The marginal of a clique follows from its parent by a recursion down the tree, so a marginal covariance near the root is cheap.
- **Nonlinear factors.** [iSAM2](/isam2/) keeps a linearization point and relinearizes the variables that moved more than a threshold, by including their cliques in the top.
- **Partial back substitution.** Stop the descent where the values of the separator did not change by more than a threshold.
- **Multifrontal solvers.** The cliques are the supernodes of the [multifrontal method](/multifrontal-method/), and the tree is a supernodal form of the [elimination tree](/elimination-tree/) of $R$.

## When to use it

Use a Bayes tree when a sparse least squares problem grows over time and the solution is needed after each addition, as in online SLAM, and when the new factors mostly touch recent variables. For a single batch solve, a sparse Cholesky or QR factorization, as in [square root SAM](/square-root-sam/), is simpler and has the same cost.

## Pitfalls

- **New variables early in the order.** If the new variables are not eliminated last, they end up deep in the tree, and the next update removes a long path. Put the variables of the new factors last.
- **Wrong orphan placement.** An orphan must go under the clique of the first eliminated variable of its separator. A different place breaks the running intersection property, and SOLVE then reads a separator value that is not computed yet.
- **Missing anchor.** A graph without a prior has a singular information matrix, and elimination fails at a block that is not positive definite.
- **Large cliques from loops.** A long loop closure joins old and new variables, and the cliques along the loop grow. The size of the tree is then close to that of a dense factor.
- **Confusing it with the junction tree.** A junction tree holds undirected potentials and passes messages both ways. A Bayes tree holds directed conditionals from one elimination and is solved by one pass from the root down.

## Implementations

## History

The junction tree of probabilistic inference and the elimination tree of sparse matrix factorization both come from variable elimination on a chordal graph. Kaess, Ila, Roberts and Dellaert (WAFR 2010, published 2011) defined the Bayes tree as the directed version for the square root information matrix of SLAM, and gave the update that removes the top and reinserts the orphans. Kaess et al. (2012) built [iSAM2](/isam2/) on it, which replaced the matrix updates of [iSAM](/isam/) by tree edits. The GTSAM library uses Bayes trees for its incremental solvers.

## References
