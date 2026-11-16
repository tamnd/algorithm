---
tag: Y54EPM
kind: definition
slug: meet-over-all-paths-solution
name: Meet-over-all-paths solution
aliases:
- MOP solution
- merge over all paths
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: The meet, over all paths from the entry to a point, of the composed transfer functions of the path, which is the ideal dataflow answer.
prereqs: [monotone-dataflow-framework]
see_also: [maximal-fixed-point-solution, mop-mfp-coincidence-theorem, distributive-dataflow-framework, worklist-dataflow-algorithm, constant-propagation-problem, ifds-framework, collecting-semantics, undecidability]
sources:
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the whole paper (the meet over all paths to a node as the meaning of a solution, and the proof that the iterative algorithm reaches it for distributive functions)
  - paper: doi:10.1007/BF00290339
    title: "John B. Kam and Jeffrey D. Ullman, Monotone data flow analysis frameworks, Acta Informatica 7(3), 1977, 305-317"
    locator: the whole paper (the MOP solution of a monotone framework, MFP below MOP, and the proof that no algorithm computes the MOP solution of every instance of every monotone framework)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.3.4 (Meaning of a Data-Flow Solution, the ideal solution, the meet-over-paths solution and the maximum fixed point)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Section 2.4 (Equation Solving, the MOP solution and its relation to the MFP solution), stated with a join
---

The meet-over-all-paths (MOP) solution of a [dataflow analysis](/dataflow-analysis/) gives each program point the meet, over every path in the [control flow graph](/control-flow-graph/) from the start to that point, of the fact that the path produces. It treats each path on its own and merges only at the end, so it is the most precise answer that an analysis can give when it assumes that every CFG path can run. It is the yardstick for the computed answer, the [maximal fixed-point solution](/maximal-fixed-point-solution/): in every [monotone dataflow framework](/monotone-dataflow-framework/) MFP $\sqsubseteq$ MOP, and in a [distributive dataflow framework](/distributive-dataflow-framework/) the two are equal. A loop gives infinitely many paths, and Kam and Ullman (1977) proved that no algorithm computes MOP for every monotone framework.

## Definition

The dataflow pages use the meet convention: $(L, \sqcap)$ is a meet semilattice, $x \sqsubseteq y$ means $x \sqcap y = x$, $\top$ is the identity of meet, and the height $h$ is finite. Lower facts are weaker, safer claims.

**The instance.** A [control flow graph](/control-flow-graph/) $G = (V, E)$ with an entry block, a transfer function $f_B : L \to L$ for each block, and a boundary value $\iota \in L$ that holds at the start of the entry.

**Paths and path functions.** A path to $B$ is a sequence of blocks $\pi = (B_0, B_1, \ldots, B_k)$ with $B_0$ the entry, $B_k = B$, and an edge from each block to the next. Its function applies the blocks before $B$ in order:

$$f_\pi = f_{B_{k-1}} \circ \cdots \circ f_{B_1} \circ f_{B_0},$$

and $f_\pi$ is the identity for the path $(B_0)$ of length zero. The fact that $\pi$ produces at the start of $B$ is $f_\pi(\iota)$.

**Definition.** For each block $B$,

$$\mathrm{MOP}[B] = \mathop{\large\sqcap}_{\pi \in \mathrm{Paths}(B)} f_\pi(\iota),$$

where $\mathrm{Paths}(B)$ is the set of paths to $B$. The value at the end of $B$ uses the paths that go through $B$ itself: $\mathrm{MOP}_{\mathrm{out}}[B] = \mathop{\large\sqcap}_{\pi} f_B(f_\pi(\iota))$. For a backward problem, the paths run from the end of a block to the end of a `ret` block, on the reverse CFG, and $\iota$ holds after each `ret` block.

**The meet exists.** A loop makes $\mathrm{Paths}(B)$ infinite, so the meet needs care. In a semilattice of finite height $h$ with a top, every set $S$ has a greatest lower bound, and when $S$ is not empty it is the meet of at most $h + 1$ members of $S$. *Proof.* Start with any $c \in S$. While some $s \in S$ has $c \sqcap s \ne c$, replace $c$ with $c \sqcap s$; each replacement goes strictly down, so there are at most $h$. At the end $c \sqsubseteq s$ for all $s \in S$, and every lower bound of $S$ is below the members used and hence below $c$. The empty set has meet $\top$. $\square$ So $\mathrm{MOP}[B]$ is well defined, and it is $\top$ exactly when no path reaches $B$ or all paths give $\top$.

