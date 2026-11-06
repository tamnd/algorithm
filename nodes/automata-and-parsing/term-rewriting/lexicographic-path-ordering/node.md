---
tag: S7HDQW
kind: definition
slug: lexicographic-path-ordering
name: Lexicographic path ordering
aliases:
- LPO
area: automata-and-parsing/term-rewriting
level: advanced
summary: A reduction ordering on terms comparing root symbols by precedence and arguments lexicographically.
prereqs: [well-founded-reduction-ordering, lexicographic-order, termination]
see_also: [recursive-path-ordering, knuth-bendix-ordering, multiset-ordering, polynomial-interpretation, knuth-bendix-completion, dependency-pairs, ackermann-function, normal-form-computation]
sources:
  - paper: doi:10.1016/0304-3975(82)90026-3
    title: Nachum Dershowitz, Orderings for term-rewriting systems, Theoretical Computer Science 17(3) (1982)
    locator: pp. 279 to 301 (simplification orderings, their well-foundedness, and the recursive path ordering)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 5, Termination (Section 5.4, simplification orders, including the lexicographic path order and its well-foundedness)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 6, Termination (recursive path orders with lexicographic status)
  - paper: doi:10.1016/0304-3975(94)00135-6
    title: Andreas Weiermann, Termination proofs for term rewriting systems by lexicographic path orderings imply multiply recursive derivation lengths, Theoretical Computer Science 139 (1995)
    locator: pp. 355 to 362
  - paper: doi:10.1016/0304-3975(85)90175-6
    title: M. S. Krishnamoorthy and P. Narendran, On recursive path ordering, Theoretical Computer Science 40 (1985)
    locator: pp. 323 to 328 (NP-completeness of finding a precedence)
---

The **lexicographic path ordering** (LPO) is an order on terms built from an order on function symbols, the precedence. A term is greater than another if one of its arguments is already at least as large, or if its root symbol is greater and it dominates every argument of the other term, or if the roots are equal and the arguments are greater from left to right. The LPO is a [well-founded reduction ordering](/well-founded-reduction-ordering/), so a [term rewriting system](/term-rewriting-system/) terminates if every rule $l \to r$ has $l >_{\mathrm{lpo}} r$. It was proposed by Kamin and Lévy in 1980 as a variant of Dershowitz's [recursive path ordering](/recursive-path-ordering/), and it proves [termination](/termination/) of the Ackermann function and of the completed group axioms, which the multiset version cannot.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, $t|_p$ and $t[s]_p$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$. $\mathrm{Var}(t)$ is the set of variables of $t$.

A **precedence** is a strict partial order $>$ on $\Sigma$. The **lexicographic path ordering** $>_{\mathrm{lpo}}$ induced by $>$ is defined by induction on $|s| + |t|$: $s >_{\mathrm{lpo}} t$ iff one of these holds.

1. $t \in \mathrm{Var}(s)$ and $t \ne s$.
2. $s = f(s_1, \ldots, s_n)$ and $s_i \ge_{\mathrm{lpo}} t$ for some $i$, where $\ge_{\mathrm{lpo}}$ means $>_{\mathrm{lpo}}$ or syntactic equality.
3. $s = f(s_1, \ldots, s_n)$, $t = g(t_1, \ldots, t_m)$, $f > g$, and $s >_{\mathrm{lpo}} t_j$ for all $j$.
4. $s = f(s_1, \ldots, s_n)$, $t = f(t_1, \ldots, t_n)$, $s >_{\mathrm{lpo}} t_j$ for all $j$, and there is a $k$ with $s_i = t_i$ for $i < k$ and $s_k >_{\mathrm{lpo}} t_k$.

Case 4 is the [lexicographic](/lexicographic-order/) comparison of the argument tuples. A variable is greater than no term. Case 1 follows from case 2 when $s$ is not a variable, and is listed for clarity.

**Theorem.** For every precedence $>$:

