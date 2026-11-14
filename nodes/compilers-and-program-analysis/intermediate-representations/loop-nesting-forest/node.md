---
tag: EMNP01
kind: data-structure
slug: loop-nesting-forest
name: Loop nesting forest
aliases:
- loop tree
area: compilers-and-program-analysis/intermediate-representations
level: advanced
summary: A forest whose nodes are the loops of a flow graph, with each loop below the loops that contain it, defined for irreducible graphs too.
prereqs: [control-flow-graph, natural-loop, reducible-flow-graph, strongly-connected-components, tarjan-scc]
see_also: [t1-t2-reduction, cooper-harvey-kennedy-dominance, dominator-tree, depth-first-orders, loop-invariant-code-motion, induction-variable-analysis, kam-ullman-iteration-bound, elimination-dataflow-methods]
sources:
  - paper: doi:10.1145/570886.570887
    title: G. Ramalingam, On loops, dominators, and dominance frontiers, ACM Transactions on Programming Languages and Systems 24(5), 2002, pages 455-490
    locator: loop nesting forests in general, the construction that finds strongly connected components, picks headers, removes the edges into the headers and repeats, the forests of Steensgaard, Havlak and Sreedhar, Gao and Lee as cases of it, and the reduced Havlak forest
  - paper: doi:10.1145/316686.316687
    title: G. Ramalingam, Identifying loops in almost linear time, ACM Transactions on Programming Languages and Systems 21(2), 1999, pages 175-188
    locator: Steensgaard's top-down algorithm with generalized entry nodes and generalized back edges, the quadratic worst case of Havlak's algorithm, and almost-linear versions of the Havlak and Sreedhar, Gao and Lee algorithms
  - paper: doi:10.1145/262004.262005
    title: Paul Havlak, Nesting of reducible and irreducible loops, ACM Transactions on Programming Languages and Systems 19(4), 1997, pages 557-567
    locator: a loop nesting forest for reducible and irreducible loops built from a depth-first search
  - paper: doi:10.1145/236114.236115
    title: Vugranam C. Sreedhar, Guang R. Gao and Yong-Fong Lee, Identifying loops using DJ graphs, ACM Transactions on Programming Languages and Systems 18(6), 1996, pages 649-658
    locator: reducible and irreducible loops found with the dominator tree and the join edges of the flow graph
  - paper: "Bjarne Steensgaard, Sequentializing program dependence graphs for irreducible programs, Technical Report MSR-TR-93-14, Microsoft Research, 1993"
    locator: the loops of irreducible programs as nested strongly connected components with entry nodes
---

A loop nesting forest describes the loops of a [control flow graph](/control-flow-graph/) and how they nest. Each node of the forest is a loop, a set of blocks, with a set of *headers*, and each loop lies below the smallest loop that contains it. On a [reducible flow graph](/reducible-flow-graph/) the loops are the [natural loops](/natural-loop/) merged by header, and the forest is the usual loop tree of a compiler. The forest is also defined when the graph is irreducible: a loop that can be entered at several blocks gets several headers. This page builds the forest of Steensgaard. The outer loops are the nontrivial [strongly connected components](/strongly-connected-components/) of the graph. The headers of a loop are its blocks with a predecessor outside the loop, and the inner loops are found again in the loop with its headers removed. Removing the edges from each loop into its headers leaves a graph with no cycle.

## In plain words

A program often has loops inside loops. A compiler wants a map of them: which blocks belong to each loop, where each loop starts, and which loop is inside which. The loop nesting forest is that map. To build it, find each group of blocks in which every block can get to every other block. Each such group is a loop. The blocks where control can come into the group from outside are its headers, the doors of the loop. Take the doors away, and look for groups again inside what is left. These are the inner loops. Go on until no group is left. In a well-structured program every loop has one door, at its top. In other programs a loop can have two or more doors, and the map shows all of them.

## The abstract type

The input is a flow graph $G = (V, E, r)$ with a root $r$. Only the part that $r$ reaches counts. The structure holds a family of *loops*. Each loop $L$ is a set of vertices with a nonempty set $H(L) \subseteq L$ of headers and a parent loop or none. The operations are:

- `loop_forest(G, r)`: build the structure.
- `headers(L)`, `parent(L)`, `children(L)`: read the forest.
- `innermost(v)`: the smallest loop that contains $v$, or none.
- `depth(L)`: the number of loops from $L$ up to its root, with $L$ counted.

The laws:

- **Nesting.** Two loops are disjoint or one contains the other, and the loops that contain $L$ are $L$ and its ancestors.
- **Children avoid the headers.** A child of $L$ lies in $L \setminus H(L)$.
- **Loops are cycles.** Each loop is strongly connected and holds a cycle, and every cycle of the graph lies in some loop.
- **The headers break the cycles.** If the edges from inside each loop $L$ into $H(L)$ are removed, the graph has no cycle.
- **Reducible graphs.** If $G$ is reducible, each loop has one header $h$. $h$ dominates the loop, and the loop is the union of the natural loops of the back edges into $h$. There is one loop for each vertex that is the target of a back edge.

## Representation

The Python code returns a list of loops. Each loop is a dict with the sorted list `nodes`, the sorted list `headers` and the index `parent`, which is $-1$ at a root of the forest. A parent comes before its children in the list. `innermost(n, loops)` gives each vertex its innermost loop, and `depth(loops, i)` follows the parent indices. `cfg_loops(prog)` does the same for a program in the toy IR and uses block labels.

A compiler does not store the full vertex set of every loop, because a vertex at depth $d$ would be stored $d$ times. It keeps one record per loop with its headers, its parent and its children, and one pointer per block to the innermost loop. Then the loops of a block are found by following parents, and the blocks of a loop by walking its subtree. This uses $O(n)$ space for $n$ blocks.

## Operations

```pseudo id=main
LOOP-NESTING-FOREST(G, r)
L1  R0 <- the vertices that r reaches; T <- the stack [(R0, none)]
L2  while T is not empty do
L3      (R, p) <- pop(T)
L4      for each strongly connected component S of G[R] do
L5          skip S if it has one vertex and no self-loop
L6          H <- {v in S : v = r or v has a predecessor in R0 outside S}
L7          record the loop S with headers H and parent p
L8          push (S \ H, the new loop) on T
L9  return the loops
```

