---
tag: KAY76S
kind: problem
slug: graph-isomorphism-problem
name: Graph isomorphism
aliases:
- graph isomorphism problem
- GI
area: graphs/graph-isomorphism
level: core
summary: Problem of deciding whether two graphs are the same up to relabeling of their vertices; in NP, not known to be in P, and solvable in quasipolynomial time.
model: word-ram
complexity:
  vars: {n: the number of vertices of each graph}
  time: {worst: exp((log n)^(O(1)))}
prereqs: [graph-isomorphism-definition, graph-isomorphism-in-np]
see_also: [weisfeiler-leman, canonical-labeling, graph-automorphism, gi-completeness, babai-quasipolynomial-algorithm, nauty, subgraph-isomorphism, np-intermediate]
sources:
  - paper: doi:10.1002/jgt.3190010410
    title: Ronald C. Read and Derek G. Corneil, The graph isomorphism disease, Journal of Graph Theory 1(4), 339 to 363 (1977)
    locator: the whole paper (survey of methods and of the status of the problem)
  - book: isbn:9780817636807
    title: Johannes Köbler, Uwe Schöning and Jacobo Torán, The Graph Isomorphism Problem, Its Structural Complexity, Birkhäuser, 1993
    locator: Chapter 1 (decision, search and counting versions) and Chapter 2 (interactive proofs and lowness)
  - paper: doi:10.1145/2897518.2897542
    title: László Babai, Graph isomorphism in quasipolynomial time, Proceedings of the 48th ACM Symposium on Theory of Computing (STOC 2016), 684 to 697
    locator: the whole paper (extended abstract; full text in arXiv:1512.03547)
  - paper: doi:10.1145/3372123
    title: Martin Grohe and Pascal Schweitzer, The graph isomorphism problem, Communications of the ACM 63(11), 128 to 134 (2020)
    locator: the whole article (survey of theory and practice)
  - paper: doi:10.1016/j.jsc.2013.09.003
    title: Brendan D. McKay and Adolfo Piperno, Practical graph isomorphism, II, Journal of Symbolic Computation 60, 94 to 112 (2014)
    locator: Sections 1 to 3 (the practical approach by individualization and refinement)
---

The graph isomorphism problem (GI) asks whether two given graphs are [isomorphic](/graph-isomorphism-definition/): whether some bijection between their vertex sets maps edges exactly onto edges. It is [in NP](/graph-isomorphism-in-np/), it is not known to be in polynomial time, and it is not believed to be [NP-complete](/np-complete/), so it is the main natural candidate for an [NP-intermediate](/np-intermediate/) problem. Since Babai's work of 2015 the best known worst-case bound is quasipolynomial time, and in practice tools such as [nauty](/nauty/) solve most instances with thousands of vertices fast.

## In plain words

You get two networks with the same number of points. The names of the points mean nothing; only the pattern of links counts. The question is whether the two networks are the same pattern. One way is to try every renaming of the points, but the number of renamings grows faster than any power of the size. Simple checks, such as counting links at each point, often show quickly that two networks differ, but some different networks pass all simple checks. No one knows a method that is always fast, and no one has shown that the problem is as hard as the hardest search problems.

## Definition

Graphs are finite, simple and undirected unless a variant says otherwise. Two graphs $G = (V, E)$ and $H = (W, F)$ are isomorphic, $G \cong H$, when there is a bijection $\varphi : V \to W$ with $\{u, v\} \in E \iff \{\varphi(u), \varphi(v)\} \in F$ for all $u, v \in V$.

**Graph isomorphism (decision).**
- Input: graphs $G$ and $H$ on $n$ vertices each, as adjacency lists or adjacency matrices.
- Output: yes when $G \cong H$; otherwise no.

**Search version.** Output an isomorphism $\varphi$ when one exists.

**Counting version.** Output the number of isomorphisms. It equals $|\mathrm{Aut}(G)|$ when $G \cong H$ and $0$ otherwise.

