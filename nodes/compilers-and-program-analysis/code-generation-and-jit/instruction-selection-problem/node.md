---
tag: MTNAAX
kind: problem
slug: instruction-selection-problem
name: Instruction selection
aliases:
- instruction selection problem
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Cover the IR of a program with patterns of target machine instructions so that the total cost of the chosen instructions is least.
prereqs: [three-address-code, expression-dag]
see_also: [maximal-munch, aho-johnson-code-generation, burs, dag-code-generation-np-completeness, tree-pattern-matching, register-allocation-problem, instruction-scheduling-problem, peephole-optimization]
sources:
  - book: isbn:9780521820608
    title: Andrew W. Appel, Modern Compiler Implementation in ML, Cambridge University Press, 1998
    locator: Chapter 9 (Instruction Selection), tree patterns, optimal and optimum tilings, maximal munch and the dynamic programming algorithm
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Chapter 8 (Code Generation), instruction selection by tree rewriting and optimal code generation for expressions
  - paper: doi:10.1145/321958.321971
    title: John Bruno and Ravi Sethi, Code generation for a one-register machine, Journal of the ACM 23(3), 1976, 502-510
    locator: the NP-completeness of optimal code for DAGs on a one-register machine
  - paper: doi:10.1145/1356058.1356065
    title: David Ryan Koes and Seth Copen Goldstein, Near-optimal instruction selection on DAGs, Proceedings of the 6th IEEE/ACM Symposium on Code Generation and Optimization (CGO 2008), 45-54
    locator: the NP-completeness of tiling a DAG and the NOLTIS heuristic
  - paper: doi:10.1145/151640.151642
    title: Christopher W. Fraser, David R. Hanson and Todd A. Proebsting, Engineering a simple, efficient code-generator generator, ACM Letters on Programming Languages and Systems 1(3), 1992, 213-226
    locator: tree grammars with costs as machine descriptions, and iburg in the lcc compiler
  - paper: "Gabriel Hjort Blindell, Survey on instruction selection, arXiv:1306.4898, 2013"
    locator: the classes of methods (macro expansion, tree covering, DAG covering and graph covering) and their history
---

Instruction selection is the step of a compiler back end that chooses the machine instructions for a program. The program is given in an intermediate form, as trees or DAGs of simple operations, and each machine instruction is described by a *pattern*: a small tree of operations that the instruction computes, with a cost. The task is to cover the program with patterns so that every operation is computed and the total cost is least. On trees, the problem is solved exactly in linear time for a fixed machine. On DAGs, it is NP-complete.

## In plain words

A compiler first turns a program into many tiny steps, such as "add these two", "multiply these two" or "read memory here". A real machine has instructions that each do one or more of these steps at once. For example, one instruction may add two values and then read memory at the result.

So the compiler must choose which instructions to use. Each instruction covers a small group of steps, like a tile covers part of a floor. Every step must be covered, and each instruction has a price, such as its time or its size. The goal is the cheapest set of tiles.

When the steps form a tree, the best choice can be found quickly. When one result feeds several later steps, the choices interact, and the problem becomes very hard.

## Definition

The machine is described by a *tree grammar*. It has a finite set of nonterminals, such as `reg` for a value in a register, a start nonterminal, and rules $A \to p$ with a cost $c \ge 0$. The pattern $p$ is a tree whose inner nodes are IR operators and whose leaves are IR leaves or nonterminals. A rule says: the instruction computes the tree $p$, reads its operands in the forms of the nonterminal leaves, and leaves its result in the form $A$.

The input is a tree or a DAG $G$ of IR operators. A *cover* of $G$ is a set of pairs $(v, r)$, where the pattern of the rule $r$ matches the part of $G$ that starts at the node $v$, such that

