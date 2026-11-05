---
tag: TA3TXZ
kind: algorithm
slug: kosaraju-sharir
name: Kosaraju-Sharir algorithm
aliases:
- Kosaraju's algorithm
- Sharir's algorithm
area: graphs/connectivity
level: intro
summary: Two DFS passes, one on the graph and one on its transpose in reverse finishing order, find all SCCs.
solves: [strongly-connected-components]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: true}
history:
  year: 1978
  people: [S. Rao Kosaraju, Micha Sharir]
  note: Kosaraju found the method in 1978 and did not publish it. Sharir found it on his own and published it in 1981.
prereqs: [strongly-connected-components, depth-first-search, discovery-and-finish-times, white-path-theorem, graph-transpose]
see_also: [tarjan-scc, gabow-path-based-scc, condensation-graph, strongly-connected-graph, topological-sort, parenthesis-theorem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.5, Strongly connected components (the procedure STRONGLY-CONNECTED-COMPONENTS, its lemmas on finish times of components, and its correctness theorem)
  - paper: doi:10.1016/0898-1221(81)90008-0
    title: Micha Sharir, A strong-connectivity algorithm and its applications in data flow analysis, Computers and Mathematics with Applications 7(1), 67 to 72 (1981)
    locator: the whole paper
  - book: isbn:9780201000238
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, Data Structures and Algorithms, Addison-Wesley (1983)
    locator: Chapter 6, Directed graphs (the section on strong components, where the method is credited to Kosaraju)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.2, Directed graphs (strong connectivity and the Kosaraju-Sharir algorithm, KosarajuSharirSCC)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 3.4, Strongly connected components (the version that searches the reverse graph first to find a sink component)
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: the section on strongly connected components (the earlier one-pass algorithm)
---

The Kosaraju-Sharir algorithm finds the [strongly connected components](/strongly-connected-components/) of a [directed graph](/directed-graph/) with two passes of [depth-first search](/depth-first-search/). The first pass runs DFS on the graph and records the [finish times](/discovery-and-finish-times/). The second pass runs DFS on the [transpose graph](/graph-transpose/), and it takes the roots in decreasing order of finish time; each tree of the second pass is exactly one component. It runs in $\Theta(n + m)$ time, and it gives the components in a [topological order](/topological-ordering/) of the [condensation](/condensation-graph/).

## In plain words

Think of a city with one-way streets. Drive around once with a depth-first search, and note the moment you leave each crossing for good. The crossing you leave last belongs to a group that no street from another group enters: it sits at the top of the map of groups.

Now turn every street around and start a new search at that last crossing. With the streets reversed, you can only reach crossings that could drive to it in the real city. From the top group, the only such crossings are in its own group. So the search collects exactly one group. Mark it, start again at the unmarked crossing that was left latest, and repeat. Each new search collects exactly one more group.

## The problem

The input is a directed graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$ and adjacency lists $\mathrm{Adj}[u]$. Parallel arcs and [self-loops](/self-loop/) are allowed: a loop $(u, u)$ stays a loop in the transpose, and a repeated arc is scanned twice, which changes nothing. The output is a label $comp[v]$ for each vertex such that $comp[u] = comp[v]$ exactly when $u$ and $v$ reach each other. This is the [strongly connected components](/strongly-connected-components/) problem. An undirected graph, given with both arcs of each edge, is its own transpose, and the algorithm then finds its [connected components](/connected-components/).

## The algorithm

```pseudo id=main
KOSARAJU-SHARIR(G)
L1  run DFS(G); list the vertices in the order they finish, as L
L2  build the transpose Gᵀ, with v ∈ Adjᵀ[u] for each arc (v, u) of G
L3  for each vertex v do comp[v] ← NIL; k ← 0
L4  for each u in L, from the last to finish to the first do
L5      if comp[u] = NIL then
L6          k ← k + 1
L7          ASSIGN(Gᵀ, u, k)
L8  return comp

ASSIGN(H, u, k)                            ▷ DFS in H over unlabelled vertices
L9  comp[u] ← k
L10 for each v ∈ H.Adj[u] do
L11     if comp[v] = NIL then ASSIGN(H, v, k)
```

Line L1 is a full [depth-first search](/depth-first-search/) of $G$, with all the roots of its line L3. A vertex is appended to $L$ when it turns black. Line L2 scans each list of $G$ one time and appends $u$ to $\mathrm{Adj}^{\mathsf T}[v]$ for each arc $(u, v)$. The loop of line L4 runs through $L$ backwards, so it meets the vertices in decreasing order of finish time. Each vertex that is still without a label starts a new search in $G^{\mathsf T}$, which labels every vertex it can reach through unlabelled vertices.

The order of the second pass does not matter inside ASSIGN: any search over the unlabelled vertices, such as a stack or a queue, labels the same set. Only the order of the roots in line L4 matters.

## Example

Take the graph of the [depth-first search](/depth-first-search/) page: vertices 0 to 6 and the lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none; $5: 4, 6$; $6: 5$.

**First pass.** The DFS of that page gives these times.

| vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $d$ | 1 | 2 | 3 | 6 | 7 | 11 | 12 |
| $f$ | 10 | 5 | 4 | 9 | 8 | 14 | 13 |

So $L = 2, 1, 4, 3, 0, 6, 5$, and line L4 meets the vertices in the order $5, 6, 0, 3, 4, 1, 2$.

**Transpose.** Line L2, with $u$ in increasing order, gives $\mathrm{Adj}^{\mathsf T}$: $0: 2$; $1: 0$; $2: 0, 1, 3$; $3: 0$; $4: 3, 5$; $5: 6$; $6: 5$.

**Second pass.**

| step of line L4 | $u$ | action | vertices labelled | component |
|---|---|---|---|---|
| 1 | 5 | $k = 1$, ASSIGN from 5 | 5, 6 | $\{5, 6\}$ |
| 2 | 6 | already labelled | | |
| 3 | 0 | $k = 2$, ASSIGN from 0 | 0, 2, 1, 3 | $\{0, 1, 2, 3\}$ |
| 4 | 3 | already labelled | | |
| 5 | 4 | $k = 3$, ASSIGN from 4 | 4 | $\{4\}$ |
| 6, 7 | 1, 2 | already labelled | | |

In step 5, the list $\mathrm{Adj}^{\mathsf T}[4] = 3, 5$ points into two components that already have labels, so the search stops at once. This is the heart of the method: the arcs that would lead a search out of a component in $G^{\mathsf T}$ lead to components that are already done. The labels $1, 2, 3$ follow the topological order $\{5, 6\}, \{0, 1, 2, 3\}, \{4\}$ of the condensation.

If line L4 used increasing finish time instead, the first search would start at 2 in $G^{\mathsf T}$ and label $\{0, 1, 2, 3\}$ correctly, but the next root, 4, would then label 4, 5 and 6 together, which is wrong.

## Correctness

For a component $C$, let $f(C) = \max_{v \in C} f[v]$ be its latest finish time in the first pass. The key lemma is:

> If $C \ne D$ are components and $G$ has an arc from $C$ to $D$, then $f(C) > f(D)$.

It follows from the [white-path theorem](/white-path-theorem/), with two cases on which of $C$ and $D$ the first pass enters first. In $G^{\mathsf T}$ the same arc goes from $D$ to $C$, so every arc of $G^{\mathsf T}$ that leaves a component points to a component with a larger value of $f$. Line L4 starts each search at the unlabelled vertex with the largest finish time, so its component $C$ has the largest $f$ among the components without labels. All components that the arcs of $G^{\mathsf T}$ lead to from $C$ are then already labelled, and by induction on the steps, ASSIGN labels exactly $C$. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **Time.** Line L1 is a DFS: $\Theta(n + m)$. Line L2 scans each of the $m$ list entries one time and does $O(1)$ work for each: $\Theta(n + m)$. Lines L3 to L8 call ASSIGN exactly one time for each vertex, because a call is made only on an unlabelled vertex and labels it at once. Each call scans its list of $G^{\mathsf T}$ one time, and these lists have $m$ entries in total. So the second pass is $\Theta(n + m)$, and so is the whole, in the best and in the worst case.
- **Space.** The transpose has $n$ lists with $m$ entries, so the extra space is $\Theta(n + m)$. If the input already stores the incoming lists, as many graph libraries do, the extra space is $\Theta(n)$ for $L$, $comp$ and the stacks.
- **Optimality.** Every algorithm for the problem needs $\Omega(n + m)$ time on adjacency lists (see [strongly connected components](/strongly-connected-components/)), so the algorithm is optimal up to a constant factor.

## Properties

- **Topological output.** The components get the labels $1, 2, \ldots$ in a topological order of the condensation: for each arc $(u, v)$ of $G$, $comp[u] \le comp[v]$. This follows from the key lemma and the order of line L4.
- **Two passes, two graphs.** It reads the graph two times and needs the transpose. [Tarjan's algorithm](/tarjan-scc/) and [Gabow's algorithm](/gabow-path-based-scc/) need one pass and no transpose.
- **Any search in the second pass.** Only the first pass must be a depth-first search, because it supplies the finish times. The second pass can be a breadth-first search or any other search.
- **Deterministic.** The labels depend on the order of the vertices and of the lists, but the partition does not.

## Variants and improvements

- **Transpose first.** Run the first pass on $G^{\mathsf T}$ and the second pass on $G$. The first search of the second pass then starts in a sink component of $G$. This is the version of Dasgupta, Papadimitriou and Vazirani. The components come out in reverse topological order.
- **Reverse postorder.** The list $L$ read backwards is the reverse postorder of the first DFS. Sedgewick and Wayne compute it with a stack and then use the same code for the second pass. See [depth-first orders](/depth-first-orders/).
- **Implicit transpose.** If the graph is stored as an arc list or as an [adjacency matrix](/adjacency-matrix/), the transpose needs no copy: read the arcs backwards, or read the matrix by columns. With a matrix the time is $\Theta(n^2)$.
- **Condensation on the fly.** When ASSIGN meets an arc of $G^{\mathsf T}$ into an already labelled vertex $v$, the arc $(comp[v], k)$ is an arc of the condensation. Collect these to output the [condensation graph](/condensation-graph/) at no extra asymptotic cost.

## When to use it

Use Kosaraju-Sharir when the code must be short and easy to check: it is two ordinary searches, and the second can reuse any search routine. It is a good choice when the graph library already keeps incoming lists. Prefer [Tarjan's algorithm](/tarjan-scc/) or [Gabow's algorithm](/gabow-path-based-scc/) when the graph is large and memory is tight, or when only the outgoing lists are available, because they need one pass and no transpose. For a single question, "is the graph strongly connected", two searches from one vertex are enough (see [strongly connected graph](/strongly-connected-graph/)).

## Pitfalls

- **Wrong order in line L4.** The roots must come in decreasing finish time. Increasing finish time can merge components, as the example shows.
- **Second pass on $G$.** If line L7 searches $G$ instead of $G^{\mathsf T}$, the first search starts in a source component and labels everything reachable from it. The fix is to search the transpose, or to run the first pass on the transpose (the variant above).
- **Order from discovery times.** Decreasing discovery time is also wrong. In the example it takes the roots $6, 5, 4, \ldots$: the search from 6 labels $\{5, 6\}$, but the search from 4 then labels 4, 3, 0, 2 and 1 together. Only the latest finish time is sure to lie in a component that no other unlabelled component has an arc into.
- **Recursion depth.** Both passes recurse as deep as the longest DFS path, which can be $n$. Use explicit stacks, as the implementation does.
- **Forgotten roots in line L1.** The first pass must start a tree at every white vertex, as DFS$(G)$ does. A single search from vertex 0 gives no finish times to the vertices that 0 does not reach.

## Implementations

## History

S. Rao Kosaraju found the algorithm in 1978 and did not publish it. Aho, Hopcroft and Ullman gave it in their 1983 book and credited it to him. Micha Sharir found it on his own and published it in 1981, with applications to data flow analysis. Tarjan's one-pass algorithm of 1972 is older.

## References
