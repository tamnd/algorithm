---
tag: 83VY7T
kind: data-structure
slug: forward-star
name: Forward star
aliases:
- forward-star representation
area: graphs/graph-representation
level: core
summary: Edges sorted by tail vertex with a per-vertex index of first outgoing edge.
implements: [graph]
prereqs: [edge-list, adjacency-list, counting-sort]
see_also: [compressed-sparse-row, compressed-sparse-column, edge-list, incidence-list, flow-network, residual-graph, network-simplex, dinic]
sources:
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows
    locator: Section 2.3 (Network representations), the forward star representation with the point array, the reverse star with the rpoint and trace arrays, and the comparison with adjacency lists
  - book: isbn:9783540779773
    title: Kurt Mehlhorn and Peter Sanders, Algorithms and Data Structures, The Basic Toolbox
    locator: Section 8.2 (Representation of graphs by adjacency arrays), the static edge array grouped by source with a first-edge index per node
---

The forward star stores a directed [graph](/graph/), often a [flow network](/flow-network/), as an array of arcs sorted by their tail, together with an array $\mathit{point}$ in which $\mathit{point}[i]$ is the index of the first arc out of vertex $i$. Each arc is a record with its tail, its head and its data, such as a cost and a capacity, and its index in the array is its permanent name. A second index, the *reverse star*, lists for each vertex the names of the arcs that enter it, so that both the out-arcs and the in-arcs of a vertex are found in time linear in their number, while the data of each arc is stored once. The layout is the [compressed sparse row](/compressed-sparse-row/) idea with whole arc records, and it is the standard representation of networks in the network flow literature.

## In plain words

Write all the arcs of the network in a table, one row per arc, with its start, its end, its cost and its capacity. Sort the table by the start vertex, so the arcs leaving vertex 0 come first, then those leaving vertex 1, and so on. Then keep a short list that says on which row the arcs of each vertex begin.

Now the arcs leaving a vertex sit together. To find the arcs entering a vertex, build a second short index that lists, for each vertex, the row numbers of the arcs that end there. The index holds only row numbers, so when a flow algorithm changes the flow on an arc, it changes one row, and both indexes see the change.

## The abstract type

The forward star implements the query part of the [graph](/graph/) type for a directed graph with named arcs: `out-arcs(G, i)`, `in-arcs(G, j)`, `out-degree`, `in-degree`, and access to the tail, head and data of an arc by its name. It allows parallel arcs and self-loops, since each arc has its own name, so it also stores directed [multigraphs](/multigraph/). An undirected graph is stored with two arcs per edge. The arcs are fixed once BUILD has run; their data, such as a flow value, may change.

## Representation

The structure has $n$ and $m$, and:

- the arc arrays $\mathit{tail}[0 \ldots m-1]$, $\mathit{head}[0 \ldots m-1]$ and any data arrays such as $\mathit{cost}$ and $\mathit{cap}$, indexed by arc name $e$;
- the array $\mathit{point}[0 \ldots n]$;
- the reverse star: an array $\mathit{rpoint}[0 \ldots n]$ and an array $\mathit{trace}[0 \ldots m-1]$ of arc names.

**Invariant (F).**

- (F1) $\mathit{tail}$ is non-decreasing, $\mathit{point}[0] = 0$, $\mathit{point}[n] = m$, and the arcs out of $i$ are exactly the names $e$ with $\mathit{point}[i] \le e < \mathit{point}[i+1]$.
- (F2) $\mathit{rpoint}[0] = 0$, $\mathit{rpoint}[n] = m$, $\mathit{rpoint}$ is non-decreasing, and $\mathit{trace}[\mathit{rpoint}[j] \ldots \mathit{rpoint}[j+1] - 1]$ lists exactly the names of the arcs with head $j$, each once, in increasing order.

Since each arc out of $i$ has tail $i$ by (F1), the $\mathit{tail}$ array is redundant, and many codes drop it and find the tail of $e$ by a binary search in $\mathit{point}$. The space is $2(n + 1)$ offsets, $m$ trace entries, and $m$ records of $2 + k$ fields for $k$ data fields.

## Operations

```pseudo id=main
BUILD(n, A)                          ▷ A: a list of m arcs (t, h, data)
L1  stably sort A by tail with a counting sort; name the arcs 0 … m − 1 in this order
L2  point[i] ← the number of arcs with tail less than i, for i in 0 … n
L3  rpoint[j] ← the number of arcs with head less than j, for j in 0 … n
L4  rpos[j] ← rpoint[j] for each j in 0 … n − 1
L5  for e ← 0 to m − 1 do
L6      j ← head[e]; trace[rpos[j]] ← e; rpos[j] ← rpos[j] + 1

OUT-ARCS(G, i)
L7  for e ← point[i] to point[i + 1] − 1 do output e

IN-ARCS(G, j)
L8  for k ← rpoint[j] to rpoint[j + 1] − 1 do output trace[k]

OUT-DEGREE(G, i)
L9  return point[i + 1] − point[i]

IN-DEGREE(G, j)
L10 return rpoint[j + 1] − rpoint[j]
```

