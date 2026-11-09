---
tag: H04GPP
kind: algorithm
slug: npga
name: NPGA
aliases:
- niched Pareto genetic algorithm
- niched Pareto GA
area: optimization/multi-objective
level: advanced
summary: The genetic algorithm of Horn, Nafpliotis and Goldberg (1994). Two candidates are tested for dominance against a random comparison set; on a tie, the one with the smaller niche count wins.
solves: [multi-objective-optimization]
model: real-ram
complexity:
  vars: {N: the population size, p: the number of objectives, g: the number of generations, n: the length of a solution vector, c: the cost of one evaluation of f}
  time: {worst: O(g (p N^2 + N (n + c)))}
  space: {extra: O(N (n + p))}
properties: {deterministic: false, iterative: true, population: true, elitist: false}
history:
  year: 1994
  people: [Jeffrey Horn, Nicholas Nafpliotis, David E. Goldberg]
  note: Horn, Nafpliotis and Goldberg presented NPGA at the first IEEE Conference on Evolutionary Computation in 1994. Erickson, Mayer and Horn gave NPGA2, with tournaments on Pareto ranks, in 2001.
prereqs: [pareto-dominance, tournament-selection, genetic-algorithm]
see_also: [moga, vega, nsga-ii, pareto-ranking, multi-objective-evolutionary-algorithm, crowding-distance]
sources:
  - paper: doi:10.1109/ICEC.1994.350037
    title: Jeffrey Horn, Nicholas Nafpliotis and David E. Goldberg, A niched Pareto genetic algorithm for multiobjective optimization, Proceedings of the First IEEE Conference on Evolutionary Computation, IEEE World Congress on Computational Intelligence, volume 1, 1994, 82-87
    locator: the Pareto domination tournament with a comparison set of size t_dom, and the use of equivalence class sharing
  - paper: "Christopher K. Oei, David E. Goldberg and Shau-Jin Chang, Tournament selection, niching, and the preservation of diversity, IlliGAL Report 91011, University of Illinois at Urbana-Champaign, 1991"
    locator: continuously updated fitness sharing with tournament selection
  - book: isbn:9780471873396
    title: Kalyanmoy Deb, Multi-Objective Optimization Using Evolutionary Algorithms, Wiley, 2001
    locator: Chapter 5, the niched Pareto genetic algorithm with a worked example
  - paper: "Mark Erickson, Alex Mayer and Jeffrey Horn, The niched Pareto genetic algorithm 2 applied to the design of groundwater remediation systems, Evolutionary Multi-Criterion Optimization (EMO 2001), LNCS 1993, Springer, 2001, 681-695"
    locator: NPGA2, tournaments on Pareto ranks with sharing
---

NPGA, the niched Pareto genetic algorithm of Horn, Nafpliotis and Goldberg (1994), is a [genetic algorithm](/genetic-algorithm/) whose selection is a Pareto domination [tournament](/tournament-selection/). Two candidates are tested against a random comparison set of $t$ members: if exactly one of them is dominated by the set, the other wins; otherwise the candidate in the less crowded part of the objective space wins. It needs no rank for the whole population, but it has two parameters, $t$ and the niche radius $\sigma$, and no elitism.

## In plain words

To pick each parent, NPGA holds a small contest. It draws two candidates and a random panel of judges from the population. A candidate fails if some judge beats it in every cost at once.

If one candidate fails and the other passes, the one that passes becomes a parent. If both pass, or both fail, the panel cannot decide. Then NPGA looks at the parents chosen so far and picks the candidate whose kind of trade-off is rarer among them. This keeps the parents spread along the front.

A bigger panel finds more weak candidates but costs more and pushes harder toward the current best. A smaller panel is cheaper and lets more weak candidates through.

## The problem

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size, and $y = f(x)$ is the image of $x$.

The input is a search space $X$, the map $f : X \to \mathbb{R}^p$, the population size $N$, the size $t$ of the comparison set, a niche radius $\sigma$ in the normalized objective space, and a number $g$ of generations. The output is a set of mutually non-dominated solutions, an approximation of the front of the [multi-objective optimization](/multi-objective-optimization/) problem, with no quality guarantee.

## The algorithm

```pseudo id=main
NPGA(f, N, t, σ, g)
L1  P ← N random solutions, each with its image f(x)
L2  repeat g times
L3      M ← an empty mating pool
L4      while |M| < N do
L5          pick candidates a and b, and a comparison set C of t members, at random from P
L6          da ← some member of C dominates a;  db ← some member of C dominates b
L7          if da and not db then append b to M
L8          else if db and not da then append a to M
L9          else append the candidate with the smaller niche count over M (a tie at random)
L10     P ← offspring of M by crossover and mutation
L11 return the members of P that no member of P dominates
```

The niche count of line L9 is $m(x) = \sum_{z \in M} \mathrm{sh}(d(f(x), f(z)))$ with $\mathrm{sh}(d) = 1 - d/\sigma$ for $d < \sigma$ and $0$ otherwise, and $d$ is the Euclidean distance after each objective is divided by its range in the population. It is taken over the pool $M$ being built, not over $P$: this is the continuously updated sharing that Oei, Goldberg and Chang (1991) proposed for tournament selection. The implementation draws $C$ without replacement from all of $P$.

