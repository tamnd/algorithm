---
tag: TSJEB3
kind: concept
slug: term-algebra
name: Term algebra
aliases:
- Herbrand universe
area: automata-and-parsing/term-rewriting
level: core
summary: The algebra whose carrier is the set of all ground terms over a signature.
prereqs: [term, substitution]
see_also: [herbrand-universe, equational-theory, birkhoff-completeness-theorem, structural-induction, inductive-theorem-proving, word-problem, unification-problem]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Sections 3.2 to 3.4 (algebras, homomorphisms and congruences; free algebras; term algebras)
  - paper: doi:10.1145/321992.321997
    title: Joseph A. Goguen, James W. Thatcher, Eric G. Wagner and Jesse B. Wright, Initial algebra semantics and continuous algebras, Journal of the ACM 24(1) (1977)
    locator: pp. 68 to 95 (the term algebra as the initial algebra of a signature)
  - book: isbn:9780444880741
    title: Nachum Dershowitz and Jean-Pierre Jouannaud, Rewrite Systems, in J. van Leeuwen (editor), Handbook of Theoretical Computer Science, Volume B, Elsevier, 1990
    locator: pp. 243 to 320 (the semantics of equations, algebras, free algebras and initial algebras)
---

The **term algebra** of a signature $\Sigma$ is the algebra whose elements are the [terms](/term/) over $\Sigma$ and whose operations build bigger terms: the operation for $f$ takes $t_1, \ldots, t_n$ to the term $f(t_1, \ldots, t_n)$. The ground term algebra $T(\Sigma)$ is the **initial** $\Sigma$-algebra, and $T(\Sigma, V)$ is the **free** $\Sigma$-algebra over the variables $V$: each way to give values to the symbols and variables extends in exactly one way to a value for every term. This is the algebraic form of definition by recursion on terms, and the reason why substitutions, evaluation and [structural induction](/structural-induction/) work.

## In plain words

Take a set of operation names, each with a number of arguments. Write every expression that you can build from them. Do not compute anything: the expression "one plus two" and the expression "two plus one" are different objects, because they are written differently. This collection of expressions, where the only thing an operation does is to build a larger expression, is the term algebra.

It is the most general structure for the given operations. To compute in any concrete structure, such as the integers, you only say what each operation means there, and the value of every expression follows, in one way only. Two expressions get the same value exactly when the meanings of the operations force it. This is why equations and rewrite rules over expressions say something about all structures at once.

## The idea

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, substitutions $\sigma$ applied as $t\sigma$.

A **$\Sigma$-algebra** $\mathcal{A}$ is a non-empty set $A$, the carrier, with a function $f^{\mathcal{A}} : A^n \to A$ for each $f \in \Sigma_n$. A **homomorphism** $h : \mathcal{A} \to \mathcal{B}$ is a map with $h(f^{\mathcal{A}}(a_1, \ldots, a_n)) = f^{\mathcal{B}}(h(a_1), \ldots, h(a_n))$ for all $f$ and arguments.

The **term algebra** $\mathcal{T}(\Sigma, V)$ has carrier $T(\Sigma, V)$ and $f^{\mathcal{T}}(t_1, \ldots, t_n) = f(t_1, \ldots, t_n)$. When $\Sigma_0 \ne \emptyset$, the **ground term algebra** $\mathcal{T}(\Sigma)$ has carrier $T(\Sigma)$, the Herbrand universe of $\Sigma$.

**Freeness.** For each $\Sigma$-algebra $\mathcal{A}$ and each map $\alpha : V \to A$ (an assignment), there is exactly one homomorphism $[\![\cdot]\!]_\alpha : \mathcal{T}(\Sigma, V) \to \mathcal{A}$ that extends $\alpha$:

$$[\![x]\!]_\alpha = \alpha(x), \qquad [\![f(t_1, \ldots, t_n)]\!]_\alpha = f^{\mathcal{A}}([\![t_1]\!]_\alpha, \ldots, [\![t_n]\!]_\alpha).$$

*Proof.* These equations define $[\![t]\!]_\alpha$ by recursion on the structure of $t$, which is well-founded because a term is finite. The map is a homomorphism by its second equation. If $h$ is another homomorphism that extends $\alpha$, then $h(t) = [\![t]\!]_\alpha$ by induction on $t$: for a variable both are $\alpha(x)$, and for $f(t_1, \ldots, t_n)$ both apply $f^{\mathcal{A}}$ to equal values by the hypothesis. The recursion is well defined only because each term is built in exactly one way: $f(t_1, \ldots, t_n) = g(u_1, \ldots, u_m)$ forces $f = g$ and $t_i = u_i$. $\blacksquare$

With $V = \emptyset$ the same argument gives **initiality**: for every $\Sigma$-algebra $\mathcal{A}$ there is exactly one homomorphism $\mathcal{T}(\Sigma) \to \mathcal{A}$, the evaluation of ground terms.

