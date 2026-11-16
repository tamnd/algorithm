---
tag: HTP3TD
kind: definition
slug: distributive-dataflow-framework
name: Distributive dataflow framework
aliases:
- distributive framework
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: A monotone framework whose transfer functions distribute over the meet, f(x meet y) = f(x) meet f(y), as gen-kill problems do.
prereqs: [monotone-dataflow-framework]
see_also: [gen-kill-problem, mop-mfp-coincidence-theorem, meet-over-all-paths-solution, maximal-fixed-point-solution, ifds-framework, ide-framework, constant-propagation-problem, worklist-dataflow-algorithm]
sources:
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the whole paper (the distributive optimizing functions on a meet semilattice, and the result that the iterative algorithm then finds the meet over all paths)
  - paper: doi:10.1007/BF00290339
    title: "John B. Kam and Jeffrey D. Ullman, Monotone data flow analysis frameworks, Acta Informatica 7(3), 1977, 305-317"
    locator: the whole paper (monotone frameworks that are not distributive, such as constant propagation, where the maximal fixed point can be strictly below the meet over all paths)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.3.2 (Transfer Functions, monotone and distributive frameworks), Section 9.3.4 (Meaning of a Data-Flow Solution, MFP and MOP) and Section 9.4.5 (nondistributivity of the constant-propagation framework)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Section 2.3 (Monotone Frameworks, including distributive frameworks) and Section 2.4 (Equation Solving, the MFP and MOP solutions and when they agree), in the join convention
---

A distributive dataflow framework is a [monotone dataflow framework](/monotone-dataflow-framework/) in which every transfer function distributes over the meet: $f(x \sqcap y) = f(x) \sqcap f(y)$. This was Kildall's original condition in 1973. It is the condition under which merging facts early loses nothing, so the [maximal fixed-point solution](/maximal-fixed-point-solution/) that an iterative solver computes equals the ideal [meet-over-all-paths solution](/meet-over-all-paths-solution/). Every [gen-kill problem](/gen-kill-problem/) is distributive, which covers reaching definitions, live variables, available expressions and very busy expressions. [Constant propagation](/constant-propagation-problem/) is the standard monotone framework that is not distributive.

## Definition

The dataflow pages use the meet convention: $(L, \sqcap)$ is a meet semilattice, $x \sqsubseteq y$ means $x \sqcap y = x$, $\top$ is the identity of meet, and the height $h$ of $L$ is the largest number of strict steps in a chain $x_0 \sqsupset x_1 \sqsupset \cdots$. A function $f : L \to L$ is *monotone* if $x \sqsubseteq y$ implies $f(x) \sqsubseteq f(y)$.

**Definition.** A monotone framework $(L, \sqcap, F)$ is *distributive* if every $f \in F$ satisfies

$$f(x \sqcap y) = f(x) \sqcap f(y) \quad \text{for all } x, y \in L.$$

A monotone function always satisfies $f(x \sqcap y) \sqsubseteq f(x) \sqcap f(y)$ (proved on the [monotone dataflow framework](/monotone-dataflow-framework/) page). Distributivity asks for equality: applying $f$ after a meet loses nothing compared with applying it before.

**Distributive implies monotone.** Let $x \sqsubseteq y$, so $x = x \sqcap y$. Then $f(x) = f(x \sqcap y) = f(x) \sqcap f(y)$, which says $f(x) \sqsubseteq f(y)$. $\square$

**Closed under composition.** If $f$ and $g$ distribute, then $(g \circ f)(x \sqcap y) = g(f(x) \sqcap f(y)) = g(f(x)) \sqcap g(f(y))$. The identity distributes too. So the functions of all paths of a distributive instance are distributive. $\square$

