---
tag: GSRBN2
kind: abstract-type
slug: ordinal-tree
name: Ordinal tree
aliases:
- static ordered tree
area: data-structures/succinct-structures
level: advanced
summary: A static rooted ordered tree supporting navigation such as parent, child, sibling and subtree size.
prereqs: [rooted-tree]
see_also: [louds-tree, balanced-parentheses-representation, dfuds, range-min-max-tree, catalan-numbers, lowest-common-ancestor, level-ancestor-problem, left-child-right-sibling]
sources:
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 8 (Trees), the list of operations at its start, and Sections 8.1 (LOUDS), 8.2 (Balanced Parentheses) and 8.3 (DFUDS Representation)
  - paper: doi:10.1137/S0097539799364092
    title: J. Ian Munro and Venkatesh Raman, Succinct representation of balanced parentheses and static trees, SIAM Journal on Computing 31(3), 2001, 762-776
    locator: Section 1 (the count of ordinal trees and the 2n + o(n) bit target) and the operations supported on the parenthesis representation
  - paper: doi:10.1145/2601073
    title: Gonzalo Navarro and Kunihiko Sadakane, Fully functional static and dynamic succinct trees, ACM Transactions on Algorithms 10(3), Article 16, 2014
    locator: Table 1 (the full list of ordinal tree operations and their times in 2n + o(n) bits)
---

An ordinal tree is an abstract data type for a static rooted tree in which the children of each node are ordered, first, second, and so on, and the nodes carry no labels other than their position. It supports navigation: the root, the parent of a node, its $i$-th child, its next sibling, its degree, its depth, the size of its subtree, the [lowest common ancestor](/lowest-common-ancestor/) of two nodes, and the rank of a node in preorder or level order. There are $C_{n-1}$ ordinal trees with $n$ nodes, a [Catalan number](/catalan-numbers/), so any representation needs $2n - \Theta(\lg n)$ bits. [LOUDS](/louds-tree/), [balanced parentheses](/balanced-parentheses-representation/) and [DFUDS](/dfuds/) use $2n + o(n)$ bits and answer most operations in $O(1)$ time on the [word RAM](/word-ram/), against $\Theta(n \lg n)$ bits for pointers.

## In plain words

An ordinal tree is a family tree that never changes, where the order of the children matters: the first child, the second child, and so on. Each node is known only by where it sits in the tree.

You want to move around the tree: go up to the parent, go down to the third child, step to the next brother or sister, and ask how many nodes lie below a node or how deep it is. The type says what these moves return. A pointer-based tree answers them easily but uses a lot of memory. Bit-string formats store the same shape in about two bits for each node and still answer the moves quickly.

## Operations

Let $T$ be an ordinal tree with $n \ge 1$ nodes. A node is named by an identifier that depends on the implementation, usually its preorder rank or the position of one of its bits; the operations below take and return such identifiers. Depth counts edges, so the root has depth 0.

| operation | returns |
|---|---|
| `root()` | the root |
| `parent(x)` | the parent of $x$, or none for the root |
| `first_child(x)`, `last_child(x)` | the first or last child of $x$, or none for a leaf |
| `next_sibling(x)`, `prev_sibling(x)` | the next or previous child of the parent of $x$, or none |
| `child(x, i)` | the $i$-th child of $x$, for $1 \le i \le$ `degree(x)` |
| `degree(x)` | the number of children of $x$ |
| `child_rank(x)` | the $i$ with `child(parent(x), i)` $= x$ |
| `is_leaf(x)` | whether $x$ has no children |
| `depth(x)` | the number of edges from the root to $x$ |
| `subtree_size(x)` | the number of nodes in the subtree of $x$, including $x$ |
| `is_ancestor(x, y)` | whether $x$ is on the path from the root to $y$ |
| `lca(x, y)` | the deepest common ancestor of $x$ and $y$ |
| `level_ancestor(x, d)` | the ancestor of $x$ at depth `depth(x)` $- d$ |
| `pre_rank(x)`, `pre_select(k)` | the preorder number of $x$, from 0, and the node with number $k$ |
| `leaf_rank(x)`, `leaf_select(k)` | the number of leaves before $x$ in preorder, and the $k$-th leaf |

Some uses need only a part of this list. A trie needs `child` by a label, which is `child(x, i)` after a search among the labels, plus `parent`. A suffix tree needs `lca`, `depth`, `subtree_size` and `leaf_rank`.

**Example.** Take the tree with root $A$, whose children are $B$, $C$ and $D$ in this order; $B$ has the children $E$ and $F$, $D$ has the child $G$, and $G$ has the child $H$. Then $n = 8$, the preorder is $A, B, E, F, C, D, G, H$, and the level order is $A, B, C, D, E, F, G, H$.

