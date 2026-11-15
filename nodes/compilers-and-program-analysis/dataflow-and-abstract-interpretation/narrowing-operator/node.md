---
tag: AZWD5B
kind: definition
slug: narrowing-operator
name: Narrowing operator
aliases:
- narrowing in abstract interpretation
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: An operator applied after widening that refines a post-fixed point downward while staying sound, in finitely many steps.
prereqs: [widening-operator]
see_also: [interval-domain, abstract-interpretation, weak-topological-ordering, knaster-tarski-theorem, abstract-domain]
sources:
  - paper: doi:10.1145/512950.512973
    title: "Patrick Cousot and Radhia Cousot, Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints, POPL 1977, pages 238 to 252"
    locator: the definition of a narrowing and the downward iteration that starts from the limit of the upward iteration with widening
  - paper: "Patrick Cousot and Radhia Cousot, Static determination of dynamic properties of programs, Proceedings of the Second International Symposium on Programming, B. Robinet (ed.), Dunod, Paris, 1976, pages 106 to 130"
    locator: the decreasing iteration on intervals that refines the infinite bounds found by the widening
  - paper: doi:10.1007/3-540-55844-6_142
    title: "Patrick Cousot and Radhia Cousot, Comparing the Galois connection and widening/narrowing approaches to abstract interpretation, PLILP 1992, LNCS 631, pages 269 to 295"
    locator: the use of widening and narrowing together, and the dual operators for iterations from above
  - book: isbn:9780262043410
    title: Xavier Rival and Kwangkeun Yi, Introduction to Static Analysis, An Abstract Interpretation Perspective, MIT Press, 2020
    locator: Chapter 3 (the refinement of loop invariants after widening) and Appendix B (the soundness proofs)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Chapter 4 (Abstract Interpretation), the treatment of narrowing operators after the widening
---

A narrowing operator $\Delta$ refines the result of a widened analysis. The widening stops at an element $z$ with $F^\sharp(z) \sqsubseteq z$, often far above the least fixed point. Each narrowing step moves the value down toward $F^\sharp$ of the value, but only so far that the result stays above the least fixed point and the steps stop after finitely many. On intervals the usual narrowing replaces an infinite bound by the finite bound that $F^\sharp$ computes, and keeps every finite bound.

## Definition

The setting is an [abstract domain](/abstract-domain/) $(A, \sqsubseteq)$ in the Cousot order and a monotone abstract function $F^\sharp : A \to A$. The [widening operator](/widening-operator/) page explains how to reach the start point.

A **narrowing** is a map $\Delta : A \times A \to A$ with two properties.

1. **Between the arguments.** For all $x, y$ with $y \sqsubseteq x$: $y \sqsubseteq x \,\Delta\, y \sqsubseteq x$.
2. **Stabilization.** For every decreasing chain $y_0 \sqsupseteq y_1 \sqsupseteq y_2 \sqsupseteq \cdots$, the chain $x_0 = y_0$, $x_{k+1} = x_k \,\Delta\, y_{k+1}$ is eventually stationary.

**The narrowed iteration.** Start from $w_0$ with $F^\sharp(w_0) \sqsubseteq w_0$, for example the result of the widened iteration. Set $w_{k+1} = w_k \,\Delta\, F^\sharp(w_k)$, and stop when $w_{k+1} = w_k$.

**Theorem (soundness is kept).** For every $k$: $w_{k+1} \sqsubseteq w_k$ and $F^\sharp(w_k) \sqsubseteq w_k$. Hence $\mathrm{lfp}\, F^\sharp \sqsubseteq w_k$ when $A$ is a complete lattice, and $\gamma(w_k)$ contains the [collecting semantics](/collecting-semantics/) when $F^\sharp$ is sound.

*Proof.* By induction on $k$. For $k = 0$, $F^\sharp(w_0) \sqsubseteq w_0$ holds by the choice of $w_0$. Assume $F^\sharp(w_k) \sqsubseteq w_k$. Property 1 with $x = w_k$ and $y = F^\sharp(w_k)$ gives

$$ F^\sharp(w_k) \sqsubseteq w_{k+1} \sqsubseteq w_k . $$

Since $F^\sharp$ is monotone and $w_{k+1} \sqsubseteq w_k$, we get $F^\sharp(w_{k+1}) \sqsubseteq F^\sharp(w_k) \sqsubseteq w_{k+1}$. This closes the induction. Each $w_k$ is an element $x$ with $F^\sharp(x) \sqsubseteq x$, so the [Knaster-Tarski theorem](/knaster-tarski-theorem/) puts $\mathrm{lfp}\, F^\sharp$ below it, and the claim on the [abstract domain](/abstract-domain/) page gives $\mathit{Coll} \subseteq \gamma(w_k)$. $\square$

In the naming of the Knaster-Tarski page each $w_k$ is a pre-fixed point; Cousot calls it a post-fixed point. Either way, every step of the narrowed iteration is a sound result, so an analyzer may stop at any step, for example when a time budget runs out.

**Theorem (termination).** The narrowed iteration stops.

*Proof.* Put $y_0 = w_0$ and $y_{k+1} = F^\sharp(w_k)$. The chain $(w_k)$ is decreasing by the first theorem, so $(F^\sharp(w_k))$ is decreasing by monotonicity, and $y_1 = F^\sharp(w_0) \sqsubseteq w_0 = y_0$. So $(y_k)$ is a decreasing chain, $w_0 = y_0$ and $w_{k+1} = w_k \,\Delta\, y_{k+1}$. By property 2 the chain $(w_k)$ is eventually stationary, so some step has $w_{k+1} = w_k$. $\square$

