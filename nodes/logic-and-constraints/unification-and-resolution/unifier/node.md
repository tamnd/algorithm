---
tag: B05FB8
kind: definition
slug: unifier
name: Unifier
area: logic-and-constraints/unification-and-resolution
level: intro
summary: A substitution that makes two terms, or all equations of a set, syntactically identical.
prereqs: [substitution, term]
see_also: [most-general-unifier, unification-problem, mgu-existence-theorem, idempotent-substitution, occurs-check, term-matching, equational-unification, semi-unification-problem]
sources:
  - paper: doi:10.1145/321250.321253
    title: J. A. Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965, pages 23 to 41
    locator: the sections on substitution and unification (unifiers of a finite set of expressions, the unification algorithm and the unification theorem)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 4.5, Syntactic unification (unification problems, unifiers and most general unifiers)
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 2 (syntactic unification)
---

A **unifier** of two [terms](/term/) $s$ and $t$ is a [substitution](/substitution/) $\sigma$ with $s\sigma = t\sigma$: after the replacement, the two terms are the same tree, symbol for symbol. A unifier of a set of equations makes each equation an identity. This page defines the object. The [unification problem](/unification-problem/) asks to find one, a [most general unifier](/most-general-unifier/) is the best one, and the [unification theorem](/mgu-existence-theorem/) says that the best one exists when any one exists.

## Definition

Let $T(\Sigma, V)$ be the set of first-order terms over a signature $\Sigma$ and a set of variables $V$. An **equation** is a pair written $s \doteq t$ of terms. A **unification problem** is a finite set $E = \{s_1 \doteq t_1, \ldots, s_m \doteq t_m\}$, and $\mathrm{Var}(E)$ is the set of variables that occur in it.

A substitution $\sigma$ is a **unifier** of $E$ if

$$s_i\sigma = t_i\sigma \quad \text{for each } i = 1, \ldots, m,$$

where $=$ is syntactic identity of terms. $\mathcal{U}(E)$ is the set of all unifiers of $E$. $E$ is **unifiable** if $\mathcal{U}(E) \ne \emptyset$. A unifier of two terms $s, t$ is a unifier of $\{s \doteq t\}$. A unifier of a set of terms $\{t_1, \ldots, t_k\}$ is a $\sigma$ with $t_1\sigma = \cdots = t_k\sigma$, the form Robinson used.

Three facts follow at once from the definition.

- **Closed under instances.** If $\sigma \in \mathcal{U}(E)$, then $\sigma\lambda \in \mathcal{U}(E)$ for each substitution $\lambda$, because $s_i\sigma\lambda = (s_i\sigma)\lambda = (t_i\sigma)\lambda$. So a unifiable problem has infinitely many unifiers, for example $\sigma\{w \mapsto w'\}$ for each pair of variables $w, w'$ outside $\mathrm{Var}(E)$, and a [most general](/most-general-unifier/) one is the useful answer.
- **Only the variables of $E$ matter.** If $\sigma$ and $\sigma'$ agree on $\mathrm{Var}(E)$, then $\sigma \in \mathcal{U}(E)$ if and only if $\sigma' \in \mathcal{U}(E)$.
- **Pairing.** $\sigma$ unifies $\{s_1 \doteq t_1, \ldots, s_m \doteq t_m\}$ if and only if it unifies the single equation $h(s_1, \ldots, s_m) \doteq h(t_1, \ldots, t_m)$ for a new symbol $h$ of arity $m$. So sets of equations and pairs of terms are the same problem.

A unifier is a solution of the equations in the **free term algebra**: the terms are equal as trees, not modulo any law. Unifiers modulo a theory such as commutativity are the subject of [equational unification](/equational-unification/).

## Examples and non-examples

Below $a, b$ are constants, $f, g$ are function symbols and $x, y, z$ are variables.

| problem | a unifier | why |
|---|---|---|
| $f(x, b) \doteq f(a, y)$ | $\{x \mapsto a,\ y \mapsto b\}$ | both sides become $f(a, b)$ |
| $f(x, g(y)) \doteq f(g(z), x)$ | $\{x \mapsto g(y),\ z \mapsto y\}$ | both sides become $f(g(y), g(y))$ |
| $f(x, g(y)) \doteq f(g(z), x)$ | $\{x \mapsto g(a),\ y \mapsto a,\ z \mapsto a\}$ | an instance of the row above |
| $x \doteq y$ | $\{x \mapsto y\}$, and also $\{y \mapsto x\}$ and $\{x \mapsto z,\ y \mapsto z\}$ | many unifiers; the first two are equally general |

Non-examples, where no unifier exists:

- **Clash.** $f(x) \doteq g(y)$: each instance of the left side has root $f$, and each instance of the right side has root $g$.
- **Occurs.** $x \doteq f(x)$: for each $\sigma$, $|f(x)\sigma| = |x\sigma| + 1$, so the sides never have the same size. This is the case that the [occurs check](/occurs-check/) detects.
- **Inconsistent bindings.** $f(x, x) \doteq f(a, b)$: a unifier must map $x$ to $a$ and to $b$.

A substitution that unifies only part of the set is not a unifier: $\{x \mapsto a\}$ unifies $x \doteq a$ but not $\{x \doteq a,\ x \doteq b\}$, and this set has no unifier.

## Related definitions

- A [most general unifier](/most-general-unifier/) $\sigma$ is a unifier with $\sigma \le \theta$ for each unifier $\theta$. It is unique up to renaming, and it can be chosen [idempotent](/idempotent-substitution/).
- A **matcher** of $s$ to $t$ is a $\sigma$ with $s\sigma = t$; it is a unifier where only one side may change. See [term matching](/term-matching/).
- A **semi-unifier** of $s \le t$ is a $\sigma$ such that $t\sigma$ is an instance of $s\sigma$. See the [semi-unification problem](/semi-unification-problem/).
- An **E-unifier** satisfies $s\sigma =_E t\sigma$ in an equational theory $E$. See [equational unification](/equational-unification/).
- An **anti-unifier** (a generalization) goes the other way: a term $g$ with substitutions that turn $g$ into $s$ and into $t$. See the [anti-unification problem](/anti-unification-problem/).

## References
