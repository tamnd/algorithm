---
tag: XG9E0W
kind: theorem
slug: knaster-tarski-theorem
name: Knaster-Tarski theorem
aliases:
- Tarski fixpoint theorem
- Tarski fixed-point theorem
- Knaster-Tarski fixed-point theorem
area: logic-and-constraints/model-checking
level: advanced
summary: Every monotone function on a complete lattice has a least and a greatest fixed point, and its fixed points form a complete lattice. It gives the semantics of the modal mu-calculus.
prereqs: [fixed-point]
see_also: [fixed-point, modal-mu-calculus, computation-tree-logic, emerson-lei-algorithm, abstract-interpretation, bisimulation, banach-fixed-point-theorem, join-semilattice]
sources:
  - paper: doi:10.2140/pjm.1955.5.285
    title: Alfred Tarski, A lattice-theoretical fixpoint theorem and its applications, Pacific Journal of Mathematics 5(2), 1955, pages 285 to 309
    locator: Theorem 1 (the set of fixed points of a monotone function on a complete lattice is a non-empty complete lattice, with the least and greatest fixed points given by the meet of the pre-fixed points and the join of the post-fixed points)
  - paper: "Bronisław Knaster, Un théorème sur les fonctions d'ensembles, Annales de la Société Polonaise de Mathématique 6, 1928, pages 133 to 134"
    locator: the fixed-point theorem for monotone functions on the subsets of a set, proved with Tarski
  - paper: "Anne C. Davis, A characterization of complete lattices, Pacific Journal of Mathematics 5(2), 1955, pages 311 to 319"
    locator: the converse (a lattice on which every monotone function has a fixed point is complete)
  - book: "B. A. Davey and H. A. Priestley, Introduction to Lattices and Order, second edition, Cambridge University Press, 2002"
    locator: Chapter 2 (complete lattices) and Chapter 8 (fixpoint theorems, the Knaster-Tarski theorem and the iteration of monotone and continuous maps)
  - paper: doi:10.2140/pjm.1979.82.43
    title: Patrick Cousot and Radhia Cousot, Constructive versions of Tarski's fixed point theorems, Pacific Journal of Mathematics 82(1), 1979, pages 43 to 57
    locator: the least fixed point as the limit of the transfinite iteration from the bottom element
---

The Knaster-Tarski theorem says that a monotone function on a complete lattice has a least and a greatest fixed point, given by explicit formulas, and that its fixed points form a complete lattice themselves. Knaster and Tarski proved it in 1928 for the lattice of subsets of a set, and Tarski stated it for all complete lattices in 1955. In model checking it is the reason that the least and greatest fixed points $\mu Z.\, \varphi$ and $\nu Z.\, \varphi$ of the [modal mu-calculus](/modal-mu-calculus/) and the fixed-point equations of [CTL](/computation-tree-logic/) make sense. The theorem is about existence and characterization; the [fixed point](/fixed-point/) page shows how the fixed points are computed by iteration on a finite set of states.

## Statement

A **complete lattice** is a partially ordered set $(L, \le)$ in which every subset $X \subseteq L$ has a least upper bound $\bigvee X$ and a greatest lower bound $\bigwedge X$. In particular $L$ has a bottom $\bot = \bigvee \emptyset$ and a top $\top = \bigwedge \emptyset$. The main example here is the power set $(2^S, \subseteq)$ of a set of states, with union and intersection.

A function $f : L \to L$ is **monotone** if $x \le y$ implies $f(x) \le f(y)$. An element $x$ is a *fixed point* if $f(x) = x$, a *pre-fixed point* if $f(x) \le x$, and a *post-fixed point* if $x \le f(x)$.

**Theorem (Knaster-Tarski).** Let $L$ be a complete lattice and $f : L \to L$ monotone. Then

1. $\mu f = \bigwedge \{x \in L : f(x) \le x\}$ is a fixed point of $f$, and it is below every fixed point (the *least* fixed point);
2. $\nu f = \bigvee \{x \in L : x \le f(x)\}$ is a fixed point of $f$, and it is above every fixed point (the *greatest* fixed point);
3. the set $\mathrm{Fix}(f)$ of fixed points, ordered by $\le$, is a complete lattice.

## In plain words

Think of a rule that takes a set of states and gives back a set of states, and that gives back a bigger set whenever you feed it a bigger set. The theorem says that such a rule always has a set it leaves unchanged. More than that: among all the sets it leaves unchanged there is a smallest and a largest, and there is a direct description of each.

The smallest one is the common part of all sets that the rule does not grow. The largest one is everything that lies in some set that the rule does not shrink. Model checkers use the smallest kind for "eventually" and the largest kind for "forever".

## Proof

*Part 1.* Let $P = \{x : f(x) \le x\}$ be the set of pre-fixed points, and $a = \bigwedge P$. It exists because $L$ is complete, and $P$ is not empty because $\top \in P$.

- $f(a) \le a$. For each $x \in P$ we have $a \le x$, so $f(a) \le f(x) \le x$ by monotonicity. So $f(a)$ is a lower bound of $P$, and therefore $f(a) \le \bigwedge P = a$.
- $a \le f(a)$. From $f(a) \le a$ and monotonicity, $f(f(a)) \le f(a)$, so $f(a) \in P$. Then $a = \bigwedge P \le f(a)$.

So $f(a) = a$. Every fixed point is a pre-fixed point, so it is in $P$ and above $a$. So $a$ is the least fixed point.

