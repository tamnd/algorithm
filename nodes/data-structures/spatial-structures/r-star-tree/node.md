---
tag: DENQWV
kind: data-structure
slug: r-star-tree
name: R*-tree
aliases:
- R-star tree
area: data-structures/spatial-structures
level: advanced
summary: R-tree variant with improved insertion and split heuristics that minimize overlap and perimeter.
implements: [spatial-index]
model: external-memory-model
complexity:
  vars: {n: the number of stored rectangles, M: the most entries in a node, m: the fewest entries in a non-root node, p: the number of entries removed by a forced reinsert, h: the height of the tree}
  time: {search: O(n), insert: O(p M^2 h^2), delete: O(n + m p M^2 h^3)}
  space: {total: O(n)}
history:
  year: 1990
  people: [Norbert Beckmann, Hans-Peter Kriegel, Ralf Schneider, Bernhard Seeger]
  note: Beckmann, Kriegel, Schneider and Seeger introduced the R*-tree at ACM SIGMOD 1990, after a study of the criteria that make R-tree queries fast.
prereqs: [r-tree, r-tree-node-splitting]
see_also: [r-tree, quadratic-split, r-plus-tree, x-tree, str-packing, overlap-and-dead-space, hilbert-r-tree, priority-r-tree]
sources:
  - paper: doi:10.1145/93597.98741
    title: Norbert Beckmann, Hans-Peter Kriegel, Ralf Schneider and Bernhard Seeger, The R*-tree, an efficient and robust access method for points and rectangles, Proceedings of ACM SIGMOD 1990, pp. 322 to 331
    locator: Section 3 (the optimization criteria, area, margin, overlap and storage use), Section 4.1 (ChooseSubtree), Section 4.2 (Split with ChooseSplitAxis and ChooseSplitIndex), Section 4.3 (forced reinsert) and Section 5 (performance comparison)
  - paper: doi:10.1145/1559845.1559929
    title: Norbert Beckmann and Bernhard Seeger, A revised R*-tree in comparison with related index structures, Proceedings of ACM SIGMOD 2009
    locator: the revised ChooseSubtree and split, which drop forced reinsertion, and the comparison with other R-tree variants
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, Object-Based and Image-Based Image Representations, the section on the R-tree and the R*-tree
  - paper: doi:10.1145/280277.280279
    title: Volker Gaede and Oliver Günther, Multidimensional access methods, ACM Computing Surveys 30(2), 1998, pp. 170 to 231
    locator: Section 5, the part on the R*-tree and the comparison of R-tree variants
---

The R*-tree is an [R-tree](/r-tree/) with better rules for where to insert and how to split. It is the same tree of nested bounding rectangles, with the same search, but it chooses the subtree above the leaves by the least growth of *overlap* with its siblings, splits a node along the axis where the split boxes have the smallest *margin* and then at the cut with the least overlap, and, before it splits a node for the first time during an insertion, removes the 30% of its entries that lie farthest from its center and inserts them again. Together these rules make boxes that are small, close to squares, and overlap little. Beckmann, Kriegel, Schneider and Seeger introduced it in 1990, and it became the R-tree used in most spatial databases.

## In plain words

An R-tree puts boxes into bags, and bags into bigger bags. A search opens every bag whose frame touches the question. So frames should be small, close to square, and should not cover each other, since a spot that two frames cover makes the search open both bags.

The R*-tree follows these goals in three places. When it adds a box near the bottom, it puts it where the frames will overlap the least. When a bag is too full, it first takes out a few boxes from the edge of the bag and adds them again from the top, since they may fit better in another bag. Only if the bag is still too full does it split the bag, and it splits it so that the two new frames are close to square and do not overlap.

## The abstract type

The R*-tree implements a [spatial index](/spatial-index/) for rectangles, as the R-tree does: `insert(id, r)`, `delete(id, r)` and `search(q)`, which reports the stored rectangles that meet the query rectangle $q$. Nearest neighbor search works by a best-first walk, as in any R-tree.

## Representation

The tree is an R-tree: nodes of at most $M$ entries, each entry a rectangle and a pointer, with the rectangle of an internal entry equal to the [minimum bounding rectangle](/minimum-bounding-rectangle/) of its child. The same invariant holds:

