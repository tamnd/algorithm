---
tag: W6YFXC
kind: algorithm
slug: ball-larus-path-profiling
name: Ball-Larus path profiling
aliases:
- efficient path profiling
area: compilers-and-program-analysis/optimizations
level: advanced
summary: Numbers the acyclic paths of a procedure so that adding values on some edges yields a unique path number, counting paths cheaply.
model: word-ram
complexity:
  vars: {V: the number of nodes of the DAG (basic blocks plus ENTRY and EXIT), E: the number of DAG edges after back edges are replaced by dummy edges, N: "the number of ENTRY-to-EXIT paths, assumed to fit in a word"}
  time: {worst: O(V + E log E)}
  space: {extra: Θ(V + E)}
properties: {deterministic: true, recursive: false, online: false, exact: true}
prereqs: [control-flow-graph, directed-acyclic-graph, topological-sort, maximum-spanning-tree, profile-guided-optimization]
see_also: [spanning-tree, fundamental-cycle, kruskal, depth-first-search, critical-edge-splitting, pettis-hansen-code-positioning, trace-scheduling, superblock-scheduling]
sources:
  - paper: doi:10.1109/MICRO.1996.566449
    title: Thomas Ball and James R. Larus, Efficient path profiling, Proceedings of the 29th Annual IEEE/ACM International Symposium on Microarchitecture (MICRO-29), Paris, 1996, 46-57
    locator: the numbering of the paths of a DAG (NumPaths and Val), the regeneration of a path from its number, the placement of increments on the chords of a spanning tree, and the treatment of loops by dummy edges for each back edge
  - paper: doi:10.1145/183432.183527
    title: Thomas Ball and James R. Larus, Optimally profiling and tracing programs, ACM Transactions on Programming Languages and Systems 16(4), 1994, 1319-1360
    locator: the placement of edge counters on the chords of a maximum spanning tree, and the recovery of the tree edge counts by flow conservation
---

Ball-Larus path profiling counts how often each acyclic path through a procedure runs. It gives each edge of the [control-flow graph](/control-flow-graph/) an integer so that the sum of the integers along any path from the entry to the exit is a number in $0, \ldots, N-1$, and different paths get different numbers. At run time a register adds up the integers of the edges it crosses, and at the end of the path it holds the path number, which indexes a table of counters. Loops are handled by cutting each back edge and recording a path there. A second step moves the integers to the chords of a [maximum spanning tree](/maximum-spanning-tree/), so that frequent edges carry no code. The profile feeds [profile-guided optimization](/profile-guided-optimization/).

## In plain words

Picture all the routes through a procedure that do not go around a loop. There can be very many, but they can be counted from the end backwards: a block with two exits has as many routes as its two successors added together. Now give each route a ticket number. At each branch, the routes that take the first exit get the lowest tickets, the routes that take the second exit get the next group, and so on. To make this happen, the program adds a fixed amount to a counter when it takes the second or a later exit. When the route ends, the counter is its ticket. Loops are cut where they jump back, and each trip around the loop is a route of its own. A last trick moves the additions off the busiest edges, so the program runs almost as fast as before.

## The problem

The input is a control-flow graph with a single entry block. The goal is to instrument it so that every run reports how many times each acyclic path ran, with as little work at run time as possible. An edge profile, which counts how often each edge runs, does not give this: two runs can cross the same edges the same number of times and still take different paths.

First the graph is made acyclic. A [depth-first search](/depth-first-search/) from the entry finds the back edges, the edges $b \to h$ to a block $h$ that is still on the search stack. Add two new nodes ENTRY and EXIT and an edge ENTRY $\to$ entry block. Every block that ends in `ret` gets an edge to EXIT. Each back edge $b \to h$ is removed, and two dummy edges take its place: a *start* edge ENTRY $\to h$ (one per header $h$) and a *stop* edge $b \to$ EXIT (one per source $b$). The result is a DAG $G = (V, E)$ in which ENTRY reaches every node and every node reaches EXIT. A path of $G$ always means a path from ENTRY to EXIT, and $N$ is their number.

