---
tag: Y67E03
kind: algorithm
slug: briggs-optimistic-coloring
name: Optimistic coloring
aliases:
- Chaitin-Briggs allocator
- Briggs allocator
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Pushes a spill candidate on the stack instead of spilling it at once and spills only if no color is free when it is popped.
solves: [register-allocation-problem]
model: word-ram
complexity:
  vars: {n: the number of names, m: the number of interference edges, s: the number of instructions, l: the time of one liveness analysis, r: the number of rounds (at most n + 1)}
  time: {worst: O(r (l + s n + n^2))}
  space: {extra: O(n + m + s)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1989
  people: [Preston Briggs, Keith D. Cooper, Ken Kennedy, Linda Torczon]
  note: Optimistic coloring was presented at PLDI 1989 and described in full in the TOPLAS paper of Briggs, Cooper and Torczon in 1994.
prereqs: [chaitin-register-allocation]
see_also: [iterated-register-coalescing, conservative-coalescing, spill-code-placement, rematerialization, greedy-coloring, k-coloring, dsatur, register-allocation-np-completeness]
sources:
  - paper: doi:10.1145/74818.74843
    title: Preston Briggs, Keith D. Cooper, Ken Kennedy and Linda Torczon, Coloring heuristics for register allocation, Proceedings of the ACM SIGPLAN 1989 Conference on Programming Language Design and Implementation (PLDI), 1989, 275-284
    locator: the optimistic heuristic, which pushes the spill candidate on the stack and spills only when select finds no color, and the graphs that it colors where Chaitin's allocator spills
  - paper: doi:10.1145/177492.177575
    title: Preston Briggs, Keith D. Cooper and Linda Torczon, Improvements to graph coloring register allocation, ACM Transactions on Programming Languages and Systems 16(3), 1994, 428-455
    locator: the optimistic allocator in full, its comparison with Chaitin's allocator, and rematerialization
  - paper: doi:10.1145/800230.806984
    title: Gregory J. Chaitin, Register allocation and spilling via graph coloring, Proceedings of the SIGPLAN '82 Symposium on Compiler Construction, SIGPLAN Notices 17(6), 1982, 98-105
    locator: the simplify rule and the spill choice by cost over degree that optimistic coloring keeps
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 11 (Register Allocation), coloring by simplification with potential spills and actual spills
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 13 (Register Allocation), the bottom-up coloring allocator and its optimistic spill decision
---

Optimistic coloring is the change that Briggs, Cooper, Kennedy and Torczon (1989) made to [Chaitin's allocator](/chaitin-register-allocation/). Chaitin's allocator spills a name as soon as the simplify phase is stuck, that is, when every vertex left in the [interference graph](/interference-graph/) has $k$ neighbors or more. Optimistic coloring only marks that vertex as a spill candidate, pushes it on the stack like the others, and decides when it pops the vertex: if its neighbors happen to use fewer than $k$ colors, it gets a color and no spill code is needed. On the same graph with the same spill choices, it spills a subset of the names that Chaitin's allocator spills, and it colors graphs, such as a cycle of length 4 with two colors, that Chaitin's allocator cannot.

## In plain words

Chaitin's method removes values with few clashes, one at a time, and gives them colors later in the reverse order. When every value left has many clashes, it gives up on one of them at once and sends it to memory. But many clashes do not mean many colors: four neighbors may all have the same color. So optimistic coloring does not give up yet. It removes the value anyway, as if it would get a color, and goes on. Later, when the colors are handed out and the turn of that value comes, it looks at its neighbors. If a color is still free, the value gets it and nothing goes to memory. Only if all colors are taken does the value go to memory.

## The problem

The input is a program $P$ in the toy IR with `const`, `copy` and `op` instructions, and a number $k \ge 2$ of registers. The output is a program that uses only the registers $r_0, \ldots, r_{k-1}$ and memory slots `mem.x`, and that has the same outcome as $P$ on every input ([register allocation problem](/register-allocation-problem/)). The allocator works on the interference graph, with the spill cost of a name given by the number of its definitions and uses. A *spill candidate* is a vertex that the simplify phase removes while every vertex left has degree at least $k$. An *actual spill* is a vertex that select cannot color.

## The algorithm

```pseudo id=main
BRIGGS-ALLOCATE(P, k)
L1  P <- P with a new entry block that loads each live parameter p from mem.p
L2  T <- the empty set                                    // spill temporaries
L3  loop
L4    G <- the interference graph of P                    // build
L5    cost[x] <- the number of definitions and uses of x in P, or infinity if x is in T
L6    stack <- empty
L7    while G has a vertex do                             // simplify
L8      if some vertex v of G has degree < k then
L9        push v on stack; remove v from G
L10     else
L11       v <- a vertex of G with the least cost[v] / degree(v)    // a spill candidate
L12       push v on stack; remove v from G
L13   spill <- the empty set
L14   for each v on stack, from the top down do          // select
L15     if some color in 0 .. k-1 is not used by a colored neighbor of v then
L16       color[v] <- the least such color
L17     else spill <- spill + {v}                         // v stays without a color
L18   if spill is empty then
L19     return P with each name x renamed to r[color[x]] and each copy r = r deleted
L20   P <- P with each x in spill kept in mem.x: a load into a new temporary before
           each use of x and a store from a new temporary after each definition of x
L21   T <- T + the new temporaries
```

Lines L1 to L11 are those of Chaitin's allocator. The only changes are line L12, which pushes the candidate instead of spilling it, and lines L15 to L17, which spill a vertex only when it has no free color. As in Chaitin's allocator, line L8 takes the vertices of degree less than $k$ in the order in which they reach that degree, and line L11 breaks ties by the order of the names in the program.

A vertex pushed at line L9 always gets a color: when it was pushed, it had fewer than $k$ neighbors left, and only those can be colored before it. So line L17 is reached only for spill candidates. A neighbor that stays without a color does not block a color, which is why a vertex below an actual spill on the stack still finds one.

## Example

This loop has one parameter `n`:

```
L0:
  d = n
  jump L1
L1:
  a = d + 1
  b = a + d
  c = a + 1
  d = b - c
  d = d % c
  br d L1 L2
L2:
  ret d
```

After line L1 adds `n = mem.n` in a new block `start`, the interference edges are $a$-$b$, $b$-$c$, $c$-$d$ and $d$-$a$, a cycle of length 4. The copy `d = n` makes no edge, and $n$ is isolated. The costs are $n{:}2$, $d{:}8$, $a{:}3$, $b{:}2$ and $c{:}3$. Take $k = 2$.

| step | line | removed | why |
|---|---|---|---|
| 1 | L9 | $n$ | degree 0 |
| 2 | L12 | $b$ | all four left have degree 2; the ratios are $8/2$, $3/2$, $2/2$ and $3/2$ |
| 3 | L9 | $a$ | degree 1 after step 2 |
| 4 | L9 | $c$ | degree 1 after step 2 |
| 5 | L9 | $d$ | degree 0 |

Select pops $d, c, a, b, n$. It gives $d \to 0$, $c \to 1$ and $a \to 1$; both are neighbors of $d$ only among the colored vertices. The candidate $b$ has the colored neighbors $a$ and $c$, both with color 1, so color 0 is free and $b$ gets it. Then $n \to 0$. Nothing is spilled, and one round is enough. Chaitin's allocator spills $b$ at step 2 and needs a second round. The copy `d = n` becomes `r0 = r0` and is deleted, by chance:

```
start:
  r0 = mem.n
  jump L0
L0:
  jump L1
L1:
  r1 = r0 + 1
  r0 = r1 + r0
  r1 = r1 + 1
  r0 = r0 - r1
  r0 = r0 % r1
  br r0 L1 L2
L2:
  ret r0
```

A script ran both programs for $n$ from $-4$ to $7$. They gave the same outcomes, including the trap for $n = -2$, where $c = 0$.

**A graph that is 3-colorable but spilled.** Take the triangular prism: the triangles $0, 3, 4$ and $1, 2, 5$ and the edges $0$-$5$, $1$-$4$ and $2$-$3$. It has a 3-coloring. Every vertex has degree 3, so with $k = 3$ and equal costs, line L11 picks vertex 0 at once. Then the rest simplify in the order $3, 4, 5, 2, 1$. Select gives $1 \to 0$, $2 \to 1$, $5 \to 2$, $4 \to 1$ and $3 \to 0$. Vertex 0 has the neighbors 3, 4 and 5, with colors 0, 1 and 2, so it is spilled. Optimistic coloring is still a heuristic.

## Correctness

The proof file shows four facts:

- A vertex pushed at line L9 always gets a color, so only spill candidates can be spilled.
- The colors given at line L16 are a proper coloring of the colored vertices.
- On the same graph with the same costs and tie-breaking, the simplify phase of Chaitin's allocator and of this allocator remove the same vertices in the same order. So the actual spills of this allocator are a subset of the spills of Chaitin's allocator. In particular, every graph that Chaitin's allocator colors without a spill is colored by optimistic coloring, with the same colors.
- The renaming, the spill code and the termination proofs of Chaitin's allocator carry over: the result has the same outcome as the input, uses only $k$ registers, and comes after at most $n + 1$ rounds.

The cycle of length 4 with $k = 2$ shows that the subset can be strict.

## Complexity

The cost is that of [Chaitin's allocator](/chaitin-register-allocation/). Simplify and select take $O(n + m)$ time, plus $O(n)$ for each spill candidate when the candidates are found by a scan; build takes $O(s n)$ after a liveness analysis of cost $l$. Each round spills at least one name of the original program, so there are at most $n + 1$ rounds, and the total time is $O(r (l + s n + n^2))$. The space is $O(n + m + s)$. The change costs nothing: the candidate is pushed instead of being put in a set.

## Properties

- **Never worse in one round.** On a given graph, the actual spills are a subset of Chaitin's spills. When Chaitin's allocator colors the graph, optimistic coloring gives the same coloring.
- **Strictly better on some graphs.** The cycle of length 4 with $k = 2$ and the loop above are colored without a spill.
- **Not optimal.** The prism with $k = 3$ is spilled although it is 3-colorable, and the problem is NP-complete ([register-allocation-np-completeness](/register-allocation-np-completeness/)).
- **Only one round is compared.** After a spill, the two allocators rewrite the program in different ways, so the subset property says nothing about the later rounds.
- **Deterministic.** The result depends on the order of the names and on the tie-breaking rules.

## Variants and improvements

- **[Iterated register coalescing](/iterated-register-coalescing/)** of George and Appel keeps optimistic select and adds [conservative coalescing](/conservative-coalescing/) of copies during simplify.
- **[Rematerialization](/rematerialization/).** Briggs, Cooper and Torczon (1992, 1994) tag values that can be recomputed cheaply, such as constants, and replace their reloads by recomputation.
- **Biased coloring.** When select has a choice of colors, it can prefer the color of a copy partner, so that more copies become `r = r` and disappear without any coalescing in the graph.
- **Other select orders.** A general coloring heuristic such as [DSatur](/dsatur/) or the [greedy coloring](/greedy-coloring/) in another order may color more graphs, but it loses the guarantee that every vertex pushed at line L9 gets a color.
- **Better spill code.** [Spill code placement](/spill-code-placement/) and [live range splitting](/live-range-splitting/) reduce the cost of the actual spills.

## When to use it

Use it instead of Chaitin's allocator in every case: it costs the same and never spills more on the same graph. It is the base of the graph-coloring allocators in the textbooks of Appel and of Cooper and Torczon. If the program has many copies, as after SSA destruction, use [iterated register coalescing](/iterated-register-coalescing/), which adds coalescing. For fast compilation, [linear scan](/linear-scan-register-allocation/) is cheaper.

## Pitfalls

- **A spill candidate is not a spill.** Do not insert spill code at line L12. Insert it only for the vertices that line L17 leaves without a color.
- **Uncolored neighbors are free.** When the colors of the neighbors are collected at line L15, a neighbor that was spilled earlier in the same select has no color and must be skipped.
- **The candidate order matters.** Line L11 still uses cost over degree. A candidate pushed early is popped late, when more neighbors have colors, so its chance of a free color is lower.
- **Rebuild after spilling.** As in Chaitin's allocator, the spill code changes liveness, so the graph is built again in the next round.
- **Spill temporaries.** Temporaries get an infinite cost; otherwise the loop may never end.

## Implementations

## History

Briggs, Cooper, Kennedy and Torczon presented the optimistic heuristic at PLDI 1989, as a change to Chaitin's allocator. Briggs, Cooper and Torczon described it in full in TOPLAS in 1994, together with rematerialization. George and Appel (1996) combined it with iterated coalescing, and the textbook allocators of Appel and of Cooper and Torczon follow this design.

## References
