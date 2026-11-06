---
tag: 22QFNE
kind: definition
slug: recursive-path-ordering
name: Recursive path ordering
aliases:
- RPO
- recursive path order
- multiset path ordering
- MPO
area: automata-and-parsing/term-rewriting
level: advanced
summary: A reduction ordering on terms generalising the lexicographic path ordering with status.
prereqs: [well-founded-reduction-ordering, multiset-ordering]
see_also: [lexicographic-path-ordering, knuth-bendix-ordering, multiset-ordering, termination, polynomial-interpretation, dependency-pairs, ackermann-function, primitive-recursive-function]
sources:
  - paper: doi:10.1016/0304-3975(82)90026-3
    title: Nachum Dershowitz, Orderings for term-rewriting systems, Theoretical Computer Science 17(3) (1982)
    locator: pp. 279 to 301 (the recursive path ordering and the proof that it is a well-founded simplification ordering)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 5.4, Simplification orders (path orders, multiset and lexicographic status)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 6, Termination (recursive path orders)
  - paper: doi:10.1016/0304-3975(92)90289-r
    title: Dieter Hofbauer, Termination proofs by multiset path orderings imply primitive recursive derivation lengths, Theoretical Computer Science 105(1) (1992)
    locator: pp. 129 to 140
  - paper: doi:10.1016/0304-3975(85)90175-6
    title: M. S. Krishnamoorthy and P. Narendran, On recursive path ordering, Theoretical Computer Science 40 (1985)
    locator: pp. 323 to 328 (finding a precedence is NP-complete)
---

The **recursive path ordering** (RPO) compares two terms by their root symbols first, using a fixed order on function symbols, the precedence, and then compares the arguments recursively. In its original form, the **multiset path ordering**, the arguments of two terms with the same root are compared as multisets, so their order does not matter. With **status**, each symbol chooses whether its arguments are compared as a multiset or lexicographically; the [lexicographic path ordering](/lexicographic-path-ordering/) is the case where all symbols have lexicographic status. The RPO is a [simplification ordering](/well-founded-reduction-ordering/), so a system whose rules all decrease in it is [terminating](/termination/).

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure. $\mathrm{Var}(t)$ is the set of variables of $t$.

A **precedence** is a strict partial order $\succ$ on $\Sigma$. A **status** assigns to each symbol either $\mathrm{mul}$ or $\mathrm{lex}$. For the version on this page, two terms are **permutatively equal**, $s \sim t$, if they are equal after reordering the arguments of symbols with multiset status; for a system without multiset status symbols, $\sim$ is syntactic equality. Write $s \succeq_{\mathrm{rpo}} t$ for $s \succ_{\mathrm{rpo}} t$ or $s \sim t$.

The **recursive path ordering** $\succ_{\mathrm{rpo}}$ is defined by induction on $|s| + |t|$: $s \succ_{\mathrm{rpo}} t$ iff $s = f(s_1, \ldots, s_m)$ and one of these holds.

1. **Subterm.** $s_i \succeq_{\mathrm{rpo}} t$ for some $i$.
2. **Bigger root.** $t = g(t_1, \ldots, t_n)$, $f \succ g$, and $s \succ_{\mathrm{rpo}} t_j$ for all $j$.
3. **Equal root, multiset status.** $t = f(t_1, \ldots, t_n)$, $f$ has status $\mathrm{mul}$, and $\{s_1, \ldots, s_m\} \succ_{\mathrm{rpo}}^{\mathrm{mul}} \{t_1, \ldots, t_n\}$ in the [multiset extension](/multiset-ordering/) of $\succ_{\mathrm{rpo}}$ (with $\sim$ as equality).
4. **Equal root, lexicographic status.** $t = f(t_1, \ldots, t_m)$, $f$ has status $\mathrm{lex}$, $(s_1, \ldots, s_m)$ is greater than $(t_1, \ldots, t_m)$ in the lexicographic extension of $\succ_{\mathrm{rpo}}$, and $s \succ_{\mathrm{rpo}} t_j$ for all $j$.

A variable is never greater than a term, and $s \succ_{\mathrm{rpo}} x$ for a variable $x$ iff $x \in \mathrm{Var}(s)$ and $s \ne x$; this follows from case 1. The side condition in case 4 is needed: without it, $f(s(x), y) \succ f(x, f(s(x), y))$ would hold, and the rule $f(s(x), y) \to f(x, f(s(x), y))$ does not terminate. Case 3 needs no such condition: if the argument multiset decreases, every $t_j$ is below some $s_i$, so $s \succ t_j$ by case 1.

**Main theorem (Dershowitz, 1982).** For any precedence and status, $\succ_{\mathrm{rpo}}$ is a simplification ordering: a strict order that is closed under contexts and substitutions and has the subterm property. If $\Sigma$ is finite, it is well-founded, and if the precedence is well-founded it is well-founded on any signature. So a system $R$ with $l \succ_{\mathrm{rpo}} r$ for all rules terminates.

