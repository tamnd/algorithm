---
tag: TMRMPW
kind: data-structure
slug: kd-b-tree
name: k-d-B tree
aliases:
- k-d-B-tree
- KDB tree
area: data-structures/spatial-structures
level: advanced
summary: Disk-oriented hybrid of the k-d tree and the B-tree in which all leaves are at the same depth.
implements: [spatial-index]
model: external-memory-model
complexity:
  vars: {n: the number of points, B: the capacity of a point page, M: the fan-out of a region page, h: the height, s: the number of pages cut by a forced split, v: the number of pages visited}
  time: {lookup: O(h M), insert: O(h M^2 + s), delete: O(h M + B), range_search: O(v M + v B)}
  space: {total: O(n)}
history:
  year: 1981
  people: [John T. Robinson]
  note: Robinson introduced the K-D-B-tree at SIGMOD 1981, combining the splitting planes of the k-d tree with the balanced, paged structure of the B-tree.
prereqs: [kd-tree, b-tree]
see_also: [grid-file, r-tree, external-memory-model, orthogonal-range-searching, bulk-loading, buffer-tree, priority-r-tree, object-partitioning]
sources:
  - paper: doi:10.1145/582318.582321
    title: John T. Robinson, The K-D-B-tree, a search structure for large multidimensional dynamic indexes, Proceedings of ACM SIGMOD 1981
    locator: the whole paper (point pages and region pages, insertion with splits of region pages by a plane, the downward forced splits, and the lack of a bound on page fill)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 1, Multidimensional Point Data, the section on the k-d-B-tree and the hB-tree among the bucket methods with tree directories
  - paper: doi:10.1145/280277.280279
    title: Volker Gaede and Oliver Günther, Multidimensional access methods, ACM Computing Surveys 30(2), 1998
    locator: the section on point access methods, the parts on the k-d-B-tree, the hB-tree and the LSD-tree
  - paper: doi:10.1145/99935.99944
    title: David B. Lomet and Betty Salzberg, The hB-tree, a multiattribute indexing method with good guaranteed performance, ACM Transactions on Database Systems 15(4), 1990
    locator: the discussion of the cascading splits of the k-d-B-tree and the holey brick regions that avoid them
---

A k-d-B tree is a [B-tree](/b-tree/) for points in $k$ dimensions. Its leaves, the *point pages*, hold up to $B$ points each, and its internal nodes, the *region pages*, hold up to $M$ entries, each a box and a pointer to a child page. The boxes of the entries of a page partition the box of the page, as the cells of a [k-d tree](/kd-tree/) do, and all point pages are at the same depth, as in a B-tree. A page that overflows is cut in two by an axis-parallel plane, and the parent gets one more entry. Unlike a B-tree, a cut of a region page may cross some of its children, which must then be cut too, down to the point pages: these *forced splits* can leave pages nearly empty, so the k-d-B tree has no bound on the fill of its pages. Robinson proposed it in 1981.

## In plain words

A B-tree keeps sorted keys in pages on disk, with every leaf at the same depth, so a search reads few pages. A k-d tree cuts space into boxes by lines, but its leaves can be at very different depths.

A k-d-B tree mixes the two. Each page covers a box. A top page lists smaller boxes that cover it with no gaps, and says which page holds each one. The bottom pages hold the points.

When a page gets too full, cut its box in two with a straight line. Sometimes the line also cuts the boxes below it, which then must be cut too. This keeps the tree level, but some pages can end up almost empty.

## The abstract type

The k-d-B tree is a [spatial index](/spatial-index/) for points in $k$ dimensions on disk. It supports `insert(p)`, `delete(p)`, exact match `p in T`, and `range_search(lo, hi)`, which reports the points in a box; partial match and nearest neighbor queries work as in a k-d tree. It is meant for the [external memory model](/external-memory-model/), with a page as one disk block.

## Representation

The code and the example are in two dimensions. Each page $u$ has a region, a box $[lo, hi)$ that is half-open on each axis; the root's region is the whole plane.

- A **point page** holds a list of at most $B$ points, all in its region.
- A **region page** holds a list of between 1 and $M$ child pages. Their regions partition the region of $u$: they are disjoint and their union is the region of $u$.

All point pages are at the same depth. In the paper a region page stores, for each entry, the box and the page number; in the code each page carries its own box.

