---
tag: ZJQ5ZM
kind: definition
slug: rewrite-rule
name: Rewrite rule
aliases:
- reduction rule
- rule
area: automata-and-parsing/term-rewriting
level: intro
summary: An oriented equation l -> r whose left side is matched inside a term and replaced by the instance of r.
prereqs: [term, substitution]
see_also: [rewrite-step, term-rewriting-system, term-matching, linearity, equational-theory, termination, string-rewriting-system, critical-pair]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 4.2, Term rewriting systems (rewrite rules and the conditions on their variables)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 2, First-order term rewriting systems (rewrite rules, and the classes of left-linear, collapsing and duplicating rules)
  - book: isbn:9780444880741
    title: Nachum Dershowitz and Jean-Pierre Jouannaud, Rewrite Systems, in J. van Leeuwen (editor), Handbook of Theoretical Computer Science, Volume B, Elsevier, 1990
    locator: pp. 243 to 320, Section 2 (rewrite rules)
---

A **rewrite rule** is a pair of [terms](/term/) $l \to r$, read "replace $l$ by $r$". Its left side $l$ is a pattern: wherever an instance $l\sigma$ occurs inside a term, a [rewrite step](/rewrite-step/) may replace it by $r\sigma$, with the same [substitution](/substitution/) $\sigma$. A rule is an equation used in one direction only, and a set of rules is a [term rewriting system](/term-rewriting-system/). Two conditions on the variables of a rule keep it from producing terms out of nothing.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, substitutions $\sigma$ applied as $t\sigma$, rules $l \to r$, and $\to^*$ for the reflexive transitive closure.

A **rewrite rule** over $\Sigma$ is a pair $(l, r)$ of terms in $T(\Sigma, V)$, written $l \to r$, such that

1. $l \notin V$: the left side is not a variable, and
2. $\mathrm{Var}(r) \subseteq \mathrm{Var}(l)$: each variable of the right side occurs in the left side.

$l$ is the **left side** (left-hand side) and $r$ is the **right side**. An **instance** of the rule is the pair $l\sigma \to r\sigma$ for a substitution $\sigma$; the term $l\sigma$ is a **redex** (reducible expression) and $r\sigma$ is its **contractum**. A **variant** of the rule is $l\rho \to r\rho$ for a renaming $\rho$, a substitution that is a bijection on $V$. Variants define the same rewrite steps, so rules are taken up to renaming, and two rules are "renamed apart" when they share no variable.

An **equation** $l \approx r$ is a pair used in both directions; a rule is an oriented equation. To turn equations into rules, each equation must be oriented so that the conditions hold and the resulting system terminates, which is the job of a [reduction ordering](/well-founded-reduction-ordering/) in [completion](/knuth-bendix-completion/).

**Classes of rules.** A rule $l \to r$ is

- **left-linear** if no variable occurs twice in $l$, and **right-linear** if none occurs twice in $r$ (see [linearity](/linearity/));
- **collapsing** if $r$ is a variable;
- **erasing** if $\mathrm{Var}(r) \ne \mathrm{Var}(l)$, so some variable of $l$ is lost;
- **duplicating** if some variable occurs more often in $r$ than in $l$;
- a **constructor rule** if the symbols of $\Sigma$ split into defined symbols and constructors, the root of $l$ is defined, and the arguments of $l$ contain only constructors and variables.

Checking the two conditions takes $O(|l| + |r|)$ time: collect $\mathrm{Var}(l)$ in a hash set, then scan $r$.

**Why the two conditions.** Each condition rules out a rule that never terminates.

- If $l = x$, every term $t$ is an instance $x\{x \mapsto t\}$, so every term is a redex, and $t \to r\{x \mapsto t\}$ applies again to the result. No term is in [normal form](/normal-form/).
- If $y \in \mathrm{Var}(r) \setminus \mathrm{Var}(l)$, take any substitution $\sigma$ and let $\tau$ agree with $\sigma$ except that $y\tau = l\sigma$. Since $y \notin \mathrm{Var}(l)$, $l\tau = l\sigma$, and the contractum $r\tau$ contains $l\tau$ as a subterm at each occurrence of $y$. So the step $l\tau \to r\tau$ can repeat inside its own result forever. The value of $y$ is also not determined by the redex, so the result of a step is not a function of the redex.

Some texts drop the conditions and treat such rules as allowed but non-terminating; the pages of this area use the definition above.

**Conditional rules.** A conditional rule $l \to r \Leftarrow s_1 = t_1, \ldots, s_k = t_k$ applies to $l\sigma$ only if each condition $s_i\sigma = t_i\sigma$ holds, usually in the sense $s_i\sigma \downarrow t_i\sigma$ (both have a common reduct). They are not treated on these pages beyond this remark.

## Examples and non-examples

**Addition on Peano numerals.** Over $\{0/0, s/1, +/2\}$, the two rules

$$0 + y \to y, \qquad s(x) + y \to s(x + y)$$

are rewrite rules: neither left side is a variable, and $\mathrm{Var}(y) \subseteq \{y\}$ and $\mathrm{Var}(s(x + y)) \subseteq \{x, y\}$. The first rule is collapsing. With $\sigma = \{x \mapsto s(0), y \mapsto s(0)\}$, the second rule has the instance $s(s(0)) + s(0) \to s(s(0) + s(0))$. Both rules are left-linear constructor rules.

**Multiplication.** The rules $x \times 0 \to 0$ and $x \times s(y) \to (x \times y) + x$ are rewrite rules. The first is erasing, because $x$ is lost. The second is duplicating, because $x$ occurs once on the left and twice on the right: the instance with $x \mapsto s(s(0))$ copies the subterm $s(s(0))$. Duplicating rules are the reason why innermost and outermost strategies cost different numbers of steps; see [reduction strategy](/reduction-strategy/).

**A non-left-linear rule.** $\mathit{eq}(x, x) \to \mathit{true}$ is a rule. It applies to $\mathit{eq}(s(0), s(0))$, where both arguments are the same term, and not to $\mathit{eq}(0, s(0))$. Matching it needs a test of syntactic equality of two subterms.

**Non-examples.**

- $x \to x + 0$ is not a rule, because its left side is a variable. Every term would be a redex, and $t \to t + 0 \to (t + 0) + 0 \to \cdots$.
- $f(x) \to g(y)$ is not a rule, because $y$ is not in the left side. With $\sigma = \{x \mapsto a, y \mapsto f(a)\}$, the instance $f(a) \to g(f(a))$ gives $f(a) \to g(f(a)) \to g(g(f(a))) \to \cdots$.
- $x + y \to y + x$ meets both conditions, so it is a rule, but every system with it is non-terminating: $a + b \to b + a \to a + b$. Commutativity is handled by [rewriting modulo equations](/rewriting-modulo-equations/), not by a rule.

## Related definitions

- [Rewrite step](/rewrite-step/): one application of a rule at one position.
- [Term rewriting system](/term-rewriting-system/): a set of rules and the relation $\to_R$ that it defines.
- [Term matching](/term-matching/): finds the $\sigma$ with $l\sigma = t|_p$, the test that decides whether a rule applies.
- [Linearity](/linearity/): left-linear and right-linear rules, and why left-linearity matters for confluence.
- [Equational theory](/equational-theory/): equations $l \approx r$ used in both directions.
- [String rewriting system](/string-rewriting-system/): rules $u \to v$ on words.
- [Critical pair](/critical-pair/): the overlap of two left sides, where two rules compete.

## References