*Proof outline.* The subterm property is case 1 with $t = s_i$. Closure under contexts: if $s \succ t$, then $f(\ldots, s, \ldots) \succ f(\ldots, t, \ldots)$ by case 3 (replace one element of the multiset by a smaller one) or by case 4 (the first difference is $s \succ t$, and the left side dominates each argument on the right, by case 1 for the others and by case 1 with $s \succ t$ for $t$). Closure under substitutions is by induction on $|s| + |t|$, case by case; case 1 with $t = x$ becomes $s_i\sigma \succeq x\sigma$. Transitivity is by induction on the sum of the three sizes. Irreflexivity is by induction on the size of $s$. Well-foundedness for finite $\Sigma$ then follows from the theorem that every simplification ordering over a finite signature is well-founded, which rests on Kruskal's tree theorem; see [reduction ordering](/well-founded-reduction-ordering/). $\blacksquare$

**Deciding the order.** For a given precedence and status, $s \succ_{\mathrm{rpo}} t$ is decidable in polynomial time by computing the answers for all pairs of subterms, smallest first; the multiset comparison of case 3 removes common elements up to $\sim$ and checks that each remaining $t_j$ is below some remaining $s_i$. Finding a precedence that orients a given system is NP-complete (Krishnamoorthy and Narendran, 1985); tools encode the search in SAT.

**Strength.** If a finite system is proved terminating by the multiset path ordering, then its derivation lengths are bounded by a [primitive recursive function](/primitive-recursive-function/) of the size of the start term (Hofbauer, 1992). The lexicographic path ordering proves termination of systems with much longer derivations, such as the [Ackermann function](/ackermann-function/).

## Examples and non-examples

All comparisons below were computed by a program that implements cases 1 to 4.

**Distributivity.** With $\times \succ +$ and multiset status, $x \times (y + z) \succ_{\mathrm{rpo}} (x \times y) + (x \times z)$. By case 2 the left side must dominate $x \times y$ and $x \times z$. For $x \times y$, case 3 compares $\{x, y + z\}$ with $\{x, y\}$: remove $x$, and $y + z \succ y$ by case 1. The same holds for $x \times z$.

**Multiset status is needed.** $f(s(x), y) \to f(y, x)$ terminates: the total number of symbols $s$ drops. With multiset status, $\{s(x), y\} \succ^{\mathrm{mul}} \{y, x\}$: remove $y$, and $s(x) \succ x$. With lexicographic status it fails, from left to right because $s(x)$ and $y$ are incomparable, and from right to left because $y$ and $x$ are. So this rule has an RPO proof but no LPO proof for any precedence.

**Lexicographic status is needed.** For $f(s(x), y) \to f(x, s(y))$, with $f \succ s$: the multiset comparison of $\{s(x), y\}$ with $\{x, s(y)\}$ fails, since $s(y)$ is below neither $s(x)$ nor $y$. The lexicographic comparison succeeds: $s(x) \succ x$ in the first place, and the left side dominates $x$ and $s(y)$. The same happens for the Ackermann function, $\mathit{ack}(0, y) \to s(y)$, $\mathit{ack}(s(x), 0) \to \mathit{ack}(x, s(0))$, $\mathit{ack}(s(x), s(y)) \to \mathit{ack}(x, \mathit{ack}(s(x), y))$, with $\mathit{ack} \succ s$ and lexicographic status for $\mathit{ack}$: all three rules decrease, while the multiset version fails on the second and third rule. This agrees with Hofbauer's bound, since the Ackermann function is not primitive recursive.

**Associativity.** $(x + y) + z \to x + (y + z)$ needs lexicographic status, left to right, for $+$: the multiset comparison of $\{x + y, z\}$ with $\{x, y + z\}$ fails, since $y + z$ is below neither $x + y$ nor $z$.

**Non-examples.**

- $f(x, y) \to f(y, x)$: no RPO orients it, and the rule does not terminate. With multiset status the two sides are permutatively equal, which is not a decrease.
- $f(f(x)) \to f(g(f(x)))$ terminates but no RPO orients it, since the RPO is a simplification ordering and the left side embeds in the right side.
- $x \to f(x)$ and $f(x) \to g(y)$ are not oriented: a variable is never greater than a term, and the right side has a variable that the left side lacks.

## Related definitions

- [Lexicographic path ordering](/lexicographic-path-ordering/): the RPO with lexicographic status for every symbol.
- [Multiset ordering](/multiset-ordering/): the extension that case 3 uses.
- [Reduction ordering](/well-founded-reduction-ordering/): the class of orders the RPO belongs to, and the proof that simplification orders are well-founded.
- [Knuth-Bendix ordering](/knuth-bendix-ordering/): a simplification ordering based on weights; it is incomparable in power with the RPO.
- [Polynomial interpretation](/polynomial-interpretation/): a termination method of a different kind, based on monotone functions.
- [Dependency pairs](/dependency-pairs/): uses path orders inside reduction pairs, often with argument filters.

## References
