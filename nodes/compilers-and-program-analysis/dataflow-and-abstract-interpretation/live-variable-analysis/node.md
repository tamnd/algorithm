---
tag: GTY2TM
kind: problem
slug: live-variable-analysis
name: Live variable analysis
aliases:
- liveness analysis
- live variables
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: intro
summary: For each program point, find the variables whose current value may be read on some path before being overwritten.
prereqs: [dataflow-analysis]
see_also: [interference-graph, register-allocation-problem, dead-code-elimination, pruned-ssa-form, gen-kill-problem, worklist-dataflow-algorithm, reaching-definitions, very-busy-expressions]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.2.5 (Live-Variable Analysis, with the use and def sets, the backward equations and the iterative algorithm)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 9 (Data-Flow Analysis), Section 9.2.2 (Live-Variable Analysis)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Section 2.1.4 (Live Variables Analysis, stated with a join)
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the whole paper (the iterative algorithm on a meet semilattice, which solves this problem on the reverse graph)
---

Live variable analysis is the backward may problem of [dataflow analysis](/dataflow-analysis/). A variable $x$ is *live* at a program point $p$ if some path in the [control flow graph](/control-flow-graph/) from $p$ reads $x$ before it writes $x$; otherwise $x$ is *dead* at $p$, and its current value will never be used. The problem asks, for every [basic block](/basic-block/), for the set of variables live at its start and at its end. The answer tells the register allocator which values must be kept, and it tells [dead code elimination](/dead-code-elimination/) which writes are useless. Liveness is a [gen-kill problem](/gen-kill-problem/) on the reverse CFG, so the [worklist dataflow algorithm](/worklist-dataflow-algorithm/) computes its [meet-over-all-paths solution](/meet-over-all-paths-solution/) exactly.

## In plain words

A variable is live at a point if the value it holds there might still be read later. If every way forward overwrites the variable first, or never reads it again, the value is dead and its storage can be reused.

To find this, the compiler reads the program backward, from the returns toward the start. A read makes a variable live above it. A write makes it dead above it, since the old value is replaced. At a branch, a variable is live if it is live on at least one of the ways out. Loops carry needs from the top of the loop back to its bottom, so the backward walk repeats until nothing changes.

The answer can call a variable live when no real run reads it, but never the reverse.

## Definition

**Input.** A [control flow graph](/control-flow-graph/) with $n$ blocks and $m$ edges, in [three-address code](/three-address-code/), and the set $V$ of its variables, with $|V| = v$.

**Output.** For every block $B$, the set $\mathrm{IN}[B] \subseteq V$ of variables live at the start of $B$ and the set $\mathrm{OUT}[B]$ live at its end.

**The framework.**

| property | value |
|---|---|
| direction | backward: the analysis runs on the reverse CFG |
| may or must | may: live if some path reads the value |
| domain $L$ | the subsets of $V$ |
| order $\sqsubseteq$ | $\supseteq$ |
| meet $\sqcap$ | $\cup$ |
| $\top$ and $\bot$ | $\top = \emptyset$, $\bot = V$ |
| boundary value $\iota$ | $\emptyset$ at the end of each block that ends in `ret`: local variables die when the procedure returns |
| start value elsewhere | $\emptyset$ ($\top$) |
| transfer functions | $f_B(X) = use_B \cup (X - def_B)$, monotone and distributive |
| height $h$ | $v$ |

The pages on dataflow use the meet convention: $\top$ is the start value and the answer is the greatest fixed point, which for a may problem with the order $\supseteq$ means the smallest sets that satisfy the equations.

**Lattice and height.** $L$ is the set of subsets of $V$. A strict chain adds one variable per step, so $h = v$.

**Transfer functions.** Read the block from its end to its start. An instruction `x = y op z` has $gen = \{y, z\}$ (the variables among its operands) and $kill = \{x\}$, and it is applied as $X \mapsto gen \cup (X - kill)$, so `x = x + 1` leaves `x` live. A terminator that reads a variable, such as `br t L1 L2` or `ret s`, has $gen = \{t\}$ or $\{s\}$ and an empty kill set. Composing the steps from the last one to the first gives $use_B$, the variables that $B$ reads before it writes them (upward exposed), and $def_B$, the variables that $B$ writes.

**Equations.** With the empty union equal to $\emptyset$:

$$\mathrm{OUT}[B] = \Big(\iota \text{ if } B \text{ ends in } \texttt{ret}\Big) \cup \bigcup_{S \in \mathrm{succ}(B)} \mathrm{IN}[S], \qquad \mathrm{IN}[B] = use_B \cup (\mathrm{OUT}[B] - def_B).$$

These are the forward equations of [dataflow analysis](/dataflow-analysis/) on the reverse CFG: the edges are turned around, the `ret` blocks are the start nodes, and the roles of IN and OUT swap.

**Meet over all paths.** For a path $\pi$ from the end of $B$ to the end of a `ret` block, $f_\pi(\emptyset)$ is the set of variables that $\pi$ reads before it writes them. The union over all such paths is the set of variables live at the end of $B$ along some CFG path.

**The fixed point computed.** The [worklist dataflow algorithm](/worklist-dataflow-algorithm/) on the reverse CFG starts all sets at $\emptyset$ and grows them. It stops at the [maximal fixed-point solution](/maximal-fixed-point-solution/), the smallest sets that satisfy the equations. Since the transfer functions are distributive, it equals MOP when every block can reach a `ret` block.

**Soundness.** If a run is at the end of $B$ and later reads the value that $x$ holds there, the part of the run between the two points follows a CFG path $B, B_1, \ldots, B_k$ in which $B_k$ reads $x$ before writing it and $B_1, \ldots, B_{k-1}$ do not write $x$. Then $x \in use_{B_k} \subseteq \mathrm{IN}[B_k]$, and going back along the path, each equation puts $x$ into the next OUT and IN sets. So $x \in \mathrm{OUT}[B]$ in every solution of the equations, including runs that never return.

**Precision.** CFG paths that no run takes make the answer larger than the truth. In this program `y` is live at the start of `entry`, because the path through `skip` and then `use` reads `y` without a write. No run takes that path, since both branches test the same `c`. A check for uninitialized variables would warn about `y` here although no run reads it before writing it.

```
entry:
  br c set skip
set:
  y = 1
  jump mid
skip:
  jump mid
mid:
  br c use other
use:
  ret y
other:
  ret c
```

**Cost.** With bit vectors of $v$ bits, one set operation costs $O(v / w)$ word operations. The worklist algorithm applies at most $n(v + 1)$ transfer functions and $m(v + 1)$ unions, so it takes $O((n + m) v^2 / w)$ time in the worst case. Round-robin iteration in reverse postorder of the reverse CFG takes at most $d + 2$ passes, where $d$ is the loop-connectedness depth of the reverse CFG ([Kam-Ullman iteration bound](/kam-ullman-iteration-bound/)), so $O((d + 2)(n + m) v / w)$ time.

## Variants

- **Instruction-level liveness.** After the block sets are known, one backward scan of each block gives the live set at every instruction. This is what register allocators use.
- **A different boundary.** If the procedure writes global variables or memory that the caller reads, those are live after every `ret`, and $\iota$ is that set. It is not $\top = \emptyset$, and leaving it out would let dead code elimination delete stores that the caller needs.
- **Strongly live variables.** Count a read only if the instruction that reads is itself useful. Then `x = y + 1` makes `y` live only if `x` is live after it: $f(X) = (X - \{x\}) \cup (\{y\} \text{ if } x \in X)$. This function distributes over $\cup$ but is not of gen-kill form, and it finds dead chains of assignments that ordinary liveness keeps.
- **Liveness on SSA form.** In [static single assignment form](/static-single-assignment-form/) each variable has one definition, and the live range of a variable can be found by walking backward from each use to that definition, one variable at a time. A read in a phi-function counts at the end of the matching predecessor, not at the start of the block.
- **Live ranges and intervals.** [Linear scan register allocation](/linear-scan-register-allocation/) turns the live sets into one interval per variable over a linear order of the instructions.

## Examples

The running example of [dataflow analysis](/dataflow-analysis/), with the parameters `n` and `x`:

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

| block | $use_B$ | $def_B$ | IN (live at the start) | OUT (live at the end) |
|---|---|---|---|---|
| entry | none | i, s | n, x | i, n, s, x |
| head | i, n | t | i, n, s, x | i, n, s, x |
| body | i, x | a, u | i, n, s, x | a, i, n, s, x |
| odd | a, s | s | a, i, n, s, x | i, n, s, x |
| next | i | i | i, n, s, x | i, n, s, x |
| done | s | none | s | none |

