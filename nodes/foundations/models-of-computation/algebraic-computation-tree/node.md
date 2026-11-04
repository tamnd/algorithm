---
tag: 7MKZCY
kind: model
slug: algebraic-computation-tree
name: Algebraic computation tree
aliases:
- computation tree model
area: foundations/models-of-computation
level: research
summary: Tree model with arithmetic nodes and branch tests, generalizing algebraic decision trees to include computed values.
prereqs: [algebraic-decision-tree, linear-decision-tree, decision-tree-model]
see_also: [ben-or-theorem, real-ram, element-distinctness, element-distinctness-lower-bound, convex-hull-problem, comparison-model, blum-shub-smale-machine]
sources:
  - paper: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), 80 to 86"
    locator: the definition of the model, the theorem on connected components, and the applications
  - paper: "J. Michael Steele and Andrew C. Yao, Lower bounds for algebraic decision trees, Journal of Algorithms 3 (1982), 1 to 8"
    locator: the earlier bound for algebraic decision trees of fixed degree
  - paper: "John Milnor, On the Betti numbers of real varieties, Proceedings of the American Mathematical Society 15 (1964), 275 to 280"
    locator: the bound on the sum of the Betti numbers of a real algebraic set
  - paper: "Rene Thom, Sur l'homologie des varietes algebriques reelles, in Differential and Combinatorial Topology, Princeton University Press (1965)"
    locator: the same bound, found independently
  - paper: "Franco P. Preparata and Michael Ian Shamos, Computational Geometry: An Introduction, Springer (1985)"
    locator: Section 1.4, Models of computation
  - paper: "Andrew Chi-Chih Yao, Decision tree complexity and Betti numbers, Journal of Computer and System Sciences 55 (1997)"
    locator: abstract (a bound by Betti numbers)
  - paper: "Andrew Chi-Chih Yao, A lower bound to finding convex hulls, Journal of the ACM 28 (1981), 780 to 787"
    locator: the Omega(n log n) bound for convex hulls in the quadratic decision tree model
---

An algebraic computation tree is a rooted tree that computes with real numbers. A computation node applies one of $+$, $-$, $\times$, $\div$ and $\sqrt{\ }$ to earlier values, and a branch node tests the sign of an earlier value. The cost of a run is the number of nodes on its path, so arithmetic is charged and not free. Ben-Or (1983) proved that a tree of height $h$ that decides a set with $C$ connected components has $h = \Omega(\log C - n)$. The bound gives $\Omega(n \log n)$ for [element distinctness](/element-distinctness/) and for several problems of computational geometry.

## The machine

The input is a point $x = (x_1, \ldots, x_n) \in \mathbb{R}^n$. An **algebraic computation tree** is a finite rooted binary tree in which each node is one of these kinds.

- **Computation node.** It has one child. It creates a new value $v = u \circ w$ with $\circ \in \{+, -, \times, \div\}$, or $v = \sqrt{u}$. Each operand is an input coordinate, a real constant, or a value created at an ancestor.
- **Branch node.** It has two children. It tests an earlier value $u$ with one of $u > 0$, $u \ge 0$ or $u = 0$, and goes to the first child when the test is true.
- **Leaf.** It holds an output. For a decision problem it is *accept* or *reject*.

The tree must be **valid**: on every input that reaches a division node, the divisor is not zero, and on every input that reaches a square root node, the operand is not negative. The tree **decides** a set $W \subseteq \mathbb{R}^n$ if it accepts exactly the points of $W$. The values at the nodes are functions of $x$: rational functions, then algebraic functions when roots occur. So the degree of a test is not bounded by a constant: after $k$ multiplications it can be $2^k$, and the fixed-degree bound of Steele and Yao does not apply.

The model needs no bound on the size of the numbers and no rounding. A value is an exact real number, as on the [real RAM](/real-ram/). There is no floor function and no way to turn a real number into an address.

## What it counts

