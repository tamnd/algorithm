---
tag: 9DTDJA
kind: problem
slug: available-expressions
name: Available expressions
aliases:
- available expressions analysis
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: intro
summary: For each program point, find the expressions computed on every path to it with no later change to their operands.
prereqs: [dataflow-analysis]
see_also: [common-subexpression-elimination, partial-redundancy-elimination, lazy-code-motion, very-busy-expressions, gen-kill-problem, worklist-dataflow-algorithm, global-value-numbering, reaching-definitions]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.2.6 (Available Expressions, with the e_gen and e_kill sets, the equations, and the reason the start value is the set of all expressions)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 9 (Data-Flow Analysis), Section 9.2.4 (Other Data-Flow Problems)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Section 2.1.1 (Available Expressions Analysis, where the answer is the largest solution)
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the whole paper (common subexpression elimination as an instance of the iterative algorithm on a meet semilattice)
---

Available expressions is the forward must problem of [dataflow analysis](/dataflow-analysis/). An expression such as `x * 2` is *available* at a program point $p$ if every path in the [control flow graph](/control-flow-graph/) from the entry to $p$ evaluates it, and no operand of it is written between the last evaluation and $p$. At such a point the value of the expression is already in some variable, so computing it again is redundant. The problem asks for the set of available expressions at the start and the end of every [basic block](/basic-block/). It drives global [common subexpression elimination](/common-subexpression-elimination/). It is a [gen-kill problem](/gen-kill-problem/), so the [worklist dataflow algorithm](/worklist-dataflow-algorithm/) computes its [meet-over-all-paths solution](/meet-over-all-paths-solution/) exactly, but only if it starts from the right values.

## In plain words

Suppose the program computes `x * 2` and later computes `x * 2` again. If `x` did not change between the two, the second computation can reuse the first result. But this is only safe if the first computation happened on every way to the second one.

The compiler walks forward through the program. Each block adds the expressions it computes and removes the expressions whose inputs it changes. Where paths join, an expression survives only if it survives on all of them. At the start of the program nothing has been computed yet. Inside loops the compiler starts with the hopeful guess "everything is available" and removes expressions until the guesses agree.

The answer can miss a reuse that is really safe, but it never claims an unsafe one.

## Definition

**Input.** A [control flow graph](/control-flow-graph/) with $n$ blocks, $m$ edges and one entry block, in [three-address code](/three-address-code/). Let $E$ be the set of expressions `a op b` that occur in the program, compared by their text, and $|E|$ its size.

**Output.** For every block $B$, the set $\mathrm{IN}[B] \subseteq E$ of expressions available at its start, and $\mathrm{OUT}[B]$ at its end.

**The framework.**

| property | value |
|---|---|
| direction | forward |
| may or must | must: available only if available along every path |
| domain $L$ | the subsets of $E$ |
| order $\sqsubseteq$ | $\subseteq$ (a smaller set is a weaker claim) |
| meet $\sqcap$ | $\cap$ |
| $\top$ and $\bot$ | $\top = E$, $\bot = \emptyset$ |
| boundary value $\iota$ | $\emptyset$ at the start of the entry block: nothing has been computed yet |
| start value elsewhere | $E$ ($\top$) |
| transfer functions | $f_B(X) = e\_gen_B \cup (X - e\_kill_B)$, monotone and distributive |
| height $h$ | $\lvert E \rvert$ |

The boundary value $\emptyset$ is $\bot$ here, not $\top$, and the start value elsewhere is $\top = E$, not $\emptyset$. Both choices matter, as the examples show. In the meet convention of the dataflow pages, the answer is the greatest fixed point, which for $\subseteq$ means the largest sets that satisfy the equations.

**Lattice and height.** $L$ is the set of subsets of $E$ ordered by $\subseteq$. A strict chain removes one expression per step, so $h = |E|$.

