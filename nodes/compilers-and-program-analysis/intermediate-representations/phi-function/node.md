---
tag: Z0Z5YA
kind: definition
slug: phi-function
name: Phi node
aliases:
- SSA phi-function
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: An SSA instruction at the head of a block that takes one operand per incoming edge and yields the operand of the edge taken.
prereqs: [static-single-assignment-form, control-flow-graph]
see_also: [dominance-frontier, ssa-construction-problem, pruned-ssa-form, out-of-ssa-translation, lost-copy-and-swap-problems, critical-edge-splitting, ssa-cps-correspondence, braun-ssa-construction]
sources:
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: the phi-function, with one operand per predecessor of the join node, and its meaning on entry from the j-th predecessor
  - paper: doi:10.1007/978-3-642-37051-9_6
    title: Matthias Braun, Sebastian Buchwald, Sebastian Hack, Roland Leißa, Christoph Mallon and Andreas Zwinkau, Simple and efficient construction of static single assignment form, Compiler Construction (CC 2013), LNCS 7791, pages 102-122
    locator: Section 2.2 (Algorithm 3, trivial phi-functions, which reference only themselves and one other value, and their recursive removal)
  - book: isbn:9783030805142
    title: Fabrice Rastello and Florent Bouchez Tichadou (editors), SSA-based Compiler Design, Springer, 2022
    locator: Chapter 2 (Properties and Flavours), the phi-function and its parallel semantics; Chapter 3 (Standard Construction and Destruction Algorithms), the replacement of phi-functions by copies
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 19 (Static Single-Assignment Form), phi-functions and their placement
---