**MOP is the ideal answer for CFG paths.** Assume each $f_B$ is *safe*: if a fact $x$ describes the state at the start of $B$, then $f_B(x)$ describes the state at the end, and a lower fact describes every state that a higher one describes. A run that reaches $B$ follows some path $\pi \in \mathrm{Paths}(B)$, so by induction along $\pi$ the fact $f_\pi(\iota)$ describes its state at $B$, and so does the lower fact $\mathrm{MOP}[B]$. This is soundness. Conversely, any answer at $B$ that is safe for every path taken on its own must be below each $f_\pi(\iota)$, so below their meet. MOP is the greatest such answer. It can still be below the truth, because some CFG paths are never run.

**Precision with an example.** For [constant propagation](/constant-propagation-problem/) on the diamond below, the two paths to `join` give $(x, y) = (2, 3)$ and $(3, 2)$, and the function of `join` gives $z = 5$ on each, so $\mathrm{MOP}_{\mathrm{out}}[\mathrm{join}]$ has $z = 5$. The maximal fixed point merges $x$ and $y$ at the start of `join` first and gets "not a constant" for $z$.

```
entry:
  br c left right
left:
  x = 2
  y = 3
  jump join
right:
  x = 3
  y = 2
  jump join
join:
  z = x + y
  ret z
```

**Relation to the fixed point.** In every monotone framework, every solution of the dataflow equations is below MOP at every block, and in particular MFP $\sqsubseteq$ MOP; the proof is on the [maximal fixed-point solution](/maximal-fixed-point-solution/) page. If the functions are distributive and every block is reachable, MOP itself solves the equations, so MFP = MOP; the proof is on the [distributive dataflow framework](/distributive-dataflow-framework/) page, and the [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/) states it.

**Cost and computability.**

- *Acyclic CFG.* The paths are finite in number, so MOP is computable by enumeration. Their number can be exponential: a chain of $k$ diamonds has $2^k$ paths from the first block to the last.
- *Distributive frameworks.* MOP = MFP, and a worklist solver finds it with $O(n h)$ transfer functions and $O(m h)$ meets on $n$ blocks and $m$ edges.
- *Finite lattices.* If $L$ has finitely many elements, MOP is computable for any monotone framework. Solve the problem on sets of facts instead: the fact at a point is the set $R[B] \subseteq L$ of values $f_\pi(\iota)$ over paths to $B$, with $R[\mathrm{entry}] \ni \iota$, union as the merge, and $f_B$ applied to each element. This lifted problem is distributive over union and has height at most $|L|$, so iteration finds the exact sets, and $\mathrm{MOP}[B] = \mathop{\large\sqcap} R[B]$. The cost grows with $|L|$, which is usually huge.
- *Infinite lattices of finite height.* Kam and Ullman (1977) showed that no algorithm computes MOP for every instance of every monotone framework. Constant propagation is of this kind: its lattice is infinite, so the method for finite lattices does not apply. This is why analyses compute MFP.

## Examples and non-examples

**Live variables on the running example.** The loop of the running example of [dataflow analysis](/dataflow-analysis/) gives infinitely many paths from each block to `done`. Live variables is distributive, so MOP equals the MFP shown on the [live variable analysis](/live-variable-analysis/) page; for instance $\mathrm{MOP}[\mathrm{entry}] = \{n, x\}$. By the lemma above, a finite number of these paths already gives the whole meet.

**An unreachable block.** If no path reaches $B$, then $\mathrm{MOP}[B] = \top$, the empty meet: every claim holds vacuously, since no run gets there. MFP need not agree: in a may problem an unreachable block that generates a fact still sends it to its successors in every solution of the equations, while MOP does not count it.

**Non-example: the meet over runs.** The meet over the paths that some input actually follows is more precise than MOP, as in the example of two branches on the same condition. But deciding which paths can run is undecidable in general, by [Rice's theorem](/rice-theorem/), so this is not a definition that any analysis can compute; MOP is the ideal relative to the CFG.

**Non-example: the meet over valid paths.** Across procedures, a CFG path that enters a callee from one call site and returns to another call site is not a real path. The interprocedural ideal is the meet over valid paths only, with matched calls and returns. The [IFDS framework](/ifds-framework/) computes it exactly for distributive problems over finite sets.

## Related definitions

- [Maximal fixed-point solution](/maximal-fixed-point-solution/): the greatest solution of the equations, what iterative solvers compute.
- [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/): MFP = MOP for distributive frameworks.
- [Distributive dataflow framework](/distributive-dataflow-framework/) and [monotone dataflow framework](/monotone-dataflow-framework/): the classes of problems.
- [Collecting semantics](/collecting-semantics/): the set of all states at each point, of which MOP is an abstraction that treats paths separately.
- [Undecidability](/undecidability/): why neither the meet over runs nor, for some monotone frameworks, the meet over CFG paths can be computed.

## References