**Transfer functions.** An instruction `x = a op b` evaluates `a op b` and then writes `x`. Let $kill_x$ be the set of expressions in $E$ that have `x` as an operand. The instruction has $kill = kill_x$ and $gen = \{a \text{ op } b\} - kill_x$; so `s = s + a` generates nothing, because it changes `s` right after it computes `s + a`. A constant or copy into `x` has $gen = \emptyset$ and $kill = kill_x$. Composing the instructions of $B$ in order gives $e\_gen_B$, the expressions that $B$ computes and does not kill afterward, and $e\_kill_B$, the expressions with an operand that $B$ writes.

**Equations.**

$$\mathrm{IN}[\mathrm{entry}] = \emptyset \cap \bigcap_{P \in \mathrm{pred}(\mathrm{entry})} \mathrm{OUT}[P] = \emptyset, \qquad \mathrm{IN}[B] = \bigcap_{P \in \mathrm{pred}(B)} \mathrm{OUT}[P], \qquad \mathrm{OUT}[B] = e\_gen_B \cup (\mathrm{IN}[B] - e\_kill_B).$$

**Meet over all paths.** For a path $\pi$ from the entry to the start of $B$, $f_\pi(\emptyset)$ is the set of expressions that $\pi$ evaluates with no later write to an operand. MOP is the intersection over all such paths: the expressions available along every CFG path.

**The fixed point computed.** The [worklist dataflow algorithm](/worklist-dataflow-algorithm/) sets the entry to $\emptyset$ and every other block to $E$, then shrinks the sets. It stops at the [maximal fixed-point solution](/maximal-fixed-point-solution/), the largest sets that satisfy the equations, and since the functions are distributive, this equals MOP when every block is reachable from the entry.

Starting the other blocks at $\emptyset$ instead also ends at a solution of the equations, but at a smaller one. In this loop `x * 2` is available at `head` and in `done`, so `c = x * 2` can reuse `a`:

```
entry:
  i = 0
  a = x * 2
  jump head
head:
  t = i < n
  br t body done
body:
  i = i + 1
  jump head
done:
  c = x * 2
  ret c
```

With the start value $E$ at `body`, $\mathrm{IN}[\mathrm{head}] = \{x * 2\} \cap \mathrm{OUT}[\mathrm{body}]$ keeps `x * 2`, since nothing in the loop writes `x`. With the start value $\emptyset$, the back edge from `body` brings $\emptyset$ to `head`, the intersection is empty, and nothing ever puts `x * 2` back. Both are solutions; only the first is the greatest one.

**Soundness.** If an expression is in $\mathrm{IN}[B]$, then every CFG path from the entry to $B$ evaluates it after the last write to its operands. Every run follows a CFG path, so at the start of $B$ the value is already computed on that run.

**Precision.** CFG paths that no run takes make the sets smaller than the truth. Here every run that reaches `r` went through `p`, since both branches test the same `c`, so `x * 2` is always already computed at `r`. The CFG path through `q` and then `r` does not compute it, so the analysis does not list it, and the redundant computation stays.

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
  b = x * 2
  ret b
s:
  ret c
