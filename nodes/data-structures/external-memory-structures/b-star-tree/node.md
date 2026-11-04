---
tag: FES1ZP
kind: data-structure
slug: b-star-tree
name: B*-tree
area: data-structures/external-memory-structures
level: intro
summary: B+ tree variant that keeps nodes at least two-thirds full by redistributing keys with siblings.
implements: [ordered-set]
model: external-memory-model
prereqs: [b-plus-tree]
see_also: [b-tree, b-plus-tree, external-searching, bulk-loading-b-tree, blink-tree, clustered-index]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.4, the B*-tree (overflow into a sibling, splits of two nodes into three, the larger root)
  - paper: doi:10.1145/356770.356776
    title: "Douglas Comer, The ubiquitous B-tree, ACM Computing Surveys 11(2) (1979)"
    locator: pp. 121 to 137, the section on B*-trees
  - paper: doi:10.1007/BF00288683
    title: "Rudolf Bayer and Edward M. McCreight, Organization and maintenance of large ordered indexes, Acta Informatica 1(3) (1972)"
    locator: pp. 173 to 189 (the B-tree that the B*-tree changes)
---

A B*-tree is a [B+ tree](/b-plus-tree/) with a stronger fill rule: each node other than the root is at least about two-thirds full, not half full. With a capacity of $C$ entries per node, each node other than the root has at least $f = \lfloor (2C+1)/3 \rfloor$ entries. To keep this rule, a node that overflows first shifts entries into a neighbouring sibling, and only when that sibling is also full are the two full nodes split into three. Deletion works the other way: a node that underflows borrows from a sibling, or three nodes are merged into two. Search, insertion and deletion still read $O(\log_C n)$ nodes, but the tree uses fewer nodes and can be one level lower than a B+ tree with the same keys.

## In plain words

Think of books on a row of shelves, in order. In an ordinary B+ tree, when a shelf is full you buy a new shelf and move half the books to it, so many shelves are only half full.

A B*-tree is more careful. When a shelf is full, it first moves some books to the shelf next to it, if that shelf has room. Only when both shelves are full does it buy one new shelf and spread the books of the two full shelves over three. Each of the three is then two-thirds full.

When a shelf gets too empty, it takes books from a neighbour, or three shelves are packed into two. So all shelves stay at least two-thirds full, and you need fewer shelves.

## The abstract type

A B*-tree implements the [ordered set](/ordered-set/), with `search(T, k)`, `insert(T, k)`, `delete(T, k)` and `range(T, a, b)`, the same as the [B+ tree](/b-plus-tree/). The keys are distinct.

## Representation

The nodes are those of a [B+ tree](/b-plus-tree/): leaves hold sorted keys and a link $next$ to the leaf on their right, and an internal node holds sorted separators $key[1 \ldots m]$ and $m + 1$ children, where the child $c[i]$ holds the keys $k$ with $key[i] \le k < key[i+1]$. The *entries* of a node are its keys if it is a leaf and its children if it is internal. There is a capacity $C \ge 4$, and

$$f = \left\lfloor \frac{2C + 1}{3} \right\rfloor, \qquad R = 2f - 1.$$

The invariants are:

- **(S1)** Each node other than the root has between $f$ and $C$ entries. The root has at most $R$ entries, and an internal root has at least 2 children.
- **(S2)** The search order of the separators, as in the B+ tree.
- **(S3)** All leaves have the same depth.
- **(S4)** The leaves are linked by $next$ in increasing order.

For $C = 4$, $f = 3$ and $R = 5$. For $C = 512$, $f = 341$, so every node other than the root is at least $341/512 \approx 66.6\%$ full. The value of $f$ is the largest that lets two full nodes, plus the one new entry, fill three nodes: $\lfloor (2C+1)/3 \rfloor \cdot 3 \le 2C + 1$.

