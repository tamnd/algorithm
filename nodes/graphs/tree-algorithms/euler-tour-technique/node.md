---
tag: RMW47N
kind: technique
slug: euler-tour-technique
name: Euler tour technique
aliases:
- Euler tour
- Euler tour of a tree
- tree flattening
area: graphs/tree-algorithms
level: core
summary: Linearize a tree with entry and exit times so every subtree becomes a contiguous interval.
prereqs: [depth-first-search, rooted-tree, discovery-and-finish-times]
see_also: [euler-tour-subtree-queries, euler-tour-lca, parenthesis-theorem, dsu-on-tree, euler-tour-tree, tree-path-queries, fenwick-tree, segment-tree]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 18, Tree queries, Section 18.2 (Subtrees and paths, the tree traversal array) and Section 18.3 (Lowest common ancestor, the Euler tour method)
  - paper: "Robert E. Tarjan and Uzi Vishkin, An efficient parallel biconnectivity algorithm, SIAM Journal on Computing 14(4) (1985), 862-874"
    locator: the Euler tour of a tree as a list of directed edges, and the tree computations (preorder numbers, subtree sizes, depths) done on it by parallel prefix sums
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.3, Depth-first search (discovery and finish times and the parenthesis theorem)
  - paper: doi:10.1007/10719839_9
    title: "Michael A. Bender and Martin Farach-Colton, The LCA Problem Revisited, LATIN 2000: Theoretical Informatics, LNCS 1776, 88-94"
    locator: Section 2 (the Euler tour of 2n - 1 vertices with their levels, and LCA as a range minimum)
---

The Euler tour technique writes a [rooted tree](/rooted-tree/) as a sequence by a [depth-first search](/depth-first-search/): each vertex is recorded when the search enters it, and in some forms also when the search returns to it or leaves it. In the sequence, the subtree of each vertex is a contiguous block, a vertical path is a prefix sum, and the lowest common ancestor of two vertices is the shallowest vertex between their first visits. So a question about subtrees or paths becomes a question about ranges of an array, which a [Fenwick tree](/fenwick-tree/), a [segment tree](/segment-tree/) or a [sparse table](/sparse-table/) answers. The tour takes $O(n)$ time to build.

## In plain words

Walk around a tree drawn on paper, keeping the tree on your left hand side, starting and ending at the top. Write down each vertex when you first reach it. Everything below a vertex is written in one run, right after it, because you finish the whole part below it before you walk back past it. So the part below a vertex is one stretch of your list, from where you wrote that vertex to just before the next vertex that is not below it.

Now a question about everything below a vertex, such as "what is the total of the numbers stored there", is a question about one stretch of a list, and there are fast tools for stretches of lists. Other ways of writing the walk, which also note when you pass a vertex on the way back, let you answer questions about paths and shared ancestors.

## When it applies

- **Queries about whole subtrees.** "Sum, minimum or count over the subtree of $v$" and "add $x$ to each vertex of the subtree of $v$" become range queries and range updates on the entry order. See [subtree queries via Euler tour](/euler-tour-subtree-queries/).
- **Ancestor tests.** "Is $a$ an ancestor of $b$?" is a comparison of entry and exit times, by the [parenthesis theorem](/parenthesis-theorem/).
- **Root-to-vertex path queries with an invertible operation.** With $+x$ at the entry of $v$ and $-x$ at its exit, the prefix sum at the entry of $v$ is the sum on the path from the root to $v$.
- **LCA by range minimum.** In the tour that records a vertex at each visit, the LCA is a range minimum by depth. See [LCA by Euler tour and RMQ](/euler-tour-lca/).
- **The tree is static, or changes in ways the sequence can follow.** A plain array needs a fixed tree. A balanced search tree over the tour, as in [Euler tour trees](/euler-tour-tree/), allows links and cuts.

## The template

The input is a tree on the vertices $0, \ldots, n-1$, rooted at $r$, with the children of each vertex in a fixed order (for example by label). The tree may carry values on the vertices; the tour itself does not use weights. The DFS is iterative: a stack holds pairs (vertex, index of the next child), so a path of $10^5$ vertices needs no deep recursion.

