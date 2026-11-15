---
tag: A8A6R0
kind: problem
slug: register-coalescing-problem
name: Register coalescing
aliases:
- copy coalescing
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Merge the nodes of copy-related values in the interference graph to remove copies, while keeping the graph colorable; NP-complete in general.
prereqs: [interference-graph, register-allocation-problem]
see_also: [conservative-coalescing, iterated-register-coalescing, chaitin-register-allocation, out-of-ssa-translation, live-range-splitting, ssa-based-register-allocation, k-coloring, copy-propagation]
sources:
  - paper: doi:10.1109/CGO.2007.26
    title: Florent Bouchez, Alain Darte and Fabrice Rastello, On the complexity of register coalescing, International Symposium on Code Generation and Optimization (CGO), 2007, 102-114
    locator: the definitions of aggressive, conservative, incremental conservative and optimistic coalescing, and their NP-completeness results
  - paper: doi:10.1145/800230.806984
    title: Gregory J. Chaitin, Register allocation and spilling via graph coloring, Proceedings of the SIGPLAN '82 Symposium on Compiler Construction, SIGPLAN Notices 17(6), 1982, 98-105
    locator: subsumption, the aggressive coalescing of copies before coloring
  - paper: doi:10.1145/177492.177575
    title: Preston Briggs, Keith D. Cooper and Linda Torczon, Improvements to graph coloring register allocation, ACM Transactions on Programming Languages and Systems 16(3), 1994, 428-455
    locator: conservative coalescing and the problem that aggressive coalescing causes spills
  - paper: doi:10.1145/229542.229546
    title: Lal George and Andrew W. Appel, Iterated register coalescing, ACM Transactions on Programming Languages and Systems 18(3), 1996, 300-324
    locator: the George test and the interleaving of coalescing with simplification
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 11 (Register Allocation), the section on coalescing and the Briggs and George criteria
---

Register coalescing removes copy instructions `x = y` by giving $x$ and $y$ the same register: the copy becomes `r = r` and is deleted. In the [interference graph](/interference-graph/), this means merging the vertices of $x$ and $y$ into one vertex, which is possible only if $x$ and $y$ do not interfere. Each merge also makes the graph harder to color, because the merged vertex has the neighbors of both. The problem is to remove as many copies as possible, weighted by how often they run, while the graph stays colorable with the $k$ registers. Bouchez, Darte and Rastello (2007) proved that its main forms are NP-complete.

## In plain words

Compilers make many copies of values: when they leave SSA form, when they inline a function, and when they move arguments into the registers a call expects. A copy costs nothing if the value and its copy sit in the same register, because then there is nothing to move. So the compiler tries to put each value and its copy in one register. This is only allowed when the two are never needed at the same time with different contents. But joining two values also joins their conflicts, and too many conflicts can push a value out to memory, which costs more than the copy. The task is to remove as many copies as possible without pushing anything out to memory.

## Definition

An *affinity graph* is an interference graph $G = (V, E)$ with a set $A$ of affinity edges, one for each copy `x = y` between two names, and a weight $w(a) \ge 0$ for each $a \in A$, such as the number of times the copy runs. A copy does not make its two names interfere: at a copy `x = y`, the definition rule of the interference graph leaves out the edge $\{x, y\}$. They interfere only if some other definition of one of them happens while the other is live.

A *coalescing* is a partition of $V$ into classes such that no two vertices of one class are adjacent in $G$. The *coalesced graph* $G_f$ has the classes as vertices, and two classes are adjacent if some vertex of one is adjacent in $G$ to some vertex of the other. An affinity is *coalesced* if its two ends are in one class. A $k$-coloring of $G_f$ gives a $k$-coloring of $G$ in which the two ends of each coalesced affinity have the same color, so each coalesced copy is deleted.

**Problem (coalescing).** Given $G$, $A$, $w$ and $k$, find a coalescing that maximizes the total weight of the coalesced affinities, such that $G_f$ satisfies a coloring condition. The condition defines the variant.

## Variants

The names follow Bouchez, Darte and Rastello (2007).

