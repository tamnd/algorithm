---
tag: 1SRBV4
kind: theorem
slug: ssa-chordal-interference-theorem
name: Chordality of SSA interference graphs
aliases:
- Hack-Grund-Goos theorem
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: The interference graph of a strict SSA program is chordal, so it is colored optimally in polynomial time and its clique size gives the bound.
prereqs: [static-single-assignment-form, interference-graph, dominator-tree, chordal-graph, perfect-elimination-ordering]
see_also: [ssa-based-register-allocation, chordal-graph-coloring, register-allocation-problem, register-allocation-np-completeness, out-of-ssa-translation, linear-scan-register-allocation, ssa-linear-scan, perfect-graph]
sources:
  - paper: doi:10.1007/11688839_20
    title: Sebastian Hack, Daniel Grund and Gerhard Goos, Register allocation for programs in SSA-form, Compiler Construction (CC 2006), LNCS 3923, Springer, 2006, 247-262
    locator: the lemma that the definition of a name live at a point dominates that point, the lemma that the definitions of two interfering names are ordered by dominance, and the theorem that the interference graph of a strict SSA program is chordal
  - paper: doi:10.1016/j.ipl.2006.01.008
    title: Sebastian Hack and Gerhard Goos, Optimal register allocation for SSA-form programs in polynomial time, Information Processing Letters 98(4), 2006, 150-155
    locator: the constructive proof that the definitions in a dominance order give a perfect elimination order, and the coloring with the register pressure as the number of colors
  - url: http://iwls.org/iwls2005/program.html
    title: Philip Brisk, Foad Dabiri, Jamie Macbeth and Majid Sarrafzadeh, Polynomial time graph coloring register allocation, 14th International Workshop on Logic and Synthesis (IWLS 2005), June 2005, 447-454
    locator: the independent proof that the interference graphs of SSA programs are chordal, in the setting of high-level synthesis (the link is the workshop program)
  - paper: doi:10.1007/978-3-540-72521-3_21
    title: Florent Bouchez, Alain Darte, Christophe Guillon and Fabrice Rastello, Register allocation, what does the NP-completeness proof of Chaitin et al. really prove? Or revisiting register allocation, why and how, LCPC 2006, LNCS 4382, Springer, 2007, 283-298
    locator: the third independent proof of chordality under strict SSA, and what it means for the complexity of spilling and coalescing
  - paper: doi:10.1007/11690634_6
    title: Fernando Magno Quintão Pereira and Jens Palsberg, Register allocation after classical SSA elimination is NP-complete, FoSSaCS 2006, LNCS 3921, Springer, 2006
    locator: the proof that coloring the interference graph after the classical replacement of phis by copies is NP-complete
  - paper: doi:10.1007/11575467_21
    title: Fernando Magno Quintão Pereira and Jens Palsberg, Register allocation via coloring of chordal graphs, APLAS 2005, LNCS 3780, Springer, 2005, 315-329
    locator: the observation that most interference graphs of Java methods are chordal, and an allocator built on that
---

The chordality theorem for SSA says that the [interference graph](/interference-graph/) of a program in strict [SSA form](/static-single-assignment-form/) is a [chordal graph](/chordal-graph/). The definitions of the names, listed in an order that respects [dominance](/dominator-tree/) and read backward, form a [perfect elimination ordering](/perfect-elimination-ordering/). So the graph is colored with the fewest colors by a greedy pass, and that number equals the largest number of names live at one point. Coloring an arbitrary interference graph is NP-hard, so SSA form moves the hard part of register allocation out of coloring and into spilling and copies. The result was found in 2005 by three groups independently, and it is the basis of [SSA-based register allocation](/ssa-based-register-allocation/).

## Statement

**The program model.** A program is a control flow graph with an entry block. Each block holds phis, then ordinary instructions, then a terminator. We work on the *item graph* $H$: its nodes are one node $\epsilon$ that defines the parameters, one node $\varphi_B$ per block $B$ with phis, which defines all phis of $B$ at once, one node per ordinary instruction and one per terminator. The edges go from $\epsilon$ to the first node of the entry block, from each node to the next one in its block, and from the terminator of a block to the first node of each successor block. A phi operand $a$ of $B$ for the predecessor $P$ is read by the terminator node of $P$. Write $\mathrm{def}(v)$ and $\mathrm{use}(v)$ for the names that node $v$ defines and reads. Dominance is taken in $H$ from $\epsilon$.

