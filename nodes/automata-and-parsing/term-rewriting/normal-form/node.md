---
tag: NMHE29
kind: definition
slug: normal-form
name: Normal form
aliases:
- irreducible term
area: automata-and-parsing/term-rewriting
level: intro
summary: A term to which no rewrite rule applies.
prereqs: [abstract-reduction-system, term-rewriting-system]
see_also: [normal-form-computation, confluence, termination, weak-normalization, innermost-reduction, outermost-reduction, joinability, rewrite-step]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 2, Abstract Reduction Systems (Section 2.1, Equivalence and reduction, the definitions of normal form, normalizing and terminating); Chapter 3 (Section 3.4, Term rewriting systems)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 1, Abstract reduction systems (normal forms, the properties WN, SN and UN); Chapter 2, First-order term rewriting systems
  - book: isbn:9780198537618
    title: Jan Willem Klop, Term rewriting systems, in S. Abramsky, D. M. Gabbay and T. S. E. Maibaum (editors), Handbook of Logic in Computer Science, Volume 2, Oxford University Press, 1992
    locator: pp. 1 to 116, Section 1 (abstract reduction systems and their normal forms)
---

A **normal form** is an element that cannot be rewritten any further: in an [abstract reduction system](/abstract-reduction-system/) it has no successor, and in a [term rewriting system](/term-rewriting-system/) it is a term in which no subterm matches the left-hand side of a rule. A normal form of a term is a normal form that the term reduces to. Evaluating a program in a rewriting language means computing a normal form, and [confluence](/confluence/) and [termination](/termination/) are exactly the properties that make each term have one normal form, and make it reachable by any reduction order.

## Definition

**Notation.** The term rewriting pages of this site share one notation. A signature $\Sigma$ is a set of function symbols, each with an arity; $V$ is a countable set of variables, disjoint from $\Sigma$; $T(\Sigma, V)$ is the set of terms built from them. A position is a finite sequence of positive integers, the root is the empty sequence $\varepsilon$, $\mathrm{Pos}(t)$ is the set of positions of $t$, $t|_p$ is the subterm of $t$ at $p$, and $t[s]_p$ is $t$ with that subterm replaced by $s$. A substitution $\sigma$ maps variables to terms, and $t\sigma$ is the result of applying it. A rule is written $l \to r$. For a relation $\to$, $\to^*$ is its reflexive transitive closure, $\to^+$ its transitive closure, $\leftarrow$ its inverse and $\leftrightarrow^*$ its reflexive, symmetric and transitive closure.

**In an abstract reduction system.** Let $(A, \to)$ be an abstract reduction system, that is, a set $A$ with a binary relation $\to \subseteq A \times A$.

- An element $x \in A$ is **in normal form** (or **irreducible**) if there is no $y \in A$ with $x \to y$. The set of normal forms is $\mathrm{NF}(\to)$.
- An element $y$ is **a normal form of** $x$ if $x \to^* y$ and $y \in \mathrm{NF}(\to)$. If $x$ has exactly one normal form, it is written $x{\downarrow}$.
- $x$ is **normalizing** (or weakly normalizing) if it has at least one normal form. The relation $\to$ is normalizing if each element is.
- $\to$ has **unique normal forms** if no element has two different normal forms.

**In a term rewriting system.** Let $R$ be a set of rules $l \to r$ over $T(\Sigma, V)$, where $l$ is not a variable and each variable of $r$ occurs in $l$. A **redex** of $t$ is a position $p \in \mathrm{Pos}(t)$ such that $t|_p = l\sigma$ for some rule $l \to r \in R$ and some substitution $\sigma$. Then $t \to_R t[r\sigma]_p$ is a [rewrite step](/rewrite-step/), and

$$t \in \mathrm{NF}(\to_R) \iff \text{no } p \in \mathrm{Pos}(t),\ l \to r \in R \text{ and } \sigma \text{ satisfy } t|_p = l\sigma.$$

So a term is in normal form exactly when no subterm is an instance of a left-hand side. For a finite $R$ this is decidable: for each position and each rule, test whether $l$ [matches](/term-matching/) $t|_p$. With a naive matcher the test takes $O(|t| \cdot \sum_{l \to r \in R} |l|)$ time.

Two facts link normal forms to the two main properties of rewriting.