- **Aggressive coalescing.** No coloring condition: any coalescing is allowed. It is the first step of Chaitin's allocator, which then spills if the coalesced graph is hard to color.
- **Conservative coalescing.** $G_f$ must stay *greedy-$k$-colorable*, that is, its $k$-core must be empty, so that the simplify phase of [Chaitin's allocator](/chaitin-register-allocation/) colors it. A stronger condition, "$G_f$ is $k$-colorable", is also studied, but even checking it is NP-complete.
- **Incremental conservative coalescing.** $G$ is greedy-$k$-colorable and only one affinity $\{x, y\}$ is given: can $x$ and $y$ be merged so that the graph stays greedy-$k$-colorable? This is the question that the [Briggs and George tests](/conservative-coalescing/) answer in part.
- **Optimistic coalescing.** Start from an aggressive coalescing and undo as few merges as possible, by weight, until the graph is greedy-$k$-colorable.
- **Precolored vertices.** Some names must be in fixed registers, for example arguments in a calling convention. They are vertices that are already colored, and two precolored vertices of different colors interfere.

## Examples

**All copies can go.** In this loop, after [out-of-SSA translation](/out-of-ssa-translation/):

```
L0:
  i = n
  s = 0
  jump L1
L1:
  t = s + i
  j = i - 1
  s = t
  i = j
  br i L1 L2
L2:
  ret s
```

the edges are $i$-$s$, $s$-$j$, $j$-$t$ and $t$-$i$, and the affinities are $i$-$n$, $i$-$j$ and $s$-$t$. The classes $\{i, j, n\}$ and $\{s, t\}$ are a coalescing with one edge between them, so with $k = 2$ all three copies are deleted. [Iterated register coalescing](/iterated-register-coalescing/) finds it.

**Two copies compete.** Here $b$ and $c$ are both copies of $a$:

```
L0:
  a = p + 1
  b = a
  c = a
  d = b * c
  ret d
```

The only edge is $b$-$c$: at `c = a`, the name $b$ is live. The affinities are $a$-$b$ and $a$-$c$. A class cannot hold both $b$ and $c$, so at most one copy can be coalesced. Note that $b$ and $c$ hold the same value, so one register would do for all three names; the definition rule does not see values, only names.

**Aggressive coalescing causes a spill.** In this program, $b$ is a copy of $a$ on one path:

```
L0:
  y = p + 2
  x = p + 1
  br x L1 L2
L1:
  a = x + 1
  a = a + x
  b = a
  jump L3
L2:
  b = y + 1
  b = b + y
  jump L3
L3:
  ret b
```

The edges are $a$-$x$, $x$-$y$, $y$-$b$ and $p$-$y$. The path $a, x, y, b$ is 2-colorable, but merging $a$ and $b$ makes a triangle with $x$ and $y$. With $k = 2$, the aggressive coalescing $\{a, b\}$ forces a spill, and an allocator with aggressive coalescing spills $y$: one store and two loads instead of one copy. The conservative answer is to keep the copy.

## Known algorithms

- **Aggressive coalescing** ([Chaitin's allocator](/chaitin-register-allocation/)): merge the ends of every copy that do not interfere, then rebuild the graph, and repeat. It removes many copies and can cause spills.
- **Conservative coalescing** ([conservative coalescing](/conservative-coalescing/)): merge only when the Briggs test or the George test proves that the merge keeps the $k$-core empty. Briggs, Cooper and Torczon (1994) ran it before coloring.
- **[Iterated register coalescing](/iterated-register-coalescing/)** (George and Appel, 1996): interleave conservative merges with simplify steps, which lower degrees and let more merges pass.
- **Optimistic coalescing** (Park and Moon): merge aggressively, and undo merges at select time when a merged vertex finds no color.
- **Biased coloring**: no merge at all. When select can choose among several colors, it prefers the color of a copy partner.
- **SSA-based allocation** ([SSA-based register allocation](/ssa-based-register-allocation/)): color the chordal graph of an SSA program first, after spilling has brought the number of live values down to $k$, then change colors to make copy partners equal, which keeps the coloring valid at each step.

## Bounds

- Aggressive coalescing is NP-complete, by the reduction below. Bouchez, Darte and Rastello (2007) proved that it stays NP-complete even when the interference graph is chordal or greedy-3-colorable.
- Conservative coalescing is NP-complete (Bouchez, Darte and Rastello, 2007).
- Incremental conservative coalescing is NP-complete when the condition is $k$-colorability, and polynomial when the graph is chordal. For greedy-$k$-colorable graphs, Bouchez, Darte and Rastello (2007) left its complexity open.
- Optimistic coalescing is NP-complete, even for chordal graphs with $k = 4$ (Bouchez, Darte and Rastello, 2007).
- At most $|A|$ copies can be removed, and every affinity whose ends interfere stays.

## Reductions

**$k$-coloring reduces to aggressive coalescing.** Given a graph $H$ with $n$ vertices and a number $k$, build $G$ from $H$ by adding a clique of $k$ new vertices $c_1, \ldots, c_k$ with no edge to $H$. Add an affinity of weight 1 between each vertex $v$ of $H$ and each $c_i$. Then some coalescing of $G$ coalesces $n$ affinities if and only if $H$ is $k$-colorable.

*Proof.* The $c_i$ are pairwise adjacent, so they are in different classes, and each vertex $v$ is in the class of at most one $c_i$. So $v$ gives at most one coalesced affinity, and $n$ affinities are coalesced exactly when each $v$ is in the class of some $c_i$. If that holds, set the color of $v$ to $i$: two adjacent vertices of $H$ cannot share a class, so this is a $k$-coloring of $H$. Conversely, a $k$-coloring $\chi$ of $H$ gives the classes $\{c_i\} \cup \chi^{-1}(i)$, which contain no edge of $G$ and coalesce all $n$ affinities. $\square$

The construction is polynomial, and a coalescing is a certificate that can be checked in polynomial time, so aggressive coalescing is NP-complete for every fixed $k \ge 3$ ([three-coloring](/three-coloring/)). The clique $c_1, \ldots, c_k$ plays the role of $k$ precolored machine registers.

For the conservative condition "$G_f$ is $k$-colorable", hardness is immediate: with $A = \emptyset$, the question is whether $G$ is [$k$-colorable](/k-coloring/).

## Applications

- **Leaving SSA form.** [Out-of-SSA translation](/out-of-ssa-translation/) replaces each $\phi$-function by copies on the incoming edges. Most of them can be coalesced, so that the copies cost nothing.
- **Live range splitting.** [Live range splitting](/live-range-splitting/) adds copies between the pieces of a value. Coalescing removes the copies where the split was not needed.
- **Calling conventions and two-address instructions.** Arguments and results must be in fixed registers, and some machines have instructions whose result register must be the same as one operand. The copies that this adds are affinities with precolored vertices.
- **[Copy propagation](/copy-propagation/)** removes some copies before allocation, but not the copies that SSA destruction makes on edges or that the machine requires.

## References
