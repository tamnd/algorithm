---
tag: WJY423
kind: algorithm
slug: cyclic-executive
name: Cyclic executive
aliases:
- cyclic scheduler
- timeline scheduling
area: systems/scheduling
level: intro
summary: "Run periodic tasks from a fixed table built before the system starts. Time is cut into equal frames, and the table repeats every hyperperiod."
solves: [real-time-scheduling]
model: word-ram
complexity:
  vars: {n: the number of tasks, h: the hyperperiod, k: the number of jobs in one hyperperiod, m: the number of frames}
  time: {worst: O(n h + k m^k)}
  space: {extra: O(k + m)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1989
  people: [Theodore P. Baker, Alan Shaw]
  note: Cyclic executives were the common structure of avionics and control software in the 1960s and 1970s; Baker and Shaw gave a formal model of them, with frames and the frame constraints, in 1988 and 1989.
prereqs: [periodic-task-model, hyperperiod, bin-packing]
see_also: [time-triggered-scheduling, fixed-priority-scheduling, earliest-deadline-first, hyperperiod, pinwheel-scheduling, least-common-multiple, greatest-common-divisor, strong-np-hardness]
sources:
  - paper: doi:10.1007/BF02341919
    title: "Theodore P. Baker and Alan Shaw, The cyclic executive model and Ada, Real-Time Systems 1(1) (1989), 7-25"
    locator: the model of major and minor cycles and the conditions on the frame size
  - book: isbn:9780130996510
    title: Jane W. S. Liu, Real-Time Systems, Prentice Hall, 2000
    locator: Chapter 5 (clock-driven scheduling), the frame size constraints and the splitting of jobs
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 4 (periodic task scheduling), timeline scheduling
---

A cyclic executive runs a set of [periodic tasks](/periodic-task-model/) from a table that is built before the system starts. Time is cut into frames of one fixed length $f$, and a timer starts each frame; in each frame the executive calls a fixed list of jobs, one after the other, and the table repeats every [hyperperiod](/hyperperiod/). Nothing is decided while the system runs, so the schedule can be checked by hand and its timing is exactly known. The hard part is offline: choose $f$ and fill the table, a search that contains [bin packing](/bin-packing/) and is [strongly NP-hard](/strong-np-hardness/).

## In plain words

A school timetable is made once, before the term. The week is cut into periods of one hour. Each class is in one fixed period, and the same timetable repeats each week. Nobody decides anything during the day. A bell rings at the start of each period, and everyone goes to the room on the list.

A cyclic executive does the same for a computer. The program is a list of slots of equal length. A timer rings at the start of each slot, and the computer runs the jobs listed for that slot. The work is all in making the list: each job must fit in a slot, the slot must come after the job is ready, and it must end before the job is due.

## The problem

The input is $n$ periodic tasks. Task $\tau_i$ has an integer period $T_i$, a worst-case execution time $C_i$ and an integer relative deadline $D_i$, and all tasks release their first job at time 0. The hyperperiod is $H = \operatorname{lcm}(T_1, \ldots, T_n)$, the [least common multiple](/least-common-multiple/) of the periods. The output is a frame size $f$ that divides $H$, and a table that puts each job of $[0, H)$ in one frame that lies inside the window from its release to its deadline, with a total cost of at most $f$ per frame. The test is the construction itself: it is exact for tables of this form, because it answers yes exactly when such a table exists.

## The algorithm

Liu states three conditions on the frame size. A frame must hold a whole job, so $f \ge \max_i C_i$. The frames should line up with the major cycle, so $f$ divides some $T_i$. Each job must see a whole frame between its release and its deadline, which holds for all jobs of $\tau_i$ exactly when $2f - \gcd(T_i, f) \le D_i$.

```pseudo id=main
CYCLIC-EXECUTIVE-PLAN(τ1, ..., τn)
L1  H ← lcm(T1, ..., Tn)
L2  for each f that divides H, in increasing order do
L3      if f < max Ci then skip f
L4      if no Ti is a multiple of f then skip f
L5      if 2f − gcd(Ti, f) > Di for some i then skip f
L6      J ← the jobs of [0, H): job k of τi has window [k Ti, k Ti + Di]
L7      table ← ASSIGN(J, f, H / f)          ▷ depth-first search, one frame per job
L8      if a table was found then return (f, table)
L9  return none
```

ASSIGN takes the jobs in order of deadline and puts each one in the first frame inside its window that still has room. When a job fits nowhere, it goes back and moves the previous job to its next frame. The executive that runs the table is a short loop: wait for the timer of frame $m$, run the jobs of row $m \bmod (H/f)$, and go back to wait. The frame timer also gives a simple check: if the jobs of a frame are not done when the next frame starts, an overrun has occurred.

## Example

Take $\tau_1 = (T, C, D) = (4, 1, 4)$, $\tau_2 = (5, 1.8, 5)$, $\tau_3 = (20, 1, 20)$ and $\tau_4 = (20, 2, 20)$. Then $H = 20$ and the utilization is $0.25 + 0.36 + 0.05 + 0.1 = 0.76$. Line L3 needs $f \ge 2$. For $f = 4$, line L5 fails for $\tau_2$: $2 \cdot 4 - \gcd(5, 4) = 7 > 5$. For $f = 5$ and $f = 10$ it fails for $\tau_1$. So $f = 2$ is the only frame size, with 10 frames.

| frame start | 0 | 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|
| jobs | $\tau_1$, $\tau_3$ | $\tau_2$ | $\tau_1$ | $\tau_2$ | $\tau_1$ | $\tau_2$ | $\tau_1$ | $\tau_4$ | $\tau_2$ | $\tau_1$ |
| load | 2 | 1.8 | 1 | 1.8 | 1 | 1.8 | 1 | 2 | 1.8 | 1 |

Each job sits in a frame inside its window. For example, the job of $\tau_2$ released at 15 runs in the frame $[16, 18]$ before its deadline 20, and the job of $\tau_1$ released at 16 runs in $[18, 20]$.

**When no frame exists.** For $(4, 1, 4)$, $(5, 2, 7)$ and $(20, 5, 20)$, line L3 needs $f \ge 5$, and line L5 fails for each of 5, 10 and 20. The fix is to split the long job: cut $\tau_3$ into three parts of cost 1, 3 and 1 with the same window. Then $f = 4$ passes all three tests, and ASSIGN puts the three parts in the frames that start at 0, 4 and 8.

## Correctness

A table gives a correct schedule: the jobs of a frame start at or after its start, which is at or after their release, and end before its end, which is at or before their deadline, since the load is at most $f$. Line L5 is exact by a short argument on residues. The first frame boundary after the release $kT_i$ is $(-kT_i) \bmod f$ later, and over the jobs of $[0, H)$ this delay takes every multiple of $g = \gcd(T_i, f)$ from 0 to $f - g$. So the worst job has a whole frame exactly when $(f - g) + f \le D_i$. ASSIGN is a complete depth-first search that cuts a branch only when a frame is over its limit, so it finds a table whenever one exists. The full proof is in the proofs folder.

## Complexity

- **Frame sizes.** Lines L1 to L5 test at most $h$ values of $f$ with $O(n)$ work each, so $O(n h)$ time, where the numbers $T_i$ have fixed size.
- **The table.** ASSIGN may try all ways to put $k$ jobs in $m$ frames, so it takes $O(k \cdot m^k)$ time in the worst case. This is unavoidable in general: if every job may go in every frame, the problem is bin packing with $m$ bins of size $f$, which is strongly NP-hard. Real tables are built with heuristics, with network flow when jobs may be split at frame boundaries, or with a solver.
- **At run time.** Each frame costs one timer interrupt and a walk over a list. The table has $k$ entries, and $h$ grows with the [least common multiple](/least-common-multiple/) of the periods, which can be very large for periods that share few factors.

## Properties

- **Fully predictable.** The order of jobs is fixed, so the worst-case response time of each job can be read from the table.
- **No preemption, no locks.** Jobs in one frame run to the end one after the other. Two jobs that share data never overlap, so no lock is needed, and there is no [priority inversion](/priority-inversion/).
- **Low overhead.** The executive is a loop and a timer. It has no ready queue and no context switch inside a frame.
- **Brittle.** A change to one task can force a new table for all of them. A long job must be split by hand into parts, and the parts need the right order.
- **Wasteful for sporadic work.** Rare events need a slot in each frame where they might occur, or a slack-stealing scheme.

## Variants and improvements

- **Job splitting.** Cut a long job into parts that fit the frames, as in the example. With splitting allowed at any point, the table is a network flow problem, which is polynomial.
- **Slack stealing.** Run aperiodic jobs in the idle time of the frames, as long as the table can still finish each frame on time.
- **Time-triggered systems.** [Time-triggered scheduling](/time-triggered-scheduling/) extends the static table to many nodes that share a global clock and a network.
- **Pinwheel schedules.** For unit jobs that must recur within a fixed gap, the table is a [pinwheel schedule](/pinwheel-scheduling/).
- **Priority-driven rules.** [Fixed-priority scheduling](/fixed-priority-scheduling/) and [earliest deadline first](/earliest-deadline-first/) decide online and handle changes and sporadic tasks better.

## When to use it

Use a cyclic executive for a small, closed set of periodic tasks whose periods have many common factors, when certification needs a schedule that can be read and checked line by line, as in flight control and engine control. It also suits small processors with no operating system. If tasks change often, if many events are sporadic, or if the periods give a very long hyperperiod, a priority-driven scheduler is a better choice.

## Pitfalls

- **Skipping the window test.** A frame size that passes lines L3 and L4 can still let a job be released just after a frame starts and be due before the next frame ends. Line L5 catches this; a check of only $f \le D_i$ does not.
- **Using the wrong gcd.** Line L5 needs $\gcd(T_i, f)$, not $\gcd$ of all periods. With the wrong value, the test accepts a frame that has no room for some job.
- **Order of split parts.** ASSIGN does not know that the parts of a split job must run in order. In the example they do, but a builder must add this as a constraint.
- **Overrun.** If a job runs longer than its $C_i$, the frame overruns and every later job moves. The frame timer of the run-time loop must detect it and take an action.

## Implementations

## History

Cyclic executives were the usual structure of real-time software in avionics and process control before priority-driven kernels were common, and the frame conditions were part of engineering practice. Baker and Shaw gave a formal model of the cyclic executive, with major and minor cycles and the constraints on the frame size, at the Real-Time Systems Symposium in 1988 and in the journal Real-Time Systems in 1989. Liu's textbook of 2000 gives the three frame constraints in the form used here.

## References
