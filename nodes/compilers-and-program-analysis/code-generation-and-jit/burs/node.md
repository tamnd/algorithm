---
tag: VPX7R8
kind: algorithm
slug: burs
name: Bottom-up rewrite system
aliases:
- BURS
- BURG
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Precomputes the dynamic programming of optimal tree tiling into tables, so a code generator labels each node by table lookup.
solves: [instruction-selection-problem]
model: word-ram
complexity:
  vars: {n: the number of nodes of the tree}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 1988
  people: [Eduardo Pelegrí-Llopart, Susan L. Graham]
  note: "Pelegrí-Llopart and Graham gave BURS theory in 1988. Balachandran, Dhamdhere and Biswas, and then Proebsting, made the table construction simple and fast, and BURG turned it into a tool in 1992."
prereqs: [aho-johnson-code-generation, tree-pattern-matching, deterministic-finite-automaton]
see_also: [maximal-munch, hoffmann-odonnell-matching, instruction-selection-problem, bellman-ford, context-free-grammar, rewrite-rule, subset-construction]
sources:
  - paper: doi:10.1145/73560.73586
    title: Eduardo Pelegrí-Llopart and Susan L. Graham, Optimal code generation for expression trees, an application of BURS theory, Proceedings of the 15th ACM Symposium on Principles of Programming Languages, 1988, 294-308
    locator: the bottom-up rewrite systems, the states with costs relative to the least cost, and the tables computed when the code generator is built
  - paper: doi:10.1145/131080.131089
    title: Christopher W. Fraser, Robert R. Henry and Todd A. Proebsting, BURG, fast optimal instruction selection and tree parsing, ACM SIGPLAN Notices 27(4), 1992, 68-76
    locator: the tree grammar with costs and chain rules, the labeler driven by tables, and the reducer
  - paper: doi:10.1145/151640.151642
    title: Christopher W. Fraser, David R. Hanson and Todd A. Proebsting, Engineering a simple, efficient code-generator generator, ACM Letters on Programming Languages and Systems 1(3), 1992, 213-226
    locator: iburg, which uses the same grammars but runs the dynamic program while it compiles
  - paper: "Todd A. Proebsting, Simple and efficient BURS table generation, Proceedings of the ACM SIGPLAN 1992 Conference on Programming Language Design and Implementation, 331-340"
    locator: the worklist construction of the states and the trimming of entries that can never be used
  - paper: "A. Balachandran, D. M. Dhamdhere and S. Biswas, Efficient retargetable code generation using bottom-up tree pattern matching, Computer Languages 15(3), 1990, 127-140"
    locator: the states with normalized costs and the construction of the transition tables
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 9 (Instruction Selection), the section on tree grammars and code generator generators
---

A bottom-up rewrite system, or BURS, is a way to build an optimum tree tiler ahead of time. It solves the [instruction selection problem](/instruction-selection-problem/) for trees with the same answer as the tiling dynamic program of [Aho and Johnson](/aho-johnson-code-generation/), but it does the dynamic program when the code generator is built, not when it runs. Each node then gets a *state* by one table lookup from its operator and the states of its children, and the states hold all the information needed to read off a least-cost tiling. BURG, by Fraser, Henry and Proebsting, is the best known generator of such tables. The method works only if the number of states is finite, which holds for most machine grammars but not for all.

## In plain words

The tiling dynamic program does the same arithmetic again and again. At every node it adds up costs from the children and keeps the cheapest tile for each kind of result.

BURS notices that only the differences between these costs matter for the choice. A subtree can be very big, but the cost to get it into a register is often just "the cost to get it into an address, plus one". So the algorithm keeps only the differences. Then the possible cost lists are few, and each one gets a number.

Before any program is compiled, the generator works out all these lists and builds a table: for an operator and the numbers of its children, the table gives the number of the node. At compile time, the code generator only looks up the table, from the leaves up. Then it walks down and writes the chosen instructions.

## The problem

The input is an expression tree $T$ with $n$ nodes and a *tree grammar* that describes the machine. A grammar has nonterminals, such as *reg* for a value in a register, and two kinds of rules, each with a cost:

- a *base rule* $X \to \mathrm{op}(Y_1, \ldots, Y_k)$: a node with operator op can be derived from $X$ if its children can be derived from $Y_1, \ldots, Y_k$;
- a *chain rule* $X \to Y$: a value of kind $Y$ can be turned into a value of kind $X$.

A pattern of the instruction table becomes rules of this form. Each inner node of a big pattern gets a fresh helper nonterminal with a rule of cost 0. With the table of [maximal munch](/maximal-munch/) and the [Aho-Johnson](/aho-johnson-code-generation/) page, the rules are:

