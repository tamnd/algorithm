---
tag: G7YMB0
kind: technique
slug: backwards-analysis
name: Backwards analysis
aliases:
- Seidel's backwards analysis
- backward analysis
area: techniques/randomization-techniques
level: advanced
summary: Bounds expected cost by asking which object would be last to be inserted and how often its removal changes the structure.
prereqs: [random-permutation, linearity-of-expectation, expected-running-time]
see_also: [randomized-incremental-construction, seidel-linear-programming, welzls-algorithm, randomized-closest-pair, delaunay-triangulation-construction, trapezoidal-map, hiring-problem, expected-running-time]
sources:
  - paper: doi:10.1007/978-3-642-58043-7_3
    title: Raimund Seidel, Backwards analysis of randomized geometric algorithms, in New Trends in Discrete and Computational Geometry, Algorithms and Combinatorics 10 (1993)
    locator: pp. 37 to 67
  - paper: doi:10.1007/BF02574699
    title: Raimund Seidel, Small-dimensional linear programming and convex hulls made easy, Discrete and Computational Geometry 6(3) (1991)
    locator: pp. 423 to 434 (the randomized incremental linear programming algorithm and the probability d/i that the i-th constraint changes the optimum)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 4 (randomized incremental linear programming and the smallest enclosing disc), Chapter 6 (the trapezoidal map) and Chapter 9 (the Delaunay triangulation), each analysed backwards
---

Backwards analysis is a way to bound the expected cost of step $i$ of an algorithm that inserts $n$ objects one at a time in a uniformly random order. Instead of asking what the new object does to the structure of the first $i - 1$ objects, it fixes the set of the first $i$ objects and asks what happens when one of them, chosen uniformly at random, is deleted. The cost then becomes an average over the $i$ objects of a set, which a counting fact about one fixed structure often bounds. Seidel named the technique and collected its uses in geometry in 1993.

## In plain words

Cards from a shuffled deck are laid down one by one, and each new card may force some work. To guess the work at the tenth card, do not think about the tenth card arriving. Think about the ten cards on the table, and ask which of them was the last one. In a fair shuffle, each of the ten is equally likely to be the last.

Now the question is about a fixed hand of ten cards: for how many of them would removing that card cause work, and how much? If only two cards matter, the chance of work is two in ten. This is much easier to count than the effect of a new card on an unknown hand, because the hand is fixed and only the choice of the last card is random.

## When it applies

- The algorithm inserts the objects of a set $S$ of size $n$ in a uniformly [random permutation](/random-permutation/) order, as in [randomized incremental construction](/randomized-incremental-construction/).
- After $i$ insertions, the algorithm holds a structure $F(S_i)$ that depends only on the set $S_i$ of the first $i$ objects, not on the order in which they came. A unique optimum, a triangulation in general position or a set of minima are of this kind.
- The cost of step $i$ can be bounded by a quantity $c(x, S_i)$ that depends only on the set $S_i$ and the object $x$ inserted last.
- For each fixed set $T$ of size $i$, the sum $\sum_{x \in T} c(x, T)$ has a good bound, usually because only a few objects of $T$ define the structure, or because the structure has $O(i)$ parts.

The core fact is a symmetry. In a uniformly random permutation, conditioned on the set $S_i$ of its first $i$ elements, the order of these $i$ elements is uniform, so the $i$-th element is uniform in $S_i$. Indeed, each of the $i!$ orders of $S_i$ extends to the same number $(n - i)!$ of permutations of $S$.

## The template

```pseudo id=main
BACKWARDS-ANALYSIS(algorithm, S, n)
L1  for each step i from 1 to n
L2      fix an arbitrary set T ⊆ S with |T| = i, and condition on S_i = T
L3      define the structure F(T)                       ▷ hole: a structure that depends on the set only
L4      bound the cost of step i by c(x, T), x the last object   ▷ hole: the charge to the deleted object
L5      E[cost_i | S_i = T] ← (1/i) · Σ_{x ∈ T} c(x, T)        ▷ x is uniform in T
L6      bound Σ_{x ∈ T} c(x, T) ≤ B(i) for every T             ▷ hole: a counting fact about F(T)
L7      E[cost_i] ≤ B(i) / i                                   ▷ the bound does not depend on T
L8  E[total] ≤ Σ_{i=1}^{n} B(i) / i                            ▷ linearity of expectation
```

The three holes are the structure of line L3, the charge of line L4 and the count of line L6. Line L7 holds because the bound of line L6 holds for every $T$, so it survives the average over the random set $S_i$. The total of line L8 needs only [linearity of expectation](/linearity-of-expectation/), and no independence between the steps.

The common form of line L6 is: at most $d$ objects of $T$ *define* $F(T)$, in the sense that deleting any other object leaves $F$ unchanged. If step $i$ costs at most $a(i)$ when $x$ is a defining object and $O(1)$ otherwise, then $\mathbb{E}[\mathrm{cost}_i] \le (d/i)\,a(i) + O(1)$.

## Classic examples

