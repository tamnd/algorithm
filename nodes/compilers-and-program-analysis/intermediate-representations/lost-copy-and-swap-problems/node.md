---
tag: NPG0EA
kind: concept
slug: lost-copy-and-swap-problems
name: Lost-copy and swap problems
aliases:
- lost copy problem
- swap problem
area: compilers-and-program-analysis/intermediate-representations
level: advanced
summary: Two cases where naive phi removal is wrong after copy folding, because phi copies are parallel and live ranges interfere.
prereqs: [out-of-ssa-translation]
see_also: [phi-function, copy-propagation, critical-edge-splitting, sreedhar-cssa-translation, static-single-assignment-form, live-variable-analysis, interference-graph, braun-ssa-construction]
sources:
  - paper: "Preston Briggs, Keith D. Cooper, Timothy J. Harvey and L. Taylor Simpson, Practical improvements to the construction and destruction of static single assignment form, Software: Practice and Experience 28(8), 1998, pages 859-881"
    locator: the lost copy problem and the swap problem, both caused by copy folding, and a translation out of SSA form that avoids them
  - paper: doi:10.1007/3-540-48294-6_13
    title: Vugranam C. Sreedhar, Roy Dz-Ching Ju, David M. Gillies and Vatsa Santhanam, Translating out of static single assignment form, Static Analysis Symposium (SAS 1999), LNCS 1694
    locator: conventional and transformed SSA form, phi congruence classes, and copy insertion that solves both problems without splitting edges
  - paper: doi:10.1109/CGO.2009.19
    title: Benoit Boissinot, Alain Darte, Fabrice Rastello, Benoît Dupont de Dinechin and Christophe Guillon, Revisiting out-of-SSA translation for correctness, code quality, and efficiency, International Symposium on Code Generation and Optimization (CGO 2009), pages 114-125
    locator: phi-functions as parallel copies and their sequentialization with one extra variable
  - book: isbn:9783030805142
    title: Fabrice Rastello and Florent Bouchez Tichadou (editors), SSA-based Compiler Design, Springer, 2022
    locator: Chapter 3 (Standard Construction and Destruction Algorithms), conventional SSA and the replacement of phi-functions by copies; Chapter 21 (SSA Destruction for Machine Code)
---

The lost copy problem and the swap problem are two ways in which a simple [out-of-SSA translation](/out-of-ssa-translation/) produces wrong code. Briggs, Cooper, Harvey and Simpson described both in 1998. The simple translation replaces each [phi-function](/phi-function/) by a copy at the end of each predecessor block. This is correct straight after SSA construction. After [copy propagation](/copy-propagation/) it can fail. In the lost copy problem, a copy at the end of a block also runs when control leaves on another edge, and it destroys a value that is still needed there. In the swap problem, phi-functions that read each other's targets become copies that run one after another, and a later copy reads a value that an earlier copy has already overwritten. Splitting critical edges fixes the first problem but not the second.

## In plain words

A phi-function picks a value according to the edge that control came along. To remove it, the compiler puts a copy on each incoming path, usually at the end of the block that the path leaves. Two things can go wrong. First, that block may have another way out, and the copy runs on that path too. If the old value is still needed there, it is lost. Second, all the phi-functions of one block take their values at the same moment. When two of them exchange values, two plain copies in a row cannot do it: the second copy sees the result of the first. Both mistakes only matter after an optimization has made two related names live at the same time. Before that, the simple method works.

## The idea

**The simple translation.** For each phi-function $x_0 = \phi(x_1, \ldots, x_n)$ of a block $L_0$, put the copy $x_0 \leftarrow x_i$ at the end of the predecessor $L_i$, before its jump, and delete the phi-function. The copy runs every time $L_i$ ends, whichever successor comes next. The copies for several phi-functions of one block run in some order.

**Why it works after construction.** Right after construction, all the names that phi-functions join came from one source variable. Two of them are never live at the same time, because the source program had only one variable to hold them. Sreedhar, Ju, Gillies and Santhanam (1999) call this *conventional SSA form*. The simple translation is then just the source program again.

**Why it fails after copy folding.** Copy propagation and the removal of trivial phi-functions replace one name by another. This extends the live range of a name over a definition of a related name, and the program is in *transformed SSA form*. Then two names of the same phi congruence class are live at the same time, and a copy into one destroys the other. Both problems are cases of this.

**The lost copy.** The copy $x_0 \leftarrow x_i$ at the end of $L_i$ is wrong when $x_0$ is live at the end of $L_i$ on an edge other than the one to $L_0$. Then $L_i$ has at least two successors. $L_0$ has a phi-function, so it has at least two predecessors, and the edge $(L_i, L_0)$ is critical. The fixes are:

- [split the critical edge](/critical-edge-splitting/) and put the copy in the new block, so that it runs only on that edge;
- or copy the phi target to a new name at the top of $L_0$, as in [Sreedhar's translation](/sreedhar-cssa-translation/), so that the copy at the end of $L_i$ writes a name that is dead on the other edge.

**The swap.** The phi-functions of one block act as one *parallel copy*: on an edge, they first read all their operands and then write all their targets. When one phi-function reads the target of another, the order of the copies matters. When the reads form a cycle, as in $a \leftarrow b$ and $b \leftarrow a$, no order is right. The edge does not have to be critical, so edge splitting does not help. The fix is to sequentialize the parallel copy properly. Emit first a copy whose target no other pending copy still reads. When only cycles are left, save one value in a temporary: $t \leftarrow a$, $a \leftarrow b$, $b \leftarrow t$. Sreedhar's translation avoids the cycle in another way: it copies each resource into a fresh name, so no copy overwrites a name that another copy reads.

## Examples

**The lost copy.** This loop keeps the value of `x` from the start of the last pass in `y.1`:

```
# params: n                          # params: n
B1:                                  B1:
  x.1 = 1                              x.1 = 1
  jump B2                              jump B2
B2:                                  B2:
  x.2 = phi [B1: x.1, B2: x.3]         x.2 = phi [B1: x.1, B2: x.3]
  y.1 = x.2                            x.3 = x.2 + 1
  x.3 = x.2 + 1                        t.1 = x.3 < n
  t.1 = x.3 < n                        br t.1 B2 B3
  br t.1 B2 B3                       B3:
B3:                                    ret x.2
  ret y.1
```

On the left is the program after construction. Copy propagation replaces `y.1` by `x.2` and gives the program on the right. Both return 2 for $n = 3$. On the left, `x.2` is dead after the add, so the simple translation is correct. On the right, B3 reads `x.2`, so it is live after the definition of `x.3`, and the two names of one class interfere. The simple translation gives:

```
# params: n
B1:
  x.1 = 1
  x.2 = x.1
  jump B2
B2:
  x.3 = x.2 + 1
  t.1 = x.3 < n
  x.2 = x.3
  br t.1 B2 B3
B3:
  ret x.2
```

The copy `x.2 = x.3` also runs when the loop exits, so B3 returns the new value. For $n = 3$ the result is 3, not 2. The edge from B2 back to B2 is critical. With a new block B4 on that edge, which holds `x.2 = x.3` and jumps to B2, the result is 2 again.

**The swap.** This loop exchanges `a` and `b` $n$ times through a temporary `t.1`:

```
# params: n                          # params: n
B1:                                  B1:
  a.1 = 1                              a.1 = 1
  b.1 = 2                              b.1 = 2
  i.1 = 0                              i.1 = 0
  jump B2                              jump B2
B2:                                  B2:
  a.2 = phi [B1: a.1, B3: a.3]         a.2 = phi [B1: a.1, B3: b.2]
  b.2 = phi [B1: b.1, B3: b.3]         b.2 = phi [B1: b.1, B3: a.2]
  i.2 = phi [B1: i.1, B3: i.3]         i.2 = phi [B1: i.1, B3: i.3]
  c.1 = i.2 < n                        c.1 = i.2 < n
  br c.1 B3 B4                         br c.1 B3 B4
B3:                                  B3:
  t.1 = a.2                            i.3 = i.2 + 1
  a.3 = b.2                            jump B2
  b.3 = t.1                          B4:
  i.3 = i.2 + 1                        r.1 = a.2 * 10
  jump B2                              r.2 = r.1 + b.2
B4:                                    ret r.2
  r.1 = a.2 * 10
  r.2 = r.1 + b.2
  ret r.2
```

Copy folding removes the three copies in B3 and moves the swap into the phi-functions, on the right. Both programs return 21 for $n = 1$ and 12 for $n = 2$. The simple translation of the right one puts these copies at the end of B3:

```
B3:
  i.3 = i.2 + 1
  a.2 = b.2
  b.2 = a.2
  i.2 = i.3
  jump B2
```

After `a.2 = b.2`, the copy `b.2 = a.2` reads the new value, so both names hold 2. For $n = 1$ the result is 22, not 21, and every larger $n$ also gives 22. B3 has only one successor, so the edge from B3 to B2 is not critical, and splitting it changes nothing. With `t = a.2` before the two copies and `b.2 = t` in place of `b.2 = a.2`, the results are right again.

## Where it is used

- **Out-of-SSA translation.** Every translation that runs after optimization must handle both problems. Briggs et al. (1998) use liveness to find the copies that would destroy a live value, and order the copies with temporaries for cycles. [Sreedhar's translation](/sreedhar-cssa-translation/) adds copies until the program is conventional, without splitting edges. Boissinot et al. (2009) treat the copies of each edge as one parallel copy and sequentialize it with one extra variable.
- **Choosing optimizations.** A compiler that builds SSA form with copy folding, as the [Braun construction](/braun-ssa-construction/) can, produces transformed SSA form from the start. So its out-of-SSA pass must not be the simple one.
- **Register allocation.** The same issues return when an SSA-based register allocator turns phi-functions into moves between registers. The moves of one edge form a parallel copy, and a swap of two registers needs a free register or a swap instruction.
- **Testing.** The two programs above are small regression tests for any out-of-SSA pass.

## References
