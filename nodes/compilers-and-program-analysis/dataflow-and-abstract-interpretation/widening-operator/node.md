---
tag: AKGMSN
kind: definition
slug: widening-operator
name: Widening operator
aliases:
- widening
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: An upper bound operator whose iteration stabilizes in finitely many steps, used to force fixed-point iteration on infinite height domains to end.
prereqs: [abstract-domain, interval-domain]
see_also: [narrowing-operator, weak-topological-ordering, abstract-interpretation, polyhedra-domain, octagon-domain, kleene-fixed-point-theorem, fixed-point]
sources:
  - paper: doi:10.1145/512950.512973
    title: "Patrick Cousot and Radhia Cousot, Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints, POPL 1977, pages 238 to 252"
    locator: the definition of a widening by its upper bound property and the stabilization of every widened increasing chain, and the upward iteration with widening
  - paper: "Patrick Cousot and Radhia Cousot, Static determination of dynamic properties of programs, Proceedings of the Second International Symposium on Programming, B. Robinet (ed.), Dunod, Paris, 1976, pages 106 to 130"
    locator: the first widening, on intervals, used to analyze loops in finitely many steps
  - paper: doi:10.1007/3-540-55844-6_142
    title: "Patrick Cousot and Radhia Cousot, Comparing the Galois connection and widening/narrowing approaches to abstract interpretation, PLILP 1992, LNCS 631, pages 269 to 295"
    locator: the argument that widenings on domains of infinite height give results that no single finite abstract lattice gives for all programs
  - paper: doi:10.1016/j.scico.2005.02.003
    title: "Roberto Bagnara, Patricia M. Hill, Elisa Ricci and Enea Zaffanella, Precise widening operators for convex polyhedra, Science of Computer Programming 58(1-2), 2005, pages 28 to 56"
    locator: the standard widening on polyhedra and a framework for widenings that are more precise
  - book: isbn:9780262043410
    title: Xavier Rival and Kwangkeun Yi, Introduction to Static Analysis, An Abstract Interpretation Perspective, MIT Press, 2020
    locator: Chapter 3 (the analysis of loops with widening) and Appendix B (the soundness proofs, including the widening iterates)
---

A widening operator $\nabla$ takes the current approximation $x$ of a loop invariant and a new value $y$, and returns an upper bound of both that grows in big jumps, so that any chain of widened values stops after finitely many steps. It lets an analysis over a domain of infinite height, such as intervals, reach an element $x$ with $F^\sharp(x) \sqsubseteq x$ in a few steps, where plain iteration would run forever. A widening is not a join: it is not monotone, not commutative, and it gives up precision on purpose.

## Definition

The setting is an [abstract domain](/abstract-domain/) $(A, \sqsubseteq)$ in the Cousot order (lower is more precise) and an abstract function $F^\sharp : A \to A$, for example the abstract transfer function of a loop. The general idea and the interval widening are on the [abstract interpretation](/abstract-interpretation/) page; this page gives the definition, the proofs and the properties.

A **widening** is a map $\nabla : A \times A \to A$ with two properties.

1. **Upper bound.** For all $x, y$: $x \sqsubseteq x \nabla y$ and $y \sqsubseteq x \nabla y$.
2. **Stabilization.** For every increasing chain $y_0 \sqsubseteq y_1 \sqsubseteq y_2 \sqsubseteq \cdots$, the chain $x_0 = y_0$, $x_{k+1} = x_k \nabla y_{k+1}$ is eventually stationary: there is a $K$ with $x_k = x_K$ for all $k \ge K$.

Some texts require property 2 for every sequence $(y_k)$, increasing or not. That stronger form is needed when $F^\sharp$ is not monotone. The interval widening has it: each bound of $x_k$ can move only once, to an infinity, whatever $y_{k+1}$ is.

**The widened iteration.** Start from $z_0 = \bot$. At step $k$, if $F^\sharp(z_k) \sqsubseteq z_k$, stop and return $z_k$. Otherwise set $z_{k+1} = z_k \nabla F^\sharp(z_k)$.

**Theorem (termination).** If $F^\sharp$ is monotone, the widened iteration stops, and it returns an element $z$ with $F^\sharp(z) \sqsubseteq z$.