**Invariant (R).** (1) Every leaf is at the same depth. (2) Every node other than the root has between $m$ and $M$ entries; an internal root has at least 2. (3) The rectangle of each internal entry is the MBR of its child.

Two more parameters set the rules. The minimum fill is $m = 40\%$ of $M$ in the paper, which found it the best value. The number of entries removed by a forced reinsert is $p = 30\%$ of $M$. For a rectangle $r$, the *margin* is the sum of its side lengths; the implementation uses $w + h$, half the perimeter, which gives the same choices. The *overlap* of an entry $E_k$ in a node with entries $E_1, \ldots, E_t$ is $\sum_{j \ne k} \operatorname{area}(E_k \cap E_j)$.

## Operations

```pseudo id=main
INSERT(r, id)
L1  done ← ∅; INSERT-AT((r, id), 0)                    ▷ done: levels with a forced reinsert in this insertion

INSERT-AT(E, level)
L2  u ← CHOOSE-SUBTREE: from the root down to height level; at a node whose children are leaves, take the entry of least
        overlap enlargement (ties: least area enlargement, then least area); higher up, take the least area enlargement (ties: least area)
L3  add E to u; j ← level
L4  while u is not none:
L5      if u has M + 1 entries and u is not the root and j ∉ done then                     ▷ OVERFLOW-TREATMENT
            done ← done ∪ {j}; remove the p entries whose centers are farthest from the center of MBR(u);
            fix the rectangles from u up to the root; INSERT-AT each removed entry at height j, nearest first; return
L6      if u has M + 1 entries then split u into u and v with R*-SPLIT
L7          if u is the root then make a new root with the entries for u and v; return
L8          add (MBR(v), v) to the parent of u
L9      set the rectangle of u in its parent to MBR(u); u ← the parent of u; j ← j + 1
```

```pseudo id=split
R*-SPLIT(E1, ..., E(M+1), m)
L10 for each axis: for each of the two sorts of the entries, by the lower and by the upper side on that axis, and each cut k = m, ..., M + 1 − m
        into the first k and the other entries: add margin(MBR(first)) + margin(MBR(rest)) to the sum S of the axis
L11 choose the axis with the smallest S                                         ▷ CHOOSE-SPLIT-AXIS
L12 on that axis, over both sorts and all cuts, take the cut of least overlap area(MBR(first) ∩ MBR(rest)); ties: least total area
L13 return the two groups                                                      ▷ CHOOSE-SPLIT-INDEX
```

```pseudo id=other
DELETE(r, id)
L14 find the leaf that holds (r, id), through the entries whose rectangles contain r; remove the entry
L15 condense the tree as in the R-tree: remove each node on the path with fewer than m entries, and fix the rectangles
L16 reinsert the entries of the removed nodes at their heights with INSERT-AT; while the root is internal with one entry, make its child the root
SEARCH(q)
L17 the R-tree search: go into each entry whose rectangle meets q, and report the leaf entries that meet q
```

**Choose subtree.** Above the leaves, area is what matters, as in Guttman's tree. Just above the leaves, the R*-tree looks at overlap, because overlap of leaf boxes is what makes point queries follow several paths. The exact test costs $O(M^2)$ per node; the paper also gives an approximation that tests only the 32 entries of least area enlargement.

**Split.** The split looks only at *sorted* distributions, $2(M - 2m + 2)$ per axis. The margin sum chooses the axis: an axis on which the cuts give boxes with a small margin is an axis along which the entries are spread, and boxes cut along it are close to squares. On that axis, the overlap chooses the cut.

**Forced reinsert.** A node that overflows has entries at its edges that may fit better elsewhere. Removing them and inserting them again moves them, shrinks the node, and often avoids the split. It runs at most once per level in each insertion, which bounds the work, and never at the root. The paper found that inserting the removed entries nearest first (close reinsert) works better than farthest first.

## Example

Take $M = 4$, $m = 2$ and $p = 1$, and insert, as $[x_1, x_2] \times [y_1, y_2]$: a $= [0, 2] \times [0, 2]$, b $= [1, 3] \times [5, 7]$, c $= [6, 8] \times [0, 1]$, d $= [7, 9] \times [6, 9]$, e $= [2, 3] \times [1, 3]$, f $= [6, 7] \times [7, 8]$, g $= [1, 2] \times [3, 4]$ and h $= [3, 4] \times [6, 8]$. The margin below is $w + h$.