**Strict SSA.** Each name $x$ is defined by exactly one node $d_x$, and $d_x$ strictly dominates every node that reads $x$.

**Liveness and interference.** A name $x$ is *live in* at $v$ if some path $v = v_0, v_1, \ldots, v_m$ in $H$ has $x \in \mathrm{use}(v_m)$ and $x \notin \mathrm{def}(v_i)$ for $i < m$. It is *live out* at $v$ if it is live in at some successor of $v$. Two different names $x$ and $y$ *interfere* if some node $v$ has $x \in \mathrm{def}(v)$ and $y \in \mathrm{def}(v) \cup \mathrm{out}(v)$, where $\mathrm{out}(v)$ is the live-out set, or the same with $x$ and $y$ exchanged. This is the rule of the interference graph page without its exception for copies. Let

$$\mathrm{MaxLive} = \max_v \, |\mathrm{def}(v) \cup \mathrm{out}(v)|,$$

the largest number of names that hold a value just after some node.

**Theorem.** Let $P$ be a program in strict SSA form, let $G$ be its interference graph, and let $\sigma$ list the names by their defining nodes in a preorder of the dominator tree of $H$, with the names of one node in any order. Then:

1. $\sigma$ read backward is a perfect elimination ordering of $G$, so $G$ is chordal.
2. $\omega(G) = \chi(G) = \mathrm{MaxLive}$: the largest clique, the [chromatic number](/chromatic-number/) and the register pressure are equal.
3. Coloring the names in the order $\sigma$, each with the lowest color not used by its colored neighbors, uses exactly $\mathrm{MaxLive}$ colors.

## In plain words

In SSA form each value is written in one place, and that place comes before every read of the value on every path. So if two values are alive at the same moment, the one written first was already alive when the second was written. Now walk through the program in the order the dominator tree gives, and give each value a register when it is written. The values that already have a register and clash with the new one are all alive at the point where it is written, and they all clash with each other. So the new value has as many clashing values as there are values alive at that point, minus itself. That means the number of registers needed is exactly the largest number of values alive at once, and a simple greedy pass finds such an assignment.

## Proof

**Lemma 1 (a live name is dominated by its definition).** If $x$ is live in at $v$, then $d_x$ strictly dominates $v$. If $x \in \mathrm{def}(v) \cup \mathrm{out}(v)$, then $d_x$ dominates $v$.

*Proof.* Let $v = v_0, \ldots, v_m$ be the path in the definition, with $x \in \mathrm{use}(v_m)$. By strictness $d_x \ne v_m$, and $x \notin \mathrm{def}(v_i)$ for $i < m$, so no node of the path is $d_x$. If $d_x$ did not dominate $v$, a path from $\epsilon$ to $v$ that avoids $d_x$, followed by this path, would reach $v_m$ without passing $d_x$. That is false, because $d_x$ dominates $v_m$. So $d_x$ dominates $v$, and $d_x \ne v = v_0$. For the second claim, $x \in \mathrm{def}(v)$ means $d_x = v$. If $x \in \mathrm{out}(v) \setminus \mathrm{def}(v)$, then $x$ is live in at a successor of $v$ and $v$ does not define it, so $x$ is live in at $v$. $\square$

**Lemma 2 (live after a later definition).** Let $d_y$ strictly dominate a node $u$, and let $y$ be live in at $u$. If $d_y$ strictly dominates $d_z$ and $d_z$ dominates $u$, then $y \in \mathrm{out}(d_z)$.

