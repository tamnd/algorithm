---
tag: 0SY9GZ
kind: concept
slug: lp-type-problem
name: LP-type problem
aliases:
- LP-type problems
- generalized linear programming
- abstract linear programming
area: geometry/geometric-optimization
level: advanced
summary: An abstract optimization problem with monotonicity and locality, like linear programming. Small bases and violation tests give randomized linear-time algorithms.
prereqs: [linear-programming-problem, seidel-linear-programming, backwards-analysis]
see_also: [welzls-algorithm, clarksons-algorithm, chans-randomized-optimization, minimum-enclosing-ball, minimum-volume-enclosing-ellipsoid, megiddo-fixed-dimension-lp, prune-and-search, helly-theorem]
sources:
  - paper: "Micha Sharir and Emo Welzl, A combinatorial bound for linear programming and related problems, STACS 92, Lecture Notes in Computer Science 577, Springer, 1992"
    locator: the definition of LP-type problems by monotonicity and locality, bases and combinatorial dimension, and the randomized recursive algorithm
  - paper: doi:10.1007/BF01940877
    title: Jiří Matoušek, Micha Sharir and Emo Welzl, A subexponential bound for linear programming, Algorithmica 16, 1996
    locator: the subexponential bound on the expected number of violation tests and basis computations, and its combination with Clarkson's algorithm
  - paper: doi:10.1145/201019.201036
    title: Kenneth L. Clarkson, Las Vegas algorithms for linear and integer programming when the dimension is small, Journal of the ACM 42(2), 1995
    locator: Section 2 (the recursive and iterative algorithms) and Lemmas 3.1 and 3.2 (violators contain a basis element, and the expected number of violators)
  - paper: "Bernd Gärtner and Emo Welzl, A simple sampling lemma, analysis and applications in geometric optimization, Discrete and Computational Geometry 25(4), 2001"
    locator: the sampling lemma that bounds the expected number of violators of a random sample
  - paper: "Emo Welzl, Smallest enclosing disks (balls and ellipsoids), New Results and New Trends in Computer Science, Lecture Notes in Computer Science 555, 1991"
    locator: the combinatorial dimensions d + 1 for balls and d(d + 3)/2 for ellipsoids
---

An LP-type problem is a pair $(H, w)$ of a finite set $H$ of constraints and a value function $w$ on the subsets of $H$ that is monotone and local, the two combinatorial properties of [linear programming](/linear-programming-problem/) that randomized algorithms use. Sharir and Welzl (1992) defined the class. Each subset has a basis, a minimal subset with the same value, and if every basis has at most $\delta$ elements, the problem has combinatorial dimension $\delta$. Linear programming in $d$ variables, the [minimum enclosing ball](/minimum-enclosing-ball/) in $\mathbb{R}^d$ and the [minimum volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/) are LP-type, with $\delta = d$, $d + 1$ and $d(d + 3)/2$. For fixed $\delta$, the algorithms of Seidel, [Welzl](/welzls-algorithm/), [Clarkson](/clarksons-algorithm/) and Matoušek, Sharir and Welzl solve every such problem in expected $O(n)$ time from two primitives: a violation test and a basis computation for $\delta + 1$ constraints.

## In plain words

Many problems ask for the best answer that satisfies a list of conditions: the smallest circle that holds all the points, or the lowest point in a region cut out by straight lines. These problems share two traits. Adding a condition never makes the best answer better. And the best answer is held in place by only a few of the conditions; the rest could be dropped without any change.

An LP-type problem is any problem with these traits, written down in an abstract way. The payoff is that one algorithm works for all of them. Take the conditions in random order, keep the best answer for the ones seen so far, and repair it only when a new condition breaks it. Because only a few conditions hold the answer in place, repairs are rare, and the total work is linear.

## The idea

Notation: $H$ is a finite set with $n = |H|$ elements, the constraints; $W$ is a totally ordered set with a least element $-\infty$; and $w : 2^H \to W$ is the value function. Read $w(G)$ as the optimum of the problem with only the constraints $G$; $-\infty$ is the value of the empty problem, or of a problem without constraints that bind.

**Definition** (Sharir and Welzl 1992). $(H, w)$ is an LP-type problem if for all $F \subseteq G \subseteq H$:

1. **Monotonicity.** $w(F) \le w(G)$.
2. **Locality.** If $-\infty < w(F) = w(G)$ and $h \in H$ with $w(G \cup \{h\}) > w(G)$, then $w(F \cup \{h\}) > w(F)$.

