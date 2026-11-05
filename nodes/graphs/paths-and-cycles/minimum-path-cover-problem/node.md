---
tag: 0RHJ5H
kind: problem
slug: minimum-path-cover-problem
name: Minimum path cover problem
aliases:
- path cover of a DAG
area: graphs/paths-and-cycles
level: advanced
summary: Cover the vertices of a DAG with the fewest vertex-disjoint paths.
prereqs: [directed-acyclic-graph, simple-path, bipartite-matching]
see_also: [path-cover-by-bipartite-matching, dilworth-theorem, transitive-closure, hamiltonian-path-problem, konig-theorem, hopcroft-karp, topological-sort, critical-path]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 26, Problem 26-2, Minimum path cover (vertex-disjoint paths in a DAG, by matching or flow)
  - paper: D. R. Fulkerson, Note on Dilworth's decomposition theorem for partially ordered sets, Proceedings of the American Mathematical Society 7(4), 701 to 702 (1956)
    title: Fulkerson, Dilworth's theorem by bipartite matching
    locator: the whole note
  - paper: R. P. Dilworth, A decomposition theorem for partially ordered sets, Annals of Mathematics 51(1), 161 to 166 (1950)
    title: Dilworth, chains and antichains
    locator: the main theorem (the least number of chains equals the largest antichain)
  - paper: George B. Dantzig and D. R. Fulkerson, Minimizing the number of tankers to meet a fixed schedule, Naval Research Logistics Quarterly 1(3), 1954
    title: Dantzig and Fulkerson, minimum fleet size
    locator: the formulation of the fleet size problem as a path cover and its solution by a transportation problem
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1 (graph theory), Hamiltonian path, used for the hardness on general graphs
---