## Example

Take the eight images of the [non-dominated sorting](/non-dominated-sorting/) page, $A = (1, 8)$, $B = (2, 5)$, $C = (3, 6)$, $D = (4, 2)$, $E = (5, 4)$, $F = (6, 7)$, $G = (7, 1)$, $H = (8, 3)$, and $t = 2$.

- **Candidates $C$ and $H$, comparison set $\{B, F\}$.** $B$ dominates $C$, and neither $B$ nor $F$ dominates $H$, because $F_2 = 7 > 3$. So $H$ wins at line L8, although $H$ has two dominators in $P$ ($D$ and $G$) and $C$ has only one.
- **Candidates $A$ and $G$, comparison set $\{D, E\}$.** Neither is dominated, so line L9 decides. If the pool already holds two parents near $A$ and none near $G$, then $m(G) < m(A)$ and $G$ wins.

The chance that a member with $k$ dominators is found dominated is $\pi(k, t) = 1 - \binom{N-k}{t} / \binom{N}{t}$ (Lemma 1 of the proof). With $N = 8$ and $t = 2$:

| member | dominators in $P$ | $k$ | $\pi(k, 2)$ |
|---|---|---|---|
| A, B, D, G | none | 0 | $0$ |
| C | B | 1 | $1 - 21/28 = 1/4$ |
| E | D | 1 | $1/4$ |
| H | D, G | 2 | $1 - 15/28 = 13/28$ |
| F | B, C, D, E | 4 | $1 - 6/28 = 11/14$ |

So with $t = 2$, the member $C$ passes the dominance test three times out of four.

## Correctness

NPGA has no guarantee to reach the front; the proof covers one tournament and the loop. The comparison set is a uniform random $t$-subset, so a member with $k$ dominators is found dominated with probability $1 - \binom{N-k}{t}/\binom{N}{t}$, which is $0$ for a non-dominated member and grows with $k$ and $t$. When exactly one candidate is found dominated, the other wins. With $t = N$ the test is exact, and a dominated candidate never beats a non-dominated one. Each generation fills a pool of exactly $N$ parents and makes $N$ offspring, and the output is the nonempty set of minimal members of the last population. The full proof is below.

## Complexity

- **One tournament, lines L5 to L9.** $O(p t)$ for the dominance tests and $O(p \lvert M \rvert)$ for the two niche counts.
- **One generation.** $N$ tournaments with $\lvert M \rvert < N$ cost $O(p N (t + N)) = O(p N^2)$, since $t \le N$. Variation and evaluation add $O(N (n + c))$. Line L11 costs $O(p N^2)$ once.

The total is $O(g (p N^2 + N (n + c)))$ time and $O(N (n + p))$ space. With the niche count over a fixed sample of the pool, as some codes do, a tournament costs $O(p t)$ plus the sample size.

## Properties

- **No global ranking.** Each tournament reads only $t + 2$ members for dominance.
- **Selection pressure set by $t$.** By Lemma 1, a small $t$ lets dominated members pass the test often; $t = N$ makes the test exact.
- **Not elitist.** The offspring replace the population.
- **Order dependent.** The niche counts depend on the parents already chosen, so the pool depends on the order of the tournaments.

## Variants and improvements

- **NPGA2.** Erickson, Mayer and Horn (2001) replace the dominance test against a comparison set with a comparison of the Pareto ranks of the two candidates in the whole population, and keep the niche count for ties.
- **Sharing over the population.** Some codes compute the niche count over $P$ instead of the pool, which makes the tournaments independent but loses the continuous update.
- **Elitism.** Adding an external archive of non-dominated points, as in the [MOEA template](/multi-objective-evolutionary-algorithm/), keeps the front points that the replacement loses.

## When to use it

Use NPGA when a rank of the whole population is too costly or when the population is distributed, since each tournament needs only a small sample. For most uses today, a method with elitism and a parameter-free density, such as [NSGA-II](/nsga-ii/), needs less tuning.

## Pitfalls

- **Choosing $t$.** A $t$ that is too small makes the dominance test weak, so selection is close to random among the candidates; a $t$ close to $N$ gives strong pressure and fast loss of diversity.
- **The niche radius.** As in [MOGA](/moga/), a $\sigma$ that is too small or too large makes the niche counts useless.
- **The first tournament.** The pool is empty, so both niche counts are $0$ and a tie is broken at random.
- **Unscaled objectives.** Sharing distances without normalization favor the objective with the largest range.

## Implementations

## History

Horn, Nafpliotis and Goldberg presented NPGA in 1994, the same year as NSGA of Srinivas and Deb, and one year after MOGA of Fonseca and Fleming. All three followed Goldberg's 1989 proposal to select by Pareto dominance and to keep diversity by sharing. NPGA took the tournament form and the continuously updated sharing of Oei, Goldberg and Chang (1991). NPGA2 of Erickson, Mayer and Horn (2001) moved to tournaments on Pareto ranks.

## References
