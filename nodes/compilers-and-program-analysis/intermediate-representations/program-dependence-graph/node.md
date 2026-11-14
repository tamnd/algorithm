---
tag: AK2XM4
kind: data-structure
slug: program-dependence-graph
name: Program dependence graph
aliases:
- PDG
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: A graph of the statements of a procedure with edges for data and control dependences, used for slicing, vectorization and scheduling.
model: word-ram
complexity:
  vars: {n: the number of instructions, m: the number of CFG edges, c: the number of control dependence edges, d: the number of flow dependence edges, r: the number of definitions}
  time: {control-edges: O(m + c), data-edges: O(n (n + m) r), slice: O(n + c + d)}
  space: {total: O(n + m + c + d)}
history:
  year: 1987
  people: [Jeanne Ferrante, Karl J. Ottenstein, Joe D. Warren]
  note: Ferrante, Ottenstein and Warren defined the PDG with control dependence from post-dominators in 1987. Horwitz, Reps and Binkley extended it across procedures in 1990.
prereqs: [control-flow-graph, control-dependence, data-dependence, reaching-definitions, post-dominance]
see_also: [program-slicing, pdg-slicing, system-dependence-graph-slicing, aggressive-dead-code-elimination, vectorization, def-use-chains, sea-of-nodes, instruction-scheduling-problem]
sources:
  - paper: doi:10.1145/24039.24041
    title: Jeanne Ferrante, Karl J. Ottenstein and Joe D. Warren, The program dependence graph and its use in optimization, ACM Transactions on Programming Languages and Systems 9(3), 1987, pages 319-349
    locator: the definition of the PDG, control dependence from the post-dominator tree, region nodes, and the uses for vectorization and code motion
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: the section on the control dependence graph
  - paper: doi:10.1145/77606.77608
    title: Susan Horwitz, Thomas Reps and David Binkley, Interprocedural slicing using dependence graphs, ACM Transactions on Programming Languages and Systems 12(1), 1990, pages 26-60
    locator: the system dependence graph, a PDG per procedure joined by call and parameter edges, and slicing by reachability
  - book: isbn:1558603204
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: the chapter on dependence analysis and dependence graphs, the section on program dependence graphs
  - paper: doi:10.1145/2480741.2480743
    title: James Stanier and Des Watson, Intermediate representations in imperative compilers, a survey, ACM Computing Surveys 45(3), 2013
    locator: the sections on graph-based intermediate representations and the PDG family
---

A program dependence graph (PDG) has one node for each instruction of a procedure and two kinds of edges. A *data edge* goes from an instruction that defines a variable to an instruction that may read that value. A *control edge* goes from a branch to an instruction whose execution the branch decides. The [control flow graph](/control-flow-graph/) fixes one order for the instructions; the PDG keeps only the order that the meaning of the program needs. So two instructions with no path between them in the PDG can be reordered or run in parallel, and the instructions that can affect a given one are its ancestors. Ferrante, Ottenstein and Warren (1987) built the control edges from [post-dominance](/post-dominance/), and the PDG is the basis of [program slicing](/program-slicing/), [aggressive dead code elimination](/aggressive-dead-code-elimination/) and dependence-based [vectorization](/vectorization/).

## In plain words

A recipe is written as a list of steps, but many steps do not need the step before them. You can chop the onions while the water boils. The PDG draws only the real needs. An arrow from step A to step B means B uses something A made, or B happens only if a test in A came out a certain way. Any order that follows the arrows cooks the same dish. To find every step that can change the taste of the sauce, follow the arrows backward from the sauce.

## The abstract type

The PDG of a procedure is a directed graph with these parts:

- **Nodes.** One node for each instruction, with the terminator of each block counted as an instruction, and one node ENTRY that stands for the start of the procedure and the definitions of the parameters.
- **Control edges** $(x, y, \ell)$: instruction $y$ is [control dependent](/control-dependence/) on the branch $x$ through the edge of $x$ to the block $\ell$. The label $\ell$ is the outcome of the branch that makes $y$ run. Instructions that run on every run of the procedure depend on ENTRY.
- **Data edges** $(d, u, v)$: the definition of variable $v$ at $d$ reaches the instruction $u$, which reads $v$. These are the flow (true) dependences of [data dependence](/data-dependence/). Anti and output dependences are added when the PDG is used to reorder memory operations, as described under Variants.

It supports these operations:

- BUILD(procedure): make the graph.
- CONTROL-PARENTS($y$) and DATA-PARENTS($y$): the edges into $y$.
- CHILDREN($x$): the edges out of $x$.
- SLICE($y$): all nodes from which $y$ is reachable, the backward slice of $y$.

## Representation

Each node has two lists of incoming edges and two lists of outgoing edges, one of each for control and for data. An instruction node is a pair (block, index), where the index equal to the number of instructions in the block names the terminator. The block-level control dependences are kept as well: every instruction of a block has the same control parents, so the per-instruction control edges are the block edges copied to each instruction.

