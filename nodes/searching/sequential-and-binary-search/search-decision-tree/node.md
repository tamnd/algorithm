---
tag: PT786H
kind: model
slug: search-decision-tree
name: Decision tree for search
aliases:
- comparison decision tree for search
area: searching/sequential-and-binary-search
level: advanced
summary: Model in which each comparison is an internal node with two branches, so the worst-case search cost is at least the tree height.
prereqs: [decision-tree-model, comparison-model, binary-search]
see_also: [search-lower-bound, sorted-search-lower-bound, binary-search-tree, optimal-binary-search-tree, decision-tree-model, algebraic-decision-tree, cell-probe-model, query-complexity]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an ordered table (comparison trees, internal and external nodes, and the cost of binary search); Section 6.2.2 (optimum binary search trees)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.4.5, Path length (internal and external path length, E = I + 2n)
---

The decision tree for search is the [decision tree model](/decision-tree-model/) specialized to searching a sorted array. For a fixed size $n$, an algorithm is a tree whose inner nodes each compare the search key $x$ with one array item $A[i]$, whose branches are the possible answers, and whose leaves give the result: an index where $x$ occurs, or the gap where $x$ would go. The cost of a search is the number of comparisons on its path, so the worst-case cost is the height of the tree and the average cost is a path length. All other work is free. In this model [binary search](/binary-search/) is optimal, and every reasonable three-way search tree is a [binary search tree](/binary-search-tree/) on the keys, which links search algorithms to search trees: choosing a search strategy and choosing a tree shape are the same thing.

## The machine

Fix $n \ge 0$ and a sorted array $A[1] \le \cdots \le A[n]$ from a [total order](/total-order/). The key $x$ is the only unknown; the order among the items is known in advance, so comparisons between two items are not needed and are not part of the model.

A **three-way search tree** for $n$ is a rooted tree with these nodes:

- An **inner node** is labeled with an index $i \in \{1, \ldots, n\}$. It compares $x$ with $A[i]$ and has three branches, for $x < A[i]$, $x = A[i]$ and $x > A[i]$.
- A **leaf** is labeled with an output: "found at $i$", or "absent", often with the gap $g$ where $A[g] < x < A[g+1]$.

A **two-way search tree** is the same with inner nodes that test "$x < A[i]$" or "$x \le A[i]$" and have two branches. Its leaves output the gap or the index of the [lower bound](/lower-bound-query/).

The run on a key $x$ starts at the root, follows at each inner node the branch of the true answer, and ends at a leaf. The tree is **correct** when the leaf is right for every $x$ and every array of the given order type. With distinct items the order type is fixed, and $x$ falls in one of $2n + 1$ **cells**: one of the $n$ items or one of the $n + 1$ gaps.

**The normal form.** Remove the $=$ branches by making each inner node a key and each $=$ branch an exit that is taken there. A three-way tree is then an extended binary tree: $n$ inner nodes for the keys and $n + 1$ leaves for the gaps, in the form used by Knuth. For $n = 3$, binary search is the tree with $A[2]$ at the root, $A[1]$ and $A[3]$ as its children, and the four gaps $g_0, g_1, g_2, g_3$ as leaves below them, from left to right.

## What it counts

Only comparisons of $x$ with items count, one per inner node on the path.

- **Worst case.** The height $h$ of the tree: the largest number of inner nodes on a root-to-leaf path.
- **Successful search.** In the normal form, a search for $A[i]$ costs the depth of the node $i$ plus one. The average over the $n$ keys is $(I + n)/n$, where $I$ is the internal path length, the sum of the depths of the inner nodes.
- **Unsuccessful search.** A search that ends in a gap costs the depth of that leaf. The average over the $n + 1$ gaps is $E/(n+1)$, where $E$ is the external path length, the sum of the depths of the leaves.
- **Weighted cost.** With probabilities $p_i$ for the keys and $q_g$ for the gaps, the cost is $\sum_i p_i (\text{depth}(i) + 1) + \sum_g q_g \, \text{depth}(g)$. This is the cost minimized by an [optimal binary search tree](/optimal-binary-search-tree/).