Line L1 drops the unreachable part, and line L6 looks only at predecessors that $r$ reaches, so dead code cannot create a header. The root has no predecessor, so line L6 counts it as an entry, as if control came into it from outside. A loop always has a header: if it does not hold $r$, a path from $r$ into the loop must enter it somewhere. So each region on the stack is smaller than the loop above it, and the loop stops. The code finds the components with [Tarjan's algorithm](/tarjan-scc/), with an explicit stack, so deep nesting does not use Python recursion.

`innermost` walks the list once and keeps, for each vertex, the last loop that contains it. This is the innermost one, because the loops that contain a vertex form a chain and a parent comes before its children.

## Example

Take the blocks B0 to B6 with the edges B0→B1, B1→B2, B2→B1, B2→B3, B3→B4, B4→B3, B4→B5, B5→B1 and B5→B6. This is a loop at B1 with a loop at B3 inside it.

| step | region | components | loop found | headers |
|---|---|---|---|---|
| 1 | B0 to B6 | {B0}, {B1, B2, B3, B4, B5}, {B6} | {B1, B2, B3, B4, B5} | B1, entered from B0 |
| 2 | {B2, B3, B4, B5} | {B2}, {B3, B4}, {B5} | {B3, B4}, parent 0 | B3, entered from B2 |
| 3 | {B4} | {B4} | none, B4 has no self-loop | |

The innermost loops are: B0 none, B1 loop 0, B2 loop 0, B3 loop 1, B4 loop 1, B5 loop 0, B6 none. The edges into headers from inside their loops are B2→B1, B5→B1 and B4→B3. Without them the graph has no cycle. The graph is reducible, and loop 0 is the union of the natural loops of B2→B1 and B5→B1.

Now take an irreducible graph: r→A, r→B, A→B, B→A and A→C. The only nontrivial component is {A, B}. Both blocks have the predecessor r outside it, so the loop {A, B} has the headers A and B, and nothing is left inside. No block of the cycle dominates the other, so the graph has no back edge at all, and no natural loop finds this cycle. The forest still shows it.

## Correctness

The proof file shows four things. First, every loop has a header, so the regions shrink and the construction stops, with at most $n$ loops and depth at most $n$. Second, the loops nest: loops made from one region are disjoint, and everything below a loop lies in it. Third, a cycle that avoids all the removed edges would lie in one component of some region, would have to avoid its headers, and so would lie in a smaller region, which gives a contradiction by induction. Fourth, for a reducible graph, take the first vertex $h$ of a top loop in a topological order of the graph without back edges. Every edge into $h$ from the loop is then a back edge, $h$ dominates the loop and is its only header, and the loop is the union of the natural loops into $h$. Inside the loop, delete the edges into $h$ and make $h$ the root. This smaller graph is reducible, has the same dominators and natural loops, and gives the same inner loops with the same headers, so induction on the number of edges finishes the proof. The component step is Tarjan's algorithm and is cited.

## Complexity

Let $n$ be the number of vertices, $m$ the number of edges and $d$ the depth of the forest.

| operation | time | space |
|---|---|---|
| build (lines L1 to L9) | $O((d + 1)(n + m))$, so $O(n (n + m))$ in the worst case | $O(n + m)$ working space |
| the loops as vertex lists | | $\Theta(\sum_v \mathrm{depth}(v))$, at most $O(n d)$ |
| `innermost` for all vertices | $O(\sum_v \mathrm{depth}(v))$ | $O(n)$ |
| `parent`, `headers` | $O(1)$ | |
| `depth(L)` | $O(\mathrm{depth}(L))$ | |

**Proved.** The regions at one depth of the forest are disjoint, so one depth costs $O(n + m)$, and there are at most $d + 1$ depths. The bound is tight: the path $0, 1, \ldots, 2k$ with the back edges $2k - i \to i$ for $i < k$ has $k$ nested loops, and the work is $\Theta(k^2)$ for $\Theta(k)$ edges. The Python code also sorts each region and each loop for a fixed output, which adds $O(n \log n)$ per depth.

**Cited, not proved.** Ramalingam showed that Havlak's algorithm is quadratic in the worst case, not almost linear as first stated, and gave almost-linear versions of it and of the algorithm of Sreedhar, Gao and Lee. He later defined the reduced Havlak forest, which a bottom-up algorithm builds in almost linear time. Those algorithms build other forests, not the one of this page.

**Measured, not proved.** On the nested path above, the Python code took about 0.04 s for $k = 250$, 0.17 s for $k = 500$, 0.71 s for $k = 1000$ and 3.0 s for $k = 2000$ on one laptop, about four times as long for each doubling. Over 2,000 seeded random graphs with up to 9 vertices, 1,749 were reducible, and the loops had 1 header in 2,140 cases, 2 in 223, 3 in 49 and 4 in 14.

## Variants

- **Havlak's forest.** Do a depth-first search and give each loop one header, its first vertex in the search. On an irreducible graph the result can depend on the order of the search.
- **Sreedhar, Gao and Lee.** Find the loops with the [dominator tree](/dominator-tree/) and the join edges of the flow graph, the DJ graph.
- **Reduced Havlak forest.** Ramalingam's forest, built bottom-up in almost linear time.
- **The loop tree of a reducible graph.** Find the back edges with dominators, build each [natural loop](/natural-loop/) by a backward search from the tail, and merge the loops that share a header. On a reducible graph this gives the forest of this page, as the proof file shows.
- **A virtual root.** Many compilers add one more node above the forest for the whole function, so the forest becomes a tree.

## When to use it

Use the forest when an optimization needs the loop structure: [loop invariant code motion](/loop-invariant-code-motion/), [induction variable analysis](/induction-variable-analysis/), unrolling and other loop transformations, block placement, and register allocation that weights spill costs by loop depth. It is also a good order for iterative data-flow analysis, since an inner loop can settle before its outer loop. Use this construction when the input can be irreducible, for example code from a goto, from a decompiler or from a JIT that enters a loop in the middle. If the graph is known to be reducible, the natural loops from a [dominator tree](/dominator-tree/) give the same forest and often come for free.

## Pitfalls

- **One header is not always true.** An irreducible loop has two or more headers. An optimization that puts a preheader before "the" header must skip such a loop or first make it reducible, for example by node splitting.
- **The forests differ.** On an irreducible graph, Steensgaard's, Havlak's and other forests can give different headers and different inner loops. Do not mix results from two of them.
- **The root.** The entry block has no predecessor. If it lies on a cycle, it must still count as a header, or the loop through it gets no header and the construction does not stop.
- **Unreachable code.** An edge from a block that the entry cannot reach must be ignored. Otherwise it can turn a block of a real loop into a header.
- **Self-loops.** A block with an edge to itself is a loop with one vertex. A block on no cycle is not a loop.
- **Recursion depth.** Loop nests from generated code can be hundreds deep. Use explicit stacks for the components and for the regions.
- **Stale forests.** A transformation that adds or removes blocks or edges can change the loops. Rebuild the forest or update it.

## Implementations

## History

Early optimizing compilers found loops through intervals and dominators, in the work of Allen and Cocke around 1970, and the natural loops of a reducible graph give the loop tree that textbooks describe. Irreducible graphs needed more. Steensgaard's technical report of 1993 defined loops as nested strongly connected components with entry nodes, for program dependence graphs of irreducible programs. Sreedhar, Gao and Lee found loops with DJ graphs in 1996, and Havlak described a forest from a depth-first search in 1997. Ramalingam showed in 1999 that Havlak's algorithm can take quadratic time and gave almost-linear versions, and in 2002 he described a common frame for these forests and the reduced Havlak forest.

## References
