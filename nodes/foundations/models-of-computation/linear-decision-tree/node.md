---
tag: V8TEGQ
kind: model
slug: linear-decision-tree
name: Linear decision tree
aliases:
- linear decision tree model
area: foundations/models-of-computation
level: advanced
summary: Decision tree whose tests are linear functions of the input, used for element distinctness lower bounds.
prereqs: [decision-tree-model, comparison-model, asymptotic-notation]
see_also: [algebraic-decision-tree, algebraic-computation-tree, ben-or-theorem, element-distinctness, 3sum, real-ram]
sources:
  - paper: "David P. Dobkin and Richard J. Lipton, On the complexity of computations under varying sets of primitives, Journal of Computer and System Sciences 18 (1979), 86 to 91"
    locator: the Omega(n log n) bound for element distinctness on linear search trees
  - paper: "Jeff Erickson, Lower bounds for linear satisfiability problems, Chicago Journal of Theoretical Computer Science (1999); conference version SODA 1995"
    locator: the Omega(n^ceil(k/2)) bound for k-SUM in k-linear decision trees
  - paper: "Allan Grønlund and Seth Pettie, Threesomes, degenerates, and love triangles, FOCS 2014"
    locator: abstract (the subquadratic linear decision tree for 3SUM)
  - paper: "Anna Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry 5 (1995), 165 to 185"
    locator: the definition of 3SUM-hard problems
  - paper: "Daniel M. Kane, Shachar Lovett and Shay Moran, Near-optimal linear decision trees for k-SUM and related problems, STOC 2018"
    locator: abstract (linear decision trees of depth O(n log^2 n) for 3SUM)
  - paper: "Friedhelm Meyer auf der Heide, A polynomial linear search algorithm for the n-dimensional knapsack problem, Journal of the ACM 31 (1984)"
    locator: abstract (a linear decision tree of polynomial depth for knapsack)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.1 (decision trees and the bound lg n! for sorting)
---

A linear decision tree is a [decision tree](/decision-tree-model/) for a function on $\mathbb{R}^n$ in which each inner node tests the sign of a linear function of the input. The cost of an algorithm is the depth of its tree, and all other work is free. It extends the [comparison model](/comparison-model/), where each test compares two inputs, and it gives the classic $\Omega(n \log n)$ bound for [element distinctness](/element-distinctness/) of Dobkin and Lipton. It is the weakest of the real-number tree models of this area: the [algebraic decision tree](/algebraic-decision-tree/) allows polynomial tests.

## The machine

The input is a point $x = (x_1, \ldots, x_n) \in \mathbb{R}^n$. A **linear decision tree** is a finite rooted tree with these parts.

- Each inner node $v$ holds a linear function $\ell_v(x) = a_1 x_1 + \cdots + a_n x_n + b$ with real coefficients $a_i$ and $b$. It has three children, for the three answers $\ell_v(x) < 0$, $\ell_v(x) = 0$ and $\ell_v(x) > 0$.
- Each leaf holds an output. For a decision problem the output is *accept* or *reject*. For a problem such as sorting the output is a value from a finite set, for example a permutation.

On input $x$ the machine starts at the root and follows the child that matches the sign of $\ell_v(x)$ at each node. It stops at a leaf and gives the output of that leaf. The tree **computes** a function $f$ if the output equals $f(x)$ for every $x \in \mathbb{R}^n$. A test with two answers (for example $\ell(x) \ge 0$ against $\ell(x) < 0$) is a three-way test with two children joined, so it needs no new definition.

The tree **computes** $f$ on a domain $D \subseteq \mathbb{R}^n$ if the output equals $f(x)$ for every $x \in D$. Sorting is defined only on inputs with distinct coordinates, so $D$ is that set for sorting.

A **$k$-linear** tree is a linear decision tree in which each $\ell_v$ depends on at most $k$ of the input variables. A comparison tree is a 2-linear tree whose tests are $x_i - x_j$.

