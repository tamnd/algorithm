---
tag: Z9PJT0
kind: problem
slug: register-allocation-problem
name: Register allocation
aliases:
- global register allocation
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Assign the values of a program to a fixed number of machine registers, storing the rest in memory at least cost.
prereqs: [control-flow-graph, live-variable-analysis, graph-coloring]
see_also: [interference-graph, register-allocation-np-completeness, chaitin-register-allocation, linear-scan-register-allocation, ssa-based-register-allocation, local-register-allocation, register-coalescing-problem, spill-code-placement]
sources:
  - paper: doi:10.1016/0096-0551(81)90048-5
    title: Gregory J. Chaitin, Marc A. Auslander, Ashok K. Chandra, John Cocke, Martin E. Hopkins and Peter W. Markstein, Register allocation via coloring, Computer Languages 6(1), 1981, 47-57
    locator: the formulation of global allocation as the coloring of the interference graph, and the proof that every graph is the interference graph of some program
  - paper: doi:10.1145/800230.806984
    title: Gregory J. Chaitin, Register allocation and spilling via graph coloring, Proceedings of the SIGPLAN '82 Symposium on Compiler Construction, SIGPLAN Notices 17(6), 1982, 98-105
    locator: the build, simplify, spill and select phases, and the spill cost estimate
  - paper: doi:10.1007/978-3-540-72521-3_21
    title: "Florent Bouchez, Alain Darte, Christophe Guillon and Fabrice Rastello, Register allocation: what does the NP-completeness proof of Chaitin et al. really prove? Or revisiting register allocation: why and how, Languages and Compilers for Parallel Computing (LCPC 2006), LNCS 4382, Springer, 2007"
    locator: the analysis of the reduction of Chaitin et al., the role of critical edges, and the result that MaxLive registers suffice for a strict program when critical edges can be split and moves and swaps can be inserted
  - paper: doi:10.1007/11688839_20
    title: Sebastian Hack, Daniel Grund and Gerhard Goos, Register allocation for programs in SSA-form, Compiler Construction (CC 2006), LNCS 3923, Springer, 2006, 247-262
    locator: the interference graph of a strict SSA program is chordal, so it can be colored with MaxLive colors in polynomial time
  - paper: doi:10.1145/1254766.1254782
    title: Florent Bouchez, Alain Darte and Fabrice Rastello, On the complexity of spill everywhere under SSA form, Proceedings of LCTES 2007, ACM, 2007
    locator: the complexity of choosing the values to spill, which stays NP-complete under SSA form in general
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 13 (Register Allocation), local and global allocation, live ranges, interference and spill costs
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 11 (Register Allocation)
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 16 (Register Allocation)
---

Register allocation decides where each value of a program lives while the program runs: in one of the $k$ registers of the machine, or in a memory slot. A value that does not get a register is *spilled*, and the compiler adds stores and loads that move it between memory and a register. The goal is a program that uses only $k$ registers, gives the same results, and runs as few added loads, stores and copies as possible. This page states the problem and its forms; [register-allocation-np-completeness](/register-allocation-np-completeness/) gives the hardness of one form, and the allocator pages give the methods.

## In plain words

A processor computes only on values in its registers, and it has few of them, often 16 or 32. A program can have thousands of temporary values. Most of them are needed only for a short time, so the registers can be shared: two values can use the same register when they are never needed at the same moment. When too many values are needed at the same moment, some of them must wait in memory. The compiler writes each such value to memory and reads it back just before it is needed again. Memory is slow, so these extra reads and writes cost time. Register allocation chooses which values stay in registers, which register each one gets, and which values go to memory, so that the program stays correct and the extra work is small.

## Definition

The input is a program $P$ in the toy IR (three-address code in basic blocks, a [control flow graph](/control-flow-graph/)), a number $k \ge 2$ of registers, and a weight $f(B) \ge 0$ for each block $B$, an estimate of how often $B$ runs. The memory slot of a name $x$ is written as the name `mem.x`; `t = mem.x` is a load and `mem.x = t` is a store. A slot is not a register.