The cost of an input is the number of nodes, of both kinds, on its path. The height $h$ of the tree is the worst-case cost. This differs from the [algebraic decision tree](/algebraic-decision-tree/), where only tests cost and the polynomial of a test is free. In the computation tree, computing a large polynomial costs one node for each arithmetic step.

A tree of height $h$ has at most $2^h$ leaves, since only branch nodes have two children.

## Relation to other models

- **Algebraic decision tree.** A tree of degree $d$ in the [algebraic decision tree](/algebraic-decision-tree/) model with depth $h$ is simulated by a computation tree whose height is $h$ times the number of arithmetic steps to evaluate one polynomial, and this number can be large. So the two models are not equivalent in cost. The computation tree is the more realistic one, and a lower bound for it is a lower bound for a program with the same operations.
- **Linear decision tree.** Computation nodes that only add and scale give the [linear decision tree](/linear-decision-tree/), but with the cost of the additions.
- **Real RAM.** A program for the [real RAM](/real-ram/) that has no floor function, with integer registers that change only by control flow, unrolls for each fixed input size $n$ to a computation tree with height at most the running time. A lower bound on the height is therefore a lower bound on the running time. The unrolling fails when the machine can convert a real value to an address, because the tree would need a node with infinitely many children.
- **Blum-Shub-Smale machine.** The [Blum-Shub-Smale machine](/blum-shub-smale-machine/) is a uniform machine over the reals. For each fixed input size, a run unrolls to a computation tree in the same way, so lower bounds for the tree carry over.
- **Comparison model.** A comparison tree is a computation tree where the only operations are the subtractions $x_i - x_j$ followed by a sign test.

## Known results in the model

**Theorem (Ben-Or, 1983).** Let $T$ be a valid algebraic computation tree of height $h$ that decides $W \subseteq \mathbb{R}^n$, and let $C \ge 1$ be the number of connected components of $W$ or of $\mathbb{R}^n \setminus W$. Then
$$h \ \ge \ \frac{\ln C - \ln 3 - (n-1)\ln 5}{\ln 50}.$$
So $h \ge a \ln C - b n$ for the absolute constants $a = 1/\ln 50$ and $b = \ln 5/\ln 50$, that is, $h = \Omega(\log C - n)$.

*Proof outline.* The steps are those of the proof for the [algebraic decision tree](/algebraic-decision-tree/). Only the first step differs, and it is stated with each case. The constants are those of the Milnor and Thom bound used with degree 3.

1. *The inputs of one leaf form a projection of a real algebraic set with equations of degree at most 3.* Fix a leaf $\lambda$ whose path has $k \le h$ nodes. Give a new variable $v_i$ to each computation node of the path, and write the node as an equation: $v_i - u - w = 0$ for a sum, $v_i - u + w = 0$ for a difference, $v_i - u w = 0$ for a product, $v_i w - u = 0$ for a quotient, and for a root the two equations $v_i^2 - u = 0$ and $v_i - y_i^2 = 0$ with a new variable $y_i$. The second equation says $v_i \ge 0$. For each branch node of the path, with tested value $u$, the answer that the path takes gives these conditions, each with one new variable $z$: $u = 0$ as it is; $u \ge 0$ as $u = z^2$; $u \le 0$ as $u = -z^2$; $u > 0$ as $z^2 u = 1$; $u < 0$ as $z^2 u = -1$; $u \ne 0$ as $z u = 1$. Each equation has degree at most 3, and the system has at most $n + 2k \le n + 2h$ variables.
2. *The projection is the set of the leaf.* Let $R(\lambda)$ be the inputs that reach $\lambda$. If $x \in R(\lambda)$, the actual values of the tree and suitable $y$ and $z$ solve the system. Conversely let $(x, v, y, z)$ solve it. By induction along the path, each $v_i$ is the value that the tree computes on $x$: the earlier branch conditions hold, so $x$ reaches the node; the tree is valid, so a divisor is not zero and a root has a non-negative operand; then $v_i w = u$ gives $v_i = u/w$, and $v_i^2 = u$ with $v_i = y_i^2 \ge 0$ gives the non-negative root. So all branch conditions of the path hold for $x$, and $x \in R(\lambda)$. Hence $R(\lambda)$ is the projection of the solution set onto the first $n$ coordinates.
3. *The components of one leaf.* By Lemma 1 of the page on the [algebraic decision tree](/algebraic-decision-tree/) (Milnor and Thom) with $d = 3$ and $N \le n + 2h$, the solution set has at most $3 \cdot 5^{n+2h-1}$ components. The projection is continuous and onto $R(\lambda)$. The argument in Lemma 2 of that page shows that $\mathrm{cc}(R(\lambda)) \le \mathrm{cc}(\text{solution set})$.
4. *Summing over leaves.* As in the proof for the decision tree, $\mathrm{cc}(W) \le \sum_\lambda \mathrm{cc}(R(\lambda))$ over the accepting leaves, and the same holds for the complement and the rejecting leaves. There are at most $2^h$ leaves. So $C \le 2^h \cdot 3 \cdot 5^{n+2h-1} = 3 \cdot 5^{n-1} \cdot 50^h$.
5. *Solve for $h$.* Take logarithms. For the form $a \ln C - bn$, note that $\ln 3 + (n-1)\ln 5 \le n \ln 5$ for $n \ge 1$. $\square$

