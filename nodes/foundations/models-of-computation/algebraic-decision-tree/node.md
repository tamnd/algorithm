---
tag: V0R16J
kind: model
slug: algebraic-decision-tree
name: Algebraic decision tree
aliases:
- algebraic computation tree
- algebraic decision tree model
- algebraic tree model
area: foundations/models-of-computation
level: advanced
summary: Decision tree whose tests are signs of polynomials, giving lower bounds via algebraic degree.
prereqs: [decision-tree-model, linear-decision-tree, asymptotic-notation]
see_also: [algebraic-computation-tree, ben-or-theorem, element-distinctness, element-distinctness-lower-bound, real-ram, comparison-model]
sources:
  - paper: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), 80 to 86"
    locator: the lower bound in terms of the number of connected components, and the application to element distinctness
  - paper: "J. Michael Steele and Andrew C. Yao, Lower bounds for algebraic decision trees, Journal of Algorithms 3 (1982), 1 to 8"
    locator: the bound for algebraic decision trees of fixed degree
  - paper: "John Milnor, On the Betti numbers of real varieties, Proceedings of the American Mathematical Society 15 (1964), 275 to 280"
    locator: the bound on the sum of the Betti numbers of a real algebraic set
  - paper: "Andrew Chi-Chih Yao, Decision tree complexity and Betti numbers, Journal of Computer and System Sciences 55 (1997)"
    locator: abstract (a bound by Betti numbers)
  - paper: "Rene Thom, Sur l'homologie des varietes algebriques reelles, in Differential and Combinatorial Topology, Princeton University Press (1965)"
    locator: the same bound, found independently
  - paper: "Franco P. Preparata and Michael Ian Shamos, Computational Geometry: An Introduction, Springer (1985)"
    locator: Chapter 1, the section on lower bounds in the algebraic decision tree model
---

An algebraic decision tree of degree $d$ is a [decision tree](/decision-tree-model/) for a function on $\mathbb{R}^n$ in which each inner node tests the sign of a polynomial of degree at most $d$ in the input. The cost is the depth of the tree. A lower bound of Steele and Yao (1982), extended by Ben-Or (1983), says that a tree for a set $W \subseteq \mathbb{R}^n$ has depth $\Omega(\log C - n)$ when $d$ is fixed, where $C$ is the number of connected components of $W$ or of its complement. With this bound, [element distinctness](/element-distinctness/) needs $\Omega(n \log n)$ tests, even though each test may use all inputs and a polynomial of any fixed degree.

## The machine

The input is a point $x \in \mathbb{R}^n$. An **algebraic decision tree of degree $d$** (with $d \ge 1$ an integer) is a finite rooted tree with these parts.

- Each inner node $v$ holds a polynomial $p_v \in \mathbb{R}[x_1, \ldots, x_n]$ of total degree at most $d$. It has three children, for the answers $p_v(x) < 0$, $p_v(x) = 0$ and $p_v(x) > 0$.
- Each leaf is labelled *accept* or *reject*, or holds another output.

On input $x$ the machine follows the path that the signs select and gives the label of the leaf. The tree **decides** a set $W \subseteq \mathbb{R}^n$ if it accepts exactly the points of $W$. The case $d = 1$ is the [linear decision tree](/linear-decision-tree/). A test with two answers is a three-way test with two children joined, so it needs no separate definition.

For a leaf $\lambda$ let $R(\lambda)$ be the set of inputs that reach $\lambda$. It is the set of $x$ for which, at each node $v$ on the path, $p_v(x)$ has the sign that the path takes. The sets $R(\lambda)$ partition $\mathbb{R}^n$. Unlike the linear case, $R(\lambda)$ is in general not convex and not connected, and this is why a different argument is needed.

## What it counts

The cost is the depth $h$, the number of tests on the longest path. Only tests cost. The tree has at most $3^h$ leaves. The coefficients of the polynomials are arbitrary real numbers and cost nothing. The degree $d$ is part of the model, and the bounds below depend on it.

The degree must be bounded. Without a bound, one test can decide a hard set: for $n \ge 2$ the polynomial $P(x) = \prod_{i<j} (x_i - x_j)^2$ has degree $n(n-1)$ and $P(x) > 0$ exactly when the coordinates of $x$ are distinct. So one test of degree $n(n-1)$ decides element distinctness. For $n = 3$ the degree is 6. For element distinctness the bound below allows a degree that grows with $n$, but it is positive only when $2d+3$ is smaller than about $n/e$, since $\ln n! \approx n \ln(n/e)$.

