---
tag: JHJMY6
kind: definition
slug: term-rewriting-system
name: Term rewriting system
aliases:
- TRS
- rewriting system
area: automata-and-parsing/term-rewriting
level: intro
summary: A set of oriented rules l -> r on terms, applied by replacing matched subterms.
prereqs: [rewrite-step, abstract-reduction-system]
see_also: [termination, confluence, normal-form, string-rewriting-system, orthogonal-rewrite-system, knuth-bendix-completion, equational-theory, reduction-strategy]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 4.2, Term rewriting systems; Chapter 2, Abstract reduction systems
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 2, First-order term rewriting systems; Chapter 3, Examples of TRSs and special rewriting formats
  - book: isbn:9780444880741
    title: Nachum Dershowitz and Jean-Pierre Jouannaud, Rewrite Systems, in J. van Leeuwen (editor), Handbook of Theoretical Computer Science, Volume B, Elsevier, 1990
    locator: pp. 243 to 320
---

A **term rewriting system** (TRS) is a set $R$ of [rewrite rules](/rewrite-rule/) $l \to r$ over a signature. It defines a one-step relation $\to_R$ on [terms](/term/): a term rewrites by replacing an instance of a left side by the same instance of the right side, anywhere in the term. Seen as an [abstract reduction system](/abstract-reduction-system/), a TRS is a model of computation as strong as Turing machines, a way to decide equational theories when it is [terminating](/termination/) and [confluent](/confluence/), and the core of functional languages, theorem provers and program transformers.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers with root $\varepsilon$, $t|_p$ and $t[s]_p$, substitutions $\sigma$ applied as $t\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure.

A **term rewriting system** is a pair $(\Sigma, R)$ of a signature and a set $R$ of rewrite rules over $\Sigma$: pairs $l \to r$ of terms with $l \notin V$ and $\mathrm{Var}(r) \subseteq \mathrm{Var}(l)$. When $\Sigma$ is clear we write $R$ for the system. Its **rewrite relation** is the [one-step relation](/rewrite-step/)

$$s \to_R t \iff \exists\, (l \to r) \in R,\ p \in \mathrm{Pos}(s),\ \sigma :\ s|_p = l\sigma \text{ and } t = s[r\sigma]_p.$$

So $(T(\Sigma, V), \to_R)$ is an abstract reduction system, and all its notions apply:

- $\to_R^+$ is the transitive closure and $\to_R^*$ the reflexive transitive closure; $s \to_R^* t$ reads "$s$ reduces to $t$".
- $\leftrightarrow_R^*$ is the reflexive, symmetric and transitive closure, the **conversion**. By the [Birkhoff completeness theorem](/birkhoff-completeness-theorem/), $s \leftrightarrow_R^* t$ iff the equation $s \approx t$ holds in every model of the rules read as equations.
- $t$ is a [normal form](/normal-form/) if no $u$ has $t \to_R u$; it is a normal form of $s$ if moreover $s \to_R^* t$.
- $s$ and $t$ are [joinable](/joinability/), $s \downarrow_R t$, if $s \to_R^* u\ {}_R^*\!\leftarrow t$ for some $u$.

The main properties of a TRS are properties of this relation:

- **terminating** (strongly normalizing): no infinite chain $t_0 \to_R t_1 \to_R \cdots$; see [termination](/termination/);
- **weakly normalizing**: each term has a normal form; see [weak normalization](/weak-normalization/);
- **confluent**: $t_1\ {}_R^*\!\leftarrow s \to_R^* t_2$ implies $t_1 \downarrow_R t_2$; see [confluence](/confluence/);
- **convergent** (complete, canonical): terminating and confluent. Then each term $s$ has exactly one normal form $s{\downarrow}_R$, and $s \leftrightarrow_R^* t$ iff $s{\downarrow}_R = t{\downarrow}_R$. This decides the [word problem](/word-problem/) of the equations when $R$ is finite.

