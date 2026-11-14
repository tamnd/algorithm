---
tag: FQABB0
kind: definition
slug: static-single-assignment-form
name: Static single assignment form
aliases:
- SSA form
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: An IR where each variable has exactly one definition, with phi-functions at join points that choose a value by the incoming edge.
prereqs: [control-flow-graph, three-address-code, dominators-problem]
see_also: [phi-function, dominance-frontier, ssa-construction-problem, pruned-ssa-form, out-of-ssa-translation, def-use-chains, ssa-chordal-interference-theorem, static-single-information-form]
sources:
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: the definition of SSA form and of the phi-function, minimal SSA form, and the measurements of the number of phi-functions
  - paper: doi:10.1145/73560.73562
    title: Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Global value numbers and redundant computations, Proceedings of the 15th ACM Symposium on Principles of Programming Languages (POPL), 1988, pages 12-27
    locator: the first use of the single assignment property and of phi-functions at join points for global value numbering
  - book: isbn:9783030805142
    title: Fabrice Rastello and Florent Bouchez Tichadou (editors), SSA-based Compiler Design, Springer, 2022
    locator: Chapter 2 (Properties and Flavours), strict, minimal, pruned and conventional SSA; Chapter 3 (Standard Construction and Destruction Algorithms)
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 19 (Static Single-Assignment Form)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 9 (Data-Flow Analysis), the section on static single-assignment form
---

Static single assignment (SSA) form is a way to write a program in an [intermediate representation](/intermediate-representation/) so that each variable has exactly one definition in the program text. When a source variable is assigned at several points, each assignment gets a new name, such as `x.1`, `x.2` and `x.3`. When different names of one source variable reach a join point of the [control flow graph](/control-flow-graph/), the form adds a [phi-function](/phi-function/) at the top of the join block. The phi-function picks the value that belongs to the edge on which control came in. Because each name has one definition, each use has exactly one reaching definition, and many analyses become simple and fast. Rosen, Wegman and Zadeck used the idea in 1988, and Cytron, Ferrante, Rosen, Wegman and Zadeck (1991) gave the efficient construction. GCC and LLVM both use SSA form for their main optimizations.

## Definition

### The single assignment rule

Let a procedure be in [three-address code](/three-address-code/) on a control flow graph $G = (N, E, r)$ with entry $r$. The procedure is in *SSA form* if these conditions hold:

1. Each name is the target of at most one instruction in the program text. The parameters count as defined at the entry, so no instruction assigns to a parameter.
2. Phi-functions appear only at the top of a block, before all other instructions.
3. A phi-function in block $b$ has exactly one operand for each incoming edge $(p, b)$. In the toy IR of this site it is written `x.3 = phi [B2: x.1, B3: x.2]`, with one entry for each predecessor.

The rule is *static*: a name has one definition in the text, but a definition inside a loop can run many times. Each run gives the name a new value.

### What a phi-function does

When control moves along the edge $(p, b)$, all phi-functions at the top of $b$ take their operand for $p$. They read all their operands first and then assign all their targets. So the phi-functions of one block act as one *parallel copy*. The order in which they are written does not matter. This rule is a trap for code that runs the phi-functions one by one: if `a.2 = phi [B2: b.2, ...]` comes before `b.2 = phi [B2: a.2, ...]`, a sequential reading gives `b.2` the new value of `a.2`, not the old one. The [lost copy and swap problems](/lost-copy-and-swap-problems/) come from this.

A phi-function operand counts as a use at the end of the predecessor $p$, not in $b$. This matters for liveness and for dominance.

### Strict SSA

A program in SSA form is *strict* if the definition of each name [dominates](/dominators-problem/) each of its uses. For a phi operand, the use is at the end of the matching predecessor. In strict SSA form, every path from the entry to a use passes through the definition, so no run reads a name that has no value.

A source program that can read a variable before it assigns it, on some path, has no strict SSA form as it stands. The usual fix is to add a definition at the entry, such as `v.0 = 0` or `v.0 = undef`, so that the definition dominates every use. Most construction and destruction algorithms, and most results on SSA form, assume strictness. The [chordal interference theorem](/ssa-chordal-interference-theorem/) is one of them.

### Flavours

- **Minimal SSA.** A phi-function for $v$ is placed at a block $b$ only if two different definitions of $v$ reach $b$ along paths that meet first at $b$. Cytron et al. showed that these blocks are the iterated [dominance frontier](/dominance-frontier/) of the blocks that assign $v$. Minimal SSA can still have dead phi-functions.
- **[Pruned SSA](/pruned-ssa-form/).** Minimal SSA without the phi-functions for variables that are dead at the top of the block. Semi-pruned SSA is a cheaper middle way that skips only the variables used in one block.
- **Conventional SSA (CSSA).** The names that a phi-function connects can all be replaced by one name, and the phi-functions dropped, without a change in behaviour. The output of the standard construction is conventional. Copy propagation and other optimizations can break this, and the result is called transformed SSA. The [out-of-SSA translation](/out-of-ssa-translation/) must handle it.

### Size

