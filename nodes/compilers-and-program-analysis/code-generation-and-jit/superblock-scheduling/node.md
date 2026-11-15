---
tag: WWP2JP
kind: algorithm
slug: superblock-scheduling
name: Superblock scheduling
aliases:
- superblock formation
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Forms traces with one entry by tail duplication and schedules each as a block, with no compensation code at side entries.
solves: [instruction-scheduling-problem]
model: word-ram
complexity:
  vars: {n: the number of items of one superblock, s: the number of instructions and terminators of the program after formation, N: the number of names, m: the number of superblocks}
  time: {worst: O(m (s N + n^2))}
  space: {extra: O(s N + n^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1993
  people: [Wen-mei W. Hwu, Scott A. Mahlke, Pohua P. Chang]
  note: The IMPACT group at the University of Illinois built superblocks into the IMPACT-I C compiler, measured scheduling models for multiple-issue processors with them in 1991, and gave the full account of formation, optimization and scheduling in 1993.
prereqs: [trace-scheduling, instruction-scheduling-problem, list-scheduling, live-variable-analysis, profile-guided-optimization]
see_also: [software-pipelining, iterative-modulo-scheduling, speculative-code-motion, ball-larus-path-profiling, tracing-jit-compilation, loop-unrolling, path-based-scheduling, pettis-hansen-code-positioning]
sources:
  - paper: doi:10.1007/BF01205185
    title: Wen-mei W. Hwu, Scott A. Mahlke, William Y. Chen, Pohua P. Chang, Nancy J. Warter, Roger A. Bringmann, Roland G. Ouellette, Richard E. Hank, Tokuzo Kiyohara, Grant E. Haab, John G. Holm and Daniel M. Lavery, The superblock, an effective technique for VLIW and superscalar compilation, The Journal of Supercomputing 7(1-2), 1993, 229-248
    locator: the definition of a superblock as a trace with one entry and one or more exits, its formation by trace selection and tail duplication, the superblock optimizations, and superblock scheduling
  - paper: doi:10.1145/115952.115979
    title: Pohua P. Chang, Scott A. Mahlke, William Y. Chen, Nancy J. Warter and Wen-mei W. Hwu, IMPACT, an architectural framework for multiple-instruction-issue processors, Proceedings of the 18th Annual International Symposium on Computer Architecture, 1991, 266-275
    locator: the experiments on the code scheduling model, the issue rate, the load latency and the limits of the function units for code from the IMPACT-I C compiler
  - paper: doi:10.1109/micro.1988.639244
    title: Pohua P. Chang and Wen-mei W. Hwu, Trace selection for compiling large C application programs to microcode, Proceedings of the 21st Annual Workshop on Microprogramming and Microarchitecture, 1988, 21-29
    locator: Section 4 on trace selection by node weights and arc weights from a seed with the best successor and the best predecessor
  - paper: doi:10.1109/micro.1992.696999
    title: Scott A. Mahlke, David C. Lin, William Y. Chen, Richard E. Hank and Roger A. Bringmann, Effective compiler support for predicated execution using the hyperblock, Proceedings of the 25th Annual International Symposium on Microarchitecture, 1992, 45-54
    locator: the hyperblock, a block with one entry formed from several paths by if-conversion and predication, as an extension of the superblock
---

Superblock scheduling is a global [instruction scheduling](/instruction-scheduling-problem/) method. A *superblock* is a trace, a likely path through several basic blocks, that control can enter only at its head and can leave at many side exits. The method makes superblocks by *tail duplication*: when another path joins a trace in the middle, the part of the trace from that point to its end is copied, and the other path goes to the copy. Then each superblock is scheduled as one block. It differs from [trace scheduling](/trace-scheduling/) in where it pays for side entrances. Trace scheduling keeps them and puts compensation code on them after scheduling. Superblock scheduling removes them before scheduling, so it needs no compensation code at entrances and, with the motion rules of this page, none at exits either. The IMPACT group (Hwu et al. 1993) introduced it.

## In plain words

A program usually takes the same way through its branches. This method finds that usual way and makes sure that nothing can jump into the middle of it. Where some other path did jump in, the method gives that path its own copy of the rest of the way. Now the usual way is one straight line that can only be left early, never entered late. The scheduler packs that line tightly for a wide machine, and it moves an instruction past an early exit only when the exit does not need the instruction and the instruction cannot fail. So no repair code is needed. The price is the copied code, which makes the program larger.

## The problem

The input is a program in the toy IR of these pages: a [control flow graph](/control-flow-graph/) with no cycle whose blocks hold `const`, `copy` and `op` instructions and end with `jump`, `br` or `ret`, and an edge profile, a count for each edge. A run ends with `ret v` or with a trap (a division or remainder by 0, or a shift by an amount outside 0 to 63). The machine is the one of [trace scheduling](/trace-scheduling/): at most 2 items per cycle, at most one multiply-unit operation (`*`, `/`, `%`, latency 3) and at most one branch (latency 1). Other operations have latency 1.

The output is a program that has the same outcome as the input on every input, the same returned value or a trap, and whose blocks are list schedules of superblocks. Loops are not handled here. A real compiler forms superblocks inside a loop body, often after unrolling, or uses [software pipelining](/software-pipelining/).

## The algorithm

```pseudo id=main
SUPERBLOCK-SCHEDULE(P, freq)
L1  done <- empty; S <- empty list
L2  while some block of P is not in done do
L3      T = b1 .. bk <- the seed of highest count, grown along edges that are most likely at both ends, never into or backward past the entry
L4      j <- the least i >= 2 such that bi has a predecessor other than b(i-1); if there is none, go to L7
L5      for i <- j to k do make a copy ci of bi whose edges to a block bm with m >= j go to cm
L6      for i <- j to k do send each edge from a predecessor p != b(i-1) of bi to ci
L7      append T to S; add b1 .. bk to done
L8  for each superblock T in S do
L9      live <- the live-in sets of the current P
L10     D <- the dependence DAG of the items of T: data edges, and an edge from each item to the end item
L11     add an edge from each side exit B to each later branch, and to each later operation that may trap or writes a name of live(off(B))
L12     add an edge to each side exit B from each earlier operation that may trap or writes a name of live(off(B))
L13     t <- a list schedule of D by height; order the items by (t, original position)
L14     emit the items in that order, starting a new block after each side exit; the first piece keeps the label b1
L15 return P
```

**Formation (lines L1 to L7).** Line L3 picks a trace among the blocks not yet in a superblock, as in trace scheduling. The *seed* is the block of highest count, the larger of the sums of its incoming and its outgoing edge counts. The trace grows forward from its last block $a$ to the successor $b$ of the largest edge count, but only if $a$ is also the predecessor of $b$ with the largest count and $b$ is not done. It grows backward in the same way. It never takes the entry block except as its head. Chang and Hwu (1988) describe this growth with a best successor and a best predecessor. Line L4 finds the first *side entrance*, the first block after the head with a second predecessor. Lines L5 and L6 copy the tail $b_j, \dots, b_k$. A copy $c_i$ keeps the instructions of $b_i$. Its edges into the tail go to the copies, so the copies never become new side entrances. Every side edge into $b_i$ moves to $c_i$. After this, the trace edge from $b_{i-1}$ is the only edge into $b_i$, and $T$ is a superblock. The copies are new blocks that are not done, so later rounds put them in superblocks of their own.

**Items (line L10).** In the original order, the *items* of a superblock $b_1, \dots, b_k$ are: the instructions of each block, called *operations*; a *side exit* item for each `br` of $b_i$, $i < k$, whose other target $\mathrm{off}(B)$ leaves the superblock; and the *end* item, the terminator of $b_k$. A `jump` from $b_i$ to $b_{i+1}$ gives no item.

**Dependences (lines L10 to L12).** The data edges are the true, anti and output dependences of [data dependence](/data-dependence/): a true dependence waits for the latency of the writer, an output dependence waits 1 cycle, and an anti dependence waits 0 cycles. Line L11 keeps the side exits in order, and lets an operation from below a side exit move above it only if the operation cannot trap and its result is dead on the exit. Such a motion is safe *speculation*. Line L12 is the rule that replaces compensation code: an operation from above a side exit moves below it only under the same two conditions. Then a run that leaves at the exit does not need the operation, and it is correct that the operation did not run. Trace scheduling lets such an operation move and puts a copy on the exit edge instead.

**Emission (line L14).** The scheduled items run in the order of $(t, \text{original position})$, so items with a delay 0 between them can share a cycle. A new block starts after each side exit and ends with the old `br` on the same condition, to the next piece and to the old exit target. The other labels of the superblock disappear: by tail duplication, nothing else jumps to them.

## Example

Take the program of the [trace scheduling](/trace-scheduling/) page, with parameters `a` and `b`, and the profile 90 for $B_0 \to B_1$ and $B_1 \to B_3$, and 10 for $B_0 \to B_2$ and $B_2 \to B_3$:

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

**Formation.** Line L3 picks $B_0$, the block of highest count, and grows it to $B_0, B_1, B_3$. The block $B_3$ has a second predecessor, $B_2$, so line L4 gives $j = 3$. Lines L5 and L6 make the copy `B3.1` of $B_3$ and send the edge $B_2 \to B_3$ to it. The second round picks $B_2$ and grows it to $B_2$, `B3.1`, which has no side entrance. The formed program has the two superblocks below, and four more instructions than the input.

| round | trace | first side entrance | copies | edge counts after the round |
|---|---|---|---|---|
| 1 | $B_0, B_1, B_3$ | $B_3$, from $B_2$ | `B3.1` | $B_1 \to B_3$: 90, $B_2 \to$ `B3.1`: 10 |
| 2 | $B_2$, `B3.1` | none | none | unchanged |

**Scheduling the first superblock.** Line L9 gives $\mathrm{live}(B_2) = \{a, b, s\}$. The items, with their units, latencies, heights and cycles, are:

| index | item | unit | latency | height | cycle |
|---|---|---|---|---|---|
| 0 | `c = b < 5` | alu | 1 | 7 | 0 |
| 1 | `s = a - b` | alu | 1 | 6 | 1 |
| 2 | side exit, off $B_2$ | br | 1 | 6 | 1 |
| 3 | `y = a / b` | mul | 3 | 6 | 2 |
| 4 | `w = b + 1` | alu | 1 | 7 | 0 |
| 5 | `v = w * w` | mul | 3 | 6 | 3 |
| 6 | `z = y + v` | alu | 1 | 3 | 6 |
| 7 | `r = z + s` | alu | 1 | 2 | 7 |
| 8 | `ret r` | br | 1 | 1 | 8 |

Line L11 adds the edge from the exit to `y = a / b`, since a division by `b` can trap. It adds no edge to `w`, `v`, `z` or `r`: they cannot trap and their names are dead at $B_2$. Line L12 adds the edge from `s = a - b` to the exit, since `s` is live at $B_2$. The list scheduler gives:

| cycle | ready, by height | issued |
|---|---|---|
| 0 | `c`, `w`, `s` | `c`, `w` |
| 1 | `s`, exit, `v` (all of height 6) | `s`, exit |
| 2 | `y`, `v` | `y` (one multiply unit) |
| 3 | `v` | `v` |
| 4, 5 | none | none |
| 6 | `z` | `z` |
| 7 | `r` | `r` |
| 8 | `ret r` | `ret r` |

The length is $8 + 1 = 9$ cycles. The optimum for this DAG is 8: `v` and `s` at cycle 1, the exit and `y` at cycle 2, `z` at 5. The list scheduler breaks the tie at cycle 1 by original position and fills the cycle with `s` and the exit, so the two multiplies start one cycle later. Trace scheduling reaches 8 cycles on the same path with this list scheduler, because it moves `s` below the exit and puts a copy of `s` on the exit edge. Line L12 forbids that motion here. Block by block, the same path takes $2 + 3 + 7 = 12$ cycles.

**The second superblock.** $B_2$, `B3.1` is one block of six items. Its list schedule puts `y` and `w` at cycle 0, `v` at 1, `z` at 4, `r` at 5 and `ret r` at 6, a length of 7, which is optimal. The output is:

```
B0:
  c = b < 5
  w = b + 1
  s = a - b
  br c B0.1 B2
B0.1:
  y = a / b
  v = w * w
  z = y + v
  r = z + s
  ret r
B2:
  y = a - 1
  w = b + 1
  v = w * w
  z = y + v
  r = z + s
  ret r
```

The operation `w = b + 1` moved above the exit by speculation. It also runs on the rare path, where its value is computed again in `B2`. No other code was added: the output has 12 instructions, the same as the formed program, while the trace scheduling output has 10. On $(a, b) = (1, 7)$ both the input and the output take the rare path and return 58. On $(4, 2)$ both return 13, and on $(4, 0)$ both trap.

## Correctness

**Theorem.** On every input, the output of SUPERBLOCK-SCHEDULE returns the same value as the input program, or traps exactly when the input program traps. Formation stops, and scheduling adds no instruction.

The full proof is in the proof file. For formation, each block of the new program maps to a block of the old one with the same instructions and the same targets after the map, so the two programs run in step. After the copies, the only edge into $b_i$, $i \ge 2$, is from $b_{i-1}$, and later rounds keep this. Formation stops because the number of paths from the blocks not yet done drops by at least 1 in each round, although the copies are new blocks. For scheduling, the edges keep the order of any two items that read or write the same name, and the order of the exits. An operation that crosses an exit in either direction cannot trap and writes only a name that is dead on the exit (lines L11 and L12). So a run that leaves at an exit sees the same values of the live names as before, a run that reaches the end item sees the same values of all names, and a trap happens in both runs or in neither. An induction over the blocks in reverse topological order finishes the proof.

## Complexity

Let $n$ be the number of items of one superblock, $s$ the number of instructions and terminators of the program after formation, $N$ the number of names and $m$ the number of superblocks.

- **Lines L3 to L7.** The counts, the growth and the copies look at each edge and each instruction a constant number of times: $O(s)$ per round.
- **Line L9.** One backward pass in reverse topological order solves the liveness equations of an acyclic graph, with sets of at most $N$ names: $O(s N)$.
- **Lines L10 to L12.** The DAG has $O(n^2)$ edges, and each one is made in $O(1)$: $O(n^2)$.
- **Line L13.** Heights in one pass over the edges, then a list schedule with a ready queue: $O(n^2 + n \log n)$, as the number of cycles is at most the sum of the latencies, $O(n)$. The Python code scans all items for each choice, which is $O(n^3)$.
- **Line L14.** $O(n)$ for the pieces and $O(s)$ for the rebuild.

So the run costs $O(m (s N + n^2))$ time and $O(s N + n^2)$ space. Tail duplication can make $s$ exponential in the number of blocks of the input, since a tail copied in one round can be copied again in later rounds. Real compilers limit the length of a superblock and the amount of copied code.

## Properties

- **Correct for every input.** The profile only chooses the superblocks. A bad profile makes the code slower, never wrong.
- **No compensation code.** All new instructions come from tail duplication, before scheduling. Scheduling only reorders.
- **Simpler than trace scheduling.** There are no entrances in a superblock, so the scheduler needs no entrance items, no entrance copies and no rejoin blocks. The copies also make a superblock a better target for classic optimizations, since no other path reaches its middle.
- **The optimum is never worse than block by block.** The best schedule of a superblock is at most the sum of the best schedules of its blocks. The list scheduler is a heuristic, so this holds for the optimum, not for every list schedule.
- **Less freedom at exits.** An operation whose result is live on an exit cannot move below it, so some schedules of trace scheduling are not possible, as for `s` in the example.
- **Code growth.** Each side entrance copies the whole tail after it, also code that is not on the hot path.

## Variants and improvements

- **Superblock optimizations** (Hwu et al. 1993). Since a superblock has one entry, the compiler can unroll superblock loops, rename registers and expand accumulators and induction variables inside it before scheduling, to remove dependences.
- **Speculation with hardware help.** With instructions that do not trap, such as non-trapping loads, the scheduler can also move operations that may trap above an exit. The IMPACT papers compare such scheduling models (Chang et al. 1991).
- **Hyperblocks** (Mahlke et al. 1992). If-conversion turns several paths into one block with one entry and predicated instructions, so that a rare path no longer cuts the hot one.
- **Better traces.** [Path profiles](/ball-larus-path-profiling/) give the real hot paths instead of a chain of locally likely edges. A [tracing JIT](/tracing-jit-compilation/) records a hot path at run time and compiles it as a superblock-like trace with one entry and many exits.
- **Loops.** The superblock stops at a back edge. [Loop unrolling](/loop-unrolling/) gives longer superblocks, and [software pipelining](/software-pipelining/) overlaps iterations instead.

## When to use it

Use it for a wide in-order machine, such as a VLIW or EPIC processor, on code with small blocks and branches that a profile can predict, when a simple scheduler matters more than code size. It suits compilers that run classic optimizations on the hot path too, since a superblock is easier to optimize than a trace with entrances. Prefer [trace scheduling](/trace-scheduling/) when code size is tight, or when moving an operation below an exit matters. On an out-of-order processor the gain is smaller. For loops with many iterations, use [iterative modulo scheduling](/iterative-modulo-scheduling/).

## Pitfalls

- **Moving the trace edge to the copy.** If line L6 sends every edge into $b_i$ to $c_i$, the edge from $b_{i-1}$ also goes to the copy, and $b_i$ is no longer reached from the trace. Move only the edges from predecessors $p \ne b_{i-1}$.
- **Copies that point back into the tail.** If line L5 keeps the targets of $b_i$ in $c_i$, the copy jumps to $b_{i+1}$, which gets a new side entrance from $c_i$. The copy edges into $b_m$, $m \ge j$, must go to $c_m$.
- **Starting the copy at the last side entrance.** If line L4 takes the greatest such $i$, the earlier side entrances stay in the superblock. Take the least $i$, so that the copied tail covers all of them.
- **Moving a live write below an exit.** If line L12 is left out, as in a trace scheduler that relies on copies, an operation can move below an exit whose path reads its result, and the rare path reads an old value. In the example, `s` would move below the exit and the run on $(1, 7)$ would read `s` before any write. Keep line L12, or add compensation code.
- **Speculating an operation that can trap.** If line L11 adds edges only for live names, a division from below an exit can move above it, and a run that leaves at that exit with a divisor of 0 traps where the input did not. Line L11 must also add the edge for every operation that may trap.
- **Stale live sets.** If line L9 runs once on the input, the copies have no live sets and the exit targets of later superblocks have the wrong ones. Compute live-in sets on the current program.

## Implementations

## History

Fisher introduced trace scheduling in 1981, with a bookkeeping phase that copies operations onto the side entrances and exits of a trace. Chang and Hwu (1988) studied trace selection for C programs in the IMPACT compiler at the University of Illinois. In 1991 Chang, Mahlke, Chen, Warter and Hwu used superblocks in the IMPACT-I C compiler to measure scheduling models, issue rates and load latencies for multiple-issue processors. Hwu and eleven coauthors gave the full account in 1993: trace selection, tail duplication, a set of optimizations on superblocks, and superblock scheduling, with large speedups on a 4-issue processor. Mahlke and others extended the idea to hyperblocks with predication in 1992. The idea of a region with one entry and many exits reappeared in dynamic optimizers and tracing JIT compilers.

## References
