---
tag: 8XWVZX
kind: concept
slug: dataflow-analysis
name: Dataflow analysis
aliases:
- data-flow analysis
- flow analysis
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: intro
summary: Computes facts that hold at each program point on all paths, by propagating them along the control flow graph to a fixed point.
prereqs: [control-flow-graph, basic-block]
see_also: [monotone-dataflow-framework, worklist-dataflow-algorithm, maximal-fixed-point-solution, gen-kill-problem, live-variable-analysis, available-expressions, constant-propagation-problem, abstract-interpretation]
sources:
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the whole paper (facts on a meet semilattice, one optimizing function per node, the iterative algorithm, and constant propagation and common subexpressions as instances)
  - paper: doi:10.1007/BF00290339
    title: "John B. Kam and Jeffrey D. Ullman, Monotone data flow analysis frameworks, Acta Informatica 7(3), 1977, 305-317"
    locator: the whole paper (monotone frameworks, the maximal fixed point, and the proof that no algorithm computes the meet over all paths solution of every monotone framework)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.2 (Introduction to Data-Flow Analysis, with reaching definitions, live variables and available expressions) and Section 9.3 (Foundations of Data-Flow Analysis)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 9 (Data-Flow Analysis), Section 9.2 (Iterative Data-Flow Analysis)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Chapter 2 (Data Flow Analysis), Sections 2.1 to 2.4
---

Dataflow analysis is a family of static analyses that compute, for each point of a program, a fact that holds whenever execution reaches that point: which definitions can reach it, which variables are still needed, which expressions are already computed. It works on the [control flow graph](/control-flow-graph/): it gives each [basic block](/basic-block/) a transfer function, writes one equation per block, and solves the equations by iteration to a [fixed point](/fixed-point/). This page is the concept. The exact definitions are on [monotone dataflow framework](/monotone-dataflow-framework/) and [distributive dataflow framework](/distributive-dataflow-framework/), the bit-vector class is [gen-kill problem](/gen-kill-problem/), the solver is the [worklist dataflow algorithm](/worklist-dataflow-algorithm/), and the two possible answers are the [meet-over-all-paths solution](/meet-over-all-paths-solution/) and the [maximal fixed-point solution](/maximal-fixed-point-solution/).

## In plain words

A compiler wants to know things about a program before it runs it. Is this value used again later? Was this sum already computed on every way to get here? The compiler cannot try every input, so it reasons about the shape of the program instead.

It draws the program as a map of straight-line pieces joined by jumps. At each piece it keeps a small note of what it knows so far. Each piece has a rule that turns the note at its start into the note at its end. Where two ways meet, the compiler combines the notes into one note that is true on both ways. It goes around the map and updates the notes. A loop sends notes back to earlier pieces, so one pass is not enough. When a full round changes no note, the notes are stable, and the compiler uses them.

## The idea

**Points and facts.** A *program point* is the point just before or just after a block (or an instruction). The analysis attaches to each point a value from a set $L$ of facts. For reaching definitions a fact is a set of definition sites; for constant propagation it is a map from variables to "this constant" or "not a constant". The examples here use the toy IR of the area: [three-address code](/three-address-code/) in basic blocks, with `jump`, `br` and `ret` as terminators.

**The order on facts.** Facts are ordered by how much they claim. A *partial order* $\sqsubseteq$ is reflexive, antisymmetric and transitive. A *meet semilattice* $(L, \sqcap)$ is a set with a binary operation $\sqcap$ that is idempotent, commutative and associative; it defines the order $x \sqsubseteq y$ if and only if $x \sqcap y = x$, and then $x \sqcap y$ is the greatest lower bound of $x$ and $y$. This page and the other dataflow pages use this meet convention of Kildall and the dragon book. $\top$ is the identity of meet ($x \sqcap \top = x$ for all $x$); it is the optimistic start value, "no information against any claim yet". Lower means a weaker claim: more conservative, but still safe. The *height* $h$ of $L$ is the largest $k$ such that a strict chain $x_0 \sqsupset x_1 \sqsupset \cdots \sqsupset x_k$ exists. A [join semilattice](/join-semilattice/) is the same structure with the order turned upside down, and turning the order upside down maps this convention onto the one of [abstract interpretation](/abstract-interpretation/), where $\bot$ is the start value and the answer is a least fixed point.

**Transfer functions and direction.** Each block $B$ has a transfer function $f_B : L \to L$. A *forward* problem maps the fact at the start of $B$ to the fact at its end; a *backward* problem maps the fact at the end to the fact at the start, so it runs on the reverse CFG. The *boundary value* $\iota$ is the fact at the entry block (forward) or after each `ret` block (backward). It is a fact about the outside world, and it is not $\top$ in general.

**The equations.** For a forward problem, with the empty meet equal to $\top$:

$$\mathrm{IN}[B] = \Big(\iota \text{ if } B \text{ is the entry}\Big) \sqcap \mathop{\large\sqcap}_{P \in \mathrm{pred}(B)} \mathrm{OUT}[P], \qquad \mathrm{OUT}[B] = f_B(\mathrm{IN}[B]).$$

For a backward problem, swap IN with OUT and predecessors with successors, and put $\iota$ in the meet of each block that ends in `ret`.

**May and must.** The meet says what happens where paths join. In a *may* problem a fact holds if it holds on some path, so the meet is union and $\top = \emptyset$. In a *must* problem a fact holds only if it holds on every path, so the meet is intersection and $\top$ is the set of all facts. Reaching definitions and live variables are may problems; available expressions and very busy expressions are must problems.

