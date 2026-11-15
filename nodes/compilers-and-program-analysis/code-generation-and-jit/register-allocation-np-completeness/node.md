---
tag: TAJDRY
kind: theorem
slug: register-allocation-np-completeness
name: NP-completeness of register allocation
aliases:
- Chaitin's NP-completeness theorem
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Every graph is the interference graph of some program, so deciding whether a program fits in k registers, each name keeping one register, is NP-complete for every fixed k >= 3.
prereqs: [register-allocation-problem, interference-graph, k-coloring, np-complete]
see_also: [three-coloring, chaitin-register-allocation, ssa-chordal-interference-theorem, critical-edge-splitting, live-range-splitting, polynomial-time-reduction, mycielski-graph, chordal-graph]
sources:
  - paper: doi:10.1016/0096-0551(81)90048-5
    title: Gregory J. Chaitin, Marc A. Auslander, Ashok K. Chandra, John Cocke, Martin E. Hopkins and Peter W. Markstein, Register allocation via coloring, Computer Languages 6(1), 1981, 47-57
    locator: the construction of a program for any given graph, so that coloring the interference graph is as hard as coloring a general graph
  - paper: doi:10.1007/978-3-540-72521-3_21
    title: "Florent Bouchez, Alain Darte, Christophe Guillon and Fabrice Rastello, Register allocation: what does the NP-completeness proof of Chaitin et al. really prove? Or revisiting register allocation: why and how, Languages and Compilers for Parallel Computing (LCPC 2006), LNCS 4382, Springer, 2007"
    locator: the program of Chaitin et al. redrawn with its extra name x, the role of critical edges, MaxLive registers suffice when critical edges can be split and moves and swaps are allowed, and hardness with splitting when critical edges cannot be split
  - paper: doi:10.1007/11690634_6
    title: Fernando Magno Quintão Pereira and Jens Palsberg, Register allocation after classical SSA elimination is NP-complete, Foundations of Software Science and Computation Structures (FoSSaCS 2006), LNCS 3921, Springer, 2006
    locator: the programs of Chaitin et al. can be colored with three colors after conversion to SSA form and back (the example of the cycle of length 4), and the reduction from circular-arc graph coloring for programs after SSA elimination
  - paper: doi:10.1007/11688839_20
    title: Sebastian Hack, Daniel Grund and Gerhard Goos, Register allocation for programs in SSA-form, Compiler Construction (CC 2006), LNCS 3923, Springer, 2006, 247-262
    locator: the interference graph of a strict SSA program is chordal and can be colored in polynomial time
  - book: isbn:0716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.1, problem GT4 (Graph K-Colorability), NP-complete for every fixed K >= 3
---

The theorem of Chaitin, Auslander, Chandra, Cocke, Hopkins and Markstein (1981) says that every graph is the interference graph of some program. So the question "can this program run in $k$ registers, if each name keeps one register for its whole life?" is exactly as hard as $k$-coloring of general graphs, and it is NP-complete for every fixed $k \ge 3$. The theorem is about this coloring form only. It says nothing about the full [register allocation problem](/register-allocation-problem/), where a name can move between registers: the hard programs of the proof need only two registers once one copy can be placed on a split edge.

## Statement

A program is in the toy IR with `const`, `copy` and `op` instructions. Its [interference graph](/interference-graph/) $G(P)$ has one vertex per name and an edge $\{x, y\}$ when $y$ is live just after an instruction that defines $x$, and that instruction is not the copy `x = y`.

