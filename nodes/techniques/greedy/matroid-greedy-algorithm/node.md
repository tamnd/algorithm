---
tag: 4BS62B
kind: algorithm
slug: matroid-greedy-algorithm
name: Matroid greedy algorithm
aliases:
- Greedy algorithm for matroids
- greedy algorithm for matroids
- matroid greedy
area: techniques/greedy
level: core
summary: Sort elements by decreasing weight and add each one that keeps the set independent.
solves: [maximum-weight-matroid-basis]
model: comparison-model
complexity:
  vars: {n: the number of elements, f: the time of one independence test}
  time: {worst: O(n log n + n f), average: O(n log n + n f), best: O(n log n + n f)}
  space: {extra: Θ(n)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1971
  people: [Richard Rado, David Gale, Jack Edmonds]
  note: Rado (1957) and Edmonds (1971) proved that greedy is optimal on matroids and only on matroids; Gale (1968) proved the stronger optimality of the greedy basis.
prereqs: [matroid, greedy-algorithm]
see_also: [matroid-greedy-theorem, maximum-weight-matroid-basis, kruskal, graphic-matroid, linear-matroid, job-sequencing-with-deadlines, matroid-intersection, uniform-matroid]
sources:
  - paper: doi:10.1007/BF01584082
    title: Jack Edmonds, Matroids and the greedy algorithm, Mathematical Programming 1(1), 1971
    locator: pages 127 to 136
  - paper: doi:10.1112/plms/s3-7.1.300
    title: Richard Rado, Note on independence functions, Proceedings of the London Mathematical Society s3-7(1), 1957
    locator: pages 300 to 320
  - paper: doi:10.1016/S0021-9800(68)80039-0
    title: David Gale, Optimal assignments in an ordered set, an application of matroid theory, Journal of Combinatorial Theory 4(2), 1968
    locator: pages 176 to 180
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 16.4, Matroids and greedy methods (the procedure GREEDY)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, sixth edition
    locator: Chapter 13, Matroids (the best-in greedy algorithm)
---

The matroid greedy algorithm finds a maximum-weight basis of a weighted [matroid](/matroid/). It sorts the elements by nonincreasing weight and scans them once, adding each element that keeps the chosen set independent. It needs only an independence oracle for the matroid, and it makes $n$ calls to it after an $O(n \log n)$ sort. By the [matroid greedy theorem](/matroid-greedy-theorem/), the result is optimal for every weight function, and this property characterizes matroids. [Kruskal's algorithm](/kruskal/) for spanning trees is the case of the [graphic matroid](/graphic-matroid/).

## In plain words

You have a set of items, each with a value, and a rule that says which groups of items are allowed. The rule has the matroid shape: a smaller allowed group can always grow by an item from a larger allowed group.

Go through the items from the most valuable to the least valuable. Take each item if the group you have, together with the new item, is still allowed. Never undo a choice.

On a matroid this simple scan gives a largest allowed group of the highest total value. It does not need to know anything about the rule except how to ask "is this group allowed?". On rules without the matroid shape, the same scan can give a bad answer.

## The problem

The input is a matroid $M = (E, \mathcal{I})$ with $|E| = n$, given by an *independence oracle* that answers whether a set $X \subseteq E$ is in $\mathcal{I}$, and a weight function $w : E \to \mathbb{R}$. A *basis* is a maximal independent set, and all bases have the same size $r(E)$. The goal is a basis $B$ with the largest weight $w(B) = \sum_{x \in B} w(x)$. This is the [maximum-weight matroid basis](/maximum-weight-matroid-basis/) problem.

## The algorithm

```pseudo id=main
MATROID-GREEDY(E, w, indep)          ▷ indep(X) tests X ∈ I
L1  sort E into e1, ..., en with w(e1) ≥ w(e2) ≥ ... ≥ w(en)
L2  A ← ∅
L3  for i ← 1 to n do
L4      if indep(A ∪ {ei}) then
L5          A ← A ∪ {ei}
L6  return A
```

Line L1 fixes the order; ties may be broken in any way, and a stable sort keeps them in input order. Line L4 is the only place where the matroid enters. Line L5 never removes an element, so $A$ only grows, and every element is tested exactly once.

## Example

A graph on vertices $1, \ldots, 5$ with eight edges, written (endpoints, weight): $a = (12, 7)$, $b = (13, 5)$, $c = (23, 8)$, $d = (24, 6)$, $e = (34, 9)$, $f = (35, 4)$, $g = (45, 6)$, $h = (15, 3)$. The matroid is the [graphic matroid](/graphic-matroid/): a set of edges is independent when it has no cycle. Line L1 gives the order $e, c, a, d, g, b, f, h$, with $d$ before $g$ by input order.

| $i$ | edge | weight | $A \cup \{e_i\}$ independent? | $A$ after the step | $w(A)$ |
| --- | --- | --- | --- | --- | --- |
| 1 | $e = 34$ | 9 | yes | $e$ | 9 |
| 2 | $c = 23$ | 8 | yes | $e, c$ | 17 |
| 3 | $a = 12$ | 7 | yes | $e, c, a$ | 24 |
| 4 | $d = 24$ | 6 | no, cycle $2, 3, 4$ | $e, c, a$ | 24 |
| 5 | $g = 45$ | 6 | yes | $e, c, a, g$ | 30 |
| 6 | $b = 13$ | 5 | no, cycle $1, 2, 3$ | $e, c, a, g$ | 30 |
| 7 | $f = 35$ | 4 | no, cycle $3, 4, 5$ | $e, c, a, g$ | 30 |
| 8 | $h = 15$ | 3 | no, cycle $1, 2, 3, 4, 5$ | $e, c, a, g$ | 30 |

The result $\{a, c, e, g\}$ is a spanning tree of weight 30. The graph has 45 spanning trees, and this is the only one of weight 30; the next best weigh 28, and the lightest weighs 19. Rejecting $d$ was forced: with $c$ and $e$ chosen, $d$ closes a triangle.

## Correctness

The full proof is below; it follows the [matroid greedy theorem](/matroid-greedy-theorem/). First, $A$ stays independent, because line L5 adds $e_i$ only after line L4 has checked it. Next, $A$ is a basis: an element $e_i$ rejected at line L4 makes $A_i \cup \{e_i\}$ dependent for the set $A_i$ at that time, and since $A_i \subseteq A$, the hereditary property makes $A \cup \{e_i\}$ dependent too. Last, let $A = \{g_1, \ldots, g_r\}$ in the order chosen and let $B = \{b_1, \ldots, b_r\}$ be any basis sorted by nonincreasing weight. If $w(g_k) < w(b_k)$ for a least $k$, the exchange property applied to $\{g_1, \ldots, g_{k-1}\}$ and $\{b_1, \ldots, b_k\}$ gives some $b_j$, with $w(b_j) \ge w(b_k) > w(g_k)$, that the algorithm would have taken before $g_k$, a contradiction. So $w(g_k) \ge w(b_k)$ for every $k$, and $w(A) \ge w(B)$.

## Complexity

- **Time.** Line L1 takes $O(n \log n)$ comparisons. Lines L3 to L5 make exactly $n$ oracle calls. If one call takes time $f$, the total is $O(n \log n + n f)$.
- **Incremental oracles.** Most oracles are faster when they keep a state for $A$ and test only the new element. For the graphic matroid a [disjoint-set](/disjoint-set/) structure gives $O(\alpha(n))$ amortized time per test, and the algorithm becomes Kruskal's, $O(m \log m)$ for $m$ edges. For a [linear matroid](/linear-matroid/) in $\mathbb{F}^d$, keeping $A$ in echelon form gives $O(r d)$ field operations per test. For a [partition matroid](/partition-matroid/) a counter per block gives $O(1)$.
- **Space.** $\Theta(n)$ for the sorted order and the set $A$, plus the state of the oracle.

## Properties

- **Optimal for every weight function, only on matroids.** On an independence system that is not a matroid, some weights make the algorithm return a set that is not optimal. See the [matroid greedy theorem](/matroid-greedy-theorem/).
- **Gale optimal.** The $k$-th heaviest element of the greedy basis is at least as heavy as the $k$-th heaviest element of any other independent set, for every $k$ (Gale, 1968). So the greedy basis is optimal for every objective that is increasing in each element weight, not only for the sum.
- **Depends only on the order.** The output depends on the weights only through their order, so the same basis is optimal for any increasing transformation of the weights, and the bottleneck problem (maximize the smallest weight in a basis) is solved too.
- **Prefixes.** After $k$ elements have been added, $A$ is a heaviest independent set of size $k$.

## Variants and improvements

- **Maximum-weight independent set.** If weights can be negative and the goal is any independent set, not a basis, stop at the first element with $w(e_i) \le 0$. The prefix of the greedy basis with positive weights is optimal.
- **Minimum-weight basis.** Sort by nondecreasing weight instead, or negate the weights. Kruskal's algorithm for the [minimum spanning tree](/minimum-spanning-tree/) is this form.
- **Worst-out greedy.** Start with $E$ and remove elements by increasing weight as long as the rest still spans $E$. It gives the same optimal basis, by duality: it is the greedy algorithm on the dual matroid.
- **Independence systems.** On a general independence system, the greedy algorithm still returns a feasible set, and its weight is within a factor of the *rank quotient* of the system, the smallest ratio between the sizes of two maximal independent subsets of one set (Jenkyns, Korte and Hausmann). See Korte and Vygen.
- **Two matroids.** For the common independent sets of two matroids, greedy fails; [matroid intersection](/matroid-intersection/) algorithms are needed.

## When to use it

Use it when the feasible sets of a problem form a matroid and the objective is a sum of element weights: spanning trees and forests, linearly independent vectors, at most $k_i$ items per group, unit jobs with deadlines. Proving the exchange property once gives an exact algorithm for every weight function. If the constraint is the intersection of two matroids, such as matchings in a bipartite graph, or not a matroid at all, such as the 0-1 knapsack, use another method.

## Pitfalls

- **Assuming the matroid property.** The algorithm is not optimal on independence systems that are not matroids, such as matchings, independent sets of vertices, or knapsack sets. Prove (I3) before relying on it.
- **Testing only the new element.** Line L4 tests $A \cup \{e_i\}$, not $\{e_i\}$ alone or $e_i$ against the last element added. Partial tests accept dependent sets.
- **Negative weights and the goal.** For a maximum-weight basis, negative elements must still be taken when they are needed to reach a basis. For a maximum-weight independent set, they must not be taken. Mixing the two goals gives wrong answers.
- **Wrong sort direction.** For a maximum the order is nonincreasing; for a minimum, nondecreasing.
- **Slow oracles.** Calling a full independence test from scratch on each $A \cup \{e_i\}$ can cost $\Theta(n)$ times more than an incremental oracle. Keep the state of $A$.

## Implementations

## History

The greedy rule for spanning trees goes back to Borůvka (1926) and Kruskal (1956). Rado proved in 1957 that for an independence system the greedy rule is optimal for all weights exactly when the system is a matroid. Gale (1968) showed that the greedy basis is optimal in the stronger, element-by-element sense. Edmonds (1971), in "Matroids and the greedy algorithm", gave the characterization in the form now used in algorithm texts, with a polyhedral proof, and made the algorithm a standard tool of combinatorial optimization. CLRS presents it as the procedure GREEDY.

## References