A phi node, or phi-function, is the instruction that [static single assignment form](/static-single-assignment-form/) adds where control flow joins. It sits at the top of a block and has one operand for each edge that enters the block. When control comes in along an edge, the phi node takes the operand of that edge as its value. So it merges the different names that one source variable has on different paths into one new name. A phi node is not a real machine instruction. Before code generation, [out-of-SSA translation](/out-of-ssa-translation/) replaces it by copies on the incoming edges. The name has nothing to do with [Euler's phi function](/euler-totient/) of number theory.

## Definition

### Form

Let $b$ be a block of a [control flow graph](/control-flow-graph/) with incoming edges $(p_1, b), \ldots, (p_k, b)$. A phi node in $b$ has the form

$$x = \phi(a_1, \ldots, a_k),$$

where $a_j$ is a name or a constant and belongs to the edge $(p_j, b)$. The toy IR of this site writes the edge next to each operand: `x.3 = phi [B2: x.1, B3: x.2]`. LLVM does the same, with one `[value, block]` pair for each operand. The paper of Cytron et al. writes the operands in the order of the predecessors and leaves the edges implicit.

The rules are:

1. All phi nodes of a block come before its other instructions.
2. A phi node has exactly one operand for each incoming edge. If a block $p$ has two edges to $b$, the phi node has two operands for $p$. The toy IR merges such edges into one, so this case does not come up there.
3. A block with one predecessor needs no phi node. A phi node there, `x.2 = phi [B1: x.1]`, is a copy.

### Meaning

Suppose control moves along the edge $(p_j, b)$. Then:

1. Every phi node of $b$ reads its operand $a_j$, using the values the names have at the end of $p_j$.
2. After all reads, every phi node of $b$ assigns its target.

All phi nodes of one block act at the same time, as one *parallel copy*. Their written order has no meaning. The operand $a_j$ is a use at the end of $p_j$, not in $b$. So $a_j$ is live at the end of $p_j$, and in strict SSA form the definition of $a_j$ must dominate $p_j$, not $b$. The target $x$ is defined at the top of $b$.

### Trivial phi nodes

A phi node is *trivial* if all its operands are the same value $v$, or are $v$ and the phi node itself, as in `x.2 = phi [B1: x.1, B3: x.2]`. It always yields $v$, so every use of `x.2` can use $v$, and the phi node can be removed. A phi node whose operands are only the node itself is in unreachable code or in the start block, and Braun et al. replace it by an undefined value. They remove trivial phi nodes while they build SSA form. Removing one phi node can make another one trivial.

### Why phi nodes are needed

Without phi nodes, the single assignment rule cannot express a value that depends on the path taken. In a diamond in which both arms assign `x`, a use after the join must read `x.1` on one path and `x.2` on the other. A phi node at the join gives one name, `x.3`, that has the right value on each path. Where phi nodes go is the job of the [SSA construction problem](/ssa-construction-problem/): the minimal set of blocks is the iterated [dominance frontier](/dominance-frontier/) of the definitions.

## Examples and non-examples

### A join after a branch

```
B4:
  x.3 = phi [B2: x.1, B3: x.2]
  y.1 = x.3 + a
  ret y.1
```

If control came from B2, `x.3` gets the value of `x.1`. If it came from B3, it gets the value of `x.2`.

### A loop header

```
B2:
  i.2 = phi [B1: i.1, B5: i.3]
```

On the first entry, from B1, `i.2` gets the start value `i.1`. On each later entry, from the latch B5, it gets `i.3`, the value of the previous iteration. The operand `i.3` is defined in B5, after B2, but it is used at the end of B5, so the definition dominates the use.

### Parallel reading: a swap

```
# params: n
B1:
  a.1 = 1
  b.1 = 2
  i.1 = 0
  jump B2
B2:
  a.2 = phi [B1: a.1, B2: b.2]
  b.2 = phi [B1: b.1, B2: a.2]
  i.2 = phi [B1: i.1, B2: i.3]
  i.3 = i.2 + 1
  t.1 = i.3 < n
  br t.1 B2 B3
B3:
  r.1 = a.2 * 10
  r.2 = r.1 + b.2
  ret r.2
```

On each trip around the loop, `a.2` and `b.2` swap their values, because both phi nodes read the old values. The program returns 12 for $n = 1$, 21 for $n = 2$ and 12 for $n = 3$. If the two phi nodes run one after the other, `b.2` reads the new `a.2`, both names become 2, and the program returns 22 for every $n \ge 2$. This is the swap problem of [out-of-SSA translation](/lost-copy-and-swap-problems/).

### Non-examples

- **A phi node in the middle of a block.** `y.1 = x.1 + 1` followed by `z.1 = phi [...]` is not valid. The phi node belongs to the edges, so it must come first.
- **A phi node with one operand too few.** In a block with predecessors B2 and B3, `x.3 = phi [B2: x.1]` has no value for a run that comes from B3.
- **A select.** `x = c ? a : b` picks a value by a condition that is a value in the program. A phi node picks by the edge taken and has no condition operand. If-conversion can turn a phi node at the end of a diamond into a select.
- **Block arguments.** MLIR, Cranelift and the [SSA and CPS correspondence](/ssa-cps-correspondence/) pass values to a block as arguments of the jump. This is the same idea written at the other end of the edge. The jump `jump B4(x.1)` and a parameter `x.3` of B4 together replace the phi node.

### Variants

- **Gated SSA.** Gamma functions carry the branch condition, so the value can be found without the control flow graph. Mu and eta functions mark loop entry and loop exit.
- **Undefined operands.** A phi node may have the operand `undef` for an edge on which the variable has no definition. This keeps the form valid when strictness fails.
- **Phi nodes for memory.** Memory SSA gives the whole memory a version number and uses phi nodes to join memory states.

## Related definitions

- [Static single assignment form](/static-single-assignment-form/): the form phi nodes belong to.
- [Dominance frontier](/dominance-frontier/) and [pruned SSA form](/pruned-ssa-form/): where phi nodes are needed.
- [Out-of-SSA translation](/out-of-ssa-translation/) and [critical edge splitting](/critical-edge-splitting/): how phi nodes become copies.
- [Lost copy and swap problems](/lost-copy-and-swap-problems/): what goes wrong if the parallel meaning is ignored.
- [Braun SSA construction](/braun-ssa-construction/): builds phi nodes on demand and removes the trivial ones.

## References
