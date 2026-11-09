---
tag: PF1EHJ
kind: theorem
slug: segment-intersection-lower-bound
name: Segment intersection lower bound
aliases:
- segment-intersection-omega-n-log-n
- lower bound for segment intersection detection
area: geometry/intersections
level: advanced
summary: Deciding whether any two of n segments in the plane intersect needs Omega(n log n) steps in the algebraic decision tree model, so reporting needs Omega(n log n + k).
prereqs: [segment-intersection-detection, element-distinctness, algebraic-decision-tree]
see_also: [element-distinctness-lower-bound, ben-or-theorem, shamos-hoey-algorithm, bentley-ottmann-algorithm, all-segment-intersections, chazelle-edelsbrunner-algorithm, algebraic-computation-tree, red-blue-intersection]
sources:
  - paper: doi:10.1109/SFCS.1976.16
    title: Michael Ian Shamos and Dan Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science (FOCS 1976)
    locator: the reduction from element uniqueness that gives the Omega(n log n) lower bound for detecting an intersection among n segments, together with the matching sweep
  - paper: doi:10.1145/800061.808735
    title: Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983)
    locator: the main theorem on the height of algebraic computation trees and its application to element distinctness
  - paper: doi:10.1016/0196-6774(82)90002-5
    title: J. Michael Steele and Andrew C. Yao, Lower bounds for algebraic decision trees, Journal of Algorithms 3(1), 1982
    locator: the main theorem, the component counting bound for algebraic decision trees of fixed degree
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 7, Intersections (the lower bounds by reduction from element uniqueness, and the segment intersection test)
---

The segment intersection lower bound says that any algorithm that decides whether $n$ line segments in the plane contain an intersecting pair needs $\Omega(n \log n)$ operations in the algebraic decision tree model. The proof reduces [element distinctness](/element-distinctness/) to the problem: $n$ numbers become $n$ vertical unit segments, and two segments meet exactly when two numbers are equal. Since element distinctness needs $\Omega(n \log n)$ by the theorems of Steele, Yao and Ben-Or, so does segment intersection. The bound shows that the [Shamos-Hoey sweep](/shamos-hoey-algorithm/) is optimal, and it gives the $\Omega(n \log n + k)$ bound for reporting all $k$ intersections that the Chazelle-Edelsbrunner and Balaban algorithms match.

## Statement

**Notation.** An input is a list of $n$ closed segments $s_i = [p_i, q_i]$ in $\mathbb{R}^2$, written as a point of $\mathbb{R}^{4n}$. The *segment intersection detection* problem asks whether $s_i \cap s_j \ne \emptyset$ for some $i \ne j$; touching at an end point and overlapping collinear segments count as intersections. An *algebraic decision tree of degree $\delta$* tests at each node the sign of a polynomial of degree at most $\delta$ in the input coordinates and branches on $<$, $=$ or $>$; its cost on an input is the length of the path.

**Theorem.** For each fixed $\delta$ there is a constant $c > 0$ such that every algebraic decision tree of degree $\delta$ that solves segment intersection detection for $n$ segments has depth at least $c\, n \log n - O(n)$. The same holds for algebraic computation trees, in which each node does an arithmetic operation or a square root, or tests a sign. Consequently, every algorithm that reports all $k$ intersecting pairs needs $\Omega(n \log n + k)$ steps in these models.

## In plain words

Some questions about $n$ numbers are hard: for example, "are all these numbers different?" A program that may only do arithmetic and comparisons needs about $n \log n$ steps for it, as much as sorting.

That question hides inside segment intersection. Turn each number $x$ into a short upright segment that stands at position $x$. Two segments touch exactly when they stand at the same position, that is, when two numbers are equal. So a fast test for crossing segments would give a fast test for equal numbers, which is impossible. Hence finding whether any segments cross also needs about $n \log n$ steps.

## Proof

**Lemma 1 (element distinctness).** For each fixed $\delta$, every algebraic decision tree of degree $\delta$ that decides whether $x_1, \dots, x_n \in \mathbb{R}$ are pairwise distinct has depth at least $c_\delta\, n \log n - O(n)$, and the same holds for algebraic computation trees.