**Invariant (K).** (1) The regions of the children of each region page partition its region. (2) Each point lies in the region of its point page, and is stored once. (3) All point pages are at the same depth. (4) A point page holds at most $B$ points and a region page between 1 and $M$ children.

By part 1, each point of the plane lies in the region of exactly one page at each level, so an exact match query follows one path. There is no lower bound on how full a page is: a point page may even be empty. The partition of a region page is *guillotine*: it can be cut by a line that crosses no child, and each side again, until single children remain, since all regions come from cuts of the root by lines.

## Operations

```pseudo id=main
INSERT(T, p)
L1  path ← the pages from the root to the point page whose region holds p
L2  add p to that point page
L3  for each page u on the path, from the bottom up:
L4      if u is within capacity then stop
L5      choose a cut x_a = v: for a point page, the median of the distinct values of the axis of larger spread; for a region page, a child boundary that balances the two halves and cuts the fewest children, with each half at most M
L6      SPLIT(u, a, v) into two pages ℓ and r
L7      if u is the root then make a new root with the children ℓ and r, and stop
L8      replace the entry of u in its parent by the two entries ℓ and r
L9      go on with the parent

SPLIT(u, a, v)                             ▷ cut u by the line x_a = v
    if u is a point page: ℓ gets the points with x_a < v, r those with x_a ≥ v
    else for each child c of u:
        if c lies left of the line then c goes to ℓ; if right, to r
        else SPLIT(c, a, v), and its two halves go to ℓ and r     ▷ a forced split

RANGE-SEARCH(lo, hi)
L10 push the root on a stack; while it is not empty: pop u
L11     if the region of u does not meet the box then skip u
L12     if u is a point page then report its points that lie in the box
L13     else push the children of u
```

```pseudo id=delete
DELETE(T, p)
L14 find the point page whose region holds p
L15 remove p from it, if it is there
```

A forced split cuts a child into two pages at the same level, and each of those has as many children as the child had, at most. So the halves of the page fit, and the depth of the point pages does not change. Pages whose union is a box can also be merged after deletions; the code here does not merge.

## Example

Take $B = 1$ point per point page and $M = 4$ entries per region page, and insert five points.

| insert | what happens | tree after |
|---|---|---|
| (3,1) | the root is a point page with room | one page: (3,1) |
| (5,1) | the page overflows; the $x$ spread is 2 and the $y$ spread is 0, so cut at $x = 5$; a new root | root: $x < 5$: (3,1); $x \ge 5$: (5,1) |
| (5,8) | the page $x \ge 5$ overflows and is cut at $y = 8$ | root: $x < 5$; $x \ge 5, y < 8$: (5,1); $x \ge 5, y \ge 8$: (5,8) |
| (7,7) | the page of (5,1) overflows and is cut at $y = 7$ | root with 4 entries: $x < 5$: (3,1); $x \ge 5, y < 7$: (5,1); $x \ge 5, 7 \le y < 8$: (7,7); $x \ge 5, y \ge 8$: (5,8) |
| (7,8) | the page of (5,8) overflows and is cut at $x = 7$; now the root has 5 entries and must be split | see below |

The root's entries are now $A$: $x < 5$; $C$: $x \ge 5, y < 7$; $D$: $x \ge 5, 7 \le y < 8$; $E$: $5 \le x < 7, y \ge 8$; $F$: $x \ge 7, y \ge 8$. The cut $x = 5$ crosses no entry, but leaves 1 entry on one side and 4 on the other. The cut $y = 8$ leaves $A$, $C$, $D$ below and $A$, $E$, $F$ above, 3 and 3, so it is chosen, and it crosses $A$. The forced split cuts $A$ into $x < 5, y < 8$, which keeps (3,1), and $x < 5, y \ge 8$, which is empty. The new root has two region pages, each with 3 point pages, and the height is 2.

- **Range** $[4, 6] \times [0, 9]$: both halves of the root meet the box; in them, the pages $C$ and $E$ hold the points (5,1) and (5,8) in the box, and $A$'s halves, $D$ and $F$ give nothing. The answer is (5,1), (5,8).
- **Delete** (3,1): its page is now empty too, and the tree keeps its shape, with two empty point pages out of six.

## Correctness

