---
tag: 9YJTCD
kind: concept
slug: dynamic-optimality-conjecture
name: Dynamic optimality conjecture
aliases:
- splay tree optimality conjecture
area: data-structures/search-trees
level: research
summary: Open question whether splay trees are within a constant factor of any offline BST algorithm on any access sequence.
prereqs: [splay-tree, tree-rotation, competitive-ratio]
see_also: [tango-tree, static-optimality-theorem, working-set-theorem, splaying, online-algorithm, offline-algorithm, finger-search-tree, optimal-binary-search-tree]
sources:
  - paper: doi:10.1145/3828.3835
    title: Daniel D. Sleator and Robert E. Tarjan, Self-adjusting binary search trees, Journal of the ACM 32(3), 1985
    locator: the dynamic optimality conjecture, and Theorems 1 to 4 for the bounds of splaying
  - paper: doi:10.1137/0218004
    title: Robert Wilber, Lower bounds for accessing binary search trees with rotations, SIAM Journal on Computing 18(1), 1989
    locator: pages 56 to 67
  - paper: doi:10.1137/S0097539705447347
    title: Erik D. Demaine, Dion Harmon, John Iacono and Mihai Pătraşcu, Dynamic optimality, almost, SIAM Journal on Computing 37(1), 2007
    locator: Section 2 (the BST model and the interleave lower bound)
  - paper: doi:10.1137/1.9781611973068.55
    title: Erik D. Demaine, Dion Harmon, John Iacono, Daniel Kane and Mihai Pătraşcu, The geometry of binary search trees, SODA 2009
    locator: the equivalence of BST executions and arborally satisfied point sets, and the Greedy algorithm
---

The dynamic optimality conjecture, stated by Sleator and Tarjan in 1985, says that the [splay tree](/splay-tree/) is, up to a constant factor, as good as every binary search tree algorithm on every access sequence: for each sequence $X$ of $m$ accesses to $n$ keys, the cost of splaying is $O(\mathrm{OPT}(X) + n)$, where $\mathrm{OPT}(X)$ is the least cost of any BST algorithm that may rotate the tree as it likes and knows the whole sequence in advance. The conjecture is still open. The best proven [competitive ratio](/competitive-ratio/) for any online BST is $O(\log \log n)$, reached by the [tango tree](/tango-tree/) and later structures.

## In plain words

A splay tree changes its shape after each search, by fixed local rules, without knowing what comes next. Imagine a rival who knows every future search in advance and may reshape the tree in the best possible way at each step. The conjecture says the rival can never win by more than a fixed factor, whatever the searches are.

Many special cases are proved: the splay tree is as good as the best fixed tree, it is fast on keys used recently, and it is fast on keys near the last one. But nobody has proved that it is as good as the best changing tree in all cases, and nobody has found a case where it is not.

## The idea

**The BST model.** The keys $1, \ldots, n$ are in a binary search tree. To serve an access to key $x_i$, an algorithm has one pointer, which starts at the root. In unit steps it moves the pointer to a parent or a child, or does a [rotation](/tree-rotation/) at the pointer, and the pointer must visit $x_i$. The cost of the access is the number of distinct nodes touched. The algorithm may change the tree in any way that these steps allow. $\mathrm{OPT}(X)$ is the least total cost over all such algorithms and all initial trees, for the sequence $X = x_1, \ldots, x_m$, when the algorithm knows $X$ in advance (an [offline algorithm](/offline-algorithm/)).

**The conjecture.** An [online algorithm](/online-algorithm/) sees $x_i$ only when it must serve it. An online BST algorithm is *dynamically optimal* if its cost is $O(\mathrm{OPT}(X))$ for each $X$ (with an additive term that depends only on $n$). Sleator and Tarjan conjectured that splaying is dynamically optimal. A weaker form asks whether *any* online BST algorithm is dynamically optimal.

**What splaying is known to do.** Each of these bounds is a consequence that a dynamically optimal tree must also have, and splaying has all of them:

| bound | statement for the access $x_i$ (amortized) | source |
|---|---|---|
| balance | $O(\log n)$ | Sleator and Tarjan 1985 |
| [static optimality](/static-optimality-theorem/) | within a constant of the best static BST | Sleator and Tarjan 1985 |
| static finger | $O(\log(\lvert x_i - f \rvert + 1))$ for a fixed key $f$ | Sleator and Tarjan 1985 |
| [working set](/working-set-theorem/) | $O(\log(t_i + 1))$, $t_i$ distinct keys since the last access to $x_i$ | Sleator and Tarjan 1985 |
| sequential access | $O(1)$ when the keys are accessed in increasing order | Tarjan 1985 |
| dynamic finger | $O(\log(\lvert x_i - x_{i-1} \rvert + 1))$ | Cole 2000, with Mishra, Schmidt and Siegel |

