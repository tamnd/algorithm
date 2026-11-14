---
tag: 5S5Z62
kind: algorithm
slug: generic-naming-scheme
name: Generic naming of topological entities
aliases:
- Capoyleas-Chen-Hoffmann naming
area: cad/solid-modeling
level: advanced
summary: Capoyleas, Chen and Hoffmann's scheme that names each face, edge and vertex by the features and operations that made it plus local context, so names survive edits.
solves: [persistent-naming-problem]
model: word-ram
complexity:
  vars: {n: the number of boundary edges of the model, L: the length of the longest boundary cycle}
  time: {worst: "O(n L^2)"}
  space: {extra: "O(n L)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1996
  people: [Vasilis Capoyleas, Xiangping Chen, Christoph M. Hoffmann]
  note: Capoyleas, Chen and Hoffmann named the entities of a generative, constraint-based model by the operations and generators that made them, extended by the names of neighbouring entities when a name alone is ambiguous.
prereqs: [persistent-naming-problem, feature-based-modeling, boundary-representation]
see_also: [attributed-adjacency-graph, graph-isomorphism-problem, weisfeiler-leman, maximum-common-subgraph, string-matching, booth-algorithm, euler-operators, direct-modeling]
sources:
  - paper: "Vasilis Capoyleas, Xiangping Chen and Christoph M. Hoffmann, Generic naming in generative, constraint-based design, Computer-Aided Design 28(1), 17 to 26, 1996"
    locator: the whole paper (names built from the creating operation and the entities it is made from, extended by neighbouring entities when ambiguous, and the matching of names after a regeneration)
  - paper: "Xiangping Chen and Christoph M. Hoffmann, Towards feature attachment, Computer-Aided Design 27(9), 695 to 702, 1995"
    locator: how a feature refers to entities of the model built before it, and what happens to the references on regeneration
  - paper: "Jiri Kripac, A mechanism for persistently naming topological entities in history-based parametric solid models, Computer-Aided Design 29(2), 113 to 122, 1997"
    locator: the topological ID system, a related scheme that names faces by their feature and edges and vertices by their faces
  - paper: "David Marcheix and Guy Pierra, A survey of the persistent naming problem, Proceedings of the Seventh ACM Symposium on Solid Modeling and Applications, 13 to 22, 2002"
    locator: the classes of naming methods, including generic naming, and the cases where each one fails
---

Generic naming gives each face, edge and vertex of a history-based model a name that does not depend on how the kernel happened to store it. The name records the operation that made the entity and the generator inside that operation. For example, "the side face that extrusion 2 swept from line 3 of its sketch". When this generative part does not single out one entity, the name is extended with the names of neighbouring entities until it does. After the designer edits a parameter and the history is replayed, every reference resolves its name in the new model by finding the entities with the same name. Capoyleas, Chen and Hoffmann gave the scheme in 1996 as an answer to the [persistent naming problem](/persistent-naming-problem/). This page gives a planar version. The model is a rectangle cut by rectangles and patterns of rectangles. Each edge is labelled by the rectangle side it lies on and named by the labels of the edges around it on its boundary cycle. The page proves exactly when names survive. If the old and new boundaries are isomorphic as labelled cycles, every name resolves to its images under all such isomorphisms: one entity when the name was unique, and the full set of symmetric candidates when it was not.

## In plain words

A designer cuts a slot into the top of a block, so the top edge breaks into two pieces. Later a rounding is attached to the left piece. How does the program remember which piece?

It cannot say "piece number 2", because numbers change when the model is rebuilt. It can say "a piece of the block's top". But there are two such pieces. So it adds what is next to it: "the piece of the block's top that has the slot's left wall on one side and the block's left side on the other". After the designer widens the block or moves the slot, the program rebuilds the model and looks for an edge with this description. There is still exactly one.

If the pieces are true twins, like the pieces between identical slots, no description tells them apart. The program should then report all of them.

## The problem

**Input.** A model $M$ built by a history, and a model $M'$ built by the same history after an edit of its parameters. In the planar toy, the history is a base rectangle followed by cut operations. Each operation is one rectangle or a pattern of copies, and the part is the base minus the cuts. The boundary of the part is a set of cycles of edges, with the material on the left.

**Labels.** Each edge lies on one side of one rectangle. Its *label* is the pair (operation, side), such as (cut 1, left). Distinct coordinates for distinct sides make this well defined. Labels are generative: they depend only on the history, not on the coordinates. A cut can split one side into several edges with the same label, and the copies of a pattern share their labels.

**Output.** A name for each edge and vertex of $M$, and a resolution rule that maps a name and $M'$ to a set of entities of $M'$. The goal is that a name resolves to the entity "with the same role" in $M'$. Here that is made precise. An *isomorphism* from $M$ to $M'$ is a bijection between their boundary cycles, with a rotation of each cycle, that keeps every label. The correct answer for an edge $e$ is the set of its images $\sigma(e)$ over all isomorphisms $\sigma$. This set is a single edge when $e$ has no symmetric twin, and a set of twins otherwise. If no isomorphism exists, the topology has changed, and no answer is claimed.

## The algorithm

The *window* of radius $r$ of an edge $e$ on a cycle of length $L$ is the tuple of the labels of the $2r + 1$ edges centred on $e$, going around the cycle. When $2r + 1 > L$ the window wraps around, and then it also records $L$. The *level* of $e$ is the least $r$ at which its window is unique among all edges of $M$. If no window is unique up to the length of the longest cycle, the level is that length. The name of $e$ is its level and its window at that level. A vertex is named by the names of the edge before it and the edge after it.

```pseudo id=main
NAME-EDGES(M)
L1  for r ← 0, 1, ... while some edge has no level and r ≤ the longest cycle length do
L2      count the windows of radius r over all edges of M
L3      for each edge e with no level yet do
L4          if window_r(e) occurs once, or r is the longest cycle length, then level(e) ← r
L5  return name(e) = (level(e), window_level(e)(e)) for every edge e

RESOLVE-EDGE((r, w), M')
L6  return the edges e' of M' with window_r(e') = w

NAME-VERTEX(v) and RESOLVE-VERTEX
L7  name(v) ← (name of the edge before v, name of the edge after v)
L8  return the vertices of M' whose edge before resolves from the first name
    and whose edge after resolves from the second
```

The level-0 window is the generative label alone, which is the name of most edges. The level-1 window adds the two neighbours, which is enough to tell apart the pieces of a side split by one cut. Higher levels are needed only when a pattern or several cuts repeat the same local picture.

## Example

The base is $[0, 10] \times [0, 6]$ and cut 1 is $[4, 6] \times [3, 8]$, a slot through the top. The part has one boundary cycle of 8 edges, listed counterclockwise from the bottom:

| edge | label | level | name |
|---|---|---|---|
| $(0,0)$ to $(10,0)$ | base bottom | 0 | base bottom |
| $(10,0)$ to $(10,6)$ | base right | 0 | base right |
| $(10,6)$ to $(6,6)$ | base top | 1 | (base right, base top, cut 1 right) |
| $(6,6)$ to $(6,3)$ | cut 1 right | 0 | cut 1 right |
| $(6,3)$ to $(4,3)$ | cut 1 bottom | 0 | cut 1 bottom |
| $(4,3)$ to $(4,6)$ | cut 1 left | 0 | cut 1 left |
| $(4,6)$ to $(0,6)$ | base top | 1 | (cut 1 left, base top, base left) |
| $(0,6)$ to $(0,0)$ | base left | 0 | base left |

The edit changes the base to $[0, 20] \times [0, 9]$ and the cut to $[5, 12] \times [4, 15]$. The new model has the same cycle of labels, so each name resolves to exactly one edge, at the same place in the cycle. The left piece of the top is now the edge from $(5, 9)$ to $(0, 9)$.

If instead the cut becomes $[4, 6] \times [3, 5]$, a pocket that no longer reaches the top, then the top is one edge again. Both names of level 1 resolve to nothing. That is the right answer, since the piece no longer exists. The level-0 label "base top" would find the whole top edge, which a modeler can offer as a repair.

With a pattern of three through slots $[4, 5]$, $[9, 10]$ and $[14, 15]$ across $[0, 20] \times [0, 10]$, the part falls into four pieces. The two middle pieces both have the cycle (base bottom, cut 1 left, base top, cut 1 right). Their 8 edges have no unique window at any level. Each gets the top level 4 and resolves to 2 edges, which are its images under the two isomorphisms that swap or keep the middle pieces. The other 8 edges are unique at level 0 or 1.

## Correctness

The proof file proves:

1. **Windows are invariant.** An isomorphism $\sigma$ keeps labels, cycle lengths and the cyclic order, so $\mathrm{window}_r(\sigma(e)) = \mathrm{window}_r(e)$ for every $r$.
2. **Names resolve to the images.** Suppose $M$ and $M'$ are isomorphic by some $\sigma_0$. The edges of $M'$ with window $w$ at radius $r$ are exactly $\sigma_0$ applied to the edges of $M$ with window $w$. If the name of $e$ is unique in $M$, it resolves to $\{\sigma_0(e)\}$, and every isomorphism agrees there. If it is not unique, the level is the top level. Then the window holds the cycle length and the whole cycle read from $e$, and the edges of $M$ with that window are exactly the images of $e$ under the automorphisms of $M$. So in both cases line L6 returns $\{\sigma(e) : \sigma \text{ an isomorphism}\}$.
3. **Vertices follow.** An isomorphism maps the vertex between $a$ and its successor to the vertex between $\sigma(a)$ and $\sigma(a)$'s successor, so line L8 returns the images of the vertex.
4. **Order-preserving edits keep every name.** If an edit keeps the order of all $x$ coordinates and of all $y$ coordinates, the code builds the same grid, cells, cycles and labels from the ranks. So the identity is an isomorphism, and each name resolves to a set that contains the edge at the same grid position, which is that edge alone when the name is unique.

The tests check these claims against a brute-force oracle. The oracle tries every bijection between the cycles of the two models and every rotation of each cycle, keeps those that preserve all labels, and collects the images of every edge. Random histories have up to 3 operations, each a single rectangle or a pattern of 2 or 3 copies, and some cut through the whole part. For 150 histories with an order-preserving change of all coordinates, every edge and vertex name must resolve to exactly the oracle's images, which must include the same grid edge. For 250 histories whose coordinates all move by up to 3, the same must hold whenever the oracle finds an isomorphism. That was 61 of them, and the other 189 changed the topology. The tests also check that the boundary cycles enclose the same area as the inside grid cells.

## Complexity

Let $n$ be the number of edges and $L$ the length of the longest cycle. Level $r$ computes $n$ windows of length $2r + 1$, so it costs $O(n r)$ time with hashing, and the levels up to $L$ cost $O(n L^2)$ in the worst case. Most edges stop at level 0 or 1, so the typical cost is $O(n)$. Resolving one name costs $O(n L)$. The names take $O(n L)$ space. Building the toy model from $c$ rectangles takes $O(c^3)$ time on its $O(c^2)$ grid cells.

These bounds are for the planar toy. In a solid modeler, names are built over the face adjacency graph, and extending a name by neighbours is a bounded-radius neighbourhood in a graph. The cost depends on how the kernel records the generators of each face during the replay, and the papers give no general bound.

## Properties

- **Deterministic and exact.** Names are tuples of labels, with integer coordinates only in the geometry of the toy.
- **Generative.** A name depends on the history and the topology, not on coordinates or storage order. Geometry enters only through the topology it produces.
- **Honest about symmetry.** A name that cannot be made unique resolves to all candidates, rather than to an arbitrary one.
- **Local.** An edge whose label is unique keeps its name under any edit that keeps its label in the model, even if the topology elsewhere changes.

## Variants and improvements

- **Names in three dimensions.** Capoyleas, Chen and Hoffmann name a face by its feature and generator, such as the sketch entity that an extrusion sweeps, or the start and end caps. They name an edge by the faces that meet at it, and a vertex by its faces or edges. When two faces meet along several edges, an edge name is extended by the faces at its ends. When a face is split, the pieces are told apart by their neighbours.
- **Topological ID.** Kripac's mechanism is close in spirit. It also names faces by feature and generator and edges and vertices by their faces, and it records the history of splits and merges.
- **Geometric tie-breaking.** When the topology leaves a tie, as with the twins of a pattern, many systems break it by geometry: the piece nearest to the old position, or on a given side of a reference plane. This picks one entity, which is right more often than not, but the choice is a heuristic and is not proved.
- **Graph matching.** Without generative labels, the resolution is a matching of [attributed adjacency graphs](/attributed-adjacency-graph/), a form of [graph isomorphism](/graph-isomorphism-problem/) or [maximum common subgraph](/maximum-common-subgraph/). The labels make that matching easy here. The windows play the role of the colours of [Weisfeiler-Leman](/weisfeiler-leman/) refinement on a cycle.
- **Faster windows.** On a cycle, the windows of all edges at all radii come from one pass of string matching on the doubled cycle, and canonical rotations come from [Booth's algorithm](/booth-algorithm/). This removes the factor $L$ from the time per level.

## When to use it

Use generic naming in a history-based modeler, whenever later features refer to entities made by earlier ones: fillets on edges, sketches on faces, holes on faces, constraints between faces. It works best when most entities have a unique generator. A face swept from one sketch line usually does. Splits and patterns are the cases where the extension by neighbours matters. In [direct modeling](/direct-modeling/), where there is no history to replay, entities can keep their identity through the edit, and naming is less critical.

## Pitfalls

- **A unique name is not a correct name.** After a topological change, a name can resolve to one entity that is not the one the designer meant. For example, a level-0 label resolves to the merged top edge, which is longer than the old piece. The scheme proves correctness only when the boundaries are isomorphic.
- **Picking one of several.** A resolution that returns several candidates must be shown to the user or handled by a stated rule. Picking the first one silently moves a feature to a twin.
- **Labels from storage order.** If the generator is recorded as "the third curve the kernel created" rather than "line 3 of the sketch", the names change on replay, and the scheme fails from the start.
- **Too small a neighbourhood.** Stopping at level 1 when two pieces still share their window leaves a tie that a larger radius would break.
- **Too large a neighbourhood.** A name that includes far-away entities breaks when something far away changes. Extend only as far as uniqueness needs, as line L4 does.

## Implementations

## History

The parametric, history-based modelers of the late 1980s and early 1990s exposed the problem. References to faces and edges broke when an early feature was edited and the history replayed. Chen and Hoffmann described in 1995 how features attach to entities of the model before them. Capoyleas, Chen and Hoffmann published generic naming in 1996, with names built from the operations and generators of a generative design and extended by neighbouring entities to remove ambiguity. Kripac's topological ID system of 1997 took a related approach in a commercial setting. Marcheix and Pierra surveyed the methods in 2002, and they showed that every known scheme fails on some edits, because the problem refers to the designer's intent.

## References
