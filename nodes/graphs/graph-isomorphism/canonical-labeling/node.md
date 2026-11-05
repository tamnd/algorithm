---
tag: Y65876
kind: problem
slug: canonical-labeling
name: Canonical labeling
aliases:
- canonical form
- graph canonization
- canonization
area: graphs/graph-isomorphism
level: core
summary: Map each graph to a unique canonical representative so that isomorphism reduces to equality of representatives.
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: exp((log n)^(O(1)))}
prereqs: [graph-isomorphism-problem, canonical-form, permutation]
see_also: [nauty, bliss, individualization-refinement, ahu-algorithm, graph-automorphism, weisfeiler-leman, canonicalization, hash-function]
sources:
  - paper: doi:10.1016/j.jsc.2013.09.003
    title: Brendan D. McKay and Adolfo Piperno, Practical graph isomorphism, II, Journal of Symbolic Computation 60, 94 to 112 (2014)
    locator: Sections 2 and 3 (canonical forms, the search tree and node invariants)
  - paper: "László Babai and Eugene M. Luks, Canonical labeling of graphs, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC 1983), 171 to 183"
    locator: the whole paper (canonical forms in exp(O(n^(1/2) log n)) time and in n^(O(d)) time for degree d)
  - paper: "László Babai, Canonical form for graphs in quasipolynomial time, preliminary report, Proceedings of the 51st ACM Symposium on Theory of Computing (STOC 2019), 1237 to 1246"
    locator: the whole paper (extension of the quasipolynomial isomorphism test to canonical forms)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 7, Computing isomorphism (certificates and canonical forms of graphs)
---

Canonical labeling asks for a function that maps every graph to a labeled copy of it, its canonical form, so that two graphs get the same canonical form exactly when they are isomorphic. With such a function, [graph isomorphism](/graph-isomorphism-problem/) becomes a string comparison, and a large collection of graphs can be stored without duplicates under a hash of the canonical form. Canonical labeling is at least as hard as isomorphism testing, but the known algorithms solve both in similar time: the practical tools [nauty](/nauty/), Traces and [bliss](/bliss/) compute canonical forms, and Babai extended his quasipolynomial bound to canonical forms in 2019.

## In plain words

The names of the points of a network are arbitrary, so the same network can be written down in many ways. A canonical labeling is a fixed rule that picks one of these ways, the standard one, and the rule must not depend on how the network was first written. Then two networks are the same exactly when their standard versions are written the same way, letter for letter. This turns a hard comparison of two networks into an easy comparison of two texts, and it lets you keep a catalog of networks and look one up fast.

## Definition

Graphs are simple, undirected and possibly vertex-colored, on the vertex set $[n] = \{1, \ldots, n\}$. For a permutation $\sigma$ of $[n]$, $G^\sigma$ is the graph with edges $\{\sigma(u), \sigma(v)\}$ for $\{u, v\} \in E(G)$ and colors moved along.

**Canonical form.**
- Input: a graph $G$ on $[n]$.
- Output: a graph $\mathrm{can}(G)$ on $[n]$ such that
  1. $\mathrm{can}(G) \cong G$, and
  2. $\mathrm{can}(G^\sigma) = \mathrm{can}(G)$ for every permutation $\sigma$ (equality as labeled graphs).

**Canonical labeling.** Output a permutation $\lambda_G$ with $G^{\lambda_G} = \mathrm{can}(G)$. It is unique up to composing with an automorphism of $G$ first.

Conditions 1 and 2 give $\mathrm{can}(G) = \mathrm{can}(H) \iff G \cong H$. A weaker object is a **complete invariant**, any function $f$ with $f(G) = f(H) \iff G \cong H$; the canonical form is a complete invariant that is itself a graph isomorphic to the input.

## Variants

- **Directed, colored and edge-labeled graphs.** The same definition, with colors and labels moved by $\sigma$. Vertex colors are often ordered, and the canonical form must keep the order of color classes.
- **Canonical forms for restricted classes.** For [trees](/tree-isomorphism/), the [AHU code](/ahu-algorithm/) is a canonical form in linear time. Planar graphs have linear-time canonical forms by the same route as [planar isomorphism](/planar-graph-isomorphism/), and Lindell's tree canonization runs in logarithmic space.
- **Other structures.** Canonical forms of hypergraphs, matrices, codes, designs and molecules reduce to canonical forms of colored graphs by encoding the structure as a graph.
- **Canonical forms versus isomorphism tests.** An isomorphism test only compares two inputs. It is open whether canonical forms reduce to isomorphism testing in polynomial time in general; for most known algorithms the canonical version costs about the same.

