---
tag: W6Y5EV
kind: problem
slug: persistent-dynamic-set
name: Persistent dynamic sets
area: data-structures/persistent-structures
level: core
summary: Dynamic sets that keep every earlier version after an insertion or deletion, usually by copying only the nodes along a changed path.
prereqs: [ordered-set, binary-search-tree, persistent-data-structure, path-copying]
see_also: [persistent-binary-search-tree, persistent-red-black-tree, persistent-treap, version-tree, full-persistence, partial-persistence, sarnak-tarjan-point-location, node-copying]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 13, Problem 13-1, Persistent dynamic sets (path copying, its cost on a tree of height h, the effect of parent pointers, and the red-black solution)
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: the application to balanced search trees
  - paper: doi:10.1145/6138.6151
    title: Neil Sarnak and Robert E. Tarjan, Planar point location using persistent search trees, Communications of the ACM 29(7), 1986
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Section 2.2 (unbalanced sets with path copying) and Section 3.3 (red-black trees)
---

The persistent dynamic set problem asks for a [dynamic set](/ordered-set/) of keys in which each insertion or deletion makes a new version and keeps all the older versions, so that a query can still ask about any past version. The standard solution is a balanced search tree with [path copying](/path-copying/): each update copies the $O(\log n)$ nodes on one search path and shares the rest, which gives $O(\log n)$ time and space per update. Cormen, Leiserson, Rivest and Stein pose it as Problem 13-1 of their book, and Sarnak and Tarjan used it to solve [planar point location](/planar-point-location/).

## In plain words

You keep a set of numbers, and you change it by adding and removing numbers. But you also want to look back: "was 17 in the set three changes ago?" You might even want to go back to an old set and change it in a new way, so that the history splits into two branches.

Saving a full copy of the set after each change works, but it costs as much memory as the set for each change. The question is how to keep all the versions while each change costs only a little more than a normal change. The answer is to store the set as a tree and to copy only the few nodes that a change touches.

## Definition

**Universe.** Keys come from a set $U$ with a total order.

**Versions.** The version $V_0$ is the empty set. An *update* names an existing version $V_j$ and makes a new version:

- $\text{insert}(j, k)$ makes $V_i = V_j \cup \{k\}$;
- $\text{delete}(j, k)$ makes $V_i = V_j \setminus \{k\}$,

where $i$ is the number of updates done so far, so the versions are $V_0, V_1, \ldots, V_m$ after $m$ updates. A *query* names any existing version and does not make a version:

- $\text{search}(j, k)$ returns whether $k \in V_j$;
- for an ordered set, also $\text{minimum}(j)$, $\text{maximum}(j)$, $\text{successor}(j, k)$ (the least key of $V_j$ greater than $k$) and $\text{predecessor}(j, k)$.

**Input and output.** The input is a sequence of updates and queries, given online: each operation must be answered before the next one is seen. The output is the answer of each query.

**Cost.** Let $n = |V_j|$ for the version used by an operation. The goal is to answer each operation in time close to the time of an ephemeral balanced tree, $O(\log n)$, while the total space after $m$ updates is small: ideally $O(m)$, and $O(m \log n)$ is acceptable.

If every update must use the newest version ($j = i - 1$), the problem asks for [partial persistence](/partial-persistence/). If an update can use any version, it asks for [full persistence](/full-persistence/), and the versions form a [version tree](/version-tree/).

## Variants

- **Partial or full persistence.** Partial persistence is enough for most uses in geometry, where time moves in one direction. Full persistence is the natural model of a functional language.
- **Unordered sets.** If only search, insert and delete are needed, a persistent hash trie can replace the search tree, with the same path-copying idea. The order queries are then lost.
- **Maps.** Each key has a value; the version answers a lookup with the value. Every solution below stores the value in the node of the key.
- **Offline.** All operations are known in advance. Then one ephemeral structure with undo suffices, see the reductions below.
- **Confluent sets.** An update may also take the union of two versions. This needs [confluent persistence](/confluent-persistence/) and join-based trees.

## Examples

Start from $V_0 = \emptyset$ and run:

| step | operation | result | version |
|---|---|---|---|
| 1 | insert$(0, 5)$ | | $V_1 = \{5\}$ |
| 2 | insert$(1, 3)$ | | $V_2 = \{3, 5\}$ |
| 3 | insert$(1, 8)$ | | $V_3 = \{5, 8\}$ |
| 4 | delete$(2, 5)$ | | $V_4 = \{3\}$ |
| 5 | search$(2, 5)$ | true | |
| 6 | search$(4, 5)$ | false | |
| 7 | search$(3, 3)$ | false | |
| 8 | successor$(2, 3)$ | 5 | |
| 9 | minimum$(3)$ | 5 | |

