---
tag: X5MM3D
kind: algorithm
slug: gabow-path-based-scc
name: Gabow's path-based strong component algorithm
aliases:
- Path-based SCC
- Gabow-Scc
area: graphs/connectivity
level: advanced
summary: A single-pass DFS SCC algorithm that uses two stacks instead of low-link values.
solves: [strongly-connected-components]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true}
history:
  year: 2000
  people: [Harold Gabow, Joseph Cheriyan, Kurt Mehlhorn]
  note: Purdom and Munro contracted cycles of the search path around 1970; Cheriyan and Mehlhorn in 1996 and Gabow in 2000 gave the linear version with two stacks.
prereqs: [strongly-connected-components, depth-first-search, stack]
see_also: [tarjan-scc, kosaraju-sharir, condensation-graph, low-link, hopcroft-tarjan-biconnectivity, topological-sort, 2-sat, biconnected-components]
sources:
  - paper: doi:10.1016/S0020-0190(00)00051-X
    title: Harold N. Gabow, Path-based depth-first search for strong and biconnected components, Information Processing Letters 74(3-4), 107 to 114 (2000)
    locator: the strong components algorithm with the stacks S and B, and its correctness and time bound
  - book: isbn:9780201316636
    title: Robert Sedgewick, Algorithms in C, Part 5, Graph Algorithms, third edition, Addison-Wesley
    locator: Chapter 19, Digraphs and DAGs, Section 19.8, Strong components in digraphs (Gabow's algorithm)
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: Section 3, strong connectivity (the one-pass method with low-link values that the path-based method replaces)
---

Gabow's algorithm finds the [strongly connected components](/strongly-connected-components/) of a [directed graph](/directed-graph/) with one [depth-first search](/depth-first-search/) in $\Theta(n + m)$ time. Like [Tarjan's algorithm](/tarjan-scc/) it keeps a [stack](/stack/) $S$ of the vertices whose component is not yet known. In place of the [low-link](/low-link/) values, it keeps a second stack $B$ that cuts $S$ into blocks of vertices that are already known to be in one component. An edge back into $S$ merges the blocks on top of the stack, and a block closes as a component when the search leaves its first vertex. The components come out in reverse [topological order](/topological-sort/) of the [condensation](/condensation-graph/), and the method needs no array of low values.

## In plain words

Walk through a one-way street network deep first, and keep the towns you have entered, in order, on a pile.

When a street leads back to a town that is still on the pile, you have found a round trip: every town on the pile from that town up to where you stand can reach every other. Mark that whole top part of the pile as one group. A second, short pile holds the place where each group starts.

When you finish with a town that starts a group, no street from the group leads back to an older part of the pile. So the group is a complete set of towns that reach each other. Take it off the pile.

## The problem

**Input.** A directed graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$ and $m$ edges in [adjacency lists](/adjacency-list/). Parallel edges and [self-loops](/self-loop/) are allowed and change nothing: a loop is an edge back to a vertex on $S$, which merges no block, and a parallel copy repeats a test that has no further effect.

**Output.** A label $\mathrm{comp}(v)$ for each vertex, with $\mathrm{comp}(u) = \mathrm{comp}(v)$ exactly when $u$ and $v$ reach each other. The labels are $0, 1, \ldots, c - 1$ in the order the components close.

## The algorithm

$\mathrm{pre}[v]$ is the preorder number of $v$, with 0 for a vertex not yet reached. $S$ holds the reached vertices that have no component yet, in preorder. $B$ holds preorder numbers in increasing order; the entry $b$ marks the block of $S$ that starts at the vertex with preorder number $b$.

