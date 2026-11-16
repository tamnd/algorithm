---
tag: CTGJNM
kind: theorem
slug: hamiltonian-cycle-np-completeness
name: NP-completeness of the Hamiltonian cycle problem
aliases:
- Hamiltonian-cycle NP-completeness
area: complexity/reductions-catalogue
level: core
summary: Deciding whether a graph has a cycle through every vertex exactly once is NP-complete, by a reduction from vertex cover with a 12-vertex gadget per edge.
prereqs: [hamiltonian-cycle-problem, vertex-cover, np-complete, polynomial-time-reduction]
see_also: [hamiltonian-path-problem, traveling-salesman-decision, gadget-reduction, held-karp-algorithm, karp-21-np-complete, karps-21-np-complete-problems, planar-graph, general-tsp-inapproximability]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 34.5.3 (the Hamiltonian-cycle problem, reduction from vertex cover with the edge widget)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 3.1.4 (HAMILTONIAN CIRCUIT, from VERTEX COVER) and Appendix A1.3, problems GT37 and GT38
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103
    locator: Section 4, problems 9 and 10 (DIRECTED and UNDIRECTED HAMILTON CIRCUIT), the reductions from NODE COVER and from the directed problem, and the credits to Lawler and Tarjan
  - paper: doi:10.1137/0205049
    title: Michael R. Garey, David S. Johnson and Robert E. Tarjan, The planar Hamiltonian circuit problem is NP-complete, SIAM Journal on Computing 5(4), 1976
    locator: the main theorem (planar, cubic, 3-connected graphs)
---

The Hamiltonian cycle problem asks whether a graph has a cycle that passes through every vertex exactly once. This theorem says that the problem is [NP-complete](/np-complete/). Karp (1972) proved it for directed graphs by a reduction from node cover, which he credits to Lawler, and then for undirected graphs by a reduction credited to Tarjan. The proof below is the textbook one of Cormen, Leiserson, Rivest and Stein, close to the proof of Garey and Johnson: a reduction from [vertex cover](/vertex-cover/) that replaces each edge by a 12-vertex gadget. The theorem is the source of NP-hardness for the [traveling salesman problem](/traveling-salesman-decision/) and for many routing problems.

## Statement

A *Hamiltonian cycle* of an undirected graph $G = (V, E)$ is a cycle that contains every vertex of $G$ exactly once. The decision problem HAM-CYCLE has as instance a graph $G$, and asks whether $G$ has a Hamiltonian cycle; see [Hamiltonian cycle problem](/hamiltonian-cycle-problem/).

**Theorem.** HAM-CYCLE is NP-complete under Karp (polynomial-time many-one) reductions. The same holds for directed graphs, for Hamiltonian paths, and (Garey, Johnson and Tarjan 1976) for planar cubic 3-connected graphs.

## In plain words

A traveler wants a round trip that visits every town exactly once, using only the given roads. Checking a proposed trip is easy. Finding one is hard, because the road map can be built to act like a different hard puzzle.

The puzzle used here is: choose $k$ towns so that every road has a chosen town at one end. For each road, the proof builds a small maze of 12 points. A round trip can cross the maze in only three ways, which say "this end is chosen", "that end is chosen" or "both ends are chosen". The trip has $k$ start points, one for each chosen town. So a round trip exists exactly when $k$ towns can watch every road.

## Proof

**Membership in NP.** The certificate is a list of the vertices in the order of the cycle. The verifier checks that every vertex appears exactly once and that consecutive vertices, and the last and the first, are adjacent. This takes polynomial time on the [multitape Turing machine](/multitape-turing-machine/).

**Hardness: a Karp reduction from vertex cover.** Let $(G, k)$ be an instance of VERTEX COVER: is there a set of at most $k$ vertices that touches every edge? Remove the isolated vertices of $G$, since they never help to cover an edge, and let $V'$ be the remaining vertices. If $E$ is empty, output a fixed yes-instance, such as a triangle. Otherwise replace $k$ by $\min(k, \lvert V' \rvert)$; if $k = 0$, output a fixed no-instance, such as a single edge. A set of at most $k$ vertices covers $E$ if and only if a set of exactly $k$ vertices of $V'$ does, since we can add vertices to a cover.

*Map.* Build the graph $H$ as follows.

