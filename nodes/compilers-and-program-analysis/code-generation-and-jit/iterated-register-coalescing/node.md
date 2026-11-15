---
tag: ZBH45M
kind: algorithm
slug: iterated-register-coalescing
name: Iterated register coalescing
aliases:
- George-Appel allocator
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Interleaves simplification with conservative coalescing of move-related nodes and freezes moves when stuck, removing many copies safely.
solves: [register-allocation-problem, register-coalescing-problem]
model: word-ram
complexity:
  vars: {n: the number of names, m: the number of interference edges, c: the number of copies, s: the number of instructions, l: the time of one liveness analysis, r: the number of rounds (at most n + 1)}
  time: {worst: O(r (l + s n + n^2 (c + 1)))}
  space: {extra: O(n + m + s + c)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1996
  people: [Lal George, Andrew W. Appel]
  note: George and Appel published the algorithm in TOPLAS in 1996. It interleaves the conservative coalescing of Briggs, Cooper and Torczon with simplification, and adds the George test.
prereqs: [briggs-optimistic-coloring, conservative-coalescing]
see_also: [register-coalescing-problem, chaitin-register-allocation, spill-code-placement, live-range-splitting, ssa-based-register-allocation, out-of-ssa-translation, copy-propagation, linear-scan-register-allocation]
sources:
  - paper: doi:10.1145/229542.229546
    title: Lal George and Andrew W. Appel, Iterated register coalescing, ACM Transactions on Programming Languages and Systems 18(3), 1996, 300-324
    locator: the worklists for simplify, coalesce, freeze and potential spill, the George test, and the safety of the Briggs and George tests
  - paper: doi:10.1145/177492.177575
    title: Preston Briggs, Keith D. Cooper and Linda Torczon, Improvements to graph coloring register allocation, ACM Transactions on Programming Languages and Systems 16(3), 1994, 428-455
    locator: conservative coalescing with the Briggs test and optimistic select
  - paper: doi:10.1145/800230.806984
    title: Gregory J. Chaitin, Register allocation and spilling via graph coloring, Proceedings of the SIGPLAN '82 Symposium on Compiler Construction, SIGPLAN Notices 17(6), 1982, 98-105
    locator: aggressive coalescing (subsumption) of copies before coloring
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 11 (Register Allocation), the full iterated coalescing allocator with worklists, precolored nodes and pseudocode
  - paper: doi:10.1109/CGO.2007.26
    title: Florent Bouchez, Alain Darte and Fabrice Rastello, On the complexity of register coalescing, International Symposium on Code Generation and Optimization (CGO), 2007, 102-114
    locator: the complexity of aggressive, conservative, incremental conservative and optimistic coalescing
---

Iterated register coalescing is the graph-coloring allocator of George and Appel (1996). It adds the removal of copies to [optimistic coloring](/briggs-optimistic-coloring/). A copy `x = y` is free if $x$ and $y$ get the same register, because it becomes `r = r` and is deleted. So the allocator *coalesces* the two names: it merges their vertices in the [interference graph](/interference-graph/). A merge can make the graph harder to color, so the allocator merges only when the [Briggs test or the George test](/conservative-coalescing/) shows that the merge is safe. It mixes these merges with the simplify steps of Chaitin's allocator: removing a vertex lowers the degrees of its neighbors, and a copy that failed the test before may pass it now.

## In plain words

Many values in a program are only copies of other values. If a value and its copy share one register, the copy instruction is not needed. So the allocator tries to give them one register by joining them into one value. Joining is risky: the joined value clashes with everything that either part clashed with, so it can force a value into memory. The allocator joins two values only when a simple count shows that the joined value can still get a register. It takes out easy values first, and each removal can make another join safe. When nothing is easy and no join is safe, it gives up on a copy. Only when no copy is left to try does it pick a value that may go to memory.

## The problem

The input is a program $P$ in the toy IR with `const`, `copy` and `op` instructions, and a number $k \ge 2$ of registers. The output is a program with the same outcome that uses only the registers $r_0, \ldots, r_{k-1}$ and memory slots `mem.x` ([register allocation problem](/register-allocation-problem/)). A second aim is to delete as many copies `x = y` between two names as possible ([register coalescing problem](/register-coalescing-problem/)).

During one round, each vertex of the graph is a set of names, at first one name. Two vertices are adjacent if a name of one interferes with a name of the other. To *merge* two vertices $u$ and $v$ that are not adjacent is to replace them by their union, adjacent to every neighbor of $u$ or $v$. The cost of a vertex is the sum of the costs of its names, without the infinite costs of spill temporaries, and it is infinite only if all its names are temporaries. A copy is *live* while it is not coalesced and not given up. A vertex is *move-related* if it has a live copy.

Two tests decide if a merge of $u$ and $v$ is safe:

- **Briggs test.** In the graph after the merge, fewer than $k$ neighbors of the merged vertex have degree $k$ or more.
- **George test.** Every neighbor of $v$ is a neighbor of $u$ or has degree less than $k$, or the same holds with $u$ and $v$ swapped.

The parameter TEST is the Briggs test, the George test, or both (a merge is safe if one of them passes).

## The algorithm

```pseudo id=main
IRC-ALLOCATE(P, k, TEST)
L1  P <- P with a new entry block that loads each live parameter p from mem.p
L2  T <- the empty set                                    // spill temporaries
L3  loop
L4    G <- the interference graph of P; W <- the copies x = y of P between two names     // build
L5    cost[x] <- the number of definitions and uses of x in P, or infinity if x is in T
L6    stack <- empty
L7    while G has a vertex do
L8      if some vertex v has degree < k and is not move-related, or v is a spill candidate then    // simplify
L9        push v on stack; remove v from G
L10     else if W is not empty then                       // coalesce
L11       take a copy x = y out of W; u <- the vertex of x; v <- the vertex of y
L12       if u = v then the copy is coalesced
L13       else if u and v are adjacent then the copy is given up    // constrained
L14       else if TEST(G, u, v, k) then merge v into u; the copy is coalesced
L15       else the copy waits, and goes back to W when the degree of u, v or one of their neighbors drops to k - 1
L16     else if some vertex v of degree < k is move-related then    // freeze
L17       give up every live copy of v
L18     else                                              // potential spill
L19       v <- a vertex with the least cost[v] / degree(v); give up every live copy of v; make v a spill candidate
L20   spill <- the empty set
L21   for each v on stack, from the top down do          // select
L22     if some color in 0 .. k-1 is not used by a colored vertex adjacent to v then
L23       color[v] <- the least such color
L24     else spill <- spill + {v}
L25   if spill is empty then
L26     return P with each name x renamed to r[color[the vertex of x]] and each copy r = r deleted
L27   P <- P with each name of each vertex in spill kept in mem.x, by loads before uses and stores after definitions
L28   T <- T + the new temporaries
```

Line L8 simplifies only vertices that are not move-related, because removing a vertex ends all chances to coalesce it. Line L10 tries copies only when no such vertex is left. Line L16 freezes a low-degree vertex when all waiting copies have failed: its copies become ordinary instructions and the vertex can be simplified. Line L19 is reached only when every vertex left has degree $k$ or more. The spill candidate is then simplified at line L8, and line L24 spills it only if select finds no free color, as in optimistic coloring.

Line L15 is the "iterated" part. A copy that fails the test is not given up. The tests count neighbors of high degree, and simplify and other merges lower degrees. So when a degree drops to $k - 1$, the copies at that vertex and at its neighbors go back to $W$. A merge of $v$ into $u$ also puts the waiting copies of $v$ back to $W$.

## Example

This loop adds the numbers $n, n - 1, \ldots, 1$, in the style of a program after [out-of-SSA translation](/out-of-ssa-translation/), with one copy per loop variable:

```
L0:
  i = n
  s = 0
  jump L1
L1:
  t = s + i
  j = i - 1
  s = t
  i = j
  br i L1 L2
L2:
  ret s
```

After line L1 adds the block `start` with `n = mem.n`, the edges are $i$-$s$, $s$-$j$, $j$-$t$ and $t$-$i$, a cycle of length 4, and $n$ is isolated. No copy makes an edge between its two names. The copies are `i = n`, `i = j` and `s = t`. Take $k = 2$ and the Briggs test.

| step | line | action | why |
|---|---|---|---|
| 1 | L14, L15 | `i = n` waits | merged with $n$, vertex $i$ has the neighbors $s$ and $t$, both of degree 2 |
| 2 | L14 | merge $j$ into $i$ | after the merge, $s$ and $t$ have degree 1, so no neighbor has a high degree; `i = n` goes back to $W$ |
| 3 | L14 | merge $t$ into $s$ | the only neighbor, $\{i, j\}$, has degree 1 after the merge |
| 4 | L9 | push $\{s, t\}$ | degree 1 and no live copy |
| 5 | L14 | merge $n$ into $i$ | $\{i, j\}$ now has degree 0 |
| 6 | L9 | push $\{i, j, n\}$ | degree 0 |

Select gives $\{i, j, n\}$ color 0 and $\{s, t\}$ color 1. All three copies become `r = r` and are deleted:

```
start:
  r0 = mem.n
  jump L0
L0:
  r1 = 0
  jump L1
L1:
  r1 = r1 + r0
  r0 = r0 - 1
  br r0 L1 L2
L2:
  ret r1
```

Optimistic coloring without coalescing also colors this graph with $k = 2$, and it deletes `s = t` and `i = j` by chance, because a cycle of length 4 has only one 2-coloring up to a swap. But it gives $n$ color 0 and $i$ color 1, so `i = n` stays as `r1 = r0`. A script checked that both outputs return $n (n + 1) / 2$ for $n$ from 1 to 7. With the George test instead, step 1 passes at once: $n$ has no neighbor, so the condition holds for every neighbor of $n$.

**Why the tests are needed.** In this program, $b$ is a copy of $a$ on one path and is computed on the other:

```
L0:
  y = p + 2
  x = p + 1
  br x L1 L2
L1:
  a = x + 1
  a = a + x
  b = a
  jump L3
L2:
  b = y + 1
  b = b + y
  jump L3
L3:
  ret b
```

The edges are $a$-$x$, $x$-$y$, $y$-$b$ and $p$-$y$, so $a, x, y, b$ is a path and the graph is 2-colorable. Merging $a$ and $b$ makes the triangle $\{a, b\}, x, y$. Both tests refuse the merge with $k = 2$: the merged vertex would have the two neighbors $x$ and $y$ of degree at least 2, and neither $x$ nor $y$ is a neighbor of the other end. So IRC-ALLOCATE keeps the copy and needs no spill. With *aggressive* coalescing, which merges every pair that does not interfere, the graph has a triangle, $y$ is spilled, and a second round is needed. The output then has one store and two loads of `mem.y` instead of one copy.

## Correctness

The proof file shows:

- **The tests are safe.** If $G$ is $k$-colorable and $u, v$ pass the Briggs test or the George test, the graph after the merge is $k$-colorable. If $G$ has an empty $k$-core, so does the merged graph. Aggressive merging has neither property: the path above becomes a triangle.
- **No spill on easy graphs.** If the interference graph has an empty $k$-core, that is, if Chaitin's allocator colors it with no spill, then IRC-ALLOCATE never runs line L19 and spills nothing.
- **Select is proper.** A vertex pushed at line L9 that is not a spill candidate always gets a color, and adjacent vertices never get the same color. This holds even though merges change the graph after a vertex is pushed.
- **The output is correct.** Each name gets the color of its vertex. The names of one vertex never interfere, so this is a $k$-coloring of the interference graph, and the renaming and spill lemmas of [Chaitin's allocator](/chaitin-register-allocation/) apply.
- **It stops.** The inner loop stops by a counting argument, and each round that spills removes at least one name of the program after line L1 for good, so there are at most $n + 1$ rounds.

## Complexity

One round has at most $n$ pushes and $n - 1$ merges. A copy is taken from $W$ once at the start and then only after a degree drops to $k - 1$. The degree of a vertex goes up only when another vertex is merged into it, so there are $O(n)$ such drops in a round, and each one puts back at most $c$ copies. So there are $O(n c)$ tests in a round. Each test, merge or push costs $O(n)$ with adjacency sets, and finding the spill candidates costs $O(n^2)$ in all. With build in $O(s n)$ after a liveness analysis of cost $l$, and at most $r \le n + 1$ rounds, the time is $O(r (l + s n + n^2 (c + 1)))$. This is a simple bound, not a tight one. The space is $O(n + m + s + c)$, if the copy list of a merged vertex replaces the lists of its parts.

## Properties

- **Safe coalescing.** With the Briggs or George test, a merge never turns a graph with an empty $k$-core into one with a nonempty $k$-core. So coalescing never causes a spill on a graph that Chaitin's allocator colors.
- **Not every safe merge is found.** The tests are sufficient conditions. A merge that keeps the graph $k$-colorable can fail both tests, and the order in which copies are tried changes the result.
- **Conservative coalescing is hard to do best.** Bouchez, Darte and Rastello (2007) proved that finding the most copies that conservative coalescing can remove is NP-complete. So IRC-ALLOCATE is a heuristic for the coalescing part as well.
- **Freezing loses copies.** A frozen copy stays in the program, even if a later merge would have been safe.
- **Deterministic.** The result depends on the order of the names and the copies.

## Variants and improvements

- **Precolored vertices.** Real machines have registers with fixed roles, such as argument and return registers. George and Appel treat them as vertices that are already colored and never simplified or spilled, and use the George test when one end is precolored, because a precolored vertex can have a very large set of neighbors.
- **Coalescing at the select phase.** Biased coloring prefers, in select, the color of a copy partner. It deletes some copies without any merge.
- **Optimistic coalescing.** Park and Moon (2004) merge aggressively first and undo merges in select when a merged vertex finds no color.
- **SSA-based allocation.** [SSA-based register allocation](/ssa-based-register-allocation/) colors the chordal interference graph of an SSA program first and removes copies afterward.
- **Spill code.** [Spill code placement](/spill-code-placement/), [live range splitting](/live-range-splitting/) and [rematerialization](/rematerialization/) improve the code for the actual spills.

## When to use it

Use it in an optimizing compiler for a machine with a moderate number of registers when the program has many copies: after SSA destruction, after inlining, or with calling conventions that move arguments into fixed registers. It is the allocator of the textbook of Appel and the base of many graph-coloring allocators. When compile time matters more than code quality, use [linear scan](/linear-scan-register-allocation/). When copies are rare, plain [optimistic coloring](/briggs-optimistic-coloring/) is simpler.

## Pitfalls

- **A copy does not interfere.** At a copy `x = y`, the source $y$ does not interfere with $x$, even if $y$ is still live. If the build phase adds this edge, no copy can be coalesced.
- **Aggressive is not safe.** Merging every pair of non-interfering copy ends can turn a 2-colorable graph into a triangle, as in the example.
- **Use the right degrees.** The Briggs test counts degrees in the graph after the merge: a common neighbor of $u$ and $v$ loses one edge.
- **Do not simplify a move-related vertex.** Removing it early ends all chances to coalesce its copies. Freeze it first.
- **Costs of merged vertices.** A merged vertex that holds an original name must keep a finite cost. If it inherits the infinite cost of a spill temporary, the spill choice can get stuck.
- **Color the names, not only the vertices.** After select, each name takes the color of the vertex it was merged into.

## Implementations

## History

Chaitin's allocator (1982) coalesced aggressively: before coloring, it merged the two names of every copy that did not interfere, and repeated the build. Briggs, Cooper and Torczon (1994) noticed that this can make the graph harder to color, and proposed conservative coalescing with the Briggs test, run before simplify. George and Appel (1996) interleaved conservative coalescing with simplify and added the George test, freezing and the reuse of failed copies. Appel's textbooks present the full algorithm with its worklists. Bouchez, Darte and Rastello (2007) studied the complexity of the coalescing problems behind it.

## References
