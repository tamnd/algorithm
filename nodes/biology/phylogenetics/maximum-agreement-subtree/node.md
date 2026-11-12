---
tag: THDNB4
kind: problem
slug: maximum-agreement-subtree
name: Maximum agreement subtree
aliases:
- MAST
area: biology/phylogenetics
level: advanced
summary: Find a largest set of leaves on which two or more phylogenetic trees restrict to the same tree. Polynomial for two trees, NP-hard for three trees of unbounded degree.
prereqs: [phylogenetic-tree, rooted-triplet, tree-dynamic-programming]
see_also: [maximum-agreement-forest, tree-comparison, robinson-foulds-distance, consensus-tree, bipartite-matching, maximum-weight-matching, tree-isomorphism, spr-distance]
sources:
  - paper: doi:10.1007/BF01908078
    title: C. R. Finden and A. D. Gordon, Obtaining common pruned trees, Journal of Classification 2(1), 1985
    locator: pp. 255 to 276, the definition of a common pruned tree and the first algorithms
  - paper: doi:10.1016/0020-0190(93)90181-8
    title: Mike Steel and Tandy Warnow, Kaikoura tree theorems, computing the maximum agreement subtree, Information Processing Letters 48(2), 1993
    locator: pp. 77 to 82, the dynamic program with bipartite matching, O(n^2) for bounded degree, and the reduction from unrooted to rooted trees
  - paper: doi:10.1137/S0097539796313477
    title: Richard Cole, Martin Farach-Colton, Ramesh Hariharan, Teresa Przytycka and Mikkel Thorup, An O(n log n) algorithm for the maximum agreement subtree problem for binary trees, SIAM Journal on Computing 30(5), 2000
    locator: pp. 1385 to 1404, the O(n log n) bound for two rooted binary trees
  - paper: doi:10.1137/S0097539794269461
    title: Amihood Amir and Dmitry Keselman, Maximum agreement subtree in a set of evolutionary trees, metrics and efficient algorithms, SIAM Journal on Computing 26(6), 1997
    locator: pp. 1656 to 1669, NP-hardness for three trees of unbounded degree and the polynomial algorithm for bounded degree
  - paper: "Jotun Hein, Tao Jiang, Lusheng Wang and Kaizhong Zhang, On the complexity of comparing evolutionary trees, Discrete Applied Mathematics 71(1-3), 1996"
    title: Jotun Hein, Tao Jiang, Lusheng Wang and Kaizhong Zhang, On the complexity of comparing evolutionary trees, 1996
    locator: pp. 153 to 169, the hardness of approximating MAST of three trees
---

The maximum agreement subtree problem asks for a largest set of taxa on which two or more phylogenetic trees agree. Remove the other taxa from each tree, suppress the nodes left with one child, and the trees that remain must be the same. The size of a maximum agreement subtree is a measure of how similar the trees are, and $n$ minus this size is a distance. For two trees the problem is solved by a [dynamic program](/tree-dynamic-programming/) over pairs of nodes, in $O(n^2)$ time for binary trees and $O(n \log n)$ with the best known method. For three trees of unbounded degree it is [NP-hard](/np-hard/). The related [maximum agreement forest](/maximum-agreement-forest/) cuts the trees into several agreeing pieces instead of keeping one.

## In plain words

Two studies give two family trees for the same species, and the trees do not fully agree. You want to know how much they have in common. One way is to throw away species, as few as possible, until the two trees look the same. The species you keep, with the tree they share, form a maximum agreement subtree.

When you throw a species away, you also tidy the tree: a branch point left with one branch is no longer a branch point. Two trees "look the same" if every group of kept species that sits together in one tree also sits together in the other.

## Definition

**Input.** Rooted trees $T_1, \ldots, T_k$ whose leaves are labeled by a set $X$ of $n$ taxa, each label used once in each tree, and every internal node with at least two children.

**Restriction.** For $S \subseteq X$, the tree $T|S$ is the smallest subtree of $T$ that contains the leaves in $S$, rooted at their [lowest common ancestor](/lowest-common-ancestor/), with every node of one child suppressed. Its clusters, the leaf sets of its subtrees, are exactly the nonempty sets $C \cap S$ for the clusters $C$ of $T$.

**Agreement.** $S$ is an *agreement set* if $T_1|S = T_2|S = \cdots = T_k|S$ as leaf-labeled rooted trees, which means that their cluster sets are equal. The common tree is an *agreement subtree*.

**The problem.** Find an agreement set $S$ of largest size. The *MAST* of the trees is this tree, and $|S|$ is its size.

