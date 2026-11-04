---
tag: FNAH5S
kind: technique
slug: fat-node
name: Fat node
aliases:
- fat-node method
- version list node
area: data-structures/persistent-structures
level: advanced
summary: Each node stores all its field values tagged with version stamps, so one node can answer for any version.
prereqs: [partial-persistence, binary-search]
see_also: [node-copying, path-copying, full-persistence, dsst-persistence-theorem, fully-persistent-array, historical-queries, version-tree, bakers-trick]
sources:
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: pages 86 to 124, the section on partial persistence (the fat node method) and the section on full persistence (the version list and fat nodes for full persistence)
  - paper: doi:10.1145/28395.28434
    title: Paul F. Dietz and Daniel D. Sleator, Two algorithms for maintaining order in a list, Proceedings of the 19th ACM Symposium on Theory of Computing (STOC 1987)
    locator: pages 365 to 372 (order maintenance with O(1) time per comparison)
  - paper: doi:10.1007/3-540-51542-9_8
    title: Paul F. Dietz, Fully persistent arrays, Algorithms and Data Structures (WADS 1989), Lecture Notes in Computer Science 382
    locator: pages 67 to 74 (fat cells with a version list, searched with a faster predecessor structure)
---

The fat node method makes a linked data structure persistent by never overwriting a field. Each field keeps the whole history of its values, each tagged with the version that wrote it, and a read in version $i$ picks the value that version $i$ sees. For [partial persistence](/partial-persistence/) the history is a list in time order, an update appends to it in $O(1)$ time and space, and a read is a [binary search](/binary-search/) in $O(\log m)$ time, where $m$ is the number of versions. For [full persistence](/full-persistence/) the versions are ordered by a preorder of the [version tree](/version-tree/), and both reads and writes take $O(\log m)$ time. The method copies nothing, so it uses the least space of the general methods, at the price of a logarithmic slowdown on every access.

## In plain words

Picture a notice board where nobody erases anything. To change a note, you pin a new card under the old one and write the date on it. To learn what the note said on some day, you look down the cards for the last one dated on or before that day. Nothing is ever thrown away, so every old day can still be read.

The board never grows by more than one card for each change, which is cheap. The cost is in reading: with many cards, you must search through them each time, even for the newest value.

## When it applies

- **The structure is made of nodes with fields.** Any linked structure, or an array seen as a set of cells, fits. Unlike [node copying](/node-copying/), the method needs no bound on the in-degree, because nodes are never copied and pointers to a node never change.
- **Space matters more than read time.** Each update step costs $O(1)$ space in the worst case, with no amortization. Each read pays a search.
- **Versions are numbered.** Partial persistence needs only the version numbers in time order. Full persistence needs a version list, kept with an order-maintenance structure.

## The template

In version $i$, $x.f$ is a search structure of pairs (stamp, value). In the partial case the stamps are version numbers and the structure is an array in increasing order. In the full case the stamps are positions in the version list, which holds two markers $b_v$ and $e_v$ for each version $v$, nested as parentheses in a preorder of the version tree, and $x.f$ is a balanced search tree ordered by the list.

```pseudo id=main
READ-PARTIAL(x, f, i)
L1  (s, v) ← the last pair of x.f with s ≤ i      ▷ binary search
L2  return v

WRITE-PARTIAL(x, f, v, t)                        ▷ t is the newest version
L3  append (t, v) to x.f, or replace the last pair if its stamp is t

NEW-VERSION(i, t)                                ▷ version t is a child of version i
L4  insert b_t, e_t right after b_i in the version list

READ-FULL(x, f, i)
L5  (q, v) ← the pair of x.f with the last position q ≤ b_i
L6  return v

WRITE-FULL(x, f, v, t)                           ▷ t is a child of i
L7  if x.f has no pair at e_t then insert (e_t, READ-FULL(x, f, i)) into x.f
L8  insert or replace (b_t, v) in x.f
```

The original value of a field, in the version $0$ that creates the node, is the pair $(0, v)$ in the partial case and $(b_0, v)$ in the full case. A node created in version $t$ is created with its pairs stamped $t$, or $b_t$ and $e_t$ as by WRITE-FULL.

**Why the partial case is correct.** Versions are made in increasing order and only the newest version $t$ is written, so the pairs of $x.f$ are in increasing order of stamps and line L3 keeps the array sorted. The value of $x.f$ in version $i$ is the value of the last write to it in a version at most $i$, which is the pair that line L1 finds.

**Why the full case is correct.** Fix a field. Call a version a *writer* if it wrote the field. Each writer $u$ has the pair $(b_u, \text{the value in } u)$ and the pair $(e_u, \text{the value in the parent of } u)$, by lines L7 and L8. Give each marker a version: $b_u$ belongs to $u$ and $e_u$ to the parent of $u$. We show that at every marker $q$, the last pair at a position at most $q$ holds the value of the field in the version of $q$. At $b_0$ this is the original value. Walk along the list. If the next marker carries a pair, the pair gives the right value by construction. If it carries no pair, it is $b_u$ or $e_u$ for a version $u$ that is not a writer, and the value of the field in $u$ equals the value in its parent. In the parenthesis order, a marker $b_u$ follows a marker of the parent of $u$, and a marker $e_u$ follows a marker of $u$, so in both cases the version changes between a parent and a child that is not a writer, and the value stays the same. So line L5 is correct. Line L4 puts the subtree of $t$, which is just $t$, inside the interval of $i$, which keeps the parenthesis structure.

