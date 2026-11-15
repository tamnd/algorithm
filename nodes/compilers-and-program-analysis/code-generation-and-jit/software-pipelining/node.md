---
tag: 3SECX7
kind: technique
slug: software-pipelining
name: Software pipelining
aliases:
- loop pipelining
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Overlaps iterations of a loop so that a new iteration starts before the previous ends, with a prologue, steady kernel and epilogue.
prereqs: [instruction-scheduling-problem, list-scheduling, data-dependence, loop-carried-dependence]
see_also: [iterative-modulo-scheduling, sdc-modulo-scheduling, loop-unrolling, iteration-bound, retiming, dsp-unfolding, trace-scheduling, vectorization]
sources:
  - paper: doi:10.1145/1014192.802449
    title: B. Ramakrishna Rau and Christopher D. Glaeser, Some scheduling techniques and an easily schedulable horizontal architecture for high performance scientific computing, Proceedings of the 14th Annual Microprogramming Workshop, 1981, 183-198
    locator: the schedule of one iteration that starts a new iteration at a fixed interval, with the resources reserved modulo that interval, and the machine designed to make such schedules easy to find
  - paper: doi:10.1145/53990.54022
    title: Monica Lam, Software pipelining, an effective scheduling technique for VLIW machines, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation, 1988, 318-328
    locator: modulo scheduling with lower bounds from resources and recurrences, modulo variable expansion, and hierarchical reduction of conditional statements, in the compiler for the Warp machine
  - paper: doi:10.1145/212094.212131
    title: Vicki H. Allan, Reese B. Jones, Randall M. Lee and Stephen J. Allan, Software pipelining, ACM Computing Surveys 27(3), 1995, 367-432
    locator: the survey of modulo scheduling and kernel recognition methods, with the prologue, kernel and epilogue, the bounds on the initiation interval, and register needs
  - paper: doi:10.1145/192724.192731
    title: B. Ramakrishna Rau, Iterative modulo scheduling, an algorithm for software pipelining loops, Proceedings of the 27th Annual International Symposium on Microarchitecture, 1994, 63-74
    locator: the definitions of ResMII and RecMII and the iterative search over initiation intervals
  - paper: doi:10.1109/c-m.1981.220595
    title: Alan E. Charlesworth, An approach to scientific array processing, the architectural design of the AP-120B/FPS-164 family, Computer 14(9), 1981, 18-27
    locator: the overlapped loop code of the FPS array processors
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Section 17.4 (Software Pipelining)
---

Software pipelining is a technique for scheduling loops. It overlaps the iterations of a loop: a new iteration starts every $II$ cycles, the *initiation interval*, before the earlier ones end, like the stages of a hardware pipeline. The code that results has three parts: a *prologue* that starts the first iterations, a *kernel* of $II$ cycles that repeats and holds pieces of several iterations at once, and an *epilogue* that finishes the last ones. This page is about the technique and what any software pipeliner must do. [Iterative modulo scheduling](/iterative-modulo-scheduling/) is one algorithm for its central step, the choice of a start time for each operation at a given $II$. Other algorithms for that step are [SDC-based modulo scheduling](/sdc-modulo-scheduling/), swing modulo scheduling and integer programming. Two lower bounds hold for every one of them: $II$ is at least the resource bound $\mathrm{ResMII}$ and at least the recurrence bound $\mathrm{RecMII}$.

## In plain words

A loop body often has a chain of steps that wait for each other: load a number, multiply it, add, store. One pass alone keeps most of the machine idle. A laundry does not wait for one load to dry before it washes the next. In the same way, the compiler starts the next pass of the loop a few cycles after the previous one, while that one is still busy, so that the passes overlap and the units stay busy. In the middle of the run, each short repeated stretch of code does one step of several different passes. The start and the end of the run need extra code, to fill the overlap and to empty it.

## When it applies

- An inner loop runs many times, and its body is straight-line code, or can be made straight-line by if-conversion.
- One iteration alone is long compared to what the machine could issue: its dependence chain is long, or it uses few of the units.
- The machine issues several operations per cycle and does not reorder them by itself, as in VLIW, EPIC and DSP processors, or the target is hardware, as in [high-level synthesis](/high-level-synthesis/).
- The dependences that cross iterations, the [loop-carried dependences](/loop-carried-dependence/), are known, each with its distance in iterations, and their cycles are short compared to the body.
- There are enough registers for the values of the overlapped iterations, or the machine has rotating registers.

## The template