- **Prefix minima and the [hiring problem](/hiring-problem/).** Scan $n$ distinct numbers in a random order and update the current minimum. The $i$-th number is a new minimum exactly when it is the minimum of $S_i$. Backwards: of the $i$ elements of $S_i$, exactly one, its minimum, defines $F(S_i)$, so the probability is $1/i$, and the expected number of updates is $H_n = \sum_{i=1}^{n} 1/i$. This is 25/12 for $n = 4$, as the 24 orders of 4 numbers give 50 updates in all, about 2.93 for $n = 10$, 5.19 for $n = 100$ and 7.49 for $n = 1000$.
- **[Seidel's linear programming](/seidel-linear-programming/).** Add the $n$ constraints of a linear program in $d$ variables in random order and keep the optimum $v_i$ of the first $i$. If the $i$-th constraint $h$ holds at $v_{i-1}$, the optimum does not change. If not, the new optimum lies on the boundary of $h$, and the algorithm solves a problem in $d - 1$ dimensions with $i - 1$ constraints. Backwards: with a unique optimum, at most $d$ constraints of $S_i$ define $v_i$, so the expensive case has probability at most $d/i$. In the plane, step $i$ costs $O(1)$ plus, with probability at most $2/i$, a one-dimensional problem in $O(i)$ time, so the expected total is $O(n)$. In general the expected time is $O(d!\,n)$.
- **The smallest enclosing disk, [Welzl's algorithm](/welzls-algorithm/).** The [minimum enclosing circle](/minimum-enclosing-circle/) of the first $i$ points is defined by at most 3 of them. Point $i$ falls outside the circle of the first $i - 1$ points only if it is one of these, with probability at most $3/i$, and then a recomputation takes $O(i)$ expected time. The expected total is $O(n)$.
- **[Randomized closest pair](/randomized-closest-pair/).** Keep the closest distance $\delta$ of the first $i$ points and a grid of cell size $\delta$. The $i$-th point changes $\delta$ only if it is in the closest pair of $S_i$, with probability at most $2/i$ when the pair is unique, and then the grid is rebuilt in $O(i)$ time. The expected total is $O(n)$ grid operations.
- **[Delaunay triangulation construction](/delaunay-triangulation-construction/).** Insert the points in random order and flip edges after each insertion. The number of new triangles at step $i$ is at most a constant times the degree of the new point in the triangulation of $S_i$. A triangulation of $i$ points has at most $3i - 6$ edges, so the degrees sum to at most $6i - 12$, and the expected degree of a random point of $S_i$ is less than 6. So the expected structural change is $O(1)$ per step.
- **The [trapezoidal map](/trapezoidal-map/).** For $n$ segments in random order, a trapezoid of the map of $S_i$ is defined by at most 4 segments, and the map has $O(i)$ trapezoids. So the expected number of trapezoids that the $i$-th segment creates is $O(1)$, and the expected size of the search structure is $O(n)$.

## Variations

- **Deletion of a constant number of objects.** Some bounds look at the last two or three objects of $S_i$, for example to bound a cost that depends on both $x$ and the previous object. The symmetry still holds: the last $j$ objects of $S_i$ form a uniform random ordered $j$-subset of $S_i$.
- **Conflict counts and the Clarkson-Shor bound.** The cost of keeping conflict lists is a sum over the parts of $F(S_i)$ of the number of uninserted objects that conflict with them. Backwards analysis bounds the expected number of new parts, and the method of Clarkson and Shor turns this into an expected total of $O(\sum_i (n/i)\,\mathbb{E}[\text{new parts at step } i])$, see [randomized incremental construction](/randomized-incremental-construction/).
- **Analysis of data structures.** The expected depth of a key in a [random binary search tree](/random-binary-search-tree/) or a [treap](/treap/) is a sum of probabilities that another key is an ancestor, and the same symmetry, applied to the set of keys between them, shows that key $j$ is an ancestor of key $i$ with probability $1/(|j - i| + 1)$.
- **Dimension recursion.** In Seidel's method, the expensive case calls the same algorithm one dimension lower, and backwards analysis gives the recurrence $T(d, n) \le T(d, n - 1) + O(d) + \frac{d}{n}\,T(d - 1, n - 1)$.

## Pitfalls

- **A structure that depends on the order.** The argument fails if $F(S_i)$ depends on the history, for example a search structure whose shape depends on the order of the insertions. Then analyse a quantity that depends on the set only, such as the triangulation, and handle the history part separately.
- **Degenerate cases.** "At most $d$ objects define the optimum" needs a unique optimum and general position. With ties, define a canonical optimum, for example the lexicographically smallest, so that the count stays at most $d$.
- **The location step is not covered.** For geometric constructions, backwards analysis bounds the structural change. The cost of finding where the new object goes, by conflict lists or by a history structure, needs its own analysis.
- **An order that is not uniform.** The symmetry holds only for a uniformly random permutation. An input order, a sort by angle or a nearly sorted order gives no guarantee, and adversarial orders can force $\Theta(n)$ work at each step.
- **The expectation is over the order, not the input.** The bound holds for every input set $S$. It says nothing about a fixed order, and a tail bound needs a separate argument.

## Exercises

1. Show by backwards analysis that the expected number of prefix minima of a random permutation of $n$ distinct numbers is $H_n$, and check the value 25/12 for $n = 4$ by listing the 24 orders.
2. Show that in a random permutation of $n$ distinct numbers, the expected number of indices $i$ at which the second smallest of the first $i$ numbers changes is $2H_n - 2$ for $n \ge 2$. (Hint: for $i \ge 2$, two of the $i$ objects define the pair.)
3. In Seidel's algorithm for two variables, prove that the expected running time is $O(n)$ by writing out the template with $d = 2$ and $a(i) = O(i)$.
4. Prove that a planar triangulation of $i \ge 3$ points in general position has at most $3i - 6$ edges, and conclude that a random vertex has expected degree less than 6.
5. In the randomized closest pair algorithm, show that the expected number of grid rebuilds is at most $2H_n$, also when several pairs are at the smallest distance. (Hint: the distance $\delta$ changes at step $i$ only if the new point is in every closest pair of $S_i$.)

## References
