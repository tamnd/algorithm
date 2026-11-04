---
tag: 6Z71CZ
kind: theorem
slug: element-distinctness-lower-bound
name: Element distinctness lower bound
aliases:
- element uniqueness lower bound
- Omega(n log n) distinctness
area: foundations/lower-bounds
level: advanced
summary: Every algebraic computation tree that decides whether n real numbers are pairwise distinct has height Omega(n log n), because the set of yes-inputs has n! connected components.
prereqs: [ben-or-theorem, element-distinctness, algebraic-computation-tree]
see_also: [linear-decision-tree, algebraic-decision-tree, comparison-model, closest-pair-of-points, reduction-lower-bound, hash-table, comparison-sort-lower-bound]
sources:
  - paper: doi:10.1145/800061.808735
    title: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), 80-86"
    locator: the main theorem and its application to element distinctness
  - paper: doi:10.1016/0022-0000(79)90054-0
    title: "David P. Dobkin and Richard J. Lipton, On the complexity of computations under varying sets of primitives, Journal of Computer and System Sciences 18(1) (1979), 86-91"
    locator: the Omega(n log n) bound for element uniqueness in linear decision trees
  - paper: doi:10.1016/0196-6774(82)90002-5
    title: "J. Michael Steele and Andrew C. Yao, Lower bounds for algebraic decision trees, Journal of Algorithms 3(1) (1982), 1-8"
    locator: the main theorem (algebraic decision trees of fixed degree)
  - paper: doi:10.1016/0890-5401(91)90034-Y
    title: "Anna Lubiw and Andras Racz, A lower bound for the integer element distinctness problem, Information and Computation 94(1) (1991), 83-92"
    locator: the main theorem (integer inputs, algebraic decision trees of bounded degree)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 5, Proximity, fundamental algorithms (element uniqueness as the prototype lower bound)
---