SPLIT cuts a page into two pages whose regions are the two sides of the line; each child goes to the side that holds it, and a child that crosses the line is cut by the same rule, so part 1 holds in both halves, and each point goes to the half that holds it. A forced split keeps a page at its level, so part 3 holds. The cut chosen in line L5 exists because the partition is guillotine. A search goes down the one path whose regions hold the point, and RANGE-SEARCH skips only pages whose region misses the box. The full proof is in the proofs folder.

## Complexity

In the external memory model, each page is one disk access.

- **Height.** All point pages are at depth $h$. In the best case pages are full and $h = O(\log_M (n/B))$. With forced splits and no merging, pages can be nearly empty, and Robinson's paper gives no bound on the fill; so $h$ is bounded in terms of the number of pages, not of $n$.
- **Lookup.** One page per level, $h + 1$ disk accesses, and $O(M)$ work in memory per region page to find the child.
- **Insert.** One path of reads and writes, plus the forced splits, which write $s$ extra pages below the cut region page. Choosing the cut in line L5 tries $O(M)$ candidate lines and counts the children on each side, $O(M^2)$ per page in the simple form here.
- **Delete.** $O(h)$ pages; without merging, the tree never shrinks.
- **Range search.** As in a k-d tree, the pages visited are those whose regions meet the box. For a tree of full pages and a range that holds $t$ points, this is about $O((n/B)^{1 - 1/k} + t/B)$ pages for a k-d tree split pattern in $k$ dimensions; with underfull pages it is more.
- **Space.** Each point is stored once, but the number of pages can exceed $n/B$ by a large factor when forced splits make many empty pages.

| operation | time | case |
|---|---|---|
| lookup | $O(h M)$, $h + 1$ disk accesses | worst |
| insert | $O(h M^2 + s)$ | worst |
| delete | $O(h M + B)$ | worst |
| range_search | $O(vM + vB)$ | worst, $v$ pages visited |
| space | $O(n)$ points, pages not bounded by $n/B$ | total |

## Variants

- **Cut choices.** Robinson considered cuts at the median of the points, which keep the point pages full but can cause forced splits, and cuts that cross no child, which avoid forced splits but can leave a region page with one child on one side. The code here balances first and breaks ties by the number of crossed children.
- **The hB-tree.** Lomet and Salzberg let the region of a page be a box with holes, described by a small k-d tree inside the page. A page can then always be split without crossing its children, which removes forced splits and gives a guaranteed fill.
- **The LSD-tree and the Bkd-tree.** The LSD-tree of Henrich and others pages a k-d tree in a different way, with no forced splits. The Bkd-tree keeps a set of static k-d trees of sizes in powers of two, each [bulk loaded](/bulk-loading/), and merges them on insertion, which gives full pages and good update cost.
- **Bulk loading.** For static data, a k-d-B tree built top down by median cuts has full pages and no forced splits.
- **Higher dimensions.** The same structure works in any dimension $k$, with cuts on any of the $k$ axes.

## When to use it

Use a k-d-B tree for points with a few keys on disk when the data changes and range queries matter, and when a flat directory such as the [grid file](/grid-file/) would grow too much on correlated data. Its region pages adapt to the data, as the cuts of a k-d tree do, and its balance keeps the number of disk accesses per lookup equal to the height. When good page fill is important, prefer the hB-tree or a Bkd-tree; for rectangles, use an [R-tree](/r-tree/).

## Pitfalls

- **Forced splits.** A cut that balances a region page can cross many of its children, and the cut goes down to the point pages. Each crossed point page may become empty. Count the crossed children when choosing the cut, as line L5 does.
- **Equal coordinates.** If more than $B$ points are equal, no cut separates them. Store the points as a set, or allow overflow chains for duplicates.
- **Cut at a child boundary.** A region page must be cut at a line that leaves each side at most $M$ entries, counting the halves of crossed children on both sides. A cut at the median of the children's corners alone can fail this.
- **Open regions.** The root region is the whole space. With finite bounds, points outside the bounds have no page; with infinite bounds, take care when comparing.

## Implementations

## History

Robinson presented the K-D-B-tree at SIGMOD in 1981, as a way to page the k-d tree of Bentley with the balance of the B-tree of Bayer and McCreight. Its forced splits and poor page fill led to the hB-tree of Lomet and Salzberg in 1990, the LSD-tree, and much later the Bkd-tree. Samet's book and the survey of Gaede and Günther describe it among the bucket methods with tree directories.

## References