For a leaf $\lambda$ let $R(\lambda)$ be the set of inputs that reach $\lambda$. It is the set of $x$ that meet, for each node $v$ on the path to $\lambda$, one condition of the form $\ell_v(x) < 0$, $\ell_v(x) = 0$ or $\ell_v(x) > 0$. Each such condition defines a [convex set](/convex-set/) (an open half-space or a hyperplane), so $R(\lambda)$ is convex. The sets $R(\lambda)$ over all leaves $\lambda$ partition $\mathbb{R}^n$. The sorting and element distinctness bounds on this page come from two facts: the regions are convex, and a tree of depth $h$ has at most $3^h$ leaves. The bounds for 3SUM and $k$-SUM need another argument (Erickson 1999).

## What it counts

The cost is the number of tests on the path that the input follows. The depth $h$ of the tree is the worst-case cost. Arithmetic to build the coefficients, memory access and all control are free, and the coefficients of one node may depend on the input size in any way. So a lower bound in this model holds for every algorithm that learns about the input only through signs of linear functions, whatever its other cost. An upper bound in this model need not give a fast algorithm. The tree is non-uniform (one tree for each $n$), and building it or choosing the next test may cost much more than its depth. The 3SUM trees of Grønlund and Pettie are an example.

Only worst-case depth is used here. Average-case and randomized versions exist, but they are not covered.

## Relation to other models

- **Comparison model.** Every comparison tree is a linear decision tree, so each upper bound in the [comparison model](/comparison-model/) carries over. A lower bound proved for linear trees is stronger, because the tests may have any number of variables. The sorting bound $\lceil \log_3 n! \rceil$ below is a bound for linear trees.
- **Algebraic decision tree.** The [algebraic decision tree](/algebraic-decision-tree/) allows polynomial tests of degree at most $d$, and a linear tree is the case $d = 1$. The convexity argument below does not work for $d \ge 2$, because the regions are not convex. The [theorem of Ben-Or](/ben-or-theorem/) replaces convexity by a bound on the number of connected components of a region (a connected component of a set is a largest connected subset of it).
- **Algebraic computation tree.** The [algebraic computation tree](/algebraic-computation-tree/) also has arithmetic nodes, so it can compute products of inputs. A linear tree cannot, so it is a restricted model and not a model of a real program.
- **Real RAM.** A program on the [real RAM](/real-ram/) that uses only addition, subtraction, multiplication by constants and comparisons unrolls, for each fixed $n$, to a linear decision tree whose depth is at most the running time. With general multiplication it unrolls to an algebraic computation tree.

## Known results in the model

**Sorting.** Let $n \ge 1$. A tree that sorts outputs the permutation that sorts the input, and it needs to be correct only on inputs with distinct coordinates. For each permutation $\sigma$ the open set $U_\sigma$ of inputs sorted by $\sigma$ is not empty, and a point of it must reach a leaf that outputs $\sigma$. So the tree has at least $n!$ leaves. A tree of depth $h$ has at most $3^h$ leaves, so $h \ge \log_3 n!$. For $n = 10$ this gives $h \ge 14$ because $\log_3 10! \approx 13.75$. Also $\log_3 n! = \Theta(n \log n)$, since $\ln n! = n \ln n - n + O(\log n)$ (see [Stirling approximation](/stirling-approximation/)). [Merge sort](/merge-sort/) uses comparisons only, so the bound $\Theta(n \log n)$ is tight.

**Element distinctness.** The problem [element distinctness](/element-distinctness/) asks whether $x_i \ne x_j$ for all $i < j$. Let $\mathrm{ED}_n = \{x \in \mathbb{R}^n : x_i \ne x_j \text{ for all } i < j\}$.

> [!note]
> **Theorem (Dobkin and Lipton, 1979).** Every linear decision tree that decides $\mathrm{ED}_n$ has depth at least $\log_3 n!$, which is $\Omega(n \log n)$.