The element distinctness lower bound says that every [algebraic computation tree](/algebraic-computation-tree/) that decides whether $n$ real numbers are pairwise distinct has height $\Omega(n \log n)$. The proof counts the connected components of the set of yes-inputs, which is exactly $n!$, and applies [Ben-Or's theorem](/ben-or-theorem/). The bound matches the $O(n \log n)$ algorithm "sort, then compare neighbours", so this algorithm is optimal in the model. It is the base of many $\Omega(n \log n)$ bounds in computational geometry, which follow by [reduction](/reduction-lower-bound/).

## Statement

The problem is [element distinctness](/element-distinctness/) on real inputs. For $n \ge 1$ let

$$\mathrm{ED}_n = \{x \in \mathbb{R}^n : x_i \ne x_j \text{ for all } 1 \le i < j \le n\}.$$

For a permutation $\sigma$ of $\{1, \ldots, n\}$ let $K_\sigma = \{x \in \mathbb{R}^n : x_{\sigma(1)} < x_{\sigma(2)} < \cdots < x_{\sigma(n)}\}$, an open cone.

**Theorem.** Let $n \ge 1$.

1. The connected components of $\mathrm{ED}_n$ are exactly the $n!$ cones $K_\sigma$. So $\mathrm{cc}(\mathrm{ED}_n) = n!$.
2. Every valid algebraic computation tree (operations $+, -, \times, \div, \sqrt{\ }$, sign tests, unit cost per node) that decides $\mathrm{ED}_n$ has height
$$h \ \ge\ \frac{\lg n! - n \lg 3}{\lg 18} = \Omega(n \log n).$$

The bound is on the worst case: some input in $\mathbb{R}^n$ follows a path with at least $h$ nodes. The inputs are exact real numbers, and the tree has no floor function and no hashing.

## In plain words

Write down a list of numbers that are all different. Now move the numbers around slowly, one small step at a time, and never let two of them become equal. Two numbers can never pass each other, because to pass they must meet. So the order of the numbers never changes.

This means that the yes-inputs fall into separate pieces, one for each possible order, and there are a huge number of orders. Ben-Or's theorem says that a program built from arithmetic and sign tests needs a long run to tell apart so many pieces. The result is the bound "the input size times the logarithm of the input size", which sorting already achieves.

## Proof

**Part 1: the components.** The cones are disjoint, each lies in $\mathrm{ED}_n$, and each point of $\mathrm{ED}_n$ has pairwise different coordinates, so it lies in the cone of the permutation that sorts them. So $\mathrm{ED}_n$ is the disjoint union of the $n!$ cones.

*Each cone is connected.* $K_\sigma$ is defined by strict linear inequalities, so it is convex: if $x, y \in K_\sigma$ and $0 \le t \le 1$, each inequality $x_{\sigma(k)} < x_{\sigma(k+1)}$ holds for $(1-t)x + ty$ because it holds for $x$ and for $y$. A convex set is connected. Each cone is not empty: it holds the point with $x_{\sigma(k)} = k$.

*Two cones are in different components.* Let $\sigma \ne \tau$. Then some pair $i \ne j$ is in one order under $\sigma$ and in the other under $\tau$: say $x_i < x_j$ on $K_\sigma$ and $x_i > x_j$ on $K_\tau$. The function $g(x) = x_j - x_i$ is continuous and is never zero on $\mathrm{ED}_n$. Suppose a connected set $D \subseteq \mathrm{ED}_n$ meets both cones. Then $g(D)$ is a connected subset of $\mathbb{R}$, so an interval, and it holds a positive and a negative value. So it holds $0$, which is false on $\mathrm{ED}_n$. Hence no connected subset of $\mathrm{ED}_n$ meets two cones.

So each cone is a connected subset of $\mathrm{ED}_n$, and the component that contains it meets no other cone. Since the cones cover $\mathrm{ED}_n$, that component is the cone. This proves $\mathrm{cc}(\mathrm{ED}_n) = n!$.

**Part 2: the height.** [Ben-Or's theorem](/ben-or-theorem/) says that a valid tree of height $h$ that decides $W \subseteq \mathbb{R}^n$ satisfies $h \ge (\lg C - n \lg 3)/\lg 18$ with $C = \mathrm{cc}(W)$. With $W = \mathrm{ED}_n$ and $C = n!$ this is the bound. For the order of growth, $\lg n! \ge \lg\bigl((n/2)^{n/2}\bigr) = \tfrac{n}{2}\lg\tfrac{n}{2}$, since at least $n/2$ factors of $n!$ are at least $n/2$. So $h \ge \bigl(\tfrac{n}{2}\lg\tfrac{n}{2} - n\lg 3\bigr)/\lg 18$, which is $\Omega(n \log n)$. $\square$

### Example

For $n = 3$ the six cones are $x_1 < x_2 < x_3$, $x_1 < x_3 < x_2$, $x_2 < x_1 < x_3$, $x_2 < x_3 < x_1$, $x_3 < x_1 < x_2$ and $x_3 < x_2 < x_1$. The points $(1, 2, 3)$ and $(3, 2, 1)$ are in $\mathrm{ED}_3$, but the segment between them passes through $(2, 2, 2)$, which is not. Any path between them must make $x_1 = x_3$ at some point, by the argument of Part 1.

The table gives the values of the bound. The column $\lceil \lg n! \rceil$ is the bound in the [comparison model](/comparison-model/) (see Tightness).

| $n$ | $\lg n!$ | $\lceil \lg n! \rceil$ | bound of the theorem, rounded up |
|---|---|---|---|
| 10 | 21.79 | 22 | 2 |
| 100 | 524.76 | 525 | 88 |
| 1000 | 8529.40 | 8530 | 1666 |
| 1000000 | 18488884.82 | 18488885 | 4053772 |

The algebraic bound is between a fifth and a quarter of the comparison bound for large $n$. It is weaker in its constant because each node of an algebraic tree can do much more than a comparison.

## Consequences

Each item is a lower bound on the height of a valid algebraic computation tree.

- **Element uniqueness.** This is another name for the same problem.
- **Closest pair.** Given $n$ points, a tree that outputs a closest pair $(i, j)$ decides $\mathrm{ED}_n$ on the points $(x_1, 0), \ldots, (x_n, 0)$ with two more nodes: compute $x_i - x_j$ and test it for zero. Two points are equal if and only if the closest pair is at distance zero. So the [closest pair of points](/closest-pair-of-points/) needs height at least $(\lg n! - n \lg 3)/\lg 18 - 2$. The reduction uses only operations of the model, which is the condition of a [reduction lower bound](/reduction-lower-bound/).
- **Minimum gap.** A tree that outputs $\min_{i<j} |x_i - x_j|$ decides $\mathrm{ED}_n$ with one more test, so it has the same bound up to one node.
- **Set disjointness.** Given $a, b \in \mathbb{R}^n$, decide whether $a_i \ne b_j$ for all $i, j$. Let $D = \{(a, b) \in \mathbb{R}^{2n} : a_i \ne b_j \text{ for all } i, j\}$. For permutations $\sigma, \tau$, the points with $a_{\sigma(1)} < b_{\tau(1)} < a_{\sigma(2)} < b_{\tau(2)} < \cdots < a_{\sigma(n)} < b_{\tau(n)}$ lie in $D$. On such a point, $a_i < b_j$ holds exactly when the rank of $a_i$ among the $a$'s is at most the rank of $b_j$ among the $b$'s. So the signs of all $a_i - b_j$ give back $\sigma$ and $\tau$, and the $(n!)^2$ pairs give $(n!)^2$ different sign patterns. Each function $a_i - b_j$ is continuous and never zero on $D$, so it has one sign on each component, and points with different patterns are in different components. Hence $\mathrm{cc}(D) \ge (n!)^2$, and Ben-Or's theorem in dimension $2n$ gives $h \ge (2\lg n! - 2n\lg 3)/\lg 18 = \Omega(n \log n)$.
- **Weaker models.** The same bound, with other constants, holds for [linear decision trees](/linear-decision-tree/) (Dobkin and Lipton) and for [algebraic decision trees](/algebraic-decision-tree/) of fixed degree (Steele and Yao). These models charge a whole linear or polynomial test as one step, so they are not special cases of the computation tree, and each needs its own counting argument.

### Pitfalls

- **Hashing.** On a [word RAM](/word-ram/) with integer keys, insert the keys into a [hash table](/hash-table/) and report a collision of equal keys. This takes $O(n)$ expected time. Hashing maps a key to an address, which an algebraic tree cannot do, so the theorem does not apply.
- **Small integers.** If the keys are integers in $\{0, \ldots, U - 1\}$, an array of $U$ flags decides distinctness in $O(n + U)$ time on a RAM. The theorem is about real inputs and a model without indirect addressing.
- **Integer inputs in the tree model.** If the inputs are integers but the machine is still an algebraic tree, with no hashing and no indirect addressing, the proof above does not apply, because it counts the components of a set of real points. Lubiw and Racz (1991) proved $\Omega(n \log n)$ for this case in algebraic decision trees of bounded degree.
- **The floor function.** A model with floor is stronger. The maximum gap of $n$ reals, for example, is found in $O(n)$ time by a bucket method that uses floor. Do not move a bound proved in a tree model to a machine with floor, or the reverse.
- **Deciding, not finding.** The theorem is about the decision problem in the worst case. Finding a duplicate when one is promised, or the time on a random input, are other questions.
- **Randomized trees.** This page covers deterministic trees only.

## Tightness

- **Upper bound.** Sort the $n$ numbers with [merge sort](/merge-sort/), which uses at most $n \lceil \lg n \rceil$ comparisons, and then compare the $n - 1$ neighbours for equality. This decides $\mathrm{ED}_n$ in $O(n \log n)$ comparisons, which are nodes of an algebraic computation tree. So the bound is tight up to a constant factor.
- **Comparison model.** In a tree whose tests are comparisons $x_i \le x_j$ or $x_i < x_j$, the set of inputs that reach a leaf is an intersection of half-spaces, so it is convex and connected. An accepting leaf therefore lies inside one cone $K_\sigma$, and each of the $n!$ cones needs its own accepting leaf. A binary tree with $n!$ leaves has height at least $\lceil \lg n! \rceil$. The same count in a three-way test model gives $\lceil \log_3 n! \rceil$, and this is the argument of the [linear decision tree](/linear-decision-tree/) page.
- **Constants.** The constant of the algebraic bound is about $1/\lg 18$, far from the constant 1 of the comparison bound. The order of growth is the content of the theorem.

## History

Dobkin and Lipton (1979) proved the $\Omega(n \log n)$ bound for element uniqueness in linear decision trees by counting the $n!$ regions of the yes-set. Steele and Yao (1982) extended it to algebraic decision trees of fixed degree, using the Milnor bound on real algebraic sets. Ben-Or (1983) proved it for algebraic computation trees, where the degree of a test may grow with the height. Preparata and Shamos (1985) use element uniqueness as the basic problem from which they derive the lower bounds for closest-point problems. Lubiw and Racz (1991) showed that the bound survives when the inputs are integers, for algebraic decision trees of bounded degree.

## References
