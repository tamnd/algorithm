---
tag: FQP3X8
kind: technique
slug: profile-guided-optimization
name: Profile-guided optimization
aliases:
- feedback-directed optimization
area: compilers-and-program-analysis/optimizations
level: core
summary: Runs the program on sample input to measure branch and call frequencies, then uses them to guide inlining, layout and allocation.
prereqs: [control-flow-graph, basic-block, function-inlining]
see_also: [ball-larus-path-profiling, pettis-hansen-code-positioning, type-feedback, just-in-time-compilation, trace-scheduling, superblock-scheduling, maximum-spanning-tree, flow-conservation]
sources:
  - paper: doi:10.1002/spe.4380010203
    title: Donald E. Knuth, An empirical study of FORTRAN programs, Software, Practice and Experience 1(2), 1971, 105-133
    locator: the frequency counts of statements in real programs and the finding that a small part of a program takes most of its time
  - paper: doi:10.1145/183432.183527
    title: Thomas Ball and James R. Larus, Optimally profiling and tracing programs, ACM Transactions on Programming Languages and Systems 16(4), 1994, 1319-1360
    locator: edge profiling with counters on the chords of a spanning tree, the derivation of the other counts by flow conservation, and the choice of a maximum spanning tree by estimated weights
  - paper: doi:10.1109/MICRO.1996.566449
    title: Thomas Ball and James R. Larus, Efficient path profiling, Proceedings of the 29th Annual IEEE/ACM International Symposium on Microarchitecture (MICRO-29), Paris, 1996, 46-57
    locator: path profiles, and the cases where edge profiles cannot tell which paths ran
  - paper: doi:10.1145/93542.93550
    title: Karl Pettis and Robert C. Hansen, Profile guided code positioning, Proceedings of the ACM SIGPLAN 1990 Conference on Programming Language Design and Implementation (PLDI), 16-27
    locator: the ordering of procedures and of basic blocks by profile counts, and the splitting of code that never ran
  - paper: doi:10.1002/spe.4380211204
    title: Pohua P. Chang, Scott A. Mahlke and Wen-mei W. Hwu, Using profile information to assist classic code optimizations, Software, Practice and Experience 21(12), 1991, 1301-1321
    locator: the selection of traces by profile, superblock formation by tail duplication, and classic optimizations applied to the superblocks
  - paper: doi:10.1145/113446.113451
    title: David W. Wall, Predicting program behavior using real or estimated profiles, Proceedings of the ACM SIGPLAN 1991 Conference on Programming Language Design and Implementation (PLDI), 59-70
    locator: how well a profile from one input predicts the behavior on another input, against profiles estimated without running the program
  - paper: doi:10.1109/TC.1981.1675827
    title: "Joseph A. Fisher, Trace scheduling: a technique for global microcode compaction, IEEE Transactions on Computers C-30(7), 1981, 478-490"
    locator: the choice of the most likely trace by estimated or measured branch probabilities, and the compensation code off the trace
  - paper: doi:10.1145/178243.178478
    title: Urs Hölzle and David Ungar, Optimizing dynamically-dispatched calls with run-time type feedback, Proceedings of the ACM SIGPLAN 1994 Conference on Programming Language Design and Implementation (PLDI), 326-336
    locator: the receiver types recorded at call sites, and the inlining of the common target behind a type test
  - paper: doi:10.1145/2854038.2854044
    title: "Dehao Chen, David Xinliang Li and Tipp Moseley, AutoFDO: automatic feedback-directed optimization for warehouse-scale applications, Proceedings of the 2016 International Symposium on Code Generation and Optimization (CGO), 12-23"
    locator: profiles collected by hardware sampling on production machines and mapped back to the source, without an instrumented build
  - paper: doi:10.1109/CGO.2019.8661201
    title: "Maksim Panchenko, Rafael Auler, Bill Nell and Guilherme Ottoni, BOLT: a practical binary optimizer for data centers and beyond, Proceedings of the 2019 IEEE/ACM International Symposium on Code Generation and Optimization (CGO), 2-14"
    locator: block and function layout of a linked binary from sampled profiles
---