1. **Edge gadget.** For each edge $\{u, v\}$ of $G$, add 12 vertices $[u, v, i]$ and $[v, u, i]$ for $i = 1, \ldots, 6$. Add the two paths $[u, v, 1], \ldots, [u, v, 6]$ and $[v, u, 1], \ldots, [v, u, 6]$, and the four cross edges $[u, v, 3]$-$[v, u, 1]$, $[v, u, 3]$-$[u, v, 1]$, $[u, v, 6]$-$[v, u, 4]$ and $[v, u, 6]$-$[u, v, 4]$. Only the four corner vertices $[u, v, 1]$, $[u, v, 6]$, $[v, u, 1]$ and $[v, u, 6]$ get edges outside the gadget.
2. **Vertex chain.** For each vertex $u \in V'$, list its neighbors in any fixed order $u^{(1)}, \ldots, u^{(d)}$, where $d$ is the degree of $u$. Add the edges $[u, u^{(i)}, 6]$-$[u, u^{(i+1)}, 1]$ for $i = 1, \ldots, d - 1$. The *chain* of $u$ is then a path from $[u, u^{(1)}, 1]$ to $[u, u^{(d)}, 6]$ through the $u$-halves of all gadgets at $u$.
3. **Selectors.** Add $k$ vertices $s_1, \ldots, s_k$, and join each $s_j$ to both ends $[u, u^{(1)}, 1]$ and $[u, u^{(d)}, 6]$ of every chain.

