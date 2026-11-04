---
tag: 51HZBR
kind: technique
slug: reduction-lower-bound
name: Lower bounds by reduction
aliases:
- lower bound by reduction
- reduction-based lower bound
- transfer of lower bounds
area: foundations/lower-bounds
level: core
summary: If a problem with a known lower bound reduces cheaply to a new problem inside the same model of computation, the new problem inherits that bound minus the cost of the reduction.
prereqs: [reduction, lower-bound, decision-tree-model]
see_also: [element-distinctness-lower-bound, ben-or-theorem, comparison-sort-lower-bound, convex-hull-problem, 3sum-hardness, conditional-lower-bound, closest-pair-of-points, algebraic-computation-tree]
sources:
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 3, Convex hulls, basic algorithms (the lower bound by reduction from sorting); Chapter 5, Proximity, fundamental algorithms (reductions from element uniqueness)
  - paper: doi:10.1145/322276.322289
    title: "Andrew Chi-Chih Yao, A lower bound to finding convex hulls, Journal of the ACM 28(4) (1981), 780-787"
    locator: the main theorem (Omega(n log n) for identifying the hull vertices in the quadratic decision tree model)
  - paper: doi:10.1016/0925-7721(95)00022-2
    title: "Anka Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry 5(3) (1995), 165-185"
    locator: the definition of 3SUM-hard problems and the reductions between them
  - paper: doi:10.1145/800061.808735
    title: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), 80-86"
    locator: the model of algebraic computation trees and the bound for element distinctness, the usual source problem of reductions
---

A lower bound by reduction proves that a new problem $B$ is hard by showing that a problem $A$ with a known lower bound can be solved with the help of $B$. If an instance of $A$ of size $n$ turns into an instance of $B$ of size $s(n)$ with $r(n)$ extra steps, then $B$ needs at least $T_A(n) - r(n)$ steps on size $s(n)$. The transfer is valid only when the reduction runs inside the same [model of computation](/decision-tree-model/) as the bound for $A$. It is how most $\Omega(n \log n)$ bounds of computational geometry follow from [sorting](/comparison-sort-lower-bound/) and [element distinctness](/element-distinctness-lower-bound/), and how [conditional lower bounds](/conditional-lower-bound/) follow from 3SUM.

## In plain words

Suppose you already know that one job is hard. You want to show that a second job is hard too. Show how to do the first job with a fast machine for the second job and a little extra work. If the second job were easy, the first job would then be easy as well, and you know it is not. So the second job is hard.

Two details decide whether the argument works. The extra work must be small compared with the known bound, or nothing is left of it. And the extra work must use only the steps that the known bound allows. A bound proved for programs that only compare numbers says nothing about a program that also does arithmetic or hashing.

## When it applies

- You have a problem $A$ with a lower bound $T_A(n)$ in a model $M$, such as the [comparison model](/comparison-model/) or the [algebraic computation tree](/algebraic-computation-tree/).
- An instance of $A$ can be encoded as an instance of the new problem $B$ with a few operations of $M$, and the answer of $B$ gives the answer of $A$ with a few more operations of $M$.
- The size of the encoded instance is linear, or at least small, in the size of the original one.
- For a conditional bound, $A$ is a problem that is believed hard, such as 3SUM, and the claim is "if $B$ is fast, then $A$ is fast".

## The template

Fix a model $M$ in which an algorithm for one input size is a program (a tree, or a RAM program) and the cost is the worst-case number of steps. Let $T_P(n)$ be the smallest worst-case cost of an $M$-algorithm that solves problem $P$ on all instances of size $n$.

A *reduction of $A$ to $B$ in $M$ with size $s(n)$ and cost $r(n) = r_1(n) + r_2(n)$* is a pair of $M$-procedures. TRANSFORM maps an instance $x$ of $A$ of size $n$ to an instance $y$ of $B$ of size $s(n)$ in at most $r_1(n)$ steps. RECOVER maps $x$ and a correct answer $z$ for $y$ to a correct answer for $x$ in at most $r_2(n)$ steps.

```pseudo id=template
SOLVE-A(x)                   ▷ x an instance of A of size n
L1  y ← TRANSFORM(x)           ▷ at most r1(n) steps of M, |y| = s(n)
L2  z ← SOLVE-B(y)             ▷ any M-algorithm for B on size s(n)
L3  return RECOVER(x, z)       ▷ at most r2(n) steps of M
```

**Lemma (transfer).** If $M$ allows composition (the program of line L2 may take as inputs the values computed in line L1), then $T_A(n) \le r(n) + T_B(s(n))$. Hence

$$T_B(s(n)) \ \ge\ T_A(n) - r(n).$$

*Proof.* Take an optimal $M$-algorithm for $B$ on size $s(n)$, with worst-case cost $T_B(s(n))$. Put it in line L2. SOLVE-A is an $M$-algorithm for $A$ on size $n$, and on every input it uses at most $r_1(n) + T_B(s(n)) + r_2(n)$ steps. By the definition of $T_A(n)$ as the least such worst-case cost, $T_A(n) \le r(n) + T_B(s(n))$. $\square$

