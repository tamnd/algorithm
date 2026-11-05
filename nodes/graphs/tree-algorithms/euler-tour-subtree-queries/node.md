---
tag: VYY0XM
kind: problem
slug: euler-tour-subtree-queries
name: Subtree queries via Euler tour
aliases:
- Subtree queries
area: graphs/tree-algorithms
level: core
summary: Problem of answering subtree sum or update queries by flattening a tree with an Euler tour into a range.
prereqs: [euler-tour-technique, fenwick-tree]
see_also: [segment-tree, lazy-propagation, point-update-range-sum-query, range-update-range-query, subtree-sizes, tree-path-queries, dsu-on-tree, heavy-light-decomposition]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 18, Tree queries, Section 18.2 (Subtrees and paths, the tree traversal array, subtree queries and path queries)
  - url: https://usaco.guide/gold/tree-euler
    title: USACO Guide, Euler Tour Technique
    locator: the sections on flattening a tree into an array and on subtree queries with a range structure
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: the Omega(lg n) lower bound for the partial sums problem
---

The subtree query problem asks to keep a value on each vertex of a [rooted tree](/rooted-tree/) and to answer, many times and mixed with updates, an aggregate such as the sum over all vertices of the subtree of a given vertex. The standard solution writes the vertices in the entry order of an [Euler tour](/euler-tour-technique/), where each subtree is one contiguous range, and keeps that array in a [Fenwick tree](/fenwick-tree/) or a [segment tree](/segment-tree/). Each update and each query then takes $O(\log n)$ time, after an $O(n)$ tour. A path is a special tree, so the problem is at least as hard as [partial sums](/point-update-range-sum-query/), and $O(\log n)$ is optimal in the cell-probe model.

## In plain words

A company keeps a number for each employee, for example the sales of the month. The manager of a department wants the total of the whole department, which is the manager, the people below the manager, the people below them, and so on. Numbers change during the month, and totals are asked again and again.

Adding up the department each time is slow for a big department. The trick is to list the employees in the order of a walk through the company chart, so that each department forms one unbroken stretch of the list. Then a department total is the total of a stretch, and a change is a change of one entry. There are known structures that do both quickly, even for a very long list.

## Definition

**Input.** A tree on the vertices $\{0, \ldots, n-1\}$, $n \ge 1$, rooted at $r$, unweighted, and an initial value $a_v$ in an abelian group $(G, +)$ for each vertex $v$ (for example the integers). Write $\mathrm{sub}(v)$ for the set of descendants of $v$, including $v$.

**Operations.**

- $\mathrm{update}(v, x)$: set $a_v \gets a_v + x$.
- $\mathrm{query}(v)$: return $\sum_{u \in \mathrm{sub}(v)} a_u$.

The operations arrive online, and each answer must reflect all earlier updates.

**The reduction to ranges.** Let $tin(v)$ be the preorder number of $v$ in a depth-first search from $r$ and $tout(v) = tin(v) + |\mathrm{sub}(v)|$. Then $\mathrm{sub}(v) = \{u : tin(v) \le tin(u) < tout(v)\}$. With $B[tin(u)] = a_u$, $\mathrm{query}(v) = \sum_{i = tin(v)}^{tout(v) - 1} B[i]$, and $\mathrm{update}(v, x)$ adds $x$ to $B[tin(v)]$. The proof that subtrees are ranges is on the [Euler tour technique](/euler-tour-technique/) page.

## Variants

- **Subtree update, point query.** Add $x$ to each vertex of $\mathrm{sub}(v)$; read one $a_u$. Store differences: add $x$ at $tin(v)$ and $-x$ at $tout(v)$; then $a_u$ is a prefix sum up to $tin(u)$.
- **Subtree update, subtree query.** Both on ranges: a segment tree with [lazy propagation](/lazy-propagation/), or two Fenwick trees, gives [range update and range query](/range-update-range-query/) in $O(\log n)$.
- **Assignment and non-invertible aggregates.** Set every value of a subtree to $x$, or ask for the minimum of a subtree. The minimum has no inverse, so a Fenwick tree of prefix sums does not apply; a segment tree does.
- **Static values.** Without updates, prefix sums over $B$ answer each query in $O(1)$ after $O(n)$ time. Even simpler, one post-order pass computes all $n$ subtree sums at once.
- **Subtree with respect to another root.** For an unrooted tree, the "subtree of $v$ when the tree is rooted at $w$" is: the whole tree if $w = v$; the whole tree minus $\mathrm{sub}(c)$ if $w$ lies in $\mathrm{sub}(v) \setminus \{v\}$, where $c$ is the child of $v$ on the path to $w$; and $\mathrm{sub}(v)$ otherwise. The child $c$ is a [level ancestor](/level-ancestor-problem/) of $w$, found by [binary lifting](/binary-lifting/). So at most two range queries answer it.
- **Offline distinct-value or frequency questions.** "How many distinct colors are in $\mathrm{sub}(v)$" has no simple range-structure answer online; [DSU on tree](/dsu-on-tree/) answers all such questions offline in $O(n \log n)$ steps.

