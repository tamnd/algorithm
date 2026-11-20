---
tag: G0MEX4
kind: algorithm
slug: dorfler-marking
name: Dorfler marking
aliases:
- bulk marking
area: scientific-computing/finite-element-practice
level: advanced
summary: "Marks a smallest set of elements whose squared indicators sum to at least a fraction theta of the total, the marking rule behind the convergence proofs of AFEM."
model: real-ram
complexity:
  vars: {M: the number of elements}
  time: {average: "Θ(M)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: false, minimal_cardinality: true, exact_with_exact_arithmetic: true}
history:
  year: 1996
  people: [Willy Dorfler]
  note: Dorfler introduced the bulk criterion in 1996 and used it to give the first proof that an adaptive finite element method converges in 2D.
prereqs: [adaptive-finite-element-method]
see_also: [afem-optimality-theorem, residual-error-estimator, newest-vertex-bisection, quickselect, median-of-medians, bucket-sort, partial-sorting]
sources:
  - paper: doi:10.1137/0733054
    title: Willy Dorfler, A convergent adaptive algorithm for Poisson's equation, SIAM Journal on Numerical Analysis 33(3) (1996) 1106-1124
    locator: the marking criterion and the error reduction proof
  - paper: doi:10.1090/mcom/3553
    title: Carl-Martin Pfeiler and Dirk Praetorius, Dorfler marking with minimal cardinality is a linear complexity problem, Mathematics of Computation 89(326) (2020) 2735-2752
    locator: the linear time algorithm for a minimal Dorfler set and its cost analysis
  - paper: doi:10.1007/s10208-005-0183-0
    title: Rob Stevenson, Optimality of a standard adaptive finite element method, Foundations of Computational Mathematics 7(2) (2007) 245-269
    locator: the marking by binning, linear cost with a set at most twice the minimal size, and the optimality proof
  - paper: doi:10.1137/07069047X
    title: J. Manuel Cascon, Christian Kreuzer, Ricardo H. Nochetto and Kunibert G. Siebert, Quasi-optimal convergence rate for an adaptive finite element method, SIAM Journal on Numerical Analysis 46(5) (2008) 2524-2550
    locator: the contraction with Dorfler marking, and the optimal marking lemma with its threshold on theta
---

Dorfler marking, also called bulk marking, is the MARK step of the [adaptive finite element method](/adaptive-finite-element-method/). Given squared error indicators $\eta_K^2$ and a parameter $\theta \in (0, 1]$, it marks a set $\mathcal{M}$ of elements with $\sum_{K \in \mathcal{M}}\eta_K^2 \ge \theta\sum_K\eta_K^2$, and among all such sets it takes one of the smallest size. So the marked elements carry a fixed share of the estimated error. This one inequality is what the convergence proofs need: with it, the error plus a multiple of the estimator contracts by a fixed factor in each step. With a small $\theta$ and a set of minimal size, the loop also reaches the optimal rate of the [AFEM optimality theorem](/afem-optimality-theorem/). The obvious implementation sorts the indicators. A partition around pivots, as in [quickselect](/quickselect/), finds a minimal set in expected linear time.

## In plain words

Each element has a number that says how much error it holds. Put the elements in order from the largest number to the smallest. Take elements from the top of the list until the ones you took hold at least a fixed share of the total, for example half of it. Those are the elements to refine. If a few elements hold most of the error, as near a corner singularity, only a few are marked. If the error is spread evenly, many are marked, and the refinement is close to uniform. A faster method gets the same answer without sorting the whole list, by splitting it around one value at a time and keeping only the part that holds the cut.

## The problem

**Input.** Numbers $\eta_1^2, \ldots, \eta_M^2 \ge 0$, one for each element, and $\theta \in (0, 1]$.

**Output.** A set $\mathcal{M} \subseteq \{1, \ldots, M\}$ with $\sum_{K \in \mathcal{M}}\eta_K^2 \ge \theta\sum_{K = 1}^M\eta_K^2$ (the bulk criterion, also called the Dorfler property) and with the smallest size among all nonempty sets with this property. The minimal size is unique. The set itself is unique only when there are no ties at the cut.

## The algorithm

DORFLER-SORT is the direct method. DORFLER-SELECT keeps a candidate list and splits it around a random pivot value. The answer is a prefix of the sorted list, so the procedure only needs to find where the prefix ends.

```pseudo id=main
DORFLER-SORT(eta2, theta)
L1  goal <- theta * sum(eta2)
L2  order <- the indices sorted by eta2, largest first
L3  M <- empty; acc <- 0
L4  for each t in order, while acc < goal or M is empty do
L5      add t to M; acc <- acc + eta2[t]
L6  return M

DORFLER-SELECT(eta2, theta)
L7  goal <- theta * sum(eta2); M <- empty
L8  cand <- all indices
L9  while cand is not empty do
L10     p <- eta2[t] for a random t in cand                ▷ the pivot value
L11     split cand into high (> p), equal (= p) and low (< p)
L12     sh <- sum of eta2 over high
L13     if high is not empty and sh >= goal then cand <- high; continue    ▷ the cut is inside high
L14     if sh + sum over equal >= goal then return M + high + enough of equal to reach goal
L15     M <- M + high + equal; goal <- goal - sh - sum over equal; cand <- low
L16 return M                                               ▷ not reached
```

Line L14 may take the elements of equal in any order, because they all have the same value.

## Example

Take seven elements with $\eta^2 = (4, 1, 9, 2, 6, 3, 5)$, numbered 0 to 6. The total is 30.

**With $\theta = \tfrac12$**, the goal is 15. DORFLER-SORT takes element 2 (value 9, sum 9) and element 4 (value 6, sum 15). The sum reaches 15, so $\mathcal{M} = \{2, 4\}$. No single element has 15, so two is the minimal size.

DORFLER-SELECT with the pivots 4 and then 6 runs as follows.

| Pass | cand | Pivot | high | equal | low | $s_h$ | Line | Action |
|---|---|---|---|---|---|---|---|---|
| 1 | all 7 | 4 | {2, 4, 6} | {0} | {1, 3, 5} | 20 | L13 | $20 \ge 15$, so cand $\leftarrow$ {2, 4, 6} |
| 2 | {2, 4, 6} | 6 | {2} | {4} | {6} | 9 | L14 | $9 + 6 \ge 15$, return {2, 4} |

**With $\theta = \tfrac45$**, the goal is 24. In pass 1 with pivot 4, $s_h = 20 < 24$ and $s_h + 4 = 24 \ge 24$, so line L14 returns {2, 4, 6, 0}, the four largest. DORFLER-SORT gives the same set. The test file checks both procedures on these inputs and on 300 random inputs with Fraction values against a search over all subsets.

**Effect in the loop.** On the L-shaped domain with $\theta = 0.5$, the [AFEM](/adaptive-finite-element-method/) reference run marks mostly triangles near the reentrant corner, and its error falls like $N^{-1/2}$ in the number $N$ of unknowns. With $\theta = 1$ every triangle is marked, the loop is uniform refinement, and the error falls only like $N^{-1/3}$.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). An exchange argument shows that among all sets of size $L$, the $L$ largest indicators have the largest sum. So the minimal size $L^*$ is the length of the shortest prefix of the sorted list that reaches the goal, and DORFLER-SORT returns that prefix. For DORFLER-SELECT, the invariant is that marked is a prefix of some descending order, cand is the block right after it, goal is what marked still lacks, and the end of the shortest bulk prefix lies inside cand. Each of the three cases at lines L13 to L15 keeps the invariant and makes cand smaller, and line L14 returns exactly the shortest bulk prefix.

