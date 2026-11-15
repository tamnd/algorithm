---
tag: FJ003B
kind: technique
slug: self-optimizing-ast-interpreter
name: Self-optimizing AST interpreter
aliases:
- node rewriting interpreter
- Truffle approach
area: compilers-and-program-analysis/code-generation-and-jit
level: research
summary: An AST interpreter whose nodes rewrite themselves to specialized forms from observed types, then are compiled by partial evaluation.
prereqs: [abstract-syntax-tree, polymorphic-inline-cache, deoptimization]
see_also: [partial-evaluation, futamura-projections, meta-tracing, type-feedback, inline-caching, just-in-time-compilation, binding-time-analysis, function-inlining]
sources:
  - paper: doi:10.1145/2384577.2384587
    title: Thomas Würthinger, Andreas Wöß, Lukas Stadler, Gilles Duboscq, Doug Simon and Christian Wimmer, Self-optimizing AST interpreters, DLS 2012, 73-82
    locator: node rewriting for type specialization, inline caches as chains of nodes, the rule that rewrites move to more general nodes so the tree stabilizes, and the compilation of a stable tree by partial evaluation with deoptimization back to the interpreter
  - paper: doi:10.1145/3062341.3062381
    title: Thomas Würthinger, Christian Wimmer, Christian Humer, Andreas Wöß, Lukas Stadler, Chris Seaton, Gilles Duboscq, Doug Simon and Matthias Grimmer, Practical partial evaluation for high-performance dynamic language runtimes, PLDI 2017, 662-676
    locator: the partial evaluation of Truffle interpreters by the Graal compiler, the boundary between partial evaluation and normal compilation, transfer to the interpreter, and assumptions that invalidate compiled code
---

A self-optimizing AST interpreter runs a program by walking its [abstract syntax tree](/abstract-syntax-tree/), and while it runs, each node replaces itself with a version specialized to the values it has seen. An addition node that has only seen integers becomes an integer addition node; a call node that has only seen one target becomes a node that checks for that target and calls it directly. When a node meets a value that its specialization does not handle, it rewrites itself to a more general version and goes on. After a while the tree stops changing, and a compiler applies [partial evaluation](/partial-evaluation/) to the interpreter with the tree as constant input: it inlines all the node code into one piece of machine code for the method. The guards of the specialized nodes become [deoptimization](/deoptimization/) points that go back to the interpreter, which rewrites the node and lets the method be compiled again. Würthinger and others introduced the approach in 2012, and it is the base of the Truffle framework with the Graal compiler.

## In plain words

An interpreter that walks a syntax tree is easy to write but slow, because each node checks the kind of its values every time.

In this design each node learns. The first time `a + b` runs with two whole numbers, the node replaces itself with a node that only adds whole numbers, with a quick check in front. If it later gets a decimal, the check fails, and the node replaces itself with one that also handles decimals. Nodes only get more general, so after a while they stop changing.

Then a compiler glues the code of all the nodes of a method into one piece of fast machine code, keeping only the quick checks. If a check fails there, the program goes back to the tree, which learns, and the method is compiled again later.

## When it applies

- You implement a dynamic language and want good performance from an interpreter that is simple to write, in the style of a tree walker.
- The operations of the language have a few common cases, such as integer arithmetic or calls with one target, and a general case that is much slower.
- A compiler is available that can partially evaluate the interpreter, such as Graal for Truffle interpreters written in Java, and the runtime supports deoptimization.
- Programs run long enough for the trees to stabilize and for compilation to pay off.

## The template

### Specializations and rewriting

For each kind of operation, such as addition, the language implementer defines a finite set of node *specializations*, partially ordered from specific to general, with a single most general one that accepts every input. Each specialization $s$ has a domain $D_s$, the inputs it handles, and on those inputs computes the result of the operation $f$. The order must be such that a more general specialization handles at least the inputs of a more specific one. A typical chain for addition is

$$\text{Uninitialized} \;<\; \text{IntAdd} \;<\; \text{DoubleAdd} \;<\; \text{GenericAdd},$$