In a tree model, composition means: below each leaf of the tree for TRANSFORM, hang the tree for $B$, with each input of $B$ replaced by the computed value; below each leaf of that tree, hang the tree for RECOVER. The height of the result is at most the sum of the heights.

**Corollary (the usual form).** Let $T_A(n) \ge g(n)$, $r(n) = o(g(n))$, $s(n) \le c n$ for a constant $c \ge 1$, and let $T_B$ be non-decreasing. Then for $m \ge c$ and $n = \lfloor m/c \rfloor$, $T_B(m) \ge T_B(s(n)) \ge g(n) - r(n)$. With $g(n) = \Omega(n \log n)$ and $r(n) = O(n)$ this gives $T_B(m) = \Omega(m \log m)$.

## Classic examples

The examples go from simple to hard. Each states the model, the reduction and its cost.

### Sorting to a priority queue (comparison model)

Insert the $n$ items into a comparison-based [priority queue](/priority-queue/), then call extract-min $n$ times. The output is the sorted order, and the reduction adds no comparisons. A comparison sort needs $\lceil \lg n! \rceil$ comparisons in the worst case ([comparison sort lower bound](/comparison-sort-lower-bound/)). So $2n$ operations cost at least $\lg n!$ comparisons, and the amortized cost of insert plus extract-min is at least $\lg(n!)/n = \lg n - \lg e + o(1)$. For $n = 10^6$ this is about $18.49$ comparisons per pair of operations. A [binary heap](/binary-heap/) meets this up to a constant factor. No comparison-based priority queue has both operations in $o(\log n)$ amortized comparisons.

### Element distinctness to closest pair (algebraic computation tree)

Given $x_1, \ldots, x_n$, form the points $(x_i, 0)$ and run a tree that outputs a closest pair $(i, j)$. Then compute $x_i - x_j$ and test it for zero: $r(n) = 2$ nodes. The numbers are distinct if and only if the test says "not zero". Element distinctness needs height $\Omega(n \log n)$ in this model ([element distinctness lower bound](/element-distinctness-lower-bound/)), so the [closest pair of points](/closest-pair-of-points/) needs it too. The reduction uses only a subtraction and a sign test, which are operations of the model.

### Sorting to convex hull (algebraic computation tree)

This reduction is due to Shamos and is in Preparata and Shamos (1985). Given distinct reals $x_1, \ldots, x_n$, form the points $p_i = (x_i, x_i^2)$ on the parabola $y = x^2$, with $n$ multiplications. Run a tree for the [convex hull problem](/convex-hull-problem/) that outputs the indices of the hull vertices in counterclockwise order. Then find the vertex with the smallest $x_i$ with $n - 1$ comparisons and rotate the cycle to start there. The result is the sorted order.

*Why it is correct.* For $a < b < c$, the point of the chord from $(a, a^2)$ to $(c, c^2)$ above $b$ has height $a^2 + (b - a)(a + c)$, and

$$b^2 - \bigl(a^2 + (b - a)(a + c)\bigr) = (b - a)(b + a) - (b - a)(a + c) = (b - a)(b - c) < 0.$$

So every point lies strictly below the chord between any point on its left and any point on its right. In particular all points except the leftmost and the rightmost lie strictly below the segment that joins those two, so the upper part of the hull is this one edge. The chain through the points in increasing order of $x$ has slopes $x_i + x_{i+1}$ between neighbours, which increase, so it is convex and forms the lower part of the hull. Every point is a vertex, and the counterclockwise order from the leftmost vertex is the increasing order of $x$.

*Example.* For $x = (3, -1, 2, 0, -2)$ the points are $(3, 9)$, $(-1, 1)$, $(2, 4)$, $(0, 0)$, $(-2, 4)$. The counterclockwise hull from the leftmost vertex is $(-2, 4), (-1, 1), (0, 0), (2, 4), (3, 9)$, that is, the indices $5, 2, 4, 3, 1$, which list $-2, -1, 0, 2, 3$ in sorted order.

*The bound.* A tree that sorts, with the sorted order of indices as output, needs a separate leaf for each of the $n!$ orders, since each order is the only correct answer on an open set of inputs, and so it has height at least $\lg n!$. Each comparison of the recovery step is one subtraction and one test, so $r(n) \le n + 2(n - 1)$, and the hull tree has height at least $\lg n! - 3n + 2 = \Omega(n \log n)$. The reduction uses multiplication. So the sorting bound used here must hold for algebraic computation trees, not only for comparison trees; it does, by the leaf count above.

The reduction says nothing about a hull algorithm that outputs only the set of hull vertices, without the order, since on the parabola every point is a vertex. Yao (1981) proved $\Omega(n \log n)$ for that weaker output in the quadratic decision tree model by a separate argument.

### 3SUM to three collinear points (conditional)

