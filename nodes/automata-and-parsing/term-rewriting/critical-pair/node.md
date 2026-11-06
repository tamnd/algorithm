---
tag: D70CZQ
kind: definition
slug: critical-pair
name: Critical pair
aliases:
- critical overlap
- overlap
area: automata-and-parsing/term-rewriting
level: core
summary: A term obtained by overlapping two rules and rewriting the overlap in two ways.
prereqs: [term-rewriting-system, most-general-unifier, subterm]
see_also: [critical-pair-lemma, local-confluence, joinability, knuth-bendix-completion, orthogonal-rewrite-system, linearity]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 6, Section 6.2, Critical pairs (the definition, and the critical pairs of the group axioms); Chapter 7, Completion
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 2, First-order term rewriting systems (overlapping rules and critical pairs)
  - paper: "Donald E. Knuth and Peter B. Bendix, Simple word problems in universal algebras, in J. Leech (editor), Computational Problems in Abstract Algebra, Pergamon Press, 1970"
    locator: pp. 263 to 297 (superpositions of two reductions and the test of their consistency)
  - paper: doi:10.1145/322217.322230
    title: Gérard Huet, Confluent reductions, abstract properties and applications to term rewriting systems, Journal of the ACM 27(4) (1980)
    locator: pp. 797 to 821, Section 3 (critical pairs and the critical pair lemma)
---

A **critical pair** of a term rewriting system is a pair of terms that comes from one term that two rules can rewrite at overlapping places. The left-hand side of one rule is unified with a non-variable subterm of the left-hand side of another, and the most general such overlap is rewritten in the two possible ways. Critical pairs are the only places where a term rewriting system can lose [local confluence](/local-confluence/): by the [critical pair lemma](/critical-pair-lemma/), a system is locally confluent exactly when all its critical pairs are [joinable](/joinability/). They are the basic objects of the Knuth-Bendix confluence test and of [completion](/knuth-bendix-completion/).

## Definition

We use the notation of the term rewriting pages: terms $T(\Sigma, V)$, positions as sequences of positive integers with root $\varepsilon$, $t|_p$ the subterm at $p$, $t[s]_p$ the replacement, $\sigma$ and $\theta$ substitutions, rules $l \to r$ with $l \notin V$ and every variable of $r$ in $l$. $\mathrm{Pos}_\Sigma(l)$ is the set of positions of $l$ that hold a function symbol, not a variable.

Let $l_1 \to r_1$ and $l_2 \to r_2$ be two rules of a system $R$, renamed so that they have no variable in common. Let $p \in \mathrm{Pos}_\Sigma(l_1)$ and suppose that $l_1|_p$ and $l_2$ are [unifiable](/unification-problem/), with [most general unifier](/most-general-unifier/) $\theta$. If $p = \varepsilon$, require also that the two rules are not renamed copies of the same rule. Then the term $l_1\theta$ is an **overlap** (or superposition) of the two rules, and

$$\big\langle\, (l_1\theta)[r_2\theta]_p,\ \ r_1\theta \,\big\rangle$$

is a **critical pair** of $R$. The two components come from the two one-step reductions of the overlap:

$$(l_1\theta)[r_2\theta]_p \ \leftarrow\ l_1\theta \ \to\ r_1\theta,$$

the left one by $l_2 \to r_2$ at position $p$, the right one by $l_1 \to r_1$ at the root. $\mathrm{CP}(R)$ is the set of all critical pairs, taken over all ordered pairs of rules (including a rule with a renamed copy of itself) and all $p \in \mathrm{Pos}_\Sigma(l_1)$.

Remarks.

- **Why the exception at the root.** A rule overlapped with a copy of itself at $\varepsilon$ gives the pair $\langle r_1\theta, r_1\theta \rangle$, which is always joinable, so it is left out.
- **Why only non-variable positions.** If the second rule applies at or below a variable position of $l_1$, the peak is a variable overlap, and it is joinable for any rules (see [local confluence](/local-confluence/)). Only overlaps inside the function-symbol skeleton of $l_1$ can fail.
- **Why the most general unifier.** Let $\sigma$ be any substitution with $l_1|_p\sigma = l_2\sigma$ (the variables of the two rules are disjoint, so one substitution serves both). The peak $(l_1\sigma)[r_2\sigma]_p \leftarrow l_1\sigma \to r_1\sigma$ is then the instance $\langle s\tau, t\tau \rangle$ of the critical pair $\langle s, t \rangle$, where $\sigma = \theta\tau$ because $\theta$ is most general. So finitely many critical pairs stand for infinitely many peaks.
- **Finiteness.** A finite $R$ has finitely many critical pairs: at most $\sum_{l_1 \to r_1 \in R} |\mathrm{Pos}_\Sigma(l_1)| \cdot |R|$. They are computed by one unification for each choice of two rules and a position, and the result is unique up to renaming of variables.
- **Soundness.** Both components equal the overlap in the [equational theory](/equational-theory/) of $R$, so $s \leftrightarrow_R^* t$ for each critical pair $\langle s, t \rangle$. Adding $s \to t$ or $t \to s$ as a rule does not change the theory, which is why completion may add it.
- **Orientation.** Some books write the pair in the other order. Joinability is symmetric, so the order does not matter for the confluence test.

