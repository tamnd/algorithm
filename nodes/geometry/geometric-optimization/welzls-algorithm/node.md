---
tag: BA4QGE
kind: algorithm
slug: welzls-algorithm
name: Welzl's algorithm
aliases:
- move-to-front minimum enclosing ball
- Welzl's randomized algorithm
- MINIDISK
- Welzl's smallest enclosing disk algorithm
area: geometry/geometric-optimization
level: core
summary: Randomized incremental algorithm for the smallest enclosing disk or ball. A point outside the current disk forces a recomputation with it on the boundary; expected O(n) time.
solves: [minimum-enclosing-circle, minimum-enclosing-ball]
model: real-ram
complexity:
  vars: {n: the number of input points in the plane}
  time: {expected: O(n), worst: O(n^3)}
  space: {extra: O(n)}
properties: {online: false, deterministic: false, recursive: true}
history:
  year: 1991
  people: [Emo Welzl]
  note: Welzl gave the recursion on the boundary set, its backwards analysis with at most 10n expected containment tests in the plane, and the move-to-front heuristic.
prereqs: [minimum-enclosing-circle, randomized-incremental-construction, backwards-analysis, circumcircle]
see_also: [minimum-enclosing-ball, lp-type-problem, megiddo-fixed-dimension-lp, seidel-linear-programming, clarksons-algorithm, badoiu-clarkson-algorithm, minimum-volume-enclosing-ellipsoid, prune-and-search]
sources:
  - paper: doi:10.1007/BFb0038202
    title: Emo Welzl, Smallest enclosing disks (balls and ellipsoids), in New Results and New Trends in Computer Science, Lecture Notes in Computer Science 555, Springer, 1991
    locator: Section 2 (procedure MINIDISK, Lemma 1, recursion (1) with t_1(n) ≤ n, t_2(n) ≤ 3n, t_3(n) ≤ 10n, Theorem 2) and Section 3 (balls, Theorem 3, ellipsoids, one permutation, the move-to-front heuristic)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: Chapter 4, Section 4.7, Smallest enclosing discs (the iterative form with three nested loops and the backwards analysis)
  - paper: doi:10.1007/BF02574699
    title: Raimund Seidel, Small-dimensional linear programming and convex hulls made easy, Discrete and Computational Geometry 6, 1991
    locator: the randomized linear programming algorithm whose analysis Welzl's proof follows
  - paper: "Bernd Gärtner, Fast and robust smallest enclosing balls, Proceedings of the 7th European Symposium on Algorithms (ESA 1999), Lecture Notes in Computer Science 1643, Springer, 1999"
    locator: the move-to-front implementation with an array and a pivoting rule for balls in higher dimension
---

Welzl's algorithm computes the smallest disk that contains $n$ given points in the plane, and in the same form the smallest ball in $\mathbb{R}^d$. It solves the [minimum enclosing circle problem](/minimum-enclosing-circle/) in expected $O(n)$ time on the [real RAM](/real-ram/). It is a [randomized incremental construction](/randomized-incremental-construction/): it adds the points in random order, and when a point falls outside the current disk, it computes a new disk that must have that point on its boundary. The expected cost comes from [backwards analysis](/backwards-analysis/), and the method is the standard example of an [LP-type problem](/lp-type-problem/) solved by random sampling.

## In plain words

Put the points in a random order. Keep the smallest circle around the points you have seen so far. Take the next point. If it is inside the circle, do nothing. If it is outside, the new smallest circle must touch this point. So start again with the earlier points, but now with the rule that the circle must pass through the new point. Inside that pass, a point that falls outside gives a second point that the circle must touch, and a third one fixes the circle completely, because three points fix one circle.

A point falls outside only when it is one of the two or three points that hold the circle up. In a random order this is rare for late points, so the restarts are cheap on average, and the total work is a small multiple of the number of points.

## The problem

Notation: $P$ is the input point set with $n = |P|$ points $p = (x, y)$, and $d$ is the dimension ($d = 2$ unless we say otherwise). For finite sets $P$ and $R$, let $\mathrm{md}(P, R)$ be the smallest closed disk that contains $P$ and has every point of $R$ on its boundary circle, if such a disk exists. The answer is $\mathrm{md}(P, \emptyset)$, the [minimum enclosing circle](/minimum-enclosing-circle/) of $P$. For $P = R = \emptyset$ there is no disk, and the code returns nothing. No general position is assumed: duplicate points, collinear points and many points on one circle are all allowed.

## The algorithm

The array form below is iterative in the points and recursive only on $R$, so the recursion depth is at most 4. Line L8 is Welzl's move-to-front heuristic. Without line L8 the algorithm is the one-permutation version, which is the version with the proved expected bound.

