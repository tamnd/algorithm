---
tag: F192NH
kind: definition
slug: maximal-fixed-point-solution
name: Maximal fixed-point solution
aliases:
- MFP solution
- maximum fixed point
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: The greatest solution of the dataflow equations of a monotone framework, which iterative algorithms compute and which is below the MOP.
prereqs: [monotone-dataflow-framework, meet-over-all-paths-solution, knaster-tarski-theorem]
see_also: [worklist-dataflow-algorithm, meet-over-all-paths-solution, mop-mfp-coincidence-theorem, distributive-dataflow-framework, kleene-fixed-point-theorem, fixed-point-iteration, kam-ullman-iteration-bound, abstract-interpretation]
sources:
  - paper: doi:10.1007/BF00290339
    title: "John B. Kam and Jeffrey D. Ullman, Monotone data flow analysis frameworks, Acta Informatica 7(3), 1977, 305-317"
    locator: the whole paper (the maximal fixed point of a monotone framework, the proof that Kildall's algorithm computes it, and the proof that it is below the meet over all paths)
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the whole paper (the iterative algorithm from the top element, and its result for distributive functions)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.3.3 (The Iterative Algorithm for General Frameworks) and Section 9.3.4 (Meaning of a Data-Flow Solution, the maximum fixedpoint and its relation to the meet-over-paths solution)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Section 2.4 (Equation Solving, the worklist algorithm for the MFP solution and the comparison with the MOP solution), in the join convention where the same solution is the least one
---

The maximal fixed-point (MFP) solution of a dataflow problem is the greatest solution of its dataflow equations. It is what iterative solvers such as the [worklist dataflow algorithm](/worklist-dataflow-algorithm/) compute: start every value at $\top$, the most optimistic fact, and lower values until the equations hold. In every [monotone dataflow framework](/monotone-dataflow-framework/) the MFP solution exists, is unique, is reached by iteration, and is below the ideal [meet-over-all-paths solution](/meet-over-all-paths-solution/), so it is safe. In a [distributive dataflow framework](/distributive-dataflow-framework/) it equals MOP. "Maximal" means greatest in the meet order used by Kildall, Kam and Ullman, and the dragon book. Turning the order upside down gives the convention of [abstract interpretation](/abstract-interpretation/) and of Nielson, Nielson and Hankin, where the same solution is the least fixed point and the start value is $\bot$.

## Definition

The dataflow pages use the meet convention. $(L, \sqcap)$ is a meet semilattice: $\sqcap$ is idempotent, commutative and associative, and $x \sqsubseteq y$ means $x \sqcap y = x$, a partial order (reflexive, antisymmetric, transitive) in which $x \sqcap y$ is the greatest lower bound. $\top$ is the identity of meet. The height $h$ is the largest number of strict steps in a chain $x_0 \sqsupset x_1 \sqsupset \cdots$, and it is finite. Lower facts are weaker, safer claims.

**The equations as one function.** Take a forward instance on a [control flow graph](/control-flow-graph/) with blocks $V$, $|V| = n$, $m$ edges, transfer functions $f_B$ that are monotone, and boundary value $\iota$ at the entry. An *assignment* gives each block a value $X[B] \in L$, the fact at its start. Assignments are ordered block by block: $X \sqsubseteq Y$ if $X[B] \sqsubseteq Y[B]$ for all $B$. Define

$$F(X)[B] = \Big(\iota \text{ if } B \text{ is the entry}\Big) \sqcap \mathop{\large\sqcap}_{(P, B) \in E} f_P(X[P]),$$

with the empty meet equal to $\top$. A *solution* of the dataflow equations is an $X$ with $X = F(X)$, a [fixed point](/fixed-point/) of $F$. The facts at the ends of the blocks are then $f_B(X[B])$. A backward instance is the same on the reverse CFG, with $\iota$ after each `ret` block.

**Definition.** The *maximal fixed-point solution* is the greatest fixed point of $F$: the solution $\mathrm{MFP}$ with $X \sqsubseteq \mathrm{MFP}$ for every solution $X$.

**Facts about $F$.** $F$ is monotone, because each $f_P$ is monotone and the meet is monotone in each argument. The assignments form a semilattice of height $n h$, since a strict step lowers at least one of the $n$ entries, and each entry can fall at most $h$ times.

**Existence, uniqueness and iteration.** Let $X_0 = \top$ (every entry $\top$) and $X_{i+1} = F(X_i)$. Then:

1. *The sequence goes down.* $X_1 \sqsubseteq \top = X_0$. If $X_{i+1} \sqsubseteq X_i$, then $X_{i+2} = F(X_{i+1}) \sqsubseteq F(X_i) = X_{i+1}$ by monotonicity.
2. *It stops.* A strict step can happen at most $n h$ times, so $X_{k+1} = X_k$ for some $k \le n h$. Then $X_k$ is a fixed point.
3. *It is the greatest.* Let $Y$ be any assignment with $Y \sqsubseteq F(Y)$, in particular any fixed point. Then $Y \sqsubseteq X_0$, and if $Y \sqsubseteq X_i$ then $Y \sqsubseteq F(Y) \sqsubseteq F(X_i) = X_{i+1}$. So $Y \sqsubseteq X_k$.

So $\mathrm{MFP} = X_k$ exists, it is unique (two greatest elements are equal by antisymmetry), and it is also the greatest $Y$ with $Y \sqsubseteq F(Y)$. $\square$ This is the dual of [Kleene's fixed-point theorem](/kleene-fixed-point-theorem/); with $\top$ and finite height, $L$ and the assignments form complete lattices, and the [Knaster-Tarski theorem](/knaster-tarski-theorem/) gives the same greatest fixed point as the join of all $Y$ with $Y \sqsubseteq F(Y)$.

**MFP is below MOP.** For every block $B$, $\mathrm{MFP}[B] \sqsubseteq \mathrm{MOP}[B]$.

*Proof.* Let $X$ be any assignment with $X \sqsubseteq F(X)$. We show $X[B] \sqsubseteq f_\pi(\iota)$ for every path $\pi$ from the entry to $B$, by induction on the length of $\pi$. If $\pi$ has length zero, $B$ is the entry, and $X[B] \sqsubseteq F(X)[B] \sqsubseteq \iota = f_\pi(\iota)$. Otherwise $\pi$ is a path $\pi'$ to some $P$ followed by the edge $(P, B)$, and $f_\pi = f_P \circ f_{\pi'}$. Then

$$X[B] \sqsubseteq F(X)[B] \sqsubseteq f_P(X[P]) \sqsubseteq f_P(f_{\pi'}(\iota)) = f_\pi(\iota),$$

using the induction hypothesis $X[P] \sqsubseteq f_{\pi'}(\iota)$ and the monotonicity of $f_P$. So $X[B]$ is a lower bound of all $f_\pi(\iota)$, and hence below their meet $\mathrm{MOP}[B]$. Take $X = \mathrm{MFP}$. $\square$

**Soundness.** If every $f_B$ is a safe description of its block, then every run that reaches $B$ follows a path $\pi$, the fact $f_\pi(\iota)$ describes its state there, and the lower facts $\mathrm{MOP}[B]$ and $\mathrm{MFP}[B]$ describe it too. The proof uses only monotonicity.

**Precision, with an example.** MFP merges facts at every join before it applies the next function, while MOP applies the functions along each path and merges only at the end. For a monotone $f$, $f(x \sqcap y) \sqsubseteq f(x) \sqcap f(y)$, so merging early can only lose. In [constant propagation](/constant-propagation-problem/) on the diamond where one branch sets $(x, y) = (2, 3)$ and the other $(3, 2)$, followed by `z = x + y`, MFP says `z` is not a constant and MOP says $z = 5$. In a distributive framework with every block reachable, MFP = MOP (proved on the [distributive dataflow framework](/distributive-dataflow-framework/) page).

**Cost.** The plain iteration $X_{i+1} = F(X_i)$ takes at most $n h + 1$ rounds, each with $n$ transfer functions and $m$ meets. The [worklist dataflow algorithm](/worklist-dataflow-algorithm/) recomputes only what can change: each entry falls at most $h$ times, so it uses at most $n(h + 1)$ transfer functions and $m(h + 1)$ meets. For rapid frameworks, round-robin iteration in reverse postorder needs only $d + 2$ rounds, with $d$ the loop-connectedness depth ([Kam-Ullman iteration bound](/kam-ullman-iteration-bound/)).

**Any fair order gives MFP.** The result does not depend on the order in which blocks are updated. Any update $X[B] \leftarrow F(X)[B]$ applied to an $X \sqsupseteq \mathrm{MFP}$ gives a value $\sqsupseteq \mathrm{MFP}[B]$, since $F(X)[B] \sqsupseteq F(\mathrm{MFP})[B] = \mathrm{MFP}[B]$. So every order stays above MFP, and an order that stops only when no update changes anything stops at a fixed point, which must then be MFP. This is why round-robin, worklist and other chaotic iteration orders of [fixed-point iteration](/fixed-point-iteration/) all agree.

## Examples and non-examples

**Live variables on the running example.** For the loop of the running example of [dataflow analysis](/dataflow-analysis/), the MFP of [live variable analysis](/live-variable-analysis/) has $\{n, x\}$ live at the start of `entry` and $\{a, i, n, s, x\}$ at the start of `odd`. Liveness is distributive and every block reaches the return, so this is also MOP.

**Non-example: a fixed point that is not the greatest.** Add `w = 0` to `entry` in the running example, and let nothing read `w`. Putting `w` into the live sets of `head`, `body`, `odd` and `next` gives another solution of the equations: around the loop, each block passes `w` to the block before it, and no block in the loop writes `w`. The facts justify each other in a cycle. This solution has larger sets, so in the order $\supseteq$ of a may problem it is strictly below the MFP. Iteration from $\top = \emptyset$ never adds `w`, because no read of `w` starts the chain. The MFP, the greatest fixed point, is the one without such self-supporting claims.

**Non-example: the wrong start value in a must problem.** For [available expressions](/available-expressions/), starting the blocks other than the entry at $\emptyset$ ($\bot$) instead of $\top$ also ends at a fixed point, but often a smaller one: an expression computed before a loop and not changed inside it is lost at the loop head, because the back edge brings $\emptyset$. Only the start at $\top$ gives the greatest fixed point.

**Non-example: a framework that is not monotone.** If a transfer function is not monotone, $F$ need not have a fixed point at all. With one item $d$, union as the meet, and a block with a self-loop whose function is $X \mapsto \{d\} - X$, the equation is $X = \{d\} - X$, which no set satisfies.

## Related definitions

- [Meet-over-all-paths solution](/meet-over-all-paths-solution/): the ideal answer, at least as precise as MFP.
- [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/): MFP = MOP for distributive frameworks.
- [Kleene fixed-point theorem](/kleene-fixed-point-theorem/) and [Knaster-Tarski theorem](/knaster-tarski-theorem/): fixed points of monotone functions by iteration and by lattice theory.
- [Fixed-point iteration](/fixed-point-iteration/) and [worklist dataflow algorithm](/worklist-dataflow-algorithm/): ways to compute MFP.
- [Abstract interpretation](/abstract-interpretation/): the same idea with the order reversed (least fixed points from $\bot$) and with [widening](/widening-operator/) for lattices of infinite height.

## References
