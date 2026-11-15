---
tag: M3TQGG
kind: definition
slug: gen-kill-problem
name: Gen-kill dataflow problem
aliases:
- bit-vector dataflow problem
- gen-kill framework
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: A dataflow problem whose transfer functions have the form f(x) = gen union (x minus kill), solved fast with bit vectors.
prereqs: [distributive-dataflow-framework, reaching-definitions]
see_also: [reaching-definitions, live-variable-analysis, available-expressions, very-busy-expressions, distributive-dataflow-framework, kam-ullman-iteration-bound, worklist-dataflow-algorithm, ifds-framework]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.2 (9.2.4 Reaching Definitions with the composition of gen and kill sets, 9.2.5 Live-Variable Analysis, 9.2.6 Available Expressions), Section 9.3.2 (Transfer Functions) and Section 9.6.7 (Speed of Convergence of Iterative Data-Flow Algorithms)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Section 2.1 (the four classical analyses, each given by kill and gen functions) and Section 2.3 (Monotone Frameworks)
  - paper: doi:10.1145/321921.321938
    title: "John B. Kam and Jeffrey D. Ullman, Global data flow analysis and iterative algorithms, Journal of the ACM 23(1), 1976, 158-171"
    locator: the whole paper (the analysis of round-robin iteration in depth-first order, which covers the bit-vector problems)
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the whole paper (distributive optimizing functions, of which gen-kill functions are the main example)
---

A gen-kill dataflow problem is a [dataflow analysis](/dataflow-analysis/) whose facts are sets of items from a finite universe and whose transfer functions all have the form $f(X) = gen \cup (X - kill)$. The four classical problems, [reaching definitions](/reaching-definitions/), [live variable analysis](/live-variable-analysis/), [available expressions](/available-expressions/) and [very busy expressions](/very-busy-expressions/), are of this form. The functions are closed under composition, so a whole block has one pair $(gen, kill)$. They distribute over both union and intersection, so every gen-kill problem is a [distributive dataflow framework](/distributive-dataflow-framework/) and its computed answer equals the [meet-over-all-paths solution](/meet-over-all-paths-solution/). Each item is independent of the others, so a set fits in a bit vector and one transfer function costs a few word operations per $w$ items.

## Definition

The dataflow pages use the meet convention: $(L, \sqcap)$ is a meet semilattice, $x \sqsubseteq y$ means $x \sqcap y = x$, and $\top$ is the identity of meet and the start value.

**Definition.** Let $U$ be a finite set of items, with $u = |U|$. A *gen-kill problem* over $U$ is a dataflow problem with:

- the domain $L = $ all subsets of $U$;
- the meet $\sqcap = \cup$ (a *may* problem: $\top = \emptyset$ and the order is $\supseteq$) or $\sqcap = \cap$ (a *must* problem: $\top = U$ and the order is $\subseteq$);
- a direction, forward or backward, and a boundary value $\iota \subseteq U$;
- for each block $B$ two sets $gen_B, kill_B \subseteq U$ and the transfer function $f_B(X) = gen_B \cup (X - kill_B)$.

The height of $L$ is $h = u$ in both cases: a strict chain adds or removes one item per step.

| problem | items $U$ | direction | meet | $gen$ of `x = a op b` | $kill$ of `x = a op b` | boundary $\iota$ |
|---|---|---|---|---|---|---|
| [reaching definitions](/reaching-definitions/) | definitions | forward | $\cup$ | this definition | the other definitions of `x` | $\emptyset$ at the entry |
| [live variables](/live-variable-analysis/) | variables | backward | $\cup$ | `a`, `b` | `x` | $\emptyset$ after `ret` |
| [available expressions](/available-expressions/) | expressions | forward | $\cap$ | `a op b`, unless `x` is `a` or `b` | expressions that read `x` | $\emptyset$ at the entry |
| [very busy expressions](/very-busy-expressions/) | expressions | backward | $\cap$ | `a op b` | expressions that read `x` | $\emptyset$ after `ret` |

In the two must problems $\iota = \emptyset = \bot$, which is far from $\top = U$. In the may problems the usual $\iota$ is $\emptyset = \top$, but variants change it, such as the pseudo definitions at the entry for reaching definitions.

**Composition.** Applying $f_1 = (g_1, k_1)$ and then $f_2 = (g_2, k_2)$ gives

$$f_2(f_1(X)) = g_2 \cup \big((g_1 \cup (X - k_1)) - k_2\big) = \big(g_2 \cup (g_1 - k_2)\big) \cup \big(X - (k_1 \cup k_2)\big).$$

So the composition is the gen-kill function with $gen = g_2 \cup (g_1 - k_2)$ and $kill = k_1 \cup k_2$. The identity is $(\emptyset, \emptyset)$. The functions therefore form a set that contains the identity and is closed under composition, as a [monotone dataflow framework](/monotone-dataflow-framework/) requires. A block's pair is the composition of its instructions in the direction of the analysis: first to last for a forward problem, last to first for a backward one.

**Distributivity.** For all $X, Y \subseteq U$:

$$f(X \cup Y) = g \cup \big((X - k) \cup (Y - k)\big) = f(X) \cup f(Y),$$

$$f(X \cap Y) = g \cup \big((X - k) \cap (Y - k)\big) = \big(g \cup (X - k)\big) \cap \big(g \cup (Y - k)\big) = f(X) \cap f(Y),$$

