---
tag: 04HWFD
kind: definition
slug: interference-graph
name: Interference graph
aliases:
- register interference graph
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: An undirected graph with one vertex per name of a program and an edge between two names that cannot share a register, because one is live where the other is defined.
prereqs: [live-variable-analysis, undirected-graph]
see_also: [register-allocation-problem, chaitin-register-allocation, k-coloring, chordal-graph, ssa-chordal-interference-theorem, register-coalescing-problem, def-use-chains, linear-scan-register-allocation]
sources:
  - paper: doi:10.1016/0096-0551(81)90048-5
    title: Gregory J. Chaitin, Marc A. Auslander, Ashok K. Chandra, John Cocke, Martin E. Hopkins and Peter W. Markstein, Register allocation via coloring, Computer Languages 6(1), 1981, 47-57
    locator: the interference graph, its edges from the live names at each definition, and the proof that every graph is the interference graph of some program
  - paper: doi:10.1145/800230.806984
    title: Gregory J. Chaitin, Register allocation and spilling via graph coloring, Proceedings of the SIGPLAN '82 Symposium on Compiler Construction, SIGPLAN Notices 17(6), 1982, 98-105
    locator: the build phase, the bit matrix and adjacency lists, and the rule that a copy does not make its source and target interfere
  - paper: doi:10.1007/11688839_20
    title: Sebastian Hack, Daniel Grund and Gerhard Goos, Register allocation for programs in SSA-form, Compiler Construction (CC 2006), LNCS 3923, Springer, 2006, 247-262
    locator: the interference graph of a strict SSA program is chordal
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 10 (Liveness Analysis), the section on interference graphs and the special treatment of move instructions
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 16 (Register Allocation), webs, and the construction of the interference graph as an adjacency matrix and adjacency lists
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 13 (Register Allocation), live ranges and the interference graph of global allocation
---

The interference graph of a program has one vertex for each name and an edge between two names that must not share a register. Two names get an edge when one of them is live just after an instruction that defines the other. A [k-coloring](/k-coloring/) of the graph is the same thing as an assignment of $k$ registers in which each name keeps one register for its whole life. The graph is the input of the allocators of Chaitin, Briggs and George and Appel; the [register allocation problem](/register-allocation-problem/) is larger, because it also allows spills, splits and copies.

## Definition

Let $P$ be a program in the toy IR. [Live variable analysis](/live-variable-analysis/) gives, for each instruction $i$, the set $\mathrm{out}(i)$ of names live just after $i$. The memory slots `mem.x` are not register candidates and are left out. A parameter is treated as defined at the entry; an allocator usually makes this explicit with a load `p = mem.p` in a new entry block.

The **interference graph** $G = (V, E)$ is the [undirected graph](/undirected-graph/) with these vertices and edges:

- $V$ is the set of names of $P$.
- For each instruction $i$ that defines a name $x$, and for each $y \in \mathrm{out}(i)$ with $y \ne x$, the edge $\{x, y\}$ is in $E$, except when $i$ is a copy `x = y`.

No other edge is in $E$. Two names *interfere* if they are joined by an edge.

The rule is Chaitin's. It looks at the definitions and not at whole live ranges, for two reasons:

1. **A copy does not make its source and target interfere.** Just after `x = y`, both names hold the same value, so one register can serve both. If one of them is later redefined while the other is still live, that later definition adds the edge.
2. **A dead definition still interferes.** If $x$ is not live after its definition $i$, the instruction still writes a register. So $x$ gets an edge to each name in $\mathrm{out}(i)$, and the write cannot destroy a live value.

The *live range* of a name is the set of points where it is live. A weaker test says that two names interfere when their live ranges meet. In a strict program, where every path from the entry to a use of a name passes through a definition of it, two live ranges that meet give an edge in $E$ unless a copy joins the two names: on a path from the entry to a common point, take the later of the two last definitions; the other name is live just after it. Compared with the weaker test, the rule above adds edges only at dead definitions, and removes edges only at copies.

The copies `x = y` between two names form a second set of edges, the **move edges** or affinities. They are not interference edges. A coalescer tries to give the two ends of a move edge the same color, so that the copy disappears ([register coalescing problem](/register-coalescing-problem/)).

A machine register that an instruction requires (an argument of a call, a result) is a **precolored** vertex: its color is fixed in advance.

