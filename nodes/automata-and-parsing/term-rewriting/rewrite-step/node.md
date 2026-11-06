---
tag: 0WBJKD
kind: definition
slug: rewrite-step
name: Rewrite step (one-step reduction)
aliases:
- one-step reduction
- reduction step
area: automata-and-parsing/term-rewriting
level: intro
summary: Replacing one instance of a left-hand side at one position by the corresponding right-hand side.
prereqs: [rewrite-rule, subterm, term-matching]
see_also: [term-rewriting-system, term-context, reduction-strategy, parallel-rewriting, normal-form, narrowing, abstract-reduction-system, critical-pair]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 4.2, Term rewriting systems (the rewrite relation and its closure under substitutions and contexts)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 2, First-order term rewriting systems (reduction steps, redexes and contexts)
  - book: isbn:9780444880741
    title: Nachum Dershowitz and Jean-Pierre Jouannaud, Rewrite Systems, in J. van Leeuwen (editor), Handbook of Theoretical Computer Science, Volume B, Elsevier, 1990
    locator: pp. 243 to 320, Section 2 (the rewrite relation)
---

A **rewrite step** replaces one subterm of a term by another, using one [rewrite rule](/rewrite-rule/) $l \to r$: at some position $p$ the subterm is an instance $l\sigma$ of the left side, and the step puts $r\sigma$ in its place. The steps of all rules of a set $R$ form the one-step relation $\to_R$ of the [term rewriting system](/term-rewriting-system/), and a computation is a sequence of steps. One term can have many steps, at different positions and with different rules, and which one to take is the question of a [reduction strategy](/reduction-strategy/).

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers with root $\varepsilon$, $t|_p$ and $t[s]_p$, substitutions $\sigma$ applied as $t\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure of $\to_R$.

Let $R$ be a set of rewrite rules. A term $s$ **rewrites in one step** to $t$, written $s \to_R t$, iff there are a rule $l \to r \in R$, a position $p \in \mathrm{Pos}(s)$ and a substitution $\sigma$ with

$$s|_p = l\sigma \qquad\text{and}\qquad t = s[r\sigma]_p.$$

We also write $s \to_{p,\, l \to r} t$ to name the position and the rule. The subterm $s|_p$ is the **redex** and $p$ is the **redex position**; $r\sigma$ is the **contractum**. With a [context](/term-context/) $C = s[\square]_p$, the same step reads $C[l\sigma] \to_R C[r\sigma]$. A step at $p = \varepsilon$ is a **root step**, written $\to^{\varepsilon}$; a step at $p \ne \varepsilon$ is written $\to^{>\varepsilon}$.

Since each rule has $\mathrm{Var}(r) \subseteq \mathrm{Var}(l)$, the substitution $\sigma$ is fixed on all variables of $r$ by the match $l\sigma = s|_p$, so the triple (position, rule, $\sigma$) determines $t$. A redex is **innermost** if no proper subterm of it is a redex, and **outermost** if it is not a proper subterm of another redex.

**Closure properties.** $\to_R$ is the smallest relation on $T(\Sigma, V)$ that contains each rule $l \to r$ of $R$ and is

1. **closed under substitutions**: $s \to_R t$ implies $s\tau \to_R t\tau$ for every substitution $\tau$, and
2. **closed under contexts**: $s \to_R t$ implies $u[s]_q \to_R u[t]_q$ for every term $u$ and $q \in \mathrm{Pos}(u)$.

*Proof.* Let $s \to_{p, l \to r} t$ with $s|_p = l\sigma$. For item 1, $p \in \mathrm{Pos}(s)$, so $(s\tau)|_p = (s|_p)\tau = l(\sigma\tau)$ and $t\tau = (s[r\sigma]_p)\tau = (s\tau)[r(\sigma\tau)]_p$, by the facts on [subterms](/subterm/) and substitutions. So $s\tau \to_{p, l \to r} t\tau$ with the substitution $\sigma\tau$. For item 2, $(u[s]_q)|_{qp} = s|_p = l\sigma$ and $u[s]_q[r\sigma]_{qp} = u[s[r\sigma]_p]_q = u[t]_q$, so $u[s]_q \to_{qp, l \to r} u[t]_q$. Each rule is a step at $\varepsilon$ with the identity substitution, so $\to_R$ contains $R$. Conversely, let $\Rightarrow$ be any relation that contains $R$ and has both closure properties. A step $s \to_{p, l \to r} t$ is $s[l\sigma]_p \to s[r\sigma]_p$; from $l \Rightarrow r$, closure under substitutions gives $l\sigma \Rightarrow r\sigma$, and closure under contexts with $u = s$ and $q = p$ gives $s \Rightarrow t$. So $\to_R \subseteq\ \Rightarrow$. $\blacksquare$

