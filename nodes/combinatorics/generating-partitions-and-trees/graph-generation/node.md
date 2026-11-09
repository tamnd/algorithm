---
tag: SSZBHT
kind: problem
slug: graph-generation
name: Generating graphs
aliases:
- Graph enumeration
- Isomorph-free generation of graphs
- Listing unlabeled graphs
area: combinatorics/generating-partitions-and-trees
level: core
summary: Producing graphs of a given kind, such as all graphs with n vertices or random graphs, for testing or enumeration.
prereqs: [labeled-graph, graph-isomorphism-problem, canonical-labeling]
see_also: [orderly-generation, canonical-augmentation, nauty, erdos-renyi-model, configuration-model, free-tree-generation, graph-isomorphism-problem, counting-labeled-graphs]
sources:
  - paper: doi:10.1006/jagm.1997.0898
    title: Brendan D. McKay, Isomorph-free exhaustive generation, Journal of Algorithms 26(2) (1998), 306 to 324
    locator: the whole paper (canonical construction path and its use for graphs)
  - paper: doi:10.1016/S0167-5060(08)70325-X
    title: Ronald C. Read, Every one a winner, or how to avoid isomorphism search when cataloguing combinatorial configurations, Annals of Discrete Mathematics 2 (1978), 107 to 120
    locator: the whole paper (orderly generation of graphs)
  - url: https://users.cecs.anu.edu.au/~bdm/data/graphs.html
    title: Brendan McKay, Combinatorial Data, Simple graphs
    locator: the counts of all graphs and of connected graphs with up to 10 vertices
  - url: https://users.cecs.anu.edu.au/~bdm/nauty/
    title: Brendan McKay and Adolfo Piperno, nauty and Traces
    locator: the gtools suite (geng, genbg, gentreeg, genrang)
  - url: https://oeis.org/A000088
    title: OEIS A000088, Number of simple graphs on n unlabeled nodes
    locator: the terms and the asymptotic formula
---

Graph generation is the task of producing graphs of a given kind: every graph with $n$ vertices up to isomorphism, every labeled graph, every graph in a class such as trees or regular graphs, or random graphs from a given distribution. Labeled graphs are just bit strings of length $\binom{n}{2}$, but unlabeled graphs need isomorph rejection, and their number $g_n$ grows like $2^{\binom{n}{2}} / n!$: $1, 2, 4, 11, 34, 156, 1044, 12346, \ldots$ for $n = 1, 2, \ldots$. The standard exhaustive methods are [orderly generation](/orderly-generation/) and [canonical augmentation](/canonical-augmentation/), and the standard random model is the [Erdős-Rényi model](/erdos-renyi-model/).

## In plain words

Programs that work on graphs need test graphs, and mathematicians check ideas on all small graphs. So we want a machine that produces graphs.

If the dots have names, a graph is just a yes or no for each pair of dots, and listing all graphs is like counting in binary. If the dots have no names, many of these lists show the same picture, and we want each picture once. That is harder: we must recognize when two graphs are the same and skip the copies, without comparing every new graph with all old ones.

Sometimes we do not need all graphs, only a few random ones. Then the task is to draw graphs at random, with the right chances.

## Definition

A *graph* $G = (V, E)$ has a finite vertex set $V$ and a set $E$ of unordered pairs of distinct vertices. A *labeled graph* on $n$ vertices has $V = \{1, \ldots, n\}$; two graphs are *isomorphic* if a bijection of their vertex sets maps edges to edges. Let $\mathcal{G}_n$ be the set of isomorphism classes of graphs with $n$ vertices, and $g_n = |\mathcal{G}_n|$.

**Exhaustive generation.**

- **Input:** $n$, and optionally a property $P$ of graphs, such as connected, bipartite, triangle-free, or a range of edge counts.
- **Output:** one representative of each class in $\mathcal{G}_n$ that satisfies $P$, each exactly once.

**Random generation.**

- **Input:** $n$ and a distribution on graphs with $n$ vertices, such as $G(n, p)$, the uniform distribution on graphs with $m$ edges, or the uniform distribution on $d$-regular graphs.
- **Output:** one graph drawn from the distribution, or a stream of independent draws.

**Cost model.** For exhaustive generation the cost is the total time divided by the number of outputs, with each graph visited in place. For random generation it is the expected time per graph, in the [word RAM](/word-ram/) with a source of random bits.

## Variants

- **Labeled or unlabeled.** Labeled graphs on $n$ vertices number $2^{\binom{n}{2}}$ and need no isomorphism test; see [counting labeled graphs](/counting-labeled-graphs/). Unlabeled graphs number $g_n$.
- **Graph classes.** Connected graphs, trees (see [free tree generation](/free-tree-generation/)), bipartite graphs, [regular graphs](/regular-graph/), [planar graphs](/planar-graph/), graphs with a forbidden subgraph or a bounded degree. A class that is closed under deleting a vertex can be pruned during the search; other classes are filtered at the output.
- **Other structures.** Directed graphs, tournaments, multigraphs, [hypergraphs](/hypergraph/), and graphs with colored vertices are generated with the same methods and a different group action.
- **Order and splitting.** Some uses need the graphs by number of edges or in a fixed order; large runs are split into independent parts by a residue class, so that each part runs on its own machine.
- **Random models.** $G(n, p)$, where each edge is present with probability $p$; $G(n, m)$, a uniform graph with $m$ edges; random regular graphs or graphs with a given degree sequence through the [configuration model](/configuration-model/); uniform random unlabeled graphs; and models for real networks, such as preferential attachment.

