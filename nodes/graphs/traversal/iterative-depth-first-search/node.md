---
tag: FP6REQ
kind: algorithm
slug: iterative-depth-first-search
name: Nonrecursive depth-first search
aliases:
- iterative depth-first search
- stack-based DFS
area: graphs/traversal
level: intro
summary: Depth-first search implemented with an explicit stack of adjacency iterators instead of recursion, visiting vertices in the same order.
solves: [graph-reachability]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [depth-first-search, stack]
see_also: [discovery-and-finish-times, parenthesis-theorem, whatever-first-search, topological-sort, dfs-forest, edge-classification, flood-fill, tarjan-scc]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.3, Depth-first search (the recursive procedures DFS and DFS-VISIT with the colours and the timestamps d and f)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 22.3, Exercise 22.3-7 (rewrite the procedure DFS, using a stack to eliminate recursion)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 5 and Chapter 6, Depth-first search (the recursive DFS and its relation to a search with an explicit stack)
---

Nonrecursive depth-first search runs [depth-first search](/depth-first-search/) with an explicit [stack](/stack/) in place of the call stack. The stack holds the gray vertices, the ones whose calls would be active, and each vertex keeps a position in its adjacency list, which plays the part of the loop variable of its call. At each step, the vertex on top of the stack examines its next list entry, or, if its list is used up, it finishes and leaves the stack. The run then has exactly the same events in the same order as the recursive DFS: the same [discovery and finish times](/discovery-and-finish-times/), the same parents and the same [edge classification](/edge-classification/). It takes $\Theta(n + m)$ time and $\Theta(n)$ extra space, and it does not overflow the call stack on graphs with long paths.

## In plain words

Recursive depth-first search uses the computer's own stack of function calls to remember where to go back. On a graph with a path of a million vertices, that stack runs out of room.

The fix is to keep the stack yourself. Put the start vertex on it. Each vertex on the stack also remembers how far it has read in its own list of neighbours. Look at the top vertex. If it has a neighbour left to read, read it, and if that neighbour is new, put it on top. If its list is finished, take it off. This is the same walk as the recursive search, step by step, so it gives the same results, including the time when each vertex is left.

## The problem

The input is a directed or undirected graph $G = (V, E)$ given by adjacency lists. The output is what the full DFS of the [depth-first search](/depth-first-search/) page gives: the discovery time $d[u]$, the finish time $f[u]$ and the parent $\pi[u]$ of each vertex, for the roots tried in the order of $V$ and each list scanned in order. These determine the [depth-first forest](/dfs-forest/), the preorder and postorder, and the types of the edges, so they solve [graph reachability](/graph-reachability/) and are the input of [topological sort](/topological-sort/), cut vertices and strong components.

## The algorithm

```pseudo id=main
ITERATIVE-DFS(G)
L1  for each u ∈ V do color[u] ← WHITE, π[u] ← NIL, next[u] ← 1
L2  time ← 0, S ← empty stack
L3  for each u ∈ V do
L4      if color[u] = WHITE then
L5          color[u] ← GRAY, time ← time + 1, d[u] ← time, PUSH(S, u)
L6          while S is not empty do
L7              x ← TOP(S)
L8              if next[x] ≤ |Adj[x]| then
L9                  v ← Adj[x][next[x]], next[x] ← next[x] + 1
L10                 if color[v] = WHITE then
L11                     π[v] ← x, color[v] ← GRAY, time ← time + 1, d[v] ← time, PUSH(S, v)
L12             else POP(S), color[x] ← BLACK, time ← time + 1, f[x] ← time
L13 return d, f, π
```

Each iteration of the loop of line L6 does one of the two things that the recursive DFS-VISIT does between two other events: examine one list entry (lines L9 to L11), or end the call and set the finish time (line L12). Line L11 is the start of the call of $v$, and line L12 is its return.

## Example

Run it on the directed graph with vertices 0 to 6 and the lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none; $5: 4, 6$; $6: 5$. The stack is written bottom first.

| step | top $x$ | action | stack after |
|---|---|---|---|
| L5 | | discover 0, $d[0] = 1$ | 0 |
| 1 | 0 | read 1, white: discover 1, $d[1] = 2$ | 0, 1 |
| 2 | 1 | read 2, white: discover 2, $d[2] = 3$ | 0, 1, 2 |
| 3 | 2 | read 0, gray: nothing | 0, 1, 2 |
| 4 | 2 | list done: $f[2] = 4$ | 0, 1 |
| 5 | 1 | list done: $f[1] = 5$ | 0 |
| 6 | 0 | read 3, white: discover 3, $d[3] = 6$ | 0, 3 |
| 7 | 3 | read 2, black: nothing | 0, 3 |
| 8 | 3 | read 4, white: discover 4, $d[4] = 7$ | 0, 3, 4 |
| 9 | 4 | list done: $f[4] = 8$ | 0, 3 |
| 10 | 3 | list done: $f[3] = 9$ | 0 |
| 11 | 0 | read 2, black: nothing | 0 |
| 12 | 0 | list done: $f[0] = 10$ | empty |