The search and counting versions reduce to the decision version in polynomial time (Mathon 1979 for counting). So all three have the same complexity up to polynomial factors.

## Variants

- **Directed graphs, multigraphs, vertex-colored and edge-labeled graphs.** The bijection must keep arc directions, multiplicities, vertex colors and edge labels. Each of these reduces to the plain undirected version by small gadgets, so all are [GI-complete](/gi-completeness/).
- **[Canonical labeling](/canonical-labeling/).** Compute a labeled copy $\mathrm{can}(G)$ with $\mathrm{can}(G) = \mathrm{can}(H) \iff G \cong H$. It solves GI by one comparison, and it lets a database of graphs be searched by hash. It is at least as hard as GI.
- **[Graph automorphism](/graph-automorphism/).** Decide whether one graph has a non-trivial automorphism, or compute generators of its [automorphism group](/graph-automorphism-group/). It reduces to GI.
- **Restricted classes.** GI is polynomial for [trees](/tree-isomorphism/), [planar graphs](/planar-graph-isomorphism/), graphs of [bounded degree](/bounded-degree-graph-isomorphism/), bounded genus, bounded [treewidth](/treewidth/), bounded eigenvalue multiplicity, and graphs that exclude a fixed [minor](/graph-minor/). It stays GI-complete for bipartite graphs, regular graphs, chordal graphs and [line graphs](/line-graph/).
- **Related problems that are NP-complete.** [Subgraph isomorphism](/subgraph-isomorphism/), [maximum common subgraph](/maximum-common-subgraph/), and [graph edit distance](/graph-edit-distance/). Deciding whether a graph has a fixed-point-free automorphism is also NP-complete (Lubiw 1981).

## Examples

**An isomorphic pair.** Let $G$ be the cycle $0 - 1 - 2 - 3 - 4 - 0$ and $H$ the pentagram with edges $02, 24, 41, 13, 30$. The map $\varphi = (0, 1, 2, 3, 4) \mapsto (0, 2, 4, 1, 3)$ is an isomorphism. A brute-force search over the $5! = 120$ bijections finds exactly 10 isomorphisms, which is $|\mathrm{Aut}(C_5)| = 10$.

**A non-isomorphic pair that degrees cannot separate.** The 6-cycle $C_6$ and two disjoint triangles $2K_3$ are both 2-regular on 6 vertices with 6 edges. None of the $720$ bijections is an isomorphism, since $2K_3$ is disconnected and has triangles. [Color refinement](/weisfeiler-leman/) gives every vertex of both graphs the same color, so it cannot separate them.

**A hard pair.** The $4 \times 4$ rook's graph and the Shrikhande graph are both strongly regular with parameters $(16, 6, 2, 2)$. They have the same degrees, the same eigenvalues and the same stable colors under 2-dimensional [Weisfeiler-Leman](/k-dimensional-weisfeiler-leman/). They are not isomorphic: the rook's graph has 8 cliques of size 4 and the Shrikhande graph has none.

**Number of classes.** The numbers of pairwise non-isomorphic graphs on 1 to 6 vertices are 1, 2, 4, 11, 34, 156. On $n$ vertices there are $2^{\binom n2}$ labeled graphs, and almost all of them have $n!$ distinct labelings (see [almost all graphs are asymmetric](/almost-all-graphs-asymmetric/)), so the number of classes is about $2^{\binom n2} / n!$.

## Known algorithms