```pseudo id=main
PATH-BASED-SCC(G)
L1  pre[v] ← 0 and comp[v] ← nil for each v ∈ V, t ← 0, c ← 0, S and B empty
L2  for each v ∈ V with pre[v] = 0 do VISIT(v)

VISIT(v)
L3  t ← t + 1, pre[v] ← t
L4  push v onto S, push pre[v] onto B          ▷ v starts a new block
L5  for each edge (v, w) do
L6      if pre[w] = 0 then VISIT(w)
L7      else if comp[w] = nil then             ▷ w is on S: a cycle closes
L8          while pre[w] < top(B) do pop B     ▷ merge the blocks above w
L9  if top(B) = pre[v] then                    ▷ v starts the top block
L10     pop B
L11     pop S down to and including v, set comp ← c for each popped vertex, c ← c + 1
```

Line L7 skips the edges into vertices that already have a component; those vertices cannot reach back. Line L6 recurses, so a program uses an explicit stack of (vertex, next edge) pairs, as in the implementation below.

## Example

The graph is the one on the [condensation](/condensation-graph/) page: vertices 0 to 7 and 13 edges $0 \to 1$, $1 \to 2$, $2 \to 0$, $2 \to 3$, $1 \to 3$, $3 \to 4$, $4 \to 3$, $4 \to 5$, $0 \to 5$, $5 \to 6$, $6 \to 5$, $6 \to 7$, and the loop $7 \to 7$. The lists are in this order, and the search starts at 0. Since $\mathrm{pre}[v] = v + 1$ here, $B$ is shown by preorder numbers.

| step | event | $S$ | $B$ |
|---|---|---|---|
| 1 | enter 0, 1, 2 | 0 1 2 | 1 2 3 |
| 2 | edge $2 \to 0$, 0 on $S$: pop 3 and 2 | 0 1 2 | 1 |
| 3 | enter 3, 4 | 0 1 2 3 4 | 1 4 5 |
| 4 | edge $4 \to 3$: pop 5 | 0 1 2 3 4 | 1 4 |
| 5 | enter 5, 6 | 0 1 2 3 4 5 6 | 1 4 6 7 |
| 6 | edge $6 \to 5$: pop 7 | 0 1 2 3 4 5 6 | 1 4 6 |
| 7 | enter 7; loop $7 \to 7$ pops nothing | 0 1 2 3 4 5 6 7 | 1 4 6 8 |
| 8 | leave 7: top is 8, close $\{7\}$ as component 0 | 0 1 2 3 4 5 6 | 1 4 6 |
| 9 | leave 6 (top is 6, not 7); leave 5: close $\{5, 6\}$ as 1 | 0 1 2 3 4 | 1 4 |
| 10 | leave 4; leave 3: close $\{3, 4\}$ as 2 | 0 1 2 | 1 |
| 11 | leave 2; edge $1 \to 3$, 3 done; leave 1; edge $0 \to 5$, 5 done | 0 1 2 | 1 |
| 12 | leave 0: close $\{0, 1, 2\}$ as 3 | empty | empty |

The labels are $\mathrm{comp} = (3, 3, 3, 2, 2, 1, 1, 0)$. The order $D, C, B, A$ of closing is the reverse of the topological order $A, B, C, D$ of the condensation.

## Correctness

The claim is that each set popped at line L11 is a strong component. A full proof is on the [correctness page](proofs/correctness/). It rests on three invariants. Call a vertex *active* when it is on $S$, and let the blocks of $S$ be the parts cut by the entries of $B$.

1. **Every entry of $B$ is the preorder number of a vertex on the call stack,** and the entries increase. When VISIT$(v)$ ends, $\mathrm{top}(B) \le \mathrm{pre}[v]$, with equality only if $v$ starts the top block.
2. **Two vertices in one block reach each other.** A new vertex is a block of its own. When the edge $(v, w)$ hits an active $w$, the first vertex of the block of $w$ is a tree ancestor of $v$, so $w$ reaches $v$, and the edge closes a cycle through all blocks from that of $w$ to the top. Line L8 merges exactly those blocks.
3. **After an edge $(x, w)$ is scanned, $w$ has a component or lies in the same block as $x$,** and no edge leads from a vertex with a component to an active one.