**Unrooted trees.** For unrooted trees, restriction suppresses the nodes of degree 2, and agreement means that the split sets are equal.

The model: $n$ leaves, $k$ trees, the maximum degree $d$ of an internal node, rooted or unrooted. Costs are on the [word RAM](/word-ram/).

## Variants

- **Two rooted binary trees.** The best studied case, with an $O(n \log n)$ algorithm.
- **Two trees of any degree.** Still polynomial. The dynamic program uses a maximum weight [bipartite matching](/bipartite-matching/) between the children of two nodes.
- **Unrooted trees.** Steel and Warnow reduced the unrooted problem to a linear number of rooted instances.
- **Many trees.** With $k \ge 3$ trees, the problem is polynomial when the degrees are bounded by a constant and NP-hard when they are not bounded.
- **Maximum compatible tree.** For trees with polytomies, one may only ask that the kept tree refines every restricted tree, rather than equals it. This is the maximum compatible tree problem, which treats a polytomy as uncertainty and not as a hard claim.
- **The removal version.** Minimize $p = n - |S|$, the number of taxa removed. This is the same optimum but a different parameter for fixed-parameter algorithms.

## Examples

**Five taxa.** Take $T_1 = ((A,B),(C,(D,E)))$ and $T_2 = ((A,C),(B,(D,E)))$. Both trees have the cherry $(D,E)$. The four-leaf sets all fail. For example, $T_1|\{A,B,D,E\} = ((A,B),(D,E))$, but $T_2|\{A,B,D,E\} = (A,(B,(D,E)))$. The agreement sets of size 3 are $\{A,D,E\}$, $\{B,D,E\}$ and $\{C,D,E\}$, each with the tree $(x,(D,E))$. So the MAST has 3 leaves.

The dynamic program for two rooted trees computes $\mathrm{mast}(u, v)$, the size of a MAST of the subtree of $T_1$ at $u$ and the subtree of $T_2$ at $v$. For binary nodes $u$ with children $u_1, u_2$ and $v$ with children $v_1, v_2$,

$$\mathrm{mast}(u, v) = \max \left\{ \begin{array}{l} \mathrm{mast}(u_1, v_1) + \mathrm{mast}(u_2, v_2), \ \mathrm{mast}(u_1, v_2) + \mathrm{mast}(u_2, v_1), \\ \mathrm{mast}(u_1, v), \ \mathrm{mast}(u_2, v), \ \mathrm{mast}(u, v_1), \ \mathrm{mast}(u, v_2) \end{array} \right\}$$

and $\mathrm{mast}(a, v) = 1$ for a leaf $a$ if $a$ is below $v$, and 0 otherwise (and the same with the roles exchanged). The first two terms are the cases in which the root of the agreement subtree maps to both $u$ and $v$; the other four are the cases in which it lies inside one child.

Name the nodes of $T_1$: $u_0$ is the root, $u_1 = (A,B)$, $u_2 = (C,u_3)$ and $u_3 = (D,E)$. Name the nodes of $T_2$: $v_0$ is the root, $v_1 = (A,C)$, $v_2 = (B,v_3)$ and $v_3 = (D,E)$.

| pair | value | best case |
|---|---|---|
| $(u_3, v_3)$ | 2 | match D with D and E with E |
| $(u_1, v_1)$ | 1 | the leaf A |
| $(u_1, v_2)$ | 1 | the leaf B |
| $(u_2, v_1)$ | 1 | the leaf C |
| $(u_2, v_2)$ | 2 | inside $(u_3, v_3)$ |
| $(u_2, v_0)$ | 3 | match C with $v_1$ (1) and $u_3$ with $v_2$ (2) |
| $(u_0, v_0)$ | 3 | inside $(u_2, v_0)$, or $(u_1, v_1) + (u_2, v_2) = 1 + 2$ |

The traceback of the implementation returns $\{C, D, E\}$ with the tree $(C,(D,E))$.

**Two caterpillars in opposite order.** Let $T_1 = (((((1,2),3),4),\ldots),n)$ and let $T_2$ be the same caterpillar with the labels in reverse order. Any three leaves $a < b < c$ give the rooted triplet $ab|c$ in $T_1$ and $bc|a$ in $T_2$. So every agreement set has at most 2 leaves, and the MAST has size 2 for every $n \ge 2$.

## Known algorithms