**Cost.** In the partial case, line L1 takes $O(\log m)$ time and line L3 takes $O(1)$ time and space, with an array that doubles when full. In the full case the comparisons of two markers take $O(1)$ time with the order-maintenance structure of Dietz and Sleator, so lines L5, L7 and L8 take $O(\log m)$ time in a balanced search tree, and a write adds at most two pairs, $O(1)$ space.

## Classic examples

### A trace for full persistence

One field starts with value 0 in version 0. Version 1 is a child of 0 and writes 5. Version 2 is a child of 1 and writes 7. Version 3 is a child of 1 and writes nothing. Version 4 is a child of 2 and writes 9.

| step | version list | pairs of the field |
|---|---|---|
| version 0 | $b_0\, e_0$ | $(b_0, 0)$ |
| version 1 | $b_0\, b_1\, e_1\, e_0$ | $(b_0, 0), (b_1, 5), (e_1, 0)$ |
| version 2 | $b_0\, b_1\, b_2\, e_2\, e_1\, e_0$ | adds $(b_2, 7), (e_2, 5)$ |
| version 3 | $b_0\, b_1\, b_3\, e_3\, b_2\, e_2\, e_1\, e_0$ | no change |
| version 4 | $b_0\, b_1\, b_3\, e_3\, b_2\, b_4\, e_4\, e_2\, e_1\, e_0$ | adds $(b_4, 9), (e_4, 7)$ |

A read in version 3 finds the last pair at or before $b_3$, which is $(b_1, 5)$: version 3 inherits the value of its parent 1. A read in version 2 finds $(b_2, 7)$, and in version 4 it finds $(b_4, 9)$. If a version 5 is made as a child of 0 without a write, the list starts $b_0\, b_5\, e_5\, b_1 \ldots$ and a read in version 5 finds $(b_0, 0)$. Note that a search by creation number would give wrong answers: version 3 was made after version 2, but it must not see the value 7.

### Other examples

- **A partially persistent array.** Each cell is a fat node with one field. A write appends a pair and a read in an old version is a binary search, as in the example on the page [partial persistence](/partial-persistence/).
- **A fully persistent array.** Dietz keeps a fat cell for each index, with stamps from the version list, and replaces the balanced search tree by a faster predecessor structure on the stamps, which gives $O(\log \log m)$ time per access; see [fully persistent array](/fully-persistent-array/).
- **A persistent search tree.** A [binary search tree](/binary-search-tree/) with fat nodes uses $O(1)$ space per changed field, but a search in version $i$ pays $O(\log m)$ at each node it visits, so $O(\log n \log m)$ in total. This slowdown is what node copying removes.
- **Temporal tables.** Some databases keep, for each row, the list of its values with the time interval in which each was valid. A query "as of time $t$" reads the value whose interval holds $t$. This is the same idea for [historical queries](/historical-queries/).

## Variations

- **Bounded fat nodes.** Give each node only a constant number of extra pairs and copy the node when they are full. This is [node copying](/node-copying/), which brings the read time down to $O(1)$ for structures of bounded in-degree; see the [DSST theorem](/dsst-persistence-theorem/).
- **Node splitting.** The full-persistence analogue of node copying splits a full fat node into two nodes that cover two ranges of the version list.
- **Faster searches on stamps.** The stamps of one field are integers or list positions, so a predecessor structure such as a van Emde Boas tree can replace the binary search, as in Dietz's arrays.
- **Rerooting.** [Baker's trick](/bakers-trick/) also keeps all versions without copies, but stores the differences between versions on a tree of versions and moves the real values to the version in use.

## Pitfalls

- **Searching by creation order in the full case.** In full persistence, the version that was made last is not the one whose value a version sees. Use the version list, as the trace shows.
- **Forgetting the end marker.** Without the pair at $e_t$, the versions after the subtree of $t$ in the list, such as the later siblings of $t$, would see the value written by $t$.
- **Every read pays.** The slowdown applies to every access step, also to the reads of the newest version. For a structure that is mostly read in its newest version, keep the newest value of each field in place next to the history.
- **Space never comes back.** The history grows with each write. Old pairs cannot be dropped while any version that may read them is still in use.

## Exercises

1. In the trace, add version 6 as a child of 3 that writes 4. Write the new version list and pairs, and read the field in versions 3, 6 and 2.
2. Show that a partially persistent linked list with fat nodes answers "the $k$-th element in version $i$" in $O(k \log m)$ time, and give an example where this is $\Theta(k \log m)$.
3. Prove that in the partial case the number of pairs in all fields together is at most the number of nodes created plus the number of field writes.
4. Why does the fat node method need no bound on the in-degree, while node copying does?

## References
