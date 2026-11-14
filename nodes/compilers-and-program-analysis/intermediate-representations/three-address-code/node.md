---
tag: ZGTNP2
kind: definition
slug: three-address-code
name: Three-address code
aliases:
- quadruples
- TAC
area: compilers-and-program-analysis/intermediate-representations
level: intro
summary: A linear IR whose instructions have at most one operator and three operands, such as x = y op z, with jumps for control.
prereqs: [intermediate-representation]
see_also: [basic-block, control-flow-graph, static-single-assignment-form, expression-dag, straight-line-program, a-normal-form, local-value-numbering, sethi-ullman-numbering]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 6.2 (Three-Address Code), with 6.2.1 (addresses and instructions), 6.2.2 (quadruples), 6.2.3 (triples and indirect triples) and 6.2.4 (static single-assignment form)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 4 (Intermediate Representations), the part on linear IRs and three-address code
  - book: isbn:1558603204
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 4 (Intermediate Representations), the medium-level form MIR
---

Three-address code is a linear [intermediate representation](/intermediate-representation/) in which each instruction applies at most one operator and names at most three addresses: up to two operands and one result, as in `x = y op z`. A source expression with several operators becomes a sequence of such instructions, with compiler temporaries for the intermediate results. Control flow is written with labels, unconditional jumps and conditional branches. Cut into [basic blocks](/basic-block/) and joined by the edges of a [control flow graph](/control-flow-graph/), three-address code is the working form of most optimizing compilers, and it is the IR that the compiler pages of this site use.

## Definition

### Addresses and instructions

An *address* is one of three things: a name of the source program, an integer constant, or a compiler temporary, a fresh name that the translator makes for an intermediate value. A *three-address instruction* is one of the forms below, where $x$, $y$, $z$ are addresses, $op$ is a binary operator and $L$ is a label. The list is the one of the dragon book, Section 6.2.1, in the syntax of this site.

| form | meaning |
|---|---|
| `x = y op z` | apply a binary operator |
| `x = op y` | apply a unary operator (the toy IR writes `x = 0 - y`) |
| `x = y` | copy |
| `jump L` | go to the instruction with label $L$ |
| `br x L1 L2`, or `if x goto L` | go to $L_1$ if $x \ne 0$, else to $L_2$ (or fall through) |
| `param x`, `call p, n`, `x = call p, n` | pass parameters and call a procedure with $n$ arguments |
| `ret x` | return from the procedure |
| `x = y[i]`, `x[i] = y` | indexed copy |
| `x = &y`, `x = *y`, `*x = y` | address and pointer operations |

A three-address program is a finite sequence of instructions, some of them with labels. Each instruction does one operation, so the order of evaluation is fully explicit, and every intermediate result has a name.

### The toy IR

The compiler pages of this site use a small three-address code. Its instructions are `x = k`, `x = y` and `x = a op b`, where $a$ and $b$ are names or integer constants and $op$ is one of `+ - * / % & | ^ << >> < <= == !=`. Comparisons give 0 or 1. The program is a list of blocks: each block is a label with a colon, then instructions, then exactly one terminator, `jump L`, `br a L1 L2` or `ret a`. So the toy IR is three-address code already cut into basic blocks, with no fall-through: every block names its successors. There is no unary operator, no indexed copy and no `param`; pointer pages add `p = &x`, `x = *p`, `*p = a` and `p = alloc`, and interprocedural pages add `x = call f(a, b)`, with the arguments inside the call. SSA pages add `x2 = phi [entry: x0, body: x3]`, which is not a three-address instruction in the strict sense, because it has one operand per predecessor.

Values are unbounded integers. `/` and `%` truncate toward zero, as in C, and trap when the divisor is 0. `<<` and `>>` trap when the shift count is outside 0 to 63. The outcome of a run is a return value, a trap, or no end.

### Representations in memory

The text form is for people. Inside a compiler, an instruction is a record, and the classic records are these:

- **Quadruple.** Four fields: $op$, $arg_1$, $arg_2$, $result$. A temporary is a name in the symbol table. Instructions can be moved freely, because each result has its own name. The toy IR helper `toyir.py` uses tuples of this kind, such as `("op", "x", "+", "y", 1)`.
- **Triple.** Three fields: $op$, $arg_1$, $arg_2$. The result has no name; a later instruction refers to it by the position $(i)$ of the triple that computes it. This saves the temporaries, but moving an instruction changes positions, so every reference to it must change too.
- **Indirect triple.** The triples stay where they are, and a separate list of pointers gives the order of execution. An optimizer reorders the pointer list, not the triples.

## Examples and non-examples

