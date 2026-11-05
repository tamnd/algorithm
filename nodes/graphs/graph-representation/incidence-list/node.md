---
tag: QV04NF
kind: data-structure
slug: incidence-list
name: Incidence list
aliases:
- edge incidence list
area: graphs/graph-representation
level: core
summary: Per-vertex list of the edges incident to it, rather than of neighbours.
implements: [graph]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, d: the largest degree of a vertex named in the call}
  time: {amortized: O(1 + d)}
  space: {extra: Θ(n + m)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [graph, edge, adjacency-list, degree]
see_also: [adjacency-list, edge-list, incidence-matrix, multigraph, forward-star, hash-based-adjacency, handshake-lemma]
sources:
  - book: isbn:9783540779773
    title: Kurt Mehlhorn and Peter Sanders, Algorithms and Data Structures, The Basic Toolbox, Springer, 2008
    locator: Chapter 8 (Graph Representation), Sections 8.1 (unordered edge sequences) and 8.3 (adjacency lists, dynamic graphs, with edge objects in the lists of both ends)
  - book: isbn:9781118290279
    title: Michael T. Goodrich, Roberto Tamassia and Michael H. Goldwasser, Data Structures and Algorithms in Python, Wiley, 2013
    locator: Chapter 14, Section 14.2 (Data structures for graphs), the edge list structure and the adjacency list structure with an incidence collection for each vertex
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1 (Representations of graphs), and Appendix B.4 for the terms incident, degree and self-loop
---

An incidence list stores a [graph](/graph/) as a table of [edges](/edge/), each with its two ends and its data, together with one list for each [vertex](/vertex/) that holds the names of the edges at that vertex. It differs from the [adjacency list](/adjacency-list/), whose lists hold neighbour vertices, in that each edge has one record and an identity of its own. So it stores a [multigraph](/multigraph/) with parallel edges and [self-loops](/self-loop/) without change, keeps a weight or other data once for each edge, and removes a given edge in $O(1)$ time. The space is $\Theta(n + m)$ for $n$ vertices and $m$ edges.

## In plain words

Number all the roads of a map: road 0, road 1, road 2, and so on. Keep one table that says, for each road number, which two towns it joins and how long it is. Then, for each town, keep a short list of the numbers of the roads that touch that town.

To find the roads out of a town, read its list and look each number up in the table. To close road 5, you know at once which two towns it touches, so you only fix those two lists. Two roads between the same two towns are no problem: they have different numbers. A ring road that leaves a town and comes back to it is no problem either.

## The abstract type

The incidence list implements the [graph](/graph/) type, and it adds edge names. An edge is a value $e$ with a tail $t(e)$ and a head $h(e)$, so the graph is a multigraph $G = (V, E, t, h)$ in which two edges may have the same ends. For a [directed graph](/directed-graph/), $e$ goes from $t(e)$ to $h(e)$. For an [undirected graph](/undirected-graph/), the order of $t(e)$ and $h(e)$ only records how the edge was given, and $e$ joins the two ends. The edge $e$ is *incident* to the vertex $v$ when $v \in \{t(e), h(e)\}$.

The operations are:

- `add-vertex(G) → v`, a new vertex with no edges.
- `add-edge(G, u, v, w) → e`, a new edge from $u$ to $v$ with the data $w$. It returns the name $e$, and it never merges $e$ with an edge that is already there.
- `remove-edge(G, e)`, for an edge name $e$.
- `incident(G, v)`, the edges at $v$, each as a pair (edge, other end). In a directed graph this lists the edges that leave $v$, and `in-incident(G, v)` lists the edges that enter $v$.
- `find-edge(G, u, v)`, the name of some edge from $u$ to $v$, or NIL. This is the [adjacency query](/adjacency-query/).
- `ends(G, e)` and `data(G, e)`, the two ends and the data of $e$.

## Representation

The structure has an edge table of four arrays indexed by the edge name $e \in \{0, 1, 2, \ldots\}$: $tail[e]$, $head[e]$, $data[e]$ and $alive[e]$. Each vertex $v$ has two arrays: $out[v]$, the names of the edges with tail $v$, and $in[v]$, the names of the edges with head $v$. Two more arrays $pos_{out}[e]$ and $pos_{in}[e]$ give the index of $e$ in $out[tail[e]]$ and in $in[head[e]]$.

**Invariant.** For each edge name $e$ with $alive[e]$:

- **(I1)** $e$ occurs exactly once in $out[tail[e]]$, at index $pos_{out}[e]$, and in no other $out$ list.
- **(I2)** $e$ occurs exactly once in $in[head[e]]$, at index $pos_{in}[e]$, and in no other $in$ list.
- **(I3)** No list holds a name $e$ with $alive[e]$ false.

So each edge has two *slots*, one at each end. A self-loop $e$ with $t(e) = h(e) = v$ has both slots at $v$, one in $out[v]$ and one in $in[v]$. In an undirected graph, the edges at $v$ are the edges of $out[v]$ followed by the edges of $in[v]$, and the degree is $d(v) = |out[v]| + |in[v]|$. This counts a self-loop twice, which is the convention of the [handshake lemma](/handshake-lemma/): the degrees sum to $2m$, because each edge has exactly two slots. In a directed graph, $|out[v]|$ is the out-degree and $|in[v]|$ the in-degree of $v$.

## Operations

```pseudo id=main
ADD-EDGE(G, u, v, w)
L1  e ← |tail|; append u to tail, v to head, w to data, true to alive
L2  append e to out[u]; pos_out[e] ← |out[u]| − 1
L3  append e to in[v]; pos_in[e] ← |in[v]| − 1
L4  return e

INCIDENT(G, v)                        ▷ undirected; a directed graph uses only line L5
L5  for each e in out[v] do report (e, head[e])
L6  for each e in in[v] do report (e, tail[e])

REMOVE-EDGE(G, e)                     ▷ alive[e] is true
L7  u ← tail[e]; v ← head[e]
L8  SWAP-REMOVE(out[u], pos_out, e)
L9  SWAP-REMOVE(in[v], pos_in, e)
L10 alive[e] ← false

SWAP-REMOVE(L, pos, e)
L11 i ← pos[e]; f ← the last name of L
L12 L[i] ← f; pos[f] ← i
L13 delete the last cell of L
```

**Add.** Line L1 gives the new edge the next free name and records its ends and data. Lines L2 and L3 put one slot in each end list and record where it is. A [dynamic array](/dynamic-array/) makes each append $O(1)$ amortized.

**Incident.** Lines L5 and L6 read the two lists of $v$ and report, for each slot, the other end of its edge. A self-loop at $v$ is reported twice in an undirected graph, once from each slot, so the number of reports is $d(v)$.

**Remove.** Line L7 reads the ends from the edge table, so there is no search. SWAP-REMOVE moves the last name of the list into the slot of $e$, fixes the position of the moved name, and shortens the list by one. The order of a list changes, which the graph type allows.

**Find.** In a directed graph, `find-edge(G, u, v)` scans the shorter of $out[u]$ and $in[v]$, for a name with the right other end. In an undirected graph it scans the edges of the end with the smaller degree. The time is $O(1 + \min(d(u), d(v)))$, or $O(1 + \min(d^+(u), d^-(v)))$ in a directed graph.

## Example

Take the undirected multigraph on the vertices $0, 1, 2, 3$ with the six edges $e_0 = 01$, $e_1 = 12$, $e_2 = 02$, $e_3 = 12$, $e_4 = 23$ and $e_5 = 33$, added in this order. The edges $e_1$ and $e_3$ are parallel, and $e_5$ is a self-loop. After the six calls of ADD-EDGE, the lists are:

| vertex | out | in | edges at the vertex | degree |
|---|---|---|---|---|
| 0 | $[0, 2]$ | $[\,]$ | $e_0, e_2$ | 2 |
| 1 | $[1, 3]$ | $[0]$ | $e_1, e_3, e_0$ | 3 |
| 2 | $[4]$ | $[1, 2, 3]$ | $e_4, e_1, e_2, e_3$ | 4 |
| 3 | $[5]$ | $[4, 5]$ | $e_5, e_4, e_5$ | 3 |

The degrees sum to $12 = 2 \cdot 6$. Now call REMOVE-EDGE$(G, e_1)$. Line L7 reads $u = 1$ and $v = 2$. In $out[1] = [1, 3]$, the slot of $e_1$ is index 0, and the last name is 3, so $out[1]$ becomes $[3]$ and $pos_{out}[3] = 0$. In $in[2] = [1, 2, 3]$, the slot of $e_1$ is index 0 and the last name is 3, so $in[2]$ becomes $[3, 2]$ and $pos_{in}[3] = 0$. No other list changes. The parallel edge $e_3$ is still there, and `find-edge`$(G, 2, 1)$ returns $e_3$.

## Correctness

Each operation keeps (I1) to (I3). ADD-EDGE appends $e$ to $out[u]$ and $in[v]$ only and records its index, so (I1) and (I2) hold for $e$, and the other edges are not moved. SWAP-REMOVE keeps the slot of every name other than $e$, except the last name $f$, whose new index it records, and it removes the only occurrence of $e$ in that list. So after REMOVE-EDGE, $e$ is in no list, and the positions of all other live edges are right. INCIDENT then reports each slot at $v$ exactly once, and by (I1) and (I2) these are exactly the slots of the edges incident to $v$. The full proof is in `proofs/correctness.md`.

## Complexity

The model is the [word RAM](/word-ram/), with the edge names and vertex names as words. The times are worst case except where marked.

| operation | time | notes |
|---|---|---|
| add-vertex | $O(1)$ amortized | two empty lists |
| add-edge | $O(1)$ amortized | three appends to dynamic arrays |
| remove-edge$(e)$ | $O(1)$ | two swap-removes; $O(1)$ amortized if the arrays also shrink |
| incident$(v)$ | $\Theta(1 + d(v))$ | output size |
| find-edge$(u, v)$ | $O(1 + \min(d(u), d(v)))$ | scan of the shorter list |
| ends$(e)$, data$(e)$ | $O(1)$ | edge table |
| remove-vertex$(v)$ | $O(1 + d(v))$ | remove each incident edge, then mark $v$ |
| space | $\Theta(n + m)$ | $n$ pairs of lists, $2m$ slots, $m$ table rows |

The space counts the names of the removed edges too, because the table keeps their rows so that the names stay valid. If there are many removals, a rebuild that renames the live edges brings the space back to $\Theta(n + m)$ in $O(n + m)$ time.

## Variants

- **Doubly linked incidence lists.** Mehlhorn and Sanders store each edge as an object with links into the lists of both ends. A removal unlinks the edge in $O(1)$ worst-case time, and the order of the other edges does not change.
- **One list for each undirected vertex.** Keep only one list $inc[v]$ and store both slots of a non-loop edge there; the slots of $e$ at $u$ and at $v$ are then two cells of different lists. This is the "incidence collection" of Goodrich, Tamassia and Goldwasser.
- **Static form.** Sort the slots by vertex and pack them into one array with an offset for each vertex. This is the [compressed sparse row](/compressed-sparse-row/) form of the incidence list, also called the [forward star](/forward-star/) when the slots hold edge names.
- **Paired half-edges.** Give the two slots of an edge the names $2e$ and $2e + 1$, so that the twin of a slot $s$ is $s \oplus 1$. Flow and planar-graph codes use this layout: the [residual graph](/residual-graph/) stores an edge and its reverse this way, and the [doubly connected edge list](/doubly-connected-edge-list/) is a richer form of it.

## When to use it

Use an incidence list when edges are objects in their own right: when the graph has parallel edges, when each edge has a weight, a capacity or a flow that must change in one place, or when an algorithm removes or marks given edges. Examples are Hierholzer's walk for an [Eulerian circuit](/eulerian-circuit/), which must use each edge once even when there are parallel edges, and [max-flow](/max-flow-problem/) codes. Use a plain [adjacency list](/adjacency-list/) when the graph is simple and the edges carry no data, because one fewer indirection is faster. Use an [adjacency matrix](/adjacency-matrix/) when the graph is dense and the main query is `find-edge`.

## Pitfalls

- **Searching to remove.** If REMOVE-EDGE searches $out[u]$ for $e$ instead of reading $pos_{out}[e]$ in line L11, a removal costs $\Theta(d(u) + d(v))$. Keep the positions, or use linked lists.
- **Forgetting the moved name.** Line L12 must set $pos[f] \leftarrow i$. Without it, the next removal of $f$ deletes the wrong slot.
- **Self-loops counted once.** A self-loop has two slots at the same vertex, so it adds 2 to the degree. Code that filters out "the edge already seen" in line L6 gets degrees that do not sum to $2m$.
- **Reusing a name.** Reusing the name of a removed edge at once breaks the outside code that still holds the old name. Recycle names only when no caller can hold them.

## Implementations

The Python class keeps the edge table and the two lists of each vertex in Python lists, uses swap-remove for removals, and keeps the names of removed edges dead so that the names stay valid.

## History

Mehlhorn and Sanders, in Chapter 8, separate the representations of a graph by the operations they support, and they describe the dynamic form in which each edge object sits in the incidence lists of both its ends. Goodrich, Tamassia and Goldwasser describe the same structure, with an incidence collection for each vertex and a list of edge objects, in Section 14.2.

## References
