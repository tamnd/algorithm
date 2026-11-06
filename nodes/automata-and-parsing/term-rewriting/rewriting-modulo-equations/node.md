---
tag: NGQJZP
kind: concept
slug: rewriting-modulo-equations
name: Rewriting modulo equations
aliases:
- rewriting modulo equational theory
- AC rewriting
- class rewriting
area: automata-and-parsing/term-rewriting
level: advanced
summary: Rewriting where some equations, such as associativity and commutativity, are built into matching.
prereqs: [term-rewriting-system, equational-theory, term-matching]
see_also: [ac-matching, ac-unification-problem, stickel-ac-unification, equational-unification, knuth-bendix-completion, unfailing-completion, word-problem, rewriting-logic]
sources:
  - paper: doi:10.1145/322248.322251
    title: Gerald E. Peterson and Mark E. Stickel, Complete sets of reductions for some equational theories, Journal of the ACM 28(2) (1981)
    locator: pp. 233 to 264 (rewriting and completion modulo associativity and commutativity, extended rules)
  - paper: doi:10.1137/0215084
    title: Jean-Pierre Jouannaud and Hélène Kirchner, Completion of a set of rules modulo a set of equations, SIAM Journal on Computing 15(4) (1986)
    locator: pp. 1155 to 1194 (rewriting with R modulo E, coherence, and the Church-Rosser property modulo E)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 11.1, Rewriting modulo equational theories (p. 265 onwards)
  - book: isbn:9780444880741
    title: Nachum Dershowitz and Jean-Pierre Jouannaud, Rewrite Systems, in J. van Leeuwen (editor), Handbook of Theoretical Computer Science, Volume B, Elsevier, 1990
    locator: pp. 243 to 320 (the section on extended rewriting and rewriting modulo a congruence)
---

**Rewriting modulo equations** splits a set of equations into two parts: rules $R$, used from left to right, and equations $E$, such as commutativity, that cannot be oriented without losing [termination](/termination/). Terms are compared and matched up to $E$, so a rule applies to a term if it applies to some $E$-equal term. With $E$ = associativity and commutativity (AC), this gives convergent systems for abelian groups, Boolean rings and other structures that ordinary rewriting cannot handle, and it is the computation model of Maude and of AC-based theorem provers.

## In plain words

Some laws cannot be used as one-way simplification rules. "A plus B equals B plus A" has no simpler side: used as a rule, it swaps the two parts back and forth forever. The fix is to stop treating such laws as steps at all, and to treat expressions that differ only by them as the same expression.

So the rewriting engine sees a sum as a bag of terms, without order and without brackets. A rule such as "x plus minus x gives zero" then applies to any sum that contains some term and its negation, wherever they stand. The price is matching: finding how a rule fits a bag of terms means trying many ways to split the bag, which can be slow.

## The idea

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions with root $\varepsilon$, $t|_p$ and $t[s]_p$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure. For a set of equations $E$, $\approx_E$ is the [equational theory](/equational-theory/) it generates.

**Class rewriting.** The relation $R/E$ rewrites equivalence classes: $s \to_{R/E} t$ iff $s \approx_E s' \to_R t' \approx_E t$ for some $s', t'$. A system is **convergent modulo $E$** if $R/E$ terminates and is confluent on classes. Then $s \approx_{R \cup E} t$ iff the normal forms of $s$ and $t$ are $E$-equal, which decides the word problem of $R \cup E$ when $\approx_E$ is decidable. But a single $R/E$ step is hard to compute: it asks for some term in the class of $s$ that contains a redex, and the classes can be large or infinite.

**$R, E$-rewriting.** The practical relation only matches modulo $E$, at the positions of $s$ itself: $s \to_{R,E} t$ iff $s|_p \approx_E l\sigma$ for some rule $l \to r$, position $p$ and substitution $\sigma$, and $t = s[r\sigma]_p$. Finding $\sigma$ is **$E$-matching**; for AC it is [AC-matching](/ac-matching/), which is NP-complete but fast on typical terms. Since $\to_{R,E} \subseteq \to_{R/E}$, termination of $R/E$ gives termination of $R, E$-rewriting.