The task on the DAG: find integers $\mathrm{Val}(e)$ on the edges such that the map from a path to the sum of $\mathrm{Val}$ along it is a bijection onto $\{0, \ldots, N-1\}$. Then find increments $\mathrm{Inc}(e)$ with the same sum on every path and with $\mathrm{Inc}(e) = 0$ on as much of the run-time traffic as possible.

## The algorithm

$\mathrm{out}(v)$ is the list of edges that leave $v$, in a fixed order. $\mathrm{num}(v)$ is the number of paths from $v$ to EXIT.

```pseudo id=main
BALL-LARUS(G, ENTRY, EXIT, weight)
L1  for each node v in reverse topological order do
L2      if v = EXIT then num(v) <- 1
L3      else
L4          num(v) <- 0
L5          for each edge e = v -> w in out(v), in order do
L6              Val(e) <- num(v)
L7              num(v) <- num(v) + num(w)
L8  H <- the undirected multigraph of G plus one edge EXIT -- ENTRY
L9  T <- a maximum spanning tree of H by weight that contains EXIT -- ENTRY
L10 phi(ENTRY) <- 0
L11 for each edge u -> v of G in T, walking T outwards from ENTRY do
L12     set phi of the new endpoint so that phi(v) = phi(u) + Val(u -> v)
L13 for each edge e = u -> v of G do
L14     Inc(e) <- Val(e) + phi(u) - phi(v)
L15 return num, Val, Inc

REGENERATE(r)                         // 0 <= r < num(ENTRY)
L16 v <- ENTRY; path <- empty
L17 while v != EXIT do
L18     find the edge e = v -> w in out(v) with Val(e) <= r < Val(e) + num(w)
L19     append e to path; r <- r - Val(e); v <- w
L20 return path
```

Lines L1 to L7 number the paths. The first edge out of a node gets value 0, and each later edge gets the number of paths through the earlier edges, so the paths through each edge form one block of consecutive numbers. REGENERATE inverts this and turns a path number back into its path.

Lines L8 to L14 are the placement. Walking the tree in L11 and L12 means: start at ENTRY, and for each tree edge with one endpoint already set, set the other endpoint from it (forwards along $u \to v$ with $+\mathrm{Val}$, or backwards with $-\mathrm{Val}$). The edge EXIT -- ENTRY is in the tree and carries no value, so $\phi(\mathrm{EXIT}) = \phi(\mathrm{ENTRY}) = 0$. Then $\mathrm{Inc}(e) = 0$ on every tree edge, so only the chords need code.

The instrumented program keeps a register $r$:

- on the edge ENTRY $\to$ entry: $r \gets \mathrm{Inc}$ of that edge (the reset and the first increment in one instruction);
- on an edge $e$ that is a chord with $\mathrm{Inc}(e) \ne 0$: $r \gets r + \mathrm{Inc}(e)$;
- at a `ret` block $b$: count the path $r + \mathrm{Inc}(b \to \mathrm{EXIT})$;
- on a back edge $b \to h$: count the path $r + \mathrm{Inc}(\text{stop edge of } b)$, then $r \gets \mathrm{Inc}(\text{start edge of } h)$.

"Count the path $t$" is `count[t] += 1` in an array when $N$ is small, and in a hash table keyed by $t$ when $N$ is large. Code on an edge goes into a new block on the edge, as in [critical edge splitting](/critical-edge-splitting/). The implementation here records the sequence of paths of one run in a single integer, so the tests can compare it with the blocks the run executed.

## Example

Take the DAG with nodes A to F and edges A$\to$B, A$\to$C, B$\to$C, B$\to$D, C$\to$D, D$\to$E, D$\to$F, E$\to$F, with A as ENTRY and F as EXIT. In reverse topological order, $\mathrm{num}$ is F 1, E 1, D 2, C 2, B 4 and A 6. The edges with a nonzero value are the second exits: $\mathrm{Val}(A \to C) = 4$, $\mathrm{Val}(B \to D) = 2$ and $\mathrm{Val}(D \to F) = 1$. The six paths get these numbers:

| path | sum of Val | number |
|---|---|---|
| A B C D E F | 0 + 0 + 0 + 0 + 0 | 0 |
| A B C D F | 0 + 0 + 0 + 1 | 1 |
| A B D E F | 0 + 2 + 0 + 0 | 2 |
| A B D F | 0 + 2 + 1 | 3 |
| A C D E F | 4 + 0 + 0 + 0 | 4 |
| A C D F | 4 + 0 + 1 | 5 |

To regenerate path 3: at A, edge A$\to$B covers numbers 0 to 3, so take it. At B with $r = 3$, B$\to$C covers 0 to 1 and B$\to$D covers 2 to 3, so take B$\to$D and set $r = 1$. At D, D$\to$F covers 1, so the path is A B D F.

Now suppose a profile run took A C D F 75 times and each other path 5 times. The edge frequencies are A$\to$B 20, A$\to$C 80, B$\to$C 10, B$\to$D 10, C$\to$D 90, D$\to$E 15, D$\to$F 85 and E$\to$F 15. Kruskal's algorithm on these weights, with F -- A taken first, puts C$\to$D, D$\to$F, D$\to$E and A$\to$B in the tree. The potentials are $\phi(A) = 0$, $\phi(B) = 0$, $\phi(F) = 0$, $\phi(D) = -1$, $\phi(C) = -1$ and $\phi(E) = -1$, so the increments are A$\to$C 5, B$\to$C 1, B$\to$D 3, E$\to$F $-1$ and 0 on the four tree edges. Every path keeps its number: A C D F gives $5 + 0 + 0 = 5$ and A B C D E F gives $0 + 1 + 0 + 0 - 1 = 0$. With one add on each edge that has a nonzero amount, the plain values run $80 + 10 + 85 = 175$ adds, and the tree placement runs $80 + 10 + 10 + 15 = 115$. On the hot path A C D F the only code left is on A$\to$C, the first edge, which becomes the reset $r \gets 5$.

A loop in the toy IR:

```
# params: n
B0:
  i = 0
  s = 0
  jump B1
B1:
  t = i < n
  br t B2 B3
B2:
  s = s + i
  i = i + 1
  jump B1
B3:
  ret s
```

The back edge is B2$\to$B1. The DAG has the edges ENTRY$\to$B0, B0$\to$B1, B1$\to$B2, B1$\to$B3, B3$\to$EXIT, the start edge ENTRY$\to$B1 and the stop edge B2$\to$EXIT. There are four paths: 0 is B0 B1 B2 (ends at the back edge), 1 is B0 B1 B3, 2 is B1 B2 (one more trip around the loop) and 3 is B1 B3 (the last test and the return). A run with $n = 2$ is the path sequence 0, 2, 3. With the tree ENTRY$\to$B0, B0$\to$B1, B1$\to$B2, B1$\to$B3, the only nonzero increments are on the dummy edges: $\mathrm{Inc}(B3 \to \mathrm{EXIT}) = 1$ and $\mathrm{Inc}(\mathrm{ENTRY} \to B1) = 2$. So no edge inside the loop body gets an add. The back edge code is "count $r$, then $r \gets 2$", and B3 counts $r + 1$.

## Correctness

The full proof is in the proof file. The three parts:

- **Numbering.** By induction in reverse topological order, the sums of $\mathrm{Val}$ along the paths from a node $v$ to EXIT are exactly $0, \ldots, \mathrm{num}(v) - 1$, each once. The paths through the $i$-th edge $v \to w$ get the block $\mathrm{Val}(v \to w) + \{0, \ldots, \mathrm{num}(w) - 1\}$, and these blocks tile the range. Regeneration follows the same blocks, so it inverts the map.
- **Placement.** For any spanning tree of $H$ that contains EXIT -- ENTRY, $\mathrm{Inc}(u \to v) = \mathrm{Val}(u \to v) + \phi(u) - \phi(v)$. Along a path from ENTRY to EXIT the $\phi$ terms telescope to $\phi(\mathrm{ENTRY}) - \phi(\mathrm{EXIT}) = 0$, so the sums of Inc and Val agree. On a tree edge Inc is 0 by the choice of $\phi$.
- **Loops.** Each run splits in one way into DAG paths, cut at every crossing of a back edge. Between two cuts the register holds the sum of Inc over the DAG edges crossed so far in the current DAG path, so each count records the number of the path that just ended.

