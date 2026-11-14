---
tag: A4Y5XS
kind: definition
slug: control-flow-graph
name: Control flow graph
aliases:
- flow graph of a procedure
area: compilers-and-program-analysis/intermediate-representations
level: intro
summary: A directed graph whose nodes are the basic blocks of a procedure and whose edges are the possible transfers of control between them.
prereqs: [basic-block, directed-graph]
see_also: [dominators-problem, depth-first-orders, natural-loop, reducible-flow-graph, post-dominance, critical-edge-splitting, dataflow-analysis, call-graph]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 8.4 (Basic Blocks and Flow Graphs), with 8.4.3 (flow graphs) and 8.4.5 (loops); Section 9.6 (Loops in Flow Graphs), with 9.6.1 (dominators) and 9.6.2 (depth-first ordering)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 4 (Intermediate Representations), the part on control flow graphs; Chapter 9 (data-flow analysis on the control flow graph)
  - book: isbn:1558603204
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 7 (Control-Flow Analysis), flow graphs, depth-first search, dominators and loops
  - paper: doi:10.1145/390013.808479
    title: Frances E. Allen, Control flow analysis, Proceedings of a Symposium on Compiler Optimization, SIGPLAN Notices 5(7), 1970
    locator: the definition of the control flow graph of a program, of dominance and of intervals
---

A control flow graph (CFG) is a directed graph that shows how control can move through one procedure. Its nodes are the [basic blocks](/basic-block/) of the procedure, and it has an edge from block $B$ to block $C$ if $C$ can run right after $B$. One node is the entry. Every run of the procedure follows a path of the graph from the entry, but some paths of the graph are never followed by any run. Almost every global analysis and optimization in a compiler, from [dataflow analysis](/dataflow-analysis/) to the construction of [static single assignment form](/static-single-assignment-form/), works on the control flow graph.

## Definition

### The graph

Let a procedure be cut into basic blocks $B_1, \ldots, B_n$, with $B_1$ the block that holds the first instruction. Its *control flow graph* is $G = (N, E, r)$ with

- $N = \{B_1, \ldots, B_n\}$,
- an edge $(B, C) \in E$ if the last instruction of $B$ is a jump or a branch with $C$ as a target, or if $C$ comes right after $B$ in the program text and the last instruction of $B$ is not an unconditional jump or a return (a fall-through),
- the *entry* $r = B_1$.

The *predecessors* of $C$ are the blocks $B$ with $(B, C) \in E$, and the *successors* of $B$ are the blocks $C$ with $(B, C) \in E$. A *path* is a sequence of blocks in which each consecutive pair is an edge. A block is *reachable* if there is a path from $r$ to it. Most analyses first delete the unreachable blocks, and many assume that $r$ has no predecessors; a compiler can add an empty entry block to make this true.

Many analyses also want one *exit*. If several blocks end in a return, or none does (the procedure loops forever), the compiler adds a new exit node with an edge from every returning block. Backward analyses and [post-dominance](/post-dominance/) start from it.

In the toy IR of this site the blocks are written out, so the successors come from the terminator alone: `jump L` gives one successor, `br a L1 L2` gives $L_1$ and $L_2$ (one edge if $L_1 = L_2$), and `ret a` gives none. The helper `toyir.py` has `succs(prog, L)`, `preds(prog)` and `edges(prog)` for this.

### Size

Each block of the toy IR has at most two successors, so $m \le 2n$ for $n$ blocks and $m$ edges, and $m = O(n)$. A `switch` lowered to a jump table can give one block many successors, so in general $m$ is not bounded by a constant times $n$, and costs on CFGs are stated in both $n$ and $m$.

### Paths and runs