```

**Cost.** With bit vectors of $|E|$ bits, one set operation costs $O(|E| / w)$ word operations. The worklist algorithm applies at most $n(|E| + 1)$ transfer functions and $m(|E| + 1)$ intersections, which is $O((n + m) |E|^2 / w)$ time in the worst case. Round-robin iteration in reverse postorder needs at most $d + 2$ passes for loop-connectedness depth $d$ ([Kam-Ullman iteration bound](/kam-ullman-iteration-bound/)), so $O((d + 2)(n + m) |E| / w)$.

## Variants

- **Commutative forms.** Treat `a + b` and `b + a` as the same expression by putting the operands in a fixed order first. This finds more redundancy at no extra cost.
- **Available copies.** The same must analysis over copies `x = y`, killed by a write to `x` or `y`, tells [copy propagation](/copy-propagation/) where a read of `x` can read `y`.
- **Available loads and checks.** Memory loads and array bound checks can be tracked the same way, with a write to memory or to the index as the kill. Aliasing makes the kill sets larger.
- **Value-based availability.** Textual equality misses `b = a; c = b * 2` after `d = a * 2`. [Global value numbering](/global-value-numbering/) works with values instead of text and finds such cases.

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

| block | $e\_gen$ | $e\_kill$ | IN | OUT |
|---|---|---|---|---|
| entry | none | `i < n`, `i & 1`, `i + 1`, `s + a` | none | none |
| head | `i < n` | none | none | `i < n` |
| body | `x * 2`, `i & 1` | `s + a` | `i < n` | `i < n`, `x * 2`, `i & 1` |
| odd | none | `s + a` | `i < n`, `x * 2`, `i & 1` | `i < n`, `x * 2`, `i & 1` |
| next | none | `i < n`, `i & 1`, `i + 1` | `i < n`, `x * 2`, `i & 1` | `x * 2` |
| done | none | none | `i < n` | `i < n` |

- `body` kills `s + a` because it writes `a`. `odd` computes `s + a` and then writes `s`, so `s + a` is never available.
- `x * 2` is available at the end of `next`, but not at `head`: the path from `entry` to `head` has not computed it. The intersection at `head` removes it.
- If `next` had a second instruction `b = x * 2`, it would be redundant, because `x * 2` is in $\mathrm{IN}[\mathrm{next}]$. CSE would replace it with `b = a`.

**The worklist trace.** In reverse postorder (entry, head, done, body, odd, next) the first pass is the last one. `entry` sends $\emptyset$ to `head`, which drops from $E$ to $\emptyset$; then each block shrinks its successors once, and `next` sends $\{x * 2\}$ to `head`, where the intersection with $\emptyset$ changes nothing. The algorithm applies 6 transfer functions and 7 intersections, and each IN set changes at most once.

**Non-example: the wrong boundary.** Starting the entry at $\top = E$ instead of $\emptyset$ claims that every expression is available before the program has computed anything. In the running example it would put `x * 2` into $\mathrm{IN}[\mathrm{head}]$, and CSE could then reuse a value that was never computed.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| [Worklist dataflow algorithm](/worklist-dataflow-algorithm/) | $O((n + m) \lvert E \rvert^2 / w)$ worst case | start at $E$ except at the entry |
| Round-robin in reverse postorder | $O((d + 2)(n + m) \lvert E \rvert / w)$ | [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/) |
| One graph search per expression on the complement | $O(\lvert E \rvert (n + m))$ | see Reductions |
| [Global value numbering](/global-value-numbering/) | depends on the method | finds equal values, not only equal text |

## Bounds

The output can have $\Theta(n \lvert E \rvert)$ entries: if the entry block computes $n$ expressions over parameters that nothing writes, all of them are available in all $n$ blocks. So listing the sets needs $\Omega(n \lvert E \rvert)$ time in the worst case.

## Reductions

- **To a may problem by complement.** Let $N[B] = E - \mathrm{IN}[B]$, the expressions that are *not* available. By De Morgan's law, $N$ satisfies a may problem with union: its transfer function is $X \mapsto (e\_kill_B - e\_gen_B) \cup (X - e\_gen_B)$, its boundary is $E$ at the entry, and its start value is $\emptyset$. The greatest solution of the original is the complement of the least sets for $N$.
- **To graph reachability.** Through the complement, $e \notin \mathrm{IN}[B]$ if and only if some path reaches $B$ either from the start of the entry or from a block that kills $e$ without generating it again, and passes through no block that generates $e$. One search per expression finds these blocks; see [graph reachability](/graph-reachability/).
- **Used by partial redundancy elimination.** [Lazy code motion](/lazy-code-motion/) combines available expressions with [very busy expressions](/very-busy-expressions/) and two more bit-vector problems to decide where to insert and delete computations.

## Applications

- **Global common subexpression elimination.** If `a op b` is available at an instruction `y = a op b`, keep the earlier result in a temporary and replace the instruction with a copy. See [common subexpression elimination](/common-subexpression-elimination/).
- **Partial redundancy elimination.** [Partial redundancy elimination](/partial-redundancy-elimination/) also removes computations that are available on some paths only, by inserting the computation on the other paths.
- **Copy propagation and redundant loads.** The available copies and available loads variants find where a copy or a load can be reused.
- **Bounds-check removal.** A check that is available at a second check of the same index and length makes the second check redundant.

## References