| case | time | source |
|---|---|---|
| two rooted binary trees, the DP above | $O(n^2)$ | Steel and Warnow 1993 |
| two trees of bounded degree, DP with matching | $O(n^2)$ | Steel and Warnow 1993 |
| two trees of any degree | $O(n^{4.5} \log n)$ | Steel and Warnow 1993 |
| two rooted binary trees | $O(n \log n)$ | Cole, Farach-Colton, Hariharan, Przytycka and Thorup 2000 |
| $k$ trees, bounded degree $d$ | polynomial for fixed $d$ | Amir and Keselman 1997 |

The DP needs the answer for every pair of nodes, so it has $O(n^2)$ pairs. For binary trees each pair takes constant time, if the test "is leaf $a$ below node $v$" uses the preorder intervals of the leaves. For a node pair of degrees $d_1$ and $d_2$, the matching term is a maximum weight matching in a bipartite graph with $d_1 + d_2$ vertices, with the weights $\mathrm{mast}(u_i, v_j)$. Steel and Warnow solve it with a standard [maximum weight matching](/maximum-weight-matching/) algorithm. The implementation of this page uses a dynamic program over subsets of the smaller side, which is enough for small degrees. Its tests compare the DP with a brute force over all leaf subsets, for binary and non-binary trees with up to 9 leaves.

For two binary trees, the faster algorithms avoid computing all $n^2$ pairs. They decompose the trees into paths and do the matching steps with fast methods for the special bipartite graphs that occur.

## Bounds

- **Two trees.** The problem is in P for any degree. The best bound for two rooted binary trees is $O(n \log n)$. No superlinear lower bound is known.
- **Three or more trees.** Amir and Keselman proved in 1997 that the problem is NP-hard for three rooted trees when the degree is not bounded. When the degrees are at most a constant $d$, it is polynomial for each fixed $d$.
- **Approximation.** Hein, Jiang, Wang and Zhang showed in 1996 that the MAST of three trees of unbounded degree cannot be approximated within a factor $2^{\log^{\delta} n}$ in polynomial time for some $\delta > 0$, unless NP has quasi-polynomial time algorithms.
- **Fixed parameter.** For binary trees, a set $S$ is an agreement set if and only if every three leaves of $S$ give the same [rooted triplet](/rooted-triplet/) in all trees. So removing the fewest taxa is a [hitting set](/hitting-set/) problem with sets of size 3, the conflicting triples, and it is [fixed-parameter tractable](/fixed-parameter-tractable/) in the number $p$ of removed taxa, with time $O(3^p \cdot \mathrm{poly}(n))$ by branching on a conflicting triple.

## Reductions

- **To rooted triplets.** For binary trees, agreement is a property of triples, as above. For trees with polytomies, a triple can also be a fan, and agreement asks that each triple has the same shape (resolved in the same way, or a fan) in all trees.
- **Unrooted to rooted.** Steel and Warnow reduced the unrooted problem to rooted instances. A simple form of the idea: for a leaf $x$, root both trees at the neighbor of $x$ and delete $x$. A set $S \ni x$ agrees in the unrooted trees if and only if $S \setminus \{x\}$ agrees in the two rooted trees. Every nonempty agreement set contains some leaf, so $n$ rooted instances give the unrooted answer.
- **Isomorphism as a special case.** If the MAST has all $n$ leaves, the two trees are equal as leaf-labeled trees. The labeled case is easy, and it is not the same as unlabeled [tree isomorphism](/tree-isomorphism/).
- **Relation to agreement forests.** A maximum agreement subtree is one piece. A [maximum agreement forest](/maximum-agreement-forest/) partitions all taxa into agreeing pieces whose subtrees are disjoint, and the number of pieces gives the TBR and rSPR distances. A forest of $c$ pieces always contains a piece with at least $n/c$ leaves, so a small forest implies a large MAST, but not the other way.

## Applications

- **Comparing trees.** The MAST size, or $n$ minus it, is a measure of tree similarity that is easy to read: it names the taxa that cause the conflict. It is one of the measures discussed on the [tree comparison](/tree-comparison/) page, next to the [Robinson-Foulds distance](/robinson-foulds-distance/).
- **Consensus.** A MAST of a set of trees is a consensus that keeps a fully resolved tree on fewer taxa, instead of a less resolved tree on all taxa as in a [consensus tree](/consensus-tree/).
- **Rogue taxa.** The taxa outside a MAST are candidates for unstable taxa that move from tree to tree, for example among bootstrap trees.
- **Gene trees.** Gene trees for the same species often differ. A MAST of several gene trees gives a set of species on which all the genes tell the same story.

## References