Let 3SUM ask whether a set $S$ of $n$ distinct reals has three distinct members $a, b, c$ with $a + b + c = 0$. Map each $x \in S$ to the point $(x, x^3)$. For distinct $a$ and $b$ the slope between $(a, a^3)$ and $(b, b^3)$ is $(b^3 - a^3)/(b - a) = a^2 + ab + b^2$. For distinct $a, b, c$ the three points are collinear if and only if $a^2 + ab + b^2 = b^2 + bc + c^2$, that is, $(a - c)(a + b + c) = 0$, that is, $a + b + c = 0$. So $S$ is a yes-instance of 3SUM exactly when some three of the points lie on a line ([collinear points](/collinear-points/)). For $S = \{-5, 1, 4, 7\}$ the triple $-5, 1, 4$ sums to $0$, and the slopes from $(-5, -125)$ to $(1, 1)$ and from $(1, 1)$ to $(4, 64)$ are both $21$.

The reduction takes $O(n)$ time. It gives no unconditional bound. It shows: if three collinear points can be found in $O(n^{2 - \delta})$ time for a constant $\delta > 0$, then so can 3SUM. Gajentaan and Overmars (1995) called a problem [3SUM-hard](/3sum-hardness/) when 3SUM reduces to it in this sense, and showed that many problems of computational geometry are 3SUM-hard.

## Variations

- **Several calls.** A Turing reduction calls $B$ more than once. Then $T_A(n) \le r(n) + \sum_i T_B(s_i(n))$, and the bound for $B$ is divided among the calls.
- **Conditional lower bounds.** When $A$ has no proved lower bound but is conjectured hard (3SUM, all-pairs shortest paths, the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/)), a reduction gives a [conditional lower bound](/conditional-lower-bound/). The reduction must then be fast in the usual sense, for example $O(n^{2 - \delta})$ for 3SUM, and runs on a RAM.
- **Data structures.** A data structure solves a static problem by a sequence of operations, as in the priority queue example. The bound then applies to the amortized cost of the operations.
- **Other cost measures.** In [communication complexity](/communication-complexity/) and in the [cell probe model](/cell-probe-lower-bound/), a reduction maps a hard problem to a new one while keeping the communication or the number of probes. The template is the same, with the cost measured in bits or probes.
- **Average case.** To transfer a bound on the average cost, the reduction must map the hard input distribution of $A$ to a distribution on $B$ for which the bound is wanted.

## Pitfalls

- **The wrong direction.** To show that $B$ is hard, reduce the hard problem $A$ to $B$. Reducing $B$ to $A$ (for example, deciding element distinctness by sorting) gives an upper bound for $B$ and no lower bound for anything.
- **A reduction outside the model.** The reduction must use only operations of the model in which the bound for $A$ holds. A reduction with the floor function or with hashing breaks a bound for algebraic trees: with floor, the maximum gap of $n$ reals takes $O(n)$ time by bucketing. A reduction that computes $x_i^2$ cannot use a bound that is proved only for comparison trees.
- **The format of the output.** The convex hull reduction needs the hull in order. The sorting bound in a tree with arithmetic needs the output as indices: with square roots, $\min(a, b) = \bigl(a + b - \sqrt{(a - b)^2}\bigr)/2$ is computed without any branch, so a leaf that outputs values can be correct on several orders, and the leaf count fails.
- **A costly reduction.** If $r(n)$ is not $o(T_A(n))$, the bound $T_A(n) - r(n)$ can be zero or negative. A reduction from sorting that costs $\Theta(n \log n)$ proves nothing.
- **Size blow-up.** If $s(n)$ grows faster than $n$, the bound in terms of the size of $B$ is weaker. With $s(n) = n^2$ and $T_A(n) = \Omega(n \log n)$, one gets only $T_B(m) = \Omega(\sqrt{m} \log m)$.
- **Domain of the inputs.** A bound for real inputs does not hold for integer inputs on a [word RAM](/word-ram/), where element distinctness takes $O(n)$ expected time with hashing. The reduction must map the hard instances of $A$ to instances that $B$ allows.
- **Conditional is not unconditional.** A 3SUM-hardness result says "no faster than 3SUM". It does not prove any bound on its own.

## Exercises

1. Reduce element distinctness to the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) of $n$ points in the plane, in the algebraic computation tree model, and give the cost $r(n)$ of the reduction.
2. Prove that no comparison-based priority queue supports insert and extract-min both in $o(\log n)$ amortized comparisons.
3. In the convex hull reduction, let the hull tree output the cycle starting at any vertex. Write the recovery step and count its nodes. Then show that, if the hull tree must start at the leftmost vertex, the recovery step needs no node.
4. Prove that the points $(a, a^3)$, $(b, b^3)$, $(c, c^3)$ with $a, b, c$ distinct are collinear if and only if $a + b + c = 0$, and find all such triples in $\{-6, -2, 1, 3, 5, 8\}$.
5. Problem $A$ needs $\Omega(n \log n)$ and reduces to $B$ with $s(n) = n^2$ and $r(n) = O(n^2)$. What does the transfer lemma give for $B$? Explain the result.
6. Explain why "element distinctness reduces to sorting in $n - 1$ extra comparisons" gives no lower bound for sorting.
7. The maximum gap problem asks for the largest difference between neighbours in the sorted order of $n$ reals. Find the step of the bucket algorithm that is not an operation of an algebraic computation tree.

## References