**Classes of systems.** $R$ is **left-linear** if each left side is [linear](/linearity/); **orthogonal** if it is left-linear and has no [critical pairs](/critical-pair/) (see [orthogonal rewrite system](/orthogonal-rewrite-system/)); a **constructor system** if the symbols split into defined symbols, the roots of left sides, and constructors, and every argument of a left side is built from constructors and variables; **ground** if no rule has a variable. A [string rewriting system](/string-rewriting-system/) is a TRS over unary symbols.

**What is undecidable.** For finite TRSs, [termination](/undecidability-of-termination/), confluence (see [confluence decision problem](/confluence-decision-problem/)) and the [word problem](/undecidability-of-word-problem/) are undecidable in general. Confluence is decidable for terminating finite systems by the [critical pair lemma](/critical-pair-lemma/) and [Newman's lemma](/newman-lemma/).

## Examples and non-examples

**Arithmetic on Peano numerals.** Over $\{0/0, s/1, +/2, \times/2\}$:

$$0 + y \to y, \qquad s(x) + y \to s(x + y), \qquad x \times 0 \to 0, \qquad x \times s(y) \to (x \times y) + x.$$

This is an orthogonal constructor system. It is terminating and confluent, and the normal form of a ground term is the numeral of its value. For $2 \times 2$, written with numerals:

$$\begin{aligned} s(s(0)) \times s(s(0)) &\to (s(s(0)) \times s(0)) + s(s(0)) \to ((s(s(0)) \times 0) + s(s(0))) + s(s(0)) \\ &\to (0 + s(s(0))) + s(s(0)) \to s(s(0)) + s(s(0)) \to s(s(0) + s(s(0))) \\ &\to s(s(0 + s(s(0)))) \to s(s(s(s(0)))). \end{aligned}$$

From $s(s(0)) \times s(s(0))$ exactly 8 terms are reachable, each has at most one step, and every reduction to the normal form has 7 steps.

**Combinatory logic.** With one binary symbol $\cdot$ for application, written as juxtaposition with left association, and constants $S$ and $K$, the rules $S\,x\,y\,z \to x\,z\,(y\,z)$ and $K\,x\,y \to x$ form an orthogonal TRS that is Turing complete and not terminating: $S\,I\,I\,(S\,I\,I)$ with $I = S\,K\,K$ has an infinite reduction. See [combinatory logic](/combinatory-logic/).

**Groups.** The three group axioms $e \cdot x \approx x$, $i(x) \cdot x \approx e$ and $(x \cdot y) \cdot z \approx x \cdot (y \cdot z)$ do not form a confluent system when oriented left to right. [Knuth-Bendix completion](/knuth-bendix-completion/) turns them into a convergent system of ten rules, which decides the word problem of free groups.

**A system that is confluent but not terminating.** $R = \{a \to a\}$ is confluent and has the infinite reduction $a \to a \to \cdots$. The empty system $R = \emptyset$ is terminating and confluent, and every term is its own normal form.

**Non-examples.**

- A set of equations $\{x + 0 \approx x\}$ is not a TRS; it becomes one only after each equation is oriented.
- $\{x \to s(x)\}$ is not a TRS, since a left side is a variable.
- A Markov algorithm, which applies the first rule that matches at the leftmost place, is not a TRS: a TRS has no order on its rules, and each redex may be contracted. A TRS with a fixed [reduction strategy](/reduction-strategy/) is closer to it; see [Markov algorithm](/markov-algorithm/).

## Related definitions

- [Rewrite rule](/rewrite-rule/) and [rewrite step](/rewrite-step/): the parts that make up the relation.
- [Abstract reduction system](/abstract-reduction-system/): the general theory of a set with a relation.
- [Termination](/termination/), [confluence](/confluence/) and [normal form](/normal-form/): the main properties.
- [Equational theory](/equational-theory/): the equations that a TRS decides when it is convergent.
- [String rewriting system](/string-rewriting-system/): the special case of words.
- [Term graph rewriting](/term-graph-rewriting/): rewriting on graphs that share subterms, which implements a TRS.

## References
