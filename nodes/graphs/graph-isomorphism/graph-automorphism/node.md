---
tag: E9YPRK
kind: problem
slug: graph-automorphism
name: Graph automorphism problem
aliases:
- automorphism group computation
- GA
area: graphs/graph-isomorphism
level: core
summary: Compute the automorphism group of a graph, usually given by generators, or decide whether a graph has a non-trivial automorphism.
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: exp((log n)^(O(1)))}
prereqs: [graph-automorphism-group, graph-isomorphism-problem]
see_also: [automorphism-orbit, asymmetric-graph, canonical-labeling, nauty, bliss, gi-completeness, symmetry-reduction, burnside-lemma]
sources:
  - paper: doi:10.1016/0020-0190(79)90004-8
    title: Rudolf Mathon, A note on the graph isomorphism counting problem, Information Processing Letters 8(3), 131 to 132 (1979)
    locator: the whole note (counting isomorphisms and computing the automorphism group reduce to deciding isomorphism)
  - book: isbn:9780817636807
    title: Johannes Köbler, Uwe Schöning and Jacobo Torán, The Graph Isomorphism Problem, Its Structural Complexity, Birkhäuser, 1993
    locator: Chapter 1 (graph automorphism, generators of the automorphism group, and reductions to graph isomorphism)
  - paper: "Anna Lubiw, Some NP-complete problems similar to graph isomorphism, SIAM Journal on Computing 10(1), 11 to 21 (1981)"
    locator: the whole paper (fixed-point-free automorphism is NP-complete)
  - paper: doi:10.1016/j.jsc.2013.09.003
    title: Brendan D. McKay and Adolfo Piperno, Practical graph isomorphism, II, Journal of Symbolic Computation 60, 94 to 112 (2014)
    locator: Sections 2 and 3 (automorphism pruning and the generators found during the search)
---

The graph automorphism problem asks for the symmetries of one graph. In its decision form (GA) it asks whether a graph has any automorphism other than the identity, that is, whether it is not [asymmetric](/asymmetric-graph/). In its computation form it asks for the whole [automorphism group](/graph-automorphism-group/), given by a short list of generators, together with its order and its [orbits](/automorphism-orbit/). Both forms reduce to [graph isomorphism](/graph-isomorphism-problem/) in polynomial time, and the decision form is not known to be as hard as isomorphism.

## In plain words

A symmetry of a network is a way to move its points around so that the links look exactly as before. Every network has the trivial symmetry that moves nothing. The question is whether there are others, and if so, to list them all. Even a network with a few dozen points can have more symmetries than you could ever write down, so the answer is a short list of basic symmetries from which all others are built by doing one after another. Practical tools find this list while they search for a standard labeling of the network.

## Definition

Graphs are simple and undirected, possibly with vertex colors that automorphisms must keep; directed graphs and edge labels are handled the same way. $\mathrm{Aut}(G)$ is the group of permutations $\sigma$ of $V$ with $\{u, v\} \in E \iff \{\sigma(u), \sigma(v)\} \in E$ that keep the colors.

**Graph automorphism (decision, GA).**
- Input: a graph $G$.
- Output: yes when $\mathrm{Aut}(G) \ne \{\mathrm{id}\}$; otherwise no.

**Automorphism group (computation).**
- Input: a graph $G$ with $n$ vertices.
- Output: a set $S$ of permutations with $\langle S \rangle = \mathrm{Aut}(G)$. Every subgroup of the [symmetric group](/symmetric-group/) $S_n$ has a generating set of at most $n - 1$ elements, so the output has polynomial size even when $|\mathrm{Aut}(G)|$ is as large as $n!$.

**Related outputs.** The order $|\mathrm{Aut}(G)|$; the orbit partition of $V$; a strong generating set with respect to a base, which supports membership tests in polynomial time.

## Variants

- **Counting automorphisms.** Output $|\mathrm{Aut}(G)|$. With a stabilizer chain, it is the product of orbit sizes along the chain.
- **Fixed-point-free automorphism.** Decide whether some automorphism moves every vertex. This is [NP-complete](/np-complete/) (Lubiw 1981), even though GA is not believed to be: asking for an automorphism with a prescribed property can be much harder than asking for any non-trivial one.
- **Orbits only.** Compute the orbit partition. Color refinement gives a partition that every orbit lies inside, which equals the orbit partition for many graphs but not all.
- **Restricted classes.** Trees, planar graphs and graphs of bounded degree have polynomial algorithms for the whole group, by the same methods as their isomorphism tests.