A constraint $h$ violates $G$ if $w(G \cup \{h\}) > w(G)$. A basis is a set $B$ with $w(B') < w(B)$ for every proper subset $B' \subset B$, and a basis of $G$ is a basis $B \subseteq G$ with $w(B) = w(G)$. The combinatorial dimension $\delta$ is the largest size of a basis. Locality says that an element violates $G$ iff it violates a basis of $G$, so a basis is a certificate for the whole set: $w(G) = w(B)$ and nothing in $G$ violates $B$.

**The two primitives.**

- *Violation test*: given a basis $B$ and $h \in H$, decide whether $h$ violates $B$.
- *Basis computation*: given a basis $B$ and $h$ that violates it, find a basis of $B \cup \{h\}$.

For fixed $\delta$ both act on $O(\delta)$ constraints and cost $O(1)$ time in the real RAM model.

**Extreme elements and the sampling lemma.** An element $h \in G$ is extreme in $G$ if $w(G \setminus \{h\}) < w(G)$. Every extreme element lies in every basis of $G$: if a basis $B$ of $G$ missed $h$, then $B \subseteq G \setminus \{h\}$ and $w(G) = w(B) \le w(G \setminus \{h\}) < w(G)$. So $G$ has at most $\delta$ extreme elements. Now let $R$ be a random subset of $H$ of size $r$, and $V_R$ the set of elements of $H \setminus R$ that violate $R$. An element $h \notin R$ violates $R$ iff $h$ is extreme in $Q = R \cup \{h\}$. Counting pairs $(Q, h)$ with $|Q| = r + 1$ and $h$ extreme in $Q$ gives

$$\mathbb{E}\,|V_R| \le \frac{\delta \binom{n}{r+1}}{\binom{n}{r}} = \frac{\delta (n - r)}{r + 1}.$$

This is the sampling lemma in the form of Gärtner and Welzl; Clarkson (1995, Lemma 3.2) proved the bound $d(n - r + 1)/(r - d)$ for linear programming without degeneracy. It drives every algorithm below. A random sample of size $r$ leaves only about $\delta n / r$ violators, and among the violators of $R$ there is always an element of every basis of $H$, so the algorithm learns something about the answer each time it meets a violator.

**The algorithms.**

| algorithm | expected cost in primitive operations | notes |
|---|---|---|
| Sharir and Welzl (1992), recursive, as in [Seidel's LP algorithm](/seidel-linear-programming/) | $O(2^\delta n)$ | remove a random constraint, solve the rest, repair if it violates |
| Matoušek, Sharir and Welzl (1996) | $\min\{2^{\delta + 2}(n - \delta),\ e^{2\sqrt{\delta \ln((n - \delta)/\sqrt{\delta})} + O(\sqrt{\delta} + \ln n)}\}$ | the subexponential bound; proved for problems in which all bases of large sets have exactly $\delta$ elements, which holds for linear programming |
| [Clarkson's algorithm](/clarksons-algorithm/) (1995) | $O(\delta n)$ violation tests, plus $O(\delta \log n)$ calls of a base solver on $O(\delta^2)$ constraints | random sampling with reweighting |
| Clarkson with the MSW algorithm as base solver | $O(d^2 n + e^{O(\sqrt{d \log d})})$ arithmetic operations for LP in $d$ variables | linear in $n$, subexponential in $d$ |

For a deterministic algorithm, [Megiddo's method](/megiddo-fixed-dimension-lp/) solves LP in $O(2^{2^d} n)$ time by [prune and search](/prune-and-search/), and derandomized versions of the sampling algorithms are known for many LP-type problems.

**Degeneracies.** The axioms need a unique value for each subset, not a unique optimal point. Linear programming becomes LP-type after ties are broken, for example by the lexicographically smallest optimal point, and after unbounded problems are bounded by a large box. If two different circles had the same radius, a radius alone would not be a good value; for the enclosing ball the smallest ball is unique, so the radius is enough.

## Examples

- **Linear programming.** $H$ is a set of halfspaces in $\mathbb{R}^d$, and $w(G)$ is the lexicographically smallest optimal point of $\min c^\top x$ over $\bigcap G$, ordered by the objective and then lexicographically. Monotonicity holds because more constraints give a smaller feasible region. Locality holds because if $F \subseteq G$ have the same optimal point $x$, then $h$ violates $G$ iff $x \notin h$ iff $h$ violates $F$. Here $\delta = d$ (plus one for infeasibility, depending on the convention).
- **Minimum enclosing circle and ball.** $H$ is a set of points, and $w(G)$ is the radius of the smallest ball that contains $G$, with $w(\emptyset) = -\infty$. The ball is unique, so $w(F) = w(G)$ with $F \subseteq G$ means equal balls, and a point violates $G$ iff it lies outside that ball. In $\mathbb{R}^d$, $\delta = d + 1$; in the plane, $\delta = 3$, and [Welzl's algorithm](/welzls-algorithm/) is the LP-type algorithm for it.
- **Minimum volume enclosing ellipsoid.** The smallest-volume ellipsoid that contains $G$ is unique (Löwner-John), so the volume is a value function, with $\delta = d(d + 3)/2$, which is 5 in the plane.
- **Distance between two polytopes.** $H$ is the union of two point sets, and $w(G)$ is the negated distance between the convex hulls of the two parts of $G$. This is LP-type with $\delta = d + 2$.
- **A non-example: the geometric median.** Let $w(G)$ be the smallest sum of distances from one point to the points of $G$. It is monotone, but for points in convex position no point is the median, so removing any one point lowers the value: every such set is its own basis, and there is no bounded $\delta$. The [geometric median](/geometric-median/) is found by iteration instead.

## Where it is used

- **Geometric optimization in fixed dimension.** Smallest enclosing balls, ellipsoids and annuli of minimum area, polytope distance, linear separability, the largest ball inside a polytope, and Chebyshev approximation all get expected linear-time algorithms from one generic code base with two problem-specific primitives.
- **Implicit problems.** When the constraints are too many to list, as in [Chan's randomized optimization technique](/chans-randomized-optimization/) and its LP-type extension by Chan, Har-Peled and Jones, only violation tests on sampled subproblems are needed.
- **Core sets.** A basis is a subset of at most $\delta$ constraints with the same optimum as the whole set, an exact [core set](/coreset/); Clarkson's reweighting finds one by sampling.
- **Helly-type theorems.** A problem of combinatorial dimension $\delta$ has a Helly-type property: if every subset of at most $\delta$ constraints has value at most $t$, then $w(H) \le t$, because $H$ has a basis of at most $\delta$ elements. Amenta (1994) connected LP-type problems with Helly-type theorems in this way.
- **Abstractions.** Violator spaces (Gärtner, Matoušek, Rüst and Škovroň 2008) drop the value function and keep only the violation relation; Clarkson's algorithm still works there.

## References