The body is a set of operations, each with a resource class and a latency. A dependence edge $(u, v)$ has a delay $\delta(u, v)$, usually the latency of $u$, and a distance $d(u, v) \ge 0$: operation $v$ of iteration $i + d$ depends on operation $u$ of iteration $i$. Iteration $i$ starts at cycle $i \cdot II$, and operation $v$ of iteration $i$ runs at cycle $i \cdot II + t(v)$.

```pseudo id=main
SOFTWARE-PIPELINE(loop, machine)
L1  G <- DEPENDENCES(loop body)                  ▷ hole: edges with a delay and a distance
L2  II <- max(ResMII, RecMII)
L3  repeat
L4      t <- PLACE(G, II, machine)               ▷ hole: a modulo scheduler, may fail
L5      if PLACE failed then II <- II + 1
L6  until PLACE succeeded
L7  stage(v) <- floor(t(v) / II); SC <- 1 + max over v of stage(v)
L8  NAMES <- RENAME(t, II)                       ▷ hole: modulo variable expansion or rotating registers
L9  emit the prologue (SC - 1 passes), the kernel, and the epilogue (SC - 1 passes)
L10 emit GUARD(SC)                               ▷ hole: run the plain loop when the trip count is below SC - 1
```

**The bounds (line L2).** If a resource class $r$ has $c_r$ units and the body uses it $u_r$ times, then in the steady state $II$ cycles must hold $u_r$ uses, so $II \ge \mathrm{ResMII} = \max_r \lceil u_r / c_r \rceil$. For a cycle $C$ of the dependence graph, adding the constraints $t(v) + II \cdot d(u, v) \ge t(u) + \delta(u, v)$ around it gives $II \cdot d(C) \ge \delta(C)$, so $II \ge \mathrm{RecMII} = \max_C \lceil \delta(C) / d(C) \rceil$. A cycle with $d(C) = 0$ is an error in the input: it would ask an operation to wait for itself.

**Placement (line L4).** A schedule $t$ is legal for $II$ when every edge has $t(v) + II \cdot d(u, v) \ge t(u) + \delta(u, v)$, and, for each class $r$ and each slot $k$ from 0 to $II - 1$, at most $c_r$ operations of class $r$ have $t(v) \bmod II = k$. The table of these slots is the *modulo reservation table*. These two conditions are exactly what makes the overlapped run legal. For an edge, operation $v$ of iteration $i + d$ runs at $(i + d) II + t(v) \ge i \cdot II + t(u) + \delta$. For a resource, the operations of class $r$ that run in cycle $c$ come from different operations $v$ with $t(v) \equiv c \pmod{II}$, at most one iteration each. The search for such a $t$ with a small $II$ is NP-hard in general, so line L4 is a heuristic, and line L5 tries the next $II$ when it fails.

**Stages and code (lines L7 to L9).** Operation $v$ belongs to stage $\mathrm{stage}(v)$. In pass $p$ of the kernel, slot $k$ runs each $v$ with $t(v) \bmod II = k$ for iteration $p - \mathrm{stage}(v)$. The prologue is the first $SC - 1$ passes, where some of these iterations do not exist yet, and the epilogue is the last $SC - 1$, where some are already past the end. With $N$ iterations the whole run takes $(N + SC - 1)$ passes, about $N \cdot II$ cycles for large $N$ instead of $N$ times the length of one iteration.

**Registers (line L8).** A value written once per iteration is written again every $II$ cycles. If it must live longer than that, one register is not enough. *Modulo variable expansion* (Lam 1988) unrolls the kernel and gives each copy its own name. Rotating registers do the renaming in hardware.

## Classic examples

**A small loop, worked.** The body computes `x = a[i]` (memory, latency 2), `y = x * c` (multiply, latency 3), `z = y + x` (ALU, latency 1) and `b[i] = z` (memory, latency 1), on a machine with one unit of each class. The loop control is left out. Two memory operations on one memory unit give $\mathrm{ResMII} = 2$. No dependence crosses an iteration, so $\mathrm{RecMII}$ does not limit $II$, and $II = 2$. A legal schedule and its table:

| operation | $t$ | slot $t \bmod 2$ | stage |
|---|---|---|---|
| `x = a[i]` | 0 | 0 | 0 |
| `y = x * c` | 2 | 0 | 1 |
| `z = y + x` | 5 | 1 | 2 |
| `b[i] = z` | 7 | 1 | 3 |