Line L3 then reaches 5 and the same steps give $d[5] = 11$, $d[6] = 12$, $f[6] = 13$, $f[5] = 14$. So $d = (1, 2, 3, 6, 7, 11, 12)$ and $f = (10, 5, 4, 9, 8, 14, 13)$, the times of the recursive DFS on the [depth-first search](/depth-first-search/) page. At each step, the stack is the chain of active calls of the recursive run, and the gray vertices are exactly the stack.

**The usual shortcut is different.** Many programs push all neighbours of a vertex at once and mark a vertex when it is pushed. On the undirected triangle with the edges $\{0, 1\}$, $\{0, 2\}$, $\{1, 2\}$, this pushes 1 and 2 from 0 and marks both, so 2 gets the parent 0. The tree is the star with centre 0, and the edge $\{1, 2\}$ joins two vertices of which neither is an ancestor of the other. A real DFS tree of the triangle is a path, and this search is not depth-first. Marking a vertex when it is popped, with the neighbours pushed in reverse order, gives the DFS preorder and parents (see [whatever-first search](/whatever-first-search/)), but it pushes each edge and gives no finish times.

## Correctness

The proof compares the run with the recursive DFS on the same input. Cut the recursive run into steps: one step is one test of a list entry by the loop of a call (with the call it may start), or the end of a call. By induction on the number of steps, after the same number of steps both runs have the same colours, times, parents and clock, the stack $S$ lists the vertices with active calls from the oldest to the newest, and for each such $x$, the call of $x$ has tested exactly the first $\mathrm{next}[x] - 1$ entries of its list. The top of the stack is the vertex whose call runs, so lines L8 to L12 do what that call does next. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model.

- **Line L1 and the loop of line L3.** $\Theta(n)$.
- **Lines L9 to L11.** Each list entry is read one time, because $\mathrm{next}[x]$ only grows: $\Theta(m)$ in total for a directed graph, and $\Theta(2m)$ for an undirected graph.
- **Line L12.** Each vertex is pushed one time, when it turns gray, and popped one time: $\Theta(n)$.

So the time is $\Theta(n + m)$ on every input. The extra space is $\Theta(n)$: the arrays and a stack of at most $n$ vertices. The stack has one entry per active call, as the call stack of the recursive version would have, but each entry is one vertex instead of a call frame, and it lives in ordinary memory.

## Properties

- **Same output as the recursion.** The times, the parents, the forest and the edge types are those of the recursive DFS with the same orders.
- **Not recursive.** The depth of the search is limited only by memory. A path of $10^6$ vertices is no problem.
- **Deterministic.** The order of the roots and of the lists fixes the run.
- **Gray set is the stack.** At each moment, the gray vertices are the stack, and in order they form the tree path from the current root to the top.
- **Resumable.** The whole state of the search is in the arrays and the stack, so the search can stop after any step and continue later.

## Variants and improvements

- **Stack of iterators.** In languages with iterators, push the pair (vertex, iterator over its list) instead of keeping the array $\mathrm{next}$.
- **Postorder hooks.** Work that the recursive version does after the loop, such as appending to a postorder list for [topological sort](/topological-sort/) or computing a [low-link](/low-link/), goes at line L12. Work that it does after a child returns goes at line L12 too, applied to the new top of the stack.
- **Single source.** Without the loop of line L3, start with $S = (s)$: this visits the vertices reachable from $s$.
- **Mark on pop.** The simpler version that pushes every neighbour and marks a vertex when it is popped gives the same preorder and parents if the neighbours are pushed in reverse order. Its stack can hold $\Theta(m)$ entries, and it does not give finish times.
- **Tarjan's algorithms.** The strong components and biconnected components algorithms are often written in this form, with the extra stack of the algorithm next to the DFS stack.

## When to use it

Use it whenever the recursive depth of DFS can be large: on graphs with long paths, on grids, and in languages with a small default call stack, such as Python with its limit near 1000 calls. Use it also when the finish times matter, for example for [topological sort](/topological-sort/), [Kosaraju-Sharir](/kosaraju-sharir/) or [Tarjan's algorithm](/tarjan-scc/), where the shortcut that marks on push or on pop gives wrong answers. If only reachability or the set of reached vertices matters, any [whatever-first search](/whatever-first-search/) is enough.

## Pitfalls

- **Mark on push.** Marking a vertex when it is pushed, with all neighbours pushed at once, gives a search that is not depth-first: the parents and the edge types differ from DFS, as in the triangle example.
- **Finish too early.** A vertex must finish only when its list is used up, not when it is popped for the first time. With the iterator version, the vertex stays on the stack until then.
- **Lost position.** If the position $\mathrm{next}[x]$ is not stored, the vertex rescans its list from the start each time it is on top again, and the time becomes $\Theta(\sum_x \deg(x)^2)$ in the worst case.
- **Wrong top.** Line L7 reads the top without popping it. Popping and pushing it back is correct but slower.

## Implementations

## History

The recursive form of depth-first search became standard with Tarjan's 1972 paper and the textbooks that followed. Rewriting it with an explicit stack is a classical exercise: Cormen, Leiserson, Rivest and Stein ask for it in the section on depth-first search. Erickson discusses the relation between recursive DFS and a search with an explicit stack. The method is the general way to remove recursion from a procedure: keep, for each active call, its local state on a stack.

## References
