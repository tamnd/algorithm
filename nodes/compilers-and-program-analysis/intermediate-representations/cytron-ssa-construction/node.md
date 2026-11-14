---
tag: BVFDF2
kind: algorithm
slug: cytron-ssa-construction
name: Cytron SSA construction
aliases:
- Cytron et al. SSA construction
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: Builds minimal SSA form by placing phi-functions at the iterated dominance frontiers of each variable's definitions and renaming over the dominator tree.
solves: [ssa-construction-problem]
model: word-ram
complexity:
  vars: {I: the number of instructions, V: the number of variables, n: the number of blocks, m: the number of edges, D: the total size of the dominance frontiers}
  time: {worst: O(I + V (n + m + D)), average: O(I + V (n + m + D)), best: Θ(I + n + m + D)}
  space: {extra: O(I + V m + D)}
properties: {deterministic: true, recursive: true, online: false}
prereqs: [ssa-construction-problem, dominance-frontier-computation, dominator-tree]
see_also: [static-single-assignment-form, phi-function, dominance-frontier, pruned-ssa-form, braun-ssa-construction, cooper-harvey-kennedy-dominance, out-of-ssa-translation, lengauer-tarjan-algorithm]
sources:
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: the placement of phi-functions with a worklist over the dominance frontiers, the renaming pass with one stack per variable over the dominator tree, the proofs that the result is minimal and correct, and the cost analysis
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 19 (Static Single-Assignment Form), inserting phi-functions and renaming the variables
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 9 (Data-Flow Analysis), the section on static single-assignment form, with the placement of phi-functions and the renaming
  - book: isbn:9783030805142
    title: Fabrice Rastello and Florent Bouchez Tichadou (editors), SSA-based Compiler Design, Springer, 2022
    locator: Chapter 3 (Standard Construction and Destruction Algorithms), phi-function insertion and variable renaming
  - paper: "Preston Briggs, Keith D. Cooper, Timothy J. Harvey and L. Taylor Simpson, Practical improvements to the construction and destruction of static single assignment form, Software: Practice and Experience 28(8), 1998, pages 859-881"
    locator: semi-pruned SSA form as a cheaper input to the same algorithm
---

The Cytron SSA construction is the standard way to build [static single assignment form](/static-single-assignment-form/). It works in two passes over a [control flow graph](/control-flow-graph/) whose [dominator tree](/dominator-tree/) and [dominance frontiers](/dominance-frontier/) are known. The first pass decides where [phi-functions](/phi-function/) go: for each variable, at the iterated dominance frontier of the blocks that assign it. The second pass walks the dominator tree from the root and gives every definition a new name, with one stack of names per variable, so that each use gets the name of the nearest definition above it. Cytron, Ferrante, Rosen, Wegman and Zadeck published it in 1991 and proved that it places the fewest phi-functions that any correct placement needs. Almost every textbook teaches it.

## In plain words

First decide where merges are needed. A variable assigned in some block can meet other values of itself only at the edge of the region that block controls, so put a merge there. A merge is itself an assignment, so repeat from each new merge until nothing changes. Then walk the blocks from the top of the dominator tree down. Keep, for each variable, a stack of the names in force. A new assignment gets a fresh name, which goes on the stack. A read takes the name on top. At the end of each block, fill in the merges of the next blocks with the names in force. After a block and everything below it in the tree are done, pop the names it pushed, so its siblings see the old ones.

## The problem

The input is a procedure in three-address code with no phi-functions, and its control flow graph $G = (N, E, r)$. Every block is reachable and the entry $r$ has no predecessors. The output is the same procedure in minimal, strict SSA form, as defined on the [SSA construction](/ssa-construction-problem/) page: a phi-function for each variable $v$ exactly at the blocks of the iterated join set $J^+(S_v)$, where $S_v$ is the set of blocks that assign $v$ plus $r$, each definition with a new name, and each use renamed so that it reads the same value as before.

The algorithm needs the immediate dominators and the dominance frontiers. The implementation computes the first with the [Cooper-Harvey-Kennedy](/cooper-harvey-kennedy-dominance/) iteration and the second with the walk described on the [dominance frontier computation](/dominance-frontier-computation/) page.

## The algorithm

```pseudo id=main
CYTRON-SSA(G, r, idom, DF)
    // Part 1: where the phi-functions go
L1  for each variable v do Sites[v] <- {r}
L2  for each block b and each instruction in b that assigns v do add b to Sites[v]
L3  for each variable v do
L4      W <- Sites[v]
L5      while W is not empty do remove a block x from W
L6          for each y in DF[x] do
L7              if y has no phi-function for v then put "v = phi" at the top of y
L8                  if y was never in W then add y to W
    // Part 2: renaming
L9  for each parameter p do push p on Stack[p]
    RENAME(r)

L10 RENAME(b)
    for each phi-function "v = phi" at the top of b do
L11     replace v by a new name v.k; push v.k on Stack[v]
L12 for each other instruction "v = ... u ..." of b, in order do
        replace each use u by Top(u)
L13     replace v by a new name v.k; push v.k on Stack[v]
    replace each use u in the terminator of b by Top(u)
L14 for each successor s of b do
L15     for each phi-function for v in s do set its operand for the edge (b, s) to Top(v)
L16 for each child c of b in the dominator tree do RENAME(c)
L17 pop every name that b pushed in lines L11 and L13
```