When VISIT$(v)$ closes the top block $T$, every edge out of $T$ has been scanned, so by invariant 3 it ends in $T$ or at a vertex that cannot reach $T$. So no vertex outside $T$ is in the component of $v$, and by invariant 2 all of $T$ is.

## Complexity

**Time.** Each vertex is reached once by line L6 or L2, pushed once onto $S$ and popped once at line L11. Each vertex pushes one entry onto $B$, so lines L8 and L10 pop at most $n$ entries in all. Each edge is scanned once at line L5. The total is $\Theta(n + m)$, best and worst, since every list is read.

**Space.** $\mathrm{pre}$, $\mathrm{comp}$, $S$, $B$ and the call stack take $\Theta(n)$ words beyond the graph. With $\mathrm{comp}$ stored in the same array as $\mathrm{pre}$ (for example as $n + 1 + c$), the method needs one array of integers and three stacks.

## Properties

- **One pass.** One depth-first search, with no [transpose](/graph-transpose/) and no second search, unlike the [Kosaraju-Sharir algorithm](/kosaraju-sharir/).
- **No low values.** Tarjan's algorithm keeps $\mathrm{low}[v]$ and updates it on each edge; here the top of $B$ plays the role of the low value of the whole current path.
- **Output order.** Components close in reverse topological order of the condensation: a component closes only after all components it reaches.
- **Deterministic.** The labels depend on the order of the vertices and the lists, but the partition does not.

## Variants and improvements

- **Biconnected components.** Gabow's paper gives the same two-stack method for the [biconnected components](/biconnected-components/) of an undirected graph, in place of the low points of the [Hopcroft-Tarjan algorithm](/hopcroft-tarjan-biconnectivity/).
- **Cheriyan and Mehlhorn.** They gave the same two-stack scheme in 1996, as part of work on dense graphs.
- **Purdom and Munro.** The first path-based methods merged the vertices of each cycle on the path with set-merging structures, which cost a little more than linear time.
- **Iterative form.** The explicit stack of (vertex, next edge) pairs avoids deep recursion; the pair can be kept in two arrays indexed by depth.
- **2-SAT and condensation.** Because the components come out in reverse topological order, the method gives the [condensation](/condensation-graph/) and solves [2-SAT](/2-sat/) without a separate topological sort.

## When to use it

Use it when you need the strong components of a large directed graph in one pass and want simple code: two stacks and a preorder array, no low values and no transpose. It is as fast as Tarjan's algorithm in theory, and in practice the two are close. If the transpose is already at hand and a simple proof matters more, the Kosaraju-Sharir algorithm is also fine.

## Pitfalls

- **Edges to finished vertices.** An edge to a vertex that already has a component must be ignored; merging on it would join two components. Line L7 tests $\mathrm{comp}[w] = \mathrm{nil}$, not only $\mathrm{pre}[w] \neq 0$.
- **The pop test.** Line L8 pops while $\mathrm{pre}[w] < \mathrm{top}(B)$, so the block that contains $w$ stays. Using $\le$ would remove it.
- **The close test.** Line L9 compares the top of $B$ with $\mathrm{pre}[v]$, not with any entry below it.
- **Recursion depth.** A directed path of $n$ vertices makes the search $n$ deep. Use an explicit stack.
- **Loops.** A loop $v \to v$ must not count as a cycle with other vertices; line L8 pops nothing for it, since $\mathrm{pre}[v] \ge \mathrm{top}(B)$ at that point.

## Implementations

## History

Purdom (1970) and Munro (1971) found strong components by following the depth-first path and contracting each cycle that closes on it into one vertex, with set-merging structures. Tarjan's 1972 algorithm reached linear time with low-link values. Cheriyan and Mehlhorn (1996) and Gabow (2000) showed that the contraction needs no set-merging: the order of the path is enough, and a stack of block boundaries represents the contracted path. Gabow's paper presents the method as a simpler view of depth-first search and applies it to strong and to biconnected components.

## References