| rule | cost | from |
|---|---|---|
| con $\to$ CONST, var $\to$ VAR | 0 | the leaves |
| reg $\to$ con | 1 | LI |
| reg $\to$ var | 3 | LD |
| reg $\to$ ADD(reg, reg) | 1 | ADD |
| reg $\to$ ADD(reg, con) | 1 | ADDI |
| reg $\to$ ADD(reg, var) | 3 | ADDM |
| reg $\to$ MUL(reg, reg) | 3 | MUL |
| reg $\to$ MEM(reg) | 3 | LDR |
| $h_1 \to$ ADD(reg, con), reg $\to$ MEM($h_1$) | 0, 3 | LDO |
| $h_2 \to$ ADD(reg, reg), reg $\to$ MEM($h_2$) | 0, 3 | LDX |
| $h_3 \to$ MUL(reg, reg), reg $\to$ ADD($h_3$, reg) | 0, 2 | MADD |

A derivation of the tree from *reg* is exactly a tiling, and it has the same cost. The output is a least-cost derivation, and the code that it gives. Registers are virtual, so there is no register limit.

## The algorithm

A state is a set of entries $(X, \delta_X, \rho_X)$: a nonterminal, its cost relative to the cheapest nonterminal of the node, and the rule that reaches this cost.

```pseudo id=main
BUILD(grammar)                      ▷ when the code generator is built
L1  for each leaf operator a do table[a] ← STATE(a, ())
    STATE(op, s_1, ..., s_k):
L2      for each base rule X → op(Y_1, ..., Y_k) with each Y_i in s_i do
L3          total ← cost of the rule + sum over i of δ_{Y_i} in s_i; keep the least total for X, with its rule
L4      repeat: for each chain rule X → Y, if δ_Y + its cost < δ_X then lower δ_X and keep the rule; until nothing changes
L5      subtract the least δ from every entry, and return the set of entries
L6  repeat: for each operator op and each tuple of known states, table[op, s...] ← STATE(op, s...); until no new state appears

LABEL(v)                            ▷ when a program is compiled
L7  for each child u of v do LABEL(u)
L8  state(v) ← table[op(v), state of each child]

REDUCE(v, X)
L9  ρ ← the rule of X in state(v)
L10 if ρ is a chain rule X → Y then REDUCE(v, Y) and emit the instruction of ρ
L11 else ρ is X → op(Y_1, ..., Y_k):
L12     for each child u_i of v do REDUCE(u_i, Y_i); emit the instruction of ρ, unless X is a helper
```

The code generator calls LABEL(root) and then REDUCE(root, reg). A helper passes the operands of its node up to the rule above it, so one instruction such as LDX gets the operands of both the MEM and the ADD.

## Example

BUILD on the grammar of the page finds 11 states. Here is the labeling of $T = \mathrm{MEM}(\mathrm{ADD}(\mathrm{MUL}(a, b), c))$:

| node | state | entries ($X$: $\delta_X$, rule) |
|---|---|---|
| $a$, $b$, $c$ | 1 | var: 0, var $\to$ VAR; reg: 3, LD |
| MUL$(a, b)$ | 5 | $h_3$: 0; reg: 3, MUL |
| ADD$(\ldots, c)$ | 9 | reg: 0, MADD; $h_2$: 1 |
| MEM | 2 | reg: 0, LDR |

At the MUL node, $h_3 \to \mathrm{MUL}(\mathrm{reg}, \mathrm{reg})$ costs $0 + 3 + 3 = 6$ and MUL costs $3 + 3 + 3 = 9$, so the relative costs are 0 and 3. At the ADD node, MADD gives $2 + 0 + 3 = 5$, ADD gives $1 + 3 + 3 = 7$, ADDM gives $3 + 3 + 0 = 6$, and $h_2$ gives $0 + 3 + 3 = 6$. The best for *reg* is MADD, and $h_2$ is 1 more. At the root, LDR gives $3 + 0 = 3$, and LDX gives $3 + 1 = 4$, so LDR wins.

REDUCE(root, reg) emits LD $a$, LD $b$, LD $c$, MADD, LDR, for a cost of 14. That is the least tiling cost; [maximal munch](/maximal-munch/) picks LDX at the root and pays 15. The absolute cost never appears at compile time. The numbers in the states are the same for any tree, however big, that reaches the same state.

## Correctness