- $>_{\mathrm{lpo}}$ is a strict partial order, closed under contexts ($s >_{\mathrm{lpo}} t$ implies $u[s]_p >_{\mathrm{lpo}} u[t]_p$) and under substitutions ($s >_{\mathrm{lpo}} t$ implies $s\sigma >_{\mathrm{lpo}} t\sigma$), and it has the subterm property ($s >_{\mathrm{lpo}} s|_p$ for $p \ne \varepsilon$). So it is a simplification ordering.
- $s >_{\mathrm{lpo}} t$ implies $\mathrm{Var}(t) \subseteq \mathrm{Var}(s)$.
- If $\Sigma$ is finite, $>_{\mathrm{lpo}}$ is well-founded. So it is a reduction ordering.
- If $>$ is total, $>_{\mathrm{lpo}}$ is total on ground terms.

The first two items are proved by induction on the sizes of the terms involved; Dershowitz proved that every simplification ordering on a finite signature is well-founded, by Kruskal's tree theorem. The direct proof below avoids Kruskal's theorem.

*Proof of well-foundedness.* A chain $s_0 >_{\mathrm{lpo}} s_1 >_{\mathrm{lpo}} \cdots$ only uses the variables of $s_0$, by the second item. Treat these finitely many variables as new constants that are incomparable with all symbols in the precedence; then cases 1 and 2 coincide, and it is enough to show that there is no infinite chain of ground terms over a finite signature. Call a term **accessible** if no infinite chain starts at it. If $s$ is accessible and $s >_{\mathrm{lpo}} t$, then $t$ is accessible. On accessible terms, $>_{\mathrm{lpo}}$ is well-founded, so its lexicographic extension to $n$-tuples of accessible terms is well-founded.

*Claim:* if $s_1, \ldots, s_n$ are accessible, then $s = f(s_1, \ldots, s_n)$ is accessible. Proceed by induction on the pair $(f, (s_1, \ldots, s_n))$, ordered first by the precedence, which is well-founded because $\Sigma$ is finite, and then by the lexicographic extension on accessible tuples. It suffices to show that every $t$ with $s >_{\mathrm{lpo}} t$ is accessible; do this by an inner induction on the size of $t$.

- Case 2, $s_i \ge_{\mathrm{lpo}} t$: $t$ is accessible because $s_i$ is.
- Case 3, $t = g(t_1, \ldots, t_m)$ with $f > g$ and $s >_{\mathrm{lpo}} t_j$: each $t_j$ is smaller than $t$, so it is accessible by the inner induction. Then $t$ is accessible by the outer induction, because $g$ is below $f$.
- Case 4, $t = f(t_1, \ldots, t_n)$ with $s >_{\mathrm{lpo}} t_j$ and $(s_1, \ldots, s_n)$ lexicographically greater than $(t_1, \ldots, t_n)$: the $t_j$ are accessible by the inner induction, and $t$ is accessible by the outer induction, because its tuple is smaller.

By the claim and induction on terms, every ground term is accessible. $\blacksquare$

**Deciding the order.** For a fixed precedence, $s >_{\mathrm{lpo}} t$ can be decided in time polynomial in $|s| + |t|$ by [memoizing](/memoization/) the answers for pairs of subterms; the recursion as written can repeat work exponentially often. Deciding whether **some** precedence makes $l >_{\mathrm{lpo}} r$ for every rule of a finite system is NP-complete (Krishnamoorthy and Narendran proved this for the recursive path ordering, 1985). Termination tools search for the precedence with a [SAT solver](/sat/).

Because $>_{\mathrm{lpo}}$ grows when the precedence grows, a system that is oriented with some partial precedence is also oriented with each total precedence that extends it. So to test a system it is enough to try the total precedences.

## Examples and non-examples