**The root.** The root has no sibling to share with. When it overflows, it splits into two nodes, and each must have at least $f$ entries, so the root may grow to $R = 2f - 1$ entries and splits at $2f$. This is Knuth's rule: the root can be larger than the other nodes. It is in memory, so its size does not cost a disk read. The condition $C \ge 4$ gives $f \ge 3$, so each internal node other than the root has at least 3 children, and the only node that can have exactly 2 children is the root.

## Operations

All the rebalancing goes through one step, SHARE, which takes $g$ neighbouring children of a node and rebuilds them as $k$ children with equal shares of their entries. Shifting entries to a sibling is SHARE with $g = k = 2$, the split of two full nodes is $g = 2, k = 3$, and the merges are $g = 3, k = 2$ and $g = 2, k = 1$.

```pseudo id=main
SEARCH(T, k)
L1  x ← T.root
L2  while x is not a leaf do
L3      i ← the number of separators of x that are ≤ k
L4      x ← x.c[i], DISK-READ(x)
L5  return (k is a key of x)

BSTAR-INSERT(T, k)                          ▷ k is not in T
L6  INSERT-REC(T.root, k)
L7  if T.root has more than R entries then  ▷ it has exactly 2f
L8      make a new root with the old root as its only child, SHARE(T.root, 0, 1, 2)

INSERT-REC(x, k)
L9  if x is a leaf then insert k into x in order, return
L10 i ← the number of separators of x that are ≤ k, DISK-READ(x.c[i])
L11 INSERT-REC(x.c[i], k)
L12 if x.c[i] has at most C entries then return
L13 if a sibling x.c[j] next to x.c[i] has fewer than C entries then
L14     SHARE(x, min(i, j), 2, 2), return       ▷ shift entries into the sibling
L15 j ← i − 1 if i > 0, else i + 1              ▷ that sibling is full
L16 SHARE(x, min(i, j), 2, 3)                   ▷ two full nodes become three

SHARE(x, j, g, k)                ▷ the children x.c[j .. j+g−1] become k children
L17 read the g children; gather their entries in order; if internal, put the separators of x between them
L18 t ← the number of entries; give each of the k new nodes ⌊t/k⌋ or ⌈t/k⌉ of them
L19 a leaf after the first sends a copy of its first key up; an internal node after the first sends up the separator before its first child
L20 put the k nodes and the k − 1 new separators in x in place of the old ones; relink the leaves

BSTAR-DELETE(T, k)                          ▷ k is in T
L21 DELETE-REC(T.root, k)
L22 if T.root is internal with only one child then T.root ← that child

DELETE-REC(x, k)
L23 if x is a leaf then remove k from x, return
L24 i ← the number of separators of x that are ≤ k, DISK-READ(x.c[i])
L25 DELETE-REC(x.c[i], k)
L26 if x.c[i] has at least f entries then return
L27 if a sibling x.c[j] next to x.c[i] has more than f entries then SHARE(x, min(i, j), 2, 2), return
L28 if x has 2 children then SHARE(x, 0, 2, 1), return   ▷ x is the root
L29 j ← the first of three neighbouring children of x that include x.c[i]
L30 if they have at most 2C entries in total then SHARE(x, j, 3, 2) else SHARE(x, j, 3, 3)
```

A range query is the same as in the B+ tree: find the leaf of the lower end and follow the $next$ links.

## Example

Take $C = 4$, so $f = 3$ and $R = 5$: each node other than the root has 3 or 4 entries. Leaves are in square brackets, an internal node is in angle brackets followed by its children. Insert $10, 20, 30, 40, 50, 60, 15, 25, 35, 45, 55, 65, 70$.

