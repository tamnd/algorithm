---
tag: M8JFJA
kind: algorithm
slug: vf2-algorithm
name: VF2 algorithm
aliases:
- VF2
- VF2 graph matching
area: graphs/graph-isomorphism
level: core
summary: Depth-first search over partial mappings with cheap feasibility rules for graph isomorphism and induced subgraph isomorphism, using memory linear in the graph size.
solves: [graph-isomorphism-problem, subgraph-isomorphism]
model: word-ram
complexity:
  vars: {n: the number of vertices of the larger graph}
  time: {worst: O(n! n^2), best: O(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, directed: false}
prereqs: [subgraph-isomorphism, graph-isomorphism-problem, generic-backtracking-algorithm, adjacency-list]
see_also: [ullmann-algorithm, weisfeiler-leman, nauty, maximum-common-subgraph, graph-edit-distance, induced-subgraph]
sources:
  - paper: doi:10.1109/TPAMI.2004.75
    title: Luigi P. Cordella, Pasquale Foggia, Carlo Sansone and Mario Vento, A (sub)graph isomorphism algorithm for matching large graphs, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(10), 1367 to 1372 (2004)
    locator: Section 2 (the state space, the candidate pairs and the feasibility rules) and Section 3 (complexity)
  - paper: doi:10.1145/321921.321925
    title: J. R. Ullmann, An algorithm for subgraph isomorphism, Journal of the ACM 23(1), 31 to 42 (1976)
    locator: the whole paper (the backtracking baseline that VF2 is compared with)
  - paper: "Vincenzo Carletti, Pasquale Foggia, Alessia Saggese and Mario Vento, Challenging the time complexity of exact subgraph isomorphism for huge and dense graphs with VF3, IEEE Transactions on Pattern Analysis and Machine Intelligence 40(4), 804 to 818 (2018)"
    locator: the whole paper (VF3, the ordering of pattern vertices and node classes)
---

VF2 is a backtracking algorithm that decides whether two graphs are isomorphic, or whether a pattern graph is isomorphic to an induced subgraph of a host graph, and it can list all such mappings. It grows a partial mapping one vertex pair at a time and tests each new pair with cheap rules: the edges to vertices already mapped must agree, and the numbers of neighbors just outside the mapping must be compatible. It stores only the current mapping and a few arrays, so its memory is linear in the size of the graphs. It is exponential in the worst case, but fast on many graphs from practice, and it is the matcher behind several libraries.

## In plain words

You try to place the points of a small network on the points of a large one, one point at a time. Each time you place a point, you check that its links to the points already placed have copies in the large network. You also look one step ahead: count how many neighbors the point has just outside the placed part, and check that its partner in the large network has enough of them. If any check fails, you take back the last placement and try the next partner. If every point gets placed, you found a match. You always grow the placed part by a point next to it, so failures show up early.

## The problem

The input is a pattern graph $G_1 = (V_1, E_1)$ with $n_1$ vertices and a host graph $G_2 = (V_2, E_2)$ with $n_2 \ge n_1$ vertices. Here both are simple and undirected, and they may carry vertex labels that a mapping must keep; the original algorithm also handles directed graphs and edge labels with the same rules applied to in-neighbors and out-neighbors. The output is every injective map $m : V_1 \to V_2$ of one of three kinds:

- **iso**: $n_1 = n_2$, and $\{u, w\} \in E_1 \iff \{m(u), m(w)\} \in E_2$ ([graph isomorphism](/graph-isomorphism-problem/));
- **induced**: the same condition with $n_1 \le n_2$ ([induced subgraph isomorphism](/subgraph-isomorphism/), called graph-subgraph isomorphism in the VF2 paper);
- **mono**: only $\{u, w\} \in E_1 \implies \{m(u), m(w)\} \in E_2$ (monomorphism, non-induced subgraph isomorphism).

## The algorithm

A state is a partial injective map $M$. For $i = 1, 2$, the terminal set $T_i$ holds the unmapped vertices of $G_i$ that have a mapped neighbor, and the new set $\tilde N_i$ holds the unmapped vertices with no mapped neighbor. $N_i(x)$ is the neighbor set of $x$ in $G_i$.

```pseudo id=main
VF2(G1, G2, mode)
L1  M ← ∅; start the search at state M
L2  if |M| = n1 then output M and backtrack
L3  P ← candidate pairs: if T1 ≠ ∅, the pairs (u, v) with u = min T1 and v ∈ T2;
        if T1 = T2 = ∅, the pairs (u, v) with u = the smallest unmapped vertex and v unmapped in G2
L4  for each (u, v) in P do
L5      if FEASIBLE(M, u, v) then
L6          M ← M ∪ {(u, v)}; update T1, T2
L7          search from the new state (go to L2)
L8          M ← M \ {(u, v)}; restore T1, T2

FEASIBLE(M, u, v)
L9  labels of u and v agree, and deg u = deg v (iso) or deg u ≤ deg v (otherwise)
L10 for each mapped neighbor u' of u: M(u') ∈ N2(v); unless mode = mono,
        for each mapped neighbor v' of v: M⁻¹(v') ∈ N1(u)
L11 iso: |N1(u) ∩ T1| = |N2(v) ∩ T2| and |N1(u) ∩ Ñ1| = |N2(v) ∩ Ñ2|
L12 induced: both with ≤ instead of =;  mono: |N1(u) ∩ T1| ≤ |N2(v) ∩ T2| and |N1(u) \ M| ≤ |N2(v) \ M|
```

Fixing $u$ in L3 and letting only $v$ vary means that each mapping is produced once, not once per order of its pairs. In iso mode, if $T_1 = \emptyset$ but $T_2 \ne \emptyset$, the state has no candidates. The implementation runs L2 to L8 with an explicit stack instead of recursion.

## Example

Let $G_1$ be a triangle $0, 1, 2$ with a pendant vertex 3 at 2 (edges $01, 12, 20, 23$), and $G_2$ the same shape with other names (edges $31, 10, 03, 02$; the triangle is $0, 1, 3$ and the pendant is 2 at 0). In iso mode the search tries:

| mapped so far | pair tried | result | reason |
|---|---|---|---|
| none | $(0, 0)$ | rejected | L9: $\deg 0 = 2$ in $G_1$, $\deg 0 = 3$ in $G_2$ |
| none | $(0, 1)$ | accepted | degrees 2 and 2; no mapped neighbors |
| $0 \to 1$ | $(1, 0)$ | rejected | L9: degrees 2 and 3 |
| $0 \to 1$ | $(1, 3)$ | accepted | edge $01$ goes to edge $13$ |
| $0 \to 1, 1 \to 3$ | $(2, 0)$ | accepted | edges $20, 21$ go to $01, 03$ |
| $0 \to 1, 1 \to 3, 2 \to 0$ | $(3, 2)$ | accepted | output $m = (1, 3, 0, 2)$ |
| none | $(0, 2)$ | rejected | L9: degrees 2 and 1 |
| none | $(0, 3)$ | accepted | then $(1, 0)$ rejected, $(1, 1)$, $(2, 0)$, $(3, 2)$ accepted |

The two outputs $(1, 3, 0, 2)$ and $(3, 1, 0, 2)$ differ by the automorphism of $G_1$ that swaps 0 and 1, so the graphs are isomorphic and $|\mathrm{Aut}(G_1)| = 2$. Other counts from the implementation: the path on 3 vertices has 10 monomorphisms and 10 induced embeddings into $C_5$; $C_4$ has 24 monomorphisms into $K_4$ but no induced embedding; the $4 \times 4$ rook's graph has 1152 automorphisms and the Shrikhande graph 192, and VF2 reports that the two are not isomorphic.

## Correctness

The [full proof](proofs/correctness.md) shows three facts.

- **Soundness.** Every output is a mapping of the requested kind. Rule L10 checks every pair of mapped vertices when the later of the two is added, in both directions for iso and induced mode, so the output keeps edges, and also non-edges unless the mode is mono. Injectivity holds because candidates are unmapped on both sides.
- **The look-ahead rules prune only dead states.** If a state extends to a full mapping $m$, then every neighbor of $u$ in $T_1$ maps into $T_2$ and every neighbor in $\tilde N_1$ maps into $\tilde N_2$ (iso and induced), so the counts in L11 and L12 hold. For mono, a neighbor in $T_1$ still maps into $T_2$, and all unmapped neighbors map to unmapped neighbors of $v$.
- **Completeness.** Every valid mapping $m$ is output exactly once. Follow the pattern vertices in the order in which L3 picks them: the pair $(u, m(u))$ is always among the candidates, since $m(u) \in T_2$ exactly when $u \in T_1$ in iso and induced mode and $m(u) \in T_2$ whenever $u \in T_1$ in mono mode, and it passes the rules by the previous point. Fixing $u$ makes the path to $m$ unique.

## Complexity

| case | time | space |
|---|---|---|
| best: every first candidate is right | $O(n^2)$ | $\Theta(n)$ |
| worst: the search tree has all partial injections | $O(n! \cdot n^2)$ for iso; $O\!\left(\frac{n_2!}{(n_2 - n_1)!} \, n^2\right)$ otherwise | $\Theta(n)$ |

Each state costs $O(n)$ to find $T_1$, $T_2$ and the candidates, and $O(\deg u + \deg v)$ per feasibility test. The stack has at most $n_1$ frames; the arrays `core` and the terminal counters take $O(n_1 + n_2)$ words besides the graphs, which is the linear memory that distinguishes VF2 from its predecessor VF and from [Ullmann's algorithm](/ullmann-algorithm/), whose candidate matrix takes $\Theta(n_1 n_2)$ space per level. The candidate lists on the stack add $O(n_1 n_2)$ in this implementation; generating candidates lazily removes this. The worst case is reached on regular graphs with large automorphism groups and on hard non-isomorphic pairs; VF2 has no refinement step such as [color refinement](/weisfeiler-leman/), so it cannot rule out a whole regular graph at once.

## Properties

- **Exact and complete.** It finds every mapping, not an approximation.
- **Deterministic.** The order of candidates depends on vertex numbers, so the running time changes when the input is relabeled.
- **Low memory.** Linear extra space, which suits large sparse graphs.
- **Flexible.** Vertex and edge labels and arbitrary compatibility predicates fit into L9 and L10, which is why graph databases and chemistry tools use it.
- **Not canonical.** It compares two given graphs; it gives no canonical form and does not exploit automorphisms.

## Variants and improvements

- **VF2++** (Jüttner and Madarasi 2018) orders the pattern vertices by a BFS from a rare, high-degree vertex and adds label-based cutting rules; it is much faster than VF2 on many inputs.
- **VF3** (Carletti and others 2018) adds a precomputed ordering of pattern vertices by probability, classes of vertices by label, and is built for large dense hosts; VF3-Light drops some rules for speed.
- **Monomorphism.** The look-ahead must use the weaker rule in L12, since non-edges of the pattern may map to edges of the host.
- **Directed graphs.** Keep separate terminal sets for successors and predecessors and apply L10 to L12 to each; this is the form in the original paper.
- **Refinement first.** Running [color refinement](/weisfeiler-leman/) on both graphs and allowing only pairs of the same color shrinks the candidates a lot; this is the main idea of [nauty](/nauty/)-type tools and of newer subgraph solvers.

## When to use it

Use VF2 for subgraph and induced subgraph matching with labels on graphs of moderate size, for finding all matches of a small pattern, and for isomorphism tests between graphs with many distinct labels. For isomorphism of unlabeled graphs, canonical labeling with [nauty](/nauty/) or [bliss](/bliss/) is much more robust, since VF2 can take exponential time on symmetric or regular inputs where those tools finish fast. For hard subgraph instances, constraint solvers with stronger propagation, such as the Glasgow Subgraph Solver, often do better.

## Pitfalls

- **Wrong look-ahead for monomorphism.** Using the induced rules in mono mode prunes valid mappings, because a pattern vertex in $\tilde N_1$ may map to a host vertex in $T_2$.
- **Candidates not fixed on one side.** Trying all pairs $(u, v)$ with both sides free outputs each mapping many times, once per order of the pairs.
- **Disconnected patterns.** When $T_1$ is empty in the middle of the search, the next component starts with all unmapped host vertices as candidates; the iso rule "no candidates when only $T_2$ is non-empty" must not be used for induced or mono mode.
- **Deep recursion.** A recursive implementation has depth $n_1$, which exceeds the default recursion limit of some languages on large patterns.
- **Expecting polynomial time.** Regular graphs, strongly regular graphs and other symmetric inputs make VF2 explore huge trees.

## Implementations

## History

Cordella, Foggia, Sansone and Vento introduced the VF algorithm in 1999 and VF2 at a workshop in 2001; the journal paper appeared in IEEE TPAMI in 2004. VF2 replaced the candidate matrix of [Ullmann's algorithm](/ullmann-algorithm/) (1976) with terminal sets and look-ahead counts, which cut memory to linear size. It became the default matcher of the VFLib library and of graph libraries such as NetworkX and the Boost Graph Library. VF2++ (2018) and VF3 (2017, journal 2018) improved the ordering of the search.

## References