Profile-guided optimization (PGO) compiles a program twice. The first build is run on sample input, and it records how often each branch goes each way and how often each call site runs. The second build reads these counts, the *profile*, and uses them where a compiler must otherwise guess: which calls to inline, which order to put blocks and functions in, which values to keep in registers, and which paths to optimize at the cost of others. Knuth's study of 1971 showed that a small part of a program takes most of its time, and a profile tells the compiler which part that is. The idea is old: Fisher's trace scheduling of 1981 already picked traces by branch probabilities, and Pettis and Hansen used counts to lay out code in 1990. Today GCC, LLVM and other compilers have PGO, sampling tools such as AutoFDO collect profiles from production machines, and most [JIT compilers](/just-in-time-compilation/) are PGO systems that profile while they run. The common mistake is to think that a profile can make the program wrong. It cannot, if each transformation is legal for all inputs; a bad profile only makes the program slower.

## In plain words

A compiler often has to guess. Which way does this branch usually go? Is this function called a million times or once? A wrong guess costs speed.

So we stop guessing. We build the program with small counters added, run it on typical input, and save the counts. Then we build it again, and the compiler reads the counts. It puts the code that runs often in a straight line, so the processor does not jump. It copies small functions that are called often into their callers. It moves code that never ran out of the way.

The counts only change choices that are safe in any case. If the real input behaves differently from the sample, the program is still correct. It is just not as fast as it could be.

## When it applies

- There is input that looks like the real workload, and the build can run it. A profile from a different workload can make things worse.
- The program has hot code whose speed depends on choices that static analysis cannot make well: branches whose direction depends on data, call sites with many possible callees, or a code size that does not fit the instruction cache.
- The build system can afford two builds and keep a profile next to the source, and refresh it when the code or the workload changes.
- In a JIT, the same ideas apply without a separate run: the interpreter or the first tier records the counts, and the optimizing tier uses them, as in [type feedback](/type-feedback/).

## The template

**The three steps.** (1) *Instrument* the program, or prepare to *sample* it with hardware counters. (2) *Train*: run it on representative input and write the profile. (3) *Optimize*: compile again and let each heuristic read the profile.

**Kinds of profile.** An *edge profile* gives, for each edge $u \to v$ of the [control-flow graph](/control-flow-graph/) of each function, the number of times a run took that edge. Block counts follow from it: the count of a block is the sum of the counts of its in-edges. A *path profile* counts whole acyclic paths, as in [Ball-Larus path profiling](/ball-larus-path-profiling/). A *call-site profile* counts each call site and, for indirect calls, each target. A *value profile* records common values of an operand, such as the length of a copy.

**Legality.** *Theorem 1. Let every transformation that the optimizer may apply be legal, meaning that it gives an equivalent program for every input. Then the optimized program is equivalent to the source for every profile, including a stale or wrong one.* Proof. The profile only chooses which legal transformations to apply and where. Each one replaces a program by an equivalent one, and equivalence is transitive, so the result is equivalent to the source, whatever the choices were. $\square$

Some transformations are legal only under a guard: inline the common target of an indirect call, or specialize a loop for the common value of a variable. These are written as `t = guard; br t Lfast Lslow`, where `Lfast` is the specialized code and `Lslow` is the original code. If the specialized code is equivalent to the original whenever the guard holds, the guarded form is equivalent to the original for every input. The profile decides only whether the guard is worth its cost. In a JIT, the slow path can be a [deoptimization](/deoptimization/) to the interpreter.

**Profit.** For a cost model that charges a cost $c(e)$ each time a run takes an edge $e$, the cost of a run is $\sum_e n(e)\, c(e)$, where $n(e)$ is the edge count of that run. A layout, an inlining plan or a register assignment changes the $c(e)$, and the profile gives the $n(e)$. So the optimizer minimizes the cost of the training run. This is also the cost of the real run to the extent that the real counts are proportional to the training counts. There is no guarantee beyond that; Wall measured how well profiles from one input predict another.

**Edge profiling with few counters.** Add a virtual edge from the exit block to the entry block. Then, for a run from entry to exit, every block $v$ has *flow conservation*: the counts on the edges into $v$ sum to the counts on the edges out of $v$. Let the graph have $V$ blocks and $E$ edges, with the virtual edge, and let every block lie on a path from the entry to the exit, so that the graph is connected.

*Theorem 2. (a) For any [spanning tree](/spanning-tree/) $T$ of the graph, with edge directions ignored, the counts on the $E - V + 1$ edges not in $T$, the chords, determine all counts. (b) No set of fewer than $E - V + 1$ edges determines all count vectors that satisfy flow conservation.*