- If $\to$ is [confluent](/confluence/), then each element has at most one normal form. If $x \to^* y_1$ and $x \to^* y_2$ with $y_1, y_2$ normal forms, confluence gives $z$ with $y_1 \to^* z$ and $y_2 \to^* z$. A normal form reduces only to itself, so $y_1 = z = y_2$.
- If $\to$ is [terminating](/termination/), then each element has at least one normal form: follow any path of steps from $x$; it is finite, and its last element is a normal form of $x$.

A system that is both is **convergent** (or complete, or canonical), and then each element $x$ has exactly one normal form $x{\downarrow}$. In that case $x \leftrightarrow^* y$ holds if and only if $x{\downarrow} = y{\downarrow}$, which is how a convergent system decides its [equational theory](/equational-theory/).

## Examples and non-examples

**Addition on unary numbers.** Let $R$ have the rules

$$\mathit{add}(0, y) \to y, \qquad \mathit{add}(s(x), y) \to s(\mathit{add}(x, y)).$$

Then $\mathit{add}(s(s(0)), s(0)) \to s(\mathit{add}(s(0), s(0))) \to s(s(\mathit{add}(0, s(0)))) \to s(s(s(0)))$. Each of the first three terms has exactly one redex, at positions $\varepsilon$, $1$ and $1.1$. The last term has no subterm of the form $\mathit{add}(\ldots)$, so it is a normal form, and it is the normal form of the first term. The normal forms of this system that have no variables are exactly the terms $s^k(0)$. The term $\mathit{add}(x, 0)$ is also a normal form: no rule applies until $x$ is replaced by $0$ or by $s(\ldots)$.

**Two normal forms.** With the rules $f(x, y) \to x$ and $f(x, y) \to y$ and constants $a, b, c$, the term $f(a, f(b, c))$ has the three normal forms $a$, $b$ and $c$. The system terminates, since each step makes the term smaller, but it is not confluent, so the normal form is not unique and $x{\downarrow}$ is not defined.

**No normal form.** With the single rule $a \to a$, the constant $a$ has no normal form: its only successor is $a$ again. With $f(x) \to f(f(x))$, no term that contains $f$ has a normal form, because each step keeps a redex at the root.

**A normal form that a bad strategy misses.** With $a \to a$ and $g(x) \to b$, the term $g(a)$ has the normal form $b$, reached in one step at the root. But the infinite sequence $g(a) \to g(a) \to \cdots$ exists too. So $g(a)$ is normalizing but not terminating, and a strategy that always reduces arguments first, like [innermost reduction](/innermost-reduction/), never finds $b$. [Outermost reduction](/outermost-reduction/) finds it.

**Non-linear left-hand sides.** With the rule $\mathit{eq}(x, x) \to \mathit{true}$, the term $\mathit{eq}(a, b)$ is a normal form, because no substitution makes $\mathit{eq}(x, x)$ equal to it, while $\mathit{eq}(f(a), f(a))$ is not.

**The empty system.** If $R = \emptyset$, every term is a normal form, and each term is its own unique normal form.

**Non-example: a variable on the left.** A rule $x \to r$ would make every term reducible, so no term would be a normal form. This is one reason the definition of a rewrite rule forbids a variable as the left-hand side.

**Non-example: normal form of a different relation.** A term in normal form for $\to_R$ need not be in normal form for a larger system, and "the normal form of $t$" means nothing until the relation is fixed. In the [lambda calculus](/lambda-calculus/), $\lambda x.\, (\lambda y.\, y)\, x$ is a [beta](/beta-reduction/) redex inside a body, so it is not a beta normal form, although it is in weak head normal form, the notion that lazy functional languages use.

## Related definitions

- [Normal form computation](/normal-form-computation/) is the problem of computing a normal form of a given term; [innermost](/innermost-reduction/) and [outermost reduction](/outermost-reduction/) are two strategies for it.
- [Termination](/termination/) (strong normalization) says that every reduction sequence is finite. [Weak normalization](/weak-normalization/) says that each element has some normal form.
- [Confluence](/confluence/) and [joinability](/joinability/) give the uniqueness of normal forms; [Newman's lemma](/newman-lemma/) reduces confluence of a terminating system to [local confluence](/local-confluence/).
- In the [lambda calculus](/lambda-calculus/), the normal form of a term is the result of the program, and by the [Church-Rosser theorem](/church-rosser-theorem/) it is unique when it exists.
- A [Markov algorithm](/markov-algorithm/) and a [string rewriting system](/string-rewriting-system/) use the same notion on strings: a string to which no rule applies.

## References
