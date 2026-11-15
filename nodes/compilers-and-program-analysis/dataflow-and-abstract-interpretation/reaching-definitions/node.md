---
tag: 7FJJMB
kind: problem
slug: reaching-definitions
name: Reaching definitions
aliases:
- reaching definitions analysis
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: intro
summary: For each program point, find the definitions of variables that can reach it along some path without being overwritten.
prereqs: [dataflow-analysis]
see_also: [def-use-chains, gen-kill-problem, worklist-dataflow-algorithm, live-variable-analysis, available-expressions, static-single-assignment-form, loop-invariant-code-motion, copy-propagation]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.2.4 (Reaching Definitions, with the gen and kill sets, the equations and the iterative algorithm) and Section 9.6.7 (Speed of Convergence of Iterative Data-Flow Algorithms)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Section 2.1.2 (Reaching Definitions Analysis, stated with a join and with pseudo definitions for the start)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 9 (Data-Flow Analysis), Section 9.2.4 (Other Data-Flow Problems)
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the whole paper (the iterative algorithm on a meet semilattice that solves this and the other bit-vector problems)
---

Reaching definitions is the forward may problem of [dataflow analysis](/dataflow-analysis/). A *definition* is an instruction that writes a variable, and a definition $d$ of $x$ *reaches* a program point $p$ if some path in the [control flow graph](/control-flow-graph/) goes from just after $d$ to $p$ with no other definition of $x$ on it. The problem asks, for every [basic block](/basic-block/), for the set of definitions that reach its start. The answer links each read of a variable to the writes that may have produced its value; these links are the use-def half of [def-use chains](/def-use-chains/). Reaching definitions is a [gen-kill problem](/gen-kill-problem/): it is distributive, so the [worklist dataflow algorithm](/worklist-dataflow-algorithm/) computes the [meet-over-all-paths solution](/meet-over-all-paths-solution/) exactly.

## In plain words

Every line that stores a value into a variable is a definition. Pick a line that reads a variable. Which of the stores could have put the value there? Follow the program backward from the read: a store counts if you can get from it to the read without passing another store into the same variable.

The compiler answers this for every block at once. It walks forward through the program. Each block adds its own stores and removes the older stores that they hide. Where paths join, a store survives if it survives on at least one of them. A loop carries stores from the bottom of the loop back to its top, so the walk repeats until nothing new arrives.

The answer may include a store that no real run delivers, but it never misses one that a run does deliver.

## Definition

**Input.** A [control flow graph](/control-flow-graph/) with $n$ blocks, $m$ edges and one entry block, whose instructions are in [three-address code](/three-address-code/). Let $D$ be the set of definitions, the instructions that write a variable, and let $|D|$ be its size.

**Output.** For every block $B$, the set $\mathrm{IN}[B] \subseteq D$ of definitions that reach the start of $B$, and the set $\mathrm{OUT}[B]$ that reach its end.

**The framework.**

| property | value |
|---|---|
| direction | forward |
| may or must | may: a definition reaches if it reaches along some path |
| domain $L$ | the subsets of $D$ |
| order $\sqsubseteq$ | $\supseteq$ (a larger set is a weaker claim) |
| meet $\sqcap$ | $\cup$ |
| $\top$ and $\bot$ | $\top = \emptyset$, $\bot = D$ |
| boundary value $\iota$ | $\mathrm{OUT}[\mathrm{entry}] = \emptyset$: no definition of the procedure has run yet |
| start value elsewhere | $\emptyset$ ($\top$) |
| transfer functions | $f_B(X) = gen_B \cup (X - kill_B)$, monotone and distributive |
| height $h$ | $\lvert D \rvert$ |

This page and the other dataflow pages use the meet convention: $\top$ is the start value and the answer is the greatest fixed point. In a may problem the order is $\supseteq$, so "greatest" means the smallest sets. Here $\iota$ happens to equal $\top$; the variant with pseudo definitions below has $\iota \ne \top$.

**Lattice and height.** $L$ is the set of all subsets of $D$, and a strict chain $\emptyset \sqsupset \{d_1\} \sqsupset \{d_1, d_2\} \sqsupset \cdots \sqsupset D$ adds one definition per step. So $h = |D|$.

**Transfer functions.** For one instruction $d$ that defines $x$, $gen = \{d\}$ and $kill$ is the set of the other definitions of $x$. A block is the composition of its instructions in order; for two steps the composition is $gen = gen_2 \cup (gen_1 - kill_2)$ and $kill = kill_1 \cup kill_2$. So $gen_B$ is the set of the last definition of each variable that $B$ writes, and $kill_B$ is the set of all other definitions of the variables that $B$ writes. A block that writes $x$ twice keeps only the second write in $gen_B$.

