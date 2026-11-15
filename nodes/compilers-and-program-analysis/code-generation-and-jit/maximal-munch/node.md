---
tag: FV9S4Q
kind: algorithm
slug: maximal-munch
name: Maximal munch instruction selection
aliases:
- maximal munch tiling
area: compilers-and-program-analysis/code-generation-and-jit
level: intro
summary: Tiles an expression tree top-down by always choosing the largest pattern that matches at the root, then tiling the subtrees.
solves: [instruction-selection-problem]
model: word-ram
complexity:
  vars: {n: the number of nodes of the tree, P: the number of patterns, m: the number of nodes of the largest pattern}
  time: {worst: O(n P m)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 1980
  people: [Roderic G. G. Cattell]
  note: "Cattell used the largest-pattern-first rule in his code generator generator, described in his 1978 thesis and in TOPLAS in 1980. Appel made the name maximal munch common in textbooks."
prereqs: [instruction-selection-problem, greedy-algorithm, postorder-traversal]
see_also: [aho-johnson-code-generation, burs, tree-pattern-matching, peephole-optimization, three-address-code, abstract-syntax-tree]
sources:
  - paper: doi:10.1145/357094.357097
    title: Roderic G. G. Cattell, Automatic derivation of code generators from machine descriptions, ACM Transactions on Programming Languages and Systems 2(2), 1980, 173-190
    locator: the code generator that matches the largest instruction pattern first at the root of the tree and then works on the subtrees
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 9 (Instruction Selection), Section 9.1, the Maximal Munch algorithm and the definitions of optimal and optimum tilings
  - paper: "Gabriel Hjort Blindell, Survey on instruction selection, an extensive and modern literature review, arXiv:1306.4898, 2013"
    locator: the section on macro expansion and tree covering, where the term maximal munch is traced to the thesis of Cattell
---

Maximal munch is the simplest way to choose machine instructions for an expression tree. It solves the [instruction selection problem](/instruction-selection-problem/) for trees with a greedy rule. At the root, it takes the largest instruction pattern that matches, and then it tiles each operand subtree in the same way. The result is always a valid cover, and no two adjacent tiles can be joined into one tile. Appel calls such a tiling *optimal*. It is not always *optimum*: the total cost can be higher than the least cost that the [Aho-Johnson dynamic program](/aho-johnson-code-generation/) or [BURS](/burs/) finds.

## In plain words

Each machine instruction does a small piece of the expression tree, so choosing instructions is like covering the tree with tiles. Some tiles are big, for example one load instruction that also adds an offset to the address.

Maximal munch starts at the top of the tree. It looks at all tiles that fit there and takes the one that covers the most nodes. The parts of the tree under the tile are still open, and the algorithm does the same thing on each of them. When the work comes back up, it writes the instructions, so each instruction comes after the instructions for its operands.

The rule is fast and easy to write by hand. A big tile is usually a good choice, but not always. A big tile at the top can take away a node that a cheaper tile below needs.

## The problem

The input is an expression tree $T$ with $n$ nodes and a table of instruction patterns. The nodes on this page are CONST $k$, VAR $x$ (a variable in memory), MEM $a$ (load the word at address $a$), ADD and MUL. In a pattern, *reg* is a hole: an operand that an earlier instruction leaves in a register. CONST in a pattern is an immediate constant, and VAR is a memory operand.

| name | pattern | cost | size |
|---|---|---|---|
| LI | CONST | 1 | 1 |
| LD | VAR | 3 | 1 |
| ADD | ADD(reg, reg) | 1 | 1 |
| ADDI | ADD(reg, CONST) | 1 | 2 |
| ADDM | ADD(reg, VAR) | 3 | 2 |
| MUL | MUL(reg, reg) | 3 | 1 |
| LDR | MEM(reg) | 3 | 1 |
| LDO | MEM(ADD(reg, CONST)) | 3 | 3 |
| LDX | MEM(ADD(reg, reg)) | 3 | 2 |
| MADD | ADD(MUL(reg, reg), reg) | 2 | 2 |

The *size* of a pattern is the number of tree nodes that it covers, so the holes do not count. A *tiling* puts one pattern on each part of the tree, so that each node is covered exactly once and each hole is the root of another tile. The output is a tiling and the code that it gives, with one new virtual register for each tile. Maximal munch does not handle a register limit.

## The algorithm

```pseudo id=main
MUNCH(v)
L1  best ← none
L2  for each pattern p of the table, in table order do
L3      if p matches at v and (best = none or size(p) > size(best)) then best ← p
L4  for each hole h of best, from left to right do
L5      x_h ← MUNCH(h)
L6  t ← a new register; emit best into t, with the registers x_h and the constants and variables that best covers
L7  return t
```

The choice goes top-down, at lines L2 and L3. The code comes out bottom-up, at line L6, after the code of the operands. A tie in size goes to the first pattern of the table, so the order of the table is part of the algorithm. Appel's version emits the code in the same order.

## Example

Take $T = \mathrm{MEM}(\mathrm{ADD}(\mathrm{MUL}(a, b), c))$, where $a$, $b$ and $c$ are variables.

| step | node | patterns that match | choice |
|---|---|---|---|
| 1 | MEM | LDR (size 1), LDX (size 2) | LDX, which also covers the ADD |
| 2 | MUL$(a, b)$ | MUL | MUL |
| 3 | $a$ | LD | LD |
| 4 | $b$ | LD | LD |
| 5 | $c$ | LD | LD |

LDO does not match at the root, because the right operand of the ADD is not a constant. The code is:

| instruction | cost |
|---|---|
| $v_0 \leftarrow a$ | 3 |
| $v_1 \leftarrow b$ | 3 |
| $v_2 \leftarrow v_0 * v_1$ | 3 |
| $v_3 \leftarrow c$ | 3 |
| $v_4 \leftarrow \mathrm{MEM}(v_2 + v_3)$ | 3 |

The total is 15. The tiling LDR, MADD and three LD costs $3 + 2 + 9 = 14$, and it is the cheapest tiling of this tree. The big tile LDX at the root took the ADD node, so the cheap MADD could not cover it. The munch tiling is still optimal in Appel's sense: LDX and MUL do not join into any pattern of the table.

On $\mathrm{MEM}(\mathrm{ADD}(a, 8))$, munch takes LDO at the root and LD for $a$, for a cost of 6. That is the cheapest tiling, and it is the case that the rule is made for.

## Correctness

MUNCH always stops, because each call covers at least the node $v$ and then works only on smaller subtrees. If the table has a pattern of size 1 for each kind of node, some pattern matches at every node, so the result is a tiling of the whole tree, and each node is covered exactly once. The code computes the value of the tree, because each instruction runs after the instructions of its holes.

The tiling is *optimal* in the sense of Appel: no two adjacent tiles can be replaced by one tile of lower cost. In fact a stronger claim holds. Let $p$ be the tile at $v$ and $p'$ the tile at a hole of $p$. If a pattern $p''$ covered exactly the nodes of $p$ and $p'$, it would match at $v$ and have size $|p| + |p'| > |p|$, so line L3 would have chosen it, or a pattern at least as large, instead of $p$. So no two adjacent tiles join into any tile at all, cheap or not. The example shows that this local property does not give the least total cost. The proof file gives the details.

## Complexity

MUNCH runs once for each tile, and each tile covers at least one node, so it runs at most $n$ times. Each run tries all $P$ patterns, and a match takes time proportional to the size of the pattern, at most $m$. The time is $O(n P m)$, which is linear in $n$ for a fixed table. A real code generator sorts the patterns by size and indexes them by the operator at the root, so a run tries only a few patterns. The recursion is as deep as the tree, so the extra space is $O(n)$.

## Properties

- **Valid.** With a complete table, the result covers each node exactly once.
- **Optimal, not optimum.** No two adjacent tiles join into one tile, but the total cost can be higher than the least cost.
- **Cost-blind.** The choice uses the sizes of the patterns, not their costs. A cost changes the result only through the order of the table.
- **Greedy and top-down.** It is a [greedy algorithm](/greedy-algorithm/): a choice at a node is never taken back.
- **No register limit.** It uses a new virtual register for each tile. A register allocator runs later.

## Variants and improvements

- **Cost as the key.** Choose the pattern with the best ratio of cost to size, or the most expensive one. Such a rule is still greedy, and it can still miss the least cost, because a choice at the root cannot see the costs below.
- **Optimum tiling.** The [Aho-Johnson dynamic program](/aho-johnson-code-generation/) and [BURS](/burs/) find the least cost with the same table, in time that is also linear for a fixed table.
- **Munch and peephole.** Some compilers first select simple instructions and then combine them with a [peephole optimizer](/peephole-optimization/). The two methods find many of the same big instructions.

## When to use it

Use it for a first code generator, a simple compiler or a JIT that must be fast and short. It also works well on machines whose cost model is close to "fewer instructions is better", where big tiles are almost always good, such as many RISC machines. When the table has many overlapping patterns with different costs, as on CISC machines or in DSP code, use a dynamic program or BURS instead.

## Pitfalls

- **"Optimal" is not "optimum".** In Appel's words an optimal tiling is only locally best. Do not claim that munch gives the cheapest code.
- **An incomplete table.** If some node kind has no pattern of size 1, munch can reach a node where nothing matches, even though a tiling of the whole tree exists.
- **The order of the table.** Two patterns of the same size can both match, for example ADDM and MADD on $\mathrm{ADD}(\mathrm{MUL}(a, b), c)$. The first one in the table wins, so a change in the order changes the code and its cost.
- **Shared nodes.** On a DAG, munch tiles a shared node once for each parent, so the code computes it more than once.
- **Another maximal munch.** In lexical analysis, "maximal munch" is the longest-match rule for tokens. It is a different algorithm with the same idea.

## Implementations

## History

Cattell used the largest-pattern-first rule in the code generator generator of his 1978 thesis at Carnegie Mellon, and he described the method in TOPLAS in 1980. The 1980 paper does not use the words "maximal munch"; Hjort Blindell traces the term to the thesis. Appel used the name for the algorithm in his textbooks of the late 1990s, where he also set the terms *optimal* and *optimum* tilings apart. Optimum tree tiling is older: Aho and Johnson gave a dynamic program in 1976.

## References
