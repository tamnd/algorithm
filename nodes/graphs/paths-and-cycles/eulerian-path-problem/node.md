---
tag: 26RENZ
kind: problem
slug: eulerian-path-problem
name: Eulerian path problem
aliases:
- Euler tour problem
- Eulerian circuit problem
area: graphs/paths-and-cycles
level: intro
summary: Find an Eulerian path or circuit in a graph, or report that none exists; solvable in linear time.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m)}
prereqs: [eulerian-path, eulerian-circuit, eulers-theorem-eulerian-graphs]
see_also: [hierholzer-algorithm, fleury-algorithm, eulerian-graph, chinese-postman-problem, de-bruijn-sequence, de-bruijn-assembly, hamiltonian-path-problem, matrix-tree-theorem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 20, Problem 20-3, Euler tour (characterization and an O(E) algorithm for directed graphs)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition, Springer, 2020
    locator: Section 18.7, Eulerian Cycle/Chinese Postman
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 3, Connected graphs, Section 3.3, Euler tours
  - paper: "Carl Hierholzer, Über die Möglichkeit, einen Linienzug ohne Wiederholung und ohne Unterbrechung zu umfahren, Mathematische Annalen 6, 30 to 32 (1873)"
    locator: the whole paper (the splicing construction)
  - paper: "Graham R. Brightwell and Peter Winkler, Counting Eulerian circuits is #P-complete, Proceedings of the Seventh Workshop on Algorithm Engineering and Experiments and the Second Workshop on Analytic Algorithmics and Combinatorics (ALENEX/ANALCO), SIAM, 259 to 262 (2005)"
    locator: the whole paper (#P-completeness of counting Eulerian circuits in undirected graphs)
  - book: "Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press, 1999"
    locator: Section 5.6, the matrix-tree theorem for directed graphs and the BEST theorem on Eulerian tours
  - paper: "Mikhail J. Atallah and Uzi Vishkin, Finding Euler tours in parallel, Journal of Computer and System Sciences 29(3), 330 to 337 (1984)"
    locator: the whole paper
---

The Eulerian path problem asks for a [trail](/trail/) that uses every edge of a given [graph](/graph/) exactly once, an [Eulerian path](/eulerian-path/), or for an [Eulerian circuit](/eulerian-circuit/) when the trail must be closed, and it asks for the answer "none" when no such trail exists. [Euler's theorem](/eulers-theorem-eulerian-graphs/) reduces the decision to a degree count and one connectivity test, and [Hierholzer's algorithm](/hierholzer-algorithm/) builds the trail, so the whole problem takes $\Theta(n + m)$ time. It is the easy cousin of the NP-complete [Hamiltonian path problem](/hamiltonian-path-problem/), which asks the same about vertices. Counting the solutions is polynomial for directed graphs and #P-complete for undirected ones.

## In plain words

You get a drawing made of dots and lines, or a map of streets. You must trace every line exactly once, in one stroke, without lifting the pen. Either give the order of the lines, or say that it cannot be done.

You can tell at once whether it is possible: count the lines at each dot. If the drawing is in one piece and at most two dots have an odd count, it is possible, and the stroke must start and end at those two odd dots. If no dot is odd, the stroke can start anywhere and comes back home. Finding the actual stroke is also fast: walk until you are stuck, then add the detours that you missed.

## Definition

**Input.** A finite graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, given by adjacency lists or incidence lists. $G$ is directed or undirected. It may be a [multigraph](/multigraph/), with parallel edges and [self-loops](/self-loop/), and it may have isolated vertices. Optionally: a flag that asks for a closed trail, and a start vertex $s$.

**Output.** A sequence of edges $e_1, \ldots, e_m$, together with vertices $v_0, \ldots, v_m$, such that each $e_i$ joins $v_{i-1}$ to $v_i$ (in the directed case, from $v_{i-1}$ to $v_i$), each edge of $E$ occurs exactly once, and $v_m = v_0$ if a closed trail is asked for and $v_0 = s$ if a start is given. If no such sequence exists, the output is "none".

**When the answer is "none".** By [Euler's theorem](/eulers-theorem-eulerian-graphs/), with $\mathrm{odd}(G)$ the set of vertices of odd degree (self-loops add 2) in the undirected case:

| case | a trail exists if and only if the edges are in one component and |
|---|---|
| undirected, closed | $\mathrm{odd}(G) = \emptyset$ |
| undirected, open or closed | $\lvert \mathrm{odd}(G) \rvert \in \{0, 2\}$ |
| undirected, start $s$ | $\mathrm{odd}(G) = \emptyset$, or $\mathrm{odd}(G) = \{s, t\}$ for some $t$ |
| directed, closed | $d^+(v) = d^-(v)$ for each $v$ |
| directed, open or closed | all balanced, or one vertex with $d^+ - d^- = 1$, one with $d^- - d^+ = 1$, the rest balanced |

"The edges are in one component" means that one component of the graph (of the underlying undirected graph in the directed case) contains every edge. Isolated vertices do not matter. In the undirected case with $\mathrm{odd}(G) = \emptyset$ and a start $s$, the vertex $s$ must also have an edge, unless $m = 0$.

## Variants

- **Decision.** Only say whether an Eulerian path or circuit exists. This is the degree test plus one [connected components](/connected-components/) search.
- **Fixed start or fixed ends.** Ask for a trail from $s$, or from $s$ to $t$. The table above covers it.
- **Lexicographically least trail.** In a directed graph, among all Eulerian paths, output the one whose vertex sequence is least in lexicographic order. Hierholzer's algorithm with sorted adjacency lists, which always follows the least unused edge and outputs the vertices in reverse order of finishing, gives it. This is a common contest task ("reconstruct the itinerary").
- **Counting, directed.** The BEST theorem (de Bruijn, van Aardenne-Ehrenfest, Smith and Tutte) counts the Eulerian circuits of a connected balanced directed graph, up to rotation:
  $$\mathrm{ec}(G) = t_w(G) \prod_{v \in V} \bigl(d^+(v) - 1\bigr)!,$$
  where $t_w(G)$ is the number of spanning arborescences oriented toward any fixed vertex $w$ (the value does not depend on $w$). The [matrix-tree theorem](/matrix-tree-theorem/) gives $t_w(G)$ as a determinant, so the count takes polynomial time.
- **Counting, undirected.** Counting the Eulerian circuits of an undirected graph is #P-complete (Brightwell and Winkler, 2005).
- **Mixed graphs.** Some edges are directed and some are not. An Eulerian circuit exists if and only if the undirected edges can be oriented so that the result is balanced and the edges are in one component. The orientation is a flow problem: each undirected edge sends one unit to the end that becomes its tail, and each vertex $v$ must receive exactly $\frac{1}{2}\bigl(d^-_{\mathrm{dir}}(v) - d^+_{\mathrm{dir}}(v) + d_{\mathrm{undir}}(v)\bigr)$ units (if this is not a non-negative integer, the answer is no), where the subscripts refer to the directed and undirected edges at $v$. So the mixed case is solved by one [maximum flow](/max-flow-problem/) computation.
- **Covering, not partitioning.** If the edges may be used more than once and each use has a cost, the problem becomes the [Chinese postman problem](/chinese-postman-problem/).

## Examples

| input | answer |
|---|---|
| house of Nicholas: square $0, 1, 2, 3$ with both diagonals, roof vertex 4 joined to 2 and 3 | open trail $0, 1, 2, 0, 3, 2, 4, 3, 1$; 44 trails start at 0 |
| $K_5$ | circuit $0, 1, 2, 3, 4, 0, 2, 4, 1, 3, 0$ |
| $K_4$ | none: four odd vertices |
| Königsberg: degrees 5, 3, 3, 3 | none |
| two disjoint triangles | none: edges in two components |
| a triangle and an isolated vertex | circuit $0, 1, 2, 0$ |
| one vertex with a self-loop | circuit of length 1 |
| directed: $0 \to 1, 1 \to 2, 2 \to 0, 0 \to 3$ | open trail $0, 1, 2, 0, 3$, the only one |
| directed: $0 \to 1, 1 \to 2, 0 \to 2$ | none: vertex 0 has surplus $+2$ |
| no edges, $n \ge 1$ | the trail of length 0 at any vertex |

**Counting examples.** In the complete directed graph on 3 vertices (all 6 ordered pairs), $t_w = 3$ and each out-degree is 2, so $\mathrm{ec} = 3 \cdot 1 \cdot 1 \cdot 1 = 3$. On 4 vertices (12 edges), $t_w = 16$ and each out-degree is 3, so $\mathrm{ec} = 16 \cdot 2^4 = 256$. The binary de Bruijn graph of order 2, on the vertices $00, 01, 10, 11$ with an edge $x \to y$ when the last symbol of $x$ is the first of $y$, has self-loops at $00$ and $11$; it has $t_w = 2$, out-degree 2 everywhere, and $\mathrm{ec} = 2$. Its two Eulerian circuits are the two binary [de Bruijn sequences](/de-bruijn-sequence/) of order 3, $00010111$ and $00011101$, up to rotation.

## Known algorithms

| algorithm | time | remark |
|---|---|---|
| [Hierholzer's algorithm](/hierholzer-algorithm/) (1873) | $\Theta(n + m)$ | walk until stuck, splice closed sub-trails; iterative form with a stack |
| [Fleury's algorithm](/fleury-algorithm/) (1883) | $O(m(n + m))$ with a search for each bridge test | never cross a [bridge](/bridge/) of the remaining graph unless forced; simple to state, slow |
| Degree count plus [connected components](/connected-components/) | $\Theta(n + m)$ | the decision version only |
| BEST theorem with a determinant | $O(n^3)$ arithmetic operations | counting, directed graphs |

In Hierholzer's algorithm each vertex keeps a pointer to its next unused edge. For an undirected graph, the two list entries of an edge share one "used" flag, so that the walk does not take the same edge back. With this, each list entry is looked at a constant number of times.

## Bounds

**Upper bound.** $O(n + m)$ time in the [word RAM](/word-ram/) model with adjacency or incidence lists, by Hierholzer's algorithm after the test of Euler's theorem.

**Lower bound.** When the answer is a trail, the output has $m$ edges, so each algorithm takes $\Omega(m)$ time on these inputs. Reading the $n$ vertex lists costs $\Omega(n)$ to find the start vertex in the worst case, for example when the only edge is a self-loop at an unknown vertex. So the bound $\Theta(n + m)$ is tight for the search version.

**Space.** $\Theta(n + m)$ words, for the used flags, the pointers and the output.

**Parallel.** Atallah and Vishkin showed in 1984 that an Eulerian circuit can be found in $O(\log n)$ time on a CRCW PRAM with a linear number of processors, so the problem is in NC.

## Reductions

- **Path to circuit.** If $\mathrm{odd}(G) = \{s, t\}$, add an edge $f = \{s, t\}$ (or $t \to s$ in the directed case), find an Eulerian circuit, rotate it so that $f$ is last, and delete $f$. The cost is $O(n + m)$.
- **To a Hamiltonian cycle in the line graph.** A directed graph $G$ has an Eulerian circuit if and only if its directed [line graph](/line-graph/) $L(G)$, with a vertex for each edge and an arc $e \to f$ when the head of $e$ is the tail of $f$, has a Hamiltonian cycle. For undirected graphs only one direction holds: an Eulerian circuit of $G$ gives a Hamiltonian cycle of $L(G)$, but $L(K_{1,3}) = K_3$ is Hamiltonian while $K_{1,3}$ has no Eulerian path. This is why Hamiltonian problems on line graphs of de Bruijn graphs are easy.
- **Mixed graphs to flows.** As in the Variants section, at the cost of one maximum flow.
- **From the Chinese postman problem.** The postman problem on an undirected graph reduces to minimum-weight perfect matching plus one Eulerian circuit; see the [Edmonds-Johnson algorithm](/edmonds-johnson-algorithm/).

## Applications

- **Drawing puzzles and plotters.** Draw a figure in as few strokes as possible: a connected figure with $2k > 0$ odd points needs exactly $k$ strokes.
- **De Bruijn sequences.** An Eulerian circuit of the de Bruijn graph spells a shortest cyclic string that contains every word of a given length, used in position-encoding and in testing locks with a keypad.
- **Genome assembly.** In the [de Bruijn assembly](/de-bruijn-assembly/) method, reads are cut into $k$-mers, and an Eulerian path in the de Bruijn graph of the $k$-mers spells a candidate genome.
- **Routing.** Street sweeping, snow ploughing, mail delivery and the inspection of pipes or power lines need routes along edges. When the network is Eulerian, an Eulerian circuit is an optimal route; otherwise the [Chinese postman problem](/chinese-postman-problem/) adds repeats.
- **Tree algorithms.** The [Euler tour technique](/euler-tour-technique/) lists the edges of a tree, each doubled, as an Eulerian circuit, and turns subtree questions into range questions.

## References
