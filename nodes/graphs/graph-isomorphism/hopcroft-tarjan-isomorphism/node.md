---
tag: NBDRZ3
kind: algorithm
slug: hopcroft-tarjan-isomorphism
name: Hopcroft-Tarjan planar isomorphism algorithm
aliases:
- Hopcroft-Tarjan isomorphism of planar graphs
area: graphs/graph-isomorphism
level: advanced
summary: Tests isomorphism of 3-connected planar graphs by partition refinement on the darts of their unique embeddings, in O(n log n) time; Hopcroft and Wong later reached linear time.
solves: [planar-graph-isomorphism, graph-isomorphism-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n^2 log n), best: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, directed: false}
prereqs: [planar-graph-isomorphism, rotation-system, partition-refinement]
see_also: [planar-embedding, hopcroft-minimization, hopcroft-tarjan-planarity-test, planar-dual-graph, weisfeiler-leman, nauty, tree-isomorphism, k-dimensional-weisfeiler-leman]
sources:
  - paper: doi:10.1016/S0022-0000(73)80013-3
    title: John E. Hopcroft and Robert E. Tarjan, A V log V algorithm for isomorphism of triconnected planar graphs, Journal of Computer and System Sciences 7(3), 323 to 331 (1973)
    locator: the whole paper (the reduction to the embedding, the partitioning of the map, and the V log V bound)
  - paper: "John E. Hopcroft and Robert E. Tarjan, Isomorphism of planar graphs, in Complexity of Computer Computations, Plenum Press, 1972, 131 to 152"
    locator: the whole chapter (decomposition into triconnected components and the overall planar test)
  - paper: doi:10.1145/800119.803896
    title: John E. Hopcroft and J. K. Wong, Linear time algorithm for isomorphism of planar graphs, Proceedings of the Sixth ACM Symposium on Theory of Computing (STOC 1974), 172 to 184
    locator: the whole paper (linear-time isomorphism of 3-connected planar graphs by reducing the maps)
---

The Hopcroft-Tarjan algorithm tests whether two 3-connected planar graphs are isomorphic in $O(n \log n)$ time. It uses Whitney's theorem: such a graph has only one embedding in the plane up to mirror image, so isomorphism of the graphs becomes isomorphism of two maps, which is a rigid structure with few symmetries. The maps are compared by partition refinement, the same "process the smaller half" idea as [Hopcroft's DFA minimization](/hopcroft-minimization/). Together with a decomposition into 3-connected pieces, it gave the first $O(n \log n)$ isomorphism test for all [planar graphs](/planar-graph-isomorphism/) (1972 and 1973), and Hopcroft and Wong reached linear time in 1974.

## In plain words

A network that can be drawn flat without crossings, and that stays connected after removing any two points, can be drawn in essentially one way: the order of the links around each point is fixed, except that the whole drawing may be flipped over. So to compare two such networks, you can compare their drawings. Stand on one link of the first drawing and on a link of the second, and walk: turn to the next link around the point, or cross to the other end. If both walks always see the same thing, the drawings match. The algorithm does this for all links at once by grouping links that look alike and splitting the groups until they stop changing, then tries the flipped drawing too.

## The problem

The input is two simple undirected graphs $G_1, G_2$, without colors or labels, both 3-connected and planar, each given with a planar [rotation system](/rotation-system/): for each vertex $v$, the clockwise order of its neighbors in a plane drawing. A [planar embedding](/planar-embedding/) algorithm computes it in linear time. The output is an isomorphism $\varphi : V(G_1) \to V(G_2)$ or the answer that none exists.