### An expression

The assignment `a = b + c * (d - e)` has three operators, so it becomes three instructions with two temporaries and a final copy, or with the last result written into `a` directly:

```
t1 = d - e
t2 = c * t1
a = b + t2
```

The translation walks the expression tree in postorder and emits one instruction per operator node. In general, an expression tree with $k$ operator nodes gives exactly $k$ instructions, and an expression with a repeated subexpression, such as `(d - e) * (d - e)`, gives one instruction per operator occurrence unless the translator shares the [expression DAG](/expression-dag/). With $b = 2$, $c = 3$, $d = 10$, $e = 4$ the result is $2 + 3 \cdot 6 = 20$.

The same code as quadruples and as triples:

| | $op$ | $arg_1$ | $arg_2$ | $result$ |
|---|---|---|---|---|
| 0 | `-` | d | e | t1 |
| 1 | `*` | c | t1 | t2 |
| 2 | `+` | b | t2 | a |

| | $op$ | $arg_1$ | $arg_2$ |
|---|---|---|---|
| (0) | `-` | d | e |
| (1) | `*` | c | (0) |
| (2) | `+` | b | (1) |
| (3) | `=` | a | (2) |

The triple form needs the extra copy triple (3), because a triple cannot name its own result.

### Control flow

The loop `while (i < n) { s = s + i * i; i = i + 1 }` in the toy IR:

```
head:
  t1 = i < n
  br t1 body exit
body:
  t2 = i * i
  s = s + t2
  i = i + 1
  jump head
```

The `while` is gone. What is left is a comparison into a temporary, a two-way branch and a jump back. In a flat three-address code with fall-through, the same loop is `L1: t1 = i < n; ifFalse t1 goto L2; t2 = i * i; s = s + t2; i = i + 1; goto L1; L2:`.

### Short-circuit conditions

`if (a < b && c != 0) x = 1` has no operator for `&&` in the toy IR. The translator emits two branches, so that `c != 0` is not computed when `a < b` is false:

```
B0:
  t1 = a < b
  br t1 B1 B3
B1:
  t2 = c != 0
  br t2 B2 B3
B2:
  x = 1
  jump B3
B3:
  ...
```

Here the evaluation order of the source becomes control flow in the IR. With `t3 = t1 & t2` instead, both operands are computed, which is wrong if the second one can trap, as `x / c` can.

### Non-examples

- `x = a + b * c` has two operators. It is a valid statement in many languages, but not a three-address instruction; it needs a temporary.
- `x = f(g(y))` nests one call inside another. In three-address code, `t = call g(y)` comes first.
- The stack machine code `load b; load c; load d; load e; sub; mul; add; store a` is a linear IR, but its operands are implicit stack slots, not addresses, so it is not three-address code.
- An [abstract syntax tree](/abstract-syntax-tree/) is not linear: the order of the operations follows from the tree shape, not from a list.

### Pitfalls

- **Assuming the order of a source expression.** C does not fix the order in which the operands of `+` are evaluated. The translator must pick one, and then the three-address code fixes it. Two compilers can legally make different choices when the operands have side effects.
- **Reusing temporaries too early.** A translator that reuses a temporary before its last use changes the value that a later instruction reads. Fresh temporaries are always safe; a [register allocation](/register-allocation-problem/) pass can merge them later.
- **Treating triples as freely movable.** Moving a triple changes the positions that other triples refer to. Use quadruples or indirect triples if the optimizer moves code.
- **Forgetting that a branch hides a trap.** Turning short-circuit control flow into arithmetic, as in the example above, computes both operands and can add a trap.

## Related definitions

- [Intermediate representation](/intermediate-representation/): the general idea; three-address code is the linear, medium-level member of the family.
- [Basic block](/basic-block/) and [control flow graph](/control-flow-graph/): three-address code is cut at labels and jumps into blocks, and the blocks are joined by edges.
- [Static single assignment form](/static-single-assignment-form/): three-address code in which each name has exactly one definition, with [phi-functions](/phi-function/) at join points.
- [Expression DAG](/expression-dag/): a graph form of one basic block of three-address code, in which equal subexpressions share a node; [local value numbering](/local-value-numbering/) builds it.
- [Straight-line program](/straight-line-program/): the algebraic version, a sequence of operations without branches, used to measure the cost of computing a polynomial.
- [A-normal form](/a-normal-form/): the functional counterpart, in which every intermediate value is bound to a name by a `let`.
- [Sethi-Ullman numbering](/sethi-ullman-numbering/): the minimum number of registers needed to evaluate an expression tree, and the order of the three-address instructions that reaches it.

## References
