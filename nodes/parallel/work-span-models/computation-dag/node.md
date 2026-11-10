---
tag: 54BC6D
kind: data-structure
slug: computation-dag
name: Computation dag
aliases:
- computation DAG
- multithreaded computation DAG
area: parallel/work-span-models
level: core
summary: Directed acyclic graph of one run of a parallel program, with strands as vertices and continuation, spawn, call and return edges; its size is the work and its longest path is the span.
implements: [graph]
model: word-ram
complexity:
  vars: {n: the number of strands, m: the number of edges}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [work-span-model, directed-acyclic-graph, topological-sort, adjacency-list]
see_also: [work-and-span, critical-path, dag-longest-path, kahns-algorithm, fork-join-model, parallel-fibonacci, greedy-scheduling, expression-dag]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1, the part on a model for multithreaded execution (strands, continuation, spawn, call and return edges, Figure 27.2 for the dag of P-FIB(4)), and Section 24.2 for the longest path in a dag in Θ(V + E) time
  - paper: doi:10.1145/324133.324234
    title: "Robert D. Blumofe and Charles E. Leiserson, Scheduling multithreaded computations by work stealing, Journal of the ACM 46(5), 1999"
    locator: the model of a multithreaded computation as a dag of unit-time instructions grouped into threads
  - paper: doi:10.1145/227234.227246
    title: "Guy E. Blelloch, Programming parallel algorithms, Communications of the ACM 39(3), 1996"
    locator: the work and depth of a computation, read off its dag
---

A computation DAG is the [directed acyclic graph](/directed-acyclic-graph/) of one run of a parallel program: its vertices are strands, which are runs of instructions with no parallel control, and its edges say which strand must finish before which other strand can start. In the terms of CLRS (third edition, Chapter 27), each edge is a continuation, spawn, call or return edge. The number of strands is the work $W$, and the number of strands on a longest path is the span $S$. One pass in [topological order](/topological-sort/) finds both in $\Theta(n + m)$ time.

## In plain words

Write down every step that a program did in one run, one box for each step. Draw an arrow from one box to another when the second step had to wait for the first. Steps that the program ran one after the other are joined by a line of arrows. When the program starts a task that may run at the same time as the rest, the arrows split into two lines, and they join again where the program waits for the task to finish.

The picture has no loops, because no step waits for a later step. Two numbers tell you a lot about the run. The first is how many boxes there are. The second is how many boxes lie on the longest line of arrows. No team of workers, however large, can finish faster than that longest line.

## The abstract type

The structure stores a DAG $G = (V, E)$ of $n$ strands and $m$ edges, with a kind on each edge. It supports:

- ADD-STRAND: add a new strand and return its number.
- ADD-EDGE$(u, v, kind)$: add the edge $u \to v$ of the given kind.
- WORK-AND-SPAN: return $(W, S)$, where $W = |V|$ and $S$ is the number of vertices on a longest path, or report a cycle.
- CRITICAL-PATH: return one longest path.

The structure is the object that the [work-span model](/work-span-model/) measures. The operations on it are ordinary sequential operations, and their costs on this page are in the [word RAM](/word-ram/). On a computation DAG with unit-time strands, the measures are as below.

| Symbol | Meaning |
|---|---|
| $n$ | the number of strands (on this page, not the input size of the program) |
| $m$ | the number of edges |
| $p$ | the number of processors that run the DAG |
| $W$, $T_1$ | the work, equal to $n$ |
| $S$, $D$, $T_\infty$ | the span, the number of strands on a longest path |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the parallelism |

**The four kinds of edges.** The terms are those of CLRS, third edition, Section 27.1. A strand $u$ is followed in the same procedure by a strand $u'$.

- A *continuation edge* $u \to u'$ joins two strands of one procedure that follow each other.
- A *spawn edge* $u \to v$ goes from the strand $u$ that spawns a procedure to the first strand $v$ of that procedure. A spawn also adds the continuation edge $u \to u'$, because the parent goes on at the same time.
- A *call edge* $u \to v$ goes from the strand that calls a procedure to its first strand. A call adds no continuation edge, because the parent waits.
- A *return edge* $u \to x$ goes from the last strand $u$ of a spawned procedure to the strand $x$ right after the next sync of the parent. This page also puts a return edge from the last strand of a called procedure to the strand right after the call. In P-FIB this is the same strand as the strand after the sync, because the call is the last thing before the sync.

The run starts with one first strand and ends with one last strand. The fourth edition of CLRS (Chapter 26) describes the same model, and this page uses the terms of the third edition.

## Representation

The structure keeps, for each strand $v$, a label, a list $succ[v]$ of successors and a list $pred[v]$ of predecessors ([adjacency lists](/adjacency-list/) in both directions). A hash map $kind$ maps each edge $(u, v)$ to its kind. The invariant is:

> **(C1)** $v \in succ[u]$ if and only if $u \in pred[v]$ if and only if $(u, v)$ is a key of $kind$. **(C2)** Each edge joins two existing strands, no edge is a loop, and each kind is one of the four kinds. **(C3)** Each pair $(u, v)$ is at most one edge.

Acyclicity is not checked on each insertion. WORK-AND-SPAN checks it, in the same pass. A program that builds the DAG from a run, as the tracer below does, gives a DAG by construction, because each edge goes from an older strand to a newer one.

## Operations

ADD-STRAND appends an empty successor list, an empty predecessor list and a label. ADD-EDGE checks the kind and the two strands, ignores a pair that is already an edge, and then appends to both lists and the map. The main operation is WORK-AND-SPAN. It is [Kahn's algorithm](/kahns-algorithm/) with a longest-path count, the same pass as for the [longest path in a DAG](/dag-longest-path/).

```pseudo id=main
WORK-AND-SPAN(G)                          ▷ returns (W, S) or reports a cycle
L1  for each strand v do indeg[v] ← |pred[v]|, d[v] ← 0
L2  Q ← a queue of the strands v with indeg[v] = 0
L3  W ← 0, S ← 0
L4  while Q is not empty do
L5      u ← remove the first strand of Q
L6      W ← W + 1
L7      d[u] ← d[u] + 1                    ▷ now d[u] = strands on a longest path that ends at u
L8      S ← max(S, d[u])
L9      for each edge u → v do
L10         d[v] ← max(d[v], d[u])
L11         indeg[v] ← indeg[v] − 1
L12         if indeg[v] = 0 then append v to Q
L13 if W < n then error "the graph has a cycle"
L14 return (W, S)
```

Before line L7 runs for $u$, $d[u]$ is the largest $d$ value of a predecessor of $u$, or 0 for a source. Line L7 adds $u$ itself.

CRITICAL-PATH runs the same pass and keeps a parent pointer for each strand.

```pseudo id=critical
CRITICAL-PATH(G)
    for each strand v do d[v] ← 0, back[v] ← NIL
    for each strand u in topological order do
        d[u] ← d[u] + 1
        for each edge u → v do
            if d[u] > d[v] then d[v] ← d[u], back[v] ← u
    z ← a strand with the largest d[z]
    return the path that follows back from z, reversed
```

A program in the fork-join style can build its own DAG while it runs. The tracer keeps a current strand for each active procedure and opens a new strand after each spawn, call or sync.

```pseudo id=trace
TRACE-SPAWN(u, B)                         ▷ the current strand u of the parent spawns B
    v ← the first strand of B; add spawn edge u → v
    u' ← a new strand of the parent; add continuation edge u → u'
    run B; remember the last strand of B for the next sync

TRACE-CALL(u, B)
    v ← the first strand of B; add call edge u → v
    run B; z ← its last strand
    u' ← a new strand of the parent; add return edge z → u'

TRACE-SYNC(u)
    x ← a new strand of the parent; add continuation edge u → x
    for each remembered last strand z of a spawned child do add return edge z → x
```

Each procedure ends with an implicit sync. Strands are opened only when the parent does more work, so a procedure that does no work after a call or a sync does not get an empty strand.

## Example

**P-FIB(4).** The tracer on the procedure P-FIB of CLRS, which spawns P-FIB$(n-1)$, calls P-FIB$(n-2)$ and then syncs, gives 17 strands and a span of 8, the numbers of CLRS, third edition, Figure 27.2. The edges are 4 spawn edges, 4 call edges, 4 continuation edges and 8 return edges. In general the tracer gives $W = 4F_{n+1} - 3$ and $S = 2n$ for $n \ge 2$, where $F_k$ is the $k$-th [Fibonacci number](/fibonacci-numbers/).

**A run of WORK-AND-SPAN.** Take the DAG of a parallel sum of four numbers, with unlabelled edges. Strand 0 splits the input, strands 1 and 5 split the halves, strands 2, 3, 6 and 7 are the leaves, strands 4 and 8 add the halves, and strand 9 adds the two half sums. The edges are $0 \to 1$, $0 \to 5$, $1 \to 2$, $1 \to 3$, $5 \to 6$, $5 \to 7$, $2 \to 4$, $3 \to 4$, $6 \to 8$, $7 \to 8$, $4 \to 9$ and $8 \to 9$. The table shows the state after each strand leaves the queue.

| step | $u$ | $d[u]$ after L7 | $W$ | $S$ | $Q$ after L12 |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 1 | 1 | 1, 5 |
| 2 | 1 | 2 | 2 | 2 | 5, 2, 3 |
| 3 | 5 | 2 | 3 | 2 | 2, 3, 6, 7 |
| 4 | 2 | 3 | 4 | 3 | 3, 6, 7 |
| 5 | 3 | 3 | 5 | 3 | 6, 7, 4 |
| 6 | 6 | 3 | 6 | 3 | 7, 4 |
| 7 | 7 | 3 | 7 | 3 | 4, 8 |
| 8 | 4 | 4 | 8 | 4 | 8 |
| 9 | 8 | 4 | 9 | 4 | 9 |
| 10 | 9 | 5 | 10 | 5 | empty |

The result is $(W, S) = (10, 5)$. A critical path is $0, 1, 2, 4, 9$.

## Correctness

WORK-AND-SPAN removes each strand from the queue at most once, and it removes a strand only after all its predecessors, so the order of removal is a topological order of the strands it removes. By induction along that order, $d[u]$ after line L7 is the number of strands on a longest path that ends at $u$: such a path is $u$ alone, or a longest path to some predecessor followed by $u$, and line L10 has taken the maximum over all predecessors before $u$ enters the queue. So $S$ is the largest such count, which is the span. No strand on a cycle is ever removed, and each strand that cannot be reached from a cycle is removed, so $W = n$ exactly when $G$ is acyclic, and line L13 reports a cycle otherwise. The full proof, with the proof for CRITICAL-PATH, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

The costs are in the word RAM, with a hash map for the edge kinds.

| operation | time | notes |
|---|---|---|
| ADD-STRAND | $O(1)$ amortized | appends to three lists |
| ADD-EDGE | $O(1)$ expected | one hash map lookup for a repeated pair |
| WORK-AND-SPAN | $\Theta(n + m)$ worst | each strand enters and leaves $Q$ once, and each edge is looked at once in line L9 |
| CRITICAL-PATH | $\Theta(n + m)$ worst | the same pass, plus a walk of $S$ parent pointers |
| tracer, per spawn, call or sync | $O(1)$ amortized, plus $O(1)$ per return edge | the run of the program itself is extra |
| space | $\Theta(n + m)$ | both adjacency lists and the map |

A fork-join DAG has $m \le 2n$: each strand has at most two outgoing edges (a spawn edge and a continuation edge, or one call, continuation or return edge), so the time is $\Theta(n) = \Theta(W)$ for such DAGs.

## Variants

- **Weighted strands.** Give each strand a time $t(v)$ and add $t(u)$ instead of 1 in lines L6 and L7. A strand of time $k$ acts like a chain of $k$ unit strands.
- **Series-parallel parse tree.** A fork-join DAG is series-parallel. Its parse tree has a leaf for each strand and an inner node for each series or parallel composition. The [composition rules](/work-span-model/) then give $W$ and $S$ in one bottom-up pass over the tree, without the edges.
- **DAGs with futures.** Futures and other synchronization that is not nested give DAGs that are not series-parallel. WORK-AND-SPAN still works, because it needs only a DAG, but the composition rules do not.
- **Expression DAGs.** The DAG of the operations of an arithmetic expression, an [expression DAG](/expression-dag/), is the kind of DAG that Brent (1974) studied.

## When to use it

Use the explicit DAG to get the exact work and span of one run, for example in tests of a parallel algorithm, to check a span bound, or to feed a schedule simulator such as [greedy scheduling](/greedy-scheduling/). For asymptotic bounds of an algorithm on all inputs of size $n$, use [work-span analysis](/work-span-analysis/) with recurrences, since a DAG gives the costs for one input only.

## Pitfalls

- **Overwriting instead of taking the maximum.** Line L10 must be $d[v] \leftarrow \max(d[v], d[u])$. Writing $d[v] \leftarrow d[u]$ keeps the count of the last predecessor that was removed, not of the one with the longest path, and gives a span that is too small.
- **Counting edges instead of strands.** In this page the span counts strands, as in CLRS. If line L8 runs before line L7, so that $S \leftarrow \max(S, d[u])$ uses the old value, the result is the number of edges on a longest path, $S - 1$. Both conventions appear in the literature, so state which one you use.
- **No cycle check.** Without line L13, a graph with a cycle returns a pair with $W < n$ and no error. A DAG that a program builds is acyclic, but a DAG that is read from a file or built by hand may not be.
- **Recursion depth is not span.** Merge sort with a serial merge has recursion depth $\lceil \lg n \rceil$ and span $\Theta(n)$. The span is a property of the DAG, and the DAG contains the strands of the merge.

## Implementations

The Python module has the class with WORK-AND-SPAN and CRITICAL-PATH, a tracer that runs fork-join programs written with spawn, call and sync, and helpers for series and parallel composition. The tests build the DAGs of a parallel sum, of P-FIB, and of merge sort with a serial and with a parallel merge, and check the work and span against the composition rules and against closed forms.

## History

Graham (1966) studied tasks with a precedence order on identical processors, which is a DAG of tasks. Brent (1974) bounded the time to evaluate an arithmetic expression with $p$ processors by counting the operations at each level of its computation. Blumofe and Leiserson (1994, journal version 1999) modelled a multithreaded computation as a DAG of unit-time instructions grouped into threads, and used it to analyse work stealing. The terms strand, continuation edge, spawn edge, call edge and return edge are those of CLRS, third edition (2009), Chapter 27, which bases its model on this line of work.

## References
