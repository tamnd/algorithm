---
tag: R2Q1DA
kind: algorithm
slug: parallel-push-relabel
name: Parallel push-relabel
aliases:
- parallel preflow-push
- Goldberg-Tarjan parallel maximum flow
area: parallel/parallel-graph-algorithms
level: advanced
summary: Push-relabel maximum flow where pushes and relabels on different vertices run concurrently.
solves: [max-flow-problem, min-cut-problem]
model: work-span-model
complexity:
  vars: {n: the number of vertices, m: the number of arcs}
  time: {worst: O(n^2 (n + m))}
  depth: {worst: O(n^2 log n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [push-relabel, max-flow-problem, preflow, residual-graph, work-span-model]
see_also: [edmonds-karp, dinic, blocking-flow, distance-labeling, max-flow-min-cut-theorem, parallel-bfs, frontier-based-processing, almost-linear-max-flow]
sources:
  - paper: doi:10.1145/48014.61051
    title: Andrew V. Goldberg and Robert E. Tarjan, A new approach to the maximum-flow problem, Journal of the ACM 35(4), 921 to 940 (1988)
    locator: the section on the parallel and distributed implementations, with pulses and the O(n^2 log n) time bound on n processors; section number to be checked
  - paper: "Andrew V. Goldberg, Efficient graph algorithms for sequential and parallel computers, PhD thesis, MIT, 1987"
    title: Efficient graph algorithms for sequential and parallel computers
    locator: the parallel push-relabel method and its analysis; chapter to be checked
  - paper: "Richard J. Anderson and João C. Setubal, A parallel implementation of the push-relabel algorithm for the maximum flow problem, Journal of Parallel and Distributed Computing, 1995"
    title: A parallel implementation of the push-relabel algorithm for the maximum flow problem
    locator: the shared-memory implementation with a concurrent global relabeling; volume and pages to be checked
  - paper: "Niklas Baumstark, Guy E. Blelloch and Julian Shun, Efficient implementation of a synchronous parallel push-relabel algorithm, ESA 2015"
    title: Efficient implementation of a synchronous parallel push-relabel algorithm
    locator: the synchronous rounds with parallel global relabeling and the measurements; pages to be checked
---

Parallel push-relabel computes a maximum flow by running the [push-relabel method](/push-relabel/) of Goldberg and Tarjan on all active vertices at the same time. The algorithm works in synchronous pulses. In a pulse, every vertex with excess pushes the excess it holds along its admissible arcs, those that go one label down, and then every vertex that still has excess and no admissible arc raises its label. Both steps use the labels from the start of the pulse, and the two ends of an arc pair are never both admissible, so the work of different vertices does not conflict. There are fewer than $4n^2$ pulses.

Notation on this page: $G = (V, A)$ is a directed graph with $n$ vertices, $m$ arcs, integer capacities, a source $s$ and a sink $t$. $r(v, w)$ is the residual capacity, $e(v)$ the excess and $d(v)$ the label of $v$; $d_0$ is the labeling at the start of a pulse. An arc $(v, w)$ is admissible if $r(v, w) > 0$ and $d_0(v) = d_0(w) + 1$. $W$ is the work and $S$ the span, in the [work-span model](/work-span-model/) with a sum per target (fetch-and-add). The bounds in the front matter are worst case and are proved here. The bound of Goldberg and Tarjan for $n$ processors is cited.

## In plain words

Think of tanks on platforms at different heights, joined by pipes. Water goes only one platform down at a time. At the start, the source floods every pipe that leaves it.

Then everyone works at the same tick of a clock. Each tank that holds water sends it down the pipes that go one step lower, as far as they take it. After that, each tank that still holds water and sees no pipe one step lower is lifted, to one step above its lowest neighbour.

Water that can reach the sink drains into it. Water that cannot is lifted above the source and runs back to it. When no tank holds water, the flow is as large as it can be.

## The problem

The input is a directed graph with nonnegative integer capacities, a source $s$ and a sink $t$. The output is a flow of maximum value, the [maximum flow problem](/max-flow-problem/); the vertices that $s$ reaches in the final residual graph give a minimum cut. Sequential push-relabel performs one operation at a time. The goal here is to do the pushes and relabels of many vertices in one step, with a proved bound on the number of steps.

## The algorithm

```pseudo id=main
PARALLEL-PUSH-RELABEL(G, c, s, t)
L1  f ← 0; d(s) ← n; d(v) ← 0 for all v ≠ s
L2  for all arcs (s, v) in parallel do push c(s, v) along (s, v)
L3  while some v ∉ {s, t} has e(v) > 0 do      ▷ one pulse
L4      d0 ← d; e0 ← e
L5      for all v ∉ {s, t} with e0(v) > 0 in parallel do
L6          push e0(v) along the admissible arcs of v, in order, each up to r      ▷ a prefix sum
L7      for all w in parallel do e(w) ← e(w) + the amount that arrived at w
L8      for all v ∉ {s, t} with e(v) > 0 and no admissible arc in parallel do
L9          d(v) ← 1 + min{d0(w) : r(v, w) > 0}
L10 return f
```

A vertex pushes only the excess $e_0(v)$ that it held at the start; what arrives in the pulse waits for the next one. Line L8 also relabels vertices that were not active at the start but received excess and have no admissible arc.

## Example

The arcs are $s \to 1$ (3), $s \to 2$ (2), $1 \to 2$ (1), $1 \to t$ (1) and $2 \to t$ (3), with $n = 4$. After line L2, $d = (4, 0, 0, 0)$ for $(s, 1, 2, t)$, $e(1) = 3$ and $e(2) = 2$.

| pulse | active (L5) | pushes (L6) | relabels (L9) | $d(1)$, $d(2)$ after | $e(1)$, $e(2)$, $e(t)$ after |
|---|---|---|---|---|---|
| 1 | 1, 2 | none: all labels are 0 | $d(1) = 1$, $d(2) = 1$ | 1, 1 | 3, 2, 0 |
| 2 | 1, 2 | 1 unit $1 \to t$, 2 units $2 \to t$ | $d(1) = 1 + d_0(2) = 2$ | 2, 1 | 2, 0, 3 |
| 3 | 1 | 1 unit $1 \to 2$ | $d(1) = 1 + d_0(s) = 5$ | 5, 1 | 1, 1, 3 |
| 4 | 1, 2 | 1 unit $1 \to s$, 1 unit $2 \to t$ | none | 5, 1 | 0, 0, 4 |

The flow has value 4: 2 units on $s \to 1$, 2 on $s \to 2$, 1 on $1 \to 2$, 1 on $1 \to t$ and 3 on $2 \to t$. In pulse 3, vertex 1 has one unit that can reach $t$ no more, so it rises above $d(s) = 4$ and sends that unit back to $s$ in pulse 4. In pulse 4, vertices 1 and 2 push at the same time.

## Correctness

The proof file proves, in full:

1. in one pulse, an arc and its reverse are never both admissible, so the pushes of different vertices do not interfere, and the synchronous pulse equals some sequence of ordinary pushes;
2. the labels stay valid, $d(v) \le d(w) + 1$ on every residual arc, even though many vertices are relabeled at once from the old labels, and each relabel raises a label by at least 1;
3. every vertex with excess has a residual path to $s$, so no label exceeds $2n - 1$;
4. when no vertex is active, valid labels with $d(s) = n$ leave no residual path from $s$ to $t$, so the flow is maximum.

## Complexity

**Pulses (proved).** Let $\Phi$ be the largest label of an active vertex. A pulse with no relabel lowers $\Phi$ by at least 1, since all excess at the top level moves one level down. A pulse with relabels raises $\Phi$ by at most its total label increase. The total label increase is below $2n^2$, so there are fewer than $2n^2$ pulses of each kind, and fewer than $4n^2$ in all.

**Work and span (proved).** A pulse reads every vertex and the arcs of the active and relabeled vertices, $O(n + m)$ work. The split of the excess over the admissible arcs is a prefix sum, the arriving amounts are a sum per target, and a relabel is a minimum, each with $O(\log n)$ span. So

$$W = O(n^2 (n + m)), \qquad S = O(n^2 \log n).$$

**Cited.** Goldberg and Tarjan (1988) give the pulse version with $O(n^2 \log n)$ time on $n$ processors, which matches the span above. The work bound is larger than the $O(n^3)$ bound of sequential FIFO push-relabel, since a pulse may read all the arcs of vertices that push little.

**Measured.** On random digraphs with $m = 4n$ arcs and capacities from 1 to 100, from vertex 0 to vertex $n - 1$, the mean number of pulses over 4 runs is 164, 1,167 and 2,998 for $n = 32$, 128 and 512, about $5n$ to $9n$. Most pulses move excess that cannot reach $t$ up above $d(s) = n$ and back to $s$. The tests assert a mean below $c \cdot n$ with $c = 16$. The number of pulses is not polylogarithmic in $n$.

## Properties

- **Deterministic.** The labels and pushes depend only on the input and the arc order.
- **Local.** A vertex reads only its arcs and the labels of its neighbours, so the method also runs in distributed systems, one vertex per process.
- **Synchronous.** The labels of the last pulse are the only shared state that a vertex reads, so no locks are needed in a pulse.

## Variants and improvements

- **Global relabeling.** A backward BFS from $t$ in the residual graph sets every label to the exact distance to $t$. Done from time to time, with [parallel BFS](/parallel-bfs/), it cuts the number of pulses by a large factor in practice. Anderson and Setubal (1995) and Baumstark, Blelloch and Shun (2015) use it.
- **Gap heuristic.** If no vertex has label $k$, every vertex with a label between $k$ and $n$ cannot reach $t$, and its label can be raised to $n + 1$ at once.
- **Asynchronous versions.** Vertices push and relabel on their own, with atomic updates of the excess and a check of the labels at push time. Such versions need more care to prove, and they do not have pulses to count.
- **Two phases.** In the two-phase form of push-relabel, the first phase does not process vertices with a label of $n$ or more. At its end, the vertices that cannot reach $t$ in the residual graph give a minimum cut, and the second phase only returns the remaining excess to $s$. For a minimum cut alone, the second phase can be skipped.

## When to use it

Use it for maximum flow and minimum cut on large graphs on shared-memory machines or GPUs, with global relabeling, for example in image segmentation with graph cuts. Without global relabeling, the number of pulses grows with $n$, as the measurements show. For graphs with short augmenting paths, a parallel version of [Dinic's algorithm](/dinic/) or of [Edmonds-Karp](/edmonds-karp/), which uses parallel BFS for each phase, can be simpler.

## Pitfalls

- **Pushing the new excess in the same pulse.** If a vertex pushes what it received in the current pulse, the pushes depend on the order of the vertices, and the proof of the bound fails.
- **Relabeling from the new labels.** All relabels of a pulse must read $d_0$. Mixing old and new labels can make the labeling invalid.
- **Arc pairs.** Each input arc needs its own reverse in the residual graph. Merging antiparallel arcs into one pair is possible, but it changes how the flow on each input arc is read back.
- **Concurrent updates of the excess.** Many vertices can push to one target in a pulse. The amounts must be added with a fetch-and-add or a sum per target.

## Implementations

## History

Goldberg (1987) and Goldberg and Tarjan (1988) introduced the push-relabel method, and gave parallel and distributed versions with synchronous pulses. Anderson and Setubal (1995) made one of the first shared-memory implementations, with concurrent global relabeling. Later work studied asynchronous and lock-free versions, and Baumstark, Blelloch and Shun (2015) gave a fast synchronous implementation with parallel global relabeling.

## References