A name $x$ is *live* at a point of $P$ if some path from that point reaches a use of $x$ with no definition of $x$ before it, as computed by [live variable analysis](/live-variable-analysis/). The *live range* of $x$ is the set of points where $x$ is live. $\mathrm{MaxLive}$ is the largest number of names live at one point. Two names *interfere* if one of them is live just after a definition of the other, unless that definition is a copy from the other name; the [interference graph](/interference-graph/) has the names as vertices and an edge for each interfering pair.

The output is a program $P'$ with these properties:

1. Every operand and result of an instruction is a register $r_0, \ldots, r_{k-1}$, except the slot of a load or a store.
2. $P'$ is $P$ with each name renamed to a register at each point, plus added loads, stores and copies, and possibly added blocks on split edges.
3. For every input, $P'$ has the same outcome as $P$ (the same return value, the same trap, or no end).

The cost of $P'$ is the sum, over the added instructions $i$, of $f(B_i) \cdot c(i)$, where $B_i$ is the block of $i$ and $c$ gives a cost to a load, a store and a copy. The problem is to find $P'$ of least cost.

Four forms of the problem are studied on their own:

- **Coloring without splitting.** Each name gets one register for its whole live range, and no code is added. This is possible if and only if the interference graph has a [k-coloring](/k-coloring/): a register is a color, and two interfering names must not share a register.
- **Spilling.** Choose the names to keep in memory, and where to put the loads and stores, so that the rest fits in $k$ registers at least cost ([spill code placement](/spill-code-placement/)).
- **Splitting.** A name can move from one register to another through copies, so different parts of its live range can get different registers ([live range splitting](/live-range-splitting/)).
- **Coalescing.** Give the source and the target of a copy the same register, so that the copy can be deleted ([register coalescing problem](/register-coalescing-problem/)).

## Variants