**Coherence and extended rules.** $R, E$-rewriting can miss steps of $R/E$. For AC, a rule $x + (-x) \to 0$ does not apply to $a + b + (-a)$ at any position, since no subterm, read modulo AC, is a sum of exactly a term and its negation. The fix (Peterson and Stickel, 1981) adds, for each rule $l \to r$ whose left side has an AC symbol $+$ at the root, the **extended rule** $l + z \to r + z$ with a new variable $z$. With the extended rules, $R, E$-rewriting simulates $R/E$-rewriting: whenever $s \to_{R/E} t$, there is $s \to_{R,E} t'$ with $t' \approx_E t$, so the two relations have the same normal forms up to AC. Jouannaud and Kirchner (1986) gave the general condition, called coherence, for other theories $E$.

**Termination.** $R/E$ terminates iff some reduction ordering $>$ is compatible with $E$ ($s' \approx_E s > t \approx_E t'$ implies $s' > t'$) and orients $R$. For AC, the usual path orders are not AC-compatible; AC-compatible versions of the [recursive path ordering](/recursive-path-ordering/) and of [polynomial interpretations](/polynomial-interpretation/) exist. A polynomial interpretation is AC-compatible when $[+]$ is an associative and commutative polynomial, such as $x + y + c$ or $axy + b(x + y) + c$ with suitable coefficients.

**Completion modulo $E$.** [Knuth-Bendix completion](/knuth-bendix-completion/) extends to rewriting modulo $E$ when $E$ has a finitary unification algorithm. Critical pairs are computed with [$E$-unification](/equational-unification/), for AC with [AC-unification](/ac-unification-problem/) by [Stickel's algorithm](/stickel-ac-unification/), and extended rules are added for the AC symbols.

## Examples

**Abelian groups.** Ordinary completion fails on the axioms of abelian groups, because commutativity $x + y \approx y + x$ cannot be oriented. Modulo AC for $+$, the system

$$x + 0 \to x, \quad x + (-x) \to 0, \quad -(-x) \to x, \quad -0 \to 0, \quad -(x + y) \to (-x) + (-y),$$

with the extended rule $x + (-x) + z \to z$, is convergent modulo AC. We checked this by a program that implements AC-matching by brute force on flattened sums and explores all reductions of 400 random ground terms over $a, b, 0, +, -$: each term had exactly one normal form up to AC, and two terms had the same normal form iff they denote the same element $m a + n b$ of $\mathbb{Z}^2$. The normal forms are the sums of copies of $a$ or $-a$, and of $b$ or $-b$, without a term and its negation together. Without the extended rule, $a + b + (-a)$ is irreducible, though it equals $b$.

**One AC step.** $-(a + (-b))$ has one step, by the rule for $-(x + y)$ with $x \mapsto a$, $y \mapsto -b$ (or the swapped match, which gives an AC-equal result), to $(-a) + (-(-b))$, and then $-(-b) \to b$ gives the normal form $b + (-a)$.

**Boolean rings.** With $\oplus$ (exclusive or) and $\wedge$ both AC, the rules $x \oplus 0 \to x$, $x \oplus x \to 0$, $x \wedge 1 \to x$, $x \wedge 0 \to 0$, $x \wedge x \to x$, $x \wedge (y \oplus z) \to (x \wedge y) \oplus (x \wedge z)$ together with extended rules give normal forms that are sums of products of distinct variables: the algebraic normal form of a Boolean function. Theorem provers for propositional and first-order logic use this normal form.

**Non-examples.**

- Commutativity as a rule, $x + y \to y + x$, is not rewriting modulo an equation: it does not terminate, since $a + b \to b + a \to a + b$.
- Ordered rewriting, used by [unfailing completion](/unfailing-completion/), applies an equation $x + y \approx y + x$ only when the result is smaller in a total order on ground terms. That keeps $E$ inside the rules, instead of building it into matching.

## Where it is used

- [Knuth-Bendix completion](/knuth-bendix-completion/) modulo AC, for abelian groups, commutative rings and Boolean rings.
- [Rewriting logic](/rewriting-logic/) and the language Maude, where operators can be declared associative, commutative, or with an identity, and rules apply modulo these axioms.
- Equational theorem provers and [superposition](/superposition/) provers with built-in AC.
- Computer algebra and SMT solvers, which normalize sums and products modulo AC by flattening and sorting arguments.
- The [word problem](/word-problem/) for theories with AC operators, decided by normal forms modulo AC.

## References