**Build** (lines L1 to L6) is a [counting sort](/counting-sort/) of the arcs by tail, which fixes their names and gives $\mathit{point}$ as [prefix sums](/prefix-sums/) of the out-degrees, followed by a second counting pass by head that fills the reverse star with arc names. Both passes take $\Theta(n + m)$ time. Since line L5 visits the names in increasing order, each segment of $\mathit{trace}$ comes out sorted.

**Out-arcs and in-arcs** (lines L7 and L8) take $\Theta(d^+(i))$ and $\Theta(d^-(j))$ time. They return arc names, so the caller reads $\mathit{head}[e]$, $\mathit{tail}[e]$, $\mathit{cost}[e]$ or the current flow $x[e]$ in $O(1)$ time per arc, and an update of $x[e]$ found through the reverse star is seen at once through the forward star.

**Degrees** (lines L9 and L10) read two offsets, in $O(1)$ time.

**Updates of the arc set.** As with CSR, adding or removing an arc renames all later arcs and requires a rebuild in $\Theta(n + m)$ time. Flow algorithms do not change the arc set, only the flows, so this is no limit for them.

## Example

Take the directed graph on $\{0, \ldots, 4\}$ with the arcs and costs below, given to BUILD in this order.

$$A = (3, 4; 2),\ (0, 2; 5),\ (2, 3; 1),\ (3, 1; 4),\ (0, 1; 3),\ (1, 2; 1).$$

Line L1 sorts them stably by tail and names them:

| name $e$ | tail | head | cost |
|---|---|---|---|
| 0 | 0 | 2 | 5 |
| 1 | 0 | 1 | 3 |
| 2 | 1 | 2 | 1 |
| 3 | 2 | 3 | 1 |
| 4 | 3 | 4 | 2 |
| 5 | 3 | 1 | 4 |

The out-degrees are $2, 1, 1, 2, 0$, so line L2 gives $\mathit{point} = [0, 2, 3, 4, 6, 6]$. The in-degrees are $0, 2, 2, 1, 1$, so line L3 gives $\mathit{rpoint} = [0, 0, 2, 4, 5, 6]$. Lines L5 and L6 place the names:

| arc $e$ | head $j$ | slot $\mathit{rpos}[j]$ | $\mathit{trace}$ after the step |
|---|---|---|---|
| 0 | 2 | 2 | \_ \_ 0 \_ \_ \_ |
| 1 | 1 | 0 | 1 \_ 0 \_ \_ \_ |
| 2 | 2 | 3 | 1 \_ 0 2 \_ \_ |
| 3 | 3 | 4 | 1 \_ 0 2 3 \_ |
| 4 | 4 | 5 | 1 \_ 0 2 3 4 |
| 5 | 1 | 1 | 1 5 0 2 3 4 |

So $\mathit{trace} = [\ \mid 1, 5 \mid 0, 2 \mid 3 \mid 4]$. Then:

- OUT-ARCS$(3)$ gives the names 4 and 5, the arcs $3 \to 4$ with cost 2 and $3 \to 1$ with cost 4.
- IN-ARCS$(1)$ gives the names 1 and 5, the arcs $0 \to 1$ and $3 \to 1$.
- A flow algorithm that pushes 7 units along arc 5 writes $x[5] = 7$ once. Both OUT-ARCS$(3)$ and IN-ARCS$(1)$ then see the new flow.

The rows of the sorted heads, $[2, 1 \mid 2 \mid 3 \mid 4, 1 \mid\ ]$, are the CSR rows of the same graph, kept in input order.

## Correctness

Line L1 sorts the arcs by tail, so the arcs with tail $i$ form one block of names, and line L2 sets $\mathit{point}[i]$ to the start of that block, which gives (F1). Lines L3 to L6 are a counting sort of the names by head: $\mathit{rpoint}[j]$ is the number of arcs with smaller heads, so the segments of $\mathit{trace}$ have the right lengths, and each name is written once into the next free slot of the segment of its head. Names are visited in increasing order, so each segment is increasing, which gives (F2). The queries then read one block or one segment, and the degrees are block and segment lengths. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | notes |
|---|---|---|
| build | $\Theta(n + m)$ | two counting passes |
| out-arcs$(i)$ | $\Theta(d^+(i))$ | consecutive names |
| in-arcs$(j)$ | $\Theta(d^-(j))$ | through $\mathit{trace}$ |
| out-degree, in-degree | $O(1)$ | |
| read or write the data of arc $e$ | $O(1)$ | by name |
| tail of $e$ without a tail array | $O(\log n)$ | binary search in $\mathit{point}$ |
| is $(i, j)$ an arc | $O(d^+(i))$, or $O(\log d^+(i))$ if blocks are sorted by head | |
| add or remove an arc | $\Theta(n + m)$ | rebuild, arcs are renamed |
| space | $2(n + 1) + m$ words plus $m$ arc records | |