**Consequences.**

- A [substitution](/substitution/) is the unique homomorphism $\mathcal{T}(\Sigma, V) \to \mathcal{T}(\Sigma, V)$ that extends a map $V \to T(\Sigma, V)$. This is why $(t\sigma)\tau = t(\sigma\tau)$ and why substitutions commute with the term structure.
- The **kernel** of a homomorphism, $\{(s, t) \mid h(s) = h(t)\}$, is a congruence: an equivalence closed under the operations. Every congruence $\approx$ on $\mathcal{T}(\Sigma)$ gives a quotient algebra $\mathcal{T}(\Sigma)/{\approx}$.
- For a set of equations $E$, the quotient $\mathcal{T}(\Sigma, V)/{\approx_E}$ by the [equational theory](/equational-theory/) is free in the class of models of $E$, and $\mathcal{T}(\Sigma)/{\approx_E}$ is initial in it. An equation holds in all models of $E$ iff it holds in the free algebra over a countable $V$; this is a step of the [Birkhoff completeness theorem](/birkhoff-completeness-theorem/).
- An equation that holds in the initial algebra $\mathcal{T}(\Sigma)/{\approx_E}$, that is, for all ground instances, is an **inductive theorem** of $E$. These are the targets of [inductive theorem proving](/inductive-theorem-proving/) and [rewriting induction](/rewriting-induction/).

The slogan for the initial algebra is "no junk and no confusion": every element is the value of a ground term (no junk), and two ground terms have the same value only if the equations force it (no confusion).

## Examples

**Evaluation of numerals.** Let $\Sigma = \{0/0, s/1, +/2\}$ and let $\mathcal{N}$ be the natural numbers with $0^{\mathcal{N}} = 0$, $s^{\mathcal{N}}(n) = n + 1$ and $+^{\mathcal{N}}$ the sum. The unique homomorphism $h : \mathcal{T}(\Sigma) \to \mathcal{N}$ gives $h(s(s(0)) + s(0)) = 3$. There are 13 ground terms of height at most 2; under $h$, five of them have value 0, six have value 1, and two, $s(s(0))$ and $s(0) + s(0)$, have value 2. So $h$ is not injective: $\mathcal{N}$ has confusion with respect to $\mathcal{T}(\Sigma)$. Its kernel is exactly $\approx_E$ on ground terms for $E = \{0 + y \approx y,\ s(x) + y \approx s(x + y)\}$, so $\mathcal{N} \cong \mathcal{T}(\Sigma)/{\approx_E}$ is the initial model of these equations.

**Junk.** The integers $\mathbb{Z}$, with $0$, successor and sum, are also a model of $E$, but $-1$ is not the value of a ground term. So $\mathbb{Z}$ is not initial. Indeed there is no homomorphism $h : \mathbb{Z} \to \mathcal{N}$: it would need $h(0) = 0$ and $h(-1) + 1 = h(s(-1)) = h(0) = 0$, which no natural number satisfies.

**Commutativity is an inductive theorem.** $x + y \approx y + x$ holds for all ground instances in $\mathcal{T}(\Sigma)/{\approx_E}$, but not in the free algebra $\mathcal{T}(\Sigma, V)/{\approx_E}$: the terms $x + y$ and $y + x$ are different normal forms of the convergent system $0 + y \to y,\ s(x) + y \to s(x + y)$, so they are not $E$-equal. This is the gap between equational and inductive reasoning.

**The Herbrand universe.** For $\Sigma = \{a/0, f/1\}$, $T(\Sigma) = \{a, f(a), f(f(a)), \ldots\}$, which is isomorphic to $\mathcal{N}$ with zero and successor. If $\Sigma$ has a symbol of arity at least 1 and a constant, the Herbrand universe is infinite. See [Herbrand universe](/herbrand-universe/).

**Syntactic unification.** Solving $s\sigma = t\sigma$ is solving an equation in the free algebra $\mathcal{T}(\Sigma, V)$. In a quotient $\mathcal{T}(\Sigma, V)/{\approx_E}$ the same question is [unification modulo a theory](/undecidability-of-unification-modulo-theories/).

## Where it is used

- [Equational theory](/equational-theory/) and the [Birkhoff completeness theorem](/birkhoff-completeness-theorem/): the free algebra $\mathcal{T}(\Sigma, V)/{\approx_E}$ is the model that makes the proof work.
- [Word problem](/word-problem/): asks whether two terms are equal in $\mathcal{T}(\Sigma, V)/{\approx_E}$.
- [Inductive theorem proving](/inductive-theorem-proving/) and [rewriting induction](/rewriting-induction/): prove equations in the initial algebra.
- [Structural induction](/structural-induction/): the proof principle that freeness gives.
- [Unification problem](/unification-problem/): equations in the free term algebra.
- Algebraic specification of abstract data types, where a data type is the initial algebra of its equations (Goguen, Thatcher, Wagner and Wright, 1977).

## References