*Proof.* Suppose the iteration never stops. Put $y_0 = \bot$ and $y_{k+1} = F^\sharp(z_k)$. Then $z_0 = y_0$ and $z_{k+1} = z_k \nabla y_{k+1}$. By property 1, $z_k \sqsubseteq z_{k+1}$ for each $k$, so $(z_k)$ is increasing. Since $F^\sharp$ is monotone, $(y_k)_{k \ge 1}$ is increasing too, and $y_0 = \bot$ is below $y_1$. So $(y_k)$ is an increasing chain, and $(z_k)$ is its widened chain. By property 2 there is a $K$ with $z_{K+1} = z_K$. Then, by property 1,

$$ F^\sharp(z_K) = y_{K+1} \sqsubseteq z_K \nabla y_{K+1} = z_{K+1} = z_K, $$

so the stop test holds at step $K$, which contradicts the assumption. The iteration therefore stops at some $z_k$, and the stop test is exactly $F^\sharp(z_k) \sqsubseteq z_k$. $\square$

With the stronger form of property 2 the same proof works without the monotonicity of $F^\sharp$.

**Soundness of the result.** The result $z$ has $F^\sharp(z) \sqsubseteq z$. By the claim on the [abstract domain](/abstract-domain/) page, $\gamma(z)$ contains the [collecting semantics](/collecting-semantics/) when $F^\sharp$ is sound; that proof does not use monotonicity either. When $F^\sharp$ is monotone on a complete lattice, the [Knaster-Tarski theorem](/knaster-tarski-theorem/) also gives $\mathrm{lfp}\, F^\sharp \sqsubseteq z$. Such a $z$ is a pre-fixed point in the naming of that page, and a post-fixed point in the naming of Cousot. It need not be a fixed point, and it is often above $\mathrm{lfp}\, F^\sharp$; a [narrowing](/narrowing-operator/) then improves it.

**Where to widen.** In a program with many blocks, $F^\sharp$ works on a map from blocks to $A$. It is enough to widen at a set of blocks that cuts every cycle of the control flow graph, and to use the join elsewhere. The heads of a [weak topological ordering](/weak-topological-ordering/) form such a set, and that page proves that the iteration then stops.

**A widening is not monotone.** For intervals, $[0, 0] \sqsubseteq [0, 1]$, but

$$ [0, 0] \nabla [0, 1] = [0, +\infty] \quad \text{and} \quad [0, 1] \nabla [0, 1] = [0, 1], $$

and $[0, +\infty] \not\sqsubseteq [0, 1]$. So a more precise first argument can give a less precise result: the widening looks at how far a bound moved, not only at where it ended. In practice this means that the result of an analysis depends on the order of the iteration, and that a more precise input fact can give a less precise output.

**A widening is not a join.** The join is commutative and gives the least upper bound. The interval widening is neither:

$$ [0, 1] \nabla [0, 2] = [0, +\infty], \qquad [0, 2] \nabla [0, 1] = [0, 2]. $$

The first argument is the old value and the second is the new one; the order matters. Using the join in place of the widening loses termination, and using the widening in place of the join at every block loses precision for nothing.

**Widening against finite domains.** A widening on a domain of infinite height can prove more than any finite domain. Take the family of programs $P_n$: `x = 0`, then `while x < n: x = x + 1`, for each constant $n \ge 0$. Intervals with widening and one narrowing step give $x \in [0, n]$ at the loop head, the exact set $\{0, \dots, n\}$. Now fix a finite domain $B$ with a concretization $\gamma$. To prove $0 \le x \le n$ at the head of $P_n$, an analysis must return some $b_n \in B$ with $\{0, \dots, n\} \subseteq \gamma(b_n) \subseteq \{x : 0 \le x \le n\}$, so $\gamma(b_n) = \{0, \dots, n\}$. The sets differ for different $n$, so the elements $b_n$ are pairwise different, and $B$ has infinitely many elements. This contradicts the choice of $B$. So for each finite domain, some program of the family has an invariant that it cannot prove; Cousot and Cousot (1992) make this point in general.

## Examples and non-examples

**A loop with two names.** The loop sums `i` into `s`.

```
entry:
  i = 0
  s = 0
  jump head
head:
  t = i < 10
  br t body exit
body:
  s = s + i
  i = i + 1
  jump head
exit:
  ret s
```

At head, $F^\sharp(x)$ joins the entry state ($i, s \in [0, 0]$) with the body applied to $x$ after the guard $i \le 9$. The widening is applied at head only, name by name.