```pseudo id=main
EULER-TOUR(T, r)
L1  t ← 0;  S ← a stack holding (r, 0)
L2  ENTER(r)                                   ▷ hole: tin(r) ← t; order[t] ← r; t ← t + 1; append r to the tours
L3  while S is not empty do
L4      (v, i) ← the top of S
L5      if i < the number of children of v then
L6          replace the top of S by (v, i + 1)
L7          c ← the i-th child of v
L8          ENTER(c);  push (c, 0) on S
L9      else
L10         pop S;  LEAVE(v)                   ▷ hole: tout(v) ← t; append the exit of v to the 2n tour
L11         if S is not empty then RETURN-TO(the top vertex of S)   ▷ hole: append it to the 2n − 1 tour
```

The three holes decide which sequence is built.

| sequence | length | recorded at | use |
|---|---|---|---|
| entry order $order[0..n-1]$ with $tin$, $tout$ | $n$ | ENTER | subtree $=$ $order[tin(v) \ldots tout(v) - 1]$ |
| tour of $2n - 1$ vertices | $2n - 1$ | ENTER and RETURN-TO | LCA as a range minimum of depth |
| bracket tour, entry and exit | $2n$ | ENTER ($+v$) and LEAVE ($-v$) | root-to-vertex path sums |

The walk-through: the top of the stack is the vertex the search is in. Line L5 asks whether it has a child left to visit. If so, lines L6 to L8 enter that child. If not, line L10 leaves the vertex, and line L11 notes the return to its parent, now on top.

**Why a subtree is a block.** The time $t$ counts ENTER calls, so $tin$ is the preorder number. A vertex $v$ is pushed at its ENTER and popped at its LEAVE, and between these the stack holds $v$ with only descendants of $v$ above it. So the vertices entered in the interval are exactly the descendants of $v$: each descendant is entered while $v$ is on the stack, and each vertex entered while $v$ is on the stack is pushed above $v$, hence is a descendant. With $tout(v)$ the value of $t$ at LEAVE, the subtree of $v$ is the set of vertices $x$ with $tin(v) \le tin(x) < tout(v)$, it has $tout(v) - tin(v)$ vertices, and it is the block $order[tin(v) \ldots tout(v) - 1]$. For two vertices the intervals $[tin, tout)$ are nested or disjoint, which is the [parenthesis theorem](/parenthesis-theorem/).

**Cost.** Each vertex is pushed once and popped once, and line L5 is true once per child, so the loop runs $2n - 1$ times. The time is $\Theta(n)$ and the stack holds at most $h + 1$ pairs, where $h$ is the height.

## Classic examples

The examples use the tree on $0, \ldots, 11$ rooted at 0 with the parent array $[-, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]$ and children in increasing order. Its children lists are $0: [1, 8]$, $1: [2]$, $2: [3, 6]$, $3: [4, 10]$, $4: [5]$, $6: [7]$, $7: [11]$, $8: [9]$.

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $tin(v)$ | 0 | 1 | 2 | 3 | 4 | 5 | 7 | 8 | 10 | 11 | 6 | 9 |
| $tout(v)$ | 12 | 10 | 10 | 7 | 6 | 6 | 10 | 10 | 12 | 12 | 7 | 10 |

The entry order is $0, 1, 2, 3, 4, 5, 10, 6, 7, 11, 8, 9$. The subtree of 3 is $order[3 \ldots 6] = 3, 4, 5, 10$, and the subtree of 6 is $order[7 \ldots 9] = 6, 7, 11$. The tour of $2n - 1 = 23$ vertices is $0, 1, 2, 3, 4, 5, 4, 3, 10, 3, 2, 6, 7, 11, 7, 6, 2, 1, 0, 8, 9, 8, 0$.

For the bracket tour, give the vertices the values $3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8$. The tour is $+0, +1, +2, +3, +4, +5, -5, -4, +10, -10, -3, +6, +7, +11, -11, -7, -6, -2, -1, +8, +9, -9, -8, -0$, with the value of the vertex at its entry and the negative value at its exit. The entry of 11 is at position 13, and the prefix sum up to it is $24 = 3 + 1 + 4 + 2 + 6 + 8$, the values of the path $0, 1, 2, 6, 7, 11$. The entry and the exit of each of 3, 4, 5 and 10 come before it and cancel, because the subtree of 3 is finished.

For one vertex, $order = [0]$, $tin(0) = 0$, $tout(0) = 1$, and both tours have one or two entries. For a path $0 - 1 - \cdots - (n-1)$ rooted at 0, $tin(v) = v$ and $tout(v) = n$ for each $v$: every subtree is a suffix, and the stack grows to $n$ pairs, which is why the template is iterative. For a star rooted at its center 0, $tin(0) = 0$, $tout(0) = n$, and each leaf $v$ is a block of length 1.