## Complexity

The numbering visits each node and edge once after a [topological sort](/topological-sort/), so it takes $\Theta(V + E)$ word operations. [Kruskal's algorithm](/kruskal/) takes $O(E \log E)$ to sort the edges and almost linear time for the union-find steps, and the potentials take $\Theta(V + E)$ more. Regeneration of one path takes $O(\text{its length} + \text{the out-degrees on it})$. At run time, each crossed chord with a nonzero increment costs one add, and each path end costs one counter update.

The numbers are the catch. $N$ can grow exponentially in $V$: a chain of $k$ diamonds has $2^k$ paths. The word-RAM bound assumes $N$ fits in a word. Real tools fall back to a hash table, or cut the procedure into smaller regions, when $N$ is too large for an array of counters.

## Properties

- The path numbers are dense: they are exactly $0, \ldots, N-1$, so an array of $N$ counters is enough.
- The method is exact. It counts each acyclic path, not an estimate from edge counts.
- The values do not depend on the profile. Only the placement uses frequencies, and any spanning tree that contains EXIT -- ENTRY gives correct counts.
- The number of edges with a nonzero Val is at most $E - V + 1$: each node other than EXIT has its first out-edge at 0. The tree placement can have nonzero increments on all $E - V + 2$ chords. Its gain is in where the code goes, not in how many edges carry it.
- An edge profile can be recovered from a path profile: the count of an edge is the sum of the counts of the paths through it. The converse fails.

## Variants and improvements

- **Edge profiling.** Ball and Larus's earlier placement puts one counter on each chord of a maximum spanning tree and recovers the tree edges by flow conservation (the flow into a node equals the flow out). Path profiling uses the same tree for a different purpose.
- **Profile to a hash table.** When $N$ is large, the counts go to a hash table keyed by the path number, and only the paths that run take space.
- **Interprocedural and longer paths.** Later work extends the numbering across calls or across loop iterations, at the cost of many more paths.
- **Sampling.** A tool can turn the instrumentation on only part of the time to lower the overhead, at the cost of exact counts.

## When to use it

Use it when an optimization needs correlated branch behavior, for example [trace scheduling](/trace-scheduling/), [superblock scheduling](/superblock-scheduling/) or the choice of a hot path to specialize. If only edge or block frequencies are needed, as for [code layout](/pettis-hansen-code-positioning/), an edge profile is cheaper and enough. For long-running production code, sampling with hardware counters avoids instrumentation altogether.

## Pitfalls

- **Counter overflow.** The path register and the numbers can overflow a machine word on large procedures. Check $N$ at compile time and switch to a hash table or split the procedure.
- **Every cycle must lose an edge.** If a cycle is left in the graph, there is no reverse topological order and the numbering does not exist. Cutting the back edges of a depth-first search breaks every cycle, also in a graph that is not reducible.
- **The tree must contain EXIT -- ENTRY.** Without it, $\phi(\mathrm{EXIT}) \ne \phi(\mathrm{ENTRY})$ in general, and every path sum is off by the same constant. The counts then go to the wrong slots.
- **Not fewer edges.** Chord placement does not reduce the number of instrumented edges. It reduces the weighted cost only if the weights predict the real run. On random graphs it can do worse than plain Val placement for some frequencies, and it is a heuristic.
- **Code on the edge.** An increment on an edge whose source has several successors and whose target has several predecessors needs a new block on the edge; putting it at the end of the source or the start of the target counts other paths too.
- **Loops are split.** A path profile does not say which iterations follow which, and two runs with the same per-iteration paths in a different order look the same.

## Implementations

## History

Before path profiles, compilers used block or edge counts. Ball and Larus showed in 1994 how to place edge counters on the chords of a maximum spanning tree, and in 1996 they gave the path numbering, its regeneration and the chord placement for paths. Their method became the usual way to collect path profiles, and later work reused the numbering for longer paths and for calling contexts.

## References
