---
tag: P2XYTJ
kind: algorithm
slug: memetic-algorithm
name: Memetic algorithm
aliases:
- hybrid genetic algorithm
- MA
- genetic local search
area: optimization/metaheuristics
level: advanced
summary: A genetic algorithm in which each child is improved by local search before it joins the population. Recombination moves between local optima, and local search makes each child locally optimal.
solves: [traveling-salesman-problem]
model: real-ram
complexity:
  vars: {n: the number of cities, N: the population size, T: the number of steps, I: the number of 2-opt passes in one local search}
  time: {worst: O((N + T) I n^2 + T N n)}
  space: {extra: O(N n + n^2)}
properties: {deterministic: false, iterative: true, anytime: true, population: true}
history:
  year: 1989
  people: [Pablo Moscato]
  note: Moscato named and described memetic algorithms in a 1989 Caltech report, after the word meme of Dawkins. Earlier and parallel work joined genetic algorithms with local search for the traveling salesman problem.
prereqs: [genetic-algorithm, local-search]
see_also: [two-opt, crossover, iterated-local-search, scatter-search, path-relinking, lin-kernighan, held-karp-algorithm, premature-convergence]
sources:
  - paper: Pablo Moscato, On evolution, search, optimization, genetic algorithms and martial arts, towards memetic algorithms, Caltech Concurrent Computation Program, Report 826, 1989
    title: On evolution, search, optimization, genetic algorithms and martial arts, towards memetic algorithms
    locator: the whole report (the name memetic algorithm and the population of locally optimized solutions)
  - paper: doi:10.1109/TEVC.2005.850260
    title: Natalio Krasnogor and Jim Smith, A tutorial for competent memetic algorithms, model, taxonomy, and design issues, IEEE Transactions on Evolutionary Computation 9(5), 2005
    locator: pages 474 to 488 (the general template, Lamarckian and Baldwinian learning, and the design choices)
  - paper: Peter Merz and Bernd Freisleben, Memetic algorithms for the traveling salesman problem, Complex Systems 13(4), 2001
    title: Memetic algorithms for the traveling salesman problem
    locator: pages 297 to 345 (memetic algorithms with 2-opt and Lin-Kernighan local search and special crossovers for the TSP)
  - book: doi:10.1007/978-3-642-23247-3
    title: Ferrante Neri, Carlos Cotta and Pablo Moscato (editors), Handbook of Memetic Algorithms, Springer, 2012
    locator: Chapter 1 (basic concepts and history) and Chapter 9 (memetic algorithms for combinatorial problems)
  - paper: doi:10.1007/3-540-58484-6_245
    title: Darrell Whitley, V. Scott Gordon and Keith Mathias, Lamarckian evolution, the Baldwin effect and function optimization, Parallel Problem Solving from Nature III, LNCS 866, 1994
    locator: pages 5 to 15 (Lamarckian and Baldwinian use of local search, compared on test functions)
  - paper: doi:10.1007/s00453-013-9801-4
    title: Matthias Englert, Heiko Röglin and Berthold Vöcking, Worst case and probabilistic analysis of the 2-Opt algorithm for the TSP, Algorithmica 68(1), 2014
    locator: pages 190 to 264 (instances in the Euclidean plane on which 2-opt can make exponentially many moves)
---

A memetic algorithm (MA) is a [genetic algorithm](/genetic-algorithm/) in which every new solution is improved by [local search](/local-search/) before it joins the population. Recombination puts together parts of two good solutions, and local search then moves the child to a nearby local optimum, so the population consists of local optima only. In the Lamarckian form the improved solution replaces the child. In the Baldwinian form only its improved fitness is kept. On the [traveling salesman problem](/traveling-salesman-problem/), memetic algorithms with strong local search are among the best heuristic methods, and this page shows a simple steady-state version with [2-opt](/two-opt/). Like other metaheuristics, it gives no certificate of optimality and no useful bound on the time to the optimum.

## In plain words

Keep a small group of good tours. Every tour in the group is as good as small repairs can make it: no swap of two edges makes it shorter.

At each step, pick two tours from the group and make a child that keeps a piece of the first tour and takes the other cities in the order of the second. Sometimes swap two cities of the child. Then repair the child with the same small repairs until it cannot get shorter. If the repaired child is shorter than the worst tour of the group and is not already in the group, it takes the place of the worst tour. Repeat for a fixed number of steps and return the shortest tour of the group.

## The problem