The key fact is shift invariance. At a node, every base rule adds the costs of the children, so if each child cost is changed by a constant, every candidate total changes by the same sum of constants. The best rule for each nonterminal stays the same, and so do the differences between the totals. The chain rules, at line L4, are a shortest path problem on the nonterminals, solved by the [Bellman-Ford](/bellman-ford/) method, and a shift does not change it either. So the state of a node, with costs taken relative to the cheapest entry, depends only on its operator and the states of its children. That is what makes a table possible.

By induction on the tree, the state of each node holds, for each nonterminal $X$, the true least cost of deriving the subtree from $X$, minus the least cost over all nonterminals, and a rule that starts such a least derivation. REDUCE follows these rules from the root down and emits a least-cost derivation from *reg*, which is a least-cost tiling. The proof file gives the details.

## Complexity

LABEL does one table lookup for each node, and REDUCE visits each node a constant number of times for a fixed grammar. So compiling a tree takes $\Theta(n)$ time and $\Theta(n)$ space for the labels. The dynamic program has moved to BUILD, whose cost depends only on the grammar. For a binary operator, the table has one entry for each pair of states, so it has size $O(S^2)$ for $S$ states. Real generators compress it, for example by mapping the states of each operand position to a few classes. For the grammar of the page, the tables have $2 + 11 + 2 \cdot 11^2 = 255$ entries.

## Properties

- **Optimum.** For a fixed grammar with a finite set of states, the result is a least-cost tiling, the same cost as the dynamic program.
- **No arithmetic at compile time.** The code generator does no cost sums and no comparisons, only lookups.
- **A tree automaton.** The states and the table form a deterministic bottom-up tree automaton, much like a [DFA](/deterministic-finite-automaton/) on strings, and BUILD is close to the [subset construction](/subset-construction/) with costs attached.
- **Fixed costs.** The costs must be known when the tables are built. A cost that depends on the tree, such as "free if the constant is small", needs a different tool.

## Variants and improvements

- **iburg.** Fraser, Hanson and Proebsting take the same grammar but run the dynamic program at compile time. The generator is much simpler and the costs can be dynamic, at the price of some speed.
- **Table trimming.** Proebsting removes entries of a state that can never be part of a least derivation, so that fewer states are distinct. This makes the tables smaller and BUILD faster.
- **On-demand tables.** A code generator can compute the states lazily, the first time it needs each one, and cache them. This avoids building states that no program reaches.
- **Rewrites.** In the theory of Pelegrí-Llopart and Graham, rules can also rewrite the tree, for example by commutativity, before it is tiled. BURG and most later tools keep only the tree grammar.
- **Matching without costs.** [Hoffmann-O'Donnell matching](/hoffmann-odonnell-matching/) builds the same kind of bottom-up tables for [tree pattern matching](/tree-pattern-matching/) without costs.

## When to use it

Use it for a production code generator with a fixed machine description, where compile speed matters and the grammar is large. The tables give a least-cost tiling at the speed of a lookup. When the grammar changes often, or the costs depend on the operands, use iburg or the plain dynamic program. When the input is a DAG, split it into trees first, since tiling a DAG is NP-complete ([the DAG theorem](/dag-code-generation-np-completeness/)).

## Pitfalls

- **Infinite states.** BUILD stops only if the relative costs are bounded. With $x \to a$ and $y \to a$ of cost 0, $x \to f(x)$ of cost 1 and $y \to f(y)$ of cost 2, a chain of $k$ copies of $f$ has $\delta_y = k$, and BUILD never stops. A generator must detect this and give an error.
- **Absolute costs in states.** If the states store absolute costs, every tree has new states and the table is useless. Always subtract the minimum.
- **Ties.** Two rules can have the same cost. Break ties in a fixed order, or two equal states can look different and the table grows.
- **Unreachable goals.** If the root state has no entry for *reg*, the grammar cannot derive the tree. Check this before REDUCE.
- **No register limit.** BURS ignores the number of registers. The [Aho-Johnson](/aho-johnson-code-generation/) cost vectors add it, at the cost of larger states.

## Implementations

## History

Pelegrí-Llopart and Graham introduced bottom-up rewrite systems in 1988. They showed that a code generator can find optimum tilings with tables computed ahead of time, with the costs in each state taken relative to the cheapest entry. Balachandran, Dhamdhere and Biswas gave a simpler table construction in 1990. In 1992, Proebsting described a fast worklist construction with trimming, and Fraser, Henry and Proebsting released BURG, a generator that reads a tree grammar and writes the tables in C. In the same year, Fraser, Hanson and Proebsting wrote iburg, which reads the same grammars and does the work at compile time; the lcc compiler uses it.

## References
