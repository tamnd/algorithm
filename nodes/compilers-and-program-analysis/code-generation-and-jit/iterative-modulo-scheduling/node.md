---
tag: PJN90C
kind: algorithm
slug: iterative-modulo-scheduling
name: Iterative modulo scheduling
aliases:
- Rau modulo scheduling
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Software pipelines a loop by trying initiation intervals from a lower bound up, placing operations in a modulo reservation table with backtracking.
solves: [instruction-scheduling-problem]
model: word-ram
complexity:
  vars: {n: the number of operations, e: the number of dependence edges, D: the sum of the positive delays, w: the length of the longest reservation table, B: the budget ratio, I: the number of values of II tried, P: the largest II tried}
  time: {worst: O(n^3 log D + I (n e + B n (n + e + P w)))}
  space: {extra: O(n^2 + e + n w)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1994
  people: [B. Ramakrishna Rau]
  note: Rau gave the algorithm at MICRO-27 in 1994 and in a long journal version in 1996, after work on modulo scheduling since 1981 and on the compiler of the Cydra 5.
prereqs: [software-pipelining, instruction-scheduling-problem, list-scheduling, loop-carried-dependence, floyd-warshall]
see_also: [sdc-modulo-scheduling, trace-scheduling, superblock-scheduling, iteration-bound, karp-minimum-mean-cycle, difference-constraints, ilp-scheduling-formulation, loop-unrolling]
sources:
  - paper: doi:10.1145/192724.192731
    title: B. Ramakrishna Rau, Iterative modulo scheduling, an algorithm for software pipelining loops, Proceedings of the 27th Annual International Symposium on Microarchitecture, 1994, 63-74
    locator: the bounds ResMII and RecMII with the MinDist matrix, the priority HeightR, and the procedures IterativeSchedule and FindTimeSlot with the earliest start Estart and a budget of BudgetRatio times the number of operations
  - paper: doi:10.1007/BF03356742
    title: B. Ramakrishna Rau, Iterative modulo scheduling, International Journal of Parallel Programming 24(1), 1996, 3-64
    locator: the journal version of the algorithm with its measurements
  - paper: doi:10.1145/53990.54022
    title: Monica Lam, Software pipelining, an effective scheduling technique for VLIW machines, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation, 1988, 318-328
    locator: modulo scheduling with lower bounds from resources and recurrences, the scheduling of strongly connected components first, and modulo variable expansion
  - paper: doi:10.1145/155090.155115
    title: Richard A. Huff, Lifetime-sensitive modulo scheduling, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation, 1993, 258-267
    locator: MinDist as all-pairs longest paths with arc costs of latency minus distance times II, and slack scheduling that places operations early or late to keep lifetimes short
  - paper: doi:10.1109/pact.1996.554030
    title: Josep Llosa, Antonio González, Eduard Ayguadé and Mateo Valero, Swing modulo scheduling, a lifetime-sensitive approach, Proceedings of the Conference on Parallel Architectures and Compilation Techniques, 1996, 80-86
    locator: the order of the operations by recurrences and the placement of each operation next to its scheduled neighbors
  - paper: doi:10.1145/212094.212131
    title: Vicki H. Allan, Reese B. Jones, Randall M. Lee and Stephen J. Allan, Software pipelining, ACM Computing Surveys 27(3), 1995, 367-432
    locator: the survey of modulo scheduling methods, with iterative modulo scheduling among them
---

Iterative modulo scheduling is an algorithm for the central step of [software pipelining](/software-pipelining/): it chooses a start time $t(v)$ for each operation of a loop body so that a new iteration can start every $II$ cycles. Software pipelining is the general technique, with its prologue, kernel, epilogue and register renaming. This page is only about the choice of $t$ and $II$, as Rau (1994) gave it. It starts at the lower bound $\mathrm{MII} = \max(\mathrm{ResMII}, \mathrm{RecMII})$ and tries each $II$ in turn. For one $II$, it places the operations one at a time, by priority, into a *modulo reservation table* with $II$ rows. When an operation finds no free row in its window, it takes a slot anyway and pushes out the operations that are in the way. These are placed again later, and a budget limits the number of steps. The result is always legal. It is not always the least $II$, but on most loops it is equal to MII.

## In plain words

Picture a loop that starts a new pass every few clock ticks. Each pass must do the same steps at the same offsets, so every step has a fixed seat in a short repeating table, one row per tick. Two steps that need the same unit cannot sit in the same row. The method seats the most urgent steps first. If a step finds every seat it could take already full, it sits down anyway and makes the others stand up and look for new seats. After too many moves it gives up and tries again with a longer table, which has more seats. The first table length that works gives the speed of the loop.

## The problem

The input is a loop body with operations $0, \dots, n - 1$ and a machine. Each operation $v$ has a *reservation table*, a list of pairs $(r, o)$: in each iteration, $v$ uses one unit of resource $r$ in cycle $t(v) + o$. Resource $r$ has $c_r$ units. Each dependence edge $(u, v)$ has a delay $\delta(u, v)$ and a distance $d(u, v) \ge 0$: operation $v$ of iteration $i + d$ starts at least $\delta$ cycles after operation $u$ of iteration $i$. Edges with distance 0 form no cycle, as described on the [loop-carried dependence](/loop-carried-dependence/) page.

The output is an $II \ge 1$ and starts $t(v) \ge 0$ that form a *legal modulo schedule*:

- every edge has $t(v) + II \cdot d(u, v) \ge t(u) + \delta(u, v)$;
- for each resource $r$ and each slot $k \in \{0, \dots, II - 1\}$, at most $c_r$ table entries of $r$ fall in cycles $t(v) + o \equiv k \pmod{II}$.

Then iteration $i$ can start at cycle $i \cdot II$, and the overlapped run keeps every dependence and every unit limit. The goal is a small $II$. Finding the least one is NP-hard in general, so the algorithm is a heuristic.

## The algorithm

```pseudo id=main
ITERATIVE-MODULO-SCHEDULE(G, machine, ratio)
L1  MII <- max(1, ResMII, RecMII)
L2  for II <- MII, MII + 1, ... do
L3      if ITERATIVE-SCHEDULE(II, ratio * n) returns t then return (II, t)

ITERATIVE-SCHEDULE(II, budget)
L4  if some operation alone overfills the table then fail; H <- HeightR at II; t, MRT <- empty
L5  while some operation is unscheduled and budget > 0 do
L6      v <- the unscheduled operation of greatest H(v), the lowest index on ties
L7      Estart <- max(0, max over scheduled predecessors p of t(p) + delta(p, v) - II * d(p, v))
L8      s <- the first time in Estart .. Estart + II - 1 at which v fits in the MRT
L9      if there is none then s <- Estart if v was never scheduled or Estart > prev(v), else prev(v) + 1
L10         unschedule the operations that hold the slots that v needs at s, until v fits
L11     unschedule each scheduled successor w of v with t(w) < s + delta(v, w) - II * d(v, w)
L12     t(v) <- s; prev(v) <- s; put v in the MRT; budget <- budget - 1
L13 if all operations are scheduled then return t else fail
```

**The bounds (line L1).** If the tables hold $u_r$ entries of resource $r$, then $\mathrm{ResMII} = \max_r \lceil u_r / c_r \rceil$. For RecMII, give each edge the weight $\delta - II \cdot d$. A cycle $C$ of weight $\delta(C) - II \cdot d(C) > 0$ makes $II$ impossible, so $\mathrm{RecMII}$ is the least $II \ge 0$ with no positive cycle, that is $\max_C \lceil \delta(C) / d(C) \rceil$. Rau finds it with the *MinDist* matrix, the all-pairs longest path weights, which [Floyd-Warshall](/floyd-warshall/) computes in $O(n^3)$. A positive cycle shows up as a positive diagonal entry. The weights only shrink as $II$ grows, so a binary search over $II$ from 0 to the sum $D$ of the positive delays finds RecMII.

**Priority (line L4).** $\mathrm{HeightR}(v)$ is the longest weight of a path from $v$, and at least 0. It measures how far the rest of the iteration reaches beyond $v$, counted at this $II$. With no positive cycle, Bellman-Ford rounds reach it. The check before it rejects an $II$ at which some operation alone uses one row of the table too often, such as a divide that holds the multiplier at offsets 0 and 2 when $II = 2$.

**One step (lines L6 to L12).** The *earliest start* of line L7 uses only the predecessors that are scheduled now. The window of line L8 has $II$ times, so it tries every row of the table once. If all rows are full, line L9 forces a time. The rule with $\mathrm{prev}(v)$ makes an operation that comes back to the same $\mathrm{Estart}$ move one cycle later each time, so that it does not push out the same operations again and again. Line L10 makes room in the table. Line L11 pushes out the successors whose dependence on $v$ the new time breaks. Predecessors cannot break, since $s \ge \mathrm{Estart}$.

**The budget (line L5).** Each step costs one unit, and the budget is ratio times $n$. When it runs out, the attempt fails and line L2 tries $II + 1$. Rau chose the ratio by measurement. The code uses 3.

## Example

The loop computes `acc = acc * c + x[i] * y[i]` and steps `i`. The machine has one memory unit, one multiplier and one ALU, each pipelined, so each table is one entry at offset 0.

| index | name | operation | resource | edges out (delay, distance) |
|---|---|---|---|---|
| 0 | `lx` | `x = load x[i]` | mem | to `m2` (2, 0), to `inc` (0, 0) |
| 1 | `ly` | `y = load y[i]` | mem | to `m2` (2, 0), to `inc` (0, 0) |
| 2 | `m1` | `p = acc * c` | mul | to `a` (2, 0) |
| 3 | `m2` | `q = x * y` | mul | to `a` (2, 0) |
| 4 | `a` | `acc = p + q` | alu | to `m1` (1, 1) |
| 5 | `inc` | `i = i + 1` | alu | to `lx` (1, 1), to `ly` (1, 1), to itself (1, 1) |

The edges into `inc` with delay 0 keep the loads before the write of `i`. Two operations use each resource, so $\mathrm{ResMII} = 2$. The cycle `m1`, `a` has delay $2 + 1 = 3$ and distance 1, so $\mathrm{RecMII} = 3$, and at $II = 2$ Floyd-Warshall finds a positive diagonal. So $\mathrm{MII} = 3$. At $II = 3$ the heights are 4 for `lx` and `ly`, 2 for `m1`, `m2` and `inc`, and 0 for `a`. The budget is $3 \cdot 6 = 18$ steps. The steps are:

| step | op | Estart | first free time in the window | time | pushed out | why |
|---|---|---|---|---|---|---|
| 1 | `lx` | 0 | 0 | 0 | none | |
| 2 | `ly` | 0 | 1 | 1 | none | memory row 0 is full |
| 3 | `m1` | 0 | 0 | 0 | none | |
| 4 | `m2` | 3 | 4 | 4 | none | multiplier row 0 holds `m1` |
| 5 | `inc` | 1 | 1 | 1 | none | |
| 6 | `a` | 6 | 6 | 6 | `m1` | `m1` at 0 breaks $t(m_1) + 3 \ge t(a) + 1$ |
| 7 | `m1` | 4 | 5 | 5 | `a` | `a` at 6 breaks $t(a) \ge t(m_1) + 2$ |
| 8 | `a` | 7 | 8 | 8 | `m1` | `m1` at 5 breaks $t(m_1) + 3 \ge 9$ |
| 9 | `m1` | 6 | 6 | 6 | none | |

Line L11 does all the pushing here: each time `a` or `m1` moves, the recurrence moves the other one. After 9 steps every operation is placed, with $II = 3 = \mathrm{MII}$, so the result is optimal. The modulo reservation table is:

| row | mem | mul | alu |
|---|---|---|---|
| 0 | `lx` (0) | `m1` (6) | |
| 1 | `ly` (1) | `m2` (4) | `inc` (1) |
| 2 | | | `a` (8) |

One iteration spans cycles 0 to 8, in three stages of three cycles. For 100 iterations the pipelined loop takes $99 \cdot 3 + 9 = 306$ cycles. Without overlap, the best schedule of one iteration takes 6 cycles (`lx` and `m1` at 0, `ly` and `inc` at 1, `m2` at 3, `a` at 5), so 600 cycles.

## Correctness

**Theorem.** If ITERATIVE-MODULO-SCHEDULE returns $(II, t)$, then $t$ is a legal modulo schedule for $II$, and $\mathrm{MII} \le II^* \le II$, where $II^*$ is the least $II$ of any legal modulo schedule.

The full proof is in the proof file. The lower bound comes from two sums. Each resource has $c_r$ units in each of $II$ rows, so $u_r \le II \cdot c_r$. Around a cycle the starts cancel, so the edge constraints add up to $II \cdot d(C) \ge \delta(C)$. For the schedule, the key invariant of line L5 is that the scheduled operations already form a legal partial schedule: the table rows are within their limits, and every edge between two scheduled operations holds. Line L7 makes the edges from scheduled predecessors hold, line L10 keeps the table rows within limits, and line L11 removes every successor whose edge would break. Self-loops hold at every $II \ge \mathrm{RecMII}$. So when every operation is scheduled, the schedule is legal. Each attempt stops within its budget.

## Complexity

The model is the word RAM. Let $n$, $e$, $D$, $w$, $B$, $I$ and $P$ be as in the front matter, with a constant number of units per resource.

- **Line L1.** ResMII takes $O(n w)$. The binary search for RecMII runs Floyd-Warshall $O(\log D)$ times, at $O(n^3 + e)$ each.
- **Line L4.** The check takes $O(n w)$, and the heights take at most $n$ rounds over the edges, $O(n e)$.
- **Lines L6 to L12, per step.** Line L6 scans $O(n)$ operations, line L7 and line L11 scan $O(e)$ edges, and line L8 tests at most $II \le P$ times at $O(w)$ each. Every operation that lines L10 and L11 remove was placed by an earlier step, so all removals cost $O(w)$ per step on average.
- **One attempt.** At most $B n$ steps: $O(n e + B n (n + e + P w))$.

So the run costs $O(n^3 \log D + I (n e + B n (n + e + P w)))$ time. The space is $O(n^2)$ for MinDist, $O(e)$ for the edges and $O(n w)$ for the table. The Python code computes the tests of line L8 with dictionaries, which keeps these bounds.

## Properties

- **Always legal.** Every returned schedule meets every dependence with its distance and every row limit of the table.
- **Not exact.** The returned $II$ can be larger than the least one: the budget can run out, and the order of line L6 can block a better choice. The least $II$ can also be larger than MII.
- **Usually optimal in practice.** On 150 random loops of at most 5 operations in the tests, the returned $II$ equalled the exhaustive optimum on all of them, and the optimum was above MII on 3. In a larger run with 300 loops of up to 6 operations, it equalled the optimum on 298. These are measurements on small random loops, not bounds.
- **Deterministic.** The order of line L6, the scan of line L8 and the removal order are fixed.
- **General resources.** A table may use several resources at several offsets, as for a divide that holds a unit for many cycles.
- **Blind to registers.** It does not look at the lifetimes of values, so it can need many registers.

## Variants and improvements

- **Lifetime-sensitive scheduling.** Huff (1993) places each operation early or late inside its slack to keep values short. Swing modulo scheduling (Llosa et al. 1996) orders the operations by recurrences and places each one next to its scheduled neighbors, without backtracking. It is the pipeliner of GCC.
- **No backtracking.** Lam (1988) schedules the strongly connected components first and raises $II$ when an operation finds no slot.
- **Constraint and integer programming.** [SDC-based modulo scheduling](/sdc-modulo-scheduling/) keeps the dependences as a system of [difference constraints](/difference-constraints/), and an [integer program](/ilp-scheduling-formulation/) gives the least $II$ for small loops.
- **Faster RecMII.** The ratio $\max_C \delta(C)/d(C)$ is a minimum cycle ratio problem. With all distances 1 it is a maximum mean cycle, which [Karp's algorithm](/karp-minimum-mean-cycle/) solves in $O(n e)$.

## When to use it

Use it to pipeline inner loops for VLIW, EPIC and DSP processors, where it is a standard method with a simple implementation and schedules close to MII. Prefer swing modulo scheduling when registers are few, since it keeps lifetimes short. Prefer an integer program for small, hot loops where the least $II$ is worth a long compile. In high-level synthesis, [SDC-based modulo scheduling](/sdc-modulo-scheduling/) handles timing rules that are not plain dependences. For code with branches and no loop, use [trace scheduling](/trace-scheduling/) or [superblock scheduling](/superblock-scheduling/).

## Pitfalls

- **Missing the successor check.** If line L11 is left out, the schedule can break a dependence. In the example, step 6 puts `a` at 6 while `m1` stays at 0, and then the next iteration multiplies the old `acc`. Line L11 must push out every scheduled successor whose edge the new time breaks.
- **Forcing the same time again.** If line L9 always takes Estart, an operation that is pushed out and comes back with the same Estart pushes out the same operations, which then push it out again, until the budget is gone. Take $\mathrm{prev}(v) + 1$ when $\mathrm{Estart} \le \mathrm{prev}(v)$.
- **The wrong earliest start.** If line L7 reads the old times of operations that are not scheduled, or leaves out $- II \cdot d$, the start of an operation on a recurrence is too late or too early. Use only the scheduled predecessors, with the weight $\delta - II \cdot d$.
- **No check of a single operation.** If line L4 does not reject an operation that alone overfills a row, line L10 cannot make room for it, even when it empties the table. Reject that $II$ at once.
- **Rounding down.** If line L1 rounds $u_r / c_r$ or $\delta(C)/d(C)$ down, the first attempts run at an $II$ that no schedule can meet. Three loads on two memory ports need $II = 2$, and a cycle with delay 5 and distance 2 needs $II = 3$.
- **A window of the wrong size.** If line L8 tries fewer than $II$ times, it misses free rows. More than $II$ times only repeats rows at later times.

## Implementations

## History

Rau and Glaeser (1981) scheduled one iteration at a fixed interval with resources reserved modulo that interval, for a machine designed to make this easy. Lam (1988) built modulo scheduling into the compiler of the Warp machine, with bounds from resources and recurrences and modulo variable expansion. At Cydrome, Rau and others built the Cydra 5 and its compiler around modulo scheduling with rotating registers. Huff (1993) added slack scheduling to keep lifetimes short. Rau (1994) gave iterative modulo scheduling, with HeightR, the budget and the displacement of operations, and a long journal version in 1996. Llosa and others gave swing modulo scheduling in 1996, and Zhang and Liu carried the modulo reservation table into high-level synthesis in 2013.

## References
