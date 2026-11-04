---
tag: XXGARB
kind: technique
slug: dp-on-dag
name: Dynamic programming on directed acyclic graphs
aliases:
- DP on directed acyclic graphs
area: techniques/dynamic-programming
level: core
summary: Technique that computes dynamic programming values over a directed acyclic graph by processing vertices in topological order.
prereqs: [directed-acyclic-graph, topological-sort, optimal-substructure]
see_also: [dag-dynamic-programming, subproblem-graph, dag-shortest-paths, dag-longest-path, critical-path-method, min-plus-matrix-multiplication, viterbi-algorithm, tabulation]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.4 (topological sort) and Section 22.2 (single-source shortest paths in directed acyclic graphs, with the PERT chart application)
  - book: isbn:9780073523408
    title: Dasgupta, Papadimitriou and Vazirani, Algorithms
    locator: Section 6.1 (shortest paths in dags, revisited)
  - book: isbn:9780321295354
    title: Kleinberg and Tardos, Algorithm Design
    locator: Section 3.6 (directed acyclic graphs and topological ordering) and Chapter 6
---

Dynamic programming on a [directed acyclic graph](/directed-acyclic-graph/) computes a value $f(v)$ for each vertex of a graph that is given as the input, from the values of its neighbors, with the vertices taken in [topological order](/topological-sort/). One pass costs $O(n + m)$ time for $n$ vertices and $m$ edges, and it solves longest paths, shortest paths with negative weights, path counting and critical-path scheduling. This page is about graphs that you are given. The design method that builds an implicit graph of states for a problem that is not a graph problem is [dynamic programming on DAGs](/dag-dynamic-programming/) in the sense of Dasgupta, Papadimitriou and Vazirani.

## In plain words

Think of a set of tasks with arrows between them. An arrow from one task to another means that the first task must finish before the second starts. No chain of arrows comes back to where it started.

Put the tasks in a row so that every arrow points to the right. Now walk along the row from left to right. When you reach a task, every task with an arrow into it is already behind you, so its answer is already known. You combine those answers and write down the answer of the current task. One walk along the row is enough.

The same walk answers many questions: the longest chain of tasks, the cheapest route, or the number of different routes. Only the rule that combines the answers changes.

## When it applies

Look for these signals.

- The input is a directed graph, and the graph has no cycle, or the problem says so (a task schedule, a circuit, a dependency list, a grid with moves only right and down).
- The question is about paths: the best path from a source, the number of paths, or the best path that ends at each vertex.
- The value of a path is built from the edge values with one operation, such as a sum or a product, and paths are compared or totalled with a second operation, such as min, max or a sum.
- The second operation distributes over the first. For example $a + \min(b, c) = \min(a + b, a + c)$.

If the graph can have a cycle, the method does not apply as it is. A topological order exists if and only if the graph has no cycle.

## The template

Let $G = (V, E)$ be a directed acyclic graph with $n = |V|$ and $m = |E|$, a source $s$, and an edge label $w(u, v)$ for each edge. The holes are an operation $\oplus$ that combines the values of different paths, an operation $\otimes$ that extends a path by one edge, the identity $\mathbf{0}$ of $\oplus$ (the value of "no path") and the identity $\mathbf{1}$ of $\otimes$ (the value of the empty path).

```pseudo id=main
DAG-DP(G, s, w, ⊕, ⊗, 0, 1)               ▷ pull form
L1  order ← TOPOLOGICAL-SORT(G)
L2  for each vertex v do f[v] ← 0
L3  f[s] ← 1
L4  for each vertex v in order do
L5      for each edge (u, v) entering v do
L6          f[v] ← f[v] ⊕ (f[u] ⊗ w(u, v))
L7  return f
```