The monotonicity of $F^\sharp$ is used in both proofs. Without it, $w_{k+1}$ may fail $F^\sharp(w_{k+1}) \sqsubseteq w_{k+1}$, and the narrowed value may be unsound. The widening has no such need in its stronger form.

**The interval narrowing.** For intervals,

$$ \bot \,\Delta\, y = \bot, \qquad x \,\Delta\, \bot = \bot, \qquad [a, b] \,\Delta\, [c, d] = [\, a = -\infty \,?\, c : a,\ \ b = +\infty \,?\, d : b \,]. $$

Property 1: if $[c, d] \sqsubseteq [a, b]$, then $a \le c$ and $d \le b$, and the new lower bound is $c$ or $a$, both between $a$ and $c$; the upper bound is the same. Property 2: a finite bound never changes, and an infinite bound changes at most once, to a finite one. So a chain of narrowed values changes at most three times: once for each bound and once to $\bot$. On a map from names to intervals the narrowing works name by name, and the chain changes at most $2v + 1$ times for $v$ names.

**A narrowing is not a meet.** For $y \sqsubseteq x$ the meet gives $x \sqcap y = y$, which is the plain decreasing step $w_{k+1} = F^\sharp(w_k)$. It satisfies property 1 but not property 2, as the second example below shows. A narrowing may stop above $F^\sharp(w_k)$, and the interval narrowing does so whenever a finite bound could still go down.

**A narrowing is not a dual widening.** A narrowing never jumps below its second argument; it stops early instead. To compute a greatest fixed point from above, which some backward analyses need, an analyzer uses a *dual widening*: an operator that jumps downward and makes every decreasing chain stop.

## Examples and non-examples

**Continuing the widened loop.** The loop that sums `i` from 0 to 9 into `s` is on the [widening operator](/widening-operator/) page. The widening stops at $w_0$ with $i \in [0, +\infty]$, $s \in [0, +\infty]$ at the loop head.

| step | $w_k$ at head | $F^\sharp(w_k)$ | $w_{k+1} = w_k \,\Delta\, F^\sharp(w_k)$ |
|---|---|---|---|
| 0 | $i \in [0, +\infty]$, $s \in [0, +\infty]$ | $i \in [0, 10]$, $s \in [0, +\infty]$ | $i \in [0, 10]$, $s \in [0, +\infty]$ |
| 1 | $i \in [0, 10]$, $s \in [0, +\infty]$ | $i \in [0, 10]$, $s \in [0, +\infty]$ | no change |

The infinite upper bound of `i` becomes 10. The upper bound of `s` stays infinite, because $F^\sharp$ itself gives $+\infty$: here $w_1$ is the least fixed point of $F^\sharp$, and the bound on `s` is lost by the domain. At the exit the guard $i \ge 10$ gives $i \in [10, 10]$, $s \in [0, +\infty]$.

**Plain decreasing iteration may not stop.** Take $F^\sharp(X) = (X \sqcap [0, +\infty]) + 1$ on intervals, the equation of a loop head that only its back edge reaches. Its least fixed point is $\bot$. Start from $w_0 = [0, +\infty]$, which satisfies $F^\sharp(w_0) = [1, +\infty] \sqsubseteq w_0$. The plain decreasing steps give

$$ [0, +\infty] \sqsupset [1, +\infty] \sqsupset [2, +\infty] \sqsupset \cdots $$

and never stop. The interval narrowing gives $[0, +\infty] \,\Delta\, [1, +\infty] = [0, +\infty]$, because the lower bound is finite, and it stops at once with a sound result.

**The narrowing keeps a finite bound that is too large.** Analyze the loop `i = 0; while i < 10: i = i + 1` with a widening with the threshold list $\{100\}$. The widening gives $[0, 0] \nabla [0, 1] = [0, 100]$, and then $F^\sharp([0, 100]) = [0, 10] \sqsubseteq [0, 100]$. The interval narrowing gives $[0, 100] \,\Delta\, [0, 10] = [0, 100]$ and stops, because both bounds are finite. One plain decreasing step gives $[0, 10]$. For this reason many analyzers use a fixed number of plain steps after the widening, for example one or two; a bounded number of steps always stops, and each step is sound by the first theorem.

**Non-example: a narrowing that goes below its second argument.** The map $x \,\Delta\, y = \bot$ makes every chain stop at once, but $\bot \sqsubseteq F^\sharp(w_k)$ is in general strictly below $F^\sharp(w_k)$, so property 1 fails. The result describes no state, and the analysis would claim that the loop head is unreachable. The lower bound $y \sqsubseteq x \,\Delta\, y$ is what keeps soundness in the proof above.

## Related definitions

- [Widening operator](/widening-operator/): the upward phase that gives the start point of the narrowed iteration.
- [Interval domain](/interval-domain/): the domain of the examples, with its transfer functions.
- [Weak topological ordering](/weak-topological-ordering/): the order of the blocks; the narrowed iteration uses the same order and the same set of heads.
- [Abstract domain](/abstract-domain/): the claim that any $X$ with $F^\sharp(X) \sqsubseteq X$ is sound.
- [Knaster-Tarski theorem](/knaster-tarski-theorem/): the least fixed point lies below every such $X$.
- [Abstract interpretation](/abstract-interpretation/): the general technique, with a decreasing step on a worked loop.

## References
