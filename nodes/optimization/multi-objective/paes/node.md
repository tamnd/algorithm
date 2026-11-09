---
tag: J8DPVZ
kind: algorithm
slug: paes
name: PAES
aliases:
- Pareto archived evolution strategy
- (1+1)-PAES
area: optimization/multi-objective
level: advanced
summary: A (1+1) evolution strategy for several objectives. A bounded archive of non-dominated points and an adaptive grid decide whether the mutant replaces the current solution.
solves: [multi-objective-optimization]
model: real-ram
complexity:
  vars: {T: the number of steps, M: the archive bound, p: the number of objectives, n: the length of a solution vector, c: the cost of one evaluation of f}
  time: {worst: O(T (p M + n + c))}
  space: {extra: O(M (n + p))}
properties: {deterministic: false, iterative: true, population: false, elitist: true}
history:
  year: 2000
  people: [Joshua D. Knowles, David W. Corne]
  note: Knowles and Corne presented PAES at CEC 1999 as a baseline local search for several objectives, and in Evolutionary Computation in 2000 with the (1+λ) and (μ+λ) forms.
prereqs: [evolution-strategies, pareto-dominance, local-search]
see_also: [multi-objective-evolutionary-algorithm, approximate-pareto-set, spea2, nsga-ii, multi-objective-simulated-annealing, pareto-local-search, hill-climbing, epsilon-dominance]
sources:
  - paper: doi:10.1162/106365600568167
    title: Joshua D. Knowles and David W. Corne, Approximating the nondominated front using the Pareto archived evolution strategy, Evolutionary Computation 8(2), 2000, 149-172
    locator: Section 3, the (1+1)-PAES loop, the test procedure, and the adaptive grid with l bisections per objective
  - paper: "Joshua D. Knowles and David W. Corne, The Pareto archived evolution strategy, a new baseline algorithm for Pareto multiobjective optimisation, Proceedings of the 1999 Congress on Evolutionary Computation, IEEE, 1999, 98-105"
    locator: the first presentation of PAES
---

PAES, the Pareto archived evolution strategy of Knowles and Corne (2000), is a (1+1) [evolution strategy](/evolution-strategies/) for several objectives: one current solution makes one mutant per step. A bounded archive of non-dominated points decides the acceptance. When the current solution and the mutant do not dominate each other, the one in the less crowded cell of an adaptive grid over the archive becomes the current solution. It is a [local search](/local-search/) with an archive, and it has no general guarantee to reach the [Pareto front](/pareto-front/).

## In plain words

PAES keeps one candidate and changes it a little each step. If the old candidate is better in every cost, the change is thrown away. If the new one is better in every cost, it takes over. If neither wins, PAES looks at a list of the best trade-offs found so far. A new candidate that some list member beats is thrown away. Otherwise it goes into the list, and it takes over if fewer list members sit near it than near the old one. The list has a size limit. When it is full, a new candidate gets in only if its region holds fewer members than the most crowded region, and then one member of that crowded region leaves.

## The problem

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size ($N = 1$ here), and $y = f(x)$ is the image of $x$. $M$ is the archive bound and $T$ is the number of steps.

The input is a search space $X$, the map $f : X \to \mathbb{R}^p$, a mutation on $X$, the archive bound $M$, the number $l$ of bisections of each objective for the grid, and $T$. The output is the archive: at most $M$ mutually non-dominated solutions, an approximation of the front of the [multi-objective optimization](/multi-objective-optimization/) problem, with no quality guarantee in general.

## The algorithm

```pseudo id=main
PAES(f, M, l, T)
L1  c ← a random solution with its image; A ← {c}
L2  repeat T times
L3      m ← a mutation of c, with its image
L4      if f(c) dominates f(m) then discard m
L5      else if f(m) dominates f(c) then c ← m; ARCHIVE-ADD(A, m)
L6      else if a member of A dominates f(m) then discard m
L7      else
L8          ARCHIVE-ADD(A, m)
L9          if the grid cell of m holds fewer members of A than the cell of c then c ← m
L10 return A

ARCHIVE-ADD(A, m)
L11 if a member of A weakly dominates f(m) then return
L12 remove from A each member that f(m) dominates
L13 if |A| < M then add m to A
L14 else if the cell of m holds fewer members than the most crowded cell then remove a member of a most crowded cell and add m
```

The grid splits the range of each objective into $2^l$ equal parts, so it has $2^{l p}$ cells. Knowles and Corne take the range over the archive and recompute it when a new point falls outside; the implementation recomputes it at each call over the archive and the new point (and $c$ in line L9). The cell count of line L9 is taken after line L8. Line L14 removes a random member of a most crowded cell. Some descriptions add the mutant in line L5 without the test of line L11; with the test the archive stays non-dominated.

## Example

Let $M = 4$, $l = 1$, and let the archive be $(0, 8), (2, 6), (3, 5), (8, 0)$ with $c = (3, 5)$. The mutant is $m = (6, 1)$.

