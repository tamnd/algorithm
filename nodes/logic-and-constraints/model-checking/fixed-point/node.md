---
tag: KYHCVB
kind: concept
slug: fixed-point
name: Fixed point
aliases:
- Fixpoint
- Least and greatest fixed points
- Kleene iteration
area: logic-and-constraints/model-checking
level: core
summary: An element that a function maps to itself. In model checking the functions are monotone maps on sets of states, and least and greatest fixed points are found by iteration.
prereqs: [kripke-structure]
see_also: [knaster-tarski-theorem, modal-mu-calculus, computation-tree-logic, symbolic-reachability, emerson-lei-algorithm, abstract-interpretation, fixed-point-iteration, banach-fixed-point-theorem]
sources:
  - book: isbn:9780521543101
    title: Michael Huth and Mark Ryan, Logic in Computer Science, second edition, Cambridge University Press, 2004
    locator: Section 3.7 (monotone functions on sets of states, the iteration from the empty and the full set, and the fixed-point characterization of CTL operators)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 6, Section 6.1 (fixpoint representations of CTL operators and the computation of least and greatest fixpoints by iteration)
  - paper: doi:10.2140/pjm.1955.5.285
    title: Alfred Tarski, A lattice-theoretical fixpoint theorem and its applications, Pacific Journal of Mathematics 5(2), 1955, pages 285 to 309
    locator: Theorem 1 (the fixed points of a monotone function on a complete lattice form a complete lattice)
  - paper: doi:10.2140/pjm.1979.82.43
    title: Patrick Cousot and Radhia Cousot, Constructive versions of Tarski's fixed point theorems, Pacific Journal of Mathematics 82(1), 1979, pages 43 to 57
    locator: the characterization of the least fixed point as the limit of a transfinite iteration from the bottom element
---

A fixed point of a function $f$ is an element $x$ with $f(x) = x$. In model checking the elements are sets of states of a [Kripke structure](/kripke-structure/), and the functions are built from Boolean operations and the one-step operators "some successor is in $Z$" and "each successor is in $Z$". Such functions are monotone, so they have a least and a greatest fixed point by the [Knaster-Tarski theorem](/knaster-tarski-theorem/), and on a finite structure both are reached by simple iteration. Reachability, invariants, the CTL operators and the whole [modal mu-calculus](/modal-mu-calculus/) are least and greatest fixed points. This page is about the concept and its computation; the Knaster-Tarski page proves the existence theorem for all complete lattices.

## In plain words

Start with a guess, apply a rule to improve it, and repeat until the guess no longer changes. The final guess is a fixed point: the rule leaves it as it is.

In model checking the guess is a set of states. To find all states from which a bad state can be reached, start with the bad states, add every state that has a step into the current set, and repeat. The set only grows, and the number of states is finite, so it stops. The result is the smallest set that the rule cannot grow further.

Some questions start from the other end. To find the states from which the system can stay safe forever, start with all safe states, remove every state that has no step back into the set, and repeat. The set only shrinks, and the result is the largest set the rule keeps.

## The idea

**Monotone functions.** Let $S$ be a finite set of states and order its subsets by inclusion. A function $f : 2^S \to 2^S$ is **monotone** if $X \subseteq Y$ implies $f(X) \subseteq f(Y)$. The operators $Z \mapsto \mathit{pre}_\exists(Z) = \{s : R(s) \cap Z \ne \emptyset\}$ and $Z \mapsto \mathit{pre}_\forall(Z) = \{s : R(s) \subseteq Z\}$ are monotone, as are union and intersection with fixed sets. A formula in which a variable $Z$ occurs only under an even number of negations defines a monotone function of $Z$.

**Kinds of fixed points.** $X$ is a *fixed point* if $f(X) = X$, a *pre-fixed point* if $f(X) \subseteq X$, and a *post-fixed point* if $X \subseteq f(X)$. The **least fixed point** $\mu f$ is a fixed point contained in every fixed point, and the **greatest fixed point** $\nu f$ contains every fixed point. By the Knaster-Tarski theorem, for monotone $f$,

$$\mu f = \bigcap \{X : f(X) \subseteq X\}, \qquad \nu f = \bigcup \{X : X \subseteq f(X)\}.$$

**Kleene iteration on a finite set.** *Theorem.* Let $f : 2^S \to 2^S$ be monotone and $S$ finite. Define $Z_0 = \emptyset$ and $Z_{i+1} = f(Z_i)$. Then $Z_0 \subseteq Z_1 \subseteq \cdots$, there is an $m \le |S|$ with $Z_{m+1} = Z_m$, and $Z_m = \mu f$. Dually, $W_0 = S$, $W_{i+1} = f(W_i)$ decreases, becomes constant after at most $|S|$ steps, and the constant is $\nu f$.

*Proof.* *The chain increases.* $Z_0 = \emptyset \subseteq Z_1$. If $Z_i \subseteq Z_{i+1}$, then by monotonicity $Z_{i+1} = f(Z_i) \subseteq f(Z_{i+1}) = Z_{i+2}$.

*It becomes constant.* Each strict step $Z_i \subsetneq Z_{i+1}$ adds at least one state, and there are $|S|$ states, so at most $|S|$ steps are strict. Once $Z_{m+1} = Z_m$, every later set equals $Z_m$, so the first such $m$ is at most $|S|$, and $Z_m = f(Z_m)$ is a fixed point.

