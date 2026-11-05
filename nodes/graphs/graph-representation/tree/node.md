---
tag: PHJCS4
kind: abstract-type
slug: tree
name: Tree
aliases:
- rooted tree
- free tree
area: graphs/graph-representation
level: intro
summary: Connected acyclic graph, rooted or free, as an abstract type.
prereqs: [graph, undirected-graph, acyclic-graph]
see_also: [rooted-tree, parent-pointer-tree, left-child-right-sibling, binary-tree, spanning-tree, prufer-sequence, louds-tree, tree-traversal]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.5 (Trees), Theorem B.2 on the properties of free trees, and rooted, ordered, binary and positional trees; Section 10.3 (Representing rooted trees)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3 (Trees), the recursive definition of trees and forests; Section 2.3.2, the binary tree representation of trees; Section 2.3.3, other representations, including parent links; Section 2.3.4.1, free trees
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 8 (Trees), the information-theoretic lower bound for ordinal trees and the LOUDS, balanced parentheses and DFUDS representations
---

A tree is a connected [graph](/graph/) with no cycles. In its free form it is an [undirected graph](/undirected-graph/) in which each two [vertices](/vertex/) are joined by exactly one path. In its rooted form one vertex is the root, every other vertex has one parent, and the tree is a hierarchy: file systems, parse trees, organisation charts, search trees and the output of [breadth-first](/breadth-first-search/) and [depth-first search](/depth-first-search/) are rooted trees. As an abstract type, a rooted tree offers `parent`, `children` and `add-child`, and its representations, such as the [parent-pointer tree](/parent-pointer-tree/) and the [left-child right-sibling](/left-child-right-sibling/) form, differ in which of these are fast.

## In plain words

A family tree without marriages is a tree. Start with one person at the top. Each person has some children, and each person except the one at the top has exactly one parent. You can never go around in a circle by following parent links, and every person is linked to the person at the top.

The same shape appears when folders hold files and smaller folders, and when a company boss has managers who have workers. A program that works with such a shape asks a few questions. Who is the parent? Who are the children? Add a new child here. How fast each answer comes depends on what the program stores: a parent link for each person, a list of children for each person, or both.

## Operations

**Free trees.** A *free tree* is a simple undirected graph $T = (V, E)$ that is connected and has no cycle; a *forest* is a graph with no cycle, so each of its components is a tree. For a simple graph with $n \ge 1$ vertices and $m$ edges, the following are equivalent (CLRS Theorem B.2):

1. $T$ is connected and has no cycle.
2. Each two vertices are joined by exactly one simple path.
3. $T$ is connected, and removing any edge disconnects it.
4. $T$ is connected and $m = n - 1$.
5. $T$ has no cycle and $m = n - 1$.
6. $T$ has no cycle, and adding any edge makes a cycle.

So a free tree is a graph, and it uses the operations of the [graph](/graph/) type, with the law $m = n - 1$ and the extra query `path`$(u, v)$, the unique path. A tree with $n \ge 2$ vertices has at least two leaves, vertices of degree 1.

**Rooted trees.** A *rooted tree* is a free tree with one vertex $r$, the root. For each $v \ne r$, the first edge of the unique path from $v$ to $r$ goes to the *parent* $p(v)$ of $v$; $v$ is a *child* of $p(v)$. The *depth* of $v$ is the length of the path from $v$ to $r$. An *ordered* tree also fixes an order on the children of each vertex. Equivalently, a rooted tree is a set $V$ with a root $r$ and a parent map $p : V \setminus \{r\} \to V$ such that for each $v$ some iterate $p^k(v)$ is $r$. See [rooted tree](/rooted-tree/).

The operations on an ordered rooted tree, where $\text{NIL}$ means "no vertex":

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}() \to (T, r)$ | the tree with the one vertex $r$, its root |
| `root` | $\text{root}(T) \to v$ | the root |
| `parent` | $\text{parent}(T, v) \to v'$ or NIL | $p(v)$, or NIL for the root |
| `children` | $\text{children}(T, v) \to$ sequence | the children of $v$, in order, each once |
| `add-child` | $\text{add-child}(T, v) \to (c, T)$ | adds a new vertex $c$ as the last child of $v$, and returns it |
| `remove-leaf` | $\text{remove-leaf}(T, v) \to T$ | removes a vertex $v \ne r$ that has no children |
| `size` | $\text{size}(T) \to n$ | the number of vertices |

Derived queries are built from these: `depth`$(v)$ by following `parent` to the root, in $O(1 + \text{depth}(v))$ calls; `is-leaf`$(v)$ as "`children`$(v)$ is empty"; and the [traversals](/tree-traversal/) in [preorder](/preorder-traversal/), [postorder](/postorder-traversal/) and [level order](/level-order-traversal/), each with one `children` call for each vertex.

### Example

| step | operation | result | parent map after |
|---|---|---|---|
| 1 | new | $(T, a)$ | $\{\}$, root $a$ |
| 2 | add-child $a$ | $b$ | $b \mapsto a$ |
| 3 | add-child $a$ | $c$ | $b, c \mapsto a$ |
| 4 | add-child $b$ | $d$ | $b, c \mapsto a$; $d \mapsto b$ |
| 5 | children $a$ | $b, c$ | |
| 6 | parent $d$ | $b$ | |
| 7 | parent $a$ | NIL | |
| 8 | remove-leaf $c$ | | $b \mapsto a$; $d \mapsto b$ |
| 9 | size | 3 | |