Ferrante, Ottenstein and Warren add *region nodes*. All instructions that have the same set of control parents with the same labels hang below one region node, and the region node carries the control edges. This saves space when many instructions share their conditions, and it gives a tree of regions that a code generator can walk to put the instructions back into a control flow graph.

## Operations

```pseudo id=main
BUILD(P)                          ▷ P: a procedure with blocks, an entry block, ret terminators
L1  G ← the CFG of P, with a node START, a node EXIT,
        an edge START → entry, an edge START → EXIT, and an edge to EXIT from every ret block
L2  ipdom ← immediate post-dominators of G   ▷ dominators of the reverse of G, rooted at EXIT
L3  for each edge a → b of G with b ≠ ipdom(a) do
L4      y ← b
L5      while y ≠ ipdom(a) do
L6          src ← ENTRY if a = START, else the terminator of a
L7          for each instruction i of block y: add control edge (src, i, b)
L8          y ← ipdom(y)
L9  IN ← reaching definitions of P, with the parameters defined at ENTRY
L10 for each block B do
L11     cur ← IN[B], grouped by variable
L12     for each instruction u of B, in order, terminator last do
L13         for each variable v that u reads, each d in cur[v]: add data edge (d, u, v)
L14         if u defines v then cur[v] ← {u}

SLICE(y)
L15 S ← {y}; stack ← [y]
L16 while stack is not empty do
L17     z ← pop(stack)
L18     for each control or data edge (x, z, ·) into z with x ∉ S: add x to S, push x
L19 return S
```

**Control edges (L1 to L8).** Line L1 builds the augmented CFG of [control dependence](/control-dependence/). The edge START → EXIT makes the blocks that run on every run depend on START, which the PDG shows as ENTRY. Line L2 computes the post-dominator tree, for example with the [Cooper-Harvey-Kennedy](/cooper-harvey-kennedy-dominance/) iteration on the [transpose graph](/transpose-graph/). Lines L3 to L8 are the walk of Ferrante, Ottenstein and Warren: for each edge $a \to b$, the blocks that depend on $a$ through it are the blocks on the post-dominator tree path from $b$ up to $\mathrm{ipdom}(a)$, with $\mathrm{ipdom}(a)$ left out. A block whose terminator is `jump` has one successor, which is its immediate post-dominator, so only the terminators `br` get children. A block can depend on its own terminator when it is a loop test.

**Data edges (L9 to L14).** Line L9 solves [reaching definitions](/reaching-definitions/), a forward [gen-kill problem](/gen-kill-problem/). Lines L10 to L14 then walk each block once. The set $\mathit{cur}[v]$ holds the definitions of $v$ that reach the current point. A definition inside the block replaces it, so a use after a definition in the same block gets one edge. These edges are the [def-use chains](/def-use-chains/) of the procedure.

**Slicing (L15 to L19).** A backward slice is plain reachability over the reversed edges. It is the method of [PDG slicing](/pdg-slicing/), and its result is a set of instructions that can affect $y$.

## Example

Take the toy IR program that adds the odd numbers below the parameter `n`:

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

The PDG has 13 nodes: ENTRY and 12 instructions. The block-level control dependences, worked out on the [control dependence](/control-dependence/) page, are B1, B2 and B6 on START, B2, B3 and B5 on the branch of B2 with label B3, and B4 on the branch of B3 with label B4. Copied to the instructions, they give 14 control edges:

| from | to | label |
|---|---|---|
| ENTRY | `i = 0`, `s = 0`, `jump B2` (B1), `t1 = i < n`, `br t1 B3 B6` (B2), `ret s` (B6) | B1 |
| `br t1 B3 B6` | `t1 = i < n`, `br t1 B3 B6` (B2), `t2 = i % 2`, `br t2 B4 B5` (B3), `i = i + 1`, `jump B2` (B5) | B3 |
| `br t2 B4 B5` | `s = s + i`, `jump B5` (B4) | B4 |

The 15 data edges are:

| definition | uses reached |
|---|---|
| `i = 0` and `i = i + 1` | `t1 = i < n`, `t2 = i % 2`, `s = s + i`, `i = i + 1` (8 edges) |
| `s = 0` and `s = s + i` | `s = s + i`, `ret s` (4 edges) |
| ENTRY (parameter `n`) | `t1 = i < n` |
| `t1 = i < n` | `br t1 B3 B6` |
| `t2 = i % 2` | `br t2 B4 B5` |

The slice of `ret s` holds ENTRY and every instruction except the three jumps: the jumps define nothing and decide nothing. The slice of `i = i + 1` is ENTRY, `i = 0`, `i = i + 1`, `t1 = i < n` and `br t1 B3 B6`, so the computation of `s` and the parity test do not affect `i`. The loop test $\texttt{br t1 B3 B6}$ is its own control parent, which is how the PDG shows that it runs again on each trip.

## Correctness

