---
tag: Q4NRFR
kind: data-structure
slug: sea-of-nodes
name: Sea of nodes
aliases:
- Click graph IR
area: compilers-and-program-analysis/intermediate-representations
level: advanced
summary: A graph IR in SSA where data and control are both edges and most instructions float free of blocks until scheduling.
model: word-ram
complexity:
  vars: {n: the number of instructions, b: the number of blocks, v: the number of variables, g: the number of nodes and edges of the graph}
  time: {build: O(n + b v) expected, schedule: O(g b)}
  space: {total: O(g)}
history:
  year: 1995
  people: [Cliff Click, Michael Paleczny]
  note: Click and Paleczny described the graph at the IR'95 workshop, and Click gave global code motion for it at PLDI 1995. The HotSpot server compiler and the V8 compiler TurboFan used it in production.
prereqs: [static-single-assignment-form, phi-function, control-flow-graph, dominator-tree, hash-consing]
see_also: [program-dependence-graph, global-value-numbering, loop-invariant-code-motion, partial-redundancy-elimination, braun-ssa-construction, instruction-scheduling-problem, just-in-time-compilation, e-graph]
sources:
  - paper: doi:10.1145/202529.202534
    title: Cliff Click and Michael Paleczny, A simple graph-based intermediate representation, ACM SIGPLAN Workshop on Intermediate Representations (IR'95), 1995, pages 35-49
    locator: the graph with control and data edges, Region, If and Phi nodes, projections, and the building of the graph from the parser with value numbering
  - paper: doi:10.1145/207110.207154
    title: Cliff Click, Global code motion, global value numbering, PLDI 1995, pages 246-257
    locator: schedule early, schedule late at the lowest common ancestor of the uses, and the choice of the block of least loop depth between them
  - url: "https://hdl.handle.net/1911/16807"
    title: Cliff Click, Combining analyses, combining optimizations, PhD thesis, Rice University, 1995
    locator: the intermediate representation used for the combined analyses
  - url: "https://www.usenix.org/legacy/events/jvm01/full_papers/paleczny/paleczny.pdf"
    title: Michael Paleczny, Christopher Vick and Cliff Click, The Java HotSpot server compiler, USENIX Java Virtual Machine Research and Technology Symposium (JVM'01), 2001
    locator: Section 3, the SSA graph IR with RegionNode and PhiNode based on Click and Paleczny; Section 10, global code motion on the sea of nodes
  - url: "https://v8.dev/blog/leaving-the-sea-of-nodes"
    title: V8 team, Land ahoy, leaving the Sea of Nodes, V8 blog, 2025
    locator: why TurboFan used the sea of nodes, the problems seen in practice, and its replacement by the CFG-based Turboshaft
---

The sea of nodes is a graph IR in [static single assignment form](/static-single-assignment-form/) in which control and data are both edges, and there are no basic blocks. Each value is one node, and its inputs are the nodes it reads. Branches, merges and returns are nodes too, joined by control edges. An arithmetic node that cannot trap has no control input at all: it floats, and the compiler decides only at the end which block computes it. Cliff Click and Michael Paleczny (1995) described it, sometimes called the Click graph IR, and it was the IR of the HotSpot server compiler and of the TurboFan compiler of V8. Because the graph keeps only real dependences, [global value numbering](/global-value-numbering/) is [hash-consing](/hash-consing/) of nodes, and loop-invariant code motion falls out of the final scheduling.

## In plain words

A normal compiler keeps the program as a list of steps inside boxes, and each step has its place in a box. In the sea of nodes, the boxes are gone for most steps. A step only remembers which other steps it needs. Steps that decide which way the program goes, and steps that can fail, such as a division, keep a link to the decision above them. All other steps float. Two steps that compute the same thing from the same inputs become one step. At the end, the compiler puts every floating step back into a box: not earlier than its inputs allow, not later than its users need, and outside loops when it can.

## The abstract type

The graph has nodes with an ordered list of inputs. The edges point from a node to its inputs, the reverse of data flow, as in Click and Paleczny. There are two classes of nodes.

**Control nodes.** START begins the procedure. A REGION node stands for a merge point, with one input for each incoming control edge. IF takes a control input and a condition, and its two projections IFTRUE and IFFALSE are the control on each outgoing edge. RETURN takes a control input and a value. The control nodes form the [control flow graph](/control-flow-graph/), with REGION nodes as blocks.

**Data nodes.** PARAM and CONST are leaves. OP applies an operator to two inputs. PHI has a REGION as input 0 and one value for each input of that REGION, in the same order, as a [phi-function](/phi-function/). An OP that can trap, such as a division, has its REGION as an extra control input, so it is pinned to that block. Other OPs have no control input and float.

The operations are:

- BUILD(procedure): make the graph from a CFG or straight from the parser.
- New nodes with value numbering: making an OP that already exists returns the old node.
- Local rewrites on the graph, such as constant folding, by replacing a node with another in all its uses.
- SCHEDULE(): place every live floating node in a block and give back a CFG in SSA form.

Real compilers add a memory or effect input to loads, stores and calls, so that the order of memory operations is an edge as well. The toy version here has no memory.

## Representation

A node is an object with a kind, a value (the operator, the constant or the parameter name) and an array of input nodes. Use lists, from a node to the nodes that read it, are kept as well, or rebuilt before scheduling. A hash table maps the key (kind, value, input ids) to the node with that key, for CONST and floating OP. The pinned nodes are never put in this table, since two divisions in different blocks are different events. A list of roots holds the nodes that must stay even with no use: RETURN, IF and the pinned OPs. A node is live if a root reaches it through input edges.

## Operations

```pseudo id=main
BUILD(P)                       ▷ P: blocks of const, copy, op; the entry has no predecessor
L1  START ← new node; for each block B: region[B] ← new REGION
L2  for each block B in reverse postorder do
L3      if B is the entry: map ← {each parameter p: PARAM(p), other names: UNDEF}
L4      else if B has one predecessor P: map ← a copy of out[P]
L5      else map ← {each name v: a new PHI(region[B])}
L6      for each instruction x = a op b of B do       ▷ x = a and x = k only change map[x]
L7          if op can trap: n ← new OP(op, region[B], map[a], map[b]); add n to the roots
L8          else n ← HASHCONS(OP(op, map[a], map[b]))
L9          map[x] ← n
L10     end B with RETURN(region[B], map[a]), with IF(region[B], map[a]) and its two projections, or with nothing for a jump
L11     out[B] ← map
L12 for each block B except the entry do
L13     region[B].inputs ← the control of the edges P1 → B, ..., Pk → B
L14     for each PHI of v at B: its inputs ← region[B], out[P1][v], ..., out[Pk][v]
L15 replace each PHI whose inputs other than itself are one node w by w, until none is left

SCHEDULE()
L16 dominator tree and loop depth of the blocks (the REGION nodes)
L17 for each live pinned node n: block[n] ← the block of its control input
L18 for each live floating node n, inputs first: early[n] ← the deepest block among the blocks of its inputs, or the entry
L19 for each live floating node n, uses first:
L20     lca ← none
L21     for each use u of n: lca ← LCA(lca, the block of u), where a PHI u that reads n through its input i counts in the i-th predecessor of its block
L22     best ← lca; walk x from lca up the dominator tree to early[n]: if depth(x) < depth(best) then best ← x
L23     block[n] ← best
L24 for each block: emit its PHIs, then its OPs with inputs first, then its terminator
```

**BUILD (L1 to L15).** This is the construction of Click and Paleczny with one simplification: every block with two or more predecessors gets a PHI for every name (line L5), and line L15 removes the PHIs that turn out to be copies, as in [Braun et al.](/braun-ssa-construction/). A block with one predecessor needs no PHI, because its predecessor dominates it. The reverse postorder of line L2 visits that predecessor first, since a block whose only predecessor comes later would be unreachable. Line L8 is [hash-consing](/hash-consing/): the second `a + b` returns the node of the first. This is global value numbering, done once at creation, with no data flow analysis. Copies and constants make no node of their own, so copy propagation is free.

**SCHEDULE (L16 to L24).** This is global code motion as Click (1995) gave it. Line L18 computes the earliest legal block: a node must come after its inputs, and the blocks of the inputs all lie on one path of the [dominator tree](/dominator-tree/), so the deepest of them is the earliest. Line L21 computes the latest legal block: it must dominate every use, so it is the lowest common ancestor of the use blocks. A PHI reads its $i$-th input at the end of its $i$-th predecessor, so that is where the use counts. Line L22 picks, on the dominator tree path from the latest block up to the earliest one, a block of least loop depth. Ties go to the lower block, which runs on fewer paths. Line L24 writes a CFG in SSA form, with the pinned nodes in their own blocks.

## Example

Take this loop, where `k = n * 4` does not change inside the loop:

```
B1:
  i = 0
  s = 0
  jump B2
B2:
  t1 = i < n
  br t1 B3 B4
B3:
  k = n * 4
  s = s + k
  i = i + 1
  jump B2
B4:
  ret s
```

BUILD makes four REGIONs. B2 has two predecessors, so it gets a PHI for each of `i`, `k`, `n`, `s` and `t1`. The PHI of `n` has the inputs PARAM(n) and itself, so line L15 removes it and its uses read PARAM(n) directly. The PHIs of `k` and `t1` stay in the graph, but no root reaches them, so they are dead. The live data nodes are:

| node | inputs | pinned? | early | latest (LCA of uses) | placed in |
|---|---|---|---|---|---|
| $\phi_i$ | REGION(B2), 0, $i_1$ | yes | B2 | | B2 |
| $\phi_s$ | REGION(B2), 0, $s_1$ | yes | B2 | | B2 |
| $c$ = $\phi_i$ < n | $\phi_i$, PARAM(n) | no | B2 | B2 (the IF) | B2 |
| $k$ = n * 4 | PARAM(n), 4 | no | B1 | B3 | B1 |
| $s_1$ = $\phi_s$ + $k$ | $\phi_s$, $k$ | no | B2 | B3 (PHI input from B3) | B3 |
| $i_1$ = $\phi_i$ + 1 | $\phi_i$, 1 | no | B2 | B3 (PHI input from B3) | B3 |

The loop body is $\{B2, B3\}$, with loop depth 1. For $k$, the walk from B3 up to B1 passes B3 (depth 1), B2 (depth 1) and B1 (depth 0), so $k$ goes to B1: the multiply has left the loop, with no separate [loop-invariant code motion](/loop-invariant-code-motion/) pass. For $s_1$ and $i_1$ the walk stops at B2, of the same depth as B3, so they stay in B3. The output, with the node numbers as names, is:

```
B1:
  v19 = n * 4
  jump B2
B2:
  v8 = phi [B1: 0, B3: v22]
  v11 = phi [B1: 0, B3: v20]
  v13 = v8 < n
  br v13 B3 B4
B3:
  v20 = v11 + v19
  v22 = v8 + 1
  jump B2
B4:
  ret v11
```

The multiply now runs once even when the loop runs zero times. That is safe because it cannot trap. A division would be pinned to B3 and stay there.

**Value numbering across branches.** In `B1: br c B2 B3`, `B2: x = a + b`, `B3: y = a + b; x = y * 2`, `B4: ret x`, both additions become one node. Its uses are in B3 and in the PHI of B4 through the edge from B2, so the latest block is the common dominator B1, and the addition is computed once in B1. A CFG compiler would need [partial redundancy elimination](/partial-redundancy-elimination/) or code hoisting for the same result.

## Correctness

There are two claims. First, BUILD keeps the meaning: for every run of the source program, and at every point of it, the value of each variable equals the value of the node that the map of line L3 to L9 assigns to it, where a PHI takes the value of its input for the last edge into its block. This holds by induction over the run, and the key point is that hash-consing only merges nodes with the same operator and the same inputs, which have the same value at every moment. Second, SCHEDULE keeps the meaning: every node is placed in a block that is dominated by the blocks of its inputs and that dominates its uses, so the output is in strict SSA form, and in strict SSA each read sees the latest computation of the node, which was made from the latest values of its inputs. Control and the pinned nodes keep their blocks, so the output takes the same branches and traps in the same blocks as the source. The full argument is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

The model is the word RAM, and the unit step is one node operation or one expected-constant-time hash table operation. Let $n$ be the number of instructions, $b$ the number of blocks, $v$ the number of variables and $g$ the number of nodes plus edges.

- **BUILD.** The maximal PHIs make $O(b v)$ nodes, and each instruction makes at most one node, so lines L1 to L14 take $O(n + b v)$ expected time. Building from the parser with PHIs only where needed, as production compilers do, makes far fewer PHIs. Line L15, done with use lists and a worklist of PHIs whose inputs changed, costs $O(g)$ per round of removals.
- **SCHEDULE.** Dominators of the $b$ blocks cost $O(b \alpha(b, b))$ with the [Lengauer-Tarjan algorithm](/lengauer-tarjan-algorithm/). Each LCA step and each step of the walk of line L22 moves up the dominator tree, so it is $O(b)$ per edge in the worst case, and $O(g b)$ in total. With a constant-time LCA structure the LCA part drops to $O(g)$, and the walk of line L22 is short in practice.
- **Space.** $O(g)$, with $g = O(n + b v)$.

## Variants

- **Effects as edges.** Click and Paleczny thread memory and I/O as values: a store takes a memory state and gives a new one, and a load reads a memory state. This makes alias information part of the graph.
- **Peephole at creation.** The production graphs run constant folding, algebraic simplification and value numbering on each new node, so the parser already gives an optimized graph.
- **Pinned versus floating loads.** A load that can fault is pinned, or has a control input from the check that makes it safe. Moving a check makes the loads it guards move with it.
- **Graphs with blocks.** A CFG of SSA instructions, as in most compilers, is the other choice. V8 moved its JavaScript backend from the sea of nodes to Turboshaft, a CFG IR, and its blog post explains why.
- **E-graphs.** An [e-graph](/e-graph/) also hash-conses nodes, but keeps many equal versions of a value at once to choose the best one later.

## When to use it

The sea of nodes fits an optimizing compiler, often a [just-in-time compiler](/just-in-time-compilation/), that runs many local rewrites and value numbering together and wants code motion as a by-product of scheduling. It is a poor fit when most operations have effects, because then most nodes sit on the effect chain and little floats. This is one of the reasons V8 gave for leaving it. It is also hard to read and debug, since the graph has no order to print, and some passes, such as those that need a fixed order of side effects, must rebuild a schedule first.

## Pitfalls

- **Floating a node that can trap.** A division moved above its guarding test can fault on a path where the source never divided. Pin every operation that can trap or fault, or give it a control input from its guard.
- **The PHI use in the wrong block.** A PHI reads its input on the incoming edge, not in its own block. Counting the use in the PHI's block can place the value in a block that the incoming edge does not pass, so the PHI reads a value that was never computed on that path.
- **Ties in loop depth.** Choosing the higher block on a tie hoists code out of branches for no gain and makes it run on paths that did not need it. Prefer the lower block when the loop depth is equal.
- **Dead PHIs and dead nodes.** Maximal PHIs leave dead nodes. Schedule only nodes that a root reaches, or the output holds code for values that nobody reads.
- **Value numbering pinned nodes.** Two divisions with the same inputs in different blocks are not the same node, because each one traps on its own path.

## Implementations

## History

Click and Paleczny (1995) published the graph IR at the IR'95 workshop. It grew from Click's thesis work at Rice on combining analyses, and Click's PLDI paper of the same year gave global code motion and global value numbering on it. The HotSpot server compiler, called C2, was built on this IR. Paleczny, Vick and Click (2001) describe its SSA graph with RegionNode and PhiNode, and its global code motion on the sea of nodes. The TurboFan compiler of V8 also used a sea of nodes. In 2025 the V8 team reported that it had replaced it with the CFG-based Turboshaft in the JavaScript backend and for WebAssembly.

## References
