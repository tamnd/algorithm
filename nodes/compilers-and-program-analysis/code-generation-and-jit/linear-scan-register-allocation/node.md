---
tag: 5E24WB
kind: algorithm
slug: linear-scan-register-allocation
name: Linear scan register allocation
aliases:
- Poletto-Sarkar linear scan
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Sorts live intervals by start and assigns registers in one pass, spilling the interval that ends last when registers run out.
solves: [register-allocation-problem]
model: word-ram
complexity:
  vars: {n: the number of names, s: the number of instructions and terminators, k: the number of registers, l: the time of one liveness analysis}
  time: {worst: O(l + s n + n log n)}
  space: {extra: O(s n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1999
  people: [Massimiliano Poletto, Vivek Sarkar]
  note: First used in the tcc dynamic code generator of Poletto, Engler and Kaashoek in 1997; the 1999 paper compared it with graph coloring.
prereqs: [register-allocation-problem, live-variable-analysis, interference-graph, interval-partitioning-greedy]
see_also: [chaitin-register-allocation, ssa-linear-scan, ssa-based-register-allocation, local-register-allocation, k-colorable-interval-subgraph, k-machine-interval-scheduling, live-range-splitting, just-in-time-compilation]
sources:
  - paper: doi:10.1145/330249.330250
    title: Massimiliano Poletto and Vivek Sarkar, Linear scan register allocation, ACM Transactions on Programming Languages and Systems 21(5), 1999, 895-913
    locator: the live intervals in a linear order, the scan with the routines EXPIRE-OLD-INTERVALS and SPILL-AT-INTERVAL, the rule that spills the interval that ends furthest away, and the comparison with graph coloring on compile time and code quality
  - paper: doi:10.1145/258915.258926
    title: Massimiliano Poletto, Dawson R. Engler and M. Frans Kaashoek, tcc, a system for fast, flexible, and high-level dynamic code generation, PLDI 1997, 109-121
    locator: the fast register allocator of the tcc dynamic compiler, the first use of linear scan
  - paper: doi:10.1145/277650.277714
    title: Omri Traub, Glenn Holloway and Michael D. Smith, Quality and speed in linear-scan register allocation, PLDI 1998, 142-151
    locator: second-chance binpacking, lifetime holes, the split of a lifetime at a spill, and the resolution moves on the edges of the control flow graph
  - paper: doi:10.1145/1064979.1064998
    title: Christian Wimmer and Hanspeter Mössenböck, Optimized interval splitting in a linear scan register allocator, VEE 2005, 132-141
    locator: lifetime intervals with holes, use positions, the split of an interval at an optimal position, fixed intervals for machine registers, and the use in the Java HotSpot client compiler
---

Linear scan register allocation gives registers to the names of a program without building an [interference graph](/interference-graph/). It puts the instructions in one linear order, replaces each name by one interval from its first to its last live position, and visits the intervals by start. A free register goes to each new interval. When none is free, it spills the interval that ends last, which may be the new one. It runs in near-linear time, so JIT compilers use it, but it is a heuristic for the [register allocation problem](/register-allocation-problem/): an interval can contain points where its name is dead, and then it spills where a [graph coloring allocator](/chaitin-register-allocation/) would not.

## In plain words

Lay the whole function out as one long line of instructions. For each value, draw a bar from the first place it is needed to the last. Now walk along the line from left to right. When a bar starts, give it a free register. When a bar ends, its register becomes free again. If a bar starts and every register is busy, look at all the bars that cover this place, the new one included. Throw out the one that goes on the longest, and keep its value in memory. That choice frees a register for the longest time, and for bars on a line it is the best choice. The bars are rough, though: a bar can cover a branch where its value is never used, so the method can waste registers there.

## The problem

The input is a program $P$ in the toy IR with `const`, `copy` and `op` instructions and no phi, and a number $k \ge 1$ of registers. The output is a program $P'$ that uses only the registers $r_0, \ldots, r_{k-1}$, two scratch registers $s_0$ and $s_1$ kept apart for spill code, and memory slots `mem.x`, and that has the same outcome as $P$ on every input.

Number the instructions and terminators of $P$ in the order of the blocks as items $0, 1, \ldots$. Item $n$ reads at position $2n$ and writes at position $2n+1$, so a value read for the last time by an item can give its register to the value that the same item writes. The *interval* of a name $x$ is the range from the first to the last position where $x$ is written or live before an item. The *overlap* of a set of intervals is the largest number of them that contain one position.

## The algorithm

```pseudo id=main
LINEAR-SCAN-ALLOCATE(P, k)
L1  number the items of P in block order; item n reads at 2n and writes at 2n+1
L2  compute the names live just before each item
L3  I[x] <- [smallest, largest] of the write positions of x and the positions 2n with x live before item n
L4  active <- empty                                        // sorted by end
L5  free <- {0, ..., k-1}
L6  for each interval i in order of increasing start do
L7    EXPIRE-OLD(i)
L8    if |active| = k then SPILL-AT(i)
L9    else reg[i] <- the lowest register in free; remove it from free; add i to active

EXPIRE-OLD(i)
L10 for each j in active, in order of increasing end do
L11   if end[j] >= start[i] then return
L12   remove j from active; add reg[j] to free

SPILL-AT(i)
L13 s <- the interval in active with the largest end
L14 if end[s] > end[i] then reg[i] <- reg[s]; spill s; remove s from active; add i to active
L15 else spill i
L16 return P with each kept name x renamed to r[reg[x]], each spilled name x kept in mem.x
           (loaded into s0 or s1 before a use, computed into s0 and stored after a definition),
           and each copy whose two sides get the same location deleted
```

Ties at line L6 go by end, then by name. Line L13 takes the largest end, then the largest start, then the last name, and line L14 keeps $i$ only if $s$ comes strictly later in that order. The implementation first adds a block that loads each parameter from its slot, as the [Chaitin allocator](/chaitin-register-allocation/) does, so that a parameter has a definition.

Lines L6 to L15 are the [interval partitioning greedy](/interval-partitioning-greedy/) with a cap of $k$ colors. The spill rule of line L13 is the furthest end rule, the same rule as Belady's cache replacement, applied to intervals.

## Example

Take this program with the parameter `p` and $k = 2$:

```
entry:
  a = p + 1
  br p B1 B2
B1:
  b = p * 2
  c = b + p
  ret c
B2:
  d = a - p
  ret d
```

The items are numbered 0 to 6 in block order: `a = p + 1` is 0, the branch is 1, `b`, `c` and `ret c` are 2 to 4, and `d` and `ret d` are 5 and 6. The names live before each item are $\{p\}$, $\{p, a\}$, $\{p\}$, $\{p, b\}$, $\{c\}$, $\{p, a\}$ and $\{d\}$. So the intervals are:

| name | written at | live at | interval |
|---|---|---|---|
| $p$ | none | 0, 2, 4, 6, 10 | $[0, 10]$ |
| $a$ | 1 | 2, 10 | $[1, 10]$ |
| $b$ | 5 | 6 | $[5, 6]$ |
| $c$ | 7 | 8 | $[7, 8]$ |
| $d$ | 11 | 12 | $[11, 12]$ |

The value $a$ is dead in `B1`, but `B1` lies between the definition of $a$ and its use in `B2`, so the interval of $a$ covers `B1`. Position 5 lies in the intervals of $p$, $a$ and $b$, so the overlap is 3. The scan goes:

| interval | expired | action | active after |
|---|---|---|---|
| $p\ [0, 10]$ | none | $p \to r_0$ | $p$ |
| $a\ [1, 10]$ | none | $a \to r_1$ | $p, a$ |
| $b\ [5, 6]$ | none | full; $s = a$ (end 10, start 1), $10 > 6$: spill $a$, $b \to r_1$ | $b, p$ |
| $c\ [7, 8]$ | $b$ | $c \to r_1$ | $c, p$ |
| $d\ [11, 12]$ | $c$, $p$ | $d \to r_0$ | $d$ |

The implementation adds the block `start` with `p = mem.p`, which moves the other positions by 4, and gives:

```
start:
  r0 = mem.p
  jump entry
entry:
  s0 = r0 + 1
  mem.a = s0
  br r0 B1 B2
B1:
  r1 = r0 * 2
  r1 = r1 + r0
  ret r1
B2:
  s0 = mem.a
  r0 = s0 - r0
  ret r0
```

The interference graph has only the edges $p$-$a$ and $p$-$b$. Two colors suffice ($p \to r_0$, $a$ and $b \to r_1$), so a graph coloring allocator needs no spill here. Linear scan spilled $a$ only because its interval covers `B1`. With the blocks in the order `entry`, `B2`, `B1`, the interval of $a$ ends before $b$ starts, the overlap is 2, and linear scan spills nothing. The block order matters.

## Correctness

The full proof is in the proof file. Its parts are:

- **Intervals contain interference.** If two names are live before the same item, or one is written while the other is live after the write, their intervals share a position. So the overlap graph of the intervals contains the interference graph.
- **Registers.** An invariant on *active* shows that two kept intervals that overlap get different registers, and that at most $k$ kept intervals contain any position.
- **No spill and few registers.** The scan spills nothing if and only if the overlap is at most $k$. Then it uses exactly as many registers as the overlap, since the lowest free register is always below the number of intervals that contain the current start.
- **Fewest spills.** For each prefix of the intervals, the kept set has at least as many intervals that end before any time $t$ as any other set with overlap at most $k$. With $t = \infty$ this says the scan keeps the most intervals. The proof uses only that line L13 drops an interval with the largest end.
- **Same outcome.** At each point of a run, each live name that has a value is held by its register or its slot. A write goes to a register that no other live name holds, because of the first two parts.

So linear scan is optimal for its intervals, both in registers and in spills, and correct for the program. It is still a heuristic, because the intervals are larger than the live ranges: the example spills a program that two registers can hold.

## Complexity

With $n$ names, $s$ items, $k$ registers and $l$ the time of [live variable analysis](/live-variable-analysis/):

- **Intervals.** One backward walk per block gives the live set before each item, in $O(s n)$ time and space. Each interval then needs only its smallest and largest position.
- **Scan.** Sorting by start takes $O(n \log n)$. With *active* in a balanced search tree keyed by end, each step costs $O(\log k)$, so the scan costs $O(n \log k)$ besides the sort. The implementation keeps *active* as a sorted list, $O(k)$ per step, which is the same for a fixed machine.
- **Rewrite.** One pass over the items, $O(s)$.

The total is $O(l + s n + n \log n)$. In a real compiler, liveness is computed once on sets of bits and the intervals come from one backward pass over the blocks, so the time is close to linear in the size of the program. That is the whole reason for the method: no graph with up to $n^2 / 2$ edges is built.

## Properties

- **Optimal on intervals.** If the overlap is at most $k$, it uses exactly the overlap number of registers. Otherwise it spills the fewest intervals that bring the overlap down to $k$, which is the unit weight case of the [maximum $k$-colorable interval subgraph](/k-colorable-interval-subgraph/).
- **Not optimal on programs.** An interval is a convex hull of a live range in the linear order. The overlap graph can have more edges than the [interference graph](/interference-graph/), as in the example.
- **Depends on the block order.** A different block order gives different intervals. Orders that keep a loop body together, such as reverse postorder, give shorter intervals.
- **Whole intervals.** A name is either in one register for its whole interval or in memory everywhere. It never moves between two registers.
- **Not optimal in spill cost.** It counts spilled intervals, not loads and stores. A spilled name that is used often in a loop costs more than its count of one.

## Variants and improvements

- **Second-chance binpacking** (Traub, Holloway and Smith, 1998) keeps the lifetime holes of each name, lets a value move between a register and memory, and adds resolution moves on the edges of the control flow graph.
- **[Interval splitting](/live-range-splitting/)** (Wimmer and Mössenböck, 2005) keeps intervals with holes and splits an interval at a good position instead of spilling it whole. A split part can get a different register. This is the allocator of the Java HotSpot client compiler.
- **[Linear scan on SSA form](/ssa-linear-scan/)** (Wimmer and Franz, 2010) builds the intervals on SSA form, which makes them simpler, and resolves the phis after allocation.
- **Spill weights.** Many versions spill the interval with the lowest use count weighted by loop depth instead of the furthest end. That loses the optimality on intervals but often gives faster code.
- **[SSA-based allocation](/ssa-based-register-allocation/)** keeps the speed of a linear walk but colors the true interference graph of an SSA program, which is chordal, with the fewest registers.

## When to use it

Use it when compile time matters more than the last few percent of code quality: in a JIT compiler ([just-in-time compilation](/just-in-time-compilation/)), in a baseline tier, or for very large generated functions. It is also simple to write and to debug. For an ahead-of-time compiler that can afford a graph, [graph coloring](/chaitin-register-allocation/) or [SSA-based allocation](/ssa-based-register-allocation/) gives fewer spills. Inside one basic block, [local register allocation](/local-register-allocation/) with the furthest next use rule spills fewer loads and stores, because it splits values at each use.

## Pitfalls

- **Read before write.** Give the reads of an item a position before its write. Otherwise `x = y + 1` with $y$ dead after it needs two registers, and the overlap is one too high.
- **Dead definitions.** A name that is written and never read still has an interval of one position. Without it, the write may land in the register of a live name.
- **Live across a back edge.** A name live at a loop header must be live to the end of the loop body in the linear order. Liveness from the fixed point gives this; a single pass that looks only at definitions and uses does not.
- **Scratch registers.** The spill code needs registers that no interval can hold. Here $s_0$ and $s_1$ are kept apart for loads, which is enough for an instruction with two operands.
- **Ties at line L14.** Spilling the active interval when it ends at the same position as the new one moves a register for nothing. Keep the active one on a tie.
- **Parameters.** A parameter live on entry needs a write position. The block that loads parameters from their slots gives it one.

## Implementations

## History

Poletto, Engler and Kaashoek (1997) used linear scan as the fast allocator of tcc, a dynamic code generator for the Tick C language. Poletto and Sarkar (1999) described the algorithm in full, gave the furthest end spill rule, and showed that it ran much faster than graph coloring and gave code that was almost as fast. Traub, Holloway and Smith (1998) had in the meantime added lifetime holes and moves between a register and memory in their second-chance binpacking allocator. Wimmer and Mössenböck (2005) brought interval splitting into the Java HotSpot client compiler, and Wimmer and Franz (2010) moved linear scan onto SSA form.

## References