**Flow algorithms.** A [residual graph](/residual-graph/) needs, for each arc $e = (i, j)$, the forward residual arc out of $i$ and the backward residual arc out of $j$. With the forward and reverse stars, a scan of the residual arcs out of a vertex $i$ reads the forward star of $i$, for the arcs with residual capacity $\mathit{cap}[e] - x[e] > 0$, and the reverse star of $i$, for the arcs with $x[e] > 0$, in $\Theta(d^+(i) + d^-(i))$ time. So [Ford-Fulkerson](/ford-fulkerson/), [Edmonds-Karp](/edmonds-karp/), [Dinic](/dinic/) and the [network simplex](/network-simplex/) method run on the forward star with their usual bounds, and each arc keeps one flow value.

## Variants

- **Without the tail array.** The tail of arc $e$ is the $i$ with $\mathit{point}[i] \le e < \mathit{point}[i+1]$. Codes that need it often, such as cycle-canceling methods, keep the array.
- **Paired arcs.** Many max-flow codes store each arc together with its reverse residual arc, at names $2k$ and $2k + 1$, so that the reverse of $e$ is $e \oplus 1$. The forward star of the doubled arc set then serves as the residual graph, and no reverse star is needed.
- **Linked forward star.** A dynamic form, common in programming contests, keeps the arcs in an array in insertion order with two extra arrays: $\mathit{first}[i]$, the name of the last arc added out of $i$, and $\mathit{next}[e]$, the name of the previous arc out of the same tail. This is an [adjacency list](/adjacency-list/) of linked lists stored in arrays. It adds an arc in $O(1)$ time and lists out-arcs in $\Theta(d^+(i))$ time, but the arcs of a vertex are no longer consecutive in memory.
- **[Compressed sparse row](/compressed-sparse-row/).** The same layout with only the head of each arc stored in the main array and the data in parallel arrays. [Compressed sparse column](/compressed-sparse-column/) is the reverse star with heads replaced by tails.
- **[Incidence list](/incidence-list/).** A list of arc names per vertex, in any order, over an [edge list](/edge-list/); the forward and reverse stars are its static, packed form.

## When to use it

Use the forward star for static networks with data on the arcs, when algorithms need both the out-arcs and the in-arcs of each vertex and must update the data of an arc from either side: maximum flow, minimum cost flow, the network simplex method and shortest paths with arc costs. Use plain [CSR](/compressed-sparse-row/) when the arcs carry no data that changes. Use an [adjacency list](/adjacency-list/), or the linked forward star, when arcs are added during the algorithm.

## Pitfalls

- **Arc names change on a rebuild.** A name is an index in the sorted array. After a rebuild, saved names point to other arcs. Keep a map from the input order to the names if the caller needs it.
- **Unstable sorting.** If line L1 uses an unstable sort, parallel arcs from the same tail may swap names between runs, which makes results hard to reproduce. Use a counting sort, which is stable.
- **Data copied into the reverse star.** Copying the cost or the flow into a separate in-arc array, in place of storing names in $\mathit{trace}$, means that an update through one star is not seen through the other.
- **The last offset.** Both $\mathit{point}$ and $\mathit{rpoint}$ have $n + 1$ entries, and $\mathit{point}[n] = m$. Some texts use the convention $\mathit{point}[n+1] = m + 1$ with 1-based names; mixing the two conventions reads one arc too many or too few.

## Implementations

The Python class `ForwardStar` takes $n$ and a list of arcs $(t, h, \mathit{cost})$, and keeps the arrays `tail`, `head`, `cost`, `point`, `rpoint` and `trace` as Python lists, plus a list `flow` of current flows indexed by arc name. It follows the main block line by line, and `check_invariant` tests (F1) and (F2).

## History

The forward and reverse star representations come from the network optimization literature, where codes for network flow problems stored arcs sorted by tail with a pointer array. Ahuja, Magnanti and Orlin (Section 2.3) present the forward star, the reverse star and the trace array in the form used here. Mehlhorn and Sanders (Section 8.2) give the same layout under the name adjacency array.

## References
