---
tag: 5T2WQ4
kind: algorithm
slug: forward-backward-scc
name: Forward-backward SCC
aliases:
- FW-BW
- Fleischer-Hendrickson-Pinar algorithm
area: parallel/parallel-graph-algorithms
level: advanced
summary: 'Parallel SCC: pick a pivot, compute forward and backward reachable sets, and recurse on the three remaining parts.'
solves: [strongly-connected-components]
model: work-span-model
complexity:
  vars: {n: the number of vertices, m: the number of arcs, d: the depth of the recursion}
  time: {worst: O((n + m) d)}
  depth: {worst: O(n d log n)}
  space: {extra: O(n + m)}
properties: {deterministic: false, recursive: true}
prereqs: [strongly-connected-components, parallel-bfs, reachability, work-span-model]
see_also: [coloring-scc, tarjan-scc, kosaraju-sharir, condensation-graph, graph-transpose, randomized-quicksort, frontier-based-processing, transitive-closure]
sources:
  - paper: doi:10.1007/3-540-45591-4_68
    title: Lisa K. Fleischer, Bruce Hendrickson and Ali Pinar, On identifying strongly connected components in parallel, IPDPS 2000 Workshops, LNCS 1800
    locator: pp. 505 to 511 (the forward-backward divide and conquer and the lemma that every SCC lies in one of the four sets); DOI and pages to be checked
  - paper: "Don Coppersmith, Lisa K. Fleischer, Bruce Hendrickson and Ali Pinar, A divide-and-conquer algorithm for identifying strongly connected components, technical report, 2003"
    title: A divide-and-conquer algorithm for identifying strongly connected components
    locator: the analysis of the expected sequential time with a random pivot; the exact statement and its conditions are to be checked
  - paper: doi:10.1016/j.jpdc.2005.03.007
    title: William McLendon III, Bruce Hendrickson, Steven J. Plimpton and Lawrence Rauchwerger, Finding strongly connected components in distributed graphs, Journal of Parallel and Distributed Computing 65(8), 2005
    locator: pp. 901 to 910 (the trimming step and a distributed implementation); DOI and pages to be checked
  - paper: doi:10.1145/2503210.2503246
    title: Sungpack Hong, Nicole C. Rodia and Kunle Olukotun, On fast parallel detection of strongly connected components (SCC) in small-world graphs, SC 2013
    locator: the two-phase method with trimming, one large FW-BW step, and weakly connected components for the rest; DOI to be checked
---

Forward-backward SCC (FW-BW) finds the [strongly connected components](/strongly-connected-components/) of a directed graph by divide and conquer on reachability. It picks a pivot vertex, finds the set $F$ of vertices the pivot reaches and the set $B$ of vertices that reach it, both by [parallel BFS](/parallel-bfs/), and outputs $F \cap B$, which is the SCC of the pivot. Every other SCC lies entirely inside $F \setminus B$, $B \setminus F$ or the rest, so the three parts are solved independently and in parallel. A trimming step first removes the vertices that are their own SCC because they have no in-arc or no out-arc.

Notation on this page: $G = (V, A)$ is a directed graph with $n$ vertices and $m$ arcs. $F(p)$ and $B(p)$ are the forward and backward reachable sets of $p$ inside the current part. $d$ is the depth of the recursion, the number of levels. $W$ is the work, $S$ the span and $T_p$ the time on $p$ processors, in the [work-span model](/work-span-model/). The bounds proved on this page are worst case in terms of $d$; $d$ itself depends on the graph and on the random pivots, and there is no general polylogarithmic bound on it.

## In plain words

Think of one-way streets between places. Two places are in the same district if you can drive from each to the other.

Pick one place. Mark every place you can drive to from it, and, in a second color, every place from which you can drive to it. The places with both marks form the district of the chosen place.

Any other district is wholly inside the places with only the first mark, or wholly inside those with only the second mark, or wholly among the places with no mark. These three groups never share a district, so three teams can solve them at the same time, each in the same way.

A place with no road in, or no road out, is a district by itself. Removing such places first saves much work.

## The problem

The input is a directed graph. The output is the partition of $V$ into strongly connected components: $u$ and $v$ are in the same part exactly when $u$ reaches $v$ and $v$ reaches $u$. Sequentially, [Tarjan's algorithm](/tarjan-scc/) and [Kosaraju's algorithm](/kosaraju-sharir/) take $O(n + m)$ time, but they depend on depth-first search, which is hard to run in parallel. FW-BW uses only reachability, which parallel BFS computes level by level.

## The algorithm

$V$ is the current part; reachability is taken inside the subgraph induced by $V$.

```pseudo id=main
FW-BW(V)
L1  trim: while some v in V has no in-arc or no out-arc inside V, output {v} as an SCC and remove v      ▷ in parallel rounds
L2  if V is empty then return
L3  p ← a uniformly random vertex of V
L4  F ← the vertices of V reachable from p inside V      ▷ parallel BFS along the arcs
L5  B ← the vertices of V that reach p inside V          ▷ parallel BFS against the arcs
L6  output F ∩ B as one SCC
L7  in parallel do FW-BW(F \ B); FW-BW(B \ F); FW-BW(V \ (F ∪ B))
```

The implementation runs the recursion level by level with an explicit list of parts, so that each level is one parallel step over disjoint parts.

## Example

The graph has the vertices 0 to 7 and the arcs $0 \to 1$, $1 \to 2$, $2 \to 0$, $2 \to 3$, $3 \to 4$, $4 \to 3$, $5 \to 0$, $5 \to 6$, $6 \to 5$, $4 \to 7$. The pivot of each part is its least vertex.