A program in SSA form has at most one phi-function per variable per block, so the phi-functions add at most $|V| \cdot |N|$ instructions, for $|V|$ variables and $|N|$ blocks. Each phi-function has one operand per incoming edge. The iterated dominance frontiers can be quadratic in the number of blocks, so in the worst case minimal SSA has $\Theta(|N|^2)$ phi-functions for $\Theta(|N|)$ variables. Cytron et al. measured the number of phi-functions on real programs and found it grew about linearly with the size of the program.

### Why it helps

- **One reaching definition per use.** A use of `x.2` is reached only by the definition of `x.2`. The [def-use chains](/def-use-chains/) are explicit and small: one definition and a list of uses per name. In code that is not in SSA form, $k$ definitions of a variable that reach $k$ uses through one join give $k^2$ chains. In SSA form the join gets one phi-function and the count is $2k$.
- **Sparse analyses.** An analysis can follow def-use edges and skip the blocks that do not touch a value. [Sparse conditional constant propagation](/sparse-conditional-constant-propagation/) and [global value numbering](/global-value-numbering/) work this way.
- **Values, not variables.** A name stands for one value. Two equal names always have equal values, which makes redundancy and copy elimination easier.

## Examples and non-examples

### Straight-line code

```
x = a + b
x = x * 2
y = x + 1
```

becomes

```
x.1 = a + b
x.2 = x.1 * 2
y.1 = x.2 + 1
```

Inside one block no phi-function is needed. Each use takes the name of the latest definition above it.

### A diamond

```
# params: a, b
B1:
  br a B2 B3
B2:
  x = b + 1
  jump B4
B3:
  x = b * 2
  jump B4
B4:
  y = x + a
  ret y
```

Two definitions of `x` reach B4, one from each side. In SSA form they get two names, and a phi-function at B4 joins them:

```
# params: a, b
B1:
  br a B2 B3
B2:
  x.1 = b + 1
  jump B4
B3:
  x.2 = b * 2
  jump B4
B4:
  x.3 = phi [B2: x.1, B3: x.2]
  y.1 = x.3 + a
  ret y.1
```

On $a = 1, b = 5$ both versions return 7, and on $a = 0, b = 5$ both return 10.

### A loop

This program, from the [control flow graph](/control-flow-graph/) page, adds the odd numbers below $n$:

```
# params: n
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

Its pruned SSA form is:

```
# params: n
B1:
  i.1 = 0
  s.1 = 0
  jump B2
B2:
  i.2 = phi [B1: i.1, B5: i.3]
  s.2 = phi [B1: s.1, B5: s.4]
  t1.1 = i.2 < n
  br t1.1 B3 B6
B3:
  t2.1 = i.2 % 2
  br t2.1 B4 B5
B4:
  s.3 = s.2 + i.2
  jump B5
B5:
  s.4 = phi [B3: s.2, B4: s.3]
  i.3 = i.2 + 1
  jump B2
B6:
  ret s.2
```

The loop header B2 needs phi-functions for `i` and `s`, because the value from before the loop and the value from the back edge meet there. B5 needs one for `s`, because B4 may or may not have changed it. The definition `i.3 = i.2 + 1` runs once in each iteration, but it is still one definition in the text. The use of `s.2` in B6 is dominated by its definition in B2, so the form is strict. On $n = 6$ both versions return 9, and on $n = 10$ both return 25.

The minimal SSA form of the same program also has phi-functions for `t1` and `t2` at B2, because both are assigned in the loop and B2 is in their iterated dominance frontier. Neither is live at the top of B2, so pruned SSA drops them.

### Non-examples

- **Two definitions of one name.** If both B2 and B3 above assign `x.1`, the program is not in SSA form, even though only one of the two runs on each path.
- **A phi-function with a missing operand.** `x.3 = phi [B2: x.1]` in a block with predecessors B2 and B3 is not valid. A run that comes from B3 has no value for `x.3`.
- **A phi-function after an ordinary instruction.** The phi-functions must be at the top of the block, because they act on the edge into it.
- **SSA form that is not strict.** In the diamond, if only B2 defines `x.1` and B4 reads `x.1` with no phi-function, each name still has one definition. The program is in SSA form, but it is not strict, and the run through B3 reads a name with no value.
- **Single assignment languages.** A pure functional program also assigns each name once, but it has no phi-functions and no control flow graph. The [SSA and CPS correspondence](/ssa-cps-correspondence/) maps one form to the other, with phi-functions as the parameters of local functions.

## Related definitions

- [Phi-function](/phi-function/): the join instruction, its operands and its parallel meaning.
- [Dominance frontier](/dominance-frontier/): the sets that give the blocks where phi-functions go.
- [SSA construction problem](/ssa-construction-problem/), [Cytron SSA construction](/cytron-ssa-construction/) and [Braun SSA construction](/braun-ssa-construction/): how to build the form.
- [Pruned SSA form](/pruned-ssa-form/): the flavour that drops dead phi-functions.
- [Out-of-SSA translation](/out-of-ssa-translation/), [lost copy and swap problems](/lost-copy-and-swap-problems/) and [Sreedhar CSSA translation](/sreedhar-cssa-translation/): how to leave the form before code generation.
- [Static single information form](/static-single-information-form/): an extension that also splits names at branches.
- [Sea of nodes](/sea-of-nodes/): a graph IR built on SSA values.
- [SSA chordal interference theorem](/ssa-chordal-interference-theorem/): the interference graph of a strict SSA program is chordal.

## References
