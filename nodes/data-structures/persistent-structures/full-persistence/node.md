---
tag: P23E4B
kind: definition
slug: full-persistence
name: Full persistence
aliases:
- fully persistent
area: data-structures/persistent-structures
level: intro
summary: Every version can be both queried and updated, which creates a version tree.
prereqs: [partial-persistence]
see_also: [confluent-persistence, version-tree, path-copying, node-copying, fat-node, dsst-persistence-theorem, fully-persistent-array, bakers-trick]
sources:
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: pages 86 to 124, the introduction (the definition and the version tree) and the section on full persistence (the version list, fat nodes with full persistence, node splitting)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 2, Persistence (Section 2.1, Lists, and Section 2.2, Binary Search Trees, with path copying)
  - paper: doi:10.1007/3-540-51542-9_8
    title: Paul F. Dietz, Fully persistent arrays, Algorithms and Data Structures (WADS 1989), Lecture Notes in Computer Science 382
    locator: pages 67 to 74 (a fully persistent array with O(log log m) time per access)
---

Full persistence is the degree of [persistence](/persistent-data-structure/) in which every version of a data structure, old or new, can be both queried and updated. An update of an old version creates a new version and leaves all others unchanged, so the versions form a tree, the [version tree](/version-tree/). It is stronger than [partial persistence](/partial-persistence/), where only the newest version can be updated, and weaker than [confluent persistence](/confluent-persistence/), where two versions can also be combined into one.

## Definition

Let a data structure have queries, which do not change the state, and updates, which do. Start from a version $D_0$. After $m$ updates the structure holds versions $D_0, D_1, \ldots, D_m$, numbered by the order of their creation. A **fully persistent** structure supports:

- $\text{update}(i, u)$, for each $i$ with $0 \le i \le m$: apply the update $u$ to version $D_i$, giving a new version $D_{m+1} = u(D_i)$. No existing version is changed.
- $\text{query}(i, q)$, for each $i$ with $0 \le i \le m$: answer the query $q$ with respect to $D_i$.

The **version tree** has a node for each version and an edge from $D_i$ to $D_j$ when $D_j$ was made by an update of $D_i$. Each version except $D_0$ has exactly one parent, so this graph is a tree with root $D_0$. The version $D_j$ is equal to the result of the updates on the path from the root to $D_j$, applied in order to $D_0$. In the partially persistent case, the tree is a path.

Two orders on the versions matter in implementations. The *creation order* is $0, 1, \ldots, m$. The *tree order* is a preorder of the version tree. Methods such as the [fat node](/fat-node/) method for full persistence keep the versions in a list in tree order, and compare two versions with an order-maintenance structure in $O(1)$ time, because the creation order does not tell whether one version is an ancestor of another.

These are the known general costs for a structure in the [pointer machine](/pointer-machine/) model with nodes of constant size, where $m$ is the number of versions:

| method | time for each access step | time and space for each update step |
|---|---|---|
| copy the whole structure | $O(1)$ | $\Theta(n)$ |
| [path copying](/path-copying/) on a tree | $O(1)$ | $O(1)$ for each node on the path to the change |
| [fat node](/fat-node/) with a version list | $O(\log m)$ worst case | $O(\log m)$ time, $O(1)$ space |
| node splitting, in-degree at most a constant | $O(1)$ worst case | $O(1)$ amortized |

The last line is the full-persistence part of the [DSST persistence theorem](/dsst-persistence-theorem/). For an [array](/array/), no constant-time solution exists: the [fully persistent array](/fully-persistent-array/) of Dietz takes $O(\log \log m)$ time for each access, and a matching lower bound holds in the cell-probe model.

## Examples and non-examples

- **A version tree of sets.** Start with the empty set $D_0$. Let $D_1 = D_0 \cup \{5\}$, $D_2 = D_1 \cup \{3\}$, $D_3 = D_1 \cup \{8\}$ and $D_4 = D_2 \setminus \{5\}$. Version 3 is made from version 1, not from the newest version 2, so the structure must be fully persistent. The versions are $D_1 = \{5\}$, $D_2 = \{3, 5\}$, $D_3 = \{5, 8\}$ and $D_4 = \{3\}$. The version tree has the edges $0 \to 1$, $1 \to 2$, $1 \to 3$ and $2 \to 4$. A preorder that visits children in creation order is $0, 1, 2, 4, 3$, which differs from the creation order $0, 1, 2, 3, 4$.
- **A persistent search tree by path copying.** Insert into a [binary search tree](/binary-search-tree/) by copying the nodes on the search path and sharing the rest. Any old root can be the start of a new insertion, so the structure is fully persistent. See [path copying](/path-copying/) and [persistent binary search tree](/persistent-binary-search-tree/).
- **Lists in a functional language.** In ML or Haskell, `x :: xs` and `y :: xs` are two new lists that share the old list `xs`, and both can be extended further. Every structure built from immutable values is fully persistent, as Okasaki's Chapter 2 explains.
- **Undo and a new edit.** An editor that keeps every state and lets the user edit any old state builds a version tree. Each edit of an old state starts a new branch.
- **Non-example: merging two branches.** An operation that takes two versions and makes one, such as the concatenation of two lists or the merge of two branches in version control, has two parents. The version graph is then not a tree. This needs [confluent persistence](/confluent-persistence/).
- **Non-example: a partially persistent structure.** The fat node array of [partial persistence](/partial-persistence/) appends each new write to the end of the list of a cell. With an update of an old version, the new value does not belong at the end of the list in creation order, and a binary search by version number gives wrong answers. Full persistence needs the tree order, not the creation order.

## Related definitions

- [Partial persistence](/partial-persistence/): only the newest version can be updated.
- [Confluent persistence](/confluent-persistence/): versions can be combined, so the version graph is a directed acyclic graph.
- [Version tree](/version-tree/): the tree of versions of a fully persistent structure.
- [Ephemeral data structure](/ephemeral-data-structure/): only the current version exists.
- [Path copying](/path-copying/), [fat node](/fat-node/), [node copying](/node-copying/) and [Baker's trick](/bakers-trick/): ways to get full persistence.
- [Fully persistent array](/fully-persistent-array/): the array case, with its log-log bounds.

## References
