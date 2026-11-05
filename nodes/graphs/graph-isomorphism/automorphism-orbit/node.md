---
tag: CQ6QC1
kind: concept
slug: automorphism-orbit
name: Automorphism orbit
aliases:
- vertex orbit
- orbit partition
area: graphs/graph-isomorphism
level: core
summary: A set of vertices that automorphisms can map onto one another; the orbits partition the vertex set.
prereqs: [graph-automorphism-group, equivalence-relation]
see_also: [equitable-partition, graph-automorphism, weisfeiler-leman, burnside-lemma, asymmetric-graph, individualization-refinement, symmetry-reduction]
sources:
  - book: isbn:9780387952208
    title: Chris Godsil and Gordon Royle, Algebraic Graph Theory, Springer, Graduate Texts in Mathematics 207, 2001
    locator: Chapter 2, Groups (permutation groups, orbits and stabilizers) and Chapter 3, Transitive graphs
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 6, Groups and symmetry, and Chapter 7, Computing isomorphism
  - paper: doi:10.1016/j.jsc.2013.09.003
    title: Brendan D. McKay and Adolfo Piperno, Practical graph isomorphism, II, Journal of Symbolic Computation 60, 94 to 112 (2014)
    locator: Section 2 (orbits of the automorphism group and their use in pruning)
---

An orbit of a graph's [automorphism group](/graph-automorphism-group/) is a set of vertices that symmetries can move onto one another: $u$ and $v$ are in the same orbit when some automorphism maps $u$ to $v$. The orbits partition the vertex set, and vertices in one orbit are structurally the same, so they agree on every [isomorphism invariant](/isomorphism-invariant/). Orbits tell an isomorphism search which choices are equivalent, and computing them is part of the [graph automorphism problem](/graph-automorphism/).

## In plain words

Two points of a network are in the same orbit when a symmetry of the network can carry one onto the other. Then nothing in the pattern of links can tell them apart: they have the same number of neighbors, they lie on the same number of triangles, and so on. Every point belongs to exactly one orbit, so the orbits split the points into groups. A network where all points form one orbit looks the same from every point. A network with no symmetry other than doing nothing has one orbit for each point.

## The idea

Let $G = (V, E)$ be a graph, simple and undirected, or directed, or vertex-colored; automorphisms keep whatever structure the graph has. Let $\Gamma$ be a subgroup of $\mathrm{Aut}(G)$, often $\Gamma = \mathrm{Aut}(G)$ itself.

**Definition.** The orbit of $v \in V$ under $\Gamma$ is $v^\Gamma = \{ \gamma(v) : \gamma \in \Gamma \}$. The relation "$u$ is in the orbit of $v$" is an [equivalence relation](/equivalence-relation/), because $\Gamma$ contains the identity, inverses and products. Its classes form the **orbit partition** of $V$.

Four facts connect orbits to the rest of the theory.

- **Orbit and stabilizer.** The stabilizer $\Gamma_v = \{\gamma \in \Gamma : \gamma(v) = v\}$ is a [subgroup](/subgroup/), and $|v^\Gamma| \cdot |\Gamma_v| = |\Gamma|$. Applied along a chain of stabilizers, this gives $|\mathrm{Aut}(G)|$ as a product of orbit sizes.
- **Orbits are equitable.** The orbit partition of any $\Gamma \le \mathrm{Aut}(G)$ is an [equitable partition](/equitable-partition/). So the stable partition of [color refinement](/weisfeiler-leman/) is coarser than or equal to the orbit partition: each refinement cell is a union of orbits.
- **Counting orbits.** The [orbit-counting lemma](/burnside-lemma/) gives the number of orbits as the average number of fixed points: $\frac{1}{|\Gamma|} \sum_{\gamma \in \Gamma} |\mathrm{Fix}(\gamma)|$.
- **Orbits on other objects.** $\Gamma$ also acts on edges, on ordered pairs, and on $k$-sets of vertices. The graph is *vertex-transitive* when $V$ is one orbit, *edge-transitive* when $E$ is one orbit, and *arc-transitive* when the ordered pairs $(u, v)$ with $\{u, v\} \in E$ form one orbit.

## Examples

| graph | orbits on vertices | $\lvert \mathrm{Aut} \rvert$ |
|---|---|---|
| path $0 - 1 - 2 - 3$ | $\{0, 3\}, \{1, 2\}$ | 2 |
| star $K_{1,3}$ | center, and the 3 leaves | 6 |
| cycle $C_n$, Petersen graph, any vertex-transitive graph | one orbit | $2n$; 120 |
| [asymmetric](/asymmetric-graph/) graph, for example the Frucht graph | one orbit per vertex | 1 |

**Refinement coarser than orbits.** Take the 6-cycle on vertices $0, \ldots, 5$, two disjoint triangles on $6, \ldots, 11$, and one more vertex $12$ joined to all 12 others. The automorphism group has order $12 \cdot 72 = 864$, and its vertex orbits are $\{0, \ldots, 5\}$, $\{6, \ldots, 11\}$ and $\{12\}$, since the cycle vertices lie on no triangle that avoids vertex 12 and the triangle vertices do. Color refinement stops with only two cells, $\{0, \ldots, 11\}$ and $\{12\}$: every vertex of the first cell has one neighbor in $\{12\}$ and two in its own cell. This is why refinement alone cannot compute orbits, and why tools add [individualization](/individualization-refinement/).

**Orbits in a stabilizer chain.** For the Petersen graph, the orbit of a vertex has size 10, its stabilizer has order 12 and has orbits of sizes 1, 3 and 6 (the vertex, its neighbors, its non-neighbors). Indeed $10 \cdot 12 = 120$.

## Where it is used

- **Pruning isomorphism search.** In [individualization-refinement](/individualization-refinement/), only one vertex per orbit of the known automorphisms needs to be tried at each node; [nauty](/nauty/) and [bliss](/bliss/) keep the orbits of the generators found so far in a union-find structure.
- **Symmetry reduction.** In SAT, integer programming and model checking, variables in one orbit are interchangeable. [Orbital branching](/orbital-branching/) branches on one representative per orbit, and [symmetry reduction](/symmetry-reduction/) explores one state per orbit.
- **Chemistry.** Atoms in one orbit of the molecular graph are equivalent; this gives the number of distinct substitution products and the classes of equivalent atoms in NMR spectra.
- **Counting structures.** The number of distinct ways to color, label or extend a graph up to symmetry is a count of orbits, computed with the orbit-counting lemma and Pólya theory.
- **Spectral graph theory.** The quotient matrix of the orbit partition gives eigenvalues of the graph, as for any equitable partition.

## References