**Equations.**

$$\mathrm{OUT}[\mathrm{entry}] = gen_{\mathrm{entry}}, \qquad \mathrm{IN}[B] = \bigcup_{P \in \mathrm{pred}(B)} \mathrm{OUT}[P], \qquad \mathrm{OUT}[B] = gen_B \cup (\mathrm{IN}[B] - kill_B).$$

The entry block has $\mathrm{IN}[\mathrm{entry}] = \iota = \emptyset$, together with the outputs of any predecessors that it has.

**Meet over all paths.** For a path $\pi = (\mathrm{entry}, B_1, \ldots, B_k)$ that ends just before $B_k$, $f_\pi(\emptyset)$ is the set of definitions that are the last write of their variable along $\pi$. The meet over all such paths is the union, which is the set of definitions that reach the start of $B_k$ along some path. This is the exact meaning of "reaches" on the CFG.

**The fixed point computed.** The [worklist dataflow algorithm](/worklist-dataflow-algorithm/) starts every set at $\emptyset$, puts $\iota$ at the entry, and grows the sets until the equations hold. The result is the [maximal fixed-point solution](/maximal-fixed-point-solution/): the smallest sets that satisfy the equations.

**Soundness.** If a run reaches the start of $B$ and the last write of $x$ on that run was $d$, then $d \in \mathrm{IN}[B]$. The run follows a CFG path, and on that path $d$ is the last write of $x$, so $d \in f_\pi(\emptyset) \subseteq \mathrm{MOP}[B]$. Since $gen$ and $kill$ functions are distributive, MFP = MOP when every block is reachable from the entry.

**Precision.** The answer is exact for CFG paths but not for runs, since some CFG paths are never taken. Two branches on the same unchanged condition `c` give an example:

```
entry:
  br c left right
left:
  x = 1
  jump mid
right:
  x = 2
  jump mid
mid:
  br c use other
use:
  y = x
  ret y
other:
  ret c
```

Both definitions of `x` reach `use`, because the CFG has the path through `right` and then `use`. No run takes that path: if `c` is false at the first branch, it is false at the second one too. So the analysis cannot tell that `y` is always 1.

**Cost.** With bit vectors of $|D|$ bits, one union or difference costs $O(|D| / w)$ word operations, where $w$ is the word size. The worklist algorithm applies at most $n(|D| + 1)$ transfer functions and does at most $m(|D| + 1)$ unions, so it runs in $O((n + m) |D|^2 / w)$ time. Processed in reverse postorder, round-robin iteration needs at most $d + 2$ passes, where $d$ is the loop-connectedness depth (the [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/)), for a total of $O((d + 2)(n + m) |D| / w)$. Real programs have small $d$.

## Variants

- **Pseudo definitions at the entry.** Add one pseudo definition $\delta_x$ for each variable $x$ and set $\iota = \{\delta_x\}$. Then $\delta_x$ reaches a read of $x$ exactly when some path reads $x$ before writing it. A parameter is fine; any other variable is a possible use before initialization. Here the boundary is not $\top = \emptyset$, and starting the entry at $\top$ would hide every such warning. Nielson, Nielson and Hankin use this form.
- **Instruction level.** The same equations with one node per instruction give the answer at every instruction. The usual practice is to solve at block level and then scan each block once.
- **Ambiguous definitions.** A store through a pointer or a call may write $x$. Such a write generates a definition of $x$ but does not kill the others, because it might not write $x$.
- **Per variable.** For a use of $x$, only the definitions of $x$ matter. Splitting $D$ by variable gives smaller vectors and the same answer.
- **Interprocedural.** Across calls, the definitions in the callee and the definitions that reach the call are matched by the [interprocedural dataflow analysis](/interprocedural-dataflow-analysis/) and [IFDS framework](/ifds-framework/) methods.

## Examples

The running example of [dataflow analysis](/dataflow-analysis/) has seven definitions:

| name | block | instruction |
|---|---|---|
| $d_1$ | entry | `i = 0` |
| $d_2$ | entry | `s = 0` |
| $d_3$ | head | `t = i < n` |
| $d_4$ | body | `a = x * 2` |
| $d_5$ | body | `u = i & 1` |
| $d_6$ | odd | `s = s + a` |
| $d_7$ | next | `i = i + 1` |

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

