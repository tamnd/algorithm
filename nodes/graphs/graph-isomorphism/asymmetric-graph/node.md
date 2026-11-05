---
tag: 31AS75
kind: definition
slug: asymmetric-graph
name: Asymmetric graph
aliases:
- rigid graph
- graph with trivial automorphism group
area: graphs/graph-isomorphism
level: intro
summary: A graph whose only automorphism is the identity.
prereqs: [graph-automorphism-group]
see_also: [almost-all-graphs-asymmetric, graph-automorphism, automorphism-orbit, canonical-labeling, tree-isomorphism]
sources:
  - paper: doi:10.1007/BF01895716
    title: Paul Erdős and Alfréd Rényi, Asymmetric graphs, Acta Mathematica Academiae Scientiarum Hungaricae 14, 295 to 315 (1963)
    locator: the whole paper (the definition, the probability that a random graph is asymmetric, and the measure of asymmetry)
  - book: isbn:9780387952208
    title: Chris Godsil and Gordon Royle, Algebraic Graph Theory, Springer, Graduate Texts in Mathematics 207, 2001
    locator: Chapter 1, Graphs (isomorphisms, automorphisms and homomorphisms)
  - book: isbn:9780521797221
    title: Béla Bollobás, Random Graphs, second edition, Cambridge University Press, 2001
    locator: Chapter 9, The automorphism group (asymmetry of random graphs)
---

An asymmetric graph is a graph whose [automorphism group](/graph-automorphism-group/) is trivial: the identity is the only permutation of the vertices that maps edges to edges and non-edges to non-edges. Each vertex of an asymmetric graph can be told apart from every other vertex by the structure alone. Small graphs are rarely asymmetric, but [almost all large graphs are](/almost-all-graphs-asymmetric/).

## Definition

A graph $G = (V, E)$ is **asymmetric** when

$$\mathrm{Aut}(G) = \{ \mathrm{id}_V \},$$

that is, when for every permutation $\sigma \ne \mathrm{id}$ of $V$ there are vertices $u, v$ with $\{u, v\} \in E$ and $\{\sigma(u), \sigma(v)\} \notin E$, or the other way round. The same definition applies to directed and colored graphs with their own notion of automorphism; adding colors can only shrink the group, so a colored graph can be asymmetric while its uncolored version is not.

Equivalent forms:

- $G$ has exactly $n!$ distinct labelings on a fixed vertex set of size $n$, because the number of labeled copies is $n!/|\mathrm{Aut}(G)|$.
- Every [orbit](/automorphism-orbit/) of $\mathrm{Aut}(G)$ on $V$ is a single vertex, and every isomorphism from $G$ to another graph $H$ is unique when it exists.
- The complement $\overline G$ is asymmetric, because $\mathrm{Aut}(G) = \mathrm{Aut}(\overline G)$.

Some authors call such a graph *rigid*. Others use *rigid* for the stronger property that the only endomorphism (an edge-preserving map, not necessarily a bijection) is the identity. On this site, asymmetric means trivial automorphism group.

## Examples and non-examples

**The smallest examples.** The graph with one vertex is asymmetric. Every graph with 2 to 5 vertices has a non-identity automorphism. On 6 vertices, 8 of the 156 isomorphism classes are asymmetric, and 5760 of the $2^{15} = 32768$ labeled graphs on $\{0, \ldots, 5\}$ are asymmetric ($5760 = 8 \cdot 6!$, about 17.6 percent).

**A 6-vertex example.** Take the path $0 - 1 - 2 - 3 - 4$ and add vertex 5 adjacent to 2 and 3. The degrees are $0{:}1, 1{:}2, 2{:}3, 3{:}3, 4{:}1, 5{:}2$. An automorphism keeps degrees, so it fixes or swaps $\{2, 3\}$, $\{0, 4\}$ and $\{1, 5\}$. Vertex 1 is the degree-2 vertex adjacent to a leaf, and 5 is not, so both are fixed; then 2 (adjacent to 1) and 3 are fixed, and so are 0 and 4. The group is trivial.

**A non-example on 6 vertices.** The 6-cycle with one chord $\{2, 5\}$ (edges $01, 12, 23, 34, 45, 50, 25$) has the automorphism swapping $1 \leftrightarrow 3$ and $0 \leftrightarrow 4$ while fixing 2 and 5, so it is not asymmetric.

**Trees.** The smallest asymmetric tree has 7 vertices: a center with three paths of lengths 1, 2 and 3 attached. No tree with 2 to 6 vertices is asymmetric.

**Regular graphs.** Regularity does not force symmetry. The Frucht graph is 3-regular with 12 vertices and 18 edges and has only the identity automorphism.

**Non-examples.** Complete graphs, cycles, paths with at least 2 vertices, and every vertex-transitive graph with at least 2 vertices have non-trivial automorphisms. A graph with two leaves at the same vertex always has the automorphism that swaps them.

## Related definitions

- [Automorphism group](/graph-automorphism-group/): the group that is trivial here.
- [Almost all graphs are asymmetric](/almost-all-graphs-asymmetric/): the fraction of asymmetric graphs among the labeled graphs on $n$ vertices tends to 1.
- [Graph automorphism problem](/graph-automorphism/): decide whether a graph is asymmetric, or find its group. Deciding asymmetry reduces to [graph isomorphism](/graph-isomorphism-problem/).
- [Canonical labeling](/canonical-labeling/): for an asymmetric graph the canonical labeling is unique, and the search tree of [individualization-refinement](/individualization-refinement/) has no automorphisms to prune.

## References