`Top(v)` is the name on top of the stack of $v$. If the stack is empty, $v$ is a local variable read on a path where it has no value yet. Then `Top(v)` returns `v.0`, and the implementation puts `v.0 = 0` at the top of the entry block. This keeps the result strict: every name has a definition that dominates all its uses. The parameters keep their own names for their values on entry.

Lines L1 and L2 put $r$ in every site set, because the entry holds each variable's first value. Lines L4 to L8 are the worklist that computes $DF^+(S_v)$; the test in line L7 puts at most one phi-function for $v$ in each block, and the test in line L8 puts each block on the list at most once. Line L12 reads the uses before line L13 pushes the new name, so `i = i + 1` reads the old name of `i`. Lines L14 and L15 run after the whole block, so a phi operand gets the name in force at the end of the predecessor.

The phi-functions of a block are read in parallel, as one copy on the edge. Line L15 takes all their operands from the state at the end of $b$, not from the other phi-functions of $s$, so the order in which the phi-functions are written does not matter.

## Example

The program from the [control flow graph](/control-flow-graph/) page adds the odd numbers below $n$:

```
# params: n
B1:
  i = 0
  s = 0
  jump B2
B2:
  t1 = i < n
  br t1 B3 B6
B3:
  t2 = i % 2
  br t2 B4 B5
B4:
  s = s + i
  jump B5
B5:
  i = i + 1
  jump B2
B6:
  ret s
```

**Part 1.** The frontiers are $DF(B2) = DF(B3) = DF(B5) = \{B2\}$, $DF(B4) = \{B5\}$, and the others are empty. The sites are `i`: {B1, B5}, `s`: {B1, B4}, `t1`: {B1, B2}, `t2`: {B1, B3} and `n`: {B1}. For `s`, the worklist takes B4 and puts a phi-function at B5, takes B5 and puts one at B2, and takes B2, whose frontier B2 already has one. For `i`, `t1` and `t2` it puts one at B2. So B2 gets four phi-functions and B5 gets one.

**Part 2.** The dominator tree is B1 → B2 → {B3, B6}, B3 → {B4, B5}. The walk visits B1, B2, B3, B4, B5 and B6.

- B1 pushes `i.1` and `s.1`. At the edge to B2, the stacks of `t1` and `t2` are empty, so those operands become `t1.0` and `t2.0`.
- B2 pushes the phi names `i.2`, `s.2`, `t1.1`, `t2.1`, then `t1.2` for `t1 = i < n`, which reads `i.2`.
- B3 pushes `t2.2`. At the edge to B5, the operand of `s` becomes `s.2`.
- B4 pushes `s.3` for `s = s + i`, which reads `s.2` and `i.2`. At the edge to B5, the operand becomes `s.3`. B4 pops `s.3`.
- B5 pushes the phi name `s.4` and `i.3`. At the edge to B2, the operands become `i.3`, `s.4`, `t1.2` and `t2.2`. B5 pops its names.
- B3 pops `t2.2`. B6 returns `s.2`, the name on top of the stack of `s` after B2.

The result is:

```
# params: n
B1:
  t1.0 = 0
  t2.0 = 0
  i.1 = 0
  s.1 = 0
  jump B2
B2:
  i.2 = phi [B1: i.1, B5: i.3]
  s.2 = phi [B1: s.1, B5: s.4]
  t1.1 = phi [B1: t1.0, B5: t1.2]
  t2.1 = phi [B1: t2.0, B5: t2.2]
  t1.2 = i.2 < n
  br t1.2 B3 B6
B3:
  t2.2 = i.2 % 2
  br t2.2 B4 B5
B4:
  s.3 = s.2 + i.2
  jump B5
B5:
  s.4 = phi [B3: s.2, B4: s.3]
  i.3 = i.2 + 1
  jump B2
B6:
  ret s.2
```

On $n = 6$ it returns 9, and on $n = 10$ it returns 25, the same as the input. The phi-functions for `t1` and `t2` are minimal but dead. [Pruned SSA form](/pruned-ssa-form/) would leave them out.

## Correctness

The proof file gives the full proof in two parts.

**Placement.** A phi-function for $v$ is needed at $y$ when two definitions of $v$ reach $y$ along paths that meet first at $y$; this set, closed under the new phi-functions, is $J^+(S_v)$. The proof shows $J^+(S_v) = DF^+(S_v)$. One direction: if $y \in DF(x)$, a path from $x$ that stays in the region $x$ dominates and a path from $r$ that avoids $x$ meet first at $y$. The other direction: follow a path from a definition to $y$ and track the deepest definition block that dominates the current node. It changes only at blocks of $DF^+(S_v)$, so if $y$ is not one of them, both paths into $y$ come from definitions that strictly dominate $y$, and one of the two paths then avoids a node that dominates $y$, which is impossible.

