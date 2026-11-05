---
tag: DV03YF
kind: problem
slug: graph-reachability
name: Graph reachability
aliases:
- s-t reachability
- single-source reachability
area: graphs/traversal
level: intro
summary: Decide which vertices can be reached from a given source vertex.
prereqs: [graph, walk]
see_also: [reachability, breadth-first-search, depth-first-search, whatever-first-search, transitive-closure, connected-components, savitch-theorem, dynamic-reachability]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.2, Breadth-first search, and Section 20.3, Depth-first search (the vertices discovered from a source are the vertices reachable from it)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 5, Basic graph algorithms (reachability, whatever-first search and its correctness)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 8, Space complexity (the language PATH, Savitch's theorem, the classes L and NL, NL-completeness of PATH, and NL = coNL)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 4, Space complexity (PATH is NL-complete, Savitch's theorem, the Immerman-Szelepcsényi theorem)
  - paper: doi:10.1145/1391289.1391291
    title: Omer Reingold, Undirected connectivity in log-space, Journal of the ACM 55(4), article 17 (2008)
    locator: the main theorem (undirected s-t connectivity is in deterministic logarithmic space)
---

The graph reachability problem asks, for a [graph](/graph/) and a source vertex $s$, which vertices can be reached from $s$ by following edges. Its decision form, "is there a path from $s$ to $t$", is the [reachability](/reachability/) problem, also called s-t connectivity. Any [graph traversal](/graph-traversal/) from $s$ solves it: [breadth-first search](/breadth-first-search/), [depth-first search](/depth-first-search/) and the generic [whatever-first search](/whatever-first-search/) all mark exactly the reachable vertices in $\Theta(n + m)$ time, which is optimal. The problem is also a central example of space complexity: directed s-t reachability is complete for [nondeterministic logarithmic space](/nondeterministic-logspace/), and the undirected version is in deterministic [logarithmic space](/logspace/).

## In plain words

You stand at one place in a network of one-way or two-way roads. Which places can you get to?

You do not need the shortest route, only whether a route exists. So you can explore in any order: walk to a new place, mark it, and keep going from the places you have marked. When no marked place has a road to an unmarked place, the marked places are exactly the ones you can reach.

## Definition

**Input.** A directed or undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, given by [adjacency lists](/adjacency-list/), and a vertex $s \in V$.

**Output.** The set $R(s) = \{ v \in V : \text{there is a walk from } s \text{ to } v \text{ in } G \}$, for example as a Boolean array.

A [walk](/walk/) from $s$ to $v$ exists exactly when a [simple path](/simple-path/) exists, because a walk with a repeated vertex can be shortened by removing the part between the two visits. The vertex $s$ is always in $R(s)$, by the walk with no edges.

**Decision form.** Given also $t$, decide whether $t \in R(s)$. In complexity theory this is the language PATH, or STCON for directed graphs and USTCON for undirected graphs.

**Certificate.** A "yes" answer is certified by a path from $s$ to $t$. A "no" answer is certified by a set $S \subseteq V$ with $s \in S$, $t \notin S$ and no edge from $S$ to $V \setminus S$; the set $R(s)$ itself is one.

## Variants

- **s-t reachability.** One target. See [reachability](/reachability/). A search can stop as soon as it marks $t$, and [bidirectional search](/bidirectional-search/) explores from both ends.
- **All pairs.** Find $R(v)$ for every $v$: the [transitive closure](/transitive-closure/) of $G$. One search from each vertex costs $O(n(n + m))$. [Warshall's algorithm](/warshall-algorithm/) costs $\Theta(n^3)$, and fast Boolean matrix multiplication gives $O(n^\omega \log n)$ by repeated squaring.
- **Undirected graphs.** Reachability is an equivalence relation, and its classes are the [connected components](/connected-components/). All components together cost $\Theta(n + m)$.
- **Strong reachability.** Both $v \in R(u)$ and $u \in R(v)$. The classes are the [strongly connected components](/strongly-connected-components/).
- **Dynamic.** Edges are inserted or deleted between queries. See [dynamic reachability](/dynamic-reachability/) and, for undirected graphs, [dynamic connectivity](/dynamic-connectivity/).
- **Implicit graphs.** The graph is given by a rule that lists the successors of a vertex, as in puzzles, games, program states and [model checking](/reachability-problem/). The cost is then measured in the number of states reached.
- **Space-bounded.** The input is read-only and the work space is small: the setting of the complexity classes L and NL.

## Examples

Take the directed graph with vertices 0 to 6 and the lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none; $5: 4, 6$; $6: 5$.

| source $s$ | $R(s)$ |
|---|---|
| 0 | 0, 1, 2, 3, 4 |
| 2 | 0, 1, 2, 3, 4 |
| 4 | 4 |
| 5 | 4, 5, 6 |

So 4 is reachable from every vertex, but only 4 is reachable from 4. Vertices 5 and 6 are not reachable from 0. The set $S = \{0, 1, 2, 3, 4\}$ has no edge leaving it, which certifies that 5 is not reachable from 0.

In the undirected graph with the edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,3\}$, $\{2,4\}$, $\{3,5\}$, $\{4,5\}$, $\{5,6\}$ on the vertices 0 to 7, the set reachable from 0 is $\{0, 1, \ldots, 6\}$, and 7 is reachable only from itself.

