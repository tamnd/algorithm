---
tag: Z8Z036
kind: concept
slug: intermediate-representation
name: Intermediate representation
aliases:
- IR
- intermediate language
area: compilers-and-program-analysis/intermediate-representations
level: intro
summary: A form of the program between source and machine code on which a compiler analyzes and transforms the program.
prereqs: [abstract-syntax-tree]
see_also: [three-address-code, basic-block, control-flow-graph, static-single-assignment-form, continuation-passing-style, sea-of-nodes, program-dependence-graph, expression-dag]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Chapter 6 (Intermediate-Code Generation), Section 6.1 (variants of syntax trees and DAGs) and Section 6.2 (three-address code); Section 8.4 (basic blocks and flow graphs)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 4 (Intermediate Representations), on graphical, linear and hybrid IRs and on the naming of values
  - book: isbn:1558603204
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 4 (Intermediate Representations), with the high-level, medium-level and low-level forms HIR, MIR and LIR
  - paper: doi:10.1109/CGO.2004.1281665
    title: Chris Lattner and Vikram Adve, LLVM, A Compilation Framework for Lifelong Program Analysis and Transformation, Proceedings of the International Symposium on Code Generation and Optimization (CGO 2004), pages 75-88
    locator: Section 2 (the LLVM code representation, a typed instruction set in SSA form)
  - paper: doi:10.1145/368892.368915
    title: J. Strong, J. Wegstein, A. Tritter, J. Olsztyn, O. Mock and T. Steel, The problem of programming communication with changing machines, a proposed solution (Part 1), Communications of the ACM 1(8), 1958
    locator: the proposal of UNCOL, one universal intermediate language between all source languages and all machines
---

An intermediate representation (IR) is the form of a program that a compiler holds between the source text and the machine code. The front end translates the source into the IR, the optimizer analyzes the IR and rewrites it into a better IR with the same behavior, and the back end translates the IR into instructions for one machine. An IR is a data structure, not only a text format: a tree, a graph, a list of instructions, or a mix of these. Most compilers use more than one IR, from a high level form close to the [abstract syntax tree](/abstract-syntax-tree/) down to a low level form close to the machine. The pages of this area use one IR, a [three-address code](/three-address-code/) in [basic blocks](/basic-block/) that form a [control flow graph](/control-flow-graph/).

## In plain words

A translator who works between many languages does not learn every pair. She translates each text into one simple middle language, and from that middle language into each target. A compiler does the same. It turns the program into a simple internal form, does all its checks and improvements on that form, and only at the end writes code for a real machine.

The middle form is easier to work on than the source. Each step does one small thing, each value has a name, and the places where the program can jump are shown clearly. Some middle forms keep the shape of the source as a tree. Others look like a list of small machine steps. Many compilers use several of them in a row, each one closer to the machine than the one before.

## The idea

### Why an IR

Without an IR, a compiler for $s$ source languages and $t$ machines needs $s \cdot t$ translators. With one shared IR it needs $s$ front ends and $t$ back ends, so $s + t$ parts, and every optimization written once on the IR serves all of them. This was the hope of the UNCOL proposal of 1958. A universal IR for all languages and machines was never built, but the split into front end, optimizer and back end around a shared IR is how GCC, LLVM and most other compilers are organized.

The second reason is that analysis is easier on a simple form. In the source, one statement can hide many operations, evaluation order is partly implicit, and control flow is spread over `while`, `break`, `return` and exceptions. In a good IR each operation is one instruction, every intermediate result has a name, and every transfer of control is one explicit edge. A [dataflow analysis](/dataflow-analysis/) then has only a few instruction forms and one kind of edge to handle.

### The main families

Cooper and Torczon sort IRs by their structure. Each family has its use.

| family | form | example | good for |
|---|---|---|---|
| graphical, tree | [abstract syntax tree](/abstract-syntax-tree/) | the parse result without punctuation | type checking, source-level transforms |
| graphical, DAG | [expression DAG](/expression-dag/) | a tree in which equal subexpressions are shared | local redundancy, instruction selection |
| linear, three-address | [three-address code](/three-address-code/) | `t2 = i * i` | dataflow analysis, most optimizations |
| linear, stack | stack machine code | JVM bytecode, WebAssembly | compact transport, simple interpreters |
| hybrid | [control flow graph](/control-flow-graph/) of [basic blocks](/basic-block/) | blocks of three-address code joined by edges | global analysis and optimization |
| value graph | [static single assignment form](/static-single-assignment-form/), [sea of nodes](/sea-of-nodes/), [program dependence graph](/program-dependence-graph/) | each value defined once, uses point to definitions | sparse analysis, value numbering, code motion |
| functional | [continuation-passing style](/continuation-passing-style/), [A-normal form](/a-normal-form/) | every intermediate value bound by a `let` | compilers for functional languages |

The families are not exclusive. LLVM IR, for example, is a control flow graph of basic blocks whose instructions are three-address code in SSA form.

### Levels

An IR also has a level. A high level IR keeps source concepts such as array subscripts, loops and method calls, so that loop transformations and inlining can see them. A medium level IR, such as the toy IR of this area, has scalar variables, arithmetic, branches and calls, and no machine registers. A low level IR shows addressing modes, machine registers and the calling convention, so that instruction selection, [register allocation](/register-allocation-problem/) and [instruction scheduling](/instruction-scheduling-problem/) can work on it. Muchnick calls these three levels HIR, MIR and LIR. A compiler lowers the program step by step from one level to the next.