**Consequences.** Each item is a lower bound on the height of a computation tree.

- **Element distinctness.** The set $\mathrm{ED}_n$ has $n!$ components (see [linear decision tree](/linear-decision-tree/)), so $h \ge (\ln n! - \ln 3 - (n-1) \ln 5)/\ln 50 = \Omega(n \log n)$. Sorting and checking neighbours gives $O(n \log n)$, so the bound is tight.
- **Sorting.** A tree that outputs the sorted order has at least $n!$ leaves and at most $2^h$ leaves. So $h \ge \lg n!$.
- **Closest pair.** See [closest pair of points](/closest-pair-of-points/). Take points $(x_i, 0)$ on a line. The smallest distance is zero if and only if two $x_i$ are equal. A tree that finds the closest pair, with the pair as output, decides $\mathrm{ED}_n$ after $O(1)$ more nodes (a test that the two points of the pair are equal). So it has height $\Omega(n \log n)$. A similar reduction works for the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/): the shortest edge of any minimum spanning tree of the points has length zero if and only if two points are equal. A tree that outputs the spanning tree decides $\mathrm{ED}_n$ after $O(n)$ more nodes (a zero test on each of the $n-1$ output edges), which does not change the $\Omega(n \log n)$ bound.
- **Convex hull.** Take the points $(x_i, x_i^2)$ for distinct $x_i$. They are in convex position, and the hull listed in counterclockwise order is the cyclic sequence of the points in sorted order of $x_i$. Two sorted orders that differ by a rotation give the same cycle, but a tree may output the cycle starting at any vertex. So take the output convention that the list starts at the leftmost vertex. Then different sorted orders give different outputs, a tree has at least $n!$ leaves, and $h \ge \lg n!$. With any starting vertex allowed, the same count gives $h \ge \lg (n-1)!$, which is also $\Omega(n \log n)$. Yao (1981) proved the $\Omega(n \log n)$ bound for convex hulls in a related model of quadratic tests. See [convex hull problem](/convex-hull-problem/).

**Where the theorem is weak.** The bound is useless for a set with $2^{O(n)}$ components, because the term $bn$ is as large as $a \ln C$. Yao refined the method with Betti numbers of higher order (STOC 1994; journal version JCSS 55, 1997).

**Floor function.** The bound holds only for the model without a floor function. With a floor function, the maximum gap problem takes $O(n)$ time by bucketing (see [real RAM](/real-ram/)), while it needs $\Omega(n \log n)$ in this model. So the model matters.

## References
