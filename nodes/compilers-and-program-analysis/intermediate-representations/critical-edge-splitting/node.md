---
tag: Z94GET
kind: technique
slug: critical-edge-splitting
name: Critical edge splitting
aliases:
- splitting critical edges
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: Puts a new empty block on each edge from a block with several successors to a block with several predecessors, to host inserted code.
prereqs: [control-flow-graph]
see_also: [out-of-ssa-translation, lost-copy-and-swap-problems, phi-function, lazy-code-motion, partial-redundancy-elimination, linear-scan-register-allocation, sreedhar-cssa-translation, ball-larus-path-profiling]
sources:
  - paper: "Jens Knoop, Oliver Rüthing and Bernhard Steffen, Lazy code motion, ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 1992), SIGPLAN Notices 27(7), pages 224-234"
    locator: Section 3.1 (Critical Edges), the example of an edge that blocks code motion, and the assumption that all critical edges are split first
  - paper: "Preston Briggs, Keith D. Cooper, Timothy J. Harvey and L. Taylor Simpson, Practical improvements to the construction and destruction of static single assignment form, Software: Practice and Experience 28(8), 1998, pages 859-881"
    locator: the lost copy problem on a critical back edge, and its repair by splitting the edge or by a careful copy insertion
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 19 (Static Single-Assignment Form), edge splitting and edge-split SSA form
  - book: isbn:9783030805142
    title: Fabrice Rastello and Florent Bouchez Tichadou (editors), SSA-based Compiler Design, Springer, 2022
    locator: Chapter 3 (Standard Construction and Destruction Algorithms), copies on critical edges during destruction; Chapter 21 (SSA Destruction for Machine Code), edges that cannot be split
  - paper: doi:10.1007/3-540-48294-6_13
    title: Vugranam C. Sreedhar, Roy Dz-Ching Ju, David M. Gillies and Vatsa Santhanam, Translating out of static single assignment form, Static Analysis Symposium (SAS 1999), LNCS 1694
    locator: translation out of SSA without splitting critical edges
---

A critical edge in a [control flow graph](/control-flow-graph/) is an edge from a block with two or more successors to a block with two or more predecessors. Code that must run exactly when control passes along such an edge has no home: the end of the source also runs on the source's other exits, and the start of the target also runs on the target's other entries. Critical edge splitting puts a new empty block in the middle of each such edge. The new block has one predecessor and one successor, so code placed there runs only on that edge. Compilers do this before [out-of-SSA translation](/out-of-ssa-translation/), before [lazy code motion](/lazy-code-motion/), and when a register allocator needs moves on an edge.

## In plain words

Some code must run when control goes from block A to block B, and at no other time. If A has only one way out, put the code at the end of A. If B has only one way in, put it at the start of B. If A has several exits and B has several entries, neither place works: code at the end of A also runs when A goes elsewhere, and code at the start of B also runs when B is entered from elsewhere. So make a new block C, send A's jump to C instead of to B, and let C jump to B. Now C is the place for the code.

## When it applies

- A transformation wants to insert code **on an edge**: the copies that replace [phi-functions](/phi-function/), the computations that [partial redundancy elimination](/partial-redundancy-elimination/) inserts, the moves that fix register assignments between blocks, or counters for edge profiling.
- The graph has edges $(a, b)$ with $|\mathit{succ}(a)| \ge 2$ and $|\mathit{pred}(b)| \ge 2$. On every other edge, the end of $a$ or the start of $b$ is already a safe place.
- The edge **can** be split. An edge whose source is a jump through a table of addresses that cannot be changed, or an exception edge into a handler, may not allow a new block in the middle. Then the transformation must place its code another way.

## The template

```pseudo id=main
SPLIT-CRITICAL-EDGES(G)
L1  for each edge (a, b) of G do
L2      if a has two or more successors and b has two or more predecessors then
L3          create a new block c with no instructions and the terminator "jump b"
L4          in the terminator of a, replace the target b by c
L5          in each phi-function of b, give the operand for a to c instead
L6  return G
```

Line L2 tests the counts in the graph before any split. Splitting one edge does not change them for any other edge: $a$ keeps its number of successors, because $c$ takes the place of $b$, and $b$ keeps its number of predecessors, because $c$ takes the place of $a$. So the order of the loop does not matter, and one pass removes all critical edges. The new block $c$ has one predecessor and one successor, so no edge at $c$ is critical.

Line L5 matters for SSA programs. A phi-function names its operands by predecessor block, and after the split, $b$ receives that value from $c$, not from $a$.