A critical pair $\langle s, t \rangle$ is **trivial** if $s = t$, and **joinable** if $s \downarrow_R t$.

## Examples and non-examples

**The group axioms.** Write $x \cdot y$ for multiplication, $i(x)$ for the inverse and $e$ for the unit, and take

$$(1)\ e \cdot x \to x, \qquad (2)\ i(x) \cdot x \to e, \qquad (3)\ (x \cdot y) \cdot z \to x \cdot (y \cdot z).$$

The non-variable positions of the left-hand sides are $\varepsilon$ and $1$ in (1), $\varepsilon$ and $1$ in (2), and $\varepsilon$ and $1$ in (3). No left-hand side unifies with $e$ or with $i(x)$, and at the root the left-hand sides of different rules do not unify. The left-hand side of (3) at position $1$ is $x \cdot y$, and it unifies with each of the three left-hand sides. So the system has exactly three critical pairs:

| rules | overlap $l_1\theta$ | inner step at $p = 1$ | root step by (3) |
|---|---|---|---|
| (3) with (1) | $(e \cdot y) \cdot z$ | $y \cdot z$ | $e \cdot (y \cdot z)$ |
| (3) with (2) | $(i(y) \cdot y) \cdot z$ | $e \cdot z$ | $i(y) \cdot (y \cdot z)$ |
| (3) with (3) | $((x \cdot y) \cdot z) \cdot w$ | $(x \cdot (y \cdot z)) \cdot w$ | $(x \cdot y) \cdot (z \cdot w)$ |

The first pair joins: $e \cdot (y \cdot z) \to y \cdot z$ by (1). The third joins: both sides reduce by (3) to $x \cdot (y \cdot (z \cdot w))$. The second does not: $e \cdot z \to z$, and $i(y) \cdot (y \cdot z)$ is a normal form. So the three axioms, read as rules, are not locally confluent, and [Knuth-Bendix completion](/knuth-bendix-completion/) adds the rule $i(y) \cdot (y \cdot z) \to z$, one of the seven rules of the ten-rule convergent system for groups that are not among the axioms.

**A rule with itself.** For the single rule $f(f(x)) \to g(x)$, rename a copy to $f(f(x')) \to g(x')$ and unify $f(x)$, the subterm at position $1$, with $f(f(x'))$: $\theta = \{x \mapsto f(x')\}$. The overlap is $f(f(f(x')))$, and the critical pair is $\langle f(g(x')), g(f(x')) \rangle$. Both terms are normal forms, so the pair is not joinable.

**A ground critical pair.** In $\{f(a) \to b,\ a \to c\}$, the subterm $a$ of $f(a)$ at position $1$ is itself a left-hand side, and the critical pair is $\langle f(c), b \rangle$, two distinct normal forms.

**No critical pairs: unary addition.** In $\mathit{add}(0, y) \to y$ and $\mathit{add}(s(x), y) \to s(\mathit{add}(x, y))$, the non-variable positions are $\varepsilon$ and $1$ in each left-hand side. At $\varepsilon$, $\mathit{add}(0, y)$ and $\mathit{add}(s(x'), y')$ clash on $0$ against $s$. At $1$, the subterms $0$ and $s(x)$ do not unify with any left-hand side, whose root is $\mathit{add}$. So there are no critical pairs, and the system is [orthogonal](/orthogonal-rewrite-system/).

**Non-example: a variable overlap.** In $\{f(x) \to g(x, x),\ a \to b\}$, the term $f(a)$ can be rewritten at $\varepsilon$ and at $1$, but position $1$ of $f(x)$ holds the variable $x$. This is not a critical overlap, and the system has no critical pairs. The peak $f(b) \leftarrow f(a) \to g(a, a)$ joins at $g(b, b)$.

**Non-example: unification fails only by the occurs check.** For $f(x, x) \to a$ and $f(x', g(x')) \to b$, the root overlap needs $x = x'$ and $x = g(x')$, so $x' = g(x')$, which has no solution. There is no critical pair. The system is still not confluent (with $c \to g(c)$ added, $f(c, c)$ reduces to $a$ and to $b$), and it is locally confluent, but its first rule is not [left-linear](/linearity/) and it does not terminate, so neither the [orthogonal confluence theorem](/orthogonal-confluence-theorem/) nor [Newman's lemma](/newman-lemma/) applies.

**The empty system** has no critical pairs.

## Related definitions

- The [critical pair lemma](/critical-pair-lemma/): $R$ is locally confluent iff all critical pairs are joinable. With [Newman's lemma](/newman-lemma/) this decides confluence of finite terminating systems.
- [Knuth-Bendix completion](/knuth-bendix-completion/) orients non-joinable critical pairs into new rules.
- An [orthogonal rewrite system](/orthogonal-rewrite-system/) is [left-linear](/linearity/) and has no critical pairs; such systems are confluent even without termination.
- [Joinability](/joinability/) and [local confluence](/local-confluence/) are the properties that critical pairs test.
- In completion with respect to an equational theory, the overlap uses [equational unification](/equational-unification/), and in theorem proving the same construction is the inference rule of [superposition](/superposition/).

## References