The store cannot go at cycle 6, its earliest start, because slot 0 of the memory unit holds the load. So $SC = 4$. The kernel runs, in slot 0, the load of iteration $p$ and the multiply of iteration $p - 1$, and in slot 1, the add of iteration $p - 2$ and the store of iteration $p - 3$. For $N = 100$ the run has 103 passes, 6 cycles of prologue, 97 kernel passes and an epilogue, and takes $2 \cdot 103 = 206$ cycles. Without overlap one iteration takes 7 cycles, so 700. The value `x` is written at cycle 2 of its iteration and read last at cycle 5, but the next load writes it again at cycle 4. So `x` needs two names, and the kernel is unrolled twice. The values `y` and `z` are read before the next write and need one name each.

**[Loop unrolling](/loop-unrolling/).** Unrolling $k$ times and scheduling the larger body overlaps $k$ iterations, but the overlap stops at each back edge. Software pipelining keeps the overlap across all iterations with a kernel of $II$ cycles. Unrolling is still used inside it, for modulo variable expansion and when the best $II$ is a fraction.

**[Iterative modulo scheduling](/iterative-modulo-scheduling/).** Rau's algorithm fills line L4: it places operations by height, one at a time, into the modulo reservation table, and moves earlier ones out when there is no free slot, within a budget of steps.

**[SDC-based modulo scheduling](/sdc-modulo-scheduling/).** In high-level synthesis, loop pipelining is the same technique for hardware: the dependence rows $t(v) - t(u) \ge \delta - II \cdot d$ form a system of difference constraints, and the modulo slots are added one operation at a time.

**[Iteration bound](/iteration-bound/), [retiming](/retiming/) and [unfolding](/dsp-unfolding/).** For a digital filter on unlimited hardware, the iteration bound is $\mathrm{RecMII}$ without the ceiling. Retiming moves the registers of a circuit, which is the same as changing the stages of its operations. Unfolding runs several iterations as one, which reaches a bound that is a fraction.

## Variations

- **Modulo scheduling algorithms.** Lam (1988) schedules strongly connected components first and reduces conditionals to single nodes. Iterative modulo scheduling (Rau 1994) uses heights and displacement. Swing modulo scheduling (Llosa et al. 1996) orders operations to keep lifetimes short and is the pipeliner of GCC. Integer programming gives optimal schedules for small loops.
- **Kernel recognition.** Instead of fixing $II$ first, unroll the loop, schedule it greedily, and wait for a pattern that repeats. Allan et al. (1995) survey these methods.
- **Hardware support.** Rotating registers rename each value once per kernel pass, and stage predicates turn the stages of the prologue and the epilogue off, so the kernel alone runs the loop. The Cydra 5 and the IA-64 processors had both.
- **Loops with branches.** If-conversion turns the body into predicated straight-line code. Hierarchical reduction (Lam 1988) schedules each branch arm first and treats the result as one operation with a union of resources.
- **Fractional rates.** If the best rate is $5/2$ cycles per iteration, unroll the body twice and pipeline it with $II = 5$.

## Pitfalls

- **Missing a loop-carried dependence.** If line L1 keeps only the dependences inside one iteration, a sum `s = s + y` can read `s` before the previous iteration writes it. Every edge needs its distance, also through memory, as in `a[i] = a[i - 1] * c`.
- **Values that live longer than $II$.** If line L8 keeps one register per value, the next iteration overwrites the value before its last read, as with `x` in the example. Expand the variable or use rotating registers.
- **Short trip counts.** The prologue and the epilogue assume at least $SC - 1$ iterations. Without line L10, a loop with fewer iterations runs operations of iterations that do not exist.
- **The wrong rounding in the bounds.** $\mathrm{ResMII}$ and $\mathrm{RecMII}$ round up. Rounding down gives an $II$ that no schedule can meet, and with a heuristic that does not check, a schedule with conflicts.
- **Register pressure.** A small $II$ with many stages keeps many values live at once. If the machine runs out of registers, the spill code can cost more than the overlap gains. A larger $II$, or a scheduler that keeps lifetimes short, can be faster.

## Exercises

1. A loop computes `x = a[i]` (memory, latency 2) and `s = s * x` (multiply, latency 3), with one memory unit and one multiplier. Find $\mathrm{ResMII}$, $\mathrm{RecMII}$ and the least $II$. (Answer: 1, 3 and 3.)
2. Prove that $II \ge \lceil \delta(C) / d(C) \rceil$ for every cycle $C$ of the dependence graph, from the edge constraints of line L4.
3. A value is written at cycle $w$ of its iteration and read last at cycle $l \ge w$. A write is seen by reads in the same cycle. Show that it needs $\lfloor (l - w) / II \rfloor + 1$ names in rotation, and check the count for `x`, `y` and `z` in the example.
4. In the example, show that no legal schedule with $II = 2$ and the load at cycle 0 puts the store before cycle 7.

## References