```pseudo id=main
MINIDISK(P)                          ▷ P is an array of n points
L1  put P in a uniformly random order
L2  return B-MTF(P, n, ∅)

B-MTF(P, m, R)                       ▷ returns md(P[0..m−1], R), with |R| ≤ 3
L3  D ← the smallest disk with R on its boundary   ▷ none, a point, a diameter disk or a circumcircle
L4  if |R| = 3 then return D
L5  for i ← 0 to m − 1 do
L6      if P[i] ∉ D then
L7          D ← B-MTF(P, i, R ∪ {P[i]})
L8          move P[i] to the front of P              ▷ optional heuristic
L9  return D
```

Line L3 has four cases. For $R = \emptyset$ there is no disk, so the first point fails the test of line L6. For one point the disk has radius 0. For two points $a, b$ the disk has center $(a + b)/2$ and radius $|a - b|/2$. For three points it is the [circumcircle](/circumcircle/). Line L8 permutes only $P[0..i]$, so the loop of the caller, which works on positions after $i$, does not see the move.

With integer or rational input, every center and squared radius is rational, and the test of line L6 compares $(x - c_x)^2 + (y - c_y)^2$ with $r^2$ exactly. No square root is needed. Three points that reach line L3 together are never collinear (the proof below shows this), so the circumcircle always exists.

## Example

Take $P = \{(0, 0), (6, 0), (2, 4), (3, 1), (5, 3), (1, 2)\}$, and suppose line L1 gives the order $(3, 1), (5, 3), (0, 0), (6, 0), (1, 2), (2, 4)$, a bad order with the inner points first. The table shows the top-level loop; a disk is written as its center and its squared radius.

| step | point | in the disk? | new disk | boundary of the new disk |
|---|---|---|---|---|
| 1 | (3, 1) | no (no disk yet) | (3, 1), 0 | (3, 1) |
| 2 | (5, 3) | no | (4, 2), 2 | (5, 3), (3, 1) |
| 3 | (0, 0) | no | (5/2, 3/2), 17/2 | (0, 0), (5, 3) |
| 4 | (6, 0) | no | (3, 2/3), 85/9 | (6, 0), (0, 0), (5, 3) |
| 5 | (1, 2) | yes | | |
| 6 | (2, 4) | no | (3, 1), 10 | (2, 4), (6, 0), (0, 0) |

At step 6 the call B-MTF$(P, 5, \{(2, 4)\})$ runs over the first five points. It meets $(3, 1)$, then $(5, 3)$, then $(0, 0)$ and $(6, 0)$ outside its current disk, and the last of these gives the circle through $(2, 4)$, $(6, 0)$ and $(0, 0)$. The answer is the disk with center $(3, 1)$ and radius $\sqrt{10}$. The points $(0, 0)$, $(6, 0)$ and $(2, 4)$ lie on its circle, $(5, 3)$ is at squared distance 8 and $(1, 2)$ at squared distance 5. In this order the algorithm makes 27 containment tests in all levels.

## Correctness

Three facts about $\mathrm{md}$ drive the proof. If some disk contains $P$ and has $R$ on its boundary, the smallest such disk exists and is unique. If $p \notin \mathrm{md}(P \setminus \{p\}, R)$, then $p$ lies on the boundary of $\mathrm{md}(P, R)$, so $\mathrm{md}(P, R) = \mathrm{md}(P \setminus \{p\}, R \cup \{p\})$. And some set of at most $3 - |R|$ points of $P$ already fixes $\mathrm{md}(P, R)$. Both uniqueness and the boundary fact come from one tool: for two disks given by $f_0(x) = |x - z_0|^2 - r_0^2 \le 0$ and $f_1(x) \le 0$, each convex combination $(1 - \lambda) f_0 + \lambda f_1$ again describes a disk. It contains all the points that both disks contain, it passes through all the points that both circles pass through, and its squared radius is $(1 - \lambda) r_0^2 + \lambda r_1^2 - \lambda (1 - \lambda) |z_0 - z_1|^2$.

The [loop invariant](/loop-invariant/) of line L5 is: before iteration $i$, $D = \mathrm{md}(P[0..i-1], R)$. A point inside $D$ keeps it the answer. A point outside forces itself onto the boundary, and the recursive call of line L7 computes exactly that disk. The full proof, with termination and the expected cost, is below.

## Complexity

Count the containment tests of line L6. Let $t_j(m)$ be the largest expected number of tests of a call B-MTF$(P, m, R)$ with $|R| = 3 - j$, over all inputs, in the version without line L8. By backwards analysis, the point $P[i]$ is uniformly random among the first $i + 1$ points, and it fails the test only if it is one of the at most $j$ points that fix $\mathrm{md}(P[0..i], R)$. So the probability of a recursive call at step $i$ is at most $j / (i + 1)$, and