- **Local allocation** works on one basic block at a time and keeps no value in a register across blocks ([local register allocation](/local-register-allocation/)). With equal reload costs and no stores, it is the paging problem, and [Belady's algorithm](/belady-algorithm/) is optimal for it.
- **Global allocation** works on a whole procedure. This is the form of this page, and the alias "global register allocation" names it.
- **Allocation on SSA form** first spills until $\mathrm{MaxLive} \le k$, then colors the chordal interference graph with at most $k$ colors, and coalesces last ([SSA-based register allocation](/ssa-based-register-allocation/)).
- **Linear scan** gives up the interference graph and assigns registers to live intervals in one sweep, for fast compilers such as JIT compilers ([linear scan register allocation](/linear-scan-register-allocation/)).
- **Real machines** add constraints: some values must be in a fixed register (arguments and results of calls), some registers are destroyed by a call, and some instructions need register pairs or a register class. An allocator models a fixed register as a precolored vertex.

## Examples

**One block.** The program below has one parameter `p`.

```
L0:
  a = p + 1
  b = p + 2
  c = a + b
  d = a * c
  e = b * d
  ret e
```

The live names just after each instruction are $\{p, a\}$, $\{a, b\}$, $\{a, b, c\}$, $\{b, d\}$ and $\{e\}$, and $\{p\}$ is live at the start, so $\mathrm{MaxLive} = 3$. The interference edges are $p$-$a$, $a$-$b$, $a$-$c$, $b$-$c$ and $b$-$d$; $e$ interferes with nothing. The triangle $a, b, c$ needs three colors, and three colors suffice. With $k = 3$ and the parameter loaded from its slot, the allocator of [Chaitin](/chaitin-register-allocation/) gives this program, with no added code apart from the parameter load:

```
start:
  r0 = mem.p
  jump L0
L0:
  r1 = r0 + 1
  r0 = r0 + 2
  r2 = r1 + r0
  r1 = r1 * r2
  r0 = r0 * r1
  ret r0
```

With $k = 2$ some value must go to memory. Just after `c = a + b`, the three values $a$, $b$ and $c$ are all used later, and only two fit in registers. In the toy IR every result is written to a register, so the value that waits in memory needs one store and one load. One store and one load also suffice: store `b` after its definition and load it just before `e = b * d`. So the least cost is one store and one load. A script ran this program and the two-register version on the inputs $-50$ to $49$ and found the same outcomes.

**Coloring is not the whole problem.** The program built on the page [register-allocation-np-completeness](/register-allocation-np-completeness/) for the triangle has three names `u`, `v` and `w` that interfere in a triangle, so no two-register assignment without splitting exists. But at most two names are live at any point, and one copy on one split edge gives a correct program with two registers. The interference graph answers only the first of the four forms above.

## Known algorithms

- [Chaitin's allocator](/chaitin-register-allocation/) builds the interference graph, removes vertices of degree less than $k$, chooses spills by cost per degree, and repeats after it adds spill code.
- [Optimistic coloring](/briggs-optimistic-coloring/) by Briggs, Cooper and Torczon delays the spill decision to the color assignment, and spills a subset of what Chaitin's allocator spills.
- [Iterated register coalescing](/iterated-register-coalescing/) of George and Appel interleaves simplification with [conservative coalescing](/conservative-coalescing/).
- [Linear scan](/linear-scan-register-allocation/) and its SSA form [SSA linear scan](/ssa-linear-scan/) trade quality for speed.
- [SSA-based register allocation](/ssa-based-register-allocation/) uses the chordal interference graph of SSA form ([SSA chordal interference theorem](/ssa-chordal-interference-theorem/)).
- Exact methods state the problem as an integer linear program. A real tool hands such a program to an ILP solver; the cost grows fast with the size of the procedure.

## Bounds

- **Lower bound.** In a strict program (every use is reached only by paths that define the name) with no copies, the names live at one point interfere in pairs. Take two such names $x$ and $y$ and a path from the entry to the point. If the last definition of $y$ on the path comes after the last definition of $x$, then $x$ is live just after that definition of $y$. So these names form a clique, and $\chi(G) \ge \omega(G) \ge \mathrm{MaxLive}$, where $\chi$ is the [chromatic number](/chromatic-number/) and $\omega$ the size of the largest [clique](/clique/).
- **The gap can be large.** Every graph, with one isolated vertex added, is the interference graph of a program with $\mathrm{MaxLive} \le 2$ (the construction on [register-allocation-np-completeness](/register-allocation-np-completeness/)). A [Mycielski graph](/mycielski-graph/) has no triangle and an arbitrarily large chromatic number, so the coloring form can need many more registers than $\mathrm{MaxLive}$.
- **Upper bound with splitting.** Bouchez, Darte, Guillon and Rastello (LCPC 2006) show that a strict program can be allocated with $\mathrm{MaxLive}$ registers and no spill when critical edges can be split ([critical edge splitting](/critical-edge-splitting/)) and moves and swaps can be inserted. So under these assumptions the question "are $k$ registers enough without spilling?" is answered by the test $\mathrm{MaxLive} \le k$, in polynomial time.
- **SSA form.** In strict SSA form the interference graph is chordal and $\chi = \omega = \mathrm{MaxLive}$ (Hack, Grund and Goos 2006), so a [perfect elimination ordering](/perfect-elimination-ordering/) colors it optimally.
- **Hardness.** The coloring form is NP-complete for every fixed $k \ge 3$ ([register-allocation-np-completeness](/register-allocation-np-completeness/)); for $k = 2$ it is a [bipartiteness test](/bipartiteness-testing/), in linear time. The choice of the values to spill everywhere stays NP-complete under SSA form in general (Bouchez, Darte and Rastello, LCTES 2007), and so does coalescing ([register coalescing problem](/register-coalescing-problem/)).

## Reductions

- The coloring form and [k-coloring](/k-coloring/) reduce to each other in polynomial time. One direction builds the interference graph. The other builds, for a graph $G$, a program whose interference graph is $G$ plus one isolated vertex. A reduction from [3-colorability](/three-coloring/) gives NP-hardness for three registers.
- Local allocation with clean values and unit reload costs is the [paging problem](/paging-problem/) with a cache of $k$ pages.
- In high-level synthesis, [register binding](/register-binding/) maps the values of a schedule to hardware registers; for a straight schedule the live ranges are intervals, and the same coloring view applies.

## Applications

Every optimizing compiler for a real processor has a register allocator, because operands of arithmetic instructions must be in registers. The allocator matters most in loops: a spill inside a loop runs on every iteration, which is why the block weights $f(B)$ usually grow with the loop depth. JIT compilers use linear scan or a local allocator to keep compile time low. The same problem appears in the allocation of registers in hardware synthesis and of scratchpad memory on accelerators.

## References
