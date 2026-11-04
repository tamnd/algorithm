---
tag: TS4K3V
kind: definition
slug: partial-persistence
name: Partial persistence
aliases:
- partially persistent
area: data-structures/persistent-structures
level: intro
summary: Old versions can be queried but only the newest version can be updated.
prereqs: [ephemeral-data-structure, persistent-data-structure]
see_also: [full-persistence, confluent-persistence, fat-node, node-copying, path-copying, dsst-persistence-theorem, historical-queries, sarnak-tarjan-point-location]
sources:
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: pages 86 to 124, the introduction (the definition) and the section on partial persistence (the fat node and node-copying methods)
  - paper: doi:10.1145/6138.6151
    title: Neil Sarnak and Robert E. Tarjan, Planar point location using persistent search trees, Communications of the ACM 29(7), 1986
    locator: pages 669 to 679 (a partially persistent search tree with O(1) amortized space per update, applied to point location)
  - paper: doi:10.7146/brics.v1i35.21608
    title: Gerth Stølting Brodal, Partially persistent data structures of bounded degree with constant update time, BRICS Report Series RS-94-35, 1994
    locator: the main theorem (worst-case O(1) time and space per update for structures of bounded in-degree)
---

Partial persistence is the degree of [persistence](/persistent-data-structure/) in which every old version of a data structure stays available for queries, but only the newest version can be updated. The versions form a single sequence, ordered by time, so a partially persistent structure answers questions of the form "what was the state at time $t$". It is the weakest of the three degrees of persistence defined by Driscoll, Sarnak, Sleator and Tarjan, and it is the one that most geometric applications need.

## Definition

Let a data structure have queries, which do not change the state, and updates, which do. Start from a version $D_0$. A **partially persistent** structure supports:

- $\text{update}(u)$: apply the update $u$ to the newest version $D_m$, giving a new version $D_{m+1} = u(D_m)$, and make $D_{m+1}$ the newest version. The version $D_m$ is not changed.
- $\text{query}(i, q)$, for each $i$ with $0 \le i \le m$: answer the query $q$ with respect to version $D_i$.

The versions are numbered by the order of their creation, so the version graph is a path $D_0 \to D_1 \to \cdots \to D_m$. In contrast with an [ephemeral data structure](/ephemeral-data-structure/), a query may name any version. In contrast with [full persistence](/full-persistence/), an update may name only the newest version.

A method that turns an ephemeral structure into a partially persistent one has two costs:

- the **time slowdown** of a query step and of an update step, relative to the ephemeral structure;
- the **space** used for each update, counted in memory words or in node fields changed.

For a structure in the [pointer machine](/pointer-machine/) model, with nodes of constant size, these are the known bounds:

| method | time for each access step | time and space for each update step |
|---|---|---|
| copy the whole structure | $O(1)$ | $\Theta(n)$ |
| [fat node](/fat-node/) | $O(\log m)$ worst case | $O(1)$ worst case |
| [node copying](/node-copying/), in-degree at most a constant | $O(1)$ worst case | $O(1)$ amortized |
| Brodal (1994), in-degree at most a constant | $O(1)$ worst case | $O(1)$ worst case |

Here $n$ is the size of the structure and $m$ the number of updates so far. The node-copying bound is part of the [DSST persistence theorem](/dsst-persistence-theorem/).

## Examples and non-examples

- **A partially persistent array.** Keep, for each cell, the list of pairs (version, value) in the order of the writes. Start with all cells 0 and do the writes $A[3] \leftarrow 7$ (version 1), $A[5] \leftarrow 2$ (version 2), $A[3] \leftarrow 9$ (version 3). The list of cell 3 is $(0, 0), (1, 7), (3, 9)$. A read of $A[3]$ in version 2 finds, by [binary search](/binary-search/), the last pair with a version at most 2, which is $(1, 7)$, so the answer is 7. In version 3 the answer is 9 and in version 0 it is 0. A new write appends to the end of one list, because it always makes the newest version. This is the [fat node](/fat-node/) method on an array.
- **Planar point location.** Sarnak and Tarjan sweep a vertical line across a planar subdivision with $n$ edges. The edges that cross the line form a sorted set that changes at each vertex. A partially persistent [search tree](/persistent-binary-search-tree/) keeps all $O(n)$ versions in $O(n)$ space. A query point $(x, y)$ is located by a binary search on $x$ for the right version, then a search for $y$ in that version, in $O(\log n)$ time. See [Sarnak-Tarjan point location](/sarnak-tarjan-point-location/).
- **A text editor history that can be viewed but not branched.** If the user can look at any old state of the file but each edit applies to the newest state, the history is partially persistent.
- **Non-example: undo followed by an edit.** If the user goes back to state 3 of 10 and edits it, keeping states 4 to 10, the update was applied to an old version. The versions now form a tree, which needs [full persistence](/full-persistence/).
- **Non-example: an undo stack.** An [undo log](/undo-log/) that throws away the undone states is ephemeral: at each moment only the current state can be queried.
- **Non-example: changing the past.** An operation that inserts an update at time 3 and changes all later versions is [retroactive](/retroactive-data-structure/), not persistent. A persistent structure never changes an existing version.

## Related definitions

- [Persistent data structure](/persistent-data-structure/): the general notion.
- [Full persistence](/full-persistence/): every version can be updated, so the versions form a tree.
- [Confluent persistence](/confluent-persistence/): versions can also be combined, so they form a directed acyclic graph.
- [Semi-persistent array](/semi-persistent-array/): semi-persistence, in the sense of Conchon and Filliâtre, is a different restriction: an update may apply to the newest version or to one of its ancestors, and then the versions after that ancestor become invalid, as in backtracking.
- [Historical queries](/historical-queries/): the problems that partial persistence solves, such as a range count in an old version.
- [Fat node](/fat-node/) and [node copying](/node-copying/): the two general methods for partial persistence; [path copying](/path-copying/) also gives full persistence.

## References