**Lower bounds on OPT.** To compare an algorithm with OPT, one needs lower bounds on OPT that can be computed. Wilber (1989) gave two. The first, the *interleave bound*, fixes a perfectly balanced reference tree $P$ on the keys. For each node $y$ of $P$, label each access to a key in the subtree of $y$ as *left* if the key is in the left subtree of $y$ or is $y$, and *right* otherwise, and count the changes of label along the sequence. The sum of these counts over all $y$ is $\mathrm{IB}(X)$, and $\mathrm{OPT}(X) \ge \mathrm{IB}(X)/2 - n$. The [tango tree](/tango-tree/) costs $O(\log \log n)$ times the interleave bound, which gives its competitive ratio.

**The geometric view.** Demaine, Harmon, Iacono, Kane and Pătraşcu (2009) plot each access $x_i$ as the point $(x_i, i)$ in the plane. A set of points is *arborally satisfied* if each axis-parallel rectangle with two of its points at opposite corners, not on one horizontal or vertical line, contains a third point of the set. They proved that the BST executions on $X$ correspond to the arborally satisfied supersets of the access points, with the cost equal to the number of points up to a constant factor. So $\mathrm{OPT}(X)$ is, up to a constant, the size of the smallest arborally satisfied superset. The *Greedy* algorithm, proposed by Lucas (1988) and by Munro (2000) as an offline method, adds at each time $i$ the fewest points in row $i$ that satisfy all rectangles with the point $(x_i, i)$; the geometric view turns it into an online BST algorithm, and Greedy is another candidate for dynamic optimality.

## Examples

**Sequential access.** For $X = 1, 2, \ldots, n$ repeated, each static BST pays $\Theta(\log n)$ per access, but a splay tree pays $O(1)$ amortized, by the sequential access theorem. Here a dynamic tree beats every static one, and splaying matches the offline optimum up to a constant.

**The bit-reversal sequence.** For $n = 2^k - 1$, access the keys in the order of the reversed $k$-bit binary forms of $1, \ldots, n$; for $k = 3$ this is $4, 2, 6, 1, 5, 3, 7$. Wilber showed that this sequence has $\mathrm{OPT} = \Theta(\log n)$ per access, so no BST can do better than a balanced tree on it. For $k = 10$ and 10 rounds of the sequence ($m = 10230$), the interleave bound is $\mathrm{IB} = 81429$, so $\mathrm{OPT} \ge 81429/2 - 1023 \approx 39700$, about 3.9 per access. A splay tree built by inserting the keys in random order visited 165157 nodes, about 16.1 per access, a ratio of about 4.2 to the lower bound. For 10 rounds of sequential access the interleave bound is only 9709, and the same splay tree visited 53027 nodes.

**A small arborally satisfied set.** Take $X = 2, 3, 1$ on the keys $1, 2, 3$. The access points are $(2, 1)$, $(3, 2)$ and $(1, 3)$. The rectangle of $(2, 1)$ and $(3, 2)$ holds no third point, so Greedy adds $(2, 2)$: at time 2 the search touches 2 and 3. At time 3, the rectangle of $(1, 3)$ and $(2, 2)$ is empty, so Greedy adds $(2, 3)$; the rectangle of $(1, 3)$ and $(3, 2)$ now holds $(2, 2)$. The superset has 5 points, and it matches a BST execution that touches $\{2\}$, $\{2, 3\}$ and $\{1, 2\}$, with 2 at the root.

## Where it is used

- **Design of self-adjusting structures.** The conjecture is the standard against which online BSTs are measured. The tango tree, the multi-splay tree of Wang, Derryberry and Sleator, and others are $O(\log \log n)$-competitive.
- **Lower bound techniques.** The interleave bound, Wilber's second bound, and the independent rectangle bound of the geometric view are tools to bound OPT from below, and the known proofs of $O(\log \log n)$ competitive ratios rest on them.
- **Adaptive data structures.** The bounds that splaying satisfies, such as the [working set bound](/working-set-theorem/) and the dynamic finger bound, are used to analyse algorithms that call search trees in a non-random order, such as sweep-line algorithms and adaptive sorting.
- **Open problems.** Whether splaying, Greedy, or any online BST is $O(1)$-competitive, and whether $\mathrm{OPT}(X)$ can be computed or approximated within $o(\log \log n)$ in polynomial time, are open.

## References
