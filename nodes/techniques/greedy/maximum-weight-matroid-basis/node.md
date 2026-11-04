---
tag: 2QJ3YN
kind: problem
slug: maximum-weight-matroid-basis
name: Maximum-weight matroid basis
aliases:
- Maximum-weight basis of a matroid
- max-weight basis of a matroid
- max-weight matroid basis
- minimum-weight matroid basis
area: techniques/greedy
level: core
summary: Find an independent set of maximum weight that is a basis of a weighted matroid.
prereqs: [matroid]
see_also: [matroid-greedy-algorithm, matroid-greedy-theorem, minimum-spanning-tree, maximum-spanning-tree, job-sequencing-with-deadlines, matroid-intersection, linear-matroid, partition-matroid]
sources:
  - paper: doi:10.1007/BF01584082
    title: Jack Edmonds, Matroids and the greedy algorithm, Mathematical Programming 1(1), 1971
    locator: pages 127 to 136
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, sixth edition
    locator: Chapter 13, Matroids (the maximization and minimization problems for independence systems)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 16.4, Matroids and greedy methods (the weighted matroid problem)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 40, The greedy algorithm and the independent set polytope
---

The maximum-weight matroid basis problem asks, for a [matroid](/matroid/) with a real weight on each element, for a basis whose total weight is as large as possible. The [matroid greedy algorithm](/matroid-greedy-algorithm/) solves it exactly with one sort and one independence test per element, and the [matroid greedy theorem](/matroid-greedy-theorem/) shows that matroids are exactly the independence systems where this works for all weights. The [minimum spanning tree](/minimum-spanning-tree/) problem, the heaviest set of linearly independent vectors and [job sequencing with deadlines](/job-sequencing-with-deadlines/) are all special cases.

## In plain words

You have a set of items with values, and a rule that says which groups of items are allowed. The rule has the matroid shape: every allowed group can grow by an item from any larger allowed group, so all the largest allowed groups have the same size. Such a largest group is called a basis.

The task is to pick a basis with the highest total value. Spanning trees of a network are bases, and so are sets of independent vectors that span a space.

Because of the matroid shape, the task is easy. Go from the most valuable item down, and keep each item that still fits. There is no need to look ahead or undo a choice.

## Definition

**Input.** A matroid $M = (E, \mathcal{I})$ on $n$ elements and a weight function $w : E \to \mathbb{R}$. The matroid is usually given by an *independence oracle*, which answers whether a given set is independent, or by an explicit structure such as a graph or a matrix.

