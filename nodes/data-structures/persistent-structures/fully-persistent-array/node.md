---
tag: MX556Y
kind: data-structure
slug: fully-persistent-array
name: Fully persistent array
aliases:
- Dietz persistent array
- persistent array
area: data-structures/persistent-structures
level: research
summary: An array whose every version supports reads and writes, with bounds in the log-log or log factors.
model: pointer-machine
complexity:
  vars: {n: the length of the array, m: the number of versions}
  time: {worst: O(log n)}
  space: {extra: O(n + m log n)}
history:
  year: 1989
  people: [Paul F. Dietz]
  note: Dietz gave a fully persistent array with O(log log m) time per access at WADS 1989, by storing each cell as a fat node and searching it in the preorder of the version tree.
prereqs: [array, full-persistence, path-copying]
see_also: [fat-node, bakers-trick, persistent-vector, persistent-segment-tree, persistent-union-find, version-tree, predecessor-problem, dsst-persistence-theorem]
sources:
  - paper: doi:10.1007/3-540-51542-9_8
    title: Paul F. Dietz, Fully persistent arrays, Algorithms and Data Structures (WADS 1989), Lecture Notes in Computer Science 382
    locator: pages 67 to 74 (fat cells, the version tree kept in preorder, and the O(log log m) access by searching among the writes to a cell)
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: pages 86 to 124, the section on full persistence (the version list and fat nodes; why bounded in-degree is needed for O(1) overhead, which an array does not have)
  - paper: doi:10.1145/1292535.1292541
    title: Sylvain Conchon and Jean-Christophe Filliâtre, A persistent union-find data structure, ACM SIGPLAN Workshop on ML, 2007
    locator: the section on persistent arrays (Baker's rerooting arrays, used as the base of a persistent union-find)
  - paper: doi:10.1145/359545.359566
    title: Henry G. Baker, Shallow binding in Lisp 1.5, Communications of the ACM 21(7), 1978
    locator: pages 565 to 569 (rerooting a tree of bindings, the idea behind Baker's trick for arrays)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 2, Persistence (path copying on binary trees) and Chapter 9, Numerical Representations (random-access lists as functional arrays)
---

A fully persistent array is an [array](/array/) of fixed length $n$ in which every version can be read and written. A write to any version, old or new, creates a new version and leaves all others unchanged, so the versions form a [version tree](/version-tree/), as in [full persistence](/full-persistence/). The simplest good implementation stores the array in a balanced binary tree and writes by [path copying](/path-copying/), with $O(\log n)$ time per read and per write. Dietz showed that $O(\log \log m)$ time per access is possible, where $m$ is the number of versions, by keeping each cell as a [fat node](/fat-node/) and searching it in the order of the version tree. [Baker's trick](/bakers-trick/) gives $O(1)$ time for the version in use, which is ideal when old versions are seldom touched. General methods with constant overhead, such as node copying, do not apply, because an array cell can be reached by index from every version.

## In plain words

Picture a row of numbered boxes that many people share, and each person wants their own copy to change. Copying the whole row for every change is slow. Instead, arrange the boxes as the leaves of a tree: one top node, split in two, then in two again, down to single boxes. To read a box, follow its number down the tree.

To change a box for one person, make new copies of only the nodes on the way down to that box. The new top node leads to the changed row. Every node off that path is shared with the old row, which stays as it was. So each change copies only a few nodes, about as many as the number of times you can halve the row.

## The abstract type

The structure holds versions $A_0, A_1, \ldots, A_{m-1}$, each a sequence of $n$ values, numbered in order of creation. $A_0$ is given at the start.

- `get(t, i)` returns $A_t[i]$, for $0 \le t < m$ and $0 \le i < n$.
- `set(t, i, x)` creates the version $A_m$, equal to $A_t$ except that $A_m[i] = x$, and returns its number $m$. Version $A_t$ is unchanged, and $t$ may be any existing version.

The version tree has an edge from $t$ to the new version for each `set`. With `set` only on the newest version, the structure is [partially persistent](/partial-persistence/).

## Representation

The array of length $n \ge 1$ is a complete-shape binary tree over the index range $[0, n)$. A node for a range $[lo, hi)$ with $hi - lo \ge 2$ has a left child for $[lo, mid)$ and a right child for $[mid, hi)$, where $mid = \lfloor (lo + hi)/2 \rfloor$. A node for a range of one index $[i, i + 1)$ is a leaf that holds a value. The tree for $[0, n)$ has $n$ leaves, $2n - 1$ nodes and height $\lceil \lg n \rceil$.

The structure keeps an array $\text{roots}$ of the roots of all versions. Nodes are never changed after they are built, and different versions share all the nodes they have in common.

**Invariant.** For every version $t$ and every index $i$, the path from $\text{roots}[t]$ chosen by $i$ ends at a leaf whose value is $A_t[i]$.

## Operations

BUILD$(a, 0, n)$ makes the root of version 0. The index ranges are not stored: GET and SET compute them on the way down.

```pseudo id=main
BUILD(a, lo, hi)
L1  if hi − lo = 1 then return LEAF(a[lo])
L2  mid ← ⌊(lo + hi) / 2⌋
L3  return NODE(BUILD(a, lo, mid), BUILD(a, mid, hi))

GET(v, i)                                ▷ v = roots[t]
L4  lo ← 0; hi ← n
L5  while hi − lo > 1 do
L6      mid ← ⌊(lo + hi) / 2⌋
L7      if i < mid then (v, hi) ← (left(v), mid) else (v, lo) ← (right(v), mid)
L8  return value(v)

SET(v, lo, hi, i, x)                     ▷ returns the root of a new tree
L9  if hi − lo = 1 then return LEAF(x)
L10 mid ← ⌊(lo + hi) / 2⌋
L11 if i < mid then return NODE(SET(left(v), lo, mid, i, x), right(v))
L12 return NODE(left(v), SET(right(v), mid, hi, i, x))

UPDATE(t, i, x)
L13 append SET(roots[t], 0, n, i, x) to roots; return the index of the new root
```

GET is a plain descent. SET builds a new leaf (line L9) and a new node for each range on the path above it (lines L11 and L12), and each new node points to the old child on the other side. UPDATE stores the new root, so the new version gets the next number.

## Example

Let $A_0 = [10, 20, 30, 40]$. Its tree has a root $R$ for $[0, 4)$, nodes $P$ for $[0, 2)$ and $Q$ for $[2, 4)$, and four leaves: 7 nodes.

| version | operation | new nodes | shared with older versions |
|---|---|---|---|
| 1 | set(0, 2, 33) | root $R_1$, $Q_1$ for $[2, 4)$, leaf 33 | $P$ and leaf 40 |
| 2 | set(0, 0, 11) | root $R_2$, $P_2$ for $[0, 2)$, leaf 11 | leaf 20 and $Q$ |
| 3 | set(1, 3, 44) | root $R_3$, $Q_3$ for $[2, 4)$, leaf 44 | $P$ and leaf 33 |

The versions are $A_1 = [10, 20, 33, 40]$, $A_2 = [11, 20, 30, 40]$ and $A_3 = [10, 20, 33, 44]$. Version 2 is made from version 0, not from the newest one, so the version tree has two branches below version 0. Memory holds $7 + 3 \cdot 3 = 16$ nodes, against $4 \cdot 7 = 28$ for four separate trees. GET$(3, 2)$ goes from $R_3$ right to $Q_3$ and left to the shared leaf 33, and GET$(2, 2)$ goes from $R_2$ right to the old node $Q$ and left to 30.

## Correctness

BUILD makes, by induction on $hi - lo$, a tree whose leaves hold $a[lo], \ldots, a[hi - 1]$ in order, so the invariant holds for version 0. GET keeps $i \in [lo, hi)$ and $v$ the node of $[lo, hi)$ on the path for $i$, so it ends at the leaf of $[i, i + 1)$. SET returns, by induction on $hi - lo$, a tree for $[lo, hi)$ whose leaf for $i$ holds $x$ and whose leaf for every $j \ne i$ is the leaf of $v$ for $j$: the side that does not contain $i$ is the old child itself. No line changes a node that exists, so every old version keeps its values. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| method | get | set | space after $m$ versions |
|---|---|---|---|
| copy the whole array | $O(1)$ | $\Theta(n)$ | $\Theta(nm)$ |
| path copying, this page | $O(\log n)$ worst case | $O(\log n)$ worst case | $O(n + m \log n)$ |
| [fat node](/fat-node/) with a search tree per cell | $O(\log m)$ | $O(\log m)$ | $O(n + m)$ |
| Dietz | $O(\log \log m)$ | $O(\log \log m)$ | $O(n + m)$ |
| [Baker's trick](/bakers-trick/) | $O(1)$ for the current version; $O(d)$ to switch to a version at distance $d$ in the version tree | same | $O(n + m)$ |

**Path copying.** The tree has height $\lceil \lg n \rceil$, so GET makes $O(\log n)$ steps, and SET builds $\lceil \lg n \rceil + 1$ nodes or fewer, each of size $O(1)$. The space bound follows by adding the $2n - 1$ nodes of version 0. The bounds are worst case and hold for any pattern of use of the versions, because no work is deferred.

**Dietz's structure.** Each cell keeps the list of its writes, one for each version that wrote it. A version $t$ reads, for cell $i$, the write made at the nearest ancestor of $t$ in the version tree that wrote cell $i$. Dietz keeps the version tree in preorder, so that the versions below a version form an interval, and reduces the read to a predecessor search among the writes to cell $i$ in this order, with markers at the ends of each interval. With a van Emde Boas style search structure on the positions of the versions, each search takes $O(\log \log m)$ time. In the original paper, this bound is amortized and expected, because of hashing and the upkeep of the preorder labels.

**Why not $O(1)$.** A read in a fully persistent array must find, among the writes to one cell, the one made at the nearest ancestor of a version, which is a search of the same kind as a [predecessor search](/predecessor-problem/). Lower bounds for predecessor search in the cell-probe model are the reason Dietz's bound is believed to be close to optimal, for space near linear. The general $O(1)$ overhead of the [DSST persistence theorem](/dsst-persistence-theorem/) does not cover arrays: its proof needs nodes of bounded in-degree, and a cell of an array is reached from every version by its index.

## Variants

- **Wide trees.** A tree with 32 children per node, as in the [persistent vector](/persistent-vector/), has height $\lceil \log_{32} n \rceil$. A write copies that many arrays of 32 slots, which is faster in practice on hardware with caches.
- **Random-access lists.** A [binary random-access list](/binary-random-access-list/) or a [skew binary random-access list](/skew-binary-random-access-list/) is a functional array that also supports cons, with $O(\log n)$ lookup and update.
- **Baker's rerooting array.** One real array holds the current version, and every other version is a chain of differences to it. Access to the current version is $O(1)$, and switching to another version reverses the chain on the way. Conchon and Filliâtre use it as the base of a [persistent union-find](/persistent-union-find/), where backtracking returns to recent versions.
- **Fat cells.** Each cell keeps its writes with version stamps. With partial persistence, a binary search by version number gives $O(\log m)$ per read. With full persistence, the stamps are compared in the preorder of the version tree.
- **Persistent segment trees.** Storing a summary such as a sum in each node turns the tree of this page into a [persistent segment tree](/persistent-segment-tree/), with range queries on every version at the same cost.

## When to use it

Use path copying when versions branch, when all versions are used about equally, and when $O(\log n)$ per access is acceptable. It is simple, needs no amortization, and is safe to share between threads. Use Baker's trick when most accesses go to one version or to versions near it, as in backtracking search. Use a plain mutable array when old versions are never needed, since each access is then $O(1)$ and no space is spent on old versions.

## Pitfalls

- **Writing in place.** A write into a node that exists changes every version that shares it. Every write must build new nodes.
- **Counting space.** Each write keeps $O(\log n)$ new nodes alive for as long as its version is reachable, so $m$ writes use $O(n + m \log n)$ space. Drop roots of versions that are no longer needed so that their nodes can be freed.
- **Index ranges.** The leaves for $[lo, mid)$ and $[mid, hi)$ must use the same $mid$ in BUILD, GET and SET. If $n$ is not a power of two, a mismatch sends reads to the wrong leaf without an error.
- **Baker's trick under branching.** Alternating between two versions far apart in the version tree costs the distance between them at every switch. It is not a good choice when old versions are used at random.
- **Fat cells with creation order.** For full persistence, the writes to a cell cannot be searched by version number, because a later version may be on a different branch. The search must use the order of the version tree.

## Implementations

The Python version is the path-copying tree of this page. `_Leaf` and `_Node` are the node classes, and `FullyPersistentArray` keeps the list of roots, so a version is an integer. It has `get(t, i)`, `set(t, i, x)` that returns the new version number, `to_list(t)`, `versions()` and `node_count()`. The tests build random version trees for several lengths, check every read and every full version against Python lists, and check the bound on the number of nodes.

## History

Path copying for arrays and other applicative data types was described by Myers in 1984. Baker's shallow binding of 1978, for Lisp environments, gave the rerooting idea, which he later applied to functional arrays. Driscoll, Sarnak, Sleator and Tarjan in 1989 gave general methods for full persistence with $O(1)$ overhead for structures of bounded in-degree, which excludes arrays. Dietz gave the $O(\log \log m)$ fully persistent array the same year. Conchon and Filliâtre in 2007 made Baker's arrays a practical base for persistent union-find.

## References
