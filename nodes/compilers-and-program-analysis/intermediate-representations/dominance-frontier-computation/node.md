---
tag: VKF111
kind: algorithm
slug: dominance-frontier-computation
name: Dominance frontier computation
aliases:
- Cytron dominance frontier algorithm
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: Computes all dominance frontiers in time linear in their total size by a bottom-up walk of the dominator tree.
model: word-ram
complexity:
  vars: {n: the number of reachable nodes, m: the number of edges, D: the total size of all dominance frontiers}
  time: {worst: Θ(n + m + D), average: Θ(n + m + D), best: Θ(n + m + D)}
  space: {extra: Θ(n + D)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [dominance-frontier, dominator-tree]
see_also: [cooper-harvey-kennedy-dominance, lengauer-tarjan-algorithm, cytron-ssa-construction, static-single-assignment-form, control-dependence, post-dominance, ssa-construction-problem, pruned-ssa-form]
sources:
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: the definition of DF_local and DF_up, the lemmas that give DF from them, the bottom-up algorithm over the dominator tree, and its cost in the size of the frontiers
  - url: "https://hdl.handle.net/1911/96345"
    title: Keith D. Cooper, Timothy J. Harvey and Ken Kennedy, A simple, fast dominance algorithm, technical report, Department of Computer Science, Rice University
    locator: the dominance frontier algorithm that walks from each predecessor of a join node up to its immediate dominator
  - paper: doi:10.1145/199448.199464
    title: Vugranam C. Sreedhar and Guang R. Gao, A linear time algorithm for placing phi-nodes, Proceedings of the 22nd ACM Symposium on Principles of Programming Languages (POPL), 1995, pages 62-73
    locator: DJ-graphs, and the iterated dominance frontier in linear time without computing the frontiers
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 19 (Static Single-Assignment Form), the computation of the dominance frontier by DF_local and DF_up
  - book: isbn:9783030805142
    title: Fabrice Rastello and Florent Bouchez Tichadou (editors), SSA-based Compiler Design, Springer, 2022
    locator: Chapter 3 (Standard Construction and Destruction Algorithms), the computation of dominance frontiers; Chapter 4 (Advanced Construction Algorithms for SSA), DJ-graphs and merge sets
---

Dominance frontier computation finds the [dominance frontier](/dominance-frontier/) of every node of a flow graph, given its [dominator tree](/dominator-tree/). The method of Cytron, Ferrante, Rosen, Wegman and Zadeck (1991) visits the tree bottom up. The frontier of a node is made from the edges that leave it directly, plus the frontiers of its children that also escape the node itself. The cost is linear in the size of the graph plus the total size of the frontiers, which is the size of the output. Cooper, Harvey and Kennedy later gave a shorter method that walks up the tree from the predecessors of each join node. This page covers both. The frontiers tell [Cytron SSA construction](/cytron-ssa-construction/) where to put phi-functions.

## In plain words

A block "owns" every block it dominates: control cannot get there without passing through it. The frontier of a block is the set of blocks just outside its land, the first blocks that can also be reached by a road that skips it. To find them all, start from the deepest blocks of the dominator tree. Each block looks at its own outgoing edges and keeps the targets it does not own. Then it looks at what its children reported, and keeps the blocks it does not own either. A parent never has to look below its children, because they already did that work. The other method starts at each meeting point and climbs the tree from each incoming edge, marking every block it passes, until it reaches the block that owns the meeting point.

## The problem

The input is a flow graph $G = (N, E, r)$ with root $r$ and the immediate dominator $\mathrm{idom}(y)$ of each node $y \ne r$ that $r$ reaches. Nodes that $r$ does not reach are ignored. The output is, for each reachable node $x$,

$$DF(x) = \{\, y : \exists\, (p, y) \in E,\ x \operatorname{dom} p,\ \text{not } x \operatorname{sdom} y \,\}.$$

Often the next step is the iterated frontier $DF^+(S)$ of a set $S$ of blocks, which is where the phi-functions for one variable go.

The two methods rest on two forms of the definition, both proved on the [dominance frontier](/dominance-frontier/) page and in the proof file. The bottom-up form is

$$DF(x) = \{y \in \mathrm{succ}(x) : \mathrm{idom}(y) \ne x\} \;\cup \bigcup_{\mathrm{idom}(z) = x} \{y \in DF(z) : \mathrm{idom}(y) \ne x\}.$$

Cytron et al. call the first part $DF_{\text{local}}(x)$ and the parts that come from the children $DF_{\text{up}}(z)$. The edge form says that $y \in DF(x)$ if and only if $x$ lies on the tree path from some predecessor $p$ of $y$ up to $\mathrm{idom}(y)$, with $\mathrm{idom}(y)$ itself excluded.

## The algorithm

```pseudo id=main
DOMINANCE-FRONTIERS(G, r, idom)
L1  for each node x, in a postorder of the dominator tree do
L2      DF[x] <- empty set
L3      for each successor y of x do
L4          if idom(y) != x then add y to DF[x]
L5      for each child z of x in the dominator tree do
L6          for each y in DF[z] do
L7              if idom(y) != x then add y to DF[x]
L8  return DF

DOMINANCE-FRONTIERS-WALK(G, r, idom)
L9  for each node y with two or more predecessors, and for y = r do
L10     for each predecessor p of y do
L11         runner <- p
L12         while runner != idom(y) and y is not in DF[runner] do
L13             add y to DF[runner]
L14             runner <- idom(runner)
```

The first routine is Cytron's. The postorder of line L1 makes sure that the children of $x$ are finished before $x$, so line L6 reads their final frontiers. Line L4 adds $DF_{\text{local}}(x)$ and line L7 adds $DF_{\text{up}}$ of each child. The test in both lines is the same: a node whose immediate dominator is $x$ is strictly dominated by $x$, and every other candidate is not.

The second routine is the walk of Cooper, Harvey and Kennedy. A node with one predecessor $p$ has $\mathrm{idom}(y) = p$, so its walk would be empty, and line L9 skips it. The root is the one exception: it can have a single predecessor through a back edge, and nothing strictly dominates it, so $\mathrm{idom}(r)$ is None and the walk goes all the way up. The second test of line L12 is an early stop. If $y$ is already in $DF[\text{runner}]$, an earlier walk for the same $y$ passed here and went on up to $\mathrm{idom}(y)$, so the rest of the path is done.

In the implementation, the immediate dominators come from the [Cooper-Harvey-Kennedy](/cooper-harvey-kennedy-dominance/) iteration, with `idom[root] = None`. The routine `program_frontiers` runs the first method on the blocks of a toy IR program, and `iterated_dominance_frontier` computes $DF^+(S)$ with a worklist.

## Example

Take the program from the [control flow graph](/control-flow-graph/) page that adds the odd numbers below $n$. Its edges are B1 → B2, B2 → B3, B2 → B6, B3 → B4, B3 → B5, B4 → B5 and B5 → B2. The dominator tree has B1 → B2, B2 → B3, B2 → B6, B3 → B4 and B3 → B5. A postorder of the tree is B4, B5, B3, B6, B2, B1.

| step | x | local part (L3, L4) | from children (L5 to L7) | DF[x] |
|---|---|---|---|---|
| 1 | B4 | B5: idom is B3, keep | none | {B5} |
| 2 | B5 | B2: idom is B1, keep | none | {B2} |
| 3 | B3 | B4, B5: idom is B3, drop | B5 from B4: idom is B3, drop. B2 from B5: keep | {B2} |
| 4 | B6 | no successors | none | ∅ |
| 5 | B2 | B3, B6: idom is B2, drop | B2 from B3: idom is B1, keep | {B2} |
| 6 | B1 | B2: idom is B1, drop | B2 from B2: idom is B1, drop | ∅ |

Step 3 shows why the test matters. B4 reports B5, but B3 dominates B5, so for B3 that is not a frontier node. Step 5 shows a node in its own frontier: the back edge B5 → B2 escapes the land of B2 by entering B2 itself, which B2 does not strictly dominate.

The walk gives the same sets. The join nodes are B2, with predecessors B1 and B5, and B5, with predecessors B3 and B4. For B2, the walk from B1 stops at once, since B1 = idom(B2). The walk from B5 adds B2 to the frontiers of B5, B3 and B2, and stops at B1. For B5, the walk from B3 stops at once, and the walk from B4 adds B5 to $DF[B4]$ and stops at B3.

The variable `s` is assigned in B1 and B4. The worklist for $DF^+(\{B1, B4\})$ takes B4 and finds B5, then takes B5 and finds B2, then takes B2 and finds B2 again. The result is {B2, B5}, the two blocks that get a phi-function for `s`.

## Correctness

The proof file proves four facts. First, for an edge $(p, y)$ with $y \ne r$, $\mathrm{idom}(y)$ dominates $p$: a path to $p$ that avoids it, plus the edge, would reach $y$ without it. So the nodes that dominate $p$ form a chain that contains $\mathrm{idom}(y)$, and the ones that do not strictly dominate $y$ are those below $\mathrm{idom}(y)$. This gives the edge form. Second, splitting the walk from $p$ at $x$ gives the bottom-up form: either $p = x$, which is the local part, or the walk passes the child $z$ of $x$ first, which puts $y$ in $DF(z)$. Third, the postorder of line L1 makes the bottom-up form an induction, so the first routine is correct, and the walk adds $y$ to exactly the nodes of the edge form, so the second one is correct too. The early stop skips only nodes that already hold $y$. Fourth, the worklist for $DF^+(S)$ returns the least set that contains $DF(S)$ and is closed under $DF$.

## Complexity

Let $n$ be the number of reachable nodes, $m$ the number of edges and $D = \sum_x |DF(x)|$.

- **The bottom-up pass.** Each node is visited once, each edge is tested once at line L4, and each element of $DF(z)$ is tested once, at the parent of $z$. With a set that tests and adds in constant time, the time is $\Theta(n + m + D)$.
- **The walk.** Because of the early stop, every pass through line L13 adds a new pair, so there are at most $D$ of them. Each predecessor costs $O(1)$ more to stop its walk. The time is $O(n + m + D)$. Without the early stop, two walks for the same $y$ can climb the same part of the tree, and the cost grows with the in-degree of $y$ times its number of frontier entries.
- **Space.** The frontiers take $\Theta(D)$ and the tree takes $\Theta(n)$.

$D$ itself can be $\Theta(n^2)$. For $k$ nested repeat-until loops the graph has $2k + 1$ nodes and $3k$ edges, and $D = k(k + 1)$; the [dominance frontier](/dominance-frontier/) page works this out. On real programs Cytron et al. found $D$ to grow about linearly with $n$. Sreedhar and Gao avoid the quadratic case: their DJ-graph method finds $DF^+(S)$ in $O(n + m)$ time for each set $S$, without computing $D$.

## Properties

- **Output sensitive.** The time is linear in the input plus the output, so neither method can be beaten by more than a constant factor when all frontiers are wanted.
- **Needs only the tree and the edges.** Both methods read the immediate dominators and the successor or predecessor lists, nothing else.
- **Works on any flow graph.** Reducible or not, with or without edges into the root.
- **Local to join nodes.** Only nodes with two or more predecessors (and the root) appear in a frontier, so the walk does no work for the other nodes.

## Variants and improvements

- **Post-dominance frontiers.** Run the same code on the reverse graph, with the [post-dominator](/post-dominance/) tree. The result gives [control dependence](/control-dependence/): $y$ is control dependent on $x$ if $x$ is in the post-dominance frontier of $y$.
- **Iterated frontiers on demand.** Placing phi-functions needs only $DF^+(S)$ for one set at a time. Sreedhar and Gao's DJ-graphs, and the merge sets of chapter 4 of the SSA book, compute it directly in linear time per set.
- **Bit vectors.** For small graphs, each $DF[x]$ can be a bit vector, and line L7 becomes a masked union.
- **No frontiers at all.** [Braun SSA construction](/braun-ssa-construction/) builds SSA form with no dominance information.

## When to use it

Use the walk when the dominator tree comes from the [Cooper-Harvey-Kennedy](/cooper-harvey-kennedy-dominance/) or [Lengauer-Tarjan](/lengauer-tarjan-algorithm/) algorithm and the frontiers are needed for many variables. It is the shortest code and is easy to get right. Use the bottom-up pass when the tree is already walked in postorder for other reasons. If the graph is large and has deep nests of loops, so that $D$ may grow quadratically, compute $DF^+$ per variable instead.

## Pitfalls

- **Edges into the root.** If the root has a predecessor, it is in some frontiers. Treat $\mathrm{idom}(r)$ as None, and do not skip the root in line L9 just because it has one predecessor. The toy IR avoids the case by giving the entry no predecessors.
- **Unreachable blocks.** A block that the root does not reach has no immediate dominator. Delete it or skip it, and skip its edges.
- **Strict versus plain dominance.** A node can be in its own frontier. Testing "$x$ dominates $y$" in place of "$x$ strictly dominates $y$" loses the loop headers, and the loops then get no phi-functions.
- **Stale frontiers.** Splitting an edge or deleting a block changes the frontiers. Recompute them, or update them with care, after the graph changes.
- **Parallel edges.** If a block has two edges to $y$, the walk runs twice from it. The early stop makes this harmless.

## Implementations

## History

Cytron, Ferrante, Rosen, Wegman and Zadeck defined the dominance frontier and gave the bottom-up algorithm in their POPL 1989 paper on computing SSA form, and in full in the 1991 TOPLAS paper, which also used the reverse graph for control dependence. Sreedhar and Gao (1995) showed that the iterated frontier can be found in linear time with DJ-graphs. Cooper, Harvey and Kennedy published the walk from the predecessors with their simple iterative dominator algorithm, at Rice University in 2001, and it became a common choice in textbooks and compilers.

## References
