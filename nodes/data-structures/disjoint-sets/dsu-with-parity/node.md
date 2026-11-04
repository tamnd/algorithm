---
tag: PG396R
kind: technique
slug: dsu-with-parity
name: Union-find with parity (online bipartite check)
aliases:
- Support parity of path length / bipartite check online
area: data-structures/disjoint-sets
level: core
summary: A disjoint set union variant that stores each node's parity relative to its root, letting edges be added online while checking bipartiteness.
prereqs: [disjoint-set-forest, bipartite-graph]
see_also: [dsu-with-distances-to-representative, weighted-union-find, bipartiteness-testing, bipartite-graph-test, incremental-connectivity, union-find-with-rollback, offline-dynamic-connectivity]
sources:
  - url: https://cp-algorithms.com/data_structures/disjoint_set_union.html
    title: cp-algorithms, Disjoint Set Union
    locator: the section Support the parity of the path length / Checking bipartiteness online
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.3, Disjoint-set forests (the forest and the find that this technique extends)
---

Union-find with parity stores one bit on each edge of a [disjoint-set forest](/disjoint-set-forest/), so that each element knows the parity of its position relative to the root of its tree. Read as a 2-coloring, the bit says whether the element has the color of its root. When the edges of a graph arrive one at a time, the structure keeps a 2-coloring of each component and detects the first edge that closes an odd cycle, which makes the graph not [bipartite](/bipartite-graph/). Each edge costs $O(\alpha(n))$ amortized time. It is the case of [union-find with distances](/dsu-with-distances-to-representative/) where the numbers are bits and the sum is exclusive or.

## In plain words

You want to paint the points of a network black and white, so that each line joins a black point and a white point. The lines arrive one by one.

Keep the points in groups, as in union-find. In each group, every point knows only one thing: does it have the same color as its leader, or the other color? A new line between two groups joins them, and you choose the color of the smaller leader so that the two ends of the line differ. A new line inside one group needs no change if its two ends already differ. If they have the same color, no painting works any more, and you report that the network is not two-colorable.

## When it applies

- **Edges arrive and are never removed**, and after each one the question is whether the graph is still bipartite.
- **Facts of the form "same" or "different".** For example "$x$ and $y$ are on opposite teams", "$x_a \oplus x_b = 1$" for bits, or "these two are enemies, those two are friends". Each fact fixes the parity of the two elements relative to each other.
- **Only merges.** Deleting an edge needs [rollback](/union-find-with-rollback/) with an offline method such as [offline dynamic connectivity](/offline-dynamic-connectivity/).

## The template

Each element $x$ has a parent $x.p$ and a bit $x.b$, the parity of the edge from $x$ to $x.p$. Roots have $r.b = 0$. The parity $\mathrm{par}(x)$ is the exclusive or of the bits on the path from $x$ to its root.

```pseudo id=main
FIND(x)                                   ▷ returns (root, par(x)) and compresses
L1  if x.p = x then return (x, 0)
L2  (r, e) ← FIND(x.p)
L3  x.b ← x.b ⊕ e
L4  x.p ← r
L5  return (r, x.b)

ADD-EDGE(a, b, ⟨REL⟩)                     ▷ hole: REL = 1 for "differ", 0 for "same"
L6  (ra, pa) ← FIND(a); (rb, pb) ← FIND(b)
L7  if ra = rb then return pa ⊕ pb = ⟨REL⟩ ▷ false: the facts conflict
L8  if ra.size > rb.size then swap (ra, pa) and (rb, pb)
L9  ra.p ← rb; ra.b ← pa ⊕ pb ⊕ ⟨REL⟩
L10 rb.size ← rb.size + ra.size
L11 return true
```

For bipartiteness, every edge says "differ", so ⟨REL⟩ $= 1$, and the bit of line L9 is $pa \oplus pb \oplus 1$, the rule of cp-algorithms.

**Why the bit of line L9 is right.** After the link, each element $z$ of the old tree of $ra$ has $\mathrm{par}(z) = (\text{old par}(z)) \oplus ra.b$, and the elements of the tree of $rb$ keep their parities. So $\mathrm{par}(a) \oplus \mathrm{par}(b)$ becomes $pa \oplus ra.b \oplus pb = pa \oplus pb \oplus pa \oplus pb \oplus \langle REL \rangle = \langle REL \rangle$. The swap of line L8 does not matter, because $\oplus$ is symmetric.

