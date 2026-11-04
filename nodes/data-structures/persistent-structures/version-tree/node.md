---
tag: Z1SJQJ
kind: concept
slug: version-tree
name: Version tree
aliases:
- version graph
- version history
area: data-structures/persistent-structures
level: core
summary: The tree of versions in which each update creates a child of the version it modified.
prereqs: [persistent-data-structure, rooted-tree]
see_also: [full-persistence, partial-persistence, confluent-persistence, fat-node, dsst-persistence-theorem, semi-persistent-array, offline-algorithm, version-vectors]
sources:
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: the definitions of partial and full persistence by the version graph, and the version list used by the fat node and node-splitting methods for full persistence
  - url: https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/
    title: Erik Demaine, MIT 6.851 Advanced Data Structures, Spring 2012
    locator: Lecture 1, Persistent data structures (the version tree, its linearization, and order maintenance)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 5 and Chapter 6 (why reuse of a version breaks amortized bounds)
---

The version tree of a [persistent data structure](/persistent-data-structure/) is the rooted tree whose nodes are the versions and in which each update adds a child to the version it was applied to. The initial version is the root. The shape of this graph is what tells the kinds of persistence apart: under [partial persistence](/partial-persistence/) it is a path, under [full persistence](/full-persistence/) it is a [rooted tree](/rooted-tree/), and under [confluent persistence](/confluent-persistence/) it is a [directed acyclic graph](/directed-acyclic-graph/). Driscoll, Sarnak, Sleator and Tarjan defined persistence in these terms, and their methods for full persistence work on a linear order of the version tree.

## In plain words

Each time you change a persistent structure, you get a new version and you keep the old one. Write down each version as a dot, and draw a line from the version you changed to the version you got. The drawing is the version tree.

If you always change the newest version, the dots form one line, like a history with no branches. If you can go back and change an old version, the line splits into branches, like a family tree. If you can also combine two versions into one, two lines can meet, and the drawing is no longer a tree.

The value of a version is what you get by starting from the first version and doing the updates on the way down to it, in order.

## The idea

**Definition.** Let $V_0$ be the initial version. An update $u$ applied to an existing version $V_j$ makes a new version $V_i = u(V_j)$, where $i$ is the count of updates so far. The version tree has the versions $V_0, \ldots, V_m$ as nodes and the edges $V_j \to V_i$, one per update, labeled with $u$. Each version except $V_0$ has exactly one parent, so the graph is a tree with $m + 1$ nodes and $m$ edges. A query reads a version and adds nothing to the tree.

**The value of a version.** Let $V_0 = W_0, W_1, \ldots, W_d = V$ be the path from the root to $V$, and let $u_k$ be the label of the edge $W_{k-1} \to W_k$. Then $V = u_d(\cdots u_2(u_1(V_0)) \cdots)$. Two versions see the same sequence of updates up to their [lowest common ancestor](/lowest-common-ancestor/) and different ones after it. The depth $d$ of $V$ is the count of updates in its history; it can be much less than $m$.

**Shapes by kind of persistence.**

- *Ephemeral.* Only the newest version exists, and each update destroys it. There is no tree to keep.
- *Partial.* Only the newest version can be updated, so each new version is a child of the one before it, and the tree is a path $V_0 \to V_1 \to \cdots \to V_m$. Versions are ordered by time, and a version can be named by its index.
- *Full.* Any version can be updated, so the tree can branch. There is no longer one time line; two versions may be on different branches.
- *Confluent.* An update may take two or more versions, such as the concatenation of two lists, and then the new version has more than one parent. The graph is a DAG. Its size can grow fast: concatenating a list of length $1$ with itself $m$ times gives a version of length $2^m$ after $m$ updates.
- *Semi-persistent.* Any version can be updated, but only versions on the path from the root to the newest version can be used later, so the live part of the tree is a path that can grow and shrink at its end, like a stack. The [semi-persistent array](/semi-persistent-array/) uses this.