## Relation to other models

- **Linear decision tree.** Degree $d = 1$ gives the [linear decision tree](/linear-decision-tree/). There the regions are convex, and counting the leaves is enough. For $d \ge 2$ the regions can have several components, and the bound must count them.
- **Algebraic computation tree.** The [algebraic computation tree](/algebraic-computation-tree/) has arithmetic nodes, so a test can have degree $2^k$ after $k$ products. A tree of depth $h$ of that kind is not an algebraic decision tree of bounded degree, and Ben-Or handled this case with the same method.
- **Comparison model.** A comparison tree is an algebraic decision tree of degree 1 with tests $x_i - x_j$. The [comparison model](/comparison-model/) is the weakest case.
- **Real RAM.** An algorithm on the [real RAM](/real-ram/) without a floor function and with a bounded number of steps unrolls to an algebraic computation tree, not always to a decision tree of bounded degree. The tree bounds are the main way to show a lower bound on the real RAM.

## Known results in the model

The lower bound uses the number of connected components of a set. The number of components of a set $S \subseteq \mathbb{R}^N$ is written $\mathrm{cc}(S)$. It is the number of classes of the relation "a connected subset of $S$ holds both points". It can be $0$ for the empty set.

**Lemma 1 (Milnor and Thom).** Let $N \ge 1$ and $d \ge 1$. Let $f_1, \ldots, f_s \in \mathbb{R}[y_1, \ldots, y_N]$ have degree at most $d$, and let $Z = \{y \in \mathbb{R}^N : f_1(y) = \cdots = f_s(y) = 0\}$. Then
$$\mathrm{cc}(Z) \le d(2d-1)^{N-1}.$$

This is the bound of Milnor (1964) and Thom (1965) on the sum of the Betti numbers of a real algebraic set. The number of components is the zeroth Betti number, so it is at most that sum. The page uses this lemma without proof. Only its form matters: for a fixed degree it is $c^N$ for a constant $c$.

**Lemma 2 (equations and strict inequalities).** Let $n \ge 1$, $d \ge 1$ and $m \ge 0$. Let $p_1, \ldots, p_s, q_1, \ldots, q_m \in \mathbb{R}[x_1, \ldots, x_n]$ have degree at most $d$, and let
$$S = \{x \in \mathbb{R}^n : p_i(x) = 0 \text{ for all } i, \ q_j(x) > 0 \text{ for all } j\}.$$
Then $\mathrm{cc}(S) \le (d+2)(2d+3)^{n+m-1}$.

*Proof.* Let $V \subseteq \mathbb{R}^{n+m}$ be the set of $(x, w)$ with $p_i(x) = 0$ for all $i$ and $w_j^2 \, q_j(x) - 1 = 0$ for all $j$. These are polynomial equations of degree at most $d + 2$ in $n + m$ variables. By Lemma 1, $\mathrm{cc}(V) \le (d+2)(2d+3)^{n+m-1}$.

Let $\pi : V \to \mathbb{R}^n$ be the projection $(x, w) \mapsto x$. It is continuous. Its image is $S$:

- If $(x, w) \in V$ then $w_j^2 q_j(x) = 1$, so $q_j(x) = 1/w_j^2 > 0$. Hence $x \in S$.
- If $x \in S$ then $q_j(x) > 0$, and $w_j = 1/\sqrt{q_j(x)}$ gives a point $(x, w) \in V$.