**Problem $\mathrm{RA}_k$** (for a fixed integer $k$). Input: a program $P$. Question: is there a map $R$ from the names of $P$ to $\{0, \ldots, k-1\}$ with $R(x) \ne R(y)$ for every edge $\{x, y\}$ of $G(P)$? Such a map renames each name to one register, and the proof file of [Chaitin's allocator](/chaitin-register-allocation/) shows that the renamed program has the same outcome as $P$.

**Theorem.**

1. For every graph $H$ with $n$ vertices and $m$ edges there is a program $P(H)$, built in time $O(n + m)$, whose interference graph is $H$ plus one isolated vertex. $P(H)$ is strict, has no loop and no copy, and at most two names are live at any point of it.
2. For every fixed $k \ge 3$, $\mathrm{RA}_k$ is NP-complete.

## In plain words

Two values that are needed at the same time cannot share a register. Draw a dot for each value and a line between two values that clash. Giving registers is then coloring the dots so that no line joins two dots of one color. Coloring a drawing with three colors is a famous hard problem. Chaitin and his colleagues showed that every drawing of dots and lines comes from some program. So if a fast method could always give registers to programs, it could also color every drawing, and no fast method for that is known. The programs in the proof are strange, though. They never need more than two values at once. They are hard only because the rules say that each value must stay in one register. If a value may move to another register on the way, two registers are enough.

## Proof

**Membership in NP.** A certificate is the map $R$. Live variable analysis over the [control flow graph](/control-flow-graph/) of $P$ takes polynomial time, and so does the walk that lists the edges of $G(P)$. Checking $R(x) \ne R(y)$ on each edge is then linear in the number of edges.

**The program $P(H)$.** Let $H = (V, E)$ with $V = \{x_1, \ldots, x_n\}$, $n \ge 1$. An *item* is an edge of $H$ or an isolated vertex of $H$. List the items as $I_1, \ldots, I_t$; then $t \ge 1$. The program has one parameter $p$, and one name for each vertex of $H$. Its blocks are:

- For $j = 1, \ldots, t - 1$, a selector block $S_j$ with `p = p - 1` and `br p N_j T_j`, where $N_j = S_{j+1}$ for $j < t - 1$ and $N_{t-1} = T_t$.
- For an item $I_j = \{x, y\}$ that is an edge, a block $T_j$ with `x = 1`, `y = 2` and `br y R_y R_x`.
- For an item $I_j = x$ that is an isolated vertex, a block $T_j$ with `x = 1` and `jump R_x`.
- For each vertex $x$, a block $R_x$ with `ret x`.

The entry block is $S_1$, or $T_1$ when $t = 1$. The program has $2t - 1 + n$ blocks and $O(n + m)$ instructions. It has no loop, because every edge of its flow graph goes from an $S$ block to a later $S$ block or to a $T$ block, or from a $T$ block to an $R$ block. It is strict: the only predecessors of $R_x$ are $T$ blocks that define $x$, and $p$ is a parameter.

The branch conditions are constants inside the $T$ blocks, so a run takes only one of the two exits. This does not matter: liveness is defined by the paths of the flow graph, not by the values.

**Lemma 1 (live sets).** The live names of $P(H)$ are:

- at the start of $R_x$: exactly $\{x\}$;
- in a $T$ block of an edge $\{x, y\}$: nothing at the start, $\{x\}$ just after `x = 1`, and $\{x, y\}$ just after `y = 2`;
- in a $T$ block of an isolated vertex $x$: nothing at the start, and $\{x\}$ just after `x = 1`;
- in each selector block: $\{p\}$ at the start and $\{p\}$ just after `p = p - 1`.

*Proof.* $R_x$ uses $x$ and has no successor, so its live-in set is $\{x\}$. A $T$ block of an edge $\{x, y\}$ has the successors $R_y$ and $R_x$, so its live-out set is $\{x, y\}$. The branch reads $y$, which is in that set already. Going backward, `y = 2` removes $y$, which leaves $\{x\}$, and `x = 1` removes $x$, which leaves the empty set. The case of an isolated vertex is the same with one successor. Every successor of a selector block is a selector block or a $T$ block, and their live-in sets are $\{p\}$ and $\emptyset$. The branch reads $p$, so $\{p\}$ is live just after `p = p - 1`, and since that instruction reads $p$, $\{p\}$ is live at the start. The live sets are a fixed point of the backward equations, and no smaller sets satisfy them, because each name in them is read later on some path with no definition before the read. $\square$

**Lemma 2 (edges).** $G(P(H))$ has the vertex set $V \cup \{p\}$ and the edge set $E$.

*Proof.* Each name of $V$ is defined in some $T$ block and read in its $R$ block, and $p$ is the parameter, so the vertices are $V \cup \{p\}$. We go through every definition and the set of names live just after it, from Lemma 1. In a selector block, `p = p - 1` is followed by $\{p\}$, which gives no edge. In a $T$ block, `x = 1` is followed by $\{x\}$, which gives no edge. In the $T$ block of an edge $\{x, y\}$, `y = 2` is followed by $\{x, y\}$, which gives exactly the edge $\{x, y\}$. Each edge of $E$ has its own $T$ block, so every edge of $E$ appears, and no other edge appears. $\square$

Lemma 1 also shows that at most two names are live at any point. This proves part 1.

**NP-hardness.** For a fixed $k \ge 3$, the problem $k$-coloring is NP-complete ([k-coloring](/k-coloring/); for $k = 3$ this is [3-colorability](/three-coloring/), and for $k > 3$ one adds $k - 3$ new vertices joined to every other vertex). Map a graph $H$ to $P(H)$. By Lemma 2, $G(P(H))$ is $H$ plus the isolated vertex $p$. An isolated vertex can take any color, so $G(P(H))$ has a $k$-coloring if and only if $H$ has one, and a $k$-coloring of $G(P(H))$ is exactly a map $R$ as in $\mathrm{RA}_k$. The map $H \mapsto P(H)$ takes linear time, so it is a [polynomial-time reduction](/polynomial-time-reduction/). With membership in NP, this proves part 2. $\blacksquare$

**Example.** For the triangle $u, v, w$, a program of the same shape, with other constants and block names, is this one, with parameter `p`:

```
S1:
  p = p - 1
  br p S2 E1
S2:
  p = p - 1
  br p E2 E3
E1:
  v = 3
  u = 0
  br u Ru Rv
E2:
  w = 5
  v = 4
  br v Rv Rw
E3:
  u = 7
  w = 0
  br w Rw Ru
Ru:
  ret u
Rv:
  ret v
Rw:
  ret w
```

The interference edges are $u$-$v$, $v$-$w$ and $w$-$u$, and $p$ is isolated. No map to two registers exists. But at most two names are live at any point, and the edge from `E3` to `Ru` is a critical edge (`E3` has two successors and `Ru` has two predecessors). Split it with a new block `X` that holds one copy, and two registers suffice:

```
S1:
  r0 = r0 - 1
  br r0 S2 E1
S2:
  r0 = r0 - 1
  br r0 E2 E3
E1:
  r0 = 3
  r1 = 0
  br r1 Ru Rv
E2:
  r1 = 5
  r0 = 4
  br r0 Rv Rw
E3:
  r0 = 7
  r1 = 0
  br r1 Rw X
X:
  r1 = r0
  jump Ru
Ru:
  ret r1
Rv:
  ret r0
Rw:
  ret r1
```

Here $u$ is in `r1` in `E1` and in `r0` in `E3`, so its live range is split. A script ran both programs on the inputs $-1$ to $3$: both return 3 for $p = 1$, 7 for $p = 2$ and 4 otherwise.

## Consequences

- No polynomial-time algorithm decides $\mathrm{RA}_k$ for any fixed $k \ge 3$ unless P = NP. This is why [Chaitin's allocator](/chaitin-register-allocation/), [optimistic coloring](/briggs-optimistic-coloring/) and [iterated register coalescing](/iterated-register-coalescing/) are heuristics that may spill a name although a coloring exists.
- The [chromatic number](/chromatic-number/) of an interference graph is not bounded by any function of $\mathrm{MaxLive}$. A [Mycielski graph](/mycielski-graph/) has no triangle and any chromatic number, and $P(H)$ has $\mathrm{MaxLive} \le 2$ for every $H$.
- The hardness comes from the rule that a name keeps one register. Bouchez, Darte, Guillon and Rastello (LCPC 2006) show that a strict program fits in $\mathrm{MaxLive}$ registers without spills when critical edges can be split and moves and swaps can be inserted, so with these freedoms the question is decided by computing $\mathrm{MaxLive}$. They also show that when critical edges cannot be split, deciding whether $k$ registers suffice stays NP-complete even with live range splitting.
- In strict SSA form the interference graph is chordal, so $\chi = \omega = \mathrm{MaxLive}$ and an optimal coloring takes polynomial time (Hack, Grund and Goos 2006; see [SSA chordal interference theorem](/ssa-chordal-interference-theorem/)). Pereira and Palsberg (FoSSaCS 2006) observe that the programs of Chaitin et al., once converted to SSA form and back, can be colored with three colors, and they show that the coloring form becomes NP-complete again for programs after the classical elimination of SSA form, by a reduction from coloring circular-arc graphs.

## Tightness

- **The bound $k \ge 3$ is needed.** $\mathrm{RA}_1$ asks whether $G(P)$ has no edge, and $\mathrm{RA}_2$ asks whether $G(P)$ is bipartite ([bipartiteness testing](/bipartiteness-testing/)). Both take linear time in the size of the graph.
- **Branches and joins are needed.** In one basic block with no copies, each live range is an interval of instruction positions, and a dead definition is a single point. Then the graph is an interval graph: its chromatic number equals the size of its largest clique, and a greedy sweep in the order of the definitions finds an optimal coloring ([interval partitioning](/interval-partitioning-greedy/)). The construction above needs a join at each $R$ block, but no loop.
- **Register pressure is not the cause.** The hard instances have $\mathrm{MaxLive} \le 2$, the smallest value that allows an edge at all.
- **The result is about one form only.** With live range splitting on split critical edges it fails, as the example above shows.

## History

Chaitin, Auslander, Chandra, Cocke, Hopkins and Markstein described global register allocation by graph coloring for the experimental PL.8 compiler at IBM in 1981. Their paper also built, for any graph, a program with that interference graph. The program, as redrawn by Bouchez et al., has one extra name $x$: each edge block also sets $x = u + v$, and each return block returns $u + x$. So $x$ interferes with every other name, and the program needs $k + 1$ registers exactly when the graph needs $k$ colors. The version on this page drops $x$ and gives an isolated vertex instead.

For twenty-five years the result was often read as "register allocation is NP-complete". Around 2005 and 2006, several groups found that SSA programs have chordal interference graphs (Hack, Grund and Goos; Bouchez, Darte, Guillon and Rastello; Brisk, Dabiri, Macbeth and Sarrafzadeh). Bouchez, Darte, Guillon and Rastello then asked what the reduction of Chaitin et al. really proves, and located the hardness in the ban on splitting, in critical edges, in spilling and in coalescing.

## References