The input is a symmetric [traveling salesman problem](/traveling-salesman-problem/) with $n \ge 4$ cities and distances $d_{ij} = d_{ji}$. A tour is a cyclic order of the cities, and its length $L$ is the sum of the distances of its $n$ edges. The goal is a short tour. The parameters are the population size $N \ge 2$, the number of steps $T$ and the mutation probability $p_m$.

The template works for any problem with a crossover and a local search, such as graph coloring, quadratic assignment and scheduling. The TSP version shows all parts.

## The algorithm

Three parts come from other pages: order crossover (OX), a [crossover](/crossover/) for permutations, the swap mutation, and 2-opt local search. A 2-opt move removes two edges $\{a, b\}$ and $\{c, d\}$ of the tour and adds $\{a, c\}$ and $\{b, d\}$, which reverses the part of the tour between them. Its change of length is $d_{ac} + d_{bd} - d_{ab} - d_{cd}$. The local search applies improving moves until there is none, so the result is **2-opt optimal**.

```pseudo id=main
MA(d, N, T, p_m)
L1  P ← N random tours, each improved by 2-opt
L2  for s ← 1 to T do
L3      choose two different tours a, b of P uniformly at random
L4      c ← OX(a, b) with a random segment
L5      with probability p_m, swap two random cities of c        ▷ mutation
L6      c ← 2-opt(c)                                             ▷ Lamarckian local search
L7      w ← a longest tour of P
L8      if L(c) < L(w) and c is not in P then replace w by c     ▷ steady state
L9  return a shortest tour of P
```

**Order crossover.** OX with segment $i..j$ copies positions $i$ to $j$ from $a$. It fills the other positions, starting after $j$ and wrapping around, with the missing cities in the order in which they occur in $b$, also starting after position $j$. The child is always a permutation.

**The duplicate test.** Line L8 compares tours as cycles: two tours are equal if one is a rotation or a reversal of the other. The test keeps the population from filling with copies of one tour, which is a main cause of [premature convergence](/premature-convergence/) in steady-state methods.

## Example

Take 6 cities on a $2 \times 1$ grid: $1 = (0,0)$, $2 = (1,0)$, $3 = (2,0)$, $4 = (2,1)$, $5 = (1,1)$ and $6 = (0,1)$, with Euclidean distances. The optimal tour 1 2 3 4 5 6 goes around the border and has length 6. Take the parents

- $a$ = 1 2 5 4 3 6, with length $5 + \sqrt 5 \approx 7.236$, and
- $b$ = 1 5 2 3 4 6, with length $6 + \sqrt 2 \approx 7.414$.

**Crossover.** OX with the segment of positions 2 to 3 keeps 2 5 from $a$. The order of $b$ from position 4 on, wrapping around, is 3 4 6 1 5 2. Without 2 and 5 it is 3 4 6 1, and these cities fill positions 4, 5, 6 and 1. The child is $c$ = 1 2 5 3 4 6, with length $6 + \sqrt 2 \approx 7.414$.

**Local search.** First-improvement 2-opt scans the moves and finds that removing the edges $\{2, 5\}$ and $\{4, 6\}$, of total length 3, and adding $\{2, 4\}$ and $\{5, 6\}$, of total length $\sqrt 2 + 1$, saves $2 - \sqrt 2 \approx 0.586$. The tour becomes 1 2 4 3 5 6, with length $4 + 2\sqrt 2 \approx 6.828$. The next improving move removes $\{2, 4\}$ and $\{3, 5\}$, of total length $2\sqrt 2$, and adds $\{2, 3\}$ and $\{4, 5\}$, of total length 2. The tour becomes 1 2 3 4 5 6, with length 6, and no move improves it.

Neither parent is 2-opt optimal, so they could not be in the population of this page, and they are used here only to show the two roles in a small case. Crossover keeps edges of both parents: $\{1, 2\}$ and $\{2, 5\}$ of $a$, $\{3, 4\}$ and $\{6, 1\}$ of both, and $\{4, 6\}$ of $b$. Only $\{5, 3\}$ is new. Local search then removes the bad edges that crossover left.

## Correctness

A memetic algorithm cannot certify that its best tour is optimal. Its correctness consists of these invariants. The proofs are below.