**Linearizing the tree.** Methods for full persistence need to know, for a field and a version $v$, which ancestor of $v$ last wrote the field. The [fat node](/fat-node/) method answers this with a total order on versions. Keep a list of versions in which each new version $i$ is put right after its parent, followed by an end marker $i^+$. Each later descendant of $i$ is put after $i$ and before $i^+$, so the subtree of $i$ is the interval from $i$ to $i^+$ in the list. When version $i$ writes value $x$ into a field whose value in $i$ was $y$, store $x$ at $i$ and $y$ at $i^+$. The value of the field in version $v$ is then the entry stored at the last list position at or before $v$. An order-maintenance structure supports insertion into the list and comparison of two positions in $O(1)$ time, which is what the method of Driscoll, Sarnak, Sleator and Tarjan uses.

**Why amortization fails.** An [amortized](/amortized-cost/) analysis assigns credit to a version and spends it once. In a version tree, a version with many children has each of its children spend the same credit. So a bound that holds on a path can fail on a tree. This is why many persistent structures have worst-case bounds, or use lazy evaluation with memoization so that work in a shared ancestor is done once.

**Offline walks.** If all operations are known in advance, the version tree can be built first. A depth-first walk with one ephemeral structure then applies the update of each edge on the way down and undoes it on the way up, and answers the queries of each version when the walk is at it. This turns full persistence into an ephemeral structure with undo, as in [union-find with rollback](/union-find-with-rollback/) and other [offline algorithms](/offline-algorithm/).

## Examples

**A small tree.** Start with $V_0$ in which a field $x$ is $0$, and do:

| update | applied to | effect | new version |
|---|---|---|---|
| 1 | $V_0$ | $x \gets 1$ | $V_1$ |
| 2 | $V_1$ | $x \gets 2$ | $V_2$ |
| 3 | $V_1$ | $y \gets 5$ | $V_3$ |
| 4 | $V_0$ | $x \gets 4$ | $V_4$ |
| 5 | $V_3$ | $y \gets 6$ | $V_5$ |

The tree has root $V_0$ with children $V_1$ and $V_4$; $V_1$ has children $V_2$ and $V_3$; $V_3$ has the child $V_5$. In $V_5$, the path from the root is $V_0, V_1, V_3, V_5$, and the last write of $x$ on it is in $V_1$, so $x = 1$ in $V_5$. Updates 2 and 4 are not on this path and do not affect $V_5$.

**The version list for the same tree.** Insert each new version right after its parent, followed by its end marker:

- after update 1: $V_0, V_1, V_1^+$;
- after update 2: $V_0, V_1, V_2, V_2^+, V_1^+$;
- after update 3: $V_0, V_1, V_3, V_3^+, V_2, V_2^+, V_1^+$;
- after update 4: $V_0, V_4, V_4^+, V_1, V_3, V_3^+, V_2, V_2^+, V_1^+$;
- after update 5: $V_0, V_4, V_4^+, V_1, V_3, V_5, V_5^+, V_3^+, V_2, V_2^+, V_1^+$.

The entries for $x$ are $0$ at $V_0$, $1$ at $V_1$ and $0$ at $V_1^+$, $2$ at $V_2$ and $1$ at $V_2^+$, $4$ at $V_4$ and $0$ at $V_4^+$. For $V_5$, the entries at or before its position are at $V_0, V_4, V_4^+, V_1$, and the last one is $1$ at $V_1$. For $V_2$, the last one is $2$ at $V_2$.

**A partial history.** A text editor that keeps an undo history, and in which a new edit after an undo discards the redo branch, keeps a path: each edit is a child of the current version and the branch beyond it is lost. An editor that keeps the discarded branches, so that the user can go to any earlier state and edit from there, keeps a full version tree.

**A confluent history.** In a version control system, a commit with two parents (a merge) joins two branches. The history of commits is a DAG, and each commit is a version of the file tree.

## Where it is used

- To define [partial](/partial-persistence/), [full](/full-persistence/) and [confluent](/confluent-persistence/) persistence, and the bounds of the [DSST persistence theorem](/dsst-persistence-theorem/).
- In the [fat node](/fat-node/) and node-splitting methods for full persistence, which order the versions by the version list above.
- In [Baker's trick](/bakers-trick/) and the [semi-persistent array](/semi-persistent-array/), where the cost of moving from one version to another is the distance between them in the version tree.
- In offline algorithms that walk the version tree with undo, such as [offline dynamic connectivity](/offline-dynamic-connectivity/) and queries on many versions of a [union-find](/union-find-with-rollback/) structure.
- In version control and in [version vectors](/version-vectors/) of distributed systems, where the history of states is a DAG.

## References