*Proof.* Take any path $\pi$ from $\epsilon$ to $u$. It passes $d_y$; let $\pi'$ be the part after the last visit of $d_y$. Suppose $\pi'$ does not pass $d_z$. Since $d_y$ strictly dominates $d_z$, $d_z$ does not dominate $d_y$, so some path from $\epsilon$ to $d_y$ avoids $d_z$. That path followed by $\pi'$ reaches $u$ without $d_z$, which is false. So $\pi'$ passes $d_z$, and the part of $\pi'$ from $d_z$ to $u$ does not pass $d_y$. Follow it with the path that makes $y$ live in at $u$. The result starts at the successor of $d_z$ on $\pi'$, reads $y$ at its end, and has no definition of $y$ before that read. So $y$ is live in at that successor, and $y \in \mathrm{out}(d_z)$. $\square$

**Lemma 3 (one point gives a clique).** For each node $v$, any two different names in $\mathrm{def}(v) \cup \mathrm{out}(v)$ interfere.

*Proof.* Let $y \ne z$ be in the set. If one of them is in $\mathrm{def}(v)$, the rule of interference applies at $v$. Otherwise both are in $\mathrm{out}(v) \setminus \mathrm{def}(v)$, so both are live in at $v$, and by Lemma 1 both $d_y$ and $d_z$ strictly dominate $v$. The dominators of a node lie on one path of the dominator tree, so they are ordered: say $d_y$ dominates $d_z$. If $d_y = d_z$, the rule applies at that node. Otherwise Lemma 2 with $u = v$ gives $y \in \mathrm{out}(d_z)$, and $z \in \mathrm{def}(d_z)$, so the rule applies at $d_z$. $\square$

**Lemma 4 (earlier neighbors are live at the definition).** If $x$ and $y$ interfere and $y$ comes before $x$ in $\sigma$, then $y \in \mathrm{def}(d_x) \cup \mathrm{out}(d_x)$.

*Proof.* By the rule, some node $v$ defines one of them while the other is in $\mathrm{def}(v) \cup \mathrm{out}(v)$. If $v$ defines $x$, then $v = d_x$ and we are done. Otherwise $v = d_y$ and $x \in \mathrm{def}(d_y) \cup \mathrm{out}(d_y)$. If $x \in \mathrm{def}(d_y)$, then $d_x = d_y$ and $y \in \mathrm{def}(d_x)$. If $x \in \mathrm{out}(d_y) \setminus \mathrm{def}(d_y)$, then $x$ is live in at $d_y$, so by Lemma 1 $d_x$ strictly dominates $d_y$. A preorder of the dominator tree lists a strict dominator first, so $x$ would come before $y$ in $\sigma$, which is false. $\square$

*Proof of the theorem.* Fix a name $x$ and let $N^-(x)$ be its neighbors that come before it in $\sigma$. By Lemma 4, $N^-(x) \cup \{x\} \subseteq \mathrm{def}(d_x) \cup \mathrm{out}(d_x)$, and by Lemma 3 that set is a clique. So the neighbors of $x$ that come after it in $\sigma$ read backward form a clique, which is the definition of a perfect elimination ordering. A graph with a perfect elimination ordering is chordal (Fulkerson and Gross). This is part 1.

For parts 2 and 3, Lemma 3 says that each set $\mathrm{def}(v) \cup \mathrm{out}(v)$ is a clique, so $\omega(G) \ge \mathrm{MaxLive}$. The greedy coloring in the order $\sigma$ gives $x$ the lowest color not used by $N^-(x)$. Since $|N^-(x)| \le |\mathrm{def}(d_x) \cup \mathrm{out}(d_x)| - 1 \le \mathrm{MaxLive} - 1$, that color is below $\mathrm{MaxLive}$. With $\omega(G) \le \chi(G)$ for every graph, we get

$$\mathrm{MaxLive} \le \omega(G) \le \chi(G) \le \mathrm{MaxLive}. \qquad \square$$

The live-in sets give nothing larger. The node $\epsilon$ has no live-in name by Lemma 1, and every other node $v$ has a predecessor $u$ with $\mathrm{in}(v) \subseteq \mathrm{out}(u)$. So $\mathrm{MaxLive}$ is also the largest number of names live at any point between two nodes, when a name that is defined and never read counts at the point just after its definition.

## Consequences