Line L1 takes $O(n + m)$ time with a [depth-first search](/depth-first-search/) or with [Kahn's algorithm](/kahns-algorithm/). Lines L4 to L6 look at each edge one time, so the loop does $m$ steps of $\oplus$ and $m$ steps of $\otimes$. The whole run takes $O(n + m)$ time when the two operations take constant time.

The holes give the classic problems.

| problem | $\oplus$ | $\otimes$ | $\mathbf{0}$ | $\mathbf{1}$ | $f(v)$ means |
|---|---|---|---|---|---|
| number of paths | $+$ | $\times$, with $w = 1$ | $0$ | $1$ | the number of paths from $s$ to $v$ |
| shortest path | $\min$ | $+$ | $+\infty$ | $0$ | the least weight of a path from $s$ to $v$ |
| longest path | $\max$ | $+$ | $-\infty$ | $0$ | the greatest weight of a path from $s$ to $v$ |
| reachability | or | and, with $w = $ true | false | true | whether $v$ can be reached from $s$ |
| widest path | $\max$ | $\min$ | $-\infty$ | $+\infty$ | the best bottleneck capacity from $s$ to $v$ |
| most likely path | $\max$ | $\times$ | $0$ | $1$ | the greatest product of probabilities |

**Claim.** Assume that $\oplus$ is associative and commutative with identity $\mathbf{0}$, that $\otimes$ is associative with identity $\mathbf{1}$, that $\mathbf{0} \otimes a = \mathbf{0}$, and that $\otimes$ distributes over $\oplus$ from the right: $(a \oplus b) \otimes c = (a \otimes c) \oplus (b \otimes c)$. These are the axioms of a semiring, without the left distributive law, which the proof does not use. Then at the end, for each $v$,
$$ f[v] = \bigoplus_{p \,:\, s \leadsto v} w(p), \qquad w(p) = w(e_1) \otimes w(e_2) \otimes \cdots \otimes w(e_k), $$
where the sum is over all paths $p = (e_1, \ldots, e_k)$ from $s$ to $v$, and an empty sum is $\mathbf{0}$.

**Proof.** By induction on the position of $v$ in the order. Consider the moment when the loop of line L4 reaches $v$. Each edge $(u, v)$ has $u$ before $v$ in the order, so $f[u]$ already has its final value, and the induction hypothesis holds for $u$. No later step changes $f[v]$, because line L6 writes only to the vertex of the current step. A path from $s$ to $v$ is either the empty path, when $v = s$, or a path from $s$ to some $u$ followed by one edge $(u, v)$. These cases do not overlap, since there is no cycle, so no nonempty path goes from $s$ back to $s$. For $v = s$, the only path is the empty one. Each edge $(u, s)$ has a tail $u$ that $s$ cannot reach, since that would close a cycle, so $f[u] = \mathbf{0}$ by the hypothesis and $f[u] \otimes w(u, s) = \mathbf{0}$. So $f[s] = \mathbf{1}$, the value of the empty path. For $v \ne s$, line L6 sums $f[u] \otimes w(u, v)$ over the entering edges. By the hypothesis and right distributivity, $f[u] \otimes w(u, v) = \bigoplus_{q : s \leadsto u} \bigl(w(q) \otimes w(u, v)\bigr)$, which is the sum over the paths to $v$ whose last edge is $(u, v)$. Summing over all entering edges gives each path to $v$ exactly once. ∎

The **push form** does the same work from the other side. It takes each $u$ in topological order and, for each edge $(u, v)$ that leaves $u$, it sets $f[v] \leftarrow f[v] \oplus (f[u] \otimes w(u, v))$. With $\min$ and $+$, this is the RELAX step of DAG-SHORTEST-PATHS in CLRS Section 22.2. The pull form needs the lists of entering edges, and the push form needs the lists of leaving edges, which is the usual adjacency list.

## Classic examples

### One graph, three questions

Take the vertices $s, a, b, c, d, t$ and the edges with these weights: $s \to a$ 2, $s \to b$ $-1$, $b \to a$ 4, $a \to c$ 3, $b \to c$ $-2$, $b \to d$ 6, $c \to d$ 1, $c \to t$ 5, $d \to t$ $-3$. A topological order is $s, b, a, c, d, t$. The pull form in this order gives:

| vertex | $s$ | $b$ | $a$ | $c$ | $d$ | $t$ |
|---|---|---|---|---|---|---|
| number of paths from $s$ | 1 | 1 | 2 | 3 | 4 | 7 |
| shortest path weight | 0 | $-1$ | 2 | $-3$ | $-2$ | $-5$ |
| longest path weight | 0 | $-1$ | 3 | 6 | 7 | 11 |

For example, $c$ has the entering edges from $a$ and $b$, so its count is $2 + 1 = 3$, its shortest weight is $\min(2 + 3, -1 - 2) = -3$, and its longest weight is $\max(3 + 3, -1 - 2) = 6$. The 7 paths from $s$ to $t$ have the weights 3, 10, 4, 11, $-5$, 2 and 2. The least is $-5$ on $s, b, c, d, t$ and the greatest is 11 on $s, b, a, c, t$. The graph has negative edges, and [Dijkstra's algorithm](/dijkstra/) would not be safe here, but the topological pass is.

### Shortest and longest paths

- [Shortest paths in a DAG](/dag-shortest-paths/) are the $(\min, +)$ case. They allow negative weights, and they take $\Theta(n + m)$ time, which is less than [Bellman-Ford](/bellman-ford/) needs on a general graph.
- [Longest paths in a DAG](/dag-longest-path/) are the $(\max, +)$ case. The [longest path problem](/longest-path-problem/) on a general graph is NP-hard, so the absence of cycles is what makes it easy. The same answer comes from the shortest-path pass with all weights negated.

### Critical path

A project is a set of jobs with durations and with precedence constraints that form a DAG. The earliest finish time of a job is its duration plus the largest earliest finish time of the jobs that must come before it. This is the longest-path pass, with the weight on the vertices. The least time of the whole project is the largest finish time, and a path that reaches it is a critical path: a delay of any job on it delays the project. CLRS Section 22.2 gives this application with PERT charts. See the [critical path method](/critical-path-method/) and [precedence-constrained scheduling](/precedence-constrained-scheduling/).

### Counting paths

With $\oplus = +$ and $\otimes = \times$, the pass counts paths, and the counts can be exponential in $n$. Chain $k$ diamonds: each diamond goes from a vertex to two middle vertices and then joins at one vertex. The graph has $3k + 1$ vertices and $2^k$ paths from the first vertex to the last. The pass adds $O(n + m)$ numbers, but each number can have $\Theta(n)$ bits. [Counting lattice paths](/counting-lattice-paths/) and [grid paths with obstacles](/grid-paths-with-obstacles/) are this case on the grid DAG.

### Hidden Markov models

The [Viterbi algorithm](/viterbi-algorithm/) finds the most likely sequence of hidden states. Its graph has one vertex for each pair of a time step and a state, and edges only from step $t$ to step $t + 1$. It is the $(\max, \times)$ case, or $(\max, +)$ on logarithms. The forward algorithm of a [hidden Markov model](/hidden-markov-model/) is the $(+, \times)$ case on the same graph.

## Variations

- **Pull and push.** Both forms do the same operations in a different order. Use the form that matches the adjacency lists that you have.
- **Memoized form.** Instead of a topological sort, compute $f(v)$ by a recursive call on each predecessor and store the result. This is [memoization](/memoization/), and the recursion visits the vertices in the order of a depth-first search. It computes only the values that the target needs, but it uses a stack of depth up to $n$.
- **Values on vertices.** When the weight is on the vertices, as in scheduling, use $f(v) = c(v) \otimes \bigoplus_{(u, v)} f(u)$, or move each vertex weight onto its leaving edges.
- **All sources.** For $f(v)$ = the best path that ends at $v$ from any start, set $f[v] \leftarrow \mathbf{1}$ for every vertex at line L2 (with $\oplus$ idempotent, such as min or max). Each vertex is then a possible start.
- **Reverse graph.** To compute the value of the best path from each vertex to a target $t$, run the pass on the graph with all edges reversed, or take the vertices in reverse topological order.
- **Other semirings.** Any semiring that meets the conditions of the claim works. For general graphs with cycles, the same sums need the closure of [Kleene algebra](/kleene-algebra/) or repeated squaring with [min-plus matrix multiplication](/min-plus-matrix-multiplication/).
- **Implicit graphs.** When the graph is not given but built from the states of a problem, the same pass is the design method of [dynamic programming on DAGs](/dag-dynamic-programming/). The analysis of that graph is the [subproblem graph](/subproblem-graph/).

## Pitfalls

- **A cycle in the input.** A topological sort of a graph with a cycle does not exist. Kahn's algorithm stops with vertices left over, and a depth-first search finds a back edge. Check this, or the pass computes values from predecessors that are not final. With weights, a cycle of positive weight makes the longest path unbounded on walks.
- **The wrong identity.** For the longest path, initialize the unreached vertices with $-\infty$, not 0. With 0, a vertex that $s$ cannot reach gets value 0, and a path from it looks like a path from $s$. In the example above, a vertex $x$ with the single edge $x \to t$ of weight 20 would give $t$ the wrong value 20.
- **The wrong order.** Taking the vertices by their names or by input order works only when that order is topological. A table with moves right and down is topological in row order. A general graph is not.
- **Overflow in counts.** Path counts grow up to $2^{\Theta(n)}$. Use big integers, or count modulo a prime when the problem asks for that.
- **A rule that does not distribute.** The pass is correct only when $\otimes$ distributes over $\oplus$. For example, the path with the least *average* edge weight is not a $(\min, \cdot)$ problem in this form: the best prefix for one continuation can be the wrong prefix for another.

## Exercises

1. Run the push form on the example graph with $(\min, +)$ and list the value of each vertex after each relaxation. Check that the final values match the table.
2. Add the vertex $x$ and the edge $x \to t$ of weight 20 to the example graph. Run the longest-path pass once with the identity $-\infty$ and once with 0. Explain the difference.
3. Give a $(+, \times)$ pass that computes, for each edge $(u, v)$, the number of paths from $s$ to $t$ that use that edge. Use two passes, one forward from $s$ and one backward from $t$.
   <details><summary>Hint</summary>The number is the count of paths from $s$ to $u$ times the count of paths from $v$ to $t$.</details>
4. Modify DAG-DP so that it also returns a longest path itself, not only its weight. State how much extra space this needs. See [traceback](/traceback/).
5. A DAG has jobs with durations on the vertices. Compute the earliest start and the latest start of each job for the least project time, and prove that the jobs with equal earliest and latest start contain a critical path.
6. Show that the claim fails without distributivity: find small numbers $a, b, c$ and a pair of operations for which $(a \oplus b) \otimes c \ne (a \otimes c) \oplus (b \otimes c)$, and a graph where the pass then gives a wrong answer.

## References