- `parent(G)` $= D$, `first_child(A)` $= B$, `next_sibling(B)` $= C$, `child(A, 3)` $= D$, `degree(A)` $= 3$, `child_rank(C)` $= 2$.
- `depth(H)` $= 3$, `subtree_size(D)` $= 3$, `subtree_size(A)` $= 8$.
- `lca(E, F)` $= B$, `lca(E, H)` $= A$, `level_ancestor(H, 2)` $= D$, `is_ancestor(D, H)` is true.
- `pre_rank(G)` $= 6$, the leaves in preorder are $E$, $F$, $C$, $H$, and `leaf_rank(C)` $= 2$.

The three succinct encodings of this tree are $(\,(\,(\,)\,(\,)\,)\,(\,)\,(\,(\,(\,)\,)\,)\,)$ in [BP](/balanced-parentheses-representation/), $10\,1110\,110\,0\,10\,0\,0\,10\,0$ in [LOUDS](/louds-tree/), and $(\,(\,(\,(\,)\,(\,(\,)\,)\,)\,)\,(\,)\,(\,)\,)$ in [DFUDS](/dfuds/).

## Laws

For all nodes $x$, $y$ of $T$:

1. `parent(child(x, i))` $= x$ and `child_rank(child(x, i))` $= i$ for $1 \le i \le$ `degree(x)`.
2. `first_child(x)` $=$ `child(x, 1)` and `last_child(x)` $=$ `child(x, degree(x))` when `degree(x)` $\ge 1$; `next_sibling(child(x, i))` $=$ `child(x, i+1)` for $i <$ `degree(x)`.
3. `depth(root())` $= 0$ and `depth(child(x, i))` $=$ `depth(x)` $+ 1$.
4. `subtree_size(x)` $= 1 + \sum_{i=1}^{\text{degree}(x)}$ `subtree_size(child(x, i))`, and `subtree_size(root())` $= n$.
5. `is_ancestor(x, y)` holds if and only if `pre_rank(x)` $\le$ `pre_rank(y)` $<$ `pre_rank(x)` $+$ `subtree_size(x)`.
6. `lca(x, y)` is an ancestor of both, and no child of it is an ancestor of both; `lca(x, y)` $= x$ if and only if `is_ancestor(x, y)`.
7. `level_ancestor(x, 0)` $= x$ and `level_ancestor(x, d)` $=$ `parent(level_ancestor(x, d-1))` for $1 \le d \le$ `depth(x)`.
8. `pre_select(pre_rank(x))` $= x$, and `pre_rank(first_child(x))` $=$ `pre_rank(x)` $+ 1$.

## Implementations

| implementation | space in bits | $O(1)$ time | slower or missing |
|---|---|---|---|
| pointers to the first child, the next sibling and the parent, plus counters | $\Theta(n \lg n)$ | all but `lca` and `level_ancestor` | `child(x, i)` is $O(i)$ |
| [LOUDS](/louds-tree/) | $2n + o(n)$ | `parent`, `child(x, i)`, `degree`, siblings, level-order rank | `depth`, `subtree_size`, `lca` |
| [BP](/balanced-parentheses-representation/) with [parenthesis matching](/parenthesis-matching/) | $2n + o(n)$ | `parent`, `first_child`, siblings, `depth`, `subtree_size`, `is_ancestor`, preorder rank | `child(x, i)` and `degree` need extra structures |
| [DFUDS](/dfuds/) | $2n + o(n)$ | `parent`, `child(x, i)`, `degree`, `subtree_size`, `lca`, preorder rank | `depth` and `level_ancestor` need extra structures |
| BP with the [range min-max tree](/range-min-max-tree/) | $2n + O(n / \text{polylog}\, n)$ | the whole list | none |

The pointer tree is simple and allows updates, but its space is a factor $\Theta(\lg n)$ above the minimum. LOUDS is the simplest succinct encoding and the fastest for tries, which move only between parents and children. BP and DFUDS need [parenthesis matching](/parenthesis-matching/) and give the operations of a depth-first view. The range min-max tree of Navarro and Sadakane supports every operation of the list on BP in $O(1)$ time, or in $O(\lg n)$ time with a simple implementation.

## Lower bounds

**Space.** The number of ordinal trees with $n$ nodes is the Catalan number $C_{n-1} = \frac{1}{n} \binom{2n-2}{n-1}$: 1, 1, 2, 5, 14, 42 for $n = 1$ to 6, and 429 for $n = 8$. Since $\binom{2m}{m} = \Theta(4^m / \sqrt{m})$, $\lg C_{n-1} = 2n - \frac32 \lg n + O(1)$, and any representation needs at least this many bits for some tree, by the [information-theoretic bound](/information-theoretic-bound/). So $2n + o(n)$ bits is succinct, and a pointer tree is not even compact.

**Redundancy.** Navarro and Sadakane reach $2n + O(n / \text{polylog}\, n)$ bits with all operations in $O(1)$ time. For trees, as for bit vectors, the cell-probe trade-offs between the redundancy and the query time follow the pattern of [Pătraşcu's lower bounds](/patrascu-succinct-lower-bound/); the exact bounds for tree navigation are less well studied than those for rank.

## References
