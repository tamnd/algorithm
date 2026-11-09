---
tag: 7XAV7R
kind: theorem
slug: closest-pair-lower-bound
name: Closest pair lower bound
aliases:
- Ben-Or lower bound
- algebraic decision tree lower bound for closest pair
- closest pair Omega(n log n)
area: geometry/proximity
level: advanced
summary: Any algebraic decision tree solving closest pair needs Omega(n log n) operations, by reduction from element uniqueness.
prereqs: [closest-pair-of-points, ben-or-theorem, element-distinctness-lower-bound, algebraic-computation-tree]
see_also: [algebraic-decision-tree, element-distinctness, closest-pair-divide-and-conquer, randomized-closest-pair, convex-hull-lower-bound, comparison-sort-lower-bound, proximity-problems]
sources:
  - paper: doi:10.1145/800061.808735
    title: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), 80-86"
    locator: the main theorem bounding the height by the number of connected components, and its application to element distinctness
  - paper: doi:10.1016/0196-6774(82)90002-5
    title: "J. Michael Steele and Andrew C. Yao, Lower bounds for algebraic decision trees, Journal of Algorithms 3(1) (1982), 1-8"
    locator: the main theorem for algebraic decision trees of fixed degree
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 5, Proximity, fundamental algorithms (the lower bounds for closest pair and related problems by reduction from element uniqueness)
  - paper: "Dima Grigoriev, Marek Karpinski, Friedhelm Meyer auf der Heide and Roman Smolensky, A lower bound for randomized algebraic decision trees, Computational Complexity 6(4), 1996/1997, 357-375"
    locator: the Omega(n log n) lower bound for element distinctness on randomized algebraic decision trees of fixed degree
  - paper: "Michiel Smid, Closest-point problems in computational geometry, in J.-R. Sack and J. Urrutia (eds.), Handbook of Computational Geometry, Elsevier, 2000, 877-935"
    locator: the survey section on lower bounds for the closest pair problem and the role of the floor function
---

The closest pair lower bound says that every algorithm in the [algebraic computation tree](/algebraic-computation-tree/) model, and so every [algebraic decision tree](/algebraic-decision-tree/) of fixed degree, needs $\Omega(n \log n)$ operations in the worst case to find the [closest pair](/closest-pair-of-points/) of $n$ points in the plane. The proof reduces [element distinctness](/element-distinctness/) to the closest pair by putting the numbers on a line, and then uses [Ben-Or's theorem](/ben-or-theorem/), which bounds the height of a tree by the number of connected components of the set it decides. The bound is matched by [divide and conquer](/closest-pair-divide-and-conquer/), and it is beaten by the [randomized grid](/randomized-closest-pair/) algorithm, which uses the floor function and hashing and so leaves the model.

## Statement

**Model.** An algebraic computation tree on inputs $z \in \mathbb{R}^N$ performs $+, -, \times, \div, \sqrt{\ }$ on inputs, real constants and earlier values, branches on the sign of an earlier value, and ends in leaves labelled with answers. Its height is the largest number of operations and branches on a root-to-leaf path. Floor, integer division and indirect addressing by real values are not available.

**Theorem.** There is a constant $c > 0$ such that for every $n \ge 2$ the following hold.

1. Every algebraic computation tree that takes $P = (x_1, y_1, \ldots, x_n, y_n) \in \mathbb{R}^{2n}$ and decides whether the $n$ points are pairwise distinct, that is, whether $\delta(P) > 0$, has height at least $c\, n \lg n$ for $n$ large enough.
2. The same holds for deciding whether $\delta(P) \ge 1$. So the bound does not depend on duplicates.
3. Every algebraic computation tree that outputs a closest pair of $P$ (two indices, or the value $\delta^2(P)$) has height $\Omega(n \log n)$.

The same bounds hold for algebraic decision trees of any fixed degree, by the theorem of Steele and Yao, and for points in $\mathbb{R}^d$ for every $d \ge 1$.

## In plain words

To find the closest pair, an algorithm must at least notice when two points are the same. Put all points on one line. Then "are all points different?" is the classic question of whether a list of numbers has repeats.

Now think of every possible input list as one point in a big space. The lists without repeats fall into many separate regions, one for each way of ordering the numbers, and you cannot walk from one region to another without passing through a list with a repeat. Ben-Or's theorem says that a program built from arithmetic and comparisons must run for a long time to tell apart that many regions. The number of orderings is so large that the time must grow like the time for sorting.

## Proof

**Step 1: the one-dimensional set has $n!$ components.** Let

$$W = \{x \in \mathbb{R}^n : x_i \ne x_j \text{ for all } i \ne j\}, \qquad W_1 = \{x \in \mathbb{R}^n : |x_i - x_j| \ge 1 \text{ for all } i \ne j\}.$$

For a permutation $\sigma$ of $\{1, \ldots, n\}$ let $C_\sigma = \{x : x_{\sigma(1)} < x_{\sigma(2)} < \cdots < x_{\sigma(n)}\}$ and $C^1_\sigma = \{x : x_{\sigma(i+1)} - x_{\sigma(i)} \ge 1 \text{ for } 1 \le i < n\}$. Each of these sets is non-empty (take $x_{\sigma(i)} = i$) and convex, as an intersection of half-spaces, so it is connected. $W$ is the disjoint union of the $n!$ sets $C_\sigma$, and $W_1$ is the disjoint union of the $n!$ sets $C^1_\sigma$, because a point of $W$ or $W_1$ has distinct coordinates and hence exactly one sorting permutation. Finally, no connected subset of $W$ meets two of the $C_\sigma$: for each pair $i \ne j$ the function $x_i - x_j$ is continuous and never $0$ on $W$, so its sign is constant on a connected subset, and the signs of all $x_i - x_j$ determine $\sigma$. The same holds in $W_1 \subseteq W$. So $\mathrm{cc}(W) = \mathrm{cc}(W_1) = n!$.

**Step 2: the reduction.** Let $T$ be a valid algebraic computation tree of height $h$ that decides "$\delta(P) > 0$" on $\mathbb{R}^{2n}$. Build $T'$ on inputs $x \in \mathbb{R}^n$ by replacing every use of the input $y_i$ by the constant $0$. Each node of $T'$ computes, on input $x$, exactly the value that the matching node of $T$ computes on the input $P(x) = (x_1, 0, x_2, 0, \ldots, x_n, 0)$. So $T'$ is valid (no division by zero, no root of a negative number), it has height $h$, and it accepts $x$ exactly when the points $(x_i, 0)$ are pairwise distinct, which is when $x \in W$. The same construction turns a tree for "$\delta(P) \ge 1$" into a tree for $W_1$, since $\|(x_i, 0) - (x_j, 0)\| = |x_i - x_j|$.

**Step 3: Ben-Or's theorem.** By [Ben-Or's theorem](/ben-or-theorem/), a valid algebraic computation tree of height $h$ that decides a set with $C$ connected components in $\mathbb{R}^n$ has $h \ge (\lg C - n \lg 3) / \lg 18$. With $C = n!$ and $\lg n! \ge n \lg n - n \lg e$,

