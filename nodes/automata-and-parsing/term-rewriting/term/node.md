---
tag: KHMRHF
kind: definition
slug: term
name: Term
aliases:
- First-order term
- first-order term
area: automata-and-parsing/term-rewriting
level: intro
summary: A labelled finite tree over a signature of function symbols and variables.
prereqs: [rooted-tree]
see_also: [subterm, term-context, substitution, term-algebra, term-matching, rewrite-rule, term-rewriting-system, term-dag]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 3.1, Terms, substitutions, and identities
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 2, First-order term rewriting systems (terms, positions, contexts and substitutions)
  - book: isbn:9780444880741
    title: Nachum Dershowitz and Jean-Pierre Jouannaud, Rewrite Systems, in J. van Leeuwen (editor), Handbook of Theoretical Computer Science, Volume B, Elsevier, 1990
    locator: pp. 243 to 320, Section 2 (syntax of terms, positions and substitutions)
---

A **term** is a finite ordered tree whose inner nodes carry function symbols, each with as many children as its arity, and whose leaves carry constants or variables. Terms are the objects that a [rewrite rule](/rewrite-rule/) changes, that [term matching](/term-matching/) and [unification](/unification-problem/) compare, and that a compiler stores as an [abstract syntax tree](/abstract-syntax-tree/). This page fixes the notation that all the term rewriting pages use.

## Definition

A **signature** $\Sigma$ is a set of function symbols, each with an **arity** $\mathrm{ar}(f) \in \mathbb{N}$. $\Sigma_n$ is the set of symbols of arity $n$, and a symbol of arity 0 is a **constant**. $V$ is a countably infinite set of **variables**, disjoint from $\Sigma$.

The set $T(\Sigma, V)$ of **terms** is the smallest set such that

1. each variable $x \in V$ is a term, and
2. if $f \in \Sigma_n$ and $t_1, \ldots, t_n$ are terms, then $f(t_1, \ldots, t_n)$ is a term.

For a constant $a$ we write $a$ and not $a()$. A **ground term** has no variable. $T(\Sigma) = T(\Sigma, \emptyset)$ is the set of ground terms; it is not empty exactly when $\Sigma_0 \ne \emptyset$. Two terms are equal when they are the same tree: $f(t_1, \ldots, t_n) = g(u_1, \ldots, u_m)$ iff $f = g$, $n = m$ and $t_i = u_i$ for each $i$. So $f(a, b) \ne f(b, a)$ even when $f$ is meant to be commutative.

**Positions.** A position is a finite sequence of positive integers; $\varepsilon$ is the empty sequence and $pq$ is concatenation. The set of positions of a term is

$$\mathrm{Pos}(x) = \{\varepsilon\}, \qquad \mathrm{Pos}(f(t_1, \ldots, t_n)) = \{\varepsilon\} \cup \{\, i p \mid 1 \le i \le n,\ p \in \mathrm{Pos}(t_i) \,\}.$$

The **subterm** at position $p$ is $t|_\varepsilon = t$ and $f(t_1, \ldots, t_n)|_{ip} = t_i|_p$. The term $t[s]_p$ is $t$ with the subterm at $p$ replaced by $s$. Position $p$ is **above** $q$, written $p \le q$, when $q = p p'$ for some $p'$; $p$ and $q$ are **parallel**, written $p \parallel q$, when neither is above the other. The **size** of $t$ is $|t| = |\mathrm{Pos}(t)|$, its **height** is the largest length of a position, and $\mathrm{Var}(t)$ is the set of variables in $t$. A term is **linear** when no variable occurs in it twice. See [subterm](/subterm/) for the properties of positions.

**Notation of the term rewriting pages.** All pages of this area use: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers with root $\varepsilon$, $t|_p$ and $t[s]_p$ as above, substitutions $\sigma$ (maps from $V$ to $T(\Sigma, V)$ that move finitely many variables) applied in postfix as $t\sigma$, rules $l \to r$, $\to_R$ for the one-step relation of a rule set $R$, and $\to_R^*$ for its reflexive transitive closure.

