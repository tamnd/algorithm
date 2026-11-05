---
tag: 6AA8GQ
kind: algorithm
slug: online-bridge-finding
name: Online bridge finding
aliases:
- Finding bridges online
area: graphs/dynamic-graphs
level: advanced
summary: Algorithm that maintains the bridges of a graph while edges are added, using union-find and a spanning forest with path compression.
solves: [bridge-finding]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of inserted edges}
  time: {amortized: O(log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [bridge, two-edge-connected-components, disjoint-set-forest, incremental-graph]
see_also: [bridge-finding, incremental-connectivity, dynamic-biconnectivity, union-by-size, path-compression, link-cut-tree, offline-dynamic-connectivity, lowest-common-ancestor]
sources:
  - url: https://cp-algorithms.com/graph/bridge-searching-online.html
    title: cp-algorithms, Finding bridges online
    locator: the whole article (2-edge-connected components in a union-find, the forest of bridges, rerooting the smaller tree, merging the path through the lowest common ancestor)
  - paper: "Jeffery Westbrook and Robert E. Tarjan, Maintaining bridge-connected and biconnected components on-line, Algorithmica 7, 433 to 464 (1992)"
    locator: the main theorem (insertions of edges in O(α(m, n)) amortized time per operation for bridge-connected components)
  - paper: "Robert E. Tarjan, A note on finding the bridges of a graph, Information Processing Letters 2(6), 160 to 161 (1974)"
    locator: the whole note (the static linear-time algorithm used as the oracle)
---

Online bridge finding keeps the set of [bridges](/bridge/) of an undirected graph while edges are inserted one at a time, and can report after each insertion how many bridges there are and whether two vertices are 2-edge-connected. It keeps the [2-edge-connected components](/two-edge-connected-components/) in a union-find; contracted, they form a forest whose edges are exactly the bridges. A new edge between two trees becomes a bridge, and a new edge inside one tree closes a cycle, so every bridge on the tree path between its ends stops being a bridge and the path collapses into one component. The method supports insertions only, is deterministic, and takes $O(\log n)$ amortized time per insertion, up to a factor $\alpha(n)$.

## In plain words

A bridge is an edge whose removal splits the graph. Adding edges can only remove bridges or create new ones in one way, so the method keeps a simple picture.

Squeeze each group of vertices that hold together without any bridge into one blob. The blobs and the bridges form a forest, like a set of trees.

When a new edge joins two different trees, it is a new bridge. Hang the smaller tree below the other one; to do so, first turn the smaller tree so that the end of the new edge is at its top.

When a new edge joins two blobs of the same tree, it closes a loop. Every bridge on the tree path between the two blobs is now on a loop, so it is not a bridge. Squeeze all blobs of that path into one blob.

## The problem

The input is a number $n$ of vertices and a sequence of edge insertions $\{u_1, v_1\}, \{u_2, v_2\}, \ldots$, given one at a time; loops and parallel edges are allowed. After each insertion the algorithm must answer, before it reads the next one:

- the number of bridges of the current graph;
- whether two given vertices are 2-edge-connected, that is, in one 2-edge-connected component;
- whether a given inserted edge is a bridge;
- whether two vertices are connected.

This is the [incremental](/incremental-graph/) form of [bridge finding](/bridge-finding/). Insertions can only make the 2-edge-connected components larger: each new edge either adds a bridge between two connected components or merges components.

## The algorithm

The structure has three parts:

- a union-find $E$ on the vertices whose sets are the 2-edge-connected components, with union by size and path compression; a component is named by its representative;
- for each representative $a$, a pointer $\mathrm{par}(a)$ to some vertex of the parent component in the **bridge forest**, or nil at a root; the parent component is $E.\mathrm{find}(\mathrm{par}(a))$;
- a union-find $C$ whose sets are the connected components, with the number of vertices of each, and a counter of bridges.

```pseudo id=main
ADD-EDGE(u, v)
L1  a ← E.FIND(u); b ← E.FIND(v); if a = b then return       ▷ inside one component
L2  ca ← C.FIND(a); cb ← C.FIND(b)
L3  if ca ≠ cb then bridges ← bridges + 1                        ▷ a new bridge
L4      if |ca| > |cb| then swap (a, ca) with (b, cb)
L5      REROOT(a); par(a) ← b; C.UNION(ca, cb)
L6  else MERGE-PATH(a, b)

MERGE-PATH(a, b)                            ▷ a and b are in one tree of the forest
L7  climb from a and from b in turn, marking components, until one is met twice: l
L8  for each component x ≠ l on the two paths: E.UNION(x, l); bridges ← bridges − 1
    the merged component keeps the parent of l

REROOT(a)                                   ▷ make a the root of its tree
L9  reverse the par pointers on the path from a to the root of its tree; par(a) ← nil
```

Line L1 ignores an edge inside one component, which includes loops and parallel copies of non-bridge edges. Line L3 finds a new bridge between two trees. Lines L4 and L5 hang the smaller tree, by vertex count, below the end $b$, after rerooting it at $a$. Line L6 handles a cycle. Line L7 finds the lowest common ancestor $l$ of $a$ and $b$ in their tree by climbing from both sides at once, so that its cost is proportional to the length of the path found, not to the depth of the tree. Line L8 merges the components on the path, each of which loses the bridge to its parent.

## Example

Take $n = 7$ and insert ten edges. The table shows the number of bridges and the 2-edge-connected components with more than one vertex.

| step | edge | event | bridges | components with more than one vertex |
|---|---|---|---|---|
| 1 | 0 1 | new bridge | 1 | none |
| 2 | 1 2 | new bridge | 2 | none |
| 3 | 2 3 | new bridge | 3 | none |
| 4 | 3 4 | new bridge | 4 | none |
| 5 | 1 5 | new bridge | 5 | none |
| 6 | 5 6 | new bridge | 6 | none |
| 7 | 4 2 | cycle 2, 3, 4 | 4 | $\{2, 3, 4\}$ |
| 8 | 6 0 | cycle 0, 1, 5, 6 | 1 | $\{2, 3, 4\}$, $\{0, 1, 5, 6\}$ |
| 9 | 3 3 | loop, ignored | 1 | same |
| 10 | 0 1 | inside a component, ignored | 1 | same |

At step 7, the ends 4 and 2 are in one tree. The climb from 4 goes to 3 and then to 2, and the climb from 2 meets 2 again, so $l = 2$ and the components of 3 and 4 merge into that of 2: the bridges $\{2, 3\}$ and $\{3, 4\}$ are gone. At step 8 the path between 6 and 0 in the forest is $6, 5, 1, 0$, which holds three bridges. At the end the only bridge is $\{1, 2\}$, between the two components.

## Correctness

The structure keeps this invariant: the sets of $E$ are the 2-edge-connected components of the current graph, the bridge forest has one node per component and one edge per bridge, and the sets of $C$ are its trees. An edge inside a component changes no component. An edge between two connected components is not on any cycle, because any cycle through it would need a second path between the two components, so it is a new bridge, and the old bridges stay bridges. An edge between two components $a$ and $b$ of one tree closes a cycle with exactly the bridges on the forest path from $a$ to $b$, so those bridges stop being bridges and the components on the path merge, while every other bridge still separates the graph. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Rerooting.** Line L9 walks a path of the smaller tree, so it costs at most the number of vertices of that tree, times the cost of a find. A vertex is in the smaller tree only if its connected component at least doubles in size by the link, so it takes part in at most $\lg n$ reroots. Only vertices that are an end of some inserted edge are ever in a tree with more than one vertex, and there are at most $\min(n, 2m)$ of them, so the total over all insertions is $O(\min(n, m) \log n)$ finds.
- **Merging.** Line L7 climbs the same number of steps on both sides, up to one more on the side that is longer, so it visits at most twice the number of components on the path plus two. Every component on the path except $l$ is merged and disappears, and at most $n - 1$ merges happen in total. So all climbs together take $O(m)$ finds.
- **Finds.** With union by size and path compression, each find costs $O(\alpha(n))$ amortized. Every insertion does $O(1)$ more finds.
- **Total.** $O(m \log n \cdot \alpha(n))$ for $m$ insertions, which is $O(\log n)$ amortized per insertion up to the factor $\alpha(n)$, and $O(m \log n)$ with the plain bound of $O(\log n)$ per find; a single insertion can take $\Theta(n)$ time. Space $O(n)$. The algorithm is deterministic.

## Properties

- **Insertions only.** Deletions can split components, and the union-finds cannot split sets. For deletions, see [dynamic biconnectivity](/dynamic-biconnectivity/), or the [offline method](/offline-dynamic-connectivity/) when the sequence is known in advance.
- **Online.** Each answer is ready before the next insertion is read.
- **Amortized.** The bound is for the whole sequence. One insertion that reroots a large tree, or that merges a long path, can be slow.
- **Deterministic.**

## Variants and improvements

- **Westbrook and Tarjan (1992)** keep bridge-connected (2-edge-connected) and biconnected components under insertions in $O(\alpha(m, n))$ amortized time per operation. They avoid the $\log n$ factor of rerooting.
- **Biconnected components.** The same plan works for vertex connectivity with the block-cut tree in place of the bridge forest; the merge step then merges the blocks on a path. See [dynamic biconnectivity](/dynamic-biconnectivity/).
- **Link-cut trees.** Storing the bridge forest in a [link-cut tree](/link-cut-tree/) gives $O(\log n)$ amortized time per insertion and supports path queries such as "how many bridges lie between $u$ and $v$".
- **Offline.** If all insertions are known in advance, build a spanning forest greedily in the order of insertion, so that each forest edge is a bridge when it arrives. Each other edge closes a cycle with forest edges inserted before it, so processing the other edges by path merges in the order of insertion gives the bridges at every time, with no rerooting.

## When to use it

Use it when edges only arrive and the questions are about bridges or 2-edge-connectivity after each arrival, for example in network reliability monitoring or in programming contests. For a graph that does not change, the static [bridge-finding](/bridge-finding/) algorithm with one depth-first search is simpler and takes linear time. For deletions, use a fully dynamic method.

## Pitfalls

- **Stale parent pointers.** $\mathrm{par}(a)$ may point to a vertex whose component has been merged into another. Always apply $E.\mathrm{find}$ to it.
- **Losing the parent of the merged component.** After line L8, the new representative must take the parent of $l$, the top of the path. A component that keeps the parent of another path vertex points into its own set, which makes a loop.
- **Climbing one side only.** Climbing from $a$ to the root and then from $b$ costs the depth of the tree, which can be $\Theta(n)$ for each insertion without merging anything. Climb from both sides in turn.
- **Rerooting the larger tree.** The $O(n \log n)$ bound needs the smaller tree to be rerooted; size by vertex count, not by component count, is the simplest correct choice.
- **Parallel edges.** A second copy of a bridge removes the bridge. Line L1 must not ignore it: the two ends are in different components, so the copy goes to MERGE-PATH, as it should.

## Implementations

## History

Tarjan (1974) gave the linear-time static algorithm for bridges. Westbrook and Tarjan (1992) solved the incremental problem for bridge-connected and biconnected components with near-constant amortized time per operation. The simpler version described here, with rerooting of the smaller tree and path merging, is the form taught on cp-algorithms and used in programming contests.

## References
