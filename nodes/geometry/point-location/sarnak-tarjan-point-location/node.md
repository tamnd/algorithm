---
tag: SN1BV9
kind: algorithm
slug: sarnak-tarjan-point-location
name: Sarnak-Tarjan point location
aliases:
- persistent search tree point location
- planar point location by persistent search trees
- persistent slab method
area: geometry/point-location
level: advanced
summary: Sweep the subdivision and store the active edges in a persistent search tree so each query is a binary search.
solves: [planar-point-location, vertical-ray-shooting]
model: real-ram
complexity:
  vars: {n: the number of segments of the subdivision}
  time: {build: O(n log n) worst case, query: O(log n) worst case}
  space: {extra: O(n) worst case, path-copying: O(n log n) worst case}
properties: {online: false, deterministic: true, recursive: true, static: true}
history:
  year: 1986
  people: [Neil Sarnak, Robert E. Tarjan]
  note: Sarnak and Tarjan published planar point location using persistent search trees in Communications of the ACM in 1986, with O(n) space and O(log n) query time.
prereqs: [slab-method-point-location, persistent-binary-search-tree, path-copying, node-copying]
see_also: [persistent-red-black-tree, dsst-persistence-theorem, partial-persistence, fat-node, trapezoidal-map, kirkpatrick-point-location, chazelle-monotone-point-location, sweep-line-technique]
sources:
  - paper: doi:10.1145/6138.6151
    title: Neil Sarnak and Robert E. Tarjan, Planar point location using persistent search trees, Communications of the ACM 29(7), 1986
    locator: the whole paper (the persistent slab sweep, node copying for red-black trees and the O(n) space bound)
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: Section 2, node copying for partial persistence, and the application to point location
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 6, Notes and Comments (persistent search trees for point location)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 38, Point location, by Jack Snoeyink, Section 38.3 and Table 38.3.1
---

Sarnak and Tarjan's method solves [planar point location](/planar-point-location/) by making the [slab method](/slab-method-point-location/) small. A sweep from left to right keeps the segments that cross the sweep line in a balanced search tree. The tree after the sweep passes vertex $i$ is exactly the slab list of slab $i$, and a [persistent search tree](/persistent-binary-search-tree/) keeps every one of these versions. With node copying the versions need $O(n)$ space in total, the build takes $O(n \log n)$ time, and a query is a search in one version, in $O(\log n)$ time. All three bounds are worst case.

## In plain words

The slab method keeps a full sorted list of streets for each vertical strip of the map. Two neighboring strips have almost the same list: only the streets that start or end at the corner between them differ. So it wastes space to store each list in full.

This method keeps one sorted tree of streets and moves it from left to right across the map. At each corner it removes the streets that end there and adds those that start there. It never throws an old tree away. Instead, each change makes a new version that shares almost all of its parts with the old one. To answer a query, it finds the right strip and searches the version of the tree that belongs to that strip.

## The problem

**Notation.** $P$ is the set of vertices (segment end points), $n$ the number of segments, $p = (x, y)$ a point, and $d = 2$. $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$, positive when $p, q, r$ turn counterclockwise. A query has output size $h = 1$. The predicate $\mathrm{incircle}$ is not used.

The input is a set of $n$ segments that meet only at shared end points: a [planar subdivision](/planar-subdivision/) given by its edges. A query point $q$ gets the vertex $q$, the segment that contains $q$, or the face answer (above, below): the segments hit by the vertical rays up and down from $q$. This is the canonical answer of [vertical ray shooting](/vertical-ray-shooting/).

**Degenerate input.** As in the slab method, a symbolic shear $(x, y) \mapsto (x + \varepsilon y, y)$ makes all sheared $x$-coordinates distinct and no segment vertical. In code, points are compared in lexicographic order and above and below are decided by $\mathrm{orient}$, which the shear does not change. Vertical segments, vertices with equal $x$ and queries on edges or vertices need no special case.

## The algorithm

Each segment $(a, b)$ is stored with $a <_{\mathrm{lex}} b$. The search tree is ordered by the vertical order of the segments in the current slab, computed with $\mathrm{orient}$ as in the slab method.