**The ideal answer and the computed answer.** The ideal answer at the start of $B$ is the [meet over all paths](/meet-over-all-paths-solution/) from the entry to $B$ of the composed transfer functions of each path, applied to $\iota$. Iteration from $\top$ computes instead the [maximal fixed point](/maximal-fixed-point-solution/) of the equations. When every $f_B$ is monotone, MFP $\sqsubseteq$ MOP, so MFP is safe; when every $f_B$ distributes over $\sqcap$, the two are equal (Kildall 1973; Kam and Ullman 1977). The [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/) states this.

**Why it is safe, and why it is not exact.** Every real execution follows a path of the CFG, so a fact that holds on all CFG paths holds on every execution. The converse fails: the CFG also has paths that no input takes, for example both arms of two branches on the same test. So the analysis is conservative. It cannot be exact in general. Put a read of `y` after a piece of code that halts only on some inputs: `y` is truly live before that code only if the code can halt, so an exact liveness analysis would decide the [halting problem](/halting-problem/). [Rice's theorem](/rice-theorem/) gives the same limit for every nontrivial property of program behavior. Even the meet over all CFG paths cannot be computed for every monotone framework (Kam and Ullman 1977).

**Cost.** With a lattice of height $h$, a CFG with $n$ blocks and $m$ edges, and a worklist, each block value falls at most $h$ times, so the solver does $O(n h)$ transfer applications and $O(m h)$ meets. For a bit-vector problem over $u$ facts, $h = u$ and one set operation costs $O(u / w)$ machine words, with $w$ the word size.

## Examples

The running example of the dataflow pages has the parameters `n` and `x`. It sums `x * 2` over the odd values of `i` below `n`.

```
entry:
  i = 0
  s = 0
  jump head
head:
  t = i < n
  br t body done
body:
  a = x * 2
  u = i & 1
  br u odd next
odd:
  s = s + a
  jump next
next:
  i = i + 1
  jump head
done:
  ret s
```

The CFG has six blocks and seven edges: entry to head, head to body, head to done, body to odd, body to next, odd to next, and next to head, which closes the loop. On the input `n = 5`, `x = 3` the program returns 12.

**A may problem: live variables.** A variable is live at a point if some path from that point reads it before it is written. The analysis is backward with union, and the boundary value after `ret` is the empty set. At the start of each block it gives:

| block | live at the start | available at the start |
|---|---|---|
| entry | n, x | none |
| head | i, n, s, x | none |
| body | i, n, s, x | i < n |
| odd | a, i, n, s, x | i < n, x * 2, i & 1 |
| next | i, n, s, x | i < n, x * 2, i & 1 |
| done | s | i < n |

Only `n` and `x` are live at the entry: they are the parameters, and every other name is written before it is read. `a` is live only between `body` and `odd`, so a register allocator can reuse its register in the rest of the loop.

**A must problem: available expressions.** An expression is available at a point if every path to the point computes it and changes none of its operands after that. The analysis is forward with intersection, and the boundary value at the entry is the empty set. In the third column of the table, `x * 2` is available in `odd`, so `s = s + a` could reuse it, but it is not available in `head`: the path from `entry` never computed it. If the analysis started the entry at $\top$ (all expressions) instead of the empty set, it would claim that `x * 2` is available in `head`. That is the boundary trap of must problems.

**The loop needs more than one pass.** For live variables the worklist processes 11 blocks before it stops, not 6, because `x` and `a` become live in `body` only after the facts travel back around the loop. The trace is on the [worklist dataflow algorithm](/worklist-dataflow-algorithm/) page.

**Non-example: a precise answer that dataflow analysis misses.** Constant propagation on two branches that set $(x, y)$ to $(2, 3)$ and to $(3, 2)$, followed by `z = x + y`, gives $z$ = "not a constant", although $z = 5$ on every path. The meet merges $x$ and $y$ separately before the sum. The [constant propagation](/constant-propagation-problem/) problem is monotone but not distributive, so its MFP can be strictly below its MOP.

## Where it is used

- **Optimization.** Live variables drive [dead code elimination](/dead-code-elimination/) and the [interference graph](/interference-graph/) of [register allocation](/register-allocation-problem/). Available expressions drive global [common subexpression elimination](/common-subexpression-elimination/). Very busy (anticipated) expressions and available expressions together drive [partial redundancy elimination](/partial-redundancy-elimination/) and [lazy code motion](/lazy-code-motion/). Reaching definitions build [def-use chains](/def-use-chains/) for [copy propagation](/copy-propagation/) and [loop-invariant code motion](/loop-invariant-code-motion/).
- **SSA form.** [Pruned SSA form](/pruned-ssa-form/) places a phi-function only where the variable is live. On SSA form, sparse analyses such as [sparse conditional constant propagation](/sparse-conditional-constant-propagation/) follow def-use edges instead of CFG edges.
- **Bug finding and security.** A read of a variable that has no reaching definition is a use before initialization. [Taint analysis](/taint-analysis/) is a may problem that tracks values from untrusted sources.
- **Whole programs.** [Interprocedural dataflow analysis](/interprocedural-dataflow-analysis/) and the [IFDS framework](/ifds-framework/) extend the same equations across calls, and count only paths whose returns match their calls.
- **Other solvers.** [Datalog-based program analysis](/datalog-program-analysis/) writes the equations as Datalog rules and evaluates them with [semi-naive evaluation](/semi-naive-evaluation/). [Elimination methods](/elimination-dataflow-methods/) solve them by graph reduction instead of iteration.

## References
