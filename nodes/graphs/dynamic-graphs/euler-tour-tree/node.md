---
tag: TH5ZDM
kind: data-structure
slug: euler-tour-tree
name: Euler tour tree
aliases:
- ETT
area: graphs/dynamic-graphs
level: advanced
summary: Stores each tree as a balanced sequence of its Euler tour, supporting link, cut and subtree queries.
implements: [dynamic-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {expected: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [euler-tour-technique, treap, tree]
see_also: [link-cut-tree, top-tree, holm-de-lichtenberg-thorup, dynamic-tree, dynamic-connectivity, euler-tour-subtree-queries, implicit-treap, splay-tree]
sources:
  - paper: doi:10.1145/320211.320215
    title: Monika R. Henzinger and Valerie King, Randomized fully dynamic graph algorithms with polylogarithmic time per operation, Journal of the ACM 46(4), 502 to 516 (1999)
    locator: the section on ET-trees (Euler tour sequences of a spanning forest kept in balanced search trees)
  - paper: doi:10.1007/BF02614369
    title: Robert E. Tarjan, Dynamic trees as search trees via Euler tours, applied to the network simplex algorithm, Mathematical Programming 78, 169 to 177 (1997)
    locator: the whole paper (Euler tours of the arcs of a tree kept in search trees, with link, cut and reroot by split and join)
  - paper: doi:10.1145/502090.502095
    title: Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Poly-logarithmic deterministic fully-dynamic algorithms for connectivity, minimum spanning tree, 2-edge, and biconnectivity, Journal of the ACM 48(4), 723 to 760 (2001)
    locator: Section 2 (the use of ET-trees for the spanning forests of each level)
---

An Euler tour tree stores each tree of a dynamic forest as the sequence of an Euler tour of that tree, and keeps the sequence in a balanced search tree ordered by position. A cut of an edge and a link of two trees change the tour in a constant number of places, so each becomes a constant number of splits and joins of search trees, in $O(\log n)$ time. It answers whether two vertices are in the same tree and computes sums over a whole tree or over one side of an edge, but it cannot compute sums over a path; for paths, use a [link-cut tree](/link-cut-tree/). Henzinger and King (1995) introduced it for [dynamic connectivity](/dynamic-connectivity/), and it is the core of the [Holm-de Lichtenberg-Thorup algorithm](/holm-de-lichtenberg-thorup/).

## In plain words

Walk around a tree drawn on paper, from a start vertex until you come back. You cross each edge twice, once in each direction. Write down each step, and also write down each vertex once when you meet it. This list is the tour of the tree.

The list has a useful shape. If you cut one edge, the two crossings of that edge split the list into a piece in the middle and a piece on the outside, and these are exactly the tours of the two new trees. If you join two trees with a new edge, you start each tour at an end of the new edge and glue the tours together with the two crossings of the new edge.

So all changes are cuts and glues of lists. A balanced search tree does each cut or glue of a list fast.

## The abstract type

The structure implements a [dynamic tree](/dynamic-tree/) (forest) on the vertices $0, \ldots, n-1$, each with a value from a commutative group (here, integers under addition):

- $\mathrm{link}(u, v)$: add the edge $\{u, v\}$; $u$ and $v$ must be in different trees;
- $\mathrm{cut}(u, v)$: remove the edge $\{u, v\}$ of the forest;
- $\mathrm{connected}(u, v)$: are $u$ and $v$ in the same tree?
- $\mathrm{component\_size}(v)$ and $\mathrm{component\_sum}(v)$: the number of vertices and the sum of the values of the tree of $v$;
- $\mathrm{subtree\_sum}(v, p)$: for a forest edge $\{p, v\}$, the sum of the values of the vertices on the side of $v$ when the edge is removed, which is the subtree of $v$ if the tree is rooted at $p$;
- $\mathrm{set\_value}(v, x)$ and $\mathrm{reroot}(v)$.

All updates are fully dynamic: links and cuts in any order, as long as the graph stays a forest.

## Representation

Each vertex $v$ has a **loop node** $(v, v)$ with the value of $v$. Each forest edge $\{u, v\}$ has two **arc nodes** $(u, v)$ and $(v, u)$ with value 0. For each tree $T$ of the forest, the nodes of $T$ are kept in one [treap](/treap/), ordered by their position in a sequence $S(T)$; the treap has no keys, only positions, as in an [implicit treap](/implicit-treap/). Each treap node stores its subtree size, its number of loop nodes and the sum of its values, and a pointer to its parent, so that the position of a node and the root of its treap can be found by walking up.

**Invariant (E).** For each tree $T$ with vertex set $V_T$, the sequence $S(T)$, read cyclically, is an Euler tour of $T$:

1. the arc nodes of $S(T)$, in order, form a closed walk: each arc $(a, b)$ is followed cyclically by an arc $(b, c)$;
2. this walk uses each arc of $T$ exactly once, so it crosses each edge once in each direction;
3. $S(T)$ holds exactly one loop node $(w, w)$ for each $w \in V_T$, and, if $|V_T| \ge 2$, it lies cyclically between an arc into $w$ and an arc out of $w$.

A tree with one vertex has the sequence $(w, w)$. Because the sequence is read cyclically, every rotation of $S(T)$ also satisfies (E). For a tree with $k$ vertices the sequence has $k + 2(k-1) = 3k - 2$ nodes, so the forest uses at most $3n - 2$ nodes.

## Operations

```pseudo id=main
REROOT(v)                                   ▷ rotate S(T) to start at (v, v)
L1  (A, B) ← SPLIT(S(T), POS((v, v)))        ▷ A = the nodes before (v, v)
L2  return JOIN(B, A)

CONNECTED(u, v)
L3  return ROOT((u, u)) = ROOT((v, v))

LINK(u, v)                                  ▷ u and v are in different trees
L4  Su ← REROOT(u); Sv ← REROOT(v)
L5  create arc nodes a = (u, v) and b = (v, u)
L6  S ← JOIN(Su, a, Sv, b)

CUT(u, v)                                   ▷ {u, v} is a forest edge
L7  a ← (u, v); b ← (v, u)
L8  if POS(a) > POS(b) then swap a and b
L9  split S into X, a, Y, b, Z; delete a and b
L10 the new sequences are Y and JOIN(X, Z)

COMPONENT-SIZE(v)
L11 return the loop count at ROOT((v, v))

SUBTREE-SUM(v, p)                           ▷ the side of v of the edge {p, v}
L12 i ← POS((p, v)); j ← POS((v, p))
L13 if i < j then return the sum of positions i + 1 to j − 1
L14 else return the total − the sum of positions j + 1 to i − 1
```

**Reroot** (lines L1 and L2) is a rotation of the cyclic sequence. It costs one split and one join.

**Connected** (line L3) compares the treap roots of the two loop nodes. By (E), two vertices are in the same tree if and only if their loop nodes are in the same sequence.

**Link** (lines L4 to L6) rotates each tour to start at its endpoint and glues them as $S_u \, (u, v) \, S_v \, (v, u)$. The walk goes around the tree of $u$ back to $u$, crosses to $v$, goes around the tree of $v$ back to $v$, and crosses back to $u$.

**Cut** (lines L7 to L10) finds the two arc nodes of the edge. Lines L8 and L9 split the sequence around them into $X\,a\,Y\,b\,Z$. The walk enters one side of the edge with $a$ and leaves it with $b$, so $Y$ is the tour of that side and $X Z$ is the tour of the other side.

**Component aggregates** (line L11) read the counters at the root of the treap. **Subtree sums** (lines L12 to L14) use the same fact as cut: the tour of the side of $v$ is the cyclic segment strictly after $(p, v)$ and strictly before $(v, p)$. Prefix sums of a treap take $O(\log n)$ expected time by a walk down from the root.

**Set value** changes the value of a loop node and updates the sums on its path to the root.

## Example

Take six vertices $0, \ldots, 5$ with the values $1, 2, 3, 4, 5, 6$. The table writes a loop node $(w, w)$ as $w$ and an arc $(a, b)$ as $ab$.

| operation | sequences after it |
|---|---|
| link(0, 1) | 0 01 1 10 |
| link(1, 2) | 1 10 0 01 12 2 21 |
| link(1, 3) | 1 10 0 01 12 2 21 13 3 31 |
| link(3, 4) | 3 31 1 10 0 01 12 2 21 13 34 4 43 |
| cut(1, 3) | 1 10 0 01 12 2 21 and 3 34 4 43 |
| link(4, 5) | 4 43 3 34 45 5 54 |
| link(2, 5) | 2 21 1 10 0 01 12 25 5 54 4 43 3 34 45 52 |

In the link of $(1, 2)$, the tour of $\{0, 1\}$ is first rotated to start at the loop node 1, which gives $1\ 10\ 0\ 01$, and then $12\ 2\ 21$ is appended. Before the cut, $\mathrm{subtree\_sum}(3, 1)$ adds the values strictly between $13$ and $31$: the loop nodes 3 and 4, so $4 + 5 = 9$. The cut of $(1, 3)$ splits $3\ 31\ 1 \ldots 21\ 13\ 34\ 4\ 43$ at $31$ and $13$: here $(3, 1)$ comes first, the middle part $1\ 10\ 0\ 01\ 12\ 2\ 21$ is the tour of $\{0, 1, 2\}$, and the outer parts $3$ and $34\ 4\ 43$ join to the tour of $\{3, 4\}$. After the last link, all six vertices form one tree, with $\mathrm{component\_sum}(0) = 21$.

## Correctness

Each operation keeps invariant (E). A rotation keeps a cyclic sequence, so reroot keeps it. For link, the sequence $S_u\,(u, v)\,S_v\,(v, u)$ is a closed walk because $S_u$ starts with the loop node of $u$ and so ends, cyclically, with an arc into $u$, and the same holds for $v$; the new arcs are used once, and every loop node keeps an arc into and an arc out of its vertex on its two sides. For cut, the walk can move from one side of the edge $\{u, v\}$ to the other only through $a$ or $b$, so the segment $Y$ between them is a closed walk on one side that uses all its arcs, and $XZ$ is one on the other side. The queries read sums of sequences that (E) identifies with trees and sides. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time with a treap | with a red-black tree |
|---|---|---|
| link, cut, reroot | $O(\log n)$ expected | $O(\log n)$ worst case |
| connected | $O(\log n)$ expected | $O(\log n)$ worst case |
| component size or sum | $O(\log n)$ expected | $O(\log n)$ worst case |
| subtree sum | $O(\log n)$ expected | $O(\log n)$ worst case |
| set value | $O(\log n)$ expected | $O(\log n)$ worst case |
| space | $\Theta(n)$ | $\Theta(n)$ |

- **Depth.** A treap on $N$ nodes with independent random priorities has expected depth $O(\log N)$, and $N \le 3n - 2$, so each walk to the root and each walk down costs $O(\log n)$ expected. The bound holds against an [oblivious adversary](/oblivious-adversary/), because the priorities are hidden from the sequence of operations.
- **Split and join** each walk one root-to-leaf path, so each costs $O(\log n)$ expected. Link does 2 rotations and 3 joins, cut does 4 splits and 1 join, so each is $O(\log n)$ expected.
- **Worst case.** Any balanced search tree that supports split and join in $O(\log N)$ worst-case time, such as a red-black tree, gives $O(\log n)$ worst-case bounds; a [splay tree](/splay-tree/) gives $O(\log n)$ amortized.
- **Space.** Three nodes per vertex at most, each of constant size, plus a hash table from edges to arc nodes.

## Variants

- **Vertex occurrences instead of loop nodes.** The original form of Henzinger and King stores the sequence of vertex visits, in which a vertex of degree $d$ occurs $d$ times (the root once more). A vertex then needs a chosen representative occurrence that carries its value, and a cut must move the representative when it is deleted. Loop nodes avoid this.
- **Non-tree edge counts.** In dynamic connectivity, each loop node also stores how many non-tree edges of a level touch its vertex, and each treap node stores whether its subtree holds such a vertex. Then a search down the treap finds the next vertex with a non-tree edge in $O(\log n)$ time. This is how the [Holm-de Lichtenberg-Thorup algorithm](/holm-de-lichtenberg-thorup/) uses Euler tour trees.
- **Subtree updates.** Adding a value to every vertex of a subtree is a lazy addition on the segment between $(p, v)$ and $(v, p)$.
- **Static form.** Without updates, an array of the tour with [prefix sums](/prefix-sums/) gives subtree sums in $O(1)$; see [subtree queries by Euler tour](/euler-tour-subtree-queries/).

## When to use it

Use an Euler tour tree when the queries are about whole trees or about subtrees, such as connectivity, component sizes and subtree sums, and the forest changes by links and cuts. It is simpler than a link-cut tree, and with a balanced search tree it gives worst-case bounds. Use a [link-cut tree](/link-cut-tree/) when you need sums or minima along paths, or the lowest common ancestor. Use a [top tree](/top-tree/) when you need both path and subtree information, or non-local queries such as the diameter.

## Pitfalls

- **Cutting without ordering the arcs.** Line L8 must compare the positions of $(u, v)$ and $(v, u)$. If the code always splits at $(u, v)$ first, a tour in which $(v, u)$ comes first gives the wrong pieces.
- **Linking two vertices of one tree.** Line L6 then creates a sequence that is not an Euler tour, and every later answer about that tree can be wrong. Check $\mathrm{connected}(u, v)$ first.
- **Stale parent pointers.** Split and join must clear the parent pointer of each new root. A root with an old parent pointer makes $\mathrm{connected}$ walk into a treap of another tree.
- **Expecting path queries.** The vertices of a tree path are not contiguous in the tour, so an Euler tour tree cannot sum a path in $O(\log n)$ time.

## Implementations

## History

Henzinger and King introduced Euler tour trees in their randomized fully dynamic connectivity algorithm, first presented at STOC 1995 and published in the Journal of the ACM in 1999. Tarjan (1997) described the form that stores the arcs of the tour in a search tree, and applied it to the network simplex algorithm. Holm, de Lichtenberg and Thorup (2001) keep one Euler tour forest per level in their deterministic polylogarithmic algorithm for dynamic connectivity.

## References