**Renaming.** For each point $q$ of the program, let $dd(q)$ be the nearest definition of $v$, phi-functions included, that dominates $q$. Along any path, crossing an edge into a block with no phi-function for $v$ does not change $dd$, because a change would put the block in the dominance frontier of a definition block. So in every run, the last definition of $v$ executed before $q$ is $dd(q)$. The stacks hold exactly the definitions on the dominator tree path above $q$, so `Top(v)` is $dd(q)$. Hence every use reads the value it read before, every name is defined once, and every definition dominates its uses. The same argument shows that two versions of one variable are never live at the same point, so the output is conventional SSA.

## Complexity

Let $I$ be the number of instructions, $V$ the number of variables, $n$ and $m$ the numbers of blocks and edges, and $D$ the total size of the dominance frontiers.

- **Dominance.** The immediate dominators take $O(m \log n)$ time with [Lengauer-Tarjan](/lengauer-tarjan-algorithm/), or a few passes of the Cooper-Harvey-Kennedy iteration in practice. The frontiers take $\Theta(n + m + D)$.
- **Placement.** For one variable, the worklist takes each block of $S_v \cup DF^+(S_v)$ once and reads its frontier once, which is $O(n + D)$. Over all variables this is $O(I + V(n + D))$.
- **Renaming.** Each instruction, each phi-function and each phi operand is handled once. The output has at most $V$ phi-functions per block, so this is $O(I + V m)$.

The total after the dominator tree is $O(I + V(n + m + D))$. $D$ can be $\Theta(n^2)$, and the output itself can have $\Theta(n^2)$ phi-functions, as the nested repeat-until loops on the [dominance frontier](/dominance-frontier/) page show. Cytron et al. found both to grow about linearly on real programs. The extra space is the frontiers, the stacks and the output.

## Properties

- **Minimal.** It places phi-functions at exactly $J^+(S_v)$ for each variable, on any control flow graph, reducible or not.
- **Not pruned.** It can place dead phi-functions, such as those for `t1` and `t2` in the example.
- **Strict and conventional.** With the entry definitions, every definition dominates its uses, and the versions of one variable never interfere. So, before any optimization, out-of-SSA translation can just drop the version numbers.
- **Needs the whole graph.** The graph must be complete before the dominator tree can be built.
- **Recursive.** RENAME recurses on the dominator tree. A deep tree needs an explicit stack in production code.

## Variants and improvements

- **Pruned SSA.** Compute [liveness](/live-variable-analysis/) first and skip a phi-function for $v$ at $y$ if $v$ is not live on entry to $y$. See [pruned SSA form](/pruned-ssa-form/).
- **Semi-pruned SSA.** Briggs, Cooper, Harvey and Simpson (1998) skip the variables that are never live across a block boundary. It needs no full liveness pass and removes most of the dead phi-functions.
- **Linear-time placement.** Sreedhar and Gao (1995) compute $DF^+(S_v)$ on the DJ-graph in $O(n + m)$ per variable, without the frontiers.
- **On-demand construction.** [Braun et al.](/braun-ssa-construction/) (2013) build SSA form during translation from the syntax tree, with no dominance information.
- **Copy folding during renaming.** For a copy `x = y`, push the name of `y` on the stack of `x` and drop the copy. This saves a pass, but the output is then no longer conventional, and [out-of-SSA translation](/out-of-ssa-translation/) must handle the [lost copy and swap problems](/lost-copy-and-swap-problems/).

## When to use it

Use it when the whole control flow graph is available and the dominator tree is needed anyway, which is the case in most optimizing compilers. It is the reference method: it is easy to prove correct and it gives the minimal placement on any graph. If the graph is not built yet, or the compiler wants to avoid the dominance passes, Braun's method is simpler. If the frontiers may be large, use DJ-graphs for the placement.

## Pitfalls

- **Missing entry definitions.** A variable read on some path before it is assigned has no name on that path. Without `v.0` at the entry, the phi operand is empty and the result is not strict.
- **Reading phi-functions one by one.** All phi-functions of a block take their operands from the end of the predecessor. Filling an operand with the name of another phi-function of the same block is wrong.
- **Popping too early or too late.** The names pushed by a block must stay on the stacks while its dominator subtree is renamed and must be gone before its siblings are. Popping at the end of the block body, before the children, gives the children wrong names.
- **Edges into the entry.** If the entry has a predecessor, it may need phi-functions, and the first entry has no incoming edge to choose an operand. Add a new empty entry block first.
- **Unreachable blocks.** They have no immediate dominator. Delete them first.
- **Assuming the output is pruned.** It is minimal, not pruned. Later passes must expect dead phi-functions, or the compiler must prune.

## Implementations

## History

Rosen, Wegman and Zadeck introduced phi-functions for global value numbering in 1988. Cytron, Ferrante, Rosen, Wegman and Zadeck gave the efficient construction through dominance frontiers at POPL 1989, and the full version with proofs and the control dependence graph in TOPLAS in 1991. The method made SSA form practical, and research and production compilers took it up; GCC, for example, places its phi-functions with dominance frontiers. Briggs et al. (1998) made it cheaper with semi-pruned SSA, and Sreedhar and Gao (1995) gave a linear-time placement.

## References