**Finite meets.** By induction on $k$, $f(x_1 \sqcap \cdots \sqcap x_k) = f(x_1) \sqcap \cdots \sqcap f(x_k)$ for every $k \ge 1$. The case $k = 0$ fails in general: the empty meet is $\top$, and $f(\top)$ need not be $\top$. For example $f(X) = \{d\} \cup X$ in a may problem maps $\top = \emptyset$ to $\{d\}$.

**Infinite meets reduce to finite ones.** In a semilattice of finite height $h$ with a top, every nonempty set $S \subseteq L$ has a greatest lower bound, and it is the meet of at most $h + 1$ members of $S$. *Proof.* Pick $s_0 \in S$ and set $c = s_0$. While some $s \in S$ has $c \sqcap s \ne c$, replace $c$ with $c \sqcap s$. Each replacement makes $c$ strictly smaller, so there are at most $h$ of them. At the end $c \sqsubseteq s$ for all $s \in S$, and any lower bound of $S$ is below each of the chosen members and hence below $c$. $\square$ So $f(\mathop{\large\sqcap} S) = \mathop{\large\sqcap}_{s \in S} f(s)$ for every nonempty $S$, even when $S$ is the infinite set of paths through a loop.

**The main consequence: MFP = MOP.** Take a forward instance on a CFG in which every block is reachable from the entry, with boundary value $\iota$. Then the [maximal fixed-point solution](/maximal-fixed-point-solution/) equals the [meet-over-all-paths solution](/meet-over-all-paths-solution/) at every block.

*Proof.* In every monotone framework MFP $\sqsubseteq$ MOP, as proved on the [maximal fixed-point solution](/maximal-fixed-point-solution/) page. For the other direction it is enough to show that MOP satisfies the equations, because MFP is the greatest solution. The paths from the entry to the start of $B$ are the empty path if $B$ is the entry, together with, for each predecessor $P$, every path to the start of $P$ followed by $P$. Write $\Pi_P$ for the paths to the start of $P$. Each $\Pi_P$ is nonempty, since $P$ is reachable. Then

$$\mathrm{MOP}[B] = \Big(\iota \text{ if } B \text{ is the entry}\Big) \sqcap \mathop{\large\sqcap}_{P} \mathop{\large\sqcap}_{\pi \in \Pi_P} f_P(f_\pi(\iota)) = \Big(\iota \text{ if } B \text{ is the entry}\Big) \sqcap \mathop{\large\sqcap}_{P} f_P\Big(\mathop{\large\sqcap}_{\pi \in \Pi_P} f_\pi(\iota)\Big) = \Big(\iota \text{ if } B \text{ is the entry}\Big) \sqcap \mathop{\large\sqcap}_{P} f_P(\mathrm{MOP}[P]).$$

The middle step uses distributivity over the nonempty set $\{f_\pi(\iota) : \pi \in \Pi_P\}$. So MOP is a solution, MOP $\sqsubseteq$ MFP, and with MFP $\sqsubseteq$ MOP they are equal. For a backward instance, use the reverse CFG and require every block to reach a `ret` block. $\square$

The [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/) states this result on its own page. Kam and Ullman (1977) proved that without distributivity no algorithm computes MOP for every monotone framework, which is why the distinction matters.

**The reachability condition is needed.** If $P$ is unreachable, $\Pi_P$ is empty, MOP[P] is $\top$, and $f_P(\top)$ can be below $\top$: an unreachable block in a may problem still sends its $gen$ set to its successors in every solution of the equations, while no path from the entry carries it. Then MFP is strictly below MOP even in a distributive framework.

**Soundness and precision.** Distributivity does not change soundness, which every monotone framework has. It removes the loss of precision at joins: the computed answer is as precise as any answer that treats all CFG paths as possible. What it cannot remove is the loss from CFG paths that no run takes.

**Cost.** The same as for any monotone framework of height $h$: a worklist solver applies $O(n h)$ transfer functions and $O(m h)$ meets on a CFG with $n$ blocks and $m$ edges. Distributivity buys exactness, not speed. Speed comes from the stronger *rapid* property of the [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/), which all gen-kill problems have.

