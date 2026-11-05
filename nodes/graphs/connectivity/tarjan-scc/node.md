---
tag: JH9ZVM
kind: algorithm
slug: tarjan-scc
name: Tarjan's strongly connected components algorithm
aliases:
- Tarjan's SCC algorithm
area: graphs/connectivity
level: core
summary: A single DFS with a stack and low-link values finds all SCCs in linear time.
solves: [strongly-connected-components]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true}
history:
  year: 1972
  people: [Robert E. Tarjan]
  note: Published in the paper that introduced linear-time depth-first search algorithms for biconnectivity and strong connectivity.
prereqs: [strongly-connected-components, depth-first-search, low-link, discovery-and-finish-times, white-path-theorem]
see_also: [kosaraju-sharir, gabow-path-based-scc, condensation-graph, 2-sat, hopcroft-tarjan-biconnectivity, parenthesis-theorem, topological-sort]
sources:
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: the section on strongly connected components (the LOWLINK values, the stack of points, and the proof that the algorithm is correct and linear)
  - paper: doi:10.1016/0020-0190(94)90047-7
    title: Esko Nuutila and Eljas Soisalon-Soininen, On finding the strongly connected components in a directed graph, Information Processing Letters 49(1), 9 to 14 (1994)
    locator: the whole paper (the improvement that keeps components of one vertex off the stack)
  - paper: doi:10.1016/j.ipl.2015.08.010
    title: David J. Pearce, A space-efficient algorithm for finding strongly connected components, Information Processing Letters 116(1), 47 to 52 (2016)
    locator: the whole paper (the space bounds v(2 + 5w), v(1 + 4w) and v(1 + 3w) bits, and the merged rindex array)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms (2019)
    locator: Chapter 6, Depth-First Search (the section on strong components in linear time)
---

Tarjan's algorithm finds the [strongly connected components](/strongly-connected-components/) of a [directed graph](/directed-graph/) with one [depth-first search](/depth-first-search/). It numbers the vertices in the order they are discovered, keeps the visited vertices of unfinished components on a stack, and computes a [low-link value](/low-link/) for each vertex. A vertex whose low-link equals its own number is the first vertex of its component, and when it finishes, the stack above it is exactly that component. It runs in $\Theta(n + m)$ time, needs no [transpose](/graph-transpose/), and outputs the components in reverse [topological order](/topological-ordering/) of the [condensation](/condensation-graph/).

## In plain words

Walk through a maze of one-way corridors with a depth-first search. Number each room as you first enter it, and drop a token in it. The tokens form a pile, in the order you entered the rooms.

When you are in a room, note the smallest number you can get back to by walking deeper and then taking one corridor to a room whose token is still on the pile. If, when you are done with a room, the best you can get back to is the room itself, then nothing below it leads back above it. That room and every room whose token lies on top of its token form one group of rooms that all reach each other. Pick up those tokens, report the group, and go on. Every group is found this way, the deepest groups first.

## The problem

The input is a directed graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$ and adjacency lists $\mathrm{Adj}[u]$. Parallel arcs and [self-loops](/self-loop/) are allowed: a loop $(v, v)$ is scanned when $v$ is on the stack and does not change $\mathrm{low}[v]$, and a repeated arc is scanned twice, which changes nothing. The output is a label $comp[v]$ for each vertex such that $comp[u] = comp[v]$ exactly when $u$ and $v$ reach each other. An undirected graph, given with both arcs of each edge, has its [connected components](/connected-components/) as its strong components, and the algorithm finds them.

## The algorithm

```pseudo id=main
TARJAN-SCC(G)
L1  for each vertex v do index[v] ← NIL; onstack[v] ← false; S ← empty stack; i ← 0; k ← 0
L2  for each vertex u do
L3      if index[u] = NIL then STRONGCONNECT(u)
L4  return comp

STRONGCONNECT(v)
L5  i ← i + 1; index[v] ← i; low[v] ← i
L6  push v on S; onstack[v] ← true
L7  for each w ∈ Adj[v] do
L8      if index[w] = NIL then                        ▷ tree arc
L9          STRONGCONNECT(w); low[v] ← min(low[v], low[w])
L10     else if onstack[w] then low[v] ← min(low[v], index[w])
L11 if low[v] = index[v] then                         ▷ v is the root of a component
L12     repeat
L13         pop w from S; onstack[w] ← false; comp[w] ← k
        until w = v
L14     k ← k + 1
```

The number $index[v]$ is the preorder number of $v$: $index[v] = j$ when $v$ is the $j$-th vertex discovered. It has the same order as the discovery time $d[v]$ of the [DFS page](/depth-first-search/). Line L10 treats every arc to an already discovered vertex the same way, whether it is a back arc, a forward arc or a cross arc: it counts only if the target is still on the stack $S$. The components get the labels $0, 1, 2, \ldots$ in the order their roots finish. The Python implementation replaces the recursion of line L9 by a stack of frames $(v, i)$, where $i$ is the next position in $\mathrm{Adj}[v]$, and starts the numbers at 0.