- **Line L4 and L5.** Neither of $(3, 5)$ and $(6, 1)$ dominates the other.
- **Line L6.** No archive member dominates $(6, 1)$; $(8, 0)$ is worse in the first objective.
- **Line L8.** No member weakly dominates $m$, and $m$ dominates none, so the archive stays full. Both objectives have range $[0, 8]$ and one bisection at $4$. The cells are $(0, 1)$ for $(0, 8)$, $(2, 6)$ and $(3, 5)$, and $(1, 0)$ for $(8, 0)$ and $m$. The cell of $m$ holds $1$ member and the most crowded cell holds $3$, so line L14 removes one of the three upper-left points at random and adds $m$.
- **Line L9.** Now the cell of $m$ holds $2$ members, and the cell of $c$ holds $2$ or $3$. It is not fewer, so $c$ stays $(3, 5)$.

A mutant $(1, 7)$ instead would fall in the cell with $3$ members, the most crowded one, and would not enter the full archive. A mutant $(1, 5)$ would dominate $(2, 6)$ and $(3, 5)$; line L12 removes both and line L13 adds it.

## Correctness

PAES has no guarantee to reach the front of a general problem; the proof covers the archive. Lines L11 to L14 keep the archive mutually non-dominated, with distinct images and at most $M$ members. If the bound is never reached, the archive images after each step are exactly the non-dominated images of all points evaluated: a discarded mutant is dominated by $c$ or by an archive member, both evaluated, and an added one is the standard elitist update. The current solution never moves to a point that it dominates. A replacement in line L14 takes a member from a most crowded cell, so in the grid of that step the largest count does not grow. The full proof is below.

## Complexity

- **One step.** The dominance tests of lines L4 to L6 and L11 to L12 cost $O(p M)$. The grid costs $O(p M)$ for the ranges and the cells, and the counts take $O(M)$ with a hash map. The mutation costs $O(n)$ and the evaluation $c$.

The total is $O(T (p M + n + c))$ time and $O(M (n + p))$ space. The grid has $2^{l p}$ cells, but only the occupied cells are stored.

## Properties

- **Single-point search.** One current solution, one mutant per step: a local search with a memory of the front.
- **Elitist archive.** The archive is the front of all points evaluated while the bound is not reached, and is non-dominated and bounded always.
- **No niche radius.** The grid adapts to the range of the archive; the parameter is the number $l$ of bisections.
- **Bounded cost per step.** $O(p M)$ plus the evaluation, linear in the archive size.
- **Scale.** Dominance does not change under increasing transforms of each objective. The grid uses equal parts of each range, so it does not change under positive affine transforms of each objective, but it does change under nonlinear ones.

## Variants and improvements

- **(1+λ) and (μ+λ)-PAES.** Knowles and Corne also give forms with $\lambda$ mutants per step and $\mu$ current solutions, selected by dominance and grid crowding.
- **PESA and PESA-II.** Corne, Knowles and Oates (2000) and Corne, Jerram, Knowles and Oates (2001) use a population and select parents from the archive by grid cell, in PESA-II by cell rather than by point.
- **Box archives.** The [epsilon-dominance](/epsilon-dominance/) archive of Laumanns, Thiele, Deb and Zitzler bounds the archive size and its coverage at once; see [approximate Pareto set](/approximate-pareto-set/).
- **Annealing acceptance.** [Multi-objective simulated annealing](/multi-objective-simulated-annealing/) accepts a worse mutant with a probability instead of rejecting it.
- **Complete neighbourhoods.** [Pareto local search](/pareto-local-search/) explores the whole neighbourhood of each archive member instead of one random mutant.

## When to use it

Use PAES as a baseline local search for several objectives, when evaluations are expensive and a population is not wanted, or as the local part of a memetic method. Its cost per step is small. Knowles and Corne (2000) reported comparisons with population-based methods of the time on test functions; these are measured results on those instances and settings.

## Pitfalls

- **Local optima.** A single current solution that only moves to points it does not dominate can stay in a region where no mutant is accepted.
- **Bounded archive is not monotone.** After a removal in line L14, a later archive can hold a point that the removed member dominated.
- **Grid resolution.** With $l$ too small, all members share few cells and crowding gives little information; with $l$ too large, each member has its own cell and all counts are $1$.
- **Grid moves.** The cells change when the range changes, so a point near a cell border can change cell between steps.
- **Archive test in line L5.** Adding a mutant that dominates $c$ without the test of line L11 can put a dominated point in the archive.

## Implementations

## History

Knowles and Corne presented PAES at CEC 1999 as a simple baseline for multi-objective search, motivated by local search for off-line routing in telecommunication networks. The journal version in 2000 gave the adaptive grid in detail and the population forms. The grid archive was reused in PESA (2000) and PESA-II (2001), and Knowles and Corne later studied the properties of grid-based archivers.

## References