## Examples

| graph | $\lvert \mathrm{Aut} \rvert$ | a generating set |
|---|---|---|
| path $P_n$, $n \ge 2$ | 2 | the reversal |
| cycle $C_n$, $n \ge 3$ | $2n$ | the rotation $i \mapsto i + 1$ and the reflection $i \mapsto -i$ |
| complete graph $K_n$ | $n!$ | the transposition $(1\,2)$ and the cycle $(1\,2 \cdots n)$ |
| Petersen graph | 120 | three permutations, from a stabilizer chain of orbit sizes 10, 6, 2 |
| Frucht graph | 1 | the empty set; GA answers no |

**A stabilizer chain for the Petersen graph.** Take the vertices as the 2-element subsets of $\{0, \ldots, 4\}$, adjacent when disjoint, and number them $0 = \{0,1\}, 1 = \{0,2\}, 2 = \{0,3\}, \ldots$ in lexicographic order. A brute-force search finds 120 automorphisms. The orbit of vertex 0 has 10 vertices. The automorphisms that fix 0 move vertex 1 (a non-neighbor of 0) onto 6 vertices, all the non-neighbors of 0. Those that fix 0 and 1 move vertex 2 onto 2 vertices, and those that fix 0, 1 and 2 fix everything. So $|\mathrm{Aut}| = 10 \cdot 6 \cdot 2 = 120$, the order of $S_5$.

## Known algorithms

| algorithm | output | worst-case time |
|---|---|---|
| brute force over permutations | the whole group as a list | $O(n! \cdot n^2)$ |
| reduction to an isomorphism oracle (Mathon 1979) | generators and order | polynomially many oracle calls |
| [nauty](/nauty/), Traces, [bliss](/bliss/), saucy | generators, order, orbits | exponential on some families, fast in practice |
| Babai (2015), via the isomorphism framework | generators | quasipolynomial |
| [Luks](/luks-algorithm/) (1982) | generators, degree $d$ | $n^{O(d)}$ |
| [color refinement](/weisfeiler-leman/) | an outer bound on the orbits | $O((n + m) \log n)$ |

The practical tools find automorphisms as pairs of leaves of the [individualization-refinement](/individualization-refinement/) search tree with equal graphs, and store them as generators. Each new generator prunes the rest of the search.

## Bounds

- **Upper bound.** Quasipolynomial time, $\exp((\log n)^{O(1)})$, as for graph isomorphism.
- **GA reduces to GI.** $G$ has a non-trivial automorphism exactly when, for some pair $u \ne v$, the graph $G$ with $u$ colored and the graph $G$ with $v$ colored are isomorphic. That is $O(n^2)$ isomorphism tests on colored graphs.
- **GI does not obviously reduce to GA.** No reduction from GI to GA is known, so GA may be strictly easier. GA has the same structural properties as GI: it is in NP, in coAM, and low for the polynomial hierarchy.
- **Computing the group is GI-equivalent.** By Mathon (1979) and the reductions above, computing generators of $\mathrm{Aut}(G)$, computing $|\mathrm{Aut}(G)|$, and counting isomorphisms are all polynomial-time equivalent to deciding GI.
- **Lower bound.** No good lower bound is known.

## Reductions

- **To isomorphism.** As in the bounds above, by marking pairs of vertices. Finding generators uses a stabilizer chain: for each base vertex, find its orbit under the current stabilizer by isomorphism tests with marks, and record one automorphism per orbit element.
- **From isomorphism, for connected graphs.** For connected $G$ and $H$, $G \cong H$ exactly when $\mathrm{Aut}(G \uplus H)$ has an element that swaps the two components. So generators of $\mathrm{Aut}(G \uplus H)$ decide GI: look for a generator that maps a vertex of $G$ into $H$.
- **Counting.** By the [orbit-counting lemma](/burnside-lemma/), the number of distinct labelings of $G$ on $[n]$ is $n! / |\mathrm{Aut}(G)|$.

## Applications

- Symmetry breaking in SAT, constraint programming and integer programming: compute $\mathrm{Aut}$ of a graph built from the instance and add constraints or use [orbital branching](/orbital-branching/).
- Counting distinct labelings and enumerating structures up to isomorphism.
- Chemistry: the symmetry number of a molecule, used in statistical mechanics, and the classes of equivalent atoms.
- Design theory and coding theory: automorphism groups of designs, codes and finite geometries.
- Pruning the search in [canonical labeling](/canonical-labeling/), where the group is found along the way.

## References