## Example

Take the graph of the [depth-first search](/depth-first-search/) page: vertices 0 to 6 and the lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none; $5: 4, 6$; $6: 5$.

| step | event | low change | stack $S$ after | output |
|---|---|---|---|---|
| 1 | enter 0, 1, 2 with $index = 1, 2, 3$ | | 0 1 2 | |
| 2 | arc $2 \to 0$, 0 on $S$ | $\mathrm{low}[2] = 1$ | 0 1 2 | |
| 3 | 2 finishes, $1 \ne 3$; back in 1 | $\mathrm{low}[1] = 1$ | 0 1 2 | |
| 4 | 1 finishes, $1 \ne 2$; back in 0, arc $0 \to 3$, enter 3 with $index = 4$ | | 0 1 2 3 | |
| 5 | arc $3 \to 2$, 2 on $S$ (a cross arc) | $\mathrm{low}[3] = 3$ | 0 1 2 3 | |
| 6 | arc $3 \to 4$, enter 4 with $index = 5$; 4 has no arcs and finishes with $\mathrm{low}[4] = 5 = index[4]$ | | 0 1 2 3 | $comp = 0$: $\{4\}$ |
| 7 | 3 finishes, $3 \ne 4$; back in 0, arc $0 \to 2$, 2 on $S$ | none | 0 1 2 3 | |
| 8 | 0 finishes with $\mathrm{low}[0] = 1 = index[0]$ | | empty | $comp = 1$: $\{3, 2, 1, 0\}$ |
| 9 | line L2 reaches 5, enter 5 with $index = 6$; arc $5 \to 4$, 4 not on $S$, skipped | | 5 | |
| 10 | arc $5 \to 6$, enter 6 with $index = 7$; arc $6 \to 5$ | $\mathrm{low}[6] = 6$ | 5 6 | |
| 11 | 6 finishes, $6 \ne 7$; back in 5; 5 finishes with $\mathrm{low}[5] = 6$ | | empty | $comp = 2$: $\{6, 5\}$ |

The final values are $index = 1, 2, 3, 4, 5, 6, 7$ and $\mathrm{low} = 1, 1, 1, 3, 5, 6, 6$, and the labels are $comp = 1, 1, 1, 1, 0, 2, 2$. The order of output, $\{4\}$, $\{0, 1, 2, 3\}$, $\{5, 6\}$, is the reverse of the topological order $\{5, 6\}, \{0, 1, 2, 3\}, \{4\}$ of the condensation. Step 5 shows why cross arcs count when their target is on the stack: vertex 2 is finished, but its component is not, and 3 belongs to it. Step 9 shows why they do not count otherwise: 4 is in a component that is already output.

## Correctness

Let the *root* of a component $C$ be the vertex of $C$ discovered first. By the [white-path theorem](/white-path-theorem/), all of $C$ lies in the DFS subtree of its root, and the tree path from the root to any vertex of $C$ stays in $C$. The proof is an induction on the order in which the calls of STRONGCONNECT finish, with the hypothesis that every earlier root popped exactly its component. That hypothesis says that a discovered vertex is on the stack exactly when the root of its component has not finished. With it, two facts hold when $v$ finishes:

- If $v$ is not a root, a path from $v$ back to its root leaves the subtree of $v$ by an arc to a vertex that is discovered earlier and still on the stack, so $\mathrm{low}[v] < index[v]$.
- Every value that enters $\mathrm{low}[x]$ is at least the number of the root of the component of $x$. So for a root, $\mathrm{low}[v] = index[v]$.

So line L11 fires exactly at roots. At that moment the vertices above $v$ on the stack are the descendants of $v$ whose roots have not finished, and these are exactly the component of $v$. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **Time.** STRONGCONNECT is called exactly once for each vertex, because it is called only when $index = $ NIL and line L5 sets the index at once. Each call scans its list once, and lines L8 to L10 do $O(1)$ work for each arc, so the scans cost $\Theta(n + m)$ in total. Each vertex is pushed once in line L6 and popped once in line L13. The total is $\Theta(n + m)$ in the best and in the worst case.
- **Space.** The arrays $index$, $\mathrm{low}$, $onstack$ and $comp$, the stack $S$ and the recursion stack each take $O(n)$ words, so the extra space is $\Theta(n)$. Pearce counts it in bits: $n(2 + 5w)$ bits for Tarjan's version with $w$-bit words, $n(1 + 4w)$ for the version of Nuutila and Soisalon-Soininen, and $n(1 + 3w)$ for his own.
- **Optimality.** Every algorithm for the problem needs $\Omega(n + m)$ time on adjacency lists (see [strongly connected components](/strongly-connected-components/)).