| level | part | trimmed (L1) | pivot | $F$ | $B$ | SCC (L6) | new parts (L7) |
|---|---|---|---|---|---|---|---|
| 1 | 0 to 7 | 7 (no out-arc) | 0 | 0, 1, 2, 3, 4 | 0, 1, 2, 5, 6 | 0, 1, 2 | $\{3, 4\}$, $\{5, 6\}$ |
| 2 | 3, 4 | none | 3 | 3, 4 | 3, 4 | 3, 4 | none |
| 2 | 5, 6 | none | 5 | 5, 6 | 5, 6 | 5, 6 | none |

The SCCs are $\{0, 1, 2\}$, $\{3, 4\}$, $\{5, 6\}$ and $\{7\}$, found in 2 levels. The rest $V \setminus (F \cup B)$ is empty at level 1, because every vertex is related to 0.

## Correctness

The key lemma, proved in full in the proof file: for every SCC $C$ inside the part, if $C$ meets $F$ then $C \subseteq F$, and if $C$ meets $B$ then $C \subseteq B$. So $C$ lies in exactly one of $F \cap B$, $F \setminus B$, $B \setminus F$ and $V \setminus (F \cup B)$, and $F \cap B$ is the SCC of $p$. The proof file also shows that the SCCs of the subgraph induced by a part are exactly the SCCs of $G$ inside it, that a trimmed vertex is an SCC by itself, and that the recursion ends, because each call removes at least the pivot.

## Complexity

**Work.** The parts of one level are disjoint, and a BFS inside a part never follows an arc out of it. So one level does $O(n + m)$ work for trimming, the two searches and the split, and

$$W = O((n + m)\, d).$$

**Span.** A level has the span of its slowest part: the trimming rounds and the BFS rounds, each $O(\log n)$ span with a [pack](/parallel-pack/) per round. The number of BFS rounds is at most the size of the part, so $S = O(n\, d \log n)$ in the worst case, and much less when the parts have small diameter.

**Depth of the recursion.** The depth $d$ can be $\Theta(n)$. Without trimming, a graph with no arcs needs $n$ levels, one pivot per vertex. With trimming, $n/3$ disjoint directed triangles still need $n/3$ levels: each level finds one triangle and leaves all the others in the rest part. The tests check both cases.

**What is cited.** Coppersmith, Fleischer, Hendrickson and Pinar analyse the expected sequential time with a random pivot, using an implementation in which the rest part keeps its label and costs nothing to form; this page cites their bound and does not prove it. In the tests, on random digraphs with $m = 2n$ arcs, the mean depth with trimming is 1.4 for $n = 64$, 1.0 for $n = 256$ and 1.2 for $n = 1{,}024$, and the mean work is about $3.5 (n + m)$: trimming removes the many small SCCs and one pivot hits the giant SCC. Without trimming, the mean depth for $n = 1{,}024$ is about 130.

## Properties

- **Las Vegas.** The output is always correct; the pivots change only the cost.
- **Reachability only.** It needs only BFS, forward and backward, so it runs on any system that has a parallel BFS, including [frontier-based](/frontier-based-processing/) graph frameworks and distributed memory.
- **Recursive.** The three parts are independent subproblems, as in [randomized quicksort](/randomized-quicksort/). Unlike in quicksort, the rest part can hold almost all the vertices, so the depth is not $O(\log n)$ in general.
- **Good on one giant SCC.** On graphs with one giant SCC and many small ones, such as many real networks, trimming and one pivot do almost all of the work.

## Variants and improvements

- **Trimming.** McLendon, Hendrickson, Plimpton and Rauchwerger (2005) add line L1. Later codes also trim SCCs of size 2 by pattern.
- **Splitting by weak components.** After one large FW-BW step, the rest is split into weakly connected components, and each one is solved on its own, often by a sequential algorithm; this removes the disjoint-triangles problem. Hong, Rodia and Olukotun (2013) use this scheme for small-world graphs.
- **Many pivots at once.** Running searches from many pivots in the same round, with a rule for overlapping searches, reduces the depth; see [coloring SCC](/coloring-scc/), which takes every vertex as a pivot.
- **Condensation.** The SCCs give the [condensation graph](/condensation-graph/), a DAG on which later steps such as [transitive closure](/transitive-closure/) can run.

## When to use it

Use it to find SCCs on a parallel machine or a distributed graph, where depth-first search does not parallelize. It does best on graphs with a giant SCC and many trivial ones, together with trimming. For graphs with many medium SCCs, combine it with splitting by weak components or with coloring.

## Pitfalls

- **Leaving out trimming.** Graphs with many vertices that are their own SCC, such as random sparse digraphs, then need one level per such vertex; the depth in the tests grows from about 1 to about 130 for $n = 1{,}024$.
- **Paying for the rest part.** If forming $V \setminus (F \cup B)$ scans the whole part, each level costs $O(n + m)$ even when $F$ and $B$ are small. Relabel only $F$ and $B$, and let the rest keep the old label.
- **Searching outside the part.** The BFS must stop at arcs that leave the current part. A search that crosses into another part merges sets that are not SCCs.
- **Expecting a logarithmic depth.** The random pivot does not split the part evenly in general; disjoint cycles give linear depth.

## Implementations

## History

Fleischer, Hendrickson and Pinar (2000) proposed the forward-backward method for parallel SCC detection, motivated by sweep scheduling in transport problems on meshes. Coppersmith, Fleischer, Hendrickson and Pinar later analysed its expected sequential time with random pivots. McLendon, Hendrickson, Plimpton and Rauchwerger (2005) added trimming and a distributed implementation, and later work, such as that of Hong, Rodia and Olukotun (2013), combined it with weak components and coloring for large graphs on multicore machines.

## References
