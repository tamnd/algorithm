---
tag: 45BF01
kind: data-structure
slug: link-cut-tree
name: Link-cut tree
aliases:
- LCT
- Sleator-Tarjan link-cut tree
- Sleator-Tarjan trees
- link-cut trees
area: graphs/dynamic-graphs
level: advanced
summary: Represents a dynamic forest with splay trees, giving O(log n) amortized link, cut and path queries.
implements: [dynamic-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {amortized: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [splay-tree, rooted-tree, dynamic-tree]
see_also: [euler-tour-tree, top-tree, dynamic-tree-path-queries, heavy-light-decomposition, lowest-common-ancestor, dinic, network-simplex, dynamic-minimum-spanning-tree]
sources:
  - paper: doi:10.1016/0022-0000(83)90006-5
    title: Daniel D. Sleator and Robert E. Tarjan, A data structure for dynamic trees, Journal of Computer and System Sciences 26(3), 362 to 391 (1983)
    locator: the whole paper (paths partitioned into solid paths, kept in biased search trees; O(log n) amortized and worst-case bounds; application to maximum flow)
  - paper: doi:10.1145/3828.3835
    title: Daniel D. Sleator and Robert E. Tarjan, Self-adjusting binary search trees, Journal of the ACM 32(3), 652 to 686 (1985)
    locator: Section 6 (link-cut trees with splay trees; the access lemma gives O(log n) amortized time per operation)
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms, SIAM (1983)
    locator: Chapter 5, Linking and cutting trees
---

A link-cut tree stores a forest whose trees change by adding and removing edges, and answers questions about the path between two vertices, such as its sum, its minimum or its maximum. It splits each tree into vertex-disjoint paths and keeps each path in a [splay tree](/splay-tree/) ordered by depth; one operation, access, moves the path from the root to any vertex into a single splay tree. Every operation takes $O(\log n)$ amortized time. Sleator and Tarjan introduced the structure in 1981 to speed up [maximum flow algorithms](/dinic/), and it is the standard tool for path queries in a [dynamic tree](/dynamic-tree/).

## In plain words

Picture each tree hanging from its root. Cut it into vertical paths, so that each vertex belongs to exactly one path. Each path is stored in its own small balanced list, sorted from top to bottom, and the top of each path remembers the vertex just above it.

To ask about the path from the root down to a vertex, the structure first makes that whole path one of the stored paths. It walks up from the vertex. At each place where it jumps to a new path, it cuts the lower part off that path and glues on the part it brought from below.

Now the root path is one list, and its total, maximum or length is at the top of the list. To make any vertex the root, reverse its root path. To link or cut an edge, change the pointer of one path top.

## The abstract type

The structure implements a [dynamic tree](/dynamic-tree/) (forest) on the vertices $0, \ldots, n-1$, each with a value from a set with an associative operation (here, integers with sum and maximum):

- $\mathrm{link}(u, v)$: add the edge $\{u, v\}$; $u$ and $v$ must be in different trees;
- $\mathrm{cut}(u, v)$: remove the edge $\{u, v\}$ of the forest;
- $\mathrm{make\_root}(v)$: make $v$ the root of its tree (also called evert);
- $\mathrm{find\_root}(v)$ and $\mathrm{connected}(u, v)$;
- $\mathrm{path\_sum}(u, v)$ and $\mathrm{path\_max}(u, v)$: the sum and the maximum of the values on the tree path from $u$ to $v$;
- $\mathrm{lca}(r, u, v)$: the [lowest common ancestor](/lowest-common-ancestor/) of $u$ and $v$ when the tree is rooted at $r$;
- $\mathrm{set\_value}(v, x)$.

The updates are fully dynamic: links and cuts in any order, as long as the graph stays a forest.

## Representation

Each tree of the forest is rooted. Each vertex has at most one **preferred child**, so the edges from vertices to their preferred children split the tree into vertex-disjoint vertical **preferred paths**. Each preferred path is stored in a splay tree whose symmetric order is the order by depth, top first. The splay trees and the pointers between them form one **virtual tree** per real tree.

Each vertex $x$ stores its two splay children, one parent pointer, a reversal bit and the sum and maximum of the values in its splay subtree. The parent pointer has two meanings. If $x$ is a child of $p$ in a splay tree, it points to $p$. If $x$ is the root of its splay tree, it is the **path-parent** pointer: it points to the real parent of the top vertex of the path, or to nothing if the path holds the root of the real tree. A vertex $x$ is a splay root exactly when its parent pointer is empty or its parent does not have $x$ as a child.

The reversal bit means "swap left and right in this whole subtree". It is pushed down lazily, so reversing a whole path costs $O(1)$.

**Invariant (L).** (1) For each splay tree, the symmetric order, read with the pending reversal bits applied, is a preferred path of the real tree, from its top to its bottom. (2) The parent pointer of each splay root is the real parent of the top of its path. (3) The sum and maximum at each vertex are those of its splay subtree.

## Operations

```pseudo id=main
ACCESS(v)                                   ▷ make root..v one preferred path, v at the splay root
L1  last ← nil
L2  x ← v; while x ≠ nil do
L3      SPLAY(x)
L4      x.right ← last; update the sums of x  ▷ the old lower part becomes its own path
L5      last ← x; x ← x.parent             ▷ jump to the path above
L6  SPLAY(v)

MAKE-ROOT(v)
L7  ACCESS(v)
L8  flip the reversal bit of v               ▷ reverse the path root..v

FIND-ROOT(v)
L9  ACCESS(v); r ← the leftmost vertex of the splay tree of v
L10 SPLAY(r); return r

LINK(u, v)                                  ▷ u and v are in different trees
L11 MAKE-ROOT(u); ACCESS(v)
L12 u.parent ← v                             ▷ a path-parent pointer

CUT(u, v)                                   ▷ {u, v} is a forest edge
L13 MAKE-ROOT(u); ACCESS(v)                  ▷ the splay tree of v is the path u, v
L14 v.left ← nil; u.parent ← nil; update the sums of v

PATH-SUM(u, v)
L15 MAKE-ROOT(u); ACCESS(v)
L16 return the sum stored at v
```

SPLAY$(x)$ is ordinary [splaying](/splaying/) inside the splay tree of $x$. It first pushes the reversal bits down along the path from the splay root to $x$, and a rotation at a splay root moves the path-parent pointer to the new splay root.

**Access** (lines L1 to L6) climbs from $v$ to the root of the real tree. In each step, line L3 brings $x$ to the root of its splay tree. Line L4 cuts off the part of the path below $x$ (the right subtree) and puts in its place the path from below, which ends at $v$. That old lower part keeps $x$ as its path-parent. Line L5 follows the path-parent pointer to the next path up. At the end the path from the root to $v$ is one splay tree, and $v$ is its splay root with no right child, because no vertex of that path is deeper than $v$.

**Make root** (lines L7 and L8). Rerooting a tree at $v$ reverses the parent relation on the path from the old root to $v$ and leaves every other parent unchanged. After the access, that path is exactly the splay tree of $v$, so a reversal bit at its root does the whole change.

**Find root** (lines L9 and L10) returns the shallowest vertex of the root path, the leftmost vertex of its splay tree. The splay in line L10 pays for the walk down.

**Link** (lines L11 and L12) makes $u$ the root of its tree, so $u$ is the top of its path and the root of its splay tree. Setting the path-parent of $u$ to $v$ hangs the whole tree of $u$ below $v$. The access of $v$ in line L11 is only for the time bound: it makes $v$ the root of its virtual tree, so the sizes grow only at $v$.

**Cut** (lines L13 and L14). After rerooting at $u$ and accessing $v$, the splay tree of $v$ holds the path from $u$ to $v$, which is the edge $u, v$. So $u$ is the left child of $v$ and nothing else is in that splay tree. Line L14 separates the two.

**Path queries** (lines L15 and L16). After rerooting at $u$ and accessing $v$, the splay tree of $v$ holds exactly the path from $u$ to $v$, and $v$ is its splay root, so the stored aggregate is the answer. Path maxima and other associative aggregates work the same way.

**Lowest common ancestor.** Make $r$ the root and access $u$. Then run the loop of an access of $v$: the last vertex $x$ reached in line L5 before the loop ends is the lowest common ancestor of $u$ and $v$.

## Example

Take seven vertices with the values $5, 3, 8, 1, 4, 7, 2$ for the vertices $0, \ldots, 6$, and link the edges $\{0,1\}$, $\{1,2\}$, $\{1,3\}$, $\{3,4\}$, $\{4,5\}$, $\{0,6\}$. The forest is the tree with the paths $6, 0, 1, 2$ and $1, 3, 4, 5$.

| operation | tree path | answer |
|---|---|---|
| path_sum(2, 5) | 2, 1, 3, 4, 5 | $8 + 3 + 1 + 4 + 7 = 23$ |
| path_max(6, 4) | 6, 0, 1, 3, 4 | $\max(2, 5, 3, 1, 4) = 5$ |
| lca(0, 2, 5) | | 1 |
| cut(1, 3) | | trees $\{0, 1, 2, 6\}$ and $\{3, 4, 5\}$ |
| connected(2, 5) | | false |
| path_sum(3, 5) | 3, 4, 5 | $1 + 4 + 7 = 12$ |
| link(2, 5) | | one tree again |
| path_sum(6, 3) | 6, 0, 1, 2, 5, 4, 3 | $2 + 5 + 3 + 8 + 7 + 4 + 1 = 30$ |

In the first query, MAKE-ROOT$(2)$ makes 2 the root, so the tree hangs from 2. ACCESS$(5)$ then climbs from 5 to 2 and leaves the vertices $2, 1, 3, 4, 5$ in one splay tree with 5 at its root; the other vertices 0 and 6 form a preferred path below 1, outside that splay tree. The sum stored at 5 is 23. For the lowest common ancestor, the tree is rooted at 0 and the access of 2 makes $0, 1, 2$ one path; the climb from 5 enters this path at 1.

## Correctness

The structure keeps invariant (L). An access changes only preferred children: in each step the vertex $x$ drops its old lower path and takes the path that comes from below, which starts at a child of $x$ because the path-parent of that path is $x$. So the splay trees still hold vertical paths ordered by depth, and the root path ends at $v$. Make root reverses one whole path, which matches the change of the parent relation. Link and cut change one path-parent pointer or one splay edge, and the paths and pointers around them stay correct. Every query reads an aggregate of a splay tree that holds exactly the wanted path. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| access, make root, find root | $O(\log n)$ amortized |
| link, cut | $O(\log n)$ amortized |
| path sum, path maximum, lowest common ancestor | $O(\log n)$ amortized |
| set value | $O(\log n)$ amortized |
| space | $\Theta(n)$ |

All bounds are amortized over any sequence of operations that starts from $n$ single vertices. The algorithm is deterministic.

- **Number of jumps.** Call an edge from $x$ to its child $c$ heavy if the subtree of $c$ holds more than half of the subtree of $x$, and light otherwise. Any root path has at most $\lg n$ light edges. In an access, each jump in line L5 makes a new preferred edge. A new light preferred edge costs at most $\lg n$ per access. A new heavy preferred edge replaces a light one, or is the first preferred edge of its vertex, so their number is at most the number of earlier light changes plus $n$ plus a term for each link and cut. So an access makes $O(\log n)$ jumps amortized.
- **Splay cost.** Give each vertex the weight 1 and let $s(x)$ be the number of vertices in its subtree of the virtual tree, and use the potential $\sum_x \lg s(x)$. By the access lemma of splay trees, splaying $x$ in its splay tree costs at most $3(\lg s(t) - \lg s(x)) + 1$ amortized, where $t$ is the splay root. In the virtual tree, $s$ of the path-parent is at least $s$ of the splay root below it, so the sum over the splays of one access telescopes to $3 \lg n + O(\text{jumps}) = O(\log n)$.
- **Updates.** A reversal bit does not change any $s(x)$. A link increases $s$ only at $v$, because $v$ is the root of its virtual tree after the access in line L11, so the potential grows by at most $\lg n$. A cut only decreases sizes.
- **Single operations** can take $\Theta(n)$ time, for example the first access to the bottom of a long path. Sleator and Tarjan (1983) also gave a form with biased search trees that has $O(\log n)$ amortized time and a more complex form with $O(\log n)$ worst-case time per operation; see the first source.
- **Space.** A constant number of fields per vertex.

## Variants

- **Rooted trees without evert.** If the trees are rooted and the root never changes, drop the reversal bit; then link makes a root a child of any vertex, cut removes the edge to the parent, and the aggregate is over the path from a vertex to its root, as in the original paper.
- **Edge values.** Store the value of an edge in a new vertex in the middle of the edge, or in the deeper end point when the root does not change. The [network simplex](/network-simplex/) method and [dynamic minimum spanning tree](/dynamic-minimum-spanning-tree/) structures for insertions use edge values: to insert an edge, find the heaviest edge of the cycle by a path maximum, then cut it.
- **Path updates.** A lazy add or assign bit, pushed down like the reversal bit, adds a value to every vertex of a path. This is what [Dinic's algorithm](/dinic/) needs to push flow along a path of residual capacities, giving $O(nm \log n)$ time.
- **Subtree aggregates.** Keep in each vertex also the sum over its virtual children (the splay trees that hang from it by path-parent pointers). Then subtree sums work too, but subtree updates do not; for both, use an [Euler tour tree](/euler-tour-tree/) or a [top tree](/top-tree/).
- **Biased search trees.** The 1983 paper stores each path in a biased search tree, weighted by the sizes of the subtrees that hang from it; this gives the same $O(\log n)$ amortized bound without splaying.

## When to use it

Use a link-cut tree when a forest changes by links and cuts and the questions are about paths: path sums, path minima or maxima, path updates, roots and lowest common ancestors. Typical uses are maximum flow with blocking flows, [network simplex](/network-simplex/), [dynamic minimum spanning trees](/dynamic-minimum-spanning-tree/) with insertions, and offline [dynamic connectivity](/dynamic-connectivity/) by maximum spanning forests over deletion times. If the tree does not change, [heavy-light decomposition](/heavy-light-decomposition/) is simpler and has worst-case bounds. If the questions are about subtrees or whole components, an [Euler tour tree](/euler-tour-tree/) is simpler. If an application needs each operation to be fast, not only on average, use a structure with worst-case bounds such as a [top tree](/top-tree/).

## Pitfalls

- **Testing for a splay root.** A vertex is a splay root if its parent is empty or if it is neither child of its parent. Testing only "parent is empty" mixes path-parent pointers with splay edges and breaks the structure at once.
- **Pushing reversal bits too late.** Before splaying $x$, push the reversal bits from the splay root down to $x$. Otherwise a rotation reads swapped children as unswapped ones.
- **Linking two vertices of one tree.** This creates a cycle in the virtual tree, and the next access loops forever. Check connectivity first.
- **Cutting a non-edge.** After line L13, check that $u$ is the left child of $v$ and has no right child; otherwise $\{u, v\}$ is not an edge.
- **Recursion.** A recursive push-down or splay can reach a depth of $\Theta(n)$ on the first access of a long path. Write both as loops.
- **Real-time use.** The bounds are amortized, so one operation can be slow. Do not use the structure where every operation has a deadline, or where operations are undone by [rollback](/rollback-technique/).

## Implementations

## History

Sleator and Tarjan presented dynamic trees at STOC 1981 and published them in the Journal of Computer and System Sciences in 1983, with biased search trees for the paths. They used them to make Dinic's blocking flow step run in $O(m \log n)$ time, which gives maximum flow in $O(nm \log n)$ time. In their 1985 paper on [splay trees](/splay-tree/), they replaced biased search trees by splay trees, which made the structure much simpler with the same amortized bound. Tarjan's 1983 book gives the splay-based form a full chapter. The structure was later extended to subtree aggregates and generalized by topology trees and top trees.

## References