*Proof.* The proof has three steps.

1. *The components of $\mathrm{ED}_n$.* For a permutation $\sigma$ of $\{1, \ldots, n\}$ let $U_\sigma = \{x : x_{\sigma(1)} < x_{\sigma(2)} < \cdots < x_{\sigma(n)}\}$. Each $U_\sigma$ is an intersection of open half-spaces, so it is open and convex, hence connected. The sets $U_\sigma$ are pairwise disjoint, because two different permutations order some pair $i, j$ in opposite ways. Their union is $\mathrm{ED}_n$, because a point with distinct coordinates has exactly one sorted order. A set that is a disjoint union of open connected sets has these sets as its connected components. So $\mathrm{ED}_n$ has exactly $n!$ connected components.
2. *A leaf covers one component.* Let $\lambda$ be an accepting leaf. Then $R(\lambda) \subseteq \mathrm{ED}_n$, because the tree is correct. The set $R(\lambda)$ is convex, hence connected, so it lies inside one component $U_\sigma$.
3. *Counting.* Each $U_\sigma$ is not empty, and every point of it reaches an accepting leaf. So each $U_\sigma$ contains $R(\lambda)$ for some accepting leaf $\lambda$ (take the leaf of any point of $U_\sigma$). By step 2 a leaf serves only one component. So the tree has at least $n!$ accepting leaves, and at most $3^h$ leaves in total. Hence $3^h \ge n!$ and $h \ge \log_3 n!$. $\square$

The upper bound matches: sort the input with a comparison sort, then test the $n - 1$ neighbouring pairs for equality. This uses $O(n \log n)$ tests with two variables each.

The argument does not use the number of variables in a test. So the bound holds even if each test may use all $n$ variables. The same argument gives depth at least $\log_3 C$ for any decision problem whose accepting set has $C$ connected components, and also when the rejecting set has $C$ (swap the answers).

**3SUM.** In the real-number form of [3SUM](/3sum/) the input is $x \in \mathbb{R}^n$, and the question is whether some $i < j < k$ have $x_i + x_j + x_k = 0$. For example, for $x = (-5, 1, 4, 7, -2)$ the answer is yes, with $-5 + 1 + 4 = 0$ and also $-5 + 7 - 2 = 0$. Sorting the input and then scanning with two pointers for each first index decides the problem with $O(n^2)$ tests, each on at most three variables. So the problem is in the 3-linear model with depth $O(n^2)$. The results on its depth depend on the number of variables allowed in a test.

- Erickson (1999; conference version 1995) proves depth $\Omega(n^{\lceil k/2 \rceil})$ for $k$-SUM in $k$-linear trees, and so $\Omega(n^2)$ for 3SUM in 3-linear trees.
- For general linear trees the quadratic bound is false. Grønlund and Pettie (2014) give a linear decision tree for 3SUM of depth $O(n^{3/2} \sqrt{\log n})$. Kane, Lovett and Moran (2018) improve the depth to $O(n \log^2 n)$, with tests on a bounded number of variables. So a quadratic bound for 3SUM needs a restriction on the tests, or another model.
- Meyer auf der Heide (1984) gives a linear decision tree of polynomial depth for the $n$-dimensional [knapsack problem](/knapsack-problem/). So an NP-hard problem can have polynomial depth in this model.
- Gajentaan and Overmars (1995) reduce many problems of computational geometry to 3SUM, and call these problems 3SUM-hard.

**Limits of the model.** The bound $\log_3(\text{number of leaves needed})$ is the only tool proved on this page. It cannot give more than a linear bound for a problem with $2^{O(n)}$ regions, and the model cannot describe algorithms whose tests need products of inputs. For those, use the [algebraic decision tree](/algebraic-decision-tree/) or the [algebraic computation tree](/algebraic-computation-tree/).

## References
