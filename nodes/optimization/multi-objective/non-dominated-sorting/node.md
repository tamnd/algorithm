---
tag: PQCHE1
kind: algorithm
slug: non-dominated-sorting
name: Non-dominated sorting
aliases:
- fast non-dominated sort
- Pareto ranking into fronts
- non-dominated sorting algorithm
area: optimization/multi-objective
level: core
summary: Split a set of objective vectors into fronts, each the Pareto front of what earlier fronts leave. Deb's fast version takes O(p N^2) time and O(N^2) space.
solves: [pareto-front-computation]
model: comparison-model
complexity:
  vars: {N: the number of points, p: the number of objectives}
  time: {worst: Θ(p N^2), best: Θ(N^2)}
  space: {extra: Θ(N^2)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 2002
  people: [Kalyanmoy Deb, Amrit Pratap, Sameer Agarwal, T. Meyarivan]
  note: Goldberg proposed ranking by successive non-dominated fronts in 1989. Srinivas and Deb used it in NSGA in 1994 with an O(p N^3) procedure. Deb, Pratap, Agarwal and Meyarivan gave the O(p N^2) fast non-dominated sort with NSGA-II in 2002.
prereqs: [pareto-dominance, pareto-front]
see_also: [pareto-ranking, nsga-ii, crowding-distance, kung-algorithm, pareto-front-computation, nsga-iii, spea2]
sources:
  - paper: doi:10.1109/4235.996017
    title: Kalyanmoy Deb, Amrit Pratap, Sameer Agarwal and T. Meyarivan, A fast and elitist multiobjective genetic algorithm, NSGA-II, IEEE Transactions on Evolutionary Computation 6(2), 2002, 182-197
    locator: Section III-A, the fast non-dominated sorting approach and its O(M N^2) cost
  - paper: doi:10.1109/TEVC.2003.817234
    title: Mikkel T. Jensen, Reducing the run-time complexity of multiobjective EAs, the NSGA-II and other algorithms, IEEE Transactions on Evolutionary Computation 7(5), 2003, 503-515
    locator: the divide and conquer non-dominated sort in O(N log^(M-1) N) time
  - paper: doi:10.1145/321906.321910
    title: H. T. Kung, F. Luccio and F. P. Preparata, On finding the maxima of a set of vectors, Journal of the ACM 22(4), 1975, 469-476
    locator: the divide and conquer maxima algorithm and the comparison lower bound
  - book: isbn:9780471873396
    title: Kalyanmoy Deb, Multi-Objective Optimization Using Evolutionary Algorithms, Wiley, 2001
    locator: Chapter 2, the procedures for finding a non-dominated set and for the non-dominated sorting of a population
  - paper: doi:10.1162/evco.1994.2.3.221
    title: N. Srinivas and Kalyanmoy Deb, Multiobjective optimization using nondominated sorting in genetic algorithms, Evolutionary Computation 2(3), 1994, 221-248
    locator: the NSGA ranking by successive fronts
---

Non-dominated sorting splits a finite set of objective vectors into *fronts*: front 1 is the [Pareto front](/pareto-front/) of the set, front 2 is the Pareto front of the rest, and so on. The front number of a point is its rank, and the ranks drive selection in [NSGA-II](/nsga-ii/), [NSGA-III](/nsga-iii/) and many other evolutionary methods. The fast non-dominated sort of Deb, Pratap, Agarwal and Meyarivan does this in $O(p N^2)$ time and $O(N^2)$ space for $N$ points with $p$ objectives. Divide and conquer methods in the style of Kung take $O(N \log^{p-1} N)$ time, and for two objectives a sweep with binary search takes $O(N \log N)$.

## In plain words

You have a list of options, and each option has several costs. One option beats another if it is no worse in any cost and better in at least one. The options that nothing beats form the first group. Take them away. The options that nothing in the rest beats form the second group. Go on until nothing is left. The group number is a grade: grade 1 is the best.

The fast method does not remove points again and again. It first compares each pair one time. For each option it counts how many options beat it, and it lists the options that it beats. The options with count zero are grade 1. Then it takes each grade 1 option and lowers the count of each option that it beats. Each option whose count drops to zero is grade 2. This goes on, grade by grade.

## The problem

**Convention.** All objectives are minimized. The input is a list $Y = (y^1, \ldots, y^N)$ of points of $\mathbb{R}^p$, where $y^i = f(x^i)$ is the image of a solution $x^i$. Point $a$ dominates point $b$, written $a \prec b$, when $a_t \le b_t$ for each $t = 1, \ldots, p$ and $a_t < b_t$ for at least one $t$. This is [Pareto dominance](/pareto-dominance/).

The output is the partition of $\{1, \ldots, N\}$ into fronts $F_1, F_2, \ldots, F_K$, defined by

$$F_k = \{\, j \in R_{k-1} : \text{no } i \in R_{k-1} \text{ has } y^i \prec y^j \,\}, \qquad R_0 = \{1, \ldots, N\}, \quad R_k = R_{k-1} \setminus F_k.$$

The rank of $j$ is the $k$ with $j \in F_k$. Equal points do not dominate each other, so they get the same rank. The first front alone is the [Pareto front computation](/pareto-front-computation/) problem for a finite set, which [Kung's algorithm](/kung-algorithm/) solves.

## The algorithm

```pseudo id=main
FAST-NON-DOMINATED-SORT(Y[1 .. N])
L1  for i ← 1 to N do S[i] ← ∅, n[i] ← 0       ▷ S[i]: points that i dominates; n[i]: count of points that dominate i
L2  for i ← 1 to N do
L3      for j ← i + 1 to N do
L4          if Y[i] ≺ Y[j] then S[i] ← S[i] ∪ {j}, n[j] ← n[j] + 1
L5          else if Y[j] ≺ Y[i] then S[j] ← S[j] ∪ {i}, n[i] ← n[i] + 1
L6  F ← {i : n[i] = 0}, k ← 1
L7  while F ≠ ∅ do
L8      output F as front k, Q ← ∅
L9      for each i ∈ F do
L10         for each j ∈ S[i] do
L11             n[j] ← n[j] − 1
L12             if n[j] = 0 then Q ← Q ∪ {j}
L13     F ← Q, k ← k + 1
L14 return the fronts
```

Lines L1 to L5 compare each unordered pair one time and build the dominance graph: $S[i]$ is the list of points that $i$ dominates, and $n[j]$ is the number of points that dominate $j$. A dominance test costs at most $2p$ comparisons. Line L6 takes the points that nothing dominates. Lines L9 to L12 remove the current front from the graph. A point whose count falls to zero has lost its last dominator, so it belongs to the next front. Deb et al. compare each ordered pair; the loop over $j > i$ does each test once and gives the same graph.

**Two objectives.** For $p = 2$ a sweep is faster. Sort the points in the lexicographic order of $(y_1, y_2)$. Keep the last point added to each front. Put each new point into the first front whose last point does not dominate it, and open a new front if there is none. The fronts whose last point dominates the new point form a prefix, so a binary search finds the place. This takes $O(N \log N)$ time and $O(N)$ space.

## Example

Take $N = 8$ points with $p = 2$: $A = (1, 8)$, $B = (2, 5)$, $C = (3, 6)$, $D = (4, 2)$, $E = (5, 4)$, $F = (6, 7)$, $G = (7, 1)$, $H = (8, 3)$.

Lines L1 to L5 give these lists and counts:

| point | $S$ (points it dominates) | $n$ (points that dominate it) |
|---|---|---|
| A (1, 8) | none | 0 |
| B (2, 5) | C, F | 0 |
| C (3, 6) | F | 1 |
| D (4, 2) | E, F, H | 0 |
| E (5, 4) | F | 1 |
| F (6, 7) | none | 4 |
| G (7, 1) | H | 0 |
| H (8, 3) | none | 2 |

The loop of line L7 then runs three rounds:

| round | front | counts that change | next front |
|---|---|---|---|
| 1 | A, B, D, G | C: 1 to 0; F: 4 to 3 to 2; E: 1 to 0; H: 2 to 1 to 0 | C, E, H |
| 2 | C, E, H | F: 2 to 1 to 0 | F |
| 3 | F | none | empty |

So the ranks are $A, B, D, G \mapsto 1$, $C, E, H \mapsto 2$ and $F \mapsto 3$. The 2D sweep visits the points in the order $A, B, C, D, E, F, G, H$. It opens front 2 at $C$, because $B$ dominates $C$. It puts $E$ into front 2, because $D$, the last point of front 1, dominates $E$ but $C$ does not. It opens front 3 at $F$, because $E$ dominates $F$. It gives the same fronts.

## Correctness

Two facts about the fronts carry the proof. If $y^i \prec y^j$, then the rank of $i$ is less than the rank of $j$. And a point of rank $k \ge 2$ has a dominator of rank $k - 1$. So the rank of a point is one more than the largest rank of its dominators. The loop of line L7 keeps this invariant: when front $k$ is the current set, $n[j]$ counts the dominators of $j$ among the points of rank at least $k$. So a count reaches zero in round $k$ exactly for the points of front $k + 1$. The full proof, with the proof of the two-objective sweep, is below.

## Complexity

- **Time, lines L1 to L5.** There are $N(N-1)/2$ pairs, and each pair takes at most two dominance tests of $O(p)$ comparisons. This is $\Theta(p N^2)$ in the worst case, for example when all points are equal and each test reads all $p$ coordinates. Each test reads at least one coordinate, so the best case is $\Theta(N^2)$.
- **Time, lines L7 to L13.** Each point is in one front, so each list $S[i]$ is read one time. The total is $\sum_i |S[i]| \le N(N-1)/2$.
- **Space.** The lists hold one entry for each dominating pair. A chain $y^1 \prec y^2 \prec \cdots \prec y^N$ has $N(N-1)/2$ such pairs, so the extra space is $\Theta(N^2)$ in the worst case.

The total is $\Theta(p N^2)$ time in the worst case. The older procedure of NSGA found each front by a new $O(p N^2)$ scan of the rest, which is $O(p N^3)$ in total when there are $N$ fronts.

**Faster methods.** Jensen (2003) adapted the divide and conquer of Kung, Luccio and Preparata to sort all fronts in $O(N \log^{p-1} N)$ time for fixed $p$. His method assumed that no two points share a value in an objective. Fortin, Grenier and Parizeau (2013) and Buzdalov and Shalyto (2014) extended it to inputs with ties at the same bound. For $p = 2$ the sweep above takes $O(N \log N)$. In the comparison model this is optimal for $p = 2$: even the first front, the maxima of a point set, needs $\Omega(N \log N)$ comparisons in the worst case (Kung, Luccio and Preparata).

## Properties

- **Deterministic and exact.** It uses only comparisons of coordinates, so there is no rounding issue.
- **Order of the output.** The order of the points inside a front depends on the order of the input. Callers that break ties by position must say so.
- **Not online.** A new point can change the rank of many old points, so the fronts are recomputed for each population.
- **Ties.** Equal points share a front. A point that is equal in one objective and better in another dominates.

## Variants and improvements

- **Peeling.** Compute the non-dominated points of the rest, remove them, and repeat. It needs no $O(N^2)$ graph, but costs $O(p N^2)$ for each front, so $O(p N^3)$ in the worst case.
- **Jensen's method and its fixes.** Divide and conquer on the objectives, $O(N \log^{p-1} N)$ time. It wins for small $p$ and large $N$.
- **The 2D sweep.** Sort, then binary search over the last points of the fronts. $O(N \log N)$.
- **Best order sort and efficient non-dominated sort (ENS).** These keep the fronts as lists and compare a new point only with the members of a front. They are $O(p N^2)$ in the worst case, and their authors report fewer comparisons than the fast sort on their test sets.
- **Incremental updates.** Steady-state algorithms insert or remove one point at a time and update only the ranks that change.
- **Ranking without fronts.** The [Pareto ranking](/pareto-ranking/) page compares this rank with the count of dominators that [MOGA](/moga/) uses and the strength of [SPEA2](/spea2/).

## When to use it

Use the fast sort when $N$ is a few hundred or a few thousand and $p$ is any size. It is short, exact and easy to test. For two objectives, use the sweep. For large $N$ with a small fixed $p$, the divide and conquer methods are faster. If only the first front is needed, use [Kung's algorithm](/kung-algorithm/) or a simple filter, not the full sort.

## Pitfalls

- **Testing $\le$ in each coordinate only.** With the test $a_t \le b_t$ for all $t$ in lines L4 and L5, an equal point "dominates" its copy, the counts never reach zero, and the copies are lost from all fronts. The test needs a strict inequality in at least one coordinate.
- **Testing both orders of a pair in one branch.** If line L5 is an `if` and not an `else if`, the code is still right only because the order is strict. If a custom dominance (for example with constraints) is not antisymmetric, a pair can count twice. Check that the relation is a strict partial order first.
- **Removing from the list that is read.** Some code deletes a point from $S$ or from the current front inside the loop of lines L9 and L10. Build the next front in a new set $Q$, as in line L8.
- **Mixing maximization and minimization.** Negate each objective to be maximized before the sort.

## Implementations

## History

Goldberg proposed in 1989 to rank a population by successive non-dominated fronts, in his book on genetic algorithms. Srinivas and Deb built NSGA on this idea in 1994, with a procedure that costs $O(p N^3)$ in the worst case. Deb, Pratap, Agarwal and Meyarivan gave the $O(p N^2)$ fast non-dominated sort in the NSGA-II paper of 2002. Jensen gave the $O(N \log^{p-1} N)$ method in 2003, from the maxima algorithm of Kung, Luccio and Preparata (1975).

## References