*Proof.* The set $W = \{x \in \mathbb{R}^n : x_i \ne x_j \text{ for } i \ne j\}$ has $n!$ connected components, one for each order of the coordinates, because two points with different orders are separated by a hyperplane $x_i = x_j$ that $W$ avoids, and the points with one order form a convex set. By the theorem of Steele and Yao for decision trees of fixed degree, and of [Ben-Or](/ben-or-theorem/) for computation trees, a tree that decides $W$ has depth at least $c_1 \log(n!) - c_2 n$, and $\log(n!) = \Theta(n \log n)$; see [the element distinctness lower bound](/element-distinctness-lower-bound/). $\square$

**Lemma 2 (reduction).** Map $x = (x_1, \dots, x_n)$ to the segments $s_i(x) = [(x_i, 0), (x_i, 1)]$. Then $s_i(x) \cap s_j(x) \ne \emptyset$ if and only if $x_i = x_j$.

*Proof.* Every point of $s_i(x)$ has first coordinate $x_i$. If $x_i \ne x_j$, the two segments lie on different vertical lines and are disjoint. If $x_i = x_j$, they are the same segment, so they meet. $\square$

**Proof of the theorem.** Let $T$ be a tree of degree $\delta$ and depth $h$ that solves segment intersection detection for $n$ segments. Replace each input coordinate of $T$ by its value under the map of Lemma 2: the coordinates of $p_i$ become $x_i$ and $0$, those of $q_i$ become $x_i$ and $1$. Each test polynomial of degree at most $\delta$ in the $4n$ coordinates becomes a polynomial of degree at most $\delta$ in $x$, because the map is affine. The new tree $T'$ has depth $h$, and on input $x$ it follows the path of $T$ on the segments $s_i(x)$, so it answers "some pair intersects" exactly when, by Lemma 2, some $x_i = x_j$. So $T'$ decides element distinctness, and Lemma 1 gives $h \ge c_\delta\, n \log n - O(n)$. For computation trees, the substitution adds $O(1)$ nodes for each input coordinate on a path, at most $O(n)$ in total, so the same bound holds up to the $O(n)$ term.

For reporting, an algorithm that lists all intersecting pairs also decides whether the list is empty, so it needs $\Omega(n \log n)$ steps, and it must write $k$ pairs, which needs $\Omega(k)$ steps. Together this is $\Omega(\max(n \log n, k)) = \Omega(n \log n + k)$. $\blacksquare$

## Consequences

- **Shamos-Hoey is optimal.** The [Shamos-Hoey algorithm](/shamos-hoey-algorithm/) decides the problem in $O(n \log n)$ time, so detection is $\Theta(n \log n)$ in the algebraic decision tree model.
- **Optimal reporting.** [Bentley-Ottmann](/bentley-ottmann-algorithm/) takes $O((n + k) \log n)$, which is not optimal when $k$ is large. The [Chazelle-Edelsbrunner algorithm](/chazelle-edelsbrunner-algorithm/) and Balaban's algorithm take $O(n \log n + k)$, which matches the bound.
- **Related problems.** The same reduction with the intervals $[x_i, x_i]$ or the rectangles $[x_i, x_i] \times [0, 1]$ gives $\Omega(n \log n)$ for interval overlap, for [rectangle intersection detection](/rectangle-intersection-detection/), and for any intersection test of $n$ objects that contains these as special cases.

## Tightness

- **Upper bound.** The bound is tight: the Shamos-Hoey sweep matches it.
- **Degenerate inputs.** The reduction uses identical segments. They are legal inputs, so they show the worst case of the problem as defined; a bound for inputs in general position, with only proper crossings, needs a different construction, which this page does not give.
- **Special inputs.** The bound does not hold for every structured input. For the $n$ edges of a closed polygonal chain, simplicity can be tested in $O(n)$ time with Chazelle's linear-time triangulation, so the lower bound needs segments in arbitrary arrangement.
- **Other models.** The proof needs a model where Ben-Or's theorem applies. On the word RAM with integer coordinates, element distinctness takes $O(n)$ expected time by hashing, so the reduction gives no $\Omega(n \log n)$ bound there.

## History

Shamos and Hoey proved the $\Omega(n \log n)$ bound for segment intersection detection in 1976, by reduction from element uniqueness, together with their matching sweep. At that time the lower bound for element uniqueness was known for linear decision trees, by Dobkin and Lipton; Steele and Yao (1982) and Ben-Or (1983) extended it to algebraic decision trees and algebraic computation trees, which extended the segment bound to these models. The reporting bound $\Omega(n \log n + k)$ was matched by Chazelle and Edelsbrunner in 1988 and by Balaban in 1995.

## References