*Part 2.* Apply part 1 to the dual lattice $(L, \ge)$, in which joins and meets swap and $f$ is still monotone. Pre-fixed points of the dual are the post-fixed points of $L$, so $\nu f = \bigvee \{x : x \le f(x)\}$ is a fixed point above every fixed point.

*Part 3.* Let $Y \subseteq \mathrm{Fix}(f)$, and $b = \bigvee Y$ in $L$. The interval $[b, \top] = \{x \in L : b \le x\}$ is a complete lattice, with the joins and meets of $L$ (for non-empty subsets) and bottom $b$. The function $f$ maps it to itself: if $b \le x$, then for each $y \in Y$, $y = f(y) \le f(x)$ because $y \le b \le x$, so $b \le f(x)$. By part 1 applied to $f$ on $[b, \top]$, there is a least fixed point $c$ of $f$ in $[b, \top]$. Then $c$ is a fixed point above every element of $Y$, and every fixed point above all of $Y$ is above $b$, so it is in $[b, \top]$ and above $c$. So $c$ is the least upper bound of $Y$ in $\mathrm{Fix}(f)$. The greatest lower bound is found dually in $[\bot, \bigwedge Y]$. So every subset of $\mathrm{Fix}(f)$ has a join and a meet in $\mathrm{Fix}(f)$. $\blacksquare$

Note that the proof does not iterate $f$. It works for every monotone $f$, also when the iteration from $\bot$ needs infinitely many steps.

## Consequences

- **Semantics of fixed-point logics.** In the [modal mu-calculus](/modal-mu-calculus/), the body of $\mu Z.\, \varphi$ defines a monotone function on $(2^S, \subseteq)$ when $Z$ occurs only positively. The theorem says that $[\![\mu Z.\, \varphi]\!]$ and $[\![\nu Z.\, \varphi]\!]$ exist, and its formulas $\bigcap \{Z : f(Z) \subseteq Z\}$ and $\bigcup \{Z : Z \subseteq f(Z)\}$ are the standard definitions. The fixed-point characterization of $\mathsf{EG}$ and $\mathsf{EU}$ in [CTL](/computation-tree-logic/) uses exactly these two formulas.
- **Proof principles.** To show $\mu f \le x$, it is enough to show $f(x) \le x$ (induction). To show $x \le \nu f$, it is enough to show $x \le f(x)$ (coinduction). The proof that two states are [bisimilar](/bisimulation/) by exhibiting a bisimulation relation is coinduction for a greatest fixed point.
- **Computation.** On a finite lattice, the iteration $\bot, f(\bot), f(f(\bot)), \ldots$ reaches $\mu f$ in at most the height of the lattice; on $2^S$ that is $|S|$ steps. The proof is on the [fixed point](/fixed-point/) page, and nested fixed points are computed by the [Emerson-Lei algorithm](/emerson-lei-algorithm/). In general the iteration is transfinite (Cousot and Cousot 1979).
- **Program analysis.** [Abstract interpretation](/abstract-interpretation/) defines the meaning of a program as the least fixed point of a monotone function on a lattice of abstract states.
- **Set theory.** The theorem on $2^A$ gives a short proof of the Schröder-Bernstein theorem: if $g : A \to B$ and $h : B \to A$ are injective, the monotone map $X \mapsto A \setminus h(B \setminus g(X))$ has a fixed point $X$, and $g$ on $X$ together with $h^{-1}$ on $A \setminus X$ is a bijection.

## Tightness

- **Monotonicity is needed.** On the two-element lattice $\{0, 1\}$, the map $f(x) = 1 - x$ has no fixed point. In the mu-calculus this is why a bound variable may not occur under an odd number of negations.
- **Completeness is needed.** On the natural numbers with the usual order, which form a lattice without a top, the monotone map $n \mapsto n + 1$ has no fixed point. Conversely, Davis (1955) proved that a lattice on which every monotone map has a fixed point must be complete. So the theorem characterizes complete lattices.
- **$\mathrm{Fix}(f)$ is a complete lattice, but not a sublattice.** On the subsets of $\{a, b, c\}$, let $f(X) = X$ when $|X| \le 1$ and $f(X) = \{a, b, c\}$ when $|X| \ge 2$. It is monotone, and its fixed points are $\emptyset$, the three singletons and $\{a, b, c\}$. The join of $\{a\}$ and $\{b\}$ in $\mathrm{Fix}(f)$ is $\{a, b, c\}$, but in $2^S$ it is $\{a, b\}$.
- **Least and greatest can differ widely.** For $f(Z) = \mathit{pre}_\exists(Z)$ on a structure with a total relation, $\mu f = \emptyset$ and $\nu f = S$, which is the difference between $\mu Z.\, \mathsf{EX}\,Z$ (false) and $\nu Z.\, \mathsf{EX}\,Z$ (true).
- **No uniqueness and no convergence from an arbitrary start.** Unlike the [Banach fixed-point theorem](/banach-fixed-point-theorem/) for contractions, there may be many fixed points, and the iteration from an element that is neither a pre- nor a post-fixed point need not converge to any of them.

## History

Bronisław Knaster published the theorem for monotone functions on the subsets of a set in 1928, in a note that credits the idea to work with Alfred Tarski. Tarski stated and proved the general lattice-theoretic form in a lecture in 1939 and in print in 1955, with applications to set theory, topology and logic. In the same journal issue, Anne Davis proved the converse. Kozen (1983) used the theorem to define the modal mu-calculus, and it underlies the fixed-point algorithms of model checking since Clarke and Emerson (1981) and Queille and Sifakis (1982).

## References