### What a good IR gives

- **Explicit names.** Each intermediate value has a name, so an analysis can talk about it and an optimization can reuse it.
- **Few instruction forms.** Each analysis and each transformation has a small case analysis.
- **Explicit control flow.** Jumps and branches are the only transfers of control, so the [control flow graph](/control-flow-graph/) can be read directly from the code.
- **A defined semantics.** Every transformation must keep the observable behavior. That is only checkable if the IR has a precise meaning, including the cases that trap or never stop.
- **Cheap updates.** Optimizations change the IR all the time, so insertion, deletion and replacement of instructions must be cheap.

No single IR is best for all tasks. A tree is good for source-level work but hides the order of evaluation. A linear form is easy to generate and to emit but makes the flow of values implicit. A graph of values makes the flow of values explicit but makes the order of side effects harder to keep.

### The toy IR of this area

The compiler pages of this site use one toy IR. A program is a list of blocks. Each block has a label, then instructions of the forms `x = k`, `x = y` and `x = a op b`, then one terminator: `jump L`, `br a L1 L2` (go to `L1` if `a` is not 0, else to `L2`) or `ret a`. The operator is one of `+ - * / % & | ^ << >> < <= == !=`, and comparisons give 0 or 1. The first block is the entry, and the parameters are the names read before any definition. Values are unbounded integers. `/` and `%` truncate toward zero and trap when the divisor is 0, and the shifts trap when the shift count is outside 0 to 63. SSA pages add `x2 = phi [entry: x0, body: x3]` at the top of a block, pointer pages add `p = &x`, `x = *p`, `*p = a` and `p = alloc`, and interprocedural pages add `x = call f(a, b)`. The Python helper `toyir.py`, which the pages with code share, parses and prints this form and runs it.

## Examples

### One loop at three levels

Take this source fragment:

```
s = 0; i = 0
while (i < n) { s = s + i * i; i = i + 1 }
return s
```

As an abstract syntax tree, the body of the loop is a sequence of two assignments. The first is `Assign(s, Add(Var(s), Mul(Var(i), Var(i))))`. The tree keeps the nesting of the expression, but not the order in which a machine computes it.

In stack machine code, which a JVM-like interpreter runs, the first assignment is `load s; load i; load i; mul; add; store s`. The operands are on an implicit stack, so no temporary has a name.

In the toy IR, the whole fragment is:

```
entry:
  s = 0
  i = 0
  jump head
head:
  t1 = i < n
  br t1 body exit
body:
  t2 = i * i
  s = s + t2
  i = i + 1
  jump head
exit:
  ret s
```

The parameter is `n`. The temporaries `t1` and `t2` are names that the source did not have. The loop is now four blocks, and its control flow is the edge list `entry -> head`, `head -> body`, `head -> exit`, `body -> head`. The run on $n = 4$ returns $0 + 1 + 4 + 9 = 14$, and the runs on $n = 0$ and $n = -3$ return 0, as the `toyir.py` interpreter confirms.

### What the toy IR makes easy

In the toy IR, an analysis that asks "which assignments to `s` can reach `ret s`" looks at two instructions and four edges. The answer is `s = 0` in `entry` (when the loop runs zero times) and `s = s + t2` in `body`. This is [reaching definitions](/reaching-definitions/). The same question on the source text must first decide what the `while` statement means.

The expression `i * i` is computed once per iteration into `t2`. If a later statement also needed `i * i`, a [local value numbering](/local-value-numbering/) pass could see that the two computations are the same, because both are one instruction with the same operator and operands.

### Lowering to SSA

[Static single assignment form](/static-single-assignment-form/) gives each assignment its own name and merges names at join points with a [phi-function](/phi-function/):

```
entry:
  s0 = 0
  i0 = 0
  jump head
head:
  s1 = phi [entry: s0, body: s2]
  i1 = phi [entry: i0, body: i2]
  t1 = i1 < n
  br t1 body exit
body:
  t2 = i1 * i1
  s2 = s1 + t2
  i2 = i1 + 1
  jump head
exit:
  ret s1
```

Now each use has exactly one definition, so the question about `s` is answered by the name alone: `ret s1` reads the phi in `head`.

## Where it is used

- **GCC** lowers C, C++ and other languages to GENERIC trees, then to GIMPLE, a three-address form on which most optimizations run (in SSA form), and then to RTL, a low level form close to the machine, for register allocation and scheduling.
- **LLVM** has one central IR: a typed three-address code in SSA form inside a control flow graph, with a text form, a binary form and an in-memory form that are equivalent. Clang, Swift, Rust and other front ends emit it (Lattner and Adve 2004).
- **The JVM and .NET** ship programs as stack machine code (Java bytecode, CIL). Just-in-time compilers translate it into their own graph IRs, for example the [sea of nodes](/sea-of-nodes/) in the HotSpot server compiler.
- **Functional language compilers** use typed lambda-calculus IRs such as GHC Core, or [continuation-passing style](/continuation-passing-style/) and [A-normal form](/a-normal-form/), and only later a control flow graph.
- **MLIR** lets one compiler mix many IRs, called dialects, at different levels in one program, and lower them step by step.
- **Program analysis tools** outside compilers, such as static checkers and verifiers, also translate the source into an IR first, for the same reason: fewer forms to handle.

## References