## Examples and non-examples

**Gen-kill functions.** On the subsets of a finite set $U$, $f(X) = g \cup (X - k)$ distributes over both $\cup$ and $\cap$, so the four bit-vector problems are distributive. The proof is on the [gen-kill problem](/gen-kill-problem/) page.

**Strongly live variables.** In this variant of [live variable analysis](/live-variable-analysis/), the instruction `x = y + z` makes `y` and `z` live only if `x` is live after it: $f(X) = (X - \{x\}) \cup (\{y, z\} \text{ if } x \in X)$. With union as the meet, $f(X \cup Y)$ contains $\{y, z\}$ exactly when $x \in X$ or $x \in Y$, so $f(X \cup Y) = f(X) \cup f(Y)$. The function is distributive, but it is not of gen-kill form, because whether it adds $y$ depends on the input.

**Distributive functions on sets.** With union as the meet on the subsets of a finite set $D$, a function $f$ is distributive if and only if $f(X) = f(\emptyset) \cup \bigcup_{d \in X} f(\{d\})$ for every $X$. *Proof.* If $f$ distributes, write $X = \emptyset \cup \{d_1\} \cup \cdots \cup \{d_k\}$ and apply the finite-meet rule. Conversely, a function of this form clearly satisfies $f(X \cup Y) = f(X) \cup f(Y)$. $\square$ So a distributive function on $D$ is fully described by $|D| + 1$ sets. The [IFDS framework](/ifds-framework/) uses exactly this to turn interprocedural distributive problems into graph reachability, and the [IDE framework](/ide-framework/) extends the idea to environments.

**Copy-constant propagation.** Constant propagation restricted to `x = c` and `x = y` is distributive. With one flat lattice per variable and the pointwise meet, the function of `x = y` maps an environment $\sigma$ to $\sigma[x \mapsto \sigma(y)]$, and $(\sigma \sqcap \tau)(y) = \sigma(y) \sqcap \tau(y)$, so the two sides agree in every variable.

**Non-example: full constant propagation.** Let one branch set $x = 2, y = 3$, the other $x = 3, y = 2$, and let them join before `z = x + y`. Call the two facts $a$ and $b$, and let $f$ be the function of `z = x + y`.

| fact | $x$ | $y$ | $z$ after $f$ |
|---|---|---|---|
| $a$ | 2 | 3 | 5 |
| $b$ | 3 | 2 | 5 |
| $f(a) \sqcap f(b)$ | not a constant | not a constant | 5 |
| $f(a \sqcap b)$ | not a constant | not a constant | not a constant |

So $f(a \sqcap b) \sqsubset f(a) \sqcap f(b)$, and on this program MFP says `z` is not a constant while MOP says `z = 5`. The function combines two variables, and the meet has already forgotten that they move together.

**Non-example: a constant that is lost at a join.** Even one variable can break distributivity if the function is not one to one. For `x = y * 0`, the function sends $y = 2$ and $y = 3$ to $x = 0$, but it sends their meet, "not a constant", to "not a constant" unless the folding rule knows that anything times 0 is 0.

## Related definitions

- [Monotone dataflow framework](/monotone-dataflow-framework/): the general class, where MFP $\sqsubseteq$ MOP and equality can fail.
- [Gen-kill problem](/gen-kill-problem/): the distributive problems on sets with functions $g \cup (X - k)$.
- [Meet-over-all-paths solution](/meet-over-all-paths-solution/) and [maximal fixed-point solution](/maximal-fixed-point-solution/): the two answers that distributivity makes equal; the [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/) is the theorem above.
- [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/): the *rapid* frameworks, where round-robin iteration in reverse postorder ends after a number of passes set by the loop structure. Rapid and distributive are different conditions.
- [IFDS framework](/ifds-framework/) and [IDE framework](/ide-framework/): interprocedural analysis that is exact over valid paths for distributive problems.

## References
