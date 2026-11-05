---
tag: K16C2B
kind: algorithm
slug: dag-longest-path
name: Longest path in a directed acyclic graph
aliases:
- DAG longest path
area: graphs/paths-and-cycles
level: intro
summary: Dynamic programming over a topological order gives the heaviest path from a source in a DAG in O(n + m) time; it is defined only for acyclic graphs.
solves: [longest-path-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1959
  people: [James E. Kelley, Morgan R. Walker]
  note: The critical path method for project scheduling, from Kelley and Walker in 1959, computes longest paths in an acyclic network of activities.
prereqs: [directed-acyclic-graph, topological-sort, dag-shortest-paths]
see_also: [longest-path-problem, critical-path, longest-to-shortest-paths-reduction, dag-dynamic-programming, kahns-algorithm, longest-increasing-subsequence, pert-chart, edge-relaxation]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.2, Single-source shortest paths in directed acyclic graphs (DAG-SHORTEST-PATHS, and critical paths in PERT charts found by negating the weights)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 4.7, Shortest paths in dags (longest paths by negating the weights) and Section 6.1, Shortest paths in dags, revisited
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.4, Shortest paths (longest paths in edge-weighted DAGs and the critical path method for parallel job scheduling)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 6, Dynamic programming, and Chapter 8, Shortest paths (dynamic programming over a topological order of a DAG)
  - book: "Michael R. Garey and David S. Johnson, Computers and Intractability: A Guide to the Theory of NP-Completeness, W. H. Freeman (1979)"
    locator: Appendix A2, problem ND29, Longest path
---

Longest path in a directed acyclic graph is a [dynamic program](/dag-dynamic-programming/) over a [topological order](/topological-sort/): it visits the vertices in that order and, for each edge $(u, v)$ of weight $w$, sets $L(v) \leftarrow \max(L(v), L(u) + w)$. On a [DAG](/directed-acyclic-graph/) with $n$ vertices and $m$ edges, with any real weights, it gives the heaviest path from a source $s$ to every vertex in $\Theta(n + m)$ time. The input must be directed and acyclic: in a general graph the [longest path problem](/longest-path-problem/) is NP-hard, and in a graph with a cycle the longest walk has no bound. It is the computation behind the [critical path](/critical-path/) of a project.

## In plain words

A project has tasks, and some tasks must wait for others. How long is the project at least? It is the longest chain of tasks that must run one after the other.

To find it, list the tasks so that every task comes after the tasks it waits for. Then go down the list. For each task, take the latest finish among the tasks it waits for, and add its own length. Because of the order of the list, when you reach a task, all the tasks it waits for are already done. The largest value at the end is the length of the longest chain, and you can trace the chain back by remembering which task gave each value.

## The problem

The input is a directed graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, a real weight $w(e)$ on each edge $e$, and a source $s$. Parallel edges are allowed. $G$ must be acyclic, so it has no self-loops; if it has a cycle, the algorithm reports it and stops.

The output is $L(v)$ for each vertex $v$: the largest total weight of a directed path from $s$ to $v$, or $-\infty$ if no path from $s$ reaches $v$. A parent pointer $\pi[v]$ gives one such path. In a DAG every walk is a path, because a walk that repeats a vertex contains a cycle, so it does not matter whether "path" means simple path or walk. With all weights 1, $L(v)$ is the largest number of edges on a path from $s$ to $v$.

## The algorithm

```pseudo id=main
DAG-LONGEST-PATH(G, w, s)
L1  T ← a topological order of G       ▷ Kahn's algorithm; stop if G has a cycle
L2  for each vertex v ∈ V do L[v] ← −∞, π[v] ← NIL
L3  L[s] ← 0
L4  for each vertex u in the order T do
L5      if L[u] ≠ −∞ then
L6          for each edge (u, v) ∈ E do
L7              if L[u] + w(u, v) > L[v] then
L8                  L[v] ← L[u] + w(u, v), π[v] ← u
L9  return L, π
```

This is [DAG shortest paths](/dag-shortest-paths/) with max in place of min and $-\infty$ in place of $+\infty$. Line L5 skips vertices that $s$ does not reach; without it, $-\infty + w$ would still be $-\infty$, so the test only saves work. Line L1 uses [Kahn's algorithm](/kahns-algorithm/), which also detects a cycle, because a vertex on a cycle never gets in-degree 0.

**All sources.** To find the heaviest path anywhere in $G$, start every $L[v]$ at 0 instead of $-\infty$ in lines L2 and L3. Then $L[v]$ is the heaviest path that ends at $v$, counting the path of one vertex with weight 0, and the answer is $\max_v L[v]$.

## Example

The DAG has 6 vertices and these arcs, with weights: $0 \to 1$ (3), $0 \to 2$ (2), $1 \to 3$ (4), $2 \to 3$ (6), $2 \to 4$ (1), $3 \to 5$ (2) and $4 \to 5$ (5). The source is $s = 0$. Kahn's algorithm with a first-in first-out queue gives the order $0, 1, 2, 3, 4, 5$.

| $u$ | $L[u]$ | arcs relaxed | changes |
|---|---|---|---|
| 0 | 0 | $0 \to 1$, $0 \to 2$ | $L[1] = 3$, $L[2] = 2$ |
| 1 | 3 | $1 \to 3$ | $L[3] = 7$, $\pi[3] = 1$ |
| 2 | 2 | $2 \to 3$, $2 \to 4$ | $L[3] = 8$, $\pi[3] = 2$; $L[4] = 3$ |
| 3 | 8 | $3 \to 5$ | $L[5] = 10$, $\pi[5] = 3$ |
| 4 | 3 | $4 \to 5$ | none, because $3 + 5 = 8 < 10$ |
| 5 | 10 | none | none |

The result is $L = (0, 3, 2, 8, 3, 10)$, and the parent pointers give the path $0 \to 2 \to 3 \to 5$ of weight 10. The shortest path from 0 to 5 is $0 \to 2 \to 4 \to 5$ with weight 8. The value of $L[3]$ went up from 7 to 8 when the second arc into 3 was relaxed: each vertex can change many times, but only before its own turn in the order.

## Correctness

The full proof is in the [correctness proof](proofs/correctness/). The key invariant is: when the loop of line L4 reaches $u$, every arc into $u$ comes from a vertex that is earlier in $T$ and has already been processed, so $L[u]$ is final. By induction along $T$, the final value of $L[u]$ is $\max_{(x, u) \in E} (L[x] + w(x, u))$, or 0 for $u = s$, and this is the recurrence of the heaviest path. The longest path problem in a DAG has [optimal substructure](/optimal-substructure/), unlike in general graphs: a prefix of a heaviest path to $v$ is a heaviest path to its end, because a heavier prefix could not meet the rest of the path again without a cycle.

## Complexity

Kahn's algorithm takes $\Theta(n + m)$ time. Lines L2 and L3 take $\Theta(n)$, and the loop of line L4 looks at each vertex once and at each arc at most once, so it takes $\Theta(n + m)$. The total is $\Theta(n + m)$ time in the best and the worst case. The extra space is $\Theta(n)$ for $L$, $\pi$, the in-degrees and the queue.

## Properties

- **Any weights.** Negative weights are allowed, since the order of the relaxations does not depend on the weights.
- **Directed only.** On an undirected graph each edge is a cycle of length 2 in both directions, and the longest path problem there is NP-hard.
- **Multigraphs.** Parallel arcs are allowed; the heaviest one wins at line L7. Self-loops are cycles and are rejected.
- **Exact arithmetic.** With integer weights, all values are sums of at most $n - 1$ weights, so they fit in a word of $O(\log n + \log W)$ bits, where $W$ is the largest absolute weight.

## Variants and improvements

- **Negate and use shortest paths.** Negate every weight and run [DAG shortest paths](/dag-shortest-paths/); the [longest-to-shortest reduction](/longest-to-shortest-paths-reduction/) is correct on a DAG because there is no cycle to become negative.
- **Vertex weights.** For task lengths on vertices, as in a [PERT chart](/pert-chart/), put the weight of $v$ on every arc into $v$, or add it when $v$ is processed.
- **Critical path method.** Compute the earliest start of each task forward and the latest start backward; the tasks where the two are equal lie on a [critical path](/critical-path/).
- **Counting longest paths.** Keep with each $L[v]$ the number of paths that reach that weight, and add the counts when there is a tie.
- **Memoized recursion.** $L(v) = \max_{(u, v)} (L(u) + w(u, v))$ computed with memoization from each vertex is the same algorithm in top-down form; it does an implicit [depth-first search](/depth-first-search/) instead of a topological sort.
- **Longest increasing subsequence.** The [longest increasing subsequence](/longest-increasing-subsequence/) of a sequence is the longest path in the DAG with an arc $i \to j$ for $i < j$ and $a_i < a_j$; faster special algorithms exist.

## When to use it

Use it for any scheduling, dependency or dynamic programming question that asks for the longest chain in an acyclic structure: build times, project length, pipeline latency, longest chains in a partial order. If the graph may have cycles, first test it with [cycle detection](/cycle-detection/), or collapse the [strongly connected components](/strongly-connected-components/) when the meaning allows it; on a graph with cycles, the longest simple path is an NP-hard problem.

## Pitfalls

- **Running on a graph with a cycle.** A Bellman-Ford style relaxation with max never settles on a positive cycle, and a topological sort does not exist. Check for a cycle first; the implementation raises an error.
- **Starting every value at 0.** Starting all values at 0 gives the heaviest path that ends at each vertex from any start, not from $s$. Both questions are useful, but they are different.
- **Treating $-\infty$ as a number.** In languages without an infinite value, a large negative constant plus a negative weight can overflow or look like a real path. Keep the test of line L5.
- **Using Dijkstra.** Greedy methods like [Dijkstra's algorithm](/dijkstra/) are wrong for longest paths, even on DAGs with positive weights, because the heaviest known value can still increase later.

## Implementations

## History

The method is the computation of the critical path method, which Kelley and Walker developed for project scheduling at DuPont and Remington Rand and published in 1959, and of PERT, developed for the United States Navy at about the same time. Garey and Johnson list the longest path problem for general graphs as NP-complete (problem ND29), which explains why the acyclic case is singled out. In algorithm textbooks it appears as the standard example of [dynamic programming over a DAG](/dag-dynamic-programming/).

## References