Step 3 updates $V_1$, not the newest version $V_2$, so this sequence needs full persistence. The versions form a tree: $V_1$ has the children $V_2$ and $V_3$, and $V_2$ has the child $V_4$.

**Path copying on the example.** With an unbalanced search tree, step 2 copies the node of 5 and adds a leaf 3 (2 new nodes); step 3 copies the node of 5 again and adds a leaf 8 (2 new nodes); step 4 deletes the root 5 of $V_2$, whose only child is 3, so the new version is the old leaf 3 itself (0 new nodes). The five versions hold $0 + 1 + 2 + 2 + 1 = 6$ keys in total and use $1 + 2 + 2 + 0 = 5$ nodes. The gain grows with the size of the set: on a balanced tree of $n$ keys an update makes $O(\log n)$ nodes instead of $n$.

## Known algorithms

- **Full copy.** Copy the set before each update. Each update takes $\Theta(n)$ time and space. This is the baseline.
- **[Persistent binary search tree](/persistent-binary-search-tree/).** An unbalanced search tree with path copying. Each operation on a version of height $h$ takes $\Theta(h)$ time, and each update makes at most $h + 1$ nodes. The height can be $n$.
- **[Persistent red-black tree](/persistent-red-black-tree/).** Path copying on a red-black tree, with a rebalancing step that touches only nodes on or next to the search path. Each operation takes $O(\log n)$ time in the worst case, and each update makes $O(\log n)$ nodes. This is the answer to part (e) of CLRS Problem 13-1.
- **[Persistent treap](/persistent-treap/).** Path copying on a treap: $O(\log n)$ expected time and space per operation.
- **[Node copying](/node-copying/) and fat nodes.** Driscoll, Sarnak, Sleator and Tarjan made balanced search trees persistent with $O(\log n)$ time per operation and $O(1)$ amortized space per update. The method writes into old nodes with version stamps instead of copying whole paths. For partial persistence this is the method that Sarnak and Tarjan used for point location.

## Bounds

**Search.** In the [comparison model](/comparison-model/), a search in a set of $n$ keys needs $\lceil \lg(n + 1) \rceil$ comparisons in the worst case, because the $n + 1$ gaps between and around the keys must all be told apart by a binary decision tree. A persistent set includes an ephemeral one (use only the newest version), so the same bound holds. The balanced solutions meet it up to a constant factor.

**Space.** Each update must record its change, so $m$ updates need $\Omega(m)$ space in total in the worst case. Node copying meets this bound up to a constant factor; path copying uses $\Theta(\log n)$ per update on a balanced tree, which is more by a factor of $\log n$.

**Path copying with parent pointers.** Suppose each node also has a pointer to its parent, and an insertion adds a new leaf. The parent of the leaf gets a new child field, so it must be a new node, and so must each node above it, up to the root. A node of the new version whose parent is a new node must itself be new, because its parent field differs from the one in the old version. The root is new, so by induction from the root down, every node of the new version is new, and an update costs $\Omega(n)$ time and space. This is part (d) of CLRS Problem 13-1. The persistent solutions avoid parent pointers and keep the search path on a stack instead.

## Reductions

- **From the ephemeral problem.** An ephemeral dynamic set is the special case in which each operation uses the newest version. So each lower bound for the ephemeral set also holds here.
- **Offline persistence to undo.** If all operations are known in advance, build the [version tree](/version-tree/), and walk it by depth-first search with one ephemeral balanced tree. On the way down an edge, apply its update and record what it changed; on the way back, undo the change. Each query is answered when the walk is at its version. The total time is $O(m \log n)$ with $O(n)$ space at any moment. This is the same idea as [union-find with rollback](/union-find-with-rollback/).
- **Planar point location to partial persistence.** Sweep a vertical line over a planar subdivision with $N$ edges. The edges that cross the line form a sorted set, which changes by $O(N)$ insertions and deletions in total. A partially persistent sorted set stores all these sets. A query point $(x, y)$ then finds the version for $x$ by a binary search on the event coordinates, and the edge just below $y$ by a successor query in that version. With node copying this gives $O(\log N)$ query time and $O(N)$ space; see [Sarnak-Tarjan point location](/sarnak-tarjan-point-location/).

## Applications

- **Computational geometry.** Sweep line algorithms whose later queries need the sweep status at any earlier position, such as point location.
- **Functional programming.** Sets and maps in Haskell, OCaml, Scala and Clojure are persistent balanced trees or tries, because a value never changes.
- **Snapshots.** A database or a file system index that must keep consistent snapshots for long reads while writes go on.
- **Search and backtracking.** A search over states that each hold a set (for example, the set of visited cells) can keep each state cheaply and return to any of them.

## References