## Examples

- $n = 3$: four unlabeled graphs, with $0$, $1$, $2$ and $3$ edges; eight labeled graphs.
- $n = 4$: $11$ unlabeled graphs: the empty graph, one edge, two disjoint edges, the path $P_3$ plus an isolated vertex, the triangle plus an isolated vertex, the star $K_{1,3}$, the path $P_4$, the cycle $C_4$, the paw (a triangle with a pendant edge), $K_4$ minus an edge, and $K_4$. Six of them are connected. There are $64$ labeled graphs.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| all graphs $g_n$ | 1 | 2 | 4 | 11 | 34 | 156 | 1044 | 12346 | 274668 | 12005168 |
| connected graphs | 1 | 1 | 2 | 6 | 21 | 112 | 853 | 11117 | 261080 | 11716571 |

Further, $g_{11} = 1018997864$ and $g_{12} = 165091172592$. The values follow from [Burnside's lemma](/burnside-lemma/) applied to the action of the symmetric group on vertex pairs.

## Known algorithms

| task | method | cost |
|---|---|---|
| all labeled graphs | count in binary, or a [Gray code](/binary-reflected-gray-code/) on the $\binom{n}{2}$ edge bits | $O(1)$ amortized per graph, one edge change per step with a Gray code |
| all unlabeled graphs | [orderly generation](/orderly-generation/) (Read, Faradzev 1978) | one canonicity test per candidate |
| all unlabeled graphs | [canonical augmentation](/canonical-augmentation/) by vertices (McKay 1998), as in geng | one automorphism group per graph and cheap rejection of most candidates |
| all free trees | [Wright-Richmond-Odlyzko-McKay](/wright-richmond-odlyzko-mckay/) | $O(1)$ amortized per tree |
| random graph $G(n, p)$ | flip a coin per pair, or jump over absent pairs with geometric gaps | $O(n^2)$, or $O(n + m)$ expected with jumps |
| random $d$-regular graph | [configuration model](/configuration-model/) with rejection of loops and multiple edges | expected $O(nd)$ for fixed $d$ |

- **Labeled graphs.** The $\binom{n}{2}$ edge indicators form a bit string, so any [subset generation](/gray-code/) method lists the labeled graphs.
- **Orderly generation.** Add edges in a fixed order of vertex pairs, and keep a graph only if its adjacency code is the largest among all relabelings. The parent of a canonical graph, with its last edge removed, is canonical, so each class is reached once, with no table of earlier outputs.
- **Canonical augmentation.** Add a vertex joined to a subset of the old vertices, one subset per orbit of the parent's automorphism group, and accept the new graph only if the new vertex lies in the orbit that a canonical labeling, computed with a program such as [nauty](/nauty/), names for deletion. Pruning by degree, by triangles or by connectivity happens during the search.
- **Generic isomorph rejection.** Generate many graphs, compute a canonical form for each with [canonical labeling](/canonical-labeling/), and keep one per form in a hash table. It is simple, but it stores all outputs and wastes work on duplicates.

## Bounds

- **Output size.** $g_n \sim 2^{\binom{n}{2}} / n!$, because almost all graphs have no symmetry. The ratio $2^{\binom{n}{2}} / (n!\, g_n)$ is $0.25$ at $n = 5$, $0.81$ at $n = 10$ and $0.93$ at $n = 12$. So exhaustive lists are practical only up to $n = 10$ or $11$; for larger $n$, only restricted classes can be listed.
- **Lower bound.** Every exhaustive method needs $\Omega(g_n)$ time in the in-place model, and $\Omega(n^2 g_n)$ bits to write adjacency matrices.
- **Isomorphism.** The canonicity tests need graph isomorphism work. No polynomial-time algorithm is known for [graph isomorphism](/graph-isomorphism-problem/), and Babai's algorithm runs in quasi-polynomial time. For random graphs the tests are fast, so in practice the cost per output is small.

## Reductions

- **Counting.** The number of classes follows from [Burnside's lemma](/burnside-lemma/) or the [Pólya enumeration theorem](/polya-enumeration-theorem/), without generation; the connected graphs follow from all graphs by the logarithm of the generating function.
- **Graphs and isomorphism.** Exhaustive generation up to isomorphism reduces to computing canonical forms; conversely, it does not need pairwise isomorphism tests between outputs.
- **Complements.** A graph with $m$ edges matches its complement with $\binom{n}{2} - m$ edges, so only the graphs with at most half of the edges must be generated.
- **Connected graphs.** Every graph is a multiset of connected graphs, so connected graphs suffice for many tasks, and some generators produce connected graphs directly.

## Applications

- Testing graph algorithms and finding counterexamples on every small graph.
- Testing conjectures in graph theory, and searching for extremal graphs such as Ramsey graphs and cages.
- Catalogues of chemical structures and of small graphs with special properties.
- Random graphs as benchmarks and as null models in network science.

## References
