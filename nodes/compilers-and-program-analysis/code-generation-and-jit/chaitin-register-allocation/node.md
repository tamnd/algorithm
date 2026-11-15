---
tag: D7BWHP
kind: algorithm
slug: chaitin-register-allocation
name: Chaitin register allocation
aliases:
- graph coloring register allocation
- Chaitin allocator
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Simplifies the interference graph by removing nodes of degree less than k, spills when none is left, and colors in reverse order.
solves: [register-allocation-problem]
model: word-ram
complexity:
  vars: {n: the number of names, m: the number of interference edges, s: the number of instructions, l: the time of one liveness analysis, r: the number of rounds (at most n + 1)}
  time: {worst: O(r (l + s n + n^2))}
  space: {extra: O(n + m + s)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1981
  people: [Gregory J. Chaitin, Marc A. Auslander, Ashok K. Chandra, John Cocke, Martin E. Hopkins, Peter W. Markstein]
  note: The allocator of the experimental PL.8 compiler at IBM. Chaitin added the simplify rule and spill costs in 1982.
prereqs: [interference-graph, register-allocation-problem, greedy-coloring, degeneracy]
see_also: [briggs-optimistic-coloring, iterated-register-coalescing, spill-code-placement, register-allocation-np-completeness, degeneracy-ordering, k-coloring, linear-scan-register-allocation, rematerialization]
sources:
  - paper: doi:10.1016/0096-0551(81)90048-5
    title: Gregory J. Chaitin, Marc A. Auslander, Ashok K. Chandra, John Cocke, Martin E. Hopkins and Peter W. Markstein, Register allocation via coloring, Computer Languages 6(1), 1981, 47-57
    locator: global allocation as coloring of the interference graph, the build and color phases, and spilling with a rebuild of the graph
  - paper: doi:10.1145/800230.806984
    title: Gregory J. Chaitin, Register allocation and spilling via graph coloring, Proceedings of the SIGPLAN '82 Symposium on Compiler Construction, SIGPLAN Notices 17(6), 1982, 98-105
    locator: the simplify rule (a node of degree less than k can always be colored last), the choice of a spill by cost divided by degree, and the loop of build, simplify, spill
  - paper: doi:10.1145/177492.177575
    title: Preston Briggs, Keith D. Cooper and Linda Torczon, Improvements to graph coloring register allocation, ACM Transactions on Programming Languages and Systems 16(3), 1994, 428-455
    locator: the description of Chaitin's allocator as the baseline, and the example graphs that are k-colorable but that Chaitin's allocator spills
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 11 (Register Allocation), coloring by simplification, and spilling
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 13 (Register Allocation), global allocation by graph coloring, the top-down and bottom-up coloring schemes, and spill costs
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 16 (Register Allocation), graph coloring with webs, spill costs and the pruning of the graph by degree
---

Chaitin's allocator gives registers to the names of a program by coloring its [interference graph](/interference-graph/) with $k$ colors, one per register. It removes vertices of degree less than $k$ one by one, because such a vertex can always be colored after its neighbors. When every vertex left has degree $k$ or more, it chooses one to spill by the ratio of its spill cost to its degree, keeps that name in memory, adds loads and stores, and starts again with a new graph. When nothing is spilled, it colors the vertices in the reverse order of their removal. It solves the [register allocation problem](/register-allocation-problem/) as a heuristic: it always gives a correct program, but it may spill a name although the graph has a $k$-coloring, and the full problem is NP-hard ([register-allocation-np-completeness](/register-allocation-np-completeness/)).

## In plain words

Each value of the program is a dot, and a line joins two values that are needed at the same time. We want to color the dots with $k$ colors so that no line joins two dots of one color. Look for a dot with fewer than $k$ lines. Whatever colors its neighbors get, at least one color is left for it. So put it aside and forget it. Its removal may give other dots fewer lines, so repeat. If every dot gets put aside, give colors in the reverse order: each dot, when its turn comes, still has a free color. If at some moment every dot left has $k$ lines or more, pick the one that is cheapest to keep in memory, move it to memory in the program, and start again.

## The problem

The input is a program $P$ in the toy IR with `const`, `copy` and `op` instructions, and a number $k \ge 2$ of registers. The output is a program $P'$ that uses only the registers $r_0, \ldots, r_{k-1}$ and memory slots `mem.x`, and that has the same outcome as $P$ on every input. The goal is few loads and stores, but the allocator gives no bound on their number.

The algorithm works on the interference graph $G = (V, E)$: two names are joined when one is live just after a definition of the other, except at a copy between them. A *$k$-coloring* is a map $c: V \to \{0, \ldots, k-1\}$ with $c(x) \ne c(y)$ on every edge. The *$k$-core* of $G$ is the largest induced subgraph in which every vertex has degree at least $k$ (it may be empty); see [degeneracy](/degeneracy/). The *spill cost* of a name is here the number of its definitions and uses; a real compiler weights each one by an estimate of how often its block runs.

## The algorithm

```pseudo id=main
CHAITIN-ALLOCATE(P, k)
L1  P <- P with a new entry block that loads each live parameter p from mem.p
L2  T <- the empty set                                    // spill temporaries
L3  loop
L4    G <- the interference graph of P                    // build
L5    cost[x] <- the number of definitions and uses of x in P, or infinity if x is in T
L6    stack <- empty; spill <- the empty set
L7    while G has a vertex do                             // simplify
L8      if some vertex v of G has degree < k then
L9        push v on stack; remove v from G
L10     else
L11       v <- a vertex of G with the least cost[v] / degree(v)
L12       spill <- spill + {v}; remove v from G
L13   if spill is empty then
L14     for each v on stack, from the top down do        // select
L15       color[v] <- the least color in 0 .. k-1 not used by a colored neighbor of v
L16     return P with each name x renamed to r[color[x]] and each copy r = r deleted
L17   P <- P with each x in spill kept in mem.x: a load into a new temporary before
           each use of x and a store from a new temporary after each definition of x
L18   T <- T + the new temporaries
```

Line L8 picks the vertices of degree less than $k$ in the order in which they reach that degree; the vertices that start below $k$ come first, in the order of the names in the program. The implementation keeps them in a queue. Line L11 breaks ties by the same order.

Line L15 always finds a color: when $v$ was pushed, it had fewer than $k$ neighbors left in $G$, and the neighbors colored before it are exactly those. The spill code of line L17 is *spill everywhere*: every use of a spilled name reads a fresh temporary loaded just before it, and every definition writes a fresh temporary stored just after it. A temporary lives across at most one instruction, so it gets an infinite cost and is never spilled again.

## Example

Take the program with one parameter `p`:

```
L0:
  a = p + 1
  b = p + 2
  c = a + b
  d = a * c
  e = b * d
  ret e
```

Line L1 adds the block `start` with `p = mem.p` and `jump L0`. The edges of $G$ are $p$-$a$, $a$-$b$, $a$-$c$, $b$-$c$ and $b$-$d$; $e$ is isolated. The names in program order are $p, a, b, c, d, e$, and the costs are 3, 3, 3, 2, 2 and 2.

**With $k = 3$.** The degrees are $p{:}1$, $a{:}3$, $b{:}3$, $c{:}2$, $d{:}1$ and $e{:}0$, so the queue starts as $p, c, d, e$.

| step | removed | degrees that change | queue after |
|---|---|---|---|
| 1 | $p$ | $a$: 3 to 2 | $c, d, e, a$ |
| 2 | $c$ | $a$: 2 to 1, $b$: 3 to 2 | $d, e, a, b$ |
| 3 | $d$ | $b$: 2 to 1 | $e, a, b$ |
| 4 | $e$ | none | $a, b$ |
| 5 | $a$ | $b$: 1 to 0 | $b$ |
| 6 | $b$ | none | empty |

No spill. Line L14 pops $b, a, e, d, c, p$ and line L15 gives $b \to 0$, $a \to 1$, $e \to 0$, $d \to 1$ (its neighbor $b$ has 0), $c \to 2$ ($a$ has 1 and $b$ has 0), and $p \to 0$. The result is:

```
start:
  r0 = mem.p
  jump L0
L0:
  r1 = r0 + 1
  r0 = r0 + 2
  r2 = r1 + r0
  r1 = r1 * r2
  r0 = r0 * r1
  ret r0
```

**With $k = 2$.** The queue starts as $p, d, e$. Removing them lowers $a$ and $b$ to degree 2, and then $a$, $b$ and $c$ all have degree 2. Line L11 compares $3/2$, $3/2$ and $2/2$ and spills $c$. Line L17 rewrites `c = a + b` and `d = a * c` as

```
  c.1 = a + b
  mem.c = c.1
  c.2 = mem.c
  d = a * c.2
```

The store and the load are next to each other, so the pressure does not drop: in round 2, $a$, $b$ and the temporary `c.2` still form a triangle. Round 2 spills $a$ (cost 3 over degree 4, tied with $b$ and first in order), round 3 spills $b$, and round 4 colors the graph. The final program has 3 stores and 5 loads besides the parameter load. One store and one load are enough, by keeping only $b$ in memory between its definition and `e = b * d`, as the page [register allocation problem](/register-allocation-problem/) shows. So the allocator is far from optimal on this program, mainly because of spill everywhere.

**A graph that is 2-colorable but spilled.** In a cycle of length 4 every vertex has degree 2. With $k = 2$, line L8 never applies, so line L11 spills a vertex, although two colors suffice. [Optimistic coloring](/briggs-optimistic-coloring/) colors this cycle.

## Correctness

The full proof is in the proof file. Its parts are:

- **Simplify rule.** If $\deg(v) < k$, then $G$ is $k$-colorable if and only if $G - v$ is. So removing $v$ at line L9 loses no coloring.
- **Select.** When no spill happens, line L15 gives each vertex a color below $k$ that differs from all its neighbors, so the coloring is proper.
- **When it spills.** Chaitin's allocator chooses a spill in a round if and only if the $k$-core of $G$ is not empty. So it colors without spilling exactly the graphs of [degeneracy](/degeneracy/) less than $k$.
- **Renaming.** If $c$ is a proper coloring of $G$, renaming each name $x$ to $r_{c(x)}$ keeps the outcome of every run. The proof is an invariant: at each point of a run, each live name that has a value is held by its register.
- **Spill everywhere.** After line L17, `mem.x` holds the value of $x$ at each point after a definition of $x$, so each load reads the right value.
- **Termination.** Each round spills at least one name of the original program, and such a name never comes back, so there are at most $n + 1$ rounds for $n$ names.

## Complexity

One round has three parts:

- **Build.** Liveness costs $l$. The walk over the instructions adds one edge per name live after each definition, so it takes $O(s n)$ time, and the graph takes $O(n + m)$ space as adjacency sets.
- **Simplify.** With a queue, each removal at line L9 updates the degrees of the neighbors, so all removals cost $O(n + m)$. A spill choice at line L11 scans the vertices left, $O(n)$ each, so at most $O(n^2)$ in a round. A heap keyed by cost over degree gives $O((n + m) \log n)$ instead.
- **Select.** Each vertex scans its neighbors once: $O(n + m)$.

Each round spills at least one original name, so $r \le n + 1$, and the total is $O(r (l + s n + n^2))$. Over all rounds, the spill code adds one load or store per occurrence of an original name, and temporaries are never spilled, so the program keeps $O(s)$ instructions. The example above needed 4 rounds for 6 names.

## Properties

- **Guarantee.** If the $k$-core of the interference graph is empty, the allocator colors it with at most $k$ colors and adds no spill code. Such a graph has degeneracy at most $k - 1$, and in the simplify order each vertex has fewer than $k$ neighbors that come later, as in a [degeneracy ordering](/degeneracy-ordering/).
- **No optimality.** It may spill when a $k$-coloring exists (the cycle of length 4 with $k = 2$), and when it spills, the amount of spill code can be far from the least (the example above). The problem it attacks is NP-complete for $k \ge 3$, so no polynomial-time allocator is exact unless P = NP.
- **Deterministic.** The result depends on the order of the names and the tie-breaking rule.
- **Copies.** The allocator does not coalesce. A copy `x = y` is deleted only when $x$ and $y$ get the same color by chance.

## Variants and improvements

- **[Optimistic coloring](/briggs-optimistic-coloring/)** (Briggs, Cooper and Torczon) pushes the spill choice of line L11 on the stack like any other vertex and spills it only if line L15 finds no free color. It spills a subset of what Chaitin's allocator spills.
- **[Iterated register coalescing](/iterated-register-coalescing/)** (George and Appel) adds [conservative coalescing](/conservative-coalescing/) of copies to the simplify loop.
- **Better spill code.** [Spill code placement](/spill-code-placement/) loads a value once for several close uses, [live range splitting](/live-range-splitting/) spills a name only where the pressure is high, and [rematerialization](/rematerialization/) recomputes a constant instead of loading it.
- **Spill cost.** A real allocator weights each definition and use by an estimate of how often its block runs, so that names used in loops are spilled last. Other ratios than cost over degree are used too.
- **Precolored vertices.** Machine registers fixed by calling conventions are vertices with a fixed color that are never removed or spilled.

## When to use it

Use it in an optimizing compiler that can afford to build the interference graph, when the target has a fixed set of uniform registers. It is the basis of most graph-coloring allocators, but production compilers use the optimistic form, usually with coalescing. For a JIT compiler or for huge functions, [linear scan](/linear-scan-register-allocation/) is cheaper. On SSA form, [SSA-based allocation](/ssa-based-register-allocation/) colors optimally once the pressure is at most $k$.

## Pitfalls

- **A copy is not an interference.** Adding an edge between `x` and `y` at `x = y` blocks coalescing and wastes a register. The rule skips the copy source.
- **A dead definition still writes a register.** The definition must interfere with the names live after it, or the write can destroy a live value.
- **Rebuild after spilling.** Spill code changes liveness. In the example, spilling $c$ left its reload `c.2` in the same triangle. Coloring the old graph minus the spilled names is wrong.
- **Spill temporaries must not be spilled.** A temporary of spill everywhere has the shortest possible life; spilling it again creates new temporaries with the same life and the loop never ends. The infinite cost of line L5 prevents this.
- **$k \ge 2$.** An instruction such as `x = a + b` with both operands spilled reads two temporaries at once, so one register is not enough in this model.
- **Parameters.** A parameter live on entry needs a definition, or it interferes with nothing and may share a register with another live parameter. Line L1 adds the loads that define them.

## Implementations

## History

Chaitin, Auslander, Chandra, Cocke, Hopkins and Markstein (1981) made graph coloring work for global register allocation in the PL.8 compiler at IBM. The same paper showed that every graph is an interference graph, so exact coloring is NP-complete. Chaitin (1982) described the simplify rule, the cost over degree heuristic and the build-simplify-spill loop that this page follows. Briggs, Cooper, Kennedy and Torczon (1989) and Briggs, Cooper and Torczon (1994) made the coloring optimistic, and George and Appel (1996) added iterated coalescing.

## References