The PDG is correct when its control edges are exactly the control dependences of Ferrante, Ottenstein and Warren, copied to the instructions, and its data edges are exactly the pairs (definition, use) joined by a path with no other definition of the same variable. The proof in [proofs/correctness.md](proofs/correctness.md) shows both. For the control edges it shows that the walk at an edge $a \to b$ visits exactly the nodes that $b$ post-dominates and that do not strictly post-dominate $a$. For the data edges it shows that the least solution of the reaching definitions equations holds exactly the definitions with such a definition-clear path, and that the scan of lines L10 to L14 adds the same pairs at instruction level. The tests compare the control edges with a brute-force search over the paths of the definition on random graphs, and the data edges with a search over instruction positions on random programs.

## Complexity

The model is the word RAM, and the unit step is one operation on a hash set or list with one element. Let $n$ be the number of instructions, $m$ the number of CFG edges, $c$ the number of control edges and $d$ the number of data edges.

- **Post-dominators.** The Cooper-Harvey-Kennedy iteration is fast in practice, and the [Lengauer-Tarjan algorithm](/lengauer-tarjan-algorithm/) takes $O(m \alpha(m, n))$ time.
- **Control edges.** Each step of the walk adds at least one new edge, so lines L3 to L8 take $O(m + c)$. The number $c$ can be $\Theta(n^2)$: the [control dependence](/control-dependence/) page has a chain with back edges where $k$ blocks give $k(k+1)/2$ dependences. Region nodes reduce the stored edges in common cases, but not in the worst case.
- **Data edges.** With $r$ definitions, each round of the reaching definitions iteration costs $O((n + m) r)$, and a round-robin iteration needs at most $n + 1$ rounds, so the worst case is $O(n (n + m) r)$. Visiting the blocks in reverse postorder needs only a few rounds on usual code. The scan of lines L10 to L14 costs $O(n + d)$ beyond that. The number $d$ can also be quadratic: $k$ definitions of one variable that all reach $k$ uses give $k^2$ edges.
- **Space.** $O(n + m + c + d)$.
- **Queries.** With adjacency lists, CONTROL-PARENTS and DATA-PARENTS cost $O(1)$ per edge returned, and SLICE costs $O(n + c + d)$.

## Variants

- **Region nodes.** As in the original paper, an extra node per set of equal control conditions.
- **System dependence graph.** Horwitz, Reps and Binkley (1990) join one PDG per procedure with call, parameter-in and parameter-out edges, plus summary edges, so that slicing across calls can respect calling context. See [system dependence graph slicing](/system-dependence-graph-slicing/).
- **All data dependences.** For reordering, the data edges must include anti dependences (a read before a write) and output dependences (two writes), and the dependences through memory, which need alias information. Loop-carried dependences with distance and direction vectors are the input of loop vectorization and parallelization.
- **SSA-based PDG.** On [static single assignment form](/static-single-assignment-form/), each use has one reaching definition, so data edges are the SSA def-use edges and reaching definitions is not needed. The [sea of nodes](/sea-of-nodes/) carries this idea further and drops the blocks.
- **Weak control dependence.** Some tools use the weak form of Podgurski and Clarke, so that code after a loop depends on the loop test, which keeps non-termination in slices.

## When to use it

Use a PDG when the question is "what can affect this" or "what can move": slicing for debugging and program understanding, dead code removal that starts from the outputs and keeps only what they need, finding statements that can run in parallel, and [vectorization](/vectorization/), where cycles of dependences inside a loop decide which statements can be vectorized. For plain forward data flow analyses a CFG is simpler, and for most scalar optimizations SSA with [def-use chains](/def-use-chains/) gives the data edges at lower cost.

## Pitfalls

- **Forgetting the edge START → EXIT.** Without it, blocks that always run have no control parent, and a slice of them misses the dependence on the procedure being called at all.
- **Several returns or no return.** The post-dominator tree needs one exit, so add EXIT with an edge from each return. A loop that never exits leaves blocks that do not reach EXIT, and the walk then has no immediate post-dominator for them. Add a fake exit edge first.
- **Flow edges are not enough to reorder.** Two writes to the same variable have no flow edge between them, but they cannot be swapped. Add anti and output edges before reordering.
- **Jumps disappear from slices.** A slice is a set of instructions, not a program. To run a slice, the jumps and the block structure must be rebuilt, for example from the region tree.
- **Memory.** Data edges through loads and stores depend on alias analysis. An edge left out makes a slice or a reordering wrong.

## Implementations

## History

Ferrante, Ottenstein and Warren (1987) defined the PDG as a common graph for control and data dependence, computed control dependence from the post-dominator tree, and showed its use for vectorization, code motion and node splitting. Horwitz, Reps and Binkley (1990) built the system dependence graph for slicing across procedures. Cytron et al. (1991) showed that control dependences are the reverse dominance frontiers, with the same algorithm that places phi-functions in SSA form. Later graph IRs, such as the sea of nodes of Click and Paleczny (1995), keep explicit dependence edges and drop the fixed order of a CFG in the same spirit.

## References