| algorithm | scope | worst-case time |
|---|---|---|
| brute force over all bijections | all graphs | $O(n! \cdot n^2)$ |
| [Color refinement](/weisfeiler-leman/) | decides almost all graphs and all trees; incomplete | $O((n + m) \log n)$ |
| [$k$-dimensional Weisfeiler-Leman](/k-dimensional-weisfeiler-leman/) | bounded treewidth, planar and other classes for fixed $k$; incomplete in general | $O(n^{k+1} \log n)$ |
| [AHU algorithm](/ahu-algorithm/) | trees | $O(n)$ |
| [Hopcroft-Tarjan](/hopcroft-tarjan-isomorphism/) and Hopcroft-Wong | planar graphs | $O(n \log n)$, and $O(n)$ |
| [Luks's algorithm](/luks-algorithm/) (1982) | maximum degree $d$ | $n^{O(d)}$ |
| Babai and Luks (1983) | all graphs | $\exp(O(\sqrt{n \log n}))$ |
| [Babai's algorithm](/babai-quasipolynomial-algorithm/) (2015) | all graphs | $\exp((\log n)^{O(1)})$ |
| [nauty](/nauty/), Traces, [bliss](/bliss/), saucy | all graphs, by [individualization-refinement](/individualization-refinement/) | exponential on some inputs, fast in practice |
| [VF2](/vf2-algorithm/) | all graphs, by backtracking | exponential |

## Bounds

- **Upper bound.** Quasipolynomial time, $\exp((\log n)^{O(1)})$. Babai announced it in November 2015 and posted it as arXiv:1512.03547 in December 2015. In January 2017 Harald Helfgott found an error in the analysis, which lowered the claimed bound to subexponential; within days Babai posted a fix that restored quasipolynomial time. Helfgott's exposition (with Bajpai and Dona) gives the exponent explicitly, as $\exp(O((\log n)^3))$.
- **Not likely NP-complete.** GI is in NP and in coAM; if it were NP-complete, the [polynomial hierarchy](/polynomial-hierarchy/) would collapse to its second level (Boppana, Håstad and Zachos 1987). Schöning (1988) showed that GI is in the low hierarchy, which gives the same conclusion.
- **Lower bounds.** GI is hard for DET under $\mathrm{AC}^0$ reductions (Torán 2004). No stronger lower bound is known.
- **Limits of combinatorial refinement.** For every $k$ there are pairs of non-isomorphic graphs with $O(k)$ vertices that $k$-dimensional Weisfeiler-Leman does not separate ([Cai, Fürer and Immerman](/cai-furer-immerman-construction/) 1992). So no fixed dimension of WL decides GI.
- **Limits of individualization-refinement.** Neuen and Schweitzer (2017) gave graph families on which every algorithm of the individualization-refinement type takes exponential time.

## Reductions

- **Search to decision.** Find an isomorphism with $O(n^2)$ calls to a decision oracle: attach a distinct gadget to vertex $1$ of $G$ and to a candidate $w$ in $H$, keep a candidate that stays isomorphic, and go on to the next vertex.
- **Counting to decision.** Mathon (1979) reduced counting isomorphisms to the decision problem in polynomial time.
- **Automorphism to isomorphism.** $G$ has a non-trivial automorphism exactly when, for some pair $u \ne v$, the graphs $G$ with $u$ marked and $G$ with $v$ marked are isomorphic.
- **From other structures.** Isomorphism of directed graphs, hypergraphs, finite automata, and many other combinatorial structures reduces to GI and back; such problems are [GI-complete](/gi-completeness/). Group isomorphism with multiplication tables reduces to GI but is not known to be GI-hard.
- **To subgraph isomorphism.** GI is the special case of [subgraph isomorphism](/subgraph-isomorphism/) with $|V_H| = |V_G|$ and $|E_H| = |E_G|$.

## Applications

- Chemistry: deciding whether two structural formulas describe the same molecule, and storing molecules in databases under a canonical key.
- Generating combinatorial objects without duplicates, such as all graphs of a given size, by keeping one canonical copy per class.
- Symmetry detection in SAT, integer programming and constraint problems, by [symmetry reduction](/symmetry-reduction/) with the automorphism group of a graph built from the instance.
- Comparing circuits and netlists, and checking that two designs are the same up to renaming.
- Graph learning, where [color refinement](/weisfeiler-leman/) bounds the power of message-passing neural networks.

## References
