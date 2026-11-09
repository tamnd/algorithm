---
tag: 6V8CKN
kind: definition
slug: herbrand-universe
name: Herbrand universe
aliases:
- Herbrand domain
- Herbrand base
- Herbrand interpretation
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: The set of ground terms built from the constants and function symbols of a clause set. A clause set has a model if and only if it has one whose domain is this set, with each term naming itself.
prereqs: [term, clausal-normal-form]
see_also: [herbrand-theorem, skolemization, robinson-completeness-theorem, first-order-theorem-proving, logic-programming, quantifier-instantiation, congruence-closure, horn-clause]
sources:
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 4, Section 4.3, The Herbrand universe of a set of clauses (the levels H_i, the Herbrand base, H-interpretations, and the reduction of unsatisfiability to H-interpretations)
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 2, Leo Bachmair and Harald Ganzinger, Resolution theorem proving (Herbrand interpretations as sets of ground atoms, and their use in the completeness proofs)
  - paper: "Jacques Herbrand, Recherches sur la théorie de la démonstration, thesis, University of Paris, 1930"
    locator: the domain of terms built from the symbols of a formula, on which the fundamental theorem is stated
---

The **Herbrand universe** of a set $S$ of [clauses](/clause/) is the set of all ground [terms](/term/) that can be built from the constants and function symbols of $S$, with one extra constant if $S$ has none. A **Herbrand interpretation** takes this set as its domain, lets each ground term denote itself, and is free only in which ground atoms it makes true. The main fact is that a set of clauses has a model if and only if it has a Herbrand model, so a search for models, or for a proof that none exists, can be done on ground terms alone. This is the base of [Herbrand's theorem](/herbrand-theorem/) and of the completeness of resolution.

## Definition

Let $S$ be a set of clauses. Its variables are read universally, and it has no existential quantifiers: those were removed by [Skolemization](/skolemization/).

**Herbrand universe.** Let $H_0$ be the set of constants in $S$; if $S$ has no constant, let $H_0 = \{a\}$ for a new constant $a$. For $i \ge 0$ let

$$H_{i+1} = H_i \cup \{ f(t_1, \ldots, t_n) : f \text{ is an } n\text{-ary function symbol of } S, \; n \ge 1, \; t_1, \ldots, t_n \in H_i \}.$$

The Herbrand universe is $H(S) = \bigcup_{i \ge 0} H_i$, and $H_i$ is its **level** $i$: the ground terms of depth at most $i$.

**Herbrand base.** The set $B(S)$ of all ground atoms $P(t_1, \ldots, t_n)$ with $P$ an $n$-ary predicate symbol of $S$ and $t_j \in H(S)$.

**Ground instance.** A clause $C\tau$, where $C \in S$ and $\tau$ maps every variable of $C$ to an element of $H(S)$.

**Herbrand interpretation.** A structure $I$ with domain $H(S)$ in which every constant $c$ denotes $c$, and every function symbol $f$ maps $t_1, \ldots, t_n$ to the term $f(t_1, \ldots, t_n)$. So each ground term denotes itself. Only the predicates are free, and $I$ is fully given by the set of ground atoms it makes true, a subset of $B(S)$. A **Herbrand model** of $S$ is a Herbrand interpretation that satisfies $S$.

**Proposition 1.** A Herbrand interpretation $I$ satisfies a clause $C$ if and only if it satisfies every ground instance of $C$.

*Proof.* An assignment of the variables of $C$ in $I$ maps them to elements of $H(S)$, which are ground terms, and it gives each literal of $C$ the truth value of the same literal in the ground instance $C\tau$ with that $\tau$. So $C$ is true under every assignment exactly when every $C\tau$ is true. $\square$

**Proposition 2.** A set $S$ of clauses has a model if and only if it has a Herbrand model.

*Proof.* A Herbrand model is a model. Conversely, let $M$ be a model of $S$, and if $H_0 = \{a\}$ was added, let $a$ denote any element of $M$. Every ground term $t$ then has a value $t^M$ in $M$. Let $I$ be the Herbrand interpretation in which a ground atom $P(t_1, \ldots, t_n)$ is true if and only if $P^M(t_1^M, \ldots, t_n^M)$ holds. Then every ground literal has the same truth value in $I$ and in $M$. Let $C \in S$ and $C\tau$ a ground instance. The clause $C$ holds in $M$ under every assignment, in particular under the one that sends each variable $x$ to $(x\tau)^M$, so $C\tau$ is true in $M$, hence in $I$. By Proposition 1, $I$ satisfies $C$. $\square$

**Size.** $H(S)$ is finite if and only if $S$ has no function symbol of arity at least 1, and then $H(S) = H_0$. Otherwise it is countably infinite. The levels grow as follows:

| symbols of $S$ | $\lvert H_0 \rvert$ | $\lvert H_1 \rvert$ | $\lvert H_2 \rvert$ | $\lvert H_3 \rvert$ |
|---|---|---|---|---|
| $a$, unary $f$ | 1 | 2 | 3 | 4 |
| $a$, unary $f$, binary $g$ | 1 | 3 | 13 | 183 |
| $a$, $b$, binary $g$ | 2 | 6 | 38 | 1446 |

The second row satisfies $|H_{i+1}| = 1 + |H_i| + |H_i|^2$, and the third $|H_{i+1}| = 2 + |H_i|^2$, since every term is a constant or a function symbol applied to terms of the level below. With a binary symbol the levels grow doubly exponentially, which is why instance enumeration is slow and [unification](/most-general-unifier/) instantiates only on demand.

## Examples and non-examples

**Example.** For $S = \{P(a), \lnot P(x) \vee P(f(x))\}$, the universe is $\{a, f(a), f(f(a)), \ldots\}$ and the base is $\{P(a), P(f(a)), \ldots\}$. The Herbrand interpretation that makes every atom true is a model. The one that makes only $P(a)$ true is not: the ground instance $\lnot P(a) \vee P(f(a))$ is false in it.

**Example with two symbols.** For constant $a$, unary $f$ and binary $g$, $H_1 = \{a, f(a), g(a, a)\}$.

**Example: Horn clauses.** If $S$ is a set of [Horn clauses](/horn-clause/) with a Herbrand model, then the intersection of all its Herbrand models is a Herbrand model, the **least Herbrand model**. *Proof.* Let $\{I_j\}$ be the nonempty family of Herbrand models, seen as sets of ground atoms, and $I = \bigcap_j I_j$. By Proposition 1 it is enough to check ground instances. For $A \vee \lnot B_1 \vee \cdots \vee \lnot B_k$: if every $B_l \in I$, then every $B_l$ is in every $I_j$, so $A$ is in every $I_j$, and $A \in I$. For $\lnot B_1 \vee \cdots \vee \lnot B_k$: some $B_l$ is missing from some $I_j$, so it is missing from $I$. $\square$ For the example above it is the whole base. In [logic programming](/logic-programming/) the least Herbrand model is the meaning of a program.

**Non-example: existential quantifiers.** $\{\lnot P(a), \exists x \, P(x)\}$ is satisfiable, but over the universe $\{a\}$ the only candidate for $x$ is $a$, and no Herbrand interpretation works. Proposition 2 needs clauses. Skolemize first: $\{\lnot P(a), P(c)\}$ has the universe $\{a, c\}$ and the Herbrand model $\{P(c)\}$.

**Non-example: equality as identity.** In a Herbrand interpretation $a$ and $b$ are different elements, so $\{a = b\}$ has no Herbrand model in which $=$ means identity, although it has models. With equality, the domain is the quotient of $H(S)$ by a congruence, as in [congruence closure](/congruence-closure/), or $=$ is treated as an ordinary predicate with the equality axioms.

**Non-example: a non-Herbrand model is not wrong, only different.** $\{P(a)\}$ has the model with domain $\{0, 1\}$, $a = 0$ and $P = \{0\}$. The Herbrand model built from it by Proposition 2 is $\{P(a)\}$ on the one-element universe $\{a\}$. Information about elements that no term names is lost, and it is not needed for satisfiability.

## Related definitions

- [Herbrand's theorem](/herbrand-theorem/): a set of clauses is unsatisfiable exactly when some finite set of its ground instances over $H(S)$ is propositionally unsatisfiable.
- [Skolemization](/skolemization/): removes existential quantifiers by new function symbols, which then enlarge the Herbrand universe.
- [Robinson completeness theorem](/robinson-completeness-theorem/): its proof refutes ground instances over $H(S)$ and lifts the steps.
- [Quantifier instantiation](/quantifier-instantiation/): SMT solvers choose finitely many ground instances, in the spirit of Herbrand's theorem.
- **Bernays-Schönfinkel class.** Sentences whose Skolem form has only constants have a finite Herbrand universe, so finitely many ground instances decide them; see [first-order theorem proving](/first-order-theorem-proving/).

## References