```pseudo id=main
ST-BUILD(S)
L1  X[0 .. m−1] ← the distinct end points of S, in lexicographic order
L2  T ← the empty persistent search tree
L3  for i ← 0 to m − 2 do
L4      for each segment that ends at X[i] do T ← DELETE(T, segment)
L5      for each segment that starts at X[i] do T ← INSERT(T, segment)
L6      R[i] ← T                       ▷ the version for slab (X[i], X[i+1])
ST-QUERY(q)
L7  if q = X[j] for some j then return the vertex X[j]
L8  find i with X[i] < q < X[i+1]; if there is none then return the face with no segment above or below
L9  walk down R[i]: at a node s = (a, b), if orient(a, b, q) = 0 return the segment s; if it is positive, record s as below and go right, else record s as above and go left
L10 return the face between the recorded segments (above, below)
```

- **Lines L4 and L5.** The deletions come first. Just left of $X[i]$, the segments that end at $X[i]$ and the other active segments are all in one slab, so the comparator is valid. Just right of $X[i]$, the remaining segments and the new ones are in one slab. So every comparison is made between segments that span a common slab.
- **Line L6** keeps a pointer to the current root. The update operations never change an old node. With path copying, each update creates the $O(\log n)$ nodes on its search path and the rotations. With node copying (the original method), each node has one spare pointer slot with a time stamp, and an update copies a node only when its slot is full.
- **Line L8** is a binary search in $X$, as in the slab method.
- **Line L9** is a search in a binary search tree. The last node at which the walk went right is the highest segment below $q$, and the last node at which it went left is the lowest segment above $q$.

The Python implementation uses path copying on an [AVL tree](/avl-tree/). It is simpler, and its space is $O(n \log n)$; the Complexity section explains how node copying reaches $O(n)$.

## Example

The subdivision is the one of the slab method page: $s_0 = (0,0)(8,2)$, $s_1 = (4,6)(8,2)$, $s_2 = (0,0)(4,6)$ and $s_3 = (2,8)(10,6)$, with $X = [(0,0), (2,8), (4,6), (8,2), (10,6)]$. Trees are written as (left key right), and a dot is an empty tree.

| event $X[i]$ | deletions | insertions | version $R[i]$ | in-order |
|---|---|---|---|---|
| $(0,0)$ | none | $s_0, s_2$ | $(.\ s_0\ (.\ s_2\ .))$ | $s_0, s_2$ |
| $(2,8)$ | none | $s_3$ | $((.\ s_0\ .)\ s_2\ (.\ s_3\ .))$, after a left rotation | $s_0, s_2, s_3$ |
| $(4,6)$ | $s_2$ | $s_1$ | $((.\ s_0\ .)\ s_1\ (.\ s_3\ .))$ | $s_0, s_1, s_3$ |
| $(8,2)$ | $s_0, s_1$ | none | $(.\ s_3\ .)$ | $s_3$ |

Each in-order list equals the slab list of the slab method, but the four versions together were built from $14$ created nodes, and they share subtrees. For $q = (4, 7)$, which has the $x$ of the vertex $(4, 6)$ but is lexicographically larger, line L8 picks slab 2. At the root $s_1 = (4,6)(8,2)$, $\mathrm{orient} = 4 > 0$, so $s_1$ is below and the walk goes right. At $s_3 = (2,8)(10,6)$, $\mathrm{orient}((2,8),(10,6),(4,7)) = 8 \cdot (-1) - (-2) \cdot 2 = -4 < 0$, so $s_3$ is above. The answer is the face between $s_1$ (below) and $s_3$ (above). The test file checks these numbers.

## Correctness

**Theorem.** For every set of segments that meet only at shared end points and every query point $q$, ST-QUERY returns the same answer as the slab method: the vertex $q$, the segment that contains $q$, or the lowest segment above and the highest segment below $q$ in the sheared plane.