## Complexity

DORFLER-SORT costs $\Theta(M\log M)$ comparisons in the worst case for the sort and $\Theta(M)$ for the scan. DORFLER-SELECT costs $\Theta(M)$ expected time in the real-RAM model: one pass is linear in the size of cand, and a random pivot makes the expected size of the next cand at most $\tfrac34$ of the current one, so the expected total is at most $16M$ operations. Its worst case is $\Theta(M^2)$, with bad pivots every time. A median of medians pivot gives worst-case linear time, and Pfeiler and Praetorius proved that marking with minimal size is a linear time problem. Both procedures need $\Theta(M)$ extra memory.

In the adaptive loop the cost of marking is small next to the solve. The sort is often fast enough in practice. The linear methods matter when the theory counts every step, as in proofs that the whole loop has optimal cost.

## Properties

- **Minimal size.** The output has the smallest size among all bulk sets. The optimality theorem allows a set up to a constant factor larger than the minimum.
- **Largest values.** Every marked indicator is at least as large as every unmarked one.
- **Monotone in theta.** A larger $\theta$ never gives a smaller set.
- **Extremes.** $\theta = 1$ marks every element with a nonzero indicator (and at least one element), and a small $\theta$ marks the few largest.
- **Contraction.** With an exact solve, [newest vertex bisection](/newest-vertex-bisection/) and the [residual estimator](/residual-error-estimator/), Dorfler marking gives $|||u - U_{k+1}|||^2 + \gamma\eta_{k+1}^2 \le \alpha^2(|||u - U_k|||^2 + \gamma\eta_k^2)$ with $\alpha < 1$ for every $\theta \in (0, 1]$.
- **Optimal marking lemma.** The converse also holds. If a refinement reduces the total error by a fixed factor, then the refined elements satisfy the bulk criterion for every $\theta$ below a threshold $\theta_*$ that depends on the stability and discrete reliability constants. This is why the optimality theorem needs a small $\theta$.