| step | what happens | the tree after it |
|---|---|---|
| insert 10 to 50 | the root leaf may hold $R = 5$ keys | [10 20 30 40 50] |
| insert 60 | the root has 6 = $2f$ keys: split into 3 and 3 | <40>([10 20 30] [40 50 60]) |
| insert 15 | | <40>([10 15 20 30] [40 50 60]) |
| insert 25 | the left leaf has 5 keys; its sibling has room: shift, 4 and 4 | <30>([10 15 20 25] [30 40 50 60]) |
| insert 35 | the leaf [30 35 40 50 60] overflows, its sibling is full: 9 keys into three leaves of 3 | <25 40>([10 15 20] [25 30 35] [40 50 60]) |
| insert 45, 55 | after 55, the last leaf shifts one key into its left sibling | <25 45>([10 15 20] [25 30 35 40] [45 50 55 60]) |
| insert 65 | the last two leaves are full: 9 keys into three of 3 | <25 40 55>([10 15 20] [25 30 35] [40 45 50] [55 60 65]) |
| insert 70 | | <25 40 55>([10 15 20] [25 30 35] [40 45 50] [55 60 65 70]) |

A B+ tree of order 2 with the same 13 keys can have leaves with only 2 keys. Here no leaf has fewer than 3. Now delete $70, 65, 10, 20, 15, 50, 55, 25$.

| step | what happens | the tree after it |
|---|---|---|
| delete 70 | | <25 40 55>([10 15 20] [25 30 35] [40 45 50] [55 60 65]) |
| delete 65 | [55 60] underflows, its sibling has exactly 3: the last three leaves, 8 keys, become two | <25 45>([10 15 20] [25 30 35 40] [45 50 55 60]) |
| delete 10 | [15 20] borrows from its right sibling of 4 | <30 45>([15 20 25] [30 35 40] [45 50 55 60]) |
| delete 20 | [15 25] underflows, its sibling has 3; the first three leaves have 9 keys, more than $2C = 8$, so they are shared out as 3, 3, 3 | <35 50>([15 25 30] [35 40 45] [50 55 60]) |
| delete 15 | the three leaves have 8 keys: merge into two | <45>([25 30 35 40] [45 50 55 60]) |
| delete 50 | | <45>([25 30 35 40] [45 55 60]) |
| delete 55 | [45 60] borrows 40 | <40>([25 30 35] [40 45 60]) |
| delete 25 | [30 35] underflows and the root has 2 children: merge them into one node of 5 keys, which becomes the root | [30 35 40 45 60] |

## Correctness

SHARE keeps the in-order sequence of the keys of its group, and for internal nodes the in-order sequence of children and separators. The separator it sends up between two new nodes divides their key ranges, so the search order (S2) holds, and all new nodes stay at the old depth, so (S3) holds. What remains is the count of entries. Each call of SHARE gives its $k$ nodes $\lfloor t/k \rfloor$ to $\lceil t/k \rceil$ entries, and the cases give:

- line L14: $t \le (C + 1) + (C - 1) = 2C$, and $t \ge (C + 1) + f$, so each node has between $f$ and $C$;
- line L16: $t = 2C + 1$, so each node has at least $\lfloor (2C+1)/3 \rfloor = f$ and at most $\lceil (2C+1)/3 \rceil \le C$;
- line L27: $f - 1 + f + 1 \le t \le f - 1 + C$, so each of the two has between $f$ and $C$;
- line L30: the siblings next to $x.c[i]$ have exactly $f$ entries and the third node of the group at least $f$, so $t \ge 3f - 1$, and two nodes have at least $\lfloor (3f - 1)/2 \rfloor \ge f$ each; if $t > 2C$ the three nodes have at least $\lfloor (2C+1)/3 \rfloor = f$ each and, since $t \le (f - 1) + f + C \le 3C$, at most $C$;
- line L28: the root has two children with $2f - 1 = R$ entries, which fit in one root.

The full proof is below.

## Complexity

**Height.** Let the tree have $n \ge 2f$ keys and height $h \ge 1$. The root has at least 2 children and each other node at least $f$ entries, so $n \ge 2 f^{h}$ and

$$h \ \le\ \log_f \frac{n}{2}, \qquad f \approx \tfrac{2}{3} C.$$

A B+ tree with nodes of the same capacity $C$ has only $C/2$ entries per node in the worst case, so its bound is $\log_{C/2}(n/2)$. For $C = 512$ and $n = 10^9$, the B*-tree bound is $\log_{341}(5 \cdot 10^8) \approx 3.43$ and the B+ bound is $\log_{256}(5 \cdot 10^8) \approx 3.61$, so both trees have at most 3 levels below the root here; for other values of $n$ the B*-tree saves a level.