| step | $z_k$ at head | $F^\sharp(z_k)$ | stop? |
|---|---|---|---|
| 0 | $\bot$ | $i \in [0, 0]$, $s \in [0, 0]$ | no |
| 1 | $i \in [0, 0]$, $s \in [0, 0]$ | $i \in [0, 1]$, $s \in [0, 0]$ | no |
| 2 | $i \in [0, +\infty]$, $s \in [0, 0]$ | $i \in [0, 10]$, $s \in [0, 9]$ | no |
| 3 | $i \in [0, +\infty]$, $s \in [0, +\infty]$ | $i \in [0, 10]$, $s \in [0, +\infty]$ | yes |

Step 0 gives $z_1 = \bot \nabla F^\sharp(\bot) = F^\sharp(\bot)$. At step 1 the upper bound of `i` moves, so it jumps to $+\infty$; `s` does not move. At step 2 the upper bound of `s` moves and jumps. At step 3 the test passes. The exit state is $i \in [10, +\infty]$, $s \in [0, +\infty]$. The [narrowing operator](/narrowing-operator/) page continues from here and gets $i \in [10, 10]$ at the exit.

**Plain iteration does not stop on the same loop.** Without widening, the iterates $(F^\sharp)^k(\bot)$ at head are $i \in [0, k - 1]$ and $s \in [0, (k-1)(k-2)/2]$ for $1 \le k \le 11$, which reaches $i \in [0, 10]$ and $s \in [0, 45]$. From then on `i` stays at $[0, 10]$, and each step adds the upper bound 9 of `i` to the upper bound of `s`: 54, 63, 72, and so on, without end. The loop runs ten times, but the interval domain does not know that $s$ and $i$ are linked. Here the least fixed point of $F^\sharp$ is $i \in [0, 10]$, $s \in [0, +\infty]$, and it is the limit of an infinite chain. The bound $s \le 45$ is lost by the domain, not by the widening.

**Delayed widening.** A common variant uses the join for the first $d$ steps and the widening after that. With $d = 2$ in the loop above, the first widening takes the old value $i \in [0, 1]$, $s \in [0, 0]$ and the new value $i \in [0, 2]$, $s \in [0, 1]$; both upper bounds jump at once, and the result is the same. In a loop whose bounds stop moving after a few passes, the delay keeps the exact bounds.

**Thresholds.** A widening with thresholds moves a bound to the next value of a fixed list, such as the constants of the program, before it moves it to infinity. With the list $\{10\}$ the first widening in the table gives $i \in [0, 10]$, and the exit state gets $i \in [10, 10]$ with no narrowing step. Each bound can move at most once per threshold plus once to infinity, so property 2 still holds.

**Widening on other domains.** The standard widening of the [polyhedra domain](/polyhedra-domain/) keeps the constraints of the old polyhedron that the new one still satisfies; it terminates because each strict step either raises the dimension or drops a constraint. The [octagon domain](/octagon-domain/) has a widening that works on the matrix of bounds, and its first argument must not be closed between steps, or the chain can grow forever.

**Non-example: the join on intervals.** The join is an upper bound, so property 1 holds. On the chain $[0, 0] \sqsubseteq [0, 1] \sqsubseteq [0, 2] \sqsubseteq \cdots$ the joined chain is the chain itself, which never stops. Property 2 fails.

**Non-example: a jump to $\top$.** The map $x \nabla y = \top$ when $y \not\sqsubseteq x$, and $x$ otherwise, is a widening: it is an upper bound, and a chain can change at most once. It is also useless: it gives $i \in [-\infty, +\infty]$ in the loop above and loses the lower bound $i \ge 0$. A good widening keeps every bound that has not moved.

## Related definitions

- [Narrowing operator](/narrowing-operator/): the decreasing phase after the widening, which recovers some of the lost precision.
- [Weak topological ordering](/weak-topological-ordering/): where to place the widenings and in which order to iterate.
- [Interval domain](/interval-domain/), [octagon domain](/octagon-domain/) and [polyhedra domain](/polyhedra-domain/): domains of infinite height, each with its own widening.
- [Abstract interpretation](/abstract-interpretation/): the general technique and the interval widening.
- [Kleene fixed-point theorem](/kleene-fixed-point-theorem/): the plain iteration from $\bot$, which reaches the least fixed point only as a limit when the domain has infinite chains.
- [Fixed point](/fixed-point/) and [Knaster-Tarski theorem](/knaster-tarski-theorem/): the reason a widened result lies above the least fixed point.

## References