Now bound $\mathrm{cc}(S)$ by $\mathrm{cc}(V)$. Let $C$ be a component of $S$. Pick $x \in C$ and $v \in V$ with $\pi(v) = x$, and let $K$ be the component of $V$ that contains $v$. The set $\pi(K)$ is connected, it lies in $S$, and it contains $x$. So $\pi(K) \subseteq C$. Two different components $C$ and $C'$ give two different sets $K$ and $K'$, because $\pi(K)$ and $\pi(K')$ are not empty and lie in the disjoint sets $C$ and $C'$. So $\mathrm{cc}(S) \le \mathrm{cc}(V)$. $\square$

**Theorem (Steele and Yao 1982, Ben-Or 1983).** Let $T$ be an algebraic decision tree of degree $d$ and depth $h$ that decides $W \subseteq \mathbb{R}^n$. Let $C$ be the number of connected components of $W$, or of $\mathbb{R}^n \setminus W$. Then
$$C \le (d+2)(2d+3)^{n-1} \bigl(3(2d+3)\bigr)^h,$$
and so
$$h \ \ge \ \frac{\ln C - \ln(d+2) - (n-1)\ln(2d+3)}{\ln\bigl(3(2d+3)\bigr)}.$$

*Proof.* The set $W$ is the disjoint union of the sets $R(\lambda)$ over the accepting leaves $\lambda$, and $\mathbb{R}^n \setminus W$ is the same for the rejecting leaves. Take the accepting leaves; the other case is the same. There are at most $3^h$ of them.

1. *Each $R(\lambda)$.* The path to $\lambda$ has at most $h$ nodes. At a node with polynomial $p$, the path takes the answer $p = 0$, or $p > 0$, or $p < 0$, and $p < 0$ means $q = -p > 0$ with $\deg q = \deg p \le d$. So $R(\lambda)$ has the form of $S$ in Lemma 2 with $s + m \le h$, hence $m \le h$. By Lemma 2, $\mathrm{cc}(R(\lambda)) \le (d+2)(2d+3)^{n+h-1}$, since $(2d+3) \ge 1$.
2. *From leaves to $W$.* Each connected component of some $R(\lambda)$ is a connected subset of $W$, so it lies in one component of $W$. Each point of $W$ lies in some $R(\lambda)$. So each component of $W$ is a union of components of the sets $R(\lambda)$, and $\mathrm{cc}(W) \le \sum_\lambda \mathrm{cc}(R(\lambda))$.
3. *Sum.* With at most $3^h$ leaves, $\mathrm{cc}(W) \le 3^h (d+2)(2d+3)^{n+h-1} = (d+2)(2d+3)^{n-1} (3(2d+3))^h$. This is the first inequality; the second follows by taking logarithms. $\square$

For fixed $d$ the bound reads $h \ge \log(C)/O(1) - O(n)$. This is the form $\Omega(\log C - n)$.

**Corollary (element distinctness).** For fixed $d$, every algebraic decision tree of degree $d$ that decides $\mathrm{ED}_n = \{x \in \mathbb{R}^n : x_i \ne x_j \text{ for all } i < j\}$ has depth $\Omega(n \log n)$.

*Proof.* The set $\mathrm{ED}_n$ has exactly $n!$ connected components, the open cones $\{x : x_{\sigma(1)} < \cdots < x_{\sigma(n)}\}$ (see the proof for the [linear decision tree](/linear-decision-tree/)). So $C = n!$ and $\ln n! = n \ln n - O(n)$. The bound of the theorem gives
$$h \ge \frac{n \ln n - O(n)}{\ln(3(2d+3))} = \Omega(n \log n),$$
since the denominator is a constant. $\square$

The bound is tight for every fixed $d \ge 1$: sort with comparisons, then test the neighbouring pairs, in $O(n \log n)$ tests of degree 1.

The theorem gives the following lower bounds on $h$, computed with $d = 2$ for $\mathrm{ED}_n$. The values are the right side of the second inequality of the theorem, rounded down.

| $n$ | lower bound on $h$ for $d = 2$ |
|---|---|
| 100 | 55 |
| 1000 | 1302 |
| 1000000 | 3570217 |

The constants are poor, and for $n = 10$ the bound is negative. The shape $\Omega(n \log n)$ is the result.

**Other consequences.** The same method gives $\Omega(n \log n)$ for the closest pair problem and for the convex hull listed in order, by reductions that the page on the [algebraic computation tree](/algebraic-computation-tree/) gives. Yao (STOC 1994; journal version 1997) refined the method with Betti numbers of higher order.

**Where the method stops.** A set with at most about $(2d+3)^n$ components gets a bound of $O(1)$ or less, because of the term $(n-1)\ln(2d+3)$. A set with $2^{O(n)}$ components gets at most $O(n)$, which is no better than reading the input. Other methods are needed for such sets. The bound also needs a fixed degree, as the one-test example above shows.

**Floor function.** The model has no floor function. With a floor function, the maximum gap problem takes $O(n)$ time by bucketing (see [real RAM](/real-ram/)), while its bound in the tree models is $\Omega(n \log n)$. So the model must exclude floor for the lower bounds to hold.

## References