In every extended binary tree with $n$ inner nodes, $E = I + 2n$. For the tree of binary search with $n = 3$: $I = 0 + 1 + 1 = 2$, $E = 4 \cdot 2 = 8 = 2 + 6$, the successful average is $5/3$ and the unsuccessful average is 2.

Because only the queries count, a lower bound in this model holds for every algorithm that learns about $x$ only by comparing it with items, however much other work it does.

## Relation to other models

- **[Decision tree model](/decision-tree-model/).** The search tree is a decision tree whose queries are the comparisons "$x$ against $A[i]$", with three answers or two.
- **[Comparison model](/comparison-model/).** A comparison algorithm for search on inputs of size $n$ unrolls into a search tree: its run on each key is a path of comparisons. In the general comparison model the algorithm can also compare two items, but for a sorted array those answers are known, so they can be removed without changing the cost. For an unsorted array they are needed, and the problem is different: see [search in an unordered array](/search-in-unordered-array/), with cost $n$.
- **Two-way and three-way.** A three-way node can be simulated by two two-way nodes. The two-way model forces separate tests for "$<$" and "$=$", and its optimal worst case for finding a key is $\lfloor \lg n \rfloor + 2$ against $\lfloor \lg n \rfloor + 1$, as shown on [sorted search lower bound](/sorted-search-lower-bound/).
- **[Algebraic decision trees](/algebraic-decision-tree/).** Queries are signs of arithmetic expressions in the keys and $x$. [Interpolation search](/interpolation-search/) computes such expressions, so it is outside the search tree model, and the $\lg(n+1)$ bound does not apply to it.
- **[Cell probe model](/cell-probe-model/).** Cost is the number of memory words read, and words can hold any data built in advance. For integer keys this allows predecessor search in less than $\lg n$ probes; the search tree model is the special case where a probe reads one item and only its order relative to $x$ is used.
- **[Query complexity](/query-complexity/).** The search tree is a query algorithm for a function of the hidden position of $x$; randomized and other query models apply to it in the usual way.

## Known results in the model

- **Worst case.** The least height of a correct three-way tree for $n$ distinct keys is $\lceil \lg(n+1) \rceil$, met by binary search; with two-way tests it is $\lceil \lg(2n+1) \rceil$. See [search lower bound](/search-lower-bound/) and [sorted search lower bound](/sorted-search-lower-bound/).
- **Average case.** Over uniform gaps the least external path length is $E(N) = Nq + 2(N - 2^q)$ with $N = n + 1$ and $q = \lfloor \lg N \rfloor$, met exactly by the trees whose leaves lie on two adjacent levels, such as binary search. Randomized algorithms still need $\lg(n+1)$ comparisons in expectation on some gap.
- **Normal form is a search tree.** In a tree without redundant comparisons (none whose answer is forced by the comparisons above it), the set of keys that reach a node is an interval of cells, and each item $A[i]$ is compared at exactly one node, the one whose interval contains $A[i]$ and is split by it. So the normal form has exactly $n$ inner nodes, and its in-order is $A[1], \ldots, A[n]$: it is a binary search tree on the keys, and every search strategy is a binary search tree.
- **Weighted case.** With given probabilities, the best tree is an optimal binary search tree, found in $O(n^2)$ time by dynamic programming with [Knuth's optimization](/knuth-optimization/). Its cost is within a small additive term of the entropy of the distribution.
- **Range and position queries.** Finding both ends of the block of copies of $x$ needs $\lceil \lg(n(n+1)/2 + 1) \rceil$ two-way tests: see [first and last occurrence](/first-and-last-occurrence/).
- **Unbounded search.** When $n$ is not known, a tree must handle every $n$; the cost then grows like $\lg n + \lg \lg n + \cdots$, as on [unbounded search](/unbounded-search/).
- **Other orders.** For a matrix sorted by rows and columns, the same model with an adversary gives $2n - 1$ comparisons for $n \times n$, met by [staircase search](/staircase-search/); see [search in a sorted matrix](/sorted-matrix-search/).

## References