**Insert a to d.** The root is a leaf with 4 entries.

**Insert e.** The root leaf overflows. The root never does a forced reinsert, so it splits. With 5 entries and $m = 2$, there are two cuts per sort, at $k = 2$ and $k = 3$.

| axis | sorted order | cut | margin sum | overlap | area sum |
|---|---|---|---|---|---|
| $x$ | a, b, e, c, d (both sorts) | a b / e c d | 26 | 7 | 84 |
| $x$ | | a b e / c d | 22 | 0 | 48 |
| $y$ | c, a, e, b, d (both sorts) | c a / e b d | 26 | 7 | 80 |
| $y$ | | c a e / b d | 23 | 0 | 56 |

Each sort appears twice in the sums, so $S_x = 2(26 + 22) = 96$ and $S_y = 2(26 + 23) = 98$. The axis is $x$, and its cut of least overlap is $\{a, b, e\}$ against $\{c, d\}$. The root now has the leaves $[0, 3] \times [0, 7]$ with a, b, e and $[6, 9] \times [0, 9]$ with c, d.

**Insert f and g.** f goes to the second leaf and g to the first: both choices have no overlap enlargement, and the area enlargement decides. The leaves are {a, b, e, g} and {c, d, f}.

**Insert h.** CHOOSE-SUBTREE compares the two leaves: both have overlap enlargement 0, and the area enlargement is 11 for the first ($[0, 3] \times [0, 7]$ becomes $[0, 4] \times [0, 8]$) against 27 for the second. The first leaf gets h and has 5 entries. It is not the root, and level 0 has no reinsert yet, so OVERFLOW-TREATMENT reinserts. The center of $[0, 4] \times [0, 8]$ is $(2, 4)$; the squared distances of the centers are 10 for a, 4 for b, 4.25 for e, 0.5 for g and 11.25 for h. So h, the farthest, is removed, and the leaf shrinks back to $[0, 3] \times [0, 7]$. h is inserted again, goes to the same leaf for the same reason, and the leaf overflows again. Level 0 is now in done, so the leaf splits.

| axis | cut | margin sum | overlap | area sum |
|---|---|---|---|---|
| $x$ | a g / b e h | 16 | 3 | 29 |
| $x$ | a g b / e h | 19 | 6 | 35 |
| $y$ | a e / g b h | 14 | 0 | 24 |
| $y$ | a e g / b h | 13 | 0 | 21 |

$S_x = 70$ and $S_y = 54$, so the axis is $y$; both cuts on $y$ have overlap 0, and the area sum picks $\{a, e, g\}$ with box $[0, 3] \times [0, 4]$ against $\{b, h\}$ with box $[1, 4] \times [5, 8]$. The root now has three leaves: {a, e, g}, {b, h} and {c, d, f}, and no two leaf boxes overlap.

**Search and delete.** SEARCH($[2.5, 7] \times [2.5, 7]$) meets all three leaves and reports b, d, e, f and h. SEARCH($[4.5, 5.5] \times [1.5, 4.5]$) meets the root box but no leaf box, and reports nothing. Deleting c leaves {d, f} with box $[6, 9] \times [6, 9]$. Deleting d then leaves f alone, under $m = 2$: the leaf is removed and f is inserted again, into the leaf of b and h, which becomes $[1, 7] \times [5, 8]$.

## Correctness

The R*-tree changes only the choices of the R-tree, so the argument of the R-tree applies. CHOOSE-SUBTREE returns some node at the right height, whatever rule it uses. A forced reinsert removes $p \le M - m$ entries from a node with $M + 1$, which keeps at least $m + 1$, fixes the rectangles above it, and then puts each entry back by INSERT-AT at its own height, so each entry is stored once and each leaf stays at the same depth. R*-SPLIT returns two groups of at least $m$ entries, since every cut it looks at has $k \ge m$ and $M + 1 - k \ge m$. Each insertion stops, since forced reinserts happen at most once per level, and each split or reinsert moves up or finishes. The full proof is in the proofs folder.

## Complexity

The model is the [external memory model](/external-memory-model/) with one node per page, or the RAM with a cost per entry examined; $h \le \log_m(n/2)$ is the height, as for any R-tree.

