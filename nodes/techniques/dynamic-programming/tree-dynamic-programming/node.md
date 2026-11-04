---
tag: JY93E9
kind: technique
slug: tree-dynamic-programming
name: Tree dynamic programming
aliases:
- DP on trees
- tree DP
area: techniques/dynamic-programming
level: core
summary: Compute values bottom-up over a rooted tree from the results of each node's children.
prereqs: [rooted-tree, depth-first-search, postorder-traversal, optimal-substructure]
see_also: [maximum-independent-set-in-trees, independent-set-on-trees, tree-diameter, dp-on-tree-decompositions, vertex-cover, dominating-set, dp-on-dag, bitmask-dp]
sources:
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms, 2019
    locator: Chapter 3, Dynamic Programming, the section Dynamic Programming on Trees (maximum independent set in a tree)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 14, end-of-chapter problems, Planning a company party
  - book: isbn:9783030393564
    title: Antti Laaksonen, Guide to Competitive Programming, second edition, Springer, 2020
    locator: the chapter on tree algorithms (dynamic programming on trees and the computation for all roots)
---

Tree dynamic programming solves a problem on a tree by rooting it, giving each vertex $v$ a small table of values for the subtree of $v$, and computing the table of $v$ from the tables of its children. The subtrees are the subproblems: they are nested, the subtrees of different children are disjoint, and a vertex has one parent, so a [postorder traversal](/postorder-traversal/) computes every table once. When each table has $O(1)$ entries and the merge of a child takes $O(1)$ time, the whole computation takes $O(n)$ time. [Maximum weight independent set in a tree](/maximum-independent-set-in-trees/), minimum [vertex cover](/vertex-cover/) and [dominating set](/dominating-set/) in a tree, and the [tree diameter](/tree-diameter/) are standard examples; all of them are NP-hard on general graphs except the diameter.

## In plain words

A tree has no cycles, so if you pick one vertex as the top, every other vertex hangs below exactly one parent. Each vertex is the top of its own smaller tree, made of itself and everything below it.

Solve the problem for each small tree, from the bottom up. A leaf is easy. For a vertex higher up, its children have already solved their own small trees, and those small trees do not touch each other. So you only need to decide what happens at the vertex itself and combine the answers of the children. For many problems, each child only has to report two or three numbers, for example its best answer when it is used and when it is not used.

## When it applies

- The input is a tree, or a forest, or a graph that can be cut into a tree of small pieces (then see [DP on tree decompositions](/dp-on-tree-decompositions/)).
- After rooting, the interaction between the subtree of a vertex $v$ and the rest of the tree passes only through $v$, and a small amount of information about $v$ is enough to describe it: whether $v$ is chosen, the color of $v$, the depth of the deepest vertex below $v$.
- The value for $v$ is a combination over the children that can be done one child at a time: a sum, a minimum, a maximum, or a small knapsack.

## The template

Root the tree at $r$. The holes are the states of a vertex, the value of a leaf and the merge of one child.

```pseudo id=main
TREE-DP(v, parent)
L1  T[v] ← init(v)                                 ▷ hole: the table of v without children
L2  for each neighbor u of v with u ≠ parent do
L3      TREE-DP(u, v)                              ▷ the table of u is complete
L4      T[v] ← merge(T[v], T[u], v, u)              ▷ hole: add the subtree of u to v
L5  T[v] ← finish(T[v], v)                          ▷ hole: optional last step at v
L6  return

L7  TREE-DP(r, nil); return answer(T[r])            ▷ hole: read the answer from the root
```

**Why it is correct.** Let $T_v$ be the subtree of $v$. When line L4 runs for the child $u$, the table $T[u]$ describes $T_u$ completely, by induction on the height. The subtrees of the children are disjoint and have no edges between them, and each edge from $T_u$ to the rest of the tree is the edge $uv$. So any solution on $T_v$ is a choice at $v$, together with one solution on each $T_u$ that agrees with that choice on the edge $uv$, and these parts can be optimized one at a time. This is the [optimal substructure](/optimal-substructure/) of the problem.

**Cost.** Each vertex is visited once and each edge is merged once, so the time is $O(n)$ times the cost of one merge. The recursion depth is the height of the tree, which can be $n - 1$. For deep trees, compute a parent array and an order of the vertices by a breadth-first or an iterative [depth-first search](/depth-first-search/), and process the vertices in the reverse of that order.

## Classic examples

### Maximum weight independent set

Choose vertices, no two adjacent, with the largest total weight. Each vertex keeps two values: $in(v)$, the best weight in $T_v$ with $v$ chosen, and $out(v)$, the best with $v$ not chosen. Then

$$in(v) = w(v) + \sum_{u \text{ child}} out(u), \qquad out(v) = \sum_{u \text{ child}} \max(in(u), out(u)).$$

