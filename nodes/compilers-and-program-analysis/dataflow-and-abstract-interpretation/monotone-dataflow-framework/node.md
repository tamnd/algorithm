---
tag: VCMGHG
kind: definition
slug: monotone-dataflow-framework
name: Monotone dataflow framework
aliases:
- monotone framework
- Kam-Ullman framework
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: A dataflow problem given by a semilattice of facts of finite height, a direction and monotone transfer functions for the nodes.
prereqs: [dataflow-analysis, fixed-point]
see_also: [distributive-dataflow-framework, gen-kill-problem, maximal-fixed-point-solution, meet-over-all-paths-solution, worklist-dataflow-algorithm, mop-mfp-coincidence-theorem, constant-propagation-problem, knaster-tarski-theorem]
sources:
  - paper: doi:10.1007/BF00290339
    title: "John B. Kam and Jeffrey D. Ullman, Monotone data flow analysis frameworks, Acta Informatica 7(3), 1977, 305-317"
    locator: the whole paper (the definition of a monotone framework, the existence of the maximal fixed point and its computation by Kildall's algorithm, MFP below MOP, and the undecidability of MOP for monotone frameworks)
  - paper: doi:10.1145/321921.321938
    title: "John B. Kam and Jeffrey D. Ullman, Global data flow analysis and iterative algorithms, Journal of the ACM 23(1), 1976, 158-171"
    locator: the whole paper (the semilattice formulation and the analysis of round-robin iteration)
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the whole paper (the meet semilattice of facts and the distributive optimizing functions that monotone frameworks generalize)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.3 (9.3.1 Semilattices, 9.3.2 Transfer Functions, 9.3.3 The Iterative Algorithm for General Frameworks, 9.3.4 Meaning of a Data-Flow Solution) and Section 9.4 (constant propagation, 9.4.4 monotonicity and 9.4.5 nondistributivity)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Section 2.3 (Monotone Frameworks, stated with a join, the ascending chain condition and least solutions)
---

A monotone dataflow framework is the general form of a [dataflow analysis](/dataflow-analysis/): a semilattice of facts with no infinite descending chains, together with a set of transfer functions that are monotone, contain the identity and are closed under composition. Kam and Ullman (1977) defined it to cover analyses such as [constant propagation](/constant-propagation-problem/) that fail Kildall's condition of distributivity. This page gives the definition and what follows from monotonicity alone. The stronger [distributive dataflow framework](/distributive-dataflow-framework/) adds $f(x \sqcap y) = f(x) \sqcap f(y)$; the [gen-kill problems](/gen-kill-problem/) are the distributive bit-vector special case; the answers are defined on [meet-over-all-paths solution](/meet-over-all-paths-solution/) and [maximal fixed-point solution](/maximal-fixed-point-solution/), and the solver is the [worklist dataflow algorithm](/worklist-dataflow-algorithm/).

## Definition

This page uses the meet convention of Kildall and the dragon book. A *partial order* is reflexive, antisymmetric and transitive. A *meet semilattice* $(L, \sqcap)$ is a set $L$ with an operation $\sqcap$ that is idempotent, commutative and associative. It defines the order $x \sqsubseteq y \iff x \sqcap y = x$, and $x \sqcap y$ is then the greatest lower bound of $x$ and $y$. The element $\top$ is the identity of meet, so $x \sqsubseteq \top$ for all $x$. Lower facts claim less. A strict descending chain is $x_0 \sqsupset x_1 \sqsupset \cdots$, and the *height* $h$ of $L$ is the largest number of strict steps in such a chain.

**The framework.** A *monotone dataflow framework* is a triple $(L, \sqcap, F)$ where:

1. $(L, \sqcap)$ is a meet semilattice with a top element $\top$ in which every strict descending chain is finite. Most texts, and the bounds on these pages, ask for the stronger condition that the height $h$ is finite.
2. $F$ is a set of functions $L \to L$, and each $f \in F$ is *monotone*: $x \sqsubseteq y$ implies $f(x) \sqsubseteq f(y)$.
3. $F$ contains the identity function and is closed under composition.

Condition 3 makes the function of a path, the composition of the functions of its blocks, a member of $F$; the empty path has the identity.

**An equivalent form of monotonicity.** A function $f$ is monotone if and only if $f(x \sqcap y) \sqsubseteq f(x) \sqcap f(y)$ for all $x, y$.

*Proof.* Assume $f$ is monotone. Since $x \sqcap y \sqsubseteq x$ and $x \sqcap y \sqsubseteq y$, we get $f(x \sqcap y) \sqsubseteq f(x)$ and $f(x \sqcap y) \sqsubseteq f(y)$. So $f(x \sqcap y)$ is a lower bound of $f(x)$ and $f(y)$, and it is below their greatest lower bound $f(x) \sqcap f(y)$. Conversely, assume the inequality and let $x \sqsubseteq y$. Then $x = x \sqcap y$, so $f(x) = f(x \sqcap y) \sqsubseteq f(x) \sqcap f(y) \sqsubseteq f(y)$. $\square$

So a monotone function may lose information at a meet: applying $f$ after the meet can give a strictly lower fact than meeting the results of $f$. A distributive function never does.

**An instance.** An instance of the framework is a [control flow graph](/control-flow-graph/) $G = (V, E)$ with $n$ blocks and $m$ edges, a direction (forward or backward), a map $B \mapsto f_B \in F$, and a boundary value $\iota \in L$. A forward instance starts at the entry block. A backward instance runs on the reverse CFG and starts after each block that ends in `ret`. The boundary value describes what is known where the program starts (forward) or ends (backward). It is chosen by the problem, and it is $\top$ only by coincidence.

**The equations.** For a forward instance, with the empty meet equal to $\top$:

$$\mathrm{IN}[B] = \Big(\iota \text{ if } B \text{ is the entry}\Big) \sqcap \bigsqcap_{(P, B) \in E} \mathrm{OUT}[P], \qquad \mathrm{OUT}[B] = f_B(\mathrm{IN}[B]).$$

A backward instance has the same equations on the reverse CFG, with $\iota$ in the meet of each exit block.

**The two answers.** The ideal answer is $\mathrm{MOP}[B] = \bigsqcap_{\pi} f_\pi(\iota)$, the meet over all paths $\pi$ from the start to $B$. The equations have a greatest solution, the maximal fixed point MFP, and iteration from $\top$ computes it. In every monotone framework MFP $\sqsubseteq$ MOP, so the computed answer is safe. The proofs are on the [maximal fixed-point solution](/maximal-fixed-point-solution/) page.

**Soundness.** Assume that each $f_B$ is a safe description of block $B$: if a fact $x$ holds before the block runs, then $f_B(x)$ holds after it. Every execution follows some path of the CFG, so the fact after an execution is at least $f_\pi(\iota)$ for its path $\pi$, and MOP and MFP are below that. Paths of the CFG that no input follows only lower the answer, which keeps it safe.

**Precision.** MFP can be strictly below MOP. In constant propagation, let one branch set $x = 2, y = 3$ and the other $x = 3, y = 2$, and let them join before `z = x + y`. On each path the transfer function gives $z = 5$, so MOP gives $z = 5$. MFP meets first: $x$ and $y$ both become "not a constant", and then $z$ is "not a constant" too. Here $f(a \sqcap b) \sqsubset f(a) \sqcap f(b)$.

**Cost.** Each fact can fall at most $h$ times. A worklist solver therefore applies $O(n h)$ transfer functions and $O(m h)$ meets. MOP itself is not computable in general: Kam and Ullman (1977) show that no algorithm computes the MOP solution of every instance of every monotone framework.

## Examples and non-examples

**The four bit-vector problems.** Each is a monotone framework whose lattice is the set of subsets of a finite universe $U$, with height $h = |U|$. The transfer functions have the form $f(x) = gen \cup (x - kill)$, which is monotone (in fact distributive, as the [gen-kill problem](/gen-kill-problem/) page proves).

| problem | direction | may or must | meet | order $\sqsubseteq$ | $\top$ | $\bot$ | boundary $\iota$ | start value elsewhere |
|---|---|---|---|---|---|---|---|---|
| [reaching definitions](/reaching-definitions/) | forward | may | $\cup$ | $\supseteq$ | $\emptyset$ | all definitions | $\emptyset$ at the entry | $\emptyset$ |
| [live variables](/live-variable-analysis/) | backward | may | $\cup$ | $\supseteq$ | $\emptyset$ | all variables | $\emptyset$ after each exit | $\emptyset$ |
| [available expressions](/available-expressions/) | forward | must | $\cap$ | $\subseteq$ | all expressions | $\emptyset$ | $\emptyset$ at the entry | all expressions |
| [very busy expressions](/very-busy-expressions/) | backward | must | $\cap$ | $\subseteq$ | all expressions | $\emptyset$ | $\emptyset$ after each exit | all expressions |

On the running example of [dataflow analysis](/dataflow-analysis/) the universes have 7 definitions, 7 variables (`n`, `x`, `i`, `s`, `t`, `a`, `u`) and 5 expressions (`i < n`, `x * 2`, `i & 1`, `s + a`, `i + 1`), so the heights are 7, 7, 5 and 5.

**Constant propagation.** For each variable the lattice is flat: $\top$ ("no value seen yet") above every integer, and every integer above $\bot$ ("not a constant"). Two different integers are incomparable, so the meet of $2$ and $3$ is $\bot$. The fact at a point is a map from the $v$ variables to this lattice, ordered pointwise. A strict step lowers at least one variable, and each variable can fall at most twice, so the height is $2v$; the chain that lowers the variables one by one to a constant and then to $\bot$ has exactly $2v$ steps. The transfer function of `z = x + y` is monotone but not distributive, as the precision example above shows. So constant propagation is a monotone framework and not a distributive one. Its lattice has infinitely many elements but finite height, which is all the iteration needs.

**Non-example: a function that is not monotone.** Let the universe be one definition $d$, with meet $\cup$, and let a block $B$ with a self-loop have $f_B(X) = \{d\} - X$, the complement. The equations $\mathrm{IN}[B] = \emptyset \cup \mathrm{OUT}[B]$ and $\mathrm{OUT}[B] = \{d\} - \mathrm{IN}[B]$ give $\mathrm{IN}[B] = \{d\} - \mathrm{IN}[B]$, which no set satisfies. The equations have no fixed point at all. A solver that only lowers facts still stops, but the values it stops at do not solve the equations.

**Non-example: infinite height.** Let the fact be the set of values that `i` can hold, as a may problem over all integers. In the loop `i = 0`, then `i = i + 1` back to the loop head, the fact at the head grows $\{0\}$, $\{0, 1\}$, $\{0, 1, 2\}$ and so on, and iteration never stops. The meet semilattice here has strictly descending chains that never end. Analyses of this kind use [abstract interpretation](/abstract-interpretation/) with a [widening operator](/widening-operator/) instead.

**Non-example: no identity.** If $F$ held only the transfer functions of blocks, then the function of the empty path, the identity, could be missing, and so could compositions. The MOP definition needs both. Adding them never breaks monotonicity, since the identity and compositions of monotone functions are monotone.

## Related definitions

- [Distributive dataflow framework](/distributive-dataflow-framework/): a monotone framework with $f(x \sqcap y) = f(x) \sqcap f(y)$. Then MFP = MOP.
- [Gen-kill problem](/gen-kill-problem/): the distributive frameworks whose functions are $gen \cup (x - kill)$ on sets.
- [Meet-over-all-paths solution](/meet-over-all-paths-solution/) and [maximal fixed-point solution](/maximal-fixed-point-solution/): the ideal and the computed answer of an instance. The [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/) says when they agree.
- [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/): the number of round-robin passes for rapid frameworks, a subclass that contains the bit-vector problems.
- [Knaster-Tarski theorem](/knaster-tarski-theorem/) and [fixed point](/fixed-point/): a monotone function on a complete lattice has a greatest fixed point. A meet semilattice of finite height with $\top$ is a complete lattice, so the theorem applies, and here the iteration from $\top$ also reaches it.
- [Join semilattice](/join-semilattice/) and [abstract interpretation](/abstract-interpretation/): Nielson, Nielson and Hankin state monotone frameworks with a join, least solutions and the ascending chain condition. Turning the order upside down maps their convention onto this one.

## References
