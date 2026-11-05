---
tag: S5MRH3
kind: algorithm
slug: johnson-elementary-cycles-algorithm
name: Johnson's algorithm for elementary cycles
aliases:
- Johnson's cycle enumeration
area: graphs/paths-and-cycles
level: advanced
summary: Lists all elementary cycles of a directed graph in O((n + m)(c + 1)) time, where c is the number of cycles, by a blocked depth-first search from the least vertex of each strong component.
solves: [enumerating-elementary-cycles]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs, c: the number of elementary cycles}
  time: {worst: O((n + m)(c + 1)), best: Θ(n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1975
  people: [Donald B. Johnson]
  note: Finding all the elementary circuits of a directed graph, SIAM Journal on Computing; the blocking rule bounds the work between two outputs.
prereqs: [simple-cycle, depth-first-search, strongly-connected-components]
see_also: [enumerating-elementary-cycles, read-tarjan-path-enumeration, tarjan-scc, cycle-detection, enumerating-simple-paths, directed-graph, self-loop, simple-path]
sources:
  - paper: doi:10.1137/0204007
    title: Donald B. Johnson, Finding all the elementary circuits of a directed graph, SIAM Journal on Computing 4(1), 77 to 84 (1975)
    locator: the algorithm CIRCUIT with the procedure UNBLOCK and the lists B, the outer loop over strong components, and the time bound O((n + e)(c + 1))
  - paper: Robert Tarjan, Enumeration of the elementary circuits of a directed graph, SIAM Journal on Computing 2(3), 1973
    title: Tarjan, backtracking enumeration of circuits with marked vertices
    locator: the algorithm and its time bound O(n e (c + 1))
  - paper: James C. Tiernan, An efficient search algorithm to find the elementary circuits of a graph, Communications of the ACM 13(12), 1970
    title: Tiernan, exhaustive search for elementary circuits
    locator: the search from each vertex over larger vertices
  - paper: doi:10.1002/net.1975.5.3.237
    title: R. C. Read and R. E. Tarjan, Bounds on backtrack algorithms for listing cycles, paths, and spanning trees, Networks 5(3), 237 to 252 (1975)
    locator: the bounds for listing cycles
---

Johnson's algorithm lists every elementary cycle of a [directed graph](/directed-graph/), that is, every [simple cycle](/simple-cycle/), exactly once. It takes the vertices in order, and for each vertex $s$ it searches for the cycles whose least vertex is $s$, inside the [strong component](/strongly-connected-components/) of $s$ in the graph of the vertices $\ge s$. A depth-first search from $s$ marks vertices as *blocked* when they cannot reach $s$ off the current path, and unblocks them, through lists $B$, only when a cycle is found that frees them. With this rule the time is $O((n + m)(c + 1))$ for $c$ cycles, so the work per cycle is linear even when the graph has exponentially many cycles.

## In plain words

You want to list every round trip in a network of one-way streets, where a round trip never visits the same corner twice.

Number the corners. First list the round trips through corner 0, then the ones through corner 1 that avoid corner 0, and so on. For each starting corner, explore streets from it, and every time you can step back to the start, write down the trip.

The trick is to stop exploring dead ends again and again. When a corner turns out to be useless, because every way from it back to the start is blocked by your own trail, you mark it and leave it alone. You also note which corners it waits for. When one of those corners is freed, the waiting corner is freed too.

## The problem

Given a directed graph $G = (V, E)$ with $V = \{0, \ldots, n - 1\}$, possibly with [self-loops](/self-loop/), parallel arcs and isolated vertices, list each elementary cycle once. A cycle is reported by its vertices $(v_0, v_1, \ldots, v_{k-1})$, with arcs $v_0 \to v_1 \to \cdots \to v_{k-1} \to v_0$ and $v_0$ the least of them. A self-loop at $v$ is the cycle $(v)$. Parallel arcs between the same pair give the same vertex sequence, so they are merged first; to list cycles by their arcs, multiply out the choices of parallel arcs along each reported cycle.

The graph must be directed. On an undirected graph read as a directed graph with two arcs per edge, the algorithm reports every edge as a cycle of length 2 and every longer cycle twice, once per direction; see [enumerating elementary cycles](/enumerating-elementary-cycles/) for undirected graphs.

## The algorithm

For a set $K$ of vertices, $A_K(v)$ is the list of successors of $v$ that are in $K$. The arrays $\mathrm{blocked}$ and $B$ are reset for the vertices of $K$ at the start of each phase. The pseudocode shows the recursive form of CIRCUIT; the implementation runs it with an explicit stack of frames.

```pseudo id=main
JOHNSON(G)
L1  s ← 0
L2  while s < n do
L3      K ← the strong component of G[{s, …, n − 1}] whose least vertex is least, among those with two or more vertices or a self-loop
L4      if there is no such component then stop
L5      s ← the least vertex of K
L6      for each v ∈ K do blocked[v] ← false; B[v] ← ∅
L7      CIRCUIT(s), with an empty stack
L8      s ← s + 1

CIRCUIT(v)
L9      f ← false; push v on the stack; blocked[v] ← true
L10     for each w ∈ A_K(v) do
L11         if w = s then output the stack as a cycle; f ← true
L12         else if not blocked[w] then if CIRCUIT(w) then f ← true
L13     if f then UNBLOCK(v)
L14     else for each w ∈ A_K(v) do if v ∉ B[w] then add v to B[w]
L15     pop v from the stack; return f

UNBLOCK(u)
L16     blocked[u] ← false
L17     for each w ∈ B[u] do remove w from B[u]; if blocked[w] then UNBLOCK(w)
```

The meaning of the marks: a vertex that is blocked and not on the stack has no path to $s$ that avoids the stack. $B[w]$ holds the vertices that were blocked while waiting for $w$; when $w$ is unblocked, they are unblocked too. Line L3 uses any linear-time strong component algorithm, for example [Tarjan's](/tarjan-scc/).

## Example

Take the vertices 0 to 5 and the arcs $0 \to 1$, $1 \to 2$, $1 \to 3$, $2 \to 0$, $2 \to 3$, $3 \to 0$, $3 \to 4$, $4 \to 3$ and the self-loop $4 \to 4$. Vertex 5 is isolated.

**Phase $s = 0$.** All of $0, \ldots, 4$ form one strong component $K$. The search runs as follows.

| step | stack | event |
|---|---|---|
| 1 | 0, 1, 2 | arc $2 \to 0$: output $(0, 1, 2)$ |
| 2 | 0, 1, 2, 3 | arc $3 \to 0$: output $(0, 1, 2, 3)$ |
| 3 | 0, 1, 2, 3, 4 | arcs $4 \to 3$ and $4 \to 4$ lead to blocked vertices; CIRCUIT(4) fails, 4 stays blocked, $4 \in B[3]$ and $4 \in B[4]$ |
| 4 | 0, 1, 2 | 3 found a cycle: UNBLOCK(3) unblocks 3, and through $B[3]$ also 4 |
| 5 | 0, 1 | 2 found a cycle: UNBLOCK(2) |
| 6 | 0, 1, 3 | arc $3 \to 0$: output $(0, 1, 3)$ |
| 7 | 0, 1, 3, 4 | 4 fails again and is blocked; then 3, 1 and 0 return true |

Step 3 shows the blocking: 4 cannot reach 0 without passing through 3, which is on the stack. Step 4 shows why 4 must be unblocked when 3 leaves the stack: in step 7, the path $0, 1, 3, 4$ is tried again, with 3 on the stack in a new position.

**Phase $s = 1$.** In the graph on $\{1, \ldots, 5\}$ the strong components are $\{1\}$, $\{2\}$, $\{3, 4\}$ and $\{5\}$. The first with a cycle is $\{3, 4\}$, so line L5 jumps to $s = 3$, and the search outputs $(3, 4)$.

**Phase $s = 4$.** The component $\{4\}$ has a self-loop; the search outputs $(4)$. Then $s = 5$, the only component $\{5\}$ has no cycle, and the algorithm stops.

The output is $(0, 1, 2)$, $(0, 1, 2, 3)$, $(0, 1, 3)$, $(3, 4)$, $(4)$: all five elementary cycles.

## Correctness

Each phase lists the cycles whose least vertex is $s$: such a cycle lies in the vertices $\ge s$ and is strongly connected, so it lies in the component $K$, and phases that line L5 skips have no such cycle. Within a phase the stack is always a simple path from $s$, because a vertex is pushed only when it is unblocked and a vertex on the stack is never unblocked; the second fact needs an argument about the order in which $B$-lists are filled. So every output is an elementary cycle, and different calls have different stacks, so no cycle is output twice. For completeness, the key invariant is that a blocked vertex off the stack has all its successors blocked and is in their $B$-lists, so every path from it to $s$ meets the stack. Then for any cycle $(s, c_1, \ldots, c_{k-1})$, the search pushes $c_1, c_2, \ldots$ in turn and outputs it. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with $B$-lists that support a membership test in $O(1)$ time (a bit per pair, or a hash set).

- **Outer loop.** Each phase that runs line L7 outputs at least one cycle, since $s$ lies on a cycle of $G[K]$ and, by completeness, that cycle is output. So lines L3 to L6 run at most $c + 1$ times, $O(n + m)$ each.
- **One phase.** Johnson shows that between the start of a phase and the first output, between two consecutive outputs, and between the last output and the end of the phase, the work is $O(n + m)$. The reason is the blocking rule: a vertex that the search leaves without finding a cycle stays blocked until a later cycle frees it, so no arc is explored twice without an output in between, up to a constant factor. A phase with $c_s$ outputs costs $O((n + m)(c_s + 1))$.
- **Total.** $O((n + m)(c + 1))$, with $\sum_s c_s = c$. The extra space is $O(n + m)$: the stack, the marks, and the $B$-lists, whose total size is at most the number of arcs, because $v$ is in $B[w]$ only for arcs $v \to w$.

On an acyclic graph the first strong component computation finds nothing, and the time is $\Theta(n + m)$. The number of cycles can be exponential: the complete digraph on $n$ vertices has $\sum_{k=2}^{n} \binom{n}{k}(k - 1)!$ of them, 84 for $n = 5$.

## Properties

- **Output-sensitive.** The time is linear per cycle, plus linear time in all.
- **Polynomial delay.** By Johnson's analysis, the time between two consecutive outputs within a phase is $O(n + m)$. Between phases there is one strong component computation, because line L5 jumps over all vertices that start no cycle, and each phase that starts outputs a cycle. So the delay is $O(n + m)$.
- **Order.** Cycles come out grouped by their least vertex, increasing, and within a group in depth-first order of the lists.
- **Deterministic.** With fixed lists, the output order is fixed.
- **Not recursive here.** The recursion of CIRCUIT and UNBLOCK can be $n$ deep, so the implementation uses explicit stacks.

## Variants and improvements

- **Tiernan (1970).** The plain search from each vertex over larger vertices, without blocking. It can spend exponential time between two outputs.
- **Tarjan (1973).** Marks vertices during a backtracking search and unmarks them when a cycle is found; $O(nm(c + 1))$ time.
- **Read and Tarjan (1975).** A search that never enters a branch without a cycle, for $O(n + m + mc)$ time; it lists cycles, paths and spanning trees with the same method (see [Read-Tarjan path enumeration](/read-tarjan-path-enumeration/)).
- **Szwarcfiter and Lauer (1976).** A depth-first method with the same bound as Johnson's.
- **Bounded length.** Listing only the cycles with at most $L$ vertices needs a change in the blocking rule, since a vertex that cannot reach $s$ within the remaining length may still lie on a longer cycle.
- **Undirected graphs.** For undirected graphs, Birmelé and others (2013) list the cycles in time proportional to the input plus the total length of the output.
- **Counting.** Counting the cycles is #P-complete, so no method avoids listing them one by one in general.

## When to use it

Use Johnson's algorithm to list all cycles of a directed graph that has few of them relative to its size, for example to report every circular dependency in a build or a module graph, every cycle of transactions in a fraud graph, or every feedback loop in a model. If the graph may have many cycles, consider whether a shorter answer suffices: [cycle detection](/cycle-detection/) finds one cycle in linear time, the strong components show where cycles are, and a cycle basis gives a small set that generates all cycles.

## Pitfalls

- **Forgetting UNBLOCK.** If a vertex that failed under one stack stays blocked for the rest of the phase, cycles are lost. Take the arcs $0 \to 1$, $0 \to 3$, $1 \to 2$, $1 \to 0$, $2 \to 1$, $3 \to 2$, with the lists in this order. With the stack $0, 1, 2$, vertex 2 fails, because its only successor 1 is on the stack. Then $1 \to 0$ gives $(0, 1)$, and UNBLOCK(1) frees 2 through $B[1]$. Later the stack $0, 3, 2, 1$ gives $(0, 3, 2, 1)$; if 2 had stayed blocked, this cycle would be lost.
- **Unblocking without the $B$-lists.** Unblocking every vertex when a cycle is found is correct but loses the time bound.
- **Searching outside $K$.** If the search from $s$ may enter vertices smaller than $s$, cycles are output once for each of their vertices.
- **Self-loops.** A self-loop at $s$ is the arc $s \to s$, and line L11 outputs it as $(s)$. A component of one vertex with a self-loop must count as nontrivial at line L3, or that cycle is lost.
- **Parallel arcs.** If parallel arcs are not merged, line L11 outputs the same vertex sequence once per arc to $s$, and line L10 explores the same successor twice.
- **Recursion depth.** A cycle through all $n$ vertices makes the recursion $n$ deep, which overflows the default stack of many languages.

## Implementations

## History

Tiernan (1970) and Weinblatt (1972) gave search methods that could spend exponential time between two outputs. Tarjan (1973) gave the first method with time polynomial per cycle, $O(nm)$. In 1975 Donald B. Johnson published the blocking rule with the $B$-lists, which brought the time per cycle down to $O(n + m)$, and Read and Tarjan published a backtracking method with a similar bound in the same year.

## References