**Why line L7 detects odd cycles.** Within one tree, $\mathrm{par}$ is a 2-coloring that satisfies all edges added so far, and every 2-coloring of a connected component is this one or its flip. An edge $(a, b)$ inside one component can be satisfied exactly when $\mathrm{par}(a) \ne \mathrm{par}(b)$. If they are equal, the tree path from $a$ to $b$ has even length, and with the edge it makes an odd cycle.

**Cost.** Each operation does $O(1)$ more work per step than the plain forest, so with union by size and compression, $m$ edges on $n$ vertices take $O(n + m\,\alpha(n))$ time.

## Classic examples

### A graph that stays bipartite until the last edge

Take the vertices $0$ to $5$ and add the edges below, with union by size (ties put the first root under the second). The tables show the arrays after each edge.

| edge | roots and parities | action | parents of 0 to 5 | bits of 0 to 5 |
|---|---|---|---|---|
| (0, 1) | 0 with 0, 1 with 0 | 0.p ← 1, 0.b ← 1 | 1 1 2 3 4 5 | 1 0 0 0 0 0 |
| (2, 3) | 2 with 0, 3 with 0 | 2.p ← 3, 2.b ← 1 | 1 1 3 3 4 5 | 1 0 1 0 0 0 |
| (1, 2) | 1 with 0, 3 with 1 | 1.p ← 3, 1.b ← 0 | 1 3 3 3 4 5 | 1 0 1 0 0 0 |
| (4, 5) | 4 with 0, 5 with 0 | 4.p ← 5, 4.b ← 1 | 1 3 3 3 5 5 | 1 0 1 0 1 0 |
| (3, 4) | 3 with 0, 5 with 1; size 4 > 2, swap | 5.p ← 3, 5.b ← 0 | 1 3 3 3 5 3 | 1 0 1 0 1 0 |
| (0, 3) | both root 3, parities 1 and 0 | consistent; find(0) compresses | 3 3 3 3 5 3 | 1 0 1 0 1 0 |
| (5, 0) | both root 3, parities 0 and 1 | consistent | 3 3 3 3 5 3 | 1 0 1 0 1 0 |
| (1, 3) | both root 3, parities 0 and 0 | odd cycle 1, 2, 3 | | |

After the seventh edge, the coloring by parity is $1, 0, 1, 0, 1, 0$ for the vertices $0$ to $5$, and each edge joins two colors. The edge $(1, 3)$ closes the triangle $1, 2, 3$, and the structure reports that the graph is no longer bipartite.

### Where it is used

- **[Bipartiteness testing](/bipartiteness-testing/) online.** A search such as the [BFS test](/bipartite-graph-test/) needs the whole graph, while this technique handles edges one at a time.
- **Bipartiteness under deletions.** With [union-find with rollback](/union-find-with-rollback/) in place of compression, and the [offline dynamic connectivity](/offline-dynamic-connectivity/) method, it answers "is the graph bipartite now?" after each insertion or deletion.
- **Parity equations.** A set of equations $x_a \oplus x_b = c$ over bits is consistent exactly when no ADD-EDGE returns false. This is the [weighted union-find](/weighted-union-find/) of the group of order 2.

## Variations

- **Two-coloring as a second copy.** Another common method keeps $2n$ elements, $x$ and $\bar x$, and for each edge $(a, b)$ unites $a$ with $\bar b$ and $\bar a$ with $b$. The graph is bipartite while no $x$ is in one set with $\bar x$. It needs no bits, but twice the space.
- **Iterative find.** With [path halving](/path-halving/), the update is $x.b \leftarrow x.b \oplus x.p.b$ before each skip.
- **Larger groups.** Replace the bit by a residue modulo $k$ for facts like "$x$ is $c$ steps after $y$ in a cycle of $k$ colors".

## Pitfalls

- **The wrong bit on the new edge.** Line L9 must use the parities $pa$ and $pb$ of the two endpoints, not $0 \oplus 1$. Setting $ra.b \leftarrow 1$ is right only when $a$ and $b$ are themselves roots.
- **Compression without the parity.** Line L3 must run before line L4. Pointing $x$ to the root with its old bit loses the bits of the skipped edges.
- **Stopping at the first conflict.** Once an odd cycle appears, the graph stays non-bipartite for all later edges. Code that reports only the result of the last edge must keep a flag.
- **Adding the edge after a conflict.** When line L7 returns false, nothing is linked, which is right: the structure still holds a valid coloring of each component, but it no longer describes the whole graph.

## Exercises

1. Prove that the coloring $\mathrm{par}$ satisfies every edge added before the first conflict.
2. Show that the two-copy method with $2n$ elements gives the same answers as the parity method.
3. Change the template so that, on a conflict, it returns the vertices of an odd cycle in $O(n)$ time.

## References
