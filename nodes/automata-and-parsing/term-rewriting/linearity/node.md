---
tag: BM5ZGV
kind: definition
slug: linearity
name: Left-linearity
aliases:
- left-linear rule
- linear rule
area: automata-and-parsing/term-rewriting
level: advanced
summary: A rule whose left-hand side has no repeated variable.
prereqs: [rewrite-rule, term, term-matching]
see_also: [orthogonal-rewrite-system, critical-pair-lemma, orthogonal-confluence-theorem, hoffmann-odonnell-matching, confluence, term-rewriting-system, tree-pattern-matching, termination]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 6, Confluence (left-linear and orthogonal systems)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 2, First-order term rewriting systems (linear, left-linear, non-erasing and non-duplicating rules); Chapter 4, Orthogonality
  - paper: doi:10.1145/322217.322230
    title: Gérard Huet, Confluent reductions, abstract properties and applications to term rewriting systems, Journal of the ACM 27(4) (1980)
    locator: pp. 797 to 821, Section 3 (confluence of linear and left-linear systems with closed critical pairs, and the counterexample without left-linearity)
  - paper: doi:10.1016/0020-0190(87)90122-0
    title: Yoshihito Toyama, Counterexamples to termination for the direct sum of term rewriting systems, Information Processing Letters 25(3) (1987)
    locator: pp. 141 to 143
---

A rewrite rule is **left-linear** if no variable occurs twice in its left-hand side. Then applying the rule only needs to check the shape of the term, not to compare two subterms for equality, and a rewrite step inside the part matched by a variable never destroys the match. Most of the theory of confluence without termination, in particular the [orthogonal confluence theorem](/orthogonal-confluence-theorem/), and most fast matching methods, such as [bottom-up tree automata](/hoffmann-odonnell-matching/), need left-linearity. Right-linearity and the related non-duplicating condition play the same role for termination.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, $t|_p$ and $t[s]_p$, substitutions $\sigma$, rules $l \to r$ with $l \notin V$ and $\mathrm{Var}(r) \subseteq \mathrm{Var}(l)$, and $\to_R^*$. For a term $t$ and a variable $x$, let $|t|_x$ be the number of positions $p$ with $t|_p = x$.

- A term $t$ is **linear** if $|t|_x \le 1$ for every variable $x$.
- A rule $l \to r$ is **left-linear** if $l$ is linear, **right-linear** if $r$ is linear, and **linear** if both.
- A rule is **non-erasing** if $\mathrm{Var}(r) = \mathrm{Var}(l)$, and **non-duplicating** if $|r|_x \le |l|_x$ for every $x$.
- A [term rewriting system](/term-rewriting-system/) $R$ has one of these properties if every rule of $R$ has it.

A right-linear rule with a linear left side is non-duplicating; a left-linear rule is non-duplicating iff it is right-linear.

**Why left-linearity matters.** Let $l$ be linear and $l\sigma = s$. If one rewrites $s$ at a position below a variable occurrence of $l$, say inside $x\sigma$ at the only occurrence of $x$, the result is $l\sigma'$, where $\sigma'$ differs from $\sigma$ only at $x$. So the redex survives with a new substitution. For a non-linear left side $f(x, x)$, rewriting one of the two copies of $x\sigma$ gives $f(u, u')$ with $u \ne u'$, and the redex is gone. This is the variable-overlap case of the [critical pair lemma](/critical-pair-lemma/), and it is the reason why critical pairs alone do not control confluence for non-left-linear systems that do not terminate.

## Examples and non-examples

**Left-linear.** $\mathit{add}(s(x), y) \to s(\mathit{add}(x, y))$ is linear. $d(x) \to p(x, x)$ is left-linear but not right-linear, so it duplicates $x$. $\mathit{fst}(x, y) \to x$ is linear and erasing.

**Not left-linear.** $\mathit{eq}(x, x) \to \mathit{true}$ and $x - x \to 0$ repeat $x$ on the left. Matching them needs an equality test of two subterms, which costs time proportional to their size unless terms are [hash-consed](/hash-consing/).

**No critical pairs, not confluent (Huet).** $R = \{ f(x, x) \to a,\ f(x, g(x)) \to b,\ c \to g(c) \}$ has no critical pairs, since $x \approx g(x)$ has no unifier. Yet $f(c, c) \to a$ and $f(c, c) \to f(c, g(c)) \to b$, two different normal forms. The first rule is not left-linear: after $c \to g(c)$ in one argument, its redex disappears. A left-linear system without critical pairs is [orthogonal](/orthogonal-rewrite-system/), and orthogonal systems are confluent.

**Duplication and termination (Toyama).** $R_1 = \{ f(a, b, x) \to f(x, x, x) \}$ and $R_2 = \{ g(x, y) \to x,\ g(x, y) \to y \}$ are each terminating, and they share no function symbol. Their union is not terminating:

$$f(a, b, g(a, b)) \to f(g(a, b), g(a, b), g(a, b)) \to f(a, g(a, b), g(a, b)) \to f(a, b, g(a, b)).$$

The rule of $R_1$ is duplicating. When both systems are non-duplicating, termination of the disjoint union follows from termination of each part (Rusinowitch, 1987).

**Ground instances.** The set of ground instances of a linear term is recognized by a finite tree automaton, which is why [tree pattern matching](/tree-pattern-matching/) and [Hoffmann and O'Donnell's matching](/hoffmann-odonnell-matching/) handle linear patterns. The ground instances of $f(x, x)$ form a set that no finite bottom-up tree automaton recognizes: such an automaton has finitely many states, so two different ground terms $u \ne u'$ reach the same state, and then it accepts $f(u, u')$ iff it accepts $f(u, u)$.

**Non-example: repetition across rules.** Linearity is about one rule at a time. The system $\{ f(x) \to x,\ g(x, y) \to y \}$ is linear even though $x$ occurs in two rules; variables of different rules are unrelated.

## Related definitions

- An [orthogonal rewrite system](/orthogonal-rewrite-system/) is a left-linear system without critical pairs; it is confluent by the [orthogonal confluence theorem](/orthogonal-confluence-theorem/), with or without termination.
- Huet (1980) showed that a linear system whose critical pairs $\langle s, t \rangle$ are strongly closed ($s \to^{=} \cdot \leftarrow^* t$ and $t \to^{=} \cdot \leftarrow^* s$, where $\to^=$ is at most one step) is confluent, and that a left-linear system is confluent if each critical pair $\langle s, t \rangle$, with $s$ the side from the inner step and $t$ the side from the root step, satisfies $s \Rightarrow t$ for one parallel step (parallel closed).
- [Term matching](/term-matching/) of a linear pattern is a single simultaneous walk of pattern and term; a non-linear pattern adds equality tests.
- In [narrowing](/narrowing/) and in [rewriting modulo equations](/rewriting-modulo-equations/), left-linearity is again the condition under which many completeness results hold.
- Non-duplicating systems are the setting of modularity results for [termination](/termination/), as in Toyama's example above.

## References