Gen and kill sets, and the solution:

| block | $gen$ | $kill$ | IN | OUT |
|---|---|---|---|---|
| entry | $d_1, d_2$ | $d_6, d_7$ | none | $d_1, d_2$ |
| head | $d_3$ | none | all seven | all seven |
| body | $d_4, d_5$ | none | all seven | all seven |
| odd | $d_6$ | $d_2$ | all seven | all but $d_2$ |
| next | $d_7$ | $d_1$ | all seven | all but $d_1$ |
| done | none | none | all seven | all seven |

What the answer says:

- In `head`, the read of `i` sees $d_1$ and $d_7$. Two definitions with different values reach it, so `i` is not a constant there.
- In `odd`, the read of `s` sees $d_2$ (first odd value) and $d_6$ (an earlier odd value). The read of `a` sees only $d_4$.
- In `body`, `a = x * 2` reads only the parameter `x`, which no definition in the procedure writes. So `x * 2` is invariant in the loop and [loop-invariant code motion](/loop-invariant-code-motion/) can hoist it.

The worklist in reverse postorder (entry, head, done, body, odd, next) processes 11 blocks: six in the first pass, then `head`, `body`, `done`, `odd` and `next` again after $d_7$ comes back along the edge from `next` to `head`. It does 13 unions and changes an IN set 11 times. The largest number of changes of one IN set is 3, at `next`, well below $h = 7$.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| [Worklist dataflow algorithm](/worklist-dataflow-algorithm/) | $O((n + m) \lvert D \rvert^2 / w)$ worst case | Kildall 1973; the usual choice |
| Round-robin in reverse postorder | $O((d + 2)(n + m) \lvert D \rvert / w)$ | the [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/) for rapid frameworks |
| One graph search per definition | $O(\lvert D \rvert (n + m))$ | see the reduction below |
| [Elimination methods](/elimination-dataflow-methods/) | see that page | solve by graph reduction instead of iteration; best on reducible graphs |
| [SSA form](/static-single-assignment-form/) | after SSA construction, each use has exactly one definition | phi-functions merge the definitions that reach a join |

## Bounds

The output alone can have $\Theta(n \lvert D \rvert)$ entries. In a chain of $n$ blocks where block $i$ writes its own variable $x_i$, every definition reaches every later block, so the answer has $n(n - 1) / 2$ pairs. Any algorithm that lists the sets therefore needs $\Omega(n \lvert D \rvert)$ time in the worst case. A search per definition matches this up to the factor $(n + m) / n$. The bit-vector algorithms win in practice because one word operation handles $w$ definitions.

## Reductions

- **To graph reachability.** Fix a definition $d$ in block $B_d$ with $d \in gen_{B_d}$. Then $d \in \mathrm{IN}[B]$ if and only if the CFG has a path $B_d, B_1, \ldots, B_k = B$ with $k \ge 1$ in which no inner block $B_1, \ldots, B_{k-1}$ kills $d$. A [depth-first search](/depth-first-search/) from the successors of $B_d$ that enters a killing block but does not leave it finds these blocks. One search per definition solves the problem, so every bit of a gen-kill problem is a [graph reachability](/graph-reachability/) question.
- **To Datalog.** The two rules `reach(D, B) :- gen(P, D), edge(P, B).` and `reach(D, B) :- reach(D, P), not kill(P, D), edge(P, B).` compute $\mathrm{IN}$; see [Datalog-based program analysis](/datalog-program-analysis/).
- **From uninitialized variables.** Possible uses before initialization reduce to reaching definitions with pseudo definitions at the entry, as in Variants.

## Applications

- **Def-use and use-def chains.** For each read of $x$ in block $B$, the definitions of $x$ in $\mathrm{IN}[B]$ (or the last write before the read in $B$) are its use-def chain. Inverting the links gives [def-use chains](/def-use-chains/).
- **Constant and copy propagation.** If the only definition that reaches a read of `x` is `x = 4`, the read can use 4. If it is the copy `x = y` and `y` is not written between, [copy propagation](/copy-propagation/) can read `y`.
- **Loop-invariant code motion.** An operand is invariant in a loop when all its reaching definitions are outside the loop, or it is a constant.
- **Warnings.** With pseudo definitions, a read that a pseudo definition reaches is a possible use of an uninitialized variable.
- **Slicing and debugging.** [Program slicing](/program-slicing/) follows use-def chains backward to find the instructions that can affect a value.

## References