Take the tree rooted at 1 with children $1 \to \{2, 3\}$, $2 \to \{4, 5\}$, $3 \to \{6, 7\}$, and the weights $w = (3, 2, 1, 4, 1, 5, 2)$ for the vertices $1, \ldots, 7$.

| $v$ | 4 | 5 | 6 | 7 | 2 | 3 | 1 |
|---|---|---|---|---|---|---|---|
| $in(v)$ | 4 | 1 | 5 | 2 | 2 | 1 | 15 |
| $out(v)$ | 0 | 0 | 0 | 0 | 5 | 7 | 12 |

For example $out(2) = \max(4, 0) + \max(1, 0) = 5$ and $in(1) = 3 + out(2) + out(3) = 3 + 5 + 7 = 15$. The answer is $\max(15, 12) = 15$, with the set $\{1, 4, 5, 6, 7\}$; a check of all $2^7$ sets gives the same value. This is CLRS's problem "Planning a company party", where the tree is the company and the weights are how much fun each guest adds, and Erickson's example of dynamic programming on trees.

### All roots at once: the sum of the distances

For each vertex $v$, let $D(v)$ be the sum of the distances from $v$ to all vertices. A first pass from the root computes the subtree sizes $s(v)$ and $down(v) = \sum_{u \text{ child}} (down(u) + s(u))$, which is $D(r)$ at the root. A second pass, from the top down, moves the root across each edge: when the root moves from the parent $p$ to $v$, the $s(v)$ vertices below $v$ come one step closer and the other $n - s(v)$ go one step away, so

$$D(v) = D(p) + n - 2 s(v).$$

On the tree above with $n = 7$: $s = (7, 3, 3, 1, 1, 1, 1)$, $D(1) = down(1) = 10$, $D(2) = D(3) = 10 + 7 - 6 = 11$, and $D(4) = \cdots = D(7) = 11 + 7 - 2 = 16$. A breadth-first search from each vertex confirms these values. This two-pass method is often called rerooting.

### Other classic uses

- **[Tree diameter](/tree-diameter/).** Keep the depth of the deepest leaf below $v$; at $v$ the longest path through $v$ joins the two largest child depths.
- **Minimum [vertex cover](/vertex-cover/) and [dominating set](/dominating-set/).** Two or three states per vertex, in the same form as the independent set.
- **Tree knapsack.** Choose $k$ vertices of a tree so that a chosen vertex has its parent chosen, with the most weight. The table of $v$ is indexed by the number of chosen vertices in $T_v$, and line L4 is a max-plus product of two tables. With the sizes bounded by the subtree sizes, the total time is $O(n^2)$, not $O(n^3)$, since each pair of vertices is joined in one merge only, at their lowest common ancestor.
- **Counting.** Count the independent sets, or the colorings of a tree, by replacing max with sum.

## Variations

- **Rerooting.** As in the sum of distances: a bottom-up pass, then a top-down pass that gives each child the answer of "the rest of the tree" through its parent. When the merge has no inverse (for example a maximum), use prefix and suffix combinations of the children of each vertex.
- **Small to large merging.** When a table is a set or a map of size up to the subtree size, always merge the smaller table into the larger. Each element moves $O(\log n)$ times, which gives $O(n \log n)$ moves in total.
- **Graphs of small treewidth.** Replace the tree by a tree decomposition and a vertex by a bag. The table of a bag is indexed by the states of all its vertices, which gives [DP on tree decompositions](/dp-on-tree-decompositions/).
- **Forests and unrooted trees.** Run the template from one root in each component and combine the answers. For an unrooted problem, any root gives the same answer.

## Pitfalls

- **Stack overflow.** A path of $10^5$ or $10^6$ vertices makes the recursion that deep. Use an explicit order instead.
- **Treating the parent as a child.** In an adjacency list of an undirected tree, the parent is also a neighbor; line L2 must skip it.
- **A state that is too small.** For the dominating set, "chosen or not chosen" is not enough: a vertex that is not chosen may be dominated by its parent, which the subtree cannot see. Use three states: chosen, dominated by a child, or waiting for the parent.
- **Quadratic merges by accident.** In the tree knapsack, a loop up to $k$ for every child, instead of up to the current subtree size, makes the time $O(n k^2)$ or worse.

## Exercises

1. Give the recurrences for the minimum vertex cover of a tree with two states per vertex, and run them on the tree above with all weights 1.
2. Count the independent sets of a path with $n$ vertices by tree DP, and show that the counts are Fibonacci numbers.
   <details><summary>Hint</summary>With $in$ and $out$ counts, $in(v) = out(u)$ and $out(v) = in(u) + out(u)$ for the single child $u$.</details>
3. For each vertex of a tree, find the largest distance to any other vertex, in $O(n)$ total time.
4. Prove that the tree knapsack with the merge bounded by the subtree sizes runs in $O(n^2)$ time.

## References