- **Search.** As for the R-tree, $O(n)$ in the worst case, and in practice a few paths. The R*-tree does not change the worst case; it makes the typical case faster: in the experiments of the paper it read fewer pages than Guttman's linear and quadratic splits on almost all the data sets and queries tested.
- **Insert without reinsert.** CHOOSE-SUBTREE costs $O(M^2)$ at the level above the leaves for the overlap test, and $O(M)$ elsewhere. A split costs $O(M \log M)$ for the sorts and $O(M)$ per cut with prefix boxes; the simple code costs $O(M^2)$. So one INSERT-AT without reinserts costs $O(M^2 h)$.
- **Insert with reinserts.** Each level does at most one forced reinsert per insertion, which starts $p$ more INSERT-ATs. So one insertion runs at most $1 + p h$ INSERT-ATs, which gives $O(p M^2 h^2)$ in the worst case. In practice most insertions do no reinsert.
- **Delete.** Finding the leaf costs $O(n)$ in the worst case. The condensation removes at most $h$ nodes, each with fewer than $m$ entries, so at most $m h$ entries are reinserted, each at the cost of an insertion.
- **Space.** $O(n)$ entries in $O(n/m)$ nodes. The reinserts raise the storage use above that of Guttman's tree, since they often avoid a split.

| operation | time | case |
|---|---|---|
| search | $O(n)$ | worst |
| insert | $O(p M^2 h^2)$ | worst |
| delete | $O(n + m p M^2 h^3)$ | worst |
| space | $O(n)$ | total |

## Variants

- **Without forced reinsert.** Many systems turn reinsertion off, because it makes insertion slower and harder to run in parallel. The tree is still good, with the split and the subtree choice of the R*-tree.
- **Revised R*-tree.** Beckmann and Seeger revised the rules in 2009: a ChooseSubtree that looks at the overlap with a bounded search, and a split that weighs overlap, the margin and the balance of the groups, with no forced reinsert.
- **Bulk loading.** For static data, [STR packing](/str-packing/) or a [Hilbert](/hilbert-r-tree/) packing builds a better tree faster, and the R*-tree rules then handle later inserts.
- **High dimensions.** The [X-tree](/x-tree/) adds supernodes to the R*-tree split when every split has too much overlap. The [SR-tree](/sr-tree/) and the [SS-tree](/ss-tree/) use spheres.
- **Without overlap.** The [R+-tree](/r-plus-tree/) gives up the single copy of each object to remove overlap entirely.

## When to use it

Use the R*-tree as the default dynamic index for rectangles and points in low dimensions, when the data changes and queries matter more than the cost of an insert, as in a spatial database or a GIS. The R*Tree module of SQLite, for example, is named after it. Use [STR packing](/str-packing/) when the data is loaded once, the [priority R-tree](/priority-r-tree/) when a worst-case bound is needed, and a plain R-tree with the linear split when inserts must be as cheap as possible.

## Pitfalls

- **Reinsert at the root.** The root has no siblings to take the entries, so reinsert there loops. The rule forbids it.
- **Reinsert more than once per level.** Without the set done, a reinsert can cause an overflow at the same level, which causes another reinsert, without end. Reset done at the start of each top-level insertion, not of each INSERT-AT.
- **Height changes during reinsertion.** A split of the root during the reinsertion of an internal entry raises the height of the tree. Store the height of an entry as the distance from the leaves, as here, not from the root.
- **Ties in the split.** Points and equal rectangles give many cuts with zero overlap and zero area. Break ties in a fixed way, or the tree depends on the input order in surprising ways.
- **Overlap in high dimensions.** In more than about 10 dimensions, almost every split has large overlap, and the R*-tree degrades toward a scan. See the [curse of dimensionality](/curse-of-dimensionality/) and the [X-tree](/x-tree/).

## Implementations

## History

Beckmann, Kriegel, Schneider and Seeger studied in 1990 which properties of an R-tree make queries fast, and found four: small area of the boxes, small overlap, small margin and high storage use. They designed the R*-tree to meet them all, and showed in experiments on many data sets that it beat Guttman's linear and quadratic splits and Greene's split. It became the usual R-tree in research systems and in many commercial ones. In 2009 Beckmann and Seeger gave a revised version that drops forced reinsertion.

## References