**Many-sorted terms.** In a many-sorted signature each symbol has a type $f : s_1 \times \cdots \times s_n \to s$ over a set of sorts, each variable has a sort, and $f(t_1, \ldots, t_n)$ is a term of sort $s$ only when each $t_i$ has sort $s_i$. The pages of this area use one sort unless they say otherwise.

## Examples and non-examples

**A term and its positions.** Let $\Sigma = \{f/2, g/1, a/0\}$ and $t = f(g(x), f(a, x))$. Then $|t| = 6$, the height is 2, $\mathrm{Var}(t) = \{x\}$, and $t$ is not linear, since $x$ occurs at positions 1.1 and 2.2.

| position $p$ | $t\vert_p$ |
|---|---|
| $\varepsilon$ | $f(g(x), f(a, x))$ |
| 1 | $g(x)$ |
| 1.1 | $x$ |
| 2 | $f(a, x)$ |
| 2.1 | $a$ |
| 2.2 | $x$ |

Replacing at position 2 gives $t[b]_2 = f(g(x), b)$ for a new constant $b$. Positions 1.1 and 2 are parallel; position 2 is above 2.1 and 2.2.

**Peano numerals.** With $\Sigma = \{0/0, s/1, +/2\}$, the number 3 is the ground term $s(s(s(0)))$, and $s(x) + y$ (infix for $+(s(x), y)$) is a term with two variables. The [term rewriting system](/term-rewriting-system/) for addition works on these terms.

**Counting ground terms.** Over $\{f/2, g/1, a/0\}$, let $N(h)$ be the number of ground terms of height at most $h$. A term of height at most $h + 1$ is $a$, or $g(u)$, or $f(u, v)$ with $u, v$ of height at most $h$, so $N(0) = 1$ and $N(h + 1) = 1 + N(h) + N(h)^2$. This gives $1, 3, 13, 183, 33673$ for $h = 0$ to $4$: the number grows doubly exponentially in the height. The number of ground terms of size $n$ is $1, 1, 2, 4, 9, 21, 51, 127, 323$ for $n = 1$ to $9$, the Motzkin numbers, because these terms are exactly the ordered trees whose nodes have 0, 1 or 2 children.

**Size against sharing.** Let $t_0 = a$ and $t_{k+1} = f(t_k, t_k)$. Then $|t_k| = 2^{k+1} - 1$, but $t_k$ has only $k + 1$ distinct subterms. A [term DAG](/term-dag/) built with [hash-consing](/hash-consing/) stores $t_k$ in $k + 1$ nodes. Algorithms on terms are often stated for trees, and their cost on DAGs can be exponentially smaller.

**Strings as terms.** A word $abc$ over an alphabet becomes the term $a(b(c(x)))$ over unary symbols, with a variable for the rest of the word. This is how a [string rewriting system](/string-rewriting-system/) becomes a term rewriting system.

**Non-examples.**

- $f(a)$ is not a term when $f$ has arity 2: the arity fixes the number of children.
- $x(a)$ is not a first-order term: a variable has no arguments. Terms with variables in function position belong to the [lambda calculus](/lambda-calculus/) and to higher-order rewriting, where matching and unification behave differently ([higher-order unification](/higher-order-unification-problem/) is undecidable).
- The infinite tree $g(g(g(\cdots)))$ is not a term, because terms are finite. Infinitary rewriting studies such trees.
- $\lambda x.\, f(x)$ is not a first-order term: binders are not part of the syntax, and terms with bound variables are equal up to renaming, which first-order terms are not.

## Related definitions

- [Subterm](/subterm/): the term at a position, and the subterm order.
- [Context](/term-context/): a term with a hole, which says where a rewrite step happens.
- [Substitution](/substitution/): a map from variables to terms, extended to all terms.
- [Term algebra](/term-algebra/): the terms as an algebra, with each symbol acting as a constructor. The ground terms form the [Herbrand universe](/herbrand-universe/).
- [Rewrite rule](/rewrite-rule/) and [term rewriting system](/term-rewriting-system/): pairs of terms used as replacement rules.
- [Term matching](/term-matching/) and the [unification problem](/unification-problem/): solve $s\sigma = t$ and $s\sigma = t\sigma$.
- [Rooted tree](/rooted-tree/) and [abstract syntax tree](/abstract-syntax-tree/): the general tree notions that terms specialize.

## References
