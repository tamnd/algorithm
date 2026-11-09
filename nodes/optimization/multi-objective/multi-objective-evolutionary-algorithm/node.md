---
tag: 1SG8N5
kind: technique
slug: multi-objective-evolutionary-algorithm
name: Multi-objective evolutionary algorithm
aliases:
- MOEA
- evolutionary multi-objective optimization
- EMO
area: optimization/multi-objective
level: advanced
summary: A population-based search that evolves many trade-off solutions at once, ranks them by Pareto dominance and density, and keeps the best non-dominated ones in an archive. It has no general guarantee.
prereqs: [pareto-dominance, pareto-front, genetic-algorithm, evolutionary-computation]
see_also: [nsga-ii, spea2, moea-d, nsga-iii, pareto-ranking, approximate-pareto-set, hypervolume-indicator, pareto-local-search]
sources:
  - book: isbn:9780471873396
    title: Kalyanmoy Deb, Multi-Objective Optimization Using Evolutionary Algorithms, Wiley, 2001
    locator: Chapters 5 and 6, non-elitist and elitist multi-objective evolutionary algorithms
  - book: isbn:9780387332543
    title: Carlos A. Coello Coello, Gary B. Lamont and David A. Van Veldhuizen, Evolutionary Algorithms for Solving Multi-Objective Problems, second edition, Springer, 2007
    locator: Chapter 2, the MOEA framework, archives and the survey of algorithms
  - paper: doi:10.1109/TEVC.2004.823470
    title: Marco Laumanns, Lothar Thiele and Eckart Zitzler, Running time analysis of multiobjective evolutionary algorithms on pseudo-Boolean functions, IEEE Transactions on Evolutionary Computation 8(2), 2004, 170-182
    locator: SEMO and FEMO, and their expected running times on LOTZ
  - paper: "Oliver Giel and Per Kristian Lehre, On the effect of populations in evolutionary multi-objective optimisation, Evolutionary Computation 18(3), 2010, 335-356"
    locator: the expected running time of GSEMO on OneMinMax
  - paper: "Günter Rudolph and Alexandru Agapie, Convergence properties of some multi-objective evolutionary algorithms, Proceedings of the 2000 Congress on Evolutionary Computation, IEEE, 2000, 1010-1016"
    locator: the convergence with probability one of elitist algorithms with an archive on a finite search space
  - paper: doi:10.1609/aaai.v36i9.21283
    title: Weijie Zheng, Yufei Liu and Benjamin Doerr, A first mathematical runtime analysis of the non-dominated sorting genetic algorithm II (NSGA-II), Proceedings of the AAAI Conference on Artificial Intelligence 36(9), 2022, 10408-10416
    locator: the expected running times of NSGA-II on OneMinMax and LOTZ with population size at least four times the front size
---

A multi-objective evolutionary algorithm (MOEA) is a [genetic algorithm](/genetic-algorithm/) or an [evolution strategy](/evolution-strategies/) whose population approximates the whole [Pareto front](/pareto-front/) in one run. It replaces the scalar fitness with a rank from [Pareto dominance](/pareto-dominance/), adds a density term that spreads the population along the front, and often keeps the best points found in an archive. The method is a heuristic: no general theorem says that it reaches the front, and the results that exist hold for archives and for small test functions with exact hypotheses.

## In plain words

When you have several costs, there is no single best answer but a whole family of fair trade-offs. An evolutionary algorithm keeps a crowd of candidate answers, mixes and changes them, and keeps the better ones. The multi-objective version needs two new rules.

The first rule says what better means. An answer is good when no other answer beats it in every cost at once. The second rule keeps the crowd spread out, so that it covers cheap answers, fast answers, and the many answers in between, not one small corner.

Many versions also keep a separate list of the best answers found so far, so a good answer is never forgotten. The method is a strong practical tool, but it has no promise to find every best trade-off.

## When it applies

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size, and $y = f(x)$ is the image of $x$.

Use an MOEA when:

- the objectives can be evaluated but have no useful structure, such as gradients, convexity or a linear form, so exact methods like [Benson's algorithm](/benson-algorithm/) or the [epsilon-constraint method](/epsilon-constraint-method/) with an exact solver do not apply;
- the user wants many trade-offs from one run, not one solution per [scalarization](/scalarization/);
- the front may be non-convex, where a [weighted sum](/weighted-sum-method/) misses points;
- the evaluation budget allows thousands of evaluations or more.

Do not use one when an exact method solves the problem in the time available, or when a guarantee is required: the [approximate Pareto set](/approximate-pareto-set/) schemes give one for many combinatorial problems.

## The template

The input is a solution space $X$, the map $f : X \to \mathbb{R}^p$, the population size $N$ and a budget. The output is an archive $A$ of mutually non-dominated pairs $(x, f(x))$.

```pseudo id=main
MOEA(X, f, N, budget)
L1  P ← N initial solutions, each with its image f(x)
L2  A ← the non-dominated members of P                ▷ the archive
L3  while budget remains do
L4      φ ← FITNESS(P)                               ▷ hole: dominance rank, then density
L5      M ← SELECT(P, φ)                              ▷ hole: mating selection
L6      Q ← VARY(M), each with its image f(x)         ▷ hole: crossover and mutation
L7      for each q in Q do UPDATE-ARCHIVE(A, q)
L8      P ← SURVIVE(P, Q, N)                          ▷ hole: keep N of P ∪ Q
L9  return A
```

**The holes.** Each named algorithm fills the holes in its own way.

- *Fitness, line L4.* A dominance rank from [Pareto ranking](/pareto-ranking/) or [non-dominated sorting](/non-dominated-sorting/), then a density term to break ties: fitness sharing with a niche radius ([MOGA](/moga/), [NPGA](/npga/)), the [crowding distance](/crowding-distance/) ([NSGA-II](/nsga-ii/)), the $k$-th nearest neighbor ([SPEA2](/spea2/)), reference directions ([NSGA-III](/nsga-iii/)), or a contribution to the [hypervolume](/hypervolume-indicator/). [MOEA/D](/moea-d/) replaces the rank with many scalar subproblems.
- *Selection, line L5.* Usually a binary [tournament](/tournament-selection/) on $\varphi$.
- *Variation, line L6.* The usual [crossover](/crossover/) and [mutation](/mutation/) of the representation, such as bit flips for bit strings or simulated binary crossover for real vectors.
- *Survival, line L8.* With [elitism](/elitism/), the next population is the best $N$ of $P \cup Q$, as in NSGA-II. Without it, $P \leftarrow Q$, as in VEGA, MOGA and NPGA.

**The unbounded archive.** UPDATE-ARCHIVE rejects $q$ when an archive image weakly dominates $f(q)$; otherwise it removes the members whose images $f(q)$ dominates, and adds $q$.

*Claim.* After any sequence of calls, the images in $A$ are exactly the non-dominated images among all points offered so far, with one member for each image.

*Proof.* By induction on the calls. Let $S$ be the set of images offered before $q$, and assume that the images in $A$ are the non-dominated images of $S$. If some $a \in A$ has $f(a) \le f(q)$, then $f(q)$ is dominated in $S \cup \{f(q)\}$ or equal to $f(a)$, and the set of non-dominated images does not change. Otherwise, no image of $S$ dominates $f(q)$: a dominating image of $S$ would be dominated by, or equal to, a non-dominated image of $S$, which is in $A$. So $f(q)$ is non-dominated in $S \cup \{f(q)\}$. The images of $A$ that $f(q)$ dominates stop being non-dominated, and the others stay. This is what the update does.

So the archive never loses a non-dominated image: an image leaves only when a new image dominates it. The archive can grow as large as the front, which can be exponential, as on the [approximate Pareto set](/approximate-pareto-set/) page. The [epsilon box archive](/approximate-pareto-set/) of Laumanns, Thiele, Deb and Zitzler (2002) has a size bound and still covers every point seen, within $\varepsilon$.

**Convergence on a finite space.** Let $X$ be finite, let the Pareto front have $m$ images, and assume that in each generation every $x \in X$ is in $Q$ with probability at least $q > 0$, whatever happened before. Then the unbounded archive holds the whole front after finitely many generations with probability $1$, and the expected number of generations is at most $m / q$. *Proof.* Fix one preimage of each front image. Each one is first sampled after a number of generations that is bounded by a geometric variable with mean $1/q$; once sampled, its image stays by the claim. The time until all $m$ are sampled is the maximum of $m$ such times, whose mean is at most the sum $m/q$. Standard bit mutation on $\{0,1\}^n$ gives $q \ge n^{-n}$ for each offspring, so the bound is true but useless in practice. Rudolph and Agapie (2000) proved results of this kind for several elitist schemes. The proof needs the archive: a bounded population with density-based survival can lose a front point, as Pitfalls shows.

**Running times on test functions.** The running time is the number of evaluations of $f$ until the population or archive holds one preimage of each front image. The functions are on bit strings of length $n$. LOTZ maximizes the number of leading ones and the number of trailing zeros; its front has the $n + 1$ points $1^i 0^{n-i}$. OneMinMax maximizes the number of zeros and the number of ones; each string is Pareto-optimal, and the front has $n + 1$ images.

| algorithm | function | expected running time | source |
|---|---|---|---|
| SEMO (one-bit mutation) | LOTZ | $\Theta(n^3)$ | Laumanns, Thiele and Zitzler (2004) |
| GSEMO (standard bit mutation) | LOTZ | $O(n^3)$ | Giel (2003) |
| GSEMO | OneMinMax | $O(n^2 \log n)$ | Giel and Lehre (2010) |
| NSGA-II, $N \ge 4(n+1)$ | OneMinMax | $O(N n \log n)$ | Zheng, Liu and Doerr (2022) |
| NSGA-II, $N \ge 4(n+1)$ | LOTZ | $O(N n^2)$ | Zheng, Liu and Doerr (2022) |

SEMO and GSEMO keep an unbounded population of mutually non-dominated points and pick a parent uniformly at random. The implementation of this page has GSEMO; its population is the archive.

## Classic examples

- **[VEGA](/vega/)** (Schaffer, 1985): selects a part of the mating pool by each objective in turn. The first MOEA.
- **[MOGA](/moga/)**, **[NPGA](/npga/)** and NSGA: Pareto ranks with fitness sharing, no elitism.
- **[NSGA-II](/nsga-ii/)**: non-dominated sorting, crowding distance, and elitist survival of the best $N$ of $2N$.
- **[SPEA](/spea/)** and **[SPEA2](/spea2/)**: an external archive and fitness from dominance strengths.
- **[PAES](/paes/)**: a $(1+1)$ evolution strategy with an adaptive grid archive.
- **[MOEA/D](/moea-d/)**: one scalar Tchebycheff subproblem for each weight vector, solved together with neighbor mating.
- **[NSGA-III](/nsga-iii/)**: reference directions in place of the crowding distance, for many objectives.
- Local search relatives: [multi-objective simulated annealing](/multi-objective-simulated-annealing/) and [Pareto local search](/pareto-local-search/).

## Variations

- **Indicator-based selection.** Replace the density term by the loss of an indicator, often the [hypervolume](/hypervolume-indicator/), when a point is removed. Exact hypervolume costs grow fast with $p$, see [hypervolume computation](/hypervolume-computation/).
- **Decomposition.** Solve many [scalarizations](/scalarization/) with different weights at once, as in MOEA/D.
- **Steady state.** Make one offspring per step and remove one member, as in SEMO and the epsilon-MOEA.
- **Bounded archives.** Keep at most a fixed number of members by grid density (PAES), clustering (SPEA), nearest neighbor truncation (SPEA2) or [epsilon boxes](/epsilon-dominance/).
- **Preferences.** Restrict the search to a region given by a reference point or by weights, see [preference articulation](/preference-articulation/).

## Pitfalls

- **Bounded archives can deteriorate.** Take an archive of at most three points that drops the inner point with the smallest crowding distance, start with $(0, 10)$ and $(10, 0)$, and offer $(4, 1)$, $(2, 4)$, $(4, 3)$. After $(2, 4)$ the four points $(0, 10)$, $(2, 4)$, $(4, 1)$, $(10, 0)$ have inner distances $13/10$ and $12/10$, so $(4, 1)$ is dropped. Then $(4, 3)$ is non-dominated in the archive, and the inner distances are $11/10$ for $(2, 4)$ and $12/10$ for $(4, 3)$, so $(2, 4)$ is dropped. The archive ends as $\{(0, 10), (4, 3), (10, 0)\}$, and $(4, 3)$ is dominated by $(4, 1)$, found earlier.
- **No general claims of superiority.** Published comparisons report the authors' measured results on their test sets, budgets and parameter settings. The [no free lunch theorem](/no-free-lunch-theorem/) rules out a method that is better on all problems.
- **Many objectives.** For random points the expected number of non-dominated points out of $N$ is $\Theta(\ln^{p-1} N)$ for fixed $p$, and the constants grow fast with $p$. With $p \ge 4$, most of a population is often non-dominated, the rank carries little information, and the density term decides almost everything.
- **Scaling.** Density terms such as distances depend on the units of the objectives. Normalize by the ranges or by the [ideal](/ideal-point/) and [nadir](/nadir-point/) points.
- **The returned set.** Return the archive or the first front of the final population, and check feasibility for constrained problems. The final population can hold dominated points.

## Exercises

1. Show that the unbounded archive is independent of the order in which the points are offered, up to the choice of one member per image. *Answer:* by the claim, its images are always the non-dominated images of all points offered.
2. For OneMinMax with $n = 3$, list the front, and show that it has $n + 1$ images although all $2^n$ strings are Pareto-optimal.
3. Give an example with $p = 2$ in which the survival "keep the best $N$ of $P \cup Q$ by front number, ties broken at random" removes a point of the first front. *Answer:* any case where the first front of $P \cup Q$ has more than $N$ points.

## References
