---
tag: 5GWXK6
kind: algorithm
slug: trace-scheduling
name: Trace scheduling
aliases:
- Fisher trace scheduling
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Schedules a likely path through several blocks as one block and adds compensation code where other paths enter or leave it.
solves: [instruction-scheduling-problem]
model: word-ram
complexity:
  vars: {n: the number of items of one trace, s: the number of instructions and terminators of the largest program during the run, N: the number of names, m: the number of traces}
  time: {worst: O(m (s N + n^2))}
  space: {extra: O(s N + n^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1981
  people: [Joseph A. Fisher]
  note: Fisher gave the method for the compaction of horizontal microcode, with a bookkeeping phase for the copies. Ellis used it in the Bulldog compiler for VLIW machines, and Multiflow built a commercial VLIW machine and compiler around it.
prereqs: [instruction-scheduling-problem, list-scheduling, control-flow-graph, live-variable-analysis, profile-guided-optimization]
see_also: [superblock-scheduling, software-pipelining, iterative-modulo-scheduling, ball-larus-path-profiling, tracing-jit-compilation, speculative-code-motion, path-based-scheduling, loop-unrolling]
sources:
  - paper: doi:10.1109/TC.1981.1675827
    title: Joseph A. Fisher, Trace scheduling, a technique for global microcode compaction, IEEE Transactions on Computers C-30(7), 1981, 478-490
    locator: the selection of traces by expected execution counts, the compaction of a trace as if it were one block, and the bookkeeping phase that copies operations onto the edges that leave or join the trace
  - paper: doi:10.1109/micro.1988.639244
    title: Pohua P. Chang and Wen-mei W. Hwu, Trace selection for compiling large C application programs to microcode, Proceedings of the 21st Annual Workshop on Microprogramming and Microarchitecture, 1988, 21-29
    locator: Section 3 on trace selection, local compaction and bookkeeping with patch code at the splits and rejoins of a trace, and Section 4 on selection by node weights and arc weights from a seed with the best successor and the best predecessor
  - paper: doi:10.1007/BF01205182
    title: P. Geoffrey Lowney, Stefan M. Freudenberger, Thomas J. Karzes, W. D. Lichtenstein, Robert P. Nix, John S. O'Donnell and John C. Ruttenberg, The Multiflow trace scheduling compiler, The Journal of Supercomputing 7(1-2), 1993, 51-142
    locator: the production trace scheduling compiler of the Multiflow TRACE machines, with its trace picker, its scheduler and its compensation code
  - paper: doi:10.1145/183432.183446
    title: Stefan M. Freudenberger, Thomas R. Gross and P. Geoffrey Lowney, Avoidance and suppression of compensation code in a trace scheduling compiler, ACM Transactions on Programming Languages and Systems 16(4), 1994, 1156-1214
    locator: the amount of compensation code in practice, and the methods that avoid code motions that need copies or remove copies that are not needed
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Section 17.5 (Trace Scheduling), 569 to 571
---

Trace scheduling is a global [instruction scheduling](/instruction-scheduling-problem/) method. It picks a *trace*, a path through several basic blocks that a profile says is likely, and schedules the whole trace as if it were one block. So an instruction can move above a branch or below the point where another path joins, which a block-by-block scheduler cannot do. The other paths must still compute the same values. When an instruction moves below a *side exit* (a branch that leaves the trace), a copy goes on the edge that leaves. When an instruction moves above a *side entrance* (a point where another path joins the trace), a copy goes on the edge that joins. These copies are the *compensation code*. Fisher (1981) introduced the method to compact horizontal microcode. It became the main scheduler of the first commercial VLIW compilers.

## In plain words

A program often takes the same way through its branches. Trace scheduling finds that usual way, treats it as one long straight line of code, and packs the instructions of that line tightly, so that a wide machine can run several of them in each cycle. Packing moves some instructions past the branches. Then a run that leaves the usual way at a branch could miss an instruction that it needs, and a run that comes in from the side could miss one that moved up past its entry point. So the method puts a copy of each such instruction on the side path. The usual way gets faster, and the rare ways get a little slower and a little longer. The method then packs the next most usual way, until all code is done.

## The problem

The input is a program in the toy IR of these pages: a [control flow graph](/control-flow-graph/) with no cycle whose blocks hold `const`, `copy` and `op` instructions and end with `jump`, `br` or `ret`, and an edge profile, a count for each edge. A run ends with `ret v` or with a trap (a division or remainder by 0). The machine issues at most 2 items per cycle, at most one multiply-unit operation (`*`, `/`, `%`, latency 3) and at most one branch (latency 1). Other operations have latency 1.

The output is a program that has the same outcome as the input on every input, the same returned value or a trap, and whose blocks are list schedules of traces. Loops are not handled here: real compilers unroll a loop and schedule traces inside its body, or use [software pipelining](/software-pipelining/).

## The algorithm

```pseudo id=main
TRACE-SCHEDULE(P, freq)
L1  while some block of P is not scheduled do
L2      T <- the seed of highest count, grown along edges that are most likely at both ends, never backward past the entry
L3      live <- the live-in sets of P
L4      D <- the dependence DAG of the items of T: data edges, branches in order, the end item last
L5      add an edge from each branch B to each later operation that may trap or whose result is in live(off(B))
L6      add an edge from each item to each later entrance, and from each entrance to each later branch
L7      S <- a list schedule of D by height; order the items by (cycle, original position)
L8      for each branch B of T do
L9          C <- the operations from above B that S puts after B
L10         put copies of C, in the order of S, in a new block on the off-trace edge of B
L11     for each entrance J of T into a block b do
L12         C <- the operations from below J that S puts before J
L13         put copies of C, in the order of S, in a new block that takes the label b and jumps to the code after J
L14     replace T by S cut after each branch and at each entrance; mark the pieces scheduled; update freq
L15 return P
```

**Trace selection (line L2).** The *seed* is the block not yet scheduled with the highest count, the larger of the sums of its incoming and its outgoing edge counts. The trace grows forward from its last block $a$ to the successor $b$ of the largest edge count, but only if $a$ is also the predecessor of $b$ with the largest count, and $b$ is not yet scheduled. It grows backward in the same way, and it stops at the entry block, so that the entry stays the head of its trace. This is the mutual most likely rule. Chang and Hwu (1988) describe this growth from a seed with a best successor and a best predecessor.

**Items (line L4).** In the original order, the *items* of the trace $b_1, \dots, b_k$ are: an *entrance* $J_j$ for each $b_j$, $j \ge 2$, that has a predecessor other than $b_{j-1}$; the instructions of each block; a *branch* item for each `br` of $b_j$, $j < k$, whose other target $\mathrm{off}(B)$ is off the trace; and the *end* item, the terminator of $b_k$. An entrance takes no issue slot.

**Dependences (lines L4 to L6).** The data edges are the usual true, anti and output dependences of [data dependence](/data-dependence/): a true dependence waits for the latency of the writer, an output dependence waits 1 cycle, and an anti dependence waits 0 cycles, so the two items can issue in the same cycle with the reader first. The branches keep their order, and every item comes before the end item. Line L5 lets an operation move above a branch only if it cannot trap and its result is dead on the off-trace edge. Such a motion is *speculation*: the operation runs also on runs that leave, and does nothing visible there. Line L6 keeps every item that is above an entrance above it, and keeps the order of entrances and branches. An operation may still move *above* an entrance.

**Compensation (lines L8 to L13).** An operation $u$ from above a branch $B$ that the schedule puts after $B$ does not run on a run that leaves at $B$. So lines L9 and L10 put a copy of it on that edge. An operation from below an entrance $J$ that the schedule puts before $J$ does not run on a run that comes in at $J$. So lines L12 and L13 put a copy of it on the side edges: the new block takes the label of $b_j$, which all side edges already use, and it jumps to the code after $J$. The trace edge from $b_{j-1}$ goes straight to that code.

**Cutting (line L14).** The schedule becomes blocks: a new block starts after each branch and at each entrance. The first piece keeps the label $b_1$. The compensation blocks are not scheduled yet, so later traces schedule them with their neighbors.

## Example

Take this program with parameters `a` and `b`, and the profile 90 for $B_0 \to B_1$ and $B_1 \to B_3$, and 10 for $B_0 \to B_2$ and $B_2 \to B_3$:

```
B0:
  c = b < 5
  s = a - b
  br c B1 B2
B1:
  y = a / b
  jump B3
B2:
  y = a - 1
  jump B3
B3:
  w = b + 1
  v = w * w
  z = y + v
  r = z + s
  ret r
```

Line L2 picks $B_0$, the block of highest count, and grows it to the trace $B_0, B_1, B_3$. Line L3 gives $\mathrm{live}(B_2) = \{a, b, s\}$. The items, with their units, latencies and heights, are:

| index | item | unit | latency | height |
|---|---|---|---|---|
| 0 | `c = b < 5` | alu | 1 | 7 |
| 1 | `s = a - b` | alu | 1 | 3 |
| 2 | branch, off $B_2$ | br | 1 | 6 |
| 3 | `y = a / b` | mul | 3 | 6 |
| 4 | entrance into $B_3$ | none | 0 | 1 |
| 5 | `w = b + 1` | alu | 1 | 7 |
| 6 | `v = w * w` | mul | 3 | 6 |
| 7 | `z = y + v` | alu | 1 | 3 |
| 8 | `r = z + s` | alu | 1 | 2 |
| 9 | `ret r` | br | 1 | 1 |

Line L5 adds the edge from the branch to `y = a / b`, since a division by `b` can trap. It adds no edge to `w`, `v`, `z` or `r`: they cannot trap and their names are dead at $B_2$. Line L6 keeps items 0 to 3 above the entrance. The list scheduler gives:

| cycle | ready, by height | issued |
|---|---|---|
| 0 | `c`, `w`, `s` | `c`, `w` |
| 1 | branch, `v`, `s`, then `y` once the branch issues | branch, `y` |
| 2 | `v`, `s`, then the entrance | `v`, `s`, entrance |
| 3, 4 | none | none |
| 5 | `z` | `z` |
| 6 | `r` | `r` |
| 7 | `ret r` | `ret r` |

The length is $7 + 1 = 8$ cycles. This is optimal. The two multiply-unit operations `y` and `v` cannot start at cycle 0, because `y` waits for the branch and `v` waits for `w`, and they cannot share cycle 1. So one of them starts at 2 or later, `z` starts at 5 or later, and `ret r` at 7 or later. Block by block, the best schedules of $B_0$, $B_1$ and $B_3$ take 2, 3 and 7 cycles, so the same path takes 12.

Two motions need copies. `s` moved below the branch, so line L10 puts `s = a - b` on the edge to $B_2$. `w` moved above the entrance into $B_3$ (and above the branch, which line L5 allows since `w` is dead at $B_2$), so line L13 makes a block with label $B_3$ that computes `w` and jumps to the code after the entrance. `y = a / b` stays below the branch. The second trace is the exit block, $B_2$ and the entrance block, which have no side entrance and become one block. The output is:

```
B0:
  c = b < 5
  w = b + 1
  br c B0.1 B0.2
B0.1:
  y = a / b
  s = a - b
  jump B0.3
B0.3:
  v = w * w
  z = y + v
  r = z + s
  ret r
B0.2:
  s = a - b
  y = a - 1
  w = b + 1
  jump B0.3
```

On $(a, b) = (1, 7)$ both programs take the rare path and return 58. On $(4, 2)$ both return 13, and on $(4, 0)$ both trap. Without the copy of `s` in `B0.2`, the run on $(1, 7)$ would read `s` before any write. The copy of `w` in `B0.2` is correct but not needed here: the only side entrance comes after `B0`, which has already computed `w`. Removing such copies is the subject of Freudenberger, Gross and Lowney (1994).

## Correctness

**Theorem.** On every input, the output of TRACE-SCHEDULE returns the same value as the input program, or traps exactly when the input program traps. The loop of line L1 stops.

The full proof is in the proof file. It goes one trace at a time. The dependence edges make the schedule keep the order of any two items that read or write the same name, and keep the branches and entrances in their original order. So from the head or from an entrance, the new code runs the same items as the old code with the same last writer for every read, up to the point where a run leaves. At a side exit, an operation from below that ran early cannot trap and wrote only a name that is dead there (line L5), and an operation from above that did not run yet is in the exit block (line L10). So both runs leave with the same values of the live names. The same holds at the end of the trace, and a trap happens in both runs or in neither. An induction over the blocks in reverse topological order finishes the step. For termination, the number of paths from the blocks not yet scheduled to the first scheduled block or `ret` drops by at least 1 with each trace, although the compensation blocks are new blocks.

## Complexity

Let $n$ be the number of items of one trace, $s$ the number of instructions and terminators of the program, $N$ the number of names and $m$ the number of traces.

- **Line L2.** The counts and the growth look at each edge a constant number of times: $O(s)$.
- **Line L3.** One backward pass in reverse topological order solves the liveness equations of an acyclic graph, with sets of at most $N$ names: $O(s N)$. The Python code repeats the pass until nothing changes, which can take more passes.
- **Lines L4 to L6.** The DAG has $O(n^2)$ edges. Each data edge, each branch edge and each entrance edge is made in $O(1)$: $O(n^2)$.
- **Line L7.** Heights in one pass over the edges, then a list schedule with a ready queue: $O(n^2 + n \log n)$, as the number of cycles is at most the sum of the latencies, $O(n)$. The Python code scans all items for each choice, which is $O(n^3)$.
- **Lines L8 to L14.** Each branch and each entrance copies at most $n$ operations: $O(n^2)$, and the rebuild is $O(s)$.

So one trace costs $O(s N + n^2)$, and the run costs $O(m (s N + n^2))$ time and $O(s N + n^2)$ space. Here $s$ is the size of the largest program during the run. The termination proof bounds $m$ by the number of paths, which can be exponential in the number of blocks, and the copies can make $s$ grow in the same way. In practice compilers limit the length of a trace and the motions that need copies.

## Properties

- **Correct for every input.** The profile only chooses the traces. A bad profile makes the code slower, never wrong.
- **The optimum is never worse than block by block.** The best schedule of the whole trace is at most the sum of the best schedules of its blocks, because the block schedules placed one after the other are a legal schedule of the trace. In the example, 8 cycles against 12. The list scheduler is a heuristic, so this holds for the optimum, not for every list schedule.
- **Slower rare paths.** A run that leaves at a side exit runs the exit block, and a run that comes in at a side entrance runs the entrance block. Their cost goes on the rare paths.
- **Code growth.** Every motion past a side exit or entrance makes a copy, and copies are scheduled again in later traces, where they can be copied again.
- **Speculation without hardware help.** Only operations that cannot trap move above a branch. With loads and stores this needs memory dependence analysis, or hardware with non-trapping loads.

## Variants and improvements

- **[Superblock scheduling](/superblock-scheduling/)** (Hwu et al. 1993) removes the side entrances first by tail duplication. Then only side exits need care, and the bookkeeping is much simpler, at the cost of more code.
- **Avoidance and suppression of compensation code** (Freudenberger, Gross and Lowney 1994). The scheduler can refuse a motion that needs a copy when the gain is small, or drop a copy whose value the side path already has, as with `w` in the example.
- **Better traces.** Chang and Hwu (1988) compare selection by block counts and by edge counts, and stop a trace when an edge is not likely enough. [Path profiles](/ball-larus-path-profiling/) give the real hot paths instead of a chain of locally likely edges.
- **Loops.** The trace stops at a back edge. Unrolling the loop with [loop unrolling](/loop-unrolling/) first gives longer traces. For loops with many iterations, [software pipelining](/software-pipelining/) overlaps the iterations instead.
- **Percolation scheduling** (Nicolau) moves operations one edge at a time by a small set of local transformations, each of which keeps the meaning, instead of scheduling a whole trace at once. Muchnick (Section 17.6) describes it.

## When to use it

Use it for a wide in-order machine, such as a VLIW or EPIC processor, on code with small blocks and branches that a profile can predict. There the machine does not reorder instructions, and a block alone has too little parallel work. Prefer [superblock scheduling](/superblock-scheduling/) when simple bookkeeping matters more than code size. On an out-of-order processor, the hardware already looks past branches, and the gain is smaller. For loops, use [iterative modulo scheduling](/iterative-modulo-scheduling/). Without a profile, the static guess of even branch splits gives traces that can slow down the paths that matter.

## Pitfalls

- **Speculating an operation that can trap.** If line L5 adds edges only for live names, a division can move above the branch that tests its divisor, and a run that leaves at that branch traps where the input did not. Line L5 must also add the edge for every operation that may trap.
- **Speculating a write to a live name.** If line L5 ignores $\mathrm{live}(\mathrm{off}(B))$, an operation from below the branch can overwrite a name that the off-trace path still reads. Use the live-in set of the off-trace target, computed by line L3 on the current program.
- **Missing exit copies.** If line L9 collects only the operations of the block of $B$, an operation from an earlier block that moved below $B$ is lost on the exit. In the example, dropping the copy of `s` makes the rare path read an undefined name. Take every operation from above $B$, in any block of the trace.
- **Moving an operation below an entrance.** If line L6 does not add the edges into the entrance, an operation from above the entrance can move below it, and then it also runs on the side path, where it did not run before. Keep every earlier item above the entrance.
- **Entrance copies on the wrong edge.** If line L13 gives the label $b_j$ to the piece after the entrance and puts the copies elsewhere, the side edges skip the copies. The new block must take the label $b_j$, which the side edges use, and the trace edge from $b_{j-1}$ must go past it.
- **Growing a trace backward past the entry.** If line L2 puts the entry block in the middle of a trace, the entry gets an entrance and its label moves to a new block. Stop the backward growth at the entry.

## Implementations

## History

Fisher developed trace scheduling in his 1979 NYU thesis and the 1981 paper to compact horizontal microcode, where one long instruction word controls many units at once. The copies on the side edges came from a separate bookkeeping phase. Ellis built the Bulldog compiler for VLIW machines on trace scheduling in his Yale thesis, published as a book in 1986. Fisher and others then founded Multiflow, whose TRACE machines (Colwell et al. 1988) and compiler (Lowney et al. 1993) were designed around the method. Chang and Hwu (1988) studied trace selection for C programs in the IMPACT compiler, and the same group then gave superblocks (Hwu et al. 1993). Freudenberger, Gross and Lowney (1994) measured how much compensation code the Multiflow compiler made and how to avoid it.

## References