Uses, from simple to hard:

1. **[Subtree sizes](/subtree-sizes/) and ancestor tests.** $size(v) = tout(v) - tin(v)$; $a$ is an ancestor of $b$ if and only if $tin(a) \le tin(b) < tout(a)$.
2. **[Subtree queries](/euler-tour-subtree-queries/).** Store the value of $v$ at position $tin(v)$ of a [Fenwick tree](/fenwick-tree/); a subtree sum is a range sum, and a point update is a point update. The subtree sum of 3 above is $1 + 5 + 9 + 5 = 20$.
3. **[LCA by Euler tour and RMQ](/euler-tour-lca/).** The LCA of $u$ and $v$ is the vertex of least depth in the $2n - 1$ tour between the first visits of $u$ and $v$.
4. **Path sums with updates.** On the bracket tour, a Fenwick tree gives root-to-vertex sums with point updates; a path $u \to v$ is $s(u) + s(v) - 2 s(\ell) + val(\ell)$ with $\ell$ the LCA.
5. **[DSU on tree](/dsu-on-tree/).** The entry order lets the method loop over all vertices of a light subtree as one array range.
6. **Parallel tree computations.** Tarjan and Vishkin build the tour as a linked list of directed edges and rank it by [list ranking](/list-ranking/); preorder numbers, depths and subtree sizes then follow from [parallel prefix sums](/parallel-prefix/).
7. **[Euler tour trees](/euler-tour-tree/).** Keep the tour of each tree of a forest in a balanced search tree; a link or a cut is a few splits and joins, so connectivity in a changing forest takes $O(\log n)$ time per operation.

## Variations

- **Exit times inclusive.** Some texts set $tout(v)$ to the last entry time in the subtree, $tin(v) + size(v) - 1$, and use closed ranges. Both work; mixing them is the most common bug.
- **Discovery and finish on one clock.** CLRS increments one clock at both entry and exit. Then each time is in $1, \ldots, 2n$, and the subtree of $v$ is the set of $x$ with $d(v) < d(x) < f(v)$.
- **Edge tour.** Replace each edge by two arcs, one down and one up. The tour is the cyclic list of the $2(n-1)$ arcs in which the successor of the arc $(u, v)$ is the arc out of $v$ that follows $(v, u)$ in the cyclic order of $v$'s neighbors. It needs no DFS, only the adjacency lists, so it is the form for parallel algorithms.
- **Heavy-first order.** If each vertex enters its largest child first, the entry order also makes each heavy path of a [heavy-light decomposition](/heavy-light-decomposition/) contiguous, so one array serves both subtree and path queries.
- **Balanced parentheses.** Writing "(" at each entry and ")" at each exit gives $2n$ bits that encode the shape of an ordered tree, the base of [succinct tree representations](/balanced-parentheses-representation/).

## Pitfalls

- **Positions and labels mixed up.** A range structure is indexed by $tin(v)$, not by $v$. Writing the value of $v$ at index $v$ makes subtree ranges hold the wrong vertices.
- **Half-open and closed ranges mixed.** If $tout$ is exclusive, the subtree is $[tin, tout - 1]$; using $[tin, tout]$ adds the next vertex outside the subtree.
- **Using the wrong tour.** The $n$-entry order cannot answer LCA by range minimum: in it, the shallowest vertex between $u$ and $v$ can lie outside the path. That needs the $2n - 1$ tour.
- **Recursion depth.** A recursive DFS on a path of $10^5$ vertices exceeds Python's default limit. Use the stack of the template.
- **The parent as a child.** With undirected adjacency lists, the DFS must skip the parent of $v$, or it walks back up and never ends.

## Exercises

1. Show that $a$ is an ancestor of $b$ if and only if $tin(a) \le tin(b)$ and $tout(b) \le tout(a)$.
2. Using one Fenwick tree on the entry order, support "add $x$ to each vertex in the subtree of $v$" and "return the value of vertex $u$".
3. Using the bracket tour and a Fenwick tree, support "change the value of $v$" and "return the sum of the values on the path from $u$ to $w$", given an LCA oracle.
4. Prove that the $2n - 1$ tour has each vertex $v$ exactly $1 + c(v)$ times, where $c(v)$ is the number of children of $v$.

## References