The minimum path cover problem asks for the fewest vertex-disjoint paths in a [directed acyclic graph](/directed-acyclic-graph/) such that every vertex lies on exactly one of them. On a DAG it reduces to a maximum [bipartite matching](/bipartite-matching/): the answer is $n$ minus the size of a maximum matching in the split graph, see [path cover by bipartite matching](/path-cover-by-bipartite-matching/). If the paths may share vertices, the answer is the least number of chains of the reachability order, which by [Dilworth's theorem](/dilworth-theorem/) equals the largest set of pairwise unreachable vertices. On graphs with cycles, or on undirected graphs, the problem contains the [Hamiltonian path problem](/hamiltonian-path-problem/) and is NP-hard.

## In plain words

Some jobs must happen in a given order, and some jobs can follow others directly. Each worker does a line of jobs, one after another, each allowed to follow the one before. Every job must be done by exactly one worker. What is the least number of workers?

Each time a job is placed right after another on the same worker, one worker is saved. So the question becomes: how many such "right after" pairs can you choose, if each job has at most one job right after it and at most one right before it? That is a matching question, and matching questions have fast exact answers.

## Definition

**Input.** A directed acyclic graph $G = (V, A)$ with $n$ vertices and $m$ arcs. Parallel arcs are allowed and change nothing. A DAG has no self-loop. Isolated vertices are allowed.

**Output.** A set $\mathcal{P}$ of [simple paths](/simple-path/) such that every vertex is on exactly one path of $\mathcal{P}$, with $|\mathcal{P}|$ as small as possible. A path may consist of a single vertex. The least size is the *path cover number* of $G$.

**Matching form.** A cover by $p$ disjoint paths uses $n - p$ arcs, and these arcs give each vertex at most one successor and one predecessor. Conversely, in a DAG, any such set of arcs is a union of disjoint paths. So minimizing $p$ is maximizing a set of arcs with in-degree and out-degree at most 1, which is a matching in the split bipartite graph.

## Variants

- **Vertex-disjoint paths in a DAG.** The main problem; polynomial by matching.
- **Paths that may share vertices.** Each vertex must be on at least one path. Replace $G$ by its [transitive closure](/transitive-closure/) and solve the disjoint problem: the answer is the least number of chains that cover the partial order of reachability, the *width* of the order. It equals the largest antichain, by Dilworth's theorem.
- **General directed graphs.** NP-hard: one path covers $G$ exactly when $G$ has a [Hamiltonian path](/hamiltonian-path/). If cycles may be used as well as paths, the matching method solves it in polynomial time.
- **Undirected graphs.** Also NP-hard by the same argument. On trees, a greedy pass from the leaves finds a minimum cover in linear time.
- **Edge cover by paths.** Cover all arcs instead of all vertices. On a DAG this is a minimum flow problem with a lower bound of 1 on every arc.
- **Weighted versions.** A cost per path and a cost per arc used; a minimum cost matching or flow solves it on a DAG.

## Examples

**A small DAG.** Vertices $0, \ldots, 6$ and arcs $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 3$, $3 \to 4$, $2 \to 5$, $5 \to 6$, $1 \to 5$. Vertices 4 and 6 have no outgoing arc, so each ends a different path, and at least 2 paths are needed. Two paths suffice: $0, 1, 5, 6$ and $2, 3, 4$. A maximum matching in the split graph has $7 - 2 = 5$ edges.

**Disjoint against shared.** Arcs $0 \to 2$, $1 \to 2$, $2 \to 3$, $2 \to 4$. Vertex 2 has one successor and one predecessor in a disjoint cover, so the cover is, for example, $0, 2, 3$ and the single vertices 1 and 4: 3 paths. If paths may share vertices, $0, 2, 3$ and $1, 2, 4$ cover everything with 2 paths. The largest antichain is $\{0, 1\}$ (or $\{3, 4\}$), of size 2, as Dilworth's theorem says.

**No arcs.** $n$ isolated vertices need $n$ paths of one vertex each.

**A path.** The arcs $0 \to 1 \to \cdots \to n - 1$ need one path. If the arc $0 \to 2$ is added, one path still suffices.

**With a cycle.** The directed cycle $0 \to 1 \to 2 \to 0$ is not a DAG. Its path cover number is 1, the path $0, 1, 2$, but the matching on the split graph can pick all three arcs and return the cycle, which is not a path. This is why the matching method requires a DAG.

## Known algorithms

- **Bipartite matching.** $n - \nu(H)$, where $\nu(H)$ is the maximum matching of the split graph. With Kuhn's augmenting paths $O(n(n + m))$, with Hopcroft-Karp $O(m\sqrt{n})$. See [path cover by bipartite matching](/path-cover-by-bipartite-matching/).
- **Maximum flow.** The same graph with a source and a sink and unit capacities.
- **Shared vertices.** Transitive closure in $O(nm)$ time, then matching on the closure, which can have $\Theta(n^2)$ arcs. Faster methods compute the width of a DAG directly with flows on $G$ and lower bounds on the vertices, without the closure.
- **Trees.** A greedy pass from the leaves, $O(n)$.
- **General graphs.** Exact methods for Hamiltonian path apply, such as the subset dynamic program in $O(2^n n^2)$ time.

## Bounds

- **Upper bound on DAGs.** $O(m\sqrt{n})$ via Hopcroft-Karp, and faster with recent maximum flow algorithms.
- **Lower bounds on the answer.** Every vertex with no incoming arc starts a path, and every vertex with no outgoing arc ends one, so the answer is at least the number of sources and at least the number of sinks. Two vertices with no path between them in either direction must be on different paths, so the answer is at least the largest antichain. For shared paths this last bound is exact (Dilworth); for disjoint paths it can be smaller than the answer, as the example with vertex 2 shows.
- **Certificate.** By [König's theorem](/konig-theorem/), a maximum matching of the split graph comes with a vertex cover of the same size, which proves that no larger matching, and so no smaller cover, exists.
- **NP-hardness.** On general directed or undirected graphs, deciding whether the path cover number is 1 is the Hamiltonian path problem, which is NP-complete (Garey and Johnson, Appendix A1).

## Reductions

- **To bipartite matching.** The split graph, as above.
- **From Dilworth's theorem.** The chain cover of a finite partial order is the shared path cover of its comparability DAG, which is transitively closed; Fulkerson (1956) proved Dilworth's theorem by this matching.
- **From Hamiltonian path.** On general graphs, path cover number 1 is Hamiltonian path; this gives the hardness.
- **To minimum cost flow.** Weighted versions, and the version where each vertex must be covered at least once, are flow problems with lower bounds.

## Applications

- **Fleet size.** Dantzig and Fulkerson (1954) found the least number of tankers to run a fixed schedule: trips are vertices, an arc $u \to v$ means one ship can do trip $v$ after trip $u$, and a path is the work of one ship.
- **Scheduling with precedences.** The least number of workers, machines or threads when each runs a chain of tasks.
- **Width of a partial order.** The width bounds the cost of many algorithms on DAGs, such as reachability labelings with one label per chain and sorting under partial information.
- **Test coverage.** The least number of test runs that visit every node of a control flow DAG, with shared nodes allowed.

## References
