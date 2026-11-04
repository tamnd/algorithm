---
tag: YPVPAT
kind: definition
slug: persistent-data-structure
name: Persistent data structure
aliases:
- persistent structure
- versioned data structure
area: data-structures/persistent-structures
level: intro
summary: A structure that keeps every earlier version alive and still queryable after updates.
prereqs: [ephemeral-data-structure, linked-list, binary-search-tree]
see_also: [partial-persistence, full-persistence, confluent-persistence, version-tree, path-copying, structural-sharing, purely-functional-data-structure, dsst-persistence-theorem]
sources:
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: Section 1 (the terms ephemeral, partially persistent and fully persistent, and the version tree)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 2, Persistence (Sections 2.1 Lists and 2.2 Binary Search Trees)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 13, Problem 13-1, Persistent dynamic sets
  - url: https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/
    title: Erik Demaine, MIT 6.851 Advanced Data Structures, Spring 2012
    locator: Lecture 1, Persistent data structures (partial, full and confluent persistence, and the functional model)
---

A persistent data structure is a data structure that keeps each earlier version after an update, so that a query can still read any old version. An ordinary [ephemeral data structure](/ephemeral-data-structure/) changes in place, and its old state is lost. Persistence has levels: [partial persistence](/partial-persistence/) lets you query every version and update only the newest, [full persistence](/full-persistence/) lets you update any version, and [confluent persistence](/confluent-persistence/) also lets an operation combine two versions. The usual tools are [path copying](/path-copying/), the [fat node](/fat-node/) method and [node copying](/node-copying/), all of which use [structural sharing](/structural-sharing/).

## Definition

Fix a data structure with a set of *query* operations, which return a value and change nothing, and a set of *update* operations, which change the state. A *version* is a state of the structure. The structure starts in version $v_0$. Number the updates $1, 2, \ldots, m$ in the order in which they are done. Update $i$ takes as input one version $v_{p(i)}$ with $p(i) < i$ (or two versions, in the confluent case) and produces the new version $v_i$. Each version $v_j$ has the value that we get when we apply, in order, the updates on the chain from $v_0$ to $v_j$.

The structure is

- **ephemeral** if only the newest version can be used: each update takes $v_{i-1}$, and after update $i$ no operation can use $v_0, \ldots, v_{i-1}$;
- **partially persistent** if a query can use any version $v_j$ with $0 \le j \le m$, but each update must take the newest version, so $p(i) = i - 1$ for each $i$;
- **fully persistent** if both queries and updates can use any version, so $p(i)$ can be any number in $\{0, \ldots, i-1\}$;
- **confluently persistent** if it is fully persistent and has, in addition, at least one update that takes two versions $v_a$ and $v_b$ and produces one new version from both (for example the concatenation of two lists);
- **functional** (or *purely functional*) if no field of a node changes after the node is made. A functional structure is fully persistent by construction, because no update can change the memory that an old version uses.

The versions with the relation "$v_i$ was made from $v_{p(i)}$" form the [version tree](/version-tree/). For partial persistence the tree is a path. For full persistence it is a rooted tree with $v_0$ at the root. For confluent persistence it is a directed acyclic graph.

The cost of persistence is the extra time per operation, and the extra space per update, compared with the ephemeral structure. A persistent structure has *constant overhead* if each operation takes $O(1)$ times the time of the ephemeral operation, and each update adds $O(1)$ space per memory cell that the ephemeral update changes.

## Examples and non-examples

**A persistent stack.** Store a [stack](/stack/) as a [linked list](/linked-list/) whose nodes never change. Push makes one new node that points to the old top, and pop returns the next node. Start with the empty stack $v_0$ and do push 1 on $v_0$ (giving $v_1 = [1]$), push 2 on $v_1$ (giving $v_2 = [2, 1]$), and push 3 on $v_1$ (giving $v_3 = [3, 1]$). The versions $v_2$ and $v_3$ share the node of 1. All four versions stay readable, and the version tree has $v_1$ with the two children $v_2$ and $v_3$. This is the [persistent stack](/persistent-stack/). It is functional, so it is fully persistent.

**A persistent search tree.** Insert into a [binary search tree](/binary-search-tree/) by copying the nodes on the path from the root to the new leaf, and keep the old root. The old root still sees the old tree, because no old node changed. For the keys 50, 30, 70, inserting 20 copies the nodes of 50 and 30 and makes one new leaf: three new nodes, while the node of 70 is shared. This is the [persistent binary search tree](/persistent-binary-search-tree/).

**A partially persistent array.** Keep, for each cell of an [array](/array/), a list of pairs (version number, value). A write appends a pair to the newest version; a read of cell $j$ in version $v$ finds the last pair of cell $j$ with a version number at most $v$. Each version can be read, but a write to an old version has no meaning, because it would change the history of all later versions. This is the [fat node](/fat-node/) method on an array.

**Non-example: an array with assignment.** The statement $A[3] \gets 7$ destroys the old value of $A[3]$. After it, no operation can read the earlier state. The array is ephemeral.

**Non-example: undo by rollback.** The [union-find with rollback](/union-find-with-rollback/) structure can return to an earlier state, but only by undoing the newest updates in reverse order, and the undone states are lost. At each moment only one version can be used. This is backtracking, not persistence.

**Non-example: a copy of the whole structure.** Copying all $n$ cells before each update keeps all versions, so it is persistent by the definition. It does not count as a good persistent structure, because each update costs $\Theta(n)$ time and space, while the ephemeral update costs $O(1)$. The definition says what is kept; the overhead says whether the method is useful.

**Partial but not full.** The fat node array above is partially persistent but not fully persistent. A write to version $v_2$ when $v_5$ exists would need a new branch of history, and one list of pairs per cell has no place for it.

## Related definitions

- [Ephemeral data structure](/ephemeral-data-structure/): the usual structure, with no old versions.
- [Partial persistence](/partial-persistence/), [full persistence](/full-persistence/) and [confluent persistence](/confluent-persistence/) are the three levels of the definition above.
- A [purely functional data structure](/purely-functional-data-structure/) is the functional case: persistence by never writing to an old cell.
- The [version tree](/version-tree/) records which version each update modified.
- [Path copying](/path-copying/), [fat node](/fat-node/) and [node copying](/node-copying/) are the general methods that turn an ephemeral linked structure into a persistent one. The [DSST persistence theorem](/dsst-persistence-theorem/) gives their cost for structures in which each node has a bounded number of incoming pointers.
- A [retroactive data structure](/retroactive-data-structure/) is a different idea: it changes an update in the past and lets the change act on all later versions, while persistence keeps the past fixed and branches.
- A [semi-persistent array](/semi-persistent-array/) is fast on the newest version and slower on old versions.

### History

Driscoll, Sarnak, Sleator and Tarjan gave the names ephemeral, partially persistent and fully persistent, and the general methods, in their paper of 1989 (a conference version appeared at STOC in 1986). Functional programmers used persistent lists and trees long before, because a value in a pure functional language never changes. Okasaki's book of 1998 collects the purely functional structures and their amortized analysis with lazy evaluation.

## References