**Associativity.** With any precedence, $(x \cdot y) \cdot z >_{\mathrm{lpo}} x \cdot (y \cdot z)$. Both roots are $\cdot$, so case 4 applies. The first arguments give $x \cdot y >_{\mathrm{lpo}} x$, a subterm. The left side also dominates each argument of the right side: $x$ is a subterm, and $(x \cdot y) \cdot z >_{\mathrm{lpo}} y \cdot z$ by case 4 again, since $x \cdot y >_{\mathrm{lpo}} y$ and $y$ and $z$ are subterms.

**Addition.** With $+ > s$, the rules $0 + y \to y$ and $s(x) + y \to s(x + y)$ decrease. For the second: case 3 gives $s(x) + y >_{\mathrm{lpo}} s(x + y)$ if $s(x) + y >_{\mathrm{lpo}} x + y$, which holds by case 4, since $s(x) >_{\mathrm{lpo}} x$.

**Ackermann's function.** With $A > s$, the rules

$$A(0, y) \to s(y), \qquad A(s(x), 0) \to A(x, s(0)), \qquad A(s(x), s(y)) \to A(x, A(s(x), y))$$

all decrease. For the third rule, case 4 compares $s(x)$ with $x$ in the first argument, and the left side dominates $x$ and, by case 4 on the second argument, $A(s(x), y)$. The [Ackermann function](/ackermann-function/) is not primitive recursive, so by Hofbauer's bound for the multiset path ordering no multiset path ordering orients these rules, and derivation lengths under the LPO are not primitive recursive in general.

**Groups.** The ten rules of the convergent system for groups, from $e \cdot x \to x$ and $(x \cdot y) \cdot z \to x \cdot (y \cdot z)$ to $i(x \cdot y) \to i(y) \cdot i(x)$, all decrease with $i > \cdot > e$. For the last rule, case 3 applies, since $i > \cdot$, and $i(x \cdot y) >_{\mathrm{lpo}} i(y)$ by case 4. This is the precedence used for [Knuth-Bendix completion](/knuth-bendix-completion/) of the group axioms.

**Distributivity.** With $\times > +$, $x \times (y + z) >_{\mathrm{lpo}} (x \times y) + (x \times z)$, although the right side is larger and duplicates $x$.

**Non-example: commutativity.** No precedence gives $x + y >_{\mathrm{lpo}} y + x$, and no reduction ordering can, since then $y + x > x + y$ by substitution, a contradiction with irreflexivity and transitivity. Commutativity is handled by [rewriting modulo equations](/rewriting-modulo-equations/).

**Non-example: a terminating system that is not simply terminating.** The rule $f(f(x)) \to f(g(f(x)))$ terminates, but its left side is embedded in its right side, so no simplification ordering, and no LPO, orients it. [Dependency pairs](/dependency-pairs/) prove its termination.

**Non-example: not total on terms with variables.** For distinct variables, $x + y$ and $y + x$ are incomparable, and $f(x)$ and $g(y)$ are incomparable whatever the precedence, because each has a variable the other lacks.

## Related definitions

- The [recursive path ordering](/recursive-path-ordering/) compares equal roots by the [multiset ordering](/multiset-ordering/) of the arguments; the LPO uses the lexicographic order. Allowing each symbol its own status, multiset or lexicographic, gives the RPO with status, which contains both. The multiset version does not orient associativity.
- The [Knuth-Bendix ordering](/knuth-bendix-ordering/) compares weights first and uses the precedence only to break ties. The two orders are incomparable in power: KBO orients no rule that duplicates a variable, and the LPO does not orient $f(g(x)) \to g(f(f(x)))$ under any precedence, which KBO orients.
- A [polynomial interpretation](/polynomial-interpretation/) is another way to build a reduction ordering; it gives derivation lengths at most double exponential, while LPO allows multiply recursive ones (Weiermann, 1995).
- [Knuth-Bendix completion](/knuth-bendix-completion/) needs a reduction ordering to orient new equations; the LPO with a total precedence is the usual choice, since it is total on ground terms.

## References