where the first lines use $(X \cup Y) - k = (X - k) \cup (Y - k)$ and $(X \cap Y) - k = (X - k) \cap (Y - k)$, and the last step of the second line is the law $g \cup (A \cap B) = (g \cup A) \cap (g \cup B)$. So every gen-kill function distributes over the meet of a may problem and of a must problem alike. A distributive function is monotone, so a gen-kill problem is a distributive framework, and when every block is reachable from the start, the computed fixed point equals MOP. $\square$

**Which set functions are gen-kill.** Call $f$ on the subsets of $U$ *bitwise* if, for each item $d$, whether $d \in f(X)$ depends only on whether $d \in X$. Then $f$ is a gen-kill function if and only if it is bitwise and monotone.

*Proof.* A gen-kill function is bitwise: $d \in f(X)$ holds if $d \in g$, fails if $d \in k - g$, and otherwise holds exactly when $d \in X$. It is monotone because it distributes. Conversely, let $f$ be bitwise and monotone. For each $d$, the map from "$d \in X$" to "$d \in f(X)$" is a monotone function from $\{0, 1\}$ to $\{0, 1\}$, so it is the constant 0, the constant 1 or the identity; the fourth function, negation, is not monotone. Put $d$ in $g$ if it is the constant 1 and in $k$ if it is the constant 0. Then $f(X) = g \cup (X - k)$. $\square$

So the gen-kill problems are exactly the dataflow problems on sets in which items do not interact. This is what lets each item be solved on its own, as one [graph reachability](/graph-reachability/) question.

**Soundness and precision.** Each of the four problems is sound by the argument on its page: every run follows a CFG path, and the fixed point is below the fact of every path. Since MFP = MOP, the only loss of precision is from CFG paths that no run takes.

**Cost.** Store each set as a vector of $u$ bits. With word size $w$, the operations $X \cup Y$, $X \cap Y$ and $g \cup (X - k)$, the last as `gen | (x & ~kill)`, cost $O(u / w)$ word operations each. On a CFG with $n$ blocks and $m$ edges, the [worklist dataflow algorithm](/worklist-dataflow-algorithm/) changes each block value at most $u$ times, so it applies at most $n(u + 1)$ transfer functions and $m(u + 1)$ meets, for $O((n + m) u^2 / w)$ time. Gen-kill problems are also *rapid*, and round-robin iteration in reverse postorder stops after at most $d + 2$ passes, where $d$ is the loop-connectedness depth of the CFG. This gives $O((d + 2)(n + m) u / w)$ time; see the [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/). Space is $O(n u / w)$ words for the IN and OUT vectors and the $gen$ and $kill$ vectors.

## Examples and non-examples

**Composing a block.** In the running example of [dataflow analysis](/dataflow-analysis/), block `body` is

```
body:
  a = x * 2
  u = i & 1
  br u odd next
```

For available expressions, `a = x * 2` has $gen = \{x * 2\}$ and $kill = \{s + a\}$, since `s + a` reads `a`. Then `u = i & 1` has $gen = \{i \,\&\, 1\}$ and $kill = \emptyset$. The composition is $gen = \{i \,\&\, 1\} \cup (\{x * 2\} - \emptyset) = \{x * 2, i \,\&\, 1\}$ and $kill = \{s + a\}$. For live variables the same block is read from the end: the branch reads `u`, then `u = i & 1` writes `u` and reads `i`, then `a = x * 2` writes `a` and reads `x`. The composition is $gen = \{i, x\}$ and $kill = \{a, u\}$; `u` is not in $gen$ because the block writes it before the branch reads it.

**An instruction that reads what it writes.** For available expressions, `s = s + a` computes `s + a` and then changes `s`, so $gen = \{s + a\} - kill_s = \emptyset$. For very busy expressions, read backward, the same instruction has $gen = \{s + a\}$: the evaluation comes before the write.

**Reaching definitions with pseudo definitions.** Adding one pseudo definition per variable at the entry keeps the problem gen-kill; only $U$ and $\iota$ change.

**Non-example: strongly live variables.** The function of `x = y + z`, $f(X) = (X - \{x\}) \cup (\{y, z\} \text{ if } x \in X)$, is distributive, but whether $y \in f(X)$ depends on whether $x \in X$. It is not bitwise, so it is not gen-kill, and the items cannot be solved one at a time.

**Non-example: points-to sets.** In a may points-to analysis the fact is a set of pairs "$p$ may point to $o$". The instruction `q = *p` adds pairs for `q` that depend on which pairs of `p` are in the input. The function is not bitwise.

**Non-example: constant propagation.** The facts are maps from variables to a flat lattice, not sets, and the function of `z = x + y` is not even distributive. See [constant propagation](/constant-propagation-problem/).

## Related definitions

- [Distributive dataflow framework](/distributive-dataflow-framework/): the wider class with $f(x \sqcap y) = f(x) \sqcap f(y)$, where MFP = MOP still holds.
- [Monotone dataflow framework](/monotone-dataflow-framework/): the general class.
- [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/): the rapid property and the $d + 2$ passes of round-robin iteration.
- [IFDS framework](/ifds-framework/): interprocedural analysis for distributive problems over finite sets, which includes the gen-kill problems.
- [Datalog-based program analysis](/datalog-program-analysis/): a gen-kill problem is two Datalog rules per direction, with $kill$ as a negated condition.

## References