Proof. (a) The unknown edges are the edges of $T$. While some remain, they form a forest; a tree of that forest with at least one edge has a leaf $v$, which has exactly one unknown edge $e$. All other edges at $v$ are known, so conservation at $v$ gives the count of $e$. Remove $e$ and repeat. (b) Write conservation as $A n = 0$, where $A$ is the $V \times E$ matrix with $+1$ in the row of the head of each edge and $-1$ in the row of its tail. The rows of $A$ sum to zero, so its rank is at most $V - 1$. The columns of the $V - 1$ edges of $T$ are independent: in a combination of them that is zero, the coefficient of an edge at a leaf of $T$ is zero, since only that edge has a nonzero entry in the row of the leaf, and the argument repeats on the rest of the tree. So the rank is $V - 1$, and the solutions of $A n = 0$ form a space of dimension $E - V + 1$. If $C$ is a set of fewer edges, the map that keeps the counts on $C$ has a nonzero vector $z$ in its kernel. Take a solution $n$ with all counts positive: each edge lies on a path from the entry to the exit, which closes into a cycle with the virtual edge, and the sum of these cycles is such a solution. Take also a small rational $\epsilon > 0$. Then $n$ and $n + \epsilon z$ are both solutions with positive counts, and after scaling both to integers, they agree on $C$ and differ elsewhere. $\square$

So the counters go on the chords. To make the counters cheap, choose $T$ as a [maximum spanning tree](/maximum-spanning-tree/) for estimated edge weights, so that the edges that are expected to be hot are in the tree and carry no counter. This is the placement of Ball and Larus.

**Uses of the profile.**

- *Block layout*: put the hot successor of each block right after it, so that the hot edge falls through, as in [Pettis-Hansen code positioning](/pettis-hansen-code-positioning/). Move blocks that never ran to the end of the function or to a cold section.
- *Function layout*: put functions that call each other often next to each other, so that hot code shares pages and cache lines.
- *Inlining*: spend a code size budget on the call sites with the most calls per byte of growth, a [knapsack](/knapsack-problem/) choice, instead of the smallest callees.
- *Register allocation*: weight the spill cost of each use by its block count, so that spills go into cold code, as in [linear scan](/linear-scan-register-allocation/) with weights.
- *Traces and superblocks*: pick the most frequent path and optimize it as a unit, as in [trace scheduling](/trace-scheduling/) and [superblock scheduling](/superblock-scheduling/).
- *Speculation*: [devirtualize](/devirtualization/) an indirect call to its common target behind a guard, or [unroll](/loop-unrolling/) a loop by its common trip count.

## Classic examples

The numbers come from a Python script that runs the toy function below on lists of integers. Each element is negative with probability $p$, drawn from $-9$ to $-1$, and otherwise from $0$ to $9$. The training input has 1000 elements, $p = 0.1$ and seed 1; the test input has 1000 elements, $p = 0.1$ and seed 2; the stale training input has 1000 elements, $p = 0.9$ and seed 3.

```
B0: i = 0
    s = 0
    jump B1
B1: t = i < n
    br t B2 B6
B2: x = a[i]
    u = x < 0
    br u B3 B4
B3: y = neg(x)
    s = s + y
    jump B5
B4: y = scale(x)
    s = s + y
    jump B5
B5: i = i + 1
    jump B1
B6: ret s
```

**Counters on chords.** The graph has $V = 7$ blocks and $E = 9$ edges with the virtual edge `B6 -> B0`, so Theorem 2 needs $9 - 7 + 1 = 3$ counters. With estimated weight 10 for the edges in the loop and 1 for the others, and a preference for the `else` path, the maximum spanning tree leaves the chords `B3 -> B5`, `B5 -> B1` and `B6 -> B0`. On the training input, these counters read 108, 1000 and 1. Peeling leaves gives the rest:

| edge | count | how it is found |
|---|---|---|
| `B6 -> B0` | 1 | counter |
| `B0 -> B1` | 1 | conservation at `B0`: in 1 |
| `B1 -> B6` | 1 | conservation at `B6`: out 1 |
| `B5 -> B1` | 1000 | counter |
| `B1 -> B2` | 1000 | at `B1`: in $1 + 1000$, minus out 1 |
| `B3 -> B5` | 108 | counter |
| `B2 -> B3` | 108 | at `B3`: out 108 |
| `B2 -> B4` | 892 | at `B2`: in 1000, minus 108 |
| `B4 -> B5` | 892 | at `B4`: in 892 |

The derived counts equal the counts of a full count of every edge, on the training input and on 50 random inputs of length 0 to 50 with $p = 0.3$ and seeds 10 to 59. The three counters do 1109 increments, against 4003 for a counter on every edge. The chord `B5 -> B1` is hot because every cycle of the graph needs a chord, and the loop is a cycle.

