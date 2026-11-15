---
tag: JMEDV5
kind: problem
slug: very-busy-expressions
name: Very busy expressions
aliases:
- anticipable expressions
- anticipated expressions
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: For each program point, find the expressions that every path from it computes before any of their operands change.
prereqs: [available-expressions, live-variable-analysis]
see_also: [lazy-code-motion, partial-redundancy-elimination, loop-invariant-code-motion, available-expressions, live-variable-analysis, gen-kill-problem, worklist-dataflow-algorithm, post-dominance]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.5.4 (Anticipation of Expressions, the backward must problem used as the first pass of lazy code motion)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Section 2.1.3 (Very Busy Expressions Analysis, a backward analysis where the answer is the largest solution)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 9 (Data-Flow Analysis), Section 9.2.4 (Other Data-Flow Problems)
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the whole paper (the iterative algorithm on a meet semilattice, which solves this problem on the reverse graph)
---

Very busy expressions is the backward must problem of [dataflow analysis](/dataflow-analysis/). An expression such as `i + 1` is *very busy* (or *anticipated*) at a program point $p$ if every path in the [control flow graph](/control-flow-graph/) from $p$ to a return evaluates it before any of its operands is written. At such a point the expression can be computed early: every path that goes on to a return would compute the same value anyway. The problem asks for the set of very busy expressions at the start and the end of every [basic block](/basic-block/). It is the mirror image of [available expressions](/available-expressions/) (backward instead of forward) and has the same meet as available expressions and the same direction as [live variable analysis](/live-variable-analysis/). It is the first pass of [lazy code motion](/lazy-code-motion/). It is a [gen-kill problem](/gen-kill-problem/), so the [worklist dataflow algorithm](/worklist-dataflow-algorithm/) on the reverse CFG computes its [meet-over-all-paths solution](/meet-over-all-paths-solution/).

## In plain words

Stand at some point in a program and look ahead. If every way forward computes `i + 1` before it changes `i`, then the value of `i + 1` is already decided where you stand. You could compute it here, once, and let the later places reuse it.

The compiler finds these expressions by reading the program backward from the returns. A block adds the expressions it computes and drops the ones whose inputs it changes before computing them. Where the program branches, an expression stays only if every branch computes it. Loops make the compiler repeat the backward walk until nothing changes.

Moving a computation to such a point never adds work to a run that returns, which is why the answer is safe to use.

## Definition

**Input.** A [control flow graph](/control-flow-graph/) with $n$ blocks and $m$ edges, in [three-address code](/three-address-code/), with the set $E$ of expressions `a op b` that occur in it.

**Output.** For every block $B$, the set $\mathrm{IN}[B] \subseteq E$ of expressions very busy at its start, and $\mathrm{OUT}[B]$ at its end.

**The framework.**

| property | value |
|---|---|
| direction | backward: the analysis runs on the reverse CFG |
| may or must | must: busy only if every path evaluates the expression |
| domain $L$ | the subsets of $E$ |
| order $\sqsubseteq$ | $\subseteq$ |
| meet $\sqcap$ | $\cap$ |
| $\top$ and $\bot$ | $\top = E$, $\bot = \emptyset$ |
| boundary value $\iota$ | $\emptyset$ at the end of each block that ends in `ret`: after the return nothing is evaluated |
| start value elsewhere | $E$ ($\top$) |
| transfer functions | $f_B(X) = use_B \cup (X - kill_B)$, monotone and distributive |
| height $h$ | $\lvert E \rvert$ |

As for [available expressions](/available-expressions/), the boundary is $\bot = \emptyset$ and the start value elsewhere is $\top = E$. The answer is the greatest fixed point, here the largest sets.

**Lattice and height.** The subsets of $E$ ordered by $\subseteq$; a strict chain removes one expression per step, so $h = |E|$.