The tree after step 4 has $n = 4$ vertices and the $3 = n - 1$ edges $ab$, $ac$, $bd$. The depth of $d$ is 2.

## Laws

For each tree $T$ built by these operations, with root $r$, and each vertex $v$ of $T$:

$$\begin{aligned}
&(\text{T1})\quad \text{parent}(T, \text{root}(T)) = \text{NIL}, \text{ and } \text{parent}(T, v) \ne \text{NIL} \text{ for } v \ne \text{root}(T),\\
&(\text{T2})\quad x \in \text{children}(T, v) \iff \text{parent}(T, x) = v,\\
&(\text{T3})\quad \text{if } (c, T') = \text{add-child}(T, v), \text{ then } \text{parent}(T', c) = v \text{ and } \text{children}(T', v) = \text{children}(T, v) \cdot c,\\
&(\text{T4})\quad \text{for each } v, \ \text{parent}^k(T, v) = \text{root}(T) \text{ for some } k \ge 0,\\
&(\text{T5})\quad \textstyle\sum_{v} |\text{children}(T, v)| = \text{size}(T) - 1.
\end{aligned}$$

Law (T2) ties the two directions together, so a representation that stores both must update both. Law (T4) says the parent links have no cycle and all lead to the root; it is what makes the graph connected and acyclic. Law (T5) is $m = n - 1$: each vertex except the root has exactly one edge to its parent. In (T3), $\cdot$ appends to the sequence; an unordered tree only needs $c$ to be added to the set of children.

## Implementations

Costs for a rooted tree with $n$ vertices, where $k$ is the number of children of $v$ and $i$ is the position of a child in the order. Vertices are the integers $0, \ldots, n - 1$, and "amortized" refers to [dynamic arrays](/dynamic-array/).

| structure | space | parent | children | $i$-th child | add-child | remove-leaf |
|---|---|---|---|---|---|---|
| [parent-pointer tree](/parent-pointer-tree/) (parent array) | $n$ words | $O(1)$ | $\Theta(n)$ scan | $\Theta(n)$ | $O(1)$ amortized | $O(1)$, by a deleted mark |
| child lists with a parent array | $\Theta(n)$ words | $O(1)$ | $\Theta(1 + k)$ | $O(1)$ | $O(1)$ amortized | $O(k)$ at the parent |
| [left-child right-sibling](/left-child-right-sibling/) with parent | $3n$ words | $O(1)$ | $\Theta(1 + k)$ | $O(i)$ | $O(1)$ at the front, $O(k)$ at the end | $O(k)$ at the parent |
| [binary tree](/binary-tree/) nodes (at most 2 children) | $3n$ words | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ |
| [LOUDS](/louds-tree/), static | $2n + o(n)$ bits | $O(1)$ | $O(1 + k)$ | $O(1)$ | rebuild | rebuild |
| [balanced parentheses](/balanced-parentheses/), static | $2n + o(n)$ bits | $O(1)$ | $O(1 + k)$ | $O(i)$ | rebuild | rebuild |

The parent array is the right choice when the algorithm only walks up, as in [disjoint-set forests](/disjoint-set-forest/) and in the predecessor arrays of search and shortest paths. Child lists suit top-down work such as traversals and tree dynamic programming. The LCRS form gives each vertex a fixed number of fields, whatever its number of children, and is the form of Knuth's binary tree representation of a forest. The succinct forms of [ordinal trees](/ordinal-tree/) are for large static trees.

A free tree on $\{0, \ldots, n - 1\}$ is usually stored as an [adjacency list](/adjacency-list/) with $2(n - 1)$ entries, and rooted on demand: one BFS or DFS from the chosen root computes the parent array in $\Theta(n)$ time.

## Lower bounds

**Space for ordered trees.** The number of ordered rooted trees with $n$ vertices is the [Catalan number](/catalan-numbers/) $C_{n-1} = \frac{1}{n}\binom{2n-2}{n-1}$. A representation that tells all of them apart needs $\lceil \lg C_{n-1} \rceil = 2n - \Theta(\log n)$ bits for some tree. The pointer forms use $\Theta(n \log n)$ bits, and LOUDS and balanced parentheses use $2n + o(n)$ bits, which is optimal up to the lower-order term.

**Space for labeled trees.** The number of free trees on the labeled vertex set $\{1, \ldots, n\}$ is $n^{n-2}$, by [Cayley's formula](/cayley-formula/), so some tree needs $(n - 2) \lg n$ bits. A parent array with $\lceil \lg n \rceil$-bit entries uses $n \lceil \lg n \rceil$ bits, and the [Prüfer sequence](/prufer-sequence/) uses $(n - 2)\lceil \lg n \rceil$, so both are optimal up to lower-order terms for labeled trees.

**Children from parents.** If the only access to the tree is `parent`, listing the children of $v$ needs $n - 1$ calls in the worst case. *Proof by adversary.* If some vertex $x \ne v$ was never asked, its parent can be $v$ or another vertex without changing any answer, and the two trees have different child sets for $v$. So a parent array must be scanned in full, and an algorithm that walks down should first build child lists, in $\Theta(n)$ time by [counting sort](/counting-sort/) on the parent values.

## References