**Block layout.** Charge 1 for each edge that a run takes when its target is not the next block in the layout, which is a taken branch or a jump. On the test input:

| layout | order | taken |
|---|---|---|
| source order | `B0 B1 B2 B3 B4 B5 B6` | 2001 |
| greedy chains, training profile | `B0 B3 B5 B1 B2 B4 B6` | 1002 |
| greedy chains, stale profile | `B0 B4 B5 B1 B2 B3 B6` | 1002 |

The greedy chains join blocks along the heaviest edges first, as in Pettis and Hansen, and start with the chain of the entry. A search over all 720 orders that start with `B0` finds no layout below 1002. There is a simple reason: each of the 1000 iterations runs a cycle, and the fall-through edges of a layout form paths, never a cycle, so each iteration takes at least one branch. In the source order, the common edge `B2 -> B4` and the back edge are both taken. Here the stale profile happens to cost the same: it moves the one taken branch per iteration from `B4 -> B5` to `B2 -> B4`.

**Inlining.** Suppose inlining `neg` at `B3` adds 4 instructions, inlining `scale` at `B4` adds 8, and the budget is 8. On the test input, `B3` calls `neg` 95 times and `B4` calls `scale` 905 times.

| rule | inlines | calls left on test |
|---|---|---|
| smallest callee first | `neg` | 905 of 1000 |
| most calls per instruction, training profile | `scale` | 95 of 1000 |
| most calls per instruction, stale profile | `neg` | 905 of 1000 |

The stale profile, where 901 of 1000 elements were negative, makes the compiler spend the budget on the cold call. The program is still correct, by Theorem 1.

## Variations

- **Instrumented PGO.** The compiler adds counters, as above. The profile is exact for the training run, but the instrumented build is slower, and the training runs must happen on a separate build.
- **Sampling PGO.** AutoFDO samples the branches that the hardware records on production machines and maps them back to source lines. There is no special build, and the profile comes from the real workload, at the cost of some loss of precision.
- **Post-link optimization.** BOLT reads a sampled profile and lays out the blocks and functions of the linked binary again, which can catch code that the compiler did not see, such as libraries and code from other languages.
- **JIT compilation.** A [JIT](/just-in-time-compilation/) counts calls and loop iterations to decide what to compile, and records receiver types in [inline caches](/inline-caching/) for type feedback. Its profile is always fresh, but it pays for profiling at run time.
- **Path profiles.** An edge profile cannot always tell which paths ran. When two branches are correlated, a [path profile](/ball-larus-path-profiling/) can, and trace formation can use it.
- **Static estimates.** Without a run, a compiler estimates the counts from the structure of the code, for example that a loop runs about ten times and that a branch to an error path is rare. Wall compared such estimates with real profiles.

## Pitfalls

- **A stale or unrepresentative profile.** In the inlining example, a profile from different data inlines the cold call. Refresh profiles when the code or the workload changes, and train on input that looks like production.
- **Profiles that do not match the code.** After the source changes, the counts of a function may not fit its new graph. Compilers check a hash of the graph and drop counts that do not match, which loses the profile for that function.
- **Counter overhead and placement.** A counter on every edge costs time and can change the behavior it measures. Use the chords of a spanning tree, and put the tree on the hot edges.
- **Hot counters on the chords.** Every cycle needs a chord, so a loop always carries one counter that runs on each iteration. Choosing the tree by estimated weights keeps the other counters on cold edges.
- **Speculation without a guard.** Inlining the common target of an indirect call without a type test is wrong for the rare call. Theorem 1 holds only for transformations that are legal for every input.
- **Overfitting a benchmark.** Training and measuring on the same input shows the best case. Measure on input that was not used for training, as with the separate test input above.
- **Code growth.** Inlining and duplication along hot paths grow the code. A budget in instructions keeps the cold code small, and the cold sections keep it out of the instruction cache.

## Exercises

1. For the toy function, choose a spanning tree that leaves the chord on `B2 -> B4` instead of `B5 -> B1`. How many increments do the counters do on the training input?
2. Without the virtual edge, prove that the in-edges and the out-edges of each block other than the entry and the exit have the same total count, and that at the entry and the exit the two totals differ by the number of runs.
3. Give a graph with two branches in sequence and two runs with the same edge profile and different path profiles.
4. Show that a layout of the toy function in which `B1 -> B2`, `B2 -> B4`, `B4 -> B5` and `B5 -> B1` all fall through cannot exist.
5. A guarded devirtualization tests the receiver type and calls the inlined body or the original call. Write it in the toy IR and prove that it is equivalent to the original call for every receiver.

## References