A dart is an edge with a direction, $(u, v)$. Two permutations act on darts: $\sigma(u, v) = (u, v')$, where $v'$ follows $v$ around $u$, and $\alpha(u, v) = (v, u)$. The cycles of $\sigma$ are the vertices and the cycles of $\sigma\alpha$ are the faces. A map isomorphism is a bijection $f$ of darts with $f\sigma = \sigma f$ and $f\alpha = \alpha f$.

## The algorithm

MAP-ISOMORPHISM works on the darts of both maps together. Each dart gets the label (degree of its tail, length of the face to its left). REFINE splits blocks until, for every block $B$, the darts whose $\sigma$-image lies in $B$ form a union of blocks, and the same for $\alpha$. It takes splitters from a queue and, as in Hopcroft's method, queues only the smaller piece of a split block that is not queued.

```pseudo id=main
MAP-ISOMORPHISM(M1, M2)
L1  blocks ← darts of M1 and M2 grouped by (degree of tail, length of face)
L2  REFINE(blocks, queue = every block) under σ and α
L3  if some block has unequal numbers of darts from M1 and M2 then return none
L4  B ← a smallest block; x ← a dart of M1 in B
L5  for each dart y of M2 in B do
L6      copy the blocks, make {x, y} a block of its own, REFINE(copy, queue = [{x, y}])
L7      if every block is a pair {a, b} with a in M1, b in M2 then return φ: tail(a) ↦ tail(b)
L8  return none
```

TRICONNECTED-PLANAR-ISOMORPHISM($G_1, G_2$) returns MAP-ISOMORPHISM($M_1, M_2$) if it is not none, and otherwise MAP-ISOMORPHISM($M_1$, mirror of $M_2$), where the mirror reverses every rotation.

## Example

The triangular bipyramid, with the triangle $1, 2, 3$ around its middle and the apexes $0$ and $4$, given by the rotations $0: (1, 2, 3)$, $1: (2, 0, 3, 4)$, $2: (0, 1, 4, 3)$, $3: (0, 2, 4, 1)$, $4: (2, 1, 3)$. It has 5 vertices, 9 edges and 6 triangular faces. The second map renames it by $p = (2, 0, 4, 1, 3)$, that is $0 \mapsto 2$, $1 \mapsto 0$ and so on, and starts some rotations at other neighbors.

| step | blocks of darts (both maps, 36 darts) | refine calls |
|---|---|---|
| L1 | label (3, 3): 12 darts; label (4, 3): 24 darts | |
| L2 | 3 blocks of 12, 6 darts from each map in each | 1 |
| L3 | counts balanced, continue | |
| L4 to L6 | first trial $y$: 18 blocks, each a pair | 2 |
| L7 | $\varphi = (2, 0, 4, 1, 3)$ | |

The result is the renaming $p$. Against the mirror of the second map, the first trial also succeeds and gives $(2, 1, 4, 0, 3)$, an isomorphism of graphs that reverses the orientation. On the cube, the octahedron and $K_4$ every dart has the same label, and L2 leaves one block of all darts; against a random renaming, the first trial splits it into pairs, 2 refine calls in all.

The mirror step is needed. The triangulation with 7 vertices and rotations $0: (1, 2, 5, 4)$, $1: (2, 0, 4)$, $2: (0, 1, 4, 3, 6, 5)$, $3: (5, 6, 2, 4)$, $4: (1, 0, 5, 3, 2)$, $5: (0, 2, 6, 3, 4)$, $6: (3, 5, 2)$ has no map isomorphism to its own mirror: after L2 all 60 darts are in pairs, both from the same map, and L3 rejects after one refine call. The second call, against the mirror of the mirror, finds the identity after three refine calls in all.

## Correctness

The [full proof](proofs/correctness.md) has four steps.

- **REFINE is the coarsest stable refinement.** A split never separates darts that a stable partition finer than the input keeps together, and Hopcroft's invariant shows that the result is stable even though only the smaller pieces are queued.
- **Invariance.** A map isomorphism $f$ preserves the labels and commutes with $\sigma$ and $\alpha$, so the partition into pairs $\{d, f(d)\}$ is stable and finer than every partition the algorithm builds. Hence every block is balanced at L3, and $f(x)$ is in the block of $x$ at L4.
- **One dart decides.** In a connected map, every dart is reached from $x$ by $\sigma$ and $\alpha$. Fixing $x \mapsto y$ forces the whole map isomorphism, and refinement finds exactly its pairs; a partition into stable pairs across the maps is a map isomorphism, which induces a graph isomorphism.
- **Whitney's theorem.** A 3-connected planar graph has one planar rotation system up to mirror image, so an isomorphism of the graphs is a map isomorphism to $M_2$ or to its mirror.

## Complexity

Let $N$ be the number of darts, twice the number of edges; for a planar graph $N \le 6n - 12$.

| step | time | space |
|---|---|---|
| labels, L1 | $O(N)$ | $O(N)$ |
| one REFINE, L2 or L6 | $O(N \log N)$ | $O(N)$ |
| trials, this implementation | at most $N/2$, so $O(N^2 \log N)$ in the worst case | $O(N)$ per trial, freed after it |
| Hopcroft and Tarjan (1973) | $O(n \log n)$ | $O(n)$ |
| Hopcroft and Wong (1974) | $O(n)$ | $O(n)$ |

Each dart enters a queued splitter only when its block at most halves, so it is scanned $O(\log N)$ times per refinement. The trials are where this implementation is weaker than the paper: in the worst case it refines once per candidate $y$. In practice the first candidate decides, because 3-connected maps have few symmetries and refinement rarely leaves large blocks; on 400 random triangulations and cubic maps of up to 30 vertices, no isomorphic pair needed more than 2 refine calls. The paper organizes the search differently to keep the total at $O(n \log n)$; this page keeps the simpler trial loop. Hopcroft and Wong reach linear time by a different method, reducing both maps step by step.

## Properties

- **Exact.** It returns an isomorphism when one exists and none otherwise, with no heuristics.
- **Rigid input.** The automorphisms of a map act freely on its darts, by the one-dart lemma, so a 3-connected planar graph with $m$ edges has at most $2m$ automorphisms that keep the orientation and $4m$ in all. This rigidity is why one trial usually decides.
- **Only for 3-connected planar graphs.** General planar graphs need the decomposition below; non-planar graphs have no rotation system that the theorem applies to.
- **Graphs are undirected and uncolored.** Vertex or edge colors fit by adding them to the labels in L1.

## Variants and improvements

- **All planar graphs.** Split each graph into biconnected components, then into triconnected components ([Hopcroft-Tarjan](/hopcroft-tarjan-planarity-test/) style depth-first search), compare the 3-connected pieces with this algorithm, and compare the trees of pieces with an [AHU](/ahu-algorithm/)-like method. This is the plan of the 1972 chapter, and the subject of [planar graph isomorphism](/planar-graph-isomorphism/).
- **Linear time.** Hopcroft and Wong (1974) reduce the two maps in step by a sequence of local simplifications that keep isomorphism, reaching $O(n)$.
- **Canonical forms.** Walking the map from each dart in a fixed order gives a code of length $O(n)$; the smallest code over all darts and both orientations is a canonical form, computable in $O(n^2)$ simply, or in linear time with more work.
- **Logarithmic space.** Datta, Limaye, Nimbhorkar, Thierauf and Wagner (2009) showed that planar graph isomorphism is in logspace.
- **Weisfeiler-Leman.** [3-dimensional WL](/k-dimensional-weisfeiler-leman/) identifies all planar graphs (Kiefer, Ponomarenko and Schweitzer 2017), a slower but uniform polynomial method.

## When to use it

Use it when the graphs are known to be planar, for example molecules, meshes, polyhedra or circuit layouts, and especially when they are 3-connected, like the graphs of convex polyhedra and triangulations. For small inputs a general tool such as [nauty](/nauty/) is simpler and fast. For mixtures of planar and non-planar graphs, test planarity first and fall back to a general method.

## Pitfalls

- **Forgetting the mirror.** Some maps, such as the 7-vertex triangulation above, are not isomorphic to their mirror images, so the test must try both orientations.
- **Applying it below 3-connectivity.** A 2-connected planar graph can have many embeddings that are not mirrors of each other, and two isomorphic graphs may then have non-isomorphic maps.
- **Unbalanced blocks.** A block with different numbers of darts from the two maps already proves that no map isomorphism exists; without the check in L3 the answer stays right, since L7 still checks every trial, but all trials are wasted.
- **Recursion.** Face tracing and refinement are loops here; recursive depth-first versions overflow the Python stack on large maps.

## Implementations

## History

Hopcroft and Tarjan gave an $O(n^2)$ algorithm for planar graph isomorphism in 1971, then in 1972 and 1973 an $O(n \log n)$ algorithm, built on their linear-time planarity test and decomposition into triconnected components. Wong's work with Hopcroft in 1974 brought the time to linear, which settled the sequential complexity of planar graph isomorphism. Later work moved to parallel and space-bounded computation, ending with the logspace algorithm of Datta and coauthors in 2009.

## References