- **Allocation is easy once the pressure is low.** If $\mathrm{MaxLive} \le k$, the strict SSA program can be colored with $k$ registers, and the greedy pass of part 3 finds the coloring in time linear in the size of the graph, or without the graph by walking the dominator tree. This is the coloring phase of [SSA-based register allocation](/ssa-based-register-allocation/).
- **Spilling and coloring come apart.** To make a strict SSA program fit into $k$ registers, it is enough to lower the pressure to $k$ at every point. No coloring step can then fail, so there is no loop of spill and color as in [Chaitin's allocator](/chaitin-register-allocation/). Choosing the cheapest spills is still NP-hard (Bouchez, Darte and Rastello, 2007), and so is the best coalescing.
- **Clique and coloring by known methods.** Every chordal graph is [perfect](/perfect-graph/), and [chordal graph coloring](/chordal-graph-coloring/) along any perfect elimination ordering is optimal. The dominance order gives such an ordering for free, with no [maximum cardinality search](/maximum-cardinality-search/).
- **Not NP-complete under SSA.** The reduction behind [register allocation NP-completeness](/register-allocation-np-completeness/) builds programs whose interference graphs are arbitrary. Those programs are not in strict SSA form, and the theorem shows they cannot be.

## Tightness

**SSA destruction breaks it.** The theorem needs one definition per name. After [out-of-SSA translation](/out-of-ssa-translation/) replaces the phis by copies, a name has several definitions, and the graph can be any graph. The loop on the [interference graph](/interference-graph/) page has a chordless cycle $a$-$b$-$c$-$d$ of length 4. Pereira and Palsberg (2006) proved that coloring the interference graph after the classical replacement of phis by copies is NP-complete. So an allocator that uses the theorem must color before it leaves SSA form, and then implement the phis with moves between registers.

**The copy exception breaks it.** The interference rule of the [interference graph](/interference-graph/) page skips the source of a copy. That gives a subgraph of $G$, and a subgraph of a chordal graph need not be chordal. In this straight-line strict SSA program

```
  a = p + 1
  b = a + 1
  c = a
  e = b + c
  d = a + c
  f = d + a
  g = f + c
  h = g + e
  ret h
```

the full graph $G$ is chordal, with the edge $a$-$c$. The copy `c = a` removes that edge, and then $a$-$b$-$c$-$d$ is a cycle of length 4 with no chord, since $b$ is dead before $d$ is defined. The coloring of $G$ is still a proper coloring of the subgraph, so $\mathrm{MaxLive} = 4$ colors (the names $a, c, d, e$ just after `d = a + c`) still suffice. The theorem itself needs the full rule.

**Strictness is needed.** If $d_x$ does not dominate a use of $x$, Lemma 1 fails, and two interfering names need not have ordered definitions. In

```
entry:
  br p B1 B2
B1:
  x = 1
  jump B3
B2:
  y = 2
  jump B3
B3:
  br p B4 B5
B4:
  ret x
B5:
  ret y
```

each name has one definition, but `ret x` is not dominated by `x = 1`. The name $y$ is live just after `x = 1` (along `B1`, `B3`, `B5`), so $x$ and $y$ interfere, and neither definition dominates the other. The proof of Lemma 4 no longer applies. The usual fix, a definition such as `y = 0` at the entry, makes the program strict.

**The bound is exact.** Parts 2 and 3 are equalities: a strict SSA program never needs fewer registers than $\mathrm{MaxLive}$, and never more when no name is spilled.

## History

Three groups found the theorem in 2005, each on its own. Brisk, Dabiri, Macbeth and Sarrafzadeh presented it at IWLS 2005 for register sharing in high-level synthesis. Hack, Grund and Goos at Karlsruhe wrote a technical report in 2005 and published the result at CC 2006, with a full allocator built on it; Hack and Goos gave a short constructive proof in Information Processing Letters in 2006. Bouchez, Darte, Guillon and Rastello proved it again and studied what it means for the NP-completeness proof of Chaitin and others, in a paper at LCPC 2006 (published 2007). In the same period Pereira and Palsberg (2005) observed that most interference graphs of Java methods are chordal even without SSA, and (2006) showed that the property is lost again after the classical SSA elimination.

## References