The loop runs over each edge once and does constant work per edge, so it takes $O(n + m)$ time for $n$ blocks and $m$ edges, and it adds at most $m$ blocks. Paths in the old graph and the new graph correspond one to one, so dominance among the old blocks does not change, and the immediate dominator of each new block $c$ is $a$.

## Classic examples

**Out-of-SSA translation: the lost copy.** In this loop, `x.2` is the value before the increment and `x.3` the value after:

```
# params: n
B1:
  x.1 = 1
  jump B2
B2:
  x.2 = phi [B1: x.1, B2: x.3]
  x.3 = x.2 + 1
  t.1 = x.3 < n
  br t.1 B2 B3
B3:
  ret x.2
```

For $n = 3$ it returns 2. The phi-function must become the copy `x.2 = x.3` on the back edge from B2 to B2. That edge is critical: B2 has the successors B2 and B3, and the predecessors B1 and B2. The naive translation puts the copy at the end of B2, before the branch. Then the exit to B3 also runs it, and the program returns 3, because `x.2` was overwritten on the way out. After the split, the back edge goes through a new block B4:

```
B2:
  x.3 = x.2 + 1
  t.1 = x.3 < n
  br t.1 B4 B3
B4:
  x.2 = x.3
  jump B2
```

Now the copy runs only when the loop repeats, and the program returns 2 again. This is the lost copy problem; see [lost copy and swap problems](/lost-copy-and-swap-problems/).

**Lazy code motion.** Knoop, Rüthing and Steffen (1992) place computations at the earliest and then the latest safe points. A critical edge can block this: to make an expression available at a join, it must be computed on the edge from a branch, and no block exists there. Their algorithm assumes that all critical edges are split first, and the new blocks are where it inserts code.

**Register allocation.** An allocator that splits live ranges can keep a value in one register at the end of block $a$ and expect it in another at the start of block $b$. The fix is a move on the edge $(a, b)$. [Linear scan](/linear-scan-register-allocation/) allocators and SSA-based allocators put these resolution moves in the predecessor, in the successor, or in a new block when the edge is critical.

**Edge profiling.** A counter for an edge must run only on that edge. Instrumentation such as [Ball-Larus path profiling](/ball-larus-path-profiling/) adds code on edges, which needs a block on each critical edge that gets code.

## Variations

- **Split on demand.** Split only the critical edges that will receive code. Many critical edges never do, and each split adds a jump.
- **Place the code in the source when it is safe.** A copy `x = y` at the end of $a$ is harmless if $x$ is dead on every other exit of $a$. [Sreedhar's method](/sreedhar-cssa-translation/) and its later improvements use liveness and interference to avoid most splits during out-of-SSA translation.
- **Clean up after.** After the inserted code is in place, a block that is still empty is just a jump. A later pass that merges blocks and removes jumps to jumps takes it out.
- **Loop preheaders.** Code motion out of a loop needs a single block before the header. A preheader is the same idea for all the edges that enter a loop from outside.

## Pitfalls

- **Forgetting the phi-functions.** After a split, the phi-functions of $b$ still name $a$ as the predecessor. The program is then malformed: the operand key does not match any predecessor.
- **Duplicate edges.** A conditional branch with both targets equal, or a switch with several cases to the same block, gives one block two edges to the same target. Some IRs count these as two edges and some as one. Split each one consistently, and update each phi operand for the right edge.
- **Edges that cannot be split.** Exception edges, edges of computed jumps, and some edges in machine code cannot have a block in the middle. Code for such an edge needs another method, such as the extra copies of Sreedhar et al. that make every phi operand safe to copy in its predecessor.
- **Changing loop structure.** Splitting a back edge makes the new block the loop latch. Passes that look for the latch by its old label, or that assume the latch is the block with the branch, must be rerun or updated.
- **Code size and speed.** Each split adds a block and usually an unconditional jump. Split only where code will go, and merge empty blocks afterwards.

## Exercises

1. Prove that splitting one critical edge does not create a new critical edge, and that it does not change whether any other edge is critical.
2. Prove that dominance between old blocks is the same before and after the split, and that the immediate dominator of the new block is the source of the split edge.
3. Change the lost copy example so that B3 returns `x.3 - 1`. Then $x.2$ is dead on the exit from B2 to B3. Show that the copy at the end of B2 is now correct without a split, and explain why liveness on the other exits decides whether a copy can stay in the source block.

## References