**Transfer functions.** Read each block from its end to its start. An instruction `x = a op b` first evaluates `a op b` and then writes `x`. Going backward, the write comes first: it removes $kill_x$, the expressions with `x` as an operand, and then the evaluation adds `a op b`. So the step is $X \mapsto \{a \text{ op } b\} \cup (X - kill_x)$, and `s = s + a` makes `s + a` very busy before it. A constant or copy into `x` only removes $kill_x$. Composing the steps from the last instruction to the first gives $use_B$, the expressions that $B$ evaluates before writing any of their operands, and $kill_B$, the expressions with an operand that $B$ writes.

**Equations.** With the empty intersection equal to $E$:

$$\mathrm{OUT}[B] = \Big(\emptyset \text{ if } B \text{ ends in } \texttt{ret}\Big) \cap \bigcap_{S \in \mathrm{succ}(B)} \mathrm{IN}[S], \qquad \mathrm{IN}[B] = use_B \cup (\mathrm{OUT}[B] - kill_B).$$

**Meet over all paths.** For a path $\pi$ from the end of $B$ to the end of a `ret` block, $f_\pi(\emptyset)$ is the set of expressions that $\pi$ evaluates before writing an operand. MOP is the intersection over all such paths.

**The fixed point computed.** The [worklist dataflow algorithm](/worklist-dataflow-algorithm/) runs on the reverse CFG with the `ret` blocks as start nodes, gives them $\iota = \emptyset$, starts every other set at $E$, and shrinks the sets. It stops at the [maximal fixed-point solution](/maximal-fixed-point-solution/), which equals MOP when every block can reach a `ret` block, because the functions are distributive.

**Soundness.** If $e \in \mathrm{OUT}[B]$ and a run leaves $B$ and later returns, the part of the run up to the return follows a CFG path from the end of $B$ to a `ret` block, and on that path $e$ is evaluated before its operands change. So computing $e$ at the end of $B$ gives the value that the run would compute later, and adds no evaluation to the run. A run that never returns is not covered; see Variants.

**Precision.** CFG paths that no run takes make the sets smaller than the truth. Here every run computes `x * 2` after `entry`: through `p` if `c` is true, and through `s` if `c` is false. But the CFG path through `q` and then `r` computes nothing, so `x * 2` is not very busy at the end of `entry`, and it cannot be hoisted there.

```
entry:
  br c p q
p:
  a = x * 2
  jump m
q:
  jump m
m:
  br c r s
r:
  ret a
s:
  b = x * 2
  ret b
```

**Cost.** With bit vectors of $|E|$ bits, the worklist algorithm applies at most $n(|E| + 1)$ transfer functions and $m(|E| + 1)$ intersections of $O(|E| / w)$ words each, so $O((n + m) |E|^2 / w)$ time in the worst case. Round-robin iteration in reverse postorder of the reverse CFG takes $O((d + 2)(n + m) |E| / w)$, where $d$ is the loop-connectedness depth of the reverse CFG ([Kam-Ullman iteration bound](/kam-ullman-iteration-bound/)).

## Variants

- **Paths that never return.** A block from which no `ret` block can be reached, such as an infinite loop, keeps the start value $E$: there is no path to a return, so the claim "every such path evaluates $e$" holds for every $e$. The value flows to the blocks before it. An optimizer that hoists an expression into such a region can add an evaluation that the run would never do; if the expression can trap, such as a division, that changes the behavior. A safe optimizer either adds an exit edge from each such region, or treats the end of each such region as a boundary with $\iota = \emptyset$.
- **Anticipated expressions in lazy code motion.** The dragon book calls these sets anticipated expressions. [Lazy code motion](/lazy-code-motion/) then uses them with available expressions to find the earliest safe point for each computation.
- **Partially anticipated expressions.** Replacing $\cap$ with $\cup$ gives the may version: some path evaluates the expression. Some forms of [partial redundancy elimination](/partial-redundancy-elimination/) use it as well.

## Examples