## Properties

- **One pass, outgoing lists only.** It reads each list once and never needs incoming arcs. This is its main advantage over [Kosaraju-Sharir](/kosaraju-sharir/).
- **Reverse topological output.** For each arc $(u, v)$, $comp[u] \ge comp[v]$: a component is output only after every component it has an arc into. The labels can be read as "sink components first".
- **Online output.** A component is output as soon as its root finishes, before the search has seen the rest of the graph. This makes it fit for searches that build the graph as they go, such as state-space search in model checking.
- **Same search as plain DFS.** The vertices are discovered in the same order as a plain DFS with the same lists, so $index$ is the preorder of that DFS.
- **Deterministic.** The labels depend on the order of the vertices and of the lists, but the partition does not.

## Variants and improvements

- **Low-link through $\mathrm{low}[w]$.** Many programs write $\mathrm{low}[v] \leftarrow \min(\mathrm{low}[v], \mathrm{low}[w])$ in line L10 too. The values change, but the test of line L11 still fires exactly at the roots, because $\mathrm{low}[w] \le index[w]$ and $\mathrm{low}[w]$ is still at least the number of the root of the component of $w$, which is the component of $v$ or a component whose root is a proper descendant of $v$. In the undirected tests of [low-link values](/low-link/) this change is wrong.
- **Nuutila and Soisalon-Soininen.** A vertex is pushed only when it is known not to be a component by itself, which saves stack work on graphs with many trivial components, and the flag $onstack$ is folded into the other arrays.
- **Pearce.** One array $rindex$ holds both the index and the low-link, and finished vertices get their component number in the same array, which gives $n(1 + 3w)$ bits.
- **Path-based search.** [Gabow's algorithm](/gabow-path-based-scc/) and the algorithm of Cheriyan and Mehlhorn replace the low-link values by a second stack of candidate roots. They have the same time bound and a simpler test.
- **Biconnectivity.** The same scheme, with a stack of edges and the low point of an undirected DFS, gives the [Hopcroft-Tarjan](/hopcroft-tarjan-biconnectivity/) algorithm for [biconnected components](/biconnected-components/).
- **2-SAT.** On the [implication graph](/implication-graph/) of a [2-SAT](/2-sat/) formula, the formula is satisfiable exactly when no variable shares a component with its negation, and then setting $x$ true exactly when $comp[x] < comp[\lnot x]$ satisfies it. The reverse topological labels of this algorithm give the assignment with no extra sort.

## When to use it

Use Tarjan's algorithm as the default for strongly connected components: it is one pass, needs only outgoing lists and $\Theta(n)$ extra words, and gives the components in a useful order. Use it when the graph is generated on the fly or is too large to transpose. Prefer [Kosaraju-Sharir](/kosaraju-sharir/) when the code must be very easy to check, or when incoming lists are already stored. For a single question, "is the graph strongly connected", two searches from one vertex are enough (see [strongly connected graph](/strongly-connected-graph/)). For graphs with billions of arcs on many processors, use parallel methods such as [forward-backward search](/forward-backward-scc/), since depth-first search is hard to parallelize.

## Pitfalls

- **Ignoring the stack test.** Line L10 must check $onstack[w]$, not just $index[w] \ne$ NIL. Without the test, in the example the arc $5 \to 4$ gives $\mathrm{low}[5] = 5 < 6$, and the vertices 5 and 6 are never popped as a component.
- **Using finished instead of on stack.** "On the stack" is not "not finished". In the example vertex 2 is finished at step 5 and must still count for the arc $3 \to 2$, else 3 is output as a component by itself.
- **Updating the parent before the child is done.** The update $\mathrm{low}[v] \leftarrow \min(\mathrm{low}[v], \mathrm{low}[w])$ of line L9 must use the final value of $\mathrm{low}[w]$. In an iterative version, do it when the frame of $w$ is popped, as the implementation does, not when $w$ is pushed.
- **Recursion depth.** The recursion is as deep as the longest DFS path, which can be $n$. On a path of $20000$ vertices a recursive Python version fails with the default limit. Use an explicit stack.
- **Expecting topological order.** The labels are in reverse topological order. Code that needs sources first must reverse them, with $k - 1 - comp[v]$.

## Implementations

## History

Robert Tarjan gave the algorithm in 1972, in the paper that showed how depth-first search yields linear-time algorithms for biconnected components and for strongly connected components. Nuutila and Soisalon-Soininen improved its stack use and space in 1994, and Pearce reduced the space further in 2016. Pearce's paper notes that his version is used in the SciPy library.

## References