## Known algorithms

| algorithm | time | work space | notes |
|---|---|---|---|
| [breadth-first search](/breadth-first-search/) | $\Theta(n + m)$ | $\Theta(n)$ | also gives the distances |
| [depth-first search](/depth-first-search/) | $\Theta(n + m)$ | $\Theta(n)$ | also gives the DFS forest and times |
| [whatever-first search](/whatever-first-search/) | $O(n + m)$ with a stack or a queue | $O(n + m)$ | any order of exploration |
| [bidirectional search](/bidirectional-search/) | $O(n + m)$ | $\Theta(n)$ | s-t form, often much less in practice |
| Savitch's divide and conquer ([Savitch's theorem](/savitch-theorem/)) | $n^{O(\log n)}$ | $O(\log^2 n)$ bits | directed, s-t form |
| Reingold's algorithm | polynomial | $O(\log n)$ bits | undirected, s-t form |

The search algorithms are proved correct on their own pages. They all rest on one fact: if the marked set $M$ contains $s$ and every edge out of a marked vertex goes to a marked vertex, then $M \supseteq R(s)$, because a walk from $s$ that left $M$ would use an edge from $M$ to outside $M$.

Savitch's method decides whether $t$ is reachable from $s$ within $k$ steps by trying each middle vertex $w$ and asking the two questions with $k/2$ steps in turn, which reuses the space. The recursion has depth $\lceil \log_2 n \rceil$ with $O(\log n)$ bits per level.

## Bounds

**Time.** Each correct algorithm for single-source reachability needs $\Omega(n + m)$ time in the worst case on adjacency lists. It must write the answer for each of the $n$ vertices. For the edges, take any graph in which some vertex $z$ is not reachable from $s$ and all other vertices are. If the algorithm never reads some entry in the list of a reachable vertex $u$, change that entry to $z$. The algorithm reads the same values and gives the same output, but now $z$ is reachable, so the output is wrong. So the algorithm reads every entry of the lists of the reachable vertices, which can be $m$ entries.

**Space.** On a read-only input with a small work space:

- Directed s-t reachability is NL-complete under logspace reductions, so it is in L exactly when L = NL.
- By Savitch's theorem it is in $\mathrm{SPACE}(\log^2 n)$.
- By the Immerman-Szelepcsényi theorem, NL = coNL, so non-reachability is also in NL: a nondeterministic logspace machine can certify that $t$ is not reachable.
- Undirected s-t reachability is complete for the class SL of [symmetric logspace](/symmetric-logspace/), and Reingold proved in 2008 that it is in L. So SL = L.

## Reductions

- **Every NL problem reduces to it.** A nondeterministic logspace machine accepts exactly when its graph of configurations has a path from the start configuration to an accepting one. This graph has polynomial size and can be produced in logspace. This is why directed reachability is NL-complete.
- **2-SAT.** A 2-CNF formula is unsatisfiable exactly when some variable $x$ has a path from $x$ to $\lnot x$ and from $\lnot x$ to $x$ in its implication graph, so 2-SAT reduces to reachability and to [strongly connected components](/strongly-connected-components/).
- **Cycle through a vertex.** The vertex $v$ lies on a directed cycle exactly when $v$ is reachable from some successor of $v$.
- **Strong connectivity.** A directed graph is strongly connected exactly when every vertex is reachable from $s$ in $G$ and in the [transpose graph](/transpose-graph/). Two searches decide it.
- **From transitive closure.** One row of the closure is the single-source problem, so all-pairs reachability is at least as hard as $n$ single-source problems with shared input.

## Applications

- **Garbage collection.** The objects that a program can still use are those reachable from its roots. The marking phase of [mark-and-sweep](/mark-and-sweep/) is a graph search over the heap.
- **Model checking and verification.** A bad state can occur exactly when it is reachable from the initial state in the transition graph. See [the reachability problem](/reachability-problem/) and [symbolic reachability](/symbolic-reachability/).
- **Images and grids.** Filling a region of one colour is reachability in the grid graph of the pixels. See [flood fill](/flood-fill/) and [connected component labeling](/connected-component-labeling/).
- **Networks.** Which hosts a message can reach, which pages a crawler can find from a start page, which modules a program loads from its entry point.
- **Compilers.** Unreachable code is the set of basic blocks not reachable from the entry block in the control flow graph.

## References