*It is the least one.* Let $Y$ be any pre-fixed point, $f(Y) \subseteq Y$. Then $Z_0 = \emptyset \subseteq Y$, and if $Z_i \subseteq Y$, then $Z_{i+1} = f(Z_i) \subseteq f(Y) \subseteq Y$. So $Z_m \subseteq Y$ for every pre-fixed point $Y$, in particular for every fixed point.

The dual statement has the same proof with the order reversed: $W_i$ decreases, and every post-fixed point $Y \subseteq f(Y)$ satisfies $Y \subseteq W_i$ for each $i$. $\blacksquare$

The same proof works on any finite lattice, and on any lattice in which each chain is finite: the number of steps is at most the height of the lattice. On an infinite lattice, the iteration up to $\omega$ reaches $\mu f$ when $f$ preserves unions of increasing chains (Scott continuity), and in general it must continue through the ordinals (Cousot and Cousot 1979).

**Approximants mean something.** The iterates are not only steps of an algorithm; each has a meaning. For $\mathsf{E}[\alpha\,\mathsf{U}\,\beta] = \mu Z.\, \beta \vee (\alpha \wedge \mathsf{EX}\,Z)$, the iterate $Z_i$ is the set of states with a witness path of fewer than $i$ steps, and for $\mathsf{EG}\,\alpha = \nu Z.\, \alpha \wedge \mathsf{EX}\,Z$, the iterate $W_i$ is the set of states with a path on which $\alpha$ holds for at least $i$ steps. A least fixed point says "eventually, in finitely many steps", and a greatest fixed point says "forever". The proofs are on the [computation tree logic](/computation-tree-logic/) page.

**Nested fixed points.** In $\nu X.\, \mu Y.\, f(X, Y)$, the inner least fixed point is a function of $X$, and it is monotone in $X$, so the outer greatest fixed point exists. Computing it by nested iteration costs up to $|S|$ inner iterations per outer one, so a nesting of depth $q$ costs up to about $(|S| + 1)^q$ evaluations of the body. The [Emerson-Lei algorithm](/emerson-lei-algorithm/) reuses inner values when the signs agree, and the cost then depends on the alternation between $\mu$ and $\nu$, not on the nesting.

## Examples

**Reachability.** On the two-process mutual exclusion structure of the [Kripke structure](/kripke-structure/) page, let $f(Z) = I \cup \mathit{post}(Z)$ with $I = \{(n, n, 1)\}$. The iterates have sizes $0, 1, 3, 6, 8, 8$: the breadth-first layers of the reachable set, which is $\mu f$. It is reached at the fourth iterate, and the fifth shows that nothing changes.

**$\mathsf{EG}$.** On the six-state structure of the [CTL labelling algorithm](/ctl-labelling-algorithm/) page, with $p$ in $0, 1, 2, 3, 5$ and edges $0 \to 1, 2$; $1 \to 3$; $2 \to 2, 4$; $3 \to 0$; $4 \to 5$; $5 \to 4$, take $f(Z) = [\![p]\!] \cap \mathit{pre}_\exists(Z)$. Then $W_0 = \{0, \ldots, 5\}$, $W_1 = \{0, 1, 2, 3, 5\}$ (state $4$ fails $p$), $W_2 = \{0, 1, 2, 3\}$ (state $5$ has no successor left in $W_1$), and $W_3 = W_2 = \nu f = [\![\mathsf{EG}\,p]\!]$.

**Least and greatest differ.** For $f(Z) = \mathit{pre}_\exists(Z)$ on any structure with a total relation, $\mu f = \emptyset$ and $\nu f = S$. The formula $\mu Z.\, \mathsf{EX}\,Z$ means "there is a path that eventually reaches a state that ...", with nothing to reach, so it is false everywhere; $\nu Z.\, \mathsf{EX}\,Z$ means "there is an infinite path", which is true everywhere.

**Non-example: no monotonicity.** $f(Z) = S \setminus Z$ is not monotone, and it has no fixed point when $S$ is non-empty. This is why the [modal mu-calculus](/modal-mu-calculus/) allows a fixed-point variable only under an even number of negations.

**Non-example: infinite branching.** Let the root $r$ have, for each $n \ge 1$, a successor that starts a path of $n$ states ending in a state with $p$. Then $r \models \mathsf{AF}\,p$, but the iterates of $\mu Z.\, p \vee \mathsf{AX}\,Z$ contain $r$ only at step $\omega + 1$, because the paths from $r$ have no common bound on their length. On a finite structure this cannot happen.

## Where it is used

- **Model checking.** The CTL operators, fair $\mathsf{EG}$, and every formula of the [modal mu-calculus](/modal-mu-calculus/) are fixed points. [Symbolic model checking](/symbolic-model-checking/) and [symbolic reachability](/symbolic-reachability/) compute them by Kleene iteration on BDDs; [mu-calculus model checking](/mu-calculus-model-checking/) studies the cost of nested ones.
- **Program analysis.** [Abstract interpretation](/abstract-interpretation/) and data-flow analysis compute least fixed points on lattices of abstract values, and use widening when the lattice has infinite chains.
- **Semantics.** The meaning of a recursive definition or a loop is the least fixed point of a monotone (continuous) function, by Kleene's fixed-point theorem.
- **Games and equivalences.** The winning region of a reachability game is a least fixed point, and [bisimulation](/bisimulation/) is the greatest fixed point of a refinement operator.
- **Numerical analysis.** There, a fixed point of $g$ is found by [fixed-point iteration](/fixed-point-iteration/), and the [Banach fixed-point theorem](/banach-fixed-point-theorem/) gives convergence for contractions. The setting is metric, not ordered, but the idea of repeating $x \leftarrow g(x)$ is the same.

## References