`t` is in $def$ but not in $use$ of `head`, because `head` writes `t` before the branch reads it. `odd` has `s` in both sets: it reads the old `s` before it writes the new one.

**The worklist trace.** The reverse CFG has `done` as its only start node, and its reverse postorder is `done`, `head`, `next`, `odd`, `body`, `entry`. The table gives each step: the block processed, the set it sends to its predecessors (its IN), and the predecessors whose OUT changed.

| step | block | sends | changed |
|---|---|---|---|
| 1 | done | s | head |
| 2 | head | i, n, s | entry, next |
| 3 | next | i, n, s | body, odd |
| 4 | odd | a, i, n, s | body |
| 5 | body | i, n, s, x | head |
| 6 | entry | n | none |
| 7 | head | i, n, s, x | entry, next |
| 8 | entry | n, x | none |
| 9 | next | i, n, s, x | body, odd |
| 10 | body | i, n, s, x | none |
| 11 | odd | a, i, n, s, x | none |

The first pass misses `x` in most blocks: `x` is read only in `body`, and that read reaches `head`, `next` and `odd` only by going around the loop. The algorithm processes 11 blocks, does 13 unions and changes an OUT set 11 times. No set changes more than 3 times, against the bound $h = 7$.

**What the answer is used for.** Just before `br u odd next`, the live variables are `a`, `i`, `n`, `s`, `x` and `u`, six at once, so the loop needs six registers unless one value is spilled. `a` is dead in `next` and `head`, so its register can hold another value there. If `body` had a further write `w = i * i` and nothing read `w`, then `w` would not be live after the write, and dead code elimination would delete it.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| [Worklist dataflow algorithm](/worklist-dataflow-algorithm/) on the reverse CFG | $O((n + m) v^2 / w)$ worst case | the usual choice |
| Round-robin in reverse postorder of the reverse CFG | $O((d + 2)(n + m) v / w)$ | the [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/) |
| One backward search per variable | $O(v (n + m))$ | see the reduction below |
| Backward walk from each use on SSA form | proportional to the total size of the live ranges | no bit vectors |

## Bounds

The output can have $\Theta(n v)$ entries: in a chain of $n$ blocks where block $i$ writes $x_i$ and the last block reads all of them, $x_i$ is live in every block after block $i$, which is $n(n - 1) / 2$ pairs with $v = n$. So listing the live sets needs $\Omega(n v)$ time in the worst case, and the search per variable is within a factor $(n + m) / n$ of it.

## Reductions

- **To graph reachability.** Variable $x$ is live at the start of $B$ if and only if the CFG has a path $B = B_0, B_1, \ldots, B_k$ with $x \in use_{B_k}$ and $x \notin def_{B_i}$ for $i < k$. One backward [depth-first search](/depth-first-search/) from the blocks with $x \in use$ finds all of them: it marks $x$ live at the end of each predecessor it visits, and it continues past that predecessor only if the predecessor does not write $x$. This is [graph reachability](/graph-reachability/) on the [transpose graph](/transpose-graph/) of the CFG.
- **To Datalog.** `live(X, B) :- use(B, X).` and `live(X, B) :- edge(B, S), live(X, S), not def(B, X).` give $\mathrm{IN}$; see [Datalog-based program analysis](/datalog-program-analysis/).
- **From uninitialized variables.** A variable that is live at the start of the entry block and is not a parameter may be read before it is written on some path.

## Applications

- **Register allocation.** Two variables interfere when one is live where the other is written; the [interference graph](/interference-graph/) of [register allocation](/register-allocation-problem/) is built from the live sets at each instruction.
- **Dead code elimination.** A write to a variable that is dead after it, with no other effect, can be removed. See [dead code elimination](/dead-code-elimination/).
- **SSA construction.** [Pruned SSA form](/pruned-ssa-form/) places a phi-function for $x$ at a join only if $x$ is live there.
- **Uninitialized variables.** A non-parameter variable that is live at the entry is a possible use before initialization.
- **Garbage collection.** A compiler records, at each point where a collection can happen, which stack slots and registers hold live references, so the collector does not keep dead objects alive.

## References
