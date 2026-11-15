---
tag: 10CJ5M
kind: algorithm
slug: aho-johnson-code-generation
name: Aho-Johnson dynamic programming code generation
aliases:
- optimal tree tiling
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Computes, bottom-up, the cheapest cost of each subtree for every number of free registers and for memory, then emits code that stores whole subtrees only where that is cheaper.
solves: [instruction-selection-problem]
model: word-ram
complexity:
  vars: {n: the number of nodes of the tree, r: the number of registers}
  time: {worst: Θ(n r)}
  space: {extra: Θ(n r)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 1976
  people: [Alfred V. Aho, Stephen C. Johnson]
  note: Aho and Johnson gave the cost vectors, the strong normal form theorem and the linear time bound for a fixed machine.
prereqs: [instruction-selection-problem, sethi-ullman-numbering, tree-dynamic-programming]
see_also: [maximal-munch, burs, tree-pattern-matching, dag-code-generation-np-completeness, register-allocation-problem, optimal-substructure, three-address-code]
sources:
  - paper: doi:10.1145/321958.321970
    title: Alfred V. Aho and Stephen C. Johnson, Optimal code generation for expression trees, Journal of the ACM 23(3), 1976, 488-501
    locator: the class of machines with r interchangeable registers, the cost vectors computed bottom-up, the strong normal form theorem, and the bound linear in the size of the tree for a fixed machine
  - paper: doi:10.1145/321607.321620
    title: Ravi Sethi and J. D. Ullman, The generation of optimal code for arithmetic expressions, Journal of the ACM 17(4), 1970, 715-728
    locator: the special case of a machine with one instruction per operator, which the cost vectors generalize
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Chapter 8 (Code Generation), Section 8.11, dynamic programming code generation, contiguous evaluation and the cost vectors
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 9 (Instruction Selection), the dynamic programming algorithm for an optimum tiling
---

Aho-Johnson code generation picks the instructions for an expression tree, and the order of their operands, on a machine with $r$ registers. It solves the [instruction selection problem](/instruction-selection-problem/) for trees and includes the register limit. For each node and for each number $j$ of free registers, it computes the cost of the cheapest code that leaves the node in a register, and also the cost to leave it in memory. The answer at the root is the least cost of any program for the tree, on the class of machines of Aho and Johnson. The [Sethi-Ullman algorithm](/sethi-ullman-numbering/) is the special case with one unit-cost instruction per operator. [BURS](/burs/) and [maximal munch](/maximal-munch/) tile the same trees but ignore the register limit, and munch does not find the cheapest tiling.

## In plain words

One machine instruction can do a small piece of a tree. Choosing the instructions is like covering the tree with tiles, where each tile has a price.

The algorithm works from the leaves up. At each node it writes down a short price list: the cheapest way to compute this subtree if one register is free, if two are free, and so on, and also the price to compute it and save it in memory. To fill the list at a node, it tries every tile that fits there and every order of the operands of the tile. The operand that is computed first can use all the free registers, and each later operand has one fewer, because the earlier results wait in registers.

When the list at the root is full, the algorithm goes down again and writes out the choices that gave the best price.

## The problem

The input is an expression tree $T$ with $n$ nodes and a machine. The nodes on this page are CONST $k$, VAR $x$ (a variable in memory), MEM $a$ (load the word at address $a$), ADD and MUL. The machine has registers $R_0, \ldots, R_{r-1}$ with $r \ge 2$. Each instruction is a tree pattern with a cost. In a pattern, *reg* is an operand in a register, CONST is an immediate constant, and VAR is a memory operand: a variable, or a temporary that holds a stored subtree.

| name | pattern | cost |
|---|---|---|
| LI | CONST | 1 |
| LD | VAR | 3 |
| ADD | ADD(reg, reg) | 1 |
| ADDI | ADD(reg, CONST) | 1 |
| ADDM | ADD(reg, VAR) | 3 |
| MUL | MUL(reg, reg) | 3 |
| LDR | MEM(reg) | 3 |
| LDO | MEM(ADD(reg, CONST)) | 3 |
| LDX | MEM(ADD(reg, reg)) | 3 |
| MADD | ADD(MUL(reg, reg), reg) | 2 |

A store $t \leftarrow R_i$ costs $s = 3$. The output is a program that leaves the value of $T$ in $R_0$, never needs more than $r$ registers at one time, and has the least total cost. A *program* here may evaluate the operands in any order, interleave them, store any value and load it back.

## The algorithm

$C[v][j]$ is the least cost to compute $T_v$ into a register when $j$ registers are free, and $C[v][0]$ is the least cost to have it in memory. All entries start at $\infty$.

```pseudo id=main
LABEL(v)
L1  for each child u of v do LABEL(u)
L2  for each pattern p that matches at v do          ▷ LD matches here only at a variable
L3      base ← cost(p) + sum of C[m][0] over the memory operands m of p that are not variables
L4      for each order h_1, ..., h_q of the register operands of p do
L5          for j ← max(1, q) to r do total ← base + sum over t of C[h_t][j - t + 1]
L6              if total < C[v][j] then C[v][j] ← total; remember (p, the order)
L7  if v is a variable then C[v][0] ← 0
L8  else C[v][0] ← C[v][r] + s                        ▷ compute with all registers, then store
L9  for j ← 1 to r do C[v][j] ← min(C[v][j], C[v][0] + cost(LD))   ▷ store, then load back

GENERATE(root)
L10 for each subtree that the chosen plan keeps in memory, deepest first:
        emit its code with all r registers free, then a store to a new temporary
L11 emit the code of the root with all r registers free
```

The code of a node $v$ with free registers $R_i, \ldots, R_{i+j-1}$ runs the operand $h_t$ in $R_{i+t-1}, \ldots, R_{i+j-1}$, so the earlier operands wait in $R_i, \ldots, R_{i+t-2}$. Then the instruction of $v$ writes $R_i$. A subtree that the plan keeps in memory is computed before everything else, when all registers are free, and its temporary is then a memory operand or the source of a load.

## Example

Take $T = (a * b) + (c * \mathrm{MEM}(a + 8))$ and $r = 2$. The vectors $(C[v][0], C[v][1], C[v][2])$ are:

| node | $C[v][0]$ | $C[v][1]$ | $C[v][2]$ | choice for $j = 2$ |
|---|---|---|---|---|
| each variable | 0 | 3 | 3 | LD |
| 8 | 4 | 1 | 1 | LI |
| $a + 8$ | 7 | 4 | 4 | ADDI |
| MEM$(a + 8)$ | 9 | 6 | 6 | LDO, which covers the ADD too |
| $a * b$ | 12 | 15 | 9 | MUL |
| $c * \mathrm{MEM}(a+8)$ | 15 | 18 | 12 | MUL |
| root | 30 | 33 | 27 | ADDM with the right product in memory |

At the root, ADD with both products in registers costs $1 + 9 + 18 = 28$ or $1 + 12 + 15 = 28$: one product has to run with one free register, and $C[\cdot][1]$ includes a store and a load. MADD needs three registers. ADDM costs $3 + 9 + 15 = 27$: the right product is computed first and stored, and the left product then has both registers. The code is:

| step | instruction | cost |
|---|---|---|
| 1 | $R_0 \leftarrow c$ | 3 |
| 2 | $R_1 \leftarrow a$ | 3 |
| 3 | $R_1 \leftarrow \mathrm{MEM}(R_1 + 8)$ | 3 |
| 4 | $R_0 \leftarrow R_0 * R_1$ | 3 |
| 5 | $t_0 \leftarrow R_0$ | 3 |
| 6 | $R_0 \leftarrow a$ | 3 |
| 7 | $R_1 \leftarrow b$ | 3 |
| 8 | $R_0 \leftarrow R_0 * R_1$ | 3 |
| 9 | $R_0 \leftarrow R_0 + t_0$ | 3 |

The total is 27. With $r = 3$ the cost falls to 20: load $a$ into $R_0$, compute the right product in $R_1$ with two free registers (12), load $b$ into $R_2$, and finish with one MADD. The best tiling with no register limit also costs 20. If the operands of a pattern may only go left to right, the best cost for $r = 3$ is 22.

## Correctness

LABEL is a [dynamic program](/tree-dynamic-programming/) over normal-form plans. A plan for $v$ with $j$ registers is a pattern at $v$, an order of its register operands, plans with $j, j-1, \ldots$ registers for those operands, and plans in memory for its memory operands, or else a store and a load of $v$. The parts of a plan are independent, so the cheapest plan is made of cheapest parts, and an induction on the tree shows that $C[v][j]$ is the least cost of a plan. GENERATE turns the plan into code with the same cost, and the registers of the operands do not overlap. Aho and Johnson prove that each tree has a cheapest program in *strong normal form*, which is exactly such a plan. So $C[\mathrm{root}][r]$ is the least cost of any program. The proof file gives the details.

## Complexity

For each node, LABEL tries each pattern, each order of its $q$ register operands and each $j$, and sums $q$ entries. That is $O(P \cdot q! \cdot q \cdot r)$ per node for $P$ patterns, and $\Theta(n r)$ for the whole tree when the machine is fixed, because LABEL fills $n (r + 1)$ entries. For a fixed $r$ the time is linear in the size of the tree. Matching a pattern at a node takes time proportional to the size of the pattern, a constant for a fixed machine. GENERATE does constant work per emitted instruction. The tables take $\Theta(n r)$ space.

## Properties

- **Exact for trees.** On the machine class of Aho and Johnson, the cost at the root is the least cost over all programs, including programs that interleave operands or store and reload values.
- **Fewer registers never help.** $C[v][j] \ge C[v][j+1]$, because each plan for $j$ registers is also a plan for $j + 1$.
- **Stores of whole subtrees.** The code stores only complete subtrees, each computed with all registers free, and each stored value is used once.
- **Equal to the best tiling when registers are plenty.** On the machine of the page, with $r$ at least the number of nodes, no plan stores a value, and the cost is the least tiling cost.

## Variants and improvements

- **No register limit.** Drop the index $j$. Then $C[v]$ is one number, the least tiling cost, and the program is the tiling dynamic program of most modern code generators. A global register allocator handles the registers later.
- **Precomputed states.** [BURS](/burs/) moves the dynamic program to the time when the code generator is built, so that labeling a tree is one table lookup per node. iburg runs the same dynamic program at compile time from a tree grammar.
- **Fast matching.** Twig, by Aho, Ganapathi and Tjiang, finds the patterns that match at each node with a top-down [tree pattern matcher](/tree-pattern-matching/) and then runs the dynamic program.
- **Commutative operators.** Add a second pattern with the operands swapped. Then ADDM also covers a variable on the left of an ADD. The order loop of line L4 only changes the order of evaluation, not the place of an operand.
- **Several nonterminals.** A real grammar has more classes of results than "register" and "memory", for example addressing modes and condition codes. Each class is one more entry of the cost vector.

## When to use it

Use it when the input is a tree, the instructions overlap in complex ways, and the register limit matters for the code of one expression. In most compilers today, a tiling dynamic program without the register index chooses the instructions, and a separate [register allocator](/register-allocation-problem/) assigns registers. The register-aware version suits small machines, accumulator machines and code generators for single expressions. For code with shared values the problem is NP-complete (see [the DAG theorem](/dag-code-generation-np-completeness/)), so split the DAG into trees first.

## Pitfalls

- **Ignoring the register limit.** The tiling cost of the example is 20, but with two registers the best program costs 27.
- **The wrong share of registers.** The $t$-th operand gets $j - t + 1$ registers, not $j$. Giving each operand all $j$ registers undercounts.
- **One order only.** The example with $r = 3$ costs 22 if the operands go left to right, and 20 with the best order.
- **Shared nodes.** On a DAG, a shared subtree is counted once per parent and computed twice. The labels are no longer exact.
- **Machines outside the class.** An instruction that needs a fixed register or a pair of registers breaks the normal form theorem, and the result is no longer guaranteed to be the least cost.
- **Ties.** Many plans can have the same cost. Break ties by a fixed rule, so that the output is reproducible.

## Implementations

## History

Aho and Johnson published the algorithm in the Journal of the ACM in 1976. They generalized the result of Sethi and Ullman (1970) from a fixed instruction set to any machine of their class, proved the strong normal form theorem, and showed that the algorithm runs in time linear in the size of the tree for a fixed machine. The tiling dynamic program became the base of the code generator generators twig, BURG and iburg.

## References