The CFG over-approximates the runs. Every run of the procedure that starts at the entry visits a sequence of blocks that is a path of $G$ from $r$. The converse is false: a path of $G$ may be *infeasible*, because the conditions of its branches cannot all hold. Which paths are feasible is undecidable in general, by [Rice's theorem](/rice-theorem/), so analyses on the CFG treat every path as possible. This is why a must-analysis that is true on all paths of the CFG is sound, and why it can lose precision.

### Terms used with CFGs

- **Dominance.** $d$ dominates $v$ if every path from $r$ to $v$ contains $d$ ([dominators problem](/dominators-problem/), [dominator tree](/dominator-tree/)). Post-dominance is the same notion on the reversed graph from the exit.
- **Depth-first orders.** A depth-first search from $r$ gives preorder, postorder and reverse postorder numbers ([depth-first orders](/depth-first-orders/)). In reverse postorder, every edge that is not a retreating edge goes forward, so forward analyses visit most predecessors before a block.
- **Back edges and loops.** An edge $(t, h)$ is a back edge if $h$ dominates $t$; each back edge defines a [natural loop](/natural-loop/). A CFG in which every cycle has a back edge is [reducible](/reducible-flow-graph/).
- **Critical edge.** An edge from a block with several successors to a block with several predecessors. Code cannot be placed on it without [critical edge splitting](/critical-edge-splitting/).

## Examples and non-examples

### A loop with a branch inside

This toy IR program adds the odd numbers below $n$:

```
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

Its CFG has 6 nodes, the entry B1, and 7 edges:

$$B1 \to B2,\; B2 \to B3,\; B2 \to B6,\; B3 \to B4,\; B3 \to B5,\; B4 \to B5,\; B5 \to B2.$$

The predecessors are B2: {B1, B5}, B3: {B2}, B4: {B3}, B5: {B3, B4} and B6: {B2}. A depth-first search that tries successors in the order of the terminator visits B1, B2, B3, B4, B5 and then B6, so the postorder is B5, B4, B3, B6, B2, B1 and the reverse postorder is B1, B2, B6, B3, B4, B5. The only edge that goes backward in this order is B5 → B2. B2 dominates B5, so it is a back edge, and its natural loop is {B2, B3, B4, B5}. The edge B3 → B5 is critical: B3 has two successors and B5 has two predecessors. The immediate dominators are B1 for B2, B2 for B3 and B6, and B3 for B4 and B5.

The run on $n = 6$ follows the path B1, B2, B3, B5, B2, B3, B4, B5, B2, ..., B6 and returns 9.

### An infeasible path

```
B0:
  br a B1 B2
B1:
  x = 1
  jump B3
B2:
  x = 0
  jump B3
B3:
  br a B4 B5
B4:
  y = 10 / x
  ret y
B5:
  ret 0
```

The CFG has the path B0, B2, B3, B4, on which `10 / x` divides by 0. No run takes it, because both branches test the same `a`. An analysis that looks at all CFG paths reports a possible trap at B4 anyway. Path-sensitive analyses and [symbolic execution](/symbolic-execution/) can rule such paths out, at a higher cost.

### Variants

- **Instruction-level CFG.** Some tools use one node per instruction. The graph is larger, but every node has one instruction, which makes some analyses simpler to state. The blocks of the block-level CFG are the maximal chains of the instruction-level CFG.
- **CFG with exception edges.** In Java and C++ compilers, an instruction that can throw has an edge to the handler. Then a block can be left in the middle, or the blocks are cut after each throwing instruction.
- **Interprocedural CFG.** The CFGs of all procedures joined by call and return edges, used by interprocedural analyses; it needs the [call graph](/call-graph/) to know the targets.

### Non-examples

- The [call graph](/call-graph/) is a graph of procedures, not of blocks; its edges are calls, not transfers of control inside a procedure.
- An [abstract syntax tree](/abstract-syntax-tree/) shows the nesting of statements. Control flow can be derived from it, but its edges are parent-child links.
- A data dependence graph or a [program dependence graph](/program-dependence-graph/) has edges for the flow of values and for [control dependence](/control-dependence/), which is computed from the CFG but is a different relation.

### Pitfalls

- **Keeping unreachable blocks.** An unreachable block has no dominator in the usual sense, and its predecessors confuse many algorithms. Delete them, or skip them consistently.
- **Assuming one exit.** A procedure may have several returns or none. Add a virtual exit before a backward analysis or post-dominance, and decide what to do with infinite loops that cannot reach it.
- **Edges with the same ends.** `br a L L` is one edge in this site's convention. Some compilers keep two parallel edges; then the predecessor list of $L$ has $B$ twice, and phi-functions need one operand per edge.

## Related definitions

- [Basic block](/basic-block/): the nodes.
- [Dominators problem](/dominators-problem/), [Cooper-Harvey-Kennedy dominance](/cooper-harvey-kennedy-dominance/) and [post-dominance](/post-dominance/): the dominance relations on a CFG and how to compute them.
- [Natural loop](/natural-loop/), [reducible flow graph](/reducible-flow-graph/) and [loop nesting forest](/loop-nesting-forest/): the loop structure of a CFG.
- [Depth-first orders](/depth-first-orders/) and [DFS forest](/dfs-forest/): the orders in which iterative analyses visit the blocks.
- [Critical edge splitting](/critical-edge-splitting/): adding a block on each critical edge.
- [Call graph](/call-graph/): the graph one level up, whose nodes are procedures.

## References