A relation with both properties is a **rewrite relation**. Closure under substitutions is what makes it safe to prove a fact about terms with variables and use it for all instances; closure under contexts is what lets a step happen deep inside a term.

**Computing the steps of a term.** All one-step reducts of $s$ are found by trying each rule at each function position of $s$, with [term matching](/term-matching/). Matching $l$ against $s|_p$ takes $O(|l|)$ time, so the cost is $O\big(|s| \cdot \sum_{l \to r \in R} |l|\big)$ for the matches, plus the cost of building each result. A term has at most $|s| \cdot |R|$ steps. Indexes such as [discrimination trees](/discrimination-tree/) and the automaton of [Hoffmann-O'Donnell matching](/hoffmann-odonnell-matching/) find the redexes faster when $R$ is large.

## Examples and non-examples

**Two steps from one term.** Let $R = \{0 + y \to y,\ s(x) + y \to s(x + y)\}$ and $s = s(0) + (0 + s(0))$. There are two steps:

- at $\varepsilon$ with the second rule and $\sigma = \{x \mapsto 0, y \mapsto 0 + s(0)\}$: $s \to s(0 + (0 + s(0)))$;
- at position 2 with the first rule and $\sigma = \{y \mapsto s(0)\}$: $s \to s(0) + s(0)$.

The redex at 2 is innermost; the redex at $\varepsilon$ is outermost. All reductions from $s$ reach the [normal form](/normal-form/) $s(s(0))$, and the set of terms reachable from $s$ has 5 elements.

**Two different steps, one result.** The term $s(0 + (0 + s(0)))$ has a step at position 1, with redex $0 + (0 + s(0))$, and a step at position 1.2, with redex $0 + s(0)$. Both give $s(0 + s(0))$. A step is a triple of position, rule and substitution, so these are two steps, even though the relation $\to_R$ only records the pair of terms. Counting steps and tracing them (in proofs about [orthogonal systems](/orthogonal-rewrite-system/) and in the [standardization theorem](/standardization-theorem/)) needs the triples.

**A step inside a substitution.** With the rule $f(x) \to g(x, x)$ and the term $f(0 + s(0))$, a step at $\varepsilon$ gives $g(0 + s(0), 0 + s(0))$, which copies the redex $0 + s(0)$. Reducing the redex first gives $f(s(0)) \to g(s(0), s(0))$ in two steps, while the other order needs three.

**Non-examples.**

- Replacing both copies of $0 + s(0)$ in $g(0 + s(0), 0 + s(0))$ at once is not one step but two. A step that contracts several redexes at parallel positions is a [parallel rewriting](/parallel-rewriting/) step.
- With the rule $f(a) \to b$, the term $f(x)$ has no step: matching may instantiate the variables of the rule, not those of the term. Instantiating $x \mapsto a$ to make the step possible is [narrowing](/narrowing/).
- Replacing $r\sigma$ by $l\sigma$ is a step of the inverse relation $\leftarrow_R$, not of $\to_R$. Steps in both directions form the conversion $\leftrightarrow_R^*$ used in the [word problem](/word-problem/).

## Related definitions

- [Rewrite rule](/rewrite-rule/): the pairs $l \to r$ that steps apply.
- [Term rewriting system](/term-rewriting-system/): the set $R$ and the relation $\to_R$ as an [abstract reduction system](/abstract-reduction-system/).
- [Context](/term-context/): the term with a hole in which a step happens.
- [Normal form](/normal-form/): a term with no step.
- [Reduction strategy](/reduction-strategy/): a rule that picks one step among those that exist.
- [Parallel rewriting](/parallel-rewriting/): several steps at parallel positions at once.
- [Critical pair](/critical-pair/): two steps whose redexes overlap.

## References