- **Valid tours.** OX, the swap and every 2-opt move map permutations to permutations, so every tour in $P$ visits each city once.
- **Local optimality.** Every tour in $P$ is 2-opt optimal, since line L1 and line L6 end with 2-opt and the improved tour is the one stored. 2-opt stops because each move shortens the tour and there are finitely many tours.
- **Monotone population.** Line L8 only replaces a longest tour by a strictly shorter one. So for each $r$, the $r$-th smallest length in $P$ never increases, and in particular the best length never increases.
- **Diversity.** A tour enters $P$ only if it is not already in $P$, so the number of distinct tours in $P$ never decreases.
- **No convergence guarantee.** This variant does not always reach the optimum, even with $T \to \infty$: the swap mutation and 2-opt cannot reach every tour from every population. If line L5 instead replaces $c$ by a uniform random tour with some probability $p_r > 0$, the optimum is created with probability at least $2 p_r / (n-1)!$ in each step, and the best length reaches $L^*$ with probability 1.

## Complexity

One pass of 2-opt checks $O(n^2)$ moves with $O(1)$ work each, and applies an improving move in $O(n)$. If one local search needs at most $I$ passes, it costs $O(I n^2)$. Line L1 runs $N$ local searches, and each step runs one local search, an $O(n)$ crossover and an $O(N n)$ duplicate test and worst search. The total is $O((N + T) I n^2 + T N n)$ time and $O(N n + n^2)$ space with the distance matrix. The number of passes $I$ has no polynomial bound in the worst case: Englert, Röglin and Vöcking (2014) built Euclidean instances in the plane on which 2-opt can make exponentially many moves. On random instances it is small in practice. Neighbor lists and don't-look bits make a 2-opt pass much faster than $O(n^2)$ on large instances.

## Properties

- **A population of local optima.** Each member is locally optimal, so the search moves from local optimum to local optimum. This differs from a plain genetic algorithm, whose members are mostly not locally optimal.
- **Anytime.** The best tour of $P$ is always available, and its length never increases.
- **Few, costly evaluations.** Each step costs one local search, so the population and the number of steps are much smaller than in a plain genetic algorithm.
- **Randomized.** Results vary from run to run, and fixed seeds give repeatable runs.

## Variants and improvements

- **Baldwinian learning.** The child keeps its own genes, but its fitness is the length after local search. Lamarckian learning, used here, writes the improved tour back.
- **Stronger local search.** 3-opt, Or-opt or [Lin-Kernighan](/lin-kernighan/) in place of 2-opt. Most strong MA results on the TSP use Lin-Kernighan.
- **Problem-specific crossover.** For the TSP, edge recombination, distance-preserving crossover and edge assembly crossover keep more edges of the parents than OX does.
- **Partial local search.** Improve only some children, or stop the local search early, to save time on large problems.
- **Generational form.** Replace the whole population each generation, with [elitism](/elitism/), instead of one tour per step.
- **Adaptive and multimeme algorithms.** Choose among several local searches during the run, based on their past success.
- **Related methods.** [Iterated local search](/iterated-local-search/) keeps one local optimum and perturbs it. [Scatter search](/scatter-search/) and [path relinking](/path-relinking/) also combine good solutions and improve the results, with deterministic rules.

## When to use it

Use a memetic algorithm when a good local search exists for the problem and you want to combine local optima. For the TSP, compare with the best specialized codes before you choose it: exact solvers prove optimality on many large instances, and Lin-Kernighan based local search alone gives very good tours. Choose by measurements on your own instances, with the same time limit for each method. If the local search alone already finds the optimum from most starts, as on the small random instances of the test file, the population adds little.

## Pitfalls

- **Loss of diversity.** Local search maps many children to the same local optima, so the population can fill with copies. Keep the duplicate test of line L8, or measure the distance between tours.
- **Too much local search.** A full local search on every child can take most of the time. Measure its cost, and use partial local search if needed.
- **Crossover that breaks too much.** If the crossover destroys most edges of the parents, local search must rebuild the tour, and the method acts like a random restart.
- **Float comparisons.** With real distances, a move whose gain is zero up to rounding can make 2-opt cycle. Accept a move only if it saves more than a small tolerance, as the implementation does.

## Implementations

## History

Moscato named and described memetic algorithms in a 1989 report of the Caltech Concurrent Computation Program, with the word meme from Dawkins (1976) for a unit of cultural evolution. Several groups had joined genetic algorithms with local search for the TSP in the late 1980s, under names such as genetic local search. Hinton and Nowlan (1987) showed how learning can guide evolution, the Baldwin effect, and Whitley, Gordon and Mathias (1994) compared Lamarckian and Baldwinian use of local search. Merz and Freisleben developed memetic algorithms for the TSP and the quadratic assignment problem in the 1990s, and Krasnogor and Smith (2005) gave a taxonomy and design guide. The Handbook of Memetic Algorithms (2012) covers the field.

## References