| operation | node reads | CPU time |
|---|---|---|
| search | $h$ | $O(h \log C)$ |
| insert | $h$ plus at most 1 sibling per level | $O(h\, C)$ |
| delete | $h$ plus at most 2 siblings per level | $O(h\, C)$ |
| range with $Z$ answers | at most $h + Z/f + 2$ | $O(h \log C + Z)$ |

**Space.** Each node other than the root holds at least $f \ge (2C - 1)/3$ entries, so the tree uses at most about $\frac{3}{2} \cdot \frac{n}{C}$ leaves, against $2n/C$ for a B+ tree in the worst case. With $C = \Theta(B)$, all operations cost $O(\log_B n)$ I/Os, as for [external searching](/external-searching/) in general.

**The cost of the fill rule.** An insertion that shifts entries into a sibling reads and writes one more node, and a split writes three nodes, not two. Deletion may read two siblings. These are constant factors per level.

## Variants

- **B*-trees in the B-tree form.** Knuth defined the B*-tree for [B-trees](/b-tree/), with records in all nodes, and the same rules work there: the node that overflows shares its keys with a sibling through the separator in the parent. This page uses the B+ form, as the stub summary does.
- **Larger groups.** The same idea with $s$ siblings: when $s$ neighbouring nodes are full, split them into $s + 1$. Nodes are then at least $s/(s+1)$ full, at the cost of more reads per update.
- **Bulk loading.** A tree built from sorted keys can fill every node to any chosen level up to $C$, which is better than either rule. See [bulk loading a B-tree](/bulk-loading-b-tree/).
- **Concurrency.** Shifting into a sibling changes two nodes and their separator, so it needs more locking than a plain split. The [B-link tree](/blink-tree/) is a common base for concurrent trees.

## When to use it

Use the B*-tree rule when space and height matter more than a little more work per update: for a large index that is read much more often than it changes, a fuller tree means fewer blocks to cache and, sometimes, one less level. When updates are frequent, the extra sibling reads and writes cost more, and most systems use a plain [B+ tree](/b-plus-tree/) with the half-full rule, or bulk loading with a fill factor for indexes that do not change.

## Pitfalls

- **The root.** If the root has the capacity $C$ of the other nodes and splits at $C + 1$, the two halves have only about $C/2$ entries and break the two-thirds rule. Let the root grow to $R = 2f - 1$ (line L7), or accept that the children of the root may be less full.
- **A capacity that is too small.** With $C = 3$ the minimum is $f = 2$, and an internal node other than the root can have 2 children. Then a node can have one sibling only, and the merge of three into two in line L30 is not always possible. Require $C \ge 4$.
- **Merging two into one.** Two nodes with $f - 1$ and $f$ entries have $2f - 1$ entries, more than $C$ for most $C$, so they cannot merge into one ordinary node. Merges take three nodes into two, and only the root case of line L28 merges two into one.
- **Separators after SHARE.** For leaves, the separator between two new leaves is a copy of the first key of the right one. For internal nodes, it is the separator that was between the two groups of children and leaves the lower level. Mixing the two rules loses keys or children, as in the B+ tree.
- **The leaf links.** SHARE rebuilds the leaves of the group, and the last new leaf must take the old $next$ link of the last leaf of the group (line L20).

## Implementations

## History

Knuth introduced the name B*-tree in Section 6.2.4 of volume 3 of The Art of Computer Programming, for a [B-tree](/b-tree/) in which a full node first shares its keys with a sibling and two full nodes are split into three, so that nodes stay at least two-thirds full. Bayer and McCreight's B-tree of 1972, which the B*-tree changes, keeps nodes only half full. Comer's survey of 1979 describes the B*-tree among the variants of the B-tree. Texts do not all use the name in the same way, and some use it for the B+ tree.

## References