where Uninitialized handles no input, IntAdd handles two integers whose sum fits in 32 bits, DoubleAdd handles any two numbers, and GenericAdd handles everything, including strings.

```
EXECUTE(node)
L1  v ← the values of the children of node, each computed by EXECUTE
L2  if v is in the domain of node's specialization then return its result on v
L3  s' ← the most specific specialization above the current one whose domain holds v
L4  replace node in the tree by a node of specialization s', with the same children
L5  return the result of s' on v
```

Line L3 always finds an $s'$, because the most general specialization handles every input. Line L4 changes the tree, which is the *self-optimizing* part. Inline caches fit the same scheme: an uninitialized call node becomes a chain of nodes, each testing one receiver class and calling its target, like a [polymorphic inline cache](/polymorphic-inline-cache/), and the chain is replaced by a generic lookup node when it grows too long.

### Why rewriting keeps the meaning and stops

**Claim 1.** Each call EXECUTE(node) returns $f(v)$, the result of the operation of the node on the values of its children, whatever the specialization of the node.

*Proof.* The values $v$ are computed once, at line L1. If $v$ is in the domain of the current specialization, line L2 returns its result, which is $f(v)$ on its domain. Otherwise line L3 picks $s'$ with $v \in D_{s'}$, and line L5 returns the result of $s'$ on $v$, which is $f(v)$. The children are not run again, so their effects happen once, as in a plain interpreter. $\square$

**Claim 2.** If the longest chain in the order of specializations of each kind of node has $h$ steps, a tree of $N$ nodes is rewritten at most $N h$ times in total.

*Proof.* Line L4 replaces a node by one whose specialization is strictly above the current one, because the current one did not handle $v$ and $s'$ is chosen above it. Nodes created by a rewrite take the place of the old node and keep its children. So for each position in the tree, the specializations along its rewrites form a strictly increasing chain, which has at most $h$ steps. With $N$ positions there are at most $N h$ rewrites. $\square$

So the tree *stabilizes*: after finitely many rewrites, every execution takes line L2. Claim 2 relies on the rule that rewriting only goes up. A design that also rewrote nodes back to more specific forms could change forever.

### Compiling a stable tree by partial evaluation

When a method has run often and its tree has not changed for a while, the system compiles it. The interpreter code of the nodes is the program, and the tree is a constant input. Partial evaluation of EXECUTE on the root with this constant input does the following: each call to the EXECUTE method of a child is a call on a constant object, so its target is known and it is inlined; the fields of the nodes are constants; and the code that remains works only on the values of the user program. This is the first [Futamura projection](/futamura-projections/), applied to one method at run time.

In the compiled code, line L2 becomes a guard and lines L3 to L5 are not compiled. In their place is a *transfer to the interpreter*: a [deoptimization](/deoptimization/) that rebuilds the interpreter state and runs EXECUTE there, which rewrites the node. Because the compiled code was made for the old tree, it is also invalidated. Facts that are not local to a node, such as "this global variable was never reassigned", are handled with *assumptions*: objects that compiled code depends on, which the runtime invalidates when the fact changes, so that the dependent code is deoptimized.

**Claim 3.** If partial evaluation is correct, and each guard of a specialization transfers to the interpreter with the exact interpreter state, then the compiled code of a method has the same outcome as interpreting the method with its tree.

*Proof.* Correct partial evaluation means that the residual program, run on the remaining inputs, has the same outcome as the interpreter run on the constant tree and those inputs, as long as the tree does not change. The tree changes only at line L4, which in the compiled code is replaced by a transfer to the interpreter before any rewrite happens. By the exactness of the transfer, the interpreter continues from the state that the interpreter alone would have at that node, and by Claim 1 it computes the same results from there. $\square$

### A worked example

One addition node runs six times with these operands, in a language with 32-bit integers that overflow into doubles:

| run | operands | specialization before | in its domain? | specialization after | result |
|---|---|---|---|---|---|
| 1 | 3, 4 | Uninitialized | no | IntAdd | 7 |
| 2 | 5, 6 | IntAdd | yes | IntAdd | 11 |
| 3 | 2147483647, 1 | IntAdd | no, the sum overflows | DoubleAdd | 2147483648 |
| 4 | 2.5, 1 | DoubleAdd | yes | DoubleAdd | 3.5 |
| 5 | "a", "b" | DoubleAdd | no | GenericAdd | "ab" |
| 6 | 1, 2 | GenericAdd | yes | GenericAdd | 3 |

There are 3 rewrites, which equals the height $h = 3$ of the chain, and from run 6 on the node never changes. Every result equals the result of a plain interpreter with a single generic addition. If the method had been compiled after run 2, the compiled code would hold an integer addition with an overflow guard, and run 3 would deoptimize, rewrite the node to DoubleAdd, and invalidate the compiled code.

## Classic examples

- **Truffle and Graal.** Truffle is a Java framework for self-optimizing AST interpreters, and the Graal compiler partially evaluates them. Implementations of JavaScript, Ruby, Python, R and other languages are built on it. Würthinger and others describe the partial evaluation in detail in 2017, including how the compiler decides where partial evaluation stops and normal compilation starts.
- **Inline caches as nodes.** A message send in a Truffle interpreter is a node that rewrites itself into a chain of cached cases, the same structure as a polymorphic inline cache, but written as ordinary interpreter code that the partial evaluator compiles.
- **Quickening in bytecode interpreters.** Bytecode interpreters that rewrite an instruction to a type-specialized form after the first run, as in CPython 3.11, apply the same idea to bytecode instead of to a tree.

## Variations

- **Generated specializations.** In Truffle a domain-specific language of annotations describes the specializations of an operation, and a code generator writes the nodes, the guards and the rewriting.
- **Tree splitting.** A method called from many places has one tree that collects the types of all callers. Copying the tree for a hot caller gives each copy its own, more specific, specializations, which plays the role of profiles per caller in [type feedback](/type-feedback/).
- **Boxing elimination.** A node that is specialized to integers can return a primitive integer instead of an object, and the partial evaluator removes the boxes between nodes.
- **Tracing instead of partial evaluation.** [Meta-tracing](/meta-tracing/) reaches the same goal, a compiler from an interpreter, by tracing the interpreter along one hot path instead of partially evaluating it along all paths of a method.

## Pitfalls

- **Rewriting in both directions.** If nodes can also become more specific again, Claim 2 fails and a node can change forever, causing endless deoptimization and recompilation. Only move up.
- **Running children twice.** A rewrite must reuse the values that the children already computed. Calling EXECUTE on the children again repeats their effects.
- **Unstable trees.** Compiling a tree that still changes leads to repeated deoptimization. Wait until the tree has been stable for a while, and limit recompilations per method.
- **Code that partial evaluation cannot see through.** Calls whose target is not constant, recursion in the interpreter code, or loops over data structures that are not constant stop the inlining. The interpreter must be written so that the parts that depend only on the tree are visible as constants, and must mark where partial evaluation stops.
- **Speed claims.** The performance of Truffle languages is reported as measurements on given benchmarks and machines. The method gives a compiler from an interpreter, not a guarantee of speed.

## Exercises

1. Extend the worked example with a run (1.5, "x") after run 6. What happens, and why does the claim on rewrites still bound the total?
2. Design the specializations of a node for property reads `o.x`, with an uninitialized state, a chain of cached shapes like the [hidden classes](/hidden-classes/) page, and a generic state. What is $h$ for a chain bound of 3?
3. Show that if IntAdd could rewrite itself back to Uninitialized after 1000 runs on doubles, a program exists for which the number of rewrites is unbounded.
4. Explain why the partial evaluator can inline the call to the EXECUTE method of a child, but not a call to a user function whose target is read from a variable of the user program. How does a call node with an inline cache solve this?
5. Write the residual code that partial evaluation should give for the tree of `while (i < n) { s = s + i; i = i + 1 }` when all nodes are specialized to integers, with each guard marked as a transfer to the interpreter.

## References