Allocators often build the graph on *webs* instead of names. A web is a maximal set of definitions and uses of one variable that are linked through [def-use chains](/def-use-chains/). In a strict program two webs of one variable are never live at the same point, so they can get different registers. Renaming each web to its own name and then building the graph on names gives the graph on webs.

**Size and construction.** The graph has $n = |V|$ vertices and at most $n(n-1)/2$ edges. A backward walk over each block from the live-out set visits each instruction once and adds one edge per live name, so the build takes time proportional to the sum of $|\mathrm{out}(i)|$ over all instructions, plus the liveness analysis. Chaitin kept both a bit matrix, to test an edge in constant time, and adjacency lists, to visit the neighbors of a vertex.

## Examples and non-examples

**A triangle.** In the block

```
L0:
  a = p + 1
  b = p + 2
  c = a + b
  d = a * c
  e = b * d
  ret e
```

the sets $\mathrm{out}(i)$ are $\{p, a\}$, $\{a, b\}$, $\{a, b, c\}$, $\{b, d\}$ and $\{e\}$. The edges are $p$-$a$, $a$-$b$, $a$-$c$, $b$-$c$ and $b$-$d$, and $e$ has no edge. The triangle $a, b, c$ shows that three registers are needed for an assignment without spills.

**A copy that does not interfere.** In

```
L0:
  y = x
  z = x + y
  ret z
```

the set $\mathrm{out}$ of the copy is $\{x, y\}$, but the copy is from $x$, so $x$ and $y$ get no edge, even though both are live at the same point. One register serves both, and after renaming the copy becomes `r0 = r0`, which is deleted. The test by meeting live ranges would put an edge here and waste a register.

**The same copy, then a redefinition.** If `y = y + 1` follows `y = x`, then $x$ is live just after that new definition, and the edge $x$-$y$ appears. The exception for copies is safe because each later change of either name is a definition, and the rule checks it.

**A dead definition.** In

```
L0:
  a = p + 1
  t = p * 2
  b = a + p
  ret b
```

the name `t` is never used, so its live range is empty. The set $\mathrm{out}$ of `t = p * 2` is $\{a, p\}$, so the rule adds $t$-$a$ and $t$-$p$, and $\{p, a, t\}$ is a triangle. Under the test by meeting live ranges, `t` has no edge, it could get the register of `a`, and the write to `t` would destroy `a`.

**Not every interference graph is chordal.** The loop

```
L0:
  d = n
  jump L1
L1:
  a = d + 1
  b = a + d
  c = a + 1
  d = b - c
  d = d % c
  br d L1 L2
L2:
  ret d
```

has the edges $a$-$b$, $b$-$c$, $c$-$d$ and $d$-$a$ and no others: a cycle of length 4 with no chord. The copy `d = n` adds the move edge $d$-$n$ but no interference. This graph is not a [chordal graph](/chordal-graph/), but it is 2-colorable. Simplification by degree fails on it with $k = 2$, which is the example of [optimistic coloring](/briggs-optimistic-coloring/).

**Every graph is an interference graph.** For each graph there is a program whose interference graph is that graph plus one isolated vertex. The construction is on the page [register-allocation-np-completeness](/register-allocation-np-completeness/), and it is the reason why the coloring form of allocation is NP-complete.

## Related definitions

- [Live variable analysis](/live-variable-analysis/) gives the sets $\mathrm{out}(i)$, and the interference graph is built from them.
- [Graph coloring](/graph-coloring/), [k-coloring](/k-coloring/) and the [chromatic number](/chromatic-number/) give the vocabulary: a color is a register.
- In strict SSA form the interference graph is chordal, and the order of the definitions in the [dominator tree](/dominator-tree/) is a [perfect elimination ordering](/perfect-elimination-ordering/) read backward ([SSA chordal interference theorem](/ssa-chordal-interference-theorem/)). The cycle above shows that this fails for programs with several definitions of one name.
- [Linear scan register allocation](/linear-scan-register-allocation/) replaces each live range by one interval from its first to its last point. The graph of overlapping intervals has at least the edges of the interference graph, and it can be colored by a greedy sweep.
- The [register coalescing problem](/register-coalescing-problem/) works on the interference edges and the move edges together.

## References