The running example of [dataflow analysis](/dataflow-analysis/) has five expressions: `i < n`, `x * 2`, `i & 1`, `s + a` and `i + 1`.

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

| block | $use_B$ | $kill_B$ | IN (busy at the start) | OUT (busy at the end) |
|---|---|---|---|---|
| entry | none | `i < n`, `i & 1`, `i + 1`, `s + a` | none | `i < n` |
| head | `i < n` | none | `i < n` | none |
| body | `x * 2`, `i & 1` | `s + a` | `x * 2`, `i & 1`, `i + 1` | `i + 1` |
| odd | `s + a` | `s + a` | `s + a`, `i + 1` | `i + 1` |
| next | `i + 1` | `i < n`, `i & 1`, `i + 1` | `i + 1` | `i < n` |
| done | none | none | none | none |

- `i + 1` is very busy at the end of `body`: both `odd` and `next` compute it, and `odd` does not write `i`. So `i + 1` could be computed once at the end of `body`. This makes the code smaller (code hoisting) but not faster, since each path still computes it once.
- `i < n` is very busy at the end of `entry` and of `next`, because `head` computes it first thing.
- Nothing is very busy at the end of `head`: the path to `done` evaluates nothing before it returns.
- `odd` has `s + a` in both $use$ and $kill$, but the evaluation comes before the write, so `s + a` is busy at its start.

The worklist on the reverse CFG, in the order `done`, `head`, `next`, `odd`, `body`, `entry`, needs one pass: 6 transfer functions and 7 intersections, with each set changing at most once.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| [Worklist dataflow algorithm](/worklist-dataflow-algorithm/) on the reverse CFG | $O((n + m) \lvert E \rvert^2 / w)$ worst case | start at $E$ except after the `ret` blocks |
| Round-robin in reverse postorder of the reverse CFG | $O((d + 2)(n + m) \lvert E \rvert / w)$ | [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/) |
| One backward search per expression on the complement | $O(\lvert E \rvert (n + m))$ | see Reductions |

## Bounds

The output can have $\Theta(n \lvert E \rvert)$ entries: if the last block before the only return computes $\lvert E \rvert$ expressions over parameters that nothing writes, and every path goes through it, every expression is very busy in all $n$ blocks. So listing the sets needs $\Omega(n \lvert E \rvert)$ time in the worst case.

## Reductions

- **To a may problem by complement.** The sets $E - \mathrm{IN}[B]$ of expressions that are not very busy satisfy a backward may problem with union, the transfer function $X \mapsto (kill_B - use_B) \cup (X - use_B)$, and the boundary $E$ after each `ret` block.
- **To graph reachability on the reverse CFG.** Through the complement, $e \notin \mathrm{OUT}[B]$ if and only if some path from the end of $B$ reaches a return, or a block that writes an operand of $e$ before it evaluates $e$, through blocks that do not evaluate $e$. One backward search per expression finds these blocks. This is [graph reachability](/graph-reachability/) on the [transpose graph](/transpose-graph/).
- **Mirror of available expressions.** On the reverse CFG with the order of the instructions in each block reversed, very busy expressions become available expressions, with one change: an instruction `x = a op b` keeps `a op b` even when `x` is an operand, since the evaluation comes first in the original order.

## Applications

- **Code hoisting.** An expression that is very busy at the end of a block can be computed there once instead of in each successor. This saves space, not time.
- **Lazy code motion and partial redundancy elimination.** Anticipation tells [lazy code motion](/lazy-code-motion/) where a computation may be inserted without adding work on any path. Together with [available expressions](/available-expressions/) it gives the earliest safe placement, and two more passes push it as late as possible.
- **Safe loop-invariant code motion.** Hoisting an invariant expression to the loop preheader is safe from new traps if the expression is very busy at the preheader, that is, every path from there evaluates it. See [loop-invariant code motion](/loop-invariant-code-motion/).

## References