*Cost.* $H$ has $12 \lvert E \rvert + k$ vertices and $14 \lvert E \rvert + (2 \lvert E \rvert - \lvert V' \rvert) + 2k \lvert V' \rvert$ edges, so it is built in polynomial time.

**Gadget lemma.** In every Hamiltonian cycle of $H$, the gadget of $\{u, v\}$ is traversed in one of three ways: (a) enter at $[u, v, 1]$, visit all 12 vertices and leave at $[u, v, 6]$; (b) the same with $u$ and $v$ exchanged; (c) traverse the path $[u, v, 1], \ldots, [u, v, 6]$ and, at another time, the path $[v, u, 1], \ldots, [v, u, 6]$.

*Proof of the lemma.* A Hamiltonian cycle uses exactly two edges at each vertex. The vertices $[u, v, 2]$ and $[u, v, 5]$ have degree 2 in $H$, so the cycle uses the edges $[u, v, 1]$-$[u, v, 2]$-$[u, v, 3]$ and $[u, v, 4]$-$[u, v, 5]$-$[u, v, 6]$, and the same for $[v, u, \cdot]$. The vertex $[u, v, 3]$ then has one more edge, to $[u, v, 4]$ or to $[v, u, 1]$.

- Suppose the cycle uses $[u, v, 3]$-$[v, u, 1]$. Then $[v, u, 1]$ has its two edges, so it has no edge outside. If the cycle also used $[v, u, 3]$-$[u, v, 1]$, it would contain the 6-cycle $[u, v, 1], [u, v, 2], [u, v, 3], [v, u, 1], [v, u, 2], [v, u, 3]$, which is shorter than $H$. So $[v, u, 3]$ goes to $[v, u, 4]$, and $[u, v, 1]$ takes its second edge outside. Now $[u, v, 3]$ is full, so $[u, v, 4]$ must use $[v, u, 6]$, which fills $[v, u, 6]$. Also $[v, u, 4]$ is full with $[v, u, 3]$ and $[v, u, 5]$, so $[u, v, 6]$ takes its second edge outside. This is way (a).
- If the cycle uses $[v, u, 3]$-$[u, v, 1]$, the same argument gives way (b).
- Otherwise $[u, v, 3]$-$[u, v, 4]$ and $[v, u, 3]$-$[v, u, 4]$ are in the cycle. Then $[u, v, 4]$ and $[v, u, 4]$ are full, so neither lower cross edge is used, and each half is a path from its vertex 1 to its vertex 6. This is way (c).

*If $G$ has a vertex cover of size $k$, then $H$ has a Hamiltonian cycle.* Let $\{c_1, \ldots, c_k\} \subseteq V'$ be a cover. For $j = 1, \ldots, k$, go from $s_j$ to the start of the chain of $c_j$ and follow the chain. At the gadget of an edge $\{c_j, v\}$, use way (a) with $c_j$ in the role of $u$ if $v$ is not in the cover, and traverse only the $c_j$-half (way (c)) if $v$ is in the cover. At the end of the chain, go to $s_{j+1}$, or to $s_1$ when $j = k$. Every gadget is visited completely: by its one cover end in way (a), or by both cover ends in way (c). So this is a Hamiltonian cycle.

*If $H$ has a Hamiltonian cycle, then $G$ has a vertex cover of size at most $k$.* Take any Hamiltonian cycle. By the lemma, the cycle enters and leaves each gadget only at the corners $[u, v, 1]$ and $[u, v, 6]$ of a half that it traverses in order. Outside its gadget, $[u, v, 6]$ is adjacent only to the next vertex of the chain of $u$ or to selectors, and $[u, v, 1]$ only to the previous vertex of the chain of $u$ or to selectors. So the part of the cycle between two consecutive selectors follows the chain of one vertex $u$ from one end to the other. The $k$ selectors cut the cycle into $k$ such parts, for vertices $c_1, \ldots, c_k$. Every gadget is visited, and the gadget of $\{u, v\}$ is visited only by the part for $u$ or the part for $v$. So $\{c_1, \ldots, c_k\}$ covers every edge.

Since VERTEX COVER is NP-complete ([clique problem](/clique-problem/) and Karp 1972), HAM-CYCLE is NP-complete. $\blacksquare$

**Worked example.** A script built $H$ and listed its Hamiltonian cycles.

- For the path $u$-$v$-$w$ with $k = 1$, $H$ has 25 vertices and 35 edges, and $\{v\}$ is a cover. $H$ has exactly one Hamiltonian cycle, and it is the one the forward direction builds: $s_1$, then $[v, u, 1], [v, u, 2], [v, u, 3]$, then $[u, v, 1], \ldots, [u, v, 6]$, then $[v, u, 4], [v, u, 5], [v, u, 6]$, then the same pattern through the gadget of $\{v, w\}$, and back to $s_1$. Both gadgets are crossed in way (a) for $v$, and reading the cycle back gives the cover $\{v\}$.
- For the triangle on $u, v, w$ with $k = 1$, $H$ has 37 vertices and 51 edges and no Hamiltonian cycle, as no single vertex covers a triangle. With $k = 2$ it has 38 vertices, 57 edges and 12 Hamiltonian cycles.
- On 80 random graphs with 2 to 4 vertices and random $k$, $H$ had a Hamiltonian cycle exactly when $G$ had a vertex cover of size $k$ (71 yes-instances and 9 no-instances).

## Consequences

- **Variants.** For the directed version, Karp gave a reduction from node cover. For [Hamiltonian paths](/hamiltonian-path-problem/), add a new vertex $x'$ joined to the neighbors of some vertex $x$, and pendant vertices at $x$ and $x'$: the new graph has a Hamiltonian path if and only if the old one has a Hamiltonian cycle.
- **Traveling salesman.** Give the edges of $G$ length 1 and the non-edges length 2. Then $G$ has a Hamiltonian cycle if and only if there is a tour of length at most $\lvert V \rvert$, so the [traveling salesman decision problem](/traveling-salesman-decision/) is NP-complete, even with the triangle inequality. With a much larger length for non-edges, the same map shows that general TSP has no constant-factor approximation unless P = NP; see [general TSP inapproximability](/general-tsp-inapproximability/).
- **Exact algorithms.** Unless P = NP, there is no polynomial-time algorithm. The [Held-Karp algorithm](/held-karp-algorithm/) decides the problem in $O(2^n n^2)$ time by dynamic programming over subsets.

## Tightness

- **Planar and cubic graphs.** The problem stays NP-complete on planar, cubic, 3-connected graphs (Garey, Johnson and Tarjan 1976). So bounded degree and planarity do not make it easy.
- **Easy cases.** On graphs with maximum degree 2 the problem is trivial: the graph must be one cycle. A Hamiltonian cycle uses every vertex once; the similar question for edges, an Eulerian circuit, is in P, because it exists exactly when the graph is connected apart from isolated vertices and every degree is even.

## History

Karp (1972) listed DIRECTED HAMILTON CIRCUIT and UNDIRECTED HAMILTON CIRCUIT among his 21 NP-complete problems; the reductions are on [Karp's reduction tree](/karp-21-np-complete/). Garey and Johnson (1979, Section 3.1.4) made Hamiltonian circuit one of their six basic NP-complete problems, with a proof from vertex cover. The 12-vertex edge gadget in the proof above is the one in Cormen, Leiserson, Rivest and Stein. Garey, Johnson and Tarjan (1976) proved the planar cubic 3-connected case.

## References