**Output.** A basis $B$ of $M$, a maximal independent set, such that
$$ w(B) = \sum_{x \in B} w(x) \ge w(B') \quad \text{for every basis } B'. $$

**Related forms.**

- *Minimum-weight basis.* Minimize $w(B)$ over bases. This is the maximum problem for $-w$.
- *Maximum-weight independent set.* Maximize $w(X)$ over all $X \in \mathcal{I}$, not only bases. With nonnegative weights some basis is optimal, so the two problems agree. With negative weights, the answer is a maximum-weight basis of the restriction of $M$ to the elements of positive weight.

**Solvability.** By the [matroid greedy theorem](/matroid-greedy-theorem/), sorting by nonincreasing weight and keeping each element that preserves independence returns a maximum-weight basis, for every $w$.

## Variants

- **Bottleneck basis.** Maximize the smallest weight in the basis. The greedy basis is optimal here too, because it dominates every basis element by element.
- **Lexicographic basis.** Compare bases by their sorted weight vectors, largest first. Again the greedy basis is optimal, by the same domination.
- **Two matroids.** Find a heaviest set that is independent in two matroids at once, such as a bipartite matching or a spanning tree with limits on colors. Greedy fails, and [matroid intersection](/matroid-intersection/) solves it in polynomial time with the [matroid intersection algorithm](/matroid-intersection-algorithm/).
- **Three or more matroids.** Common independent sets of three matroids include Hamiltonian paths in directed graphs, so the problem is NP-hard.
- **Online.** If the elements arrive one by one and each must be accepted or rejected at once, the problem is the matroid secretary problem; for the [uniform matroid](/uniform-matroid/) it is the [secretary problem](/secretary-problem/) with $k$ choices.

## Examples

**Basis against independent set.** On the [uniform matroid](/uniform-matroid/) $U_{3,5}$ with weights $6, 4, -1, -2, -5$, the bases are the 3-element sets. The maximum-weight basis is $\{6, 4, -1\}$ with weight 9. The maximum-weight independent set is $\{6, 4\}$ with weight 10, because it does not have to be a basis.

**Spanning trees.** For the graphic matroid of a connected graph, bases are spanning trees. The [matroid greedy algorithm](/matroid-greedy-algorithm/) page traces a graph on five vertices with eight edges, where the greedy basis $\{a, c, e, g\}$ of weight 30 is the only optimum among 45 spanning trees. The minimum form is the [minimum spanning tree](/minimum-spanning-tree/).

**A partition matroid.** Blocks $\{a, b, c\}$ with weights $9, 7, 4$ and capacity 1, $\{d, e, f\}$ with weights $8, 6, 5$ and capacity 2, and $\{g, h\}$ with weights $3, 2$ and capacity 1. The maximum-weight basis takes the heaviest elements of each block up to its capacity: $\{a, d, e, g\}$ with weight 26. See [partition matroid](/partition-matroid/).

**Unit jobs.** In [job sequencing with deadlines](/job-sequencing-with-deadlines/), the sets of jobs that can all meet their deadlines form a matroid, and a maximum-profit schedule is a maximum-weight independent set.

## Known algorithms

- **Matroid greedy algorithm.** Sort, then scan with $n$ independence tests. $O(n \log n + n f)$ time for an oracle of cost $f$. Exact for every matroid.
- **Uniform and partition matroids.** Pick the heaviest $k$ elements, or the heaviest $k_i$ in each block, with linear-time [selection](/top-k-selection/). $O(n)$ time, no sort needed.
- **Graphic matroids.** Any minimum or [maximum spanning tree](/maximum-spanning-tree/) algorithm: [Kruskal](/kruskal/) is the greedy algorithm with a disjoint-set oracle, and [Prim](/prim/) and [Borůvka](/boruvka/) use other cut properties of the same matroid.
- **Linear matroids.** The greedy algorithm with Gaussian elimination as an incremental oracle; see [linear matroid](/linear-matroid/).
- **Linear programming.** Edmonds showed that the maximum of $w^\top x$ over the matroid polytope $\{x \ge 0 : x(S) \le r(S) \text{ for all } S\}$ is reached at the greedy solution, so the problem is also a linear program with an integral optimum.

## Bounds

- **Upper bound.** $O(n \log n)$ comparisons and $n$ oracle calls, by the greedy algorithm.
- **Without a full sort.** For some matroids, sorting is not needed: uniform and partition matroids take $O(n)$ time, and minimum spanning trees can be found in linear expected time. In general, the greedy algorithm needs only the order of the weights, and its work beyond the oracle is the sort.
- **Lower bound.** $\Omega(n)$ time, because the weight of each element can change the answer.

## Reductions

- **Minimum to maximum.** Negate the weights.
- **Independent set to basis.** Delete the elements of nonpositive weight and solve the basis problem on the restriction; the restriction of a matroid is a matroid.
- **Shift invariance.** Adding a constant $c$ to every weight adds $c \cdot r(E)$ to the weight of every basis, because all bases have $r(E)$ elements. So the basis problem can always be made to have positive weights.
- **To matroid intersection.** The basis problem is the special case of [matroid intersection](/matroid-intersection/) in which the second matroid is the free matroid.

## Applications

- **Network design.** Cheapest or most reliable spanning networks, as minimum or maximum spanning trees.
- **Selecting independent measurements.** Choosing the most valuable set of linearly independent features or sensors.
- **Scheduling.** Unit-time jobs with deadlines, and more generally any problem whose feasible sets are the matchable sets of a bipartite graph.
- **Subroutine.** Matroid intersection and many approximation algorithms call a maximum-weight basis routine as a step.

## References