1. each root of $G$ has a pair whose rule has the start nonterminal on the left;
2. for each pair $(v, r)$ and each nonterminal leaf $B$ of the pattern of $r$, matched at a node $u$, there is a pair $(u, r')$ whose rule has $B$ on the left.

The cost of the cover is the sum of the costs of its rules. Each pair is one instruction, and a value that is computed once is available to every parent. The *optimization problem* asks for a cover of least cost. The *decision problem* asks whether a cover of cost at most $K$ exists. In a tree, each node has one parent, which asks for one form of its value, so a cover of least cost is a *tiling*: each node is covered by exactly one tile. A chain rule, whose pattern is a single nonterminal, converts a value from one form to another and covers no node.

Appel calls a tiling *optimal* when no two adjacent tiles can be joined into one tile of lower cost, and *optimum* when no tiling has a lower total cost. An optimum tiling is optimal, but not the reverse. The problem asks for an optimum.

## Variants

- **Tree tiling.** The input is a tree, for example one expression of an [abstract syntax tree](/abstract-syntax-tree/) or one statement of the IR. Shared values are first stored in temporaries, so that each tree is separate.
- **DAG tiling.** The input is the [DAG](/expression-dag/) of a basic block, with common subexpressions. Tiles may *overlap*, so that a shared node is computed again inside the tiles of two users, or they may be forbidden to overlap, so that each shared value is computed once into a register.
- **Graph covering.** The input is the graph of a whole function, often in [SSA form](/static-single-assignment-form/), so that patterns can span blocks and loops.
- **Complex instructions.** Some instructions have more than one result, such as a division that gives the quotient and the remainder, or an add that also sets the condition flags. Their patterns are DAGs or graphs, not trees, and tree tiling cannot use them.
- **Integrated code generation.** Selection is solved together with [register allocation](/register-allocation-problem/) and [scheduling](/instruction-scheduling-problem/), because the best instructions depend on the free registers and on the timing.
- **Cost models.** The cost can be the time, the code size or the energy. Only the costs change; the problem stays the same.

## Examples

Take a small machine with these instructions, where `reg` is a value in a register:

| name | pattern | cost |
|---|---|---|
| li | CONST | 1 |
| ld | VAR | 3 |
| add | ADD(reg, reg) | 1 |
| addi | ADD(reg, CONST) | 1 |
| addm | ADD(reg, VAR) | 3 |
| mul | MUL(reg, reg) | 3 |
| ldr | MEM(reg) | 3 |
| ldo | MEM(ADD(reg, CONST)) | 3 |
| ldx | MEM(ADD(reg, reg)) | 3 |
| madd | ADD(MUL(reg, reg), reg) | 2 |

Each rule has `reg` on the left, so this grammar has one nonterminal. The tree $\mathrm{MEM}(\mathrm{ADD}(\mathrm{MUL}(a, b), c))$, with three variables in memory, has exactly four tilings:

| tiles | cost |
|---|---|
| ldr, madd, ld $a$, ld $b$, ld $c$ | 14 |
| ldr, addm, mul, ld $a$, ld $b$ | 15 |
| ldx, mul, ld $a$, ld $b$, ld $c$ | 15 |
| ldr, add, mul, ld $a$, ld $b$, ld $c$ | 16 |

The optimum is 14. [Maximal munch](/maximal-munch/) takes the largest tile at the root, which is ldx, and ends with 15: that tiling is optimal in Appel's sense, but it is not the optimum. The tree $\mathrm{MEM}(\mathrm{ADD}(a, 8))$ has the optimum tiling ldo and ld $a$, of cost 6.

On a DAG, a shared node must suit all its users. If $\mathrm{MUL}(a, b)$ is used both by the tree above and by $\mathrm{ADD}(\mathrm{MUL}(a, b), d)$, then the selector can compute the product once with mul and use the register in both sums, or let two madd tiles each compute it again. Which choice is cheaper depends on the costs, and with many shared nodes the choices interact.

## Known algorithms

- **Macro expansion.** Each IR operation is replaced by a fixed sequence of instructions, and a [peephole optimizer](/peephole-optimization/) then joins neighbouring instructions. It is simple and fast, and it gives no guarantee.
- **[Maximal munch](/maximal-munch/).** It takes, from the root down, the largest pattern that matches. It is fast and gives an optimal tiling, in Appel's sense, but not always the optimum.
- **[Aho-Johnson dynamic programming](/aho-johnson-code-generation/).** It computes, from the leaves up, the least cost of each subtree for each nonterminal. It gives the optimum tiling of a tree, in time linear in the tree for a fixed grammar.
- **[BURS](/burs/).** It precomputes the dynamic program into the tables of a tree automaton, so that labeling a node is one table lookup. BURG and iburg are code generator generators of this kind.
- **[Tree pattern matching](/tree-pattern-matching/).** It finds all the patterns that match at each node, which is the first step of the dynamic program. Twig uses a top-down matcher, and the [Hoffmann-O'Donnell](/hoffmann-odonnell-matching/) method gives a bottom-up one.
- **DAG methods.** Splitting the DAG into trees at the shared nodes and tiling each tree; the NOLTIS heuristic of Koes and Goldstein; and integer programming, which finds the optimum for small blocks.

## Bounds

- **Trees, fixed grammar: $\Theta(n)$.** Each of the $n$ nodes must be read, and the dynamic program does a constant amount of work at each node when the grammar is fixed. For a grammar with $R$ rules whose patterns have at most $m$ nodes, it takes $O(n R m)$ time, and BURS removes the factor $R m$ at code generation time.
- **DAGs: NP-complete.** Tiling a DAG with a tree grammar and unlimited registers is NP-complete, even for one fixed grammar ([the NP-completeness of code generation for DAGs](/dag-code-generation-np-completeness/)). Earlier, Bruno and Sethi showed that finding the shortest program for a DAG on a machine with one register is NP-complete.
- **Graphs.** Covering a whole function contains DAG covering as a special case, so it is NP-hard as well.

## Reductions

- **Tree tiling to tree parsing.** A tiling of a tree is a derivation of the tree in the tree grammar, and its cost is the cost of the derivation. So tree tiling is the problem of a least-cost derivation, and the bottom-up dynamic program is a parser for regular tree grammars. When the patterns are written in prefix order, they become the productions of a [context-free grammar](/context-free-grammar/), and an LR parser can select instructions. This was the approach of Glanville and Graham.
- **3-SAT to DAG tiling.** A reduction from [3-SAT](/3-sat/) makes each variable a shared node with two possible forms, true and false, and each clause a root whose tiles exist only when some literal is true. A cover of cost equal to the number of nodes exists exactly when the formula is satisfiable.
- **DAG tiling to integer programming.** One 0-1 variable for each pair of a node and a rule, with constraints for conditions 1 and 2 of the definition, gives an exact formulation that general solvers handle for blocks of moderate size.

## Applications

Every compiler for a real machine solves this problem in some form. The lcc compiler uses tree grammars with iburg. LLVM selects instructions on a DAG for each basic block, with matchers generated from the machine descriptions. GCC expands its IR to machine operations by fixed rules and then joins them with a combining pass. JIT compilers often use macro expansion or maximal munch, because the time to compile matters more than the last few percent of speed. The same covering problem appears in the mapping of logic circuits to the cells of a technology library.

## References
