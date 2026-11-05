---
tag: HTR1D9
kind: problem
slug: planar-graph-isomorphism
name: Planar graph isomorphism
aliases:
- isomorphism of planar graphs
area: graphs/graph-isomorphism
level: advanced
summary: Graph isomorphism restricted to planar graphs, solvable in linear time using planar embeddings.
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n)}
  space: {extra: O(n)}
prereqs: [graph-isomorphism-problem, planar-graph, planar-embedding]
see_also: [hopcroft-tarjan-isomorphism, tree-isomorphism, rotation-system, k-dimensional-weisfeiler-leman, bounded-degree-graph-isomorphism, gi-completeness, canonical-labeling, planarity-testing]
sources:
  - paper: doi:10.1145/800119.803896
    title: John E. Hopcroft and J. K. Wong, Linear time algorithm for isomorphism of planar graphs, Proceedings of the Sixth ACM Symposium on Theory of Computing (STOC 1974), 172 to 184
    locator: the whole paper (the linear-time bound, through decomposition and the 3-connected case)
  - paper: doi:10.1016/S0022-0000(73)80013-3
    title: John E. Hopcroft and Robert E. Tarjan, A V log V algorithm for isomorphism of triconnected planar graphs, Journal of Computer and System Sciences 7(3), 323 to 331 (1973)
    locator: the whole paper (Whitney's theorem used to reduce to maps, and partition refinement of the map)
  - paper: "Samir Datta, Nutan Limaye, Prajakta Nimbhorkar, Thomas Thierauf and Fabian Wagner, Planar graph isomorphism is in log-space, Proceedings of the 24th IEEE Conference on Computational Complexity (CCC 2009), 203 to 214"
    locator: the main theorem and the sections on the decomposition into biconnected and triconnected components in logspace
  - paper: "Sandra Kiefer, Ilia Ponomarenko and Pascal Schweitzer, The Weisfeiler-Leman dimension of planar graphs is at most 3, Proceedings of the 32nd ACM/IEEE Symposium on Logic in Computer Science (LICS 2017)"
    locator: the main theorem (3-dimensional Weisfeiler-Leman identifies every planar graph)
---

Planar graph isomorphism is the [graph isomorphism problem](/graph-isomorphism-problem/) for graphs that can be drawn in the plane without crossings. Unlike general graph isomorphism, it is solved in linear time: Hopcroft and Tarjan gave an $O(n \log n)$ algorithm in 1972 and 1973, and Hopcroft and Wong reached $O(n)$ in 1974. The key fact is Whitney's theorem, that a 3-connected planar graph has essentially one drawing, which turns isomorphism of graphs into isomorphism of rigid maps. The problem is also in logarithmic space and is identified by 3-dimensional Weisfeiler-Leman.

## In plain words

Two road maps without bridges or tunnels are given, each as a list of crossings and roads. Are they the same network with the crossings renamed? For most networks this kind of question has no known fast answer. For flat networks it does. A flat network that is well connected can be drawn in only one way, apart from a mirror image, so around each crossing the roads come in a fixed order. Matching two such drawings is like matching two maps: pick a road in each, and the rest of the match is forced. Networks that are less well connected are cut into well connected pieces first, the pieces are matched, and then the way they are glued together is matched like a family tree.

## Definition

**Planar graph isomorphism.**
- Input: two simple undirected graphs $G$ and $H$ on $n$ vertices, without colors or labels, both planar.
- Output: whether there is a bijection $\varphi : V(G) \to V(H)$ with $uv \in E(G) \iff \varphi(u)\varphi(v) \in E(H)$, and, in the search version, such a $\varphi$.

Planarity itself is tested in linear time by [planarity testing](/planarity-testing/), so the promise that the inputs are planar costs nothing. A planar graph has at most $3n - 6$ edges, so linear time means $O(n)$.

## Variants

- **3-connected planar graphs.** The core case. By Whitney's theorem the embedding is unique up to mirror image, and the [Hopcroft-Tarjan algorithm](/hopcroft-tarjan-isomorphism/) compares the two maps.
- **Map isomorphism.** The graphs come with fixed [rotation systems](/rotation-system/), and the isomorphism must keep them, possibly up to reflection. This is easy for every connected map: fixing one dart forces the rest, so $O(n^2)$ is trivial and $O(n)$ is possible.
- **Colored, directed or edge-labeled planar graphs.** The same algorithms work with the labels added to the comparisons.
- **Canonical forms.** A canonical code of a planar graph is computable in linear time as well, which allows hashing of large collections, such as molecule databases.
- **Bounded genus.** Graphs embeddable on a fixed surface: isomorphism is in polynomial time for each genus (Filotti and Mayer; Miller, 1980), and later in linear time for each fixed genus.
- **Classes excluding a minor.** Ponomarenko (1988) and Grohe (2012) gave polynomial-time algorithms for every class that excludes a fixed minor, which includes planar graphs.

## Examples

All values were computed with the implementations on the pages of [Hopcroft-Tarjan](/hopcroft-tarjan-isomorphism/), [nauty](/nauty/), [color refinement](/weisfeiler-leman/) and [k-WL](/k-dimensional-weisfeiler-leman/).

| pair | vertices, edges | 3-connected? | color refinement | isomorphic? |
|---|---|---|---|---|
| cube and the dual $D$ of the 6-vertex triangulation with degrees 3, 3, 4, 4, 5, 5 | 8, 12 each | yes | not distinguished | no |
| two embeddings of the theta graph with paths of lengths 2, 2, 3, 3 | 8, 10 each | no, only 2-connected | not distinguished | yes, but the maps differ |
| the 7-vertex chiral triangulation of the Hopcroft-Tarjan page and its mirror image | 7, 15 each | yes | not distinguished | yes, through the mirror only |

- **Cube and $D$.** Both are 3-regular, so color refinement keeps one color. Their faces differ: the cube has six faces of length 4, and $D$ has faces of lengths 3, 3, 4, 4, 5, 5. The Hopcroft-Tarjan labels already tell them apart, and so does 2-WL, which counts the triangles of $D$. $\lvert \mathrm{Aut} \rvert$ is 48 for the cube and 4 for $D$.
- **The theta graph.** Two vertices joined by four internally disjoint paths with 2, 2, 3 and 3 edges. Ordering the paths around the ends as 2, 2, 3, 3 gives faces of lengths 4, 5, 5, 6, and the order 2, 3, 2, 3 gives four faces of length 5. The graph is the same, but neither map is isomorphic to the other or to its mirror. So for graphs that are not 3-connected, comparing one embedding of each is wrong.
- **The chiral triangulation.** It is not isomorphic to its mirror as a map, but as a graph it is isomorphic to it, which shows that the 3-connected test must try both orientations.

## Known algorithms

| algorithm | time | idea |
|---|---|---|
| brute force over bijections | $O(n! \cdot n)$ | try every map |
| Weinberg (1966), 3-connected | $O(n^2)$ | a code from a walk of the embedding from each starting dart |
| Hopcroft and Tarjan (1971) | $O(n^2)$ | the first quadratic algorithm for all planar graphs |
| [Hopcroft and Tarjan](/hopcroft-tarjan-isomorphism/) (1972, 1973) | $O(n \log n)$ | triconnected components, then partition refinement of the darts of each 3-connected piece |
| Hopcroft and Wong (1974) | $O(n)$ | the same decomposition, with a linear-time test for the 3-connected pieces |
| Datta, Limaye, Nimbhorkar, Thierauf and Wagner (2009) | logarithmic space | the decomposition and canonical codes, computed in logspace |
| [3-dimensional WL](/k-dimensional-weisfeiler-leman/) | $O(n^4 \log n)$ | identifies every planar graph (Kiefer, Ponomarenko and Schweitzer 2017) |
| [nauty](/nauty/), [bliss](/bliss/) | exponential in the worst case | general tools, fast on most planar inputs |

The general plan is the same in all the decomposition algorithms. Split the graph into biconnected components and arrange them in the block-cut tree; split each biconnected component into triconnected components (3-connected graphs, cycles and bonds) and arrange them in a tree; compare the 3-connected pieces through their unique embeddings; and compare the trees bottom up, as in [tree isomorphism](/tree-isomorphism/), where each tree node carries the code of its piece and of how its children attach.

## Bounds

- **Upper bound.** $O(n)$ time (Hopcroft and Wong 1974), which is optimal, since the input must be read. The problem is also in logarithmic space (Datta et al. 2009), which the authors show is tight: it is complete for L.
- **Weisfeiler-Leman dimension.** At most 3 for planar graphs (Kiefer, Ponomarenko and Schweitzer 2017), in the convention where $k$-WL matches counting logic with $k + 1$ variables. Color refinement alone fails, as the cube example shows.
- **Not GI-complete.** Since it is in P, it is not [GI-complete](/gi-completeness/) unless graph isomorphism itself is in P.

## Reductions

- **To the 3-connected case.** The decomposition into biconnected and triconnected components is unique and computable in linear time, and two planar graphs are isomorphic exactly when their decomposition trees are isomorphic with matching pieces at the nodes.
- **3-connected to map isomorphism.** By Whitney's theorem, two 3-connected planar graphs are isomorphic exactly when one map is isomorphic to the other or to its mirror image.
- **Map isomorphism to a string problem.** A walk of a connected map from a dart, taking edges in rotation order, gives a code that determines the map, so map isomorphism reduces to comparing codes over all starting darts.
- **Tree isomorphism** is the special case of trees, all of which are planar, and the decomposition trees reduce planar isomorphism to it.

## Applications

- **Chemistry.** Most molecular graphs are planar, and canonical forms of planar graphs give exact keys for molecule databases.
- **Polyhedra and meshes.** The graphs of convex polyhedra are exactly the 3-connected planar graphs (Steinitz's theorem), so this problem compares polyhedra and triangulated meshes combinatorially.
- **Circuit layout and geographic data.** Comparing planar layouts and road or region networks.
- **Enumeration.** Generators of planar graphs, such as plantri, use canonical forms of planar maps to output each graph once.
- **Theory.** The linear-time algorithm is a classic use of depth-first search and partition refinement, and the logspace and WL results are milestones in the study of graph classes with easy isomorphism.

## References