## Examples

**The largest adjacency string.** One canonical form takes, over all $n!$ permutations $\sigma$, the graph $G^\sigma$ whose upper-triangle string, with pairs ordered $12, 13, \ldots, 1n, 23, \ldots$, is largest. It is canonical because the set $\{G^\sigma\}$ depends only on the isomorphism class. On 4 vertices, with pairs in the order $01, 02, 03, 12, 13, 23$:

| graph | edges | canonical string | permutations that reach it |
|---|---|---|---|
| path $0 - 1 - 2 - 3$ | $01, 12, 23$ | 110010 | 2 |
| the same path relabeled | $02, 21, 13$ | 110010 | 2 |
| star $K_{1,3}$ | $01, 02, 03$ | 111000 | 6 |
| triangle with a pendant edge | $01, 12, 20, 23$ | 111100 | 2 |

The two paths get the same string, so they are isomorphic; the number of permutations that reach the maximum is $|\mathrm{Aut}(G)|$. This form costs $n! \cdot n^2$ time and only serves as a definition.

**Trees.** The [AHU](/ahu-algorithm/) code of a rooted tree is a canonical form: the nested sorted lists of children's codes.

**Molecules.** Chemistry databases store each compound under a canonical string of its labeled molecular graph, so that the same molecule entered with atoms in another order is found.

## Known algorithms

| algorithm | scope | worst-case time |
|---|---|---|
| maximum over all permutations | all graphs | $O(n! \cdot n^2)$ |
| [AHU](/ahu-algorithm/) | trees | $O(n)$ |
| Babai, Erdős and Selkow (1980) | almost all graphs, by degree refinement | $O(n^2)$ |
| Babai and Luks (1983) | all graphs | $\exp(O(\sqrt{n \log n}))$ |
| Babai and Luks (1983) | maximum degree $d$ | $n^{O(d)}$ |
| Babai (2019) | all graphs | quasipolynomial, $\exp((\log n)^{O(1)})$ |
| [nauty](/nauty/) and Traces, [bliss](/bliss/) | all graphs, by [individualization-refinement](/individualization-refinement/) | exponential on some families, fast in practice |

The practical tools search a tree of [equitable partitions](/equitable-partition/) and define the canonical form as the leaf with the best value of a fixed function, pruning with automorphisms they find on the way. They do not compute the maximal adjacency string over all permutations; their canonical form depends on the tool, its version and its options.

## Bounds

- **Lower bound.** Canonical labeling is at least as hard as [graph isomorphism](/graph-isomorphism-problem/), because one isomorphism test is two canonical forms and a comparison.
- **Upper bound.** Quasipolynomial time. Babai announced the isomorphism test in 2015 and extended it to canonical forms in a preliminary report at STOC 2019; before that, the best general bound for canonical forms was the $\exp(O(\sqrt{n \log n}))$ of Babai and Luks (1983).
- **Practical limits.** Neuen and Schweitzer (2017) built graphs on which every individualization-refinement algorithm, and so every canonical labeling tool of the nauty type, takes exponential time.
- **Through color refinement.** If [color refinement](/weisfeiler-leman/) gives a discrete partition, ordering the vertices by color is a canonical labeling, in $O((n + m) \log n)$ time. This happens for almost all graphs, but never for graphs with non-trivial automorphisms.

## Reductions

- **Isomorphism to canonical form.** $G \cong H \iff \mathrm{can}(G) = \mathrm{can}(H)$.
- **Automorphism group as a by-product.** Individualization-refinement tools return generators of $\mathrm{Aut}(G)$ along with the canonical form, so canonical labeling solves the [graph automorphism problem](/graph-automorphism/) in practice.
- **Colored to uncolored.** A vertex-colored graph can be encoded as an uncolored graph with gadgets, but the practical tools take colors directly, as the initial partition of refinement.
- **Isomorphism classes of a list.** For $N$ graphs, compute $N$ canonical forms and sort or hash them; this beats $\binom N2$ pairwise tests.

## Applications

- Generating all graphs of a class without duplicates, by canonical augmentation (McKay's method) or by keeping only canonical representatives, for example in `geng`.
- Chemical structure databases and registry systems, with canonical strings of molecular graphs.
- Hashing and memoizing combinatorial objects: designs, codes, Latin squares, and states of search procedures under symmetry.
- Deduplicating isomorphic subproblems in SAT and constraint solving, and in [symmetry reduction](/symmetry-reduction/).

## References