## Variants and improvements

- **Binning.** Stevenson puts the indicators into bins by powers of 2 of their size relative to the largest one and takes whole bins from the top. This costs linear time and gives a bulk set at most twice the minimal size, which the optimality theorem allows.
- **Maximum strategy.** Mark every $K$ with $\eta_K \ge \theta\max_{K'}\eta_{K'}$. It needs no sort and often works well, but it does not satisfy the bulk criterion in general, and the classical rate proofs do not cover it.
- **Marking for oscillation.** Morin, Nochetto and Siebert (2000) also marked by the data oscillation with a second bulk criterion. Cascon, Kreuzer, Nochetto and Siebert showed this is not needed for the model problem.
- **Separate marking for hp.** For [hp-FEM](/hp-finite-element-method/), the marked elements are then split between h and p refinement by a smoothness test.
- **Goal-oriented marking.** With a primal and a dual estimator, one marks a bulk set for each, or for their product, and takes the smaller set. The rates are then proved for the goal error.

## When to use it

Use Dorfler marking in any adaptive loop where a convergence guarantee matters, and whenever the code should follow the theory of rates. It is also the safe default in practice: it adapts the number of marked elements to how concentrated the error is. When the indicators come from the [Zienkiewicz-Zhu estimator](/zienkiewicz-zhu-estimator/) or the [dual weighted residual method](/dual-weighted-residual-method/), the same rule applies, but the convergence theory is less complete.

## Pitfalls

- **Squares, not norms.** The criterion sums the squared indicators $\eta_K^2$. Summing $\eta_K$ gives a different set and is not what the proofs use.
- **Theta near 1.** A large $\theta$ marks almost everything and loses the point of adaptivity. The optimality theorem needs $\theta < \theta_*$, and $\theta_*$ is not known in practice. Values from 0.25 to 0.6 are common, and they are a rule of thumb.
- **Floating point at the cut.** In floating point, two procedures that add the values in different orders can disagree by one element when the sum is very close to the goal. Use exact arithmetic in tests, as the test file does with Fraction values.
- **All zero indicators.** If all indicators are 0, the goal is 0 and any single element satisfies the criterion. The loop should stop before this, because the estimator is already 0.
- **Ties.** With ties at the cut, the minimal set is not unique. Code that depends on a particular choice, for example in a parallel run, needs a fixed rule for ties.

## Implementations

## History

Willy Dorfler introduced the criterion in 1996, in the first proof that an adaptive finite element method for Poisson's equation in 2D reduces the error by a fixed factor in each step. His proof needed a fine enough initial mesh to resolve the data. Pedro Morin, Ricardo Nochetto and Kunibert Siebert removed this condition in 2000. Peter Binev, Wolfgang Dahmen and Ronald DeVore in 2004, and Rob Stevenson in 2007, used bulk marking in the first proofs of optimal rates, and Stevenson gave the binning method with linear cost. Manuel Cascon, Christian Kreuzer, Nochetto and Siebert proved the optimal marking lemma in 2008. Carl-Martin Pfeiler and Dirk Praetorius showed in 2020 that a set of exactly minimal size can be found in linear time.

## References