$$t_j(m) \le \sum_{i=0}^{m-1} \Big(1 + \frac{j}{i + 1}\, t_{j-1}(i)\Big), \qquad t_0(m) = 0.$$

This gives $t_j(m) \le c_j m$ with $c_0 = 0$ and $c_j = 1 + j\, c_{j-1}$, so $c_1 = 1$, $c_2 = 3$ and $c_3 = 10$. The expected number of tests is at most $10n$, and each test and each base disk takes $O(1)$ time.

- **Expected time:** $O(n)$ in the plane, for every input. The expectation is over the random order only.
- **Worst case over the random choices:** each of the three loop levels runs at most $n$ times, so at most $n + n^2 + n^3$ tests.
- **Dimension $d$:** replace 3 by $\delta = d + 1$. The same recursion gives $c_\delta = \sum_{k=1}^{\delta} \delta!/k! = \lfloor (e - 1)\, \delta! \rfloor$, so at most $(e - 1)(d + 1)!\, n$ expected tests, each of $O(d)$ arithmetic operations. Welzl states the bound as $O(\delta\, \delta!\, n)$ time.
- **Base disks:** Welzl shows that the expected number of evaluations of line L3 is at most $(1 + H_n)^\delta$, where $H_n$ is the $n$-th harmonic number.
- **Space:** $O(n)$ for the array, and $O(d)$ frames of recursion.

The constant 10 is a proved bound. Welzl reports that about $10n$ tests is also what one observes for points uniform in a disk. The move-to-front version of line L8 is faster in experiments, but Welzl left its expected-time analysis open, and this page does not claim a bound for it.

## Properties

- **Las Vegas.** The answer is always exact; only the running time depends on the random order. See [Las Vegas algorithm](/las-vegas-algorithm/).
- **Exact on rational input.** The disks have rational centers and squared radii, so the test of line L6 needs no tolerance.
- **No general position.** Duplicates are inside every disk that has their twin on the boundary. Collinear and cocircular points need no special case.
- **Not online.** The bound needs the random order of the whole input. Points that arrive in an order chosen by an adversary can force $\Theta(n)$ recomputations.
- **Shallow recursion.** The recursion is on $R$ only, so its depth is at most $d + 2$ frames.

## Variants and improvements

- **Three nested loops.** de Berg et al. write the planar version as MINIDISC, MINIDISCWITHPOINT and MINIDISCWITH2POINTS, the same algorithm with the recursion unrolled.
- **Balls in $\mathbb{R}^d$.** The same code with $|R| \le d + 1$ and a base case that computes the smallest ball with $R$ on its boundary in the affine hull of $R$. See [minimum enclosing ball](/minimum-enclosing-ball/).
- **Ellipsoids.** Welzl applies the same scheme to the smallest enclosing ellipsoid, with $\delta = d(d + 3)/2$. See [minimum-volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/).
- **LP-type problems.** Sharir and Welzl turned the scheme into an algorithm for any [LP-type problem](/lp-type-problem/), which gives subexponential bounds in the dimension.
- **Deterministic linear time.** Megiddo's [prune-and-search](/prune-and-search/) method solves the planar problem in $O(n)$ worst-case time, but with a large constant.
- **Pivoting.** Gärtner's code for balls in moderate dimension combines move-to-front with a pivoting rule and floating-point arithmetic with careful checks.

## When to use it

Use Welzl's algorithm for the exact smallest enclosing circle or sphere in low dimension. It is short, exact with rational arithmetic, and fast in practice. For dimension above about 10 the factor $(d + 1)!$ grows too fast; use the [Badoiu-Clarkson](/badoiu-clarkson-algorithm/) iteration or a second-order cone solver for an approximate ball instead.

## Pitfalls

- **No shuffle.** Without line L1 a sorted input can make every point fail the test, and the time becomes quadratic or worse.
- **Deep recursion.** Welzl's text removes one point per call, which gives recursion depth $n$. In Python this overflows the stack. The loop form above has depth at most $d + 2$.
- **Floating-point tests.** With floats the test of line L6 can fail for a point on the circle, and the algorithm can recurse with three nearly collinear points. Use exact arithmetic, or compare against $r^2 (1 + \varepsilon)$ and accept an approximate answer.
- **Two points is not always a diameter.** With two boundary points and other points to cover, the answer can be a larger circle through both points. Only the base case of line L3 uses the diameter disk.
- **Line L8 with a plain list.** Moving an item to the front of an array costs $O(n)$. Use a linked list, or count this cost.

## Implementations

## History

Welzl published the algorithm in 1991. He credits the analysis to the method of Seidel's randomized linear programming algorithm of the same year, which is an early example of backwards analysis. In the same paper he extends the method to balls and ellipsoids, shows that one random permutation is enough, and proposes the move-to-front heuristic. Earlier, Megiddo had solved the planar problem in deterministic linear time in 1983.

## References