$$h \ \ge\ \frac{n \lg n - n \lg e - n \lg 3}{\lg 18} \ =\ \frac{n \lg n}{\lg 18} - O(n),$$

which is at least $c\, n \lg n$ for any $c < 1/\lg 18$ and $n$ large enough. This proves parts 1 and 2.

**Step 4: computing a pair.** Suppose a tree $T$ of height $h$ outputs indices $i \ne j$ of a closest pair. Replace each leaf with output $(i, j)$ by the computation $u = (x_i - x_j)^2 + (y_i - y_j)^2$ (five operations) and a branch on $u > 0$, with leaves accept and reject. The new tree decides "$\delta(P) > 0$" and has height $h + 6$, so $h \ge c\, n \lg n - 6$ by part 1. A tree that outputs $\delta^2(P)$ is handled the same way with one branch at each leaf. This proves part 3.

**Other dimensions.** For $\mathbb{R}^d$, Step 2 sets all coordinates but the first to $0$. For algebraic decision trees of fixed degree, Step 2 keeps the degree of every test, and the theorem of Steele and Yao gives the same $\Omega(\log C) - O(n)$ bound for them. $\blacksquare$

**Why the line is needed.** In the plane, the set of configurations of $n$ pairwise distinct points is connected: two points can move around each other without meeting. So Ben-Or's theorem applied directly to $\{P \in \mathbb{R}^{2n} : \delta(P) > 0\}$ gives nothing. Restricting to the line $y = 0$ is what creates the $n!$ components.

## Consequences

- **Optimal algorithms.** [Divide and conquer](/closest-pair-divide-and-conquer/) and the [sweep line](/closest-pair-sweep-line/) take $O(n \log n)$ time and use only polynomial tests of degree $2$, so they are algebraic decision trees of degree 2. Up to a constant factor they are optimal in the model.
- **Related problems.** Each problem that determines the closest pair in $O(n)$ extra time inherits the bound: [all nearest neighbors](/all-nearest-neighbors/), the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) (its shortest edge), the [Delaunay triangulation](/delaunay-triangulation/) and the [Voronoi diagram](/voronoi-diagram/) (a closest pair is a Delaunay edge), and the [nearest neighbor graph](/nearest-neighbor-graph/).
- **One dimension.** For numbers on a line the closest pair needs $\Omega(n \log n)$ as well, which matches sorting followed by a scan of neighbours.
- **Element distinctness.** The theorem is a geometric form of the [element distinctness lower bound](/element-distinctness-lower-bound/); both rest on the same $n!$ components.

## Tightness

The bound is tight in the model: divide and conquer runs in $O(n \log n)$ time. It is not a bound on all algorithms.

- **Floor and hashing.** With the floor function, a grid of cells of side $\delta$ and a hash table on the cells, the [randomized closest pair](/randomized-closest-pair/) algorithm runs in $O(n)$ expected time (Rabin, 1976). Floor is not an algebraic operation, and a hash table indexes memory by a computed integer, which an algebraic tree cannot do.
- **Floor without randomization.** Fortune and Hopcroft (1979) gave a deterministic $O(n \log \log n)$ algorithm with floor.
- **Randomization alone does not help.** Randomized algebraic decision trees of fixed degree still need $\Omega(n \log n)$ for element distinctness (Grigoriev, Karpinski, Meyer auf der Heide and Smolensky). So Rabin's speedup comes from floor and hashing, not from the coin flips.
- **Integer input.** On the [word RAM](/word-ram/) with integer coordinates, [integer sorting](/integer-sorting/) and hashing give bounds below $n \log n$, and the theorem does not apply.

## History

Ben-Or proved the component bound for algebraic computation trees in 1983 and used it for element distinctness, from which the closest pair bound follows by the reduction above. Earlier, Dobkin and Lipton (1979) had the component argument for linear decision trees and Steele and Yao (1982) for algebraic decision trees of fixed degree. The reduction from element uniqueness to the closest pair and to other proximity problems is presented in Preparata and Shamos's book. Rabin's 1976 linear expected time algorithm, which predates these bounds, was an early example that the choice of model decides the answer.

## References