## Examples

The tree on $0, \ldots, 11$ rooted at 0 with the parent array $[-, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]$ and children in increasing order has the entry order $0, 1, 2, 3, 4, 5, 10, 6, 7, 11, 8, 9$. The tin and tout values are:

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $tin(v)$ | 0 | 1 | 2 | 3 | 4 | 5 | 7 | 8 | 10 | 11 | 6 | 9 |
| $tout(v)$ | 12 | 10 | 10 | 7 | 6 | 6 | 10 | 10 | 12 | 12 | 7 | 10 |
| $a_v$ | 3 | 1 | 4 | 1 | 5 | 9 | 2 | 6 | 5 | 3 | 5 | 8 |

The flat array is $B = [3, 1, 4, 1, 5, 9, 5, 2, 6, 8, 5, 3]$. The subtree sums of the vertices $0, \ldots, 11$ are $52, 41, 40, 20, 14, 9, 16, 14, 8, 3, 5, 8$.

A run of operations:

| operation | range of $B$ | answer |
|---|---|---|
| $\mathrm{query}(3)$ | $B[3 \ldots 6] = 1 + 5 + 9 + 5$ | 20 |
| $\mathrm{update}(10, 4)$ | $B[6] \gets 9$ | |
| $\mathrm{query}(3)$ | $1 + 5 + 9 + 9$ | 24 |
| $\mathrm{query}(2)$ | $B[2 \ldots 9]$ | 44 |
| $\mathrm{query}(8)$ | $B[10 \ldots 11] = 5 + 3$ | 8 |
| $\mathrm{query}(0)$ | $B[0 \ldots 11]$ | 56 |

Three small shapes. For one vertex, $\mathrm{query}(0) = a_0$. For a path $0 - 1 - \cdots - (n-1)$ rooted at 0, $tin(v) = v$ and $\mathrm{sub}(v) = \{v, \ldots, n-1\}$, so each query is a suffix sum; this is the partial sums problem itself. For a star rooted at its center 0, $\mathrm{query}(0)$ is the total and $\mathrm{query}(v) = a_v$ for each leaf.

## Known algorithms

| method | build | update | query |
|---|---|---|---|
| walk the subtree | $O(n)$ | $O(1)$ | $O(\vert \mathrm{sub}(v) \vert)$ |
| [Euler tour](/euler-tour-technique/) and [Fenwick tree](/fenwick-tree/) | $O(n)$ | $O(\log n)$ | $O(\log n)$ |
| Euler tour and [segment tree](/segment-tree/) | $O(n)$ | $O(\log n)$ | $O(\log n)$, any monoid |
| Euler tour and [lazy segment tree](/lazy-propagation/) | $O(n)$ | $O(\log n)$ for a subtree update | $O(\log n)$ |
| Euler tour and prefix sums (no updates) | $O(n)$ | | $O(1)$ |

The times are worst case in the word RAM, for a group operation of constant cost.

## Bounds

Upper bound: $O(\log n)$ per operation, by the table above.

Lower bound: on a path rooted at one end, a subtree is a suffix, so any structure for subtree queries solves the partial sums problem with the same costs (with $\mathrm{prefix}(i) = \mathrm{query}(0) - \mathrm{query}(i+1)$ for $i < n - 1$). Patrascu and Demaine prove that partial sums with $n$ elements needs $\Omega(\log n)$ time per operation in the cell-probe model with words of $\Theta(\log n)$ bits, amortized, for the maximum of the update and the query time. So the Euler tour with a Fenwick tree is optimal up to a constant factor.

## Reductions

- **Subtree queries to range queries.** The Euler tour maps the tree to an array in $O(n)$ time, subtree $v$ to the range $[tin(v), tout(v))$, so each subtree problem becomes the matching [range query problem](/range-query-problem/).
- **Partial sums to subtree queries.** A path rooted at one end, as in the lower bound.
- **Path queries.** A root-to-vertex path is not a range of the entry order, but it is a prefix of the bracket tour with $+a_v$ at the entry and $-a_v$ at the exit. A general path $u \to w$ needs the LCA as well; see [path queries on trees](/tree-path-queries/).

## Applications

- **Hierarchy totals.** Sums over departments, directories (the size of a directory is the sum of its file sizes), or categories, with updates.
- **Subtree counts.** "How many marked vertices are in the subtree of $v$" is a subtree sum of 0 and 1 values; [subtree sizes](/subtree-sizes/) are the case with all values 1.
- **Ancestor updates seen from below.** "Add $x$ to each vertex of $\mathrm{sub}(v)$, then read $a_u$" gives, for each $u$, the sum of the updates made at the ancestors of $u$.
- **Sub-steps of larger methods.** [Heavy-light decomposition](/heavy-light-decomposition/) uses an order that is an Euler tour order with heavy children first, so the same array also answers subtree queries.

## References