The key invariant: after line L6 for index $i$, the in-order sequence of $R[i]$ is the set of segments that span the slab $(X[i], X[i+1])$, sorted from bottom to top, and no later update changes $R[i]$. The first half is the sweep invariant of the slab method, proved for insertions into a sorted sequence; a balanced search tree is a sorted sequence with $O(\log n)$ updates. The second half is persistence: updates create new nodes and never write to old ones. The query is then a search in a binary search tree whose in-order is the slab order, and the monotonicity of "$q$ is above $s$" along that order gives the answer. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Build time.** Line L1 sorts at most $2n$ points. Each segment is inserted once and deleted once, and each update in a balanced tree of at most $n$ keys costs $O(\log n)$ comparisons, each one orientation test. So the build takes $O(n \log n)$ time in the worst case on the [real RAM](/real-ram/).
- **Space with path copying.** Each update copies the nodes on one root-to-leaf path and the $O(1)$ nodes touched by rotations, so it creates $O(\log n)$ nodes. With $2n$ updates the space is $O(n \log n)$ in the worst case. This is what the Python code does, and the tests check that the quadratic family of the slab method uses at most $4 n \lceil \log_2 (n+1) \rceil$ nodes.
- **Space with node copying.** In a red-black tree, an insertion or deletion makes $O(1)$ rotations in the worst case and $O(1)$ amortized color changes, and old versions are only searched, so their colors are not needed. Sarnak and Tarjan give each node one extra pointer field with a version stamp. A change of a pointer fills the extra field, and a full node is copied, which changes one pointer of its parent, and so on. A potential argument (the number of full live nodes) shows that each update creates $O(1)$ amortized new nodes, so the $2n$ updates create $O(n)$ nodes. The total space $O(n)$ is a worst-case bound for the whole structure. The general form is the [DSST persistence theorem](/dsst-persistence-theorem/) for [node copying](/node-copying/).
- **Query time.** Line L8 costs $O(\log n)$, and line L9 walks one root-to-leaf path of a tree of height $O(\log n)$. With node copying, each step picks one of at most two pointer values by its version stamp in $O(1)$. So a query takes $O(\log n)$ time in the worst case, which matches the $\Omega(\log n)$ lower bound of [planar point location](/planar-point-location/) in the [algebraic decision tree](/algebraic-decision-tree/) model.

## Properties

- **Optimal in all three measures.** $O(n \log n)$ build, $O(n)$ space and $O(\log n)$ query, all deterministic and worst case.
- **No triangulation needed.** It works on any set of non-crossing segments, including faces with holes and dangling edges.
- **Static.** A version for an old slab is never updated, so a new segment would need a new sweep.
- **Exact.** It uses only lexicographic comparisons and the orientation test.

## Variants and improvements

- **Path copying.** Copy whole search paths, as the Python code does. It is simpler and works on any balanced tree, at $O(n \log n)$ space.
- **Fat nodes.** Store all versions of each field in a sorted list inside the node; see [fat node](/fat-node/). The space is $O(n)$, but each step of a query needs a binary search in a field list, so a query takes $O(\log^2 n)$.
- **Cole's method.** Richard Cole (1986) obtained the same bounds by storing the slab lists as a sequence of similar lists, without the persistent tree framework.
- **Other optimal methods.** [Kirkpatrick's hierarchy](/kirkpatrick-point-location/) (1983), the chain method with fractional cascading of Edelsbrunner, Guibas and Stolfi (1986), see [monotone point location](/chazelle-monotone-point-location/), and the randomized [trapezoidal map](/trapezoidal-map/) all have $O(n)$ space and $O(\log n)$ query. Sarnak and Tarjan report smaller constants than the hierarchy.

## When to use it

Use it when the subdivision is static, the input is a list of segments with no triangulation or face structure, and deterministic worst-case bounds matter. It is a sweep, so it fits well with programs that already do a [plane sweep](/sweep-line-technique/). If a library has a persistent balanced tree, path copying gives a short implementation with $O(n \log n)$ space. For a structure that is easy to update, use the [trapezoidal map](/trapezoidal-map/), which supports insertions.

## Pitfalls

- **Inserting before deleting.** If line L5 runs before line L4 at a vertex, a segment that starts at $X[i]$ is compared with one that ends there, and the comparator can give the wrong order, since the two do not span a common slab. Run line L4 first.
- **Mutating a shared node.** A rebalancing step that changes a node in place, as in a usual AVL or red-black tree, corrupts all older versions that share the node. Every change in lines L4 and L5 must create new nodes.
- **Storing the colors in old versions.** With node copying on a red-black tree, the color changes of an update can touch $\Theta(\log n)$ nodes. Keep the colors only in the newest version, or the space bound is lost.
- **Equal $x$.** Building versions only at distinct $x$ values merges several events into one and loses the slabs between vertices with equal $x$. Sort the vertices in lexicographic order in line L1, which is the symbolic shear.

## Implementations

## History

Neil Sarnak and Robert Tarjan published the method in Communications of the ACM in 1986. It took the slab method of Dobkin and Lipton (1976), whose space is quadratic, and observed that the slab lists are the versions of one sorted list that changes by one insertion or deletion at a time. Their node copying technique for red-black trees gave $O(n)$ space and $O(\log n)$ query time. In the same year Richard Cole gave a different solution of the same problem of storing similar lists. Driscoll, Sarnak, Sleator and Tarjan then turned node copying into a general method for making linked data structures persistent (Journal of Computer and System Sciences, 1989).

## References
